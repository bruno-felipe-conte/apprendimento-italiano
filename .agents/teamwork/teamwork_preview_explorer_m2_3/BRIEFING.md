# BRIEFING — 2026-10-31T04:31:00Z

## Mission
Investigate audio/TTS lifecycle bugs, unhandled promise rejections, worker synthesis invalidation, utterance GC issues, and propose exact fix designs for M2.3.

## 🔒 My Identity
- Archetype: teamwork_preview_explorer
- Roles: Explorer, Investigator, Synthesizer
- Working directory: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_3
- Original parent: 0d5d82a5-da3d-44a0-9804-5de6b897019d
- Milestone: M2.3 Audio/TTS & Navigation Robustness

## 🔒 Key Constraints
- Read-only investigation — do NOT implement
- Write only to /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m2_3/
- Follow Handoff Protocol (handoff.md with 5 components)
- Propose exact fix design with before/after snippets and exact line numbers

## Current Parent
- Conversation ID: 0d5d82a5-da3d-44a0-9804-5de6b897019d
- Updated: 2026-10-31T04:24:06Z

## Investigation State
- **Explored paths**:
  - `js/core/navigation.js`: `AppNavigation.navegar()` line 61-64 stops only `Canzoni.tocandoKaraoke`. Missing teardown for `VoiceEngine`, `speechSynthesis`, `Storie`, `Imitazione` (recording/audio player), and `Flashcards` (recognition).
  - `js/imitazione.js`: `tocarMinhaGravacao()` line 274 has unhandled `_userAudioPlayer.play()` lacking `.catch()`, causing `unhandledrejection` on autoplay block or abort.
  - `js/voice_engine.ts`: `VoiceEngine.parar()` lines 424-440 does not invalidate `_pendingSyntheses` worker promises, allowing delayed neural buffers to play or fallback to native speech after stop. Also `u.onerror` lines 586-596 executes `setTimeout(opcoes.onend, 800)` even on `canceled` or `interrupted` errors, restarting chained playback in Storie.
  - `js/vocab.js`: `pronunciarExemplo()` lines 496-498 creates ephemeral `SpeechSynthesisUtterance` without variable anchoring on `Vocab` or `window`, exposing it to Chromium/WebKit premature GC.
- **Key findings**: Complete root cause and fix designs formulated for all 4 issues.
- **Unexplored areas**: None for M2.3 scope; all 4 items fully explored and verified.

## Key Decisions Made
- Centralized `AppNavigation.teardownAudio(novaSecao)` with targeted section exclusion to avoid restarting/stopping valid destination media while killing background audio/recording.
- Generation counter (`_sessionEpoch`) and `_pendingSyntheses.clear()` in `VoiceEngine.parar()` to ensure instant, fail-safe worker synthesis invalidation.
- Error code check (`err.error === 'canceled' || err.error === 'interrupted'`) in `VoiceEngine.falar()` to suppress spurious `onend` callbacks and console warnings.
- Explicit `_activeUtterance` anchoring on both `Vocab` and `window` with `onend`/`onerror` reference cleanup.

## Artifact Index
- DISPATCH.md — Dispatch instructions
- BRIEFING.md — Working memory & state
- progress.md — Heartbeat / progress log
- handoff.md — Final structured report
