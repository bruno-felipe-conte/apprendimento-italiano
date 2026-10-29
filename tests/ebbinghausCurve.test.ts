// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import {
  calculateRetention,
  calculateTimeToTarget,
  predictNextStabilityGood,
  formatDaysLabel,
  computeEbbinghausCurve,
  renderEbbinghausCurve,
  EBBINGHAUS_I18N,
  FSRSCardInput,
} from '../src/analytics/ebbinghausCurve';

describe('src/analytics/ebbinghausCurve.ts — FSRS-4.5 / FSRS-5 & UI Specification', () => {
  beforeEach(() => {
    document.body.innerHTML = '';
  });

  describe('1. Suporte Real ao Decaimento Paramétrico do FSRS-5 (w20 / decay)', () => {
    it('deve respeitar R(S, S) = 0.90 para qualquer w20 no intervalo válido [0.1, 0.8]', () => {
      const s = 10;
      const w20Values = [0.1, 0.2, 0.35, 0.5, 0.65, 0.8];

      for (const w20 of w20Values) {
        const decay = -w20;
        const factor = Math.pow(0.9, 1 / decay) - 1;
        const rAtS = calculateRetention(s, s, factor, decay);
        expect(rAtS).toBeCloseTo(0.9, 6);
      }
    });

    it('quando w20 = 0.5, factor deve coincidir exatamente com 19/81 (FSRS-4.5)', () => {
      const decay = -0.5;
      const factor = Math.pow(0.9, 1 / decay) - 1;
      expect(factor).toBeCloseTo(19 / 81, 7);
    });

    it('w20 altera a inclinação da curva de esquecimento mantendo R(S, S) = 0.90', () => {
      const card: FSRSCardInput = { stability: 10, difficulty: 5 };

      // Curva com w20 = 0.2 vs w20 = 0.7
      const curveW20Baixo = computeEbbinghausCurve([card], card, { desiredRetention: 0.9, w20: 0.2 });
      const curveW20Alto = computeEbbinghausCurve([card], card, { desiredRetention: 0.9, w20: 0.7 });

      // Ambas cruzam 0.90 exatamente em t = S = 10 dias
      expect(curveW20Baixo.tTargetAtual).toBe(10);
      expect(curveW20Alto.tTargetAtual).toBe(10);

      const decayBaixo = -0.2;
      const factorBaixo = Math.pow(0.9, 1 / decayBaixo) - 1;

      const decayAlto = -0.7;
      const factorAlto = Math.pow(0.9, 1 / decayAlto) - 1;

      // Ponto de teste a t = 10 (t = S): ambos são 0.90
      expect(calculateRetention(10, 10, factorBaixo, decayBaixo)).toBeCloseTo(0.9, 6);
      expect(calculateRetention(10, 10, factorAlto, decayAlto)).toBeCloseTo(0.9, 6);

      // Ponto de teste após t = S (ex: t = 20 dias, esquecimento mais avançado):
      // Com w20 maior (|decay| maior), a retenção cai mais rápido a longo prazo
      const rPosSBaixo = calculateRetention(20, 10, factorBaixo, decayBaixo);
      const rPosSAlto = calculateRetention(20, 10, factorAlto, decayAlto);
      expect(rPosSBaixo).toBeGreaterThan(rPosSAlto);
    });

    it('faz clamp seguro de w20 para [0.1, 0.8]', () => {
      const card: FSRSCardInput = { stability: 10, difficulty: 5 };
      const curveUnder = computeEbbinghausCurve([card], card, { w20: 0.01 });
      const curveOver = computeEbbinghausCurve([card], card, { w20: 1.5 });

      expect(curveUnder.hasData).toBe(true);
      expect(curveOver.hasData).toBe(true);
    });
  });

  describe('2. Cálculo Real da Recuperabilidade (R) em predictNextStabilityGood', () => {
    it('gera um ganho de estabilidade maior quando currentR é menor (efeito de espaçamento em revisões atrasadas)', () => {
      const card: FSRSCardInput = { stability: 10, difficulty: 5 };

      // Caso A: revisão pontual (R = 0.90)
      const nextSPontual = predictNextStabilityGood(card, 10, 0.9);

      // Caso B: revisão atrasada (R = 0.75 - estudante quase esquecendo, esforço maior)
      const nextSAtrasada = predictNextStabilityGood(card, 10, 0.75);

      // No FSRS: (Math.exp(W10 * (1 - R)) - 1) aumenta quanto menor o R
      expect(nextSAtrasada).toBeGreaterThan(nextSPontual);
    });

    it('calcula o R real via last_review quando fornecido no card ativo', () => {
      const agora = Date.now();
      // Card revisado há 20 dias com estabilidade de 10 dias (R real bem abaixo de 0.90)
      const cardAtrasado: FSRSCardInput = {
        stability: 10,
        difficulty: 5,
        last_review: agora - 20 * 86400000,
      };

      const curveAtrasada = computeEbbinghausCurve([cardAtrasado], cardAtrasado, {
        desiredRetention: 0.9,
      });

      // Comparado com um card sem last_review (onde currentR é o target 0.9)
      const cardPadrao: FSRSCardInput = { stability: 10, difficulty: 5 };
      const curvePadrao = computeEbbinghausCurve([cardPadrao], cardPadrao, {
        desiredRetention: 0.9,
      });

      expect(curveAtrasada.sBom).toBeGreaterThan(curvePadrao.sBom);
    });

    it('aplica clamp de segurança em currentR entre 0.1 e 0.99', () => {
      const card: FSRSCardInput = { stability: 5, difficulty: 4 };
      const resMin = predictNextStabilityGood(card, 5, -0.5);
      const resMax = predictNextStabilityGood(card, 5, 2.0);

      expect(Number.isFinite(resMin)).toBe(true);
      expect(Number.isFinite(resMax)).toBe(true);
      expect(resMin).toBeGreaterThan(5);
      expect(resMax).toBeGreaterThan(5);
    });
  });

  describe('3. Coerência entre Pontos Plotados e Rótulos de Tempo (tTargetLabel vs sLabel)', () => {
    it('com desiredRetention: 0.90, tTargetAtual é exatamente igual a sAtual', () => {
      const card: FSRSCardInput = { stability: 4, difficulty: 5 };
      const curve = computeEbbinghausCurve([card], card, { desiredRetention: 0.9 });

      expect(curve.sAtual).toBe(4);
      expect(curve.tTargetAtual).toBe(4);
      expect(curve.sAtualLabel).toBe('4d');
      expect(curve.tTargetAtualLabel).toBe('4d');
    });

    it('com desiredRetention: 0.85, tTargetAtual é maior que sAtual e tTargetAtualLabel reflete esse tempo maior', () => {
      const card: FSRSCardInput = { stability: 4, difficulty: 5 };
      const curve = computeEbbinghausCurve([card], card, { desiredRetention: 0.85 });

      expect(curve.sAtual).toBe(4);
      // Para S = 4 e R = 0.85 com FSRS padrão (w20=0.5):
      // t = (4 / (19/81)) * (0.85^(-2) - 1) = 17.0526 * (1.38408 - 1) ≈ 6.55 dias
      expect(curve.tTargetAtual).toBeGreaterThan(curve.sAtual);
      expect(curve.tTargetAtual).toBeCloseTo(6.55, 1);

      expect(curve.sAtualLabel).toBe('4d');
      expect(curve.tTargetAtualLabel).toBe('6.5d');
    });

    it('renderEbbinghausCurve exibe tTarget no eixo X e estabilidade S na legenda', () => {
      const container = document.createElement('div');
      const card: FSRSCardInput = { stability: 4, difficulty: 5 };

      renderEbbinghausCurve(container, [card], card, { desiredRetention: 0.85, locale: 'pt' });

      const svg = container.querySelector('svg');
      expect(svg).not.toBeNull();

      // No eixo X (y="164") do SVG deve constar o tempo real até o alvo (+6.5d)
      const textosX = Array.from(svg!.querySelectorAll('text[y="164"]')).map((t) =>
        t.textContent?.trim()
      );
      expect(textosX.some((txt) => txt?.includes('+6.5d'))).toBe(true);

      // Na legenda inferior deve constar o parâmetro de estabilidade S (S=4d)
      const legenda = container.querySelector('.it-ebbinghaus-legend');
      expect(legenda?.textContent).toContain('S=4d');
    });
  });

  describe('4. Prevenção Dinâmica de Colisão dos Rótulos no Eixo X do SVG', () => {
    it('separa rótulos próximos garantindo distância mínima de 68px', () => {
      const container = document.createElement('div');
      // Cards com S muito próximo (S atual = 10, S bom próximo de 12)
      const card: FSRSCardInput = { stability: 10, difficulty: 9.8 };

      renderEbbinghausCurve(container, [card], card, { desiredRetention: 0.9, locale: 'it' });

      const texts = Array.from(container.querySelectorAll('text[y="164"]'));
      // texts[0] = Hoje/Oggi (x=36)
      // texts[1] = Atual
      // texts[2] = Bom
      expect(texts.length).toBe(3);

      const xAtual = parseFloat(texts[1].getAttribute('x') || '0');
      const xBom = parseFloat(texts[2].getAttribute('x') || '0');

      expect(xBom - xAtual).toBeGreaterThanOrEqual(67.9);
      // Garante que o rótulo atual não colide com "Hoje" em x=36
      expect(xAtual).toBeGreaterThanOrEqual(80);
      expect(texts[1].getAttribute('text-anchor')).toBe('middle');
      expect(texts[2].getAttribute('text-anchor')).toBe('middle');
    });
  });

  describe('5. Utilitários, Internacionalização e Acessibilidade (WCAG / Axe-core)', () => {
    it('formatDaysLabel formata inteiros e decimais com precisão', () => {
      expect(formatDaysLabel(1)).toBe('1d');
      expect(formatDaysLabel(4)).toBe('4d');
      expect(formatDaysLabel(6.92)).toBe('6.9d');
      expect(formatDaysLabel(15.0)).toBe('15d');
    });

    it('suporta múltiplos idiomas (it, pt, en)', () => {
      expect(EBBINGHAUS_I18N.it.title).toBe('Curva dell’Oblio (Ebbinghaus)');
      expect(EBBINGHAUS_I18N.pt.title).toBe('Curva de Esquecimento (Ebbinghaus)');
      expect(EBBINGHAUS_I18N.en.title).toBe('Forgetting Curve (Ebbinghaus)');
    });

    it('renderiza fallback amigável quando não há cards cadastrados', () => {
      const container = document.createElement('div');
      renderEbbinghausCurve(container, [], null, { locale: 'pt' });

      expect(container.textContent).toContain('Estude o 1º card para calcular a curva real');
      expect(container.querySelector('circle')).toBeNull();
    });

    it('atende critérios de acessibilidade SVG (role="img", aria-labelledby, <title> e <desc>)', () => {
      const container = document.createElement('div');
      const card: FSRSCardInput = { stability: 5, difficulty: 4 };

      renderEbbinghausCurve(container, [card], card, { locale: 'it' });

      const svg = container.querySelector('svg');
      expect(svg?.getAttribute('role')).toBe('img');
      expect(svg?.getAttribute('aria-labelledby')).toBeTruthy();
      expect(svg?.querySelector('title')).not.toBeNull();
      expect(svg?.querySelector('desc')).not.toBeNull();
    });
  });
});
