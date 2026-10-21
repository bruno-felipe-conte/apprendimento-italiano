/**
 * Módulo de Analytics e Testes A/B (Feature Flags) (EV-04)
 * Telemetria offline-first, adapters plugáveis e avaliação determinística estável.
 */

import type {
  AnalyticsEvent,
  FeatureFlag,
  IAnalyticsProvider
} from '../../types/app';

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
export function hashStringToInt(str: string): number {
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
export class MockAnalyticsProvider implements IAnalyticsProvider {
  name = 'mock';
  public trackedEvents: AnalyticsEvent[] = [];
  public identifiedUser: { userId: string; traits?: Record<string, any> } | null = null;
  public shouldFail: boolean = false;

  track(event: AnalyticsEvent): void {
    if (this.shouldFail) throw new Error('Falha simulada no MockAnalyticsProvider');
    this.trackedEvents.push(event);
  }

  identify(userId: string, traits?: Record<string, any>): void {
    this.identifiedUser = { userId, traits };
  }
}

export class PlausibleAnalyticsProvider implements IAnalyticsProvider {
  name = 'plausible';
  private domain: string;
  private apiHost: string;

  constructor(domain: string = 'apprendimento-italiano.app', apiHost: string = 'https://plausible.io') {
    this.domain = domain;
    this.apiHost = apiHost.replace(/\/$/, '');
  }

  async track(event: AnalyticsEvent): Promise<void> {
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
    } catch {
      // Falha silenciosa em telemetria externa para não travar UX
    }
  }
}

// ==========================================
// ANALYTICS MANAGER (OFFLINE-FIRST)
// ==========================================
export class AnalyticsManager {
  private queue: AnalyticsEvent[] = [];
  private provider: IAnalyticsProvider;
  private userId: string;
  private sessionId: string;
  private isFlushing: boolean = false;

  constructor(provider?: IAnalyticsProvider) {
    this.provider = provider || new MockAnalyticsProvider();
    this.userId = this.obterOuCriarUserId();
    this.sessionId = `sess_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
    this.carregarFila();
  }

  private obterOuCriarUserId(): string {
    try {
      if (typeof localStorage !== 'undefined') {
        let id = localStorage.getItem(STORAGE_USER_ID_KEY);
        if (!id) {
          id = `usr_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
          localStorage.setItem(STORAGE_USER_ID_KEY, id);
        }
        return id;
      }
    } catch (_) {}
    return 'anonymous_user';
  }

  private carregarFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        const raw = localStorage.getItem(STORAGE_EVENTS_KEY);
        if (raw) this.queue = JSON.parse(raw);
      }
    } catch (_) {
      this.queue = [];
    }
  }

  private persistirFila(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        if (this.queue.length > MAX_EVENTS_IN_QUEUE) {
          this.queue = this.queue.slice(-MAX_EVENTS_IN_QUEUE);
        }
        localStorage.setItem(STORAGE_EVENTS_KEY, JSON.stringify(this.queue));
      }
    } catch (_) {}
  }

  public getUserId(): string {
    return this.userId;
  }

  public setProvider(provider: IAnalyticsProvider): void {
    this.provider = provider;
  }

  public getProvider(): IAnalyticsProvider {
    return this.provider;
  }

  public identify(userId: string, traits?: Record<string, any>): void {
    this.userId = userId;
    try {
      if (typeof localStorage !== 'undefined') {
        localStorage.setItem(STORAGE_USER_ID_KEY, userId);
      }
    } catch (_) {}
    if (this.provider.identify) {
      this.provider.identify(userId, traits);
    }
  }

  public track(name: string, properties: Record<string, any> = {}): AnalyticsEvent {
    const event: AnalyticsEvent = {
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
      this.flush().catch(() => {});
    }

    return event;
  }

  public page(section: string, properties: Record<string, any> = {}): AnalyticsEvent {
    return this.track('section_viewed', { section, ...properties });
  }

  public async flush(): Promise<number> {
    if (this.isFlushing || this.queue.length === 0) return 0;
    this.isFlushing = true;

    let enviados = 0;
    const restantes: AnalyticsEvent[] = [];

    for (const event of this.queue) {
      try {
        await this.provider.track(event);
        enviados++;
      } catch {
        restantes.push(event);
      }
    }

    this.queue = restantes;
    this.persistirFila();
    this.isFlushing = false;
    return enviados;
  }

  public getEvents(): readonly AnalyticsEvent[] {
    return [...this.queue];
  }

  public clearEvents(): void {
    this.queue = [];
    this.persistirFila();
  }
}

// ==========================================
// FEATURE FLAG & A/B TESTING MANAGER
// ==========================================
export class FeatureFlagManager {
  private flags: Map<string, FeatureFlag> = new Map();
  private overrides: Map<string, string> = new Map();
  private analytics: AnalyticsManager;
  private exposedInSession: Set<string> = new Set();

  constructor(analytics: AnalyticsManager) {
    this.analytics = analytics;
    this.carregarOverrides();
    this.registrarFlagsPadrao();
  }

  private carregarOverrides(): void {
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
    } catch (_) {}
  }

  private salvarOverrides(): void {
    try {
      if (typeof localStorage !== 'undefined') {
        const obj: Record<string, string> = {};
        this.overrides.forEach((v, k) => {
          obj[k] = v;
        });
        localStorage.setItem(STORAGE_OVERRIDES_KEY, JSON.stringify(obj));
      }
    } catch (_) {}
  }

  private registrarFlagsPadrao(): void {
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

  public registerFlag(flag: FeatureFlag): void {
    this.flags.set(flag.key, flag);
  }

  public setOverride(flagKey: string, variant: string): void {
    this.overrides.set(flagKey, variant);
    this.salvarOverrides();
  }

  public clearOverrides(): void {
    this.overrides.clear();
    this.salvarOverrides();
  }

  /**
   * Avalia a variante da flag de forma determinística por usuário.
   */
  public getVariant(flagKey: string): string {
    // 1. Verifica override manual/debug
    if (this.overrides.has(flagKey)) {
      return this.overrides.get(flagKey)!;
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

  public isEnabled(flagKey: string): boolean {
    const variant = this.getVariant(flagKey);
    return variant === 'true' || variant === 'on' || variant === 'enabled' || variant !== 'control';
  }

  public getAllFlagsStatus(): Record<string, { variant: string; isOverride: boolean }> {
    const result: Record<string, { variant: string; isOverride: boolean }> = {};
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
