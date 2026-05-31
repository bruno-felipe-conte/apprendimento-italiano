import json
with open('data/mod1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
with open('output.txt', 'w', encoding='utf-8') as out:
    for u in d.get('unidades', []):
        out.write(f"ID: {u.get('id')}\n")
        out.write(f"TITULO: {u.get('titulo')}\n")
        out.write(f"TECNICA: {u.get('tecnica')}\n")
        out.write("-" * 40 + "\n")
