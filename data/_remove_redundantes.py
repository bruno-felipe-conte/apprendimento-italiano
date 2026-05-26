import json, shutil

PATH = 'data/grammar.json'
shutil.copy(PATH, PATH + '.bak')

d = json.load(open(PATH, encoding='utf-8'))

# IDs a remover por serem redundantes com A1
REMOVER = {
    'A2': {'A2-01', 'A2-03', 'A2-04'},  # Passato Prossimo, Imperfetto, Preposizioni Articolate
    'B1': {'B1-02', 'B1-03'},           # Condizionale Presente, Gerundio
}

for mod in d['moduli']:
    if mod['id'] in REMOVER:
        antes = len(mod['unidades'])
        mod['unidades'] = [u for u in mod['unidades'] if u['id'] not in REMOVER[mod['id']]]
        depois = len(mod['unidades'])
        print(f"{mod['id']}: {antes} -> {depois} unidades")
        for u in mod['unidades']:
            print(f"  [KEPT] {u['num']} - {u['titulo']}")

json.dump(d, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('\ngrammar.json atualizado.')
