const fs = require('fs');

const f1 = 'js/ia-import.js';
if (fs.existsSync(f1)) {
  let text = fs.readFileSync(f1, 'utf8');
  text = text.replace(/localStorage\.setItem\((key), JSON\.stringify\((.*?)\)\);/g, 
    "try { localStorage.setItem($1, JSON.stringify($2)); } catch(e) { if(e.name === 'QuotaExceededError') { App.notificar('Memoria piena! Elimina vecchie storie/canzoni.', 'erro'); } }");
  fs.writeFileSync(f1, text, 'utf8');
}

console.log('Fixed ia-import storage quota');
