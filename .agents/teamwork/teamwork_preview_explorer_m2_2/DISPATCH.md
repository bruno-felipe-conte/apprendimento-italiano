# Dispatch: Explorer M2.2 — Ebbinghaus Harmonization & Study Flow Reentrancy

## Mission
Investigate Ebbinghaus property key harmonization between `flashcards.js` (`lastReview`) and `ebbinghausCurve.ts`/`ebbinghaus.js` (`last_review`), and reentrancy/double-click guards in `Flashcards.avaliar` and `Quiz.proximaPergunta` (Features F9, F10).

## Scope & Target Files
- `src/analytics/ebbinghausCurve.ts`
- `js/ebbinghaus.js`
- `js/flashcards.js` (lines 900–950, 1330–1340, 1680–1720)
- `js/quiz.js` (lines 300–390)
- `PROJECT.md`
- `ORIGINAL_REQUEST.md`

## Deliverable
Write your findings report in `.agents/teamwork/teamwork_preview_explorer_m2_2/handoff.md`.
Report back via send_message when done.

## 2026-10-31T04:24:06Z
[Message] sender=0d5d82a5-da3d-44a0-9804-5de6b897019d priority=MESSAGE_PRIORITY_HIGH
You are Explorer M2.2 (type: teamwork_preview_explorer).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_2/
You are read-only. DO NOT modify any code.
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_2/DISPATCH.md
4. src/analytics/ebbinghausCurve.ts, js/ebbinghaus.js, js/flashcards.js (lines 900–950, 1330–1340, 1680–1720), and js/quiz.js (lines 300–390)

Investigate:
1. Ebbinghaus property key discrepancy: flashcards.js stores lastReview (camelCase), while ebbinghausCurve.ts looks only for last_review (snake_case), causing retention projections to fall back to static 90%.
2. Reentrancy and double-click flaws: Flashcards.avaliar() lacks entry guard causing double XP and skipping cards; Quiz.proximaPergunta() lacks debounce causing question skipping and duplicate XP at the end.
Propose exact fix design.
Write your structured findings to /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_2/handoff.md.
Send a completion message to the caller when done.
