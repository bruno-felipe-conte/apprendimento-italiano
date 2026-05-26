import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione IX")

novos = [
    # 30 esercizi sobre L'imperfetto indicativo
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Imperfetto regolare (-ARE):\nIo _____ (parlare) ieri?", "resposta": "parlavò", "explicacao": "-ARE: Io -avo. Io parlavo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Imperfetto regolare (-ARE):\nTu _____ (mangiare) ieri?", "resposta": "mangiavi", "explicacao": "-ARE: Tu -avi. Tu mangiavi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'he used to speak'? A:", "opcoes": ["parlava", "parlova", "parlerà"], "resposta": 0, "explicacao": "Parlava = Lui parlava. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Imperfetto regolare (-ARE):\nLei _____ (studiare) ieri?", "resposta": "studiavo", "explicacao": "-ARE: Lei -ava. Lei studiava."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Imperfetto regolare (-ARE):\nNoi _____ (lavorare) ieri?", "resposta": "lavoravamo", "explicacao": "-ARE: Noi -avamo. Noi lavoravamo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'you used to write' in italiano?", "opcoes": ["scrivevi", "scriveresti", "scrivete"], "resposta": 0, "explicacao": "Scrivevi = Tu scrivevi. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Imperfetto regolare (-ARE):\nVoi _____ (giocare) ieri?", "resposta": "giocavate", "explicacao": "-ARE: Voi -avate. Voi giocavate."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Imperfetto regolare (-ARE):\nLoro _____ (dormire) ieri?", "resposta": "dormivano", "explicacao": "-ARE: Loro -avano. Loro dormivano."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I used to eat'? A:", "opcoes": ["mangiavo", "mangerò", "mangio"], "resposta": 0, "explicacao": "Mangiavo = Io mangiavo. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Imperfetto irregolare:\nIo _____ (essere) da bambino?", "resposta": "ero", "explicacao": "ESSERE irregolare: ero. Io ero."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Imperfetto irregolare:\nTu _____ (avere) fame?", "resposta": "avevi", "explicacao": "AVERE irregolare: avevi. Tu avevi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she was'? A:", "opcoes": ["era", "è", "sarà"], "resposta": 0, "explicacao": "Era = Lei era. Imperfetto di essere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Imperfetto irregolare:\nLei _____ (fare) il lavoro?", "resposta": "faceva", "explicacao": "FARE irregolare: faceva. Lei faceva."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Imperfetto irregolare:\nNoi _____ (dire) una bugia?", "resposta": "dicevamo", "explicacao": "Dire irregolare: dicevamo. Noi dicevamo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they had'? A:", "opcoes": ["avevano", "avere", "ebbero"], "resposta": 0, "explicacao": "Avevano = Loro avevano. Imperfetto di avere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Imperfetto irregolare:\nVoi _____ (bere) il vino?", "resposta": "bevete", "explicacao": "-ERE irregolare: bevevate. Voi bevevate."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Imperfetto irregolare:\nLoro _____ (vedere) il film?", "resposta": "vedevano", "explicacao": "-ERE regolare: vedevano. Loro vedevano."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I was'? A:", "opcoes": ["ero", "era", "sarei"], "resposta": 0, "explicacao": "Ero = Io ero. Imperfetto di essere."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Passato prossimo vs imperfetto:\nIeri _____ film (azioni)", "resposta": "ho visto il film", "explicacao": "Passato prossimo = Azione completata. Ieri ho visto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Passato prossimo vs imperfetto:\nQuando _____ bambino (descrizione)", "resposta": "ero un bambino", "explicacao": "Imperfetto = Descrizione. Ero + descrizione."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I was happy'? A:", "opcoes": ["ero felice", "feci felice", "sarò felice"], "resposta": 0, "explicacao": "Ero felice = Io era felice. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Passato prossimo vs imperfetto:\nMentre _____ la TV (azione in corso)", "resposta": "guardavo", "explicacao": "Imperfetto = Azione in corso. Mentre + imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Passato prossimo vs imperfetto:\nQuando suonavano, _____ (azione)", "resposta": "suonavo", "explicacao": "Imperfetto = Azione in corso. Io suonavo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'while I was reading'? A:", "opcoes": ["mentre leggevo", "leggevo", "ho letto"], "resposta": 0, "explicacao": "Mentre leggevo = Mentre + imperfetto. Azione in corso."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Durante + sostantivo:\nDurante _____ (mangiare)", "resposta": "durante pranzo", "explicacao": "Durante + sostantivo. Durante il pranzo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Mentre + imperfetto:\nMentre _____ (parlare), arrivò", "resposta": "parlavò", "explicacao": "Mentre + imperfetto. Mentre parlavo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'he was working'? A:", "opcoes": ["lavorava", "lavoro", "ho lavorato"], "resposta": 0, "explicacao": "Lavorava = Lui lavorava. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Imperfetto di verbi regolari:\nTu _____ (finire) ieri?", "resposta": "finivi", "explicacao": "-IRE: Tu -ivi. Tu finivi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Imperfetto di verbi regolari:\nLei _____ (scendere) ieri?", "resposta": "scendeva", "explicacao": "-ERE: Lei -eva. Lei scendeva."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they used to go'? A:", "opcoes": ["andavano", "andarono", "andrano"], "resposta": 0, "explicacao": "Andavano = Loro andavano. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Imperfetto di verbi regolari:\nNoi _____ (scrivere) ieri?", "resposta": "scrivevamo", "explicacao": "-ERE: Noi -evamo. Noi scrivevamo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Imperfetto di verbi regolari:\nVoi _____ (venire) ieri?", "resposta": "venivate", "explicacao": "-IRE: Voi -ivate. Voi venivate."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I was tired'? A:", "opcoes": ["ero stanco", "stavo stanco", "sarò stanco"], "resposta": 0, "explicacao": "Ero stanco = Io ero stanco. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Imperfetto di verbi irregolari:\nTu _____ (andare) ieri sera?", "resposta": "andavi", "explicacao": "ANDARE irregolare: andavi. Tu andavi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Imperfetto di verbi irregolari:\nLoro _____ (dare) il regalo?", "resposta": "davano", "explicacao": "DARE irregolare: davano. Loro davano."},
    {"tipo": "escolha", "pergunta": "Come si dice 'she used to live'? A:", "opcoes": ["abitava", "abiterà", "abitò"], "resposta": 0, "explicacao": "Abitava = Lei abitava. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Imperfetto di verbi irregolari:\nNoi _____ (fare) l'esercizio?", "resposta": "facevamo", "explicacao": "FARE irregolare: facevamo. Noi facevamo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Imperfetto di verbi irregolari:\nLei _____ (dire) la verità?", "resposta": "diceva", "explicacao": "Dire irregolare: diceva. Lei diceva."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'I was going'? A:", "opcoes": ["andavo", "andai", "andrò"], "resposta": 0, "explicacao": "Andavo = Io andavo. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Descrizione di persona:\nEra un ragazzo _____ (alto)", "resposta": "ero alto", "explicacao": "Descrizione con imperfetto. Ero + aggettivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Abitudine con quando:\nQuando _____ bambino, _____ (giocare)", "resposta": "ero bambino, giocavo", "explicacao": "Abitudine con imperfetto. Ero + giocavo."},
    {"tipo": "escolha", "pergunta": "Come si dice 'he was sleeping'? A:", "opcoes": ["dormiva", "dorme", "dormì"], "resposta": 0, "explicacao": "Dormiva = Lui dormiva. Imperfetto."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Azione ripetuta:\nTutti i giorni _____ (andare) a scuola", "resposta": "andavo a scuola", "explicacao": "Abitudine con imperfetto. Andavo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Contesto temporale:\nNel _____ (vivere)", "resposta": "nel 1990 vivevo", "explicacao": "Tempo passato con imperfetto. Nel 1990 vivevo."}
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
