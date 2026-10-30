// @vitest-environment happy-dom
import { describe, it, expect, beforeEach } from 'vitest';
import Progressao, { LevelUp } from '../js/progression';

describe('ARC-03: Módulo de Progressão e XP em TypeScript (Progressao & LevelUp)', () => {
  beforeEach(() => {
    localStorage.clear();
    window.App = {
      estado: {
        progresso: {
          nivel: 1,
          xp: 0,
          xp_proximo_nivel: 300,
          templos_desbloqueados: [1],
          templos_concluidos: [],
          total_palavras: 20,
          streak: 0,
          ultimo_estudo: null,
          grammatica_completadas: [],
          meta_diaria: 100,
          xp_hoje: 0,
          data_xp_hoje: null,
          favoritos: [],
          conquistas: [],
          data_inicio: Date.now(),
          meta_prazo: null,
          audio_rate: 0.85
        },
        templosData: {
          1: {
            templo: 1,
            nome: 'Roma',
            palavras: [{ id: 'p1' }, { id: 'p2' }, { id: 'p3' }]
          }
        },
        flashcardData: {
          p1: { state: 'review', reps: 3, stability: 10, difficulty: 0.3 },
          p2: { state: 'review', reps: 4, stability: 15, difficulty: 0.2 },
          p3: { state: 'new', reps: 0, stability: 0, difficulty: 0 }
        }
      },
      salvarProgresso: () => {},
      atualizarStats: () => {},
      renderizarTemplos: () => {},
      notificar: () => {}
    };
  });

  it('deve calcular corretamente o limiar de XP acumulado por nível', () => {
    expect(Progressao.xpParaNivel(1)).toBe(0);
    expect(Progressao.xpParaNivel(2)).toBe(300);
    expect(Progressao.xpParaNivel(3)).toBe(700);
    expect(Progressao.xpParaNivel(4)).toBe(1200);
  });

  it('deve subir de nível e atualizar estado quando XP atinge o próximo limiar', () => {
    Progressao.ganhar(350);
    expect(window.App.estado.progresso.nivel).toBe(2);
    expect(window.App.estado.progresso.xp).toBe(350);
  });

  it('deve calcular palavras dominadas e percentual de conclusão do templo com FSRS', () => {
    // p1 e p2 têm reps >= 3 (dominadas); p3 tem reps 0
    expect(Progressao.palavrasDominadas(1)).toBe(2);
    expect(Progressao.temploConcluido(1)).toBe(false);

    // Domina p3
    window.App.estado.flashcardData.p3.reps = 3;
    expect(Progressao.palavrasDominadas(1)).toBe(3);
    expect(Progressao.temploConcluido(1)).toBe(true);
  });

  it('deve calcular estimativas matemáticas para metas com prazo', () => {
    const dataFutura = new Date(Date.now() + 10 * 86400000).toISOString().slice(0, 10);
    Progressao.definirMetaPrazo(5, dataFutura);

    const calc = Progressao.calcularMetaPrazo();
    expect(calc).not.toBeNull();
    expect(calc?.nivel_alvo).toBe(5);
    expect(calc?.diasRestantes).toBeGreaterThanOrEqual(9);
    expect(calc?.xpFaltante).toBeGreaterThan(0);
    // Sincronização automática da meta diária com o cálculo de xpPorDia
    expect(window.App.estado.progresso.meta_diaria).toBe(calc?.xpPorDia);
  });

  it('deve exportar LevelUp com métodos de inicialização e exibição', () => {
    expect(LevelUp).toBeDefined();
    expect(typeof LevelUp.mostrar).toBe('function');
    expect(typeof LevelUp.fechar).toBe('function');
  });
});
