# BRIEFING — 2026-10-31T04:35:00Z

## Mission
Investigate FSRS mathematical bounds, formula robustness against NaN, Infinity, negative values, and clock skew (lastReview in the future or clock rollback). Propose exact fix design for FSRS.sanitizeCard() and review() formulas.

## 🔒 My Identity
- Archetype: teamwork_preview_explorer
- Roles: explorer, analyst, synthesist
- Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/
- Original parent: 0d5d82a5-da3d-44a0-9804-5de6b897019d
- Milestone: Milestone 2 (F7, F8)

## 🔒 Key Constraints
- Read-only investigation — do NOT implement or modify any project code
- Write only to our own directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/
- Produce structured findings report in handoff.md with 5 sections: Observation, Logic Chain, Caveats, Conclusion, Verification Method
- Send completion message to parent upon finishing

## Current Parent
- Conversation ID: 0d5d82a5-da3d-44a0-9804-5de6b897019d
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `js/flashcards.js` (lines 7–169, 500–520, 880–935, 1720–1751)
  - `scripts/validate-fsrs.js` (lines 1–185)
  - `PROJECT.md` (Features F7, F8, F9, Interface Contracts, write boundaries)
  - `ORIGINAL_REQUEST.md` (R1, R3, R4, Acceptance Criteria)
  - `src/analytics/ebbinghausCurve.ts` (lines 1–70, 195–250)
  - `js/ebbinghaus.js` (lines 1–60, 120–145)
  - `tests/e2e/tier2_boundary_corner.test.ts` (Test B11: clock skew)
  - `tests/e2e/tier1_feature_coverage.test.ts` (Test F7/F8)
- **Key findings**:
  - `Math.max(NaN, 0.1)` and `Math.min(Math.max(NaN, 1), 10)` return `NaN` due to JS IEEE 754 spec.
  - Power singularity at $d=0$: `Math.pow(0, -0.51) === Infinity` in `nextForgetStability`.
  - Negative stability at $d>11$: `11 - d < 0` produces negative increment in `nextRecallStability`.
  - Unbounded exponential stability: after 50 easy reviews, $S = 1.3e19$, exceeding ECMAScript Date limit ($8.64e15$), causing `RangeError: Invalid time value`.
  - In serialization, `Infinity` and `NaN` convert to `null`, causing cards to become perpetually due.
  - Future `lastReview` or clock rollback produces negative or `NaN` $tDays$.
  - Missing centralized `FSRS.sanitizeCard()` in `js/flashcards.js`.
  - Local `FSRS` is not exported to `Flashcards.FSRS` or `window.FSRS`.
- **Unexplored areas**: None within the scope of M2.1.

## Key Decisions Made
- Designed universal `FSRS.sanitizeCard(card)` clamping $D \in [1.0, 10.0]$, $S \in [0.1, 36500.0]$ ($0$ for 'new'), $I \in [1, 36500]$, and integer $reps, lapses \ge 0$.
- Immunized all 7 core mathematical formulas with input sanitization and post-clamping.
- Designed monotonic clock skew handler: $tDays = \max(0, (now - lastReview) / 86400000)$ and $R = 1.0$ when $lastReview \ge now$.
- Exposed `Flashcards.FSRS = FSRS` and `window.FSRS = FSRS` for testability and cross-module resilience.
- Authored 5-component handoff report in `handoff.md`.

## Artifact Index
- /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/DISPATCH.md — Dispatch log
- /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/BRIEFING.md — Situational awareness and state
- /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/progress.md — Liveness heartbeat
- /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/handoff.md — Final handoff report
