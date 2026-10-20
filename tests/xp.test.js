// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import AppState from '../js/core/state.js';
import AppXP from '../js/core/xp.js';
import App from '../js/core.js';

describe('ARC-02: Submódulo de XP e Progressão (AppXP & App Facade)', () => {
  beforeEach(() => {
    localStorage.clear();
    AppState.estado.progresso = {
      nivel: 1,
      xp: 100,
      xp_proximo_nivel: 500,
      templos_desbloqueados: [1],
      total_palavras: 20,
      streak: 1,
      meta_diaria: 100,
      xp_hoje: 20
    };

    document.body.innerHTML = `
      <div id="stat-xp">XP: 100/500</div>
      <div id="stat-nivel">Livello 1</div>
      <div id="toast-container"></div>
    `;
  });

  it('deve adicionar XP corretamente em modo fallback e salvar progresso', () => {
    // Garante que Progressao global não exista neste teste unitário isolado
    delete global.Progressao;

    AppXP.ganharXP(50);

    expect(AppState.estado.progresso.xp).toBe(150);
    const salvo = JSON.parse(localStorage.getItem('it_progresso') || '{}');
    expect(salvo.xp).toBe(150);
  });

  it('deve aplicar classe de animação otimista no contador de XP', () => {
    const elXp = document.getElementById('stat-xp');
    expect(elXp.classList.contains('optimistic-xp-pulse')).toBe(false);

    AppXP.ganharXP(25);
    expect(elXp.classList.contains('optimistic-xp-pulse')).toBe(true);
  });

  it('deve delegar para Progressao.ganhar quando o módulo estiver ativo', () => {
    let chamadoCom = null;
    global.Progressao = {
      ganhar: (qtd) => { chamadoCom = qtd; }
    };

    AppXP.ganharXP(75);
    expect(chamadoCom).toBe(75);

    delete global.Progressao;
  });

  it('deve funcionar perfeitamente através do facade App.ganharXP', () => {
    delete global.Progressao;

    App.ganharXP(100);
    expect(App.estado.progresso.xp).toBe(200);
    expect(AppState.estado.progresso.xp).toBe(200);
  });
});
