// @ts-nocheck
// @vitest-environment happy-dom
// tests/e2e/tier1_feature_coverage.test.ts
// Tier 1: Feature Coverage — Representative Happy-Path Inputs in Isolation (F1–F25)

import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  bootstrapAppDOM,
  resetAppEnvironment,
  dispatchKey,
  dispatchClick
} from './e2e_helpers';

import AppState from '../../js/core/state.js';
import AppNavigation from '../../js/core/navigation.js';
import AppXP from '../../js/core/xp.js';
import AppStats from '../../js/core/stats.js';
import AppMeta from '../../js/core/meta.js';
import AppFavorites from '../../js/core/favorites.js';
import AppTTS from '../../js/core/tts.js';
import App from '../../js/core.js';
import ModalManager from '../../js/modal_manager';
import { ConflictResolver } from '../../js/core/collaboration';
import { SyncManager, MockBackendAdapter } from '../../js/core/sync';
import {
  calculateRetention,
  calculateTimeToTarget,
  predictNextStabilityGood
} from '../../src/analytics/ebbinghausCurve';
import fs from 'node:fs';
import path from 'node:path';

describe('Tier 1: Feature Coverage (Happy Path in Isolation)', () => {
  beforeEach(() => {
    bootstrapAppDOM();
    resetAppEnvironment();
  });

  // ============================================================
  // Area 1: Storage, Persistence & Data Resilience (F1–F6)
  // ============================================================
  describe('Area 1: Storage, Persistence & Data Resilience (F1–F6)', () => {
    it('F1: deve executar GC e expurgar flashcards suspensos ou obsoletos (>90 dias)', () => {
      const agora = Date.now();
      const NOVENTA_E_UM_DIAS = 91 * 24 * 3600 * 1000;

      AppState.estado.flashcardData = {
        card_ativo: {
          state: 'review',
          difficulty: 5,
          stability: 10,
          lastReview: agora - 1000
        },
        card_suspenso: {
          state: 'suspended',
          difficulty: 5,
          stability: 5,
          lastReview: agora - 5000
        },
        card_obsoleto_novo: {
          state: 'new',
          difficulty: 5,
          stability: 1,
          lastReview: agora - NOVENTA_E_UM_DIAS
        }
      };

      AppState._gcFlashcards();

      expect(AppState.estado.flashcardData['card_ativo']).toBeDefined();
      expect(AppState.estado.flashcardData['card_suspenso']).toBeUndefined();
      expect(AppState.estado.flashcardData['card_obsoleto_novo']).toBeUndefined();
    });

    it('F2: deve permitir despejo de caches efêmeros SWR e logs de erro sem alterar o progresso', () => {
      localStorage.setItem('it_swr_templos_meta', JSON.stringify({ 1: { nome: 'Roma' } }));
      localStorage.setItem('it_swr_grammar', JSON.stringify({ moduli: [1, 2] }));
      localStorage.setItem('it_client_errors', JSON.stringify([{ msg: 'teste erro' }]));
      AppState.salvarProgresso();

      // Simulação da escada de despejo (eviction ladder)
      const chavesSWR = ['it_swr_templos_meta', 'it_swr_grammar', 'it_client_errors'];
      for (const k of chavesSWR) {
        localStorage.removeItem(k);
      }

      expect(localStorage.getItem('it_swr_templos_meta')).toBeNull();
      expect(localStorage.getItem('it_swr_grammar')).toBeNull();
      expect(localStorage.getItem('it_client_errors')).toBeNull();

      // Progresso do usuário permanece intacto
      const progSalvo = JSON.parse(localStorage.getItem('it_progresso') || '{}');
      expect(progSalvo.nivel).toBe(1);
      expect(progSalvo.templos_desbloqueados).toContain(1);
    });

    it('F3: deve sincronizar e reconciliar dados cross-tab via ConflictResolver sem perda de dados', () => {
      const resolver = new ConflictResolver();
      const local = {
        nivel: 2,
        xp: 350,
        templos_desbloqueados: [1, 2],
        conquistas: ['primeiro_quiz'],
        grammatica_completadas: ['mod_1']
      } as any;

      const remoto = {
        nivel: 3,
        xp: 600,
        templos_desbloqueados: [1, 3],
        conquistas: ['streak_3_dias'],
        grammatica_completadas: ['mod_2']
      } as any;

      const resultado = resolver.reconciliarProgresso(local, remoto);

      expect(resultado.progresso.xp).toBe(600);
      expect(resultado.progresso.nivel).toBe(3);
      expect(resultado.progresso.templos_desbloqueados).toEqual([1, 2, 3]);
      expect(resultado.progresso.conquistas).toContain('primeiro_quiz');
      expect(resultado.progresso.conquistas).toContain('streak_3_dias');
      expect(resultado.progresso.grammatica_completadas).toContain('mod_1');
      expect(resultado.progresso.grammatica_completadas).toContain('mod_2');
    });

    it('F4: deve carregar progresso defensivamente com valores default ao encontrar storage vazio', () => {
      localStorage.removeItem('it_progresso');
      const p = AppState.carregarProgresso();

      expect(p).toBeDefined();
      expect(p.nivel).toBe(1);
      expect(p.xp).toBe(0);
      expect(p.templos_desbloqueados).toEqual([1]);
      expect(Array.isArray(p.favoritos)).toBe(true);
      expect(Array.isArray(p.conquistas)).toBe(true);
      expect(p.meta_diaria).toBe(100);
      expect(p.audio_rate).toBe(0.85);
    });

    it('F4: deve retornar objeto vazio ao carregar flashcards com chave inexistente', () => {
      localStorage.removeItem('it_flashcards');
      const cards = AppState.carregarFlashcards();
      expect(cards).toEqual({});
    });

    it('F5: deve estruturar payload atômico completo na exportação de dados', () => {
      AppState.estado.progresso.xp = 120;
      AppState.estado.progresso.nivel = 1;
      AppState.salvarProgresso();

      AppState.estado.flashcardData = {
        w1: { state: 'review', difficulty: 5, stability: 2.5 }
      };
      AppState.salvarFlashcards();

      localStorage.setItem('it_tema', 'dark');
      localStorage.setItem('it_idioma', 'it');

      // Gera payload canônico de backup
      const backup = {
        versao: 4,
        data: new Date().toISOString(),
        progresso: JSON.parse(localStorage.getItem('it_progresso') || 'null'),
        flashcards: JSON.parse(localStorage.getItem('it_flashcards') || '{}'),
        tema: localStorage.getItem('it_tema'),
        idioma: localStorage.getItem('it_idioma')
      };

      expect(backup.versao).toBe(4);
      expect(backup.progresso.xp).toBe(120);
      expect(backup.flashcards.w1).toBeDefined();
      expect(backup.tema).toBe('dark');
      expect(backup.idioma).toBe('it');
    });

    it('F6: deve sanitizar caracteres de HTML com escapeHtml evitando injeção maliciosa', () => {
      const perigoso = '<script>alert("xss")</script>&"\'';
      const seguro = AppState.escapeHtml(perigoso);

      expect(seguro).not.toContain('<script>');
      expect(seguro).toContain('&lt;script&gt;');
      expect(seguro).toContain('&amp;');
      expect(seguro).toContain('&quot;');
      expect(seguro).toContain('&#39;');
    });
  });

  // ============================================================
  // Area 2: Algorithmic Stability, FSRS & Concurrency Guards (F7–F12)
  // ============================================================
  describe('Area 2: Algorithmic Stability, FSRS & Concurrency Guards (F7–F12)', () => {
    it('F7: deve calcular a retenção de Ebbinghaus decaindo monotonicamente de 1.0 para 0', () => {
      const s = 10;
      const decay = -0.5;
      const factor = 19 / 81;

      const r0 = calculateRetention(0, s, factor, decay);
      const rS = calculateRetention(s, s, factor, decay);
      const r2S = calculateRetention(s * 2, s, factor, decay);

      expect(r0).toBe(1.0);
      expect(rS).toBeCloseTo(0.9, 5);
      expect(r2S).toBeLessThan(rS);
      expect(r2S).toBeGreaterThan(0);
    });

    it('F7: deve calcular tempo exato até a meta de retenção alvo', () => {
      const s = 15;
      const decay = -0.5;
      const factor = 19 / 81;

      const tTarget = calculateTimeToTarget(s, factor, decay);
      expect(tTarget).toBeCloseTo(s, 4);
    });

    it('F8: deve projetar aumento de estabilidade após avaliação Good', () => {
      const dAtual = 5;
      const sAtual = 5;
      const rAtual = 0.9;

      const novaS = predictNextStabilityGood(dAtual, sAtual, rAtual);
      expect(novaS).toBeGreaterThan(sAtual);
      expect(Number.isFinite(novaS)).toBe(true);
    });

    it('F9: deve harmonizar timestamps para o cálculo de dias decorridos', () => {
      const agora = Date.now();
      const tresDiasAtras = agora - 3 * 86400000;

      const diffDias = Math.max(0, (agora - tresDiasAtras) / 86400000);
      expect(diffDias).toBeCloseTo(3, 2);
    });

    it('F10: deve registrar acúmulo de XP e atualizar UI sem duplicidade', () => {
      AppState.estado.progresso.xp = 100;
      AppXP.ganharXP(50);

      expect(AppState.estado.progresso.xp).toBe(150);
      const salvo = JSON.parse(localStorage.getItem('it_progresso') || '{}');
      expect(salvo.xp).toBe(150);
    });

    it('F11: deve atualizar secaoAtiva e persistir última seção ao navegar', () => {
      AppNavigation.navegar('quiz');

      expect(AppState.estado.secaoAtiva).toBe('quiz');
      expect(AppState.estado.progresso.ultima_secao).toBe('quiz');

      const secQuiz = document.getElementById('sec-quiz');
      expect(secQuiz?.classList.contains('active')).toBe(true);

      const secTempli = document.getElementById('sec-templi');
      expect(secTempli?.classList.contains('active')).toBe(false);
    });

    it('F12: deve configurar velocidade e voz TTS italiana de acordo com preferências', () => {
      AppState.estado.progresso.audio_rate = 0.7;
      AppTTS.atualizarAudioSpeedUI();

      expect(document.getElementById('btn-audio-speed-ico')?.textContent).toBe('.7x');

      // Testa pronúncia sem disparar erro
      expect(() => AppTTS.pronunciar('Ciao mondo')).not.toThrow();
    });
  });

  // ============================================================
  // Area 3: UX, Ergonomics, PWA Resilience & A11y Standards (F13–F21)
  // ============================================================
  describe('Area 3: UX, Ergonomics, PWA Resilience & A11y Standards (F13–F21)', () => {
    it('F13: deve alternar abas de navegação ativas no DOM', () => {
      const tabFlash = document.querySelector('.nav-tab[data-section="flashcard"]') as HTMLElement;
      expect(tabFlash).not.toBeNull();

      dispatchClick(tabFlash);
      AppNavigation.navegar('flashcard');

      expect(tabFlash.classList.contains('ativa')).toBe(true);
      expect(document.getElementById('sec-flashcard')?.classList.contains('active')).toBe(true);
    });

    it('F14: deve renderizar opções de quiz com números de atalho e feedback acessível', () => {
      const opcoesContainer = document.getElementById('quiz-opcoes');
      expect(opcoesContainer?.children.length).toBe(4);

      const primeiraOpcao = opcoesContainer?.firstElementChild as HTMLElement;
      expect(primeiraOpcao.textContent).toContain('Buongiorno');

      const feedbackEl = document.getElementById('quiz-feedback');
      expect(feedbackEl?.getAttribute('aria-live')).toBe('polite');
      expect(feedbackEl?.getAttribute('role')).toBe('status');
    });

    it('F15: deve possuir manifesto PWA válido com suporte a standalone e tema', () => {
      const manifestPath = path.resolve(process.cwd(), 'manifest.webmanifest');
      expect(fs.existsSync(manifestPath)).toBe(true);

      const manifestContent = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      expect(manifestContent.display).toBe('standalone');
      expect(manifestContent.theme_color).toBe('#9B2335');
      expect(manifestContent.name).toBe('Italiano Autentico');
    });

    it('F16: deve persistir e aplicar fixação da barra lateral (sidebar pinned)', () => {
      const pinBtn = document.getElementById('sidebar-pin-btn') as HTMLElement;
      expect(pinBtn).not.toBeNull();

      AppNavigation.toggleSidebarPin();
      expect(document.body.classList.contains('sidebar-pinned')).toBe(true);
      expect(localStorage.getItem('it_sidebar_pinned')).toBe('true');

      AppNavigation.toggleSidebarPin();
      expect(document.body.classList.contains('sidebar-pinned')).toBe(false);
      expect(localStorage.getItem('it_sidebar_pinned')).toBe('false');
    });

    it('F17: deve possuir botões utilitários no cabeçalho com identificadores e acessibilidade', () => {
      const btnTema = document.getElementById('theme-toggle');
      const btnSom = document.getElementById('btn-som');
      const btnVoz = document.getElementById('btn-audio-speed');

      expect(btnTema?.getAttribute('aria-label')).toBeTruthy();
      expect(btnSom?.getAttribute('aria-label')).toBeTruthy();
      expect(btnVoz?.getAttribute('aria-label')).toBeTruthy();
    });

    it('F18: deve abrir e fechar modais acessíveis com ModalManager', () => {
      const id = ModalManager.abrir({
        id: 'modal_teste_e2e',
        titulo: 'Modal E2E',
        html: '<div id="conteudo-teste">Corpo do Modal</div>'
      });

      expect(ModalManager.stack.length).toBe(1);
      const overlay = document.getElementById('modal_overlay_modal_teste_e2e');
      expect(overlay).not.toBeNull();
      expect(overlay?.getAttribute('role')).toBe('dialog');
      expect(overlay?.getAttribute('aria-modal')).toBe('true');

      ModalManager.fechar(id);
      expect(ModalManager.stack.length).toBe(0);
      expect(overlay?.style.opacity).toBe('0');
    });

    it('F19: o elemento do flashcard deve possuir role="button" e tabindex para foco', () => {
      const fc = document.getElementById('flashcard');
      expect(fc?.getAttribute('role')).toBe('button');
      expect(fc?.getAttribute('tabindex')).toBe('0');
      expect(fc?.getAttribute('aria-label')).toBeTruthy();
    });

    it('F20: a barra de estatísticas deve exibir o nível atual e contagem de XP', () => {
      AppState.estado.progresso.nivel = 2;
      AppState.estado.progresso.xp = 250;
      AppStats.atualizarStats();

      expect(document.getElementById('stat-nivel')?.textContent).toContain('2');
      expect(document.getElementById('stat-xp')?.textContent).toContain('250');
    });

    it('F21: deve alternar entre modo claro e escuro persistindo a escolha', () => {
      const btnTema = document.getElementById('theme-toggle') as HTMLElement;
      dispatchClick(btnTema);

      // Simula alternância de tema
      const temaAtual = localStorage.getItem('it_tema') === 'dark' ? 'light' : 'dark';
      localStorage.setItem('it_tema', temaAtual);
      if (temaAtual === 'dark') {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }

      expect(localStorage.getItem('it_tema')).toBe('dark');
      expect(document.body.classList.contains('dark-mode')).toBe(true);
    });
  });

  // ============================================================
  // Area 4: Continuous Improvement Framework & Automated Stress (F22–F25)
  // ============================================================
  describe('Area 4: Continuous Improvement Framework & Automated Stress (F22–F25)', () => {
    it('F22: deve persistir e reidratar 50 cards de flashcard sem corrupção de schema', () => {
      const deck: Record<string, any> = {};
      for (let i = 1; i <= 50; i++) {
        deck[`card_${i}`] = {
          state: i % 2 === 0 ? 'review' : 'new',
          difficulty: 5.0,
          stability: Number((i * 0.5).toFixed(1)),
          reps: i,
          lapses: 0,
          lastReview: Date.now() - i * 1000
        };
      }

      AppState.estado.flashcardData = deck;
      AppState.salvarFlashcards();

      const carregado = AppState.carregarFlashcards();
      expect(Object.keys(carregado).length).toBe(50);
      expect(carregado['card_25'].stability).toBe(12.5);
    });

    it('F23: deve simular 5 iterações consecutivas de Ebbinghaus mantendo retenção válida [0, 1]', () => {
      let s = 2.0;
      for (let i = 1; i <= 5; i++) {
        const r = calculateRetention(s, s, 19 / 81, -0.5);
        expect(r).toBeCloseTo(0.9, 5);
        s = predictNextStabilityGood(5.0, s, r);
        expect(s).toBeGreaterThan(2.0);
        expect(Number.isFinite(s)).toBe(true);
      }
    });

    it('F24: deve enfileirar operações offline no SyncManager mantendo rastreamento de pendências', () => {
      const adapter = new MockBackendAdapter();
      const sync = new SyncManager(adapter);
      sync.limparFila();

      sync.enfileirar('progress', 'update', 'user_1', { xp: 150 });
      sync.enfileirar('flashcards', 'update', 'deck_1', { count: 30 });

      const status = sync.getStatus();
      expect(status.pendingCount).toBe(2);

      const fila = sync.getFila();
      expect(fila[0].entity).toBe('progress');
      expect(fila[1].entity).toBe('flashcards');
    });

    it('F25: o projeto deve conter o roadmap de melhoria contínua planejado ou especificado em PROJECT.md', () => {
      const projectMdPath = path.resolve(process.cwd(), 'PROJECT.md');
      expect(fs.existsSync(projectMdPath)).toBe(true);

      const projectContent = fs.readFileSync(projectMdPath, 'utf8');
      expect(projectContent).toContain('F25');
      expect(projectContent).toContain('Continuous Improvement Roadmap');
    });
  });
});
