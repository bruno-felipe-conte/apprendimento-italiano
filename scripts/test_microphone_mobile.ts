import { chromium, type Page } from '@playwright/test';
import http from 'http';
import fs from 'fs';
import path from 'path';

interface WindowWithModules {
  _mockSrStarted?: boolean;
  App?: { navegar: (s: string) => void };
  Flashcards?: { init: (t: number) => void; toggleGravar: () => void };
  Imitazione?: {
    toggleGravacao: () => void;
    isRecording?: boolean;
    recognition?: {
      onerror?: (e: { error: string }) => void;
    };
  };
  SpeechRecognition?: unknown;
  webkitSpeechRecognition?: unknown;
}

function criarServidorEstatico(pastaRaiz: string): Promise<{ server: http.Server; url: string }> {
  const mimeTypes: Record<string, string> = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.ico': 'image/x-icon'
  };

  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      let reqPath = req.url ? req.url.split('?')[0] : '/';
      if (reqPath === '/') reqPath = '/index.html';
      const filePath = path.join(pastaRaiz, reqPath);

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
  await page.evaluate(() => {
    const ob = document.getElementById('onboarding-modal');
    if (ob) ob.style.display = 'none';
    const cq = document.getElementById('conquista-modal');
    if (cq) cq.style.display = 'none';
    const bk = document.getElementById('backup-reminder-popup');
    if (bk) bk.style.display = 'none';
  });
}

async function main(): Promise<void> {
  console.log('==================================================');
  console.log('📱 TESTE E2E: SUPORTE A MICROFONE EM BROWSERS MOBILE');
  console.log('==================================================\n');

  const rootDir = process.cwd();
  const { server, url } = await criarServidorEstatico(rootDir);
  console.log(`📡 Servidor de teste ativo em: ${url}`);

  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  // Emula dispositivo móvel (Pixel 7 / Android Chrome)
  const context = await browser.newContext({
    viewport: { width: 412, height: 915 },
    userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
    isMobile: true,
    hasTouch: true,
    permissions: ['microphone']
  });

  const page = await context.newPage();
  page.on('console', msg => console.log('  [Browser Console]', msg.text()));
  page.on('pageerror', err => console.log('  [Browser PageError]', err.message));

  // Injetar mock controlado de SpeechRecognition para validar o ciclo no mobile
  await page.addInitScript({
    content: `
      // Desativa ServiceWorker no ambiente de teste para prevenir controllerchange -> reload
      if (window.navigator && window.navigator.serviceWorker) {
        window.navigator.serviceWorker.register = function() {
          return new Promise(function() {});
        };
      }

      window._mockSrStarted = false;
      function MockSpeechRecognition() {
        this.lang = '';
        this.continuous = false;
        this.interimResults = false;
        this.maxAlternatives = 1;
        this.onstart = null;
        this.onresult = null;
        this.onerror = null;
        this.onend = null;
      }
      MockSpeechRecognition.prototype.start = function() {
        window._mockSrStarted = true;
        if (this.onstart) this.onstart();
        var self = this;
        setTimeout(function() {
          if (self.onresult) {
            self.onresult({
              results: [[{ transcript: 'buongiorno come stai' }]]
            });
          }
          if (self.onend) self.onend();
        }, 150);
      };
      MockSpeechRecognition.prototype.stop = function() {
        if (this.onend) this.onend();
      };
      window.SpeechRecognition = MockSpeechRecognition;
      window.webkitSpeechRecognition = MockSpeechRecognition;
    `
  });

  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(600);
  await fecharModais(page);

  // ─────────────────────────────────────────────────────────────
  // 1. TESTE NO MODO IMITAÇÃO (DOJO DE PRONÚNCIA)
  // ─────────────────────────────────────────────────────────────
  console.log('🎙️ [Teste 1] Modo Imitação em Dispositivo Mobile:');
  await page.evaluate(() => {
    const w = window as unknown as { App?: { navegar: (s: string) => void } };
    if (w.App?.navegar) w.App.navegar('imitazione');
  });
  
  // Aguarda a renderização assíncrona do container e botão de microfone
  const btnMic = page.locator('#dojo-btn-mic');
  await btnMic.waitFor({ state: 'visible', timeout: 10000 });
  const micVisivel = await btnMic.isVisible();
  console.log(`  Botão de microfone visível: ${micVisivel}`);
  if (!micVisivel) throw new Error('Botão #dojo-btn-mic não visível!');

  // Tocar no microfone
  console.log('  Clicando no microfone para falar...');
  await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    w.Imitazione?.toggleGravacao();
  });
  await page.waitForTimeout(500);

  const srIniciado = await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    return w._mockSrStarted === true;
  });
  console.log(`  SpeechRecognition.start() executado: ${srIniciado}`);
  if (!srIniciado) throw new Error('SpeechRecognition.start() não foi executado no clique!');

  // Aguardar processamento do resultado
  await page.waitForTimeout(600);

  const debugResultado = await page.evaluate(() => {
    const el = document.getElementById('imitazione-resultado');
    return {
      exists: !!el,
      display: el ? el.style.display : null,
      innerHTML: el ? el.innerHTML.slice(0, 100) : null
    };
  });
  console.log('  [Debug Resultado]', JSON.stringify(debugResultado));

  const resVisivel = debugResultado.exists && debugResultado.display !== 'none';
  console.log(`  Painel de diagnóstico de dicção exibido: ${resVisivel}`);
  if (!resVisivel) throw new Error('Painel de resultado #imitazione-resultado não foi exibido!');

  // ─────────────────────────────────────────────────────────────
  // 2. TESTE NOS FLASHCARDS (BOTÃO IMITAR)
  // ─────────────────────────────────────────────────────────────
  console.log('\n🃏 [Teste 2] Flashcards em Dispositivo Mobile:');
  await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    if (w.App?.navegar) w.App.navegar('flashcard');
    if (w.Flashcards?.init) w.Flashcards.init(1);
  });
  await page.waitForTimeout(600);
  await fecharModais(page);

  const btnImitar = page.locator('#btn-gravar');
  await btnImitar.waitFor({ state: 'visible', timeout: 10000 });
  const imitarVisivel = await btnImitar.isVisible();
  console.log(`  Botão "Imitar" (🎤) nos Flashcards visível: ${imitarVisivel}`);
  if (!imitarVisivel) throw new Error('Botão #btn-gravar não visível nos Flashcards!');

  // Clicar no botão Imitar
  console.log('  Clicando no botão "Imitar" nos flashcards...');
  await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    w.Flashcards?.toggleGravar();
  });
  await page.waitForTimeout(600);

  const fbVisivel = await page.locator('#imitacao-feedback').isVisible();
  const fbTexto = await page.locator('#imitacao-feedback').textContent();
  console.log(`  Feedback de pronúncia nos flashcards exibido: ${fbVisivel}`);
  console.log(`  Mensagem do feedback: "${fbTexto?.trim()}"`);
  if (!fbVisivel) throw new Error('Feedback #imitacao-feedback não foi exibido nos flashcards!');

  // ─────────────────────────────────────────────────────────────
  // 3. TESTE DE FEEDBACK DIAGNÓSTICO EM CASO DE ERROS MOBILE
  // ─────────────────────────────────────────────────────────────
  console.log('\n⚠️ [Teste 3] Mensagens Diagnósticas de Erro (Permissão, No-Speech):');
  const msgErro = await page.evaluate(() => {
    const w = window as unknown as WindowWithModules;
    if (w.Imitazione) {
      // Inicia gravação e imediatamente simula erro de permissão do navegador
      w.Imitazione.toggleGravacao();
      if (w.Imitazione.recognition && typeof w.Imitazione.recognition.onerror === 'function') {
        w.Imitazione.recognition.onerror({ error: 'not-allowed' });
      }
    }
    const st = document.getElementById('dojo-mic-status');
    return st ? st.innerText : '';
  });
  console.log(`  Mensagem para permissão negada: "${msgErro}"`);
  if (!msgErro.includes('Permissão negada')) {
    throw new Error('Mensagem amigável para permissão negada não exibida corretamente!');
  }

  console.log('\n==================================================');
  console.log('🎉 TESTE DE MICROFONE MOBILE FINALIZADO COM 100% DE SUCESSO!');
  console.log('==================================================');

  await browser.close();
  server.close();
}

main().catch((err) => {
  console.error('\n❌ ERRO NO TESTE:', err);
  process.exit(1);
});
