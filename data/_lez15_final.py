import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XV"), None)
if lez is None:
    lez = {"id": "a1-lez15", "num": "Lezione XV", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il comparativo e il superlativo"
lez["subtitulo"] = "Gradi dell'aggettivo: comparativo e superlativo relativo/assoluto"

lez["teoria"] = """\
## Un'amica vanitosa

Carla è la più vanitosa di tutte le mie amiche. Si veste meglio di chiunque altra e trascorre più tempo davanti allo specchio che a studiare. Quando uscivamo insieme, ci voleva sempre più di un'ora per aspettarla. Lei diceva sempre che il tempo era meno importante della bellezza. Eppure, nonostante sia così vanitosa, è anche la persona più generosa che conosca: è sempre pronta ad aiutare gli altri ed è più gentile di quanto sembri a prima vista. Il suo appartamento è il più ordinato che abbia mai visto, mentre la sua vita è quanto di meno organizzato si possa immaginare. È contraddittoria, ma per questo la voglio tanto bene.

---

## A Il comparativo

### Comparativo di maggioranza (più... di/che)

- **più + aggettivo/avverbio + di** (confronto tra persone/cose diverse):
  - Marco è **più alto di** Luigi.
  - Questa borsa è **più cara di** quella.

- **più... che** (confronto tra due qualità dello stesso soggetto, o con verbi/preposizioni):
  - Studio **più** volentieri **che** con obbligo.
  - È **più** simpatico **che** bello.
  - C'è **più** neve **in** montagna **che** in città.

### Comparativo di minoranza (meno... di/che)
- Roma è **meno** fredda **di** Milano.
- Questo esercizio è **meno** difficile **che** il precedente.

### Comparativo di uguaglianza (tanto... quanto / così... come)
- Marco è **tanto alto quanto** Luigi. (= tanto... quanto)
- Lei è **così** gentile **come** sua madre. (= così... come)

---

## B Il superlativo relativo

Si forma con: **articolo + più/meno + aggettivo (+ di)**

- È **il più bello** della classe.
- È **la più intelligente** del gruppo.
- Sono **i più veloci** della squadra.
- È **il meno caro** del negozio.

---

## C Il superlativo assoluto

Si forma con: **aggettivo + -issimo/a/i/e** (oppure: molto + aggettivo)

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">aggettivo</th><th class="gram-art">superlativo assoluto</th><th class="gram-art">alternativa</th></tr>
</thead>
<tbody>
<tr><td>bello</td><td>bellissimo/a/i/e</td><td>molto bello</td></tr>
<tr><td>grande</td><td>grandissimo/a/i/e</td><td>molto grande</td></tr>
<tr><td>facile</td><td>facilissimo/a/i/e</td><td>molto facile</td></tr>
<tr><td>lungo</td><td>lunghissimo/a/i/e</td><td>molto lungo</td></tr>
<tr><td>ricco</td><td>ricchissimo/a/i/e</td><td>molto ricco</td></tr>
<tr><td>antico</td><td>antichissimo/a/i/e</td><td>molto antico</td></tr>
</tbody>
</table>

---

## D Comparativi e superlativi irregolari

<table class="gram-table gram-table-rich">
<thead>
<tr><th class="gram-art">aggettivo</th><th class="gram-art">comparativo</th><th class="gram-art">superlativo relativo</th><th class="gram-art">superlativo assoluto</th></tr>
</thead>
<tbody>
<tr><td>buono</td><td>migliore (di)</td><td>il migliore</td><td>ottimo</td></tr>
<tr><td>cattivo</td><td>peggiore (di)</td><td>il peggiore</td><td>pessimo</td></tr>
<tr><td>grande</td><td>maggiore (di)</td><td>il maggiore</td><td>massimo</td></tr>
<tr><td>piccolo</td><td>minore (di)</td><td>il minore</td><td>minimo</td></tr>
<tr><td>alto</td><td>superiore (a)</td><td>il superiore</td><td>sommo / supremo</td></tr>
<tr><td>basso</td><td>inferiore (a)</td><td>l'inferiore</td><td>infimo</td></tr>
</tbody>
</table>

---

## E Comparativi di avverbio

| avverbio | comparativo | superlativo |
|---|---|---|
| bene | meglio | benissimo / ottimamente |
| male | peggio | malissimo / pessimamente |
| molto | più | moltissimo |
| poco | meno | pochissimo |

---

## Osservare — L'uso di NEANCHE, NEMMENO, NEPPURE

Queste tre forme sono sinonimi e significano **"neppure / nemmeno"**:

- Non capisco **neanche/nemmeno/neppure** una parola.
- **Neanche** lui sa la risposta.
- Non è venuto **neppure** Mario.
- Non ho mangiato **nemmeno** un boccone.

> Quando anticipano il soggetto o l'oggetto (in posizione enfatica), non richiedono NON davanti al verbo:
> *Neanche lui viene.* (= non viene neanche lui)
"""

lez["exemplos"] = [
    "Marco è più alto di Luigi. (comparativo di maggioranza con 'di')",
    "È più simpatico che bello. (comparativo tra due qualità)",
    "È il più bello della classe. (superlativo relativo)",
    "Questo film è bellissimo! (superlativo assoluto)",
    "Questo vino è migliore di quello. (comparativo irregolare)",
]

EX = []

# Domande sul testo
EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Un'amica vanitosa:\n1. Com'è descritta Carla rispetto alle altre amiche?\n2. Come trascorre il suo tempo?\n3. Quanto tempo ci voleva per aspettarla?\n4. Cosa pensava del tempo?\n5. Qual è la qualità positiva di Carla?\n6. Come sono descritti il suo appartamento e la sua vita?",
    "resposta": "1. È la più vanitosa di tutte.\n2. Si veste meglio di chiunque e trascorre più tempo davanti allo specchio che a studiare.\n3. Ci voleva sempre più di un'ora.\n4. Pensava che il tempo fosse meno importante della bellezza.\n5. È la persona più generosa che conosca, sempre pronta ad aiutare.\n6. L'appartamento è il più ordinato che si possa immaginare; la vita è quanto di meno organizzato.",
    "explicacao": "Uso dei gradi dell'aggettivo nel testo: la più vanitosa, meglio di, più... che, meno importante, il più ordinato."
})

# Esercizio 1
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Formare il comparativo di maggioranza con DI o CHE:\n1. Roma / grande / Milano.\n2. Marco / simpatico / intelligente. (due qualità)\n3. L'oro / caro / l'argento.\n4. Studio / volentieri / obbligo. (con verbi)\n5. Questo film / interessante / quello.\n6. C'è più gente / in città / in campagna.",
    "resposta": "1. Roma è più grande di Milano.\n2. Marco è più simpatico che intelligente.\n3. L'oro è più caro dell'argento.\n4. Studio più volentieri che con obbligo.\n5. Questo film è più interessante di quello.\n6. C'è più gente in città che in campagna.",
    "explicacao": "PIÙ... DI: confronto tra due persone/cose diverse. PIÙ... CHE: confronto tra due qualità dello stesso soggetto, o verbi, o con preposizioni."
})

# Esercizio 2
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Formare il superlativo assoluto:\n1. bello\n2. grande\n3. difficile\n4. lungo\n5. ricco\n6. antico\n7. simpatico\n8. stanco\n9. buono (usa ottimo)\n10. cattivo (usa pessimo)",
    "resposta": "1. bellissimo/a\n2. grandissimo/a\n3. difficilissimo/a\n4. lunghissimo/a\n5. ricchissimo/a\n6. antichissimo/a\n7. simpaticissimo/a\n8. stanchissimo/a\n9. ottimo/a\n10. pessimo/a",
    "explicacao": "Superlativo assoluto: -issimo/a/i/e. Attenzione ai cambiamenti ortografici: -co→-chissimo, -go→-ghissimo, -co→-cissimo (simpatico→simpaticissimo per conservare il suono)."
})

# Esercizio 3
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Usare il comparativo irregolare (migliore/peggiore/maggiore/minore):\n1. Questo ristorante è ___ (buono) di quello che pensavo.\n2. I risultati di quest'anno sono ___ (cattivo) di quelli dell'anno scorso.\n3. La parte ___ (grande) del lavoro è già fatta.\n4. La sorella ___ (piccolo) di Marco ha dieci anni.\n5. Questa soluzione è ___ (buono) delle altre.\n6. Il rendimento è ___ (cattivo) del previsto.",
    "resposta": "1. migliore\n2. peggiori\n3. maggiore\n4. minore\n5. la migliore\n6. peggiore",
    "explicacao": "Comparativi irregolari: buono→migliore, cattivo→peggiore, grande→maggiore, piccolo→minore. Non cambiano con genere, ma concordano col numero: migliore/migliori."
})

# Esercizio 4
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Formare il superlativo relativo:\n1. Firenze è una città bella (d'Italia).\n2. Questo è un film interessante (che ho visto).\n3. Mario è uno studente bravo (della classe).\n4. Luglio è un mese caldo (dell'anno).\n5. Queste sono delle scarpe care (del negozio).",
    "resposta": "1. Firenze è la città più bella d'Italia.\n2. Questo è il film più interessante che ho visto.\n3. Mario è lo studente più bravo della classe.\n4. Luglio è il mese più caldo dell'anno.\n5. Queste sono le scarpe più care del negozio.",
    "explicacao": "Superlativo relativo: articolo + più/meno + aggettivo + di/che. L'articolo concorda con il nome: la città, il film, lo studente, le scarpe."
})

# Esercizio 5 - avverbi
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Usare il comparativo/superlativo di avverbio:\n1. Parli ___ (bene) di tua sorella.\n2. Ieri mi sono sentito ___ (male) di oggi.\n3. Questa volta ho studiato ___ (molto) delle altre.\n4. Hai mangiato ___ (poco) di ieri.\n5. Marco canta ___ (bene) di tutti.",
    "resposta": "1. meglio\n2. peggio\n3. di più / moltissimo\n4. di meno / pochissimo\n5. meglio",
    "explicacao": "Comparativi irregolari di avverbio: bene→meglio, male→peggio, molto→di più/moltissimo, poco→di meno/pochissimo."
})

# Esercizio 6 - neanche/nemmeno/neppure
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Completare con NEANCHE, NEMMENO o NEPPURE (tutte e tre accettate):\n1. Non capisco ___ una parola di quello che dici.\n2. ___ lui sa rispondere a questa domanda.\n3. Non ho mangiato ___ un boccone.\n4. Non è venuto ___ Marco alla festa.\n5. ___ io sapevo che era il tuo compleanno. Scusa!",
    "resposta": "1. neanche / nemmeno / neppure\n2. Neanche / Nemmeno / Neppure\n3. neanche / nemmeno / neppure\n4. neanche / nemmeno / neppure\n5. Neanche / Nemmeno / Neppure",
    "explicacao": "NEANCHE / NEMMENO / NEPPURE sono sinonimi. Prima del verbo: NON è necessario. Dopo il verbo o in posizione enfatica iniziale: NON non si usa."
})

# Esercizio 7
EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 7** — Lavorare sul testo — La mia nuova casa\n\nDescrivi la tua casa o una casa che conosci, usando almeno 5 comparativi o superlativi.",
    "resposta": "Esempio: La mia nuova casa è molto più grande di quella vecchia. Il soggiorno è il più luminoso di tutti i locali, grazie alle grandi finestre. La cucina è più moderna di quella che avevo prima, ma meno spaziosa del soggiorno. Il mio studio è il più piccolo della casa, ma è il più tranquillo. Il bagno è bellissimo, con una vasca grandissima. Nel complesso, questa casa è migliore di tutte quelle che ho visto prima di sceglierla.",
    "explicacao": "Comparativi: più... di, meno... di. Superlativi relativi: il più/meno + aggettivo + di. Superlativi assoluti: -issimo."
})

# Esercizi di verifica
verifica = [
    ("Roma è più grande di Milano.", "Roma è più grande che Milano.", "Roma è grande più di Milano.", 0,
     "Confronto tra due persone/cose diverse → PIÙ + aggettivo + DI. 'Che' si usa per confrontare due qualità dello stesso soggetto."),
    ("È più simpatico che intelligente.", "È più simpatico di intelligente.", "È simpatico più che intelligente.", 0,
     "Confronto tra due qualità dello stesso soggetto → PIÙ... CHE. 'Di intelligente' sarebbe sbagliato perché intelligente non è una persona."),
    ("Questo è il film più bello che abbia visto.", "Questo è il film più bello che ho visto.", "Questo è il più bello film che abbia visto.", 0,
     "Superlativo relativo con congiuntivo: il film più bello CHE ABBIA visto. L'aggettivo segue il nome: film più bello (non 'più bello film')."),
    ("Questo vino è ottimo.", "Questo vino è buonissimo.", "Entrambe le forme sono corrette.", 2,
     "OTTIMO = superlativo assoluto irregolare di BUONO. BUONISSIMO è il superlativo regolare. Entrambi corretti."),
    ("La situazione è peggiore di quella di ieri.", "La situazione è più cattiva di quella di ieri.", "La situazione è peggio di quella di ieri.", 0,
     "PEGGIORE è l'aggettivo comparativo di CATTIVO. PEGGIO è l'avverbio. 'Più cattiva' è grammaticalmente possibile ma meno elegante."),
    ("Marco studia meno di Luisa.", "Marco studia meno che Luisa.", "Marco studia meno che di Luisa.", 0,
     "Con verbo + nome/pronome → MENO DI. 'Che' si usa per confrontare verbi o aggettivi, non sostantivi in questo contesto."),
    ("Non capisco neanche una parola.", "Non capisco neppure una parola.", "Entrambe le forme sono corrette.", 2,
     "NEANCHE e NEPPURE sono sinonimi perfetti. Entrambi corretti."),
    ("È la più brava studentessa della classe.", "È la studentessa più brava della classe.", "Entrambe le forme sono corrette.", 2,
     "L'aggettivo al superlativo può stare prima o dopo il nome: la più brava studentessa / la studentessa più brava. Entrambe corrette."),
    ("Ho mangiato meglio ieri.", "Ho mangiato più bene ieri.", "Ho mangiato bene di più ieri.", 0,
     "MEGLIO = comparativo di BENE. 'Più bene' non esiste in italiano. 'Bene di più' è possibile con diverso senso."),
    ("Questo esercizio è facilissimo.", "Questo esercizio è facillissimo.", "Questo esercizio è facilissimo.", 0,
     "FACILE + -issimo = facilISSIMO (una sola L). 'Facillissimo' con due L è un errore ortografico."),
    ("È tanto brava quanto sua sorella.", "È cosi brava come sua sorella.", "Entrambe le forme sono corrette.", 2,
     "Comparativo di uguaglianza: TANTO... QUANTO oppure COSÌ... COME. Entrambe corrette e intercambiabili."),
    ("Il prezzo è superiore alle mie aspettative.", "Il prezzo è più alto che le mie aspettative.", "Il prezzo è maggiore che le mie aspettative.", 0,
     "SUPERIORE A: preposizione A (non DI). 'Più alto che' sarebbe per confrontare qualità. 'Maggiore' si usa per quantità/importanza."),
    ("Questo è il problema più piccolo di tutti.", "Questo è il problema minimo di tutti.", "Questo è il problema minore di tutti.", 2,
     "MINORE = comparativo di PICCOLO, usato come superlativo relativo. MINIMO = superlativo assoluto (il più piccolo possibile in assoluto)."),
    ("Non ho studiato nemmeno un po'.", "Non ho nemmeno studiato un po'.", "Entrambe le forme sono corrette.", 2,
     "NEMMENO può stare prima o dopo il verbo con piccole variazioni di enfasi. Entrambe accettabili."),
    ("Questo caffè è pessimo.", "Questo caffè è cattivissimo.", "Entrambe le forme sono corrette.", 2,
     "PESSIMO = superlativo assoluto irregolare di CATTIVO. CATTIVISSIMO è il regolare. Entrambi grammaticalmente corretti."),
    ("Parla più piano possibile.", "Parla il più piano possibile.", "Parla pianissimo.", 1,
     "Con 'possibile': IL PIÙ... POSSIBILE (articolo richiesto). 'Più piano possibile' senza articolo è informale ma accettato."),
    ("La qualità è inferiore al solito.", "La qualità è meno alta del solito.", "Entrambe le forme sono corrette.", 2,
     "INFERIORE A = meno alto di. Entrambe le espressioni sono corrette."),
    ("Ho dormito pochissimo stanotte.", "Ho dormito meno poco stanotte.", "Ho dormito molto poco stanotte.", 0,
     "POCHISSIMO = superlativo assoluto di POCO. 'Meno poco' non è corretto. 'Molto poco' è corretto ma meno elegante."),
    ("Marco è il maggiore dei fratelli.", "Marco è il più grande dei fratelli.", "Entrambe le forme sono corrette.", 2,
     "IL MAGGIORE e IL PIÙ GRANDE: entrambi corretti per indicare il fratello più vecchio/grande."),
    ("Questo divano è comodissimo.", "Questo divano è molto comodo.", "Entrambe le forme sono corrette.", 2,
     "COMODISSIMO (superlativo assoluto) e MOLTO COMODO sono sinonimi perfetti. Entrambi corretti."),
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
    ("Marco è più alto che Luigi.",
     "Marco è più alto di Luigi.",
     "Confronto tra due persone diverse → PIÙ... DI. 'Che' si usa per due qualità dello stesso soggetto."),
    ("Questo film è il più bello che ho mai visto.",
     "Questo film è il più bello che abbia mai visto.",
     "Dopo superlativo relativo → congiuntivo: che ABBIA visto (non indicativo)."),
    ("Ho mangiato più bene di te.",
     "Ho mangiato meglio di te.",
     "MEGLIO = comparativo irregolare di BENE. 'Più bene' non esiste."),
    ("La situazione è più cattiva del previsto.",
     "La situazione è peggiore del previsto.",
     "PEGGIORE = comparativo irregolare di CATTIVO. 'Più cattiva' è possibile ma peggiore è preferito."),
    ("Non capisce neanche le spiega due volte.",
     "Non capisce nemmeno se glielo spiegano due volte.",
     "Frase grammaticalmente incompleta e scorretta. NEANCHE/NEMMENO/NEPPURE si usano per escludere un elemento."),
    ("Questo libro è il più interessante di ho letto.",
     "Questo libro è il più interessante che abbia letto.",
     "Superlativo relativo + proposizione relativa: CHE + congiuntivo (abbia letto). 'Di ho letto' è scorretta."),
    ("Maria è tanto bella di sua sorella.",
     "Maria è tanto bella quanto sua sorella.",
     "Comparativo di uguaglianza: TANTO... QUANTO (non 'di'). Oppure: così... come."),
    ("Questo vino è buonissimo.",
     "Corretta.",
     "BUONISSIMO è il superlativo assoluto regolare di BUONO. Forma corretta."),
    ("È il più grande problema che abbiamo.",
     "È il problema più grande che abbiamo.",
     "L'aggettivo nel superlativo relativo segue il nome: il problema più grande (non 'il più grande problema')."),
    ("Il risultato è superiore di quello previsto.",
     "Il risultato è superiore a quello previsto.",
     "SUPERIORE A (preposizione A). Non 'superiore di': questo comparativo irregolare regge A, non DI."),
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
