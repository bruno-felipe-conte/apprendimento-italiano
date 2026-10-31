// ============================================================
// flashcards.js — FSRS-4.5 spaced repetition engine
// Free Spaced Repetition Scheduler (Anki 23.10+ algorithm)
// ============================================================

// ── FSRS-4.5 core algorithm ───────────────────────────────────
const FSRS = {
  // Default weights from FSRS-4.5 paper (trained on 20M reviews)
  w: [0.4072, 1.1829, 3.1262, 15.4722, 7.2102, 0.5316, 1.0651, 0.0589,
      1.9395, 0.11,   0.29,   2.9898,  0.51,   0.34,   1.3436, 0.0762, 2.9898],

  // Power forgetting curve constants
  DECAY: -0.5,
  FACTOR: 19 / 81,
  TARGET_R: 0.9,

  // Mathematical Clamping Bounds per FSRS-4.5 Specification & Feature F7
  MIN_DIFFICULTY: 1.0,
  MAX_DIFFICULTY: 10.0,
  DEFAULT_DIFFICULTY: 5.0,
  MIN_STABILITY: 0.1,
  MAX_STABILITY: 36500.0, // 100 years
  DEFAULT_STABILITY: 2.0,
  MIN_INTERVAL: 1,
  MAX_INTERVAL: 36500,    // 100 years

  /**
   * Sanitiza e blinda um card FSRS contra valores nulos, NaN, Infinito e tipos inválidos.
   * Contrato M2 (PROJECT.md line 70):
   * FSRS.sanitizeCard(card: FSRSCardInput): FSRSCard
   * - Garante números finitos
   * - Dificuldade clampada em [1.0, 10.0]
   * - Estabilidade clampada em [0.1, 36500.0] (ou 0 para estado 'new')
   * - Reps e lapses inteiros >= 0
   * - Preserva histórico e metadados customizados
   */
  sanitizeCard(card) {
    if (!card || typeof card !== 'object') {
      return {
        state: 'new',
        difficulty: this.DEFAULT_DIFFICULTY,
        stability: 0,
        retrievability: 1.0,
        lapses: 0,
        reps: 0,
        lastReview: null,
        last_review: null,
        interval: 0,
        nextReview: null,
        next_review: null,
        history: []
      };
    }

    const validStates = ['new', 'learning', 'review', 'suspended'];
    const reps = (typeof card.reps === 'number' && Number.isInteger(card.reps) && card.reps >= 0)
      ? card.reps
      : (typeof card.repeticoes === 'number' && Number.isInteger(card.repeticoes) && card.repeticoes >= 0 ? card.repeticoes : 0);
    const lapses = (typeof card.lapses === 'number' && Number.isInteger(card.lapses) && card.lapses >= 0)
      ? card.lapses
      : 0;

    const state = validStates.includes(card.state)
      ? card.state
      : (reps > 0 ? 'review' : 'new');

    const difficulty = (typeof card.difficulty === 'number' && Number.isFinite(card.difficulty))
      ? Math.min(Math.max(card.difficulty, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;

    let stability;
    if (typeof card.stability === 'number' && Number.isFinite(card.stability)) {
      if (card.stability <= 0) {
        stability = (state === 'new') ? 0 : this.MIN_STABILITY;
      } else {
        stability = Math.min(Math.max(card.stability, this.MIN_STABILITY), this.MAX_STABILITY);
      }
    } else {
      stability = (state === 'new') ? 0 : this.DEFAULT_STABILITY;
    }

    const retrievability = (typeof card.retrievability === 'number' && Number.isFinite(card.retrievability))
      ? Math.min(Math.max(card.retrievability, 0.0), 1.0)
      : 1.0;

    let interval = 0;
    if (typeof card.interval === 'number' && Number.isFinite(card.interval) && card.interval >= 0) {
      interval = Math.min(Math.floor(card.interval), this.MAX_INTERVAL);
    } else if (state !== 'new') {
      interval = 1;
    }

    let lastReview = null;
    const rawLastReview = card.lastReview ?? card.last_review ?? card.ultima_revisao;
    if (typeof rawLastReview === 'number' && Number.isFinite(rawLastReview) && rawLastReview > 0) {
      lastReview = rawLastReview;
    } else if (typeof rawLastReview === 'string' && !isNaN(Date.parse(rawLastReview))) {
      lastReview = new Date(rawLastReview).getTime();
    } else if (rawLastReview instanceof Date) {
      lastReview = rawLastReview.getTime();
    }

    let nextReview = null;
    const rawNextReview = card.nextReview ?? card.next_review ?? card.proxima_revisao;
    if (typeof rawNextReview === 'number' && Number.isFinite(rawNextReview) && rawNextReview > 0) {
      nextReview = rawNextReview;
    } else if (typeof rawNextReview === 'string' && !isNaN(Date.parse(rawNextReview))) {
      nextReview = new Date(rawNextReview).getTime();
    } else if (rawNextReview instanceof Date) {
      nextReview = rawNextReview.getTime();
    }

    const history = Array.isArray(card.history) ? card.history : [];

    return {
      ...card,
      state,
      difficulty,
      stability,
      retrievability,
      lapses,
      reps,
      interval,
      lastReview,
      last_review: lastReview,
      nextReview,
      next_review: nextReview,
      history
    };
  },

  // Retrievability given elapsed time t (days) and stability S
  // Resiliente a clock skew (t <= 0) e valores não finitos
  retrievability(t, s) {
    if (!Number.isFinite(s) || s <= 0 || !Number.isFinite(t) || t <= 0) return 1.0;
    const r = Math.pow(1 + this.FACTOR * t / s, this.DECAY);
    if (!Number.isFinite(r)) return 1.0;
    return Math.min(Math.max(r, 0.0), 1.0);
  },

  // Days until retrievability drops to TARGET_R (clamped [1, 36500])
  nextInterval(s) {
    if (!Number.isFinite(s) || s <= 0) return this.MIN_INTERVAL;
    const safeS = Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY);
    const t = safeS * (Math.pow(this.TARGET_R, 1 / this.DECAY) - 1) / this.FACTOR;
    if (!Number.isFinite(t)) return this.MIN_INTERVAL;
    return Math.min(Math.max(Math.round(t), this.MIN_INTERVAL), this.MAX_INTERVAL);
  },

  // Initial stability after first review (rating 1-4)
  initStability(rating) {
    const r = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    const s = this.w[r - 1];
    if (!Number.isFinite(s) || s <= 0) return this.MIN_STABILITY;
    return Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY);
  },

  // Initial difficulty after first review (rating 1-4)
  initDifficulty(rating) {
    const r = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    const d = this.w[4] - Math.exp(this.w[5] * (r - 1)) + 1;
    if (!Number.isFinite(d)) return this.DEFAULT_DIFFICULTY;
    return Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY);
  },

  // Difficulty after subsequent reviews (with mean reversion toward Easy baseline)
  nextDifficulty(d, rating) {
    const safeD = (typeof d === 'number' && Number.isFinite(d))
      ? Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;
    const r = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    const d0easy = this.initDifficulty(4); // ~3.28 — Easy baseline
    const delta  = -this.w[6] * (r - 3);
    const raw    = safeD + delta;
    // w[7]=0.0589 pulls ~6% toward the easy baseline each review
    const next   = this.w[7] * d0easy + (1 - this.w[7]) * raw;
    if (!Number.isFinite(next)) return this.DEFAULT_DIFFICULTY;
    return Math.min(Math.max(next, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY);
  },

  // Stability after a successful recall (rating 2/3/4)
  nextRecallStability(d, s, r, rating) {
    const rVal = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    if (!Number.isFinite(s) || s <= 0) return this.initStability(rVal);

    const safeD = (typeof d === 'number' && Number.isFinite(d))
      ? Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;
    const safeS = Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY);
    const safeR = (typeof r === 'number' && Number.isFinite(r))
      ? Math.min(Math.max(r, 0.0), 1.0)
      : 1.0;

    const hardPenalty = rVal === 2 ? this.w[15] : 1;
    const easyBonus   = rVal === 4 ? this.w[16] : 1;
    const increment   = Math.exp(this.w[8]) *
                        (11 - safeD) *
                        Math.pow(safeS, -this.w[9]) *
                        (Math.exp(this.w[10] * (1 - safeR)) - 1) *
                        hardPenalty * easyBonus;

    if (!Number.isFinite(increment) || increment < 0) {
      return safeS;
    }
    const newS = safeS * (increment + 1);
    if (!Number.isFinite(newS)) return this.MAX_STABILITY;
    return Math.min(Math.max(newS, this.MIN_STABILITY), this.MAX_STABILITY);
  },

  // Stability after forgetting (rating 1 — Again)
  nextForgetStability(d, s, r) {
    const safeD = (typeof d === 'number' && Number.isFinite(d))
      ? Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;
    const safeS = (typeof s === 'number' && Number.isFinite(s) && s > 0)
      ? Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY)
      : this.DEFAULT_STABILITY;
    const safeR = (typeof r === 'number' && Number.isFinite(r))
      ? Math.min(Math.max(r, 0.0), 1.0)
      : 1.0;

    const res = this.w[11] *
                Math.pow(safeD, -this.w[12]) *
                (Math.pow(safeS + 1, this.w[13]) - 1) *
                Math.exp(this.w[14] * (1 - safeR));

    if (!Number.isFinite(res)) return this.MIN_STABILITY;
    return Math.min(Math.max(res, this.MIN_STABILITY), this.MAX_STABILITY);
  },

  // ── Review a card, return updated card state ───────────────
  // Feature F7 & F8: Sanitização prévia + monotonicidade temporal contra clock skew
  review(card, rating) {
    const safeCard = this.sanitizeCard(card);
    const rVal = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;

    const now = Date.now();
    // Clock skew handling (F8): se lastReview estiver no futuro ou nulo, tDays é estritamente 0
    const lastRev = safeCard.lastReview ?? safeCard.last_review;
    const tDays = (lastRev && lastRev < now)
      ? (now - lastRev) / 86400000
      : 0;

    const d = safeCard.difficulty;
    const s = safeCard.stability;
    const r = (s > 0) ? this.retrievability(tDays, s) : 1.0;

    let newD, newS;

    if (safeCard.state === 'new') {
      newD = this.initDifficulty(rVal);
      newS = this.initStability(rVal);
    } else if (rVal === 1) {
      // Again — forgot
      safeCard.lapses++;
      newD = this.nextDifficulty(d, rVal);
      newS = this.nextForgetStability(d, s, r);
    } else {
      // Hard / Good / Easy — remembered
      newD = this.nextDifficulty(d, rVal);
      newS = this.nextRecallStability(d, s, r, rVal);
    }

    safeCard.reps++;
    const newState    = rVal === 1 ? 'learning' : 'review';
    const intervalDay = rVal === 1 ? 1 : this.nextInterval(newS);
    const previousHistory = Array.isArray(safeCard.history) ? safeCard.history : [];
    const reviewRecord = {
      timestamp: now,
      rating: rVal,
      stabilityBefore: Number((Number.isFinite(s) ? s : 1.0).toFixed(2)),
      stabilityAfter: Number((Number.isFinite(newS) ? newS : 1.0).toFixed(2)),
      retrievabilityBefore: Number((Number.isFinite(r) ? r : 1.0).toFixed(3)),
      targetPeak: rVal === 1 ? 0.85 : 1.0,
      intervalDays: intervalDay
    };

    return {
      ...safeCard,
      state:          newState,
      difficulty:     newD,
      stability:      newS,
      retrievability: r,
      lapses:         safeCard.lapses,
      reps:           safeCard.reps,
      lastReview:     now,
      last_review:    now,
      interval:       intervalDay,
      nextReview:     now + intervalDay * 86400000,
      next_review:    now + intervalDay * 86400000,
      history:        [...previousHistory, reviewRecord]
    };
  },

  // ── Preview intervals for each rating without committing ───
  previewIntervals(card) {
    const safeCard = this.sanitizeCard(card);
    const now   = Date.now();
    const lastRev = safeCard.lastReview ?? safeCard.last_review;
    const tDays = (lastRev && lastRev < now)
      ? (now - lastRev) / 86400000
      : 0;
    const { difficulty: d, stability: s, state } = safeCard;
    const r = (s > 0) ? this.retrievability(tDays, s) : 1.0;

    return [1, 2, 3, 4].map(rating => {
      if (state === 'new') {
        return rating === 1 ? 1 : this.nextInterval(this.initStability(rating));
      }
      if (rating === 1) return 1;
      const newS = this.nextRecallStability(d, s, r, rating);
      return this.nextInterval(newS);
    });
  },

  // ── Migrate a legacy SM-2 record to FSRS schema ───────────
  migrateSM2(sm2) {
    if (!sm2 || typeof sm2 !== 'object') {
      return this.sanitizeCard(null);
    }
    const rawInterval = typeof sm2.intervalo === 'number' && Number.isFinite(sm2.intervalo)
      ? sm2.intervalo
      : (typeof sm2.interval === 'number' && Number.isFinite(sm2.interval) ? sm2.interval : 1);
    const s = Math.min(Math.max(rawInterval, this.MIN_STABILITY), this.MAX_STABILITY);

    const rawEase = typeof sm2.facilidade === 'number' && Number.isFinite(sm2.facilidade)
      ? sm2.facilidade
      : (typeof sm2.ease_factor === 'number' && Number.isFinite(sm2.ease_factor)
        ? sm2.ease_factor
        : (typeof sm2.factor === 'number' && Number.isFinite(sm2.factor) ? sm2.factor : 2.5));
    const d = Math.min(Math.max(10 - (rawEase - 1.3) * (9 / 1.7), this.MIN_DIFFICULTY), this.MAX_DIFFICULTY);

    const reps = (Number.isInteger(sm2.repeticoes) && sm2.repeticoes >= 0)
      ? sm2.repeticoes
      : (Number.isInteger(sm2.repetitions) && sm2.repetitions >= 0
        ? sm2.repetitions
        : (Number.isInteger(sm2.reps) && sm2.reps >= 0 ? sm2.reps : 0));

    const lapses = (Number.isInteger(sm2.lapses) && sm2.lapses >= 0) ? sm2.lapses : 0;
    const lastReview = sm2.ultima_revisao || sm2.lastReview || sm2.last_review || null;
    const nextReview = sm2.proxima_revisao || sm2.nextReview || sm2.next_review || null;

    return this.sanitizeCard({
      ...sm2,
      state:          reps > 0 ? 'review' : 'new',
      difficulty:     Number(d.toFixed(2)),
      stability:      Number(s.toFixed(2)),
      retrievability: 1.0,
      lapses,
      reps,
      lastReview,
      last_review:    lastReview,
      interval:       s >= 1 ? Math.round(s) : 1,
      nextReview,
      next_review:    nextReview
    });
  },

  // Format interval as human-readable string
  formatInterval(days) {
    if (!Number.isFinite(days) || days <= 0) return 'hoje';
    const d = Math.round(days);
    if (d === 1) return '1 dia';
    if (d < 31) return `${d} dias`;
    const months = Math.round(d / 30);
    return months === 1 ? '1 mês' : `${months} meses`;
  },
};


// ── Flashcard UI module ────────────────────────────────────────
const Flashcards = {
  _bloqueioAvaliacao: false,
  _cardEmAvaliacaoId: null,
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
  _sessaoRevisoes:   0,
  revisoesContinuas: 0,
  gravando:          false,
  _recognition:      null,
  _swipeInitialized: false,
  _swipeStartX:      0,
  _swipeStartY:      0,
  abaOrigem:         'templos', // 'templos' | 'especiais'
  gavetaAberta:      false,
  seletorRecolhido:  true,

  // ── Smart Retractable Drawer & Selector Bar ─────────────────
  toggleGaveta(forcarEstado) {
    if (typeof forcarEstado === 'boolean') {
      this.gavetaAberta = forcarEstado;
    } else {
      this.gavetaAberta = !this.gavetaAberta;
    }
    this.seletorRecolhido = !this.gavetaAberta;
    this._sincronizarGaveta();
    this.atualizarEbbinghaus();
  },

  recolherGaveta() {
    this.toggleGaveta(false);
  },

  abrirGaveta() {
    this.toggleGaveta(true);
  },

  // Alias para retrocompatibilidade
  toggleSeletor(forcarEstado) {
    if (typeof forcarEstado === 'boolean') {
      this.toggleGaveta(!forcarEstado);
    } else {
      this.toggleGaveta();
    }
  },

  _sincronizarGaveta() {
    const drawer = document.getElementById('fc-seletor-drawer');
    const btnToggle = document.getElementById('fc-compact-toggle-btn');
    if (drawer) {
      drawer.classList.toggle('recolhido', !this.gavetaAberta);
    }
    if (btnToggle) {
      btnToggle.setAttribute('aria-expanded', String(this.gavetaAberta));
      btnToggle.innerHTML = this.gavetaAberta
        ? '<span>Fechar</span><span class="fc-compact-chevron" id="fc-compact-chevron">▴</span>'
        : '<span>Baralhos</span><span class="fc-compact-chevron" id="fc-compact-chevron">▾</span>';
    }
    this._sincronizarBarraCompacta();
  },

  _sincronizarBarraCompacta() {
    const bar = document.getElementById('fc-compact-bar');
    if (!bar) return;

    // A barra compacta fica sempre disponível no topo
    bar.style.display = 'flex';

    // Label de origem (Templo, Baralho Especial ou Revisão Geral)
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
      } else {
        labelOrigem = '🏛️ Selecione um Tempio';
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
      if (this.cartasDisponiveis && this.cartasDisponiveis.length > 0 && this.indiceAtual < this.cartasDisponiveis.length) {
        elCount.textContent = `${this.indiceAtual + 1}/${this.cartasDisponiveis.length}`;
      } else if (this.cartasDisponiveis && this.cartasDisponiveis.length > 0) {
        elCount.textContent = `${this.cartasDisponiveis.length}/${this.cartasDisponiveis.length}`;
      } else {
        elCount.textContent = '0 cartas';
      }
    }

    // Atualiza estado do botão se não sincronizado
    const btnToggle = document.getElementById('fc-compact-toggle-btn');
    if (btnToggle && !btnToggle.hasAttribute('aria-expanded')) {
      btnToggle.setAttribute('aria-expanded', String(this.gavetaAberta));
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
    this.recolherGaveta(); // Recolhe a gaveta ao selecionar baralho especial
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
    this.recolherGaveta(); // Recolhe a gaveta ao selecionar templo
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
      this.abrirGaveta();
      this.mostrarVazio();
    } else {
      this.recolherGaveta();
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
    this._bloqueioAvaliacao = false;
    this._cardEmAvaliacaoId = null;

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
    if (cardEl) { cardEl.classList.remove('virado'); cardEl.setAttribute('aria-expanded', 'false'); cardEl.style.display = ''; }
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
    this.atualizarEbbinghaus();
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
      const fsrs = (App.estado && App.estado.flashcardData) ? App.estado.flashcardData[this.cartaAtual.id] : null;
      const lr = fsrs ? (fsrs.lastReview ?? fsrs.last_review) : null;
      if (fsrs && fsrs.stability > 0 && lr) {
        const tDays = Math.max(0, (Date.now() - lr) / 86400000);
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

  // ── Atualiza a Curva de Esquecimento de Ebbinghaus (FSRS) ──
  atualizarEbbinghaus() {
    const container = document.getElementById('ebbinghaus-container');
    if (!container) return;

    container.style.display = 'block';
    const renderFn = (typeof renderEbbinghausCurve === 'function')
      ? renderEbbinghausCurve
      : (typeof window !== 'undefined' && typeof window.renderEbbinghausCurve === 'function')
        ? window.renderEbbinghausCurve
        : (typeof window !== 'undefined' && window.Ebbinghaus && typeof window.Ebbinghaus.renderEbbinghausCurve === 'function')
          ? window.Ebbinghaus.renderEbbinghausCurve
          : (typeof globalThis !== 'undefined' && globalThis.Ebbinghaus && typeof globalThis.Ebbinghaus.renderEbbinghausCurve === 'function')
            ? globalThis.Ebbinghaus.renderEbbinghausCurve
            : null;

    if (!renderFn) {
      console.warn('[Flashcards] renderEbbinghausCurve não encontrado');
      return;
    }

    const cardDataMap = (typeof App !== 'undefined' && App.estado && App.estado.flashcardData) ? App.estado.flashcardData : {};
    let fsrsCard = (this.cartaAtual && cardDataMap[this.cartaAtual.id])
      ? cardDataMap[this.cartaAtual.id]
      : (this.cartaAtual ? { id: this.cartaAtual.id, stability: 1.0, difficulty: 5.0, state: 'new' } : null);
    let allCards = Object.values(cardDataMap);

    // Se ainda não houver revisões salvas ou carta em foco, gera projeção referencial FSRS padrão
    if (allCards.length === 0) {
      const baselineCard = fsrsCard || { id: 'baseline', stability: 1.5, difficulty: 5.0, state: 'new' };
      allCards = [baselineCard];
      if (!fsrsCard) fsrsCard = baselineCard;
    }

    renderFn(container, allCards, fsrsCard || null, {
      desiredRetention: 0.90,
      locale: (typeof I18n !== 'undefined' ? I18n.currentLang : 'it') || 'it',
      curveMode: 'fsrs-power'
    });
  },

  // ── Flip card to reveal answer ─────────────────────────────
  virar() {
    if (this.virada || !this.cartaAtual) return;
    this.virada = true;
    if (typeof SomFeedback !== 'undefined') SomFeedback.virar();

    const cardEl = document.getElementById('flashcard');
    if (cardEl) { cardEl.classList.add('virado'); cardEl.setAttribute('aria-expanded', 'true'); }
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
      if (elDica) elDica.textContent = `💡 ${hint}`;
      if (btnDica) btnDica.title = 'Ver dica (revelar)';
    } else {
      // Level 3: just flip the card.
      // virar() will call _aplicarPenalidadeDica() because dicaUsada===true,
      // so we must NOT call it again here to avoid double application.
      if (elDica) elDica.textContent = '💡 Revelado';
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
    // Reentrancy guard: block multiple evaluations of the same card
    if (this._bloqueioAvaliacao && this._cardEmAvaliacaoId === this.cartaAtual.id) return;
    this._bloqueioAvaliacao = true;
    this._cardEmAvaliacaoId = this.cartaAtual.id;

    // Immediately disable rating buttons to prevent click bounce
    const botoesAvaliar = document.querySelectorAll(
      '.fc-btn-fsrs, .fc-action-btn, #btn-again, #btn-hard, #btn-good, #btn-easy, .btn-rating'
    );
    botoesAvaliar.forEach(b => { if (b) b.disabled = true; });

    try {
      const carta = this.cartaAtual;

      let fsrs = App.estado.flashcardData[carta.id];
      if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
        fsrs = FSRS.migrateSM2(fsrs);
      }
      if (!fsrs) {
        fsrs = { state: 'new', difficulty: 5, stability: 0, retrievability: 1,
                 lapses: 0, reps: 0, lastReview: null, last_review: null, interval: 0, nextReview: null };
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

      // F20: Pacing cognitivo e micro-pausa a cada 20 revisões consecutivas
      this._sessaoRevisoes = (this._sessaoRevisoes || 0) + 1;
      this.revisoesContinuas = this._sessaoRevisoes;
      if (this._sessaoRevisoes % 20 === 0 && typeof App !== 'undefined' && App.notificar) {
        App.notificar('🧠 Ottimo lavoro! Fai una pausa di 1 minuto para consolidare la memoria.', 'info');
      }

      // Check achievements off the critical path to avoid jank on card transition
      if (typeof Conquistas !== 'undefined') {
        if (typeof requestIdleCallback === 'function') requestIdleCallback(() => Conquistas.verificar());
        else setTimeout(() => Conquistas.verificar(), 300);
      }

      // ── Animação imediata da Curva Ebbinghaus (Seta subindo até 100% ou 85%) ──
      this.atualizarEbbinghaus();

      // Micro-pausa de 650ms para absorção cognitiva visual da retenção restaurada
      setTimeout(() => {
        try {
          this.proxima();
        } finally {
          this._bloqueioAvaliacao = false;
          this._cardEmAvaliacaoId = null;
          botoesAvaliar.forEach(b => { if (b) b.disabled = false; });
        }
      }, 650);
    } catch (err) {
      console.error('[FSRS] avaliar() error:', err);
      App.notificar('notif_fc_erro_resposta', 'erro');
      try {
        this.proxima(); // advance anyway so user isn't stuck
      } finally {
        this._bloqueioAvaliacao = false;
        this._cardEmAvaliacaoId = null;
        botoesAvaliar.forEach(b => { if (b) b.disabled = false; });
      }
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
    this._bloqueioAvaliacao = false;
    this._cardEmAvaliacaoId = null;
    this.abrirGaveta();
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
    this.atualizarEbbinghaus();
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
    this.recolherGaveta();
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
    this.recolherGaveta();
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
    this.recolherGaveta();
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
    this.recolherGaveta();

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
    this._sincronizarGaveta();
    this.atualizarEbbinghaus();
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

if (typeof document !== 'undefined') {
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
    Flashcards.atualizarEbbinghaus();
  });
}

// ── Atalhos de Teclado no Flashcards ────────────────────────
if (typeof window !== 'undefined') {
  window.addEventListener('keydown', (e) => {
    if (typeof Flashcards !== 'undefined' && Flashcards._bloqueioAvaliacao) return;
    const tag = (e.target.tagName || '').toUpperCase();
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || e.target.isContentEditable) return;

    if (typeof document === 'undefined') return;
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
    if (key === '1') { e.preventDefault(); e.stopImmediatePropagation(); Flashcards.avaliar(1); return; }
    if (key === '2') { e.preventDefault(); e.stopImmediatePropagation(); Flashcards.avaliar(2); return; }
    if (key === '3') { e.preventDefault(); e.stopImmediatePropagation(); Flashcards.avaliar(3); return; }
    if (key === '4') { e.preventDefault(); e.stopImmediatePropagation(); Flashcards.avaliar(4); return; }
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
}


// Exposição global segura para navegadores e testes
Flashcards.FSRS = FSRS;

if (typeof window !== 'undefined') {
  window.Flashcards = Flashcards;
  window.FSRS = FSRS;
}
if (typeof globalThis !== 'undefined') {
  globalThis.Flashcards = Flashcards;
  globalThis.FSRS = FSRS;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Flashcards;
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      if (typeof Flashcards !== 'undefined' && typeof Flashcards.atualizarEbbinghaus === 'function') {
        Flashcards.atualizarEbbinghaus();
      }
    });
  } else {
    setTimeout(() => {
      if (typeof Flashcards !== 'undefined' && typeof Flashcards.atualizarEbbinghaus === 'function') {
        Flashcards.atualizarEbbinghaus();
      }
    }, 50);
  }
}
