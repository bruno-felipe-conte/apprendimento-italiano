## 2026-10-31T05:09:17Z
You are Worker M3 (type: teamwork_preview_worker).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3/DISPATCH.md
4. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_3/handoff.md

Your exclusive write boundaries:
- js/core.js
- index.html
- sw.js
- css/italia.css
- manifest.webmanifest
- js/modal_manager.ts

Implement all Milestone 3 features (F13 through F21):
- F13: Keyboard Shortcut Conflict Resolution (scope global 1-5 navigation in js/core.js so it does not hijack keys in flashcards/quiz or when modal open).
- F14: Quiz Keyboard Accessibility (number keys 1-4 for options, Enter/Space to advance).
- F15: Viewport & PWA Service Worker (remove maximum-scale=1.0 and user-scalable=no in index.html, add ignoreSearch: true in sw.js caches.match, decouple controllerchange auto-reload).
- F16: Mobile Overscroll Containment (add overscroll-behavior: contain to modal scroll containers .tm-card, .ia-import-box, .ach-scroll-container, lyrics, sidebar).
- F17: Touch Target Sizing >= 44x44px (enlarge header buttons, mode toggles, bottom nav to >=44px per WCAG 2.1).
- F18: Modal Focus Trapping & Accessibility (static modals use focus trap, Escape to dismiss, focus return).
- F19: Quiz ARIA feedback (aria-live="polite", role="status") and flashcard accessibility (role="button", tabindex="0", Enter/Space flip).
- F20: Cognitive pacing & micro-breaks prompt after sustained review sets.
- F21: High-contrast focus ring in dark mode (outline contrast >= 3:1 in body.dark-mode).

Verification:
Run:
- npm run build:ts
- npx vite build
- npx vitest run tests/modal_manager.test.js tests/navigation.test.js tests/e2e/tier1_feature_coverage.test.ts tests/e2e/tier2_boundary_corner.test.ts
- graphify update .

Write handoff report to /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3/handoff.md.
Send completion message to caller when done.

DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
