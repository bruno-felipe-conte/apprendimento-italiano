import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XVII")

novos = [
    # 30 exercícios sobre Ordini numerali
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Ordine numerale:\nIo sono il _____ (secondo) della classe.", "resposta": "secondo", "explicacao": "Ordine: secondo. Io sono il secondo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Ordine numerale:\nLei è la _____ (terza) del gruppo.", "resposta": "terza", "explicacao": "Ordine: terza. Lei è la terza."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'second'? A:", "opcoes": ["duro", "secondo", "due"], "resposta": 1, "explicacao": "Secondo = Ordine numerale. Secondo = second."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Ordine numerale:\nLui è il _____ (quinto) della fila.", "resposta": "quinto", "explicacao": "Ordine: quinto. Lui è il quinto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Ordine numerale:\nNoi siamo i _____ (primi) arrivati.", "resposta": "primi", "explicacao": "Ordine: primi. Noi siamo i primi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'fifth' in italiano? A:", "opcoes": ["quinto", "cinque", "cinque"], "resposta": 0, "explicacao": "Quinto = Ordine numerale. Quinto = fifth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Ordine numerale:\nÈ la _____ (settima) volta.", "resposta": "settima", "explicacao": "Ordine: settima. È la settima volta."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Ordine numerale:\nLei è il _____ (dodicesimo) studente.", "resposta": "dodicesimo", "explicacao": "Ordine: dodicesimo. Lei è il dodicesimo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'tenth'? A:", "opcoes": ["decimo", "dieci", "dici"], "resposta": 0, "explicacao": "Decimo = Ordine numerale. Decimo = tenth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Ordine numerale:\nViviamo in _____ (ventunesimo) secolo.", "resposta": "ventunesimo", "explicacao": "Ordine: ventunesimo. Viviamo in ventunesimo secolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Ordine numerale:\nÈ la _____ (ventesima) edizione.", "resposta": "ventesima", "explicacao": "Ordine: ventesima. È la ventesima edizione."},
    {"tipo": "escolha", "pergunta": "Come si dice 'three hundredth'? A:", "opcoes": ["trecentesimo", "trecento", "tre"], "resposta": 0, "explicacao": "Trecentesimo = Ordine numerale. Trecentesimo = three hundredth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Ordine numerale:\nSiamo _____ (ventunesimi) arrivati.", "resposta": "ventunesimi", "explicacao": "Ordine: ventunesimi. Siamo ventunesimi arrivati."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Ordine numerale:\nÈ la _____ (centesima) pagina.", "resposta": "centesima", "explicacao": "Ordine: centesima. È la centesima pagina."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'first'? A:", "opcoes": ["uno", "primo", "unico"], "resposta": 1, "explicacao": "Primo = Ordine numerale. Primo = first."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Ordine numerale:\nÈ il _____ (centesimo) giorno.", "resposta": "centesimo", "explicacao": "Ordine: centesimo. È il centesimo giorno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Ordine numerale:\nÈ la _____ (quattordicesima) volta.", "resposta": "quattordicesima", "explicacao": "Ordine: quattordicesima. È la quattordicesima volta."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'hundredth'? A:", "opcoes": ["centesimo", "cento", "mille"], "resposta": 0, "explicacao": "Centesimo = Ordine numerale. Centesimo = hundredth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Ordine numerale:\nÈ il _____ (quarantesimo) capitolo.", "resposta": "quarantesimo", "explicacao": "Ordine: quarantesimo. È il quarantesimo capitolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Ordine numerale:\nÈ la _____ (nona) ora.", "resposta": "nona", "explicacao": "Ordine: nona. È la nona ora."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'fortieth'? A:", "opcoes": ["quarantesimo", "quaranta", "quattordici"], "resposta": 0, "explicacao": "Quarantesimo = Ordine numerale. Quarantesimo = fortieth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Ordine numerale:\nÈ il _____ (ottavo) membro.", "resposta": "ottavo", "explicacao": "Ordine: ottavo. È il ottavo membro."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Ordine numerale:\nÈ la _____ (quindicesima) canzone.", "resposta": "quindicesima", "explicacao": "Ordine: quindicesima. È la quindicesima canzone."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'eleventh'? A:", "opcoes": ["undicesimo", "undici", "uno"], "resposta": 0, "explicacao": "Undicesimo = Ordine numerale. Undicesimo = eleventh."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Ordine numerale:\nÈ il _____ (undicesimo) turno.", "resposta": "undicesimo", "explicacao": "Ordine: undicesimo. È il undicesimo turno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Ordine numerale:\nÈ la _____ (decima) volta.", "resposta": "decima", "explicacao": "Ordine: decima. È la decima volta."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'sixth'? A:", "opcoes": ["sesto", "sei", "sesta"], "resposta": 0, "explicacao": "Sesto = Ordine numerale. Sesto = sixth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Ordine numerale:\nÈ il _____ (sesto) livello.", "resposta": "sesto", "explicacao": "Ordine: sesto. È il sesto livello."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Ordine numerale:\nÈ la _____ (quinta) nota.", "resposta": "quinta", "explicacao": "Ordine: quinta. È la quinta nota."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'third'? A:", "opcoes": ["terzo", "tre", "trenta"], "resposta": 0, "explicacao": "Terzo = Ordine numerale. Terzo = third."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Ordine numerale:\nÈ il _____ (terzo) posto.", "resposta": "terzo", "explicacao": "Ordine: terzo. È il terzo posto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Ordine numerale:\nÈ la _____ (seconda) volta.", "resposta": "seconda", "explicacao": "Ordine: seconda. È la seconda volta."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'twentieth'? A:", "opcoes": ["ventesimo", "vенти", "due"], "resposta": 0, "explicacao": "Ventesimo = Ordine numerale. Ventesimo = twentieth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Ordine numerale:\nÈ il _____ (ventesimo) giorno.", "resposta": "ventesimo", "explicacao": "Ordine: ventesimo. È il ventesimo giorno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Ordine numerale:\nÈ la _____ (quarta) stanza.", "resposta": "quarta", "explicacao": "Ordine: quarta. È la quarta stanza."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'twelfth'? A:", "opcoes": ["dodicesimo", "doce", "due"], "resposta": 0, "explicacao": "Dodicesimo = Ordine numerale. Dodicesimo = twelfth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Ordine numerale:\nÈ il _____ (dodicesimo) mese.", "resposta": "dodicesimo", "explicacao": "Ordine: dodicesimo. È il dodicesimo mese."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Ordine numerale:\nÈ la _____ (prima) ora.", "resposta": "prima", "explicacao": "Ordine: prima. È la prima ora."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'seventh'? A:", "opcoes": ["settimo", "sette", "settanta"], "resposta": 0, "explicacao": "Settimo = Ordine numerale. Settimo = seventh."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Ordine numerale:\nÈ il _____ (settimo) giorno.", "resposta": "settimo", "explicacao": "Ordine: settimo. È il settimo giorno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Ordine numerale:\nÈ la _____ (nona) lettera.", "resposta": "nona", "explicacao": "Ordine: nona. È la nona lettera."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'fifteenth'? A:", "opcoes": ["quindicesimo", "quindici", "diciotto"], "resposta": 0, "explicacao": "Quindicesimo = Ordine numerale. Quindicesimo = fifteenth."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Ordine numerale:\nÈ il _____ (quindicesimo) posto.", "resposta": "quindicesimo", "explicacao": "Ordine: quindicesimo. È il quindicesimo posto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Ordine numerale:\nÈ la _____ (trentesima) volta.", "resposta": "trentesima", "explicacao": "Ordine: trentesima. È la trentesima volta."}
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
