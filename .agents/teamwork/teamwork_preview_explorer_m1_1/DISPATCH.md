## 2026-10-31T00:40:37Z
You are Explorer M1.1 (Storage Gateway & Quota Eviction).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_1/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_1/handoff.md

Objective:
Detail the exact implementation blueprint for features F1, F2, and F4 (Milestone 1):
1. Design `js/core/storage.js` (or `SafeStorage` module): API contracts, safe parsing, error fallbacks, and QuotaExceededError variant detection across browser engines.
2. Design the Eviction Priority Ladder in `salvarProgresso()` and `salvarFlashcards()` in `js/core/state.js`:
   - Step 1: Evict ephemeral SWR network caches (`it_swr_templos_meta`, `it_swr_grammar`, `it_swr_canzoni`, `it_swr_dialogi`, `it_swr_storie`, `it_swr_imitazioni`).
   - Step 2: Evict client error logs (`it_client_errors`).
   - Step 3: Prune stale flashcards via corrected `_gcFlashcards()` ensuring pruned cards are ACTUALLY written to `localStorage` so bytes are freed. Fix the `f.state === 'new'` condition.
   - Step 4: Display user-visible alert toast when storage remains exhausted.

Scope Boundaries:
- READ-ONLY: Do NOT modify code. Provide code-level blueprints, diffs, and verification commands.
- Output handoff to:
  /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_1/handoff.md
- Send completion message to orchestrator_1.
