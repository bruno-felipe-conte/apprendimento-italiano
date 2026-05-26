import json
import re

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione I")

novos = [
    # ARTICOLI (10 exercícios)
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Inserire l'articolo corretto:\n___ casa / ___ città / ___ amico", "resposta": "la casa / la città / l'amico", "explicacao": "LA (femminile) per casa/città. L' (vocale) per amico."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Inserire l'articolo:\n___ tavolo / ___ finestra / ___ giardino", "resposta": "il tavolo / la finestra / il giardino", "explicacao": "IL (maschile) per tavolo/giardino. LA (femminile) per finestra."},
    {"tipo": "escolha", "pergunta": "Quale articolo è corretto per 'libro'?", "opcoes": ["il libro", "lo libro", "la libro"], "resposta": 0, "explicacao": "Libro è maschile, usa il determinativo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Articolazione:\n___ ora / ___ acqua / ___ idea", "resposta": "l'ora / l'acqua / l'idea", "explicacao": "L' davanti a vocale per tutte e tre le parole."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta?", "opcoes": ["lo studente", "l'studiante", "la studente"], "resposta": 0, "explicacao": "LO si usa per sostantivi maschili che iniziano con s+consonante."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Plurale dei nomi in -o:\nii medico / la farmacia / il lago", "resposta": "i medici / le farmacie / i laghi", "explicacao": "-co diventa -ci (medico→medici). -a diventa -e (farmacia→farmacie). -o diventa -hi (lago→laghi)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Plurale dei nomi in -a:\nla poesia / la mano / la città", "resposta": "le poesie / le mani / le città", "explicacao": "-ia diventa -ie (poesia→poesie). -o diventa -i con accento chiuso (mano→mani). -tà mantiene il suono (città→città)."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'la radio' è:", "opcoes": ["le radios", "le radio", "gli radio"], "resposta": 1, "explicacao": "Radio è femminile e invariabile al plurale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Plurale dei nomi in -e:\nla neve / la penna / la mappa", "resposta": "le nevi / le penne / le mappe", "explicacao": "-e diventa -i (neve→nevi). Consonante finale cambia suono: penna→penne, mappa→mappe."},
    {"tipo": "escolha", "pergunta": "Quale plurale è corretto per 'l'amico'? A:", "opcoes": ["le amici", "gli amici", "i amici"], "resposta": 1, "explicacao": "Amico diventa amici e prende gli perché femminile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Articolazione con z:\n___ zaino / ___ zoo / ___ zero", "resposta": "lo zaino / lo zoo / lo zero", "explicacao": "LO si usa davanti a s+consonante, z, gn, ps, x, y."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Plurale di psicologo:\nil psicologo / il tecnologo / il geologo", "resposta": "i psicologi / i tecnologi / i geologi", "explicacao": "-ogo diventa -oghi quando persona, ma -ico semplice diventa -ici (psicologo→psicologi)."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'lo gnomo' è:", "opcoes": ["gli gnomi", "gli gnomos", "i gnomi"], "resposta": 0, "explicacao": "GN si mantiene con -i (gnomo→gnomi)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Articolazione prima di vocale:\n___ uomo / ___ ora / ___ euro", "resposta": "l'uomo / l'ora / l'euro", "explicacao": "L' davanti a tutte le vocali (o, u, e)."},
    {"tipo": "escolha", "pergunta": "Quale articolo è corretto per 'acqua'? A:", "opcoes": ["il acqua", "lo acqua", "l'acqua"], "resposta": 2, "explicacao": "Acqua inizia con vocale, usa L'."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Articolazione indefinita:\n___ gatto / ___ casa / ___ zuppa", "resposta": "un gatto / una casa / una zuppa", "explicacao": "UN (maschile), UNA (femminile) per singolari."}
]

# Aggiungi altri 20 esercizi rivolti alla pratica grammaticale base
novos.extend([
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Forma contratta:\nio sono / tu sei / lui è / noi siamo / voi siete / sono", "resposta": "Io sono / Tu sei / Lui è / Noi siamo / Voi siete / Essere", "explicacao": "L'essere si contrae: io→i', tu→t', lui/lei→è, noi→n', voi→v'. Io e tu non contraggono."},
    {"tipo": "escolha", "pergunta": "Quale verbo è corretto per 'noia'? A:", "opcoes": ["ho noia", "mi ha noia", "avevo la noia"], "resposta": 0, "explicacao": "Ho (o) con noia (espressione idiomatica)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Articolazione con numeri:\nii libro primo / la pagina prima / lo zero vigesimo", "resposta": "Il libro primo / La pagina prima / Lo zero vigesimo", "explicacao": "Articolo determinativo si mantiene anche davanti a numerali ordinales."},
    {"tipo": "escolha", "pergunta": "Come si scrive 'la musica' al plurale?", "opcoes": ["le musicas", "le musica", "le musiche"], "resposta": 2, "explicacao": "-a diventa -e quando la parola finisce con suono nasale."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Plurale di parole straniere:\nla computer / il cinema / la televisione", "resposta": "le computer / i cinema / le televisioni", "explicacao": "Parole inglesi spesso invariabili o -i/-e secondo genere."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'l'arancia' è:", "opcoes": ["le arance", "gli arance", "le arancie"], "resposta": 0, "explicacao": "-a diventa -e (arancia→arance)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Genere maschile/femminile:\nll tavolo (maschile) / la sedia (femminile) / lo scaffale (maschile)", "resposta": "Il tavolo è maschile / La sedia è femminile / Lo scaffale è maschile", "explicacao": "-o/-ale indicano maschile, -a indica femminile."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'lo studente':?", "opcoes": ["gli studenti", "le studenti", "i studenti"], "resposta": 2, "explicacao": "Studente diventa Studenti con articolo IL→I."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Articolazione corretta:\n___ biblioteca / ___ Università / ___ scuola", "resposta": "La biblioteca / La Università / La scuola", "explicacao": "Tutte e tre sono femminili, quindi LA."},
    {"tipo": "escolha", "pergunta": "Come si dice 'i libri' correttamente?", "opcoes": ["gli libri", "le libri", "i libri"], "resposta": 2, "explicacao": "Libri è maschile plurale, usa I (non gli che è per -a/-o femminile)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Plurale irregolare:\nll bambino / il ceto / la mano", "resposta": "i bambini / i ceti / le mani", "explicacao": "-ino diventa -ini (bambino→bambini). Ceti semplice. Mano→mani (-o→-i)."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'la rosa' è:", "opcoes": ["le rosas", "le rose", "gli rossi"], "resposta": 1, "explicacao": "-a diventa -e (rosa→rose)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Articolazione con consonante s:\n___ sport / ___ scienza / ___ scuola", "resposta": "Lo sport / La scienza / La scuola", "explicacao": "LO per maschile, LA per femminile. S+consonante usa lo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'lo psicologo':?", "opcoes": ["le psicologhe", "gli psicologi", "i psicologhi"], "resposta": 1, "explicacao": "Psicologo (maschile) → Psicologi. Non psicologhe."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Articolazione con vocale:\n___ italiano / ___ estate / ___ ospedale", "resposta": "L'italiano / L'estate / L'ospedale", "explicacao": "Tutte iniziano con vocale, quindi L'."},
    {"tipo": "escolha", "pergunta": "Come si dice 'la casa' in plurale?", "opcoes": ["le case", "gli case", "i case"], "resposta": 0, "explicacao": "Casa (femminile) → Case. Usa LE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Plurale di -ico:\nii fisico / la medico / lo psichiatra", "resposta": "i fisici / le mediche / i psichiatri", "explicacao": "-ico diventa -ici (fisico→fisici). Medico femminile → mediche."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'l'elettronica' è:", "opcoes": ["le elettroniche", "gli elettroniche", "le electronicos"], "resposta": 0, "explicacao": "Elettronica (femminile) → Elettroniche."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Articolazione corretta:\n___ problema / la soluzione / lo scenario", "resposta": "Il problema / La soluzione / Lo scenario", "explicacao": "Problema (maschile) = Il. Soluzione (femminile) = La. Scenario (maschile con s) = Lo."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'la carta'?", "opcoes": ["le carte", "i carte", "gli carte"], "resposta": 0, "explicacao": "Carta (femminile) → Carte. Usa LE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Plurale di -uma:\nla camera / la natura / la musica", "resposta": "le camere / le nature / le musiche", "explicacao": "-a diventa -e (camera→camere). Natura mantiene suono (-t-). Musica → Musiche."},
    {"tipo": "escolha", "pergunta": "Come si dice 'i cani' correttamente?", "opcoes": ["gli cani", "le cani", "i cani"], "resposta": 0, "explicacao": "Cani è maschile plurale, usa GLI (prima regola)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Articolazione con i:\n___ giardino / la piscina / lo stadio", "resposta": "Il giardino / La piscina / Lo stadio", "explicacao": "Tutte con articoli corrispondenti al genere."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'il sole' è:", "opcoes": ["li soli", "i soli", "le soli"], "resposta": 1, "explicacao": "Sole (maschile) → Soli. Usa I."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Plurale di -o finale:\nla foto / il voto / il polo", "resposta": "le foto / i voti / i poli", "explicacao": "Foto invariabile. Voto → Voti (-o→-i). Polo → Poli (-o→-i)."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'lo studio':?", "opcoes": ["gli studi", "le studi", "i studii"], "resposta": 0, "explicacao": "Studio (maschile) → Studi. Usa GLI."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Articolazione con consonante:\n___ ponte / la strada / il confine", "resposta": "Il ponte / La strada / Il confine", "explicacao": "Tutti maschili, quindi IL."},
    {"tipo": "escolha", "pergunta": "Come si dice 'i fiori' correttamente?", "opcoes": ["le fiori", "gli fiori", "i fiori"], "resposta": 2, "explicacao": "Fiori è maschile plurale, usa I (non gli per -i)."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Plurale di nomi composti:\nla mamma / il papà / lo zio", "resposta": "le mamme / i papà / gli zii", "explicacao": "Mamma→Mamme, Papà→Papà (invariabile), Zio→Zii."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'la banca' è:", "opcoes": ["le banche", "gli banche", "i banche"], "resposta": 0, "explicacao": "Banca (femminile) → Banche. Usa LE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Articolazione con i:\n___ ufficio / la stanza / lo schermo", "resposta": "L'ufficio / La stanza / Lo schermo", "explicacao": "Ufficio inizia con vocale → L'. Stanza e Schermo sono maschili/femminili."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'la festa':?", "opcoes": ["le feste", "i feste", "gli feste"], "resposta": 0, "explicacao": "Festa (femminile) → Feste. Usa LE."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Plurale di -io:\nla radio / il piano / lo studio", "resposta": "le radios / i piani / gli studi", "explicacao": "Radio invariabile. Piano → Piani (-o→-i). Studio (in alcuni casi) → Studi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'il tempo' al plurale?", "opcoes": ["i tempi", "le tempi", "gli tempi"], "resposta": 0, "explicacao": "Tempo (maschile) → Tempi. Usa I."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Articolazione con i:\n___ negozio / la piazza / lo schermo", "resposta": "Il negozio / La piazza / Lo schermo", "explicacao": "Negozio (maschile) = Il. Piazza (femminile) = La."},
    {"tipo": "escolha", "pergunta": "Il plurale di 'il medico' è:", "opcoes": ["i medici", "gli medici", "le mediche"], "resposta": 0, "explicacao": "Medico (maschile) → Medici. Usa I."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Plurale di -e finale:\nla legge / la pelle / la chiave", "resposta": "le leggi / le pelli / le chiavi", "explicacao": "-e diventa -i (legge→leggi). Pelle → Pelli (-e→-i). Chiave → Chiavi (-e→-i)."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'lo zucchero':?", "opcoes": ["gli zuccheri", "le zuccheri", "i zuccheri"], "resposta": 0, "explicacao": "Zucchero (maschile) → Zuccheri. Usa GLI."}
])

# Inserimento: trova il primo esercizio "escolha" esistente e inserisci prima di quello
exercicios = lez["exercicios"]
idx_insert = next((i for i, e in enumerate(exercicios) if e["tipo"] == "escolha"), len(exercicios))

for i, ex in enumerate(novos):
    exercicios.insert(idx_insert + i, ex)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
