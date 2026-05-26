import json

with open(r'grammar.json', encoding='utf-8') as f:
    data = json.load(f)

teoria_lines = [
    "**A. Le preposizioni semplici**",
    "",
    "| preposizione | uso principale | esempi |",
    "|--------------|----------------|--------|",
    "| **di** | possesso, materia, argomento | il libro *di* Mario / un vestito *di* cotone / parliamo *di* politica |",
    "| **a** | luogo (città), tempo, termine | vivo *a* Roma / *alle* cinque / do il libro *a* Maria |",
    "| **da** | provenienza, durata, scopo | vengo *da* Parigi / abito qui *da* due anni / occhiali *da* sole |",
    "| **in** | luogo (nazione/regione), mezzo | vivo *in* Italia / vado *in* treno / sono *in* ufficio |",
    "| **con** | compagnia, mezzo | esco *con* Laura / vengo *con* la bici |",
    "| **su** | sopra, argomento | il libro è *sul* tavolo / conto *su* di te |",
    "| **per** | destinazione, scopo, causa | parto *per* Roma / studio *per* imparare / grido *per* il dolore |",
    "| **fra / tra** | tempo futuro, mezzo | *fra* tre giorni / *tra* noi c'è amicizia |",
    "",
    "**B. Le preposizioni articolate**",
    "",
    """<table class="gram-table gram-table-rich">
<thead>
<tr><th></th><th class="gram-art"><em>il</em></th><th class="gram-art"><em>lo</em></th><th class="gram-art"><em>la</em></th><th class="gram-art"><em>l'</em></th><th class="gram-art"><em>i</em></th><th class="gram-art"><em>gli</em></th><th class="gram-art"><em>le</em></th></tr>
</thead>
<tbody>
<tr><td class="gram-genere">a</td><td>al</td><td>allo</td><td>alla</td><td>all'</td><td>ai</td><td>agli</td><td>alle</td></tr>
<tr><td class="gram-genere">da</td><td>dal</td><td>dallo</td><td>dalla</td><td>dall'</td><td>dai</td><td>dagli</td><td>dalle</td></tr>
<tr><td class="gram-genere">su</td><td>sul</td><td>sullo</td><td>sulla</td><td>sull'</td><td>sui</td><td>sugli</td><td>sulle</td></tr>
<tr><td class="gram-genere">di</td><td>del</td><td>dello</td><td>della</td><td>dell'</td><td>dei</td><td>degli</td><td>delle</td></tr>
<tr><td class="gram-genere">in</td><td>nel</td><td>nello</td><td>nella</td><td>nell'</td><td>nei</td><td>negli</td><td>nelle</td></tr>
</tbody></table>""",
    "",
    "**Regola:** Le preposizioni **con**, **per**, **fra**, **tra** generalmente NON si contraggono con l'articolo.",
    "",
    "**C. Preposizioni con i luoghi**",
    "",
    "| luogo | preposizione | esempi |",
    "|-------|--------------|--------|",
    "| città / paese / piccola isola | **a** | vivo *a* Roma / vado *a* Capri |",
    "| continente / nazione / regione / grande isola | **in** | vivo *in* Italia / vado *in* Toscana / *in* Sardegna |",
    "| nazione con articolo | **negli / nei / nelle** | vado *negli* Stati Uniti / *nei* Paesi Bassi |",
    "| persona / professionista | **da** | vado *dal* dottore / sono *da* Giulia |",
    "",
    "**D. Preposizioni con i mezzi di trasporto**",
    "",
    "Vado in macchina / in treno / in autobus / in bicicletta / in aereo.",
    "Vado **a** piedi. (unico caso con *a*)",
    "",
    "**E. Avverbi di frequenza** (dal più frequente al meno frequente)",
    "",
    "| | | | | | | | |",
    "|-|-|-|-|-|-|-|-|",
    "| *sempre* | *molto spesso* | *spesso* | *abbastanza spesso* | *ogni tanto* | *raramente* | *quasi mai* | *mai* |",
    "",
    "**Uso:** Non prendo **mai** il caffè la sera. / Mario va **sempre** a scuola a piedi.",
    "",
    "**F. Preposizioni con avverbi di luogo**",
    "",
    "Intorno **alla** casa c'è un giardino. / Dietro **alla** villa c'è un orto.",
    "Laura abita lontano **dal** centro. / Il ragazzo siede accanto **a** Guido.",
    "Davanti **alla** scuola c'è un cinema. / Gira prima **a** sinistra, poi **a** destra.",
]

teoria = "\n".join(teoria_lines)

exercicios = [

    # ══════════════════════════════════════════════════════════
    #  ESERCIZI 1–11  (dal libro)
    # ══════════════════════════════════════════════════════════

    # ── Esercizio 1 — Completare con le preposizioni ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 1** — Completare con le preposizioni:\n\n1. Anna abita ___ via Torino.\n2. Conosco tuo padre ___ molti anni.\n3. Questo bicchiere non è ___ vetro, ma ___ cristallo.\n4. Vado ___ Mantova ___ Laura.\n5. ___ Carlo e Anna ci sono molti problemi.\n6. Il professore parla ___ Leonardo Sciascia.\n7. ___ dove vieni? Sono ___ Francoforte.\n8. ___ chi sono queste foto? Sono ___ Pietro.\n9. Andiamo ___ cena ___ mio zio.\n10. ___ che ora aprono i negozi?\n11. Torno ___ casa ___ piedi.\n12. ___ questa casa ci sono quattro stanze.\n13. ___ chi esci la sera?\n14. ___ gli amici.\n15. ___ quella collina c'è la casa di Andrea.\n16. ___ tre ore arriva il padre di Giacomo.\n17. Il giovane ___ la giacca chiara è mio fratello.\n18. Sono ___ Firenze ___ studiare l'italiano.\n19. ___ noi va bene.\n20. Resto in questa città ___ tre mesi.",
        "resposta": "1. in via Torino\n2. da molti anni\n3. di vetro / di cristallo\n4. a Mantova / con Laura\n5. Tra Carlo e Anna\n6. di Leonardo Sciascia\n7. Da dove vieni? / di Francoforte\n8. Di chi sono? / di Pietro\n9. a cena / da mio zio\n10. A che ora\n11. a casa / a piedi\n12. In questa casa\n13. Con chi\n14. Con gli amici\n15. Su quella collina\n16. Fra/Tra tre ore\n17. con la giacca chiara\n18. a Firenze / per studiare\n19. Per noi\n20. per tre mesi",
        "explicacao": "Di: possesso/materia. A: città/ora. Da: durata/persona. In: luogo interno. Con: compagnia. Su: sopra. Per: scopo/durata. Fra/Tra: tempo futuro."
    },

    # ── Esercizio 2 — Completare con le preposizioni articolate ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 2** — Completare con le preposizioni:\n\n**a) Dove tieni i tuoi soldi?**\n___ banca. / ___ tasca ___ cappotto. / Nella Banca Toscana. / ___ tasche ___ pantaloni. / ___ casa. / ___ borsa ___ pelle. / ___ cassetto.\n\n**b) Dove tieni la tua macchina?**\n___ garage. / ___ strada. / ___ garage ___ via del Corso. / ___ fronte a casa.\n\n**c) A chi scrivi?**\n___ miei amici. / ___ studenti della mia classe. / ___ avvocato.\n\n**d) Da chi vai stasera?**\n___ Giovanna. / ___ amico di mia sorella. / ___ professore.\n\n**e) Di chi sono questi libri?**\nSono ___ mie amiche tedesche. / ___ segretaria. / ___ mio medico. / ___ miei amici. / ___ meccanico. / ___ Carla.",
        "resposta": "a) In banca. / In tasca del cappotto. / Nelle tasche dei pantaloni. / In casa. / Nella borsa di pelle. / Nel cassetto.\n\nb) Nel garage. / Per strada. / Nel garage in via del Corso. / Di fronte a casa.\n\nc) Ai miei amici. / Agli studenti della mia classe. / All'avvocato.\n\nd) Da Giovanna. / Da un amico di mia sorella. / Dal professore.\n\ne) Sono delle mie amiche tedesche. / Della segretaria. / Del mio medico. / Dei miei amici. / Del meccanico. / Di Carla.",
        "explicacao": "di+il=del, di+lo=dello, di+la=della, di+l'=dell', di+i=dei, di+gli=degli, di+le=delle. a+il=al, a+gli=agli, a+le=alle. da+il=dal, da+il professore=dal professore."
    },

    # ── Esercizio 3 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 3** — Come il precedente:\n\n**a) Mando / Do:**\nMando i libri ___ mio amico. / Mando il regalo ___ amici di Pietro. / Mando la lettera ___ mie sorelle. / Do il diploma ___ studenti. / Do il diploma ___ ragazza di Sandro. / Mando il pacco ___ miei genitori. / Do il diploma ___ studentesse.\n\n**b) Ricevo:**\nRicevo i fiori ___ miei amici. / Ricevo i fiori ___ amici di Andrea. / Ricevo la lettera ___ studenti tedeschi. / Ricevo un regalo ___ amico di mia sorella. / Ricevo una telefonata ___ ragazza francese. / Ricevo una telefonata ___ insegnante. / Ricevo una telefonata ___ direttore. / Ricevo una telefonata ___ studentesse.\n\n**c) Metto / Tengo:**\nMetto i documenti ___ cassetto ___ scrivania. / Metto le chiavi ___ tasca. / Tengo i vestiti ___ armadio ___ camera da letto. / Metto i libri ___ libreria. / Metto la giacca ___ armadio ___ ingresso. / Metto l'assegno ___ portafoglio.\n\n**d) Luoghi:**\nGli uccelli vivono ___ alberi. / I gatti vivono ___ tetti. / La neve cade ___ montagne. / Lascio i libri ___ tavolo.\n\n**e) Di chi è?**\nIl libro è ___ direttrice. / La macchina è parcheggiata ___ ponte. / La borsa è ___ studentessa inglese. / L'ombrello è ___ insegnante di matematica. / Le valigie sono ___ studenti. / I bagagli sono ___ turisti.",
        "resposta": "a) al mio amico / agli amici di Pietro / alle mie sorelle / agli studenti / alla ragazza di Sandro / ai miei genitori / alle studentesse\n\nb) dai miei amici / dagli amici di Andrea / dagli studenti tedeschi / dall'amico di mia sorella / dalla ragazza francese / dall'insegnante / dal direttore / dalle studentesse\n\nc) nel cassetto della scrivania / in tasca / nell'armadio della camera da letto / nella libreria / nell'armadio dell'ingresso / nel portafoglio\n\nd) sugli alberi / sui tetti / sulle montagne / sul tavolo\n\ne) della direttrice / sotto il ponte / della studentessa inglese / dell'insegnante di matematica / degli studenti / dei turisti",
        "explicacao": "a/da/su/di/in + articolo formano contrazioni. Ricevere DA qualcuno. Mandare/dare A qualcuno. Su+gli=sugli, su+i=sui, su+le=sulle. Di+degli=degli."
    },

    # ── Esercizio 4 — Completare ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 4** — Completare con le preposizioni:\nMod.: *Il cappello nero è ___ direttore. → del direttore.*\n\n1. Quella ragazza ___ gonna rossa è la sorella ___ Pietro.\n2. Preferisco le persone ___ gli occhi scuri e ___ i capelli chiari.\n3. ___ inverno fa freddo ___ Firenze.\n4. ___ l'autobus sale molta gente.\n5. Sei venuto ___ macchina o ___ piedi?\n6. È bella la tua sciarpa ___ lana ___ righe bianche e rosse.\n7. Vado ___ montagna e porto gli scarponi ___ sci.\n8. Vado spesso ___ mare ___ estate.\n9. ___ primavera vado ___ campagna ___ bicicletta.\n10. ___ due giorni torna Claudio ___ vacanze.\n11. ___ notte i gatti miagolano ___ letti e ___ alberi.\n12. Abitiamo ___ questa casa ___ tre mesi.",
        "resposta": "1. con la gonna rossa / di Pietro\n2. con gli occhi scuri / con i capelli chiari\n3. D'/In inverno / a Firenze\n4. Sull'autobus (su+l')\n5. in macchina / a piedi\n6. di lana / con le righe\n7. in montagna / da sci\n8. al mare / in estate\n9. In primavera / in campagna / in bicicletta\n10. Fra/Tra due giorni / dalle vacanze\n11. Di notte / sui letti / sugli alberi\n12. in questa casa / da tre mesi",
        "explicacao": "Con: descrizione fisica. Di: materia/possesso. In: nazione/stagione/mezzo. A: città. Da sci: scopo (occhiali da sole, scarponi da sci). Dai vacanze: partenza."
    },

    # ── Conversazione: «In montagna» ──
    {
        "tipo": "revelar",
        "pergunta": "**Conversazione — «In montagna»**\n\nPaolo: Ehi, Giovanni, abbiamo due giorni di vacanza, tu che programmi hai?\nGiovanni: Penso di andare in montagna, all'Abetone, sulle Montagne Pistoiesi. Ho voglia di respirare un po' di aria fresca, di prendere il sole e di fare una bella camminata.\nPaolo: Vai da solo o con qualche amico?\nGiovanni: Vado con Giulia e suo fratello Carlo. Se non hai niente da fare, perché non vieni anche tu con noi?\nPaolo: Volentieri, grazie. Ma senti, andiamo con la macchina o con il pullman?\nGiovanni: Con la macchina. È più comodo; così possiamo partire e tornare quando vogliamo.\nPaolo: Hai proprio ragione, ma a che ora partiamo? Spero non troppo presto.\nGiovanni: No, no. Domani mattina voglio dormire fino alle nove. Alle dieci dobbiamo essere da Giulia. Partiamo da lì e poi passiamo a prendere Carlo.\n\n**Rispondere:**\n1. Dove vuole andare Giovanni?\n2. Con chi va?\n3. Come decidono di andare?\n4. A che ora devono essere da Giulia?\n5. Dove abita Giulia?",
        "resposta": "1. Giovanni vuole andare in montagna, all'Abetone, sulle Montagne Pistoiesi.\n2. Va con Giulia e suo fratello Carlo (e con Paolo).\n3. Decidono di andare con la macchina perché è più comodo.\n4. Alle dieci devono essere da Giulia.\n5. Giulia abita vicino a piazza Giuseppe Verdi, in via del Campanile al numero tre, secondo piano.",
        "explicacao": "Preposizioni chiave: IN montagna (regione/zona). ALL'Abetone (luogo specifico con articolo). DA Giulia (presso la casa di). CON la macchina (mezzo). FINO ALLE nove (limite di tempo)."
    },

    # ── Vocabolario sistematico — Avverbi di frequenza ──
    {
        "tipo": "revelar",
        "pergunta": "**Vocabolario sistematico — Avverbi di frequenza**\n\nMettere i seguenti avverbi in ordine di frequenza (dal più frequente al meno frequente):\n\nspesso / quasi mai / ogni tanto / sempre / abbastanza spesso / molto spesso / raramente / mai\n\n---\nCompletare con l'avverbio di frequenza appropriato:\na. Giovanni non ha la sveglia, così arriva ___ in ritardo a scuola.\nb. Non vedo ___ mia sorella perché vive in un'altra città.\nc. ___ incontro Laura per strada.\nd. Mario va ___ a scuola a piedi.\ne. La mia amica cucina ___ gli spaghetti perché le piacciono molto.\nf. Vengo ___ in questa città per motivi di lavoro.\ng. A pranzo mangio ___ a casa perché ho solo un'ora libera.\nh. Non prendo ___ il caffè la sera, altrimenti non dormo.",
        "resposta": "Ordine: sempre › molto spesso › spesso › abbastanza spesso › ogni tanto › raramente › quasi mai › mai\n\na. spesso\nb. quasi mai\nc. Ogni tanto\nd. sempre\ne. abbastanza spesso\nf. molto spesso\ng. raramente\nh. mai",
        "explicacao": "Non prendo MAI (mai in frase negativa viene dopo il verbo). Vai SEMPRE (sempre prima o dopo il verbo). Ogni tanto / raramente / quasi mai esprimono bassa frequenza."
    },

    # ── Esercizio 5 — Completare ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 5** — Completare con le preposizioni:\n\n1. Arrivo ___ casa ___ le otto ___ sera.\n2. Frequento questa scuola ___ un anno.\n3. Telefono ___ mie amiche.\n4. Vengo ___ Italia ___ treno.\n5. Vengo ___ Italia ___ macchina ___ mia sorella.\n6. Daniele lavora ___ una fabbrica e suo padre ___ una banca.\n7. Lavoro ___ una pasticceria ___ centro.\n8. Tengo i biglietti ___ taschino ___ giacca.\n9. Metto la chiave ___ tasca interna ___ impermeabile.\n10. Mangio spesso ___ ristorante.\n11. Mangio raramente ___ ristorante ___ fronte ___ casa mia.\n12. Il cappotto ___ professore è ___ sedia.\n13. Scrivo ___ mio padre e ___ miei fratelli.\n14. Tengo i libri ___ una cartella ___ plastica.\n15. Non porto mai gli occhiali ___ sole.\n16. ___ estate fa molto caldo ___ questa città.",
        "resposta": "1. a casa / alle / di sera\n2. da un anno\n3. alle mie amiche\n4. in Italia / in treno\n5. in Italia / in macchina / con mia sorella\n6. in una fabbrica / in una banca\n7. in una pasticceria / in centro\n8. nel taschino / della giacca\n9. nella tasca interna / dell'impermeabile\n10. al ristorante\n11. al ristorante / di fronte / a casa mia\n12. del professore / sulla sedia\n13. a mio padre / ai miei fratelli\n14. in una cartella / di plastica\n15. da sole (occhiali da sole)\n16. In estate / in questa città",
        "explicacao": "In estate/inverno/primavera/autunno (senza articolo). Di sera/di mattina/di notte. Frequentare da X (durata). Occhiali DA sole (scopo). Di fronte A (davanti a)."
    },

    # ── Esercizio 6 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 6** — Come il precedente:\n\n1. Scrivo ___ amici che vivono ___ Spagna.\n2. Spedisco dei fiori ___ amiche che vivono ___ Germania.\n3. Telefono ___ studente svizzero che vive ___ Hotel Excelsior.\n4. ___ mio appartamento ci sono quattro stanze.\n5. Gloria regala ___ suo marito un orologio ___ oro.\n6. Preparo una sorpresa ___ Carlo.\n7. Sono qui ___ due ore.\n8. Il negozio ___ fronte ___ scuola vende borse.\n9. Il dizionario ___ Paolo è ___ scrivania.\n10. Vengo ___ scuola ___ la bicicletta ___ Francesco.\n11. Faccio colazione ___ bar vicino ___ duomo.\n12. Seguo un corso ___ lingua italiana.",
        "resposta": "1. agli amici / in Spagna\n2. alle amiche / in Germania\n3. allo studente svizzero / all'Hotel Excelsior\n4. Nel mio appartamento\n5. a suo marito / d'oro (di+oro)\n6. per Carlo\n7. da due ore\n8. di fronte / alla scuola\n9. di Paolo / sulla scrivania\n10. a scuola / con la bicicletta / di Francesco\n11. al bar / al duomo\n12. di lingua italiana",
        "explicacao": "In Spagna/Germania (nazioni senza articolo). All'Hotel (maschile con vocale). D'oro = di oro (elisione). Di fronte ALLA (prep. articolata). Da due ore (durata continua)."
    },

    # ── Esercizio 7 — Completare ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 7** — Completare con le preposizioni:\n\n1. Studio l'italiano ___ parlare ___ gli amici.\n2. Scrivo spesso ___ miei genitori e ___ miei amici.\n3. ___ casa ___ professore ci sono molti quadri.\n4. Milano è ___ Lombardia.\n5. Mia sorella va ___ ufficio ___ motorino.\n6. Vado ___ Roma ___ macchina.\n7. Vado ___ cinema ___ piedi.\n8. Molti studenti vengono ___ Svizzera e ___ Germania.\n9. Esco ___ Giorgio ___ tre settimane.\n10. Abito ___ Carlo ___ due anni.\n11. La capitale ___ Italia è Roma.\n12. Stasera vado ___ cena ___ Luisa.",
        "resposta": "1. per parlare / con gli amici\n2. ai miei genitori / ai miei amici\n3. A casa del professore\n4. in Lombardia\n5. in ufficio / in motorino\n6. a Roma / in macchina\n7. al cinema / a piedi\n8. dalla Svizzera / dalla Germania\n9. con Giorgio / da tre settimane\n10. con Carlo / da due anni\n11. dell'Italia\n12. a cena / da Luisa",
        "explicacao": "Per + infinito (scopo). A casa DI/DEL (possesso). In Lombardia (regione). Da + nazione con articolo = DALLA Svizzera. Da tre settimane/anni = durata. Da Luisa = a casa di Luisa."
    },

    # ── Esercizio 8 — I contrari ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 8** — Rispondere secondo il modello.\nMod.: *Luigi (alto — basso): È alto Luigi? No, Luigi non è alto, ma basso.*\n\n1. I pantaloni (lungo — corto)\n2. La strada (largo — stretto)\n3. Il caffè (caldo — freddo)\n4. Il vestito (chiaro — scuro)\n5. Lo studente (attento — distratto)\n6. Il libro (interessante — noioso)\n7. Il ristorante (caro — a buon mercato)\n8. L'esercizio (facile — difficile)\n9. La spiegazione (semplice — complicata)\n10. Il miele (amaro — dolce)",
        "resposta": "1. Sono lunghi i pantaloni? No, i pantaloni non sono lunghi, ma corti.\n2. È larga la strada? No, la strada non è larga, ma stretta.\n3. È caldo il caffè? No, il caffè non è caldo, ma freddo.\n4. È chiaro il vestito? No, il vestito non è chiaro, ma scuro.\n5. È attento lo studente? No, lo studente non è attento, ma distratto.\n6. È interessante il libro? No, il libro non è interessante, ma noioso.\n7. È caro il ristorante? No, il ristorante non è caro, ma a buon mercato.\n8. È facile l'esercizio? No, l'esercizio non è facile, ma difficile.\n9. È semplice la spiegazione? No, la spiegazione non è semplice, ma complicata.\n10. È amaro il miele? No, il miele non è amaro, ma dolce.",
        "explicacao": "L'aggettivo concorda con il sostantivo: lungo→lunga→lunghi→lunghe; largo→larga; chiaro→chiara; complicato→complicata. A buon mercato = economico (espressione fissa)."
    },

    # ── Esercizio 9 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 9** — Come il precedente:\n\n1. La canzone (allegro — triste)\n2. Il ragazzo (simpatico — antipatico)\n3. Il film (divertente — noioso)\n4. La bistecca (duro — tenero)\n5. Il turista (straniero — italiano)\n6. L'autobus (veloce — lento)\n7. La scultura (moderno — antico)\n8. Il vino (buono — cattivo)\n9. L'asciugamano (asciutto — bagnato)\n10. Il latte (freddo — caldo)",
        "resposta": "1. È allegra la canzone? No, la canzone non è allegra, ma triste.\n2. È simpatico il ragazzo? No, il ragazzo non è simpatico, ma antipatico.\n3. È divertente il film? No, il film non è divertente, ma noioso.\n4. È dura la bistecca? No, la bistecca non è dura, ma tenera.\n5. È straniero il turista? No, il turista non è straniero, ma italiano.\n6. È veloce l'autobus? No, l'autobus non è veloce, ma lento.\n7. È moderna la scultura? No, la scultura non è moderna, ma antica.\n8. È buono il vino? No, il vino non è buono, ma cattivo.\n9. È asciutto l'asciugamano? No, l'asciugamano non è asciutto, ma bagnato.\n10. È freddo il latte? No, il latte non è freddo, ma caldo.",
        "explicacao": "Accordo aggettivo: allegra (f.), dura (f.), moderna (f.), antica (f.), asciutto (m.), bagnato (m.). Aggettivi in -e (triste, veloce, lente) sono invariabili nel genere."
    },

    # ── Esercizio 10 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 10** — Come il precedente:\nMod.: *Peter (tedesco — austriaco): È tedesco Peter? No, Peter non è tedesco, ma austriaco.*\n\n1. Il clima di Firenze (secco — umido)\n2. Il cielo (sereno — nuvoloso)\n3. Il ragazzo (biondo — moro)\n4. Il giovane (forte — debole)\n5. Il cane (malato — sano)\n6. La commessa (gentile — scortese)\n7. La camera (sporco — pulito)\n8. La città (tranquillo — rumoroso)\n9. Il palazzo (grande — piccolo)\n10. Il posto (libero — occupato)",
        "resposta": "1. È secco il clima di Firenze? No, il clima di Firenze non è secco, ma umido.\n2. È sereno il cielo? No, il cielo non è sereno, ma nuvoloso.\n3. È biondo il ragazzo? No, il ragazzo non è biondo, ma moro.\n4. È forte il giovane? No, il giovane non è forte, ma debole.\n5. È malato il cane? No, il cane non è malato, ma sano.\n6. È gentile la commessa? No, la commessa non è gentile, ma scortese.\n7. È sporca la camera? No, la camera non è sporca, ma pulita.\n8. È tranquilla la città? No, la città non è tranquilla, ma rumorosa.\n9. È grande il palazzo? No, il palazzo non è grande, ma piccolo.\n10. È libero il posto? No, il posto non è libero, ma occupato.",
        "explicacao": "L'aggettivo concorda: sporco→sporca (femm.), tranquillo→tranquilla, rumoroso→rumorosa. Moro = di carnagione scura (capelli scuri). Scortese: aggettivo in -e, stessa forma m./f."
    },

    # ── Esercizio 11 — Come il precedente ──
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio 11** — Come il precedente:\n\n1. Il padre di Anna (ricco — povero)\n2. La donna (generoso — avaro)\n3. La persona (sicuro — insicuro)\n4. La coppia (felice — infelice)\n5. La storia (allegro — triste)\n6. La bottiglia (pieno — vuoto)\n7. La valigia (leggero — pesante)\n8. La notizia (vero — falso)\n9. Il ragazzo (bugiardo — sincero)\n10. Il museo (aperto — chiuso)",
        "resposta": "1. È ricco il padre di Anna? No, il padre di Anna non è ricco, ma povero.\n2. È generosa la donna? No, la donna non è generosa, ma avara.\n3. È sicura la persona? No, la persona non è sicura, ma insicura.\n4. È felice la coppia? No, la coppia non è felice, ma infelice.\n5. È allegra la storia? No, la storia non è allegra, ma triste.\n6. È piena la bottiglia? No, la bottiglia non è piena, ma vuota.\n7. È leggera la valigia? No, la valigia non è leggera, ma pesante.\n8. È vera la notizia? No, la notizia non è vera, ma falsa.\n9. È bugiardo il ragazzo? No, il ragazzo non è bugiardo, ma sincero.\n10. È aperto il museo? No, il museo non è aperto, ma chiuso.",
        "explicacao": "Aggettivi in -o/-a: generoso→generosa, pieno→piena, leggero→leggera, vero→vera, falso→falsa. Infelice: aggettivo in -e, stessa forma m./f. Bugiardo: chi dice bugie."
    },

    # ── Lavorare sul testo — «La giornata di uno studente» ──
    {
        "tipo": "revelar",
        "pergunta": "**Lavorare sul testo — «La giornata di uno studente»**\n\nOgni giorno Guido fa colazione alle otto: mangia una fetta di pane con burro e marmellata e beve un cappuccino. Alle otto e trenta esce di casa e va alla fermata dell'autobus per andare in città. L'autobus passa dopo pochi minuti e Guido arriva all'università verso le nove meno dieci. Le lezioni cominciano alle nove e finiscono all'una. All'ora di pranzo Guido va con un suo compagno in pizzeria o al bar per fare uno spuntino. Nel primo pomeriggio torna a casa per riposarsi e per studiare. Verso le otto cena e poi esce per incontrare gli amici. Di solito va al cinema o in centro per fare una passeggiata e per guardare le vetrine dei negozi, ma ogni tanto va anche in discoteca. Infine, a mezzanotte, Guido torna a casa: legge qualche pagina di un libro e poi va a dormire.\n\n**a) Trascrivere alla terza persona plurale:**\nMod.: Ogni giorno Guido e Paolo...\n\n**b) Scrivere una frase con:**\n1. fare colazione\n2. fermata\n3. di solito\n4. nel primo pomeriggio\n5. pranzo / pranzare\n6. cena / cenare\n7. fare una passeggiata\n8. qualche",
        "resposta": "**a)** Ogni giorno Guido e Paolo fanno colazione alle otto: mangiano una fetta di pane con burro e marmellata e bevono un cappuccino. Alle otto e trenta escono di casa e vanno alla fermata dell'autobus per andare in città. L'autobus passa dopo pochi minuti e Guido e Paolo arrivano all'università verso le nove meno dieci. Le lezioni cominciano alle nove e finiscono all'una. All'ora di pranzo vanno con i loro compagni in pizzeria o al bar per fare uno spuntino. Nel primo pomeriggio tornano a casa per riposarsi e per studiare. Verso le otto cenano e poi escono per incontrare gli amici. Di solito vanno al cinema o in centro per fare una passeggiata. Infine, a mezzanotte, tornano a casa: leggono qualche pagina di un libro e poi vanno a dormire.\n\n**b)** Esempi:\n1. Ogni mattina faccio colazione alle sette.\n2. Aspetto l'autobus alla fermata.\n3. Di solito pranzo a casa.\n4. Nel primo pomeriggio mi riposo.\n5. Il pranzo è il pasto principale in Italia. / Pranzo a mezzogiorno.\n6. La cena è alle otto di sera. / Ceniamo alle otto.\n7. La domenica faccio una passeggiata nel parco.\n8. Leggo qualche pagina ogni sera.",
        "explicacao": "Terza persona plurale: fa→fanno, esce→escono, va→vanno, arriva→arrivano, comincia→cominciano, torna→tornano, cena→cenano, legge→leggono."
    },

    # ══════════════════════════════════════════════════════════
    #  ESERCIZI DI VERIFICA  (20 domande)
    # ══════════════════════════════════════════════════════════

    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Il vestito è ___",
        "opcoes": [
            "in l'armadio.",
            "nell'armadio.",
            "in il armadio."
        ],
        "resposta": 1,
        "explicacao": "in + l' = **nell'**. Davanti a vocale: nell'armadio, nell'ufficio, nell'ospedale."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Telefono ___",
        "opcoes": [
            "al zio.",
            "a lo zio.",
            "allo zio."
        ],
        "resposta": 2,
        "explicacao": "Zio inizia con z → articolo LO → a + lo = **ALLO**. Telefono allo zio."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — La porta ___ è chiusa.",
        "opcoes": [
            "di l'ufficio",
            "dell'ufficio",
            "de l'ufficio"
        ],
        "resposta": 1,
        "explicacao": "di + l' = **dell'**. La porta dell'ufficio (ufficio inizia con vocale → l')."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Lo sciopero ___ è finito.",
        "opcoes": [
            "di treni",
            "delli treni",
            "dei treni"
        ],
        "resposta": 2,
        "explicacao": "di + i = **DEI**. Lo sciopero dei treni. 'Delli' non esiste in italiano."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Preferisco il caffè ___",
        "opcoes": [
            "al tè.",
            "allo tè.",
            "a il tè."
        ],
        "resposta": 0,
        "explicacao": "a + il = **AL**. Preferisco il caffè al tè. Tè inizia con consonante → il tè → al tè."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Questa cartolina viene ___",
        "opcoes": [
            "dal Giappone.",
            "da il Giappone.",
            "del Giappone."
        ],
        "resposta": 0,
        "explicacao": "da + il = **DAL**. La cartolina viene dal Giappone (provenienza). 'Del' è di+il (possesso)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Il gatto dorme ___",
        "opcoes": [
            "sullo letto.",
            "sul letto.",
            "su letto."
        ],
        "resposta": 1,
        "explicacao": "su + il = **SUL**. Il gatto dorme sul letto. 'Sullo' si usa con lo (sullo zaino). La preposizione non si usa da sola senza articolo."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Il professore spiega la lettera ___",
        "opcoes": [
            "agli studenti.",
            "a gli studenti.",
            "ai studenti."
        ],
        "resposta": 0,
        "explicacao": "a + gli = **AGLI**. Studenti inizia con st (s+consonante) → gli studenti → agli studenti. 'A gli' non si scrive separato."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Mario parla ___",
        "opcoes": [
            "coi amici.",
            "con gli amici.",
            "con gl'amici."
        ],
        "resposta": 1,
        "explicacao": "Con gli amici: 'con' generalmente non forma contrazioni obbligatorie. 'Coi' (con+i) è raro e letterario. 'Gl'' non esiste come elisione di 'gli'."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — C'è una lettera ___",
        "opcoes": [
            "per il mamma.",
            "pella mamma.",
            "per la mamma."
        ],
        "resposta": 2,
        "explicacao": "Per non si contrae con l'articolo. Mamma è femminile → la mamma → **per la mamma**. 'Pella' non esiste."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Torno ___",
        "opcoes": [
            "a casa alle sette.",
            "alla mia casa alle sette.",
            "alla casa alle sette."
        ],
        "resposta": 0,
        "explicacao": "'Tornare **a casa**' è un'espressione fissa senza articolo. Con il possessivo: torno a casa mia (non alla mia casa)."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Il treno arriva ___",
        "opcoes": [
            "in tre minuti.",
            "fra tre minuti.",
            "a tre minuti."
        ],
        "resposta": 1,
        "explicacao": "**Fra / tra** esprimono il tempo che intercorre fino a un evento futuro: il treno arriva fra tre minuti."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Abito ___",
        "opcoes": [
            "su via Faenza.",
            "in via Faenza.",
            "per via Faenza."
        ],
        "resposta": 1,
        "explicacao": "Per indicare la via/strada dove si abita si usa **IN**: abito in via Faenza / in piazza Navona."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Studio ___",
        "opcoes": [
            "a Firenze in Italia.",
            "in Firenze in Italia.",
            "in Firenze nell'Italia."
        ],
        "resposta": 0,
        "explicacao": "Città → **A** (a Firenze). Nazione senza articolo → **IN** (in Italia). Non si dice 'in Firenze' né 'nell'Italia'."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Andiamo ___",
        "opcoes": [
            "alla discoteca.",
            "in discoteca.",
            "per la discoteca."
        ],
        "resposta": 1,
        "explicacao": "Andare **IN discoteca** è l'espressione fissa. Come: in palestra, in piscina, in biblioteca, in pizzeria."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Stasera ceno ___",
        "opcoes": [
            "a Carlo.",
            "da Carlo.",
            "al Carlo."
        ],
        "resposta": 1,
        "explicacao": "**DA** + persona = a casa di quella persona: ceno da Carlo = ceno a casa di Carlo. Come: vado dal dottore, sono da Giulia."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Vai ___?",
        "opcoes": [
            "dal dottore",
            "al dottore",
            "per il dottore"
        ],
        "resposta": 0,
        "explicacao": "**DA** + professionista: vado dal dottore, dal dentista, dal meccanico. da + il = **DAL**."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Gli studenti vanno ___",
        "opcoes": [
            "a studiare in biblioteca.",
            "per studiare in biblioteca.",
            "studiare in biblioteca."
        ],
        "resposta": 0,
        "explicacao": "Andare **A** + infinito esprime lo scopo: vanno a studiare, vado a comprare, esco a fare una passeggiata."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Vengo a scuola ___",
        "opcoes": [
            "sull'autobus.",
            "con l'autobus.",
            "nell'autobus."
        ],
        "resposta": 1,
        "explicacao": "Il mezzo di trasporto si esprime con **CON** (con l'autobus, con il treno) o con **IN** (in autobus, in treno). Mai con SU o NEL."
    },
    {
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Quella ragazza è ___",
        "opcoes": [
            "da Roma.",
            "in Roma.",
            "di Roma."
        ],
        "resposta": 2,
        "explicacao": "La provenienza/origine si esprime con **DI**: è di Roma, sono di Milano. 'Da Roma' indica partenza: vengo da Roma."
    },

    # ══════════════════════════════════════════════════════════
    #  TROVARE GLI ERRORI  (10 domande)
    # ══════════════════════════════════════════════════════════

    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Gli occhiali per il sole sono sul tavolo.»",
        "resposta": "Gli occhiali da sole sono sul tavolo.",
        "explicacao": "'Occhiali **da** sole' è un'espressione fissa con DA (scopo/uso). Non si dice 'per il sole'."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Vado al tabaccaio a comprare le sigarette.»",
        "resposta": "Vado dal tabaccaio a comprare le sigarette.",
        "explicacao": "Quando si va da una persona o professionista si usa **DA**: dal medico, dal dentista, **dal tabaccaio**. 'Al tabaccaio' indica il negozio (tabaccheria)."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Vive in Friburgo a Germania.»",
        "resposta": "Vive a Friburgo in Germania.",
        "explicacao": "Città → **A** (a Friburgo). Nazione → **IN** (in Germania). L'ordine corretto è: città, poi nazione."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Quando cominci di studiare all'università?»",
        "resposta": "Quando cominci a studiare all'università?",
        "explicacao": "Cominciare / iniziare si costruisce con **A** + infinito: comincio A studiare, inizio A lavorare. Non con 'di'."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Usciamo con la macchina o andiamo su piedi?»",
        "resposta": "Usciamo con la macchina o andiamo a piedi?",
        "explicacao": "'**A piedi**' è l'unico mezzo di trasporto che usa A (non SU o CON). Tutte le altre eccezioni usano IN o CON."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Telefono con la mia amica.»",
        "resposta": "Telefono alla mia amica.",
        "explicacao": "Telefonare vuole la preposizione **A**: telefono a Luisa / **alla** mia amica. Non si usa 'con'."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Il ritardo del treno dipende sullo sciopero.»",
        "resposta": "Il ritardo del treno dipende dallo sciopero.",
        "explicacao": "Dipendere vuole **DA**: dipende da te / **dallo** sciopero / dalle condizioni. da + lo = DALLO."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Sono sposato per pochi mesi.»",
        "resposta": "Sono sposato da pochi mesi.",
        "explicacao": "La durata di un'azione che continua nel presente si esprime con **DA**: sono sposato da pochi mesi / vivo qui da due anni."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Saluto a Carlo.»",
        "resposta": "Saluto Carlo.",
        "explicacao": "Salutare è un verbo transitivo diretto: non vuole preposizione. Saluto Carlo (non 'a Carlo'). Come: chiamo Marco, aspetto Laura."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Trovare l'errore** — Correggere la frase:\n«Nell'inverno non fa molto freddo in Firenze.»",
        "resposta": "In inverno non fa molto freddo a Firenze.",
        "explicacao": "Le stagioni con IN non vogliono articolo: **in inverno**, in estate, in primavera, in autunno. Città → **A**: a Firenze (non 'in Firenze')."
    },
]

exemplos = [
    {"it": "Vado a Roma in treno. Vivo in Italia da due anni.", "pt": "Vou a Roma de trem. Vivo na Itália há dois anos."},
    {"it": "Il libro è sul tavolo. Metto i soldi nel portafoglio.", "pt": "O livro está sobre a mesa. Coloco o dinheiro na carteira."},
    {"it": "Vado dal dottore. Ceno da Giulia stasera.", "pt": "Vou ao médico. Janto na casa da Giulia esta noite."},
    {"it": "Telefono alla mia amica. Do il diploma agli studenti.", "pt": "Ligo para minha amiga. Dou o diploma aos estudantes."},
    {"it": "Mario va sempre a scuola a piedi. Non prendo mai il caffè la sera.", "pt": "Mario sempre vai à escola a pé. Nunca tomo café à noite."},
]

lez3 = {
    "id": "a1-lez3",
    "num": "Lezione III",
    "titulo": "Le preposizioni semplici e articolate",
    "subtitulo": "Di, a, da, in, con, su, per, fra",
    "teoria": teoria,
    "exemplos": exemplos,
    "exercicios": exercicios
}

data['moduli'][0]['unidades'][2] = lez3

with open(r'grammar.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

u = data['moduli'][0]['unidades'][2]
escolha = sum(1 for e in u['exercicios'] if e['tipo'] == 'escolha')
revelar = sum(1 for e in u['exercicios'] if e['tipo'] == 'revelar')
print(f"OK: {u['num']} - {u['titulo']}")
print(f"Teoria: {len(u['teoria'])} chars")
print(f"Exemplos: {len(u['exemplos'])}")
print(f"Exercicios: {len(u['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
print(f"  - Esercizi 1-11 + conv. + vocab. + lettura: {revelar - 10} revelar")
print(f"  - Esercizi di verifica: {escolha} escolha")
print(f"  - Trovare gli errori: 10 revelar")
