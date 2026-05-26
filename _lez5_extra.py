import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione V")

novos = [
    # 30 exercícios sobre La particella "ci" / Partitivo
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Ci come pronome di luogo:\nC'è _____ casa? (essere + ci)", "resposta": "c'è in casa", "explicacao": "C'è in casa = C'è + in + casa. Si usa CI per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Ci come pronome di luogo:\nNoi _____ al mare? (andare + ci)", "resposta": "ci andiamo al mare", "explicacao": "Ci andiamo = Andiamo + ci. Si usa CI per movimento verso luogo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'there are'? A:", "opcoes": ["c'è", "ci sono", "ci"], "resposta": 1, "explicacao": "Ci sono = Ci + sono. Si usa CI SONO per plural."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Ci come pronome di luogo:\nLoro _____ in Italia? (essere + ci)", "resposta": "ci sono in Italia", "explicacao": "Ci sono = Ci + sono. Si usa CI SONO per plural."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Ci come pronome di luogo:\nTu _____ a scuola? (andare + ci)", "resposta": "ci vai a scuola", "explicacao": "Ci vai = Vai + ci. Si usa CI per movimento verso luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'there is' in italiano?", "opcoes": ["c'è", "ci", "sono"], "resposta": 0, "explicacao": "C'è = C'è (esserci singolare). Si usa C'È per singolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Ci come pronome di luogo:\nLui _____ al lavoro? (andare + ci)", "resposta": "ci va al lavoro", "explicacao": "Ci va = Va + ci. Si usa CI per movimento verso luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Ci come pronome di luogo:\nLei _____ all'università? (andare + ci)", "resposta": "ci va all'università", "explicacao": "Ci va = Va + ci. Si usa CI per movimento verso luogo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'there are many'? A:", "opcoes": ["c'è molti", "ci sono molti", "molti c'è"], "resposta": 1, "explicacao": "Ci sono molti = Ci + sono + molti. Si usa CI SONO per plural."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Ci come pronome di luogo:\nVoi _____ in piscina? (essere + ci)", "resposta": "ci siete in piscina", "explicacao": "Ci siete = Ci + siete. Si usa CI SONO per plural."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Ci come pronome di luogo:\nEssi _____ in treno? (andare + ci)", "resposta": "ci vanno in treno", "explicacao": "Ci vanno = Vanno + ci. Si usa CI per movimento verso luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'there is one'? A:", "opcoes": ["c'è uno", "ci è uno", "uno c'è"], "resposta": 0, "explicacao": "C'è uno = C'è + uno. Si usa C'È per singolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Ci come pronome di luogo:\nNoi _____ al cinema? (essere + ci)", "resposta": "ci siamo al cinema", "explicacao": "Ci siamo = Ci + siamo. Si usa CI SONO per plural."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Ci come pronome di luogo:\nIo _____ in ufficio? (essere + ci)", "resposta": "ci sono in ufficio", "explicacao": "Ci sono = Ci + sono. Si usa CI SONO per plural."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'we will go'? A:", "opcoes": ["andremo", "andarci", "andiamo"], "resposta": 0, "explicacao": "Andremo = Andare + ranno. Futuro semplice di andare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Ci con verbi:\nQuesto lavoro _____ tempo? (volerci)", "resposta": "ci vuole tempo", "explicacao": "Ci vuole = Volere + ci. Si usa CI VUOLE per necessità."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Ci con verbi:\nQuanto _____ lavoro? (volerci)", "resposta": "ci vuole tempo", "explicacao": "Ci vuole = Volere + ci. Si usa CI VUOLE per necessità."},
    {"tipo": "escolha", "pergunta": "Come si dice 'it takes time' in italiano?", "opcoes": ["serve tempo", "ci vuole tempo", "c'è tempo"], "resposta": 1, "explicacao": "Ci vuole tempo = Ci + vuole tempo. Si usa CI VUOLE per necessità."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Ci con verbi:\nQuesto compito _____ fatica? (volerci)", "resposta": "ci vuole fatica", "explicacao": "Ci vuole = Volere + ci. Si usa CI VUOLE per necessità."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Ci con verbi:\nQuanto _____ denaro? (volerci)", "resposta": "ci vuole denaro", "explicacao": "Ci vuole = Volere + ci. Si usa CI VUOLE per necessità."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'it takes'? A:", "opcoes": ["ci serve", "c'è bisogno", "vuole"], "resposta": 0, "explicacao": "Ci serve = Ci + serve. Si usa CI SERVE per necessità."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Ci con verbi:\nMettere un po' _____? (metterci)", "resposta": "ci mette tempo", "explicacao": "Ci mette = Mettere + ci. Si usa CI METTE per necessità."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Ci con verbi:\nFare _____? (farcela)", "resposta": "fa la faccia", "explicacao": "Fa la faccia = Fare + la faccia. Si usa CI VUOLE per necessità."},
    {"tipo": "escolha", "pergunta": "Come si dice 'it requires'? A:", "opcoes": ["richiede", "ci vuole", "vuole"], "resposta": 1, "explicacao": "Ci vuole = Ci + vuole. Si usa CI VUOLE per necessità."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Partitivo: Del/Della:\nHo fame di _____ (di + il)", "resposta": "del pane", "explicacao": "Del = Di + il. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Partitivo: Della:\nHo sete di _____ (di + la)", "resposta": "dell'acqua", "explicacao": "Della = Di + la. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'some'? A:", "opcoes": ["qualche", "alcuni", "del"], "resposta": 2, "explicacao": "Del = Di + il. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Partitivo: Dei:\nHo _____ fratelli (di + i)", "resposta": "dei fratelli", "explicacao": "Dei = Di + i. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Partitivo: Degli:\nHo _____ amici (di + gli)", "resposta": "degli amici", "explicacao": "Degli = Di + gli. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'some books'? A:", "opcoes": ["dei libri", "degli libri", "i libri"], "resposta": 0, "explicacao": "Dei = Di + i. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Partitivo: Delle:\nHo _____ amiche (di + le)", "resposta": "delle amiche", "explicacao": "Delle = Di + le. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Partitivo: Della:\nHo _____ pazienza (di + la)", "resposta": "della pazienza", "explicacao": "Della = Di + la. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'some money'? A:", "opcoes": ["del denaro", "delle denaro", "denaro"], "resposta": 0, "explicacao": "Del = Di + il. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Partitivo: Del/Della:\nMangerò _____ pizza (di + la)", "resposta": "della pizza", "explicacao": "Della = Di + la. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Partitivo: Dei:\nPrenderò _____ libri (di + i)", "resposta": "dei libri", "explicacao": "Dei = Di + i. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'some water'? A:", "opcoes": ["dell'acqua", "acque", "alcuna acqua"], "resposta": 0, "explicacao": "Dell' = Di + l'. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Partitivo: Degli:\nVorrò _____ spaghetti (di + gli)", "resposta": "degli spaghetti", "explicacao": "Degli = Di + gli. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Partitivo: Delle:\nLeggerò _____ riviste (di + le)", "resposta": "delle riviste", "explicacao": "Delle = Di + le. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "escolha", "pergunta": "Come si dice 'some bread'? A:", "opcoes": ["del pane", "pani", "qualche pane"], "resposta": 0, "explicacao": "Del = Di + il. Si usa ARTICOLO PARTITIVO per quantità indeterminata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Partitivo: Qualche:\nVorrò _____ libro (singolare)", "resposta": "qualche libro", "explicacao": "Qualche = Alcuni. Si usa QUALCHE per singolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Partitivo: Alcuni/Alcune:\nHo _____ amiche (femminile)", "resposta": "alcune amiche", "explicacao": "Alcune = Alcuni. Si usa ALCHUNE per femminile plurale."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'some men'? A:", "opcoes": ["alcuni uomini", "qualche uomo", "degli uomini"], "resposta": 0, "explicacao": "Alcuni = Alcuni. Si usa ALCHUNI per maschile plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Partitivo: Qualche:\nHo _____ idee (femminile)", "resposta": "qualche idea", "explicacao": "Qualche = Alcune. Si usa QUALCHE per singolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Partitivo: Un po' di:\nVorrei _____ (cantare)", "resposta": "un po' di musica", "explicacao": "Un po' di = Some. Si usa UN PO' DI per quantità indeterminata."}
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
