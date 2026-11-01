// js/production.js — Direct Text-Production Validator Engine (F6)
// Milestone 2: Cognitive Friction & Direct Active Production
// Zero external runtime dependencies (Vanilla JS/TS)
// ============================================================

/**
 * @typedef {Object} ValidationResult
 * @property {boolean} isCorrect - Se a resposta foi aceita (exata ou fuzzy)
 * @property {boolean} isFuzzy - Se foi aceita com tolerância de digitação
 * @property {number} distance - Distância de edição Levenshtein mínima
 * @property {string|null} diagnostic - Mensagem pedagógica explicativa ou de erro
 */

const ProductionValidator = {
  /**
   * Normaliza texto em italiano tratando acentos, apóstrofos e pontuações.
   * Mapeia acentos graves e agudos para 'vogal + apóstrofo' para garantir
   * equivalência bidirecional com digitação em teclados internacionais.
   *
   * @param {string} input - Texto bruto digitado
   * @returns {string} Texto normalizado em minúsculas
   */
  normalize(input) {
    if (input === null || input === undefined) return '';
    let s = String(input).trim().toLowerCase();
    if (!s) return '';

    // 1. Normaliza aspas e apóstrofos curvos/tipográficos para apóstrofo reto ASCII
    s = s.replace(/[’‘ʻʼ`´]/g, "'");

    // 2. Mapeamento de acentos italianos para convenção de apóstrofo
    s = s.replace(/è/g, "e'").replace(/é/g, "e'");
    s = s.replace(/à/g, "a'");
    s = s.replace(/ì/g, "i'");
    s = s.replace(/ò/g, "o'");
    s = s.replace(/ù/g, "u'");

    // 3. Compostos comuns com -ché / -chè
    s = s.replace(/perché|perchè/g, "perche'");
    s = s.replace(/poiché|poichè/g, "poiche'");
    s = s.replace(/affinché|affinchè/g, "affinche'");
    s = s.replace(/benché|benchè/g, "benche'");
    s = s.replace(/giacché|giacchè/g, "giacche'");
    s = s.replace(/finché|finchè/g, "finche'");

    // 4. Remove pontuação externa no início e no final (preserva apóstrofos internos)
    s = s.replace(/^[.,!?:;…«»"—–\s]+|[.,!?:;…«»"—–\s]+$/g, '').trim();

    // 5. Normaliza espaço pós-apóstrofo acidental inserido por teclados mobile em elisões
    s = s.replace(/\b([ldcn]|un|all|dell|nell|sull|dall)'\s+([a-z])/g, "$1'$2");

    // 6. Colapso de múltiplos espaços em branco
    return s.replace(/\s+/g, ' ');
  },

  /**
   * Calcula a distância de edição de Levenshtein entre duas strings normalizadas.
   * Utiliza matriz DP com espaço otimizado.
   *
   * @param {string} a - Primeira string
   * @param {string} b - Segunda string
   * @returns {number} Número mínimo de inserções, deleções ou substituições
   */
  levenshtein(a, b) {
    const s1 = this.normalize(a);
    const s2 = this.normalize(b);
    const m = s1.length;
    const n = s2.length;

    if (m === 0) return n;
    if (n === 0) return m;

    let prev = new Array(n + 1);
    let curr = new Array(n + 1);

    for (let j = 0; j <= n; j++) prev[j] = j;

    for (let i = 1; i <= m; i++) {
      curr[0] = i;
      const char1 = s1[i - 1];
      for (let j = 1; j <= n; j++) {
        if (char1 === s2[j - 1]) {
          curr[j] = prev[j - 1];
        } else {
          curr[j] = 1 + Math.min(prev[j], curr[j - 1], prev[j - 1]);
        }
      }
      for (let j = 0; j <= n; j++) prev[j] = curr[j];
    }

    return prev[n];
  },

  /**
   * Diagnostica erros gramaticais e morfológicos específicos da língua italiana:
   * 1. Troca ou omissão de artigos determinativos/indeterminativos.
   * 2. Erros de "doppie" (consoantes duplas omitidas ou adicionadas).
   * 3. Erros de desinência verbal (conjugação de pessoa/tempo incorreta).
   *
   * @param {string} input - Resposta digitada pelo usuário
   * @param {string} expected - Resposta correta esperada
   * @returns {string|null} Mensagem de diagnóstico ou null se não houver erro morfológico específico
   */
  diagnose(input, expected) {
    const normInput = this.normalize(input);
    const normExpected = this.normalize(expected);

    if (!normInput || !normExpected) return null;

    // ── 1. Diagnóstico de Artigos ──────────────────────────────
    const artReg = /^(il|lo|la|l'|i|gli|le|un|uno|una|un')(?:(?<=')|\s+)/;
    const inArt = normInput.match(artReg);
    const expArt = normExpected.match(artReg);

    if (inArt && expArt && inArt[1] !== expArt[1]) {
      return `Atenção ao artigo: esperava-se '${expArt[1]}', mas foi digitado '${inArt[1]}'.`;
    }

    // ── 2. Diagnóstico de Doppie (Consoantes Duplas) ────────────
    const getAllDoppie = (s) => (s.match(/([bcdfglmnpqrstvz])\1/g) || []);
    const expDoppie = getAllDoppie(normExpected);
    const inDoppie = getAllDoppie(normInput);

    // Verifica se as palavras são análogas retirando as consoantes duplas
    const collapseDoppie = (s) => s.replace(/([bcdfglmnpqrstvz])\1/g, '$1');
    const saoAnalogos = collapseDoppie(normInput) === collapseDoppie(normExpected) ||
                        this.levenshtein(collapseDoppie(normInput), collapseDoppie(normExpected)) <= 1;

    if (saoAnalogos) {
      for (const d of expDoppie) {
        if (!inDoppie.includes(d)) {
          return `Atenção à doppia: escreve-se com consoante dupla '${d}'!`;
        }
      }
      for (const d of inDoppie) {
        if (!expDoppie.includes(d)) {
          return `Atenção à doppia: '${normInput}' não possui consoante dupla '${d}' neste contexto.`;
        }
      }
    }

    // ── 3. Diagnóstico de Desinência Verbal ──────────────────────
    const desinencias = [
      'evamo', 'eremo', 'avamo', 'avate', 'erete',
      'iamo', 'ite', 'ete', 'ate', 'ano', 'ono', 'esti', 'ebbe'
    ];

    for (const d of desinencias) {
      if (normExpected.endsWith(d) && !normInput.endsWith(d)) {
        // Valida se compartilham radical inicial (mínimo 3 caracteres)
        const stemExp = normExpected.slice(0, -d.length);
        if (stemExp.length >= 3 && normInput.startsWith(stemExp.slice(0, 3))) {
          return `Atenção à desinência verbal: confira a conjugação para a pessoa correta.`;
        }
        // Se TextNormalizer estiver presente, valida via lema compartilhado
        if (typeof globalThis !== 'undefined' && globalThis.TextNormalizer?.toLemma) {
          try {
            const lemmaIn = globalThis.TextNormalizer.toLemma(normInput);
            const lemmaExp = globalThis.TextNormalizer.toLemma(normExpected);
            if (lemmaIn && lemmaExp && lemmaIn === lemmaExp) {
              return `Atenção à desinência verbal: confira a conjugação para a pessoa correta.`;
            }
          } catch (_) {}
        }
      }
    }

    return null;
  },

  /**
   * Valida uma entrada digitada contra a resposta esperada e suas variantes.
   *
   * @param {string} input - Texto produzido pelo estudante
   * @param {string} expected - Resposta principal esperada
   * @param {string[]} [variants=[]] - Lista opcional de variantes aceitas (sinônimos)
   * @returns {ValidationResult}
   */
  validate(input, expected, variants = []) {
    const normInput = this.normalize(input);
    const normExpected = this.normalize(expected);
    const normVariants = (variants || []).map((v) => this.normalize(v));

    // 1. Input vazio ou em branco
    if (!normInput) {
      return {
        isCorrect: false,
        isFuzzy: false,
        distance: normExpected ? normExpected.length : 0,
        diagnostic: 'Input vazio. Por favor, digite sua resposta.'
      };
    }

    // 2. Correspondência exata direta
    if (normInput === normExpected || normVariants.includes(normInput)) {
      return {
        isCorrect: true,
        isFuzzy: false,
        distance: 0,
        diagnostic: null
      };
    }

    // 3. Distâncias Levenshtein
    const distExp = this.levenshtein(normInput, normExpected);
    let minVariantDist = Infinity;
    let closestTarget = normExpected;

    for (let i = 0; i < normVariants.length; i++) {
      const v = normVariants[i];
      const d = this.levenshtein(normInput, v);
      if (d < minVariantDist) {
        minVariantDist = d;
        closestTarget = v;
      }
    }
    const dist = Math.min(distExp, minVariantDist);

    // 4. Verificação de diagnósticos morfológicos específicos PRIMEIRO
    const diag = this.diagnose(input, expected);
    if (diag) {
      return {
        isCorrect: false,
        isFuzzy: false,
        distance: dist,
        diagnostic: diag
      };
    }

    // 5. Tolerância Fuzzy Levenshtein (apenas se nenhum erro gramatical foi detectado)
    const len = closestTarget.length;
    const isFuzzy = (len >= 5 && dist === 1) || (len >= 8 && dist <= 2);

    if (isFuzzy) {
      return {
        isCorrect: true,
        isFuzzy: true,
        distance: dist,
        diagnostic: 'Quase lá! Pequeno erro de digitação aceito com tolerância.'
      };
    }

    // 6. Resposta incorreta estrita
    return {
      isCorrect: false,
      isFuzzy: false,
      distance: dist,
      diagnostic: `Resposta incorreta. Esperava-se '${expected}'.`
    };
  }
};

// Exportação universal (ESM + Globais para compatibilidade PWA e testes)
if (typeof window !== 'undefined') window.ProductionValidator = ProductionValidator;
if (typeof globalThis !== 'undefined') globalThis.ProductionValidator = ProductionValidator;

export default ProductionValidator;
export { ProductionValidator };
