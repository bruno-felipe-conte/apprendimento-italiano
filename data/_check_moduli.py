import json
d = json.load(open('data/grammar.json', encoding='utf-8'))
for mod in d['moduli']:
    if mod['id'] in ('A2','B1','B2'):
        print('MODULE:', mod['id'], '-', mod['nome'])
        for u in mod['unidades']:
            titulo = u['titulo']
            uid = u['id']
            num = u['num']
            nex = len(u['exercicios'])
            teoria_preview = u['teoria'][:150].replace('\n', ' ')
            print(f'  [{uid}] {num} - {titulo} ({nex} ex)')
            print(f'    {teoria_preview}...')
        print()
