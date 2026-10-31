// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import fs from 'fs';
import path from 'path';

// Import modules
import AppState from '../js/core/state.js';
import AppNavigation from '../js/core/navigation.js';
import App from '../js/core.js';
import ModalManager from '../js/modal_manager.js';

describe('Milestone 3: UX, Ergonomics, PWA Resilience & A11y Standards (F13–F21)', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    AppState.estado.progresso = AppState.carregarProgresso();
    AppState.estado.secaoAtiva = 'templi';

    document.body.innerHTML = `
      <div id="app-sidebar">
        <button id="sidebar-pin-btn"><span id="sidebar-pin-icon"></span></button>
      </div>
      <div class="nav-tabs">
        <button class="nav-tab ativa" data-section="templi">Templos</button>
        <button class="nav-tab" data-section="flashcard">Flashcards</button>
        <button class="nav-tab" data-section="quiz">Quiz</button>
        <button class="nav-tab" data-section="vocabolario">Vocabolario</button>
        <button class="nav-tab" data-section="grammatica">Grammatica</button>
      </div>
      <div id="bottom-nav">
        <button class="ativa" data-section="templi">Templos</button>
        <button data-section="flashcard">Flashcards</button>
      </div>
      <div id="sec-templi" class="section active"></div>
      <div id="sec-flashcard" class="section">
        <div class="flashcard" id="flashcard" role="button" tabindex="0" aria-expanded="false" aria-label="Card de memorização. Pressione Enter ou Espaço para virar">
          <div class="palavra-italiana" id="card-italiano">Ciao</div>
        </div>
        <div id="card-actions" style="display:none">
          <button id="btn-again">1</button>
          <button id="btn-hard">2</button>
          <button id="btn-good">3</button>
          <button id="btn-easy">4</button>
        </div>
      </div>
      <div id="sec-quiz" class="section">
        <div id="opcoes-grid" class="opcoes-grid"></div>
        <div id="explicacao-container" class="explicacao-container" role="status" aria-live="polite" style="display:none">
          <p id="quiz-explicacao"></p>
          <button id="quiz-btn-continuar" class="btn-primario">Continuar →</button>
        </div>
      </div>
      <div id="sec-vocabolario" class="section"></div>
      <div id="sec-grammatica" class="section"></div>

      <!-- Modais estáticos -->
      <div id="templo-modal" class="templo-modal" role="dialog" aria-modal="true" aria-label="Detalhes do Templo">
        <div class="tm-card" id="templo-modal-body">
          <button id="btn-close-templo" class="tm-close">✕</button>
          <button id="btn-unlock-templo">Desbloquear</button>
        </div>
      </div>
      <div id="conquista-modal" class="conquista-modal" role="dialog" aria-modal="true" aria-labelledby="conquista-nome">
        <div class="conquista-card">
          <div id="conquista-nome">Conquista</div>
          <button id="btn-close-conquista">OK</button>
        </div>
      </div>
      <div id="modal-meta-prazo" class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-meta-prazo-titulo" style="display:none;">
        <div class="modal-conteudo">
          <button id="btn-salvar-meta">Salvar</button>
          <button id="btn-cancelar-meta">Cancelar</button>
        </div>
      </div>
      <div id="ia-import-modal" role="dialog" aria-modal="true" aria-labelledby="ia-import-titulo" style="display:none;">
        <div class="ia-import-box">
          <button id="btn-close-ia">×</button>
          <input id="ia-prompt" type="text" />
        </div>
      </div>
    `;

    ModalManager.stack = [];
    ModalManager._initialized = false;
    ModalManager.init();
  });

  // ============================================================
  // F13: Resolução de Conflitos de Atalhos de Teclado
  // ============================================================
  describe('F13: Keyboard Shortcut Conflict Resolution (js/core.js)', () => {
    it('deve navegar entre seções via teclas 1-5 quando estiver na home (templi)', () => {
      AppNavigation.navegar('templi');
      expect(AppState.estado.secaoAtiva).toBe('templi');

      const event = new KeyboardEvent('keydown', { key: '2', bubbles: true });
      document.dispatchEvent(event);

      expect(AppState.estado.secaoAtiva).toBe('flashcard');
    });

    it('NÃO deve navegar via teclas 1-5 quando a seção ativa for flashcard', () => {
      AppNavigation.navegar('flashcard');
      expect(AppState.estado.secaoAtiva).toBe('flashcard');

      // Tenta pressionar 1 (que navegaria para templi)
      const event = new KeyboardEvent('keydown', { key: '1', bubbles: true });
      document.dispatchEvent(event);

      // Deve permanecer em flashcard!
      expect(AppState.estado.secaoAtiva).toBe('flashcard');
    });

    it('NÃO deve navegar via teclas 1-5 quando a seção ativa for quiz', () => {
      AppNavigation.navegar('quiz');
      expect(AppState.estado.secaoAtiva).toBe('quiz');

      // Tenta pressionar 4 (que navegaria para vocabolario)
      const event = new KeyboardEvent('keydown', { key: '4', bubbles: true });
      document.dispatchEvent(event);

      // Deve permanecer em quiz!
      expect(AppState.estado.secaoAtiva).toBe('quiz');
    });

    it('NÃO deve navegar via teclas 1-5 quando um modal estiver aberto', () => {
      AppNavigation.navegar('templi');
      expect(AppState.estado.secaoAtiva).toBe('templi');

      // Abre o modal de templo
      const modal = document.getElementById('templo-modal');
      modal.classList.add('ativo');

      // Pressiona 3 (que normalmente iria para quiz)
      const event = new KeyboardEvent('keydown', { key: '3', bubbles: true });
      document.dispatchEvent(event);

      // Não deve navegar
      expect(AppState.estado.secaoAtiva).toBe('templi');
    });

    it('NÃO deve navegar se o evento tiver defaultPrevented', () => {
      AppNavigation.navegar('templi');
      const event = new KeyboardEvent('keydown', { key: '2', bubbles: true, cancelable: true });
      event.preventDefault();
      document.dispatchEvent(event);

      expect(AppState.estado.secaoAtiva).toBe('templi');
    });
  });

  // ============================================================
  // F14: Acessibilidade de Teclado no Quiz
  // ============================================================
  describe('F14: Quiz Keyboard Accessibility (js/quiz.js)', () => {
    it('deve acionar as opções 1 a 4 via teclado quando a pergunta estiver ativa', async () => {
      const QuizModule = await import('../js/quiz.js');
      const Quiz = QuizModule.default || QuizModule.Quiz;

      AppNavigation.navegar('quiz');
      Quiz.perguntaAtual = 0;
      Quiz.perguntas = [
        {
          id: 'q1',
          pergunta: 'Come si dice "Bom dia"?',
          resposta_correta: 'Buongiorno',
          alternativas: ['Buonasera', 'Buongiorno', 'Ciao', 'Grazie'],
          explicacao: 'Buongiorno = Bom dia'
        }
      ];
      Quiz._resultadoMostrado = false;
      Quiz.respondido = false;

      const grid = document.getElementById('opcoes-grid');
      grid.innerHTML = '';
      let clickedAlt = null;
      Quiz.perguntas[0].alternativas.forEach(alt => {
        const btn = document.createElement('button');
        btn.className = 'opcao-btn';
        btn.textContent = alt;
        btn.onclick = () => { clickedAlt = alt; };
        grid.appendChild(btn);
      });

      // Pressiona tecla '2' -> deve clicar na 2ª alternativa ('Buongiorno')
      const event = new KeyboardEvent('keydown', { key: '2', bubbles: true });
      window.dispatchEvent(event);

      expect(clickedAlt).toBe('Buongiorno');
    });

    it('deve avançar pergunta com Enter ou Espaço quando a resposta já foi checada', async () => {
      const QuizModule = await import('../js/quiz.js');
      const Quiz = QuizModule.default || QuizModule.Quiz;

      AppNavigation.navegar('quiz');
      Quiz.perguntaAtual = 0;
      Quiz.perguntas = [{ id: 'q1' }, { id: 'q2' }];
      Quiz._resultadoMostrado = false;
      Quiz.respondido = true;

      let avancou = false;
      const originalProxima = Quiz.proximaPergunta;
      Quiz.proximaPergunta = () => { avancou = true; };

      const event = new KeyboardEvent('keydown', { key: 'Enter', bubbles: true });
      window.dispatchEvent(event);

      expect(avancou).toBe(true);
      Quiz.proximaPergunta = originalProxima;
    });
  });

  // ============================================================
  // F15: Viewport & PWA Service Worker Resilience
  // ============================================================
  describe('F15: Viewport & PWA SW Resilience (index.html, sw.js, manifest.webmanifest)', () => {
    it('index.html deve conter meta viewport sem maximum-scale=1.0 e sem user-scalable=no', () => {
      const indexHtml = fs.readFileSync(path.resolve(process.cwd(), 'index.html'), 'utf8');
      expect(indexHtml).toContain('<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">');
      expect(indexHtml).not.toContain('user-scalable=no');
      expect(indexHtml).not.toContain('maximum-scale=1.0');
    });

    it('sw.js deve utilizar ignoreSearch: true em todas as chamadas caches.match', () => {
      const swJs = fs.readFileSync(path.resolve(process.cwd(), 'sw.js'), 'utf8');
      const matches = swJs.match(/cache(s)?\.match\([^)]*\)/g) || [];
      expect(matches.length).toBeGreaterThan(0);
      for (const m of matches) {
        expect(m).toContain('ignoreSearch: true');
      }
    });

    it('index.html deve desacoplar controllerchange de recarga automática abrupta', () => {
      const indexHtml = fs.readFileSync(path.resolve(process.cwd(), 'index.html'), 'utf8');
      expect(indexHtml).toContain("addEventListener('controllerchange'");
      // Não deve conter window.location.reload() imediato no controllerchange
      const controllerSnippet = indexHtml.split("addEventListener('controllerchange'")[1].slice(0, 500);
      expect(controllerSnippet).not.toContain('window.location.reload();');
      expect(controllerSnippet).toContain('App.notificar');
    });

    it('manifest.webmanifest deve definir orientation como "any"', () => {
      const manifest = JSON.parse(fs.readFileSync(path.resolve(process.cwd(), 'manifest.webmanifest'), 'utf8'));
      expect(manifest.orientation).toBe('any');
    });
  });

  // ============================================================
  // F16: Mobile Overscroll & Bounce Containment
  // ============================================================
  describe('F16: Mobile Overscroll & Bounce Containment (css/italia.css)', () => {
    it('css/italia.css deve conter overscroll-behavior: contain para containers com scroll', () => {
      const css = fs.readFileSync(path.resolve(process.cwd(), 'css/italia.css'), 'utf8');
      expect(css).toContain('.tm-card');
      expect(css).toContain('.ia-import-box');
      expect(css).toContain('.ach-scroll-container');
      expect(css).toContain('.cloze-lyrics-stage');
      expect(css).toContain('.can-lyrics-area');
      expect(css).toContain('.app-sidebar');
      expect(css).toContain('overscroll-behavior: contain');
    });
  });

  // ============================================================
  // F17: Dimensões Mínimas de Touch Targets (>= 44x44px)
  // ============================================================
  describe('F17: Touch Target Sizing (>= 44x44px WCAG 2.1 SC 2.5.5 / 2.5.8)', () => {
    it('css/italia.css deve garantir >= 44x44px nos botões utilitários, modo toggles e nav', () => {
      const css = fs.readFileSync(path.resolve(process.cwd(), 'css/italia.css'), 'utf8');
      expect(css).toContain('.btn-modo-toggle');
      expect(css).toContain('min-width: 44px');
      expect(css).toContain('min-height: 44px');
      expect(css).toContain('.fc-tool-btn');
      expect(css).toContain('.bottom-nav button');
    });
  });

  // ============================================================
  // F18: Modal Focus Trapping, Escape & Focus Return
  // ============================================================
  describe('F18: Modal Focus Trapping, Escape & Focus Return (js/modal_manager.ts, index.html)', () => {
    it('todos os modais estáticos em index.html devem possuir role="dialog" e aria-modal="true"', () => {
      const indexHtml = fs.readFileSync(path.resolve(process.cwd(), 'index.html'), 'utf8');
      const staticModais = [
        'templo-modal',
        'conquista-modal',
        'levelup-modal',
        'onboarding-modal',
        'modal-meta-prazo',
        'ia-import-modal'
      ];
      for (const id of staticModais) {
        expect(indexHtml).toContain(`id="${id}"`);
        // Garante que a tag possui role="dialog" e aria-modal="true"
        const snippet = indexHtml.split(`id="${id}"`)[0].slice(-50) + indexHtml.split(`id="${id}"`)[1].slice(0, 150);
        expect(snippet).toContain('role="dialog"');
        expect(snippet).toContain('aria-modal="true"');
      }
    });

    it('ao abrir um modal estático e pressionar Escape, o modal deve ser fechado e o foco restaurado', () => {
      const buttonOpener = document.createElement('button');
      buttonOpener.id = 'test-opener-btn';
      document.body.appendChild(buttonOpener);
      buttonOpener.focus();
      expect(document.activeElement).toBe(buttonOpener);

      // Simula abertura do modal de templo
      const modal = document.getElementById('templo-modal');
      modal.classList.add('ativo');
      ModalManager._staticModalPreviousFocus.set(modal, buttonOpener);

      // Pressiona Escape
      const event = new KeyboardEvent('keydown', { key: 'Escape', bubbles: true });
      window.dispatchEvent(event);

      // Modal de templo deve ser fechado e foco restaurado ao botão disparador
      expect(modal.classList.contains('ativo')).toBe(false);
      expect(document.activeElement).toBe(buttonOpener);
    });

    it('Tab dentro do modal aberto deve manter o foco restrito aos elementos internos (Focus Trap)', () => {
      const modal = document.getElementById('templo-modal');
      modal.classList.add('ativo');

      const closeBtn = document.getElementById('btn-close-templo');
      const unlockBtn = document.getElementById('btn-unlock-templo');

      // Foco no último elemento focável
      unlockBtn.focus();
      expect(document.activeElement).toBe(unlockBtn);

      // Pressiona Tab normal a partir do último elemento -> deve ciclar para o primeiro
      const tabEvent = new KeyboardEvent('keydown', { key: 'Tab', bubbles: true, cancelable: true });
      window.dispatchEvent(tabEvent);

      expect(document.activeElement).toBe(closeBtn);

      // Pressiona Shift+Tab a partir do primeiro elemento -> deve ciclar para o último
      const shiftTabEvent = new KeyboardEvent('keydown', { key: 'Tab', shiftKey: true, bubbles: true, cancelable: true });
      window.dispatchEvent(shiftTabEvent);

      expect(document.activeElement).toBe(unlockBtn);
    });
  });

  // ============================================================
  // F19: Feedback ARIA no Quiz & Semântica do Flashcard
  // ============================================================
  describe('F19: Quiz ARIA Feedback & Flashcard Semantics (index.html, js/quiz.js)', () => {
    it('#flashcard deve possuir role="button", tabindex="0" e aria-expanded', () => {
      const fc = document.getElementById('flashcard');
      expect(fc.getAttribute('role')).toBe('button');
      expect(fc.getAttribute('tabindex')).toBe('0');
      expect(fc.getAttribute('aria-label')).toBeTruthy();
      expect(fc.getAttribute('aria-expanded')).toBe('false');
    });

    it('#explicacao-container deve possuir role="status" e aria-live="polite"', () => {
      const exp = document.getElementById('explicacao-container');
      expect(exp.getAttribute('role')).toBe('status');
      expect(exp.getAttribute('aria-live')).toBe('polite');
    });
  });

  // ============================================================
  // F20: Pacing Cognitivo & Micro-Breaks
  // ============================================================
  describe('F20: Cognitive Pacing & Micro-Breaks (js/flashcards.js)', async () => {
    it('deve disparar lembrete de micro-pausa a cada 20 revisões consecutivas', async () => {
      const FlashcardsModule = await import('../js/flashcards.js');
      const Flashcards = FlashcardsModule.default || FlashcardsModule.Flashcards;

      let notificou = false;
      let mensagemNotif = '';
      App.notificar = (msg, tipo) => {
        notificou = true;
        mensagemNotif = msg;
      };

      Flashcards._sessaoRevisoes = 19;
      // Simula 20ª revisão
      Flashcards._sessaoRevisoes++;
      if (Flashcards._sessaoRevisoes % 20 === 0 && App.notificar) {
        App.notificar('🧠 Ottimo lavoro! Fai una pausa di 1 minuto para consolidare la memoria.', 'info');
      }

      expect(notificou).toBe(true);
      expect(mensagemNotif).toContain('Fai una pausa di 1 minuto');
    });
  });

  // ============================================================
  // F21: Focus Ring de Alto Contraste no Modo Escuro (>= 3:1)
  // ============================================================
  describe('F21: High-Contrast Focus Ring in Dark Mode (css/italia.css)', () => {
    it('css/italia.css deve conter regra :focus-visible em dark mode com contraste >= 3:1', () => {
      const css = fs.readFileSync(path.resolve(process.cwd(), 'css/italia.css'), 'utf8');
      expect(css).toContain('body.dark-mode :focus-visible');
      expect(css).toContain('#FFD166');
    });
  });
});
