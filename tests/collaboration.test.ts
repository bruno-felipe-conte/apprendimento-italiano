import { describe, it, expect, beforeEach } from 'vitest';
import {
  ConflictResolver,
  SharedDeckManager,
  LeaderboardManager,
  CollaborationManager,
  calcularChecksumSimples
} from '../js/core/collaboration';
import type { ProgressoUsuario, FlashcardFSRS } from '../types/app';

describe('EV-05: Multi-device Sync & Collaboration', () => {
  let resolver: ConflictResolver;
  let sharedDecks: SharedDeckManager;
  let leaderboard: LeaderboardManager;
  let collaboration: CollaborationManager;

  beforeEach(() => {
    resolver = new ConflictResolver();
    sharedDecks = new SharedDeckManager();
    leaderboard = new LeaderboardManager();
    collaboration = new CollaborationManager();
  });

  describe('Reconciliação de Progresso (CRDT Union & Max Merge)', () => {
    it('deve fundir progresso sem perda de dados: união de templos e max de XP', () => {
      const localProgresso: ProgressoUsuario = {
        nivel: 2,
        xp: 350,
        xp_proximo_nivel: 500,
        templos_desbloqueados: [1, 2],
        templos_concluidos: [1],
        total_palavras: 20,
        streak: 3,
        streak_recorde: 5,
        ultimo_estudo: 1000,
        grammatica_completadas: ['artigos'],
        meta_diaria: 100,
        xp_hoje: 50,
        data_xp_hoje: '2026-10-21',
        favoritos: ['t1_001'],
        conquistas: ['primeiro_passo'],
        data_inicio: 500,
        meta_prazo: null,
        audio_rate: 0.85
      };

      const remotoProgresso: ProgressoUsuario = {
        nivel: 3,
        xp: 600,
        xp_proximo_nivel: 1000,
        templos_desbloqueados: [1, 3],
        templos_concluidos: [],
        total_palavras: 30,
        streak: 4,
        streak_recorde: 6,
        ultimo_estudo: 2000,
        grammatica_completadas: ['plurais'],
        meta_diaria: 100,
        xp_hoje: 100,
        data_xp_hoje: '2026-10-21',
        favoritos: ['t1_002'],
        conquistas: ['mestre_vocabulario'],
        data_inicio: 500,
        meta_prazo: null,
        audio_rate: 0.85
      };

      const { progresso, conflitos } = resolver.reconciliarProgresso(localProgresso, remotoProgresso);

      expect(progresso.nivel).toBe(3);
      expect(progresso.xp).toBe(600);
      expect(progresso.streak).toBe(4);
      expect(progresso.streak_recorde).toBe(6);
      expect(progresso.templos_desbloqueados).toEqual([1, 2, 3]);
      expect(progresso.templos_concluidos).toEqual([1]);
      expect(progresso.grammatica_completadas).toEqual(expect.arrayContaining(['artigos', 'plurais']));
      expect(progresso.conquistas).toEqual(expect.arrayContaining(['primeiro_passo', 'mestre_vocabulario']));
      expect(progresso.favoritos).toEqual(expect.arrayContaining(['t1_001', 't1_002']));
      expect(progresso.ultimo_estudo).toBe(2000);
      expect(conflitos.length).toBeGreaterThanOrEqual(2);
    });
  });

  describe('Reconciliação de Flashcards (LWW & Reps Depth)', () => {
    it('deve priorizar a revisão com timestamp mais recente quando há divergência', () => {
      const localCards: Record<string, FlashcardFSRS> = {
        t1_001: {
          id: 't1_001',
          state: 'review',
          reps: 2,
          lapses: 0,
          difficulty: 4.5,
          stability: 3.2,
          lastReview: 5000,
          due: 8000
        }
      };

      const remotoCards: Record<string, FlashcardFSRS> = {
        t1_001: {
          id: 't1_001',
          state: 'review',
          reps: 3,
          lapses: 0,
          difficulty: 4.2,
          stability: 6.0,
          lastReview: 9000, // Mais recente
          due: 15000
        },
        t1_002: { // Existe apenas no remoto
          id: 't1_002',
          state: 'new',
          reps: 0,
          lapses: 0,
          difficulty: 0,
          stability: 0,
          due: 1000
        }
      };

      const { flashcards, conflitos } = resolver.reconciliarFlashcards(localCards, remotoCards);

      expect(flashcards['t1_001'].lastReview).toBe(9000);
      expect(flashcards['t1_001'].reps).toBe(3);
      expect(flashcards['t1_002']).toBeDefined();
      expect(conflitos.length).toBe(1);
      expect(conflitos[0].entityId).toBe('flashcard.t1_001');
    });

    it('deve priorizar o card com maior número de reps se os timestamps forem idênticos', () => {
      const localCards: Record<string, FlashcardFSRS> = {
        t1_005: {
          id: 't1_005',
          state: 'review',
          reps: 5,
          lapses: 0,
          difficulty: 3.0,
          stability: 10.0,
          lastReview: 8000,
          due: 12000
        }
      };

      const remotoCards: Record<string, FlashcardFSRS> = {
        t1_005: {
          id: 't1_005',
          state: 'review',
          reps: 3,
          lapses: 0,
          difficulty: 3.0,
          stability: 8.0,
          lastReview: 8000, // Mesmo timestamp
          due: 12000
        }
      };

      const { flashcards } = resolver.reconciliarFlashcards(localCards, remotoCards);
      expect(flashcards['t1_005'].reps).toBe(5);
    });
  });

  describe('Decks Compartilhados (SharedDeckManager)', () => {
    it('deve exportar baralho com cálculo automático de checksum', () => {
      const deckExportado = sharedDecks.exportar({
        title: 'Expressões em Roma',
        description: 'Frases para usar no centro histórico',
        author: 'Mario',
        cards: [
          { palavra: 'Mamma mia', traducao: 'Nossa senhora', categoria: 'expressoes' }
        ]
      });

      expect(deckExportado.title).toBe('Expressões em Roma');
      expect(deckExportado.checksum).toBeDefined();
      expect(deckExportado.checksum.length).toBe(8);
      expect(deckExportado.cards).toHaveLength(1);
    });

    it('deve importar baralho válido e validar integridade do checksum', () => {
      const deckExportado = sharedDecks.exportar({
        title: 'Verbos Essenciais',
        cards: [{ palavra: 'andare', traducao: 'ir' }]
      });

      const res = sharedDecks.importar(JSON.stringify(deckExportado));
      expect(res.sucesso).toBe(true);
      expect(res.deck?.title).toBe('Verbos Essenciais');
    });

    it('deve rejeitar baralho com checksum adulterado', () => {
      const deckExportado = sharedDecks.exportar({
        title: 'Frutas',
        cards: [{ palavra: 'mela', traducao: 'maçã' }]
      });

      // Adulteração proposital
      deckExportado.checksum = 'deadbeef';

      const res = sharedDecks.importar(deckExportado);
      expect(res.sucesso).toBe(false);
      expect(res.erro).toContain('checksum divergente');
    });
  });

  describe('Leaderboard (Study with Friends)', () => {
    it('deve gerar ranking semanal ordenado decrescente de XP incluindo o usuário atual', () => {
      const ranking = leaderboard.getRanking({
        nome: 'Bruno',
        xp: 1100,
        streak: 12
      });

      expect(ranking.length).toBeGreaterThanOrEqual(5);
      expect(ranking[0].xpSemanal).toBeGreaterThanOrEqual(ranking[1].xpSemanal);

      const bruno = ranking.find((r) => r.isCurrentUser);
      expect(bruno).toBeDefined();
      expect(bruno?.nome).toContain('Bruno');
      expect(bruno?.xpSemanal).toBe(1100);
    });
  });

  describe('Reconciliação Integrada via Facade', () => {
    it('deve reconciliar estado completo e reportar contadores de conflitos', () => {
      const local = {
        progresso: { nivel: 1, xp: 100 } as any,
        flashcards: { c1: { reps: 1, lastReview: 100 } } as any
      };

      const remoto = {
        progresso: { nivel: 2, xp: 250 } as any,
        flashcards: { c1: { reps: 2, lastReview: 200 } } as any
      };

      const res = collaboration.reconciliar(local, remoto);
      expect(res.conflictsDetected).toBeGreaterThanOrEqual(2);
      expect(res.conflictsResolved).toBe(res.conflictsDetected);
      expect(res.updatedLocal).toBe(true);
      expect(res.mergedProgress?.xp).toBe(250);
      expect(res.mergedFlashcards?.['c1'].reps).toBe(2);
    });
  });
});
