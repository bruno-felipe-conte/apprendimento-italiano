import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

contesti_list = []

contextos = [
    ("La Mafia", "O Padrinho (Il Padrino)", "Filme", "A1", "Cena de máfia clássica.", ["famiglia", "onore", "rispetto", "tradimento", "offerta"]),
    ("La Dolce Vita", "La Dolce Vita", "Filme", "A2", "Paparazzi em Roma.", ["fontana", "notte", "scandalo", "bacio", "fotografo"]),
    ("Il Gladiatore", "O Gladiador", "Filme", "B1", "Luta no Coliseu.", ["arena", "spada", "imperatore", "sangue", "libertà"]),
    ("Gomorra", "Gomorra", "Série", "C1", "Crime organizado em Nápoles.", ["camorra", "droga", "quartiere", "soldi", "clan"]),
    ("La Casa de Papel", "La Casa di Carta", "Série", "B1", "Assalto ao banco.", ["rapina", "ostaggio", "maschera", "piano", "polizia"]),
    ("Stranger Things", "Stranger Things", "Série", "A2", "Monstros nos anos 80.", ["mostro", "bicicletta", "sottosopra", "dimensione", "amici"]),
    ("Harry Potter", "Harry Potter", "Filme", "A1", "Magia em Hogwarts.", ["magia", "bacchetta", "incantesimo", "strega", "cicatrice"]),
    ("Il Trono di Spade", "Game of Thrones", "Série", "B2", "Inverno está chegando.", ["inverno", "trono", "drago", "re", "battaglia"]),
    ("Breaking Bad", "Breaking Bad", "Série", "C1", "Química e crime.", ["chimica", "laboratorio", "cancro", "denaro", "pericolo"]),
    ("Amici Miei", "Meus Caros Amigos", "Filme", "B2", "Pegadinhas na Toscana.", ["scherzo", "zingarata", "amicizia", "risata", "treno"]),
    ("Nuovo Cinema Paradiso", "Cinema Paradiso", "Filme", "B1", "Magia do cinema na Sicília.", ["pellicola", "bacio", "proiezionista", "piazza", "ricordo"]),
    ("Il Postino", "O Carteiro e o Poeta", "Filme", "B1", "Poesia e amor.", ["poesia", "lettera", "isola", "metafora", "amore"]),
    ("La Vita è Bella", "A Vida é Bela", "Filme", "A2", "Esperança no campo.", ["gioco", "carro armato", "principessa", "premio", "sorriso"]),
    ("L'Amica Geniale", "My Brilliant Friend", "Série", "B2", "Crescendo em Nápoles.", ["scuola", "quartiere", "scarpe", "invidia", "matrimonio"]),
    ("Suburra", "Suburra", "Série", "B2", "Corrupção em Roma.", ["politica", "chiesa", "mafia", "potere", "segreto"]),
    ("Mare Fuori", "Mare Fuori", "Série", "B1", "Jovens na prisão.", ["carcere", "mare", "libertà", "speranza", "rabbia"]),
    ("Tre Uomini e una Gamba", "Aldo, Giovanni e Giacomo", "Filme", "B1", "Viagem cômica.", ["gamba", "viaggio", "ospedale", "matrimonio", "scherzo"]),
    ("La Grande Bellezza", "A Grande Beleza", "Filme", "C1", "Festa mundana.", ["festa", "mondanità", "bellezza", "scrittore", "vuoto"]),
    ("Che Bella Giornata", "Checco Zalone", "Filme", "A2", "Comédia no terrorismo.", ["duomo", "sicurezza", "innamorato", "terrone", "raccomandazione"]),
    ("Guerre Stellari", "Star Wars", "Filme", "B1", "Que a força esteja com você.", ["forza", "jedi", "spazio", "spada laser", "lato oscuro"]),
    ("Il Signore degli Anelli", "O Senhor dos Anéis", "Filme", "B2", "Jornada do anel.", ["anello", "elfo", "nano", "vulcano", "compagnia"]),
    ("Matrix", "Matrix", "Filme", "B2", "A pílula vermelha.", ["pillola", "realtà", "illusione", "macchina", "eletto"]),
    ("Jurassic Park", "Jurassic Park", "Filme", "A2", "Dinossauros fogem.", ["dinosauro", "recinto", "ambra", "zanzara", "isola"]),
    ("Titanic", "Titanic", "Filme", "A2", "Naufrágio.", ["nave", "ghiaccio", "affondare", "cuore", "collana"]),
    ("Ritorno al Futuro", "De Volta Para o Futuro", "Filme", "B1", "Viagem no tempo.", ["tempo", "macchina", "futuro", "passato", "fulmine"]),
    ("Avengers", "Vingatori", "Filme", "A2", "Heróis unidos.", ["scudo", "martello", "armatura", "alieno", "squadra"]),
    ("Spider-Man", "Homem-Aranha", "Filme", "A1", "Grandes poderes.", ["ragno", "ragnatela", "potere", "responsabilità", "maschera"]),
    ("Batman", "Batman", "Filme", "B1", "Cavaleiro das Trevas.", ["pipistrello", "oscurità", "cavaliere", "giustizia", "paura"]),
    ("Il Re Leone", "O Rei Leão", "Animação", "A1", "Ciclo da vida.", ["leone", "cerchio", "re", "zio", "savana"]),
    ("Alla Ricerca di Nemo", "Procurando Nemo", "Animação", "A1", "Oceano.", ["pesce", "oceano", "corrente", "memoria", "figlio"]),
    ("Toy Story", "Toy Story", "Animação", "A1", "Brinquedos vivos.", ["giocattolo", "sceriffo", "spaziale", "infinito", "oltre"]),
    ("Shrek", "Shrek", "Animação", "A2", "Ogro no pântano.", ["orco", "palude", "asino", "principessa", "drago"]),
    ("I Simpson", "Os Simpsons", "Série", "A1", "Família amarela.", ["ciambella", "centrale", "bar", "scuola", "divano"]),
    ("Friends", "Friends", "Série", "A2", "Amigos no café.", ["caffetteria", "divorzio", "dinosauro", "coinquilino", "pausa"]),
    ("The Office", "The Office", "Série", "B1", "Rotina no escritório.", ["ufficio", "carta", "capo", "scherzo", "telecamera"]),
    ("Lost", "Lost", "Série", "B2", "Ilha misteriosa.", ["volo", "sopravvissuti", "fumo", "isola", "mistero"]),
    ("Sherlock", "Sherlock", "Série", "C1", "Detetive brilhante.", ["indagine", "deduzione", "assassino", "pipa", "violino"]),
    ("Doctor Who", "Doctor Who", "Série", "B2", "Viagem no tempo.", ["dottore", "cabina", "alieno", "universo", "tempo"]),
    ("Black Mirror", "Black Mirror", "Série", "C1", "Distopia tecnológica.", ["schermo", "tecnologia", "futuro", "angoscia", "social"]),
    ("Squid Game", "Squid Game", "Série", "B1", "Jogos mortais.", ["gioco", "debiti", "sopravvivenza", "premio", "guardia"]),
    ("Narcos", "Narcos", "Série", "B2", "Cartel.", ["cartello", "polizia", "droga", "plata", "plomo"]),
    ("Peaky Blinders", "Peaky Blinders", "Série", "B2", "Gangue de Birmingham.", ["lametta", "scommessa", "fratelli", "fumo", "whisky"]),
    ("The Crown", "The Crown", "Série", "C1", "Realeza britânica.", ["regina", "corona", "governo", "scandalo", "palazzo"]),
    ("Bridgerton", "Bridgerton", "Série", "B1", "Fofoca na corte.", ["ballo", "duca", "gossip", "matrimonio", "diamante"]),
    ("Lupin", "Lupin", "Série", "B1", "Ladrão cavalheiro.", ["ladro", "collana", "vendetta", "trucco", "prigione"]),
    ("La Casa nella Prateria", "Little House", "Série", "A2", "Vida no campo.", ["prateria", "carro", "pionieri", "famiglia", "raccolto"]),
    ("X-Files", "X-Files", "Série", "B2", "Verdade está lá fora.", ["alieno", "complotto", "agente", "verità", "paranormale"]),
    ("Twin Peaks", "Twin Peaks", "Série", "C1", "Quem matou Laura?", ["caffè", "torta", "omicidio", "sogno", "mistero"]),
    ("I Soprano", "Os Sopranos", "Série", "B2", "Máfia em NJ.", ["terapia", "famiglia", "rifiuti", "panico", "affari"]),
    ("Mad Men", "Mad Men", "Série", "C1", "Publicidade nos anos 60.", ["pubblicità", "sigaretta", "campagna", "segretaria", "ambizione"])
]

for i, (titulo, origin, tipo, livello, desc, vocab) in enumerate(contextos, 1):
    contesti_list.append({
        "id": f"ctx_{i:03d}",
        "titulo": titulo,
        "origem": origin,
        "tipo": tipo,
        "nivel": livello,
        "descricao": desc,
        "vocabulario": [
            {"italiano": v, "portugues": f"Trad de {v}", "exemplo": f"Esempio con {v}."} 
            for v in vocab
        ],
        "xp_recompensa": 20
    })

os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
with open(os.path.join(OUT, 'data', 'contesti.json'), 'w', encoding='utf-8') as f:
    json.dump({"contesti": contesti_list}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(contesti_list)} contesti in data/contesti.json")
