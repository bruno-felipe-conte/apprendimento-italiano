import { z } from 'zod';

// ==========================================
// SCHEMAS DE VALIDAÇÃO DE CONTEÚDO (EV-03)
// ==========================================

export const NivelCEFRSchema = z.enum(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']);

export const PalavraTemploSchema = z.preprocess(
  (val: unknown) => {
    if (val && typeof val === 'object') {
      const copy = { ...(val as Record<string, unknown>) };
      if (!copy.exemplo && copy.esempio) copy.exemplo = copy.esempio;
      if (!copy.exemplo_pt && copy.esempio_pt) copy.exemplo_pt = copy.esempio_pt;
      return copy;
    }
    return val;
  },
  z.object({
    id: z.string().min(1, 'ID da palavra é obrigatório'),
    italiano: z.string().min(1, 'Termo em italiano é obrigatório'),
    portugues: z.string().min(1, 'Tradução em português é obrigatória'),
    genero: z.string().nullable().optional(),
    plural: z.string().nullable().optional(),
    exemplo: z.string().min(1, 'Frase de exemplo é obrigatória'),
    exemplo_pt: z.string().min(1, 'Tradução do exemplo é obrigatória'),
    categoria: z.string().min(1, 'Categoria é obrigatória'),
    dificuldade: z.enum(['facil', 'medio', 'dificil']).or(z.string()),
    audio_ipa: z.string().optional()
  })
);

export const TemploSchema = z.object({
  templo: z.number().int().positive('Número do templo deve ser inteiro positivo'),
  cidade: z.string().min(1, 'Cidade do templo é obrigatória'),
  nivel: NivelCEFRSchema.or(z.string()),
  palavras: z.array(PalavraTemploSchema).min(1, 'O templo deve conter ao menos 1 palavra')
});

export const ParolaStoriaSchema = z.object({
  parola: z.string().min(1),
  traduzione: z.string().min(1),
  ipa: z.string().optional(),
  categoria: z.string().optional()
});

export const ParagrafoStoriaSchema = z.object({
  id: z.string().min(1),
  italiano: z.string().min(1),
  portugues: z.string().min(1),
  parole: z.array(ParolaStoriaSchema).optional().default([])
});

export const StoriaItemSchema = z.object({
  id: z.string().min(1),
  titulo: z.string().min(1),
  titulo_pt: z.string().min(1),
  nivel: NivelCEFRSchema.or(z.string()),
  icone: z.string().optional().default('📜'),
  autor: z.string().optional().default('Autentico'),
  tema: z.string().optional(),
  descricao: z.string().optional(),
  descricao_pt: z.string().optional(),
  xp_recompensa: z.number().nonnegative().optional().default(50),
  testo: z.array(ParagrafoStoriaSchema).min(1, 'A história deve conter ao menos 1 parágrafo')
});

export const StorieFileSchema = z.object({
  storie: z.array(StoriaItemSchema).min(1)
});

export const TurnoDialogoSchema = z.object({
  id: z.number().int().or(z.string()),
  personaggio: z.string().min(1),
  frase: z.string().min(1),
  traducao: z.string().min(1),
  audio_ipa: z.string().optional(),
  alternativas: z.array(z.string()).optional(),
  resposta_correta: z.number().int().nonnegative().optional()
});

export const DialogoItemSchema = z.object({
  id: z.string().min(1),
  titulo: z.string().min(1),
  icone: z.string().optional().default('💬'),
  nivel: NivelCEFRSchema.or(z.string()),
  contexto: z.string().min(1),
  turni: z.array(TurnoDialogoSchema).min(1, 'O diálogo deve conter ao menos 1 turno de fala')
});

export const DialoghiFileSchema = z.object({
  dialogi: z.array(DialogoItemSchema).min(1)
});

export const EstrofeCanzoneSchema = z.object({
  id: z.number().int().or(z.string()),
  texto_completo: z.string().min(1),
  texto_lacuna: z.string().min(1),
  palavra_oculta: z.string().min(1),
  traducao: z.string().min(1),
  dica: z.string().optional()
});

export const CanzoneItemSchema = z.object({
  id: z.string().min(1),
  titulo: z.string().min(1),
  artista: z.string().min(1),
  nivel: NivelCEFRSchema.or(z.string()),
  icone: z.string().optional().default('🎵'),
  tema: z.string().optional(),
  estrofes: z.array(EstrofeCanzoneSchema).min(1, 'A canção deve conter ao menos 1 estrofe')
});

export const CanzoniFileSchema = z.object({
  canzoni: z.array(CanzoneItemSchema).min(1)
});

export const ImitazioneItemSchema = z.object({
  id: z.string().or(z.number()),
  frase: z.string().min(1),
  traducao: z.string().min(1),
  audio_ipa: z.string().optional(),
  dificuldade: z.string().optional(),
  nivel: z.string().optional()
});

export const ImitazioniFileSchema = z.object({
  imitazioni: z.array(ImitazioneItemSchema).min(1)
}).or(z.array(ImitazioneItemSchema));

// ==========================================
// SCHEMAS TOP 1.000 VOCABULÁRIO & TOP 500 FLASHCARDS
// ==========================================

export const TopVocabItemSchema = z.object({
  rank: z.number().int().positive(),
  id: z.string().min(1),
  italiano: z.string().min(1),
  portugues: z.string().min(1),
  categoria: z.string().min(1),
  genere: z.string().nullable().optional(),
  plurale: z.string().nullable().optional(),
  livello: z.string().min(1),
  audio_ipa: z.string().optional(),
  exemplo: z.string().min(1),
  exemplo_pt: z.string().min(1),
  collocazioni: z.array(z.string()).optional().default([])
});

export const TopVocabFileSchema = z.object({
  total: z.number().int().positive(),
  fonte: z.string().optional(),
  niveis: z.record(z.string(), z.number()).optional(),
  palavras: z.array(TopVocabItemSchema).length(1000, 'Top 1000 deve conter exatamente 1000 palavras')
});

export const TopFlashcardDeckInfoSchema = z.object({
  id: z.string().min(1),
  nome: z.string().min(1),
  icone: z.string().optional(),
  total: z.number().int().positive(),
  descricao: z.string().optional()
});

export const TopFlashcardItemSchema = z.object({
  id: z.string().min(1),
  deck: z.string().min(1),
  deck_nome: z.string().min(1),
  nivel: z.string().min(1),
  italiano: z.string().min(1),
  portugues: z.string().min(1),
  categoria: z.string().min(1),
  frente: z.string().min(1),
  verso: z.string().min(1),
  traducao_frase: z.string().min(1),
  dica: z.string().optional(),
  exemplo: z.string().min(1),
  exemplo_pt: z.string().min(1),
  audio_palavra: z.string().min(1),
  audio_frase: z.string().min(1),
  audio_ipa: z.string().optional(),
  explicacao: z.string().optional()
});

export const TopFlashcardsFileSchema = z.object({
  total: z.number().int().positive(),
  decks: z.record(z.string(), TopFlashcardDeckInfoSchema),
  cards: z.array(TopFlashcardItemSchema).length(500, 'Top 500 deve conter exatamente 500 cards')
});
