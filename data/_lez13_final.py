import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XIII"), None)
if lez is None:
    lez = {"id": "a1-lez13", "num": "Lezione XIII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il condizionale semplice e composto"
lez["subtitulo"] = "Formazione e usi del condizionale presente e passato"

lez["teoria"] = """\
## Una scampagnata

Era domenica mattina e Giorgio aveva finalmente un giorno libero. Avrebbe voluto andare in campagna con i suoi amici, ma non sapeva se erano liberi. Ha telefonato a Luisa e le ha detto: "Oggi farebbe bello. Saresti libera per una scampagnata?" Luisa ha risposto che sarebbe venuta volentieri, ma che prima avrebbe dovuto finire di studiare. Giorgio ha detto che avrebbero potuto partire verso mezzogiorno. Poi ha chiamato Carlo e Marina, che hanno detto di sì subito. Alla fine sono partiti in quattro e hanno passato una bella giornata in campagna. Avrebbero voluto restare anche a cena, ma Marina aveva detto che avrebbe dovuto essere a casa entro le otto.

---

## A Il condizionale semplice (presente)

Il condizionale semplice si forma con il **tema del futuro** + desinenze: **-ei, -esti, -ebbe, -emmo, -este, -ebbero**.

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th class="gram-genere">I -ARE (parlare)</th><th class="gram-genere">II -ERE (prendere)</th><th class="gram-genere">III -IRE (partire)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>parler<strong>ei</strong></td><td>prenderr<strong>ei</strong></td><td>partir<strong>ei</strong></td></tr>
<tr><td class="gram-art">tu</td><td>parler<strong>esti</strong></td><td>prenderr<strong>esti</strong></td><td>partir<strong>esti</strong></td></tr>
<tr><td class="gram-art">lui/lei/Lei</td><td>parler<strong>ebbe</strong></td><td>prenderr<strong>ebbe</strong></td><td>partir<strong>ebbe</strong></td></tr>
<tr><td class="gram-art">noi</td><td>parler<strong>emmo</strong></td><td>prenderr<strong>emmo</strong></td><td>partir<strong>emmo</strong></td></tr>
<tr><td class="gram-art">voi</td><td>parler<strong>este</strong></td><td>prenderr<strong>este</strong></td><td>partir<strong>este</strong></td></tr>
<tr><td class="gram-art">loro</td><td>parler<strong>ebbero</strong></td><td>prenderr<strong>ebbero</strong></td><td>partir<strong>ebbero</strong></td></tr>
</tbody>
</table>

---

## B Condizionale irregolare

I verbi irregolari al condizionale usano lo stesso tema del futuro irregolare:

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">infinito</th><th class="gram-art">tema futuro/condiz.</th><th class="gram-art">io</th><th class="gram-art">lui/lei</th></tr>
</thead>
<tbody>
<tr><td>essere</td><td>sar-</td><td>sarei</td><td>sarebbe</td></tr>
<tr><td>avere</td><td>avr-</td><td>avrei</td><td>avrebbe</td></tr>
<tr><td>andare</td><td>andr-</td><td>andrei</td><td>andrebbe</td></tr>
<tr><td>venire</td><td>verr-</td><td>verrei</td><td>verrebbe</td></tr>
<tr><td>fare</td><td>far-</td><td>farei</td><td>farebbe</td></tr>
<tr><td>dovere</td><td>dovr-</td><td>dovrei</td><td>dovrebbe</td></tr>
<tr><td>potere</td><td>potr-</td><td>potrei</td><td>potrebbe</td></tr>
<tr><td>volere</td><td>vorr-</td><td>vorrei</td><td>vorrebbe</td></tr>
<tr><td>sapere</td><td>sapr-</td><td>saprei</td><td>saprebbe</td></tr>
<tr><td>tenere</td><td>terr-</td><td>terrei</td><td>terrebbe</td></tr>
<tr><td>rimanere</td><td>rimarr-</td><td>rimarrei</td><td>rimarrebbe</td></tr>
</tbody>
</table>

---

## C Il condizionale composto (passato)

Si forma con il **condizionale di ESSERE o AVERE** + **participio passato**:

- Avrei **mangiato** volentieri. (avere)
- Sarei **partito/a** prima. (essere)
- Mi sarei **alzato/a** tardi. (riflessivo)

---

## D Usi del condizionale

**1. Desiderio o richiesta cortese:**
- **Vorrei** un caffè, per favore.
- **Potrebbe** ripetere, per favore?
- **Mi daresti** un'informazione?

**2. Ipotesi (con SE):**
- *Se avessi tempo, **verrei** con te.*
- *Se potessi, **parterei** subito.*

**3. Notizia non confermata (condizionale giornalistico):**
- Il presidente **avrebbe** dichiarato che...
- Secondo le notizie, i due **sarebbero** in fuga.

**4. Nel discorso indiretto** (futuro nel passato):
- Marco ha detto: "Verrò domani." → Marco ha detto che **sarebbe venuto** il giorno dopo.
- Luisa ha detto: "Studierò domani." → Luisa ha detto che **avrebbe studiato** il giorno dopo.

---

## Conversazione — In un negozio di scarpe

— Buongiorno, desidero.
— Buongiorno. Vorrei vedere quelle scarpe marroni in vetrina.
— Che numero porta?
— Porto il 40, ma dipende dalla scarpa. Potrei provarle un 39 e un 40?
— Certo, signora. Un momento. Eccole. Come Le stanno?
— Il 39 è un po' stretto. Preferirei il 40.
— Sì, il 40 Le va molto meglio. Come Le sembrano?
— Mi piacciono molto. Quanto costano?
— Ottantadue euro.
— Hmm, mi sembrerebbero un po' care. Non ci sarebbe uno sconto?
— Mi dispiace, sono già in promozione. Ma potremmo offrirLe anche questo modello, simile ma più economico: cinquantacinque euro.
— Lo proverei volentieri. Sì, questi mi piacciono di più. Li prendo.
— Benissimo. Li metto in una scatola?

---

## Vocabolario sistematico — Gli animali domestici

Il **cane** è considerato il migliore amico dell'uomo. La **gatta** ama stare in casa e fa le fusa quando è contenta. Il **coniglio** è tenero e docile. Il **criceto** è piccolo e vive in una gabbia. Il **pappagallo** può imitare la voce umana. La **tartaruga** è lenta ma può vivere molto a lungo. Il **pesce rosso** vive in acquario. L'**uccellino** canta dalla mattina.

**Verbi utili:** abbaiare (il cane), miagolare (il gatto), fare le fusa, graffiare, mordere, accarezzare, addestrare, nutrire, portare a spasso.

---

## Osservare — L'uso di TOCCARE (impersonale)

**Toccare** si usa in modo impersonale per indicare un obbligo o una necessità:

| struttura | esempio |
|---|---|
| tocca + infinito | Tocca lavorare. (= si deve lavorare) |
| tocca a + persona + infinito | Tocca a me pagare. |
| è toccato a + persona + infinito | È toccato a lui farlo. |

- *Stasera tocca a te cucinare.*
- *Ieri mi è toccato aspettare un'ora.*
- *A chi tocca lavare i piatti?*
"""

lez["exemplos"] = [
    "Vorrei un caffè, per favore. (richiesta cortese)",
    "Potrebbe ripetere più lentamente? (richiesta formale)",
    "Se avessi tempo, verrei con te. (ipotesi)",
    "Ha detto che sarebbe venuto domani. (futuro nel passato)",
    "Mi sarei alzata prima, ma avevo sonno. (condiz. composto riflessivo)",
]

EX = []

# Domande sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Una scampagnata:\n1. Cosa avrebbe voluto fare Giorgio la domenica?\n2. A chi ha telefonato per primo?\n3. Perché Luisa non poteva partire subito?\n4. A che ora hanno deciso di partire?\n5. Chi altro è venuto con loro?\n6. Perché non sono rimasti a cena?",
    "resposta": "1. Avrebbe voluto andare in campagna con i suoi amici.\n2. Ha telefonato a Luisa per prima.\n3. Perché avrebbe dovuto finire di studiare prima.\n4. Avrebbero potuto partire verso mezzogiorno.\n5. Sono venuti anche Carlo e Marina.\n6. Perché Marina aveva detto che avrebbe dovuto essere a casa entro le otto.",
    "explicacao": "Uso del condizionale composto nel discorso indiretto passato: avrebbe voluto, avrebbe dovuto, sarebbero potuti."
})

# Esercizio 1
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Coniugare al condizionale semplice:\n1. io / parlare\n2. tu / prendere\n3. lui / partire\n4. noi / essere\n5. voi / avere\n6. loro / andare\n7. io / venire\n8. tu / fare\n9. lei / dovere\n10. loro / volere\n11. noi / potere\n12. io / sapere",
    "resposta": "1. parlerei\n2. prenderesti\n3. partirebbe\n4. saremmo\n5. avreste\n6. andrebbero\n7. verrei\n8. faresti\n9. dovrebbe\n10. vorrebbero\n11. potremmo\n12. saprei",
    "explicacao": "Condizionale = tema futuro + -ei/-esti/-ebbe/-emmo/-este/-ebbero. Irregolari: sar-, avr-, andr-, verr-, far-, dovr-, potr-, vorr-, sapr-."
})

# Esercizio 2 - cortesia
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Trasformare in forma cortese usando il condizionale:\n1. Voglio un bicchiere d'acqua.\n2. Puoi aiutarmi?\n3. Mi dai il sale, per favore?\n4. Vuoi venire con me?\n5. Devo parlare con il direttore.\n6. Sai dov'è la stazione?\n7. Posso entrare?\n8. Vuoi prendere un caffè?",
    "resposta": "1. Vorrei un bicchiere d'acqua.\n2. Potresti aiutarmi?\n3. Mi daresti il sale, per favore?\n4. Vorresti venire con me?\n5. Dovrei parlare con il direttore.\n6. Sapresti dov'è la stazione?\n7. Potrei entrare?\n8. Vorresti prendere un caffè?",
    "explicacao": "Il condizionale ammorbidisce le richieste, le rende più cortesi. Particolarmente usato con volere→vorrei, potere→potrei/potresti, dovere→dovrei."
})

# Esercizio 3 - ipotesi
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Completare con il condizionale semplice:\n1. Se avessi più tempo, (studiare) ___ il pianoforte.\n2. Se potessi, (andare) ___ a vivere in Italia.\n3. Se fossi ricco, (comprare) ___ una villa al mare.\n4. Se non piovesse, (uscire) ___ a fare una passeggiata.\n5. Cosa (fare) ___ tu al mio posto?\n6. (Venire) ___ volentieri, ma ho un impegno.\n7. (Preferire) ___ restare a casa stasera.\n8. Con più soldi, (potere) ___ viaggiare di più.",
    "resposta": "1. studierei\n2. andrei\n3. comprerei\n4. uscirei\n5. faresti\n6. Verrei\n7. Preferirei\n8. potrei",
    "explicacao": "Il condizionale esprime azioni ipotetiche o desiderate. Con SE + congiuntivo imperfetto (ipotetico) o come espressione di desiderio/preferenza."
})

# Esercizio 4 - discorso indiretto
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Trasformare al discorso indiretto (futuro→condizionale):\n1. Marco ha detto: \"Verrò domani.\"\n2. Luisa ha promesso: \"Studierò per l'esame.\"\n3. Il professore ha annunciato: \"Faremo una gita.\"\n4. Paolo ha detto: \"Partirò la settimana prossima.\"\n5. I ragazzi hanno detto: \"Finiremo presto.\"\n6. Maria ha detto: \"Sarò puntuale.\"",
    "resposta": "1. Marco ha detto che sarebbe venuto il giorno dopo.\n2. Luisa ha promesso che avrebbe studiato per l'esame.\n3. Il professore ha annunciato che avrebbero fatto una gita.\n4. Paolo ha detto che sarebbe partito la settimana dopo.\n5. I ragazzi hanno detto che avrebbero finito presto.\n6. Maria ha detto che sarebbe stata puntuale.",
    "explicacao": "Discorso indiretto: futuro semplice → condizionale composto (avrei/sarei + participio). Il futuro del passato è sempre condizionale composto."
})

# Esercizio 5 - condizionale composto
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Formare il condizionale composto:\n1. io / mangiare\n2. tu / partire\n3. lei / essere\n4. noi / venire\n5. voi / fare\n6. loro / andare\n7. io / dovere studiare\n8. lei / potere venire\n9. noi / volere restare\n10. tu / alzarsi",
    "resposta": "1. avrei mangiato\n2. saresti partito/a\n3. sarebbe stata\n4. saremmo venuti/e\n5. avreste fatto\n6. sarebbero andati/e\n7. avrei dovuto studiare\n8. avrebbe potuto venire\n9. avremmo voluto restare\n10. ti saresti alzato/a",
    "explicacao": "Condizionale composto: condizionale di avere/essere + participio. Con ESSERE: participio concorda col soggetto. Verbi servili prendono l'ausiliare del verbo retto."
})

# Esercizio 6 - negozio di scarpe
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Conversazione: In un negozio di scarpe.\nRispondere alle domande:\n1. Cosa ha chiesto la signora di vedere?\n2. Che numero porta di solito?\n3. Perché ha preferito il 40?\n4. Quanto costavano le prime scarpe?\n5. Perché ha scelto il secondo modello?\n6. Quanto costava il secondo modello?",
    "resposta": "1. Ha chiesto di vedere le scarpe marroni in vetrina.\n2. Di solito porta il 40.\n3. Perché il 39 era un po' stretto.\n4. Costavano ottantadue euro.\n5. Perché le piacevano di più e costavano meno.\n6. Costava cinquantacinque euro.",
    "explicacao": "Lessico del negozio di abbigliamento: numero, stretto, modello, promozione, sconto, scatola."
})

# Esercizio 7 - produzione
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 7** — Lavorare sul testo — Regalo di compleanno\n\nDescrivi cosa faresti se avessi 500 euro in più questo mese. Usa almeno 5 condizionali semplici.",
    "resposta": "Esempio: Se avessi 500 euro in più questo mese, prima di tutto ne metterei da parte la metà. Con i 250 rimasti, comprerei dei regali per la mia famiglia. Mia sorella vorrebbe un nuovo libro, e mia madre preferirebbe dei fiori e una cena al ristorante. Io mangerei volentieri in quel ristorante giapponese che ho sempre voluto provare. Forse potrei anche fare un breve viaggio fuori città nel fine settimana.",
    "explicacao": "Produzione libera con condizionale semplice. Usi: desiderio, ipotesi, preferenza."
})

# Esercizi di verifica
verifica = [
    ("Vorrei un caffè, per favore.", "Voglio un caffè, per favore.", "Vorei un caffè, per favore.", 0,
     "VORREI = condizionale di volere (io vorr-ei). 'Vorei' non esiste. Il condizionale esprime richiesta cortese."),
    ("Se potessi, verrei con te.", "Se potevo, venivo con te.", "Se posso, vengo con te.", 0,
     "Ipotesi irreale: SE + congiuntivo imperfetto (potessi) + condizionale (verrei). 'Potevo/venivo' è una narrazione passata, non ipotesi."),
    ("Avrei voluto venire, ma avevo un impegno.", "Ho voluto venire, ma avevo un impegno.", "Avevo voluto venire, ma avevo un impegno.", 0,
     "Rimpianto passato: condizionale COMPOSTO (avrei voluto). 'Ho voluto' indica azione compiuta, non rimpianto."),
    ("Potresti aiutarmi con questi bagagli?", "Puoi aiutarmi con questi bagagli?", "Potevi aiutarmi con questi bagagli?", 0,
     "Richiesta cortese: POTRESTI (condizionale). 'Puoi' è diretto ma meno cortese. 'Potevi' è imperfetto indicativo."),
    ("Marco ha detto che sarebbe venuto il giorno dopo.", "Marco ha detto che verrà il giorno dopo.", "Marco ha detto che veniva il giorno dopo.", 0,
     "Futuro nel passato (discorso indiretto): condizionale composto SAREBBE VENUTO. 'Verrà' è futuro diretto; 'veniva' è descrizione."),
    ("Dovrebbe essere più puntuale.", "Doveva essere più puntuale.", "Dovrebbe essere stato più puntuale.", 0,
     "Critica/consiglio al presente: DOVREBBE (condizionale semplice). 'Doveva' è imperfetto indicativo (descrizione del passato)."),
    ("Avremmo preferito restare a casa.", "Abbiamo preferito restare a casa.", "Preferivamo restare a casa.", 0,
     "Preferenza non realizzata nel passato: condizionale COMPOSTO (avremmo preferito). 'Abbiamo preferito' indica azione effettivamente compiuta."),
    ("Sai dov'è la banca? — Sapresti dov'è la banca?", "Sai dov'è la banca? — Sapresti dov'è la banca?", "Entrambe sono corrette, con diverso grado di cortesia.", 2,
     "SAPI è diretto; SAPRESTI è la forma cortese del condizionale. Entrambe grammaticalmente corrette."),
    ("Secondo le notizie, il ministro avrebbe rassegnato le dimissioni.", "Secondo le notizie, il ministro ha rassegnato le dimissioni.", "Secondo le notizie, il ministro rassegnava le dimissioni.", 0,
     "Condizionale giornalistico: AVREBBE RASSEGNATO indica notizia non confermata. 'Ha rassegnato' sarebbe un fatto certo."),
    ("Sarei venuto prima, ma ho perso il treno.", "Ero venuto prima, ma ho perso il treno.", "Venivo prima, ma ho perso il treno.", 0,
     "Rimpianto con ESSERE: SAREI VENUTO (condizionale composto). 'Ero venuto' è trapassato prossimo (fatto avvenuto prima di un altro)."),
    ("Come ti chiameresti se potessi scegliere il tuo nome?", "Come ti chiameresti se potevi scegliere il tuo nome?", "Come ti chiamavi se potessi scegliere il tuo nome?", 0,
     "Ipotesi: condizionale (ti chiameresti) + congiuntivo (potessi). 'Potevi' non è congiuntivo. 'Chiamavi' è imperfetto indicativo."),
    ("Tocca a te portare le sedie.", "Tocca te portare le sedie.", "Tocchi a te portare le sedie.", 0,
     "TOCCARE impersonale: tocca A + persona + infinito. La preposizione A è obbligatoria. 'Tocchi' è congiuntivo, non adatto qui."),
    ("Preferirei un tavolo vicino alla finestra.", "Preferivo un tavolo vicino alla finestra.", "Ho preferito un tavolo vicino alla finestra.", 0,
     "Preferenza educata al ristorante: PREFERIREI (condizionale presente). 'Preferivo' è descrizione passata; 'ho preferito' è azione compiuta."),
    ("Avreste dovuto avvisarci prima.", "Dovreste avvisarci prima.", "Avevate dovuto avvisarci prima.", 0,
     "Rimprovero per qualcosa di non fatto nel passato: AVRESTE DOVUTO (condizionale composto). 'Dovreste' è presente; 'avevate dovuto' è trapassato."),
    ("Se fossi in te, partirei subito.", "Se ero in te, partivo subito.", "Se sarò in te, partirò subito.", 0,
     "Ipotesi con SE: congiuntivo imperfetto (fossi) + condizionale (partirei). 'Ero/partivo' è narrazione passata."),
    ("Sarebbe bello andare al mare questo weekend.", "Sarà bello andare al mare questo weekend.", "È bello andare al mare questo weekend.", 0,
     "Desiderio/ipotesi: SAREBBE BELLO (condizionale). 'Sarà bello' indica previsione futura. 'È bello' è constatazione presente."),
    ("Mi daresti il numero di telefono?", "Mi dai il numero di telefono?", "Dammi il numero di telefono!", 0,
     "Richiesta molto cortese: MI DARESTI (condizionale). 'Mi dai' è accettabile ma meno formale. L'imperativo è più diretto/brusco."),
    ("Avrebbero potuto telefonare prima.", "Potevano telefonare prima.", "Hanno potuto telefonare prima.", 0,
     "Rimpianto/critica per azione non fatta nel passato: AVREBBERO POTUTO (condizionale composto). 'Potevano' descrive una possibilità passata."),
    ("Non saprei cosa fare senza di te.", "Non so cosa fare senza di te.", "Non sapevo cosa fare senza di te.", 0,
     "Incertezza/dipendenza affettiva: NON SAPREI (condizionale) enfatizza il disorientamento ipotetico. 'Non so' è presente diretto."),
    ("A chi è toccato fare la spesa oggi?", "A chi ha toccato fare la spesa oggi?", "Chi ha toccato fare la spesa oggi?", 0,
     "TOCCARE impersonale al passato: È TOCCATO a chi. Con ESSERE al passato prossimo. La preposizione A è necessaria prima della persona."),
]

for a, b, c, r, expl in verifica:
    EX.append({
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la forma corretta:",
        "opcoes": [a, b, c],
        "resposta": r,
        "explicacao": expl
    })

# Trovare gli errori
errori = [
    ("Vorrei un caffè e mangerei un cornetto.",
     "Vorrei un caffè e mangerei un cornetto. (CORRETTA — desiderio educato)",
     "Entrambe le forme al condizionale sono corrette per esprimere un ordine/desiderio educato."),
    ("Se avevo tempo, venivo con te.",
     "Se avessi tempo, verrei con te.",
     "Ipotesi irreale al presente: SE + congiuntivo imperfetto (avessi) + condizionale (verrei). Non indicativo."),
    ("Marco ha detto che verrà domani.",
     "Marco ha detto che sarebbe venuto il giorno dopo.",
     "Discorso indiretto con verbo principale al passato: il futuro diventa condizionale composto."),
    ("Potevo aiutarti, ma non lo sapevo.",
     "Avrei potuto aiutarti, ma non lo sapevo.",
     "Rimpianto: condizionale COMPOSTO (avrei potuto). 'Potevo' descrive una possibilità, non un rimpianto."),
    ("Saremmo venuto prima, ma c'era traffico.",
     "Saremmo venuti prima, ma c'era traffico.",
     "ESSERE: participio concorda col soggetto plurale (noi) → venuti (maschile plurale)."),
    ("Dovevi avvisarmi prima!",
     "Avresti dovuto avvisarmi prima!",
     "Rimprovero per qualcosa non fatto nel passato: condizionale COMPOSTO (avresti dovuto). 'Dovevi' descrive un obbligo passato."),
    ("Preferirei di andare al cinema stasera.",
     "Preferirei andare al cinema stasera.",
     "PREFERIRE + infinito diretto: senza preposizione DI. 'Preferire di fare' è un errore comune."),
    ("Tocca a me di pagare.",
     "Tocca a me pagare.",
     "TOCCARE a + persona + infinito DIRETTO: senza preposizione DI dopo 'tocca a me'."),
    ("Se potevo, verrei.",
     "Se potessi, verrei.",
     "Ipotesi: SE + congiuntivo imperfetto (potessi), non indicativo (potevo)."),
    ("Avrebbe bello andare in vacanza.",
     "Sarebbe bello andare in vacanza.",
     "Impersonale con ESSERE: SAREBBE bello (non avrebbe). 'Bello' è aggettivo predicativo con ESSERE."),
]

for sbagliato, corretto, expl in errori:
    EX.append({
        "tipo": "revelar",
        "pergunta": f"**Trovare l'errore** — Correggere la frase:\n{sbagliato}",
        "resposta": corretto,
        "explicacao": expl
    })

lez["exercicios"] = EX

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
