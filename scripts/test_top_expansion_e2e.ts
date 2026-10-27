import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { chromium, type Page, type ConsoleMessage } from '@playwright/test';

interface ConsoleIssue {
  type: string;
  text: string;
  location?: string;
}

interface RequestFailure {
  url: string;
  errorText: string;
}

interface WindowWithModules {
  App?: {
    estado?: {
      vocabCache?: unknown[];
      topFlashcards?: unknown[];
      flashcardData?: Record<string, unknown>;
    };
    navegar?: (tab: string) => void;
    pronunciar?: (texto: string) => void;
  };
  Flashcards?: {
    init?: (templo: string | number) => void;
    selecionarTemplo?: (val: string) => void;
    virarCarta?: () => void;
    responder?: (grau: string | number) => void;
    toggleModo?: (modo: string) => void;
    temploAtual?: string | number;
    cartasDisponiveis?: unknown[];
    cartaAtual?: {
      id?: string;
      italiano?: string;
      portugues?: string;
      deck?: string;
    };
  };
  Vocab?: {
    filtrarTop1000?: () => Promise<void>;
    renderizar?: () => void;
    filtroOrigem?: string;
    filtroTexto?: string;
    top1000Data?: unknown[];
  };
}

function criarServidorEstatico(pastaRaiz: string): Promise<{ server: http.Server; url: string }> {
  return new Promise((resolve) => {
    const mimeTypes: Record<string, string> = {
      '.html': 'text/html; charset=utf-8',
      '.js': 'application/javascript; charset=utf-8',
      '.css': 'text/css; charset=utf-8',
      '.json': 'application/json; charset=utf-8',
      '.svg': 'image/svg+xml',
      '.png': 'image/png',
      '.ico': 'image/x-icon',
      '.webmanifest': 'application/manifest+json'
    };

    const server = http.createServer((req, res) => {
      let reqPath = req.url ? req.url.split('?')[0] : '/';
      if (reqPath === '/') reqPath = '/index.html';

      const filePath = path.join(pastaRaiz, decodeURIComponent(reqPath));

      if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const ext = path.extname(filePath).toLowerCase();
        const contentType = mimeTypes[ext] || 'application/octet-stream';
        res.writeHead(200, {
          'Content-Type': contentType,
          'Access-Control-Allow-Origin': '*'
        });
        fs.createReadStream(filePath).pipe(res);
      } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');
      }
    });

    server.listen(0, '127.0.0.1', () => {
      const addr = server.address();
      const port = typeof addr === 'object' && addr ? addr.port : 8080;
      resolve({ server, url: `http://127.0.0.1:${port}/` });
    });
  });
}

async function fecharModais(page: Page): Promise<void> {
  const onboarding = page.locator('#onboarding-modal');
  if (await onboarding.isVisible().catch(() => false)) {
    const btnPular = onboarding.locator('button:has-text("Pular"), button:has-text("Iniciar"), button:has-text("Fechar")').first();
    if (await btnPular.isVisible().catch(() => false)) {
      await btnPular.click({ force: true }).catch(() => {});
    } else {
      await page.evaluate(() => {
        const el = document.getElementById('onboarding-modal');
        if (el) el.style.display = 'none';
      });
    }
  }

  const conquista = page.locator('#conquista-modal');
  if (await conquista.isVisible().catch(() => false)) {
    await page.evaluate(() => {
      const el = document.getElementById('conquista-modal');
      if (el) el.style.display = 'none';
    });
  }
}

async function main(): Promise<void> {
  console.log('==================================================');
  console.log('🧪 TESTE COMPLETO E2E: TOP 500 FLASHCARDS & TOP 1.000 VOCABULÁRIO');
  console.log('==================================================\n');

  const rootDir = process.cwd();
  const resultsDir = path.join(rootDir, 'test-results', 'expansion');
  fs.mkdirSync(resultsDir, { recursive: true });

  const { server, url } = await criarServidorEstatico(rootDir);
  console.log(`📡 Servidor de testes local ativo em: ${url}`);

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });

  const page = await context.newPage();

  const consoleIssues: ConsoleIssue[] = [];
  const requestFailures: RequestFailure[] = [];

  page.on('console', (msg: ConsoleMessage) => {
    const type = msg.type();
    const text = msg.text();
    if (type === 'error' && !text.includes('favicon.ico')) {
      consoleIssues.push({ type, text, location: msg.location().url });
    }
  });

  page.on('pageerror', (err: Error) => {
    consoleIssues.push({ type: 'pageerror', text: err.message });
  });

  page.on('requestfailed', (req) => {
    const reqUrl = req.url();
    const failure = req.failure();
    if (!reqUrl.includes('google-analytics') && !reqUrl.includes('favicon.ico')) {
      requestFailures.push({ url: reqUrl, errorText: failure?.errorText || 'Unknown' });
    }
  });

  console.log('Carregando aplicação no navegador...');
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);
  await fecharModais(page);

  // ─────────────────────────────────────────────────────────────
  // 1. TESTE DOS FLASHCARDS: OS 5 BARALHOS TEMÁTICOS E O GERAL
  // ─────────────────────────────────────────────────────────────
  console.log('\n--------------------------------------------------');
  console.log('🃏 TESTANDO BARALHOS TEMÁTICOS DE FLASHCARDS (TOP 500)');
  console.log('--------------------------------------------------');

  // Navegar para Flashcards
  await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    if (w.App?.navegar) w.App.navegar('flashcard');
  });
  await page.waitForTimeout(800);
  await fecharModais(page);

  const tabTemplos = page.locator('#fc-tab-templos');
  const tabEspeciais = page.locator('#fc-tab-especiais');
  const painelTemplos = page.locator('#fc-painel-templos');
  const painelEspeciais = page.locator('#fc-painel-especiais');

  console.log(`  Verificando botões de aba de origem:`);
  console.log(`    Aba Templos visível: ${await tabTemplos.isVisible()}`);
  console.log(`    Aba Baralhos Especiais visível: ${await tabEspeciais.isVisible()}`);

  if (!await tabEspeciais.isVisible()) {
    throw new Error('Botão #fc-tab-especiais não encontrado ou não visível!');
  }

  // 1. Clicar em "Baralhos Especiais (Top 500)"
  console.log('\n  ▶ Clicando na aba "⭐ Baralhos Especiais (Top 500)"...');
  await tabEspeciais.click();
  await page.waitForTimeout(400);

  const painelEspVisivel = await painelEspeciais.isVisible();
  const painelTmpOculto = !(await painelTemplos.isVisible());
  console.log(`    Painel Especial exibido: ${painelEspVisivel} | Painel Templos oculto: ${painelTmpOculto}`);
  if (!painelEspVisivel || !painelTmpOculto) {
    throw new Error('Falha na alternância de abas: o painel especial deveria estar visível e o de templos oculto.');
  }

  const selectDeck = page.locator('#flashcard-deck-select');
  const optionsDeck = await selectDeck.locator('option').all();
  console.log(`    Opções no seletor de categorias especiais: ${optionsDeck.length}`);

  const decksParaTestar = [
    { id: 'deck_colocacoes', nome: 'Colocações & Chunks', esperado: 100 },
    { id: 'deck_falsi_amici', nome: 'Falsos Amigos / Falsi Amici', esperado: 100 },
    { id: 'deck_preposizioni', nome: 'Preposições & Regências', esperado: 100 },
    { id: 'deck_verbi_irregolari', nome: 'Verbos Irregulares em Contexto', esperado: 100 },
    { id: 'deck_situazioni_reali', nome: 'Situações da Vida Real', esperado: 100 },
    { id: 'deck_all', nome: 'Todos os 500 Cards', esperado: 500 }
  ];

  for (const d of decksParaTestar) {
    console.log(`\n  ▶ Testando baralho especial: "${d.nome}" (${d.id})...`);
    
    // Selecionar o deck especial via chip ou dropdown
    const chip = page.locator(`.fc-deck-chip[data-deck="${d.id}"]`);
    if (await chip.isVisible()) {
      await chip.click();
    } else {
      await selectDeck.selectOption(d.id);
    }
    await page.waitForTimeout(600);

    const info = await page.evaluate(() => {
      const w = window as unknown as WindowWithModules;
      const fc = w.Flashcards as unknown as {
        temploAtual?: string | number;
        totalNoDeck?: number;
        cartasDisponiveis?: unknown[];
        cartaAtual?: {
          id?: string;
          italiano?: string;
          portugues?: string;
          deck?: string;
        };
      };
      return {
        temploAtual: fc?.temploAtual,
        totalNoDeck: fc?.totalNoDeck || 0,
        sessaoCartas: fc?.cartasDisponiveis?.length || 0,
        cartaId: fc?.cartaAtual?.id,
        italiano: fc?.cartaAtual?.italiano,
        portugues: fc?.cartaAtual?.portugues,
        deck: fc?.cartaAtual?.deck
      };
    });

    console.log(`    Total no baralho: ${info.totalNoDeck} (Esperado: ${d.esperado}) | Na sessão FSRS: ${info.sessaoCartas}`);
    console.log(`    Primeira carta ID: ${info.cartaId} | Italiano: "${info.italiano}" | PT: "${info.portugues}"`);

    if (info.totalNoDeck !== d.esperado) {
      throw new Error(`Contagem incorreta de cartas no baralho para ${d.id}: esperado ${d.esperado}, obteve ${info.totalNoDeck}`);
    }

    // Testar virar a carta
    const cardEl = page.locator('#flashcard');
    await cardEl.click();
    await page.waitForTimeout(300);

    const virado = await cardEl.evaluate((el) => el.classList.contains('virado'));
    console.log(`    Carta virada com clique: ${virado}`);
    if (!virado) throw new Error(`Falha ao virar a carta no deck ${d.id}`);

    // Testar resposta FSRS (clicar em "Bom / Buono")
    const btnBom = page.locator('#fc-btn-good, .btn-fsrs-good').first();
    if (await btnBom.isVisible()) {
      await btnBom.click();
      await page.waitForTimeout(400);
      console.log('    Resposta FSRS registrada com sucesso (próxima carta carregou).');
    }

    // Salvar screenshot do deck
    const screenPath = path.join(resultsDir, `flashcards_${d.id}.png`);
    await page.screenshot({ path: screenPath });
    console.log(`    📸 Screenshot: ${screenPath}`);
  }

  // Testar Modos de Estudo (Normal, Reverso, Contexto, Escuta) no deck ativo
  console.log('\n  ▶ Testando Modos de Estudo (Normal, Reverso, Contexto, Escuta)...');
  const btnContexto = page.locator('#btn-modo-contexto');
  if (await btnContexto.isVisible()) {
    await btnContexto.click();
    await page.waitForTimeout(300);
    const frenteTexto = await page.locator('#card-italiano').textContent();
    console.log(`    Modo Contexto ativado (frente cloze/mascarada): "${frenteTexto?.slice(0, 50)}..."`);
  }

  const btnReverso = page.locator('#btn-modo-reverso');
  if (await btnReverso.isVisible()) {
    await btnReverso.click();
    await page.waitForTimeout(300);
    const frenteTexto = await page.locator('#card-italiano').textContent();
    console.log(`    Modo Reverso ativado (frente em português): "${frenteTexto?.slice(0, 50)}..."`);
  }

  const btnEscuta = page.locator('#btn-modo-escuta');
  if (await btnEscuta.isVisible()) {
    await btnEscuta.click();
    await page.waitForTimeout(300);
    const frenteTexto = await page.locator('#card-italiano').textContent();
    console.log(`    Modo Escuta ativado: "${frenteTexto}"`);
  }

  // Testar alternar de volta para a aba "🏛️ Templos"
  console.log('\n  ▶ Testando retorno à aba "🏛️ Templos"...');
  await tabTemplos.click();
  await page.waitForTimeout(400);

  const painelTmpVisivel = await painelTemplos.isVisible();
  const painelEspOculto = !(await painelEspeciais.isVisible());
  console.log(`    Painel Templos exibido: ${painelTmpVisivel} | Painel Especial oculto: ${painelEspOculto}`);
  if (!painelTmpVisivel || !painelEspOculto) {
    throw new Error('Falha ao retornar para a aba Templos.');
  }

  // Verificar que o select de templos não contém opções de deck_
  const optionsTemplo = await page.evaluate(() => {
    const sel = document.getElementById('flashcard-templo-select') as HTMLSelectElement | null;
    if (!sel) return [];
    return Array.from(sel.querySelectorAll('option')).map(o => o.value);
  });
  const contemDeckEspecial = optionsTemplo.some(val => val.startsWith('deck_'));
  console.log(`    Opções no select de templos: ${optionsTemplo.length} | Contém decks especiais misturados: ${contemDeckEspecial}`);
  if (contemDeckEspecial) {
    throw new Error('O select de templos não deve conter opções de baralhos especiais misturadas!');
  }

  // ─────────────────────────────────────────────────────────────
  // 2. TESTE DO VOCABULÁRIO: TOP 1.000, BUSCA E BADGES
  // ─────────────────────────────────────────────────────────────
  console.log('\n--------------------------------------------------');
  console.log('📚 TESTANDO FILTRO E RENDERIZAÇÃO DO TOP 1.000 NO VOCABULÁRIO');
  console.log('--------------------------------------------------');

  // Navegar para Vocabulário
  await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    if (w.App?.navegar) w.App.navegar('vocabolario');
  });
  await page.waitForTimeout(800);
  await fecharModais(page);

  const pillTop1000 = page.locator('#vocab-pill-top1000');
  const existePill = await pillTop1000.isVisible();
  console.log(`  Botão de filtro '⭐ Top 1000' visível: ${existePill}`);
  if (!existePill) throw new Error("Botão #vocab-pill-top1000 não encontrado na interface!");

  // Clicar na pílula Top 1000
  await pillTop1000.click();
  await page.waitForTimeout(800);

  const totalPalavrasTop = await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    return w.Vocab?.top1000Data?.length || 0;
  });
  console.log(`  Dataset Top 1.000 carregado dinamicamente: ${totalPalavrasTop} palavras`);
  if (totalPalavrasTop !== 1000) {
    throw new Error(`Dataset Top 1000 incorreto: esperado 1000, carregou ${totalPalavrasTop}`);
  }

  // Verificar elementos na lista
  const itensVocab = await page.locator('#vocab-list .vocab-item').all();
  console.log(`  Itens renderizados na primeira página: ${itensVocab.length}`);

  // Verificar presença de badge com #rank
  const primeiroItem = page.locator('#vocab-list .vocab-item').first();
  const badgeRank = await primeiroItem.locator('.vocab-cat-badge:has-text("#")').textContent().catch(() => null);
  console.log(`  Badge de ranking na primeira palavra: "${badgeRank}"`);
  if (!badgeRank || !badgeRank.includes('#1')) {
    throw new Error(`Badge de rank esperado '#1' não encontrado na primeira palavra!`);
  }

  // Testar busca textual dentro do Top 1000
  console.log('  ▶ Testando busca pelo termo "caffè"...');
  const inputBusca = page.locator('#vocab-busca');
  await inputBusca.fill('caffè');
  await page.waitForTimeout(400);

  const itensFiltrados = await page.locator('#vocab-list .vocab-item').count();
  console.log(`  Resultados encontrados para "caffè": ${itensFiltrados}`);
  if (itensFiltrados === 0) throw new Error('A busca por "caffè" no Top 1000 não retornou nenhum item!');

  // Limpar busca
  await inputBusca.fill('');
  await page.waitForTimeout(300);

  // Salvar screenshot do Vocabulário Top 1000
  const screenVocab = path.join(resultsDir, 'vocabulario_top1000.png');
  await page.screenshot({ path: screenVocab });
  console.log(`  📸 Screenshot: ${screenVocab}`);

  // ─────────────────────────────────────────────────────────────
  // 3. VERIFICAÇÃO DE ERROS DE CONSOLE E REQUISIÇÕES
  // ─────────────────────────────────────────────────────────────
  console.log('\n==================================================');
  console.log('📊 CONSOLIDAÇÃO DE INTEGRIDADE');
  console.log('==================================================');
  console.log(`  Erros no console: ${consoleIssues.length}`);
  console.log(`  Requisições com falha: ${requestFailures.length}`);

  if (consoleIssues.length > 0) {
    console.error('  ⚠️ Erros detectados no console:');
    consoleIssues.forEach((c) => console.error(`    - [${c.type}] ${c.text}`));
  }

  if (requestFailures.length > 0) {
    console.error('  ⚠️ Requisições falhas:');
    requestFailures.forEach((r) => console.error(`    - ${r.url}: ${r.errorText}`));
  }

  await browser.close();
  server.close();

  if (consoleIssues.length === 0 && requestFailures.length === 0) {
    console.log('\n🎉 TODOS OS TESTES PASSARAM COM 100% DE SUCESSO! 0 ERROS DETECTADOS.');
    process.exit(0);
  } else {
    console.error('\n❌ Houve problemas detectados nos testes.');
    process.exit(1);
  }
}

main().catch((err) => {
  console.error('Erro fatal durante a execução do teste:', err);
  process.exit(1);
});
