/**
 * QuizService - Sistema completo de quizzes com validação e XP
 */

class QuizService {
  constructor() {
    this.storageKey = 'it_quiz_historico';
    
    // Dados iniciais de exemplo (vazio no localStorage inicialmente)
    this.quizData = [];
    this.loadPromise = null;
  }

  /**
   * Carrega quizzes.json ou usa dados inline se não existir
   */
  async carregarQuizzes() {
    if (this.loadPromise) return this.loadPromise;

    try {
      const response = await fetch('data/quizzes.json');
      
      if (!response.ok) {
        // JSON não existe - usar dados inline
        console.warn('[QuizService] quizzes.json não encontrado, usando inline data');
        
        this.quizData = [
          { categoria: 'saudacoes', questoes: this._dadosSaudacoes() },
          { categoria: 'numeros', questoes: this._dadosNumeros() },
          { categoria: 'verbos', questoes: this._dadosVerbos() },
          { categoria: 'familia', questoes: this._dadosFamilia() }
        ];
        
        // Persistir para não recarregar a cada refresh
        localStorage.setItem(this.storageKey, JSON.stringify(this.quizData));
      } else {
        this.quizData = await response.json();
      }

      console.log(`[QuizService] Carregou ${this.quizData.length} categorias de quiz`);
    } catch (error) {
      console.error('[QuizService]', 'Falha ao carregar quizzes:', error.message);
      this.quizData = []; // Fallback vazio
    }

    this.loadPromise = null;
  }

  /**
   * Gera N questões aleatorias de uma categoria
   */
  async gerarQuestoes(categoria, n = 5) {
    await this.carregarQuizzes();

    const categoriaObj = this.quizData.find(c => c.categoria === categoria);
    if (!categoriaObj || !categoriaObj.questoes) {
      console.error(`[QuizService] Categoria ${categoria} não possui questoes`);
      return [];
    }

    // Retornar N questões aleatorias
    const shuffled = [...categoriaObj.questoes].sort(() => 0.5 - Math.random());
    return shuffled.slice(0, n);
  }

  /**
   * Valida resposta de quiz e calcula XP
   */
  validarResposta(questao, respostaUsuario) {
    const correta = questao.respostaCorreta === respostaUsuario;
    
    const xpGanho = {
      correta: 10,
      incorreta: 0
    }[correta];

    return {
      correta,
      xpGanho,
      questaoTexto: questao.italiano,
      questaoPt: questao.ptbr || '',
      respostaCorreta: questao.respostaCorreta,
      usuarioRespondeu: respostaUsuario
    };
  }

  /**
   * Salva resultado do quiz no localStorage
   */
  salvarResultadoQuiz(resultado) {
    const session = {
      timestamp: Date.now(),
      categoria: resultado.categoria,
      numeroQuestoes: resultado.questoes.length,
      corretas: resultado.corretas,
      incorretas: resultado.incorretas,
      percentualAcerto: ((resultado.corretas / resultado.questoes.length) * 100).toFixed(1),
      xpGanhoTotal: resultado.xpGanhoTotal
    };

    const historico = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    historico.push(session);
    
    // Limpar histórico antigo (manter últimos 50)
    if (historico.length > 50) {
      historico.splice(0, historico.length - 50);
    }

    localStorage.setItem(this.storageKey, JSON.stringify(historico));
    console.log(`[QuizService] Salvou quiz: ${session.percentualAcerto}% (${session.corretas}/${session.numeroQuestoes})`);
    
    return session;
  }

  /**
   * Retorna histórico de quizzes (últimos N)
   */
  async obterHistorico(n = 5) {
    await this.carregarQuizzes();
    const historico = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
    return historico.slice(-n); // Últimos N
  }

  /**
   * Dados inline para fallback (vazio ou exemplo)
   */
  _dadosSaudacoes() {
    return [
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
      }
    ];
  }

  _dadosNumeros() {
    return [
      {
        id: 'q_n_01',
        italiano: 'Uno',
        ptbr: 'Um',
        respostaCorreta: 'uno',
        distratores: ['due', 'tre', 'quattro'],
        dica: 'Número 1'
      },
      {
        id: 'q_n_02',
        italiano: 'Due',
        ptbr: 'Dois',
        respostaCorreta: 'due',
        distratores: ['uno', 'tre', 'cinque'],
        dica: 'Número 2'
      }
    ];
  }

  _dadosVerbos() {
    return [
      {
        id: 'q_v_01',
        italiano: 'Andare',
        ptbr: 'Ir (eu vado, tu vai, lui va)',
        respostaCorreta: 'andare',
        distratores: ['mangiare', 'parlare', 'dormire'],
        dica: 'Verbo irregular de movimento'
      },
      {
        id: 'q_v_02',
        italiano: 'Mangiare',
        ptbr: 'Comer (eu mangio, tu mangi)',
        respostaCorreta: 'mangiare',
        distratores: ['bere', 'dormire', 'parlare'],
        dica: 'Verbo regular de 1ª conjugação'
      }
    ];
  }

  _dadosFamilia() {
    return [
      {
        id: 'q_f_01',
        italiano: 'Mamma',
        ptbr: 'Mãe',
        respostaCorreta: 'mamma',
        distratores: ['papà', 'nonna', 'zia'],
        dica: 'Pai de família'
      },
      {
        id: 'q_f_02',
        italiano: 'Papà',
        ptbr: 'Pai',
        respostaCorreta: 'papà',
        distratores: ['mamma', 'nonno', 'fratello'],
        dica: 'Marido da família'
      }
    ];
  }

  /**
   * Exemplo de uso em main.js:
   * 
   * const quizService = new QuizService();
   * const categoria = 'saudacoes';
   * const questoes = await quizService.gerarQuestoes(categoria, 5);
   * App.renderizarQuiz(questoes);
   */
}
