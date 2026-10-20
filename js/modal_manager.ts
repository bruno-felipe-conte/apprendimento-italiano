// ============================================================
// js/modal_manager.ts — Sistema Unificado de Modais (ARC-03 / ARC-04)
// Gerenciador singleton com stack, trap de foco, acessibilidade
// WCAG 2.1 AA, tecla ESC e clique fora.
// ============================================================

export interface ModalAcao {
  texto?: string;
  classe?: string;
  primario?: boolean;
  onclick?: (id: string) => void;
}

export interface ModalOpcoes {
  id?: string;
  titulo?: string;
  html?: string;
  acoes?: ModalAcao[];
  fecharAoClicarFora?: boolean;
  tamanho?: 'pequeno' | 'medio' | 'grande';
  onclose?: () => void;
}

export interface ModalItem {
  id: string;
  overlay: HTMLDivElement;
  box: HTMLDivElement;
  onclose?: () => void;
}

export const ModalManager = {
  stack: [] as ModalItem[],
  _initialized: false,
  _previouslyFocused: null as HTMLElement | null,

  init(): void {
    if (this._initialized || typeof window === 'undefined') return;
    this._initialized = true;

    // Listener global para fechar o modal do topo com tecla Escape
    window.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Escape' && this.stack.length > 0) {
        e.preventDefault();
        this.fecharTopo();
      }
    });
  },

  // Retorna os elementos focáveis dentro de um container
  _obterFocaveis(el: HTMLElement | null): HTMLElement[] {
    if (!el) return [];
    return Array.from(
      el.querySelectorAll<HTMLElement>(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    );
  },

  // Prende a navegação por Tab no modal ativo (Focus Trap)
  _ativarFocusTrap(modalEl: HTMLElement): void {
    modalEl.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;
      const focaveis = this._obterFocaveis(modalEl);
      if (focaveis.length === 0) {
        e.preventDefault();
        return;
      }
      const primeiro = focaveis[0];
      const ultimo = focaveis[focaveis.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === primeiro) {
          e.preventDefault();
          ultimo.focus();
        }
      } else {
        if (document.activeElement === ultimo) {
          e.preventDefault();
          primeiro.focus();
        }
      }
    });
  },

  abrir(opts: ModalOpcoes = {}): string {
    this.init();
    const id = opts.id || `modal_${Date.now()}`;
    this.fechar(id); // Evita duplicata se já aberto

    if (typeof document !== 'undefined') {
      this._previouslyFocused = document.activeElement as HTMLElement | null;
    }

    const overlay = document.createElement('div');
    overlay.id = `modal_overlay_${id}`;
    overlay.className = 'modal-manager-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', `modal_title_${id}`);
    overlay.style.cssText = `
      position: fixed; inset: 0; background: rgba(20, 10, 5, 0.65);
      backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
      z-index: ${2000 + this.stack.length * 10};
      display: flex; align-items: center; justify-content: center;
      padding: 1rem; opacity: 0; transition: opacity 0.2s ease;
    `;

    const maxW = opts.tamanho === 'pequeno' ? '380px' : (opts.tamanho === 'grande' ? '720px' : '520px');

    const box = document.createElement('div');
    box.className = 'modal-manager-box';
    box.style.cssText = `
      background: var(--cor-marmore, #FAF7F2);
      border: 2px solid var(--cor-toscano, #C9952A);
      border-radius: 16px; width: 100%; max-width: ${maxW};
      box-shadow: 0 16px 40px rgba(0,0,0,0.35); overflow: hidden;
      transform: scale(0.95); transition: transform 0.2s ease;
      display: flex; flex-direction: column; max-height: 85vh;
    `;

    // Cabeçalho
    const header = document.createElement('div');
    header.style.cssText = `
      background: linear-gradient(135deg, #9B2335 0%, #6B1525 100%);
      color: #F5EDD8; padding: 0.85rem 1.25rem; display: flex;
      align-items: center; justify-content: space-between;
    `;
    const titleEl = document.createElement('h3');
    titleEl.id = `modal_title_${id}`;
    titleEl.style.cssText = "font-family:'Cinzel',serif; font-size:1.05rem; font-weight:700; margin:0;";
    titleEl.textContent = opts.titulo || '';

    const closeBtn = document.createElement('button');
    closeBtn.setAttribute('aria-label', 'Fechar modal');
    closeBtn.style.cssText = 'background:none; border:none; color:#F5EDD8; font-size:1.25rem; cursor:pointer; padding:0 0.2rem;';
    closeBtn.textContent = '✕';
    closeBtn.onclick = () => this.fechar(id);

    header.appendChild(titleEl);
    header.appendChild(closeBtn);

    // Corpo
    const body = document.createElement('div');
    body.className = 'modal-manager-body';
    body.style.cssText = 'padding: 1.25rem; overflow-y: auto; color: var(--cor-inchiostro, #2E1B0E); line-height: 1.5;';
    body.innerHTML = opts.html || '';

    // Rodapé de Ações
    let footer: HTMLDivElement | null = null;
    if (Array.isArray(opts.acoes) && opts.acoes.length > 0) {
      footer = document.createElement('div');
      footer.style.cssText = `
        padding: 0.75rem 1.25rem; background: var(--cor-marmore-escuro, #EDE5D8);
        display: flex; gap: 0.5rem; justify-content: flex-end; flex-wrap: wrap;
      `;
      for (const acao of opts.acoes) {
        const btn = document.createElement('button');
        btn.textContent = acao.texto || 'OK';
        btn.className = acao.classe || (acao.primario ? 'btn-primario' : 'btn-secondario');
        btn.style.cssText = 'padding: 0.45rem 1.1rem; border-radius: 8px; font-weight: 600; cursor: pointer; font-size: 0.9rem;';
        btn.onclick = () => {
          if (typeof acao.onclick === 'function') acao.onclick(id);
          else this.fechar(id);
        };
        footer.appendChild(btn);
      }
    }

    box.appendChild(header);
    box.appendChild(body);
    if (footer) box.appendChild(footer);
    overlay.appendChild(box);

    if (opts.fecharAoClicarFora !== false) {
      overlay.addEventListener('click', (e: MouseEvent) => {
        if (e.target === overlay) this.fechar(id);
      });
    }

    this._ativarFocusTrap(box);
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';

    // Animação de entrada
    requestAnimationFrame(() => {
      overlay.style.opacity = '1';
      box.style.transform = 'scale(1)';
      const focaveis = this._obterFocaveis(box);
      if (focaveis.length > 0) focaveis[0].focus();
    });

    this.stack.push({ id, overlay, box, onclose: opts.onclose });
    return id;
  },

  fechar(id: string): void {
    const idx = this.stack.findIndex(m => m.id === id);
    if (idx === -1) return;

    const item = this.stack[idx];
    this.stack.splice(idx, 1);

    item.overlay.style.opacity = '0';
    item.box.style.transform = 'scale(0.95)';

    setTimeout(() => {
      item.overlay.remove();
      if (typeof item.onclose === 'function') item.onclose();
      if (this.stack.length === 0 && typeof document !== 'undefined') {
        document.body.style.overflow = '';
        if (this._previouslyFocused && typeof this._previouslyFocused.focus === 'function') {
          this._previouslyFocused.focus();
        }
      }
    }, 200);
  },

  fecharTopo(): void {
    if (this.stack.length > 0) {
      const topo = this.stack[this.stack.length - 1];
      this.fechar(topo.id);
    }
  }
};

if (typeof window !== 'undefined') {
  window.ModalManager = ModalManager;
}
if (typeof globalThis !== 'undefined') {
  (globalThis as any).ModalManager = ModalManager;
}

export default ModalManager;
