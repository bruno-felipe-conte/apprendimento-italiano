## 2026-10-31T00:52:18Z
You are Worker M1 (Implementation of Milestone 1: Storage, Persistence & Data Resilience).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m1/

You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. The 3 Explorer blueprints:
   - /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_1/handoff.md (SafeStorage, Eviction Ladder, Quota Detection)
   - /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_2/handoff.md (BroadcastChannel, StorageEvent, CRDT Reconciliation, Sync Lock, IndexedDB VersionChange)
   - /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_3/handoff.md (Defensive Schema Validation, Atomic Staging & Rollback Backup, Safe Export, XSS Sanitization)

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Exclusive Write Boundaries:
You own and can modify:
- js/core/storage.js (create new file per M1.1 blueprint)
- js/core/state.js (integrate SafeStorage, Eviction Ladder, Cross-Tab Sync, CRDT reconciliation, and defensive schema validation per blueprints)
- js/core/sync.ts (integrate cross-tab queue reload and mutual-exclusion lease lock per M1.2 blueprint)
- js/profilo.js (integrate atomic staging import with rollback, safe export, and bookmark sanitization per M1.3 blueprint)
- js/audio_cache.js (add onversionchange, onclose, and onblocked handlers per M1.2 blueprint)
- index.html (add `<script src="js/core/storage.js?v=162"></script>` immediately before `js/core/state.js`)
DO NOT modify files outside your boundary.

Implementation Tasks:
1. Create `js/core/storage.js`: Universal SafeStorage gateway, memory fallback, multi-engine QuotaExceededError detection, 4-step Eviction Priority Ladder (Step 1: SWR caches, Step 2: client logs, Step 3: flashcards GC, Step 4: alert toast).
2. Update `js/core/state.js`:
   - Replace direct localStorage calls with SafeStorage.
   - Implement `_sanitizeProgresso()` and `_sanitizeFlashcards()`.
   - Implement `_gcFlashcards(persistir = true)` fixing the oxymoron and ensuring pruned deck is actually written to disk.
   - Implement cross-tab sync (`BroadcastChannel` + `storage` event fallback) and pure CRDT `reconciliarProgresso` and `reconciliarFlashcards`.
   - Wire up eviction ladder handlers at priority 3 (GC) and priority 4 (alert toast).
3. Update `js/core/sync.ts`: Add `tabId`, cross-tab queue reload via `BroadcastChannel`/`storage`, and mutual-exclusion `apprendimento_sync_lock` (15s lease) in `flush()`.
4. Update `js/profilo.js`:
   - In `exportarDados()`: wrap storage parsing in `_safeParseStorage()` so broken keys don't abort export.
   - In `importarDados()`: implement `_validarPayloadBackup()`, `_sanitizarBookmarks()`, and 2-phase transactional staging (`it_stage_*`) with automatic rollback to snapshot on failure.
5. Update `js/audio_cache.js`: Add `db.onversionchange` (closes connection and nulls `_dbPromise`), `db.onclose`, `req.onblocked`, and `fechar()`.
6. Update `index.html`: Add `<script src="js/core/storage.js?v=162"></script>`.

Verification:
- Run `npm test` (or `npx vitest run`) and ensure all existing tests pass with 0 regressions.
- Run `npm run build` (tsc + vite build) and ensure build succeeds with exit code 0.

Output Requirements:
- Write your complete handoff report to:
  /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m1/handoff.md
- Include: Observation (files changed, line numbers), Logic Chain, Build & Test output, Caveats, and Verification Commands.
- Send completion message to orchestrator_1.
