const fs = require('fs');
const glob = require('fs');

const files = fs.readdirSync('js').filter(f => f.endsWith('.js')).map(f => 'js/' + f);
files.forEach(f => {
  const text = fs.readFileSync(f, 'utf8');
  if (text.includes('addEventListener')) {
    console.log('File:', f);
    const lines = text.split('\n');
    lines.forEach((l, i) => {
      if (l.includes('addEventListener')) console.log(i + 1, l.trim());
    });
  }
});
