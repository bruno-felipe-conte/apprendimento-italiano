# BRIEFING — 2026-10-31T00:07:30Z

## Mission
Investigate algorithms (FSRS/forgetting curve), math edge cases, temporal edge cases, audio/TTS lifecycle, and concurrency/race conditions across the codebase.

## 🔒 My Identity
- Archetype: explorer
- Roles: survey_2 (Algorithms, State Machines, Audio & Concurrency)
- Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_2
- Original parent: d325678e-ec9a-40b2-9b89-5f56cec87dab
- Milestone: codebase-survey

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Do NOT modify or create source code or tests
- Do NOT fix bugs yourself
- Strictly diagnostic mapping and risk analysis

## Current Parent
- Conversation ID: d325678e-ec9a-40b2-9b89-5f56cec87dab
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `js/flashcards.js` (FSRS algorithm, rating UI, keydown shortcuts, gestures)
  - `src/analytics/ebbinghausCurve.ts` & `js/ebbinghaus.js` (Ebbinghaus mathematical projection, retention, stability calculation)
  - `js/progression.ts` (Level-up, XP calculation, daily streak reset, goal deadlines)
  - `js/quiz.js` (Question flow, answer verification, double-click on Continuar, XP calculation)
  - `js/core.js` & `js/core/navigation.js` (Global keydown listeners, section navigation, tab switching teardown)
  - `js/audio.js`, `js/audio_cache.js`, `js/core/tts.js`, `js/voice_engine.ts` (AudioContext, Web Speech API, IndexedDB cache, worker synthesis)
  - `js/storie.js` & `js/imitazione.js` (Story speech chunking, user recording, SpeechRecognition lifecycle)
  - `scripts/validate-fsrs.js`, `tests/*.test.{ts,js}` (Unit test coverage survey)
- **Key findings**:
  1. FSRS has no clamp or NaN guards; unhandled undefined/NaN inputs permanently corrupt cards.
  2. Ebbinghaus `getElapsedDays` searches `card.last_review`, but `flashcards.js` saves `lastReview`, causing curve to always fall back to default retention target.
  3. Keyboard collision in `core.js`: Keys 1-4 navigate away during flashcard review instead of rating.
  4. Missing reentrancy guard in `Flashcards.avaliar` causes double evaluation, duplicate XP, and card skipping.
  5. Quiz "Continuar" lacks debounce; double clicks skip questions or grant duplicate XP.
  6. Missing audio/TTS cancellation in `AppNavigation.navegar()` allows background voice leakage.
  7. `_userAudioPlayer.play()` in `imitazione.js` lacks `.catch()`, risking `UnhandledPromiseRejection`.
- **Unexplored areas**: None within the survey scope. Complete diagnostic handoff produced.

## Key Decisions Made
- Fully documented all 10 diagnostic vectors with exact file paths, lines, and proposed fix strategies in `handoff.md`.

## Artifact Index
- DISPATCH.md — incoming dispatch instructions
- BRIEFING.md — persistent working memory
- progress.md — liveness heartbeat and execution log
- handoff.md — final comprehensive survey report
