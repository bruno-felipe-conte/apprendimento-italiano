// ============================================================
// quiz.js — Quiz system with multiple choice questions
// ============================================================

const Quiz = {
  _bloqueioAvanco: false,
  _resultadoMostrado: false,
  modoDireto: false,            // true = Digitação Direta ("Sem Rede"), false = Múltipla Escolha
  _submetendoDigitacao: false,  // Debounce guard para Enter / Clique
  temploAtual: null,
  perguntas: [],       // 10 questions for this session
  perguntaAtual: 0,
  pontuacao: 0,
  xpTotal: 0,
  respondido: false,
  combo: 0,
  abaSeletor: 'templos', // 'templos' | 'morfologia' | 'listening' | 'gramatica' | 'verbi'

  // ── Smart Retractable Quiz Bar ─────────────────────────────
  inicializarModoDireto() {
    try {
      this.modoDireto = localStorage.getItem('it_quiz_modo_direto') === 'true';
    } catch (_) {
      this.modoDireto = false;
    }
  },

  alternarModo(novoModo) {
    if (typeof novoModo === 'boolean') {
      this.modoDireto = novoModo;
    } else {
      this.modoDireto = !this.modoDireto;
    }
    try {
      localStorage.setItem('it_quiz_modo_direto', this.modoDireto ? 'true' : 'false');
    } catch (_) {}

    this._atualizarBotaoModo();
    this._aplicarModoVisual();
  },

  _atualizarBotaoModo() {
    const btn = document.getElementById('btn-toggle-modo-quiz');
    if (!btn) return;
    btn.setAttribute('aria-pressed', this.modoDireto ? 'true' : 'false');
    btn.classList.toggle('ativo', this.modoDireto);
    const txt = btn.querySelector('.modo-quiz-txt');
    if (txt) {
      txt.textContent = this.modoDireto ? 'Modo Sem Rede (Ativo)' : 'Modo Sem Rede';
    }
  },

  _aplicarModoVisual() {
    const grid = document.getElementById('opcoes-grid');
    let directTyping = document.getElementById('quiz-direct-typing');
    const input = document.getElementById('quiz-input-resposta');

    if (!directTyping && this.modoDireto) {
      this._injetarDirectTypingDOM();
      directTyping = document.getElementById('quiz-direct-typing');
    }

    if (this.modoDireto) {
      if (grid) grid.style.display = 'none';
      if (directTyping) directTyping.style.display = 'flex';
      this._vincularEventosDirectTyping();
      if (input && !this.respondido) {
        input.disabled = false;
        setTimeout(() => input.focus(), 60);
      }
    } else {
      if (grid) grid.style.display = 'grid';
      if (directTyping) directTyping.style.display = 'none';
    }
  },

  _injetarDirectTypingDOM() {
    let directTyping = document.getElementById('quiz-direct-typing');
    const container = document.getElementById('quiz-container');
    if (directTyping || !container) return;

    directTyping = document.createElement('div');
    directTyping.id = 'quiz-direct-typing';
    directTyping.className = 'quiz-direct-typing';
    directTyping.innerHTML = `
      <div class="quiz-input-wrapper">
        <label for="quiz-input-resposta" class="sr-only">Digite em italiano</label>
        <input type="text" id="quiz-input-resposta" class="quiz-input-resposta" placeholder="Digite em italiano..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" aria-describedby="quiz-feedback" />
      </div>
      <div id="quiz-accent-toolbar" class="quiz-accent-toolbar" role="toolbar" aria-label="Acentos italianos">
        <button type="button" class="btn-accent" data-char="à" aria-label="Inserir à">à</button>
        <button type="button" class="btn-accent" data-char="è" aria-label="Inserir è">è</button>
        <button type="button" class="btn-accent" data-char="é" aria-label="Inserir é">é</button>
        <button type="button" class="btn-accent" data-char="ì" aria-label="Inserir ì">ì</button>
        <button type="button" class="btn-accent" data-char="ò" aria-label="Inserir ò">ò</button>
        <button type="button" class="btn-accent" data-char="ù" aria-label="Inserir ù">ù</button>
      </div>
      <button type="button" id="btn-quiz-enviar" class="btn-primario btn-quiz-enviar" onclick="Quiz.verificarDigitacao()">Verificar (Enter)</button>
    `;

    const feedback = document.getElementById('quiz-feedback');
    if (feedback) {
      container.insertBefore(directTyping, feedback);
    } else {
      const expContainer = document.getElementById('explicacao-container');
      container.insertBefore(directTyping, expContainer || null);
    }

    this._vincularEventosDirectTyping();
  },

  _vincularEventosDirectTyping() {
    const input = document.getElementById('quiz-input-resposta');
    const toolbar = document.getElementById('quiz-accent-toolbar');
    const btnEnviar = document.getElementById('btn-quiz-enviar');

    if (toolbar && !toolbar._bound) {
      toolbar._bound = true;
      toolbar.querySelectorAll('.btn-accent').forEach(btn => {
        btn.addEventListener('mousedown', (e) => e.preventDefault());
        btn.onclick = (e) => {
          e.preventDefault();
          const char = btn.getAttribute('data-char') || btn.textContent.trim();
          this.inserirAcento(char);
        };
      });
    }

    if (input && !input._bound) {
      input._bound = true;
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          e.preventDefault();
          e.stopPropagation();
          if (!this.respondido) {
            this.verificarDigitacao();
          } else {
            this.proximaPergunta();
          }
        }
      });
    }

    if (btnEnviar && !btnEnviar._bound) {
      btnEnviar._bound = true;
      btnEnviar.onclick = (e) => {
        e.preventDefault();
        if (!this.respondido) {
          this.verificarDigitacao();
        } else {
          this.proximaPergunta();
        }
      };
    }
  },

  inserirAcento(char) {
    const input = document.getElementById('quiz-input-resposta');
    if (!input) return;

    const start = input.selectionStart ?? input.value.length;
    const end = input.selectionEnd ?? input.value.length;
    const val = input.value;

    input.value = val.substring(0, start) + char + val.substring(end);
    const newPos = start + char.length;
    input.selectionStart = newPos;
    input.selectionEnd = newPos;

    // Preserva o foco no input sem dispensar o teclado virtual
    input.focus();
  },

  verificarDigitacao() {
    if (this.respondido) return;

    // Debounce guard contra acionamentos múltiplos rápidos (F7-2.8)
    if (this._submetendoDigitacao) return;
    this._submetendoDigitacao = true;
    setTimeout(() => { this._submetendoDigitacao = false; }, 250);

    const input = document.getElementById('quiz-input-resposta');
    const feedback = document.getElementById('quiz-feedback');
    if (!input) return;

    const valorDigitado = input.value.trim();

    // Rejeita input vazio ou em branco sem penalizar (F7-2.7 & F6-2.1)
    if (!valorDigitado) {
      input.classList.add('shake');
      setTimeout(() => input.classList.remove('shake'), 400);
      if (feedback) {
        feedback.className = 'quiz-feedback alerta';
        feedback.setAttribute('role', 'status');
        feedback.textContent = 'Digite sua resposta antes de verificar.';
      }
      return;
    }

    const p = this.perguntas[this.perguntaAtual];
    if (!p) return;

    this.respondido = true;
    this._bloqueioAvanco = false;
    input.disabled = true;

    // Resolve ProductionValidator de forma defensiva
    const validator = (typeof ProductionValidator !== 'undefined' ? ProductionValidator : null) ||
                      (typeof globalThis !== 'undefined' && globalThis.ProductionValidator) ||
                      (typeof window !== 'undefined' && window.ProductionValidator);

    const esperado = p.resposta_correta || p.italiano || '';
    const variantes = (p.variantes || []).slice();
    if (p.italiano && p.italiano !== esperado && !variantes.includes(p.italiano)) {
      variantes.push(p.italiano);
    }

    let check;
    if (validator && typeof validator.validate === 'function') {
      check = validator.validate(valorDigitado, esperado, variantes);
    } else {
      const normInput = valorDigitado.toLowerCase().replace(/['’]/g, "'");
      const normExp = esperado.toLowerCase().replace(/['’]/g, "'");
      const correto = normInput === normExp;
      check = {
        isCorrect: correto,
        isFuzzy: false,
        distance: correto ? 0 : 1,
        diagnostic: correto ? null : `Resposta correta: ${esperado}`
      };
    }

    const btnEnviar = document.getElementById('btn-quiz-enviar');
    if (btnEnviar) {
      btnEnviar.textContent = 'Continuar (Enter) →';
    }

    if (check.isCorrect) {
      this.pontuacao++;
      this.combo++;
      const mult = this.combo >= 5 ? 3 : this.combo >= 3 ? 2 : 1;
      const xpBase = p.xp_recompensa || 20;
      this.xpTotal += xpBase * mult;

      if (typeof SomFeedback !== 'undefined') SomFeedback.correto();

      if (feedback) {
        feedback.setAttribute('role', 'status');
        feedback.className = 'quiz-feedback correto';
        if (check.isFuzzy) {
          feedback.innerHTML = `<span class="acerto-icon">🎉</span> Bravissimo! Resposta correta 🎉<br><small class="quiz-fuzzy-aviso">Atenção à grafia: esperado "<strong>${esperado}</strong>", você digitou "${valorDigitado}".</small>`;
        } else {
          feedback.textContent = 'Bravissimo! Resposta correta 🎉';
        }
      }
    } else {
      this.combo = 0;
      if (typeof SomFeedback !== 'undefined') SomFeedback.errado();

      if (feedback) {
        feedback.setAttribute('role', 'status');
        feedback.className = 'quiz-feedback incorreto';
        let diagHtml = '';
        if (check.diagnostic) {
          diagHtml = `<div class="quiz-diag-detalhe">${check.diagnostic}</div>`;
        }
        feedback.innerHTML = `<span class="erro-icon">❌</span> Errado. Resposta correta: <strong>${esperado}</strong>.${diagHtml}`;
      }
    }

    this._atualizarCombo();

    const explicacaoContainer = document.getElementById('explicacao-container');
    const explicacaoEl = document.getElementById('quiz-explicacao');
    if (explicacaoContainer) {
      explicacaoContainer.style.display = 'block';
      explicacaoContainer.setAttribute('role', 'status');
      explicacaoContainer.setAttribute('aria-live', 'polite');
    }
    if (explicacaoEl) {
      explicacaoEl.textContent = p.explicacao || '';
    }

    const btnContinuar = explicacaoContainer?.querySelector('button');
    if (btnContinuar) {
      setTimeout(() => btnContinuar.focus(), 80);
    }
  },

  // ── Smart Retractable Quiz Bar ─────────────────────────────
  toggleSeletor() {
    const seletor = document.getElementById('quiz-templo-selector');
    if (!seletor) return;
    const visivel = seletor.style.display !== 'none';
    if (visivel) {
      seletor.style.display = 'none';
    } else {
      this.renderizarSeletor();
      seletor.style.display = 'grid';
    }
    this._sincronizarBarraCompacta();
  },

  _sincronizarBarraCompacta() {
    const bar       = document.getElementById('quiz-compact-bar');
    const container = document.getElementById('quiz-container');
    const seletor   = document.getElementById('quiz-templo-selector');
    if (!bar) return;

    const quizAtivo = container && container.style.display !== 'none' && this.perguntas && this.perguntas.length > 0;
    if (!quizAtivo) {
      bar.style.display = 'none';
      return;
    }

    bar.style.display = 'flex';
    const elNome = document.getElementById('quiz-compact-nome');
    if (elNome) {
      let nomeQuiz = '🏛️ Quiz';
      if (this.temploAtual === 'misto') {
        nomeQuiz = '🌍 Quiz Generale';
      } else if (this.temploAtual === 0) {
        nomeQuiz = '⏱️ Conjugação';
      } else if (typeof this.temploAtual === 'string' && this.temploAtual.startsWith('gramatica_')) {
        const nivel = this.temploAtual.replace('gramatica_', '');
        nomeQuiz = nivel === 'misto' ? '🌍 Gramática Geral' : `📚 Gramática ${nivel}`;
      } else if (this.temploAtual) {
        const d = App.estado?.templosData?.[this.temploAtual];
        nomeQuiz = `🏛️ T${this.temploAtual} · ${d?.nome || 'Tempio ' + this.temploAtual}`;
      }
      elNome.textContent = nomeQuiz;
    }

    const elProg = document.getElementById('quiz-compact-progresso');
    if (elProg) {
      const total = this.perguntas.length || 10;
      const atual = Math.min(this.perguntaAtual + 1, total);
      elProg.textContent = `${atual}/${total}`;
    }

    const btn = bar.querySelector('.quiz-compact-toggle-btn');
    const seletorVisivel = seletor && seletor.style.display !== 'none';
    if (btn) {
      btn.innerHTML = seletorVisivel
        ? '<span>✕ Ocultar</span><span class="quiz-compact-chevron">▴</span>'
        : '<span>⚙️ Trocar Quiz</span><span class="quiz-compact-chevron">▾</span>';
    }
  },

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
    this._bloqueioAvanco = false;
    this._resultadoMostrado = false;

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
    this._sincronizarBarraCompacta();

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
    this._bloqueioAvanco = false;
    this._resultadoMostrado = false;

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

    this.inicializarModoDireto();

    const p = this.perguntas[this.perguntaAtual];
    this.respondido = false;
    this._resultadoMostrado = false;
    this._bloqueioAvanco = false;
    this._atualizarCombo();
    this._sincronizarBarraCompacta();

    // Reset feedback
    const feedback = document.getElementById('quiz-feedback');
    if (feedback) {
      feedback.className = 'quiz-feedback';
      feedback.textContent = '';
      feedback.innerHTML = '';
    }

    // Reset input se em modo direto
    const input = document.getElementById('quiz-input-resposta');
    if (input) {
      input.value = '';
      input.disabled = false;
    }
    const btnEnviar = document.getElementById('btn-quiz-enviar');
    if (btnEnviar) {
      btnEnviar.textContent = 'Verificar (Enter)';
    }

    this._atualizarBotaoModo();
    this._aplicarModoVisual();

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
    this._bloqueioAvanco = false;

    const p = this.perguntas[this.perguntaAtual];
    const correto = escolha === p.resposta_correta;

    // Mark all buttons and collapse non-relevant options (In-Place Transition)
    const grid = document.getElementById('opcoes-grid');
    if (grid) {
      grid.querySelectorAll('.opcao-btn').forEach(btn => {
        btn.disabled = true;
        const ehCorreta = btn.textContent === p.resposta_correta;
        const foiEscolhida = btn.textContent === escolha;

        if (ehCorreta) {
          btn.classList.add('correta');
        } else if (foiEscolhida && !correto) {
          btn.classList.add('errada');
        } else {
          // Opção irrelevante: recolhe para dar espaço in-place à explicação
          btn.classList.add('opcao-recolhida');
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
    if (explicacaoContainer) {
      explicacaoContainer.style.display = 'block';
      explicacaoContainer.setAttribute('role', 'status');
      explicacaoContainer.setAttribute('aria-live', 'polite');
      const btnContinuar = explicacaoContainer.querySelector('button');
      if (btnContinuar) {
        setTimeout(() => btnContinuar.focus?.(), 50);
      }
    }
    if (explicacaoEl) explicacaoEl.textContent = p.explicacao || (correto ? I18n.t('quiz_correto') : `${I18n.t('quiz_resposta_correta_era')} ${p.resposta_correta}`);
  },

  // ── Advance to next question ───────────────────────────────
  proximaPergunta() {
    if (this._bloqueioAvanco) return;
    this._bloqueioAvanco = true;

    // Immediately disable "Continuar" button to absorb double-clicks
    const btnContinuar = document.querySelector(
      '#explicacao-container .btn-primario, button[data-i18n="quiz_continuar"]'
    );
    if (btnContinuar) btnContinuar.disabled = true;

    try {
      this.perguntaAtual++;
      if (this.perguntaAtual >= this.perguntas.length) {
        this.mostrarResultado();
      } else {
        this._salvarSessao(); // persiste progresso parcial
        this.mostrarPergunta();
      }
    } finally {
      // Fallback debounce window (300ms) to re-enable button and clear lock
      setTimeout(() => {
        this._bloqueioAvanco = false;
        if (btnContinuar) btnContinuar.disabled = false;
      }, 300);
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
    this._bloqueioAvanco = true;

    this._limparSessao(); // sessão concluída — limpa
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    if (container) container.style.display = 'none';
    this._sincronizarBarraCompacta();

    if (!resultado) return;
    resultado.style.display = 'block';

    const total = this.perguntas.length;
    const pct = total > 0 ? Math.round((this.pontuacao / total) * 100) : 0;

    // Choose message based on score
    let msg = '';
    if (pct >= 90) msg = '🏆 Perfetto! Sei un maestro dell\'italiano!';
    else if (pct >= 70) msg = '👏 Molto bene! Continua così!';
    else if (pct >= 50) msg = '📚 Bene! Ma puoi fare di melhor!';
    else msg = '💪 Non mollare! Continua a studiare!';

    const scoreEl = document.getElementById('resultado-score');
    const xpEl = document.getElementById('resultado-xp');
    const msgEl = document.getElementById('resultado-msg');
    if (scoreEl) scoreEl.textContent = `${this.pontuacao}/${total}`;
    if (xpEl) xpEl.textContent = I18n.t('quiz_xp_ganhos').replace('{n}', this.xpTotal);
    if (msgEl) msgEl.textContent = msg;

    // Idempotency: if already processed rewards and history for this completion, return
    if (this._resultadoMostrado) return;
    this._resultadoMostrado = true;

    // Log quiz completion to heatmap diary (count actual questions answered)
    if (typeof Calor !== 'undefined') Calor.registrar(this.perguntas.length || 1);

    // Give XP and atomically reset to prevent duplicate awards
    const xpParaConceder = this.xpTotal;
    this.xpTotal = 0;
    if (xpParaConceder > 0) {
      Progressao.ganhar(xpParaConceder);
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
        xp_ganho: xpParaConceder,
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
    this._sincronizarBarraCompacta();
    this.renderizarSeletor();
  },

  // ── Render the temple selector buttons ────────────────────
  renderizarSeletor() {
    const seletor = document.getElementById('quiz-templo-selector');
    if (!seletor) return;
    seletor.innerHTML = '';
    seletor.style.display = 'grid';

    // Barra de categorias (Tabs inteligentes)
    const tabs = [
      { id: 'templos', label: '🏛️ Templos' },
      { id: 'morfologia', label: '🔤 Morfologia' },
      { id: 'listening', label: '🎧 Listening' },
      { id: 'gramatica', label: '📚 Gramática' },
      { id: 'verbi', label: '⏱️ Conjugação' }
    ];

    const tabNav = document.createElement('div');
    tabNav.className = 'quiz-tabs-nav';
    tabNav.style.cssText = 'grid-column: 1 / -1; display: flex; gap: 0.35rem; overflow-x: auto; padding-bottom: 0.5rem; margin-bottom: 0.5rem; -webkit-overflow-scrolling: touch; scrollbar-width: none;';
    
    tabs.forEach(t => {
      const btn = document.createElement('button');
      btn.type = 'button';
      const ativa = this.abaSeletor === t.id;
      btn.style.cssText = `padding: 0.35rem 0.75rem; border-radius: 999px; border: 1.5px solid ${ativa ? 'var(--cor-veneziano,#9B2335)' : 'var(--cor-marmore-escuro,#D4C4B5)'}; background: ${ativa ? 'var(--cor-veneziano,#9B2335)' : 'transparent'}; color: ${ativa ? '#fff' : 'inherit'}; font-size: 0.8rem; font-weight: 600; white-space: nowrap; cursor: pointer; transition: all 0.2s;`;
      btn.textContent = t.label;
      btn.onclick = () => {
        this.abaSeletor = t.id;
        this.renderizarSeletor();
      };
      tabNav.appendChild(btn);
    });
    seletor.appendChild(tabNav);

    // Usa a lista de templos carregados (1-50), ordenados
    const todosTemplos = Object.keys(App.estado.templosData)
      .map(Number).sort((a, b) => a - b);

    // Calcular histórico por templo para estatísticas de acerto
    let historico = [];
    try { historico = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]'); } catch (_) {}

    const temploStats = {};
    historico.forEach(h => {
      const key = String(h.templo);
      if (!temploStats[key]) temploStats[key] = { total: 0, acertos: 0, totalPerguntas: 0, lastScore: 0 };
      temploStats[key].total++;
      temploStats[key].acertos += h.acertos || 0;
      temploStats[key].totalPerguntas += h.total || 10;
      temploStats[key].lastScore = h.pontuacao || 0;
    });

    // ── Aba Templos ───────────────────────────────────────
    if (this.abaSeletor === 'templos') {
      if (Progressao.temploDesbloqueado(1)) {
        const btnMisto = document.createElement('button');
        btnMisto.className = 'quiz-templo-btn';
        btnMisto.innerHTML = '🌍 Quiz Generale<br><small>Tutti i templi misti</small>';
        btnMisto.style.gridColumn = '1 / -1';
        btnMisto.style.background = 'linear-gradient(135deg, #2C3E50, #3498DB)';
        btnMisto.style.color = 'white';
        btnMisto.onclick = () => this.iniciarMisto();
        seletor.appendChild(btnMisto);
      }

      todosTemplos.forEach(i => {
        const desbloqueado = Progressao.temploDesbloqueado(i);
        const data = App.estado.templosData[i];
        const nome = (data && data.nome) || `Tempio ${i}`;
        const nivel = data ? data.nivel : '—';
        const stats = temploStats[String(i)];

        const btn = document.createElement('button');
        btn.className = `quiz-templo-btn${desbloqueado ? '' : ' bloqueado'}`;

        let statusHtml = '';
        if (desbloqueado && stats) {
          const avgPct = stats.totalPerguntas > 0 ? Math.round((stats.acertos / stats.totalPerguntas) * 100) : 0;
          const stars = avgPct >= 90 ? '⭐⭐⭐' : avgPct >= 70 ? '⭐⭐' : avgPct >= 50 ? '⭐' : '☆';
          statusHtml = `<div style="font-size:0.7rem;color:#27AE60;margin-top:0.2rem">${stars} ${avgPct}% avg</div>`;
        }

        btn.innerHTML = desbloqueado
          ? `🏛️ ${i}. ${nome}<br><small>${nivel}</small>${statusHtml}`
          : `🔒 ${i}. ${nome}<br><small>Livello ${Progressao.TEMPLO_NIVEL[i] || i}</small>`;

        if (desbloqueado) btn.onclick = () => this.iniciar(i);
        else btn.disabled = true;
        seletor.appendChild(btn);
      });
      return;
    }

    // ── Aba Morfologia ────────────────────────────────────
    if (this.abaSeletor === 'morfologia') {
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
      return;
    }

    // ── Aba Listening ─────────────────────────────────────
    if (this.abaSeletor === 'listening') {
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
      return;
    }

    // ── Aba Gramática ─────────────────────────────────────
    if (this.abaSeletor === 'gramatica') {
      const gramData = this._obterDadosGramatica();
      if (!gramData || !Array.isArray(gramData.moduli) || gramData.moduli.length === 0) {
        fetch('data/grammar.json')
          .then(r => r.ok ? r.json() : { moduli: [] })
          .then(fresh => {
            if (fresh && Array.isArray(fresh.moduli) && fresh.moduli.length > 0) {
              if (App.estado) App.estado.grammarData = fresh;
              if (typeof Grammar !== 'undefined' && !Grammar.dados) Grammar.dados = fresh;
              try { localStorage.setItem('it_swr_grammar', JSON.stringify(fresh)); } catch (_) {}
              this.renderizarSeletor();
            }
          })
          .catch(() => {});

        const msg = document.createElement('p');
        msg.style.cssText = 'grid-column: 1 / -1; text-align:center;color:var(--cor-inchiostro-claro,#5A4535);font-weight:500;font-style:italic;padding:0.5rem;font-size:0.85rem;';
        msg.textContent = I18n.t('quiz_gram_nao_carregado') || 'Carregando exercícios de gramática...';
        seletor.appendChild(msg);
        return;
      }

      // Botão Misto Geral (Misto A1-C2)
      const totalGeral = this._contarExerciciosGramatica();
      const btnMisto = document.createElement('button');
      btnMisto.className = 'quiz-templo-btn';
      btnMisto.innerHTML = `🌍 Quiz Grammatica Generale<br><small>Tutti i livelli misti (${totalGeral} quizzes)</small>`;
      btnMisto.style.gridColumn = '1 / -1';
      btnMisto.style.background = 'linear-gradient(135deg, #1B4D3E, #27AE60)';
      btnMisto.style.color = 'white';
      btnMisto.onclick = () => this.iniciarGramatica('misto');
      seletor.appendChild(btnMisto);

      gramData.moduli.forEach(mod => {
        const nivel = mod.id;
        const qtd = this._contarExerciciosGramatica(nivel);
        const btn = document.createElement('button');
        btn.className = 'quiz-templo-btn quiz-gram-btn';
        btn.innerHTML = `📚 ${mod.nome || ('Livello ' + nivel)}<br><small style="opacity:0.85">${qtd} quizzes disponíveis</small>`;
        btn.onclick = () => this.iniciarGramatica(nivel);
        seletor.appendChild(btn);
      });
      return;
    }

    // ── Aba Conjugação ────────────────────────────────────
    if (this.abaSeletor === 'verbi') {
      const verbosDisponiveis = (App.estado.conjugacoesData || []);
      if (verbosDisponiveis.length === 0) {
        const msg = document.createElement('p');
        msg.style.cssText = 'grid-column: 1 / -1; text-align:center;color:var(--cor-inchiostro-claro,#5A4535);font-weight:500;font-style:italic;padding:0.5rem;font-size:0.85rem;';
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
      return;
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
    this._bloqueioAvanco = false;
    this._resultadoMostrado = false;

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
    this._bloqueioAvanco = false;
    this._resultadoMostrado = false;

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
    this._bloqueioAvanco = false;
    this._resultadoMostrado = false;

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
    this._bloqueioAvanco = false;
    this._resultadoMostrado = false;

    const pool = this._gerarGramatica(livello);
    this.perguntas = this._embaralhar(pool).slice(0, 10);
    if (this.perguntas.length === 0) {
      App.notificar('notif_quiz_gram_insuf', 'alerta');
      return;
    }
    
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    const seletor = document.getElementById('quiz-templo-selector');
    if (container) container.style.display = 'block';
    if (resultado) resultado.style.display = 'none';
    if (seletor) seletor.style.display = 'none';
    this._sincronizarBarraCompacta();

    this.mostrarPergunta();
  },

  _obterDadosGramatica() {
    if (App.estado && App.estado.grammarData && Array.isArray(App.estado.grammarData.moduli) && App.estado.grammarData.moduli.length > 0) {
      return App.estado.grammarData;
    }
    if (typeof Grammar !== 'undefined' && Grammar.dados && Array.isArray(Grammar.dados.moduli) && Grammar.dados.moduli.length > 0) {
      App.estado.grammarData = Grammar.dados;
      return Grammar.dados;
    }
    try {
      const cached = localStorage.getItem('it_swr_grammar');
      if (cached) {
        const parsed = JSON.parse(cached);
        if (parsed && Array.isArray(parsed.moduli) && parsed.moduli.length > 0) {
          App.estado.grammarData = parsed;
          return parsed;
        }
      }
    } catch (_) {}
    return null;
  },

  _contarExerciciosGramatica(nivel = null) {
    const data = this._obterDadosGramatica();
    if (!data || !Array.isArray(data.moduli)) return 0;
    let count = 0;
    data.moduli.forEach(mod => {
      if (nivel && nivel !== 'misto' && mod.id !== nivel) return;
      (mod.lezioni || []).forEach(lez => {
        (lez.exercicios || []).forEach(ex => {
          if (ex.tipo === 'escolha' && Array.isArray(ex.opcoes) && ex.resposta !== undefined && ex.opcoes[ex.resposta]) {
            count++;
          }
        });
      });
    });
    return count;
  },

  _gerarGramatica(livello) {
    const data = this._obterDadosGramatica();
    if (!data || !Array.isArray(data.moduli)) return [];

    const perguntas = [];
    data.moduli.forEach(mod => {
      if (livello && livello !== 'misto' && mod.id !== livello) return;

      (mod.lezioni || []).forEach((lez, lIdx) => {
        (lez.exercicios || []).forEach((ex, eIdx) => {
          if (ex.tipo === 'escolha' && Array.isArray(ex.opcoes) && ex.resposta !== undefined && ex.opcoes[ex.resposta]) {
            const respostaCorreta = ex.opcoes[ex.resposta];
            perguntas.push({
              id: `gram_${mod.id}_${lIdx}_${eIdx}`,
              templo: `gramatica_${mod.id}`,
              tipo: 'gramática',
              nivel: mod.id,
              pergunta: ex.pergunta,
              resposta_correta: respostaCorreta,
              alternativas: [...ex.opcoes],
              explicacao: ex.explicacao || `A resposta correta é: "${respostaCorreta}"`,
              xp_recompensa: 25
            });
          }
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


// Atalhos de teclado para o Quiz (1-4 para responder, Espaço/Enter para avançar) (F14)
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', (e) => {
    if (e.defaultPrevented) return;
    const tag = (e.target?.tagName || '').toUpperCase();
    if (['INPUT', 'SELECT', 'TEXTAREA'].includes(tag) || e.target?.isContentEditable) return;

    const secaoAtiva = (typeof AppNavigation !== 'undefined' && AppNavigation.secaoAtiva) ||
                       (typeof AppState !== 'undefined' && AppState.estado?.secaoAtiva) ||
                       (typeof App !== 'undefined' && App.estado?.secaoAtiva) || '';
    const secQuiz = document.getElementById('sec-quiz');
    const isQuizAtivo = secaoAtiva === 'quiz' || (secQuiz && secQuiz.classList.contains('active'));
    if (!isQuizAtivo) return;

    // Don't hijack keys when modals or dialogs are active
    if (typeof ModalManager !== 'undefined' && (ModalManager.stack?.length > 0 || ModalManager.getOpenStaticModal?.())) {
      return;
    }
    const modais = document.querySelectorAll(
      '.modal.ativo, .modal.show, .templo-modal.ativo, .conquista-modal.ativo, .levelup-modal.ativo, .meta-settings-modal.ativo, .modal-manager-overlay, .tm-overlay:not([style*="display: none"]), dialog[open]'
    );
    for (const m of modais) {
      if (m.classList.contains('ativo') || m.classList.contains('show') || (m.tagName === 'DIALOG' && m.open)) return;
      if (m.style.display && m.style.display !== 'none') return;
    }

    if (!Quiz.perguntas || Quiz.perguntas.length === 0 || Quiz._resultadoMostrado) return;

    const explicacaoContainer = document.getElementById('explicacao-container');
    const isExplicacaoVisivel = (explicacaoContainer && explicacaoContainer.style.display !== 'none') || Quiz.respondido;

    if (isExplicacaoVisivel) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'Spacebar') {
        e.preventDefault();
        e.stopImmediatePropagation();
        Quiz.proximaPergunta();
      }
    } else {
      if (['1', '2', '3', '4'].includes(e.key)) {
        const idx = parseInt(e.key, 10) - 1;
        const opcoes = document.querySelectorAll('#opcoes-grid .opcao-btn, .opcoes-grid .opcao-btn');
        if (opcoes && opcoes[idx] && !opcoes[idx].disabled) {
          e.preventDefault();
          e.stopImmediatePropagation();
          opcoes[idx].click();
        }
      }
    }
  });
}

// Exposição global segura para navegadores e testes
if (typeof window !== 'undefined') window.Quiz = Quiz;
if (typeof globalThis !== 'undefined') globalThis.Quiz = Quiz;
if (typeof module !== 'undefined' && module.exports) module.exports = Quiz;
