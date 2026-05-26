import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VIII")

novos = [
    # 30 exercícios sobre I pronomi diretti
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Pronomi diretti atoni:\nIo ti _____ (vedere)", "resposta": "ti vedo", "explicacao": "Mi + vedo = Io ti vedo. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Pronomi diretti atoni:\nLui mi _____ (aiutare)", "resposta": "mi aiuta", "explicacao": "Mi = Io. Pronomi diretti dopo verbi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you see him'? A:", "opcoes": ["lo vedi", "ti lo vedono", "vi vedo"], "resposta": 0, "explicacao": "Lo vedi = Tu + lo (lui) vedi. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Pronomi diretti atoni:\nLei lo _____ (conosco)", "resposta": "lo conosce", "explicacao": "Lo = Lui. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Pronomi diretti atoni:\nNoi vi _____ (incontrare)", "resposta": "vi incontriamo", "explicacao": "Vi = Voi. Pronomi diretti dopo verbi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they see her'? A:", "opcoes": ["la vedono", "lo vedono", "ci vedono"], "resposta": 0, "explicacao": "La vedono = Loro + la (lei) vedono. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Pronomi diretti atoni:\nTu mi _____ (chiamare)", "resposta": "mi chiami", "explicacao": "Mi = Io. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Pronomi diretti atoni:\nEssi ci _____ (vedere)", "resposta": "ci vedono", "explicacao": "Ci = Noi. Pronomi diretti dopo verbi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she sees me'? A:", "opcoes": ["mi vede", "ti vede", "ci vede"], "resposta": 0, "explicacao": "Mi vede = Lei + mi (io) vede. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Pronomi diretti atoni:\nVoi lo _____ (amare)", "resposta": "lo amate", "explicacao": "Lo = Lui. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Pronomi diretti atoni:\nLoro le _____ (vedere)", "resposta": "le vedono", "explicacao": "Le = Loro (femminile). Pronomi diretti dopo verbi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I see her'? A:", "opcoes": ["la vedo", "ti vedo", "lo vedo"], "resposta": 0, "explicacao": "La vedo = Io + la (lei) vedo. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Pronomi diretti atoni:\nTu mi _____ (incontrare)", "resposta": "mi incontriamo", "explicacao": "Mi = Io. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Pronomi diretti atoni:\nLei lo _____ (comprare)", "resposta": "lo compra", "explicacao": "Lo = Lui. Pronomi diretti dopo verbi."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you see them'? A:", "opcoes": ["li vedi", "le vedi", "la vedi"], "resposta": 0, "explicacao": "Li vedi = Tu + li (loro) vedi. Pronomi diretti dopo verbi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Passato prossimo con pronomi:\nIo _____ visto (avere + part.)", "resposta": "ho veduto", "explicacao": "Ho veduto = Ho + veduto. Pronomi dopo participio."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Passato prossimo con pronomi:\nTu _____ parlato (avere + part.)", "resposta": "hai parlato", "explicacao": "Hai parlato = Hai + parlato. Pronomi dopo participio."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I have seen you'? A:", "opcoes": ["ti ho visto", "ho visto te", "l'ho visto"], "resposta": 0, "explicacao": "Ti ho visto = Io + ti (te) ho visto. Pronomi dopo verbo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Passato prossimo con pronomi:\nLei _____ detto (avere + part.)", "resposta": "ha detto", "explicacao": "Ha detto = Ha + detto. Pronomi dopo participio."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Passato prossimo con pronomi:\nNoi _____ mangiato (avere + part.)", "resposta": "abbiamo mangiato", "explicacao": "Abbiamo mangiato = Abbiamo + mangiato. Pronomi dopo participio."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'she has seen him'? A:", "opcoes": ["lo ha visto", "la ha visto", "l'ha vista"], "resposta": 0, "explicacao": "Lo ha visto = Lei + lo (lui) ha visto. Passato prossimo con pronomi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Passato prossimo con pronomi:\nVoi _____ scritto (avere + part.)", "resposta": "avete scritto", "explicacao": "Avete scritto = Avete + scritto. Pronomi dopo participio."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Passato prossimo con pronomi:\nLoro _____ letto (avere + part.)", "resposta": "hanno letto", "explicacao": "Hanno letto = Hanno + letto. Pronomi dopo participio."},
    {"tipo": "escolha", "pergunta": "Come si dice 'they have seen us'? A:", "opcoes": ["ci hanno visto", "ci vedono", "visti ci"], "resposta": 0, "explicacao": "Ci hanno visto = Loro + ci (noi) hanno visto. Passato prossimo con pronomi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Pronome LO:\nIo _____ libro (prendere il libro)", "resposta": "prendo il libro", "explicacao": "Prendere il libro = Prendere + lo. Uso di LO."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Pronome LA:\nLei _____ penna (prendere la penna)", "resposta": "prende la penna", "explicacao": "Prendere la penna = Prendere + la. Uso di LA."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'take it'? A:", "opcoes": ["lo prendo", "la prendo", "ci prendi"], "resposta": 0, "explicacao": "Lo prendo = Io + lo (lavoro/oggetto). Uso di LO."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Pronome LI:\nNoi _____ amici (vedere gli amici)", "resposta": "vediamo gli amici", "explicacao": "Vedere gli amici = Vedere + li. Uso di LI."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Pronome LE:\nEssi _____ sorelle (vedere le sorelle)", "resposta": "vedono le sorelle", "explicacao": "Vedere le sorelle = Vedere + le. Uso di LE."},
    {"tipo": "escolha", "pergunta": "Come si dice 'see them' (masc)? A:", "opcoes": ["li vedo", "le vedo", "lo vedo"], "resposta": 0, "explicacao": "Li vedo = Io + li (loro) vedo. Uso di LI."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Pronome CI:\nNoi _____ casa (andare a casa)", "resposta": "viamo a casa", "explicacao": "Andare a casa = Andare + ci. Uso di CI."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Pronome VI:\nLoro _____ amici (andare agli amici)", "resposta": "vanno agli amici", "explicacao": "Andare agli amici = Andare + vi. Uso di VI."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'come here'? A:", "opcoes": ["venite qui", "ci venite", "vi venite"], "resposta": 0, "explicacao": "Venite qui = Venite + ci. Uso di CI."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Ne (quantità):\nHo _____ (mangiare ne)", "resposta": "ne mangio", "explicacao": "Mangiare ne = Mangiare + en. Uso di NE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Ne (quantità):\nLei _____ (bere ne)", "resposta": "ne beve", "explicacao": "Bere ne = Bere + en. Uso di NE."},
    {"tipo": "escolha", "pergunta": "Come si dice 'I eat some'? A:", "opcoes": ["ne mangio", "mangio alcuni", "lo mangio"], "resposta": 0, "explicacao": "Ne mangio = Io + en (alcuni) mangio. Uso di NE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Ne (quantità):\nVoi _____ (fare ne)", "resposta": "ne fate", "explicacao": "Fare ne = Fare + en. Uso di NE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Ne (quantità):\nLoro _____ (prendere ne)", "resposta": "ne prendono", "explicacao": "Prendere ne = Prendere + en. Uso di NE."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'they take some'? A:", "opcoes": ["ne prendono", "prendono alcuni", "lo prendono"], "resposta": 0, "explicacao": "Ne prendono = Loro + en (alcuni) prendono. Uso di NE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Posizione del pronome:\nPosso _____ fare (lo posso fare)", "resposta": "lo posso fare", "explicacao": "Lo posso fare = Lo + posso fare. Pronomi prima verbi ausiliari."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Posizione del pronome:\nPuoi _____ vedere (lo puoi vedere)", "resposta": "lo puoi vedere", "explicacao": "Lo puoi vedere = Lo + puoi vedere. Pronomi prima verbi ausiliari."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'you can see him'? A:", "opcoes": ["puoi vederlo", "lo puoi vedere", "vedi lui"], "resposta": 1, "explicacao": "Lo puoi vedere = Lo + puoi vedere. Pronomi prima verbi ausiliari."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Posizione del pronome:\nPosso _____ aiutare (lo posso aiutare)", "resposta": "lo posso aiutare", "explicacao": "Lo posso aiutare = Lo + posso aiutare. Pronomi prima verbi ausiliari."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Posizione del pronome:\nLei _____ comprare (la può comprare)", "resposta": "può comprarla", "explicacao": "Può comprarla = Può + la comprare. Pronomi dopo verbo principale."}
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
