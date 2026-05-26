import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XVIII"), None)
if lez is None:
    lez = {"id": "a1-lez18", "num": "Lezione XVIII", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Le preposizioni"
lez["subtitulo"] = "Usi di DI, A, DA, IN, CON, SU, PER, TRA/FRA nelle espressioni idiomatiche"

lez["teoria"] = """\
## Una passeggiata sfortunata

Ieri pomeriggio Maria uscì di casa con l'intenzione di fare una passeggiata nel parco. Camminava tranquillamente per i viali alberati quando, a causa di una buca nel marciapiede, inciampò e cadde. Si fece male a un ginocchio e rimase per terra qualche minuto. Un signore anziano che passava di lì si fermò ad aiutarla. «Come sta?» le chiese con preoccupazione. «Non mi sono fatta niente di grave», rispose Maria, alzandosi con fatica. Il signore la accompagnò fino alla farmacia più vicina, dove il farmacista le mise una fasciatura sul ginocchio. Maria lo ringraziò di cuore e tornò a casa in autobus. Da quella giornata in poi, Maria guarda sempre dove mette i piedi.

---

## A La preposizione DI

**DI** esprime vari rapporti:

| uso | esempio |
|---|---|
| Possesso | il libro **di** Marco |
| Materia | una borsa **di** pelle |
| Argomento | un libro **di** storia |
| Provenienza | sono **di** Roma |
| Specificazione | una tazza **di** caffè |
| Con infinito | ho paura **di** volare |
| Paragone | più grande **di** te |
| Partitivo | ho comprato **del** pane |

---

## B La preposizione A

**A** esprime:

| uso | esempio |
|---|---|
| Luogo (stato/moto a) | abito **a** Roma / vado **a** Roma |
| Tempo | **alle** tre / **a** dicembre |
| Modo | **a** piedi / **a** voce alta |
| Fine/scopo | vado **a** studiare |
| Distanza | **a** due chilometri |
| Con verbi | pensare **a**, credere **a** |

---

## C La preposizione DA

**DA** esprime:

| uso | esempio |
|---|---|
| Provenienza | vengo **da** Firenze |
| Moto da luogo | parto **dall**'Italia |
| Tempo (da quando) | studio italiano **da** tre anni |
| Causa | trema **dal** freddo |
| Scopo/caratteristica | occhiali **da** sole |
| Presso una persona | vado **dal** dottore |

---

## D Preposizioni IN, CON, SU, PER, TRA/FRA

| prep. | uso principale | esempi |
|---|---|---|
| **IN** | luogo (stato/moto) | vivere **in** Italia / entrare **in** casa |
| **IN** | mezzo di trasporto | andare **in** macchina / **in** treno |
| **IN** | tempo futuro | torno **in** un'ora |
| **CON** | compagnia | uscire **con** gli amici |
| **CON** | mezzo/strumento | scrivere **con** la penna |
| **SU** | luogo sopra | il libro è **sul** tavolo |
| **SU** | argomento | un libro **sull**'arte |
| **PER** | scopo/destinazione | parto **per** Roma |
| **PER** | durata | ho aspettato **per** un'ora |
| **TRA/FRA** | posizione intermedia | tra Milano e Torino |
| **TRA/FRA** | tempo futuro | torno **tra** un'ora |

---

## E Espressioni fisse con le preposizioni

**Con A:** a casa, a scuola, a letto, a piedi, a destra/sinistra, a voce, a caso, a proposito, al contrario, a causa di, a differenza di, a meno che.

**Con DI:** di solito, di notte, di giorno, di nuovo, di certo, di fronte a, di moda, di seguito, di recente.

**Con DA:** da solo, da parte, da capo, da vicino, da lontano, dall'altra parte, da allora.

**Con IN:** in fretta, in ritardo, in orario, in anticipo, in punto, in giro, in fondo, in cima, in fila.

**Con PER:** per caso, per fortuna, per piacere, per forza, per niente, per esempio, per conto mio.
"""

lez["exemplos"] = [
    "Vivo a Roma da tre anni. (A = luogo; DA = tempo)",
    "Vado dal medico in macchina. (DA = presso persona; IN = mezzo)",
    "Ho paura di volare. (DI + infinito)",
    "Il libro è sul tavolo vicino alla finestra. (SU + A)",
    "Parto per Londra tra una settimana. (PER = destinazione; TRA = tempo futuro)",
]

EX = []

EX.append({
    "tipo": "revelar",
    "pergunta": "**Domande sul testo** — Una passeggiata sfortunata:\n1. Dove voleva andare Maria?\n2. Cosa le è successo durante la passeggiata?\n3. Chi l'ha aiutata?\n4. Dove l'ha accompagnata il signore?\n5. Come è tornata a casa?\n6. Cosa ha imparato da questa esperienza?",
    "resposta": "1. Voleva andare nel parco a fare una passeggiata.\n2. Ha inciampato in una buca nel marciapiede ed è caduta, facendosi male a un ginocchio.\n3. Un signore anziano che passava di lì si è fermato ad aiutarla.\n4. L'ha accompagnata fino alla farmacia più vicina.\n5. È tornata a casa in autobus.\n6. Da quella giornata in poi guarda sempre dove mette i piedi.",
    "explicacao": "Lessico e preposizioni: nel parco, a causa di, di lì, con preoccupazione, fino alla farmacia, in autobus."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 1** — Completare con la preposizione corretta (semplice o articolata):\n1. Abito ___ Milano ___ tre anni.\n2. Vado ___ medico ogni sei mesi.\n3. Il libro è ___ tavolo.\n4. Parto ___ Roma domani mattina.\n5. Ho paura ___ volare.\n6. Viene ___ Francia; è francese.\n7. Scrivo ___ penna, non ___ computer.\n8. Torno a casa ___ un'ora.\n9. Vive ___ campagna, ___ una piccola casa.\n10. Lavora ___ ospedale come infermiere.",
    "resposta": "1. a / da\n2. dal\n3. sul\n4. per\n5. di\n6. dalla\n7. con la / col\n8. tra / fra\n9. in / in\n10. in",
    "explicacao": "A/IN = luogo stato. DA = provenienza o 'presso'. PER = destinazione. DI = dopo paura, voglia, ecc. CON = mezzo/strumento. TRA/FRA = tempo futuro."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 2** — Scegliere A o IN:\n1. Vivo ___ Italia / ___ Roma.\n2. Vado ___ scuola / ___ università.\n3. Sono ___ casa / ___ ufficio.\n4. Studio ___ biblioteca / ___ camera mia.\n5. Lavoro ___ ospedale / ___ banca.\n6. Vado ___ mercato / ___ supermercato.\n7. Andiamo ___ montagna / ___ mare.\n8. Stanno ___ albergo / ___ pensione.",
    "resposta": "1. in Italia / a Roma (paese/continente→IN; città→A)\n2. a scuola / all'università\n3. a casa / in ufficio\n4. in biblioteca / nella mia camera\n5. in ospedale / in banca\n6. al mercato / al supermercato\n7. in montagna / al mare\n8. in albergo / in pensione",
    "explicacao": "A + città; IN + paese/continente/regione. A casa, a scuola (senza articolo). In ufficio, in banca, in ospedale (senza articolo). Al mercato, al supermercato (con articolo)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 3** — Completare con DA:\n1. Studio italiano ___ sei mesi.\n2. Tremava ___ freddo.\n3. Vengo ___ Milano.\n4. Vado ___ dottore.\n5. Questi sono occhiali ___ sole.\n6. È una tazza ___ tè.\n7. Ho aspettato ___ stamattina.\n8. La stazione è ___ qui a due chilometri.",
    "resposta": "1. da\n2. dal\n3. da\n4. dal\n5. da\n6. da\n7. da\n8. da",
    "explicacao": "DA: tempo (da quando fino ad ora), causa (tremava dal), provenienza, presso (dal dottore), caratteristica (occhiali da sole, tazza da tè), distanza."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 4** — Completare con le espressioni preposizionali:\n1. Di solito mi alzo ___ (di/a) sette.\n2. Per fortuna non è successo niente ___ (di/a) grave.\n3. Torno ___ (tra/in) poco, aspettami!\n4. Ha sbagliato ___ (per/di) caso, non apposta.\n5. L'esame è andato ___ (al/di) contrario delle mie aspettative.\n6. Ho aspettato ___ (per/da) un'ora intera.\n7. ___ (A/Di) proposito, hai chiamato Marco?\n8. Lavoro ___ (da/in) casa oggi.",
    "resposta": "1. alle\n2. di\n3. tra\n4. per\n5. al\n6. per\n7. A\n8. da",
    "explicacao": "Espressioni fisse: alle sette (orario), di grave (partitivo), tra poco (tempo futuro), per caso (avverbio), al contrario (espressione), per un'ora (durata), a proposito (avverbio), da casa (luogo da cui si lavora)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 5** — Conversazione Al ristorante\n\nCompletare il dialogo con le preposizioni mancanti:\n— Buonasera. Avete un tavolo ___ due persone?\n— Sì, ___ corso, venga pure. Preferisce sedersi ___ finestra o ___ fondo?\n— ___ finestra, grazie. Cosa ci consiglia ___ primo?\n— Oggi abbiamo un ottimo risotto ___ funghi.\n— Bene. E ___ secondo?\n— La bistecca ___ ferri o il pesce ___ giorno.",
    "resposta": "— per due persone\n— Di corso\n— vicino alla finestra / alla finestra\n— in fondo\n— Alla finestra\n— di primo / per il primo\n— ai funghi\n— per il secondo / di secondo\n— ai ferri\n— del giorno",
    "explicacao": "Espressioni al ristorante: tavolo per (scopo), di primo/secondo (pasto), ai funghi/ferri (modo), del giorno (specificazione)."
})

EX.append({
    "tipo": "revelar",
    "pergunta": "**Esercizio 6** — Lavorare sul testo — I problemi del traffico\n\nScrivere 6 frasi sui problemi del traffico in città usando le preposizioni: a causa di, in ritardo, per, tra, da, in.",
    "resposta": "Esempio:\n1. A causa del traffico, arrivo sempre in ritardo al lavoro.\n2. In città è più conveniente spostarsi in bicicletta che in macchina.\n3. Tra le ore 8 e le ore 9 il traffico è insopportabile.\n4. Da quando uso i mezzi pubblici, arrivo prima.\n5. Per evitare il traffico, molti partono di notte.\n6. In molte città italiane ci sono zone a traffico limitato nel centro storico.",
    "explicacao": "A causa di = esprime causa. In ritardo = espressione fissa. In bicicletta/macchina = mezzo di trasporto. Tra le ore = intervallo di tempo. Da quando = tempo. Per + infinito = scopo."
})

verifica = [
    ("Vivo a Milano da tre anni.", "Vivo in Milano da tre anni.", "Vivo a Milano per tre anni.", 0,
     "A + città (A Milano). IN + paesi/regioni. DA + tempo (continuo fino al presente): da tre anni. PER + durata limitata: per tre anni (non più in corso)."),
    ("Vado dal medico domani.", "Vado al medico domani.", "Vado dal medico domani.", 0,
     "DAL medico: presso la persona (=allo studio del medico). Entrambe 'dal' e 'al' sono usate, ma DAL è più preciso."),
    ("Ho paura di volare.", "Ho paura a volare.", "Ho paura per volare.", 0,
     "PAURA DI + infinito. 'Paura a' e 'paura per' non si usano in italiano."),
    ("Studio italiano da sei mesi.", "Studio italiano per sei mesi.", "Studio italiano in sei mesi.", 0,
     "DA + tempo che continua fino al presente: da sei mesi (e continuo a studiare). PER: durata conclusa. IN: tempo per completare qualcosa."),
    ("Il treno parte tra dieci minuti.", "Il treno parte in dieci minuti.", "Il treno parte fra dieci minuti.", 2,
     "TRA e FRA sono sinonimi: entrambi corretti per indicare tempo futuro. 'In dieci minuti' significa in un lasso di dieci minuti, diverso significato."),
    ("Andiamo in vacanza in Spagna.", "Andiamo in vacanza a Spagna.", "Andiamo in vacanza nella Spagna.", 0,
     "IN + paese/nazione: in Spagna. A + città: a Madrid. 'Nella Spagna' con articolo è accettato ma non standard."),
    ("Sono uscito di casa senza chiavi.", "Sono uscito da casa senza chiavi.", "Entrambe le forme sono corrette.", 2,
     "USCIRE DI CASA (espressione fissa) e USCIRE DA CASA sono entrambe corrette e comuni nell'italiano parlato."),
    ("Torno a casa in un'ora.", "Torno a casa tra un'ora.", "Torno a casa per un'ora.", 1,
     "TRA un'ora = dopo un'ora (tempo futuro). IN un'ora = nel giro di un'ora (durata per completare). PER un'ora = per una durata di un'ora."),
    ("Scrivo con la matita.", "Scrivo di matita.", "Scrivo alla matita.", 0,
     "Strumento: CON + la + strumento. 'Di matita' non si usa. 'Alla matita' non è italiano standard."),
    ("È una camicia di seta.", "È una camicia in seta.", "Entrambe le forme sono corrette.", 2,
     "Materia: DI seta (standard) o IN seta (entrambe accettate). 'Una camicia in seta' e 'una camicia di seta' sono equivalenti."),
    ("Abita in una villa di campagna.", "Abita in una villa da campagna.", "Abita a una villa di campagna.", 0,
     "DI campagna = specificazione del tipo (villa di campagna). 'Da campagna' non si usa. IN + villa (luogo)."),
    ("Vengo dalla Francia.", "Vengo di Francia.", "Vengo da Francia.", 0,
     "DA + LA + Francia = DALLA Francia (provenienza con articolo). 'Di Francia' non indica provenienza. 'Da Francia' senza articolo sarebbe sbagliato."),
    ("Ho aspettato per due ore.", "Ho aspettato di due ore.", "Ho aspettato da due ore.", 0,
     "Durata conclusa: PER due ore (= durante due ore, e poi ho smesso). 'Da due ore' indicherebbe che sto ancora aspettando."),
    ("Vado in bicicletta al lavoro.", "Vado con bicicletta al lavoro.", "Vado a bicicletta al lavoro.", 0,
     "Mezzo di trasporto: IN bicicletta, IN macchina, IN treno. CON la bicicletta è anche corretto. 'A bicicletta' non si usa."),
    ("Parliamo di politica spesso.", "Parliamo sulla politica spesso.", "Parliamo in politica spesso.", 0,
     "PARLARE DI: argomento. 'Parlare sulla politica' è calco straniero. 'In politica' significa 'nel campo della politica'."),
    ("Abito su per i quaranta anni.", "Ho su per i quaranta anni.", "Ho sui quaranta anni.", 2,
     "Età approssimativa: SUI quaranta anni (corretto). 'Abito su per' è scorretta. 'Ho su per i quaranta' è popolare ma non standard."),
    ("Per caso hai visto Marco?", "Di caso hai visto Marco?", "A caso hai visto Marco?", 0,
     "PER CASO = casualmente (domanda educata). 'Di caso' non esiste. 'A caso' = in modo casuale/random, diverso significato."),
    ("È un film sul Rinascimento.", "È un film del Rinascimento.", "È un film di Rinascimento.", 0,
     "SUL = su + il: argomento. 'Del Rinascimento' indicherebbe un film prodotto nel Rinascimento. 'Di Rinascimento' non è standard."),
    ("Tra noi non ci sono segreti.", "Fra noi non ci sono segreti.", "Entrambe le forme sono corrette.", 2,
     "TRA e FRA sono sinonimi perfetti anche nella posizione intermedia: tra noi = fra noi."),
    ("Ho fatto male di non studiare.", "Ho fatto male a non studiare.", "Ho sbagliato a non studiare.", 1,
     "FARE MALE A + infinito. 'Fare male di' non esiste. 'Sbagliare a' è sinonimo corretto."),
]

for a, b, c, r, expl in verifica:
    EX.append({
        "tipo": "escolha",
        "pergunta": "**Esercizi di verifica** — Scegliere la preposizione corretta:",
        "opcoes": [a, b, c],
        "resposta": r,
        "explicacao": expl
    })

errori = [
    ("Vivo in Roma da dieci anni.",
     "Vivo a Roma da dieci anni.",
     "A + città: A Roma. IN si usa con paesi (in Italia), regioni (in Toscana), non con città."),
    ("Ho paura a sbagliare l'esame.",
     "Ho paura di sbagliare l'esame.",
     "Paura DI + infinito. 'Paura a' non esiste in italiano."),
    ("Studio italiano per tre anni e non riesco ancora a parlarlo.",
     "Studio italiano da tre anni e non riesco ancora a parlarlo.",
     "Azione iniziata nel passato che continua → DA (tre anni). PER indica durata conclusa."),
    ("Sono andato al mio amico ieri.",
     "Sono andato dal mio amico ieri. / Sono andato a casa del mio amico ieri.",
     "DAL + persona = presso la persona. 'Al mio amico' si usa solo con certi verbi (dare al, parlare al, ecc.)."),
    ("Abita a campagna, non in città.",
     "Abita in campagna, non in città.",
     "IN campagna (luogo generale). A + città specifica. 'A campagna' senza articolo non si usa."),
    ("Parto per Roma in due ore.",
     "Parto per Roma tra due ore.",
     "Tempo futuro: TRA due ore (= dopo due ore). IN due ore = nel giro di due ore (durata)."),
    ("Ho lavorato per questa azienda da dieci anni.",
     "Corretta. (o: Lavoro per questa azienda da dieci anni, se ancora lavora)",
     "PER questa azienda (scopo/relazione). DA dieci anni (tempo continuato). Se l'azione è terminata: 'ho lavorato per... per dieci anni'."),
    ("Vengo di Milano.",
     "Vengo da Milano.",
     "Provenienza: VENGO DA + città. 'Vengo di' non si usa per provenienza."),
    ("Ho bisogno a riposarmi.",
     "Ho bisogno di riposarmi.",
     "Aver bisogno DI + infinito/sostantivo. 'Bisogno a' non esiste."),
    ("Scrivo in penna stilografica.",
     "Scrivo con la penna stilografica.",
     "Strumento: CON + articolo + strumento. 'Scrivere in penna' non è standard (si dice 'a matita' solo per matita)."),
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
