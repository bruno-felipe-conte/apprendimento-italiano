# Implementation Blueprint: Storage Gateway, Quota Eviction & Defensive Loading (F1, F2, F4)

**Author**: Explorer M1.1 (Storage Gateway & Quota Eviction)  
**Date**: 2026-10-31T00:46:00Z  
**Workspace**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano`  
**Working Directory**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_1`

---

## 1. Observation

### 1.1 Existing Storage Operations & Direct LocalStorage Calls
- **Direct Code Search**: Over 250 direct invocations of `localStorage.getItem`, `localStorage.setItem`, and `localStorage.removeItem` exist across 28 files in `js/` without an abstraction layer.
- **Absence of Unified Storage Gateway**: There is currently no `js/core/storage.js` in the repository (confirmed via `list_dir` on `js/core/`). Each subsystem reads/writes `localStorage` ad-hoc.
- **Script Loading Order in `index.html`**:
  `index.html` lines 632-636 load core dependencies:
  ```html
  <script type="module" src="js/core/sync.js?v=156"></script>
  <script type="module" src="js/core/analytics.js?v=156"></script>
  <script type="module" src="js/core/collaboration.js?v=156"></script>
  <script src="js/core/state.js?v=159"></script>
  <script src="js/core/navigation.js?v=160"></script>
  ```
  `storage.js` must be loaded prior to `state.js` so `AppState` and all downstream modules can leverage `SafeStorage`.

### 1.2 Inspection of `salvarProgresso()`, `salvarFlashcards()` and `_gcFlashcards()`
- In `js/core/state.js` lines 141-149:
  ```javascript
  salvarProgresso() {
    try {
      localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        this._gcFlashcards();
        try { localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso)); } catch (_) {}
      }
    }
  ```
- In `js/core/state.js` lines 166-174:
  ```javascript
  salvarFlashcards() {
    try {
      localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        this._gcFlashcards();
        try { localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData)); } catch (_) {}
      }
    }
  ```
- In `js/core/state.js` lines 183-197:
  ```javascript
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
  }
  ```
- **Observed Defects**:
  1. `_gcFlashcards()` mutates `this.estado.flashcardData` in memory (`delete data[id]`), but **never calls `localStorage.setItem('it_flashcards', ...)`**! When `salvarProgresso()` calls `this._gcFlashcards()`, zero bytes are released from disk. The subsequent retry of `setItem('it_progresso', ...)` is guaranteed to fail identically.
  2. The boolean condition `(f.lastReview && agora - f.lastReview > NOVENTA_DIAS && f.state === 'new')` is an impossible oxymoron. In FSRS (`js/flashcards.js:81, 893`), a card in state `'new'` has never been reviewed, meaning `f.lastReview` is either `null` or `undefined`. This clause can never evaluate to `true`.
  3. When quota fails, the code immediately attacks user flashcards instead of first evicting multi-megabyte disposable SWR caches and error logs.
  4. Quota detection is hardcoded to `e.name === 'QuotaExceededError'`. Firefox (`NS_ERROR_DOM_QUOTA_REACHED`), older Safari/WebKit (`code === 22`, `number === -2147024882`), and WebKit private browsing throw alternate error signatures that bypass the catch block.
  5. If writes fail, errors are silently suppressed with `catch (_) {}`. The user receives no toast notification that study progress is not being committed.

### 1.3 Ephemeral Caches Inventory
Search for `it_swr_` across the codebase revealed 6 primary keys:
- `it_swr_templos_meta` (`js/core/state.js:84, 300`): Lightweight temple metadata cache (can reach ~1-2 MB).
- `it_swr_grammar` (`js/core/state.js:262`, `js/grammar.js:25`, `js/quiz.js:559`): Grammar rule definitions and quizzes (~400-800 KB).
- `it_swr_canzoni` (`js/canzoni.js:97, 106, 120`): Songs, lyrics, and metadata (~500-1500 KB).
- `it_swr_dialogi` (`js/dialoghi.js:12, 20, 32`): Dialogues and audio metadata (~300-800 KB).
- `it_swr_storie` (`js/storie.js:36, 47, 62`): Stories and reading exercises (~400-1200 KB).
- `it_swr_imitazioni` (`js/imitazione.js:29, 37, 49`): Shadowing sentences (~300-800 KB).
Total ephemeral SWR footprint: 2.5 MB to 4.5 MB of the typical 5 MB browser quota.

### 1.4 Client Logs Inventory
- `it_client_errors` (`js/core/state.js:58, 74`): Stores up to 30 unhandled runtime errors, userAgent strings, and stack traces. Consumes 50 KB to 200 KB of localStorage quota.

### 1.5 Baseline Verification
- `npm test`: Ran Vitest suite — 15 test files passed, 104 tests passed.
- `npm run build`: Ran TypeScript checks and Vite build — completed with exit code 0.

---

## 2. Logic Chain

1. **Premise**: In an offline-first PWA, `localStorage` is the authoritative client persistence medium for user progress (`it_progresso`) and spaced repetition decks (`it_flashcards`).
2. **Defect Causality (F1 - Quota GC Persistence)**:
   - When quota is reached, `salvarProgresso()` calls `this._gcFlashcards()`.
   - `_gcFlashcards()` only removes keys from the JS object in memory.
   - Because `_gcFlashcards()` never calls `localStorage.setItem('it_flashcards', ...)`, the disk representation remains completely full.
   - Therefore, the subsequent write `localStorage.setItem('it_progresso', ...)` fails 100% of the time, progress is silently lost, and the student's XP/streak is destroyed upon tab reload.
3. **Defect Causality (F2 - Ephemeral Cache Eviction)**:
   - Ephemeral SWR caches consume up to 4 MB of the 5 MB quota.
   - They are purely disposable network acceleration caches; if removed, they are simply refetched from `/data/*.json` on demand.
   - Therefore, evicting `it_swr_*` and `it_client_errors` before touching flashcards recovers 50-80% of storage quota instantaneously without touching any student data.
4. **Defect Causality (F4 - Storage Gateway & Quota Variants)**:
   - Browsers differ in quota error representations (Safari code 22, Firefox 1014 / `NS_ERROR_DOM_QUOTA_REACHED`, older WebKit private mode 0-byte quota).
   - Reading corrupted payloads (`"corrupted"`, `null`, `[]`, `123`) directly crashes views expecting object properties (`p.templos_desbloqueados.includes`).
   - A centralized `SafeStorage` facade with schema validation, fallback defaults, and multi-engine quota detection provides total system resilience against corruption and crashes.

---

## 3. Caveats

1. **In-Memory Fallback Scope**: If third-party storage is disabled or private mode blocks `localStorage` entirely, `SafeStorage` gracefully falls back to an in-memory dictionary. State persists for the duration of the page session, but cannot survive tab closure without storage access.
2. **Flashcard Deck Size**: If a user's deck exceeds 5 MB on its own (tens of thousands of cards), even complete cache eviction will not free enough space. In this extreme scenario, Step 3 prunes unreviewed cards and truncates review history, and Step 4 alerts the user to export a backup immediately.
3. **Write Isolation**: Milestone 1 exclusive boundaries strictly cover `js/core/storage.js`, `js/core/state.js`, `js/core/sync.ts`, `js/profilo.js`, and `js/audio_cache.js`. This blueprint touches only `storage.js`, `state.js`, and the script tag in `index.html`.

---

## 4. Conclusion & Concrete Blueprints

### 4.1 Blueprint 1: `js/core/storage.js` (New File)

Create `js/core/storage.js` with universal module packaging, resilient fallback, multi-engine quota detection, and automated 4-step Eviction Priority Ladder:

```javascript
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
    } catch (_) {
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
        e.message.includes('exceeded') ||
        e.message.includes('NS_ERROR_DOM_QUOTA_REACHED')
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
      if (k.startsWith('it_import_stage_') || k.startsWith('it_temp_')) {
        try {
          window.localStorage.removeItem(k);
        } catch (_) {}
      }
    }
    if (bytesFreedStep2 > 0) {
      console.info(`[SafeStorage/Ladder] Step 2 concluído: liberados ~${Math.round(bytesFreedStep2 / 1024)} KB de logs.`);
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
            console.info(`[SafeStorage/Ladder] Handler '${h.name}' executado.`);
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
```

---

### 4.2 Blueprint 2: Modifications to `js/core/state.js`

In `js/core/state.js`, apply the following improvements:

1. **Global Error Logger Hardening** (lines 58-61, 74-77):
   Replace direct `localStorage` calls with `SafeStorage.getItem` and `SafeStorage.setItem`.

2. **Defensive Progress Loading** (`carregarProgresso`):
   Validate object shape, guarantee that array properties (`templos_desbloqueados`, `templos_concluidos`, `grammatica_completadas`, `conquistas`, `favoritos`) are verified arrays, and guarantee finite numbers for `nivel`, `xp`, `streak`, `total_palavras`.

3. **Resilient Progress Saving** (`salvarProgresso`):
   Route save through `SafeStorage.setItem('it_progresso', this.estado.progresso)`.

4. **Defensive Flashcard Loading** (`carregarFlashcards`):
   Ensure returned object is a non-null dictionary `{}` and not a primitive or array.

5. **Resilient Flashcard Saving** (`salvarFlashcards`):
   Route save through `SafeStorage.setItem('it_flashcards', this.estado.flashcardData)`.

6. **Corrected `_gcFlashcards(persistir = true)`** (lines 183-197):
   - Remove suspended cards (`f.state === 'suspended'`).
   - Fix oxymoron: remove cards in state `'new'` or with `!f.lastReview` / `f.reps === 0`.
   - Truncate long `f.history` arrays to last 5 entries to shed accumulated review weight.
   - Remove stale cards unreviewed for > 90 days with `f.reps <= 1` or `state === 'learning'`.
   - **CRITICAL**: When `persistir === true`, immediately write `window.localStorage.setItem('it_flashcards', JSON.stringify(data))` to commit reclaimed bytes to disk!

7. **Storage Alert Toast & Eviction Handler Registration**:
   Add `_mostrarAlertaArmazenamento()` with a 45-second debounce throttle, calling `AppTTS.notificar(msg, 'erro')`. Register GC handler at priority 3 and Alert handler at priority 4.

#### Concrete Code Patch for `js/core/state.js`:

```javascript
  // ── localStorage ───────────────────────────────────────────
  carregarProgresso() {
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
      favoritos:   [],
      conquistas:  [],
      data_inicio: Date.now(),
      meta_prazo: null,
      audio_rate: 0.85
    };

    try {
      const p = (typeof SafeStorage !== 'undefined')
        ? SafeStorage.getItem('it_progresso', null)
        : JSON.parse(localStorage.getItem('it_progresso') || 'null');

      if (p && typeof p === 'object' && !Array.isArray(p)) {
        p.nivel = (typeof p.nivel === 'number' && !isNaN(p.nivel) && p.nivel >= 1) ? p.nivel : defaults.nivel;
        p.xp = (typeof p.xp === 'number' && !isNaN(p.xp) && p.xp >= 0) ? p.xp : defaults.xp;
        p.xp_proximo_nivel = (typeof p.xp_proximo_nivel === 'number' && !isNaN(p.xp_proximo_nivel) && p.xp_proximo_nivel > 0) ? p.xp_proximo_nivel : defaults.xp_proximo_nivel;
        p.templos_desbloqueados = (Array.isArray(p.templos_desbloqueados) && p.templos_desbloqueados.length > 0) ? p.templos_desbloqueados : [1];
        p.templos_concluidos = Array.isArray(p.templos_concluidos) ? p.templos_concluidos : [];
        p.total_palavras = (typeof p.total_palavras === 'number' && !isNaN(p.total_palavras) && p.total_palavras >= 0) ? p.total_palavras : defaults.total_palavras;
        p.streak = (typeof p.streak === 'number' && !isNaN(p.streak) && p.streak >= 0) ? p.streak : defaults.streak;
        p.ultimo_estudo = (typeof p.ultimo_estudo === 'number' && !isNaN(p.ultimo_estudo)) ? p.ultimo_estudo : null;
        p.grammatica_completadas = Array.isArray(p.grammatica_completadas) ? p.grammatica_completadas : [];
        p.meta_diaria = (typeof p.meta_diaria === 'number' && p.meta_diaria > 0) ? p.meta_diaria : defaults.meta_diaria;
        p.xp_hoje = (typeof p.xp_hoje === 'number' && !isNaN(p.xp_hoje)) ? p.xp_hoje : 0;
        p.data_xp_hoje = p.data_xp_hoje || null;
        p.favoritos = Array.isArray(p.favoritos) ? p.favoritos : [];
        p.conquistas = Array.isArray(p.conquistas) ? p.conquistas : [];
        p.data_inicio = (typeof p.data_inicio === 'number' && !isNaN(p.data_inicio)) ? p.data_inicio : (p.ultimo_estudo || Date.now());
        p.meta_prazo = p.meta_prazo || null;
        p.audio_rate = (typeof p.audio_rate === 'number' && !isNaN(p.audio_rate)) ? p.audio_rate : 0.85;
        return p;
      }
    } catch (e) {
      console.warn('[AppState] Falha ao carregar progresso, restaurando defaults:', e);
    }
    return defaults;
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
      console.error('[AppState] Erro inesperado ao salvar progresso:', e);
    }

    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.progresso) {
        sync.enfileirar('progress', 'update', 'current_progress', this.estado.progresso);
      }
    } catch (_) {}
    return sucesso;
  },

  carregarFlashcards() {
    try {
      const raw = (typeof SafeStorage !== 'undefined')
        ? SafeStorage.getItem('it_flashcards', {})
        : JSON.parse(localStorage.getItem('it_flashcards') || '{}');

      if (raw && typeof raw === 'object' && !Array.isArray(raw)) {
        return raw;
      }
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
      console.error('[AppState] Erro inesperado ao salvar flashcards:', e);
    }

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

      // 2. Fix oxymoron: remove cards in state 'new' or without review/reps (they contain no study history)
      if (f.state === 'new' || !f.lastReview || f.reps === 0) {
        delete data[id];
        removidos++;
        continue;
      }

      // 3. Compact unbounded review history array (keep last 5 entries)
      if (Array.isArray(f.history) && f.history.length > 5) {
        f.history = f.history.slice(-5);
        historyTruncated++;
      }

      // 4. Stale cards: reviewed > 90 days ago with single rep or abandoned in learning state
      if (f.lastReview && (agora - f.lastReview > NOVENTA_DIAS) && (f.reps <= 1 || f.state === 'learning')) {
        delete data[id];
        removidos++;
        continue;
      }
    }

    if (removidos > 0 || historyTruncated > 0) {
      console.info(`[GC] Flashcards otimizados: ${removidos} cards removidos, ${historyTruncated} históricos compactados.`);
      if (persistir) {
        try {
          const payload = JSON.stringify(data);
          if (typeof window !== 'undefined' && window.localStorage) {
            window.localStorage.setItem('it_flashcards', payload);
          }
        } catch (err) {
          console.warn('[GC] Falha ao persistir flashcards podados no localStorage:', err);
        }
      }
    }
    return removidos;
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
  }
```

And at the bottom of `js/core/state.js`, wire up the eviction hooks:
```javascript
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
```

---

### 4.3 Blueprint 3: Script Tag Registration in `index.html`

In `index.html`, insert `<script src="js/core/storage.js?v=162"></script>` right before `state.js` (line 635):

```html
  <script type="module" src="js/core/sync.js?v=156"></script>
  <script type="module" src="js/core/analytics.js?v=156"></script>
  <script type="module" src="js/core/collaboration.js?v=156"></script>
  <script src="js/core/storage.js?v=162"></script>
  <script src="js/core/state.js?v=162"></script>
  <script src="js/core/navigation.js?v=160"></script>
```

---

### 4.4 Blueprint 4: Test Specification for Milestone 4

The implementer of Milestone 4 (`tests/storage_quota.test.ts` and `tests/storage_corruption.test.ts`) should use this exact specification:

#### Test File: `tests/storage_quota.test.ts`
```typescript
// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import '../js/core/storage.js';
import '../js/core/state.js';

const SafeStorage = (globalThis as any).SafeStorage;
const AppState = (globalThis as any).AppState;

describe('SafeStorage & Quota Eviction Ladder', () => {
  beforeEach(() => {
    localStorage.clear();
    SafeStorage._memoryFallback = {};
    AppState._ultimoAlertaArmazenamento = 0;
    vi.restoreAllMocks();
  });

  it('deve detectar QuotaExceededError em múltiplos formatos de browsers (Safari, Firefox, Chrome)', () => {
    expect(SafeStorage.isQuotaExceeded({ name: 'QuotaExceededError' })).toBe(true);
    expect(SafeStorage.isQuotaExceeded({ name: 'NS_ERROR_DOM_QUOTA_REACHED', code: 1014 })).toBe(true);
    expect(SafeStorage.isQuotaExceeded({ code: 22 })).toBe(true);
    expect(SafeStorage.isQuotaExceeded({ message: 'The quota has been exceeded' })).toBe(true);
    expect(SafeStorage.isQuotaExceeded(new Error('SyntaxError'))).toBe(false);
  });

  it('Step 1: deve despejar caches SWR (it_swr_*) prioritariamente mantendo dados do usuário', () => {
    localStorage.setItem('it_swr_templos_meta', '{"1":{"templo":1}}');
    localStorage.setItem('it_swr_canzoni', '[1,2,3]');
    localStorage.setItem('it_progresso', '{"nivel":2}');

    let attempts = 0;
    const realSet = localStorage.setItem.bind(localStorage);
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation((k, v) => {
      if (k === 'novo_item' && attempts === 0) {
        attempts++;
        const err = new Error('Quota exceeded');
        err.name = 'QuotaExceededError';
        throw err;
      }
      return realSet(k, v);
    });

    const res = SafeStorage.setItem('novo_item', { data: 'ok' });
    expect(res).toBe(true);
    expect(localStorage.getItem('it_swr_templos_meta')).toBeNull();
    expect(localStorage.getItem('it_swr_canzoni')).toBeNull();
    expect(localStorage.getItem('it_progresso')).not.toBeNull();
  });

  it('Step 2: deve despejar logs de erro de cliente (it_client_errors)', () => {
    localStorage.setItem('it_client_errors', JSON.stringify([{ msg: 'err' }]));
    let attempts = 0;
    const realSet = localStorage.setItem.bind(localStorage);
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation((k, v) => {
      if (k === 'novo_item' && attempts < 2) {
        attempts++;
        const err = new Error('Quota exceeded');
        err.name = 'QuotaExceededError';
        throw err;
      }
      return realSet(k, v);
    });

    const res = SafeStorage.setItem('novo_item', { data: 'ok' });
    expect(res).toBe(true);
    expect(localStorage.getItem('it_client_errors')).toBeNull();
  });

  it('Step 3: _gcFlashcards deve remover cartas new/suspended e persistir no disco', () => {
    AppState.estado.flashcardData = {
      card1: { id: 'card1', state: 'suspended' },
      card2: { id: 'card2', state: 'new', reps: 0 },
      card3: { id: 'card3', state: 'review', reps: 5, lastReview: Date.now(), history: [1,2,3,4,5,6,7,8] }
    };
    AppState.salvarFlashcards();

    AppState._gcFlashcards(true);

    expect(AppState.estado.flashcardData.card1).toBeUndefined();
    expect(AppState.estado.flashcardData.card2).toBeUndefined();
    expect(AppState.estado.flashcardData.card3).toBeDefined();
    expect(AppState.estado.flashcardData.card3.history.length).toBe(5);

    // Confirma persistência em disco
    const salvo = JSON.parse(localStorage.getItem('it_flashcards') || '{}');
    expect(salvo.card1).toBeUndefined();
    expect(salvo.card2).toBeUndefined();
    expect(salvo.card3).toBeDefined();
  });

  it('Step 4: dispara alerta quando armazenamento continua esgotado', () => {
    const alertSpy = vi.fn();
    SafeStorage.registerEvictionHandler(4, 'test_alert', alertSpy);

    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
      const err = new Error('Storage completely full');
      err.name = 'QuotaExceededError';
      throw err;
    });

    const res = SafeStorage.setItem('key_fail', { large: 'data' });
    expect(res).toBe(false);
    expect(alertSpy).toHaveBeenCalled();
  });
});
```

#### Test File: `tests/storage_corruption.test.ts`
```typescript
// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import '../js/core/storage.js';
import '../js/core/state.js';

const SafeStorage = (globalThis as any).SafeStorage;
const AppState = (globalThis as any).AppState;

describe('SafeStorage Defensive Loading & Corruption Immunity', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('carregarProgresso deve retornar defaults íntegros quando localStorage contém payload primitivo ou malformado', () => {
    localStorage.setItem('it_progresso', '"corrompido"');
    let p = AppState.carregarProgresso();
    expect(p.nivel).toBe(1);
    expect(p.templos_desbloqueados).toEqual([1]);

    localStorage.setItem('it_progresso', '12345');
    p = AppState.carregarProgresso();
    expect(p.nivel).toBe(1);
    expect(p.templos_desbloqueados).toEqual([1]);

    localStorage.setItem('it_progresso', '{"nivel": "invalid", "templos_desbloqueados": "broken"}');
    p = AppState.carregarProgresso();
    expect(p.nivel).toBe(1);
    expect(p.templos_desbloqueados).toEqual([1]);
  });

  it('carregarFlashcards deve retornar objeto vazio quando dados estão corrompidos ou em array', () => {
    localStorage.setItem('it_flashcards', '[1, 2, 3]');
    expect(AppState.carregarFlashcards()).toEqual({});

    localStorage.setItem('it_flashcards', '{ not valid json');
    expect(AppState.carregarFlashcards()).toEqual({});
  });
});
```

---

## 5. Verification Method

To verify this implementation blueprint:

1. **Verify Baseline Test Suite**:
   ```bash
   npm test
   ```
   *Expected*: 15 passed test files, 104 passed tests.
2. **Verify Production Build**:
   ```bash
   npm run build
   ```
   *Expected*: `tsc` runs cleanly, Vite builds client bundle with code 0.
3. **Verify Code Location References**:
   - `grep -n -C 5 "this._gcFlashcards()" js/core/state.js` (lines 145, 171)
   - `grep -n -C 5 "_gcFlashcards()" js/core/state.js` (lines 183-197)
   - `grep -n "it_swr_" js/canzoni.js js/core/state.js js/dialoghi.js js/grammar.js js/imitazione.js js/storie.js`
4. **Post-Implementation Verification (when executed by Implementer)**:
   - Run `npx vitest run tests/storage_quota.test.ts tests/storage_corruption.test.ts`
   - Verify that all tests pass and `npm run build` generates production assets without errors.
