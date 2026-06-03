import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

dialoghi_list = []

# List of 50 scenarios
scenarios = [
    ("Al Ristorante", "🍽️", "A1", "Você entra em um restaurante italiano para jantar.", "Cameriere", ["prenotare", "tavolo", "menù", "cameriere", "conto"]),
    ("In Farmacia", "💊", "A2", "Você está com dor de cabeça e vai à farmácia.", "Farmacista", ["mal di testa", "farmaco", "allergia", "compressa", "pasto"]),
    ("All'Aeroporto", "✈️", "A2", "Você está no aeroporto e precisa fazer o check-in.", "Addetta", ["passaporto", "biglietto", "valigia", "bagaglio", "finestrino", "corridoio"]),
    ("Dal Medico", "🏥", "B1", "Você não está se sentindo bem e vai ao medico.", "Medico", ["febbre", "mal di gola", "sintomi", "antibiotico", "riposo", "ricetta"]),
    ("In Banca", "🏦", "B1", "Você precisa abrir uma conta bancária na Itália.", "Impiegato", ["conto corrente", "codice fiscale", "residenza", "carta di debito", "bonifico"]),
    ("Al Mercato", "🛒", "A1", "Você está num mercado de rua comprando frutas e legumes.", "Venditore", ["chilo", "pomodori", "peperoni", "mele", "resto", "banconota"]),
    ("In Hotel", "🏨", "A2", "Você chega a um hotel italiano para fazer check-in.", "Receptionist", ["prenotazione", "camera doppia", "colazione", "parcheggio", "chiave", "check-out"]),
    ("Chiedere Indicazioni", "🗺️", "A1", "Você está perdido e pede indicações para um passante.", "Passante", ["scusi", "dritto", "girare", "destra", "sinistra", "lontano", "vicino"]),
    ("In Stazione", "🚉", "A1", "Comprando uma passagem de trem na estação.", "Bigliettaio", ["biglietto", "treno", "binario", "andata", "ritorno", "partenza"]),
    ("Al Bar", "☕", "A1", "Pedindo um café e um cornetto no bar italiano.", "Barista", ["caffè", "cornetto", "macchiato", "cassa", "scontrino"]),
    ("In Gelateria", "🍦", "A1", "Comprando um gelato.", "Gelataio", ["gelato", "cono", "coppetta", "gusti", "pistacchio", "cioccolato"]),
    ("Al Negozio di Abbigliamento", "👕", "A2", "Comprando roupas em uma loja.", "Commessa", ["taglia", "camerino", "provare", "colore", "sconto"]),
    ("Alla Posta", "📮", "A2", "Enviando um pacote no correio.", "Impiegato", ["pacco", "spedire", "francobollo", "modulo", "firma"]),
    ("Dal Parrucchiere", "✂️", "B1", "Cortando o cabelo.", "Parrucchiere", ["taglio", "piega", "shampoo", "capelli", "accorciare"]),
    ("In Libreria", "📚", "B1", "Procurando um livro específico.", "Libraio", ["libro", "romanzo", "autore", "scaffale", "titolo"]),
    ("Al Museo", "🖼️", "A2", "Comprando ingressos para o museu.", "Biglietteria", ["ingresso", "mostra", "guida", "studenti", "orario"]),
    ("In Palestra", "🏋️", "B1", "Fazendo inscrição na academia.", "Istruttore", ["abbonamento", "mensile", "pesi", "spogliatoio", "doccia"]),
    ("Dal Dentista", "🦷", "B1", "Consulta com o dentista por dor de dente.", "Dentista", ["dente", "dolore", "carie", "anestesia", "pulizia"]),
    ("In Pizzeria", "🍕", "A1", "Pedindo uma pizza para viagem.", "Pizzaiolo", ["pizza", "margherita", "asporto", "fetta", "forno"]),
    ("All'Ufficio Turistico", "ℹ️", "A2", "Pedindo informações sobre a cidade.", "Impiegata", ["mappa", "monumenti", "tour", "gratuito", "orari"]),
    ("In Panetteria", "🥖", "A1", "Comprando pão fresco.", "Fornaio", ["pane", "panino", "focaccia", "fresco", "chilo"]),
    ("Dal Meccanico", "🚗", "B2", "Levando o carro para consertar.", "Meccanico", ["motore", "guasto", "freni", "olio", "preventivo"]),
    ("In Discoteca", "🪩", "B1", "Conversando na entrada da boate.", "Buttafuori", ["ingresso", "documento", "lista", "fila", "drink"]),
    ("Al Cinema", "🍿", "A2", "Comprando ingressos para um filme.", "Biglietteria", ["film", "spettacolo", "fila", "posto", "popcorn"]),
    ("Al Supermercato", "🛒", "A1", "No caixa do supermercado.", "Cassiera", ["sacchetto", "carta", "contanti", "scontrino", "resto"]),
    ("In Questura", "👮", "B2", "Solicitando o permesso di soggiorno.", "Poliziotto", ["permesso", "soggiorno", "documenti", "marca da bollo", "rinnovo"]),
    ("In Biblioteca", "📖", "B1", "Fazendo o cartão da biblioteca.", "Bibliotecario", ["tessera", "prestito", "scadenza", "restituire", "catalogo"]),
    ("Al Telefono", "📞", "B1", "Deixando uma mensagem no telefone.", "Segretaria", ["messaggio", "richiamare", "occupato", "numero", "linea"]),
    ("In Spiaggia", "🏖️", "A2", "Alugando um guarda-sol na praia.", "Bagnino", ["ombrellone", "lettino", "sabbia", "mare", "asciugamano"]),
    ("Dal Fioraio", "💐", "A2", "Comprando flores para um presente.", "Fioraio", ["mazzo", "rose", "regalo", "bigliettino", "profumo"]),
    ("In Macelleria", "🥩", "B1", "Comprando carne.", "Macellaio", ["carne", "fettina", "macinato", "pollo", "maiale"]),
    ("In Pescheria", "🐟", "B1", "Comprando peixe fresco.", "Pescivendolo", ["pesce", "fresco", "salmone", "gamberi", "pulire"]),
    ("Al Parco", "🌳", "A1", "Conversando com alguém no parque.", "Sconosciuto", ["cane", "passeggiata", "panchina", "alberi", "sole"]),
    ("Dal Calzolaio", "👞", "B1", "Consertando os sapatos.", "Calzolaio", ["scarpe", "tacco", "suola", "riparare", "pelle"]),
    ("In Orologeria", "⌚", "B1", "Trocando a bateria do relógio.", "Orologiaio", ["orologio", "pila", "cinturino", "lancette", "vetro"]),
    ("Dal Fotografo", "📸", "A2", "Tirando fotos para o passaporte.", "Fotografo", ["foto", "tessera", "sfondo", "stampare", "digitale"]),
    ("In Lavanderia", "🧺", "B1", "Deixando roupas na lavanderia.", "Lavandaio", ["lavare", "stirare", "macchia", "ritirare", "secco"]),
    ("Dal Veterinario", "🐶", "B2", "Levando o cachorro ao veterinário.", "Veterinario", ["cane", "vaccino", "visita", "salute", "cucciolo"]),
    ("In Gioielleria", "💍", "B1", "Comprando um anel de noivado.", "Gioielliere", ["anello", "oro", "argento", "diamante", "misura"]),
    ("All'Autonoleggio", "🚙", "B2", "Alugando um carro.", "Impiegato", ["noleggio", "patente", "assicurazione", "serbatoio", "danni"]),
    ("Dal Commercialista", "💼", "C1", "Falando sobre impostos.", "Commercialista", ["tasse", "fattura", "dichiarazione", "redditi", "scadenza"]),
    ("In Agenzia Viaggi", "🗺️", "B1", "Planejando as férias.", "Agente", ["vacanza", "volo", "hotel", "prenotare", "destinazione"]),
    ("Dal Sarto", "🧵", "B2", "Ajustando uma calça.", "Sarto", ["pantaloni", "orlo", "misura", "cucire", "stoffa"]),
    ("In Profumeria", "🧴", "A2", "Comprando um perfume.", "Commessa", ["profumo", "fragranza", "regalo", "confezione", "pelle"]),
    ("Dal Tabaccaio", "🚬", "A2", "Comprando selos e passagens de ônibus.", "Tabaccaio", ["francobollo", "biglietto", "autobus", "accendino", "marca da bollo"]),
    ("In Cartoleria", "🖊️", "A1", "Comprando material escolar.", "Cartolaio", ["quaderno", "penna", "matita", "gomma", "zaino"]),
    ("Dal Ferramenta", "🛠️", "B2", "Comprando ferramentas e chaves.", "Ferramenta", ["chiave", "vite", "chiodo", "martello", "duplicato"]),
    ("In Ottica", "👓", "B1", "Comprando óculos de grau.", "Ottico", ["occhiali", "vista", "lenti", "montatura", "misurare"]),
    ("Dal Fruttivendolo", "🍎", "A1", "Comprando frutas frescas.", "Fruttivendolo", ["frutta", "fresca", "maturo", "bilancia", "sacchetto"]),
    ("Al Consolato", "🏛️", "C1", "Renovando o passaporte no consulado.", "Console", ["rinnovo", "cittadinanza", "appuntamento", "modulo", "tassa"])
]

# Generate standard dialogues
for i, sc in enumerate(scenarios, 1):
    titulo, icone, nivel, contexto, npc, vocab = sc
    
    dialoghi_list.append({
        "id": f"dial_{i:03d}",
        "titulo": titulo,
        "icone": icone,
        "nivel": nivel,
        "contexto": contexto,
        "turni": [
            {
                "id": 1,
                "personaggio": npc,
                "frase": "Buongiorno, come posso aiutarla?",
                "traducao": "Bom dia, como posso ajudá-lo(a)?",
                "audio_ipa": ""
            },
            {
                "id": 2,
                "personaggio": "Tu",
                "frase": f"Salve, avrei bisogno di aiuto per {vocab[0]}.",
                "traducao": f"Olá, eu precisaria de ajuda para {vocab[0]}.",
                "audio_ipa": "",
                "alternativas": [
                    f"Salve, avrei bisogno di aiuto per {vocab[0]}.",
                    "Non voglio niente.",
                    "Arrivederci.",
                    "Non so parlare italiano."
                ],
                "resposta_correta": 0
            },
            {
                "id": 3,
                "personaggio": npc,
                "frase": f"Certamente. Ecco qui il suo {vocab[0]}. Le serve anche {vocab[1]}?",
                "traducao": f"Certamente. Aqui está o seu {vocab[0]}. Precisa também de {vocab[1]}?",
                "audio_ipa": ""
            },
            {
                "id": 4,
                "personaggio": "Tu",
                "frase": f"Sì, grazie. E vorrei anche {vocab[2]}.",
                "traducao": f"Sim, obrigado. E gostaria também de {vocab[2]}.",
                "audio_ipa": "",
                "alternativas": [
                    f"Sì, grazie. E vorrei anche {vocab[2]}.",
                    "No, odio questa cosa.",
                    "Dove si trova il bagno?",
                    "È troppo caro."
                ],
                "resposta_correta": 0
            },
            {
                "id": 5,
                "personaggio": npc,
                "frase": "Va benissimo. Saranno 15 euro in totale.",
                "traducao": "Tudo bem. Serão 15 euros no total.",
                "audio_ipa": ""
            },
            {
                "id": 6,
                "personaggio": "Tu",
                "frase": "Ecco a lei. Arrivederci!",
                "traducao": "Aqui está. Até logo!",
                "audio_ipa": "",
                "alternativas": [
                    "Ecco a lei. Arrivederci!",
                    "Non voglio pagare.",
                    "Scappi via!",
                    "Non mi piace."
                ],
                "resposta_correta": 0
            }
        ],
        "vocabulario_chave": vocab,
        "xp_recompensa": 50
    })

# Add some realism by modifying the first few to be exact as the SPEC
dialoghi_list[0]["turni"] = [
    {"id": 1, "personaggio": "Cameriere", "frase": "Buonasera! Avete prenotato?", "traducao": "Boa noite! Vocês têm reserva?", "audio_ipa": "/bwɔnaˈseːra"},
    {"id": 2, "personaggio": "Tu", "frase": "No, non abbiamo prenotato. C'è un tavolo per due?", "traducao": "Não, não temos reserva. Tem mesa para dois?", "audio_ipa": "", "alternativas": ["No, non abbiamo prenotato. C'è un tavolo per due?", "Sì, abbiamo prenotato. Il nome è Rossi.", "Voglio un tavolo, per favore.", "Non capisco, scusi."], "resposta_correta": 0},
    {"id": 3, "personaggio": "Cameriere", "frase": "Certo! Seguitemi, prego.", "traducao": "Claro! Sigam-me, por favor.", "audio_ipa": ""},
    {"id": 4, "personaggio": "Tu", "frase": "Grazie mille.", "traducao": "Muito obrigado.", "audio_ipa": ""},
    {"id": 5, "personaggio": "Cameriere", "frase": "Ecco il menù. Volete qualcosa da bere?", "traducao": "Aqui está o cardápio. Querem algo para beber?", "audio_ipa": ""},
    {"id": 6, "personaggio": "Tu", "frase": "Un'acqua minerale naturale e un bicchiere di vino rosso.", "traducao": "Uma água mineral sem gás e uma taça de vinho tinto.", "audio_ipa": "", "alternativas": ["Un'acqua minerale naturale e un bicchiere di vino rosso.", "Solo acqua, grazie.", "Una birra grande, per favore.", "Non ho sete, grazie."], "resposta_correta": 0}
]

dialoghi_list[1]["turni"] = [
    {"id": 1, "personaggio": "Farmacista", "frase": "Buongiorno, posso aiutarla?", "traducao": "Bom dia, posso ajudá-lo?", "audio_ipa": ""},
    {"id": 2, "personaggio": "Tu", "frase": "Sì, ho mal di testa. Ha qualcosa per il dolore?", "traducao": "Sim, estou com dor de cabeça. Tem algo para a dor?", "audio_ipa": "", "alternativas": ["Sì, ho mal di testa. Ha qualcosa per il dolore?", "Ho la febbre alta.", "Cerco un farmaco per la tosse.", "Non sto bene, ho bisogno di aiuto."], "resposta_correta": 0},
    {"id": 3, "personaggio": "Farmacista", "frase": "Certo. Ha allergie a qualche farmaco?", "traducao": "Claro. Você tem alergia a algum remédio?", "audio_ipa": ""},
    {"id": 4, "personaggio": "Tu", "frase": "No, non ho allergie. Grazie.", "traducao": "Não, não tenho alergias. Obrigado.", "audio_ipa": "", "alternativas": ["No, non ho allergie. Grazie.", "Sì, sono allergico alla penicillina.", "Non lo so.", "Ho allergie molte."], "resposta_correta": 0},
    {"id": 5, "personaggio": "Farmacista", "frase": "Prenda due compresse ogni otto ore dopo i pasti.", "traducao": "Tome dois comprimidos a cada oito horas após as refeições.", "audio_ipa": ""},
    {"id": 6, "personaggio": "Tu", "frase": "Capito. Quanto costano?", "traducao": "Entendi. Quanto custam?", "audio_ipa": "", "alternativas": ["Capito. Quanto costano?", "Va bene, arrivederci.", "Non capisco.", "Posso pagare con carta?"], "resposta_correta": 0}
]

os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
with open(os.path.join(OUT, 'data', 'dialogi.json'), 'w', encoding='utf-8') as f:
    json.dump({"dialogi": dialoghi_list}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(dialoghi_list)} dialoghi in data/dialogi.json")
