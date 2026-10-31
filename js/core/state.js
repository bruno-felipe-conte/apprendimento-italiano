// ============================================================
// js/core/state.js — Global State & Persistence (ARC-02)
// ============================================================

const AppState = {
  // ── State ──────────────────────────────────────────────────
  /** @type {{ secaoAtiva: string, templosData: Record<string | number, any>, quizData: any[], vocabCache: any[], conjugacoesData: any[], grammarData: any, progresso: any, flashcardData: Record<string, any> }} */
  estado: {
    secaoAtiva: 'templi',
    templosData: {},       // { 1: { templo, nome, cidade, nivel, palavras: [] }, ... }
    quizData: [],          // flat array of all quiz questions
    vocabCache: [],        // flat array of all words (with templo_num attached)
    conjugacoesData: [],   // verb conjugation data
    grammarData: null,     // grammar modules and exercises
    progresso: null,       // persisted in localStorage
    flashcardData: {}      // persisted in localStorage
  },

  // Hash criptográfico SHA-256 do código mestre de acesso/desbloqueio (SEC-01)
  _UNLOCK_HASH: '4b9a7f50c0bb198c6f5414c5a8459f5d216d34ab521ea94c060ea35cac66f900',

  async verificarCodigoAcesso(codigo) {
    if (!codigo || typeof codigo !== 'string') return false;
    try {
      const enc = new TextEncoder().encode(codigo.trim());
      const buf = await crypto.subtle.digest('SHA-256', enc);
      const hex = Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, '0')).join('');
      return hex === this._UNLOCK_HASH;
    } catch (_) {
      return false;
    }
  },

  escapeHtml(str) {
    if (str == null) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  },

  // ── Error Boundary Global (HAR-01) ────────────────────────
  initGlobalErrorHandler() {
    window.onerror = (message, source, lineno, colno, error) => {
      try {
        const errorLog = {
          tipo: 'uncaught_error',
          timestamp: new Date().toISOString(),
          message: String(message),
          source: String(source),
          lineno,
          colno,
          stack: error?.stack || null,
          userAgent: navigator.userAgent
        };
        console.error('[GlobalError]', errorLog);
        const logs = (typeof SafeStorage !== 'undefined')
          ? SafeStorage.getItem('it_client_errors', [])
          : JSON.parse(localStorage.getItem('it_client_errors') || '[]');
        const arr = Array.isArray(logs) ? logs : [];
        arr.unshift(errorLog);
        if (typeof SafeStorage !== 'undefined') {
          SafeStorage.setItem('it_client_errors', arr.slice(0, 30));
        } else {
          localStorage.setItem('it_client_errors', JSON.stringify(arr.slice(0, 30)));
        }
      } catch (_) {}
    };

    window.addEventListener('unhandledrejection', (event) => {
      try {
        const errorLog = {
          tipo: 'unhandled_rejection',
          timestamp: new Date().toISOString(),
          reason: String(event.reason?.message || event.reason),
          stack: event.reason?.stack || null,
          userAgent: navigator.userAgent
        };
        console.error('[UnhandledRejection]', errorLog);
        const logs = (typeof SafeStorage !== 'undefined')
          ? SafeStorage.getItem('it_client_errors', [])
          : JSON.parse(localStorage.getItem('it_client_errors') || '[]');
        const arr = Array.isArray(logs) ? logs : [];
        arr.unshift(errorLog);
        if (typeof SafeStorage !== 'undefined') {
          SafeStorage.setItem('it_client_errors', arr.slice(0, 30));
        } else {
          localStorage.setItem('it_client_errors', JSON.stringify(arr.slice(0, 30)));
        }
      } catch (_) {}
    });
  },

  // ── Sanitização Textual Ingestion (SEC-02) ───────────────────
  sanitizarTexto(str) {
    if (str == null) return '';
    if (typeof str !== 'string') return String(str);
    return str.replace(/<[^>]*>?/gm, '').trim();
  },

  // ── Stale-While-Revalidate helper for Templos & Vocab ──────
  _hidratarCacheLocal() {
    try {
      const meta = (typeof SafeStorage !== 'undefined')
        ? SafeStorage.getItem('it_swr_templos_meta', null)
        : JSON.parse(localStorage.getItem('it_swr_templos_meta') || 'null');
      if (!meta || typeof meta !== 'object' || Array.isArray(meta)) return false;
      for (const k of Object.keys(meta)) {
        const num = Number(k);
        if (!this.estado.templosData[num]) {
          this.estado.templosData[num] = meta[k];
        }
      }
      return Object.keys(meta).length > 0;
    } catch (_) {
      return false;
    }
  },

  // ── Multi-Tab Concurrency & Synchronization (F3) ────────────
  _tabId: null,
  _syncChannel: null,
  _syncInitialized: false,

  _getTabId() {
    if (!this._tabId) {
      this._tabId = 'tab_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);
    }
    return this._tabId;
  },

  initCrossTabSync() {
    if (this._syncInitialized || typeof window === 'undefined') return;
    this._syncInitialized = true;
    const tabId = this._getTabId();

    if (typeof BroadcastChannel !== 'undefined') {
      try {
        this._syncChannel = new BroadcastChannel('apprendimento_channel');
        this._syncChannel.onmessage = (event) => {
          const msg = event?.data;
          if (!msg || msg.senderId === tabId) return;
          this._tratarMensagemSincronizacao(msg);
        };
      } catch (err) {
        console.warn('[Sync] Falha ao instanciar BroadcastChannel, usando fallback storage:', err);
        this._syncChannel = null;
      }
    }

    window.addEventListener('storage', (e) => {
      if (!e.key) return;
      if (e.key === 'it_progresso' || e.key === 'it_flashcards') {
        this._tratarStorageEvent(e);
      }
    });
  },

  _broadcastSync(key, payload) {
    const tabId = this._getTabId();
    const envelope = {
      type: 'SYNC_UPDATE',
      key,
      senderId: tabId,
      timestamp: Date.now(),
      payload
    };

    if (this._syncChannel) {
      try {
        this._syncChannel.postMessage(envelope);
      } catch (err) {
        console.warn('[Sync] Erro ao enviar BroadcastChannel:', err);
      }
    }
  },

  _tratarMensagemSincronizacao(msg) {
    if (!msg || msg.type !== 'SYNC_UPDATE') return;
    if (msg.key === 'it_progresso') {
      this._processarProgressoRemoto(msg.payload);
    } else if (msg.key === 'it_flashcards') {
      this._processarFlashcardsRemoto(msg.payload);
    }
  },

  _tratarStorageEvent(e) {
    if (e.key === 'it_progresso' && e.newValue) {
      try {
        const remoto = JSON.parse(e.newValue);
        this._processarProgressoRemoto(remoto);
      } catch (_) {}
    } else if (e.key === 'it_flashcards' && e.newValue) {
      try {
        const remoto = JSON.parse(e.newValue);
        this._processarFlashcardsRemoto(remoto);
      } catch (_) {}
    }
  },

  _processarProgressoRemoto(remoto) {
    if (!remoto || typeof remoto !== 'object' || Array.isArray(remoto)) return;
    const local = this.estado.progresso;
    const merged = this.reconciliarProgresso(local, remoto);

    if (JSON.stringify(local) === JSON.stringify(merged)) return;

    this.estado.progresso = merged;

    if (JSON.stringify(merged) !== JSON.stringify(remoto)) {
      try {
        if (typeof SafeStorage !== 'undefined') {
          SafeStorage.setItem('it_progresso', merged);
        } else {
          localStorage.setItem('it_progresso', JSON.stringify(merged));
        }
        this._broadcastSync('it_progresso', merged);
      } catch (_) {}
    }

    const statsMod = (typeof window !== 'undefined' && window.AppStats) || (typeof AppStats !== 'undefined' ? AppStats : null);
    if (statsMod && typeof statsMod.atualizarStats === 'function') {
      statsMod.atualizarStats();
    }
    if (typeof Progressao !== 'undefined' && typeof Progressao.verificarDesbloqueioTemplos === 'function') {
      Progressao.verificarDesbloqueioTemplos();
    }
  },

  _processarFlashcardsRemoto(remoto) {
    if (!remoto || typeof remoto !== 'object' || Array.isArray(remoto)) return;
    const local = this.estado.flashcardData;
    const merged = this.reconciliarFlashcards(local, remoto);

    if (JSON.stringify(local) === JSON.stringify(merged)) return;

    this.estado.flashcardData = merged;

    if (JSON.stringify(merged) !== JSON.stringify(remoto)) {
      try {
        if (typeof SafeStorage !== 'undefined') {
          SafeStorage.setItem('it_flashcards', merged);
        } else {
          localStorage.setItem('it_flashcards', JSON.stringify(merged));
        }
        this._broadcastSync('it_flashcards', merged);
      } catch (_) {}
    }

    const statsMod = (typeof window !== 'undefined' && window.AppStats) || (typeof AppStats !== 'undefined' ? AppStats : null);
    if (statsMod && typeof statsMod.atualizarStats === 'function') {
      statsMod.atualizarStats();
    }
  },

  reconciliarProgresso(local, remoto) {
    if (!local && !remoto) return this.carregarProgresso();
    if (!local) return this._sanitizeProgresso(remoto);
    if (!remoto) return this._sanitizeProgresso(local);

    const uniaoNumeros = (a = [], b = []) =>
      Array.from(new Set([...(Array.isArray(a) ? a : []), ...(Array.isArray(b) ? b : [])]))
        .filter(n => typeof n === 'number' && !isNaN(n))
        .sort((x, y) => x - y);
    const uniaoStrings = (a = [], b = []) =>
      Array.from(new Set([...(Array.isArray(a) ? a : []), ...(Array.isArray(b) ? b : [])]))
        .filter(s => s !== null && s !== undefined);

    const nivel = Math.max(Number(local.nivel) || 1, Number(remoto.nivel) || 1);
    const xp = Math.max(Number(local.xp) || 0, Number(remoto.xp) || 0);

    let streak = Math.max(Number(local.streak) || 0, Number(remoto.streak) || 0);
    if (local.ultimo_estudo && remoto.ultimo_estudo) {
      if (remoto.ultimo_estudo > local.ultimo_estudo && remoto.streak !== undefined) {
        streak = Math.max(streak, Number(remoto.streak) || 0);
      } else if (local.ultimo_estudo > remoto.ultimo_estudo && local.streak !== undefined) {
        streak = Math.max(streak, Number(local.streak) || 0);
      }
    }

    const streakRecorde = Math.max(
      Number(local.streak_recorde) || 0,
      Number(remoto.streak_recorde) || 0,
      streak
    );

    let xp_hoje = Math.max(Number(local.xp_hoje) || 0, Number(remoto.xp_hoje) || 0);
    let data_xp_hoje = local.data_xp_hoje || remoto.data_xp_hoje || null;
    if (local.data_xp_hoje && remoto.data_xp_hoje) {
      if (remoto.data_xp_hoje > local.data_xp_hoje) {
        data_xp_hoje = remoto.data_xp_hoje;
        xp_hoje = Number(remoto.xp_hoje) || 0;
      } else if (local.data_xp_hoje > remoto.data_xp_hoje) {
        data_xp_hoje = local.data_xp_hoje;
        xp_hoje = Number(local.xp_hoje) || 0;
      }
    }

    const uniaoTemplosDesbloqueados = uniaoNumeros(local.templos_desbloqueados, remoto.templos_desbloqueados);
    if (!uniaoTemplosDesbloqueados.includes(1)) {
      uniaoTemplosDesbloqueados.unshift(1);
    }

    return {
      ...local,
      ...remoto,
      nivel,
      xp,
      xp_proximo_nivel: Math.max(Number(local.xp_proximo_nivel) || 500, Number(remoto.xp_proximo_nivel) || 500),
      templos_desbloqueados: uniaoTemplosDesbloqueados,
      templos_concluidos: uniaoNumeros(local.templos_concluidos, remoto.templos_concluidos),
      total_palavras: Math.max(Number(local.total_palavras) || 0, Number(remoto.total_palavras) || 0),
      streak,
      streak_recorde: streakRecorde,
      ultimo_estudo: Math.max(Number(local.ultimo_estudo) || 0, Number(remoto.ultimo_estudo) || 0) || null,
      grammatica_completadas: uniaoStrings(local.grammatica_completadas, remoto.grammatica_completadas),
      meta_diaria: local.meta_diaria || remoto.meta_diaria || 100,
      xp_hoje,
      data_xp_hoje,
      favoritos: uniaoStrings(local.favoritos, remoto.favoritos),
      conquistas: uniaoStrings(local.conquistas, remoto.conquistas),
      data_inicio: Math.min(Number(local.data_inicio) || Date.now(), Number(remoto.data_inicio) || Date.now()),
      meta_prazo: remoto.meta_prazo || local.meta_prazo || null,
      audio_rate: (typeof remoto.audio_rate === 'number' && !isNaN(remoto.audio_rate))
        ? remoto.audio_rate
        : (typeof local.audio_rate === 'number' && !isNaN(local.audio_rate) ? local.audio_rate : 0.85)
    };
  },

  reconciliarFlashcards(local = {}, remoto = {}) {
    const loc = local && typeof local === 'object' && !Array.isArray(local) ? local : {};
    const rem = remoto && typeof remoto === 'object' && !Array.isArray(remoto) ? remoto : {};
    const merged = { ...loc };

    for (const cardId of Object.keys(rem)) {
      const cardRemoto = rem[cardId];
      const cardLocal = loc[cardId];

      if (!cardLocal) {
        merged[cardId] = { ...cardRemoto };
        continue;
      }

      const timeLocal = Number(cardLocal.lastReview || cardLocal.last_review) || 0;
      const timeRemoto = Number(cardRemoto.lastReview || cardRemoto.last_review) || 0;

      if (timeRemoto > timeLocal) {
        merged[cardId] = { ...cardRemoto };
      } else if (timeLocal > timeRemoto) {
        merged[cardId] = { ...cardLocal };
      } else {
        const repsLocal = Number(cardLocal.reps || cardLocal.repeticoes) || 0;
        const repsRemoto = Number(cardRemoto.reps || cardRemoto.repeticoes) || 0;
        merged[cardId] = repsRemoto >= repsLocal ? { ...cardRemoto } : { ...cardLocal };
      }
    }

    return merged;
  },

  // ── Schema Sanitization (F4, F5) ───────────────────────────
  _sanitizeProgresso(p) {
    const defaults = {
      nivel: 1,
      xp: 0,
      xp_proximo_nivel: 500,
      templos_desbloqueados: [1],
      templos_concluidos: [],
      total_palavras: 0,
      streak: 0,
      ultimo_estudo: null,
      grammatica_completadas: [],
      meta_diaria: 100,
      xp_hoje: 0,
      data_xp_hoje: null,
      favoritos: [],
      conquistas: [],
      data_inicio: Date.now(),
      meta_prazo: null,
      audio_rate: 0.85
    };

    if (!p || typeof p !== 'object' || Array.isArray(p)) {
      return defaults;
    }

    const nivel = (Number.isInteger(p.nivel) && p.nivel >= 1) ? p.nivel : 1;
    const xp = (typeof p.xp === 'number' && Number.isFinite(p.xp) && p.xp >= 0) ? Math.floor(p.xp) : 0;
    const xp_proximo_nivel = (typeof p.xp_proximo_nivel === 'number' && Number.isFinite(p.xp_proximo_nivel) && p.xp_proximo_nivel > 0)
      ? Math.floor(p.xp_proximo_nivel)
      : (nivel * 500);

    let templos_desbloqueados = [1];
    if (Array.isArray(p.templos_desbloqueados)) {
      const validos = p.templos_desbloqueados.filter(t => Number.isInteger(t) && t >= 1 && t <= 100);
      if (!validos.includes(1)) validos.unshift(1);
      templos_desbloqueados = Array.from(new Set(validos));
    }

    const templos_concluidos = Array.isArray(p.templos_concluidos)
      ? Array.from(new Set(p.templos_concluidos.filter(t => Number.isInteger(t) && t >= 1)))
      : [];

    const total_palavras = (typeof p.total_palavras === 'number' && Number.isFinite(p.total_palavras) && p.total_palavras >= 0)
      ? Math.floor(p.total_palavras)
      : 0;

    const streak = (typeof p.streak === 'number' && Number.isFinite(p.streak) && p.streak >= 0)
      ? Math.floor(p.streak)
      : 0;

    const ultimo_estudo = (typeof p.ultimo_estudo === 'number' && Number.isFinite(p.ultimo_estudo))
      ? p.ultimo_estudo
      : (typeof p.ultimo_estudo === 'string' && !isNaN(Date.parse(p.ultimo_estudo)) ? Date.parse(p.ultimo_estudo) : null);

    const grammatica_completadas = Array.isArray(p.grammatica_completadas)
      ? p.grammatica_completadas.filter(id => typeof id === 'string' || typeof id === 'number')
      : [];

    const meta_diaria = (typeof p.meta_diaria === 'number' && Number.isFinite(p.meta_diaria) && p.meta_diaria > 0)
      ? Math.floor(p.meta_diaria)
      : 100;

    const xp_hoje = (typeof p.xp_hoje === 'number' && Number.isFinite(p.xp_hoje) && p.xp_hoje >= 0)
      ? Math.floor(p.xp_hoje)
      : 0;

    const data_xp_hoje = typeof p.data_xp_hoje === 'string' ? p.data_xp_hoje : null;

    const favoritos = Array.isArray(p.favoritos)
      ? p.favoritos.filter(f => typeof f === 'string' || typeof f === 'number')
      : [];

    const conquistas = Array.isArray(p.conquistas)
      ? p.conquistas.filter(c => typeof c === 'string' || (c && typeof c.id === 'string'))
      : [];

    const data_inicio = (typeof p.data_inicio === 'number' && Number.isFinite(p.data_inicio))
      ? p.data_inicio
      : (ultimo_estudo || Date.now());

    let meta_prazo = null;
    if (p.meta_prazo && typeof p.meta_prazo === 'object' && !Array.isArray(p.meta_prazo)) {
      if (Number.isInteger(p.meta_prazo.nivelAlvo) && p.meta_prazo.dataAlvo) {
        meta_prazo = {
          nivelAlvo: p.meta_prazo.nivelAlvo,
          dataAlvo: String(p.meta_prazo.dataAlvo)
        };
      }
    }

    const audio_rate = (typeof p.audio_rate === 'number' && Number.isFinite(p.audio_rate) && p.audio_rate >= 0.5 && p.audio_rate <= 2.0)
      ? p.audio_rate
      : 0.85;

    return {
      nivel,
      xp,
      xp_proximo_nivel,
      templos_desbloqueados,
      templos_concluidos,
      total_palavras,
      streak,
      ultimo_estudo,
      grammatica_completadas,
      meta_diaria,
      xp_hoje,
      data_xp_hoje,
      favoritos,
      conquistas,
      data_inicio,
      meta_prazo,
      audio_rate
    };
  },

  /**
   * @param {any} deck
   * @returns {Record<string, any>}
   */
  _sanitizeFlashcards(deck) {
    if (!deck || typeof deck !== 'object' || Array.isArray(deck)) {
      return {};
    }
    const sanitizedDeck = {};
    const validStates = ['new', 'learning', 'review', 'relearning', 'suspended'];

    for (const [id, card] of Object.entries(deck)) {
      if (!card || typeof card !== 'object' || Array.isArray(card)) {
        continue;
      }

      const state = validStates.includes(card.state) ? card.state : 'new';
      const difficulty = (typeof card.difficulty === 'number' && Number.isFinite(card.difficulty))
        ? Math.min(Math.max(card.difficulty, 1), 10)
        : 5.0;
      const stability = (typeof card.stability === 'number' && Number.isFinite(card.stability) && card.stability >= 0)
        ? Math.min(Math.max(card.stability, 0.1), 36500)
        : 1.0;
      const reps = (Number.isInteger(card.reps) && card.reps >= 0) ? card.reps : 0;
      const lapses = (Number.isInteger(card.lapses) && card.lapses >= 0) ? card.lapses : 0;
      const lastReview = (typeof card.lastReview === 'number' && Number.isFinite(card.lastReview))
        ? card.lastReview
        : null;
      const interval = (typeof card.interval === 'number' && Number.isFinite(card.interval) && card.interval >= 0)
        ? card.interval
        : 1;
      const nextReview = (typeof card.nextReview === 'number' && Number.isFinite(card.nextReview))
        ? card.nextReview
        : null;
      const retrievability = (typeof card.retrievability === 'number' && Number.isFinite(card.retrievability))
        ? Math.min(Math.max(card.retrievability, 0), 1)
        : 1.0;

      sanitizedDeck[id] = {
        ...card,
        state,
        difficulty,
        stability,
        reps,
        lapses,
        lastReview,
        interval,
        nextReview,
        retrievability
      };
    }

    return sanitizedDeck;
  },

  // ── localStorage ───────────────────────────────────────────
  carregarProgresso() {
    try {
      const raw = (typeof SafeStorage !== 'undefined')
        ? SafeStorage.getItem('it_progresso', null)
        : JSON.parse(localStorage.getItem('it_progresso') || 'null');
      return this._sanitizeProgresso(raw);
    } catch (e) {
      console.warn('[AppState] Falha ao carregar progresso, restaurando defaults:', e);
    }
    return this._sanitizeProgresso(null);
  },

  salvarProgresso() {
    if (!this.estado.progresso) return false;
    let sucesso = false;
    try {
      if (typeof SafeStorage !== 'undefined') {
        sucesso = SafeStorage.setItem('it_progresso', this.estado.progresso);
      } else {
        localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
        sucesso = true;
      }
    } catch (e) {
      if ((typeof SafeStorage !== 'undefined' && SafeStorage.isQuotaExceeded(e)) || e.name === 'QuotaExceededError') {
        this._gcFlashcards(true);
        try {
          if (typeof SafeStorage !== 'undefined') {
            sucesso = SafeStorage.setItem('it_progresso', this.estado.progresso);
          } else {
            localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
            sucesso = true;
          }
        } catch (_) {}
      } else {
        console.error('[AppState] Erro inesperado ao salvar progresso:', e);
      }
    }

    this._broadcastSync('it_progresso', this.estado.progresso);

    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.progresso) {
        sync.enfileirar('progress', 'update', 'current_progress', this.estado.progresso);
      }
    } catch (_) {}
    return sucesso;
  },

  /**
   * @returns {Record<string, any>}
   */
  carregarFlashcards() {
    try {
      const raw = (typeof SafeStorage !== 'undefined')
        ? SafeStorage.getItem('it_flashcards', {})
        : JSON.parse(localStorage.getItem('it_flashcards') || '{}');
      return this._sanitizeFlashcards(raw);
    } catch (e) {
      console.warn('[AppState] Falha ao carregar flashcards, iniciando vazio:', e);
    }
    return {};
  },

  salvarFlashcards() {
    if (!this.estado.flashcardData) return false;
    let sucesso = false;
    try {
      if (typeof SafeStorage !== 'undefined') {
        sucesso = SafeStorage.setItem('it_flashcards', this.estado.flashcardData);
      } else {
        localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData));
        sucesso = true;
      }
    } catch (e) {
      if ((typeof SafeStorage !== 'undefined' && SafeStorage.isQuotaExceeded(e)) || e.name === 'QuotaExceededError') {
        this._gcFlashcards(true);
        try {
          if (typeof SafeStorage !== 'undefined') {
            sucesso = SafeStorage.setItem('it_flashcards', this.estado.flashcardData);
          } else {
            localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData));
            sucesso = true;
          }
        } catch (_) {}
      } else {
        console.error('[AppState] Erro inesperado ao salvar flashcards:', e);
      }
    }

    this._broadcastSync('it_flashcards', this.estado.flashcardData);

    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.flashcardData) {
        sync.enfileirar('flashcards', 'update', 'current_deck', this.estado.flashcardData);
      }
    } catch (_) {}
    return sucesso;
  },

  _gcFlashcards(persistir = true) {
    const data = this.estado.flashcardData;
    if (!data || typeof data !== 'object') return 0;
    const agora = Date.now();
    const NOVENTA_DIAS = 90 * 24 * 3600 * 1000;
    let removidos = 0;
    let historyTruncated = 0;

    for (const id in data) {
      const f = data[id];
      if (!f || typeof f !== 'object') {
        delete data[id];
        removidos++;
        continue;
      }

      // 1. Remove suspended cards
      if (f.state === 'suspended') {
        delete data[id];
        removidos++;
        continue;
      }

      // 2. Remove obsolete cards (>90 days without review)
      if (f.lastReview && (agora - f.lastReview > NOVENTA_DIAS)) {
        delete data[id];
        removidos++;
        continue;
      }

      // 3. Remove obsolete new/unreviewed cards
      if (f.state === 'new' && f.lastReview && (agora - f.lastReview > NOVENTA_DIAS)) {
        delete data[id];
        removidos++;
        continue;
      }

      // 4. Compact unbounded review history array (keep last 5 entries)
      if (Array.isArray(f.history) && f.history.length > 5) {
        f.history = f.history.slice(-5);
        historyTruncated++;
      }
    }

    if (removidos > 0 || historyTruncated > 0) {
      console.info(`[GC] Flashcards otimizados: ${removidos} cards removidos, ${historyTruncated} históricos compactados.`);
      if (persistir) {
        try {
          const payload = JSON.stringify(data);
          if (typeof window !== 'undefined' && window.localStorage) {
            window.localStorage.setItem('it_flashcards', payload);
          } else if (typeof localStorage !== 'undefined') {
            localStorage.setItem('it_flashcards', payload);
          }
        } catch (err) {
          console.warn('[GC] Falha ao persistir flashcards podados no localStorage:', err);
        }
      }
    }
    return removidos + historyTruncated;
  },

  _ultimoAlertaArmazenamento: 0,

  _mostrarAlertaArmazenamento() {
    const agora = Date.now();
    if (this._ultimoAlertaArmazenamento && (agora - this._ultimoAlertaArmazenamento < 45000)) {
      return;
    }
    this._ultimoAlertaArmazenamento = agora;

    const msg = (typeof I18n !== 'undefined' && I18n.t)
      ? I18n.t('storage_cheio_alerta') || 'Atenção: Armazenamento local esgotado! Exporte seu backup nas configurações para não perder dados.'
      : 'Atenção: Armazenamento local esgotado! Exporte seu backup nas configurações para não perder dados.';

    if (typeof AppTTS !== 'undefined' && AppTTS.notificar) {
      AppTTS.notificar(msg, 'erro');
    } else if (typeof App !== 'undefined' && App.notificar) {
      App.notificar(msg, 'erro');
    } else if (typeof console !== 'undefined') {
      console.error('[Armazenamento]', msg);
    }
  },

  // ── Data loading (Stale-While-Revalidate) ──────────────────
  async carregarDados() {
    const novosTemplos = {};
    const novoVocab = [];
    const promises = [];
    // Load templo-1.json through templo-51.json; skip gracefully on 404
    for (let i = 1; i <= 51; i++) {
      promises.push(
        fetch(`data/templo-${i}.json`)
          .then(r => {
            if (!r.ok) return null;
            return r.json();
          })
          .then(data => {
            if (!data) return;
            // Normalize: JSON files use "vocabulario" or "palavras" — always expose as "palavras"
            const lista = data.palavras || data.vocabulario || [];
            data.palavras = lista.map(p => ({ ...p, templo_num: data.templo }));
            novoVocab.push(...data.palavras);
            novosTemplos[data.templo] = data;
          })
          .catch(err => {
            console.warn(`[App] Falha de rede ao carregar data/templo-${i}.json:`, err);
            return null;
          })
      );
    }

    // Load quiz questions
    promises.push(
      fetch('data/quizzes.json')
        .then(r => r.ok ? r.json() : { perguntas: [] })
        .then(data => {
          this.estado.quizData = data.perguntas || [];
        })
        .catch(err => {
          console.warn('[App] Falha ao carregar quizzes.json:', err);
          this.estado.quizData = [];
        })
    );

    // Load verb conjugations
    promises.push(
      fetch('data/conjugacoes.json')
        .then(r => r.ok ? r.json() : { verbos: [] })
        .then(data => {
          this.estado.conjugacoesData = data.verbos || [];
        })
        .catch(err => {
          console.warn('[App] Falha ao carregar conjugacoes.json:', err);
          this.estado.conjugacoesData = [];
        })
    );

    // Load grammar modules & exercises
    promises.push(
      fetch('data/grammar.json')
        .then(r => r.ok ? r.json() : { moduli: [] })
        .then(data => {
          this.estado.grammarData = data;
          if (typeof Grammar !== 'undefined' && !Grammar.dados) {
            Grammar.dados = data;
          }
          if (typeof SafeStorage !== 'undefined') {
            SafeStorage.setItem('it_swr_grammar', data);
          } else {
            try { localStorage.setItem('it_swr_grammar', JSON.stringify(data)); } catch (_) {}
          }
        })
        .catch(err => {
          console.warn('[App] Falha ao carregar grammar.json:', err);
          try {
            const cached = (typeof SafeStorage !== 'undefined')
              ? SafeStorage.getItem('it_swr_grammar', null)
              : JSON.parse(localStorage.getItem('it_swr_grammar') || 'null');
            this.estado.grammarData = (cached && typeof cached === 'object') ? cached : { moduli: [] };
          } catch (_) {
            this.estado.grammarData = { moduli: [] };
          }
        })
    );

    await Promise.all(promises);

    if (Object.keys(novosTemplos).length > 0) {
      this.estado.templosData = novosTemplos;
      this.estado.vocabCache = novoVocab;
      // Salva resumo leve de metadados para Stale-While-Revalidate instantâneo na próxima abertura
      try {
        const metaLeve = {};
        for (const [num, t] of Object.entries(novosTemplos)) {
          metaLeve[num] = {
            templo: t.templo,
            nome: t.nome,
            cidade: t.cidade,
            nivel: t.nivel,
            palavras: (t.palavras || []).map(p => ({
              id: p.id,
              italiano: p.italiano,
              portugues: p.portugues,
              audio_ipa: p.audio_ipa,
              categoria: p.categoria,
              exemplo: p.exemplo,
              exemplo_pt: p.exemplo_pt
            }))
          };
        }
        if (typeof SafeStorage !== 'undefined') {
          SafeStorage.setItem('it_swr_templos_meta', metaLeve);
        } else {
          localStorage.setItem('it_swr_templos_meta', JSON.stringify(metaLeve));
        }
      } catch (_) {}
    }

    // Injeta vocabulário customizado (via IA Import)
    try {
      const custom = (typeof SafeStorage !== 'undefined')
        ? SafeStorage.getItem('it_vocab_custom', [])
        : JSON.parse(localStorage.getItem('it_vocab_custom') || '[]');
      if (Array.isArray(custom) && custom.length) {
        custom.forEach(w => { if (!w.templo_num) w.templo_num = 0; });
        this.estado.vocabCache.unshift(...custom);
      }
    } catch (e) {}

    // Update total_palavras in progress
    if (this.estado.progresso) {
      this.estado.progresso.total_palavras = this.estado.vocabCache.length;
      this.salvarProgresso();
    }
  }
};

// Registro de handlers no Eviction Priority Ladder do SafeStorage
if (typeof SafeStorage !== 'undefined') {
  SafeStorage.registerEvictionHandler(3, 'flashcards_gc', () => {
    const freed = AppState._gcFlashcards(true);
    return freed > 0;
  });
  SafeStorage.registerEvictionHandler(4, 'toast_alert', () => {
    AppState._mostrarAlertaArmazenamento();
    return false;
  });
}

// Auto-inicialização de cross-tab sync e binding global
if (typeof window !== 'undefined') {
  window.AppState = AppState;
  try {
    AppState.initCrossTabSync();
  } catch (err) {
    console.warn('[AppState] Falha ao inicializar cross-tab sync:', err);
  }
}
if (typeof globalThis !== 'undefined') {
  globalThis.AppState = AppState;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppState;
}
