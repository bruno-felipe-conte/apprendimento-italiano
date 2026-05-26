import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VII")

novos = [
    # 30 exercícios sobre I possessivi
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Aggettivo possessivo con articolo:\nIo vedo _____ zaino (mio)", "resposta": "lo zio mio", "explicacao": "Aggettivo possessivo con articolo: il mio, la mia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Aggettivo possessivo con articolo:\nTu vedi _____ libro (tuo)", "resposta": "il tuo libro", "explicacao": "Aggettivo possessivo con artigo: il tuo, la tua."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'his mother'? A:", "opcoes": ["madre suo", "sua madre", "la madre lui"], "resposta": 1, "explicacao": "Sua madre = Sua madre. Possessivo con nome di parentela."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Aggettivo possessivo senza articolo:\nVado a _____ (casa mia)", "resposta": "a casa mia", "explicacao": "A casa mia = Possessivo senza articolo. Si usa per luoghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Aggettivo possessivo senza articolo:\nMi dispiace _____ (pesco tuo)", "resposta": "pezzo tuo", "explicacao": "Pezzo tuo = Possessivo senza artigo per oggetti personali."},
    {"tipo": "escolha", "pergunta": "Come si dice 'my car' in italiano?", "opcoes": ["macchina mio", "la mia macchina", "mia macchina"], "resposta": 1, "explicacao": "La mia macchina = Possessivo con articolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Aggettivo possessivo senza articolo:\nTelefono a _____ (amico tuo)", "resposta": "al tuo amico", "explicacao": "Al tuo amico = Possessivo con preposizione articolata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Aggettivo possessivo senza articolo:\nLeggo _____ (giornale mio)", "resposta": "il giornale mio", "explicacao": "Il giornale mio = Possessivo con artigo per oggetti."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'her book'? A:", "opcoes": ["libro lei", "libro suo", "suo libro"], "resposta": 2, "explicacao": "Suo libro = Possessivo senza artigo con nome."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Aggettivo possessivo senza articolo:\nMangio _____ (panino mio)", "resposta": "il panino mio", "explicacao": "Il panino mio = Possessivo con artigo per cibo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Aggettivo possessivo senza articolo:\nBevo _____ (caffè tuo)", "resposta": "il tuo caffè", "explicacao": "Il tuo caffè = Possessivo con artigo per bevande."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'their house'? A:", "opcoes": ["casa loro", "la casa loro", "loro casa"], "resposta": 1, "explicacao": "La casa loro = Possessivo con articolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Aggettivo possessivo senza articolo:\nVedo _____ (sorella tua)", "resposta": "la sorella tua", "explicacao": "La sorella tua = Possessivo con artigo per parentela."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Aggettivo possessivo senza articolo:\nAspetto _____ (collega tuo)", "resposta": "il tuo collega", "explicacao": "Il tuo collega = Possessivo con artigo per colleghi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'our company' in italiano?", "opcoes": ["azienda noi", "nostra azienda", "la nostra azienda"], "resposta": 2, "explicacao": "La nostra azienda = Possessivo con articolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Aggettivo possessivo senza articolo:\nDiro a _____ (maestro tuo)", "resposta": "al tuo maestro", "explicacao": "Al tuo maestro = Possessivo con preposizione articolata."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Aggettivo possessivo senza articolo:\nPorto _____ (vestito mio)", "resposta": "il mio vestito", "explicacao": "Il mio vestito = Possessivo con artigo per vestiti."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'your phone'? A:", "opcoes": ["telefono tuo", "tuo telefono", "tu telefono"], "resposta": 0, "explicacao": "Telefono tuo = Possessivo senza artigo per oggetti."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Aggettivo possessivo senza articolo:\nMando _____ (email mia)", "resposta": "la mia email", "explicacao": "La mia email = Possessivo con artigo per oggetti digitali."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Aggettivo possessivo senza articolo:\nScrivo _____ (articolo mio)", "resposta": "l'articolo mio", "explicacao": "L'articolo mio = Possessivo con artigo per documenti."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'his friend'? A:", "opcoes": ["amico suo", "sua amico", "lui amico"], "resposta": 0, "explicacao": "Amico suo = Possessivo con nome di persona."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Aggettivo possessivo senza articolo:\nCerco _____ (chiavi tue)", "resposta": "le tue chiavi", "explicacao": "Le tue chiavi = Possessivo con artigo per oggetti."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Aggettivo possessivo senza articolo:\nSento _____ (musicia tua)", "resposta": "la tua musica", "explicacao": "La tua musica = Possessivo con artigo per arte."},
    {"tipo": "escolha", "pergunta": "Come si dice 'their children' in italiano?", "opcoes": ["figli loro", "loro figli", "i loro figli"], "resposta": 2, "explicacao": "I loro figli = Possessivo con articolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Aggettivo possessivo senza articolo:\nHo _____ (problemi suoi)", "resposta": "i suoi problemi", "explicacao": "I suoi problemi = Possessivo con artigo per cose."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Aggettivo possessivo senza articolo:\nPenso a _____ (padre mio)", "resposta": "al mio padre", "explicacao": "Al mio padre = Possessivo con preposizione articolata per parentela."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'your friends'? A:", "opcoes": ["amici tuoi", "tuoi amici", "tuo amici"], "resposta": 1, "explicacao": "Tuoi amici = Possessivo con nome di persone."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Aggettivo possessivo senza articolo:\nFaccio _____ (lavoro mio)", "resposta": "il mio lavoro", "explicacao": "Il mio lavoro = Possessivo con artigo per attività."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Aggettivo possessivo senza articolo:\nStudio _____ (lingua tua)", "resposta": "la tua lingua", "explicacao": "La tua lingua = Possessivo con artigo per lingue."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'her friends'? A:", "opcoes": ["amici sua", "sue amici", "le sue amiche"], "resposta": 2, "explicacao": "Le sue amiche = Possessivo con nome di persone femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Aggettivo possessivo senza articolo:\nConosco _____ (colleghi tuoi)", "resposta": "i tuoi colleghi", "explicacao": "I tuoi colleghi = Possessivo con artigo per colleghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Aggettivo possessivo senza articolo:\nMi piace _____ (punto di vista tuo)", "resposta": "il tuo punto", "explicacao": "Il tuo punto = Possessivo con artigo per idee."},
    {"tipo": "escolha", "pergunta": "Come si dice 'their parents'? A:", "opcoes": ["genitori loro", "loro genitori", "i loro genitori"], "resposta": 2, "explicacao": "I loro genitori = Possessivo con articolo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Aggettivo possessivo senza articolo:\nVoglio _____ (casa tua)", "resposta": "la tua casa", "explicacao": "La tua casa = Possessivo con preposizione per luoghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Aggettivo possessivo senza articolo:\nSento _____ (voglia sua)", "resposta": "la sua voglia", "explicacao": "La sua voglia = Possessivo con artigo per emozioni."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'their school'? A:", "opcoes": ["scuola loro", "loro scuola", "la loro scuola"], "resposta": 2, "explicacao": "La loro scuola = Possessivo con artigo per luoghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Aggettivo possessivo senza articolo:\nLeggo _____ (romanzi suoi)", "resposta": "i suoi romanzi", "explicacao": "I suoi romanzi = Possessivo con artigo per libri."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Aggettivo possessivo senza articolo:\nAscolto _____ (radio tua)", "resposta": "la tua radio", "explicacao": "La tua radio = Possessivo con artigo per oggetti."},
    {"tipo": "escolha", "pergunta": "Come si dice 'her brother'? A:", "opcoes": ["fratello sua", "suo fratello", "lei fratello"], "resposta": 1, "explicacao": "Suo fratello = Possessivo con nome di persona."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Aggettivo possessivo senza articolo:\nVedo _____ (sorelle tue)", "resposta": "le tue sorelle", "explicacao": "Le tue sorelle = Possessivo con artigo per parentela."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Aggettivo possessivo senza articolo:\nPenso a _____ (vecchio mio)", "resposta": "al mio vecchio", "explicacao": "Al mio vecchio = Possessivo con preposizione articolata per persone."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'your sister'? A:", "opcoes": ["sorella tua", "tua sorella", "la tua sorella"], "resposta": 2, "explicacao": "La tua sorella = Possessivo con articolo per parentela."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Aggettivo possessivo senza articolo:\nMando _____ (messaggi suoi)", "resposta": "i suoi messaggi", "explicacao": "I suoi messaggi = Possessivo con artigo per comunicazioni."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Aggettivo possessivo senza articolo:\nPreparo _____ (pranzo mio)", "resposta": "il mio pranzo", "explicacao": "Il mio pranzo = Possessivo con artigo per cibo."}
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
