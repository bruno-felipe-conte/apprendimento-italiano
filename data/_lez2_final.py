import json

with open(r'grammar.json', encoding='utf-8') as f:
    data = json.load(f)

teoria_lines = [
    "**A. Il presente indicativo dei verbi regolari**",
    "",
    """<table class="gram-table gram-table-rich">
<thead>
<tr><th></th><th>I (-ARE)<br><em>guardare</em></th><th>II (-ERE)<br><em>vivere</em></th><th>III (-IRE)<br><em>aprire</em></th><th>III (-IRE)<br><em>finire</em></th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>guardo</td><td>vivo</td><td>apro</td><td>finisco</td></tr>
<tr><td class="gram-art">tu</td><td>guardi</td><td>vivi</td><td>apri</td><td>finisci</td></tr>
<tr><td class="gram-art">lui / lei / Lei</td><td>guarda</td><td>vive</td><td>apre</td><td>finisce</td></tr>
<tr><td class="gram-art">noi</td><td>guardiamo</td><td>viviamo</td><td>apriamo</td><td>finiamo</td></tr>
<tr><td class="gram-art">voi</td><td>guardate</td><td>vivete</td><td>aprite</td><td>finite</td></tr>
<tr><td class="gram-art">loro</td><td>guardano</td><td>vivono</td><td>aprono</td><td>finiscono</td></tr>
</tbody></table>""",
    "",
    "**Regola:** Verbi in **-IRE** tipo *finire* aggiungono **-isc-** nelle forme singolari e in *loro* (finisco, finisci, finisce, finiscono). Verbi tipo *aprire* no (apro, apri, apre, aprono).",
    "",
    "**B. Verbi in -CARE e -GARE**",
    "",
    """<table class="gram-table gram-table-rich">
<thead>
<tr><th></th><th><em>parlare</em></th><th><em>cercare</em></th><th><em>pagare</em></th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>parlo</td><td>cerco</td><td>pago</td></tr>
<tr><td class="gram-art">tu</td><td>parli</td><td><strong>cerchi</strong></td><td><strong>paghi</strong></td></tr>
<tr><td class="gram-art">lui / lei</td><td>parla</td><td>cerca</td><td>paga</td></tr>
<tr><td class="gram-art">noi</td><td>parliamo</td><td><strong>cerchiamo</strong></td><td><strong>paghiamo</strong></td></tr>
<tr><td class="gram-art">voi</td><td>parlate</td><td>cercate</td><td>pagate</td></tr>
<tr><td class="gram-art">loro</td><td>parlano</td><td>cercano</td><td>pagano</td></tr>
</tbody></table>""",
    "",
    "**Regola:** Verbi in **-CARE** e **-GARE** mantengono il suono duro aggiungendo **h** davanti a **-i** (tu cerchi / noi cerchiamo; tu paghi / noi paghiamo).",
    "",
    "**C. Verbi ESSERE e AVERE**",
    "",
    """<table class="gram-table gram-table-rich">
<thead><tr><th>persona</th><th>ESSERE</th><th>AVERE</th></tr></thead>
<tbody>
<tr><td class="gram-art">io</td><td>sono</td><td>ho</td></tr>
<tr><td class="gram-art">tu</td><td>sei</td><td>hai</td></tr>
<tr><td class="gram-art">lui / lei / Lei</td><td>è</td><td>ha</td></tr>
<tr><td class="gram-art">noi</td><td>siamo</td><td>abbiamo</td></tr>
<tr><td class="gram-art">voi</td><td>siete</td><td>avete</td></tr>
<tr><td class="gram-art">loro</td><td>sono</td><td>hanno</td></tr>
</tbody></table>""",
    "",
    "**D. Verbi irregolari al presente**",
    "",
    """<table class="gram-table gram-table-rich">
<thead><tr><th></th><th><em>fare</em></th><th><em>sapere</em></th><th><em>bere</em></th><th><em>stare</em></th></tr></thead>
<tbody>
<tr><td class="gram-art">io</td><td>faccio</td><td>so</td><td>bevo</td><td>sto</td></tr>
<tr><td class="gram-art">tu</td><td>fai</td><td>sai</td><td>bevi</td><td>stai</td></tr>
<tr><td class="gram-art">lui / lei</td><td>fa</td><td>sa</td><td>beve</td><td>sta</td></tr>
<tr><td class="gram-art">noi</td><td>facciamo</td><td>sappiamo</td><td>beviamo</td><td>stiamo</td></tr>
<tr><td class="gram-art">voi</td><td>fate</td><td>sapete</td><td>bevete</td><td>state</td></tr>
<tr><td class="gram-art">loro</td><td>fanno</td><td>sanno</td><td>bevono</td><td>stanno</td></tr>
</tbody></table>""",
    "",
    """<table class="gram-table gram-table-rich">
<thead><tr><th></th><th><em>venire</em></th><th><em>andare</em></th><th><em>dovere</em></th><th><em>potere</em></th><th><em>volere</em></th></tr></thead>
<tbody>
<tr><td class="gram-art">io</td><td>vengo</td><td>vado</td><td>devo</td><td>posso</td><td>voglio</td></tr>
<tr><td class="gram-art">tu</td><td>vieni</td><td>vai</td><td>devi</td><td>puoi</td><td>vuoi</td></tr>
<tr><td class="gram-art">lui / lei</td><td>viene</td><td>va</td><td>deve</td><td>può</td><td>vuole</td></tr>
<tr><td class="gram-art">noi</td><td>veniamo</td><td>andiamo</td><td>dobbiamo</td><td>possiamo</td><td>vogliamo</td></tr>
<tr><td class="gram-art">voi</td><td>venite</td><td>andate</td><td>dovete</td><td>potete</td><td>volete</td></tr>
<tr><td class="gram-art">loro</td><td>vengono</td><td>vanno</td><td>devono</td><td>possono</td><td>vogliono</td></tr>
</tbody></table>""",
    "",
    """<table class="gram-table gram-table-rich">
<thead><tr><th></th><th><em>dire</em></th><th><em>uscire</em></th><th><em>salire</em></th><th><em>scegliere</em></th></tr></thead>
<tbody>
<tr><td class="gram-art">io</td><td>dico</td><td>esco</td><td>salgo</td><td>scelgo</td></tr>
<tr><td class="gram-art">tu</td><td>dici</td><td>esci</td><td>sali</td><td>scegli</td></tr>
<tr><td class="gram-art">lui / lei</td><td>dice</td><td>esce</td><td>sale</td><td>sceglie</td></tr>
<tr><td class="gram-art">noi</td><td>diciamo</td><td>usciamo</td><td>saliamo</td><td>scegliamo</td></tr>
<tr><td class="gram-art">voi</td><td>dite</td><td>uscite</td><td>salite</td><td>scegliete</td></tr>
<tr><td class="gram-art">loro</td><td>dicono</td><td>escono</td><td>salgono</td><td>scelgono</td></tr>
</tbody></table>""",
    "",
    "**E. Vocabolario sistematico**",
    "",
    "**I giorni della settimana:** lunedì, martedì, mercoledì, giovedì, venerdì, sabato, domenica.",
    "",
    "**I mesi dell'anno:** gennaio, febbraio, marzo, aprile, maggio, giugno, luglio, agosto, settembre, ottobre, novembre, dicembre.",
    "",
    "**I numeri ordinali:**",
    "",
    "| | | |",
    "|-|-|-|",
    "| 1° primo/a | 2° secondo/a | 3° terzo/a |",
    "| 4° quarto/a | 5° quinto/a | 6° sesto/a |",
    "| 7° settimo/a | 8° ottavo/a | 9° nono/a |",
    "| 10° decimo/a | 11° undicesimo/a | 12° dodicesimo/a |",
    "",
    "**F. C'è / Ci sono — uso in contesto**",
    "",
    "Che cosa **c'è** sul tavolo? → Sul tavolo **c'è** il libro.",
    "Dov'è il libro? → Il libro **è** sul tavolo.",
    "",
    "Chi **ci sono** nella classe? → Nella classe **ci sono** gli studenti.",
    "Dove sono gli studenti? → Gli studenti **sono** nella classe.",
]

teoria = "\n".join(teoria_lines)

exercicios = [

    # ══════════════════════════════════════════════════════════
    #  ESERCIZI 1–8  (dal libro)
    # ══════════════════════════════════════════════════════════

    # ── Esercizio 1 — Trasformare ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 1** — Trasformare secondo il soggetto indicato:\n\n1. Maria accompagna i bambini a scuola. → *noi*\n2. Luisa saluta i suoi amici. → *io / tu / voi*\n3. La segretaria entra in classe. → *io / tu / noi / voi / loro*\n4. Il direttore chiama la studentessa. → *io / tu / noi / voi / loro*\n5. Incontro gli amici al bar. → *lei / noi / voi / loro*\n6. Mario studia a Roma. → *io / tu / noi / voi / loro*\n7. Tu aspetti l'autobus. → *lui / noi / voi / loro*\n8. Leggi un libro. → *voi / loro*\n9. Voi scrivete l'esercizio sul quaderno. → *lei / io / noi*\n10. Apro il negozio alle sette. → *tu / lui / noi / voi / loro*\n11. Carlo riceve molte lettere. → *io / tu / noi / voi / loro*\n12. Butto via i vestiti vecchi. → *lei / noi / tu / voi / loro*",
        "resposta": "1. Noi accompagniamo i bambini a scuola.\n2. Io saluto i miei amici. / Tu saluti i tuoi amici. / Voi salutate i vostri amici.\n3. Io entro / tu entri / noi entriamo / voi entrate / loro entrano in classe.\n4. Io chiamo / tu chiami / noi chiamiamo / voi chiamate / loro chiamano la studentessa.\n5. Lei incontra / noi incontriamo / voi incontrate / loro incontrano gli amici al bar.\n6. Io studio / tu studi / noi studiamo / voi studiate / loro studiano a Roma.\n7. Lui aspetta / noi aspettiamo / voi aspettate / loro aspettano l'autobus.\n8. Voi leggete / loro leggono un libro.\n9. Lei scrive / io scrivo / noi scriviamo l'esercizio sul quaderno.\n10. Tu apri / lui apre / noi apriamo / voi aprite / loro aprono il negozio alle sette.\n11. Io ricevo / tu ricevi / noi riceviamo / voi ricevete / loro ricevono molte lettere.\n12. Lei butta / noi buttiamo / tu butti / voi buttate / loro buttano via i vestiti vecchi.",
        "explicacao": "Verbi -ARE: -o/-i/-a/-iamo/-ate/-ano. Verbi -ERE: -o/-i/-e/-iamo/-ete/-ono. Verbi -IRE (tipo aprire): -o/-i/-e/-iamo/-ite/-ono. Studiare → studi (non studii)."
    },

    # ── Esercizio 2 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 2** — Come il precedente. Trasformare:\n\n1. Cambia la tua vecchia automobile. → *io / noi / loro*\n2. Non capisco la spiegazione dell'insegnante. → *lei / noi / loro*\n3. Loro comprano la frutta al mercato. → *io / tu / voi*\n4. Luisa copia le frasi sul quaderno. → *io / voi / noi*\n5. La professoressa corregge le frasi sbagliate. → *io / tu / voi / loro*\n6. Io desidero salutare Antonio. → *lei / noi / loro*\n7. Dimentico spesso le chiavi di casa. → *voi / tu / loro*\n8. Michele dipinge da molti anni. → *io / tu / loro*\n9. Anna divide la camera con una ragazza brasiliana. → *io / noi / loro*\n10. Noi finiamo di studiare alle cinque. → *voi / loro / tu*\n11. Io firmo un assegno. → *tu / lei / loro*\n12. Lei fissa l'appuntamento con Giorgio al bar. → *io / noi / loro*",
        "resposta": "1. Io cambio / noi cambiamo / loro cambiano la loro vecchia automobile.\n2. Lei non capisce / noi non capiamo / loro non capiscono la spiegazione.\n3. Io compro / tu compri / voi comprate la frutta al mercato.\n4. Io copio / voi copiate / noi copiamo le frasi sul quaderno.\n5. Io correggo / tu correggi / voi correggete / loro correggono le frasi sbagliate.\n6. Lei desidera / noi desideriamo / loro desiderano salutare Antonio.\n7. Voi dimenticate / tu dimentichi / loro dimenticano spesso le chiavi di casa.\n8. Io dipingo / tu dipingi / loro dipingono da molti anni.\n9. Io divido / noi dividiamo / loro dividono la camera.\n10. Voi finite / loro finiscono / tu finisci di studiare alle cinque.\n11. Tu firmi / lei firma / loro firmano un assegno.\n12. Io fisso / noi fissiamo / loro fissano l'appuntamento con Giorgio al bar.",
        "explicacao": "Capire (tipo -isc): capisco/capisci/capisce/capiamo/capite/capiscono. Correggere→correggo/correggi/corregge. Dipingere→dipingo/dipingi/dipinge."
    },

    # ── Esercizio 3 — Trasformare (verbi misti) ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 3** — Trasformare:\n\n1. Guardo la televisione. → *lei / voi / noi*\n2. Lei non guida la macchina. → *io / loro / voi*\n3. Spendiamo molti soldi a Firenze. → *io / voi / loro*\n4. Parto per gli Stati Uniti. → *noi / voi / loro*\n5. Anna suona la chitarra. → *noi / io / voi*\n6. Rispondo alla tua domanda. → *noi / loro*\n7. Pietro non capisce queste parole. → *tu / noi / loro*\n8. Ogni giorno pranzo a casa. → *noi / voi / loro*\n9. Conosco molto bene sua moglie. → *noi / voi / loro*\n10. Preferisco restare a casa. → *voi / noi / loro*\n11. Regalo dei fiori a quella ragazza. → *noi / tu / loro*\n12. Preparo la cena per i miei amici. → *voi / lei*",
        "resposta": "1. Lei guarda / voi guardate / noi guardiamo la televisione.\n2. Io non guido / loro non guidano / voi non guidate la macchina.\n3. Io spendo / voi spendete / loro spendono molti soldi a Firenze.\n4. Noi partiamo / voi partite / loro partono per gli Stati Uniti.\n5. Noi suoniamo / io suono / voi suonate la chitarra.\n6. Noi rispondiamo / loro rispondono alla tua domanda.\n7. Tu non capisci / noi non capiamo / loro non capiscono queste parole.\n8. Noi pranziamo / voi pranzate / loro pranzano a casa ogni giorno.\n9. Noi conosciamo / voi conoscete / loro conoscono molto bene sua moglie.\n10. Voi preferite / noi preferiamo / loro preferiscono restare a casa.\n11. Noi regaliamo / tu regali / loro regalano dei fiori a quella ragazza.\n12. Voi preparate / lei prepara la cena per i suoi amici.",
        "explicacao": "Preferire (tipo -isc): preferisco/preferisci/preferisce/preferiamo/preferite/preferiscono. Conoscere→conosco/conosci/conosce. Spendere→spendo/spendi/spende."
    },

    # ── Esercizio 4 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 4** — Come il precedente:\n\n1. Spiego il presente allo studente. → *tu / noi / voi*\n2. Cerco le chiavi di casa. → *tu / noi / lei*\n3. Offriamo la cena agli amici. → *voi / tu*\n4. Telefona a Paolo una volta al giorno. → *io / tu / noi / voi / loro*\n5. Spedisco la lettera per via aerea. → *tu / lei / noi / voi / loro*\n6. Pagate il conto. → *io / tu / lui / noi / loro*\n7. Dormo nove ore al giorno. → *tu / lui / noi / voi / loro*\n8. Cucino gli spaghetti. → *tu / lei / noi / voi / loro*\n9. Apro la finestra. → *tu / lei / noi / voi / loro*\n10. Rispondo al professore. → *tu / lui / noi / voi / loro*\n11. Cantiamo una canzone. → *io / tu / voi / loro*\n12. Vedo Luisa al bar. → *tu / lei / noi / voi / loro*",
        "resposta": "1. Tu spieghi / noi spieghiamo / voi spiegate il presente allo studente.\n2. Tu cerchi / noi cerchiamo / lei cerca le chiavi di casa.\n3. Voi offrite / tu offri la cena agli amici.\n4. Io telefono / tu telefoni / noi telefoniamo / voi telefonate / loro telefonano a Paolo.\n5. Tu spedisci / lei spedisce / noi spediamo / voi spedite / loro spediscono la lettera.\n6. Io pago / tu paghi / lui paga / noi paghiamo / loro pagano il conto.\n7. Tu dormi / lui dorme / noi dormiamo / voi dormite / loro dormono nove ore al giorno.\n8. Tu cucini / lei cucina / noi cuciniamo / voi cucinate / loro cucinano gli spaghetti.\n9. Tu apri / lei apre / noi apriamo / voi aprite / loro aprono la finestra.\n10. Tu rispondi / lui risponde / noi rispondiamo / voi rispondete / loro rispondono al professore.\n11. Io canto / tu canti / voi cantate / loro cantano una canzone.\n12. Tu vedi / lei vede / noi vediamo / voi vedete / loro vedono Luisa al bar.",
        "explicacao": "Spiegare→spieghiamo (mant. suono duro). Cercare→cerchi/cerchiamo (h davanti a -i). Pagare→paghi/paghiamo. Spedire (tipo -isc): spedisco/spedisci/spedisce/spediamo/spedite/spediscono."
    },

    # ── Esercizio 5 — Volgere al presente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Volgere al presente (coniugare il verbo tra parentesi):\n\n1. Io (andare) a scuola per imparare l'italiano.\n2. Luigi (mangiare) poco perché (non volere) ingrassare.\n3. Quale (essere) il tuo libro?\n4. Roberto e Laura (rimanere) a Firenze.\n5. Io (lavorare) in un ufficio.\n6. Lucia (uscire) con gli amici.\n7. (Noi / comprare) questo orologio per Lucia.\n8. Oggi (io / dovere) studiare i verbi irregolari.\n9. I miei fratelli (stare) molto bene.\n10. Questo bambino (dire) sempre la verità.\n11. (Noi / salire) su quest'autobus o su quell'altro?",
        "resposta": "1. vado\n2. mangia / non vuole\n3. è\n4. rimangono\n5. lavoro\n6. esce\n7. compriamo\n8. devo\n9. stanno\n10. dice\n11. Saliamo",
        "explicacao": "Andare→vado/vai/va/andiamo/andate/vanno. Volere→voglio/vuoi/vuole. Rimanere→rimango/rimani/rimane/rimaniamo/rimanete/rimangono. Uscire→esco/esci/esce/usciamo/uscite/escono. Stare→sto/stai/sta/stiamo/state/stanno."
    },

    # ── Esercizio 6 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 6** — Come il precedente:\n\n1. Signorina, (fumare)?\n2. (Voi / volere) una tazza di tè?\n3. Anna, (noi / venire) subito!\n4. (Noi / tradurre) questa frase in italiano.\n5. Massimo e io (cercare) una casa in campagna.\n6. Professore, (io / non capire) cosa (Lei / dire).\n7. Carlo e Marisa (viaggiare) molto in estate.\n8. (Io / finire) di pranzare alle due.\n9. Chi (abitare) in questa casa?\n10. Laura (non sapere) il nostro indirizzo.\n11. Che cosa (tu / cercare)?\n12. Oggi (io / essere) contento perché (arrivare) Carlo e Marta.",
        "resposta": "1. fuma\n2. volete\n3. veniamo\n4. traduciamo\n5. cerchiamo\n6. non capisco / dice\n7. viaggiano\n8. finisco\n9. abita\n10. non sa\n11. cerchi\n12. sono / arriva",
        "explicacao": "Venire→vengo/vieni/viene/veniamo/venite/vengono. Tradurre→traduco/traduci/traduce/traduciamo/traducete/traducono. Cercare→cerchiamo (h). Finire (tipo -isc): finisco."
    },

    # ── Esercizio 7 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 7** — Come il precedente:\n\n1. Signorina, (capire) quando (io / parlare) italiano?\n2. (Io / vivere) a Firenze da due settimane.\n3. (Tu / avere) una sigaretta, per favore?\n4. (Io / aprire) la finestra perché (fare) molto caldo.\n5. Luca e Donatella (abitare) in una casa molto grande.\n6. (Noi / leggere) questo libro in classe.\n7. (Io / frequentare) una scuola di musica.\n8. Quale vino (voi / bere) a tavola?\n9. Silvio (ascoltare) la radio mentre (lavorare).\n10. (Io / fumare) dieci sigarette al giorno.\n11. Maria (scrivere) una lettera a sua madre.\n12. Lisa (offrire) dei dolci agli ospiti.",
        "resposta": "1. capisce / parlo\n2. vivo\n3. hai\n4. apro / fa\n5. abitano\n6. leggiamo\n7. frequento\n8. bevete\n9. ascolta / lavora\n10. fumo\n11. scrive\n12. offre",
        "explicacao": "Capire→capisce (tipo -isc). Fare→fa (irregolare). Bere→bevo/bevi/beve/beviamo/bevete/bevono. Leggere→leggo/leggi/legge/leggiamo/leggete/leggono. Scrivere→scrivo/scrivi/scrive."
    },

    # ── Esercizio 8 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 8** — Come il precedente:\n\n1. Piera (non sapere) cucinare.\n2. Stasera Aldo e Alberto (andare) al cinema.\n3. Signora, (Lei / conoscere) la galleria degli Uffizi?\n4. Maria (lavare) i piatti.\n5. Io (andare) al circo; (voi / volere) venire con me?\n6. Carla, Lei (parlare) molto bene il tedesco!\n7. Gianni, a che ora (uscire) dall'ufficio?\n8. Nella nostra biblioteca (avere) molti libri di filosofia.\n9. Gli operai di quella fabbrica (essere) in sciopero.\n10. (Noi / preparare) la cena per i nostri amici.\n11. La scuola (organizzare) ogni mese delle gite turistiche.\n12. Guido (accompagnare) gli studenti al museo.",
        "resposta": "1. non sa\n2. vanno\n3. conosce\n4. lava\n5. vado / volete\n6. parla\n7. esci\n8. abbiamo\n9. sono\n10. prepariamo\n11. organizza\n12. accompagna",
        "explicacao": "Sapere→so/sai/sa/sappiamo/sapete/sanno. Andare→vanno (loro). Conoscere→conosco/conosci/conosce. Uscire→esco/esci/esce/usciamo/uscite/escono."
    },

    # ── Lavorare sul testo — A scuola ──
    {
        "tipo": "revelar",
        "pergunta": "**Lavorare sul testo — «A scuola»**\n\nStephen è un ragazzo americano di New York. Ora è a Firenze e frequenta un corso di lingua italiana per stranieri. Nella sua classe ci sono dieci studenti di nazionalità differenti: tre tedeschi, due greci, due messicani, un austriaco e un ungherese. Gli studenti conoscono solo poche parole italiane, perciò fra loro parlano l'inglese o il tedesco, ma durante le lezioni cercano di usare solo la lingua italiana. Ogni settimana Stephen ha venti ore di lezione e i suoi insegnanti sono tre: uno di grammatica, uno di conversazione e uno di lessico. Il sabato e la domenica non c'è scuola, così Stephen va con i suoi compagni di classe a fare una gita in una città vicina o in campagna.\n\n**Rispondere alle domande:**\n1. Di dov'è Stephen?\n2. Dov'è ora?\n3. Che cosa fa?\n4. Quanti studenti ci sono nella sua classe?\n5. Di quali nazionalità sono?\n6. Quale lingua parlano fra loro?\n7. Perché?\n8. Che lingua cercano di usare durante le lezioni?\n9. Quante ore di lezione ci sono ogni settimana?\n10. Che cosa fa Stephen il sabato e la domenica?",
        "resposta": "1. Stephen è di New York (americano).\n2. Ora è a Firenze.\n3. Frequenta un corso di lingua italiana per stranieri.\n4. Nella sua classe ci sono dieci studenti.\n5. Tre tedeschi, due greci, due messicani, un austriaco e un ungherese.\n6. Fra loro parlano l'inglese o il tedesco.\n7. Perché conoscono solo poche parole italiane.\n8. Durante le lezioni cercano di usare solo la lingua italiana.\n9. Ogni settimana ha venti ore di lezione.\n10. Il sabato e la domenica va con i suoi compagni di classe a fare una gita in una città vicina o in campagna.",
        "explicacao": "Frequentare, cercare, usare, andare — tutti verbi usati in questo brano. Osservare: 'perciò' (= quindi/pertanto), 'così' (= per questo motivo), 'vicino/a' (aggettivo che concorda con il nome)."
    },

    # ══════════════════════════════════════════════════════════
    #  ESERCIZI DI VERIFICA  (18 domande — Scegliere la frase corretta)
    # ══════════════════════════════════════════════════════════

    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Io aspetto l'autobus e torna a casa.",
            "Io aspetto l'autobus e torno a casa.",
            "Io aspetta l'autobus e torna a casa."
        ],
        "resposta": 1,
        "explicacao": "Con il soggetto 'io': aspettare → **aspetto**; tornare → **torno**. La forma 'aspetta / torna' è di lui/lei."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Noi preferisciamo un caffè.",
            "Noi preferiamo un caffè.",
            "Noi preferimo un caffè."
        ],
        "resposta": 1,
        "explicacao": "Preferire (tipo -isc): io preferisco, tu preferisci, lui preferisce, **NOI PREFERIAMO**, voi preferite, loro preferiscono. La forma -isc NON si usa con noi e voi."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Io sono venti anni.",
            "Io ho venti anni.",
            "Io è venti anni."
        ],
        "resposta": 1,
        "explicacao": "L'età si esprime con **AVERE**: ho venti anni, hai trent'anni, ecc. Mai con essere."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Quando partite per Milano?",
            "Quando partete per Milano?",
            "Quando partate per Milano?"
        ],
        "resposta": 0,
        "explicacao": "Partire (tipo aprire): io parto, tu parti, lui parte, noi partiamo, **VOI PARTITE**, loro partono."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Sei grasso perché ___",
        "opcoes": [
            "mangii troppo.",
            "mangi troppo.",
            "mangia troppo."
        ],
        "resposta": 1,
        "explicacao": "Mangiare → tu **mangi** (non mangii). 'Mangia' è la forma di lui/lei."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Che cosa cerchi?",
            "Che cosa cerci?",
            "Che cosa cerchi tu?"
        ],
        "resposta": 0,
        "explicacao": "Cercare → tu **cerchi** (con h per mantenere il suono duro). 'Cerci' è errato. La risposta c) è grammaticalmente corretta ma ridondante (il tu è già nella forma verbale)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — A che ora ___?",
        "opcoes": [
            "cominchi?",
            "cominci?",
            "comincii?"
        ],
        "resposta": 1,
        "explicacao": "Cominciare → tu **cominci** (il gruppo -ci già ha il suono dolce, non serve aggiungere h)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Laura e Maria ___",
        "opcoes": [
            "spedono una cartolina.",
            "spediscono una cartolina.",
            "spedano una cartolina."
        ],
        "resposta": 1,
        "explicacao": "Spedire (tipo finire, con -isc): io spedisco, tu spedisci, lui spedisce, noi spediamo, voi spedite, **LORO SPEDISCONO**."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Loro ___",
        "opcoes": [
            "frequentino un corso d'italiano.",
            "frequentono un corso d'italiano.",
            "frequentano un corso d'italiano."
        ],
        "resposta": 2,
        "explicacao": "Frequentare (verbo -ARE): loro **frequentano**. 'Frequentino' è il congiuntivo; 'frequentono' non esiste."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Signora, Lei ___?",
        "opcoes": [
            "fumi",
            "fume",
            "fuma"
        ],
        "resposta": 2,
        "explicacao": "Fumare → lui/lei/Lei **fuma**. Con il pronome di cortesia Lei si usa la terza persona singolare."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Ciao, Mario, ___?",
        "opcoes": [
            "come sei",
            "come stai?",
            "come sta?"
        ],
        "resposta": 1,
        "explicacao": "'Come **stai**?' è la forma informale (tu). 'Come **sta**?' è la forma formale (Lei). Con 'Ciao' si usa l'informale: come stai?"
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Gli zii anno una casa grande.",
            "I zii hanno una casa grande.",
            "Gli zii hanno una casa grande."
        ],
        "resposta": 2,
        "explicacao": "Zio → zii (plurale). Inizia con z → articolo **GLI**. Avere → loro **HANNO** (non 'anno', che è l'anno del calendario)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Queste sono le nuove chiavi.",
            "Questi sono i nuovi chiavi.",
            "Queste sono le nuove chiave."
        ],
        "resposta": 0,
        "explicacao": "Chiave è femminile → **le chiavi** (plurale in -i). **Queste** (femminile plurale). **Nuove** (femminile plurale)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "La problema è semplice.",
            "Il problema è semplice.",
            "Lo problema è semplice."
        ],
        "resposta": 1,
        "explicacao": "Problema è maschile (come tema, poema, sistema). Inizia con pr (consonante normale) → **IL** problema."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "La dentista è bravo.",
            "Il dentista è brava.",
            "Il dentista è bravo."
        ],
        "resposta": 2,
        "explicacao": "Dentista è maschile quando si riferisce a un uomo → **IL dentista**. L'aggettivo concorda: **bravo** (maschile)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Pagamo noi il conto.",
            "Paghiamo noi il conto.",
            "Pagiamo noi il conto."
        ],
        "resposta": 1,
        "explicacao": "Pagare → noi **paghiamo** (h per mantenere il suono duro del g davanti a -iamo)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Pulisco la casa.",
            "Pulo la casa.",
            "Pulischo la casa."
        ],
        "resposta": 0,
        "explicacao": "Pulire (tipo finire, con -isc): io **PULISCO**. 'Pulo' e 'pulischo' non esistono."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la frase corretta:",
        "opcoes": [
            "Volono uscire.",
            "Vogliono uscire.",
            "Volgono uscire."
        ],
        "resposta": 1,
        "explicacao": "Volere (irregolare): io voglio, tu vuoi, lui vuole, noi vogliamo, voi volete, **LORO VOGLIONO**."
    },

    # ══════════════════════════════════════════════════════════
    #  TROVARE GLI ERRORI  (10 domande)
    # ══════════════════════════════════════════════════════════

    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Pagiamo il conto oggi.»",
        "resposta": "Paghiamo il conto oggi.",
        "explicacao": "Pagare → noi **paghiamo** (con h). 'Pagiamo' non mantiene il suono duro del g."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Capiscete se parlo italiano?»",
        "resposta": "Capite se parlo italiano?",
        "explicacao": "Capire → voi **capite** (non 'capiscete'). La forma -isc si usa solo con io/tu/lui/loro, non con noi e voi."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Quando finischi l'università?»",
        "resposta": "Quando finisci l'università?",
        "explicacao": "Finire → tu **finisci** (non 'finischi'). La forma corretta per 'tu' è finisci."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Corregghi bene gli errori.»",
        "resposta": "Correggi bene gli errori.",
        "explicacao": "Correggere → tu **correggi** (non 'corregghi'). I verbi in -ggere fanno tu correggi, lui corregge."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Legghe un libro interessante.»",
        "resposta": "Legge un libro interessante.",
        "explicacao": "Leggere → lui/lei **legge** (non 'legghe'). La h non si aggiunge in questo caso."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Io prepara la cena.»",
        "resposta": "Io preparo la cena.",
        "explicacao": "Preparare → io **preparo**. 'Prepara' è la forma di lui/lei/Lei."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Il spagnolo è una lingua neolatina.»",
        "resposta": "Lo spagnolo è una lingua neolatina.",
        "explicacao": "Spagnolo inizia con sp (s + consonante) → articolo **LO**, non il."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Gl'alberi sono alti.»",
        "resposta": "Gli alberi sono alti.",
        "explicacao": "Davanti a vocale il plurale maschile è **GLI** (non gl'). L'elisione non si usa con gli."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«La giacca e i pantaloni sono molti eleganti.»",
        "resposta": "La giacca e i pantaloni sono molto eleganti.",
        "explicacao": "'**Molto**' usato come avverbio (davanti ad aggettivo) è invariabile: molto elegante / molto eleganti."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Ho pochi amichi italiani.»",
        "resposta": "Ho pochi amici italiani.",
        "explicacao": "Amico → plurale **amici** (non amichi). Regola -co/-ca: amico/amici, medico/medici (3+ sillabe → senza h)."
    },
]

exemplos = [
    {"it": "Io guardo la televisione. Tu guardi un film. Lei guarda le notizie.", "pt": "Eu assisto televisão. Você assiste um filme. Ela assiste as notícias."},
    {"it": "Noi cerchiamo casa. Voi pagate il conto. Loro mangiano al ristorante.", "pt": "Nós procuramos casa. Vocês pagam a conta. Eles comem no restaurante."},
    {"it": "Io ho vent'anni. Tu hai fame? Lei ha fretta.", "pt": "Eu tenho vinte anos. Você está com fome? Ela está com pressa."},
    {"it": "Dove vai? Vado a casa. Cosa fai stasera? Non so ancora.", "pt": "Onde você vai? Vou para casa. O que você faz esta noite? Ainda não sei."},
    {"it": "Oggi è lunedì. Domani è martedì. Siamo nel mese di maggio.", "pt": "Hoje é segunda-feira. Amanhã é terça-feira. Estamos no mês de maio."},
]

lez2 = {
    "id": "a1-lez2",
    "num": "Lezione II",
    "titulo": "Il presente indicativo",
    "subtitulo": "Verbi regolari e irregolari",
    "teoria": teoria,
    "exemplos": exemplos,
    "exercicios": exercicios
}

data['moduli'][0]['unidades'][1] = lez2

with open(r'grammar.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

u = data['moduli'][0]['unidades'][1]
escolha = sum(1 for e in u['exercicios'] if e['tipo'] == 'escolha')
revelar = sum(1 for e in u['exercicios'] if e['tipo'] == 'revelar')
print(f"OK: {u['num']} - {u['titulo']}")
print(f"Teoria: {len(u['teoria'])} chars")
print(f"Exemplos: {len(u['exemplos'])}")
print(f"Exercicios: {len(u['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
print(f"  - Esercizi 1-8 + leitura: {revelar - 10} revelar")
print(f"  - Esercizi di verifica: {escolha} escolha")
print(f"  - Trovare gli errori: 10 revelar")
