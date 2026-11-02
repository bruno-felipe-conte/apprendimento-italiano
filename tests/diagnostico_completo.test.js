// tests/diagnostico_completo.test.js
// Testes unitários para o Teste de Nível Completo (+25 Palavras e 25 Frases A1→C1)

import { describe, it, expect } from 'vitest';
import VocabDiagnostic from '../js/diagnostico.js';

describe('Teste Completo de Nível de Italiano (Vocabulário Expandido + 25 Frases)', () => {
  it('deve conter exatamente 25 palavras autênticas desafiadoras adicionais', () => {
    expect(Array.isArray(VocabDiagnostic.PALAVRAS_AVANCADAS)).toBe(true);
    expect(VocabDiagnostic.PALAVRAS_AVANCADAS.length).toBe(25);

    // Checa palavras representativas
    const palavras = VocabDiagnostic.PALAVRAS_AVANCADAS.map(p => p.w);
    expect(palavras).toContain('tramonto');
    expect(palavras).toContain('ciononostante');
    expect(palavras).toContain('sgomento');
    expect(palavras).toContain('scaturire');
    expect(palavras).toContain('imprescindibile');
    expect(palavras).toContain('sviscerare');
  });

  it('deve conter exatamente 25 frases autênticas balanceadas em 5 níveis CEFR', () => {
    expect(Array.isArray(VocabDiagnostic.FRASI_DIAGNOSTICO)).toBe(true);
    expect(VocabDiagnostic.FRASI_DIAGNOSTICO.length).toBe(25);

    const contagemNiveis = { A1: 0, A2: 0, B1: 0, B2: 0, C1: 0 };
    VocabDiagnostic.FRASI_DIAGNOSTICO.forEach(f => {
      expect(f.frase).toBeDefined();
      expect(f.frase).toContain('_____');
      expect(f.opcoes.length).toBe(4);
      expect(f.resposta_idx).toBeGreaterThanOrEqual(0);
      expect(f.resposta_idx).toBeLessThan(4);
      expect(f.explicacao).toBeDefined();
      contagemNiveis[f.nivel]++;
    });

    expect(contagemNiveis.A1).toBe(5);
    expect(contagemNiveis.A2).toBe(5);
    expect(contagemNiveis.B1).toBe(5);
    expect(contagemNiveis.B2).toBe(5);
    expect(contagemNiveis.C1).toBe(5);
  });

  it('gerarItensFrases deve embaralhar mantendo a opção correta alinhada ao texto_correto', () => {
    const itens = VocabDiagnostic.gerarItensFrases();
    expect(itens.length).toBe(25);

    itens.forEach(item => {
      expect(item.opcoes[item.resposta_idx]).toBe(item.texto_correto);
    });
  });

  it('calcularScore com 25 frases deve gerar discriminação por nível e teto CEFR', () => {
    // Vocabulário perfeito (simulação)
    const respostasVocab = Array.from({ length: 30 }, (_, i) => ({
      word: `parola_${i}`,
      isPseudoword: false,
      known: true,
      band: (i % 3) + 1
    }));
    // 6 pseudopalavras honestamente rejeitadas
    for (let i = 0; i < 6; i++) {
      respostasVocab.push({ word: `pseudo_${i}`, isPseudoword: true, known: false });
    }

    // Caso 1: Usuário acerta A1, A2 e B1, mas erra B2 e C1
    const respostasFrasesB1 = [
      // A1: 5/5
      { nivel: 'A1', correto: true }, { nivel: 'A1', correto: true }, { nivel: 'A1', correto: true }, { nivel: 'A1', correto: true }, { nivel: 'A1', correto: true },
      // A2: 5/5
      { nivel: 'A2', correto: true }, { nivel: 'A2', correto: true }, { nivel: 'A2', correto: true }, { nivel: 'A2', correto: true }, { nivel: 'A2', correto: true },
      // B1: 4/5
      { nivel: 'B1', correto: true }, { nivel: 'B1', correto: true }, { nivel: 'B1', correto: true }, { nivel: 'B1', correto: true }, { nivel: 'B1', correto: false },
      // B2: 1/5
      { nivel: 'B2', correto: true }, { nivel: 'B2', correto: false }, { nivel: 'B2', correto: false }, { nivel: 'B2', correto: false }, { nivel: 'B2', correto: false },
      // C1: 0/5
      { nivel: 'C1', correto: false }, { nivel: 'C1', correto: false }, { nivel: 'C1', correto: false }, { nivel: 'C1', correto: false }, { nivel: 'C1', correto: false }
    ];

    const scoreB1 = VocabDiagnostic.calcularScore(respostasVocab, respostasFrasesB1);
    expect(scoreB1.nivel_cefr).toBe('B1');
    expect(scoreB1.frasi_score.acertos).toBe(15);
    expect(scoreB1.frasi_score.total).toBe(25);
    expect(scoreB1.frasi_score.por_nivel.A1.acertos).toBe(5);
    expect(scoreB1.frasi_score.por_nivel.B1.acertos).toBe(4);
    expect(scoreB1.frasi_score.por_nivel.C1.acertos).toBe(0);

    // Caso 2: Usuário com proficiência avançada C1
    const respostasFrasesC1 = respostasFrasesB1.map(() => ({ nivel: 'A1', correto: true }));
    const respostasPerfeitas = [];
    ['A1', 'A2', 'B1', 'B2', 'C1'].forEach(lvl => {
      for (let i = 0; i < 5; i++) respostasPerfeitas.push({ nivel: lvl, correto: true });
    });

    const scoreC1 = VocabDiagnostic.calcularScore(respostasVocab, respostasPerfeitas);
    expect(scoreC1.nivel_cefr).toBe('C1/C2');
    expect(scoreC1.frasi_score.acertos).toBe(25);
    expect(scoreC1.confiavel).toBe(true);
  });
});
