import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXV"), None)
if lez is None:
    lez = {"id": "a1-lez25", "num": "Lezione XXV", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il discorso indiretto"
lez["subtitulo"] = "Trasformare il discorso diretto in indiretto — cambiamenti di tempo, pronomi e espressioni"
lez["exemplos"] = [
    "Diretto: «Sono stanco.» → Indiretto: Ha detto che era stanco.",
    "Diretto: «Vengo domani.» → Indiretto: Ha detto che sarebbe venuto il giorno dopo.",
    "Diretto: «Ho mangiato.» → Indiretto: Ha detto che aveva mangiato.",
    "Diretto: «Vieni!» → Indiretto: Mi ha detto di venire.",
    "Diretto: «Sei pronto?» → Indiretto: Mi ha chiesto se ero pronto.",
    "Diretto: «Dove vai?» → Indiretto: Mi ha chiesto dove andassi."
]

lez["teoria"] = """<h3>Il discorso indiretto</h3>
<p>Il <strong>discorso indiretto</strong> riporta le parole di qualcuno senza citarle direttamente. La frase principale di riferimento è al <strong>passato</strong> nella maggior parte dei casi.</p>

<h4>Verbi introduttori</h4>
<p>I verbi più usati per introdurre il discorso indiretto sono:</p>
<ul>
  <li><strong>dire, affermare, rispondere, spiegare, aggiungere</strong> → che + indicativo/congiuntivo</li>
  <li><strong>chiedere, domandare, voler sapere</strong> → se (sì/no) / parola interrogativa</li>
  <li><strong>ordinare, chiedere, pregare</strong> → di + infinito</li>
</ul>

<h4>Cambiamenti dei tempi verbali</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Discorso diretto → Discorso indiretto (verbo principale al passato)</th>
  </tr>
  <tr>
    <th class="gram-art">Discorso diretto</th>
    <th class="gram-art">Discorso indiretto</th>
  </tr>
  <tr><td>Presente: <em>«Sono stanco.»</em></td><td>Imperfetto: <em>...che era stanco.</em></td></tr>
  <tr><td>Passato prossimo: <em>«Ho mangiato.»</em></td><td>Trapassato: <em>...che aveva mangiato.</em></td></tr>
  <tr><td>Futuro: <em>«Verrò domani.»</em></td><td>Condizionale passato: <em>...che sarebbe venuto.</em></td></tr>
  <tr><td>Imperfetto: <em>«Lavoravo molto.»</em></td><td>Imperfetto: <em>...che lavorava molto.</em></td></tr>
  <tr><td>Condizionale presente: <em>«Verrei.»</em></td><td>Condizionale passato: <em>...che sarebbe venuto.</em></td></tr>
  <tr><td>Imperativo: <em>«Vieni!»</em></td><td>di + infinito: <em>...di venire.</em></td></tr>
</table>

<h4>Cambiamenti di pronomi e aggettivi</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Cambiamenti pronominali</th>
  </tr>
  <tr>
    <th class="gram-art">Discorso diretto</th>
    <th class="gram-art">Discorso indiretto</th>
  </tr>
  <tr><td>io → lui/lei</td><td>tu → io / lui/lei (secondo contesto)</td></tr>
  <tr><td>mio → suo</td><td>tuo → mio / suo</td></tr>
  <tr><td>mi → gli/le/si</td><td>ti → mi / gli/le</td></tr>
</table>

<h4>Cambiamenti di espressioni di tempo e luogo</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Espressioni temporali e locali</th>
  </tr>
  <tr>
    <th class="gram-art">Discorso diretto</th>
    <th class="gram-art">Discorso indiretto</th>
  </tr>
  <tr><td>oggi</td><td>quel giorno</td></tr>
  <tr><td>domani</td><td>il giorno dopo / l'indomani</td></tr>
  <tr><td>ieri</td><td>il giorno prima / il giorno precedente</td></tr>
  <tr><td>questa settimana</td><td>quella settimana</td></tr>
  <tr><td>qui / qua</td><td>lì / là</td></tr>
  <tr><td>questo</td><td>quello</td></tr>
  <tr><td>adesso / ora</td><td>in quel momento / allora</td></tr>
</table>

<h4>Discorso indiretto con domande</h4>
<p>Quando si riporta una domanda:</p>
<ul>
  <li><strong>Domanda sì/no</strong>: si usa <em>se</em><br>
  <em>«Sei pronto?» → Mi ha chiesto <strong>se</strong> ero pronto.</em></li>
  <li><strong>Domanda con parola interrogativa</strong>: si mantiene la parola interrogativa<br>
  <em>«Dove vai?» → Mi ha chiesto <strong>dove</strong> andassi.</em><br>
  <em>«Quando arrivi?» → Ha domandato <strong>quando</strong> arrivassi.</em></li>
</ul>

<h4>Dialogo: Una notizia importante</h4>
<p><strong>Marco racconta ad Anna:</strong><br>
"Ieri ho incontrato Giulia. Mi ha detto che era molto felice perché aveva trovato un nuovo lavoro. Ha aggiunto che avrebbe iniziato la settimana dopo. Mi ha chiesto se conoscevo la sua nuova azienda. Le ho risposto che non ne sapevo niente ma che le auguravo buona fortuna. Mi ha ringraziato e mi ha detto di salutarti."</p>
<p><em>(Le parole originali di Giulia: «Sono molto felice perché ho trovato un nuovo lavoro. Inizierò la settimana prossima. Conosci la mia nuova azienda? Saluta Anna!»)</em></p>"""

lez["exercicios"] = [
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Trasforma al discorso indiretto (verbo al passato):\n1. «Sono stanco.» → Ha detto che ___.\n2. «Ho mangiato.» → Ha detto che ___.\n3. «Verrò domani.» → Ha detto che ___.\n4. «Lavoro molto.» → Ha detto che ___.",
        "resposta": "1. era stanco | 2. aveva mangiato | 3. sarebbe venuto il giorno dopo | 4. lavorava molto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Trasforma imperativo al discorso indiretto:\n1. «Studia!» → Mi ha detto ___.\n2. «Vieni subito!» → Mi ha ordinato ___.\n3. «Non uscire!» → Mi ha detto ___.\n4. «Aspetta qui!» → Mi ha chiesto ___.",
        "resposta": "1. di studiare | 2. di venire subito | 3. di non uscire | 4. di aspettare lì"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Domande indirette con SE:\n1. «Sei pronto?» → Mi ha chiesto ___.\n2. «Hai finito?» → Ha domandato ___.\n3. «Vieni alla festa?» → Mi ha chiesto ___.\n4. «Parli italiano?» → Ha voluto sapere ___.",
        "resposta": "1. se ero pronto | 2. se avevo finito | 3. se venivo alla festa | 4. se parlavo italiano"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Domande indirette con parola interrogativa:\n1. «Dove vai?» → Mi ha chiesto ___.\n2. «Quando arrivi?» → Ha domandato ___.\n3. «Come stai?» → Mi ha chiesto ___.\n4. «Perché sei in ritardo?» → Ha voluto sapere ___.",
        "resposta": "1. dove andassi | 2. quando arrivassi | 3. come stavo | 4. perché ero in ritardo"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Cambia le espressioni di tempo:\n1. «Vengo oggi.» → Ha detto che veniva ___.\n2. «L'ho visto ieri.» → Ha detto che l'aveva visto ___.\n3. «Partirò domani.» → Ha detto che sarebbe partito ___.\n4. «Lavoro qui.» → Ha detto che lavorava ___.",
        "resposta": "1. quel giorno | 2. il giorno prima | 3. il giorno dopo / l'indomani | 4. lì"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Discorso diretto completo. Riporta al discorso indiretto:\n«Sono molto felice perché ho trovato un lavoro. Inizierò lunedì.»\nHa detto che ___ molto felice perché ___ un lavoro e che ___ il lunedì successivo.",
        "resposta": "era / aveva trovato / avrebbe iniziato"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Ricostruisci il discorso diretto originale:\nHa detto che era stanco e che avrebbe dormito quel pomeriggio.\nDiscorso diretto originale: «___ e ___.»",
        "resposta": "Sono stanco e dormirò questo pomeriggio."
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Discorso indiretto misto:\n«Non so se vengo alla festa. Dipende dal lavoro. Se posso, ti chiamo.»\nHa detto che non sapeva ___ alla festa, che dipendeva dal lavoro e che, se ___, mi avrebbe chiamato.",
        "resposta": "se veniva / poteva"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "«Sono stanco.» → Al discorso indiretto (passato): Ha detto che ___.",
        "opcoes": ["è stanco", "era stanco", "fosse stanco", "sarà stanco"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Ho mangiato.» → Al discorso indiretto: Ha detto che ___.",
        "opcoes": ["ha mangiato", "mangiava", "aveva mangiato", "mangi"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "«Verrò domani.» → Al discorso indiretto: Ha detto che ___.",
        "opcoes": ["verrà il giorno dopo", "sarebbe venuto il giorno dopo", "veniva il giorno dopo", "venisse il giorno dopo"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Vieni!» → Al discorso indiretto: Mi ha detto ___.",
        "opcoes": ["che vengo", "di venire", "che venga", "che venissi"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Sei pronto?» → Al discorso indiretto: Mi ha chiesto ___.",
        "opcoes": ["che ero pronto", "se ero pronto", "se fossi pronto", "perché ero pronto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Dove vai?» → Al discorso indiretto: Mi ha chiesto ___.",
        "opcoes": ["dove vai", "dove andavo", "dove andassi", "dove andrò"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Nel discorso indiretto, «oggi» diventa:",
        "opcoes": ["domani", "quel giorno", "l'indomani", "adesso"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Nel discorso indiretto, «domani» diventa:",
        "opcoes": ["quel giorno", "il giorno prima", "il giorno dopo", "questa settimana"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "«Non uscire!» → Al discorso indiretto: Mi ha detto ___.",
        "opcoes": ["che non esco", "di non uscire", "che non uscissi", "di non uscito"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il futuro nel discorso diretto diventa ___ nel discorso indiretto al passato.",
        "opcoes": ["imperfetto", "condizionale presente", "condizionale passato", "trapassato"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "«Lavoravo molto.» → Al discorso indiretto: Ha detto che ___.",
        "opcoes": ["lavorava molto", "aveva lavorato molto", "lavorerebbe molto", "lavorasse molto"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale verbo NON si usa per introdurre il discorso indiretto?",
        "opcoes": ["dire", "chiedere", "correre", "rispondere"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "«Quando parti?» → Al discorso indiretto: Ha chiesto ___.",
        "opcoes": ["quando parto", "quando partivo", "quando partissi", "se parto"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Nel discorso indiretto, «qui» diventa:",
        "opcoes": ["qua", "là / lì", "qui stesso", "vicino"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Ho trovato lavoro!» → Ha detto che ___.",
        "opcoes": ["ha trovato lavoro", "aveva trovato lavoro", "avrebbe trovato lavoro", "trovava lavoro"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Per le domande sì/no nel discorso indiretto si usa:",
        "opcoes": ["che", "se", "perché", "dove"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Studia di più!» → Mi ha detto ___.",
        "opcoes": ["che studi di più", "di studiare di più", "che studiassi di più", "se studio di più"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il passato prossimo nel discorso indiretto (al passato) diventa:",
        "opcoes": ["imperfetto", "trapassato prossimo", "passato remoto", "condizionale passato"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Questo» nel discorso indiretto diventa:",
        "opcoes": ["codesto", "quello", "quel", "tale"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "«Come ti chiami?» → Ha chiesto ___.",
        "opcoes": ["come mi chiamo", "come mi chiamassi", "come mi chiamavo", "se mi chiamo"],
        "resposta": 2
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Ha detto che è stanco. (verbo principale al passato)\n2. Mi ha detto di vengo subito.\n3. Ha chiesto se venivo alla festa — è corretto?\n4. Ha detto che verrà domani. (futuro → condizionale passato)\n5. Mi ha chiesto dove vado.",
        "resposta": "1. era | 2. di venire | 3. SÌ, corretto | 4. sarebbe venuto il giorno dopo | 5. dove andassi"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Ha detto che aveva trovato lavoro — è corretto?\n2. Mi ha chiesto se sono pronto. (concordanza al passato)\n3. Ha detto che veniva oggi. (oggi → quel giorno)\n4. Mi ha ordinato di non uscissi.",
        "resposta": "1. SÌ, corretto | 2. se ero pronto | 3. quel giorno | 4. di non uscire"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
