# Project: Aprendimento Italiano — Deep Stress, Resilience & UX Optimization

## Architecture
- **Client Tier**: Pure Vanilla JavaScript/TypeScript PWA with zero external runtime dependencies (except Zod for schema validation).
- **Persistence Tier**: Hybrid LocalStorage (core user progress, flashcards, diary) + IndexedDB (`it_audio_db`, `it_canzoni_audio_db`) + Cache API.
- **State & Concurrency Management**: `AppState` reactive singleton, cross-tab synchronization via `BroadcastChannel` and `window.addEventListener('storage')`, CRDT-inspired reconciliation for offline/multi-tab updates.
- **Study Engines**: FSRS-4.5 spaced repetition scheduler and Ebbinghaus forgetting curve analytics.
- **Audio & Speech**: Web Audio API, Web Speech API / TTS, local Whisper/neural voice worker fallbacks.
- **Presentation & Ergonomics**: Responsive CSS layout (`css/italia.css`), accessible semantic components (WCAG 2.1 AA), PWA manifest and Service Worker.
- **Testing & Verification**: Vitest unit/integration runner, TypeScript typecheck (`tsc`), Vite production bundler.

---

## Feature Inventory
Every feature and vulnerability from the survey is inventoried below with its assigned milestone.

| # | Feature / Remediation | Description | Milestone | Source |
|---|-----------------------|-------------|-----------|--------|
| F1 | Storage Quota GC Persistence Fix | Fix `_gcFlashcards()` in `state.js` to persist pruned flashcards to `localStorage` so bytes are actually recovered during `QuotaExceededError`. Fix oxymoronic `f.state === 'new'` condition. | M1 | Survey 1 (VULN-STO-01) |
| F2 | SWR Ephemeral Cache Eviction Ladder | Evict multi-megabyte ephemeral caches (`it_swr_*`) and error logs (`it_client_errors`) before touching core flashcard data on quota errors. | M1 | Survey 1 (VULN-STO-02) |
| F3 | Cross-Tab Synchronization | Implement `BroadcastChannel('apprendimento_channel')` and `window.addEventListener('storage')` to reconcile `it_progresso`, `it_flashcards`, and `sync_queue` without LWW data clobbering. | M1 | Survey 1 (VULN-STO-03) |
| F4 | Safe Storage Gateway & Defensive Loading | Centralized `SafeStorage` facade with schema defaults, resilient to corrupted/primitive/null storage payloads and preventing startup crashes. | M1 | Survey 1 (VULN-STO-04, 05) |
| F5 | Atomic & Validated Backup Import/Export | Pre-flight schema validation, staging namespace with automatic rollback upon failure in `importarDados()`, and non-crashing `exportarDados()`. | M1 | Survey 1 (VULN-STO-04, 05) |
| F6 | Stored Content Sanitization | Sanitize custom imported songs, stories, and dialogues against XSS before storage and rendering. | M1 | Survey 1 (VULN-STO-04) |
| F7 | FSRS Mathematical Bounds & NaN Immunization | Implement `FSRS.sanitizeCard()` clamping difficulty `[1, 10]`, stability `[0.1, 36500]`, intervals `[1, 36500]`, and immunizing all FSRS formulas from `NaN`/`Infinity`. | M2 | Survey 2 |
| F8 | Temporal Anomaly & Clock Skew Handling | Handle reviews with `lastReview > now` (device clock desync / timezone shift) monotonically without negative intervals or historical distortion. | M2 | Survey 2 |
| F9 | Ebbinghaus Property Key Harmonization | Harmonize `lastReview` (camelCase) in `flashcards.js` with `getElapsedDays()` in `ebbinghausCurve.ts` and `ebbinghaus.js`, unfreezing retention projection from 90%. | M2 | Survey 2 |
| F10 | Study Flow Reentrancy & Double-Click Guards | Entry locks and debounce on `Flashcards.avaliar` and `Quiz.proximaPergunta`, preventing skipped cards/questions and duplicate XP awards. | M2 | Survey 2 |
| F11 | Cross-Section Audio/TTS Teardown | Teardown active TTS, `VoiceEngine`, story audio, and mic recording on section navigation in `AppNavigation.navegar()`. | M2 | Survey 2 |
| F12 | Audio Promise Rejection & VoiceEngine Fixes | Add `.catch()` to `_userAudioPlayer.play()` in `imitazione.js`, ignore `canceled` errors in `VoiceEngine.u.onerror`, and anchor utterances against GC. | M2 | Survey 2 |
| F13 | Keyboard Shortcut Conflict Resolution | Scope `core.js` global `1-5` navigation to ignore when in `flashcard` or `quiz` sections, or when modals are open; add `stopImmediatePropagation()` to `flashcards.js`. | M3 | Survey 3 |
| F14 | Quiz Keyboard Accessibility | Enable number keys `1-4` for answering quiz options and `Enter`/`Space` to advance to the next question. | M3 | Survey 3 |
| F15 | Viewport & PWA SW Resilience | Remove `maximum-scale=1.0, user-scalable=no` (WCAG 1.4.4); add `{ ignoreSearch: true }` in `sw.js`; decouple `controllerchange` from disruptive auto-reload. | M3 | Survey 3 |
| F16 | Mobile Overscroll & Bounce Containment | Add `overscroll-behavior: contain` to modal and container scrollable elements (`.tm-card`, `.ia-import-box`, `.ach-scroll-container`, lyrics). | M3 | Survey 3 |
| F17 | Touch Target Sizing (>= 44x44px) | Enlarge header utility buttons, mode toggles, flashcard buttons, and bottom-nav tabs to minimum 44x44px per WCAG 2.1 SC 2.5.5 / 2.5.8. | M3 | Survey 3 |
| F18 | Modal Focus Trapping & Accessibility | Route static modals through `ModalManager` or equip with focus trapping, Escape handling, and focus return. | M3 | Survey 3 |
| F19 | Quiz ARIA Feedback & Flashcard Semantics | Add `aria-live="polite"` and `role="status"` to quiz feedback, auto-focus "Continuar", and equip `#flashcard` with `role="button"` and keyboard trigger. | M3 | Survey 3 |
| F20 | Cognitive Pacing & Micro-Breaks | Introduce study session micro-break consolidation prompt after sustained review sets. | M3 | Survey 3 |
| F21 | High-Contrast Focus Ring in Dark Mode | Ensure `:focus-visible` outline in dark mode achieves >= 3:1 contrast ratio against dark backgrounds. | M3 | Survey 3 |
| F22 | Storage & Quota Automated Stress Tests | Implement fuzzing and quota stress tests in `tests/storage_quota.test.ts` and `tests/storage_corruption.test.ts`. | M4 | Survey 1 (R4) |
| F23 | Algorithmic & Concurrency Automated Stress Tests | Implement FSRS math stress tests (`tests/fsrs_math_stress.test.ts`) and audio/concurrency tests (`tests/audio_concurrency.test.ts`). | M4 | Survey 2 (R4) |
| F24 | Cross-Tab & Backup Integrity Automated Tests | Implement cross-tab sync tests (`tests/cross_tab_sync.test.ts`) and atomic backup validation tests (`tests/backup_integrity.test.ts`). | M4 | Survey 1, 2 (R4) |
| F25 | Continuous Improvement Roadmap | Document long-term architectural and UX evolution in `docs/CONTINUOUS_IMPROVEMENT_ROADMAP.md`. | M4 | R4 requirement |
| F26 | E2E Opaque-Box Test Suite & Hardening | Opaque-box requirement-driven test suite (Tiers 1-4) + Adversarial coverage hardening (Tier 5). | M-FINAL | Dual Track requirement |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Storage, Persistence & Data Resilience | F1, F2, F3, F4, F5, F6 | none | PLANNED |
| M2 | Algorithmic Stability, FSRS & Concurrency Guards | F7, F8, F9, F10, F11, F12 | none | PLANNED |
| M3 | UX, Ergonomics, PWA Resilience & A11y Standards | F13, F14, F15, F16, F17, F18, F19, F20, F21 | none | PLANNED |
| M4 | Continuous Improvement Framework & Test Suites | F22, F23, F24, F25 | M1, M2 | PLANNED |
| M-FINAL | E2E Test Suite Pass (100%) & Adversarial Hardening | F26 (Tiers 1-5 validation, build code 0, final synthesis) | M1, M2, M3, M4, TEST_READY.md | PLANNED |

---

## Interface Contracts

### M1 ↔ App Core & Other Modules (`SafeStorage` / State)
- `SafeStorage.getItem(key: string, fallback?: any): any`
- `SafeStorage.setItem(key: string, value: any): boolean` (returns true on success; automatically manages eviction ladder on `QuotaExceededError`)
- `SafeStorage.removeItem(key: string): void`
- `AppState.reconciliarProgresso(local: ProgressState, remoto: ProgressState): ProgressState` (pure CRDT merge)
- Event: `BroadcastChannel('apprendimento_channel').postMessage({ type: 'SYNC_UPDATE', key: string, payload: any })`

### M2 ↔ Flashcards & Analytics (`FSRS` / Ebbinghaus)
- `FSRS.sanitizeCard(card: FSRSCardInput): FSRSCard` (guarantees finite numbers, clamped `difficulty` in `[1, 10]`, `stability` in `[0.1, 36500]`, non-negative reps/lapses)
- `Ebbinghaus.getElapsedDays(card: { lastReview?: number, last_review?: number }): number | null`
- Guard interface: `Flashcards._bloqueioAvaliacao: boolean`, `Quiz._bloqueioAvanco: boolean`
- Audio lifecycle contract: `AppNavigation.navegar(secao)` calls centralized `teardownAudio()` terminating TTS, worker voice synthesis, recording, and story audio.

### M3 ↔ UX / Modals / Layout
- Keyboard routing contract: `core.js` keydown listener checks `e.defaultPrevented`, active section !== 'flashcard' && !== 'quiz', and no active dialog before navigating.
- Modal contract: All dialogs implement standard trap focus, Escape key dismiss, and aria attribute toggles (`aria-hidden`, `aria-modal="true"`).

---

## Code Layout & Write Boundaries

To prevent concurrent worker collisions, each milestone has strict exclusive write ownership:

- **Milestone 1 Exclusively Owns**:
  - `js/core/storage.js` (new SafeStorage gateway)
  - `js/core/state.js` (quota GC, safe parsing, reconciler integration)
  - `js/core/sync.ts` (cross-tab queue sync)
  - `js/profilo.js` (import/export validation and atomicity)
  - `js/audio_cache.js` (IndexedDB version change handling)

- **Milestone 2 Exclusively Owns**:
  - `js/flashcards.js` (FSRS sanitization, bounds, review monotonic logic, reentrancy guard)
  - `src/analytics/ebbinghausCurve.ts` and `js/ebbinghaus.js` (property key harmonization)
  - `js/quiz.js` (advance debounce, double XP prevention, keyboard integration)
  - `js/core/navigation.js` (audio/TTS teardown on navigation)
  - `js/imitazione.js` (`play().catch()` and microphone teardown)
  - `js/voice_engine.ts` (session invalidation, error handling)
  - `js/vocab.js` (utterance anchoring)

- **Milestone 3 Exclusively Owns**:
  - `js/core.js` (global keyboard shortcut scoping)
  - `index.html` (viewport meta, flashcard button semantics, aria-live regions)
  - `sw.js` (cache matching `ignoreSearch`, reload decoupling)
  - `css/italia.css` (touch targets >= 44px, overscroll containment, dark mode contrast)
  - `manifest.webmanifest` (icon definitions, orientation adjustment)
  - `js/modal_manager.ts` (static modal unification)

- **Milestone 4 Exclusively Owns**:
  - `tests/storage_quota.test.ts`
  - `tests/storage_corruption.test.ts`
  - `tests/cross_tab_sync.test.ts`
  - `tests/backup_integrity.test.ts`
  - `tests/fsrs_math_stress.test.ts`
  - `tests/audio_concurrency.test.ts`
  - `tests/keyboard_concurrency.test.ts`
  - `docs/CONTINUOUS_IMPROVEMENT_ROADMAP.md`

- **E2E Testing Track Exclusively Owns**:
  - `tests/e2e/` (opaque-box requirement-driven test suite across Tiers 1-4)
  - `TEST_INFRA.md`
  - `TEST_READY.md`
