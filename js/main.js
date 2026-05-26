/**
 * Main App - Italian Learning App (v0.x.x)
 * Integração completa com: VocabularioService, ReviewService, QuizService + Progressão + Heatmaps
 */

import VocabularyService from './vocabulary_service.js';
import ReviewService from './review_service.js';
import QuizService from './quiz_service.js';

// Exemplo de uso (remover se não necessário)
/*
window.app = new App();

// Exemplo: Carregar vocabulário + persistir ao localStorage
const vocabService = new VocabularyService();
await vocabService.carregarJSON();
vocabService.persistirPalavras(vocabService.defaultData);

// Exemplo: Adicionar card ao review queue (SM-2)
reviewService.adicionarAoQueue({ id: 'palavra1', italiano: 'ciao', nivel: 1 });

// Exemplo: Verificar reviews hoje
const pending = await reviewService.obterParaReviewHoje();
console.log('[Review]', 'Reviews pendentes:', pending);
*/
