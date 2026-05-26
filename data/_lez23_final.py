import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXIII"), None)
if lez is None:
    lez = {"id": "a1-lez23", "num": "Lezione XXIII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I verbi modali"
lez["subtitulo"] = "Potere, dovere, volere, sapere — usi e costruzioni"
lez["exemplos"] = [
    "Posso venire domani.",
    "Devo studiare per l'esame.",
    "Voglio imparare l'italiano.",
    "Sai cucinare la pasta?",
    "Non ho potuto dormire.",
    "Avrebbe dovuto chiamare prima."
]

lez["teoria"] = """<h3>I verbi modali</h3>
<p>I <strong>verbi modali</strong> (o servili) si usano insieme a un infinito per esprimere possibilità, obbligo, volontà o capacità. I principali sono: <strong>potere, dovere, volere, sapere</strong>.</p>

<h4>Coniugazione al presente indicativo</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="5">Verbi modali — presente indicativo</th>
  </tr>
  <tr>
    <th class="gram-art">Persona</th>
    <th class="gram-art">POTERE</th>
    <th class="gram-art">DOVERE</th>
    <th class="gram-art">VOLERE</th>
    <th class="gram-art">SAPERE</th>
  </tr>
  <tr><td>io</td><td>posso</td><td>devo</td><td>voglio</td><td>so</td></tr>
  <tr><td>tu</td><td>puoi</td><td>devi</td><td>vuoi</td><td>sai</td></tr>
  <tr><td>lui/lei</td><td>può</td><td>deve</td><td>vuole</td><td>sa</td></tr>
  <tr><td>noi</td><td>possiamo</td><td>dobbiamo</td><td>vogliamo</td><td>sappiamo</td></tr>
  <tr><td>voi</td><td>potete</td><td>dovete</td><td>volete</td><td>sapete</td></tr>
  <tr><td>loro</td><td>possono</td><td>devono</td><td>vogliono</td><td>sanno</td></tr>
</table>

<h4>Significati dei verbi modali</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Significati e usi</th>
  </tr>
  <tr>
    <th class="gram-art">Verbo</th>
    <th class="gram-art">Significato</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td><strong>POTERE</strong></td><td>possibilità, permesso</td><td><em>Posso uscire? / Puoi farlo domani.</em></td></tr>
  <tr><td><strong>DOVERE</strong></td><td>obbligo, necessità</td><td><em>Devo studiare. / Deve partire presto.</em></td></tr>
  <tr><td><strong>VOLERE</strong></td><td>volontà, desiderio</td><td><em>Voglio un caffè. / Vuole imparare.</em></td></tr>
  <tr><td><strong>SAPERE</strong></td><td>capacità (saper fare)</td><td><em>So nuotare. / Sai suonare la chitarra?</em></td></tr>
</table>

<h4>Tempi composti: quale ausiliare?</h4>
<p>Nei tempi composti, i modali prendono l'ausiliare del verbo che introducono:</p>
<ul>
  <li>Con verbi che vogliono <strong>AVERE</strong>: <em>Ho potuto mangiare. / Non ho voluto uscire.</em></li>
  <li>Con verbi che vogliono <strong>ESSERE</strong>: <em>Sono potuto andare. / Sono dovuto partire.</em></li>
</ul>
<p><strong>Nota:</strong> Quando il modale è usato da solo (senza infinito), si usa sempre AVERE: <em>Ho voluto. / Non ho potuto.</em></p>

<h4>Coniugazione all'imperfetto e al condizionale</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="5">Modali — imperfetto e condizionale presente</th>
  </tr>
  <tr>
    <th class="gram-art">Persona</th>
    <th class="gram-art">POTERE imp.</th>
    <th class="gram-art">DOVERE imp.</th>
    <th class="gram-art">POTERE cond.</th>
    <th class="gram-art">DOVERE cond.</th>
  </tr>
  <tr><td>io</td><td>potevo</td><td>dovevo</td><td>potrei</td><td>dovrei</td></tr>
  <tr><td>tu</td><td>potevi</td><td>dovevi</td><td>potresti</td><td>dovresti</td></tr>
  <tr><td>lui/lei</td><td>poteva</td><td>doveva</td><td>potrebbe</td><td>dovrebbe</td></tr>
  <tr><td>noi</td><td>potevamo</td><td>dovevamo</td><td>potremmo</td><td>dovremmo</td></tr>
  <tr><td>voi</td><td>potevate</td><td>dovevate</td><td>potreste</td><td>dovreste</td></tr>
  <tr><td>loro</td><td>potevano</td><td>dovevano</td><td>potrebbero</td><td>dovrebbero</td></tr>
</table>

<h4>Usi particolari del condizionale modale</h4>
<ul>
  <li><strong>Dovrebbe</strong> = probabilità: <em>Dovrebbero arrivare presto.</em></li>
  <li><strong>Potrebbe</strong> = possibilità educata: <em>Potresti aiutarmi?</em></li>
  <li><strong>Vorrei</strong> = desiderio cortese: <em>Vorrei un caffè, per favore.</em></li>
  <li><strong>Avrebbe dovuto</strong> = rimprovero: <em>Avresti dovuto studiare di più.</em></li>
</ul>

<h4>SAPERE vs CONOSCERE</h4>
<p><strong>Sapere</strong> = conoscere un fatto, saper fare qualcosa:<br>
<em>So che hai ragione. / So cucinare.</em></p>
<p><strong>Conoscere</strong> = essere in contatto con persone o luoghi:<br>
<em>Conosco Marco. / Conosco Roma.</em></p>

<h4>Dialogo: Problemi al lavoro</h4>
<p><strong>Luca:</strong> Non posso venire alla riunione, devo restare in ufficio.<br>
<strong>Sara:</strong> Ma dovresti esserci — è importante!<br>
<strong>Luca:</strong> Lo so, vorrei venire, ma non posso proprio.<br>
<strong>Sara:</strong> Almeno potresti chiamare durante la pausa?<br>
<strong>Luca:</strong> Sì, quello posso farlo. So che avrei dovuto avvisare prima.<br>
<strong>Sara:</strong> Va bene. La prossima volta, però, vuoi comunicarcelo in anticipo?</p>"""

lez["exercicios"] = [
    # --- REVELAR exercises ---
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Coniuga POTERE al presente:\nio ___, tu ___, lui ___, noi ___, voi ___, loro ___",
        "resposta": "posso, puoi, può, possiamo, potete, possono"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Coniuga DOVERE e VOLERE al presente:\nDOVERE: io ___, tu ___, lui ___, noi ___, voi ___, loro ___\nVOLERE: io ___, tu ___, lui ___, noi ___, voi ___, loro ___",
        "resposta": "DOVERE: devo, devi, deve, dobbiamo, dovete, devono\nVOLERE: voglio, vuoi, vuole, vogliamo, volete, vogliono"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Scegli l'ausiliare corretto al passato prossimo:\n1. Non ___ (potere) dormire. (mangiare → AVERE)\n2. ___ (dovere) partire presto. (partire → ESSERE)\n3. Non ___ (volere) uscire. (uscire → ESSERE)\n4. ___ (sapere) rispondere. (rispondere → AVERE)",
        "resposta": "1. ho potuto | 2. sono dovuto/a | 3. non sono voluto/a | 4. ho saputo"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Completa con il modale giusto (potere/dovere/volere/sapere):\n1. ___ nuotare molto bene. (capacità)\n2. ___ studiare per l'esame. (obbligo)\n3. ___ un caffè, per favore. (desiderio cortese — condizionale)\n4. ___ uscire stasera? (permesso)",
        "resposta": "1. So | 2. Devo | 3. Vorrei | 4. Posso"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Trasforma al condizionale presente:\n1. devo → ___\n2. posso → ___\n3. voglio → ___\n4. devi → ___\n5. può → ___",
        "resposta": "1. dovrei | 2. potrei | 3. vorrei | 4. dovresti | 5. potrebbe"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Usa il condizionale passato per esprimere rimprovero:\n1. Tu non hai studiato. → ___ studiare di più.\n2. Lei non ha chiamato. → ___ chiamare prima.\n3. Loro non sono arrivati in orario. → ___ arrivare in orario.",
        "resposta": "1. Avresti dovuto | 2. Avrebbe dovuto | 3. Avrebbero dovuto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — SAPERE o CONOSCERE?\n1. ___ (sap./conosc.) Marco da molti anni.\n2. ___ (sap./conosc.) parlare tre lingue.\n3. ___ (sap./conosc.) che sei in ritardo.\n4. ___ (sap./conosc.) Roma molto bene.",
        "resposta": "1. Conosco | 2. So | 3. So | 4. Conosco"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Forma frasi complete con i modali:\n1. tu / dovere / arrivare / presto → ___\n2. lei / potere / aiutarmi / domani? → ___\n3. noi / volere / imparare / l'italiano → ___\n4. lui / sapere / suonare / la chitarra → ___",
        "resposta": "1. Devi arrivare presto | 2. Può aiutarmi domani? | 3. Vogliamo imparare l'italiano | 4. Sa suonare la chitarra"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "___ venire alla festa stasera? (permesso educato)",
        "opcoes": ["Devo", "Voglio", "Posso", "So"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Loro ___ studiare molto per l'esame.",
        "opcoes": ["sanno", "possono", "devono", "vogliono"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ cucinare la pasta perfettamente. (capacità)",
        "opcoes": ["Posso", "So", "Voglio", "Devo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Non ho ___ dormire ieri notte.",
        "opcoes": ["dovuto", "voluto", "potuto", "saputo"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ un bicchiere d'acqua, per favore. (desiderio cortese)",
        "opcoes": ["Voglio", "Vorrei", "Devo", "Dovrò"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Avresti ___ chiamare prima! (rimprovero)",
        "opcoes": ["potuto", "dovuto", "voluto", "saputo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Voi ___ essere già partiti. (probabilità)",
        "opcoes": ["dovete", "dovreste", "dovrà", "dovevate"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Conosco / So Marco da dieci anni. Quale è corretto?",
        "opcoes": ["So", "Conosco", "entrambi", "nessuno dei due"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Sono ___ andare dal medico ieri.",
        "opcoes": ["potuto", "dovuto", "voluto", "saputo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il condizionale di VOLERE (io) è:",
        "opcoes": ["voglio", "volevo", "vorrei", "vorrò"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ aiutarmi a portare questi bagagli? (richiesta educata)",
        "opcoes": ["Devi", "Puoi", "Sai", "Vuoi"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Non ___ (volere) uscire ieri, avevo mal di testa. (passato — uscire vuole ESSERE)",
        "opcoes": ["ho voluto", "sono voluto/a", "volevo", "avevo voluto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "SAPERE si usa per indicare:",
        "opcoes": ["conoscere persone", "conoscere luoghi", "capacità o conoscenza di fatti", "solo stati d'animo"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ (loro) arrivare tra poco. (probabilità)",
        "opcoes": ["Devono", "Dovrebbero", "Devono essere", "Sanno"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il condizionale passato di DOVERE (io) è:",
        "opcoes": ["dovevo", "dovrei", "avrei dovuto", "sarei dovuto"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Ho ___ mangiare tutto perché avevo fame.",
        "opcoes": ["voluto", "dovuto", "potuto", "saputo"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "___ Roma bene — ci vivo da vent'anni.",
        "opcoes": ["So", "Conosco", "Sapevo", "Posso"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Non ___ (potere) partire — avevo perso il treno. (passato, partire → ESSERE)",
        "opcoes": ["ho potuto", "sono potuto/a", "potevo", "avevo potuto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il condizionale di POTERE (tu) è:",
        "opcoes": ["potevi", "puoi", "potresti", "potessi"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ che Marco è tornato? (conoscenza di un fatto)",
        "opcoes": ["Conosci", "Sai", "Puoi", "Vuoi"],
        "resposta": 1
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Io posso cucinare bene. (capacità) — è corretto?\n2. Ho sono potuto partire ieri.\n3. Vorrei un caffè — è corretto?\n4. Conosco che Marco è arrivato.\n5. Dovresti studiare di più — è corretto?",
        "resposta": "1. Meglio: So cucinare (capacità = sapere) | 2. Sono potuto partire | 3. SÌ, corretto | 4. So | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Non ho voluto uscire. (uscire → ESSERE) — è corretto?\n2. Lui devrebbe arrivare presto — è corretto?\n3. Avresti voluto andare — è corretto?\n4. So molto bene Roma.",
        "resposta": "1. Non sono voluto uscire | 2. SÌ, corretto | 3. SÌ, corretto | 4. Conosco molto bene Roma"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
