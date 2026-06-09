#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script per generare 27 storie di filosofia classica (C1-C2) divise in capitoli.
Filosofi: Platone, Aristotele, Seneca, Marco Aurelio, Descartes, Nietzsche, Epicuro, Socrate.
Livelli C1-C2 con vocabolario sofisticato e temi filosofici complessi.
"""

import json

# Template base per una storia
template = """
    {
      "id": "{id}",
      "titolo": "{titulo}",
      "titolo_pt": "{titulo_pt}",
      "nivel": "{nivel}",
      "icone": "{icone}",
      "autore": "{autore}",
      "tema": "{tema}",
      "descrizione": "{descrizione}",
      "descrizione_pt": "{descrizione_pt}",
      "xp_recompensa": {xp},
      "testo": [
"""

# Capitoli di Platone - La Repubblica
capitoli_platone = [
    (1, "Il Mitto della Grotta", "A Caverna", 65, 🕳️),
    (2, "La Via Fuori dalla Caverna", "La Scala", 55, 🧭),
    (3, "L'Amore per il Sapere", "Diosfelia", 50, 💡),
]

# Capitoli di Aristotele - Etica Nicomachea
capitoli_aristotele = [
    (1, "La Felicità come Fine Ultimo", "Eudaimonia", 60, 🎯),
    (2, "Le Virtù Pratiche", "Cardinali e Teziali", 55, ⚖️),
    (3, "Il Tempo Medio", "Dorosofia", 50, 📏),
]

# Lettere da Montecassino di Seneca
capitoli_seneca = [
    (1, "La Felicità Interiore", "Beatus Vitae", 60, 🌿),
    (2, "Vivere nel Presente", "Tempus Volat", 55, ⏳),
    (3, "Morte e Indifferenza", "Finis Rerum", 50, 💀),
]

# Massimae del Imperatore Marco Aurelio
capitoli_marcu_aur = [
    (1, "Il Debito verso gli Esseri Umani", "Gratitudo", 60, 👥),
    (2, "Nessuno ti Può Danneggiare", "Ad Nullum", 55, 🛡️),
    (3, "Il Tempo è Breve", "Tempus Breve", 50, ⏰),
]

# Meditazioni di Epitteto
capitoli_epitto = [
    (1, "Non Sono Io il Mio Corpo", "Sum Non Corpus", 60, 🗿),
    (2, "Il Volere è la Causa del Dolore", "Voluntas Doloris", 55, 🔑),
    (3, "Natura e Razionalità", "Phusis Logos", 50, 🌊),
]

# Discorsi di Descartes - Meditaciones Metaphysicae
capitoli_descartes = [
    (1, "I Doubt Everything", "Cogito Ergo Sum", 65, 🤔),
    (2, "God's Existence and Perfection", "Deus Ens Perfectum", 60, ⭐),
    (3, "Clear and Distinct Ideas", "Ideae Clarae Et Distinctae", 55, 🔍),
]

# Considerazioni di Nietzsche - Thus Spoke Zarathustra
capitoli_nietzsche = [
    (1, "The Overman", "Der Ubermensch", 60, 🦁),
    (2, "Eternal Recurrence", "Die Ewige Wiederkunft", 55, 🔁),
    (3, "Death of God", "Gott Ist Tot", 50, ⚰️),
]

# Discorsi di Epicuro - Lettere ai Figli
capitoli_epicuro = [
    (1, "Quarante Volte Felice", "Forty Times Happy", 60, 🏛️),
    (2, "Atomo e Tempo", "Aion Chronos", 55, ⚛️),
    (3, "Il Giardino degli Epicurei", "Kyonos Koinonia", 50, 🌺),
]

# Dialoghi di Socrate - Apologia
capitoli_soccrate = [
    (1, "Sapere che non so", "Aletheia Ignorance", 60, ❓),
    (2, "Il Maieutico", "Midwifery Method", 55, 👶),
    (3, "Morte e Immortalità dell'Anima", "Physis Psyche", 50, 🕊️),
]

# Testi base di filosofia C1-C2 (Livello avanzato)
filosofi_testi = [
    (1, "Platone", "Repubblica - Grotta della Metafora"),
    (2, "Aristotele", "Etica Nicomachea - Eudaimonia"),
    (3, "Seneca", "Lettere a Lucilio - Felicità Intima"),
    (4, "Marco Aurelio", "Meditazioni - Umanità e Virtù"),
    (5, "Epitteto", "Discorsi - Dominio di Sé"),
    (6, "Descartes", "Meditazioni Metaphysicae - Cogito"),
    (7, "Nietzsche", "Così Parlò Zarathustra - l'Ubermensch"),
    (8, "Epicuro", "Lettere ai Figli - Giardino"),
    (9, "Socrate", "Apologia di Socrate"),
]

# Generazione testi complessi per livello C1-C2
testi_capitoli = {
    1: "C'era una volta una caverna profonda dove uomini seduti come statue da secoli guardavano l'ombra che danzava sulle pareti. Luce di fuochi dall'ingresso li illuminava, ma loro credevano quelle ombre fossero la realtà stessa. Quando uno si alzò con sforzo e dolore, uscì dalla grotta verso il sole. La vista gli bruciò, poi piano piano vide le cose vere: non ombre, ma esseri viventi; non fuoco acceso, ma il calore del mattino; non statue, ma persone reali con pensieri veri."
    + "「Traduzione」：Era uma caverna profunda onde homens sentados como estátuas desde séculos olhavam sombras que dançavam nas paredes. Luce de fogos do entrada lhos iluminava, mas eles acreditavam aquelas sombras fossem a própria realidade."
    + "Vocabolario: caverna /ka.vɛrˈna/ (s.f.) grotta; ombra ˈom.bra/ (s.f.) sombra; realtà reˈal.tà/ (s.f.) realidade; fuoco ˈfukk/ (s.m.) fogo; sole soˈle/ (s.m.) sol",
    
    2: "Dalla caverna l'uscita fu ardua. La scala che conduce al mondo vero era lunga, ripida, faticosa. Si deve girare intorno con la vista alla luce esterna invece di guardar le ombre interne. L'occhio, abituato al buio della grotta, soffriva il lume del sole. Ma col tempo si accostumò. Vide che non ci fu mai un fuoco vero all'interno e che tutto era proiezione illusoria."
    + "「Tradução」：Da caverna saída foi árdua. Escada que conduzia ao mundo verdadeiro era longa, íngreme, penosa. Deve-se girar em volta com a vista à luz externa."
    + "Vocabolario: arduo ˈar.dwo/ (agg.) árduo; scala ˈska.la/ (s.f.) escada; lume ˈlu.me/ (s.m.) claridade; proiezione pro.je.ˈtjo.ne/ (s.f.) projeção",
    
    3: "Il cammino verso la caverna fuori fu lungo, ma la vista alla luce esterna si affacciò finalmente all'aria aperta. Non più ombre e specchi, ma cose vere e reali che toccano con mano e occhio. La conoscenza dell'oggetto non è più apparenza, ma essenza. Si chiama filosofia: amore del sapere vero."
    + "「Tradução」：O caminho rumo à caverna exterior foi longo, mas a vista à luz externa finalmente se deparou ao ar livre. Não mais sombras e espelhos, mas coisas verdadeiras e reais que tocam com mão e olho."
    + "Vocabolario: essenza esˈsæn.tsja/ (s.f.) essência; apparenza ap.paˈren.tsa/ (s.f.) aparência; essenza esˈsen.tsa/ (s.f.) substância",
}

# Funzione per generare una storia completa
def genera_storia(capitolo, autore, tema, xp):
    numero = capitolo["numero"]
    titolo = capitolo["titolo"]
    titolo_pt = capitolo["titolo_pt"]
    icone = capitolo["icone"]
    
    id_storia = f"stor_{numero:03d}_phi"
    
    # Testo italiano completo unendo tutti i capitoli (o usando il testo base se esiste)
    if numero in testi_capitoli and capitolo.get("testo", "") == "":
        testo_italiano = testi_capitoli[numero]["testo_it"]
        testo_portuguese = testi_capitoli[numero]["testo_pt"]
        vocabolario = json.loads(testi_capitoli[numero]["vocab"])
    else:
        testo_italiano = "C'era una volta un filosofo che camminava nel tempio del pensiero, cercando la verità nuda. «Non esiste risposta semplice», disse. «Il sapere è come una scala infinita», soggiunse. Ogni gradino rappresenta una virtù: saggezza, coraggio, giustizia e temperanza."
        testo_portuguese = "Era uma vez um filósofo que caminhava no templo do pensamento, buscando a verdade nua. «Não existe resposta simples», disse ele. «O saber é como uma escala infinita», continuou. Cada degrau representa uma virtude: sabedoria, coragem, justiça e temperança."
        vocabolario = [
            {"parola": "filosofo", "traduzione": "filósofo", "ipa": "/fi.loˈzo.f/ (s.m.)"},
            {"parola": "tempio", "traduzione": "templo", "ipa": "/ˈtem.pjo/ (s.m.)"},
            {"parola": "verità", "traduzione": "verdade", "ipa": "/ve.ˈrja.tà/ (s.f.)"},
        ]
    
    paragraphs = [
        {
            "id": f"{id_storia}_p1",
            "italiano": testo_italiano,
            "portuguese": testo_portuguese,
            "parole": vocabolario if vocabolario else [{"parola": "pensiero", "traduzione": "pensamento", "ipa": "/penˈsjɛ.ro/ (s.m.)"}],
        }
    ]
    
    return {
        "id": id_storia,
        "titolo": titolo,
        "titolo_pt": titolo_pt,
        "nivel": random.choice(["C1", "C2"]),
        "icone": icone,
        "autore": autore,
        "tema": tema,
        "descrizione": f"Capitolo {numero}: {titolo}",
        "descrizione_pt": f"Capítulo {numero}: {titulo_pt}",
        "xp_recompensa": xp,
        "testo": paragraphs,
    }

# Carica le storie esistenti
with open("data/storie.json", "r", encoding="utf-8") as f:
    dati_esistenti = json.load(f)

storie = dati_esistenti["storie"]

print(f"Storie esistenti: {len(storie)}")
ultimo_id = storie[-1]["id"] if storie else None
print(f"Ultimo ID: {ultimo_id}")

# Genera 27 nuove storie (fino ad arrivare a 45 totale)
nuovi_capitoli = []

# Plato - Repubbica (C1-C2, livello filosofico alto)
for numero, titolo_it, titolo_pt, xp, icone in capitoli_platone:
    nuovi_capitoli.append({
        "autore": "Platone",
        "tema": "metafisica/epistemologia",
        "titolo": titolo_it,
        "titolo_pt": titolo_pt,
        "icone": icone,
        "xp": xp,
    })

# Aristotele - Etica (C1-C2)
for numero, titolo_it, titolo_pt, xp, icone in capitoli_aristotele:
    nuovi_capitoli.append({
        "autore": "Aristotele",
        "tema": "etica/pratica",
        "titolo": titolo_it,
        "titolo_pt": titolo_pt,
        "icone": icone,
        "xp": xp,
    })

# Seneca - Lettere a Lucilio (C1-C2)
for numero, titolo_it, titolo_pt, xp, icone in capitoli_seneca:
    nuovi_capitoli.append({
        "autore": "Seneca",
        "tema": "stoicismo/virtù",
        "titolo": titolo_it,
        "titolo_pt": titolo_pt,
        "icone": icone,
        "xp": xp,
    })

# Marco Aurelio - Meditazioni (C1-C2)
for numero, titolo_it, titolo_pt, xp, icone in capitoli_marcu_aur:
    nuovi_capitoli.append({
        "autore": "Marco Aurelio",
        "tema": "stoicismo/imperiale",
        "titolo": titolo_it,
        "titolo_pt": titolo_pt,
        "icone": icone,
        "xp": xp,
    })

# Aggiungi fino a 27 totali
count = len(nuovi_capitoli)
while count < 27:
    # Alternare filosofi esistenti con nuovi testi basati su opere classiche
    filosofo_idx = count % len(filosofi_testi)
    _, autore, opera = filosofi_testi[filosofo_idx]
    
    numero = len(nuovi_capitoli) + 1
    titoli_universali = [
        ("La Scala del Sapere", "A Escada do Saber"),
        ("Il Tempo Fugace", "O Tempo Fugaz"),
        ("Virtù e Fortuna", "Virtude e Sorte"),
        ("L'Anima Immortale", "Alma Imortal"),
    ]
    
    titolo_it = titoli_universuali[count % len(titoli_universali)][0]
    titolo_pt = titoli_universuali[count % len(titoli_universali)][1]
    
    nuovi_capitoli.append({
        "autore": autore,
        "tema": opera.split(" - ")[0],
        "titolo": titolo_it,
        "titolo_pt": titolo_pt,
        "icone": random.choice(["📜", "🔱", "✨"]),
        "xp": 55 + (count % 15),
    })
    count += 1

# Aggiungi testi di Niccolò Machiavelli (Il Principe)
for i in range(3):
    nuovi_capitoli.append({
        "autore": "Machiavelli",
        "tema": "politica/etica",
        "titolo": ["La Volontà del Principe", "L'Artigine Politica"][i],
        "titolo_pt": ["A Vontade do Príncipe", "A Arte Política"][i],
        "icone": random.choice(["👑", "⚔️", "🏛️"]),
        "xp": 50,
    })

# Aggiungi testi di Leonardo Bruni (Umanesimo)
for i in range(2):
    nuovi_capitoli.append({
        "autore": "Bruni",
        "tema": "umanesimo/classico",
        "titolo": ["La Dignità dell'Uomo", "Il Ritorno agli Antichi"][i],
        "titolo_pt": ["A Dignidade do Homem", "O Retorno aos Antigos"][i],
        "icone": random.choice(["🎓", "📚", "🕰️"]),
        "xp": 52,
    })

# Ordina e aggiungi al JSON
storie += [genera_storia(c["numero"], c["autore"], f"{c['tema']} - {c['titolo']}", c["xp"]) for c in nuovi_capitoli]

# Salva con nuovo ID sequenziale
with open("data/storie.json", "w", encoding="utf-8") as f:
    json.dump({"storie": storie}, f, ensure_ascii=False, indent=4)

print(f"\n✅ Generazione completata!")
print(f"Totale storie: {len(storie)}")
print(f"Nuove storie aggiunte: {len(nuovi_capitoli)}")
