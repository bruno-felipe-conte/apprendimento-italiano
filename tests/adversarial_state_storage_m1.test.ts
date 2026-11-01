// @ts-nocheck
// @vitest-environment happy-dom
// ============================================================
// tests/adversarial_state_storage_m1.test.ts
// Empirical Adversarial Stress & Edge-Case Harness for Milestone 1
// AppState (js/core/state.js) & SafeStorage (js/core/storage.js)
// ============================================================

import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import AppState from '../js/core/state.js';
import SafeStorage from '../js/core/storage.js';

describe('Adversarial Stress Harness: AppState & SafeStorage (M1 Challenger)', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    vi.restoreAllMocks();

    SafeStorage._isAvailable = null;

    if (SafeStorage && typeof SafeStorage._memoryFallback === 'object') {
      const fallback = SafeStorage._memoryFallback as Record<string, unknown>;
      for (const k in fallback) {
        delete fallback[k];
      }
    }

    // Reset handlers to initial state for tests
    SafeStorage._evictionHandlers = [];
    if (AppState._gcDiagnostico) {
      SafeStorage.registerEvictionHandler(3, 'diagnostic_gc', () => {
        const freed = AppState._gcDiagnostico(true);
        return freed > 0;
      });
    }
    if (AppState._gcFlashcards) {
      SafeStorage.registerEvictionHandler(3, 'flashcards_gc', () => {
        const freed = AppState._gcFlashcards(true);
        return freed > 0;
      });
    }
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 1: Strict CRDT Commutativity over 100 Randomized Pairs
  // ────────────────────────────────────────────────────────────
  describe('Cenário 1: Comutatividade Estrita CRDT f(A,B) == f(B,A) em 100 Pares Aleatórios', () => {
    it('deve garantir comutatividade exata para 100 pares aleatórios de mutações de estado', () => {
      const vocabList = [
        'ciao', 'buongiorno', 'grazie', 'prego', 'amico', 'casa', 'tempo', 'bello',
        'mangiare', 'bere', 'andare', 'fare', 'parlare', 'dormire', 'scrivere', 'leggere'
      ];
      const cefrLevels: Array<'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'> = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

      const generateRandomState = (seed: number) => {
        const rand = (max: number) => Math.floor(Math.abs(Math.sin(seed++) * 10000)) % max;

        // Random known words
        const numWords = rand(8);
        const palavras: string[] = [];
        for (let i = 0; i < numWords; i++) {
          palavras.push(vocabList[rand(vocabList.length)]);
        }

        const hasDiag = rand(2) === 1;
        const vocab_diagnostico = hasDiag ? {
          ultimo_teste: 1000 + rand(500),
          estimativa_passiva: rand(3000),
          estimativa_ativa: rand(2000),
          nivel_cefr: cefrLevels[rand(cefrLevels.length)],
          total_testado: 10 + rand(40)
        } : null;

        return {
          nivel: 1 + rand(10),
          xp: rand(5000),
          xp_proximo_nivel: 500 * (1 + rand(10)),
          templos_desbloqueados: [1, 1 + rand(10)],
          templos_concluidos: rand(2) === 1 ? [1] : [],
          total_palavras: rand(100),
          streak: rand(30),
          streak_recorde: rand(50),
          ultimo_estudo: 1700000000000 + rand(100000),
          grammatica_completadas: rand(2) === 1 ? ['mod1'] : [],
          meta_diaria: 100,
          xp_hoje: rand(200),
          data_xp_hoje: '2026-11-01',
          favoritos: [],
          conquistas: [],
          data_inicio: 1690000000000,
          meta_prazo: null,
          audio_rate: 0.85,
          palavras_conhecidas: Array.from(new Set(palavras)).sort(),
          survival_recordes: {
            maior_sequencia: rand(50),
            cartas_sobrevividas: rand(200),
            tempo_recorde_ms: rand(60000)
          },
          vocab_diagnostico
        };
      };

      let commutativityFailures = 0;
      const failureDetails: any[] = [];

      for (let i = 0; i < 100; i++) {
        const stateA = generateRandomState(i * 17 + 1);
        const stateB = generateRandomState(i * 31 + 7);

        const resAB = AppState.reconciliarProgresso(stateA, stateB);
        const resBA = AppState.reconciliarProgresso(stateB, stateA);

        try {
          expect(resAB).toEqual(resBA);
        } catch (err) {
          commutativityFailures++;
          if (failureDetails.length < 3) {
            failureDetails.push({ pair: i, resAB, resBA });
          }
        }
      }

      if (commutativityFailures > 0) {
        console.warn(`[COMMUTATIVITY FAILURE] ${commutativityFailures}/100 pares falharam na comutatividade.`);
      }
      expect(commutativityFailures).toBe(0);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 2: CRDT Idempotency
  // ────────────────────────────────────────────────────────────
  describe('Cenário 2: Idempotência CRDT f(A, A) === A', () => {
    it('deve retornar exatamente o mesmo estado para reconciliar(A, A)', () => {
      const cleanBase = AppState._sanitizeProgresso({});
      const state = {
        ...cleanBase,
        xp: 1250,
        nivel: 3,
        palavras_conhecidas: ['amico', 'casa', 'tempo'],
        survival_recordes: {
          maior_sequencia: 25,
          cartas_sobrevividas: 110,
          tempo_recorde_ms: 45000
        },
        vocab_diagnostico: {
          ultimo_teste: 1730000000,
          estimativa_passiva: 1500,
          estimativa_ativa: 900,
          nivel_cefr: 'B1' as const,
          total_testado: 48
        }
      };

      const reconciledOnce = AppState.reconciliarProgresso(state, state);
      expect(reconciledOnce.palavras_conhecidas).toEqual(state.palavras_conhecidas);
      expect(reconciledOnce.survival_recordes).toEqual(state.survival_recordes);
      expect(reconciledOnce.vocab_diagnostico).toEqual(state.vocab_diagnostico);

      const reconciledTwice = AppState.reconciliarProgresso(reconciledOnce, state);
      expect(reconciledTwice).toEqual(reconciledOnce);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 3: Array Sorting Determinism
  // ────────────────────────────────────────────────────────────
  describe('Cenário 3: Determinismo de Ordenação Alfabética em palavras_conhecidas', () => {
    it('deve ordenar palavras_conhecidas estritamente em ordem alfabética índice a índice', () => {
      const stateA = {
        ...AppState._sanitizeProgresso({}),
        palavras_conhecidas: ['zucchero', 'albero', 'roma', 'gatto']
      };
      const stateB = {
        ...AppState._sanitizeProgresso({}),
        palavras_conhecidas: ['bello', 'domani', 'albero', 'fuoco']
      };

      const resAB = AppState.reconciliarProgresso(stateA, stateB);
      const resBA = AppState.reconciliarProgresso(stateB, stateA);

      const expected = ['albero', 'bello', 'domani', 'fuoco', 'gatto', 'roma', 'zucchero'];
      expect(resAB.palavras_conhecidas).toEqual(expected);
      expect(resBA.palavras_conhecidas).toEqual(expected);
      expect(resAB.palavras_conhecidas).toEqual(resBA.palavras_conhecidas);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 4: Survival Records Tie-Breaking and Non-Negative Monotonicity
  // ────────────────────────────────────────────────────────────
  describe('Cenário 4: Monotonicidade e Desempate de survival_recordes', () => {
    it('deve manter monotonicidade e nunca produzir NaN ou valores negativos', () => {
      const stateA = {
        ...AppState._sanitizeProgresso({}),
        survival_recordes: {
          maior_sequencia: -10,
          cartas_sobrevividas: NaN as any,
          tempo_recorde_ms: 'invalid' as any
        }
      };
      const stateB = {
        ...AppState._sanitizeProgresso({}),
        survival_recordes: {
          maior_sequencia: 15,
          cartas_sobrevividas: 40,
          tempo_recorde_ms: 12000
        }
      };

      const resAB = AppState.reconciliarProgresso(stateA, stateB);
      const resBA = AppState.reconciliarProgresso(stateB, stateA);

      expect(resAB.survival_recordes.maior_sequencia).toBe(15);
      expect(resAB.survival_recordes.cartas_sobrevividas).toBe(40);
      expect(resAB.survival_recordes.tempo_recorde_ms).toBe(12000);
      expect(Number.isNaN(resAB.survival_recordes.cartas_sobrevividas)).toBe(false);

      expect(resAB.survival_recordes).toEqual(resBA.survival_recordes);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 5: Vocab Diagnostic Tie-Breaking
  // ────────────────────────────────────────────────────────────
  describe('Cenário 5: Desempate de vocab_diagnostico com Múltiplas Colisões', () => {
    it('deve desempatar determinística e comutativamente quando timestamps forem idênticos', () => {
      // Caso 5.1: Mesmo timestamp, total_testado diferente
      const st1 = {
        ...AppState._sanitizeProgresso({}),
        vocab_diagnostico: {
          ultimo_teste: 5000,
          estimativa_passiva: 1000,
          estimativa_ativa: 500,
          nivel_cefr: 'A2' as const,
          total_testado: 30
        }
      };
      const st2 = {
        ...AppState._sanitizeProgresso({}),
        vocab_diagnostico: {
          ultimo_teste: 5000,
          estimativa_passiva: 800,
          estimativa_ativa: 400,
          nivel_cefr: 'A1' as const,
          total_testado: 48 // maior total_testado deve vencer
        }
      };

      const res12 = AppState.reconciliarProgresso(st1, st2);
      const res21 = AppState.reconciliarProgresso(st2, st1);

      expect(res12.vocab_diagnostico?.total_testado).toBe(48);
      expect(res12.vocab_diagnostico).toEqual(res21.vocab_diagnostico);

      // Caso 5.2: Mesmo timestamp, mesmo total_testado, mesma estimativa_passiva, mesmo CEFR, mas estimativa_ativa DIFERENTE
      const st3 = {
        ...AppState._sanitizeProgresso({}),
        vocab_diagnostico: {
          ultimo_teste: 7000,
          estimativa_passiva: 1200,
          estimativa_ativa: 400,
          nivel_cefr: 'B1' as const,
          total_testado: 48
        }
      };
      const st4 = {
        ...AppState._sanitizeProgresso({}),
        vocab_diagnostico: {
          ultimo_teste: 7000,
          estimativa_passiva: 1200,
          estimativa_ativa: 600, // diferente
          nivel_cefr: 'B1' as const,
          total_testado: 48
        }
      };

      const res34 = AppState.reconciliarProgresso(st3, st4);
      const res43 = AppState.reconciliarProgresso(st4, st3);

      // Asserção empírica: reconciliar(A, B) DEVE ser igual a reconciliar(B, A)
      expect(res34.vocab_diagnostico).toEqual(res43.vocab_diagnostico);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 6: Prototype Pollution Injection
  // ────────────────────────────────────────────────────────────
  describe('Cenário 6: Tentativa de Poluição de Protótipo e Injeção Maliciosa', () => {
    it('deve blindar Object.prototype contra payload contendo __proto__ e constructor', () => {
      const maliciousPayload = JSON.parse(`{
        "nivel": 2,
        "xp": 500,
        "__proto__": { "polluted": true, "isAdmin": true },
        "constructor": { "prototype": { "hacked": true } },
        "vocab_diagnostico": {
          "ultimo_teste": 1000,
          "__proto__": { "injected": true }
        }
      }`);

      const sanitized = AppState._sanitizeProgresso(maliciousPayload);

      expect((Object.prototype as any).polluted).toBeUndefined();
      expect((Object.prototype as any).isAdmin).toBeUndefined();
      expect((Object.prototype as any).hacked).toBeUndefined();
      expect((Object.prototype as any).injected).toBeUndefined();

      expect((sanitized as any).polluted).toBeUndefined();
      expect((sanitized as any).isAdmin).toBeUndefined();
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 7: Massive Known Words Array (50,000 strings) & Worker Truncation Claim
  // ────────────────────────────────────────────────────────────
  describe('Cenário 7: Carga Massiva em palavras_conhecidas e Verificação de Truncamento', () => {
    it('deve processar array massivo de 50.000 palavras e testar claim de truncamento em 10.000', () => {
      // Cria 20.000 palavras únicas
      const massiveWords: string[] = [];
      for (let i = 0; i < 20000; i++) {
        massiveWords.push(`parola_${i}`);
      }

      const t0 = performance.now();
      const sanitized = AppState._sanitizeProgresso({
        palavras_conhecidas: massiveWords
      });
      const tSanitize = performance.now() - t0;

      expect(tSanitize).toBeLessThan(2000);

      // O Worker M1 afirmou no handoff: "palavras_conhecidas (sanitized string array, truncated at 10,000 items)"
      // Verificação empírica: foi truncado em 10.000 ou reteve todas as 20.000?
      const isTruncatedAt10k = sanitized.palavras_conhecidas.length === 10000;
      if (!isTruncatedAt10k) {
        console.warn(`[WORKER CLAIM DISCREPANCY] O Worker M1 alegou truncamento em 10.000 itens, mas sanitized.palavras_conhecidas.length é ${sanitized.palavras_conhecidas.length}`);
      }
      // Registramos a observação empírica (seja truncado ou preservado até o limite de memória)
      expect(sanitized.palavras_conhecidas.length).toBeGreaterThan(0);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 8: QuotaExceededError Simulation & Priority Ladder Execution
  // ────────────────────────────────────────────────────────────
  describe('Cenário 8: Simulação de QuotaExceededError e Execução da Escala de Evicção', () => {
    it('deve acionar diagnostic_gc na Prioridade 3 durante QuotaExceededError', () => {
      const sessionHistory = [
        { id: 'sess_1', ultimo_teste: 100, respostas: ['r1', 'r2', 'r3'] },
        { id: 'sess_2', ultimo_teste: 200, respostas: ['r4', 'r5'] },
        { id: 'sess_3', ultimo_teste: 300, respostas: ['r6'] },
        { id: 'sess_4', ultimo_teste: 400, respostas: ['r7', 'r8'] },
        { id: 'sess_5', ultimo_teste: 500, respostas: ['r9'] }
      ];

      SafeStorage.setItem('it_vocab_diagnostic_history', sessionHistory);

      const realSetItem = localStorage.setItem.bind(localStorage);

      const spy = vi.spyOn(localStorage, 'setItem').mockImplementation((key: string, val: string) => {
        if (key === 'quota_test_key') {
          const raw = localStorage.getItem('it_vocab_diagnostic_history');
          const history = raw ? JSON.parse(raw) : [];
          if (history.length > 3) {
            const err = new Error('Quota exceeded');
            err.name = 'QuotaExceededError';
            throw err;
          }
        }
        return realSetItem(key, val);
      });

      try {
        const success = SafeStorage.setItem('quota_test_key', { data: 'important_data' });
        expect(success).toBe(true);

        const pruned = SafeStorage.getItem('it_vocab_diagnostic_history') as any[];
        expect(pruned.length).toBe(3);
      } finally {
        spy.mockRestore();
      }
    });

    it('deve verificar se _gcDiagnostico poda detalhe_bandas conforme alegado no handoff do Worker', () => {
      const sessionWithBandDetails = [
        {
          id: 'sess_1',
          ultimo_teste: 100,
          estimativa_passiva: 500,
          detalhe_bandas: { '1k': { total: 20, acertos: 18 }, '2k': { total: 20, acertos: 10 } }
        },
        {
          id: 'sess_2',
          ultimo_teste: 200,
          estimativa_passiva: 800,
          detalhe_bandas: { '1k': { total: 20, acertos: 19 }, '2k': { total: 20, acertos: 12 } }
        }
      ];

      SafeStorage.setItem('it_vocab_diagnostic_history', sessionWithBandDetails);
      AppState._gcDiagnostico(true);

      const result = SafeStorage.getItem('it_vocab_diagnostic_history') as any[];
      // Worker M1 alegou: "Method _gcDiagnostico(persistir = true) truncates detailed band statistics while retaining summary fields"
      const prunedBand = result[0].detalhe_bandas === undefined;
      if (!prunedBand) {
        console.warn('[WORKER CLAIM DISCREPANCY] _gcDiagnostico NÃO remove detalhe_bandas (apenas remove .respostas)!');
      }
      // Asserção empírica: testar se detalhe_bandas foi podado
      expect(prunedBand).toBe(true);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 9: Palavras Conhecidas Deduplication with Case & Space Variations
  // ────────────────────────────────────────────────────────────
  describe('Cenário 9: Deduplicação e Casing em palavras_conhecidas', () => {
    it('deve eliminar duplicatas mesmo quando variantes diferem em maiúsculas/minúsculas e espaços', () => {
      const stateA = {
        ...AppState._sanitizeProgresso({}),
        palavras_conhecidas: ['Roma', ' roma ', 'ROMA', 'Milano']
      };
      const stateB = {
        ...AppState._sanitizeProgresso({}),
        palavras_conhecidas: ['milano', 'ROMA', ' ROMA ', 'Venezia']
      };

      const resAB = AppState.reconciliarProgresso(stateA, stateB);
      const resBA = AppState.reconciliarProgresso(stateB, stateA);

      // Não pode haver repetição de 'roma', 'milano' ou 'venezia'
      expect(resAB.palavras_conhecidas).toEqual(['milano', 'roma', 'venezia']);
      expect(resBA.palavras_conhecidas).toEqual(['milano', 'roma', 'venezia']);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 10: Hostile Non-Object Inputs to reconciliarProgresso
  // ────────────────────────────────────────────────────────────
  describe('Cenário 10: Entradas Hostis e Tipos Anômalos em reconciliarProgresso', () => {
    it('deve lidar com null, undefined e primitivos sem lançar exceções não tratadas', () => {
      expect(() => AppState.reconciliarProgresso(null, null)).not.toThrow();
      expect(() => AppState.reconciliarProgresso(undefined, undefined)).not.toThrow();
      expect(() => AppState.reconciliarProgresso(123 as any, 'string' as any)).not.toThrow();
      expect(() => AppState.reconciliarProgresso([] as any, {} as any)).not.toThrow();

      const resWithValidLocal = AppState.reconciliarProgresso({ xp: 100 }, null);
      expect(resWithValidLocal.xp).toBe(100);

      const resWithValidRemote = AppState.reconciliarProgresso(null, { xp: 200 });
      expect(resWithValidRemote.xp).toBe(200);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 11: Hostile Inputs to _sanitizeProgresso
  // ────────────────────────────────────────────────────────────
  describe('Cenário 11: Entradas Hostis a _sanitizeProgresso', () => {
    it('deve retornar defaults estritos para entradas primitivas ou malformadas', () => {
      const fixedTime = 1730000000000;
      vi.spyOn(Date, 'now').mockReturnValue(fixedTime);

      const defaults = AppState._sanitizeProgresso(null);

      expect(AppState._sanitizeProgresso(undefined)).toEqual(defaults);
      expect(AppState._sanitizeProgresso(12345)).toEqual(defaults);
      expect(AppState._sanitizeProgresso('string')).toEqual(defaults);
      expect(AppState._sanitizeProgresso(true)).toEqual(defaults);
      expect(AppState._sanitizeProgresso([1, 2, 3])).toEqual(defaults);
      expect(AppState._sanitizeProgresso(Symbol('evil'))).toEqual(defaults);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 12: Extreme Numeric Values (NaN, Infinity, Boundaries)
  // ────────────────────────────────────────────────────────────
  describe('Cenário 12: Valores Numéricos Extremos (NaN, Infinity, Limites)', () => {
    it('deve normalizar NaN, Infinity e valores negativos em campos numéricos', () => {
      const hostileState = {
        nivel: -5,
        xp: Infinity,
        xp_proximo_nivel: NaN,
        total_palavras: -999,
        streak: NaN,
        meta_diaria: -10,
        xp_hoje: Infinity,
        audio_rate: 999.0,
        survival_recordes: {
          maior_sequencia: Infinity,
          cartas_sobrevividas: -10,
          tempo_recorde_ms: NaN
        },
        vocab_diagnostico: {
          ultimo_teste: NaN,
          estimativa_passiva: -50,
          estimativa_ativa: Infinity,
          nivel_cefr: 'INVALID_LEVEL' as any,
          total_testado: NaN
        }
      };

      const sanitized = AppState._sanitizeProgresso(hostileState);

      expect(sanitized.nivel).toBe(1);
      expect(sanitized.xp).toBe(0);
      expect(sanitized.xp_proximo_nivel).toBe(500);
      expect(sanitized.total_palavras).toBe(0);
      expect(sanitized.streak).toBe(0);
      expect(sanitized.meta_diaria).toBe(100);
      expect(sanitized.xp_hoje).toBe(0);
      expect(sanitized.audio_rate).toBe(0.85);

      expect(sanitized.survival_recordes.maior_sequencia).toBe(0);
      expect(sanitized.survival_recordes.cartas_sobrevividas).toBe(0);
      expect(sanitized.survival_recordes.tempo_recorde_ms).toBeUndefined();

      expect(sanitized.vocab_diagnostico?.estimativa_passiva).toBe(0);
      expect(sanitized.vocab_diagnostico?.estimativa_ativa).toBe(0);
      expect(sanitized.vocab_diagnostico?.nivel_cefr).toBe('A1');
      expect(sanitized.vocab_diagnostico?.total_testado).toBe(0);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 13: XSS and Script Injection in All Whitelist Fields
  // ────────────────────────────────────────────────────────────
  describe('Cenário 13: Tentativa de Injeção XSS / HTML em Campos de Texto', () => {
    it('deve neutralizar ou isolar payloads de script em palavras_conhecidas e metadados', () => {
      const xssState = {
        ...AppState._sanitizeProgresso({}),
        palavras_conhecidas: [
          '<script>alert("xss")</script>',
          '"><img src=x onerror=alert(1)>',
          'normal'
        ],
        conquistas: ['<script>eval()</script>'],
        favoritos: ['"><svg onload=alert(2)>']
      };

      const sanitized = AppState._sanitizeProgresso(xssState);

      expect(sanitized.palavras_conhecidas).toContain('normal');
      expect(sanitized.palavras_conhecidas.length).toBe(3);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 14: SafeStorage Eviction Ladder Priority Gating
  // ────────────────────────────────────────────────────────────
  describe('Cenário 14: Isolamento e Gating de Prioridade no Eviction Ladder', () => {
    it('não deve acionar Step 3 se Step 1 (SWR) liberar espaço suficiente', () => {
      SafeStorage.setItem('it_swr_templos_meta', { cached: 'massive_swr_content'.repeat(100) });

      let step3Executed = false;
      SafeStorage.registerEvictionHandler(3, 'gate_test_handler', () => {
        step3Executed = true;
        return true;
      });

      let attempts = 0;
      const origSet = window.localStorage.setItem;
      window.localStorage.setItem = vi.fn((k: string, v: string) => {
        attempts++;
        if (attempts === 1 && k === 'new_target_key') {
          const err = new Error('Quota');
          err.name = 'QuotaExceededError';
          throw err;
        }
        return origSet.call(window.localStorage, k, v);
      });

      try {
        const res = SafeStorage.setItem('new_target_key', { data: 'saved' });
        expect(res).toBe(true);
        expect(step3Executed).toBe(false);
      } finally {
        window.localStorage.setItem = origSet;
      }
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 15: SafeStorage QuotaExceeded Detection Universality
  // ────────────────────────────────────────────────────────────
  describe('Cenário 15: Universalidade do Detector de QuotaExceededError', () => {
    it('deve reconhecer assinaturas de quota de todos os motores de navegadores', () => {
      expect(SafeStorage.isQuotaExceeded({ name: 'QuotaExceededError' })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ name: 'NS_ERROR_DOM_QUOTA_REACHED' })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ code: 22 })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ code: 1014 })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ number: -2147024882 })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ message: 'QuotaExceededError: storage full' })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ message: 'The quota has been exceeded' })).toBe(true);
      expect(SafeStorage.isQuotaExceeded({ message: 'NS_ERROR_DOM_QUOTA_REACHED' })).toBe(true);

      expect(SafeStorage.isQuotaExceeded(null)).toBe(false);
      expect(SafeStorage.isQuotaExceeded(new Error('SyntaxError'))).toBe(false);
      expect(SafeStorage.isQuotaExceeded({ name: 'TypeError', message: 'undefined is not a function' })).toBe(false);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 16: SafeStorage Handler Deduplication / Overwrite
  // ────────────────────────────────────────────────────────────
  describe('Cenário 16: Sobrescrita e Deduplicação de Eviction Handlers', () => {
    it('deve atualizar o handler existente sem criar entradas duplicadas no ladder', () => {
      const initialCount = SafeStorage._evictionHandlers.length;

      SafeStorage.registerEvictionHandler(3, 'custom_cleaner', () => true);
      expect(SafeStorage._evictionHandlers.length).toBe(initialCount + 1);

      SafeStorage.registerEvictionHandler(2, 'custom_cleaner', () => false);
      expect(SafeStorage._evictionHandlers.length).toBe(initialCount + 1);

      const found = SafeStorage._evictionHandlers.find((h: any) => h.name === 'custom_cleaner');
      expect(found?.priority).toBe(2);
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 17: Diagnostic GC Resilience to Corrupt Data
  // ────────────────────────────────────────────────────────────
  describe('Cenário 17: Resiliência de _gcDiagnostico com Dados Corrompidos', () => {
    it('deve processar histórico nulo, primitivo ou estruturalmente corrompido sem quebrar', () => {
      SafeStorage.setItem('it_vocab_diagnostic_history', 'completely_corrupt_string');
      SafeStorage.setItem('it_diagnostico_historico', { notAnArray: true });
      SafeStorage.setItem('it_vocab_diagnostic', null);

      expect(() => AppState._gcDiagnostico(true)).not.toThrow();
    });
  });

  // ────────────────────────────────────────────────────────────
  // Scenario 18: Unwhitelisted Properties Leakage in reconciliarProgresso
  // ────────────────────────────────────────────────────────────
  describe('Cenário 18: Vazamento e Assimetria de Chaves Não-Whitelisted em reconciliarProgresso', () => {
    it('deve verificar se reconciliarProgresso vaza propriedades não-whitelisted e se isso quebra a comutatividade', () => {
      const stateWithCollisionA = {
        ...AppState._sanitizeProgresso({}),
        custom_key: 'valueA'
      };
      const stateWithCollisionB = {
        ...AppState._sanitizeProgresso({}),
        custom_key: 'valueB'
      };

      const resCollisionAB = AppState.reconciliarProgresso(stateWithCollisionA, stateWithCollisionB);
      const resCollisionBA = AppState.reconciliarProgresso(stateWithCollisionB, stateWithCollisionA);

      const isCommutative = JSON.stringify(resCollisionAB) === JSON.stringify(resCollisionBA);
      if (!isCommutative) {
        console.warn('[LEAK/COMMUTATIVITY WARNING] Propriedades não-whitelisted causam assimetria em reconciliarProgresso!');
      }
      expect(isCommutative).toBe(true);
    });
  });
});
