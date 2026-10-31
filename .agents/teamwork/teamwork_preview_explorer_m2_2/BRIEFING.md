# BRIEFING — 2026-10-31T04:32:00Z

## Mission
Investigate Ebbinghaus property key discrepancy (lastReview vs last_review) and reentrancy/double-click flaws in Flashcards.avaliar and Quiz.proximaPergunta, proposing exact fix designs.

## 🔒 My Identity
- Archetype: explorer
- Roles: investigator, analyzer, synthesizer
- Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_2
- Original parent: 0d5d82a5-da3d-44a0-9804-5de6b897019d
- Milestone: M2.2

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Write only to .agents/teamwork/teamwork_preview_explorer_m2_2/
- Propose exact fix designs (diff/snippets) in handoff report
- Do not modify source code directly

## Current Parent
- Conversation ID: 0d5d82a5-da3d-44a0-9804-5de6b897019d
- Updated: not yet

## Investigation State
- **Explored paths**:
  - `src/analytics/ebbinghausCurve.ts`
  - `js/ebbinghaus.js`
  - `js/flashcards.js` (lines 60–160, 600–775, 890–1010, 1320–1360, 1670–1735)
  - `js/quiz.js` (lines 1–140, 200–395)
  - `tests/ebbinghausCurve.test.ts`
  - `tests/ebbinghaus.test.ts`
  - `tests/e2e/tier4_real_world_workloads.test.ts`
- **Key findings**:
  - F9: `flashcards.js` stores `lastReview` (camelCase), but `ebbinghausCurve.ts` checks only `last_review` (snake_case). Result: `getElapsedDays` returns `null`, causing `cardR` to statically fall back to 90% (`retentionTarget`) regardless of actual study age. `js/ebbinghaus.js` doesn't pass `cardR` to `predictNextStabilityGood` at all and lacks `getElapsedDays` export.
  - F10 Flashcards: `Flashcards.avaliar` lacks an initial guard `if (this._bloqueioAvaliacao) return;` and assigns `_bloqueioAvaliacao = true` only at line 975. Rapid clicks/touches/keys reenter, award duplicate XP, corrupt error tracking, and double `this.proxima()` skipping the next card. Guard must also preserve synchronous test workflows by keying on `_cardEmAvaliacaoId`.
  - F10 Quiz: `Quiz.proximaPergunta` has no debounce or guard (`_bloqueioAvanco` missing). Rapid double clicks on "Continuar →" skip intermediate questions or call `mostrarResultado()` multiple times, granting duplicate XP and multiple diary completions.
- **Unexplored areas**: None. Both problem boundaries fully investigated.

## Key Decisions Made
- Designed bidirectional property harmonization (`card.lastReview ?? card.last_review`) in both `ebbinghausCurve.ts` and `ebbinghaus.js`.
- Added `getElapsedDays` to `Ebbinghaus` public module export per `PROJECT.md:71`.
- Designed robust reentrancy guard in `Flashcards.avaliar` with immediate button disabling, card ID matching to protect synchronous test loops, and cleanup in timeout `finally`.
- Designed debounce and idempotency lock for `Quiz.proximaPergunta` and `Quiz.mostrarResultado` (`_bloqueioAvanco`, `_resultadoMostrado`, clearing `this.xpTotal`).

## Artifact Index
- DISPATCH.md — Dispatch instructions and tasks
- BRIEFING.md — Persistent working memory
- progress.md — Liveness heartbeat
- handoff.md — 5-component handoff report
