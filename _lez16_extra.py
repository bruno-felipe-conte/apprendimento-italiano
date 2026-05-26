import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XVI")

novos = [
    # 30 exercícios sobre La congiunzione
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Congiunzione 'e':\nStudio italiano _____ inglese.", "resposta": "e", "explicacao": "E = e (and). Studio italiano e inglese."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Congiunzione 'ma':\nÈ intelligente _____ pigro.", "resposta": "ma", "explicacao": "Ma = ma (but). È intelligente ma pigro."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'and'? A:", "opcoes": ["e", "o", "se"], "resposta": 0, "explicacao": "E = e (and). Congiunzione coordinante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Congiunzione 'ma':\nÈ alto _____ grasso.", "resposta": "ma", "explicacao": "Ma = ma (but). È alto ma grasso."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Congiunzione 'o':\nVerrai _____ resterai?", "resposta": "o", "explicacao": "O = o (or). Verrai o resterai?"},
    {"tipo": "escolha", "pergunta": "Come si dice 'but' in italiano? A:", "opcoes": ["e", "ma", "o"], "resposta": 1, "explicacao": "Ma = ma (but). Congiunzione avversativa."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Congiunzione 'o':\nPrendi l'ombrello _____ il cappello.", "resposta": "o", "explicacao": "O = o (or). Prendi l'ombrello o il cappello."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Congiunzione 'se':\n_____, verrò.", "resposta": "Se", "explicacao": "Se = se (if). Se pioverà, verrò."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'or'? A:", "opcoes": ["e", "o", "ma"], "resposta": 1, "explicacao": "O = o (or). Congiunzione alternativa."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Congiunzione 'se':\nIo _____ lui non possiamo andare.", "resposta": "se", "explicacao": "Se = se (if). Se tu, io non possiamo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Congiunzione 'e':\nParlo francese _____ tedesco.", "resposta": "o", "explicacao": "O = o (or). Parlo francese o tedesco."},
    {"tipo": "escolha", "pergunta": "Come si dice 'if' in italiano? A:", "opcoes": ["se", "quando", "poiché"], "resposta": 0, "explicacao": "Se = se (if). Congiunzione subordinante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Congiunzione 'se':\n_____ hai tempo, aiutami.", "resposta": "Se", "explicacao": "Se = se (if). Se hai tempo, aiutami."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Congiunzione 'se':\n_____ piove, non verrò.", "resposta": "Se", "explicacao": "Se = se (if). Se piove, non verrò."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'but'? A:", "opcoes": ["e", "o", "ma"], "resposta": 2, "explicacao": "Ma = ma (but). Congiunzione avversativa."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Congiunzione 'ma':\nÈ ricco _____ non è felice.", "resposta": "ma", "explicacao": "Ma = ma (but). È ricco ma non è felice."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Congiunzione 'se':\n_____ vuoi venire, dimmelo.", "resposta": "Se", "explicacao": "Se = se (if). Se vuoi venire, dimmelo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'and then'? A:", "opcoes": ["e poi", "poi e", "prima"], "resposta": 0, "explicacao": "E poi = e (and) + poi (then)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Congiunzione 'e':\nHo mangiato _____ bevuto.", "resposta": "e", "explicacao": "E = e (and). Ho mangiato e bevuto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Congiunzione 'ma':\nÈ bello _____ è freddo.", "resposta": "ma", "explicacao": "Ma = ma (but). È bello ma è freddo."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'if'? A:", "opcoes": ["se", "qualora", "quando"], "resposta": 0, "explicacao": "Se = se (if). Congiunzione subordinante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Congiunzione 'o':\n_____ vieni _____ ti fermi?", "resposta": "o", "explicacao": "O = o (or). O vieni o ti fermi?"},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Congiunzione 'se':\n_____ finisci, partiamo.", "resposta": "Se", "explicacao": "Se = se (if). Se finisci, partiamo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'unless'? A:", "opcoes": ["a meno che non", "se", "quando"], "resposta": 0, "explicacao": "A meno che non = unless. Congiunzione con negazione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Congiunzione 'e':\nLeggo _____ scrivo.", "resposta": "e", "explicacao": "E = e (and). Leggo e scrivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Congiunzione 'ma':\nÈ veloce _____ non è forte.", "resposta": "ma", "explicacao": "Ma = ma (but). È veloce ma non è forte."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'although'? A:", "opcoes": ["anche se", "se", "quando"], "resposta": 0, "explicacao": "Anche se = although. Congiunzione concessiva."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Congiunzione 'se':\n_____ studi di più, passerai l'esame.", "resposta": "Se", "explicacao": "Se = se (if). Se studi di più, passerai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Congiunzione 'o':\nFai _____ dormi.", "resposta": "o", "explicacao": "O = o (or). Fai o dormi?"},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'unless'? A:", "opcoes": ["a meno che non", "se", "anche se"], "resposta": 0, "explicacao": "A meno che non = unless. Congiunzione con negazione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Congiunzione 'e':\nCorro _____ salto.", "resposta": "e", "explicacao": "E = e (and). Corro e salto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Congiunzione 'ma':\nÈ piccolo _____ è bravo.", "resposta": "ma", "explicacao": "Ma = ma (but). È piccolo ma è bravo."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'while'? A:", "opcoes": ["mentre", "quando", "se"], "resposta": 0, "explicacao": "Mentre = while. Congiunzione temporale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Congiunzione 'se':\n_____ vuoi aiuto, chiedi.", "resposta": "Se", "explicacao": "Se = se (if). Se vuoi aiuto, chiedi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Congiunzione 'e':\nVedo _____ ascolto.", "resposta": "e", "explicacao": "E = e (and). Vedo e ascolto."},
    {"tipo": "escolha", "pergunta": "Come si dice 'until'? A:", "opcoes": ["fino a quando", "quando", "dopo"], "resposta": 0, "explicacao": "Fino a quando = until. Congiunzione temporale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Congiunzione 'ma':\nÈ forte _____ è stanco.", "resposta": "ma", "explicacao": "Ma = ma (but). È forte ma è stanco."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Congiunzione 'se':\n_____ hai fame, mangia.", "resposta": "Se", "explicacao": "Se = se (if). Se hai fame, mangia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Congiunzione 'e':\nCammino _____ parlo.", "resposta": "e", "explicacao": "E = e (and). Cammino e parlo."},
    {"tipo": "escolha", "pergunta": "Quale congiunzione è corretta per 'although'? A:", "opcoes": ["anche se", "se", "mentre"], "resposta": 0, "explicacao": "Anche se = although. Congiunzione concessiva."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Congiunzione 'ma':\nÈ gentile _____ è schivo.", "resposta": "ma", "explicacao": "Ma = ma (but). È gentile ma è schivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Congiunzione 'se':\n_____ vuoi uscire, vado.", "resposta": "Se", "explicacao": "Se = se (if). Se vuoi uscire, vado."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Congiunzione 'o':\nTi ami _____ me?", "resposta": "o", "explicacao": "O = o (or). Ti ami o me?"}
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
