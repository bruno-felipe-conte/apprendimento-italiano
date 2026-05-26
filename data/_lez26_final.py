import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

lez = next((u for u in modulo["unidades"] if u["num"] == "Lezione XXVI"), None)
if lez is None:
    lez = {"id": "a1-lez26", "num": "Lezione XXVI", "titulo": "", "subtitulo": "",
           "teoria": "", "exemplos": [], "exercicios": []}
    modulo["unidades"].append(lez)

lez["titulo"] = "I numeri, la data e l'ora"
lez["subtitulo"] = "Numeri cardinali e ordinali, espressioni di data, ora e durata"
lez["exemplos"] = [
    "Sono le tre e un quarto.",
    "Oggi è il venticinque maggio duemilasedici.",
    "Il treno parte alle diciassette e trenta.",
    "Vivo in Italia da tre anni.",
    "È la prima volta che vengo a Roma.",
    "Il negozio chiude alle venti."
]

lez["teoria"] = """<h3>I numeri, la data e l'ora</h3>

<h4>Numeri cardinali (0–1000)</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Numeri cardinali</th>
  </tr>
  <tr>
    <th class="gram-art">Numero</th>
    <th class="gram-art">Italiano</th>
    <th class="gram-art">Numero</th>
    <th class="gram-art">Italiano</th>
  </tr>
  <tr><td>0</td><td>zero</td><td>11</td><td>undici</td></tr>
  <tr><td>1</td><td>uno/una</td><td>12</td><td>dodici</td></tr>
  <tr><td>2</td><td>due</td><td>13</td><td>tredici</td></tr>
  <tr><td>3</td><td>tre</td><td>14</td><td>quattordici</td></tr>
  <tr><td>4</td><td>quattro</td><td>15</td><td>quindici</td></tr>
  <tr><td>5</td><td>cinque</td><td>16</td><td>sedici</td></tr>
  <tr><td>6</td><td>sei</td><td>17</td><td>diciassette</td></tr>
  <tr><td>7</td><td>sette</td><td>18</td><td>diciotto</td></tr>
  <tr><td>8</td><td>otto</td><td>19</td><td>diciannove</td></tr>
  <tr><td>9</td><td>nove</td><td>20</td><td>venti</td></tr>
  <tr><td>10</td><td>dieci</td><td>21</td><td>ventuno</td></tr>
  <tr><td>30</td><td>trenta</td><td>40</td><td>quaranta</td></tr>
  <tr><td>50</td><td>cinquanta</td><td>60</td><td>sessanta</td></tr>
  <tr><td>70</td><td>settanta</td><td>80</td><td>ottanta</td></tr>
  <tr><td>90</td><td>novanta</td><td>100</td><td>cento</td></tr>
  <tr><td>200</td><td>duecento</td><td>1.000</td><td>mille</td></tr>
  <tr><td>2.000</td><td>duemila</td><td>1.000.000</td><td>un milione</td></tr>
</table>
<p><strong>Note:</strong> davanti a -uno e -otto si elide la vocale: <em>vent<strong>uno</strong>, trent<strong>otto</strong></em> (non ventouno). Tre finale accentato in composizione: <em>ventit<strong>ré</strong>, trentat<strong>ré</strong></em>.</p>

<h4>Numeri ordinali</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="4">Numeri ordinali</th>
  </tr>
  <tr>
    <th class="gram-art">Numero</th>
    <th class="gram-art">Ordinale</th>
    <th class="gram-art">Numero</th>
    <th class="gram-art">Ordinale</th>
  </tr>
  <tr><td>1°</td><td>primo/a</td><td>7°</td><td>settimo/a</td></tr>
  <tr><td>2°</td><td>secondo/a</td><td>8°</td><td>ottavo/a</td></tr>
  <tr><td>3°</td><td>terzo/a</td><td>9°</td><td>nono/a</td></tr>
  <tr><td>4°</td><td>quarto/a</td><td>10°</td><td>decimo/a</td></tr>
  <tr><td>5°</td><td>quinto/a</td><td>11°</td><td>undicesimo/a</td></tr>
  <tr><td>6°</td><td>sesto/a</td><td>20°</td><td>ventesimo/a</td></tr>
</table>
<p>Dal 11° in poi: si aggiunge <strong>-esimo/a</strong> al numero cardinale (togliendo la vocale finale se c'è): <em>undicesimo, ventesimo, centesimo</em>.</p>

<h4>L'ora</h4>
<p>Per chiedere l'ora: <strong>Che ore sono? / Che ora è?</strong></p>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">Espressioni dell'ora</th>
  </tr>
  <tr>
    <th class="gram-art">Ora</th>
    <th class="gram-art">Come si dice</th>
  </tr>
  <tr><td>1:00</td><td>È l'una.</td></tr>
  <tr><td>2:00</td><td>Sono le due.</td></tr>
  <tr><td>3:15</td><td>Sono le tre e un quarto.</td></tr>
  <tr><td>4:30</td><td>Sono le quattro e mezza / mezzo.</td></tr>
  <tr><td>5:45</td><td>Sono le sei meno un quarto.</td></tr>
  <tr><td>12:00</td><td>È mezzogiorno.</td></tr>
  <tr><td>24:00</td><td>È mezzanotte.</td></tr>
  <tr><td>17:30</td><td>Sono le diciassette e trenta. (orario ufficiale)</td></tr>
</table>

<h4>La data</h4>
<p>Per chiedere la data: <strong>Quanti ne abbiamo oggi? / Qual è la data di oggi?</strong></p>
<ul>
  <li>Per il primo del mese si usa l'ordinale: <em>il <strong>primo</strong> gennaio</em></li>
  <li>Per gli altri giorni si usano i cardinali: <em>il <strong>due</strong> febbraio, il <strong>venticinque</strong> marzo</em></li>
  <li>L'anno si legge come numero cardinale: <em>il <strong>duemilaventisei</strong></em></li>
</ul>
<p><strong>Formula completa:</strong> <em>Oggi è il venticinque maggio duemilaventisei.</em></p>

<h4>Espressioni di durata</h4>
<table class="gram-table-rich">
  <tr>
    <th class="gram-genere" colspan="2">DA, PER, FA, TRA/FRA + tempo</th>
  </tr>
  <tr>
    <th class="gram-art">Espressione</th>
    <th class="gram-art">Significato ed esempio</th>
  </tr>
  <tr><td><strong>da</strong> + durata</td><td>azione iniziata nel passato e ancora in corso: <em>Studio italiano da due anni.</em></td></tr>
  <tr><td><strong>per</strong> + durata</td><td>durata limitata: <em>Ho studiato per due ore.</em></td></tr>
  <tr><td><strong>fa</strong></td><td>tempo trascorso da un evento passato: <em>Sono arrivato tre giorni fa.</em></td></tr>
  <tr><td><strong>tra/fra</strong> + durata</td><td>nel futuro: <em>Parto tra due giorni.</em></td></tr>
</table>

<h4>Dialogo: Un appuntamento</h4>
<p><strong>Lucia:</strong> A che ora ci vediamo domani?<br>
<strong>Paolo:</strong> Che ne dici delle dieci e mezza?<br>
<strong>Lucia:</strong> Va bene. Dove?<br>
<strong>Paolo:</strong> Al bar in piazza. È il terzo a destra dall'uscita della metro.<br>
<strong>Lucia:</strong> Perfetto. Quanti ne abbiamo domani?<br>
<strong>Paolo:</strong> Il ventisette. Ci vediamo alle dieci e trenta allora.<br>
<strong>Lucia:</strong> A domani! Ah, non sono stata lì da almeno tre mesi.</p>"""

lez["exercicios"] = [
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 1 — Scrivi in lettere:\n1. 15 → ___\n2. 23 → ___\n3. 38 → ___\n4. 56 → ___\n5. 100 → ___\n6. 1.000 → ___",
        "resposta": "1. quindici | 2. ventitré | 3. trentotto | 4. cinquantasei | 5. cento | 6. mille"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 2 — Scrivi l'ordinale (maschile):\n1. 1° → ___\n2. 3° → ___\n3. 5° → ___\n4. 8° → ___\n5. 12° → ___\n6. 20° → ___",
        "resposta": "1. primo | 2. terzo | 3. quinto | 4. ottavo | 5. dodicesimo | 6. ventesimo"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 3 — Che ore sono? Scrivi in parole:\n1. 1:00 → ___\n2. 3:15 → ___\n3. 7:30 → ___\n4. 9:45 → ___\n5. 12:00 → ___\n6. 24:00 → ___",
        "resposta": "1. È l'una | 2. Sono le tre e un quarto | 3. Sono le sette e mezza | 4. Sono le dieci meno un quarto | 5. È mezzogiorno | 6. È mezzanotte"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 4 — Scrivi la data in parole:\n1. 01/01 → ___\n2. 14/02 → ___\n3. 25/04 → ___\n4. 08/03 → ___\n5. 31/12 → ___",
        "resposta": "1. il primo gennaio | 2. il quattordici febbraio | 3. il venticinque aprile | 4. l'otto marzo | 5. il trentuno dicembre"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 5 — DA, PER, FA o TRA/FRA:\n1. Studio italiano ___ due anni. (azione ancora in corso)\n2. Ho lavorato ___ sei ore ieri.\n3. Sono arrivato tre giorni ___.\n4. Partiremo ___ una settimana.",
        "resposta": "1. da | 2. per | 3. fa | 4. tra / fra"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 6 — Domande e risposte sull'ora:\n1. «Che ore sono?» — 15:20 → ___\n2. «A che ora apre il museo?» — 09:00 → ___\n3. «Quando parte il treno?» — 17:45 → ___",
        "resposta": "1. Sono le tre e venti | 2. Apre alle nove | 3. Parte alle diciassette e quarantacinque / alle diciotto meno un quarto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 7 — Numeri grandi. Scrivi in lettere:\n1. 2.026 → ___\n2. 1.500 → ___\n3. 3.000.000 → ___\n4. 250 → ___",
        "resposta": "1. duemilaventisei | 2. millecinquecento | 3. tre milioni | 4. duecentocinquanta"
    },
    {
        "tipo": "revelar",
        "pergunta": "Esercizio 8 — Costruisci frasi complete:\n1. Vivere in Italia / da / 5 anni → ___\n2. Il film inizia / alle / 20:30 → ___\n3. L'esame / è / il / 15 / giugno → ___\n4. Sono arrivato / 2 settimane / fa → ___",
        "resposta": "1. Vivo in Italia da cinque anni | 2. Il film inizia alle venti e trenta | 3. L'esame è il quindici giugno | 4. Sono arrivato due settimane fa"
    },

    # --- ESCOLHA: Esercizi di verifica ---
    {
        "tipo": "escolha",
        "pergunta": "Come si dice 21 in italiano?",
        "opcoes": ["ventiuno", "ventuno", "ventieuno", "ventuno"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Il numero ordinale di 3° è:",
        "opcoes": ["terzo", "terzimo", "tresimo", "trigesimo"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Sono le 4:30. Come si dice?",
        "opcoes": ["Sono le quattro e trenta", "Sono le quattro e mezza", "È le quattro e trenta", "Sono le quattro meno mezza"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si dice 1:00?",
        "opcoes": ["Sono le uno", "È l'una", "È uno", "Sono le una"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Per il primo giorno del mese si usa:",
        "opcoes": ["il numero cardinale", "il numero ordinale (primo)", "il numero zero", "nessuno dei due"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Studio italiano ___ tre anni. (azione ancora in corso)",
        "opcoes": ["per", "fa", "da", "tra"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Sono arrivato due giorni ___.",
        "opcoes": ["da", "per", "tra", "fa"],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si dice 9:45?",
        "opcoes": ["Sono le nove e quarantacinque", "Sono le dieci meno un quarto", "Sono le nove e tre quarti", "Sono le dieci meno quindici"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "L'ordinale dal 11° in poi si forma aggiungendo:",
        "opcoes": ["-esimo al cardinale", "-imo al cardinale", "-mo al cardinale", "-asso al cardinale"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si scrive 33 in lettere?",
        "opcoes": ["trentetre", "trentatré", "trentitré", "tretatre"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Partirò ___ due settimane. (nel futuro)",
        "opcoes": ["da", "fa", "per", "tra"],
        "resposta": 3
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si dice 12:00 (mezzogiorno)?",
        "opcoes": ["Sono le dodici", "È mezzogiorno", "entrambe sono corrette", "nessuna delle due"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si legge la data 08/03?",
        "opcoes": ["l'otto marzo", "il otto marzo", "l'ottavo marzo", "ottobre marzo"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Ho lavorato ___ otto ore. (durata finita)",
        "opcoes": ["da", "tra", "per", "fa"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si dice 2.000?",
        "opcoes": ["duomila", "duemila", "duemile", "doemila"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Sono le 5:45. L'altra forma corretta è:",
        "opcoes": ["sono le sei meno un quarto", "sono le cinque e tre quarti", "entrambe corrette", "nessuna delle due"],
        "resposta": 2
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si dice il numero 18?",
        "opcoes": ["diciassette", "diciotto", "dieciotto", "oiciotto"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "L'ordinale femminile di 5° è:",
        "opcoes": ["quinta", "quinto", "cinqueesima", "quintima"],
        "resposta": 0
    },
    {
        "tipo": "escolha",
        "pergunta": "Qual è la domanda corretta per chiedere la data?",
        "opcoes": ["Che ora è?", "Quanti ne abbiamo oggi?", "Quanto costa?", "Chi è oggi?"],
        "resposta": 1
    },
    {
        "tipo": "escolha",
        "pergunta": "Come si dice 17:30 in orario ufficiale?",
        "opcoes": ["Sono le cinque e mezza di pomeriggio", "Sono le diciassette e trenta", "Sono le diciassette e mezza", "entrambe b e c sono corrette"],
        "resposta": 3
    },

    # --- REVELAR: Trovare gli errori ---
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori — correggi la frase:\n1. Sono le uno. (1:00)\n2. Il primo del mese si dice «il uno».\n3. Studio italiano per due anni. (azione ancora in corso)\n4. Sono arrivato da tre giorni. (tempo trascorso)\n5. Come si dice 21? «Ventiuno» — è corretto?",
        "resposta": "1. È l'una | 2. il primo | 3. da due anni | 4. tre giorni fa | 5. SÌ, corretto"
    },
    {
        "tipo": "revelar",
        "pergunta": "Trovare gli errori (2) — correggi la frase:\n1. Parto tra due giorni — è corretto?\n2. Il dodicesimo piano (12°) — è corretto?\n3. Sono le dieci meno trenta. (9:30)\n4. Ho lavorato da sei ore ieri.",
        "resposta": "1. SÌ, corretto | 2. SÌ, corretto | 3. Sono le nove e mezza | 4. per sei ore"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {lez['titulo']}")
print(f"Teoria: {len(lez['teoria'])} chars")
print(f"Exercicios: {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
