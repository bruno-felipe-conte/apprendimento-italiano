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
      // 4 — flashcard selector (Templos vs Baralhos Especiais Top 500)
      { sec: 'flashcard', prep: null },
      // 5 — 5 modos de estudo (wrapper)
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
      // 9 — vocabulário → Top 1000 e botões Ocultar PT/IT
      { sec: 'vocabolario', prep: () => {
          if (typeof Vocab !== 'undefined') Vocab.renderizar();
      }},
      // 10 — storie
      { sec: 'storie', prep: () => {
          if (typeof Storie !== 'undefined') Storie.renderizarSeletor?.();
      }},
      // 11 — dialoghi
      { sec: 'dialoghi', prep: () => {
          if (typeof Dialoghi !== 'undefined') Dialoghi.renderizarSeletor?.();
      }},
      // 12 — canzoni
      { sec: 'canzoni', prep: () => {
          if (typeof Canzoni !== 'undefined') Canzoni.renderizarSeletor?.();
      }},
      // 13 — imitazione
      { sec: 'imitazione', prep: () => {
          if (typeof Imitazione !== 'undefined') Imitazione.renderizar?.();
      }},
      // 14 — botão 🤖 via IA (storie)
      { sec: 'storie', prep: () => {
          if (typeof Storie !== 'undefined') Storie.renderizarSeletor?.();
      }},
    ];

    // Seletores de cada step — usados para scrollIntoView antes do Driver posicionar
    const stepSelectors = [
      '.app-header',
      '.stats-bar',
      '#templos-grid .templo-card:first-child',   // só o Templo 1
      '#meta-prazo-container',
      '.card-selecao-templo',
      '#btn-modos-wrapper',                         // todos os 5 botões de modo
      '.card-actions',
      '.quiz-templo-btn:not(.bloqueado)',           // Le Fondamenta
      '.gram-nivel-banner',                         // bloco A1
      '#vocab-blur-btns',                           // Ocultar PT / Ocultar IT
      '#storie-container',                          // lista de histórias
      '.dialogo-card',                              // card de diálogo
      '#canzoni-container .dialogo-card',           // card de canção
      '#imitazione-container',                      // container imitazione
      '.btn-ia-add',                                // botão 🤖 via IA
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
            description: 'Este tour de 15 passos apresenta todas as funções do app. No topo você alterna o idioma (PT | IT), o tema (☀️/🌙), os efeitos sonoros (🔔 já ativados por padrão), a velocidade da voz (.85x / 1x) e o seu Perfil (👤).',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.stats-bar',
          popover: {
            title: '🏅 Nível, XP, Sequência e Meta do Dia',
            description: 'Acompanhe seu Nível, XP, dias seguidos (🔥), Templos desbloqueados e Palavras dominadas. Logo abaixo fica sua Meta do Dia — clique em "⚙️ Meta" para ajustar seu objetivo diário!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#templos-grid .templo-card:first-child',
          popover: {
            title: '🏛️ Os Templos do Italiano — Comece por Roma!',
            description: 'Cada templo reúne o vocabulário essencial de uma cidade ou tema italiano (50 templos do A1 ao C2). Comece pelo Templo 1 (Roma) e suba de nível para desbloquear os próximos!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#meta-prazo-container',
          popover: {
            title: '🎯 Defina uma Meta com Prazo',
            description: 'Escolha um nível-alvo e uma data limite. O app calcula quantos XP por dia você precisa conquistar para chegar lá a tempo — seu GPS de aprendizado!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.card-selecao-templo',
          popover: {
            title: '🃏 Flashcards: Templos & Baralhos Especiais (Top 500)',
            description: 'Alterne entre "🏛️ Templos" (cidades desbloqueadas) e "⭐ Baralhos Especiais (Top 500)" — com 5 categorias práticas: Colocações & Chunks, Falsos Amigos, Preposições, Verbos Irregulares e Situações da Vida Real.',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#btn-modos-wrapper',
          popover: {
            title: '✍️ 5 Modos de Estudo nos Flashcards',
            description: '🎴 Normal (IT→PT) · 🔄 Reverso (PT→IT) · 📖 Contexto (complete a frase) · 🎧 Escuta (adivinhe pelo áudio) · ✍️ Scrittura (escreva a palavra à mão com o dedo ou mouse!).',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.card-actions',
          popover: {
            title: '⭐ Avaliação FSRS-4.5 & Imitação por Voz',
            description: 'O algoritmo FSRS-4.5 agenda a revisão no momento ideal: ❌ Esqueci · ⚡ Difícil · ✅ Bom · ⭐ Fácil. Use também "🔊 Pronunciar", "🐢 Lento" e "🎤 Imitar" para treinar sua fala no microfone!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '.quiz-templo-btn:not(.bloqueado)',
          popover: {
            title: '❓ Quiz — 5 Modalidades de Exercício',
            description: 'Teste seus conhecimentos no Quiz Generale misto ou por templo: Vocabulário · Morfologia (gênero & plural) · Listening (áudio) · Gramática · Conjugação Verbal. Cada acerto rende XP!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '.gram-nivel-banner',
          popover: {
            title: '📚 Gramática — Do A1 ao C2',
            description: 'Lições completas em 3 etapas: Regra, Exemplos e Prática. Clique no banner do nível para expandir ou recolher os capítulos!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#vocab-blur-btns',
          popover: {
            title: '📖 Vocabulário & Ranking Top 1000',
            description: 'Explore todas as palavras ou filtre pelo botão "🔥 Top 1000" (as 1.000 palavras mais usadas no italiano com frases de exemplo narradas). Use "Ocultar PT" ou "Ocultar IT" para testar a memória!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#storie-container',
          popover: {
            title: '📖 Storie — Leitura em Formato de Livro',
            description: 'Leia contos e reflexões filosóficas (A1–C2) diagramados como livro clássico paginado. Toque em qualquer palavra para ver a tradução, ouvir a pronúncia e salvar nos flashcards!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.dialogo-card',
          popover: {
            title: '💬 Dialoghi — Conversação Real',
            description: '200 diálogos do cotidiano italiano com Modo Leitura e Modo Prática interativo. Ouça cada turno e escolha a resposta certa para ganhar XP!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#canzoni-container .dialogo-card',
          popover: {
            title: '🎵 Canzoni — Karaokê & Cloze Studio',
            description: 'Aprenda com músicas italianas no modo Karaokê (destaque palavra por palavra), complete as lacunas ou use o "🎧 Cloze Studio" para importar suas próprias faixas!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#imitazione-container',
          popover: {
            title: '🎤 Imitazione — Estúdio de Pronúncia',
            description: 'Ouça o modelo nativo (1.0x ou 0.75x) e fale no microfone (no celular ou computador). O app avalia sua dicção palavra por palavra e permite ouvir sua própria gravação!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '.btn-ia-add',
          popover: {
            title: '🤖 Crie Conteúdo Personalizado com IA',
            description: 'Clique em "🤖 via IA" em qualquer seção para gerar novos diálogos, histórias, músicas, frases ou vocabulário personalizados — ou cole textos livres para criar livros interativos!',
            side: 'bottom', align: 'center'
          }
        },
      ]
    });

    // Navega ao passo inicial antes de iniciar o Driver
    navegar(0, () => driverObj.drive());
  }
};


// Exposição global segura para navegadores e testes
if (typeof window !== 'undefined') window.Tour = Tour;
if (typeof globalThis !== 'undefined') globalThis.Tour = Tour;
if (typeof module !== 'undefined' && module.exports) module.exports = Tour;
