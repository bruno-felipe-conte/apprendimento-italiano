import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione III")

novos = [
    # 30 exercícios sobre Preposizioni articolate
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Preposizione articolata:\nio _____ casa (a + la)", "resposta": "vado a casa", "explicacao": "Andare + a + la = andare a casa. Si usa A per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Preposizione articolata:\nIo _____ scuola (in + la)", "resposta": "vado a scuola", "explicacao": "Andare + a + la = andare a scuola."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'di + il'? A:", "opcoes": ["del", "dello", "della"], "resposta": 0, "explicacao": "Di + il = del (preposizione articolata)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Preposizione articolata:\nLui _____ città (da + la)", "resposta": "viene dalla città", "explicacao": "Venire + da + la = venire dalla città. Si usa DA per origine."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Preposizione articolata:\nNoi _____ Italia (in + l')", "resposta": "viamo in Italia", "explicacao": "Andare + in + l' = andare in Italia. Si usa IN per luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'of the man' correttamente?", "opcoes": ["del uomo", "dell'uomo", "dello uomo"], "resposta": 1, "explicacao": "Di + il uomo = Dell'uomo (con apostrofo)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Preposizione articolata:\nNoi _____ casa (di + la)", "resposta": "parliamo della casa", "explicacao": "Parlare + di + la = parlare della casa. Si usa DI per possesso/tema."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Preposizione articolata:\nLui _____ lavoro (a + il)", "resposta": "va a lavoro", "explicacao": "Andare + a + il = andare a lavoro. Si usa A per destinazione."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'con + lo'? A:", "opcoes": ["del", "dello", "colla"], "resposta": 1, "explicacao": "Con + lo = dello (preposizione articolata)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Preposizione articolata:\nLei _____ sorella (con + la)", "resposta": "parla con la sorella", "explicacao": "Parlare + con + la = parlare con la sorella. Si usa CON per compagnia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Preposizione articolata:\nIo _____ parco (in + il)", "resposta": "vado al parco", "explicacao": "Andare + in + il = andare al parco. Si usa IN per luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'from the city' correttamente?", "opcoes": ["dalla città", "del città", "al città"], "resposta": 0, "explicacao": "Da + la città = Dalla città (apostrofo)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Preposizione articolata:\nNoi _____ Italia (in + l')", "resposta": "andiamo in Italia", "explicacao": "Andare + in + l' = andare in Italia. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Preposizione articolata:\nIo _____ libro (di + il)", "resposta": "parlo del libro", "explicacao": "Parlare + di + il = parlare del libro. Si usa DI per tema."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'tra + la'? A:", "opcoes": ["tra", "della", "alla"], "resposta": 0, "explicacao": "Tra/fra sono preposizioni semplici per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Preposizione articolata:\nLui _____ negozio (in + il)", "resposta": "è nel negozio", "explicacao": "Essere + in + il = essere nel negozio. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Preposizione articolata:\nNoi _____ amico (con + l')", "resposta": "parliamo con l'amico", "explicacao": "Parlare + con + l' = parlare con l'amico. Si usa CON per compagnia."},
    {"tipo": "escolha", "pergunta": "Come si dice 'about the book' correttamente?", "opcoes": ["dell libro", "sull libro", "dello libro"], "resposta": 2, "explicacao": "Di + il libro = Del libro (o 'del')."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Preposizione articolata:\nLei _____ ufficio (in + l')", "resposta": "è in ufficio", "explicacao": "Essere + in + l' = essere in ufficio. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Preposizione articolata:\nIo _____ treno (con + il)", "resposta": "vado a bordo del treno", "explicacao": "Andare + su/col + il = andare a bordo del treno. Si usa SU per mezzo."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'per + la'? A:", "opcoes": ["per", "della", "alla"], "resposta": 0, "explicacao": "Per sono preposizione semplice per scopo/luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Preposizione articolata:\nNoi _____ cinema (in + il)", "resposta": "andiamo al cinema", "explicacao": "Andare + in + il = andare al cinema. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Preposizione articolata:\nLui _____ mare (in + il)", "resposta": "va in mare", "explicacao": "Andare + in + il = andare in mare. Si usa IN per luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'with the car' correttamente?", "opcoes": ["con l'auto", "col auto", "del auto"], "resposta": 0, "explicacao": "Con + l' = Col (abbreviazione di collo)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Preposizione articolata:\nLei _____ pizzo (sul + il)", "resposta": "è sullo zio", "explicacao": "Essere + su + lo = essere sullo zio. Si usa SU per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Preposizione articolata:\nIo _____ strada (su + la)", "resposta": "vado sulla strada", "explicacao": "Andare + su + la = andare sulla strada. Si usa SU per posizione."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'sotto + il'? A:", "opcoes": ["sotto", "dello", "allo"], "resposta": 0, "explicacao": "Sotto sono preposizione semplice per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Preposizione articolata:\nNoi _____ casa (a + la)", "resposta": "viamo a casa", "explicacao": "Andare + a + la = andare a casa. Si usa A per destinazione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Preposizione articolata:\nLui _____ giardino (in + il)", "resposta": "è nel giardino", "explicacao": "Essere + in + il = essere nel giardino. Si usa IN per luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'behind the house' correttamente?", "opcoes": ["dietro la casa", "della casa", "alla casa"], "resposta": 0, "explicacao": "Dietro è preposizione semplice per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Preposizione articolata:\nLei _____ finestra (di + la)", "resposta": "parla della finestra", "explicacao": "Parlare + di + la = parlare della finestra. Si usa DI per tema."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Preposizione articolata:\nIo _____ porta (a + la)", "resposta": "vado alla porta", "explicacao": "Andare + a + la = andare alla porta. Si usa A per destinazione."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'dentro + il'? A:", "opcoes": ["dentro", "dello", "all"], "resposta": 0, "explicacao": "Dentro è preposizione semplice per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Preposizione articolata:\nNoi _____ stazione (in + la)", "resposta": "andiamo alla stazione", "explicacao": "Andare + in + la = andare alla stazione. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Preposizione articolata:\nLui _____ aeroporto (in + il)", "resposta": "è nell aeroporto", "explicacao": "Essere + in + l' = essere in aeroporto. Si usa IN per luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'above the tree' correttamente?", "opcoes": ["sopra l'albero", "dell albero", "alla albero"], "resposta": 0, "explicacao": "Sopra è preposizione semplice per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Preposizione articolata:\nLei _____ muro (di + il)", "resposta": "parla del muro", "explicacao": "Parlare + di + il = parlare del muro. Si usa DI per tema."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Preposizione articolata:\nIo _____ tetto (a + il)", "resposta": "vado al tetto", "explicacao": "Andare + su/col + il = andare al tetto. Si usa SU per posizione."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'vicino a + la'? A:", "opcoes": ["vicino", "vicina", "vicine"], "resposta": 0, "explicacao": "Vicino è preposizione semplice per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Preposizione articolata:\nNoi _____ lago (in + il)", "resposta": "andiamo al lago", "explicacao": "Andare + in/col + il = andare al lago. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Preposizione articolata:\nLui _____ fiume (in + il)", "resposta": "è nel fiume", "explicacao": "Essere + in + il = essere nel fiume. Si usa IN per luogo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'opposite the school' correttamente?", "opcoes": ["di fronte la scuola", "della scuola", "alla scuola"], "resposta": 0, "explicacao": "Di fronte è preposizione semplice per posizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Preposizione articolata:\nLei _____ giardino (in + il)", "resposta": "è nel giardino", "explicacao": "Essere + in + il = essere nel giardino. Si usa IN per luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Preposizione articolata:\nIo _____ piazza (in + la)", "resposta": "vado alla piazza", "explicacao": "Andare + in + la = andare alla piazza. Si usa IN per luogo."}
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
