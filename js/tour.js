// ============================================================
// tour.js — Walkthrough interativo via Driver.js
// Sempre em Português — iniciantes precisam entender o app
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

    const driverObj = drv({
      showProgress: true,
      animate:      true,
      allowClose:   true,
      nextBtnText:  'Próximo →',
      prevBtnText:  '← Voltar',
      doneBtnText:  '🎉 Começar!',
      progressText: '{{current}} de {{total}}',
      popoverClass: 'app-tour-theme',
      onDestroyStarted: () => {
        if (!driverObj.hasNextStep() || confirm('Deseja sair do tour?')) {
          driverObj.destroy();
          try { localStorage.setItem(Tour.STORAGE_KEY, '1'); } catch(e) {}
        }
      },
      steps: [
        // ── 1. Boas vindas ──────────────────────────────────────
        {
          element: '.app-header',
          popover: {
            title: '👋 Bem-vindo ao Italiano Autentico!',
            description: 'Este tour de 10 passos apresenta as principais funções do app. Leva menos de 2 minutos — vamos lá!',
            side: 'bottom', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('templi'); window.scrollTo(0,0); }
        },

        // ── 2. Stats bar ────────────────────────────────────────
        {
          element: '.stats-bar',
          popover: {
            title: '🏅 Nível, XP e Sequência',
            description: 'Aqui você acompanha seu progresso. Cada atividade rende XP. Ao atingir XP suficiente, seu nível sobe e novos templos são desbloqueados. A barra dourada mostra o quanto falta para o próximo nível.',
            side: 'bottom', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('templi'); window.scrollTo(0,0); }
        },

        // ── 3. Templos ──────────────────────────────────────────
        {
          element: '#templos-grid',
          popover: {
            title: '🏛️ Templos — Seu Mapa de Aprendizado',
            description: 'Cada templo é um pacote de vocabulário temático de uma cidade italiana. Comece pelo Templo 1 (Roma). Os demais se desbloqueiam conforme você evolui de nível.',
            side: 'top', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('templi'); }
        },

        // ── 4. Meta prazo ───────────────────────────────────────
        {
          element: '#meta-prazo-container',
          popover: {
            title: '🎯 Defina uma Meta com Prazo',
            description: 'Clique aqui para escolher um nível alvo e uma data limite. O app calcula quantos XP por dia você precisa para chegar lá a tempo — seu GPS de aprendizado!',
            side: 'bottom', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('templi'); window.scrollTo(0,0); }
        },

        // ── 5. Flashcard ────────────────────────────────────────
        {
          element: '.card-selecao-templo',
          popover: {
            title: '🃏 Flashcards com Repetição Espaçada',
            description: 'Selecione um templo e estude as palavras. O algoritmo FSRS-4.5 decide quando cada palavra precisa ser revisada — você só vê uma carta no momento exato em que estaria prestes a esquecer.',
            side: 'bottom', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('flashcard'); }
        },

        // ── 6. Modos de estudo ──────────────────────────────────
        {
          element: '#btn-reverso',
          popover: {
            title: '🔄 Três Modos de Estudo',
            description: '🔄 Reverso: veja o português e diga o italiano · 📖 Contexto: complete a frase · 🎧 Escuta: ouça o áudio e adivinhe a palavra. Use os três para um aprendizado completo!',
            side: 'bottom', align: 'start'
          },
          onHighlightStarted: () => { App.navegar('flashcard'); }
        },

        // ── 7. Botões de avaliação ──────────────────────────────
        {
          element: '.card-actions',
          popover: {
            title: '⭐ Como Avaliar as Cartas',
            description: '❌ Esqueci → revisão em breve · ⚡ Difícil → 1 dia · ✅ Bom → 3 dias · ⭐ Fácil → 2 semanas. Seja honesto na avaliação — o sistema aprende com você e fica cada vez mais preciso!',
            side: 'top', align: 'center'
          },
          onHighlightStarted: () => {
            App.navegar('flashcard');
            const a = document.getElementById('card-actions');
            if (a) a.style.display = 'grid';
          }
        },

        // ── 8. Quiz ─────────────────────────────────────────────
        {
          element: '#quiz-templo-selector',
          popover: {
            title: '❓ Quiz — 4 Tipos de Exercício',
            description: 'Teste seu italiano com: Vocabulário (múltipla escolha) · Morfologia (gênero & plural) · Listening (reconheça pelo áudio) · Conjugação verbal. Cada acerto rende XP!',
            side: 'top', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('quiz'); }
        },

        // ── 9. Gramática ────────────────────────────────────────
        {
          element: '#grammatica-container',
          popover: {
            title: '📚 Gramática — Do A1 ao C2',
            description: '82 lições organizadas em 6 níveis (A1 → C2). Cada lição explica a regra com exemplos reais e tem exercícios interativos. Ative o Modo Imersão 🇮🇹 para ver tudo em italiano!',
            side: 'top', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('grammatica'); }
        },

        // ── 10. Vocabulário ─────────────────────────────────────
        {
          element: '#vocab-search',
          popover: {
            title: '📖 Vocabulário — Seu Glossário Completo',
            description: 'Pesquise qualquer palavra por italiano ou português. Filtre por dificuldade, favoritos ou templo. Clique em qualquer palavra para ouvir a pronúncia. Use "Ocultar PT/IT" para testar sua memória!',
            side: 'bottom', align: 'center'
          },
          onHighlightStarted: () => { App.navegar('vocabolario'); }
        },
      ]
    });

    driverObj.drive();
  }
};
