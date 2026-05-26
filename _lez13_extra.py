import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XIII")

novos = [
    # 30 exercícios sobre I pronomi relativi
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Pronome relativo 'che':\nQuesto è il libro _____ ho letto.", "resposta": "che", "explicacao": "Che = soggetto. Questo è il libro che ho letto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Pronome relativo 'che':\nLa ragazza _____ incontro ieri.", "resposta": "che", "explicacao": "Che = oggetto. La ragazza che incontro."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the house that I bought'? A:", "opcoes": ["casa ho comprato", "casa che ho comprato", "di casa ho comprato"], "resposta": 1, "explicacao": "Casa che ho comprato = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Pronome relativo 'che':\nLa città _____ vivo qui è grande.", "resposta": "dove", "explicacao": "Dove = luogo. La città dove vivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Pronome relativo 'che':\nIl giorno _____ sono nato era bello.", "resposta": "in cui", "explicacao": "In cui = tempo. Il giorno in cui sono nato."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the man who came'? A:", "opcoes": ["uomo venuto", "uomo che è venuto", "uomo di"], "resposta": 1, "explicacao": "Uomo che è venuto = Pronome relativo 'che' come soggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Pronome relativo 'dove':\nLa scuola _____ vado a piedi.", "resposta": "dove", "explicacao": "Dove = luogo. La scuola dove vado."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Pronome relativo 'quando':\nRicordo il momento _____ sono successo tutto.", "resposta": "quando", "explicacao": "Quando = tempo. Il momento quando sono successo tutto."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the place where I live'? A:", "opcoes": ["posto vivo", "posto dove vivo", "di posto vivo"], "resposta": 1, "explicacao": "Posto dove vivo = Pronome relativo 'dove' per luoghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Pronome relativo 'dove':\nLa casa _____ abito ha un giardino.", "resposta": "dove", "explicacao": "Dove = luogo. La casa dove abito."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Pronome relativo 'quando':\nIl anno _____ sono nato ho dieci anni.", "resposta": "in cui", "explicacao": "In cui = tempo. L'anno in cui sono nato."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the day that I met her'? A:", "opcoes": ["giorno incontro lei", "giorno che ho incontrato lei", "giorno a cui"], "resposta": 1, "explicacao": "Giorno che ho incontrato lei = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Pronome relativo 'dove':\nLa piazza _____ incontro è grande.", "resposta": "dove", "explicacao": "Dove = luogo. La piazza dove incontro."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Pronome relativo 'che':\nL'uomo _____ vedo è mio amico.", "resposta": "che", "explicacao": "Che = oggetto. L'uomo che vedo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the time when I left'? A:", "opcoes": ["quando sono partito", "tempo quando sono partito", "quando ho lasciato"], "resposta": 0, "explicacao": "Quando = tempo. Quando sono partito."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Pronome relativo 'che':\nIl film _____ ho visto ieri era ottimo.", "resposta": "che", "explicacao": "Che = oggetto. Il film che ho visto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Pronome relativo 'dove':\nLa strada _____ vivo è silenziosa.", "resposta": "dove", "explicacao": "Dove = luogo. La strada dove vivo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the person who helped me'? A:", "opcoes": ["persone aiutato", "persona che mi ha aiutato", "persona a cui"], "resposta": 1, "explicacao": "Persona che mi ha aiutato = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Pronome relativo 'dove':\nIl ristorante _____ mangio spesso è buono.", "resposta": "dove", "explicacao": "Dove = luogo. Il ristorante dove mangio."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Pronome relativo 'che':\nIl professore _____ insegno è intelligente.", "resposta": "che", "explicacao": "Che = oggetto. Il professore che insegno."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the car that I drive'? A:", "opcoes": ["auto conduco", "auto che conduzco", "della auto conduco"], "resposta": 1, "explicacao": "Auto che conduco = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Pronome relativo 'quando':\nHo dimenticato il giorno _____ sono arrivato.", "resposta": "quando", "explicacao": "Quando = tempo. Il giorno quando sono arrivato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Pronome relativo 'dove':\nIl museo _____ visito è interessante.", "resposta": "dove", "explicacao": "Dove = luogo. Il museo dove visito."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the place where we meet'? A:", "opcoes": ["posto ci vediamo", "posto dove ci vediamo", "della posto"], "resposta": 1, "explicacao": "Posto dove ci vediamo = Pronome relativo 'dove' per luoghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Pronome relativo 'che':\nLa macchina _____ uso è vecchia.", "resposta": "che", "explicacao": "Che = oggetto. La macchina che uso."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Pronome relativo 'dove':\nIl parco _____ cammino è grande.", "resposta": "dove", "explicacao": "Dove = luogo. Il parco dove cammino."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the book that I read'? A:", "opcoes": ["libro leggo", "libro che ho letto", "del libro"], "resposta": 1, "explicacao": "Libro che ho letto = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Pronome relativo 'dove':\nL'hotel _____ sto è lontano.", "resposta": "dove", "explicacao": "Dove = luogo. L'hotel dove sto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Pronome relativo 'che':\nLa lezione _____ ho dato era difficile.", "resposta": "che", "explicacao": "Che = oggetto. La lezione che ho dato."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the house which he owns'? A:", "opcoes": ["casa lui possiede", "casa che lui possiede", "della casa"], "resposta": 1, "explicacao": "Casa che lui possiede = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Pronome relativo 'quando':\nIl mese _____ sono partito era freddo.", "resposta": "quando", "explicacao": "Quando = tempo. Il mese quando sono partito."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Pronome relativo 'dove':\nIl negozio _____ lavoro è pieno.", "resposta": "dove", "explicacao": "Dove = luogo. Il negozio dove lavoro."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the day that he died'? A:", "opcoes": ["giorno morì", "giorno in cui morì", "del giorno"], "resposta": 1, "explicacao": "Giorno in cui morì = Pronome relativo 'in cui' per tempo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Pronome relativo 'che':\nIl regalo _____ ho ricevuto è bello.", "resposta": "che", "explicacao": "Che = oggetto. Il regalo che ho ricevuto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Pronome relativo 'dove':\nLa stazione _____ arrivo è grande.", "resposta": "dove", "explicacao": "Dove = luogo. La stazione dove arrivo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the year that I graduated'? A:", "opcoes": ["anno sono laureato", "anno in cui ho laurea", "dell'anno"], "resposta": 1, "explicacao": "Anno in cui ho laurea = Pronome relativo 'in cui' per tempo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Pronome relativo 'che':\nLa canzone _____ canto è famosa.", "resposta": "che", "explicacao": "Che = oggetto. La canzone che canto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Pronome relativo 'dove':\nIl campo _____ giochi è erboso.", "resposta": "dove", "explicacao": "Dove = luogo. Il campo dove giochi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the moment that I saw him'? A:", "opcoes": ["momento l'ho visto", "momento che ho visto", "del momento"], "resposta": 1, "explicacao": "Momento che ho visto = Pronome relativo 'che' come oggetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Pronome relativo 'quando':\nLa notte _____ sono nato era scura.", "resposta": "quando", "explicacao": "Quando = tempo. La notte quando sono nato."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Pronome relativo 'dove':\nIl mare _____ vado d'estate è caldo.", "resposta": "dove", "explicacao": "Dove = luogo. Il mare dove vado."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the place where she was born'? A:", "opcoes": ["posto è nata", "posto dove è nata", "del posto"], "resposta": 1, "explicacao": "Posto dove è nata = Pronome relativo 'dove' per luoghi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Pronome relativo 'che':\nIl problema _____ devo risolvere è difficile.", "resposta": "che", "explicacao": "Che = oggetto. Il problema che devo risolvere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Pronome relativo 'dove':\nIl paese _____ vivo ha un bel centro.", "resposta": "dove", "explicacao": "Dove = luogo. Il paese dove vivo."}
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
