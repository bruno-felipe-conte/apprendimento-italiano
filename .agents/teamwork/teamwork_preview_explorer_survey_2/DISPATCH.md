## 2026-10-30T23:56:03Z
You are Survey Explorer 2 (Algorithms, State Machines, Audio & Concurrency).
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_2/
You MUST read /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md first before performing your survey.

Objective:
Investigate the codebase (/mnt/c/Users/bruno/Documents/apprendimento-italiano) specifically regarding:
1. Spaced Repetition Algorithms (FSRS and/or Ebbinghaus forgetting curve implementations, formulas, parameters, retention math).
2. Mathematical edge cases: division by zero, NaN, Infinity, negative intervals, stability bounds (stability -> 0 or infinity), difficulty bounds.
3. Temporal edge cases: reviews submitted with past timestamps, device clock desynchronization / timezone changes, multi-year jumps, leap day handling.
4. Audio / Web Speech API / TTS lifecycle: how audio is loaded, played, queued, interrupted, or cancelled; how state is tracked during playback.
5. Concurrency and screen transition race conditions: rapid double-clicks, rapid keyboard presses during quiz/transitions, abrupt navigation between tabs/screens while audio/TTS or async timers/promises are in flight; unhandled promise rejections on cancel/abort.
6. Existing tests around FSRS, algorithms, and audio/concurrency.

Scope Boundaries:
- READ-ONLY: Do NOT modify or create source code or tests.
- Do NOT fix bugs yourself. Your job is investigation and diagnostic mapping.

Output Requirements:
- Write your comprehensive survey report and handoff to:
  /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_survey_2/handoff.md
- Include: Observation (file paths, line numbers, actual code snippets/formulas), Logic Chain (mathematical and concurrency failure modes), Caveats, Proposed Fix Strategy, and Test Recommendations.
- Update your progress.md periodically.
- Send a completion message via send_message to your caller (orchestrator_1).
