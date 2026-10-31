# Survey Report & Handoff — UX, Ergonomics, PWA, A11y & Frontend Architecture

**Agent**: Survey Explorer 3 (UX, Ergonomics, PWA, a11y & Frontend Architecture)  
**Date**: 2026-10-30T21:08:00Z  
**Target Milestone**: Survey & Diagnostic Mapping (R2/R3/R4)  
**Integrity Mode**: Read-Only Investigation  

---

## 1. Observation

### 1.1 PWA Configuration, Manifest & Service Worker
- **Viewport Meta Tag (`index.html:7`)**:
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  ```
  `user-scalable=no` and `maximum-scale=1.0` restrict pinch-to-zoom on mobile devices, preventing low-vision users from scaling text, violating WCAG 2.1 Success Criterion 1.4.4 (Resize text).
- **Web App Manifest (`manifest.webmanifest:1-46`)**:
  - `icons` (`lines 15-28`) only defines `./icons/icon.svg` (`type="image/svg+xml"`). Lacks standardized PNG launcher icons (`192x192`, `512x512`) required for iOS Safari home screen bookmarking and older Android Chromium splash screens.
  - `orientation: "portrait-primary"` (`line 12`) forces portrait lock on devices that support manifest orientation, breaking ergonomic horizontal usage on tablets and desktop-convertibles.
- **Service Worker Lifecycle & Cache Versioning (`sw.js` vs `index.html`)**:
  - `sw.js:9`: Cache identifier is `const CACHE = 'italiano-v158';`.
  - `sw.js:16-106`: `STATIC` pre-cache table lists stale version strings, e.g.:
    `./css/italia.css?v=97`, `./js/dialoghi.js?v=99`, `./js/canzoni.js?v=99`, `./js/imitazione.js?v=99`, `./js/grammar.js?v=99`, `./js/ia-import.js?v=91`.
  - `index.html:11, 622-658`: Loads newer versioned assets:
    `<link rel="stylesheet" href="css/italia.css?v=159">`, `js/dialoghi.js?v=157`, `js/canzoni.js?v=156`, `js/grammar.js?v=159`.
  - `sw.js:176-184`: Cache matching uses default `caches.match(req)` without `{ ignoreSearch: true }`. If network is unavailable on first launch with mismatched version queries, scripts fail to resolve from cache.
  - `sw.js:117, 127`: Calls `self.skipWaiting()` and `self.clients.claim()`.
  - `index.html:694-696`:
    ```javascript
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      window.location.reload();
    });
    ```
    An immediate activation reload destroys active student sessions (in-progress quizzes, flashcard reviews, audio recording) without confirmation.

### 1.2 Overscroll, Pull-to-Refresh & Bounce Behavior
- **Global Rules**:
  - `css/italia.css:63-65`: `html { overscroll-behavior: none; overscroll-behavior-y: none; overscroll-behavior-x: none; }`
  - `css/italia.css:80-82`: `body { overscroll-behavior: none; overscroll-behavior-y: none; overscroll-behavior-x: none; }`
  - `css/italia.css:4652-4653`: `.app-header { overscroll-behavior: none; touch-action: none; }`
- **Missing Nested Scroll Container Containment**:
  Nested scroll containers lack `overscroll-behavior: contain` (or `none`), resulting in scroll chaining and pull-to-refresh / rubber-band triggers when reaching boundaries:
  - Temple modal card: `.tm-card` (`css/italia.css:4917`: `max-height:88vh; overflow-y:auto;`)
  - AI Import modal box: `.ia-import-box` (`css/italia.css:6952`: `max-height:92vh; overflow-y:auto;`)
  - Achievements scroll container: `.ach-scroll-container` (`css/italia.css:596-603`: `max-height: 250px; overflow-y: auto;`)
  - Cloze lyrics stage: `.cloze-lyrics-stage` (`css/italia.css:1998-2009`: `max-height: 48vh; overflow-y: auto;`)
  - Canzoni lyrics area: `.can-lyrics-area` (`css/italia.css:7768`: `overflow-y:auto;`)
  - Sidebar and sidebar tab list: `.app-sidebar` (`css/italia.css:4269`: `overflow-y: auto;`), `.app-sidebar .nav-tabs` (`css/italia.css:4330`: `overflow-y: auto;`)

### 1.3 Accessibility (a11y) Violations & Touch Targets (WCAG 2.1)
- **Interactive Touch Targets below 44x44px (WCAG 2.1 SC 2.5.5 / 2.5.8)**:
  - Header Utility Buttons on Mobile (`css/italia.css:1739-1748`):
    ```css
    @media (max-width: 640px) {
      .theme-toggle-btn {
        min-width: 32px !important;
        min-height: 32px !important;
        padding: 0.14rem 0.24rem !important;
        border-radius: 8px !important;
      }
    }
    ```
    Affects: `#theme-toggle`, `#btn-som`, `#btn-audio-speed`, help button, and profile button. Shrunk to 32x32px on the very viewports where touch accuracy is critical.
  - Flashcard Mode Toggles (`css/italia.css:5004`):
    ```css
    .btn-modo-toggle { width: 32px; height: 32px; border-radius: 50%; ... }
    ```
    Explicitly sized at 32x32px.
  - Language Pill Button (`css/italia.css:331-355`):
    `padding: 0.18rem 0.22rem !important;` with 0.7rem text. Total rendered height is ~26px.
  - Flashcard Toolbelt Buttons (`css/italia.css:2928-2938`):
    `.fc-tool-btn { padding: 0.45rem 0.9rem; font-size: 0.82rem; }` (~32-34px height).
  - Sidebar Navigation Tabs (`css/italia.css:4334-4340`):
    `.app-sidebar .nav-tab { height: 42px; min-height: 42px; padding: 0 8px; }` (42px < 44px).
  - Mobile Bottom Navigation Bar (`css/italia.css:441-458`):
    `@media (max-width: 1023px) { .bottom-nav button { flex: 1 1 0; min-width: 0; padding: 0.3rem 0.1rem 0.2rem; } }`
    All 9 section tabs are placed in a single row without horizontal overflow. On standard 360px mobile viewports, width is 360px / 9 = 40px per button; on 320px screens, width is 35.5px.
- **Severe Keyboard Shortcut Collision**:
  - Global navigation listener in `js/core.js:161-167`:
    ```javascript
    document.addEventListener('keydown', (e) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)) return;
      const mapa = { '1': 'templi', '2': 'flashcard', '3': 'quiz', '4': 'vocabolario', '5': 'grammatica' };
      if (mapa[e.key]) this.navegar(mapa[e.key]);
    });
    ```
  - Flashcard evaluation listener in `js/flashcards.js:1684-1710`:
    ```javascript
    window.addEventListener('keydown', (e) => {
      ...
      if (Flashcards.virada) {
        if (key === '1') { e.preventDefault(); Flashcards.avaliar(1); return; }
        if (key === '2') { e.preventDefault(); Flashcards.avaliar(2); return; }
        if (key === '3') { e.preventDefault(); Flashcards.avaliar(3); return; }
        if (key === '4') { e.preventDefault(); Flashcards.avaliar(4); return; }
      }
    });
    ```
    `document` event listener receives key events before `window`. When reviewing flashcards, pressing keys `1`, `2`, `3`, `4` triggers global navigation to another section rather than submitting the rating.
  - Quiz screen (`js/quiz.js`) has NO keyboard listeners for choices (`1-4`) or advancement (`Enter`/`Space`). Pressing `1-4` in Quiz navigates to other sections.
  - Global navigation listener executes even while modals are displayed on screen.
- **Flashcard Interactive Semantics (`index.html:290`)**:
  ```html
  <div class="flashcard" id="flashcard" onclick="Flashcards.virar()">
  ```
  Rendered as a plain `<div>`. Lacks `role="button"`, `tabindex="0"`, `aria-label`, and `aria-expanded`. Inaccessible via keyboard Tab navigation and unannounced as interactive to screen readers.
- **Modal Focus Trap & Escape Management**:
  - `js/modal_manager.ts` implements focus trapping and Escape handlers.
  - However, all primary static modals in `index.html` (`#templo-modal`, `#conquista-modal`, `#levelup-modal`, `#onboarding-modal`, `#modal-meta-prazo`, `#ia-import-modal`, and `js/grammar.js:203`) bypass `ModalManager`.
  - When opened, focus leaks outside the modal into background DOM, pressing Escape fails to dismiss the modal, and focus is not restored to the triggering element upon close.
- **Focus Rings & Dark Mode Contrast (WCAG 2.1 SC 1.4.11)**:
  - Only one global focus rule exists (`css/italia.css:1036`):
    `:focus-visible { outline:2px solid var(--cor-veneziano); outline-offset:2px; border-radius:2px; }`
  - In dark mode (`body.dark-mode`), `--cor-veneziano` is `#C4304A` (luminance ~0.114) over `#1A1510` background (luminance ~0.007). The contrast ratio is 2.88:1, failing WCAG 2.1 SC 1.4.11 (minimum 3.0:1 required).

### 1.4 Visual and Cognitive Feedback & Fatigue Prevention
- **Quiz Answer Feedback & ARIA Live Regions**:
  - In `js/quiz.js:273-287`, clicking an option immediately marks all buttons as disabled (`btn.disabled = true`), causing focus drop to `document.body`.
  - `#explicacao-container` (`index.html:416-419`) lacks `role="status"` or `aria-live="polite"`. Screen reader users receive no auditory announcement of whether their choice was correct or what the explanation is.
- **Absence of Fatigue Prevention & Pacing**:
  - 0 mechanisms for micro-breaks, session length boundaries, or cognitive pacing in the application.
  - Flashcards sessions can run indefinitely through all due cards without natural consolidation intervals.
- **Typography & Dyslexia Plan**:
  - `dev/plano-dislexia.md` designed a plan to introduce `Atkinson Hyperlegible` and expanded line-height.
  - `index.html:14` still loads only `Cinzel`, `EB Garamond`, and `UnifrakturMaguntia`. High-contrast serif typefaces remain active across all lessons.

### 1.5 Frontend Architecture & Build System
- **CSS Architecture**:
  - `css/italia.css` is a monolithic file of 338 KB (8,383 lines) created by concatenating multiple design drafts.
  - Redundant resets (`*, *::before, *::after` reset at line 58 and line 4616).
  - Duplicate rules for `.opcao-btn` (`line 819` and `line 5090`) with conflicting styles.
- **Script Loading & Build Pipeline**:
  - `index.html` loads 41 individual scripts via `<script>` and `<script type="module">`.
  - `npm run build` runs `tsc` and `vite build`. Vite issues 31 warnings (`can't be bundled without type="module" attribute`).
  - Production build in `vite.config.ts` relies on custom plugin `copyLegacyAssets()` copying loose raw scripts into `dist/js/`.
  - Zero-external-runtime-deps: strictly followed; runtime dependencies consist solely of `zod`.

### 1.6 Existing UI/UX & A11y Tests
- Vitest unit suite (`npm test`) passes 15/15 test files (104 tests), but tests only algorithmic logic, state management, and mock DOM class toggles.
- Playwright a11y suite (`npm run test:a11y` via `tests/a11y/a11y.spec.ts`):
  - Fails to run in Linux/WSL environment due to missing OS libraries (`libnspr4.so`).
  - Filters exclusively for `critical` and `serious` violations, omitting `moderate`/`minor`.
  - Excluded from standard CI / `npm test` pipeline.

---

## 2. Logic Chain

```
[Observation 1: Viewport user-scalable=no]
  ↳ Low-vision users cannot zoom page text
  ↳ Violates WCAG 1.4.4 (Resize text)
  ↳ Causes severe reading strain on mobile devices

[Observation 2: SW skipWaiting + controllerchange auto-reload]
  ↳ Service worker activates in background during app use
  ↳ Dispatches 'controllerchange'
  ↳ Calls window.location.reload()
  ↳ Unsaved progress in Quiz, Flashcards, or Voice Recording is obliterated

[Observation 3: Missing overscroll-behavior: contain on modals & drawers]
  ↳ User scrolls inside .tm-card, .ia-import-box, or lyrics containers
  ↳ Reach start or end boundary
  ↳ Scroll chains to root window
  ↳ Triggers unwanted browser pull-to-refresh or window rubber-banding on iOS/Android PWA

[Observation 4: Shrunk touch targets on mobile (32px header buttons, 40px bottom-nav tabs)]
  ↳ Mobile viewports contract interactive areas below 44x44px
  ↳ Violates WCAG 2.1 SC 2.5.5 / 2.5.8
  ↳ Users frequently trigger accidental clicks (e.g. tapping Help instead of Sound, or Canzoni instead of Dialoghi)

[Observation 5: Keydown collision in core.js vs flashcards.js]
  ↳ core.js listens on document for '1'-'5' to navigate sections
  ↳ flashcards.js listens on window for '1'-'4' to rate FSRS
  ↳ document captures event before window
  ↳ User reviewing flashcards presses '1' (Again) -> core.js navigates to 'templi'
  ↳ Critical UX breakdown: reviewing cards via keyboard kicks user out of study session

[Observation 6: Disabled option buttons without focus transfer or aria-live in Quiz]
  ↳ User chooses answer -> btn.disabled = true
  ↳ Focused element disappears -> focus reset to document.body
  ↳ Explanation container is revealed without aria-live or role="status"
  ↳ Screen reader users hear silence; keyboard users must tab 20+ times through the header to reach 'Continuar'
```

---

## 3. Caveats

1. **Playwright A11y Runner Execution**: `npm run test:a11y` requires Linux shared libraries (`libnspr4`, `libnss3`) not present in all minimal WSL distributions. In environments lacking these packages, a11y test suites must be executed in CI Docker containers or standard browser contexts.
2. **Offline Font Caching**: Google Fonts (`Cinzel`, `EB Garamond`) use stale-while-revalidate in `sw.js`. If offline on very first launch before visiting online, system serif fallbacks (`Georgia`, `serif`) are used, which may slightly alter layout metrics.
3. **No Visual Regression Suite**: There is currently no automated screenshot diffing mechanism (e.g., Playwright image snapshot). Visual ergonomics must be verified through manual inspection or programmatic bounding box checks.

---

## 4. Conclusion

The application possesses a solid offline-first foundation with zero runtime bloat. However, there are five severe UX and accessibility bottlenecks that directly degrade usability:
1. **Critical Keyboard Collision**: `core.js` intercepts keys `1-5`, breaking FSRS rating in flashcards and causing accidental navigation during study sessions and modals.
2. **PWA Data Disruption**: Aggressive Service Worker activation reloads the page mid-exercise, and mismatched precache query strings endanger offline script loading.
3. **Touch Ergonomics**: Key mobile targets (`.theme-toggle-btn` at 32px, `.btn-modo-toggle` at 32px, `.bottom-nav` tabs at ~36-40px) fall short of the 44x44px WCAG threshold.
4. **Scroll & Rubber-Band Chaining**: Modals and lyrics containers lack `overscroll-behavior: contain`, creating erratic viewport jumps in standalone PWA mode.
5. **A11y Gaps in Quiz & Modals**: Inline modals lack focus traps and Escape listeners; Quiz answer submissions drop focus and lack `aria-live` announcements; and `#flashcard` is a non-semantic, keyboard-unreachable `<div>`.

### Proposed Fix Strategy

1. **Keyboard Scope Management**:
   - In `js/core.js`: Guard global `1-5` navigation with checks:
     - Disallow if any modal is visible (`document.querySelector('.modal.ativo, [role="dialog"]:not([style*="display: none"])')`).
     - Disallow if active section is `flashcard` or `quiz`.
   - In `js/quiz.js`: Add keyboard support for options (`1-4`) and advancement (`Enter`/`Space`).
2. **PWA & SW Resilience**:
   - Update `index.html` viewport meta tag: remove `maximum-scale=1.0, user-scalable=no`.
   - In `sw.js`: Use `{ ignoreSearch: true }` in `caches.match()` for static assets.
   - Decouple `controllerchange`: Prompt user with a toast ("Atualização disponível. Atualizar agora?") instead of calling `window.location.reload()` automatically.
   - Add standard 192x192 and 512x512 PNG icons to `manifest.webmanifest`.
3. **Ergonomic Touch Targets & Containment**:
   - In `css/italia.css`:
     - Set `min-width: 44px; min-height: 44px;` on `.theme-toggle-btn`, `.btn-modo-toggle`, `.fc-tool-btn`, and `.nav-tab`.
     - In `.bottom-nav`: Provide comfortable touch spacing or horizontal scrolling/overflow grouping when viewport < 400px.
     - Add `overscroll-behavior: contain` to `.tm-card`, `.ia-import-box`, `.ach-scroll-container`, `.cloze-lyrics-stage`, and `.can-lyrics-area`.
     - Update dark mode `:focus-visible` outline to high-contrast `#D4A843` or `#FAF7F2` (>= 3:1 contrast ratio).
4. **Modal Manager Unification & ARIA**:
   - Route static modals (`templo-modal`, `conquista-modal`, `levelup-modal`, `ia-import-modal`, `modal-meta-prazo`) through `ModalManager` or equip them with standardized focus trapping, Escape listener, and focus restoration.
   - Make `#flashcard` accessible: `role="button"`, `tabindex="0"`, `aria-label="Flashcard interativo"`, `aria-expanded="false/true"`, and keyboard trigger on Space/Enter.
   - Add `aria-live="polite"` and `role="status"` to `#explicacao-container`, and auto-focus the "Continuar" button when answering a quiz question.
5. **Cognitive Fatigue & Micro-Breaks**:
   - Introduce a study session counter: after 20 flashcards or 3 quizzes, present a subtle 60-second breathing/memory consolidation prompt before proceeding.

---

## 5. Verification Method

1. **Verify Unit & Core Tests**:
   ```bash
   npm test
   ```
2. **Verify Static TypeScript Checking & Production Build**:
   ```bash
   npm run build
   ```
3. **Verify Touch Targets via Programmatic DOM Query**:
   In browser console or node script:
   ```javascript
   document.querySelectorAll('button, [role="button"], a').forEach(el => {
     const rect = el.getBoundingClientRect();
     if (rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44)) {
       console.warn('Touch target < 44px:', el, rect.width, rect.height);
     }
   });
   ```
4. **Verify Keyboard Navigation Conflict**:
   Open `#flashcard` section, flip a card with Space, press `1`. Confirm card is graded "Again" (1) and user remains on `#flashcard` without redirecting to `#templi`.
5. **Verify Modal Accessibility**:
   Open `#templo-modal`, `#levelup-modal`, or `#ia-import-modal`. Press Tab repeatedly; confirm focus stays trapped within modal. Press Escape; confirm modal closes cleanly and focus returns to the opener.
