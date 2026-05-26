import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXII"), None)
if lez is None:
    lez = {"id": "a1-lez22", "num": "Lezione XXII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "La forma passiva"
lez["subtitulo"] = "Costruzione passiva con essere, venire, andare e si passivante"
lez["exemplos"] = [
    "Il libro è stato scritto da Moravia.",
    "La porta viene chiusa ogni sera.",
    "Questo errore va corretto subito.",
    "In Italia si mangia molto bene.",
    "Le lettere sono state spedite ieri.",
    "Il ladro fu arrestato dalla polizia."
]

lez["teoria"] = """<h3>La forma passiva</h3>
<p>Nella <strong>forma passiva</strong>, il soggetto della frase non compie l'azione ma la subisce. L'azione è compiuta dall'<strong>agente</strong>, introdotto dalla preposizione <strong>da</strong>.</p>

<h4>Forma attiva vs. forma passiva</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Attiva → Passiva</th>
  </tr>
  <tr>
    <th class="gram-art">Forma attiva</th>
    <th class="gram-art">Forma passiva</th>
  </tr>
  <tr><td>Marco scrive la lettera.</td><td>La lettera è scritta da Marco.</td></tr>
  <tr><td>Il professore ha corretto i compiti.</td><td>I compiti sono stati corretti dal professore.</td></tr>
  <tr><td>Tutti amano questa canzone.</td><td>Questa canzone è amata da tutti.</td></tr>
  <tr><td>La polizia arrestò il ladro.</td><td>Il ladro fu arrestato dalla polizia.</td></tr>
</table>

<h4>Passiva con ESSERE</h4>
<p>La costruzione passiva più comune usa <strong>essere + participio passato</strong>. Il participio concorda con il soggetto.</p>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Passiva con ESSERE — tutti i tempi</th>
  </tr>
  <tr>
    <th class="gram-art">Tempo</th>
    <th class="gram-art">Attiva</th>
    <th class="gram-art">Passiva</th>
  </tr>
  <tr><td>Presente</td><td>Marco legge il libro.</td><td>Il libro è letto da Marco.</td></tr>
  <tr><td>Imperfetto</td><td>Marco leggeva il libro.</td><td>Il libro era letto da Marco.</td></tr>
  <tr><td>Passato prossimo</td><td>Marco ha letto il libro.</td><td>Il libro è stato letto da Marco.</td></tr>
  <tr><td>Futuro</td><td>Marco leggerà il libro.</td><td>Il libro sarà letto da Marco.</td></tr>
  <tr><td>Condizionale</td><td>Marco leggerebbe il libro.</td><td>Il libro sarebbe letto da Marco.</td></tr>
</table>

<h4>Passiva con VENIRE</h4>
<p><strong>Venire</strong> sostituisce <em>essere</em> nei tempi semplici per indicare un'azione abituale o ripetuta:</p>
<ul>
  <li><em>La porta <strong>viene chiusa</strong> ogni sera.</em> (non viene usato nei tempi composti)</li>
  <li><em>I compiti <strong>venivano corretti</strong> dal professore.</em></li>
  <li><em>Le finestre <strong>vengono aperte</strong> al mattino.</em></li>
</ul>

<h4>Passiva con ANDARE</h4>
<p><strong>Andare</strong> + participio passato esprime <strong>obbligo o necessità</strong> (= deve essere fatto):</p>
<ul>
  <li><em>Questo errore <strong>va corretto</strong> subito.</em> (= deve essere corretto)</li>
  <li><em>Le regole <strong>vanno rispettate</strong>.</em> (= devono essere rispettate)</li>
  <li><em>Il modulo <strong>andava compilato</strong> ieri.</em></li>
</ul>

<h4>Il SI passivante</h4>
<p>Il <strong>si passivante</strong> si usa quando non si vuole indicare l'agente. Il verbo concorda con il soggetto:</p>
<ul>
  <li><em>In Italia <strong>si mangia</strong> bene.</em> (= il cibo viene mangiato bene)</li>
  <li><em><strong>Si vendono</strong> appartamenti.</em> (= gli appartamenti vengono venduti)</li>
  <li><em><strong>Si parla</strong> italiano qui.</em></li>
  <li><em><strong>Si sono aperti</strong> nuovi negozi.</em></li>
</ul>

<h4>Differenza VENIRE / ANDARE / ESSERE</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Ausiliari passivi a confronto</th>
  </tr>
  <tr>
    <th class="gram-art">Ausiliare</th>
    <th class="gram-art">Uso</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td>ESSERE</td><td>Tutti i tempi, neutro</td><td>Il libro è scritto da lui.</td></tr>
  <tr><td>VENIRE</td><td>Solo tempi semplici, azione abituale</td><td>Il libro viene scritto ogni anno.</td></tr>
  <tr><td>ANDARE</td><td>Tutti i tempi semplici, obbligo</td><td>Il libro va letto subito.</td></tr>
</table>

<h4>Dialogo: In ufficio</h4>
<p><strong>Direttore:</strong> Il rapporto è stato preparato?<br>
<strong>Segretaria:</strong> Sì, è stato finito stamattina e verrà spedito nel pomeriggio.<br>
<strong>Direttore:</strong> Bene. Queste lettere vanno firmate entro oggi.<br>
<strong>Segretaria:</strong> Certo. Vengono sempre firmate di pomeriggio.<br>
<strong>Direttore:</strong> E il documento? Si è già stampato?<br>
<strong>Segretaria:</strong> Sì, è stato stampato e distribuito a tutti.</p>"""

lez["exercicios"] = [
    # --- REVELAR exercises ---
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Trasforma alla forma passiva:\n1. Marco scrive la lettera. → ___\n2. La maestra corregge i compiti. → ___\n3. Tutti amano questa canzone. → ___\n4. Il cuoco prepara la cena. → ___",
        "resposta": "1. La lettera è scritta da Marco | 2. I compiti sono corretti dalla maestra | 3. Questa canzone è amata da tutti | 4. La cena è preparata dal cuoco"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Trasforma alla passiva (passato prossimo):\n1. Il professore ha spiegato la lezione. → ___\n2. Maria ha comprato il vestito. → ___\n3. I ragazzi hanno aperto le finestre. → ___\n4. La polizia ha arrestato il ladro. → ___",
        "resposta": "1. La lezione è stata spiegata dal professore | 2. Il vestito è stato comprato da Maria | 3. Le finestre sono state aperte dai ragazzi | 4. Il ladro è stato arrestato dalla polizia"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Usa VENIRE per indicare azioni abituali:\n1. La porta è chiusa ogni sera. → La porta ___ ogni sera.\n2. I compiti sono corretti dal professore. → I compiti ___ dal professore.\n3. Le lettere sono spedite il lunedì. → Le lettere ___ il lunedì.",
        "resposta": "1. viene chiusa | 2. vengono corretti | 3. vengono spedite"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Usa ANDARE (obbligo):\n1. Questo modulo deve essere compilato. → Questo modulo ___.\n2. Le regole devono essere rispettate. → Le regole ___.\n3. Il rapporto deve essere consegnato domani. → Il rapporto ___.",
        "resposta": "1. va compilato | 2. vanno rispettate | 3. va consegnato domani"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — SI passivante. Trasforma:\n1. Le persone parlano italiano qui. → ___\n2. Le persone vendono appartamenti in questa zona. → ___\n3. Le persone mangiano bene in questo ristorante. → ___\n4. Le persone aprono i negozi alle nove. → ___",
        "resposta": "1. Si parla italiano qui | 2. Si vendono appartamenti in questa zona | 3. Si mangia bene in questo ristorante | 4. Si aprono i negozi alle nove"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Trasforma dalla passiva all'attiva:\n1. Il libro è stato scritto da Moravia. → ___\n2. La torta è stata mangiata dai bambini. → ___\n3. Le finestre vengono aperte dal custode. → ___",
        "resposta": "1. Moravia ha scritto il libro | 2. I bambini hanno mangiato la torta | 3. Il custode apre le finestre"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Scegli ESSERE, VENIRE o ANDARE:\n1. Il rapporto ___ (essere/venire) spedito ogni mese. → ___\n2. Questi errori ___ (andare) corretti subito. → ___\n3. Il progetto ___ (essere) finito ieri. → ___\n4. Le regole ___ (andare) rispettate sempre. → ___",
        "resposta": "1. viene | 2. vanno | 3. è stato | 4. vanno"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Forma passiva a tutti i tempi:\nVerbo: COSTRUIRE — soggetto: il ponte — agente: gli ingegneri\n1. Presente: ___\n2. Imperfetto: ___\n3. Passato prossimo: ___\n4. Futuro: ___",
        "resposta": "1. Il ponte è costruito dagli ingegneri | 2. Il ponte era costruito dagli ingegneri | 3. Il ponte è stato costruito dagli ingegneri | 4. Il ponte sarà costruito dagli ingegneri"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "La lettera ___ scritta da Marco.",
        "opcoes": ["ha", "è", "ha stata", "viene stata"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "I compiti ___ corretti ogni giorno dal professore. (azione abituale)",
        "opcoes": ["sono stati", "vanno", "vengono", "andranno"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Questo documento ___ firmato subito. (obbligo)",
        "opcoes": ["viene", "va", "è", "andrà stato"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "In questo negozio ___ prodotti biologici.",
        "opcoes": ["si vende", "si vendono", "si è venduto", "si vendiamo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il museo ___ aperto il mese scorso.",
        "opcoes": ["viene", "è stato", "va", "veniva"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Le regole ___ rispettate da tutti. (obbligo)",
        "opcoes": ["vengono", "vanno", "sono", "verranno"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Nella frase passiva, l'agente è introdotto da:",
        "opcoes": ["con", "per", "da", "in"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ molte lingue in questo ufficio. (SI passivante)",
        "opcoes": ["Si parla", "Si parlano", "Si è parlato", "Si parlava"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il libro ___ pubblicato l'anno prossimo.",
        "opcoes": ["è stato", "viene", "sarà", "va"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "VENIRE passivo si usa solo con:",
        "opcoes": ["tempi composti", "tempi semplici", "il futuro", "il condizionale passato"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "La pasta ___ ogni giorno in questo ristorante. (SI passivante)",
        "opcoes": ["si fa", "si fanno", "si fa fatto", "si è fatta"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale frase è alla forma passiva?",
        "opcoes": [
            "Marco ha scritto la lettera.",
            "La lettera è stata scritta da Marco.",
            "Marco scriveva la lettera.",
            "Marco scriverà la lettera."
        ],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il partecipante ___ premiato durante la cerimonia.",
        "opcoes": ["è stato", "ha stato", "è", "venne stato"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "ANDARE + participio passato esprime:",
        "opcoes": ["un'azione abituale", "un'azione passata", "un obbligo", "un desiderio"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Le notizie ___ trasmesse ogni ora. (azione abituale, tempi semplici)",
        "opcoes": ["sono state", "vengono", "vanno", "andranno"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Qual è la forma passiva corretta del futuro?",
        "opcoes": [
            "Il progetto viene finito domani.",
            "Il progetto sarà finito domani.",
            "Il progetto è finito domani.",
            "Il progetto va finito domani."
        ],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "___ una nuova legge approvata ieri.",
        "opcoes": ["Si è", "È stata", "Si è stata", "Viene stata"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Questi moduli ___ compilati entro venerdì. (obbligo)",
        "opcoes": ["vengono", "sono", "vanno", "verranno"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "In questo ristorante ___ solo pesce fresco.",
        "opcoes": ["si servono", "si serve", "si è servito", "si serviva"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "La finestra ___ aperta da qualcuno durante la notte.",
        "opcoes": ["viene stata", "è stata", "va stata", "veniva stata"],
        "resposta": 1
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Il libro è scritto ha Moravia.\n2. I compiti vengono stati corretti ieri.\n3. Questo errore va correggersi.\n4. In Italia si mangiano bene.\n5. La porta viene chiusa ogni sera — è corretto?",
        "resposta": "1. da Moravia | 2. sono stati corretti | 3. va corretto | 4. si mangia | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Le regole andano rispettate.\n2. Il rapporto è stato scritto da il direttore.\n3. Si vende appartamenti qui.\n4. Il progetto viene finito la settimana scorsa.",
        "resposta": "1. vanno | 2. dal direttore | 3. si vendono | 4. è stato finito"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
