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
  combo: 0,

  // ── Start quiz for a temple ────────────────────────────────
  iniciar(temploNum) {
    if (!Progressao.temploDesbloqueado(temploNum)) {
      App.notificar('notif_quiz_bloqueado', 'erro');
      return;
    }

    // Restaura sessão parcial se for o mesmo templo
    const salvo = this._carregarSessao();
    if (salvo && salvo.temploAtual === temploNum && salvo.perguntaAtual > 0 && salvo.perguntas?.length > 0) {
      Object.assign(this, salvo);
      const container = document.getElementById('quiz-container');
      const resultado  = document.getElementById('quiz-resultado');
      const seletor    = document.getElementById('quiz-templo-selector');
      if (container) container.style.display = 'block';
      if (resultado)  resultado.style.display  = 'none';
      if (seletor)    seletor.style.display     = 'none';
      App.notificar(`↩️ Retomando da pergunta ${this.perguntaAtual + 1}`, 'alerta');
      this.mostrarPergunta();
      return;
    }

    this.temploAtual = temploNum;
    this.perguntaAtual = 0;
    this.pontuacao = 0;
    this.xpTotal = 0;
    this.respondido = false;
    this.combo = 0;

    // Try to get quiz questions for this temple from the JSON data
    let pool = App.estado.quizData.filter(q => q.templo === temploNum);

    // If no quiz JSON data for this temple, generate questions from vocabulary
    if (pool.length === 0) {
      pool = this._gerarPerguntas(temploNum);
    }

    // Shuffle and take up to 10
    this.perguntas = this._embaralhar(pool).slice(0, 10);

    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_sem_perguntas', 'alerta');
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

  // ── Start mixed quiz (all unlocked temples) ────────────────
  iniciarMisto() {
    this.temploAtual = 'misto';
    this.perguntaAtual = 0;
    this.pontuacao = 0;
    this.xpTotal = 0;
    this.respondido = false;
    this.combo = 0;

    let pool = [];
    const desbloqueados = App.estado.progresso ? App.estado.progresso.templos_desbloqueados : [1];
    
    desbloqueados.forEach(temploNum => {
      let tPool = App.estado.quizData.filter(q => q.templo === temploNum);
      if (tPool.length === 0) tPool = this._gerarPerguntas(temploNum);
      pool = pool.concat(tPool);
    });

    this.perguntas = this._embaralhar(pool).slice(0, 10);

    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_sem_perguntas_todos', 'alerta');
      return;
    }

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
        pergunta: I18n.idioma === 'it' ? `Cosa significa "${p.italiano}"?` : `O que significa "${p.italiano}"?`,
        resposta_correta: p.portugues,
        alternativas: alternativas,
        explicacao: p.exemplo
          ? (I18n.idioma === 'it' ? `"${p.italiano}" significa "${p.portugues}". Esempio: ${p.exemplo}` : `"${p.italiano}" significa "${p.portugues}". Exemplo: ${p.exemplo}`)
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
    this._atualizarCombo();

    // Update progress bar
    const total = this.perguntas.length;
    const pct = Math.round(((this.perguntaAtual) / total) * 100);
    const barFill = document.getElementById('quiz-barra-fill');
    const numLabel = document.getElementById('quiz-num-pergunta');
    if (barFill) barFill.style.width = Math.max(5, pct) + '%';
    if (numLabel) numLabel.textContent = I18n.t('quiz_pergunta_de').replace('{a}', this.perguntaAtual + 1).replace('{b}', total);

    // Question type badge
    const tipoBadge = document.getElementById('quiz-tipo');
    if (tipoBadge) tipoBadge.textContent = p.tipo || 'Vocabolario';

    // Question text
    const perguntaEl = document.getElementById('quiz-pergunta');
    if (perguntaEl) {
      perguntaEl.textContent = p.pergunta;
      if (p.italiano) perguntaEl.dataset.italiano = p.italiano;
      else delete perguntaEl.dataset.italiano;
    }

    const btnOuvir = document.getElementById('btn-ouvir-quiz');
    if (btnOuvir) {
      if (p.tipo === 'listening') {
        btnOuvir.style.display = 'flex';
        // Auto play audio when question appears
        if (p.italiano) setTimeout(() => { if (typeof App !== 'undefined' && App.pronunciar) App.pronunciar(p.italiano); }, 400);
      } else {
        btnOuvir.style.display = 'none';
      }
    }

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
      this.combo++;
      // XP multiplier: combo 1-2 = ×1, combo 3-4 = ×2, combo 5+ = ×3
      const mult = this.combo >= 5 ? 3 : this.combo >= 3 ? 2 : 1;
      const xpBase = p.xp_recompensa || 20;
      this.xpTotal += xpBase * mult;
      if (typeof SomFeedback !== 'undefined') SomFeedback.correto();
    } else {
      this.combo = 0;
      if (typeof SomFeedback !== 'undefined') SomFeedback.errado();
    }
    this._atualizarCombo();

    // Show explanation
    const explicacaoContainer = document.getElementById('explicacao-container');
    const explicacaoEl = document.getElementById('quiz-explicacao');
    if (explicacaoContainer) explicacaoContainer.style.display = 'block';
    if (explicacaoEl) explicacaoEl.textContent = p.explicacao || (correto ? I18n.t('quiz_correto') : `${I18n.t('quiz_resposta_correta_era')} ${p.resposta_correta}`);
  },

  // ── Advance to next question ───────────────────────────────
  proximaPergunta() {
    this.perguntaAtual++;
    if (this.perguntaAtual >= this.perguntas.length) {
      this.mostrarResultado();
    } else {
      this._salvarSessao(); // persiste progresso parcial
      this.mostrarPergunta();
    }
  },

  // ── Show final result screen ───────────────────────────────
  // ── Persiste / restaura sessão parcial ────────────────────
  _salvarSessao() {
    try {
      sessionStorage.setItem('it_quiz_sessao', JSON.stringify({
        temploAtual:   this.temploAtual,
        perguntas:     this.perguntas,
        perguntaAtual: this.perguntaAtual,
        pontuacao:     this.pontuacao,
        xpTotal:       this.xpTotal,
        combo:         this.combo,
      }));
    } catch(_) {}
  },

  _carregarSessao() {
    try {
      const raw = sessionStorage.getItem('it_quiz_sessao');
      return raw ? JSON.parse(raw) : null;
    } catch(_) { return null; }
  },

  _limparSessao() {
    try { sessionStorage.removeItem('it_quiz_sessao'); } catch(_) {}
  },

  mostrarResultado() {
    this._limparSessao(); // sessão concluída — limpa
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
    if (xpEl) xpEl.textContent = I18n.t('quiz_xp_ganhos').replace('{n}', this.xpTotal);
    if (msgEl) msgEl.textContent = msg;

    // Give XP (without XP toast — resultado screen is enough feedback)
    if (this.xpTotal > 0) {
      Progressao.ganhar(this.xpTotal);
    }

    // Check achievements
    if (typeof Conquistas !== 'undefined') {
      const p = App.estado.progresso;
      if (p) {
        if (pct >= 80) p.quiz_consecutivos_80 = (p.quiz_consecutivos_80 || 0) + 1;
        else p.quiz_consecutivos_80 = 0;
        App.salvarProgresso();
      }
      if (pct === 100) Conquistas.ganharQuizPerfetto();
      Conquistas.verificar();
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

    // ── Misto Button ───────────────────────────────────────
    if (Progressao.temploDesbloqueado(1)) {
      const btnMisto = document.createElement('button');
      btnMisto.className = 'quiz-templo-btn';
      btnMisto.innerHTML = '🌍 Quiz Generale<br><small>Tutti i templi misti</small>';
      btnMisto.style.gridColumn = '1 / -1'; // span full width
      btnMisto.style.background = 'linear-gradient(135deg, #2C3E50, #3498DB)';
      btnMisto.style.color = 'white';
      btnMisto.onclick = () => this.iniciarMisto();
      seletor.appendChild(btnMisto);
    }

    // Usa a lista de templos carregados (1-50), ordenados
    const todosTemplos = Object.keys(App.estado.templosData)
      .map(Number).sort((a, b) => a - b);

    todosTemplos.forEach(i => {
      const desbloqueado = Progressao.temploDesbloqueado(i);
      const data = App.estado.templosData[i];
      const nome = (data && data.nome) || `Tempio ${i}`;
      const nivel = data ? data.nivel : '—';

      const btn = document.createElement('button');
      btn.className = `quiz-templo-btn${desbloqueado ? '' : ' bloqueado'}`;
      btn.innerHTML = desbloqueado
        ? `🏛️ ${i}. ${nome}<br><small>${nivel}</small>`
        : `🔒 ${i}. ${nome}<br><small>Livello ${Progressao.TEMPLO_NIVEL[i] || i}</small>`;

      if (desbloqueado) btn.onclick = () => this.iniciar(i);
      else btn.disabled = true;
      seletor.appendChild(btn);
    });

    // ── Morphology section ────────────────────────────────
    const sep = document.createElement('div');
    sep.className = 'quiz-secao-titulo';
    sep.textContent = I18n.t('quiz_morf_titulo');
    seletor.appendChild(sep);

    todosTemplos.forEach(i => {
      const desbloqueado = Progressao.temploDesbloqueado(i);
      const data = App.estado.templosData[i];
      const nome = (data && data.nome) || `Tempio ${i}`;
      const temMorf = data && data.palavras && data.palavras.some(p => p.genero || p.plural);

      const btn = document.createElement('button');
      btn.className = `quiz-templo-btn quiz-morf-btn${desbloqueado && temMorf ? '' : ' bloqueado'}`;
      btn.innerHTML = `🔤 ${i}. ${nome}`;

      if (desbloqueado && temMorf) btn.onclick = () => this.iniciarMorfologia(i);
      else btn.disabled = true;
      seletor.appendChild(btn);
    });

    // ── Listening section ────────────────────────────────
    const sepList = document.createElement('div');
    sepList.className = 'quiz-secao-titulo';
    sepList.textContent = I18n.t('quiz_list_titulo');
    seletor.appendChild(sepList);

    todosTemplos.forEach(i => {
      const desbloqueado = Progressao.temploDesbloqueado(i);
      const data = App.estado.templosData[i];
      const nome = (data && data.nome) || `Tempio ${i}`;

      const btn = document.createElement('button');
      btn.className = `quiz-templo-btn quiz-list-btn${desbloqueado ? '' : ' bloqueado'}`;
      btn.innerHTML = `🎧 ${i}. ${nome}`;

      if (desbloqueado) btn.onclick = () => this.iniciarListening(i);
      else btn.disabled = true;
      seletor.appendChild(btn);
    });

    // ── Gramática section ────────────────────────────────
    const sepGram = document.createElement('div');
    sepGram.className = 'quiz-secao-titulo';
    sepGram.textContent = I18n.t('quiz_gram_titulo');
    seletor.appendChild(sepGram);

    const gramData = App.estado.grammarData || { moduli: [] };
    if (gramData.moduli.length === 0) {
      const msg = document.createElement('p');
      msg.style.cssText = 'text-align:center;color:#aaa;font-style:italic;padding:0.5rem;font-size:0.85rem;';
      msg.textContent = I18n.t('quiz_gram_nao_carregado');
      seletor.appendChild(msg);
    } else {
      gramData.moduli.forEach(mod => {
        const btn = document.createElement('button');
        btn.className = 'quiz-templo-btn quiz-gram-btn';
        btn.innerHTML = I18n.t('quiz_gram_nivel').replace('{n}', mod.livello);
        btn.onclick = () => this.iniciarGramatica(mod.livello);
        seletor.appendChild(btn);
      });
    }

    // ── Conjugação section ────────────────────────────────
    const sepVerbi = document.createElement('div');
    sepVerbi.className = 'quiz-secao-titulo';
    sepVerbi.textContent = I18n.t('quiz_verbi_titulo');
    seletor.appendChild(sepVerbi);

    const verbosDisponiveis = (App.estado.conjugacoesData || []);
    if (verbosDisponiveis.length === 0) {
      const msg = document.createElement('p');
      msg.style.cssText = 'text-align:center;color:#aaa;font-style:italic;padding:0.5rem;font-size:0.85rem;';
      msg.textContent = I18n.t('quiz_verbi_nao_carregado');
      seletor.appendChild(msg);
    } else {
      const tempos = ['Presente', 'Imperfetto', 'Futuro'];
      tempos.forEach(tempo => {
        const btn = document.createElement('button');
        btn.className = 'quiz-templo-btn quiz-verbi-btn';
        const emoji = tempo === 'Presente' ? '⏱️' : tempo === 'Imperfetto' ? '⏪' : '⏩';
        btn.innerHTML = `${emoji} ${tempo}`;
        btn.onclick = () => this.iniciarConjugacao(tempo);
        seletor.appendChild(btn);
      });
    }
  },

  // ── Morphology quiz (gênero & plural) ────────────────────
  iniciarMorfologia(temploNum) {
    if (!Progressao.temploDesbloqueado(temploNum)) {
      App.notificar('notif_quiz_bloqueado', 'erro');
      return;
    }
    this.temploAtual   = temploNum;
    this.perguntaAtual = 0;
    this.pontuacao     = 0;
    this.xpTotal       = 0;
    this.respondido    = false;
    this.combo         = 0;

    this.perguntas = this._embaralhar(this._gerarMorfologia(temploNum)).slice(0, 10);
    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_morf_insuf', 'alerta');
      return;
    }
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    const seletor   = document.getElementById('quiz-templo-selector');
    if (container) container.style.display = 'block';
    if (resultado) resultado.style.display = 'none';
    if (seletor)   seletor.style.display   = 'none';
    this.mostrarPergunta();
  },

  _gerarMorfologia(temploNum) {
    const data = App.estado.templosData[temploNum];
    if (!data || !data.palavras || data.palavras.length < 2) return [];
    const palavras = data.palavras;
    const perguntas = [];

    // Gender questions
    const comGenero = palavras.filter(p => p.genero === 'm' || p.genero === 'f');
    comGenero.forEach(p => {
      const corretoPT = p.genero === 'm' ? 'masculino' : 'feminino';
      const corretoIT = p.genero === 'm' ? I18n.t('quiz_morf_genero_masc') : I18n.t('quiz_morf_genero_fem');
      perguntas.push({
        id: `morf_g_${p.id}`, templo: temploNum, tipo: 'morfologia',
        nivel: data.nivel || 'A1',
        pergunta: I18n.t('quiz_morf_genero_pergunta').replace('{w}', p.italiano),
        resposta_correta: corretoIT,
        alternativas: [I18n.t('quiz_morf_genero_masc'), I18n.t('quiz_morf_genero_fem')],
        explicacao: I18n.t('quiz_morf_genero_exp').replace('{w}', p.italiano).replace('{g}', corretoIT) + (p.plural ? ` (${I18n.idioma === 'it' ? 'plurale' : 'plural'}: ${p.plural})` : '') + '.',
        xp_recompensa: 20
      });
    });

    // Plural questions — need at least 4 words with plural for wrong options
    const comPlural = palavras.filter(p => p.plural && p.plural !== p.italiano);
    const todoPlurais = comPlural.map(p => p.plural);
    if (todoPlurais.length >= 4) {
      comPlural.forEach(p => {
        const erradas = this._embaralhar(todoPlurais.filter(pl => pl !== p.plural)).slice(0, 3);
        perguntas.push({
          id: `morf_p_${p.id}`, templo: temploNum, tipo: 'morfologia',
          nivel: data.nivel || 'A1',
          pergunta: I18n.t('quiz_morf_plural_pergunta').replace('{w}', p.italiano),
          resposta_correta: p.plural,
          alternativas: this._embaralhar([p.plural, ...erradas]),
          explicacao: I18n.t('quiz_morf_plural_exp').replace('{w}', p.italiano).replace('{p}', p.plural),
          xp_recompensa: 20
        });
      });
    }

    return perguntas;
  },

  // ── Conjugação quiz ───────────────────────────────────────
  iniciarConjugacao(tempo) {
    this.temploAtual   = 0; // special: 0 = conjugação
    this.perguntaAtual = 0;
    this.pontuacao     = 0;
    this.xpTotal       = 0;
    this.respondido    = false;
    this.combo         = 0;

    this.perguntas = this._embaralhar(this._gerarConjugacao(tempo)).slice(0, 10);
    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_conj_insuf', 'alerta');
      return;
    }
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    const seletor   = document.getElementById('quiz-templo-selector');
    if (container) container.style.display = 'block';
    if (resultado) resultado.style.display = 'none';
    if (seletor)   seletor.style.display   = 'none';
    this.mostrarPergunta();
  },

  _gerarConjugacao(tempo) {
    const verbos = App.estado.conjugacoesData || [];
    const perguntas = [];
    const pronomes = ['io','tu','lui/lei','noi','voi','loro'];

    // Collect all forms for this tense (for distractors)
    const todasFormas = [];
    verbos.forEach(v => {
      const t = v.tempos && v.tempos[tempo];
      if (t) pronomes.forEach(pr => { if (t[pr]) todasFormas.push(t[pr]); });
    });

    verbos.forEach(v => {
      const t = v.tempos && v.tempos[tempo];
      if (!t) return;

      pronomes.forEach(pr => {
        const correta = t[pr];
        if (!correta) return;

        // Use other forms of THIS verb as primary distractors, fill from all verbs
        const erradasVerbo = pronomes
          .filter(p => p !== pr && t[p] && t[p] !== correta)
          .map(p => t[p]);
        const erradasGlobal = todasFormas.filter(f => f !== correta);
        const pool = this._embaralhar([...new Set([...erradasVerbo, ...erradasGlobal])]);
        const erradas = pool.slice(0, 3);
        if (erradas.length < 3) return; // skip if not enough distractors

        const pronomeLabel = pr === 'lui/lei' ? 'lui / lei' : pr;
        perguntas.push({
          id: `conj_${v.infinitivo}_${tempo}_${pr}`,
          templo: 0,
          tipo: 'conjugação',
          nivel: 'A1',
          pergunta: `"${v.infinitivo}" (${v.traducao}) — ${pronomeLabel} — ${tempo}`,
          resposta_correta: correta,
          alternativas: this._embaralhar([correta, ...erradas]),
          explicacao: `${pronomeLabel} ${v.infinitivo} (${tempo}): "${correta}"`,
          xp_recompensa: 20
        });
      });
    });

    return perguntas;
  },

  // ── Listening Quiz ───────────────────────────────────────
  iniciarListening(temploNum) {
    if (!Progressao.temploDesbloqueado(temploNum)) return;
    this.temploAtual = temploNum;
    this.perguntaAtual = 0;
    this.pontuacao = 0;
    this.xpTotal = 0;
    this.respondido = false;
    this.combo = 0;

    this.perguntas = this._embaralhar(this._gerarListening(temploNum)).slice(0, 10);
    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_listen_insuf', 'alerta');
      return;
    }
    
    document.getElementById('quiz-container').style.display = 'block';
    document.getElementById('quiz-resultado').style.display = 'none';
    document.getElementById('quiz-templo-selector').style.display = 'none';
    this.mostrarPergunta();
  },

  _gerarListening(temploNum) {
    const data = App.estado.templosData[temploNum];
    if (!data || !data.palavras || data.palavras.length < 4) return [];
    
    const palavras = data.palavras;
    const perguntas = [];

    palavras.forEach(p => {
      const outras = palavras.filter(o => o.id !== p.id);
      const erradas = this._embaralhar(outras).slice(0, 3).map(o => o.italiano);
      const alternativas = this._embaralhar([p.italiano, ...erradas]);

      perguntas.push({
        id: `list_${p.id}`, templo: temploNum, tipo: 'listening',
        nivel: data.nivel || 'A1',
        italiano: p.italiano,
        pergunta: `Qual foi a palavra dita? (${p.portugues})`,
        resposta_correta: p.italiano,
        alternativas: alternativas,
        explicacao: `A palavra dita foi "${p.italiano}".`,
        xp_recompensa: 25
      });
    });
    return perguntas;
  },

  // ── Gramática Quiz ───────────────────────────────────────
  iniciarGramatica(livello) {
    this.temploAtual = 'gramatica_' + livello;
    this.perguntaAtual = 0;
    this.pontuacao = 0;
    this.xpTotal = 0;
    this.respondido = false;
    this.combo = 0;

    this.perguntas = this._embaralhar(this._gerarGramatica(livello)).slice(0, 10);
    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_gram_insuf', 'alerta');
      return;
    }
    
    document.getElementById('quiz-container').style.display = 'block';
    document.getElementById('quiz-resultado').style.display = 'none';
    document.getElementById('quiz-templo-selector').style.display = 'none';
    this.mostrarPergunta();
  },

  _gerarGramatica(livello) {
    const data = App.estado.grammarData || { moduli: [] };
    const modulo = data.moduli.find(m => m.livello === livello);
    if (!modulo || !modulo.lezioni) return [];

    const perguntas = [];
    
    modulo.lezioni.forEach(lez => {
      (lez.esempi || []).forEach(ex => {
        if (!ex.it || !ex.pt) return;
        
        const palavras = ex.it.split(' ').map(w => w.replace(/[.,?!]/g, ''));
        const candidatas = palavras.filter(w => w.length > 2);
        if (candidatas.length === 0) return;
        
        const oculta = candidatas[Math.floor(Math.random() * candidatas.length)];
        const regex = new RegExp(`\\b${oculta}\\b`, 'i');
        const perguntaTexto = ex.it.replace(regex, '___');
        
        const poolErradas = ["di", "a", "da", "in", "con", "su", "per", "tra", "fra", "il", "lo", "la", "i", "gli", "le", "un", "una", "e", "sono", "ho", "hai", "ha", "abbiamo", "avete", "hanno"].filter(w => w !== oculta.toLowerCase());
        const erradas = this._embaralhar(poolErradas).slice(0, 3);
        
        perguntas.push({
          id: `gram_${Math.random().toString(36).substr(2, 9)}`,
          tipo: 'gramática',
          nivel: livello,
          pergunta: `${perguntaTexto} (${ex.pt})`,
          resposta_correta: oculta.toLowerCase(),
          alternativas: this._embaralhar([oculta.toLowerCase(), ...erradas]),
          explicacao: `A frase completa é: "${ex.it}"`,
          xp_recompensa: 30
        });
      });
    });
    return perguntas;
  },

  // ── Update combo badge display ────────────────────────────
  _atualizarCombo() {
    const badge = document.getElementById('quiz-combo-badge');
    if (!badge) return;
    if (this.combo >= 3) {
      badge.textContent = `🔥 ×${this.combo} combo`;
      badge.style.display = 'inline-block';
    } else {
      badge.style.display = 'none';
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

document.addEventListener('i18n:changed', () => {
  const seletor   = document.getElementById('quiz-templo-selector');
  const resultado = document.getElementById('quiz-resultado');
  const pergunta  = document.getElementById('quiz-pergunta');
  if (!seletor && !resultado && !pergunta) return;

  if (resultado && resultado.style.display !== 'none') {
    Quiz.mostrarResultado();
  } else if (document.getElementById('quiz-container')?.style.display !== 'none') {
    Quiz.mostrarPergunta(Quiz.indiceAtual);
  } else {
    Quiz.renderizarSeletor();
  }
});
