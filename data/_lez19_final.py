import json, re

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XIX"), None)
if lez is None:
    lez = {"id": "a1-lez19", "num": "Lezione XIX", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "La concordanza dei tempi"
lez["subtitulo"] = "Indicativo e congiuntivo nelle frasi dipendenti"
lez["exemplos"] = [
    "Penso che lui abbia ragione.",
    "Credevo che lei fosse stanca.",
    "Spero che tu possa venire.",
    "Pensavo che fossero partiti.",
    "È necessario che tu studi.",
    "Era importante che lui sapesse la verità."
]

lez["teoria"] = """<h3>La concordanza dei tempi</h3>
<p>La <strong>concordanza dei tempi</strong> è la corrispondenza tra il tempo della frase principale e il tempo della frase dipendente (subordinata). In italiano, il modo più usato nelle frasi dipendenti è il <strong>congiuntivo</strong>.</p>

<h4>Schema principale</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Frase principale (indicativo)</th>
    <th class="gram-genere" colspan="2">Frase dipendente (congiuntivo)</th>
  </tr>
  <tr>
    <th class="gram-art">Tempo</th>
    <th class="gram-art">Esempio</th>
    <th class="gram-art">Contemporaneità / Posteriorità</th>
    <th class="gram-art">Anteriorità</th>
  </tr>
  <tr>
    <td>Presente / Futuro</td>
    <td><em>Penso / Penserò che...</em></td>
    <td>Congiuntivo <strong>presente</strong><br><em>...che venga</em></td>
    <td>Congiuntivo <strong>passato</strong><br><em>...che sia venuto</em></td>
  </tr>
  <tr>
    <td>Passato / Imperfetto / Condizionale</td>
    <td><em>Pensavo / Ho pensato / Penserei che...</em></td>
    <td>Congiuntivo <strong>imperfetto</strong><br><em>...che venisse</em></td>
    <td>Congiuntivo <strong>trapassato</strong><br><em>...che fosse venuto</em></td>
  </tr>
</table>

<h4>Contemporaneità e posteriorità (azioni simultanee o future)</h4>
<p>Quando l'azione della frase dipendente è <strong>contemporanea o successiva</strong> a quella della principale:</p>
<ul>
  <li>Se la principale è al <strong>presente/futuro</strong> → congiuntivo <strong>presente</strong>:<br>
  <em>Credo che Paolo <strong>sia</strong> a casa.</em></li>
  <li>Se la principale è al <strong>passato/condizionale</strong> → congiuntivo <strong>imperfetto</strong>:<br>
  <em>Credevo che Paolo <strong>fosse</strong> a casa.</em></li>
</ul>

<h4>Anteriorità (azione già accaduta)</h4>
<p>Quando l'azione della frase dipendente è <strong>precedente</strong> a quella della principale:</p>
<ul>
  <li>Se la principale è al <strong>presente/futuro</strong> → congiuntivo <strong>passato</strong>:<br>
  <em>Penso che Paolo <strong>sia andato</strong> via.</em></li>
  <li>Se la principale è al <strong>passato/condizionale</strong> → congiuntivo <strong>trapassato</strong>:<br>
  <em>Pensavo che Paolo <strong>fosse andato</strong> via.</em></li>
</ul>

<h4>Il congiuntivo presente</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Congiuntivo presente — verbi regolari</th>
  </tr>
  <tr>
    <th class="gram-art">Persona</th>
    <th class="gram-art">-ARE (parlare)</th>
    <th class="gram-art">-ERE (vedere)</th>
    <th class="gram-art">-IRE (sentire)</th>
  </tr>
  <tr><td>io</td><td>parli</td><td>veda</td><td>senta</td></tr>
  <tr><td>tu</td><td>parli</td><td>veda</td><td>senta</td></tr>
  <tr><td>lui/lei</td><td>parli</td><td>veda</td><td>senta</td></tr>
  <tr><td>noi</td><td>parliamo</td><td>vediamo</td><td>sentiamo</td></tr>
  <tr><td>voi</td><td>parliate</td><td>vediate</td><td>sentiate</td></tr>
  <tr><td>loro</td><td>parlino</td><td>vedano</td><td>sentano</td></tr>
</table>

<h4>Il congiuntivo imperfetto</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Congiuntivo imperfetto — verbi regolari</th>
  </tr>
  <tr>
    <th class="gram-art">Persona</th>
    <th class="gram-art">-ARE (parlare)</th>
    <th class="gram-art">-ERE (vedere)</th>
    <th class="gram-art">-IRE (sentire)</th>
  </tr>
  <tr><td>io</td><td>parlassi</td><td>vedessi</td><td>sentissi</td></tr>
  <tr><td>tu</td><td>parlassi</td><td>vedessi</td><td>sentissi</td></tr>
  <tr><td>lui/lei</td><td>parlasse</td><td>vedesse</td><td>sentisse</td></tr>
  <tr><td>noi</td><td>parlassimo</td><td>vedessimo</td><td>sentissimo</td></tr>
  <tr><td>voi</td><td>parlaste</td><td>vedeste</td><td>sentiste</td></tr>
  <tr><td>loro</td><td>parlassero</td><td>vedessero</td><td>sentissero</td></tr>
</table>

<h4>Congiuntivi irregolari comuni</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="6">Congiuntivo presente — verbi irregolari</th>
  </tr>
  <tr>
    <th class="gram-art">Persona</th>
    <th class="gram-art">essere</th>
    <th class="gram-art">avere</th>
    <th class="gram-art">fare</th>
    <th class="gram-art">andare</th>
    <th class="gram-art">venire</th>
  </tr>
  <tr><td>io</td><td>sia</td><td>abbia</td><td>faccia</td><td>vada</td><td>venga</td></tr>
  <tr><td>tu</td><td>sia</td><td>abbia</td><td>faccia</td><td>vada</td><td>venga</td></tr>
  <tr><td>lui/lei</td><td>sia</td><td>abbia</td><td>faccia</td><td>vada</td><td>venga</td></tr>
  <tr><td>noi</td><td>siamo</td><td>abbiamo</td><td>facciamo</td><td>andiamo</td><td>veniamo</td></tr>
  <tr><td>voi</td><td>siate</td><td>abbiate</td><td>facciate</td><td>andiate</td><td>veniate</td></tr>
  <tr><td>loro</td><td>siano</td><td>abbiano</td><td>facciano</td><td>vadano</td><td>vengano</td></tr>
</table>

<h4>Verbi che reggono il congiuntivo</h4>
<p>Il congiuntivo si usa obbligatoriamente dopo certe espressioni:</p>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Espressioni + congiuntivo</th>
  </tr>
  <tr>
    <th class="gram-art">Tipo</th>
    <th class="gram-art">Esempi</th>
  </tr>
  <tr><td>Verbi di opinione</td><td>pensare, credere, ritenere, supporre</td></tr>
  <tr><td>Verbi di speranza/desiderio</td><td>sperare, desiderare, volere, preferire</td></tr>
  <tr><td>Verbi di dubbio/timore</td><td>dubitare, temere, avere paura</td></tr>
  <tr><td>Espressioni impersonali</td><td>è necessario, è importante, è possibile, bisogna</td></tr>
  <tr><td>Congiunzioni</td><td>benché, sebbene, affinché, prima che, a meno che</td></tr>
</table>

<h4>Dialogo: Un incidente</h4>
<p><strong>Marco:</strong> Hai sentito? Dicono che ci sia stato un incidente in via Roma.<br>
<strong>Sofia:</strong> Sì, pensavo che fosse già tutto a posto. Non sapevo che la strada fosse ancora chiusa.<br>
<strong>Marco:</strong> Mi auguro che nessuno si sia fatto male.<br>
<strong>Sofia:</strong> Anch'io. Credevo che la polizia avesse già risolto tutto.<br>
<strong>Marco:</strong> Bisogna che aspettiamo. Prima che arrivino i soccorsi, non possono riaprire.<br>
<strong>Sofia:</strong> Spero che domani la situazione sia tornata alla normalità.</p>"""

lez["exercicios"] = [
    # --- REVELAR exercises (book exercises) ---
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Completa con il congiuntivo presente di ESSERE o AVERE:\n1. Penso che lui ___ (essere) a casa.\n2. Credo che lei ___ (avere) fame.\n3. Spero che loro ___ (essere) pronti.\n4. È possibile che Marco ___ (avere) ragione.\n5. Suppongo che tu ___ (essere) stanco.",
        "resposta": "1. sia | 2. abbia | 3. siano | 4. abbia | 5. sia"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Trasforma al passato (imperfetto → congiuntivo imperfetto):\n1. Penso che venga. → Pensavo che ___.\n2. Credo che abbia fame. → Credevo che ___.\n3. Spero che partano. → Speravo che ___.\n4. È necessario che studi. → Era necessario che ___.",
        "resposta": "1. venisse | 2. avesse fame | 3. partissero | 4. studiasse"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Scegli il tempo corretto del congiuntivo:\n1. Penso che ieri Paolo ___ (andare) al cinema.\n2. Credevo che stamattina lei ___ (uscire) presto.\n3. Spero che domani tu ___ (potere) venire.\n4. Pensavo che il treno ___ (partire) già.",
        "resposta": "1. sia andato | 2. fosse uscita | 3. possa | 4. fosse già partito"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Completa con il verbo corretto al congiuntivo presente:\n1. È importante che voi ___ (arrivare) in orario.\n2. Bisogna che noi ___ (parlare) con il direttore.\n3. È possibile che loro ___ (venire) domani.\n4. Voglio che tu ___ (studiare) di più.\n5. Preferisco che lui ___ (sapere) la verità.",
        "resposta": "1. arriviate | 2. parliamo | 3. vengano | 4. studi | 5. sappia"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Completa con il congiuntivo imperfetto:\n1. Volevo che tu ___ (venire) alla festa.\n2. Era necessario che loro ___ (partire) subito.\n3. Pensavo che lui ___ (avere) più esperienza.\n4. Speravo che voi ___ (capire) la situazione.\n5. Credevo che lei ___ (essere) più simpatica.",
        "resposta": "1. venissi | 2. partissero | 3. avesse | 4. capiste | 5. fosse"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Completa con il congiuntivo passato:\n1. Penso che Marco ___ (andare) a Roma.\n2. Credo che loro ___ (finire) il lavoro.\n3. Spero che tu ___ (dormire) bene.\n4. È possibile che lei ___ (partire) ieri.",
        "resposta": "1. sia andato | 2. abbiano finito | 3. tu abbia dormito | 4. sia partita"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Completa con il congiuntivo trapassato:\n1. Pensavo che lui ___ (partire) il giorno prima.\n2. Credevo che voi ___ (vedere) quel film.\n3. Speravo che lei ___ (finire) in tempo.\n4. Temevo che loro ___ (dimenticare) l'appuntamento.",
        "resposta": "1. fosse partito | 2. aveste visto | 3. avesse finito | 4. avessero dimenticato"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Collega le frasi con la concordanza corretta:\n1. So che lui (avere) molto da fare domani.\n2. Sapevo che lei (essere) molto stanca ieri.\n3. Penso che noi (dovere) partire subito.\n4. Pensavo che Marco già (tornare) quando ho chiamato.",
        "resposta": "1. avrà | 2. era / fosse | 3. dobbiamo / dobbiate | 4. fosse già tornato"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "Penso che lei ___ molto intelligente.",
        "opcoes": ["è", "sia", "era", "fosse"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Credevo che loro ___ già partiti.",
        "opcoes": ["sono", "siano", "fossero", "erano"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "È necessario che tu ___ subito.",
        "opcoes": ["vieni", "venga", "venissi", "venuto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Speravo che Marco ___ alla festa.",
        "opcoes": ["venisse", "venga", "viene", "è venuto"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Penso che ieri lui ___ a Milano.",
        "opcoes": ["vada", "andasse", "sia andato", "andò"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Pensavo che lei ___ già mangiato quando sono arrivato.",
        "opcoes": ["abbia", "aveva", "avesse", "ha"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "È possibile che domani ___ bel tempo.",
        "opcoes": ["fa", "faccia", "facesse", "fece"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Benché ___ stanco, ha continuato a lavorare.",
        "opcoes": ["era", "è", "fosse", "sia"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Voglio che tu ___ la verità.",
        "opcoes": ["dici", "dicessi", "dica", "dire"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Temevo che il treno ___ già.",
        "opcoes": ["parta", "partisse", "sia partito", "fosse partito"],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "Affinché tu ___ capire, spiegherò ancora.",
        "opcoes": ["puoi", "possa", "potessi", "potuto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Preferisco che voi ___ con noi.",
        "opcoes": ["venite", "veniate", "veniste", "verrete"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Prima che lui ___, dobbiamo parlare.",
        "opcoes": ["parte", "parta", "partisse", "partirà"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Credevo che lei ___ la risposta.",
        "opcoes": ["sappia", "sapesse", "sa", "sapeva"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "È strano che loro non ___ ancora.",
        "opcoes": ["arrivino", "arrivassero", "arrivano", "sono arrivati"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Dubitavo che lui ___ la verità.",
        "opcoes": ["dica", "dicesse", "dice", "dirà"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Spero che voi ___ bene l'esame.",
        "opcoes": ["fate", "facciate", "faceste", "avete fatto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Sebbene ___ tardi, hanno continuato la riunione.",
        "opcoes": ["era", "fosse", "è", "sia"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Pensavo che Marco ___ già ___ quando siamo arrivati.",
        "opcoes": ["abbia mangiato", "aveva mangiato", "avesse mangiato", "mangiasse"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "È importante che tutti ___ la riunione.",
        "opcoes": ["vengono", "vengano", "venissero", "venuto"],
        "resposta": 1
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Penso che lui è molto bravo.\n2. Credevo che lei venga ieri.\n3. È necessario che tu studierai.\n4. Speravo che Marco vada alla festa.\n5. Prima che lei parte, voglio salutarla.",
        "resposta": "1. sia | 2. fosse venuta | 3. studi | 4. andasse | 5. parta"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Benché era stanco, ha lavorato.\n2. Pensavo che loro arrivano domani.\n3. Volevo che tu venuto con me.\n4. È possibile che ieri lui è andato.\n5. Affinché capisce, parla lentamente.",
        "resposta": "1. fosse | 2. arrivassero | 3. venissi | 4. sia andato | 5. capisca"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
