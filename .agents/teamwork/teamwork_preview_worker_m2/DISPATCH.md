## 2026-10-31T04:40:01Z
You are Worker M2 (type: teamwork_preview_worker).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m2/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m2/DISPATCH.md
4. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/handoff.md
5. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_2/handoff.md
6. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_3/handoff.md

Your exclusive write boundaries:
- js/flashcards.js
- src/analytics/ebbinghausCurve.ts
- js/ebbinghaus.js
- js/quiz.js
- js/core/navigation.js
- js/imitazione.js
- js/voice_engine.ts
- js/vocab.js

Implement all 6 features (F7, F8, F9, F10, F11, F12) per the exact specifications and code designs in the 3 Explorer handoff reports:
- F7 & F8: FSRS Math Bounds, NaN Immunization & Clock Skew in js/flashcards.js. Add FSRS.sanitizeCard(), immunize formulas, handle lastReview > now gracefully, emit both lastReview and last_review, expose FSRS globally.
- F9: Ebbinghaus Harmonization in src/analytics/ebbinghausCurve.ts and js/ebbinghaus.js. Check card.lastReview ?? card.last_review in getElapsedDays, export getElapsedDays, pass currentR to predictNextStabilityGood.
- F10: Reentrancy & Double-Click Guards in js/flashcards.js (Flashcards.avaliar guard) and js/quiz.js (Quiz.proximaPergunta debounce guard & idempotent mostrarResultado).
- F11: Cross-Section Audio Teardown in js/core/navigation.js. Stop all active speech, VoiceEngine, Storie audio, Imitazione, Flashcards recording, and Canzoni.
- F12: Audio Promise Rejection Safety & VoiceEngine Fixes in js/imitazione.js (play().catch() & sync mediaStream track cleanup), js/voice_engine.ts (epoch invalidation, worker AbortError, suppress canceled in u.onerror), and js/vocab.js (utterance anchoring).

Verification requirements:
Run:
- npm run build:ts
- npx vite build
- npx vitest run tests/ebbinghaus.test.ts tests/ebbinghausCurve.test.ts tests/voice_engine.test.ts tests/navigation.test.ts tests/e2e/tier1_feature_coverage.test.ts tests/e2e/tier2_boundary_corner.test.ts
- graphify update .

Write handoff report to /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m2/handoff.md.
Send completion message to caller when done.

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
