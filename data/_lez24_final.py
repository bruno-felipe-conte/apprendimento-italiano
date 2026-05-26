import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXIV"), None)
if lez is None:
    lez = {"id": "a1-lez24", "num": "Lezione XXIV", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I pronomi diretti e indiretti combinati"
lez["subtitulo"] = "Ripasso e uso avanzato dei pronomi combinati con i tempi composti"
lez["exemplos"] = [
    "Me lo dai?",
    "Glielo ho già detto.",
    "Te la mando domani.",
    "Ce ne sono molti.",
    "Ve lo spiego subito.",
    "Non gliene ho parlato ancora."
]

lez["teoria"] = """<h3>I pronomi diretti e indiretti combinati — ripasso avanzato</h3>
<p>Quando un <strong>pronome indiretto</strong> e un <strong>pronome diretto</strong> (o <em>ne</em>) si trovano insieme nella stessa frase, si uniscono formando un <strong>pronome combinato</strong>.</p>

<h4>Tabella completa dei pronomi combinati</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="6">Pronomi combinati</th>
  </tr>
  <tr>
    <th class="gram-art">Indiretto →</th>
    <th class="gram-art">+ lo</th>
    <th class="gram-art">+ la</th>
    <th class="gram-art">+ li</th>
    <th class="gram-art">+ le</th>
    <th class="gram-art">+ ne</th>
  </tr>
  <tr><td><strong>mi</strong></td><td>me lo</td><td>me la</td><td>me li</td><td>me le</td><td>me ne</td></tr>
  <tr><td><strong>ti</strong></td><td>te lo</td><td>te la</td><td>te li</td><td>te le</td><td>te ne</td></tr>
  <tr><td><strong>gli/le</strong></td><td>glielo</td><td>gliela</td><td>glieli</td><td>gliele</td><td>gliene</td></tr>
  <tr><td><strong>ci</strong></td><td>ce lo</td><td>ce la</td><td>ce li</td><td>ce le</td><td>ce ne</td></tr>
  <tr><td><strong>vi</strong></td><td>ve lo</td><td>ve la</td><td>ve li</td><td>ve le</td><td>ve ne</td></tr>
  <tr><td><strong>gli (loro)</strong></td><td>glielo</td><td>gliela</td><td>glieli</td><td>gliele</td><td>gliene</td></tr>
</table>

<h4>Posizione dei pronomi combinati</h4>
<p>I pronomi combinati si collocano <strong>prima del verbo coniugato</strong> o si <strong>attaccano all'infinito</strong> (che perde la -e finale):</p>
<ul>
  <li><em><strong>Me lo</strong> dai? — Sì, te lo do subito.</em></li>
  <li><em>Vuoi dirmelo? — Sì, voglio dirtelo.</em></li>
  <li><em><strong>Glielo</strong> mando domani.</em></li>
</ul>

<h4>Pronomi combinati con i tempi composti</h4>
<p>Con i tempi composti (passato prossimo, trapassato, ecc.), il participio passato <strong>concorda con il pronome diretto</strong>:</p>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Accordo del participio con pronome diretto</th>
  </tr>
  <tr>
    <th class="gram-art">Pronome diretto</th>
    <th class="gram-art">Esempio</th>
    <th class="gram-art">Accordo</th>
  </tr>
  <tr><td>lo (m. sing.)</td><td>Me lo hai dato → Me l'hai dat<strong>o</strong></td><td>-o</td></tr>
  <tr><td>la (f. sing.)</td><td>Te la ho mandata → Te l'ho mandat<strong>a</strong></td><td>-a</td></tr>
  <tr><td>li (m. plur.)</td><td>Glieli ho comprati → Glieli ho comprat<strong>i</strong></td><td>-i</td></tr>
  <tr><td>le (f. plur.)</td><td>Ve le ho portate → Ve le ho portat<strong>e</strong></td><td>-e</td></tr>
  <tr><td>ne</td><td>Ce ne ha parlato (accordo facoltativo)</td><td>variabile</td></tr>
</table>

<h4>Pronomi con i verbi modali</h4>
<p>Con i verbi modali i pronomi si mettono <strong>prima del modale</strong> o si <strong>attaccano all'infinito</strong>:</p>
<ul>
  <li><em><strong>Te lo</strong> posso dire. / Posso dirtelo.</em></li>
  <li><em><strong>Glielo</strong> devo mandare. / Devo mandarglielo.</em></li>
  <li><em><strong>Me ne</strong> vuoi parlare? / Vuoi parlarmene?</em></li>
</ul>

<h4>NE con i pronomi combinati</h4>
<p><strong>Ne</strong> sostituisce una quantità o un complemento introdotto da <em>di</em>:</p>
<ul>
  <li><em>Quante pizze hai mangiato? <strong>Ne</strong> ho mangiate due.</em></li>
  <li><em>Hai parlato del problema a Marco? Sì, <strong>gliene</strong> ho parlato.</em></li>
  <li><em>Hai bisogno di aiuto? Sì, <strong>ne</strong> ho bisogno.</em></li>
</ul>

<h4>Dialogo: Un regalo</h4>
<p><strong>Anna:</strong> Hai comprato il regalo per Marco?<br>
<strong>Luigi:</strong> Sì, glielo compro oggi pomeriggio.<br>
<strong>Anna:</strong> Gli hai già detto della festa?<br>
<strong>Luigi:</strong> No, non gliene ho parlato ancora. Voglio dirglielo di persona.<br>
<strong>Anna:</strong> E le candeline? Le hai prese?<br>
<strong>Luigi:</strong> Me le porti tu? Io non ho tempo.<br>
<strong>Anna:</strong> Va bene, te le porto io.</p>"""

lez["exercicios"] = [
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Sostituisci con i pronomi combinati:\n1. Do il libro a te. → ___\n2. Mando la lettera a lui. → ___\n3. Racconto la storia a voi. → ___\n4. Porto i fiori a lei. → ___",
        "resposta": "1. Te lo do | 2. Gliela mando | 3. Ve la racconto | 4. Gliele porto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Pronomi combinati con passato prossimo (accordo del participio):\n1. Ho dato la lettera a Marco. → ___\n2. Ho comprato i libri a te. → ___\n3. Ho portato le rose a lei. → ___\n4. Ho mandato il pacco a voi. → ___",
        "resposta": "1. Gliela ho data / Gliel'ho data | 2. Te li ho comprati | 3. Gliele ho portate | 4. Ve lo ho mandato / Ve l'ho mandato"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Rispondi usando i pronomi combinati:\n1. Hai spiegato la grammatica agli studenti? Sì, ___.\n2. Hai portato i documenti a me? No, ___.\n3. Hai dato la ricetta a tua sorella? Sì, ___.\n4. Hai comprato i biglietti per noi? Sì, ___.",
        "resposta": "1. Sì, gliela ho spiegata | 2. No, non te li ho portati | 3. Sì, gliela ho data | 4. Sì, ve li ho comprati"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — NE combinato. Completa:\n1. Hai parlato del viaggio a Marco? Sì, ___ ho parlato.\n2. Hai bisogno di aiuto? Sì, ___ ho bisogno.\n3. Quante paste hai comprato? ___ ho comprate tre.\n4. Hai detto a lei del problema? Sì, ___ ho detto.",
        "resposta": "1. gliene | 2. ne | 3. ne | 4. gliene"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Pronomi con i verbi modali (due posizioni):\n1. Devo dire la verità a te. → ___ (prima del modale) / ___ (attaccato all'infinito)\n2. Voglio portare i fiori a lei. → ___ / ___\n3. Puoi mandare il messaggio a noi? → ___ / ___",
        "resposta": "1. Te la devo dire / Devo dirtela | 2. Glieli voglio portare / Voglio portarglieli | 3. Ce lo puoi mandare? / Puoi mandarcelo?"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Imperativo + pronomi combinati:\n1. Dai il libro a me! → ___!\n2. Manda la lettera a lui! → ___!\n3. Porta i fiori a noi! → ___!\n4. Di' la verità a lei! → ___!",
        "resposta": "1. Dammelo! | 2. Mandagliela! | 3. Portaceli! | 4. Digliela!"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Identifica i pronomi nella frase:\n1. Glielo mando domani. → indiretto: ___ / diretto: ___\n2. Me ne ha parlato. → indiretto: ___ / ne sostituisce: ___\n3. Ve le ho portate. → indiretto: ___ / diretto: ___",
        "resposta": "1. gli (a lui/lei) / lo | 2. mi / un complemento di/partitivo | 3. vi (a voi) / le"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Trasforma usando i pronomi (risposta libera guidata):\n1. Ho già regalato il libro a Marco e Sofia. → ___\n2. Posso spiegare le regole a voi? → ___\n3. Non ho ancora detto niente ai miei genitori. → ___",
        "resposta": "1. Gliel'ho già regalato | 2. Ve le posso spiegare? / Posso spiegarvele? | 3. Non gliene ho ancora detto niente"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "\"Mando la lettera a te\" con pronomi combinati diventa:",
        "opcoes": ["mi la mando", "te la mando", "gli la mando", "ve la mando"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Do il libro a lui\" con pronomi combinati diventa:",
        "opcoes": ["me lo do", "glielo do", "te lo do", "ce lo do"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Ho dato la lettera a Maria → con pronomi:",
        "opcoes": ["Glielo ho dato", "Gliel'ho data", "La le ho data", "Le lo ho dato"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ne\" nel pronome combinato GLIENE sostituisce:",
        "opcoes": ["il pronome diretto", "un complemento di/partitivo", "il soggetto", "l'oggetto diretto maschile"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Vuoi portare i fiori a me? → Vuoi ___?",
        "opcoes": ["portarmeli", "portarmile", "portarlomi", "portameli"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Ho comprato le scarpe per voi → con pronomi:",
        "opcoes": ["Ve le ho comprate", "Vi le ho comprate", "Ve li ho comprati", "Ce le ho comprate"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Il participio passato con pronome combinato concorda con:",
        "opcoes": ["il soggetto", "il pronome indiretto", "il pronome diretto", "il verbo ausiliare"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Hai detto la verità a noi?\" con pronomi → \"___ hai detto?\"",
        "opcoes": ["Ce la", "Ve la", "Me la", "Gliela"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Devo spiegare la situazione a te → con pronomi (attaccato all'infinito):",
        "opcoes": ["devo spiegartila", "devo spiegartela", "devo spiegarteela", "devo spiegartila"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Glieli ho mandati → \"li\" si riferisce a:",
        "opcoes": ["qualcosa di femminile singolare", "qualcosa di maschile plurale", "qualcosa di femminile plurale", "una quantità"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Hai parlato del viaggio a Marco?\" → \"Sì, ___ ho parlato.\"",
        "opcoes": ["ne gli", "gliene", "glielo", "gli ne"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Porto le borse a voi → con pronomi:",
        "opcoes": ["ve le porto", "vi le porto", "ve li porto", "ce le porto"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Con il verbo modale, i pronomi combinati possono andare:",
        "opcoes": [
            "solo prima del modale",
            "solo attaccati all'infinito",
            "sia prima del modale sia attaccati all'infinito",
            "solo dopo il participio"
        ],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Me ne ha comprate tre\" → \"ne\" sostituisce:",
        "opcoes": ["il soggetto", "una quantità di qualcosa", "il complemento indiretto", "l'avverbio"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Mandagliela! → si tratta di:",
        "opcoes": ["indicativo + pronomi", "imperativo + pronomi attaccati", "congiuntivo + pronomi", "infinito + pronomi"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ho dato i libri a te e Marco\" → con pronomi:",
        "opcoes": ["Ve li ho dati", "Glielo ho dati", "Glieli ho dati", "Te li ho dati"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale forma è corretta?",
        "opcoes": ["Li me ha dato", "Me lo ha dato", "Me l'ha dato (maschile)", "Lo mi ha dato"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Gliela\" può riferirsi a:",
        "opcoes": [
            "solo a lui + la",
            "solo a lei + la",
            "a lui, lei o loro + la",
            "solo a loro + la"
        ],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Puoi dirmelo?\" equivale a:",
        "opcoes": ["Mel puoi dire?", "Me lo puoi dire?", "Lo mi puoi dire?", "Puoi lo dirmi?"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Ho portato le rose a loro → con pronomi:",
        "opcoes": ["Loro le ho portate", "Gliele ho portate", "Ve le ho portate", "Ce le ho portate"],
        "resposta": 1
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Te lo ho dato ieri. (elision)\n2. Glielo ho dato — accordo: dato o data? (riferito a 'la lettera')\n3. Me ne ha parlato di molto.\n4. Glieli ho portato. (riferito a 'i libri')\n5. Lo mi puoi dire?",
        "resposta": "1. Te l'ho dato | 2. data (concorda con 'la lettera') | 3. Me ne ha parlato molto | 4. Glieli ho portati | 5. Me lo puoi dire?"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Vi le ho comprate. (vi → ve davanti a pronome diretto)\n2. Devo spiegartila la lezione.\n3. Ne gli ho parlato.\n4. Vuoi portarmeli i libri? — è corretto?",
        "resposta": "1. Ve le ho comprate | 2. Devo spiegartela | 3. Gliene ho parlato | 4. SÌ, corretto"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
