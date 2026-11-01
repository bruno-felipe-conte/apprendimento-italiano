// ============================================================
// js/core/frequency.js — Italian 3k Lemma Frequency Index (F4)
// Milestone 1: Frequency Dataset & Helpers
// Zero external runtime dependencies (Vanilla JS/TS)
// ============================================================

/**
 * @typedef {'1k' | '2k' | '3k' | 'rare'} FrequencyBand
 *
 * @typedef {Object} FrequencyProfile
 * @property {number} totalTokens
 * @property {Record<FrequencyBand, number>} bandCounts
 * @property {Record<FrequencyBand, number>} bandPercentages
 * @property {number} coveredTokens
 * @property {number} coveragePct
 */

const AppFrequency = {
  _rankMap: new Map(),
  _words: [],
  _isReady: false,
  _storageKey: 'it_swr_frequenza_3000',

  /**
   * Inicializa o índice de forma síncrona a partir de dados pré-carregados.
   * Suporta formatos:
   * 1. Objeto com campo 'data' pipe-delimited (Schema canônico < 30 KB)
   * 2. Objeto com array 'parole' ou 'words'
   * 3. Array direto de strings
   *
   * @param {any} payload
   */
  init(payload) {
    if (!payload) return;

    let list = [];
    if (typeof payload === 'string') {
      list = payload.split('|');
    } else if (payload && typeof payload.data === 'string') {
      list = payload.data.split('|');
    } else if (payload && Array.isArray(payload.parole)) {
      list = payload.parole;
    } else if (payload && Array.isArray(payload.words)) {
      list = payload.words;
    } else if (Array.isArray(payload)) {
      list = payload;
    }

    if (!list || list.length === 0) return;

    this._rankMap.clear();
    this._words = new Array(list.length);

    for (let i = 0; i < list.length; i++) {
      const raw = list[i];
      if (!raw || typeof raw !== 'string') continue;

      const rank = i + 1;
      const normalized = raw.trim().toLowerCase();

      this._words[i] = normalized;
      this._rankMap.set(normalized, rank);

      // Índice defensivo para colocações com pontuação (ex: 'come stai?' -> 'come stai')
      const cleaned = normalized.replace(/[?!.,;:]/g, '').trim();
      if (cleaned && !this._rankMap.has(cleaned)) {
        this._rankMap.set(cleaned, rank);
      }
    }

    this._isReady = true;
  },

  /**
   * Carrega os dados de data/frequenza_3000.json com suporte offline SWR.
   * @param {string} [url='data/frequenza_3000.json']
   * @returns {Promise<boolean>}
   */
  async load(url = 'data/frequenza_3000.json') {
    // 1. Tentar hidratação imediata via SafeStorage SWR
    if (typeof SafeStorage !== 'undefined') {
      const cached = SafeStorage.getItem(this._storageKey);
      if (cached) {
        try {
          const parsed = typeof cached === 'string' ? JSON.parse(cached) : cached;
          this.init(parsed);
        } catch (_) {}
      }
    }

    // 2. Fetch de rede / Node.js filesystem fallback
    try {
      let data = null;
      if (typeof fetch !== 'undefined') {
        const resp = await fetch(url);
        if (resp.ok) {
          data = await resp.json();
        }
      } else if (typeof process !== 'undefined' && process.versions && process.versions.node) {
        // Ambiente Node.js (Vitest)
        const fs = await import('node:fs');
        const path = await import('node:path');
        const resolved = path.resolve(process.cwd(), url);
        if (fs.existsSync(resolved)) {
          data = JSON.parse(fs.readFileSync(resolved, 'utf-8'));
        }
      }

      if (data) {
        this.init(data);
        if (typeof SafeStorage !== 'undefined') {
          SafeStorage.setItem(this._storageKey, data);
        }
        return true;
      }
    } catch (e) {
      console.warn('[AppFrequency] Aviso ao carregar frequenza_3000.json:', e);
    }

    return this._isReady;
  },

  /**
   * Informa se o índice está hidratado e pronto para consultas O(1).
   * @returns {boolean}
   */
  isReady() {
    return this._isReady;
  },

  /**
   * Retorna o rank de frequência (1 a 3.000) do lema em tempo O(1).
   * Retorna null se a palavra não estiver no índice dos 3.000 mais frequentes.
   *
   * @param {string} lemma
   * @returns {number | null}
   */
  getRank(lemma) {
    if (!lemma || typeof lemma !== 'string') return null;
    const key = lemma.trim().toLowerCase();
    return this._rankMap.get(key) || null;
  },

  /**
   * Retorna o rank de frequência com fallback seguro para ordenação e cálculos numéricos.
   *
   * @param {string} lemma
   * @param {number} [fallback=Infinity]
   * @returns {number}
   */
  getRankSafe(lemma, fallback = Infinity) {
    const r = this.getRank(lemma);
    return r !== null ? r : fallback;
  },

  /**
   * Classifica o lema em uma das 4 faixas frequenciais pedagógicas:
   * - '1k': ranks 1–1.000 (A1/A2, funcional, cobre ~79% do texto autêntico)
   * - '2k': ranks 1.001–2.000 (A2/B1, vocabolario fondamentale de De Mauro, cobre ~87%)
   * - '3k': ranks 2.001–3.000 (B1/B2, vocabolario di alto uso, destrava 90%+)
   * - 'rare': ranks > 3.000 ou vocábulo ausente do índice
   *
   * @param {string} lemma
   * @returns {FrequencyBand}
   */
  getBand(lemma) {
    const rank = this.getRank(lemma);
    if (rank === null) return 'rare';
    if (rank <= 1000) return '1k';
    if (rank <= 2000) return '2k';
    if (rank <= 3000) return '3k';
    return 'rare';
  },

  /**
   * Predicado rápido: verifica se o lema pertence ao núcleo frequencial comum.
   *
   * @param {string} lemma
   * @param {number} [maxRank=3000]
   * @returns {boolean}
   */
  isCommon(lemma, maxRank = 3000) {
    const r = this.getRank(lemma);
    return r !== null && r <= maxRank;
  },

  /**
   * Retorna o lema canônico no rank especificado (1 a 3.000) em tempo O(1).
   *
   * @param {number} rank
   * @returns {string | null}
   */
  getLemmaAtRank(rank) {
    if (!Number.isInteger(rank) || rank < 1 || rank > this._words.length) {
      return null;
    }
    return this._words[rank - 1] || null;
  },

  /**
   * Retorna todos os lemas de uma faixa específica.
   *
   * @param {FrequencyBand} band
   * @returns {string[]}
   */
  getLemmasInBand(band) {
    if (band === '1k') return this._words.slice(0, 1000);
    if (band === '2k') return this._words.slice(1000, 2000);
    if (band === '3k') return this._words.slice(2000, 3000);
    return [];
  },

  /**
   * Retorna os limites numéricos [min, max] de uma faixa.
   *
   * @param {FrequencyBand} band
   * @returns {[number, number] | null}
   */
  getBandRange(band) {
    if (band === '1k') return [1, 1000];
    if (band === '2k') return [1001, 2000];
    if (band === '3k') return [2001, 3000];
    return null;
  },

  /**
   * Analisa um conjunto de lemas ou tokens de um texto e gera seu perfil frequencial completo.
   * Utilizado pelo CoverageMeter (F11) e Diagnóstico (F10).
   *
   * @param {string[]} tokens
   * @returns {FrequencyProfile}
   */
  getProfile(tokens) {
    const counts = { '1k': 0, '2k': 0, '3k': 0, 'rare': 0 };
    if (!Array.isArray(tokens) || tokens.length === 0) {
      return {
        totalTokens: 0,
        bandCounts: counts,
        bandPercentages: { '1k': 0, '2k': 0, '3k': 0, 'rare': 0 },
        coveredTokens: 0,
        coveragePct: 0
      };
    }

    for (let i = 0; i < tokens.length; i++) {
      const band = this.getBand(tokens[i]);
      counts[band]++;
    }

    const total = tokens.length;
    const covered = counts['1k'] + counts['2k'] + counts['3k'];

    return {
      totalTokens: total,
      bandCounts: counts,
      bandPercentages: {
        '1k': Math.round((counts['1k'] / total) * 10000) / 100,
        '2k': Math.round((counts['2k'] / total) * 10000) / 100,
        '3k': Math.round((counts['3k'] / total) * 10000) / 100,
        'rare': Math.round((counts['rare'] / total) * 10000) / 100
      },
      coveredTokens: covered,
      coveragePct: Math.round((covered / total) * 10000) / 100
    };
  },

  /**
   * Retorna uma amostra de N lemas aleatórios de uma determinada faixa.
   * Utilizado pelo VocabDiagnosticEngine (F10) para compor os testes adaptativos.
   *
   * @param {FrequencyBand} band
   * @param {number} count
   * @param {Function} [rng=Math.random]
   * @returns {string[]}
   */
  sampleBand(band, count, rng = Math.random) {
    const list = this.getLemmasInBand(band);
    if (!list || list.length === 0) return [];

    const n = Math.min(count, list.length);
    const shuffled = [...list];

    // Fisher-Yates partial shuffle
    for (let i = shuffled.length - 1; i > shuffled.length - 1 - n; i--) {
      const j = Math.min(i, Math.floor(rng() * (i + 1)));
      const temp = shuffled[i];
      shuffled[i] = shuffled[j];
      shuffled[j] = temp;
    }

    return shuffled.slice(shuffled.length - n);
  },

  /**
   * Total de lemas catalogados no índice (3.000).
   * @returns {number}
   */
  getTotal() {
    return this._words.length;
  }
};

// Universal Module Pattern
if (typeof globalThis !== 'undefined') {
  globalThis.AppFrequency = AppFrequency;
}
if (typeof window !== 'undefined') {
  window.AppFrequency = AppFrequency;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppFrequency;
}

