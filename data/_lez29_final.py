import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXIX"), None)
if lez is None:
    lez = {"id": "a1-lez29", "num": "Lezione XXIX", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Gli avverbi"
lez["subtitulo"] = "Avverbi di modo, tempo, luogo, quantità e frequenza"
lez["exemplos"] = [
    "Parla lentamente, per favore.",
    "Oggi non ho voglia di uscire.",
    "Abito qui da tre anni.",
    "Ho mangiato troppo.",
    "Va spesso al cinema.",
    "È arrivato tardi, quindi ha perso il treno."
]

lez["teoria"] = """<h3>Gli avverbi</h3>
<p>Gli <strong>avverbi</strong> modificano il significato di un verbo, di un aggettivo o di un altro avverbio. Sono <strong>invariabili</strong> (non cambiano per genere e numero).</p>

<h4>Avverbi di modo</h4>
<p>Indicano <strong>come</strong> si svolge un'azione. Molti si formano aggiungendo <strong>-mente</strong> all'aggettivo:</p>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Formazione avverbi in -MENTE</th>
  </tr>
  <tr>
    <th class="gram-art">Aggettivo</th>
    <th class="gram-art">Regola</th>
    <th class="gram-art">Avverbio</th>
  </tr>
  <tr><td>lento/a</td><td>forma femminile + -mente</td><td>lentamente</td></tr>
  <tr><td>rapido/a</td><td>forma femminile + -mente</td><td>rapidamente</td></tr>
  <tr><td>facile</td><td>agg. in -le/-re: si elide la -e</td><td>facilmente</td></tr>
  <tr><td>regolare</td><td>agg. in -re: si elide la -e</td><td>regolarmente</td></tr>
  <tr><td>felice</td><td>forma femminile (=maschile) + -mente</td><td>felicemente</td></tr>
</table>
<p>Avverbi di modo irregolari o speciali: <em>bene, male, così, insieme, volentieri, piano</em></p>

<h4>Avverbi di tempo</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Avverbi di tempo</th>
  </tr>
  <tr>
    <th class="gram-art">Avverbio</th>
    <th class="gram-art">Significato / Esempio</th>
  </tr>
  <tr><td>oggi</td><td>Oggi non lavoro.</td></tr>
  <tr><td>ieri</td><td>Ieri sono andato al cinema.</td></tr>
  <tr><td>domani</td><td>Domani partirò.</td></tr>
  <tr><td>adesso / ora</td><td>Adesso sto studiando.</td></tr>
  <tr><td>presto</td><td>Arriva sempre presto.</td></tr>
  <tr><td>tardi</td><td>È arrivato tardi.</td></tr>
  <tr><td>già</td><td>Ho già mangiato.</td></tr>
  <tr><td>ancora</td><td>Non ho ancora finito.</td></tr>
  <tr><td>poi / dopo</td><td>Prima mangio, poi esco.</td></tr>
  <tr><td>subito</td><td>Vieni subito!</td></tr>
  <tr><td>sempre</td><td>Arriva sempre in ritardo.</td></tr>
  <tr><td>mai</td><td>Non sono mai stato a Tokyo.</td></tr>
</table>

<h4>Avverbi di luogo</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Avverbi di luogo</th>
  </tr>
  <tr>
    <th class="gram-art">Avverbio</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td>qui / qua</td><td>Vieni qui!</td></tr>
  <tr><td>lì / là</td><td>Il libro è là.</td></tr>
  <tr><td>vicino / lontano</td><td>Abita vicino / lontano.</td></tr>
  <tr><td>dentro / fuori</td><td>Entra dentro! / Aspetta fuori!</td></tr>
  <tr><td>sopra / sotto</td><td>Il gatto è sopra il divano.</td></tr>
  <tr><td>davanti / dietro</td><td>Siediti davanti!</td></tr>
  <tr><td>su / giù</td><td>Vai su! / Scendi giù!</td></tr>
  <tr><td>ovunque / dappertutto</td><td>L'ho cercato dappertutto.</td></tr>
</table>

<h4>Avverbi di quantità</h4>
<ul>
  <li><strong>molto, poco, troppo, abbastanza, tanto, quanto, più, meno, quasi</strong></li>
  <li><em>Ho <strong>molto</strong> da fare. / Parla <strong>poco</strong>. / Ha mangiato <strong>troppo</strong>.</em></li>
  <li>Attenzione: quando modificano un aggettivo o altro avverbio, sono invariabili:<br>
  <em>È <strong>molto</strong> bello. / Parla <strong>troppo</strong> velocemente.</em></li>
</ul>

<h4>Avverbi di frequenza</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Frequenza — dalla più alta alla più bassa</th>
  </tr>
  <tr>
    <th class="gram-art">Avverbio</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td>sempre (100%)</td><td>Fa sempre colazione.</td></tr>
  <tr><td>di solito / solitamente</td><td>Di solito prendo il treno.</td></tr>
  <tr><td>spesso</td><td>Va spesso al cinema.</td></tr>
  <tr><td>qualche volta / a volte</td><td>A volte cucino a casa.</td></tr>
  <tr><td>raramente / di rado</td><td>Raramente esco di sera.</td></tr>
  <tr><td>mai (0%) con non</td><td>Non vado mai in discoteca.</td></tr>
</table>

<h4>Posizione degli avverbi</h4>
<ul>
  <li>Con i <strong>tempi semplici</strong>: l'avverbio va <em>dopo</em> il verbo: <em>Parla <strong>bene</strong>.</em></li>
  <li>Con i <strong>tempi composti</strong>: gli avverbi brevi vanno <em>tra ausiliare e participio</em>: <em>Ho <strong>già</strong> mangiato. / Non sono <strong>mai</strong> stato.</em></li>
  <li>Gli avverbi in -mente vanno generalmente <em>dopo</em> il participio: <em>Ha parlato <strong>lentamente</strong>.</em></li>
</ul>

<h4>Dialogo: Le abitudini di Giulia</h4>
<p><strong>Marco:</strong> Giulia, vai spesso in palestra?<br>
<strong>Giulia:</strong> Abbastanza. Di solito ci vado tre volte a settimana, ma ultimamente sono andata raramente.<br>
<strong>Marco:</strong> E fai sempre colazione?<br>
<strong>Giulia:</strong> Quasi sempre. Qualche volta mi alzo tardi e non ho tempo.<br>
<strong>Marco:</strong> Anch'io. Non ho mai capito come fa la gente ad alzarsi presto facilmente!<br>
<strong>Giulia:</strong> Lo so! Io invece di solito mi sveglio subito, ma poi resto a letto ancora un po'.</p>"""

lez["exercicios"] = [
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Forma l'avverbio in -MENTE:\n1. lento → ___\n2. facile → ___\n3. felice → ___\n4. regolare → ___\n5. rapido → ___\n6. tranquillo → ___",
        "resposta": "1. lentamente | 2. facilmente | 3. felicemente | 4. regolarmente | 5. rapidamente | 6. tranquillamente"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Avverbi di tempo. Scegli quello giusto:\n1. Ho ___ (già/ancora) mangiato. Non ho fame.\n2. Non ho ___ (già/ancora) finito. Aspetta.\n3. Arriva ___ (sempre/mai) tardi — è una sua abitudine.\n4. Non vado ___ (sempre/mai) al cinema — lo odio.",
        "resposta": "1. già | 2. ancora | 3. sempre | 4. mai"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Posizione degli avverbi nei tempi composti:\n1. Ho mangiato già. → ___\n2. Sono uscito mai. → ___\n3. Hai capito già? → ___\n4. Avevo dormito bene. → ___",
        "resposta": "1. Ho già mangiato | 2. Non sono mai uscito | 3. Hai già capito? | 4. Avevo dormito bene (avverbio di modo → può restare dopo)"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Avverbi di luogo. Completa:\n1. Vieni ___! (qui/qua = vicino a me)\n2. Il libro è ___ sul tavolo. (posizione lontana)\n3. I bambini giocano ___. (all'esterno)\n4. Ho cercato le chiavi ___. (in ogni posto)",
        "resposta": "1. qui / qua | 2. lì / là | 3. fuori | 4. dappertutto / ovunque"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Avverbi di quantità (invariabili). Correggi se necessario:\n1. È molto bella quella ragazza.\n2. Ha mangiato troppa velocemente.\n3. Parla abbastanza bene.\n4. Ho pochi da fare oggi.",
        "resposta": "1. SÌ, corretto | 2. troppo velocemente | 3. SÌ, corretto | 4. poco da fare"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Frequenza. Ordina dal più al meno frequente:\nraramente / sempre / di solito / mai / spesso / a volte",
        "resposta": "sempre → di solito → spesso → a volte → raramente → mai"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Completa con l'avverbio corretto:\n1. Non ho ___ visto quel film. (mai)\n2. Parla ___ veloce! Non capisco. (troppo)\n3. Di ___ vado a correre la mattina. (solito)\n4. Ho ___ finito! Possiamo andare. (appena/già)",
        "resposta": "1. mai | 2. troppo | 3. solito | 4. appena / già"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Descrivi le tue abitudini usando avverbi di frequenza:\n1. andare in palestra → ___\n2. fare colazione → ___\n3. leggere libri → ___\n4. guardare la TV → ___",
        "resposta": "(risposta libera) Es: vado in palestra spesso / faccio sempre colazione / leggo raramente / guardo la TV qualche volta"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "L'avverbio di FACILE è:",
        "opcoes": ["facilamente", "facilmente", "facilmento", "facilimento"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ho ___ mangiato.\" (l'azione è già avvenuta)",
        "opcoes": ["ancora", "mai", "già", "sempre"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Nei tempi composti, gli avverbi brevi vanno:",
        "opcoes": [
            "prima dell'ausiliare",
            "tra ausiliare e participio",
            "dopo il participio",
            "all'inizio della frase"
        ],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non sono ___ stato a Tokyo.\" (mai ci sono andato)",
        "opcoes": ["già", "ancora", "mai", "sempre"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "L'avverbio di LENTO è:",
        "opcoes": ["lentamente", "lentamente", "lentimamente", "lentamente"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Va ___ al cinema — almeno tre volte a settimana.\"",
        "opcoes": ["raramente", "mai", "spesso", "qualche volta"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"È ___ bella!\" — quale forma è corretta?",
        "opcoes": ["molto bella", "molti bella", "molto belli", "molte bella"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale avverbio indica luogo vicino a chi parla?",
        "opcoes": ["là", "lì", "qui", "ovunque"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ha mangiato ___.\" (con eccesso)",
        "opcoes": ["molto", "abbastanza", "poco", "troppo"],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale avverbio esprime la frequenza PIÙ BASSA?",
        "opcoes": ["raramente", "mai", "di solito", "qualche volta"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non ho ancora finito\" significa:",
        "opcoes": [
            "Ho finito prima del previsto.",
            "Ho finito già.",
            "Non ho terminato, ma sto ancora lavorando.",
            "Non finirò mai."
        ],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "L'avverbio di REGOLARE è:",
        "opcoes": ["regularmente", "regolarmente", "regolarmento", "regolarimento"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Aspetta ___ — arrivo tra poco.\" (immediatamente)",
        "opcoes": ["subito", "già", "ancora", "poi"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Gli avverbi sono:",
        "opcoes": ["variabili per genere e numero", "invariabili", "variabili per genere solo", "variabili per numero solo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Parla ___ velocemente.\" (con eccesso, avverbio di quantità invariabile)",
        "opcoes": ["troppa", "troppi", "troppo", "troppe"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"I bambini giocano ___\" (all'aperto, non dentro)",
        "opcoes": ["dentro", "vicino", "fuori", "sopra"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Di ___ prendo il caffè al bar.\" (quasi ogni giorno)",
        "opcoes": ["rado", "mai", "solito", "volta"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale posizione è ERRATA per un avverbio in -mente nei tempi composti?",
        "opcoes": [
            "Ha parlato lentamente.",
            "Lentamente ha parlato.",
            "Ha lentamente parlato.",
            "nessuna è errata, tutte ammissibili"
        ],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Raramente esco di sera\" equivale a:",
        "opcoes": ["Non esco mai di sera.", "Esco di sera ogni tanto.", "Esco spesso di sera.", "Esco sempre di sera."],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ho già capito\" — quale posizione dell'avverbio è corretta?",
        "opcoes": ["Ho capito già", "Già ho capito", "Ho già capito", "entrambe a e c"],
        "resposta": 2
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. L'avverbio di FACILE è 'facilamente'.\n2. Ho mangiato mai in quel ristorante. (non ci sono mai andato)\n3. È molto belli quei quadri.\n4. Ha parlato rapido — usa l'avverbio!\n5. Non sono ancora tornato — è corretto?",
        "resposta": "1. facilmente (non facilamente) | 2. Non ho mai mangiato | 3. molto belli è corretto (belli è agg. variabile) | 4. rapidamente | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Ho già mangiato — è corretto?\n2. Parla troppa velocemente.\n3. Vieni qua! — è corretto?\n4. Di rado esco — significa 'esco spesso'?",
        "resposta": "1. SÌ, corretto | 2. troppo velocemente | 3. SÌ, corretto | 4. No, significa 'esco raramente'"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
