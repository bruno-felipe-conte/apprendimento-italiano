import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione IX"), None)
if lez is None:
    lez = {"id": "a1-lez9", "num": "Lezione IX", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "L'imperfetto indicativo"
lez["subtitulo"] = "Formazione e usi dell'imperfetto"

lez["teoria"] = """\
## Il primo soggiorno di Peter in Italia

Peter era un ragazzo tedesco e studiava la pittura rinascimentale italiana all'Università di Monaco. Ogni anno, durante le vacanze estive, veniva in Italia dove trascorreva un mese o due. Quando Peter ha fatto il suo primo soggiorno in Italia aveva soltanto diciannove anni: era un ragazzo alto, grassonello e portava i capelli lunghi. Era luglio e la sera verso le sette il treno è arrivato alla stazione di Firenze. Peter, carico di bagagli, è andato subito a cercare un telefono e quando l'ha trovato ha avvertito del suo arrivo alcuni amici italiani. Poi è uscito dalla stazione ed è andato alla fermata dell'autobus. Mentre Peter aspettava il numero undici per arrivare al centro, guardava la città: le strade, le case, le persone e tutto era per lui nuovo e interessante. Infine l'autobus è arrivato e Peter ci è salito. Dopo soli dieci minuti è sceso davanti al duomo.

---

## A L'imperfetto indicativo — forme

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th>I -ARE (parlare)</th><th>II -ERE (scrivere)</th><th>III -IRE (dormire)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>parlavo</td><td>scrivevo</td><td>dormivo</td></tr>
<tr><td class="gram-art">tu</td><td>parlavi</td><td>scrivevi</td><td>dormivi</td></tr>
<tr><td class="gram-art">lui/lei/Lei</td><td>parlava</td><td>scriveva</td><td>dormiva</td></tr>
<tr><td class="gram-art">noi</td><td>parlavamo</td><td>scrivevamo</td><td>dormivamo</td></tr>
<tr><td class="gram-art">voi</td><td>parlavate</td><td>scrivevate</td><td>dormivate</td></tr>
<tr><td class="gram-art">loro</td><td>parlavano</td><td>scrivevano</td><td>dormivano</td></tr>
</tbody>
</table>

**Forme irregolari:**

| infinito | io | tu | lui/lei | noi | voi | loro |
|---|---|---|---|---|---|---|
| essere | ero | eri | era | eravamo | eravate | erano |
| avere | avevo | avevi | aveva | avevamo | avevate | avevano |
| fare | facevo | facevi | faceva | facevamo | facevate | facevano |
| dire | dicevo | dicevi | diceva | dicevamo | dicevate | dicevano |
| bere | bevevo | bevevi | beveva | bevevamo | bevevate | bevevano |
| tradurre | traducevo | traducevi | traduceva | traducevamo | traducevate | traducevano |

---

## B Usi dell'imperfetto

**a) Azione passata in atto (in corso di svolgimento):**
- Stamattina, quando sei arrivato, **dormivo** ancora.
- Ieri, mentre **pranzavo**, ascoltavo il giornale-radio.
- **Aspettavo** l'autobus da pochi minuti quando ho visto passare Giorgio.

**b) Azione abituale nel passato:**
- Tutte le domeniche **andavo** a trovare i nonni.
- Di solito, mentre **pranzavo**, ascoltavo il giornale-radio.

> *Nel caso di azioni passate non abituali, accadute successivamente, si usa il passato prossimo:*
> *Ieri ho pranzato e poi ho ascoltato il giornale-radio.*

**c) Descrizione di condizioni nel passato** (atmosferiche, fisiche, emotive):
- La giornata **era** bella; **splendeva** il sole, ma **faceva** freddo.
- Carlo **era** alto e magro. **Aveva** i capelli e gli occhi scuri.

**d) Azione contemporanea rispetto a un'altra passata:**
- Ho preso un'aspirina perché **avevo** la febbre.
- Laura mi ha detto che **aspettava** una telefonata da Paolo.
- Ho conosciuto Luca quando **frequentavo** l'università.

---

## C L'uso di mentre e durante

| | esempio |
|---|---|
| **mentre** + verbo coniugato | Paolo, **mentre cenava**, ha bevuto troppo vino. |
| **durante** + nome | **Durante la cena** Paolo ha bevuto troppo vino. |
| **mentre** + verbo | **Mentre ero** in Italia, ho conosciuto molte persone. |
| **durante** + nome | **Durante il mio soggiorno** in Italia, ho conosciuto molte persone. |
"""

lez["exemplos"] = [
    "Mentre aspettavo l'autobus, guardavo la città.",
    "Tutte le domeniche andavo a trovare i nonni.",
    "Era luglio e faceva molto caldo.",
    "Ho preso un'aspirina perché avevo la febbre.",
    "Quando ero bambino, dormivo sempre fino a tardi.",
]

exercicios = []

# ── Domande sul testo ─────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Rispondere alle domande sul testo 'Il primo soggiorno di Peter in Italia':",
    "pergunta": (
        "1. Di dov'era Peter?\n"
        "2. Che cosa studiava?\n"
        "3. Che cosa faceva durante le vacanze estive?\n"
        "4. A che età ha fatto il suo primo soggiorno in Italia?\n"
        "5. Com'era fisicamente?\n"
        "6. In che mese è venuto in Italia?\n"
        "7. A che ora è arrivato il treno alla stazione?\n"
        "8. Che cosa ha fatto Peter quando è sceso dal treno?\n"
        "9. Che cosa guardava mentre aspettava l'autobus?\n"
        "10. Che cosa ha fatto quando è arrivato?"
    ),
    "resposta": (
        "1. Era tedesco (di Monaco).\n"
        "2. La pittura rinascimentale italiana.\n"
        "3. Veniva in Italia e trascorreva un mese o due.\n"
        "4. A diciannove anni.\n"
        "5. Era alto, grassonello e portava i capelli lunghi.\n"
        "6. In luglio.\n"
        "7. Verso le sette di sera.\n"
        "8. Ha cercato un telefono e ha avvertito alcuni amici italiani.\n"
        "9. Le strade, le case, le persone.\n"
        "10. Ha preso l'autobus ed è sceso davanti al duomo."
    )
})

# ── Esercizio 1 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1 — Volgere all'imperfetto:\nMod.: Mentre Elsa (fare) faceva i letti, Renzo (lavare) lavava il pavimento.",
    "pergunta": (
        "1. Mentre Giovanni (preparare) ___ il caffè, Franca (stirare) ___ le camicie.\n"
        "2. Ieri sera, mentre (io leggere) ___ il giornale, mia figlia (giocare) ___ con un trenino elettrico.\n"
        "3. Stamattina, mentre (io vestirsi) ___, (pensare) ___ alle cose da fare.\n"
        "4. La scorsa settimana, mentre lei (essere) ___ in vacanza, io (lavorare) ___\n"
        "5. Mentre il dentista (cercare) ___ di estrarre il dente, Pierino (urlare) ___\n"
        "6. Mentre Luisa (passeggiare) ___ nel parco, Roberto (giocare) ___ con il cane.\n"
        "7. Mentre il professore (spiegare) ___, gli studenti (prendere) ___ appunti.\n"
        "8. Paolo (lavare) ___ i piatti mentre Luisa (sparecchiare) ___ la tavola.\n"
        "9. Mentre (io fare) ___ i compiti, (ascoltare) ___ la musica alla radio.\n"
        "10. Loro (parlare) ___ ad alta voce mentre io (cercare) ___ di concentrarmi."
    ),
    "resposta": (
        "1. preparava / stirava\n"
        "2. leggevo / giocava\n"
        "3. mi vestivo / pensavo\n"
        "4. era / lavoravo\n"
        "5. cercava / urlava\n"
        "6. passeggiava / giocava\n"
        "7. spiegava / prendevano\n"
        "8. lavava / sparecchiava\n"
        "9. facevo / ascoltavo\n"
        "10. parlavano / cercavo"
    )
})

# ── Esercizio 2 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 2 — Volgere al passato prossimo:\nMod.: (Io finire) ho finito l'università e poi (cercare) ho cercato un lavoro.",
    "pergunta": (
        "1. Luisa (preparare) ___ le valigie e poi (partire) ___\n"
        "2. (Io mangiare) ___ il gelato e subito dopo (sentirsi) ___ male.\n"
        "3. Elisa (scrivere) ___ la lettera e poi (andare) ___ a imbucarla.\n"
        "4. Noi (arrivare) ___ a casa e (accendere) ___ subito il televisore.\n"
        "5. Mio fratello (vendere) ___ la sua vecchia bici e (comprare) ___ un motorino usato.\n"
        "6. Stamattina (io uscire) ___ presto: (fare) ___ colazione al bar poi (leggere) ___ il giornale.\n"
        "7. (Io fare) ___ il bucato e poi (stirare) ___ la biancheria.\n"
        "8. Linda (finire) ___ il corso e poi (partire) ___ per le vacanze.\n"
        "9. Il direttore (firmare) ___ i diplomi e poi (consegnarli) ___ agli studenti.\n"
        "10. Prima (io andare) ___ dal medico e poi (passare) ___ dalla farmacia."
    ),
    "resposta": (
        "1. ha preparato / è partita\n"
        "2. ho mangiato / mi sono sentito/a\n"
        "3. ha scritto / è andata\n"
        "4. siamo arrivati / abbiamo acceso\n"
        "5. ha venduto / ha comprato\n"
        "6. sono uscito/a / ho fatto / ho letto\n"
        "7. ho fatto / ho stirato\n"
        "8. ha finito / è partita\n"
        "9. ha firmato / li ha consegnati\n"
        "10. sono andato/a / sono passato/a"
    )
})

# ── Esercizio 3 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 3 — Passato prossimo o imperfetto?",
    "pergunta": (
        "1. (Io vedere) ___ Anna ieri sera mentre (uscire) ___ dal cinema.\n"
        "2. (Lei essere) ___ stanca morta e per questo (andare) ___ a dormire presto.\n"
        "3. Il mio orologio (non funzionare) ___, così (dovere) ___ cambiarlo.\n"
        "4. Mia sorella (non andare) ___ a lavorare perché (stare) ___ male.\n"
        "5. (Io telefonare) ___ a Giulio perché (volere) ___ invitarlo a cena.\n"
        "6. (Io non potere) ___ avvertirti perché (non sapere) ___ il tuo numero di telefono.\n"
        "7. Carla (non mangiare) ___ nulla perché (non avere) ___ fame.\n"
        "8. Ieri sera, quando (io vederla) ___ così pallida, (capire) ___ subito che (lei stare) ___ male.\n"
        "9. (Loro chiedere) ___ a Carlo dei soldi in prestito perché (essere) ___ al verde.\n"
        "10. (Io bere) ___ tutta l'acqua perché (avere) ___ molta sete."
    ),
    "resposta": (
        "1. ho visto / usciva\n"
        "2. era / è andata\n"
        "3. non funzionava / ho dovuto\n"
        "4. non è andata / stava\n"
        "5. ho telefonato / volevo\n"
        "6. non ho potuto / non sapevo\n"
        "7. non ha mangiato / non aveva\n"
        "8. l'ho vista / ho capito / stava\n"
        "9. hanno chiesto / erano\n"
        "10. ho bevuto / avevo"
    )
})

# ── Esercizio 4 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 4 — Passato prossimo o imperfetto?",
    "pergunta": (
        "1. Mentre lei (studiare) ___, lui (preparare) ___ la cena.\n"
        "2. Quando (io entrare) ___ in casa, mia madre (leggere) ___\n"
        "3. (Io aspettare) ___ Carlo tutto il giorno.\n"
        "4. (Noi arrivare) ___ a casa mentre tutti (essere) ___ a tavola.\n"
        "5. Mentre (io andare) ___ a lavoro, (vedere) ___ un mio vecchio amico e (invitarlo) ___ a bere qualcosa.\n"
        "6. Mentre (io essere) ___ sull'autostrada (vedere) ___ un incidente grave e (dovere) ___ fermarmi.\n"
        "7. Il meccanico (dire) ___ che la mia macchina (essere) ___ troppo vecchia e che non (essere) ___ possibile ripararla.\n"
        "8. Stamattina, quando (io uscire) ___, (fare) ___ molto freddo.\n"
        "9. (Lei avere) ___ molta fame, perciò (mangiare) ___ tutto quello che (esserci) ___ nel vassoio.\n"
        "10. Ieri (io perdere) ___ le chiavi mentre (andare) ___ al lavoro così, quando (ritornare) ___ a casa, (non potere) ___ entrare."
    ),
    "resposta": (
        "1. studiava / preparava\n"
        "2. sono entrato/a / leggeva\n"
        "3. ho aspettato\n"
        "4. siamo arrivati / erano\n"
        "5. andavo / ho visto / ho invitato\n"
        "6. ero / ho visto / ho dovuto\n"
        "7. ha detto / era / era\n"
        "8. sono uscito/a / faceva\n"
        "9. aveva / ha mangiato / c'era\n"
        "10. ho perso / andavo / sono ritornato/a / non ho potuto"
    )
})

# ── Conversazione — All'ufficio postale ──────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Conversazione — All'ufficio postale (leggere il dialogo):",
    "pergunta": (
        "1° Cliente: Scusi, è questo lo sportello per le raccomandate?\n"
        "Impiegato: Sì, signore, è proprio questo.\n"
        "1° Cliente: Ecco, vorrei spedire una raccomandata per via aerea.\n"
        "Impiegato: Sì, ma prima deve riempire questo modulo.\n"
        "1° Cliente: Ecco fatto, va bene così?\n"
        "Impiegato: Sì, va bene. Sono un euro trentanove centesimi e questa è la Sua ricevuta.\n\n"
        "2° Cliente: Scusi, qual è lo sportello per i telegrammi?\n"
        "Impiegato: Il numero sei.\n"
        "2° Cliente: Mi può dare un modulo per telegrammi?\n"
        "Impiegato: Sì, eccolo. Qui deve scrivere l'indirizzo del mittente, cioè il Suo indirizzo, qui quello del destinatario e qui, in modo chiaro, il testo del telegramma.\n"
        "2° Cliente: Così va bene.\n"
        "Impiegato: L'indirizzo del destinatario non è scritto in modo chiaro, lo deve riscrivere, per favore.\n"
        "2° Cliente: Ora può andare?\n"
        "Impiegato: Sì, perfetto.\n"
        "2° Cliente: Quanto spendo?\n"
        "Impiegato: Sono sette parole... dunque due euro ventisette centesimi.\n"
        "2° Cliente: Quando arriverà questo telegramma?\n"
        "Impiegato: Fra due o tre ore.\n"
        "2° Cliente: Grazie, arrivederci."
    ),
    "resposta": "Dialogo all'ufficio postale per spedire una raccomandata e un telegramma."
})

# ── Vocabolario + Lettura ─────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lettura — 'La mia cucina' (rispondere alle domande):",
    "pergunta": (
        "Nel mio appartamento c'è una cucina non molto grande, ma abbastanza graziosa e "
        "funzionale. L'arredamento è in stile moderno e i mobili sono pochi ed essenziali. "
        "Quando si entra, a destra c'è una credenza dove tengo due servizi di piatti, le "
        "tazze di tutti i giorni e i bicchieri. Nella parete di fronte alla porta c'è "
        "un'ampia finestra con ai vetri delle tendine colorate. Sotto la finestra c'è un "
        "mobiletto bianco, dove tengo un servizio di bicchieri per le occasioni speciali, "
        "un altro servizio di piatti di porcellana cinese, un servizio da caffè e altro "
        "vasellame. Nella parte superiore del mobiletto ci sono due cassetti con dentro "
        "le posate. Alla parete a sinistra c'è l'acquaio con a destra la cucina e a "
        "sinistra la lavastoviglie, il frigorifero e un piano di lavoro. Sopra l'acquaio "
        "ci sono quattro armadietti pensili dove tengo le cose più svariate: il tè, il "
        "caffè, i biscotti, le spezie, ecc. Nel centro della stanza c'è una tavola con "
        "intorno sei sedie. La mia cucina è sempre un po' in disordine, ma è pulita e io "
        "ci sto volentieri.\n\n"
        "1. Com'è la cucina?\n"
        "2. In che stile è l'arredamento?\n"
        "3. Quali mobili ci sono?\n"
        "4. Dove tieni i bicchieri?\n"
        "5. Quanti servizi di piatti hai?\n"
        "6. C'è una tavola nella cucina?\n"
        "7. A che cosa serve l'acquaio?\n"
        "8. Chi lava i piatti?"
    ),
    "resposta": (
        "1. Non molto grande, ma abbastanza graziosa e funzionale.\n"
        "2. Moderno.\n"
        "3. Credenza, mobiletto, lavastoviglie, frigorifero, armadietti pensili, tavola e sedie.\n"
        "4. Nella credenza (di tutti i giorni) e nel mobiletto (per occasioni speciali).\n"
        "5. Almeno tre: di tutti i giorni, di porcellana cinese e da caffè.\n"
        "6. Sì, con sei sedie intorno.\n"
        "7. Per lavare i piatti.\n"
        "8. La lavastoviglie (o la persona che vive lì)."
    )
})

# ── Esercizio 5 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 5 — Passato prossimo o imperfetto?",
    "pergunta": (
        "1. Mentre (io leggere) ___ il giornale, (ascoltare) ___ la radio.\n"
        "2. Quando (noi essere) ___ a Firenze, ogni giorno (andare) ___ a visitare una chiesa.\n"
        "3. Mentre (tu fare) ___ gli esercizi, (pensare) ___ in italiano?\n"
        "4. (Essere) ___ una brutta giornata, (tirare) ___ vento e (piovere) ___\n"
        "5. Mentre (io prendere) ___ il caffè al bar, (vedere) ___ Carla che (aspettare) ___ un taxi.\n"
        "6. Allora (io essere) ___ troppo giovane per capire certe cose.\n"
        "7. Durante l'estate scorsa (io fare) ___ delle lunghe passeggiate.\n"
        "8. In quella casa (abitare) ___ una vecchia signora.\n"
        "9. Ieri (essere) ___ una bella giornata, ma oggi piove.\n"
        "10. Mentre voi (parlare) ___, Luigi (ascoltare) ___ con attenzione.\n"
        "11. Mentre (io bere) ___ il caffè, (arrivare) ___ Susanna.\n"
        "12. Quando (io essere) ___ in Italia, (andare) ___ anche a Roma."
    ),
    "resposta": (
        "1. leggevo / ascoltavo\n"
        "2. eravamo / andavamo\n"
        "3. facevi / pensavi\n"
        "4. era / tirava / pioveva\n"
        "5. prendevo / ho visto / aspettava\n"
        "6. ero\n"
        "7. ho fatto\n"
        "8. abitava\n"
        "9. era\n"
        "10. parlavate / ascoltava\n"
        "11. bevevo / è arrivata\n"
        "12. ero / sono andato/a"
    )
})

# ── Esercizio 6 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 6 — Come il precedente (passato prossimo o imperfetto):",
    "pergunta": (
        "1. Il nostro professore (essere) ___ in gamba, ma noi (studiare) ___ poco.\n"
        "2. Nella preistoria sulla Terra (vivere) ___ i dinosauri.\n"
        "3. Mentre Lucia (cucinare) ___, Francesca (apparecchiare) ___ la tavola.\n"
        "4. Fino al mese scorso (io fumare) ___ venti sigarette al giorno, ma poi (smettere) ___\n"
        "5. Quando (io arrivare) ___ in Italia, (conoscere) ___ già tante persone.\n"
        "6. Quando (io essere) ___ al mare, (fare) ___ il bagno tutti i giorni.\n"
        "7. Mentre (cenare) ___, (arrivare) ___ i miei amici.\n"
        "8. Quando (noi abitare) ___ a Firenze, (andare) ___ al cinema quasi tutte le sere.\n"
        "9. (Noi giocare) ___ a scacchi per passare i pomeriggi.\n"
        "10. Paola (parlare) ___ spesso dei suoi figli.\n"
        "11. Quando (io studiare) ___ a Firenze, (avere) ___ un insegnante molto bravo.\n"
        "12. Quel giorno (fare) ___ molto caldo, il mare (essere) ___ calmo e la gente (prendere) ___ il sole."
    ),
    "resposta": (
        "1. era / studiavamo\n"
        "2. vivevano\n"
        "3. cucinava / apparecchiava\n"
        "4. fumavo / ho smesso\n"
        "5. sono arrivato/a / conoscevo\n"
        "6. ero / facevo\n"
        "7. cenavamo / sono arrivati\n"
        "8. abitavamo / andavamo\n"
        "9. giocavamo\n"
        "10. parlava\n"
        "11. studiavo / avevo\n"
        "12. faceva / era / prendeva"
    )
})

# ── Esercizio 7 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 7 — Passato prossimo o imperfetto?",
    "pergunta": (
        "1. (Io incontrare) ___ Luca mentre (passeggiare) ___ per il centro.\n"
        "2. Mentre noi (giocare) ___ a tennis, loro (fare) ___ il bagno in piscina.\n"
        "3. Rita (non potere) ___ uscire perché (piovere) ___ a dirotto.\n"
        "4. (Io essere) ___ molto piccola quando (andare) ___ di moda quella canzone.\n"
        "5. Quando (loro abitare) ___ in campagna, ogni mattina (uscire) ___ presto di casa.\n"
        "6. Da piccola (io avere) ___ paura del buio.\n"
        "7. Ieri (io non venire) ___ in discoteca perché (essere) ___ malato.\n"
        "8. Mentre lei (studiare) ___ a Milano, il suo ragazzo (fare) ___ il servizio militare a Napoli.\n"
        "9. Quando (io guardare) ___ la TV, (non capire) ___ il significato di molte parole.\n"
        "10. Marco, da ragazzo (avere) ___ anche tu una grande passione per le motociclette?\n"
        "11. Silvia (cadere) ___ mentre (sciare) ___\n"
        "12. Perché (tu arrivare) ___ a scuola sempre in ritardo?"
    ),
    "resposta": (
        "1. ho incontrato / passeggiavo\n"
        "2. giocavamo / facevano\n"
        "3. non ha potuto / pioveva\n"
        "4. ero / andava\n"
        "5. abitavano / uscivano\n"
        "6. avevo\n"
        "7. non sono venuto/a / ero\n"
        "8. studiava / faceva\n"
        "9. guardavo / non capivo\n"
        "10. avevi\n"
        "11. è caduta / sciava\n"
        "12. arrivavi"
    )
})

# ── Esercizio 8 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8 — Come il precedente:",
    "pergunta": (
        "1. (Io venire) ___ da te nel pomeriggio, ma tu (non esserci) ___\n"
        "2. Mentre (noi guardare) ___ le vetrine, (sognare) ___ di poter comprare tutto.\n"
        "3. Quando (io abitare) ___ a Roma, (avere) ___ l'abitudine di fare tardi la sera.\n"
        "4. Mentre la mamma (cucinare) ___, i bambini (mettere) ___ in ordine i loro giocattoli.\n"
        "5. (Essere) ___ una notte tranquilla e la luna (splendere) ___ sulla città.\n"
        "6. Luisa (non partire) ___ perché (esserci) ___ sciopero dei treni.\n"
        "7. Il direttore (entrare) ___ mentre il professore (spiegare) ___ la lezione.\n"
        "8. Quando (io andare) ___ a scuola, (prendere) ___ sempre l'autobus alle sette e mezza.\n"
        "9. Marco e io, quando (essere) ___ in Egitto, (bere) ___ molto perché il caldo (essere) ___ insopportabile.\n"
        "10. Mentre (io scrivere) ___ una lettera a mia madre, (loro bussare) ___ alla porta; (io andare) ___ ad aprire, ma (non esserci) ___ nessuno."
    ),
    "resposta": (
        "1. sono venuto/a / non c'eri\n"
        "2. guardavamo / sognavamo\n"
        "3. abitavo / avevo\n"
        "4. cucinava / mettevano\n"
        "5. era / splendeva\n"
        "6. non è partita / c'era\n"
        "7. è entrato / spiegava\n"
        "8. andavo / prendevo\n"
        "9. eravamo / bevevamo / era\n"
        "10. scrivevo / hanno bussato / sono andato/a / non c'era"
    )
})

# ── Esercizio 9 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 9 — Trasformare secondo il modello (abitudine nel passato):\nMod.: Ceno a casa. → Cenavo sempre a casa.",
    "pergunta": (
        "1. Prendo il caffè dopo pranzo.\n"
        "2. Faccio colazione al bar.\n"
        "3. Esco di casa alle otto.\n"
        "4. Gioco a tennis con Mario.\n"
        "5. Pranzo al ristorante.\n"
        "6. Guardo la T.V.\n"
        "7. Telefono a Carlo dall'ufficio.\n"
        "8. Vado a casa a piedi.\n"
        "9. Passo le vacanze al mare.\n"
        "10. Uso i colori a olio."
    ),
    "resposta": (
        "1. Prendevo sempre il caffè dopo pranzo.\n"
        "2. Facevo sempre colazione al bar.\n"
        "3. Uscivo sempre di casa alle otto.\n"
        "4. Giocavo sempre a tennis con Mario.\n"
        "5. Pranzavo sempre al ristorante.\n"
        "6. Guardavo sempre la T.V.\n"
        "7. Telefonavo sempre a Carlo dall'ufficio.\n"
        "8. Andavo sempre a casa a piedi.\n"
        "9. Passavo sempre le vacanze al mare.\n"
        "10. Usavo sempre i colori a olio."
    )
})

# ── Esercizio 10 ─────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 10 — Trasformare secondo il modello (sequenza nel passato):\nMod.: Saluto gli amici e poi vado via. → Ho salutato gli amici e poi sono andato via.",
    "pergunta": (
        "1. Preparo il pranzo e poi telefono a Mario.\n"
        "2. Metto in ordine la mia camera e poi pulisco il bagno.\n"
        "3. Fumo una sigaretta e poi entro in classe.\n"
        "4. Leggo la rivista e poi scrivo una lettera.\n"
        "5. Ripasso la lezione e poi faccio i compiti.\n"
        "6. Risparmio un po' di soldi e poi parto.\n"
        "7. Ascolto l'ultimo disco e poi vado a letto.\n"
        "8. Esco di casa alle nove e poi torno la sera tardi.\n"
        "9. Passeggio per il centro e poi prendo l'autobus per l'università.\n"
        "10. Accompagno Luisa a casa e poi passo alla stazione."
    ),
    "resposta": (
        "1. Ho preparato il pranzo e poi ho telefonato a Mario.\n"
        "2. Ho messo in ordine la mia camera e poi ho pulito il bagno.\n"
        "3. Ho fumato una sigaretta e poi sono entrato/a in classe.\n"
        "4. Ho letto la rivista e poi ho scritto una lettera.\n"
        "5. Ho ripassato la lezione e poi ho fatto i compiti.\n"
        "6. Ho risparmiato un po' di soldi e poi sono partito/a.\n"
        "7. Ho ascoltato l'ultimo disco e poi sono andato/a a letto.\n"
        "8. Sono uscito/a di casa alle nove e poi sono tornato/a la sera tardi.\n"
        "9. Ho passeggiato per il centro e poi ho preso l'autobus per l'università.\n"
        "10. Ho accompagnato Luisa a casa e poi sono passato/a alla stazione."
    )
})

# ── Esercizio 11 ─────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 11 — Volgere al passato (prossimo o imperfetto):",
    "pergunta": (
        "1. Mentre Carlo (leggere) ___, Anna (stirare) ___\n"
        "2. (Io bere) ___ un bicchiere d'acqua perché (avere) ___ sete.\n"
        "3. Carlo (scrivere) ___ una cartolina e poi (andare) ___ alla posta.\n"
        "4. Luisa (frequentare) ___ spesso quelle persone.\n"
        "5. (Loro salutare) ___ gli amici e poi (salire) ___ sul treno.\n"
        "6. Quando (io arrivare) ___ a Firenze, (fare) ___ molto freddo e (piovere) ___ a dirotto.\n"
        "7. Quel ragazzo (avere) ___ vent'anni ed (essere) ___ molto gentile.\n"
        "8. Carlo (non cenare) ___ perché (volere) ___ vedere la partita alla T.V.\n"
        "9. Quando Luisa (entrare) ___, (noi parlare) ___ proprio di lei.\n"
        "10. Mentre (io aspettare) ___ il treno, (conoscere) ___ una ragazza inglese.\n"
        "11. Quando (lui essere) ___ più giovane, (giocare) ___ in una squadra di calcio.\n"
        "12. Che cosa (voi fare) ___ quando (voi essere) ___ a Londra?"
    ),
    "resposta": (
        "1. leggeva / stirava\n"
        "2. ho bevuto / avevo\n"
        "3. ha scritto / è andato\n"
        "4. frequentava\n"
        "5. hanno salutato / sono saliti\n"
        "6. sono arrivato/a / faceva / pioveva\n"
        "7. aveva / era\n"
        "8. non ha cenato / voleva\n"
        "9. è entrata / parlavamo\n"
        "10. aspettavo / ho conosciuto\n"
        "11. era / giocava\n"
        "12. facevate / eravate"
    )
})

# ── Lavorare sul testo ────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lavorare sul testo — 'La domenica' (trascrivere alla 3a persona singolare):",
    "pergunta": (
        "Quando ero bambino ogni settimana aspettavo la domenica, perché non dovevo andare a "
        "scuola e perché così potevo dormire più a lungo. La mattina mio fratello e io "
        "facevamo colazione e poi, con i nostri genitori, uscivamo di casa per andare a fare "
        "una passeggiata. Dopo nostra madre tornava a casa, aveva molte cose da fare, ma noi, "
        "se il tempo era bello, andavamo in un parco pubblico. Mio fratello e io correvamo "
        "insieme agli altri bambini e giocavamo sul prato con la palla, mentre nostro padre, "
        "seduto su una panchina, leggeva il giornale. Verso mezzogiorno tornavamo a casa, ma "
        "prima passavamo da una pasticceria dove compravamo un dolce per festeggiare la "
        "domenica. A casa aiutavamo la mamma a preparare il pranzo e ad apparecchiare la "
        "tavola. La domenica mangiavamo prima degli altri giorni e c'era quasi sempre un "
        "piatto speciale.\n\n"
        "Trascrivere il testo alla terza persona singolare:\n"
        "Mod.: Quando Laura era una bambina ogni settimana aspettava..."
    ),
    "resposta": (
        "Quando Laura era bambina ogni settimana aspettava la domenica, perché non doveva "
        "andare a scuola e perché così poteva dormire più a lungo. La mattina suo fratello "
        "e lei facevano colazione e poi, con i loro genitori, uscivano di casa per andare "
        "a fare una passeggiata. Dopo loro madre tornava a casa, aveva molte cose da fare, "
        "ma loro, se il tempo era bello, andavano in un parco pubblico. Suo fratello e lei "
        "correvano insieme agli altri bambini e giocavano sul prato con la palla, mentre "
        "loro padre, seduto su una panchina, leggeva il giornale. Verso mezzogiorno "
        "tornavano a casa... (continuare)"
    )
})

# ════════════════════════════════════════════════════════════════════════════════
# ESERCIZI DI VERIFICA — 20 escolha
# ════════════════════════════════════════════════════════════════════════════════

verifica = [
    # 1
    {"pergunta": "Non sono uscito perché ___",
     "opcoes": ["ha fatto freddo.", "faceva freddo."],
     "resposta": 1},
    # 2
    {"pergunta": "Quando mi hai telefonato, ___",
     "opcoes": ["non ero a casa.", "non sono stato a casa."],
     "resposta": 0},
    # 3
    {"pergunta": "___ perciò sono andato a letto presto.",
     "opcoes": ["Ho avuto un sonno da morire,", "Avevo un sonno da morire,"],
     "resposta": 1},
    # 4
    {"pergunta": "Giorgio è caduto mentre ___",
     "opcoes": ["ha sceso le scale.", "scendeva le scale.", "è sceso le scale."],
     "resposta": 1},
    # 5
    {"pergunta": "Quando ___ disturbavo sempre i vicini.",
     "opcoes": ["sono stato bambino,", "ero bambino,", "ero stato bambino,"],
     "resposta": 1},
    # 6
    {"pergunta": "Prima del matrimonio ___",
     "opcoes": ["ho fatto una vita più disordinata.", "facevo una vita più disordinata."],
     "resposta": 1},
    # 7
    {"pergunta": "___ italiano per tre anni.",
     "opcoes": ["Studiavo", "Ho studiato"],
     "resposta": 1},
    # 8
    {"pergunta": "Che cosa ___ quando ti ho visto al bar?",
     "opcoes": ["hai bevuto", "bevevi"],
     "resposta": 1},
    # 9
    {"pergunta": "Prima ___ dieci sigarette al giorno, ma ora ho smesso.",
     "opcoes": ["ho fumato", "fumavo"],
     "resposta": 1},
    # 10
    {"pergunta": "Mentre ___ ho incontrato Mario.",
     "opcoes": ["camminavo per il centro,", "ho camminato per il centro,"],
     "resposta": 0},
    # 11
    {"pergunta": "Quando ero in vacanza, di solito ___",
     "opcoes": ["sono andato a letto tardissimo.", "andavo a letto tardissimo."],
     "resposta": 1},
    # 12
    {"pergunta": "Hai la moto? ___",
     "opcoes": ["Ce l'ho avuta, ma ora l'ho venduta.", "Ce l'avevo, ma ora l'ho venduta."],
     "resposta": 1},
    # 13
    {"pergunta": "Non ha mangiato perché non ___",
     "opcoes": ["ha avuto appetito.", "aveva appetito."],
     "resposta": 1},
    # 14
    {"pergunta": "Non sapevo cosa fare perciò ___",
     "opcoes": ["sono rimasto a casa.", "rimanevo a casa.", "ho rimasto a casa."],
     "resposta": 0},
    # 15
    {"pergunta": "Dovevo cambiare i soldi, e ___",
     "opcoes": ["sono andato in banca.", "andavo in banca."],
     "resposta": 0},
    # 16
    {"pergunta": "Maria è già partita? Non ___",
     "opcoes": ["l'ho saputo.", "lo sapevo."],
     "resposta": 1},
    # 17
    {"pergunta": "Ora il cielo è sereno, ma stamattina ___",
     "opcoes": ["è stato nuvoloso.", "era nuvoloso."],
     "resposta": 1},
    # 18
    {"pergunta": "Mentre copiavamo dal libro, l'insegnante ___",
     "opcoes": ["entrava in classe.", "è entrato in classe."],
     "resposta": 1},
    # 19
    {"pergunta": "Non sono venuto perché ___",
     "opcoes": ["ho avuto un appuntamento.", "avevo un appuntamento."],
     "resposta": 1},
    # 20
    {"pergunta": "___ e poi sono tornato a casa.",
     "opcoes": ["Ho fatto la spesa", "Facevo la spesa"],
     "resposta": 0},
]

for v in verifica:
    exercicios.append({
        "tipo": "escolha",
        "enunciado": "Scegliere la frase corretta:",
        "pergunta": v["pergunta"],
        "opcoes": v["opcoes"],
        "resposta": v["resposta"]
    })

# ── Trovare gli errori ────────────────────────────────────────────────────────
errori = [
    ("Avevo mal di denti e andavo dal dottore.",
     "Avevo mal di denti e sono andato dal dottore."),
    ("È cominciato a piovere, mentre siamo usciti.",
     "È cominciato a piovere, mentre uscivamo."),
    ("Quando è stato giovane, ha viaggiato molto.",
     "Quando era giovane, ha viaggiato molto."),
    ("Mio padre lavorava dieci anni in Venezuela.",
     "Mio padre ha lavorato dieci anni in Venezuela."),
    ("Vendevo la mia auto perché era vecchia.",
     "Ho venduto la mia auto perché era vecchia."),
    ("Ho lavato le camicie e le stiravo.",
     "Ho lavato le camicie e le ho stirate."),
    ("Ho parlato con la segretaria perché ho voluto sapere il costo del corso.",
     "Ho parlato con la segretaria perché volevo sapere il costo del corso."),
    ("Hai visto la televisione? Che cosa c'è stato?",
     "Hai visto la televisione? Che cosa c'era? (o: Che cosa c'è stato di bello?)"),
    ("Non ho telefonato perché non ho saputo che eri in casa.",
     "Non ho telefonato perché non sapevo che eri in casa."),
    ("Dove hai passato le vacanze quando eri bambino? (nessun errore)",
     "Corretto! Domanda con passato prossimo + imperfetto nella stessa frase."),
]

for i, (frase, corretta) in enumerate(errori, 21):
    exercicios.append({
        "tipo": "revelar",
        "enunciado": f"Trovare l'errore ({i}):",
        "pergunta": frase,
        "resposta": corretta
    })

lez["exercicios"] = exercicios

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

n_e = sum(1 for e in exercicios if e["tipo"] == "escolha")
n_r = sum(1 for e in exercicios if e["tipo"] == "revelar")
print(f"OK: Lezione IX — L'imperfetto indicativo")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(exercicios)} total (escolha: {n_e}, revelar: {n_r})")
