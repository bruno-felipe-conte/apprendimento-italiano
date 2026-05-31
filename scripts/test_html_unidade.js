const fs = require('fs');
const js = fs.readFileSync('./js/grammar.js', 'utf8');

// Mock DOM
global.document = {
  getElementById: () => ({ innerHTML: '' })
};
global.window = { scrollTo: () => {} };

// Evaluate Grammatica class definition
let code = js.substring(js.indexOf('const Grammatica = {'));
code = code.substring(0, code.indexOf('window.Grammatica = Grammatica;'));
eval(code);

// Inject mock data
const g = JSON.parse(fs.readFileSync('./data/grammar.json'));
Grammatica.dados = g;

console.log("Testing A1-04...");
try {
  Grammatica.abrirUnidade('A1', 'A1-04');
  console.log("A1-04 success!");
} catch(e) {
  console.log("A1-04 error:", e);
}

console.log("Testing a2-i...");
try {
  Grammatica.abrirUnidade('A2', 'a2-i');
  console.log("a2-i success!");
} catch(e) {
  console.log("a2-i error:", e);
}
