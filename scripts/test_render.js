const fs = require('fs');
const g = JSON.parse(fs.readFileSync('./data/grammar.json'));

const htmlFases = function(u) {
  let html = '';
  
  if (u.alerta) html += u.alerta;
  if (u.inventario && u.inventario.length) html += u.inventario.join('');
  if (u.definicao) {
    if (u.definicao.fenomeno) html += u.definicao.fenomeno;
    if (u.definicao.causa) html += u.definicao.causa;
    if (u.definicao.conceito) html += u.definicao.conceito;
  }
  if (u.tecnica) html += u.tecnica;
  
  if (u.exemplos_prc && u.exemplos_prc.length) {
    u.exemplos_prc.forEach(e => {
      html += e.oracao || '';
      html += e.pergunta || '';
      html += e.resposta || '';
      html += e.conclusao || '';
    });
  }
  
  if (u.ponte) html += u.ponte;
  if (u.coda) html += u.coda;

  if (u.observacao_cards) {
    u.observacao_cards.forEach(c => {
      html += c.italiano;
      html += c.traducao;
      html += c.motivo;
    });
  }

  if (u.armadilhas) {
    u.armadilhas.forEach(a => {
      html += a.errado;
      html += a.certo;
      html += a.motivo;
    });
  }
  
  return html;
};

let errors = [];
g.moduli.forEach(m => {
  m.lezioni.forEach(u => {
    try {
      htmlFases(u);
    } catch(e) {
      errors.push(`Error in ${m.id} - ${u.titulo}: ${e.message}`);
    }
  });
});

console.log(errors.length > 0 ? errors : "No rendering errors.");
