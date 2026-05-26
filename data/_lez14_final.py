import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XIV"), None)
if lez is None:
    lez = {"id": "a1-lez14", "num": "Lezione XIV", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I pronomi relativi e interrogativi"
lez["subtitulo"] = "Che, cui, il quale; chi, che cosa, quale, quanto"

lez["teoria"] = """\
## Una lettura interessante

Giulia stava leggendo un romanzo che le aveva prestato un'amica. Era un libro molto interessante, scritto da un autore italiano di cui non conosceva il nome. La storia, che si svolgeva a Firenze nel Rinascimento, parlava di un pittore il cui talento era straordinario. Il protagonista, che si chiamava Leonardo, incontrava per strada una donna di cui si innamorava perdutamente. Giulia, che di solito non leggeva molto, si era appassionata talmente che non riusciva a smettere. Quando sua madre le ha chiesto cosa stesse leggendo, Giulia le ha detto che era il libro più bello che avesse mai letto.

---

## A I pronomi relativi

I pronomi relativi collegano due frasi, evitando ripetizioni. Il loro uso dipende dalla funzione nella frase.

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">pronome</th><th class="gram-art">funzione</th><th class="gram-art">esempio</th></tr>
</thead>
<tbody>
<tr><td><strong>che</strong></td><td>soggetto o complemento diretto (invariabile)</td><td>Il libro <strong>che</strong> leggo. / L'uomo <strong>che</strong> parla.</td></tr>
<tr><td><strong>cui</strong></td><td>dopo preposizione (a, di, da, in, con, su...)</td><td>Il libro di <strong>cui</strong> parlo. / La ragazza con <strong>cui</strong> esco.</td></tr>
<tr><td><strong>il quale / la quale / i quali / le quali</strong></td><td>sostituto di che/cui, più formale</td><td>L'uomo <strong>il quale</strong> parla. / La donna con <strong>la quale</strong> esco.</td></tr>
<tr><td><strong>il cui / la cui / i cui / le cui</strong></td><td>possessivo (di + cui + accordo con nome seguente)</td><td>Il pittore <strong>il cui</strong> talento è famoso.</td></tr>
<tr><td><strong>chi</strong></td><td>= colui che / coloro che (senza antecedente)</td><td><strong>Chi</strong> studia impara. / Non so <strong>chi</strong> ha chiamato.</td></tr>
</tbody>
</table>

---

## B Uso di CHE e CUI

**CHE** si usa come soggetto o complemento diretto (senza preposizione):
- La ragazza **che** parla è mia sorella. (soggetto)
- Il libro **che** ho comprato è interessante. (complemento diretto)

**CUI** si usa dopo preposizione:
- Il libro **di cui** ti ho parlato. (parlare di)
- La città **in cui** vivo. (vivere in)
- L'amico **con cui** viaggio. (viaggiare con)
- La ragione **per cui** sono qui. (essere qui per)

> **ATTENZIONE!** Con l'articolo, CUI diventa possessivo: *il/la/i/le + cui*
> - Il professore **il cui** corso è interessante. (il corso del professore)
> - La studentessa **la cui** tesi è pronta.

---

## C I pronomi interrogativi

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">pronome</th><th class="gram-art">uso</th><th class="gram-art">esempio</th></tr>
</thead>
<tbody>
<tr><td><strong>chi?</strong></td><td>persone (sogg. o compl.)</td><td><strong>Chi</strong> è? / Con <strong>chi</strong> parli?</td></tr>
<tr><td><strong>che cosa? / cosa? / che?</strong></td><td>cose (sogg. o compl.)</td><td><strong>Che cosa</strong> fai? / <strong>Cosa</strong> mangi?</td></tr>
<tr><td><strong>quale/i?</strong></td><td>scelta tra più elementi</td><td><strong>Quale</strong> libro preferisci? / <strong>Quali</strong> sono i tuoi?</td></tr>
<tr><td><strong>quanto/a/i/e?</strong></td><td>quantità</td><td><strong>Quanto</strong> costa? / <strong>Quante</strong> persone?</td></tr>
</tbody>
</table>

---

## D Espressioni con CHI

**Chi** può introdurre proposizioni generali (= colui che):
- **Chi** dorme non piglia pesci. (proverbio)
- **Chi** lavora sodo ottiene risultati.
- **Chi** sei tu per dirmi cosa fare?
- Non so **chi** abbia preso il mio ombrello.
- Dimmi **chi** frequenti e ti dirò chi sei.

---

## Conversazione — Una presentazione

— Buongiorno! Mi chiamo Francesca Landi. Sono la nuova collega di cui vi ha parlato il direttore.
— Ah, benvenuta! Sono Marco Bianchi. Di dove sei?
— Sono di Roma, ma da qualche anno vivo a Milano. E tu, da dove vieni?
— Io sono fiorentino. Da quanto tempo lavori in questo settore?
— Da cinque anni. Ho lavorato in un'altra azienda il cui direttore era molto esigente, ma ho imparato molto.
— Quale posizione occupavi?
— Ero responsabile marketing. E qui, con chi lavorerò?
— Con me e con Giulia, che è quella ragazza che vedi là. È bravissima, da cui puoi imparare molto.
— Benissimo! Non vedo l'ora di cominciare.

---

## Vocabolario sistematico — Espressioni idiomatiche con FARE

| espressione | significato | esempio |
|---|---|---|
| fare a meno di | non poter rinunciare | Non riesco a fare a meno del caffè. |
| fare finta di | fingere | Fa finta di non sentire. |
| fare del proprio meglio | impegnarsi al massimo | Faccio del mio meglio. |
| farsi vivo | dare notizie di sé | Non si fa vivo da settimane. |
| fare presente | segnalare | Ti faccio presente che sei in ritardo. |
| fare fuori | eliminare / mangiare tutto | Ha fatto fuori tutta la torta! |
| fare bella/brutta figura | fare una buona/cattiva impressione | Non voglio fare brutta figura. |
| fare il giro | girare intorno / in giro | Facciamo un giro del centro? |

---

## Osservare — L'uso di CAVARSELA

**Cavarsela** = riuscire a superare una situazione difficile

| struttura | esempio |
|---|---|
| cavarsela (presente) | Me la cavo abbastanza bene con l'italiano. |
| cavarsela (passato) | Me la sono cavata all'esame! |
| come te la cavi? | Come te la cavi con il computer? |
| se la cava | Si cava sempre d'impaccio. |

> **Nota:** CAVARSELA è un verbo pronominale: cavar**sela** = cavare + si + la
"""

lez["exemplos"] = [
    "Il libro che leggo è interessante. (che = complemento diretto)",
    "La ragazza con cui parlo è mia sorella. (cui dopo preposizione)",
    "Il professore il cui corso è difficile. (possessivo il cui)",
    "Chi studia ottiene buoni risultati. (chi = colui che)",
    "Me la cavo bene con l'italiano. (cavarsela)",
]

EX = []

# Domande sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Una lettura interessante:\n1. Cosa stava leggendo Giulia?\n2. Chi le aveva prestato il libro?\n3. Dove si svolgeva la storia?\n4. Chi era il protagonista?\n5. Di cosa si innamorava il protagonista?\n6. Come ha risposto Giulia alla madre?",
    "resposta": "1. Stava leggendo un romanzo molto interessante.\n2. Un'amica le aveva prestato il libro.\n3. La storia si svolgeva a Firenze nel Rinascimento.\n4. Il protagonista si chiamava Leonardo, un pittore dal talento straordinario.\n5. Si innamorava di una donna incontrata per strada.\n6. Le ha detto che era il libro più bello che avesse mai letto.",
    "explicacao": "Il testo usa vari pronomi relativi: che, cui, il cui. Attenzione all'uso di ciascuno."
})

# Esercizio 1 - CHE
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Unire le frasi con CHE:\n1. Ho comprato un libro. Il libro è molto interessante.\n2. Ho incontrato una ragazza. La ragazza abita vicino a me.\n3. Conosco uno studente. Lo studente parla cinque lingue.\n4. Abbiamo visitato un museo. Il museo era chiuso ieri.\n5. Ho letto un articolo. L'articolo parlava dell'ambiente.\n6. Ho visto un film. Il film mi ha fatto piangere.",
    "resposta": "1. Ho comprato un libro che è molto interessante.\n2. Ho incontrato una ragazza che abita vicino a me.\n3. Conosco uno studente che parla cinque lingue.\n4. Abbiamo visitato un museo che era chiuso ieri.\n5. Ho letto un articolo che parlava dell'ambiente.\n6. Ho visto un film che mi ha fatto piangere.",
    "explicacao": "CHE invariabile: soggetto (un museo che era) o complemento diretto (un libro che leggo). Non cambia con genere/numero."
})

# Esercizio 2 - CUI con preposizione
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Unire le frasi con la preposizione + CUI:\n1. Ho comprato un libro. Ti ho parlato di questo libro.\n2. Ho incontrato una ragazza. Esco spesso con questa ragazza.\n3. Abito in una città. In questa città ci sono molti musei.\n4. Ho uno zio. Mi fido molto di questo zio.\n5. Lavoro in un'azienda. Sono soddisfatto di questa azienda.\n6. Ho preso un treno. Con questo treno sono arrivato in ritardo.",
    "resposta": "1. Ho comprato un libro di cui ti ho parlato.\n2. Ho incontrato una ragazza con cui esco spesso.\n3. Abito in una città in cui ci sono molti musei.\n4. Ho uno zio di cui mi fido molto.\n5. Lavoro in un'azienda di cui sono soddisfatto.\n6. Ho preso un treno con cui sono arrivato in ritardo.",
    "explicacao": "CUI dopo preposizione: di cui, con cui, in cui, per cui, su cui, a cui. La preposizione si conserva prima di cui."
})

# Esercizio 3 - IL CUI possessivo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Trasformare usando IL CUI / LA CUI / I CUI / LE CUI:\n1. Ho letto un libro. Il titolo del libro è famoso.\n2. Conosco un professore. Le lezioni del professore sono molto interessanti.\n3. Abbiamo incontrato una signora. Il marito della signora è medico.\n4. Lavoro con un ragazzo. I genitori del ragazzo vivono in Sicilia.\n5. Ho visto un film. Il regista del film è molto noto.",
    "resposta": "1. Ho letto un libro il cui titolo è famoso.\n2. Conosco un professore le cui lezioni sono molto interessanti.\n3. Abbiamo incontrato una signora il cui marito è medico.\n4. Lavoro con un ragazzo i cui genitori vivono in Sicilia.\n5. Ho visto un film il cui regista è molto noto.",
    "explicacao": "Il/la/i/le + cui + nome: l'articolo concorda col nome che segue (il/la/i/le), non con l'antecedente."
})

# Esercizio 4 - interrogativi
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Formare la domanda con il pronome interrogativo corretto:\n1. (chi) ___ hai telefonato?\n2. (cosa) ___ stai mangiando?\n3. (quale) ___ libro preferisci?\n4. (quanto) ___ costa questa giacca?\n5. (quante) ___ persone erano alla festa?\n6. (chi) ___ è quella signora?\n7. (cosa) ___ significa questa parola?\n8. (quale) ___ di questi colori ti piace di più?",
    "resposta": "1. Chi hai telefonato? / A chi hai telefonato?\n2. Che cosa stai mangiando? / Cosa stai mangiando?\n3. Quale libro preferisci?\n4. Quanto costa questa giacca?\n5. Quante persone erano alla festa?\n6. Chi è quella signora?\n7. Che cosa significa questa parola? / Cosa significa?\n8. Quale di questi colori ti piace di più?",
    "explicacao": "Chi (persone), che cosa/cosa (cose), quale/i (scelta), quanto/a/i/e (quantità)."
})

# Esercizio 5 - CHI relativo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Completare con CHI (= colui che):\n1. ___ lavora sodo ottiene buoni risultati.\n2. ___ non risica non rosica. (proverbio)\n3. Dimmi ___ frequenti e ti dirò chi sei.\n4. Non so ___ abbia preso il mio dizionario.\n5. Aiuterò ___ ha bisogno di me.\n6. ___ ha detto questa cosa non capisce niente.",
    "resposta": "1. Chi lavora sodo ottiene buoni risultati.\n2. Chi non risica non rosica.\n3. Dimmi chi frequenti e ti dirò chi sei.\n4. Non so chi abbia preso il mio dizionario.\n5. Aiuterò chi ha bisogno di me.\n6. Chi ha detto questa cosa non capisce niente.",
    "explicacao": "CHI relativo (= colui che / chiunque) si usa senza antecedente. Introduce proposizioni generali."
})

# Esercizio 6 - misto
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Scegliere CHE, CUI o IL/LA/I/LE CUI:\n1. La ragazza ___ ho visto ieri è bella.\n2. Il professore con ___ ho parlato è molto disponibile.\n3. Il libro ___ mi hai prestato è interessantissimo.\n4. L'azienda per ___ lavoro è internazionale.\n5. L'attrice ___ film ho visto si chiama Sofia.\n6. La città in ___ sono nato è piccola.\n7. Gli studenti ___ studiano di più prendono voti migliori.\n8. La ragione per ___ sono qui è semplice.",
    "resposta": "1. che\n2. cui\n3. che\n4. cui\n5. il cui\n6. cui\n7. che\n8. cui",
    "explicacao": "CHE = sogg./compl.dir. senza prep. CUI = dopo preposizione. Il/la/i/le + CUI = possessivo (il film dell'attrice → l'attrice il cui film)."
})

# Esercizio 7 - cavarsela + fare
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 7** — Completare con l'espressione corretta (cavarsela / fare finta / fare a meno / fare bella figura):\n1. All'esame di italiano me ___ abbastanza bene.\n2. Non riesco a ___ del caffè al mattino.\n3. Ha ___ di non capire, ma in realtà sa tutto.\n4. Voglio ___ alla festa del mio capo, quindi mi vestirò elegante.\n5. Come te ___ con l'informatica?\n6. Si sono cavati ___ d'impaccio grazie al loro senso dell'umorismo.",
    "resposta": "1. la sono cavato/a\n2. fare a meno\n3. fatto finta\n4. fare bella figura\n5. la cavi\n6. d'impaccio (se la sono cavata)",
    "explicacao": "CAVARSELA: me la cavo, te la cavi, se la cava, ce la caviamo, ve la cavate, se la cavano. FARE A MENO DI + infinito. FARE FINTA DI + infinito."
})

# Esercizi di verifica
verifica = [
    ("Il libro che ho comprato è bello.", "Il libro cui ho comprato è bello.", "Il libro il quale ho comprato è bello.", 0,
     "CHE = complemento diretto (senza preposizione). CUI si usa dopo preposizione. 'Il quale' richiede accordo dell'articolo."),
    ("La città in cui vivo è bella.", "La città che vivo è bella.", "La città cui vivo è bella.", 0,
     "Con preposizione IN → CUI: in cui. CHE non si usa dopo preposizione. 'Cui' senza preposizione è scorretta qui."),
    ("Il professore il cui corso è difficile.", "Il professore che corso è difficile.", "Il professore di cui corso è difficile.", 0,
     "Possessivo: il + CUI + nome (il cui corso). L'articolo concorda col nome che segue (corso, masch.sg. → il)."),
    ("Non so chi abbia telefonato.", "Non so che abbia telefonato.", "Non so quale abbia telefonato.", 0,
     "CHI interrogativo/relativo per persone sconosciute: non so CHI. 'Che' qui sarebbe relativo, non interrogativo."),
    ("Quale libro preferisci?", "Che libro preferisci?", "Entrambe le forme sono corrette.", 2,
     "QUALE e CHE possono entrambi introdurre aggettivi interrogativi prima di un sostantivo: Quale/Che libro?"),
    ("La ragazza con la quale esco è simpatica.", "La ragazza con che esco è simpatica.", "La ragazza con cui esco è simpatica.", 2,
     "Dopo preposizione: sia CUI che IL/LA QUALE sono corretti. 'Con che' non si usa."),
    ("Chi studia ottiene buoni risultati.", "Che studia ottiene buoni risultati.", "Quale studia ottiene buoni risultati.", 0,
     "CHI = colui che (senza antecedente, proposizione generica). CHE senza antecedente non può introdurre soggetto generale."),
    ("Quante persone sono venute alla festa?", "Quanti persone sono venute alla festa?", "Quanto persone sono venute alla festa?", 0,
     "QUANTO concorda col nome: persone è femm.pl. → QUANTE. 'Quanti' è masch.pl., 'quanto' è sing."),
    ("L'attrice le cui film sono famosi.", "L'attrice i cui film sono famosi.", "L'attrice la cui film sono famosi.", 1,
     "Possessivo: il/la/i/le + CUI concorda col nome seguente (film, masch.pl.) → I CUI. Non con l'antecedente (attrice, femm.)."),
    ("Me la cavo bene con le lingue.", "Mi cavo bene con le lingue.", "Me cavo bene con le lingue.", 0,
     "CAVARSELA: me la cavo (io), te la cavi (tu), se la cava (lui/lei). 'Mi cavo' e 'me cavo' non esistono."),
    ("Per cui non sono potuto venire.", "Perché non sono potuto venire.", "Per il quale non sono potuto venire.", 0,
     "Per cui / per il quale = proposizione esplicativa. Ma nel senso di 'quindi/perciò' si usa spesso PER CUI in italiano parlato."),
    ("La ragione per cui sono partito.", "La ragione che sono partito.", "La ragione di cui sono partito.", 0,
     "RAGIONE PER CUI: preposizione PER + CUI. 'Ragione che' è incorretto. 'Ragione di cui' cambierebbe il senso."),
    ("Ho incontrato una persona di cui mi fido.", "Ho incontrato una persona che mi fido.", "Ho incontrato una persona cui mi fido.", 0,
     "FIDARSI DI → di cui. CHE non si usa dopo preposizione. CUI senza preposizione davanti è scorretta con 'fidarsi'."),
    ("Chi non studia non impara.", "Che non studia non impara.", "Il quale non studia non impara.", 0,
     "CHI = colui che (proposizione generica senza antecedente). 'Che' e 'il quale' richiedono un antecedente."),
    ("Il film di cui mi hai parlato era noioso.", "Il film che mi hai parlato era noioso.", "Il film cui mi hai parlato era noioso.", 0,
     "PARLARE DI → di cui. 'Che mi hai parlato' senza preposizione è sbagliato (parlare vuole 'di'). CUI senza prep. scorretta."),
    ("Sai con chi ha parlato Marco?", "Sai con che ha parlato Marco?", "Sai con quale ha parlato Marco?", 0,
     "CON CHI: interrogativo indiretto per persona. 'Con che' non è standard. 'Con quale' si usa per cose, non persone."),
    ("Le cui figlie sono brave studentesse.", "La cui figlie sono brave studentesse.", "I cui figlie sono brave studentesse.", 0,
     "Possessivo: concorda col nome seguente FIGLIE (femm.pl.) → LE CUI figlie. Non con l'antecedente."),
    ("Non capisco di cosa parli.", "Non capisco di che parli.", "Non capisco di cui parli.", 0,
     "DI COSA: interrogativo indiretto per cose. 'Di che' è accettabile informalmente. 'Di cui' è pronome relativo, non interrogativo."),
    ("La studentessa la cui tesi è pronta.", "La studentessa che tesi è pronta.", "La studentessa di cui tesi è pronta.", 0,
     "Possessivo femminile singolare (tesi = femm.sg.) con antecedente femminile → LA CUI. 'Che tesi' e 'di cui tesi' errati."),
    ("Quanto tempo ci vuole?", "Quanta tempo ci vuole?", "Quale tempo ci vuole?", 0,
     "TEMPO è maschile singolare → QUANTO. 'Quanta' è femm. 'Quale tempo' significa 'che tipo di tempo', non durata."),
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
    ("Ho comprato un libro di cui è interessante.",
     "Ho comprato un libro che è interessante.",
     "CHE = soggetto. CUI si usa dopo preposizione. 'Di cui è interessante' sarebbe 'di cui si parla' o simile."),
    ("La città che vivo è bella.",
     "La città in cui vivo è bella. / La città nella quale vivo è bella.",
     "VIVERE IN → preposizione + CUI: in cui. CHE non si usa dopo preposizione."),
    ("Non so che ha preso le mie chiavi.",
     "Non so chi ha preso le mie chiavi.",
     "Per persona sconosciuta → CHI (interrogativo indiretto). CHE non si usa come interrogativo per persone."),
    ("Il professore di cui corso è interessante.",
     "Il professore il cui corso è interessante.",
     "Possessivo: il/la/i/le + CUI. Qui corso è maschile singolare → IL CUI. 'Di cui corso' è scorretta."),
    ("Quanti soldi hai spento?",
     "Quanti soldi hai speso?",
     "SPENDERE: participio irregolare SPESO (non 'spento' che è di spegnere). Quanti concorda con soldi (m.pl.) ✓."),
    ("Me cavo sempre d'impaccio.",
     "Me la cavo sempre d'impaccio.",
     "CAVARSELA richiede tutti i pronomi: me LA cavo. Non si può omettere LA."),
    ("La ragazza che ho parlato ieri.",
     "La ragazza con cui ho parlato ieri. / La ragazza con la quale ho parlato ieri.",
     "PARLARE CON → preposizione + CUI: con cui. CHE non si usa dopo preposizione."),
    ("Chi lavori sodo ottiene risultati.",
     "Chi lavora sodo ottiene risultati.",
     "CHI relativo + indicativo: chi lavora (3ª sing.). 'Lavori' è congiuntivo, non necessario qui."),
    ("La donna la cui marito è famoso.",
     "La donna il cui marito è famoso.",
     "Possessivo: concorda col nome seguente MARITO (masch.sg.) → IL CUI. Non con la donna (femm.)."),
    ("Fare a meno di studiare è impossibile.",
     "Fare a meno di studiare è impossibile. (CORRETTA)",
     "Forma corretta: fare a meno DI + infinito."),
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
