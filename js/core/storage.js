// ============================================================
// js/core/storage.js — SafeStorage Gateway & Quota Eviction (F1, F2, F4)
// ============================================================

const SafeStorage = {
  // In-memory fallback if localStorage is disabled or completely blocked
  _memoryFallback: {},
  _isAvailable: null,
  _evictionHandlers: [],

  // Known disposable cache keys for Step 1
  SWR_KEYS: [
    'it_swr_templos_meta',
    'it_swr_grammar',
    'it_swr_canzoni',
    'it_swr_dialogi',
    'it_swr_storie',
    'it_swr_imitazioni'
  ],

  // Known disposable log keys for Step 2
  LOG_KEYS: [
    'it_client_errors'
  ],

  /**
   * Tests whether localStorage is accessible and writable.
   * @returns {boolean}
   */
  isStorageAvailable() {
    if (this._isAvailable !== null) return this._isAvailable;
    try {
      if (typeof window === 'undefined' || !window.localStorage) {
        this._isAvailable = false;
        return false;
      }
      const testKey = '__storage_probe__';
      window.localStorage.setItem(testKey, '1');
      window.localStorage.removeItem(testKey);
      this._isAvailable = true;
      return true;
    } catch (e) {
      if (this.isQuotaExceeded(e)) {
        this._isAvailable = true;
        return true;
      }
      this._isAvailable = false;
      return false;
    }
  },

  /**
   * Universal QuotaExceededError detector across all browser engines.
   * @param {any} e - The caught exception.
   * @returns {boolean}
   */
  isQuotaExceeded(e) {
    if (!e) return false;
    return (
      e.name === 'QuotaExceededError' ||
      e.name === 'NS_ERROR_DOM_QUOTA_REACHED' ||
      e.code === 22 ||
      e.code === 1014 ||
      (typeof e.number === 'number' && ((e.number & 0xFFFF) === 0x70 || e.number === -2147024882)) ||
      (typeof e.message === 'string' && (
        e.message.includes('QuotaExceededError') ||
        e.message.includes('quota') ||
        e.message.includes('NS_ERROR_DOM_QUOTA_REACHED') ||
        e.message.toLowerCase().includes('storage full') ||
        e.message.toLowerCase().includes('quota exceeded')
      ))
    );
  },

  /**
   * Registers a custom eviction callback into the ladder.
   * @param {number} priority - Priority level (1: SWR, 2: Logs, 3: Flashcard GC, 4: Alerts)
   * @param {string} name - Handler identifier
   * @param {Function} handler - Function returning boolean (true if space was freed)
   */
  registerEvictionHandler(priority, name, handler) {
    this._evictionHandlers.push({ priority, name, handler });
    this._evictionHandlers.sort((a, b) => a.priority - b.priority);
  },

  /**
   * Reads and parses a key safely from localStorage with a fallback.
   * Handles JSON parsing and falls back to raw string or fallback value on error.
   * @param {string} key
   * @param {any} fallback
   * @returns {any}
   */
  getItem(key, fallback = null) {
    if (!this.isStorageAvailable()) {
      return Object.prototype.hasOwnProperty.call(this._memoryFallback, key)
        ? this._memoryFallback[key]
        : fallback;
    }
    try {
      const raw = window.localStorage.getItem(key);
      if (raw === null || raw === undefined) return fallback;
      try {
        return JSON.parse(raw);
      } catch (_) {
        // Return raw string for legacy unquoted values
        return raw;
      }
    } catch (err) {
      console.warn(`[SafeStorage] Erro ao ler '${key}':`, err);
      return fallback;
    }
  },

  /**
   * Persists a key-value pair to localStorage with automatic JSON serialization
   * and automated Eviction Priority Ladder on quota exhaustion.
   * @param {string} key
   * @param {any} value
   * @returns {boolean} True if successfully stored, false otherwise.
   */
  setItem(key, value) {
    const serialized = (typeof value === 'string') ? value : JSON.stringify(value);

    if (!this.isStorageAvailable()) {
      this._memoryFallback[key] = (typeof value === 'string') ? value : JSON.parse(serialized);
      return true;
    }

    try {
      window.localStorage.setItem(key, serialized);
      return true;
    } catch (err) {
      if (!this.isQuotaExceeded(err)) {
        console.error(`[SafeStorage] Falha não relacionada a quota ao gravar '${key}':`, err);
        return false;
      }

      console.warn(`[SafeStorage] QuotaExceededError detectado ao gravar '${key}'. Executando Eviction Ladder...`);
      return this._executeEvictionLadder(key, serialized);
    }
  },

  /**
   * Safely removes an item from storage.
   * @param {string} key
   */
  removeItem(key) {
    if (!this.isStorageAvailable()) {
      delete this._memoryFallback[key];
      return;
    }
    try {
      window.localStorage.removeItem(key);
    } catch (err) {
      console.warn(`[SafeStorage] Erro ao remover '${key}':`, err);
    }
  },

  /**
   * Removes all keys matching an optional prefix.
   * @param {string} prefix
   */
  clear(prefix = '') {
    if (!this.isStorageAvailable()) {
      if (!prefix) {
        this._memoryFallback = {};
      } else {
        Object.keys(this._memoryFallback).forEach(k => {
          if (k.startsWith(prefix)) delete this._memoryFallback[k];
        });
      }
      return;
    }
    try {
      if (!prefix) {
        window.localStorage.clear();
      } else {
        const toRemove = [];
        for (let i = 0; i < window.localStorage.length; i++) {
          const k = window.localStorage.key(i);
          if (k && k.startsWith(prefix)) toRemove.push(k);
        }
        toRemove.forEach(k => window.localStorage.removeItem(k));
      }
    } catch (err) {
      console.warn('[SafeStorage] Erro ao limpar storage:', err);
    }
  },

  /**
   * Returns list of keys matching prefix.
   * @param {string} prefix
   * @returns {string[]}
   */
  keys(prefix = '') {
    if (!this.isStorageAvailable()) {
      return Object.keys(this._memoryFallback).filter(k => !prefix || k.startsWith(prefix));
    }
    const result = [];
    try {
      for (let i = 0; i < window.localStorage.length; i++) {
        const k = window.localStorage.key(i);
        if (k && (!prefix || k.startsWith(prefix))) result.push(k);
      }
    } catch (_) {}
    return result;
  },

  /**
   * Estimates approximate bytes consumed in localStorage.
   * @returns {number}
   */
  getStorageUsage() {
    if (!this.isStorageAvailable()) return 0;
    let bytes = 0;
    try {
      for (let i = 0; i < window.localStorage.length; i++) {
        const k = window.localStorage.key(i);
        if (k) {
          const v = window.localStorage.getItem(k) || '';
          bytes += (k.length + v.length) * 2;
        }
      }
    } catch (_) {}
    return bytes;
  },

  /**
   * Orchestrates the 4-step Eviction Priority Ladder upon QuotaExceededError.
   * @private
   */
  _executeEvictionLadder(targetKey, serializedValue) {
    // ── Step 1: Evict ephemeral SWR network caches ─────────────
    let bytesFreedStep1 = 0;
    const allKeys = this.keys();
    for (const k of allKeys) {
      if (k.startsWith('it_swr_') || this.SWR_KEYS.includes(k)) {
        try {
          const val = window.localStorage.getItem(k) || '';
          bytesFreedStep1 += (k.length + val.length) * 2;
          window.localStorage.removeItem(k);
        } catch (_) {}
      }
    }
    if (bytesFreedStep1 > 0) {
      console.info(`[SafeStorage/Ladder] Step 1 concluído: liberados ~${Math.round(bytesFreedStep1 / 1024)} KB de caches SWR.`);
      try {
        window.localStorage.setItem(targetKey, serializedValue);
        return true;
      } catch (e) {
        if (!this.isQuotaExceeded(e)) return false;
      }
    }

    // ── Step 2: Evict client error logs and transient keys ─────
    let bytesFreedStep2 = 0;
    for (const k of this.LOG_KEYS) {
      try {
        const val = window.localStorage.getItem(k) || '';
        bytesFreedStep2 += (k.length + val.length) * 2;
        window.localStorage.removeItem(k);
      } catch (_) {}
    }
    for (const k of this.keys()) {
      if (k.startsWith('it_import_stage_') || k.startsWith('it_stage_') || k.startsWith('it_temp_')) {
        try {
          const val = window.localStorage.getItem(k) || '';
          bytesFreedStep2 += (k.length + val.length) * 2;
          window.localStorage.removeItem(k);
        } catch (_) {}
      }
    }
    if (bytesFreedStep2 > 0) {
      console.info(`[SafeStorage/Ladder] Step 2 concluído: liberados ~${Math.round(bytesFreedStep2 / 1024)} KB de logs e staging.`);
      try {
        window.localStorage.setItem(targetKey, serializedValue);
        return true;
      } catch (e) {
        if (!this.isQuotaExceeded(e)) return false;
      }
    }

    // ── Step 3: Run custom registered handlers (Flashcards GC, etc.) ─
    for (const h of this._evictionHandlers) {
      if (h.priority <= 3) {
        try {
          const freed = h.handler();
          if (freed) {
            console.info(`[SafeStorage/Ladder] Handler '${h.name}' executado com sucesso.`);
            try {
              window.localStorage.setItem(targetKey, serializedValue);
              return true;
            } catch (e) {
              if (!this.isQuotaExceeded(e)) return false;
            }
          }
        } catch (err) {
          console.warn(`[SafeStorage/Ladder] Erro ao executar handler '${h.name}':`, err);
        }
      }
    }

    // ── Step 4: Storage still exhausted — notify user via alert handlers ──
    console.error(`[SafeStorage/Ladder] Armazenamento completamente esgotado ao tentar gravar '${targetKey}'. Disparando alertas.`);
    for (const h of this._evictionHandlers) {
      if (h.priority >= 4) {
        try {
          h.handler();
        } catch (err) {
          console.warn(`[SafeStorage/Ladder] Erro ao disparar alerta '${h.name}':`, err);
        }
      }
    }

    return false;
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.SafeStorage = SafeStorage;
}
if (typeof window !== 'undefined') {
  window.SafeStorage = SafeStorage;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SafeStorage;
}
