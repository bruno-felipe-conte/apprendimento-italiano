/**
 * js/ebbinghaus.js
 * Proiezione matematica della Curva dell'Oblio (Ebbinghaus) basata su FSRS-4.5 / FSRS-5.
 * Compatibile con architettura Offline-First PWA (zero dipendenze esterne).
 * Pienamente allineato alle specifiche WCAG 2.1 AA / Axe-core.
 */

// Pesi ufficiali FSRS per incremento di stabilità in revisione 'Buono' (Rating = 3)
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
    modeRecent: '3 Recenti',
    modeAll: 'Tutti i Cicli',
    toggleTip: 'Tocca per alternare visualizzazione (3 Recenti / Tutti)',
    initialEncoding: 'Inizio',
    retrieval: 'Ripasso',
    lapseLabel: 'Oblio (85%)',
  },
  pt: {
    title: 'Curva de Esquecimento (Ebbinghaus)',
    subtitle: 'Projeção matemática de retenção baseada no FSRS-5',
    sourceEmpty: 'Sem cards cadastrados',
    sourceFocused: 'Card em foco',
    sourceDeck: 'Média do baralho',
    today: 'Hoje',
    currentS: 'S atual',
    goodS: 'Bom',
    emptyPrompt: 'Estude o 1º card para calcular a curva real',
    legendNoReview: (s) => `Sem revisão (S=${s})`,
    legendAfterGood: (s) => `Após 'Bom' (S=${s})`,
    ariaSummary: (sAtual, sBom, pct) =>
      `Gráfico da Curva de Esquecimento de Ebbinghaus. Meta de retenção de ${pct}%. Estabilidade atual de ${sAtual} e projeção após resposta Bom de ${sBom}.`,
    modeRecent: '3 Recentes',
    modeAll: 'Todos os Ciclos',
    toggleTip: 'Toque para alternar modo (3 Recentes / Todos)',
    initialEncoding: 'Início',
    retrieval: 'Revisão',
    lapseLabel: 'Lapso (85%)',
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
    modeRecent: '3 Recent',
    modeAll: 'All Cycles',
    toggleTip: 'Tap to toggle view (3 Recent / All)',
    initialEncoding: 'Initial',
    retrieval: 'Retrieval',
    lapseLabel: 'Lapse (85%)',
  },
};

/**
 * Funzione di ritenzione R(t, S)
 */
function calculateRetention(t, s, factor, decay, curveMode = 'fsrs-power', retentionTarget = 0.9) {
  const safeS = Math.max(0.2, s);
  if (curveMode === 'exponential') {
    return Math.pow(retentionTarget, t / safeS);
  }
  return Math.pow(1 + factor * (t / safeS), decay);
}

/**
 * Tempo t necessario affinché R(t, S) == retentionTarget
 */
function calculateTimeToTarget(s, factor, decay, curveMode = 'fsrs-power', retentionTarget = 0.9) {
  const safeS = Math.max(0.2, s);
  if (curveMode === 'exponential') return safeS;
  return (safeS / factor) * (Math.pow(retentionTarget, 1 / decay) - 1);
}

/**
 * Stima la prossima stabilità S' dopo una revisione con voto "Buono" (Rating = 3)
 */
function predictNextStabilityGood(card, currentS, currentR = 0.9) {
  if (!card) return Number(Math.max(currentS + 1, currentS * 2.5).toFixed(1));
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

function formatDaysLabel(d) {
  const rounded = Number(Number(d).toFixed(1));
  return Number.isInteger(rounded) ? `${rounded}d` : `${rounded.toFixed(1)}d`;
}

function getElapsedDays(card) {
  if (!card || card.last_review == null) return null;
  const lr = card.last_review;
  let timeMs;
  if (typeof lr === 'number') timeMs = lr;
  else if (lr instanceof Date) timeMs = lr.getTime();
  else if (typeof lr === 'string') timeMs = new Date(lr).getTime();
  else return null;

  if (Number.isNaN(timeMs) || timeMs <= 0) return null;
  const diffMs = Date.now() - timeMs;
  return Math.max(0, diffMs / 86400000);
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
  const effectiveCards = (Array.isArray(cards) && cards.length > 0)
    ? cards
    : (activeCard ? [activeCard] : []);
  if (effectiveCards.length === 0) {
    return {
      hasData: false,
      isCascade: false,
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
      cascadeSegments: [],
      cascadeArrows: [],
      cascadeLabels: [],
      viewMode: 'recent'
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
    const sumS = effectiveCards.reduce((acc, c) => acc + extractS(c), 0);
    sAtual = Number((sumS / effectiveCards.length).toFixed(1));
    const sumNext = effectiveCards.reduce((acc, c) => acc + predictNextStabilityGood(c, extractS(c)), 0);
    sBom = Number(Math.max(sAtual + 1, sumNext / effectiveCards.length).toFixed(1));
  }
  const rawW20 = options.w20 ?? options.fsrsDecay ?? 0.5;
  const clampedW20 = Math.max(0.1, Math.min(0.8, Number(rawW20) || 0.5));
  const decay = -clampedW20;
  const factor = Math.pow(0.9, 1 / decay) - 1;

  const retentionAt = (t, s) => {
    const safeS = Math.max(0.2, s);
    if (curveMode === 'exponential') {
      return Math.pow(retentionTarget, t / safeS);
    }
    return Math.pow(1 + factor * (t / safeS), decay);
  };
  const timeToTarget = (s) => {
    const safeS = Math.max(0.2, s);
    if (curveMode === 'exponential') return safeS;
    return (safeS / factor) * (Math.pow(retentionTarget, 1 / decay) - 1);
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
  // ── Construção da Cascata Multi-Ciclos (Ebbinghaus / FSRS) ──────────────
  const isCascade = !!activeCard;
  const history = (activeCard && Array.isArray(activeCard.history)) ? activeCard.history : [];
  const viewMode = options.cascadeMode || (typeof window !== 'undefined' && window._ebbinghausViewMode) || 'recent';
  const maxCycles = viewMode === 'all' ? history.length : Math.min(3, history.length);
  const displayedHistory = history.slice(history.length - maxCycles);
  const cascadeSegments = [];
  const cascadeArrows = [];
  const cascadeLabels = [];
  const palette = [
    'var(--it-eb-crimson, #C0392B)',
    'var(--it-eb-gold, #C27D2C)',
    'var(--it-eb-cypress, #3D7A4A)',
    '#2563EB',
    '#8B5CF6',
    '#06B6D4'
  ];
  const buildSegmentPath = (x0, x1, y0, stab, stepCount = 14) => {
    const pts = [];
    const span = x1 - x0;
    const startingR = 1.0 - ((y0 - 20) / 125) * 0.4;
    let lastY = y0;
    for (let i = 0; i <= stepCount; i++) {
      const frac = i / stepCount;
      const x = Number((x0 + frac * span).toFixed(1));
      const tNorm = frac * 2.5;
      const rDecay = Math.pow(1 + factor * (tNorm * 1.8 / Math.max(0.6, Math.log2(stab + 1.2))), decay);
      const currentR = startingR * rDecay;
      const y = yFromRetention(currentR);
      pts.push(`${i === 0 ? 'M' : 'L'} ${x} ${y}`);
      if (i === stepCount) lastY = y;
    }
    return { d: pts.join(' '), endY: lastY };
  };
  if (isCascade) {
    if (displayedHistory.length > 0) {
      const M = displayedHistory.length + 1;
      const segWidth = (xEnd - xStart) / M;
      // Segmento 0 (Initial)
      const s0 = displayedHistory[0].stabilityBefore || 1.0;
      const x0 = xStart;
      const x1 = Number((xStart + segWidth).toFixed(1));
      const seg0 = buildSegmentPath(x0, x1, 20, s0);
      cascadeSegments.push({
        id: 'seg-0',
        d: seg0.d,
        xStart: x0,
        yStart: 20,
        xEnd: x1,
        yEnd: seg0.endY,
        color: palette[0],
        label: 'Inizio',
        opacity: 0.95
      });
      cascadeLabels.push({ x: x0, text: 'Inizio', color: 'var(--it-eb-dim)', anchor: 'start' });
      let currentEndY = seg0.endY;
      // Ciclos de Retrieval com setas verticais para cima
      for (let k = 0; k < displayedHistory.length; k++) {
        const rec = displayedHistory[k];
        const rIndex = (history.length - displayedHistory.length) + k + 1;
        const arrowX = Number((xStart + (k + 1) * segWidth).toFixed(1));
        const isLapse = (rec.rating === 1);
        const yPeak = isLapse ? 66.9 : 20; // 85% para lapso, 100% para sucesso
        const arrowColor = isLapse ? 'var(--it-eb-crimson, #C0392B)' : 'var(--it-eb-cypress, #3D7A4A)';
        const marker = isLapse ? 'crimson' : 'cypress';
        cascadeArrows.push({
          x: arrowX,
          yFrom: currentEndY,
          yTo: yPeak,
          color: arrowColor,
          marker,
          label: `R${rIndex}`,
          isLapse,
          targetPeakPct: isLapse ? 85 : 100
        });
        cascadeLabels.push({
          x: arrowX,
          text: `R${rIndex}`,
          color: arrowColor,
          anchor: 'middle'
        });
        const xNext = Number((xStart + (k + 2) * segWidth).toFixed(1));
        const nextStab = rec.stabilityAfter || sAtual;
        const color = palette[(k + 1) % palette.length];
        const segNext = buildSegmentPath(arrowX, xNext, yPeak, nextStab);
        cascadeSegments.push({
          id: `seg-${k + 1}`,
          d: segNext.d,
          xStart: arrowX,
          yStart: yPeak,
          xEnd: xNext,
          yEnd: segNext.endY,
          color: color,
          label: `R${rIndex}`,
          opacity: (k === displayedHistory.length - 1) ? 1.0 : 0.85
        });
        currentEndY = segNext.endY;
      }
      cascadeLabels.push({
        x: xEnd,
        text: `+${formatDaysLabel(sBom)} (Buono)`,
        color: 'var(--it-eb-cypress)',
        anchor: 'end'
      });
    } else {
      // Card novo sem histórico: Initial Encoding e projeção da 1ª revisão
      const midX = 185;
      const seg0 = buildSegmentPath(xStart, midX, 20, sAtual);
      cascadeSegments.push({
        id: 'seg-init',
        d: seg0.d,
        xStart: xStart,
        yStart: 20,
        xEnd: midX,
        yEnd: seg0.endY,
        color: palette[0],
        label: 'Inizio',
        opacity: 0.95
      });
      cascadeArrows.push({
        x: midX,
        yFrom: seg0.endY,
        yTo: 20,
        color: 'var(--it-eb-cypress, #3D7A4A)',
        marker: 'cypress',
        label: 'R1',
        isLapse: false,
        isGhost: true,
        targetPeakPct: 100
      });
      const segProj = buildSegmentPath(midX, xEnd, 20, sBom);
      cascadeSegments.push({
        id: 'seg-proj',
        d: segProj.d,
        xStart: midX,
        yStart: 20,
        xEnd: xEnd,
        yEnd: segProj.endY,
        color: palette[2],
        label: 'Dopo Buono',
        opacity: 0.9,
        dash: '4 4'
      });
      cascadeLabels.push({ x: xStart, text: 'Oggi', color: 'var(--it-eb-dim)', anchor: 'start' });
      cascadeLabels.push({ x: midX, text: '+1d (R1)', color: 'var(--it-eb-cypress)', anchor: 'middle' });
      cascadeLabels.push({ x: xEnd, text: `+${formatDaysLabel(sBom)} (Buono)`, color: 'var(--it-eb-cypress)', anchor: 'end' });
    }
  }
  return {
    hasData: true,
    isCascade,
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
    cascadeSegments,
    cascadeArrows,
    cascadeLabels,
    viewMode,
    totalHistoryCount: history.length
  };
}

/**
 * Renderizza la Curva dell'Oblio (Ebbinghaus) nel container
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
  const toggleBtnHtml = (data.isCascade && data.totalHistoryCount > 3)
    ? `<button type="button" class="it-eb-mode-pill" onclick="Ebbinghaus.toggleMode(event)" title="${dict.toggleTip}">
         <span>${data.viewMode === 'all' ? dict.modeAll : dict.modeRecent}</span>
         <span style="opacity:0.6;font-size:9px">⮂</span>
       </button>`
    : '';
  let svgContentHtml = '';
  if (data.isCascade && data.cascadeSegments && data.cascadeSegments.length > 0) {
    let arrowsHtml = '';
    data.cascadeArrows.forEach(arrow => {
      arrowsHtml += `
        <line x1="${arrow.x}" y1="145" x2="${arrow.x}" y2="${arrow.yFrom}" stroke="var(--it-eb-border)" stroke-width="1" stroke-dasharray="3 3" opacity="0.6" />
        <line class="eb-arrow-animated" x1="${arrow.x}" y1="${arrow.yFrom}" x2="${arrow.x}" y2="${arrow.yTo}" stroke="${arrow.color}" stroke-width="2.5" ${arrow.isGhost ? 'stroke-dasharray="3 3"' : ''} marker-end="url(#eb-arrowhead-${arrow.marker})" />
        <circle cx="${arrow.x}" cy="${arrow.yTo}" r="3.5" fill="${arrow.color}" />
        <text x="${arrow.x}" y="13" text-anchor="middle" fill="${arrow.color}" font-size="9" font-weight="bold" font-family="monospace">${arrow.label}</text>
      `;
    });
    let segsHtml = '';
    data.cascadeSegments.forEach(seg => {
      segsHtml += `
        <path class="eb-curve-animated" d="${seg.d}" fill="none" stroke="${seg.color}" stroke-width="${seg.strokeWidth || 2.2}" opacity="${seg.opacity || 0.9}" ${seg.dash ? `stroke-dasharray="${seg.dash}"` : ''} />
        <circle cx="${seg.xStart}" cy="${seg.yStart}" r="3" fill="${seg.color}" />
      `;
    });
    let labelsHtml = '';
    data.cascadeLabels.forEach(lbl => {
      labelsHtml += `<text x="${lbl.x}" y="164" fill="${lbl.color || 'var(--it-eb-dim)'}" font-size="9" font-family="monospace" text-anchor="${lbl.anchor || 'middle'}">${lbl.text}</text>`;
    });
    svgContentHtml = `
      <defs>
        <marker id="eb-arrowhead-cypress" viewBox="0 0 10 10" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 10 L 5 0 L 10 10 z" fill="var(--it-eb-cypress, #3D7A4A)" />
        </marker>
        <marker id="eb-arrowhead-crimson" viewBox="0 0 10 10" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 10 L 5 0 L 10 10 z" fill="var(--it-eb-crimson, #C0392B)" />
        </marker>
      </defs>
      ${arrowsHtml}
      ${segsHtml}
      ${labelsHtml}
    `;
  } else if (data.hasData && data.pointAtual && data.pointBom) {
    svgContentHtml = `
      <path d="${data.pathAtual}" fill="none" stroke="var(--it-eb-crimson)" stroke-width="2" opacity="0.85" />
      <path d="${data.pathBom}" fill="none" stroke="var(--it-eb-cypress)" stroke-width="3" />
      <circle cx="38" cy="20" r="4" fill="var(--it-eb-cypress)" />
      <circle cx="${data.pointAtual.x}" cy="${data.pointAtual.y}" r="3.5" fill="var(--it-eb-crimson)" />
      <circle cx="${data.pointBom.x}" cy="${data.pointBom.y}" r="4.5" fill="var(--it-eb-gold)" />
      <text x="36" y="164" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">${dict.today}</text>
      <text x="${xLabelAtual}" y="164" fill="var(--it-eb-dim)" font-size="9" font-family="monospace">+${data.sAtualLabel} (${dict.currentS})</text>
      <text x="${xLabelBom}" y="164" fill="var(--it-eb-cypress)" font-size="9" font-family="monospace">+${data.sBomLabel} (${dict.goodS})</text>
    `;
  } else {
    svgContentHtml = `
      <text x="198" y="92" text-anchor="middle" fill="var(--it-eb-dim)" font-size="10" font-family="monospace">
        ${dict.emptyPrompt}
      </text>
    `;
  }
  container.innerHTML = `
    <section class="it-ebbinghaus-card it-ebbinghaus-interactive" aria-labelledby="${uid}-title" onclick="Ebbinghaus.toggleMode(event)" title="${dict.toggleTip}">
      <header class="it-ebbinghaus-header">
        <div>
          <h3 id="${uid}-title" class="it-ebbinghaus-title">${dict.title}</h3>
          <p class="it-ebbinghaus-subtitle">${dict.subtitle}</p>
        </div>
        <div style="display:flex;align-items:center;gap:0.35rem">
          ${toggleBtnHtml}
          <span class="it-ebbinghaus-badge">${sourceText}</span>
        </div>
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
          ${svgContentHtml}
        </svg>
        <footer class="it-ebbinghaus-legend">
          <span class="it-ebbinghaus-legend-item">
            <span class="it-ebbinghaus-dot" style="background:var(--it-eb-crimson)"></span>
            ${dict.initialEncoding || 'Inizio'}
          </span>
          <span class="it-ebbinghaus-legend-item">
            <span style="display:inline-block;transform:rotate(-90deg);font-size:11px;font-weight:bold;color:var(--it-eb-cypress)">➔</span>
            ${dict.retrieval || 'R'} (100%)
          </span>
          <span class="it-ebbinghaus-legend-item">
            <span class="it-ebbinghaus-dot" style="background:var(--it-eb-cypress)"></span>
            ${dict.legendAfterGood(data.sBomLabel)}
          </span>
        </footer>
      </div>
    </section>
  `;
  return data;
}

function toggleMode(event) {
  if (event && event.stopPropagation) event.stopPropagation();
  if (typeof window !== 'undefined') {
    window._ebbinghausViewMode = (window._ebbinghausViewMode === 'all') ? 'recent' : 'all';
    const container = document.getElementById('ebbinghaus-container');
    if (container && typeof Flashcards !== 'undefined' && typeof Flashcards.atualizarEbbinghaus === 'function') {
      Flashcards.atualizarEbbinghaus();
    }
  }
}

// Exportações para Browser e Node.js
if (typeof window !== 'undefined') {
  window.Ebbinghaus = {
    EBBINGHAUS_I18N,
    predictNextStabilityGood,
    formatDaysLabel,
    computeEbbinghausCurve,
    renderEbbinghausCurve,
    toggleMode
  };
  window.computeEbbinghausCurve = computeEbbinghausCurve;
  window.renderEbbinghausCurve = renderEbbinghausCurve;
}

if (typeof globalThis !== 'undefined') {
  globalThis.Ebbinghaus = {
    EBBINGHAUS_I18N,
    predictNextStabilityGood,
    formatDaysLabel,
    computeEbbinghausCurve,
    renderEbbinghausCurve,
    toggleMode
  };
  globalThis.computeEbbinghausCurve = computeEbbinghausCurve;
  globalThis.renderEbbinghausCurve = renderEbbinghausCurve;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    EBBINGHAUS_I18N,
    predictNextStabilityGood,
    formatDaysLabel,
    computeEbbinghausCurve,
    renderEbbinghausCurve,
    toggleMode
  };
}
