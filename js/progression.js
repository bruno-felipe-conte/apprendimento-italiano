// ============================================================
// progression.js — XP levels, temple unlocks, mastery
// ============================================================

const Progressao = {
  // Cumulative XP required to reach each level index
  // Index 0 = start of level 1 (0 XP), index 1 = start of level 2 (500 XP), etc.
  NIVEL_XP: [
    0,       // level 1 starts at 0
    500,     // level 2
    800,     // level 3
    1200,    // level 4
    1800,    // level 5
    2600,    // level 6
    3500,    // level 7
    4500,    // level 8
    6000,    // level 9
    8000,    // level 10
    10000,   // level 11
    13000,   // level 12
    16000,   // level 13
    20000,   // level 14
    25000,   // level 15
    30000,   // level 16
    37000,   // level 17
    45000,   // level 18
    55000,   // level 19
    65000,   // level 20
    80000    // level 21
  ],

  // Minimum level required to unlock each temple
  TEMPLO_NIVEL: { 1: 1, 2: 3, 3: 6, 4: 10, 5: 15, 6: 21, 7: 28, 8: 36, 9: 45, 10: 55 },

  // ── XP threshold for level N (1-based) ────────────────────
  // Returns the cumulative XP needed to reach the START of level N
  xpParaNivel(n) {
    if (n <= 1) return 0;
    const idx = n - 1; // level 2 is at index 1
    if (idx < this.NIVEL_XP.length) return this.NIVEL_XP[idx];
    // Beyond table: extrapolate
    return this.NIVEL_XP[this.NIVEL_XP.length - 1] + (n - this.NIVEL_XP.length) * 5000;
  },

  // ── Gain XP and trigger cascading checks ──────────────────
  ganhar(quantidade) {
    const p = App.estado.progresso;
    if (!p) return;

    // Track daily XP (reset if new day)
    const hoje = new Date().toISOString().slice(0, 10);
    if (p.data_xp_hoje !== hoje) {
      p.xp_hoje = 0;
      p.data_xp_hoje = hoje;
    }
    const xpAntes = p.xp_hoje || 0;
    p.xp_hoje = xpAntes + quantidade;

    // Fire "meta reached" toast exactly once per day
    const meta = p.meta_diaria || 100;
    if (xpAntes < meta && p.xp_hoje >= meta) {
      setTimeout(() => App.notificar('🎯 Meta diária atingida! Ottimo!', 'successo'), 400);
    }

    p.xp += quantidade;
    p.ultimo_estudo = Date.now();

    const nivelAnterior = p.nivel;
    this.verificarNivelUp();

    const subiu = p.nivel > nivelAnterior;
    if (subiu) {
      this.verificarDesbloqueioTemplos();
      App.notificar(`🎉 Livello ${p.nivel}! Avanzamento!`, 'successo');
    }

    App.salvarProgresso();
    App.atualizarStats();
  },

  // ── Level-up check ─────────────────────────────────────────
  verificarNivelUp() {
    const p = App.estado.progresso;
    if (!p) return;

    // Keep leveling while XP exceeds the next threshold
    let continuar = true;
    while (continuar) {
      const xpProximo = this.xpParaNivel(p.nivel + 1);
      if (p.xp >= xpProximo) {
        p.nivel++;
        p.xp_proximo_nivel = this.xpParaNivel(p.nivel + 1);
      } else {
        continuar = false;
      }
    }
  },

  // ── Temple unlock check ────────────────────────────────────
  verificarDesbloqueioTemplos() {
    const p = App.estado.progresso;
    if (!p) return;

    let novoDesbloqueio = false;
    for (const [temploNum, nivelNecessario] of Object.entries(this.TEMPLO_NIVEL)) {
      const num = parseInt(temploNum, 10);
      if (p.nivel >= nivelNecessario && !p.templos_desbloqueados.includes(num)) {
        p.templos_desbloqueados.push(num);
        p.templos_desbloqueados.sort((a, b) => a - b);
        novoDesbloqueio = true;
        App.notificar(`🏛️ Tempio ${num} sbloccato!`, 'successo');
      }
    }

    if (novoDesbloqueio) {
      App.salvarProgresso();
      App.renderizarTemplos();
      // Refresh quiz selector and flashcard dropdown
      if (typeof Quiz !== 'undefined') Quiz.renderizarSeletor();
      if (typeof Flashcards !== 'undefined') Flashcards.atualizarSelectTemplo();
      // Refresh vocab temple filter
      if (typeof Vocab !== 'undefined') Vocab.popularCategorias();
    }
  },

  // ── XP percentage within current level ────────────────────
  percentualNivel() {
    const p = App.estado.progresso;
    if (!p) return 0;
    const inicio = this.xpParaNivel(p.nivel);
    const fim = this.xpParaNivel(p.nivel + 1);
    const range = fim - inicio;
    if (range <= 0) return 100;
    return Math.min(100, Math.round(((p.xp - inicio) / range) * 100));
  },

  // ── Is temple unlocked? ────────────────────────────────────
  temploDesbloqueado(n) {
    const p = App.estado.progresso;
    if (!p) return false;
    return p.templos_desbloqueados.includes(n);
  },

  // ── Words mastered in a temple (FSRS: reps>=3 or stability>7d; SM-2: repeticoes>=3) ──
  palavrasDominadas(temploNum) {
    const data = App.estado.templosData[temploNum];
    if (!data || !data.palavras) return 0;
    return data.palavras.filter(p => {
      const sm = App.estado.flashcardData[p.id];
      if (!sm) return false;
      return (sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7);
    }).length;
  },

  // ── Check if temple is fully mastered ─────────────────────
  temploConcluido(temploNum) {
    const data = App.estado.templosData[temploNum];
    if (!data || !data.palavras || data.palavras.length === 0) return false;
    const dominadas = this.palavrasDominadas(temploNum);
    return dominadas >= data.palavras.length;
  },

  // ── Mark temple as concluded ───────────────────────────────
  marcarTemploConcluido(temploNum) {
    const p = App.estado.progresso;
    if (!p) return;
    if (!p.templos_concluidos.includes(temploNum)) {
      p.templos_concluidos.push(temploNum);
      App.salvarProgresso();
      App.notificar(`🏆 Tempio ${temploNum} completato!`, 'successo');
      App.renderizarTemplos();
    }
  }
};
