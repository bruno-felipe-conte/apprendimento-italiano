import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione VIII"), None)
if lez is None:
    lez = {"id": "a1-lez8", "num": "Lezione VIII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I pronomi diretti"
lez["subtitulo"] = "Pronomi diretti (lo/la/li/le), partitivo NE e pronomi personali"

lez["teoria"] = """\
## In un negozio di abbigliamento

Giovanna vuole comprare una camicetta semplice e fresca di cotone, di un colore chiaro — rosa. La commessa le mostra una camicetta graziosa con tessuto fresco: Giovanna la prova e decide di comprarla (€ 30,99). Anna invece cerca un vestito sportivo, adatto a tutte le occasioni, abbastanza lungo e scuro, taglia 46. La commessa le mostra due modelli; Anna ne prova uno solo, quello a fantasia, e dopo qualche esitazione lo compra (€ 41,32).

---

## A I pronomi diretti

<table class="gram-table gram-table-rich">
<thead><tr><th>soggetto</th><th>complemento oggetto</th><th>al passato prossimo</th></tr></thead>
<tbody>
<tr><td>Saluto <strong>Paolo</strong></td><td>Lo saluto</td><td>L'ho salutato</td></tr>
<tr><td>Saluto <strong>Anna</strong></td><td>La saluto</td><td>L'ho salutata</td></tr>
<tr><td>Saluto <strong>gli amici</strong></td><td>Li saluto</td><td>Li ho salutati</td></tr>
<tr><td>Saluto <strong>le amiche</strong></td><td>Le saluto</td><td>Le ho salutate</td></tr>
<tr><td>Compro <strong>il pane</strong></td><td>Lo compro</td><td>L'ho comprato</td></tr>
<tr><td>Compro <strong>la pasta</strong></td><td>La compro</td><td>L'ho comprata</td></tr>
<tr><td>Compro <strong>gli spaghetti</strong></td><td>Li compro</td><td>Li ho comprati</td></tr>
<tr><td>Compro <strong>le mele</strong></td><td>Le compro</td><td>Le ho comprate</td></tr>
</tbody>
</table>

> **Al passato prossimo:** il participio concorda con il pronome diretto (lo/la/li/le).
> *L'ho salutata* (lei), *li ho salutati* (loro masch.), *le ho salutate* (loro femm.)

**b)** Il pronome **lo** può sostituire anche un'intera frase:
- Sai dove abita Valentina? → Sì, **lo** so.
- Partiremo presto? → Sì, **lo** so.

**c)** Forma di cortesia: **La** (per maschile e femminile):
- Signore, **La** vedo con molto piacere.
- Signora, **La** vedo con molto piacere.

**d)** Posizione dei pronomi: NON + PRONOME + VERBO, oppure VERBO + PRONOME (infinito):
- Luigi **lo** deve pagare = Luigi deve **pagarlo**.
- **Li** possiamo comprare qui = Possiamo **comprarli** qui.

---

## B Il pronome partitivo NE

**NE** sostituisce una parte di qualcosa (con quantità) o un'intera espressione introdotta da **di**:

| frase con quantità | con NE |
|---|---|
| Scrivo un tema. | **Ne** scrivo uno. |
| Ho scritto due temi. | **Ne** ho scritti due. / pochi / molti |
| Non ho scritto nessun tema. | Non **ne** ho scritto nessuno. |
| Bevi tutto il caffè? | No, **ne** bevo solo un po'. |
| Quanti anni hai? | **Ne** ho venticinque. |

> **CE L'HO / CE LI HO / CE LE HO** — quando il pronome si combina con **ci**:
> - Andrea, hai il dizionario? Sì, **ce l'ho**! No, non **ce l'ho**.
> - Ragazzi, avete i libri? Sì, **ce li abbiamo**. No, non **ce li abbiamo**.
> - Laura, hai le mie fotografie? Sì, **ce le ho** io! No, non **ce le ho**.

---

## C Pronomi personali — tabella completa

<table class="gram-table gram-table-rich">
<thead><tr><th>soggetto</th><th>complemento diretto</th><th>altri complementi</th></tr></thead>
<tbody>
<tr><td><strong>io</strong></td><td>mi chiama</td><td>parla di me, con me, ecc.</td></tr>
<tr><td><strong>tu</strong></td><td>ti chiama</td><td>parla di te, con te, ecc.</td></tr>
<tr><td><strong>lui</strong> (egli)</td><td>lo chiama</td><td>parla di lui, con lui, ecc.</td></tr>
<tr><td><strong>lei</strong> (ella)</td><td>la chiama</td><td>parla di lei, con lei, ecc.</td></tr>
<tr><td><strong>Lei</strong> (cortesia)</td><td>La chiama</td><td>parla di Lei, con Lei, ecc.</td></tr>
<tr><td><strong>noi</strong></td><td>ci chiama</td><td>parla di noi, con noi, ecc.</td></tr>
<tr><td><strong>voi</strong></td><td>vi chiama</td><td>parla di voi, con voi, ecc.</td></tr>
<tr><td><strong>loro</strong> (essi/esse)</td><td>li / le chiama</td><td>parla di loro, con loro, ecc.</td></tr>
</tbody>
</table>

---

## D L'uso di "stare per" + infinito

Indica un'azione che sta per accadere (futuro immediato):
- Giulio apre la porta → **Sta per** uscire.
- Il professore entra in classe → La lezione **sta per** cominciare.
- Il cielo è coperto → **Sta per** piovere.
"""

lez["exemplos"] = [
    "Ho comprato il pane → l'ho comprato.",
    "Conosco gli studenti → li conosco → li ho conosciuti.",
    "Quante mele vuoi? Ne voglio tre.",
    "Hai il dizionario? Sì, ce l'ho.",
    "Giulio sta per uscire.",
]

exercicios = []

# ── Domande sul dialogo ──────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Rispondere alle domande sul dialogo 'In un negozio di abbigliamento':",
    "pergunta": (
        "1. Che cosa vuole comprare Giovanna?\n"
        "2. Come la vuole?\n"
        "3. Perché preferisce il cotone?\n"
        "4. Che cosa fa Giovanna?\n"
        "5. Come sono i modelli di quest'anno?\n"
        "6. Che cosa vuole comprare Anna?\n"
        "7. Come lo vuole?\n"
        "8. Quale prova?\n"
        "9. Com'è il prezzo del vestito?"
    ),
    "resposta": (
        "1. Una camicetta.\n"
        "2. Semplice, fresca, di colore chiaro (rosa).\n"
        "3. Perché il lino è troppo delicato.\n"
        "4. La prova e la compra.\n"
        "5. Più aderenti dello scorso anno.\n"
        "6. Un vestito sportivo adatto a tutte le occasioni.\n"
        "7. Abbastanza lungo e scuro.\n"
        "8. Quello a fantasia.\n"
        "9. È buono / conveniente."
    )
})

# ── Esercizio 1 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1 — Sostituire il complemento oggetto con il pronome e volgere al passato:\nMod.: Studio il francese. → Lo studio. → L'ho studiato.",
    "pergunta": (
        "1. Il medico visita Giulio.\n"
        "2. Il professore corregge gli esercizi.\n"
        "3. Lo studente ripassa la lezione.\n"
        "4. Anna prepara il tè.\n"
        "5. Porto le caramelle ai bambini.\n"
        "6. Paolo conosce i miei fratelli.\n"
        "7. Il turista fotografa i monumenti.\n"
        "8. La mamma fa la torta di mele.\n"
        "9. Prepariamo la cena.\n"
        "10. Laura compra le carote.\n"
        "11. Il professore spiega i pronomi.\n"
        "12. Bevo il vino."
    ),
    "resposta": (
        "1. Lo visita. → L'ha visitato.\n"
        "2. Li corregge. → Li ha corretti.\n"
        "3. La ripassa. → L'ha ripassata.\n"
        "4. Lo prepara. → L'ha preparato.\n"
        "5. Le porto. → Le ho portate.\n"
        "6. Li conosce. → Li ha conosciuti.\n"
        "7. Li fotografa. → Li ha fotografati.\n"
        "8. La fa. → L'ha fatta.\n"
        "9. La prepariamo. → L'abbiamo preparata.\n"
        "10. Le compra. → Le ha comprate.\n"
        "11. Li spiega. → Li ha spiegati.\n"
        "12. Lo bevo. → L'ho bevuto."
    )
})

# ── Esercizio 2 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 2 — Rispondere alle domande con un pronome diretto:",
    "pergunta": (
        "1. Hai spedito le lettere?\n"
        "2. Hai ricevuto sue notizie?\n"
        "3. Hai scelto il regalo per la tua amica?\n"
        "4. Avete fissato l'incontro con il sindaco?\n"
        "5. Sai guidare la macchina?\n"
        "6. Chi guida la moto?\n"
        "7. Hai preso tu i miei occhiali?\n"
        "8. Chi ha preparato la cena?\n"
        "9. Avete dato l'esame di storia?\n"
        "10. Avete salutato i vostri amici?"
    ),
    "resposta": (
        "1. Sì, le ho spedite.\n"
        "2. Sì, le ho ricevute.\n"
        "3. Sì, l'ho scelto.\n"
        "4. Sì, l'abbiamo fissato.\n"
        "5. Sì, la so guidare.\n"
        "6. La guido io.\n"
        "7. No, non li ho presi.\n"
        "8. L'ho preparata io.\n"
        "9. Sì, l'abbiamo dato.\n"
        "10. Sì, li abbiamo salutati."
    )
})

# ── Esercizio 3 — Forma di cortesia ──────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 3 — Forma di cortesia: completare con i pronomi (La / Le / Li):",
    "pergunta": (
        "1. Signorina, ___ posso invitare a cena?\n"
        "2. Signorina, domani mattina ___ sveglierò io.\n"
        "3. Signore, domani mattina ___ sveglierà il portiere.\n"
        "4. Signora, ___ ringrazio e arriveder ___\n"
        "5. Signorina, se Lei permette, ___ accompagno a casa.\n"
        "6. Signorina, se non ___ disturbo, mi siedo qui accanto a lei.\n"
        "7. Signor Grassini, ___ prego di chiudere quella finestra.\n"
        "8. Signora, ___ prego di accettare questo regalo.\n"
        "9. Signore, mi scusi, ma non ___ sento bene.\n"
        "10. Se Lei vuole, ___ posso aiutare io a cercare un buon hotel.\n"
        "11. Carla, se Lei permette, ___ vorrei invitare a cena.\n"
        "12. Signorina Rita, non vorrei offender ___, ma Lei sbaglia.\n"
        "13. Signore, non vorrei offender ___, ma Lei non mi ha capito.\n"
        "14. Signora, io non riesco proprio a comprender ___!\n"
        "15. Dottore, io non ___ capisco!"
    ),
    "resposta": (
        "1. La posso invitare a cena?\n"
        "2. La sveglierò io.\n"
        "3. La sveglierà il portiere.\n"
        "4. La ringrazio e arrivederLa.\n"
        "5. La accompagno a casa.\n"
        "6. La disturbo.\n"
        "7. La prego di chiudere quella finestra.\n"
        "8. La prego di accettare questo regalo.\n"
        "9. La sento bene.\n"
        "10. La posso aiutare io.\n"
        "11. La vorrei invitare a cena.\n"
        "12. offenderLa.\n"
        "13. offenderLa.\n"
        "14. comprenderLa.\n"
        "15. La capisco."
    )
})

# ── Esercizio 4 — Pronomi personali diretti ───────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 4 — Pronomi personali diretti: rispondere con pronome:\nMod.: Mi senti? (bene) → Sì, ti sento bene.",
    "pergunta": (
        "1. Dove mi avete visto? (al bar)\n"
        "2. Chi ti ha invitato? (un mio vecchio amico)\n"
        "3. Chi vi ha salutato? (l'insegnante di storia)\n"
        "4. A che ora ti ha svegliato? (alle sette)\n"
        "5. Dove vi ho incontrato? (a casa di Paolo)\n"
        "6. Chi ci accompagna? (mio fratello)\n"
        "7. A che ora mi passa a prendere? (verso le nove)\n"
        "8. Chi vi ha chiamato? (il direttore)"
    ),
    "resposta": (
        "1. Vi abbiamo visto al bar.\n"
        "2. Mi ha invitato un mio vecchio amico.\n"
        "3. Ci ha salutato l'insegnante di storia.\n"
        "4. Mi ha svegliato alle sette.\n"
        "5. Vi ho incontrato a casa di Paolo.\n"
        "6. Ci accompagna mio fratello.\n"
        "7. La passo a prendere verso le nove.\n"
        "8. Ci ha chiamato il direttore."
    )
})

# ── Esercizio 5 — Rispondere con pronome (gruppi a-f) ────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 5 — Rispondere alle domande con un pronome diretto (gruppi 1-6):",
    "pergunta": (
        "1a. Hai riparato la bicicletta?\n"
        "1b. Hai controllato l'orario dei treni?\n"
        "1c. Hai rivisto il tuo amico?\n"
        "1d. Hai pagato molto questi orecchini?\n\n"
        "2a. Chi ha spento la luce?\n"
        "2b. Chi ha chiuso la porta?\n"
        "2c. Chi ha preso i miei dischi?\n"
        "2d. Chi ha ascoltato il concerto?\n\n"
        "3a. Dove hai parcheggiato la macchina?\n"
        "3b. Dove hai imbucato le lettere?\n"
        "3c. Dove avete messo i soldi?\n"
        "3d. Dove avete posato il mio cappello?\n\n"
        "4a. Quando avete attaccato questi quadri?\n"
        "4b. Quando avete cambiato casa?\n"
        "4c. Quando avete salutato i vostri amici?\n"
        "4d. Quando hai preso quella brutta tosse?\n\n"
        "5a. Hai corretto le frasi sbagliate?\n"
        "5b. Hai letto il biglietto che ti ho scritto?\n"
        "5c. Hai salutato la padrona di casa?\n"
        "5d. Hai aspettato i tuoi figli all'uscita di scuola?\n\n"
        "6a. Chi ha dipinto questi affreschi?\n"
        "6b. Chi ha progettato questo palazzo?\n"
        "6c. Chi ha realizzato quest'opera d'arte?\n"
        "6d. Chi ha restaurato quelle vecchie sedie?"
    ),
    "resposta": (
        "1a. Sì, l'ho riparata.\n"
        "1b. Sì, l'ho controllato.\n"
        "1c. Sì, l'ho rivisto.\n"
        "1d. Sì, li ho pagati molto.\n\n"
        "2a. L'ha spenta Mario (es.).\n"
        "2b. L'ha chiusa Luca (es.).\n"
        "2c. Li ha presi Anna (es.).\n"
        "2d. L'ha ascoltato Paolo (es.).\n\n"
        "3a. L'ho parcheggiata in via Roma (es.).\n"
        "3b. Le ho imbucate davanti alla farmacia (es.).\n"
        "3c. Li abbiamo messi in banca (es.).\n"
        "3d. L'abbiamo posato sul tavolo (es.).\n\n"
        "4a. Li abbiamo attaccati la settimana scorsa (es.).\n"
        "4b. L'abbiamo cambiata due anni fa (es.).\n"
        "4c. Li abbiamo salutati ieri (es.).\n"
        "4d. L'ho presa in gennaio (es.).\n\n"
        "5a. Sì, le ho corrette.\n"
        "5b. Sì, l'ho letto.\n"
        "5c. Sì, l'ho salutata.\n"
        "5d. Sì, li ho aspettati.\n\n"
        "6a. Li ha dipinti Giotto (es.).\n"
        "6b. L'ha progettato Brunelleschi (es.).\n"
        "6c. L'ha realizzata il maestro (es.).\n"
        "6d. Le ha restaurate un antiquario (es.)."
    )
})

# ── Conversazione ─────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Conversazione — A teatro / Al cinema (leggere i dialoghi):",
    "pergunta": (
        "A teatro:\n"
        "— Pronto, signorina, mi sente?\n"
        "— Sì, la sento bene. Prego, dica pure!\n"
        "— Vorrei prenotare due poltrone in platea, possibilmente centrali, per lo spettacolo di venerdì.\n"
        "— Mi dispiace, ma in platea i posti sono esauriti, però ce ne sono due liberi in galleria, non troppo laterali. Vanno bene, anche se sono un po' lontani dal palcoscenico. A che ora comincia lo spettacolo?\n"
        "— Alle venti e trenta precise.\n"
        "— E a che ora finisce?\n"
        "— A mezzanotte meno un quarto.\n"
        "— Grazie, signorina, arrivederla.\n\n"
        "Al cinema:\n"
        "— Tre biglietti, per favore; due normali e uno ridotto.\n"
        "— Mi dispiace, ma le riduzioni ci sono soltanto il martedì.\n"
        "— È vero, ha ragione. Platea o galleria?\n"
        "— Platea, grazie. Quanto spendo?\n"
        "— Dodici euro trentanove centesimi.\n"
        "— Ecco a Lei. A che ora comincia il film?\n"
        "— Fra venti minuti, quando finirà il secondo tempo del primo spettacolo.\n"
        "— Grazie tante."
    ),
    "resposta": "Dialogo al botteghino di teatro e cinema."
})

# ── Vocabolario — Il vestiario ─────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lettura — 'Il guardaroba dei signori Chiari' (rispondere alle domande):",
    "pergunta": (
        "Il signore e la signora Chiari vestono sempre in modo semplice, ma raffinato. Nella "
        "loro camera da letto c'è un grande armadio a quattro ante dove tengono i loro vestiti "
        "e la loro biancheria. Le due ante a sinistra sono per i vestiti della signora Chiari "
        "e le due a destra per i vestiti del marito. La signora Chiari tiene i capi di "
        "vestiario invernale separati da quelli estivi e da quelli per la mezza stagione. "
        "In un'anta dell'armadio ci sono i cappotti, le giacche, le gonne di lana e "
        "l'impermeabile; mentre nell'altra ci sono le gonne, i vestitini leggeri e le "
        "camicette. La signora Chiari ha disposto il vestiario del marito nelle altre due "
        "ante: un cappotto, un impermeabile, tre completi sportivi, due completi eleganti, "
        "alcune paia di pantaloni e le camicie. Nel ripostiglio c'è un altro armadio con i "
        "capi sportivi: maglioni da sci, giacche a vento, berretti di lana, sciarpe, ecc.\n\n"
        "1. Come vestono i signori Chiari?\n"
        "2. Che cosa c'è nella loro camera da letto?\n"
        "3. Che cosa c'è nelle due ante a sinistra?\n"
        "4. Che cosa c'è nelle due ante a destra?\n"
        "5. Quali sono i capi di vestiario invernali della signora?\n"
        "6. Quali sono i capi estivi?\n"
        "7. Quali sono i vestiti del signor Chiari?\n"
        "8. Che cosa c'è nel ripostiglio?"
    ),
    "resposta": (
        "1. In modo semplice ma raffinato.\n"
        "2. Un grande armadio a quattro ante.\n"
        "3. I vestiti della signora Chiari.\n"
        "4. I vestiti del marito.\n"
        "5. Cappotti, giacche, gonne di lana, impermeabile.\n"
        "6. Gonne, vestitini leggeri, camicette.\n"
        "7. Un cappotto, un impermeabile, tre completi sportivi, due completi eleganti, pantaloni, camicie.\n"
        "8. Un armadio con capi sportivi: maglioni da sci, giacche a vento, berretti, sciarpe."
    )
})

# ── Esercizio 6 — Rispondere con pronome ─────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 6 — Rispondere alle domande con un pronome diretto:",
    "pergunta": (
        "1. A chi hai mandato quei fiori?\n"
        "2. A chi hai letto la tua poesia?\n"
        "3. A chi hai preparato la sorpresa?\n"
        "4. A chi hai lasciato il tuo gatto durante l'estate?\n"
        "5. Sai di chi è la borsa?\n"
        "6. Sai che lavoro fa suo padre?\n"
        "7. Hai saputo chi è morto?\n"
        "8. Hai stirato la camicia?\n"
        "9. Hai lavato il vestito?\n"
        "10. Hai assaggiato la torta?\n"
        "11. Hai pagato le bollette?\n"
        "12. Hai attaccato il quadro?\n"
        "13. Hai pulito i vetri delle finestre?\n"
        "14. Hai letto le riviste?\n"
        "15. Hai preso l'ombrello?\n"
        "16. Hai fatto le valigie?\n"
        "17. Hai corretto la composizione?\n"
        "18. Hai aperto il pacco?\n"
        "19. Dove getti la spazzatura?\n"
        "20. Dove hai messo le scarpe?\n"
        "21. Dove hai comprato quella cravatta?\n"
        "22. Dove hai lasciato le valigie?"
    ),
    "resposta": (
        "1. Li ho mandati a mia madre (es.).\n"
        "2. L'ho letta a Carla (es.).\n"
        "3. L'ho preparata per Giulio (es.).\n"
        "4. L'ho lasciato ai miei vicini (es.).\n"
        "5. Sì, lo so.\n"
        "6. Sì, lo so.\n"
        "7. Sì, l'ho saputo.\n"
        "8. Sì, l'ho stirata.\n"
        "9. Sì, l'ho lavato.\n"
        "10. Sì, l'ho assaggiata.\n"
        "11. Sì, le ho pagate.\n"
        "12. Sì, l'ho attaccato.\n"
        "13. Sì, li ho puliti.\n"
        "14. Sì, le ho lette.\n"
        "15. Sì, l'ho preso.\n"
        "16. Sì, le ho fatte.\n"
        "17. Sì, l'ho corretta.\n"
        "18. Sì, l'ho aperto.\n"
        "19. La getto nel bidone (es.).\n"
        "20. Le ho messe nell'armadio (es.).\n"
        "21. L'ho comprata in centro (es.).\n"
        "22. Le ho lasciate in albergo (es.)."
    )
})

# ── Esercizio 7 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 7 — Come il precedente (rispondere con pronome diretto):",
    "pergunta": (
        "1. Hai preso l'autobus?\n"
        "2. Quando hai perduto le chiavi di casa?\n"
        "3. Hai letto il libro che ti ho prestato?\n"
        "4. Hai fatto gli esercizi per oggi?\n"
        "5. Hai comprato tu la frutta?\n"
        "6. Hai speso tutti i soldi?\n"
        "7. Sai suonare la tromba?\n"
        "8. Chi ha preso la mia giacca?\n"
        "9. Chi ha vinto la partita tra l'Inter e il Milan?\n"
        "10. Chi ha vinto il campionato di calcio?"
    ),
    "resposta": (
        "1. Sì, l'ho preso.\n"
        "2. Le ho perdute ieri (es.).\n"
        "3. Sì, l'ho letto.\n"
        "4. Sì, li ho fatti.\n"
        "5. Sì, l'ho comprata io.\n"
        "6. Sì, li ho spesi tutti.\n"
        "7. Sì, la so suonare.\n"
        "8. L'ha presa Marco (es.).\n"
        "9. L'ha vinta l'Inter (es.).\n"
        "10. L'ha vinto la Juventus (es.)."
    )
})

# ── Esercizio 8 — Pronome NE ─────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8 — Completare con i pronomi (NE / lo / la / li / le):",
    "pergunta": (
        "1. Quanto vino hai bevuto? ___ ho bevuto molto.\n"
        "2. Quanta birra hai bevuto? ___ ho bevuto abbastanza.\n"
        "3. Quante traduzioni hai fatto? ___ ho fatte tante.\n"
        "4. Quanta torta hai mangiato? ___ ho mangiata una fetta.\n"
        "5. Quanta pizza hai mangiato? ___ ho mangiata metà.\n"
        "6. Quante sigarette hai fumato ieri? ___ ho fumata una sola.\n"
        "7. Ho visto delle mele e ___ ho prese alcune.\n"
        "8. Mi piacciono molto le banane. ___ mangio molte.\n"
        "9. Ti piace questo vino? ___ vuoi ancora? No, grazie ___ ho già bevuto abbastanza.\n"
        "10. Mi piacciono i gatti e a casa mia ___ tengo tre.\n"
        "11. Scrivo molte cartoline, oggi ___ ho scritte tre.\n"
        "12. Queste frasi sono molto complicate, ___ ho fatte poche.\n"
        "13. Questo libro è divertente, ___ comprerò alcune copie per i miei amici.\n"
        "14. Quanti anni hai? ___ ho molti più di te!\n"
        "15. Ti piacciono questi dischi? ___ vuoi alcuni o ___ vuoi tutti?\n"
        "16. Quante maglie porti? ___ porto due.\n"
        "17. Quanti giornali leggi al giorno? ___ leggo uno solo.\n"
        "18. Consuma molta benzina questa macchina? Sì, ___ consuma molta."
    ),
    "resposta": (
        "1. Ne ho bevuto molto.\n"
        "2. Ne ho bevuta abbastanza.\n"
        "3. Ne ho fatte tante.\n"
        "4. Ne ho mangiata una fetta.\n"
        "5. Ne ho mangiata metà.\n"
        "6. Ne ho fumata una sola.\n"
        "7. ne ho prese alcune.\n"
        "8. Ne mangio molte.\n"
        "9. Ne vuoi ancora? / ne ho già bevuto abbastanza.\n"
        "10. ne tengo tre.\n"
        "11. ne ho scritte tre.\n"
        "12. ne ho fatte poche.\n"
        "13. ne comprerò alcune copie.\n"
        "14. Ne ho molti più di te!\n"
        "15. Ne vuoi alcuni / li vuoi tutti?\n"
        "16. Ne porto due.\n"
        "17. Ne leggo uno solo.\n"
        "18. ne consuma molta."
    )
})

# ── Lavorare sul testo ────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lavorare sul testo — 'Una serata al cinema' (rispondere alle domande):",
    "pergunta": (
        "Per tutto questo mese al cinema Vittoria è in programmazione una rassegna di film "
        "dedicata a Pier Paolo Pasolini, il celebre regista e scrittore italiano che ha "
        "diretto film come Accatrone, Teorema e molti altri. I film più significativi di "
        "Pasolini sono entrati nella storia del cinema italiano e internazionale. Venerdì "
        "prossimo daranno Mamma Roma, un film del 1962 con la famosa attrice Anna Magnani "
        "nel ruolo di protagonista. Paolo e Luigi, due appassionati di cinema, hanno deciso "
        "di andare a vederlo. Ci andranno alle nove, al primo spettacolo della sera, e poi, "
        "quando il film sarà finito, passeranno un po' di tempo a parlare degli attori, del "
        "regista, della sceneggiatura, seduti in un locale davanti a un bicchiere di vino. "
        "Infine, verso mezzanotte, torneranno a casa contenti di come hanno trascorso la serata.\n\n"
        "1. Che cosa è in programmazione al cinema Vittoria?\n"
        "2. Chi è Pier Paolo Pasolini?\n"
        "3. Che film ha diretto?\n"
        "4. Dove sono entrati i suoi film più significativi?\n"
        "5. Che film daranno venerdì prossimo?\n"
        "6. Chi è la protagonista?\n"
        "7. Chi sono Paolo e Luigi?\n"
        "8. Che cosa hanno deciso di fare?\n"
        "9. A quale spettacolo andranno?\n"
        "10. Che cosa faranno quando il film sarà finito?\n"
        "11. A che ora torneranno a casa?\n"
        "12. Come saranno?"
    ),
    "resposta": (
        "1. Una rassegna di film dedicata a Pier Paolo Pasolini.\n"
        "2. Un celebre regista e scrittore italiano.\n"
        "3. Accatrone, Teorema e molti altri.\n"
        "4. Nella storia del cinema italiano e internazionale.\n"
        "5. Mamma Roma (1962).\n"
        "6. Anna Magnani.\n"
        "7. Due appassionati di cinema.\n"
        "8. Di andare a vedere il film.\n"
        "9. Al primo spettacolo della sera, alle nove.\n"
        "10. Passeranno un po' di tempo a parlare del film in un locale.\n"
        "11. Verso mezzanotte.\n"
        "12. Contenti di come hanno trascorso la serata."
    )
})

# ════════════════════════════════════════════════════════════════════════════════
# ESERCIZI DI VERIFICA — 20 escolha
# ════════════════════════════════════════════════════════════════════════════════

verifica = [
    # 1
    {"pergunta": "Chi è Giorgio? ___",
     "opcoes": ["Io non la conosco.", "Io non lo conosco.", "Io non il conosco."],
     "resposta": 1},
    # 2
    {"pergunta": "Finirò la lettera e ___",
     "opcoes": ["lo spedisco subito.", "La spedisco subito.", "la spedisco subito."],
     "resposta": 2},
    # 3
    {"pergunta": "Sono a piedi: ___",
     "opcoes": ["puoi mi accompagnare?", "mi puoi accompagnare?", "puoi accompagnarme?"],
     "resposta": 1},
    # 4
    {"pergunta": "Dove prendi l'autobus? ___",
     "opcoes": ["Lo prendo alla stazione.", "La prendo alla stazione.", "Il prendo alla stazione."],
     "resposta": 0},
    # 5
    {"pergunta": "Non compro mai dischi, ___",
     "opcoes": ["loro registro da un amico.", "li registro da un amico.", "le registro da un amico."],
     "resposta": 1},
    # 6
    {"pergunta": "La tua amica è già arrivata: ___",
     "opcoes": ["l'ho visto poco fa in segreteria.", "la sono vista poco fa in segreteria.", "l'ho vista poco fa in segreteria."],
     "resposta": 2},
    # 7
    {"pergunta": "Non ho ancora i biglietti: ___",
     "opcoes": ["tu hai comprato?", "tu li hai comprato?", "tu li hai comprati?"],
     "resposta": 2},
    # 8
    {"pergunta": "Grazie, signora e ___",
     "opcoes": ["arrivederti.", "arrivederLa.", "arrivederLe."],
     "resposta": 1},
    # 9
    {"pergunta": "Quanti anni hai? ___",
     "opcoes": ["Ho venticinque.", "Li ho venticinque.", "Ne ho venticinque."],
     "resposta": 2},
    # 10
    {"pergunta": "Questo vocabolario è vecchio: ___",
     "opcoes": ["devo comprare uno nuovo.", "devo comprarne uno nuovo.", "devo comprarlo uno nuovo."],
     "resposta": 1},
    # 11
    {"pergunta": "Grazie, ma non prendo il caffè: ___",
     "opcoes": ["ne ho già presi due stamattina.", "li ho già presi due stamattina.", "ne ho già preso due stamattina."],
     "resposta": 0},
    # 12
    {"pergunta": "Bella questa giacca! ___",
     "opcoes": ["Dove l'hai comprata?", "Dove ne hai comprata?", "Dove hai comprata la?"],
     "resposta": 0},
    # 13
    {"pergunta": "Signorina, ___",
     "opcoes": ["ti posso aiutare?", "La posso aiutare?", "posso La aiutare?"],
     "resposta": 1},
    # 14
    {"pergunta": "Questi cioccolatini sono buoni, ___",
     "opcoes": ["prendo un altro.", "ne prendo un altro.", "lo prendo un altro."],
     "resposta": 1},
    # 15
    {"pergunta": "Ho pochi soldi: ___",
     "opcoes": ["li ho spesi troppi.", "ne ho spesi troppi.", "ho spesi troppi."],
     "resposta": 1},
    # 16
    {"pergunta": "Dove hai passato le vacanze? ___",
     "opcoes": ["Le ho passate con i miei genitori al mare.", "Ne ho passate con i miei genitori al mare.", "Le ho passato con i miei genitori al mare."],
     "resposta": 0},
    # 17
    {"pergunta": "C'è ancora pasta: ___",
     "opcoes": ["la vuoi un po'?", "vuoi un po'?", "ne vuoi un po'?"],
     "resposta": 2},
    # 18
    {"pergunta": "La macchina è guasta: ___",
     "opcoes": ["devo la portare dal meccanico.", "devo portarla dal meccanico.", "lo devo portare dal meccanico."],
     "resposta": 1},
    # 19
    {"pergunta": "Ha un documento, signore? ___",
     "opcoes": ["Sì, l'ho.", "Sì, ce l'ho.", "Sì, io ho."],
     "resposta": 1},
    # 20
    {"pergunta": "Questa notizia è falsa: ___",
     "opcoes": ["dove hai letto?", "dove l'hai letto?", "dove l'hai letta?"],
     "resposta": 2},
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
    ("Non ho la macchina fotografica, l'ho lasciato a casa.",
     "Non ho la macchina fotografica, l'ho lasciata a casa."),
    ("Ci sono rimasti pochi posti: dobbiamo li prenotare subito.",
     "Ci sono rimasti pochi posti: dobbiamo prenotarli subito."),
    ("Questi esercizi sono troppi: faccio solo due.",
     "Questi esercizi sono troppi: ne faccio solo due."),
    ("Mia zia è malata: l'ho accompagnato a casa.",
     "Mia zia è malata: l'ho accompagnata a casa."),
    ("Conosco i film di Fellini: li ho visto molti.",
     "Conosco i film di Fellini: ne ho visti molti."),
    ("Preparo il pacco e mando alla zia.",
     "Preparo il pacco e lo mando alla zia."),
    ("Molti negozi sono cari, ma ho trovato uno a buon mercato.",
     "Molti negozi sono cari, ma ne ho trovato uno a buon mercato."),
    ("È una mostra molto interessante: l'ho visitato ieri.",
     "È una mostra molto interessante: l'ho visitata ieri."),
    ("Posso avere il suo numero di telefono? Mi dispiace ma non l'ho.",
     "Posso avere il suo numero di telefono? Mi dispiace ma non ce l'ho."),
    ("Devi fare da solo questo lavoro? Se vuoi, aiuto te.",
     "Devi fare da solo questo lavoro? Se vuoi, ti aiuto."),
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
print(f"OK: Lezione VIII — I pronomi diretti")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(exercicios)} total (escolha: {n_e}, revelar: {n_r})")
