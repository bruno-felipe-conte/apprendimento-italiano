// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  SyncManager,
  MockBackendAdapter,
  SupabaseAdapter,
  PocketBaseAdapter
} from '../js/core/sync';
import type { SyncItem } from '../types/app';

describe('EV-02: Backend Lite / Sync Queue Offline-First', () => {
  let mockAdapter: MockBackendAdapter;
  let syncManager: SyncManager;

  beforeEach(() => {
    localStorage.clear();
    mockAdapter = new MockBackendAdapter();
    syncManager = new SyncManager(mockAdapter);
    syncManager.salvarConfig({
      provider: 'mock',
      autoSync: false,
      userId: 'test-user-123'
    });
    syncManager.limparFila();
  });

  describe('Fila Offline e Persistência', () => {
    it('deve enfileirar itens corretamente e expor status com pendingCount', () => {
      const item = syncManager.enfileirar('progress', 'update', 'progresso_1', { xp: 150, nivel: 2 });
      
      expect(item).toBeDefined();
      expect(item.entity).toBe('progress');
      expect(item.entityId).toBe('progresso_1');
      expect(item.payload.xp).toBe(150);

      const status = syncManager.getStatus();
      expect(status.pendingCount).toBe(1);
      expect(status.userId).toBe('test-user-123');
    });

    it('deve deduplicar updates da mesma entidade aplicando Last-Write-Wins (LWW)', () => {
      syncManager.enfileirar('flashcards', 'update', 'deck_it', { total_cards: 10, reps: 5 });
      syncManager.enfileirar('flashcards', 'update', 'deck_it', { total_cards: 12, novos: 2 });

      const fila = syncManager.getFila();
      expect(fila.length).toBe(1);
      expect(fila[0].payload.total_cards).toBe(12);
      expect(fila[0].payload.reps).toBe(5);
      expect(fila[0].payload.novos).toBe(2);
    });

    it('deve descartar entidade se criada e depois deletada offline antes de sincronizar', () => {
      syncManager.enfileirar('custom_content', 'create', 'historia_nova_1', { titulo: 'La Bella Roma' });
      expect(syncManager.getFila().length).toBe(1);

      syncManager.enfileirar('custom_content', 'delete', 'historia_nova_1', {});
      expect(syncManager.getFila().length).toBe(0);
    });
  });

  describe('Flush e Sincronização', () => {
    it('deve esvaziar a fila e salvar dados no backend mock ao executar flush()', async () => {
      syncManager.enfileirar('progress', 'update', 'progresso_1', { xp: 200, nivel: 3 });
      syncManager.enfileirar('stories_read', 'create', 'storia_10', { tempo_segundos: 120 });

      expect(syncManager.getFila().length).toBe(2);

      const res = await syncManager.flush();

      expect(res.sucesso).toBe(true);
      expect(res.processados.length).toBe(2);
      expect(syncManager.getFila().length).toBe(0);

      const progressoSalvo = await mockAdapter.pullLatest('progress');
      expect(progressoSalvo.length).toBe(1);
      expect(progressoSalvo[0].xp).toBe(200);

      const status = syncManager.getStatus();
      expect(status.lastSyncSuccess).toBeGreaterThan(0);
      expect(status.lastSyncError).toBeNull();
    });

    it('não deve enviar itens se o navegador reportar que está offline', async () => {
      syncManager.enfileirar('quiz_history', 'create', 'quiz_1', { score: 100 });
      
      // Simula offline
      vi.spyOn(syncManager, 'isOnline').mockReturnValue(false);

      const res = await syncManager.flush();
      expect(res.sucesso).toBe(false);
      expect(syncManager.getFila().length).toBe(1);
      expect(res.falhas[0].erro).toBe('Dispositivo offline');
    });

    it('deve registrar tentativas e descartar após exceder MAX_ATTEMPTS em caso de erro persistente', async () => {
      mockAdapter.shouldFail = true;

      syncManager.enfileirar('progress', 'update', 'falha_1', { xp: 50 });

      // Executa flush repetidamente até atingir o limite
      for (let i = 0; i < 5; i++) {
        await syncManager.flush();
      }

      // O item deve ser descartado após atingir o limite de 5 tentativas
      expect(syncManager.getFila().length).toBe(0);
      expect(syncManager.getStatus().lastSyncError).toContain('Falha simulada');
    });
  });

  describe('Adaptadores REST', () => {
    it('SupabaseAdapter: deve formatar URLs, headers e payload REST PostgREST', async () => {
      const adapter = new SupabaseAdapter();
      adapter.init({
        provider: 'supabase',
        endpoint: 'https://xyz.supabase.co',
        apiKey: 'anon-key-123',
        authToken: 'jwt-token-456',
        userId: 'user-789'
      });

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        status: 201,
        text: async () => ''
      });
      globalThis.fetch = fetchMock;

      const item: SyncItem = {
        id: 'sync_1',
        entity: 'progress',
        action: 'update',
        entityId: 'user-789',
        payload: { xp: 300 },
        timestamp: Date.now(),
        attempts: 0
      };

      const res = await adapter.syncBatch([item]);
      expect(res.sucesso).toBe(true);
      expect(fetchMock).toHaveBeenCalledWith(
        'https://xyz.supabase.co/rest/v1/progress',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            apikey: 'anon-key-123',
            Authorization: 'Bearer jwt-token-456'
          })
        })
      );
    });

    it('PocketBaseAdapter: deve formatar URLs para collections e PATCH para atualizações', async () => {
      const adapter = new PocketBaseAdapter();
      adapter.init({
        provider: 'pocketbase',
        endpoint: 'https://pb.exemplo.com',
        authToken: 'pb-token-abc'
      });

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        text: async () => ''
      });
      globalThis.fetch = fetchMock;

      const item: SyncItem = {
        id: 'sync_2',
        entity: 'flashcards',
        action: 'update',
        entityId: 'rec_flash_99',
        payload: { reps: 8 },
        timestamp: Date.now(),
        attempts: 0
      };

      const res = await adapter.syncBatch([item]);
      expect(res.sucesso).toBe(true);
      expect(fetchMock).toHaveBeenCalledWith(
        'https://pb.exemplo.com/api/collections/flashcards/records/rec_flash_99',
        expect.objectContaining({
          method: 'PATCH',
          headers: expect.objectContaining({
            Authorization: 'pb-token-abc'
          })
        })
      );
    });
  });
});
