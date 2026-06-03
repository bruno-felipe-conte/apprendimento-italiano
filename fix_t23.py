import json

t23_add = [
    ('criceto', 'hamster', 'domestici', 'Il criceto gira sulla ruota.', 'O hamster gira na roda.', '/kriˈtʃeto/', 'm', 'criceti'),
    ('canarino', 'canário', 'domestici', 'Il canarino canta nella gabbia.', 'O canário canta na gaiola.', '/kanaˈrino/', 'm', 'canarini'),
    ('furetto', 'furão', 'domestici', 'Un furetto molto vivace.', 'Um furão muito vivo.', '/fuˈretto/', 'm', 'furetti'),
    ('libellula', 'libélula', 'insetti', 'Una libellula sullo stagno.', 'Uma libélula no lago.', '/liˈbɛllula/', 'f', 'libellule'),
    ('vespa', 'vespa', 'insetti', 'Attento alla vespa.', 'Cuidado com a vespa.', '/ˈvɛspa/', 'f', 'vespe'),
    ('lucciola', 'vagalume', 'insetti', 'Le lucciole illuminano la notte.', 'Os vagalumes iluminam a noite.', '/ˈluttʃola/', 'f', 'lucciole'),
    ('pulce', 'pulga', 'insetti', 'Il cane ha le pulci.', 'O cachorro tem pulgas.', '/ˈpultʃe/', 'f', 'pulci'),
    ('zecca', 'carrapato', 'insetti', 'Attento alle zecche nel bosco.', 'Cuidado com os carrapatos no bosque.', '/ˈtsekka/', 'f', 'zecche'),
    ('pidocchio', 'piolho', 'insetti', 'Lavare i capelli per i pidocchi.', 'Lavar os cabelos por causa dos piolhos.', '/piˈdɔkkjo/', 'm', 'pidocchi'),
    ('tonno', 'atum', 'marini', 'Un grande banco di tonni.', 'Um grande cardume de atuns.', '/ˈtonno/', 'm', 'tonni'),
    ('salmone', 'salmão', 'marini', 'Il salmone nuota controcorrente.', 'O salmão nada contra a corrente.', '/salˈmone/', 'm', 'salmoni'),
    ('calamaro', 'lula', 'marini', 'Un calamaro gigante.', 'Uma lula gigante.', '/kalaˈmaro/', 'm', 'calamari'),
    ('ostrica', 'ostra', 'marini', 'L\'ostrica contiene una perla.', 'A ostra contém uma pérola.', '/ˈɔstrika/', 'f', 'ostriche'),
    ('cozza', 'mexilhão', 'marini', 'Spaghetti con le cozze.', 'Espaguete com mexilhões.', '/ˈkɔttsa/', 'f', 'cozze'),
    ('pinguino_reale', 'pinguim real', 'uccelli', 'Il pinguino reale.', 'O pinguim real.', '/pinˈɡwino reˈale/', 'm', 'pinguini reali'),
    ('formichiere', 'tamanduá', 'selvatici', 'Il formichiere mangia le formiche.', 'O tamanduá come as formigas.', '/formiˈkjɛre/', 'm', 'formichieri')
]

path = 'c:/Users/bruno/Documents/italian-learning-app-pro/data/templo-23.json'
with open(path, 'r', encoding='utf-8') as f:
    obj = json.load(f)

current_count = len(obj['palavras'])

def w(tid, it, pt, cat, ex_it, ex_pt, ipa='', gen=None, pl=None):
    return {
        'id': tid, 'italiano': it, 'portugues': pt, 'genero': gen, 'plural': pl,
        'exemplo': ex_it, 'exemplo_pt': ex_pt, 'categoria': cat, 'dificuldade': 'medio', 'audio_ipa': ipa
    }

for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(t23_add, current_count + 1):
    tid = f't23_{i:03d}'
    obj['palavras'].append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))

with open(path, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)

print(f'T23 now has {len(obj["palavras"])} parole')
