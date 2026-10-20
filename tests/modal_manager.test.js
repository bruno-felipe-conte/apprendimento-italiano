// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import ModalManager from '../js/modal_manager';

describe('ARC-04: Sistema Unificado de Modais (ModalManager)', () => {
  beforeEach(() => {
    // Reset global state
    ModalManager.stack = [];
    ModalManager._initialized = false;
    document.body.innerHTML = '';
  });

  it('deve inicializar e gerenciar a stack de modais corretamente', () => {
    const id1 = ModalManager.abrir({
      id: 'modal_test_1',
      titulo: 'Modal de Teste 1',
      html: '<p>Conteúdo 1</p>'
    });

    expect(ModalManager.stack.length).toBe(1);
    expect(ModalManager.stack[0].id).toBe('modal_test_1');

    const id2 = ModalManager.abrir({
      id: 'modal_test_2',
      titulo: 'Modal de Teste 2',
      html: '<p>Conteúdo 2</p>'
    });

    expect(id2).toBe('modal_test_2');
    expect(ModalManager.stack.length).toBe(2);
    expect(ModalManager.stack[1].id).toBe('modal_test_2');

    // Fechar topo deve fechar o id2
    ModalManager.fecharTopo();
    expect(ModalManager.stack.length).toBe(1);
    expect(ModalManager.stack[0].id).toBe('modal_test_1');

    // Fechar id1
    ModalManager.fechar(id1);
    expect(ModalManager.stack.length).toBe(0);
  });

  it('deve criar elementos acessíveis com atributos ARIA', () => {
    ModalManager.abrir({
      id: 'modal_a11y',
      titulo: 'Acessibilidade WCAG',
      html: '<input id="nome_input" type="text" />'
    });

    const overlay = document.getElementById('modal_overlay_modal_a11y');
    expect(overlay).not.toBeNull();
    expect(overlay.getAttribute('role')).toBe('dialog');
    expect(overlay.getAttribute('aria-modal')).toBe('true');
    expect(overlay.getAttribute('aria-labelledby')).toBe('modal_title_modal_a11y');

    const title = document.getElementById('modal_title_modal_a11y');
    expect(title.textContent).toBe('Acessibilidade WCAG');
  });

  it('deve fechar ao acionar tecla Escape', () => {
    ModalManager.abrir({
      id: 'modal_esc',
      titulo: 'Fechar no ESC',
      html: '<p>Texto</p>'
    });

    expect(ModalManager.stack.length).toBe(1);

    // Dispara evento Escape
    const event = new KeyboardEvent('keydown', { key: 'Escape' });
    window.dispatchEvent(event);

    expect(ModalManager.stack.length).toBe(0);
  });
});
