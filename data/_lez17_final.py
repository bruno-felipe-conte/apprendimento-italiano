import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XVII"), None)
if lez is None:
    lez = {"id": "a1-lez17", "num": "Lezione XVII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il trapassato prossimo"
lez["subtitulo"] = "Formazione e uso del trapassato; sequenza temporale nel passato"

lez["teoria"] = """\
## Un furto nella villa del conte Amerighi

Quando i carabinieri arrivarono nella villa del conte Amerighi, il ladro era già scappato. Aveva aperto la cassaforte, aveva preso i gioielli e i soldi che il conte aveva messo lì il giorno prima, e se n'era andato senza lasciare tracce. La domestica, che aveva sentito un rumore strano, aveva chiamato la polizia, ma quando gli agenti erano arrivati era ormai troppo tardi. Il conte, che era partito quella mattina per un viaggio di lavoro, non sapeva ancora nulla di quello che era successo. Solo dopo molte ore di indagini, gli investigatori scoprirono che il ladro era entrato dalla finestra del piano terra, che qualcuno aveva lasciato aperta per sbaglio.

---

## A Il trapassato prossimo — formazione

Si forma con l'**imperfetto di AVERE o ESSERE** + **participio passato**:

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th class="gram-genere">con AVERE (mangiare)</th><th class="gram-genere">con ESSERE (partire)</th><th class="gram-genere">riflessivo (alzarsi)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>avevo mangiato</td><td>ero partito/a</td><td>mi ero alzato/a</td></tr>
<tr><td class="gram-art">tu</td><td>avevi mangiato</td><td>eri partito/a</td><td>ti eri alzato/a</td></tr>
<tr><td class="gram-art">lui/lei</td><td>aveva mangiato</td><td>era partito/a</td><td>si era alzato/a</td></tr>
<tr><td class="gram-art">noi</td><td>avevamo mangiato</td><td>eravamo partiti/e</td><td>ci eravamo alzati/e</td></tr>
<tr><td class="gram-art">voi</td><td>avevate mangiato</td><td>eravate partiti/e</td><td>vi eravate alzati/e</td></tr>
<tr><td class="gram-art">loro</td><td>avevano mangiato</td><td>erano partiti/e</td><td>si erano alzati/e</td></tr>
</tbody>
</table>

---

## B Uso del trapassato prossimo

Il trapassato indica un'azione **anteriore** rispetto a un'altra azione già passata:

**PASSATO (trapassato) → PASSATO (imperfetto / passato prossimo / passato remoto)**

- Quando sono arrivato, Marco **era già partito**. (prima è partito Marco, poi sono arrivato io)
- **Avevo studiato** tutto il pomeriggio, quindi ero stanco.
- Non sapevo che cosa **fosse successo**. (con congiuntivo, registro formale)

**Schema temporale:**
```
TRAPASSATO  →  PASSATO  →  PRESENTE
(il prima)     (il dopo)
```

**Esempi pratici:**
- *Non ho mangiato perché* **avevo già fatto colazione**.
- *Era arrabbiata perché* **avevo dimenticato** il suo compleanno.
- *Quando siamo arrivati al cinema, il film* **era già cominciato**.
- *Ha preso l'ombrello perché* **aveva visto** le nuvole.

---

## C Trapassato vs altri tempi passati

| tempo | uso | esempio |
|---|---|---|
| imperfetto | azione in corso nel passato | *Quando arrivò, dormivo.* |
| passato prossimo/remoto | azione puntuale nel passato | *Ieri sono arrivato tardi.* |
| trapassato prossimo | azione anteriore a un'altra passata | *Quando arrivò, **avevo già dormito**.* |

---

## D Osservare — L'uso di MICA

**Mica** è un avverbio negativo che rafforza la negazione, spesso con tono sorpreso o difensivo:

- *Non sono mica stanco!* (= per nulla stanco)
- *Non l'ho mica detto io!* (= non sono stato io a dirlo)
- *Mica è colpa mia!* (= non è affatto colpa mia)
- *Non è mica semplice come sembra.* (= non è per niente semplice)

> **Nota:** MICA va sempre con la negazione NON (o senza NON in posizione iniziale per enfasi).
"""

lez["exemplos"] = [
    "Quando sono arrivato, Marco era già partito. (trapassato per anteriorità)",
    "Non ho mangiato perché avevo già fatto colazione. (trapassato con avere)",
    "Si era alzata tardi perché aveva studiato fino a tardi. (trapassato riflessivo)",
    "Il ladro era già scappato quando arrivò la polizia. (trapassato in narrazione)",
    "Non sono mica stanco! (mica per enfasi negativa)",
]

EX = []

EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Un furto nella villa:\n1. Quando arrivarono i carabinieri, dov'era il ladro?\n2. Cosa aveva fatto il ladro?\n3. Chi aveva chiamato la polizia e perché?\n4. Dove era il conte quando avvenne il furto?\n5. Come era entrato il ladro nella villa?",
    "resposta": "1. Il ladro era già scappato.\n2. Aveva aperto la cassaforte, aveva preso i gioielli e i soldi.\n3. La domestica aveva chiamato la polizia perché aveva sentito un rumore strano.\n4. Il conte era partito quella mattina per un viaggio di lavoro.\n5. Era entrato dalla finestra del piano terra, che qualcuno aveva lasciato aperta per sbaglio.",
    "explicacao": "Uso del trapassato per indicare azioni avvenute prima dell'arrivo dei carabinieri: era scappato, aveva aperto, aveva preso, aveva chiamato, aveva sentito."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Formare il trapassato prossimo:\n1. io / mangiare\n2. tu / partire\n3. lei / alzarsi\n4. noi / studiare\n5. voi / venire\n6. loro / dimenticare\n7. lui / finire\n8. io / svegliarsi\n9. tu / leggere\n10. noi / arrivare",
    "resposta": "1. avevo mangiato\n2. eri partito/a\n3. si era alzata\n4. avevamo studiato\n5. eravate venuti/e\n6. avevano dimenticato\n7. aveva finito\n8. mi ero svegliato/a\n9. avevi letto\n10. eravamo arrivati/e",
    "explicacao": "Trapassato = imperfetto di avere/essere + participio passato. Con ESSERE: participio concorda col soggetto. Con AVERE: participio invariabile (salvo con pronomi diretti precedenti)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Completare con il trapassato prossimo:\n1. Quando sono arrivato alla stazione, il treno ___ (partire) già.\n2. Marco non è venuto alla festa perché ___ (dimenticare) il nostro invito.\n3. Ero stanco perché ___ (lavorare) tutto il giorno.\n4. Luisa non sapeva nulla perché nessuno le ___ (dire) la verità.\n5. Quando la polizia è arrivata, i ladri ___ (scappare) già.\n6. Ho comprato un ombrello perché la mattina ___ (vedere) le nuvole.\n7. Non ho mangiato a cena perché ___ (fare) uno spuntino tardi.\n8. Quando è tornata a casa, i figli ___ (addormentarsi) già.",
    "resposta": "1. era già partito\n2. aveva dimenticato\n3. avevo lavorato\n4. aveva detto\n5. erano già scappati\n6. avevo visto\n7. avevo fatto\n8. si erano già addormentati",
    "explicacao": "Il trapassato indica l'azione avvenuta PRIMA dell'altra azione passata. Schema: trapassato (prima) + passato prossimo/remoto/imperfetto (dopo)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Unire le due frasi usando il trapassato prossimo:\n1. Prima ho telefonato a Luisa. Poi sono uscito. (Quando sono uscito...)\n2. Prima Marco è arrivato. Poi io sono partito. (Quando sono partito...)\n3. Prima abbiamo mangiato. Poi siamo andati al cinema. (Quando siamo andati al cinema...)\n4. Prima ha piovuto. Poi è uscito il sole. (Quando è uscito il sole...)\n5. Prima mi sono alzato. Poi ho fatto la doccia. (Quando ho fatto la doccia...)",
    "resposta": "1. Quando sono uscito, avevo già telefonato a Luisa.\n2. Quando sono partito, Marco era già arrivato.\n3. Quando siamo andati al cinema, avevamo già mangiato.\n4. Quando è uscito il sole, aveva già piovuto.\n5. Quando ho fatto la doccia, mi ero già alzato.",
    "explicacao": "La sequenza temporale: l'azione anteriore va al trapassato, quella posteriore al passato prossimo. 'Già' rafforza l'anteriorità."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Spiegare la situazione usando il trapassato:\n1. Laura era triste. (litigare con il fidanzato)\n2. Marco era stanco. (lavorare tutta la notte)\n3. I bambini non avevano fame. (mangiare poco fa)\n4. L'insegnante era arrabbiata. (nessuno fare i compiti)\n5. Carla non poteva guidare. (dimenticare la patente a casa)",
    "resposta": "1. Laura era triste perché aveva litigato con il fidanzato.\n2. Marco era stanco perché aveva lavorato tutta la notte.\n3. I bambini non avevano fame perché avevano mangiato poco fa.\n4. L'insegnante era arrabbiata perché nessuno aveva fatto i compiti.\n5. Carla non poteva guidare perché aveva dimenticato la patente a casa.",
    "explicacao": "Il trapassato spiega la causa di uno stato o situazione passata: lo stato (imperfetto) è la conseguenza dell'azione anteriore (trapassato)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Usare MICA nelle seguenti frasi:\n1. Non è semplice come sembra.\n2. Non l'ho detto io!\n3. Non sono d'accordo.\n4. Non è colpa mia.\n5. Non voglio offenderti.",
    "resposta": "1. Non è mica semplice come sembra.\n2. Non l'ho mica detto io!\n3. Non sono mica d'accordo.\n4. Non è mica colpa mia. / Mica è colpa mia!\n5. Non voglio mica offenderti.",
    "explicacao": "MICA rafforza la negazione: va dopo il verbo ausiliare o dopo il verbo semplice. Può stare anche in posizione iniziale senza NON per maggiore enfasi."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Lavorare sul testo — Una conversazione fra amiche\n\nMaria racconta a Giulia quello che era successo il giorno prima. Completare il racconto:\nIeri sera ero molto stanca perché... Prima di andare a letto... Quando mi sono svegliata stamattina, mi sono ricordata che...",
    "resposta": "Esempio:\nIeri sera ero molto stanca perché avevo lavorato tutto il giorno senza pausas. Prima di andare a letto avevo già preparato i vestiti per il giorno dopo e avevo messo la sveglia. Quando mi sono svegliata stamattina, mi sono ricordata che la sera prima avevo dimenticato di chiamare mia madre per il suo compleanno. Mi sono sentita in colpa per tutto il giorno!",
    "explicacao": "Narrazione al passato con trapassato prossimo per indicare azioni anteriori. Il trapassato spiega cause e contesto di situazioni già passate."
})

verifica = [
    ("Quando sono arrivato, Marco era già partito.", "Quando sono arrivato, Marco è già partito.", "Quando sono arrivato, Marco partiva già.", 0,
     "Anteriorità: partenza di Marco avviene PRIMA del mio arrivo → trapassato: ERA GIÀ PARTITO. Pass. prossimo e imperfetto non indicano anteriorità rispetto all'arrivo."),
    ("Non ho mangiato perché avevo già fatto colazione.", "Non ho mangiato perché ho già fatto colazione.", "Non ho mangiato perché facevo già colazione.", 0,
     "La colazione è avvenuta PRIMA del non-mangiare → trapassato: AVEVO GIÀ FATTO. Pass. prossimo 'ho fatto' mescola i piani. Imperfetto indica azione in corso."),
    ("Il film era già cominciato quando siamo arrivati.", "Il film ha già cominciato quando siamo arrivati.", "Il film già cominciava quando siamo arrivati.", 0,
     "Anteriorità: il film comincia PRIMA del nostro arrivo → trapassato: ERA GIÀ COMINCIATO (essere + cominciare). 'Ha cominciato' non è corretto (cominciare intransitivo usa essere)."),
    ("Aveva preso l'ombrello perché aveva visto le nuvole.", "Ha preso l'ombrello perché aveva visto le nuvole.", "Prese l'ombrello perché aveva visto le nuvole.", 2,
     "Il trapassato (aveva visto) indica anteriorità rispetto a 'prese' (pass. remoto) o 'ha preso' (pass. prossimo). Entrambe le opzioni a/c sono corrette."),
    ("Non sono mica stanco!", "Non sono affatto stanco!", "Entrambe le forme sono corrette.", 2,
     "MICA e AFFATTO sono sinonimi nella negazione enfatica. Entrambe grammaticalmente corrette."),
    ("Eravamo arrivati alle tre quando lui ha chiamato.", "Siamo arrivati alle tre quando lui ha chiamato.", "Arrivavamo alle tre quando lui ha chiamato.", 0,
     "L'arrivo alle tre è anteriore alla telefonata → trapassato: ERAVAMO ARRIVATI. Pass. prossimo mette le azioni allo stesso livello."),
    ("Marco aveva già finito i compiti quando la madre è tornata.", "Marco ha già finito i compiti quando la madre è tornata.", "Marco finiva i compiti quando la madre è tornata.", 0,
     "Trapassato per anteriorità: AVEVA GIÀ FINITO (prima) → è tornata (dopo). L'imperfetto 'finiva' indica azione in corso, non completata."),
    ("Si era alzata tardi perché aveva studiato fino a tardi.", "Si alzò tardi perché aveva studiato fino a tardi.", "Entrambe le forme sono corrette.", 2,
     "SI ERA ALZATA (trapassato) e SI ALZÒ (pass. remoto): entrambi corretti. Il trapassato sottolinea che l'alzarsi era già avvenuto; il pass. remoto è narrazione diretta."),
    ("Mica è difficile questo esercizio!", "Non è mica difficile questo esercizio!", "Entrambe le forme sono corrette.", 2,
     "MICA può stare all'inizio senza NON (enfatica) o dopo il verbo con NON. Entrambe le strutture sono corrette."),
    ("Quando ho aperto la finestra, aveva già smesso di piovere.", "Quando ho aperto la finestra, ha già smesso di piovere.", "Quando ho aperto la finestra, smetteva di piovere.", 0,
     "La pioggia è smessa PRIMA dell'apertura della finestra → trapassato: AVEVA GIÀ SMESSO. 'Ha smesso' non indica anteriorità. 'Smetteva' indica azione in corso."),
    ("I ladri avevano già rubato tutto quando la polizia è arrivata.", "I ladri hanno già rubato tutto quando la polizia è arrivata.", "I ladri rubavano tutto quando la polizia è arrivata.", 0,
     "Il furto è anteriore all'arrivo della polizia → trapassato: AVEVANO GIÀ RUBATO. 'Rubavano' indica azione in corso (li avrebbero potuti fermare)."),
    ("Non l'avevo mai visto prima.", "Non l'ho mai visto prima.", "Entrambe le forme sono corrette.", 0,
     "Nel contesto di una narrazione passata (sequenza di eventi) → trapassato: NON L'AVEVO MAI VISTO. Il pass. prossimo 'non l'ho mai visto' è affermazione valida per il presente."),
    ("Avevo già studiato quando Marco mi ha telefonato.", "Ho già studiato quando Marco mi ha telefonato.", "Studiavo quando Marco mi ha telefonato.", 0,
     "Studio anteriore alla telefonata → trapassato: AVEVO GIÀ STUDIATO. 'Studiavo' indica azione in corso (interrotta dalla telefonata), diverso significato."),
    ("Era partita prima che io arrivassi.", "Era partita prima che io arrivavo.", "Era partita prima che io sono arrivato.", 0,
     "Con PRIMA CHE + congiuntivo: ERA PARTITA prima che io ARRIVASSI (congiuntivo imperfetto). 'Arrivavo' è indicativo; 'sono arrivato' è indicativo presente/pass. prossimo."),
    ("Non avevano capito nulla della spiegazione.", "Non hanno capito nulla della spiegazione.", "Entrambe le forme sono corrette.", 2,
     "Il contesto determina la scelta. Se l'incomprensione è anteriore a un'altra azione passata → trapassato. Come affermazione autonoma → pass. prossimo. Entrambe corrette in diversi contesti."),
    ("Avevo dimenticato le chiavi e sono dovuto tornare.", "Dimenticai le chiavi e sono dovuto tornare.", "Avevo dimenticato le chiavi e dovevo tornare.", 0,
     "La dimenticanza (anteriore) → trapassato: AVEVO DIMENTICATO. Il ritorno (conseguenza) → pass. prossimo: SONO DOVUTO tornare."),
    ("Quando siamo tornati, i bambini si erano già addormentati.", "Quando siamo tornati, i bambini si sono già addormentati.", "Quando siamo tornati, i bambini già dormivano.", 0,
     "Addormentarsi è anteriore al ritorno → trapassato: SI ERANO GIÀ ADDORMENTATI. 'Dormivano' indica sonno in corso (corretto ma meno preciso sull'anteriorità)."),
    ("Non sapevo che Marco fosse già partito.", "Non sapevo che Marco era già partito.", "Entrambe le forme sono corrette.", 2,
     "Con 'sapere' + che: congiuntivo (fosse partito, formale) o indicativo (era partito, comune). Entrambe accettate nell'italiano moderno."),
    ("Aveva lavorato tutta la vita e ora poteva riposarsi.", "Ha lavorato tutta la vita e ora poteva riposarsi.", "Lavorò tutta la vita e ora poteva riposarsi.", 0,
     "Nella narrazione: trapassato (AVEVA LAVORATO) per l'azione anteriore + imperfetto (POTEVA) per lo stato presente nel passato."),
    ("Non sono mica venuto per litigare.", "Non sono venuto mica per litigare.", "Entrambe le forme sono corrette.", 2,
     "MICA può stare dopo l'ausiliare o dopo il participio. Entrambe le posizioni sono accettate nell'italiano parlato."),
]

for a, b, c, r, expl in verifica:
    EX.append({
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la forma corretta:",
        "opcoes": [a, b, c],
        "resposta": r,
        "explicacao": expl
    })

errori = [
    ("Quando sono arrivato, Marco è già partito.",
     "Quando sono arrivato, Marco era già partito.",
     "Anteriorità nel passato → trapassato: ERA GIÀ PARTITO. Pass. prossimo 'è partito' non indica chiaramente anteriorità."),
    ("Non ho mangiato perché facevo già colazione.",
     "Non ho mangiato perché avevo già fatto colazione.",
     "L'azione anteriore (colazione) va al trapassato: AVEVO FATTO. L'imperfetto 'facevo' indica azione in corso, non completata."),
    ("Aveva già piovuto quando uscii.",
     "Corretta.",
     "Forma corretta: trapassato (aveva piovuto = anteriore) + passato remoto (uscii = posteriore)."),
    ("Si era alzato tardi perché aveva studiare fino a tardi.",
     "Si era alzato tardi perché aveva studiato fino a tardi.",
     "Trapassato: imperfetto di avere + PARTICIPIO PASSATO (studiato), non infinito (studiare)."),
    ("Marco mica ha detto questo.",
     "Marco non ha mica detto questo. / Marco mica ha detto questo.",
     "Entrambe accettate: MICA + NON davanti al verbo, oppure MICA in posizione iniziale senza NON (enfatico)."),
    ("Quando la polizia è arrivata, il ladro scappava già.",
     "Quando la polizia è arrivata, il ladro era già scappato.",
     "La fuga è avvenuta prima dell'arrivo → trapassato: ERA GIÀ SCAPPATO. 'Scappava' indica azione in corso."),
    ("Non avevo mai mangito sushi prima.",
     "Non avevo mai mangiato sushi prima.",
     "Participio di MANGIARE: mangiato (non mangito). Forma irregolare inesistente."),
    ("Era andata al mercato e aveva comprato frutta fresca.",
     "Corretta.",
     "Forma corretta: ERA ANDATA (essere+andare) + AVEVA COMPRATO (avere+comprare). Entrambi trapassati."),
    ("Avevano già finiti i compiti.",
     "Avevano già finito i compiti.",
     "Con AVERE, il participio NON concorda (senza pronome diretto precedente): avevano finito (non finiti)."),
    ("Non erano mica arrivati quando ho chiamato.",
     "Non erano mica arrivati quando ho chiamato. (CORRETTA)",
     "Forma corretta: trapassato con MICA e negazione. 'Non erano mica arrivati' = non erano affatto arrivati."),
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
