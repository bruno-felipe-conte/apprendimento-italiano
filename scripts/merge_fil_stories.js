// Script de integração: lê scripts/new_fil_*.json e substitui o campo "testo" das histórias correspondentes em data/storie.json
// Uso: node scripts/merge_fil_stories.js
const fs = require('fs');
const path = require('path');

const BASE = path.resolve(__dirname, '..');
const STORIE_PATH = path.join(BASE, 'data', 'storie.json');
const SCRIPTS_DIR = __dirname;

function main() {
  console.log('[merge] Lendo storie.json...');
  const raw = fs.readFileSync(STORIE_PATH, 'utf8');
  const data = JSON.parse(raw);
  if (!data.storie || !Array.isArray(data.storie)) {
    throw new Error('Estrutura inesperada: data.storie não é array');
  }
  const newFiles = fs.readdirSync(SCRIPTS_DIR).filter(f => /^new_fil_.+\.json$/.test(f));
  console.log(`[merge] Encontrados ${newFiles.length} arquivos new_fil_*.json`);
  let updated = 0, skipped = 0;
  for (const f of newFiles) {
    const fp = path.join(SCRIPTS_DIR, f);
    let newObj;
    try {
      newObj = JSON.parse(fs.readFileSync(fp, 'utf8'));
    } catch (e) {
      console.error(`[merge] ERRO ao parsear ${f}: ${e.message}`);
      skipped++;
      continue;
    }
    if (!newObj.id || !Array.isArray(newObj.testo)) {
      console.error(`[merge] ERRO ${f}: faltam campos id ou testo[]`);
      skipped++;
      continue;
    }
    const target = data.storie.find(s => s.id === newObj.id);
    if (!target) {
      console.error(`[merge] ERRO ${f}: história ${newObj.id} não encontrada em storie.json`);
      skipped++;
      continue;
    }
    const oldLen = (target.testo || []).length;
    const newLen = newObj.testo.length;
    target.testo = newObj.testo;
    console.log(`[merge] OK ${newObj.id}: ${oldLen} -> ${newLen} parágrafos`);
    updated++;
  }
  // Backup
  const backupPath = STORIE_PATH + '.bak';
  fs.copyFileSync(STORIE_PATH, backupPath);
  console.log(`[merge] Backup criado em ${backupPath}`);
  // Save
  fs.writeFileSync(STORIE_PATH, JSON.stringify(data, null, 2), 'utf8');
  console.log(`[merge] Salvo: ${updated} atualizadas, ${skipped} ignoradas, ${newFiles.length} total`);
  // Validate
  const recheck = JSON.parse(fs.readFileSync(STORIE_PATH, 'utf8'));
  const stillGeneric = recheck.storie.filter(s => s.id.startsWith('fil_') && Array.isArray(s.testo) && s.testo[0] && typeof s.testo[0].italiano === 'string' && s.testo[0].italiano.startsWith("Nell'antica Accademia"));
  console.log(`[merge] Validação: ${stillGeneric.length} histórias fil_ ainda com texto genérico`);
}

main();
