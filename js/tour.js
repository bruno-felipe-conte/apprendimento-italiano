// ============================================================
// tour.js — Walkthrough interativo via Driver.js
// Sempre em Português — iniciantes precisam entender o app
//
// FIX: usa onNextClick/onPrevClick para navegar a seção ANTES
// do Driver.js posicionar o overlay, garantindo que o elemento
// alvo esteja visível quando o highlight for calculado.
// ============================================================

const Tour = {
  STORAGE_KEY: 'it_tour_done',

  reiniciar() {
    try { localStorage.removeItem(this.STORAGE_KEY); } catch(e) {}
    this.iniciar(true);
  },

  iniciar(forcar = false) {
    if (!window.driver || !window.driver.js) return;
    try {
      if (!forcar && localStorage.getItem(this.STORAGE_KEY)) return;
    } catch(e) {}

    const drv = window.driver.js.driver;

    // Seção e preparação necessária para cada passo (indexed)
    const passos = [
      // 0 — header
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 1 — stats bar
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 2 — templos grid
      { sec: 'templi',    prep: null },
      // 3 — meta prazo
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 4 — flashcard selector
      { sec: 'flashcard', prep: null },
      // 5 — modos de estudo
      { sec: 'flashcard', prep: null },
      // 6 — botões avaliação
      { sec: 'flashcard', prep: () => {
          const a = document.getElementById('card-actions');
          if (a) a.style.display = 'grid';
      }},
      // 7 — quiz
      { sec: 'quiz',       prep: null },
      // 8 — gramática
      { sec: 'grammatica', prep: null },
      // 9 — vocabulário
      { sec: 'vocabolario', prep: null },
    ];

    // Seletores de cada step — usados para scrollIntoView antes do Driver posicionar
    const stepSelectors = [
      '.app-header',
      '.stats-bar',
      '#templos-grid',
      '#meta-prazo-container',
      '.card-selecao-templo',
      '#btn-reverso',
      '.card-actions',
      '#quiz-templo-selector',
      '#grammatica-container',
      '#vocab-search',
    ];

    const navegar = (idx, cb) => {
      const p = passos[idx];
      if (!p) { cb(); return; }
      App.navegar(p.sec);
      if (p.prep) p.prep();
      // Aguarda seção renderizar, depois scrolla o elemento-alvo para o centro
      // visível ANTES do Driver calcular a posição do overlay
      setTimeout(() => {
        const sel = stepSelectors[idx];
        if (sel) {
          const el = document.querySelector(sel);
          if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
        }
        // Pequena pausa extra para o scroll terminar
        setTimeout(cb, 60);
      }, 100);
    };

    let driverObj;

    driverObj = drv({
      showProgress: true,
      animate:      true,
      allowClose:   true,
      nextBtnText:  'Próximo →',
      prevBtnText:  '← Voltar',
      doneBtnText:  '🎉 Começar!',
      progressText: '{{current}} de {{total}}',
      popoverClass: 'app-tour-theme',

      // Intercepta "próximo" — navega primeiro, depois move
      onNextClick: () => {
        const cur = driverObj.getActiveIndex() ?? 0;
        navegar(cur + 1, () => driverObj.moveNext());
      },

      // Intercepta "anterior" — navega primeiro, depois move
      onPrevClick: () => {
        const cur = driverObj.getActiveIndex() ?? 0;
        navegar(cur - 1, () => driverObj.movePrevious());
      },

      onDestroyStarted: () => {
        if (!driverObj.hasNextStep() || confirm('Deseja sair do tour?')) {
          driverObj.destroy();
          try { localStorage.setItem(Tour.STORAGE_KEY, '1'); } catch(e) {}
        }
      },

      steps: [
        {
          element: '.app-header',
          popover: {
            title: '👋 Bem-vindo ao Italiano Autentico!',
            description: 'Este tour de 10 passos apresenta as principais funções do app. Leva menos de 2 minutos — vamos lá!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.stats-bar',
          popover: {
            title: '🏅 Nível, XP e Sequência',
            description: 'Aqui você acompanha seu progresso. Cada atividade rende XP. Ao atingir XP suficiente, seu nível sobe e novos templos são desbloqueados. A barra dourada mostra o quanto falta para o próximo nível.',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#templos-grid',
          popover: {
            title: '🏛️ Templos — Seu Mapa de Aprendizado',
            description: 'Cada templo é um pacote de vocabulário de uma cidade italiana. Comece pelo Templo 1 (Roma). Os demais se desbloqueiam conforme você evolui de nível.',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#meta-prazo-container',
          popover: {
            title: '🎯 Defina uma Meta com Prazo',
            description: 'Escolha um nível alvo e uma data limite. O app calcula quantos XP por dia você precisa para chegar lá a tempo — seu GPS de aprendizado!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.card-selecao-templo',
          popover: {
            title: '🃏 Flashcards com Repetição Espaçada',
            description: 'Selecione um templo e estude as palavras. O algoritmo FSRS-4.5 decide quando cada palavra precisa ser revisada — você vê a carta exatamente quando está prestes a esquecer.',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#btn-reverso',
          popover: {
            title: '🔄 Três Modos de Estudo',
            description: '🔄 Reverso (PT→IT) · 📖 Contexto (complete a frase) · 🎧 Escuta (adivinhe pelo áudio). Use os três modos para domínio completo!',
            side: 'bottom', align: 'start'
          }
        },
        {
          element: '.card-actions',
          popover: {
            title: '⭐ Como Avaliar as Cartas',
            description: '❌ Esqueci → revisão amanhã · ⚡ Difícil → 1 dia · ✅ Bom → 3 dias · ⭐ Fácil → 2 semanas. Seja honesto — o sistema aprende com você!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#quiz-templo-selector',
          popover: {
            title: '❓ Quiz — 4 Tipos de Exercício',
            description: 'Vocabulário · Morfologia (gênero & plural) · Listening (reconheça pelo áudio) · Conjugação verbal. Cada acerto rende XP!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#grammatica-container',
          popover: {
            title: '📚 Gramática — Do A1 ao C2',
            description: '82 lições em 6 níveis. Cada lição tem explicação + exercícios interativos. Ative o Modo Imersão 🇮🇹 para ver tudo em italiano!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#vocab-search',
          popover: {
            title: '📖 Vocabulário — Seu Glossário Completo',
            description: 'Pesquise qualquer palavra. Filtre por dificuldade, favoritos ou templo. Clique para ouvir a pronúncia. Use "Ocultar PT/IT" para testar a memória!',
            side: 'bottom', align: 'center'
          }
        },
      ]
    });

    // Navega ao passo inicial antes de iniciar o Driver
    navegar(0, () => driverObj.drive());
  }
};
