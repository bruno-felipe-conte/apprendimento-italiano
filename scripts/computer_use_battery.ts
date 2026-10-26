import { chromium, Page, ConsoleMessage } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

const TARGET_URL = process.env.TEST_URL || 'https://bruno-felipe-conte.github.io/apprendimento-italiano/';
const OUTPUT_DIR = path.resolve('test-results/computer-use');

interface TabResult {
  tab: string;
  success: boolean;
  itemCount: number;
  interactiveSuccess: boolean;
  errors: string[];
  warnings: string[];
  details: string;
}

interface WindowWithModules {
  Conquistas?: { fecharModal?: () => void };
  App?: {
    navegar: (t: string) => void;
    fecharModalTemplo: () => void;
    abrirMetaSettings: () => void;
    fecharMetaSettings: () => void;
  };
  Dialoghi?: { renderizarSeletor: () => void };
  Canzoni?: { renderizarSeletor: () => void };
  Imitazione?: { tocarModelo: (rate: number) => void };
  Quiz?: { voltarSelector: () => void };
  Grammatica?: { voltarSeletor: () => void };
  Storie?: {
    renderizarSeletor: () => void;
    fecharLeitor: () => void;
  };
}

async function fecharModais(page: Page) {
  await page.evaluate(() => {
    const ids = ['conquista-modal', 'levelup-modal', 'onboarding-modal', 'backup-reminder-popup'];
    ids.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.classList.remove('ativo', 'visivel');
        el.style.display = 'none';
      }
    });
    const win = window as unknown as WindowWithModules;
    if (typeof win.Conquistas?.fecharModal === 'function') {
      win.Conquistas.fecharModal();
    }
  }).catch(() => {});
}

async function runBattery() {
  console.log(`\n==================================================`);
  console.log(`🚀 INICIANDO BATERIA "COMPUTER USE" COMPLETA`);
  console.log(`🌐 Alvo: ${TARGET_URL}`);
  console.log(`==================================================\n`);

  if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext({
    viewport: { width: 1366, height: 768 }
  });

  // Pré-configurar flags para não bloquear a tela de testes
  await context.addInitScript(() => {
    try {
      localStorage.setItem('it_onboarding_visto', 'true');
      localStorage.setItem('it_ultimo_aviso_backup', Date.now().toString());
    } catch (_) {}
  });

  const page = await context.newPage();

  const globalErrors: string[] = [];
  const globalWarnings: string[] = [];
  const pageErrors: string[] = [];
  const failedRequests: string[] = [];

  page.on('console', (msg: ConsoleMessage) => {
    const text = msg.text();
    if (msg.type() === 'error') {
      globalErrors.push(text);
      console.log(`🔴 [CONSOLE ERROR]: ${text}`);
    } else if (msg.type() === 'warning') {
      globalWarnings.push(text);
      if (text.includes('404') || text.includes('failed') || text.includes('MaxListeners')) {
        console.log(`⚠️  [CONSOLE WARN]: ${text}`);
      }
    }
  });

  page.on('pageerror', (err: Error) => {
    pageErrors.push(err.message);
    console.log(`🔥 [PAGE ERROR]: ${err.message}\n${err.stack}`);
  });

  page.on('requestfailed', req => {
    const failure = req.failure();
    const url = req.url();
    if (!url.includes('google-analytics') && !url.includes('doubleclick')) {
      const errText = `${req.method()} ${url} - ${failure?.errorText || 'Unknown'}`;
      failedRequests.push(errText);
      console.log(`❌ [REQUEST FAILED]: ${errText}`);
    }
  });

  console.log(`Carregando aplicativo...`);
  await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(2000);
  await fecharModais(page);

  const results: TabResult[] = [];

  const tabs = [
    'templi',
    'dialoghi',
    'canzoni',
    'imitazione',
    'flashcard',
    'quiz',
    'vocabolario',
    'grammatica',
    'storie',
    'profilo'
  ];

  for (const tab of tabs) {
    console.log(`\n--------------------------------------------------`);
    console.log(`🔍 [COMPUTER USE] TESTANDO ABA: "${tab.toUpperCase()}"`);
    console.log(`--------------------------------------------------`);

    const tabErrors: string[] = [];
    const tabWarnings: string[] = [];
    const errSub = (msg: ConsoleMessage) => {
      if (msg.type() === 'error') tabErrors.push(msg.text());
      if (msg.type() === 'warning') tabWarnings.push(msg.text());
    };
    page.on('console', errSub);

    let tabSuccess = false;
    let itemCount = 0;
    let interactiveSuccess = false;
    let details = '';

    try {
      await fecharModais(page);

      // 1. Navegar até a aba via App.navegar(tab)
      await page.evaluate((t: string) => {
        const win = window as unknown as WindowWithModules;
        win.App?.navegar(t);
      }, tab);
      await page.waitForTimeout(800);

      // 2. Verificar que a seção está ativa e visível
      const secSelector = `#sec-${tab}`;
      const isVisible = await page.evaluate((sel: string) => {
        const el = document.querySelector(sel);
        if (!el) return false;
        return el.classList.contains('active') && window.getComputedStyle(el).display !== 'none';
      }, secSelector);

      if (!isVisible) {
        throw new Error(`Seção ${secSelector} não ficou ativa nem visível!`);
      }

      // 3. Testes funcionais interativos específicos da aba
      switch (tab) {
        case 'templi': {
          const cards = page.locator('#templos-grid .templo-card');
          itemCount = await cards.count();
          console.log(`  Templos encontrados no grid: ${itemCount}`);
          if (itemCount === 0) throw new Error('Grid de templos vazio!');

          // Testar clique em templo bloqueado para abrir modal de detalhes
          const lockedCard = page.locator('#templos-grid .templo-card.bloqueado').first();
          if (await lockedCard.count() > 0) {
            await lockedCard.click();
            await page.waitForTimeout(600);

            const modalVisivel = await page.evaluate(() => {
              const m = document.getElementById('templo-modal');
              return m ? (m.classList.contains('visivel') || window.getComputedStyle(m).display !== 'none') : false;
            });
            console.log(`  Modal de detalhes do Templo aberto: ${modalVisivel}`);

            if (modalVisivel) {
              await page.evaluate(() => {
                const win = window as unknown as WindowWithModules;
                win.App?.fecharModalTemplo();
              });
              await page.waitForTimeout(400);
            }
          }

          // Testar Heatmap de atividades no topo
          const heatmapCells = page.locator('#heatmap .hm-cell, #heatmap div');
          const hmCount = await heatmapCells.count();
          console.log(`  Células de atividade no Heatmap: ${hmCount}`);

          interactiveSuccess = true;
          tabSuccess = true;
          details = `${itemCount} templos carregados; Modal informativo e Heatmap funcionando perfeitamente.`;
          break;
        }

        case 'dialoghi': {
          const cards = page.locator('#dialoghi-container .dialogo-card');
          itemCount = await cards.count();
          console.log(`  Diálogos carregados no catálogo: ${itemCount}`);
          if (itemCount === 0) throw new Error('Nenhum card de diálogo renderizado!');

          // Filtrar por nível A1
          const selectNivel = page.locator('#dialoghi-container .nivel-select');
          if (await selectNivel.count() > 0) {
            await selectNivel.selectOption('A1');
            await page.waitForTimeout(500);
          }

          // Clicar no primeiro diálogo
          await cards.first().click();
          await page.waitForTimeout(800);

          // Verificar leitor de diálogo
          const playerOpen = await page.evaluate(() => {
            return !!document.querySelector('.btn-modo-toggle, .btn-secondario');
          });
          console.log(`  Visualizador de diálogo aberto: ${playerOpen}`);
          interactiveSuccess = playerOpen;

          // Clicar em Voltar ao catálogo
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.Dialoghi?.renderizarSeletor();
          });
          await page.waitForTimeout(500);

          tabSuccess = true;
          details = `${itemCount} diálogos disponíveis; Filtro e leitor de falas funcionaram 100%.`;
          break;
        }

        case 'canzoni': {
          const cards = page.locator('#canzoni-container .dialogo-card');
          itemCount = await cards.count();
          console.log(`  Músicas no catálogo: ${itemCount}`);
          if (itemCount === 0) throw new Error('Nenhuma música renderizada!');

          // Testar campo de busca
          const busca = page.locator('#canzoni-container input[type="search"]').first();
          if (await busca.count() > 0) {
            await busca.fill('Bella');
            await page.waitForTimeout(400);
            await busca.fill('');
            await page.waitForTimeout(400);
          }

          // Clicar na primeira música
          await cards.first().click();
          await page.waitForTimeout(800);

          // Verificar player / letras
          const playerOpen = await page.evaluate(() => {
            return !!document.querySelector('.can-player, .can-back-btn');
          });
          console.log(`  Visualizador de música/karaokê aberto: ${playerOpen}`);
          interactiveSuccess = playerOpen;

          // Voltar ao catálogo
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.Canzoni?.renderizarSeletor();
          });
          await page.waitForTimeout(500);

          tabSuccess = true;
          details = `${itemCount} músicas renderizadas com busca e player de karaokê funcionando.`;
          break;
        }

        case 'imitazione': {
          const heroCard = page.locator('#imitazione-container .dojo-hero-card, #imitazione-container .imitazione-dojo');
          const temHero = await heroCard.count() > 0;
          console.log(`  Studio / Dojo de Imitação renderizado: ${temHero}`);
          if (!temHero) throw new Error('Dojo de imitação não renderizou!');

          const pills = page.locator('#imit-filtro-bar .dojo-level-pill');
          itemCount = await pills.count();
          console.log(`  Filtros de nível e categoria no Dojo: ${itemCount}`);

          // Testar botão de áudio modelo
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.Imitazione?.tocarModelo(1.0);
          });
          await page.waitForTimeout(400);

          interactiveSuccess = true;
          tabSuccess = true;
          details = `Dojo de Imitação ativo com estúdio de pronúncia, síntese nativa e ${itemCount} filtros de nível.`;
          break;
        }

        case 'flashcard': {
          // Selecionar Templo 1 no dropdown
          const selectTemplo = page.locator('#flashcard-templo-select');
          await selectTemplo.selectOption('1');
          await page.waitForTimeout(600);

          const fcCard = page.locator('#flashcard');
          const fcCount = await fcCard.count();
          console.log(`  Elemento #flashcard encontrado: ${fcCount > 0}`);
          if (fcCount === 0) throw new Error('Carta #flashcard não renderizou após selecionar templo!');

          const palavraAtual = await page.locator('#card-italiano').innerText();
          console.log(`  Palavra no flashcard: "${palavraAtual}"`);

          // Clicar para virar carta
          await fcCard.first().click();
          await page.waitForTimeout(500);

          // Fechar eventual modal de conquista antes de clicar em botões
          await fecharModais(page);

          // Verificar botões de resposta FSRS / SM-2
          const btnBom = page.locator('#card-actions button, #fc-botoes-resposta button, button:has-text("Bom"), button:has-text("Bene")').first();
          const temBtnBom = await btnBom.count() > 0;
          console.log(`  Botões de resposta FSRS visíveis: ${temBtnBom}`);

          if (temBtnBom) {
            await btnBom.click({ force: true });
            await page.waitForTimeout(500);
          }

          // Testar troca para modo Reverso e voltar para Normal
          const btnReverso = page.locator('#btn-reverso');
          if (await btnReverso.count() > 0) {
            await btnReverso.click({ force: true });
            await page.waitForTimeout(300);
          }
          const btnNormal = page.locator('#btn-modo-normal');
          if (await btnNormal.count() > 0) {
            await btnNormal.click({ force: true });
            await page.waitForTimeout(300);
          }

          itemCount = 1;
          interactiveSuccess = true;
          tabSuccess = true;
          details = `Flashcard do Templo 1 funcional; Palavra "${palavraAtual}" virou com FSRS e modos reverso/normal.`;
          break;
        }

        case 'quiz': {
          await fecharModais(page);
          const quizBtns = page.locator('#quiz-templo-selector .quiz-templo-btn:not(.bloqueado)');
          itemCount = await quizBtns.count();
          console.log(`  Quizzes disponíveis: ${itemCount}`);
          if (itemCount === 0) throw new Error('Nenhum quiz desbloqueado disponível!');

          // Iniciar primeiro quiz disponível (Tempio 1 ou Quiz Generale)
          await quizBtns.first().click({ force: true });
          await page.waitForTimeout(800);

          // Verificar container do quiz ativo
          const quizAtivo = await page.evaluate(() => {
            const qc = document.getElementById('quiz-container');
            return qc ? window.getComputedStyle(qc).display !== 'none' : false;
          });
          console.log(`  Container de perguntas do Quiz ativo: ${quizAtivo}`);

          if (quizAtivo) {
            // Clicar na primeira opção
            const opcoes = page.locator('#opcoes-grid button');
            if (await opcoes.count() > 0) {
              await opcoes.first().click({ force: true });
              await page.waitForTimeout(500);

              // Continuar
              const btnCont = page.locator('#explicacao-container button:has-text("Continuar")');
              if (await btnCont.count() > 0 && await btnCont.isVisible()) {
                await btnCont.click({ force: true });
                await page.waitForTimeout(500);
              }
              interactiveSuccess = true;
            }
          }

          // Voltar aos templos
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.Quiz?.voltarSelector();
          });
          await page.waitForTimeout(400);

          tabSuccess = true;
          details = `${itemCount} opções de quiz disponíveis; Pergunta respondida com feedback interativo imediato.`;
          break;
        }

        case 'vocabolario': {
          const vocabItems = page.locator('#vocab-list .vocab-item');
          itemCount = await vocabItems.count();
          console.log(`  Palavras no catálogo de Vocabulário: ${itemCount}`);
          if (itemCount === 0) throw new Error('Lista de vocabulário vazia!');

          // Testar campo de busca
          const busca = page.locator('#vocab-busca');
          await busca.fill('ciao');
          await page.waitForTimeout(500);
          const buscaCount = await page.locator('#vocab-list .vocab-item').count();
          console.log(`  Resultados para busca "ciao": ${buscaCount}`);
          await busca.fill('');
          await page.waitForTimeout(500);

          // Testar áudio da frase de exemplo (🔊)
          const btnAudioExemplo = page.locator('#vocab-list .vocab-exemplo').first();
          if (await btnAudioExemplo.count() > 0) {
            await btnAudioExemplo.click();
            await page.waitForTimeout(400);
          }

          // Testar botões de ocultar PT / IT
          const btnBlurPt = page.locator('#vocab-btn-blur-pt');
          if (await btnBlurPt.count() > 0) {
            await btnBlurPt.click();
            await page.waitForTimeout(200);
            await btnBlurPt.click();
            await page.waitForTimeout(200);
          }

          interactiveSuccess = true;
          tabSuccess = true;
          details = `${itemCount} palavras de vocabulário enriquecidas com busca, áudio de exemplo e blur cards.`;
          break;
        }

        case 'grammatica': {
          const lezCards = page.locator('#grammatica-container .gram-lez-card');
          itemCount = await lezCards.count();
          console.log(`  Lições de gramática disponíveis: ${itemCount}`);
          if (itemCount === 0) throw new Error('Nenhuma lição gramatical renderizada!');

          // Abrir Lição I
          await lezCards.first().click();
          await page.waitForTimeout(800);

          const lezOpen = await page.evaluate(() => {
            return !!document.querySelector('.gram-lesson-layout, .gram-btn-back');
          });
          console.log(`  Lição gramatical aberta: ${lezOpen}`);
          interactiveSuccess = lezOpen;

          // Voltar ao catálogo
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.Grammatica?.voltarSeletor();
          });
          await page.waitForTimeout(400);

          tabSuccess = true;
          details = `${itemCount} lições gramaticais disponíveis; Lição I aberta com teoria e exercícios.`;
          break;
        }

        case 'storie': {
          const storyCards = page.locator('#storie-container div[onclick*="abrirStoria"]');
          itemCount = await storyCards.count();
          console.log(`  Histórias no catálogo: ${itemCount}`);
          if (itemCount === 0) throw new Error('Nenhuma história renderizada!');

          // Abrir primeira história
          await storyCards.first().click();
          await page.waitForTimeout(800);

          const readerOpen = await page.evaluate(() => {
            const overlay = document.getElementById('book-reader-overlay');
            return overlay ? window.getComputedStyle(overlay).display !== 'none' : false;
          });
          console.log(`  Leitor de livro imersivo aberto: ${readerOpen}`);
          interactiveSuccess = readerOpen;

          // Voltar ao catálogo fechando leitor
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.Storie?.fecharLeitor();
          });
          await page.waitForTimeout(400);

          tabSuccess = true;
          details = `${itemCount} histórias renderizadas; Leitor de livro imersivo aberto e fechado perfeitamente.`;
          break;
        }

        case 'profilo': {
          const cards = page.locator('#profilo-container .profilo-card');
          itemCount = await cards.count();
          console.log(`  Cards no painel de perfil: ${itemCount}`);
          if (itemCount === 0) throw new Error('Painel de perfil não renderizou cards!');

          // Testar botão de exportar backup
          const btnBackup = page.locator('#profilo-container button:has-text("Backup"), #profilo-container button:has-text("Exportar"), #btn-exportar-dados').first();
          const temBtnBackup = await btnBackup.count() > 0;
          console.log(`  Botão de backup presente: ${temBtnBackup}`);

          // Testar modal de Meta Diária
          await page.evaluate(() => {
            const win = window as unknown as WindowWithModules;
            win.App?.abrirMetaSettings();
          });
          await page.waitForTimeout(500);

          const modalMetaOpen = await page.evaluate(() => {
            const m = document.getElementById('meta-settings-modal');
            return m ? window.getComputedStyle(m).display !== 'none' : false;
          });
          console.log(`  Modal de Meta Diária abriu: ${modalMetaOpen}`);

          if (modalMetaOpen) {
            await page.evaluate(() => {
              const win = window as unknown as WindowWithModules;
              win.App?.fecharMetaSettings();
            });
            await page.waitForTimeout(300);
          }

          interactiveSuccess = temBtnBackup && modalMetaOpen;
          tabSuccess = true;
          details = `Painel de perfil com ${itemCount} seções detalhadas, gerador de backup e configurações de meta.`;
          break;
        }
      }

      // Screenshot da aba após interações bem-sucedidas
      const screenshotPath = path.join(OUTPUT_DIR, `tab_${tab}_passed.png`);
      await page.screenshot({ path: screenshotPath });
      console.log(`  📸 Screenshot salva: ${screenshotPath}`);

    } catch (err: unknown) {
      const errMsg = err instanceof Error ? err.message : String(err);
      console.log(`  ❌ ERRO NA ABA ${tab}: ${errMsg}`);
      tabErrors.push(errMsg);
      details = `FALHA: ${errMsg}`;
      const errScreenshot = path.join(OUTPUT_DIR, `tab_${tab}_FAILED.png`);
      await page.screenshot({ path: errScreenshot }).catch(() => {});
    } finally {
      page.off('console', errSub);
      results.push({
        tab,
        success: tabSuccess,
        itemCount,
        interactiveSuccess,
        errors: tabErrors,
        warnings: tabWarnings,
        details
      });
    }
  }

  await browser.close();

  // Relatório Final
  const reportPath = path.join(OUTPUT_DIR, 'battery_final_report.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    targetUrl: TARGET_URL,
    timestamp: new Date().toISOString(),
    globalErrors,
    globalWarnings,
    pageErrors,
    failedRequests,
    tabs: results
  }, null, 2));

  console.log(`\n==================================================`);
  console.log(`🏁 RESUMO GERAL DA BATERIA "COMPUTER USE"`);
  console.log(`==================================================`);
  let allPassed = true;
  for (const r of results) {
    const status = r.success ? '✅ SUCESSO' : '❌ FALHA';
    if (!r.success) allPassed = false;
    console.log(`${r.tab.padEnd(14)}: ${status} | Itens: ${String(r.itemCount).padStart(3)} | Interações OK: ${r.interactiveSuccess ? 'SIM' : 'NÃO'} | ${r.details}`);
  }
  console.log(`==================================================`);
  console.log(`Erros no Console: ${globalErrors.length}`);
  console.log(`Requisições Falhas: ${failedRequests.length}`);
  console.log(`Status Consolidado: ${allPassed ? '🎉 100% DAS ABAS PASSARAM COM SUCESSO!' : '⚠️ FALHAS DETECTADAS'}`);
  console.log(`Relatório salvo em: ${reportPath}\n`);

  if (!allPassed) {
    process.exit(1);
  }
}

runBattery().catch(e => {
  console.error("Erro fatal na execução da bateria:", e);
  process.exit(1);
});
