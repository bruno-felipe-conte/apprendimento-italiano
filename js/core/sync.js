/**
 * Módulo de Sincronização e Backend Lite (EV-02)
 * Arquitetura Offline-First com Fila Persistente e Adapters para Supabase e PocketBase.
 */
const STORAGE_QUEUE_KEY = 'apprendimento_sync_queue';
const STORAGE_CONFIG_KEY = 'apprendimento_backend_config';
const MAX_ATTEMPTS = 5;
// ==========================================
// ADAPTER MOCK (Para Testes e Modo Local)
// ==========================================
export class MockBackendAdapter {
    provider = 'mock';
    memoryStore = new Map();
    shouldFail = false;
    networkDelayMs = 0;
    async init(_config) {
        // Inicialização mock
    }
    async syncBatch(items) {
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
        const processados = [];
        for (const item of items) {
            if (!this.memoryStore.has(item.entity)) {
                this.memoryStore.set(item.entity, new Map());
            }
            const table = this.memoryStore.get(item.entity);
            if (item.action === 'delete') {
                table.delete(item.entityId);
            }
            else {
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
    async pullLatest(entity) {
        const table = this.memoryStore.get(entity);
        if (!table)
            return [];
        return Array.from(table.values());
    }
}
// ==========================================
// ADAPTER SUPABASE (REST / PostgREST)
// ==========================================
export class SupabaseAdapter {
    provider = 'supabase';
    config = { provider: 'supabase', endpoint: '' };
    init(config) {
        this.config = config;
    }
    getHeaders() {
        const headers = {
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
    async syncBatch(items) {
        const processados = [];
        const falhas = [];
        for (const item of items) {
            try {
                const url = `${this.config.endpoint.replace(/\/$/, '')}/rest/v1/${item.entity}`;
                const headers = this.getHeaders();
                let resp;
                if (item.action === 'delete') {
                    resp = await fetch(`${url}?id=eq.${encodeURIComponent(item.entityId)}`, {
                        method: 'DELETE',
                        headers
                    });
                }
                else {
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
                }
                else {
                    const errText = await resp.text();
                    falhas.push({ id: item.id, erro: `HTTP ${resp.status}: ${errText}` });
                }
            }
            catch (err) {
                falhas.push({ id: item.id, erro: err.message || 'Erro de conexão com Supabase' });
            }
        }
        return {
            sucesso: falhas.length === 0,
            processados,
            falhas
        };
    }
    async authMagicLink(email) {
        try {
            const url = `${this.config.endpoint.replace(/\/$/, '')}/auth/v1/otp`;
            const resp = await fetch(url, {
                method: 'POST',
                headers: this.getHeaders(),
                body: JSON.stringify({ email, create_user: true })
            });
            return resp.ok;
        }
        catch {
            return false;
        }
    }
}
// ==========================================
// ADAPTER POCKETBASE (REST)
// ==========================================
export class PocketBaseAdapter {
    provider = 'pocketbase';
    config = { provider: 'pocketbase', endpoint: '' };
    init(config) {
        this.config = config;
    }
    getHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (this.config.authToken) {
            headers['Authorization'] = this.config.authToken;
        }
        return headers;
    }
    async syncBatch(items) {
        const processados = [];
        const falhas = [];
        for (const item of items) {
            try {
                const base = `${this.config.endpoint.replace(/\/$/, '')}/api/collections/${item.entity}/records`;
                const headers = this.getHeaders();
                let resp;
                if (item.action === 'delete') {
                    resp = await fetch(`${base}/${encodeURIComponent(item.entityId)}`, {
                        method: 'DELETE',
                        headers
                    });
                }
                else if (item.action === 'update') {
                    resp = await fetch(`${base}/${encodeURIComponent(item.entityId)}`, {
                        method: 'PATCH',
                        headers,
                        body: JSON.stringify(item.payload)
                    });
                }
                else {
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
                }
                else {
                    const errText = await resp.text();
                    falhas.push({ id: item.id, erro: `HTTP ${resp.status}: ${errText}` });
                }
            }
            catch (err) {
                falhas.push({ id: item.id, erro: err.message || 'Erro de conexão com PocketBase' });
            }
        }
        return {
            sucesso: falhas.length === 0,
            processados,
            falhas
        };
    }
    async authWithPassword(email, pass) {
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
    queue = [];
    adapter;
    config;
    isSyncing = false;
    syncTimer = null;
    statusListeners = [];
    lastSyncSuccess = null;
    lastSyncError = null;
    // Multi-tab coordination
    tabId = `sync_tab_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;
    syncChannel = null;
    constructor(adapter) {
        this.config = this.carregarConfig();
        this.adapter = adapter || this.criarAdapter(this.config.provider);
        this.carregarFila();
        this.configurarListenersOnline();
        this.configurarCrossTabSync();
        if (this.config.autoSync) {
            this.iniciarSyncPeriodico();
        }
    }
    carregarConfig() {
        try {
            if (typeof localStorage !== 'undefined') {
                const raw = localStorage.getItem(STORAGE_CONFIG_KEY);
                if (raw)
                    return JSON.parse(raw);
            }
        }
        catch (e) {
            console.warn('[SyncManager] Erro ao carregar config:', e);
        }
        return {
            provider: 'mock',
            endpoint: '',
            autoSync: true,
            syncIntervalMs: 30000
        };
    }
    salvarConfig(novaConfig) {
        this.config = { ...this.config, ...novaConfig };
        try {
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem(STORAGE_CONFIG_KEY, JSON.stringify(this.config));
            }
        }
        catch (e) {
            console.warn('[SyncManager] Erro ao salvar config:', e);
        }
        if (novaConfig.provider && novaConfig.provider !== this.adapter.provider) {
            this.adapter = this.criarAdapter(this.config.provider);
            this.adapter.init(this.config);
        }
        if (this.config.autoSync) {
            this.iniciarSyncPeriodico();
        }
        else {
            this.pararSyncPeriodico();
        }
        this.notificarStatus();
    }
    setAdapter(adapter) {
        this.adapter = adapter;
        this.adapter.init(this.config);
    }
    getAdapter() {
        return this.adapter;
    }
    criarAdapter(provider) {
        switch (provider) {
            case 'supabase':
                return new SupabaseAdapter();
            case 'pocketbase':
                return new PocketBaseAdapter();
            default:
                return new MockBackendAdapter();
        }
    }
    carregarFila() {
        try {
            if (typeof localStorage !== 'undefined') {
                const raw = localStorage.getItem(STORAGE_QUEUE_KEY);
                if (raw) {
                    this.queue = JSON.parse(raw);
                }
            }
        }
        catch (e) {
            console.warn('[SyncManager] Erro ao carregar fila:', e);
            this.queue = [];
        }
    }
    persistirFila() {
        try {
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem(STORAGE_QUEUE_KEY, JSON.stringify(this.queue));
            }
        }
        catch (e) {
            console.error('[SyncManager] Falha ao persistir fila no localStorage:', e);
        }
        this.broadcastQueueChange();
    }
    configurarCrossTabSync() {
        if (typeof window === 'undefined')
            return;
        if (typeof BroadcastChannel !== 'undefined') {
            try {
                this.syncChannel = new BroadcastChannel('apprendimento_channel');
                this.syncChannel.onmessage = (event) => {
                    const msg = event?.data;
                    if (!msg || msg.senderId === this.tabId)
                        return;
                    if (msg.type === 'SYNC_UPDATE' && msg.key === STORAGE_QUEUE_KEY) {
                        this.recarregarFila();
                    }
                };
            }
            catch (_) {
                this.syncChannel = null;
            }
        }
        window.addEventListener('storage', (e) => {
            if (e.key === STORAGE_QUEUE_KEY) {
                this.recarregarFila();
            }
        });
    }
    broadcastQueueChange() {
        if (this.syncChannel) {
            try {
                this.syncChannel.postMessage({
                    type: 'SYNC_UPDATE',
                    key: STORAGE_QUEUE_KEY,
                    senderId: this.tabId,
                    timestamp: Date.now()
                });
            }
            catch (_) { }
        }
    }
    recarregarFila() {
        const contagemAnterior = this.queue.length;
        this.carregarFila();
        if (this.queue.length !== contagemAnterior) {
            this.notificarStatus();
        }
    }
    tentarAdquirirLockFlush() {
        if (typeof localStorage === 'undefined')
            return true;
        try {
            const agora = Date.now();
            const raw = localStorage.getItem('apprendimento_sync_lock');
            if (raw) {
                const lock = JSON.parse(raw);
                // Lock ativo de outra aba com expiração de 15 segundos
                if (lock && lock.tabId !== this.tabId && (agora - lock.timestamp < 15000)) {
                    return false;
                }
            }
            localStorage.setItem('apprendimento_sync_lock', JSON.stringify({ tabId: this.tabId, timestamp: agora }));
            return true;
        }
        catch (_) {
            return true;
        }
    }
    liberarLockFlush() {
        if (typeof localStorage === 'undefined')
            return;
        try {
            const raw = localStorage.getItem('apprendimento_sync_lock');
            if (raw) {
                const lock = JSON.parse(raw);
                if (lock && lock.tabId === this.tabId) {
                    localStorage.removeItem('apprendimento_sync_lock');
                }
            }
        }
        catch (_) { }
    }
    configurarListenersOnline() {
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
    iniciarSyncPeriodico() {
        this.pararSyncPeriodico();
        const interval = this.config.syncIntervalMs || 30000;
        this.syncTimer = setInterval(() => {
            if (this.queue.length > 0 && this.isOnline()) {
                this.flush();
            }
        }, interval);
    }
    pararSyncPeriodico() {
        if (this.syncTimer) {
            clearInterval(this.syncTimer);
            this.syncTimer = null;
        }
    }
    isOnline() {
        if (typeof navigator !== 'undefined' && typeof navigator.onLine === 'boolean') {
            return navigator.onLine;
        }
        return true;
    }
    /**
     * Enfileira uma ação de sincronização com deduplicação inteligente LWW (Last-Write-Wins).
     */
    enfileirar(entity, action, entityId, payload) {
        // Sincroniza com o estado em disco antes de mutar a fila
        this.recarregarFila();
        const timestamp = Date.now();
        const id = `sync_${timestamp}_${Math.random().toString(36).substring(2, 9)}`;
        // Deduplicação: verifica se já existe uma operação pendente para a mesma entidade
        const existingIndex = this.queue.findIndex((item) => item.entity === entity && item.entityId === entityId);
        let item;
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
            }
            else {
                // LWW: mescla o payload mais recente
                existing.payload = { ...existing.payload, ...payload };
                existing.timestamp = timestamp;
                item = existing;
            }
        }
        else {
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
        }
        else if (typeof navigator !== 'undefined' && 'serviceWorker' in navigator && typeof window !== 'undefined' && 'SyncManager' in window) {
            navigator.serviceWorker.ready.then((reg) => {
                if (reg?.sync?.register) {
                    reg.sync.register('app-sync-queue').catch(() => { });
                }
            }).catch(() => { });
        }
        return item;
    }
    /**
     * Esvazia e processa a fila de sincronização enviando as operações pendentes.
     */
    async flush() {
        if (this.isSyncing) {
            return { sucesso: true, processados: [], falhas: [] };
        }
        if (this.queue.length === 0) {
            // Recarrega do disco caso outra aba tenha enfileirado itens
            this.recarregarFila();
            if (this.queue.length === 0) {
                return { sucesso: true, processados: [], falhas: [] };
            }
        }
        if (!this.isOnline()) {
            return {
                sucesso: false,
                processados: [],
                falhas: [{ id: 'network', erro: 'Dispositivo offline' }]
            };
        }
        // Mutual-exclusion guard entre abas (15s lease lock)
        if (!this.tentarAdquirirLockFlush()) {
            return { sucesso: true, processados: [], falhas: [] };
        }
        this.isSyncing = true;
        this.notificarStatus();
        try {
            // Pega os primeiros 25 itens da fila para processar em lote
            const batch = this.queue.slice(0, 25);
            const resultado = await this.adapter.syncBatch(batch);
            // Recarrega a fila atual do disco para evitar sobrescrever itens gravados concorrentemente por outras abas
            let currentDisk = [];
            try {
                const raw = (typeof localStorage !== 'undefined') ? localStorage.getItem(STORAGE_QUEUE_KEY) : null;
                if (raw) {
                    const parsed = JSON.parse(raw);
                    currentDisk = Array.isArray(parsed) ? parsed : this.queue;
                }
                else {
                    currentDisk = this.queue;
                }
            }
            catch (_) {
                currentDisk = this.queue;
            }
            if (resultado.processados.length > 0) {
                const setSucesso = new Set(resultado.processados);
                this.queue = currentDisk.filter((item) => !setSucesso.has(item.id));
                this.lastSyncSuccess = Date.now();
                this.lastSyncError = null;
            }
            else {
                this.queue = currentDisk;
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
        }
        catch (err) {
            const erroMsg = err.message || 'Falha durante o flush de sincronização';
            this.lastSyncError = erroMsg;
            return {
                sucesso: false,
                processados: [],
                falhas: [{ id: 'exception', erro: erroMsg }]
            };
        }
        finally {
            this.isSyncing = false;
            this.liberarLockFlush();
            this.notificarStatus();
        }
    }
    /**
     * Limpa todos os itens da fila local.
     */
    limparFila() {
        this.queue = [];
        this.persistirFila();
        this.notificarStatus();
    }
    getFila() {
        return [...this.queue];
    }
    getStatus() {
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
    onStatusChange(listener) {
        this.statusListeners.push(listener);
        listener(this.getStatus());
        return () => {
            this.statusListeners = this.statusListeners.filter((l) => l !== listener);
        };
    }
    notificarStatus() {
        const status = this.getStatus();
        this.statusListeners.forEach((listener) => {
            try {
                listener(status);
            }
            catch (e) {
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
