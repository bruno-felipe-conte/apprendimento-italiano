// ============================================================
// tour.js — Guided Walkthrough Tour via Driver.js
// ============================================================

const Tour = {
  STORAGE_KEY: 'it_tour_done',

  iniciar() {
    // Only run if driver.js is loaded
    if (!window.driver || !window.driver.js) {
      console.warn("Driver.js not loaded. Skipping tour.");
      return;
    }

    try {
      if (localStorage.getItem(this.STORAGE_KEY)) return;
    } catch(e) {}

    const driver = window.driver.js.driver;
    const isMobile = window.innerWidth <= 768;
    
    // Function to get the right tab selector based on device
    const getTab = (section) => {
      return isMobile 
        ? `.bottom-nav [data-section="${section}"]` 
        : `.nav-tabs [data-section="${section}"]`;
    };
    
    const driverObj = driver({
      showProgress: true,
      animate: true,
      allowClose: true,
      nextBtnText: 'Avanti',
      prevBtnText: 'Indietro',
      doneBtnText: 'Finito!',
      progressText: 'Passo {{current}} de {{total}}',
      popoverClass: 'app-tour-theme', // Our custom CSS theme
      onDestroyStarted: () => {
        if (!driverObj.hasNextStep() || confirm("Vuoi uscire dal tour? (Deseja pular o tour?)")) {
          driverObj.destroy();
          try {
            localStorage.setItem(this.STORAGE_KEY, '1');
          } catch(e) {}
        }
      },
      steps: [
        {
          element: getTab('templi'),
          popover: {
            title: '🏛️ Templi (Sua Jornada)',
            description: 'Aqui é o coração do seu aprendizado. Desbloqueie novos templos e alcance sua meta diária de experiência.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('templi'); }
        },
        {
          element: getTab('dialoghi'),
          popover: {
            title: '💬 Dialoghi',
            description: 'Leia e escute diálogos reais para pegar o ritmo, contexto e melhorar sua compreensão auditiva.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('dialoghi'); }
        },
        {
          element: getTab('canzoni'),
          popover: {
            title: '🎵 Canzoni',
            description: 'Aprenda vocabulário se divertindo com os clássicos da música italiana.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('canzoni'); }
        },
        {
          element: getTab('imitazione'),
          popover: {
            title: '🎙️ Imitazione',
            description: 'Escute um nativo falando e grave sua própria voz. O segredo para uma dicção autêntica.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('imitazione'); }
        },
        {
          element: getTab('flashcard'),
          popover: {
            title: '🧠 Flashcard',
            description: 'Revise o vocabulário no momento exato em que estiver prestes a esquecer, usando nosso algoritmo espaçado.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('flashcard'); }
        },
        {
          element: getTab('quiz'),
          popover: {
            title: '📝 Quiz',
            description: 'Teste seus conhecimentos em baterias de exercícios rápidos e conquiste moedas.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('quiz'); }
        },
        {
          element: getTab('grammatica'),
          popover: {
            title: '📚 Grammatica',
            description: 'Dúvidas estruturais? Consulte rapidamente todas as regras de gramática aqui.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('grammatica'); }
        },
        {
          element: getTab('vocabolario'),
          popover: {
            title: '📖 Vocabolario',
            description: 'Seu glossário mestre. Pesquise por qualquer palavra aprendida até o momento.',
            side: isMobile ? 'top' : 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { App.navegar('vocabolario'); }
        },
        {
          element: '.top-header',
          popover: {
            title: '⚙️ Configurações & Perfil',
            description: 'Mude para o modo escuro, silencie os sons e acesse as opções de Perfil no topo da tela.',
            side: 'bottom',
            align: 'center'
          },
          onHighlightStarted: () => { 
            App.navegar('templi'); 
            window.scrollTo(0, 0); 
          }
        }
      ]
    });

    driverObj.drive();
  }
};

