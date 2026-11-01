// ============================================================
// js/core/text_normalizer.js — Italian Text Normalizer Engine (F3)
// Milestone 1: Core Linguistic & Morphological Engine
// Zero external runtime dependencies (Vanilla JS/TS)
// ============================================================

/**
 * @typedef {Object} EncliticResult
 * @property {string} stem - O radical limpo ou infinitivo restaurado
 * @property {string|null} enclitic - O pronome enclítico descolado ou null
 */

/**
 * @typedef {Object} GulpeaseResult
 * @property {number} score - Pontuação normalizada [0, 100] (1 casa decimal)
 * @property {number} rawScore - Pontuação matemática pura da fórmula
 * @property {'molto_facile'|'facile'|'difficile'|'molto_difficile'} level - Nível de acessibilidade
 * @property {number} lp - Total de letras (Lettere nelle Parole)
 * @property {number} p - Total de palavras (Parole)
 * @property {number} fr - Total de frases (Frasi)
 * @property {string} interpretation - Interpretação educacional e escolar italiana
 */

const TextNormalizer = {
  // ── 1. Tabelas de Preposições Articuladas (32 formas canônicas) ──
  ARTICULATED_PREPOSITIONS: {
    // di + [il, lo, la, i, gli, le]
    'del': ['di', 'il'],
    'dello': ['di', 'lo'],
    'della': ['di', 'la'],
    'dei': ['di', 'i'],
    'degli': ['di', 'gli'],
    'delle': ['di', 'le'],

    // a + [il, lo, la, i, gli, le]
    'al': ['a', 'il'],
    'allo': ['a', 'lo'],
    'alla': ['a', 'la'],
    'ai': ['a', 'i'],
    'agli': ['a', 'gli'],
    'alle': ['a', 'le'],

    // da + [il, lo, la, i, gli, le]
    'dal': ['da', 'il'],
    'dallo': ['da', 'lo'],
    'dalla': ['da', 'la'],
    'dai': ['da', 'i'],
    'dagli': ['da', 'gli'],
    'dalle': ['da', 'le'],

    // in + [il, lo, la, i, gli, le]
    'nel': ['in', 'il'],
    'nello': ['in', 'lo'],
    'nella': ['in', 'la'],
    'nei': ['in', 'i'],
    'negli': ['in', 'gli'],
    'nelle': ['in', 'le'],

    // su + [il, lo, la, i, gli, le]
    'sul': ['su', 'il'],
    'sullo': ['su', 'lo'],
    'sulla': ['su', 'la'],
    'sui': ['su', 'i'],
    'sugli': ['su', 'gli'],
    'sulle': ['su', 'le'],

    // con + [il, i] (formas canônicas/coloquiais 31 e 32)
    'col': ['con', 'il'],
    'coi': ['con', 'i'],

    // Variantes adicionais literárias/antigas
    'collo': ['con', 'lo'],
    'colla': ['con', 'la'],
    'cogli': ['con', 'gli'],
    'colle': ['con', 'le'],
    'pel': ['per', 'il'],
    'pei': ['per', 'i']
  },

  // Preposições articuladas elididas (seguidas de apóstrofo)
  ELIDED_PREPOSITIONS: {
    'dell': ['di', 'il'],
    'all': ['a', 'il'],
    'dall': ['da', 'il'],
    'nell': ['in', 'il'],
    'sull': ['su', 'il']
  },

  // Prefixos elididos comuns (artigos, pronomes, advérbios)
  ELIDED_PREFIXES: {
    'l': 'il',
    'un': 'una',
    'c': 'ci',
    'd': 'di',
    'm': 'mi',
    't': 'ti',
    's': 'si',
    'v': 'vi',
    'n': 'ne',
    'ch': 'che',
    'gl': 'gli',
    'dov': 'dove',
    'com': 'come',
    'qual': 'quale',
    'quant': 'quanto',
    'tutt': 'tutto',
    'senz': 'senza',
    'bell': 'bello',
    'grand': 'grande',
    'sant': 'santo',
    'buon': 'buono',
    'pover': 'povero'
  },

  // ── 2. Dicionário Exato de Apócopes (Troncamento) ──
  APOCOPE_EXACT: {
    'bel': 'bello',
    'gran': 'grande',
    'san': 'santo',
    'buon': 'buono',
    'ben': 'bene',
    'mal': 'male',
    'man': 'mano',
    'qual': 'quale',
    'tal': 'tale',
    'quel': 'quello',
    'nessun': 'nessuno',
    'alcun': 'alcuno',
    'ciascun': 'ciascuno',
    "po'": 'poco',
    'po': 'poco',
    "fa'": 'fare',
    "da'": 'dare',
    "di'": 'dire',
    "sta'": 'stare',
    "va'": 'andare',
    "be'": 'bene',
    "mo'": 'modo',
    'son': 'sono',
    'fan': 'fanno',
    'dan': 'danno',
    'van': 'vanno',
    'far': 'fare',
    'han': 'hanno'
  },

  // Exceções que terminam em -ar/-er/-ir/-or e NÃO são apócopes italianas
  APOCOPE_EXCEPTIONS: new Set([
    'per', 'bar', 'computer', 'leader', 'laser', 'super', 'sponsor', 'humor',
    'junior', 'senior', 'horror', 'inter', 'noir', 'premier', 'master',
    'tour', 'star', 'partner', 'killer', 'cluster', 'server', 'browser'
  ]),

  // ── 3. Pronomes Enclíticos (Simples e Combinados) ──
  ENCLITICS: [
    // Combinados (ordem decrescente de comprimento para matching guloso)
    'glielo', 'gliela', 'glieli', 'gliele', 'gliene',
    'melo', 'mela', 'meli', 'mele', 'mene',
    'telo', 'tela', 'teli', 'tele', 'tene',
    'selo', 'sela', 'seli', 'sele', 'sene',
    'celo', 'cela', 'celi', 'cele', 'cene',
    'velo', 'vela', 'veli', 'vele', 'vene',
    // Simples
    'gli', 'mi', 'ti', 'si', 'ci', 'vi', 'lo', 'la', 'li', 'le', 'ne'
  ],

  // Imperativos monossilábicos com raddoppiamento sintattico
  MONO_IMPERATIVES: {
    'dammi': { stem: "da'", enclitic: 'mi' },
    'dallo': { stem: "da'", enclitic: 'lo' },
    'dalla': { stem: "da'", enclitic: 'la' },
    'dalli': { stem: "da'", enclitic: 'li' },
    'dalle': { stem: "da'", enclitic: 'le' },
    'dagli': { stem: "da'", enclitic: 'gli' },
    'dammelo': { stem: "da'", enclitic: 'melo' },
    'dimmi': { stem: "di'", enclitic: 'mi' },
    'dillo': { stem: "di'", enclitic: 'lo' },
    'dilla': { stem: "di'", enclitic: 'la' },
    'dilli': { stem: "di'", enclitic: 'li' },
    'dille': { stem: "di'", enclitic: 'le' },
    'digli': { stem: "di'", enclitic: 'gli' },
    'dimmelo': { stem: "di'", enclitic: 'melo' },
    'dirmelo': { stem: 'dire', enclitic: 'melo' },
    'fammi': { stem: "fa'", enclitic: 'mi' },
    'fallo': { stem: "fa'", enclitic: 'lo' },
    'falla': { stem: "fa'", enclitic: 'la' },
    'falli': { stem: "fa'", enclitic: 'li' },
    'falle': { stem: "fa'", enclitic: 'le' },
    'fagli': { stem: "fa'", enclitic: 'gli' },
    'fammelo': { stem: "fa'", enclitic: 'melo' },
    'vammi': { stem: "va'", enclitic: 'mi' },
    'vacci': { stem: "va'", enclitic: 'ci' },
    'stammi': { stem: "sta'", enclitic: 'mi' },
    'stacci': { stem: "sta'", enclitic: 'ci' }
  },

  // Guarda rigorosa contra falsos positivos: palavras autônomas que terminam com sílabas de clíticos
  NON_ENCLITIC_WORDS: new Set([
    'carne', 'pane', 'cane', 'fine', 'sole', 'miele', 'stelo', 'isola', 'vela', 'tela',
    'vitale', 'iniziale', 'facile', 'difficile', 'possibile', 'visibile', 'gentile', 'fedele',
    'amici', 'nemici', 'edifici', 'stoici', 'medici', 'sindaci', 'portici', 'uffici', 'benefici',
    'giornale', 'canale', 'ospedale', 'animale',
    'parla', 'parli', 'dice', 'aperti', 'certi', 'esterni', 'esterne', 'limi', 'peli',
    'simile', 'chiavi', 'frasi', 'crisi', 'quasi', 'motivi', 'archivi', 'politici', 'simili', 'brindisi'
  ]),

  // Palavras invariáveis e advérbios que terminam em -i ou -e e não devem sofrer desinência de plural
  INVARIABLE_WORDS: new Set([
    'quasi', 'ieri', 'domani', 'oggi', 'qui', 'lì', 'fuori', 'davanti', 'dietro',
    'crisi', 'analisi', 'tesi', 'ipotesi', 'sintesi', 'oasi', 'enfasi', 'diocesi', 'metropoli',
    'brindisi', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì',
    'tuttavia', 'così', 'meglio', 'peggio', 'poco', 'tanto', 'troppo',
    'sempre', 'spesso', 'mai', 'ancora', 'già', 'presto', 'tardi', 'subito', 'poi', 'infine'
  ]),

  // Dicionário embutido de verbos irregulares fundamentais (garantia de bootstrap zero-network)
  _coreVerbs: new Map([
    // essere
    ['sono', 'essere'], ['sei', 'essere'], ['è', 'essere'], ['e\'', 'essere'],
    ['siamo', 'essere'], ['siete', 'essere'],
    ['ero', 'essere'], ['eri', 'essere'], ['era', 'essere'], ['eravamo', 'essere'],
    ['eravate', 'essere'], ['erano', 'essere'],
    ['sarò', 'essere'], ['sarai', 'essere'], ['sarà', 'essere'], ['saremo', 'essere'],
    ['sarete', 'essere'], ['saranno', 'essere'],
    ['sia', 'essere'], ['siate', 'essere'], ['siano', 'essere'],
    ['stato', 'essere'], ['stata', 'essere'], ['stati', 'essere'], ['state', 'essere'],
    // avere
    ['ho', 'avere'], ['hai', 'avere'], ['ha', 'avere'], ['abbiamo', 'avere'],
    ['avete', 'avere'], ['hanno', 'avere'],
    ['avevo', 'avere'], ['avevi', 'avere'], ['aveva', 'avere'], ['avevamo', 'avere'],
    ['avevate', 'avere'], ['avevano', 'avere'],
    ['avrò', 'avere'], ['avrai', 'avere'], ['avrà', 'avere'], ['avremo', 'avere'],
    ['avrete', 'avere'], ['avranno', 'avere'],
    ['abbia', 'avere'], ['abbiate', 'avere'], ['abbiano', 'avere'],
    ['avuto', 'avere'], ['avuta', 'avere'], ['avuti', 'avere'], ['avute', 'avere'],
    // andare
    ['vado', 'andare'], ['vai', 'andare'], ['va', 'andare'], ['andiamo', 'andare'],
    ['andate', 'andare'], ['vanno', 'andare'],
    ['andavo', 'andare'], ['andavi', 'andare'], ['andava', 'andare'],
    ['andavamo', 'andare'], ['andavate', 'andare'], ['andavano', 'andare'],
    ['andrò', 'andare'], ['andrai', 'andare'], ['andrà', 'andare'],
    ['andremo', 'andare'], ['andrete', 'andare'], ['andranno', 'andare'],
    ['vada', 'andare'], ['vadano', 'andare'],
    ['andato', 'andare'], ['andata', 'andare'], ['andati', 'andare'], ['andate', 'andare'],
    // fare
    ['faccio', 'fare'], ['fai', 'fare'], ['fa', 'fare'], ['facciamo', 'fare'],
    ['fate', 'fare'], ['fanno', 'fare'],
    ['facevo', 'fare'], ['facevi', 'fare'], ['faceva', 'fare'],
    ['facevamo', 'fare'], ['facevate', 'fare'], ['facevano', 'fare'],
    ['farò', 'fare'], ['farai', 'fare'], ['farà', 'fare'],
    ['faremo', 'fare'], ['farete', 'fare'], ['faranno', 'fare'],
    ['faccia', 'fare'], ['facciano', 'fare'],
    ['fatto', 'fare'], ['fatta', 'fare'], ['fatti', 'fare'], ['fatte', 'fare'],
    // dire
    ['dico', 'dire'], ['dici', 'dire'], ['dice', 'dire'], ['diciamo', 'dire'],
    ['dite', 'dire'], ['dicono', 'dire'],
    ['dicevo', 'dire'], ['dicevi', 'dire'], ['diceva', 'dire'],
    ['dicevamo', 'dire'], ['dicevate', 'dire'], ['dicevano', 'dire'],
    ['dirò', 'dire'], ['dirai', 'dire'], ['dirà', 'dire'],
    ['diremo', 'dire'], ['direte', 'dire'], ['diranno', 'dire'],
    ['dica', 'dire'], ['dicano', 'dire'],
    ['detto', 'dire'], ['detta', 'dire'], ['detti', 'dire'], ['dette', 'dire'],
    // venire
    ['vengo', 'venire'], ['vieni', 'venire'], ['viene', 'venire'], ['veniamo', 'venire'],
    ['venite', 'venire'], ['vengono', 'venire'],
    ['venivo', 'venire'], ['venivi', 'venire'], ['veniva', 'venire'],
    ['venuto', 'venire'], ['venuta', 'venire'], ['venuti', 'venire'], ['venute', 'venire'],
    // potere, volere, dovere
    ['posso', 'potere'], ['puoi', 'potere'], ['può', 'potere'], ['possiamo', 'potere'], ['potete', 'potere'], ['possono', 'potere'],
    ['potevo', 'potere'], ['potuto', 'potere'],
    ['voglio', 'volere'], ['vuoi', 'volere'], ['vuole', 'volere'], ['vogliamo', 'volere'], ['volete', 'volere'], ['vogliono', 'volere'],
    ['volevo', 'volere'], ['voluto', 'volere'],
    ['devo', 'dovere'], ['devi', 'dovere'], ['deve', 'dovere'], ['dobbiamo', 'dovere'], ['dovete', 'dovere'], ['devono', 'dovere'],
    ['dovevo', 'dovere'], ['dovuto', 'dovere']
  ]),

  // Mapas de lookup hidratados em memória
  _verbMap: new Map(),
  _pluralMap: new Map(),
  _templeWords: new Set(),
  _initialized: false,

  /**
   * Inicializa o motor morfológico com dados do AppState ou parâmetros externos.
   * @param {Object} [options]
   */
  init(options = {}) {
    if (this._verbMap.size === 0) {
      // Carrega verbos core embutidos
      for (const [k, v] of this._coreVerbs) {
        this._verbMap.set(k, v);
      }
    }

    // Se conjugacoesData existir no contexto global (AppState), hidrata automaticamente
    if (typeof AppState !== 'undefined' && AppState.estado) {
      if (Array.isArray(AppState.estado.conjugacoesData) && AppState.estado.conjugacoesData.length > 0) {
        this.loadConjugations(AppState.estado.conjugacoesData);
      }
      if (Array.isArray(AppState.estado.vocabCache) && AppState.estado.vocabCache.length > 0) {
        this.loadPlurals(AppState.estado.vocabCache);
      }
    }

    if (options.conjugations) {
      this.loadConjugations(options.conjugations);
    }
    if (options.plurals) {
      this.loadPlurals(options.plurals);
    }

    this._initialized = true;
  },

  /**
   * Carrega e indexa formas verbais flexionadas a partir do formato conjugacoes.json.
   * @param {Array<Object>|Object} data
   */
  loadConjugations(data) {
    const verbList = Array.isArray(data) ? data : (data && data.verbos) ? data.verbos : [];
    for (const v of verbList) {
      if (!v || !v.infinitivo) continue;
      const inf = v.infinitivo.toLowerCase().trim();
      this._verbMap.set(inf, inf);

      // Particípio
      if (v.participio) {
        for (const p of String(v.participio).split('/')) {
          const cleanP = p.trim().toLowerCase();
          if (cleanP && !this._verbMap.has(cleanP)) {
            this._verbMap.set(cleanP, inf);
          }
        }
      }

      // Tempos simples e compostos
      if (v.tempos && typeof v.tempos === 'object') {
        for (const [tempo, pessoas] of Object.entries(v.tempos)) {
          if (!pessoas || typeof pessoas !== 'object') continue;

          if (tempo === 'Passato prossimo') {
            // Em tempos compostos, apenas o particípio pertence a este verbo
            for (const forma of Object.values(pessoas)) {
              if (typeof forma !== 'string') continue;
              for (const f of forma.split('/')) {
                const parts = f.trim().toLowerCase().split(/\s+/);
                const part = parts[parts.length - 1];
                if (part && !this._verbMap.has(part)) {
                  this._verbMap.set(part, inf);
                }
              }
            }
          } else {
            // Tempos simples (Presente, Imperfetto, Futuro, Congiuntivo presente)
            for (const forma of Object.values(pessoas)) {
              if (typeof forma !== 'string') continue;
              for (const f of forma.split('/')) {
                const w = f.trim().toLowerCase();
                if (w && !this._verbMap.has(w)) {
                  this._verbMap.set(w, inf);
                }
              }
            }
          }
        }
      }
    }
  },

  /**
   * Carrega e indexa plurais e palavras conhecidas a partir de itens de templo.
   * @param {Array<Object>|Record<string, string>} items
   */
  loadPlurals(items) {
    if (Array.isArray(items)) {
      for (const p of items) {
        if (!p) continue;
        const it = p.italiano ? p.italiano.toLowerCase().trim() : '';
        if (it) this._templeWords.add(it);

        const pl = p.plural ? p.plural.toLowerCase().trim() : '';
        if (pl && pl !== '-' && pl !== it) {
          for (const singlePl of pl.split('/')) {
            const cleanPl = singlePl.trim();
            if (cleanPl && cleanPl !== it) {
              this._pluralMap.set(cleanPl, it);
            }
          }
        }
      }
    } else if (items && typeof items === 'object') {
      for (const [pl, sg] of Object.entries(items)) {
        this._pluralMap.set(String(pl).toLowerCase().trim(), String(sg).toLowerCase().trim());
      }
    }
  },

  /**
   * Tokeniza o texto em palavras italianas, preservando acentuação, elisões internas
   * e apóstrofes apocópicas (po', fa'), ignorando pontuações e aspas externas.
   * @param {string} text - Texto italiano
   * @param {Object} [options] - Opções de tokenização
   * @param {boolean} [options.lowercase=false] - Se true, converte todos os tokens para minúsculas
   * @returns {string[]} Lista de tokens de palavras
   */
  tokenize(text, options = {}) {
    if (!text || typeof text !== 'string') return [];

    // Normaliza apóstrofe tipográfica U+2019 e crase para apóstrofe simples ASCII
    const normalized = text.replace(/[’‘`]/g, "'");

    // Regex para palavras italianas com acentos:
    // Captura palavras com apóstrofe interna (l'amico, dell'acqua) OU palavras com apóstrofe apocópica final (po', fa')
    const pattern = /[a-zA-Z\u00C0-\u024F]+'[a-zA-Z\u00C0-\u024F]+|[a-zA-Z\u00C0-\u024F]+'|[a-zA-Z\u00C0-\u024F]+/g;
    const rawMatches = normalized.match(pattern) || [];

    // Limpa aspas externas espúrias de citações (ex: "'ciao'" -> "ciao")
    const cleanTokens = [];
    for (let t of rawMatches) {
      // Se tiver apóstrofe no início, remove
      if (t.startsWith("'") && t.length > 1) {
        t = t.substring(1);
      }
      // Se tiver apóstrofe no final e não for uma palavra apocópica conhecida (po', fa', etc.), remove
      if (t.endsWith("'") && t.length > 1) {
        const lower = t.toLowerCase();
        if (!this.APOCOPE_EXACT[lower] && lower !== "po'" && lower !== "fa'" && lower !== "da'" && lower !== "di'" && lower !== "sta'" && lower !== "va'") {
          t = t.slice(0, -1);
        }
      }
      if (t.length > 0) {
        cleanTokens.push(options.lowercase ? t.toLowerCase() : t);
      }
    }

    return cleanTokens;
  },

  /**
   * Descompacta preposições articuladas (del -> [di, il]) e palavras com elisão (l'amico -> [il, amico]).
   * @param {string} word - Palavra ou token elidido
   * @returns {string[]} Lista de tokens constituintes
   */
  unpackElisions(word) {
    if (!word || typeof word !== 'string') return [];
    const clean = word.toLowerCase().trim().replace(/[’‘`]/g, "'");
    if (!clean) return [];

    // 1. Preposição articulada não-elidida direta (del, nello, alla, etc.)
    if (this.ARTICULATED_PREPOSITIONS[clean]) {
      return [...this.ARTICULATED_PREPOSITIONS[clean]];
    }

    // 2. Token contendo apóstrofe
    const apoIdx = clean.indexOf("'");
    if (apoIdx !== -1) {
      const prefix = clean.substring(0, apoIdx);
      const suffix = clean.substring(apoIdx + 1);

      // 2a. Preposições articuladas elididas (dell'acqua -> [di, il, acqua])
      if (this.ELIDED_PREPOSITIONS[prefix]) {
        const prepArticles = this.ELIDED_PREPOSITIONS[prefix];
        return suffix ? [...prepArticles, suffix] : [...prepArticles];
      }

      // 2b. Prefixos elididos canônicos (l'amico -> [il, amico], un'ora -> [una, ora])
      if (this.ELIDED_PREFIXES[prefix]) {
        const expandedPrefix = this.ELIDED_PREFIXES[prefix];
        return suffix ? [expandedPrefix, suffix] : [expandedPrefix];
      }

      // 2c. Apócope com apóstrofe no final (un po', fa', da')
      if (!suffix && this.APOCOPE_EXACT[clean]) {
        return [this.APOCOPE_EXACT[clean]];
      }

      // 2d. Fallback para apóstrofe genérica dividindo prefixo e sufixo
      if (prefix && suffix) {
        return [prefix, suffix];
      }
    }

    return [clean];
  },

  /**
   * Restaura palavras poéticas ou coloquiais que sofreram apócope (troncamento).
   * Ex: 'morir' -> 'morire', 'invasor' -> 'invasore', 'bel' -> 'bello', "po'" -> 'poco'.
   * @param {string} word - Palavra italiana
   * @returns {string} Palavra canônica restaurada
   */
  restoreApocope(word) {
    if (!word || typeof word !== 'string') return '';
    const clean = word.toLowerCase().trim().replace(/[’‘`]/g, "'");
    if (!clean) return '';

    // 1. Tabela exata de apócopes canônicas
    if (this.APOCOPE_EXACT[clean]) {
      return this.APOCOPE_EXACT[clean];
    }

    // 2. Guarda contra palavras estrangeiras e preposições (per, bar, etc.)
    if (this.APOCOPE_EXCEPTIONS.has(clean)) {
      return clean;
    }

    // 3. Infinitivos poéticos terminados em -ar, -er, -ir (min 4 letras: morir -> morire, andar -> andare)
    if (clean.length >= 4 && (clean.endsWith('ar') || clean.endsWith('er') || clean.endsWith('ir'))) {
      return clean + 'e';
    }

    // 4. Substantivos e adjetivos poéticos em -or (min 4 letras: invasor -> invasore, amor -> amore)
    if (clean.length >= 4 && clean.endsWith('or')) {
      return clean + 'e';
    }

    return clean;
  },

  /**
   * Descola pronomes enclíticos acoplados a infinitivos, gerúndios ou imperativos,
   * preservando palavras autônomas que terminam em sílabas idênticas (carne, sole, vitale).
   * @param {string} word - Palavra italiana
   * @returns {EncliticResult} Radical e pronome descolado
   */
  stripEnclitics(word) {
    if (!word || typeof word !== 'string') return { stem: '', enclitic: null };
    const clean = word.toLowerCase().trim().replace(/[’‘`]/g, "'");
    if (!clean) return { stem: '', enclitic: null };

    // 1. Imperativos monossilábicos com raddoppiamento sintattico (dimmi, dammi, fammi)
    if (this.MONO_IMPERATIVES[clean]) {
      return { ...this.MONO_IMPERATIVES[clean] };
    }

    // 2. Guarda contra falsos positivos (substantivos e adjetivos que não são verbos)
    if (this.NON_ENCLITIC_WORDS.has(clean)) {
      return { stem: clean, enclitic: null };
    }

    // 3. Varre pronomes enclíticos (combinados e simples)
    for (const enc of this.ENCLITICS) {
      if (clean.endsWith(enc) && clean.length > enc.length + 2) {
        const rawStem = clean.slice(0, -enc.length);

        // Caso A: Gerúndio (terminado em -ando ou -endo)
        if (rawStem.endsWith('ando') || rawStem.endsWith('endo')) {
          return { stem: rawStem, enclitic: enc };
        }

        // Caso B: Infinitivo (radical termina em vogal + r: veder-lo -> vedere, parlar-gli -> parlare)
        if (rawStem.length >= 3 && rawStem.endsWith('r') && /[aeiou]/.test(rawStem[rawStem.length - 2])) {
          return { stem: rawStem + 'e', enclitic: enc };
        }

        // Caso C: Imperativo regular (terminado em -a ou -i: porta-mi, prendi-lo)
        if (rawStem.length >= 3 && (rawStem.endsWith('a') || rawStem.endsWith('i'))) {
          return { stem: rawStem, enclitic: enc };
        }

        // Caso D: Imperativo voi (terminado em -te: ascoltate-mi, guardate-lo)
        if (rawStem.length >= 4 && rawStem.endsWith('te')) {
          return { stem: rawStem, enclitic: enc };
        }
      }
    }

    return { stem: clean, enclitic: null };
  },

  /**
   * Converte uma forma flexionada italiana para seu lema canônico no dicionário.
   * Consulta o acervo de conjugações (data/conjugacoes.json), tabela de plurais e regras regulares.
   * @param {string} word - Palavra italiana
   * @returns {string} Lema canônico
   */
  toLemma(word) {
    if (!word || typeof word !== 'string') return '';
    let clean = word.toLowerCase().trim().replace(/[’‘`]/g, "'");
    if (!clean) return '';

    // Artigos / pronomes canônicos
    if (clean === 'una' || clean === 'un') return 'uno';

    // Se a palavra contém apócope, restaura primeiro (morir -> morire, bel -> bello)
    clean = this.restoreApocope(clean);

    // Formas invariáveis, advérbios e substantivos que não sofrem flexão (quasi, ieri, crisi, ecc.)
    if (this.INVARIABLE_WORDS.has(clean)) {
      return clean;
    }

    // 1. Busca no mapa de flexões verbais indexadas
    if (this._verbMap.has(clean)) {
      return this._verbMap.get(clean);
    }

    // 2. Busca no mapa de plurais dos templos
    if (this._pluralMap.has(clean)) {
      return this._pluralMap.get(clean);
    }

    // 3. Se já for lema exato nos templos
    if (this._templeWords.has(clean)) {
      return clean;
    }

    // 4. Advérbios regulares em -mente (lentamente -> lento, facilmente -> facile)
    if (clean.endsWith('mente') && clean.length > 7) {
      const base = clean.slice(0, -5);
      if (this._templeWords.has(base)) return base;
      if (base.endsWith('a') && this._templeWords.has(base.slice(0, -1) + 'o')) {
        return base.slice(0, -1) + 'o';
      }
      if (this._templeWords.has(base + 'e')) return base + 'e';
      return base.endsWith('a') ? base.slice(0, -1) + 'o' : base;
    }

    // 5. Superlativos regulares em -issimo/a/i/e (bravissimo -> bravo, bellissima -> bello)
    if (/issim[oaie]$/.test(clean) && clean.length > 7) {
      const stem = clean.slice(0, -6);
      if (this._templeWords.has(stem + 'o')) return stem + 'o';
      if (this._templeWords.has(stem + 'e')) return stem + 'e';
      return stem + 'o';
    }

    // 6. Se for verbo com pronome enclítico, descola (portami -> porta -> portare, vederlo -> vedere, dimmi -> dire)
    const encliticCheck = this.stripEnclitics(clean);
    if (encliticCheck.enclitic !== null) {
      const stem = this.restoreApocope(encliticCheck.stem);
      if (this._verbMap.has(stem)) return this._verbMap.get(stem);
      if (stem.endsWith('a') && stem.length >= 4) {
        const candInf = stem + 're';
        if (this._verbMap.has(candInf)) return candInf;
        return candInf;
      }
      if (stem.endsWith('i') && stem.length >= 4) {
        const candIre = stem.slice(0, -1) + 'ire';
        if (this._verbMap.has(candIre)) return candIre;
        const candEre = stem.slice(0, -1) + 'ere';
        if (this._verbMap.has(candEre)) return candEre;
      }
      if (stem.endsWith('te') && stem.length >= 5) {
        const candInf = stem.slice(0, -2) + 're';
        if (this._verbMap.has(candInf)) return candInf;
      }
      clean = stem;
    }

    // 6. Regras regulares de flexão nominal:
    // Plural masculino -i -> -o
    if (clean.endsWith('i') && clean.length > 3) {
      const candO = clean.slice(0, -1) + 'o';
      if (this._templeWords.has(candO)) return candO;
      const candE = clean.slice(0, -1) + 'e';
      if (this._templeWords.has(candE)) return candE;
      return candO;
    }

    // Substantivos singulares em -ore (invasore, amore, fiore) e -ione (canzone, lezione)
    if (clean.endsWith('ore') && clean.length >= 4) return clean;
    if (clean.endsWith('ione') && clean.length >= 5) return clean;

    // Plural feminino -e -> -a
    if (clean.endsWith('e') && clean.length > 3) {
      const candA = clean.slice(0, -1) + 'a';
      if (this._templeWords.has(candA)) return candA;
      if (!clean.endsWith('are') && !clean.endsWith('ere') && !clean.endsWith('ire')) {
        return candA;
      }
    }

    // Feminino singular de adjetivos regulares -a -> -o
    if (clean.endsWith('a') && clean.length > 3) {
      const candO = clean.slice(0, -1) + 'o';
      if (this._templeWords.has(candO)) return candO;
    }

    // Particípios passados regulares (-ato -> -are, -uto -> -ere, -ito -> -ire)
    if (clean.endsWith('ato') && clean.length > 4) return clean.slice(0, -3) + 'are';
    if (clean.endsWith('uto') && clean.length > 4) return clean.slice(0, -3) + 'ere';
    if (clean.endsWith('ito') && clean.length > 4) return clean.slice(0, -3) + 'ire';

    // Gerúndios regulares (-ando -> -are, -endo -> -ere)
    if (clean.endsWith('ando') && clean.length > 5) return clean.slice(0, -4) + 'are';
    if (clean.endsWith('endo') && clean.length > 5) return clean.slice(0, -4) + 'ere';

    // Imperfeito regular (-avo/-ava -> -are, -evo/-eva -> -ere, -ivo/-iva -> -ire)
    if (/(?:avo|ava|avano)$/.test(clean) && clean.length > 5) return clean.replace(/(?:avo|ava|avano)$/, 'are');
    if (/(?:evo|eva|evano)$/.test(clean) && clean.length > 5) return clean.replace(/(?:evo|eva|evano)$/, 'ere');
    if (/(?:ivo|iva|ivano)$/.test(clean) && clean.length > 5) return clean.replace(/(?:ivo|iva|ivano)$/, 'ire');

    return clean;
  },

  /**
   * Calcula o Índice de Legibilidade Oficial Gulpease para textos em italiano.
   * Fórmula: 89 - (10 * LP / P) + (300 * FR / P)
   * Onde LP = total de letras nas palavras, P = total de palavras, FR = total de frases.
   * @param {string} text - Texto italiano
   * @returns {GulpeaseResult} Resultado detalhado do índice
   */
  computeGulpease(text) {
    if (!text || typeof text !== 'string' || !text.trim()) {
      return {
        score: 0,
        rawScore: 0,
        level: 'molto_difficile',
        lp: 0,
        p: 0,
        fr: 0,
        interpretation: 'Testo vuoto'
      };
    }

    const clean = text.trim();
    // Extrai palavras com caracteres alfabéticos
    const words = clean.match(/[a-zA-Z\u00C0-\u024F]+/g) || [];
    const p = words.length;

    if (p === 0) {
      return {
        score: 0,
        rawScore: 0,
        level: 'molto_difficile',
        lp: 0,
        p: 0,
        fr: 0,
        interpretation: 'Nessuna parola trovata'
      };
    }

    // LP: Lettere nelle Parole (soma do tamanho das palavras)
    const lp = words.reduce((acc, w) => acc + w.length, 0);

    // FR: Frasi Totali
    // Protege abreviações comuns italianas para que o ponto não fragmente frases
    let t = clean.replace(/(\b(?:dott|prof|sig|sig\.ra|ing|avv|es|ecc|pag|vol|art)\.)/gi, ' ');
    const rawSentences = t.split(/[.!?;\n]+/).filter(s => s.trim().length > 0);
    const fr = Math.max(1, rawSentences.length);

    // Fórmula Gulpease
    const rawScore = 89 - (10.0 * lp / p) + (300.0 * fr / p);
    const clampedScore = Math.max(0, Math.min(100, Math.round(rawScore * 10) / 10));

    let level = 'molto_difficile';
    let interpretation = 'Molto difficile (accessibile solo con laurea / C2)';
    if (clampedScore >= 80) {
      level = 'molto_facile';
      interpretation = 'Molto facile (licenza elementare / A1-A2)';
    } else if (clampedScore >= 60) {
      level = 'facile';
      interpretation = 'Facile (licenza media / B1-B2)';
    } else if (clampedScore >= 40) {
      level = 'difficile';
      interpretation = 'Difficile (diploma scuola superiore / C1)';
    }

    return {
      score: clampedScore,
      rawScore: Math.round(rawScore * 10) / 10,
      level,
      lp,
      p,
      fr,
      interpretation
    };
  },

  /**
   * Alias de conveniência para computeGulpease
   * @param {string} text - Texto italiano
   * @returns {GulpeaseResult} Resultado detalhado do índice
   */
  calculateGulpease(text) {
    return this.computeGulpease(text);
  },

  /**
   * Pipeline completo de normalização: tokeniza o texto, desempacota elisões,
   * restaura apócopes e reduz cada token ao seu lema de dicionário.
   * @param {string} text - Texto em italiano
   * @returns {string[]} Lista de lemas normalizados
   */
  normalizeText(text) {
    if (!text || typeof text !== 'string') return [];
    const tokens = this.tokenize(text, { lowercase: true });
    const lemmas = [];

    for (const token of tokens) {
      const unpacked = this.unpackElisions(token);
      for (const piece of unpacked) {
        const lemma = this.toLemma(piece);
        if (lemma) {
          lemmas.push(lemma);
        }
      }
    }

    return lemmas;
  }
};

// Auto-inicialização caso o motor seja carregado em ambiente com AppState já presente
if (typeof globalThis !== 'undefined') {
  globalThis.TextNormalizer = TextNormalizer;
}
if (typeof window !== 'undefined') {
  window.TextNormalizer = TextNormalizer;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TextNormalizer;
}
