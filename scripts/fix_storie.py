"""
fix_storie.py — Corrige storie.json:
  1. Remove IDs duplicados entre contos originais e filosofia
  2. Mescla segmentos do mesmo título em uma única história
  3. Atribui ícones por filósofo/tema
"""
import json, re
from pathlib import Path

ICONS = {
    'socrate':   '🦉',
    'platone':   '🏛️',
    'aristotele':'📐',
    'epicuro':   '🌿',
    'marco':     '🛡️',
    'seneca':    '✍️',
    'plotino':   '✨',
    'nietzsche': '⚡',
    'descartes': '🧠',
}

def icon_for(title: str) -> str:
    t = title.lower()
    for key, ico in ICONS.items():
        if key in t:
            return ico
    return '📜'

def slug(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[''`]", '', s)
    s = re.sub(r'[^a-z0-9]+', '_', s)
    return s.strip('_')[:30]

src = Path(__file__).parent.parent / 'data' / 'storie.json'
data = json.loads(src.read_text(encoding='utf-8'))
stories = data['storie']

originals = [s for s in stories if 'titulo' in s]   # schema correto
philosophy = [s for s in stories if 'titolo' in s]   # schema alternativo

# Mesclar segmentos pelo título
merged: dict[str, dict] = {}
for s in philosophy:
    title = s['titolo']
    if title not in merged:
        merged[title] = {
            'id':           f'fil_{slug(title)}',
            'titulo':       title,
            'titulo_pt':    title,
            'nivel':        s.get('livello', 'C2'),
            'icone':        icon_for(title),
            'autor':        s.get('autor', 'Filosofia Classica'),
            'tema':         s.get('tema', 'filosofia'),
            'descricao':    s.get('tema', 'filosofia').capitalize(),
            'descricao_pt': s.get('tema', 'filosofia').capitalize(),
            'xp_recompensa': 80,
            '_testo_raw':   [],
        }
    merged[title]['_testo_raw'].append(s.get('testo', ''))

# Converter testo raw em array de parágrafos
def to_paragraphs(texts: list[str]) -> list[dict]:
    paras = []
    idx = 0
    for text in texts:
        frases = re.split(r'(?<=[.!?])\s+', text.strip())
        chunk_size = 3
        for i in range(0, len(frases), chunk_size):
            chunk = ' '.join(frases[i:i+chunk_size]).strip()
            if chunk:
                paras.append({'id': f'p{idx}', 'italiano': chunk, 'portugues': '', 'parole': []})
                idx += 1
    return paras

phil_list = []
for title, story in merged.items():
    story['testo'] = to_paragraphs(story.pop('_testo_raw'))
    phil_list.append(story)

# Ordenar por filósofo (autor) para agrupar bem
phil_list.sort(key=lambda s: (s['autor'], s['titulo']))

data['storie'] = originals + phil_list
src.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'OK: {len(originals)} originais + {len(phil_list)} filosofia = {len(data["storie"])} total')
for s in phil_list:
    print(f'  {s["id"]:35s} {s["nivel"]} {s["titulo"]}')
