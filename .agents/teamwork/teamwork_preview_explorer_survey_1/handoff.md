# Diagnostic Survey & Vulnerability Mapping: Storage, Persistence & Data Integrity

**Author**: Survey Explorer 1 (Storage, Persistence & Data Integrity)  
**Date**: 2026-10-31T00:05:00Z  
**Workspace**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano`  
**Working Directory**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_1`

---

## 1. Observation

### 1.1 LocalStorage & IndexedDB Inventory & Abstraction Layers
- **Direct Code Locations**:
  - Over 250 references to `localStorage` across 28 distinct JavaScript/TypeScript source files (`js/core/state.js`, `js/core/sync.ts`, `js/core/analytics.ts`, `js/core/backup_reminder.js`, `js/core/favorites.js`, `js/core/navigation.js`, `js/core/stats.js`, `js/core/tts.js`, `js/audio.js`, `js/canzoni.js`, `js/dialoghi.js`, `js/grammar.js`, `js/heatmap.js`, `js/i18n.js`, `js/ia-import.js`, `js/imitazione.js`, `js/notificacoes.js`, `js/onboarding.js`, `js/profilo.js`, `js/progression.ts`, `js/quiz.js`, `js/storie.js`, `js/tour.js`, `js/voice_engine.ts`).
  - **IndexedDB Stores**:
    - `it_audio_db` (version 2) in `js/audio_cache.js` lines 9-37: Object stores `audio_cache` (keyPath `hash`) and `trad_cache` (keyPath `hash`, TTL 7 days).
    - `it_canzoni_audio_db` (version 1) in `js/canzoni.js` lines 4-18: Object store `audios` (out-of-line keys by song `id`).
- **Complete Key Catalog**:
  1. `it_progresso`: Core user progress object (`nivel`, `xp`, `streak`, `templos_desbloqueados`, `conquistas`, etc.).
  2. `it_flashcards`: Full FSRS flashcard deck keyed by word id (`{ [id]: FlashcardFSRS }`).
  3. `it_diario`: Daily study activity calendar map (`{ [YYYY-MM-DD]: { cards, xp } | number }`).
  4. `it_quiz_historico`: Quiz result entries array.
  5. `it_storie_lidas`: Array of story IDs marked as read.
  6. `it_canzoni_custom`, `it_dialoghi_custom`, `it_storie_custom`, `it_imitazioni_custom`, `it_vocab_custom`: Custom user-created/imported modules.
  7. `it_canzoni_ocultas`: Hidden track IDs list.
  8. `it_book_bm_${id}`: Dynamic bookmark page offsets for stories/books.
  9. `it_palavra_dia`: Cached daily word `{ data, id }`.
  10. `it_client_errors`: Array of up to 30 unhandled runtime errors and promise rejections.
  11. `it_swr_templos_meta`, `it_swr_grammar`, `it_swr_canzoni`, `it_swr_dialogi`, `it_swr_storie`, `it_swr_imitazioni`: Ephemeral network cache payloads (often several megabytes total).
  12. `it_locale_cache_${lang}`: i18n locale translations dictionary.
  13. `it_som`, `it_som_default_on`, `it_sidebar_pinned`, `it_audio_speed`, `it_tema`, `it_idioma`, `it_onboarding_done`, `it_tour_done`, `it_ultimo_aviso_backup`, `it_voz_preferida`, `it_usar_voz_neural`, `it_voz_neural_instalada`, `it_imersao_usada`: Configuration flags and preferences.
  14. `apprendimento_sync_queue`: Offline-first backend sync queue.
  15. `apprendimento_backend_config`: Remote backend settings (Supabase/PocketBase).
  16. `apprendimento_analytics_events`, `apprendimento_analytics_user_id`, `apprendimento_flag_overrides`: Telemetry events and A/B test flag overrides.
  17. `it_quiz_sessao`: In `sessionStorage` (in-flight quiz questions and answers).
- **Storage Abstraction Finding**:
  There is **no centralized storage gateway or storage adapter interface**. 28 separate modules directly call `window.localStorage` methods directly. There is no unified error handling, no key prefix enforcement, and no transparent fallbacks when storage is unavailable or full.

---

### 1.2 Quota Management & Handling of QuotaExceededError
- **Direct Code Locations**:
  - `js/core/state.js` lines 141-149:
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
      ...
    }
    ```
  - `js/core/state.js` lines 166-174:
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
      ...
    }
    ```
  - `js/core/state.js` lines 183-197:
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
  - `js/heatmap.js` lines 39-41:
    ```javascript
    try {
      localStorage.setItem('it_diario', JSON.stringify(diario));
    } catch (e) {}
    ```
  - `js/core/sync.ts` lines 351-359:
    ```typescript
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
- **Observations on Quota Management**:
  1. In `_gcFlashcards()`, the method mutates `this.estado.flashcardData` in memory by deleting keys, but **never persists `this.estado.flashcardData` back to localStorage**! Thus, when `salvarProgresso()` calls `this._gcFlashcards()`, **zero bytes are released from localStorage**. The subsequent `setItem('it_progresso', ...)` is guaranteed to fail again.
  2. The GC condition `(f.lastReview && agora - f.lastReview > NOVENTA_DIAS && f.state === 'new')` is an impossible oxymoron: a card in state `'new'` has never been reviewed, so `f.lastReview` is either `null` or `undefined`.
  3. Non-critical ephemeral caches (`it_swr_templos_meta`, `it_swr_grammar`, `it_swr_canzoni`, `it_swr_storie`, `it_client_errors`) take up 2 to 4 MB of the ~5 MB localStorage budget. When quota is exceeded, the GC targets core user flashcard data rather than evicting the disposable SWR caches.
  4. Quota check only looks for `e.name === 'QuotaExceededError'`. On Safari/WebKit, older mobile engines, or private browsing modes, the exception may be `code === 22`, `QUOTA_EXCEEDED_ERR`, `NSURLErrorDomain`, or `-2147024882`, causing the block to be skipped.
  5. Both `salvarProgresso()` and `salvarFlashcards()` fail silently with `catch (_) {}`. The user receives no toast notification, banner, or error log indicating that study progress is not being committed.

---

### 1.3 Multi-Tab Concurrency & Race Conditions
- **Direct Code Search**:
  - `BroadcastChannel`: 0 occurrences in codebase.
  - `addEventListener('storage', ...)` or `window.onstorage`: 0 occurrences in codebase.
  - `navigator.locks` (Web Locks API): 0 occurrences in codebase.
- **Cross-Tab State Destruction**:
  - In `js/core/state.js`, state is loaded once on application startup via `carregarProgresso()` (line 101) and `carregarFlashcards()` (line 158) into `AppState.estado.progresso` and `AppState.estado.flashcardData`.
  - When user works in Tab A (e.g. completes 15 flashcards, gaining 150 XP, advancing to Level 2), Tab A writes to `it_progresso` and `it_flashcards`.
  - Tab B remains on its stale in-memory snapshot (Level 1, 0 XP, unreviewed cards).
  - When Tab B triggers an action (e.g. answering a single quiz question, completing a dialogue, or toggling sound/sidebar), it calls `salvarProgresso()` or `salvarFlashcards()`.
  - Tab B executes `localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso))`, **blindly overwriting and destroying Tab A's 15 card reviews, XP gain, streak update, and unlocked temples**.
- **Cross-Tab Queue Corruption in `AppSyncManager`**:
  - In `js/core/sync.ts`, `this.queue` is initialized once in `carregarFila()` (line 337).
  - When Tab A enqueues an offline action, it updates `localStorage.setItem(STORAGE_QUEUE_KEY, ...)`.
  - When Tab B enqueues an offline action, its in-memory `this.queue` does not contain Tab A's item. Tab B writes its queue to localStorage, dropping Tab A's offline action permanently.
- **IndexedDB Multi-Tab Blocking**:
  - In `js/audio_cache.js` (`AudioCache`) and `js/canzoni.js` (`CanzoniAudioDB`), neither registers an `onversionchange` handler nor an `onblocked` handler on the `IDBDatabase` or `IDBOpenDBRequest`. If an upgrade is triggered in one tab, the database becomes blocked by open connections in background tabs.

---

### 1.4 Corrupted Data & Malformed Payload Handling
- **Direct Code Locations**:
  - `js/canzoni.js` line 128: `this.custom = JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]');` (no try/catch block).
  - `js/canzoni.js` line 132: `this._ocultas = JSON.parse(localStorage.getItem('it_canzoni_ocultas') || '[]');` (no try/catch block).
  - `js/core/backup_reminder.js` line 43: `parseInt(localStorage.getItem(this.CHAVE_STORAGE), 10);` (returns `NaN` if malformed string).
  - `js/core/state.js` lines 103-118 (`carregarProgresso`):
    ```javascript
    const raw = localStorage.getItem('it_progresso');
    if (raw) {
      const p = JSON.parse(raw);
      if (!p.grammatica_completadas) p.grammatica_completadas = [];
      if (p.meta_diaria === undefined) p.meta_diaria = 100;
      ...
      return p;
    }
    ```
- **Observations on Schema Validation**:
  - If `p` in `carregarProgresso` parses to a primitive (e.g. `"corrupted"` or `123`) or `null`, accessing `p.grammatica_completadas` throws `TypeError: Cannot create property 'grammatica_completadas' on string/number`.
  - If `p.templos_desbloqueados` is missing or not an array, `AppState` does not repair it. When the UI loads and runs `p.templos_desbloqueados.includes(num)`, it throws a fatal TypeError that crashes temple rendering and leaves a blank screen.
  - If `it_flashcards` parses to an array `[]` or corrupted structure, `carregarFlashcards()` returns it as-is without verifying that values conform to `{ state, reps, stability, difficulty }`. When `FSRS.review()` is called, mathematical operations produce `NaN`, which poisons card stability and interval calculations permanently.
  - `package.json` includes `zod: ^4.6.7`, but Zod is currently completely unused at runtime for parsing or validating persisted data or imported payloads.

---

### 1.5 Export / Import Mechanisms & State Wipe Risks
- **Direct Code Locations**:
  - `js/profilo.js` lines 414-463 (`exportarDados`): Collects `it_progresso`, `it_flashcards`, `it_diario`, custom content, and `it_book_bm_*` into a version 4 backup JSON.
    - If any single item in localStorage contains invalid JSON, `JSON.parse(localStorage.getItem(...) || '...')` in `exportarDados()` throws an unhandled `SyntaxError`, completely crashing the export button and preventing the user from creating a rescue backup!
  - `js/profilo.js` lines 466-514 (`importarDados`):
    ```javascript
    const backup = JSON.parse(e.target.result);
    if (!backup.versao || !backup.progresso) throw new Error(I18n.t('prof_erro_formato'));
    if (!confirm(I18n.t('prof_confirm_importar'))) return;
    if (backup.progresso)  localStorage.setItem('it_progresso',  JSON.stringify(backup.progresso));
    if (backup.flashcards) localStorage.setItem('it_flashcards', JSON.stringify(backup.flashcards));
    if (backup.diario)     localStorage.setItem('it_diario',     JSON.stringify(backup.diario));
    ...
    ```
- **Observations on Import Risks**:
  1. **Zero Validation of Subfields**: The only requirement is `backup.versao` and `backup.progresso`. An imported backup with `"progresso": { "nivel": "NaN", "templos_desbloqueados": "broken" }` is directly written to localStorage. Upon `location.reload()`, the application crashes permanently on boot.
  2. **Non-Atomic State Corruption**: The import performs 20 consecutive `localStorage.setItem` calls without staging or transaction guarantees. If `QuotaExceededError` occurs on item 8:
     - The first 7 items (e.g. progress, flashcards, diary) are updated.
     - The remaining items (custom songs, stories, vocabulary, settings) are lost or left in an inconsistent mixed state.
     - There is no rollback to the pre-import state.
  3. **Key Namespace Injection & Storage Flooding via Bookmarks**:
     Lines 494-498:
     ```javascript
     if (backup.bookmarks && typeof backup.bookmarks === 'object') {
       for (const [k, v] of Object.entries(backup.bookmarks)) {
         if (k.startsWith('it_book_bm_')) localStorage.setItem(k, v);
       }
     }
     ```
     Any arbitrary key starting with `it_book_bm_` is written directly without validation on key character sets, key count limits, or value byte size. An imported payload can inject 50,000 keys or large base64 strings, crashing storage.
  4. **XSS & Content Injection**:
     In `importarConteudoCustom()` and `importarDados()`, imported songs, dialogues, and stories containing HTML tags or JavaScript URI vectors are stored and subsequently rendered with `innerHTML` across multiple views without entity escaping (e.g. `js/profilo.js` line 65).

---

### 1.6 Audit of Existing Persistence Tests
- **Direct File Examination**:
  - Ran `npm test`: 15 test files passed (104 tests passed).
  - `tests/backup_reminder.test.js`: Tests only timestamp math (`deveExibir()`) and DOM modal insertion.
  - `tests/sync.test.ts`: Tests `SyncManager` using an in-memory `MockBackendAdapter` and `localStorage.clear()` in setup.
  - `tests/collaboration.test.ts`: Tests CRDT merge math (`ConflictResolver`) and `SharedDeckManager` checksum purely in-memory.
  - `tests/security.test.js`: Defines a fake local `validarDialogo()` function inside lines 66-79 that does not exist in production code (`js/ia-import.js`).
  - `tests/progression.test.ts`: Specifically stubs `App.salvarProgresso = () => {}`, explicitly bypassing all storage code.
- **Coverage Gap**:
  - **Zero tests exist** for `AppState.carregarProgresso()`, `AppState.salvarProgresso()`, `AppState.carregarFlashcards()`, `AppState.salvarFlashcards()`.
  - **Zero tests exist** for `AppState._gcFlashcards()` or `QuotaExceededError` recovery.
  - **Zero tests exist** for `Profilo.exportarDados()` or `Profilo.importarDados()`.
  - **Zero tests exist** for `AudioCache` or `CanzoniAudioDB`.
  - **Zero tests exist** for multi-tab concurrency or storage synchronization.
  - **Zero tests exist** for handling corrupted or truncated JSON in localStorage.

---

## 2. Logic Chain

1. **Premise**: In an offline-first PWA learning app, client storage is the single source of truth for user progress, spaced repetition intervals, streaks, and custom content.
2. **From Observation 1.1 & 1.2**:
   - The app stores both critical user state (`it_progresso`, `it_flashcards`, `it_diario`) and massive disposable network caches (`it_swr_templos_meta`, `it_swr_grammar`, `it_swr_canzoni`) in the exact same 5 MB `localStorage` partition.
   - When quota limit is reached, `salvarProgresso()` calls `_gcFlashcards()`.
   - `_gcFlashcards()` deletes items from the in-memory object but does not call `localStorage.setItem('it_flashcards', ...)`.
   - Therefore, zero disk space is freed, the retry fails, and the user's progress write is silently swallowed in `catch (_) {}`.
   - **Deduction**: Once a user approaches 5 MB (or is on iOS with reduced quota), all subsequent flashcard reviews and XP gains are silently dropped. On page refresh, the user discovers their study session was completely lost.
3. **From Observation 1.3**:
   - `window.addEventListener('storage', ...)` and `BroadcastChannel` are absent.
   - `AppState` maintains state in singleton memory variables loaded only at boot.
   - If a user opens the app in two tabs (e.g. one for flashcards, one for grammar or dictionary lookup), writes from either tab overwrite the other without reading the latest state from `localStorage` or merging differences.
   - **Deduction**: Multi-tab usage is guaranteed to cause silent data loss (LWW clobbering) where whatever tab writes last overwrites all progress made in concurrent tabs.
4. **From Observation 1.4 & 1.5**:
   - `carregarProgresso()` assumes `p` is an object and that fields like `templos_desbloqueados` exist and have `.includes()`.
   - `importarDados()` accepts any JSON with `.versao` and `.progresso` without validating field types, array shapes, or numerical ranges.
   - `importarDados()` executes non-atomic sequential writes.
   - `exportarDados()` fails if any single key in localStorage has malformed JSON.
   - **Deduction**: If a user encounters a crash, power cut mid-write, or imports a corrupted backup, the app enters an unrecoverable crash loop on startup. Furthermore, because `exportarDados()` crashes on malformed JSON, the user cannot even rescue their salvageable data.
5. **From Observation 1.6**:
   - No existing unit or integration tests exercise storage failure modes, quota exhaustion, malformed JSON recovery, or import validation.
   - **Deduction**: Future refactoring or bug fixes without dedicated storage stress tests risk introducing silent regressions that compromise student data integrity.

---

## 3. Caveats

1. **Storage Quota Variability**: The exact threshold for `QuotaExceededError` varies by browser and operating system: ~5 MB in standard desktop browsers, but can be as low as 1 MB to 2.5 MB in certain mobile WebKit/PWA contexts, or 0 bytes if storage is blocked by browser policies.
2. **IndexedDB Availability in Private Mode**: While modern browsers support IndexedDB in private browsing, older iOS Safari versions could throw `SecurityError` or `InvalidStateError` when opening IndexedDB.
3. **Third-Party Sync Adapters**: `SupabaseAdapter` and `PocketBaseAdapter` were inspected at the code level, but live external endpoints were not pinged, as tests appropriately run against `MockBackendAdapter`.

---

## 4. Conclusion & Proposed Strategy

### 4.1 Vulnerability Severity Matrix

| Vulnerability ID | Description | Severity | Affected Files | Risk Impact |
| :--- | :--- | :--- | :--- | :--- |
| **VULN-STO-01** | `_gcFlashcards()` in-memory mutation without localStorage write on `QuotaExceededError` | **CRITICAL** | `js/core/state.js:145, 170, 183` | Permanent silent loss of study progress and flashcard reviews when storage is full. |
| **VULN-STO-02** | SWR network caches choking localStorage user quota | **HIGH** | `js/core/state.js:262, 300`, `js/canzoni.js:106, 120` | Multi-megabyte static caches exhaust 5MB quota, preventing user progress saves. |
| **VULN-STO-03** | Total absence of multi-tab concurrency sync (no `storage` event, no `BroadcastChannel`) | **HIGH** | `js/core/state.js`, `js/core.js`, `js/core/sync.ts` | Concurrent tabs silently overwrite and erase each other's XP, reviews, and sync queues. |
| **VULN-STO-04** | Non-atomic, unvalidated backup import causing Franken-state or startup crash | **HIGH** | `js/profilo.js:466-514`, `js/ia-import.js:624-760` | Ingesting corrupted/malformed backup permanently crashes the PWA with no rollback. |
| **VULN-STO-05** | Fragile `JSON.parse` across 28 files crashing on malformed storage or blocking export | **MEDIUM** | `js/profilo.js:427-454`, `js/canzoni.js:128-132`, `js/heatmap.js:35` | Single corrupt key prevents entire backup export and crashes views. |
| **VULN-STO-06** | Complete absence of automated tests for persistence, quota recovery, and backup integrity | **MEDIUM** | `tests/` | High regression risk across releases. |

---

### 4.2 Proposed Fix Strategy (Architectural Roadmap)

1. **Unified Storage Gateway (`js/core/storage.ts` or `js/core/storage.js`)**:
   - Provide a safe facade (`SafeStorage.get(key, fallback)`, `SafeStorage.set(key, val)`, `SafeStorage.remove(key)`).
   - Wrap all `JSON.parse` operations in safe parsing with schema defaults.
   - Detect all variants of `QuotaExceededError` (`e.name === 'QuotaExceededError'`, `e.code === 22`, etc.).
   - Implement an **Eviction Priority Ladder** upon quota exhaustion:
     1. Evict ephemeral SWR caches (`it_swr_templos_meta`, `it_swr_grammar`, `it_swr_canzoni`, `it_swr_storie`, `it_swr_dialogi`, `it_swr_imitazioni`).
     2. Evict old client error logs (`it_client_errors`).
     3. Evict expired translations from IndexedDB/cache.
     4. If flashcard pruning is strictly necessary, ensure pruned flashcards are immediately persisted to disk so space is actually recovered.
     5. If write still fails, trigger a high-visibility user alert toast (`"Armazenamento local cheio! Faça o download do seu backup nas configurações."`).
2. **Move Large Ephemeral SWR Caches out of LocalStorage**:
   - Static templates and SWR metadata should reside in `IndexedDB` or standard Cache API (`caches.open('app-swr-cache')`), keeping `localStorage` reserved exclusively for high-integrity user progress (< 500 KB).
3. **Cross-Tab Synchronization via `BroadcastChannel` & `StorageEvent`**:
   - Create a lightweight synchronization channel (`const channel = new BroadcastChannel('apprendimento_channel')`).
   - Listen to `window.addEventListener('storage', (e) => { ... })`:
     - When `e.key === 'it_progresso'`, use `AppCollaboration.resolver.reconciliarProgresso(local, remoto)` to merge progress without overwriting (union of unlocked temples, max of XP/level).
     - When `e.key === 'it_flashcards'`, merge updated cards using LWW on `lastReview`.
     - When `e.key === 'apprendimento_sync_queue'`, reload the queue in `AppSyncManager`.
4. **Atomic & Schema-Validated Backup Import with Staging**:
   - Implement strict schema validation (using runtime Zod schemas or robust type guard functions) verifying all required fields (`nivel`, `xp`, `streak`, `templos_desbloqueados: Array`, `conquistas: Array`).
   - **Atomic Transaction Pattern**:
     - Pre-flight test: serialize all keys and verify total byte size against available quota.
     - Create an in-memory backup snapshot of current `localStorage`.
     - Write to a temporary staging namespace (e.g. `it_import_stage_*`).
     - If all writes succeed, commit to live keys. If any write fails (e.g. QuotaExceeded), abort, purge staging keys, and restore original state with zero data corruption.
5. **Sanitization of Custom Imported Content**:
   - Run all imported textual fields (`titulo`, `frase`, `letra_raw`, `contexto`, `parola`) through `AppState.escapeHtml()` or a DOMPurify-equivalent sanitizer before saving and rendering to neutralize stored XSS.

---

### 4.3 Recommended Test Implementations (for R4 Framework)

1. `tests/storage_quota.test.ts`:
   - Simulate `localStorage.setItem` throwing `QuotaExceededError` (and code 22).
   - Verify that SWR caches are evicted first.
   - Verify that `_gcFlashcards()` persists the trimmed flashcard deck to localStorage.
   - Verify that user is notified and critical progress is preserved in memory/IndexedDB.
2. `tests/storage_corruption.test.ts`:
   - Inject malformed strings (truncated JSON, `"{ corrupted"`, `null`, `12345`, `[ "invalid" ]`) into `it_progresso`, `it_flashcards`, `it_diario`, and `it_canzoni_custom`.
   - Verify that `carregarProgresso()` and `carregarFlashcards()` fall back to canonical defaults without throwing unhandled exceptions.
   - Verify that `exportarDados()` does not crash when one key is corrupted, exporting whatever valid data is recoverable.
3. `tests/cross_tab_sync.test.ts`:
   - Simulate two tab contexts emitting `StorageEvent` for `it_progresso` and `it_flashcards`.
   - Verify that concurrent XP gains and flashcard reviews merge cleanly using CRDT union and max rules instead of overwriting.
4. `tests/backup_integrity.test.ts`:
   - Test importing valid v1, v2, v3, and v4 backups.
   - Test importing corrupted, partial, or maliciously crafted backups (XSS payloads, missing arrays, negative numbers, giant bookmark sets).
   - Verify atomic rollback if import is interrupted midway.

---

## 5. Verification Method

To independently verify all findings and baseline claims:

1. **Verify Baseline Tests**:
   ```bash
   npm test
   ```
   *Expected outcome*: 15 passed test files, 104 passed tests.
2. **Verify Baseline Production Build**:
   ```bash
   npm run build
   ```
   *Expected outcome*: `tsc` runs cleanly, Vite generates production bundle in `dist/` with exit code 0.
3. **Inspect Problematic Code Points**:
   - Run `grep -n -C 5 "this._gcFlashcards()" js/core/state.js` to observe that `_gcFlashcards()` is called inside `salvarProgresso()` and `salvarFlashcards()` without subsequently writing `flashcardData` to disk.
   - Run `grep -n -C 5 "_gcFlashcards()" js/core/state.js` to observe lines 183-197 modifying memory only.
   - Run `grep -rn "addEventListener('storage'" js/` and `grep -rn "BroadcastChannel" js/` to confirm zero cross-tab coordination.
   - Run `grep -n -C 10 "importarDados" js/profilo.js` to inspect lines 466-514 for lack of schema validation and lack of transactional atomicity.

---
*Report completed by Survey Explorer 1 for Orchestrator consolidation and downstream Phase 2/Phase 3 tasks.*
