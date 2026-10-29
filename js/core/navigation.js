// ============================================================
// js/core/navigation.js — Navigation & Sidebar Pin (ARC-02)
// ============================================================

const AppNavigation = {
  // ── Desktop Sidebar Pin / Unpin ───────────────────────────
  initSidebarPin() {
    if (typeof localStorage === 'undefined' || typeof document === 'undefined') return;
    const isPinned = localStorage.getItem('it_sidebar_pinned') === 'true';
    const sidebar = document.getElementById('app-sidebar');
    const pinBtn = document.getElementById('sidebar-pin-btn');
    const pinIcon = document.getElementById('sidebar-pin-icon');

    const svgUnpinned = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"></line><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a1 1 0 0 0 0-2H8a1 1 0 0 0 0 2h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"></path></svg>`;
    const svgPinned = `<svg viewBox="0 0 24 24" width="13" height="13" stroke="currentColor" stroke-width="2" fill="currentColor" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="17" x2="12" y2="22"></line><path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 10.76V6h1a1 1 0 0 0 0-2H8a1 1 0 0 0 0 2h1v4.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24Z"></path></svg>`;

    if (isPinned) {
      document.body.classList.add('sidebar-pinned');
      if (sidebar) sidebar.classList.add('pinned');
      if (pinBtn) {
        pinBtn.classList.add('ativo');
        pinBtn.title = 'Desafixar barra lateral';
        pinBtn.setAttribute('aria-label', 'Desafixar barra lateral');
      }
      if (pinIcon) pinIcon.innerHTML = svgPinned;
    } else {
      document.body.classList.remove('sidebar-pinned');
      if (sidebar) sidebar.classList.remove('pinned');
      if (pinBtn) {
        pinBtn.classList.remove('ativo');
        pinBtn.title = 'Fixar barra lateral';
        pinBtn.setAttribute('aria-label', 'Fixar barra lateral');
      }
      if (pinIcon) pinIcon.innerHTML = svgUnpinned;
    }
  },

  toggleSidebarPin(e) {
    if (e && e.stopPropagation) e.stopPropagation();
    if (typeof document === 'undefined' || typeof localStorage === 'undefined') return;
    const isPinned = document.body.classList.contains('sidebar-pinned');
    const novoEstado = !isPinned;
    localStorage.setItem('it_sidebar_pinned', novoEstado ? 'true' : 'false');
    this.initSidebarPin();
  },

  // ── Navigation (Preserves DOM & Filter state across tabs) ──
  navegar(secao) {
    // 'home' é um alias para 'templi' (seção inicial)
    if (secao === 'home') secao = 'templi';

    const stateMod = (typeof window !== 'undefined' && window.AppState) || (typeof globalThis !== 'undefined' && globalThis.AppState) || (typeof AppState !== 'undefined' ? AppState : null);
    const estado = stateMod ? stateMod.estado : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const secaoAnterior = estado ? estado.secaoAtiva : '';

    if (estado) {
      estado.secaoAtiva = secao;
    }

    // Pausa karaokê se sair da aba de músicas
    if (secao !== 'canzoni' && typeof Canzoni !== 'undefined' && Canzoni.tocandoKaraoke) {
      Canzoni.pararAudio();
    }

    // Notifica plugins de mudança de seção
    const pluginMgr = (typeof window !== 'undefined' && window.AppPluginManager) || (typeof globalThis !== 'undefined' && globalThis.AppPluginManager);
    if (pluginMgr && typeof pluginMgr.notifySectionChange === 'function') {
      pluginMgr.notifySectionChange(secao, secaoAnterior);
    }

    // Registra telemetria de visualização de seção (EV-04)
    const analytics = (typeof window !== 'undefined' && window.AppAnalytics) || (typeof globalThis !== 'undefined' && globalThis.AppAnalytics);
    if (analytics && typeof analytics.page === 'function') {
      analytics.page(secao, { de: secaoAnterior });
    }

    if (typeof document !== 'undefined') {
      // Update tab buttons
      document.querySelectorAll('.nav-tab').forEach(btn => {
        btn.classList.toggle('ativa', btn.dataset.section === secao);
      });

      // Update bottom nav buttons
      document.querySelectorAll('#bottom-nav button').forEach(btn => {
        btn.classList.toggle('ativa', btn.dataset.section === secao);
      });

      // Show/hide sections
      document.querySelectorAll('.section').forEach(sec => {
        sec.classList.toggle('active', sec.id === `sec-${secao}`);
      });
    }

    // Persist last section visited
    if (estado && estado.progresso) {
      estado.progresso.ultima_secao = secao;
      if (stateMod && typeof stateMod.salvarProgresso === 'function') {
        stateMod.salvarProgresso();
      } else if (typeof App !== 'undefined' && typeof App.salvarProgresso === 'function') {
        App.salvarProgresso();
      }
    }

    // Se houver plugin com rota registrada para a seção, despacha para ele
    if (pluginMgr && typeof pluginMgr.hasRoute === 'function' && pluginMgr.hasRoute(secao)) {
      pluginMgr.dispatchRoute(secao);
      return;
    }

    const _precisaRender = (containerId) => {
      if (typeof document === 'undefined') return false;
      const el = document.getElementById(containerId);
      if (!el) return true;
      return el.children.length === 0 || !!el.querySelector('.skeleton-box, .skeleton-card-media, .skeleton-card-templo, .skeleton-vocab-row');
    };

    // Lazy-render on first visit or when container only has skeleton (preserves active lessons & filters!)
    if (secao === 'dialoghi' && typeof Dialoghi !== 'undefined') {
      if (_precisaRender('dialoghi-container') && !Dialoghi.dialogoAtual) Dialoghi.renderizarSeletor();
    }
    if (secao === 'canzoni' && typeof Canzoni !== 'undefined') {
      if (_precisaRender('canzoni-container')) Canzoni.renderizarSeletor();
    }
    if (secao === 'imitazione' && typeof Imitazione !== 'undefined') {
      if (_precisaRender('imitazione-container')) Imitazione.renderizar();
    }
    if (secao === 'vocabolario' && typeof Vocab !== 'undefined') {
      if (_precisaRender('vocab-list')) Vocab.renderizar();
    }
    if (secao === 'quiz' && typeof Quiz !== 'undefined') {
      if (_precisaRender('quiz-templo-selector')) Quiz.renderizarSeletor();
    }
    if (secao === 'flashcard' && typeof Flashcards !== 'undefined') {
      Flashcards.atualizarSelectTemplo();
      if (typeof Flashcards.atualizarEbbinghaus === 'function') Flashcards.atualizarEbbinghaus();
    }
    if (secao === 'grammatica' && typeof Grammatica !== 'undefined') {
      if (_precisaRender('grammatica-container')) Grammatica.renderizarSeletor();
    }
    if (secao === 'storie' && typeof Storie !== 'undefined') {
      if (_precisaRender('storie-container')) Storie.renderizarSeletor();
    }
    if (secao === 'profilo' && typeof Profilo !== 'undefined') {
      Profilo.renderizar();
    }
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppNavigation = AppNavigation;
}
if (typeof window !== 'undefined') {
  window.AppNavigation = AppNavigation;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppNavigation;
}
