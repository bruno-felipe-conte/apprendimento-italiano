// ============================================================
// js/core/plugins.ts — Plugin Architecture Core (EV-01)
// Permite extensibilidade modular, lazy-loading de recursos e
// desacoplamento das seções da aplicação em plugins com ciclo de vida.
// ============================================================

import type { IPlugin, PluginContext } from '../../types/app';

export class PluginManager {
  private _plugins: Map<string, IPlugin> = new Map();
  private _initialized = false;
  private _appRef: any = null;

  /**
   * Registra um novo plugin no ecossistema
   */
  register(plugin: IPlugin): void {
    if (!plugin || !plugin.id) {
      console.warn('[PluginManager] Tentativa de registrar plugin sem ID válido:', plugin);
      return;
    }

    if (this._plugins.has(plugin.id)) {
      console.warn(`[PluginManager] Plugin "${plugin.id}" já registrado. Atualizando registro.`);
      this.unregister(plugin.id);
    }

    this._plugins.set(plugin.id, plugin);

    // Se o ecossistema já estiver inicializado, inicializa o plugin imediatamente
    if (this._initialized) {
      try {
        const ctx = this._createContext();
        const res = plugin.init(ctx);
        if (res instanceof Promise) {
          res.catch((err) => console.error(`[PluginManager] Erro assíncrono ao inicializar "${plugin.id}":`, err));
        }
      } catch (err) {
        console.error(`[PluginManager] Falha ao inicializar plugin "${plugin.id}":`, err);
      }
    }
  }

  /**
   * Remove um plugin e executa seu hook destroy()
   */
  unregister(id: string): void {
    const p = this._plugins.get(id);
    if (!p) return;

    try {
      if (typeof p.destroy === 'function') {
        const res = p.destroy();
        if (res instanceof Promise) {
          res.catch((err) => console.error(`[PluginManager] Erro assíncrono ao destruir "${id}":`, err));
        }
      }
    } catch (err) {
      console.error(`[PluginManager] Erro ao desregistrar plugin "${id}":`, err);
    }

    this._plugins.delete(id);
  }

  /**
   * Obtém um plugin registrado pelo ID
   */
  get(id: string): IPlugin | undefined {
    return this._plugins.get(id);
  }

  /**
   * Retorna todos os plugins atualmente registrados
   */
  getAll(): IPlugin[] {
    return Array.from(this._plugins.values());
  }

  /**
   * Verifica se existe alguma rota registrada correspondente ao caminho
   */
  hasRoute(path: string): boolean {
    for (const plugin of this._plugins.values()) {
      if (plugin.routes?.some((r) => r.path === path)) {
        return true;
      }
    }
    return false;
  }

  /**
   * Despacha uma rota para o handler do plugin correspondente
   */
  dispatchRoute(path: string, params?: Record<string, any>): boolean {
    for (const plugin of this._plugins.values()) {
      if (!plugin.routes) continue;
      const route = plugin.routes.find((r) => r.path === path);
      if (route && typeof route.handler === 'function') {
        try {
          route.handler(params);
          return true;
        } catch (err) {
          console.error(`[PluginManager] Erro ao executar rota "${path}" no plugin "${plugin.id}":`, err);
          return false;
        }
      }
    }
    return false;
  }

  /**
   * Notifica todos os plugins que a seção ativa foi alterada
   */
  notifySectionChange(novaSecao: string, secaoAnterior: string): void {
    for (const plugin of this._plugins.values()) {
      if (typeof plugin.onSectionChange === 'function') {
        try {
          plugin.onSectionChange(novaSecao, secaoAnterior);
        } catch (err) {
          console.error(`[PluginManager] Erro em onSectionChange no plugin "${plugin.id}":`, err);
        }
      }
    }
  }

  /**
   * Inicializa todos os plugins registrados
   */
  async initAll(app?: any): Promise<void> {
    if (app) this._appRef = app;
    this._initialized = true;
    const ctx = this._createContext();

    for (const plugin of this._plugins.values()) {
      try {
        await plugin.init(ctx);
      } catch (err) {
        console.error(`[PluginManager] Falha ao inicializar "${plugin.id}":`, err);
      }
    }
  }

  /**
   * Destrói todos os plugins
   */
  async destroyAll(): Promise<void> {
    for (const plugin of this._plugins.values()) {
      try {
        if (typeof plugin.destroy === 'function') {
          await plugin.destroy();
        }
      } catch (err) {
        console.error(`[PluginManager] Erro ao destruir plugin "${plugin.id}":`, err);
      }
    }
    this._plugins.clear();
    this._initialized = false;
  }

  /**
   * Contexto seguro compartilhado com os plugins
   */
  private _createContext(): PluginContext {
    const win = typeof window !== 'undefined' ? window : ({} as any);
    return {
      app: this._appRef || win.App || null,
      state: win.AppState?.estado || win.App?.estado || null,
      navigation: win.AppNavigation || null,
      modals: win.ModalManager || null,
      t: (key: string) => (win.I18n ? win.I18n.t(key) : key)
    };
  }
}

export const AppPluginManager = new PluginManager();

if (typeof window !== 'undefined') {
  (window as any).AppPluginManager = AppPluginManager;
}
if (typeof globalThis !== 'undefined') {
  (globalThis as any).AppPluginManager = AppPluginManager;
}
