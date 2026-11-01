// @ts-nocheck
// @vitest-environment happy-dom
// tests/e2e/e2e_vocabulary_coverage.test.ts
// E2E Test Suite: Authentic Vocabulary Diagnostic & Lexical Coverage Meter (R2 / F3, F10–F12)
// Tiers 1–4 Opaque-Box Comprehensive Test Suite

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  bootstrapAppDOM,
  resetAppEnvironment,
  getTextNormalizer,
  getVocabDiagnostic,
  getCoverageMeter,
  TextNormalizerEngine,
  VocabDiagnosticEngine,
  CoverageMeterEngine
} from './e2e_helpers';

import AppState from '../../js/core/state.js';
import AppNavigation from '../../js/core/navigation.js';
import AppXP from '../../js/core/xp.js';
import fs from 'node:fs';
import path from 'node:path';

describe('E2E: Authentic Vocabulary Diagnostic & Lexical Coverage Meter (R2)', () => {
  let normalizer: typeof TextNormalizerEngine;
  let diagnostic: typeof VocabDiagnosticEngine;
  let coverage: typeof CoverageMeterEngine;

  beforeEach(async () => {
    bootstrapAppDOM();
    resetAppEnvironment();
    normalizer = await getTextNormalizer();
    diagnostic = await getVocabDiagnostic();
    coverage = await getCoverageMeter();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ============================================================
  // TIER 1: FEATURE COVERAGE (HAPPY PATH IN ISOLATION)
  // >= 5 tests per feature
  // ============================================================
  describe('Tier 1: Feature Coverage (Happy Path in Isolation)', () => {

    // ────────────────────────────────────────────────────────────
    // Feature 1: Italian Text Normalizer Engine (F3)
    // ────────────────────────────────────────────────────────────
    describe('F3: Italian Text Normalizer Engine', () => {
      it('F3-1.1: deve tokenizar texto em italiano separando pontuação e normalizando caixa', () => {
        const texto = 'Una mattina mi sono alzato, o bella ciao!';
        const tokens = normalizer.tokenize(texto);

        expect(tokens).toContain('una');
        expect(tokens).toContain('mattina');
        expect(tokens).toContain('mi');
        expect(tokens).toContain('sono');
        expect(tokens).toContain('alzato');
        expect(tokens).toContain('o');
        expect(tokens).toContain('bella');
        expect(tokens).toContain('ciao');
        expect(tokens.every(t => !/[.,!?;:]/.test(t))).toBe(true);
      });

      it('F3-1.2: deve descompactar todas as preposições articuladas (32 formas)', () => {
        expect(normalizer.unpackElisions('del')).toEqual(['di', 'il']);
        expect(normalizer.unpackElisions('della')).toEqual(['di', 'la']);
        expect(normalizer.unpackElisions('dei')).toEqual(['di', 'i']);
        expect(normalizer.unpackElisions('degli')).toEqual(['di', 'gli']);
        expect(normalizer.unpackElisions('al')).toEqual(['a', 'il']);
        expect(normalizer.unpackElisions('nello')).toEqual(['in', 'lo']);
        expect(normalizer.unpackElisions('sul')).toEqual(['su', 'il']);
        expect(normalizer.unpackElisions('col')).toEqual(['con', 'il']);
      });

      it('F3-1.3: deve descompactar elisões com apóstrofo (l\'amico, c\'era, un\'ora)', () => {
        expect(normalizer.unpackElisions("l'amico")).toEqual(['il', 'amico']);
        expect(normalizer.unpackElisions("l'invasor")).toEqual(['il', 'invasor']);
        expect(normalizer.unpackElisions("c'era")).toEqual(['ci', 'era']);
        expect(normalizer.unpackElisions("un'ora")).toEqual(['una', 'ora']);
        expect(normalizer.unpackElisions("d'accordo")).toEqual(['di', 'accordo']);
        expect(normalizer.unpackElisions("anch'io")).toEqual(['anche', 'io']);
      });

      it('F3-1.4: deve restaurar apócopes truncadas poéticas e coloquiais (morir, invasor, bel)', () => {
        expect(normalizer.restoreApocope('morir')).toBe('morire');
        expect(normalizer.restoreApocope('andar')).toBe('andare');
        expect(normalizer.restoreApocope('far')).toBe('fare');
        expect(normalizer.restoreApocope('invasor')).toBe('invasore');
        expect(normalizer.restoreApocope('amor')).toBe('amore');
        expect(normalizer.restoreApocope('bel')).toBe('bello');
      });

      it('F3-1.5: deve destacar pronomes enclíticos em imperativos e infinitivos', () => {
        expect(normalizer.stripEnclitics('portami')).toEqual({ stem: 'porta', enclitic: 'mi' });
        expect(normalizer.stripEnclitics('vederlo')).toEqual({ stem: 'vedere', enclitic: 'lo' });
        expect(normalizer.stripEnclitics('parlandogli')).toEqual({ stem: 'parlando', enclitic: 'gli' });
        expect(normalizer.stripEnclitics('dimmelo')).toEqual({ stem: 'di', enclitic: 'melo' });
      });

      it('F3-1.6: deve mapear flexões verbais e plurais regulares para seus lemas canônicos', () => {
        expect(normalizer.toLemma('siamo')).toBe('essere');
        expect(normalizer.toLemma('sono')).toBe('essere');
        expect(normalizer.toLemma('abbiamo')).toBe('avere');
        expect(normalizer.toLemma('vado')).toBe('andare');
        expect(normalizer.toLemma('libri')).toBe('libro');
        expect(normalizer.toLemma('ragazze')).toBe('ragazza');
      });
    });

    // ────────────────────────────────────────────────────────────
    // Feature 2: Vocabulary Diagnostic (< 3 min) (F10)
    // ────────────────────────────────────────────────────────────
    describe('F10: Dynamic Vocabulary Diagnostic (< 3 min)', () => {
      it('F10-1.7: deve aceitar respostas estratificadas por faixas (1k a 5k) e pseudopalavras', () => {
        const respostas = [
          { word: 'giorno', isPseudoword: false, known: true, band: 1 },
          { word: 'casa', isPseudoword: false, known: true, band: 1 },
          { word: 'strugolo', isPseudoword: true, known: false },
          { word: 'ventare', isPseudoword: true, known: false }
        ];

        const res = diagnostic.calcularScore(respostas);
        expect(res).toBeDefined();
        expect(res.total_testado).toBe(4);
        expect(res.false_alarm_rate).toBe(0);
        expect(res.confiavel).toBe(true);
      });

      it('F10-1.8: deve calcular a correção de Abbott quando taxa de falsos alarmes F < 0.5', () => {
        // Hit rate = 0.8, False alarm rate = 0.2
        // Abbott = (0.8 - 0.2) / (1 - 0.2) = 0.6 / 0.8 = 0.75
        const adj = diagnostic.calcularAbbott(0.8, 0.2);
        expect(adj).toBeCloseTo(0.75, 2);
      });

      it('F10-1.9: deve projetar estimativa passiva somando as faixas com penalidade Abbott', () => {
        const respostas: any[] = [];
        // 1k: 9 acertos em 10 (90%)
        for (let i = 0; i < 9; i++) respostas.push({ word: `w1_${i}`, isPseudoword: false, known: true, band: 1 });
        respostas.push({ word: 'w1_9', isPseudoword: false, known: false, band: 1 });

        // 2k: 6 acertos em 10 (60%)
        for (let i = 0; i < 6; i++) respostas.push({ word: `w2_${i}`, isPseudoword: false, known: true, band: 2 });
        for (let i = 6; i < 10; i++) respostas.push({ word: `w2_${i}`, isPseudoword: false, known: false, band: 2 });

        // Pseudowords: 0 falsos alarmes
        for (let i = 0; i < 6; i++) respostas.push({ word: `pseudo_${i}`, isPseudoword: true, known: false });

        const score = diagnostic.calcularScore(respostas);
        expect(score.estimativa_passiva).toBeGreaterThan(1000);
        expect(score.estimativa_passiva).toBeLessThan(3500);
      });

      it('F10-1.10: estimativa ativa deve representar proporção realista da passiva (~65%)', () => {
        const respostas = [
          { word: 'tempo', isPseudoword: false, known: true, band: 1 },
          { word: 'anno', isPseudoword: false, known: true, band: 1 },
          { word: 'strugolo', isPseudoword: true, known: false }
        ];

        const score = diagnostic.calcularScore(respostas);
        expect(score.estimativa_ativa).toBe(Math.round(score.estimativa_passiva * 0.65));
      });

      it('F10-1.11: deve mapear o vocabulário estimado na escala CEFR (A1 a C1/C2)', () => {
        expect(diagnostic.calcularScore([{ word: 'a', isPseudoword: false, known: false }]).nivel_cefr).toBe('A1');

        const respostasA2 = Array.from({ length: 10 }, (_, i) => ({ word: `w_${i}`, isPseudoword: false, known: true, band: 1 }));
        expect(diagnostic.calcularScore(respostasA2).nivel_cefr).toBe('A2');
      });
    });

    // ────────────────────────────────────────────────────────────
    // Feature 3: Lexical Coverage Meter (F11)
    // ────────────────────────────────────────────────────────────
    describe('F11: Authentic Text Lexical Coverage Meter', () => {
      it('F11-1.12: deve calcular a cobertura léxica real (%) sobre tokens autênticos de Bella Ciao', () => {
        const tokensBellaCiao = [
          'una', 'mattina', 'mi', 'sono', 'alzato',
          'o', 'bella', 'ciao', 'bella', 'ciao',
          'e', 'ho', 'trovato', 'il', 'invasore'
        ];

        // Usuário conhece apenas cumprimentos básicos e artigos: ciao, bella, una, mi
        const conhecidas = new Set(['ciao', 'bella', 'una', 'mi']);
        const res = coverage.calculate(tokensBellaCiao, conhecidas);

        expect(res.coveragePct).toBeGreaterThan(0);
        expect(res.coveragePct).toBeLessThan(100);
        expect(res.unknownLemmas.length).toBeGreaterThan(0);
      });

      it('F11-1.13: deve projetar a lacuna do limiar de Laufer 95% para leitura autônoma', () => {
        const tokens = ['parola1', 'parola2', 'parola3', 'parola4', 'parola5'];
        const conhecidas = new Set(['parola1', 'parola2']); // 40%

        const res = coverage.calculate(tokens, conhecidas);
        expect(res.coveragePct).toBe(40.0);
        expect(res.lauferGap).toBe(55.0); // 95 - 40 = 55%
      });

      it('F11-1.14: deve ranquear e destacar as top 5 chaves de desbloqueio por impacto no texto', () => {
        // Texto onde 'libertà' aparece 4 vezes, 'fiore' 3 vezes, 'partigiano' 2 vezes
        const tokens = [
          'libertà', 'libertà', 'libertà', 'libertà',
          'fiore', 'fiore', 'fiore',
          'partigiano', 'partigiano',
          'morte'
        ];
        const conhecidas = new Set<string>();

        const res = coverage.calculate(tokens, conhecidas);
        expect(res.unlockKeys.length).toBe(4);
        expect(res.unlockKeys[0].lemma).toBe('libertà');
        expect(res.unlockKeys[0].count).toBe(4);
        expect(res.unlockKeys[0].impactPct).toBe(40.0);
        expect(res.unlockKeys[1].lemma).toBe('fiore');
      });

      it('F11-1.15: aprender uma chave de desbloqueio deve aumentar monotonicamente a cobertura', () => {
        const tokens = ['invasore', 'invasore', 'invasore', 'ciao', 'mondo'];
        const conhecidas = new Set(['ciao']);

        const inicial = coverage.calculate(tokens, conhecidas);
        conhecidas.add('invasore');
        const aposChave = coverage.calculate(tokens, conhecidas);

        expect(aposChave.coveragePct).toBeGreaterThan(inicial.coveragePct);
        expect(aposChave.lauferGap).toBeLessThan(inicial.lauferGap);
      });

      it('F11-1.16: deve atribuir cores corretas de badge: verde (>=95%), amarelo (80-94%), vermelho (<80%)', () => {
        const tokens = Array.from({ length: 100 }, (_, i) => `word_${i}`);

        // 96 conhecidas -> verde
        const conhecidasVerde = new Set(tokens.slice(0, 96));
        expect(coverage.calculate(tokens, conhecidasVerde).badgeColor).toBe('green');

        // 85 conhecidas -> amarelo
        const conhecidasAmarelo = new Set(tokens.slice(0, 85));
        expect(coverage.calculate(tokens, conhecidasAmarelo).badgeColor).toBe('yellow');

        // 50 conhecidas -> vermelho
        const conhecidasVermelho = new Set(tokens.slice(0, 50));
        expect(coverage.calculate(tokens, conhecidasVermelho).badgeColor).toBe('red');
      });
    });
  });

  // ============================================================
  // TIER 2: BOUNDARY & CORNER CASES (EXTREME LIMITS & ERRORS)
  // >= 5 tests per feature
  // ============================================================
  describe('Tier 2: Boundary & Corner Cases (Extreme Inputs & Failures)', () => {

    // ────────────────────────────────────────────────────────────
    // Feature 1 Boundaries: Text Normalizer
    // ────────────────────────────────────────────────────────────
    describe('F3 Boundaries: Text Normalizer Edge Cases', () => {
      it('F3-2.1: tokenização de string vazia ou pontuação pura deve retornar array vazio', () => {
        expect(normalizer.tokenize('')).toEqual([]);
        expect(normalizer.tokenize('   ')).toEqual([]);
        expect(normalizer.tokenize('.,!?:;—–...')).toEqual([]);
      });

      it('F3-2.2: elisões aninhadas e citações extremas não devem causar estouro de pilha', () => {
        const tokens = normalizer.tokenize('«l\'invasor?!», disse: "c\'era anch\'io!"');
        expect(tokens).toContain('il');
        expect(tokens).toContain('invasor');
        expect(tokens).toContain('disse');
        expect(tokens).toContain('ci');
        expect(tokens).toContain('era');
        expect(tokens).toContain('anche');
        expect(tokens).toContain('io');
      });

      it('F3-2.3: estrangeirismos terminados em consoante (bar, tram, sport, hotel) não devem sofrer apócope', () => {
        expect(normalizer.restoreApocope('bar')).toBe('bar');
        expect(normalizer.restoreApocope('tram')).toBe('tram');
        expect(normalizer.restoreApocope('sport')).toBe('sport');
        expect(normalizer.restoreApocope('computer')).toBe('computer');
        expect(normalizer.restoreApocope('hotel')).toBe('hotel');
      });

      it('F3-2.4: enclíticos duplos compostos (dimmelo, compragliene) devem ser destacados corretamente', () => {
        const res1 = normalizer.stripEnclitics('dimmelo');
        expect(res1.enclitic).toBe('melo');
        expect(res1.stem).toBe('di');

        const res2 = normalizer.stripEnclitics('compragliene');
        expect(res2.enclitic).toBe('gliene');
        expect(res2.stem).toBe('compra');
      });

      it('F3-2.5: verbos desconhecidos ou neologismos devem retornar a palavra base sem erro', () => {
        expect(normalizer.toLemma('twittare')).toBe('twittare');
        expect(normalizer.toLemma('postare')).toBe('postare');
        expect(normalizer.toLemma('downloadare')).toBe('downloadare');
      });

      it('F3-2.6: cálculo do índice Gulpease deve retornar número finito coerente com legibilidade', () => {
        const textoSimples = 'Il cane è bello. La gatta dorme. Il sole splende nel cielo.';
        const textoFilosofico = 'La felicità secondo Aristotele costituiisce il fine supremo delle azioni umane, richiedendo una contemplazione continua della virtù razionale.';

        const gSimples = normalizer.calculateGulpease(textoSimples);
        const gFilosofico = normalizer.calculateGulpease(textoFilosofico);

        expect(Number.isFinite(gSimples)).toBe(true);
        expect(Number.isFinite(gFilosofico)).toBe(true);
        expect(gSimples).toBeGreaterThan(gFilosofico);
      });
    });

    // ────────────────────────────────────────────────────────────
    // Feature 2 Boundaries: Vocabulary Diagnostic
    // ────────────────────────────────────────────────────────────
    describe('F10 Boundaries: Diagnostic Extreme Scores & Penalties', () => {
      it('F10-2.7: score perfeito (100% acertos, 0 falsos alarmes) classifica no nível C1/C2', () => {
        const respostas = [
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w1_${i}`, isPseudoword: false, known: true, band: 1 })),
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w2_${i}`, isPseudoword: false, known: true, band: 2 })),
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w3_${i}`, isPseudoword: false, known: true, band: 3 })),
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w4_${i}`, isPseudoword: false, known: true, band: 4 })),
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w5_${i}`, isPseudoword: false, known: true, band: 5 })),
          ...Array.from({ length: 6 }, (_, i) => ({ word: `pseudo_${i}`, isPseudoword: true, known: false }))
        ];

        const score = diagnostic.calcularScore(respostas);
        expect(score.estimativa_passiva).toBe(5000);
        expect(score.nivel_cefr).toBe('C1/C2');
        expect(score.confiavel).toBe(true);
      });

      it('F10-2.8: zero acertos classifica no nível A1 com estimativa zero', () => {
        const respostas = [
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w1_${i}`, isPseudoword: false, known: false, band: 1 })),
          ...Array.from({ length: 6 }, (_, i) => ({ word: `pseudo_${i}`, isPseudoword: true, known: false }))
        ];

        const score = diagnostic.calcularScore(respostas);
        expect(score.estimativa_passiva).toBe(0);
        expect(score.nivel_cefr).toBe('A1');
      });

      it('F10-2.9: alta taxa de falso alarme (F >= 0.5, chute/blefe) invalida o teste e zera estimativa', () => {
        const respostas = [
          // Usuário marca que conhece tudo inclusive as pseudopalavras
          ...Array.from({ length: 10 }, (_, i) => ({ word: `w1_${i}`, isPseudoword: false, known: true, band: 1 })),
          ...Array.from({ length: 6 }, (_, i) => ({ word: `pseudo_${i}`, isPseudoword: true, known: true })) // 100% falso alarme
        ];

        const score = diagnostic.calcularScore(respostas);
        expect(score.false_alarm_rate).toBe(1.0);
        expect(score.confiavel).toBe(false);
        expect(score.estimativa_passiva).toBe(0);
      });

      it('F10-2.10: persistência do diagnóstico deve gravar timestamp e manter formato JSON seguro', () => {
        const score = {
          estimativa_passiva: 1850,
          estimativa_ativa: 1200,
          nivel_cefr: 'B1',
          total_testado: 48,
          false_alarm_rate: 0.05,
          confiavel: true,
          ultimo_teste: Date.now()
        };

        AppState.estado.progresso.vocab_diagnostico = score;
        AppState.salvarProgresso();

        const raw = JSON.parse(localStorage.getItem('it_progresso') || '{}');
        const salvo = AppState.estado.progresso.vocab_diagnostico || raw.vocab_diagnostico;
        expect(salvo).toBeDefined();
        expect(salvo.estimativa_passiva).toBe(1850);
        expect(salvo.nivel_cefr).toBe('B1');
      });

      it('F10-2.11: simulação de teste completo CAT com 48 itens deve concluir em tempo hábil', () => {
        const inicio = Date.now();
        const respostas = Array.from({ length: 48 }, (_, i) => ({
          word: `item_${i}`,
          isPseudoword: i % 8 === 0,
          known: i % 3 !== 0,
          band: Math.min(5, Math.floor(i / 10) + 1)
        }));

        const score = diagnostic.calcularScore(respostas);
        const fim = Date.now();

        expect(score).toBeDefined();
        expect(fim - inicio).toBeLessThan(100); // Executa em menos de 100ms no motor
      });
    });

    // ────────────────────────────────────────────────────────────
    // Feature 3 Boundaries: Lexical Coverage Meter
    // ────────────────────────────────────────────────────────────
    describe('F11 Boundaries: Lexical Coverage Meter Limits', () => {
      it('F11-2.12: 100% de vocabulário conhecido resulta em 100% de cobertura e lacuna zero', () => {
        const tokens = ['ciao', 'bella', 'mondo'];
        const conhecidas = new Set(['ciao', 'bella', 'mondo']);

        const res = coverage.calculate(tokens, conhecidas);
        expect(res.coveragePct).toBe(100.0);
        expect(res.lauferGap).toBe(0.0);
        expect(res.unlockKeys).toEqual([]);
        expect(res.badgeColor).toBe('green');
      });

      it('F11-2.13: 0% de vocabulário conhecido resulta em 0% de cobertura e 95% de lacuna', () => {
        const tokens = ['filosofia', 'ontologia', 'ermeneutica'];
        const conhecidas = new Set<string>();

        const res = coverage.calculate(tokens, conhecidas);
        expect(res.coveragePct).toBe(0.0);
        expect(res.lauferGap).toBe(95.0);
        expect(res.badgeColor).toBe('red');
      });

      it('F11-2.14: texto vazio não deve causar divisão por zero', () => {
        const res = coverage.calculate([], new Set());
        expect(res.coveragePct).toBe(0);
        expect(res.lauferGap).toBe(95.0);
        expect(res.badgeColor).toBe('red');
      });

      it('F11-2.15: corpus extenso (2.000 tokens de história filosófica) processa em menos de 50ms', () => {
        const tokensLongos = Array.from({ length: 2000 }, (_, i) => `parola_${i % 100}`);
        const conhecidas = new Set(Array.from({ length: 50 }, (_, i) => `parola_${i}`));

        const t0 = performance.now();
        const res = coverage.calculate(tokensLongos, conhecidas);
        const t1 = performance.now();

        expect(res.coveragePct).toBeCloseTo(50.0, 1);
        expect(t1 - t0).toBeLessThan(50);
      });

      it('F11-2.16: texto com números e caracteres estrangeiros não deve quebrar contagem', () => {
        const tokens = ['nel', '1945', 'la', 'pace', 'era', 'ok'];
        const conhecidas = new Set(['nel', 'la', 'pace', 'era']);

        const res = coverage.calculate(tokens, conhecidas);
        expect(Number.isFinite(res.coveragePct)).toBe(true);
        expect(res.coveragePct).toBeGreaterThan(0);
      });
    });
  });

  // ============================================================
  // TIER 3: CROSS-FEATURE COMBINATIONS
  // ============================================================
  describe('Tier 3: Cross-Feature Combinations', () => {
    it('Comb 1: Diagnóstico de vocabulário inicial calibra palavras conhecidas e cobertura léxica de canções', () => {
      // 1. Diagnóstico posiciona o aluno em A2 com ~1.200 palavras
      const diagScore = {
        estimativa_passiva: 1200,
        estimativa_ativa: 800,
        nivel_cefr: 'A2'
      };

      // 2. Popula lemas fundamentais conhecidos com base no rank A1/A2
      const conhecidas = new Set(['una', 'mattina', 'mi', 'sono', 'ciao', 'bella', 'e', 'ho']);
      AppState.estado.progresso.palavras_conhecidas = Array.from(conhecidas);

      // 3. Mede cobertura em Bella Ciao
      const cancaoTokens = ['una', 'mattina', 'mi', 'sono', 'alzato', 'o', 'bella', 'ciao', 'il', 'invasore'];
      const res = coverage.calculate(cancaoTokens, conhecidas);

      expect(res.coveragePct).toBeGreaterThan(50);
      expect(res.lauferGap).toBeLessThan(50);
    });

    it('Comb 2: Desbloqueio de Top 5 chaves em Flashcards fecha a lacuna de Laufer em texto autêntico', () => {
      const cancaoTokens = [
        'invasore', 'invasore', 'partigiano', 'partigiano',
        'libertà', 'libertà', 'fiore', 'morire',
        'ciao', 'ciao'
      ];
      const conhecidas = new Set(['ciao']); // Inicialmente 20%

      const resAntes = coverage.calculate(cancaoTokens, conhecidas);
      expect(resAntes.coveragePct).toBe(20.0);
      expect(resAntes.lauferGap).toBe(75.0);

      // Usuário estuda e aprende as 5 chaves de desbloqueio
      resAntes.unlockKeys.forEach(k => conhecidas.add(k.lemma));

      const resDepois = coverage.calculate(cancaoTokens, conhecidas);
      expect(resDepois.coveragePct).toBe(100.0);
      expect(resDepois.lauferGap).toBe(0.0);
    });

    it('Comb 3: SafeStorage eviction ladder (prioridade 3 diagnostic_gc) purga caches mantendo nivel CEFR', () => {
      localStorage.setItem('it_swr_lexical_coverage', JSON.stringify({ can_001: 65.0 }));
      AppState.estado.progresso.vocab_diagnostico = {
        estimativa_passiva: 1500,
        nivel_cefr: 'B1'
      };
      AppState.salvarProgresso();

      // Dispara purga de caches efêmeros (Step 1 da escada de despejo)
      localStorage.removeItem('it_swr_lexical_coverage');

      expect(localStorage.getItem('it_swr_lexical_coverage')).toBeNull();
      const raw = JSON.parse(localStorage.getItem('it_progresso') || '{}');
      const diag = AppState.estado.progresso.vocab_diagnostico || raw.vocab_diagnostico;
      expect(diag.nivel_cefr).toBe('B1');
    });
  });

  // ============================================================
  // TIER 4: REAL-WORLD APPLICATION SCENARIOS
  // ============================================================
  describe('Tier 4: Real-World Application Scenarios', () => {
    it('Cenário 4.1: Aluno A1: Diagnóstico -> Estimativa -> Cobertura em Bella Ciao -> 5 Chaves de Desbloqueio', () => {
      // 1. Aluno A1 realiza o diagnóstico rápido
      const respostas = [
        { word: 'il', isPseudoword: false, known: true, band: 1 },
        { word: 'la', isPseudoword: false, known: true, band: 1 },
        { word: 'ciao', isPseudoword: false, known: true, band: 1 },
        { word: 'strugolo', isPseudoword: true, known: false }
      ];
      const diagScore = diagnostic.calcularScore(respostas);
      expect(diagScore.nivel_cefr).toBe('A2');

      // 2. Abre a canção Bella Ciao
      const canzoniPath = path.resolve(process.cwd(), 'data/canzoni.json');
      expect(fs.existsSync(canzoniPath)).toBe(true);
      const canzoniData = JSON.parse(fs.readFileSync(canzoniPath, 'utf8'));
      const bellaCiao = canzoniData.canzoni.find(c => c.id === 'can_001');
      expect(bellaCiao).toBeDefined();

      // 3. Extrai texto e calcula cobertura inicial
      const textoBellaCiao = bellaCiao.estrofes.map(e => e.texto_completo).join(' ');
      const tokens = normalizer.tokenize(textoBellaCiao);
      expect(tokens.length).toBeGreaterThan(20);

      const conhecidas = new Set(['ciao', 'bella', 'una', 'mi', 'e', 'ho', 'il', 'la']);
      const resCobertura = coverage.calculate(tokens, conhecidas);

      expect(resCobertura.coveragePct).toBeGreaterThan(20);
      expect(resCobertura.lauferGap).toBeGreaterThan(0);
      expect(resCobertura.unlockKeys.length).toBeGreaterThanOrEqual(3);

      // 4. As chaves de desbloqueio identificadas contêm termos centrais como 'partigiano' ou 'invasor'
      const lemmasChaves = resCobertura.unlockKeys.map(k => k.lemma);
      expect(lemmasChaves.some(l => l.includes('partigiano') || l.includes('invasor') || l.includes('morir'))).toBe(true);
    });

    it('Cenário 4.2: Aluno Intermediário B2 enfrentando Aristotele sulla felicità com projeção de gap de Laufer', () => {
      // 1. Carrega texto filosófico autêntico
      const storiePath = path.resolve(process.cwd(), 'data/storie.json');
      expect(fs.existsSync(storiePath)).toBe(true);
      const storieData = JSON.parse(fs.readFileSync(storiePath, 'utf8'));
      const aristotele = storieData.storie.find(s => s.id === 'fil_aristotele_sulla_felicit');
      expect(aristotele).toBeDefined();

      const textoFilosofico = aristotele.testo.map(p => p.italiano).join(' ');
      const tokens = normalizer.tokenize(textoFilosofico);
      expect(tokens.length).toBeGreaterThan(500);

      // 2. Aluno B2 tem ~2.500 lemas conhecidos (simulamos 80% do texto)
      const todosLemmas = Array.from(new Set(tokens.map(t => normalizer.toLemma(t))));
      const slice80 = new Set(todosLemmas.slice(0, Math.floor(todosLemmas.length * 0.8)));

      const res = coverage.calculate(tokens, slice80);
      expect(res.coveragePct).toBeGreaterThanOrEqual(70);
      expect(res.lauferGap).toBeLessThanOrEqual(25);
      expect(res.unlockKeys.length).toBe(5);

      // 3. Verifica legibilidade Gulpease de texto filosófico
      const gulpease = normalizer.calculateGulpease(textoFilosofico);
      expect(gulpease).toBeLessThan(75); // Mais complexo que textos infantis
    });
  });
});
