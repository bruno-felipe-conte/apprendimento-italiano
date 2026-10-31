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

export interface StaticModalConfig {
  id: string;
  isOpen: (el: HTMLElement) => boolean;
  close: (el: HTMLElement) => void;
}

export const ModalManager = {
  stack: [] as ModalItem[],
  _initialized: false,
  _previouslyFocused: null as HTMLElement | null,
  _staticModalPreviousFocus: new Map<HTMLElement, HTMLElement | null>(),
  _staticConfigs: [
    {
      id: 'templo-modal',
      isOpen: (el: HTMLElement) => el.classList.contains('ativo') || el.classList.contains('show'),
      close: (el: HTMLElement) => {
        const app = (typeof window !== 'undefined' ? (window as any).App : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).App : null);
        const appTemploModal = (typeof window !== 'undefined' ? (window as any).AppTemploModal : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).AppTemploModal : null);
        if (app && typeof app.fecharModalTemplo === 'function') app.fecharModalTemplo();
        else if (appTemploModal && typeof appTemploModal.fecharModalTemplo === 'function') appTemploModal.fecharModalTemplo();
        else el.classList.remove('ativo', 'show');
      }
    },
    {
      id: 'conquista-modal',
      isOpen: (el: HTMLElement) => el.classList.contains('ativo') || el.classList.contains('show'),
      close: (el: HTMLElement) => {
        const conquistas = (typeof window !== 'undefined' ? (window as any).Conquistas : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).Conquistas : null);
        if (conquistas && typeof conquistas.fecharModal === 'function') conquistas.fecharModal();
        else el.classList.remove('ativo', 'show');
      }
    },
    {
      id: 'levelup-modal',
      isOpen: (el: HTMLElement) => el.classList.contains('ativo') || el.classList.contains('show'),
      close: (el: HTMLElement) => {
        const levelUp = (typeof window !== 'undefined' ? (window as any).LevelUp : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).LevelUp : null);
        const appProg = (typeof window !== 'undefined' ? (window as any).AppProgression : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).AppProgression : null);
        if (levelUp && typeof levelUp.fechar === 'function') levelUp.fechar();
        else if (appProg && typeof appProg.fecharLevelUpModal === 'function') appProg.fecharLevelUpModal();
        else el.classList.remove('ativo', 'show');
      }
    },
    {
      id: 'onboarding-modal',
      isOpen: (el: HTMLElement) => el.style.display !== 'none' && !el.hasAttribute('hidden'),
      close: (el: HTMLElement) => {
        const onboarding = (typeof window !== 'undefined' ? (window as any).Onboarding : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).Onboarding : null);
        if (onboarding && typeof onboarding.fechar === 'function') onboarding.fechar();
        else if (onboarding && typeof onboarding.pular === 'function') onboarding.pular();
        else el.style.display = 'none';
      }
    },
    {
      id: 'modal-meta-prazo',
      isOpen: (el: HTMLElement) => el.style.display !== 'none' && !el.hasAttribute('hidden'),
      close: (el: HTMLElement) => {
        const app = (typeof window !== 'undefined' ? (window as any).App : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).App : null);
        const appMeta = (typeof window !== 'undefined' ? (window as any).AppMeta : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).AppMeta : null);
        if (app && typeof app.fecharModalMetaPrazo === 'function') app.fecharModalMetaPrazo();
        else if (appMeta && typeof appMeta.fecharModalMetaPrazo === 'function') appMeta.fecharModalMetaPrazo();
        else el.style.display = 'none';
      }
    },
    {
      id: 'ia-import-modal',
      isOpen: (el: HTMLElement) => el.style.display !== 'none' && !el.hasAttribute('hidden'),
      close: (el: HTMLElement) => {
        const iaImport = (typeof window !== 'undefined' ? (window as any).IAImport : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).IAImport : null);
        if (iaImport && typeof iaImport.fechar === 'function') iaImport.fechar();
        else el.style.display = 'none';
      }
    },
    {
      id: 'meta-settings-modal',
      isOpen: (el: HTMLElement) => el.classList.contains('ativo') || el.classList.contains('show'),
      close: (el: HTMLElement) => {
        const app = (typeof window !== 'undefined' ? (window as any).App : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).App : null);
        const appMeta = (typeof window !== 'undefined' ? (window as any).AppMeta : null) || (typeof globalThis !== 'undefined' ? (globalThis as any).AppMeta : null);
        if (app && typeof app.fecharMetaSettings === 'function') app.fecharMetaSettings();
        else if (appMeta && typeof appMeta.fecharMetaSettings === 'function') appMeta.fecharMetaSettings();
        else el.classList.remove('ativo', 'show');
      }
    }
  ] as StaticModalConfig[],

  getOpenStaticModal(): HTMLElement | null {
    if (typeof document === 'undefined') return null;
    for (const cfg of this._staticConfigs) {
      const el = document.getElementById(cfg.id);
      if (el && cfg.isOpen(el)) return el;
    }
    const generic = document.querySelector<HTMLElement>(
      '.modal.ativo, .modal.show, .templo-modal.ativo, .conquista-modal.ativo, .levelup-modal.ativo, .meta-settings-modal.ativo, dialog[open]'
    );
    return generic;
  },

  fecharModalEstatico(modalEl: HTMLElement): boolean {
    if (!modalEl) return false;
    const cfg = this._staticConfigs.find(c => c.id === modalEl.id);
    if (cfg) {
      cfg.close(modalEl);
    } else if (modalEl.tagName === 'DIALOG' && typeof (modalEl as any).close === 'function') {
      (modalEl as any).close();
    } else {
      modalEl.classList.remove('ativo', 'show');
      modalEl.style.display = 'none';
    }
    const previous = this._staticModalPreviousFocus.get(modalEl);
    if (previous && typeof previous.focus === 'function') {
      previous.focus();
      this._staticModalPreviousFocus.delete(modalEl);
    }
    return true;
  },

  init(): void {
    if (this._initialized || typeof window === 'undefined') return;
    this._initialized = true;

    // Listener global para fechar modais com Escape e prender foco com Tab (F18)
    window.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (this.stack.length > 0) {
          e.preventDefault();
          this.fecharTopo();
          return;
        }
        const openStatic = this.getOpenStaticModal();
        if (openStatic) {
          e.preventDefault();
          this.fecharModalEstatico(openStatic);
          return;
        }
      }

      if (e.key === 'Tab') {
        let activeContainer: HTMLElement | null = null;
        if (this.stack.length > 0) {
          activeContainer = this.stack[this.stack.length - 1].box;
        } else {
          activeContainer = this.getOpenStaticModal();
        }

        if (activeContainer) {
          const focaveis = this._obterFocaveis(activeContainer);
          if (focaveis.length === 0) {
            e.preventDefault();
            return;
          }
          const primeiro = focaveis[0];
          const ultimo = focaveis[focaveis.length - 1];

          if (e.shiftKey) {
            if (document.activeElement === primeiro || !activeContainer.contains(document.activeElement)) {
              e.preventDefault();
              ultimo.focus();
            }
          } else {
            if (document.activeElement === ultimo || !activeContainer.contains(document.activeElement)) {
              e.preventDefault();
              primeiro.focus();
            }
          }
        }
      }
    });

    this._setupStaticModalObserver();
  },

  _setupStaticModalObserver(): void {
    if (typeof document === 'undefined' || typeof MutationObserver === 'undefined') return;

    const modalIds = this._staticConfigs.map(c => c.id);
    const isModalOpen = (el: HTMLElement) => {
      const cfg = this._staticConfigs.find(c => c.id === el.id);
      return cfg ? cfg.isOpen(el) : (el.classList.contains('ativo') || el.classList.contains('show') || (el.style.display !== 'none' && !el.hasAttribute('hidden')));
    };

    const previousStates = new Map<HTMLElement, boolean>();

    const checkModal = (el: HTMLElement) => {
      const wasOpen = previousStates.get(el) || false;
      const nowOpen = isModalOpen(el);
      if (nowOpen && !wasOpen) {
        previousStates.set(el, true);
        if (document.activeElement && !el.contains(document.activeElement)) {
          this._staticModalPreviousFocus.set(el, document.activeElement as HTMLElement);
        }
        setTimeout(() => {
          const focaveis = this._obterFocaveis(el);
          if (focaveis.length > 0) focaveis[0].focus();
        }, 30);
      } else if (!nowOpen && wasOpen) {
        previousStates.set(el, false);
        const prev = this._staticModalPreviousFocus.get(el);
        if (prev && typeof prev.focus === 'function') {
          prev.focus();
          this._staticModalPreviousFocus.delete(el);
        }
      }
    };

    const observer = new MutationObserver((mutations) => {
      for (const m of mutations) {
        const target = m.target as HTMLElement;
        if (target && (modalIds.includes(target.id) || target.classList?.contains('modal') || target.classList?.contains('templo-modal') || target.getAttribute?.('role') === 'dialog')) {
          checkModal(target);
        }
      }
    });

    try {
      if (document.body) {
        observer.observe(document.body, {
          attributes: true,
          attributeFilter: ['class', 'style', 'open', 'hidden'],
          subtree: true
        });
      }
    } catch (_) {}
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
  },

  // Vincula focus trap, Escape e restauração de foco a modais estáticos do DOM
  bindStaticModal(modalEl: HTMLElement | null, onclose?: () => void): () => void {
    if (!modalEl || typeof document === 'undefined') return () => {};
    this.init();
    const previousFocus = document.activeElement as HTMLElement | null;
    if (previousFocus) this._staticModalPreviousFocus.set(modalEl, previousFocus);

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        if (typeof onclose === 'function') onclose();
        else this.fecharModalEstatico(modalEl);
        if (previousFocus && typeof previousFocus.focus === 'function') previousFocus.focus();
        return;
      }
      if (e.key === 'Tab') {
        const focaveis = this._obterFocaveis(modalEl);
        if (focaveis.length === 0) { e.preventDefault(); return; }
        const primeiro = focaveis[0];
        const ultimo = focaveis[focaveis.length - 1];
        if (e.shiftKey && (document.activeElement === primeiro || !modalEl.contains(document.activeElement))) {
          e.preventDefault();
          ultimo.focus();
        } else if (!e.shiftKey && (document.activeElement === ultimo || !modalEl.contains(document.activeElement))) {
          e.preventDefault();
          primeiro.focus();
        }
      }
    };

    modalEl.addEventListener('keydown', onKeyDown);
    const focaveis = this._obterFocaveis(modalEl);
    if (focaveis.length > 0) focaveis[0].focus();

    return () => {
      modalEl.removeEventListener('keydown', onKeyDown);
      if (previousFocus && typeof previousFocus.focus === 'function') previousFocus.focus();
    };
  }
};

if (typeof window !== 'undefined') {
  window.ModalManager = ModalManager;
}
if (typeof globalThis !== 'undefined') {
  (globalThis as any).ModalManager = ModalManager;
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => ModalManager.init());
  } else {
    ModalManager.init();
  }
}

export default ModalManager;
