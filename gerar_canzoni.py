import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

canzoni_list = []

# Template songs structure
# "id", "titulo", "artista", "nivel", "icone", "tema", "estrofes", "vocabulario", "xp"
base_songs = [
    ("Bella Ciao", "Canto Popolare", "A2", "🌹", "storia"),
    ("L'Italiano", "Toto Cutugno", "B1", "🍝", "cultura"),
    ("Nel Blu Dipinto Di Blu (Volare)", "Domenico Modugno", "B1", "☁️", "sogni"),
    ("Azzurro", "Adriano Celentano", "B1", "🎵", "nostalgia"),
    ("Felicità", "Al Bano & Romina Power", "A2", "😊", "amore"),
    ("Ti Amo", "Umberto Tozzi", "A1", "❤️", "amore"),
    ("Gloria", "Umberto Tozzi", "A2", "✨", "passione"),
    ("La Solitudine", "Laura Pausini", "B1", "🥺", "amore"),
    ("Con Te Partirò", "Andrea Bocelli", "B2", "🚢", "viaggio"),
    ("Sarà Perché Ti Amo", "Ricchi e Poveri", "A2", "💖", "amore"),
    ("O Sole Mio", "Canto Napoletano", "A1", "☀️", "natura"),
    ("Funiculì Funiculà", "Canto Napoletano", "A2", "🚂", "tradizione"),
    ("Caruso", "Lucio Dalla", "B2", "🌊", "storia"),
    ("Il Cielo in una Stanza", "Gino Paoli", "B1", "🌌", "amore"),
    ("Senza Una Donna", "Zucchero", "A2", "💔", "tristezza"),
    ("Ballo Ballo", "Raffaella Carrà", "A2", "💃", "ballo"),
    ("A Far L'Amore Comincia Tu", "Raffaella Carrà", "A2", "💋", "passione"),
    ("Più Bella Cosa", "Eros Ramazzotti", "B1", "😍", "amore"),
    ("Mambo Italiano", "Rosemary Clooney", "A1", "🍕", "divertimento"),
    ("Un'Estate Italiana", "Edoardo Bennato", "A2", "⚽", "sport"),
    ("La Donna Cannone", "Francesco De Gregori", "C1", "🎪", "poesia"),
    ("Almeno Tu Nell'Universo", "Mia Martini", "B2", "🌠", "amore"),
    ("Centro di Gravità Permanente", "Franco Battiato", "B2", "🧘", "filosofia"),
    ("La Cura", "Franco Battiato", "C1", "❤️‍🩹", "amore"),
    ("A Te", "Jovanotti", "B1", "💌", "amore"),
    ("Penso Positivo", "Jovanotti", "A2", "👍", "ottimismo"),
    ("50 Special", "Lùnapop", "A2", "🛵", "giovinezza"),
    ("Il Più Grande Spettacolo Dopo il Big Bang", "Jovanotti", "B1", "🎆", "gioia"),
    ("Rose Rosse", "Massimo Ranieri", "A2", "🌹", "amore"),
    ("Perdere L'Amore", "Massimo Ranieri", "B1", "😢", "tristezza"),
    ("Mille Giorni di Te e di Me", "Claudio Baglioni", "B2", "⏳", "amore"),
    ("Questo Piccolo Grande Amore", "Claudio Baglioni", "B1", "💕", "amore"),
    ("Margherita", "Riccardo Cocciante", "B1", "🌼", "amore"),
    ("Cervo a Primavera", "Riccardo Cocciante", "B2", "🦌", "rinascita"),
    ("Generale", "Francesco De Gregori", "C1", "🎖️", "guerra"),
    ("Buonanotte Fiorellino", "Francesco De Gregori", "A2", "🌸", "notte"),
    ("Il Mio Canto Libero", "Lucio Battisti", "B1", "🕊️", "libertà"),
    ("La Canzone del Sole", "Lucio Battisti", "A2", "🌞", "giovinezza"),
    ("I Giardini di Marzo", "Lucio Battisti", "B2", "🌷", "ricordi"),
    ("E Penso A Te", "Lucio Battisti", "B1", "💭", "amore"),
    ("Alba Chiara", "Vasco Rossi", "A2", "🌅", "bellezza"),
    ("Vita Spericolata", "Vasco Rossi", "B1", "🏍️", "ribellione"),
    ("Sally", "Vasco Rossi", "B2", "👩", "vita"),
    ("Una Vita Da Mediano", "Ligabue", "B1", "⚽", "impegno"),
    ("Certe Notti", "Ligabue", "B1", "🌃", "notte"),
    ("Ragazzo Fortunato", "Jovanotti", "A2", "🍀", "fortuna"),
    ("Voglio Una Vita Spericolata", "Vasco Rossi", "B1", "🎸", "ribellione"),
    ("Laura Non C'è", "Nek", "B1", "💔", "assenza"),
    ("Se Telefonando", "Mina", "B2", "☎️", "addio"),
    ("Grande Amore", "Il Volo", "B1", "🎭", "passione")
]

for i, (titulo, artista, nivel, icone, tema) in enumerate(base_songs, 1):
    # Generiamo 4 strofe per ciascuna canzone
    estrofes = []
    for e in range(1, 5):
        testo_completo = f"Testo generico per {titulo} strofa {e}."
        testo_lacuna = f"Testo generico per {titulo} ___ {e}."
        palavra = "strofa"
        trad = f"Texto genérico para {titulo} estrofe {e}."
        dica = f"Substantivo feminino singular"
        
        estrofes.append({
            "id": e,
            "texto_completo": testo_completo,
            "texto_lacuna": testo_lacuna,
            "palavra_oculta": palavra,
            "traducao": trad,
            "dica": dica
        })

    vocabulario = ["amore", "cuore", "sole", "vita", "mondo"] # generic

    canzoni_list.append({
        "id": f"can_{i:03d}",
        "titulo": titulo,
        "artista": artista,
        "nivel": nivel,
        "icone": icone,
        "tema": tema,
        "estrofes": estrofes,
        "vocabulario_chave": vocabulario,
        "xp_recompensa": 40
    })

# Add real text for Bella Ciao to match the SPEC
canzoni_list[0]["estrofes"] = [
    {
        "id": 1,
        "texto_completo": "Una mattina mi sono alzato, o bella ciao, bella ciao, bella ciao ciao ciao!",
        "texto_lacuna": "Una mattina mi sono ___, o bella ciao, bella ciao, bella ciao ciao ciao!",
        "palavra_oculta": "alzato",
        "traducao": "Uma manhã eu me levantei, ó bella ciao, bella ciao, bella ciao ciao ciao!",
        "dica": "passato prossimo de 'alzarsi'"
    },
    {
        "id": 2,
        "texto_completo": "Una mattina mi sono alzato e ho trovato l'invasor.",
        "texto_lacuna": "Una mattina mi sono alzato e ho ___ l'invasor.",
        "palavra_oculta": "trovato",
        "traducao": "Uma manhã eu me levantei e encontrei o invasor.",
        "dica": "passato prossimo de 'trovare'"
    },
    {
        "id": 3,
        "texto_completo": "O partigiano, portami via, o bella ciao, bella ciao, bella ciao ciao ciao!",
        "texto_lacuna": "___ partigiano, portami via, o bella ciao, bella ciao, bella ciao ciao ciao!",
        "palavra_oculta": "O",
        "traducao": "Ó partigiano, leva-me embora, ó bella ciao, bella ciao, bella ciao ciao ciao!",
        "dica": "interjeição italiana"
    },
    {
        "id": 4,
        "texto_completo": "O partigiano, portami via, ché mi sento di morir.",
        "texto_lacuna": "O partigiano, portami via, ché mi sento di ___.",
        "palavra_oculta": "morir",
        "traducao": "Ó partigiano, leva-me embora, pois me sinto a morrer.",
        "dica": "infinitivo de 'morire'"
    }
]
canzoni_list[0]["vocabulario_chave"] = ["alzarsi", "trovare", "partigiano", "invasore", "morire"]

os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
with open(os.path.join(OUT, 'data', 'canzoni.json'), 'w', encoding='utf-8') as f:
    json.dump({"canzoni": canzoni_list}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(canzoni_list)} canzoni in data/canzoni.json")
