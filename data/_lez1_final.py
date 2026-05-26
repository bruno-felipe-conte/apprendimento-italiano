import json

with open(r'grammar.json', encoding='utf-8') as f:
    data = json.load(f)

teoria_lines = [
    "**A. La formazione del nome maschile e femminile**",
    "",
    "| | singolare | plurale |",
    "|-|-----------|---------|",
    "| *maschile* | quaderno | quaderni |",
    "| *femminile* | lavagna | lavagne |",
    "",
    "| | singolare | plurale |",
    "|-|-----------|---------|",
    "| *maschile* | giornale | giornali |",
    "| *femminile* | lezione | lezioni |",
    "",
    "**Regola:** Nomi in **-o** → plurale **-i** (m.). Nomi in **-a** → plurale **-e** (f.). Nomi in **-e** → plurale **-i** (m. e f.).",
    "",
    "**B. La formazione dell'articolo determinativo**",
    "",
    """<table class="gram-table gram-table-rich">
<thead><tr><th></th><th colspan="2">singolare</th><th colspan="2">plurale</th></tr></thead>
<tbody>
<tr><th rowspan="3" class="gram-genere">maschile</th><td class="gram-art">il</td><td>libro<br>gatto<br>cane</td><td class="gram-art">i</td><td>libri<br>gatti<br>cani</td></tr>
<tr><td class="gram-art">lo</td><td>zaino<br>spagnolo<br>studente</td><td class="gram-art">gli</td><td>zaini<br>spagnoli<br>studenti</td></tr>
<tr><td class="gram-art">l'</td><td>ufficio<br>esame<br>orologio</td><td class="gram-art">gli</td><td>uffici<br>esami<br>orologi</td></tr>
<tr><th rowspan="2" class="gram-genere">femminile</th><td class="gram-art">la</td><td>studentessa<br>ragazza<br>chiave</td><td class="gram-art">le</td><td>studentesse<br>ragazze<br>chiavi</td></tr>
<tr><td class="gram-art">l'</td><td>ora<br>idea<br>opera</td><td class="gram-art">le</td><td>ore<br>idee<br>opere</td></tr>
</tbody></table>""",
    "",
    "**C. La formazione dell'aggettivo**",
    "",
    "**a. Aggettivi variabili nel genere e nel numero:**",
    "",
    "| | singolare | plurale |",
    "|-|-----------|---------|",
    "| *maschile* | tavolo / cappotto / fiore **rosso** | tavoli / cappotti / fiori **rossi** |",
    "| *femminile* | casa / borsa / luce **rossa** | case / borse / luci **rosse** |",
    "",
    "**b. Aggettivi variabili solamente nel numero:**",
    "",
    "| | singolare | plurale |",
    "|-|-----------|---------|",
    "| *maschile* | tavolo / televisore **grande** | tavoli / televisori **grandi** |",
    "| *femminile* | borsa / chiave **grande** | borse / chiavi **grandi** |",
    "",
    "**c. Aggettivi invariabili:**",
    "",
    "| | singolare / plurale |",
    "|-|---------------------|",
    "| *maschile e femminile* | libro / libri / gonna / gonne **blu** |",
    "",
    "**D. La coniugazione del verbo ESSERE**",
    "",
    "| persona | forma |",
    "|---------|-------|",
    "| io | **sono** |",
    "| tu | **sei** |",
    "| lui / lei / Lei | **è** |",
    "| noi | **siamo** |",
    "| voi | **siete** |",
    "| loro | **sono** |",
    "",
    "**Uso informale:** Io sono Michela, e *tu chi sei*? — Io sono Claudia.",
    "**Uso formale:** Io sono il professor Brandini, e *Lei chi è*? — Io sono il signor Urbani.",
    "",
    "**Chi è...? Che cosa è...?**",
    "Chi è questo? → Questo è Leonardo. / Chi sono questi? → Questi sono Carlo e Paolo.",
    "Che cosa è quello? → Quello è il duomo. / Che cosa sono quelle? → Quelle sono due biciclette.",
    "",
    "**E. La formazione dell'articolo indeterminativo**",
    "",
    """<table class="gram-table gram-table-rich">
<thead><tr><th></th><th>articolo</th><th>esempi</th><th>quando si usa</th></tr></thead>
<tbody>
<tr><th rowspan="2" class="gram-genere">maschile</th><td class="gram-art">un</td><td>un libro<br>un orologio</td><td>davanti a consonante o vocale</td></tr>
<tr><td class="gram-art">uno</td><td>uno specchio<br>uno zaino</td><td>davanti a s+cons., z, gn, ps</td></tr>
<tr><th rowspan="2" class="gram-genere">femminile</th><td class="gram-art">una</td><td>una matita<br>una casa</td><td>davanti a consonante</td></tr>
<tr><td class="gram-art">un'</td><td>un'immagine<br>un'albicocca</td><td>davanti a vocale</td></tr>
</tbody></table>""",
    "",
    "**Plurale partitivo:** dei libri / degli orologi / degli specchi / delle matite / delle case / delle immagini.",
    "",
    "**C'è / Ci sono:**",
    "Sul tavolo **c'è** un libro. (singolare)",
    "Sul tavolo **ci sono** dei libri. (plurale)",
]

teoria = "\n".join(teoria_lines)

exercicios = [

    # ══════════════════════════════════════════════════════════
    #  ESERCIZI 1–18  (dal libro)
    # ══════════════════════════════════════════════════════════

    # ── Esercizio 1 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 1** — Volgere al plurale (nomi in **-o** e **-a**):\nsedia / finestra / foglio / penna / registro / tavolo / cassetto / sigaretta / borsa / corso / documento",
        "resposta": "sedie / finestre / fogli / penne / registri / tavoli / cassetti / sigarette / borse / corsi / documenti",
        "explicacao": "Femminili in **-a** → **-e** (sedia→sedie, borsa→borse). Maschili in **-o** → **-i** (tavolo→tavoli, corso→corsi)."
    },

    # ── Esercizio 2 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 2** — Volgere al plurale (nomi in **-e**):\nmadre / padre / chiave / signore / luce / stazione / pane / fiore / bicchiere / frase / ponte",
        "resposta": "madri / padri / chiavi / signori / luci / stazioni / pani / fiori / bicchieri / frasi / ponti",
        "explicacao": "Tutti i nomi in **-e** (maschili e femminili) fanno il plurale in **-i**."
    },

    # ── Esercizio 3 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 3** — Mettere l'articolo determinativo e volgere al plurale:\npadre / stazione / cassetta / bottiglia / albero / luce / signore / scarpa / esercizio / giornale / uscita / indirizzo / amico / cane",
        "resposta": "il padre → i padri\nla stazione → le stazioni\nla cassetta → le cassette\nla bottiglia → le bottiglie\nl'albero → gli alberi\nla luce → le luci\nil signore → i signori\nla scarpa → le scarpe\nl'esercizio → gli esercizi\nil giornale → i giornali\nl'uscita → le uscite\nl'indirizzo → gli indirizzi\nl'amico → gli amici\nil cane → i cani",
        "explicacao": "Parole che iniziano con vocale → l' / gli o l' / le. Amico→amici (accento sulla terzultima: plurale in -ci). Signore→signori (maschile in -e → -i)."
    },

    # ── Esercizio 4 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 4** — Volgere al plurale:\ncorso difficile / madre gentile / treno veloce / parete rosa / lingua facile / soffitto viola / sedia verde / stazione grande / padre cortese / studente giapponese",
        "resposta": "corsi difficili / madri gentili / treni veloci / pareti rosa / lingue facili / soffitti viola / sedie verdi / stazioni grandi / padri cortesi / studenti giapponesi",
        "explicacao": "Aggettivi in **-e** → **-i** (difficile→difficili, gentile→gentili, veloce→veloci). Aggettivi di colore invariabili: **rosa** e **viola** non cambiano mai."
    },

    # ── Esercizio 5 (5 gruppi) ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Mettere l'articolo determinativo e indeterminativo, poi volgere al plurale.\n\n**Gruppo 1:** soffitto / pavimento / muro / tetto / libro / foglio / medico / disco / popolo / museo / quadro / piano / coltello / gatto / tappeto",
        "resposta": "il soffitto / un soffitto → i soffitti / dei soffitti\nil pavimento / un pavimento → i pavimenti / dei pavimenti\nil muro / un muro → i muri / dei muri\nil tetto / un tetto → i tetti / dei tetti\nil libro / un libro → i libri / dei libri\nil foglio / un foglio → i fogli / dei fogli\nil medico / un medico → i medici / dei medici\nil disco / un disco → i dischi / dei dischi\nil popolo / un popolo → i popoli / dei popoli\nil museo / un museo → i musei / dei musei\nil quadro / un quadro → i quadri / dei quadri\nil piano / un piano → i piani / dei piani\nil coltello / un coltello → i coltelli / dei coltelli\nil gatto / un gatto → i gatti / dei gatti\nil tappeto / un tappeto → i tappeti / dei tappeti",
        "explicacao": "Maschili in -o → il/un, plur. -i. Eccezioni: medico→medici (acc. terzultima → -ci); disco→dischi (acc. penultima → -schi); museo→musei."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Gruppo 2:\nsale / direttore / padre / sapone / mare / bicchiere / fiore / colore / cane / inglese / fiume / prete",
        "resposta": "il sale / un sale → i sali / dei sali\nil direttore / un direttore → i direttori / dei direttori\nil padre / un padre → i padri / dei padri\nil sapone / un sapone → i saponi / dei saponi\nil mare / un mare → i mari / dei mari\nil bicchiere / un bicchiere → i bicchieri / dei bicchieri\nil fiore / un fiore → i fiori / dei fiori\nil colore / un colore → i colori / dei colori\nil cane / un cane → i cani / dei cani\nl'inglese / un inglese → gli inglesi / degli inglesi\nil fiume / un fiume → i fiumi / dei fiumi\nil prete / un prete → i preti / dei preti",
        "explicacao": "Maschili in **-e** → plurale in **-i**. Inglese inizia con vocale → l'inglese / gli inglesi."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Gruppo 3:\nzucchero / zero / orologio / uomo / amico / zio / errore / uccello / occhio / ordine / studente / insegnante / straniero / stadio",
        "resposta": "lo zucchero / uno zucchero → gli zuccheri / degli zuccheri\nlo zero / uno zero → gli zeri / degli zeri\nl'orologio / un orologio → gli orologi / degli orologi\nl'uomo / un uomo → gli uomini / degli uomini\nl'amico / un amico → gli amici / degli amici\nlo zio / uno zio → gli zii / degli zii\nl'errore / un errore → gli errori / degli errori\nl'uccello / un uccello → gli uccelli / degli uccelli\nl'occhio / un occhio → gli occhi / degli occhi\nl'ordine / un ordine → gli ordini / degli ordini\nlo studente / uno studente → gli studenti / degli studenti\nl'insegnante / un insegnante → gli insegnanti / degli insegnanti\nlo straniero / uno straniero → gli stranieri / degli stranieri\nlo stadio / uno stadio → gli stadi / degli stadi",
        "explicacao": "Inizia con z, s+cons. → lo/uno. Inizia con vocale → l'/un. Uomo ha plurale irregolare: **uomini**. Zio→zii (raddoppia la i)."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Gruppo 4:\nsedia / casa / coperta / spazzola / borsa / finestra / lettera / fabbrica / scuola / cintura / maglietta / gonna / trattoria / mela / fragola",
        "resposta": "la sedia / una sedia → le sedie / delle sedie\nla casa / una casa → le case / delle case\nla coperta / una coperta → le coperte / delle coperte\nla spazzola / una spazzola → le spazzole / delle spazzole\nla borsa / una borsa → le borse / delle borse\nla finestra / una finestra → le finestre / delle finestre\nla lettera / una lettera → le lettere / delle lettere\nla fabbrica / una fabbrica → le fabbriche / delle fabbriche\nla scuola / una scuola → le scuole / delle scuole\nla cintura / una cintura → le cinture / delle cinture\nla maglietta / una maglietta → le magliette / delle magliette\nla gonna / una gonna → le gonne / delle gonne\nla trattoria / una trattoria → le trattorie / delle trattorie\nla mela / una mela → le mele / delle mele\nla fragola / una fragola → le fragole / delle fragole",
        "explicacao": "Femminili in **-a** → **-e**. Fabbrica→fabbriche (mant. suono duro con h: -ca→-che)."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Gruppo 5:\nchiave / madre / traduzione / spiegazione / cornice / luce / matita / arte / estate / immagine / nave / morte / fronte",
        "resposta": "la chiave / una chiave → le chiavi / delle chiavi\nla madre / una madre → le madri / delle madri\nla traduzione / una traduzione → le traduzioni / delle traduzioni\nla spiegazione / una spiegazione → le spiegazioni / delle spiegazioni\nla cornice / una cornice → le cornici / delle cornici\nla luce / una luce → le luci / delle luci\nla matita / una matita → le matite / delle matite\nl'arte / un'arte → le arti / delle arti\nl'estate / un'estate → le estati / delle estati\nl'immagine / un'immagine → le immagini / delle immagini\nla nave / una nave → le navi / delle navi\nla morte / una morte → le morti / delle morti\nla fronte / una fronte → le fronti / delle fronti",
        "explicacao": "Femminili in **-e** → **-i** (chiave→chiavi, luce→luci). Inizia con vocale → l'/un' (l'arte, l'estate). Cornice→cornici (-ce→-ci, suono dolce)."
    },

    # ── Esercizio 6 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 6** — Mettere l'articolo determinativo e indeterminativo, poi volgere al plurale:\norologio / cappotto / foglio / scarpa / bottiglia / luce / fiammifero / cassetta / piatto / tappo / tazza / albero / pero / pianta / zio / armadio / tovaglia / asciugamano / elefante / piede / quadro / tenda / vestito / giornale / libro / parco / amico / straniero / padre / madre / nemico / naso / bocca / dente / lingua / specchio / vino / birra / palla / nonna / studentessa / telefono",
        "resposta": "l'orologio / un orologio → gli orologi / degli orologi\nil cappotto / un cappotto → i cappotti / dei cappotti\nil foglio / un foglio → i fogli / dei fogli\nla scarpa / una scarpa → le scarpe / delle scarpe\nla bottiglia / una bottiglia → le bottiglie / delle bottiglie\nla luce / una luce → le luci / delle luci\nil fiammifero / un fiammifero → i fiammiferi / dei fiammiferi\nla cassetta / una cassetta → le cassette / delle cassette\nil piatto / un piatto → i piatti / dei piatti\nil tappo / un tappo → i tappi / dei tappi\nla tazza / una tazza → le tazze / delle tazze\nl'albero / un albero → gli alberi / degli alberi\nil pero / un pero → i peri / dei peri\nla pianta / una pianta → le piante / delle piante\nlo zio / uno zio → gli zii / degli zii\nl'armadio / un armadio → gli armadi / degli armadi\nla tovaglia / una tovaglia → le tovaglie / delle tovaglie\nl'asciugamano / un asciugamano → gli asciugamani / degli asciugamani\nl'elefante / un elefante → gli elefanti / degli elefanti\nil piede / un piede → i piedi / dei piedi\nil quadro / un quadro → i quadri / dei quadri\nla tenda / una tenda → le tende / delle tende\nil vestito / un vestito → i vestiti / dei vestiti\nil giornale / un giornale → i giornali / dei giornali\nil libro / un libro → i libri / dei libri\nil parco / un parco → i parchi / dei parchi\nl'amico / un amico → gli amici / degli amici\nlo straniero / uno straniero → gli stranieri / degli stranieri\nil padre / un padre → i padri / dei padri\nla madre / una madre → le madri / delle madri\nil nemico / un nemico → i nemici / dei nemici\nil naso / un naso → i nasi / dei nasi\nla bocca / una bocca → le bocche / delle bocche\nil dente / un dente → i denti / dei denti\nla lingua / una lingua → le lingue / delle lingue\nlo specchio / uno specchio → gli specchi / degli specchi\nil vino / un vino → i vini / dei vini\nla birra / una birra → le birre / delle birre\nla palla / una palla → le palle / delle palle\nla nonna / una nonna → le nonne / delle nonne\nla studentessa / una studentessa → le studentesse / delle studentesse\nil telefono / un telefono → i telefoni / dei telefoni",
        "explicacao": "Bocca→bocche (-ca→-che). Parco→parchi (-co acc. penultima → -chi). Amico, nemico→amici, nemici (-co acc. terzultima → -ci). Specchio→specchi."
    },

    # ── Esercizio 7 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 7** — Volgere al plurale (attenzione ai plurali irregolari in **-co/-ca/-go/-ga**):\namico / amica / giacca / luogo / lago / austriaca / fuoco / tacco / pacco / parco / tedesca / greco / fungo / marco / barca",
        "resposta": "amici / amiche / giacche / luoghi / laghi / austriache / fuochi / tacchi / pacchi / parchi / tedesche / greci / funghi / marchi / barche",
        "explicacao": "**-CA/-GA → -CHE/-GHE** (amica→amiche, giacca→giacche, austriaca→austriache, tedesca→tedesche, barca→barche).\n**-CO acc. terzultima → -CI** (amico→amici, greco→greci).\n**-CO acc. penultima → -CHI** (fuoco→fuochi, tacco→tacchi, pacco→pacchi, parco→parchi, marco→marchi).\n**-GO → -GHI** (luogo→luoghi, lago→laghi, fungo→funghi)."
    },

    # ── Esercizio 8 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 8** — Mettere l'articolo determinativo e indeterminativo e volgere al plurale:\ncasa nuova / libro vecchio / ragazza gentile / uomo interessante / bottiglia vuota / vino dolce / vetro rotto / chiave piccola / madre affettuosa / studente giovane / bicchiere pieno / insegnante simpatico / ragazza nervosa / giacca verde / pacco leggero / scatola aperta / sedia utile / penna rossa / treno veloce / esercizio facile",
        "resposta": "la casa nuova / una casa nuova → le case nuove / delle case nuove\nil libro vecchio / un libro vecchio → i libri vecchi / dei libri vecchi\nla ragazza gentile / una ragazza gentile → le ragazze gentili / delle ragazze gentili\nl'uomo interessante / un uomo interessante → gli uomini interessanti / degli uomini interessanti\nla bottiglia vuota / una bottiglia vuota → le bottiglie vuote / delle bottiglie vuote\nil vino dolce / un vino dolce → i vini dolci / dei vini dolci\nil vetro rotto / un vetro rotto → i vetri rotti / dei vetri rotti\nla chiave piccola / una chiave piccola → le chiavi piccole / delle chiavi piccole\nla madre affettuosa / una madre affettuosa → le madri affettuose / delle madri affettuose\nlo studente giovane / uno studente giovane → gli studenti giovani / degli studenti giovani\nil bicchiere pieno / un bicchiere pieno → i bicchieri pieni / dei bicchieri pieni\nl'insegnante simpatico / un insegnante simpatico → gli insegnanti simpatici / degli insegnanti simpatici\nla ragazza nervosa / una ragazza nervosa → le ragazze nervose / delle ragazze nervose\nla giacca verde / una giacca verde → le giacche verdi / delle giacche verdi\nil pacco leggero / un pacco leggero → i pacchi leggeri / dei pacchi leggeri\nla scatola aperta / una scatola aperta → le scatole aperte / delle scatole aperte\nla sedia utile / una sedia utile → le sedie utili / delle sedie utili\nla penna rossa / una penna rossa → le penne rosse / delle penne rosse\nil treno veloce / un treno veloce → i treni veloci / dei treni veloci\nl'esercizio facile / un esercizio facile → gli esercizi facili / degli esercizi facili",
        "explicacao": "L'aggettivo concorda con il sostantivo in genere e numero. Vecchio→vecchi, affettuosa→affettuose, simpatico→simpatici. Giacca→giacche (mant. suono duro). Pacco→pacchi."
    },

    # ── Esercizio 9 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 9** — Formare delle frasi con i seguenti sostantivi e aggettivi e volgere al plurale.\nMod.: *Il libro è difficile → I libri sono difficili.*\n\nSostantivi: giacca / camicia / stanza / ragazzo / amica / strada / uomo / vino / scarpe / quaderno / esercizio / frase / città\nAggettivi: facile / difficile / chiaro / dolce / pulito / sporco / cattivo / buono / gentile / intelligente / interessante / noioso / tranquillo / silenzioso / stretto / largo / nuovo / vecchio",
        "resposta": "La giacca è nuova → Le giacche sono nuove.\nLa camicia è pulita → Le camicie sono pulite.\nLa stanza è silenziosa → Le stanze sono silenziose.\nIl ragazzo è simpatico → I ragazzi sono simpatici.\nL'amica è intelligente → Le amiche sono intelligenti.\nLa strada è stretta → Le strade sono strette.\nL'uomo è gentile → Gli uomini sono gentili.\nIl vino è dolce → I vini sono dolci.\nLe scarpe sono vecchie → (già plurale).\nIl quaderno è nuovo → I quaderni sono nuovi.\nL'esercizio è facile → Gli esercizi sono facili.\nLa frase è chiara → Le frasi sono chiare.\nLa città è tranquilla → Le città sono tranquille.",
        "explicacao": "Il verbo ESSERE: è (sing.) / sono (plur.). Aggettivi e articoli concordano. Città→città (invariabile al plurale). Amica→amiche (femm. -ca→-che)."
    },

    # ── Esercizio 10 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 10** — Come il precedente.\n\nSostantivi: treno / film / lezione / insegnante / ristorante / gelato / medicina / appartamento / pensione / famiglia / pranzo / turista / museo / penna / pantaloni / borsa / giardino / fiume / negozio\nAggettivi: affollato / bello / noioso / bravo / caro / economico / utile / inutile / nuovo / rumoroso / tranquillo / chiaro / simpatico / largo / aperto / pesante / leggero / verde / buono",
        "resposta": "Il treno è affollato → I treni sono affollati.\nIl film è noioso → I film sono noiosi.\nLa lezione è utile → Le lezioni sono utili.\nL'insegnante è bravo → Gli insegnanti sono bravi.\nIl ristorante è caro → I ristoranti sono cari.\nIl gelato è buono → I gelati sono buoni.\nLa medicina è utile → Le medicine sono utili.\nL'appartamento è nuovo → Gli appartamenti sono nuovi.\nLa pensione è economica → Le pensioni sono economiche.\nLa famiglia è tranquilla → Le famiglie sono tranquille.\nIl pranzo è buono → I pranzi sono buoni.\nIl turista è simpatico → I turisti sono simpatici.\nIl museo è bello → I musei sono belli.\nLa penna è nuova → Le penne sono nuove.\nI pantaloni sono larghi → (già plurale).\nLa borsa è pesante → Le borse sono pesanti.\nIl giardino è verde → I giardini sono verdi.\nIl fiume è lungo → I fiumi sono lunghi.\nIl negozio è aperto → I negozi sono aperti.",
        "explicacao": "Film è invariabile (i film). Bello→belli (maschile plur.). Pensione→pensioni. Lungo→lunghi (mant. suono duro)."
    },

    # ── Esercizio 11 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 11** — Volgere al plurale:\nLa bistecca è cruda. / Il pesce è cotto. / Il vino è secco. / L'orologio è rotto. / L'esercizio non è difficile. / L'autobus non è puntuale. / L'amica è simpatica. / La macchina è veloce. / La segretaria è gentile. / Il turista è confuso. / La stanza è piccola. / Il mio amico non è alto. / L'albero è vecchio e malato. / L'esercizio è molto utile. / Lo studente è intelligente. / La città è caotica. / Il libro è interessante. / Il posto è libero. / La sedia è occupata. / Il tavolo è nuovo. / La lezione è finita. / Il programma televisivo è noioso. / Il concerto è interessante. / Il cibo è fresco. / Il fiore è profumato. / Il caffè è caldo. / La zuppa è fredda. / La ragazza è bella. / Il ristorante è troppo caro. / La pizza è buona.",
        "resposta": "Le bistecche sono crude. / I pesci sono cotti. / I vini sono secchi. / Gli orologi sono rotti. / Gli esercizi non sono difficili. / Gli autobus non sono puntuali. / Le amiche sono simpatiche. / Le macchine sono veloci. / Le segretarie sono gentili. / I turisti sono confusi. / Le stanze sono piccole. / I miei amici non sono alti. / Gli alberi sono vecchi e malati. / Gli esercizi sono molto utili. / Gli studenti sono intelligenti. / Le città sono caotiche. / I libri sono interessanti. / I posti sono liberi. / Le sedie sono occupate. / I tavoli sono nuovi. / Le lezioni sono finite. / I programmi televisivi sono noiosi. / I concerti sono interessanti. / I cibi sono freschi. / I fiori sono profumati. / I caffè sono caldi. / Le zuppe sono fredde. / Le ragazze sono belle. / I ristoranti sono troppo cari. / Le pizze sono buone.",
        "explicacao": "Secco→secchi (mant. suono duro). Autobus→autobus (invariabile). Caotico→caotici. Città→città (invariabile). Programma→programmi (maschile in -a)."
    },

    # ── Esercizio 12 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 12** — Volgere al plurale.\nMod.: *Questa / quella è la mia borsa → Queste / quelle sono le mie borse.*\n\n1. Questo è il tuo libro.\n2. Questa è la sua macchina.\n3. Questa è la sua amica.\n4. Questo è il suo amico.\n5. Questa è la mia camicia.\n6. Quella è la tua casa.\n7. Quella è la nostra vecchia sedia.\n8. Questo è il nostro simpatico insegnante.\n9. Quella è la vostra nuova camera.\n10. Quello è il vostro nuovo appartamento.\n11. Questo è il loro giornale.\n12. Questa è la loro segretaria.\n13. Quello è il mio armadio.",
        "resposta": "1. Questi sono i tuoi libri.\n2. Queste sono le sue macchine.\n3. Queste sono le sue amiche.\n4. Questi sono i suoi amici.\n5. Queste sono le mie camicie.\n6. Quelle sono le tue case.\n7. Quelle sono le nostre vecchie sedie.\n8. Questi sono i nostri simpatici insegnanti.\n9. Quelle sono le vostre nuove camere.\n10. Quelli sono i vostri nuovi appartamenti.\n11. Questi sono i loro giornali.\n12. Queste sono le loro segretarie.\n13. Quelli sono i miei armadi.",
        "explicacao": "Dimostrativi plurali: questo→questi/queste, quello→quelli/quelle. Possessivi: mio→miei/mie, tuo→tuoi/tue, suo→suoi/sue, nostro→nostri/nostre, vostro→vostri/vostre. Loro è sempre invariabile."
    },

    # ── Esercizio 13 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 13** — Fare la domanda secondo il modello.\nMod.: *Mario è il nostro insegnante. → Chi è Mario?*\n\n1. Giovanna è la segretaria.\n2. Questi due giovani sono i nostri cugini.\n3. Erika è una studentessa straniera.\n4. Peter e Kate sono gli amici di Paolo.\n5. La signora Gentili è la nostra vicina.\n6. Quelle ragazze sono le nostre compagne di classe.\n7. La signora Falchi è la madre del vostro amico.",
        "resposta": "1. Chi è Giovanna?\n2. Chi sono questi due giovani?\n3. Chi è Erika?\n4. Chi sono Peter e Kate?\n5. Chi è la signora Gentili?\n6. Chi sono quelle ragazze?\n7. Chi è la signora Falchi?",
        "explicacao": "**Chi è...?** → persona singolare. **Chi sono...?** → persone al plurale. Per le cose si usa **Che cos'è...? / Che cosa sono...?**"
    },

    # ── Esercizio 14 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 14** — Replicare secondo il modello.\nMod.: *Lui è sempre stanco. → Lei, invece, non è mai stanca.*\n\n1. Lui è sempre contento.\n2. Lui è sempre attento.\n3. Lui è sempre malato.\n4. Lui è sempre vestito male.\n5. Lui è sempre nervoso.\n6. Lui è sempre allegro.\n7. Lui è sempre calmo.\n8. Lui è sempre arrabbiato.\n9. Lui è sempre gentile.\n10. Lui è sempre elegante.",
        "resposta": "1. Lei, invece, non è mai contenta.\n2. Lei, invece, non è mai attenta.\n3. Lei, invece, non è mai malata.\n4. Lei, invece, non è mai vestita male.\n5. Lei, invece, non è mai nervosa.\n6. Lei, invece, non è mai allegra.\n7. Lei, invece, non è mai calma.\n8. Lei, invece, non è mai arrabbiata.\n9. Lei, invece, non è mai gentile.\n10. Lei, invece, non è mai elegante.",
        "explicacao": "**Sempre** ↔ **mai**. L'aggettivo concorda al femminile: contento→contenta, nervoso→nervosa, allegro→allegra. Aggettivi in -e (gentile, elegante) sono invariabili nel genere."
    },

    # ── Esercizio 15 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 15** — Replicare secondo il modello.\nMod.: *Io ho un libro. → Anch'io ho un libro.*\n\n1. Io ho una giacca nuova.\n2. Io ho una macchina rossa.\n3. Io ho i vestiti sporchi.\n4. Io ho le scarpe pulite.\n5. Io ho un fratello.\n6. Io ho un amico francese.\n7. Io ho un gatto siamese.\n8. Io ho una casa vecchia.\n9. Io ho gli occhiali da sole.\n10. Io ho fame.",
        "resposta": "1. Anch'io ho una giacca nuova.\n2. Anch'io ho una macchina rossa.\n3. Anch'io ho i vestiti sporchi.\n4. Anch'io ho le scarpe pulite.\n5. Anch'io ho un fratello.\n6. Anch'io ho un amico francese.\n7. Anch'io ho un gatto siamese.\n8. Anch'io ho una casa vecchia.\n9. Anch'io ho gli occhiali da sole.\n10. Anch'io ho fame.",
        "explicacao": "**Anch'io** (= anche + io, elisione davanti a vocale) per concordare con frasi affermative. Opposto: **Neanche io** per frasi negative."
    },

    # ── Esercizio 16 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 16** — Replicare secondo il modello.\nMod.: *Io non sono tedesco. → Neanche io sono tedesco.*\n\n1. Io non sono un insegnante.\n2. Io non sono uno studente americano.\n3. Io non sono un architetto.\n4. Io non sono stanco.\n5. Io non sono arrabbiato.\n6. Io non sono distratto.\n7. Io non sono svizzero.\n8. Io non sono un meccanico.\n9. Io non sono una segretaria.\n10. Io non sono triste.",
        "resposta": "1. Neanche io sono un insegnante.\n2. Neanche io sono uno studente americano.\n3. Neanche io sono un architetto.\n4. Neanche io sono stanco.\n5. Neanche io sono arrabbiato.\n6. Neanche io sono distratto.\n7. Neanche io sono svizzero.\n8. Neanche io sono un meccanico.\n9. Neanche io sono una segretaria.\n10. Neanche io sono triste.",
        "explicacao": "**Neanche io** per concordare con frasi negative. **Anch'io** per affermative. 'Neanche' = nemmeno = neppure (sinonimi)."
    },

    # ── Esercizio 17 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 17** — Completare secondo il modello.\nMod.: *casa vecchia / bella → Questa casa vecchia è bella.*\n\n1. Ragazza francese / simpatica.\n2. Insegnante giovane / brava.\n3. Studente tedesco / intelligente.\n4. Libro nuovo / difficile.\n5. Città vecchia / interessante.\n6. Vestito nero / brutto.\n7. Strada alberata / bella.\n8. Lingua straniera / difficile.",
        "resposta": "1. Questa ragazza francese è simpatica.\n2. Questa insegnante giovane è brava.\n3. Questo studente tedesco è intelligente.\n4. Questo libro nuovo è difficile.\n5. Questa città vecchia è interessante.\n6. Questo vestito nero è brutto.\n7. Questa strada alberata è bella.\n8. Questa lingua straniera è difficile.",
        "explicacao": "Il dimostrativo **questo/questa** concorda con il genere del sostantivo. Femminili → questa; maschili → questo."
    },

    # ── Esercizio 18 ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 18** — Rispondere secondo il modello.\nMod.: *Cosa c'è sul tavolo? (libro)*\n*a) Sul tavolo c'è un libro. b) Sul tavolo ci sono dei libri.*\n\n1. Cosa c'è nella borsa? (chiave)\n2. Cosa c'è nel cassetto? (camicia)\n3. Cosa c'è nella stanza? (sedia)\n4. Cosa c'è nella camera? (letto)\n5. Cosa c'è sul letto? (cuscino)\n6. Cosa c'è sul tavolo? (bottiglia)\n7. Cosa c'è nella valigia? (vestito)\n8. Cosa c'è in quella scatola? (regalo)\n9. Cosa c'è nel vaso di vetro? (pesce rosso)\n10. Cosa c'è nella busta? (fotografia)",
        "resposta": "1. a) Nella borsa c'è una chiave. b) Nella borsa ci sono delle chiavi.\n2. a) Nel cassetto c'è una camicia. b) Nel cassetto ci sono delle camicie.\n3. a) Nella stanza c'è una sedia. b) Nella stanza ci sono delle sedie.\n4. a) Nella camera c'è un letto. b) Nella camera ci sono dei letti.\n5. a) Sul letto c'è un cuscino. b) Sul letto ci sono dei cuscini.\n6. a) Sul tavolo c'è una bottiglia. b) Sul tavolo ci sono delle bottiglie.\n7. a) Nella valigia c'è un vestito. b) Nella valigia ci sono dei vestiti.\n8. a) In quella scatola c'è un regalo. b) In quella scatola ci sono dei regali.\n9. a) Nel vaso di vetro c'è un pesce rosso. b) Nel vaso di vetro ci sono dei pesci rossi.\n10. a) Nella busta c'è una fotografia. b) Nella busta ci sono delle fotografie.",
        "explicacao": "**C'è** + singolare (un/una/uno/un'). **Ci sono** + plurale (dei/delle/degli). Pesce rosso→pesci rossi (entrambe le parole al plurale)."
    },

    # ══════════════════════════════════════════════════════════
    #  ESERCIZI DI VERIFICA  (15 domande — Scegliere la frase corretta)
    # ══════════════════════════════════════════════════════════

    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "La borsa e il zaino sono pieno.",
            "La borsa e lo zaino sono pieni.",
            "La borsa e lo zaino e pieni."
        ],
        "resposta": 1,
        "explicacao": "Con due soggetti → verbo al plurale: SONO. Zaino inizia con z → LO zaino. Pieni: maschile plurale (accordo con il sostantivo maschile zaino)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "La porta e la finestra sono chiusi.",
            "La porta e la finestra sono chiuso.",
            "La porta e la finestra sono chiuse."
        ],
        "resposta": 2,
        "explicacao": "Porta e finestra sono femminili → aggettivo femminile plurale: **chiuse**."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Io ho un'amico italiano.",
            "Io o un amico italiano.",
            "Io ho un amico italiano."
        ],
        "resposta": 2,
        "explicacao": "Amico è maschile → si usa **un** (non un'). Un' è solo per femminili davanti a vocale (un'amica)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Queste frasi sono facile.",
            "Queste frasi sono facili.",
            "Questi frasi sono facili."
        ],
        "resposta": 1,
        "explicacao": "Frasi è femminile plurale → **Queste** (non questi) e **facili** (plurale)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Il ristorante è bene.",
            "Il ristorante è buono.",
            "Lo ristorante è bene."
        ],
        "resposta": 1,
        "explicacao": "'Bene' è avverbio (parla bene). 'Buono' è aggettivo di qualità. Il ristorante è **buono**. Articolo: IL (ristorante inizia con r)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "La gente sono gentile.",
            "La gente sono gentili.",
            "La gente è gentile."
        ],
        "resposta": 2,
        "explicacao": "'Gente' è sostantivo collettivo singolare → verbo al singolare: **è**. Aggettivo singolare: **gentile**."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Lo sbaglio e non grave.",
            "Il sbaglio non è grave.",
            "Lo sbaglio non è grave."
        ],
        "resposta": 2,
        "explicacao": "Sbaglio inizia con sb (s + consonante) → **LO**. La negazione **non** va prima del verbo: non è (non: è non)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Le citte sono sporche e rumorose.",
            "Le città sono sporche e rumorose.",
            "Le cità sono sporche e rumorose."
        ],
        "resposta": 1,
        "explicacao": "Città è invariabile al plurale: **le città** (non citte né cità). I nomi in **-tà** non cambiano."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Io ho non soldi.",
            "Io non ho soldi.",
            "Io ha non soldi."
        ],
        "resposta": 1,
        "explicacao": "La negazione **non** va immediatamente prima del verbo: io **non ho**. 'Ha' è la forma di lui/lei, non di io."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "I studenti sono stranieri.",
            "Gli estudenti sono stranieri.",
            "Gli studenti sono stranieri."
        ],
        "resposta": 2,
        "explicacao": "Studenti inizia con st (s + consonante) → articolo plurale: **GLI**. 'Estudenti' non esiste in italiano."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Sono uno studente della Germania.",
            "Sono uno studente di Germania.",
            "Sono uno studente tedesco."
        ],
        "resposta": 2,
        "explicacao": "Per indicare nazionalità si usa l'aggettivo: **tedesco**. 'Della Germania' o 'di Germania' sono forme scorrette per esprimere nazionalità."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Questa canzone è bella.",
            "Queste canzone è bella.",
            "Queste canzone e belle."
        ],
        "resposta": 0,
        "explicacao": "Canzone è femminile singolare → **Questa** canzone **è** bella. 'Queste' è plurale e non concorda con il singolare."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Non c'è stanze grandi.",
            "Non ci sono stanze grandi.",
            "Non ci sono stanze grande."
        ],
        "resposta": 1,
        "explicacao": "**Ci sono** con il plurale. Stanze grandi: aggettivo femminile plurale. 'C'è' è solo per il singolare."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Maria è un'amica di Cristina.",
            "Maria è un amica di Cristina.",
            "Maria è una amica di Cristina."
        ],
        "resposta": 0,
        "explicacao": "Amica è femminile e inizia con vocale → **un'amica** (con apostrofo). 'Una amica' si elide obbligatoriamente davanti a vocale."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Il orologio è fermo.",
            "L'orologio è fermo.",
            "Lo orologio è fermo."
        ],
        "resposta": 1,
        "explicacao": "Orologio è maschile e inizia con vocale → **L'orologio** (elisione). 'Il orologio' e 'Lo orologio' sono scorretti davanti a vocale."
    },

    # ══════════════════════════════════════════════════════════
    #  TROVARE GLI ERRORI  (5 domande)
    # ══════════════════════════════════════════════════════════

    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Il zio italiano.»",
        "resposta": "Lo zio italiano.",
        "explicacao": "Zio inizia con z → si usa **LO** (non il). Lo zio / gli zii."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Un'orologio svizzero.»",
        "resposta": "Un orologio svizzero.",
        "explicacao": "Orologio è **maschile**. Un' si usa solo per femminili davanti a vocale (un'ora, un'idea). Corretto: **UN** orologio."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Le spiegazioni sono facile.»",
        "resposta": "Le spiegazioni sono facili.",
        "explicacao": "L'aggettivo concorda con il sostantivo: spiegazioni (femminile plurale) → **facili** (plurale)."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Il autobus non è puntuale.»",
        "resposta": "L'autobus non è puntuale.",
        "explicacao": "Autobus inizia con vocale → **L'autobus** (elisione). 'Il' si usa solo davanti a consonante."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Il scherzo è divertente.»",
        "resposta": "Lo scherzo è divertente.",
        "explicacao": "Scherzo inizia con sch (s + consonante) → **LO** scherzo. Plurale: gli scherzi."
    },
]

exemplos = [
    {"it": "Il quaderno è nuovo; i quaderni sono nuovi.", "pt": "O caderno é novo; os cadernos são novos."},
    {"it": "Lo studente studia molto; gli studenti studiano molto.", "pt": "O estudante estuda muito; os estudantes estudam muito."},
    {"it": "La lezione è interessante; le lezioni sono interessanti.", "pt": "A lição é interessante; as lições são interessantes."},
    {"it": "C'è un libro sul tavolo. Ci sono dei libri sul tavolo.", "pt": "Há um livro na mesa. Há livros na mesa."},
    {"it": "Io sono Marco. Tu sei Maria. Lei è la professoressa.", "pt": "Eu sou Marco. Você é Maria. Ela é a professora."},
]

lez1 = {
    "id": "a1-lez1",
    "num": "Lezione I",
    "titulo": "Nome, Articolo e Aggettivo",
    "subtitulo": "Strutture elementari",
    "teoria": teoria,
    "exemplos": exemplos,
    "exercicios": exercicios
}

data['moduli'][0]['unidades'][0] = lez1

with open(r'grammar.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

u = data['moduli'][0]['unidades'][0]
escolha = sum(1 for e in u['exercicios'] if e['tipo'] == 'escolha')
revelar = sum(1 for e in u['exercicios'] if e['tipo'] == 'revelar')
print(f"OK: {u['num']} - {u['titulo']}")
print(f"Teoria: {len(u['teoria'])} chars")
print(f"Exemplos: {len(u['exemplos'])}")
print(f"Exercicios: {len(u['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
print(f"  - Esercizi 1-18: {revelar - 5} revelar")
print(f"  - Esercizi di verifica: {escolha} escolha")
print(f"  - Trovare gli errori: 5 revelar")
