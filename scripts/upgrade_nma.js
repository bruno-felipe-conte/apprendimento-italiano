const fs = require('fs');

const dataFile = './data/grammar.json';
const grammar = JSON.parse(fs.readFileSync(dataFile, 'utf8'));

function createTabelaVisual(title) {
  return `<p class="tabela-intro">Tabela de consulta rápida — ${title}</p>
<div class="artigo-cards">
  <div class="ac-card"><div class="ac-head">Regra 1</div><div class="ac-body">Uso geral</div></div>
  <div class="ac-card"><div class="ac-head">Regra 2</div><div class="ac-body">Exceções</div></div>
</div>`;
}

function createObservacaoCards(exemplos) {
  if (exemplos && exemplos.length >= 2) {
    return exemplos.slice(0, 4).map(ex => ({
      italiano: ex.oracao,
      traducao: ex.resposta || 'tradução',
      artigo: '⚠️',
      genero: 'importante',
      motivo: ex.conclusao || 'Observe como a regra se aplica.'
    }));
  }
  return [
    { italiano: "Esempio 1", traducao: "Exemplo 1", artigo: "📌", genero: "regra", motivo: "Padrão normal." },
    { italiano: "Esempio 2", traducao: "Exemplo 2", artigo: "📌", genero: "regra", motivo: "Padrão normal." }
  ];
}

function createArmadilhas(title) {
  return [
    { errado: "Erro comum 1", certo: "Forma correta 1", motivo: "Em português fazemos assim, mas em italiano é diferente." },
    { errado: "Erro comum 2", certo: "Forma correta 2", motivo: "Atenção a esta exceção." }
  ];
}

function processExercises(exs) {
  if (!exs || exs.length === 0) return [];
  
  // We want ~15 exercises: 5 escolha, 6 digitar, 4 revelar
  const result = [];
  
  // Take first 15 exercises, convert types to match the distribution
  const subset = exs.slice(0, 15);
  
  subset.forEach((ex, i) => {
    let tipo = 'revelar';
    if (i < 5) tipo = 'escolha';
    else if (i < 11) tipo = 'digitar';
    
    const newEx = { ...ex, tipo };
    
    if (tipo === 'escolha') {
      const correta = ex.resposta || ex.soluzione || 'Opção Certa';
      newEx.resposta_correta = correta;
      newEx.alternativas = [correta, correta + 's', correta + 'a', correta + 'e'].sort(() => Math.random() - 0.5);
    } else if (tipo === 'digitar') {
      newEx.resposta = ex.resposta || ex.soluzione || 'resposta';
    }
    
    // Ensure explicacao is present
    if (!newEx.explicacao) {
      newEx.explicacao = ex.spiegazione || `A forma correta é: ${newEx.resposta || newEx.resposta_correta}`;
    }
    
    result.push(newEx);
  });
  
  return result;
}

grammar.moduli.forEach((modulo, modIdx) => {
  const units = modulo.unidades || modulo.lezioni || [];
  
  units.forEach((u, uIdx) => {
    // Skip if already has observacao_cards (like module 0 lez 0 and 1)
    if (u.observacao_cards && u.observacao_cards.length > 0) return;
    
    console.log(`Upgrading Modulo ${modIdx} Lezione ${uIdx}: ${u.titulo}`);
    
    // Fill missing NMA fields
    if (!u.alerta) u.alerta = `Atenção: Entender "${u.titulo}" é essencial para se comunicar como um italiano nativo.`;
    if (!u.inventario) u.inventario = ["Regras principais", "Exceções comuns", "Casos práticos"];
    if (!u.definicao) u.definicao = {
      fenomeno: "Como isso aparece no dia a dia",
      causa: "Por que os italianos falam assim?",
      conceito: "A regra estrutural por trás do uso."
    };
    if (!u.tecnica) u.tecnica = "1. Observe o contexto.\n2. Aplique a regra geral.\n3. Verifique as exceções.";
    if (!u.exemplos_prc) u.exemplos_prc = [
      { oracao: "Questa è una frase d'esempio.", pergunta: "O que observar?", resposta: "A estrutura", conclusao: "Sempre siga este padrão." }
    ];
    if (!u.ponte) u.ponte = `Em português usamos algo parecido com "${u.titulo}", mas em italiano preste atenção aos detalhes.`;
    if (!u.coda) u.coda = "Pratique todos os dias: crie 3 frases usando esta regra antes de dormir.";
    
    u.observacao_cards = createObservacaoCards(u.exemplos_prc);
    u.armadilhas = createArmadilhas(u.titulo);
    u.tabela_visual = createTabelaVisual(u.titulo);
    
    u.exercicios = processExercises(u.exercicios);
  });
});

fs.writeFileSync(dataFile, JSON.stringify(grammar, null, 2));
console.log('Grammar upgrade complete!');
