import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XIX")

novos = [
    # 30 exercícios sobre Gli articoli possessivi
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Artico possessivo:\nQuesto è _____ macchina (tua).", "resposta": "la tua", "explicacao": "Articolo possessivo femminile singolare. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Artico possessivo:\nQuello è _____ libro (suo).", "resposta": "il suo", "explicacao": "Articolo possessivo maschile singolare. Suo = his/her."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'your house'? A:", "opcoes": ["casa tua", "tua casa", "casa vostra"], "resposta": 1, "explicacao": "Tua casa = Possessivo. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Artico possessivo:\nQuesto è _____ casa (tua).", "resposta": "la tua", "explicacao": "Articolo possessivo femminile singolare. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Artico possessivo:\nQuello è _____ amico (mio).", "resposta": "il mio", "explicacao": "Articolo possessivo maschile singolare. Mio = my."},
    {"tipo": "escolha", "pergunta": "Come si dice 'his father'? A:", "opcoes": ["padre suo", "suo padre", "suoi"], "resposta": 1, "explicacao": "Suo padre = Possessivo. Suo = his."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Artico possessivo:\nQuesto è _____ figlio (suo).", "resposta": "il suo", "explicacao": "Articolo possessivo maschile singolare. Suo = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Artico possessivo:\nQuello è _____ sorella (mia).", "resposta": "la mia", "explicacao": "Articolo possessivo femminile singolare. Mia = my."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'my brother'? A:", "opcoes": ["fratello mio", "mio fratello", "mia fratello"], "resposta": 1, "explicacao": "Mio fratello = Possessivo. Mio = my."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Artico possessivo:\nQuesto è _____ moglie (sua).", "resposta": "la sua", "explicacao": "Articolo possessivo femminile singolare. Sua = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Artico possessivo:\nQuello è _____ zio (nostro).", "resposta": "il nostro", "explicacao": "Articolo possessivo maschile singolare. Nostro = our."},
    {"tipo": "escolha", "pergunta": "Come si dice 'her mother'? A:", "opcoes": ["madre suo", "sua madre", "mamma lei"], "resposta": 1, "explicacao": "Sua madre = Possessivo. Sua = her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Artico possessivo:\nQuesto è _____ padre (suo).", "resposta": "il suo", "explicacao": "Articolo possessivo maschile singolare. Suo = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Artico possessivo:\nQuello è _____ cugina (tua).", "resposta": "la tua", "explicacao": "Articolo possessivo femminile singolare. Tua = your."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'our home'? A:", "opcoes": ["casa nostri", "nostro casa", "la nostra casa"], "resposta": 2, "explicacao": "La nostra casa = Possessivo. Nostra = our."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Artico possessivo:\nQuesto è _____ cugino (mia).", "resposta": "il mio", "explicacao": "Articolo possessivo maschile singolare. Mio = my."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Artico possessivo:\nQuello è _____ nipote (suo).", "resposta": "il suo", "explicacao": "Articolo possessivo maschile singolare. Suo = his/her."},
    {"tipo": "escolha", "pergunta": "Come si dice 'their car'? A:", "opcoes": ["auto loro", "loro auto", "la loro auto"], "resposta": 2, "explicacao": "La loro auto = Possessivo. Loro = their."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Artico possessivo:\nQuesto è _____ nonno (tua).", "resposta": "il tuo", "explicacao": "Articolo possessivo maschile singolare. Tuo = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Artico possessivo:\nQuello è _____ nipoti (nostri).", "resposta": "i nostri", "explicacao": "Articolo possessivo maschile plurale. Nostri = our."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'your father'? A:", "opcoes": ["padre tuo", "tuo padre", "padre vostra"], "resposta": 1, "explicacao": "Tuo padre = Possessivo. Tuo = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Artico possessivo:\nQuesto è _____ zia (tua).", "resposta": "la tua", "explicacao": "Articolo possessivo femminile singolare. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Artico possessivo:\nQuello è _____ fratelli (loro).", "resposta": "i loro", "explicacao": "Articolo possessivo maschile plurale. Loro = their."},
    {"tipo": "escolha", "pergunta": "Come si dice 'your sister'? A:", "opcoes": ["sorella tua", "tua sorella", "sorella vostra"], "resposta": 1, "explicacao": "Tua sorella = Possessivo. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Artico possessivo:\nQuesto è _____ cognato (suo).", "resposta": "il suo", "explicacao": "Articolo possessivo maschile singolare. Suo = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Artico possessivo:\nQuello è _____ sorelle (loro).", "resposta": "le loro", "explicacao": "Articolo possessivo femminile plurale. Loro = their."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'their parents'? A:", "opcoes": ["genitori loro", "loro genitori", "i loro genitori"], "resposta": 2, "explicacao": "I loro genitori = Possessivo. Loro = their."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Artico possessivo:\nQuesto è _____ nonna (tua).", "resposta": "la tua", "explicacao": "Articolo possessivo femminile singolare. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Artico possessivo:\nQuello è _____ cugini (nostri).", "resposta": "i nostri", "explicacao": "Articolo possessivo maschile plurale. Nostri = our."},
    {"tipo": "escolha", "pergunta": "Come si dice 'her friend'? A:", "opcoes": ["amico suo", "suo amico", "amice lei"], "resposta": 1, "explicacao": "Suo amico = Possessivo. Suo = her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Artico possessivo:\nQuesto è _____ cognata (suo).", "resposta": "la sua", "explicacao": "Articolo possessivo femminile singolare. Sua = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Artico possessivo:\nQuello è _____ zii (nostri).", "resposta": "i nostri", "explicacao": "Articolo possessivo maschile plurale. Nostri = our."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'our room'? A:", "opcoes": ["stanza nostro", "nostro stanza", "la nostra stanza"], "resposta": 2, "explicacao": "La nostra stanza = Possessivo. Nostra = our."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Artico possessivo:\nQuesto è _____ zia (sua).", "resposta": "la sua", "explicacao": "Articolo possessivo femminile singolare. Sua = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Artico possessivo:\nQuello è _____ nipoti (tuoi).", "resposta": "i tuoi", "explicacao": "Articolo possessivo maschile plurale. Tuoi = your."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'his wife'? A:", "opcoes": ["moglie suo", "sua moglie", "moglie lui"], "resposta": 1, "explicacao": "Sua moglie = Possessivo. Sua = his."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Artico possessivo:\nQuesto è _____ cognata (sua).", "resposta": "la sua", "explicacao": "Articolo possessivo femminile singolare. Sua = his/her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Artico possessivo:\nQuello è _____ sorelline (loro).", "resposta": "le loro", "explicacao": "Articolo possessivo femminile plurale. Loro = their."},
    {"tipo": "escolha", "pergunta": "Come si dice 'your room'? A:", "opcoes": ["stanza tua", "tua stanza", "stanza vostra"], "resposta": 1, "explicacao": "Tua stanza = Possessivo. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Artico possessivo:\nQuesto è _____ marito (mia).", "resposta": "il mio", "explicacao": "Articolo possessivo maschile singolare. Mio = my."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Artico possessivo:\nQuello è _____ cugine (loro).", "resposta": "i loro", "explicacao": "Articolo possessivo maschile plurale. Loro = their."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'her sister'? A:", "opcoes": ["sorella suo", "sua sorella", "sorella lei"], "resposta": 1, "explicacao": "Sua sorella = Possessivo. Sua = her."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Artico possessivo:\nQuesto è _____ cognata (tua).", "resposta": "la tua", "explicacao": "Articolo possessivo femminile singolare. Tua = your."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Artico possessivo:\nQuello è _____ fratelli (tuoi).", "resposta": "i tuoi", "explicacao": "Articolo possessivo maschile plurale. Tuoi = your."}
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
