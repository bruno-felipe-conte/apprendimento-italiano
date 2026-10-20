// @vitest-environment happy-dom
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { PluginManager } from '../js/core/plugins';
import { CorePlugins, registrarPluginsPadrao } from '../js/plugins/index';
import type { IPlugin } from '../types/app';

describe('EV-01: Arquitetura de Plugins (Plugin Architecture)', () => {
  let manager: PluginManager;

  beforeEach(() => {
    manager = new PluginManager();
  });

  it('deve registrar e recuperar plugins por ID', () => {
    const dummyPlugin: IPlugin = {
      id: 'test-plugin',
      name: 'Test Plugin',
      version: '1.0.0',
      init: vi.fn(),
      destroy: vi.fn()
    };

    manager.register(dummyPlugin);
    expect(manager.get('test-plugin')).toBe(dummyPlugin);
    expect(manager.getAll()).toHaveLength(1);
    expect(manager.getAll()[0].id).toBe('test-plugin');
  });

  it('deve desregistrar plugin e disparar hook destroy()', () => {
    const destroySpy = vi.fn();
    const dummyPlugin: IPlugin = {
      id: 'disposable-plugin',
      name: 'Disposable Plugin',
      init: vi.fn(),
      destroy: destroySpy
    };

    manager.register(dummyPlugin);
    expect(manager.get('disposable-plugin')).toBeDefined();

    manager.unregister('disposable-plugin');
    expect(destroySpy).toHaveBeenCalledTimes(1);
    expect(manager.get('disposable-plugin')).toBeUndefined();
    expect(manager.getAll()).toHaveLength(0);
  });

  it('deve despachar rotas registradas com sucesso', () => {
    const routeHandler = vi.fn();
    const routedPlugin: IPlugin = {
      id: 'routed-plugin',
      name: 'Routed Plugin',
      routes: [
        {
          path: 'custom-view',
          handler: routeHandler,
          title: 'Custom View'
        }
      ],
      init: vi.fn()
    };

    manager.register(routedPlugin);
    expect(manager.hasRoute('custom-view')).toBe(true);
    expect(manager.hasRoute('non-existent')).toBe(false);

    const handled = manager.dispatchRoute('custom-view', { param: 42 });
    expect(handled).toBe(true);
    expect(routeHandler).toHaveBeenCalledWith({ param: 42 });
  });

  it('deve notificar plugins de mudança de seção (onSectionChange)', () => {
    const sectionChangeSpy = vi.fn();
    const observerPlugin: IPlugin = {
      id: 'observer',
      name: 'Observer',
      init: vi.fn(),
      onSectionChange: sectionChangeSpy
    };

    manager.register(observerPlugin);
    manager.notifySectionChange('canzoni', 'flashcard');

    expect(sectionChangeSpy).toHaveBeenCalledWith('canzoni', 'flashcard');
  });

  it('deve inicializar todos os plugins com initAll() e fornecer PluginContext', async () => {
    const initSpy1 = vi.fn();
    const initSpy2 = vi.fn();

    const p1: IPlugin = { id: 'p1', name: 'P1', init: initSpy1 };
    const p2: IPlugin = { id: 'p2', name: 'P2', init: initSpy2 };

    manager.register(p1);
    manager.register(p2);

    await manager.initAll({ custom: 'app-instance' });

    expect(initSpy1).toHaveBeenCalledTimes(1);
    expect(initSpy2).toHaveBeenCalledTimes(1);
    expect(initSpy1.mock.calls[0][0]).toHaveProperty('app');
    expect(initSpy1.mock.calls[0][0]).toHaveProperty('t');
  });

  it('deve conter todos os 9 plugins essenciais do acervo no CorePlugins', () => {
    const ids = CorePlugins.map(p => p.id);
    expect(ids).toContain('flashcards');
    expect(ids).toContain('quiz');
    expect(ids).toContain('vocabolario');
    expect(ids).toContain('grammatica');
    expect(ids).toContain('storie');
    expect(ids).toContain('dialoghi');
    expect(ids).toContain('canzoni');
    expect(ids).toContain('imitazione');
    expect(ids).toContain('profilo');
    expect(CorePlugins.length).toBeGreaterThanOrEqual(9);
  });
});
