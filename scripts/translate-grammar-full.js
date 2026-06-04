// ============================================================
// translate-grammar-full.js
// Traduz grammar.json PT→IT em lotes, produzindo grammar-it.json
// Cobre: titulo, subtitulo, alerta, inventario, definicao, tecnica,
//        ponte, coda, tabela_visual, exemplos_prc, observacao_cards,
//        armadilhas, exercicios.pergunta, exercicios.explicacao
// ============================================================

const fs    = require('fs');
const path  = require('path');
const translate = require('google-translate-api-x');

const INPUT   = path.join(__dirname, '../data/grammar.json');
const OUTPUT  = path.join(__dirname, '../data/grammar-it.json');
const PROGRESS= path.join(__dirname, '../data/grammar-it-progress.json');

const BATCH_SIZE = 15;   // strings per API call
const DELAY_MS   = 220;  // ms between batch calls

const delay = ms => new Promise(r => setTimeout(r, ms));

// ── Translation cache (avoid re-translating same string) ──────────
const cache = new Map();

async function translateBatch(strings) {
  // Filter empty/non-string
  const valid = strings.map((s, i) => ({ s, i })).filter(({ s }) => typeof s === 'string' && s.trim());
  if (!valid.length) return strings.map(s => s);

  // Check cache
  const uncached = valid.filter(({ s }) => !cache.has(s));

  if (uncached.length > 0) {
    try {
      const texts = uncached.map(({ s }) => s);
      const results = await translate(texts, { from: 'pt', to: 'it' });
      const resultArr = Array.isArray(results) ? results : [results];
      uncached.forEach(({ s }, idx) => {
        cache.set(s, resultArr[idx]?.text ?? s);
      });
    } catch (err) {
      console.error(`  ⚠ Erro no batch: ${err.message} — retentando em 2s...`);
      await delay(2000);
      try {
        const texts = uncached.map(({ s }) => s);
        const results = await translate(texts, { from: 'pt', to: 'it' });
        const resultArr = Array.isArray(results) ? results : [results];
        uncached.forEach(({ s }, idx) => {
          cache.set(s, resultArr[idx]?.text ?? s);
        });
      } catch (err2) {
        console.error(`  ✗ Falhou 2x, mantendo original.`);
        uncached.forEach(({ s }) => cache.set(s, s));
      }
    }
  }

  return strings.map(s => (typeof s === 'string' && s.trim()) ? (cache.get(s) ?? s) : s);
}

// ── Translate a single string ─────────────────────────────────────
async function t(str) {
  if (!str || typeof str !== 'string') return str;
  const [res] = await translateBatch([str]);
  return res;
}

// ── Translate an array of strings ─────────────────────────────────
async function tArr(arr) {
  if (!Array.isArray(arr)) return arr;
  const results = [];
  for (let i = 0; i < arr.length; i += BATCH_SIZE) {
    const batch = arr.slice(i, i + BATCH_SIZE);
    const translated = await translateBatch(batch);
    results.push(...translated);
    if (i + BATCH_SIZE < arr.length) await delay(DELAY_MS);
  }
  return results;
}

// ── Strip HTML tags for translation, then reinsert ────────────────
// (google translate handles HTML reasonably well, so we pass raw)
async function tHtml(html) {
  if (!html || typeof html !== 'string') return html;
  // Pass HTML directly — Google Translate preserves tags
  const [res] = await translateBatch([html]);
  return res;
}

// ── Process a single lesson ───────────────────────────────────────
async function processLeicao(lez, modId, lezNum) {
  process.stdout.write(`    L${lezNum} ${lez.titulo?.substring(0,30)}... `);

  // Collect all simple string fields in one batch
  const simpleFields = ['titulo', 'subtitulo', 'alerta', 'tecnica', 'ponte', 'coda'];
  const simpleVals = simpleFields.map(f => lez[f] || '');
  const simpleTrans = await tArr(simpleVals);
  simpleFields.forEach((f, i) => { if (lez[f]) lez[f] = simpleTrans[i]; });
  await delay(DELAY_MS);

  // inventario: array of strings
  if (Array.isArray(lez.inventario) && lez.inventario.length) {
    lez.inventario = await tArr(lez.inventario);
    await delay(DELAY_MS);
  }

  // definicao: {fenomeno (IT), causa (PT), conceito (PT)}
  if (lez.definicao && typeof lez.definicao === 'object') {
    const defFields = ['causa', 'conceito'].filter(f => lez.definicao[f]);
    if (defFields.length) {
      const defVals = defFields.map(f => lez.definicao[f]);
      const defTrans = await tArr(defVals);
      defFields.forEach((f, i) => { lez.definicao[f] = defTrans[i]; });
      await delay(DELAY_MS);
    }
  }

  // tabela_visual: HTML string
  if (lez.tabela_visual) {
    lez.tabela_visual = await tHtml(lez.tabela_visual);
    await delay(DELAY_MS);
  }

  // exemplos_prc: array of {oracao (IT), pergunta (PT), resposta (PT)}
  if (Array.isArray(lez.exemplos_prc) && lez.exemplos_prc.length) {
    const perguntas = lez.exemplos_prc.map(e => e.pergunta || '');
    const respostas = lez.exemplos_prc.map(e => e.resposta || '');
    const pTrans = await tArr(perguntas);
    await delay(DELAY_MS);
    const rTrans = await tArr(respostas);
    await delay(DELAY_MS);
    lez.exemplos_prc.forEach((e, i) => {
      if (e.pergunta) e.pergunta = pTrans[i];
      if (e.resposta) e.resposta = rTrans[i];
    });
  }

  // observacao_cards: array of {italiano (IT), traducao (PT), artigo (IT), genero (PT), motivo (PT)}
  if (Array.isArray(lez.observacao_cards) && lez.observacao_cards.length) {
    const trad = lez.observacao_cards.map(c => c.traducao || '');
    const gen  = lez.observacao_cards.map(c => c.genero   || '');
    const mot  = lez.observacao_cards.map(c => c.motivo   || '');
    const [tT, tG, tM] = await Promise.all([tArr(trad), tArr(gen), tArr(mot)]);
    await delay(DELAY_MS);
    lez.observacao_cards.forEach((c, i) => {
      if (c.traducao) c.traducao = tT[i];
      if (c.genero)   c.genero   = tG[i];
      if (c.motivo)   c.motivo   = tM[i];
    });
  }

  // armadilhas: array of {errado (IT), certo (IT), motivo (PT)}
  if (Array.isArray(lez.armadilhas) && lez.armadilhas.length) {
    const motivos = lez.armadilhas.map(a => a.motivo || '');
    const mTrans  = await tArr(motivos);
    await delay(DELAY_MS);
    lez.armadilhas.forEach((a, i) => { if (a.motivo) a.motivo = mTrans[i]; });
  }

  // exercicios: pergunta + explicacao
  const exs = lez.exercicios || [];
  const perguntas  = exs.map(e => e.pergunta   || '');
  const explicacoes = exs.map(e => e.explicacao || '');

  for (let i = 0; i < perguntas.length; i += BATCH_SIZE) {
    const pBatch = perguntas.slice(i, i + BATCH_SIZE);
    const eBatch = explicacoes.slice(i, i + BATCH_SIZE);
    const [pT, eT] = await Promise.all([translateBatch(pBatch), translateBatch(eBatch)]);
    pBatch.forEach((_, j) => {
      if (exs[i+j].pergunta)   exs[i+j].pergunta   = pT[j];
      if (exs[i+j].explicacao) exs[i+j].explicacao = eT[j];
    });
    await delay(DELAY_MS);
  }

  process.stdout.write(`✓\n`);
}

// ── Main ──────────────────────────────────────────────────────────
async function run() {
  console.log('═══════════════════════════════════════════');
  console.log('  Tradução Profunda: grammar.json → PT→IT');
  console.log('═══════════════════════════════════════════\n');

  console.log('Lendo grammar.json...');
  const data = JSON.parse(fs.readFileSync(INPUT, 'utf-8'));

  // Load progress if exists (resume support)
  let startModule = 0, startLesson = 0;
  let outputData = { moduli: [] };
  if (fs.existsSync(PROGRESS)) {
    const prog = JSON.parse(fs.readFileSync(PROGRESS, 'utf-8'));
    startModule = prog.modIdx || 0;
    startLesson = prog.lezIdx || 0;
    if (fs.existsSync(OUTPUT)) {
      outputData = JSON.parse(fs.readFileSync(OUTPUT, 'utf-8'));
      console.log(`Retomando do módulo ${startModule}, lição ${startLesson}...`);
    }
  }

  const totalMods = data.moduli.length;
  let globalLez = 0;

  for (let mi = 0; mi < totalMods; mi++) {
    const modOriginal = data.moduli[mi];

    // Ensure output has this module entry
    if (!outputData.moduli[mi]) {
      outputData.moduli[mi] = JSON.parse(JSON.stringify(modOriginal));
    }
    const mod = outputData.moduli[mi];

    if (mi < startModule) {
      globalLez += modOriginal.lezioni.length;
      continue;
    }

    console.log(`\n📚 Módulo ${mi+1}/${totalMods}: ${modOriginal.id} — ${modOriginal.nome}`);
    if (mi === startModule && startLesson === 0) {
      mod.nome = await t(modOriginal.nome);
    }

    const totalLez = modOriginal.lezioni.length;
    for (let li = 0; li < totalLez; li++) {
      globalLez++;
      if (mi === startModule && li < startLesson) continue;

      const lezOriginal = JSON.parse(JSON.stringify(modOriginal.lezioni[li]));
      mod.lezioni[li] = lezOriginal;

      await processLeicao(mod.lezioni[li], modOriginal.id, li + 1);

      // Save progress after each lesson
      fs.writeFileSync(OUTPUT, JSON.stringify(outputData, null, 2), 'utf-8');
      fs.writeFileSync(PROGRESS, JSON.stringify({ modIdx: mi, lezIdx: li + 1 }), 'utf-8');
    }

    // Mark module done
    fs.writeFileSync(PROGRESS, JSON.stringify({ modIdx: mi + 1, lezIdx: 0 }), 'utf-8');
    console.log(`  ✅ Módulo ${modOriginal.id} concluído.`);
  }

  // Cleanup progress file
  if (fs.existsSync(PROGRESS)) fs.unlinkSync(PROGRESS);

  console.log('\n═══════════════════════════════════════════');
  console.log('  ✅ Tradução completa! grammar-it.json salvo.');
  console.log('═══════════════════════════════════════════');
}

run().catch(err => {
  console.error('\n✗ Erro fatal:', err.message);
  process.exit(1);
});
