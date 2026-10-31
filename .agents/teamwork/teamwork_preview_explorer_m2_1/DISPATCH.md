# Dispatch: Explorer M2.1 — FSRS Math Bounds & Clock Skew

## Mission
Investigate FSRS mathematical stability, NaN/Infinity propagation, negative intervals, and clock skew handling for Milestone 2 (Features F7, F8).

## Scope & Target Files
- `js/flashcards.js` (lines 7–130)
- `scripts/validate-fsrs.js`
- `PROJECT.md`
- `ORIGINAL_REQUEST.md`

## Deliverable
Write your findings report in `.agents/teamwork/teamwork_preview_explorer_m2_1/handoff.md`.
Report back via send_message when done.

## 2026-10-31T04:24:06Z
Sender: 0d5d82a5-da3d-44a0-9804-5de6b897019d
Message:
You are Explorer M2.1 (type: teamwork_preview_explorer).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/
You are read-only. DO NOT modify any code.
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md
3. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/DISPATCH.md
4. js/flashcards.js (lines 7–130) and scripts/validate-fsrs.js

Investigate FSRS mathematical bounds, formula robustness against NaN, Infinity, negative values, and clock skew (lastReview in the future or clock rollback). Propose exact fix design for FSRS.sanitizeCard() and review() formulas.
Write your structured findings to /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_1/handoff.md.
Send a completion message to the caller when done.
