import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VI")

novos = [
    # 30 exercícios sobre Futuro semplice e composto
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Futuro semplice regolare (-ARE):\nIo _____ (parlare) domani?", "resposta": "parlerò", "explicacao": "-ARE: Io -erò. Parlerò = Io parlerò."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Futuro semplice regolare (-ARE):\nTu _____ (parlare) domani?", "resposta": "parlerai", "explicacao": "-ARE: Tu -erai. Parlerai = Tu parlerai."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'he will speak'? A:", "opcoes": ["parlerà", "parla", "parlò"], "resposta": 0, "explicacao": "Parlerà = Parler + à. Terza persona singolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Futuro semplice regolare (-ARE):\nLei _____ (parlare) domani?", "resposta": "parlerà", "explicacao": "-ARE: Lei -erà. Parlerà = Lei parlerà."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Futuro semplice regolare (-ARE):\nNoi _____ (parlare) domani?", "resposta": "parleremo", "explicacao": "-ARE: Noi -eremo. Parleremo = Noi parleremo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'you will speak' in italiano?", "opcoes": ["parlerete", "parla", "parlere"], "resposta": 0, "explicacao": "Parlaterete = Voi parlerete. Seconda persona plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Futuro semplice regolare (-ARE):\nVoi _____ (parlare) domani?", "resposta": "parlerete", "explicacao": "-ARE: Voi -erete. Parlerete = Voi parlerete."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Futuro semplice regolare (-ARE):\nLoro _____ (parlare) domani?", "resposta": "parleranno", "explicacao": "-ARE: Loro -eranno. Parleranno = Loro parleranno."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I will speak'? A:", "opcoes": ["parlerò", "parlo", "parlarò"], "resposta": 0, "explicacao": "Parlerò = Io parlerò. Prima persona singolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Futuro semplice irregolare:\nIo _____ (essere) domani?", "resposta": "sarò", "explicacao": "ESSERE irregolare: sarò. Io sarò."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Futuro semplice irregolare:\nTu _____ (essere) domani?", "resposta": "sarai", "explicacao": "ESSERE irregolare: sarai. Tu sarai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he will be' in italiano?", "opcoes": ["sarà", "è", "era"], "resposta": 0, "explicacao": "Sarà = Lui sarà. Terza persona singolare di essere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Futuro semplice irregolare:\nLei _____ (essere) domani?", "resposta": "sarà", "explicacao": "ESSERE irregolare: sarà. Lei sarà."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Futuro semplice irregolare:\nNoi _____ (essere) domani?", "resposta": "saremo", "explicacao": "ESSERE irregolare: saremo. Noi saremo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you will be' in italiano?", "opcoes": ["sarete", "sestate", "eri"], "resposta": 0, "explicacao": "Sarete = Voi sarete. Seconda persona plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Futuro semplice irregolare:\nVoi _____ (essere) domani?", "resposta": "sarete", "explicacao": "ESSERE irregolare: sarete. Voi sarete."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Futuro semplice irregolare:\nLoro _____ (essere) domani?", "resposta": "saranno", "explicacao": "ESSERE irregolare: saranno. Loro saranno."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I will be'? A:", "opcoes": ["sarò", "sono", "ero"], "resposta": 0, "explicacao": "Sarò = Io sarò. Prima persona singolare di essere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Futuro semplice irregolare:\nAvere:\nIo _____ (avere) domani?", "resposta": "avrò", "explicacao": "AVERE irregolare: avrò. Io avrò."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Futuro semplice irregolare:\nTu _____ (avere) domani?", "resposta": "avrai", "explicacao": "AVERE irregolare: avrai. Tu avrai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he will have' in italiano?", "opcoes": ["avrà", "ha", "aveva"], "resposta": 0, "explicacao": "Avrà = Lui avrà. Terza persona singolare di avere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Futuro semplice irregolare:\nLei _____ (avere) domani?", "resposta": "avrà", "explicacao": "AVERE irregolare: avrà. Lei avrà."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Futuro semplice irregolare:\nNoi _____ (avere) domani?", "resposta": "avremo", "explicacao": "AVERE irregolare: avremo. Noi avremo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you will have' in italiano?", "opcoes": ["avrete", "avete", "avevate"], "resposta": 0, "explicacao": "Avrete = Voi avrete. Seconda persona plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Futuro semplice irregolare:\nLoro _____ (avere) domani?", "resposta": "avranno", "explicacao": "AVERE irregolare: avranno. Loro avranno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Futuro semplice irregolare:\nAndare:\nIo _____ (andare) domani?", "resposta": "andrò", "explicacao": "ANDARE irregolare: andrò. Io andrò."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Futuro semplice irregolare:\nTu _____ (andare) domani?", "resposta": "andrai", "explicacao": "ANDARE irregolare: andrai. Tu andrai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they will go' in italiano?", "opcoes": ["andranno", "andano", "andarono"], "resposta": 0, "explicacao": "Andranno = Loro andranno. Terza persona plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Futuro semplice irregolare:\nLei _____ (andare) domani?", "resposta": "andrà", "explicacao": "ANDARE irregolare: andrà. Lei andrà."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Futuro semplice irregolare:\nNoi _____ (andare) domani?", "resposta": "andremo", "explicacao": "ANDARE irregolare: andremo. Noi andremo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you will go' in italiano?", "opcoes": ["andrete", "andate", "andavate"], "resposta": 0, "explicacao": "Andrete = Voi andrete. Seconda persona plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Futuro semplice irregolare:\nLoro _____ (andare) domani?", "resposta": "andranno", "explicacao": "ANDARE irregolare: andranno. Loro andranno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Futuro composto:\nIo _____ mangiato (avere + part.)", "resposta": "avrò mangiato", "explicacao": "Futuro composto = avrò + participio passato. Io avrò mangiato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Futuro composto:\nTu _____ visto (avere + part.)", "resposta": "avrai visto", "explicacao": "Futuro composto = avrai + participio passato. Tu avrai visto."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I will have done'? A:", "opcoes": ["avrò fatto", "averò fatto", "farò"], "resposta": 0, "explicacao": "Avrò fatto = Io avrò + fatto. Futuro composto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Futuro composto:\nLei _____ parlato (avere + part.)", "resposta": "avrà parlato", "explicacao": "Futuro composto = avrà + participio passato. Lei avrà parlato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Futuro composto:\nNoi _____ fatto (avere + part.)", "resposta": "avremo fatto", "explicacao": "Futuro composto = avremo + participio passato. Noi avremo fatto."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'we will have eaten'? A:", "opcoes": ["avrà mangiato", "avremo mangiati", "mangeremo"], "resposta": 1, "explicacao": "Avremo mangiato = Noi avremo + mangiato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Futuro composto:\nVoi _____ dormito (avere + part.)", "resposta": "avrete dormito", "explicacao": "Futuro composto = avrete + participio passato. Voi avrete dormito."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Futuro composto:\nLoro _____ scritto (avere + part.)", "resposta": "avranno scritto", "explicacao": "Futuro composto = avranno + participio passato. Loro avranno scritto."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they will have written'? A:", "opcoes": ["averranno scritto", "scrivevano", "scriveranno"], "resposta": 0, "explicacao": "Avranno scritto = Loro avranno + scritto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Futuro composto:\nNoi _____ andato (essere + part.)", "resposta": "saremo andati", "explicacao": "Futuro composto = saremo + participio passato. Noi saremo andati."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Uso del futuro per probabilità:\n_____ pioverà domani? (probabilità)", "resposta": "Probabilmente pioverà domani", "explicacao": "Futuro usato per probabilità presente. Probabilmente pioverà."}
]

exercicios = lez["exercicios"]
idx_insert = next((i for i, e in enumerate(exercicios) if e["tipo"] == "escolha"), len(exercicios))

for i, ex in enumerate(novos):
    exercicios.insert(idx_insert + i, ex)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
