import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXX"), None)
if lez is None:
    lez = {"id": "a1-lez30", "num": "Lezione XXX", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Ripasso generale"
lez["subtitulo"] = "Revisione di tutte le strutture grammaticali del corso"
lez["exemplos"] = [
    "Se avessi studiato di più, avrei parlato meglio.",
    "Glielo ho già detto tre volte!",
    "Benché sia stanco, continuerò a studiare.",
    "Ha detto che sarebbe venuto il giorno dopo.",
    "In Italia si mangia benissimo.",
    "Avendo finito il lavoro, siamo usciti a festeggiare."
]

lez["teoria"] = """<h3>Ripasso generale — Tutte le strutture del corso</h3>
<p>In questa lezione finale ripassiamo le <strong>strutture grammaticali fondamentali</strong> del corso, con un riepilogo sistematico di tutti gli argomenti studiati.</p>

<h4>1. I verbi — riepilogo dei tempi</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Tempi verbali — uso principale</th>
  </tr>
  <tr>
    <th class="gram-art">Tempo</th>
    <th class="gram-art">Uso</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td>Presente</td><td>azioni abituali, stati presenti, futuro vicino</td><td><em>Studio italiano.</em></td></tr>
  <tr><td>Passato prossimo</td><td>azioni passate con effetti nel presente</td><td><em>Ho studiato ieri.</em></td></tr>
  <tr><td>Imperfetto</td><td>azioni abituali nel passato, descrizioni</td><td><em>Studiavo ogni giorno.</em></td></tr>
  <tr><td>Passato remoto</td><td>azioni storiche, completamente concluse</td><td><em>Dante nacque nel 1265.</em></td></tr>
  <tr><td>Trapassato prossimo</td><td>azione anteriore a un'altra al passato</td><td><em>Avevo già mangiato.</em></td></tr>
  <tr><td>Futuro semplice</td><td>azioni future, ipotesi nel presente</td><td><em>Partirò domani.</em></td></tr>
  <tr><td>Condizionale presente</td><td>desideri, cortesia, ipotesi</td><td><em>Vorrei un caffè.</em></td></tr>
  <tr><td>Condizionale passato</td><td>ipotesi nel passato, rimprovero</td><td><em>Avrei studiato di più.</em></td></tr>
  <tr><td>Congiuntivo presente</td><td>opinioni, dubbi, desideri (pres./fut.)</td><td><em>Penso che venga.</em></td></tr>
  <tr><td>Congiuntivo imperfetto</td><td>opinioni, desideri (riferimento al passato)</td><td><em>Pensavo che venisse.</em></td></tr>
  <tr><td>Congiuntivo passato</td><td>anteriorità con frase principale al presente</td><td><em>Penso che sia venuto.</em></td></tr>
  <tr><td>Congiuntivo trapassato</td><td>anteriorità con frase principale al passato</td><td><em>Pensavo che fosse venuto.</em></td></tr>
</table>

<h4>2. I pronomi — riepilogo</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="5">Pronomi personali</th>
  </tr>
  <tr>
    <th class="gram-art">Persona</th>
    <th class="gram-art">Soggetto</th>
    <th class="gram-art">Diretto</th>
    <th class="gram-art">Indiretto</th>
    <th class="gram-art">Riflessivo</th>
  </tr>
  <tr><td>1a sing.</td><td>io</td><td>mi / me</td><td>mi / a me</td><td>mi</td></tr>
  <tr><td>2a sing.</td><td>tu</td><td>ti / te</td><td>ti / a te</td><td>ti</td></tr>
  <tr><td>3a sing. m.</td><td>lui</td><td>lo / l'</td><td>gli</td><td>si</td></tr>
  <tr><td>3a sing. f.</td><td>lei</td><td>la / l'</td><td>le</td><td>si</td></tr>
  <tr><td>1a plur.</td><td>noi</td><td>ci</td><td>ci</td><td>ci</td></tr>
  <tr><td>2a plur.</td><td>voi</td><td>vi</td><td>vi</td><td>vi</td></tr>
  <tr><td>3a plur.</td><td>loro</td><td>li / le</td><td>gli (loro)</td><td>si</td></tr>
</table>

<h4>3. Strutture fondamentali — riepilogo</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Strutture grammaticali chiave</th>
  </tr>
  <tr>
    <th class="gram-art">Struttura</th>
    <th class="gram-art">Schema / Esempio</th>
  </tr>
  <tr><td>Periodo ipotetico tipo 2</td><td>Se + cong. imp. → condizionale presente: <em>Se avessi tempo, verrei.</em></td></tr>
  <tr><td>Periodo ipotetico tipo 3</td><td>Se + cong. trap. → condizionale passato: <em>Se avessi studiato, avrei capito.</em></td></tr>
  <tr><td>Concordanza dei tempi</td><td>Pres. principale → cong. presente / passato; Pass. principale → cong. imp. / trap.</td></tr>
  <tr><td>Discorso indiretto</td><td>Presente → imperfetto; Futuro → condizionale passato; Imperativo → di + infinito</td></tr>
  <tr><td>Forma passiva</td><td>ESSERE/VENIRE/ANDARE + participio passato (+ da + agente)</td></tr>
  <tr><td>Gerundio</td><td>Presente (-ando/-endo): contemporaneità; Passato (avendo/essendo + p.p.): anteriorità</td></tr>
  <tr><td>Pronomi combinati</td><td>indiretto + diretto: me lo, te la, glielo, ce ne, ecc.</td></tr>
  <tr><td>SI passivante</td><td>Si + verbo 3a persona: <em>In Italia si mangia bene.</em></td></tr>
</table>

<h4>4. Congiunzioni principali e modi verbali</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Congiunzioni e modo verbale</th>
  </tr>
  <tr>
    <th class="gram-art">Tipo</th>
    <th class="gram-art">Congiunzioni</th>
    <th class="gram-art">Modo</th>
  </tr>
  <tr><td>Causale</td><td>perché, siccome, dato che</td><td>indicativo</td></tr>
  <tr><td>Temporale</td><td>quando, mentre, appena, dopo che</td><td>indicativo</td></tr>
  <tr><td>Prima che</td><td>prima che</td><td>congiuntivo</td></tr>
  <tr><td>Finale</td><td>affinché, perché (scopo), in modo che</td><td>congiuntivo</td></tr>
  <tr><td>Concessiva</td><td>benché, sebbene, nonostante che</td><td>congiuntivo</td></tr>
  <tr><td>Condizionale</td><td>se (tipo 2/3)</td><td>congiuntivo imp./trap.</td></tr>
</table>

<h4>5. Dialogo finale: Un anno di italiano</h4>
<p><strong>Professoressa:</strong> Allora, com'è andata quest'anno?<br>
<strong>Bruno:</strong> Benché all'inizio fosse difficile, adesso mi sento molto più sicuro.<br>
<strong>Professoressa:</strong> Ricordi le prime lezioni? Ti sembrava impossibile!<br>
<strong>Bruno:</strong> Sì! Se avessi saputo che era così complesso, avrei iniziato prima. Ma sono contento di aver perseverato.<br>
<strong>Professoressa:</strong> Lo sapevo che ce l'avresti fatta. Avendo studiato ogni giorno, hai fatto progressi enormi.<br>
<strong>Bruno:</strong> Glielo dico sinceramente: questo corso ha cambiato il mio modo di vedere la lingua.<br>
<strong>Professoressa:</strong> Perfetto. In Italia si dice: «Chi non risica, non rosica». Chi non rischia, non ottiene nulla.<br>
<strong>Bruno:</strong> Lo terrò a mente. Grazie di tutto!</p>"""

lez["exercicios"] = [
    # --- REVELAR: Ripasso generale ---
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 1 — Tempi verbali. Scegli il tempo corretto e spiega perché:\n1. Ieri ___ (andare) al cinema con Marco.\n2. Quando ero piccolo, ___ (giocare) in strada ogni giorno.\n3. Dante ___ (nascere) a Firenze nel 1265.\n4. Domani ___ (partire) per Milano.",
        "resposta": "1. sono andato (passato prossimo) | 2. giocavo (imperfetto: abitudine) | 3. nacque (passato remoto: fatto storico) | 4. partirò (futuro)"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 2 — Congiuntivo. Completa:\n1. Penso che lui ___ (essere) a casa.\n2. Credevo che lei ___ (venire) alla festa.\n3. È necessario che voi ___ (studiare).\n4. Speravo che loro ___ (finire) in tempo.",
        "resposta": "1. sia | 2. venisse | 3. studiate | 4. avessero finito / finissero"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 3 — Periodo ipotetico. Completa:\n1. Se ___ (avere) tempo, vengo da te. (tipo 1)\n2. Se ___ (sapere) la risposta, te la direi. (tipo 2)\n3. Se ___ (studiare) di più, avresti capito. (tipo 3)",
        "resposta": "1. ho | 2. sapessi | 3. avessi studiato"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 4 — Discorso indiretto. Trasforma:\n1. «Sono stanco.» → Ha detto che ___.\n2. «Vengo domani.» → Ha detto che ___.\n3. «Hai fame?» → Mi ha chiesto ___.\n4. «Studia!» → Mi ha detto ___.",
        "resposta": "1. era stanco | 2. sarebbe venuto il giorno dopo | 3. se avevo fame | 4. di studiare"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 5 — Pronomi combinati. Sostituisci:\n1. Ho dato il libro a lui. → ___\n2. Spiego la lezione a voi. → ___\n3. Ho portato i fiori a lei. → ___\n4. Mando il messaggio a te. → ___",
        "resposta": "1. Glielo ho dato | 2. Ve la spiego | 3. Gliele ho portate | 4. Te lo mando"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 6 — Forma passiva. Trasforma:\n1. Marco ha scritto il libro. → ___\n2. Il professore corregge i compiti ogni giorno. → ___ (venire)\n3. Questo modulo deve essere firmato. → ___ (andare)",
        "resposta": "1. Il libro è stato scritto da Marco | 2. I compiti vengono corretti ogni giorno dal professore | 3. Questo modulo va firmato"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 7 — Gerundio. Completa:\n1. ___ (studiare) ogni giorno, migliorerai.\n2. ___ (avere) finito, siamo usciti.\n3. Pur ___ (essere) stanco, ha lavorato.\n4. Stavo ___ (leggere) quando hai chiamato.",
        "resposta": "1. Studiando | 2. Avendo finito | 3. essendo | 4. leggendo"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso 8 — Mix finale. Correggi o conferma:\n1. Penso che lui è a casa.\n2. Se avrei tempo, verrei.\n3. In Italia si mangia molto bene — è corretto?\n4. Ho già detto glielo.\n5. Benché era stanco, ha lavorato.",
        "resposta": "1. sia | 2. avessi | 3. SÌ, corretto | 4. Glielo ho già detto | 5. fosse"
    },

    # --- ESCOLHA: Esercizi di verifica (ripasso) ---
    {
        "tipo": "escolha",
        "pergunta": "Quale tempo si usa per azioni abituali nel passato?",
        "opcoes": ["passato prossimo", "passato remoto", "imperfetto", "trapassato prossimo"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Penso che lui ___ a casa.\" (opinione, presente)",
        "opcoes": ["è", "sia", "era", "fosse"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Se ___ più soldi, comprerei una villa.\" (tipo 2)",
        "opcoes": ["ho", "avrei", "avessi", "avrò"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ha detto che ___ domani.\" (futuro → discorso indiretto)",
        "opcoes": ["verrà", "viene", "sarebbe venuto", "veniva"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ho dato la lettera a lui.\" → con pronomi:",
        "opcoes": ["Me la ho data", "Gliela ho data", "Gliel'ho data", "entrambe b e c"],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "La forma passiva con ANDARE esprime:",
        "opcoes": ["un'azione abituale", "un'azione nel futuro", "un obbligo", "una possibilità"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ (studiare) ogni giorno, imparerai l'italiano.\" (gerundio)",
        "opcoes": ["Studiato", "Studio", "Studiando", "Studiare"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Benché ___ tardi, continuiamo.\" (concessiva)",
        "opcoes": ["è", "sia", "era", "fosse"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"In questo ristorante ___ ottimi vini.\" (SI passivante)",
        "opcoes": ["si serve", "si servono", "si è servito", "si serva"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale pronome indiretto diventa GLI nei combinati?",
        "opcoes": ["mi", "ti", "gli/le", "vi"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Avrei ___ studiare di più.\" (rimprovero a me stesso)",
        "opcoes": ["potuto", "dovuto", "voluto", "saputo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Nel periodo ipotetico tipo 3, l'apodosi usa:",
        "opcoes": ["condizionale presente", "condizionale passato", "congiuntivo trapassato", "futuro anteriore"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Studio ___ (per/affinché) imparare.\" (stesso soggetto)",
        "opcoes": ["affinché", "per", "benché", "sebbene"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il participio passato con i pronomi combinati concorda con:",
        "opcoes": ["il soggetto", "il pronome indiretto", "il pronome diretto", "l'ausiliare"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Pensavo che Maria ___ già partita.\" (trapassato nel congiuntivo)",
        "opcoes": ["sia", "fosse", "è", "era"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale avverbio si posiziona tra ausiliare e participio?",
        "opcoes": ["lentamente", "già", "spesso", "abbastanza"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ la lettera, Marco è uscito.\" (proposizione participiale)",
        "opcoes": ["Leggendo", "Avendo letto", "Letta", "Legge"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non ho capito ___.\" (niente/nulla — doppia negazione)",
        "opcoes": ["qualcosa", "niente", "nessuno", "alcunché"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "La concordanza dei tempi: frase principale al passato → congiuntivo imperfetto per:",
        "opcoes": ["anteriorità", "contemporaneità / posteriorità", "solo per il futuro", "sempre"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale frase contiene UN SOLO ERRORE grammaticale?",
        "opcoes": [
            "Penso che lui è molto bravo.",
            "Se avessi tempo, verrei da te.",
            "Glielo ho dato ieri — è corretta?",
            "Studiando ogni giorno imparerai."
        ],
        "resposta": 0
    },

    # --- REVELAR: Trovare gli errori (ripasso finale) ---
    {
        "tipo": "revelar",
        "pergunta": "Ripasso finale — Trovare gli errori (5 frasi):\n1. Se verrei, ti aiuterei.\n2. Ha detto che viene domani. (futuro nel discorso indiretto)\n3. Benché fosse stanco, ha lavorato — è corretto?\n4. Ho dato glielo ieri.\n5. In Italia si mangia bene — è corretto?",
        "resposta": "1. venissi | 2. sarebbe venuto il giorno dopo | 3. SÌ, corretto | 4. Glielo ho dato | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Ripasso finale — Trovare gli errori (5 frasi):\n1. Studiando ogni giorno, il italiano migliora.\n2. Avendo finito, siamo usciti — è corretto?\n3. La lettera è stata scritta da il direttore.\n4. Penso che lui fosse a casa. (riferimento al presente)\n5. Gliela ho portate. (riferito a 'le rose')",
        "resposta": "1. l'italiano | 2. SÌ, corretto | 3. dal direttore | 4. sia (congiuntivo presente, riferimento presente) | 5. Gliele ho portate"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")

# Verificação final
print(f"\n{'='*50}")
print("VERIFICAÇÃO FINAL — Total de lezioni no módulo A1:")
lezioni = [u for u in modulo["unidades"]]
for l in lezioni:
    n_ex = len(l.get("exercicios", []))
    print(f"  {l['num']}: {l['titulo']} — {n_ex} exercícios")
print(f"\nTotal: {len(lezioni)} lezioni")
