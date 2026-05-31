import json

with open('data/mod2.json', encoding='utf-8') as f:
    data = json.load(f)

with open('output_b1.txt', 'w', encoding='utf-8') as out:
    for u in data['unidades']:
        out.write(f"ID: {u['id']}\n")
        out.write(f"TITULO: {u.get('titulo', '')}\n")
        out.write(f"TECNICA: {u.get('tecnica', '')}\n")
        out.write("-" * 40 + "\n")
