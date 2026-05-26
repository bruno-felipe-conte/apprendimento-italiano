import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XX")

novos = [
    # 30 exercícios sobre I pronomi diretti e indiretti
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Pronome diretto:\nLo _____ incontro ieri era mio amico.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Lo che = That which I met."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Pronome indiretto:\nGli _____ ho parlato era mio professore.", "resposta": "a lui", "explicacao": "Pronome indiretto 'a lui'. A gli = To him."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I gave it to him'? A:", "opcoes": ["glie l'ho dato", "gli ho dato", "l'ho dato a"], "resposta": 1, "explicacao": "Gli ho dato = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Pronome diretto:\nL' _____ ho visto era mio fratello.", "resposta": "che", "explicacao": "Pronome diretto 'che'. L' che = That whom I saw."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Pronome indiretto:\nLe _____ ho scritto era mio amico.", "resposta": "a lui", "explicacao": "Pronome indiretto 'a lui'. A le = To him."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she gave it to me'? A:", "opcoes": ["me l'ha data", "mi ha dato", "la ha data a me"], "resposta": 0, "explicacao": "Me l'ha data = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Pronome diretto:\nChi _____ ho chiamato è mio zio.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Chi che = The one I called."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Pronome indiretto:\nA chi _____ ho dato i soldi?", "resposta": "gli", "explicacao": "Pronome indiretto 'gli'. A chi gli = To whom I gave."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I sent it to her'? A:", "opcoes": ["a lei l'ho mandato", "le ho mandato", "l'ho mandato a lei"], "resposta": 1, "explicacao": "Le ho mandato = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Pronome diretto:\nQuello _____ hai comprato è bello.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Quello che = That which you bought."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Pronome indiretto:\nLe _____ ho regalato il libro.", "resposta": "a lei", "explicacao": "Pronome indiretto 'a lei'. A le = To her."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they showed it to us'? A:", "opcoes": ["ci hanno mostrato", "hanno ci mostrato", "mostrato ci"], "resposta": 0, "explicacao": "Ci hanno mostrato = Indiretto + direto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Pronome diretto:\nCosa _____ stai cercando?", "resposta": "che", "explicacao": "Pronome diretto 'che'. Cosa che = What you are looking for."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Pronome indiretto:\nA chi _____ devi parlare?", "resposta": "gli", "explicacao": "Pronome indiretto 'gli'. A chi gli = To whom must speak."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I told them about it'? A:", "opcoes": ["loro l'ho detto", "l'ho detto a loro", "l'ho detta"], "resposta": 1, "explicacao": "L'ho detto a loro = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Pronome diretto:\nLa persona _____ incontri è amica.", "resposta": "che", "explicacao": "Pronome diretto 'che'. La persona che = The person whom you meet."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Pronome indiretto:\nA chi _____ vuoi inviare la email?", "resposta": "a lui", "explicacao": "Pronome indiretto 'a lui'. A chi lui = To whom do you want to send."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he gave it to her'? A:", "opcoes": ["gli ha data", "ha dato lei", "a lei l'ha data"], "resposta": 2, "explicacao": "A lei l'ha data = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Pronome diretto:\nIl film _____ guardi è interessante.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Il film che = The film which you watch."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Pronome indiretto:\nA chi _____ hai dato la chiave?", "resposta": "a lei", "explicacao": "Pronome indiretto 'a lei'. A chi lei = To whom did you give."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I showed it to him'? A:", "opcoes": ["l'ho mostrato a lui", "gli ho mostrato", "lui l'ho mostrato"], "resposta": 1, "explicacao": "Gli ho mostrato = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Pronome diretto:\nL' _____ hai promesso è importante.", "resposta": "che", "explicacao": "Pronome diretto 'che'. L' che = That which you promised."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Pronome indiretto:\nA chi _____ ho inviato i documenti?", "resposta": "a loro", "explicacao": "Pronome indiretto 'a loro'. A chi loro = To whom I sent."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she gave it to us'? A:", "opcoes": ["ci ha dato", "ha ci dato", "ci ha data"], "resposta": 0, "explicacao": "Ci ha dato = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Pronome diretto:\nIl ragazzo _____ vedi è mio fratello.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Il ragazzo che = The boy whom you see."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Pronome indiretto:\nA chi _____ ho prestato il libro?", "resposta": "a lui", "explicacao": "Pronome indiretto 'a lui'. A chi lui = To whom I lent."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they gave it to her'? A:", "opcoes": ["le hanno dato", "hanno lei dato", "la hanno data a lei"], "resposta": 0, "explicacao": "Le hanno dato = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Pronome diretto:\nL' _____ desideri è buono.", "resposta": "che", "explicacao": "Pronome diretto 'che'. L' che = That which you desire."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Pronome indiretto:\nA chi _____ hai parlato ieri?", "resposta": "a lei", "explicacao": "Pronome indiretto 'a lei'. A chi lei = To whom you spoke."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I gave it to them'? A:", "opcoes": ["loro l'ho dato", "l'ho dato loro", "gli ho dato"], "resposta": 2, "explicacao": "L'ho dato loro = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Pronome diretto:\nIl libro _____ leggi è interessante.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Il libro che = The book which you read."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Pronome indiretto:\nA chi _____ hai mandato la lettera?", "resposta": "a lui", "explicacao": "Pronome indiretto 'a lui'. A chi lui = To whom I sent."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'he gave it to us'? A:", "opcoes": ["ci ha dato", "ha ci dato", "l'ha data a noi"], "resposta": 0, "explicacao": "Ci ha dato = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Pronome diretto:\nCosa _____ stai comprando?", "resposta": "che", "explicacao": "Pronome diretto 'che'. Cosa che = What you are buying."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Pronome indiretto:\nA chi _____ vuoi chiedere l'indirizzo?", "resposta": "a lei", "explicacao": "Pronome indiretto 'a lei'. A chi lei = To whom do you want to ask."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they showed it to us'? A:", "opcoes": ["ci hanno mostrato", "hanno ci mostrato", "ci mostrarono"], "resposta": 0, "explicacao": "Ci hanno mostrado = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Pronome diretto:\nIl film _____ hai visto è bello.", "resposta": "che", "explicacao": "Pronome diretto 'che'. Il film che = The film which you saw."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Pronome indiretto:\nA chi _____ ho dato la risposta?", "resposta": "a loro", "explicacao": "Pronome indiretto 'a loro'. A chi loro = To whom I gave."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I told it to him'? A:", "opcoes": ["gli ho detto", "l'ho detto a lui", "lui ho detto"], "resposta": 0, "explicacao": "Gli ho detto = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Pronome diretto:\nLa persona _____ hai incontrato è bella.", "resposta": "che", "explicacao": "Pronome diretto 'che'. La persona che = The person whom you met."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Pronome indiretto:\nA chi _____ devi inviare il pacco?", "resposta": "a lei", "explicacao": "Pronome indiretto 'a lei'. A chi lei = To whom must send."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she gave it to them'? A:", "opcoes": ["le ha dato loro", "loro le ha dato", "le hanno dato"], "resposta": 2, "explicacao": "Le ha dato loro = Indiretto + diretto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Pronome diretto:\nL' _____ hai promesso è difficile.", "resposta": "che", "explicacao": "Pronome diretto 'che'. L' che = That which you promised."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Pronome indiretto:\nA chi _____ hai scritto la lettera?", "resposta": "a lui", "explicacao": "Pronome indiretto 'a lui'. A chi lui = To whom you wrote."}
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
