import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

imitazioni_list = []

# 50 Frases Icônicas para Imitação Fonética
frases = [
    ("Mamma mia!", "Mãe minha! (Nossa!)", "A1", "Espressione classica di stupore."),
    ("Che bello!", "Que lindo!", "A1", "Per esprimere ammirazione."),
    ("Buongiorno principessa!", "Bom dia princesa! (La vita è bella)", "A2", "Frase iconica dal film La Vita è Bella."),
    ("Non ci piove.", "Não há dúvida sobre isso.", "B1", "Espressione idiomatica per certezza."),
    ("Lasciatemi cantare.", "Deixem-me cantar. (L'Italiano)", "A2", "Dalla famosa canzone di Toto Cutugno."),
    ("La dolce vita.", "A doce vida.", "A1", "Dal film capolavoro di Fellini."),
    ("In bocca al lupo!", "Boa sorte!", "A2", "Per augurare buona fortuna."),
    ("Crepi il lupo!", "Que morra o lobo! (Obrigado!)", "A2", "Risposta classica a in bocca al lupo."),
    ("Piano piano si va lontano.", "Devagar se vai longe.", "A2", "Proverbio italiano."),
    ("Meglio tardi che mai.", "Antes tarde do que nunca.", "A2", "Proverbio comune."),
    ("Veni, vidi, vici.", "Vim, vi, venci.", "B2", "Latino usato in italiano, di Giulio Cesare."),
    ("Eppur si muove.", "E no entanto ela se move.", "B2", "Attribuita a Galileo Galilei."),
    ("Una pizza Margherita, per favore.", "Uma pizza Margherita, por favor.", "A1", "Richiesta tipica al ristorante."),
    ("Scusa il ritardo.", "Desculpe o atraso.", "A1", "Per scusarsi di un ritardo."),
    ("Non ho capito.", "Não entendi.", "A1", "Frase utile per i principianti."),
    ("Piacere di conoscerti.", "Prazer em te conhecer.", "A1", "Presentazione informale."),
    ("Quanto costa?", "Quanto custa?", "A1", "Per chiedere il prezzo."),
    ("Dov'è il bagno?", "Onde é o banheiro?", "A1", "Domanda essenziale."),
    ("Buon appetito!", "Bom apetite!", "A1", "Si dice prima di mangiare."),
    ("Salute!", "Saúde!", "A1", "Si dice quando si brinda o quando qualcuno starnutisce."),
    ("Che schifo!", "Que nojo!", "A2", "Espressione di disgusto."),
    ("Non mi interessa.", "Não me interessa.", "A2", "Per declinare un'offerta."),
    ("Sono d'accordo.", "Estou de acordo.", "A2", "Per esprimere consenso."),
    ("Hai ragione.", "Você tem razão.", "A2", "Per dare ragione a qualcuno."),
    ("Non lo so.", "Não sei.", "A1", "Per esprimere ignoranza su un fatto."),
    ("Ci penso io.", "Deixa comigo / Eu cuido disso.", "B1", "Per rassicurare qualcuno."),
    ("Magari!", "Quem dera!", "B1", "Espressione di desiderio."),
    ("Macché!", "Que nada!", "B1", "Per negare energicamente."),
    ("Boh!", "Sei lá!", "A2", "Espressione colloquiale di incertezza."),
    ("Dai!", "Vamos! / Para com isso!", "A1", "Esclamazione molto comune e versatile."),
    ("Meno male.", "Ainda bem.", "A2", "Espressione di sollievo."),
    ("Roba da matti.", "Coisa de louco.", "B1", "Per descrivere una situazione assurda."),
    ("Acqua in bocca.", "Bico calado.", "B2", "Per chiedere di mantenere un segreto."),
    ("Piove sul bagnato.", "Chove no molhado.", "B2", "Quando i problemi si accumulano."),
    ("Tirare il calzino.", "Bater as botas.", "C1", "Modo di dire per 'morire'."),
    ("Ogni morte di papa.", "De vez em nunca.", "B2", "Per indicare un evento rarissimo."),
    ("Fuori di testa.", "Fora da casinha / louco.", "B1", "Essere pazzo."),
    ("Avere le mani bucate.", "Ser mão aberta (gastador).", "B2", "Spendere troppi soldi."),
    ("Costare un occhio della testa.", "Custar os olhos da cara.", "B1", "Essere molto costoso."),
    ("Prendere due piccioni con una fava.", "Matar dois coelhos com uma cajadada só.", "B2", "Ottenere due risultati con una sola azione."),
    ("Non vedo l'ora.", "Mal vejo a hora.", "A2", "Essere impaziente per qualcosa di bello."),
    ("Fare finta di niente.", "Fingir que não é nada.", "B1", "Ignorare volontariamente qualcosa."),
    ("Tutto fumo e niente arrosto.", "Muito barulho por nada (Só fumaça, nada de carne).", "C1", "Molte apparenze, poca sostanza."),
    ("Trovarsi tra l'incudine e il martello.", "Estar entre a cruz e a espada.", "C1", "Essere in una situazione difficile senza via d'uscita."),
    ("Salvare capra e cavoli.", "Agradar a gregos e troianos.", "C1", "Trovare un compromesso che soddisfi tutti."),
    ("Sputare il rospo.", "Desembuchar (Cuspir o sapo).", "B2", "Dire finalmente la verità."),
    ("Arrampicarsi sugli specchi.", "Dar desculpas esfarrapate.", "C1", "Cercare scuse improbabili."),
    ("Avere il pollice verde.", "Ter dedo verde (saber cuidar de plantas).", "B1", "Essere bravi col giardinaggio."),
    ("Essere al verde.", "Estar liso (sem dinheiro).", "B1", "Non avere soldi."),
    ("Dormire sugli allori.", "Dormir sobre os louros.", "C1", "Accontentarsi dei successi passati.")
]

for i, (frase, trad, livello, contesto) in enumerate(frases, 1):
    imitazioni_list.append({
        "id": f"imi_{i:03d}",
        "frase_italiano": frase,
        "frase_portugues": trad,
        "nivel": livello,
        "contexto": contesto,
        "audio_ipa": "",
        "xp_recompensa": 15
    })

os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
with open(os.path.join(OUT, 'data', 'imitazioni.json'), 'w', encoding='utf-8') as f:
    json.dump({"imitazioni": imitazioni_list}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(imitazioni_list)} imitazioni in data/imitazioni.json")
