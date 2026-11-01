// ============================================================
// coverage_meter.js — Authentic Text Lexical Coverage Meter
// Laufer 95% Autonomous Reading Threshold & Top 5 Unlock Keys
// Feature F11 / Milestone 3: "O Espelho"
// ============================================================

const CoverageMeter = {
  /**
   * Obtém o conjunto normalizado de lemas/palavras que o usuário conhece.
   * Agrega palavras_conhecidas com cartas dominadas do FSRS.
   * @returns {Set<string>}
   */
  getUserKnownLemmas() {
    const conhecidas = new Set();

    if (typeof AppState !== 'undefined' && AppState.estado) {
      // 1. Palavras conhecidas explicitamente salvas
      const lista = AppState.estado.progresso?.palavras_conhecidas;
      if (Array.isArray(lista)) {
        lista.forEach(w => {
          if (typeof w === 'string') conhecidas.add(w.toLowerCase().trim());
        });
      }

      // 2. Flashcards com estabilidade ou repetições consolidadas
      const flashData = AppState.estado.flashcardData || {};
      Object.entries(flashData).forEach(([id, card]) => {
        if (card && (card.reps >= 2 || card.repeticoes >= 2 || card.stability >= 5.0)) {
          // Extrai termo limpo do id (ex: 't1_ciao' -> 'ciao')
          const termo = id.includes('_') ? id.split('_').slice(1).join('_') : id;
          if (termo) conhecidas.add(termo.toLowerCase().trim());
        }
      });
    }

    return conhecidas;
  },

  /**
   * Calcula a cobertura léxica real sobre os tokens de um texto autêntico.
   * @param {string[]} textTokens - Tokens extraídos pelo TextNormalizer
   * @param {Set<string>} userKnownLemmas - Set de palavras/lemas conhecidos
   * @returns {{
   *   coveragePct: number,
   *   unknownLemmas: string[],
   *   unlockKeys: Array<{lemma: string, count: number, impactPct: number}>,
   *   lauferGap: number,
   *   badgeColor: 'green' | 'yellow' | 'red'
   * }}
   */
  calculate(textTokens, userKnownLemmas) {
    if (!textTokens || !Array.isArray(textTokens) || textTokens.length === 0) {
      return {
        coveragePct: 0,
        unknownLemmas: [],
        unlockKeys: [],
        lauferGap: 95.0,
        badgeColor: 'red'
      };
    }

    const totalTokens = textTokens.length;
    let knownTokensCount = 0;
    const unknownFrequency = {};

    const normalizer = (typeof TextNormalizer !== 'undefined' && typeof TextNormalizer.toLemma === 'function')
      ? TextNormalizer
      : (typeof TextNormalizerEngine !== 'undefined' ? TextNormalizerEngine : null);

    const knownSet = userKnownLemmas || new Set();

    for (const token of textTokens) {
      const lower = String(token).toLowerCase().trim();
      const lemma = normalizer ? normalizer.toLemma(lower) : lower;

      if (knownSet.has(lemma) || knownSet.has(lower)) {
        knownTokensCount++;
      } else {
        unknownFrequency[lemma] = (unknownFrequency[lemma] || 0) + 1;
      }
    }

    const coveragePct = Number(((knownTokensCount / totalTokens) * 100).toFixed(1));
    const lauferGap = Number(Math.max(0, 95.0 - coveragePct).toFixed(1));

    const unlockKeys = Object.entries(unknownFrequency)
      .map(([lemma, count]) => ({
        lemma,
        count,
        impactPct: Number(((count / totalTokens) * 100).toFixed(1))
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);

    const badgeColor = coveragePct >= 95 ? 'green' : (coveragePct >= 80 ? 'yellow' : 'red');

    return {
      coveragePct,
      unknownLemmas: Object.keys(unknownFrequency),
      unlockKeys,
      lauferGap,
      badgeColor
    };
  },

  /**
   * Renderiza a badge visual de cobertura para ser inserida em canções e histórias.
   */
  renderBadgeHTML(coverageResult) {
    if (!coverageResult) return '';

    const corClasses = {
      green: 'badge-cobertura-verde',
      yellow: 'badge-cobertura-amarela',
      red: 'badge-cobertura-vermelha'
    };
    const corClass = corClasses[coverageResult.badgeColor] || 'badge-cobertura-vermelha';

    let icon = '🔴';
    if (coverageResult.badgeColor === 'green') icon = '🟢';
    else if (coverageResult.badgeColor === 'yellow') icon = '🟡';

    return `
      <div class="espelho-cobertura-badge ${corClass}" title="Limiar de Laufer: 95% para leitura autônoma sem dicionário">
        <span class="badge-icon">${icon}</span>
        <span class="badge-pct">${coverageResult.coveragePct}% de Cobertura</span>
        <span class="badge-gap">Lacuna Laufer: -${coverageResult.lauferGap}%</span>
      </div>
    `;
  },

  /**
   * Renderiza o card de chaves de desbloqueio ("Top 5 Unlock Keys").
   */
  renderUnlockKeysHTML(unlockKeys) {
    if (!Array.isArray(unlockKeys) || unlockKeys.length === 0) return '';

    return `
      <div class="espelho-unlock-keys-box">
        <h5 class="unlock-title">🔑 Chaves de Desbloqueio (Aprenda estas para maior salto de compreensão):</h5>
        <div class="unlock-chips-list">
          ${unlockKeys.map(k => `
            <span class="unlock-chip" title="Aparece ${k.count}x (+${k.impactPct}% de compreensão)">
              <strong>${k.lemma}</strong> <span class="chip-gain">+${k.impactPct}%</span>
            </span>
          `).join('')}
        </div>
      </div>
    `;
  }
};

// Exportação global e para testes
if (typeof window !== 'undefined') {
  window.CoverageMeter = CoverageMeter;
}
if (typeof globalThis !== 'undefined') {
  globalThis.CoverageMeter = CoverageMeter;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CoverageMeter;
}
