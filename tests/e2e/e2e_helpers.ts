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
