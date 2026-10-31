// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import '../js/core/storage.js';
import AppState from '../js/core/state.js';

const SafeStorage = globalThis.SafeStorage;

describe('Challenger M1.1 — Adversarial Storage, Quota & Corruption Verification', () => {

  beforeEach(() => {
    localStorage.clear();
    SafeStorage._isAvailable = true;
    SafeStorage._memoryFallback = {};
    AppState.estado.progresso = null;
    AppState.estado.flashcardData = {};
    AppState._ultimoAlertaArmazenamento = 0;
  });

  // ============================================================
  // REQUIREMENT 1: QuotaExceededError across browser engines
  // ============================================================
  describe('Req 1: QuotaExceededError Detection Across Browser Formats', () => {
    it('1.1: should recognize standard DOMException QuotaExceededError', () => {
      const err = new DOMException('The quota has been exceeded.', 'QuotaExceededError');
      expect(SafeStorage.isQuotaExceeded(err)).toBe(true);
    });

    it('1.2: should recognize Safari code 22 QuotaExceededError', () => {
      const safariErr = {
        name: 'QuotaExceededError',
        code: 22,
        message: 'The quota has been exceeded'
      };
      expect(SafeStorage.isQuotaExceeded(safariErr)).toBe(true);
    });

    it('1.3: should recognize Firefox code 1014 and NS_ERROR_DOM_QUOTA_REACHED', () => {
      const firefoxErr = {
        name: 'NS_ERROR_DOM_QUOTA_REACHED',
        code: 1014,
        message: 'Persistent storage maximum size reached'
      };
      expect(SafeStorage.isQuotaExceeded(firefoxErr)).toBe(true);
    });

    it('1.4: should recognize legacy Edge/IE number bitmask for quota error', () => {
      const ieErr1 = { number: -2147024882, message: 'Out of memory' };
      const ieErr2 = { number: 0x80070070, message: 'There is not enough space on the disk' };
      expect(SafeStorage.isQuotaExceeded(ieErr1)).toBe(true);
      expect(SafeStorage.isQuotaExceeded(ieErr2)).toBe(true);
    });

    it('1.5: should recognize message-based quota errors across engines', () => {
      expect(SafeStorage.isQuotaExceeded(new Error('QuotaExceededError: storage full'))).toBe(true);
      expect(SafeStorage.isQuotaExceeded(new Error('localStorage quota exceeded'))).toBe(true);
      expect(SafeStorage.isQuotaExceeded(new Error('NS_ERROR_DOM_QUOTA_REACHED: out of space'))).toBe(true);
    });

    it('1.6: should reject non-quota exceptions, but surface overbroad message match', () => {
      expect(SafeStorage.isQuotaExceeded(new TypeError('Cannot read property of null'))).toBe(false);
      expect(SafeStorage.isQuotaExceeded({ name: 'SecurityError', code: 18 })).toBe(false);
      expect(SafeStorage.isQuotaExceeded(null)).toBe(false);
      expect(SafeStorage.isQuotaExceeded(undefined)).toBe(false);
      expect(SafeStorage.isQuotaExceeded('string error')).toBe(false);
      expect(SafeStorage.isQuotaExceeded(42)).toBe(false);

      // ADVERSARIAL FINDING: RangeError with 'exceeded' in message matches overbroad regex
      const stackOverflow = new RangeError('Maximum call stack size exceeded');
      // Line 64 of storage.js checks e.message.includes('exceeded'), causing a false positive:
      const matchesExceeded = SafeStorage.isQuotaExceeded(stackOverflow);
      expect(matchesExceeded).toBe(true); // Demonstrates confirmed empirical false positive
    });

    it('1.7: should trigger eviction ladder when Safari code 22 error is thrown by localStorage.setItem', () => {
      const originalSetItem = Storage.prototype.setItem;
      let targetWriteAttempts = 0;

      localStorage.setItem('it_swr_templos_meta', 'temp-data');

      Storage.prototype.setItem = function(key, val) {
        if (key === 'it_test_safari') {
          targetWriteAttempts++;
          if (targetWriteAttempts === 1) {
            const safariErr = new Error('Quota exceeded');
            safariErr.name = 'QuotaExceededError';
            safariErr.code = 22;
            throw safariErr;
          }
        }
        return originalSetItem.call(this, key, val);
      };

      try {
        const stored = SafeStorage.setItem('it_test_safari', { test: true });
        expect(stored).toBe(true);
        expect(targetWriteAttempts).toBe(2); // First failed with Safari error, second succeeded after Step 1
        expect(localStorage.getItem('it_swr_templos_meta')).toBeNull();
      } finally {
        Storage.prototype.setItem = originalSetItem;
      }
    });

    it('1.8: should trigger eviction ladder when Firefox code 1014 is thrown by localStorage.setItem', () => {
      const originalSetItem = Storage.prototype.setItem;
      let targetWriteAttempts = 0;

      localStorage.setItem('it_swr_grammar', 'grammar-cache');

      Storage.prototype.setItem = function(key, val) {
        if (key === 'it_test_ff') {
          targetWriteAttempts++;
          if (targetWriteAttempts === 1) {
            const ffErr = new Error('Storage limit reached');
            ffErr.name = 'NS_ERROR_DOM_QUOTA_REACHED';
            ffErr.code = 1014;
            throw ffErr;
          }
        }
        return originalSetItem.call(this, key, val);
      };

      try {
        const stored = SafeStorage.setItem('it_test_ff', { test: 'ff' });
        expect(stored).toBe(true);
        expect(targetWriteAttempts).toBe(2);
        expect(localStorage.getItem('it_swr_grammar')).toBeNull();
      } finally {
        Storage.prototype.setItem = originalSetItem;
      }
    });

    it('1.9: should NOT trigger eviction ladder on non-quota errors (e.g. SecurityError)', () => {
      const originalSetItem = Storage.prototype.setItem;
      localStorage.setItem('it_swr_canzoni', 'must-not-be-deleted');

      Storage.prototype.setItem = function(key, val) {
        if (key === 'test_sec') {
          const secErr = new Error('Access denied');
          secErr.name = 'SecurityError';
          secErr.code = 18;
          throw secErr;
        }
        return originalSetItem.call(this, key, val);
      };

      try {
        const result = SafeStorage.setItem('test_sec', 'value');
        expect(result).toBe(false);
        // SWR key must NOT have been evicted because error was NOT quota related
        expect(localStorage.getItem('it_swr_canzoni')).toBe('must-not-be-deleted');
      } finally {
        Storage.prototype.setItem = originalSetItem;
      }
    });
  });

  // ============================================================
  // REQUIREMENT 2: SWR Caches evicted BEFORE Flashcards
  // ============================================================
  describe('Req 2: SWR Caches Evicted Before Flashcards in Ladder', () => {
    it('2.1: SWR caches must be purged at Step 1 WITHOUT touching flashcards when SWR eviction suffices', () => {
      const originalSetItem = Storage.prototype.setItem;
      const flashcardsInitial = JSON.stringify({
        card_1: { id: 'card_1', state: 'suspended', front: 'test' }
      });
      localStorage.setItem('it_flashcards', flashcardsInitial);
      localStorage.setItem('it_swr_templos_meta', 'swr-content-meta');
      localStorage.setItem('it_swr_canzoni', 'swr-content-canzoni');

      const gcSpy = vi.spyOn(AppState, '_gcFlashcards');

      let targetAttempts = 0;
      Storage.prototype.setItem = function(key, val) {
        if (key === 'it_progresso') {
          targetAttempts++;
          if (targetAttempts === 1) {
            const err = new DOMException('QuotaExceededError', 'QuotaExceededError');
            throw err;
          }
        }
        return originalSetItem.call(this, key, val);
      };

      try {
        const ok = SafeStorage.setItem('it_progresso', { nivel: 2, xp: 500 });
        expect(ok).toBe(true);
        expect(targetAttempts).toBe(2);

        // Step 1 freed SWR keys
        expect(localStorage.getItem('it_swr_templos_meta')).toBeNull();
        expect(localStorage.getItem('it_swr_canzoni')).toBeNull();

        // Flashcards in localStorage must remain completely untouched
        expect(localStorage.getItem('it_flashcards')).toBe(flashcardsInitial);

        // AppState._gcFlashcards must NOT have been called!
        expect(gcSpy).not.toHaveBeenCalled();
      } finally {
        Storage.prototype.setItem = originalSetItem;
        gcSpy.mockRestore();
      }
    });

    it('2.2: Flashcards GC (Step 3) must be called ONLY IF Step 1 (SWR) and Step 2 (logs) do not resolve quota', () => {
      const originalSetItem = Storage.prototype.setItem;
      const originalRemoveItem = Storage.prototype.removeItem;
      const order = [];

      localStorage.setItem('it_swr_dialogi', 'swr-dialog-data');
      localStorage.setItem('it_client_errors', 'logged error');

      AppState.estado.flashcardData = {
        card_old: { id: 'card_old', state: 'suspended', lastReview: 1000 }
      };
      localStorage.setItem('it_flashcards', JSON.stringify(AppState.estado.flashcardData));

      Storage.prototype.removeItem = function(key) {
        if (key.startsWith('it_swr_')) {
          order.push(`evict_swr:${key}`);
        } else if (key === 'it_client_errors') {
          order.push(`evict_log:${key}`);
        }
        return originalRemoveItem.call(this, key);
      };

      let targetAttempts = 0;
      Storage.prototype.setItem = function(key, val) {
        if (key === 'it_progresso') {
          targetAttempts++;
          if (targetAttempts <= 3) {
            // Fail on initial attempt (1), fail after Step 1 SWR (2), fail after Step 2 logs (3)
            const err = new DOMException('QuotaExceededError', 'QuotaExceededError');
            throw err;
          }
        }
        return originalSetItem.call(this, key, val);
      };

      const gcSpy = vi.spyOn(AppState, '_gcFlashcards').mockImplementation((persist) => {
        order.push('step3_gc_flashcards');
        return AppState._gcFlashcards.call(AppState, persist);
      });

      try {
        const ok = SafeStorage.setItem('it_progresso', { nivel: 3 });
        expect(ok).toBe(true);

        // Verify exact execution ordering: Step 1 (SWR) -> Step 2 (Logs) -> Step 3 (GC)
        expect(order).toEqual([
          'evict_swr:it_swr_dialogi',
          'evict_log:it_client_errors',
          'step3_gc_flashcards'
        ]);
      } finally {
        Storage.prototype.setItem = originalSetItem;
        Storage.prototype.removeItem = originalRemoveItem;
        gcSpy.mockRestore();
      }
    });

    it('2.3: ADVERSARIAL FINDING: Step 2 does NOT count bytes freed from staging keys', () => {
      // If only it_stage_* or it_import_stage_* keys exist without it_client_errors:
      // bytesFreedStep2 remains 0 and Step 2 never attempts target key write!
      const originalSetItem = Storage.prototype.setItem;
      localStorage.setItem('it_stage_backup', '5MB of staging data');

      let targetAttempts = 0;
      Storage.prototype.setItem = function(key, val) {
        if (key === 'it_progresso') {
          targetAttempts++;
          // Fails on attempt 1
          if (targetAttempts === 1) {
            throw new DOMException('QuotaExceededError', 'QuotaExceededError');
          }
        }
        return originalSetItem.call(this, key, val);
      };

      try {
        // SafeStorage will delete it_stage_backup in Step 2, but bytesFreedStep2 is 0.
        // So it will skip write retry and move straight to Step 3.
        SafeStorage.setItem('it_progresso', { nivel: 1 });
        // Key was removed:
        expect(localStorage.getItem('it_stage_backup')).toBeNull();
      } finally {
        Storage.prototype.setItem = originalSetItem;
      }
    });
  });

  // ============================================================
  // REQUIREMENT 3: _gcFlashcards Persists to localStorage & Byte Reduction
  // ============================================================
  describe('Req 3: _gcFlashcards Persistence and Disk Byte Reduction', () => {
    it('3.1: _gcFlashcards(true) must prune cards and persist reduced JSON to localStorage', () => {
      const now = Date.now();
      const oneHundredDaysAgo = now - (100 * 24 * 3600 * 1000);

      const deck = {
        c_active: {
          id: 'c_active',
          state: 'review',
          lastReview: now - 3600000,
          difficulty: 5,
          stability: 2,
          history: [{ t: now, r: 1 }]
        },
        c_suspended: {
          id: 'c_suspended',
          state: 'suspended',
          lastReview: now,
          difficulty: 7,
          history: [{ t: now, r: 0 }]
        },
        c_obsolete: {
          id: 'c_obsolete',
          state: 'review',
          lastReview: oneHundredDaysAgo,
          difficulty: 6,
          history: [{ t: oneHundredDaysAgo, r: 1 }]
        },
        c_long_history: {
          id: 'c_long_history',
          state: 'review',
          lastReview: now - 86400000,
          difficulty: 5,
          history: Array.from({ length: 25 }, (_, i) => ({ t: now - i * 1000, r: i % 4 }))
        }
      };

      const initialPayload = JSON.stringify(deck);
      const initialBytes = initialPayload.length;
      localStorage.setItem('it_flashcards', initialPayload);

      AppState.estado.flashcardData = JSON.parse(initialPayload);

      const removedCount = AppState._gcFlashcards(true);

      // c_suspended and c_obsolete should be removed (2 cards)
      expect(removedCount).toBe(2);

      // Verify localStorage was updated
      const storedPayloadAfter = localStorage.getItem('it_flashcards');
      expect(storedPayloadAfter).not.toBeNull();
      const parsedStored = JSON.parse(storedPayloadAfter);

      // Check card presence
      expect(parsedStored['c_active']).toBeDefined();
      expect(parsedStored['c_suspended']).toBeUndefined();
      expect(parsedStored['c_obsolete']).toBeUndefined();
      expect(parsedStored['c_long_history']).toBeDefined();

      // Check history truncation to 5 entries
      expect(parsedStored['c_long_history'].history.length).toBe(5);

      // Check disk byte reduction
      const bytesAfter = storedPayloadAfter.length;
      expect(bytesAfter).toBeLessThan(initialBytes);
      const freedBytes = initialBytes - bytesAfter;
      expect(freedBytes).toBeGreaterThan(100);
    });

    it('3.2: _gcFlashcards(false) must modify memory but NOT persist to localStorage', () => {
      const deck = {
        c_suspended: { id: 'c_suspended', state: 'suspended' }
      };
      const initialPayload = JSON.stringify(deck);
      localStorage.setItem('it_flashcards', initialPayload);
      AppState.estado.flashcardData = JSON.parse(initialPayload);

      const removed = AppState._gcFlashcards(false);
      expect(removed).toBe(1);

      // Memory was pruned
      expect(AppState.estado.flashcardData['c_suspended']).toBeUndefined();

      // localStorage was NOT updated because persistir === false
      expect(localStorage.getItem('it_flashcards')).toBe(initialPayload);
    });

    it('3.3: EMPIRICAL STRESS / DEFECT PROBE: History truncation only when removidos === 0', () => {
      // If no cards are suspended and none > 90 days, but history is truncated on cards:
      // Does _gcFlashcards return > 0 or 0?
      const now = Date.now();
      const deck = {
        card_with_huge_history: {
          id: 'card_with_huge_history',
          state: 'review',
          lastReview: now,
          history: Array.from({ length: 50 }, (_, i) => ({ t: now - i * 1000, rating: i % 4 }))
        }
      };
      const payloadBefore = JSON.stringify(deck);
      localStorage.setItem('it_flashcards', payloadBefore);
      AppState.estado.flashcardData = JSON.parse(payloadBefore);

      const result = AppState._gcFlashcards(true);
      const payloadAfter = localStorage.getItem('it_flashcards');

      // Byte reduction DID occur on disk
      expect(payloadAfter.length).toBeLessThan(payloadBefore.length);
      expect(JSON.parse(payloadAfter).card_with_huge_history.history.length).toBe(5);

      // In state.js line 695: `return removidos;`
      // Since no cards were deleted (only truncated), `removidos` is 0!
      // This causes SafeStorage registered handler `freed > 0` to be false,
      // which means SafeStorage does not retry write when ONLY history truncation occurred!
      expect(result).toBe(0);
    });
  });

  // ============================================================
  // REQUIREMENT 4: Corrupted Data Injection Resilience
  // ============================================================
  describe('Req 4: Injected Corrupted Payloads Do Not Crash', () => {
    const maliciousProgressoPayloads = [
      { desc: 'malformed JSON syntax', val: '{ corrupted: true, "test" ' },
      { desc: 'null literal', val: 'null' },
      { desc: 'undefined literal', val: 'undefined' },
      { desc: 'empty string', val: '' },
      { desc: 'number primitive', val: '12345' },
      { desc: 'negative number', val: '-999' },
      { desc: 'float primitive', val: '3.14159' },
      { desc: 'boolean true', val: 'true' },
      { desc: 'boolean false', val: 'false' },
      { desc: 'raw string', val: '"im-a-string"' },
      { desc: 'empty array', val: '[]' },
      { desc: 'array with objects', val: '[{"nivel": 10}]' },
      { desc: 'empty object', val: '{}' },
      { desc: 'corrupted schema types (strings instead of numbers)', val: JSON.stringify({
          nivel: 'master',
          xp: 'infinity',
          xp_proximo_nivel: -50,
          streak: 'invalid',
          audio_rate: 999.9,
          templos_desbloqueados: 'all'
        })
      },
      { desc: 'extreme out-of-bounds values', val: JSON.stringify({
          nivel: -10,
          xp: -5000,
          audio_rate: 0.001,
          streak: -100,
          templos_desbloqueados: []
        })
      },
      { desc: 'prototype pollution attempt', val: '{"__proto__": {"polluted": true}}' }
    ];

    maliciousProgressoPayloads.forEach(({ desc, val }) => {
      it(`4.1: carregarProgresso() must not crash with ${desc}`, () => {
        localStorage.setItem('it_progresso', val);

        let prog;
        expect(() => {
          prog = AppState.carregarProgresso();
        }).not.toThrow();

        expect(prog).toBeDefined();
        expect(typeof prog).toBe('object');
        expect(prog).not.toBeNull();
        expect(Array.isArray(prog)).toBe(false);

        // Verify schema guarantees
        expect(prog.nivel).toBeGreaterThanOrEqual(1);
        expect(prog.xp).toBeGreaterThanOrEqual(0);
        expect(Array.isArray(prog.templos_desbloqueados)).toBe(true);
        expect(prog.templos_desbloqueados).toContain(1);
        expect(prog.audio_rate).toBeGreaterThanOrEqual(0.5);
        expect(prog.audio_rate).toBeLessThanOrEqual(2.0);
        expect(Array.isArray(prog.favoritos)).toBe(true);
        expect(Array.isArray(prog.conquistas)).toBe(true);
      });
    });

    const maliciousFlashcardPayloads = [
      { desc: 'malformed JSON syntax', val: '{ bad json :::: ' },
      { desc: 'null literal', val: 'null' },
      { desc: 'undefined literal', val: 'undefined' },
      { desc: 'empty string', val: '' },
      { desc: 'number primitive', val: '42' },
      { desc: 'boolean primitive', val: 'true' },
      { desc: 'raw string', val: '"a raw string"' },
      { desc: 'empty array', val: '[]' },
      { desc: 'array of cards', val: '[{"id": "c1", "front": "test"}]' },
      { desc: 'object with corrupted cards', val: JSON.stringify({
          c1: null,
          c2: 'not an object',
          c3: 12345,
          c4: [],
          c5: {
            state: 'invalido',
            difficulty: 9999,
            stability: -50,
            retrievability: 2.5,
            interval: -10,
            reps: -5,
            lapses: 'three'
          }
        })
      }
    ];

    maliciousFlashcardPayloads.forEach(({ desc, val }) => {
      it(`4.2: carregarFlashcards() must not crash with ${desc}`, () => {
        localStorage.setItem('it_flashcards', val);

        let deck;
        expect(() => {
          deck = AppState.carregarFlashcards();
        }).not.toThrow();

        expect(deck).toBeDefined();
        expect(typeof deck).toBe('object');
        expect(deck).not.toBeNull();
        expect(Array.isArray(deck)).toBe(false);

        // Non-object card entries must be stripped
        expect(deck['c1']).toBeUndefined();
        expect(deck['c2']).toBeUndefined();
        expect(deck['c3']).toBeUndefined();
        expect(deck['c4']).toBeUndefined();

        // Valid card entries with corrupted parameters must be clamped
        if (deck['c5']) {
          expect(deck['c5'].state).toBe('new'); // defaulted from invalid
          expect(deck['c5'].difficulty).toBeLessThanOrEqual(10);
          expect(deck['c5'].difficulty).toBeGreaterThanOrEqual(1);
          expect(deck['c5'].stability).toBeGreaterThanOrEqual(0.1);
          expect(deck['c5'].stability).toBeLessThanOrEqual(36500);
          expect(deck['c5'].retrievability).toBeLessThanOrEqual(1.0);
          expect(deck['c5'].retrievability).toBeGreaterThanOrEqual(0);
          expect(deck['c5'].interval).toBeGreaterThanOrEqual(0);
          expect(deck['c5'].reps).toBeGreaterThanOrEqual(0);
          expect(deck['c5'].lapses).toBeGreaterThanOrEqual(0);
        }
      });
    });

    it('4.3: SafeStorage.getItem() returns fallback safely when parsing broken JSON', () => {
      localStorage.setItem('corrupt_key', '{ bad: "json" ...');
      const fallback = { fallback: true };
      const val = SafeStorage.getItem('corrupt_key', fallback);
      // SafeStorage falls back to raw string if it cannot JSON.parse
      expect(typeof val).toBe('string');
      expect(val).toBe('{ bad: "json" ...');
    });

    it('4.4: SafeStorage memory fallback activates when localStorage is unavailable', () => {
      SafeStorage._isAvailable = false;
      const key = 'offline_key';
      const val = { saved: 123 };

      expect(SafeStorage.setItem(key, val)).toBe(true);
      expect(SafeStorage.getItem(key)).toEqual(val);
      expect(SafeStorage.keys()).toContain(key);
      SafeStorage.removeItem(key);
      expect(SafeStorage.getItem(key)).toBeNull();
    });
  });

  // ============================================================
  // REQUIREMENT 5: State Reconciliation (CRDT) Under Corrupted Data
  // ============================================================
  describe('Req 5: AppState.reconciliarProgresso & reconciliarFlashcards Under Anomalies', () => {
    it('5.1: reconciliarProgresso handles null/undefined/corrupted inputs gracefully', () => {
      expect(() => {
        AppState.reconciliarProgresso(null, null);
        AppState.reconciliarProgresso(null, { xp: 100 });
        AppState.reconciliarProgresso({ xp: 100 }, null);
        AppState.reconciliarProgresso('corrupted', 123);
        AppState.reconciliarProgresso({ nivel: 'abc', xp: null }, { nivel: 5, xp: 200 });
      }).not.toThrow();
    });

    it('5.2: reconciliarFlashcards handles primitives, nulls, and arrays without crashing', () => {
      expect(() => {
        AppState.reconciliarFlashcards(null, null);
        AppState.reconciliarFlashcards([], 'broken');
        AppState.reconciliarFlashcards({ c1: { reps: 5 } }, null);
        AppState.reconciliarFlashcards(null, { c2: { reps: 3 } });
        AppState.reconciliarFlashcards({ c1: null }, { c1: { reps: 2 } });
      }).not.toThrow();
    });
  });
});
