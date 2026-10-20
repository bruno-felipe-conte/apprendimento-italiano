// ============================================================
// js/core/xp.js — Experience Points & Level Progression (ARC-02)
// ============================================================

const AppXP = {
  // ── XP system (Optimistic UI pulse) ───────────────────────
  ganharXP(quantidade) {
    if (typeof document !== 'undefined') {
      const elXp = document.getElementById('stat-xp');
      if (elXp) {
        elXp.classList.remove('optimistic-xp-pulse');
        void elXp.offsetWidth;
        elXp.classList.add('optimistic-xp-pulse');
      }
    }

    const stateMod = (typeof window !== 'undefined' && window.AppState) || (typeof globalThis !== 'undefined' && globalThis.AppState) || (typeof AppState !== 'undefined' ? AppState : null);
    const statsMod = (typeof window !== 'undefined' && window.AppStats) || (typeof globalThis !== 'undefined' && globalThis.AppStats) || (typeof AppStats !== 'undefined' ? AppStats : null);
    const ttsMod = (typeof window !== 'undefined' && window.AppTTS) || (typeof globalThis !== 'undefined' && globalThis.AppTTS) || (typeof AppTTS !== 'undefined' ? AppTTS : null);

    if (typeof Progressao !== 'undefined') {
      Progressao.ganhar(quantidade);
    } else if (stateMod && stateMod.estado?.progresso) {
      stateMod.estado.progresso.xp += quantidade;
      if (typeof stateMod.salvarProgresso === 'function') {
        stateMod.salvarProgresso();
      }
      if (statsMod && typeof statsMod.atualizarStats === 'function') {
        statsMod.atualizarStats();
      }
    }

    if (ttsMod && typeof ttsMod.notificar === 'function') {
      ttsMod.notificar(`+${quantidade} XP`, 'alerta');
    }
  },

  verificarNivelUp() {
    if (typeof Progressao !== 'undefined') {
      Progressao.verificarNivelUp();
    }
  },

  verificarDesbloqueioTemplos() {
    if (typeof Progressao !== 'undefined') {
      Progressao.verificarDesbloqueioTemplos();
    }
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppXP = AppXP;
}
if (typeof window !== 'undefined') {
  window.AppXP = AppXP;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppXP;
}
