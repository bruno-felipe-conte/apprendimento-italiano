// ============================================================
// types/app.d.ts — Canonical Type Definitions (ARC-03)
// ============================================================

export interface PalavraVocab {
  id: string;
  italiano: string;
  portugues: string;
  audio_ipa?: string;
  categoria?: string;
  exemplo?: string;
  exemplo_pt?: string;
  templo_num?: number;
  _templo?: number;
}

export interface TemploData {
  templo: number;
  nome: string;
  cidade: string;
  nivel: string;
  palavras: PalavraVocab[];
  vocabulario?: PalavraVocab[];
}

export interface MetaPrazoData {
  nivel_alvo: number;
  data_alvo: string;
  xp_na_criacao?: number;
  criado_em?: number;
}

export interface MetaPrazoCalculada {
  diasRestantes: number;
  xpFaltante: number;
  xpPorDia: number;
  xpMedioDia: number;
  dataPrevisao: string;
  atingeNoPrazo: boolean;
  nivel_alvo: number;
  data_alvo: string;
}

export interface ProgressoUsuario {
  nivel: number;
  xp: number;
  xp_proximo_nivel: number;
  templos_desbloqueados: number[];
  templos_concluidos: number[];
  total_palavras: number;
  streak: number;
  ultimo_estudo: number | null;
  grammatica_completadas: string[];
  meta_diaria: number;
  xp_hoje: number;
  data_xp_hoje: string | null;
  favoritos: string[];
  conquistas: string[];
  data_inicio: number;
  meta_prazo: MetaPrazoData | null;
  audio_rate: number;
  ultima_secao?: string;
}

export interface FlashcardFSRS {
  id?: string;
  state: 'new' | 'learning' | 'review' | 'suspended';
  due?: number;
  stability: number;
  difficulty: number;
  reps: number;
  lapses: number;
  lastReview?: number;
  nextReview?: number;
  repeticoes?: number;
}

export interface AppEstado {
  secaoAtiva: string;
  templosData: Record<number, TemploData>;
  quizData: any[];
  vocabCache: PalavraVocab[];
  conjugacoesData: any[];
  progresso: ProgressoUsuario | null;
  flashcardData: Record<string, FlashcardFSRS>;
}

export interface VoiceEngineOptions {
  rate?: number;
  pitch?: number;
  onend?: () => void;
  onerror?: (err: any) => void;
}

export interface StatusVozNeural {
  instalada: boolean;
  baixando: boolean;
  ativa: boolean;
}

export interface ModalAction {
  texto: string;
  classe?: string;
  onClick: (modal: any) => void;
}

export interface ModalConfig {
  id: string;
  titulo?: string;
  html?: string;
  conteudoEl?: HTMLElement;
  acoes?: ModalAction[];
  onFechar?: () => void;
  ariaLabel?: string;
  larguraMax?: string;
}

export interface PluginRoute {
  path: string;
  handler: (params?: Record<string, any>) => void;
  title?: string;
}

export interface PluginContext {
  app: any;
  state: any;
  navigation: any;
  modals: any;
  t: (key: string) => string;
}

export interface IPlugin {
  id: string;
  name: string;
  version?: string;
  routes?: PluginRoute[];
  init(ctx?: PluginContext | any): Promise<void> | void;
  destroy?(): Promise<void> | void;
  onSectionChange?(novaSecao: string, secaoAnterior: string): void;
}

export type SyncEntity = 'users' | 'progress' | 'flashcards' | 'quiz_history' | 'stories_read' | 'custom_content';
export type SyncAction = 'create' | 'update' | 'delete';

export interface SyncItem {
  id: string;
  entity: SyncEntity;
  action: SyncAction;
  entityId: string;
  payload: Record<string, any>;
  timestamp: number;
  attempts: number;
  lastAttempt?: number;
  lastError?: string;
}

export interface SyncBatchResult {
  sucesso: boolean;
  processados: string[];
  falhas: { id: string; erro: string }[];
}

export interface SyncStatus {
  isOnline: boolean;
  isSyncing: boolean;
  pendingCount: number;
  lastSyncSuccess: number | null;
  lastSyncError: string | null;
  provider: 'supabase' | 'pocketbase' | 'mock' | 'none';
  userId: string | null;
}

export interface BackendConfig {
  provider: 'supabase' | 'pocketbase' | 'mock' | 'none';
  endpoint: string;
  apiKey?: string;
  authToken?: string;
  userId?: string;
  autoSync?: boolean;
  syncIntervalMs?: number;
}

export interface IBackendAdapter {
  provider: 'supabase' | 'pocketbase' | 'mock' | 'none';
  init(config: BackendConfig): Promise<void> | void;
  syncBatch(items: SyncItem[]): Promise<SyncBatchResult>;
  pullLatest?(entity: SyncEntity, sinceTimestamp: number): Promise<any[]>;
  authMagicLink?(email: string): Promise<boolean>;
  authWithPassword?(email: string, password: string): Promise<{ token: string; user: any }>;
}

export interface AnalyticsEvent {
  id: string;
  name: string;
  properties: Record<string, any>;
  timestamp: number;
  userId?: string;
  sessionId?: string;
}

export interface FeatureFlag {
  key: string;
  variants: string[];
  weights?: number[];
  defaultValue: string;
  enabled?: boolean;
}

export interface IAnalyticsProvider {
  name: string;
  init?(config?: any): void | Promise<void>;
  track(event: AnalyticsEvent): void | Promise<void>;
  identify?(userId: string, traits?: Record<string, any>): void | Promise<void>;
}

declare global {
  interface Window {
    App: any;
    AppState: any;
    AppNavigation: any;
    AppPluginManager: any;
    AppSyncManager: any;
    AppAnalytics: any;
    AppFeatureFlags: any;
    AppXP: any;
    AppStats: any;
    AppMeta: any;
    AppFavorites: any;
    AppTemploData: any;
    AppTemploModal: any;
    AppTemplos: any;
    AppTTS: any;
    Progressao: any;
    LevelUp: any;
    VoiceEngine: any;
    ModalManager: any;
    AudioCache: any;
    I18n: any;
    SomFeedback: any;
    FSRS: any;
    Flashcards: any;
    Quiz: any;
    Vocab: any;
    Storie: any;
    Grammatica: any;
    Dialoghi: any;
    Canzoni: any;
    Imitazione: any;
    Heatmap: any;
    Profilo: any;
    Conquistas: any;
    IAImport: any;
    Onboarding: any;
    Notificacoes: any;
    Tour: any;
    Calor: any;
    _activeUtterance: SpeechSynthesisUtterance | null;
    _activeVoiceUtterance: SpeechSynthesisUtterance | null;
  }
}


