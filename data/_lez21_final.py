import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXI"), None)
if lez is None:
    lez = {"id": "a1-lez21", "num": "Lezione XXI", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il gerundio e i participi"
lez["subtitulo"] = "Gerundio presente e passato, participio presente e passato"
lez["exemplos"] = [
    "Studiando ogni giorno, impari bene.",
    "Avendo studiato, ho superato l'esame.",
    "Pur essendo stanco, ha continuato a lavorare.",
    "Ho visto Marco uscire dal negozio.",
    "La porta aperta lasciava entrare il vento.",
    "Correndo, è arrivato in tempo."
]

lez["teoria"] = """<h3>Il gerundio</h3>
<p>Il <strong>gerundio</strong> è una forma verbale indefinita che esprime un'azione in relazione alla frase principale. Può essere <em>presente</em> o <em>passato</em>.</p>

<h4>Formazione del gerundio</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Gerundio — formazione</th>
  </tr>
  <tr>
    <th class="gram-art">Coniugazione</th>
    <th class="gram-art">Infinito</th>
    <th class="gram-art">Gerundio presente</th>
    <th class="gram-art">Gerundio passato</th>
  </tr>
  <tr><td>-ARE</td><td>parlare</td><td>parlando</td><td>avendo parlato</td></tr>
  <tr><td>-ERE</td><td>vedere</td><td>vedendo</td><td>avendo visto</td></tr>
  <tr><td>-IRE</td><td>partire</td><td>partendo</td><td>essendo partito</td></tr>
  <tr><td>essere</td><td>essere</td><td>essendo</td><td>essendo stato</td></tr>
  <tr><td>fare</td><td>fare</td><td>facendo</td><td>avendo fatto</td></tr>
  <tr><td>dire</td><td>dire</td><td>dicendo</td><td>avendo detto</td></tr>
  <tr><td>bere</td><td>bere</td><td>bevendo</td><td>avendo bevuto</td></tr>
</table>

<h4>Usi del gerundio presente</h4>
<p>Il gerundio presente indica un'azione <strong>contemporanea</strong> a quella della principale:</p>
<ul>
  <li><strong>Modo/mezzo:</strong> <em>Studiando ogni giorno, impari bene.</em></li>
  <li><strong>Causa:</strong> <em>Essendo stanco, è andato a letto presto.</em></li>
  <li><strong>Condizione:</strong> <em>Lavorando sodo, potresti farcela.</em></li>
  <li><strong>Tempo:</strong> <em>Uscendo di casa, ho incontrato Mario.</em></li>
  <li><strong>Concessione (pur + gerundio):</strong> <em>Pur sapendo la verità, non ha parlato.</em></li>
  <li><strong>Stare + gerundio (progressivo):</strong> <em>Sto studiando.</em> / <em>Stavo mangiando.</em></li>
</ul>

<h4>Usi del gerundio passato</h4>
<p>Il gerundio passato indica un'azione <strong>precedente</strong> a quella della principale:</p>
<ul>
  <li><em><strong>Avendo studiato</strong> molto, ho superato l'esame.</em></li>
  <li><em><strong>Essendo arrivata</strong> tardi, non ha trovato posto.</em></li>
  <li><em><strong>Avendo letto</strong> il libro, poteva rispondere.</em></li>
</ul>

<h4>Attenzione: il soggetto del gerundio</h4>
<p>Il soggetto del gerundio deve essere lo stesso della frase principale:</p>
<ul>
  <li>✅ <em><strong>Camminando</strong> per la strada, <strong>ho</strong> incontrato Paolo.</em> (io = io)</li>
  <li>❌ <em>Camminando per la strada, <strong>Paolo</strong> mi ha salutato.</em> (soggetti diversi)</li>
</ul>

<h4>Il participio presente</h4>
<p>Il <strong>participio presente</strong> si forma aggiungendo <em>-ante/-ente</em> al tema:</p>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Participio presente</th>
  </tr>
  <tr>
    <th class="gram-art">Infinito</th>
    <th class="gram-art">Participio presente</th>
    <th class="gram-art">Uso comune</th>
  </tr>
  <tr><td>parlare</td><td>parlante</td><td>la lingua parlante</td></tr>
  <tr><td>seguire</td><td>seguente</td><td>il giorno seguente</td></tr>
  <tr><td>interessare</td><td>interessante</td><td>un libro interessante</td></tr>
  <tr><td>studiare</td><td>studiante</td><td>gli studenti (→ studente)</td></tr>
</table>
<p>Oggi il participio presente ha funzione prevalentemente <strong>aggettivale</strong>.</p>

<h4>Il participio passato</h4>
<p>Il <strong>participio passato</strong> ha usi fondamentali:</p>
<ul>
  <li><strong>Ausiliare nei tempi composti:</strong> <em>Ho <strong>mangiato</strong>. Sono <strong>partito</strong>.</em></li>
  <li><strong>Forma passiva:</strong> <em>La porta è stata <strong>aperta</strong>.</em></li>
  <li><strong>Aggettivo:</strong> <em>una finestra <strong>rotta</strong>, un lavoro <strong>fatto</strong></em></li>
  <li><strong>Proposizione participiale:</strong> <em><strong>Finito</strong> il lavoro, siamo andati a cena.</em></li>
</ul>

<h4>Dialogo: In biblioteca</h4>
<p><strong>Giulia:</strong> Stai studiando ancora? Sono le undici di sera!<br>
<strong>Roberto:</strong> Sì, studiando ogni giorno, spero di superare l'esame la prossima settimana.<br>
<strong>Giulia:</strong> Avendo già letto tutti i libri, dovresti fare qualche esercizio pratico.<br>
<strong>Roberto:</strong> Hai ragione. Pur essendo stanco, continuerò ancora un po'.<br>
<strong>Giulia:</strong> Finito di studiare, vieni a prendere un caffè con me?<br>
<strong>Roberto:</strong> Volentieri! Facendo una pausa, starò meglio.</p>"""

lez["exercicios"] = [
    # --- REVELAR exercises ---
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Forma il gerundio presente:\n1. lavorare → ___\n2. scrivere → ___\n3. dormire → ___\n4. fare → ___\n5. essere → ___\n6. bere → ___",
        "resposta": "1. lavorando | 2. scrivendo | 3. dormendo | 4. facendo | 5. essendo | 6. bevendo"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Forma il gerundio passato:\n1. andare → ___\n2. leggere → ___\n3. partire → ___\n4. fare → ___\n5. vedere → ___",
        "resposta": "1. essendo andato | 2. avendo letto | 3. essendo partito | 4. avendo fatto | 5. avendo visto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Sostituisci con il gerundio:\n1. Mentre studiava, ascoltava musica. → ___\n2. Poiché era tardi, è andato a casa. → ___\n3. Anche se era stanco, ha continuato. → ___\n4. Dopo che ho mangiato, sono uscito. → ___",
        "resposta": "1. Studiando, ascoltava musica | 2. Essendo tardi, è andato a casa | 3. Pur essendo stanco, ha continuato | 4. Avendo mangiato, sono uscito"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Completa con STARE + gerundio:\n1. Marco ___ (leggere) un libro adesso.\n2. Noi ___ (mangiare) quando hai chiamato.\n3. Loro ___ (lavorare) tutto il giorno.\n4. Io ___ (scrivere) una mail in questo momento.",
        "resposta": "1. sta leggendo | 2. stavamo mangiando | 3. stanno lavorando | 4. sto scrivendo"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Trasforma usando il participio passato come aggettivo:\n1. La finestra che è stata rotta → la finestra ___\n2. Il libro che è stato aperto → il libro ___\n3. Le lettere che sono state scritte → le lettere ___\n4. Il lavoro che è stato fatto → il lavoro ___",
        "resposta": "1. rotta | 2. aperto | 3. scritte | 4. fatto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Forma proposizioni participiali:\n1. Dopo che ha finito il lavoro, è uscito. → ___\n2. Dopo che siamo arrivati, abbiamo chiamato. → ___\n3. Dopo che ha letto la lettera, si è calmata. → ___",
        "resposta": "1. Finito il lavoro, è uscito | 2. Arrivati, abbiamo chiamato | 3. Letta la lettera, si è calmata"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Correggi o conferma il gerundio (soggetti uguali?):\n1. Uscendo di casa, la pioggia mi ha bagnato. ✓ o ✗?\n2. Studiando ogni giorno, imparo bene. ✓ o ✗?\n3. Essendo tardi, abbiamo preso un taxi. ✓ o ✗?\n4. Correndo veloce, il treno è partito. ✓ o ✗?",
        "resposta": "1. ✗ (soggetti diversi) | 2. ✓ | 3. ✓ | 4. ✗ (soggetti diversi)"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Spiega la funzione del gerundio (modo, causa, tempo, concessione, condizione):\n1. Studiando si impara. → ___\n2. Pur avendo soldi, vive semplicemente. → ___\n3. Avendo finito presto, siamo usciti. → ___\n4. Lavorando sodo, riuscirai. → ___",
        "resposta": "1. modo/mezzo | 2. concessione | 3. tempo/causa | 4. condizione"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "Il gerundio di FARE è:",
        "opcoes": ["farendo", "facendo", "fando", "fendo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "___ ogni giorno, migliorerai il tuo italiano.",
        "opcoes": ["Studiato", "Studiando", "Studio", "Studiare"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Avendo ___ il libro, poteva rispondere a tutte le domande.",
        "opcoes": ["letto", "leggendo", "legge", "leggere"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Sto ___ una email importante.",
        "opcoes": ["scritto", "scriva", "scrivendo", "scrivere"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Pur ___ stanco, ha finito il lavoro.",
        "opcoes": ["essere", "essendo", "fosse", "sia"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il gerundio passato di PARTIRE è:",
        "opcoes": ["avendo partito", "essendo partiti", "essendo partito", "partendo"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "___ la lettera, si è sentita meglio. (proposizione participiale)",
        "opcoes": ["Leggendo", "Letta", "Avendo leggere", "Leggere"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale frase usa correttamente il gerundio?",
        "opcoes": [
            "Uscendo di casa, la pioggia ci ha bagnati.",
            "Uscendo di casa, abbiamo preso l'ombrello.",
            "Uscendo di casa, il sole è apparso.",
            "Uscendo di casa, il tram è passato."
        ],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il participio presente di INTERESSARE è:",
        "opcoes": ["interessato", "interessante", "interessando", "interessi"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Stavamo ___ quando sei arrivato.",
        "opcoes": ["mangiato", "mangiare", "mangiando", "mangiato"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Il gerundio di BERE è:",
        "opcoes": ["berendo", "bevendo", "birendo", "bevuto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "___ già vista la mostra, non ci siamo tornati.",
        "opcoes": ["Avendo", "Essendo", "Avuto", "Avere"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Il gerundio esprime principalmente:",
        "opcoes": [
            "un'azione futura",
            "un'azione indipendente",
            "un'azione in relazione alla principale",
            "un'azione al passato remoto"
        ],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Finito di lavorare, siamo ___ a casa.",
        "opcoes": ["andando", "andati", "andiamo", "andare"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "___ (dormire) bene, mi sono sentito riposato.",
        "opcoes": ["Avendo dormito", "Dormendo", "Dormito", "Essendo dormito"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Il participio passato si usa per formare:",
        "opcoes": [
            "solo il futuro",
            "i tempi composti e la forma passiva",
            "solo l'imperativo",
            "il congiuntivo presente"
        ],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Una finestra ___ lasciava entrare il freddo.",
        "opcoes": ["aperta", "aprendo", "aprire", "aperto"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "___ (arrivare) in ritardo, non ha trovato posto.",
        "opcoes": ["Essendo arrivata", "Avendo arrivato", "Arrivando", "Arrivata avendo"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Correndo ogni mattina, ___ in forma.",
        "opcoes": ["stai", "sto", "stando", "stavo"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Pur ___ la risposta, non ha parlato.",
        "opcoes": ["sapere", "sapendo", "saputo", "sa"],
        "resposta": 1
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Il gerundio di DIRE è dicendo — è corretto?\n2. Avendo partito presto, è arrivato in tempo.\n3. Uscendo di casa, il telefono ha squillato.\n4. Stavo mangiare quando hai chiamato.\n5. Letto il libro, siamo usciti — è corretto?",
        "resposta": "1. SÌ, corretto | 2. Essendo partito | 3. ✗ soggetti diversi | 4. mangiando | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Studiando ogni giorno, imparo — è corretto?\n2. Pur essere stanco, ha lavorato.\n3. Avendo letto, potevo rispondere — è corretto?\n4. Finendo il lavoro, siamo andati a cena.",
        "resposta": "1. SÌ, corretto | 2. essendo | 3. SÌ, corretto | 4. Finito il lavoro (proposizione participiale)"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
