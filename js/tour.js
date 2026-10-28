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
      // 0 — header & controles rápidos (som, idioma, tema, voz)
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 1 — stats bar & meta diária
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 2 — continuar de onde parou + sessão de 15 min
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 3 — 51 templos + filtros de trilha
      { sec: 'templi',    prep: null },
      // 4 — meta prazo
      { sec: 'templi',    prep: () => window.scrollTo(0,0) },
      // 5 — flashcard selector (Templos vs Baralhos Especiais Top 500)
      { sec: 'flashcard', prep: null },
      // 6 — 5 modos de estudo (Normal, Reverso, Contexto, Escuta, Escrita)
      { sec: 'flashcard', prep: null },
      // 7 — botões avaliação FSRS-4.5
      { sec: 'flashcard', prep: () => {
          const a = document.getElementById('card-actions');
          if (a) a.style.display = 'grid';
      }},
      // 8 — quiz → abas de modalidade + templos agrupados
      { sec: 'quiz', prep: () => {
          if (typeof Quiz !== 'undefined') Quiz.renderizarSeletor();
      }},
      // 9 — gramática → continuar de onde parou + módulos A1-C2
      { sec: 'grammatica', prep: () => {
          if (typeof Grammatica !== 'undefined') Grammatica.renderizarSeletor();
      }},
      // 10 — vocabulário → Top 1000, Modo Compacto e Menu Mais
      { sec: 'vocabolario', prep: () => {
          if (typeof Vocab !== 'undefined') Vocab.renderizar();
      }},
      // 11 — storie
      { sec: 'storie', prep: () => {
          if (typeof Storie !== 'undefined') Storie.renderizarSeletor?.();
      }},
      // 12 — dialoghi
      { sec: 'dialoghi', prep: () => {
          if (typeof Dialoghi !== 'undefined') Dialoghi.renderizarSeletor?.();
      }},
      // 13 — canzoni
      { sec: 'canzoni', prep: () => {
          if (typeof Canzoni !== 'undefined') Canzoni.renderizarSeletor?.();
      }},
      // 14 — imitazione + criação via IA
      { sec: 'imitazione', prep: () => {
          if (typeof Imitazione !== 'undefined') Imitazione.renderizar?.();
      }},
    ];

    // Seletores de cada step — usados para scrollIntoView antes do Driver posicionar
    const stepSelectors = [
      '.app-header',
      '.stats-bar',
      '#continuar-container',
      '#templos-filter-bar',
      '#meta-prazo-container',
      '.card-selecao-templo',
      '#btn-modos-wrapper',
      '.card-actions',
      '#quiz-templo-selector',
      '#grammatica-container',
      '.vocab-controles',
      '#storie-container',
      '#dialoghi-container',
      '#canzoni-container',
      '#imitazione-container',
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
            title: '👋 Bem-vindo ao Italiano Autêntico!',
            description: 'Este tour rápido de 15 passos apresenta todas as ferramentas do app. No topo você alterna o idioma da interface (PT | IT), o tema (☀️/🌙), os efeitos sonoros (🔔 já ativados por padrão), a velocidade da voz (.85x / 1x) e seu Perfil (👤).',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.stats-bar',
          popover: {
            title: '🏅 Nível, XP, Ofensiva e Meta Diária',
            description: 'Acompanhe seu Nível, XP, dias seguidos de estudo (🔥), Templos desbloqueados (1 a 51) e Palavras dominadas. Logo abaixo do topo fica a barra fina da sua Meta Diária de XP.',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#continuar-container',
          popover: {
            title: '⚡ Retomada Rápida e Sessão de 15 Minutos',
            description: 'Sem tempo a perder: clique em "Continuar de onde parou" para retomar seu último estudo ou em "Sessão de Hoje (15 min)" para um treino guiado (5 min de revisão + 5 min de palavras novas + 5 min de escuta/quiz).',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#templos-filter-bar',
          popover: {
            title: '🏛️ Os 51 Templos e Filtros por Trilha',
            description: 'O app conta com 51 templos (mais de 5.000 palavras): a Trilha Clássica (1–10, de Roma a Milão) e os Templos Temáticos (11–51, do A1 ao C2). Use estes filtros para navegar rapidamente e confira a Palavra do Dia ao lado do Calendário de Ofensiva.',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#meta-prazo-container',
          popover: {
            title: '🎯 Meta com Prazo (Seu GPS)',
            description: 'Escolha um nível-alvo e uma data limite. O app calcula automaticamente quantos XP por dia você precisa conquistar para atingir sua meta no prazo!',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '.card-selecao-templo',
          popover: {
            title: '🃏 Flashcards: Templos & Baralhos Especiais (Top 500)',
            description: 'Alterne entre "🏛️ Templos" (vocabulário das cidades desbloqueadas) e "⭐ Baralhos Especiais (Top 500)" — com 5 categorias exclusivas: Colocações & Chunks, Falsos Amigos, Preposições, Verbos Irregulares e Situações da Vida Real.',
            side: 'right', align: 'start'
          }
        },
        {
          element: '#btn-modos-wrapper',
          popover: {
            title: '✍️ 5 Modos de Estudo nos Flashcards',
            description: '🎴 Normal (IT→PT) · 🔄 Reverso (PT→IT) · 📖 Contexto (frase com lacuna) · 🎧 Escuta (áudio) · ✍️ Escrita (desenhe a palavra à mão na lousa digital). Use também o botão "🌍 Revisão Geral" para revisar todas as cartas vencidas!',
            side: 'right', align: 'start'
          }
        },
        {
          element: '.card-actions',
          popover: {
            title: '⭐ Avaliação FSRS-4.5 & Imitação por Voz',
            description: 'O algoritmo FSRS-4.5 agenda a revisão no momento ideal: ❌ Esqueci · ⚡ Difícil · ✅ Bom · ⭐ Fácil. Use também "🔊 Pronunciar", "🐢 Lento" e "🎤 Imitar" para testar sua fala pelo microfone!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#quiz-templo-selector',
          popover: {
            title: '❓ Quiz Organizado por Modalidade',
            description: 'Escolha entre o "🌍 Quiz Geral" (todos os templos mistos) ou navegue pelas abas: 🏛️ Vocabulário, 🔤 Morfologia (gênero e plural), 🎧 Escuta (Listening) e 📚 Gramática & Verbos, com templos agrupados em gavetas retráteis.',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#grammatica-container',
          popover: {
            title: '📚 Gramática Interativa — Do A1 ao C2',
            description: 'Lições completas em 3 etapas: 1. Aprender a Regra, 2. Exemplos & Armadilhas e 3. Praticar. O card no topo leva você direto para a próxima lição pendente!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '.vocab-controles',
          popover: {
            title: '📖 Vocabulário & Top 1000 Palavras',
            description: 'Explore todas as palavras ou filtre pelo ranking "🔥 Top 1000" mais usadas no italiano! Alterne a visualização em "☰ Compacto" e use o menu "⋯ Mais" para ocultar colunas (PT/IT) ou adicionar palavras via IA.',
            side: 'bottom', align: 'center'
          }
        },
        {
          element: '#storie-container',
          popover: {
            title: '📚 Histórias e Ensaios Filosóficos',
            description: 'Leia contos e reflexões do A1 ao C2 em formato de livro clássico paginado, com estimativa de tempo de leitura (⏱️), marcador de página automático, narração em voz alta e tradução ao tocar em qualquer palavra.',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#dialoghi-container',
          popover: {
            title: '💬 Diálogos da Vida Real',
            description: '200 diálogos interativos com filtro por nível e por tema (🍝 Restaurante, ✈️ Viagem, 🛍️ Cotidiano, 💼 Trabalho, 🏥 Saúde, 🎭 Cultura). Conclua no Modo Prática para ganhar XP e o selo ✓!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#canzoni-container',
          popover: {
            title: '🎵 Músicas com Karaokê & Cloze Studio',
            description: '100 trechos musicais didáticos com barra de progresso por música, destaque sincronizado palavra por palavra (Karaokê), treino de lacunas e o "🎧 Cloze Studio" para importar suas próprias faixas!',
            side: 'top', align: 'center'
          }
        },
        {
          element: '#imitazione-container',
          popover: {
            title: '🎙️ Dojo de Imitação & Criação com IA',
            description: 'Ouça o modelo nativo (1.0x ou 0.75x), grave sua voz pelo microfone (no celular ou computador) e receba diagnóstico palavra por palavra! E em qualquer tela, use o botão "🤖 + IA" para gerar novos conteúdos personalizados.',
            side: 'top', align: 'center'
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
