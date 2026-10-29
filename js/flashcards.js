// ============================================================
// flashcards.js — FSRS-4.5 spaced repetition engine
// Free Spaced Repetition Scheduler (Anki 23.10+ algorithm)
// ============================================================

// ── FSRS-4.5 core algorithm ───────────────────────────────────
const FSRS = {
  // Default weights from FSRS-4.5 paper (trained on 20M reviews)
  w: [0.4072, 1.1829, 3.1262, 15.4722, 7.2102, 0.5316, 1.0651, 0.0589,
      1.9395, 0.11,   0.29,   2.9898,  0.51,   0.34,   1.3436, 0.0762, 2.9898],

  // Power forgetting curve: R(t) = (1 + FACTOR × t/S)^DECAY
  // DECAY=-0.5, FACTOR=19/81 → R=0.9 when t=S (stability in days)
  DECAY: -0.5,
  FACTOR: 19 / 81,
  TARGET_R: 0.9,

  // Current retrievability given elapsed time t (days) and stability S
  retrievability(t, s) {
    if (s <= 0 || t < 0) return 1;
    return Math.pow(1 + this.FACTOR * t / s, this.DECAY);
  },

  // Days until retrievability drops to TARGET_R
  nextInterval(s) {
    const t = s * (Math.pow(this.TARGET_R, 1 / this.DECAY) - 1) / this.FACTOR;
    return Math.max(Math.round(t), 1);
  },

  // Initial stability after first review (rating 1-4)
  initStability(rating) {
    return Math.max(this.w[rating - 1], 0.1);
  },

  // Initial difficulty after first review (rating 1-4)
  initDifficulty(rating) {
    const d = this.w[4] - Math.exp(this.w[5] * (rating - 1)) + 1;
    return Math.min(Math.max(d, 1), 10);
  },

  // Difficulty after subsequent reviews (with mean reversion toward Easy baseline)
  nextDifficulty(d, rating) {
    const d0easy = this.initDifficulty(4); // ~3.28 — Easy baseline
    const delta  = -this.w[6] * (rating - 3);
    const raw    = d + delta;
    // w[7]=0.0589 pulls ~6% toward the easy baseline each review
    const next   = this.w[7] * d0easy + (1 - this.w[7]) * raw;
    return Math.min(Math.max(next, 1), 10);
  },

  // Stability after a successful recall (rating 2/3/4)
  nextRecallStability(d, s, r, rating) {
    if (s <= 0) return this.initStability(rating); // guard: treat degenerate cards as new
    const hardPenalty = rating === 2 ? this.w[15] : 1;
    const easyBonus   = rating === 4 ? this.w[16] : 1;
    const increment   = Math.exp(this.w[8]) *
                        (11 - d) *
                        Math.pow(s, -this.w[9]) *
                        (Math.exp(this.w[10] * (1 - r)) - 1) *
                        hardPenalty * easyBonus;
    return s * (increment + 1);
  },

  // Stability after forgetting (rating 1 — Again)
  nextForgetStability(d, s, r) {
    return this.w[11] *
           Math.pow(d, -this.w[12]) *
           (Math.pow(s + 1, this.w[13]) - 1) *
           Math.exp(this.w[14] * (1 - r));
  },

  // ── Review a card, return updated card state ───────────────
  review(card, rating) {
    const now   = Date.now();
    const tDays = card.lastReview ? (now - card.lastReview) / 86400000 : 0;
    let { difficulty: d, stability: s, lapses, reps, state } = card;
    const r = (s > 0) ? this.retrievability(tDays, s) : 1;

    let newD, newS;

    if (state === 'new') {
      newD = this.initDifficulty(rating);
      newS = this.initStability(rating);
    } else if (rating === 1) {
      // Again — forgot
      lapses++;
      newD = this.nextDifficulty(d, rating);
      newS = Math.max(this.nextForgetStability(d, s, r), 0.1);
    } else {
      // Hard / Good / Easy — remembered
      newD = this.nextDifficulty(d, rating);
      newS = Math.max(this.nextRecallStability(d, s, r, rating), 0.1);
    }

    reps++;
    const newState    = rating === 1 ? 'learning' : 'review';
    const intervalDay = rating === 1 ? 1 : this.nextInterval(newS);

    return {
      ...card,
      state:          newState,
      difficulty:     newD,
      stability:      newS,
      retrievability: r,
      lapses,
      reps,
      lastReview:     now,
      interval:       intervalDay,
      nextReview:     now + intervalDay * 86400000,
    };
  },

  // ── Preview intervals for each rating without committing ───
  previewIntervals(card) {
    const now   = Date.now();
    const tDays = card.lastReview ? (now - card.lastReview) / 86400000 : 0;
    const { difficulty: d, stability: s, state } = card;
    const r = (s > 0) ? this.retrievability(tDays, s) : 1;

    return [1, 2, 3, 4].map(rating => {
      if (state === 'new') {
        return rating === 1 ? 1 : this.nextInterval(this.initStability(rating));
      }
      if (rating === 1) return 1;
      const newS = Math.max(this.nextRecallStability(d, s, r, rating), 0.1);
      return this.nextInterval(newS);
    });
  },

  // ── Migrate a legacy SM-2 record to FSRS schema ───────────
  migrateSM2(sm2) {
    // Estimate stability from SM-2 interval
    const s = Math.max(sm2.intervalo || 1, 0.1);
    // Estimate difficulty: ease=2.5 → D=5, ease=1.3 → D=9, ease=3.0 → D=3
    const ease = sm2.facilidade || 2.5;
    const d = Math.min(Math.max(10 - (ease - 1.3) * (9 / 1.7), 1), 10);
    return {
      state:          sm2.repeticoes > 0 ? 'review' : 'new',
      difficulty:     d,
      stability:      s,
      retrievability: 1,
      lapses:         0,
      reps:           sm2.repeticoes || 0,
      lastReview:     sm2.ultima_revisao || null,
      interval:       sm2.intervalo || 0,
      nextReview:     sm2.proxima_revisao || null,
    };
  },

  // Format interval as human-readable string
  formatInterval(days) {
    if (days <= 0) return 'hoje';
    if (days === 1) return '1 dia';
    if (days < 31) return `${days} dias`;
    const months = Math.round(days / 30);
    return months === 1 ? '1 mês' : `${months} meses`;
  },
};


// ── Flashcard UI module ────────────────────────────────────────
const Flashcards = {
  temploAtual:      null,
  cartasDisponiveis: [],
  cartaAtual:       null,
  indiceAtual:      0,
  virada:           false,
  praticandoTodas:  false,
  modoReverso:       false,
  modoEscrita:       false,
  modoContexto:      false,
  modoEscuta:        false,
  nivelDica:         0,      // 0=none, 1=first letter, 2=more letters, 3=flipped
  dicaUsada:         false,  // penalises Good/Easy when true
  sessaoStats:       null,
  gravando:          false,
  _recognition:      null,
  _swipeInitialized: false,
  _swipeStartX:      0,
  _swipeStartY:      0,
  abaOrigem:         'templos', // 'templos' | 'especiais'
  seletorRecolhido:  false,

  // ── Smart Retractable Selector Bar ─────────────────────────
  toggleSeletor(forcarEstado) {
    if (typeof forcarEstado === 'boolean') {
      this.seletorRecolhido = forcarEstado;
    } else {
      this.seletorRecolhido = !this.seletorRecolhido;
    }
    this._sincronizarBarraCompacta();
  },

  _sincronizarBarraCompacta() {
    const layout  = document.getElementById('fc-studio-layout');
    const sidebar = document.getElementById('fc-studio-sidebar') || document.querySelector('.fc-studio-sidebar');
    const bar     = document.getElementById('fc-compact-bar');
    if (!bar || !sidebar) return;

    const temSessaoAtiva = this.cartasDisponiveis && this.cartasDisponiveis.length > 0 && this.indiceAtual < this.cartasDisponiveis.length;

    if (!temSessaoAtiva) {
      bar.style.display = 'none';
      sidebar.classList.remove('recolhido');
      if (layout) layout.classList.remove('seletor-recolhido');
      return;
    }

    bar.style.display = 'flex';
    sidebar.classList.toggle('recolhido', !!this.seletorRecolhido);
    if (layout) layout.classList.toggle('seletor-recolhido', !!this.seletorRecolhido);

    // Label de origem (Templo ou Baralho Especial)
    const elOrigem = document.getElementById('fc-compact-origem');
    if (elOrigem) {
      let labelOrigem = '🌍 Revisão Geral';
      if (typeof this.temploAtual === 'string' && this.temploAtual.startsWith('deck_')) {
        const mapDecks = {
          deck_all: '⭐ Top 500',
          deck_colocacoes: '🧩 Chunks',
          deck_falsi_amici: '⚠️ Falsi Amici',
          deck_preposizioni: '📍 Preposições',
          deck_verbi_irregolari: '⚡ Verbos',
          deck_situazioni_reali: '🎭 Vida Real',
        };
        labelOrigem = mapDecks[this.temploAtual] || '⭐ Top 500';
      } else if (this.temploAtual === 'custom') {
        labelOrigem = '🤖 Minhas Palavras';
      } else if (this.temploAtual) {
        const tData = App.estado?.templosData?.[this.temploAtual];
        const tNome = tData?.nome || `Tempio ${this.temploAtual}`;
        labelOrigem = `🏛️ T${this.temploAtual} · ${tNome}`;
      }
      elOrigem.textContent = labelOrigem;
    }

    // Label de modo ativo
    const elModo = document.getElementById('fc-compact-modo');
    if (elModo) {
      let modoTxt = '🎴 Normal';
      if (this.modoReverso)  modoTxt = '🔄 Reverso';
      if (this.modoContexto) modoTxt = '📖 Contexto';
      if (this.modoEscuta)   modoTxt = '🎧 Escuta';
      if (this.modoEscrita)  modoTxt = '✍️ Scrittura';
      elModo.textContent = modoTxt;
    }

    // Contador 1/20
    const elCount = document.getElementById('fc-compact-count');
    if (elCount) {
      elCount.textContent = `${this.indiceAtual + 1}/${this.cartasDisponiveis.length}`;
    }

    // Botão Trocar
    const btnToggle = document.getElementById('fc-compact-toggle-btn');
    if (btnToggle) {
      btnToggle.innerHTML = this.seletorRecolhido
        ? '<span>⚙️ Trocar</span><span class="fc-compact-chevron">▾</span>'
        : '<span>✕ Ocultar</span><span class="fc-compact-chevron">▴</span>';
    }
  },

  // ── Switch between Templos and Baralhos Especiais ───────────
  trocarAbaOrigem(origem, autoLoad = true) {
    this.abaOrigem = origem;
    const tabTemplos = document.getElementById('fc-tab-templos');
    const tabEspeciais = document.getElementById('fc-tab-especiais');
    const painelTemplos = document.getElementById('fc-painel-templos');
    const painelEspeciais = document.getElementById('fc-painel-especiais');

    if (origem === 'especiais') {
      if (tabTemplos) {
        tabTemplos.classList.remove('ativo');
        tabTemplos.setAttribute('aria-selected', 'false');
      }
      if (tabEspeciais) {
        tabEspeciais.classList.add('ativo');
        tabEspeciais.setAttribute('aria-selected', 'true');
      }
      if (painelTemplos) painelTemplos.style.display = 'none';
      if (painelEspeciais) painelEspeciais.style.display = '';

      if (autoLoad) {
        const selDeck = document.getElementById('flashcard-deck-select');
        const deckVal = (selDeck && selDeck.value) ? selDeck.value : 'deck_all';
        this.selecionarDeckEspecial(deckVal);
      }
    } else {
      if (tabEspeciais) {
        tabEspeciais.classList.remove('ativo');
        tabEspeciais.setAttribute('aria-selected', 'false');
      }
      if (tabTemplos) {
        tabTemplos.classList.add('ativo');
        tabTemplos.setAttribute('aria-selected', 'true');
      }
      if (painelEspeciais) painelEspeciais.style.display = 'none';
      if (painelTemplos) painelTemplos.style.display = '';

      if (autoLoad) {
        const selTemplo = document.getElementById('flashcard-templo-select');
        let temploVal = selTemplo ? selTemplo.value : null;
        if (!temploVal || (typeof temploVal === 'string' && temploVal.startsWith('deck_'))) {
          const desbloqueados = App.estado?.progresso?.templos_desbloqueados || [1];
          temploVal = desbloqueados[0] || 1;
          if (selTemplo) selTemplo.value = String(temploVal);
        }
        this.selecionarTemplo(temploVal);
      }
    }
  },

  // ── Select a special deck (Top 500) ────────────────────────
  selecionarDeckEspecial(deckVal) {
    if (!deckVal) return;
    const selDeck = document.getElementById('flashcard-deck-select');
    if (selDeck && selDeck.value !== deckVal) {
      selDeck.value = deckVal;
    }
    const chips = document.querySelectorAll('.fc-deck-chip');
    chips.forEach(chip => {
      if (chip.getAttribute('data-deck') === deckVal) {
        chip.classList.add('ativo');
      } else {
        chip.classList.remove('ativo');
      }
    });

    if (this.abaOrigem !== 'especiais') {
      this.trocarAbaOrigem('especiais', false);
    }
    this.init(deckVal);
  },

  // ── Initialize for a specific temple or special deck ─────
  selecionarTemplo(val) {
    if (!val) return;
    if (typeof val === 'string' && val.startsWith('deck_')) {
      this.selecionarDeckEspecial(val);
    } else if (val === 'custom') {
      this.init(val);
    } else {
      this.init(parseInt(val, 10));
    }
  },

  async init(templo) {
    if (!templo) return;
    const ehCustom = templo === 'custom';
    const ehDeckEspecial = typeof templo === 'string' && templo.startsWith('deck_');

    // Sincronizar painéis, botões de aba e seletores
    if (ehDeckEspecial) {
      if (this.abaOrigem !== 'especiais') {
        this.trocarAbaOrigem('especiais', false);
      }
      const selDeck = document.getElementById('flashcard-deck-select');
      if (selDeck && selDeck.value !== templo) {
        selDeck.value = templo;
      }
      const chips = document.querySelectorAll('.fc-deck-chip');
      chips.forEach(chip => {
        if (chip.getAttribute('data-deck') === templo) {
          chip.classList.add('ativo');
        } else {
          chip.classList.remove('ativo');
        }
      });
    } else {
      if (this.abaOrigem !== 'templos') {
        this.trocarAbaOrigem('templos', false);
      }
      const selTemplo = document.getElementById('flashcard-templo-select');
      if (selTemplo && selTemplo.value !== String(templo)) {
        selTemplo.value = String(templo);
      }
    }

    if (!ehCustom && !ehDeckEspecial) {
      if (isNaN(templo)) return;
      if (!Progressao.temploDesbloqueado(templo)) {
        App.notificar('notif_fc_bloqueado', 'erro');
        return;
      }
      if (!App.estado.templosData[templo]) {
        App.notificar('notif_fc_vocab_nao_carregado', 'erro');
        return;
      }
    }

    if (ehDeckEspecial && (!App.estado.topFlashcards || !App.estado.topFlashcards.length)) {
      try {
        const resp = await fetch('data/top500_flashcards.json');
        const data = await resp.json();
        App.estado.topFlashcards = data.cards || [];
        this.topFlashcardsCache = data.cards || [];
      } catch (err) {
        console.error('Erro ao carregar top500_flashcards.json:', err);
      }
    }

    this.temploAtual     = templo;
    this.praticandoTodas = false;
    this.sessaoStats     = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
    if (!this._swipeInitialized) { this._iniciarSwipe(); this._swipeInitialized = true; }
    this.carregarCartas();
    this.indiceAtual = 0;
    this.virada      = false;

    const vazio   = document.getElementById('flashcard-vazio');
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display   = 'none';
    if (cardEl)  cardEl.style.display  = '';
    if (actions) actions.style.display = 'none';

    if (this.cartasDisponiveis.length === 0) {
      this.seletorRecolhido = false;
      this.mostrarVazio();
    } else {
      this.seletorRecolhido = true;
      this.mostrarCarta();
    }
    
    // Suporte ao botão de imitar por voz
    const btnGravar = document.getElementById('btn-gravar');
    if (btnGravar) {
      btnGravar.style.display = '';
    }
  },

  // ── Load and sort cards due for review ────────────────────
  carregarCartas() {
    let listaPalavras = [];

    if (typeof this.temploAtual === 'string' && this.temploAtual.startsWith('deck_')) {
      const deckKey = this.temploAtual.replace('deck_', '');
      const allCards = App.estado.topFlashcards || this.topFlashcardsCache || [];
      if (deckKey === 'all') {
        listaPalavras = allCards;
      } else {
        listaPalavras = allCards.filter(c => c.deck === deckKey);
      }
    } else if (this.temploAtual === 'custom') {
      const todos = App.estado?.vocabCache || [];
      listaPalavras = todos.filter(p => p._custom || p.templo_num === 0 || p.id?.startsWith('w_custom_') || p.id?.startsWith('vocab_custom_'));
    } else {
      const data = App.estado.templosData[this.temploAtual];
      listaPalavras = data?.palavras || [];
    }

    this.totalNoDeck = listaPalavras.length;

    if (!listaPalavras.length) { this.cartasDisponiveis = []; return; }

    const agora   = Date.now();
    const novas   = [];
    const devidas = [];

    listaPalavras.forEach(palavra => {
      let fsrs = App.estado.flashcardData[palavra.id];

      // Migrate SM-2 records automatically
      if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
        fsrs = FSRS.migrateSM2(fsrs);
        App.estado.flashcardData[palavra.id] = fsrs;
      }

      if (!fsrs || fsrs.state === 'new') {
        novas.push(palavra);
      } else if ((fsrs.nextReview || 0) <= agora) {
        devidas.push({ ...palavra, _nextReview: fsrs.nextReview || 0 });
      }
    });

    devidas.sort((a, b) => a._nextReview - b._nextReview);
    this.cartasDisponiveis = [...novas, ...devidas].slice(0, 20);
  },

  _limparEscritaCanvas() {
    const wrap = document.getElementById('fc-handwriting-wrap');
    if (wrap) wrap.remove();
  },

  limparEscrita() {
    const canvas = document.getElementById('fc-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  },

  _iniciarCanvasEscrita() {
    const canvas = document.getElementById('fc-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    ctx.scale(dpr, dpr);

    const isDark = document.body.classList.contains('dark-mode') || document.documentElement.getAttribute('data-tema') === 'dark';
    ctx.lineWidth = 3;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = isDark ? '#D4A843' : '#8B1E0F';

    let desenhando = false;
    let lastX = 0;
    let lastY = 0;

    const getPos = (e) => {
      const r = canvas.getBoundingClientRect();
      const clientX = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
      const clientY = e.clientY !== undefined ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
      return { x: clientX - r.left, y: clientY - r.top };
    };

    canvas.onpointerdown = (e) => {
      e.stopPropagation();
      try { canvas.setPointerCapture(e.pointerId); } catch (_) {}
      desenhando = true;
      const pos = getPos(e);
      lastX = pos.x;
      lastY = pos.y;
      ctx.beginPath();
      ctx.arc(lastX, lastY, ctx.lineWidth / 2, 0, Math.PI * 2);
      ctx.fill();
    };

    canvas.onpointermove = (e) => {
      if (!desenhando) return;
      e.stopPropagation();
      const pos = getPos(e);
      ctx.beginPath();
      ctx.moveTo(lastX, lastY);
      ctx.lineTo(pos.x, pos.y);
      ctx.stroke();
      lastX = pos.x;
      lastY = pos.y;
    };

    const stopDrawing = (e) => {
      if (desenhando && e) {
        try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
      }
      desenhando = false;
    };

    canvas.onpointerup = stopDrawing;
    canvas.onpointercancel = stopDrawing;
  },

  // ── Render current card ────────────────────────────────────
  mostrarCarta() {
    if (this.indiceAtual >= this.cartasDisponiveis.length) {
      this.mostrarVazio();
      return;
    }

    this.cartaAtual  = this.cartasDisponiveis[this.indiceAtual];
    this.virada      = false;
    this.nivelDica   = 0;
    this.dicaUsada   = false;

    // Reset dica button appearance
    const btnDica = document.getElementById('btn-dica');
    if (btnDica) { btnDica.classList.remove('ativo'); btnDica.title = 'Ver dica (nível 1)'; }

    const cardEl = document.getElementById('flashcard');
    if (cardEl) { cardEl.classList.remove('virado'); cardEl.style.display = ''; }
    const stageEl = document.querySelector('.fc-studio-stage');
    if (stageEl) stageEl.classList.remove('fc-stage-virado');

    const actions = document.getElementById('card-actions');
    if (actions) actions.style.display = 'none';

    const elIt   = document.getElementById('card-italiano');
    const elCat  = document.getElementById('card-categoria');
    const elDica = document.getElementById('card-dica');
    const elHelp = document.getElementById('selector-helper');
    const elTrad = document.getElementById('card-traducao');
    const elEx   = document.getElementById('card-exemplo');
    const elIpa  = document.getElementById('card-ipa');
    if (elHelp) elHelp.style.display = 'none';

    // Apply mode classes to card for CSS theming
    const cardEl2 = document.getElementById('flashcard');
    if (cardEl2) {
      cardEl2.classList.toggle('modo-reverso',  this.modoReverso  && !this.modoContexto && !this.modoEscuta);
      cardEl2.classList.toggle('modo-contexto', this.modoContexto);
      cardEl2.classList.toggle('modo-escuta',   this.modoEscuta);
    }

    if (this.modoEscuta) {
      // 👂 Listening: hide word on front, click card reveals it normally
      if (elIt)  elIt.textContent  = '🎧';
      if (elCat) elCat.textContent = '';
      if (elDica) elDica.textContent = I18n.t('fc_dica_revelar');
      if (elTrad) elTrad.textContent = this.cartaAtual.italiano || '—';
    } else if (this.modoContexto) {
      // 📖 Context: show example sentence with blank
      const ex = this.cartaAtual.exemplo || '';
      const mascarada = ex ? this._mascarar(this.cartaAtual.italiano, ex) : null;
      if (elIt) elIt.textContent = mascarada || `${this.cartaAtual.italiano} → ?`;
      if (elCat) elCat.textContent = this.cartaAtual.categoria || '';
      if (elDica) elDica.textContent = I18n.t('fc_dica_palavra_falta');
      if (elTrad) elTrad.textContent = this.cartaAtual.italiano || '—';
    } else if (this.modoEscrita) {
      if (elIt)  elIt.textContent  = this.cartaAtual.portugues || '—';
      if (elCat) elCat.textContent = this.cartaAtual.categoria || '';
      if (elDica) elDica.textContent = '✍️ Scrivi la parola in italiano e tocca per controllare';
      if (elTrad) elTrad.textContent = this.cartaAtual.italiano || '—';

      // Injeta o canvas de caligrafia / escrita à mão na frente
      this._limparEscritaCanvas();
      const front = document.querySelector('.card-frente');
      if (front) {
        const wrap = document.createElement('div');
        wrap.id = 'fc-handwriting-wrap';
        wrap.className = 'fc-handwriting-wrap';
        wrap.setAttribute('onclick', 'event.stopPropagation()');
        wrap.innerHTML = `
          <div class="fc-canvas-header">
            <span class="fc-canvas-label">✍️ Scrittura a mano:</span>
            <button type="button" class="fc-canvas-clear-btn" onclick="event.stopPropagation();Flashcards.limparEscrita()">🧹 Pulisci</button>
          </div>
          <div class="fc-canvas-box">
            <canvas id="fc-canvas"></canvas>
            <div class="fc-canvas-baseline"></div>
          </div>
        `;
        const tapPrompt = front.querySelector('.card-tap-prompt');
        if (tapPrompt) {
          front.insertBefore(wrap, tapPrompt);
        } else {
          front.appendChild(wrap);
        }
        setTimeout(() => this._iniciarCanvasEscrita(), 50);
      }
    } else if (this.modoReverso) {
      // 🔄 Reverse: PT front, IT back
      if (elIt)  elIt.textContent  = this.cartaAtual.portugues || '—';
      if (elCat) elCat.textContent = this.cartaAtual.categoria || '';
      if (elDica) elDica.textContent = I18n.t('fc_dica_revelar');
      if (elTrad) elTrad.textContent = this.cartaAtual.italiano || '—';
    } else {
      // Normal: IT front, PT back
      if (elIt)  elIt.textContent  = this.cartaAtual.italiano || '—';
      if (elCat) elCat.textContent = this.cartaAtual.categoria || '';
      if (elDica) elDica.textContent = I18n.t('fc_dica_revelar');
      if (elTrad) elTrad.textContent = this.cartaAtual.portugues || '—';
    }

    if (elEx) {
      const f   = this.cartaAtual.exemplo    || '';
      const fPt = this.cartaAtual.exemplo_pt ? ` — ${this.cartaAtual.exemplo_pt}` : '';
      elEx.textContent = f ? `"${f}"${fPt}` : '';
    }
    if (elIpa) {
      const raw = this.cartaAtual.audio_ipa || '';
      elIpa.textContent = raw ? (raw.startsWith('/') ? raw : `/${raw}/`) : '';
    }

    // Verso Italian header
    const elVersoIt = document.getElementById('card-verso-it');
    if (elVersoIt) elVersoIt.textContent = this.cartaAtual.italiano || '';

    // Deck stacking physical depth
    const restantes = this.cartasDisponiveis.length - this.indiceAtual;
    const layer1 = document.getElementById('deck-layer-1');
    const layer2 = document.getElementById('deck-layer-2');
    if (layer1) layer1.style.display = restantes >= 2 ? 'block' : 'none';
    if (layer2) layer2.style.display = restantes >= 3 ? 'block' : 'none';

    // Progressive hint pearls
    const elPearls = document.getElementById('dica-pearls');
    if (elPearls) {
      elPearls.textContent = this.nivelDica === 1 ? '● ○ ○' : (this.nivelDica === 2 ? '● ● ○' : (this.nivelDica >= 3 ? '● ● ●' : '○ ○ ○'));
    }

    // Mode pills update
    const isNormal = !this.modoReverso && !this.modoContexto && !this.modoEscuta;
    const btnNormal = document.getElementById('btn-modo-normal');
    if (btnNormal) btnNormal.classList.toggle('ativo', isNormal);
    const btnRev = document.getElementById('btn-reverso');
    if (btnRev) btnRev.classList.toggle('ativo', !!this.modoReverso);
    const btnCtx = document.getElementById('btn-contexto');
    if (btnCtx) btnCtx.classList.toggle('ativo', !!this.modoContexto);
    const btnEsc = document.getElementById('btn-escuta');
    if (btnEsc) btnEsc.classList.toggle('ativo', !!this.modoEscuta);

    this.atualizarContador();
    this._sincronizarBarraCompacta();
    // Update favorite button state
    const btnFav = document.getElementById('btn-favorito');
    if (btnFav) btnFav.textContent = App.ehFavorito(this.cartaAtual.id) ? '❤️' : '🤍';

    const vazio = document.getElementById('flashcard-vazio');
    if (vazio) vazio.style.display = 'none';
  },

  // ── Update progress counter with retrievability ───────────
  atualizarContador() {
    const elInfo = document.getElementById('card-info');
    if (!elInfo) return;

    const total = this.cartasDisponiveis.length;
    const atual = this.indiceAtual + 1;

    // Show current card's retrievability if it has a history
    let rStr = '';
    if (this.cartaAtual) {
      const fsrs = App.estado.flashcardData[this.cartaAtual.id];
      if (fsrs && fsrs.stability > 0 && fsrs.lastReview) {
        const tDays = (Date.now() - fsrs.lastReview) / 86400000;
        const r     = FSRS.retrievability(tDays, fsrs.stability);
        rStr        = ` <span class="fc-retrievability-pill">R ${Math.round(r * 100)}%</span>`;
      }
    }

    const novosCount   = this.cartasDisponiveis.filter(c => !App.estado.flashcardData[c.id] || App.estado.flashcardData[c.id].state === 'new').length;
    const revisaoCount = total - novosCount;
    const partes       = [];
    if (novosCount   > 0) partes.push(`${novosCount} ${I18n.t('fc_novas')}`);
    if (revisaoCount > 0) partes.push(`${revisaoCount} ${I18n.t('fc_revisao')}`);

    elInfo.innerHTML = `<span>Carta <strong>${atual}</strong> de ${total}${partes.length ? ' &nbsp;·&nbsp; ' + partes.join(', ') : ''}</span>${rStr}`;
  },

  // ── Flip card to reveal answer ─────────────────────────────
  virar() {
    if (this.virada || !this.cartaAtual) return;
    this.virada = true;
    if (typeof SomFeedback !== 'undefined') SomFeedback.virar();

    const cardEl = document.getElementById('flashcard');
    if (cardEl) cardEl.classList.add('virado');
    const stageEl = document.querySelector('.fc-studio-stage');
    if (stageEl) stageEl.classList.add('fc-stage-virado');

    // Show action buttons with interval previews (In-Place replacement of front toolbelt emphasis)
    const actions = document.getElementById('card-actions');
    if (actions) {
      actions.style.display = 'grid';
      this._atualizarBotoesIntervalo();
      if (this.dicaUsada) this._aplicarPenalidadeDica();
    }
  },

  // ── Progressive hints ─────────────────────────────────────
  mostrarDica() {
    if (this.virada || !this.cartaAtual) return;
    this.nivelDica++;
    this.dicaUsada = true;

    // Mark dica button
    const btnDica = document.getElementById('btn-dica');
    if (btnDica) btnDica.classList.add('ativo');
    const elPearls = document.getElementById('dica-pearls');
    if (elPearls) {
      elPearls.textContent = this.nivelDica === 1 ? '● ○ ○' : (this.nivelDica === 2 ? '● ● ○' : '● ● ●');
    }

    // In reverse mode the target word is Italian; in context mode the user
    // must guess the Italian word (fill the blank); in normal mode it's Portuguese.
    const alvo = (this.modoReverso || this.modoContexto)
      ? this.cartaAtual.italiano
      : this.cartaAtual.portugues;
    const elDica = document.getElementById('card-dica');

    if (this.nivelDica === 1) {
      // Level 1: first letter + blanks
      const hint = alvo.charAt(0).toUpperCase() + '_'.repeat(Math.max(1, alvo.length - 1));
      if (elDica) elDica.textContent = `💡 ${hint}`;
      if (btnDica) btnDica.title = 'Ver dica (nível 2)';
    } else if (this.nivelDica === 2) {
      // Level 2: first third of letters revealed
      const revealed = Math.max(2, Math.ceil(alvo.length / 3));
      const hint = alvo.substring(0, revealed) + '_'.repeat(Math.max(1, alvo.length - revealed));
      if (elDica) elDica.textContent = `💡💡 ${hint}`;
      if (btnDica) btnDica.title = 'Ver dica (revelar)';
    } else {
      // Level 3: just flip the card.
      // virar() will call _aplicarPenalidadeDica() because dicaUsada===true,
      // so we must NOT call it again here to avoid double application.
      if (elDica) elDica.textContent = `💡💡💡 Revelado`;
      this.virar();
    }
  },

  _aplicarPenalidadeDica() {
    ['btn-good', 'btn-easy'].forEach(id => {
      const btn = document.getElementById(id);
      if (btn) btn.classList.add('dica-penalizado');
    });
  },

  // ── Update button interval previews ───────────────────────
  _atualizarBotoesIntervalo() {
    if (!this.cartaAtual) return;
    let fsrs = App.estado.flashcardData[this.cartaAtual.id];
    if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
      fsrs = FSRS.migrateSM2(fsrs);
    }
    const card     = fsrs || { state: 'new', difficulty: 5, stability: 0, lastReview: null };
    const previews = FSRS.previewIntervals(card);

    const labels = ['btn-again', 'btn-hard', 'btn-good', 'btn-easy'];
    labels.forEach((id, i) => {
      const el = document.getElementById(id);
      if (!el) return;
      const sub = el.querySelector('.btn-intervalo');
      if (sub) sub.textContent = FSRS.formatInterval(previews[i]);
    });
  },

  // ── Rate the card (FSRS 4-button model) ───────────────────
  // rating: 1=Again, 2=Hard, 3=Good, 4=Easy
  avaliar(rating) {
    if (!this.cartaAtual) return;
    try {
      const carta = this.cartaAtual;

      let fsrs = App.estado.flashcardData[carta.id];
      if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
        fsrs = FSRS.migrateSM2(fsrs);
      }
      if (!fsrs) {
        fsrs = { state: 'new', difficulty: 5, stability: 0, retrievability: 1,
                 lapses: 0, reps: 0, lastReview: null, interval: 0, nextReview: null };
      }

      const wasNew = !fsrs || fsrs.state === 'new';
      const updated = FSRS.review(fsrs, rating);

      // Track error count for "Parole Difficili" feature
      // FSRS.review spreads ...card so 'erros' is preserved; we update it here
      const errosAnteriores = updated.erros || 0;
      if (rating === 1)      updated.erros = errosAnteriores + 1;
      else if (rating >= 3)  updated.erros = Math.max(0, errosAnteriores - 1);
      // rating === 2 (Hard): erros unchanged

      App.estado.flashcardData[carta.id] = updated;
      App.salvarFlashcards();

      // XP: Again=0, Hard=5, Good=10, Easy=15; +5 bonus in context/listen modes
      const xpMap = [0, 0, 5, 10, 15];
      const xpBonus = (this.modoContexto || this.modoEscuta) ? 5 : 0;
      const xpGanho = (xpMap[rating] || 0) + xpBonus;
      if (xpGanho > 0) {
        // Route through Progressao.ganhar() so xp_hoje, level-up and
        // temple-unlock checks all fire correctly from flashcard reviews.
        if (typeof Progressao !== 'undefined') {
          Progressao.ganhar(xpGanho);
        } else {
          App.estado.progresso.xp += xpGanho;
          App.salvarProgresso();
          App.atualizarStats();
        }
      }

      // Track session stats
      if (this.sessaoStats) {
        const rNames = ['', 'again', 'hard', 'good', 'easy'];
        this.sessaoStats[rNames[rating]]++;
        this.sessaoStats.xp += xpGanho;
        if (wasNew && updated.state === 'review') {
          this.sessaoStats.novas.push(carta);
        }
      }

      // Log to heatmap diary
      if (typeof Calor !== 'undefined') Calor.registrar(1);

      if (typeof Progressao !== 'undefined' && Progressao.temploConcluido(this.temploAtual)) {
        Progressao.marcarTemploConcluido(this.temploAtual);
      }

      // Check achievements off the critical path to avoid jank on card transition
      if (typeof Conquistas !== 'undefined') {
        if (typeof requestIdleCallback === 'function') requestIdleCallback(() => Conquistas.verificar());
        else setTimeout(() => Conquistas.verificar(), 300);
      }

      this.proxima();
    } catch (err) {
      console.error('[FSRS] avaliar() error:', err);
      App.notificar('notif_fc_erro_resposta', 'erro');
      this.proxima(); // advance anyway so user isn't stuck
    }
  },

  // ── Advance to next card ───────────────────────────────────
  proxima() {
    this.indiceAtual++;
    this.virada = false;
    if (this.indiceAtual >= this.cartasDisponiveis.length) {
      this.mostrarVazio();
    } else {
      this.mostrarCarta();
    }
  },

  // ── Empty / all-done state ────────────────────────────────
  mostrarVazio() {
    this.seletorRecolhido = false;
    this._sincronizarBarraCompacta();
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    const vazio   = document.getElementById('flashcard-vazio');
    const resumo  = document.getElementById('flashcard-resumo');
    const info    = document.getElementById('card-info');
    const stageEl = document.querySelector('.fc-studio-stage');
    if (stageEl) stageEl.classList.remove('fc-stage-virado');

    if (cardEl)  cardEl.style.display  = 'none';
    if (actions) actions.style.display = 'none';
    if (info)    info.textContent      = '';

    const total = this.sessaoStats
      ? (this.sessaoStats.again + this.sessaoStats.hard + this.sessaoStats.good + this.sessaoStats.easy)
      : 0;

    if (total > 0 && resumo) {
      if (vazio) vazio.style.display = 'none';
      this.mostrarResumo();
    } else {
      if (resumo) resumo.style.display = 'none';
      if (vazio)  vazio.style.display  = 'block';
    }
  },

  // ── Session summary screen ─────────────────────────────────
  mostrarResumo() {
    const resumo = document.getElementById('flashcard-resumo');
    if (!resumo || !this.sessaoStats) return;
    const s = this.sessaoStats;
    const total = s.again + s.hard + s.good + s.easy;
    const acertos = s.good + s.easy;
    const pct = total > 0 ? Math.round((acertos / total) * 100) : 0;

    let emoji = '🎉';
    let titulo = 'Sessione completata!';
    if (pct >= 80) { emoji = '🏆'; titulo = 'Ottimo lavoro!'; }
    else if (pct >= 60) { emoji = '👏'; titulo = I18n.t('fc_resumo_muito_bom'); }
    else if (pct < 40) { emoji = '💪'; titulo = I18n.t('fc_resumo_continua'); }

    // Next due card
    let proxLabel = I18n.t('fc_resumo_sem_agendamento');
    if (this.temploAtual) {
      let palavrasTemplo = [];
      if (this.temploAtual === 'custom') {
        palavrasTemplo = (App.estado?.vocabCache || []).filter(p => p._custom || p.templo_num === 0 || p.id?.startsWith('w_custom_') || p.id?.startsWith('vocab_custom_'));
      } else {
        const data = App.estado.templosData[this.temploAtual];
        palavrasTemplo = data?.palavras || [];
      }
      if (palavrasTemplo.length > 0) {
        const agora = Date.now();
        const proximas = palavrasTemplo
          .map(p => App.estado.flashcardData[p.id])
          .filter(f => f && f.nextReview && f.nextReview > agora)
          .map(f => f.nextReview)
          .sort((a, b) => a - b);
        if (proximas.length > 0) {
          const diffMs = proximas[0] - agora;
          const diffH  = Math.round(diffMs / 3600000);
          const diffD  = Math.round(diffMs / 86400000);
          proxLabel = diffD >= 1
            ? I18n.t(diffD > 1 ? 'fc_resumo_em_dias_plural' : 'fc_resumo_em_dias').replace('{n}', diffD)
            : I18n.t('fc_resumo_em_horas').replace('{n}', diffH);
        }
      }
    }

    const novCount = s.novas.length;

    resumo.innerHTML = `
      <div class="resumo-card">
        <div class="resumo-emoji">${emoji}</div>
        <div class="resumo-titulo">${titulo}</div>
        <div class="resumo-stats-grid">
          <div class="resumo-stat">
            <span class="resumo-num">${total}</span>
            <span class="resumo-lab">${I18n.t('fc_resumo_cartas')}</span>
          </div>
          <div class="resumo-stat">
            <span class="resumo-num">${pct}%</span>
            <span class="resumo-lab">${I18n.t('fc_resumo_acertos')}</span>
          </div>
          ${s.xp > 0 ? `<div class="resumo-stat"><span class="resumo-num">+${s.xp}</span><span class="resumo-lab">XP</span></div>` : ''}
        </div>
        <div class="resumo-ratings">
          ${s.again > 0 ? `<span class="rr rr-again">❌ ${s.again}</span>` : ''}
          ${s.hard  > 0 ? `<span class="rr rr-hard">⚡ ${s.hard}</span>` : ''}
          ${s.good  > 0 ? `<span class="rr rr-good">✅ ${s.good}</span>` : ''}
          ${s.easy  > 0 ? `<span class="rr rr-easy">⭐ ${s.easy}</span>` : ''}
        </div>
        ${novCount > 0 ? `<p class="resumo-novas">${I18n.t(novCount > 1 ? 'fc_resumo_novas_plural' : 'fc_resumo_novas').replace('{n}', novCount)}</p>` : ''}
        <p class="resumo-proxima">${I18n.t('fc_resumo_proxima')} <strong>${proxLabel}</strong></p>
        <div class="resumo-acoes">
          <button class="btn-primario" onclick="Flashcards.praticaTodas()">${I18n.t('fc_resumo_praticar')}</button>
        </div>
      </div>
    `;
    resumo.style.display = 'block';
  },

  // ── Toggle favorite for current card (Optimistic UI) ───────
  toggleFavorito() {
    if (!this.cartaAtual) return;
    const btn = document.getElementById('btn-favorito');
    const adicionado = App.toggleFavorito(this.cartaAtual.id, btn);
    if (btn) btn.textContent = adicionado ? '❤️' : '🤍';
    App.notificar(adicionado ? 'notif_fc_favorito_add' : 'notif_fc_favorito_rem', 'alerta');
  },

  // ── Study favorite words ──────────────────────────────────
  estudarFavoritos() {
    const favIds = (App.estado.progresso || {}).favoritos || [];
    if (favIds.length === 0) {
      App.notificar('notif_fc_sem_favoritos', 'alerta');
      return;
    }
    // Busca em todos os templos carregados via vocabCache (inclui T11-T50)
    const favPalavras = (App.estado.vocabCache || []).filter(p => favIds.includes(p.id));
    if (favPalavras.length === 0) {
      App.notificar('notif_fc_favoritos_nao_enc', 'erro');
      return;
    }
    this.temploAtual      = null;
    this.praticandoTodas  = false;
    this.sessaoStats      = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
    this.cartasDisponiveis = favPalavras;
    this.indiceAtual      = 0;
    this.virada           = false;
    const vazio = document.getElementById('flashcard-vazio');
    const resumo = document.getElementById('flashcard-resumo');
    const cardEl = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display  = 'none';
    if (resumo)  resumo.style.display = 'none';
    if (cardEl)  cardEl.style.display = '';
    if (actions) actions.style.display = 'none';
    App.navegar('flashcard');
    this.seletorRecolhido = true;
    App.notificar(I18n.t('notif_fc_favoritos_revisar').replace('{n}', favPalavras.length), 'alerta');
    this.mostrarCarta();
  },

  // ── Study difficult words (erros >= 3) across all templos ─
  estudarDificeis() {
    const dificeis = [];
    const desbloqueados = App.estado.progresso ? App.estado.progresso.templos_desbloqueados : [1];
    desbloqueados.forEach(num => {
      const data = App.estado.templosData[num];
      if (!data || !data.palavras) return;
      data.palavras.forEach(p => {
        const fsrs = App.estado.flashcardData[p.id];
        if (fsrs && (fsrs.erros || 0) >= 3) dificeis.push(p);
      });
    });

    if (dificeis.length === 0) {
      App.notificar('notif_fc_sem_dificeis', 'sucesso');
      return;
    }

    // Sort by most errors first
    dificeis.sort((a, b) => {
      const ea = (App.estado.flashcardData[a.id] || {}).erros || 0;
      const eb = (App.estado.flashcardData[b.id] || {}).erros || 0;
      return eb - ea;
    });

    this.temploAtual    = null;
    this.praticandoTodas = false;
    this.sessaoStats    = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
    this.cartasDisponiveis = dificeis.slice(0, 20);
    this.indiceAtual   = 0;
    this.virada        = false;

    const vazio   = document.getElementById('flashcard-vazio');
    const resumo  = document.getElementById('flashcard-resumo');
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display   = 'none';
    if (resumo)  resumo.style.display  = 'none';
    if (cardEl)  cardEl.style.display  = '';
    if (actions) actions.style.display = 'none';

    App.navegar('flashcard');
    this.seletorRecolhido = true;
    App.notificar(I18n.t('notif_fc_dificeis_revisar').replace('{n}', dificeis.length), 'alerta');
    this.mostrarCarta();
  },

  // ── Mode toggles (mutually exclusive) ────────────────────
  _limparModos() {
    this.modoReverso  = false;
    this.modoContexto = false;
    this.modoEscuta   = false;
    this.modoEscrita  = false;
    ['btn-modo-normal', 'btn-reverso', 'btn-contexto', 'btn-escuta', 'btn-escrita'].forEach(id => {
      const b = document.getElementById(id);
      if (b) b.classList.remove('ativo');
    });
    const btnNormal = document.getElementById('btn-modo-normal');
    if (btnNormal) btnNormal.classList.add('ativo');
    this.seletorRecolhido = true;
  },

  toggleReverso() {
    const novoValor = !this.modoReverso;
    this._limparModos();
    this.modoReverso = novoValor;
    const btn = document.getElementById('btn-reverso');
    if (btn) btn.classList.toggle('ativo', this.modoReverso);
    this.seletorRecolhido = true;
    if (this.cartaAtual) this.mostrarCarta();
  },

  toggleContexto() {
    const novoValor = !this.modoContexto;
    this._limparModos();
    this.modoContexto = novoValor;
    const btn = document.getElementById('btn-contexto');
    if (btn) btn.classList.toggle('ativo', this.modoContexto);
    this.seletorRecolhido = true;
    if (this.cartaAtual) this.mostrarCarta();
  },

  toggleEscrita() {
    const novoValor = !this.modoEscrita;
    this._limparModos();
    this.modoEscrita = novoValor;
    const btn = document.getElementById('btn-escrita');
    if (btn) btn.classList.toggle('ativo', this.modoEscrita);
    const btnNormal = document.getElementById('btn-modo-normal');
    if (btnNormal && this.modoEscrita) btnNormal.classList.remove('ativo');
    this.seletorRecolhido = true;
    if (this.cartaAtual) this.mostrarCarta();
  },

  toggleEscuta() {
    const novoValor = !this.modoEscuta;
    this._limparModos();
    this.modoEscuta = novoValor;
    const btn = document.getElementById('btn-escuta');
    if (btn) btn.classList.toggle('ativo', this.modoEscuta);
    this.seletorRecolhido = true;
    if (this.cartaAtual) {
      this.mostrarCarta();
      // Pronunciar imediatamente dentro do gesto do usuário (evita bloqueio mobile)
      if (this.modoEscuta) this.pronunciar();
    }
  },

  // ── Mask Italian word in example sentence ─────────────────
  // Handles: accented chars, short words (≤4 chars), inflected forms.
  _mascarar(italiano, exemplo) {
    if (!italiano || !exemplo) return exemplo || '';

    const escape = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

    // 1. Exact case-insensitive match (handles most cases)
    const r1 = exemplo.replace(new RegExp(escape(italiano), 'gi'), '___');
    if (r1 !== exemplo) return r1;

    // 2. Diacritic-insensitive: strip combining marks, find position, replace in original
    const stripped = s => s.normalize('NFD').replace(/[̀-ͯ]/g, '');
    const exStripped = stripped(exemplo);
    const itStripped = stripped(italiano);
    const idx = exStripped.toLowerCase().indexOf(itStripped.toLowerCase());
    if (idx !== -1) {
      return exemplo.slice(0, idx) + '___' + exemplo.slice(idx + italiano.length);
    }

    // 3. Prefix match on first 4 chars (covers inflected forms, e.g. "caffè" → "caff")
    if (italiano.length >= 3) {
      const prefix = escape(stripped(italiano).slice(0, Math.min(4, italiano.length)));
      const r3 = exStripped.replace(new RegExp(prefix + '\\S*', 'gi'), '___');
      if (r3 !== exStripped) {
        // Apply the same replacement to the original text
        return exemplo.replace(new RegExp(escape(italiano.slice(0, Math.min(4, italiano.length))) + '\\S*', 'gi'), '___');
      }
    }

    // 4. No match found — show placeholder so the answer is never accidentally revealed
    return `___ (${italiano.length} lettre)`;
  },

  // ── Swipe-to-rate (touch devices) ─────────────────────────
  _iniciarSwipe() {
    const arena = document.querySelector('.flashcard-arena');
    if (!arena) return;

    arena.addEventListener('touchstart', (e) => {
      const t = e.touches[0];
      this._swipeStartX = t.clientX;
      this._swipeStartY = t.clientY;
    }, { passive: true });

    arena.addEventListener('touchmove', (e) => {
      if (!this.virada || !this.cartaAtual) return;
      const dx = e.touches[0].clientX - this._swipeStartX;
      const inner = document.querySelector('#flashcard .card-inner');
      if (inner) {
        const tilt = Math.max(-7, Math.min(7, dx * 0.04));
        const slide = dx * 0.12;
        inner.style.transform = `rotateY(180deg) rotate(${tilt}deg) translateX(${-slide}px)`;
      }
      this._mostrarSwipeHint(dx);
    }, { passive: true });

    arena.addEventListener('touchend', (e) => {
      const t = e.changedTouches[0];
      const dx = t.clientX - this._swipeStartX;
      const dy = t.clientY - this._swipeStartY;

      // Reset tilt
      const inner = document.querySelector('#flashcard .card-inner');
      if (inner) inner.style.transform = '';
      this._esconderSwipeHints();

      const absDx = Math.abs(dx), absDy = Math.abs(dy);

      if (!this.virada) {
        // Swipe down → pronunciar
        if (absDy > 55 && dy > 0 && absDy > absDx * 1.5) this.pronunciar();
        return;
      }
      // Rating swipes — require minimum 55px
      if (absDx < 55) return;
      if      (dx < -110) this.avaliar(1); // strong left → Again
      else if (dx <  -55) this.avaliar(2); // mild left  → Hard
      else if (dx >  110) this.avaliar(4); // strong right → Easy
      else if (dx >   55) this.avaliar(3); // mild right  → Good
    }, { passive: true });
  },

  _mostrarSwipeHint(dx) {
    const left  = document.getElementById('swipe-hint-left');
    const right = document.getElementById('swipe-hint-right');
    const absDx = Math.abs(dx);
    const opacity = Math.min(0.95, absDx / 70);
    if (dx < 0) {
      if (left)  { left.style.opacity  = opacity; left.textContent  = dx < -110 ? '❌ Again' : '⚡ Hard'; }
      if (right) right.style.opacity = 0;
    } else {
      if (right) { right.style.opacity = opacity; right.textContent = dx > 110 ? '⭐ Easy' : '✅ Good'; }
      if (left)  left.style.opacity  = 0;
    }
  },

  _esconderSwipeHints() {
    ['swipe-hint-left','swipe-hint-right'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.style.opacity = 0;
    });
  },

  // ── Revisão Geral: all due cards across ALL unlocked temples ─
  initRevisaoGeral() {
    const p = App.estado.progresso;
    if (!p) return;
    const agora = Date.now();
    const novas = [], devidas = [];

    p.templos_desbloqueados.forEach(num => {
      const data = App.estado.templosData[num];
      if (!data || !data.palavras) return;
      data.palavras.forEach(palavra => {
        let fsrs = App.estado.flashcardData[palavra.id];
        if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
          fsrs = FSRS.migrateSM2(fsrs);
          App.estado.flashcardData[palavra.id] = fsrs;
        }
        if (!fsrs || fsrs.state === 'new') {
          novas.push(palavra);
        } else if ((fsrs.nextReview || 0) <= agora) {
          devidas.push({ ...palavra, _nextReview: fsrs.nextReview || 0 });
        }
      });
    });

    // Inclui também palavras adicionadas via IA / personalizadas
    const customVocab = (App.estado?.vocabCache || []).filter(p => p._custom || p.templo_num === 0 || p.id?.startsWith('w_custom_') || p.id?.startsWith('vocab_custom_'));
    customVocab.forEach(palavra => {
      let fsrs = App.estado.flashcardData[palavra.id];
      if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
        fsrs = FSRS.migrateSM2(fsrs);
        App.estado.flashcardData[palavra.id] = fsrs;
      }
      if (!fsrs || fsrs.state === 'new') {
        novas.push(palavra);
      } else if ((fsrs.nextReview || 0) <= agora) {
        devidas.push({ ...palavra, _nextReview: fsrs.nextReview || 0 });
      }
    });

    devidas.sort((a, b) => a._nextReview - b._nextReview);
    // Mix: prioritize overdue, sprinkle new cards (max 5 new per session)
    const novasLimitadas = novas.slice(0, 5);
    const total = [...devidas, ...novasLimitadas];

    if (total.length === 0) {
      App.notificar('🎉 Nessuna carta in scadenza oggi!', 'sucesso');
      return;
    }

    // Shuffle for variety
    for (let i = total.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [total[i], total[j]] = [total[j], total[i]];
    }

    this.temploAtual       = null; // cross-temple mode
    this.praticandoTodas   = false;
    this.sessaoStats       = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
    this.cartasDisponiveis = total.slice(0, 30); // cap at 30
    this.indiceAtual       = 0;
    this.virada            = false;
    if (!this._swipeInitialized) { this._iniciarSwipe(); this._swipeInitialized = true; }

    const vazio   = document.getElementById('flashcard-vazio');
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display   = 'none';
    if (cardEl)  cardEl.style.display  = '';
    if (actions) actions.style.display = 'none';

    const total_devidas = devidas.length;
    this.seletorRecolhido = true;
    App.notificar(`🌍 ${total_devidas} carta${total_devidas !== 1 ? 's' : ''} em revisão + ${novasLimitadas.length} novas`, 'alerta');
    this.mostrarCarta();
  },

  // ── Practice all cards regardless of schedule ─────────────
  praticaTodas() {
    let palavrasTemplo = [];
    if (typeof this.temploAtual === 'string' && this.temploAtual.startsWith('deck_')) {
      const deckKey = this.temploAtual.replace('deck_', '');
      const allCards = App.estado.topFlashcards || this.topFlashcardsCache || [];
      palavrasTemplo = deckKey === 'all' ? allCards : allCards.filter(c => c.deck === deckKey);
    } else if (this.temploAtual === 'custom') {
      palavrasTemplo = (App.estado?.vocabCache || []).filter(p => p._custom || p.templo_num === 0 || p.id?.startsWith('w_custom_') || p.id?.startsWith('vocab_custom_'));
    } else {
      const data = App.estado.templosData[this.temploAtual];
      palavrasTemplo = data?.palavras || [];
    }
    if (!palavrasTemplo || palavrasTemplo.length === 0) return;
    this.praticandoTodas  = true;
    this.sessaoStats      = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
    this.cartasDisponiveis = [...palavrasTemplo];
    this.indiceAtual      = 0;
    this.virada           = false;
    this.seletorRecolhido = true;

    const vazio   = document.getElementById('flashcard-vazio');
    const resumo  = document.getElementById('flashcard-resumo');
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display   = 'none';
    if (resumo)  resumo.style.display  = 'none';
    if (cardEl)  cardEl.style.display  = '';
    if (actions) actions.style.display = 'none';

    this.mostrarCarta();
  },

  // ── Pronounce the current word ────────────────────────────
  pronunciar() {
    if (this.cartaAtual && this.cartaAtual.italiano) {
      App.pronunciar(this.cartaAtual.italiano);
    }
  },

  pronunciarLento() {
    if (this.cartaAtual && this.cartaAtual.italiano) {
      App.pronunciar(this.cartaAtual.italiano, 0.72);
    }
  },

  // ── Populate temple and special deck selectors ────────────
  atualizarSelectTemplo() {
    const sel = document.getElementById('flashcard-templo-select');
    if (sel) {
      const anterior = sel.value;
      sel.innerHTML  = '<option value="">-- Seleziona tempio --</option>';

      // Grupo dos Templos do Conhecimento (apenas templos desbloqueados)
      const optGroupTemplos = document.createElement('optgroup');
      optGroupTemplos.label = '🏛️ Templos do Conhecimento';
      const desbloqueados = App.estado.progresso ? App.estado.progresso.templos_desbloqueados : [1];
      desbloqueados.forEach(num => {
        const data = App.estado.templosData[num];
        if (!data) return;
        const opt        = document.createElement('option');
        opt.value        = num;
        const nomeTemplo = data.nome || (App.TEMPLO_NOMES && App.TEMPLO_NOMES[num]) || `Tempio ${num}`;
        opt.textContent  = `${num}. ${nomeTemplo} (${data.cidade})`;
        optGroupTemplos.appendChild(opt);
      });
      sel.appendChild(optGroupTemplos);

      // Opção de deck customizado se houver palavras adicionadas via IA
      const customVocab = (App.estado?.vocabCache || []).filter(p => p._custom || p.templo_num === 0 || p.id?.startsWith('w_custom_') || p.id?.startsWith('vocab_custom_'));
      if (customVocab.length > 0) {
        const optCustom = document.createElement('option');
        optCustom.value = 'custom';
        optCustom.textContent = `🤖 Palavras Adicionadas (${customVocab.length})`;
        optCustom.style.fontWeight = 'bold';
        optCustom.style.color = '#7B68A0';
        sel.appendChild(optCustom);
      }

      if (anterior && sel.querySelector(`option[value="${anterior}"]`)) {
        sel.value = anterior;
      }
    }

    // Seletor exclusivo para Baralhos Especiais (Top 500)
    const selDeck = document.getElementById('flashcard-deck-select');
    if (selDeck) {
      const deckAnterior = selDeck.value || 'deck_all';
      selDeck.innerHTML = `
        <option value="deck_all">⭐ Todos os 500 Cards</option>
        <option value="deck_colocacoes">🧩 Colocações & Chunks (100)</option>
        <option value="deck_falsi_amici">⚠️ Falsos Amigos / Falsi Amici (100)</option>
        <option value="deck_preposizioni">📍 Preposições & Regências (100)</option>
        <option value="deck_verbi_irregolari">⚡ Verbos Irregulares em Contexto (100)</option>
        <option value="deck_situazioni_reali">🎭 Situações da Vida Real (100)</option>
      `;
      if (selDeck.querySelector(`option[value="${deckAnterior}"]`)) {
        selDeck.value = deckAnterior;
      }
    }
  },

  // ── Speech Recognition (Modo Imitação) ──────────────────────
  _iniciarReconhecimento() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return null;
    const r = new SR();
    r.lang = 'it-IT';
    r.continuous = false;
    r.interimResults = false;
    return r;
  },

  _atualizarBotaoGravar(gravando) {
    const btn = document.getElementById('btn-gravar');
    if (!btn) return;
    if (gravando) {
      const pararTxt = (typeof I18n !== 'undefined' && I18n.t('fc_gravar_parar') ? I18n.t('fc_gravar_parar').replace(/^[^\w\s]+\s*/, '') : 'Parar');
      btn.innerHTML = `<span class="btn-tool-icon">⏹️</span><span class="btn-tool-label">${pararTxt}</span>`;
      btn.style.background = '#C0392B';
      btn.style.color = '#fff';
    } else {
      const imitarTxt = (typeof I18n !== 'undefined' && I18n.t('fc_btn_imitar') ? I18n.t('fc_btn_imitar') : 'Imitar');
      btn.innerHTML = `<span class="btn-tool-icon">🎤</span><span class="btn-tool-label">${imitarTxt}</span>`;
      btn.style.background = '';
      btn.style.color = '';
    }
  },

  toggleGravar() {
    if (!this.cartaAtual) return;

    // Cancela qualquer reprodução de TTS / sintetizador de áudio em andamento
    if ('speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (_) {}
    }
    if (typeof VoiceEngine !== 'undefined' && VoiceEngine.parar) {
      try { VoiceEngine.parar(); } catch (_) {}
    }

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      App.notificar('Reconhecimento de voz não suportado neste navegador. Recomendamos Google Chrome (Android) ou Safari (iOS).', 'alerta');
      return;
    }
    
    if (this.gravando) {
      if (this._recognition) {
        try { this._recognition.stop(); } catch (_) {}
        this._recognition = null;
      }
      this.gravando = false;
      this._atualizarBotaoGravar(false);
      return;
    }
    
    this.gravando = true;
    this._atualizarBotaoGravar(true);
    
    // Instância fresca por sessão para suporte pleno no Chrome Android e Safari iOS
    const rec = new SR();
    rec.lang = 'it-IT';
    rec.continuous = false;
    rec.interimResults = false;
    rec.maxAlternatives = 1;
    
    rec.onresult = (e) => {
      const texto = (e.results[0][0].transcript || '').toLowerCase();
      const alvo = (this.cartaAtual.italiano || '').toLowerCase();
      
      const textoNormalize = texto.replace(/[.,!?;:]/g, '').trim();
      const alvoNormalize = alvo.replace(/[.,!?;:]/g, '').trim();
      
      const reconheceu = textoNormalize.includes(alvoNormalize) || alvoNormalize.includes(textoNormalize.split(' ')[0]);
      this._mostrarFeedbackPronuncia(texto, reconheceu);
    };

    rec.onerror = (event) => {
      console.warn('[Flashcards] Erro no reconhecimento:', event?.error);
      this.gravando = false;
      this._recognition = null;
      this._atualizarBotaoGravar(false);
      if (event?.error === 'not-allowed') {
        App.notificar('Permissão de microfone negada. Verifique as permissões do navegador.', 'erro');
      } else if (event?.error === 'no-speech') {
        App.notificar('Nenhuma fala detectada. Fale mais perto do microfone.', 'alerta');
      } else if (event?.error === 'audio-capture') {
        App.notificar('Microfone ocupado por outro app.', 'alerta');
      } else if (event?.error === 'network') {
        App.notificar('Erro de rede no serviço de voz. Verifique sua conexão.', 'alerta');
      } else if (event?.error !== 'aborted') {
        App.notificar('notif_fc_nao_ouviu', 'alerta');
      }
    };

    rec.onend = () => {
      this.gravando = false;
      this._recognition = null;
      this._atualizarBotaoGravar(false);
    };

    this._recognition = rec;
    try {
      rec.start();
    } catch (err) {
      console.warn('[Flashcards] Falha ao iniciar reconhecimento:', err);
      this.gravando = false;
      this._recognition = null;
      this._atualizarBotaoGravar(false);
    }
  },

  _mostrarFeedbackPronuncia(texto, reconheceu) {
    const fb = document.getElementById('imitacao-feedback');
    if (!fb) return;
    if (reconheceu) {
      fb.innerHTML = `<span style="color:#27AE60">✅ Perfetto! Ouvimos: "${texto}"</span>`;
      if (typeof Progressao !== 'undefined') Progressao.ganhar(3);
      else if (typeof App !== 'undefined') App.ganharXP(3);
    } else {
      fb.innerHTML = `<span style="color:#E67E22">🔄 Ouvimos: "${texto}" — tente de novo!</span>`;
    }
    fb.style.display = 'block';
    setTimeout(() => { if(fb) fb.style.display = 'none'; }, 4000);
  }
};

document.addEventListener('i18n:changed', () => {
  if (!document.getElementById('flashcard')) return;
  const vazio  = document.getElementById('flashcard-vazio');
  const resumo = document.getElementById('flashcard-resumo');

  if (resumo && resumo.style.display !== 'none') {
    Flashcards.mostrarResumo();
  } else if (vazio && vazio.style.display !== 'none') {
    Flashcards.mostrarVazio();
  } else if (Flashcards.cartaAtual) {
    Flashcards.mostrarCarta();
  }
});


// ── Atalhos de Teclado no Flashcards ────────────────────────
window.addEventListener('keydown', (e) => {
  const tag = (e.target.tagName || '').toUpperCase();
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target.isContentEditable) return;

  const sec = document.getElementById('sec-flashcard');
  if (!sec || !sec.classList.contains('active')) return;
  if (!Flashcards.cartaAtual || !Flashcards.cartasDisponiveis || Flashcards.cartasDisponiveis.length === 0) return;

  const key = e.key;

  // Espaço ou Enter: virar a carta
  if (key === ' ' || key === 'Enter') {
    e.preventDefault();
    if (!Flashcards.virada) {
      Flashcards.virar();
    }
    return;
  }

  // Teclas 1 a 4 para classificar no FSRS (quando carta virada)
  if (Flashcards.virada) {
    if (key === '1') { e.preventDefault(); Flashcards.avaliar(1); return; }
    if (key === '2') { e.preventDefault(); Flashcards.avaliar(2); return; }
    if (key === '3') { e.preventDefault(); Flashcards.avaliar(3); return; }
    if (key === '4') { e.preventDefault(); Flashcards.avaliar(4); return; }
  }

  // Atalhos utilitários
  if (key === 'r' || key === 'R' || key === 'a' || key === 'A') {
    e.preventDefault();
    Flashcards.pronunciar();
    return;
  }
  if (key === 'd' || key === 'D') {
    e.preventDefault();
    Flashcards.mostrarDica();
    return;
  }
  if (key === 'f' || key === 'F') {
    e.preventDefault();
    Flashcards.toggleFavorito();
    return;
  }
});


// Exposição global segura para navegadores e testes
if (typeof window !== 'undefined') window.Flashcards = Flashcards;
if (typeof globalThis !== 'undefined') globalThis.Flashcards = Flashcards;
if (typeof module !== 'undefined' && module.exports) module.exports = Flashcards;
