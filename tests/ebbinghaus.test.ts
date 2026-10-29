// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import '../js/ebbinghaus.js';

interface IEbbinghausCard {
  id?: string;
  stability?: number;
  difficulty?: number;
  intervalo?: number;
  scheduled_days?: number;
  ease_factor?: number;
  ef?: number;
}

interface IEbbinghausModule {
  EBBINGHAUS_I18N: Record<string, {
    title: string;
    subtitle: string;
    sourceEmpty: string;
    sourceFocused: string;
    sourceDeck: string;
    today: string;
    currentS: string;
    goodS: string;
    emptyPrompt: string;
    legendNoReview: (s: string) => string;
    legendAfterGood: (s: string) => string;
    ariaSummary: (sAtual: string, sBom: string, pct: number) => string;
  }>;
  predictNextStabilityGood: (card: IEbbinghausCard | null, currentS: number) => number;
  formatDaysLabel: (d: number) => string;
  computeEbbinghausCurve: (
    cards?: IEbbinghausCard[],
    activeCard?: IEbbinghausCard | null,
    options?: { desiredRetention?: number; curveMode?: string }
  ) => {
    hasData: boolean;
    targetPct: number;
    targetY: number;
    sAtual: number;
    sBom: number;
    tTargetAtual: number;
    tTargetBom: number;
    sAtualLabel: string;
    sBomLabel: string;
    pathAtual: string;
    pathBom: string;
    pointAtual: { x: number; y: number } | null;
    pointBom: { x: number; y: number } | null;
    sourceKey: string;
  };
  renderEbbinghausCurve: (
    container: HTMLElement | null,
    cards?: IEbbinghausCard[],
    activeCard?: IEbbinghausCard | null,
    options?: { locale?: string; desiredRetention?: number; curveMode?: string }
  ) => unknown;
}

declare global {
  var Ebbinghaus: IEbbinghausModule;
}

const {
  EBBINGHAUS_I18N,
  predictNextStabilityGood,
  formatDaysLabel,
  computeEbbinghausCurve,
  renderEbbinghausCurve
} = globalThis.Ebbinghaus;

describe('Curva dell’Oblio (Ebbinghaus) — FSRS-4.5 / FSRS-5 Spec', () => {
  beforeEach(() => {
    document.body.innerHTML = '';
  });

  it('1. Proprietà matematiche della ritenzione R(t,S) secondo la legge di potenza FSRS', () => {
    const cards: IEbbinghausCard[] = [{ stability: 10, difficulty: 5 }];
    const curve = computeEbbinghausCurve(cards, cards[0], { desiredRetention: 0.90 });

    expect(curve.hasData).toBe(true);
    expect(curve.sAtual).toBe(10);
    expect(curve.tTargetAtual).toBe(10); // A R_alvo = 0.90, tTarget = S
    expect(curve.targetPct).toBe(90);

    // Valida limiti delle coordinate SVG (viewBox 0 0 380 175)
    expect(curve.pointAtual?.x).toBeGreaterThanOrEqual(38);
    expect(curve.pointAtual?.x).toBeLessThanOrEqual(355);
    expect(curve.pointAtual?.y).toBeGreaterThanOrEqual(20);
    expect(curve.pointAtual?.y).toBeLessThanOrEqual(145);
  });

  it('2. Predizione della stabilità successiva S_bom (Rating = 3)', () => {
    // Carta con difficoltà FSRS (D = 4, S = 5)
    const cardFSRS: IEbbinghausCard = { stability: 5, difficulty: 4 };
    const nextS = predictNextStabilityGood(cardFSRS, 5);
    expect(nextS).toBeGreaterThan(5);
    expect(nextS).toBeGreaterThanOrEqual(6); // S + 1

    // Fallback con Ease Factor (EF = 2.5)
    const cardLegacy: IEbbinghausCard = { ease_factor: 2.5 };
    const nextSLegacy = predictNextStabilityGood(cardLegacy, 4);
    expect(nextSLegacy).toBe(10); // 4 * 2.5 = 10
  });

  it('3. Formattazione dell’etichetta dei giorni (formatDaysLabel)', () => {
    expect(formatDaysLabel(1)).toBe('1d');
    expect(formatDaysLabel(10)).toBe('10d');
    expect(formatDaysLabel(2.5)).toBe('2.5d');
    expect(formatDaysLabel(3.0)).toBe('3d');
  });

  it('4. computeEbbinghausCurve — Stato vuoto (senza carte)', () => {
    const emptyResult = computeEbbinghausCurve([], null, { desiredRetention: 0.90 });
    expect(emptyResult.hasData).toBe(false);
    expect(emptyResult.sAtual).toBe(0);
    expect(emptyResult.sBom).toBe(0);
    expect(emptyResult.sourceKey).toBe('empty');
    expect(emptyResult.pointAtual).toBeNull();
    expect(emptyResult.pathAtual).toBe('');
  });

  it('5. computeEbbinghausCurve — Carta attiva in esame (focused)', () => {
    const cards: IEbbinghausCard[] = [
      { id: 'c1', stability: 3, difficulty: 5 },
      { id: 'c2', stability: 20, difficulty: 3 }
    ];
    const result = computeEbbinghausCurve(cards, cards[0], { desiredRetention: 0.90 });
    expect(result.hasData).toBe(true);
    expect(result.sourceKey).toBe('focused');
    expect(result.sAtual).toBe(3);
    expect(result.sBom).toBeGreaterThan(3);
  });

  it('6. computeEbbinghausCurve — Media del mazzo (deck average)', () => {
    const cards: IEbbinghausCard[] = [
      { id: 'c1', stability: 2 },
      { id: 'c2', stability: 6 }
    ];
    const result = computeEbbinghausCurve(cards, null, { desiredRetention: 0.90 });
    expect(result.hasData).toBe(true);
    expect(result.sourceKey).toBe('deck_average');
    expect(result.sAtual).toBe(4); // (2 + 6) / 2 = 4
  });

  it('7. Dizionario multilingue e localizzazione (it, pt, en)', () => {
    expect(EBBINGHAUS_I18N.it).toBeDefined();
    expect(EBBINGHAUS_I18N.pt).toBeDefined();
    expect(EBBINGHAUS_I18N.en).toBeDefined();

    expect(EBBINGHAUS_I18N.it.title).toBe('Curva dell’Oblio (Ebbinghaus)');
    expect(EBBINGHAUS_I18N.it.sourceFocused).toBe('Carta in esame');
    expect(EBBINGHAUS_I18N.it.goodS).toBe('Buono');

    const summaryIT = EBBINGHAUS_I18N.it.ariaSummary('5d', '12d', 90);
    expect(summaryIT).toContain('Curva dell’Oblio');
    expect(summaryIT).toContain('90%');
  });

  it('8. renderEbbinghausCurve — Generazione DOM e conformità WCAG / Axe-core', () => {
    const container = document.createElement('div');
    document.body.appendChild(container);

    const cards: IEbbinghausCard[] = [{ id: 'c1', stability: 7, difficulty: 5 }];
    const data = renderEbbinghausCurve(container, cards, cards[0], { locale: 'it' });

    expect(data).not.toBeNull();
    const section = container.querySelector('.it-ebbinghaus-card');
    expect(section).not.toBeNull();

    const svg = container.querySelector('svg.it-ebbinghaus-svg');
    expect(svg).not.toBeNull();
    expect(svg?.getAttribute('role')).toBe('img');
    expect(svg?.querySelector('title')).not.toBeNull();
    expect(svg?.querySelector('desc')).not.toBeNull();
    expect(container.textContent).toContain('Curva dell’Oblio');
    expect(container.textContent).toContain('Carta in esame');
  });
});
