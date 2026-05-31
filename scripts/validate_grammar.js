const fs = require('fs');
const g = JSON.parse(fs.readFileSync('./data/grammar.json'));

let errors = 0;
let warnings = 0;
let totalLezioni = 0;

g.moduli.forEach((mod, modIdx) => {
  const lez = mod.lezioni || mod.unidades;
  
  if (!lez || !Array.isArray(lez)) {
    console.log(`[ERRO] Módulo ${mod.id} não possui o array lezioni/unidades`);
    errors++;
    return;
  }
  
  lez.forEach((u, uIdx) => {
    totalLezioni++;
    const path = `Módulo ${mod.id} - Lição ${uIdx}`;
    
    if (!u.titulo) {
      console.log(`[ERRO] ${path} não tem titulo`);
      errors++;
    }
    
    if (!u.exercicios || !Array.isArray(u.exercicios) || u.exercicios.length === 0) {
      console.log(`[ERRO] ${path} (${u.titulo}) não tem exercícios`);
      errors++;
    } else {
      u.exercicios.forEach((ex, exIdx) => {
        if (!ex.tipo || !ex.pergunta) {
          console.log(`[ERRO] ${path} Exercício ${exIdx} malformado`);
          errors++;
        }
      });
    }
    
    if (!u.tabela_visual) {
      console.log(`[ERRO] ${path} (${u.titulo}) missing tabela_visual`);
      errors++;
    }
    
    if (!u.armadilhas || !Array.isArray(u.armadilhas)) {
      console.log(`[ERRO] ${path} (${u.titulo}) missing armadilhas`);
      errors++;
    }
    
    if (!u.observacao_cards || !Array.isArray(u.observacao_cards)) {
      console.log(`[ERRO] ${path} (${u.titulo}) missing observacao_cards`);
      errors++;
    }

    if (!u.alerta) warnings++;
  });
});

console.log(`=============================`);
console.log(`Validação Concluída!`);
console.log(`Total de lições analisadas: ${totalLezioni}`);
console.log(`Total de Erros críticos: ${errors}`);
console.log(`Total de Alertas: ${warnings}`);
console.log(`=============================`);
