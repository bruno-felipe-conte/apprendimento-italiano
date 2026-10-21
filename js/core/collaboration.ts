/**
 * Módulo de Sincronização Multi-Dispositivo e Colaboração (EV-05)
 * Reconciliação de conflitos sem perda de dados (CRDT/LWW), Decks Compartilhados e Leaderboards.
 */

import type {
  ProgressoUsuario,
  FlashcardFSRS,
  SyncConflict,
  ReconciliationResult,
  SharedDeck,
  LeaderboardEntry
} from '../../types/app';

// ==========================================
// FUNÇÕES UTILITÁRIAS DE CHECKSUM
// ==========================================
export function calcularChecksumSimples(conteudo: string): string {
  let hash = 0;
  for (let i = 0; i < conteudo.length; i++) {
    hash = (hash << 5) - hash + conteudo.charCodeAt(i);
    hash |= 0;
  }
  return Math.abs(hash).toString(16).padStart(8, '0');
}

// ==========================================
// CONFLICT RESOLVER (CRDT / LWW HÍBRIDO)
// ==========================================
export class ConflictResolver {
  /**
   * Reconcilia dois estados de progresso sem perda de dados.
   * Aplica união em conjuntos (templos, lições de gramática, conquistas) e max em pontuação (XP, nível).
   */
  public reconciliarProgresso(
    local: ProgressoUsuario,
    remoto: ProgressoUsuario
  ): { progresso: ProgressoUsuario; conflitos: SyncConflict[] } {
    const conflitos: SyncConflict[] = [];

    const uniaoNumeros = (a: number[] = [], b: number[] = []): number[] => {
      return Array.from(new Set([...a, ...b])).sort((x, y) => x - y);
    };

    const uniaoStrings = (a: string[] = [], b: string[] = []): string[] => {
      return Array.from(new Set([...a, ...b]));
    };

    const xpConflito = local.xp !== remoto.xp;
    if (xpConflito) {
      conflitos.push({
        entityId: 'progress.xp',
        localVersion: local.xp,
        remoteVersion: remoto.xp,
        resolvedVersion: Math.max(local.xp, remoto.xp),
        strategy: 'crdt-merge',
        timestamp: Date.now()
      });
    }

    const nivelConflito = local.nivel !== remoto.nivel;
    if (nivelConflito) {
      conflitos.push({
        entityId: 'progress.nivel',
        localVersion: local.nivel,
        remoteVersion: remoto.nivel,
        resolvedVersion: Math.max(local.nivel, remoto.nivel),
        strategy: 'crdt-merge',
        timestamp: Date.now()
      });
    }

    const merged: ProgressoUsuario = {
      ...local,
      nivel: Math.max(local.nivel || 1, remoto.nivel || 1),
      xp: Math.max(local.xp || 0, remoto.xp || 0),
      streak: Math.max(local.streak || 0, remoto.streak || 0),
      streak_recorde: Math.max(local.streak_recorde || 0, remoto.streak_recorde || 0),
      templos_desbloqueados: uniaoNumeros(local.templos_desbloqueados, remoto.templos_desbloqueados),
      templos_concluidos: uniaoNumeros(local.templos_concluidos, remoto.templos_concluidos),
      grammatica_completadas: uniaoStrings(local.grammatica_completadas, remoto.grammatica_completadas),
      conquistas: uniaoStrings(local.conquistas, remoto.conquistas),
      favoritos: uniaoStrings(local.favoritos, remoto.favoritos),
      ultimo_estudo: Math.max(local.ultimo_estudo || 0, remoto.ultimo_estudo || 0) || null,
      data_inicio: Math.min(local.data_inicio || Date.now(), remoto.data_inicio || Date.now())
    };

    return { progresso: merged, conflitos };
  }

  /**
   * Reconcilia baralhos de flashcards aplicando LWW e maior profundidade de aprendizado (reps).
   */
  public reconciliarFlashcards(
    local: Record<string, FlashcardFSRS>,
    remoto: Record<string, FlashcardFSRS>
  ): { flashcards: Record<string, FlashcardFSRS>; conflitos: SyncConflict[] } {
    const conflitos: SyncConflict[] = [];
    const merged: Record<string, FlashcardFSRS> = { ...local };

    for (const cardId of Object.keys(remoto)) {
      const cardRemoto = remoto[cardId];
      const cardLocal = local[cardId];

      if (!cardLocal) {
        // Se existe apenas no remoto, incorpora
        merged[cardId] = { ...cardRemoto };
        continue;
      }

      // Se existe em ambos, resolve conflito
      const timeLocal = cardLocal.lastReview || 0;
      const timeRemoto = cardRemoto.lastReview || 0;

      let resolvedCard: FlashcardFSRS;

      if (timeRemoto > timeLocal) {
        resolvedCard = { ...cardRemoto };
      } else if (timeLocal > timeRemoto) {
        resolvedCard = { ...cardLocal };
      } else {
        // Timestamps iguais: prioriza quem tem maior repetição
        resolvedCard = (cardRemoto.reps || 0) >= (cardLocal.reps || 0)
          ? { ...cardRemoto }
          : { ...cardLocal };
      }

      if (JSON.stringify(cardLocal) !== JSON.stringify(cardRemoto)) {
        conflitos.push({
          entityId: `flashcard.${cardId}`,
          localVersion: cardLocal,
          remoteVersion: cardRemoto,
          resolvedVersion: resolvedCard,
          strategy: 'last-write-wins',
          timestamp: Date.now()
        });
      }

      merged[cardId] = resolvedCard;
    }

    return { flashcards: merged, conflitos };
  }
}

// ==========================================
// SHARED DECK MANAGER (IMPORT / EXPORT)
// ==========================================
export class SharedDeckManager {
  public exportar(deck: {
    id?: string;
    title: string;
    description?: string;
    author?: string;
    cards: Array<{ palavra: string; traducao: string; exemplo?: string; categoria?: string; ipa?: string }>;
  }): SharedDeck {
    const cards = deck.cards || [];
    const serializado = JSON.stringify(cards);
    const checksum = calcularChecksumSimples(serializado);

    return {
      id: deck.id || `deck_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      title: deck.title,
      description: deck.description || 'Baralho compartilhado da comunidade',
      author: deck.author || 'Usuário Autentico',
      version: '1.0.0',
      createdAt: Date.now(),
      cards,
      checksum
    };
  }

  public importar(dado: string | SharedDeck): { sucesso: boolean; deck?: SharedDeck; erro?: string } {
    let parsed: SharedDeck;

    try {
      if (typeof dado === 'string') {
        parsed = JSON.parse(dado);
      } else {
        parsed = dado;
      }
    } catch (e: any) {
      return { sucesso: false, erro: `JSON inválido: ${e.message}` };
    }

    if (!parsed.title || !Array.isArray(parsed.cards)) {
      return { sucesso: false, erro: 'Formato de baralho inválido: campos obrigatórios ausentes' };
    }

    const checksumAtual = calcularChecksumSimples(JSON.stringify(parsed.cards));
    if (parsed.checksum && parsed.checksum !== checksumAtual) {
      return { sucesso: false, erro: 'Falha na verificação de integridade: checksum divergente' };
    }

    return {
      sucesso: true,
      deck: parsed
    };
  }
}

// ==========================================
// LEADERBOARD MANAGER (STUDY WITH FRIENDS)
// ==========================================
export class LeaderboardManager {
  private peers: LeaderboardEntry[] = [];

  constructor() {
    this.carregarColegasPadrao();
  }

  private carregarColegasPadrao(): void {
    this.peers = [
      { userId: 'usr_marco', nome: 'Marco Rossi', avatar: '🏛️', xpSemanal: 1250, streak: 14 },
      { userId: 'usr_giulia', nome: 'Giulia Bianchi', avatar: '🍕', xpSemanal: 980, streak: 9 },
      { userId: 'usr_matteo', nome: 'Matteo Ferrari', avatar: '☕', xpSemanal: 840, streak: 7 },
      { userId: 'usr_elena', nome: 'Elena Moretti', avatar: '🎭', xpSemanal: 620, streak: 4 }
    ];
  }

  public getRanking(usuarioAtual: { nome: string; xp: number; streak: number; avatar?: string }): LeaderboardEntry[] {
    const usuarioEntry: LeaderboardEntry = {
      userId: 'current_user',
      nome: `${usuarioAtual.nome} (Você)`,
      avatar: usuarioAtual.avatar || '⭐',
      xpSemanal: usuarioAtual.xp,
      streak: usuarioAtual.streak,
      isCurrentUser: true
    };

    const lista = [...this.peers, usuarioEntry];
    lista.sort((a, b) => b.xpSemanal - a.xpSemanal);
    return lista;
  }
}

// ==========================================
// COLLABORATION MANAGER (FACADE SINGLETON)
// ==========================================
export class CollaborationManager {
  public resolver: ConflictResolver;
  public decks: SharedDeckManager;
  public leaderboard: LeaderboardManager;

  constructor() {
    this.resolver = new ConflictResolver();
    this.decks = new SharedDeckManager();
    this.leaderboard = new LeaderboardManager();
  }

  public reconciliar(
    estadoLocal: { progresso?: ProgressoUsuario; flashcards?: Record<string, FlashcardFSRS> },
    estadoRemoto: { progresso?: ProgressoUsuario; flashcards?: Record<string, FlashcardFSRS> }
  ): ReconciliationResult {
    let totalConflitos = 0;
    let mergedProgresso: ProgressoUsuario | undefined;
    let mergedCards: Record<string, FlashcardFSRS> | undefined;

    if (estadoLocal.progresso && estadoRemoto.progresso) {
      const resProgresso = this.resolver.reconciliarProgresso(estadoLocal.progresso, estadoRemoto.progresso);
      mergedProgresso = resProgresso.progresso;
      totalConflitos += resProgresso.conflitos.length;
    }

    if (estadoLocal.flashcards && estadoRemoto.flashcards) {
      const resCards = this.resolver.reconciliarFlashcards(estadoLocal.flashcards, estadoRemoto.flashcards);
      mergedCards = resCards.flashcards;
      totalConflitos += resCards.conflitos.length;
    }

    return {
      conflictsDetected: totalConflitos,
      conflictsResolved: totalConflitos,
      updatedLocal: totalConflitos > 0 || !estadoLocal.progresso,
      mergedProgress: mergedProgresso,
      mergedFlashcards: mergedCards
    };
  }
}

export const AppCollaboration = new CollaborationManager();

if (typeof window !== 'undefined') {
  window.AppCollaboration = AppCollaboration;
}
