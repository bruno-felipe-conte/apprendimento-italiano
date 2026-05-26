import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VI")

lez["titulo"] = "Il futuro semplice e composto"
lez["subtitulo"] = "Come formare e usare il futuro semplice e composto"

lez["teoria"] = """\
## Una vacanza nell'Italia meridionale

È estate e fra qualche settimana finiranno i corsi all'università. Paolo avrà circa venti giorni di vacanza e poi comincerà a lavorare come cameriere in un hotel. Farà questo lavoro per tutta la stagione estiva. In queste tre settimane di vacanza, lui e la sua ragazza hanno deciso di fare un viaggio nell'Italia meridionale. Partiranno da Firenze in macchina, così saranno liberi di fermarsi dove vorranno, e come prima tappa andranno a Napoli, dove hanno alcuni amici. Ci rimarranno una settimana e poi, dopo che avranno visitato gli scavi di Ercolano e di Pompei, prenderanno il traghetto per Capri. Qui saranno ospiti per alcuni giorni di una loro amica napoletana che possiede una casa sull'isola. Insieme andranno a vedere alcuni fra i posti più famosi del mondo: gli splendidi giardini, la villa di Tiberio, quella di Curzio Malaparte, la Grotta Azzurra e altri luoghi incantevoli. Infine torneranno a Napoli, per andare nel Lazio, sul lago di Bolsena, dove trascorreranno gli ultimi giorni di vacanza.

---

## A Il futuro semplice

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th>I -ARE (parlare)</th><th>II -ERE (prendere)</th><th>III -IRE (partire)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>parlerò</td><td>prenderò</td><td>partirò</td></tr>
<tr><td class="gram-art">tu</td><td>parlerai</td><td>prenderai</td><td>partirai</td></tr>
<tr><td class="gram-art">lui/lei/Lei</td><td>parlerà</td><td>prenderà</td><td>partirà</td></tr>
<tr><td class="gram-art">noi</td><td>parleremo</td><td>prenderemo</td><td>partiremo</td></tr>
<tr><td class="gram-art">voi</td><td>parlerete</td><td>prenderete</td><td>partirete</td></tr>
<tr><td class="gram-art">loro</td><td>parleranno</td><td>prenderanno</td><td>partiranno</td></tr>
</tbody>
</table>

> **Nota:** I verbi in **-CARE/-GARE** mantengono il suono duro: **cercare → cercherò**, **pagare → pagherò**.
> I verbi in **-CIARE/-GIARE** perdono la i: **cominciare → comincerò**, **mangiare → mangerò**.

---

## B Verbi con futuro irregolare

<table class="gram-table gram-table-rich">
<thead><tr><th>infinito</th><th>io</th><th>tu</th><th>lui/lei</th><th>noi</th><th>voi</th><th>loro</th></tr></thead>
<tbody>
<tr><td><strong>andare</strong></td><td>andrò</td><td>andrai</td><td>andrà</td><td>andremo</td><td>andrete</td><td>andranno</td></tr>
<tr><td><strong>avere</strong></td><td>avrò</td><td>avrai</td><td>avrà</td><td>avremo</td><td>avrete</td><td>avranno</td></tr>
<tr><td><strong>essere</strong></td><td>sarò</td><td>sarai</td><td>sarà</td><td>saremo</td><td>sarete</td><td>saranno</td></tr>
<tr><td><strong>bere</strong></td><td>berrò</td><td>berrai</td><td>berrà</td><td>berremo</td><td>berrete</td><td>berranno</td></tr>
<tr><td><strong>cadere</strong></td><td>cadrò</td><td>cadrai</td><td>cadrà</td><td>cadremo</td><td>cadrete</td><td>cadranno</td></tr>
<tr><td><strong>dovere</strong></td><td>dovrò</td><td>dovrai</td><td>dovrà</td><td>dovremo</td><td>dovrete</td><td>dovranno</td></tr>
<tr><td><strong>potere</strong></td><td>potrò</td><td>potrai</td><td>potrà</td><td>potremo</td><td>potrete</td><td>potranno</td></tr>
<tr><td><strong>rimanere</strong></td><td>rimarrò</td><td>rimarrai</td><td>rimarrà</td><td>rimarremo</td><td>rimarrete</td><td>rimarranno</td></tr>
<tr><td><strong>sapere</strong></td><td>saprò</td><td>saprai</td><td>saprà</td><td>sapremo</td><td>saprete</td><td>sapranno</td></tr>
<tr><td><strong>tenere</strong></td><td>terrò</td><td>terrai</td><td>terrà</td><td>terremo</td><td>terrete</td><td>terranno</td></tr>
<tr><td><strong>vedere</strong></td><td>vedrò</td><td>vedrai</td><td>vedrà</td><td>vedremo</td><td>vedrete</td><td>vedranno</td></tr>
<tr><td><strong>venire</strong></td><td>verrò</td><td>verrai</td><td>verrà</td><td>verremo</td><td>verrete</td><td>verranno</td></tr>
<tr><td><strong>volere</strong></td><td>vorrò</td><td>vorrai</td><td>vorrà</td><td>vorremo</td><td>vorrete</td><td>vorranno</td></tr>
</tbody>
</table>

---

## C Il futuro composto

Il futuro composto si forma con il **futuro semplice di essere o avere** + **participio passato**.

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th>con ESSERE (arrivare)</th><th>con AVERE (conoscere)</th><th>con ESSERE (dormire)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>sarò arrivato/a</td><td>avrò conosciuto</td><td>avrò dormito</td></tr>
<tr><td class="gram-art">tu</td><td>sarai arrivato/a</td><td>avrai conosciuto</td><td>avrai dormito</td></tr>
<tr><td class="gram-art">lui/lei</td><td>sarà arrivato/a</td><td>avrà conosciuto</td><td>avrà dormito</td></tr>
<tr><td class="gram-art">noi</td><td>saremo arrivati/e</td><td>avremo conosciuto</td><td>avremo dormito</td></tr>
<tr><td class="gram-art">voi</td><td>sarete arrivati/e</td><td>avrete conosciuto</td><td>avrete dormito</td></tr>
<tr><td class="gram-art">loro</td><td>saranno arrivati/e</td><td>avranno conosciuto</td><td>avranno dormito</td></tr>
</tbody>
</table>

> Il futuro composto esprime un'azione futura che sarà completata prima di un'altra azione futura:
> *Quando **avrò finito** i compiti, uscirò.*
> *Dopo che **avranno visitato** Pompei, prenderanno il traghetto.*

---

## D Un uso particolare del futuro

Il futuro può esprimere una **supposizione o probabilità** nel presente:

| domanda | risposta con probabilità |
|---|---|
| Quanti studenti ci sono nella tua classe? | Ci **saranno** quindici studenti. |
| Mario, sai che ore sono? | **Sarà** mezzogiorno. |
| A che ora siete tornati ieri sera? | **Saremo** tornati alle sette. |
| Chissà perché Carlo non è ancora arrivato! | **Avrà** perduto l'autobus. |

---

## E Vocabolario sistematico — Espressioni con "avere"

avere freddo · avere caldo · avere fame · avere sete · avere sonno · avere nostalgia · avere fretta · avere paura

Esempi:
- La finestra è aperta, **ho freddo**.
- Maria ha caldo perché ha fatto una corsa nel parco.
- Guido ieri non ha cenato e ora **ha fame**.
- Prendo un bicchiere d'acqua perché **ho molta sete**.
- **Ho sonno**, ma non riesco a dormire perché c'è troppo rumore.
- Maria **ha ancora nostalgia** della sua famiglia.
- Mi dispiace, ma ora **ho fretta**.
- Dobbiamo accompagnare Anna, perché **ha paura** di tornare a casa sola.
"""

lez["exemplos"] = [
    "Fra qualche settimana finiranno i corsi all'università.",
    "Partiranno da Firenze in macchina e si fermeranno dove vorranno.",
    "Quando avrò finito i compiti, andrò in piscina.",
    "Che ore sono? Saranno le cinque. (probabilità)",
    "Se non ci sarà sciopero, partirò sabato mattina.",
]

exercicios = []

# ── Domande sul testo ─────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Rispondere alle domande sul testo 'Una vacanza nell'Italia meridionale':",
    "pergunta": (
        "1. Fra quanto tempo finiranno i corsi all'università?\n"
        "2. Quanti giorni di vacanza avrà Paolo?\n"
        "3. E poi che cosa farà?\n"
        "4. Cosa hanno deciso di fare lui e la sua ragazza?\n"
        "5. Come ci andranno?\n"
        "6. Perché?\n"
        "7. Quale sarà la loro prima tappa?\n"
        "8. Quanto tempo ci rimarranno?\n"
        "9. Dove andranno dopo?\n"
        "10. Dove alloggeranno?\n"
        "11. Che cosa andranno a vedere?\n"
        "12. Che cosa faranno infine?"
    ),
    "resposta": (
        "1. Fra qualche settimana.\n"
        "2. Circa venti giorni.\n"
        "3. Lavorerà come cameriere in un hotel per tutta la stagione estiva.\n"
        "4. Di fare un viaggio nell'Italia meridionale.\n"
        "5. In macchina.\n"
        "6. Per essere liberi di fermarsi dove vorranno.\n"
        "7. Napoli.\n"
        "8. Una settimana.\n"
        "9. A Capri.\n"
        "10. Ospiti di una loro amica napoletana.\n"
        "11. I giardini, la villa di Tiberio, la villa di Malaparte, la Grotta Azzurra.\n"
        "12. Andranno nel Lazio, sul lago di Bolsena."
    )
})

# ── Esercizio 1 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1 — Volgere al futuro semplice:",
    "pergunta": (
        "1. (Io studiare) in questa scuola per imparare l'italiano.\n"
        "2. Luca (andare) a Napoli domani.\n"
        "3. Domani Marta (partire) e (tornare) nel suo Paese.\n"
        "4. (Io arrivare) alle due.\n"
        "5. (Io finire) di studiare e poi (andare) al cinema.\n"
        "6. So che domani Luigi (uscire) con Claudio.\n"
        "7. Questa sera (noi venire) a trovarti.\n"
        "8. Domani il professore (spiegare) una nuova lezione.\n"
        "9. Domenica sera (tu andare) in discoteca?\n"
        "10. Sabato prossimo (lei pagare) la bolletta della luce."
    ),
    "resposta": (
        "1. Studierò in questa scuola per imparare l'italiano.\n"
        "2. Luca andrà a Napoli domani.\n"
        "3. Domani Marta partirà e tornerà nel suo Paese.\n"
        "4. Arriverò alle due.\n"
        "5. Finirò di studiare e poi andrò al cinema.\n"
        "6. So che domani Luigi uscirà con Claudio.\n"
        "7. Questa sera verremo a trovarti.\n"
        "8. Domani il professore spiegherà una nuova lezione.\n"
        "9. Domenica sera andrai in discoteca?\n"
        "10. Sabato prossimo lei pagherà la bolletta della luce."
    )
})

# ── Esercizio 2 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 2 — Volgere al futuro semplice:",
    "pergunta": (
        "1. Per me domani (essere) una giornata faticosa.\n"
        "2. Domenica (noi andare) in montagna.\n"
        "3. (Io finire) il corso e poi (partire) per Berlino.\n"
        "4. Penso che domani (io rispondere) bene alle domande del professore.\n"
        "5. Spero che il bambino (dormire) bene questa notte.\n"
        "6. Mi ha detto che (partire) molto presto.\n"
        "7. Carla (non potere) venire al cinema con noi.\n"
        "8. Andrea (dovere) lavorare molto se (volere) guadagnare bene.\n"
        "9. (Io finire) i compiti e poi (andare) in piscina.\n"
        "10. (Voi rimanere) qui o (andare) in montagna per Natale?"
    ),
    "resposta": (
        "1. Per me domani sarà una giornata faticosa.\n"
        "2. Domenica andremo in montagna.\n"
        "3. Finirò il corso e poi partirò per Berlino.\n"
        "4. Penso che domani risponderò bene alle domande del professore.\n"
        "5. Spero che il bambino dormirà bene questa notte.\n"
        "6. Mi ha detto che partirà molto presto.\n"
        "7. Carla non potrà venire al cinema con noi.\n"
        "8. Andrea dovrà lavorare molto se vorrà guadagnare bene.\n"
        "9. Finirò i compiti e poi andrò in piscina.\n"
        "10. Rimarrete qui o andrete in montagna per Natale?"
    )
})

# ── Esercizio 3 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 3 — Volgere al futuro semplice:",
    "pergunta": (
        "1. Che cosa (tu fare) quando (essere) a Roma?\n"
        "2. (Io finire) di leggere il giornale e poi (preparare) la cena.\n"
        "3. (Tu vedere) che tutto (andare) bene.\n"
        "4. Se voi (non studiare), (non essere) promossi.\n"
        "5. (Noi parlare) a Gianni del tuo lavoro.\n"
        "6. Stasera (noi venire) alla tua festa.\n"
        "7. Anna (telefonare) a Giorgio.\n"
        "8. Che cosa (tu fare) da grande?\n"
        "9. Da grande (io scrivere) molti libri.\n"
        "10. Quando (voi essere) a Londra, (pensare) ancora a me?"
    ),
    "resposta": (
        "1. Che cosa farai quando sarai a Roma?\n"
        "2. Finirò di leggere il giornale e poi preparerò la cena.\n"
        "3. Vedrai che tutto andrà bene.\n"
        "4. Se non studierete, non sarete promossi.\n"
        "5. Parleremo a Gianni del tuo lavoro.\n"
        "6. Stasera verremo alla tua festa.\n"
        "7. Anna telefonerà a Giorgio.\n"
        "8. Che cosa farai da grande?\n"
        "9. Da grande scriverò molti libri.\n"
        "10. Quando sarete a Londra, penserete ancora a me?"
    )
})

# ── Esercizio 4 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 4 — Volgere al futuro semplice:",
    "pergunta": (
        "1. (Tu cantare) una canzone per me?\n"
        "2. Laura (volere) un altro caffè.\n"
        "3. (Loro telefonare) alle cinque del pomeriggio.\n"
        "4. (Io pagare) l'affitto quando (prendere) lo stipendio.\n"
        "5. Alla festa (noi conoscere) tuo marito.\n"
        "6. Questo pomeriggio Andrea (andare) dal barbiere.\n"
        "7. Quando (tu smettere) di fumare?\n"
        "8. Appena (io tornare) a casa, (fare) la doccia.\n"
        "9. Noi (mandare) i nostri bambini alla scuola pubblica.\n"
        "10. (Io non vedere) mai più quella persona."
    ),
    "resposta": (
        "1. Canterai una canzone per me?\n"
        "2. Laura vorrà un altro caffè.\n"
        "3. Telefoneranno alle cinque del pomeriggio.\n"
        "4. Pagherò l'affitto quando prenderò lo stipendio.\n"
        "5. Alla festa conosceremo tuo marito.\n"
        "6. Questo pomeriggio Andrea andrà dal barbiere.\n"
        "7. Quando smetterai di fumare?\n"
        "8. Appena tornerò a casa, farò la doccia.\n"
        "9. Noi manderemo i nostri bambini alla scuola pubblica.\n"
        "10. Non vedrò mai più quella persona."
    )
})

# ── Esercizio 5 (items 7-10 dal libro, gli altri non sono nell'OCR) ───────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 5 — Completare con il futuro semplice (trasformare il verbo tra parentesi):",
    "pergunta": (
        "7. Passerò qualche giorno al mare e poi _____ a Firenze.\n"
        "8. Venderò la mia macchina e poi ne _____ una nuova.\n"
        "9. Esaminerò la tua proposta e poi _____ cosa fare.\n"
        "10. Comprerò gli sci e poi _____ a sciare.\n\n"
        "(tornare / comprare / decidere / imparare)"
    ),
    "resposta": (
        "7. ...tornerò a Firenze.\n"
        "8. ...ne comprerò una nuova.\n"
        "9. ...deciderò cosa fare.\n"
        "10. ...imparerò a sciare."
    )
})

# ── Conversazione ─────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Conversazione — Al bar con gli amici (leggere il dialogo):",
    "pergunta": (
        "Maria: Perché dopo la lezione non andiamo al bar a bere qualcosa?\n"
        "Laura: Buona idea, così finalmente potremo fare due chiacchiere. Vieni anche tu Giulia?\n"
        "Giulia: Mi dispiace, ma sono di fretta: fra un quarto d'ora devo essere dall'altra parte della città e ho i minuti contati. Comunque, grazie. A presto!\n"
        "Laura: Sarà per un'altra volta, ciao Giulia! E Lei, Paolo, che fa?\n"
        "Paolo: Io vengo con voi.\n"
        "Maria: Laura, che cosa prendi?\n"
        "Laura: Un tè al limone e una pasta.\n"
        "Maria: Ma come, sei a dieta e mangi i dolci?\n"
        "Laura: Sì, hai ragione, i dolci fanno ingrassare, ma sono tanto buoni!\n"
        "Maria: Anche Lei, Paolo, prende un tè?\n"
        "Paolo: No, grazie, preferisco una bibita fresca... un succo d'arancia.\n"
        "Maria: Cameriere, per favore, un tè al limone e una pasta per la signora; un succo d'arancia per il signore e per me un caffè macchiato e un bicchiere d'acqua minerale. L'acqua con un po' di ghiaccio, muoio dalla sete."
    ),
    "resposta": "Dialogo al bar con ordini al cameriere."
})

# ── Vocabolario sistematico — Espressioni con avere ───────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Vocabolario sistematico — Espressioni con 'avere' (completare con la frase corretta):",
    "pergunta": (
        "Spiegare il significato e usare in una frase:\n"
        "1. avere freddo\n"
        "2. avere caldo\n"
        "3. avere fame\n"
        "4. avere sete\n"
        "5. avere sonno\n"
        "6. avere nostalgia\n"
        "7. avere fretta\n"
        "8. avere paura"
    ),
    "resposta": (
        "1. La finestra è aperta, ho freddo.\n"
        "2. Maria ha caldo perché ha fatto una corsa.\n"
        "3. Guido non ha cenato e ora ha fame.\n"
        "4. Prendo un bicchiere d'acqua perché ho sete.\n"
        "5. Ho sonno ma non riesco a dormire.\n"
        "6. Maria vive all'estero e ha nostalgia della sua famiglia.\n"
        "7. Mi dispiace, ho fretta, non posso fermarmi.\n"
        "8. Ha paura di tornare a casa da sola di notte."
    )
})

# ── Storia di parole ──────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Storia di parole — Etimologia di alcune parole scolastiche:",
    "pergunta": (
        "Leggere e commentare l'etimologia delle seguenti parole:\n"
        "SCUOLA — dal greco skole = 'ozio, riposo, tempo libero'\n"
        "PROFESSORE — dal latino profiteri = 'dichiarare pubblicamente' → insegnare\n"
        "ALUNNO — dal latino alere = 'nutrire' → persona nutrita intellettualmente\n"
        "QUADERNO — dal latino quaterni = 'a quattro a quattro' → 4 fogli di carta\n"
        "MATITA — dal greco haematites = nome di una pietra rossa usata per disegnare\n"
        "MAESTRO — dal latino magister → da magis = 'di più' → chi sa di più e può guidare"
    ),
    "resposta": "Etimologie delle parole scolastiche più comuni."
})

# ── Esercizio 6 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 6 — Volgere al futuro semplice:",
    "pergunta": (
        "1. Domani (noi partire) con Lucia per Roma.\n"
        "2. Cosa (raccontare) Piero ai suoi genitori?\n"
        "3. Quando (tu preparare) la torta?\n"
        "4. Aldo (non sapere) mai la verità.\n"
        "5. Se (io comprare) questo vestito, (rimanere) senza soldi.\n"
        "6. A che ora (loro andare) a casa di Roberto?\n"
        "7. Chi (lavare) i piatti?\n"
        "8. Tuo padre (dormire) a casa nostra.\n"
        "9. Se (tu prendere) questa medicina, (stare) meglio.\n"
        "10. Chi di voi (partecipare) alla gita?"
    ),
    "resposta": (
        "1. Domani partiremo con Lucia per Roma.\n"
        "2. Cosa racconterà Piero ai suoi genitori?\n"
        "3. Quando preparerai la torta?\n"
        "4. Aldo non saprà mai la verità.\n"
        "5. Se comprerò questo vestito, rimarrò senza soldi.\n"
        "6. A che ora andranno a casa di Roberto?\n"
        "7. Chi laverà i piatti?\n"
        "8. Tuo padre dormirà a casa nostra.\n"
        "9. Se prenderai questa medicina, starai meglio.\n"
        "10. Chi di voi parteciperà alla gita?"
    )
})

# ── Esercizio 7 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 7 — Volgere al futuro semplice:",
    "pergunta": (
        "1. Stasera (io telefonare) a Paolo.\n"
        "2. (Io finire) di vedere il film e poi (andare) a letto.\n"
        "3. Domani gli studenti (visitare) la chiesa di San Miniato.\n"
        "4. Quando (nascere) tuo figlio?\n"
        "5. (Io regalare) a Renato questo disco.\n"
        "6. Giulio (scrivere) una lettera appena (arrivare) in Australia.\n"
        "7. La partita (durare) novanta minuti.\n"
        "8. Domani (io passare) la mattinata in biblioteca.\n"
        "9. Quando (voi buttare) questi vecchi libri?\n"
        "10. Per andare alla festa (io mettersi) il vestito azzurro."
    ),
    "resposta": (
        "1. Stasera telefonerò a Paolo.\n"
        "2. Finirò di vedere il film e poi andrò a letto.\n"
        "3. Domani gli studenti visiteranno la chiesa di San Miniato.\n"
        "4. Quando nascerà tuo figlio?\n"
        "5. Regalerò a Renato questo disco.\n"
        "6. Giulio scriverà una lettera appena arriverà in Australia.\n"
        "7. La partita durerà novanta minuti.\n"
        "8. Domani passerò la mattinata in biblioteca.\n"
        "9. Quando butterete questi vecchi libri?\n"
        "10. Per andare alla festa mi metterò il vestito azzurro."
    )
})

# ── Esercizio 8 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8 — Volgere al futuro semplice:",
    "pergunta": (
        "1. Spero che domani Lisa (essere) puntuale all'appuntamento.\n"
        "2. Noi (andare) a pranzo fuori e poi a lezione.\n"
        "3. Il dottore ha detto che (lui guarire) presto.\n"
        "4. Quando (io essere) in ferie, (viaggiare) per l'Italia.\n"
        "5. Ragazzi, per domani (voi fare) il seguente esercizio.\n"
        "6. (Tu sapere) tutto al momento giusto.\n"
        "7. Quali musei (tu visitare) a Roma?\n"
        "8. (Io amare) quell'uomo per tutta la vita.\n"
        "9. (Finire) presto questa bella vacanza!\n"
        "10. (Voi leggere) più tardi il giornale."
    ),
    "resposta": (
        "1. Spero che domani Lisa sarà puntuale all'appuntamento.\n"
        "2. Noi andremo a pranzo fuori e poi a lezione.\n"
        "3. Il dottore ha detto che guarirà presto.\n"
        "4. Quando sarò in ferie, viaggerò per l'Italia.\n"
        "5. Ragazzi, per domani farete il seguente esercizio.\n"
        "6. Saprai tutto al momento giusto.\n"
        "7. Quali musei visiterai a Roma?\n"
        "8. Amerò quell'uomo per tutta la vita.\n"
        "9. Finirà presto questa bella vacanza!\n"
        "10. Leggerete più tardi il giornale."
    )
})

# ── Esercizio 9 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 9 — Volgere al futuro semplice:",
    "pergunta": (
        "1. Dove (tu trascorrere) le vacanze?\n"
        "2. (Noi potere) uscire quando (arrivare) Luca.\n"
        "3. (Voi partire) per il Brasile la settimana prossima?\n"
        "4. (Noi tornare) a casa a piedi perché c'è lo sciopero degli autobus.\n"
        "5. Il film (cominciare) alle otto e (finire) dopo due ore.\n"
        "6. Sabato prossimo l'Italia (giocare) contro la Germania.\n"
        "7. (Io venire) alla festa, ma (non potere) bere niente.\n"
        "8. L'estate prossima (arrivare) molti turisti a Firenze.\n"
        "9. Ora che hai perso il portafoglio, come (pagare) il conto dell'albergo?\n"
        "10. Chi (andare) a prendere Marco alla stazione?"
    ),
    "resposta": (
        "1. Dove trascorrerai le vacanze?\n"
        "2. Potremo uscire quando arriverà Luca.\n"
        "3. Partirete per il Brasile la settimana prossima?\n"
        "4. Torneremo a casa a piedi perché c'è lo sciopero degli autobus.\n"
        "5. Il film comincerà alle otto e finirà dopo due ore.\n"
        "6. Sabato prossimo l'Italia giocherà contro la Germania.\n"
        "7. Verrò alla festa, ma non potrò bere niente.\n"
        "8. L'estate prossima arriveranno molti turisti a Firenze.\n"
        "9. Come pagherai il conto dell'albergo?\n"
        "10. Chi andrà a prendere Marco alla stazione?"
    )
})

# ── Lavorare sul testo ────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lavorare sul testo — 'Un pomeriggio in casa' (rispondere + composizione guidata):",
    "pergunta": (
        "Fra due giorni ci sarà un giorno di festa e la famiglia Rossi sarà riunita sotto lo "
        "stesso tetto. Il signor Rossi non dovrà andare in ufficio e così dedicherà la mattinata "
        "alla famiglia e il pomeriggio al suo passatempo preferito: il giardinaggio. La signora "
        "Rossi, invece, verso le cinque riceverà alcune amiche; prenderanno il tè con i "
        "pasticcini e faranno una chiacchierata. Mario, il figlio maggiore, non andrà "
        "all'università e così aiuterà il padre a tagliare l'erba del giardino, poi, quando le "
        "amiche della madre saranno andate via, farà qualche esercizio al pianoforte. Laura, "
        "la figlia minore, passerà come al solito molto tempo al telefono a parlare con la sua "
        "migliore amica e poi, se non uscirà, andrà in salotto a finire di leggere un "
        "appassionante giallo. Sarà bello passare un pomeriggio sereno con tutta la famiglia.\n\n"
        "Composizione guidata — Usare le seguenti parole per scrivere un racconto:\n"
        "giorno di festa · finire · passatempo · gelato · fare una chiacchierata · raccontare · migliore · gatto · piangere"
    ),
    "resposta": (
        "Il signor Rossi non lavorerà; dedicherà la mattinata alla famiglia e il pomeriggio al giardinaggio.\n"
        "La signora riceverà amiche per il tè.\n"
        "Mario aiuterà il padre e poi suonerà il pianoforte.\n"
        "Laura telefonerà e leggerà un giallo.\n"
        "Sarà una giornata di festa serena."
    )
})

# ════════════════════════════════════════════════════════════════════════════════
# ESERCIZI DI VERIFICA — 20 escolha
# ════════════════════════════════════════════════════════════════════════════════

verifica = [
    # 1
    {"pergunta": "A maggio ___",
     "opcoes": ["finaro l'università.", "finirò l'università.", "finero l'università."],
     "resposta": 1},
    # 2
    {"pergunta": "Quando ___ casa?",
     "opcoes": ["cambierai", "cambirai", "cambiérai"],
     "resposta": 0},
    # 3
    {"pergunta": "Il bambino ___ alla fine dell'anno.",
     "opcoes": ["nascerà", "naschera", "nascerà alla fine dell'anno"],
     "resposta": 0},
    # 4
    {"pergunta": "Alla festa ___ gli amici di Roberto.",
     "opcoes": ["incontraremo", "incontreremo", "incontrerò"],
     "resposta": 1},
    # 5
    {"pergunta": "___ sciopero, partirò sabato mattina.",
     "opcoes": ["Se non ci sera", "Se non ci era", "Se non ci sarà"],
     "resposta": 2},
    # 6
    {"pergunta": "___ una pensione per i miei genitori.",
     "opcoes": ["Cercaro", "Cercherò", "Cerchero"],
     "resposta": 1},
    # 7
    {"pergunta": "Come ___ a Londra: in treno o in aereo?",
     "opcoes": ["anderai", "andrai", "andarai"],
     "resposta": 1},
    # 8
    {"pergunta": "Il primo di novembre ___ il riscaldamento.",
     "opcoes": ["accenderanno", "accendaranno", "accenderono"],
     "resposta": 0},
    # 9
    {"pergunta": "Non ___ mai quel giorno.",
     "opcoes": ["dimenticaro", "dimenticherò", "dimentichero"],
     "resposta": 1},
    # 10
    {"pergunta": "A che ora ___ a Firenze?",
     "opcoes": ["arrivarai", "arriverai", "arrivarei"],
     "resposta": 1},
    # 11
    {"pergunta": "Se smetterà di fumare non ___ più la tosse.",
     "opcoes": ["avera", "avrà", "avara"],
     "resposta": 1},
    # 12
    {"pergunta": "___ sei mesi in Italia.",
     "opcoes": ["Rimanero", "Rimanaro", "Rimarrò"],
     "resposta": 2},
    # 13
    {"pergunta": "Quando mi ___ la cena che mi hai promesso?",
     "opcoes": ["pagerai", "pagarai", "pagherai"],
     "resposta": 2},
    # 14
    {"pergunta": "Se farai una festa ___ volentieri.",
     "opcoes": ["ci veniro", "ci venro", "ci verrò"],
     "resposta": 2},
    # 15
    {"pergunta": "Quando la nuova autostrada ___ il viaggio sarà molto più breve.",
     "opcoes": ["sarà finita", "sara finita", "finira"],
     "resposta": 0},
    # 16
    {"pergunta": "Quando ___ casa, inviterò tutti gli amici.",
     "opcoes": ["trovo", "avero trovato", "avrò trovato"],
     "resposta": 2},
    # 17
    {"pergunta": "___ Luisa tra un mese, quando tornerà a casa.",
     "opcoes": ["Verrò", "Vedero", "Vedrò"],
     "resposta": 2},
    # 18
    {"pergunta": "Presto ___ quando ci saranno gli esami.",
     "opcoes": ["saperemo", "sappremo", "sapremo"],
     "resposta": 2},
    # 19
    {"pergunta": "Che ore sono? Non ho l'orologio, ___",
     "opcoes": ["ma sono le cinque.", "ma saranno le cinque."],
     "resposta": 1},
    # 20
    {"pergunta": "Sai quanto costa? Non so, ___",
     "opcoes": ["costa dieci euro trentatré centesimi.", "costerà dieci euro trentatré centesimi."],
     "resposta": 1},
]

for v in verifica:
    exercicios.append({
        "tipo": "escolha",
        "enunciado": "Scegliere la forma corretta:",
        "pergunta": v["pergunta"],
        "opcoes": v["opcoes"],
        "resposta": v["resposta"]
    })

# ── Trovare gli errori ────────────────────────────────────────────────────────
errori = [
    ("Rimanero qui fino a giugno.",
     "Rimarrò qui fino a giugno."),
    ("Se arriverai tardi, veniro a prenderti alla stazione.",
     "Se arriverai tardi, verrò a prenderti alla stazione."),
    ("Oggi non posso, ci andero domani. (nessun errore nella logica)",
     "Oggi non posso, ci andrò domani."),
    ("Quando Mario vedera il regalo, sarà molto contento.",
     "Quando Mario vedrà il regalo, sarà molto contento."),
    ("Adesso non ho soldi, pagero la prossima settimana.",
     "Adesso non ho soldi, pagherò la prossima settimana."),
    ("Doveremo assolutamente essere puntuali.",
     "Dovremo assolutamente essere puntuali."),
    ("Quando ci seranno le prossime elezioni politiche?",
     "Quando ci saranno le prossime elezioni politiche?"),
    ("Finiro gli studi in un anno.",
     "Finirò gli studi in un anno."),
    ("Non è ancora arrivato, ma venira fra poco.",
     "Non è ancora arrivato, ma verrà fra poco."),
    ("Leggero questo libro quando potero.",
     "Leggerò questo libro quando potrò."),
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
print(f"OK: Lezione VI — Il futuro semplice e composto")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(exercicios)} total (escolha: {n_e}, revelar: {n_r})")
