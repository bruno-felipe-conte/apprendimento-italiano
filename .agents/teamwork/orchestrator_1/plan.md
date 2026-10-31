# Project Plan: Deep Stress & Resilience Audit and UX Optimization

## Goal
Audit, harden, and optimize the "Aprendimento Italiano" application according to requirements R1, R2, R3, R4, ensuring 0 runtime external dependencies, 100% backward compatibility, 100% passing tests, error-free build, and a robust continuous improvement framework.

## Phases
1. **Phase 0: Survey & Scope Mapping**
   - Explorer 1 (Storage & Persistence): LocalStorage/IndexedDB corruption, quota limits, multi-tab sync, corrupted payload import, schema migration.
   - Explorer 2 (Algorithmic & Concurrency Edge Cases): FSRS & Ebbinghaus math edge cases (past timestamps, timezone skew, multi-year jumps, stability bounds), Audio/TTS playback race conditions, rapid multi-clicks, rapid navigation/tab-switch aborts.
   - Explorer 3 (UX, Ergonomics & PWA/a11y): Mobile/PWA overscroll/bounce, keyboard shortcuts, touch targets (44x44px), visual & cognitive feedback, micro-breaks/mental fatigue.

2. **Phase 1: Synthesis & PROJECT.md Formulation**
   - Synthesize findings into comprehensive Feature Inventory, Architecture, Interface Contracts, and Milestones.
   - Establish strict file ownership and code layout to prevent concurrent worker conflicts.

3. **Phase 2: Dual Track Launch**
   - E2E Testing Track Orchestrator: Requirements-driven opaque-box test suite across Tiers 1-4 (stress tests, fuzzing, temporal boundaries, schema migration). Produces `TEST_READY.md`.
   - Implementation Track Sub-Orchestrators: Modular execution of identified milestones.

4. **Phase 3: Implementation & Validation**
   - Milestone Sub-Orchestrators execute Explorer → Worker → Reviewer → Challenger → Auditor cycle.
   - Strict audit gating (binary veto) and review consensus.

5. **Phase 4: Final Milestone (E2E Test Pass & Coverage Hardening)**
   - Phase 1: 100% passing rate on Tiers 1-4 test suite.
   - Phase 2: Adversarial Coverage Hardening (Tier 5 with Challenger → Worker → Reviewer).

6. **Phase 5: Final Review, Build Verification & Handover**
   - Verification of `npm test` and `npm run build` (exit code 0).
   - Detailed comprehensive audit report covering anomalies, applied fixes, and continuous improvement roadmap.
   - Notification to Sentinel.
