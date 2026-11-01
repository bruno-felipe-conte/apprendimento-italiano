// ============================================================
// tests/frequency.test.ts — Italian 3k Lemma Frequency Index Tests (F4)
// Milestone 1 (F4)
// ============================================================

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import AppFrequency from '../js/core/frequency.js';

describe('F4: Italian 3k Lemma Frequency Index (js/core/frequency.js)', () => {
  beforeEach(() => {
    const filePath = path.resolve(process.cwd(), 'data/frequenza_3000.json');
    if (fs.existsSync(filePath)) {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
      AppFrequency.init(data);
    }
  });

  describe('1. Invariants and Basic Lookups', () => {
    it('deve estar inicializado e conter exatamente 3.000 lemas', () => {
      expect(AppFrequency.isReady()).toBe(true);
      expect(AppFrequency.getTotal()).toBe(3000);
    });

    it('deve retornar rank 1 para "il" e rank 10 para "avere"', () => {
      expect(AppFrequency.getRank('il')).toBe(1);
      expect(AppFrequency.getRank('avere')).toBe(10);
    });

    it('deve ser case-insensitive e tolerar espaços nas bordas', () => {
      expect(AppFrequency.getRank('IL')).toBe(1);
      expect(AppFrequency.getRank('  Di  ')).toBe(2);
      expect(AppFrequency.getRank('Roma')).toBe(AppFrequency.getRank('roma'));
    });

    it('deve indexar colocações com e sem pontuação (ex: "come stai?" e "come stai")', () => {
      const rankWithQ = AppFrequency.getRank('come stai?');
      const rankWithoutQ = AppFrequency.getRank('come stai');
      expect(rankWithQ).not.toBeNull();
      expect(rankWithoutQ).toBe(rankWithQ);
    });
  });

  describe('2. Bands and Boundaries', () => {
    it('deve classificar palavras nas 4 faixas frequenciais corretamente', () => {
      expect(AppFrequency.getBand('il')).toBe('1k');
      
      const lemma1000 = AppFrequency.getLemmaAtRank(1000);
      expect(lemma1000).not.toBeNull();
      expect(AppFrequency.getBand(lemma1000!)).toBe('1k');

      const lemma1001 = AppFrequency.getLemmaAtRank(1001);
      expect(lemma1001).not.toBeNull();
      expect(AppFrequency.getBand(lemma1001!)).toBe('2k');

      const lemma2000 = AppFrequency.getLemmaAtRank(2000);
      expect(lemma2000).not.toBeNull();
      expect(AppFrequency.getBand(lemma2000!)).toBe('2k');

      const lemma2001 = AppFrequency.getLemmaAtRank(2001);
      expect(lemma2001).not.toBeNull();
      expect(AppFrequency.getBand(lemma2001!)).toBe('3k');

      const lemma3000 = AppFrequency.getLemmaAtRank(3000);
      expect(lemma3000).not.toBeNull();
      expect(AppFrequency.getBand(lemma3000!)).toBe('3k');
    });

    it('deve retornar "rare" para palavras além dos 3.000 lemas mais frequentes', () => {
      expect(AppFrequency.getRank('parolainventatasuperrara123')).toBeNull();
      expect(AppFrequency.getBand('parolainventatasuperrara123')).toBe('rare');
      expect(AppFrequency.getRankSafe('parolainventatasuperrara123')).toBe(Infinity);
      expect(AppFrequency.isCommon('parolainventatasuperrara123')).toBe(false);
    });

    it('deve retornar faixas numéricas de cada banda', () => {
      expect(AppFrequency.getBandRange('1k')).toEqual([1, 1000]);
      expect(AppFrequency.getBandRange('2k')).toEqual([1001, 2000]);
      expect(AppFrequency.getBandRange('3k')).toEqual([2001, 3000]);
      expect(AppFrequency.getBandRange('rare')).toBeNull();
    });

    it('deve retornar exatamente 1.000 lemas em cada uma das três faixas principais', () => {
      expect(AppFrequency.getLemmasInBand('1k').length).toBe(1000);
      expect(AppFrequency.getLemmasInBand('2k').length).toBe(1000);
      expect(AppFrequency.getLemmasInBand('3k').length).toBe(1000);
      expect(AppFrequency.getLemmasInBand('rare')).toEqual([]);
    });
  });

  describe('3. Defensive Guards and Edge Cases', () => {
    it('deve lidar com inputs nulos, indefinidos, vazios ou numéricos com segurança', () => {
      expect(AppFrequency.getRank('')).toBeNull();
      expect(AppFrequency.getRank('   ')).toBeNull();
      // @ts-expect-error test invalid types
      expect(AppFrequency.getRank(null)).toBeNull();
      // @ts-expect-error test invalid types
      expect(AppFrequency.getRank(undefined)).toBeNull();
      // @ts-expect-error test invalid types
      expect(AppFrequency.getRank(123)).toBeNull();

      expect(AppFrequency.getBand('')).toBe('rare');
      // @ts-expect-error test invalid types
      expect(AppFrequency.getBand(null)).toBe('rare');

      // Proteção contra a armadilha de coerção JavaScript: null <= 1000 é true, mas getRankSafe retorna Infinity
      expect(AppFrequency.getRankSafe('')).toBe(Infinity);
      // @ts-expect-error test invalid types
      expect(AppFrequency.getRankSafe(null)).toBe(Infinity);
      expect(AppFrequency.isCommon('')).toBe(false);
    });

    it('deve validar getLemmaAtRank para índices fora do intervalo [1, 3000]', () => {
      expect(AppFrequency.getLemmaAtRank(0)).toBeNull();
      expect(AppFrequency.getLemmaAtRank(-5)).toBeNull();
      expect(AppFrequency.getLemmaAtRank(3001)).toBeNull();
      // @ts-expect-error test invalid types
      expect(AppFrequency.getLemmaAtRank('1')).toBeNull();
    });
  });

  describe('4. Lexical Profiler & Sampling', () => {
    it('deve computar o perfil frequencial de um conjunto de tokens', () => {
      const tokens = ['il', 'gatto', 'casa', 'parolainexistente'];
      const profile = AppFrequency.getProfile(tokens);

      expect(profile.totalTokens).toBe(4);
      expect(profile.bandCounts['1k']).toBeGreaterThanOrEqual(2);
      expect(profile.bandCounts['rare']).toBe(1);
      expect(profile.coveredTokens).toBe(3);
      expect(profile.coveragePct).toBe(75);
    });

    it('deve retornar zeros para lista vazia de tokens', () => {
      const empty = AppFrequency.getProfile([]);
      expect(empty.totalTokens).toBe(0);
      expect(empty.coveragePct).toBe(0);
      expect(empty.coveredTokens).toBe(0);
    });

    it('deve realizar amostragem determinística da faixa usando RNG customizado', () => {
      let counter = 0;
      const fakeRng = () => {
        counter += 0.1;
        return counter % 1;
      };

      const sample = AppFrequency.sampleBand('1k', 5, fakeRng);
      expect(sample.length).toBe(5);
      expect(new Set(sample).size).toBe(5);
      for (const word of sample) {
        expect(AppFrequency.getBand(word)).toBe('1k');
      }
    });
  });
});
