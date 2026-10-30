// ============================================================
// js/core/state.js — Global State & Persistence (ARC-02)
// ============================================================

const AppState = {
  // ── State ──────────────────────────────────────────────────
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
        const logs = JSON.parse(localStorage.getItem('it_client_errors') || '[]');
        logs.unshift(errorLog);
        localStorage.setItem('it_client_errors', JSON.stringify(logs.slice(0, 30)));
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
        const logs = JSON.parse(localStorage.getItem('it_client_errors') || '[]');
        logs.unshift(errorLog);
        localStorage.setItem('it_client_errors', JSON.stringify(logs.slice(0, 30)));
      } catch (_) {}
    });
  },

  // ── Stale-While-Revalidate helper for Templos & Vocab ──────
  _hidratarCacheLocal() {
    try {
      const raw = localStorage.getItem('it_swr_templos_meta');
      if (!raw) return false;
      const meta = JSON.parse(raw);
      if (!meta || typeof meta !== 'object') return false;
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

  // ── localStorage ───────────────────────────────────────────
  carregarProgresso() {
    try {
      const raw = localStorage.getItem('it_progresso');
      if (raw) {
        const p = JSON.parse(raw);
        // Backward compatibility
        if (!p.grammatica_completadas) p.grammatica_completadas = [];
        if (p.meta_diaria === undefined) p.meta_diaria = 100;
        if (p.xp_hoje === undefined) p.xp_hoje = 0;
        if (p.data_xp_hoje === undefined) p.data_xp_hoje = null;
        if (!p.favoritos)   p.favoritos   = [];
        if (!p.conquistas)  p.conquistas  = [];
        if (!p.data_inicio) p.data_inicio = p.ultimo_estudo || Date.now();
        if (p.meta_prazo === undefined) p.meta_prazo = null;
        if (p.audio_rate === undefined) p.audio_rate = 0.85;
        return p;
      }
    } catch (e) { /* ignore */ }
    // Default state
    return {
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
      favoritos:   [],
      conquistas:  [],
      data_inicio: Date.now(),
      meta_prazo: null,
      audio_rate: 0.85
    };
  },

  salvarProgresso() {
    try {
      localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        this._gcFlashcards();
        try { localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso)); } catch (_) {}
      }
    }
    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.progresso) {
        sync.enfileirar('progress', 'update', 'current_progress', this.estado.progresso);
      }
    } catch (_) {}
  },

  carregarFlashcards() {
    try {
      const raw = localStorage.getItem('it_flashcards');
      if (raw) return JSON.parse(raw);
    } catch (e) { /* ignore */ }
    return {};
  },

  salvarFlashcards() {
    try {
      localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        this._gcFlashcards();
        try { localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData)); } catch (_) {}
      }
    }
    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.flashcardData) {
        sync.enfileirar('flashcards', 'update', 'current_deck', this.estado.flashcardData);
      }
    } catch (_) {}
  },

  _gcFlashcards() {
    const data = this.estado.flashcardData;
    if (!data) return;
    const agora = Date.now();
    const NOVENTA_DIAS = 90 * 24 * 3600 * 1000;
    let removidos = 0;
    for (const id in data) {
      const f = data[id];
      if (f.state === 'suspended' || (f.lastReview && agora - f.lastReview > NOVENTA_DIAS && f.state === 'new')) {
        delete data[id];
        removidos++;
      }
    }
    if (removidos > 0) console.info(`[GC] Flashcards removidos do cache: ${removidos}`);
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
          try { localStorage.setItem('it_swr_grammar', JSON.stringify(data)); } catch (_) {}
        })
        .catch(err => {
          console.warn('[App] Falha ao carregar grammar.json:', err);
          try {
            const cached = localStorage.getItem('it_swr_grammar');
            this.estado.grammarData = cached ? JSON.parse(cached) : { moduli: [] };
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
        localStorage.setItem('it_swr_templos_meta', JSON.stringify(metaLeve));
      } catch (_) {}
    }

    // Injeta vocabulário customizado (via IA Import)
    try {
      const custom = JSON.parse(localStorage.getItem('it_vocab_custom') || '[]');
      if (custom.length) {
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

if (typeof globalThis !== 'undefined') {
  globalThis.AppState = AppState;
}
if (typeof window !== 'undefined') {
  window.AppState = AppState;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppState;
}
