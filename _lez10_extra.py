import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione X")

novos = [
    # 30 ejercicios sobre Comparativi e superlativi
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Comparativo di maggioranza:\nMarco è _____ (alto) Luca.", "resposta": "più alto di", "explicacao": "Comparativo: più + aggettivo + di."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Comparativo di maggioranza:\nAnna è _____ (bella) Sofia.", "resposta": "più bella di", "explicacao": "Comparativo: più + aggettivo femminile + di."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'more intelligent than'? A:", "opcoes": ["più intelligente che", "maggiormente intelligente di", "più intelligente di"], "resposta": 2, "explicacao": "Più intelligente di = Comparativo di maggioranza."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Comparativo di minoranza:\nQuesti libri sono _____ (costosi) quelli.", "resposta": "meno costosi di", "explicacao": "Comparativo: meno + aggettivo + di."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Comparativo di minoranza:\nLui è _____ (lento) suo fratello.", "resposta": "meno lento di", "explicacao": "Comparativo: meno + aggettivo + di."},
    {"tipo": "escolha", "pergunta": "Come si dice 'less expensive than'? A:", "opcoes": ["maggiormente economico di", "più economici che", "meno costosi di"], "resposta": 2, "explicacao": "Meno costosi di = Comparativo di minoranza."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Comparativo di uguaglianza:\nMarco è _____ (alto) Andrea.", "resposta": "tanto alto quanto", "explicacao": "Comparativo: tanto + aggettivo + quanto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Comparativo di uguaglianza:\nAnna è _____ (brava) Marta.", "resposta": "tanto brava quanto", "explicacao": "Comparativo: tanto + aggettivo femminile + quanto."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'as fast as'? A:", "opcoes": ["come veloce", "tanto veloce come", "più veloce di"], "resposta": 1, "explicacao": "Tanto veloce quanto = Comparativo di uguaglianza."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Superlativo relativo:\nQuesto è il film _____ (buono) dell'anno.", "resposta": "più buono", "explicacao": "Superlativo: più + aggettivo. Con 'il/la'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Superlativo relativo:\nLei è la studentessa _____ (intelligente) della classe.", "resposta": "più intelligente", "explicacao": "Superlativo femminile: più + aggettivo. Con 'la'."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the smallest'? A:", "opcoes": ["il più piccolo", "il minore", "la meno piccolo"], "resposta": 0, "explicacao": "Il più piccolo = Superlativo relativo maschile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Superlativo assoluto:\nMarco è _____ (alto) possibile!", "resposta": "altissimo", "explicacao": "Superlativo assoluto: suffisso -issimo. Senza 'di'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Superlativo assoluto:\nAnna è _____ (bella) possibile!", "resposta": "bellissima", "explicacao": "Superlativo assoluto femminile: -issima. Senza 'di'.",},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'very kind'? A:", "opcoes": ["molto gentile", "gentilissimo", "più gentile di"], "resposta": 1, "explicacao": "Gentilissimo = Superlativo assoluto. Molto + aggettivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Comparativo con irregolare:\nMarco è _____ (bene) di Luca.", "resposta": "più bravo di", "explicacao": "Avverbio 'bravo' = meglio. Ma uso regolare più."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Comparativo con irregolare:\nAnna è _____ (bene) Sofia.", "resposta": "più brava di", "explicacao": "Avverbio femminile 'brava' = meglio. Ma uso regolare più."},
    {"tipo": "escolha", "pergunta": "Come si dice 'worse than'? A:", "opcoes": ["peggio di", "meno buono di", "più male"], "resposta": 0, "explicacao": "Peggio di = Superlativo negativo. Irregolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Comparativo con irregolare:\nLui è _____ (male) suo fratello.", "resposta": "peggio di", "explicacao": "Avverbio 'male' = peggio. Irregolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Superlativo negativo:\nQuesto è il film _____ (buono) dell'anno.", "resposta": "meno buono", "explicacao": "Superlativo: meno + aggettivo. Con 'il/la'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Superlativo negativo:\nLei è la studentessa _____ (lenta) della classe.", "resposta": "meno lenta", "explicacao": "Superlativo femminile: meno + aggettivo. Con 'la'.",},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'worst'? A:", "opcoes": ["il peggio", "il peggiore", "il più peggio"], "resposta": 1, "explicacao": "Il peggiore = Superlativo negativo. Irregolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Uso di 'sì come' nella negazione:\nMarco non è _____ (bello) Luca.", "resposta": "più bello di", "explicacao": "Negazione: non + più. Marco non è più."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Uso di 'sì come' nella negazione:\nAnna non è _____ (brava) Sofia.", "resposta": "più brava di", "explicacao": "Negazione: non + più. Anna non è più."},
    {"tipo": "escolha", "pergunta": "Come si dice 'not as tall as'? A:", "opcoes": ["non tanto alto quanto", "meno alto di", "più basso di"], "resposta": 0, "explicacao": "Non tanto alto quanto = Negazione comparativo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Comparativo con 'molto':\nMarco è _____ (alto) Luca.", "resposta": "più molto alto di", "explicacao": "Enfatico: più + intensificatore + aggettivo. Ma raro."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Comparativo con 'molto':\nAnna è _____ (bella) Sofia.", "resposta": "più molto bella di", "explicacao": "Enfatico: più + intensificatore + aggettivo. Ma raro."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'more beautiful than'? A:", "opcoes": ["più bella che", "maggiormente bella di", "più molto bella di"], "resposta": 0, "explicacao": "Più bella che = Comparativo regolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Confronto tra gruppi:\nGli italiani sono _____ (puliti) gli americani.", "resposta": "più puliti di", "explicacao": "Confronto tra gruppi: più + aggettivo + di."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Confronto tra gruppi:\nLe donne sono _____ (brave) gli uomini.", "resposta": "più brave di", "explicacao": "Confronto tra gruppi femminile: più + aggettivo + di."},
    {"tipo": "escolha", "pergunta": "Come si dice 'as good as'? A:", "opcoes": ["tanto buono quanto", "meglio che", "più buono di"], "resposta": 0, "explicacao": "Tanto buono quanto = Comparativo di uguaglianza."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Confronto temporale:\nOggi è _____ (buono) ieri.", "resposta": "più buono di", "explicacao": "Confronto temporale: più + aggettivo + di."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Confronto spaziale:\nRoma è _____ (grande) Milano.", "resposta": "più grande di", "explicacao": "Confronto tra luoghi: più + aggettivo + di."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the richest'? A:", "opcoes": ["il più ricco", "il maggiore", "il meglio"], "resposta": 0, "explicacao": "Il più ricco = Superlativo relativo maschile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Superlativo con 'di':\nMarco è il _____ della classe.", "resposta": "più intelligente", "explicacao": "Superlativo: più + aggettivo. Con preposizione articolata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Superlativo con 'di':\nAnna è la _____ della classe.", "resposta": "più brava", "explicacao": "Superlativo femminile: più + aggettivo. Con preposizione articolata."},
    {"tipo": "escolha", "pergunta": "Come si dice 'more careful than'? A:", "opcoes": ["più attento di", "meglio che", "maggiormente attento"], "resposta": 0, "explicacao": "Più attento di = Comparativo di maggioranza."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Comparativo irregolare speciale:\nMarco corre _____ Luca.", "resposta": "meglio di", "explicacao": "Correggere: migliore o meglio. Irregolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Comparativo irregolare speciale:\nAnna canta _____ Sofia.", "resposta": "meglio di", "explicacao": "Cantare: meglio. Irregolare per performance."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'less smart'? A:", "opcoes": ["meno intelligente", "più stupido di", "peggiore"], "resposta": 0, "explicacao": "Meno intelligente = Comparativo di minoranza."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Comparativo di minoranza:\nQuesto telefono è _____ quello.", "resposta": "meno costoso di", "explicacao": "Oggetti inanimati: meno + aggettivo + di."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Comparativo con 'più' e numeri:\nMarco ha _____ anni di Luca.", "resposta": "più molti", "explicacao": "Numeri: più + numero. Marco ha più."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Superlativo relativo con gruppo:\nLei è la _____ dei due sorelle.", "resposta": "più brava delle", "explicacao": "Superlativo: più + aggettivo. Con preposizione articolata."}
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
