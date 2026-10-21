// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import {
  AnalyticsManager,
  FeatureFlagManager,
  MockAnalyticsProvider,
  hashStringToInt
} from '../js/core/analytics';

describe('EV-04: Analytics & A/B Testing (Feature Flags)', () => {
  let mockProvider: MockAnalyticsProvider;
  let analytics: AnalyticsManager;
  let featureFlags: FeatureFlagManager;

  beforeEach(() => {
    localStorage.clear();
    mockProvider = new MockAnalyticsProvider();
    analytics = new AnalyticsManager(mockProvider);
    featureFlags = new FeatureFlagManager(analytics);
  });

  describe('Função de Hash Determinístico', () => {
    it('deve gerar sempre o mesmo valor entre 0 e 99 para a mesma string', () => {
      const h1 = hashStringToInt('user_42:xp_multiplier_variant');
      const h2 = hashStringToInt('user_42:xp_multiplier_variant');
      expect(h1).toBe(h2);
      expect(h1).toBeGreaterThanOrEqual(0);
      expect(h1).toBeLessThan(100);
    });
  });

  describe('Telemetria e Fila Offline (AnalyticsManager)', () => {
    it('deve registrar eventos com metadados completos (timestamp, userId, sessionId)', () => {
      const event = analytics.track('flashcard_rated', {
        card_id: 't1_001',
        rating: 3,
        reps: 2
      });

      expect(event).toBeDefined();
      expect(event.name).toBe('flashcard_rated');
      expect(event.properties.card_id).toBe('t1_001');
      expect(event.userId).toBe(analytics.getUserId());
      expect(event.sessionId).toBeDefined();
      expect(event.timestamp).toBeGreaterThan(0);
    });

    it('deve rastrear visualização de seção via helper page()', () => {
      const pageEv = analytics.page('grammatica', { de: 'templi' });
      expect(pageEv.name).toBe('section_viewed');
      expect(pageEv.properties.section).toBe('grammatica');
      expect(pageEv.properties.de).toBe('templi');
    });

    it('deve reter na fila quando offline e esvaziar ao despachar eventos via flush()', async () => {
      Object.defineProperty(navigator, 'onLine', { value: false, configurable: true });

      analytics.track('quiz_completed', { score: 10, total: 10 });
      analytics.track('story_finished', { story_id: 'stor_01' });

      expect(analytics.getEvents().length).toBe(2);

      Object.defineProperty(navigator, 'onLine', { value: true, configurable: true });

      const enviados = await analytics.flush();
      expect(enviados).toBe(2);
      expect(analytics.getEvents().length).toBe(0);
      expect(mockProvider.trackedEvents.length).toBe(2);
    });

    it('deve reter eventos na fila se o provider lançar erro', async () => {
      mockProvider.shouldFail = true;
      analytics.track('grammar_lesson_done', { topico: 'artigos' });

      await analytics.flush();
      // O evento deve continuar na fila para tentativa futura
      expect(analytics.getEvents().length).toBe(1);
    });

    it('deve atualizar o userId e propagar para o provider via identify()', () => {
      analytics.identify('aluno_vip_99', { plano: 'pro' });
      expect(analytics.getUserId()).toBe('aluno_vip_99');
      expect(mockProvider.identifiedUser?.userId).toBe('aluno_vip_99');
      expect(mockProvider.identifiedUser?.traits?.plano).toBe('pro');
    });
  });

  describe('A/B Testing & Feature Flags (FeatureFlagManager)', () => {
    it('deve avaliar variantes de forma determinística e estável para o mesmo usuário', () => {
      const var1 = featureFlags.getVariant('xp_multiplier_variant');
      const var2 = featureFlags.getVariant('xp_multiplier_variant');
      expect(var1).toBe(var2);
      expect(['standard', 'accelerated']).toContain(var1);
    });

    it('deve permitir sobrescrita manual de variante (para testes e QA)', () => {
      featureFlags.setOverride('xp_multiplier_variant', 'accelerated');
      expect(featureFlags.getVariant('xp_multiplier_variant')).toBe('accelerated');

      featureFlags.clearOverrides();
      const variantPosLimpeza = featureFlags.getVariant('xp_multiplier_variant');
      expect(['standard', 'accelerated']).toContain(variantPosLimpeza);
    });

    it('deve disparar evento experiment_exposure na primeira avaliação da sessão', () => {
      mockProvider.trackedEvents = [];
      featureFlags.getVariant('ui_templo_card_variant');

      const exposure = mockProvider.trackedEvents.find(
        (e) => e.name === 'experiment_exposure' && e.properties.flag_key === 'ui_templo_card_variant'
      );
      expect(exposure).toBeDefined();
      expect(['classic', 'compact']).toContain(exposure?.properties.variant);
    });

    it('deve retornar status consolidado de todas as flags registradas', () => {
      const status = featureFlags.getAllFlagsStatus();
      expect(status['xp_multiplier_variant']).toBeDefined();
      expect(status['fsrs_weights_experiment']).toBeDefined();
      expect(status['ui_templo_card_variant']).toBeDefined();
    });
  });
});
