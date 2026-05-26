import json, re, copy

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

# Find modulo A1 and Lezione IV
modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione IV")

lez["titulo"] = "Il passato prossimo"
lez["subtitulo"] = "Come formare e usare il passato prossimo"

lez["teoria"] = """\
## Una gita

**Mario:** Come mai ieri non sei venuto con me e Gigi in campagna?
**Paolo:** Perché sono andato con Anna a fare una gita a Siena e nel senese. Ma tu come hai passato la giornata di ieri?
**Mario:** La mattina ho fatto le solite cose: sono andato al mercato a fare la spesa, ho studiato qualche ora, ho pulito la casa... Insomma, niente di speciale. Poi a pranzo ho mangiato in una piccola trattoria con Laura; quella ragazza che ho conosciuto qualche giorno fa a casa di Pietro.
**Paolo:** Ah, sì, ricordo. Mi sembra molto simpatica, vero?
**Mario:** Sì, è proprio carina.
**Paolo:** Ma allora quando sei andato con Gigi in campagna?
**Mario:** Nel pomeriggio verso le tre, ma all'ora di cena, siamo tornati in città. E voi?
**Paolo:** Noi siamo partiti in macchina la mattina molto presto e siamo arrivati a Siena verso le nove. Abbiamo fatto un giro per la città, abbiamo visitato il Palazzo Pubblico con la torre del Mangia, il duomo e altre belle chiese. Poi abbiamo bevuto qualcosa in un bar, seduti nella splendida piazza del Campo, quella dove ogni anno, in estate, fanno il palio.
**Mario:** Siete rimasti tutto il giorno a Siena?
**Paolo:** No, nel pomeriggio siamo andati a Pienza, una città a sud di Siena, dove c'è un bellissimo Duomo, realizzato nel XV secolo dal Rossellino per il Papa Pio II. Siamo rimasti a Pienza per circa due ore poi abbiamo ripreso la macchina e abbiamo fatto ritorno a casa.

---

## A Il passato prossimo

<table class="gram-table gram-table-rich">
<thead>
<tr><th></th><th colspan="2">presente</th><th colspan="2">passato prossimo</th></tr>
</thead>
<tbody>
<tr>
  <td class="gram-genere">-ARE</td>
  <td>Luigi<br>Anna</td>
  <td>studia il francese<br>compra il pane</td>
  <td>Luigi<br>Anna</td>
  <td>ha studiato il francese<br>ha comprato il pane</td>
</tr>
<tr>
  <td class="gram-genere">-ERE</td>
  <td>Luca<br>Marco</td>
  <td>vende la bicicletta<br>riceve gli amici</td>
  <td>Luca<br>Marco</td>
  <td>ha venduto la bicicletta<br>ha ricevuto gli amici</td>
</tr>
<tr>
  <td class="gram-genere">-IRE</td>
  <td>Paolo<br>Luisa</td>
  <td>parte alle dieci<br>finisce l'esercizio</td>
  <td>Paolo<br>Luisa</td>
  <td>è partito alle dieci<br>ha finito l'esercizio</td>
</tr>
</tbody>
</table>

> **PASSATO PROSSIMO = presente di ESSERE o AVERE + participio passato del verbo**

---

## B Il participio passato (forme regolari)

**-ARE → -ATO &nbsp;&nbsp; -ERE → -UTO &nbsp;&nbsp; -IRE → -ITO**

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th>I -ARE (cambiare)</th><th>II -ERE (vendere)</th><th>III -IRE (partire)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td>ho cambiato</td><td>ho venduto</td><td>sono partito/a</td></tr>
<tr><td class="gram-art">tu</td><td>hai cambiato</td><td>hai venduto</td><td>sei partito/a</td></tr>
<tr><td class="gram-art">lui/lei/Lei</td><td>ha cambiato</td><td>ha venduto</td><td>è partito/a</td></tr>
<tr><td class="gram-art">noi</td><td>abbiamo cambiato</td><td>abbiamo venduto</td><td>siamo partiti/e</td></tr>
<tr><td class="gram-art">voi</td><td>avete cambiato</td><td>avete venduto</td><td>siete partiti/e</td></tr>
<tr><td class="gram-art">loro</td><td>hanno cambiato</td><td>hanno venduto</td><td>sono partiti/e</td></tr>
</tbody>
</table>

---

## C Essere o avere?

**a)** Un verbo **transitivo** forma il passato prossimo con l'ausiliare **avere** e il participio passato del verbo. Un verbo **intransitivo**, invece, con l'ausiliare **essere** e il participio passato del verbo che concorda con il soggetto in genere e numero.

| con AVERE | con ESSERE |
|---|---|
| Giulio **ha mangiato** la pizza | Giulio **è arrivato** presto |
| Anna **ha venduto** la macchina | Anna **è caduta** in terra |
| I ragazzi **hanno capito** tutto | I ragazzi **sono usciti** tardi |
| Le ragazze **hanno cucito** i vestiti | Le ragazze **sono partite** ieri |

**b)** Non tutti i verbi intransitivi formano il passato prossimo con l'ausiliare **essere**: alcuni richiedono **avere**, altri in alcuni casi essere e in altri avere.

> Carlo **ha camminato** / **ha passeggiato** / **ha viaggiato** molto
> ma: Carlo **ha salito** le scale in fretta / Carlo **è salito** in fretta

**c)** In genere i verbi intransitivi che indicano un **movimento o un fatto** (andare, arrivare, nascere, morire, ecc.) vogliono l'ausiliare **essere**, mentre vogliono l'ausiliare **avere** i verbi che indicano un'azione (cenare, piangere, ecc.).

---

## D Participio passato irregolare

<table class="gram-table gram-table-rich">
<thead><tr><th>infinito</th><th>participio</th><th>infinito</th><th>participio</th><th>infinito</th><th>participio</th></tr></thead>
<tbody>
<tr><td>accendere</td><td><strong>acceso</strong></td><td>mettere</td><td><strong>messo</strong></td><td>scegliere</td><td><strong>scelto</strong></td></tr>
<tr><td>aprire</td><td><strong>aperto</strong></td><td>morire</td><td><strong>morto</strong></td><td>scendere</td><td><strong>sceso</strong></td></tr>
<tr><td>bere</td><td><strong>bevuto</strong></td><td>nascere</td><td><strong>nato</strong></td><td>scrivere</td><td><strong>scritto</strong></td></tr>
<tr><td>chiedere</td><td><strong>chiesto</strong></td><td>offrire</td><td><strong>offerto</strong></td><td>spegnere</td><td><strong>spento</strong></td></tr>
<tr><td>chiudere</td><td><strong>chiuso</strong></td><td>perdere</td><td><strong>perso</strong></td><td>spendere</td><td><strong>speso</strong></td></tr>
<tr><td>correre</td><td><strong>corso</strong></td><td>prendere</td><td><strong>preso</strong></td><td>succedere</td><td><strong>successo</strong></td></tr>
<tr><td>dire</td><td><strong>detto</strong></td><td>produrre</td><td><strong>prodotto</strong></td><td>tradurre</td><td><strong>tradotto</strong></td></tr>
<tr><td>essere</td><td><strong>stato</strong></td><td>rendere</td><td><strong>reso</strong></td><td>vedere</td><td><strong>visto</strong></td></tr>
<tr><td>fare</td><td><strong>fatto</strong></td><td>rimanere</td><td><strong>rimasto</strong></td><td>venire</td><td><strong>venuto</strong></td></tr>
<tr><td>giungere</td><td><strong>giunto</strong></td><td>rispondere</td><td><strong>risposto</strong></td><td>vincere</td><td><strong>vinto</strong></td></tr>
<tr><td>leggere</td><td><strong>letto</strong></td><td>rompere</td><td><strong>rotto</strong></td><td>vivere</td><td><strong>vissuto</strong></td></tr>
</tbody>
</table>

---

## E Il passato prossimo riflessivo

Il passato prossimo di un verbo riflessivo (alzarsi, svegliarsi, ecc.) si forma con il presente del verbo **essere** e il participio passato del verbo.

| soggetto | passato prossimo |
|---|---|
| Paolo | si è svegliato presto |
| Laura | si è svegliata presto |
| I bambini | si sono svegliati presto |
| Le bambine | si sono svegliate presto |

---

## F Verbi servili (dovere, potere, volere)

I verbi **dovere, potere** e **volere**, usati come verbi servili (seguiti da un infinito), prendono l'ausiliare del verbo che reggono. Se invece sono usati come verbi indipendenti, prendono l'ausiliare **avere**.

> Laura **ha** studiato la lezione.
> Laura **ha** dovuto (potuto, voluto) studiare la lezione.
> Laura **è** partita ieri mattina.
> Laura **è** dovuta (potuta, voluta) partire ieri mattina.

---

## G Formazione del participio — II coniugazione

| GG → TT | | | NG → NT | | |
|---|---|---|---|---|---|
| leggere | → | **letto** | giungere | → | **giunto** |
| proteggere | → | **protetto** | piangere | → | **pianto** |
| distruggere | → | **distrutto** | spingere | → | **spinto** |

| ND → SO | | | GL → LT | | |
|---|---|---|---|---|---|
| prendere | → | **preso** | scegliere | → | **scelto** |
| scendere | → | **sceso** | sciogliere | → | **sciolto** |
| spendere | → | **speso** | togliere | → | **tolto** |
"""

lez["exemplos"] = [
    "Ieri ho mangiato in una trattoria con Laura.",
    "Siamo partiti la mattina molto presto.",
    "Hai già finito i compiti?",
    "La segretaria ha aperto la porta dell'ufficio.",
    "I signori Gentili sono andati al mare quest'anno.",
]

exercicios = []

# ── Domande sul dialogo ──────────────────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Rispondere alle domande sul dialogo 'Una gita' (risposte complete):",
    "pergunta": (
        "1. Perché Paolo non è andato in campagna con Mario?\n"
        "2. Che cosa ha fatto la mattina Mario?\n"
        "3. Dove ha mangiato a pranzo?\n"
        "4. Com'è Laura?\n"
        "5. Quando è andato in campagna Mario?\n"
        "6. È andato da solo?\n"
        "7. A che ora sono tornati in città?\n"
        "8. Quando sono partiti Anna e Paolo?\n"
        "9. A che ora sono arrivati a Siena?\n"
        "10. Che cosa hanno visitato?\n"
        "11. Come hanno passato il pomeriggio?\n"
        "12. Quanto tempo sono rimasti a Pienza?"
    ),
    "resposta": (
        "1. Perché è andato con Anna a fare una gita a Siena.\n"
        "2. Ha fatto le solite cose: è andato al mercato, ha studiato, ha pulito la casa.\n"
        "3. In una piccola trattoria.\n"
        "4. È molto simpatica / è carina.\n"
        "5. Nel pomeriggio verso le tre.\n"
        "6. No, è andato con Gigi.\n"
        "7. All'ora di cena.\n"
        "8. La mattina molto presto.\n"
        "9. Verso le nove.\n"
        "10. Il Palazzo Pubblico con la torre del Mangia, il duomo e belle chiese.\n"
        "11. Sono andati a Pienza.\n"
        "12. Circa due ore."
    )
})

# ── Esercizio 1 — Volgere al passato prossimo (a–c) ──────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1a — Volgere al passato prossimo (la segretaria):",
    "pergunta": (
        "1. La segretaria arriva a scuola alle otto.\n"
        "2. Apre la porta dell'ufficio.\n"
        "3. Scrive a macchina una lettera.\n"
        "4. Risponde al telefono.\n"
        "5. Dà le informazioni agli studenti.\n"
        "6. Suona la campanella per l'inizio delle lezioni.\n"
        "7. Fa le fotocopie.\n"
        "8. Indica la classe a un nuovo studente."
    ),
    "resposta": (
        "1. La segretaria è arrivata a scuola alle otto.\n"
        "2. Ha aperto la porta dell'ufficio.\n"
        "3. Ha scritto a macchina una lettera.\n"
        "4. Ha risposto al telefono.\n"
        "5. Ha dato le informazioni agli studenti.\n"
        "6. Ha suonato la campanella per l'inizio delle lezioni.\n"
        "7. Ha fatto le fotocopie.\n"
        "8. Ha indicato la classe a un nuovo studente."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1b — Volgere al passato prossimo (il direttore):",
    "pergunta": (
        "1. Il direttore arriva presto a scuola.\n"
        "2. Legge gli appunti sul tavolo.\n"
        "3. Firma alcune lettere.\n"
        "4. Consegna i diplomi agli studenti.\n"
        "5. Telefona all'ambasciata.\n"
        "6. Riceve una nuova studentessa nel suo ufficio.\n"
        "7. Saluta gli studenti.\n"
        "8. Presenta l'insegnante alla classe."
    ),
    "resposta": (
        "1. Il direttore è arrivato presto a scuola.\n"
        "2. Ha letto gli appunti sul tavolo.\n"
        "3. Ha firmato alcune lettere.\n"
        "4. Ha consegnato i diplomi agli studenti.\n"
        "5. Ha telefonato all'ambasciata.\n"
        "6. Ha ricevuto una nuova studentessa nel suo ufficio.\n"
        "7. Ha salutato gli studenti.\n"
        "8. Ha presentato l'insegnante alla classe."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1c — Volgere al passato prossimo (l'insegnante):",
    "pergunta": (
        "1. L'insegnante arriva a scuola alle nove.\n"
        "2. Entra in classe.\n"
        "3. Fa l'appello.\n"
        "4. Spiega una nuova lezione.\n"
        "5. Scrive delle frasi alla lavagna.\n"
        "6. Ripete la spiegazione.\n"
        "7. Risponde alle domande degli studenti.\n"
        "8. Aiuta una studentessa.\n"
        "9. Corregge le frasi sbagliate.\n"
        "10. Assegna i compiti per il giorno dopo."
    ),
    "resposta": (
        "1. L'insegnante è arrivata a scuola alle nove.\n"
        "2. È entrata in classe.\n"
        "3. Ha fatto l'appello.\n"
        "4. Ha spiegato una nuova lezione.\n"
        "5. Ha scritto delle frasi alla lavagna.\n"
        "6. Ha ripetuto la spiegazione.\n"
        "7. Ha risposto alle domande degli studenti.\n"
        "8. Ha aiutato una studentessa.\n"
        "9. Ha corretto le frasi sbagliate.\n"
        "10. Ha assegnato i compiti per il giorno dopo."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1d — Volgere al passato prossimo (Peter):",
    "pergunta": (
        "1. Peter arriva a scuola alle otto e mezza.\n"
        "2. Controlla la posta.\n"
        "3. Chiede un'informazione alla segretaria.\n"
        "4. Va al bar.\n"
        "5. Beve un cappuccino.\n"
        "6. Fuma una sigaretta.\n"
        "7. Legge un giornale italiano.\n"
        "8. Parla con un insegnante.\n"
        "9. Entra in classe.\n"
        "10. Saluta i suoi compagni.\n"
        "11. Mette i libri e i quaderni sul tavolo.\n"
        "12. Si siede vicino alla cattedra."
    ),
    "resposta": (
        "1. Peter è arrivato a scuola alle otto e mezza.\n"
        "2. Ha controllato la posta.\n"
        "3. Ha chiesto un'informazione alla segretaria.\n"
        "4. È andato al bar.\n"
        "5. Ha bevuto un cappuccino.\n"
        "6. Ha fumato una sigaretta.\n"
        "7. Ha letto un giornale italiano.\n"
        "8. Ha parlato con un insegnante.\n"
        "9. È entrato in classe.\n"
        "10. Ha salutato i suoi compagni.\n"
        "11. Ha messo i libri e i quaderni sul tavolo.\n"
        "12. Si è seduto vicino alla cattedra."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1e — Volgere al passato prossimo (il signor Müller):",
    "pergunta": (
        "1. Il signor Müller passeggia per le strade di Firenze.\n"
        "2. Visita una chiesa e un museo.\n"
        "3. Fa delle fotografie.\n"
        "4. Si siede in un caffè per riposarsi.\n"
        "5. Ordina una birra.\n"
        "6. Legge la guida della città.\n"
        "7. Scrive delle cartoline.\n"
        "8. Paga il conto.\n"
        "9. Si alza dopo poco.\n"
        "10. Torna in albergo."
    ),
    "resposta": (
        "1. Il signor Müller ha passeggiato per le strade di Firenze.\n"
        "2. Ha visitato una chiesa e un museo.\n"
        "3. Ha fatto delle fotografie.\n"
        "4. Si è seduto in un caffè per riposarsi.\n"
        "5. Ha ordinato una birra.\n"
        "6. Ha letto la guida della città.\n"
        "7. Ha scritto delle cartoline.\n"
        "8. Ha pagato il conto.\n"
        "9. Si è alzato dopo poco.\n"
        "10. È tornato in albergo."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1f — Volgere al passato prossimo (la signorina Brown in banca):",
    "pergunta": (
        "1. La signorina Brown va in banca per cambiare un assegno.\n"
        "2. Fa la fila davanti allo sportello.\n"
        "3. Parla con l'impiegato.\n"
        "4. Firma l'assegno.\n"
        "5. Mostra il passaporto.\n"
        "6. Riceve il denaro.\n"
        "7. Lo mette nella borsetta.\n"
        "8. Ringrazia l'impiegato.\n"
        "9. Saluta.\n"
        "10. Esce dalla banca."
    ),
    "resposta": (
        "1. La signorina Brown è andata in banca per cambiare un assegno.\n"
        "2. Ha fatto la fila davanti allo sportello.\n"
        "3. Ha parlato con l'impiegato.\n"
        "4. Ha firmato l'assegno.\n"
        "5. Ha mostrato il passaporto.\n"
        "6. Ha ricevuto il denaro.\n"
        "7. Lo ha messo nella borsetta.\n"
        "8. Ha ringraziato l'impiegato.\n"
        "9. Ha salutato.\n"
        "10. È uscita dalla banca."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 1g — Volgere al passato prossimo (Marco e Giulia al ristorante):",
    "pergunta": (
        "1. Marco e Giulia vanno al ristorante.\n"
        "2. Si siedono a un tavolo vicino alla finestra.\n"
        "3. Marco chiede la lista al cameriere.\n"
        "4. Il cameriere consiglia il vino della casa.\n"
        "5. Marco e Giulia ordinano il primo e il secondo.\n"
        "6. Giulia prende anche il contorno.\n"
        "7. Marco e Giulia mangiano con gusto.\n"
        "8. Finiscono la cena con un dolce.\n"
        "9. Pagano il conto.\n"
        "10. Lasciano la mancia al cameriere.\n"
        "11. Marco e Giulia escono dal ristorante."
    ),
    "resposta": (
        "1. Marco e Giulia sono andati al ristorante.\n"
        "2. Si sono seduti a un tavolo vicino alla finestra.\n"
        "3. Marco ha chiesto la lista al cameriere.\n"
        "4. Il cameriere ha consigliato il vino della casa.\n"
        "5. Marco e Giulia hanno ordinato il primo e il secondo.\n"
        "6. Giulia ha preso anche il contorno.\n"
        "7. Marco e Giulia hanno mangiato con gusto.\n"
        "8. Hanno finito la cena con un dolce.\n"
        "9. Hanno pagato il conto.\n"
        "10. Hanno lasciato la mancia al cameriere.\n"
        "11. Marco e Giulia sono usciti dal ristorante."
    )
})

# ── Esercizio 2 — Volgere al passato prossimo (frasi libere) ─────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 2 — Volgere al passato prossimo:",
    "pergunta": (
        "1. Dove (voi andare) ieri sera?\n"
        "2. Marco (tornare) tardi dal concerto.\n"
        "3. Anna (partire) da Milano alle tre ed (arrivare) a Zurigo alle dieci.\n"
        "4. Ieri gli studenti (fare) molti esercizi e (capire) il passato prossimo.\n"
        "5. Lo scorso fine-settimana (noi rimanere) a casa.\n"
        "6. (Noi andare) al mare, (fare) il bagno e (prendere) il sole.\n"
        "7. Cosa (tu mangiare) ieri sera a casa di Emanuela?\n"
        "8. Questa mattina (noi venire) a scuola a piedi.\n"
        "9. Chi (accendere) la luce del bagno?\n"
        "10. Quante sigarette (tu fumare) ieri?\n"
        "11. Marco (dimenticarsi) di chiudere la porta.\n"
        "12. Anna (svegliarsi) alle otto."
    ),
    "resposta": (
        "1. Dove siete andati ieri sera?\n"
        "2. Marco è tornato tardi dal concerto.\n"
        "3. Anna è partita da Milano alle tre ed è arrivata a Zurigo alle dieci.\n"
        "4. Ieri gli studenti hanno fatto molti esercizi e hanno capito il passato prossimo.\n"
        "5. Lo scorso fine-settimana siamo rimasti a casa.\n"
        "6. Siamo andati al mare, abbiamo fatto il bagno e abbiamo preso il sole.\n"
        "7. Cosa hai mangiato ieri sera a casa di Emanuela?\n"
        "8. Questa mattina siamo venuti a scuola a piedi.\n"
        "9. Chi ha acceso la luce del bagno?\n"
        "10. Quante sigarette hai fumato ieri?\n"
        "11. Marco si è dimenticato di chiudere la porta.\n"
        "12. Anna si è svegliata alle otto."
    )
})

# ── Esercizio 3 — Come il precedente ─────────────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 3 — Volgere al passato prossimo:",
    "pergunta": (
        "1. (Noi aprire) la finestra perché fa caldo.\n"
        "2. Fabrizio (avere) mal di testa per tutto il pomeriggio.\n"
        "3. (Voi dare) le chiavi della macchina a Marco?\n"
        "4. Il pittore che (dipingere) questo quadro è molto famoso.\n"
        "5. (Tu decidere) cosa fare durante il fine-settimana?\n"
        "6. Dove (voi conoscere) Carlo e Donatella?\n"
        "7. (Tu cucinare) la carne che (io comprare)?\n"
        "8. (Telefonare) Luigi a suo padre?\n"
        "9. (Noi andare) a trovare Silvio.\n"
        "10. Anna (dire) che questo disco è bello.\n"
        "11. Giancarlo e Sara (comprare) una macchina nuova.\n"
        "12. Giovanna (prestare) un libro a Enrico."
    ),
    "resposta": (
        "1. Abbiamo aperto la finestra perché fa caldo.\n"
        "2. Fabrizio ha avuto mal di testa per tutto il pomeriggio.\n"
        "3. Avete dato le chiavi della macchina a Marco?\n"
        "4. Il pittore che ha dipinto questo quadro è molto famoso.\n"
        "5. Hai deciso cosa fare durante il fine-settimana?\n"
        "6. Dove avete conosciuto Carlo e Donatella?\n"
        "7. Hai cucinato la carne che ho comprato?\n"
        "8. Luigi ha telefonato a suo padre?\n"
        "9. Siamo andati a trovare Silvio.\n"
        "10. Anna ha detto che questo disco è bello.\n"
        "11. Giancarlo e Sara hanno comprato una macchina nuova.\n"
        "12. Giovanna ha prestato un libro a Enrico."
    )
})

# ── Esercizio 4 — Volgere al passato prossimo ────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 4 — Volgere al passato prossimo:",
    "pergunta": (
        "1. (Io dare) a Giovanni un pacchetto di sigarette.\n"
        "2. (Noi pulire) tutta la casa prima del tuo arrivo.\n"
        "3. (Tu leggere) il libro che (io comprare) in quella libreria del centro?\n"
        "4. Giacomo (vedere) quel film e (dire) che è molto bello.\n"
        "5. Dove (voi mettere) le mie fotografie?\n"
        "6. Molti soldati (morire) durante la guerra.\n"
        "7. (Io ascoltare) volentieri questo disco.\n"
        "8. In questi giorni (io scrivere) molto.\n"
        "9. Con chi (tu uscire) domenica?\n"
        "10. (Tu offrire) il caffè alla signora Rossi?\n"
        "11. Lui e Marco (nascere) in Toscana.\n"
        "12. (Noi prendere) il treno per Roma."
    ),
    "resposta": (
        "1. Ho dato a Giovanni un pacchetto di sigarette.\n"
        "2. Abbiamo pulito tutta la casa prima del tuo arrivo.\n"
        "3. Hai letto il libro che ho comprato in quella libreria del centro?\n"
        "4. Giacomo ha visto quel film e ha detto che è molto bello.\n"
        "5. Dove avete messo le mie fotografie?\n"
        "6. Molti soldati sono morti durante la guerra.\n"
        "7. Ho ascoltato volentieri questo disco.\n"
        "8. In questi giorni ho scritto molto.\n"
        "9. Con chi sei uscito domenica?\n"
        "10. Hai offerto il caffè alla signora Rossi?\n"
        "11. Lui e Marco sono nati in Toscana.\n"
        "12. Abbiamo preso il treno per Roma."
    )
})

# ── Conversazione — In banca + Un'informazione ────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Conversazione — In banca (leggere e praticare il dialogo):",
    "pergunta": (
        "Cliente: Scusi, è questo l'ufficio di cambio?\n"
        "Impiegato: No, signore, deve andare più avanti allo sportello numero sei.\n"
        "Cliente: Va bene, grazie. Buongiorno, signore.\n"
        "Impiegato: Buongiorno. Per favore, qual è la quotazione del dollaro americano oggi?\n"
        "Cliente: Settantadue centesimi.\n"
        "Impiegato: Vorrei cambiare trecento dollari. Ha un documento?\n"
        "Cliente: Ho il passaporto.\n"
        "Impiegato: Bene, grazie. Ecco a Lei gli euro.\n\n"
        "— — —\n\n"
        "Gianni: Scusi signora, vorrei un'informazione... Devo andare alla stazione, è lontano da qui?\n"
        "Signora: No, non troppo, se vuole può andare anche a piedi.\n"
        "Gianni: Che strada devo fare?\n"
        "Signora: Deve andare sempre dritto in questa direzione, poi, al primo incrocio, girare a destra e infine, alla seconda traversa, a sinistra. Quando vede davanti a sé un grande edificio antico, è arrivato.\n"
        "Gianni: Grazie tante. È stata molto gentile... Ma posso raggiungere la stazione anche con l'autobus?\n"
        "Signora: Sì, certo. Può prendere l'autobus numero dodici; la fermata è davanti a quel bar.\n"
        "Gianni: Grazie di nuovo, arrivederLa."
    ),
    "resposta": "Dialogo sulla conversazione in banca e per chiedere informazioni stradali."
})

# ── Vocabolario sistematico — Le stagioni + I numeri ─────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Vocabolario sistematico — Le stagioni dell'anno:",
    "pergunta": (
        "Le stagioni dell'anno sono quattro: l'inverno, la primavera, l'estate e l'autunno.\n\n"
        "In inverno fa freddo; il cielo è quasi sempre nuvoloso, piove e cade la neve.\n"
        "In primavera la campagna diventa verde; il cielo è sereno e spesso tira vento.\n"
        "In estate fa caldo; il tempo è quasi sempre bello e le giornate sono lunghe.\n"
        "In autunno cadono le foglie dagli alberi; cominciano i primi temporali e l'aria è fresca.\n\n"
        "Rispondere:\n"
        "- Quante sono le stagioni dell'anno?\n"
        "- In quale stagione siamo ora?\n"
        "- Nel nostro emisfero, quali sono i mesi invernali? E primaverili? Estivi? Autunnali?\n"
        "- Com'è il tempo nelle differenti stagioni?"
    ),
    "resposta": (
        "Le stagioni sono quattro.\n"
        "Mesi invernali: dicembre, gennaio, febbraio.\n"
        "Primaverili: marzo, aprile, maggio.\n"
        "Estivi: giugno, luglio, agosto.\n"
        "Autunnali: settembre, ottobre, novembre."
    )
})

# ── Esercizio 6 — Volgere al passato prossimo ────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 6 — Volgere al passato prossimo:",
    "pergunta": (
        "1. (Prendere) tu le nostre riviste?\n"
        "2. (Voi rimanere) molto tempo a Siena?\n"
        "3. Luisa, (perdere) veramente le chiavi di casa?\n"
        "4. (Noi non andare) a teatro perché John e Susan (arrivare) dagli Stati Uniti.\n"
        "5. (Lei sapere) solo ieri del disastro aereo.\n"
        "6. Quale vestito (tu scegliere)?\n"
        "7. (Io comprare) quello blu di Jana.\n"
        "8. Franze Karen (rispondere) a tutte le domande.\n"
        "9. Chi (rompere) il vaso di porcellana?\n"
        "10. Dove (voi stare) per tutto questo tempo?\n"
        "11. (Io venire) in centro con la macchina di Franco.\n"
        "12. Luca (cadere) dalla bicicletta."
    ),
    "resposta": (
        "1. Hai preso le nostre riviste?\n"
        "2. Siete rimasti molto tempo a Siena?\n"
        "3. Luisa, hai perso veramente le chiavi di casa?\n"
        "4. Non siamo andati a teatro perché John e Susan sono arrivati dagli Stati Uniti.\n"
        "5. Lei ha saputo solo ieri del disastro aereo.\n"
        "6. Quale vestito hai scelto?\n"
        "7. Ho comprato quello blu di Jana.\n"
        "8. Franze Karen ha risposto a tutte le domande.\n"
        "9. Chi ha rotto il vaso di porcellana?\n"
        "10. Dove siete stati per tutto questo tempo?\n"
        "11. Sono venuto in centro con la macchina di Franco.\n"
        "12. Luca è caduto dalla bicicletta."
    )
})

# ── Esercizio 7 — Come il precedente (forme irregolari avanzate) ──────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 7 — Volgere al passato prossimo (participi irregolari):",
    "pergunta": (
        "1. (Io leggere) questo libro da bambino.\n"
        "2. La bomba (distruggere) l'ambasciata.\n"
        "3. (Loro non proteggere) i loro amici.\n"
        "4. Chi (vincere) la partita?\n"
        "5. Anna (togliersi) la giacca.\n"
        "6. (Noi lavarsi) i capelli.\n"
        "7. Il tuo amico (non bere) molto vino.\n"
        "8. Quella bambina (piangere) molto.\n"
        "9. Mario (dipingere) un bel quadro.\n"
        "10. Dove (tu nascere)?\n"
        "11. (Accendere) voi la luce?\n"
        "12. Ragazzi, (spegnere) la TV?\n"
        "13. Chi (dividere) la torta in questo modo?\n"
        "14. Quando (io raccontare) questa storiella, tutti (ridere).\n"
        "15. (Io non decidere) ancora cosa fare.\n"
        "16. L'Italia (produrre) molte auto in questi ultimi anni.\n"
        "17. Gli studenti (non tradurre) le frasi.\n"
        "18. Lei (promettere) di venire alla festa."
    ),
    "resposta": (
        "1. Ho letto questo libro da bambino.\n"
        "2. La bomba ha distrutto l'ambasciata.\n"
        "3. Non hanno protetto i loro amici.\n"
        "4. Chi ha vinto la partita?\n"
        "5. Anna si è tolta la giacca.\n"
        "6. Ci siamo lavati i capelli.\n"
        "7. Il tuo amico non ha bevuto molto vino.\n"
        "8. Quella bambina ha pianto molto.\n"
        "9. Mario ha dipinto un bel quadro.\n"
        "10. Dove sei nato/a?\n"
        "11. Avete acceso voi la luce?\n"
        "12. Ragazzi, avete spento la TV?\n"
        "13. Chi ha diviso la torta in questo modo?\n"
        "14. Quando ho raccontato questa storiella, tutti hanno riso.\n"
        "15. Non ho ancora deciso cosa fare.\n"
        "16. L'Italia ha prodotto molte auto in questi ultimi anni.\n"
        "17. Gli studenti non hanno tradotto le frasi.\n"
        "18. Lei ha promesso di venire alla festa."
    )
})

# ── Esercizio 8 — Preposizioni (da / fra / fa / per / in) ────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8A — Preposizioni con 'da' (tempo continuato):\nMod.: Da quanto abiti a Firenze? (due giorni) → Abito a Firenze da due giorni.",
    "pergunta": (
        "1. Da quanto tempo studi l'italiano? (un mese)\n"
        "2. Da quanto tempo hai la febbre? (due giorni)\n"
        "3. Da quanto tempo alloggi in quell'hotel? (pochi giorni)\n"
        "4. Da quanto tempo conosci Luisa? (molti anni)"
    ),
    "resposta": (
        "1. Studio l'italiano da un mese.\n"
        "2. Ho la febbre da due giorni.\n"
        "3. Alloggio in quell'hotel da pochi giorni.\n"
        "4. Conosco Luisa da molti anni."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8B — Preposizioni con 'fra' (futuro):\nMod.: Quando parti? (un'ora) → Parto fra un'ora.",
    "pergunta": (
        "1. Quando finisce la lezione? (tre ore)\n"
        "2. Quando ritorna Laura? (due giorni)\n"
        "3. Quando arriva tua madre? (dieci minuti)\n"
        "4. Quando pranziamo? (un attimo)"
    ),
    "resposta": (
        "1. La lezione finisce fra tre ore.\n"
        "2. Laura ritorna fra due giorni.\n"
        "3. Mia madre arriva fra dieci minuti.\n"
        "4. Pranziamo fra un attimo."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8C — Preposizioni con 'fa' (passato):\nMod.: Quando sei arrivata? (un'ora) → Sono arrivata un'ora fa.",
    "pergunta": (
        "1. Quando è partita Isabella? (tre giorni)\n"
        "2. Quando hai avuto quell'incidente? (due mesi)\n"
        "3. Quando avete ricevuto il telegramma? (mezz'ora)\n"
        "4. Quando è morto tuo nonno? (tre anni)"
    ),
    "resposta": (
        "1. Isabella è partita tre giorni fa.\n"
        "2. Ho avuto quell'incidente due mesi fa.\n"
        "3. Abbiamo ricevuto il telegramma mezz'ora fa.\n"
        "4. Mio nonno è morto tre anni fa."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8D — Preposizioni con 'per' (durata):\nMod.: Per quanto tempo hai abitato a Bonn? (dieci anni) → Ho abitato a Bonn per dieci anni.",
    "pergunta": (
        "1. Per quanto tempo hai frequentato l'università? (sei anni)\n"
        "2. Per quanto tempo hai aspettato Lucia? (più di un'ora)\n"
        "3. Per quanto tempo hanno vissuto insieme? (dieci anni)\n"
        "4. Per quanto tempo siete rimasti in casa? (tutto il giorno)"
    ),
    "resposta": (
        "1. Ho frequentato l'università per sei anni.\n"
        "2. Ho aspettato Lucia per più di un'ora.\n"
        "3. Hanno vissuto insieme per dieci anni.\n"
        "4. Siamo rimasti in casa per tutto il giorno."
    )
})

exercicios.append({
    "tipo": "revelar",
    "enunciado": "Esercizio 8E — Preposizioni con 'in' (durata dell'azione):\nMod.: In quanto tempo hai fatto il lavoro? (due ore) → Ho fatto il lavoro in due ore.",
    "pergunta": (
        "1. In quanto tempo hai fatto i compiti? (un'ora)\n"
        "2. In quanto tempo Carlo ha finito il lavoro? (una settimana)\n"
        "3. In quanto tempo il meccanico ha riparato la macchina? (due giorni)\n"
        "4. In quanto tempo hai dipinto questo quadro? (poche ore)"
    ),
    "resposta": (
        "1. Ho fatto i compiti in un'ora.\n"
        "2. Carlo ha finito il lavoro in una settimana.\n"
        "3. Il meccanico ha riparato la macchina in due giorni.\n"
        "4. Ho dipinto questo quadro in poche ore."
    )
})

# ── Lavorare sul testo — In vacanza al mare ───────────────────────────────────
exercicios.append({
    "tipo": "revelar",
    "enunciado": "Lavorare sul testo — 'In vacanza al mare' (rispondere alle domande):",
    "pergunta": (
        "I signori Gentili di solito passano le vacanze estive in montagna, ma quest'anno hanno "
        "deciso di andare in villeggiatura al mare. Per tutto il mese di luglio hanno preso in "
        "affitto una villetta in una località balneare vicino a Genova. Un sabato mattina, dopo "
        "lunghi preparativi, sono partiti da Firenze con la macchina carica di bagagli: valigie, "
        "sedie a sdraio, racchette da tennis e ombrellone. Dopo un viaggio piuttosto faticoso, "
        "a causa del traffico intenso e del caldo, sono arrivati a destinazione. Dopo che hanno "
        "sistemato tutte le loro cose nella villetta, sono andati alla spiaggia: hanno preso il "
        "sole, hanno fatto il bagno, hanno letto il giornale sotto l'ombrellone e infine, verso "
        "le due, sono tornati a casa per preparare il pranzo, soddisfatti del loro primo giorno "
        "al mare.\n\n"
        "1. Dove passano di solito le vacanze i signori Gentili?\n"
        "2. Dove hanno deciso di andare quest'anno?\n"
        "3. Che cosa hanno preso in affitto?\n"
        "4. Quando sono partiti da Firenze?\n"
        "5. Com'è stato il viaggio? Perché?\n"
        "6. Quando sono andati alla spiaggia?\n"
        "7. Come hanno passato la mattina?\n"
        "8. Perché sono tornati a casa verso le due?\n"
        "9. Hanno passato una bella mattinata?\n\n"
        "Attività scritta: Trascrivere il testo alla prima persona singolare.\n"
        "Mod.: Io di solito passo le vacanze..."
    ),
    "resposta": (
        "1. Di solito in montagna.\n"
        "2. Al mare, in villeggiatura vicino a Genova.\n"
        "3. Una villetta in una località balneare.\n"
        "4. Un sabato mattina.\n"
        "5. È stato faticoso, a causa del traffico intenso e del caldo.\n"
        "6. Dopo aver sistemato le cose nella villetta.\n"
        "7. Hanno preso il sole, fatto il bagno, letto il giornale.\n"
        "8. Per preparare il pranzo.\n"
        "9. Sì, sono tornati soddisfatti."
    )
})

# ════════════════════════════════════════════════════════════════════════════════
# ESERCIZI DI VERIFICA (escolha) — 22 domande
# ════════════════════════════════════════════════════════════════════════════════

verifica = [
    # 1
    {"pergunta": "Scusa, puoi ripetere, ___",
     "opcoes": ["non ho capito bene.", "non sono capito bene.", "non è capito bene."],
     "resposta": 0},
    # 2
    {"pergunta": "Mio padre ___",
     "opcoes": ["ha andato dal dottore.", "è andato dal dottore.", "sono andato dal dottore."],
     "resposta": 1},
    # 3
    {"pergunta": "Dove ___ in vacanza?",
     "opcoes": ["hai stato", "sei stato", "ha stato"],
     "resposta": 1},
    # 4
    {"pergunta": "A che ora ___, Carla?",
     "opcoes": ["hai partito", "sei partito", "sei partita"],
     "resposta": 2},
    # 5
    {"pergunta": "I miei amici ___",
     "opcoes": ["sono arrivati.", "hanno arrivato.", "sono arrivate."],
     "resposta": 0},
    # 6
    {"pergunta": "___ ieri sera?",
     "opcoes": ["Hai uscito", "Sei uscito", "Ho uscito"],
     "resposta": 1},
    # 7
    {"pergunta": "Dove ___, signora?",
     "opcoes": ["ha nato", "sei nata", "è nata"],
     "resposta": 2},
    # 8
    {"pergunta": "Quando ___ a casa?",
     "opcoes": ["siete tornati", "avete tornato"],
     "resposta": 0},
    # 9
    {"pergunta": "È tardi. Il film ___",
     "opcoes": ["è già finito.", "ha già finito."],
     "resposta": 0},
    # 10
    {"pergunta": "___ i soldi.",
     "opcoes": ["Sono finiti", "Ho finito"],
     "resposta": 0},
    # 11
    {"pergunta": "Quando ___ a studiare l'italiano?",
     "opcoes": ["hai cominciato", "sei cominciato"],
     "resposta": 0},
    # 12
    {"pergunta": "Lo spettacolo ___",
     "opcoes": ["è già iniziato.", "ha già iniziato."],
     "resposta": 0},
    # 13
    {"pergunta": "___ questo libro.",
     "opcoes": ["Non ho leggiuto", "Non ho letto", "Non sono letto"],
     "resposta": 1},
    # 14
    {"pergunta": "___ la finestra perché fa caldo.",
     "opcoes": ["Abbiamo aperto", "Siamo apriti", "Abbiamo aprito"],
     "resposta": 0},
    # 15
    {"pergunta": "___ un anno in Italia per imparare la lingua.",
     "opcoes": ["È rimanuta", "Ha rimanuto", "È rimasta"],
     "resposta": 2},
    # 16
    {"pergunta": "Ieri pomeriggio ___",
     "opcoes": ["ho camminato molto.", "sono camminato molto."],
     "resposta": 0},
    # 17
    {"pergunta": "La signora ___",
     "opcoes": ["ha offrito un caffè a tutti.", "ha offerto un caffè a tutti.", "è offerta un caffè a tutti."],
     "resposta": 1},
    # 18
    {"pergunta": "___ alla sua lettera.",
     "opcoes": ["Non ho ancora risponduto", "Non sono ancora risposto", "Non ho ancora risposto"],
     "resposta": 2},
    # 19
    {"pergunta": "Che cosa ___ ieri sera?",
     "opcoes": ["ha successo", "è successo", "è succeduto"],
     "resposta": 1},
    # 20
    {"pergunta": "___ il tuo nome e cognome?",
     "opcoes": ["Hai scrivuto", "Hai scritto", "Sei scritto"],
     "resposta": 1},
    # 21
    {"pergunta": "Mio padre ___",
     "opcoes": ["ha morto cinque anni fa.", "è morto cinque anni fa."],
     "resposta": 1},
    # 22
    {"pergunta": "___ di fare una vacanza studio a Firenze.",
     "opcoes": ["Ho deciduto", "Ho deciso", "Sono deciduto"],
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

# ════════════════════════════════════════════════════════════════════════════════
# TROVARE GLI ERRORI (revelar) — 10 frasi
# ════════════════════════════════════════════════════════════════════════════════

errori = [
    ("Hai renduto i soldi a Gianni?",
     "Hai reso i soldi a Gianni?"),
    ("È vivuto tre anni negli Stati Uniti.",
     "È vissuto tre anni negli Stati Uniti."),
    ("Ho passato alla banca e ho cambiato i soldi.",
     "Sono passato alla banca e ho cambiato i soldi."),
    ("Sono passato una bella vacanza in Francia.",
     "Ho passato una bella vacanza in Francia."),
    ("Il treno è giunguto in ritardo.",
     "Il treno è giunto in ritardo."),
    ("Hai chiuduto bene la porta?",
     "Hai chiuso bene la porta?"),
    ("Il tempo ha diventato brutto: piove e fa freddo.",
     "Il tempo è diventato brutto: piove e fa freddo."),
    ("Da quanto ha cominciato la partita?",
     "Da quanto tempo è cominciata la partita?"),
    ("Ho studiato italiano da due settimane.",
     "Studio italiano da due settimane. (azione in corso → presente + da)"),
    ("Dove hai mettuto il giornale?",
     "Dove hai messo il giornale?"),
]

for i, (frase, corretta) in enumerate(errori, 23):
    exercicios.append({
        "tipo": "revelar",
        "enunciado": f"Trovare l'errore ({i}):",
        "pergunta": frase,
        "resposta": corretta
    })

lez["exercicios"] = exercicios

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

n_escolha = sum(1 for e in exercicios if e["tipo"] == "escolha")
n_revelar = sum(1 for e in exercicios if e["tipo"] == "revelar")
print(f"OK: Lezione IV — Il passato prossimo")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exemplos: {len(lez['exemplos'])}")
print(f"Exercicios: {len(exercicios)} total (escolha: {n_escolha}, revelar: {n_revelar})")
