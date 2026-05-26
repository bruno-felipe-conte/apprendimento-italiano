/**
 * QuizData - Dados inline de quizzes para fallback (quizzes.json vazio)
 */

// Saudações
const QUIZ_SAUDACOES = [
  {
    id: 'q_s_01',
    italiano: 'Ciao',
    ptbr: 'Olá / Adeus',
    respostaCorreta: 'ciao',
    distratores: ['buongiorno', 'arrivederci', 'prego'],
    dica: 'Uso informal para cumprimentos/adeus'
  },
  {
    id: 'q_s_02',
    italiano: 'Prego',
    ptbr: 'Por favor / Coma',
    respostaCorreta: 'prego',
    distratores: ['ciao', 'grazie', 'buongiorno'],
    dica: 'Dizido na mesa ao comer'
  },
  {
    id: 'q_s_03',
    italiano: 'Grazie',
    ptbr: 'Obrigado(a)',
    respostaCorreta: 'grazie',
    distratores: ['per favore', 'prego', 'buonasera'],
    dica: 'Agradeecimento básico'
  },
  {
    id: 'q_s_04',
    italiano: 'Buongiorno',
    ptbr: 'Bom dia',
    respostaCorreta: 'buongiorno',
    distratores: ['ciao', 'buonasera', 'bona notte'],
    dica: 'Cumprimento matinal'
  },
  {
    id: 'q_s_05',
    italiano: 'Arrivederci',
    ptbr: 'Tchau / Até',
    respostaCorreta: 'arrivederci',
    distratores: ['ciao', 'prego', 'buonasera'],
    dica: 'Cumprimento formal para despedida'
  }
];

// Números (0-29)
const QUIZ_NUMEROS = [
  { id: 'q_n_01', italiano: 'Uno', ptbr: 'Um', respostaCorreta: 'uno', distratores: ['due', 'tre', 'quattro'], dica: 'Número 1' },
  { id: 'q_n_02', italiano: 'Due', ptbr: 'Dois', respostaCorreta: 'due', distratores: ['uno', 'tre', 'cinque'], dica: 'Número 2' },
  { id: 'q_n_03', italiano: 'Tre', ptbr: 'Três', respostaCorreta: 'tre', distratores: ['due', 'quattro', 'cinque'], dica: 'Número 3' },
  { id: 'q_n_04', italiano: 'Quattro', ptbr: 'Quatro', respostaCorreta: 'quattro', distratores: ['tre', 'cinque', 'sei'], dica: 'Número 4' },
  { id: 'q_n_05', italiano: 'Cinque', ptbr: 'Cinco', respostaCorreta: 'cinque', distratores: ['quattro', 'sei', 'sette'], dica: 'Número 5' },
  { id: 'q_n_06', italiano: 'Dieci', ptbr: 'Dez', respostaCorreta: 'dieci', distratores: ['nove', 'undici', 'dodici'], dica: 'Número 10' },
  { id: 'q_n_07', italiano: 'Venti', ptbr: 'Vinte', respostaCorreta: 'venti', distratores: ['trenta', 'quaranta', 'cinquanta'], dica: 'Número 20' },
  { id: 'q_n_08', italiano: 'Ventuno', ptbr: 'Vinte e um', respostaCorreta: 'ventuno', distratores: ['venti', 'ventidue', 'ventitre'], dica: 'Número 21' },
  { id: 'q_n_09', italiano: 'Novanta', ptbr: 'Noventa', respostaCorreta: 'novanta', distratores: ['ottanta', 'cento', 'nonanta'], dica: 'Número 90' },
  { id: 'q_n_10', italiano: 'Centuno', ptbr: 'Cento', respostaCorreta: 'centuno', distratores: ['novanta', 'duecento', 'centodieci'], dica: 'Número 100' }
];

// Verbos (presente indicativo)
const QUIZ_VERBOS = [
  { id: 'q_v_01', italiano: 'Andare', ptbr: 'Ir', respostaCorreta: 'vado', distratores: ['mangio', 'parlo', 'dormo'], dica: 'Eu vou (ir)' },
  { id: 'q_v_02', italiano: 'Mangiare', ptbr: 'Comer', respostaCorreta: 'mango', distratores: ['bevo', 'parlo', 'corro'], dica: 'Eu como' },
  { id: 'q_v_03', italiano: 'Parlare', ptbr: 'Conversar', respostaCorreta: 'paro', distratores: ['mangio', 'bevo', 'dormo'], dica: 'Eu falo' },
  { id: 'q_v_04', italiano: 'Dormire', ptbr: 'Dormir', respostaCorreta: 'dormo', distratores: ['parlo', 'mango', 'studio'], dica: 'Eu durmo' },
  { id: 'q_v_05', italiano: 'Studiare', ptbr: 'Estudar', respostaCorreta: 'studio', distratores: ['parlo', 'mangio', 'lavoro'], dica: 'Eu estudo' }
];

// Família
const QUIZ_FAMILIA = [
  { id: 'q_f_01', italiano: 'Mamma', ptbr: 'Mãe', respostaCorreta: 'mamma', distratores: ['papà', 'nonna', 'zia'], dica: 'Mãe' },
  { id: 'q_f_02', italiano: 'Papà', ptbr: 'Pai', respostaCorreta: 'papà', distratores: ['mamma', 'nonno', 'fratello'], dica: 'Pai' },
  { id: 'q_f_03', italiano: 'Nonna', ptbr: 'Vovó (avó)', respostaCorreta: 'nonna', distratores: ['zia', 'nipote', 'nonno'], dica: 'Avó' },
  { id: 'q_f_04', italiano: 'Zia', ptbr: 'Tia', respostaCorreta: 'zia', distratores: ['fratello', 'sorella', 'cugino'], dica: 'Tia (irmã do pai/mãe)' },
  { id: 'q_f_05', italiano: 'Fratello', ptbr: 'Irmão (masc.)', respostaCorreta: 'fratello', distratores: ['sorella', 'cugino', 'nipote'], dica: 'Irmão masculino' },
  { id: 'q_f_06', italiano: 'Sorella', ptbr: 'Irmã (fem.)', respostaCorreta: 'sorella', distratores: ['fratello', 'zio', 'cugina'], dica: 'Irmã feminina' },
  { id: 'q_f_07', italiano: 'Nonno', ptbr: 'Vovô (avô)', respostaCorreta: 'nonno', distratores: ['zia', 'papà', 'mamma'], dica: 'Avô' }
];

// Exportar dados inline
export default {
  SAUDACOES: QUIZ_SAUDACOES,
  NUMEROS: QUIZ_NUMEROS,
  VERBOS: QUIZ_VERBOS,
  FAMILIA: QUIZ_FAMILIA
};
