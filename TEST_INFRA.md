# TEST_INFRA: Opaque-Box E2E Testing Infrastructure & Specification

**Project**: Aprendimento Italiano — Deep Stress, Resilience & UX Optimization  
**Author**: E2E Test Writer  
**Target Runner**: Vitest (Environment: `happy-dom`)  
**Scope**: Requirements R1–R4, Features F1–F26  
**Status**: ACTIVE

---

## 1. Test Philosophy & Principles

The E2E testing framework for *Aprendimento Italiano* is built upon rigorous **opaque-box, requirement-driven verification**. Tests treat the application as a black box with observable interfaces (DOM elements, user keyboard/touch events, Web APIs, LocalStorage/SessionStorage, BroadcastChannel, and network payloads).

### Core Pillars
1. **Zero-Facade Guarantee**: Every test executes genuine application logic, exercises actual DOM nodes or modules, and asserts strict state and side-effect mutations. No dummy assertions (`expect(true).toBe(true)`) or artificial bypasses.
2. **Progressive Testability & Backward Compatibility**: Tests validate existing behaviors and newly specified contracts without modifying application source code directly. Interfaces are probed with graceful detection of contract adherence.
3. **Hermetic Test Isolation**: Every test run resets its DOM, clears `localStorage`/`sessionStorage`, isolates `BroadcastChannel`, and silences or spies upon async audio/speech APIs to guarantee zero inter-test interference.
4. **Adversarial & Stress Verification**:
   - *Encoding & Escaping*: Unsafe HTML entities, cross-site script payloads (`<script>`, `onerror`), Unicode surrogates, RTL markers, and empty string boundaries.
   - *Storage Exhaustion*: Realistic `QuotaExceededError` triggering to verify ephemeral cache eviction ladders and garbage collection persistence.
   - *Mathematical Stability*: Immunity against `NaN`, `Infinity`, negative intervals, degenerate stability, and past timestamp skew in FSRS-4.5 / Ebbinghaus algorithms.
   - *Concurrency & Race Conditions*: Double-click reentrancy, rapid tab navigation while audio is playing, multi-tab broadcast clobbering, and unhandled promise rejection prevention.

---

## 2. 4-Tier Systematic Testing Hierarchy

The E2E test suite is organized into four complementary tiers across dedicated suite files:

| Tier | Suite File | Scope & Focus | Min Target |
|------|------------|---------------|------------|
| **Tier 1** | `tests/e2e/tier1_feature_coverage.test.ts` | **Feature Coverage**: Representative happy-path inputs in isolation across all 4 feature areas. | >= 5 tests per area (>= 20 total) |
| **Tier 2** | `tests/e2e/tier2_boundary_corner.test.ts` | **Boundary & Corner Cases**: Limits, empty inputs, max sizes, negative/zero, NaN/Infinity, clock skew, and rapid input. | >= 5 tests per area (>= 20 total) |
| **Tier 3** | `tests/e2e/tier3_pairwise_combinations.test.ts` | **Cross-Feature Pairwise Interactions**: Multi-feature collisions (e.g. Quota during Quiz, Audio during Tab Navigation, Sync during Backup Import). | >= 10 combination tests |
| **Tier 4** | `tests/e2e/tier4_real_world_workloads.test.ts` | **Real-World Workloads**: Full end-to-end multi-step learning journeys, offline simulation, and PWA resilience. | >= 5 comprehensive scenarios |

---

## 3. Feature Inventory Mapping

Every feature from `PROJECT.md` is mapped to its tier coverage and primary verification points:

| # | Feature / Remediation | Area | Tier 1 (Happy Path) | Tier 2 (Boundary & Corner) | Tier 3 (Cross-Feature) | Tier 4 (Real-World) |
|---|-----------------------|------|---------------------|----------------------------|------------------------|---------------------|
| **F1** | Storage Quota GC Persistence | Storage | Test GC triggers on quota error | Test GC with 0 cards, 10k cards, suspended cards | Storage quota hit during active quiz | Full recovery in offline PWA scenario |
| **F2** | SWR Cache Eviction Ladder | Storage | Test `it_swr_*` evicted before flashcards | Test empty cache, large 5MB SWR payload | SWR eviction during backup export | Multi-megabyte session persistence |
| **F3** | Cross-Tab Synchronization | Storage | Test broadcast sync message handling | Test corrupted channel payload, missing keys | Concurrent multi-tab review & sync | Multi-device sync reconciliation |
| **F4** | Safe Storage Gateway | Storage | Test safe parse with schema defaults | Test null, undefined, primitive, invalid JSON | Storage failure fallback during review | Startup recovery from corrupted storage |
| **F5** | Atomic Backup Import/Export | Storage | Test valid JSON import and state hydration | Test malformed JSON, schema mismatch, rollback | Import during in-progress quiz session | Full backup creation & restore roundtrip |
| **F6** | Stored Content Sanitization | Storage | Test custom story/song import | Test XSS payload `<img onerror>`, `<script>` | Custom content rendering in flashcards | Import user book with special formatting |
| **F7** | FSRS Mathematical Bounds | Algorithm | Test ratings 1–4 produce valid intervals | Test NaN, Infinity, negative stability/difficulty | FSRS review under storage write failure | 50-card spaced review progression |
| **F8** | Clock Skew & Temporal Anomaly | Algorithm | Test future review scheduled monotonically | Test `lastReview > now`, leap year, timezone shifts | Clock skew during multi-tab sync | 7-day study simulation across days |
| **F9** | Ebbinghaus Harmonization | Algorithm | Test `lastReview` camelCase projection | Test missing `lastReview`, null timestamp | Ebbinghaus projection with active cards | Long-term retention curve evaluation |
| **F10** | Reentrancy & Debounce Guards | Algorithm | Test single review/next advances smoothly | Test rapid double-click on `avaliar` / `proxima` | Double-click during network sync latency | High-velocity speed-run study session |
| **F11** | Cross-Section Audio Teardown | Algorithm | Test navigation pauses audio/TTS | Test navigation during TTS load, worker speech | Navigation to flashcards while quiz audio plays | Tab switching during song karaoke |
| **F12** | Audio Promise Rejection Safety | Algorithm | Test play/stop audio cycle | Test rejected audio promise, muted autoplay | Audio rejection during rapid navigation | Interrupted speech synthesis session |
| **F13** | Keyboard Shortcut Scoping | UX / A11y | Test global `1-5` navigates between tabs | Test keys `1-4` in flashcards/quiz do not switch tab | Keyboard answer while modal is open | Full keyboard-only study walkthrough |
| **F14** | Quiz Keyboard Accessibility | UX / A11y | Test keys `1-4` select option, Enter advances | Test keys `0`, `5`, `a`, rapid Enter keypresses | Keyboard quiz answering with sound enabled | Complete 10-question quiz via keyboard |
| **F15** | Viewport & PWA SW Resilience | UX / A11y | Test cache matching with query parameters | Test SW offline fallback for `/data/*.json` | SW update event during active study | PWA offline navigation and reload |
| **F16** | Overscroll Containment | UX / A11y | Test modal and card contain scroll | Test nested container boundaries | Scroll chaining during modal review | Mobile scroll interaction in dialogs |
| **F17** | Touch Target Sizing (>=44px) | UX / A11y | Test navigation tabs & toggles meet 44px | Test small viewport (320px/360px mobile) | Mobile touch interaction on flashcard | Complete study session in mobile viewport |
| **F18** | Modal Focus Trapping | UX / A11y | Test modal opens, focuses, and closes | Test Escape key dismiss, focus return to trigger | Nested modal stacking and escape ladder | Opening help/temple modal and returning |
| **F19** | Quiz ARIA & Flashcard Semantics| UX / A11y | Test `aria-live` polite feedback, `#flashcard` role | Test screen-reader attribute transitions | ARIA live announcements during combo | Accessible study session validation |
| **F20** | Cognitive Pacing & Micro-Breaks | UX / A11y | Test micro-break suggestion after study set | Test dismiss and continue review | Micro-break prompt during quota check | Sustained 25-card review session |
| **F21** | Dark Mode Focus Contrast | UX / A11y | Test dark mode toggle applies class & styles | Test focus ring contrast >= 3:1 in dark mode | Theme toggle during active quiz | Day-to-night theme switch workflow |
| **F22** | Storage Stress Suite | Framework | Test large dataset insertion & retrieval | Test storage fuzzing with malformed data | Storage stress alongside state updates | End-to-end data resilience under load |
| **F23** | Math & Concurrency Stress Suite | Framework | Test 1,000 FSRS iterations without drift | Test extreme difficulty and stability values | Concurrency race condition stress | Algorithmic stability verification |
| **F24** | Cross-Tab & Backup Stress Suite | Framework | Test multi-device sync conflict resolution | Test CRDT union and max resolution | Import corrupt backup over healthy state | Multi-tab parallel progress updates |
| **F25** | Continuous Improvement Roadmap | Framework | Verify roadmap architectural specifications | Verify mitigation documentation alignment | Trace roadmap guidelines against code | Long-term evolution verification |

---

## 4. Test Architecture & Directory Layout

```
tests/e2e/
├── e2e_helpers.ts                     # Shared DOM bootstrap, mock harness, storage & event utilities
├── tier1_feature_coverage.test.ts     # Tier 1: Isolated Happy-Path Feature Coverage (F1–F25)
├── tier2_boundary_corner.test.ts      # Tier 2: Boundary, Limit, Malformed, Overflow & Clock Skew
├── tier3_pairwise_combinations.test.ts# Tier 3: Pairwise Cross-Feature Interactions & Concurrency
└── tier4_real_world_workloads.test.ts # Tier 4: Comprehensive Real-World User Journeys & Scenarios
```

### Shared E2E Test Harness (`tests/e2e/e2e_helpers.ts`)
- **`bootstrapAppDOM()`**: Initializes the exact DOM structure from `index.html` (header, sidebar, nav-tabs, bottom-nav, sections, modals, flashcard containers, and quiz stage).
- **`createIsolatedStorage()`**: Creates an isolated in-memory LocalStorage/SessionStorage proxy that supports quota simulation, error injection, and event dispatch.
- **`mockWebApis()`**: Provides resilient mocks for `BroadcastChannel`, `speechSynthesis`, `AudioContext`, `Notification`, and `ServiceWorker`.
- **`simulateUserClick(el)` / `simulateKey(key, target)`**: Dispatches authentic browser MouseEvent and KeyboardEvent sequences with bubbling and default prevention tracking.
- **`resetAppState()`**: Fully cleans up singletons (`AppState`, `AppXP`, `AppNavigation`, `Flashcards`, `Quiz`, `ModalManager`, `ConflictResolver`).

---

## 5. Real-World Application Scenarios (Tier 4)

1. **Scenario 1: Nuovo Studente (First-Time Onboarding to Mastery)**
   - New user visits the application.
   - Initial state check: Level 1, 0 XP, Temple 1 unlocked, default theme, audio rate 0.85x.
   - Complete onboarding tour dismiss, navigate to Temple 1, study 3 vocabulary words.
   - Earn XP, verify level progression and XP bar update.

2. **Scenario 2: Sessione Spaziata FSRS (Intensive Flashcard Review & Retention)**
   - User loads Temple 1 flashcard deck.
   - Flips card 1, rates "Good" (rating 3) → interval calculated, XP awarded, heatmap entry recorded.
   - Flips card 2, rates "Hard" (rating 2) → interval calculated, error count preserved.
   - Flips card 3, rates "Again" (rating 1) → lapses incremented, scheduled for relearning.
   - Verifies FSRS history record, nextReview timestamp, and Ebbinghaus projection update.

3. **Scenario 3: Il Templo della Conoscenza (Quiz Examination & Combo Pacing)**
   - User launches Temple 1 Quiz session.
   - Question 1 answered correctly via keyboard key `1` → combo increments, sound triggered, ARIA status announced.
   - Advance via keyboard `Enter` → Question 2 answered incorrectly → combo reset, explanation displayed.
   - Advance through final question → result modal displayed, total XP awarded, heatmap updated.

4. **Scenario 4: Sincronizzazione Multi-Dispositivo (Cross-Tab & CRDT Merge)**
   - Tab A has 250 XP and Temples [1, 2] unlocked.
   - Tab B receives remote update with 400 XP and Temples [1, 3] unlocked.
   - BroadcastChannel event fires `SYNC_UPDATE`.
   - `ConflictResolver` performs pure CRDT merge: max XP = 400, union of temples = [1, 2, 3].
   - State and UI in Tab A synchronize without data loss or user disruption.

5. **Scenario 5: Resilienza PWA Offline & Backup di Emergenza (Quota & Rollback)**
   - PWA operates in offline mode (`navigator.onLine = false`).
   - SWR cache and error logs fill storage toward simulated quota limit.
   - Trigger `QuotaExceededError` during flashcard save → eviction ladder clears `it_swr_*` and pruned cards.
   - User creates JSON backup, tests export validity.
   - User attempts importing corrupted backup JSON → schema validator rejects payload, staging namespace rolls back without corrupting local data.

---

## 6. Coverage Thresholds & Quality Gates

- **Total E2E Test Cases**: >= 70 individual test assertions across 4 tiers.
- **Pass Rate**: 100% executable pass in `vitest run tests/e2e`.
- **Console Hygiene**: 0 unhandled promise rejections, 0 uncaught errors during normal operation.
- **Execution Speed**: Full E2E suite completes in under 10 seconds in Vitest.
