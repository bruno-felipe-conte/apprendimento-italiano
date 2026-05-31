const fs = require('fs');
const indexPath = './index.html';
let css = fs.readFileSync(indexPath, 'utf8');

// 1. Tipografia Atkinson
css = css.replace(
  '<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lato:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">',
  '<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Cinzel:wght@400;600;700&family=Lato:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">'
);

css = css.replace(
  "body { font-family: 'Lato', sans-serif;",
  "body { font-family: 'Atkinson Hyperlegible', 'Lato', sans-serif;"
);

const replacements = {
  '.gram-inventario': '{ margin: 0; padding: 0.75rem 1rem 0.75rem 2rem; font-size: 0.92rem; color: #1e1e1e; line-height: 2.1; letter-spacing: 0.018em; }',
  '.gram-def-corpo': '{ padding: 0.75rem 0.85rem; font-size: 0.9rem; color: #1e1e1e; line-height: 1.85; letter-spacing: 0.015em; }',
  '.gram-tecnica-corpo': '{ padding: 0.85rem 1.1rem; font-size: 0.93rem; color: #1e1e1e; line-height: 2.05; letter-spacing: 0.015em; }',
  '.gram-prc-pq': '{ display: flex; align-items: baseline; gap: 0.55rem; padding: 0.6rem 0.85rem; font-size: 0.88rem; color: #2c2c2c; border-top: 1px solid #f0e8d8; line-height: 1.7; }',
  '.gram-prc-conclusao': '{ display: flex; align-items: baseline; gap: 0.55rem; padding: 0.65rem 0.85rem; background: #f0f9f4; border-top: 1px solid #c8e6c9; font-size: 0.9rem; line-height: 1.7; font-weight: 700; }',
  '.gram-prc-oracao': '{ background: #f9f4ee; padding: 0.7rem 0.85rem; font-size: 0.95rem; color: #5C0E1A; cursor: pointer; line-height: 1.6; letter-spacing: 0.02em; }',
  '.gram-prc-lista': '{ padding: 0.6rem 1rem 1rem; display: flex; flex-direction: column; gap: 1.2rem; }',
  '.gram-ponte-corpo': '{ padding: 0.85rem 1.1rem; font-size: 0.93rem; color: #1e1e1e; line-height: 2.0; letter-spacing: 0.015em; }',
  '.gram-coda': '{ background: #2c2c2c; color: #F5EDD8; padding: 0.85rem 1.1rem; border-radius: 8px; font-size: 0.9rem; font-style: normal; line-height: 1.85; letter-spacing: 0.02em; }',
  '.gram-camada-label': '{ background: #f5ece0; padding: 0.4rem 1rem; font-size: 0.76rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #9B2335; border-bottom: 1px solid #ede5d5; }',
  '.gram-def-label': '{ padding: 0.35rem 0.75rem; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }',
  '.gram-prc-tag': '{ display: inline-block; background: #9B2335; color: white; border-radius: 4px; font-size: 0.72rem; font-weight: 800; padding: 0.15rem 0.45rem; flex-shrink: 0; min-width: 1.4rem; text-align: center; }',
  '.gram-ex-question': '{ padding: 1.3rem 1.5rem 1.1rem; font-size: 1.08rem; font-weight: 700; color: #1a1a1a; line-height: 1.75; border-bottom: 1px solid #f0e8d8; letter-spacing: 0.01em; }',
  '.gram-ex-dica': '{ background: #fffbf0; border-left: 4px solid #D4A843; border-radius: 0 8px 8px 0; padding: 0.65rem 1rem; font-size: 0.88rem; color: #5a4500; margin: 0.5rem 0 1rem; line-height: 1.7; letter-spacing: 0.01em; }',
  '.gram-lesson-layout': '{ display: flex; flex-direction: column; gap: 1.8rem; }',
  '.gram-ex-progress-label': '{ font-size: 0.82rem; color: #9B2335; margin-bottom: 0.55rem; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; }',
  '.gram-alerta': '{ background: linear-gradient(135deg, #9B2335 0%, #6B1525 100%); color: #F5EDD8; padding: 1rem 1.25rem; border-radius: 10px; font-size: 0.95rem; font-weight: 600; line-height: 1.75; letter-spacing: 0.015em; }',
  '.gram-lesson-subtitle': '{ font-size: 0.88rem; color: #888; margin-top: 0.35rem; font-style: normal; font-weight: 400; letter-spacing: 0.02em; }',
  '.gram-res-msg': '{ font-style: normal; color: #666; margin: 0.8rem 0 1.2rem; font-size: 0.95rem; font-weight: 600; }'
};

// Replace class bodies globally
for (const [cls, newRules] of Object.entries(replacements)) {
  // Regex to find class definition and its body, replacing it entirely
  const regex = new RegExp(`\\${cls}\\s*\\{[^}]+\\}`, 'g');
  css = css.replace(regex, `${cls} ${newRules}`);
}

// Hover effect for PRC
if (!css.includes('.gram-prc-row:hover')) {
  css = css.replace(
    /\.gram-prc-row\s*\{[^}]+\}/,
    match => match + `\n    .gram-prc-row:hover { box-shadow: 0 0 0 2px #D4A843; border-color: #D4A843; transition: box-shadow 0.18s, border-color 0.18s; }`
  );
}

// 3. Responsividade aprimorada
// Append @media to the end of the <style> block
if (!css.includes('.gram-lesson-layout { padding: 0 0.5rem;')) {
  const mediaQuery = `
    @media (max-width: 640px) {
      .gram-lesson-layout { padding: 0 0.5rem; gap: 1.5rem; }
      .gram-prc-row { flex-direction: column; align-items: flex-start; padding: 0.8rem; }
      .gram-prc-tag { margin-bottom: 0.4rem; }
      .gram-ex-question { font-size: 1rem; padding: 1rem 1.2rem; }
      .gram-option { padding: 0.85rem 1.1rem; font-size: 0.9rem; }
    }
  </style>`;
  css = css.replace('</style>', mediaQuery);
}

fs.writeFileSync(indexPath, css);
console.log("Dyslexia replacements finished perfectly.");
