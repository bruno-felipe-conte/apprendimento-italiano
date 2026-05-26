import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione X"), None)
if lez is None:
    lez = {"id": "a1-lez10", "num": "Lezione X", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I pronomi indiretti"
lez["subtitulo"] = "Pronomi personali — complemento indiretto e diretto"

lez["teoria"] = """\
## I regali di Natale

Maria e Paolo sono davanti a un negozio. Maria propone di entrare a comprare i regali di Natale per i loro genitori. Paolo è d'accordo ma vuole prima guardare la vetrina. Nella vetrina notano una borsetta. Paolo preferisce quella marrone, che secondo lui starà bene con il cappotto color nocciola della madre. Entrano e chiedono al commesso di vedere la borsetta marrone. Il commesso dice che è molto elegante e che il prezzo è ottimo. Maria la trova graziosa e la pelle morbida, ma precisa che non è per lei, è per la loro madre. Paolo decide di prendere la borsetta. Poi Paolo vuole vedere una sciarpa per il padre, ma Maria ricorda che gliene ha già regalata una l'anno scorso. Propone invece una cravatta o un paio di guanti di pelle. Il commesso li informa che gli articoli da uomo si trovano al secondo piano.

---

## Pronomi personali — complemento indiretto e diretto

<table class="gram-table gram-table-rich">
<thead>
<tr>
  <th class="gram-art" rowspan="2">Soggetto</th>
  <th colspan="2" class="gram-genere">Complemento indiretto (a chi?)</th>
  <th colspan="2" class="gram-genere">Complemento diretto (chi?)</th>
</tr>
<tr>
  <th class="gram-art">tonico</th>
  <th class="gram-art">atono</th>
  <th class="gram-art">tonico</th>
  <th class="gram-art">atono</th>
</tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>a me</td><td><strong>mi</strong></td><td>me</td><td><strong>mi</strong></td></tr>
<tr><td class="gram-art">tu</td><td>a te</td><td><strong>ti</strong></td><td>te</td><td><strong>ti</strong></td></tr>
<tr><td class="gram-art">lui (egli)</td><td>a lui</td><td><strong>gli</strong></td><td>lui</td><td><strong>lo</strong></td></tr>
<tr><td class="gram-art">lei (ella)</td><td>a lei</td><td><strong>le</strong></td><td>lei</td><td><strong>la</strong></td></tr>
<tr><td class="gram-art">Lei (formale)</td><td>a Lei</td><td><strong>Le</strong></td><td>Lei</td><td><strong>La</strong></td></tr>
<tr><td class="gram-art">noi</td><td>a noi</td><td><strong>ci</strong></td><td>noi</td><td><strong>ci</strong></td></tr>
<tr><td class="gram-art">voi</td><td>a voi</td><td><strong>vi</strong></td><td>voi</td><td><strong>vi</strong></td></tr>
<tr><td class="gram-art">essi/esse</td><td>a loro</td><td><strong>gli</strong> (loro)*</td><td>loro</td><td><strong>li / le</strong></td></tr>
</tbody>
</table>

> \* **Loro** non è una forma atona e la sua posizione è **dopo** il verbo. Es.: *Carlo scrive loro una lettera.*
> Il pronome indiretto formale **Le** si usa tanto per il maschile che per il femminile.

---

## Presente e passato prossimo

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">frase con tonico</th><th class="gram-art">presente (atono)</th><th class="gram-art">passato prossimo</th></tr>
</thead>
<tbody>
<tr><td>Gianni scrive <strong>a me</strong></td><td>Gianni <strong>mi</strong> scrive</td><td><strong>mi</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>a te</strong></td><td>Gianni <strong>ti</strong> scrive</td><td><strong>ti</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>a Paolo</strong></td><td>Gianni <strong>gli</strong> scrive</td><td><strong>gli</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>a Luisa</strong></td><td>Gianni <strong>le</strong> scrive</td><td><strong>le</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>a Lei</strong></td><td>Gianni <strong>Le</strong> scrive</td><td><strong>Le</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>a noi</strong></td><td>Gianni <strong>ci</strong> scrive</td><td><strong>ci</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>a voi</strong></td><td>Gianni <strong>vi</strong> scrive</td><td><strong>vi</strong> ha scritto</td></tr>
<tr><td>Gianni scrive <strong>ai ragazzi</strong></td><td>Gianni <strong>gli</strong> scrive (oppure: scrive loro)</td><td><strong>gli</strong> ha scritto (ha scritto loro)</td></tr>
</tbody>
</table>

---

## ATTENZIONE — Con i verbi servili

Con i verbi **dovere / potere / volere / sapere**, il pronome indiretto può andare **prima del verbo servile** (forma atona) oppure **dopo l'infinito** (attaccato):

| forma separata | forma unita |
|---|---|
| Ragazzi, **mi** dovete fare un favore. | Ragazzi, dovete far**mi** un favore. |
| Luisa, **ti** voglio dire la verità. | Luisa, voglio dir**ti** la verità. |
| Signore, quando **Le** posso telefonare? | Signore, quando posso telefonar**Le**? |
| **Ci** sai spiegare questa parola? | Sai spiegar**ci** questa parola? |
| Non **vi** posso rispondere ora. | Non posso risponder**vi** ora. |

---

## Il verbo PIACERE

Il verbo **piacere** funziona diversamente: il **soggetto** è la cosa che piace, e la **persona** è il complemento indiretto.

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto grammaticale</th><th class="gram-genere">forma informale (tu)</th><th class="gram-genere">forma formale (Lei)</th></tr>
</thead>
<tbody>
<tr><td>singolare (es. film)</td><td>Carlo, <strong>ti piace</strong> questo film?<br>Sì, <strong>mi piace</strong> molto.</td><td>Signore, <strong>Le piace</strong> questo film?<br>Sì, <strong>mi piace</strong> molto.</td></tr>
<tr><td>plurale (es. rose)</td><td>Laura, <strong>ti piacciono</strong> queste rose?<br>Sì, <strong>mi piacciono</strong> molto.</td><td>Signora, <strong>Le piacciono</strong> queste rose?<br>Sì, <strong>mi piacciono</strong> molto.</td></tr>
</tbody>
</table>

> **Osservate:** Come **piacere** funzionano anche: *sembrare, occorrere, bastare, servire, interessare, importare, mancare.*

---

## Conversazione — Alla stazione

**(Ufficio informazioni)**

— Domani devo essere a Bolzano verso mezzogiorno; che treno posso prendere?
— Non c'è un diretto da Firenze per Bolzano: deve cambiare a Bologna e aspettare la coincidenza. Parte da Firenze alle sette e ventitre e prende l'espresso 772 che arriva a Bologna alle otto e trenta; poi, alle otto e quaranta, prende il diretto per Bolzano e arriverà alle dodici e venticinque.
— Da quale binario parte l'espresso?
— Dal numero nove.
— Grazie tante e arrivederLa. — ArrivederLa.

**(Alla biglietteria)**

— Un biglietto di andata e ritorno per Bolzano. — Di prima o seconda classe?
— Di seconda. — Sono quindici euro sessanta centesimi. — Grazie.

**(In treno)**

— Scusi signora, è libero quel posto?
— Mi dispiace, quello accanto al finestrino è occupato, ma questo qui è libero, se vuole si può accomodare.
— Grazie, ma vedo che questo è uno scompartimento per fumatori; io non fumo, perciò preferisco cercare un altro posto. ArrivederLa.

---

## Vocabolario sistematico — I gradi di parentela

- **Paolo** è il marito di Maria, il padre di Giulia e di Mario, il suocero di Guido e di Linda, il nonno di Simone e di Elena.
- **Maria** è la moglie di Paolo, la madre di Mario e di Giulia, la suocera di Linda e di Guido, la nonna di Simone e di Elena.
- **Giulia** è la figlia di Paolo e di Maria, la sorella di Mario, la cognata di Linda, la zia di Elena.
- **Mario** è il figlio di Paolo e di Maria, il fratello di Giulia, il cognato di Guido, lo zio di Simone.
- **Guido** è il genero di Paolo e Maria.
- **Linda** è la nuora di Paolo e Maria.
- **Simone** è il nipote di Paolo e Maria, il cugino di Elena, il nipote di Mario e Linda.
- **Elena** è la nipote di Paolo e Maria, la cugina di Simone, la nipote di Guido e Giulia.

---

## Storia di parole

**Ciao** — Deriva dal veneziano *sciao*, forma abbreviata di "(sono suo) schiavo"; in passato era una formula ossequiosa di commiato. Oggi è un saluto molto confidenziale.

**Salve** — Deriva dalla seconda persona singolare del verbo latino *salvere* "star bene". Si usa come formula per dare il benvenuto, raramente come formula di commiato. Significa "stai bene", "salute a te".

**Addio** — Composto da "a" e "Dio", significa "ti raccomando a Dio". È un saluto molto affettuoso e si usa per esprimere il dispiacere di lasciare una persona cara.

---

## L'uso di appena

**a)** *Francesco è **appena** arrivato a Firenze.* (= da poco / poco fa)
**b)** *È in casa Laura? No, è **appena** uscita.* (= da un momento)
**c)** ***Appena** avrai finito di lavorare, vieni a casa mia.* (= non appena / subito dopo)
**d)** *Le scriverò **appena** Carlo mi avrà dato il suo indirizzo.* (futuro anteriore + futuro semplice)
"""

lez["exemplos"] = [
    "Carlo mi dà il libro. (indiretto atono = mi)",
    "Anna ti telefonerà. (indiretto atono = ti)",
    "Domani gli scriverò. (a lui → gli)",
    "Le consiglio di restare, signora. (formale → Le)",
    "Ti piace questo film? — Sì, mi piace molto.",
]

EX = []

# Domande sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — I regali di Natale:\n1. Cosa vogliono comprare Maria e Paolo?\n2. Che cosa vedono nella vetrina del negozio?\n3. Perché Paolo preferisce la borsetta marrone?\n4. Com'è la borsetta marrone?\n5. Che cosa vuole vedere Paolo?\n6. Di che cosa è sicuro il commesso?\n7. Perché Maria suggerisce un altro regalo?\n8. Che cosa vuole vedere Maria?\n9. Dove tengono gli articoli da uomo?",
    "resposta": "1. Vogliono comprare i regali di Natale per i loro genitori.\n2. Vedono una borsetta nella vetrina.\n3. Perché starà bene con il cappotto color nocciola della mamma.\n4. È molto elegante, graziosa e la pelle è morbida.\n5. Vuole vedere una sciarpa per suo padre.\n6. È sicuro che la signora (la madre) resterà soddisfatta.\n7. Perché Paolo ha già regalato una sciarpa al padre l'anno scorso.\n8. Vuole vedere una cravatta o un paio di guanti di pelle.\n9. Li tengono al secondo piano.",
    "explicacao": "Lettura del dialogo: pronomi indiretti, verbo piacere e lessico del negozio."
})

# Esercizio 1
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Completare con i pronomi indiretti:\n1. Luisa ___ ha scritto diverse volte, ma io non ___ ho ancora risposto.\n2. Hai telefonato alla segretaria? Sì, ___ ho telefonato.\n3. Quando hai risposto ai ragazzi? ___ ho risposto la settimana scorsa.\n4. Hai risposto alle ragazze? Sì, ___ ho risposto.\n5. Hai scritto al tuo ragazzo? Sì, ___ ho scritto.\n6. È una donna molto nervosa, non ___ si può dire nulla!\n7. Carla, stasera non ___ posso invitare a casa mia perché sono fuori a cena.\n8. Giovanni l'ha chiamata e ___ ha detto che può prestar___ la macchina.\n9. Quando li ho visti, ___ ho spiegato tutto.\n10. Quando le ho viste, ___ ho spiegato tutto.\n11. I tuoi amici ___ hanno chiesto una mano, ma io ___ ho detto che non posso aiutarli.\n12. Una studentessa ___ ha chiesto di spiegarle la regola un'altra volta.\n13. Roberto ha superato l'esame e suo padre ___ farà un regalo.\n14. È il compleanno di sua moglie e lui ___ regalerà un mazzo di fiori.\n15. Gli studenti non hanno capito l'uso dei pronomi e ho dovuto ripetere la spiegazione ___ .\n16. Sei un bugiardo: non ___ crederò più una parola di quello che dirai.\n17. Le ho invitate a casa e ho offerto ___ un tè e dei biscotti.\n18. Ho detto a mio figlio che non ___ posso dare in prestito la mia auto perché ___ serve.",
    "resposta": "1. le / le\n2. le\n3. Gli\n4. le\n5. gli\n6. le / ci\n7. ti\n8. le / le\n9. gli\n10. gli\n11. mi / gli\n12. mi\n13. gli\n14. le\n15. loro / gli\n16. ti\n17. loro / gli\n18. gli / mi",
    "explicacao": "Pronomi indiretti atoni: mi (a me), ti (a te), gli (a lui/loro m.), le (a lei/lei f.), ci (a noi), vi (a voi)."
})

# Esercizio 2
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Come il precedente:\n1. Signorina, ___ posso presentare mia moglie?\n2. Signor Farini, ___ presento mia figlia.\n3. Voglio vedere Mario perché ___ devo parlare.\n4. Ha detto alle ragazze che ___ telefonerà domani.\n5. Ha detto ai ragazzi che ___ telefonerà domani.\n6. ___ devi fare un grosso favore. ___ devi prestare cinque euro sedici centesimi.\n7. Carlo, ___ serve il tuo aiuto.\n8. Lui non sa tenere la bocca chiusa: a quest'ora ciò che ___ hai detto lo sapranno tutti.\n9. È una ragazza pettegola, se ___ dici una cosa, dopo poco la sanno tutti.\n10. Suo marito è davvero sfortunato: ieri sera ___ hanno rubato il portafoglio.\n11. Se quei ragazzi mi cercano, ___ devi dire che ritorno domani.\n12. Se quelle ragazze mi cercano, ___ devi dire che sarò in casa alle sette.\n13. Ho avvertito Carlo e ___ ho detto di venire più tardi.\n14. Ho telefonato a sua sorella e ___ ho detto di non venire.\n15. Ho cercato di far___ cambiare idea, ma non ___ hanno dato ascolto.\n16. Sono andato a casa di Mario e ho cercato di far___ cambiare idea.\n17. Ho incontrato tua moglie e ___ ho presentato mio marito.\n18. Ho incontrato il mio principale e ___ ho presentato mio marito.",
    "resposta": "1. Le\n2. Le\n3. gli\n4. gli\n5. gli\n6. Mi / Mi\n7. mi\n8. gli\n9. le / ci\n10. gli\n11. gli\n12. le\n13. gli\n14. le\n15. loro / mi / gli\n16. gli\n17. le\n18. gli",
    "explicacao": "Pronome formale Le (signorina/signor). Gli = a lui / a loro (masch. plur.). Le = a lei."
})

# Esercizio 3
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Sostituire alle forme toniche dei pronomi le forme atone:\n1. Se scrivi a me, risponderò a te subito.\n2. La madre di Carla ha raccontato a noi la sua vita.\n3. Raccomando a voi di leggere questo libro.\n4. Il direttore ha consegnato a lei il diploma.\n5. Voglio dire a Lui quello che penso.\n6. La nonna regala a te un orologio.\n7. Ricordo a loro l'appuntamento.\n8. Laura vuole molto bene a noi.\n9. Restituiremo a Lei i soldi domani.\n10. Mia sorella deve portare a me delle riviste.\n11. Posso fare a te una domanda?\n12. Telefono a Lei domani.",
    "resposta": "1. Se mi scrivi, ti risponderò subito.\n2. La madre di Carla ci ha raccontato la sua vita.\n3. Vi raccomando di leggere questo libro.\n4. Il direttore le ha consegnato il diploma.\n5. Gli voglio dire quello che penso.\n6. La nonna ti regala un orologio.\n7. Gli ricordo l'appuntamento.\n8. Laura ci vuole molto bene.\n9. Le restituiremo i soldi domani.\n10. Mia sorella mi deve portare delle riviste.\n11. Posso farti una domanda?\n12. Le telefono domani.",
    "explicacao": "Tonico → atono: a me→mi, a te→ti, a lui→gli, a lei→le, a Lei→Le, a noi→ci, a voi→vi, a loro→gli/loro."
})

# Esercizio 4
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Volgere al presente (Mod.: Questo libro (sembrarmi) → mi sembra interessante):\n1. I suoi figli (sembrarmi) molto educati.\n2. Quella tua amica (sembrarmi) un po' insicura.\n3. Come (sembrarti) queste scarpe? (Piacerti)?\n4. (Non occorrermi) quei documenti.\n5. (Non occorrermi) la macchina, vado a piedi.\n6. Ragazzi, (bastarvi) questo vino?\n7. Se non (bastarti) questi francobolli, puoi comprarne degli altri.\n8. Signorina, (bastarLe) questi soldi?\n9. (Servirmi) diecimila lire, me le presti?\n10. Signorina, cosa (servirLe)? (Servirmi) delle buste.\n11. Buongiorno! (Servirmi) alcuni libri, ecco la lista.\n12. (Non occorrerti) né carta né penna, ho tutto io.\n13. Questi libri (occorrerLe) subito?\n14. (Non interessarmi) vedere questo spettacolo.\n15. Non (importarmi) quello che pensate di me!\n16. (InteressarLe) questi gioielli?\n17. (Non piacerci) quello che ha detto quell'uomo.\n18. (Piacermi) molto i suoi occhi.\n19. Ho saputo che (interessarti) questo quadro.\n20. È incontentabile! Non (bastarle) mai nulla.",
    "resposta": "1. mi sembrano\n2. mi sembra\n3. ti sembrano? ti piacciono?\n4. Non mi occorrono\n5. Non mi occorre\n6. vi basta\n7. non ti bastano\n8. Le bastano\n9. Mi servono\n10. Le serve? Mi servono\n11. Mi servono\n12. Non ti occorrono\n13. Le occorrono\n14. Non mi interessa\n15. Non mi importa\n16. Le interessano\n17. Non ci piace\n18. Mi piacciono\n19. ti interessa\n20. Non le basta",
    "explicacao": "Verbi come piacere: il soggetto è la cosa, la persona è complemento indiretto. Sing. → piace/serve/basta; Plur. → piacciono/servono/bastano."
})

# Esercizio 5
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Completare con i pronomi diretti o indiretti:\n1. Non conosco bene Maria, ma ___ incontro sempre al bar.\n2. Conosco bene Giovanna, ___ vedo spesso e ___ telefono quasi ogni settimana.\n3. Ieri sera ho incontrato tua sorella; ___ ho invitat___ a cena e ___ ho parlato del nostro viaggio.\n4. Quando ha visto Gianni, ___ ha detto tutto quello che pensava di lui.\n5. Ho scritto ai miei amici e ___ ho detto di venire a trovarmi.\n6. Quando ho saputo il suo numero di telefono, ___ ho chiamat___.\n7. Ha visto il ladro scappare e ha tentato di fermar___.\n8. Giulio ___ ama, ma io non ___ amo.\n9. Quei ragazzi sono stati gentili con me; ___ voglio fare un regalo.\n10. Loro sono stati molto generosi con me; voglio invitar___ a cena.\n11. Quelle ragazze sono molto simpatiche, ___ voglio invitare a casa mia.\n12. La tua amica è carina, voglio regalar___ dei fiori.\n13. Perché sei così duro con lei? Perché ___ tratti così?\n14. Perché sei così fredda con lui? Perché non ___ parli in modo più amichevole?\n15. Ho parlato con tua sorella e ___ ho detto che volevo invitar___ alla festa.\n16. Dove sono i tuoi amici? ___ hai vist___? ___ hai telefonato?\n17. Dove sono le tue amiche? ___ hai vist___? ___ hai telefonato?\n18. Non devi avere paura di lei; ___ devi dire tutto.\n19. Non devi avere paura di lui; ___ devi dire tutto.\n20. Conosci Pietro? Sì, ___ conosco da molto tempo e ___ voglio bene.",
    "resposta": "1. la\n2. la / le\n3. l' / a / le\n4. gli\n5. gli\n6. l' / a (la ho chiamata)\n7. lo\n8. lo / lo\n9. gli\n10. li\n11. le\n12. le\n13. la\n14. gli\n15. le / la\n16. li / li / gli\n17. le / le / gli (loro)\n18. le\n19. gli\n20. lo / gli",
    "explicacao": "Diretto (chi?): lo/la/li/le. Indiretto (a chi?): gli/le/ci/vi. Telefonare, parlare, dire = indiretti. Invitare, vedere, conoscere = diretti."
})

# Esercizio 6
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Volgere al passato prossimo:\n1. Mi piacciono poco i suoi discorsi.\n2. Ti piacciono le mie amiche?\n3. Sono sicuro che non vi piace quel film.\n4. Tua figlia ci piace molto.\n5. La cena che ci hai preparato ci piace davvero tanto!\n6. Sai se gli piacciono questi libri?",
    "resposta": "1. Mi sono piaciuti poco i suoi discorsi.\n2. Ti sono piaciute le mie amiche?\n3. Sono sicuro che non vi è piaciuto quel film.\n4. Tua figlia ci è piaciuta molto.\n5. La cena che ci hai preparato ci è piaciuta davvero tanto!\n6. Sai se gli sono piaciuti questi libri?",
    "explicacao": "Piacere al passato prossimo usa ESSERE: il participio concorda col soggetto grammaticale (la cosa che piace)."
})

# Esercizio 7
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 7** — Esercizio misto (usare il tempo corretto):\n1. Domani Maria (rimanere) in casa tutto il giorno.\n2. Ieri Sandro (partire) per Milano.\n3. L'anno passato gli studenti (studiare) il latino.\n4. Oggi (noi volere) tornare presto a casa.\n5. Ieri le ragazze (uscire) dalla classe prima della fine della lezione.\n6. (Tu conoscere) il mio amico? Sì, (conoscere) ___.\n7. (Voi comprare) una macchina nuova? No, non compriamo.\n8. Quanti anni (avere)? Ho venti anni.\n9. Voi (leggere) i giornali? Sì, leggiamo.\n10. Carlo e Mario sono fratelli; ___ padre è medico.\n11. Hanno detto che domenica scorsa Mario (offrire) da bere a tutta la compagnia.\n12. Domani mattina tutti (potere) dormire fino a tardi.\n13. Ieri una ragazza italiana (venire) con me al cinema.\n14. Se domani (piovere), (io restare) a casa.\n15. Ieri (noi decidere) di andare in discoteca stasera.",
    "resposta": "1. rimarrà\n2. è partito\n3. hanno studiato\n4. vogliamo\n5. sono uscite\n6. Conosci / lo conosco\n7. Avete comprato\n8. hai\n9. leggete\n10. il loro\n11. ha offerto\n12. potranno\n13. è venuta\n14. pioverà / resterò\n15. abbiamo deciso",
    "explicacao": "Esercizio misto: presente, passato prossimo, futuro semplice. Attenzione ai verbi irregolari e all'ausiliare (essere/avere)."
})

# Esercizio 8 - Gradi di parentela
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 8** — Completare con il grado di parentela:\n1. Il marito di mia madre è mio ___.\n2. La moglie di mio fratello è mia ___.\n3. La sorella della mamma è mia ___.\n4. La madre di mio padre è mia ___.\n5. Il padre di mia madre è mio ___.\n6. I figli degli zii e delle zie sono i miei ___.\n7. Mio padre è il ___ della madre di mia madre.\n8. Mia madre è la ___ del padre di mio padre.\n9. La madre di mio padre è la ___ di mia madre.\n10. Il padre di mia madre è il ___ di mio padre.\n11. La moglie di un figlio è una ___.\n12. Il marito di una figlia è un ___.",
    "resposta": "1. padre(vitrigno/patrigno)\n2. cognata\n3. zia\n4. nonna\n5. nonno\n6. cugini\n7. genero\n8. nuora\n9. suocera\n10. suocero\n11. nuora\n12. genero",
    "explicacao": "Lessico della famiglia: nonno/nonna, zio/zia, cugino/cugina, cognato/cognata, suocero/suocera, genero, nuora."
})

# Lettura
EX.append({
    "tipo": "revelar",
    "pergunta": "**Lettura — La famiglia di Mario**\n\nRispondere alle domande:\n- Quali sono i componenti della famiglia di Mario? Quanti sono? Come si chiamano?\n- Dove vivono? Che cosa fanno?\n- Quando si riunisce tutta la famiglia? Dove?",
    "resposta": "I componenti sono: Mario (bibliotecario), Linda (moglie americana, insegnante di inglese), Elena (figlia, 6 anni). I genitori di Mario (Paolo in pensione, Maria casalinga) vivono in campagna vicino a Siena. La sorella Giulia vive a Roma con il marito Guido (dentista) e il figlio Simone (7 anni).\nLa famiglia si riunisce tre volte l'anno: a Natale, a Pasqua e durante le vacanze estive, nella casa di campagna dei genitori di Mario.",
    "explicacao": "Comprensione del testo e lessico dei gradi di parentela in contesto reale."
})

# Lavorare sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Lavorare sul testo — Una lettera**\n\nScrivere una frase con ciascuna delle seguenti parole o espressioni:\n1. di nuovo\n2. pittura\n3. nessuno\n4. mostra\n5. carino\n6. compleanno",
    "resposta": "Risposte libere. Esempi:\n1. Sono di nuovo a casa dopo le vacanze.\n2. Mi piace molto la pittura rinascimentale.\n3. Non c'era nessuno in casa quando sono arrivato.\n4. Ieri siamo andati a vedere una mostra di arte moderna.\n5. Il tuo cappotto nuovo è molto carino.\n6. Domani è il compleanno di mia sorella.",
    "explicacao": "Produzione scritta libera: usare le parole in contesto corretto."
})

# Esercizi di verifica (escolha)
verifica = [
    ("A mio padre piace molto l'opera.", "Mio padre piace molto l'opera.", "Il mio padre piace molto l'opera.", 0,
     "PIACERE: il soggetto è 'l'opera', 'mio padre' è complemento indiretto → A mio padre piace."),
    ("Ti piace queste scarpe?", "Piace ti queste scarpe?", "Ti piacciono queste scarpe?", 2,
     "Soggetto plurale 'scarpe' → PIACCIONO. Pronome atono TI prima del verbo."),
    ("regalo lui una cintura di cuoio.", "lo regalo una cintura di cuoio.", "gli regalo una cintura di cuoio.", 2,
     "Regalare a lui → pronome indiretto GLI. Il complemento indiretto non è 'lo' (diretto)."),
    ("Cosa te ha consigliato?", "Cosa ti ha consigliato?", "Cosa ha consigliato a te?", 1,
     "Pronome atono TI prima del verbo ausiliare. 'Te' è forma tonica, non si usa prima del verbo."),
    ("consiglio di prendere un autobus.", "Le consiglio di prendere un autobus.", "consiglio le di prendere un autobus.", 1,
     "Forma formale: pronome LE prima del verbo. Non si può mettere 'le' dopo il verbo."),
    ("non mi ha piaciuto.", "non mi ha piaciuta.", "non mi è piaciuta.", 2,
     "PIACERE usa ESSERE come ausiliare: 'mi è piaciuta' (la mostra, femminile singolare)."),
    ("Mi fai vedere le foto che hai fatto alla festa?", "Me fai vedere le foto che hai fatto alla festa?", "Fai mi vedere le foto che hai fatto alla festa?", 0,
     "MI prima del verbo principale. 'Me' è tonico. Il pronome atono non si inserisce tra verbo e infinito così."),
    ("Posso chiederti un favore, signorina?", "Posso Le chiedere un favore, signorina?", "Le posso chiedere un favore, signorina?", 2,
     "Con 'signorina' si usa la forma formale LE. LE prima del verbo modale: 'Le posso chiedere' = 'posso chiederLe'."),
    ("gli ho ancora scritto.", "le ho ancora scritto.", "lei ho ancora scritto.", 1,
     "Lei aspetta → femminile → pronome LE. 'Lei' tonico non si usa prima del verbo ausiliare."),
    ("Mi dispiace, ma non posso aiutarti.", "Me dispiace, ma non posso aiutarti.", "Dispiacemi, ma non posso aiutarti.", 0,
     "MI dispiace: pronome atono MI prima del verbo. 'Me' e la posizione dopo il verbo sono sbagliati."),
    ("Gli presento mia madre, signora.", "Le presento mia madre, signora.", "Ti presento mia signora.", 1,
     "Con 'signora' si usa la forma formale LE. GLI è maschile, TI è informale."),
    ("Le hai telefonata?", "L'hai telefonata?", "Le hai telefonato?", 2,
     "TELEFONARE è intransitivo → complemento INDIRETTO → LE. Il participio non concorda: 'telefonato' invariabile."),
    ("Le mandiamo il pacco direttamente a casa.", "gli mandiamo il pacco direttamente a casa.", "ti mandiamo il pacco direttamente a casa.", 0,
     "Forma formale con 'signora': LE. GLI è maschile/plurale, TI è informale."),
    ("voglio ti cucinare un piatto tipico.", "voglio cucinarti un piatto tipico.", "te voglio cucinare un piatto tipico.", 1,
     "Con verbi servili: pronome attaccato all'infinito (cucinarTI) oppure prima del modale (TI voglio cucinare)."),
    ("Ti hanno piaciuto?", "Ti sono piaciuti?", "Ti e piaciuti?", 1,
     "PIACERE + ESSERE → participio concorda col soggetto: 'quadri' = maschile plurale → piaciuTI."),
    ("ci ha offerto da bere.", "ci ha offerti da bere.", "ha offerto noi da bere.", 0,
     "OFFRIRE + AVERE → participio non concorda col pronome indiretto CI. 'Offerti' è sbagliato."),
    ("Puoi mi scrivere l'indirizzo, per favore?", "Mi puoi scrivere l'indirizzo, per favore?", "Puoi scriverme l'indirizzo, per favore?", 1,
     "MI prima del verbo modale, oppure 'scriverMI' attaccato all'infinito. 'Scriverme' non esiste."),
    ("Mi non piace fare sport.", "Non mi piace fare sport.", "Me non piace fare sport.", 1,
     "La negazione NON precede il pronome atono: NON MI piace. 'Mi non' e 'Me non' sono sbagliati."),
    ("Ai miei genitori non piace viaggiare.", "Miei genitori non piace viaggiare.", "I miei genitori non piacciono viaggiare.", 0,
     "Piacere + infinito: soggetto è l'infinito (singolare) → piace. 'Ai miei genitori' = complemento indiretto tonico."),
    ("consegnerà me le chiavi di casa.", "mi consegnerà le chiavi di casa.", "consegnerà mi le chiavi di casa.", 1,
     "Pronome atono MI prima del verbo. 'Me' tonico e 'mi' dopo il verbo sono posizioni scorrette."),
]

for a, b, c, r, expl in verifica:
    EX.append({
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [a, b, c],
        "resposta": r,
        "explicacao": expl
    })

# Trovare gli errori
errori = [
    ("Mi non piacciono le città con troppi turisti.",
     "Non mi piacciono le città con troppi turisti.",
     "Negazione NON precede sempre il pronome atono: NON MI piacciono."),
    ("Mia sorella piace molto la moda.",
     "A mia sorella piace molto la moda.",
     "Piacere richiede il complemento indiretto: A mia sorella piace (= le piace)."),
    ("Signora, ti dispiace ripetere, non ho capito.",
     "Signora, Le dispiace ripetere, non ho capito.",
     "Con 'signora' si usa la forma formale LE, non TI (informale)."),
    ("Voglio ti raccontare una storia buffa.",
     "Voglio raccontarti una storia buffa. / Ti voglio raccontare una storia buffa.",
     "Con verbi servili: pronome prima del modale (TI voglio) o dopo l'infinito (raccontarTI). Non tra i due verbi."),
    ("Gli piace la pasta, signora?",
     "Le piace la pasta, signora?",
     "Con 'signora' si usa la forma formale LE (non GLI, che è maschile)."),
    ("Ti ha piaciuto il film?",
     "Ti è piaciuto il film?",
     "PIACERE usa ESSERE come ausiliare: ti È piaciuto (non ha)."),
    ("Mia madre aspetta mie notizie, gli scriverò domani.",
     "Mia madre aspetta mie notizie, le scriverò domani.",
     "Mia madre = femminile → pronome indiretto LE, non GLI (maschile)."),
    ("Quando vedrò Luisa gli consegnerò la lettera.",
     "Quando vedrò Luisa le consegnerò la lettera.",
     "Luisa = femminile → pronome indiretto LE. GLI si usa per maschile o plurale."),
    ("Ho incontrato i miei amici e loro ho raccontato tutto.",
     "Ho incontrato i miei amici e gli ho raccontato tutto.",
     "Forma atona GLI (o 'ho raccontato loro' con tonico dopo il verbo). 'Loro ho' è ordine sbagliato."),
    ("A che ora hai mi telefonato?",
     "A che ora mi hai telefonato?",
     "Il pronome atono MI precede il verbo ausiliare HAI: mi HAI telefonato."),
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
