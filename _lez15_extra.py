import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XV")

novos = [
    # 30 exercícios sobre La negazione
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Negazione semplice:\nIo _____ (parlare) italiano.", "resposta": "non parlo", "explicacao": "Non + verbo. Non parlo = Io non parlo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Negazione semplice:\nTu _____ (mangiare) carne.", "resposta": "non mangi", "explicacao": "Non + verbo. Non mangi = Tu non mangi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she doesn't speak'? A:", "opcoes": ["lei parla non", "lei non parla", "non lei parla"], "resposta": 1, "explicacao": "Lei non parla = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Negazione semplice:\nLui _____ (vivere) qui.", "resposta": "non vive", "explicacao": "Non + verbo. Non vive = Lui non vive."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Negazione semplice:\nNoi _____ (lavorare) qui.", "resposta": "non lavoriamo", "explicacao": "Non + verbo. Non lavoriamo = Noi non lavoriamo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they don't like'? A:", "opcoes": ["loro piace non", "loro non piacciono", "non li piace"], "resposta": 1, "explicacao": "Loro non piacciono = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Negazione semplice:\nVoi _____ (comprare) questa?", "resposta": "non comprate", "explicacao": "Non + verbo. Non comprate = Voi non comprate."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Negazione semplice:\nEssi _____ (venire) domani.", "resposta": "non vengono", "explicacao": "Non + verbo. Non vengono = Essi non vengono."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I don't know'? A:", "opcoes": ["so non", "non so", "io non"], "resposta": 1, "explicacao": "Non so = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Negazione con 'mai':\nIo _____ mai (andare) in Giappone.", "resposta": "non vado", "explicacao": "Non + verbo. Mai = never. Io non vado mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Negazione con 'più':\nIo _____ (fare) più errori.", "resposta": "non faccio", "explicacao": "Non + verbo. Non faccio = Io non faccio."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he never does'? A:", "opcoes": ["lei mai fa", "lei non mai fa", "lei non mai fa mai"], "resposta": 0, "explicacao": "Lei non mai fa = Non + verbo. Mai = never."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Negazione con 'mai':\nLei _____ mai (parlare) francese.", "resposta": "non parla", "explicacao": "Non + verbo. Mai = never. Lei non parla mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Negazione con 'mai':\nNoi _____ mai (scrivere) poesie.", "resposta": "non scriviamo", "explicacao": "Non + verbo. Mai = never. Noi non scriviamo mai."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I don't eat meat'? A:", "opcoes": ["mangi carne no", "non mangio carne", "carne io non"], "resposta": 1, "explicacao": "Non mangio carne = Non + verbo + oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Negazione con 'mai':\nEssi _____ mai (studiare) la sera.", "resposta": "non studiano", "explicacao": "Non + verbo. Mai = never. Essi non studiano mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Negazione semplice:\nIo _____ (essere) triste.", "resposta": "non sono", "explicacao": "Non + verbo ausiliare. Non sono = Io non sono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Negazione semplice:\nTu _____ (avere) paura?", "resposta": "non hai", "explicacao": "Non + verbo ausiliare. Non hai = Tu non hai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she isn't'? A:", "opcoes": ["lei è non", "lei non è", "non lei"], "resposta": 1, "explicacao": "Lei non è = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Negazione semplice:\nLui _____ (essere) felice.", "resposta": "non è", "explicacao": "Non + verbo ausiliare. Non è = Lui non è."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Negazione semplice:\nNoi _____ (avere) tempo.", "resposta": "non abbiamo", "explicacao": "Non + verbo ausiliare. Non abbiamo = Noi non abbiamo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they don't have'? A:", "opcoes": ["loro avere non", "loro non hanno", "non loro"], "resposta": 1, "explicacao": "Loro non hanno = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Negazione con 'mai':\nVoi _____ mai (vedere) le stelle?", "resposta": "non vedete", "explicacao": "Non + verbo. Mai = never. Voi non vedete mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Negazione con 'mai':\nLei _____ mai (bere) latte.", "resposta": "non beve", "explicacao": "Non + verbo. Mai = never. Lei non beve mai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I don't understand'? A:", "opcoes": ["capisco non", "non capisco", "io non"], "resposta": 1, "explicacao": "Non capisco = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Negazione con 'mai':\nEssi _____ mai (andare) al cinema.", "resposta": "non vanno", "explicacao": "Non + verbo. Mai = never. Essi non vanno mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Negazione con 'mai':\nVoi _____ mai (venire) qui?", "resposta": "non venite", "explicacao": "Non + verbo. Mai = never. Voi non venite mai."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I don't believe'? A:", "opcoes": ["credere no io", "io non credo", "no credono"], "resposta": 1, "explicacao": "Io non credo = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Negazione con 'mai':\nLui _____ mai (dormire) troppo.", "resposta": "non dorme", "explicacao": "Non + verbo. Mai = never. Lui non dorme mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Negazione con 'mai':\nNoi _____ mai (cantare) al karaoke.", "resposta": "non cantiamo", "explicacao": "Non + verbo. Mai = never. Noi non cantiamo mai."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she doesn't believe'? A:", "opcoes": ["lei crede no", "lei non creda", "non lei"], "resposta": 1, "explicacao": "Lei non creda = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Negazione con 'mai':\nIo _____ mai (ascoltare) la radio.", "resposta": "non ascolto", "explicacao": "Non + verbo. Mai = never. Io non ascolto mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Negazione con 'mai':\nTu _____ mai (studiare) la notte?", "resposta": "non studi", "explicacao": "Non + verbo. Mai = never. Tu non studii mai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he doesn't know'? A:", "opcoes": ["egli sa no", "egli non sa", "non egli"], "resposta": 1, "explicacao": "Egli non sa = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Negazione con 'mai':\nEssi _____ mai (lavorare) il weekend.", "resposta": "non lavorano", "explicacao": "Non + verbo. Mai = never. Essi non lavorano mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Negazione con 'mai':\nLei _____ mai (telefonare) a casa?", "resposta": "non telefona", "explicacao": "Non + verbo. Mai = never. Lei non telefona mai."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I don't think'? A:", "opcoes": ["penso no io", "io non penso", "no penso"], "resposta": 1, "explicacao": "Io non penso = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Negazione con 'mai':\nNoi _____ mai (uscire) di sera.", "resposta": "non usciamo", "explicacao": "Non + verbo. Mai = never. Noi non usciamo mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Negazione con 'mai':\nVoi _____ mai (leggere) libri?", "resposta": "non leggete", "explicacao": "Non + verbo. Mai = never. Voi non leggete mai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they don't want'? A:", "opcoes": ["loro vogliono no", "loro non vogliono", "non loro"], "resposta": 1, "explicacao": "Loro non vogliono = Non + verbo. Negazione semplice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Negazione con 'mai':\nEssi _____ mai (andare) in montagna.", "resposta": "non vanno", "explicacao": "Non + verbo. Mai = never. Essi non vanno mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Negazione con 'mai':\nLui _____ mai (dare) una mano?", "resposta": "non dà", "explicacao": "Non + verbo. Mai = never. Lui non dà mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Negazione semplice:\nIo _____ (parlare) con estranei.", "resposta": "non parlo", "explicacao": "Non + verbo. Non parlo = Io non parlo."}
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
