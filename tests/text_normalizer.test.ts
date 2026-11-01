// ============================================================
// tests/text_normalizer.test.ts — Italian Text Normalizer Engine Unit Tests
// Milestone 1 (F3)
// ============================================================

import { describe, it, expect, beforeEach } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import TextNormalizer from '../js/core/text_normalizer.js';

describe('F3: Italian Text Normalizer Engine (js/core/text_normalizer.js)', () => {
  beforeEach(() => {
    TextNormalizer.init();

    // Carrega dados se disponíveis no ambiente de teste
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
  });

  // ────────────────────────────────────────────────────────────
  // 1. TOKENIZATION
  // ────────────────────────────────────────────────────────────
  describe('Domain 1: Tokenization', () => {
    it('deve extrair palavras simples preservando acentos italianos', () => {
      const text = 'La città di Roma è meravigliosa e l’università è antica.';
      const tokens = TextNormalizer.tokenize(text);
      expect(tokens).toContain('città');
      expect(tokens).toContain('Roma');
      expect(tokens).toContain('è');
      expect(tokens).toContain('meravigliosa');
      expect(tokens).toContain('antica');
    });

    it('deve preservar elisões internas com apóstrofo como tokens íntegros', () => {
      const text = "C'era una volta un re che beveva dell'acqua.";
      const tokens = TextNormalizer.tokenize(text);
      expect(tokens).toContain("C'era");
      expect(tokens).toContain("dell'acqua");
    });

    it('deve remover aspas simples, duplas e guillemets das bordas das palavras', () => {
      const text = "«Bella ciao!» gridò: 'Portami via!'";
      const tokens = TextNormalizer.tokenize(text);
      expect(tokens).toEqual(['Bella', 'ciao', 'gridò', 'Portami', 'via']);
    });

    it('deve preservar apóstrofes apocópicas lexicais no final (po\', fa\', da\', di\', va\', sta\')', () => {
      const text = "Dammi un po' di pane, fa' presto e di' la verità!";
      const tokens = TextNormalizer.tokenize(text);
      expect(tokens).toContain("po'");
      expect(tokens).toContain("fa'");
      expect(tokens).toContain("di'");
    });

    it('deve retornar array vazio para texto vazio, nulo ou composto apenas por pontuação', () => {
      expect(TextNormalizer.tokenize('')).toEqual([]);
      expect(TextNormalizer.tokenize('   ')).toEqual([]);
      expect(TextNormalizer.tokenize(null as unknown as string)).toEqual([]);
      expect(TextNormalizer.tokenize('... --- ??? !!!')).toEqual([]);
    });

    it('deve respeitar a opção lowercase: true quando solicitada', () => {
      const tokens = TextNormalizer.tokenize('Il Grande Colosseo', { lowercase: true });
      expect(tokens).toEqual(['il', 'grande', 'colosseo']);
    });
  });

  // ────────────────────────────────────────────────────────────
  // 2. ELISION UNPACKING
  // ────────────────────────────────────────────────────────────
  describe('Domain 2: Elision Unpacking & Articulated Prepositions', () => {
    it('deve descompactar as 32 preposições articuladas canônicas não-elididas', () => {
      // di
      expect(TextNormalizer.unpackElisions('del')).toEqual(['di', 'il']);
      expect(TextNormalizer.unpackElisions('dello')).toEqual(['di', 'lo']);
      expect(TextNormalizer.unpackElisions('della')).toEqual(['di', 'la']);
      expect(TextNormalizer.unpackElisions('dei')).toEqual(['di', 'i']);
      expect(TextNormalizer.unpackElisions('degli')).toEqual(['di', 'gli']);
      expect(TextNormalizer.unpackElisions('delle')).toEqual(['di', 'le']);

      // a
      expect(TextNormalizer.unpackElisions('al')).toEqual(['a', 'il']);
      expect(TextNormalizer.unpackElisions('allo')).toEqual(['a', 'lo']);
      expect(TextNormalizer.unpackElisions('alla')).toEqual(['a', 'la']);
      expect(TextNormalizer.unpackElisions('ai')).toEqual(['a', 'i']);
      expect(TextNormalizer.unpackElisions('agli')).toEqual(['a', 'gli']);
      expect(TextNormalizer.unpackElisions('alle')).toEqual(['a', 'le']);

      // da
      expect(TextNormalizer.unpackElisions('dal')).toEqual(['da', 'il']);
      expect(TextNormalizer.unpackElisions('dallo')).toEqual(['da', 'lo']);
      expect(TextNormalizer.unpackElisions('dalla')).toEqual(['da', 'la']);
      expect(TextNormalizer.unpackElisions('dai')).toEqual(['da', 'i']);
      expect(TextNormalizer.unpackElisions('dagli')).toEqual(['da', 'gli']);
      expect(TextNormalizer.unpackElisions('dalle')).toEqual(['da', 'le']);

      // in
      expect(TextNormalizer.unpackElisions('nel')).toEqual(['in', 'il']);
      expect(TextNormalizer.unpackElisions('nello')).toEqual(['in', 'lo']);
      expect(TextNormalizer.unpackElisions('nella')).toEqual(['in', 'la']);
      expect(TextNormalizer.unpackElisions('nei')).toEqual(['in', 'i']);
      expect(TextNormalizer.unpackElisions('negli')).toEqual(['in', 'gli']);
      expect(TextNormalizer.unpackElisions('nelle')).toEqual(['in', 'le']);

      // su
      expect(TextNormalizer.unpackElisions('sul')).toEqual(['su', 'il']);
      expect(TextNormalizer.unpackElisions('sullo')).toEqual(['su', 'lo']);
      expect(TextNormalizer.unpackElisions('sulla')).toEqual(['su', 'la']);
      expect(TextNormalizer.unpackElisions('sui')).toEqual(['su', 'i']);
      expect(TextNormalizer.unpackElisions('sugli')).toEqual(['su', 'gli']);
      expect(TextNormalizer.unpackElisions('sulle')).toEqual(['su', 'le']);

      // con
      expect(TextNormalizer.unpackElisions('col')).toEqual(['con', 'il']);
      expect(TextNormalizer.unpackElisions('coi')).toEqual(['con', 'i']);
    });

    it('deve descompactar preposições articuladas elididas com substantivo', () => {
      expect(TextNormalizer.unpackElisions("dell'acqua")).toEqual(['di', 'il', 'acqua']);
      expect(TextNormalizer.unpackElisions("all'estero")).toEqual(['a', 'il', 'estero']);
      expect(TextNormalizer.unpackElisions("nell'ombra")).toEqual(['in', 'il', 'ombra']);
      expect(TextNormalizer.unpackElisions("sull'albero")).toEqual(['su', 'il', 'albero']);
      expect(TextNormalizer.unpackElisions("dall'inizio")).toEqual(['da', 'il', 'inizio']);
    });

    it('deve descompactar artigos e pronomes elididos', () => {
      expect(TextNormalizer.unpackElisions("l'amico")).toEqual(['il', 'amico']);
      expect(TextNormalizer.unpackElisions("l'invasor")).toEqual(['il', 'invasor']);
      expect(TextNormalizer.unpackElisions("un'ora")).toEqual(['una', 'ora']);
      expect(TextNormalizer.unpackElisions("c'era")).toEqual(['ci', 'era']);
      expect(TextNormalizer.unpackElisions("c'è")).toEqual(['ci', 'è']);
      expect(TextNormalizer.unpackElisions("d'oro")).toEqual(['di', 'oro']);
      expect(TextNormalizer.unpackElisions("d'accordo")).toEqual(['di', 'accordo']);
      expect(TextNormalizer.unpackElisions("m'ama")).toEqual(['mi', 'ama']);
      expect(TextNormalizer.unpackElisions("t'amo")).toEqual(['ti', 'amo']);
      expect(TextNormalizer.unpackElisions("s'allontana")).toEqual(['si', 'allontana']);
      expect(TextNormalizer.unpackElisions("v'era")).toEqual(['vi', 'era']);
      expect(TextNormalizer.unpackElisions("n'ha")).toEqual(['ne', 'ha']);
      expect(TextNormalizer.unpackElisions("dov'è")).toEqual(['dove', 'è']);
      expect(TextNormalizer.unpackElisions("com'è")).toEqual(['come', 'è']);
      expect(TextNormalizer.unpackElisions("qual'è")).toEqual(['quale', 'è']);
      expect(TextNormalizer.unpackElisions("tutt'altro")).toEqual(['tutto', 'altro']);
      expect(TextNormalizer.unpackElisions("senz'altro")).toEqual(['senza', 'altro']);
    });

    it('deve retornar a própria palavra em array se não houver elisão', () => {
      expect(TextNormalizer.unpackElisions('amico')).toEqual(['amico']);
      expect(TextNormalizer.unpackElisions('casa')).toEqual(['casa']);
    });
  });

  // ────────────────────────────────────────────────────────────
  // 3. APOCOPE RESTORATION
  // ────────────────────────────────────────────────────────────
  describe('Domain 3: Apocope Restoration', () => {
    it('deve restaurar infinitivos poéticos truncados terminados em -r', () => {
      expect(TextNormalizer.restoreApocope('morir')).toBe('morire');
      expect(TextNormalizer.restoreApocope('andar')).toBe('andare');
      expect(TextNormalizer.restoreApocope('far')).toBe('fare');
      expect(TextNormalizer.restoreApocope('veder')).toBe('vedere');
      expect(TextNormalizer.restoreApocope('parlar')).toBe('parlare');
      expect(TextNormalizer.restoreApocope('aver')).toBe('avere');
      expect(TextNormalizer.restoreApocope('esser')).toBe('essere');
      expect(TextNormalizer.restoreApocope('saper')).toBe('sapere');
      expect(TextNormalizer.restoreApocope('voler')).toBe('volere');
      expect(TextNormalizer.restoreApocope('poter')).toBe('potere');
      expect(TextNormalizer.restoreApocope('venir')).toBe('venire');
      expect(TextNormalizer.restoreApocope('sentir')).toBe('sentire');
    });

    it('deve restaurar substantivos e adjetivos poéticos em -or', () => {
      expect(TextNormalizer.restoreApocope('invasor')).toBe('invasore');
      expect(TextNormalizer.restoreApocope('amor')).toBe('amore');
      expect(TextNormalizer.restoreApocope('dolor')).toBe('dolore');
      expect(TextNormalizer.restoreApocope('color')).toBe('colore');
      expect(TextNormalizer.restoreApocope('fior')).toBe('fiore');
      expect(TextNormalizer.restoreApocope('cuor')).toBe('cuore');
      expect(TextNormalizer.restoreApocope('signor')).toBe('signore');
      expect(TextNormalizer.restoreApocope('dottor')).toBe('dottore');
      expect(TextNormalizer.restoreApocope('professor')).toBe('professore');
    });

    it('deve restaurar adjetivos e advérbios truncados canônicos', () => {
      expect(TextNormalizer.restoreApocope('bel')).toBe('bello');
      expect(TextNormalizer.restoreApocope('gran')).toBe('grande');
      expect(TextNormalizer.restoreApocope('san')).toBe('santo');
      expect(TextNormalizer.restoreApocope('buon')).toBe('buono');
      expect(TextNormalizer.restoreApocope('ben')).toBe('bene');
      expect(TextNormalizer.restoreApocope('mal')).toBe('male');
      expect(TextNormalizer.restoreApocope('man')).toBe('mano');
      expect(TextNormalizer.restoreApocope('qual')).toBe('quale');
      expect(TextNormalizer.restoreApocope('tal')).toBe('tale');
      expect(TextNormalizer.restoreApocope('quel')).toBe('quello');
      expect(TextNormalizer.restoreApocope('nessun')).toBe('nessuno');
      expect(TextNormalizer.restoreApocope('alcun')).toBe('alcuno');
    });

    it('deve restaurar verbos poéticos monossilábicos truncados (son, fan, dan, van, han)', () => {
      expect(TextNormalizer.restoreApocope('son')).toBe('sono');
      expect(TextNormalizer.restoreApocope('fan')).toBe('fanno');
      expect(TextNormalizer.restoreApocope('dan')).toBe('danno');
      expect(TextNormalizer.restoreApocope('van')).toBe('vanno');
      expect(TextNormalizer.restoreApocope('han')).toBe('hanno');
    });

    it('deve restaurar apócopes marcadas por apóstrofe (po\', fa\', da\', di\', va\', sta\')', () => {
      expect(TextNormalizer.restoreApocope("po'")).toBe('poco');
      expect(TextNormalizer.restoreApocope("fa'")).toBe('fare');
      expect(TextNormalizer.restoreApocope("da'")).toBe('dare');
      expect(TextNormalizer.restoreApocope("di'")).toBe('dire');
      expect(TextNormalizer.restoreApocope("sta'")).toBe('stare');
      expect(TextNormalizer.restoreApocope("va'")).toBe('andare');
      expect(TextNormalizer.restoreApocope("be'")).toBe('bene');
    });

    it('NÃO deve modificar palavras protegidas, preposições ou empréstimos estrangeiros', () => {
      expect(TextNormalizer.restoreApocope('per')).toBe('per');
      expect(TextNormalizer.restoreApocope('bar')).toBe('bar');
      expect(TextNormalizer.restoreApocope('computer')).toBe('computer');
      expect(TextNormalizer.restoreApocope('leader')).toBe('leader');
      expect(TextNormalizer.restoreApocope('sponsor')).toBe('sponsor');
      expect(TextNormalizer.restoreApocope('humor')).toBe('humor');
    });
  });

  // ────────────────────────────────────────────────────────────
  // 4. ENCLITIC PRONOUN DETACHMENT
  // ────────────────────────────────────────────────────────────
  describe('Domain 4: Enclitic Pronoun Detachment', () => {
    it('deve descolar pronomes enclíticos acoplados a infinitivos e restaurar o infinitivo', () => {
      expect(TextNormalizer.stripEnclitics('vederlo')).toEqual({ stem: 'vedere', enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('parlarle')).toEqual({ stem: 'parlare', enclitic: 'le' });
      expect(TextNormalizer.stripEnclitics('dirti')).toEqual({ stem: 'dire', enclitic: 'ti' });
      expect(TextNormalizer.stripEnclitics('farlo')).toEqual({ stem: 'fare', enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('sentirmi')).toEqual({ stem: 'sentire', enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('andarsene')).toEqual({ stem: 'andare', enclitic: 'sene' });
      expect(TextNormalizer.stripEnclitics('svegliarsi')).toEqual({ stem: 'svegliare', enclitic: 'si' });
    });

    it('deve descolar pronomes enclíticos acoplados a gerúndios', () => {
      expect(TextNormalizer.stripEnclitics('parlandogli')).toEqual({ stem: 'parlando', enclitic: 'gli' });
      expect(TextNormalizer.stripEnclitics('facendolo')).toEqual({ stem: 'facendo', enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('guardandoti')).toEqual({ stem: 'guardando', enclitic: 'ti' });
      expect(TextNormalizer.stripEnclitics('rivolgendosi')).toEqual({ stem: 'rivolgendo', enclitic: 'si' });
    });

    it('deve descolar pronomes em imperativos regulares', () => {
      expect(TextNormalizer.stripEnclitics('portami')).toEqual({ stem: 'porta', enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('ascoltami')).toEqual({ stem: 'ascolta', enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('guardalo')).toEqual({ stem: 'guarda', enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('prendilo')).toEqual({ stem: 'prendi', enclitic: 'lo' });
    });

    it('deve descolar pronomes em imperativos monossilábicos com raddoppiamento sintattico', () => {
      expect(TextNormalizer.stripEnclitics('dimmi')).toEqual({ stem: "di'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('dammi')).toEqual({ stem: "da'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('fammi')).toEqual({ stem: "fa'", enclitic: 'mi' });
      expect(TextNormalizer.stripEnclitics('dillo')).toEqual({ stem: "di'", enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('fallo')).toEqual({ stem: "fa'", enclitic: 'lo' });
      expect(TextNormalizer.stripEnclitics('dammelo')).toEqual({ stem: "da'", enclitic: 'melo' });
      expect(TextNormalizer.stripEnclitics('fammelo')).toEqual({ stem: "fa'", enclitic: 'melo' });
      expect(TextNormalizer.stripEnclitics('vacci')).toEqual({ stem: "va'", enclitic: 'ci' });
      expect(TextNormalizer.stripEnclitics('stacci')).toEqual({ stem: "sta'", enclitic: 'ci' });
    });

    it('NÃO deve descolar terminações em palavras que não são verbos com clíticos (guarda de falsos positivos)', () => {
      expect(TextNormalizer.stripEnclitics('carne')).toEqual({ stem: 'carne', enclitic: null });
      expect(TextNormalizer.stripEnclitics('pane')).toEqual({ stem: 'pane', enclitic: null });
      expect(TextNormalizer.stripEnclitics('cane')).toEqual({ stem: 'cane', enclitic: null });
      expect(TextNormalizer.stripEnclitics('fine')).toEqual({ stem: 'fine', enclitic: null });
      expect(TextNormalizer.stripEnclitics('sole')).toEqual({ stem: 'sole', enclitic: null });
      expect(TextNormalizer.stripEnclitics('vitale')).toEqual({ stem: 'vitale', enclitic: null });
      expect(TextNormalizer.stripEnclitics('iniziale')).toEqual({ stem: 'iniziale', enclitic: null });
      expect(TextNormalizer.stripEnclitics('facile')).toEqual({ stem: 'facile', enclitic: null });
      expect(TextNormalizer.stripEnclitics('edifici')).toEqual({ stem: 'edifici', enclitic: null });
      expect(TextNormalizer.stripEnclitics('amici')).toEqual({ stem: 'amici', enclitic: null });
      expect(TextNormalizer.stripEnclitics('parla')).toEqual({ stem: 'parla', enclitic: null });
      expect(TextNormalizer.stripEnclitics('parli')).toEqual({ stem: 'parli', enclitic: null });
    });
  });

  // ────────────────────────────────────────────────────────────
  // 5. LEMMATIZATION MAPPING
  // ────────────────────────────────────────────────────────────
  describe('Domain 5: Lemmatization Mapping', () => {
    it('deve mapear formas flexionadas dos verbos essenciais para seus infinitivos canônicos', () => {
      expect(TextNormalizer.toLemma('sono')).toBe('essere');
      expect(TextNormalizer.toLemma('sei')).toBe('essere');
      expect(TextNormalizer.toLemma('era')).toBe('essere');
      expect(TextNormalizer.toLemma('stato')).toBe('essere');

      expect(TextNormalizer.toLemma('ho')).toBe('avere');
      expect(TextNormalizer.toLemma('avevo')).toBe('avere');
      expect(TextNormalizer.toLemma('avuto')).toBe('avere');

      expect(TextNormalizer.toLemma('vado')).toBe('andare');
      expect(TextNormalizer.toLemma('va')).toBe('andare');
      expect(TextNormalizer.toLemma('andavano')).toBe('andare');
      expect(TextNormalizer.toLemma('andato')).toBe('andare');

      expect(TextNormalizer.toLemma('faccio')).toBe('fare');
      expect(TextNormalizer.toLemma('fatto')).toBe('fare');

      expect(TextNormalizer.toLemma('dico')).toBe('dire');
      expect(TextNormalizer.toLemma('detto')).toBe('dire');
    });

    it('deve mapear plurais nominais e adjetivais dos templos para o singular canônico', () => {
      expect(TextNormalizer.toLemma('rossi')).toBe('rosso');
      expect(TextNormalizer.toLemma('sorelle')).toBe('sorella');
      expect(TextNormalizer.toLemma('uomini')).toBe('uomo');
      expect(TextNormalizer.toLemma('mogli')).toBe('moglie');
      expect(TextNormalizer.toLemma('medici')).toBe('medico');
    });

    it('deve normalizar advérbios em -mente para o adjetivo base', () => {
      expect(TextNormalizer.toLemma('lentamente')).toBe('lento');
      expect(TextNormalizer.toLemma('facilmente')).toBe('facile');
    });

    it('deve normalizar superlativos em -issimo para o adjetivo base', () => {
      expect(TextNormalizer.toLemma('bravissimo')).toBe('bravo');
      expect(TextNormalizer.toLemma('bellissima')).toBe('bello');
    });

    it('deve aplicar regras morfológicas regulares de fallback para palavras não registradas', () => {
      expect(TextNormalizer.toLemma('tavoli')).toBe('tavolo');
      expect(TextNormalizer.toLemma('ragazze')).toBe('ragazza');
    });

    it('deve lematizar verbos com pronomes enclíticos diretamente para o infinitivo', () => {
      expect(TextNormalizer.toLemma('portami')).toBe('portare');
      expect(TextNormalizer.toLemma('vederlo')).toBe('vedere');
      expect(TextNormalizer.toLemma('dimmi')).toBe('dire');
    });
  });

  // ────────────────────────────────────────────────────────────
  // 6. GULPEASE READABILITY CALCULATION
  // ────────────────────────────────────────────────────────────
  describe('Domain 6: Gulpease Readability Calculation', () => {
    it('deve calcular corretamente a fórmula oficial Gulpease: 89 - (10*LP/P) + (300*FR/P)', () => {
      const text = 'Il gatto dorme bene. Il cane corre veloce.';
      const res = TextNormalizer.computeGulpease(text);
      expect(res.lp).toBe(33);
      expect(res.p).toBe(8);
      expect(res.fr).toBe(2);
      expect(res.score).toBeGreaterThan(80);
      expect(res.level).toBe('molto_facile');
    });

    it('deve classificar texto clássico narrativo (ex: Pinocchio/Cappuccetto) com índice acessível', () => {
      const text = "C'era una volta una bambina che abitava in un villaggio vicino al bosco. Tutti la chiamavano Cappuccetto Rosso.";
      const res = TextNormalizer.computeGulpease(text);
      expect(res.score).toBeGreaterThanOrEqual(60);
      expect(['facile', 'molto_facile']).toContain(res.level);
    });

    it('deve tratar abreviações comuns (dott., prof., sig., es., ecc.) sem fragmentar frases', () => {
      const text = 'Il dott. Rossi e il prof. Bianchi sono arrivati ieri. Hanno portato i documenti.';
      const res = TextNormalizer.computeGulpease(text);
      expect(res.fr).toBe(2);
    });

    it('deve retornar pontuação zero e nível difícil de forma segura para texto vazio ou sem palavras', () => {
      const resEmpty = TextNormalizer.computeGulpease('');
      expect(resEmpty.score).toBe(0);
      expect(resEmpty.p).toBe(0);
      expect(resEmpty.level).toBe('molto_difficile');

      const resPunct = TextNormalizer.computeGulpease('... --- ???');
      expect(resPunct.score).toBe(0);
      expect(resPunct.p).toBe(0);
    });
  });

  // ────────────────────────────────────────────────────────────
  // 7. END-TO-END PIPELINE ON AUTHENTIC CORPUS
  // ────────────────────────────────────────────────────────────
  describe('Domain 7: End-to-End Pipeline on Authentic Italian Corpus', () => {
    it('deve normalizar perfeitamente a estrofe de Bella Ciao para lemas de dicionário', () => {
      const text = "Una mattina mi son svegliato, o bella ciao! E ho trovato l'invasor. O partigiano, portami via, ché mi sento di morir.";
      const lemmas = TextNormalizer.normalizeText(text);

      expect(lemmas).toContain('uno');
      expect(lemmas).toContain('essere');    // son -> sono -> essere
      expect(lemmas).toContain('svegliare'); // svegliato -> svegliare
      expect(lemmas).toContain('bello');     // bella -> bello
      expect(lemmas).toContain('ciao');
      expect(lemmas).toContain('avere');     // ho -> avere
      expect(lemmas).toContain('trovare');   // trovato -> trovare
      expect(lemmas).toContain('il');        // l' -> il
      expect(lemmas).toContain('invasore');  // invasor -> invasore
      expect(lemmas).toContain('portare');   // portami -> porta -> portare
      expect(lemmas).toContain('morire');    // morir -> morire
    });
  });
});
