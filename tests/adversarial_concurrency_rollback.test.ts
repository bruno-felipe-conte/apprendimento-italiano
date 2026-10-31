// @ts-nocheck
// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import AppState from '../js/core/state.js';
import SafeStorage from '../js/core/storage.js';
import Profilo from '../js/profilo.js';
import { SyncManager, MockBackendAdapter } from '../js/core/sync';
import type { SyncBatchResult } from '../types/app';

describe('Adversarial & Empirical Verification: Multi-Tab Concurrency & Atomic Backup Rollback', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    vi.restoreAllMocks();

    // Setup global facades needed for Profilo and AppState
    globalThis.I18n = {
      t: (key: string) => key,
      idioma: 'pt'
    } as any;

    globalThis.App = {
      notificar: vi.fn(),
      pronunciar: vi.fn(),
      estado: AppState.estado
    } as any;

    globalThis.SafeStorage = SafeStorage;
    globalThis.AppState = AppState;
    globalThis.Profilo = Profilo;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // =========================================================================
  // 1. Simultaneous Progress Updates Across Simulated Tabs (CRDT Reconciliation)
  // =========================================================================
  describe('1. Simultaneous Progress Updates Across Simulated Tabs (CRDT)', () => {
    it('1.1: Commutativity - reconciliarProgresso(A, B) === reconciliarProgresso(B, A)', () => {
      const stateA = {
        nivel: 3,
        xp: 1450,
        xp_proximo_nivel: 2000,
        templos_desbloqueados: [1, 2, 3, 5],
        templos_concluidos: [1, 2],
        total_palavras: 65,
        streak: 7,
        streak_recorde: 12,
        ultimo_estudo: 1700000000000,
        grammatica_completadas: ['g1', 'g2'],
        meta_diaria: 100,
        xp_hoje: 150,
        data_xp_hoje: '2026-10-30',
        favoritos: ['fav_1', 'fav_2'],
        conquistas: ['conq_a'],
        data_inicio: 1690000000000,
        audio_rate: 0.85
      };

      const stateB = {
        nivel: 4,
        xp: 2100,
        xp_proximo_nivel: 3000,
        templos_desbloqueados: [1, 2, 4, 6],
        templos_concluidos: [1, 4],
        total_palavras: 80,
        streak: 9,
        streak_recorde: 15,
        ultimo_estudo: 1700050000000,
        grammatica_completadas: ['g2', 'g3'],
        meta_diaria: 120,
        xp_hoje: 200,
        data_xp_hoje: '2026-10-31',
        favoritos: ['fav_2', 'fav_3'],
        conquistas: ['conq_b'],
        data_inicio: 1680000000000,
        audio_rate: 0.90
      };

      const resAB = AppState.reconciliarProgresso(stateA, stateB);
      const resBA = AppState.reconciliarProgresso(stateB, stateA);

      expect(resAB.nivel).toBe(4);
      expect(resBA.nivel).toBe(4);

      expect(resAB.xp).toBe(2100);
      expect(resBA.xp).toBe(2100);

      // Temple unions must match and preserve all temples without LWW clobbering
      expect(resAB.templos_desbloqueados).toEqual([1, 2, 3, 4, 5, 6]);
      expect(resBA.templos_desbloqueados).toEqual([1, 2, 3, 4, 5, 6]);

      expect(resAB.templos_concluidos).toEqual([1, 2, 4]);
      expect(resBA.templos_concluidos).toEqual([1, 2, 4]);

      // Set unions for string collections
      expect(resAB.grammatica_completadas.sort()).toEqual(['g1', 'g2', 'g3']);
      expect(resBA.grammatica_completadas.sort()).toEqual(['g1', 'g2', 'g3']);

      expect(resAB.favoritos.sort()).toEqual(['fav_1', 'fav_2', 'fav_3']);
      expect(resBA.favoritos.sort()).toEqual(['fav_1', 'fav_2', 'fav_3']);

      expect(resAB.conquistas.sort()).toEqual(['conq_a', 'conq_b']);
      expect(resBA.conquistas.sort()).toEqual(['conq_a', 'conq_b']);

      expect(resAB.total_palavras).toBe(80);
      expect(resBA.total_palavras).toBe(80);

      expect(resAB.streak_recorde).toBe(15);
      expect(resBA.streak_recorde).toBe(15);

      expect(resAB.data_inicio).toBe(1680000000000);
      expect(resBA.data_inicio).toBe(1680000000000);
    });

    it('1.2: Idempotence - reconciliarProgresso(A, A) leaves state consistent', () => {
      const state = {
        nivel: 2,
        xp: 750,
        xp_proximo_nivel: 1000,
        templos_desbloqueados: [1, 2, 3],
        templos_concluidos: [1],
        total_palavras: 30,
        streak: 4,
        streak_recorde: 5,
        ultimo_estudo: 1700000000000,
        grammatica_completadas: ['g1'],
        meta_diaria: 100,
        xp_hoje: 50,
        data_xp_hoje: '2026-10-31',
        favoritos: ['w1'],
        conquistas: ['c1'],
        data_inicio: 1690000000000,
        audio_rate: 0.85
      };

      const result = AppState.reconciliarProgresso(state, state);
      expect(result.xp).toBe(750);
      expect(result.nivel).toBe(2);
      expect(result.templos_desbloqueados).toEqual([1, 2, 3]);
      expect(result.templos_concluidos).toEqual([1]);
      expect(result.streak).toBe(4);
    });

    it('1.3: Temple Unlocking & Progress without LWW clobbering', () => {
      // Tab 1 unlocked temple 5 while working offline or concurrently
      const tab1State = {
        nivel: 2,
        xp: 900,
        templos_desbloqueados: [1, 2, 5],
        templos_concluidos: [1]
      };

      // Tab 2 unlocked temple 6 and completed temple 2
      const tab2State = {
        nivel: 3,
        xp: 1100,
        templos_desbloqueados: [1, 2, 6],
        templos_concluidos: [1, 2]
      };

      const merged = AppState.reconciliarProgresso(tab1State, tab2State);

      // If LWW occurred, either temple 5 or temple 6 would have been dropped!
      expect(merged.templos_desbloqueados).toContain(1);
      expect(merged.templos_desbloqueados).toContain(2);
      expect(merged.templos_desbloqueados).toContain(5);
      expect(merged.templos_desbloqueados).toContain(6);
      expect(merged.templos_desbloqueados).toEqual([1, 2, 5, 6]);

      expect(merged.templos_concluidos).toEqual([1, 2]);
      expect(merged.xp).toBe(1100);
      expect(merged.nivel).toBe(3);
    });

    it('1.4: Resilient handling of malformed or null remote state (Fuzzing protection)', () => {
      const validLocal = {
        nivel: 2,
        xp: 500,
        xp_proximo_nivel: 1000,
        templos_desbloqueados: [1, 2],
        templos_concluidos: [1],
        total_palavras: 25,
        streak: 3
      };

      // Remote is null
      const resNull = AppState.reconciliarProgresso(validLocal, null);
      expect(resNull.xp).toBe(500);
      expect(resNull.templos_desbloqueados).toEqual([1, 2]);

      // Remote is undefined
      const resUndef = AppState.reconciliarProgresso(undefined, validLocal);
      expect(resUndef.xp).toBe(500);

      // Remote has string XP and corrupted temple types
      const corruptedRemote = {
        nivel: '5',
        xp: '1200',
        templos_desbloqueados: [1, 'corrupted', null, 3, NaN, undefined, 4],
        templos_concluidos: 'not-an-array',
        streak: '8'
      };

      const resCorrupted = AppState.reconciliarProgresso(validLocal, corruptedRemote);
      expect(resCorrupted.nivel).toBe(5);
      expect(resCorrupted.xp).toBe(1200);
      expect(resCorrupted.streak).toBe(8);
      // Clean numeric filter must have pruned strings, NaN, and nulls
      expect(resCorrupted.templos_desbloqueados).toEqual([1, 2, 3, 4]);
      expect(Array.isArray(resCorrupted.templos_concluidos)).toBe(true);
    });

    it('1.5: Simulated cross-tab broadcast synchronization without ping-pong loops', () => {
      // Mock BroadcastChannel
      let postMessageSpy = vi.fn();
      let onmessageHandler: ((ev: any) => void) | null = null;

      class MockBroadcastChannel {
        name: string;
        constructor(name: string) {
          this.name = name;
        }
        postMessage(data: any) {
          postMessageSpy(data);
          if (onmessageHandler && data.senderId !== AppState._getTabId()) {
            onmessageHandler({ data });
          }
        }
        set onmessage(handler: any) {
          onmessageHandler = handler;
        }
        get onmessage() {
          return onmessageHandler;
        }
        close() {}
      }

      globalThis.BroadcastChannel = MockBroadcastChannel as any;
      AppState._syncInitialized = false;
      AppState.initCrossTabSync();

      AppState.estado.progresso = {
        nivel: 2,
        xp: 400,
        templos_desbloqueados: [1, 2],
        templos_concluidos: []
      };

      // Tab B sends an update with higher XP and new unlocked temple 3
      const remotePayload = {
        nivel: 2,
        xp: 600,
        templos_desbloqueados: [1, 2, 3],
        templos_concluidos: [1]
      };

      postMessageSpy.mockClear();

      AppState._tratarMensagemSincronizacao({
        type: 'SYNC_UPDATE',
        key: 'it_progresso',
        senderId: 'remote_tab_999',
        timestamp: Date.now(),
        payload: remotePayload
      });

      // Local state was successfully merged
      expect(AppState.estado.progresso.xp).toBe(600);
      expect(AppState.estado.progresso.templos_desbloqueados).toEqual([1, 2, 3]);
      expect(AppState.estado.progresso.templos_concluidos).toEqual([1]);

      // If remote payload is already equal to merged result, it should NOT trigger infinite rebroadcast loop
      postMessageSpy.mockClear();
      AppState._tratarMensagemSincronizacao({
        type: 'SYNC_UPDATE',
        key: 'it_progresso',
        senderId: 'remote_tab_999',
        timestamp: Date.now(),
        payload: remotePayload
      });

      expect(postMessageSpy).not.toHaveBeenCalled();
    });
  });

  // =========================================================================
  // 2. Flashcard Review Merge (CRDT Flashcards)
  // =========================================================================
  describe('2. Flashcard Review Merge (CRDT)', () => {
    it('2.1: Non-overlapping cards are 100% preserved in both merge directions', () => {
      const deckA: Record<string, any> = {
        card_1: { state: 'review', lastReview: 1000, reps: 2, stability: 5.0 },
        card_2: { state: 'learning', lastReview: 1200, reps: 1, stability: 2.0 }
      };

      const deckB: Record<string, any> = {
        card_3: { state: 'review', lastReview: 1500, reps: 3, stability: 8.0 },
        card_4: { state: 'new', lastReview: null, reps: 0, stability: 1.0 }
      };

      const mergedAB = AppState.reconciliarFlashcards(deckA, deckB);
      const mergedBA = AppState.reconciliarFlashcards(deckB, deckA);

      expect(Object.keys(mergedAB).sort()).toEqual(['card_1', 'card_2', 'card_3', 'card_4']);
      expect(Object.keys(mergedBA).sort()).toEqual(['card_1', 'card_2', 'card_3', 'card_4']);

      expect(mergedAB.card_1.stability).toBe(5.0);
      expect(mergedAB.card_3.stability).toBe(8.0);
      expect(mergedBA.card_1.stability).toBe(5.0);
      expect(mergedBA.card_3.stability).toBe(8.0);
    });

    it('2.2: Newer lastReview timestamp wins regardless of merge order', () => {
      const deckLocal = {
        shared_card: {
          state: 'learning',
          lastReview: 5000,
          reps: 2,
          stability: 3.5,
          interval: 2
        }
      };

      const deckRemoto = {
        shared_card: {
          state: 'review',
          lastReview: 8500, // Newer timestamp
          reps: 5,
          stability: 14.2,
          interval: 12
        }
      };

      // Remote has newer timestamp -> Remote wins in local + remote
      const merged1 = AppState.reconciliarFlashcards(deckLocal, deckRemoto);
      expect(merged1.shared_card.lastReview).toBe(8500);
      expect(merged1.shared_card.state).toBe('review');
      expect(merged1.shared_card.stability).toBe(14.2);
      expect(merged1.shared_card.reps).toBe(5);

      // Inverted: Local has newer timestamp -> Local wins in remote + local
      const merged2 = AppState.reconciliarFlashcards(deckRemoto, deckLocal);
      expect(merged2.shared_card.lastReview).toBe(8500);
      expect(merged2.shared_card.state).toBe('review');
      expect(merged2.shared_card.stability).toBe(14.2);
    });

    it('2.3: Tie-breaker on equal timestamps selects the card with higher reps', () => {
      const timestamp = 1700000000000;

      const deckA = {
        card_tie: {
          state: 'review',
          lastReview: timestamp,
          reps: 3,
          stability: 8.0
        }
      };

      const deckB = {
        card_tie: {
          state: 'review',
          lastReview: timestamp,
          reps: 7, // Higher reps
          stability: 18.0
        }
      };

      const mergedAB = AppState.reconciliarFlashcards(deckA, deckB);
      expect(mergedAB.card_tie.reps).toBe(7);
      expect(mergedAB.card_tie.stability).toBe(18.0);

      const mergedBA = AppState.reconciliarFlashcards(deckB, deckA);
      expect(mergedBA.card_tie.reps).toBe(7);
      expect(mergedBA.card_tie.stability).toBe(18.0);
    });

    it('2.4: Legacy property support (last_review and repeticoes) resolves cleanly', () => {
      const deckCamel = {
        card_legacy: {
          lastReview: 12000,
          reps: 4
        }
      };

      const deckSnake = {
        card_legacy: {
          last_review: 15000, // Newer, snake_case
          repeticoes: 5
        }
      };

      const merged = AppState.reconciliarFlashcards(deckCamel, deckSnake);
      expect(merged.card_legacy.last_review).toBe(15000);
      expect(merged.card_legacy.repeticoes).toBe(5);
    });

    it('2.5: Resilient to null/undefined or corrupted deck structures', () => {
      expect(AppState.reconciliarFlashcards(null, undefined)).toEqual({});
      expect(AppState.reconciliarFlashcards({}, null)).toEqual({});
      expect(AppState.reconciliarFlashcards({ c1: { lastReview: 100 } }, 'corrupted-string' as any)).toEqual({
        c1: { lastReview: 100 }
      });
    });
  });

  // =========================================================================
  // 3. SyncManager Mutual-Exclusion Lease Lock (apprendimento_sync_lock)
  // =========================================================================
  describe('3. SyncManager Mutual-Exclusion Lease Lock (apprendimento_sync_lock)', () => {
    it('3.1: Concurrent flush in Tab 2 is blocked while Tab 1 holds active lease lock', async () => {
      const adapter1 = new MockBackendAdapter();
      const adapter2 = new MockBackendAdapter();

      const syncTab1 = new SyncManager(adapter1);
      const syncTab2 = new SyncManager(adapter2);
      syncTab1.salvarConfig({ autoSync: false });
      syncTab2.salvarConfig({ autoSync: false });

      // Force distinct tab IDs
      (syncTab1 as any).tabId = 'tab_1_active';
      (syncTab2 as any).tabId = 'tab_2_concurrent';

      // Both tabs enqueue items
      syncTab1.enfileirar('progress', 'update', 'p1', { xp: 100 });
      syncTab2.enfileirar('progress', 'update', 'p2', { xp: 200 });

      // Artificial delay on Tab 1's backend adapter to simulate async in-flight flush
      let resolveAdapter1: (value: SyncBatchResult) => void;
      const delayedPromise = new Promise<SyncBatchResult>((resolve) => {
        resolveAdapter1 = resolve;
      });
      vi.spyOn(adapter1, 'syncBatch').mockReturnValue(delayedPromise);
      const adapter2Spy = vi.spyOn(adapter2, 'syncBatch');

      // Tab 1 initiates flush
      const flushTab1Promise = syncTab1.flush();

      // Verify Tab 1 acquired the lock in localStorage
      const rawLock = localStorage.getItem('apprendimento_sync_lock');
      expect(rawLock).not.toBeNull();
      const lockObj = JSON.parse(rawLock!);
      expect(lockObj.tabId).toBe('tab_1_active');
      expect(Date.now() - lockObj.timestamp).toBeLessThan(1000);

      // While Tab 1 is in-flight, Tab 2 attempts flush
      const resTab2 = await syncTab2.flush();

      // Tab 2 must be blocked!
      expect(resTab2.sucesso).toBe(true);
      expect(resTab2.processados.length).toBe(0);
      expect(adapter2Spy).not.toHaveBeenCalled();

      // Resolve Tab 1's network batch
      resolveAdapter1!({
        sucesso: true,
        processados: ['sync_p1'],
        falhas: []
      });

      await flushTab1Promise;

      // Tab 1 must have released its lock upon completion
      expect(localStorage.getItem('apprendimento_sync_lock')).toBeNull();

      // Now Tab 2 can flush successfully!
      const resTab2After = await syncTab2.flush();
      expect(resTab2After.sucesso).toBe(true);
      expect(adapter2Spy).toHaveBeenCalledTimes(1);
    });

    it('3.2: Stale lease expiration (>15s) allows a new tab to override crashed tab lock', async () => {
      const adapter = new MockBackendAdapter();
      const syncManager = new SyncManager(adapter);
      syncManager.salvarConfig({ autoSync: false });
      (syncManager as any).tabId = 'tab_active_alive';

      syncManager.enfileirar('progress', 'update', 'p1', { xp: 300 });

      // Place a stale lock in localStorage from a dead/crashed tab from 25 seconds ago
      const staleTimestamp = Date.now() - 25000;
      localStorage.setItem('apprendimento_sync_lock', JSON.stringify({
        tabId: 'tab_dead_crashed',
        timestamp: staleTimestamp
      }));

      // Active tab flushes
      const adapterSpy = vi.spyOn(adapter, 'syncBatch');
      const res = await syncManager.flush();

      expect(res.sucesso).toBe(true);
      expect(adapterSpy).toHaveBeenCalledTimes(1);

      // Lock should have been acquired by tab_active_alive and then cleanly released
      expect(localStorage.getItem('apprendimento_sync_lock')).toBeNull();
    });

    it('3.3: Active lease (<15s) from another tab cannot be hijacked', async () => {
      const adapter = new MockBackendAdapter();
      const syncManager = new SyncManager(adapter);
      syncManager.salvarConfig({ autoSync: false });
      (syncManager as any).tabId = 'tab_intruder';

      syncManager.enfileirar('progress', 'update', 'p1', { xp: 400 });

      // Active lock from peer tab created 5 seconds ago
      const recentTimestamp = Date.now() - 5000;
      localStorage.setItem('apprendimento_sync_lock', JSON.stringify({
        tabId: 'tab_peer_owner',
        timestamp: recentTimestamp
      }));

      const adapterSpy = vi.spyOn(adapter, 'syncBatch');
      const res = await syncManager.flush();

      // Blocked!
      expect(res.sucesso).toBe(true);
      expect(res.processados.length).toBe(0);
      expect(adapterSpy).not.toHaveBeenCalled();

      // The original lock must still belong to tab_peer_owner!
      const lock = JSON.parse(localStorage.getItem('apprendimento_sync_lock')!);
      expect(lock.tabId).toBe('tab_peer_owner');
    });

    it('3.4: Lock release isolation - Tab 2 never deletes Tab 1 lock on teardown', () => {
      const syncManager = new SyncManager(new MockBackendAdapter());
      (syncManager as any).tabId = 'tab_intruder';

      localStorage.setItem('apprendimento_sync_lock', JSON.stringify({
        tabId: 'tab_legitimate_owner',
        timestamp: Date.now()
      }));

      // Call private liberarLockFlush
      (syncManager as any).liberarLockFlush();

      // Lock must remain intact because tabId did not match
      const lock = JSON.parse(localStorage.getItem('apprendimento_sync_lock')!);
      expect(lock.tabId).toBe('tab_legitimate_owner');
    });
  });

  // =========================================================================
  // 4. Atomic Backup Import Failure & Rollback
  // =========================================================================
  describe('4. Atomic Backup Import Failure & Rollback', () => {
    it('4.1: Pre-flight schema validation throws and halts before storage is touched', () => {
      const invalidPayloads = [
        null,
        'not a json object',
        [],
        { versao: 0, progresso: { nivel: 1, xp: 0, templos_desbloqueados: [1] } },
        { versao: 4, progresso: null },
        { versao: 4, progresso: { nivel: -1, xp: 0, templos_desbloqueados: [1] } },
        { versao: 4, progresso: { nivel: 1, xp: -50, templos_desbloqueados: [1] } },
        { versao: 4, progresso: { nivel: 1, xp: 100, templos_desbloqueados: [] } },
        { versao: 4, progresso: { nivel: 1, xp: 100, templos_desbloqueados: [1] }, quiz_historico: 'invalid-string' },
        { versao: 4, progresso: { nivel: 1, xp: 100, templos_desbloqueados: [1] }, storie_lidas: {} }
      ];

      for (const payload of invalidPayloads) {
        expect(() => Profilo._validarPayloadBackup(payload)).toThrow();
      }
    });

    it('4.2: Staging phase failure (QuotaExceededError) cleans staging keys and leaves original live data intact', async () => {
      // Set initial live state
      const initialProgresso = { nivel: 3, xp: 750, templos_desbloqueados: [1, 2, 3] };
      const initialFlashcards = { fc_orig: { state: 'review', lastReview: 1000 } };
      localStorage.setItem('it_progresso', JSON.stringify(initialProgresso));
      localStorage.setItem('it_flashcards', JSON.stringify(initialFlashcards));
      localStorage.setItem('it_tema', 'dark');

      const validBackup = {
        versao: 4,
        progresso: { nivel: 5, xp: 2000, templos_desbloqueados: [1, 2, 3, 4, 5] },
        flashcards: { fc_new: { state: 'review', lastReview: 5000 } },
        tema: 'light'
      };

      // Mock confirm to accept import
      globalThis.confirm = () => true;

      // Mock localStorage.setItem to simulate QuotaExceededError during staging
      const realSetItem = localStorage.setItem.bind(localStorage);
      let stagingWriteAttempts = 0;

      const stagingSpy = vi.spyOn(localStorage, 'setItem').mockImplementation((key: string, val: string) => {
        if (key.startsWith('it_stage_')) {
          stagingWriteAttempts++;
          if (stagingWriteAttempts >= 2) {
            const quotaErr = new Error('Storage quota exceeded');
            quotaErr.name = 'QuotaExceededError';
            throw quotaErr;
          }
        }
        return realSetItem(key, val);
      });

      try {
        // Construct file input change event
        const blob = new Blob([JSON.stringify(validBackup)], { type: 'application/json' });
        const mockEvent = {
          target: {
            files: [blob],
            value: 'backup.json'
          }
        };

        // Invoke import and await async FileReader
        Profilo.importarDados(mockEvent);
        await new Promise(r => setTimeout(r, 60));

        // Verify that notification reported error
        expect(App.notificar).toHaveBeenCalledWith(
          expect.stringContaining('Falha no armazenamento durante preparação do backup'),
          'erro'
        );

        // Staging keys must be completely purged
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          expect(k?.startsWith('it_stage_')).toBe(false);
        }

        // Live state must remain 100% untouched
        expect(JSON.parse(localStorage.getItem('it_progresso')!)).toEqual(initialProgresso);
        expect(JSON.parse(localStorage.getItem('it_flashcards')!)).toEqual(initialFlashcards);
        expect(localStorage.getItem('it_tema')).toBe('dark');
      } finally {
        stagingSpy.mockRestore();
      }
    });

    it('4.3: Commit phase failure triggers complete transactional rollback to pre-import snapshot', async () => {
      // Set initial live state
      const initialProgresso = { nivel: 2, xp: 500, templos_desbloqueados: [1, 2] };
      const initialFlashcards = { fc_1: { state: 'review', lastReview: 2000 } };
      localStorage.setItem('it_progresso', JSON.stringify(initialProgresso));
      localStorage.setItem('it_flashcards', JSON.stringify(initialFlashcards));
      localStorage.setItem('it_tema', 'dark');
      localStorage.setItem('it_audio_speed', '0.85');

      const incomingBackup = {
        versao: 4,
        progresso: { nivel: 10, xp: 50000, templos_desbloqueados: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] },
        flashcards: { fc_imported: { state: 'review', lastReview: 90000 } },
        tema: 'light',
        audio_speed: '1.25'
      };

      globalThis.confirm = () => true;

      const realSetItem = localStorage.setItem.bind(localStorage);
      let officialKeysWritten = 0;

      // Allow staging writes to succeed, but fail on the 2nd official key commit
      const commitSpy = vi.spyOn(localStorage, 'setItem').mockImplementation((key: string, val: string) => {
        if (!key.startsWith('it_stage_') && key.startsWith('it_')) {
          officialKeysWritten++;
          // Fail after committing first key
          if (officialKeysWritten === 2) {
            const commitErr = new Error('Disk write I/O failure during commit');
            commitErr.name = 'QuotaExceededError';
            throw commitErr;
          }
        }
        return realSetItem(key, val);
      });

      try {
        const blob = new Blob([JSON.stringify(incomingBackup)], { type: 'application/json' });
        const mockEvent = {
          target: {
            files: [blob],
            value: 'backup.json'
          }
        };

        Profilo.importarDados(mockEvent);
        await new Promise(r => setTimeout(r, 60));

        // Verify that notification reported error
        expect(App.notificar).toHaveBeenCalledWith(
          expect.stringContaining('Estado anterior restaurado com sucesso'),
          'erro'
        );

        // Rollback must have restored all pre-import keys exactly
        expect(JSON.parse(localStorage.getItem('it_progresso')!)).toEqual(initialProgresso);
        expect(JSON.parse(localStorage.getItem('it_flashcards')!)).toEqual(initialFlashcards);
        expect(localStorage.getItem('it_tema')).toBe('dark');
        expect(localStorage.getItem('it_audio_speed')).toBe('0.85');

        // Staging keys must be completely removed
        for (let i = 0; i < localStorage.length; i++) {
          const k = localStorage.key(i);
          expect(k?.startsWith('it_stage_')).toBe(false);
        }
      } finally {
        commitSpy.mockRestore();
      }
    });

    it('4.4: Bookmark sanitization guards against prototype pollution and limits payload sizes', () => {
      const maliciousBookmarks = {
        '__proto__': 'malicious',
        'constructor': 'malicious',
        'it_book_bm_valid_1': 'page_42',
        'it_book_bm_valid_2': 105,
        'it_book_bm_invalid$char!': 'bad',
        'it_book_bm_oversized': 'x'.repeat(2048)
      };

      const clean = Profilo._sanitizarBookmarks(maliciousBookmarks);

      expect(Object.prototype.hasOwnProperty.call(clean, '__proto__')).toBe(false);
      expect(Object.prototype.hasOwnProperty.call(clean, 'constructor')).toBe(false);
      expect(Object.prototype.hasOwnProperty.call(clean, 'it_book_bm_invalid$char!')).toBe(false);

      expect(clean['it_book_bm_valid_1']).toBe('page_42');
      expect(clean['it_book_bm_valid_2']).toBe('105');
      // Truncated to 1024 chars
      expect(clean['it_book_bm_oversized'].length).toBe(1024);
    });
  });

  // =========================================================================
  // 5. High-Stress Mass Concurrency, Chaos Fuzzing & Eviction Ladder Stress
  // =========================================================================
  describe('5. High-Stress Mass Concurrency, Chaos Fuzzing & Eviction Ladder Stress', () => {
    it('5.1: 10 Simulated Tabs Race - 100 concurrent progress updates converge to complete union', () => {
      let accumulatedState = {
        nivel: 1,
        xp: 0,
        templos_desbloqueados: [1],
        templos_concluidos: [],
        total_palavras: 0,
        streak: 0,
        grammatica_completadas: [],
        favoritos: []
      };

      // Generate 100 random progress snapshots across 10 simulated tabs
      const tabSnapshots: any[] = [];
      const allUnlockedExpected = new Set<number>([1]);
      let maxXPExpected = 0;
      let maxNivelExpected = 1;
      let maxStreakExpected = 0;

      for (let i = 0; i < 100; i++) {
        const tabIndex = i % 10;
        const xp = (i + 1) * 35;
        const nivel = Math.floor(xp / 500) + 1;
        const streak = (i % 15) + 1;
        const randomTemple = ((i * 7) % 50) + 1;
        allUnlockedExpected.add(randomTemple);
        if (xp > maxXPExpected) maxXPExpected = xp;
        if (nivel > maxNivelExpected) maxNivelExpected = nivel;
        if (streak > maxStreakExpected) maxStreakExpected = streak;

        tabSnapshots.push({
          tabId: `tab_${tabIndex}`,
          snapshot: {
            nivel,
            xp,
            templos_desbloqueados: [1, randomTemple],
            templos_concluidos: randomTemple > 1 ? [1] : [],
            total_palavras: (i + 1) * 2,
            streak,
            grammatica_completadas: [`gram_${i % 8}`],
            favoritos: [`fav_${i % 12}`]
          }
        });
      }

      // Shuffle snapshots to simulate arbitrary concurrent network / storage delivery
      const shuffled = [...tabSnapshots].sort(() => Math.random() - 0.5);

      for (const item of shuffled) {
        accumulatedState = AppState.reconciliarProgresso(accumulatedState, item.snapshot);
      }

      expect(accumulatedState.xp).toBe(maxXPExpected);
      expect(accumulatedState.nivel).toBe(maxNivelExpected);
      expect(accumulatedState.streak).toBe(maxStreakExpected);
      expect(accumulatedState.templos_desbloqueados.sort((a: number, b: number) => a - b))
        .toEqual(Array.from(allUnlockedExpected).sort((a, b) => a - b));
      expect(accumulatedState.grammatica_completadas.length).toBe(8);
      expect(accumulatedState.favoritos.length).toBe(12);
    });

    it('5.2: 100 Flashcards Concurrent Review Stress - Latest timestamp guarantees correctness', () => {
      let mergedDeck: Record<string, any> = {};

      // 5 tabs reviewing 100 cards with varying timestamps
      const latestExpectedCard: Record<string, any> = {};

      for (let cardNum = 1; cardNum <= 100; cardNum++) {
        const cardId = `card_${cardNum}`;
        // Tab 1 reviewed card early
        const rev1 = {
          state: 'learning',
          lastReview: 10000 + cardNum,
          reps: 1,
          stability: 2.0
        };
        // Tab 2 reviewed card later
        const rev2 = {
          state: 'review',
          lastReview: 30000 + (cardNum % 2 === 0 ? 50000 : 0),
          reps: 3,
          stability: 8.5
        };
        // Tab 3 reviewed card even later or earlier depending on parity
        const rev3 = {
          state: 'review',
          lastReview: 20000 + (cardNum % 3 === 0 ? 80000 : 0),
          reps: 4,
          stability: 15.0
        };

        const candidates = [rev1, rev2, rev3];
        const winner = candidates.reduce((best, curr) => curr.lastReview > best.lastReview ? curr : best);
        latestExpectedCard[cardId] = winner;

        mergedDeck = AppState.reconciliarFlashcards(mergedDeck, { [cardId]: rev1 });
        mergedDeck = AppState.reconciliarFlashcards(mergedDeck, { [cardId]: rev2 });
        mergedDeck = AppState.reconciliarFlashcards(mergedDeck, { [cardId]: rev3 });
      }

      expect(Object.keys(mergedDeck).length).toBe(100);
      for (let cardNum = 1; cardNum <= 100; cardNum++) {
        const cardId = `card_${cardNum}`;
        expect(mergedDeck[cardId].lastReview).toBe(latestExpectedCard[cardId].lastReview);
        expect(mergedDeck[cardId].stability).toBe(latestExpectedCard[cardId].stability);
        expect(mergedDeck[cardId].reps).toBe(latestExpectedCard[cardId].reps);
      }
    });

    it('5.3: SafeStorage Eviction Priority Ladder recovers progressively under QuotaExceededError', () => {
      // Setup ephemeral caches
      localStorage.setItem('it_swr_grammar', JSON.stringify({ large: 'x'.repeat(5000) }));
      localStorage.setItem('it_swr_templos_meta', JSON.stringify({ large: 'y'.repeat(5000) }));
      localStorage.setItem('it_client_errors', JSON.stringify(['error1', 'error2']));
      localStorage.setItem('it_stage_dummy', 'transient');

      // Mock localStorage.setItem to simulate quota error until SWR caches are removed
      const realSetItem = localStorage.setItem.bind(localStorage);
      const ladderSpy = vi.spyOn(localStorage, 'setItem').mockImplementation((key: string, val: string) => {
        if (key === 'it_progresso_crucial') {
          // Check if SWR caches have been evicted by SafeStorage
          if (localStorage.getItem('it_swr_grammar') !== null) {
            const err = new Error('Quota exceeded on write');
            err.name = 'QuotaExceededError';
            throw err;
          }
        }
        return realSetItem(key, val);
      });

      try {
        const success = SafeStorage.setItem('it_progresso_crucial', { crucial: true });

        expect(success).toBe(true);
        // Verify Step 1 purged SWR caches
        expect(localStorage.getItem('it_swr_grammar')).toBeNull();
        expect(localStorage.getItem('it_swr_templos_meta')).toBeNull();
        // Crucial key was written successfully
        expect(SafeStorage.getItem('it_progresso_crucial')).toEqual({ crucial: true });
      } finally {
        ladderSpy.mockRestore();
      }
    });

    it('5.4: 10 Tabs concurrent lock acquisition contention - Exactly ONE tab acquires lease', () => {
      const managers: SyncManager[] = [];
      for (let i = 0; i < 10; i++) {
        const sm = new SyncManager(new MockBackendAdapter());
        (sm as any).tabId = `contender_tab_${i}`;
        managers.push(sm);
      }

      // All 10 attempt tentarAdquirirLockFlush at the exact same instant
      const results = managers.map(sm => (sm as any).tentarAdquirirLockFlush());

      const successes = results.filter(r => r === true);
      const failures = results.filter(r => r === false);

      expect(successes.length).toBe(1);
      expect(failures.length).toBe(9);

      const activeLock = JSON.parse(localStorage.getItem('apprendimento_sync_lock')!);
      expect(activeLock.tabId).toMatch(/^contender_tab_\d$/);
    });
  });
});

