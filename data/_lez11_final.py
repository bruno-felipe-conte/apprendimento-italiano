import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XI"), None)
if lez is None:
    lez = {"id": "a1-lez11", "num": "Lezione XI", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I pronomi combinati"
lez["subtitulo"] = "Combinazione di pronome indiretto + pronome diretto"

lez["teoria"] = """\
## Un prestito

Giulio chiede a Paolo un grande favore: vuole prendere in prestito la sua macchina da scrivere per qualche giorno, perché la sua non funziona e tra una settimana deve consegnare al professore di storia una relazione dattiloscritta. Paolo dice che gliela presta con piacere, ma non ce l'ha in quel momento: l'ha prestata ad Antonia per battere la sua tesi di laurea. Paolo è sicuro che adesso Antonia non ne ha più bisogno e che può restituirgliela. Giulio chiede se deve telefonarle lui o lo fa Paolo. Paolo propone di telefonarle lui stesso quella sera, coglie l'occasione per parlarle di alcune cose e le chiede di restituirgli la macchina. Giulio è veramente grato: Paolo è sempre generoso con gli altri e dice che l'amicizia serve anche a questo.

---

## I pronomi combinati

Quando un verbo ha **due pronomi** (uno indiretto + uno diretto), si formano i **pronomi combinati**. Il pronome indiretto si trasforma davanti al pronome diretto:

<table class="gram-table gram-table-rich">
<thead>
<tr>
  <th class="gram-art">pron. indiretto</th>
  <th class="gram-art">→ davanti a diretto</th>
  <th class="gram-genere">+ lo</th>
  <th class="gram-genere">+ la</th>
  <th class="gram-genere">+ li</th>
  <th class="gram-genere">+ le</th>
  <th class="gram-genere">+ ne</th>
</tr>
</thead>
<tbody>
<tr><td class="gram-art">mi</td><td class="gram-art">me</td><td><strong>me lo</strong></td><td><strong>me la</strong></td><td><strong>me li</strong></td><td><strong>me le</strong></td><td><strong>me ne</strong></td></tr>
<tr><td class="gram-art">ti</td><td class="gram-art">te</td><td><strong>te lo</strong></td><td><strong>te la</strong></td><td><strong>te li</strong></td><td><strong>te le</strong></td><td><strong>te ne</strong></td></tr>
<tr><td class="gram-art">gli / le / Le</td><td class="gram-art">glie-</td><td><strong>glielo</strong></td><td><strong>gliela</strong></td><td><strong>glieli</strong></td><td><strong>gliele</strong></td><td><strong>gliene</strong></td></tr>
<tr><td class="gram-art">ci</td><td class="gram-art">ce</td><td><strong>ce lo</strong></td><td><strong>ce la</strong></td><td><strong>ce li</strong></td><td><strong>ce le</strong></td><td><strong>ce ne</strong></td></tr>
<tr><td class="gram-art">vi</td><td class="gram-art">ve</td><td><strong>ve lo</strong></td><td><strong>ve la</strong></td><td><strong>ve li</strong></td><td><strong>ve le</strong></td><td><strong>ve ne</strong></td></tr>
</tbody>
</table>

> **Nota:** i pronomi **gli, le, Le** (indiretto 3ª persona) diventano tutti **glie-** e si uniscono al pronome diretto formando **una sola parola**: glielo, gliela, glieli, gliele, gliene.

---

## Osservate — Con verbi servili

Con i verbi servili (**volere / potere / dovere**) il pronome combinato può stare **prima del verbo servile** (separato) oppure **dopo l'infinito** (unito):

| separato | unito |
|---|---|
| Lo zio **me lo** vuole regalare. | Lo zio vuole regalare**melo**. |
| Carlo, **te ne** devo restituire molti. | Carlo, devo restituirt**ene** molti. |
| Signore, **glielo** posso offrire? | Signore, posso offrirg**lielo**? |
| Signorina, **gliene** devo fare alcune. | Signorina, devo fargl**iene** alcune. |
| Paolo **ce la** sa spiegare bene. | Paolo sa spiegarcela bene. |
| **Gliene** devo consegnare alcune. | Devo consegnargliene alcune. |

---

## ATTENZIONE — Pronomi combinati con NE (quantità)

Con **NE** che indica quantità, il participio **concorda** col nome a cui si riferisce NE:

| domanda | risposta |
|---|---|
| Quanti regali gli porti? | Gliene porto **uno** / due / molti. |
| Quante fotografie le fai? | Gliene faccio **una** / due / molte. |
| Quanti regali gli hai portato? | Gliene ho portato **uno** / portati due. |
| Quante fotografie le hai fatto? | Gliene ho fatta **una** / fatte due. |

---

## Conversazione — In una pensione

— Buona sera, signore.
— Buona sera. Avete una camera singola con bagno?
— Quanto tempo si trattiene?
— Quattro o cinque giorni.
— Mi dispiace, ma le camere singole sono tutte occupate. In città c'è la mostra dell'antiquariato e la pensione è quasi al completo; comunque, se Le interessa, abbiamo una camera doppia con bagno.
— Quanto costa?
— Quindici euro quattro centesimi per notte, compresa la prima colazione.
— Va bene, la prendo. C'è anche il telefono?
— Sì, certo, signore. Ha un documento, per favore?
— Sì, ecco a Lei il passaporto.
— Bene, grazie. Questa è la chiave della Sua camera; numero 18, secondo piano. Ha molti bagagli?
— Una valigia e una borsa.
— Se aspetta un attimo, chiamo il facchino.
— Non importa, grazie, le porto io. Dov'è l'ascensore?
— Alle Sue spalle, signore.
— Ah, scusi, un'ultima cosa: a che ora viene servita la colazione?
— Dalle sette e trenta alle nove e mezza, nella sala a destra dell'ascensore. Buona notte, signore.
— Buona notte, grazie.

---

## Vocabolario sistematico — Gli ortaggi e fare la spesa

**Gli ortaggi:** il ravanello, il sedano, la zucca, la carota, il cavolfiore, la lattuga, il cetriolo, l'insalata, la melanzana, la patata, il peperone, il pomodoro, la cipolla, l'aglio, l'asparago, il carciofo, il prezzemolo, il basilico, il rosmarino, la salvia.

**Dove si compra:**
- In **macelleria**: la carne e gli affettati
- Dal **fruttivendolo**: la frutta e la verdura
- In **panetteria**: il pane e la pasta
- In **latteria**: il latte, il burro e lo yogurt
- In **polleria**: le uova e il pollame
- In **pizzicheria**: i formaggi, i salumi e svariati prodotti alimentari
- Dal **vinaio**: il vino
- In **pescheria**: il pesce

---

## Osservare — Espressioni idiomatiche con VOLERCI

Il verbo **volerci** (= essere necessario) si usa per indicare tempo o quantità necessari:

| domanda | risposta singolare | risposta plurale |
|---|---|---|
| Quanto tempo ci vuole per andare da Paolo? | Ci **vuole** un'ora. | Ci **vogliono** quaranta minuti. |
| Quanto tempo c'è voluto per costruire la chiesa? | C'è **voluto** un secolo. | Ci **sono voluti** cento anni. |
| Quanto tempo c'è voluto per fare l'esame? | C'è **voluta** circa un'ora. | Ci **sono volute** circa due ore. |

> Participio passato di **volerci** concorda col soggetto (la quantità/il tempo).
"""

lez["exemplos"] = [
    "Franco mi dà il libro → me lo dà. (mi + lo = me lo)",
    "Franco ti dà la penna → te la dà. (ti + la = te la)",
    "Franco gli/le/Le dà i libri → glieli dà. (gli + li = glieli)",
    "Paolo ce la presta con piacere. (ci + la = ce la)",
    "Gliene devo consegnare alcune. (gli + ne = gliene)",
]

EX = []

# Domande sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Un prestito:\n1. A chi chiede il favore Giulio?\n2. Che cosa chiede a Paolo?\n3. Perché gli chiede questo favore?\n4. Chi ha la macchina da scrivere?\n5. Perché Antonia ne aveva bisogno?\n6. Perché adesso la può restituire a Paolo?\n7. Chi telefonerà ad Antonia?\n8. Perché le telefona Paolo?\n9. Com'è Paolo con gli altri?\n10. A che cosa serve l'amicizia per lui?",
    "resposta": "1. Chiede il favore a Paolo.\n2. Chiede di prestargli la macchina da scrivere.\n3. Perché la sua non funziona e deve consegnare una relazione dattiloscritta.\n4. Antonia ce l'ha (Paolo gliela ha prestata).\n5. Perché ne aveva bisogno per battere la sua tesi di laurea.\n6. Perché ha già finito la tesi.\n7. Telefonerà Paolo (quella sera).\n8. Perché deve parlarle di alcune cose e le chiederà di restituire la macchina.\n9. È sempre generoso con gli altri.\n10. L'amicizia serve anche ad aiutarsi a vicenda.",
    "explicacao": "Comprensione del dialogo. Attenzione all'uso dei pronomi combinati nel testo (gliela, gliene, ecc.)."
})

# Esercizio 1
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Completare con un pronome combinato:\n1. Ho scritto la lettera a Daniela e ___ ho spedit___.\n2. Ho scritto una lettera a Gino e ___ ho spedit___.\n3. Le ho comprato dei dischi e ___ ho portat___ a casa.\n4. Gli ho comprato delle cassette e ___ ho portat___ a casa.\n5. Ho saputo che Giulio ha vinto un premio, ma lui non ___ ha volut___ dire.\n6. Sapevo che era la più bella, ma non ___ ho voluto dir___.\n7. Ho spiegato quella regola a tutti e ___ ho ripetut___ molte volte.\n8. Ho spedito dei regali a tutte, ma non ___ hanno ancora consegnat___.\n9. Mi vuole molto bene, ma non si decide a dir___.\n10. A Carlo gliel'ho già detto, ma dovrò ripetr___ ancora una volta!",
    "resposta": "1. gliela / spedita\n2. gliela / spedita\n3. glieli / portati\n4. gliele / portate\n5. gliel' / voluto (non gliel'ha voluto dire)\n6. gliel' / detto (non gliel'ho voluto dire)\n7. gliel' / ripetuta (gliela ho ripetuta)\n8. gliele / consegnate\n9. dirmelo\n10. ripeterglielo",
    "explicacao": "Pronomi combinati 3ª persona: gli/le + lo/la/li/le/ne → glielo/gliela/glieli/gliele/gliene (sempre uniti)."
})

# Esercizio 2
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Rispondere alle domande con un pronome combinato:\n(Mod.: Chi ti ha regalato questi occhiali? → Me li ha regalati mia sorella.)\n1. Chi ti ha regalato questi occhiali?\n2. Chi vi ha spiegato queste regole?\n3. Chi ti ha mandato questa cartolina?\n4. Chi gli ha offerto la cena?\n5. Chi ti ha spiegato i pronomi?\n6. Chi ci ha portato queste rose?\n7. Chi mi ha fatto questo regalo?\n8. Chi le ha comunicato la notizia?\n9. Chi gli ha chiesto se vogliono uscire?\n10. Chi ti ha dato queste informazioni?",
    "resposta": "1. Me li ha regalati... (mia madre / un amico, ecc.)\n2. Ce le ha spiegate... (il professore)\n3. Me la ha mandata... (un amico)\n4. Gliela ha offerta... (Mario)\n5. Me li ha spiegati... (la professoressa)\n6. Ce le ha portate... (Luisa)\n7. Te lo ha fatto... (tua sorella)\n8. Gliel'ha comunicata... (il direttore)\n9. Gliel'ha chiesto... (Paolo)\n10. Me le ha date... (Carlo)",
    "explicacao": "Risposta libera con pronome combinato. Participio concorda col diretto: -o/a/i/e."
})

# Esercizio 3
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Rispondere con pronome combinato:\n1. Chi vi ha spiegato queste regole?\n2. Chi mi ha preso il dizionario?\n3. Le hai raccontato quel fatto?\n4. Gli hai presentato i tuoi genitori?\n5. Quando le avete spedito l'acconto?\n6. Quando ci avete spedito il pacco?\n7. Le avete chiesto se ha preso lei la mia borsa?\n8. Gli avete chiesto se ha preso lui la mia bicicletta?\n9. Chi ti ha insegnato questo gioco?\n10. Quando ti hanno detto che c'è lo sciopero dell'autobus?",
    "resposta": "1. Ce le ha spiegate il professore.\n2. Te l'ha preso Carlo.\n3. Sì, gliel'ho raccontato.\n4. Sì, glieli ho presentati.\n5. Gliel'abbiamo spedito ieri.\n6. Ve l'abbiamo spedito lunedì.\n7. Sì, gliel'abbiamo chiesto.\n8. Sì, gliel'abbiamo chiesto.\n9. Me l'ha insegnato mio zio.\n10. Me l'hanno detto stamattina.",
    "explicacao": "Forma sempre glielo/gliela/glieli/gliele per 3ª persona (masch., femm., formale). Ce lo/ce la per 1ª plur."
})

# Esercizio 4
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Rispondere alle domande con un pronome combinato:\n1. Le hai spiegato che non la puoi aiutare?\n2. Le hai reso i soldi?\n3. Gli hai restituito i libri?\n4. Le hai regalato tu la collana?\n5. Gli hai prestato tu il dizionario?\n6. Chi vi ha scritto questa cartolina?\n7. Quando ti hanno presentato i loro parenti?\n8. Hai detto a quelle ragazze che qui non si può fumare?\n9. Hai detto a quei ragazzi che qui non si può fumare?\n10. Hai letto a Carlo le tue poesie?\n11. Hai mostrato le foto a Luisa?\n12. Quando ti hanno ritirato il passaporto?",
    "resposta": "1. Sì, gliel'ho spiegato.\n2. Sì, glieli ho resi.\n3. Sì, glieli ho restituiti.\n4. Sì, gliel'ho regalata io.\n5. Sì, gliel'ho prestato io.\n6. Ce l'ha scritta Maria.\n7. Me li hanno presentati ieri.\n8. Sì, gliel'ho detto.\n9. Sì, gliel'ho detto.\n10. Sì, gliele ho lette.\n11. Sì, gliele ho mostrate.\n12. Me l'hanno ritirato la settimana scorsa.",
    "explicacao": "Combinati 3ª pers. sempre con glie-: gliel'(ho), glieli, gliele. Participio concorda con il diretto."
})

# Conversazione
EX.append({
    "tipo": "revelar",
    "pergunta": "**Conversazione — In una pensione**\n\nRispondere alle domande:\n1. Perché le camere singole sono occupate?\n2. Che tipo di camera offre il receptionist?\n3. Quanto costa la camera?\n4. Cosa è compreso nel prezzo?\n5. A che ora viene servita la colazione?",
    "resposta": "1. Perché c'è la mostra dell'antiquariato e la pensione è quasi al completo.\n2. Una camera doppia con bagno.\n3. Quindici euro quattro centesimi per notte.\n4. La prima colazione è compresa.\n5. Dalle sette e trenta alle nove e mezza.",
    "explicacao": "Lessico dell'albergo/pensione. Uso formale di Lei/Le nell'interazione con il receptionist."
})

# Esercizio 5
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Rispondere alle domande con un pronome combinato:\n1. Quante lettere le hai scritto?\n   (rispondere: non ne ho scritta nessuna / ne ho scritta una / ne ho scritte molte)\n2. Quanti libri ti ha dato?\n3. Quante cartoline hai mandato a Maria?\n4. Quante pagine hai letto a Carlo?\n5. Quanti dischi gli hai prestato?",
    "resposta": "1. Non gliene ho scritta nessuna. / Gliene ho scritta una. / Gliene ho scritte molte.\n2. Non me ne ha dato nessuno. / Me ne ha dato uno solo. / Me ne ha dati diversi.\n3. Non gliene ho mandata nessuna. / Gliene ho mandata una. / Gliene ho mandate molte.\n4. Non gliene ho letta nessuna. / Gliene ho lette alcune.\n5. Non gliene ho prestato nessuno. / Gliene ho prestato uno solo. / Gliene ho prestati diversi / tutti.",
    "explicacao": "Gliene + quantità. Participio concorda con il nome: lettera (f.sg.) → scritta; libri (m.pl.) → dati; dischi (m.pl.) → prestati."
})

# Vocabolario + Osservare volerci
EX.append({
    "tipo": "revelar",
    "pergunta": "**Osservare — Volerci**\n\nCompletare con la forma corretta di VOLERCI:\n1. Quanto tempo ___ per imparare l'italiano?\n2. Per costruire quel palazzo ___ tre anni.\n3. Per fare questo esercizio ___ solo dieci minuti.\n4. Quanti soldi ___ per comprare una casa?\n5. Quante ore ___ per arrivare a Roma in treno?",
    "resposta": "1. ci vuole\n2. ci sono voluti\n3. ci vogliono\n4. ci vogliono\n5. ci vogliono",
    "explicacao": "VOLERCI: ci vuole + singolare; ci vogliono + plurale. Passato: c'è voluto/a; ci sono voluti/e (accordo col soggetto)."
})

# Esercizi di verifica (escolha)
verifica = [
    ("Me lo dai?", "Mi lo dai?", "Me la dai?", 0,
     "MI + LO → ME LO. 'Mi lo' non esiste in italiano. L'oggetto è maschile singolare → lo."),
    ("Gliel'ho detto.", "Gli lo ho detto.", "Le lo ho detto.", 0,
     "GLI/LE + LO → GLIELO (una sola parola). Al passato: gliel'ho (con elisione davanti ad h)."),
    ("Te ne ho portati tre.", "Ti ne ho portati tre.", "Te li ho portati tre.", 0,
     "TI + NE → TE NE. 'Ti ne' non esiste. Con quantità si usa NE, non il diretto."),
    ("Ce la ha spiegata.", "Ce l'ha spiegata.", "Ci la ha spiegata.", 1,
     "CE + LA → CE LA; davanti ad ha → elisione: ce l'ha. 'Ci la' non esiste."),
    ("Voglio regalartelo.", "Voglio te lo regalare.", "Voglio ti lo regalare.", 0,
     "Con infinito: pronome unito alla fine. 'Te lo voglio regalare' è anche corretto (prima del servile)."),
    ("Gliene ho portata una.", "Gliene ho portato una.", "Gliene ho portate una.", 0,
     "NE si riferisce a 'lettera' (femm. sing.) → participio: portata. 'Gliene ho portato' solo con maschile."),
    ("Ve li consegnerò domani.", "Vi li consegnerò domani.", "Ve lo consegnerò domani.", 0,
     "VI + LI → VE LI. 'Vi li' non esiste. L'oggetto è plurale maschile → li."),
    ("Posso offrirglielo?", "Posso glielo offrire?", "Entrambe le forme sono corrette.", 2,
     "Con verbi servili: pronome prima del servile (glielo posso offrire) O dopo l'infinito (offrirGLIELO). Entrambe corrette."),
    ("Me ne ha dato due.", "Mi ne ha dato due.", "Me li ha dato due.", 0,
     "MI + NE → ME NE. Con quantità si usa NE. 'Mi ne' non esiste."),
    ("Gliela regalo.", "Gli la regalo.", "Le lo regalo.", 0,
     "GLI/LE + LA → GLIELA (sempre unito). 'Gli la' e 'Le lo' non esistono."),
    ("Te lo devo restituire.", "Ti lo devo restituire.", "Te lo devo restituirlo.", 0,
     "TI + LO → TE LO. Con il servile DEVO: pronome prima (TE LO devo) o dopo infinito (devo restituirTELO)."),
    ("Quante ne hai mangiate?", "Quanti ne hai mangiati?", "Quante le hai mangiate?", 0,
     "NE con quantità femminile (mele): quante NE. Participio concorda: mangiate. Non si usa il diretto LE con quante."),
    ("Ce ne ha parlato molto.", "Ci ne ha parlato molto.", "Ce lo ha parlato molto.", 0,
     "CI + NE → CE NE. 'Ci ne' non esiste. Parlare di qualcosa → NE (non lo)."),
    ("Devo spiegartelo.", "Devo spiegarti lo.", "Ti lo devo spiegare.", 0,
     "TI + LO → unito all'infinito: spiegare+ti+lo = spiegartELO. 'Ti lo devo spiegare' è sbagliato."),
    ("Gliene ho fatte due.", "Gliene ho fatto due.", "Gliele ho fatte due.", 0,
     "NE si riferisce a 'fotografie' (femm. pl.): participio FATTE. 'Fatto' non concorda. Non si usa LE con quantità."),
    ("Non ve ne parlo più.", "Non vi ne parlo più.", "Non ve lo parlo più.", 0,
     "VI + NE → VE NE. Parlare di qualcosa → NE. 'Vi ne' non esiste."),
    ("Me la devi dare.", "Mi la devi dare.", "Me la devi darla.", 0,
     "MI + LA → ME LA. Con servile: ME LA devi dare, oppure devi darMELA. 'Mi la' non esiste."),
    ("Gliel'abbiamo restituita.", "Gli l'abbiamo restituita.", "Gliela abbiamo restituita.", 0,
     "GLIELA + avere → gliel'abbiamo (elisione). Entrambe gliela/gliel' sono accettate, ma gliel' è preferibile davanti a vocale."),
    ("Ce ne andiamo domani.", "Ci ne andiamo domani.", "Ce lo andiamo domani.", 0,
     "Andarsene: CE NE andiamo. È un'espressione idiomatica. 'Ci ne' e 'ce lo' non esistono."),
    ("Te ne do un po'.", "Ti ne do un po'.", "Te lo do un po'.", 0,
     "TI + NE → TE NE. Con quantità indeterminata (un po') si usa NE. 'Ti ne' non esiste."),
]

for a, b, c, r, expl in verifica:
    EX.append({
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la forma corretta:",
        "opcoes": [a, b, c],
        "resposta": r,
        "explicacao": expl
    })

# Trovare gli errori
errori = [
    ("Mi lo ha detto ieri.",
     "Me lo ha detto ieri.",
     "MI + LO → ME LO. 'Mi lo' non esiste: il pronome indiretto cambia davanti al diretto."),
    ("Gli la presto volentieri.",
     "Gliela presto volentieri.",
     "GLI + LA → GLIELA (una sola parola, sempre unita). 'Gli la' non esiste."),
    ("Ti ne ho portato tre.",
     "Te ne ho portati tre.",
     "TI + NE → TE NE. Inoltre il participio concorda con NE: tre oggetti maschili → portaTI."),
    ("Ce l'ho restituito ieri.",
     "Gliel'ho restituito ieri. (se a lui/lei) / Ce l'ha restituita ieri. (se restituire la borsa a noi)",
     "CE + LO si usa per 1ª plurale (a noi). Se il contesto è 3ª pers. va GLIELO. Verificare chi riceve."),
    ("Voglio spiegarti lo.",
     "Voglio spiegartelo.",
     "Con infinito, i pronomi combinati si attaccano entrambi alla fine: spiegare+ti+lo = spiegartELO."),
    ("Non vi lo posso dire.",
     "Non ve lo posso dire. / Non posso dirvelo.",
     "VI + LO → VE LO (prima del servile) oppure dirvELO (dopo l'infinito). 'Vi lo' non esiste."),
    ("Gliene ho portato molte.",
     "Gliene ho portate molte.",
     "NE si riferisce a oggetto femminile plurale (rose/lettere): participio concordato → portaTE."),
    ("Me la ha regalata.",
     "Me l'ha regalata.",
     "ME + LA + ha → me l'ha (elisione obbligatoria della 'a' di 'la' davanti ad 'ha')."),
    ("Ti lo devo restituire.",
     "Te lo devo restituire. / Devo restituirtelo.",
     "TI + LO → TE LO prima del verbo. Oppure unito all'infinito: restituirTELO."),
    ("Ci ne ha parlato tutto il giorno.",
     "Ce ne ha parlato tutto il giorno.",
     "CI + NE → CE NE. 'Ci ne' non esiste in italiano."),
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
