import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione II")

novos = [
    # 30 exercícios sobre Verbi -ARE/-ERE/-IRE / Avere / Essere
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Coniugazione presente di mangiare:\nIo _____ (mangiare), Tu _____ (mangiare)", "resposta": "mangio, mangi", "explicacao": "-ARE: Io -o, Tu -i. Io mangio, tu mangi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Essere presente:\nIo _____ (essere), Tu _____ (essere)", "resposta": "sono, sei", "explicacao": "ESSERE irregolare: Io sono, tu sei."},
    {"tipo": "escolha", "pergunta": "Come si dice 'we eat' in italiano?", "opcoes": ["mangiamo", "mangiato", "mangeremo"], "resposta": 0, "explicacao": "Mangiare (Io mangio, noi mangiamo)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Avere presente:\nIo _____ (avere), Lui _____ (avere)", "resposta": "ho, ha", "explicacao": "AVERE irregolare: Io ho, tu hai, lui ha."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Coniugazione presente di amare:\nNoi _____ (amare), Voi _____ (amare)", "resposta": "amiamo, amate", "explicacao": "-ARE: Noi -iamo, Voi -ate."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she is'?", "opcoes": ["è", "sei", "sono"], "resposta": 0, "explicacao": "È = Lui/lei è (essere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Essere irregolare:\nLoro _____ (essere), Voi _____ (essere)", "resposta": "sono, siete", "explicacao": "ESSERE: Loro sono, voi siete."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Verbo avere irregolare:\nTu _____ (avere), Essi _____ (avere)", "resposta": "hai, hanno", "explicacao": "AVERE: Tu hai, essi/esse hanno."},
    {"tipo": "escolha", "pergunta": "Quale verbo è corretto per 'we love'?", "opcoes": ["amiamo", "amo", "amoremo"], "resposta": 0, "explicacao": "Amare (noi amiamo)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Coniugazione di studiare:\nTu _____ (studiare), Lei _____ (studiare)", "resposta": "studi, studia", "explicacao": "-ARE: Tu -i, Lei -a. Tu studi, lei studia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Essere irregolare:\nNoi _____ (essere), Voi _____ (essere)", "resposta": "siamo, siete", "explicacao": "ESSERE: Noi siamo, voi siete."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he has' in italiano?", "opcoes": ["ha", "hanno", "abbiamo"], "resposta": 0, "explicacao": "Ha = Lui/lei ha (avere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Verbo avere irregolare:\nIo _____ (avere), Lei _____ (avere)", "resposta": "ho, ha", "explicacao": "AVERE: Io ho, lui/lei ha."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Coniugazione di parlare:\nTu _____ (parlare), Loro _____ (parlare)", "resposta": "parli, parlano", "explicacao": "-ARE: Tu -i, Loro -ano. Tu parli, loro parlano."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you are' (voi)?", "opcoes": ["è", "sei", "siete"], "resposta": 2, "explicacao": "Siete = Voi siete (essere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Verbo essere irregolare:\nIo _____ (essere), Tu _____ (essere)", "resposta": "sono, sei", "explicacao": "ESSERE: Io sono, tu sei."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Verbo avere irregolare:\nTu _____ (avere), Lui _____ (avere)", "resposta": "hai, ha", "explicacao": "AVERE: Tu hai, lui/lei ha."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they are' in italiano?", "opcoes": ["sono", "sei", "siete"], "resposta": 0, "explicacao": "Sono = Loro sono (essere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Coniugazione di scrivere:\nLei _____ (scrivere), Io _____ (scrivere)", "resposta": "scrive, scrivo", "explicacao": "-IRE: Lei -e, Io -o. Lei scrive, io scrivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Verbo avere irregolare:\nNoi _____ (avere), Voi _____ (avere)", "resposta": "abbiamo, avete", "explicacao": "AVERE: Noi abbiamo, voi avete."},
    {"tipo": "escolha", "pergunta": "Quale verbo è corretto per 'she eats'?", "opcoes": ["mangia", "mangiare", "mangiato"], "resposta": 0, "explicacao": "Mangiare: Lei mangia (terza persona)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Verbo essere irregolare:\nTu _____ (essere), Loro _____ (essere)", "resposta": "sei, sono", "explicacao": "ESSERE: Tu sei, loro sono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Coniugazione di finire:\nVoi _____ (finire), Io _____ (finire)", "resposta": "finite, finisco", "explicacao": "-IRE: Voi -ite, Io -isco. Voi finite, io finisco."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I am' in italiano?", "opcoes": ["sono", "sei", "siete"], "resposta": 0, "explicacao": "Sono = Io sono (essere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Verbo avere irregolare:\nVoi _____ (avere), Loro _____ (avere)", "resposta": "avete, hanno", "explicacao": "AVERE: Voi avete, loro/esse hanno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Coniugazione di aprire:\nNoi _____ (aprire), Io _____ (aprire)", "resposta": "apriamo, apro", "explicacao": "-IRE: Noi -iamo, Io -o. Noi apriamo, io apro."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they have'?", "opcoes": ["hanno", "hai", "ha"], "resposta": 0, "explicacao": "Hanno = Loro hanno (avere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Verbo essere irregolare:\nLei _____ (essere), Noi _____ (essere)", "resposta": "è, siamo", "explicacao": "ESSERE: Lei è, noi siamo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Coniugazione di bere:\nLoro _____ (bere), Tu _____ (bere)", "resposta": "beono, bevi", "explicacao": "-ERE irregolare: Loro bevono, tu bevi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I love you' in italiano?", "opcoes": ["ti amo", "amo te", "amiamo te"], "resposta": 0, "explicacao": "Amo (Io amo) + ti = Ti amo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Verbo avere irregolare:\nEssa _____ (avere), Essi _____ (avere)", "resposta": "ha, hanno", "explicacao": "AVERE: Essa/ella ha, essi/e hanno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Coniugazione di uscire:\nIo _____ (uscire), Tu _____ (uscire)", "resposta": "esco, esci", "explicacao": "-IRE irregolare: Io esco, tu esci."},
    {"tipo": "escolha", "pergunta": "Quale verbo è corretto per 'he is'?", "opcoes": ["è", "sei", "sono"], "resposta": 0, "explicacao": "È = Lui/lei è (essere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Verbo essere irregolare:\nEssi _____ (essere), Esse _____ (essere)", "resposta": "sono, sono", "explicacao": "ESSERE: Essi/esse sono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Coniugazione di andare:\nLoro _____ (andare), Tu _____ (andare)", "resposta": "vanno, vai", "explicacao": "ANDARE irregolare: Loro vanno, tu vai."},
    {"tipo": "escolha", "pergunta": "Come si dice 'we are' in italiano?", "opcoes": ["siamo", "siete", "sono"], "resposta": 0, "explicacao": "Siamo = Noi siamo (essere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Verbo avere irregolare:\nIo _____ (avere), Tu _____ (avere)", "resposta": "ho, hai", "explicacao": "AVERE: Io ho, tu hai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Coniugazione di leggere:\nLei _____ (leggere), Loro _____ (leggere)", "resposta": "legge, leggono", "explicacao": "-ERE regolare: Lei -e, Loro -ono. Lei legge, loro leggono."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you have' (tu)?", "opcoes": ["hai", "ha", "abbiamo"], "resposta": 0, "explicacao": "Hai = Tu hai (avere)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Verbo essere irregolare:\nLui _____ (essere), Essa _____ (essere)", "resposta": "è, è", "explicacao": "ESSERE: Lui/lei è."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Coniugazione di giocare:\nIo _____ (giocare), Voi _____ (giocare)", "resposta": "gioco, giocate", "explicacao": "-ARE: Io -o, Voi -ate. Io gioco, voi giocate."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she loves' in italiano?", "opcoes": ["ama", "amo", "amare"], "resposta": 0, "explicacao": "Amare: Lei ama (terza persona)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Verbo avere irregolare:\nLei _____ (avere), Loro _____ (avere)", "resposta": "ha, hanno", "explicacao": "AVERE: Lei ha, loro/esse hanno."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Coniugazione di dormire:\nTu _____ (dormire), Io _____ (dormire)", "resposta": "dormi, dormo", "explicacao": "-IRE: Tu -i, Io -o. Tu dormi, io dormo."}
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
