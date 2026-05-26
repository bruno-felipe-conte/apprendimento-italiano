import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XXI")

novos = [
    # 30 exercícios sobre La preposizione relativa
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Preposizione relativa:\nLa casa _____ vivo ha giardino.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). La casa dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Preposizione relativa:\nIl giorno _____ sono nato era bello.", "resposta": "quando", "explicacao": "Preposizione: in cui. Il giorno quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the house in which I live'? A:", "opcoes": ["casa vivo", "casa dove vivo", "casa nella"], "resposta": 1, "explicacao": "Casa dove vivo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Preposizione relativa:\nLa scuola _____ vado è grande.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). La scuola dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Preposizione relativa:\nIl momento _____ sono successo tutto.", "resposta": "quando", "explicacao": "Preposizione: in cui. Il momento quando."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the day when I was born'? A:", "opcoes": ["giorno sono nato", "giorno in cui sono nato", "giorno che"], "resposta": 1, "explicacao": "Giorno quando = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Preposizione relativa:\nIl ristorante _____ mangio è buono.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il ristorante dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Preposizione relativa:\nL'anno _____ sono nato era bello.", "resposta": "quando", "explicacao": "Preposizione: in cui. L'anno quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the place where I live'? A:", "opcoes": ["posto vivo", "posto dove vivo", "posto in"], "resposta": 1, "explicacao": "Posto dove vivo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Preposizione relativa:\nIl teatro _____ lavoro è bello.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il teatro dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Preposizione relativa:\nIl mese _____ sono arrivato era freddo.", "resposta": "quando", "explicacao": "Preposizione: in cui. Il mese quando."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the city in which he lives'? A:", "opcoes": ["città abita", "città dove abita", "città la"], "resposta": 1, "explicacao": "Città dove abita = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Preposizione relativa:\nIl museo _____ visito è interessante.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il museo dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Preposizione relativa:\nLa sera _____ sono nato era scura.", "resposta": "quando", "explicacao": "Preposizione: in cui. La sera quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the park where we play'? A:", "opcoes": ["parco giochiamo", "parco dove giochiamo", "parco al"], "resposta": 1, "explicacao": "Parco dove giochiamo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Preposizione relativa:\nIl negozio _____ lavoro è pieno.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il negozio dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Preposizione relativa:\nLa notte _____ sono nato era buia.", "resposta": "quando", "explicacao": "Preposizione: in cui. La notte quando."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the office in which he works'? A:", "opcoes": ["ufficio lavora", "ufficio dove lavora", "ufficio al"], "resposta": 1, "explicacao": "Ufficio dove lavora = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Preposizione relativa:\nIl parco _____ cammino è grande.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il parco dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Preposizione relativa:\nLa mattina _____ sono nato era bella.", "resposta": "quando", "explicacao": "Preposizione: in cui. La mattina quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the street where I live'? A:", "opcoes": ["strada vivo", "strada dove vivo", "strada in"], "resposta": 1, "explicacao": "Strada dove vivo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Preposizione relativa:\nIl campo _____ giochi è erboso.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il campo dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Preposizione relativa:\nLa domenica _____ sono nato era festa.", "resposta": "quando", "explicacao": "Preposizione: in cui. La domenica quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the room where she sleeps'? A:", "opcoes": ["stanza dorme", "stanza dove dorme", "stanza al"], "resposta": 1, "explicacao": "Stanza dove dorme = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Preposizione relativa:\nIl mare _____ vado è caldo.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il mare dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Preposizione relativa:\nLa primavera _____ mi piace è bella.", "resposta": "quando", "explicacao": "Preposizione: in cui. La primavera quando."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the garden in which we walk'? A:", "opcoes": ["giardino camminiamo", "giardino dove camminiamo", "giardino nel"], "resposta": 1, "explicacao": "Giardino dove camminiamo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Preposizione relativa:\nIl lago _____ vivo è bello.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il lago dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Preposizione relativa:\nL'estate _____ mi piace è bella.", "resposta": "quando", "explicacao": "Preposizione: in cui. L'estate quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the city where I live'? A:", "opcoes": ["città vivo", "città dove vivo", "città nella"], "resposta": 1, "explicacao": "Città dove vivo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Preposizione relativa:\nIl fiume _____ abito è grande.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il fiume dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Preposizione relativa:\nL'inverno _____ mi piace è freddo.", "resposta": "quando", "explicacao": "Preposizione: in cui. L'inverno quando."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the school where I studied'? A:", "opcoes": ["scuola studio", "scuola dove studio", "scuola al"], "resposta": 1, "explicacao": "Scuola dove studio = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Preposizione relativa:\nIl bosco _____ cammino è silenzioso.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il bosco dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Preposizione relativa:\nL'autunno _____ mi piace è bella.", "resposta": "quando", "explicacao": "Preposizione: in cui. L'autunno quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the house where I live'? A:", "opcoes": ["casa vivo", "casa dove vivo", "casa nella"], "resposta": 1, "explicacao": "Casa dove vivo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Preposizione relativa:\nIl giardino _____ lavoro è bello.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il giardino dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Preposizione relativa:\nLa stagione _____ preferisco è bella.", "resposta": "quando", "explicacao": "Preposizione: in cui. La stagione quando."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'the village where we live'? A:", "opcoes": ["villaggio viviamo", "villaggio dove viviamo", "villaggio nel"], "resposta": 1, "explicacao": "Villaggio dove viviamo = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Preposizione relativa:\nLa piazza _____ incontro è grande.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). La piazza dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Preposizione relativa:\nIl periodo _____ lavoro è bello.", "resposta": "quando", "explicacao": "Preposizione: in cui. Il periodo quando."},
    {"tipo": "escolha", "pergunta": "Come si dice 'the town where he works'? A:", "opcoes": ["città lavora", "città dove lavora", "città al"], "resposta": 1, "explicacao": "Città dove lavora = Relativa + preposizione."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Preposizione relativa:\nIl teatro _____ ando è bello.", "resposta": "dove", "explicacao": "Preposizione: dove (in cui). Il teatro dove."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Preposizione relativa:\nLa stagione _____ arrivo è bella.", "resposta": "quando", "explicacao": "Preposizione: in cui. La stagione quando."}
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
