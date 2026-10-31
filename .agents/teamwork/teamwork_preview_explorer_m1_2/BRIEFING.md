# BRIEFING — 2026-10-31T00:47:30Z

## Mission
Investigate and design the exact implementation blueprint for Multi-Tab Concurrency & Synchronization (F3) including BroadcastChannel, localStorage event fallback, CRDT-like merge reconciliation for it_progresso and it_flashcards, apprendimento_sync_queue synchronization, and IndexedDB audio_cache onversionchange deadlock prevention.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigator, architect, blueprint designer
- Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_2
- Original parent: d325678e-ec9a-40b2-9b89-5f56cec87dab
- Milestone: Milestone 1 (M1.2 Multi-Tab Concurrency & Synchronization)

## 🔒 Key Constraints
- Read-only investigation — do NOT modify application source code
- Provide complete code-level blueprints, diffs/patches, and verification commands
- Output handoff to /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_2/handoff.md
- Send completion message to parent (d325678e-ec9a-40b2-9b89-5f56cec87dab)

## Current Parent
- Conversation ID: d325678e-ec9a-40b2-9b89-5f56cec87dab
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `ORIGINAL_REQUEST.md`, `PROJECT.md`, `teamwork_preview_explorer_survey_1/handoff.md`
  - `js/core/state.js`, `js/core/sync.ts`, `js/audio_cache.js`, `js/core/collaboration.ts`
  - `js/flashcards.js`, `js/core/stats.js`, `js/core/xp.js`, `js/heatmap.js`, `js/canzoni.js`
  - `tests/collaboration.test.ts`, `tests/sync.test.ts`
- **Key findings**:
  1. Zero cross-tab sync currently exists in `state.js` or `sync.ts`; multi-tab writes result in LWW clobbering.
  2. `ConflictResolver` in `collaboration.ts` provides existing CRDT math, but `AppState` does not expose or call `reconciliarProgresso` or `reconciliarFlashcards`.
  3. `AudioCache` lacks `onversionchange`, `onclose`, and `onblocked` handlers on `IDBDatabase`, creating deadlock whenever schema upgrade is triggered across open tabs.
  4. `SyncManager` queue in `js/core/sync.ts` is in-memory only without cross-tab lock or reloading on foreign writes, leading to dropped offline queue items and duplicate concurrent flushes.
- **Unexplored areas**: None for M1.2 scope.

## Key Decisions Made
- Use `BroadcastChannel('apprendimento_channel')` as primary real-time transport with automatic fallback to `window.addEventListener('storage', ...)`.
- Attach pure, defensive `AppState.reconciliarProgresso(local, remoto)` and `AppState.reconciliarFlashcards(local, remoto)` directly in `js/core/state.js` with idempotent union/max logic and LWW on `lastReview`/`reps`.
- Equip `SyncManager` in `js/core/sync.ts` with cross-tab queue reload, channel broadcast on mutation, and cross-tab concurrency lease lock to serialize `flush()`.
- Add `onversionchange`, `onclose`, `onblocked`, and explicit `fechar()` to `AudioCache` in `js/audio_cache.js`.

## Artifact Index
- DISPATCH.md — Recorded dispatch instructions
- BRIEFING.md — Persistent working memory
- progress.md — Liveness heartbeat and step tracking
- handoff.md — Final 5-component handoff report
