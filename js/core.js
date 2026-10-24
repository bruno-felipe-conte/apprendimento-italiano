// ============================================================
// core.js — Global App Facade & Bootstrap (ARC-02)
// Submodules: js/core/{state, navigation, xp, stats, favorites, meta, templo_data, templo_modal, templos, tts}.js
// ============================================================

const _g = (name) => (typeof window !== 'undefined' && window[name]) || (typeof globalThis !== 'undefined' && globalThis[name]) || null;

const App = {
  // ── Global State Proxy ─────────────────────────────────────
  get estado() { const s = _g('AppState'); return s ? s.estado : null; },
  set estado(val) { const s = _g('AppState'); if (s) s.estado = val; },

  // ── Constants delegation ───────────────────────────────────
  get TEMPLO_CORES() { return (_g('AppTemploData') || _g('AppTemplos'))?.TEMPLO_CORES || []; },
  get TEMPLO_NOMES() { return (_g('AppTemploData') || _g('AppTemplos'))?.TEMPLO_NOMES || []; },
  get TEMPLO_NIVEL_MINIMO() { return (_g('AppTemploData') || _g('AppTemplos'))?.TEMPLO_NIVEL_MINIMO || {}; },
  get TEMPLO_DESC() { return (_g('AppTemploData') || _g('AppTemplos'))?.TEMPLO_DESC || []; },
  get _UNLOCK_HASH() { return _g('AppState')?._UNLOCK_HASH || ''; },

  // ── State & Persistence (js/core/state.js) ─────────────────
  verificarCodigoAcesso: (c) => _g('AppState')?.verificarCodigoAcesso(c),
  escapeHtml: (s) => _g('AppState')?.escapeHtml(s),
  initGlobalErrorHandler: () => _g('AppState')?.initGlobalErrorHandler(),
  carregarProgresso: () => _g('AppState')?.carregarProgresso(),
  salvarProgresso: () => _g('AppState')?.salvarProgresso(),
  carregarFlashcards: () => _g('AppState')?.carregarFlashcards(),
  salvarFlashcards: () => _g('AppState')?.salvarFlashcards(),
  _gcFlashcards: () => _g('AppState')?._gcFlashcards(),
  _hidratarCacheLocal: () => _g('AppState')?._hidratarCacheLocal(),
  carregarDados: () => _g('AppState')?.carregarDados(),

  // ── Navigation (js/core/navigation.js) ─────────────────────
  initSidebarPin: () => _g('AppNavigation')?.initSidebarPin(),
  toggleSidebarPin: (e) => _g('AppNavigation')?.toggleSidebarPin(e),
  navegar: (s) => _g('AppNavigation')?.navegar(s),

  // ── Experience & Progression (js/core/xp.js) ───────────────
  ganharXP: (q) => _g('AppXP')?.ganharXP(q),
  verificarNivelUp: () => _g('AppXP')?.verificarNivelUp(),
  verificarDesbloqueioTemplos: () => _g('AppXP')?.verificarDesbloqueioTemplos(),

  // ── Stats & Diagnostics (js/core/stats.js) ─────────────────
  atualizarStats: () => _g('AppStats')?.atualizarStats?.(),
  renderizarCardContinuar: () => _g('AppStats')?.renderizarCardContinuar?.() || '',
  abrirHealthCheck: () => _g('AppStats')?.abrirHealthCheck?.(),
  fecharHealthCheck: () => _g('AppStats')?.fecharHealthCheck?.(),

  // ── Goals & Deadlines (js/core/meta.js) ─────────────────────
  _renderizarMetaPrazo: () => _g('AppMeta')?._renderizarMetaPrazo?.() || '',
  abrirMetaSettings: () => _g('AppMeta')?.abrirMetaSettings?.(),
  fecharMetaSettings: () => _g('AppMeta')?.fecharMetaSettings?.(),
  setMeta: (v) => _g('AppMeta')?.setMeta?.(v),
  abrirModalMetaPrazo: () => _g('AppMeta')?.abrirModalMetaPrazo?.(),
  fecharModalMetaPrazo: () => _g('AppMeta')?.fecharModalMetaPrazo?.(),
  confirmarMetaPrazo: () => _g('AppMeta')?.confirmarMetaPrazo?.(),

  // ── Favorites (js/core/favorites.js) ───────────────────────
  toggleFavorito: (id, el) => _g('AppFavorites')?.toggleFavorito(id, el),
  ehFavorito: (id) => _g('AppFavorites')?.ehFavorito(id),
  renderizarParolaDia: () => _g('AppFavorites')?.renderizarParolaDia(),

  // ── Temples (js/core/templos.js & js/core/templo_modal.js) ──
  renderizarTemplos: () => _g('AppTemplos')?.renderizarTemplos(),
  estudarTemplo: (n) => _g('AppTemplos')?.estudarTemplo(n),
  estudarPalavra: (id, n) => _g('AppTemplos')?.estudarPalavra(id, n),
  quizTemplo: (n) => _g('AppTemplos')?.quizTemplo(n),
  abrirModalTemplo: (i) => (_g('AppTemploModal') || _g('AppTemplos'))?.abrirModalTemplo(i),
  fecharModalTemplo: () => (_g('AppTemploModal') || _g('AppTemplos'))?.fecharModalTemplo(),
  pedirSenhaTemplo: (n) => (_g('AppTemploModal') || _g('AppTemplos'))?.pedirSenhaTemplo(n),
  tentarDesbloquear: (n) => (_g('AppTemploModal') || _g('AppTemplos'))?.tentarDesbloquear(n),

  // ── Speech & Notifications (js/core/tts.js) ────────────────
  notificar: (m, t) => _g('AppTTS')?.notificar?.(m, t),
  toggleAudioSpeed: () => _g('AppTTS')?.toggleAudioSpeed?.(),
  atualizarAudioSpeedUI: () => _g('AppTTS')?.atualizarAudioSpeedUI?.(),
  _getVozItaliana: () => _g('AppTTS')?._getVozItaliana?.() || null,
  pronunciar: (txt, r) => _g('AppTTS')?.pronunciar?.(txt, r),

  // ── Plugin Architecture (js/core/plugins.ts) ───────────────
  get pluginManager() { return _g('AppPluginManager'); },
  registerPlugin: (p) => _g('AppPluginManager')?.register(p),
  unregisterPlugin: (id) => _g('AppPluginManager')?.unregister(id),
  getPlugin: (id) => _g('AppPluginManager')?.get(id),
  getPlugins: () => _g('AppPluginManager')?.getAll() || [],

  // ── Backend Lite & Sync (js/core/sync.ts) ──────────────────
  get sync() { return _g('AppSyncManager'); },
  sincronizar: () => _g('AppSyncManager')?.flush(),
  obterStatusSync: () => _g('AppSyncManager')?.getStatus(),

  // ── Analytics & A/B Testing (js/core/analytics.ts) ────────
  get analytics() { return _g('AppAnalytics'); },
  get features() { return _g('AppFeatureFlags'); },
  track: (name, props) => _g('AppAnalytics')?.track(name, props),
  getFlag: (key) => _g('AppFeatureFlags')?.getVariant(key),

  // ── Multi-Device Sync & Collaboration (js/core/collaboration.ts) ──
  get collaboration() { return _g('AppCollaboration'); },
  reconciliarDados: (remoto) => _g('AppCollaboration')?.reconciliar(
    { progresso: _g('AppState')?.estado?.progresso, flashcards: _g('AppState')?.estado?.flashcardData },
    remoto
  ),

  // ── Bootstrap & Lifecycle ──────────────────────────────────
  async init() {
    this.initGlobalErrorHandler();
    if (_g('AppAnalytics')) {
      _g('AppAnalytics').track('app_initialized', { timestamp: Date.now() });
    }
    if (_g('AppPluginManager')) {
      await _g('AppPluginManager').initAll(this);
    }
    this.estado.progresso = this.carregarProgresso();
    this.estado.flashcardData = this.carregarFlashcards();
    if (typeof I18n !== 'undefined') I18n.inicializar();

    if (_g('AppSyncManager') && typeof navigator !== 'undefined' && navigator.onLine) {
      _g('AppSyncManager').flush().catch(() => {});
    }

    if (this._hidratarCacheLocal()) {
      this.atualizarStats();
      this.renderizarTemplos();
    }

    await this.carregarDados();
    this.atualizarStats();
    this.renderizarTemplos();

    if (typeof Progressao !== 'undefined') Progressao.verificarDesbloqueioTemplos();
    if (typeof Quiz !== 'undefined') Quiz.renderizarSeletor();
    if (typeof Vocab !== 'undefined') { Vocab.popularCategorias(); Vocab.renderizar(); }
    if (typeof Flashcards !== 'undefined') Flashcards.atualizarSelectTemplo();
    if (typeof Calor !== 'undefined') Calor.renderizar();
    if (typeof Grammatica !== 'undefined') Grammatica.renderizarSeletor();
    if (typeof SomFeedback !== 'undefined') SomFeedback.init();
    if (typeof Notificacoes !== 'undefined') Notificacoes.init();

    if (typeof navigator !== 'undefined' && navigator.storage?.estimate) {
      navigator.storage.estimate().then(est => {
        if (est.quota && est.usage && (est.usage / est.quota) > 0.8) {
          this.notificar('Atenção: Armazenamento local quase cheio (>80%). Considere limpar itens antigos.', 'alerta');
        }
      }).catch(() => {});
    }

    this.atualizarAudioSpeedUI();
    this.initSidebarPin();

    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      speechSynthesis.getVoices();
      speechSynthesis.onvoiceschanged = () => { this._getVozItaliana(); speechSynthesis.onvoiceschanged = null; };
    }

    if (typeof Onboarding !== 'undefined' && Onboarding.deveExibir()) Onboarding.mostrar();
    if (typeof BackupReminder !== 'undefined') BackupReminder.verificarLembrete();

    if (typeof document !== 'undefined') {
      document.addEventListener('keydown', (e) => {
        if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)) return;
        const mapa = { '1': 'templi', '2': 'flashcard', '3': 'quiz', '4': 'vocabolario', '5': 'grammatica' };
        if (mapa[e.key]) this.navegar(mapa[e.key]);
      });
    }
  }
};

if (typeof window !== 'undefined') window.App = App;
if (typeof globalThis !== 'undefined') globalThis.App = App;
if (typeof module !== 'undefined' && module.exports) module.exports = App;

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => App.init());
}

if (typeof window !== 'undefined') {
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === 'H' || e.key === 'h')) {
      e.preventDefault();
      App.abrirHealthCheck?.();
    }
  });
}
