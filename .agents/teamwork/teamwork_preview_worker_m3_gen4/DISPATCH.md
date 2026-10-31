# Dispatch: Worker M3 (Gen 4)

## Objective
Implement Milestone 3: UX, Ergonomics, PWA Resilience & A11y Standards (Features F13–F21).

## Working Directory
`/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3_gen4/`

## Context & Inputs
- `ORIGINAL_REQUEST.md`: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md`
- `PROJECT.md`: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md`
- Survey Explorer 3 Report: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_3/handoff.md`

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Feature Implementation Details (F13–F21)
1. **F13: Keyboard Shortcut Conflict Resolution (`js/core.js`)**:
   - In `js/core.js`, scope global `1-5` navigation keydown listener to check:
     * active section is NOT 'flashcard' and NOT 'quiz'
     * no modal or dialog is open (`document.querySelector('.modal.ativo, .tm-overlay:not([style*="display: none"]), dialog[open]')`)
     * event is not defaultPrevented
   - In `js/flashcards.js`, ensure rating keys `1-4` call `e.stopImmediatePropagation()`.
2. **F14: Quiz Keyboard Accessibility (`js/quiz.js` / `js/core.js`)**:
   - Enable number keys `1-4` to select options on active quiz question.
   - Enable `Enter` and `Space` to advance ("Próxima pergunta" / "Continuar") when answer is already checked.
3. **F15: Viewport & PWA SW Resilience (`index.html`, `sw.js`, `manifest.webmanifest`)**:
   - In `index.html`: Change `<meta name="viewport">` to `width=device-width, initial-scale=1.0, viewport-fit=cover` (remove `maximum-scale=1.0, user-scalable=no` for WCAG 1.4.4 compliance).
   - In `index.html`: Decouple `navigator.serviceWorker.addEventListener('controllerchange')` from immediate disruptive reload. If a session is active, do not force reload; show a non-intrusive toast or update notice.
   - In `sw.js`: Add `{ ignoreSearch: true }` to `caches.match()` calls so versioned query strings match cached assets cleanly.
   - In `manifest.webmanifest`: Change `orientation: "portrait-primary"` to `"any"` to support tablets/desktop-convertibles.
4. **F16: Mobile Overscroll & Bounce Containment (`css/italia.css`)**:
   - Add `overscroll-behavior: contain` and `-webkit-overflow-scrolling: touch` to nested scroll containers:
     `.tm-card`, `.ia-import-box`, `.ach-scroll-container`, `.cloze-lyrics-stage`, `.can-lyrics-area`, `.app-sidebar`, `.app-sidebar .nav-tabs`.
5. **F17: Touch Target Sizing (>= 44x44px WCAG 2.1 SC 2.5.5 / 2.5.8) (`css/italia.css`)**:
   - Header utility buttons (`#theme-toggle`, `#btn-som`, `#btn-audio-speed`, help, profile): replace 32x32px mobile styles with `min-width: 44px; min-height: 44px; display: inline-flex; align-items: center; justify-content: center;`.
   - Flashcard mode toggles (`.btn-modo-toggle`): enlarge to min 44x44px.
   - Flashcard toolbelt buttons (`.fc-tool-btn`) and language pill: ensure min 44px touch targets.
   - Sidebar navigation tabs (`.app-sidebar .nav-tab`): min-height 44px.
   - Bottom navigation tabs (`.bottom-nav button`): min-height 44px and responsive touch area.
6. **F18: Modal Focus Trapping & Accessibility (`js/modal_manager.ts`, `index.html`)**:
   - Ensure all static modals (`#templo-modal`, `#conquista-modal`, `#levelup-modal`, `#onboarding-modal`, `#modal-meta-prazo`, `#ia-import-modal`) integrate focus trapping, `Escape` key dismissal, and return focus to triggering element. Set `aria-modal="true"` and appropriate ARIA roles.
7. **F19: Quiz ARIA Feedback & Flashcard Semantics (`index.html`, `js/quiz.js`)**:
   - In `index.html`: Add `role="button"`, `tabindex="0"`, `aria-label="Card de memorização. Pressione Enter ou Espaço para virar"` to `#flashcard`, and add keydown listener (Enter/Space to flip).
   - In `index.html` & `js/quiz.js`: Add `role="status"` and `aria-live="polite"` to `#explicacao-container`. Auto-focus the advance button when an answer is evaluated.
8. **F20: Cognitive Pacing & Micro-Breaks (`js/flashcards.js`)**:
   - Introduce a gentle micro-break suggestion prompt after 20 continuous card reviews ("Ottimo lavoro! Fai una pausa di 1 minuto para consolidare la memoria").
9. **F21: High-Contrast Focus Ring in Dark Mode (`css/italia.css`)**:
   - In `body.dark-mode :focus-visible`, set outline color with >= 3:1 contrast ratio against `#1A1510` (e.g., `#FFD166` or `--cor-oro`).

## Verification Requirements
- Run `npm run build:ts`
- Run `npx vite build`
- Run `npm test`
- Run `graphify update .`

## Output
Write `handoff.md` in your working directory with sections: Observation, Logic Chain, Caveats, Conclusion, Verification Method.


## 2026-10-31T09:00:39Z
You are Worker M3 (Gen 4).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3_gen4/
Read your task dispatch in: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3_gen4/DISPATCH.md
Read the original user request in: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
Read the project master plan in: /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
Read the Survey 3 findings in: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_3/handoff.md

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task is to implement Milestone 3: UX, Ergonomics, PWA Resilience & A11y Standards (Features F13–F21):
- F13: Keyboard shortcut conflict resolution in js/core.js
- F14: Quiz keyboard accessibility (keys 1-4 for choices, Enter/Space for advance)
- F15: Viewport meta tag (remove user-scalable=no, max-scale=1.0), SW cache ignoreSearch: true, decouple controllerchange auto-reload, manifest orientation: any
- F16: Mobile overscroll & bounce containment in css/italia.css
- F17: Touch target sizing (>= 44x44px) for header utility buttons, mode toggles, flashcard toolbelt, sidebar/bottom nav
- F18: Modal focus trapping, Escape key handling, and focus return in js/modal_manager.ts and index.html
- F19: Quiz ARIA feedback (aria-live/role status on explanation) and #flashcard button semantics (role=button, tabindex=0, aria-label, Enter/Space key flip)
- F20: Cognitive pacing & micro-break reminder after 20 continuous flashcard reviews
- F21: High-contrast focus-visible ring in dark mode (>= 3:1 contrast ratio)

Exclusive Write Boundaries:
js/core.js, index.html, sw.js, css/italia.css, manifest.webmanifest, js/modal_manager.ts (and minor adjustments to js/quiz.js / js/flashcards.js if required for keyboard/microbreak).

Verification:
- Run `npm run build:ts`
- Run `npx vite build`
- Run `npm test`
- Run `graphify update .`

Produce handoff.md in your working directory with Observation, Logic Chain, Caveats, Conclusion, and Verification Method.
Send a completion message with your handoff path back to the caller using send_message.
