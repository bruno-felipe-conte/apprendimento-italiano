import sys, json
sys.stdout.reconfigure(encoding='utf-8')

with open('data/canzoni.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

songs = data['canzoni']

# Show estrofes of can_051
song = next(s for s in songs if s['id'] == 'can_051')
print('can_051 estrofes:')
for e in song['estrofes']:
    print(f'  estrofe {e.get("id")}: {repr(str(e)[:300])}')

print('\nvocabulario_chave:')
for v in song['vocabulario_chave']:
    print(f'  {repr(str(v)[:200])}')
