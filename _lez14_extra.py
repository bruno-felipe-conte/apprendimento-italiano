import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XIV")

novos = [
    # 30 exercícios sobre I verbi modali
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Modale 'potere':\n_____ andare al cinema?", "resposta": "Posso", "explicacao": "Potere: posso + infinito. Io poso."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Modale 'potere':\n_____ venire con te?", "resposta": "Può", "explicacao": "Potere: può + infinito. Lui può."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'can you'? A:", "opcoes": ["puoi", "poti", "può"], "resposta": 0, "explicacao": "Puoi = Potere + infinito. Tu puoi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Modale 'dovere':\n_____ studiare per l'esame?", "resposta": "Devo", "explicacao": "Dovere: devo + infinito. Io devo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Modale 'dovere':\n_____ rispettare le regole?", "resposta": "Devono", "explicacao": "Dovere: devono + infinito. Loro devono."},
    {"tipo": "escolha", "pergunta": "Come si dice 'must you'? A:", "opcoes": ["devo", "devi", "può"], "resposta": 1, "explicacao": "Devi = Dovere + infinito. Tu devi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Modale 'volere':\n_____ comprare un'auto?", "resposta": "Vuole", "explicacao": "Volere: vuole + infinito. Lui vuole."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Modale 'volere':\n_____ mangiare sushi?", "resposta": "Vogliamo", "explicacao": "Volere: vogliamo + infinito. Noi vogliamo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they want'? A:", "opcoes": ["vogliono", "volete", "vuole"], "resposta": 0, "explicacao": "Vogliono = Volere + infinito. Loro vogliono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Modale 'dovere':\n_____ finire il compito?", "resposta": "Deve", "explicacao": "Dovere: deve + infinito. Lei deve."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Modale 'potere':\n_____ entrare ora?", "resposta": "Potete", "explicacao": "Potere: potete + infinito. Voi potete."},
    {"tipo": "escolha", "pergunta": "Come si dice 'we can'? A:", "opcoes": ["possiamo", "possono", "potrebbe"], "resposta": 0, "explicacao": "Possiamo = Potere + infinito. Noi possiamo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Modale 'dovere':\n_____ pagare le tasse?", "resposta": "Devi", "explicacao": "Dovere: devi + infinito. Tu devi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Modale 'volere':\n_____ imparare italiano?", "resposta": "Volevo", "explicacao": "Volere: volevo + infinito (passato). Io volevo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you can not'? A:", "opcoes": ["non posso", "può no", "deve no"], "resposta": 0, "explicacao": "Non posso = Non + potere. Negazione modale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Modale 'dovere':\n_____ prendere l'autobus?", "resposta": "Devono", "explicacao": "Dovere: devono + infinito. Loro devono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Modale 'volere':\n_____ comprare casa?", "resposta": "Vuole", "explicacao": "Volere: vuole + infinito. Lui vuole."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she wants'? A:", "opcoes": ["vuoi", "vuolo", "vuole"], "resposta": 2, "explicacao": "Vuole = Volere + infinito. Lei vuole."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Modale 'potere':\n_____ telefonare a mamma?", "resposta": "Posso", "explicacao": "Potere: posso + infinito. Io posso."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Modale 'dovere':\n_____ studiare molto?", "resposta": "Devi", "explicacao": "Dovere: devi + infinito. Tu devi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they can'? A:", "opcoes": ["possono", "posse", "potrebbe"], "resposta": 0, "explicacao": "Possono = Potere + infinito. Loro possono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Modale 'volere':\n_____ aiutare qualcuno?", "resposta": "Volete", "explicacao": "Volere: volete + infinito. Voi volete."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Modale 'potere':\n_____ vedere il film?", "resposta": "Puoi", "explicacao": "Potere: puoi + infinito. Tu puoi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they must'? A:", "opcoes": ["devono", "potranno", "possono"], "resposta": 0, "explicacao": "Devono = Dovere + infinito. Loro devono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Modale 'dovere':\n_____ lasciare la stanza?", "resposta": "Devo", "explicacao": "Dovere: devo + infinito. Io devo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Modale 'volere':\n_____ sapere la risposta?", "resposta": "Vuole", "explicacao": "Volere: vuole + infinito. Lui vuole."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'he will'? A:", "opcoes": ["sarà", "può", "deve"], "resposta": 0, "explicacao": "Sarà = Futuro semplice. Ma 'will' = futuro."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Modale 'potere':\n_____ uscire stasera?", "resposta": "Posso", "explicacao": "Potere: posso + infinito. Io posso."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Modale 'dovere':\n_____ arrivare in tempo?", "resposta": "Deve", "explicacao": "Dovere: deve + infinito. Lei deve."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they want to'? A:", "opcoes": ["vogliono", "volete", "vuole"], "resposta": 0, "explicacao": "Vogliono = Volere + infinito. Loro vogliono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Modale 'volere':\n_____ andare al mare?", "resposta": "Vuole", "explicacao": "Volere: vuole + infinito. Lui vuole."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Modale 'potere':\n_____ comprare i biglietti?", "resposta": "Posso", "explicacao": "Potere: posso + infinito. Io posso."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you must'? A:", "opcoes": ["devi", "puoi", "devo"], "resposta": 0, "explicacao": "Devi = Dovere + infinito. Tu devi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Modale 'dovere':\n_____ finire il lavoro?", "resposta": "Devi", "explicacao": "Dovere: devi + infinito. Tu devi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Modale 'volere':\n_____ imparare nuove lingue?", "resposta": "Volete", "explicacao": "Volere: volete + infinito. Voi volete."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she can'? A:", "opcoes": ["può", "vuolo", "vorrei"], "resposta": 0, "explicacao": "Può = Potere + infinito. Lei può."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Modale 'potere':\n_____ aiutare gli altri?", "resposta": "Puote", "explicacao": "Potere: può + infinito. Lui può."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Modale 'dovere':\n_____ rispettare i genitori?", "resposta": "Devo", "explicacao": "Dovere: devo + infinito. Io devo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he wants to'? A:", "opcoes": ["vuoto", "vuole", "vorrebbe"], "resposta": 1, "explicacao": "Vuole = Volere + infinito. Lui vuole."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Modale 'volere':\n_____ andare in Giappone?", "resposta": "Vogliono", "explicacao": "Volere: vogliono + infinito. Loro vogliono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Modale 'potere':\n_____ prendere una pausa?", "resposta": "Posso", "explicacao": "Potere: posso + infinito. Io posso."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they must not'? A:", "opcoes": ["non devono", "devono no", "possono"], "resposta": 0, "explicacao": "Non devono = Negazione modale. Loro non devono."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Modale 'dovere':\n_____ pulire la camera?", "resposta": "Devo", "explicacao": "Dovere: devo + infinito. Io devo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Modale 'volere':\n_____ cambiare lavoro?", "resposta": "Vuole", "explicacao": "Volere: vuole + infinito. Lui vuole."}
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
