import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
    }

def append_to_existing(templo_num, new_words_data):
    path = os.path.join(OUT, "data", f"templo-{templo_num}.json")
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    
    current_count = len(obj["palavras"])
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(new_words_data, current_count + 1):
        tid = f"t{templo_num}_{i:03d}"
        obj["palavras"].append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))
        
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"APPENDED templo-{templo_num}.json -- now has {len(obj['palavras'])} parole")

t32_add = [
    ("plebeo", "plebeu", "romani", "Un soldato plebeo.", "Um soldado plebeu.", "/pleˈbɛo/", "m", "plebei"),
    ("patrizio", "patrício", "romani", "Una famiglia patrizia.", "Uma família patrícia.", "/paˈtrittsjo/", "m", "patrizi"),
    ("console", "cônsul", "romani", "Il console romano.", "O cônsul romano.", "/ˈkɔnsole/", "m", "consoli"),
    ("barbarie", "barbárie", "epoche", "Anni di barbarie.", "Anos de barbárie.", "/barˈbarje/", "f", "barbarie"),
    ("centurione", "centurião", "romani", "Il centurione al comando.", "O centurião no comando.", "/tʃentuˈrjone/", "m", "centurioni"),
    ("dominazione", "dominação", "epoche", "La dominazione straniera.", "A dominação estrangeira.", "/dominatˈtsjone/", "f", "dominazioni"),
    ("spedizione", "expedição", "medioevo", "La spedizione dei Mille.", "A expedição dos Mil.", "/speditˈtsjone/", "f", "spedizioni"),
    ("stemma", "brasão", "medioevo", "Lo stemma reale.", "O brasão real.", "/ˈstɛmma/", "m", "stemmi"),
    ("scudo", "escudo", "medioevo", "Uno scudo di ferro.", "Um escudo de ferro.", "/ˈskudo/", "m", "scudi"),
    ("lancia", "lança", "medioevo", "Lanciare la lancia.", "Lançar a lança.", "/ˈlantʃa/", "f", "lance"),
    ("cavalleria", "cavalaria", "medioevo", "L'assalto della cavalleria.", "O ataque da cavalaria.", "/kavalleˈria/", "f", "cavallerie"),
    ("fanteria", "infantaria", "medioevo", "La fanteria avanza.", "A infantaria avança.", "/fanteˈria/", "f", "fanterie"),
    ("alleanza", "aliança", "epoche", "Firmare un'alleanza.", "Assinar uma aliança.", "/alleˈantsa/", "f", "alleanze")
]

t33_add = [
    ("escursione", "excursão", "viaggio", "Fare un'escursione in montagna.", "Fazer uma excursão na montanha.", "/eskurˈsjone/", "f", "escursioni")
]

if __name__ == "__main__":
    append_to_existing(32, t32_add)
    append_to_existing(33, t33_add)
