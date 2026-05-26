import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XXII")

novos = [
    # 30 exercícios sobre Il congiuntivo
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Congiuntivo presente:\nSpero _____ venghi.", "resposta": "che tu venga", "explicacao": "Congiuntivo: che + subj. Spero che tu venga."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Congiuntivo presente:\nPensavo _____ fossi pronto.", "resposta": "che tu fossi", "explicacao": "Congiuntivo imperfetto: che + subj. Pensavo che tu fossi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I hope you come'? A:", "opcoes": ["spero vieni", "spero tu venga", "spero che viene"], "resposta": 1, "explicacao": "Spero che tu venga = Congiuntivo presente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Congiuntivo presente:\nVorrei _____ fosse vero.", "resposta": "che fosse", "explicacao": "Congiuntivo: che + subj. Vorrei che fosse."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Congiuntivo presente:\nÈ importante _____ studi di più.", "resposta": "che tu studi", "explicacao": "Congiuntivo: che + subj. È importante che tu studi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'if I knew'? A:", "opcoes": ["se sapessi", "se so", "se ho"], "resposta": 0, "explicacao": "Se sapessi = Congiuntivo imperfetto per condizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Congiuntivo presente:\nPenso _____ sia giusto.", "resposta": "che sia", "explicacao": "Congiuntivo: che + subj. Penso che sia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Congiuntivo presente:\nÈ possibile _____ arrivi.", "resposta": "che arrivi", "explicacao": "Congiuntivo: che + subj. È possibile che arrivi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I want you to go'? A:", "opcoes": ["voglio tu vada", "vorrei tu venga", "voglio che tu vada"], "resposta": 2, "explicacao": "Voglio che tu vada = Congiuntivo presente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Congiuntivo presente:\nÈ necessario _____ venga.", "resposta": "che venga", "explicacao": "Congiuntivo: che + subj. È necessario che venga."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Congiuntivo presente:\nDubito _____ abbia ragione.", "resposta": "che abbia", "explicacao": "Congiuntivo: che + subj. Dubito che abbia."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I wish I were'? A:", "opcoes": ["spero sono", "vorrei fossi", "mi auguro fossi"], "resposta": 2, "explicacao": "Mi auguro fossi = Congiuntivo imperfetto per desiderio."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Congiuntivo presente:\nSembra _____ sia facile.", "resposta": "che sia", "explicacao": "Congiuntivo: che + subj. Sembra che sia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Congiuntivo presente:\nÈ strano _____ parta.", "resposta": "che parta", "explicacao": "Congiuntivo: che + subj. È strano che parta."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I hope she passes'? A:", "opcoes": ["spero passa", "spero tu passi", "spero che passi"], "resposta": 2, "explicacao": "Spero che passi = Congiuntivo presente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Congiuntivo presente:\nAffliggo _____ non abbia successo.", "resposta": "che non abbia", "explicacao": "Congiuntivo: che + subj. Affliggo che non abbia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Congiuntivo presente:\nPreferirei _____ fossi qui.", "resposta": "che tu fossi", "explicacao": "Congiuntivo imperfetto: che + subj. Preferirei che tu fossi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I think he is'? A:", "opcoes": ["penso è", "penso che sia", "penso lui è"], "resposta": 1, "explicacao": "Penso che sia = Congiuntivo presente dopo pensare."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Congiuntivo presente:\nÈ meglio _____ studi.", "resposta": "che tu studi", "explicacao": "Congiuntivo: che + subj. È meglio che tu studi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Congiuntivo presente:\nNon credo _____ venga.", "resposta": "che venga", "explicacao": "Congiuntivo: che + subj. Non credo che venga."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I wish I had'? A:", "opcoes": ["vorrei aveva", "mi auguro avessi", "preferevo avevo"], "resposta": 1, "explicacao": "Mi auguro avessi = Congiuntivo imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Congiuntivo presente:\nÈ probabile _____ riesca.", "resposta": "che riesca", "explicacao": "Congiuntivo: che + subj. È probabile che riesca."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Congiuntivo presente:\nSento _____ sia vero.", "resposta": "che sia", "explicacao": "Congiuntivo: che + subj. Sento che sia."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I wish you would'? A:", "opcoes": ["vorrei faresti", "mi auguro facessi", "spero farai"], "resposta": 1, "explicacao": "Mi auguro facessi = Congiuntivo imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Congiuntivo presente:\nÈ incredibile _____ abbia vinto.", "resposta": "che abbia", "explicacao": "Congiuntivo: che + subj. È incredibile che abbia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Congiuntivo presente:\nNon è possibile _____ lavori.", "resposta": "che tu lavori", "explicacao": "Congiuntivo: che + subj. Non è possibile che tu lavori."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I hope he comes'? A:", "opcoes": ["spero viene", "spero che venga", "spero tu vieni"], "resposta": 1, "explicacao": "Spero che venga = Congiuntivo presente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Congiuntivo presente:\nMi dispiace _____ non riesca.", "resposta": "che non riesca", "explicacao": "Congiuntivo: che + subj. Mi dispiace che non riesca."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Congiuntivo presente:\nSospetto _____ sia vero.", "resposta": "che sia", "explicacao": "Congiuntivo: che + subj. Sospetto che sia."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I wish I could'? A:", "opcoes": ["vorrei potessi", "mi auguro potessi", "spero puoi"], "resposta": 1, "explicacao": "Mi auguro potessi = Congiuntivo imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Congiuntivo presente:\nÈ urgente _____ arrivi.", "resposta": "che tu arrivi", "explicacao": "Congiuntivo: che + subj. È urgente che tu arrivi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Congiuntivo presente:\nNon penso _____ abbia senso.", "resposta": "che abbia", "explicacao": "Congiuntivo: che + subj. Non penso che abbia."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I hope you win'? A:", "opcoes": ["spero vinci", "spero tu vinca", "spero che tu vinca"], "resposta": 2, "explicacao": "Spero che tu vinca = Congiuntivo presente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Congiuntivo presente:\nNon mi piace _____ tu parli.", "resposta": "che tu parli", "explicacao": "Congiuntivo: che + subj. Non mi piace che tu parli."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Congiuntivo presente:\nNon voglio _____ vada via.", "resposta": "che parta", "explicacao": "Congiuntivo: che + subj. Non voglio che parta."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I hope she succeeds'? A:", "opcoes": ["spero riesce", "spero tu riesca", "spero lei ha successo"], "resposta": 1, "explicacao": "Spero che tu riesca = Congiuntivo presente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Congiuntivo presente:\nÈ meglio _____ non lo faccia.", "resposta": "che tu non faccia", "explicacao": "Congiuntivo: che + subj. È meglio che tu non faccia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Congiuntivo presente:\nVorrei _____ fossimo insieme.", "resposta": "che fossimo", "explicacao": "Congiuntivo imperfetto: che + subj. Vorrei che fossimo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I wish I were here'? A:", "opcoes": ["vorrei ero", "mi auguro fossi", "spero sono"], "resposta": 1, "explicacao": "Mi auguro fossi = Congiuntivo imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Congiuntivo presente:\nDubito _____ abbia successo.", "resposta": "che abbia", "explicacao": "Congiuntivo: che + subj. Dubito che abbia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Congiuntivo presente:\nNon è certo _____ venga.", "resposta": "che venga", "explicacao": "Congiuntivo: che + subj. Non è certo che venga."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I wish you were'? A:", "opcoes": ["vorrei eri", "mi auguro fossi", "spero sei"], "resposta": 1, "explicacao": "Mi auguro fossi = Congiuntivo imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Congiuntivo presente:\nÈ chiaro _____ sia necessario.", "resposta": "che sia", "explicacao": "Congiuntivo: che + subj. È chiaro che sia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Congiuntivo presente:\nSospetto _____ sia il caso.", "resposta": "che sia", "explicacao": "Congiuntivo: che + subj. Sospetto che sia."}
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
