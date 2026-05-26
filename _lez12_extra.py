import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XII")

novos = [
    # 30 esercizi sobre gli articoli indeterminativi
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Articolo indeterminativo:\n_____ studente (uno studente)", "resposta": "Uno", "explicacao": "Articolo indeterminativo maschile singolare: uno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Articolo indeterminativo:\n_____ macchina (un macchina)", "resposta": "Un", "explicacao": "Articolo indeterminativo maschile con consonante: un."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'an apple'? A:", "opcoes": ["una mela", "un mela", "uno mela"], "resposta": 0, "explicacao": "Una mela = Articolo indeterminativo femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Articolo indeterminativo:\n_____ casa (una casa)", "resposta": "Una", "explicacao": "Articolo indeterminativo femminile singolare: una."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Articolo indeterminativo:\n_____ libro (un libro)", "resposta": "Un", "explicacao": "Articolo indeterminativo maschile con consonante: un."},
    {"tipo": "escolha", "pergunta": "Come si dice 'a book'? A:", "opcoes": ["una libro", "uno libro", "un libro"], "resposta": 2, "explicacao": "Un libro = Articolo indeterminativo maschile con consonante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Articolo indeterminativo:\n_____ amica (una amica)", "resposta": "Una", "explicacao": "Articolo indeterminativo femminile singolare: una."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Articolo indeterminativo:\n_____ amico (un amico)", "resposta": "Un", "explicacao": "Articolo indeterminativo maschile con consonante: un."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'a woman'? A:", "opcoes": ["una donna", "uno donna", "un donna"], "resposta": 0, "explicacao": "Una donna = Articolo indeterminativo femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Articolo indeterminativo con 's':\n_____ studente (uno studente)", "resposta": "Uno", "explicacao": "Uno si usa davanti a s + consonante. Uno studente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Articolo indeterminativo con 's':\n_____ scienza (una scienza)", "resposta": "Una", "explicacao": "Articolo indeterminativo femminile: una scienza."},
    {"tipo": "escolha", "pergunta": "Come si dice 'a university'? A:", "opcoes": ["una università", "uno università", "un università"], "resposta": 0, "explicacao": "Una università = Articolo indeterminativo femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Articolo indeterminativo con 's':\n_____ sport (uno sport)", "resposta": "Uno", "explicacao": "Uno si usa davanti a s + consonante. Uno sport."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Articolo indeterminativo con 's':\n_____ sedia (una sedia)", "resposta": "Una", "explicacao": "Articolo indeterminativo femminile: una sedia."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'a star'? A:", "opcoes": ["uno stella", "una stella", "un stella"], "resposta": 0, "explicacao": "Uno stella = Articolo indeterminativo con s."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Articolo indeterminativo con 's':\n_____ strada (una strada)", "resposta": "Una", "explicacao": "Articolo indeterminativo femminile: una strada."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Articolo indeterminativo con 's':\n_____ studio (uno studio)", "resposta": "Uno", "explicacao": "Uno si usa davanti a s + consonante. Uno studio."},
    {"tipo": "escolha", "pergunta": "Come si dice 'a sofa'? A:", "opcoes": ["uno divano", "una divano", "un divano"], "resposta": 0, "explicacao": "Uno divano = Articolo indeterminativo con s."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Articolo indeterminativo con 's':\n_____ sera (una sera)", "resposta": "Una", "explicacao": "Articolo indeterminativo femminile: una sera."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Uso di un/uno:\nPrendi _____ libro sul tavolo.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. Prendi un libro."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Uso di un/uno:\nHo visto _____ studente in biblioteca.", "resposta": "uno", "explicacao": "Uno = Maschile con s + consonante. Ho visto uno studente."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'a house'? A:", "opcoes": ["una casa", "uno casa", "un casa"], "resposta": 0, "explicacao": "Una casa = Articolo indeterminativo femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Uso di un/uno:\nÈ _____ eroe in ogni film.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un eroe."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Uso di un/uno:\nMio fratello è _____ artista.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un artista."},
    {"tipo": "escolha", "pergunta": "Come si dice 'a year'? A:", "opcoes": ["un anno", "uno anno", "una anno"], "resposta": 0, "explicacao": "Un anno = Articolo indeterminativo maschile con consonante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Uso di un/uno:\nVuole comprare _____ auto.", "resposta": "un'", "explicacao": "Un' + vocale. Vuole comprare un'auto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Uso di un/uno:\nÈ _____ ospite in questa casa.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un ospite."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'a hospital'? A:", "opcoes": ["un ospedale", "uno ospedale", "una ospedale"], "resposta": 0, "explicacao": "Un ospedale = Articolo indeterminativo maschile con consonante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Uso di un/uno:\nLegge _____ enciclopedia.", "resposta": "un'", "explicacao": "Un' + vocale. Legge un'enciclopedia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Uso di un/uno:\nÈ una _____ interessante esperienza.", "resposta": "un'", "explicacao": "Una' + vocale. È una interessante esperienza."},
    {"tipo": "escolha", "pergunta": "Come si dice 'a orange'? A:", "opcoes": ["una arancia", "uno arancia", "un arancia"], "resposta": 0, "explicacao": "Una arancia = Articolo indeterminativo femminile con vocale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Uso di un/uno:\nVuole _____ umbrella.", "resposta": "un'", "explicacao": "Un' + vocale. Vuole un'ombrello (ma ombrello è maschile con vocale)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Uso di un/uno:\nHo incontrato _____ amico.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. Ho incontrato un amico."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Uso di un/uno:\nÈ _____ esperto in questo campo.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un esperto."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'a island'? A:", "opcoes": ["una isola", "uno isola", "un isola"], "resposta": 0, "explicacao": "Una isola = Articolo indeterminativo femminile con vocale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Uso di un/uno:\nÈ _____ avvocato difensore.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un avvocato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Uso di un/uno:\nPrende _____ appuntamento.", "resposta": "un'", "explicacao": "Un' + vocale. Prende un'appuntamento (ma appuntamento è maschile)."},
    {"tipo": "escolha", "pergunta": "Come si dice 'a onion'? A:", "opcoes": ["uno cipolla", "una cipolla", "un cipolla"], "resposta": 1, "explicacao": "Una cipolla = Articolo indeterminativo femminile con vocale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Uso di un/uno:\nÈ _____ uomo d'affari.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un uomo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Uso di un/uno:\nLegge _____ informazione.", "resposta": "un'", "explicacao": "Un' + vocale. Legge un'informazione."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'a university'? A:", "opcoes": ["una università", "uno università", "un università"], "resposta": 0, "explicacao": "Una università = Articolo indeterminativo femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Uso di un/uno:\nÈ _____ ufficiale della squadra.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un ufficiale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Uso di un/uno:\nÈ _____ ospite in questa casa.", "resposta": "un", "explicacao": "Un = Maschile con consonante semplice. È un ospite."}
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
