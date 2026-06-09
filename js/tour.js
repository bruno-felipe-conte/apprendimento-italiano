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
      // 2 — templo 1 (só o primeiro card)
      { sec: 'templi',    prep: null },
      // 3 — meta prazo
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 4 — flashcard selector
      { sec: 'flashcard', prep: null },
      // 5 — três modos de estudo (wrapper)
      { sec: 'flashcard', prep: null },
      // 6 — botões avaliação
      { sec: 'flashcard', prep: () => {
          const a = document.getElementById('card-actions');
          if (a) a.style.display = 'grid';
      }},
      // 7 — quiz → botão Le Fondamenta
      { sec: 'quiz', prep: () => {
          if (typeof Quiz !== 'undefined') Quiz.renderizarSeletor();
      }},
      // 8 — gramática → banner A1
      { sec: 'grammatica', prep: () => {
          if (typeof Grammatica !== 'undefined') Grammatica.renderizarSeletor();
      }},
      // 9 — vocabulário → botões Ocultar PT/IT
      { sec: 'vocabolario', prep: () => {
          if (typeof Vocab !== 'undefined') Vocab.renderizar();
      }},
      // 10 — storie
      { sec: 'storie', prep: null },
      // 11 — dialoghi
      { sec: 'dialoghi', prep: null },
      // 12 — canzoni
      { sec: 'canzoni', prep: null },
    ];

    // Seletores de cada step — usados para scrollIntoView antes do Driver posicionar
    const stepSelectors = [
      '.app-header',
      '.stats-bar',
      '#templos-grid .templo-card:first-child',   // só o Templo 1
      '#meta-prazo-container',
      '.card-selecao-templo',
      '#btn-modos-wrapper',                         // todos os 3 botões de modo
      '.card-actions',
      '.quiz-templo-btn:not(.bloqueado)',           // Le Fondamenta
      '.gram-nivel-banner',                         // bloco A1
      '#vocab-blur-btns',                           // Ocultar PT / Ocultar IT
      '#storie-lista',                              // lista de histórias
      '.dialogo-card',                              // card de diálogo
      '.canzone-card',                              // card de canção
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
            description: 'Este tour de 13 passos apresenta as principais funções do app. Leva menos de 2 minutos — vamos lá!',
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
          element: '#templos-grid .templo-card:first-child',
          popover: {
            title: '🏛️ Templo 1 — Por Aqui Você Começa!',
            description: 'Cada templo é um pacote de vocabulário de uma cidade italiana. Comece aqui, pelo Templo 1 (Roma). Os demais se desbloqueiam conforme você evolui de nível.',
            side: 'bottom', align: 'center'
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
          element: '#btn-modos-wrapper',
          popover: {
            title: '🔄 Três Modos de Estudo',
            description: '🔄 Reverso (PT→IT) · 📖 Contexto (complete a frase) · 🎧 Escuta (adivinhe pelo áudio). Use os três modos para domínio completo!',
            side: 'bottom', align: 'center'
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
          element: '.quiz-templo-btn:not(.bloqueado)',
          popover: {
            title: '❓ Quiz — 4 Tipos de Exercício',
            description: 'Comece pelo Templo 1. Vocabulário · Morfologia (gênero & plural) · Listening (reconheça pelo áudio) · Conjugação verbal. Cada acerto rende XP!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '.gram-nivel-banner',
          popover: {
            title: '📚 Gramática — Do A1 ao C2',
            description: '82 lições em 6 níveis. Clique no banner do nível para expandir ou recolher as lições. Ative o Modo Imersão 🇮🇹 para ver tudo em italiano!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#vocab-blur-btns',
          popover: {
            title: '📖 Vocabulário — Treine a Memória',
            description: 'Use "Ocultar PT" ou "Ocultar IT" para esconder uma coluna e testar se você lembra a tradução. Pesquise, filtre por templo ou favoritos e clique para ouvir a pronúncia!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#storie-lista',
          popover: {
            title: '📖 Storie — Leitura Autêntica',
            description: 'Leia textos italianos reais com dificuldade A1–C2. Ative o Modo Imersão para esconder a tradução e testar sua compreensão!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.dialogo-card',
          popover: {
            title: '💬 Dialoghi — Conversação Real',
            description: 'Pratique diálogos do cotidiano italiano. Ouça, leia e repita — ideal para treinar ouvido e fala!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.canzone-card',
          popover: {
            title: '🎵 Canzoni — Aprenda com Música',
            description: '200 músicas italianas com letra completa. Ouça e acompanhe a letra — aprender italiano nunca foi tão divertido!',
            side: 'bottom', align: 'center'
          }
        },
      ]
    });

    // Navega ao passo inicial antes de iniciar o Driver
    navegar(0, () => driverObj.drive());
  }
};
