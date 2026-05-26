import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione V")

lez["titulo"] = "La particella \"ci\""
lez["subtitulo"] = "Uso della particella 'ci' come avverbio di luogo"

lez["teoria"] = """\
## Un invito

**Mario:** Senti Laura, dopodomani è il compleanno di Guido e con alcuni amici voglio organizzare una festa nella casa di campagna di mio fratello. Ci vuoi venire anche tu?
**Laura:** Grazie Mario, sei molto gentile, ma ho paura di non poterci venire: la mia macchina è rotta, è dal meccanico.
**Mario:** Ma non è affatto un problema! Mia sorella e il suo ragazzo hanno deciso di venirci e sono in macchina, così, se a te va bene, potete fare il viaggio insieme.
**Laura:** D'accordo Mario! Accetto con piacere l'invito. Stasera telefono a tua sorella per fissare un appuntamento. Quante persone ci sono alla festa?
**Mario:** Tante! La casa è molto spaziosa, così abbiamo invitato molti amici: se vengono tutti gli invitati siamo sessanta, ma forse anche di più.
**Laura:** Che bello! Va bene se porto con me un amico?
**Mario:** Ma certo, Laura!
**Laura:** Grazie Mario! Allora ci vediamo sabato.
**Mario:** D'accordo, ciao.

---

## A L'uso della particella "ci"

La particella **ci** sostituisce un'espressione di luogo (a Roma, in centro, da Carlo, qui, lì...).

| senza "ci" | con "ci" |
|---|---|
| Carlo e Paolo non vanno a Roma domani. | Carlo e Paolo **non ci vanno** domani. |
| Quanto tempo rimani a Firenze? | Quanto tempo **ci rimani**? |
| Veniamo in centro a piedi. | **Ci veniamo** a piedi. |
| Restate a casa anche oggi? | **Ci restate** anche oggi? |
| Passo da te verso le sette. | **Ci passo** verso le sette. |
| Sei qui da molto tempo? | **Ci sei** da molto tempo? |
| Luisa sta volentieri in questa città. | Luisa **ci sta** volentieri. |

> **NON + CI + VERBO**

Con i verbi modali, **ci** può stare prima o dopo:

- A che ora devi andare dal medico? → **Ci devo andare** alle cinque. / **Devo andarci** alle cinque.
- Puoi venire a casa mia stasera? → Sì, **ci posso venire**. / Sì, **posso venirci**.
- Volete rimanere ancora qui? → No, **non ci vogliamo rimanere**. / No, **non vogliamo rimanerci**.

---

## B L'uso del partitivo: di + articolo, alcuni/e, qualche

| | esempio |
|---|---|
| **di + articolo** | Giovanna ha comprato **dei** fiori. |
| **alcuni/alcune** | Giovanna ha comprato **alcuni** fiori. |
| **qualche** (+ singolare) | Giovanna ha comprato **qualche** fiore. |

> **Qualche** è invariabile e vuole sempre il nome al **singolare**.
> Alcuni/alcune concordano in genere e numero con il nome.

Esempi:
- Paolo ha scritto **delle** cartoline / **alcune** cartoline / **qualche** cartolina a casa.
- **Degli** studenti hanno fatto un buon esame. / **Alcuni** studenti... / **Qualche** studente...

---

## C Vocabolario sistematico — La casa

**Parti esterne della casa:**
la facciata · il tetto · il camino (comignolo) · il portone · la finestra · il davanzale · il balcone · la persiana · la grondaia · il garage (la rimessa) · il primo piano · il pianterreno (piano terra)

**Le stanze:**
l'ingresso · il soggiorno · la sala da pranzo · lo studio · la camera da letto · il ripostiglio · il guardaroba · il bagno
"""

lez["exemplos"] = [
    "Sei stato a Roma? Sì, ci sono stato la settimana scorsa.",
    "Quando vai in piscina? Ci vado domani mattina.",
    "Quanto tempo rimani a Venezia? Ci rimango tre giorni.",
    "Mario ha invitato qualche amico alla festa.",
    "Ci sono delle parole che non conosco.",
]

exercicios = []

# ── Domande sul dialogo ──────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Rispondere alle domande sul dialogo 'Un invito':",
    "pergunta": (
        "1. Quando è il compleanno di Guido?\n"
        "2. Che cosa vuole organizzare Mario?\n"
        "3. Dove?\n"
        "4. Chi invita?\n"
        "5. Perché Laura ha paura di non poterci andare?\n"
        "6. Con chi ci può andare?\n"
        "7. Perché telefona alla sorella di Mario?\n"
        "8. Quante persone ci sono alla festa?"
    ),
    "resposta": (
        "1. Dopodomani.\n"
        "2. Una festa.\n"
        "3. Nella casa di campagna di suo fratello.\n"
        "4. Laura e molti altri amici.\n"
        "5. Perché la sua macchina è rotta, è dal meccanico.\n"
        "6. Con la sorella di Mario e il suo ragazzo.\n"
        "7. Per fissare un appuntamento per il viaggio.\n"
        "8. Sessanta, forse anche di più."
    )
})

# ── Esercizio 1 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1 — Completare con la particella 'ci':",
    "pergunta": (
        "1. Vai a scuola? Sì, ___\n"
        "2. Siete stati a Venezia? No, non ___\n"
        "3. Venite da Carlo? Sì, ___\n"
        "4. Da quanto tempo abiti in questa casa? ___ da un anno.\n"
        "5. Signora, vive in questa città? Sì, ___ da molti anni.\n"
        "6. Con chi vai a teatro? ___ con Anna.\n"
        "7. Quando sei andata a Parigi? ___ il mese scorso.\n"
        "8. Perché vai a Roma? ___ per vedere la Cappella Sistina.\n"
        "9. Vieni al cinema con noi? No, non ___\n"
        "10. Quando vieni a Pisa? ___ sabato prossimo.\n"
        "11. Paolo, quanti giorni rimani a Firenze? ___ una settimana.\n"
        "12. Sei stato a Londra? Sì, ___"
    ),
    "resposta": (
        "1. Sì, ci vado.\n"
        "2. No, non ci siamo stati.\n"
        "3. Sì, ci veniamo.\n"
        "4. Ci abito da un anno.\n"
        "5. Sì, ci vivo da molti anni.\n"
        "6. Ci vado con Anna.\n"
        "7. Ci sono andata il mese scorso.\n"
        "8. Ci vado per vedere la Cappella Sistina.\n"
        "9. No, non ci vengo.\n"
        "10. Ci vengo sabato prossimo.\n"
        "11. Ci rimango una settimana.\n"
        "12. Sì, ci sono stato."
    )
})

# ── Esercizio 2 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 2 — Come il precedente (completare con 'ci'):",
    "pergunta": (
        "1. Come vai a casa? Di solito ___ con l'autobus.\n"
        "2. Noi andiamo a vedere il Duomo, perché non ___ anche tu?\n"
        "3. Chi resta con Luca? ___ noi.\n"
        "4. Siete andati in campagna? Sì, ___\n"
        "5. Venite anche voi alla gita? No, ___\n"
        "6. Abiti volentieri da quella famiglia? Sì, ___ volentieri.\n"
        "7. Quando ritorna in America? ___ fra tre mesi.\n"
        "8. Chi viene con te al circo? ___ Paolo e Marta.\n"
        "9. Con chi vai al mare quest'anno? ___ con i miei zii.\n"
        "10. Chi porti a Pisa con te? ___ mia figlia.\n"
        "11. Da quanto tempo non abiti più là? Non ___ da quasi due anni.\n"
        "12. A che ora sono andati al ristorante? ___ alle due."
    ),
    "resposta": (
        "1. Di solito ci vado con l'autobus.\n"
        "2. Perché non ci vieni anche tu?\n"
        "3. Ci restiamo noi.\n"
        "4. Sì, ci siamo andati.\n"
        "5. No, non ci veniamo.\n"
        "6. Sì, ci sto volentieri.\n"
        "7. Ci torno fra tre mesi.\n"
        "8. Ci vengono Paolo e Marta.\n"
        "9. Ci vado con i miei zii.\n"
        "10. Ci porto mia figlia.\n"
        "11. Non ci abito da quasi due anni.\n"
        "12. Ci sono andati alle due."
    )
})

# ── Esercizio 3 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 3 — Completare con la particella 'ci':",
    "pergunta": (
        "1. Posso andare a ballare con Giulio? Sì, ___\n"
        "2. Agli Uffizi ___ sono dei quadri meravigliosi.\n"
        "3. Quando torni a casa? ___ alle tre.\n"
        "4. Franca non è venuta con noi a vedere questo film perché è già stata ieri con Vincenzo.\n"
        "5. Vuoi rimanere da me ancora un giorno? Sì, ___ con piacere.\n"
        "6. Quando vai in ospedale? ___ domani.\n"
        "7. È mai stata a Venezia? No, ___ mai.\n"
        "8. Roma è una città caotica, ___ è molto traffico.\n"
        "9. Chi abita qui? Non ___ nessuno.\n"
        "10. Cosa c'è in quella bottiglia? Non ___ è niente.\n"
        "11. Come tornate in Inghilterra? ___ in treno.\n"
        "12. Quando puoi andare dal medico? ___ mercoledì."
    ),
    "resposta": (
        "1. Sì, ci puoi andare.\n"
        "2. Agli Uffizi ci sono dei quadri meravigliosi.\n"
        "3. Ci torno alle tre.\n"
        "4. Ci è già stata ieri con Vincenzo. (risposta)\n"
        "5. Sì, ci rimango con piacere.\n"
        "6. Ci vado domani.\n"
        "7. No, non ci sono mai stata.\n"
        "8. Ci è molto traffico.\n"
        "9. Non ci abita nessuno.\n"
        "10. Non ci è niente.\n"
        "11. Ci torniamo in treno.\n"
        "12. Ci posso andare mercoledì."
    )
})

# ── Esercizio 4 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 4 — Come il precedente (completare con 'ci'):",
    "pergunta": (
        "1. A che ora sei andato in ufficio? ___ alle nove.\n"
        "2. In quel negozio ___ sono dei bei vestiti.\n"
        "3. Vai in piscina domani? ___ solo se non piove.\n"
        "4. Perché non porti anche Nino con te? Perché non vuole venir ___\n"
        "5. Vado al supermercato. ___ con Marco?\n"
        "6. Ritorni a Francoforte? Sì, ___ presto.\n"
        "7. Venite al ristorante? No, non ___\n"
        "8. Vuoi già andare a letto? Sì, ___ subito.\n"
        "9. Signorina, torna volentieri in Italia? Sì, ___ sempre con molto piacere.\n"
        "10. Quanto tempo rimanete a Pisa? ___ una settimana.\n"
        "11. Roma è bella, voglio andar ___ con Anna.\n"
        "12. Come siete andati a San Gimignano? ___ con la macchina."
    ),
    "resposta": (
        "1. Ci sono andato alle nove.\n"
        "2. Ci sono dei bei vestiti.\n"
        "3. Ci vado solo se non piove.\n"
        "4. Perché non vuole venirci.\n"
        "5. Ci vieni con Marco?\n"
        "6. Sì, ci ritorno presto.\n"
        "7. No, non ci veniamo.\n"
        "8. Sì, ci vado subito.\n"
        "9. Sì, ci torno sempre con molto piacere.\n"
        "10. Ci rimaniamo una settimana.\n"
        "11. Voglio andarci con Anna.\n"
        "12. Ci siamo andati con la macchina."
    )
})

# ── Conversazione ─────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Conversazione — Un annuncio sul giornale / In un'agenzia immobiliare (leggere i dialoghi):",
    "pergunta": (
        "Un annuncio sul giornale:\n"
        "— Pronto, signora, buon giorno. Telefono per quell'annuncio sul giornale di oggi. Ha una camera da affittare?\n"
        "— Sì. È una camera spaziosa e ben ammobiliata in un appartamento dove vivono già due studenti, e c'è anche l'uso di cucina.\n"
        "— In che zona è?\n"
        "— In una zona silenziosa e tranquilla vicino al centro.\n"
        "— Quanto costa al mese?\n"
        "— Quattrocentomila lire, comprese tutte le spese.\n"
        "— La ringrazio, ma è troppo cara per me. ArrivederLa.\n\n"
        "In un'agenzia immobiliare:\n"
        "— Buon giorno, signorina, desidera?\n"
        "— Cerco un piccolo appartamento di due o tre stanze in una zona centrale.\n"
        "— Da acquistare o in affitto?\n"
        "— In affitto.\n"
        "— Bene, ora guardo subito se c'è qualcosa che La può interessare. Ecco, abbiamo un mini-appartamento ammobiliato nel quartiere di Santo Spirito. Le interessa?\n"
        "— Quanto è l'affitto?\n"
        "— Ottocentomila lire al mese, comprese le spese del condominio. Inoltre è necessario dare due mesi anticipati come deposito.\n"
        "— Mi sembra un po' caro, ma lo vorrei vedere, è possibile?\n"
        "— Sì, certamente."
    ),
    "resposta": "Dialogo sulla ricerca di un appartamento in affitto."
})

# ── Vocabolario sistematico + Lettura ─────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lettura — La casa dei signori Chiari (rispondere alle domande):",
    "pergunta": (
        "I signori Chiari hanno una graziosa casetta in campagna. La casa è a un piano ed è "
        "circondata da un giardino con alcuni alberi. Il giardino è piuttosto grande ed è "
        "recintato da un muro alto circa due metri. Il tetto della casa è rosso e la facciata "
        "è gialla. Sul davanti, al piano-terra, c'è il portone d'entrata con a destra e a "
        "sinistra due finestre. Al primo piano ci sono tre finestre e quella centrale ha un "
        "balcone. Tutte le finestre hanno le persiane verdi che servono a proteggere la casa "
        "dal sole e a ripararla dalla pioggia. Sui davanzali delle finestre ci sono alcuni "
        "vasi di fiori che danno alla casa un aspetto vivace e allegro.\n\n"
        "1. Com'è la casa dei signori Chiari?\n"
        "2. Quanti piani ha?\n"
        "3. Dov'è il giardino?\n"
        "4. Che cosa c'è intorno al giardino?\n"
        "5. Di che colore è il tetto?\n"
        "6. Di che colore è la facciata?\n"
        "7. Quante finestre ci sono sul davanti?\n"
        "8. Quanti balconi?\n"
        "9. Che cosa hanno le finestre?\n"
        "10. A che cosa servono le persiane?\n"
        "11. Che cosa c'è sui davanzali?\n"
        "12. Che aspetto ha la casa?"
    ),
    "resposta": (
        "1. È una graziosa casetta in campagna.\n"
        "2. Ha un piano.\n"
        "3. Intorno alla casa.\n"
        "4. Un muro alto circa due metri.\n"
        "5. Rosso.\n"
        "6. Gialla.\n"
        "7. Tre in tutto sul davanti (due al piano-terra + tre al primo piano).\n"
        "8. Un balcone.\n"
        "9. Le persiane verdi.\n"
        "10. A proteggere dal sole e a ripararla dalla pioggia.\n"
        "11. Vasi di fiori.\n"
        "12. Vivace e allegro."
    )
})

# ── Esercizio 5 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 5 — Completare con la particella 'ci':",
    "pergunta": (
        "1. Venite anche voi alla festa della scuola? Sì, ___ volentieri.\n"
        "2. Quanto tempo rimangono in Italia? ___ tre mesi.\n"
        "3. Chi va a Roma al concerto di Pavarotti? ___ tutti.\n"
        "4. Quando torni a Berlino? ___ il prossimo mese.\n"
        "5. Quanto tempo hai vissuto a Verona? ___ un anno.\n"
        "6. Siete stati a teatro ieri sera? No, ___\n"
        "7. Dottore, vai in ospedale? No, ___\n"
        "8. Chi viene con me a teatro? ___ tutti.\n"
        "9. Sono stati allo zoo i tuoi bambini? No, ___\n"
        "10. Vai spesso al cinema? Sì, ___ abbastanza spesso.\n"
        "11. Andiamo anche noi in montagna la prossima settimana? No, ___\n"
        "12. Luisa, rimani a letto stamattina? Sì, ___ fino a mezzogiorno."
    ),
    "resposta": (
        "1. Sì, ci veniamo volentieri.\n"
        "2. Ci rimangono tre mesi.\n"
        "3. Ci vanno tutti.\n"
        "4. Ci torno il prossimo mese.\n"
        "5. Ci ho vissuto un anno.\n"
        "6. No, non ci siamo stati.\n"
        "7. No, non ci vado.\n"
        "8. Ci vengono tutti.\n"
        "9. No, non ci sono stati.\n"
        "10. Sì, ci vado abbastanza spesso.\n"
        "11. No, non ci andiamo.\n"
        "12. Sì, ci rimango fino a mezzogiorno."
    )
})

# ── Esercizio 6 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 6 — Come il precedente (completare con 'ci'):",
    "pergunta": (
        "1. Susan, vieni a scuola domani? No, ___ perché arrivano i miei genitori.\n"
        "2. Chi è andato a comprare i biglietti per l'autobus? ___ Paolo e Caterina.\n"
        "3. Vieni anche tu in discoteca domani sera? Sì, anch'io ___ .\n"
        "4. Come tornate a casa stasera? ___ in taxi.\n"
        "5. Professore, è andato a ritirare quel libro? Sì, ___ stamattina.\n"
        "6. Quanto tempo sei stato in India? ___ due mesi.\n"
        "7. Rimanete a pranzo con noi oggi? No, ___ perché dobbiamo tornare a casa.\n"
        "8. Signora, va spesso a fare la spesa al mercato? Sì, ___ quasi tutti i giorni.\n"
        "9. Stai bene in Italia? Sì, ___ molto bene.\n"
        "10. Chi va a scuola domani? Non ___ nessuno.\n"
        "11. Perché torni nel tuo Paese? ___ perché ho nostalgia.\n"
        "12. Come andate a Genova? ___ con la macchina di Mario."
    ),
    "resposta": (
        "1. Non ci vado perché arrivano i miei genitori.\n"
        "2. Ci sono andati Paolo e Caterina.\n"
        "3. Sì, anch'io ci vengo.\n"
        "4. Ci torniamo in taxi.\n"
        "5. Sì, ci sono andato stamattina.\n"
        "6. Ci sono stato due mesi.\n"
        "7. No, non ci rimaniamo perché dobbiamo tornare a casa.\n"
        "8. Sì, ci vado quasi tutti i giorni.\n"
        "9. Sì, ci sto molto bene.\n"
        "10. Non ci va nessuno.\n"
        "11. Ci torno perché ho nostalgia.\n"
        "12. Ci andiamo con la macchina di Mario."
    )
})

# ── Lavorare sul testo ────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lavorare sul testo — 'Una casa in città' (rispondere alle domande):",
    "pergunta": (
        "I signori Allegri abitano da alcuni anni in un quartiere popolare della città. La loro "
        "casa è in una piazza molto frequentata, soprattutto la mattina, quando c'è il mercato. "
        "L'appartamento è spazioso ed è disposto su due piani: al primo, dopo l'ingresso, c'è "
        "un breve corridoio con a destra la sala da pranzo e la cucina; a sinistra il soggiorno, "
        "lo studio e un piccolo bagno. In fondo al corridoio c'è una scala che porta al secondo "
        "piano, dove ci sono due camere da letto, una matrimoniale e una per gli ospiti, il "
        "guardaroba e il bagno. Le stanze della casa con le finestre che danno sulla piazza sono "
        "luminose, ma durante il giorno c'è un po' di rumore; quelle con le finestre che danno "
        "sul giardino, invece, sono silenziose e fresche d'estate. La casa dei signori Allegri "
        "è comoda e accogliente, e i loro amici ci vanno volentieri.\n\n"
        "1. Dove abitano i signori Allegri?\n"
        "2. Da quanto tempo?\n"
        "3. Dov'è la loro casa?\n"
        "4. Com'è il loro appartamento?\n"
        "5. Quali stanze ci sono al primo piano?\n"
        "6. E al secondo?\n"
        "7. Come sono le stanze sul davanti e quelle sul retro?\n"
        "8. Com'è la casa dei signori Allegri?"
    ),
    "resposta": (
        "1. In un quartiere popolare della città.\n"
        "2. Da alcuni anni.\n"
        "3. In una piazza molto frequentata.\n"
        "4. È spazioso e disposto su due piani.\n"
        "5. L'ingresso, il corridoio, la sala da pranzo, la cucina, il soggiorno, lo studio e un piccolo bagno.\n"
        "6. Due camere da letto, il guardaroba e il bagno.\n"
        "7. Quelle sulla piazza sono luminose ma rumorose; quelle sul giardino sono silenziose e fresche.\n"
        "8. Comoda e accogliente."
    )
})

# ════════════════════════════════════════════════════════════════════════════════
# ESERCIZI DI VERIFICA — 20 escolha
# ════════════════════════════════════════════════════════════════════════════════

verifica = [
    # 1
    {"pergunta": "Oggi ___",
     "opcoes": ["ha uno sciopero dei treni.", "è uno sciopero dei treni.", "c'è uno sciopero dei treni."],
     "resposta": 2},
    # 2
    {"pergunta": "Sono a Firenze per frequentare la scuola e ___",
     "opcoes": ["rimango tre mesi.", "ci rimango tre mesi.", "rimangi tre mesi."],
     "resposta": 1},
    # 3
    {"pergunta": "Venite in discoteca stasera?",
     "opcoes": ["Sì, ci veniamo.", "Sì, veniamo.", "Sì, veniamo ci."],
     "resposta": 0},
    # 4
    {"pergunta": "Sei stato dal dottore? Sì, ___",
     "opcoes": ["sono stato.", "ci sono stato.", "sono ci stato."],
     "resposta": 1},
    # 5
    {"pergunta": "Questo appartamento è grande, ___",
     "opcoes": ["stiamo bene.", "ci stiamo bene."],
     "resposta": 1},
    # 6
    {"pergunta": "___ un incidente ieri pomeriggio davanti a casa mia.",
     "opcoes": ["Ha stato", "C'è stato", "È stato"],
     "resposta": 1},
    # 7
    {"pergunta": "Non è la prima volta che vengo in Italia: ___",
     "opcoes": ["sono già stata due anni fa.", "sono già ci stata due anni fa.", "ci sono già stata due anni fa."],
     "resposta": 2},
    # 8
    {"pergunta": "Lui ___ il nome della strada.",
     "opcoes": ["non sape", "non sa", "non sappi"],
     "resposta": 1},
    # 9
    {"pergunta": "Siena è bella: ___",
     "opcoes": ["voglio ci tornare ancora una volta.", "voglio tornarci ancora una volta.", "voglio torni ancora una volta."],
     "resposta": 1},
    # 10
    {"pergunta": "Mario ha invitato ___",
     "opcoes": ["qualche amici.", "qualche amico.", "qualche amichi."],
     "resposta": 1},
    # 11
    {"pergunta": "___ incontro Luigi quando torno dal lavoro.",
     "opcoes": ["Ogni giorni", "Ogni giorno", "Ogni le giornate"],
     "resposta": 1},
    # 12
    {"pergunta": "I miei amici ___",
     "opcoes": ["rimanete a dormire da me.", "rimanono a dormire da me.", "rimangono a dormire da me."],
     "resposta": 2},
    # 13
    {"pergunta": "Ho ___",
     "opcoes": ["qualche domanda da fare.", "qualche domande da fare.", "qualchi domande da fare."],
     "resposta": 0},
    # 14
    {"pergunta": "___ ha delle difficoltà.",
     "opcoes": ["Ogni frasa", "Ogni frasi", "Ogni frase"],
     "resposta": 2},
    # 15
    {"pergunta": "Ci sono ___",
     "opcoes": ["delle parole che non conosco.", "dei parole che non conosco.", "della parola che non conosco."],
     "resposta": 0},
    # 16
    {"pergunta": "A scuola ho incontrato ___",
     "opcoes": ["degli studenti giapponesi.", "dei studenti giapponesi.", "di studenti giapponesi."],
     "resposta": 0},
    # 17
    {"pergunta": "Paolo è uscito con ___",
     "opcoes": ["dei ragazze straniere.", "delle ragazze straniere.", "della ragazza straniere."],
     "resposta": 1},
    # 18
    {"pergunta": "Vai domani a teatro? No, ___",
     "opcoes": ["vado stasera.", "ci vado stasera.", "vado ci stasera."],
     "resposta": 1},
    # 19
    {"pergunta": "___ dimentico i nomi delle persone.",
     "opcoes": ["Qualche volta", "Qualche volte", "Qualchi volte"],
     "resposta": 0},
    # 20
    {"pergunta": "Ho comprato ___",
     "opcoes": ["delli fiori per mia zia.", "dei fiori per mia zia.", "degli fiori per mia zia."],
     "resposta": 1},
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
    ("Rimano un po' con te.",
     "Rimango un po' con te."),
    ("Silenzio! Facete troppa confusione.",
     "Silenzio! Fate troppa confusione."),
    ("Sceglio questo colore perché è più scuro.",
     "Scelgo questo colore perché è più scuro."),
    ("Sedi qua, accanto a me.",
     "Siediti qua, accanto a me."),
    ("Ando subito a casa, è tardi!",
     "Vado subito a casa, è tardi!"),
    ("Stasera non uscio, sono stanco.",
     "Stasera non esco, sono stanco."),
    ("Quando salo sull'autobus c'è sempre gente che spinge.",
     "Quando salgo sull'autobus c'è sempre gente che spinge."),
    ("Questo letto è troppo duro, non dormo bene. (nessun errore)",
     "Corretto! 'Non dormo bene' è già al presente → nessun errore grammaticale."),
    ("Come fai la torta? Meno latte, zucchero, farina, burro e uova.",
     "Come fai la torta? Metti latte, zucchero, farina, burro e uova. (meno → metti)"),
    ("Stai bene in questo appartamento? Sì, sto molto bene. (nessun errore)",
     "Corretto! La risposta 'ci sto molto bene' sarebbe più idiomatica ma 'sto' non è errore."),
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
print(f"OK: Lezione V — La particella 'ci'")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(exercicios)} total (escolha: {n_e}, revelar: {n_r})")
