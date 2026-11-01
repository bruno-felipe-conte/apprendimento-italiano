// @vitest-environment happy-dom
import { describe, it, expect } from 'vitest';
import ProductionValidator from '../js/production.js';

describe('ProductionValidator Unit Test Suite (F6)', () => {
  // Domain 1: Accent Normalization & Diacritic Equivalence
  describe('Domain 1: Accent Normalization & Diacritic Equivalence', () => {
    it('normalizes vowels with grave and acute accents to apostrophe convention', () => {
      expect(ProductionValidator.normalize('è')).toBe("e'");
      expect(ProductionValidator.normalize('é')).toBe("e'");
      expect(ProductionValidator.normalize('à')).toBe("a'");
      expect(ProductionValidator.normalize('ì')).toBe("i'");
      expect(ProductionValidator.normalize('ò')).toBe("o'");
      expect(ProductionValidator.normalize('ù')).toBe("u'");
    });

    it('validates accent-equivalent answers as exact match (dist 0)', () => {
      expect(ProductionValidator.validate("e'", 'è').isCorrect).toBe(true);
      expect(ProductionValidator.validate('è', "e'").isCorrect).toBe(true);
      expect(ProductionValidator.validate("perche'", 'perché').isCorrect).toBe(true);
      expect(ProductionValidator.validate('città', "citta'").isCorrect).toBe(true);
      expect(ProductionValidator.validate("piu'", 'più').isCorrect).toBe(true);
      expect(ProductionValidator.validate("cosi'", 'così').isCorrect).toBe(true);
      expect(ProductionValidator.validate("puo'", 'può').isCorrect).toBe(true);
    });

    it('handles uppercase accented strings', () => {
      expect(ProductionValidator.normalize('È')).toBe("e'");
      expect(ProductionValidator.normalize('CITTÀ')).toBe("citta'");
      expect(ProductionValidator.validate('CITTÀ', "citta'").isCorrect).toBe(true);
    });

    it('normalizes full sentences with multiple accents', () => {
      const res = ProductionValidator.validate("lui e' piu' alto di me", 'lui è più alto di me');
      expect(res.isCorrect).toBe(true);
      expect(res.distance).toBe(0);
    });
  });

  // Domain 2: Typographic Quotes & Apostrophe Variations
  describe('Domain 2: Typographic Quotes & Apostrophe Variations', () => {
    it('normalizes curved apostrophes and quotes to straight apostrophe', () => {
      expect(ProductionValidator.normalize('l’amico')).toBe("l'amico");
      expect(ProductionValidator.normalize('un’ora')).toBe("un'ora");
      expect(ProductionValidator.normalize('c’era')).toBe("c'era");
      expect(ProductionValidator.normalize('d`oro')).toBe("d'oro");
    });

    it('corrects accidental space after mobile keyboard elision', () => {
      expect(ProductionValidator.normalize("l' amico")).toBe("l'amico");
      expect(ProductionValidator.normalize("un' ora")).toBe("un'ora");
      expect(ProductionValidator.normalize("dell' acqua")).toBe("dell'acqua");
    });
  });

  // Domain 3: Whitespace & Extreme Punctuation
  describe('Domain 3: Whitespace & Extreme Punctuation', () => {
    it('trims leading, trailing and internal multiple spaces', () => {
      expect(ProductionValidator.normalize('  il    colosseo   ')).toBe('il colosseo');
    });

    it('removes extreme outer punctuation while preserving internal apostrophes', () => {
      expect(ProductionValidator.normalize("   l'amico!?!   ")).toBe("l'amico");
      expect(ProductionValidator.normalize("...perche'...")).toBe("perche'");
    });

    it('handles purely punctuation inputs as empty', () => {
      const res = ProductionValidator.validate('... ? !', 'ciao');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('vazio');
    });
  });

  // Domain 4: Levenshtein Distance Mathematical Matrix
  describe('Domain 4: Levenshtein Distance Mathematical Matrix', () => {
    it('computes exact distance matrix values', () => {
      expect(ProductionValidator.levenshtein('roma', 'roma')).toBe(0);
      expect(ProductionValidator.levenshtein('gatto', 'matto')).toBe(1);
      expect(ProductionValidator.levenshtein('pasta', 'pata')).toBe(1);
      expect(ProductionValidator.levenshtein('casa', 'scatola')).toBe(4);
    });

    it('normalizes strings automatically before calculating distance', () => {
      expect(ProductionValidator.levenshtein('città', "citta'")).toBe(0);
      expect(ProductionValidator.levenshtein("perche'", 'perché')).toBe(0);
    });
  });

  // Domain 5: Fuzzy Matching Thresholds
  describe('Domain 5: Fuzzy Matching Thresholds', () => {
    it('rejects short words (< 5 chars) with distance = 1', () => {
      const res = ProductionValidator.validate('cane', 'pane');
      expect(res.isCorrect).toBe(false);
      expect(res.isFuzzy).toBe(false);
    });

    it('accepts medium words (>= 5 chars) with distance = 1 as fuzzy', () => {
      const res = ProductionValidator.validate('arrivedirci', 'arrivederci');
      expect(res.isCorrect).toBe(true);
      expect(res.isFuzzy).toBe(true);
      expect(res.distance).toBe(1);
      expect(res.diagnostic).toContain('Quase lá');
    });

    it('accepts long words (>= 8 chars) with distance <= 2 as fuzzy', () => {
      const res = ProductionValidator.validate('univerzita', 'universita');
      expect(res.isCorrect).toBe(true);
      expect(res.isFuzzy).toBe(true);
      expect(res.distance).toBe(1);
    });

    it('rejects words with distance >= 3', () => {
      const res = ProductionValidator.validate('universidade', 'universita');
      expect(res.isCorrect).toBe(false);
    });
  });

  // Domain 6: Morphological Diagnostics — Artigos
  describe('Domain 6: Morphological Diagnostics — Artigos', () => {
    it('diagnoses incorrect definite article substitution', () => {
      const res = ProductionValidator.validate('il zaino', 'lo zaino');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('artigo');
      expect(res.diagnostic).toContain('lo');
    });

    it('diagnoses incorrect indefinite article substitution', () => {
      const res = ProductionValidator.validate('un studente', 'uno studente');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('artigo');
      expect(res.diagnostic).toContain('uno');
    });
  });

  // Domain 7: Morphological Diagnostics — Doppie (Consoantes Duplas)
  describe('Domain 7: Morphological Diagnostics — Doppie', () => {
    it('diagnoses missing double consonants and avoids fuzzy false positives', () => {
      const res = ProductionValidator.validate('capuccino', 'cappuccino');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('doppia');
      expect(res.diagnostic).toContain('pp');
    });

    it('diagnoses missing double consonant in minimal pair pala/palla', () => {
      const res = ProductionValidator.validate('pala', 'palla');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('doppia');
      expect(res.diagnostic).toContain('ll');
    });

    it('diagnoses spurious double consonants', () => {
      const res = ProductionValidator.validate('fatto', 'fato');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('doppia');
    });
  });

  // Domain 8: Morphological Diagnostics — Desinência Verbal
  describe('Domain 8: Morphological Diagnostics — Desinência Verbal', () => {
    it('diagnoses verb person/tense ending errors', () => {
      const res = ProductionValidator.validate('parlate', 'parliamo');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('desinência verbal');
    });

    it('diagnoses imperfect vs present verb endings', () => {
      const res = ProductionValidator.validate('parlavamo', 'parliamo');
      expect(res.isCorrect).toBe(false);
      expect(res.diagnostic).toContain('desinência verbal');
    });
  });

  // Domain 9: Synonyms & Multiple Accepted Variants
  describe('Domain 9: Synonyms & Multiple Accepted Variants', () => {
    it('accepts valid alternative variants without penalty', () => {
      const res = ProductionValidator.validate('il cane', 'cane', ['il cane', 'un cane']);
      expect(res.isCorrect).toBe(true);
      expect(res.distance).toBe(0);
    });

    it('calculates distance against the closest variant', () => {
      const res = ProductionValidator.validate('cagnolino', 'cane', ['cagnolino', 'cucciolo']);
      expect(res.isCorrect).toBe(true);
      expect(res.distance).toBe(0);
    });
  });

  // Domain 10: Robustness, Defensividade e Fuzzing
  describe('Domain 10: Robustness, Defensividade e Fuzzing', () => {
    it('handles null and undefined safely without throwing', () => {
      expect(ProductionValidator.normalize(null as any)).toBe('');
      expect(ProductionValidator.normalize(undefined as any)).toBe('');
      const resNull = ProductionValidator.validate(null as any, 'roma');
      expect(resNull.isCorrect).toBe(false);
      expect(resNull.diagnostic).toContain('vazio');
    });

    it('handles very large input strings without stack overflow', () => {
      const hugeString = 'a'.repeat(2000);
      const res = ProductionValidator.validate(hugeString, 'roma');
      expect(res.isCorrect).toBe(false);
      expect(res.distance).toBeGreaterThan(100);
    });

    it('treats XSS / HTML scripts as inert text', () => {
      const xss = '<script>alert(1)</script>';
      const res = ProductionValidator.validate(xss, 'roma');
      expect(res.isCorrect).toBe(false);
    });
  });
});
