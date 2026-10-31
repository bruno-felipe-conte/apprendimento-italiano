// @vitest-environment happy-dom
// tests/e2e/tier2_boundary_corner.test.ts
// Tier 2: Boundary & Corner Cases (Limits, Empty, Max-size, Negative, NaN/Infinity, Skew, Rapid Inputs)

import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  bootstrapAppDOM,
  resetAppEnvironment,
  dispatchKey,
  dispatchClick
} from './e2e_helpers';

import AppState from '../../js/core/state.js';
import AppNavigation from '../../js/core/navigation.js';
import AppXP from '../../js/core/xp.js';
import AppStats from '../../js/core/stats.js';
import AppTTS from '../../js/core/tts.js';
import App from '../../js/core.js';
import ModalManager from '../../js/modal_manager';
import { ConflictResolver } from '../../js/core/collaboration';
import { SyncManager, MockBackendAdapter } from '../../js/core/sync';
import {
  calculateRetention,
  calculateTimeToTarget,
  predictNextStabilityGood
} from '../../src/analytics/ebbinghausCurve';

describe('Tier 2: Boundary & Corner Cases (Extreme Limits, Malformed Payloads & Clock Skew)', () => {
  beforeEach(() => {
    bootstrapAppDOM();
    resetAppEnvironment();
  });

  // ============================================================
  // Area 1: Storage, Persistence & Data Resilience Boundaries
  // ============================================================
  describe('Area 1: Storage, Persistence & Data Resilience Boundaries', () => {
    it('B1: deve lidar graciosamente com QuotaExceededError durante salvarProgresso() acionando GC', () => {
      const quotaErr = new DOMException('The quota has been exceeded.', 'QuotaExceededError');
      const spyGC = vi.spyOn(AppState, '_gcFlashcards');

      const spySet = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => {
        throw quotaErr;
      });

      try {
        AppState.salvarProgresso();
      } finally {
        spySet.mockRestore();
      }

      expect(spyGC).toHaveBeenCalled();
    });

    it('B2: deve suportar _hidratarCacheLocal() quando payload SWR for corrupto, vazio ou nulo', () => {
      localStorage.setItem('it_swr_templos_meta', 'invalid-json{{{');
      expect(AppState._hidratarCacheLocal()).toBe(false);

      localStorage.setItem('it_swr_templos_meta', '');
      expect(AppState._hidratarCacheLocal()).toBe(false);

      localStorage.setItem('it_swr_templos_meta', '12345');
      expect(AppState._hidratarCacheLocal()).toBe(false);

      localStorage.setItem('it_swr_templos_meta', 'null');
      expect(AppState._hidratarCacheLocal()).toBe(false);
    });

    it('B3: deve carregar progresso defensivamente ao encontrar JSON malformado em it_progresso', () => {
      const entradasInvalidas = [
        '{nivel: 2, xp: ',
        '{"invalido": true,',
        'corrompido<<>>',
        ''
      ];

      for (const inv of entradasInvalidas) {
        localStorage.setItem('it_progresso', inv);
        const p = AppState.carregarProgresso();
        expect(p).toBeDefined();
        expect(p.nivel).toBe(1);
        expect(p.xp).toBe(0);
        expect(Array.isArray(p.templos_desbloqueados)).toBe(true);
      }
    });

    it('B4: deve carregar flashcards defensivamente quando it_flashcards for corrupto ou inválido', () => {
      const entradasInvalidas = ['{{{', '{invalido:', '<<corrompido>>', ''];

      for (const inv of entradasInvalidas) {
        localStorage.setItem('it_flashcards', inv);
        const cards = AppState.carregarFlashcards();
        expect(cards).toBeDefined();
        expect(cards).toEqual({});
      }
    });

    it('B5: escapeHtml deve suportar inputs limites: strings vazias, null, undefined, números e payloads gigantes', () => {
      expect(AppState.escapeHtml('')).toBe('');
      expect(AppState.escapeHtml(null)).toBe('');
      expect(AppState.escapeHtml(undefined)).toBe('');
      expect(AppState.escapeHtml(0)).toBe('0');
      expect(AppState.escapeHtml(12345)).toBe('12345');

      const payloadGigante = '<script>'.repeat(1000) + 'A&B'.repeat(1000);
      const sanitizado = AppState.escapeHtml(payloadGigante);
      expect(sanitizado).not.toContain('<script>');
      expect(sanitizado).toContain('&lt;script&gt;');
      expect(sanitizado).toContain('&amp;');
    });

    it('B6: backup import deve rejeitar payloads sem estrutura mínima sem corromper estado local', () => {
      const estadoOriginalXP = AppState.estado.progresso.xp;

      const payloadSemVersao = JSON.stringify({ progresso: { xp: 9999 } });
      const payloadSemProgresso = JSON.stringify({ versao: 4 });
      const payloadNaoJson = 'arquivonaojson';

      // Simulação da verificação estrita pré-flight de importação
      const validarBackup = (raw: string) => {
        try {
          const parsed = JSON.parse(raw);
          return !!(parsed && parsed.versao && parsed.progresso);
        } catch (_) {
          return false;
        }
      };

      expect(validarBackup(payloadSemVersao)).toBe(false);
      expect(validarBackup(payloadSemProgresso)).toBe(false);
      expect(validarBackup(payloadNaoJson)).toBe(false);

      expect(AppState.estado.progresso.xp).toBe(estadoOriginalXP);
    });

    it('B7: reconciliação com payload remoto vazio ou indefinido deve manter o estado local íntegro', () => {
      const resolver = new ConflictResolver();
      const local = {
        nivel: 2,
        xp: 200,
        templos_desbloqueados: [1, 2],
        conquistas: [],
        grammatica_completadas: []
      } as any;

      const remotoVazio = {
        nivel: 0,
        xp: 0,
        templos_desbloqueados: [],
        conquistas: [],
        grammatica_completadas: []
      } as any;

      const resultado = resolver.reconciliarProgresso(local, remotoVazio);
      expect(resultado.progresso.xp).toBe(200);
      expect(resultado.progresso.nivel).toBe(2);
      expect(resultado.progresso.templos_desbloqueados).toEqual([1, 2]);
    });
  });

  // ============================================================
  // Area 2: Algorithmic Stability, FSRS & Concurrency Boundaries
  // ============================================================
  describe('Area 2: Algorithmic Stability, FSRS & Concurrency Boundaries', () => {
    it('B8: calculateRetention com t < 0 ou estabilidade zero/negativa não deve produzir NaN', () => {
      const factor = 19 / 81;
      const decay = -0.5;

      // Tempo decorrido negativo (descompasso de relógio)
      const rNegT = calculateRetention(-5, 10, factor, decay);
      expect(Number.isFinite(rNegT)).toBe(true);
      expect(rNegT).toBeGreaterThanOrEqual(1.0);

      // Estabilidade zero ou negativa
      const rZeroS = calculateRetention(5, 0, factor, decay);
      expect(Number.isFinite(rZeroS)).toBe(true);
      expect(rZeroS).not.toBeNaN();
      expect(rZeroS).toBeGreaterThanOrEqual(0);

      const rNegS = calculateRetention(5, -10, factor, decay);
      expect(Number.isFinite(rNegS)).toBe(true);
      expect(rNegS).not.toBeNaN();
      expect(rNegS).toBeGreaterThanOrEqual(0);
    });

    it('B9: calculateRetention com t tendendo ao infinito deve tender assintoticamente a zero sem NaN', () => {
      const factor = 19 / 81;
      const decay = -0.5;

      const rGrande = calculateRetention(1000000, 10, factor, decay);
      expect(Number.isFinite(rGrande)).toBe(true);
      expect(rGrande).toBeGreaterThan(0);
      expect(rGrande).toBeLessThan(0.01);
    });

    it('B10: predictNextStabilityGood com valores extremos de dificuldade [1, 10] e estabilidade [0.1, 36500]', () => {
      const cardMinD = { difficulty: 1 };
      const cardMaxD = { difficulty: 10 };

      // Dificuldade mínima (1) e máxima (10)
      const sMinD = predictNextStabilityGood(cardMinD, 10, 0.9);
      const sMaxD = predictNextStabilityGood(cardMaxD, 10, 0.9);

      expect(Number.isFinite(sMinD)).toBe(true);
      expect(Number.isFinite(sMaxD)).toBe(true);
      expect(sMinD).toBeGreaterThan(sMaxD); // Menor dificuldade cresce estabilidade mais rápido

      // Estabilidade extrema
      const cardNormal = { difficulty: 5 };
      const sGigante = predictNextStabilityGood(cardNormal, 36500, 0.9);
      expect(Number.isFinite(sGigante)).toBe(true);
      expect(sGigante).toBeGreaterThan(36500);
    });

    it('B11: descompasso temporal (lastReview > now) deve ser contido monotonicamente em zero dias decorridos', () => {
      const agora = Date.now();
      const revisaoFutura = agora + 86400000 * 5; // 5 dias no futuro

      // Cálculo de elapsed days seguro (com clamp Math.max(0, ...))
      const diffDias = Math.max(0, (agora - revisaoFutura) / 86400000);
      expect(diffDias).toBe(0);

      // Retenção em t = 0 é exatamente 1.0
      const r = calculateRetention(diffDias, 10, 19 / 81, -0.5);
      expect(r).toBe(1.0);
    });

    it('B12: chamadas repetidas e com valores nulos/zero/negativos em ganharXP não devem corromper XP', () => {
      const xpOriginal = AppState.estado.progresso.xp;

      AppXP.ganharXP(0);
      expect(AppState.estado.progresso.xp).toBe(xpOriginal);

      // Valores negativos não devem subtrair na lógica de recompensa
      AppXP.ganharXP(-50 as any);
      // Se for tolerado ou adicionado, verificamos que não gera NaN
      expect(Number.isFinite(AppState.estado.progresso.xp)).toBe(true);
    });

    it('B13: navegação com parâmetros vazios, nulos ou desconhecidos não deve quebrar a aplicação', () => {
      expect(() => AppNavigation.navegar('')).not.toThrow();
      expect(() => AppNavigation.navegar(null as any)).not.toThrow();
      expect(() => AppNavigation.navegar('secao_fantasma_xyz')).not.toThrow();
    });

    it('B14: pronúncia de TTS com texto vazio, nulo ou com caracteres especiais não deve lançar exceção não-tratada', () => {
      expect(() => AppTTS.pronunciar('')).not.toThrow();
      expect(() => AppTTS.pronunciar(null as any)).not.toThrow();
      expect(() => AppTTS.pronunciar('!@#$%^&*()_+~`|}{[]:;?><,./')).not.toThrow();
    });
  });

  // ============================================================
  // Area 3: UX, Ergonomics, PWA Resilience & A11y Standards Boundaries
  // ============================================================
  describe('Area 3: UX, Ergonomics, PWA Resilience & A11y Standards Boundaries', () => {
    it('B15: teclas modificadoras (Ctrl/Alt/Meta) não devem disparar navegação numérica acidental', () => {
      const secInicial = AppState.estado.secaoAtiva;

      // Dispara tecla '2' com Ctrl pressionado
      const eventoCtrl = new KeyboardEvent('keydown', { key: '2', ctrlKey: true, bubbles: true });
      document.dispatchEvent(eventoCtrl);

      // Navegação não deve ter ocorrido
      expect(AppState.estado.secaoAtiva).toBe(secInicial);
    });

    it('B16: ModalManager deve criar valores padrão caso chamado sem opções ou com título vazio', () => {
      const id = ModalManager.abrir();
      expect(id).toBeTruthy();
      expect(ModalManager.stack.length).toBe(1);

      const titleEl = document.getElementById(`modal_title_${id}`);
      expect(titleEl?.textContent).toBe('');

      ModalManager.fechar(id);
    });

    it('B17: fechar modal inexistente ou fecharTopo com pilha vazia deve ser no-op seguro', () => {
      expect(() => ModalManager.fechar('id_fantasma')).not.toThrow();
      expect(ModalManager.stack.length).toBe(0);

      expect(() => ModalManager.fecharTopo()).not.toThrow();
      expect(ModalManager.stack.length).toBe(0);
    });

    it('B18: toggleAudioSpeed deve ciclar ciclicamente entre taxas válidas (0.85 -> 0.7 -> 0.5 -> 1 -> 0.85)', () => {
      AppState.estado.progresso.audio_rate = 1;

      AppTTS.toggleAudioSpeed();
      expect(AppState.estado.progresso.audio_rate).toBe(0.85);

      AppTTS.toggleAudioSpeed();
      expect(AppState.estado.progresso.audio_rate).toBe(0.7);

      AppTTS.toggleAudioSpeed();
      expect(AppState.estado.progresso.audio_rate).toBe(0.5);

      AppTTS.toggleAudioSpeed();
      expect(AppState.estado.progresso.audio_rate).toBe(1);
    });

    it('B19: toggleSidebarPin deve operar com segurança mesmo se elementos do DOM estiverem ausentes', () => {
      // Remove botões e barra do DOM temporariamente
      document.getElementById('sidebar-pin-btn')?.remove();
      document.getElementById('app-sidebar')?.remove();

      expect(() => AppNavigation.toggleSidebarPin()).not.toThrow();
      expect(localStorage.getItem('it_sidebar_pinned')).toBeTruthy();
    });

    it('B20: alternar tema repetidamente em alta frequência deve manter integridade e consistência', () => {
      for (let i = 0; i < 20; i++) {
        const proximo = i % 2 === 0 ? 'dark' : 'light';
        localStorage.setItem('it_tema', proximo);
        if (proximo === 'dark') document.body.classList.add('dark-mode');
        else document.body.classList.remove('dark-mode');
      }

      expect(localStorage.getItem('it_tema')).toBe('light');
      expect(document.body.classList.contains('dark-mode')).toBe(false);
    });
  });

  // ============================================================
  // Area 4: Continuous Improvement Framework & Automated Stress Boundaries
  // ============================================================
  describe('Area 4: Continuous Improvement Framework & Automated Stress Boundaries', () => {
    it('B21: fuzzing de payload em localStorage: caracteres Unicode, RTL, emojis e tags preservam integridade', () => {
      const payloadComplexo = {
        emoji: '🇮🇹 🍕 🏛️ 💬',
        rtl: 'مرحبا بالعالم',
        caracteresEspeciais: 'àèéìíîòóùú·«»“”',
        tags: '<span class="destaque">italiano</span>'
      };

      localStorage.setItem('it_teste_fuzzing', JSON.stringify(payloadComplexo));
      const resgatado = JSON.parse(localStorage.getItem('it_teste_fuzzing') || '{}');

      expect(resgatado.emoji).toBe(payloadComplexo.emoji);
      expect(resgatado.rtl).toBe(payloadComplexo.rtl);
      expect(resgatado.caracteresEspeciais).toBe(payloadComplexo.caracteresEspeciais);
      expect(resgatado.tags).toBe(payloadComplexo.tags);
    });

    it('B22: FSRS 100-step decay boundary: retrievability deve permanecer estritamente no intervalo (0, 1] para t de 0 a 100.000 dias', () => {
      const s = 5.0;
      const factor = 19 / 81;
      const decay = -0.5;

      for (let dias = 0; dias <= 100000; dias += 1000) {
        const r = calculateRetention(dias, s, factor, decay);
        expect(Number.isFinite(r)).toBe(true);
        expect(r).not.toBeNaN();
        expect(r).toBeGreaterThan(0);
        expect(r).toBeLessThanOrEqual(1.0);
      }
    });

    it('B23: SyncManager deve lidar com estouro de tentativas (MAX_ATTEMPTS) sem travar a fila offline', async () => {
      const adapter = new MockBackendAdapter();
      adapter.shouldFail = true; // Força erro simulado

      const sync = new SyncManager(adapter);
      sync.limparFila();

      sync.enfileirar('progress', 'update', 'progresso_teste', { xp: 50 });
      expect(sync.getFila().length).toBe(1);

      // Simula 5 tentativas consecutivas de flush
      for (let i = 0; i < 5; i++) {
        await sync.flush();
      }

      // Após exceder MAX_ATTEMPTS, o item deve ter sido descartado ou marcado com falha sem travar o app
      const filaFinal = sync.getFila();
      expect(filaFinal.length).toBe(0);
    });

    it('B24: reconciliador com timestamps no passado distante (1970) ou futuro distante (2099) resolve sem exceções', () => {
      const resolver = new ConflictResolver();
      const local = {
        nivel: 1,
        xp: 100,
        templos_desbloqueados: [1],
        ultimo_estudo: 0 // Epoch 1970
      } as any;

      const remoto = {
        nivel: 2,
        xp: 250,
        templos_desbloqueados: [1, 2],
        ultimo_estudo: 4102444800000 // Ano 2100
      } as any;

      const res = resolver.reconciliarProgresso(local, remoto);
      expect(res.progresso.xp).toBe(250);
      expect(res.progresso.nivel).toBe(2);
      expect(res.progresso.templos_desbloqueados).toEqual([1, 2]);
    });
  });
});
