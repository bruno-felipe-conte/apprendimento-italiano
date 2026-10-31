# BRIEFING — 2026-10-31T09:22:00Z

## Mission
Implement Milestone 3: UX, Ergonomics, PWA Resilience & A11y Standards (Features F13–F21).

## 🔒 My Identity
- Archetype: worker
- Roles: implementer, qa, specialist
- Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_worker_m3_replacement/
- Original parent: 0da54649-4aba-4a6a-a092-7fd167240d19
- Milestone: Milestone 3 (F13–F21)

## 🔒 Key Constraints
- Strict write boundaries: js/core.js, index.html, sw.js, css/italia.css, manifest.webmanifest, js/modal_manager.ts, js/quiz.js, js/flashcards.js, plus relevant tests.
- DO NOT CHEAT. All implementations must be genuine.
- Zero external runtime deps.
- Must verify with npm run build:ts, npx vite build, npm test, graphify update .

## Current Parent
- Conversation ID: 0da54649-4aba-4a6a-a092-7fd167240d19
- Updated: not yet

## Task Summary
- **What to build**: Features F13–F21:
  - F13: Keyboard shortcut conflict resolution in js/core.js & js/flashcards.js
  - F14: Quiz keyboard accessibility (keys 1-4 for choices, Enter/Space for advance) in js/quiz.js
  - F15: Viewport meta tag update, SW cache ignoreSearch: true, decouple controllerchange auto-reload, manifest orientation: any
  - F16: Mobile overscroll & bounce containment in css/italia.css
  - F17: Touch target sizing (>= 44x44px) for header utility buttons, mode toggles, flashcard toolbelt, sidebar/bottom nav
  - F18: Modal focus trapping, Escape key handling, and focus return in js/modal_manager.ts and index.html
  - F19: Quiz ARIA feedback (role=status, aria-live=polite) & #flashcard button semantics (role=button, tabindex=0, aria-label, Enter/Space flip)
  - F20: Cognitive pacing & micro-break reminder after 20 continuous flashcard reviews
  - F21: High-contrast focus-visible ring in dark mode (>= 3:1 contrast ratio)
- **Success criteria**: All 9 features implemented cleanly, tests passing, builds passing, graph updated, no regressions.
- **Interface contracts**: PROJECT.md § Interface Contracts
- **Code layout**: PROJECT.md § Code Layout & Write Boundaries

## Key Decisions Made
- [TBD]

## Artifact Index
- DISPATCH.md — Assignment instructions
- progress.md — Liveness & status heartbeat
- handoff.md — Final deliverable report

## Change Tracker
- **Files modified**: None yet
- **Build status**: Pending
- **Pending issues**: None

## Quality Status
- **Build/test result**: Pending
- **Lint status**: Pending
- **Tests added/modified**: Pending

## Loaded Skills
- None required directly (no external skill paths in dispatch prompt)
