import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXVII"), None)
if lez is None:
    lez = {"id": "a1-lez27", "num": "Lezione XXVII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Gli aggettivi e i pronomi indefiniti"
lez["subtitulo"] = "Qualcuno, nessuno, tutto, ogni, qualcosa, niente e altri indefiniti"
lez["exemplos"] = [
    "Qualcuno ha chiamato mentre eri fuori.",
    "Non ho visto nessuno al parco.",
    "Tutti sono arrivati in orario.",
    "Ogni studente deve portare il libro.",
    "Ho bisogno di qualcosa da mangiare.",
    "Non c'è niente di interessante in TV."
]

lez["teoria"] = """<h3>Gli aggettivi e i pronomi indefiniti</h3>
<p>Gli <strong>indefiniti</strong> indicano persone, cose o quantità in modo non preciso. Possono funzionare come <strong>aggettivi</strong> (accompagnano un sostantivo) o come <strong>pronomi</strong> (sostituiscono un sostantivo).</p>

<h4>Principali indefiniti</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Indefiniti — schema</th>
  </tr>
  <tr>
    <th class="gram-art">Indefinito</th>
    <th class="gram-art">Uso</th>
    <th class="gram-art">Esempio aggettivo</th>
    <th class="gram-art">Esempio pronome</th>
  </tr>
  <tr><td><strong>tutto/a/i/e</strong></td><td>agg. + pron.</td><td><em>Tutti i bambini giocano.</em></td><td><em>Tutti sono arrivati.</em></td></tr>
  <tr><td><strong>ogni</strong></td><td>solo agg. (invariabile)</td><td><em>Ogni giorno studio.</em></td><td>—</td></tr>
  <tr><td><strong>qualche</strong></td><td>solo agg. (invariabile, sing.)</td><td><em>Ho comprato qualche libro.</em></td><td>—</td></tr>
  <tr><td><strong>qualcuno/a</strong></td><td>solo pron.</td><td>—</td><td><em>Qualcuno ha telefonato.</em></td></tr>
  <tr><td><strong>qualcosa</strong></td><td>solo pron. (invariabile)</td><td>—</td><td><em>Ho mangiato qualcosa.</em></td></tr>
  <tr><td><strong>nessuno/a</strong></td><td>agg. + pron.</td><td><em>Nessun problema.</em></td><td><em>Non è venuto nessuno.</em></td></tr>
  <tr><td><strong>niente / nulla</strong></td><td>solo pron. (invariabile)</td><td>—</td><td><em>Non ho capito niente.</em></td></tr>
  <tr><td><strong>molto/a/i/e</strong></td><td>agg. + pron.</td><td><em>Ho molti amici.</em></td><td><em>Molti preferiscono il mare.</em></td></tr>
  <tr><td><strong>poco/a/pochi/poche</strong></td><td>agg. + pron.</td><td><em>Ho pochi soldi.</em></td><td><em>Pochi capiscono.</em></td></tr>
  <tr><td><strong>troppo/a/i/e</strong></td><td>agg. + pron.</td><td><em>Ha mangiato troppa pizza.</em></td><td><em>Ne ha mangiato troppo.</em></td></tr>
  <tr><td><strong>tanto/a/i/e</strong></td><td>agg. + pron.</td><td><em>Ha tanti libri.</em></td><td><em>Ne ho tanti.</em></td></tr>
  <tr><td><strong>alcuno/a/i/e</strong></td><td>agg. + pron.</td><td><em>Alcuni studenti.</em></td><td><em>Alcuni sono partiti.</em></td></tr>
  <tr><td><strong>altro/a/i/e</strong></td><td>agg. + pron.</td><td><em>Vuoi altro caffè?</em></td><td><em>Gli altri sono in ritardo.</em></td></tr>
  <tr><td><strong>certo/a/i/e</strong></td><td>agg. (prima del sost.)</td><td><em>Certi giorni sono difficili.</em></td><td>—</td></tr>
</table>

<h4>TUTTO — forme e concordanza</h4>
<p><strong>Tutto</strong> si declina come un aggettivo regolare e vuole l'articolo determinativo:</p>
<ul>
  <li><em><strong>tutto il</strong> giorno — <strong>tutta la</strong> notte</em></li>
  <li><em><strong>tutti i</strong> giorni — <strong>tutte le</strong> notti</em></li>
  <li><em><strong>Tutti</strong> sono venuti.</em> (pronome)</li>
</ul>

<h4>OGNI vs. QUALCHE vs. ALCUNI</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="3">Confronto: ogni / qualche / alcuni</th>
  </tr>
  <tr>
    <th class="gram-art">Parola</th>
    <th class="gram-art">Caratteristiche</th>
    <th class="gram-art">Esempio</th>
  </tr>
  <tr><td><strong>ogni</strong></td><td>invariabile, sempre singolare</td><td><em>Ogni studente porta il libro.</em></td></tr>
  <tr><td><strong>qualche</strong></td><td>invariabile, sempre singolare (idea di plurale)</td><td><em>Ho qualche problema. (= alcuni problemi)</em></td></tr>
  <tr><td><strong>alcuni/alcune</strong></td><td>solo plurale, variabile</td><td><em>Alcuni studenti sono arrivati tardi.</em></td></tr>
</table>

<h4>Indefiniti negativi: NESSUNO e NIENTE</h4>
<p>Con gli indefiniti negativi in posizione post-verbale, il verbo vuole la <strong>doppia negazione</strong> con <em>non</em>:</p>
<ul>
  <li><em><strong>Non</strong> è venuto <strong>nessuno</strong>.</em> / <em><strong>Nessuno</strong> è venuto.</em> (senza non)</li>
  <li><em><strong>Non</strong> ho capito <strong>niente</strong>.</em> / <em><strong>Niente</strong> mi ha colpito.</em></li>
</ul>
<p><strong>Nessuno</strong> come aggettivo si elide come l'articolo indeterminativo: <em>nessun problema, nessuna risposta</em>.</p>

<h4>QUALCOSA e NIENTE + di + aggettivo</h4>
<p>Con <em>qualcosa</em> e <em>niente</em>, l'aggettivo che segue è sempre al <strong>maschile singolare</strong> e preceduto da <strong>di</strong>:</p>
<ul>
  <li><em>Ho visto qualcosa di <strong>bello</strong>.</em></li>
  <li><em>Non c'è niente di <strong>interessante</strong>.</em></li>
  <li><em>Hai qualcosa di <strong>urgente</strong> da dirmi?</em></li>
</ul>

<h4>Dialogo: Una serata tranquilla</h4>
<p><strong>Marta:</strong> C'è qualcuno in casa?<br>
<strong>Luca:</strong> No, non c'è nessuno. Tutti sono usciti.<br>
<strong>Marta:</strong> Hai qualcosa da mangiare? Non ho mangiato niente oggi.<br>
<strong>Luca:</strong> Ho qualche avanzo in frigo. Non è niente di speciale, ma...<br>
<strong>Marta:</strong> Va bene tutto! Ogni cosa è meglio del niente.<br>
<strong>Luca:</strong> Hai ragione. Alcuni giorni è così — non trovi nulla di buono ma poi qualcosa salta fuori.</p>"""

lez["exercicios"] = [
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Scegli tra TUTTO, OGNI, QUALCHE, ALCUNI:\n1. ___ studente deve studiare. (ogni singolo)\n2. ___ libri sono interessanti. (non tutti, una parte)\n3. Ho ___ amico a Roma. (idea vaga, plurale)\n4. ___ la classe ha capito. (la classe intera)",
        "resposta": "1. Ogni | 2. Alcuni | 3. qualche | 4. Tutta"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Completa con NESSUNO/NIENTE:\n1. ___ ha risposto al telefono.\n2. Non ho fatto ___ oggi.\n3. Non c'è ___ in casa.\n4. Ho cercato ma non ho trovato ___.",
        "resposta": "1. Nessuno | 2. niente/nulla | 3. nessuno | 4. niente/nulla"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — QUALCOSA/NIENTE + DI + aggettivo. Completa:\n1. Ho visto ___ di molto bello in TV.\n2. Non c'è ___ di nuovo sotto il sole.\n3. Hai ___ di importante da dirmi?\n4. Non ho letto ___ di interessante ultimamente.",
        "resposta": "1. qualcosa | 2. niente/nulla | 3. qualcosa | 4. niente/nulla"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — TUTTO concordato. Completa:\n1. ___ (tutto + il) giorno ho lavorato.\n2. ___ (tutto + le) ragazze erano presenti.\n3. ___ (tutto + i) bambini giocavano nel parco.\n4. ___ (tutto + la) notte non ho dormito.",
        "resposta": "1. Tutto il | 2. Tutte le | 3. Tutti i | 4. Tutta la"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Doppia negazione. Trasforma:\n1. Nessuno è arrivato. → Non è arrivato ___.\n2. Niente mi piace qui. → Non mi piace ___.\n3. Nessuna risposta è giusta. → Non è giusta ___ risposta.",
        "resposta": "1. nessuno | 2. niente/nulla | 3. nessuna"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Scegli l'indefinito corretto:\n1. Ho ___ (molto/tanto) voglia di dormire.\n2. ___ (pochi/poco) studenti hanno capito.\n3. Ha mangiato ___ (troppo/troppa) pizza.\n4. ___ (altri/altro) caffè?",
        "resposta": "1. molta | 2. Pochi | 3. troppa | 4. Altro"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Pronome o aggettivo? Identifica la funzione:\n1. Tutti i miei amici sono simpatici. → ___\n2. Tutti sono già arrivati. → ___\n3. Nessun problema! → ___\n4. Non è venuto nessuno. → ___",
        "resposta": "1. aggettivo | 2. pronome | 3. aggettivo | 4. pronome"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Forma frasi complete con gli indefiniti dati:\n1. qualcuno / chiamare / ieri → ___\n2. niente / capire / io → ___\n3. tutti / arrivare / in orario → ___\n4. qualcosa / mangiare / volere / tu → ___",
        "resposta": "1. Qualcuno ha chiamato ieri | 2. Non ho capito niente | 3. Tutti sono arrivati in orario | 4. Vuoi mangiare qualcosa?"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "\"___ studente porta il libro.\" Quale indefinito è corretto?",
        "opcoes": ["Tutti", "Qualche", "Ogni", "Alcuni"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non ho visto ___ al parco.\"",
        "opcoes": ["qualcuno", "nessuno", "alcuno", "niente"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale frase è corretta con QUALCOSA?",
        "opcoes": [
            "Ho visto qualcosa bella.",
            "Ho visto qualcosa di bella.",
            "Ho visto qualcosa di bello.",
            "Ho visto qualcosa bello."
        ],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ le ragazze erano presenti.\" (tutte quante)",
        "opcoes": ["Tutta", "Tutto", "Tutte", "Tutti"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "QUALCHE si usa sempre con:",
        "opcoes": ["il plurale", "il singolare", "solo femminile", "solo maschile"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non c'è ___ di interessante in TV.\"",
        "opcoes": ["qualcosa", "niente", "nessuno", "alcuno"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ studenti hanno capito.\" (una parte, non tutti)",
        "opcoes": ["Ogni", "Qualche", "Alcuni", "Tutto"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si elide NESSUNO davanti a un sostantivo maschile che inizia per consonante?",
        "opcoes": ["nessuno problema", "nessun problema", "nessuno' problema", "nessuni problema"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ho ___ (molto) amici a Milano.\"",
        "opcoes": ["molto", "molti", "molta", "molte"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale frase usa la doppia negazione correttamente?",
        "opcoes": [
            "Non è venuto nessuno.",
            "È venuto nessuno.",
            "Non è venuto non nessuno.",
            "Nessuno non è venuto."
        ],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "QUALCUNO si usa come:",
        "opcoes": ["solo aggettivo", "solo pronome", "sia aggettivo che pronome", "avverbio"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ha mangiato ___ (troppo) torta.\"",
        "opcoes": ["troppo", "troppi", "troppa", "troppe"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ i libri sono stati letti.\" (tutti quanti)",
        "opcoes": ["Tutto", "Tutti", "Tutta", "Tutte"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Vuoi ___ caffè?\" (ancora un po')",
        "opcoes": ["altro", "altri", "altra", "alcune"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "OGNI è invariabile e si usa:",
        "opcoes": ["solo al plurale", "solo al singolare", "sia singolare che plurale", "solo con femminili"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Non ho fatto niente\" equivale a:",
        "opcoes": ["Ho fatto niente.", "Niente ho fatto.", "Niente non ho fatto.", "Non ho fatto nulla."],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ (pochi) persone capiscono questa regola.\"",
        "opcoes": ["Poco", "Pochi", "Poche", "Alcune poche"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "\"Ho qualche ___ da risolvere.\" (problema — singolare o plurale?)",
        "opcoes": ["problemi", "problema", "problemata", "problemas"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "\"___ (certo) giorni sono difficili.\"",
        "opcoes": ["Certo", "Certi", "Certa", "Certuni"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale coppia è corretta?",
        "opcoes": [
            "qualcosa bella / niente bello",
            "qualcosa di bella / niente di bello",
            "qualcosa di bello / niente di bello",
            "qualcosa bello / niente bella"
        ],
        "resposta": 2
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Ogni studenti devono studiare.\n2. Ho visto qualcosa bella.\n3. Non è venuto nessuno — è corretto?\n4. Qualche libri sono interessanti.\n5. Ho mangiato troppo pizza.",
        "resposta": "1. Ogni studente deve | 2. qualcosa di bello | 3. SÌ, corretto | 4. Qualche libro è / Alcuni libri sono | 5. troppa pizza"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Tutti le notti non dormo. (tutti → tutta)\n2. Nessun problema — è corretto?\n3. Non ho trovato niente di interessante — è corretto?\n4. Alcuni studente è arrivato tardi.",
        "resposta": "1. Tutte le notti | 2. SÌ, corretto | 3. SÌ, corretto | 4. Alcuni studenti sono arrivati tardi"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
