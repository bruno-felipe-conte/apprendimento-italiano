## 2026-10-31T00:40:57Z
You are Explorer M1.2 (Multi-Tab Concurrency & Synchronization).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_2/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_1/handoff.md

Objective:
Detail the exact implementation blueprint for feature F3 (Milestone 1):
1. Cross-tab synchronization via `BroadcastChannel('apprendimento_channel')` and fallback to `window.addEventListener('storage', ...)`.
2. Safe reconciliation of `it_progresso`: merge logic in `AppState` avoiding LWW data loss (union of unlocked temples and achievements, max of level and XP, latest daily streak).
3. Safe reconciliation of `it_flashcards`: merge updated cards by latest `lastReview` timestamp.
4. Synchronization of `apprendimento_sync_queue` in `js/core/sync.ts` across open tabs.
5. Prevent IndexedDB version change deadlock in `js/audio_cache.js` (`onversionchange` listener closing open db connection).

Scope Boundaries:
- READ-ONLY: Do NOT modify code. Provide code-level blueprints, diffs, and verification commands.
- Output handoff to:
  /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_2/handoff.md
- Send completion message to orchestrator_1.
