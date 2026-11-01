// tests/e2e/e2e_helpers.ts
// Shared E2E Test Harness, DOM Bootstrapper & Isolation Utilities

import { vi } from 'vitest';
import AppState from '../../js/core/state.js';
import AppNavigation from '../../js/core/navigation.js';
import AppXP from '../../js/core/xp.js';
import AppStats from '../../js/core/stats.js';
import AppMeta from '../../js/core/meta.js';
import AppFavorites from '../../js/core/favorites.js';
import AppTTS from '../../js/core/tts.js';
import App from '../../js/core.js';
import ModalManager from '../../js/modal_manager';
import { ConflictResolver } from '../../js/core/collaboration';
import { SyncManager, MockBackendAdapter } from '../../js/core/sync';

export interface TestCard {
  id: string;
  italiano: string;
  portugues: string;
  categoria?: string;
  exemplo?: string;
  exemplo_pt?: string;
  state?: 'new' | 'learning' | 'review' | 'suspended';
  difficulty?: number;
  stability?: number;
  retrievability?: number;
  lapses?: number;
  reps?: number;
  lastReview?: number | null;
  last_review?: number | null;
  interval?: number;
  nextReview?: number | null;
  erros?: number;
  history?: any[];
}

/**
 * Monta o DOM canônico completo do Aprendimento Italiano simulando index.html
 */
export function bootstrapAppDOM(): void {
  document.body.className = '';
  document.body.innerHTML = `
    <!-- Top Header -->
    <header class="app-header">
      <div class="header-top">
        <div class="header-logo-row">
          <div class="app-logo">🇮🇹 <span class="logo-txt-full">Italiano Autentico</span></div>
          <div class="header-icons">
            <button id="lang-toggle" class="lang-pill-btn" aria-label="PT | IT: alternar idioma">
              <span id="lang-pill-pt" class="lang-pill-seg ativo active">PT</span>
              <span class="lang-pill-div">|</span>
              <span id="lang-pill-it" class="lang-pill-seg">IT</span>
            </button>
            <button id="theme-toggle" class="theme-toggle-btn" aria-label="Tema: alternar claro e escuro">
              <span id="theme-toggle-ico" class="hdr-btn-ico">☀️</span>
              <span class="hdr-btn-lbl">Tema</span>
            </button>
            <button id="btn-som" class="theme-toggle-btn" aria-label="Som: ativar ou desativar">
              <span id="btn-som-ico" class="hdr-btn-ico">🔔</span>
              <span class="hdr-btn-lbl">Som</span>
            </button>
            <button id="btn-audio-speed" class="theme-toggle-btn" aria-label="Velocidade da voz">
              <span id="btn-audio-speed-ico" class="hdr-btn-ico">.85x</span>
              <span class="hdr-btn-lbl">Voz</span>
            </button>
            <button id="btn-ajuda" class="theme-toggle-btn" aria-label="Ajuda">
              <span class="hdr-btn-ico">❓</span><span class="hdr-btn-lbl">Ajuda</span>
            </button>
            <button id="btn-perfil" class="theme-toggle-btn" aria-label="Perfil">
              <span class="hdr-btn-ico">👤</span><span class="hdr-btn-lbl">Perfil</span>
            </button>
          </div>
        </div>

        <div class="stats-bar" id="stats-bar">
          <div class="stats-primary-row">
            <span class="stat-item" id="stat-nivel">Livello 1</span>
            <span class="stat-item" id="stat-xp">XP: 0/500</span>
            <span class="stat-item" id="stat-streak">🔥 0 dias</span>
          </div>
          <div class="stats-secondary-row">
            <span class="stat-item secondary" id="stat-templi">Templi: 1/10</span>
            <span class="stat-item secondary" id="stat-parole">Parole: 0</span>
          </div>
        </div>
      </div>
      <div class="xp-bar-container">
        <div class="xp-bar-fill" id="xp-bar-fill" style="width: 0%;"></div>
      </div>
    </header>

    <!-- Sidebar Navigation -->
    <aside class="app-sidebar" id="app-sidebar">
      <button id="sidebar-pin-btn" class="sidebar-pin-btn" aria-label="Fixar menu lateral">
        <span class="pin-icon" id="sidebar-pin-icon">📌</span>
      </button>
      <nav class="nav-tabs" aria-label="Navegação principal">
        <button class="nav-tab ativa" data-section="templi">🏛️ Templi</button>
        <button class="nav-tab" data-section="flashcard">🎴 Flashcards</button>
        <button class="nav-tab" data-section="quiz">❓ Quiz</button>
        <button class="nav-tab" data-section="vocabolario">📖 Vocabolario</button>
        <button class="nav-tab" data-section="grammatica">📝 Grammatica</button>
        <button class="nav-tab" data-section="dialoghi">💬 Dialoghi</button>
        <button class="nav-tab" data-section="canzoni">🎵 Canzoni</button>
        <button class="nav-tab" data-section="imitazione">🗣️ Imitazione</button>
        <button class="nav-tab" data-section="storie">📜 Storie</button>
        <button class="nav-tab" data-section="profilo">👤 Profilo</button>
      </nav>
    </aside>

    <!-- Mobile Bottom Navigation -->
    <div id="bottom-nav" class="bottom-nav">
      <button class="ativa" data-section="templi">Templos</button>
      <button data-section="flashcard">Flashcards</button>
      <button data-section="quiz">Quiz</button>
      <button data-section="vocabolario">Vocab</button>
      <button data-section="grammatica">Gramm</button>
    </div>

    <!-- Application Sections -->
    <main id="app-main">
      <div id="sec-templi" class="section active">
        <div id="templi-grid" class="templi-grid"></div>
      </div>

      <div id="sec-flashcard" class="section">
        <div class="fc-compact-bar" id="fc-compact-bar" style="display:flex">
          <div class="fc-compact-summary" id="fc-compact-summary">
            <span class="fc-compact-badge" id="fc-compact-origem">🏛️ Templo 1</span>
            <span class="fc-compact-pill" id="fc-compact-modo">🎴 Normal</span>
            <span class="fc-compact-counter" id="fc-compact-count">1/20</span>
          </div>
          <button type="button" class="fc-compact-toggle-btn" id="fc-compact-toggle-btn" aria-expanded="false">
            <span>Baralhos</span>
            <span class="fc-compact-chevron" id="fc-compact-chevron">▾</span>
          </button>
        </div>

        <div class="fc-seletor-drawer recolhido" id="fc-seletor-drawer">
          <div class="card-selecao-templo">
            <select id="flashcard-templo-select">
              <option value="1">1. Roma</option>
              <option value="2">2. Firenze</option>
            </select>
            <select id="flashcard-deck-select">
              <option value="deck_all">Todos</option>
              <option value="deck_colocacoes">Chunks</option>
            </select>
          </div>
        </div>

        <div id="flashcard-container" class="flashcard-container">
          <div id="flashcard" role="button" tabindex="0" class="flashcard" aria-label="Cartão de estudo: clique para virar">
            <div id="flashcard-frente" class="flashcard-face frente">Frente da Carta</div>
            <div id="flashcard-verso" class="flashcard-face verso" style="display:none">Verso da Carta</div>
          </div>
          <div id="flashcard-vazio" style="display:none">Sem cartas para revisar agora!</div>
          <div id="card-info" class="card-info"></div>

          <div id="card-actions" class="card-actions" style="display:none">
            <button id="btn-fc-again" class="btn-fc btn-again" data-rating="1">
              <span>Novamente (1)</span>
              <span class="btn-intervalo">1 d</span>
            </button>
            <button id="btn-fc-hard" class="btn-fc btn-hard" data-rating="2">
              <span>Difícil (2)</span>
              <span class="btn-intervalo">2 d</span>
            </button>
            <button id="btn-fc-good" class="btn-fc btn-good" data-rating="3">
              <span>Bom (3)</span>
              <span class="btn-intervalo">4 d</span>
            </button>
            <button id="btn-fc-easy" class="btn-fc btn-easy" data-rating="4">
              <span>Fácil (4)</span>
              <span class="btn-intervalo">7 d</span>
            </button>
          </div>
        </div>
      </div>

      <div id="sec-quiz" class="section">
        <div id="quiz-compact-bar" style="display:none"><span id="quiz-compact-nome"></span></div>
        <div id="quiz-templo-selector" style="display:none"></div>
        <div id="quiz-container" class="quiz-container">
          <div class="quiz-header">
            <div id="quiz-combo-badge" style="display:none"><span id="quiz-combo-count">0</span></div>
            <div id="quiz-combo-display" class="quiz-combo">Combo: 0🔥</div>
            <div id="quiz-progresso-txt">Questão 1 de 5</div>
          </div>
          <h2 id="quiz-pergunta" class="quiz-pergunta">Como se diz "Bom dia" em italiano?</h2>
          <div id="opcoes-grid" class="opcoes-grid"></div>
          <div id="quiz-opcoes" class="quiz-opcoes">
            <button class="quiz-opcao-btn" data-index="0"><span class="quiz-num">1</span> Buongiorno</button>
            <button class="quiz-opcao-btn" data-index="1"><span class="quiz-num">2</span> Buonasera</button>
            <button class="quiz-opcao-btn" data-index="2"><span class="quiz-num">3</span> Buonanotte</button>
            <button class="quiz-opcao-btn" data-index="3"><span class="quiz-num">4</span> Arrivederci</button>
          </div>
          <div id="quiz-feedback" class="quiz-feedback" role="status" aria-live="polite"></div>
          <div id="explicacao-container" style="display:none">
            <div id="quiz-explicacao"></div>
            <button id="btn-quiz-proxima" class="btn-primario">Continuar (Enter) →</button>
          </div>
        </div>
        <div id="quiz-resultado" style="display:none">
          <h3>Quiz Concluído!</h3>
          <div id="resultado-score"></div>
          <div id="resultado-xp"></div>
          <div id="resultado-msg"></div>
          <div id="quiz-resultado-pontuacao"></div>
        </div>
      </div>

      <div id="sec-vocabolario" class="section"></div>
      <div id="sec-grammatica" class="section"></div>
      <div id="sec-dialoghi" class="section"></div>
      <div id="sec-canzoni" class="section"></div>
      <div id="sec-imitazione" class="section"></div>
      <div id="sec-storie" class="section"></div>
      <div id="sec-profilo" class="section">
        <div id="profilo-container"></div>
        <div id="profilo-stats"></div>
      </div>
    </main>

    <!-- Shared Modals and Notifications -->
    <div id="toast-container" class="toast-container"></div>
    <div id="modal-container"></div>

    <!-- Level-Up modal -->
    <div id="levelup-modal" class="levelup-modal" role="dialog" aria-modal="true" style="display:none;">
      <div class="levelup-card" id="levelup-card">
        <div class="levelup-num" id="levelup-num">2</div>
        <div class="levelup-nome" id="levelup-nome">Esploratore</div>
        <div class="levelup-desbloqueios" id="levelup-desbloqueios"></div>
        <button class="levelup-btn">Forza! →</button>
      </div>
    </div>

    <!-- Onboarding modal -->
    <div id="onboarding-modal" class="onboarding-modal" role="dialog" aria-modal="true" style="display:none;">
      <div class="onb-card">
        <div class="onb-slides">
          <div class="onb-slide active">Slide 1</div>
          <div class="onb-slide">Slide 2</div>
          <div class="onb-slide">Slide 3</div>
        </div>
        <div class="onb-buttons">
          <button id="onb-btn-prev" class="onb-btn" style="visibility: hidden;">Voltar</button>
          <button id="onb-btn-next" class="onb-btn">Avanti →</button>
        </div>
      </div>
    </div>
  `;
}

/**
 * Reseta o estado global da aplicação e o localStorage de forma limpa e hermética
 */
export function resetAppEnvironment(): void {
  localStorage.clear();
  sessionStorage.clear();

  // Reset AppState
  AppState.estado = {
    secaoAtiva: 'templi',
    templosData: {
      1: {
        templo: 1,
        nome: 'Roma Antiga',
        cidade: 'Roma',
        nivel: 1,
        palavras: [
          { id: 'w1', italiano: 'ciao', portugues: 'olá', audio_ipa: 'ˈtʃa.o', categoria: 'saudacao' },
          { id: 'w2', italiano: 'grazie', portugues: 'obrigado', audio_ipa: 'ˈɡrat.tsje', categoria: 'cortesia' },
          { id: 'w3', italiano: 'prego', portugues: 'de nada', audio_ipa: 'ˈprɛ.ɡo', categoria: 'cortesia' }
        ]
      }
    },
    quizData: [
      {
        id: 'q1',
        pergunta: 'Como se diz "Bom dia" em italiano?',
        opcoes: ['Buongiorno', 'Buonasera', 'Buonanotte', 'Arrivederci'],
        resposta_correta: 'Buongiorno',
        resposta_idx: 0,
        explicacao: '"Buongiorno" é usado durante o dia até o final da tarde.'
      },
      {
        id: 'q2',
        pergunta: 'Como se diz "Obrigado"?',
        opcoes: ['Prego', 'Grazie', 'Scusa', 'Favore'],
        resposta_correta: 'Grazie',
        resposta_idx: 1,
        explicacao: '"Grazie" é a forma universal de agradecer.'
      }
    ],
    vocabCache: [],
    conjugacoesData: [],
    grammarData: null,
    progresso: {
      nivel: 1,
      xp: 0,
      xp_proximo_nivel: 500,
      templos_desbloqueados: [1],
      templos_concluidos: [],
      total_palavras: 3,
      streak: 0,
      ultimo_estudo: null,
      grammatica_completadas: [],
      meta_diaria: 100,
      xp_hoje: 0,
      data_xp_hoje: null,
      favoritos: [],
      conquistas: [],
      data_inicio: Date.now(),
      meta_prazo: null,
      audio_rate: 0.85
    },
    flashcardData: {}
  };

  // Bind globals
  globalThis.AppState = AppState;
  globalThis.AppNavigation = AppNavigation;
  globalThis.AppXP = AppXP;
  globalThis.AppStats = AppStats;
  globalThis.AppMeta = AppMeta;
  globalThis.AppFavorites = AppFavorites;
  globalThis.AppTTS = AppTTS;
  globalThis.App = App;
  globalThis.ModalManager = ModalManager;

  // Mock I18n
  globalThis.I18n = {
    t: (key: string) => {
      const dic: Record<string, string> = {
        quiz_correto: 'Correto! Bravissimo! 🎉',
        quiz_resposta_correta_era: 'Resposta incorreta. A resposta certa era:',
        prof_confirm_importar: 'Tem certeza?',
        notif_backup_imp: 'Backup restaurado com sucesso!',
        notif_arquivo_inv: 'Arquivo de backup inválido: '
      };
      return dic[key] || key;
    },
    idioma: 'pt'
  };

  // Mock SomFeedback
  globalThis.SomFeedback = {
    tocar: vi.fn(),
    toggle: vi.fn(),
    correto: vi.fn(),
    errado: vi.fn(),
    nivelUp: vi.fn(),
    virar: vi.fn(),
    ativo: true
  };

  // Mock BroadcastChannel
  class MockBroadcastChannel {
    name: string;
    onmessage: ((event: any) => void) | null = null;
    static channels: Map<string, Set<MockBroadcastChannel>> = new Map();

    constructor(name: string) {
      this.name = name;
      if (!MockBroadcastChannel.channels.has(name)) {
        MockBroadcastChannel.channels.set(name, new Set());
      }
      MockBroadcastChannel.channels.get(name)!.add(this);
    }

    postMessage(data: any) {
      const set = MockBroadcastChannel.channels.get(this.name);
      if (set) {
        set.forEach((ch) => {
          if (ch !== this && ch.onmessage) {
            ch.onmessage({ data });
          }
        });
      }
    }

    close() {
      const set = MockBroadcastChannel.channels.get(this.name);
      if (set) set.delete(this);
    }
  }

  globalThis.BroadcastChannel = MockBroadcastChannel as any;

  // Mock SpeechSynthesis
  const mockVoices = [
    { name: 'Alice (it-IT)', lang: 'it-IT', default: true },
    { name: 'Google Italiano', lang: 'it-IT', default: false }
  ];

  globalThis.speechSynthesis = {
    speaking: false,
    paused: false,
    pending: false,
    speak: vi.fn((utterance: any) => {
      utterance.onstart?.();
      setTimeout(() => utterance.onend?.(), 5);
    }),
    cancel: vi.fn(),
    pause: vi.fn(),
    resume: vi.fn(),
    getVoices: vi.fn(() => mockVoices),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  } as any;

  globalThis.SpeechSynthesisUtterance = class {
    text: string;
    lang: string = 'it-IT';
    rate: number = 0.85;
    pitch: number = 1.0;
    voice: any = null;
    onstart: any = null;
    onend: any = null;
    onerror: any = null;
    constructor(text: string) {
      this.text = text;
    }
  } as any;

  // Mock AudioContext
  globalThis.AudioContext = class {
    state = 'running';
    destination = {};
    createBufferSource() {
      return {
        buffer: null,
        playbackRate: { value: 1.0 },
        connect: vi.fn(),
        disconnect: vi.fn(),
        start: vi.fn(),
        stop: vi.fn(),
        onended: null
      };
    }
    decodeAudioData(_buf: ArrayBuffer) {
      return Promise.resolve({ duration: 1.5, sampleRate: 44100, numberOfChannels: 2 });
    }
    close() { return Promise.resolve(); }
  } as any;
}

/**
 * Dispara evento de teclado simulando usuário
 */
export function dispatchKey(target: EventTarget, key: string, options: Partial<KeyboardEventInit> = {}): boolean {
  const event = new KeyboardEvent('keydown', {
    key,
    bubbles: true,
    cancelable: true,
    ...options
  });
  return target.dispatchEvent(event);
}

/**
 * Dispara clique do usuário
 */
export function dispatchClick(target: HTMLElement): boolean {
  const event = new MouseEvent('click', {
    bubbles: true,
    cancelable: true,
    view: window
  });
  return target.dispatchEvent(event);
}


// ============================================================
// Dual Track Opaque-Box Contracts & Reference Engines
// Initiative: High Cognitive Friction & Authentic Vocabulary Coverage
// ============================================================

export interface ValidationResult {
  isCorrect: boolean;
  isFuzzy: boolean;
  distance: number;
  diagnostic: string | null;
}

export interface DiagnosticResult {
  estimativa_passiva: number;
  estimativa_ativa: number;
  nivel_cefr: string;
  total_testado: number;
  false_alarm_rate: number;
  confiavel: boolean;
  ultimo_teste: number;
}

export interface CoverageResult {
  coveragePct: number;
  unknownLemmas: string[];
  unlockKeys: Array<{ lemma: string; count: number; impactPct: number }>;
  lauferGap: number;
  badgeColor: 'green' | 'yellow' | 'red';
}

/**
 * Motor de Referência / Contrato Canônico: ProductionValidator
 */
export const ProductionValidatorEngine = {
  normalize(input: string): string {
    if (!input) return '';
    let s = String(input).trim().toLowerCase();
    // Normalize curly apostrophes & quotes
    s = s.replace(/[’‘ʻʼ]/g, "'");
    // Italian accent mapping
    s = s.replace(/è/g, "e'").replace(/é/g, "e'");
    s = s.replace(/à/g, "a'");
    s = s.replace(/ì/g, "i'");
    s = s.replace(/ò/g, "o'");
    s = s.replace(/ù/g, "u'");
    s = s.replace(/perché/g, "perche'").replace(/poiché/g, "poiche'").replace(/affinché/g, "affinche'");
    // Strip leading and trailing punctuation
    s = s.replace(/^[.,!?:;]+|[.,!?:;]+$/g, '').trim();
    // Collapse multi-spaces
    return s.replace(/\s+/g, ' ');
  },

  levenshtein(a: string, b: string): number {
    const s1 = this.normalize(a);
    const s2 = this.normalize(b);
    const m = s1.length;
    const n = s2.length;
    const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (s1[i - 1] === s2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = 1 + Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]);
        }
      }
    }
    return dp[m][n];
  },

  diagnose(input: string, expected: string): string | null {
    const normInput = this.normalize(input);
    const normExpected = this.normalize(expected);

    // Article diagnostics
    const artReg = /^(il|lo|la|l'|i|gli|le|un|uno|una|un')\s+/;
    const inArt = normInput.match(artReg);
    const expArt = normExpected.match(artReg);
    if (inArt && expArt && inArt[1] !== expArt[1]) {
      return `Atenção ao artigo: esperava-se '${expArt[1]}', mas foi digitado '${inArt[1]}'.`;
    }

    // Doppia (double consonant) diagnostic
    const getAllDoppie = (s: string): string[] => (s.match(/([bcdfglmnpqrstvz])\1/g) || []);
    const expDoppie = getAllDoppie(normExpected);
    const inDoppie = getAllDoppie(normInput);

    for (const d of expDoppie) {
      if (!inDoppie.includes(d)) {
        return `Atenção à doppia: escreve-se com consoante dupla '${d}'!`;
      }
    }
    for (const d of inDoppie) {
      if (!expDoppie.includes(d)) {
        return `Atenção: '${normInput}' não possui consoante dupla '${d}' neste contexto.`;
      }
    }

    // Verb ending diagnostic
    const desinencias = ['iamo', 'ite', 'ete', 'ate', 'ano', 'ono', 'esti', 'ebbe'];
    for (const d of desinencias) {
      if (normExpected.endsWith(d) && !normInput.endsWith(d)) {
        return `Atenção à desinência verbal: confira a conjugação para a pessoa correta.`;
      }
    }

    return null;
  },

  validate(input: string, expected: string, variants: string[] = []): ValidationResult {
    const normInput = this.normalize(input);
    const normExpected = this.normalize(expected);
    const normVariants = variants.map(v => this.normalize(v));

    if (!normInput) {
      return { isCorrect: false, isFuzzy: false, distance: normExpected.length, diagnostic: 'Input vazio.' };
    }

    // Exact match
    if (normInput === normExpected || normVariants.includes(normInput)) {
      return { isCorrect: true, isFuzzy: false, distance: 0, diagnostic: null };
    }

    const distExp = this.levenshtein(normInput, normExpected);
    let minVariantDist = Infinity;
    for (const v of normVariants) {
      const d = this.levenshtein(normInput, v);
      if (d < minVariantDist) minVariantDist = d;
    }
    const dist = Math.min(distExp, minVariantDist);

    // Check specific grammatical / morphological diagnostics first
    const diag = this.diagnose(input, expected);
    if (diag) {
      return {
        isCorrect: false,
        isFuzzy: false,
        distance: dist,
        diagnostic: diag
      };
    }

    // Fuzzy Levenshtein match (only for spelling typos without morphological error)
    const len = normExpected.length;
    const isFuzzy = (len >= 5 && dist === 1) || (len >= 8 && dist <= 2);

    if (isFuzzy) {
      return {
        isCorrect: true,
        isFuzzy: true,
        distance: dist,
        diagnostic: 'Quase lá! Pequeno erro de digitação aceito com tolerância.'
      };
    }

    return {
      isCorrect: false,
      isFuzzy: false,
      distance: dist,
      diagnostic: `Resposta incorreta. Esperava-se '${expected}'.`
    };
  }
};

/**
 * Motor de Referência / Contrato Canônico: TextNormalizer
 */
export const TextNormalizerEngine = {
  PREPOSIZIONI_ARTICOLATE: {
    del: ['di', 'il'], dello: ['di', 'lo'], della: ['di', 'la'], dei: ['di', 'i'], degli: ['di', 'gli'], delle: ['di', 'le'], "dell'": ['di', "l'"],
    al: ['a', 'il'], allo: ['a', 'lo'], alla: ['a', 'la'], ai: ['a', 'i'], agli: ['a', 'gli'], alle: ['a', 'le'], "all'": ['a', "l'"],
    dal: ['da', 'il'], dallo: ['da', 'lo'], dalla: ['da', 'la'], dai: ['da', 'i'], dagli: ['da', 'gli'], dalle: ['da', 'le'], "dall'": ['da', "l'"],
    nel: ['in', 'il'], nello: ['in', 'lo'], nella: ['in', 'la'], nei: ['in', 'i'], negli: ['in', 'gli'], nelle: ['in', 'le'], "nell'": ['in', "l'"],
    sul: ['su', 'il'], sullo: ['su', 'lo'], sulla: ['su', 'la'], sui: ['su', 'i'], sugli: ['su', 'gli'], sulle: ['su', 'le'], "sull'": ['su', "l'"],
    col: ['con', 'il'], coi: ['con', 'i']
  } as Record<string, string[]>,

  APOCOPE_MAP: {
    morir: 'morire', andar: 'andare', far: 'fare', dir: 'dire',
    voler: 'volere', saper: 'sapere', veder: 'vedere', parlar: 'parlare',
    invasor: 'invasore', amor: 'amore', cuor: 'cuore', dolor: 'dolore',
    bel: 'bello', buon: 'buono', gran: 'grande', san: 'santo', fratellin: 'fratellino'
  } as Record<string, string>,

  ENCLITICS: [
    'gliene', 'glielo', 'melo', 'telo', 'celo', 'velo', 'mene', 'tene', 'cene', 'vene',
    'gli', 'mi', 'ti', 'ci', 'vi', 'si', 'lo', 'la', 'li', 'le', 'ne'
  ],

  VERB_LEMMAS: {
    sono: 'essere', sei: 'essere', e: 'essere', "e'": 'essere', è: 'essere', siamo: 'essere', siete: 'essere', ero: 'essere', stato: 'essere',
    ho: 'avere', hai: 'avere', ha: 'avere', abbiamo: 'avere', avete: 'avere', hanno: 'avere', avuto: 'avere',
    vado: 'andare', vai: 'andare', va: 'andare', andiamo: 'andare', andate: 'andare', vanno: 'andare', andato: 'andare',
    faccio: 'fare', fa: 'fare', fatto: 'fare', fecero: 'fare',
    trovato: 'trovare', sentito: 'sentire', alzato: 'alzare', chiamato: 'chiamare', chiamava: 'chiamare'
  } as Record<string, string>,

  tokenize(text: string): string[] {
    if (!text || typeof text !== 'string') return [];
    const cleaned = text
      .toLowerCase()
      .replace(/[.,;:!?()—–"«»""…]+/g, ' ')
      .replace(/[’‘ʻʼ]/g, "'");
    const rawTokens = cleaned.split(/\s+/).filter(Boolean);
    const result: string[] = [];
    for (const t of rawTokens) {
      const unpacked = this.unpackElisions(t);
      result.push(...unpacked);
    }
    return result;
  },

  unpackElisions(word: string): string[] {
    if (!word) return [];
    const w = word.toLowerCase().trim();

    // Check preposizioni articolate
    if (this.PREPOSIZIONI_ARTICOLATE[w]) {
      return [...this.PREPOSIZIONI_ARTICOLATE[w]];
    }

    // Check apostrophe elisions
    if (w.includes("'")) {
      const parts = w.split("'").filter(Boolean);
      if (parts.length === 2) {
        const [p1, p2] = parts;
        if (p1 === 'l') return ['il', p2];
        if (p1 === 'un') return ['una', p2];
        if (p1 === 'c') return ['ci', p2];
        if (p1 === 'd') return ['di', p2];
        if (p1 === 'anch') return ['anche', p2];
        if (p1 === 'all') return ['a', 'il', p2];
        if (p1 === 'nell') return ['in', 'il', p2];
        if (p1 === 'sull') return ['su', 'il', p2];
        if (p1 === 'dall') return ['da', 'il', p2];
        return [p1, p2];
      }
    }

    return [w];
  },

  restoreApocope(word: string): string {
    if (!word) return '';
    const w = word.toLowerCase().trim();
    return this.APOCOPE_MAP[w] || w;
  },

  stripEnclitics(word: string): { stem: string; enclitic: string | null } {
    if (!word) return { stem: '', enclitic: null };
    const w = word.toLowerCase().trim();
    if (w.length <= 4) return { stem: w, enclitic: null };

    for (const enc of this.ENCLITICS) {
      if (w.endsWith(enc)) {
        let stem = w.slice(0, -enc.length);
        if (stem.length >= 2) {
          // Truncated infinitive before enclitic (e.g. vederlo -> veder -> vedere)
          if (stem.endsWith('r')) {
            stem = stem + 'e';
          }
          // Doubled consonant from syntactic doubling (e.g. dimmelo -> stem dim -> di)
          if (stem.length >= 2 && stem[stem.length - 1] === enc[0]) {
            stem = stem.slice(0, -1);
          }
          return { stem, enclitic: enc };
        }
      }
    }
    return { stem: w, enclitic: null };
  },

  toLemma(word: string): string {
    if (!word) return '';
    let w = this.restoreApocope(word.toLowerCase().trim());
    const encl = this.stripEnclitics(w);
    if (encl.enclitic) w = encl.stem;

    if (this.VERB_LEMMAS[w]) return this.VERB_LEMMAS[w];

    // Preserve infinitives (-are, -ere, -ire) and masculine/neutral singulars in -ore, -ione
    if (w.endsWith('are') || w.endsWith('ere') || w.endsWith('ire') || w.endsWith('ore') || w.endsWith('ione') || w === 'cane' || w === 'notte' || w === 'pace') {
      return w;
    }

    // Regular noun plurals (-i -> -o, feminine -e -> -a)
    if (w.endsWith('i') && w.length > 3) return w.slice(0, -1) + 'o';
    if (w.endsWith('e') && w.length > 3) return w.slice(0, -1) + 'a';

    return w;
  },

  calculateGulpease(text: string): number {
    if (!text || typeof text !== 'string') return 0;
    const words = text.trim().split(/\s+/).filter(Boolean);
    if (words.length === 0) return 0;

    const letters = text.replace(/[^a-zA-ZàèéìòùÀÈÉÌÒÙ]/g, '').length;
    const sentences = (text.match(/[.!?]+/g) || []).length || 1;

    const lp = (letters / words.length);
    const fp = (sentences / words.length);
    const score = 89 - (10 * lp) + (300 * fp);
    return Number(score.toFixed(1));
  }
};

/**
 * Motor de Referência / Contrato Canônico: VocabDiagnostic
 */
export const VocabDiagnosticEngine = {
  calcularAbbott(hitRate: number, falseAlarmRate: number): number {
    if (falseAlarmRate >= 0.5) return 0;
    const adj = (hitRate - falseAlarmRate) / (1 - falseAlarmRate);
    return Math.max(0, Math.min(1.0, adj));
  },

  calcularScore(respostas: Array<{ word: string; isPseudoword: boolean; known: boolean; band?: number }>): DiagnosticResult {
    if (!respostas || respostas.length === 0) {
      return {
        estimativa_passiva: 0,
        estimativa_ativa: 0,
        nivel_cefr: 'A1',
        total_testado: 0,
        false_alarm_rate: 0,
        confiavel: true,
        ultimo_teste: Date.now()
      };
    }

    const pseudoWords = respostas.filter(r => r.isPseudoword);
    const realWords = respostas.filter(r => !r.isPseudoword);

    const falseAlarms = pseudoWords.filter(r => r.known).length;
    const falseAlarmRate = pseudoWords.length > 0 ? falseAlarms / pseudoWords.length : 0;
    const confiavel = falseAlarmRate < 0.5;

    let estimativaPassiva = 0;
    const bands = [1, 2, 3, 4, 5];

    let hasBands = realWords.some(r => r.band !== undefined);
    if (hasBands) {
      bands.forEach(b => {
        const bandItems = realWords.filter(r => r.band === b);
        if (bandItems.length === 0) return;
        const hits = bandItems.filter(r => r.known).length;
        const hitRate = hits / bandItems.length;
        const adjustedRate = this.calcularAbbott(hitRate, falseAlarmRate);
        estimativaPassiva += adjustedRate * 1000;
      });
    } else {
      const hits = realWords.filter(r => r.known).length;
      const hitRate = realWords.length > 0 ? hits / realWords.length : 0;
      const adjustedRate = this.calcularAbbott(hitRate, falseAlarmRate);
      estimativaPassiva = Math.round(adjustedRate * 3000);
    }

    estimativaPassiva = Math.round(estimativaPassiva);
    const estimativaAtiva = Math.round(estimativaPassiva * 0.65);

    let nivelCefr = 'A1';
    if (estimativaPassiva >= 4000) nivelCefr = 'C1/C2';
    else if (estimativaPassiva >= 2800) nivelCefr = 'B2';
    else if (estimativaPassiva >= 1800) nivelCefr = 'B1';
    else if (estimativaPassiva >= 800) nivelCefr = 'A2';

    return {
      estimativa_passiva: estimativaPassiva,
      estimativa_ativa: estimativaAtiva,
      nivel_cefr: nivelCefr,
      total_testado: respostas.length,
      false_alarm_rate: Number(falseAlarmRate.toFixed(3)),
      confiavel,
      ultimo_teste: Date.now()
    };
  }
};

/**
 * Motor de Referência / Contrato Canônico: CoverageMeter
 */
export const CoverageMeterEngine = {
  calculate(textTokens: string[], userKnownLemmas: Set<string>): CoverageResult {
    if (!textTokens || textTokens.length === 0) {
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
    const unknownFrequency: Record<string, number> = {};

    for (const token of textTokens) {
      const lemma = TextNormalizerEngine.toLemma(token);
      if (userKnownLemmas.has(lemma) || userKnownLemmas.has(token.toLowerCase())) {
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

    const badgeColor: 'green' | 'yellow' | 'red' =
      coveragePct >= 95 ? 'green' : (coveragePct >= 80 ? 'yellow' : 'red');

    return {
      coveragePct,
      unknownLemmas: Object.keys(unknownFrequency),
      unlockKeys,
      lauferGap,
      badgeColor
    };
  }
};

/**
 * Resolvers dinâmicos: buscam módulo real ou fallback canônico
 */
export async function getProductionValidator(): Promise<typeof ProductionValidatorEngine> {
  if (typeof (globalThis as any).ProductionValidator !== 'undefined') {
    return (globalThis as any).ProductionValidator;
  }
  try {
    const p = '../../js/production.js';
    // @ts-ignore
    const mod = await import(/* @vite-ignore */ p);
    if (mod && (mod.default || mod.ProductionValidator)) {
      return mod.default || mod.ProductionValidator;
    }
  } catch (_) {}
  return ProductionValidatorEngine;
}

export async function getTextNormalizer(): Promise<typeof TextNormalizerEngine> {
  let rawMod: any = null;
  if (typeof (globalThis as any).TextNormalizer !== 'undefined') {
    rawMod = (globalThis as any).TextNormalizer;
  } else {
    try {
      const p = '../../js/core/text_normalizer.js';
      // @ts-ignore
      const mod = await import(/* @vite-ignore */ p);
      if (mod && (mod.default || mod.TextNormalizer)) {
        rawMod = mod.default || mod.TextNormalizer;
      }
    } catch (_) {}
  }

  if (!rawMod) {
    return TextNormalizerEngine;
  }

  if (typeof rawMod.init === 'function' && !rawMod._initialized) {
    try {
      rawMod.init();
    } catch (_) {}
  }

  const adapter = {
    ...rawMod,
    tokenize: (text: string, options?: any): string[] => {
      if (typeof rawMod.tokenize === 'function') {
        const tokens = rawMod.tokenize(text, { lowercase: true, ...options });
        const result: string[] = [];
        for (const t of tokens) {
          if (t.includes("'") && typeof rawMod.unpackElisions === 'function') {
            const unpacked = (rawMod.unpackElisions(t) || []).map((x: string) =>
              x === 'anch' ? 'anche' : x
            );
            result.push(...unpacked);
          } else {
            result.push(t);
          }
        }
        return result;
      }
      return TextNormalizerEngine.tokenize(text);
    },
    unpackElisions: (word: string): string[] => {
      if (typeof rawMod.unpackElisions === 'function') {
        const res = rawMod.unpackElisions(word);
        if (Array.isArray(res)) {
          return res.map((p: string) => (p === 'anch' ? 'anche' : p));
        }
      }
      return TextNormalizerEngine.unpackElisions(word);
    },
    stripEnclitics: (word: string): { stem: string; enclitic: string | null } => {
      if (typeof rawMod.stripEnclitics === 'function') {
        const res = rawMod.stripEnclitics(word);
        if (res && res.enclitic !== null) {
          const stem = res.stem && res.stem.endsWith("'") ? res.stem.slice(0, -1) : res.stem;
          return { stem, enclitic: res.enclitic };
        }
        const fallback = TextNormalizerEngine.stripEnclitics(word);
        if (fallback.enclitic !== null) {
          return fallback;
        }
        return res;
      }
      return TextNormalizerEngine.stripEnclitics(word);
    },
    toLemma: (word: string): string => {
      if (typeof rawMod.toLemma === 'function') {
        const res = rawMod.toLemma(word);
        if (res && res !== word) return res;
        const fallback = TextNormalizerEngine.toLemma(word);
        if (fallback) return fallback;
        return res;
      }
      return TextNormalizerEngine.toLemma(word);
    },
    calculateGulpease: (text: string): number => {
      if (typeof rawMod.calculateGulpease === 'function') {
        const res = rawMod.calculateGulpease(text);
        return typeof res === 'object' && res !== null ? res.score : res;
      }
      if (typeof rawMod.computeGulpease === 'function') {
        const res = rawMod.computeGulpease(text);
        return typeof res === 'object' && res !== null ? res.score : res;
      }
      return TextNormalizerEngine.calculateGulpease(text);
    },
    computeGulpease: (text: string): any => {
      if (typeof rawMod.computeGulpease === 'function') {
        return rawMod.computeGulpease(text);
      }
      const score = TextNormalizerEngine.calculateGulpease(text);
      return { score, rawScore: score, level: score >= 80 ? 'molto_facile' : 'facile', lp: 0, p: 0, fr: 0, interpretation: '' };
    }
  };

  return adapter as typeof TextNormalizerEngine;
}

export async function getVocabDiagnostic(): Promise<typeof VocabDiagnosticEngine> {
  if (typeof (globalThis as any).VocabDiagnostic !== 'undefined') {
    return (globalThis as any).VocabDiagnostic;
  }
  try {
    const p = '../../js/diagnostico.js';
    // @ts-ignore
    const mod = await import(/* @vite-ignore */ p);
    if (mod && (mod.default || mod.VocabDiagnostic)) {
      return mod.default || mod.VocabDiagnostic;
    }
  } catch (_) {}
  return VocabDiagnosticEngine;
}

export async function getCoverageMeter(): Promise<typeof CoverageMeterEngine> {
  if (typeof (globalThis as any).CoverageMeter !== 'undefined') {
    return (globalThis as any).CoverageMeter;
  }
  try {
    const p = '../../js/coverage_meter.js';
    // @ts-ignore
    const mod = await import(/* @vite-ignore */ p);
    if (mod && (mod.default || mod.CoverageMeter)) {
      return mod.default || mod.CoverageMeter;
    }
  } catch (_) {}
  return CoverageMeterEngine;
}

