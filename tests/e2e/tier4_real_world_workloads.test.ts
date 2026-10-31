// @ts-nocheck
// @vitest-environment happy-dom
// tests/e2e/tier4_real_world_workloads.test.ts
// Tier 4: Real-World Application Workload Scenarios & User Journeys

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
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
import AppTTS from '../../js/core/tts.js';
import App from '../../js/core.js';
import ModalManager from '../../js/modal_manager';
import { ConflictResolver } from '../../js/core/collaboration';
import { SyncManager, MockBackendAdapter } from '../../js/core/sync';
import Flashcards from '../../js/flashcards.js';
import Quiz from '../../js/quiz.js';
import Onboarding from '../../js/onboarding.js';
import Calor from '../../js/heatmap.js';
import Profilo from '../../js/profilo.js';
import Progressao, { LevelUp } from '../../js/progression.js';
import {
  calculateRetention,
  predictNextStabilityGood,
  calculateTimeToTarget
} from '../../src/analytics/ebbinghausCurve';

describe('Tier 4: Real-World Workload Scenarios & User Journeys', () => {
  beforeEach(() => {
    bootstrapAppDOM();
    resetAppEnvironment();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ============================================================
  // Scenario 1: Nuovo Studente (Fresh Onboarding & First Temple Mastery)
  // ============================================================
  it('Cenário 1: Nuovo Studente — Onboarding completo, estudo de vocabulário, quiz perfeito e primeiro level-up', () => {
    // 1. Início hermético do novo estudante (sem registros prévios)
    localStorage.clear();
    sessionStorage.clear();

    expect(Onboarding.deveExibir()).toBe(true);

    // 2. Apresentação do Onboarding e navegação pelos 3 slides
    Onboarding.mostrar();
    const modalOnboarding = document.getElementById('onboarding-modal');
    expect(modalOnboarding?.style.display).toBe('flex');
    expect(Onboarding.slideAtual).toBe(0);

    // Avança slides e conclui
    Onboarding.proximoSlide();
    expect(Onboarding.slideAtual).toBe(1);
    Onboarding.proximoSlide();
    expect(Onboarding.slideAtual).toBe(2);
    Onboarding.concluir();

    expect(modalOnboarding?.style.display).toBe('none');
    expect(localStorage.getItem('it_onboarding_done')).toBe('1');
    expect(Onboarding.deveExibir()).toBe(false);

    // 3. Verificação do estado inicial da progressão
    AppState.estado.progresso = AppState.carregarProgresso();
    expect(AppState.estado.progresso.nivel).toBe(1);
    expect(AppState.estado.progresso.xp).toBe(0);
    expect(AppState.estado.progresso.templos_desbloqueados).toEqual([1]);
    expect(AppState.estado.progresso.templos_concluidos).toEqual([]);

    // 4. Usuário estuda o vocabulário inicial do Templo 1 (Roma)
    const palavrasTemplo1 = [
      { id: 'w1', italiano: 'ciao', portugues: 'olá' },
      { id: 'w2', italiano: 'grazie', portugues: 'obrigado' },
      { id: 'w3', italiano: 'prego', portugues: 'de nada' }
    ];

    palavrasTemplo1.forEach(palavra => {
      Flashcards.cartaAtual = palavra;
      // Classifica como "Good" (rating 3)
      Flashcards.avaliar(3);
    });

    // Flashcards agora possuem estabilidade registrada
    expect(AppState.estado.flashcardData['w1']).toBeDefined();
    expect(AppState.estado.flashcardData['w1'].stability).toBeGreaterThan(0);
    expect(AppState.estado.flashcardData['w2'].reps).toBeGreaterThanOrEqual(1);

    // 5. Usuário realiza o primeiro Quiz do Templo 1 com aproveitamento de 100%
    Quiz.temploAtual = 1;
    Quiz.perguntas = [
      {
        id: 'q1',
        pergunta: 'Como se diz "Bom dia"?',
        alternativas: ['Buongiorno', 'Buonasera', 'Ciao', 'Grazie'],
        resposta_correta: 'Buongiorno',
        xp_recompensa: 20
      },
      {
        id: 'q2',
        pergunta: 'Como se diz "Obrigado"?',
        alternativas: ['Prego', 'Grazie', 'Scusa', 'Favore'],
        resposta_correta: 'Grazie',
        xp_recompensa: 20
      }
    ];
    Quiz.perguntaAtual = 0;
    Quiz.pontuacao = 0;
    Quiz.xpTotal = 0;
    Quiz.combo = 0;
    Quiz.respondido = false;

    // Responde questão 1 com acerto
    Quiz.mostrarPergunta();
    Quiz.checarResposta('Buongiorno');
    expect(Quiz.pontuacao).toBe(1);
    expect(Quiz.combo).toBe(1);

    // Avança para questão 2 e responde com acerto
    Quiz.proximaPergunta();
    Quiz.checarResposta('Grazie');
    expect(Quiz.pontuacao).toBe(2);
    expect(Quiz.combo).toBe(2);

    // Conclui Quiz
    Quiz.mostrarResultado();
    expect(document.getElementById('resultado-score')?.textContent).toBe('2/2');

    // 6. Concessão de XP e avanço para Nível 2
    // Concede XP adicional de domínio de templo para atingir marco de nível 2 (300 XP)
    Progressao.ganhar(300);

    expect(AppState.estado.progresso.xp).toBeGreaterThanOrEqual(300);
    expect(AppState.estado.progresso.nivel).toBe(2);

    // Templo 2 (Firenze) é desbloqueado e Templo 1 marcado como concluído
    Progressao.verificarDesbloqueioTemplos();
    expect(AppState.estado.progresso.templos_desbloqueados).toContain(2);

    AppState.estado.progresso.templos_concluidos.push(1);
    AppState.salvarProgresso();

    // 7. Persistência verificada no localStorage
    const progSalvo = JSON.parse(localStorage.getItem('it_progresso') || '{}');
    expect(progSalvo.nivel).toBe(2);
    expect(progSalvo.templos_desbloqueados).toContain(2);
    expect(progSalvo.templos_concluidos).toContain(1);
  });

  // ============================================================
  // Scenario 2: Sessione Spaziata FSRS (Full Spaced Repetition Cycle)
  // ============================================================
  it('Cenário 2: Sessione Spaziata FSRS — Ciclo completo de repetição espaçada, modelo 4 botões e retenção matemática', () => {
    const agora = Date.now();
    const UM_DIA = 24 * 3600 * 1000;

    // Inicializa 4 cards em estados distintos
    AppState.estado.flashcardData = {
      card_again: { state: 'review', difficulty: 5.0, stability: 4.0, lapses: 0, reps: 2, lastReview: agora - 2 * UM_DIA },
      card_hard:  { state: 'review', difficulty: 4.5, stability: 5.0, lapses: 0, reps: 3, lastReview: agora - 3 * UM_DIA },
      card_good:  { state: 'review', difficulty: 4.0, stability: 6.0, lapses: 0, reps: 4, lastReview: agora - 4 * UM_DIA },
      card_easy:  { state: 'review', difficulty: 3.5, stability: 8.0, lapses: 0, reps: 5, lastReview: agora - 5 * UM_DIA }
    };
    AppState.salvarFlashcards();

    // Retenção prévia calculada
    const FACTOR = 19 / 81;
    const DECAY = -0.5;
    const rPrevGood = calculateRetention(4, 6.0, FACTOR, DECAY);
    expect(rPrevGood).toBeGreaterThan(0.7);
    expect(rPrevGood).toBeLessThan(1.0);

    // 1. Avalia Card 1 como "Again" (rating 1)
    Flashcards.cartaAtual = { id: 'card_again', italiano: 'parola1', portugues: 'palavra1' };
    Flashcards.avaliar(1);
    const c1 = AppState.estado.flashcardData['card_again'];
    expect(c1.erros).toBe(1);
    expect(c1.reps).toBeGreaterThanOrEqual(2);

    // 2. Avalia Card 2 como "Hard" (rating 2)
    Flashcards.cartaAtual = { id: 'card_hard', italiano: 'parola2', portugues: 'palavra2' };
    Flashcards.avaliar(2);
    const c2 = AppState.estado.flashcardData['card_hard'];
    expect(c2.difficulty).toBeGreaterThanOrEqual(4.0);

    // 3. Avalia Card 3 como "Good" (rating 3)
    Flashcards.cartaAtual = { id: 'card_good', italiano: 'parola3', portugues: 'palavra3' };
    Flashcards.avaliar(3);
    const c3 = AppState.estado.flashcardData['card_good'];
    expect(c3.stability).toBeGreaterThan(6.0); // Estabilidade subiu
    expect(c3.reps).toBe(5);

    // 4. Avalia Card 4 como "Easy" (rating 4)
    Flashcards.cartaAtual = { id: 'card_easy', italiano: 'parola4', portugues: 'palavra4' };
    Flashcards.avaliar(4);
    const c4 = AppState.estado.flashcardData['card_easy'];
    expect(c4.stability).toBeGreaterThan(10.0); // Bônus de facilidade
    expect(c4.difficulty).toBeLessThanOrEqual(4.0);

    // 5. Verificação da retenção pós-avaliação (estabilidade maior projeta retenção mais duradoura)
    const rPosEasy = calculateRetention(1, c4.stability, FACTOR, DECAY);
    expect(rPosEasy).toBeGreaterThan(0.95);

    // 6. Registro de atividade no Heatmap diário
    Calor.registrar(4, 30);
    const diario = JSON.parse(localStorage.getItem('it_diario') || '{}');
    const hoje = Calor._dataLocal();
    expect(diario[hoje]).toBeDefined();
    expect(diario[hoje].cards).toBeGreaterThanOrEqual(4);

    // 7. Persistência atômica no localStorage
    const savedCards = JSON.parse(localStorage.getItem('it_flashcards') || '{}');
    expect(savedCards['card_good'].stability).toBe(c3.stability);
    expect(savedCards['card_easy'].stability).toBe(c4.stability);
  });

  // ============================================================
  // Scenario 3: Il Tempio della Conoscenza (Quiz Exam Session)
  // ============================================================
  it('Cenário 3: Il Tempio della Conoscenza — Fluxo completo de quiz com combo crescente, feedback e persistência de histórico', () => {
    // Configura sessão de exame com 4 perguntas estruturadas
    Quiz.temploAtual = 1;
    Quiz.perguntas = [
      {
        id: 'q1',
        pergunta: 'Come si traduce "arrivederci"?',
        alternativas: ['Adeus / Até logo', 'Obrigado', 'Por favor', 'Desculpe'],
        resposta_correta: 'Adeus / Até logo',
        xp_recompensa: 20
      },
      {
        id: 'q2',
        pergunta: 'Come si dice "Grazie mille"?',
        alternativas: ['Muito obrigado', 'De nada', 'Com licença', 'Bom dia'],
        resposta_correta: 'Muito obrigado',
        xp_recompensa: 20
      },
      {
        id: 'q3',
        pergunta: 'Cosa significa "Buonanotte"?',
        alternativas: ['Boa noite (ao despedir/dormir)', 'Bom dia', 'Boa tarde', 'Olá'],
        resposta_correta: 'Boa noite (ao despedir/dormir)',
        xp_recompensa: 20
      },
      {
        id: 'q4',
        pergunta: 'Quale parola indica "por favore"?',
        alternativas: ['Prego', 'Scusa', 'Grazie', 'Ciao'],
        resposta_correta: 'Prego',
        xp_recompensa: 20
      }
    ];
    Quiz.perguntaAtual = 0;
    Quiz.pontuacao = 0;
    Quiz.xpTotal = 0;
    Quiz.combo = 0;
    Quiz.respondido = false;

    // Responde P1 corretamente -> Combo 1 (multiplicador ×1)
    Quiz.mostrarPergunta();
    Quiz.checarResposta('Adeus / Até logo');
    expect(Quiz.pontuacao).toBe(1);
    expect(Quiz.combo).toBe(1);
    expect(Quiz.xpTotal).toBe(20);

    // Responde P2 corretamente -> Combo 2 (multiplicador ×1)
    Quiz.proximaPergunta();
    Quiz.checarResposta('Muito obrigado');
    expect(Quiz.pontuacao).toBe(2);
    expect(Quiz.combo).toBe(2);
    expect(Quiz.xpTotal).toBe(40);

    // Responde P3 corretamente -> Combo 3 (multiplicador ×2)
    Quiz.proximaPergunta();
    Quiz.checarResposta('Boa noite (ao despedir/dormir)');
    expect(Quiz.pontuacao).toBe(3);
    expect(Quiz.combo).toBe(3);
    expect(Quiz.xpTotal).toBe(80); // 40 + (20 * 2)

    // Responde P4 incorretamente -> Combo reseta para 0
    Quiz.proximaPergunta();
    Quiz.checarResposta('Scusa'); // Incorreta
    expect(Quiz.pontuacao).toBe(3);
    expect(Quiz.combo).toBe(0);
    expect(Quiz.xpTotal).toBe(80);

    // Container de explicação exibe feedback corretivo
    const explicacaoContainer = document.getElementById('explicacao-container');
    expect(explicacaoContainer?.style.display).toBe('block');
    const explicacaoTexto = document.getElementById('quiz-explicacao')?.textContent;
    expect(explicacaoTexto).toContain('Prego');

    // Conclusão e exibição de resultados
    Quiz.mostrarResultado();
    expect(document.getElementById('resultado-score')?.textContent).toBe('3/4');

    // Histórico de quiz registrado no localStorage
    const historico = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]');
    expect(historico.length).toBeGreaterThanOrEqual(1);
    expect(historico[0].templo).toBe(1);
    expect(historico[0].acertos).toBe(3);
    expect(historico[0].total).toBe(4);
    expect(historico[0].xp_ganho).toBe(80);
  });

  // ============================================================
  // Scenario 4: Sincronizzazione Multi-Dispositivo (Cross-Tab Collaboration)
  // ============================================================
  it('Cenário 4: Sincronização Multi-Dispositivo — Colaboração concorrente entre duas abas sem colisão ou perda de dados via CRDT', () => {
    const agora = Date.now();
    const resolver = new ConflictResolver();

    // ── Aba A: Estudou Templo 1 e desbloqueou Templo 2
    const estadoAbaA_Progresso = {
      nivel: 2,
      xp: 320,
      templos_desbloqueados: [1, 2],
      templos_concluidos: [1],
      conquistas: ['quiz_master'],
      grammatica_completadas: ['mod_1']
    } as any;

    const estadoAbaA_Flashcards = {
      w1: { id: 'w1', state: 'review', reps: 4, stability: 12.0, lastReview: agora - 1000 },
      w2: { id: 'w2', state: 'learning', reps: 1, stability: 2.5, lastReview: agora - 2000 }
    };

    // ── Aba B: Revisou gramática e flashcard w2 mais recente
    const estadoAbaB_Progresso = {
      nivel: 1,
      xp: 290,
      templos_desbloqueados: [1],
      templos_concluidos: [],
      conquistas: ['streak_3_dias'],
      grammatica_completadas: ['mod_2']
    } as any;

    const estadoAbaB_Flashcards = {
      w1: { id: 'w1', state: 'review', reps: 2, stability: 6.0, lastReview: agora - 5000 },
      w2: { id: 'w2', state: 'review', reps: 3, stability: 8.0, lastReview: agora - 500 } // Mais recente!
    };

    // Reconciliação CRDT de Progresso
    const resProgresso = resolver.reconciliarProgresso(estadoAbaA_Progresso, estadoAbaB_Progresso);
    const progressoReconciliado = resProgresso.progresso;

    // Monotonicidade & União de conjuntos garantida
    expect(progressoReconciliado.nivel).toBe(2);
    expect(progressoReconciliado.xp).toBe(320); // Max preservado
    expect(progressoReconciliado.templos_desbloqueados).toEqual(expect.arrayContaining([1, 2]));
    expect(progressoReconciliado.templos_concluidos).toEqual([1]);
    expect(progressoReconciliado.conquistas).toEqual(expect.arrayContaining(['quiz_master', 'streak_3_dias']));
    expect(progressoReconciliado.grammatica_completadas).toEqual(expect.arrayContaining(['mod_1', 'mod_2']));
    expect(resProgresso.conflitos.length).toBeGreaterThan(0);

    // Reconciliação LWW de Flashcards via AppState.reconciliarFlashcards
    const flashcardsReconciliados = AppState.reconciliarFlashcards(estadoAbaA_Flashcards, estadoAbaB_Flashcards);

    // w1 mantém versão da Aba A (lastReview mais recente e mais reps)
    expect(flashcardsReconciliados['w1'].stability).toBe(12.0);
    expect(flashcardsReconciliados['w1'].reps).toBe(4);

    // w2 adota versão da Aba B (lastReview mais recente: agora - 500 vs agora - 2000)
    expect(flashcardsReconciliados['w2'].stability).toBe(8.0);
    expect(flashcardsReconciliados['w2'].reps).toBe(3);

    // Reversibilidade: merge na ordem inversa produz exatamente o mesmo resultado determinístico
    const flashcardsReverso = AppState.reconciliarFlashcards(estadoAbaB_Flashcards, estadoAbaA_Flashcards);
    expect(flashcardsReverso['w1'].stability).toBe(12.0);
    expect(flashcardsReverso['w2'].stability).toBe(8.0);
  });

  // ============================================================
  // Scenario 5: Resilienza PWA Offline & Backup Lifecycle
  // ============================================================
  it('Cenário 5: Resilienza PWA Offline & Backup — Operação offline, dreno de fila ao reconectar e validação atômica de backup', async () => {
    // 1. Simula entrada em modo offline
    let isOnlineMock = false;
    const sync = new SyncManager();
    sync.salvarConfig({
      provider: 'mock',
      autoSync: false,
      userId: 'offline_tester_e2e'
    });
    vi.spyOn(sync, 'isOnline').mockImplementation(() => isOnlineMock);

    // 2. Três ações de aprendizagem realizadas desconectado
    sync.enfileirar('quiz', 'complete', 'sessao_101', { templo: 1, score: 100 });
    sync.enfileirar('flashcards', 'review', 'w1_card', { stability: 15.0, rating: 3 });
    sync.enfileirar('progress', 'update', 'user_prog', { xp: 450, nivel: 2 });

    expect(sync.getStatus().pendingCount).toBe(3);

    // Tentativa de flush em offline é barrada com erro sem perda da fila
    const resOffline = await sync.flush();
    expect(resOffline.sucesso).toBe(false);
    expect(sync.getStatus().pendingCount).toBe(3);

    // 3. Simula cache SWR e logs que podem ser descartados sob pressão de cota
    localStorage.setItem('it_swr_grammar', JSON.stringify({ cache: true }));
    localStorage.setItem('it_client_errors', JSON.stringify([{ msg: 'old log' }]));

    // 4. Reconexão: volta a ficar online e executa flush da fila pendente
    isOnlineMock = true;
    const resOnline = await sync.flush();
    expect(resOnline.sucesso).toBe(true);
    expect(resOnline.processados.length).toBe(3);
    expect(sync.getStatus().pendingCount).toBe(0);

    // 5. Ciclo de Backup — Geração e exportação
    const backupGerado = {
      versao: 4,
      data: new Date().toISOString(),
      progresso: {
        nivel: 2,
        xp: 450,
        templos_desbloqueados: [1, 2],
        total_palavras: 10,
        streak: 2
      },
      flashcards: {
        w1: { state: 'review', reps: 4, stability: 15.0 }
      },
      diario: {},
      quiz_historico: [],
      storie_lidas: []
    };

    // Validação de payload íntegro é aceita com sucesso
    expect(Profilo._validarPayloadBackup(backupGerado)).toBe(true);

    // 6. Teste de rejeição e barreira defensiva com backup corrupto
    const backupsCorrompidos = [
      null,
      {},
      { versao: 0, progresso: backupGerado.progresso },
      { versao: 4, progresso: null },
      { versao: 4, progresso: { nivel: -1, xp: 50, templos_desbloqueados: [1] } },
      { versao: 4, progresso: { nivel: 1, xp: 50, templos_desbloqueados: [] } } // Sem templos
    ];

    backupsCorrompidos.forEach(corrompido => {
      expect(() => Profilo._validarPayloadBackup(corrompido)).toThrow();
    });

    // 7. Aplicação atômica do backup legítimo
    localStorage.setItem('it_progresso', JSON.stringify(backupGerado.progresso));
    localStorage.setItem('it_flashcards', JSON.stringify(backupGerado.flashcards));

    AppState.estado.progresso = AppState.carregarProgresso();
    AppState.estado.flashcardData = AppState.carregarFlashcards();

    expect(AppState.estado.progresso.xp).toBe(450);
    expect(AppState.estado.progresso.nivel).toBe(2);
    expect(AppState.estado.flashcardData['w1'].stability).toBe(15.0);
  });
});
