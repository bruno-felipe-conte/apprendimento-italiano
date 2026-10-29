/**
 * src/analytics/ebbinghausCurve.ts
 *
 * Projeção matemática da Curva do Esquecimento (Ebbinghaus) baseada em FSRS-4.5 / FSRS-5.
 * Implementação pura, zero dependências externas, compatível com TypeScript 5.7+ ESNext.
 * Em conformidade com acessibilidade WCAG 2.1 AA / Axe-core.
 */

// Padrões de Pesos do FSRS para incremento de estabilidade com avaliação "Bom" (Rating = 3)
export const W8 = 1.54575;
export const W9 = 0.1192;
export const W10 = 1.01925;

export interface FSRSCardInput {
  id?: string;
  stability?: number;
  difficulty?: number;
  intervalo?: number;
  scheduled_days?: number;
  ease_factor?: number;
  ef?: number;
  last_review?: string | number | Date | null;
  [key: string]: unknown;
}

export interface EbbinghausOptions {
  desiredRetention?: number;
  curveMode?: 'fsrs-power' | 'exponential';
  w20?: number;
  fsrsDecay?: number;
  locale?: 'it' | 'pt' | 'en' | string;
}

export interface EbbinghausPoint {
  x: number;
  y: number;
}

export interface EbbinghausResult {
  hasData: boolean;
  targetPct: number;
  targetY: number;
  sAtual: number;
  sBom: number;
  tTargetAtual: number;
  tTargetBom: number;
  sAtualLabel: string;
  sBomLabel: string;
  tTargetAtualLabel: string;
  tTargetBomLabel: string;
  pathAtual: string;
  pathBom: string;
  pointAtual: EbbinghausPoint | null;
  pointBom: EbbinghausPoint | null;
  sourceKey: 'empty' | 'focused' | 'deck_average';
}

export const EBBINGHAUS_I18N: Record<
  string,
  {
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
  }
> = {
  it: {
    title: 'Curva dell’Oblio (Ebbinghaus)',
    subtitle: 'Proiezione matematica di ritenzione basata su FSRS-5',
    sourceEmpty: 'Nessuna carta presente',
    sourceFocused: 'Carta in esame',
    sourceDeck: 'Media del mazzo',
    today: 'Oggi',
    currentS: 'S attuale',
    goodS: 'Buono',
    emptyPrompt: 'Ripassa la 1ª carta per calcolare la curva reale',
    legendNoReview: (s: string) => `Senza ripasso (S=${s})`,
    legendAfterGood: (s: string) => `Dopo 'Buono' (S=${s})`,
    ariaSummary: (sAtual: string, sBom: string, pct: number) =>
      `Grafico della Curva dell’Oblio di Ebbinghaus. Obiettivo di ritenzione del ${pct}%. Stabilità attuale di ${sAtual} e proiezione dopo risposta Buono di ${sBom}.`,
  },
  pt: {
    title: 'Curva de Esquecimento (Ebbinghaus)',
    subtitle: 'Projeção matemática de retenção baseada no FSRS-5',
    sourceEmpty: 'Sem cards cadastrados',
    sourceFocused: 'Carta em foco',
    sourceDeck: 'Média do baralho',
    today: 'Hoje',
    currentS: 'S atual',
    goodS: 'Bom',
    emptyPrompt: 'Estude o 1º card para calcular a curva real',
    legendNoReview: (s: string) => `Sem revisão (S=${s})`,
    legendAfterGood: (s: string) => `Após 'Bom' (S=${s})`,
    ariaSummary: (sAtual: string, sBom: string, pct: number) =>
      `Gráfico da Curva de Esquecimento de Ebbinghaus. Meta de retenção de ${pct}%. Estabilidade atual de ${sAtual} e projeção após resposta Bom de ${sBom}.`,
  },
  en: {
    title: 'Forgetting Curve (Ebbinghaus)',
    subtitle: 'Mathematical retention projection based on FSRS-5',
    sourceEmpty: 'No cards available',
    sourceFocused: 'Active card',
    sourceDeck: 'Deck average',
    today: 'Today',
    currentS: 'Current S',
    goodS: 'Good',
    emptyPrompt: 'Review your 1st card to calculate the retention curve',
    legendNoReview: (s: string) => `Without review (S=${s})`,
    legendAfterGood: (s: string) => `After 'Good' (S=${s})`,
    ariaSummary: (sAtual: string, sBom: string, pct: number) =>
      `Ebbinghaus Forgetting Curve chart. Target retention of ${pct}%. Current stability ${sAtual} and projected stability after Good of ${sBom}.`,
  },
};

/**
 * Calcula a probabilidade de retenção R(t, S) no modelo de potência FSRS-5/4.5.
 */
export function calculateRetention(
  t: number,
  s: number,
  factor: number,
  decay: number,
  curveMode: 'fsrs-power' | 'exponential' = 'fsrs-power',
  retentionTarget = 0.9
): number {
  const safeS = Math.max(0.2, s);
  if (curveMode === 'exponential') {
    return Math.pow(retentionTarget, t / safeS);
  }
  return Math.pow(1 + factor * (t / safeS), decay);
}

/**
 * Calcula o tempo t até a curva cruzar retentionTarget: R(t, S) = retentionTarget.
 */
export function calculateTimeToTarget(
  s: number,
  factor: number,
  decay: number,
  curveMode: 'fsrs-power' | 'exponential' = 'fsrs-power',
  retentionTarget = 0.9
): number {
  const safeS = Math.max(0.2, s);
  if (curveMode === 'exponential') {
    return safeS;
  }
  return (safeS / factor) * (Math.pow(retentionTarget, 1 / decay) - 1);
}

/**
 * Estima a próxima estabilidade S' após uma revisão com avaliação "Bom" (Rating = 3).
 *
 * Utiliza o R atual seguro (safeR ∈ [0.1, 0.99]), levando em consideração se o card
 * está atrasado (revisão tardia com R < 0.90 aumenta o ganho de estabilidade).
 */
export function predictNextStabilityGood(
  card: FSRSCardInput | null | undefined,
  currentS: number,
  currentR = 0.9
): number {
  if (!card) {
    return Number(Math.max(currentS + 1, currentS * 2.5).toFixed(1));
  }

  const dRaw = Number(card.difficulty);
  if (Number.isFinite(dRaw) && dRaw >= 1 && dRaw <= 10) {
    const safeR = Math.max(0.1, Math.min(0.99, Number(currentR) || 0.9));
    const gain =
      1 +
      Math.exp(W8) *
        (11 - dRaw) *
        Math.pow(Math.max(0.5, currentS), -W9) *
        (Math.exp(W10 * (1 - safeR)) - 1);

    const nextS = currentS * Math.max(1.5, gain);
    return Number(Math.max(currentS + 1, nextS).toFixed(1));
  }

  const ef = Math.max(1.3, Math.min(3.5, Number(card.ease_factor ?? card.ef ?? 2.5)));
  return Number(Math.max(currentS + 1, currentS * ef).toFixed(1));
}

/**
 * Formata dias para texto amigável (ex: 4d, 6.9d).
 */
export function formatDaysLabel(d: number): string {
  const rounded = Number(Number(d).toFixed(1));
  return Number.isInteger(rounded) ? `${rounded}d` : `${rounded.toFixed(1)}d`;
}

/**
 * Extrai os dias decorridos desde a última revisão do card, caso disponível.
 */
function getElapsedDays(card: FSRSCardInput | null | undefined): number | null {
  if (!card || card.last_review == null) return null;
  const lr = card.last_review;
  let timeMs: number;
  if (typeof lr === 'number') {
    timeMs = lr;
  } else if (lr instanceof Date) {
    timeMs = lr.getTime();
  } else if (typeof lr === 'string') {
    timeMs = new Date(lr).getTime();
  } else {
    return null;
  }

  if (Number.isNaN(timeMs) || timeMs <= 0) return null;
  const diffMs = Date.now() - timeMs;
  return Math.max(0, diffMs / 86400000);
}

/**
 * Calcula todos os dados matemáticos e vetores SVG da Curva de Ebbinghaus.
 */
export function computeEbbinghausCurve(
  cards: FSRSCardInput[] = [],
  activeCard: FSRSCardInput | null = null,
  options: EbbinghausOptions = {}
): EbbinghausResult {
  const retentionTarget = Math.max(
    0.7,
    Math.min(0.98, Number(options.desiredRetention) || 0.9)
  );
  const targetPct = Math.round(retentionTarget * 100);
  const curveMode = options.curveMode ?? 'fsrs-power';

  // Item 1: Suporte ao decaimento paramétrico FSRS-5 (w20 / fsrsDecay)
  const rawW20 = options.w20 ?? options.fsrsDecay ?? 0.5;
  const clampedW20 = Math.max(0.1, Math.min(0.8, Number(rawW20) || 0.5));
  const decay = -clampedW20;
  // Fator derivado dinamicamente para garantir que R(S, S) = 0.90 sempre:
  const factor = Math.pow(0.9, 1 / decay) - 1;

  const yFromRetention = (r: number): number => {
    const clamped = Math.max(0.58, Math.min(1.0, r));
    return Number((20 + ((1.0 - clamped) / 0.4) * 125).toFixed(1));
  };

  const targetY = yFromRetention(retentionTarget);

  if (!Array.isArray(cards) || cards.length === 0) {
    return {
      hasData: false,
      targetPct,
      targetY,
      sAtual: 0,
      sBom: 0,
      tTargetAtual: 0,
      tTargetBom: 0,
      sAtualLabel: '0d',
      sBomLabel: '0d',
      tTargetAtualLabel: '0d',
      tTargetBomLabel: '0d',
      pathAtual: '',
      pathBom: '',
      pointAtual: null,
      pointBom: null,
      sourceKey: 'empty',
    };
  }

  const extractS = (c: FSRSCardInput): number => {
    const raw = Number(c.stability ?? c.intervalo ?? c.scheduled_days ?? 0);
    return raw > 0 ? raw : 1;
  };

  const retentionAt = (t: number, s: number): number =>
    calculateRetention(t, s, factor, decay, curveMode, retentionTarget);

  const timeToTarget = (s: number): number =>
    calculateTimeToTarget(s, factor, decay, curveMode, retentionTarget);

  let sAtual = 1;
  let sBom = 2.5;
  let sourceKey: 'focused' | 'deck_average' = 'deck_average';

  // Item 2: Recuperabilidade real em predictNextStabilityGood
  if (activeCard) {
    sAtual = Number(extractS(activeCard).toFixed(1));
    const elapsed = getElapsedDays(activeCard);
    const cardR = elapsed !== null ? retentionAt(elapsed, sAtual) : retentionTarget;
    sBom = predictNextStabilityGood(activeCard, sAtual, cardR);
    sourceKey = 'focused';
  } else {
    const sumS = cards.reduce((acc, c) => acc + extractS(c), 0);
    sAtual = Number((sumS / cards.length).toFixed(1));

    const sumNext = cards.reduce((acc, c) => {
      const cS = extractS(c);
      const elapsed = getElapsedDays(c);
      const cardR = elapsed !== null ? retentionAt(elapsed, cS) : retentionTarget;
      return acc + predictNextStabilityGood(c, cS, cardR);
    }, 0);

    sBom = Number(Math.max(sAtual + 1, sumNext / cards.length).toFixed(1));
  }

  const tTargetAtual = Number(timeToTarget(sAtual).toFixed(2));
  const tTargetBom = Number(timeToTarget(sBom).toFixed(2));
  const tMax = Math.max(5, tTargetBom * 1.22);

  const xStart = 38;
  const xEnd = 355;
  const xSpan = xEnd - xStart;

  const xFromT = (t: number): number =>
    Number((xStart + Math.min(1, Math.max(0, t / tMax)) * xSpan).toFixed(1));

  const steps = 28;
  const buildPath = (s: number): string => {
    const pts: string[] = [];
    for (let i = 0; i <= steps; i++) {
      const t = (tMax * i) / steps;
      const x = xFromT(t);
      const y = yFromRetention(retentionAt(t, s));
      pts.push(`${i === 0 ? 'M' : 'L'} ${x} ${y}`);
    }
    return pts.join(' ');
  };

  return {
    hasData: true,
    targetPct,
    targetY,
    sAtual,
    sBom,
    tTargetAtual,
    tTargetBom,
    sAtualLabel: formatDaysLabel(sAtual),
    sBomLabel: formatDaysLabel(sBom),
    tTargetAtualLabel: formatDaysLabel(tTargetAtual),
    tTargetBomLabel: formatDaysLabel(tTargetBom),
    pathAtual: buildPath(sAtual),
    pathBom: buildPath(sBom),
    pointAtual: { x: xFromT(tTargetAtual), y: targetY },
    pointBom: { x: xFromT(tTargetBom), y: targetY },
    sourceKey,
  };
}

/**
 * Renderiza a visualização SVG da Curva de Ebbinghaus em um elemento do DOM.
 * Conforme WCAG 2.1 AA / Axe-core.
 */
export function renderEbbinghausCurve(
  container: HTMLElement | null,
  cards: FSRSCardInput[] = [],
  activeCard: FSRSCardInput | null = null,
  options: EbbinghausOptions = {}
): EbbinghausResult | null {
  if (!container) return null;

  const locale =
    options.locale ||
    ((typeof globalThis !== 'undefined' &&
      (globalThis as unknown as { I18n?: { currentLang?: string } }).I18n?.currentLang) as
      | string
      | undefined) ||
    'it';

  const dict = EBBINGHAUS_I18N[locale] || EBBINGHAUS_I18N['it'];
  const data = computeEbbinghausCurve(cards, activeCard, options);

  const sourceText =
    data.sourceKey === 'focused'
      ? dict.sourceFocused
      : data.sourceKey === 'deck_average'
        ? dict.sourceDeck
        : dict.sourceEmpty;

  const uid = `eb-${Math.random().toString(36).slice(2, 8)}`;

  // Item 4: Prevenção Dinâmica de Colisão dos Rótulos do Eixo X
  let xLabelAtual = data.pointAtual?.x ?? 120;
  let xLabelBom = data.pointBom?.x ?? 250;

  // Clampa ambos dentro das margens visíveis do SVG (38 a 355)
  xLabelAtual = Math.max(82, Math.min(340, xLabelAtual));
  xLabelBom = Math.max(82, Math.min(340, xLabelBom));

  const minGap = 68;
  if (xLabelBom - xLabelAtual < minGap) {
    const overlap = minGap - (xLabelBom - xLabelAtual);
    const shift = overlap / 2;
    xLabelAtual = Math.max(82, xLabelAtual - shift);
    xLabelBom = Math.min(345, xLabelBom + shift);

    // Se o clamp direito ainda causar proximidade, reajusta para a esquerda mantendo > 75
    if (xLabelBom - xLabelAtual < minGap) {
      xLabelAtual = Math.max(82, xLabelBom - minGap);
    }
  }

  container.innerHTML = `
    <section class="it-ebbinghaus-card" aria-labelledby="${uid}-title">
      <header class="it-ebbinghaus-header">
        <div>
          <h3 id="${uid}-title" class="it-ebbinghaus-title">${dict.title}</h3>
          <p class="it-ebbinghaus-subtitle">${dict.subtitle}</p>
        </div>
        <span class="it-ebbinghaus-badge">${sourceText}</span>
      </header>
      <div class="it-ebbinghaus-canvas">
        <svg
          viewBox="0 0 380 175"
          class="it-ebbinghaus-svg"
          role="img"
          aria-labelledby="${uid}-svg-title ${uid}-svg-desc"
        >
          <title id="${uid}-svg-title">${dict.title}</title>
          <desc id="${uid}-svg-desc">${dict.ariaSummary(
            data.sAtualLabel,
            data.sBomLabel,
            data.targetPct
          )}</desc>
          <line x1="36" y1="20" x2="360" y2="20" stroke="var(--it-eb-border)" stroke-width="1" />
          <line
            x1="36"
            y1="${data.targetY}"
            x2="360"
            y2="${data.targetY}"
            stroke="var(--it-eb-amber)"
            stroke-width="1"
            stroke-dasharray="4 4"
          />
          <line x1="36" y1="145" x2="360" y2="145" stroke="var(--it-eb-border)" stroke-width="1" />
          <text x="4" y="24" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">100%</text>
          <text x="4" y="${data.targetY + 3}" fill="var(--it-eb-amber)" font-size="9" font-family="monospace">${data.targetPct}%</text>
          <text x="8" y="148" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">60%</text>
          ${
            data.hasData && data.pointAtual && data.pointBom
              ? `
            <path d="${data.pathAtual}" fill="none" stroke="var(--it-eb-crimson)" stroke-width="2" opacity="0.85" />
            <path d="${data.pathBom}" fill="none" stroke="var(--it-eb-cypress)" stroke-width="3" />
            <circle cx="38" cy="20" r="4" fill="var(--it-eb-cypress)" />
            <circle cx="${data.pointAtual.x}" cy="${data.pointAtual.y}" r="3.5" fill="var(--it-eb-crimson)" />
            <circle cx="${data.pointBom.x}" cy="${data.pointBom.y}" r="4.5" fill="var(--it-eb-gold)" />
            <text x="36" y="164" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">${dict.today}</text>
            <text x="${xLabelAtual}" y="164" text-anchor="middle" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">+${data.tTargetAtualLabel} (${dict.currentS})</text>
            <text x="${xLabelBom}" y="164" text-anchor="middle" fill="var(--it-eb-cypress)" font-size="9" font-family="monospace">+${data.tTargetBomLabel} (${dict.goodS})</text>
          `
              : `
            <text x="198" y="92" text-anchor="middle" fill="var(--it-eb-dim)" font-size="10" font-family="monospace">
              ${dict.emptyPrompt}
            </text>
          `
          }
        </svg>
        <footer class="it-ebbinghaus-legend">
          <span class="it-ebbinghaus-legend-item it-ebbinghaus-legend-item--current">
            <span class="it-ebbinghaus-dot it-ebbinghaus-dot--current" aria-hidden="true"></span>
            ${dict.legendNoReview(data.sAtualLabel)}
          </span>
          <span class="it-ebbinghaus-legend-item it-ebbinghaus-legend-item--good">
            <span class="it-ebbinghaus-dot it-ebbinghaus-dot--good" aria-hidden="true"></span>
            ${dict.legendAfterGood(data.sBomLabel)}
          </span>
        </footer>
      </div>
    </section>
  `;

  return data;
}

// Objeto de exportação unificado para consumo modular ou UMD/Global
export const Ebbinghaus = {
  W8,
  W9,
  W10,
  EBBINGHAUS_I18N,
  calculateRetention,
  calculateTimeToTarget,
  predictNextStabilityGood,
  formatDaysLabel,
  computeEbbinghausCurve,
  renderEbbinghausCurve,
};

if (typeof window !== 'undefined') {
  (window as unknown as Record<string, unknown>).Ebbinghaus = Ebbinghaus;
  (window as unknown as Record<string, unknown>).computeEbbinghausCurve = computeEbbinghausCurve;
  (window as unknown as Record<string, unknown>).renderEbbinghausCurve = renderEbbinghausCurve;
}

if (typeof globalThis !== 'undefined') {
  (globalThis as unknown as Record<string, unknown>).Ebbinghaus = Ebbinghaus;
  (globalThis as unknown as Record<string, unknown>).computeEbbinghausCurve = computeEbbinghausCurve;
  (globalThis as unknown as Record<string, unknown>).renderEbbinghausCurve = renderEbbinghausCurve;
}

export default Ebbinghaus;
