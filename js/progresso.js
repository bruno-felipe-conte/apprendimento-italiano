/**
 * Progressao - Sistema completo de progressão (XP, levels, streaks) + SM-2 integration
 */

class App {
  constructor() {
    this.progresso = null; // Singleton no localStorage
    this.vocabularyDB = new Map(); // Mapa palavras por ID
    
    // Tabs
    this.tabsNavigation = ['home', 'flashcards', 'quiz', 'vocabolario', 'templi'];
    this.activeTab = 'home';
    
    // Heatmap (Calor) - stats para rendering no tab "Templi"
    this.it_diario = {}; // {"2026-05-15": 14}
    this.it_quiz_historico = []; // Array de sessões quiz
    
    // System de reviews SM-2
    this.reviewsQueue = [];
    this.reviewService = null; // ReviewService singleton
  }

  /**
   * Inicializa app e carrega progressão do localStorage
   */
  async initialize() {
    console.log('[App] Inicializando Italian Learning App...');

    // Criar singleton de review service
    this.reviewService = new (window.ReviewService)();

    // Carregar dados
    await this.carregarProgressao(); // XP, levels, etc.
    await this.carregarHeatmapDiario(); // Stats para heatmap
    await this.carregarVocabulario(); // Vocabulario service

    // Inicializar streak (se primeiro acesso hoje)
    if (!this.progresso.streak || new Date().toDateString() !== this.progresso.streak_lastDate?.toLocaleDateString()) {
      this.resetarStreakHoje();
    }

    console.log('[App] Inicializado. Streak atual:', this.progresso.streak, 'Level:', this.progresso.nivel);
  }

  /**
   * Carrega progressão do localStorage (XP, levels, desbloqueados)
   */
  async carregarProgressao() {
    const progressoRaw = localStorage.getItem('templo_progresso');
    
    if (!progressoRaw) {
      // Primeiro acesso - criar novo user
      this.progresso = {
        xp: 0,
        nivel: 1,
        streak: 0,
        streak_lastDate: null,
        templos_desbloqueados: ['t1'], // Templo I desbloqueado por padrão
        vocabulario_desbloqueado: [], // Lista de IDs
        frase_desbloqueada: '',
        review_queue: [], // Cards para SM-2
      };
      this.salvarProgressao();
    } else {
      try {
        this.progresso = JSON.parse(progressoRaw);
        
        // Mapeamento legacy keys (compatibilidade)
        if (typeof this.progresso.streak !== 'number') {
          const streakRaw = localStorage.getItem('streak_count');
          if (streakRaw) {
            this.progresso.streak = parseInt(streakRaw, 10);
          }
        }

        console.log('[Progressao] Carregado: XP', this.progresso.xp, '| Level', this.progresso.nivel, '| Streak', this.progresso.streak);
      } catch (e) {
        console.error('[Progressao]', 'Falha ao carregar:', e.message);
        this.resetarProgressao();
      }
    }

    // Atualizar UI de XP bar
    if (typeof this.updateXpBar === 'function') {
      this.updateXpBar();
    }
  }

  /**
   * Salva progressão no localStorage
   */
  salvarProgressao() {
    try {
      localStorage.setItem('templo_progresso', JSON.stringify(this.progresso));
      console.log(`[Progressao] Salvado: XP ${this.progresso.xp} | Level ${this.progresso.nivel}`);
    } catch (e) {
      if (/Quota/.test(e.name)) {
        console.warn('[Progressao]', 'localStorage full. Limpe cache ou use IndexedDB.');
      } else {
        console.error('[Progressao]', 'Erro ao salvar:', e.message);
      }
    }
  }

  /**
   * Resetar progressão (útil para test/nuovo utente)
   */
  resetarProgressao() {
    localStorage.removeItem('templo_progresso');
    this.progresso = {
      xp: 0,
      nivel: 1,
      streak: 0,
      streak_lastDate: null,
      templos_desbloqueados: ['t1'],
      vocabulario_desbloqueado: [],
      frase_desbloqueada: '',
      review_queue: []
    };
    console.log('[Progressao]', 'Resetado para novo usuário');
  }

  /**
   * Resetar streak (novo dia ou manual)
   */
  resetarStreakHoje() {
    const hoje = new Date().toLocaleDateString();
    if (!this.progresso.streak_lastDate || this.progresso.streak_lastDate !== hoje) {
      this.progresso.streak = 1;
      this.progresso.streak_lastDate = hoje;
      this.salvarProgressao();
      console.log(`[Progressao] Streak resetado para 1 (hoje: ${hoje})`);
    }
  }

  /**
   * Adiciona XP + ganha level se necessario
   */
  addXp(xpGanho) {
    this.progresso.xp += xpGanho;
    
    // Calcular novo nivel baseado em thresholds de XP (simples)
    const newLevel = Math.floor(this.progresso.xp / 100) + 1;
    
    if (newLevel > this.progresso.nivel) {
      console.log(`[Progressao] Level UP! Nível ${this.progresso.nivel} → ${newLevel}`);
      this.progresso.nivel = newLevel;
      
      // Adicionar bonus streak por level up
      this.progresso.streak += 1;
    }

    // Teto de XP por level (simples)
    const maxXP = Math.pow(10, this.progresso.nivel - 1) * 100; // Level 1: 100, Level 2: 1000, etc.
    if (this.progresso.xp > maxXP) {
      console.warn(`[Progressao] XP atingiu teto do nivel ${newLevel} (${maxXP}). Resetando para ${maxXP}`);
      this.progresso.xp = maxXP;
    }

    this.salvarProgressao();
  }

  /**
   * Gain level - bonus streak por novo level
   */
  ganharLevel() {
    console.log(`[Progressao] Level UP! 🎉 Nível ${this.progresso.nivel} → ${this.progresso.nivel + 1}`);
    this.progresso.streak += 1; // Bonus de 1 dia por level up
    this.salvarProgressao();
  }

  /**
   * Carrega stats do heatmap (Calor) - para tab "Templi"
   */
  async carregarHeatmapDiario() {
    const heatmapKey = 'it_diario';
    
    // Se it_diario não existe no localStorage, usar empty object
    if (!this.it_diario || Object.keys(this.it_diario).length === 0) {
      try {
        const raw = localStorage.getItem(heatmapKey);
        this.it_diario = raw ? JSON.parse(raw) : {};
        
        // Se localStorage vazio e item existia antes, usar fallback
        if (Object.keys(this.it_diario).length === 0 && typeof localStorage !== 'undefined') {
          const legacyHeatmap = localStorage.getItem('it_progresso');
          if (legacyHeatmap) {
            console.warn('[Heatmap]', 'Encontrado it_progresso legacy, migrando...');
            this.it_diario = JSON.parse(legacyHeatmap);
            localStorage.setItem(heatmapKey, JSON.stringify(this.it_diario));
            localStorage.removeItem('it_progresso');
          }
        }
      } catch (e) {
        console.error('[Heatmap]', 'Falha ao carregar:', e.message);
      }
    }

    // Se it_quiz_historico não existe, usar empty array
    if (!this.it_quiz_historico || !Array.isArray(this.it_quiz_historico)) {
      try {
        const raw = localStorage.getItem('it_quiz_historico');
        this.it_quiz_historico = raw ? JSON.parse(raw) : [];
      } catch (e) {
        console.error('[Heatmap]', 'Falha ao carregar it_quiz_historico:', e.message);
      }
    }

    // Se reviewsQueue não existe, migrar do review service (se existir)
    if (!this.progresso.review_queue || !Array.isArray(this.progresso.review_queue)) {
      try {
        const reviewsRaw = localStorage.getItem('it_reviews');
        if (reviewsRaw) {
          this.progresso.review_queue = JSON.parse(reviewsRaw);
          console.log('[Heatmap]', 'Migrou review queue de it_reviews para templo_progresso.review_queue');
        }
      } catch (e) {
        console.error('[Heatmap]', 'Falha ao carregar reviews:', e.message);
      }
    }

    console.log(`[Heatmap] Carregado: ${Object.keys(this.it_diario).length} dias registrados`);
  }

  /**
   * Salva stats do heatmap (Calor)
   */
  salvarHeatmap(stats = {}) {
    this.it_diario = { ...this.it_diario, ...stats };
    localStorage.setItem('it_diario', JSON.stringify(this.it_diario));
    
    console.log(`[Heatmap] Salvou stats: ${JSON.stringify(stats)}`);
  }

  /**
   * Adiciona ponto ao heatmap (ex: após sessão de flashcards)
   */
  adicionarPontoHeatmap() {
    const hoje = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    
    if (!this.it_diario[hoje]) {
      this.it_diario[hojee] = 1; // Primeiro ponto do dia
    } else {
      this.it_diario[hojee]++; // Segundo ponto (ex: flashcards + quiz)
    }

    this.salvarHeatmap(this.it_diario);
    console.log(`[Heatmap] Adicionado ponto para ${hoje}. Total do dia: ${this.it_diario[hoje]}`);
  }

  /**
   * Renderiza grid de vocabulário (FIX: agora carrega palavras reais)
   */
  renderizarGridVocabulario(n = 5, categoria = null) {
    const container = document.getElementById('vocabolo-grid');
    if (!container) return;

    // Carregar dados asyncamente
    this.vocabularyService.carregarJSON()
      .then(palavras => {
        // Filtrar por categoria se fornecido
        let filtrado = [...palavras];
        if (categoria) {
          filtrado = filtrado.filter(p => p.categoria === categoria);
          if (filtrado.length === 0) filtrado = palavras; // Fallback para todas
        }

        // Obter N aleatórios ou todas
        let selecionadas = [...filtrado];
        if (n && selecionadas.length > n) {
          selecionadas = selecionadas.sort(() => 0.5 - Math.random()).slice(0, n);
        }

        // Renderizar grid
        container.innerHTML = `
          <div class="grid-vocabulario">
            ${selecionadas.map(palavra => this._renderCardVocabulario(palavra)).join('')}
          </div>
        `;

        // Adicionar event listeners para audio
        const cards = container.querySelectorAll('.palavra-card');
        cards.forEach(card => {
          card.addEventListener('click', () => {
            const id = card.dataset.id;
            this.tocarAudio(palavra);
          });
        });

      })
      .catch(error => {
        console.error('[VocabularyService]', 'Falha ao carregar vocabulário:', error.message);
        container.innerHTML = '<p class="error-msg">Erro ao carregar vocabulário. Verifique o console.</p>';
      });
  }

  /**
   * Renderiza um card individual (usado no grid e em reviews)
   */
  _renderCardVocabulario(palavra) {
    return `
      <div class="palavra-card" data-id="${palavra.id}" onclick="window.app.tocarAudio('${palavra.italiano}')">
        <span class="it">${palavra.italiano}</span>
        <span class="pt">${palavra.portugues}</span>
        ${palavra.audio_ipa ? `<small>${palavra.audio_ipa}</small>` : ''}
        ${palavra.genero ? `<span class="categoria-label">${palavra.genero}</span>` : ''}
      </div>
    `;
  }

  /**
   * Toca áudio da palavra (Web Speech API)
   */
  tocarAudio(texto) {
    const speech = new SpeechSynthesisUtterance(texto);
    speech.lang = 'it-IT'; // Italiano
    speech.rate = 0.9; // Um pouco mais lento para learners
    
    // Tentar usar voz italiana se disponível
    const voices = window.speechSynthesis.getVoices();
    const italianVoice = voices.find(v => v.lang.includes('it'));
    if (italianVoice) speech.voice = italianVoice;

    window.speechSynthesis.speak(speech);
  }

  /**
   * Renderiza reviews pendentes (flashcards para hoje)
   */
  renderizarReviewsPendentes() {
    const container = document.getElementById('reviews-container');
    if (!container) return;

    // Obter reviews para review hoje + pending cards do queue
    this.reviewService.obterParaReviewHoje()
      .then(reviews => {
        if (reviews.length === 0) {
          container.innerHTML = '<p class="empty-state">Nenhum review pendente hoje. Bom trabalho! 🎉</p>';
          return;
        }

        // Renderizar cards para review
        container.innerHTML = `
          <div class="review-header">
            <h3>Reviews Pendentes (${reviews.length})</h3>
            <button onclick="window.app.verificarReviewAtrasada()" class="btn btn-warning">Verificar atrasos</button>
          </div>
          <div id="reviews-grid" class="grid-reviews">
            ${reviews.map(r => this._renderCardReview(r)).join('')}
          </div>
        `;

        // Adicionar listeners de review (acerto/repetir)
        const cards = container.querySelectorAll('.review-card');
        cards.forEach(card => {
          card.addEventListener('click', event => {
            const cardId = card.dataset.cardId;
            this.verificarReview(cardId, event.target);
          });
        });
      })
      .catch(error => {
        console.error('[ReviewService]', 'Falha ao carregar reviews:', error.message);
        container.innerHTML = '<p class="error-msg">Erro ao carregar reviews pendentes.</p>';
      });
  }

  /**
   * Renderiza card individual para review
   */
  _renderCardReview(review) {
    const { italiano, portugues, dificuldade } = review;
    return `
      <div class="review-card" data-cardid="${review.cardId}">
        <span class="word">${italiano}</span>
        <button onclick="event.stopPropagation(); window.app.verificarReview('${review.cardId}', event.target)" 
          class="btn ${dificuldade === 'facil' ? 'success' : dificuldade === 'medio' ? 'primary' : 'danger'}" 
          ${dificuldade === 'facil' ? '' : difficulty === 'medio' ? 'medium' : 'hard'}">
          ${dificuldade}
        </button>
      </div>
    `;
  }

  /**
   * Verifica review (acerto/repetir) e atualiza SM-2 schedule
   */
  async verificarReview(cardId, btnElemento) {
    const review = this.reviewService.processarReview(cardId);
    
    if (!review) {
      console.warn('[Review]', `Card ${cardId} não encontrado`);
      return;
    }

    // Salvar ponto ao heatmap (após revisão)
    this.adicionarPontoHeatmap();

    // Atualizar UI com feedback
    const card = document.querySelector(`[data-cardid="${cardId}"]`);
    if (card && btnElemento) {
      const label = btnElemento.textContent;
      
      // Mostrar animação de sucesso (simples)
      if (label === 'facil') {
        card.classList.add('success-anim');
      } else if (label === 'medium') {
        card.classList.add('warning-anim');
      } else if (label === 'hard') {
        card.classList.add('danger-anim');
      }

      // Remover do DOM após animação (opcional - ou mantê-lo visível)
      setTimeout(() => {
        card.style.opacity = '0.3';
        setTimeout(() => card.remove(), 300);
      }, 150);
    }

    console.log(`[Review] Processou ${cardId} como: ${btnElemento.textContent}`);
    
    // Re-renderizar queue se necessario (opcional - pode manter em memoria)
    this.renderizarReviewsPendentes();
  }

  /**
   * Verifica reviews atrasadas (bônus/streak)
   */
  verificarReviewAtrasada() {
    console.log('[Review]', 'Verificando reviews atrasadas...');
    
    const hoje = Date.now();
    const reviews = this.reviewService.reviewQueue;
    
    const atrasadas = reviews.filter(r => {
      if (r.status === 'reviewed') return false;
      return r.nextReview < hoje; // Passou da data
    });

    console.log(`[Review] Found ${atrasadas.length} reviews atrasadas`);

    // Bônus por revisar review atrasada (streak +1)
    atrasadas.forEach(r => {
      console.log(`[Review] Review atrasada: ${r.italiano} - adicionando bônus streak`);
      this.progresso.streak += 1; // Bónus de 1 dia por review atrasada revisada
    });

    this.salvarProgressao();
    
    // Re-renderizar reviews pendentes
    this.renderizarReviewsPendentes();
  }

  /**
   * Carrega vocabulário (inicialização)
   */
  async carregarVocabulario() {
    await this.vocabularyService.carregarJSON();
    
    // Persistir ao localStorage por padrão (MVP behavior)
    try {
      this.vocabularyService.persistirPalavras(this.vocabularyService.defaultData);
    } catch (e) {
      console.warn('[Vocabulary]', 'Falha ao persistir vocabulário:', e.message);
    }

    console.log(`[Vocabulary] Carregou ${this.vocabularyService.defaultData.length} palavras`);
  }

  /**
   * Exemplo de uso: renderizar flashcards para hoje (ReviewsPendentes)
   */
  async montarFlashcards() {
    await this.carregarVocabulario(); // Lazy load vocabulario
    
    const pending = await this.reviewService.obterParaReviewHoje();
    
    if (pending.length === 0) {
      console.log('[App]', 'Nenhum flashcard pendente para hoje');
      return [];
    }

    const cardsContainer = document.getElementById('flashcards-container');
    if (!cardsContainer) return pending;

    cardsContainer.innerHTML = `
      <div class="flashcards-header">
        <h3>Flashcards Pendentes</h3>
        <button onclick="window.app.renderizarReviewsPendentes()" class="btn btn-secondary">Carregar Pendentes</button>
      </div>
      <div id="reviews-grid"></div>
    `;

    this.renderizarReviewsPendentes();
    return pending;
  }

  /**
   * Renderiza quiz interface (carrega questions + valida respostas)
   */
  async renderizarQuiz(categoria = 'saudacoes', n = 5) {
    const container = document.getElementById('quiz-container');
    if (!container) return;

    // Gerar N questões da categoria
    await this.quizService.carregarQuizzes();
    
    try {
      const questoes = await this.quizService.gerarQuestoes(categoria, n);
      
      if (questoes.length === 0) {
        container.innerHTML = '<p class="error-msg">Nenhuma questão encontrada.</p>';
        return;
      }

      // Renderizar quiz interface
      container.innerHTML = this._renderizarQuizInterface(questoes);

      // Adicionar listeners de resposta
      const botaoResponder = container.querySelector('.btn-responder');
      if (botaoResponder) {
        botaoResponder.addEventListener('click', () => {
          this.submeterRespostaQuiz();
        });
      }
    } catch (e) {
      console.error('[QuizService]', 'Erro ao gerar quiz:', e.message);
      container.innerHTML = '<p class="error-msg">Erro ao carregar questões. Verifique o console.</p>';
    }
  }

  /**
   * Renderiza interface do quiz
   */
  _renderizarQuizInterface(questoes) {
    return `
      <div class="quiz-header">
        <h3>${questoes.length} Questões</h3>
        <button onclick="window.app.sairQuiz()" class="btn btn-secondary">Cancelar</button>
      </div>
      <div id="quiz-questions"></div>
      <button id="quiz-responder" class="btn btn-primary responder">Responder</button>
    `;
  }

  /**
   * Renderiza questões do quiz
   */
  _renderizarQuestoes(questoes) {
    const container = document.getElementById('quiz-questions');
    if (!container) return;

    container.innerHTML = questoes.map((q, index) => `
      <div class="quiz-item">
        <div class="quiz-question">${index + 1}. ${q.italiano}</div>
        <input type="text" class="quiz-input" placeholder="Digite sua resposta" autocomplete="off">
        <span class="quiz-dica">${q.dica || ''}</span>
      </div>
    `).join('');

    // Adicionar listeners para inputs
    const inputs = container.querySelectorAll('.quiz-input');
    inputs.forEach(input => {
      input.addEventListener('keydown', event => {
        if (event.key === 'Enter') {
          this.submeterRespostaQuiz();
        }
      });
    });
  }

  /**
   * Submete respostas do quiz e calcula XP
   */
  async submeterRespostaQuiz() {
    const inputs = document.querySelectorAll('.quiz-input');
    
    // Validar que todos tenham resposta
    inputs.forEach((input, index) => {
      if (!input.value.trim()) {
        alert(`Questão ${index + 1}: Responda antes de enviar!`);
        throw new Error('Resposta incompleta');
      }
    });

    // Gerar resultado
    const questoes = document.querySelectorAll('.quiz-question');
    const questoesTexto = Array.from(questoes).map(q => q.textContent.replace(/^\d+\. /, ''));
    
    // Obter categorias disponíveis
    await this.quizService.carregarQuizzes();
    const todasQuestoes = [];
    this.quizService.quizData.forEach(categoria => {
      if (categoria.questoes) todasQuestoes.push(...categoria.questoes);
    });

    // Validar respostas e calcular XP
    let corretas = 0;
    let incorretas = 0;
    let xpGanhoTotal = 0;

    questoesTexto.forEach((qTexto, index) => {
      const input = inputs[index];
      const respostaUsuario = input.value.trim().toLowerCase();
      
      // Encontrar questão correspondente
      const questao = todasQuestoes.find(q => 
        q.italiano.toLowerCase() === qTexto.toLowerCase()
      );

      if (!questao) {
        console.warn('[Quiz]', 'Questão não encontrada:', qTexto);
        return;
      }

      const validacao = this.quizService.validarResposta(questao, respostaUsuario);
      
      if (validacao.correta) {
        corretas++;
        xpGanhoTotal += 10;
      } else {
        incorretas++;
      }
    });

    // Salvar resultado + XP
    const resultado = {
      categoria: 'mixed', // Quiz misturado por default
      questoes: todasQuestoes,
      corretas,
      incorretas,
      percentualAcerto: ((corretas / todasQuestoes.length) * 100).toFixed(1),
      xpGanhoTotal
    };

    this.quizService.salvarResultadoQuiz(resultado);
    
    // Adicionar XP ao progressão + bônus por quiz completo
    this.addXp(xpGanhoTotal + (todosQuestoes.length > 3 ? 20 : 0)); // Bônus de completar quiz
    
    // Renderizar feedback
    const container = document.getElementById('quiz-container');
    if (!container) return;

    container.innerHTML = `
      <div class="quiz-resultado">
        <h3>Quiz Completo!</h3>
        <p>Corretas: ${corretas} / ${todosQuestoes.length}</p>
        <p>Erros: ${incorretas}</p>
        <p>${resultado.percentualAcerto}% de acerto</p>
        <p class="xp-ganho">XP Ganho: ${xpGanhoTotal + (todosQuestoes.length > 3 ? 20 : 0)} (+${ xpGanhoTotal})</p>
      </div>
    `;
  }

  /**
   * Sair do quiz
   */
  sairQuiz() {
    const container = document.getElementById('quiz-container');
    if (!container) return;
    container.innerHTML = ''; // Limpar
  }

  /**
   * Renderiza vocabulário (MVP: carrega JSON ao load)
   */
  async renderizarVocabulario() {
    const container = document.getElementById('vocabolo-grid');
    if (!container) return;

    try {
      // Carregar asyncamente (lazy load como vocabulary_service)
      await this.vocabularyService.carregarJSON();
      
      // Renderizar todas as palavras
      container.innerHTML = `
        <div class="grid-vocabulario">
          ${this.vocabularyService.defaultData.slice(0, 50).map(palavra => this._renderCardVocabulario(palavra)).join('')}
        </div>
      `;

      // Adicionar listeners de audio
      const cards = container.querySelectorAll('.palavra-card');
      cards.forEach(card => {
        card.addEventListener('click', () => {
          const id = card.dataset.id;
          const palavra = this.vocabularyService.defaultData.find(p => p.id === id);
          if (palavra) {
            this.tocarAudio(palavra.italiano);
          }
        });
      });

    } catch (e) {
      console.error('[Vocabulary]', 'Falha ao carregar vocabulário:', e.message);
      container.innerHTML = '<p class="error-msg">Erro ao carregar vocabulário.</p>';
    }
  }

  /**
   * Renderiza heatmaps (Calor) no tab "Templi"
   */
  renderizarHeatmap() {
    const container = document.getElementById('calor');
    if (!container) return;

    // Heatmap simples usando divs coloridas (sem chart.js para MVP)
    container.innerHTML = `
      <div class="heatmap-container">
        <h3>Calor de Estudos</h3>
        <div class="heatmap-grid" id="heatmap-grid"></div>
        ${Object.keys(this.it_diario).length > 0 ? `
          <small>${Object.keys(this.it_diario).length} dias registrados</small>
        ` : ''}
      </div>
    `;

    // Renderizar grid de heatmaps (simplificado - 7x12 = 84 dias recentes)
    const hoje = new Date();
    const heatmapGrid = document.getElementById('heatmap-grid');
    if (!heatmapGrid) return;

    let html = '';
    for (let dia = 0; dia < 7 * 12; dia++) {
      const data = new Date(hoje);
      data.setDate(hoje.getDate() - (69 - dia)); // Começar de 69 dias atrás

      const dateStr = data.toISOString().split('T')[0]; // YYYY-MM-DD
      const count = this.it_diario[dateStr] || 0;

      // Cor baseada no count (parchment → gold → venetian red)
      let cor = 'bg-parchment';
      if (count >= 1) cor = 'bg-gold';
      if (count >= 2) cor = 'bg-venetian-red';

      html += `<div class="heatmap-cell ${cor}" data-date="${dateStr}">${count > 0 ? count : ''}</div>`;
    }

    heatmapGrid.innerHTML = html;

    // Adicionar tooltip ao passar o mouse (simples)
    const cells = heatmapGrid.querySelectorAll('.heatmap-cell');
    cells.forEach(cell => {
      cell.addEventListener('mouseenter', event => {
        const dateStr = event.target.dataset.date;
        const count = this.it_diario[dateStr] || 0;
        
        // Mostrar tooltip (simples)
        if (typeof window === 'undefined' || !window.tooltip) return;
        
        // Criar tooltip manual (sem biblioteca externa)
        const tooltip = document.createElement('div');
        tooltip.style.cssText = `
          position: absolute;
          background: rgba(0,0,0,0.8);
          color: white;
          padding: 5px 10px;
          border-radius: 4px;
          font-size: 12px;
          z-index: 1000;
          pointer-events: none;
        `;
        tooltip.textContent = `${dateStr} - ${count} sessões`;
        
        const rect = event.target.getBoundingClientRect();
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.top = `${rect.top - 30}px`;
        
        document.body.appendChild(tooltip);

        // Limpar após delay
        setTimeout(() => tooltip.remove(), 1500);
      });
    });
  }

  /**
   * Renderiza grid de templos (MVP: com palavras carregadas do JSON)
   */
  async renderizarGridTempli() {
    const container = document.getElementById('templi-grid');
    if (!container) return;

    await this.vocabularyService.carregarJSON(); // Lazy load vocabulario
    
    // Carregar progresso de cada templo (simples - só t1 por agora)
    const templos = [
      { id: 't1', nome: 'Templo I' }
    ];

    container.innerHTML = `
      <div class="templi-grid">
        ${templos.map(t => this._renderGridTemploCard(t)).join('')}
      </div>
    `;

    // Adicionar listeners de abrir templo
    const cards = container.querySelectorAll('.templo-card');
    cards.forEach(card => {
      card.addEventListener('click', event => {
        const temploId = card.dataset.id;
        
        // Mostrar modal com palavras deste templo (carregadas do JSON)
        window.app.abrirTemplo(temploId);
      });
    });
  }

  /**
   * Renderiza card individual de templo (grid)
   */
  _renderGridTemploCard(templo) {
    // Carregar progressão deste templo (simplificado - hardcoded por agora)
    const progresso = {
      xp: this.progresso.xp,
      nivel: this.progresso.nivel,
      bloqeado: !this.progresso.templos_desbloqueados.includes(templo.id),
      desbloqXp: 100 // XP necessario para desbloquear (exemplo)
    };

    return `
      <div class="templo-card ${progresso.bloqeado ? 'bloqeado' : ''}" data-id="${templo.id}">
        <div class="templo-header">
          <h4>${templo.nome}</h4>
          <span class="status-${progresso.xp === 0 ? 'pending' : 'active'}">${
            progresso.bloqeado ? 'BLOQUEADO 🔒' : 'ATIVO ✅'
          }</span>
        </div>
        
        ${!progresso.bloqeado ? `
          <div class="templo-stats">
            <div class="xp-bar-container">
              <div class="xp-bar" style="width: ${(progresso.xp / progresso.desbloqXp) * 100}%"></div>
            </div>
            <small>${progresso.xp}/${progresso.desbloqXp} XP</small>
          </div>
          
          <div class="templo-progression">
            <span>Nível ${progresso.nivel}</span>
            <span>XP: ${progresso.xp}</span>
          </div>

          <!-- Grid de palavras deste templo (renderizado dinamicamente ao abrir) -->
          <button onclick="window.app.abrirTemplo('${templo.id}')" class="btn btn-primary">
            Ver Palavras
          </button>
        ` : ''}
      </div>
    `;
  }

  /**
   * Abre modal de templo (MVP: grid de palavras deste templo)
   */
  async abrirTemplo(temploId = 't1') {
    const container = document.getElementById('templo-modal');
    if (!container || !confirm(`Abri Templo ${temploId}?`)) return;

    // Carregar palavras deste templo (simplificado - TODAS por agora)
    await this.vocabularyService.carregarJSON();
    
    const palavras = this.vocabularyService.defaultData;

    container.innerHTML = `
      <div class="modal-content">
        <h3>Templo ${temploId}</h3>
        <button onclick="window.app.fecharTemplo()" class="btn btn-secondary">Fechar</button>
        
        <div class="modal-grid">
          ${palavras.slice(0, 100).map(palavra => this._renderCardVocabulario(palavra)).join('')}
        </div>
      </div>
    `;

    // Adicionar listeners de fechar
    const btnFechar = container.querySelector('.btn-secondary');
    if (btnFechar) {
      btnFechar.addEventListener('click', () => this.fecharTemplo());
    }
  }

  /**
   * Fecha modal de templo
   */
  fecharTemplo() {
    const container = document.getElementById('templo-modal');
    if (!container) return;
    container.innerHTML = ''; // Limpar ou fechar com overlay (MVP: clear)
  }

  /**
   * Renderiza flashcards do templo (ReviewsPendentes + grid de grid)
   */
  async renderizarFlashcards() {
    await this.carregarVocabulario(); // Lazy load vocabulario
    
    const container = document.getElementById('flashcards-container');
    if (!container) return;

    // Obter reviews pendentes + todas palavras
    const pending = await this.reviewService.obterParaReviewHoje();
    
    if (pending.length > 0) {
      container.innerHTML = `
        <div class="flashcards-header">
          <h3>Flashcards Pendentes (${pending.length})</h3>
          <button onclick="window.app.renderizarReviewsPendentes()" class="btn btn-secondary">Recarregar</button>
        </div>
        <div id="reviews-grid"></div>
      `;

      this.renderizarReviewsPendentes();
    } else {
      container.innerHTML = '<p class="empty-state">Nenhum flashcard pendente hoje. Bom trabalho! 🎉</p>';
    }
  }

  /**
   * Renderiza vocabulário tab (todas palavras)
   */
  renderizarVocabularioTab() {
    this.renderizarGridVocabulario(); // MVP: carrega 50 primeiras
  }

  /**
   * Atualiza XP bar (visual)
   */
  updateXpBar() {
    const xpBar = document.querySelector('.xp-bar');
    if (!xpBar || !this.progresso) return;

    // Calcular XP% do nivel atual (simples)
    const nivelAtual = this.progresso.nivel;
    const xpAtual = this.progresso.xp;
    const maxXP = Math.pow(10, nivelAtual - 1) * 100;
    
    const percentage = (xpAtual / maxXP) * 100;

    xpBar.style.width = `${percentage}%`;
    xpBar.textContent = `${xpAtual}/${maxXP} XP`;
  }

  /**
   * Inicializa app
   */
  static async init() {
    const app = new App();
    await app.initialize();
    
    // Renderizar UI inicial (tabs + grid de templos)
    app.renderizarGridTempli();
    app.carregarHeatmapDiario(); // Stats para heatmap
    app.renderizarGridVocabulario(10, 'saudacoes'); // Exemplo: 5 primeiras palavras
    
    // Atualizar XP bar (visual)
    app.updateXpBar();

    console.log('[App]', 'Italian Learning App pronto!');
  }
}

// Inicializar ao load da página
window.onload = async () => {
  if (!window.app) window.app = new App();
  await App.init(); // Singleton global
};
