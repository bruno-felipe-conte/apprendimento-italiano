import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XII"), None)
if lez is None:
    lez = {"id": "a1-lez12", "num": "Lezione XII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I verbi riflessivi"
lez["subtitulo"] = "Verbi riflessivi propri, reciproci e forma impersonale"

lez["teoria"] = """\
## A letto con l'influenza

Laura ha l'influenza e deve stare a letto. Stamattina si è svegliata tardi, si è alzata lentamente, si è lavata e si è guardata allo specchio: era pallida e aveva il naso rosso. Si è sentita subito molto stanca e si è rimessa a letto. Sua madre le ha portato una tazza di tè caldo. Laura si è addormentata di nuovo e si è svegliata verso mezzogiorno. Nel pomeriggio, mentre si annoiava, ha chiamato la sua amica Carla per lamentarsi della sua situazione. Carla si è messa a ridere e le ha detto che si sarebbe rimessa presto. Poi le due amiche si sono messe a chiacchierare per un po'. La sera, Laura si è sentita meglio e ha potuto mangiare qualcosa. Poi si è lavata i denti, si è tolta il pigiama e si è addormentata di nuovo.

---

## A I verbi riflessivi

I verbi riflessivi si coniugano con i **pronomi riflessivi**: mi, ti, si, ci, vi, si.

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">soggetto</th><th class="gram-genere">alzarsi (presente)</th><th class="gram-genere">alzarsi (passato prossimo)</th></tr>
</thead>
<tbody>
<tr><td class="gram-art">io</td><td><strong>mi</strong> alzo</td><td><strong>mi</strong> sono alzato/a</td></tr>
<tr><td class="gram-art">tu</td><td><strong>ti</strong> alzi</td><td><strong>ti</strong> sei alzato/a</td></tr>
<tr><td class="gram-art">lui/lei/Lei</td><td><strong>si</strong> alza</td><td><strong>si</strong> è alzato/a</td></tr>
<tr><td class="gram-art">noi</td><td><strong>ci</strong> alziamo</td><td><strong>ci</strong> siamo alzati/e</td></tr>
<tr><td class="gram-art">voi</td><td><strong>vi</strong> alzate</td><td><strong>vi</strong> siete alzati/e</td></tr>
<tr><td class="gram-art">loro</td><td><strong>si</strong> alzano</td><td><strong>si</strong> sono alzati/e</td></tr>
</tbody>
</table>

> Il passato prossimo dei verbi riflessivi si forma sempre con **ESSERE**. Il participio concorda col soggetto.

---

## B Verbi riflessivi comuni

**Routine quotidiana:**
- alzarsi, svegliarsi, addormentarsi, lavarsi, pettinarsi, vestirsi, spogliarsi, togliersi, mettersi, guardarsi, truccarsi, farsi la barba, sedersi, sdraiarsi

**Sentimenti e stati:**
- sentirsi (bene/male), annoiarsi, divertirsi, arrabbiarsi, preoccuparsi, stufarsi, rilassarsi, lamentarsi, vergognarsi, pentirsi, fidarsi (di), innamorarsi (di), sposarsi, laurearsi

**Con il corpo:**
- lavarsi le mani / i denti / i capelli
- rompersi una gamba / il braccio
- farsi male (a)

---

## C Verbi riflessivi reciproci

Esprimono un'azione che soggetti diversi compiono l'uno sull'altro (sempre plurale):

- Marco e Luisa **si amano**. (si amano a vicenda)
- I due amici **si telefonano** spesso.
- Ci siamo incontrati in centro.
- Vi conoscete da molto tempo?
- Si sono scritti per anni.

---

## D La forma impersonale con SI

Il **si impersonale** + 3ª pers. sing. esprime un'azione generica, senza soggetto preciso:

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">si + verbo</th><th class="gram-art">significato</th><th class="gram-art">esempio</th></tr>
</thead>
<tbody>
<tr><td>si parla</td><td>si parla in modo generico</td><td>In Italia <strong>si parla</strong> italiano.</td></tr>
<tr><td>si mangia</td><td>la gente mangia</td><td>Qui <strong>si mangia</strong> bene.</td></tr>
<tr><td>si può</td><td>è possibile</td><td><strong>Si può</strong> entrare?</td></tr>
<tr><td>si deve</td><td>è necessario</td><td><strong>Si deve</strong> studiare molto.</td></tr>
<tr><td>si va</td><td>la gente va</td><td>D'estate <strong>si va</strong> al mare.</td></tr>
</tbody>
</table>

> Con un **sostantivo plurale** il verbo va al **plurale**: *Si vendono case. Si cercano impiegati.*

---

## Conversazione — Dal fruttivendolo

— Buongiorno, signora, desidera?
— Buongiorno. Vorrei un chilo di pomodori.
— Ecco a Lei, signora. Sono freschissimi, arrivati stamattina. Desidera altro?
— Sì, mi dia anche mezzo chilo di fagiolini e quattro zucchine.
— Benissimo. Altro?
— Avete le melanzane?
— Sì, certo. Quante ne vuole?
— Me ne dia tre, grazie. Quanto viene in tutto?
— Allora: i pomodori fanno un euro e ottanta, i fagiolini novanta centesimi, le zucchine un euro, le melanzane ottanta centesimi. In tutto sono quattro euro e cinquanta centesimi.
— Ecco a Lei cinque euro.
— Cinquanta centesimi di resto. Grazie e arrivederLa, signora.
— ArrivederLa.

---

## Vocabolario sistematico — Il corpo umano

**La testa:** il cervello, il cranio, il capello/i capelli, la fronte, l'occhio/gli occhi, il naso, la guancia, il mento, la bocca, il labbro/le labbra, i denti, l'orecchio/le orecchie, il collo.

**Il tronco:** la spalla, il petto, il seno, la schiena, la pancia/lo stomaco, la vita, il fianco.

**Gli arti:** il braccio/le braccia, il gomito, il polso, la mano/le mani, il dito/le dita, la gamba, il ginocchio, la caviglia, il piede.

**Modi di dire:**
- *avere mal di testa / di stomaco / di denti / di gola*
- *avere la febbre / il raffreddore / la tosse*
- *farsi male a una gamba*
- *rompersi un braccio*

---

## Osservare — La forma impersonale

La forma impersonale con **SI** può essere usata anche con aggettivi e participi. In questo caso l'aggettivo/participio è sempre **maschile plurale**:

- Quando **si è giovani**, si hanno tante speranze.
- **Si è stanchi** dopo una lunga giornata di lavoro.
- In Italia, **si è abituati** a mangiare bene.
- **Si è contenti** quando si finisce un lavoro difficile.
"""

lez["exemplos"] = [
    "Mi sono svegliato tardi stamattina. (riflessivo + essere)",
    "Si è lavata i capelli. (riflessivo con parte del corpo)",
    "Marco e Luisa si sono sposati l'anno scorso. (reciproco)",
    "In Italia si mangia bene. (si impersonale)",
    "Si vendono appartamenti. (si impersonale + plurale)",
]

EX = []

# Domande sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — A letto con l'influenza:\n1. Perché Laura deve stare a letto?\n2. Come si è sentita quando si è alzata?\n3. Chi le ha portato il tè?\n4. Chi ha chiamato nel pomeriggio?\n5. Cosa ha fatto Carla quando ha sentito di Laura?\n6. Come si è sentita Laura la sera?",
    "resposta": "1. Ha l'influenza.\n2. Si è sentita stanca e pallida, con il naso rosso.\n3. Sua madre le ha portato una tazza di tè.\n4. Ha chiamato la sua amica Carla.\n5. Si è messa a ridere e le ha detto che si sarebbe rimessa presto.\n6. Si è sentita meglio e ha potuto mangiare qualcosa.",
    "explicacao": "Comprensione del testo con verbi riflessivi: si è svegliata, si è alzata, si è sentita, si è addormentata."
})

# Esercizio 1
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Coniugare al presente indicativo:\n1. io / alzarsi\n2. tu / svegliarsi\n3. lui / lavarsi\n4. noi / sedersi\n5. voi / vestirsi\n6. loro / addormentarsi\n7. lei / pettinarsi\n8. io / divertirsi\n9. tu / annoiarsi\n10. loro / innamorarsi",
    "resposta": "1. mi alzo\n2. ti svegli\n3. si lava\n4. ci sediamo\n5. vi vestite\n6. si addormentano\n7. si pettina\n8. mi diverto\n9. ti annoi\n10. si innamorano",
    "explicacao": "I verbi riflessivi si coniugano con pronomi riflessivi: mi, ti, si, ci, vi, si + forma verbale corrispondente."
})

# Esercizio 2
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Volgere al passato prossimo:\n1. Mi alzo alle sette.\n2. Ti svegli presto.\n3. Laura si veste in fretta.\n4. Ci laviamo le mani.\n5. Vi sedete a tavola.\n6. I bambini si addormentano subito.\n7. Mi annoio durante la conferenza.\n8. Tu ti arrabbi facilmente.\n9. Carla si sposa a giugno.\n10. Noi ci divertiamo alla festa.",
    "resposta": "1. Mi sono alzato/a alle sette.\n2. Ti sei svegliato/a presto.\n3. Laura si è vestita in fretta.\n4. Ci siamo lavati/e le mani.\n5. Vi siete seduti/e a tavola.\n6. I bambini si sono addormentati subito.\n7. Mi sono annoiato/a durante la conferenza.\n8. Tu ti sei arrabbiato/a facilmente.\n9. Carla si è sposata a giugno.\n10. Noi ci siamo divertiti/e alla festa.",
    "explicacao": "Passato prossimo riflessivo: sempre con ESSERE. Participio concorda col soggetto (es: laura → vestita, i bambini → addormentati)."
})

# Esercizio 3
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Descrivere la routine di Maria usando i verbi: svegliarsi / alzarsi / lavarsi i denti / farsi la doccia / vestirsi / truccarsi / uscire di casa / arrivare in ufficio / sedersi alla scrivania / cominciare a lavorare",
    "resposta": "Ogni mattina Maria si sveglia alle sette. Si alza dopo qualche minuto, va in bagno e si lava i denti. Poi si fa la doccia e si veste. Prima di uscire si trucca velocemente. Esce di casa alle otto meno un quarto e arriva in ufficio alle otto e venti. Si siede alla sua scrivania e comincia a lavorare.",
    "explicacao": "Uso dei verbi riflessivi in sequenza narrativa. Il soggetto (Maria) resta stabile, i pronomi riflessivi si concordano: si sveglia, si alza, si lava, si fa, si veste, si trucca, si siede."
})

# Esercizio 4 - reciproci
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Riscrivere usando il verbo riflessivo reciproco:\n1. Marco ama Luisa e Luisa ama Marco.\n2. Paolo telefona a Gianni e Gianni telefona a Paolo.\n3. Carlo scrive a Lucia e Lucia scrive a Carlo.\n4. Anna conosce Roberto e Roberto conosce Anna.\n5. Ieri Franco ha salutato Maria e Maria ha salutato Franco.",
    "resposta": "1. Marco e Luisa si amano.\n2. Paolo e Gianni si telefonano.\n3. Carlo e Lucia si scrivono.\n4. Anna e Roberto si conoscono.\n5. Ieri Franco e Maria si sono salutati.",
    "explicacao": "Verbo riflessivo reciproco: soggetto sempre plurale, si esprime azione svolta a vicenda tra due o più persone."
})

# Esercizio 5 - si impersonale
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Trasformare usando la forma impersonale con SI:\n1. La gente mangia bene in questo ristorante.\n2. In Italia la gente parla italiano.\n3. È necessario studiare per imparare.\n4. La gente va spesso al cinema in questa città.\n5. È possibile parcheggiare qui?\n6. In questo negozio vendono scarpe italiane.\n7. La gente entra da questa porta.\n8. Qui la gente non fuma.",
    "resposta": "1. In questo ristorante si mangia bene.\n2. In Italia si parla italiano.\n3. Si deve studiare per imparare.\n4. In questa città si va spesso al cinema.\n5. Si può parcheggiare qui?\n6. In questo negozio si vendono scarpe italiane.\n7. Si entra da questa porta.\n8. Qui non si fuma.",
    "explicacao": "SI impersonale + verbo 3ª pers. sing. Per sostantivi plurali → plurale: si vendono scarpe. Con dovere/potere: si deve, si può."
})

# Esercizio 6 - misto
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Completare con il verbo riflessivo corretto (presente o passato prossimo):\n1. A che ora (tu svegliarsi) ___ stamattina?\n2. Laura (sentirsi) ___ male ieri e (mettersi) ___ a letto.\n3. Di solito (io lavarsi) ___ i capelli ogni due giorni.\n4. Quanti anni aveva quando (lui sposarsi) ___?\n5. (Noi divertirsi) ___ molto alla festa di sabato.\n6. Non (voi preoccuparsi) ___ , andrà tutto bene!\n7. I bambini (addormentarsi) ___ subito dopo cena.\n8. Come (tu chiamarsi) ___?",
    "resposta": "1. ti sei svegliato/a\n2. si è sentita / si è messa\n3. mi lavo\n4. si è sposato\n5. ci siamo divertiti/e\n6. vi preoccupate\n7. si sono addormentati\n8. ti chiami",
    "explicacao": "Selezione del tempo: di solito / ogni → presente; ieri / stamattina / alla festa → passato prossimo. Participio concorda sempre col soggetto."
})

# Esercizio 7
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 7** — Lavorare sul testo — Un incontro per strada\n\nInventare un breve dialogo (6-8 battute) tra due vecchi amici che si incontrano per strada dopo molto tempo. Usare almeno 4 verbi riflessivi.",
    "resposta": "Esempio:\n— Ciao Marco! Come stai? Non ci vediamo da mesi!\n— Ah, Giulio! Che piacere rivederti! Mi ero dimenticato che abiti in questo quartiere.\n— Sì, mi sono trasferito qui sei mesi fa. Come ti sei trovato nel nuovo lavoro?\n— Benissimo! Mi sono ambientato subito. E tu? Ti sei sposato, ho sentito!\n— Sì, mi sono sposato a settembre. Siamo molto felici.\n— Congratulazioni! Dobbiamo vederci presto. Ti telefono questa settimana.\n— Perfetto! ArrivederLa... ah no, ciao! Ci vediamo!",
    "explicacao": "Produzione libera con verbi riflessivi. Possibili verbi: vedersi, incontrarsi, trovarsi, trasferirsi, sposarsi, dimenticarsi, telefonarsi, salutarsi."
})

# Esercizi di verifica
verifica = [
    ("Stamattina mi sono svegliato alle sette.", "Stamattina mi ho svegliato alle sette.", "Stamattina ho mi svegliato alle sette.", 0,
     "I verbi riflessivi usano ESSERE al passato prossimo: mi SONO svegliato. Non si usa AVERE."),
    ("Luisa si è pettinata.", "Luisa si ha pettinato.", "Luisa ha pettinata.", 0,
     "Riflessivo + ESSERE: si È pettinata. Il participio concorda con Luisa (femm.): pettinata."),
    ("Si mangia bene qui.", "Si mangiano bene qui.", "Mangia si bene qui.", 0,
     "SI impersonale + verbo sing.: si MANGIA (non c'è soggetto plurale). 'Mangia si' è ordine sbagliato."),
    ("In questo negozio si vendono vestiti eleganti.", "In questo negozio si vende vestiti eleganti.", "In questo negozio vendesi vestiti eleganti.", 0,
     "Con sostantivo plurale (vestiti) → SI VENDONO (plurale). 'vendesi' è forma arcaica."),
    ("Marco e Luisa si sono sposati l'anno scorso.", "Marco e Luisa si hanno sposato l'anno scorso.", "Marco e Luisa hanno sposato l'anno scorso.", 0,
     "Riflessivo reciproco: si SONO sposati (ESSERE). Participio al maschile plurale (Marco + Luisa)."),
    ("Mi sono fatta una doccia.", "Mi sono fatto una doccia.", "Ho fatto una doccia a me.", 1,
     "Se il soggetto è femminile: mi sono fatta. Se maschile: mi sono fatto. La scelta dipende dal genere."),
    ("Quando si è giovani, si commettono errori.", "Quando si è giovani, si commette errori.", "Quando si è giovane, si commettono errori.", 0,
     "SI impersonale + aggettivo → aggettivo maschile plurale: giovani. Con sostantivo plurale: si commettono."),
    ("Non ti preoccupare!", "Non si preoccupare!", "Non preoccuparti!", 2,
     "Imperativo negativo dei riflessivi: NON + infinito (non preoccuparti) OPPURE usa la forma base."),
    ("Si sono laureati l'anno scorso.", "Si hanno laureato l'anno scorso.", "Hanno laureati l'anno scorso.", 0,
     "Riflessivo: si SONO laureati (ESSERE). Participio concorda col soggetto plurale maschile."),
    ("Ti sei divertita alla festa?", "Ti hai divertito alla festa?", "Ti sei divertito alla festa?", 0,
     "Se il soggetto è femminile: ti sei divertita. 'Ti hai divertito' sbagliato (usa ESSERE, non AVERE)."),
    ("Come ti chiami?", "Come si chiami?", "Come mi chiami?", 0,
     "Con soggetto TU: ti chiami. 'Si' è per lui/lei/loro. 'Mi chiami' significherebbe 'come mi stai chiamando'."),
    ("Si deve studiare per imparare.", "Si deve studiare per imparare.", "Si devono studiare per imparare.", 0,
     "SI impersonale + dovere + infinito: SI DEVE (sing.) studiare. Il verbo modale resta al singolare."),
    ("I bambini si sono addormentati subito.", "I bambini si sono addormentate subito.", "I bambini si hanno addormentato subito.", 0,
     "Soggetto maschile plurale: addormentaTI. 'Addormentate' è femminile. Riflessivo vuole ESSERE."),
    ("Ci siamo incontrati per caso.", "Ci abbiamo incontrati per caso.", "Ci siamo incontrate per caso.", 0,
     "Reciproco + ESSERE: ci SIAMO incontrati. Se gruppo misto o maschile → incontrati. 'Abbiamo' sbagliato."),
    ("Perché ti sei arrabbiata?", "Perché ti sei arrabbiato?", "Perché hai arrabbiarti?", 0,
     "Se il soggetto è femminile: ti sei arrabbiatA. 'Hai arrabbiarti' non esiste in italiano."),
    ("Si possono visitare molti musei a Firenze.", "Si può visitare molti musei a Firenze.", "Si possono visitato molti musei.", 0,
     "Con sostantivo plurale (musei) → SI POSSONO (plurale). 'Possono visitato' mescola modi diversi."),
    ("Laura si è messa a piangere.", "Laura si è messa piangere.", "Laura ha messo a piangere.", 0,
     "Mettersi a + infinito: si è MESSA a piangere. 'Messa piangere' manca la preposizione A."),
    ("Dove vi siete conosciuti?", "Dove vi avete conosciuto?", "Dove ci avete conosciuti?", 0,
     "Reciproco 2ª pers. plur.: vi SIETE conosciuti. 'Vi avete' sbagliato (ESSERE non AVERE)."),
    ("Si è stanchi dopo una lunga giornata.", "Si è stanco dopo una lunga giornata.", "Uno è stanchi dopo una lunga giornata.", 0,
     "SI impersonale + aggettivo → maschile plurale: stanCHI. 'Stanco' è singolare. 'Uno è' non è la stessa costruzione."),
    ("Non ci siamo visti da molto tempo.", "Non ci abbiamo visto da molto tempo.", "Non si siamo visti da molto tempo.", 0,
     "Reciproco 1ª pers. plur. + ESSERE: ci SIAMO visti. 'Abbiamo' sbagliato. 'Si siamo' non esiste."),
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
    ("Mi ho svegliato tardi stamattina.",
     "Mi sono svegliato/a tardi stamattina.",
     "I verbi riflessivi usano sempre ESSERE al passato prossimo: mi SONO svegliato."),
    ("Luisa si ha pettinata stamattina.",
     "Luisa si è pettinata stamattina.",
     "Riflessivo → ESSERE: si È pettinata. Mai AVERE con i verbi riflessivi."),
    ("In Italia si parlano italiano.",
     "In Italia si parla italiano.",
     "SI impersonale + verbo singolare se la cosa espressa è singolare (italiano = linguaggio, sing.)."),
    ("Voglio lavarmi le mani prima di mangiare.",
     "Corretta. / Mi voglio lavare le mani prima di mangiare.",
     "Entrambe le forme sono corrette: lavarMI (unito all'infinito) o MI voglio lavare (prima del servile)."),
    ("Marco e Giulia si hanno incontrati in centro.",
     "Marco e Giulia si sono incontrati in centro.",
     "Reciproco → ESSERE: si SONO incontrati. Mai AVERE con i riflessivi reciproci."),
    ("Quando si è giovane, si fanno errori.",
     "Quando si è giovani, si fanno errori.",
     "SI impersonale + aggettivo → maschile plurale: giovanI (non singolare)."),
    ("I ragazzi si sono divertiti alla festa.",
     "Corretta.",
     "Forma corretta: riflessivo + ESSERE + participio maschile plurale (-iti)."),
    ("Non preoccuparsi, andrà tutto bene!",
     "Non preoccuparti! (a tu) / Non si preoccupi! (formale) / Non preoccupatevi! (a voi)",
     "L'imperativo negativo riflessivo: NON + infinito o forma adatta alla persona."),
    ("Si vende appartamenti in questo palazzo.",
     "Si vendono appartamenti in questo palazzo.",
     "Con sostantivo plurale (appartamenti) → SI VENDONO (plurale)."),
    ("Come ti chiami tu? Mi chiamo Luigi.",
     "Corretta.",
     "Corretta: ti chiami (tu) / mi chiamo (io). Uso corretto dei pronomi riflessivi."),
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
