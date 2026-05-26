import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione IV")

novos = [
    # 30 exercícios sobre Passato prossimo
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Passato prossimo con AVERE:\nIo _____ mangiato (avere + part. pass.)", "resposta": "ho mangiato", "explicacao": "Ho mangiato = Ho + mangiato. Si usa AVERE per la maggior parte dei verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Passato prossimo con ESSERE:\nIo _____ andato (essere + part. pass.)", "resposta": "sono andato", "explicacao": "Sono andato = Sono + andato. Si usa ESSERE per verbi di moto."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I have eaten'? A:", "opcoes": ["ho mangiato", "sono mangiato", "mangiai"], "resposta": 0, "explicacao": "Ho mangiato = Passato prossimo con AVERE. Sono mangiato è sbagliato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Passato prossimo con AVERE:\nTu _____ bevuto (avere + part. pass.)", "resposta": "hai bevuto", "explicacao": "Hai bevuto = Hai + bevuto. Terza persona di avere: hai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Passato prossimo con ESSERE:\nLui _____ andato (essere + part. pass.)", "resposta": "è andato", "explicacao": "È andato = È + andato. Terza persona di essere: è."},
    {"tipo": "escolha", "pergunta": "Come si dice 'She has slept' in italiano?", "opcoes": ["ha dormito", "dormì", "dormiva"], "resposta": 0, "explicacao": "Ha dormito = Ha + dormito. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Passato prossimo con AVERE:\nLei _____ scritto (avere + part. pass.)", "resposta": "ha scritto", "explicacao": "Ha scritto = Ha + scritto. Terza persona singolare di avere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Passato prossimo con ESSERE:\nNoi _____ stati (essere + part. pass.)", "resposta": "siamo stati", "explicacao": "Siamo stati = Siamo + stati. Noi sono -> siamo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'They have gone'? A:", "opcoes": ["sono andati", "hanno andati", "andarono"], "resposta": 0, "explicacao": "Sono andati = Sono + andati. Essere con verbi di moto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Passato prossimo con AVERE:\nVoi _____ comprato (avere + part. pass.)", "resposta": "avete comprato", "explicacao": "Avete comprato = Avete + comprato. Voi -> avete."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Passato prossimo con ESSERE:\nEssi _____ tornato (essere + part. pass.)", "resposta": "sono tornati", "explicacao": "Sono tornati = Sono + tornati. Essi -> sono."},
    {"tipo": "escolha", "pergunta": "Come si dice 'We have eaten' in italiano?", "opcoes": ["abbiamo mangiato", "siamo mangiati", "mangiammo"], "resposta": 0, "explicacao": "Abbiamo mangiato = Abbiamo + mangiato. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Passato prossimo con AVERE:\nLoro _____ visto (avere + part. pass.)", "resposta": "hanno visto", "explicacao": "Hanno visto = Hanno + visto. Loro -> hanno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Passato prossimo con ESSERE:\nTu _____ venuto (essere + part. pass.)", "resposta": "sei venuto", "explicacao": "Sei venuto = Sei + venuto. Tu -> sei."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'He has written'? A:", "opcoes": ["ha scritto", "scriveva", "scrisse"], "resposta": 0, "explicacao": "Ha scritto = Ha + scritto. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Participio passato regolare:\nmangiare → _____ (mangiato)", "resposta": "mangiato", "explicacao": "-ARE: mangiato. Participio passato regolare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Passato prossimo con ESSERE:\nLei _____ parlato (essere + part. pass.)", "resposta": "ha parlato", "explicacao": "Ha parlato = Ha + parlato. Parlare usa AVERE."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I have gone' in italiano?", "opcoes": ["sono andato", "ho andato", "andai"], "resposta": 0, "explicacao": "Sono andato = Sono + andato. Essere con verbi di moto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Participio passato irregolare:\nessere → _____ (stato)", "resposta": "stato", "explicacao": "Essere è irregolare: stato. Non 'essuto'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Passato prossimo con ESSERE:\nIo _____ visto (essere + part. pass.)", "resposta": "ho visto", "explicacao": "Ho visto = Ho + visto. Vedere usa AVERE."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'She has seen'? A:", "opcoes": ["ha visto", "è vista", "vede"], "resposta": 0, "explicacao": "Ha visto = Ha + visto. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Participio passato irregolare:\ndormire → _____ (dormito)", "resposta": "dormito", "explicacao": "-IRE regolare: dormito. Anche se -ere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Passato prossimo con AVERE:\nNoi _____ giocato (avere + part. pass.)", "resposta": "abbiamo giocato", "explicacao": "Abbiamo giocato = Abbiamo + giocato. Noi -> abbiamo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'He has spoken' in italiano?", "opcoes": ["ha parlato", "parlò", "parlava"], "resposta": 0, "explicacao": "Ha parlato = Ha + parlato. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Passato prossimo con ESSERE:\nLei _____ arrivata (essere + part. pass.)", "resposta": "è arrivata", "explicacao": "È arrivata = È + arrivata. Arrivare usa ESSERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Passato prossimo con AVERE:\nLui _____ lavorato (avere + part. pass.)", "resposta": "ha lavorato", "explicacao": "Ha lavorato = Ha + lavorato. Lavorare usa AVERE."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'They have been'? A:", "opcoes": ["sono stati", "hanno stati", "stettero"], "resposta": 0, "explicacao": "Sono stati = Sono + stati. Essere con verbi di stato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Passato prossimo con AVERE:\nTu _____ comprato (avere + part. pass.)", "resposta": "hai comprato", "explicacao": "Hai comprato = Hai + comprato. Tu -> hai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Passato prossimo con ESSERE:\nIo _____ tornato (essere + part. pass.)", "resposta": "sono tornato", "explicacao": "Sono tornato = Sono + tornato. Tornare usa ESSERE."},
    {"tipo": "escolha", "pergunta": "Come si dice 'She has gone' in italiano?", "opcoes": ["è andata", "è andato", "andò"], "resposta": 0, "explicacao": "È andata = È + andata. Essere con verbi di moto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Participio passato irregolare:\navere → _____ (avuto)", "resposta": "avuto", "explicacao": "Avere è irregolare: avuto. Non 'averuto'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Passato prossimo con AVERE:\nLoro _____ mangiato (avere + part. pass.)", "resposta": "hanno mangiato", "explicacao": "Hanno mangiato = Hanno + mangiato. Loro -> hanno."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I have worked'? A:", "opcoes": ["ho lavorato", "lavorai", "lavorato"], "resposta": 0, "explicacao": "Ho lavorato = Ho + lavorato. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Passato prossimo con ESSERE:\nVoi_____ uscite (essere + part. pass.)", "resposta": "seste usciti", "explicacao": "Siete usciti = Siete + usciti. Usire usa ESSERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Passato prossimo con AVERE:\nLei _____ telefonato (avere + part. pass.)", "resposta": "ha telefonato", "explicacao": "Ha telefonato = Ha + telefonato. Telefonare usa AVERE."},
    {"tipo": "escolha", "pergunta": "Come si dice 'We have seen' in italiano?", "opcoes": ["abbiamo visto", "siamo visti", "videmmo"], "resposta": 0, "explicacao": "Abbiamo visto = Abbiamo + visto. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Participio passato irregolare:\nfare → _____ (fatto)", "resposta": "fatto", "explicacao": "Fare è irregolare: fatto. Non 'feuto'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Passato prossimo con AVERE:\nNoi _____ studiato (avere + part. pass.)", "resposta": "abbiamo studiato", "explicacao": "Abbiamo studiato = Abbiamo + studiato. Noi -> abbiamo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'They have done'? A:", "opcoes": ["hanno fatto", "fecero", "fanno"], "resposta": 0, "explicacao": "Hanno fatto = Hanno + fatto. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Passato prossimo con ESSERE:\nEssi _____ partiti (essere + part. pass.)", "resposta": "sono partiti", "explicacao": "Sono partiti = Sono + partiti. Partire usa ESSERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Passato prossimo con AVERE:\nIo _____ letto (avere + part. pass.)", "resposta": "ho letto", "explicacao": "Ho letto = Ho + letto. Leggere usa AVERE."},
    {"tipo": "escolha", "pergunta": "Come si dice 'You have eaten' in italiano?", "opcoes": ["hai mangiato", "mangiasti", "mangia"], "resposta": 0, "explicacao": "Hai mangiato = Hai + mangiato. Passato prossimo con AVERE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Participio passato irregolare:\ndire → _____ (detto)", "resposta": "detto", "explicacao": "Dire è irregolare: detto. Non 'dito'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Passato prossimo con AVERE:\nTu _____ aperto (avere + part. pass.)", "resposta": "hai aperto", "explicacao": "Hai aperto = Hai + aperto. Aprire usa AVERE."}
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
