import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

# Find or create Lezione VII
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione VII"), None)
if lez is None:
    lez = {"id": "a1-lez7", "num": "Lezione VII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I possessivi"
lez["subtitulo"] = "Aggettivi e pronomi possessivi"

lez["teoria"] = """\
## Una lettera a un'amica

Mia cara Daniela, finalmente ho trovato un po' di tempo per scriverti e per rispondere alla tua lettera. Le mie giornate sono molto intense, ho sempre tante cose da fare: la mattina, come sai, lavoro a scuola e il pomeriggio è dedicato alla famiglia e alla casa. Per fortuna mia madre viene spesso da noi e passa molto tempo con i bambini. La sera sono quasi sempre stanca morta, così vado a letto presto, ma qualche volta esco con mio marito per andare a casa di alcuni nostri amici o al cinema.
Mio marito sta bene ed è contento del suo nuovo lavoro in banca: i colleghi sono simpatici e il direttore è un uomo gentile e capace. Mia figlia Giulia fra qualche giorno comincerà ad andare a scuola ed è molto impaziente di conoscere i suoi compagni di classe. Francesco invece, l'altro mio figlio, in questo momento è in campagna con i suoi nonni. Anche Chicco, il nostro gatto, sta bene, ma è sempre dispettoso. In questo momento è sulle mie gambe e dorme tranquillo. Ora, mia cara amica, ti devo lasciare, ma spero di avere presto tue notizie. Ti penso sempre con affetto.
Un abbraccio, tua Laura.

---

## A I possessivi — tabella completa

<table class="gram-table gram-table-rich">
<thead>
<tr><th></th><th>io</th><th>tu</th><th>lui/lei/Lei</th><th>noi</th><th>voi</th><th>loro</th></tr>
</thead>
<tbody>
<tr>
  <td class="gram-art">masch. sing.</td>
  <td>il <strong>mio</strong> gatto</td>
  <td>il <strong>tuo</strong> gatto</td>
  <td>il <strong>suo</strong> gatto / il <strong>Suo</strong> gatto</td>
  <td>il <strong>nostro</strong> bambino</td>
  <td>il <strong>vostro</strong> bambino</td>
  <td>il <strong>loro</strong> bambino</td>
</tr>
<tr>
  <td class="gram-art">femm. sing.</td>
  <td>la <strong>mia</strong> gatta</td>
  <td>la <strong>tua</strong> gatta</td>
  <td>la <strong>sua</strong> gatta / la <strong>Sua</strong> gatta</td>
  <td>la <strong>nostra</strong> bambina</td>
  <td>la <strong>vostra</strong> bambina</td>
  <td>la <strong>loro</strong> bambina</td>
</tr>
<tr>
  <td class="gram-art">masch. plur.</td>
  <td>i <strong>miei</strong> gatti</td>
  <td>i <strong>tuoi</strong> gatti</td>
  <td>i <strong>suoi</strong> gatti / i <strong>Suoi</strong> gatti</td>
  <td>i <strong>nostri</strong> bambini</td>
  <td>i <strong>vostri</strong> bambini</td>
  <td>i <strong>loro</strong> bambini</td>
</tr>
<tr>
  <td class="gram-art">femm. plur.</td>
  <td>le <strong>mie</strong> gatte</td>
  <td>le <strong>tue</strong> gatte</td>
  <td>le <strong>sue</strong> gatte / le <strong>Sue</strong> gatte</td>
  <td>le <strong>nostre</strong> bambine</td>
  <td>le <strong>vostre</strong> bambine</td>
  <td>le <strong>loro</strong> bambine</td>
</tr>
</tbody>
</table>

---

## B Regole importanti

**a) L'aggettivo possessivo è sempre preceduto dall'articolo**, ma perde l'articolo quando precede un nome di parentela al singolare (padre, madre, figlio, figlia, fratello, sorella, marito, moglie, zio, zia, nonno, nonna, nipote, cugino, cugina, suocero, suocera...) — **eccetto** la terza persona plurale **loro**:

| con articolo | senza articolo |
|---|---|
| il mio amico | **mio** padre |
| la tua casa | **mia** madre |
| i suoi libri | **suo** fratello |
| il loro cane | il **loro** padre ← loro vuole sempre l'articolo |

**b) Il possessivo conserva l'articolo** quando il nome di parentela è:
- alterato: il mio fratellino, la mia sorellona
- accompagnato da aggettivo: la mia sorella sposata, il mio caro babbo

**c) Pronome possessivo** (dopo essere):
- Carlo, è **tuo** questo libro? Sì, è **mio**, grazie.
- Laura, sono **nostri** questi cappotti? No, non sono **nostri**, ma **suoi**.

**d) Espressioni senza articolo** (possessivo posposto):
- a casa **mia** (tua, sua...)
- per conto **mio** (tio, suo...)
- è colpa **mia** (tua, sua...)
- a modo **mio** (tuo, suo...)

---

## C Vocabolario sistematico — Che ora è?

**Che ora è? / Che ore sono?**

- Sono le (ore) quindici = Sono le **tre** (del pomeriggio)
- Sono le tre e venticinque
- Sono le tre e mezza (mezzo)
- Sono le tre e quarantacinque = Manca un quarto alle quattro = Sono le quattro meno un quarto
- È **mezzogiorno** (ore 12:00)
- È **mezzanotte** (ore 24:00)

**Ore con orologio:**
06.20 → Sono le sei e venti
14.30 → Sono le due e mezza (del pomeriggio)
12.45 → È l'una meno un quarto / Sono le tredici e quarantacinque
05.40 → Sono le sei meno venti
22.15 → Sono le dieci e un quarto (di sera)
24.03 → È mezzanotte e tre

---

## D Uso di siccome, perché e perciò

| connettivo | posizione | esempio |
|---|---|---|
| **siccome** (causa) | prima della causa | **Siccome** fa freddo, preferisco rimanere a casa. |
| **perché** (causa) | dopo l'effetto | Preferisco rimanere a casa **perché** fa freddo. |
| **perciò** (conseguenza) | dopo la causa | Fa freddo, **perciò** preferisco rimanere a casa. |
"""

lez["exemplos"] = [
    "Mio marito è contento del suo nuovo lavoro.",
    "I suoi nonni vivono in campagna.",
    "Loro padre è medico. (con articolo: il loro padre)",
    "Sono a casa mia, non al loro posto.",
    "Siccome è tardi, torno a casa in autobus.",
]

exercicios = []

# ── Domande sulla lettera ─────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Rispondere alle domande sulla lettera di Laura:",
    "pergunta": (
        "1. Come sono le giornate di Laura?\n"
        "2. Come trascorre la mattina e il pomeriggio?\n"
        "3. Che cosa fa la sera?\n"
        "4. Perché il marito è contento del suo nuovo lavoro?\n"
        "5. Che cosa farà sua figlia Giulia?\n"
        "6. Dov'è Francesco?\n"
        "7. Chi è Chicco?\n"
        "8. Com'è?\n"
        "9. Che cosa spera Laura?"
    ),
    "resposta": (
        "1. Sono molto intense, ha sempre tante cose da fare.\n"
        "2. La mattina lavora a scuola; il pomeriggio è dedicato alla famiglia e alla casa.\n"
        "3. Va a letto presto, ma qualche volta esce con il marito.\n"
        "4. Perché i colleghi sono simpatici e il direttore è gentile e capace.\n"
        "5. Comincerà ad andare a scuola.\n"
        "6. È in campagna con i suoi nonni.\n"
        "7. Il gatto della famiglia.\n"
        "8. È dispettoso.\n"
        "9. Spera di avere presto notizie da Daniela."
    )
})

# ── Esercizio 1 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1 — Completare con il possessivo adatto:",
    "pergunta": (
        "1. Lisa ha una bella casa, ma ___ camera da letto è piccola.\n"
        "2. Signore, quello rosso è ___ libro di grammatica.\n"
        "3. Ragazze, ___ chiavi sono sul tavolo del salotto.\n"
        "4. Io ho una macchina: ___ macchina è rossa.\n"
        "5. Ieri sono andato con ___ sorella a fare una passeggiata.\n"
        "6. Barbara ha dimenticato ___ matite sul tavolo.\n"
        "7. I miei genitori hanno molti amici: ___ amici sono simpatici.\n"
        "8. Lucia, sono queste ___ sigarette?\n"
        "9. Noi abbiamo uno zio: ___ zio si chiama Tom e vive in America.\n"
        "10. Di chi sono questi libri? Sono ___, professore? No, non sono ___, ma di Mario."
    ),
    "resposta": (
        "1. la sua\n"
        "2. il Suo\n"
        "3. le vostre\n"
        "4. la mia\n"
        "5. mia\n"
        "6. le sue\n"
        "7. i loro\n"
        "8. le tue\n"
        "9. nostro\n"
        "10. Suoi / miei"
    )
})

# ── Esercizio 2 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 2 — Come il precedente (possessivi):",
    "pergunta": (
        "1. Paolo, devo mettere lo zucchero nel ___ caffè?\n"
        "2. Abbiamo mandato a scuola ___ bambini.\n"
        "3. Ragazzi, il professore ha corretto ___ frasi?\n"
        "4. Ho incontrato Luigi con ___ moglie.\n"
        "5. I bambini hanno chiuso a chiave ___ stanza.\n"
        "6. Abbiamo incontrato ___ zio.\n"
        "7. Dove ho messo ___ scarpe?\n"
        "8. Abbiamo speso tutti ___ soldi.\n"
        "9. Laura, hai comprato il latte per ___ sorella?\n"
        "10. Abbiamo perso ___ cane! È forse grigio ___ cane?"
    ),
    "resposta": (
        "1. tuo\n"
        "2. i nostri\n"
        "3. le vostre\n"
        "4. sua\n"
        "5. la loro\n"
        "6. nostro\n"
        "7. le mie\n"
        "8. i nostri\n"
        "9. tua\n"
        "10. il nostro / il tuo"
    )
})

# ── Esercizio 3 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 3 — Completare con il possessivo adatto:",
    "pergunta": (
        "1. Professore, sono ___ queste riviste?\n"
        "2. Non potete venire da noi se non conoscete ___ indirizzo.\n"
        "3. Mentre Luisa e Grazia discutono, noi ascoltiamo ___ discorsi.\n"
        "4. Sono andato al cinema con ___ madre e ___ fratelli.\n"
        "5. Leggete bene ___ appunti.\n"
        "6. Paola e Caterina leggono ___ oroscopo.\n"
        "7. Signore, è ___ questo giornale?\n"
        "8. Gianni, sono ___ questi libri?\n"
        "9. ___ casa è molto bella, signora.\n"
        "10. Ho regalato tutti ___ giocattoli a quel bambino."
    ),
    "resposta": (
        "1. Sue\n"
        "2. il nostro\n"
        "3. i loro\n"
        "4. mia / i miei\n"
        "5. i vostri\n"
        "6. il loro\n"
        "7. il Suo\n"
        "8. i tuoi\n"
        "9. La Sua\n"
        "10. i miei"
    )
})

# ── Esercizio 4 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 4 — Come il precedente (possessivi):",
    "pergunta": (
        "1. Tutti hanno ___ problemi.\n"
        "2. Qual è ___ scuola, Guido?\n"
        "3. Rinaldo è arrivato con ___ macchina nuova.\n"
        "4. Signorina, ___ vestito è veramente bello.\n"
        "5. Luigi, Franca, avete dimenticato ___ quaderni!\n"
        "6. Elena, ___ camicia è molto elegante.\n"
        "7. Professore, ___ lezione è interessante.\n"
        "8. Tutti hanno ___ idee.\n"
        "9. Laura, hai deciso di tornare a casa ___?\n"
        "10. Laura e Carlo abitano nella ___ nuova casa da pochi mesi."
    ),
    "resposta": (
        "1. i loro\n"
        "2. la tua\n"
        "3. la sua\n"
        "4. il Suo\n"
        "5. i vostri\n"
        "6. la tua\n"
        "7. la Sua\n"
        "8. le loro\n"
        "9. tua (a casa tua)\n"
        "10. la loro"
    )
})

# ── Conversazione — Dal tabaccaio ─────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Conversazione — Dal tabaccaio (leggere i dialoghi):",
    "pergunta": (
        "1° Cliente: Vorrei un pacchetto di sigarette, Super senza filtro, e una scatola di cerini.\n"
        "Tabaccaio: Mi dispiace signore, ma ho solamente le Super con filtro.\n"
        "1° Cliente: Allora prendo un pacchetto di MS. Quant'è in tutto?\n"
        "Tabaccaio: Duemilacinquecento lire.\n"
        "1° Cliente: Grazie, arrivederci.\n"
        "Tabaccaio: Prego, arrivederci.\n\n"
        "2° Cliente: Una busta per posta aerea e un francobollo per lettera, per favore.\n"
        "Tabaccaio: Il francobollo per l'Italia o per l'estero?\n"
        "2° Cliente: Per gli Stati Uniti, via aerea.\n"
        "Tabaccaio: Desidera altro, signora?\n"
        "2° Cliente: No, grazie. Quanto Le devo?\n"
        "Tabaccaio: Ottanta centesimi.\n"
        "2° Cliente: Mi sa dire se qui vicino c'è una buca per le lettere?\n"
        "Tabaccaio: Sì, è un po' più avanti, dall'altra parte della strada.\n"
        "2° Cliente: Grazie tante, arrivederci.\n"
        "Tabaccaio: Arrivederci."
    ),
    "resposta": "Dialogo al tabaccaio per comprare sigarette e francobolli."
})

# ── Esercizio 5 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 5 — Completare con il possessivo adatto:",
    "pergunta": (
        "1. Maurizio, qual è ___ bicicletta?\n"
        "2. Chi sono ___ amici, Riccardo?\n"
        "3. Ho dimenticato ___ borsa a casa di Claudio.\n"
        "4. Di chi sono questi guanti? Sono ___\n"
        "5. Dov'è Bruno? Ho trovato ___ cappello e ___ sigarette nel salotto.\n"
        "6. Mi piace molto leggere e ho molti libri nella ___ biblioteca.\n"
        "7. Hai voglia di rivedere ___ città?\n"
        "8. Signora, è ___ questo cappello?\n"
        "9. Veronica è triste perché ___ genitori sono partiti.\n"
        "10. Luca, hai visto ___ occhiali?"
    ),
    "resposta": (
        "1. la tua\n"
        "2. i tuoi\n"
        "3. la mia\n"
        "4. miei (sono miei)\n"
        "5. il suo / le sue\n"
        "6. mia\n"
        "7. la tua\n"
        "8. il Suo\n"
        "9. i suoi\n"
        "10. i tuoi"
    )
})

# ── Esercizio 6 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 6 — Come il precedente (possessivi):",
    "pergunta": (
        "1. A che ora verranno ___ amici, Giulio?\n"
        "2. Prendi ___ macchina o vai in moto con Gino?\n"
        "3. Puoi prestare un paio delle ___ scarpe a Chiara?\n"
        "4. Michela ha un gatto molto bello: ___ gatto ha il pelo nero.\n"
        "5. Vuoi vedere ___ giardino? Quello che abbiamo dietro ___ casa?\n"
        "6. Parla spesso di ___ padre e dei ___ nonni.\n"
        "7. Signora, ho incontrato ___ marito con ___ figli.\n"
        "8. Giorgio, ___ idee sono un po' strane.\n"
        "9. Andiamo a casa ___, Carlo!\n"
        "10. Ho ascoltato ___ discorsi e sono sicuro che avete torto."
    ),
    "resposta": (
        "1. i tuoi\n"
        "2. la tua\n"
        "3. mie\n"
        "4. il suo\n"
        "5. il nostro / la nostra\n"
        "6. suo / i suoi\n"
        "7. Suo / i Suoi\n"
        "8. le tue\n"
        "9. nostra (a casa nostra)\n"
        "10. i vostri"
    )
})

# ── Esercizio 7 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 7 — Completare con il possessivo adatto:",
    "pergunta": (
        "1. Signore, ___ macchina è quella gialla?\n"
        "2. Signorina, sono ___ questi guanti?\n"
        "3. ___ libro di grammatica è buono perché le spiegazioni sono chiare.\n"
        "4. Guido, dove vive ___ famiglia?\n"
        "5. Stasera andiamo a ballare e Daniele porterà anche ___ cugine.\n"
        "6. Ho perso ___ passaporto.\n"
        "7. Signore, non ho capito bene ___ parole.\n"
        "8. Giuseppe, ho visto ___ nuova motocicletta.\n"
        "9. Sono molto ospitali e mi piace molto ___ casa.\n"
        "10. Dottore, ___ figlia è qui."
    ),
    "resposta": (
        "1. la Sua\n"
        "2. i Suoi\n"
        "3. Il mio\n"
        "4. la tua\n"
        "5. le sue\n"
        "6. il mio\n"
        "7. le Sue\n"
        "8. la tua\n"
        "9. la loro\n"
        "10. Sua"
    )
})

# ── Esercizio 8 ──────────────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8 — Volgere al plurale o al singolare:",
    "pergunta": (
        "1. I miei nonni sono arrivati alle sette.\n"
        "2. Laura parla spesso delle sue sorelle.\n"
        "3. Carlo, cerchi il tuo cappotto?\n"
        "4. I loro desideri sono irrealizzabili.\n"
        "5. Io scrivo la mia composizione in italiano e tu scrivi la tua in tedesco.\n"
        "6. Mio zio partirà domani per la Sicilia.\n"
        "7. Vostra sorella è molto graziosa.\n"
        "8. I nostri problemi sono davvero difficili.\n"
        "9. Sono andata al cinema con i tuoi cugini.\n"
        "10. Questo è il suo difetto più grande."
    ),
    "resposta": (
        "1. Mio nonno è arrivato alle sette.\n"
        "2. Laura parla spesso della sua sorella.\n"
        "3. Carlo, cerchi i tuoi cappotti?\n"
        "4. Il loro desiderio è irrealizzabile.\n"
        "5. Io scrivo le mie composizioni... e tu scrivi le tue...\n"
        "6. I miei zii partiranno domani per la Sicilia.\n"
        "7. Le vostre sorelle sono molto graziose.\n"
        "8. Il nostro problema è davvero difficile.\n"
        "9. Sono andata al cinema con il tuo cugino.\n"
        "10. Questi sono i suoi difetti più grandi."
    )
})

# ── Vocabolario — Le ore + Lavorare sul testo ─────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Vocabolario sistematico — Che ora è? (rispondere):",
    "pergunta": (
        "Rispondere in forma scritta:\n"
        "1. 06.20 → ?\n"
        "2. 14.30 → ?\n"
        "3. 12.45 → ?\n"
        "4. 05.40 → ?\n"
        "5. 22.15 → ?\n"
        "6. 24.03 → ?"
    ),
    "resposta": (
        "1. Sono le sei e venti (del mattino).\n"
        "2. Sono le due e mezza / le quattordici e trenta.\n"
        "3. È l'una meno un quarto / Sono le dodici e quarantacinque.\n"
        "4. Sono le sei meno venti / le cinque e quaranta.\n"
        "5. Sono le dieci e un quarto (di sera) / le ventidue e quindici.\n"
        "6. È mezzanotte e tre."
    )
})

# ── Lavorare sul testo — Un fumatore ─────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lavorare sul testo — 'Un fumatore' (rispondere alle domande):",
    "pergunta": (
        "Mario ha cominciato a fumare da ragazzo; oggi ha trentacinque anni e al giorno fuma "
        "un pacchetto di sigarette forti e senza filtro. Siccome da un po' di tempo la mattina "
        "ha sempre la tosse, è andato dal medico e questo gli ha detto che il fumo è la causa "
        "del suo disturbo. Mario ha seguito i consigli del medico e ha cercato di smettere di "
        "fumare, ma non ci è riuscito in modo definitivo. Prima ha cominciato a comprare delle "
        "sigarette più leggere e ne ha diminuito il numero, poi è passato alla pipa. Quando "
        "uno fuma la pipa non aspira; perciò il fumo non arriva ai polmoni e fa meno male. "
        "Poi, da quando Mario è entrato in un bar e ha visto il suo medico fumare, ha deciso "
        "di concedersi ogni tanto una sigaretta dopo i pasti.\n\n"
        "1. Quando ha cominciato a fumare Mario?\n"
        "2. Quante sigarette fuma al giorno?\n"
        "3. Che tipo di sigarette fuma?\n"
        "4. Perché è andato dal medico?\n"
        "5. Che cosa ha cercato di fare?\n"
        "6. Che cosa ha fatto per smettere di fumare?\n"
        "7. Perché fumare la pipa fa meno male?\n"
        "8. Perché Mario ha deciso di concedersi qualche sigaretta?"
    ),
    "resposta": (
        "1. Da ragazzo.\n"
        "2. Un pacchetto al giorno.\n"
        "3. Forti e senza filtro.\n"
        "4. Perché la mattina aveva sempre la tosse.\n"
        "5. Ha cercato di smettere di fumare.\n"
        "6. Ha comprato sigarette più leggere, ha diminuito il numero e poi è passato alla pipa.\n"
        "7. Perché non si aspira, il fumo non arriva ai polmoni.\n"
        "8. Perché ha visto il suo medico fumare."
    )
})

# ════════════════════════════════════════════════════════════════════════════════
# ESERCIZI DI VERIFICA — 20 escolha
# ════════════════════════════════════════════════════════════════════════════════

verifica = [
    # 1
    {"pergunta": "___ amica è simpatica, Roberto.",
     "opcoes": ["Tua", "La tua", "Tuo"],
     "resposta": 0},
    # 2
    {"pergunta": "___ sono questi occhiali?",
     "opcoes": ["Di chi", "A chi", "Da chi"],
     "resposta": 0},
    # 3
    {"pergunta": "Gli zii vendono ___",
     "opcoes": ["la sua casa in campagna.", "la loro casa in campagna.", "sua casa in campagna."],
     "resposta": 1},
    # 4
    {"pergunta": "Tutti questi fogli sono ___",
     "opcoes": ["mie.", "miei.", "di me."],
     "resposta": 1},
    # 5
    {"pergunta": "Questi dischi sono di Marco? Sì, sono ___",
     "opcoes": ["suoi.", "sui.", "tuoi."],
     "resposta": 0},
    # 6
    {"pergunta": "Che età hanno ___?",
     "opcoes": ["i tui genitori", "tui genitori", "i tuoi genitori"],
     "resposta": 2},
    # 7
    {"pergunta": "Stasera esco con ___",
     "opcoes": ["mii compagni di classe.", "i mii compagni di classe.", "i miei compagni di classe."],
     "resposta": 2},
    # 8
    {"pergunta": "Tutti i miei amici vivono con ___",
     "opcoes": ["i suoi genitori.", "suoi genitori.", "i loro genitori."],
     "resposta": 2},
    # 9
    {"pergunta": "Qual è ___ numero di telefono?",
     "opcoes": ["tuo", "tuoi", "tua"],
     "resposta": 0},
    # 10
    {"pergunta": "___ è più grande di me.",
     "opcoes": ["Il mio fratello", "Mio fratello", "Il fratello di me"],
     "resposta": 1},
    # 11
    {"pergunta": "Come si chiama il padre di Fabio? ___",
     "opcoes": ["Il suo padre si chiama Mario.", "Suo padre si chiama Mario.", "Lo suo padre si chiama Mario."],
     "resposta": 1},
    # 12
    {"pergunta": "___ ha girato tutto il mondo.",
     "opcoes": ["Lo nostro zio", "Nostro zio", "Il nostro zio"],
     "resposta": 1},
    # 13
    {"pergunta": "Vengo volentieri alla vostra festa, ma posso portare anche ___?",
     "opcoes": ["un amico mio", "un amico di me", "un mio amico"],
     "resposta": 2},
    # 14
    {"pergunta": "Vieni ___ a sentire un po' di musica?",
     "opcoes": ["alla mia casa", "a casa mia", "a mia casa"],
     "resposta": 1},
    # 15
    {"pergunta": "Signora, come sta ___?",
     "opcoes": ["il Suo marito", "Suo marito", "il marito Suo"],
     "resposta": 1},
    # 16
    {"pergunta": "___ vivono in campagna.",
     "opcoes": ["I miei nonni", "Miei nonni", "Mii nonni"],
     "resposta": 0},
    # 17
    {"pergunta": "Gianni e Laura sono orfani: ___",
     "opcoes": ["il loro padre è morto due anni fa.", "loro padre è morto due anni fa.", "suo padre è morto due anni fa."],
     "resposta": 0},
    # 18
    {"pergunta": "Lui è un po' testardo: vuole fare tutto ___",
     "opcoes": ["a modo suo.", "al modo suo.", "al suo modo."],
     "resposta": 0},
    # 19
    {"pergunta": "Sono ___ questi guanti?",
     "opcoes": ["tuoi", "tui", "i tui"],
     "resposta": 0},
    # 20
    {"pergunta": "Dalla finestra ___ vedo il giardino di Boboli.",
     "opcoes": ["di mia stanza", "del mia stanza", "della mia stanza"],
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
    ("Mio colore preferito è il verde.",
     "Il mio colore preferito è il verde."),
    ("I signori Rossi invitano i suoi parenti per Natale.",
     "I signori Rossi invitano i loro parenti per Natale."),
    ("Ieri è arrivato un amico di me.",
     "Ieri è arrivato un mio amico."),
    ("La sua cugina è molto carina. (nessun errore se la cugina è di una terza persona)",
     "Corretto, se si riferisce a una terza persona. Ma se ci si riferisce a tu: 'La tua cugina è molto carina.'"),
    ("Di chi è la penna? È di te?",
     "Di chi è la penna? È tua?"),
    ("Carla è uscita con suo ragazzo.",
     "Carla è uscita con il suo ragazzo."),
    ("Miei nipoti sono ancora piccoli.",
     "I miei nipoti sono ancora piccoli."),
    ("Hai dimenticato tuoi appunti sul tavolo.",
     "Hai dimenticato i tuoi appunti sul tavolo."),
    ("Vado alla mia casa.",
     "Vado a casa mia."),
    ("Tua sorellina è molto graziosa. (nessun errore)",
     "Corretto! 'Sorellina' è alterato, quindi mantiene l'articolo: La tua sorellina."),
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
print(f"OK: Lezione VII — I possessivi")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(exercicios)} total (escolha: {n_e}, revelar: {n_r})")
