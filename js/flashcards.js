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

  // ── Initialize for a specific temple ──────────────────────
  init(templo) {
    if (!templo || isNaN(templo)) return;
    if (!Progressao.temploDesbloqueado(templo)) {
      App.notificar('notif_fc_bloqueado', 'erro');
      return;
    }
    if (!App.estado.templosData[templo]) {
      App.notificar('notif_fc_vocab_nao_carregado', 'erro');
      return;
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
      this.mostrarVazio();
    } else {
      this.mostrarCarta();
    }
    
    // Check speech API support
    const btnGravar = document.getElementById('btn-gravar');
    if (btnGravar) {
      const suporta = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
      btnGravar.style.display = suporta ? '' : 'none';
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

    this.cartaAtual  = this.cartasDisponiveis[this.indiceAtual];
    this.virada      = false;
    this.nivelDica   = 0;
    this.dicaUsada   = false;

    // Reset dica button appearance
    const btnDica = document.getElementById('btn-dica');
    if (btnDica) { btnDica.classList.remove('ativo'); btnDica.title = 'Ver dica (nível 1)'; }

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

    this.atualizarContador();
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
        rStr        = ` · R ${Math.round(r * 100)}%`;
      }
    }

    const novosCount   = this.cartasDisponiveis.filter(c => !App.estado.flashcardData[c.id] || App.estado.flashcardData[c.id].state === 'new').length;
    const revisaoCount = total - novosCount;
    const partes       = [];
    if (novosCount   > 0) partes.push(`${novosCount} ${I18n.t('fc_novas')}`);
    if (revisaoCount > 0) partes.push(`${revisaoCount} ${I18n.t('fc_revisao')}`);

    elInfo.innerHTML = `<strong>${atual}</strong> / ${total}${partes.length ? ' &nbsp;·&nbsp; ' + partes.join(', ') : ''}${rStr}`;
  },

  // ── Flip card to reveal answer ─────────────────────────────
  virar() {
    if (this.virada || !this.cartaAtual) return;
    this.virada = true;
    if (typeof SomFeedback !== 'undefined') SomFeedback.virar();

    const cardEl = document.getElementById('flashcard');
    if (cardEl) cardEl.classList.add('virado');

    // Show action buttons with interval previews
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

      // Check achievements after each review
      if (typeof Conquistas !== 'undefined') Conquistas.verificar();

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
    else if (pct >= 60) { emoji = '👏'; titulo = I18n.t('fc_resumo_muito_bom'); }
    else if (pct < 40) { emoji = '💪'; titulo = I18n.t('fc_resumo_continua'); }

    // Next due card
    let proxLabel = I18n.t('fc_resumo_sem_agendamento');
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

  // ── Toggle favorite for current card ─────────────────────
  toggleFavorito() {
    if (!this.cartaAtual) return;
    const adicionado = App.toggleFavorito(this.cartaAtual.id);
    const btn = document.getElementById('btn-favorito');
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
    App.notificar(I18n.t('notif_fc_dificeis_revisar').replace('{n}', dificeis.length), 'alerta');
    this.mostrarCarta();
  },

  // ── Mode toggles (mutually exclusive) ────────────────────
  _limparModos() {
    this.modoReverso  = false;
    this.modoContexto = false;
    this.modoEscuta   = false;
    ['btn-reverso','btn-contexto','btn-escuta'].forEach(id => {
      const b = document.getElementById(id);
      if (b) b.classList.remove('ativo');
    });
  },

  toggleReverso() {
    const novoValor = !this.modoReverso;
    this._limparModos();
    this.modoReverso = novoValor;
    const btn = document.getElementById('btn-reverso');
    if (btn) btn.classList.toggle('ativo', this.modoReverso);
    if (this.cartaAtual) this.mostrarCarta();
  },

  toggleContexto() {
    const novoValor = !this.modoContexto;
    this._limparModos();
    this.modoContexto = novoValor;
    const btn = document.getElementById('btn-contexto');
    if (btn) btn.classList.toggle('ativo', this.modoContexto);
    if (this.cartaAtual) this.mostrarCarta();
  },

  toggleEscuta() {
    const novoValor = !this.modoEscuta;
    this._limparModos();
    this.modoEscuta = novoValor;
    const btn = document.getElementById('btn-escuta');
    if (btn) btn.classList.toggle('ativo', this.modoEscuta);
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
    App.notificar(`🌍 ${total_devidas} carta${total_devidas !== 1 ? 's' : ''} em revisão + ${novasLimitadas.length} novas`, 'alerta');
    this.mostrarCarta();
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

  toggleGravar() {
    if (!this.cartaAtual) return;
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { App.notificar('notif_fc_sem_voz', 'alerta'); return; }
    
    if (this.gravando) {
      if (this._recognition) this._recognition.stop();
      this.gravando = false;
      return;
    }
    
    this.gravando = true;
    const btnGravar = document.getElementById('btn-gravar');
    if (btnGravar) { btnGravar.textContent = I18n.t('fc_gravar_parar'); btnGravar.style.background = '#C0392B'; btnGravar.style.color = '#fff'; }
    
    this._recognition = this._iniciarReconhecimento();
    if (!this._recognition) return;
    
    this._recognition.onresult = (e) => {
      const texto = e.results[0][0].transcript.toLowerCase();
      const alvo = (this.cartaAtual.italiano || '').toLowerCase();
      
      const textoNormalize = texto.replace(/[.,!?;:]/g, '').trim();
      const alvoNormalize = alvo.replace(/[.,!?;:]/g, '').trim();
      
      const reconheceu = textoNormalize.includes(alvoNormalize) || alvoNormalize.includes(textoNormalize.split(' ')[0]);
      this._mostrarFeedbackPronuncia(texto, reconheceu);
    };
    this._recognition.onerror = () => { App.notificar('notif_fc_nao_ouviu', 'alerta'); };
    this._recognition.onend = () => {
      this.gravando = false;
      if (btnGravar) { btnGravar.textContent = I18n.t('fc_gravar_imitar'); btnGravar.style.background = ''; btnGravar.style.color = ''; }
    };
    this._recognition.start();
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
