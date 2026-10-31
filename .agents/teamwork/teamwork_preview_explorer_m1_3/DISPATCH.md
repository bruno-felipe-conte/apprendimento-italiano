## 2026-10-31T00:40:57Z
You are Explorer M1.3 (Schema Validation, Atomic Backup & Content Sanitization).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_3/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_1/handoff.md

Objective:
Detail the exact implementation blueprint for features F4, F5, and F6 (Milestone 1):
1. Defensive schema validation for `carregarProgresso()` and `carregarFlashcards()` in `js/core/state.js` preventing crashes if payload is string, number, null, or corrupted object missing arrays.
2. Atomic & validated backup import in `js/profilo.js` (`importarDados`):
   - Pre-flight schema validation of all required subfields.
   - Transactional staging pattern: backup in-memory state, write to temporary staging keys (`it_stage_*`), commit to live keys only if all pass, automatic rollback on error.
   - Bookmarks sanitization: limit key count, check regex `/^it_book_bm_[a-zA-Z0-9_-]+$/`.
3. Safe export in `js/profilo.js` (`exportarDados`): wrap each key parse in try/catch so one corrupted key does not crash export.
4. Stored XSS sanitization: sanitize imported songs, stories, and dialogues in `js/canzoni.js`, `js/storie.js`, `js/dialoghi.js` and `js/profilo.js`.

Scope Boundaries:
- READ-ONLY: Do NOT modify code. Provide code-level blueprints, diffs, and verification commands.
- Output handoff to:
  /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_3/handoff.md
- Send completion message to orchestrator_1.
