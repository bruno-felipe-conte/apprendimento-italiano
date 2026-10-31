# Handoff Report: FSRS Mathematical Bounds, Formula Robustness & Clock Skew (M2.1)

**Agent**: `teamwork_preview_explorer_m2_1`  
**Milestone**: Milestone 2 (Features F7, F8)  
**Date**: 2026-10-31  
**Target Files**: `js/flashcards.js` (lines 7–169), `scripts/validate-fsrs.js`, `PROJECT.md`

---

## 1. Observation

Direct code observations from inspecting `/mnt/c/Users/bruno/Documents/apprendimento-italiano/js/flashcards.js`, `/mnt/c/Users/bruno/Documents/apprendimento-italiano/scripts/validate-fsrs.js`, and Node REPL empirical evaluations:

### 1.1 IEEE 754 Arithmetic Vulnerabilities in Current Code (`js/flashcards.js:7–122`)
1. **`Math.max` and `Math.min` behavior on `NaN`**:
   - In JavaScript (ECMA-262 §21.2.2.24/25), if any argument is `NaN`, `Math.max(x, y)` and `Math.min(x, y)` unconditionally return `NaN`.
   - Verified via Node:
     ```javascript
     Math.max(NaN, 0.1) // -> NaN
     Math.min(Math.max(NaN, 1), 10) // -> NaN
     ```
   - In `flashcards.js`:
     - Line 32: `initStability(rating) { return Math.max(this.w[rating - 1], 0.1); }`  
       If `rating <= 0` or `rating = NaN`, `this.w[rating - 1]` evaluates to `undefined`, and `Math.max(undefined, 0.1)` produces `NaN`.
     - Line 38: `initDifficulty(rating) { const d = ...; return Math.min(Math.max(d, 1), 10); }`  
       If `rating` is `NaN`, `d = NaN` and the function returns `NaN`.
     - Line 48: `nextDifficulty(d, rating)`  
       If input `d` is `NaN`, `raw = NaN + delta = NaN`, and the return is `NaN`.
     - Line 88: `newS = Math.max(this.nextForgetStability(d, s, r), 0.1);`  
       If `nextForgetStability` returns `NaN`, `newS` becomes `NaN`.
     - Line 92: `newS = Math.max(this.nextRecallStability(d, s, r, rating), 0.1);`  
       If `nextRecallStability` returns `NaN`, `newS` becomes `NaN`.

2. **Negative and Zero Singularity in Power Formulas**:
   - In `nextForgetStability(d, s, r)` (lines 65–70):
     ```javascript
     nextForgetStability(d, s, r) {
       return this.w[11] *
              Math.pow(d, -this.w[12]) *
              (Math.pow(s + 1, this.w[13]) - 1) *
              Math.exp(this.w[14] * (1 - r));
     }
     ```
     - With `w[12] = 0.51`: if `d = 0` (or `null` coerced to 0 in arithmetic), `Math.pow(0, -0.51) === Infinity`. Verified via Node: `Math.pow(0, -0.51) === Infinity`.
     - If `d < 0`: `Math.pow(negative, -0.51) === NaN`.
     - If `s < -1`: `(s + 1) < 0`, so `Math.pow(s + 1, 0.34) === NaN`.
   - In `nextRecallStability(d, s, r, rating)` (lines 52–62):
     ```javascript
     const increment = Math.exp(this.w[8]) *
                       (11 - d) *
                       Math.pow(s, -this.w[9]) *
                       (Math.exp(this.w[10] * (1 - r)) - 1) *
                       hardPenalty * easyBonus;
     return s * (increment + 1);
     ```
     - If `d > 11` (e.g. `d = 15` or `d = 99.9` as in corrupt test fixtures): `(11 - d) < 0`. This produces a negative increment (`increment < -1`), resulting in negative stability `newS < 0`. Verified in Node: `d=15, s=2, r=0.5, rating=3` results in `s * (increment + 1) = -6.04499`.
     - If `s = NaN`: line 53 `if (s <= 0)` evaluates to `false` because `NaN <= 0` is false in JS. The calculation proceeds with `Math.pow(NaN, -w[9])`, returning `NaN`.

3. **Unbounded Exponential Stability Growth & JS Date Overflow**:
   - Neither `nextRecallStability` nor `nextInterval` imposes an upper bound on $S$ or $I$.
   - Repeated "Easy" evaluations under overdue conditions ($r \le 0.5$) cause stability to scale exponentially:
     - 50 consecutive reviews produced $S = 1.305 \times 10^{19}$.
     - `nextInterval(1.3e19)` yields $1.305 \times 10^{19}$ days.
     - `nextReview = now + 1.3e19 * 86400000` evaluates to $\approx 1.12 \times 10^{27}$ ms.
     - The maximum valid timestamp supported by ECMAScript `Date` is $\pm 8.64 \times 10^{15}$ ms ($\pm 100,000,000$ days from 1970). Any timestamp $> 8.64 \times 10^{15}$ causes `new Date(ts).toISOString()` to throw `RangeError: Invalid time value`.
     - In JSON serialization, both `Infinity` and `NaN` are serialized to `null` (`JSON.stringify({ s: Infinity, n: NaN }) === '{"s":null,"n":null}'`). When loaded back into memory, `stability: null` causes `nextForgetStability` to yield `Infinity`, permanently bricking the card.

4. **Missing Centralized Sanitizer `FSRS.sanitizeCard()`**:
   - `PROJECT.md` line 25 (Feature F7) and line 70 (Interface Contracts) explicitly require:
     `- FSRS.sanitizeCard(card: FSRSCardInput): FSRSCard (guarantees finite numbers, clamped difficulty in [1, 10], stability in [0.1, 36500], non-negative reps/lapses)`
   - Currently, `js/flashcards.js` contains **zero** implementation of `FSRS.sanitizeCard()`.
   - `scripts/validate-fsrs.js` defines an external standalone function `validarCardFSRS(id, card)` (lines 18–81), but this is not accessible from the core runtime engine `FSRS` in `flashcards.js`.

5. **Clock Skew and Future `lastReview` (Feature F8)**:
   - In `flashcards.js` line 75:
     ```javascript
     const tDays = card.lastReview ? (now - card.lastReview) / 86400000 : 0;
     ```
   - If `card.lastReview > now` (e.g. system clock set back, timezone changed from UTC+2 to UTC, or corrupted future timestamp), `now - card.lastReview < 0`, yielding negative `tDays`.
   - In line 20: `retrievability(t, s)` checks `if (s <= 0 || t < 0) return 1;`. While `retrievability` handles $t < 0$ by returning 1, `tDays` remains negative. If `card.lastReview` is a corrupt non-numeric string or `NaN`, `tDays` evaluates to `NaN`, poisoning `retrievability` and causing `r = NaN`.
   - In `tests/e2e/tier2_boundary_corner.test.ts` lines 215–226:
     ```javascript
     it('B11: descompasso temporal (lastReview > now) deve ser contido monotonicamente em zero dias decorridos', () => {
       const agora = Date.now();
       const revisaoFutura = agora + 86400000 * 5;
       const diffDias = Math.max(0, (agora - revisaoFutura) / 86400000);
       expect(diffDias).toBe(0);
       const r = calculateRetention(diffDias, 10, 19 / 81, -0.5);
       expect(r).toBe(1.0);
     });
     ```
     The contract requires elapsed time to be clamped to 0 monotonically whenever `lastReview > now`.

6. **Global Exposure and Namespace Boundary**:
   - In `flashcards.js` lines 1731–1735:
     ```javascript
     if (typeof window !== 'undefined') window.Flashcards = Flashcards;
     if (typeof globalThis !== 'undefined') globalThis.Flashcards = Flashcards;
     if (typeof module !== 'undefined' && module.exports) module.exports = Flashcards;
     ```
     `FSRS` is declared as a local `const FSRS` at line 7 and is NOT exposed on `Flashcards`, `window`, or `globalThis`. External consumers (like `SafeStorage`, state sanitizers, and Vitest test suites) cannot access `FSRS.sanitizeCard()` or `FSRS.review()` directly without exposing `Flashcards.FSRS = FSRS` and `window.FSRS = FSRS`.

---

## 2. Logic Chain

1. **Causality of Math Breakdown**:
   - Input containing `difficulty: null`, `NaN`, or an out-of-bounds number enters `FSRS.review()` (either from localStorage or test payloads).
   - Because `FSRS.review()` does not sanitize inputs at entry, `d` and `s` are passed directly into `nextDifficulty` and `nextRecallStability`/`nextForgetStability`.
   - Floating-point calculations involving `NaN` propagate `NaN` through addition, subtraction, exponential, and power functions.
   - `Math.max(NaN, 0.1)` fails to clamp, returning `NaN`.
   - `interval` and `nextReview` become `NaN`.
   - Upon JSON serialization (`JSON.stringify`), `NaN` becomes `null`.
   - On subsequent sessions, `App.carregarFlashcards()` loads `null`, which evaluates to `(null || 0) <= Date.now()`, marking the card as due immediately and permanently corrupting the deck queue.

2. **Causality of Date Overflow**:
   - A student reviewing mature cards with rating 4 ("Easy") triggers `increment = Math.exp(1.9395) * ... * 2.9898`.
   - Without an upper clamp, $S$ doubles or triples on every repetition, surpassing $10^{15}$ within dozens of cycles.
   - `nextReview = now + S * 86400000` exceeds `8.64e15`.
   - Standard Date APIs (`new Date().toISOString()`) throw uncaught `RangeError`, breaking UI analytics and backup exporters.

3. **Causality of Clock Skew Distortions**:
   - Device clock desync (moving between timezones or clock correction) causes `lastReview > now`.
   - Without strict non-negative clamping `Math.max(0, ...)`, $tDays$ evaluates to a negative number.
   - When parsed from diverse formats (ISO strings vs millisecond numbers), non-standard values yield `NaN`.

4. **Necessary Architectural Fix**:
   - Immunization requires a two-layer defense:
     1. **Entry sanitization**: `FSRS.sanitizeCard(card)` enforces valid card shape, finite numbers, clamped bounds, and valid integer states before any math is executed.
     2. **Formula defense & post-clamping**: Every formula method (`retrievability`, `nextInterval`, `initStability`, `initDifficulty`, `nextDifficulty`, `nextRecallStability`, `nextForgetStability`) must sanitize its parameters, clamp results within domain bounds, and prevent `NaN`/`Infinity` from escaping.

---

## 3. Caveats

1. **Read-Only Scope**:
   - As `teamwork_preview_explorer_m2_1`, we do NOT edit `js/flashcards.js` directly. The exact proposed code design provided below is for the Milestone 2 implementation worker (`teamwork_preview_worker_m2_1`).
2. **Backward Compatibility**:
   - Production cards in `localStorage` may contain legacy SM-2 properties (`intervalo`, `repeticoes`, `facilidade`), partial FSRS properties, or missing properties.
   - `sanitizeCard` must preserve all legitimate extra properties (`...card`, such as `id`, `frente`, `verso`, `erros`) while strictly normalizing algorithm state variables.
3. **Card State Semantics**:
   - For `state === 'new'`, stability is conventionally `0` (indicating unreviewed). When reviewed for the first time, `initStability(rating)` assigns the initial stability ($w_{0..3} \ge 0.4072$).
   - For `state !== 'new'` ('learning', 'review', 'suspended'), stability must strictly satisfy $S \in [0.1, 36500.0]$.

---

## 4. Conclusion & Exact Proposed Fix Design

### 4.1 Architectural Design of `FSRS` Engine

The following complete, drop-in replacement design for `FSRS` in `js/flashcards.js` guarantees mathematical immunity against `NaN`, `Infinity`, negative numbers, date overflows, and clock skew:

```javascript
// ============================================================
// js/flashcards.js (lines 7–170) — Hardened FSRS-4.5 Core Engine
// ============================================================

const FSRS = {
  // Default weights from FSRS-4.5 paper (trained on 20M reviews)
  w: [0.4072, 1.1829, 3.1262, 15.4722, 7.2102, 0.5316, 1.0651, 0.0589,
      1.9395, 0.11,   0.29,   2.9898,  0.51,   0.34,   1.3436, 0.0762, 2.9898],

  // Power forgetting curve constants
  DECAY: -0.5,
  FACTOR: 19 / 81,
  TARGET_R: 0.9,

  // Mathematical Clamping Bounds per FSRS-4.5 Specification & Feature F7
  MIN_DIFFICULTY: 1.0,
  MAX_DIFFICULTY: 10.0,
  DEFAULT_DIFFICULTY: 5.0,
  MIN_STABILITY: 0.1,
  MAX_STABILITY: 36500.0, // 100 years
  DEFAULT_STABILITY: 2.0,
  MIN_INTERVAL: 1,
  MAX_INTERVAL: 36500,    // 100 years

  /**
   * Sanitiza e blinda um card FSRS contra valores nulos, NaN, Infinito e tipos inválidos.
   * Contrato M2 (PROJECT.md line 70):
   * FSRS.sanitizeCard(card: FSRSCardInput): FSRSCard
   * - Garante números finitos
   * - Dificuldade clampada em [1.0, 10.0]
   * - Estabilidade clampada em [0.1, 36500.0] (ou 0 para estado 'new')
   * - Reps e lapses inteiros >= 0
   * - Preserva histórico e metadados customizados
   */
  sanitizeCard(card) {
    if (!card || typeof card !== 'object') {
      return {
        state: 'new',
        difficulty: this.DEFAULT_DIFFICULTY,
        stability: 0,
        retrievability: 1.0,
        lapses: 0,
        reps: 0,
        lastReview: null,
        interval: 0,
        nextReview: null,
        history: []
      };
    }

    const validStates = ['new', 'learning', 'review', 'suspended'];
    const reps = (typeof card.reps === 'number' && Number.isInteger(card.reps) && card.reps >= 0)
      ? card.reps
      : 0;
    const lapses = (typeof card.lapses === 'number' && Number.isInteger(card.lapses) && card.lapses >= 0)
      ? card.lapses
      : 0;

    const state = validStates.includes(card.state)
      ? card.state
      : (reps > 0 ? 'review' : 'new');

    const difficulty = (typeof card.difficulty === 'number' && Number.isFinite(card.difficulty))
      ? Math.min(Math.max(card.difficulty, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;

    let stability;
    if (typeof card.stability === 'number' && Number.isFinite(card.stability)) {
      if (card.stability <= 0) {
        stability = (state === 'new') ? 0 : this.MIN_STABILITY;
      } else {
        stability = Math.min(Math.max(card.stability, this.MIN_STABILITY), this.MAX_STABILITY);
      }
    } else {
      stability = (state === 'new') ? 0 : this.DEFAULT_STABILITY;
    }

    const retrievability = (typeof card.retrievability === 'number' && Number.isFinite(card.retrievability))
      ? Math.min(Math.max(card.retrievability, 0.0), 1.0)
      : 1.0;

    let interval = 0;
    if (typeof card.interval === 'number' && Number.isFinite(card.interval) && card.interval >= 0) {
      interval = Math.min(Math.floor(card.interval), this.MAX_INTERVAL);
    } else if (state !== 'new') {
      interval = 1;
    }

    let lastReview = null;
    if (typeof card.lastReview === 'number' && Number.isFinite(card.lastReview) && card.lastReview > 0) {
      lastReview = card.lastReview;
    } else if (typeof card.lastReview === 'string' && !isNaN(Date.parse(card.lastReview))) {
      lastReview = new Date(card.lastReview).getTime();
    }

    let nextReview = null;
    if (typeof card.nextReview === 'number' && Number.isFinite(card.nextReview) && card.nextReview > 0) {
      nextReview = card.nextReview;
    } else if (typeof card.nextReview === 'string' && !isNaN(Date.parse(card.nextReview))) {
      nextReview = new Date(card.nextReview).getTime();
    }

    const history = Array.isArray(card.history) ? card.history : [];

    return {
      ...card,
      state,
      difficulty,
      stability,
      retrievability,
      lapses,
      reps,
      interval,
      lastReview,
      nextReview,
      history
    };
  },

  // Retrievability given elapsed time t (days) and stability S
  // Resiliente a clock skew (t <= 0) e valores não finitos
  retrievability(t, s) {
    if (!Number.isFinite(s) || s <= 0 || !Number.isFinite(t) || t <= 0) return 1.0;
    const r = Math.pow(1 + this.FACTOR * t / s, this.DECAY);
    if (!Number.isFinite(r)) return 1.0;
    return Math.min(Math.max(r, 0.0), 1.0);
  },

  // Days until retrievability drops to TARGET_R (clamped [1, 36500])
  nextInterval(s) {
    if (!Number.isFinite(s) || s <= 0) return this.MIN_INTERVAL;
    const safeS = Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY);
    const t = safeS * (Math.pow(this.TARGET_R, 1 / this.DECAY) - 1) / this.FACTOR;
    if (!Number.isFinite(t)) return this.MIN_INTERVAL;
    return Math.min(Math.max(Math.round(t), this.MIN_INTERVAL), this.MAX_INTERVAL);
  },

  // Initial stability after first review (rating 1-4)
  initStability(rating) {
    const r = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    const s = this.w[r - 1];
    if (!Number.isFinite(s) || s <= 0) return this.MIN_STABILITY;
    return Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY);
  },

  // Initial difficulty after first review (rating 1-4)
  initDifficulty(rating) {
    const r = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    const d = this.w[4] - Math.exp(this.w[5] * (r - 1)) + 1;
    if (!Number.isFinite(d)) return this.DEFAULT_DIFFICULTY;
    return Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY);
  },

  // Difficulty after subsequent reviews (with mean reversion toward Easy baseline)
  nextDifficulty(d, rating) {
    const safeD = (typeof d === 'number' && Number.isFinite(d))
      ? Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;
    const r = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    const d0easy = this.initDifficulty(4); // ~3.28 — Easy baseline
    const delta  = -this.w[6] * (r - 3);
    const raw    = safeD + delta;
    // w[7]=0.0589 pulls ~6% toward the easy baseline each review
    const next   = this.w[7] * d0easy + (1 - this.w[7]) * raw;
    if (!Number.isFinite(next)) return this.DEFAULT_DIFFICULTY;
    return Math.min(Math.max(next, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY);
  },

  // Stability after a successful recall (rating 2/3/4)
  nextRecallStability(d, s, r, rating) {
    const rVal = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;
    if (!Number.isFinite(s) || s <= 0) return this.initStability(rVal);

    const safeD = (typeof d === 'number' && Number.isFinite(d))
      ? Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;
    const safeS = Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY);
    const safeR = (typeof r === 'number' && Number.isFinite(r))
      ? Math.min(Math.max(r, 0.0), 1.0)
      : 1.0;

    const hardPenalty = rVal === 2 ? this.w[15] : 1;
    const easyBonus   = rVal === 4 ? this.w[16] : 1;
    const increment   = Math.exp(this.w[8]) *
                        (11 - safeD) *
                        Math.pow(safeS, -this.w[9]) *
                        (Math.exp(this.w[10] * (1 - safeR)) - 1) *
                        hardPenalty * easyBonus;

    if (!Number.isFinite(increment) || increment < 0) {
      return safeS;
    }
    const newS = safeS * (increment + 1);
    if (!Number.isFinite(newS)) return this.MAX_STABILITY;
    return Math.min(Math.max(newS, this.MIN_STABILITY), this.MAX_STABILITY);
  },

  // Stability after forgetting (rating 1 — Again)
  nextForgetStability(d, s, r) {
    const safeD = (typeof d === 'number' && Number.isFinite(d))
      ? Math.min(Math.max(d, this.MIN_DIFFICULTY), this.MAX_DIFFICULTY)
      : this.DEFAULT_DIFFICULTY;
    const safeS = (typeof s === 'number' && Number.isFinite(s) && s > 0)
      ? Math.min(Math.max(s, this.MIN_STABILITY), this.MAX_STABILITY)
      : this.DEFAULT_STABILITY;
    const safeR = (typeof r === 'number' && Number.isFinite(r))
      ? Math.min(Math.max(r, 0.0), 1.0)
      : 1.0;

    const res = this.w[11] *
                Math.pow(safeD, -this.w[12]) *
                (Math.pow(safeS + 1, this.w[13]) - 1) *
                Math.exp(this.w[14] * (1 - safeR));

    if (!Number.isFinite(res)) return this.MIN_STABILITY;
    return Math.min(Math.max(res, this.MIN_STABILITY), this.MAX_STABILITY);
  },

  // ── Review a card, return updated card state ───────────────
  // Feature F7 & F8: Sanitização prévia + monotonicidade temporal contra clock skew
  review(card, rating) {
    const safeCard = this.sanitizeCard(card);
    const rVal = (Number.isInteger(rating) && rating >= 1 && rating <= 4) ? rating : 3;

    const now = Date.now();
    // Clock skew handling (F8): se lastReview estiver no futuro ou nulo, tDays é estritamente 0
    const tDays = (safeCard.lastReview && safeCard.lastReview < now)
      ? (now - safeCard.lastReview) / 86400000
      : 0;

    const d = safeCard.difficulty;
    const s = safeCard.stability;
    const r = (s > 0) ? this.retrievability(tDays, s) : 1.0;

    let newD, newS;

    if (safeCard.state === 'new') {
      newD = this.initDifficulty(rVal);
      newS = this.initStability(rVal);
    } else if (rVal === 1) {
      // Again — forgot
      safeCard.lapses++;
      newD = this.nextDifficulty(d, rVal);
      newS = this.nextForgetStability(d, s, r);
    } else {
      // Hard / Good / Easy — remembered
      newD = this.nextDifficulty(d, rVal);
      newS = this.nextRecallStability(d, s, r, rVal);
    }

    safeCard.reps++;
    const newState    = rVal === 1 ? 'learning' : 'review';
    const intervalDay = rVal === 1 ? 1 : this.nextInterval(newS);
    const previousHistory = Array.isArray(safeCard.history) ? safeCard.history : [];
    const reviewRecord = {
      timestamp: now,
      rating: rVal,
      stabilityBefore: Number((Number.isFinite(s) ? s : 1.0).toFixed(2)),
      stabilityAfter: Number((Number.isFinite(newS) ? newS : 1.0).toFixed(2)),
      retrievabilityBefore: Number((Number.isFinite(r) ? r : 1.0).toFixed(3)),
      targetPeak: rVal === 1 ? 0.85 : 1.0,
      intervalDays: intervalDay
    };

    return {
      ...safeCard,
      state:          newState,
      difficulty:     newD,
      stability:      newS,
      retrievability: r,
      lapses:         safeCard.lapses,
      reps:           safeCard.reps,
      lastReview:     now,
      interval:       intervalDay,
      nextReview:     now + intervalDay * 86400000,
      history:        [...previousHistory, reviewRecord]
    };
  },

  // ── Preview intervals for each rating without committing ───
  previewIntervals(card) {
    const safeCard = this.sanitizeCard(card);
    const now   = Date.now();
    const tDays = (safeCard.lastReview && safeCard.lastReview < now)
      ? (now - safeCard.lastReview) / 86400000
      : 0;
    const { difficulty: d, stability: s, state } = safeCard;
    const r = (s > 0) ? this.retrievability(tDays, s) : 1.0;

    return [1, 2, 3, 4].map(rating => {
      if (state === 'new') {
        return rating === 1 ? 1 : this.nextInterval(this.initStability(rating));
      }
      if (rating === 1) return 1;
      const newS = this.nextRecallStability(d, s, r, rating);
      return this.nextInterval(newS);
    });
  },

  // ── Migrate a legacy SM-2 record to FSRS schema ───────────
  migrateSM2(sm2) {
    if (!sm2 || typeof sm2 !== 'object') {
      return this.sanitizeCard(null);
    }
    const rawInterval = typeof sm2.intervalo === 'number' && Number.isFinite(sm2.intervalo)
      ? sm2.intervalo
      : (typeof sm2.interval === 'number' && Number.isFinite(sm2.interval) ? sm2.interval : 1);
    const s = Math.min(Math.max(rawInterval, this.MIN_STABILITY), this.MAX_STABILITY);

    const rawEase = typeof sm2.facilidade === 'number' && Number.isFinite(sm2.facilidade)
      ? sm2.facilidade
      : (typeof sm2.ease_factor === 'number' && Number.isFinite(sm2.ease_factor)
        ? sm2.ease_factor
        : (typeof sm2.factor === 'number' && Number.isFinite(sm2.factor) ? sm2.factor : 2.5));
    const d = Math.min(Math.max(10 - (rawEase - 1.3) * (9 / 1.7), this.MIN_DIFFICULTY), this.MAX_DIFFICULTY);

    const reps = (Number.isInteger(sm2.repeticoes) && sm2.repeticoes >= 0)
      ? sm2.repeticoes
      : (Number.isInteger(sm2.repetitions) && sm2.repetitions >= 0
        ? sm2.repetitions
        : (Number.isInteger(sm2.reps) && sm2.reps >= 0 ? sm2.reps : 0));

    const lapses = (Number.isInteger(sm2.lapses) && sm2.lapses >= 0) ? sm2.lapses : 0;
    const lastReview = sm2.ultima_revisao || sm2.lastReview || sm2.last_review || null;
    const nextReview = sm2.proxima_revisao || sm2.nextReview || sm2.next_review || null;

    return this.sanitizeCard({
      ...sm2,
      state:          reps > 0 ? 'review' : 'new',
      difficulty:     Number(d.toFixed(2)),
      stability:      Number(s.toFixed(2)),
      retrievability: 1.0,
      lapses,
      reps,
      lastReview,
      interval:       s >= 1 ? Math.round(s) : 1,
      nextReview
    });
  },

  // Format interval as human-readable string
  formatInterval(days) {
    if (!Number.isFinite(days) || days <= 0) return 'hoje';
    const d = Math.round(days);
    if (d === 1) return '1 dia';
    if (d < 31) return `${d} dias`;
    const months = Math.round(d / 30);
    return months === 1 ? '1 mês' : `${months} meses`;
  },
};
```

### 4.2 Global Export Harmonization (`js/flashcards.js:1731–1735`)

In `js/flashcards.js`, lines 1731–1735 should be updated to expose `FSRS`:

```javascript
Flashcards.FSRS = FSRS;

if (typeof window !== 'undefined') {
  window.Flashcards = Flashcards;
  window.FSRS = FSRS;
}
if (typeof globalThis !== 'undefined') {
  globalThis.Flashcards = Flashcards;
  globalThis.FSRS = FSRS;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Flashcards;
}
```

---

## 5. Verification Method

To independently verify this design and confirm immunity against edge cases:

1. **Standalone Node Test**:
   Execute the stress test matrix:
   ```bash
   node -e '
   // Paste proposed FSRS object
   const tests = [
     { desc: "NaN difficulty", card: { difficulty: NaN, stability: 10, reps: 5, state: "review" }, rating: 3 },
     { desc: "Infinity stability", card: { difficulty: 5, stability: Infinity, reps: 5, state: "review" }, rating: 4 },
     { desc: "Negative stability", card: { difficulty: 5, stability: -10, reps: 5, state: "review" }, rating: 2 },
     { desc: "Difficulty out of bounds (99.9)", card: { difficulty: 99.9, stability: 2, reps: 1, state: "review" }, rating: 3 },
     { desc: "Difficulty negative (-5)", card: { difficulty: -5, stability: 2, reps: 1, state: "review" }, rating: 1 },
     { desc: "Future lastReview (+10 days)", card: { difficulty: 5, stability: 10, lastReview: Date.now() + 10 * 86400000, reps: 5, state: "review" }, rating: 3 },
     { desc: "50 consecutive Easy reviews", card: { difficulty: 5, stability: 10, reps: 1, state: "review" }, rating: 4, loop: 50 },
     { desc: "Null input card", card: null, rating: 3 },
     { desc: "Bogus rating (NaN)", card: { state: "new" }, rating: NaN }
   ];
   for (const t of tests) {
     let c = t.card;
     for (let i = 0; i < (t.loop || 1); i++) c = FSRS.review(c, t.rating);
     const ok = Number.isFinite(c.difficulty) && Number.isFinite(c.stability) &&
                Number.isFinite(c.interval) && Number.isFinite(c.nextReview) &&
                c.difficulty >= 1.0 && c.difficulty <= 10.0 &&
                c.stability >= 0.1 && c.stability <= 36500.0 &&
                c.interval >= 1 && c.interval <= 36500;
     console.log((ok ? "PASS" : "FAIL") + ": " + t.desc);
   }
   '
   ```
   **Pass Condition**: All 9 cases print `PASS`.

2. **Run Existing FSRS Validation Suite**:
   ```bash
   npm run fsrs:validate
   ```
   **Pass Condition**: Output ends with `STATUS DA SUÍTE FSRS: ✅ APROVADA (3 aprovados, 0 falhas)`.

3. **Run Vitest Core Suite**:
   ```bash
   npx vitest run tests/e2e/tier2_boundary_corner.test.ts
   ```
   **Pass Condition**: Test `B11: descompasso temporal (lastReview > now) deve ser contido monotonicamente em zero dias decorridos` passes with 0 failures.

4. **Invalidation Conditions**:
   The fix is considered invalid if:
   - Any property of a card returned by `review()` or `sanitizeCard()` evaluates to `NaN` or `Infinity`.
   - `c.stability < 0.1` or `c.stability > 36500.0` for any reviewed card.
   - `c.difficulty < 1.0` or `c.difficulty > 10.0`.
   - `c.interval < 1` or `c.interval > 36500`.
   - `tDays < 0` when `lastReview > now`.
