# Handoff Report: Explorer M2.2 — Ebbinghaus Harmonization & Study Flow Reentrancy

**Author**: Explorer M2.2 (`teamwork_preview_explorer_m2_2`)  
**Parent Orchestrator**: `0d5d82a5-da3d-44a0-9804-5de6b897019d`  
**Milestone Scope**: Milestone 2 (Features F9, F10)  
**Date**: 2026-10-31  

---

## 1. Observation

### 1.1 Ebbinghaus Property Key Discrepancy (Feature F9)

1. **`js/flashcards.js`**:
   - Line 75: `const tDays = card.lastReview ? (now - card.lastReview) / 86400000 : 0;`
   - Line 117: `FSRS.review(card, rating)` assigns `lastReview: now,` (camelCase) to the updated card.
   - Line 155: `FSRS.migrateSM2(sm2)` populates `lastReview: sm2.ultima_revisao || null,`.
   - Line 761: `if (fsrs && fsrs.stability > 0 && fsrs.lastReview) { const tDays = (Date.now() - fsrs.lastReview) / 86400000; }`.
   - Line 893: `const card = fsrs || { state: 'new', difficulty: 5, stability: 0, lastReview: null };`.
   - Line 918: `lastReview: null`.
   - Verbatim check: `grep_search` across `js/flashcards.js` confirms **zero** occurrences of `last_review`.

2. **`src/analytics/ebbinghausCurve.ts`**:
   - Lines 14–24:
     ```typescript
     export interface FSRSCardInput {
       id?: string;
       stability?: number;
       difficulty?: number;
       intervalo?: number;
       scheduled_days?: number;
       ease_factor?: number;
       ef?: number;
       last_review?: string | number | Date | null;
       [key: string]: unknown;
     }
     ```
     `lastReview` is missing from the interface declaration.
   - Lines 201–218:
     ```typescript
     function getElapsedDays(card: FSRSCardInput | null | undefined): number | null {
       if (!card || card.last_review == null) return null;
       const lr = card.last_review;
       let timeMs: number;
       if (typeof lr === 'number') {
         timeMs = lr;
       } else if (lr instanceof Date) {
         timeMs = lr.getTime();
       } else if (typeof lr === 'string') {
         timeMs = new Date(lr).getTime();
       } else {
         return null;
       }

       if (Number.isNaN(timeMs) || timeMs <= 0) return null;
       const diffMs = Date.now() - timeMs;
       return Math.max(0, diffMs / 86400000);
     }
     ```
     `getElapsedDays` exclusively tests `card.last_review`.
   - Lines 287–290 & 298–301:
     ```typescript
     const elapsed = getElapsedDays(activeCard);
     const cardR = elapsed !== null ? retentionAt(elapsed, sAtual) : retentionTarget;
     sBom = predictNextStabilityGood(activeCard, sAtual, cardR);
     ```
     Because `card.last_review` is always `undefined` when reading cards from `App.estado.flashcardData`, `getElapsedDays` returns `null`. `cardR` is therefore statically fixed to `retentionTarget` (default 0.90 / 90%).
   - Lines 475–486: `getElapsedDays` is not exported on `Ebbinghaus`, violating `PROJECT.md:71` (`Ebbinghaus.getElapsedDays(card: { lastReview?: number, last_review?: number }): number | null`).

3. **`js/ebbinghaus.js`**:
   - Lines 125–137: `getElapsedDays(card)` also checks only `card.last_review`.
   - Lines 187–196:
     ```javascript
     if (activeCard) {
       sAtual = Number(extractS(activeCard).toFixed(1));
       sBom = predictNextStabilityGood(activeCard, sAtual);
       sourceKey = 'focused';
     } else {
       const sumS = effectiveCards.reduce((acc, c) => acc + extractS(c), 0);
       sAtual = Number((sumS / effectiveCards.length).toFixed(1));
       const sumNext = effectiveCards.reduce((acc, c) => acc + predictNextStabilityGood(c, extractS(c)), 0);
       sBom = Number(Math.max(sAtual + 1, sumNext / effectiveCards.length).toFixed(1));
     }
     ```
     `predictNextStabilityGood` is called without the 3rd argument `currentR`. `retentionAt`, `decay`, and `factor` are defined at lines 197–208, *after* lines 187–196.
   - Lines 554–589: `getElapsedDays` is omitted from `window.Ebbinghaus`, `globalThis.Ebbinghaus`, and `module.exports`.

---

### 1.2 Study Flow Reentrancy & Double-Click Flaws (Feature F10)

1. **`Flashcards.avaliar` in `js/flashcards.js`**:
   - Lines 907–909:
     ```javascript
     avaliar(rating) {
       if (!this.cartaAtual) return;
       try {
         const carta = this.cartaAtual;
     ```
     No guard `if (this._bloqueioAvaliacao) return;` exists at function entry.
   - Lines 931–948:
     ```javascript
     App.estado.flashcardData[carta.id] = updated;
     App.salvarFlashcards();
     // ...
     if (typeof Progressao !== 'undefined') {
       Progressao.ganhar(xpGanho);
     }
     ```
     XP is granted, data is committed, heatmap diary is logged (`Calor.registrar(1)` line 961).
   - Lines 975–983:
     ```javascript
     this._bloqueioAvaliacao = true;
     const botoesAvaliar = document.querySelectorAll('.fc-btn-fsrs, .fc-action-btn, #btn-again, #btn-hard, #btn-good, #btn-easy');
     botoesAvaliar.forEach(b => { if (b) b.disabled = true; });
     setTimeout(() => {
       this._bloqueioAvaliacao = false;
       botoesAvaliar.forEach(b => { if (b) b.disabled = false; });
       this.proxima();
     }, 650);
     ```
     `this._bloqueioAvaliacao = true` is placed at line 975, at the very end of the method.
   - Line 976: The button selector omits `.btn-rating` (the class used in `index.html` lines 348–363: `<button id="btn-again" class="btn-rating btn-again" onclick="Flashcards.avaliar(1)">`).
   - Line 1685: Global keydown listener checks `if (typeof Flashcards !== 'undefined' && Flashcards._bloqueioAvaliacao) return;`, but because `_bloqueioAvaliacao` was set late at line 975, rapid key strokes or synthetic click bounces reenter.
   - Test interaction observed in `tests/e2e/tier4_real_world_workloads.test.ts`: Lines 85–89 and 181–205 evaluate multiple cards in a synchronous `forEach` loop by setting `Flashcards.cartaAtual = nextWord; Flashcards.avaliar(3);`. A naive global boolean lock would block legitimate card progression in synchronous test runners if not scoped or cleared when a new card is loaded.

2. **`Quiz.proximaPergunta` in `js/quiz.js`**:
   - Lines 5–13: The `Quiz` object definition lacks `_bloqueioAvanco: false`.
   - Lines 311–319:
     ```javascript
     proximaPergunta() {
       this.perguntaAtual++;
       if (this.perguntaAtual >= this.perguntas.length) {
         this.mostrarResultado();
       } else {
         this._salvarSessao(); // persiste progresso parcial
         this.mostrarPergunta();
       }
     },
     ```
     Zero debounce and zero reentrancy guard.
   - `index.html:418`: `<button class="btn-primario" onclick="Quiz.proximaPergunta()" data-i18n="quiz_continuar">Continuar →</button>`.
   - Lines 347–380 (`mostrarResultado()`):
     ```javascript
     mostrarResultado() {
       this._limparSessao();
       // ...
       if (typeof Calor !== 'undefined') Calor.registrar(this.perguntas.length || 1);
       // ...
       if (this.xpTotal > 0) {
         Progressao.ganhar(this.xpTotal);
       }
       if (typeof Conquistas !== 'undefined') { ... }
     ```
     When double-clicking "Continuar →" on the final question, `mostrarResultado()` is invoked twice. Because `this.xpTotal` is never reset to 0 and there is no idempotency flag, `Progressao.ganhar(this.xpTotal)` fires twice (granting double XP).
   - Test interaction observed in `tests/e2e/tier4_real_world_workloads.test.ts`: Lines 274–288 call `Quiz.proximaPergunta(); Quiz.checarResposta(...); Quiz.proximaPergunta();` synchronously. `checarResposta` must reset the advance lock so sequential questions can be answered without waiting for timer delays in synchronous tests.

---

## 2. Logic Chain

### 2.1 Ebbinghaus Property Key Discrepancy Logic Chain

```
Observation 1.1: Flashcards stores { lastReview: now } in flashcards.js:117
       ↓
Observation 1.2: Flashcards.atualizarEbbinghaus passes App.estado.flashcardData to Ebbinghaus
       ↓
Observation 1.3: ebbinghausCurve.ts:202 and ebbinghaus.js:126 check card.last_review == null
       ↓
Deduction: card.last_review is undefined because Flashcards never set it
       ↓
Deduction: getElapsedDays(activeCard) and getElapsedDays(c) evaluate to null
       ↓
Deduction: cardR defaults to retentionTarget (0.90) in ebbinghausCurve.ts:289
       ↓
Observation 1.4: In predictNextStabilityGood (ebbinghausCurve.ts:180):
  gain = 1 + exp(W8) * (11 - dRaw) * (S)^(-W9) * (exp(W10 * (1 - safeR)) - 1)
  where safeR = clamp(currentR, 0.1, 0.99)
       ↓
Deduction: safeR is clamped to exactly 0.90 regardless of elapsed days (1 hour, 3 days, 30 days)
       ↓
Impact: Retention projections after 'Bom' are statically frozen and do not reflect memory decay or review urgency
```

### 2.2 Flashcards Reentrancy & Double-Click Logic Chain

```
Observation 2.1: Flashcards.avaliar() line 908 has no entry guard
       ↓
Observation 2.2: Flashcards._bloqueioAvaliacao = true is assigned at line 975
       ↓
Observation 2.3: Button disabling occurs at line 977, after XP is granted at line 942
       ↓
User Action: Rapid double-tap on mobile, mouse double-click, or keydown while transition timeout runs
       ↓
Execution:
  Call 1: Reviews cartaAtual, awards XP, schedules setTimeout(proxima, 650)
  Call 2: Reenters before timeout 1 finishes; cartaAtual is STILL the old card!
          Reviews SAME cartaAtual AGAIN, awards DUPLICATE XP, schedules setTimeout(proxima, 650)
       ↓
Timeout Resolution:
  t = 650ms: Timeout 1 fires -> proxima() -> indiceAtual becomes N+1 (shows card N+1)
  t = 650ms + delta: Timeout 2 fires -> proxima() -> indiceAtual becomes N+2 (shows card N+2)
       ↓
Impact: Card N+1 is completely skipped; user loses learning opportunity, duplicate XP awarded, diary corrupted
```

### 2.3 Quiz Advance Debounce Logic Chain

```
Observation 2.4: Quiz.proximaPergunta() increments perguntaAtual with zero guards
       ↓
User Action: Double-click on "Continuar →" button
       ↓
Scenario A (Intermediate question, e.g. question index 2):
  Call 1: perguntaAtual becomes 3 -> mostrarPergunta() displays question 3
  Call 2: perguntaAtual becomes 4 -> mostrarPergunta() displays question 4
  Result: Question 3 is skipped without being presented or answered!
       ↓
Scenario B (Final question, e.g. question index 9 of 10):
  Call 1: perguntaAtual becomes 10 -> mostrarResultado() runs -> awards XP (e.g. 200 XP), logs Calor
  Call 2: perguntaAtual becomes 11 -> mostrarResultado() runs AGAIN -> awards XP AGAIN (400 XP total!), logs Calor again
       ↓
Impact: Question skipping during quiz and duplicate XP granting at end of quiz
```

---

## 3. Caveats

1. **Synchronous Test Suites**:
   - `tests/e2e/tier4_real_world_workloads.test.ts` executes sequential flashcard reviews (`forEach`) and quiz answers without awaiting `setTimeout`.
   - *Design requirement*: The guard in `Flashcards.avaliar` must track `_cardEmAvaliacaoId`. Evaluating a different card ID (`this.cartaAtual.id !== this._cardEmAvaliacaoId`) must proceed unhindered.
   - *Design requirement*: The guard in `Quiz.proximaPergunta` must be unlocked when `Quiz.checarResposta` is invoked for the next question, in addition to the 300ms fallback debounce timer.
2. **Backward Compatibility**:
   - Thousands of existing user profiles in `localStorage` have flashcard records saved with `lastReview`. Older legacy schemas or mock fixtures might have `last_review`.
   - *Design requirement*: Bidirectional fallback (`card.lastReview ?? card.last_review`) ensures 100% retrocompatibility.
3. **No External Runtime Dependencies**:
   - All locks and debounces must use vanilla JS properties and native browser timers (`setTimeout`), adhering to the project's zero-external-runtime-deps constraint.

---

## 4. Conclusion & Exact Proposed Fix Design

### 4.1 Changes to `src/analytics/ebbinghausCurve.ts`

#### Step 1: Update `FSRSCardInput` interface (lines 14–24)
```diff
 export interface FSRSCardInput {
   id?: string;
   stability?: number;
   difficulty?: number;
   intervalo?: number;
   scheduled_days?: number;
   ease_factor?: number;
   ef?: number;
+  lastReview?: string | number | Date | null;
   last_review?: string | number | Date | null;
   [key: string]: unknown;
 }
```

#### Step 2: Update `getElapsedDays` (lines 201–218)
```diff
-function getElapsedDays(card: FSRSCardInput | null | undefined): number | null {
-  if (!card || card.last_review == null) return null;
-  const lr = card.last_review;
+export function getElapsedDays(card: FSRSCardInput | null | undefined): number | null {
+  if (!card) return null;
+  const lr = card.lastReview ?? card.last_review;
+  if (lr == null) return null;
   let timeMs: number;
   if (typeof lr === 'number') {
     timeMs = lr;
   } else if (lr instanceof Date) {
     timeMs = lr.getTime();
   } else if (typeof lr === 'string') {
     timeMs = new Date(lr).getTime();
   } else {
     return null;
   }

   if (Number.isNaN(timeMs) || timeMs <= 0) return null;
   const diffMs = Date.now() - timeMs;
   return Math.max(0, diffMs / 86400000);
 }
```

#### Step 3: Export `getElapsedDays` on `Ebbinghaus` (lines 475–486)
```diff
 export const Ebbinghaus = {
   W8,
   W9,
   W10,
   EBBINGHAUS_I18N,
   calculateRetention,
   calculateTimeToTarget,
   predictNextStabilityGood,
   formatDaysLabel,
+  getElapsedDays,
   computeEbbinghausCurve,
   renderEbbinghausCurve,
 };
```

---

### 4.2 Changes to `js/ebbinghaus.js`

#### Step 1: Update `getElapsedDays` (lines 125–137)
```diff
-function getElapsedDays(card) {
-  if (!card || card.last_review == null) return null;
-  const lr = card.last_review;
+function getElapsedDays(card) {
+  if (!card) return null;
+  const lr = (card.lastReview != null) ? card.lastReview : card.last_review;
+  if (lr == null) return null;
   let timeMs;
   if (typeof lr === 'number') timeMs = lr;
   else if (lr instanceof Date) timeMs = lr.getTime();
   else if (typeof lr === 'string') timeMs = new Date(lr).getTime();
   else return null;

   if (Number.isNaN(timeMs) || timeMs <= 0) return null;
   const diffMs = Date.now() - timeMs;
   return Math.max(0, diffMs / 86400000);
 }
```

#### Step 2: Compute `cardR` dynamically and pass to `predictNextStabilityGood` (lines 184–215)
```diff
   const extractS = (c) => {
     const raw = Number(c.stability ?? c.intervalo ?? c.scheduled_days ?? 0);
     return raw > 0 ? raw : 1;
   };
+
+  const rawW20 = options.w20 ?? options.fsrsDecay ?? 0.5;
+  const clampedW20 = Math.max(0.1, Math.min(0.8, Number(rawW20) || 0.5));
+  const decay = -clampedW20;
+  const factor = Math.pow(0.9, 1 / decay) - 1;
+
+  const retentionAt = (t, s) => {
+    const safeS = Math.max(0.2, s);
+    if (curveMode === 'exponential') {
+      return Math.pow(retentionTarget, t / safeS);
+    }
+    return Math.pow(1 + factor * (t / safeS), decay);
+  };
+
   let sAtual = 1;
   let sBom = 2.5;
   let sourceKey = 'deck_average';
   if (activeCard) {
     sAtual = Number(extractS(activeCard).toFixed(1));
-    sBom = predictNextStabilityGood(activeCard, sAtual);
+    const elapsed = getElapsedDays(activeCard);
+    const cardR = elapsed !== null ? retentionAt(elapsed, sAtual) : retentionTarget;
+    sBom = predictNextStabilityGood(activeCard, sAtual, cardR);
     sourceKey = 'focused';
   } else {
     const sumS = effectiveCards.reduce((acc, c) => acc + extractS(c), 0);
     sAtual = Number((sumS / effectiveCards.length).toFixed(1));
-    const sumNext = effectiveCards.reduce((acc, c) => acc + predictNextStabilityGood(c, extractS(c)), 0);
+    const sumNext = effectiveCards.reduce((acc, c) => {
+      const cS = extractS(c);
+      const elapsed = getElapsedDays(c);
+      const cardR = elapsed !== null ? retentionAt(elapsed, cS) : retentionTarget;
+      return acc + predictNextStabilityGood(c, cS, cardR);
+    }, 0);
     sBom = Number(Math.max(sAtual + 1, sumNext / effectiveCards.length).toFixed(1));
   }
-  const rawW20 = options.w20 ?? options.fsrsDecay ?? 0.5;
-  const clampedW20 = Math.max(0.1, Math.min(0.8, Number(rawW20) || 0.5));
-  const decay = -clampedW20;
-  const factor = Math.pow(0.9, 1 / decay) - 1;
-
-  const retentionAt = (t, s) => {
-    const safeS = Math.max(0.2, s);
-    if (curveMode === 'exponential') {
-      return Math.pow(retentionTarget, t / safeS);
-    }
-    return Math.pow(1 + factor * (t / safeS), decay);
-  };
```

#### Step 3: Export `getElapsedDays` on `Ebbinghaus` (lines 554–589)
```diff
   window.Ebbinghaus = {
     EBBINGHAUS_I18N,
     predictNextStabilityGood,
     formatDaysLabel,
+    getElapsedDays,
     computeEbbinghausCurve,
     renderEbbinghausCurve,
     toggleMode
   };
```
(Repeat for `globalThis.Ebbinghaus` and `module.exports`).

---

### 4.3 Changes to `js/flashcards.js`

#### Step 1: Initialize lock state on `Flashcards` object (around line 180)
```javascript
  _bloqueioAvaliacao: false,
  _cardEmAvaliacaoId: null,
```

#### Step 2: Add dual-key emission in `FSRS.review` and `FSRS.migrateSM2` (lines 117 & 155)
```diff
     return {
       ...card,
       state:          newState,
       difficulty:     newD,
       stability:      newS,
       retrievability: r,
       lapses,
       reps,
       lastReview:     now,
+      last_review:    now,
       interval:       intervalDay,
       nextReview:     now + intervalDay * 86400000,
       history:        [...previousHistory, reviewRecord]
     };
```

#### Step 3: Reentrancy guard in `Flashcards.avaliar` (lines 907–990)
```javascript
  avaliar(rating) {
    if (!this.cartaAtual) return;
    // Reentrancy guard: block multiple evaluations of the same card
    if (this._bloqueioAvaliacao && this._cardEmAvaliacaoId === this.cartaAtual.id) return;
    this._bloqueioAvaliacao = true;
    this._cardEmAvaliacaoId = this.cartaAtual.id;

    // Immediately disable rating buttons to prevent click bounce
    const botoesAvaliar = document.querySelectorAll(
      '.fc-btn-fsrs, .fc-action-btn, #btn-again, #btn-hard, #btn-good, #btn-easy, .btn-rating'
    );
    botoesAvaliar.forEach(b => { if (b) b.disabled = true; });

    try {
      const carta = this.cartaAtual;

      let fsrs = App.estado.flashcardData[carta.id];
      if (fsrs && fsrs.repeticoes !== undefined && fsrs.stability === undefined) {
        fsrs = FSRS.migrateSM2(fsrs);
      }
      if (!fsrs) {
        fsrs = { state: 'new', difficulty: 5, stability: 0, retrievability: 1,
                 lapses: 0, reps: 0, lastReview: null, last_review: null, interval: 0, nextReview: null };
      }

      const wasNew = !fsrs || fsrs.state === 'new';
      const updated = FSRS.review(fsrs, rating);

      // Track error count for "Parole Difficili" feature
      const errosAnteriores = updated.erros || 0;
      if (rating === 1)      updated.erros = errosAnteriores + 1;
      else if (rating >= 3)  updated.erros = Math.max(0, errosAnteriores - 1);

      App.estado.flashcardData[carta.id] = updated;
      App.salvarFlashcards();

      // XP calculation and award
      const xpMap = [0, 0, 5, 10, 15];
      const xpBonus = (this.modoContexto || this.modoEscuta) ? 5 : 0;
      const xpGanho = (xpMap[rating] || 0) + xpBonus;
      if (xpGanho > 0) {
        if (typeof Progressao !== 'undefined') {
          Progressao.ganhar(xpGanho);
        } else {
          App.estado.progresso.xp += xpGanho;
          App.salvarProgresso();
          App.atualizarStats();
        }
      }

      if (this.sessaoStats) {
        const rNames = ['', 'again', 'hard', 'good', 'easy'];
        this.sessaoStats[rNames[rating]]++;
        this.sessaoStats.xp += xpGanho;
        if (wasNew && updated.state === 'review') {
          this.sessaoStats.novas.push(carta);
        }
      }

      if (typeof Calor !== 'undefined') Calor.registrar(1);

      if (typeof Progressao !== 'undefined' && Progressao.temploConcluido(this.temploAtual)) {
        Progressao.marcarTemploConcluido(this.temploAtual);
      }

      if (typeof Conquistas !== 'undefined') {
        if (typeof requestIdleCallback === 'function') requestIdleCallback(() => Conquistas.verificar());
        else setTimeout(() => Conquistas.verificar(), 300);
      }

      this.atualizarEbbinghaus();

      // Micro-pausa de 650ms para absorção cognitiva visual
      setTimeout(() => {
        try {
          this.proxima();
        } finally {
          this._bloqueioAvaliacao = false;
          this._cardEmAvaliacaoId = null;
          botoesAvaliar.forEach(b => { if (b) b.disabled = false; });
        }
      }, 650);
    } catch (err) {
      console.error('[FSRS] avaliar() error:', err);
      App.notificar('notif_fc_erro_resposta', 'erro');
      try {
        this.proxima();
      } finally {
        this._bloqueioAvaliacao = false;
        this._cardEmAvaliacaoId = null;
        botoesAvaliar.forEach(b => { if (b) b.disabled = false; });
      }
    }
  },
```

#### Step 4: Reset lock in `mostrarCarta` and `mostrarVazio` (lines 609 & 1004)
```javascript
  this._bloqueioAvaliacao = false;
  this._cardEmAvaliacaoId = null;
```

---

### 4.4 Changes to `js/quiz.js`

#### Step 1: Initialize flags in `Quiz` object (lines 5–14)
```javascript
  _bloqueioAvanco: false,
  _resultadoMostrado: false,
```

#### Step 2: Reset flags in all `iniciar*` methods (lines 97, 133, 619, 689, 759, 807)
```javascript
  this._bloqueioAvanco = false;
  this._resultadoMostrado = false;
```

#### Step 3: Debounce and lock in `proximaPergunta()` (lines 311–319)
```javascript
  proximaPergunta() {
    if (this._bloqueioAvanco) return;
    this._bloqueioAvanco = true;

    // Immediately disable "Continuar" button to absorb double-clicks
    const btnContinuar = document.querySelector(
      '#explicacao-container .btn-primario, button[data-i18n="quiz_continuar"]'
    );
    if (btnContinuar) btnContinuar.disabled = true;

    try {
      this.perguntaAtual++;
      if (this.perguntaAtual >= this.perguntas.length) {
        this.mostrarResultado();
      } else {
        this._salvarSessao(); // persiste progresso parcial
        this.mostrarPergunta();
      }
    } finally {
      // Fallback debounce window (300ms) to re-enable button and clear lock
      setTimeout(() => {
        this._bloqueioAvanco = false;
        if (btnContinuar) btnContinuar.disabled = false;
      }, 300);
    }
  },
```

#### Step 4: Unlock advance on answering the next question in `checarResposta()` (line 266)
```javascript
  checarResposta(escolha) {
    if (this.respondido) return;
    this.respondido = true;
    this._bloqueioAvanco = false; // Next question answered: unlocking advance button
```

#### Step 5: Idempotency and double-XP protection in `mostrarResultado()` (lines 347–380)
```javascript
  mostrarResultado() {
    if (this._resultadoMostrado) return;
    this._resultadoMostrado = true;
    this._bloqueioAvanco = true;

    this._limparSessao(); // sessão concluída — limpa
    const container = document.getElementById('quiz-container');
    const resultado = document.getElementById('quiz-resultado');
    if (container) container.style.display = 'none';
    this._sincronizarBarraCompacta();

    // Log quiz completion to heatmap diary
    if (typeof Calor !== 'undefined') Calor.registrar(this.perguntas.length || 1);
    if (!resultado) return;
    resultado.style.display = 'block';

    const total = this.perguntas.length;
    const pct = total > 0 ? Math.round((this.pontuacao / total) * 100) : 0;

    let msg = '';
    if (pct >= 90) msg = '🏆 Perfetto! Sei un maestro dell\'italiano!';
    else if (pct >= 70) msg = '👏 Molto bene! Continua così!';
    else if (pct >= 50) msg = '📚 Bene! Ma puoi fare di melhor!';
    else msg = '💪 Non mollare! Continua a studiare!';

    const scoreEl = document.getElementById('resultado-score');
    const xpEl = document.getElementById('resultado-xp');
    const msgEl = document.getElementById('resultado-msg');
    if (scoreEl) scoreEl.textContent = `${this.pontuacao}/${total}`;
    if (xpEl) xpEl.textContent = I18n.t('quiz_xp_ganhos').replace('{n}', this.xpTotal);
    if (msgEl) msgEl.textContent = msg;

    // Give XP and atomically reset to prevent duplicate awards
    const xpParaConceder = this.xpTotal;
    this.xpTotal = 0;
    if (xpParaConceder > 0) {
      Progressao.ganhar(xpParaConceder);
    }

    // Check achievements
    if (typeof Conquistas !== 'undefined') {
      const p = App.estado.progresso;
      if (p) {
        if (pct >= 80) p.quiz_consecutivos_80 = (p.quiz_consecutivos_80 || 0) + 1;
        else p.quiz_consecutivos_80 = 0;
        App.salvarProgresso();
      }
      if (pct === 100) Conquistas.ganharQuizPerfetto();
      Conquistas.verificar();
    }

    // Save to quiz history
    try {
      const historico = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]');
      historico.unshift({
        templo: this.temploAtual,
        pontuacao: pct,
        xp_ganho: xpParaConceder,
        acertos: this.pontuacao,
        total: total,
        data: Date.now()
      });
      localStorage.setItem('it_quiz_historico', JSON.stringify(historico.slice(0, 50)));
    } catch (e) { /* ignore */ }
  },
```

---

## 5. Verification Method

### 5.1 Test Execution
Execute the Vitest suite targeting the affected test suites:
```bash
npx vitest run tests/ebbinghaus.test.ts tests/ebbinghausCurve.test.ts tests/e2e/tier4_real_world_workloads.test.ts
```
Expected result: 3 test files, 28 tests passing with exit code 0.

### 5.2 Unit Verification for Ebbinghaus Harmonization (F9)
In a test file or `tests/ebbinghausCurve.test.ts`:
```typescript
it('computes dynamic retention when card has camelCase lastReview', () => {
  const now = Date.now();
  const cardWithCamelCase = {
    stability: 10,
    difficulty: 5,
    lastReview: now - 20 * 86400000, // 20 days ago
  };
  const cardBaseline = { stability: 10, difficulty: 5 };

  const curveAtrasada = computeEbbinghausCurve([cardWithCamelCase], cardWithCamelCase);
  const curveBaseline = computeEbbinghausCurve([cardBaseline], cardBaseline);

  // When overdue (R < 0.90), stability gain on 'Good' is significantly higher
  expect(curveAtrasada.sBom).toBeGreaterThan(curveBaseline.sBom);
  expect(Ebbinghaus.getElapsedDays(cardWithCamelCase)).toBeCloseTo(20, 1);
});
```

### 5.3 Stress Verification for Flashcard Reentrancy (F10)
```typescript
it('Flashcards.avaliar ignores double-clicks and awards XP only once', () => {
  const initialXP = AppState.estado.progresso.xp;
  Flashcards.cartaAtual = { id: 'card_reentrancy_test', italiano: 'prova', portugues: 'teste' };
  
  // Rapid double-call simulating double click
  Flashcards.avaliar(3);
  Flashcards.avaliar(3);

  expect(Flashcards._bloqueioAvaliacao).toBe(true);
  // XP for Good (rating 3) is 10 XP; must not be 20 XP
  expect(AppState.estado.progresso.xp).toBe(initialXP + 10);
});
```

### 5.4 Stress Verification for Quiz Debounce (F10)
```typescript
it('Quiz.proximaPergunta ignores double-clicks and grants final XP only once', () => {
  Quiz.temploAtual = 1;
  Quiz.perguntas = [
    { id: 'q1', pergunta: 'P1', alternativas: ['A', 'B'], resposta_correta: 'A', xp_recompensa: 20 }
  ];
  Quiz.perguntaAtual = 0;
  Quiz.xpTotal = 20;
  Quiz.pontuacao = 1;

  const initialXP = AppState.estado.progresso.xp;

  // Rapid double-call advancing from question 1
  Quiz.proximaPergunta();
  Quiz.proximaPergunta();

  expect(Quiz._resultadoMostrado).toBe(true);
  expect(AppState.estado.progresso.xp).toBe(initialXP + 20);
});
```

### 5.5 Invalidation Conditions
- Any occurrence of `card.last_review == null` without fallback to `card.lastReview`.
- `Flashcards.avaliar` modifying state or calling `Progressao.ganhar` before verifying `this._bloqueioAvaliacao`.
- `Quiz.proximaPergunta` advancing `this.perguntaAtual` without setting or checking `this._bloqueioAvanco`.
