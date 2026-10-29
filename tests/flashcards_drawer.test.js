// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import '../js/flashcards.js';

describe('Gaveta Retrátil nos Flashcards (Zero-Scroll UX)', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div class="fc-compact-bar" id="fc-compact-bar">
        <div class="fc-compact-summary" id="fc-compact-summary">
          <span class="fc-compact-badge" id="fc-compact-origem">🏛️ Tempio 1</span>
          <span class="fc-compact-pill" id="fc-compact-modo">🎴 Normal</span>
          <span class="fc-compact-counter" id="fc-compact-count">1/20</span>
        </div>
        <button type="button" class="fc-compact-toggle-btn" id="fc-compact-toggle-btn" aria-expanded="false">
          <span>Baralhos</span>
          <span class="fc-compact-chevron" id="fc-compact-chevron">▾</span>
        </button>
      </div>
      <div class="fc-seletor-drawer recolhido" id="fc-seletor-drawer">
        <div class="card-selecao-templo">
          <select id="flashcard-templo-select">
            <option value="1">1. Roma</option>
            <option value="2">2. Firenze</option>
          </select>
          <select id="flashcard-deck-select">
            <option value="deck_all">Todos</option>
            <option value="deck_colocacoes">Chunks</option>
          </select>
        </div>
      </div>
      <div id="flashcard" style="display:none"></div>
      <div id="card-actions" style="display:none"></div>
      <div id="flashcard-vazio" style="display:none"></div>
      <div id="card-info"></div>
    `;

    // Mock global App and Progressao
    globalThis.App = {
      estado: {
        progresso: { templos_desbloqueados: [1, 2] },
        topFlashcards: [{ deck: 'colocacoes', id: 'top_1', italiano: 'ciao', portugues: 'olá' }],
        templosData: {
          1: { nome: 'Roma', palavras: [{ id: 'p1', italiano: 'ciao', portugues: 'olá' }] },
          2: { nome: 'Firenze', palavras: [{ id: 'p2', italiano: 'grazie', portugues: 'obrigado' }] }
        },
        flashcardData: {}
      },
      notificar: vi.fn(),
      ehFavorito: vi.fn(() => false),
      pronunciar: vi.fn(),
      navegar: vi.fn()
    };

    globalThis.Progressao = {
      temploDesbloqueado: vi.fn(() => true),
      temploConcluido: vi.fn(() => false)
    };

    globalThis.I18n = {
      t: vi.fn((k) => k)
    };

    Flashcards.cartasDisponiveis = [{ id: 'p1', italiano: 'ciao', portugues: 'olá' }];
    Flashcards.indiceAtual = 0;
    Flashcards.recolherGaveta();
  });

  it('1. Deve iniciar com a gaveta recolhida por padrão quando há sessão', () => {
    const drawer = document.getElementById('fc-seletor-drawer');
    const btn = document.getElementById('fc-compact-toggle-btn');

    expect(Flashcards.gavetaAberta).toBe(false);
    expect(drawer?.classList.contains('recolhido')).toBe(true);
    expect(btn?.getAttribute('aria-expanded')).toBe('false');
  });

  it('2. Deve abrir e fechar a gaveta ao alternar com toggleGaveta()', () => {
    const drawer = document.getElementById('fc-seletor-drawer');
    const btn = document.getElementById('fc-compact-toggle-btn');

    // Abre
    Flashcards.toggleGaveta();
    expect(Flashcards.gavetaAberta).toBe(true);
    expect(drawer?.classList.contains('recolhido')).toBe(false);
    expect(btn?.getAttribute('aria-expanded')).toBe('true');
    expect(btn?.innerHTML).toContain('Fechar');

    // Fecha
    Flashcards.toggleGaveta();
    expect(Flashcards.gavetaAberta).toBe(false);
    expect(drawer?.classList.contains('recolhido')).toBe(true);
    expect(btn?.getAttribute('aria-expanded')).toBe('false');
    expect(btn?.innerHTML).toContain('Baralhos');
  });

  it('3. Deve recolher a gaveta automaticamente após selecionar um templo', () => {
    const drawer = document.getElementById('fc-seletor-drawer');

    // Abre a gaveta primeiro
    Flashcards.abrirGaveta();
    expect(drawer?.classList.contains('recolhido')).toBe(false);

    // Usuário seleciona o templo 2
    Flashcards.selecionarTemplo(2);

    // A gaveta deve se recolher imediatamente
    expect(Flashcards.gavetaAberta).toBe(false);
    expect(drawer?.classList.contains('recolhido')).toBe(true);
    expect(Flashcards.temploAtual).toBe(2);
  });

  it('4. Deve recolher a gaveta automaticamente após selecionar um baralho especial', () => {
    const drawer = document.getElementById('fc-seletor-drawer');

    // Abre a gaveta
    Flashcards.abrirGaveta();
    expect(drawer?.classList.contains('recolhido')).toBe(false);

    // Usuário seleciona um baralho especial
    Flashcards.selecionarDeckEspecial('deck_colocacoes');

    // A gaveta deve se recolher imediatamente
    expect(Flashcards.gavetaAberta).toBe(false);
    expect(drawer?.classList.contains('recolhido')).toBe(true);
    expect(Flashcards.temploAtual).toBe('deck_colocacoes');
  });

  it('5. toggleSeletor deve funcionar como alias retrocompatível', () => {
    const drawer = document.getElementById('fc-seletor-drawer');

    Flashcards.recolherGaveta();
    expect(Flashcards.gavetaAberta).toBe(false);

    Flashcards.toggleSeletor();
    expect(Flashcards.gavetaAberta).toBe(true);
    expect(drawer?.classList.contains('recolhido')).toBe(false);

    Flashcards.toggleSeletor(true); // forcar recolhido
    expect(Flashcards.gavetaAberta).toBe(false);
    expect(drawer?.classList.contains('recolhido')).toBe(true);
  });

  it('6. O botão toggle da barra compacta deve conter apenas 1 ícone/chevron (sem emojis duplicados)', () => {
    const btn = document.getElementById('fc-compact-toggle-btn');
    Flashcards.recolherGaveta();
    expect(btn?.textContent?.trim()).toMatch(/^Baralhos\s*▾$/);
    expect(btn?.textContent).not.toContain('⚙️');

    Flashcards.abrirGaveta();
    expect(btn?.textContent?.trim()).toMatch(/^Fechar\s*▴$/);
    expect(btn?.textContent).not.toContain('✕');
  });

  it('7. A curva de esquecimento deve se ocultar durante o estudo ativo dos cards', () => {
    const ebb = document.createElement('div');
    ebb.id = 'ebbinghaus-container';
    ebb.style.display = 'block';
    document.body.appendChild(ebb);

    Flashcards.cartaAtual = { id: 'p1', italiano: 'ciao', portugues: 'olá' };
    Flashcards.atualizarEbbinghaus();
    expect(ebb.style.display).toBe('none');

    // Ao chamar mostrarVazio(), a curva é reexibida
    Flashcards.sessaoStats = { again: 0, hard: 0, good: 0, easy: 0 };
    Flashcards.cartaAtual = null;
    Flashcards.mostrarVazio();
    expect(ebb.style.display).toBe('block');
  });
});
