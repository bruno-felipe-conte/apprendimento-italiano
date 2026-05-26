import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXVIII"), None)
if lez is None:
    lez = {"id": "a1-lez28", "num": "Lezione XXVIII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Le congiunzioni e le proposizioni subordinate"
lez["subtitulo"] = "Congiunzioni coordinanti e subordinanti — causali, temporali, finali, concessive"
lez["exemplos"] = [
    "Studio italiano perché mi piace la cultura.",
    "Quando arrivo, ti chiamo.",
    "Studio affinché tu possa capire.",
    "Benché sia tardi, continuiamo.",
    "Appena finisco, esco.",
    "Poiché era stanco, è andato a letto."
]

lez["teoria"] = """<h3>Le congiunzioni e le proposizioni subordinate</h3>
<p>Le <strong>congiunzioni</strong> collegano parole, frasi o proposizioni. Si dividono in <strong>coordinanti</strong> (uniscono elementi dello stesso livello) e <strong>subordinanti</strong> (introducono proposizioni dipendenti).</p>

<h4>Congiunzioni coordinanti</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Congiunzioni coordinanti</th>
  </tr>
  <tr>
    <th class="gram-art">Tipo</th>
    <th class="gram-art">Congiunzioni</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td>Copulative</td><td>e, anche, inoltre, né...né</td><td><em>Marco e Luca sono amici.</em></td></tr>
  <tr><td>Disgiuntive</td><td>o, oppure, o...o</td><td><em>Vieni o resti?</em></td></tr>
  <tr><td>Avversative</td><td>ma, però, tuttavia, anzi, eppure</td><td><em>Voglio venire, ma non posso.</em></td></tr>
  <tr><td>Conclusive</td><td>quindi, dunque, perciò, allora</td><td><em>Era tardi, quindi siamo andati.</em></td></tr>
  <tr><td>Esplicative</td><td>cioè, ossia, ovvero, infatti</td><td><em>È italiano, cioè parla italiano.</em></td></tr>
</table>

<h4>Proposizioni causali (perché, causa)</h4>
<p>Indicano la <strong>causa</strong> dell'azione principale. Si usano con l'<strong>indicativo</strong>:</p>
<ul>
  <li><strong>perché, poiché, siccome, dato che, visto che</strong></li>
  <li><em>Studio molto <strong>perché</strong> voglio imparare.</em></li>
  <li><em><strong>Siccome</strong> era tardi, siamo partiti.</em></li>
  <li><em><strong>Dato che</strong> non sei venuto, ho finito da solo.</em></li>
</ul>

<h4>Proposizioni temporali (quando, tempo)</h4>
<p>Indicano il <strong>tempo</strong> dell'azione. Si usano con l'<strong>indicativo</strong>:</p>
<ul>
  <li><strong>quando, mentre, appena, dopo che, prima che, finché</strong></li>
  <li><em><strong>Quando</strong> arrivo, ti chiamo.</em></li>
  <li><em><strong>Appena</strong> ho finito, sono uscito.</em></li>
  <li><em><strong>Mentre</strong> studiavo, ascoltavo musica.</em></li>
  <li><em><strong>Prima che</strong> arrivi, devo pulire.</em> (+ congiuntivo)</li>
</ul>

<h4>Proposizioni finali (per, scopo)</h4>
<p>Indicano lo <strong>scopo</strong> dell'azione. Si usano con il <strong>congiuntivo</strong> (o infinito se stesso soggetto):</p>
<ul>
  <li><strong>affinché, perché, in modo che, così che</strong></li>
  <li><em>Parlo lentamente <strong>affinché</strong> tu possa capire.</em> (soggetti diversi → congiuntivo)</li>
  <li><em>Studio <strong>per</strong> imparare.</em> (stesso soggetto → infinito)</li>
  <li><em>Lo scrivo <strong>in modo che</strong> tu lo ricordi.</em></li>
</ul>

<h4>Proposizioni concessive (benché, sebbene)</h4>
<p>Esprimono una <strong>concessione</strong> — un ostacolo che non impedisce l'azione. Si usano con il <strong>congiuntivo</strong>:</p>
<ul>
  <li><strong>benché, sebbene, nonostante (che), malgrado, anche se, pur + gerundio</strong></li>
  <li><em><strong>Benché</strong> fosse tardi, abbiamo continuato.</em></li>
  <li><em><strong>Nonostante</strong> la pioggia, siamo usciti.</em></li>
  <li><em><strong>Anche se</strong> era stanco, ha lavorato.</em> (+ indicativo)</li>
</ul>

<h4>Altre proposizioni subordinate importanti</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Altre subordinate</th>
  </tr>
  <tr>
    <th class="gram-art">Tipo</th>
    <th class="gram-art">Congiunzioni</th>
    <th class="gram-art">Modo verbale</th>
  </tr>
  <tr><td>Condizionale</td><td>se, a condizione che, purché</td><td>indicativo / congiuntivo</td></tr>
  <tr><td>Consecutiva</td><td>così...che, tanto...che</td><td>indicativo</td></tr>
  <tr><td>Modale</td><td>come, come se, nel modo in cui</td><td>indicativo / congiuntivo</td></tr>
  <tr><td>Comparativa</td><td>come, più...di quanto, meno...di quanto</td><td>indicativo / congiuntivo</td></tr>
</table>

<h4>Dialogo: Una decisione difficile</h4>
<p><strong>Elena:</strong> Ho deciso di partire per la Spagna, sebbene non parli ancora bene lo spagnolo.<br>
<strong>Fabio:</strong> Perché vuoi andare proprio lì?<br>
<strong>Elena:</strong> Siccome voglio imparare la lingua, ho pensato di viverci un anno.<br>
<strong>Fabio:</strong> Quando parti?<br>
<strong>Elena:</strong> Appena finisco il corso qui, quindi tra due mesi.<br>
<strong>Fabio:</strong> Ma non hai paura?<br>
<strong>Elena:</strong> Certo, però voglio farlo affinché la mia vita cambi. Eppure capisco le tue preoccupazioni.</p>"""

lez["exercicios"] = [
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Causali. Unisci le frasi con PERCHÉ, SICCOME o DATO CHE:\n1. Era stanco. È andato a letto presto. → ___\n2. Non ha studiato. Non ha superato l'esame. → ___\n3. Ha piovuto. Siamo rimasti in casa. → ___",
        "resposta": "1. Siccome/Dato che era stanco, è andato a letto presto | 2. Non ha superato l'esame perché non ha studiato | 3. Siamo rimasti in casa perché/dato che ha piovuto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Temporali. Completa con QUANDO, MENTRE, APPENA o PRIMA CHE:\n1. ___ arrivo, ti chiamo.\n2. ___ studiavo, ascoltavo musica.\n3. ___ finisco, esco.\n4. ___ parta, devo salutarla.",
        "resposta": "1. Quando | 2. Mentre | 3. Appena | 4. Prima che"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Finali. Completa con AFFINCHÉ + congiuntivo o PER + infinito:\n1. Studio molto ___ imparare. (stesso soggetto)\n2. Parlo lentamente ___ tu possa capire. (soggetti diversi)\n3. Ho comprato un libro ___ leggere in vacanza. (stesso soggetto)\n4. Le ho spiegato tutto ___ lei capisse. (soggetti diversi)",
        "resposta": "1. per | 2. affinché | 3. per | 4. affinché / in modo che"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Concessive. Completa con BENCHÉ, SEBBENE o NONOSTANTE + congiuntivo:\n1. ___ fosse tardi, abbiamo continuato.\n2. ___ la fatica, ha finito il lavoro.\n3. ___ non parli bene, si fa capire.\n4. ___ avesse poco tempo, ha aiutato tutti.",
        "resposta": "1. Benché/Sebbene | 2. Nonostante | 3. Benché/Sebbene | 4. Benché/Sebbene"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Coordinanti. Scegli la congiunzione giusta:\n1. Vuoi tè ___ caffè? (scelta)\n2. Era stanco ___ ha continuato. (opposizione)\n3. Non ho mangiato ___ bevuto niente. (negazione doppia)\n4. Era tardi, ___ siamo andati a casa. (conclusione)",
        "resposta": "1. o/oppure | 2. ma/però | 3. né | 4. quindi/dunque/perciò"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Identifica il tipo di proposizione:\n1. Studio affinché tu capisca. → ___\n2. Quando arrivi, chiamami. → ___\n3. Benché sia tardi, resto. → ___\n4. Non mangio perché non ho fame. → ___",
        "resposta": "1. finale | 2. temporale | 3. concessiva | 4. causale"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Modo verbale corretto:\n1. Benché ___ (essere) stanco, lavora. → ___\n2. Siccome ___ (avere) fame, ho mangiato. → ___\n3. Affinché tu ___ (capire), spiego ancora. → ___\n4. Appena ___ (finire), ci sentiamo. → ___",
        "resposta": "1. sia (congiuntivo) | 2. avevo (indicativo) | 3. capisca (congiuntivo) | 4. finisco (indicativo)"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Consecutiva. Trasforma:\n1. Era così stanco che non riusciva ad alzarsi. → Era ___ stanco ___ non riusciva ad alzarsi.\n2. Ha mangiato talmente tanto che si sentiva male. → Ha mangiato ___ tanto ___ si sentiva male.",
        "resposta": "1. così / che | 2. talmente / che"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "\"Non ho mangiato ___ dormito.\" (negazione doppia)",
        "opcoes": ["o...o", "né...né", "ma...ma", "e...e"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Era tardi, ___ siamo partiti.\" (conclusione)",
        "opcoes": ["però", "quindi", "eppure", "sebbene"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Studio molto ___ imparare.\" (stesso soggetto, scopo)",
        "opcoes": ["affinché", "sebbene", "per", "benché"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ fosse tardi, abbiamo continuato.\" (concessiva)",
        "opcoes": ["Perché", "Quando", "Benché", "Siccome"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ arrivo, ti chiamo.\" (temporale)",
        "opcoes": ["Perché", "Benché", "Quando", "Affinché"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Le proposizioni causali si usano con:",
        "opcoes": ["il congiuntivo", "l'indicativo", "l'infinito", "il gerundio"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Parlo lentamente ___ tu possa capire.\" (soggetti diversi, scopo)",
        "opcoes": ["per", "affinché", "sebbene", "appena"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ sia tardi, esco lo stesso.\" (concessiva)",
        "opcoes": ["Siccome", "Perché", "Sebbene", "Appena"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ studiavo, ascoltavo musica.\" (azioni contemporanee)",
        "opcoes": ["Appena", "Quando", "Mentre", "Prima che"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "BENCHÉ e SEBBENE reggono:",
        "opcoes": ["l'indicativo", "il congiuntivo", "l'infinito", "il condizionale"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Voglio venire, ___ non posso.\" (opposizione)",
        "opcoes": ["quindi", "siccome", "ma", "sebbene"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ finisco, esco.\" (subito dopo)",
        "opcoes": ["Quando", "Appena", "Prima che", "Finché"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Era così stanco ___ non riusciva ad alzarsi.\" (consecutiva)",
        "opcoes": ["affinché", "quindi", "che", "sebbene"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "SICCOME introduce una proposizione:",
        "opcoes": ["finale", "causale", "concessiva", "temporale"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non ho studiato ___ non ho superato l'esame.\" (conseguenza)",
        "opcoes": ["ma", "però", "quindi", "sebbene"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ parta, devo salutarla.\" (anteriorità temporale + congiuntivo)",
        "opcoes": ["Quando", "Appena", "Prima che", "Dopo che"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale coppia di congiunzioni è COORDINANTE?",
        "opcoes": ["benché / sebbene", "ma / però", "affinché / perché", "quando / appena"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ non parli bene, si fa capire.\" (azione nonostante l'ostacolo)",
        "opcoes": ["Siccome", "Sebbene", "Affinché", "Perché"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Vuoi tè ___ caffè?\" (alternativa)",
        "opcoes": ["e", "né", "o", "ma"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "DATO CHE introduce una proposizione:",
        "opcoes": ["temporale", "concessiva", "causale", "finale"],
        "resposta": 2
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Benché era tardi, abbiamo continuato.\n2. Studio per affinché imparo.\n3. Siccome è stanco, quindi va a letto.\n4. Appena finisca, esco. (temporale con indicativo)\n5. Era stanco ma ha lavorato — è corretto?",
        "resposta": "1. fosse (congiuntivo) | 2. Studio per imparare / Studio affinché impari | 3. togliere 'quindi' (siccome già introduce la causa) | 4. finisco (indicativo) | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Parlo lentamente per tu possa capire.\n2. Sebbene fosse stanco, lavora — è corretto?\n3. Né mangio né dormo — è corretto?\n4. È tardi, dunque andiamo — è corretto?",
        "resposta": "1. affinché tu possa capire | 2. SÌ, corretto | 3. SÌ, corretto | 4. SÌ, corretto"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
