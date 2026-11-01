// ============================================================
// tests/state_whitelist_crdt.test.ts — AppState Whitelist, CRDT & Eviction Tests (F1, F2)
// Milestone 1 (F1, F2)
// ============================================================

import { describe, it, expect, beforeEach } from 'vitest';
import AppState from '../js/core/state.js';
import SafeStorage from '../js/core/storage.js';

describe('F1 & F2: AppState Whitelist, Storage & CRDT Reconciliation', () => {
  beforeEach(() => {
    // Reset mock / memory storage
    if (typeof localStorage !== 'undefined') {
      localStorage.clear();
    }
    if (SafeStorage && typeof SafeStorage._memoryFallback === 'object') {
      const fallback = SafeStorage._memoryFallback as Record<string, unknown>;
      for (const k in fallback) {
        delete fallback[k];
      }
    }
  });

  describe('1. _sanitizeProgresso Whitelist and Bounds', () => {
    it('deve retornar defaults seguros para payload vazio ou inválido', () => {
      const defaultsFromNull = AppState._sanitizeProgresso(null);
      const defaultsFromArr = AppState._sanitizeProgresso([]);
      const defaultsFromEmpty = AppState._sanitizeProgresso({});

      expect(defaultsFromEmpty.vocab_diagnostico).toBeNull();
      expect(defaultsFromEmpty.palavras_conhecidas).toEqual([]);
      expect(defaultsFromEmpty.survival_recordes).toEqual({
        maior_sequencia: 0,
        cartas_sobrevividas: 0
      });

      expect(defaultsFromNull).toEqual(defaultsFromEmpty);
      expect(defaultsFromArr).toEqual(defaultsFromEmpty);
    });

    it('deve sanitizar vocab_diagnostico corretamente', () => {
      const raw = {
        vocab_diagnostico: {
          ultimo_teste: 1730450000123.8,
          estimativa_passiva: 1250.7,
          estimativa_ativa: 820.2,
          nivel_cefr: 'B1',
          total_testado: 48.9,
          campo_invalido: 'hack'
        }
      };

      const sanitized = AppState._sanitizeProgresso(raw);
      expect(sanitized.vocab_diagnostico).toEqual({
        ultimo_teste: 1730450000123,
        estimativa_passiva: 1250,
        estimativa_ativa: 820,
        nivel_cefr: 'B1',
        total_testado: 48
      });
      // @ts-expect-error test that extraneous field was discarded
      expect(sanitized.vocab_diagnostico.campo_invalido).toBeUndefined();
    });

    it('deve aplicar fallback A1 para nivel_cefr inválido em vocab_diagnostico', () => {
      const raw = {
        vocab_diagnostico: {
          ultimo_teste: 1000,
          estimativa_passiva: 50,
          estimativa_ativa: 20,
          nivel_cefr: 'Z9', // inválido
          total_testado: 10
        }
      };

      const sanitized = AppState._sanitizeProgresso(raw);
      expect(sanitized.vocab_diagnostico?.nivel_cefr).toBe('A1');
    });

    it('deve normalizar, ordenar e deduplicar palavras_conhecidas', () => {
      const raw = {
        palavras_conhecidas: [' Roma ', 'casa', 'CASA', 'amico', '', '   ', 123, null, 'bello']
      };

      const sanitized = AppState._sanitizeProgresso(raw);
      expect(sanitized.palavras_conhecidas).toEqual(['amico', 'bello', 'casa', 'roma']);
    });

    it('deve sanitizar survival_recordes com números inteiros não-negativos', () => {
      const raw = {
        survival_recordes: {
          maior_sequencia: 18.9,
          cartas_sobrevividas: 142.3,
          tempo_recorde_ms: 65432.1,
          campo_estranho: true
        }
      };

      const sanitized = AppState._sanitizeProgresso(raw);
      expect(sanitized.survival_recordes).toEqual({
        maior_sequencia: 18,
        cartas_sobrevividas: 142,
        tempo_recorde_ms: 65432
      });
    });

    it('deve descartar qualquer propriedade fora da whitelist em progresso', () => {
      const raw = {
        xp: 350,
        nivel: 2,
        campo_malicioso: '<script>alert(1)</script>',
        token_secreto: '12345'
      };

      const sanitized = AppState._sanitizeProgresso(raw);
      expect((sanitized as Record<string, unknown>).campo_malicioso).toBeUndefined();
      expect((sanitized as Record<string, unknown>).token_secreto).toBeUndefined();
      expect(sanitized.xp).toBe(350);
      expect(sanitized.nivel).toBe(2);
    });
  });

  describe('2. CRDT Multi-Tab Reconciliation (reconciliarProgresso)', () => {
    const cleanBase = AppState._sanitizeProgresso({});

    it('Comutatividade: reconciliar(A, B) === reconciliar(B, A)', () => {
      const stA = {
        ...cleanBase,
        xp: 500,
        palavras_conhecidas: ['amico', 'rosso'],
        survival_recordes: { maior_sequencia: 10, cartas_sobrevividas: 30 },
        vocab_diagnostico: {
          ultimo_teste: 1000,
          estimativa_passiva: 800,
          estimativa_ativa: 400,
          nivel_cefr: 'A2' as const,
          total_testado: 48
        }
      };

      const stB = {
        ...cleanBase,
        xp: 650,
        palavras_conhecidas: ['bello', 'amico', 'gatto'],
        survival_recordes: { maior_sequencia: 15, cartas_sobrevividas: 20 },
        vocab_diagnostico: {
          ultimo_teste: 2000, // mais recente (vence por LWW)
          estimativa_passiva: 1200,
          estimativa_ativa: 700,
          nivel_cefr: 'B1' as const,
          total_testado: 48
        }
      };

      const resAB = AppState.reconciliarProgresso(stA, stB);
      const resBA = AppState.reconciliarProgresso(stB, stA);

      expect(resAB).toEqual(resBA);
      expect(resAB.palavras_conhecidas).toEqual(['amico', 'bello', 'gatto', 'rosso']);
      expect(resAB.survival_recordes).toEqual({ maior_sequencia: 15, cartas_sobrevividas: 30 });
      expect(resAB.vocab_diagnostico).toEqual(stB.vocab_diagnostico);
      expect(resAB.xp).toBe(650);
    });

    it('Idempotência: reconciliar(A, A) === A', () => {
      const stA = {
        ...cleanBase,
        palavras_conhecidas: ['amico', 'bello'],
        survival_recordes: { maior_sequencia: 12, cartas_sobrevividas: 45 }
      };

      const res = AppState.reconciliarProgresso(stA, stA);
      expect(res.palavras_conhecidas).toEqual(stA.palavras_conhecidas);
      expect(res.survival_recordes).toEqual(stA.survival_recordes);
    });

    it('Desempate determinístico em caso de mesmo timestamp em vocab_diagnostico', () => {
      const stA = {
        ...cleanBase,
        vocab_diagnostico: {
          ultimo_teste: 5000,
          estimativa_passiva: 1000,
          estimativa_ativa: 500,
          nivel_cefr: 'A2' as const,
          total_testado: 48
        }
      };

      const stB = {
        ...cleanBase,
        vocab_diagnostico: {
          ultimo_teste: 5000, // mesmo timestamp
          estimativa_passiva: 1200, // maior passiva vence
          estimativa_ativa: 600,
          nivel_cefr: 'B1' as const,
          total_testado: 48
        }
      };

      const resAB = AppState.reconciliarProgresso(stA, stB);
      const resBA = AppState.reconciliarProgresso(stB, stA);

      expect(resAB.vocab_diagnostico?.estimativa_passiva).toBe(1200);
      expect(resBA.vocab_diagnostico?.estimativa_passiva).toBe(1200);
      expect(resAB).toEqual(resBA);
    });
  });

  describe('3. SafeStorage Eviction Ladder & _gcDiagnostico (F2)', () => {
    it('deve podar histórico antigo de diagnósticos preservando no máximo 3 sessões', () => {
      const testHistory = [
        { id: 'sess_1', ultimo_teste: 100, respostas: ['a', 'b', 'c'] },
        { id: 'sess_2', ultimo_teste: 200, respostas: ['d', 'e'] },
        { id: 'sess_3', ultimo_teste: 300, respostas: ['f'] },
        { id: 'sess_4', ultimo_teste: 400, respostas: ['g'] },
        { id: 'sess_5', ultimo_teste: 500, respostas: ['h'] }
      ];

      SafeStorage.setItem('it_vocab_diagnostic_history', testHistory);

      const itemsPruned = AppState._gcDiagnostico(true);
      expect(itemsPruned).toBeGreaterThan(0);

      const pruned = SafeStorage.getItem('it_vocab_diagnostic_history') as Array<Record<string, unknown>>;
      expect(pruned.length).toBe(3);
      // As duas mais antigas das 3 sobreviventes tiveram respostas expurgadas
      expect(pruned[0].respostas).toBeUndefined();
      expect(pruned[1].respostas).toBeUndefined();
      // A última (mais recente) preserva respostas completas
      expect(pruned[2].respostas).toBeDefined();
    });

    it('SafeStorage.registerEvictionHandler deve sobrescrever handlers com mesmo identificador sem duplicatas', () => {
      const initialCount = SafeStorage._evictionHandlers.length;

      SafeStorage.registerEvictionHandler(3, 'test_handler', () => true);
      expect(SafeStorage._evictionHandlers.length).toBe(initialCount + 1);

      // Re-registro com mesmo nome
      SafeStorage.registerEvictionHandler(2, 'test_handler', () => false);
      expect(SafeStorage._evictionHandlers.length).toBe(initialCount + 1);

      const handlers = SafeStorage._evictionHandlers as Array<{ name: string; priority: number }>;
      const found = handlers.find(h => h.name === 'test_handler');
      expect(found?.priority).toBe(2);
    });
  });
});
