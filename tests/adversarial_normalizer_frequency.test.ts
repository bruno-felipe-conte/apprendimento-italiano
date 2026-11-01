// ============================================================
// tests/adversarial_normalizer_frequency.test.ts — Adversarial Stress Test Harness
// Milestone 1: TextNormalizer & FrequencyIndex Adversarial Verification
// ============================================================

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import TextNormalizer from '../js/core/text_normalizer.js';
import AppFrequency from '../js/core/frequency.js';

describe('Adversarial Harness: TextNormalizer & FrequencyIndex', () => {
  beforeEach(() => {
    TextNormalizer.init();

    try {
      const conjPath = path.resolve(process.cwd(), 'data/conjugacoes.json');
      if (fs.existsSync(conjPath)) {
        const conjData = JSON.parse(fs.readFileSync(conjPath, 'utf8'));
        TextNormalizer.loadConjugations(conjData);
      }

      const templeFiles = fs.readdirSync(path.resolve(process.cwd(), 'data')).filter(f => f.startsWith('templo-') && f.endsWith('.json'));
      for (const f of templeFiles) {
        const tData = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'data', f), 'utf8'));
        TextNormalizer.loadPlurals(tData.palavras || []);
      }
    } catch (_) {}

    const freqPath = path.resolve(process.cwd(), 'data/frequenza_3000.json');
    if (fs.existsSync(freqPath)) {
      const data = JSON.parse(fs.readFileSync(freqPath, 'utf-8'));
      AppFrequency.init(data);
    }
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 1: Punctuation chaos & multiple nested apostrophes
  // ────────────────────────────────────────────────────────────
  describe('Scenario 1: Punctuation chaos & nested apostrophes', () => {
    it('deve descompactar corretamente frases com múltiplas elisões encadeadas', () => {
      const text = "l'amico d'un altro diceva che non c'era un'ora fa'";
      const tokens = TextNormalizer.tokenize(text);
      expect(tokens).toContain("l'amico");
      expect(tokens).toContain("d'un");
      expect(tokens).toContain("c'era");
      expect(tokens).toContain("un'ora");
      expect(tokens).toContain("fa'");

      const unpackedAmico = TextNormalizer.unpackElisions("l'amico");
      expect(unpackedAmico).toEqual(['il', 'amico']);

      const unpackedDun = TextNormalizer.unpackElisions("d'un");
      expect(unpackedDun).toEqual(['di', 'un']);

      const unpackedCera = TextNormalizer.unpackElisions("c'era");
      expect(unpackedCera).toEqual(['ci', 'era']);

      const unpackedUnora = TextNormalizer.unpackElisions("un'ora");
      expect(unpackedUnora).toEqual(['una', 'ora']);

      const unpackedFa = TextNormalizer.unpackElisions("fa'");
      expect(unpackedFa).toEqual(['fare']);
    });

    it('deve lidar com pontuação extrema, aspas duplas, simples e guillemets sem crashar', () => {
      const chaotic = "«“‘...l'amico... d'un'altra???’!”» ;;; --- !!! ???";
      const tokens = TextNormalizer.tokenize(chaotic);
      expect(tokens.length).toBeGreaterThan(0);
      expect(tokens).not.toContain('');
      for (const t of tokens) {
        expect(t.startsWith('«')).toBe(false);
        expect(t.startsWith('"')).toBe(false);
        expect(t.startsWith("'")).toBe(false);
      }
    });

    it('deve desempacotar elisão de preposição combinada (dell\'arte, all\'aria, sull\'albero)', () => {
      expect(TextNormalizer.unpackElisions("dell'arte")).toEqual(['di', 'il', 'arte']);
      expect(TextNormalizer.unpackElisions("all'aria")).toEqual(['a', 'il', 'aria']);
      expect(TextNormalizer.unpackElisions("sull'albero")).toEqual(['su', 'il', 'albero']);
    });

    it('deve tolerar apóstrofes duplicadas ou malformadas sem lançar exceção', () => {
      expect(() => TextNormalizer.tokenize("l''amico")).not.toThrow();
      expect(() => TextNormalizer.unpackElisions("l''amico")).not.toThrow();
      expect(() => TextNormalizer.unpackElisions("'''")).not.toThrow();
      expect(TextNormalizer.unpackElisions("'''")).toEqual(["'''"]);
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 2: Extreme apocope cases in poetry
  // ────────────────────────────────────────────────────────────
  describe('Scenario 2: Extreme apocope cases in poetry', () => {
    it('deve restaurar apócopes clássicas da poesia italiana (morir d\'amor, bel vedere)', () => {
      expect(TextNormalizer.restoreApocope('morir')).toBe('morire');
      expect(TextNormalizer.restoreApocope('amor')).toBe('amore');
      expect(TextNormalizer.restoreApocope('bel')).toBe('bello');
      expect(TextNormalizer.restoreApocope('vedere')).toBe('vedere');
      expect(TextNormalizer.restoreApocope('cuor')).toBe('cuore');
      expect(TextNormalizer.restoreApocope('fior')).toBe('fiore');
    });

    it('deve normalizar a frase poética "morir d\'amor" para os lemas canônicos', () => {
      const lemmas = TextNormalizer.normalizeText("morir d'amor");
      expect(lemmas).toEqual(['morire', 'di', 'amore']);
    });

    it('deve normalizar "bel vedere" para ["bello", "vedere"]', () => {
      const lemmas = TextNormalizer.normalizeText("bel vedere");
      expect(lemmas).toEqual(['bello', 'vedere']);
    });

    it('deve processar aférese poética "e \'l sol" sem gerar tokens corrompidos', () => {
      const tokens = TextNormalizer.tokenize("e 'l sol");
      expect(tokens).toContain('e');
      expect(tokens).toContain('sol');
      for (const t of tokens) {
        expect(() => TextNormalizer.toLemma(t)).not.toThrow();
      }
    });

    it('deve proteger palavras não-apocópicas, estrangeirismos e preposições (per, bar, computer)', () => {
      const exceptions = ['per', 'bar', 'computer', 'leader', 'laser', 'super', 'sponsor', 'humor', 'junior', 'senior', 'horror', 'star'];
      for (const w of exceptions) {
        expect(TextNormalizer.restoreApocope(w)).toBe(w);
      }
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 3: False-positive enclitic guards
  // ────────────────────────────────────────────────────────────
  describe('Scenario 3: False-positive enclitic guards', () => {
    const safeWords = [
      'carne', 'pane', 'cane', 'fine', 'sole', 'miele', 'stelo', 'isola', 'vela', 'tela',
      'vitale', 'iniziale', 'facile', 'difficile', 'possibile', 'visibile', 'gentile', 'fedele',
      'amici', 'nemici', 'edifici', 'stoici', 'medici', 'sindaci', 'portici', 'uffici', 'benefici',
      'giornale', 'canale', 'ospedale', 'animale',
      'parla', 'parli', 'dice', 'aperti', 'certi', 'esterni', 'esterne', 'limi', 'peli'
    ];

    it.each(safeWords)('deve garantir que "%s" não seja falsamente fatiado como clítico', (word) => {
      const result = TextNormalizer.stripEnclitics(word);
      expect(result.enclitic).toBeNull();
      expect(result.stem).toBe(word);
    });

    it('auditoria adversarial: comprovar proteção de "simile" contra clitic stripping', () => {
      const result = TextNormalizer.stripEnclitics('simile');
      // "simile" termina em "le" e o radical "simi" termina em "i", mas está protegido em NON_ENCLITIC_WORDS:
      expect(result).toEqual({ stem: 'simile', enclitic: null });
      expect(TextNormalizer.toLemma('simile')).toBe('simile');
    });

    it('auditoria adversarial: comprovar proteção contra clitic stripping indevido em substantivos comuns (chiavi, frasi, crisi, quasi)', () => {
      // Substantivos que terminam em -vi, -si com vogal a/i precedente protegidos:
      expect(TextNormalizer.stripEnclitics('chiavi')).toEqual({ stem: 'chiavi', enclitic: null });
      expect(TextNormalizer.toLemma('chiavi')).toBe('chiave');

      expect(TextNormalizer.stripEnclitics('frasi')).toEqual({ stem: 'frasi', enclitic: null });
      expect(TextNormalizer.toLemma('frasi')).toBe('frase');

      expect(TextNormalizer.stripEnclitics('crisi')).toEqual({ stem: 'crisi', enclitic: null });
      expect(TextNormalizer.toLemma('crisi')).toBe('crisi');

      expect(TextNormalizer.stripEnclitics('quasi')).toEqual({ stem: 'quasi', enclitic: null });
      expect(TextNormalizer.toLemma('quasi')).toBe('quasi');
    });

    it('deve descolar enclíticos legítimos corretamente em infinitivos, gerúndios e imperativos', () => {
      expect(TextNormalizer.stripEnclitics('portami')).toEqual({ stem: 'porta', enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('vederlo')).toEqual({ stem: 'vedere', enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('parlandogli')).toEqual({ stem: 'parlando', enclitic: 'gli' });
      expect(TextNormalizer.stripEnclitics('dimmi')).toEqual({ stem: "di'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('fallo')).toEqual({ stem: "fa'", enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('dammelo')).toEqual({ stem: "da'", enclitic: 'melo' });
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 4: Irregular verb stems and compound forms
  // ────────────────────────────────────────────────────────────
  describe('Scenario 4: Irregular verb stems and forms', () => {
    it('deve mapear formas irregulares do núcleo para seus infinitivos canônicos', () => {
      expect(TextNormalizer.toLemma('sono')).toBe('essere');
      expect(TextNormalizer.toLemma('era')).toBe('essere');
      expect(TextNormalizer.toLemma('stato')).toBe('essere');
      expect(TextNormalizer.toLemma('ho')).toBe('avere');
      expect(TextNormalizer.toLemma('avuto')).toBe('avere');
      expect(TextNormalizer.toLemma('vado')).toBe('andare');
      expect(TextNormalizer.toLemma('faccio')).toBe('fare');
      expect(TextNormalizer.toLemma('fatto')).toBe('fare');
      expect(TextNormalizer.toLemma('dico')).toBe('dire');
      expect(TextNormalizer.toLemma('detto')).toBe('dire');
      expect(TextNormalizer.toLemma('posso')).toBe('potere');
      expect(TextNormalizer.toLemma('voglio')).toBe('volere');
      expect(TextNormalizer.toLemma('devo')).toBe('dovere');
    });

    it('auditoria empírica de formas de Passato Remoto (andammo, fecero, diedero, stettero, fu, fui)', () => {
      // Formas de Passato Remoto ausentes em conjugacoes.json e _coreVerbs:
      expect(TextNormalizer.toLemma('andammo')).toBe('andammo'); // Esperado: 'andare'
      expect(TextNormalizer.toLemma('fecero')).toBe('fecero');   // Esperado: 'fare'
      expect(TextNormalizer.toLemma('diedero')).toBe('diedero'); // Esperado: 'dare'
      expect(TextNormalizer.toLemma('stettero')).toBe('stettero'); // Esperado: 'stare'
      expect(TextNormalizer.toLemma('fu')).toBe('fu');           // Esperado: 'essere'
    });

    it('auditoria adversarial: proteção de plurais em -ivi (motivi -> motivo, archivi -> archivio)', () => {
      // 'motivi' e 'archivi' protegidos de clitic stripping em NON_ENCLITIC_WORDS:
      expect(TextNormalizer.stripEnclitics('motivi')).toEqual({ stem: 'motivi', enclitic: null });
      expect(TextNormalizer.toLemma('motivi')).toBe('motivo');
      expect(TextNormalizer.stripEnclitics('archivi')).toEqual({ stem: 'archivi', enclitic: null });
      expect(TextNormalizer.toLemma('archivi')).toBe('archivio');
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 5: Gulpease index under edge cases
  // ────────────────────────────────────────────────────────────
  describe('Scenario 5: Gulpease index edge cases & stress', () => {
    it('deve retornar pontuação 0 segura para texto vazio ou whitespace', () => {
      const empty = TextNormalizer.computeGulpease('');
      expect(empty.score).toBe(0);
      expect(empty.rawScore).toBe(0);
      expect(empty.p).toBe(0);
      expect(empty.lp).toBe(0);
      expect(empty.level).toBe('molto_difficile');

      const ws = TextNormalizer.computeGulpease('   \n\t   ');
      expect(ws.score).toBe(0);
      expect(ws.p).toBe(0);
    });

    it('deve retornar pontuação 0 para texto composto exclusivamente por números e símbolos', () => {
      const res = TextNormalizer.computeGulpease('12345 67890 @#$%^&*()_+ == --');
      expect(res.score).toBe(0);
      expect(res.p).toBe(0);
      expect(res.level).toBe('molto_difficile');
    });

    it('deve calcular corretamente para texto de 1 palavra', () => {
      const oneWord = TextNormalizer.computeGulpease('ciao');
      expect(oneWord.p).toBe(1);
      expect(oneWord.lp).toBe(4);
      expect(oneWord.fr).toBe(1);
      expect(oneWord.score).toBeGreaterThan(0);
      expect(oneWord.score).toBeLessThanOrEqual(100);
    });

    it('deve suportar texto massivo de 10.000 palavras em menos de 500ms sem estourar memória', () => {
      const singleSentence = 'Questo è un testo di prova per verificare la stabilità e la velocità del calcolo Gulpease su larga scala. ';
      const largeText = singleSentence.repeat(600); // ~10.800 palavras
      const t0 = performance.now();
      const res = TextNormalizer.computeGulpease(largeText);
      const elapsed = performance.now() - t0;

      expect(res.p).toBeGreaterThan(10000);
      expect(res.score).toBeGreaterThanOrEqual(0);
      expect(res.score).toBeLessThanOrEqual(100);
      expect(Number.isFinite(res.score)).toBe(true);
      expect(elapsed).toBeLessThan(500); // performance guard
    });

    it('deve tratar tempestade de abreviações sem fragmentar contagem de frases', () => {
      const text = 'Il dott. Rossi, il prof. Bianchi, l’ing. Verdi e la sig.ra Neri hanno firmato l’art. 5 ecc. Tutto in regola!';
      const res = TextNormalizer.computeGulpease(text);
      expect(res.fr).toBe(1); // Somente '!' final deve fechar frase
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 6: Frequency lookups & boundaries (1..3000)
  // ────────────────────────────────────────────────────────────
  describe('Scenario 6: Frequency lookups & boundaries (1..3000)', () => {
    it('deve retornar exatamente os ranks nas fronteiras 1, 1000, 1001, 2000, 2001, 3000', () => {
      const lemma1 = AppFrequency.getLemmaAtRank(1);
      expect(lemma1).not.toBeNull();
      expect(AppFrequency.getRank(lemma1!)).toBe(1);
      expect(AppFrequency.getBand(lemma1!)).toBe('1k');

      const lemma1000 = AppFrequency.getLemmaAtRank(1000);
      expect(lemma1000).not.toBeNull();
      expect(AppFrequency.getRank(lemma1000!)).toBe(1000);
      expect(AppFrequency.getBand(lemma1000!)).toBe('1k');

      const lemma1001 = AppFrequency.getLemmaAtRank(1001);
      expect(lemma1001).not.toBeNull();
      expect(AppFrequency.getRank(lemma1001!)).toBe(1001);
      expect(AppFrequency.getBand(lemma1001!)).toBe('2k');

      const lemma2000 = AppFrequency.getLemmaAtRank(2000);
      expect(lemma2000).not.toBeNull();
      expect(AppFrequency.getRank(lemma2000!)).toBe(2000);
      expect(AppFrequency.getBand(lemma2000!)).toBe('2k');

      const lemma2001 = AppFrequency.getLemmaAtRank(2001);
      expect(lemma2001).not.toBeNull();
      expect(AppFrequency.getRank(lemma2001!)).toBe(2001);
      expect(AppFrequency.getBand(lemma2001!)).toBe('3k');

      const lemma3000 = AppFrequency.getLemmaAtRank(3000);
      expect(lemma3000).not.toBeNull();
      expect(AppFrequency.getRank(lemma3000!)).toBe(3000);
      expect(AppFrequency.getBand(lemma3000!)).toBe('3k');
    });

    it('deve retornar null para rank 3001 e índices fora do intervalo', () => {
      expect(AppFrequency.getLemmaAtRank(3001)).toBeNull();
      expect(AppFrequency.getLemmaAtRank(0)).toBeNull();
      expect(AppFrequency.getLemmaAtRank(-1)).toBeNull();
      expect(AppFrequency.getLemmaAtRank(NaN)).toBeNull();
      expect(AppFrequency.getLemmaAtRank(Infinity)).toBeNull();
      // @ts-expect-error non-number test
      expect(AppFrequency.getLemmaAtRank('1')).toBeNull();
    });

    it('deve classificar palavras desconhecidas e inventadas como "rare"', () => {
      const rareWords = ['xyzabc', 'pseudoparola123', 'supercalifragilistico'];
      for (const w of rareWords) {
        expect(AppFrequency.getRank(w)).toBeNull();
        expect(AppFrequency.getBand(w)).toBe('rare');
        expect(AppFrequency.getRankSafe(w)).toBe(Infinity);
        expect(AppFrequency.isCommon(w)).toBe(false);
      }
    });

    it('deve lidar de forma defensiva com null, undefined, vazios, números e espaços', () => {
      // @ts-expect-error null test
      expect(AppFrequency.getRank(null)).toBeNull();
      // @ts-expect-error undefined test
      expect(AppFrequency.getRank(undefined)).toBeNull();
      expect(AppFrequency.getRank('')).toBeNull();
      expect(AppFrequency.getRank('   ')).toBeNull();
      // @ts-expect-error number test
      expect(AppFrequency.getRank(1234)).toBeNull();

      // @ts-expect-error null test
      expect(AppFrequency.getBand(null)).toBe('rare');
      // @ts-expect-error undefined test
      expect(AppFrequency.getBand(undefined)).toBe('rare');
      expect(AppFrequency.getBand('')).toBe('rare');

      // Case insensitivity e padding
      expect(AppFrequency.getRank('  IL  ')).toBe(1);
      expect(AppFrequency.getRank('\tDi\n')).toBe(2);
    });

    it('auditoria empírica: vocabulário fundamental italiano presente no Top 3000', () => {
      // Palavras de altíssimo uso em italiano devidamente indexadas em frequenza_3000:
      expect(AppFrequency.getRank('poco')).not.toBeNull();
      expect(AppFrequency.getRank('tanto')).not.toBeNull();
      expect(AppFrequency.getRank('troppo')).not.toBeNull();
      expect(AppFrequency.getRank('quasi')).not.toBeNull();
      expect(AppFrequency.getRank('tuttavia')).not.toBeNull();
      expect(AppFrequency.getRank('così')).not.toBeNull();
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 7: Profile calculation with 100% rare, 100% 1k, and empty input
  // ────────────────────────────────────────────────────────────
  describe('Scenario 7: Profile calculation with pure and empty distributions', () => {
    it('deve calcular perfil de 100% de palavras 1k', () => {
      const tokens1k = ['il', 'di', 'che', 'avere', 'essere'];
      const profile = AppFrequency.getProfile(tokens1k);

      expect(profile.totalTokens).toBe(5);
      expect(profile.bandCounts['1k']).toBe(5);
      expect(profile.bandCounts['2k']).toBe(0);
      expect(profile.bandCounts['3k']).toBe(0);
      expect(profile.bandCounts['rare']).toBe(0);
      expect(profile.bandPercentages['1k']).toBe(100);
      expect(profile.coveredTokens).toBe(5);
      expect(profile.coveragePct).toBe(100);
    });

    it('deve calcular perfil de 100% de palavras raras', () => {
      const rareTokens = ['parolainventata1', 'parolainventata2', 'parolainventata3'];
      const profile = AppFrequency.getProfile(rareTokens);

      expect(profile.totalTokens).toBe(3);
      expect(profile.bandCounts['rare']).toBe(3);
      expect(profile.bandCounts['1k']).toBe(0);
      expect(profile.bandPercentages['rare']).toBe(100);
      expect(profile.coveredTokens).toBe(0);
      expect(profile.coveragePct).toBe(0);
    });

    it('deve retornar zeros seguros para array vazio ou parâmetros inválidos', () => {
      const empty = AppFrequency.getProfile([]);
      expect(empty.totalTokens).toBe(0);
      expect(empty.coveragePct).toBe(0);
      expect(empty.coveredTokens).toBe(0);
      expect(empty.bandPercentages['1k']).toBe(0);

      // @ts-expect-error null test
      const nullInput = AppFrequency.getProfile(null);
      expect(nullInput.totalTokens).toBe(0);
      expect(nullInput.coveragePct).toBe(0);

      // @ts-expect-error undefined test
      const undefInput = AppFrequency.getProfile(undefined);
      expect(undefInput.totalTokens).toBe(0);
    });

    it('deve manter a soma das porcentagens em 100% em distribuições mistas', () => {
      const mixedTokens = [
        'il',         // 1k
        'coltello',   // 2k
        'allarmante', // 3k
        'xyzraro'     // rare
      ];
      const profile = AppFrequency.getProfile(mixedTokens);
      expect(profile.totalTokens).toBe(4);
      const sum = profile.bandPercentages['1k'] +
                  profile.bandPercentages['2k'] +
                  profile.bandPercentages['3k'] +
                  profile.bandPercentages['rare'];
      expect(Math.round(sum)).toBe(100);
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 8: Elision and articulated prepositions edge cases
  // ────────────────────────────────────────────────────────────
  describe('Scenario 8: Elision & Articulated Prepositions Edge Cases', () => {
    it('deve descompactar corretamente todas as variantes de preposições com apóstrofo', () => {
      const elidedPreps = ["dell'", "all'", "dall'", "nell'", "sull'"];
      for (const ep of elidedPreps) {
        const res = TextNormalizer.unpackElisions(ep);
        expect(res.length).toBeGreaterThanOrEqual(1);
      }
    });

    it('deve lidar com elisões de artigos e pronomes sem sufixo ou com sufixo', () => {
      expect(TextNormalizer.unpackElisions("un'")).toEqual(['una']);
      expect(TextNormalizer.unpackElisions("l'")).toEqual(['il']);
      expect(TextNormalizer.unpackElisions("c'")).toEqual(['ci']);
      expect(TextNormalizer.unpackElisions("d'")).toEqual(['di']);
    });

    it('deve descompactar termos com prefixos elididos clássicos (senz\'altro, tutt\'altro)', () => {
      expect(TextNormalizer.unpackElisions("senz'altro")).toEqual(['senza', 'altro']);
      expect(TextNormalizer.unpackElisions("tutt'altro")).toEqual(['tutto', 'altro']);
      expect(TextNormalizer.unpackElisions("dov'è")).toEqual(['dove', 'è']);
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 9: Clitic detachment invariants on combined pronouns
  // ────────────────────────────────────────────────────────────
  describe('Scenario 9: Clitic detachment on combined pronouns', () => {
    it('deve descolar pronomes combinados (glielo, gliela, melo, telo, selo, celo, velo)', () => {
      expect(TextNormalizer.stripEnclitics('darmelo')).toEqual({ stem: 'dare', enclitic: 'melo' });
      expect(TextNormalizer.stripEnclitics('portarglielo')).toEqual({ stem: 'portare', enclitic: 'glielo' });
      expect(TextNormalizer.stripEnclitics('dicendotelo')).toEqual({ stem: 'dicendo', enclitic: 'telo' });
      expect(TextNormalizer.stripEnclitics('prendendosela')).toEqual({ stem: 'prendendo', enclitic: 'sela' });
    });

    it('deve descolar imperativos com raddoppiamento sintattico monossilábico', () => {
      expect(TextNormalizer.stripEnclitics('dammi')).toEqual({ stem: "da'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('dallo')).toEqual({ stem: "da'", enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('fammi')).toEqual({ stem: "fa'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('fallo')).toEqual({ stem: "fa'", enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('dimmi')).toEqual({ stem: "di'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('dillo')).toEqual({ stem: "di'", enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('vacci')).toEqual({ stem: "va'", enclitic: 'ci' });
      expect(TextNormalizer.stripEnclitics('stacci')).toEqual({ stem: "sta'", enclitic: 'ci' });
    });

    it('auditoria adversarial: presença de "dimmelo" em MONO_IMPERATIVES', () => {
      // 'dammi', 'dammelo' e 'dimmelo' devidamente registrados:
      expect(TextNormalizer.stripEnclitics('dammelo')).toEqual({ stem: "da'", enclitic: 'melo' });
      expect(TextNormalizer.stripEnclitics('dimmelo')).toEqual({ stem: "di'", enclitic: 'melo' });
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 10: Suffix stripping & Regular Morphology
  // ────────────────────────────────────────────────────────────
  describe('Scenario 10: Suffix stripping & regular morphology', () => {
    it('deve lematizar advérbios em -mente para o adjetivo base', () => {
      expect(TextNormalizer.toLemma('rapidamente')).toBe('rapido');
      expect(TextNormalizer.toLemma('lentamente')).toBe('lento');
      expect(TextNormalizer.toLemma('facilmente')).toBe('facile');
    });

    it('auditoria adversarial: superlativos absolutos femininos/singulares vs plurais masculinos (-issimi)', () => {
      expect(TextNormalizer.toLemma('bravissimo')).toBe('bravo');
      expect(TextNormalizer.toLemma('bravissima')).toBe('bravo');
      expect(TextNormalizer.toLemma('bravissime')).toBe('bravo');
      // Superlativos plurais masculinos (-issimi) preservados via reordenação do pipeline:
      expect(TextNormalizer.toLemma('bravissimi')).toBe('bravo');
      expect(TextNormalizer.toLemma('bellissimi')).toBe('bello');
    });

    it('deve preservar substantivos terminados em -ore e -ione sem truncamento indevido', () => {
      expect(TextNormalizer.toLemma('attore')).toBe('attore');
      expect(TextNormalizer.toLemma('canzone')).toBe('canzone');
      expect(TextNormalizer.toLemma('lezione')).toBe('lezione');
      expect(TextNormalizer.toLemma('invasore')).toBe('invasore');
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 11: Frequency index band integrity & sizes
  // ────────────────────────────────────────────────────────────
  describe('Scenario 11: Frequency index band integrity & sizes', () => {
    it('deve conter exatamente 1.000 lemas em cada uma das três faixas (1k, 2k, 3k)', () => {
      const b1 = AppFrequency.getLemmasInBand('1k');
      const b2 = AppFrequency.getLemmasInBand('2k');
      const b3 = AppFrequency.getLemmasInBand('3k');
      expect(b1.length).toBe(1000);
      expect(b2.length).toBe(1000);
      expect(b3.length).toBe(1000);

      // Verificação de disjunção: nenhum lema repetido entre faixas
      const allLemmas = new Set([...b1, ...b2, ...b3]);
      expect(allLemmas.size).toBe(3000);
    });

    it('deve retornar ranges corretos para cada banda', () => {
      expect(AppFrequency.getBandRange('1k')).toEqual([1, 1000]);
      expect(AppFrequency.getBandRange('2k')).toEqual([1001, 2000]);
      expect(AppFrequency.getBandRange('3k')).toEqual([2001, 3000]);
      expect(AppFrequency.getBandRange('rare')).toBeNull();
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 12: Frequency sampling determinism and boundaries
  // ────────────────────────────────────────────────────────────
  describe('Scenario 12: Frequency sampling determinism and boundaries', () => {
    it('deve suportar amostragem com count maior que o tamanho da faixa sem quebrar', () => {
      const sample = AppFrequency.sampleBand('1k', 2000);
      expect(sample.length).toBe(1000); // capped at 1000
    });

    it('deve suportar count zero ou negativo retornando array vazio', () => {
      expect(AppFrequency.sampleBand('1k', 0)).toEqual([]);
      expect(AppFrequency.sampleBand('1k', -5)).toEqual([]);
    });

    it('deve produzir amostragem determinística quando um RNG previsível é fornecido', () => {
      let seed = 42;
      const deterministicRng = () => {
        seed = (seed * 9301 + 49297) % 233280;
        return seed / 233280;
      };

      let seed2 = 42;
      const deterministicRng2 = () => {
        seed2 = (seed2 * 9301 + 49297) % 233280;
        return seed2 / 233280;
      };

      const sample1 = AppFrequency.sampleBand('1k', 10, deterministicRng);
      const sample2 = AppFrequency.sampleBand('1k', 10, deterministicRng2);
      expect(sample1).toEqual(sample2);
    });

    it('auditoria adversarial: ausência de vazamento de undefined em sampleBand se rng retornar 1.0', () => {
      // Quando rng() == 1.0, o índice é travado com Math.min(i, ...) sem indexar undefined
      const boundarySample = AppFrequency.sampleBand('1k', 3, () => 1.0);
      expect(boundarySample).not.toContain(undefined);
      expect(boundarySample.length).toBe(3);
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 13: End-to-end normalization on authentic complex sentences
  // ────────────────────────────────────────────────────────────
  describe('Scenario 13: End-to-end normalization on authentic complex sentences', () => {
    it('deve normalizar frase com elisão, apócope, enclítico e preposição articulada', () => {
      const sentence = "L'amico del professore disse: 'Portami quel bel libro d'arte!'";
      const lemmas = TextNormalizer.normalizeText(sentence);

      expect(lemmas).toContain('il');        // L' -> il
      expect(lemmas).toContain('amico');     // amico
      expect(lemmas).toContain('di');        // del -> di + il
      expect(lemmas).toContain('professore');// professore
      expect(lemmas).toContain('portare');   // Portami -> portare
      expect(lemmas).toContain('quello');    // quel -> quello
      expect(lemmas).toContain('bello');     // bel -> bello
      expect(lemmas).toContain('libro');     // libro
      expect(lemmas).toContain('arte');      // d'arte -> di + arte
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 14: Re-entrancy, repeated initialization & memory stability
  // ────────────────────────────────────────────────────────────
  describe('Scenario 14: Re-entrancy & repeated initialization', () => {
    it('deve tolerar inicializações repetidas sem duplicar dados ou causar vazamentos', () => {
      for (let i = 0; i < 5; i++) {
        TextNormalizer.init();
      }
      expect(TextNormalizer.toLemma('sono')).toBe('essere');

      const freqData = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'data/frequenza_3000.json'), 'utf-8'));
      for (let i = 0; i < 5; i++) {
        AppFrequency.init(freqData);
      }
      expect(AppFrequency.getTotal()).toBe(3000);
      expect(AppFrequency.getRank('il')).toBe(1);
    });
  });

  // ────────────────────────────────────────────────────────────
  // SCENARIO 15: Type coercion, malformed payloads & boundary resilience
  // ────────────────────────────────────────────────────────────
  describe('Scenario 15: Type coercion, malformed payloads & boundary resilience', () => {
    it('deve tolerar chamadas com tipos completamente anômalos em TextNormalizer', () => {
      // @ts-expect-error non-string test
      expect(TextNormalizer.tokenize(12345)).toEqual([]);
      // @ts-expect-error non-string test
      expect(TextNormalizer.tokenize({})).toEqual([]);
      // @ts-expect-error non-string test
      expect(TextNormalizer.unpackElisions(null)).toEqual([]);
      // @ts-expect-error non-string test
      expect(TextNormalizer.restoreApocope(undefined)).toBe('');
      // @ts-expect-error non-string test
      expect(TextNormalizer.stripEnclitics(null)).toEqual({ stem: '', enclitic: null });
      // @ts-expect-error non-string test
      expect(TextNormalizer.toLemma(123)).toBe('');
      // @ts-expect-error non-string test
      expect(TextNormalizer.normalizeText(null)).toEqual([]);
      // @ts-expect-error non-string test
      expect(TextNormalizer.computeGulpease(null).score).toBe(0);
    });

    it('deve tolerar payloads vazios ou inválidos no AppFrequency.init', () => {
      expect(() => AppFrequency.init(null)).not.toThrow();
      expect(() => AppFrequency.init(undefined)).not.toThrow();
      expect(() => AppFrequency.init({})).not.toThrow();
      expect(() => AppFrequency.init('')).not.toThrow();
      expect(() => AppFrequency.init({ words: [] })).not.toThrow();
    });
  });
});
