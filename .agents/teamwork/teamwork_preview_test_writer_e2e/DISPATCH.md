## 2026-10-31T00:40:57Z
Sender: d325678e-ec9a-40b2-9b89-5f56cec87dab (orchestrator_1)
Priority: MESSAGE_PRIORITY_HIGH

You are the E2E Test Writer for the Aprendimento Italiano project.
Your working directory is: /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_test_writer_e2e/
You MUST read:
1. /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/ORIGINAL_REQUEST.md
2. /mnt/c/Users/bruno/Documents/apprendimento-italiano/PROJECT.md

Mandatory Integrity Warning:
DO NOT CHEAT. All test implementations must be genuine and thorough. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A forensic auditor will independently verify your work. Integrity violations WILL be detected and rejected.

Objective:
Design and build a comprehensive, requirement-driven, opaque-box E2E test suite covering user requirements R1, R2, R3, R4 and features F1-F25 listed in PROJECT.md.
Methodology (4-Tier Systematic Testing):
- Tier 1: Feature Coverage (>=5 test cases per feature area) covering representative happy-path inputs in isolation.
- Tier 2: Boundary & Corner Cases (>=5 test cases per feature area) covering limits, empty inputs, max-size inputs, negative/zero values, overflow, NaN/Infinity, clock skew, and rapid inputs.
- Tier 3: Cross-Feature Combinations (pairwise interactions, e.g. storage quota during quiz, audio during multi-tab sync, backup import during active session).
- Tier 4: Real-World Application Scenarios (>=5 realistic learning sessions, end-to-end user workflows, offline PWA simulation).

Write Ownership:
- You exclusively own:
  - tests/e2e/ (all files within)
  - /mnt/c/Users/bruno/Documents/apprendimento-italiano/TEST_INFRA.md
  - /mnt/c/Users/bruno/Documents/apprendimento-italiano/TEST_READY.md
- DO NOT modify application source code in js/, css/, or index.html.

Requirements:
1. Create /mnt/c/Users/bruno/Documents/apprendimento-italiano/TEST_INFRA.md following the template in PROJECT.md and the Project Pattern guidelines (Test Philosophy, Feature Inventory mapping, Test Architecture, Real-World Scenarios, Coverage Thresholds).
2. Implement test suites in tests/e2e/:
   - tests/e2e/tier1_feature_coverage.test.ts
   - tests/e2e/tier2_boundary_corner.test.ts
   - tests/e2e/tier3_pairwise_combinations.test.ts
   - tests/e2e/tier4_real_world_workloads.test.ts
3. Verify test execution using `npx vitest run tests/e2e`.
4. Create /mnt/c/Users/bruno/Documents/apprendimento-italiano/TEST_READY.md with the runner command and coverage summary.
5. Write your handoff report to:
   /mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_test_writer_e2e/handoff.md
6. Send completion message via send_message to orchestrator_1.
