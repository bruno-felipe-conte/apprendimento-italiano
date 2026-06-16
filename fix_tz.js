const fs = require('fs');
const glob = require('fs');

const files = ['js/core.js', 'js/profilo.js', 'js/progression.js', 'js/heatmap.js'];
files.forEach(f => {
  if (fs.existsSync(f)) {
    let text = fs.readFileSync(f, 'utf8');
    text = text.replace(/new Date\(\)\.toISOString\(\)\.slice\(0, ?10\)/g, "new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10)");
    text = text.replace(/now\.toISOString\(\)\.slice\(0, ?10\)/g, "new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10)");
    text = text.replace(/d\.toISOString\(\)\.slice\(0, ?10\)/g, "new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10)");
    fs.writeFileSync(f, text, 'utf8');
  }
});
console.log('Fixed timezone dates.');
