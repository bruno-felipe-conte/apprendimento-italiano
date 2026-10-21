/**
 * Módulo de Sincronização e Backend Lite (EV-02)
 * Arquitetura Offline-First com Fila Persistente e Adapters para Supabase e PocketBase.
 */

import type {
  SyncEntity,
  SyncAction,
  SyncItem,
  SyncBatchResult,
  SyncStatus,
  BackendConfig,
  IBackendAdapter
} from '../../types/app';

const STORAGE_QUEUE_KEY = 'apprendimento_sync_queue';
const STORAGE_CONFIG_KEY = 'apprendimento_backend_config';
const MAX_ATTEMPTS = 5;

// ==========================================
// ADAPTER MOCK (Para Testes e Modo Local)
// ==========================================
export class MockBackendAdapter implements IBackendAdapter {
  provider: 'mock' = 'mock';
  public memoryStore: Map<string, Map<string, any>> = new Map();
  public shouldFail: boolean = false;
  public networkDelayMs: number = 0;

  async init(_config: BackendConfig): Promise<void> {
    // Inicialização mock
  }

  async syncBatch(items: SyncItem[]): Promise<SyncBatchResult> {
    if (this.networkDelayMs > 0) {
      await new Promise((r) => setTimeout(r, this.networkDelayMs));
    }

    if (this.shouldFail) {
      return {
        sucesso: false,
        processados: [],
        falhas: items.map((i) => ({ id: i.id, erro: 'Falha simulada no MockAdapter' }))
      };
    }

    const processados: string[] = [];

    for (const item of items) {
      if (!this.memoryStore.has(item.entity)) {
        this.memoryStore.set(item.entity, new Map());
      }
      const table = this.memoryStore.get(item.entity)!;

      if (item.action === 'delete') {
        table.delete(item.entityId);
      } else {
        table.set(item.entityId, { ...item.payload, updated_at: item.timestamp });
      }
      processados.push(item.id);
    }

    return {
      sucesso: true,
      processados,
      falhas: []
    };
  }

  async pullLatest(entity: SyncEntity): Promise<any[]> {
    const table = this.memoryStore.get(entity);
    if (!table) return [];
    return Array.from(table.values());
  }
}

// ==========================================
// ADAPTER SUPABASE (REST / PostgREST)
// ==========================================
export class SupabaseAdapter implements IBackendAdapter {
  provider: 'supabase' = 'supabase';
  private config: BackendConfig = { provider: 'supabase', endpoint: '' };

  init(config: BackendConfig): void {
    this.config = config;
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Prefer': 'resolution=merge-duplicates,return=minimal'
    };
    if (this.config.apiKey) {
      headers['apikey'] = this.config.apiKey;
    }
    const token = this.config.authToken || this.config.apiKey;
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  async syncBatch(items: SyncItem[]): Promise<SyncBatchResult> {
    const processados: string[] = [];
    const falhas: { id: string; erro: string }[] = [];

    for (const item of items) {
      try {
        const url = `${this.config.endpoint.replace(/\/$/, '')}/rest/v1/${item.entity}`;
        const headers = this.getHeaders();
        let resp: Response;

        if (item.action === 'delete') {
          resp = await fetch(`${url}?id=eq.${encodeURIComponent(item.entityId)}`, {
            method: 'DELETE',
            headers
          });
        } else {
          // Upsert no PostgREST
          resp = await fetch(url, {
            method: 'POST',
            headers,
            body: JSON.stringify({
              id: item.entityId,
              ...item.payload,
              user_id: this.config.userId || item.payload.user_id,
              synced_at: new Date().toISOString()
            })
          });
        }

        if (resp.ok) {
          processados.push(item.id);
        } else {
          const errText = await resp.text();
          falhas.push({ id: item.id, erro: `HTTP ${resp.status}: ${errText}` });
        }
      } catch (err: any) {
        falhas.push({ id: item.id, erro: err.message || 'Erro de conexão com Supabase' });
      }
    }

    return {
      sucesso: falhas.length === 0,
      processados,
      falhas
    };
  }

  async authMagicLink(email: string): Promise<boolean> {
    try {
      const url = `${this.config.endpoint.replace(/\/$/, '')}/auth/v1/otp`;
      const resp = await fetch(url, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ email, create_user: true })
      });
      return resp.ok;
    } catch {
      return false;
    }
  }
}

// ==========================================
// ADAPTER POCKETBASE (REST)
// ==========================================
export class PocketBaseAdapter implements IBackendAdapter {
  provider: 'pocketbase' = 'pocketbase';
  private config: BackendConfig = { provider: 'pocketbase', endpoint: '' };

  init(config: BackendConfig): void {
    this.config = config;
  }

  private getHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };
    if (this.config.authToken) {
      headers['Authorization'] = this.config.authToken;
    }
    return headers;
  }

  async syncBatch(items: SyncItem[]): Promise<SyncBatchResult> {
    const processados: string[] = [];
    const falhas: { id: string; erro: string }[] = [];

    for (const item of items) {
      try {
        const base = `${this.config.endpoint.replace(/\/$/, '')}/api/collections/${item.entity}/records`;
        const headers = this.getHeaders();
        let resp: Response;

        if (item.action === 'delete') {
          resp = await fetch(`${base}/${encodeURIComponent(item.entityId)}`, {
            method: 'DELETE',
            headers
          });
        } else if (item.action === 'update') {
          resp = await fetch(`${base}/${encodeURIComponent(item.entityId)}`, {
            method: 'PATCH',
            headers,
            body: JSON.stringify(item.payload)
          });
        } else {
          // create
          resp = await fetch(base, {
            method: 'POST',
            headers,
            body: JSON.stringify({
              id: item.entityId,
              ...item.payload,
              user: this.config.userId || item.payload.user_id
            })
          });
        }

        if (resp.ok || resp.status === 404 && item.action === 'delete') {
          processados.push(item.id);
        } else {
          const errText = await resp.text();
          falhas.push({ id: item.id, erro: `HTTP ${resp.status}: ${errText}` });
        }
      } catch (err: any) {
        falhas.push({ id: item.id, erro: err.message || 'Erro de conexão com PocketBase' });
      }
    }

    return {
      sucesso: falhas.length === 0,
      processados,
      falhas
    };
  }

  async authWithPassword(email: string, pass: string): Promise<{ token: string; user: any }> {
    const url = `${this.config.endpoint.replace(/\/$/, '')}/api/collections/users/auth-with-password`;
    const resp = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identity: email, password: pass })
    });
    if (!resp.ok) {
      throw new Error(`Erro de autenticação PocketBase: HTTP ${resp.status}`);
    }
    const data = await resp.json();
    return { token: data.token, user: data.record };
  }
}

// ==========================================
// SYNC MANAGER (SINGLETON & FILA OFFLINE-FIRST)
// ==========================================
export class SyncManager {
  private queue: SyncItem[] = [];
  private adapter: IBackendAdapter;
  private config: BackendConfig;
  private isSyncing: boolean = false;
  private syncTimer: any = null;
  private statusListeners: Array<(status: SyncStatus) => void> = [];
  private lastSyncSuccess: number | null = null;
  private lastSyncError: string | null = null;

  constructor(adapter?: IBackendAdapter) {
    this.config = this.carregarConfig();
    this.adapter = adapter || this.criarAdapter(this.config.provider);
    this.carregarFila();
    this.configurarListenersOnline();

    if (this.config.autoSync) {
      this.iniciarSyncPeriodico();
    }
  }

  private carregarConfig(): BackendConfig {
    try {
      if (typeof localStorage !== 'undefined') {
        const raw = localStorage.getItem(STORAGE_CONFIG_KEY);
        if (raw) return JSON.parse(raw);
      }
    } catch (e) {
      console.warn('[SyncManager] Erro ao carregar config:', e);
    }
    return {
      provider: 'mock',
      endpoint: '',
      autoSync: true,
      syncIntervalMs: 30000
    };
  }

  public salvarConfig(novaConfig: Partial<BackendConfig>): void {
    this.config = { ...this.config, ...novaConfig };
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_CONFIG_KEY, JSON.stringify(this.config));
      }
    } catch (e) {
      console.warn('[SyncManager] Erro ao salvar config:', e);
    }

    if (novaConfig.provider && novaConfig.provider !== this.adapter.provider) {
      this.adapter = this.criarAdapter(this.config.provider);
      this.adapter.init(this.config);
    }

    if (this.config.autoSync) {
      this.iniciarSyncPeriodico();
    } else {
      this.pararSyncPeriodico();
    }

    this.notificarStatus();
  }

  public setAdapter(adapter: IBackendAdapter): void {
    this.adapter = adapter;
    this.adapter.init(this.config);
  }

  public getAdapter(): IBackendAdapter {
    return this.adapter;
  }

  private criarAdapter(provider: string): IBackendAdapter {
    switch (provider) {
      case 'supabase':
        return new SupabaseAdapter();
      case 'pocketbase':
        return new PocketBaseAdapter();
      default:
        return new MockBackendAdapter();
    }
  }

  private carregarFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        const raw = localStorage.getItem(STORAGE_QUEUE_KEY);
        if (raw) {
          this.queue = JSON.parse(raw);
        }
      }
    } catch (e) {
      console.warn('[SyncManager] Erro ao carregar fila:', e);
      this.queue = [];
    }
  }

  private persistirFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_QUEUE_KEY, JSON.stringify(this.queue));
      }
    } catch (e) {
      console.error('[SyncManager] Falha ao persistir fila no localStorage:', e);
    }
  }

  private configurarListenersOnline(): void {
    if (typeof window !== 'undefined') {
      window.addEventListener('online', () => {
        this.notificarStatus();
        this.flush();
      });
      window.addEventListener('offline', () => {
        this.notificarStatus();
      });

      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.addEventListener('message', (event) => {
          if (event.data?.type === 'EXECUTE_SYNC_QUEUE') {
            this.flush();
          }
        });
      }
    }
  }

  public iniciarSyncPeriodico(): void {
    this.pararSyncPeriodico();
    const interval = this.config.syncIntervalMs || 30000;
    this.syncTimer = setInterval(() => {
      if (this.queue.length > 0 && this.isOnline()) {
        this.flush();
      }
    }, interval);
  }

  public pararSyncPeriodico(): void {
    if (this.syncTimer) {
      clearInterval(this.syncTimer);
      this.syncTimer = null;
    }
  }

  public isOnline(): boolean {
    if (typeof navigator !== 'undefined' && typeof navigator.onLine === 'boolean') {
      return navigator.onLine;
    }
    return true;
  }

  /**
   * Enfileira uma ação de sincronização com deduplicação inteligente LWW (Last-Write-Wins).
   */
  public enfileirar(
    entity: SyncEntity,
    action: SyncAction,
    entityId: string,
    payload: Record<string, any>
  ): SyncItem {
    const timestamp = Date.now();
    const id = `sync_${timestamp}_${Math.random().toString(36).substring(2, 9)}`;

    // Deduplicação: verifica se já existe uma operação pendente para a mesma entidade
    const existingIndex = this.queue.findIndex(
      (item) => item.entity === entity && item.entityId === entityId
    );

    let item: SyncItem;

    if (existingIndex >= 0) {
      const existing = this.queue[existingIndex];

      if (action === 'delete') {
        if (existing.action === 'create') {
          // Se foi criado localmente e deletado antes de sincronizar, remove ambos
          this.queue.splice(existingIndex, 1);
          this.persistirFila();
          this.notificarStatus();
          return existing;
        }
        // Sobrescreve para delete
        existing.action = 'delete';
        existing.payload = {};
        existing.timestamp = timestamp;
        item = existing;
      } else {
        // LWW: mescla o payload mais recente
        existing.payload = { ...existing.payload, ...payload };
        existing.timestamp = timestamp;
        item = existing;
      }
    } else {
      item = {
        id,
        entity,
        action,
        entityId,
        payload,
        timestamp,
        attempts: 0
      };
      this.queue.push(item);
    }

    this.persistirFila();
    this.notificarStatus();

    // Se estiver online e com autoSync, dispara sincronização
    if (this.isOnline() && this.config.autoSync) {
      this.flush();
    } else if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator && typeof window !== 'undefined' && 'SyncManager' in window) {
      navigator.serviceWorker.ready.then((reg: any) => {
        if (reg?.sync?.register) {
          reg.sync.register('app-sync-queue').catch(() => {});
        }
      }).catch(() => {});
    }

    return item;
  }

  /**
   * Esvazia e processa a fila de sincronização enviando as operações pendentes.
   */
  public async flush(): Promise<SyncBatchResult> {
    if (this.isSyncing || this.queue.length === 0) {
      return { sucesso: true, processados: [], falhas: [] };
    }

    if (!this.isOnline()) {
      return {
        sucesso: false,
        processados: [],
        falhas: [{ id: 'network', erro: 'Dispositivo offline' }]
      };
    }

    this.isSyncing = true;
    this.notificarStatus();

    try {
      // Pega os primeiros 25 itens da fila para processar em lote
      const batch = this.queue.slice(0, 25);
      const resultado = await this.adapter.syncBatch(batch);

      if (resultado.processados.length > 0) {
        const setSucesso = new Set(resultado.processados);
        this.queue = this.queue.filter((item) => !setSucesso.has(item.id));
        this.lastSyncSuccess = Date.now();
        this.lastSyncError = null;
      }

      if (resultado.falhas.length > 0) {
        const mapaFalhas = new Map(resultado.falhas.map((f) => [f.id, f.erro]));
        for (const item of this.queue) {
          if (mapaFalhas.has(item.id)) {
            item.attempts += 1;
            item.lastAttempt = Date.now();
            item.lastError = mapaFalhas.get(item.id);
          }
        }

        // Remove itens que excederam o limite máximo de tentativas
        const descartados = this.queue.filter((i) => i.attempts >= MAX_ATTEMPTS);
        if (descartados.length > 0) {
          console.warn('[SyncManager] Itens descartados por exceder tentativas:', descartados);
          this.queue = this.queue.filter((i) => i.attempts < MAX_ATTEMPTS);
        }

        this.lastSyncError = resultado.falhas[0].erro;
      }

      this.persistirFila();
      return resultado;
    } catch (err: any) {
      const erroMsg = err.message || 'Falha durante o flush de sincronização';
      this.lastSyncError = erroMsg;
      return {
        sucesso: false,
        processados: [],
        falhas: [{ id: 'exception', erro: erroMsg }]
      };
    } finally {
      this.isSyncing = false;
      this.notificarStatus();
    }
  }

  /**
   * Limpa todos os itens da fila local.
   */
  public limparFila(): void {
    this.queue = [];
    this.persistirFila();
    this.notificarStatus();
  }

  public getFila(): readonly SyncItem[] {
    return [...this.queue];
  }

  public getStatus(): SyncStatus {
    return {
      isOnline: this.isOnline(),
      isSyncing: this.isSyncing,
      pendingCount: this.queue.length,
      lastSyncSuccess: this.lastSyncSuccess,
      lastSyncError: this.lastSyncError,
      provider: this.config.provider,
      userId: this.config.userId || null
    };
  }

  public onStatusChange(listener: (status: SyncStatus) => void): () => void {
    this.statusListeners.push(listener);
    listener(this.getStatus());
    return () => {
      this.statusListeners = this.statusListeners.filter((l) => l !== listener);
    };
  }

  private notificarStatus(): void {
    const status = this.getStatus();
    this.statusListeners.forEach((listener) => {
      try {
        listener(status);
      } catch (e) {
        console.error('[SyncManager] Erro no listener de status:', e);
      }
    });
  }
}

// Instância singleton global do SyncManager
export const AppSyncManager = new SyncManager();

if (typeof window !== 'undefined') {
  window.AppSyncManager = AppSyncManager;
}
