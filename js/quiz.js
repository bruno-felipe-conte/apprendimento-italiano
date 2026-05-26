// ============================================================
// quiz.js — Quiz system with multiple choice questions
// ============================================================

const Quiz = {
  temploAtual: null,
  perguntas: [],       // 10 questions for this session
  perguntaAtual: 0,
  pontuacao: 0,
  xpTotal: 0,
  respondido: false,

  // ── Start quiz for a temple ────────────────────────────────
  iniciar(temploNum) {
    if (!Progressao.temploDesbloqueado(temploNum)) {
      App.notificar('Tempio não desbloqueado!', 'erro');
      return;
    }

    this.temploAtual = temploNum;
    this.perguntaAtual = 0;
    this.pontuacao = 0;
    this.xpTotal = 0;
    this.respondido = false;

    // Try to get quiz questions for this temple from the JSON data
    let pool = App.estado.quizData.filter(q => q.templo === temploNum);

    // If no quiz JSON data for this temple, generate questions from vocabulary
    if (pool.length === 0) {
      pool = this._gerarPerguntas(temploNum);
    }

    // Shuffle and take up to 10
    this.perguntas = this._embaralhar(pool).slice(0, 10);

    if (this.perguntas.length === 0) {
      App.notificar('Nenhuma pergunta disponível para este tempio.', 'alerta');
      return;
    }

    // Show quiz container, hide selector and resultado
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    const seletor = document.getElementById('quiz-templo-selector');
    if (container) container.style.display = 'block';
    if (resultado) resultado.style.display = 'none';
    if (seletor) seletor.style.display = 'none';

    this.mostrarPergunta();
  },

  // ── Generate vocab questions if no JSON quiz data ──────────
  _gerarPerguntas(temploNum) {
    const data = App.estado.templosData[temploNum];
    if (!data || !data.palavras || data.palavras.length < 4) return [];

    const palavras = data.palavras;
    const perguntas = [];

    palavras.forEach(p => {
      // Build 3 wrong alternatives from other words in the same temple
      const outras = palavras.filter(o => o.id !== p.id);
      const erradas = this._embaralhar(outras).slice(0, 3).map(o => o.portugues);
      const alternativas = this._embaralhar([p.portugues, ...erradas]);

      perguntas.push({
        id: `gen_${p.id}`,
        templo: temploNum,
        tipo: 'vocabulario',
        nivel: data.nivel || 'A1',
        pergunta: `O que significa "${p.italiano}"?`,
        resposta_correta: p.portugues,
        alternativas: alternativas,
        explicacao: p.exemplo
          ? `"${p.italiano}" significa "${p.portugues}". Exemplo: ${p.exemplo}`
          : `"${p.italiano}" significa "${p.portugues}".`,
        xp_recompensa: 20
      });
    });

    return perguntas;
  },

  // ── Display current question ───────────────────────────────
  mostrarPergunta() {
    if (this.perguntaAtual >= this.perguntas.length) {
      this.mostrarResultado();
      return;
    }

    const p = this.perguntas[this.perguntaAtual];
    this.respondido = false;

    // Update progress bar
    const total = this.perguntas.length;
    const pct = Math.round(((this.perguntaAtual) / total) * 100);
    const barFill = document.getElementById('quiz-barra-fill');
    const numLabel = document.getElementById('quiz-num-pergunta');
    if (barFill) barFill.style.width = Math.max(5, pct) + '%';
    if (numLabel) numLabel.textContent = `Pergunta ${this.perguntaAtual + 1} de ${total}`;

    // Question type badge
    const tipoBadge = document.getElementById('quiz-tipo');
    if (tipoBadge) tipoBadge.textContent = p.tipo || 'Vocabolario';

    // Question text
    const perguntaEl = document.getElementById('quiz-pergunta');
    if (perguntaEl) perguntaEl.textContent = p.pergunta;

    // Hide explanation
    const explicacaoContainer = document.getElementById('explicacao-container');
    if (explicacaoContainer) explicacaoContainer.style.display = 'none';

    // Render options
    const grid = document.getElementById('opcoes-grid');
    if (!grid) return;
    grid.innerHTML = '';

    // Shuffle alternatives for display
    const alternativas = this._embaralhar([...(p.alternativas || [])]);
    alternativas.forEach(alt => {
      const btn = document.createElement('button');
      btn.className = 'opcao-btn';
      btn.textContent = alt;
      btn.onclick = () => this.checarResposta(alt);
      grid.appendChild(btn);
    });
  },

  // ── Check the selected answer ─────────────────────────────
  checarResposta(escolha) {
    if (this.respondido) return;
    this.respondido = true;

    const p = this.perguntas[this.perguntaAtual];
    const correto = escolha === p.resposta_correta;

    // Mark all buttons
    const grid = document.getElementById('opcoes-grid');
    if (grid) {
      grid.querySelectorAll('.opcao-btn').forEach(btn => {
        btn.disabled = true;
        if (btn.textContent === p.resposta_correta) {
          btn.classList.add('correta');
        } else if (btn.textContent === escolha && !correto) {
          btn.classList.add('errada');
        }
      });
    }

    if (correto) {
      this.pontuacao++;
      this.xpTotal += (p.xp_recompensa || 20);
    }

    // Show explanation
    const explicacaoContainer = document.getElementById('explicacao-container');
    const explicacaoEl = document.getElementById('quiz-explicacao');
    if (explicacaoContainer) explicacaoContainer.style.display = 'block';
    if (explicacaoEl) explicacaoEl.textContent = p.explicacao || (correto ? '✅ Corretto!' : `❌ La risposta corretta era: ${p.resposta_correta}`);
  },

  // ── Advance to next question ───────────────────────────────
  proximaPergunta() {
    this.perguntaAtual++;
    if (this.perguntaAtual >= this.perguntas.length) {
      this.mostrarResultado();
    } else {
      this.mostrarPergunta();
    }
  },

  // ── Show final result screen ───────────────────────────────
  mostrarResultado() {
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    if (container) container.style.display = 'none';
    
    // Log quiz completion to heatmap diary (count actual questions answered)
    if (typeof Calor !== 'undefined') Calor.registrar(this.perguntas.length || 1);
    if (!resultado) return;
    resultado.style.display = 'block';

    const total = this.perguntas.length;
    const pct = total > 0 ? Math.round((this.pontuacao / total) * 100) : 0;

    // Choose message based on score
    let msg = '';
    if (pct >= 90) msg = '🏆 Perfetto! Sei un maestro dell\'italiano!';
    else if (pct >= 70) msg = '👏 Molto bene! Continua così!';
    else if (pct >= 50) msg = '📚 Bene! Ma puoi fare di meglio!';
    else msg = '💪 Non mollare! Continua a studiare!';

    const scoreEl = document.getElementById('resultado-score');
    const xpEl = document.getElementById('resultado-xp');
    const msgEl = document.getElementById('resultado-msg');
    if (scoreEl) scoreEl.textContent = `${this.pontuacao}/${total}`;
    if (xpEl) xpEl.textContent = `+${this.xpTotal} XP ganhos`;
    if (msgEl) msgEl.textContent = msg;

    // Give XP (without XP toast — resultado screen is enough feedback)
    if (this.xpTotal > 0) {
      Progressao.ganhar(this.xpTotal);
    }

    // Save to quiz history
    try {
      const historico = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]');
      historico.unshift({
        templo: this.temploAtual,
        pontuacao: pct,
        xp_ganho: this.xpTotal,
        acertos: this.pontuacao,
        total: total,
        data: Date.now()
      });
      // Keep only last 50 entries
      localStorage.setItem('it_quiz_historico', JSON.stringify(historico.slice(0, 50)));
    } catch (e) { /* ignore */ }
  },

  // ── Return to temple selector ──────────────────────────────
  voltarSelector() {
    const resultado = document.getElementById('quiz-resultado');
    const seletor = document.getElementById('quiz-templo-selector');
    if (resultado) resultado.style.display = 'none';
    if (seletor) seletor.style.display = 'grid';
    this.renderizarSeletor();
  },

  // ── Render the temple selector buttons ────────────────────
  renderizarSeletor() {
    const seletor = document.getElementById('quiz-templo-selector');
    if (!seletor) return;
    seletor.innerHTML = '';
    seletor.style.display = 'grid';

    for (let i = 1; i <= 10; i++) {
      const desbloqueado = Progressao.temploDesbloqueado(i);
      const data = App.estado.templosData[i];
      const nome = data ? data.nome : `Tempio ${i}`;
      const nivel = data ? data.nivel : '—';

      const btn = document.createElement('button');
      btn.className = `quiz-templo-btn${desbloqueado ? '' : ' bloqueado'}`;
      btn.innerHTML = desbloqueado
        ? `🏛️ ${i}. ${nome}<br><small>${nivel}</small>`
        : `🔒 Tempio ${i}<br><small>Nível ${Progressao.TEMPLO_NIVEL[i] || i}</small>`;

      if (desbloqueado) {
        btn.onclick = () => this.iniciar(i);
      } else {
        btn.disabled = true;
      }

      seletor.appendChild(btn);
    }
  },

  // ── Utility: Fisher-Yates shuffle ─────────────────────────
  _embaralhar(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }
};
