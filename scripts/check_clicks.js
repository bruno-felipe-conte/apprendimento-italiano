const fs = require('fs');
const g = JSON.parse(fs.readFileSync('./data/grammar.json'));
console.log("A1:");
g.moduli[0].lezioni.slice(0, 5).forEach((u, i) => {
  console.log(`Index ${i} | Titulo: ${u.titulo} | ID: ${u.id} | HTML: <button onclick="Grammatica.abrirUnidade('A1', '${u.id}')">`);
});
console.log("A2:");
g.moduli[1].lezioni.slice(0, 5).forEach((u, i) => {
  console.log(`Index ${i} | Titulo: ${u.titulo} | ID: ${u.id} | HTML: <button onclick="Grammatica.abrirUnidade('A2', '${u.id}')">`);
});
