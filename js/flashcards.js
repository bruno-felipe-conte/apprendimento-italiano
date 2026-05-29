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
  modoReverso:      false,
  sessaoStats:      null,

  // ── Initialize for a specific temple ──────────────────────
  init(templo) {
    if (!templo || isNaN(templo)) return;
    if (!Progressao.temploDesbloqueado(templo)) {
      App.notificar('Tempio não desbloqueado ainda!', 'erro');
      return;
    }
    if (!App.estado.templosData[templo]) {
      App.notificar('Vocabulário deste tempio não carregado.', 'erro');
      return;
    }
    this.temploAtual     = templo;
    this.praticandoTodas = false;
    this.sessaoStats     = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
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
      this.mostrarVazio();
    } else {
      this.mostrarCarta();
    }
  },

  // ── Load and sort cards due for review ────────────────────
  carregarCartas() {
    const data = App.estado.templosData[this.temploAtual];
    if (!data || !data.palavras) { this.cartasDisponiveis = []; return; }

    const agora   = Date.now();
    const novas   = [];
    const devidas = [];

    data.palavras.forEach(palavra => {
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

  // ── Render current card ────────────────────────────────────
  mostrarCarta() {
    if (this.indiceAtual >= this.cartasDisponiveis.length) {
      this.mostrarVazio();
      return;
    }

    this.cartaAtual = this.cartasDisponiveis[this.indiceAtual];
    this.virada     = false;

    const cardEl = document.getElementById('flashcard');
    if (cardEl) { cardEl.classList.remove('virado'); cardEl.style.display = ''; }

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
    if (elDica) elDica.textContent = 'Clique para revelar';

    // Apply/remove reverse mode class for CSS theming
    const cardEl2 = document.getElementById('flashcard');
    if (cardEl2) cardEl2.classList.toggle('modo-reverso', this.modoReverso);

    if (this.modoReverso) {
      // PT → IT: front shows Portuguese, back reveals Italian + IPA
      if (elIt)  elIt.textContent  = this.cartaAtual.portugues || '—';
      if (elCat) elCat.textContent = this.cartaAtual.categoria || '';
      if (elTrad) elTrad.textContent = this.cartaAtual.italiano || '—';
    } else {
      // IT → PT (normal): front shows Italian, back reveals Portuguese
      if (elIt)  elIt.textContent  = this.cartaAtual.italiano || '—';
      if (elCat) elCat.textContent = this.cartaAtual.categoria || '';
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

    this.atualizarContador();

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
        rStr        = ` · R ${Math.round(r * 100)}%`;
      }
    }

    const novosCount   = this.cartasDisponiveis.filter(c => !App.estado.flashcardData[c.id] || App.estado.flashcardData[c.id].state === 'new').length;
    const revisaoCount = total - novosCount;
    const partes       = [];
    if (novosCount   > 0) partes.push(`${novosCount} novas`);
    if (revisaoCount > 0) partes.push(`${revisaoCount} revisão`);

    elInfo.innerHTML = `<strong>${atual}</strong> / ${total}${partes.length ? ' &nbsp;·&nbsp; ' + partes.join(', ') : ''}${rStr}`;
  },

  // ── Flip card to reveal answer ─────────────────────────────
  virar() {
    if (this.virada || !this.cartaAtual) return;
    this.virada = true;

    const cardEl = document.getElementById('flashcard');
    if (cardEl) cardEl.classList.add('virado');

    // Show action buttons with interval previews
    const actions = document.getElementById('card-actions');
    if (actions) {
      actions.style.display = 'grid';
      this._atualizarBotoesIntervalo();
    }
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

      // XP: Again=0, Hard=5, Good=10, Easy=15
      const xpMap = [0, 0, 5, 10, 15];
      const xpGanho = xpMap[rating] || 0;
      if (xpGanho > 0 && App.estado.progresso) {
        App.estado.progresso.xp += xpGanho;
        App.salvarProgresso();
        App.atualizarStats();
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

      this.proxima();
    } catch (err) {
      console.error('[FSRS] avaliar() error:', err);
      App.notificar('Erro ao registrar resposta. Tente novamente.', 'erro');
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
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    const vazio   = document.getElementById('flashcard-vazio');
    const resumo  = document.getElementById('flashcard-resumo');
    const info    = document.getElementById('card-info');

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
    else if (pct >= 60) { emoji = '👏'; titulo = 'Muito bom!'; }
    else if (pct < 40) { emoji = '💪'; titulo = 'Continua a praticare!'; }

    // Next due card
    let proxLabel = 'Sem agendamento';
    if (this.temploAtual) {
      const data = App.estado.templosData[this.temploAtual];
      if (data && data.palavras) {
        const agora = Date.now();
        const proximas = data.palavras
          .map(p => App.estado.flashcardData[p.id])
          .filter(f => f && f.nextReview && f.nextReview > agora)
          .map(f => f.nextReview)
          .sort((a, b) => a - b);
        if (proximas.length > 0) {
          const diffMs = proximas[0] - agora;
          const diffH  = Math.round(diffMs / 3600000);
          const diffD  = Math.round(diffMs / 86400000);
          proxLabel = diffD >= 1 ? `em ${diffD} dia${diffD > 1 ? 's' : ''}` : `em ${diffH}h`;
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
            <span class="resumo-lab">cartas</span>
          </div>
          <div class="resumo-stat">
            <span class="resumo-num">${pct}%</span>
            <span class="resumo-lab">acertos</span>
          </div>
          ${s.xp > 0 ? `<div class="resumo-stat"><span class="resumo-num">+${s.xp}</span><span class="resumo-lab">XP</span></div>` : ''}
        </div>
        <div class="resumo-ratings">
          ${s.again > 0 ? `<span class="rr rr-again">❌ ${s.again}</span>` : ''}
          ${s.hard  > 0 ? `<span class="rr rr-hard">⚡ ${s.hard}</span>` : ''}
          ${s.good  > 0 ? `<span class="rr rr-good">✅ ${s.good}</span>` : ''}
          ${s.easy  > 0 ? `<span class="rr rr-easy">⭐ ${s.easy}</span>` : ''}
        </div>
        ${novCount > 0 ? `<p class="resumo-novas">🌱 ${novCount} palavra${novCount > 1 ? 's' : ''} nova${novCount > 1 ? 's' : ''} aprendida${novCount > 1 ? 's' : ''}!</p>` : ''}
        <p class="resumo-proxima">⏰ Próxima revisão: <strong>${proxLabel}</strong></p>
        <div class="resumo-acoes">
          <button class="btn-primario" onclick="Flashcards.praticaTodas()">🔁 Praticar todas</button>
        </div>
      </div>
    `;
    resumo.style.display = 'block';
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
      App.notificar('Nenhuma palavra difícil encontrada! 🎉', 'successo');
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
    App.notificar(`📚 ${dificeis.length} palavras difíceis para revisar`, 'alerta');
    this.mostrarCarta();
  },

  // ── Toggle reverse mode (PT → IT) ─────────────────────────
  toggleReverso() {
    this.modoReverso = !this.modoReverso;
    const btn = document.getElementById('btn-reverso');
    if (btn) btn.classList.toggle('ativo', this.modoReverso);
    if (this.cartaAtual) this.mostrarCarta();
  },

  // ── Practice all cards regardless of schedule ─────────────
  praticaTodas() {
    const data = App.estado.templosData[this.temploAtual];
    if (!data || !data.palavras || data.palavras.length === 0) return;
    this.praticandoTodas  = true;
    this.sessaoStats      = { again: 0, hard: 0, good: 0, easy: 0, xp: 0, novas: [] };
    this.cartasDisponiveis = [...data.palavras];
    this.indiceAtual      = 0;
    this.virada           = false;

    const vazio   = document.getElementById('flashcard-vazio');
    const cardEl  = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display   = 'none';
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

  // ── Populate temple selector ──────────────────────────────
  atualizarSelectTemplo() {
    const sel = document.getElementById('flashcard-templo-select');
    if (!sel) return;
    const anterior = sel.value;
    sel.innerHTML  = '<option value="">-- Seleziona tempio --</option>';
    const desbloqueados = App.estado.progresso ? App.estado.progresso.templos_desbloqueados : [1];
    desbloqueados.forEach(num => {
      const data = App.estado.templosData[num];
      if (!data) return;
      const opt        = document.createElement('option');
      opt.value        = num;
      const nomeTemplo = data.nome || (App.TEMPLO_NOMES && App.TEMPLO_NOMES[num]) || `Tempio ${num}`;
      opt.textContent  = `${num}. ${nomeTemplo} (${data.cidade})`;
      sel.appendChild(opt);
    });
    if (anterior && sel.querySelector(`option[value="${anterior}"]`)) {
      sel.value = anterior;
    }
  },
};
