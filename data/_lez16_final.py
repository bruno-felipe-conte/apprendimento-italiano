import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XVI"), None)
if lez is None:
    lez = {"id": "a1-lez16", "num": "Lezione XVI", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il passato remoto"
lez["subtitulo"] = "Formazione e uso del passato remoto; differenza con il passato prossimo"

lez["teoria"] = """\
## Giorgio e il suo lavoro

Giorgio Marini nacque a Firenze nel 1945. Studiò ragioneria e poi si iscrisse all'università di Bologna, dove si laureò in economia. Dopo la laurea tornò nella sua città e trovò lavoro in una piccola azienda commerciale. Lavorò duramente per molti anni e alla fine divenne direttore commerciale. Nel 1972 sposò Maria Bianchi, una ragazza fiorentina, e andarono a vivere in un appartamento vicino al centro. Ebbero due figli: un maschio e una femmina. Giorgio fu sempre un uomo serio e responsabile. Nel 1990 decise di mettersi in proprio e aprì la sua azienda. Le cose andarono bene fin dall'inizio e l'azienda crebbe rapidamente. Giorgio non si pentì mai di quella decisione.

---

## A Il passato remoto — forme regolari

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th class="gram-genere">I -ARE (parlare)</th><th class="gram-genere">II -ERE (credere)</th><th class="gram-genere">III -IRE (partire)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>parla<strong>i</strong></td><td>crede<strong>tti</strong> / crede<strong>i</strong></td><td>part<strong>ii</strong></td></tr>
<tr><td class="gram-art">tu</td><td>parla<strong>sti</strong></td><td>crede<strong>sti</strong></td><td>part<strong>isti</strong></td></tr>
<tr><td class="gram-art">lui/lei/Lei</td><td>parl<strong>ò</strong></td><td>crede<strong>tte</strong> / crede<strong>é</strong></td><td>part<strong>ì</strong></td></tr>
<tr><td class="gram-art">noi</td><td>parla<strong>mmo</strong></td><td>crede<strong>mmo</strong></td><td>part<strong>immo</strong></td></tr>
<tr><td class="gram-art">voi</td><td>parla<strong>ste</strong></td><td>crede<strong>ste</strong></td><td>part<strong>iste</strong></td></tr>
<tr><td class="gram-art">loro</td><td>parla<strong>rono</strong></td><td>crede<strong>ttero</strong> / crede<strong>rono</strong></td><td>part<strong>irono</strong></td></tr>
</tbody>
</table>

---

## B Il passato remoto — forme irregolari comuni

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">infinito</th><th class="gram-art">io</th><th class="gram-art">tu</th><th class="gram-art">lui/lei</th><th class="gram-art">noi</th><th class="gram-art">voi</th><th class="gram-art">loro</th></tr>
</thead>
<tbody>
<tr><td>essere</td><td>fui</td><td>fosti</td><td>fu</td><td>fummo</td><td>foste</td><td>furono</td></tr>
<tr><td>avere</td><td>ebbi</td><td>avesti</td><td>ebbe</td><td>avemmo</td><td>aveste</td><td>ebbero</td></tr>
<tr><td>fare</td><td>feci</td><td>facesti</td><td>fece</td><td>facemmo</td><td>faceste</td><td>fecero</td></tr>
<tr><td>dire</td><td>dissi</td><td>dicesti</td><td>disse</td><td>dicemmo</td><td>diceste</td><td>dissero</td></tr>
<tr><td>venire</td><td>venni</td><td>venisti</td><td>venne</td><td>venimmo</td><td>veniste</td><td>vennero</td></tr>
<tr><td>volere</td><td>volli</td><td>volesti</td><td>volle</td><td>volemmo</td><td>voleste</td><td>vollero</td></tr>
<tr><td>potere</td><td>potei</td><td>potesti</td><td>poté</td><td>potemmo</td><td>poteste</td><td>poterono</td></tr>
<tr><td>sapere</td><td>seppi</td><td>sapesti</td><td>seppe</td><td>sapemmo</td><td>sapeste</td><td>seppero</td></tr>
<tr><td>mettere</td><td>misi</td><td>mettesti</td><td>mise</td><td>mettemmo</td><td>metteste</td><td>misero</td></tr>
<tr><td>prendere</td><td>presi</td><td>prendesti</td><td>prese</td><td>prendemmo</td><td>prendeste</td><td>presero</td></tr>
<tr><td>nascere</td><td>nacqui</td><td>nascesti</td><td>nacque</td><td>nascemmo</td><td>nasceste</td><td>nacquero</td></tr>
<tr><td>vivere</td><td>vissi</td><td>vivesti</td><td>visse</td><td>vivemmo</td><td>viveste</td><td>vissero</td></tr>
</tbody>
</table>

---

## C Passato remoto vs Passato prossimo

La scelta tra passato remoto e passato prossimo dipende dal **tempo** e dalla **relazione con il presente**:

| passato prossimo | passato remoto |
|---|---|
| Azione recente o con effetti presenti | Azione lontana nel tempo, conclusa |
| *Oggi ho lavorato molto.* | *Dante nacque nel 1265.* |
| *Stamattina ho preso il caffè.* | *Colombo scoprì l'America nel 1492.* |
| *Questa settimana ho studiato.* | *I miei nonni vissero durante la guerra.* |

> **ATTENZIONE:** In molte regioni del **Nord Italia**, si usa il passato prossimo anche per eventi lontani. Al **Centro-Sud** si preferisce il passato remoto anche per eventi recenti.

---

## D Forme irregolari — schema 1-3-3

Molti verbi irregolari seguono lo schema: irregolari alla 1ª e 3ª persona (singolare e plurale), regolari alle altre:

| io | tu | lui | noi | voi | loro |
|---|---|---|---|---|---|
| **scrissi** | scrivesti | **scrisse** | scrivemmo | scriveste | **scrissero** |
| **lessi** | leggesti | **lesse** | leggemmo | leggeste | **lessero** |
| **chiusi** | chiudesti | **chiuse** | chiudemmo | chiudeste | **chiusero** |
"""

lez["exemplos"] = [
    "Dante nacque a Firenze nel 1265. (passato remoto storico)",
    "Giorgio parlò con il direttore e poi partì. (narrazione passata)",
    "Stamattina ho preso il caffè. (passato prossimo, azione recente)",
    "I Romani costruirono molte strade in Europa. (fatto storico lontano)",
    "Misi la borsa sul tavolo e uscii. (passato remoto narrativo)",
]

EX = []

EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Giorgio e il suo lavoro:\n1. Dove nacque Giorgio?\n2. Dove si laureò e in cosa?\n3. Quando si sposò e con chi?\n4. Quanti figli ebbero?\n5. Cosa decise di fare nel 1990?\n6. Come andò la sua azienda?",
    "resposta": "1. Nacque a Firenze.\n2. Si laureò a Bologna in economia.\n3. Si sposò nel 1972 con Maria Bianchi.\n4. Ebbero due figli.\n5. Decise di mettersi in proprio e aprì la sua azienda.\n6. Le cose andarono bene e l'azienda crebbe rapidamente.",
    "explicacao": "Il testo usa il passato remoto per narrare eventi biografici lontani: nacque, studiò, si laureò, tornò, trovò, lavorò, divenne, sposò, ebbero."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Coniugare al passato remoto (verbi regolari):\n1. io / parlare\n2. tu / credere\n3. lui / partire\n4. noi / lavorare\n5. voi / vendere\n6. loro / finire\n7. lei / aspettare\n8. io / rispondere\n9. tu / sentire\n10. noi / camminare",
    "resposta": "1. parlai\n2. credesti\n3. partì\n4. lavorammo\n5. vendeste\n6. finirono\n7. aspettò\n8. risposi (irregolare) / risposi\n9. sentisti\n10. camminammo",
    "explicacao": "-ARE: -ai/-asti/-ò/-ammo/-aste/-arono. -ERE: -ei(-etti)/-esti/-é(-ette)/-emmo/-este/-erono(-ettero). -IRE: -ii/-isti/-ì/-immo/-iste/-irono."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Coniugare al passato remoto (verbi irregolari):\n1. io / essere\n2. tu / avere\n3. lui / fare\n4. noi / dire\n5. voi / venire\n6. loro / volere\n7. lei / nascere\n8. io / mettere\n9. tu / prendere\n10. lui / sapere\n11. noi / vivere\n12. loro / scrivere",
    "resposta": "1. fui\n2. avesti\n3. fece\n4. dicemmo\n5. veniste\n6. vollero\n7. nacque\n8. misi\n9. prendesti\n10. seppe\n11. vivemmo\n12. scrissero",
    "explicacao": "Irregolari: schema 1-3-3 per molti verbi (io/lui-lei/loro irregolari, tu/noi/voi regolari). Es: scrissi/scrivesti/scrisse/scrivemmo/scriveste/scrissero."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Volgere al passato remoto:\n1. Marco va a Roma.\n2. Luisa studia medicina all'università.\n3. I miei nonni vivono in campagna.\n4. Il professore dice che l'esame è difficile.\n5. Napoleone nasce in Corsica.\n6. Dante scrive la Divina Commedia.\n7. I Romani costruiscono strade in tutta Europa.\n8. Colombo arriva in America nel 1492.",
    "resposta": "1. Marco andò a Roma.\n2. Luisa studiò medicina all'università.\n3. I miei nonni vissero in campagna.\n4. Il professore disse che l'esame era difficile.\n5. Napoleone nacque in Corsica.\n6. Dante scrisse la Divina Commedia.\n7. I Romani costruirono strade in tutta Europa.\n8. Colombo arrivò in America nel 1492.",
    "explicacao": "Passato remoto per fatti storici e narrazione. Andare→andò. Vivere→visse. Dire→disse. Nascere→nacque. Scrivere→scrisse. Costruire→costruì (regolare)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Scegliere passato prossimo o passato remoto:\n1. Stamattina (io bere) ___ due caffè.\n2. Garibaldi (nascere) ___ nel 1807.\n3. Ieri (noi andare) ___ al cinema.\n4. Nel Medioevo la gente (vivere) ___ molto meno di oggi.\n5. La settimana scorsa (tu finire) ___ il corso.\n6. Leonardo da Vinci (dipingere) ___ la Gioconda.",
    "resposta": "1. ho bevuto (recente)\n2. nacque (storico, lontano)\n3. siamo andati (ieri, recente)\n4. visse/viveva (lontano nel tempo)\n5. hai finito (recente)\n6. dipinse (storico, lontano)",
    "explicacao": "Pass. prossimo: azione recente, con legame al presente. Pass. remoto: azione lontana, senza legame al presente. Dipingere→dipinse (irregolare: dipinsi/dipingesti/dipinse...)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Volgere tutta la storia al passato remoto:\nMarco arriva a Firenze, cerca un albergo, trova una pensione in centro, entra, parla con il receptionist, prende una camera singola, sale al secondo piano, mette le valigie sul letto, si lava le mani e esce a visitare la città.",
    "resposta": "Marco arrivò a Firenze, cercò un albergo, trovò una pensione in centro, entrò, parlò con il receptionist, prese una camera singola, salì al secondo piano, mise le valigie sul letto, si lavò le mani e uscì a visitare la città.",
    "explicacao": "Narrativa al passato remoto: arrivò, cercò, trovò, entrò, parlò (regolari -ARE). Prese (prendere→presi/prese). Mise (mettere→misi/mise). Salì (salire, regolare). Uscì (uscire, regolare)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Lavorare sul testo — La formica e la colomba\n\nRaccontare al passato remoto la favola di Esopo:\n«Una formica cade in un fiume. Una colomba vede la formica e lascia cadere una foglia vicino ad essa. La formica sale sulla foglia e si salva. Dopo qualche tempo, la formica vede un cacciatore che vuole uccidere la colomba. La formica punge il cacciatore sul piede. Il cacciatore manca il colpo e la colomba può volare via.»",
    "resposta": "Una formica cadde in un fiume. Una colomba vide la formica e lasciò cadere una foglia vicino ad essa. La formica salì sulla foglia e si salvò. Dopo qualche tempo, la formica vide un cacciatore che voleva uccidere la colomba. La formica punse il cacciatore sul piede. Il cacciatore mancò il colpo e la colomba poté volare via.",
    "explicacao": "Favola al passato remoto. Cadde (cadere→caddi/cadde). Vide (vedere→vidi/vide). Lasciò (regolare). Salì (regolare). Voleva (imperfetto: azione in corso). Punse (pungere→punsi/punse)."
})

verifica = [
    ("Giorgio nacque a Firenze nel 1945.", "Giorgio è nato a Firenze nel 1945.", "Giorgio nasceva a Firenze nel 1945.", 0,
     "Data di nascita lontana → passato remoto: NACQUE. Il pass. prossimo 'è nato' è accettabile al Nord. L'imperfetto non si usa per nascita puntuale."),
    ("Stamattina ho preso il caffè.", "Stamattina presi il caffè.", "Stamattina prendevo il caffè.", 0,
     "Azione recente (stamattina) → passato prossimo: HO PRESO. Il pass. remoto 'presi' è tipico del Sud. L'imperfetto indica abitudine."),
    ("Dante scrisse la Divina Commedia.", "Dante ha scritto la Divina Commedia.", "Dante scriveva la Divina Commedia.", 0,
     "Fatto storico lontano → passato remoto: SCRISSE. 'Ha scritto' è accettabile ma meno formale. L'imperfetto indica un'azione in corso, non conclusa."),
    ("I Romani costruirono molte strade.", "I Romani hanno costruito molte strade.", "Entrambe le forme sono corrette.", 0,
     "Per fatti storici lontani il passato remoto è preferito nel registro formale e letterario: COSTRUIRONO."),
    ("Ieri sera mangiai a casa di Marco.", "Ieri sera ho mangiato a casa di Marco.", "Entrambe le forme sono corrette.", 2,
     "Al Nord: pass. prossimo per ieri. Al Sud/Centro: pass. remoto. Formalmente entrambe accettate, ma pass. prossimo è più comune nell'italiano standard."),
    ("Feci quello che potei.", "Feci quello che ho potuto.", "Ho fatto quello che ho potuto.", 0,
     "Narrazione con consecutività temporale: FECI / POTEI (entrambi pass. remoto per coerenza). 'Ho potuto' mescola i tempi senza necessità."),
    ("Napoleone Bonaparte fu imperatore dei Francesi.", "Napoleone Bonaparte era imperatore dei Francesi.", "Napoleone Bonaparte è stato imperatore dei Francesi.", 0,
     "Fatto storico concluso → passato remoto: FU. L'imperfetto 'era' descrive uno stato prolungato ma è meno preciso per un fatto storico puntuale."),
    ("Marco mi disse che era stanco.", "Marco mi disse che fu stanco.", "Marco mi disse che è stanco.", 0,
     "Nel discorso indiretto dopo passato remoto: imperfetto per lo stato contemporaneo (ERA stanco). 'Fu stanco' implicherebbe anteriorità. 'È stanco' è presente diretto."),
    ("La nonna visse fino a novant'anni.", "La nonna ha vissuto fino a novant'anni.", "Entrambe le forme sono corrette.", 2,
     "Per la vita di una persona ormai scomparsa: pass. remoto è preferito. Pass. prossimo è accettato. Entrambe grammaticalmente corrette."),
    ("Colombo arrivò in America nel 1492.", "Colombo è arrivato in America nel 1492.", "Colombo arrivava in America nel 1492.", 0,
     "Data precisa, fatto storico lontano → passato remoto: ARRIVÒ. L'imperfetto non indica un momento preciso."),
    ("Ieri ho lavorato tutto il giorno.", "Ieri lavorai tutto il giorno.", "Ieri lavoravo tutto il giorno.", 0,
     "Italiano standard/Nord: pass. prossimo per ieri (HO LAVORATO). L'imperfetto indica abitudine o azione in corso nel passato."),
    ("Ebbero tre figli e vissero felici.", "Hanno avuto tre figli e hanno vissuto felici.", "Avevano tre figli e vivevano felici.", 0,
     "Conclusione di racconto (stile favola/biografia) → passato remoto: EBBERO, VISSERO. L'imperfetto indicherebbe stati, non la conclusione della narrazione."),
    ("Garibaldi morì nel 1882.", "Garibaldi è morto nel 1882.", "Entrambe le forme sono corrette.", 0,
     "Fatto storico lontano → passato remoto preferito nel registro formale/letterario: MORÌ."),
    ("Si alzò, si vestì e uscì di casa.", "Si è alzato, si è vestito e è uscito di casa.", "Entrambe le forme sono corrette.", 0,
     "In narrazione letteraria consecutiva: pass. remoto per coerenza stilistica (SI ALZÒ, SI VESTÌ, USCÌ)."),
    ("Misi la chiave nel cassetto.", "Ho messo la chiave nel cassetto.", "Entrambe le forme sono corrette.", 2,
     "MISI (pass. remoto) e HO MESSO (pass. prossimo) sono entrambe corrette. La scelta dipende dal registro e dalla regione."),
    ("Quando arrivò a Roma, prese una camera in albergo.", "Quando arrivò a Roma, ha preso una camera in albergo.", "Quando arrivò a Roma, prendeva una camera in albergo.", 0,
     "Coerenza temporale nella narrazione: dopo ARRIVÒ → PRESE (pass. remoto). L'imperfetto indicherebbe un'azione in corso, non puntuale."),
    ("Il terremoto distrusse la città nel 1908.", "Il terremoto ha distrutto la città nel 1908.", "Entrambe le forme sono corrette.", 0,
     "Fatto storico preciso e lontano → passato remoto: DISTRUSSE. Nel registro formale/letterario è preferito."),
    ("Seppi la verità solo dopo molti anni.", "Ho saputo la verità solo dopo molti anni.", "Entrambe le forme sono corrette.", 2,
     "SEPPI (pass. remoto) e HO SAPUTO (pass. prossimo) sono entrambe grammaticalmente corrette."),
    ("Vennero tutti alla festa tranne Marco.", "Sono venuti tutti alla festa tranne Marco.", "Entrambe le forme sono corrette.", 2,
     "Entrambe corrette. VENNERO (pass. remoto, narrativo/formale); SONO VENUTI (pass. prossimo, più comune al Nord)."),
    ("Nacqui a Milano nel 1980.", "Sono nato a Milano nel 1980.", "Entrambe le forme sono corrette.", 2,
     "Per la propria nascita: entrambe corrette. NACQUI (formale/letterario); SONO NATO (comune nell'italiano parlato)."),
]

for a, b, c, r, expl in verifica:
    EX.append({
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la forma più appropriata:",
        "opcoes": [a, b, c],
        "resposta": r,
        "explicacao": expl
    })

errori = [
    ("Ieri ho andato al mercato.",
     "Ieri sono andato/a al mercato.",
     "ANDARE usa ESSERE al passato prossimo: sono andato/a. MAI 'ho andato'."),
    ("Dante ha nascuto nel 1265.",
     "Dante nacque nel 1265.",
     "NASCERE usa ESSERE: Dante È nato. Per il passato remoto: NACQUE. 'Ha nascuto' non esiste."),
    ("Marco disse che andrà domani.",
     "Marco disse che sarebbe andato il giorno dopo.",
     "Discorso indiretto con passato remoto: futuro → condizionale composto (SAREBBE ANDATO)."),
    ("Loro venirono a trovarmi.",
     "Loro vennero a trovarmi.",
     "VENIRE irregolare: io venni, tu venisti, lui/lei VENNE, noi venimmo, voi veniste, loro VENNERO (non venirono)."),
    ("Ieri sera ho dormii male.",
     "Ieri sera ho dormito male.",
     "Passato prossimo: AVERE + participio passato (dormito). Non si usa la desinenza del pass. remoto (-ii) con l'ausiliare."),
    ("Colombo scoprì l'America nel 1492.",
     "Corretta.",
     "Forma corretta: passato remoto di scoprire (scoprire → scoprì). Fatto storico lontano."),
    ("Io feci quello che voleva fare.",
     "Io feci quello che volli fare. / Io feci quello che volevo fare.",
     "Nella narrazione: VOLLI (pass. remoto per azione puntuale) o VOLEVO (imperfetto per stato/volontà in corso)."),
    ("La formica cadde nel fiume e la colomba la salvava.",
     "La formica cadde nel fiume e la colomba la salvò.",
     "Nella narrazione consecutiva: entrambe le azioni sono puntuali → pass. remoto: CADDE e SALVÒ."),
    ("Mio nonno fu un uomo generoso.",
     "Corretta.",
     "FU = passato remoto di ESSERE (io fui, tu fosti, lui/lei FU). Forma corretta per descrizione storica puntuale."),
    ("Garibaldi morette nel 1882.",
     "Garibaldi morì nel 1882.",
     "MORIRE regolare: morì (3ª pers. sing.). 'Morette' non esiste in italiano."),
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
