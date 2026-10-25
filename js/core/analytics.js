/**
 * Módulo de Analytics e Testes A/B (Feature Flags) (EV-04)
 * Telemetria offline-first, adapters plugáveis e avaliação determinística estável.
 */
const STORAGE_EVENTS_KEY = 'apprendimento_analytics_events';
const STORAGE_USER_ID_KEY = 'apprendimento_analytics_user_id';
const STORAGE_OVERRIDES_KEY = 'apprendimento_flag_overrides';
const MAX_EVENTS_IN_QUEUE = 200;
// ==========================================
// FUNÇÕES UTILITÁRIAS DE HASHING
// ==========================================
/**
 * Gera um hash determinístico de 0 a 99 baseado em uma string de entrada.
 */
export function hashStringToInt(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = (hash << 5) - hash + str.charCodeAt(i);
        hash |= 0; // Converte para inteiro de 32 bits
    }
    return Math.abs(hash) % 100;
}
// ==========================================
// PROVIDERS DE TELEMETRIA
// ==========================================
export class MockAnalyticsProvider {
    name = 'mock';
    trackedEvents = [];
    identifiedUser = null;
    shouldFail = false;
    track(event) {
        if (this.shouldFail)
            throw new Error('Falha simulada no MockAnalyticsProvider');
        this.trackedEvents.push(event);
    }
    identify(userId, traits) {
        this.identifiedUser = { userId, traits };
    }
}
export class PlausibleAnalyticsProvider {
    name = 'plausible';
    domain;
    apiHost;
    constructor(domain = 'apprendimento-italiano.app', apiHost = 'https://plausible.io') {
        this.domain = domain;
        this.apiHost = apiHost.replace(/\/$/, '');
    }
    async track(event) {
        try {
            await fetch(`${this.apiHost}/api/event`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: event.name,
                    url: `app://italian/${event.properties?.section || 'main'}`,
                    domain: this.domain,
                    props: event.properties
                })
            });
        }
        catch {
            // Falha silenciosa em telemetria externa para não travar UX
        }
    }
}
// ==========================================
// ANALYTICS MANAGER (OFFLINE-FIRST)
// ==========================================
export class AnalyticsManager {
    queue = [];
    provider;
    userId;
    sessionId;
    isFlushing = false;
    constructor(provider) {
        this.provider = provider || new MockAnalyticsProvider();
        this.userId = this.obterOuCriarUserId();
        this.sessionId = `sess_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
        this.carregarFila();
    }
    obterOuCriarUserId() {
        try {
            if (typeof localStorage !== 'undefined') {
                let id = localStorage.getItem(STORAGE_USER_ID_KEY);
                if (!id) {
                    id = `usr_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
                    localStorage.setItem(STORAGE_USER_ID_KEY, id);
                }
                return id;
            }
        }
        catch (_) { }
        return 'anonymous_user';
    }
    carregarFila() {
        try {
            if (typeof localStorage !== 'undefined') {
                const raw = localStorage.getItem(STORAGE_EVENTS_KEY);
                if (raw)
                    this.queue = JSON.parse(raw);
            }
        }
        catch (_) {
            this.queue = [];
        }
    }
    persistirFila() {
        try {
            if (typeof localStorage !== 'undefined') {
                if (this.queue.length > MAX_EVENTS_IN_QUEUE) {
                    this.queue = this.queue.slice(-MAX_EVENTS_IN_QUEUE);
                }
                localStorage.setItem(STORAGE_EVENTS_KEY, JSON.stringify(this.queue));
            }
        }
        catch (_) { }
    }
    getUserId() {
        return this.userId;
    }
    setProvider(provider) {
        this.provider = provider;
    }
    getProvider() {
        return this.provider;
    }
    identify(userId, traits) {
        this.userId = userId;
        try {
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem(STORAGE_USER_ID_KEY, userId);
            }
        }
        catch (_) { }
        if (this.provider.identify) {
            this.provider.identify(userId, traits);
        }
    }
    track(name, properties = {}) {
        const event = {
            id: `ev_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`,
            name,
            properties: { ...properties },
            timestamp: Date.now(),
            userId: this.userId,
            sessionId: this.sessionId
        };
        this.queue.push(event);
        this.persistirFila();
        // Se estiver online, tenta enviar imediatamente
        if (typeof navigator === 'undefined' || navigator.onLine) {
            this.flush().catch(() => { });
        }
        return event;
    }
    page(section, properties = {}) {
        return this.track('section_viewed', { section, ...properties });
    }
    async flush() {
        if (this.isFlushing || this.queue.length === 0)
            return 0;
        this.isFlushing = true;
        let enviados = 0;
        const restantes = [];
        for (const event of this.queue) {
            try {
                await this.provider.track(event);
                enviados++;
            }
            catch {
                restantes.push(event);
            }
        }
        this.queue = restantes;
        this.persistirFila();
        this.isFlushing = false;
        return enviados;
    }
    getEvents() {
        return [...this.queue];
    }
    clearEvents() {
        this.queue = [];
        this.persistirFila();
    }
}
// ==========================================
// FEATURE FLAG & A/B TESTING MANAGER
// ==========================================
export class FeatureFlagManager {
    flags = new Map();
    overrides = new Map();
    analytics;
    exposedInSession = new Set();
    constructor(analytics) {
        this.analytics = analytics;
        this.carregarOverrides();
        this.registrarFlagsPadrao();
    }
    carregarOverrides() {
        try {
            if (typeof localStorage !== 'undefined') {
                const raw = localStorage.getItem(STORAGE_OVERRIDES_KEY);
                if (raw) {
                    const obj = JSON.parse(raw);
                    for (const [k, v] of Object.entries(obj)) {
                        this.overrides.set(k, String(v));
                    }
                }
            }
        }
        catch (_) { }
    }
    salvarOverrides() {
        try {
            if (typeof localStorage !== 'undefined') {
                const obj = {};
                this.overrides.forEach((v, k) => {
                    obj[k] = v;
                });
                localStorage.setItem(STORAGE_OVERRIDES_KEY, JSON.stringify(obj));
            }
        }
        catch (_) { }
    }
    registrarFlagsPadrao() {
        // 1. Variante de Curva de XP (padrão vs acelerado para novatos)
        this.registerFlag({
            key: 'xp_multiplier_variant',
            variants: ['standard', 'accelerated'],
            weights: [50, 50],
            defaultValue: 'standard',
            enabled: true
        });
        // 2. Variante de Hiperparâmetros FSRS
        this.registerFlag({
            key: 'fsrs_weights_experiment',
            variants: ['default', 'aggressive_recall'],
            weights: [50, 50],
            defaultValue: 'default',
            enabled: true
        });
        // 3. Variante de Visualização de Cards
        this.registerFlag({
            key: 'ui_templo_card_variant',
            variants: ['classic', 'compact'],
            weights: [50, 50],
            defaultValue: 'classic',
            enabled: true
        });
    }
    registerFlag(flag) {
        this.flags.set(flag.key, flag);
    }
    setOverride(flagKey, variant) {
        this.overrides.set(flagKey, variant);
        this.salvarOverrides();
    }
    clearOverrides() {
        this.overrides.clear();
        this.salvarOverrides();
    }
    /**
     * Avalia a variante da flag de forma determinística por usuário.
     */
    getVariant(flagKey) {
        // 1. Verifica override manual/debug
        if (this.overrides.has(flagKey)) {
            return this.overrides.get(flagKey);
        }
        const flag = this.flags.get(flagKey);
        if (!flag || flag.enabled === false) {
            return flag?.defaultValue || 'control';
        }
        // 2. Cálculo determinístico estável
        const userId = this.analytics.getUserId();
        const hashVal = hashStringToInt(`${userId}:${flagKey}`);
        const weights = flag.weights || flag.variants.map(() => 100 / flag.variants.length);
        let acumulado = 0;
        let selectedVariant = flag.defaultValue;
        for (let i = 0; i < flag.variants.length; i++) {
            acumulado += weights[i] || 0;
            if (hashVal < acumulado) {
                selectedVariant = flag.variants[i];
                break;
            }
        }
        // 3. Dispara evento de exposição apenas uma vez por sessão
        const exposureKey = `${flagKey}:${selectedVariant}`;
        if (!this.exposedInSession.has(exposureKey)) {
            this.exposedInSession.add(exposureKey);
            this.analytics.track('experiment_exposure', {
                flag_key: flagKey,
                variant: selectedVariant,
                user_id: userId
            });
        }
        return selectedVariant;
    }
    isEnabled(flagKey) {
        const variant = this.getVariant(flagKey);
        return variant === 'true' || variant === 'on' || variant === 'enabled' || variant !== 'control';
    }
    getAllFlagsStatus() {
        const result = {};
        this.flags.forEach((_, key) => {
            result[key] = {
                variant: this.getVariant(key),
                isOverride: this.overrides.has(key)
            };
        });
        return result;
    }
}
// Singletons globais
export const AppAnalytics = new AnalyticsManager();
export const AppFeatureFlags = new FeatureFlagManager(AppAnalytics);
if (typeof window !== 'undefined') {
    window.AppAnalytics = AppAnalytics;
    window.AppFeatureFlags = AppFeatureFlags;
}
