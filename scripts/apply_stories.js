const fs = require('fs');
const path = require('path');

const storieFile = path.join(__dirname, '../data/storie.json');
const batches = [
  path.join(__dirname, 'stories_batch1.json'),
  path.join(__dirname, 'stories_batch2.json'),
  path.join(__dirname, 'stories_batch3.json'),
  path.join(__dirname, 'stories_batch4.json'),
];

const data = JSON.parse(fs.readFileSync(storieFile, 'utf8'));

let updated = 0;

for (const batchFile of batches) {
  const batch = JSON.parse(fs.readFileSync(batchFile, 'utf8'));
  for (const newStory of batch) {
    const idx = data.storie.findIndex(s => s.id === newStory.id);
    if (idx === -1) {
      console.error(`ERROR: story not found: ${newStory.id}`);
      continue;
    }
    data.storie[idx].testo = newStory.testo;
    console.log(`Updated: ${newStory.id} (${newStory.testo.length} paragraphs)`);
    updated++;
  }
}

fs.writeFileSync(storieFile, JSON.stringify(data, null, 2), 'utf8');
console.log(`\nDone. Updated ${updated} stories.`);
