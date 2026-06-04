const fs = require('fs');
const translate = require('google-translate-api-x');

// Configs
const INPUT_FILE = '../data/grammar.json';
const OUTPUT_FILE = '../data/grammar-it.json';
const TARGET_LANG = 'it';
const SOURCE_LANG = 'pt';
const MODULE_TO_TEST = 'A1';

const delay = ms => new Promise(res => setTimeout(res, ms));

async function translateText(text) {
  if (!text || typeof text !== 'string') return text;
  // Se o texto j estiver em italiano, a prpria API vai lidar com isso ou podemos s enviar.
  // Evitar traduzir blocos vazios ou muito curtos.
  try {
    const res = await translate(text, { from: SOURCE_LANG, to: TARGET_LANG });
    return res.text;
  } catch (err) {
    console.error(`Erro ao traduzir: "${text.substring(0, 30)}..."`, err.message);
    return text; // fallback to original
  }
}

async function processModule(modulo) {
  console.log(`\nTratando Módulo: ${modulo.nome}`);
  modulo.nome = await translateText(modulo.nome);

  // LIMIT TO 1 LESSON FOR TESTING PURPOSES
  modulo.lezioni = modulo.lezioni.slice(0, 1);

  for (const lez of modulo.lezioni) {
    console.log(`  Traduzindo lição: ${lez.num} - ${lez.titulo}`);
    if (lez.subtitulo) lez.subtitulo = await translateText(lez.subtitulo);
    
    // As "descricoes" em grammar.json so arrays ou strings? Vamos garantir que seja tratado
    if (Array.isArray(lez.descricoes)) {
        for (let i = 0; i < lez.descricoes.length; i++) {
            lez.descricoes[i] = await translateText(lez.descricoes[i]);
            await delay(100);
        }
    }

    if (lez.exercicios) {
      let qCount = 1;
      for (const ex of lez.exercicios) {
        process.stdout.write(`    [Ex ${qCount++}] `);
        if (ex.pergunta) ex.pergunta = await translateText(ex.pergunta);
        await delay(150);
        if (ex.explicacao) ex.explicacao = await translateText(ex.explicacao);
        await delay(150);

        // Opcoes podem ser palavras isoladas em italiano j. Vamos ignorar a traduo de "opcoes" 
        // ou respostas a menos que seja um quiz longo. Em grammar, a "pergunta" j d o contexto.
        // ex.opcoes so as alternativas em italiano, no deve traduzir!
        
        // Se houver campos extras:
        if (ex.texto) ex.texto = await translateText(ex.texto);
        process.stdout.write('Ok.\n');
      }
    }
  }
}

async function run() {
  console.log('Lendo banco de dados original...');
  const data = JSON.parse(fs.readFileSync(INPUT_FILE, 'utf8'));
  
  // Isolar mdulo A1 para teste
  const moduleA1 = data.moduli.find(m => m.id === MODULE_TO_TEST);
  if (!moduleA1) {
    console.error('Mdulo A1 no encontrado!');
    return;
  }

  // Clona a estrutura para o arquivo de teste
  const testData = { moduli: [ moduleA1 ] };

  console.log(`\nIniciando traduo (Mdulo: ${MODULE_TO_TEST})...`);
  await processModule(testData.moduli[0]);

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(testData, null, 2), 'utf8');
  console.log(`\nConcludo! Salvo em ${OUTPUT_FILE}`);
}

run();
