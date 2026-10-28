import { describe, it, expect } from 'vitest';
import path from 'node:path';
import fs from 'node:fs';
import {
  TemploSchema,
  StoriaItemSchema,
  DialogoItemSchema,
  TopVocabFileSchema,
  TopFlashcardsFileSchema
} from '../scripts/schemas';
import { validarTodosConteudos } from '../scripts/validate_content';
import { ingerirConteudo } from '../scripts/ingest_content';

describe('EV-03: Content Pipeline Automatizado', () => {
  describe('Validação de Schemas Zod', () => {
    it('deve aprovar um templo válido com campos obrigatórios e normalização', () => {
      const temploValido = {
        templo: 99,
        cidade: 'Venezia',
        nivel: 'B1',
        palavras: [
          {
            id: 't99_001',
            italiano: 'gondola',
            portugues: 'gôndola',
            exemplo: 'La gondola scivola sul canale.',
            exemplo_pt: 'A gôndola desliza pelo canal.',
            categoria: 'trasporti',
            dificuldade: 'medio'
          }
        ]
      };

      const resultado = TemploSchema.safeParse(temploValido);
      expect(resultado.success).toBe(true);
      if (resultado.success) {
        expect(resultado.data.cidade).toBe('Venezia');
        expect(resultado.data.palavras[0].italiano).toBe('gondola');
      }
    });

    it('deve rejeitar templos com número negativo ou sem palavras', () => {
      const temploInvalido = {
        templo: -5,
        cidade: 'Milano',
        nivel: 'A1',
        palavras: []
      };

      const resultado = TemploSchema.safeParse(temploInvalido);
      expect(resultado.success).toBe(false);
    });

    it('deve validar estrutura de história completa com parágrafos e palavras-chave', () => {
      const storiaValida = {
        id: 'stor_teste_01',
        titulo: 'Il Colosseo Misterioso',
        titulo_pt: 'O Coliseu Misterioso',
        nivel: 'B1',
        testo: [
          {
            id: 'p1',
            italiano: 'Sotto la luna di Roma, il monumento brillava.',
            portugues: 'Sob a lua de Roma, o monumento brilhava.',
            parole: [
              {
                parola: 'brillava',
                traduzione: 'brilhava',
                categoria: 'verbo'
              }
            ]
          }
        ]
      };

      const resultado = StoriaItemSchema.safeParse(storiaValida);
      expect(resultado.success).toBe(true);
      if (resultado.success) {
        expect(resultado.data.autor).toBe('Autentico');
        expect(resultado.data.xp_recompensa).toBe(50);
      }
    });

    it('deve validar estrutura de diálogos com turnos de personagens', () => {
      const dialogoValido = {
        id: 'dial_teste_01',
        titulo: 'In Farmacia',
        nivel: 'A2',
        contexto: 'Comprando remédio para dor de cabeça.',
        turni: [
          {
            id: 1,
            personaggio: 'Farmacista',
            frase: 'Ha una ricetta medica?',
            traducao: 'Tem uma receita médica?'
          }
        ]
      };

      const resultado = DialogoItemSchema.safeParse(dialogoValido);
      expect(resultado.success).toBe(true);
    });
  });

  describe('Ingestão e Normalização de Rascunhos', () => {
    it('deve ingerir e normalizar templo em modo dry-run sem corromper dados', () => {
      const tempPath = path.resolve(process.cwd(), 'temp_draft_templo.json');
      fs.writeFileSync(
        tempPath,
        JSON.stringify({
          templo: 99,
          cidade: 'Firenze',
          nivel: 'A2',
          palavras: [
            {
              italiano: 'duomo',
              portugues: 'catedral',
              exemplo: 'Il Duomo di Firenze è magnifico.',
              exemplo_pt: 'A Catedral de Florença é magnífica.'
            }
          ]
        })
      );

      try {
        const resultado = ingerirConteudo({
          tipo: 'templo',
          caminhoEntrada: tempPath,
          dryRun: true
        });

        expect(resultado.sucesso).toBe(true);
        expect(resultado.totalItens).toBe(1);
        expect(resultado.mensagem).toContain('Templo 99');
      } finally {
        if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
      }
    });

    it('deve rejeitar ingestão de arquivo inexistente', () => {
      const resultado = ingerirConteudo({
        tipo: 'templo',
        caminhoEntrada: './arquivo_fantasma_123.json'
      });
      expect(resultado.sucesso).toBe(false);
      expect(resultado.mensagem).toContain('não encontrado');
    });
  });

  describe('Auditoria Completa de Conteúdo dos Dados Mestres (data/)', () => {
    it('deve validar 100% dos 51 templos e histórias do repositório', () => {
      const relatorio = validarTodosConteudos();
      expect(relatorio.sucesso).toBe(true);
      expect(relatorio.totalArquivos).toBeGreaterThanOrEqual(51);
      expect(relatorio.totalPalavras).toBeGreaterThan(5000);
      expect(relatorio.erros).toHaveLength(0);
    }, 20000);

    it('deve validar o arquivo mestre top1000_vocabulario.json com 1000 palavras enriquecidas', () => {
      const top1000Path = path.resolve(process.cwd(), 'data', 'top1000_vocabulario.json');
      const raw = fs.readFileSync(top1000Path, 'utf-8');
      const json = JSON.parse(raw);
      const resultado = TopVocabFileSchema.safeParse(json);
      expect(resultado.success).toBe(true);
      if (resultado.success) {
        expect(resultado.data.total).toBe(1000);
        expect(resultado.data.palavras).toHaveLength(1000);
        expect(resultado.data.palavras[0].rank).toBe(1);
        expect(resultado.data.palavras[999].rank).toBe(1000);
      }
    });

    it('deve validar o arquivo mestre top500_flashcards.json com 500 cards e 5 baralhos de 100', () => {
      const top500Path = path.resolve(process.cwd(), 'data', 'top500_flashcards.json');
      const raw = fs.readFileSync(top500Path, 'utf-8');
      const json = JSON.parse(raw);
      const resultado = TopFlashcardsFileSchema.safeParse(json);
      expect(resultado.success).toBe(true);
      if (resultado.success) {
        expect(resultado.data.total).toBe(500);
        expect(resultado.data.cards).toHaveLength(500);
        expect(Object.keys(resultado.data.decks)).toHaveLength(5);
        expect(resultado.data.decks['colocacoes'].total).toBe(100);
        expect(resultado.data.decks['falsi_amici'].total).toBe(100);
        expect(resultado.data.decks['preposizioni'].total).toBe(100);
        expect(resultado.data.decks['verbi_irregolari'].total).toBe(100);
        expect(resultado.data.decks['situazioni_reali'].total).toBe(100);
      }
    });
  });
});
