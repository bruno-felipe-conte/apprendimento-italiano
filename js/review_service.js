/**
 * ReviewService - Sistema SM-2 para reviews agendados de flashcards
 */

class ReviewService {
  constructor() {
    this.storageKey = 'it_reviews'; // Unificado com other data
    this.reviewQueue = []; // Array de reviews agendadas por timestamp
    
    /**
     * Tabela espaçamento inicial (SM-2 base):
     * Facíil: 1d, Médio: 3d, Difícil: 7d
     */
    this.intervalosBase = { facil: 1, medio: 3, dificil: 7 };
    
    /**
     * Tabela de multiplicadores (simplificado):
     * A cada acerto o intervalo dobra até um teto baseado no nivel do usuário.
     */
    this.tetoIntervaloPorNivel = {
      1: 30,
      2: 60,
      3: 120,
      4: 365 // Teto em dias após level 4
    };
  }

  /**
   * Adiciona um card ao sistema de reviews
   */
  adicionarAoQueue(cardData) {
    if (!cardData || !cardData.id) {
      console.error('[ReviewService]', 'Card inválido para review');
      return null;
    }

    const agora = Date.now();
    const intervaloDias = this.intervalosBase[cardData.dificuldade] || 3;
    
    // Calcular timestamp do próximo review (hoje + intervalos)
    const nextReviewDate = new Date(agora);
    nextReviewDate.setDate(nextReviewDate.getDate() + intervaloDias);

    const review = {
      cardId: cardData.id,
      italiano: cardData.italiano || '',
      portugues: cardData.portugues || '',
      dificuldade: cardData.dificuldade || 'medio',
      categoria: cardData.categoria || null,
      
      // Metadata SM-2
      easiness: 2.5, // EF base (Easy Factor)
      lastReview: Date.parse(nextReviewDate.toISOString()),
      nextReview: nextReviewDate.getTime(),
      intervalosPassados: 0,
      
      dataCriacao: agora,
      status: 'pending', // pending, reviewed
    };

    this.reviewQueue.push(review);
    console.log(`[ReviewService] Adicionado ao queue: ${cardData.italiano} (nível: ${cardData.nivel || 1})`);
    
    return review;
  }

  /**
   * Processa review de um card (acerto/repetir)
   * 
   * @param {string} cardId - ID do card
   * @param {string} resultado - 'easy' (0.9), 'good' (1.3), 'hard' (1.5)
   */
  processarReview(cardId, resultado = 'good') {
    const reviewIndex = this.reviewQueue.findIndex(r => r.cardId === cardId);
    if (reviewIndex === -1) return null;

    const review = this.reviewQueue[reviewIndex];
    const agora = Date.now();
    
    // Verificar se já passou da data do review
    if (agora > review.nextReview) {
      console.warn(`[ReviewService] Review atrasada para ${cardId}`);
    }

    // Calcular novo intervalo baseado no resultado e EF
    const novoIntervalo = this.calcularNovoIntervalo(review, resultado);
    
    // Atualizar metadata SM-2
    review.intervalosPassados++;
    review.lastReview = agora;
    review.nextReview = Date.parse(new Date(agora + novoIntervalo));
    review.easiness *= novoIntervalo.efMultiplier || 1.3;

    // Determinar dificuldade baseada no EF (para intervalos base)
    const novaDificuldade = this.obterDificuldadePorEF(review.easiness);
    review.dificuldade = novaDificuldade;

    // Atualizar localStorage
    this.salvarReviewAoStorage(review);

    return {
      cardId,
      novoIntervalo,
      status: 'reviewed'
    };
  }

  /**
   * Calcula novo intervalo baseado no resultado (SM-2 simplificado)
   */
  calcularNovoIntervalo(review, resultado) {
    const intervalosBase = {
      easy: { dias: 1, efMultiplier: 0.9 },
      good: { dias: 3, efMultiplier: 1.3 },
      hard: { dias: 7, efMultiplier: 1.5 }
    };

    const base = intervalosBase[resultado] || intervalosBase.good;
    let novoIntervalo = base.dias * (review.easiness / 2.5); // Normalizar por EF base

    // Aplicar teto baseado no nivel do usuário
    const tetoDias = this.tetoIntervaloPorNivel[review.nivel] || this.tetoIntervaloPorNivel[3];
    novoIntervalo = Math.min(novoIntervalo, tetoDias);

    // Arredondar para múltiplo de base (simplificado)
    const baseMultiplo = 7; 
    novoIntervalo = Math.ceil(novoIntervalo / baseMultiplo) * baseMultiplo || novoIntervalo;

    return { dias: novoIntervalo, efMultiplier: base.efMultiplier };
  }

  /**
   * Determina dificuldade baseada no EF (simplificação heurística)
   */
  obterDificuldadePorEF(easiness) {
    if (easiness < 2.4) return 'facil';
    if (easiness < 2.7) return 'medio';
    if (easiness < 3.0) return 'dificil';
    return 'extremo';
  }

  /**
   * Salva review ao localStorage (append)
   */
  salvarReviewAoStorage(review) {
    const reviews = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    const existingIndex = reviews.findIndex(r => r.cardId === review.cardId);

    if (existingIndex >= 0) {
      // Update existente
      reviews[existingIndex] = { ...review, updatedAt: Date.now() };
    } else {
      // Append novo
      reviews.push(review);
    }

    localStorage.setItem(this.storageKey, JSON.stringify(reviews));
  }

  /**
   * Retorna cards para review hoje (pending)
   */
  async obterParaReviewHoje() {
    await this._carregarReviewsAoStorage(); // Lazy load
    
    const hoje = Date.now();
    return this.reviewQueue.filter(r => {
      if (r.status === 'reviewed') return false;
      return r.nextReview >= hoje && r.nextReview <= hoje + 24 * 60 * 60 * 1000; // Hoje ou até amanhã
    });
  }

  /**
   * Carrega reviews do storage (lazy load)
   */
  async _carregarReviewsAoStorage() {
    if (!localStorage.getItem(this.storageKey)) return [];
    
    try {
      const raw = localStorage.getItem(this.storageKey);
      this.reviewQueue = JSON.parse(raw || '[]');
      console.log(`[ReviewService] Carregou ${this.reviewQueue.length} reviews pendentes`);
    } catch (e) {
      console.error('[ReviewService]', 'Falha ao carregar reviews:', e.message);
    }
  }

  /**
   * Remove card do queue (se já revisado)
   */
  removerDoQueue(cardId) {
    this.reviewQueue = this.reviewQueue.filter(r => r.cardId !== cardId);
  }
}

// Exemplo de uso:
/*
const reviewService = new ReviewService();

// Ao terminar sessão de flashcards (opcional):
await vocabularyService.carregarJSON();
const pendingCards = await vocabService.obterAleatorias(10);
pendingCards.forEach(card => {
  reviewService.adicionarAoQueue({ id: card.id, italiano: card.italiano, nivel: 1 });
});

// Checar reviews pendentes (ex: ao abrir flashcards tab):
const reviewsPendentes = await reviewService.obterParaReviewHoje();
console.log('[ReviewService]', 'Reviews para hoje:', reviewsPendentes);
*/
