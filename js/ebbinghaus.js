/**
 * js/ebbinghaus.js
 * Proiezione matematica della Curva dell'Oblio (Ebbinghaus) basata su FSRS-4.5 / FSRS-5.
 * Compatibile con architettura Offline-First PWA (zero dipendenze esterne).
 */

const FSRS_DECAY = -0.5;
const FSRS_FACTOR = 19 / 81; // ~0.2345679 (garantisce R(S, S) = 0.90)

// Pesi ufficiali FSRS-4.5 per incremento di stabilità in revisione 'Buono' (Rating = 3)
const W8 = 1.54575;
const W9 = 0.1192;
const W10 = 1.01925;

const EBBINGHAUS_I18N = {
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
    legendNoReview: (s) => `Senza ripasso (S=${s})`,
    legendAfterGood: (s) => `Dopo 'Buono' (S=${s})`,
    ariaSummary: (sAtual, sBom, pct) =>
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
    legendNoReview: (s) => `Sem revisão (S=${s})`,
    legendAfterGood: (s) => `Após 'Bom' (S=${s})`,
    ariaSummary: (sAtual, sBom, pct) =>
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
    legendNoReview: (s) => `Without review (S=${s})`,
    legendAfterGood: (s) => `After 'Good' (S=${s})`,
    ariaSummary: (sAtual, sBom, pct) =>
      `Ebbinghaus Forgetting Curve chart. Target retention of ${pct}%. Current stability ${sAtual} and projected stability after Good of ${sBom}.`,
  },
};

/**
 * Stima la prossima stabilità S' dopo una revisione con voto "Buono" (Rating = 3)
 */
function predictNextStabilityGood(card, currentS) {
  if (!card) return Number(Math.max(currentS + 1, currentS * 2.5).toFixed(1));
  const dRaw = Number(card.difficulty);
  if (Number.isFinite(dRaw) && dRaw >= 1 && dRaw <= 10) {
    // Formula ufficiale di incremento stabilità FSRS-4.5 (a R ≈ 0.90)
    const r = 0.9;
    const gain =
      1 +
      Math.exp(W8) *
        (11 - dRaw) *
        Math.pow(Math.max(0.5, currentS), -W9) *
        (Math.exp(W10 * (1 - r)) - 1);
    const nextS = currentS * Math.max(1.5, gain);
    return Number(Math.max(currentS + 1, nextS).toFixed(1));
  }
  const ef = Math.max(1.3, Math.min(3.5, Number(card.ease_factor ?? card.ef ?? 2.5)));
  return Number(Math.max(currentS + 1, currentS * ef).toFixed(1));
}

function formatDaysLabel(d) {
  const rounded = Number(Number(d).toFixed(1));
  return Number.isInteger(rounded) ? `${rounded}d` : `${rounded.toFixed(1)}d`;
}

/**
 * Calcola tutti i dati matematici e i vettori SVG della Curva dell'Oblio
 */
function computeEbbinghausCurve(cards = [], activeCard = null, options = {}) {
  const retentionTarget = Math.max(
    0.7,
    Math.min(0.98, Number(options.desiredRetention) || 0.9)
  );
  const targetPct = Math.round(retentionTarget * 100);
  const curveMode = options.curveMode ?? 'fsrs-power';

  const yFromRetention = (r) => {
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
      pathAtual: '',
      pathBom: '',
      pointAtual: null,
      pointBom: null,
      sourceKey: 'empty',
    };
  }

  const extractS = (c) => {
    const raw = Number(c.stability ?? c.intervalo ?? c.scheduled_days ?? 0);
    return raw > 0 ? raw : 1;
  };

  let sAtual = 1;
  let sBom = 2.5;
  let sourceKey = 'deck_average';

  if (activeCard) {
    sAtual = Number(extractS(activeCard).toFixed(1));
    sBom = predictNextStabilityGood(activeCard, sAtual);
    sourceKey = 'focused';
  } else {
    const sumS = cards.reduce((acc, c) => acc + extractS(c), 0);
    sAtual = Number((sumS / cards.length).toFixed(1));
    const sumNext = cards.reduce((acc, c) => acc + predictNextStabilityGood(c, extractS(c)), 0);
    sBom = Number(Math.max(sAtual + 1, sumNext / cards.length).toFixed(1));
  }

  // Funzione di ritenzione R(t, S) e tempo esatto t in cui R(t, S) == retentionTarget
  const retentionAt = (t, s) => {
    const safeS = Math.max(0.2, s);
    if (curveMode === 'exponential') {
      return Math.pow(retentionTarget, t / safeS);
    }
    // Legge di potenza FSRS-4.5/5 calibrata affinché a t = tTarget(s), R = retentionTarget
    return Math.pow(1 + FSRS_FACTOR * (t / safeS), FSRS_DECAY);
  };

  const timeToTarget = (s) => {
    const safeS = Math.max(0.2, s);
    if (curveMode === 'exponential') return safeS;
    return (safeS / FSRS_FACTOR) * (Math.pow(retentionTarget, 1 / FSRS_DECAY) - 1);
  };

  const tTargetAtual = Number(timeToTarget(sAtual).toFixed(2));
  const tTargetBom = Number(timeToTarget(sBom).toFixed(2));
  const tMax = Math.max(5, tTargetBom * 1.22);

  const xStart = 38;
  const xEnd = 355;
  const xSpan = xEnd - xStart;

  const xFromT = (t) =>
    Number((xStart + Math.min(1, Math.max(0, t / tMax)) * xSpan).toFixed(1));

  const steps = 28;
  const buildPath = (s) => {
    const pts = [];
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
    pathAtual: buildPath(sAtual),
    pathBom: buildPath(sBom),
    pointAtual: { x: xFromT(tTargetAtual), y: targetY },
    pointBom: { x: xFromT(tTargetBom), y: targetY },
    sourceKey,
  };
}

/**
 * Renderizza la scheda della Curva dell'Oblio dentro qualsiasi HTMLElement della PWA
 * Pienamente conforme a WCAG 2.1 AA / Axe-core
 */
function renderEbbinghausCurve(container, cards = [], activeCard = null, options = {}) {
  if (!container) return null;
  const locale = options.locale || (typeof I18n !== 'undefined' ? I18n.currentLang : 'it') || 'it';
  const dict = EBBINGHAUS_I18N[locale] || EBBINGHAUS_I18N['it'];
  const data = computeEbbinghausCurve(cards, activeCard, options);

  const sourceText =
    data.sourceKey === 'focused'
      ? dict.sourceFocused
      : data.sourceKey === 'deck_average'
        ? dict.sourceDeck
        : dict.sourceEmpty;

  const uid = `eb-${Math.random().toString(36).slice(2, 8)}`;
  const xLabelAtual = Math.max(75, Math.min(200, (data.pointAtual?.x ?? 135) - 24));
  const xLabelBom = Math.max(205, Math.min(285, (data.pointBom?.x ?? 260) - 25));

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
            <text x="${xLabelAtual}" y="164" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">+${data.sAtualLabel} (${dict.currentS})</text>
            <text x="${xLabelBom}" y="164" fill="var(--it-eb-cypress)" font-size="9" font-family="monospace">+${data.sBomLabel} (${dict.goodS})</text>
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

// Esposizione per Browser, Node.js e moduli
const Ebbinghaus = {
  EBBINGHAUS_I18N,
  predictNextStabilityGood,
  formatDaysLabel,
  computeEbbinghausCurve,
  renderEbbinghausCurve
};

if (typeof window !== 'undefined') {
  window.Ebbinghaus = Ebbinghaus;
  window.computeEbbinghausCurve = computeEbbinghausCurve;
  window.renderEbbinghausCurve = renderEbbinghausCurve;
}

if (typeof globalThis !== 'undefined') {
  globalThis.Ebbinghaus = Ebbinghaus;
  globalThis.computeEbbinghausCurve = computeEbbinghausCurve;
  globalThis.renderEbbinghausCurve = renderEbbinghausCurve;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = Ebbinghaus;
}
