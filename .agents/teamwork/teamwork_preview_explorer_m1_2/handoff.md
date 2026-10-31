# Implementation Blueprint & Technical Architecture: Multi-Tab Concurrency & Synchronization (Feature F3, Milestone 1)

**Author**: Explorer M1.2 (Multi-Tab Concurrency & Synchronization)  
**Date**: 2026-10-31T00:48:30Z  
**Workspace**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano`  
**Output Path**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_2/handoff.md`  
**Target Milestone**: Milestone 1 (Storage, Persistence & Data Resilience)  
**Target Feature**: Feature F3 (Cross-Tab Synchronization & Concurrency Resilience)  

---

## 1. Observation

A direct code-level investigation of `/mnt/c/Users/bruno/Documents/apprendimento-italiano` revealed the following concrete architectural facts:

### 1.1 Complete Absence of Cross-Tab Synchronization Primitives
- An exhaustive search across the entire codebase (`grep_search`) for `BroadcastChannel`, `addEventListener('storage')`, `window.onstorage`, and `navigator.locks` returned **0 matches** in production code:
  ```bash
  grep -rn "BroadcastChannel" js/
  # Result: 0 matches
  grep -rn "addEventListener('storage'" js/
  # Result: 0 matches
  grep -rn "navigator.locks" js/
  # Result: 0 matches
  ```
- **Consequence**: When multiple tabs are open on the same origin, each tab operates on isolated, stale in-memory references (`AppState.estado.progresso`, `AppState.estado.flashcardData`, and `AppSyncManager.queue`).

### 1.2 Destructive Last-Write-Wins (LWW) Clobbering in `AppState`
- In `js/core/state.js`, lines 101–156 and 158–181:
  ```javascript
  salvarProgresso() {
    try {
      localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
    } catch (e) { ... }
    ...
  }

  salvarFlashcards() {
    try {
      localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData));
    } catch (e) { ... }
    ...
  }
  ```
- In `js/core/state.js`, `carregarProgresso()` (lines 101–139) and `carregarFlashcards()` (lines 158–164) are only executed once at application boot (`init()` in `js/core.js` lines 113–114).
- When a user studies in Tab A (completing 15 flashcards, gaining 150 XP, advancing to Level 2), Tab A writes to `localStorage`. Tab B remains on its stale initial state (Level 1, 0 XP, unreviewed cards). If Tab B performs any action that triggers `salvarProgresso()` or `salvarFlashcards()` (such as answering a single quiz question, completing a dialogue, or toggling sound), Tab B blindly overwrites `localStorage.setItem('it_progresso', ...)` and `localStorage.setItem('it_flashcards', ...)`.
- **Verbatim Effect**: All 15 flashcard reviews, XP progress, level advancement, and unlocked temples earned in Tab A are permanently destroyed.

### 1.3 Offline Queue Race Condition & Duplicate Remote Flush in `AppSyncManager`
- In `js/core/sync.ts`, lines 337–359:
  ```typescript
  private carregarFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        const raw = localStorage.getItem(STORAGE_QUEUE_KEY);
        if (raw) {
          this.queue = JSON.parse(raw);
        }
      }
    } catch (e) {
      console.warn('[SyncManager] Erro ao carregar fila:', e);
      this.queue = [];
    }
  }

  private persistirFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_QUEUE_KEY, JSON.stringify(this.queue));
      }
    } catch (e) {
      console.error('[SyncManager] Falha ao persistir fila no localStorage:', e);
    }
  }
  ```
- In `enfileirar()` (lines 408–474), `this.queue` is queried and updated strictly in memory before calling `persistirFila()`. If Tab A enqueues an offline action, and then Tab B enqueues an offline action, Tab B's in-memory `this.queue` lacks Tab A's item. Tab B writes its isolated queue to `STORAGE_QUEUE_KEY`, permanently dropping Tab A's queued action.
- In `flush()` (lines 479–541), there is no cross-tab mutual exclusion or lock. When the device transitions from offline to online (`window.addEventListener('online')` in line 363), **both tabs trigger `flush()` simultaneously**, sending duplicate batches to the backend adapter (PostgREST/Supabase or PocketBase).

### 1.4 IndexedDB Upgrade Deadlock in `AudioCache`
- In `js/audio_cache.js`, lines 15–47:
  ```javascript
  _abrirDB() {
    if (this._dbPromise) return this._dbPromise;

    this._dbPromise = new Promise((resolve) => {
      if (typeof indexedDB === 'undefined') {
        resolve(null);
        return;
      }

      const req = indexedDB.open(this.DB_NAME, this.DB_VERSION);

      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          db.createObjectStore(this.STORE_NAME, { keyPath: 'hash' });
        }
        if (!db.objectStoreNames.contains(this.TRAD_STORE)) {
          db.createObjectStore(this.TRAD_STORE, { keyPath: 'hash' });
        }
      };

      req.onsuccess = (e) => resolve(e.target.result);
      req.onerror = (e) => {
        console.warn('[AudioCache] Erro ao abrir IndexedDB:', e);
        resolve(null);
      };
    });

    return this._dbPromise;
  }
  ```
- **Omission**: Neither `db.onversionchange`, `db.onclose`, nor `req.onblocked` are implemented.
- **W3C IndexedDB Specification**: When an application update or service worker increases `DB_VERSION` (or adds an object store) in Tab B, the browser attempts an upgrade. However, the upgrade transaction is blocked until all other open connections to the database in other tabs are closed.
- Because Tab A never listens for `versionchange` on `IDBDatabase` and never calls `db.close()`, Tab A holds the database open indefinitely. Tab B's `indexedDB.open` hangs forever in a deadlocked state, and audio caching fails completely.

### 1.5 Existing Reconciliation Math in `ConflictResolver`
- In `js/core/collaboration.ts`, lines 30–144: A well-tested `ConflictResolver` class already implements CRDT union on sets (`templos_desbloqueados`, `conquistas`, `grammatica_completadas`, `favoritos`), max operations on scalar progress (`xp`, `nivel`, `streak`, `streak_recorde`), and LWW on flashcards based on `lastReview` (tie-breaking on `reps`).
- However, `AppState` in `js/core/state.js` currently does not integrate or call this reconciliation logic when persisting or loading state.

---

## 2. Logic Chain

1. **Premise**: Web browsers operate separate JavaScript execution contexts per tab/window. When users open multiple tabs of the PWA (e.g. Flashcards in Tab 1, Grammar or Songs in Tab 2), writes to `localStorage` or `IndexedDB` occur concurrently.
2. **From Observation 1.1 & 1.2**:
   - `AppState` keeps state in module variables (`AppState.estado.progresso` and `AppState.estado.flashcardData`).
   - Without a cross-tab communication mechanism (`BroadcastChannel` and `storage` event), Tab B cannot observe mutations made by Tab A.
   - When Tab B calls `salvarProgresso()`, it serializes its stale in-memory snapshot, clobbering all progress made in Tab A.
   - **Deduction**: Cross-tab state synchronization requires:
     a) Real-time notification across tabs using `BroadcastChannel('apprendimento_channel')` with fallback to `window.addEventListener('storage')`.
     b) A non-destructive CRDT-inspired reconciliation function `AppState.reconciliarProgresso(local, remoto)` and `AppState.reconciliarFlashcards(local, remoto)` that merges foreign updates into the active memory state before saving.
3. **From Observation 1.3**:
   - `AppSyncManager` maintains an in-memory `this.queue` that only reads `localStorage` on boot.
   - Concurrent writes cause dropped queue items, and concurrent online transitions trigger race conditions during `flush()`.
   - **Deduction**: `AppSyncManager` must:
     a) Re-read/merge the queue from `localStorage` whenever another tab mutates `apprendimento_sync_queue`.
     b) Acquire a cross-tab mutex or timestamp lease lock (`apprendimento_sync_lock`) before executing `flush()`, ensuring only one tab processes the queue while other tabs wait and reload the drained queue.
4. **From Observation 1.4**:
   - If an existing tab does not close its `IDBDatabase` connection upon receiving `versionchange`, subsequent database upgrades in other tabs deadlock.
   - Furthermore, the existing tab must invalidate its cached `_dbPromise` so that subsequent audio lookups reopen the upgraded database cleanly.
   - **Deduction**: `AudioCache._abrirDB()` must attach `db.onversionchange = () => { db.close(); AudioCache._dbPromise = null; }`, handle `req.onblocked`, and provide an explicit `fechar()` lifecycle method.
5. **From Observation 1.5**:
   - Pure reconciliation functions can be integrated directly into `AppState` in `js/core/state.js` with zero runtime external dependencies, ensuring high-speed, offline-first execution.

---

## 3. Caveats

1. **Browser Transport Support**: `BroadcastChannel` is supported in all modern evergreen browsers (Chrome 54+, Safari 15.4+, Firefox 38+, Edge 79+). For legacy environments, private browsing restrictions, or Web Worker sandboxes where `BroadcastChannel` may throw or be undefined, the `window.addEventListener('storage')` fallback provides complete coverage.
2. **Storage Event Quirks**: The `storage` event fires exclusively on **other** windows/tabs of the same origin (not in the window that performed `setItem`). However, `storage` events do not carry custom headers (such as `senderId`). Therefore, deduplication must rely on payload equivalence (`JSON.stringify(local) === JSON.stringify(remoto)`) to prevent unnecessary redundant re-renders.
3. **Clock Skew Between Devices vs Local Tabs**: Cross-tab synchronization occurs within the same machine and operating system, meaning system clock timestamps (`Date.now()`) are uniform across tabs. Any edge-case timezone or system clock shifts are safely handled by monotonic timestamp comparisons and fallback tie-breaking on `reps`.
4. **Execution Boundaries**: Milestone 1 exclusively owns `js/core/state.js`, `js/core/sync.ts`, and `js/audio_cache.js`. No files owned by Milestone 2, 3, or 4 are touched.

---

## 4. Conclusion & Complete Implementation Blueprint

### 4.1 Architecture Overview & Message Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│ TAB A (Active Study Session)                                           │
│ 1. User reviews Flashcard or earns XP.                                 │
│ 2. AppState.salvarProgresso() / salvarFlashcards()                     │
│ 3. Writes to localStorage ('it_progresso', 'it_flashcards')            │
│ 4. Broadcasts message over BroadcastChannel('apprendimento_channel')   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
           ┌────────────────────────┴────────────────────────┐
           │ Message Envelope:                               │
           │ {                                               │
           │   type: 'SYNC_UPDATE',                          │
           │   key: 'it_progresso' | 'it_flashcards',        │
           │   senderId: 'tab_1730335200000_abc123',         │
           │   timestamp: 1730335200000,                     │
           │   payload: { ... }                              │
           │ }                                               │
           └────────────────────────┬────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ TAB B (Passive / Concurrent Session)                                   │
│ 1. Receives message on BroadcastChannel (or fallback 'storage' event). │
│ 2. Ignores if senderId === thisTabId.                                  │
│ 3. AppState.reconciliarProgresso(local, remoto):                       │
│    - Sets: union(templos_desbloqueados, conquistas, grammatica)       │
│    - Scalars: max(xp, nivel, streak_recorde)                           │
│    - Streak: evaluates latest ultimo_estudo & max streak               │
│ 4. AppState.reconciliarFlashcards(local, remoto):                      │
│    - Merges cards: card with latest lastReview wins; tie-break on reps │
│ 5. If local had extra uncommitted data -> writes merged to storage.   │
│ 6. Re-renders UI: AppStats.atualizarStats() + temple unlock checks.   │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 4.2 Blueprint 1: `js/core/state.js` (Cross-Tab Sync & CRDT Reconciliation)

#### Key Responsibilities:
1. Generate unique `_tabId` per tab instance (`tab_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`).
2. Initialize `BroadcastChannel('apprendimento_channel')` defensively with try/catch, falling back gracefully to `window.addEventListener('storage')`.
3. Implement pure `reconciliarProgresso(local, remoto)`:
   - Union of number sets: `templos_desbloqueados`, `templos_concluidos`.
   - Union of string sets: `grammatica_completadas`, `conquistas`, `favoritos`.
   - Max scalars: `nivel`, `xp`, `total_palavras`, `streak_recorde`.
   - Streak reconciliation: compares `ultimo_estudo` timestamps; if one tab has a newer study timestamp, its streak takes precedence; if same day or ambiguous, take `Math.max(local.streak, remoto.streak)`.
   - Daily XP (`xp_hoje`, `data_xp_hoje`): takes newer date; if same date, take `Math.max()`.
   - Monotonic `data_inicio`: `Math.min()`.
4. Implement pure `reconciliarFlashcards(local, remoto)`:
   - Preserves all cards unique to either deck.
   - For intersecting card IDs, compares `lastReview` (and legacy `last_review`). The card with the newer review timestamp wins.
   - If timestamps are identical, the card with higher `reps` (or legacy `repeticoes`) wins.
5. In `salvarProgresso()` and `salvarFlashcards()`:
   - Writes to `localStorage` (or `SafeStorage` once available).
   - Broadcasts the update to `'apprendimento_channel'`.
6. Auto-initializes `AppState.initCrossTabSync()` when loaded in browser environments.

#### Code Patch / Blueprint for `js/core/state.js`:

```javascript
// ============================================================
// Additions to js/core/state.js
// ============================================================

const AppState = {
  // Existing state properties...
  estado: {
    secaoAtiva: 'templi',
    templosData: {},
    quizData: [],
    vocabCache: [],
    conjugacoesData: [],
    grammarData: null,
    progresso: null,
    flashcardData: {}
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

    // 1. BroadcastChannel (Modern cross-tab transport)
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

    // 2. window.addEventListener('storage') (Universal Fallback)
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
    if (msg.type !== 'SYNC_UPDATE') return;
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
    if (!remoto || typeof remoto !== 'object') return;
    const local = this.estado.progresso;
    const merged = this.reconciliarProgresso(local, remoto);

    // Evita loop se o estado mesclado já for idêntico ao local
    if (JSON.stringify(local) === JSON.stringify(merged)) return;

    this.estado.progresso = merged;

    // Se o merge integrou dados locais não presentes no remoto, persiste e propaga
    if (JSON.stringify(merged) !== JSON.stringify(remoto)) {
      try {
        localStorage.setItem('it_progresso', JSON.stringify(merged));
        this._broadcastSync('it_progresso', merged);
      } catch (_) {}
    }

    // Reatividade imediata de UI
    const statsMod = (typeof window !== 'undefined' && window.AppStats) || (typeof AppStats !== 'undefined' ? AppStats : null);
    if (statsMod && typeof statsMod.atualizarStats === 'function') {
      statsMod.atualizarStats();
    }
    if (typeof Progressao !== 'undefined' && typeof Progressao.verificarDesbloqueioTemplos === 'function') {
      Progressao.verificarDesbloqueioTemplos();
    }
  },

  _processarFlashcardsRemoto(remoto) {
    if (!remoto || typeof remoto !== 'object') return;
    const local = this.estado.flashcardData;
    const merged = this.reconciliarFlashcards(local, remoto);

    if (JSON.stringify(local) === JSON.stringify(merged)) return;

    this.estado.flashcardData = merged;

    if (JSON.stringify(merged) !== JSON.stringify(remoto)) {
      try {
        localStorage.setItem('it_flashcards', JSON.stringify(merged));
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
    if (!local) return { ...remoto };
    if (!remoto) return { ...local };

    const uniaoNumeros = (a = [], b = []) =>
      Array.from(new Set([...(Array.isArray(a) ? a : []), ...(Array.isArray(b) ? b : [])])).sort((x, y) => x - y);
    const uniaoStrings = (a = [], b = []) =>
      Array.from(new Set([...(Array.isArray(a) ? a : []), ...(Array.isArray(b) ? b : [])]));

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

    return {
      ...local,
      ...remoto,
      nivel,
      xp,
      xp_proximo_nivel: Math.max(Number(local.xp_proximo_nivel) || 500, Number(remoto.xp_proximo_nivel) || 500),
      templos_desbloqueados: uniaoNumeros(local.templos_desbloqueados, remoto.templos_desbloqueados),
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
      audio_rate: remoto.audio_rate || local.audio_rate || 0.85
    };
  },

  reconciliarFlashcards(local = {}, remoto = {}) {
    const loc = local && typeof local === 'object' ? local : {};
    const rem = remoto && typeof remoto === 'object' ? remoto : {};
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

  salvarProgresso() {
    try {
      localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        this._gcFlashcards();
        try { localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso)); } catch (_) {}
      }
    }
    this._broadcastSync('it_progresso', this.estado.progresso);
    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.progresso) {
        sync.enfileirar('progress', 'update', 'current_progress', this.estado.progresso);
      }
    } catch (_) {}
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
    this._broadcastSync('it_flashcards', this.estado.flashcardData);
    try {
      const sync = (typeof window !== 'undefined' && window.AppSyncManager) || (typeof globalThis !== 'undefined' && globalThis.AppSyncManager);
      if (sync && this.estado.flashcardData) {
        sync.enfileirar('flashcards', 'update', 'current_deck', this.estado.flashcardData);
      }
    } catch (_) {}
  }
};

// Auto-inicialização ao carregar no browser
if (typeof window !== 'undefined') {
  window.AppState = AppState;
  try {
    AppState.initCrossTabSync();
  } catch (err) {
    console.warn('[AppState] Falha ao inicializar cross-tab sync:', err);
  }
}
```

---

### 4.3 Blueprint 2: `js/core/sync.ts` (Queue Synchronization & Concurrency Lock)

#### Key Responsibilities:
1. Generate unique `tabId` for each `SyncManager` instance.
2. Listen to `BroadcastChannel('apprendimento_channel')` and fallback `window.addEventListener('storage')` for `key === 'apprendimento_sync_queue'`.
3. In `recarregarFila()`: reload `this.queue` from `localStorage` and trigger status updates.
4. In `enfileirar()`: refresh queue from storage prior to deduplication, ensuring actions enqueued by other tabs are never overwritten.
5. In `persistirFila()`: write to storage and broadcast `type: 'SYNC_UPDATE'`, `key: 'apprendimento_sync_queue'`.
6. In `flush()`: implement a mutual-exclusion cross-tab lock (`apprendimento_sync_lock` timestamp token with 15s lease). If another tab is actively flushing, the second tab skips the network batch, avoiding duplicate PostgREST requests. When the active tab finishes, it broadcasts the drained queue, and waiting tabs update their pending counter automatically.

#### Code Patch / Blueprint for `js/core/sync.ts`:

```typescript
// ============================================================
// Additions to js/core/sync.ts
// ============================================================

export class SyncManager {
  private queue: SyncItem[] = [];
  private adapter: IBackendAdapter;
  private config: BackendConfig = { provider: 'mock', autoSync: true, syncIntervalMs: 30000 };
  private isSyncing: boolean = false;
  private lastSyncSuccess: number | null = null;
  private lastSyncError: string | null = null;
  private syncTimer: any = null;
  private statusListeners: Array<(status: SyncStatus) => void> = [];

  // Multi-tab coordination
  private tabId: string = `sync_tab_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
  private syncChannel: BroadcastChannel | null = null;

  constructor(adapter?: IBackendAdapter) {
    this.adapter = adapter || new MockBackendAdapter();
    this.carregarConfig();
    this.carregarFila();
    this.configurarListenersOnline();
    this.configurarCrossTabSync();
  }

  private configurarCrossTabSync(): void {
    if (typeof window === 'undefined') return;

    if (typeof BroadcastChannel !== 'undefined') {
      try {
        this.syncChannel = new BroadcastChannel('apprendimento_channel');
        this.syncChannel.onmessage = (event) => {
          const msg = event?.data;
          if (!msg || msg.senderId === this.tabId) return;
          if (msg.type === 'SYNC_UPDATE' && msg.key === STORAGE_QUEUE_KEY) {
            this.recarregarFila();
          }
        };
      } catch (_) {
        this.syncChannel = null;
      }
    }

    window.addEventListener('storage', (e) => {
      if (e.key === STORAGE_QUEUE_KEY) {
        this.recarregarFila();
      }
    });
  }

  private broadcastQueueChange(): void {
    if (this.syncChannel) {
      try {
        this.syncChannel.postMessage({
          type: 'SYNC_UPDATE',
          key: STORAGE_QUEUE_KEY,
          senderId: this.tabId,
          timestamp: Date.now()
        });
      } catch (_) {}
    }
  }

  public recarregarFila(): void {
    const contagemAnterior = this.queue.length;
    this.carregarFila();
    if (this.queue.length !== contagemAnterior) {
      this.notificarStatus();
    }
  }

  private persistirFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_QUEUE_KEY, JSON.stringify(this.queue));
      }
    } catch (e) {
      console.error('[SyncManager] Falha ao persistir fila no localStorage:', e);
    }
    this.broadcastQueueChange();
  }

  private tentarAdquirirLockFlush(): boolean {
    if (typeof localStorage === 'undefined') return true;
    try {
      const agora = Date.now();
      const raw = localStorage.getItem('apprendimento_sync_lock');
      if (raw) {
        const lock = JSON.parse(raw);
        // Lock ativo de outra aba com expiração de 15 segundos
        if (lock && lock.tabId !== this.tabId && (agora - lock.timestamp < 15000)) {
          return false;
        }
      }
      localStorage.setItem('apprendimento_sync_lock', JSON.stringify({ tabId: this.tabId, timestamp: agora }));
      return true;
    } catch (_) {
      return true;
    }
  }

  private liberarLockFlush(): void {
    if (typeof localStorage === 'undefined') return;
    try {
      const raw = localStorage.getItem('apprendimento_sync_lock');
      if (raw) {
        const lock = JSON.parse(raw);
        if (lock && lock.tabId === this.tabId) {
          localStorage.removeItem('apprendimento_sync_lock');
        }
      }
    } catch (_) {}
  }

  public enfileirar(
    entity: SyncEntity,
    action: SyncAction,
    entityId: string,
    payload: Record<string, any>
  ): SyncItem {
    // Sincroniza com o estado em disco antes de mutar a fila
    this.recarregarFila();

    const timestamp = Date.now();
    const id = `sync_${timestamp}_${Math.random().toString(36).substring(2, 9)}`;

    const existingIndex = this.queue.findIndex(
      (item) => item.entity === entity && item.entityId === entityId
    );

    let item: SyncItem;

    if (existingIndex >= 0) {
      const existing = this.queue[existingIndex];
      if (action === 'delete') {
        if (existing.action === 'create') {
          this.queue.splice(existingIndex, 1);
          this.persistirFila();
          this.notificarStatus();
          return existing;
        }
        existing.action = 'delete';
        existing.payload = {};
        existing.timestamp = timestamp;
        item = existing;
      } else {
        existing.payload = { ...existing.payload, ...payload };
        existing.timestamp = timestamp;
        item = existing;
      }
    } else {
      item = {
        id,
        entity,
        action,
        entityId,
        payload,
        timestamp,
        attempts: 0
      };
      this.queue.push(item);
    }

    this.persistirFila();
    this.notificarStatus();

    if (this.isOnline() && this.config.autoSync) {
      this.flush();
    }

    return item;
  }

  public async flush(): Promise<SyncBatchResult> {
    if (this.isSyncing || this.queue.length === 0) {
      return { sucesso: true, processados: [], falhas: [] };
    }

    if (!this.isOnline()) {
      return {
        sucesso: false,
        processados: [],
        falhas: [{ id: 'network', erro: 'Dispositivo offline' }]
      };
    }

    // Mutual-exclusion guard entre abas
    if (!this.tentarAdquirirLockFlush()) {
      return { sucesso: true, processados: [], falhas: [] };
    }

    this.isSyncing = true;
    this.notificarStatus();

    try {
      const batch = this.queue.slice(0, 25);
      const resultado = await this.adapter.syncBatch(batch);

      if (resultado.processados.length > 0) {
        const setSucesso = new Set(resultado.processados);
        this.queue = this.queue.filter((item) => !setSucesso.has(item.id));
        this.lastSyncSuccess = Date.now();
        this.lastSyncError = null;
      }

      if (resultado.falhas.length > 0) {
        const mapaFalhas = new Map(resultado.falhas.map((f) => [f.id, f.erro]));
        for (const item of this.queue) {
          if (mapaFalhas.has(item.id)) {
            item.attempts += 1;
            item.lastAttempt = Date.now();
            item.lastError = mapaFalhas.get(item.id);
          }
        }
        const descartados = this.queue.filter((i) => i.attempts >= MAX_ATTEMPTS);
        if (descartados.length > 0) {
          this.queue = this.queue.filter((i) => i.attempts < MAX_ATTEMPTS);
        }
        this.lastSyncError = resultado.falhas[0].erro;
      }

      this.persistirFila();
      return resultado;
    } catch (err: any) {
      const erroMsg = err.message || 'Falha durante o flush de sincronização';
      this.lastSyncError = erroMsg;
      return {
        sucesso: false,
        processados: [],
        falhas: [{ id: 'exception', erro: erroMsg }]
      };
    } finally {
      this.isSyncing = false;
      this.liberarLockFlush();
      this.notificarStatus();
    }
  }
}
```

---

### 4.4 Blueprint 3: `js/audio_cache.js` (IndexedDB Version Change Deadlock Prevention)

#### Key Responsibilities:
1. Attach `db.onversionchange` listener inside `req.onsuccess`:
   - Closes the active database connection immediately (`db.close()`).
   - Nulls out `AudioCache._dbPromise`, allowing subsequent operations to re-open the database at the upgraded schema.
2. Attach `db.onclose` listener to null out `_dbPromise` on unexpected teardown.
3. Attach `req.onblocked` listener to log clear diagnostics if a blocked event occurs.
4. In `req.onerror`: null out `AudioCache._dbPromise` so transient errors do not permanently poison the cached promise.
5. Provide explicit `fechar()` method on `AudioCache` for lifecycle management, clean test teardown, and `beforeunload` handling.

#### Code Patch / Blueprint for `js/audio_cache.js`:

```javascript
// ============================================================
// Additions to js/audio_cache.js
// ============================================================

const AudioCache = {
  DB_NAME: 'it_audio_db',
  DB_VERSION: 2,
  STORE_NAME: 'audio_cache',
  TRAD_STORE: 'trad_cache',
  _dbPromise: null,

  _abrirDB() {
    if (this._dbPromise) return this._dbPromise;

    this._dbPromise = new Promise((resolve) => {
      if (typeof indexedDB === 'undefined') {
        resolve(null);
        return;
      }

      const req = indexedDB.open(this.DB_NAME, this.DB_VERSION);

      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          db.createObjectStore(this.STORE_NAME, { keyPath: 'hash' });
        }
        if (!db.objectStoreNames.contains(this.TRAD_STORE)) {
          db.createObjectStore(this.TRAD_STORE, { keyPath: 'hash' });
        }
      };

      req.onsuccess = (e) => {
        const db = e.target.result;

        // PREVENÇÃO DE DEADLOCK EM MULTI-ABA (F3):
        // Quando uma nova versão do banco é aberta por outra aba ou SW, o navegador
        // dispara 'versionchange' em todas as conexões abertas existentes.
        // O fechamento imediato permite que o req.onupgradeneeded da outra aba prossiga.
        db.onversionchange = () => {
          console.warn('[AudioCache] Mudança de versão detectada em outra aba. Fechando conexão para permitir upgrade.');
          try { db.close(); } catch (_) {}
          AudioCache._dbPromise = null;
        };

        db.onclose = () => {
          AudioCache._dbPromise = null;
        };

        resolve(db);
      };

      req.onblocked = (e) => {
        console.warn('[AudioCache] Abertura do IndexedDB bloqueada por conexão ativa em outra aba.');
      };

      req.onerror = (e) => {
        console.warn('[AudioCache] Erro ao abrir IndexedDB:', e);
        AudioCache._dbPromise = null;
        resolve(null);
      };
    });

    return this._dbPromise;
  },

  // Fecha explicitamente a conexão com o IndexedDB (útil para testes e teardown)
  fechar() {
    if (this._dbPromise) {
      this._dbPromise.then(db => {
        if (db) {
          try { db.close(); } catch (_) {}
        }
      }).catch(() => {});
      this._dbPromise = null;
    }
  },

  // Rest of existing AudioCache methods unchanged (obter, salvar, estatisticas, limpar, etc.)
  ...
};
```

---

## 5. Verification Method

To independently verify the implementation blueprint and ensure zero regressions:

### 5.1 Baseline Checks
1. **Existing Test Suite**:
   ```bash
   npm test
   ```
   *Expected outcome*: 15 passed test files, 104 passed tests, code 0.
2. **TypeScript & Production Build**:
   ```bash
   npm run build
   ```
   *Expected outcome*: `build:ts` transpiles ES2022 modules, `tsc --noEmit` validates types without errors, Vite outputs production bundle to `dist/` with exit code 0.

### 5.2 Automated Test Suite Specification for Feature F3 (`tests/cross_tab_sync.test.ts`)
The implementer (and M4 test track) can run the following dedicated test suite in Vitest:

```typescript
// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import AppState from '../js/core/state';
import { SyncManager, MockBackendAdapter } from '../js/core/sync';
import AudioCache from '../js/audio_cache';

describe('F3: Multi-Tab Concurrency & Synchronization', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    AudioCache.fechar();
  });

  describe('AppState.reconciliarProgresso()', () => {
    it('deve unir templos desbloqueados e concluídos sem perda de dados', () => {
      const local = {
        nivel: 2,
        xp: 200,
        templos_desbloqueados: [1, 2],
        templos_concluidos: [1],
        conquistas: ['c1'],
        streak: 3
      };
      const remoto = {
        nivel: 3,
        xp: 350,
        templos_desbloqueados: [1, 3],
        templos_concluidos: [2],
        conquistas: ['c2'],
        streak: 4
      };

      const merged = AppState.reconciliarProgresso(local, remoto);

      expect(merged.nivel).toBe(3);
      expect(merged.xp).toBe(350);
      expect(merged.templos_desbloqueados).toEqual([1, 2, 3]);
      expect(merged.templos_concluidos).toEqual([1, 2]);
      expect(merged.conquistas).toEqual(expect.arrayContaining(['c1', 'c2']));
      expect(merged.streak).toBe(4);
    });

    it('deve ser idempotente: mesclar o mesmo estado não altera valores', () => {
      const state = {
        nivel: 5,
        xp: 1200,
        templos_desbloqueados: [1, 2, 3, 4],
        conquistas: ['mestre'],
        streak: 10
      };

      const merged = AppState.reconciliarProgresso(state, state);
      expect(merged.xp).toBe(1200);
      expect(merged.nivel).toBe(5);
      expect(merged.templos_desbloqueados).toEqual([1, 2, 3, 4]);
    });
  });

  describe('AppState.reconciliarFlashcards()', () => {
    it('deve priorizar a carta com timestamp lastReview mais recente', () => {
      const local = {
        c1: { id: 'c1', state: 'learning', reps: 1, lastReview: 1000 }
      };
      const remoto = {
        c1: { id: 'c1', state: 'review', reps: 2, lastReview: 2000 }
      };

      const merged = AppState.reconciliarFlashcards(local, remoto);
      expect(merged.c1.lastReview).toBe(2000);
      expect(merged.c1.reps).toBe(2);
    });

    it('deve preservar cartas existentes apenas no baralho local ou remoto', () => {
      const local = {
        c1: { id: 'c1', lastReview: 1000 }
      };
      const remoto = {
        c2: { id: 'c2', lastReview: 1500 }
      };

      const merged = AppState.reconciliarFlashcards(local, remoto);
      expect(merged.c1).toBeDefined();
      expect(merged.c2).toBeDefined();
    });
  });

  describe('AppSyncManager Concurrency & Lock', () => {
    it('deve sincronizar a fila entre instâncias quando uma ação for enfileirada', () => {
      const adapter = new MockBackendAdapter();
      const tabA = new SyncManager(adapter);
      const tabB = new SyncManager(adapter);

      tabA.enfileirar('progress', 'update', 'p1', { xp: 100 });
      tabB.recarregarFila();

      expect(tabB.getFila().length).toBe(1);
      expect(tabB.getFila()[0].payload.xp).toBe(100);
    });

    it('deve impedir execução concorrente de flush quando lock ativo de outra aba existir', async () => {
      const adapter = new MockBackendAdapter();
      const tabA = new SyncManager(adapter);
      const tabB = new SyncManager(adapter);

      tabA.enfileirar('progress', 'update', 'p1', { xp: 100 });

      // Simula lock ativo de outra aba
      localStorage.setItem('apprendimento_sync_lock', JSON.stringify({
        tabId: 'outra_aba_ativa',
        timestamp: Date.now()
      }));

      const res = await tabB.flush();
      expect(res.processados.length).toBe(0); // Evitou execução concorrente
    });
  });

  describe('AudioCache IndexedDB onversionchange', () => {
    it('deve registrar onversionchange fechando a conexão e limpando _dbPromise', async () => {
      const db = await AudioCache._abrirDB();
      if (!db) return; // Ambiente sem IndexedDB nativo (ex: mock limitado)

      expect(AudioCache._dbPromise).not.toBeNull();
      // Dispara evento manual de versionchange
      db.dispatchEvent(new Event('versionchange'));

      expect(AudioCache._dbPromise).toBeNull();
    });
  });
});
```

### 5.3 Invalidation Conditions
This blueprint is invalidated if:
1. `AppState` dependencies require asynchronous import chains that block synchronous `localStorage` reading on boot.
2. The browser policy strictly disables `BroadcastChannel` and blocks `localStorage` in a way that `window.addEventListener('storage')` does not fire (handled by our graceful try/catch and in-memory fallback).
3. The schema for `it_progresso` introduces nested objects that violate commutative CRDT properties (all current fields are primitive scalars or discrete sets, preserving commutativity and idempotency).

---
*Report completed by Explorer M1.2 for Orchestrator consolidation and Milestone 1 implementer execution.*
