import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XX"), None)
if lez is None:
    lez = {"id": "a1-lez20", "num": "Lezione XX", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "Il periodo ipotetico"
lez["subtitulo"] = "Frasi condizionali con se: realtà, possibilità e impossibilità"
lez["exemplos"] = [
    "Se ho tempo, vengo da te.",
    "Se avessi tempo, verrei da te.",
    "Se avessi avuto tempo, sarei venuto da te.",
    "Se fa bello, andiamo al mare.",
    "Se facesse bello, andremmo al mare.",
    "Se avesse fatto bello, saremmo andati al mare."
]

lez["teoria"] = """<h3>Il periodo ipotetico</h3>
<p>Il <strong>periodo ipotetico</strong> è una frase composta da una <em>protasi</em> (condizione con <strong>se</strong>) e un'<em>apodosi</em> (conseguenza). In italiano esistono tre tipi fondamentali.</p>

<h4>I tre tipi di periodo ipotetico</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Periodo ipotetico — schema</th>
  </tr>
  <tr>
    <th class="gram-art">Tipo</th>
    <th class="gram-art">Significato</th>
    <th class="gram-art">Protasi (SE + ...)</th>
    <th class="gram-art">Apodosi</th>
  </tr>
  <tr>
    <td><strong>Realtà</strong></td>
    <td>Condizione possibile/reale</td>
    <td>Indicativo presente/futuro</td>
    <td>Indicativo presente/futuro</td>
  </tr>
  <tr>
    <td><strong>Possibilità</strong></td>
    <td>Condizione ipotetica (presente/futuro)</td>
    <td>Congiuntivo imperfetto</td>
    <td>Condizionale presente</td>
  </tr>
  <tr>
    <td><strong>Impossibilità</strong></td>
    <td>Condizione irreale (passato)</td>
    <td>Congiuntivo trapassato</td>
    <td>Condizionale passato</td>
  </tr>
</table>

<h4>Tipo 1 — Realtà</h4>
<p>La condizione è <strong>reale o molto probabile</strong>. Si usa l'indicativo in entrambe le frasi.</p>
<ul>
  <li><em>Se <strong>ho</strong> tempo, <strong>vengo</strong> da te.</em> (= forse ho tempo)</li>
  <li><em>Se <strong>piove</strong>, <strong>resto</strong> a casa.</em></li>
  <li><em>Se <strong>avrai</strong> fame, <strong>mangeremo</strong> qualcosa.</em></li>
</ul>

<h4>Tipo 2 — Possibilità</h4>
<p>La condizione è <strong>ipotetica ma possibile</strong> nel presente o futuro. Si usa il congiuntivo imperfetto nella protasi e il condizionale presente nell'apodosi.</p>
<ul>
  <li><em>Se <strong>avessi</strong> tempo, <strong>verrei</strong> da te.</em> (= non ho tempo adesso)</li>
  <li><em>Se <strong>facesse</strong> bello, <strong>andremmo</strong> al mare.</em></li>
  <li><em>Se <strong>fossi</strong> ricco, <strong>comprerei</strong> una villa.</em></li>
</ul>

<h4>Tipo 3 — Impossibilità</h4>
<p>La condizione è <strong>irreale e impossibile</strong> perché si riferisce al passato. Si usa il congiuntivo trapassato nella protasi e il condizionale passato nell'apodosi.</p>
<ul>
  <li><em>Se <strong>avessi avuto</strong> tempo, <strong>sarei venuto</strong> da te.</em> (= non avevo tempo)</li>
  <li><em>Se <strong>avesse fatto</strong> bello, <strong>saremmo andati</strong> al mare.</em></li>
  <li><em>Se <strong>fossi partito</strong> prima, <strong>saresti arrivato</strong> in tempo.</em></li>
</ul>

<h4>Attenzione!</h4>
<p>Dopo <strong>se</strong> non si usa mai:</p>
<ul>
  <li>❌ il condizionale (<em>Se verrei</em> — sbagliato!)</li>
  <li>❌ il congiuntivo presente (<em>Se venga</em> — sbagliato!)</li>
  <li>✅ solo indicativo (tipo 1) o congiuntivo imperfetto/trapassato (tipi 2 e 3)</li>
</ul>

<h4>Periodo ipotetico misto</h4>
<p>A volte la protasi e l'apodosi hanno tempi diversi:</p>
<ul>
  <li><em>Se <strong>fossi partito</strong> ieri, <strong>sarei</strong> già a Roma.</em> (passato → presente)</li>
  <li><em>Se <strong>avessi studiato</strong> di più, <strong>parleresti</strong> meglio italiano.</em></li>
</ul>

<h4>Dialogo: Una vacanza mancata</h4>
<p><strong>Luca:</strong> Se avessi più ferie, verrei in vacanza con voi.<br>
<strong>Anna:</strong> Peccato! Se fossi venuto, ci saremmo divertiti molto.<br>
<strong>Luca:</strong> Lo so. Se avessi prenotato prima, avrei trovato anche un volo più economico.<br>
<strong>Anna:</strong> La prossima volta, se prenoti in anticipo, risparmi sicuramente.<br>
<strong>Luca:</strong> Hai ragione. Se potessi, partirei subito!</p>"""

lez["exercicios"] = [
    # --- REVELAR exercises ---
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Tipo 1 (realtà). Completa con l'indicativo:\n1. Se ___ (fare) bello domani, andiamo al mare.\n2. Se Mario ___ (avere) fame, mangia qualcosa.\n3. Se voi ___ (arrivare) tardi, aspettiamo.\n4. Se lei ___ (studiare) ogni giorno, imparerà presto.",
        "resposta": "1. fa | 2. ha | 3. arrivate | 4. studia"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Tipo 2 (possibilità). Completa con congiuntivo imperfetto + condizionale presente:\n1. Se ___ (avere) più soldi, ___ (comprare) una casa grande.\n2. Se ___ (sapere) la risposta, te la ___ (dire).\n3. Se lui ___ (venire) alla festa, ___ (divertirsi).\n4. Se voi ___ (lavorare) meno, ___ (stare) meglio.",
        "resposta": "1. avessi / comprerei | 2. sapessi / direi | 3. venisse / si divertirebbe | 4. lavoraste / stareste"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Tipo 3 (impossibilità). Completa con congiuntivo trapassato + condizionale passato:\n1. Se ___ (partire) prima, ___ (arrivare) in orario.\n2. Se lei ___ (studiare) di più, ___ (superare) l'esame.\n3. Se loro ___ (prenotare) in anticipo, ___ (trovare) un posto.\n4. Se tu ___ (venire), ci ___ (divertire) insieme.",
        "resposta": "1. fossi partito / sarei arrivato | 2. avesse studiato / avrebbe superato | 3. avessero prenotato / avrebbero trovato | 4. fossi venuto / ci saremmo divertiti"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Identifica il tipo (1/2/3) e completa:\n1. Se ___ (potere — tipo 2) partire, verrei subito.\n2. Se ___ (piovere — tipo 1) domani, rimango a casa.\n3. Se ___ (sapere — tipo 3) la verità, non l'avrei detto.\n4. Se ___ (essere — tipo 2) in vacanza, leggerei molto.",
        "resposta": "1. potessi | 2. piove | 3. avessi saputo | 4. fossi"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — Trasforma: tipo 1 → tipo 2:\n1. Se ho tempo, vengo. → Se ___, ___.\n2. Se fa bello, usciamo. → Se ___, ___.\n3. Se parli italiano, capisci. → Se ___, ___.",
        "resposta": "1. avessi tempo, verrei | 2. facesse bello, usciremmo | 3. parlassi italiano, capiresti"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Trasforma: tipo 2 → tipo 3:\n1. Se avessi tempo, verrei. → Se ___, ___.\n2. Se sapessi la risposta, te la direi. → Se ___, ___.\n3. Se lui lavorasse meno, starebbe meglio. → Se ___, ___.",
        "resposta": "1. avessi avuto tempo, sarei venuto | 2. avessi saputo la risposta, te l'avrei detta | 3. avesse lavorato meno, sarebbe stato meglio"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Completa liberamente l'apodosi:\n1. Se vincessi alla lotteria, ___.\n2. Se fossi nato in Italia, ___.\n3. Se avessi studiato medicina, ___.\n4. Se potessi viaggiare nel tempo, ___.",
        "resposta": "(risposta libera) Es: comprerei una villa / parlerei italiano perfettamente / sarei medico / andrei nel futuro"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Periodo ipotetico misto. Completa:\n1. Se ___ (studiare) di più da giovane, oggi ___ (avere) un lavoro migliore.\n2. Se ___ (partire) ieri, adesso ___ (essere) già a Parigi.\n3. Se ___ (prendere) l'ombrello, ora non ___ (essere) bagnato.",
        "resposta": "1. avessi studiato / avrei | 2. fossi partito / sarei | 3. avessi preso / sarei"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "Se ___ tempo, vengo da te. (tipo realtà)",
        "opcoes": ["avessi", "avrò", "ho", "avrei"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se ___ più soldi, comprerei una macchina nuova.",
        "opcoes": ["ho", "avevo", "avessi", "avrei"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se lei ___ studiato, avrebbe superato l'esame.",
        "opcoes": ["ha", "avesse", "abbia", "avrebbe"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Se facesse bello, ___ al mare.",
        "opcoes": ["andiamo", "siamo andati", "andremmo", "andassimo"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se ___ partito prima, saresti arrivato in tempo.",
        "opcoes": ["sei", "fossi", "saresti", "sia"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Dopo SE non si usa mai:",
        "opcoes": ["l'indicativo", "il congiuntivo imperfetto", "il condizionale", "il congiuntivo trapassato"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se piove domani, ___ a casa.",
        "opcoes": ["resterei", "restassi", "resto", "sia restato"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se avessi saputo la verità, ___ diversamente.",
        "opcoes": ["agisco", "agirei", "avrei agito", "abbia agito"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Nel tipo 2 del periodo ipotetico, l'apodosi usa:",
        "opcoes": ["il futuro", "il condizionale presente", "il congiuntivo imperfetto", "l'imperfetto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Se ___ in Italia, parleresti italiano perfettamente.",
        "opcoes": ["vivi", "vivessi", "vivrai", "vivevi"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Se avesse preso l'ombrello, non ___ bagnato.",
        "opcoes": ["si sarebbe", "si sia", "si fosse", "sarà"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Se voi ___ prima, avremmo cenato insieme.",
        "opcoes": ["arrivaste", "arriviate", "foste arrivati", "siete arrivati"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se ___ ricco, viaggerei per il mondo.",
        "opcoes": ["sono", "sia", "fossi", "sarò"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Nel tipo 3, la protasi usa:",
        "opcoes": ["congiuntivo presente", "congiuntivo imperfetto", "congiuntivo trapassato", "indicativo passato"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se Maria ___ (tipo 1) stanca, si riposa.",
        "opcoes": ["fosse", "sia", "è", "sarà stata"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Se avessimo studiato di più, ___ l'esame.",
        "opcoes": ["superiamo", "avremmo superato", "supereremmo", "avessimo superato"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Se ___ partire adesso, arriverei in tempo.",
        "opcoes": ["potessi", "possa", "posso", "potrei"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Se avessi letto il libro, ___ rispondere alle domande.",
        "opcoes": ["potrei", "potresti", "avresti potuto", "potrò"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale frase è corretta?",
        "opcoes": ["Se verrei, ti aiuterei.", "Se venissi, ti aiuterei.", "Se venga, ti aiuto.", "Se vengo, ti aiuterei."],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Se non ___ tanto, stareste meglio.",
        "opcoes": ["mangiate", "mangiate", "mangiaste", "mangereste"],
        "resposta": 2
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Se verrei da te, potremmo parlare.\n2. Se avesse più tempo, viene con noi.\n3. Se avrei saputo, ti avrei detto.\n4. Se pioverà domani, sarei rimasto a casa.\n5. Se venisse, avrebbe detto qualcosa.",
        "resposta": "1. venissi | 2. verrebbe | 3. avessi saputo | 4. piove / rimarrò | 5. CORRETTA"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Se avessi studiato, passeresti l'esame. (tipo 3)\n2. Se avesse piovuto, siamo rimasti a casa.\n3. Se posso, vengo — questa frase è sbagliata?\n4. Se fosse ricco, comprava una villa.",
        "resposta": "1. avresti passato | 2. saremmo rimasti | 3. CORRETTA (tipo 1) | 4. comprerebbe"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
