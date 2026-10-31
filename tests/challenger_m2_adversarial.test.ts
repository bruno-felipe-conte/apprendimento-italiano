// @ts-nocheck
// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import Flashcards from '../js/flashcards.js';
import Quiz from '../js/quiz.js';
import AppNavigation from '../js/core/navigation.js';
import VoiceEngine from '../js/voice_engine';
import Imitazione from '../js/imitazione.js';
import {
  getElapsedDays as tsGetElapsedDays,
  computeEbbinghausCurve as tsComputeEbbinghausCurve,
  calculateRetention as tsCalculateRetention,
  predictNextStabilityGood as tsPredictNextStabilityGood
} from '../src/analytics/ebbinghausCurve';
import '../js/ebbinghaus.js';

describe('Challenger M2 Adversarial Test Suite: Algorithmic Stability, FSRS & Concurrency Guards', () => {
  // ─────────────────────────────────────────────────────────────
  // DOMAIN 1: FSRS Mathematical Bounds & NaN Immunization (F7 & F8)
  // ─────────────────────────────────────────────────────────────
  describe('Domain 1: FSRS Math Extreme Inputs & Temporal Anomaly Defense', () => {
    const FSRS = Flashcards.FSRS || (globalThis as any).FSRS;

    it('FSRS-1.1: sanitizeCard handles null, undefined, primitive, and empty payloads without crashing', () => {
      const corruptInputs = [
        null,
        undefined,
        '',
        'corrupt_string',
        12345,
        true,
        [],
        {}
      ];

      for (const input of corruptInputs) {
        const sanitized = FSRS.sanitizeCard(input as any);
        expect(sanitized).toBeDefined();
        expect(sanitized.state).toBe('new');
        expect(Number.isFinite(sanitized.difficulty)).toBe(true);
        expect(sanitized.difficulty).toBe(5.0);
        expect(sanitized.stability).toBe(0);
        expect(sanitized.retrievability).toBe(1.0);
        expect(sanitized.reps).toBe(0);
        expect(sanitized.lapses).toBe(0);
        expect(sanitized.interval).toBe(0);
        expect(sanitized.lastReview).toBeNull();
        expect(sanitized.last_review).toBeNull();
        expect(Array.isArray(sanitized.history)).toBe(true);
      }
    });

    it('FSRS-1.2: sanitizeCard clamps NaN, Infinity, -Infinity and negative numeric parameters', () => {
      const corruptCard = {
        state: 'invalid_state',
        difficulty: NaN,
        stability: NaN,
        retrievability: NaN,
        interval: NaN,
        reps: -10,
        lapses: -5,
        lastReview: NaN
      };

      const sanitized = FSRS.sanitizeCard(corruptCard as any);
      expect(Number.isFinite(sanitized.difficulty)).toBe(true);
      expect(sanitized.difficulty).toBe(5.0);
      expect(sanitized.stability).toBe(0); // new state
      expect(sanitized.retrievability).toBe(1.0);
      expect(sanitized.reps).toBe(0);
      expect(sanitized.lapses).toBe(0);
      expect(sanitized.interval).toBe(0);

      // Extreme Infinities — non-finite values safely reset to finite defaults
      const infCard = {
        state: 'review',
        difficulty: Infinity,
        stability: Infinity,
        retrievability: 2.5,
        interval: Infinity,
        reps: 10,
        lapses: 0
      };
      const sanitizedInf = FSRS.sanitizeCard(infCard as any);
      expect(Number.isFinite(sanitizedInf.difficulty)).toBe(true);
      expect(sanitizedInf.difficulty).toBeGreaterThanOrEqual(1.0);
      expect(sanitizedInf.difficulty).toBeLessThanOrEqual(10.0);
      expect(Number.isFinite(sanitizedInf.stability)).toBe(true);
      expect(sanitizedInf.stability).toBeGreaterThanOrEqual(0.1);
      expect(sanitizedInf.stability).toBeLessThanOrEqual(36500.0);
      expect(sanitizedInf.retrievability).toBe(1.0); // clamped to [0, 1]

      // Finite out-of-bounds numbers are strictly clamped
      const outOfBoundsCard = {
        state: 'review',
        difficulty: 999.0,
        stability: 999999.0,
        retrievability: 1.5,
        interval: 999999,
        reps: 10,
        lapses: 0
      };
      const sanitizedOut = FSRS.sanitizeCard(outOfBoundsCard as any);
      expect(sanitizedOut.difficulty).toBe(10.0);
      expect(sanitizedOut.stability).toBe(36500.0);
      expect(sanitizedOut.retrievability).toBe(1.0);
      expect(sanitizedOut.interval).toBe(36500);

      // Sub-minimum finite numbers clamped
      const subMinCard = {
        state: 'review',
        difficulty: -100.0,
        stability: -50.0,
        retrievability: -0.5,
        interval: -100,
        reps: -5,
        lapses: -2
      };
      const sanitizedSub = FSRS.sanitizeCard(subMinCard as any);
      expect(sanitizedSub.difficulty).toBe(1.0);
      expect(sanitizedSub.stability).toBe(0.1);
      expect(sanitizedSub.retrievability).toBe(0.0);
      expect(sanitizedSub.interval).toBe(1);
      expect(sanitizedSub.reps).toBe(0);
      expect(sanitizedSub.lapses).toBe(0);
    });

    it('FSRS-1.3: sanitizeCard handles extreme timestamps (1970 epoch, year 3000, 100y in future, corrupt dates)', () => {
      // Year 1970 (0ms)
      const epochCard = FSRS.sanitizeCard({ state: 'review', lastReview: 0 } as any);
      expect(epochCard.lastReview).toBeNull(); // 0 is treated as no valid review date

      // Valid timestamp in year 1970 (e.g. 1 hour past epoch)
      const earlyCard = FSRS.sanitizeCard({ state: 'review', lastReview: 3600000 } as any);
      expect(earlyCard.lastReview).toBe(3600000);
      expect(earlyCard.last_review).toBe(3600000);

      // Year 3000 (32503680000000)
      const year3000 = new Date('3000-01-01T00:00:00Z').getTime();
      const futureCard = FSRS.sanitizeCard({ state: 'review', lastReview: year3000 } as any);
      expect(futureCard.lastReview).toBe(year3000);
      expect(futureCard.last_review).toBe(year3000);

      // ISO string
      const isoCard = FSRS.sanitizeCard({ state: 'review', lastReview: '2026-05-15T12:00:00.000Z' } as any);
      expect(isoCard.lastReview).toBe(new Date('2026-05-15T12:00:00.000Z').getTime());

      // Corrupt string / invalid Date
      const invalidDateCard = FSRS.sanitizeCard({ state: 'review', lastReview: 'not-a-valid-date' } as any);
      expect(invalidDateCard.lastReview).toBeNull();
    });

    it('FSRS-1.4: retrievability is immunized against NaN, Infinity, and negative elapsed time (clock skew)', () => {
      // Clock skew: negative elapsed days must clamp to 1.0
      expect(FSRS.retrievability(-10, 2)).toBe(1.0);
      expect(FSRS.retrievability(-0.00001, 5)).toBe(1.0);
      expect(FSRS.retrievability(0, 5)).toBe(1.0);

      // Non-finite values
      expect(FSRS.retrievability(NaN, 2)).toBe(1.0);
      expect(FSRS.retrievability(5, NaN)).toBe(1.0);
      expect(FSRS.retrievability(NaN, NaN)).toBe(1.0);
      expect(FSRS.retrievability(Infinity, 2)).toBeLessThanOrEqual(1.0);
      expect(FSRS.retrievability(Infinity, 2)).toBeGreaterThanOrEqual(0.0);
      expect(FSRS.retrievability(2, Infinity)).toBe(1.0);
      expect(FSRS.retrievability(-Infinity, 2)).toBe(1.0);

      // Stability <= 0
      expect(FSRS.retrievability(5, 0)).toBe(1.0);
      expect(FSRS.retrievability(5, -2)).toBe(1.0);

      // Normal decay bounds: always in [0.0, 1.0]
      const r = FSRS.retrievability(30, 5);
      expect(r).toBeGreaterThan(0.0);
      expect(r).toBeLessThan(1.0);
      expect(Number.isFinite(r)).toBe(true);
    });

    it('FSRS-1.5: nextInterval clamps strictly within [MIN_INTERVAL, MAX_INTERVAL] for all inputs', () => {
      expect(FSRS.nextInterval(NaN)).toBe(1);
      expect(FSRS.nextInterval(-100)).toBe(1);
      expect(FSRS.nextInterval(0)).toBe(1);
      expect(FSRS.nextInterval(-Infinity)).toBe(1);

      // Non-finite or extreme finite intervals
      const ivInf = FSRS.nextInterval(Infinity);
      expect(Number.isInteger(ivInf)).toBe(true);
      expect(ivInf).toBeGreaterThanOrEqual(1);
      expect(ivInf).toBeLessThanOrEqual(36500);

      expect(FSRS.nextInterval(1000000)).toBe(36500);
      expect(FSRS.nextInterval(0.1)).toBe(1);

      const iv = FSRS.nextInterval(10);
      expect(Number.isInteger(iv)).toBe(true);
      expect(iv).toBeGreaterThanOrEqual(1);
      expect(iv).toBeLessThanOrEqual(36500);
    });

    it('FSRS-1.6: nextDifficulty maintains strict [1.0, 10.0] bounds under adversarial ratings', () => {
      const invalidRatings = [-5, 0, 5, 10, NaN, Infinity, -Infinity, null, undefined];
      for (const r of invalidRatings) {
        const d = FSRS.nextDifficulty(5.0, r as any);
        expect(Number.isFinite(d)).toBe(true);
        expect(d).toBeGreaterThanOrEqual(1.0);
        expect(d).toBeLessThanOrEqual(10.0);
      }

      // Extreme initial difficulties with FSRS mean reversion toward d0easy
      const dFromNan = FSRS.nextDifficulty(NaN, 3);
      expect(Number.isFinite(dFromNan)).toBe(true);
      expect(dFromNan).toBeGreaterThanOrEqual(1.0);
      expect(dFromNan).toBeLessThanOrEqual(10.0);
      expect(dFromNan).toBeCloseTo(4.90, 2);

      const dFromInf = FSRS.nextDifficulty(Infinity, 4);
      expect(Number.isFinite(dFromInf)).toBe(true);
      expect(dFromInf).toBeGreaterThanOrEqual(1.0);
      expect(dFromInf).toBeLessThanOrEqual(10.0);

      const dFromNegInf = FSRS.nextDifficulty(-Infinity, 1);
      expect(Number.isFinite(dFromNegInf)).toBe(true);
      expect(dFromNegInf).toBeGreaterThanOrEqual(1.0);
      expect(dFromNegInf).toBeLessThanOrEqual(10.0);
    });

    it('FSRS-1.7: nextRecallStability and nextForgetStability never produce NaN or escape [MIN_STABILITY, MAX_STABILITY]', () => {
      // Adversarial inputs to nextRecallStability
      const recallRes = FSRS.nextRecallStability(NaN, NaN, NaN, NaN);
      expect(Number.isFinite(recallRes)).toBe(true);
      expect(recallRes).toBeGreaterThanOrEqual(0.1);
      expect(recallRes).toBeLessThanOrEqual(36500.0);

      // Extreme high values
      const highRecall = FSRS.nextRecallStability(10.0, 36500.0, 0.1, 4);
      expect(Number.isFinite(highRecall)).toBe(true);
      expect(highRecall).toBeLessThanOrEqual(36500.0);

      // Adversarial inputs to nextForgetStability
      const forgetRes = FSRS.nextForgetStability(NaN, NaN, NaN);
      expect(Number.isFinite(forgetRes)).toBe(true);
      expect(forgetRes).toBeGreaterThanOrEqual(0.1);
      expect(forgetRes).toBeLessThanOrEqual(36500.0);

      const highForget = FSRS.nextForgetStability(1.0, 1000.0, 0.0);
      expect(Number.isFinite(highForget)).toBe(true);
      expect(highForget).toBeGreaterThanOrEqual(0.1);
      expect(highForget).toBeLessThanOrEqual(36500.0);
    });

    it('FSRS-1.8: review() survives device clock skew (lastReview in the future) without negative intervals or NaN', () => {
      const futureTime = Date.now() + 100 * 86400000; // 100 days in the future!
      const skewedCard = {
        state: 'review',
        difficulty: 4.5,
        stability: 10.0,
        reps: 3,
        lapses: 0,
        lastReview: futureTime,
        last_review: futureTime
      };

      const updated = FSRS.review(skewedCard as any, 3);
      expect(Number.isFinite(updated.difficulty)).toBe(true);
      expect(Number.isFinite(updated.stability)).toBe(true);
      expect(Number.isFinite(updated.interval)).toBe(true);
      expect(updated.interval).toBeGreaterThanOrEqual(1);
      expect(updated.lastReview).toBeCloseTo(Date.now(), -3);
      expect(updated.last_review).toBe(updated.lastReview);
      expect(updated.nextReview).toBe(updated.lastReview + updated.interval * 86400000);
    });

    it('FSRS-1.9: Fuzzing stress — 100 consecutive reviews with randomized intervals and ratings never corrupt state', () => {
      let card: any = { state: 'new' };
      const ratings = [1, 2, 3, 4, 0, 5, NaN]; // includes chaotic ratings

      for (let i = 0; i < 100; i++) {
        const rating = ratings[Math.floor(Math.random() * ratings.length)];
        card = FSRS.review(card, rating);

        expect(Number.isFinite(card.difficulty)).toBe(true);
        expect(card.difficulty).toBeGreaterThanOrEqual(1.0);
        expect(card.difficulty).toBeLessThanOrEqual(10.0);

        expect(Number.isFinite(card.stability)).toBe(true);
        expect(card.stability).toBeGreaterThanOrEqual(0.1);
        expect(card.stability).toBeLessThanOrEqual(36500.0);

        expect(Number.isFinite(card.interval)).toBe(true);
        expect(card.interval).toBeGreaterThanOrEqual(1);
        expect(card.interval).toBeLessThanOrEqual(36500);

        expect(Number.isFinite(card.retrievability)).toBe(true);
        expect(card.retrievability).toBeGreaterThanOrEqual(0.0);
        expect(card.retrievability).toBeLessThanOrEqual(1.0);

        expect(card.lastReview).toBeDefined();
        expect(card.lastReview).toBe(card.last_review);
      }
    });
  });

  // ─────────────────────────────────────────────────────────────
  // DOMAIN 2: Ebbinghaus Property Key Harmonization & Dynamic Retrievability (F9)
  // ─────────────────────────────────────────────────────────────
  describe('Domain 2: Ebbinghaus Property Key Compatibility & Dynamic Retrievability', () => {
    const jsEbbinghaus = (globalThis as any).Ebbinghaus;

    it('EBB-2.1: getElapsedDays accurately parses camelCase lastReview, snake_case last_review, ISO strings, and Dates across TS and JS implementations', () => {
      const now = Date.now();
      const threeDaysAgoMs = now - 3 * 86400000;
      const threeDaysAgoIso = new Date(threeDaysAgoMs).toISOString();
      const threeDaysAgoDate = new Date(threeDaysAgoMs);

      const testCases = [
        { label: 'camelCase number', card: { lastReview: threeDaysAgoMs } },
        { label: 'snake_case number', card: { last_review: threeDaysAgoMs } },
        { label: 'both present', card: { lastReview: threeDaysAgoMs, last_review: threeDaysAgoMs } },
        { label: 'camelCase ISO string', card: { lastReview: threeDaysAgoIso } },
        { label: 'snake_case ISO string', card: { last_review: threeDaysAgoIso } },
        { label: 'Date instance', card: { lastReview: threeDaysAgoDate } }
      ];

      for (const tc of testCases) {
        const elapsedTs = tsGetElapsedDays(tc.card as any);
        const elapsedJs = jsEbbinghaus.getElapsedDays(tc.card);

        expect(elapsedTs, `TS failed on ${tc.label}`).not.toBeNull();
        expect(elapsedJs, `JS failed on ${tc.label}`).not.toBeNull();
        expect(elapsedTs!).toBeCloseTo(3.0, 1);
        expect(elapsedJs!).toBeCloseTo(3.0, 1);
      }
    });

    it('EBB-2.2: getElapsedDays handles null, undefined, invalid strings, and future timestamps (clock skew)', () => {
      const invalidCards = [
        null,
        undefined,
        {},
        { lastReview: null },
        { last_review: undefined },
        { lastReview: 'corrupt_timestamp' },
        { lastReview: -500 },
        { last_review: 0 }
      ];

      for (const c of invalidCards) {
        expect(tsGetElapsedDays(c as any)).toBeNull();
        expect(jsEbbinghaus.getElapsedDays(c)).toBeNull();
      }

      // Future clock skew: must return 0, never negative
      const futureCard = { lastReview: Date.now() + 5 * 86400000 };
      expect(tsGetElapsedDays(futureCard)).toBe(0);
      expect(jsEbbinghaus.getElapsedDays(futureCard)).toBe(0);
    });

    it('EBB-2.3: Dynamic retrievability test — overdue cards yield higher stability boost than fresh cards', () => {
      const now = Date.now();

      // Card reviewed fresh (0 days ago, R ≈ 1.0)
      const freshCard = {
        difficulty: 5.0,
        stability: 4.0,
        lastReview: now
      };

      // Card overdue (30 days ago, R will be much lower, e.g. < 0.40)
      const overdueCard = {
        difficulty: 5.0,
        stability: 4.0,
        lastReview: now - 30 * 86400000
      };

      // Test TS computeEbbinghausCurve
      const resFreshTs = tsComputeEbbinghausCurve([freshCard], freshCard);
      const resOverdueTs = tsComputeEbbinghausCurve([overdueCard], overdueCard);

      expect(resFreshTs.hasData).toBe(true);
      expect(resOverdueTs.hasData).toBe(true);
      // In FSRS, recall under low retrievability gives a larger stability increment:
      expect(resOverdueTs.sBom).toBeGreaterThan(resFreshTs.sBom);

      // Test JS computeEbbinghausCurve
      const resFreshJs = jsEbbinghaus.computeEbbinghausCurve([freshCard], freshCard);
      const resOverdueJs = jsEbbinghaus.computeEbbinghausCurve([overdueCard], overdueCard);

      expect(resFreshJs.hasData).toBe(true);
      expect(resOverdueJs.hasData).toBe(true);
      expect(resOverdueJs.sBom).toBeGreaterThan(resFreshJs.sBom);
    });

    it('EBB-2.4: computeEbbinghausCurve generates valid SVG paths without NaN or invalid coordinates on mixed key decks', () => {
      const deck = [
        { id: '1', difficulty: 4.0, stability: 3.5, lastReview: Date.now() - 2 * 86400000 },
        { id: '2', difficulty: 6.0, stability: 5.0, last_review: Date.now() - 5 * 86400000 },
        { id: '3', difficulty: 5.0, stability: 1.0 } // no review date
      ];

      const res = jsEbbinghaus.computeEbbinghausCurve(deck, null);
      expect(res.hasData).toBe(true);
      expect(res.pathAtual).toContain('M ');
      expect(res.pathAtual).not.toContain('NaN');
      expect(res.pathBom).toContain('M ');
      expect(res.pathBom).not.toContain('NaN');
      expect(Number.isFinite(res.sAtual)).toBe(true);
      expect(Number.isFinite(res.sBom)).toBe(true);
      expect(res.sBom).toBeGreaterThan(res.sAtual);
    });
  });

  // ─────────────────────────────────────────────────────────────
  // DOMAIN 3: Study Flow Reentrancy & Double-Click Guards (F10)
  // ─────────────────────────────────────────────────────────────
  describe('Domain 3: Reentrancy & Concurrency Double Invocation Probes', () => {
    beforeEach(() => {
      document.body.innerHTML = `
        <div id="flashcard" style="display:block">
          <button id="btn-again" class="fc-btn-fsrs">Again</button>
          <button id="btn-hard" class="fc-btn-fsrs">Hard</button>
          <button id="btn-good" class="fc-btn-fsrs">Good</button>
          <button id="btn-easy" class="fc-btn-fsrs">Easy</button>
        </div>
        <div id="card-actions"></div>
        <div id="flashcard-vazio" style="display:none"></div>
        <div id="explicacao-container" style="display:none">
          <button class="btn-primario">Continuar</button>
          <div id="explicacao-texto"></div>
        </div>
        <div id="quiz-container" style="display:block">
          <div id="opcoes-container"></div>
        </div>
        <div id="quiz-resultado" style="display:none">
          <span id="resultado-score"></span>
          <span id="resultado-xp"></span>
          <span id="resultado-msg"></span>
        </div>
        <div id="ebbinghaus-container"></div>
      `;

      (globalThis as any).App = {
        estado: {
          flashcardData: {},
          progresso: { xp: 0, nivel: 1 }
        },
        salvarFlashcards: vi.fn(),
        salvarProgresso: vi.fn(),
        atualizarStats: vi.fn(),
        notificar: vi.fn()
      };

      (globalThis as any).Progressao = {
        ganhar: vi.fn(),
        temploConcluido: vi.fn(() => false),
        marcarTemploConcluido: vi.fn()
      };

      (globalThis as any).I18n = {
        t: vi.fn((k: string) => k)
      };
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    it('REENT-3.1: Flashcards.avaliar blocks rapid synchronous double-invocation, preventing duplicate reviews and double XP', () => {
      const card = { id: 'card_reentrancy_test', front: 'ciao', back: 'olá' };
      Flashcards.cartaAtual = card;
      Flashcards._bloqueioAvaliacao = false;
      Flashcards._cardEmAvaliacaoId = null;

      (globalThis as any).App.estado.flashcardData['card_reentrancy_test'] = {
        state: 'new',
        difficulty: 5.0,
        stability: 0,
        reps: 0,
        lapses: 0
      };

      const spyReview = vi.spyOn(Flashcards.FSRS, 'review');

      // Double invocation in rapid synchronous sequence:
      Flashcards.avaliar(3); // Call 1
      Flashcards.avaliar(3); // Call 2 — must be rejected by reentrancy lock

      // Assert review called only once
      expect(spyReview).toHaveBeenCalledTimes(1);
      // Assert XP granted only once
      expect((globalThis as any).Progressao.ganhar).toHaveBeenCalledTimes(1);

      // Assert buttons were disabled
      const btnGood = document.getElementById('btn-good') as HTMLButtonElement;
      expect(btnGood.disabled).toBe(true);

      // Clean up timers
      Flashcards._bloqueioAvaliacao = false;
      Flashcards._cardEmAvaliacaoId = null;
    });

    it('REENT-3.2: Flashcards.avaliar releases reentrancy lock in finally block if exception occurs', () => {
      const card = { id: 'card_err_test', front: 'ciao', back: 'olá' };
      Flashcards.cartaAtual = card;
      Flashcards._bloqueioAvaliacao = false;
      Flashcards._cardEmAvaliacaoId = null;

      // Force an unexpected exception in salvarFlashcards
      (globalThis as any).App.salvarFlashcards = vi.fn(() => {
        throw new Error('Storage simulated catastrophic failure');
      });

      const spyProxima = vi.spyOn(Flashcards, 'proxima').mockImplementation(() => {});

      Flashcards.avaliar(3);

      // Lock MUST be released despite exception
      expect(Flashcards._bloqueioAvaliacao).toBe(false);
      expect(Flashcards._cardEmAvaliacaoId).toBeNull();
      // User notification must be fired
      expect((globalThis as any).App.notificar).toHaveBeenCalledWith('notif_fc_erro_resposta', 'erro');
      // Proxima card must be called so user is not stuck
      expect(spyProxima).toHaveBeenCalled();
    });

    it('REENT-3.3: Quiz.proximaPergunta debounces rapid repeated invocations, preventing skipped questions', () => {
      Quiz._bloqueioAvanco = false;
      Quiz.perguntaAtual = 0;
      Quiz.perguntas = [
        { id: 1, pergunta: 'Q1', opcoes: ['A', 'B'], resposta_correta: 'A' },
        { id: 2, pergunta: 'Q2', opcoes: ['A', 'B'], resposta_correta: 'B' },
        { id: 3, pergunta: 'Q3', opcoes: ['A', 'B'], resposta_correta: 'A' }
      ];

      vi.spyOn(Quiz, 'mostrarPergunta').mockImplementation(() => {});

      // Invoke 5 times in a rapid loop
      for (let i = 0; i < 5; i++) {
        Quiz.proximaPergunta();
      }

      // PerguntaAtual must only advance by 1
      expect(Quiz.perguntaAtual).toBe(1);
      expect(Quiz._bloqueioAvanco).toBe(true);

      // Clean up
      Quiz._bloqueioAvanco = false;
    });

    it('REENT-3.4: Quiz.mostrarResultado grants XP idempotently and zeroes xpTotal atomically', () => {
      Quiz._bloqueioAvanco = false;
      Quiz._resultadoMostrado = false;
      Quiz.pontuacao = 3;
      Quiz.perguntas = [{ id: 1 }, { id: 2 }, { id: 3 }] as any;
      Quiz.xpTotal = 150;

      // First call
      Quiz.mostrarResultado();

      expect((globalThis as any).Progressao.ganhar).toHaveBeenCalledTimes(1);
      expect((globalThis as any).Progressao.ganhar).toHaveBeenCalledWith(150);
      expect(Quiz.xpTotal).toBe(0);
      expect(Quiz._resultadoMostrado).toBe(true);

      // Immediate second call (double invocation)
      Quiz.mostrarResultado();

      // Progressao.ganhar must NOT be called a second time
      expect((globalThis as any).Progressao.ganhar).toHaveBeenCalledTimes(1);
    });
  });

  // ─────────────────────────────────────────────────────────────
  // DOMAIN 4: Audio Lifecycle, Teardown & Rejection Safety (F11 & F12)
  // ─────────────────────────────────────────────────────────────
  describe('Domain 4: Audio Lifecycle & Navigation Route Teardown', () => {
    let mockSpeechCancel: any;
    let mockAudioTrack: any;
    let mockUserAudioPause: any;

    beforeEach(() => {
      mockSpeechCancel = vi.fn();
      mockAudioTrack = { stop: vi.fn() };
      mockUserAudioPause = vi.fn();

      window.speechSynthesis = {
        cancel: mockSpeechCancel,
        speak: vi.fn(),
        getVoices: vi.fn(() => [])
      } as any;

      (globalThis as any).Storie = {
        _pararAudioPagina: vi.fn(),
        renderizarSeletor: vi.fn()
      };

      (globalThis as any).Dialoghi = {
        renderizarSeletor: vi.fn()
      };

      (globalThis as any).Vocab = {
        renderizar: vi.fn()
      };

      (globalThis as any).Grammatica = {
        renderizarSeletor: vi.fn()
      };

      (globalThis as any).Profilo = {
        renderizar: vi.fn()
      };

      (globalThis as any).Imitazione = Imitazione;
      Imitazione.renderizar = vi.fn();
      Imitazione.pararGravacao = vi.fn();
      Imitazione._userAudioPlayer = {
        pause: mockUserAudioPause,
        currentTime: 10
      } as any;
      Imitazione._mediaStream = {
        getTracks: () => [mockAudioTrack]
      } as any;

      (globalThis as any).Flashcards = Flashcards;
      Flashcards.gravando = true;
      Flashcards.pararGravacao = vi.fn(() => { Flashcards.gravando = false; });
      Flashcards.atualizarSelectTemplo = vi.fn();
      Flashcards.atualizarEbbinghaus = vi.fn();

      (globalThis as any).Canzoni = {
        pararAudio: vi.fn(),
        renderizarSeletor: vi.fn()
      };
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    it('AUDIO-4.1: teardownAudio cleanly terminates active speech, worker voice promises, media streams, and audio elements', () => {
      (window as any)._activeUtterance = { text: 'test' };
      (window as any)._vocabActiveUtterance = { text: 'vocab' };

      const rejectedReasons: any[] = [];
      VoiceEngine._pendingSyntheses.set('mock_job_1', {
        resolve: vi.fn(),
        reject: (err: any) => rejectedReasons.push(err)
      });

      const initialEpoch = VoiceEngine._sessionEpoch;

      // Execute teardown
      AppNavigation.teardownAudio('templi');

      // 1. Web Speech API cancel invoked and anchors cleared
      expect(mockSpeechCancel).toHaveBeenCalled();
      expect((window as any)._activeUtterance).toBeNull();
      expect((window as any)._vocabActiveUtterance).toBeNull();

      // 2. VoiceEngine epoch incremented and pending syntheses aborted
      expect(VoiceEngine._sessionEpoch).toBeGreaterThan(initialEpoch);
      expect(rejectedReasons.length).toBe(1);
      expect(rejectedReasons[0].name).toBe('AbortError');
      expect(VoiceEngine._pendingSyntheses.size).toBe(0);

      // 3. Storie audio stopped
      expect((globalThis as any).Storie._pararAudioPagina).toHaveBeenCalled();

      // 4. Imitazione mic track stopped and player paused
      expect(mockAudioTrack.stop).toHaveBeenCalled();
      expect(Imitazione._mediaStream).toBeNull();
      expect(mockUserAudioPause).toHaveBeenCalled();

      // 5. Flashcards recording stopped
      expect(Flashcards.pararGravacao).toHaveBeenCalled();

      // 6. Canzoni stopped
      expect((globalThis as any).Canzoni.pararAudio).toHaveBeenCalled();
    });

    it('AUDIO-4.2: Rapid route transition stress — rapid navigation cycling produces zero unhandled rejections or runtime crashes', () => {
      const routes = ['templi', 'flashcard', 'canzoni', 'imitazione', 'quiz', 'storie', 'vocabolario'];

      // Cycle rapidly across routes 20 times
      for (let i = 0; i < 20; i++) {
        const targetRoute = routes[i % routes.length];
        expect(() => AppNavigation.navegar(targetRoute)).not.toThrow();
      }
    });

    it('AUDIO-4.3: Imitazione.tocarMinhaGravacao catches AbortError and interruptions without unhandled rejection', async () => {
      Imitazione._userAudioUrl = 'blob:http://localhost/mock-audio';

      // Mock HTMLAudioElement play() rejecting with AbortError using a proper class constructor
      const mockPlay = vi.fn(() => Promise.reject(new DOMException('The play() request was interrupted by a call to pause().', 'AbortError')));
      window.Audio = class {
        play = mockPlay;
        pause = vi.fn();
        currentTime = 0;
        constructor(public src?: string) {}
      } as any;

      // Executing tocarMinhaGravacao must handle the rejection internally without throwing
      await expect(
        (async () => {
          Imitazione.tocarMinhaGravacao();
          // allow microtasks to settle
          await new Promise(r => setTimeout(r, 10));
        })()
      ).resolves.not.toThrow();

      expect(mockPlay).toHaveBeenCalled();
    });
  });
});
