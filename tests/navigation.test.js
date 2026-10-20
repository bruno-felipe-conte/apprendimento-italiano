// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import AppState from '../js/core/state.js';
import AppNavigation from '../js/core/navigation.js';
import App from '../js/core.js';

describe('ARC-02: Submódulo de Navegação (AppNavigation & App Facade)', () => {
  beforeEach(() => {
    localStorage.clear();
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
      </div>
      <div id="bottom-nav">
        <button class="ativa" data-section="templi">Templos</button>
        <button data-section="flashcard">Flashcards</button>
      </div>
      <div id="sec-templi" class="section active"></div>
      <div id="sec-flashcard" class="section"></div>
      <div id="sec-quiz" class="section"></div>
      <div id="sec-vocabolario" class="section"></div>
    `;
  });

  it('deve alternar a seção ativa e atualizar classes no DOM', () => {
    AppNavigation.navegar('flashcard');

    expect(AppState.estado.secaoAtiva).toBe('flashcard');
    expect(AppState.estado.progresso.ultima_secao).toBe('flashcard');

    const tabFlashcard = document.querySelector('.nav-tab[data-section="flashcard"]');
    const tabTempli = document.querySelector('.nav-tab[data-section="templi"]');
    expect(tabFlashcard.classList.contains('ativa')).toBe(true);
    expect(tabTempli.classList.contains('ativa')).toBe(false);

    const secFlashcard = document.getElementById('sec-flashcard');
    const secTempli = document.getElementById('sec-templi');
    expect(secFlashcard.classList.contains('active')).toBe(true);
    expect(secTempli.classList.contains('active')).toBe(false);
  });

  it('deve tratar "home" como alias de "templi"', () => {
    AppNavigation.navegar('home');
    expect(AppState.estado.secaoAtiva).toBe('templi');
    expect(document.getElementById('sec-templi').classList.contains('active')).toBe(true);
  });

  it('deve delegar de forma idêntica via facade App.navegar', () => {
    App.navegar('quiz');
    expect(AppState.estado.secaoAtiva).toBe('quiz');
    expect(App.estado.secaoAtiva).toBe('quiz');
    expect(document.getElementById('sec-quiz').classList.contains('active')).toBe(true);
  });

  it('deve controlar o estado de fixação da sidebar (pin/unpin)', () => {
    expect(document.body.classList.contains('sidebar-pinned')).toBe(false);

    AppNavigation.toggleSidebarPin();
    expect(document.body.classList.contains('sidebar-pinned')).toBe(true);
    expect(localStorage.getItem('it_sidebar_pinned')).toBe('true');

    AppNavigation.toggleSidebarPin();
    expect(document.body.classList.contains('sidebar-pinned')).toBe(false);
    expect(localStorage.getItem('it_sidebar_pinned')).toBe('false');
  });
});
