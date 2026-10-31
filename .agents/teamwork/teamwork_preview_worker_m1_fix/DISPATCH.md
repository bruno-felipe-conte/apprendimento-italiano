## 2026-10-31T04:23:23Z
You are Worker M1 Remediation (type: teamwork_preview_worker).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m1_fix/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_reviewer_m1_1/handoff.md

Your exclusive write boundaries:
- js/core/storage.js
- js/core/state.js
- js/core/sync.ts
- js/profilo.js
- js/audio_cache.js

Your task is to implement the exact fixes requested in Reviewer M1.1 report (Section 3: Findings 1 through 6):
1. [Finding 1 - Critical] In js/core/storage.js: isStorageAvailable() must catch QuotaExceededError and return true instead of false (quota full means storage is present and usable, allowing eviction ladder to run and data to be read).
2. [Finding 2 - Critical] In js/core/sync.ts: flush() must reload current disk queue from localStorage before filtering out processed batch items, avoiding clobbering concurrent offline items written by other tabs while the network batch was in-flight.
3. [Finding 3 - Major] In js/core/storage.js: isQuotaExceeded() must refine keyword matching so generic 'exceeded' does not match 'Maximum call stack size exceeded'.
4. [Finding 4 - Major] In js/core/storage.js: In Eviction Ladder Step 2, account for staging key bytes freed: bytesFreedStep2 += (k.length + val.length) * 2 when removing it_stage_*, it_temp_*, it_import_stage_*.
5. [Finding 5 - Minor] In js/core/state.js: _gcFlashcards() should return removidos + historyTruncated so Step 3 callback recognizes history compaction as freed space.
6. [Finding 6 - Minor] In js/profilo.js: In _sanitizarBookmarks, use Object.create(null) for dictionary mapping.

Verification requirements:
Run `npm run build:ts`, `npx vite build`, and `npx vitest run tests/adversarial_concurrency_rollback.test.ts tests/sync.test.ts tests/e2e/tier1_feature_coverage.test.ts tests/e2e/tier2_boundary_corner.test.ts`. All must pass with exit code 0.

Document your work in /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m1_fix/handoff.md.
When finished, send a message to caller with your handoff summary.

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
