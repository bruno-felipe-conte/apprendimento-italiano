import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XI")

novos = [
    # 30 esercizi sobre Le preposizioni semplici
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Preposizione semplice:\n_____ casa (a casa)", "resposta": "A", "explicacao": "Preposizione semplice: a = a luogo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Preposizione semplice:\n_____ scuola (alla scuola)", "resposta": "Alla", "explicacao": "Preposizione articolata: a + la = alla."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'to Italy'? A:", "opcoes": ["ad", "in", "a"], "resposta": 1, "explicacao": "A = Preposizione semplice per direzioni."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Preposizione semplice:\n_____ tavolo (sul tavolo)", "resposta": "Sul", "explicacao": "Preposizione articolata: su + il = sul."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Preposizione semplice:\n_____ penna (con la penna)", "resposta": "Con", "explicacao": "Preposizione semplice: con = companhia."},
    {"tipo": "escolha", "pergunta": "Come si dice 'of' in italiano? A:", "opcoes": ["di", "da", "sotto"], "resposta": 0, "explicacao": "Di = Preposizione semplice per 'of'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Preposizione semplice:\n_____ amico (del mio amico)", "resposta": "Del", "explicacao": "Preposizione articolata: di + il = del."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Preposizione semplice:\n_____ macchina (sulla macchina)", "resposta": "Sulla", "explicacao": "Preposizione articolata: su + la = sulla."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'from'? A:", "opcoes": ["da", "fuiori", "fuori"], "resposta": 0, "explicacao": "Da = Preposizione semplice per 'from'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Preposizione semplice:\n_____ lavoro (al lavoro)", "resposta": "Al", "explicacao": "Preposizione articolata: a + il = al."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Preposizione semplice:\n_____ letto (sulla letto)", "resposta": "Sul", "explicacao": "Preposizione articolata: su + il = sul. Letto è maschile."},
    {"tipo": "escolha", "pergunta": "Come si dice 'by' in italiano? A:", "opcoes": ["con", "da", "a"], "resposta": 0, "explicacao": "Con = Preposizione semplice per 'with/by'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Preposizione semplice:\n_____ finestra (dalla finestra)", "resposta": "Dalla", "explicacao": "Preposizione articolata: da + la = dalla."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Preposizione semplice:\n_____ giardino (nel giardino)", "resposta": "Nel", "explicacao": "Preposizione articolata: in + il = nel."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'into'? A:", "opcoes": ["in", "dentro", "all'interno"], "resposta": 0, "explicacao": "In = Preposizione semplice per 'into'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Preposizione semplice:\n_____ mare (in mare)", "resposta": "In", "explicacao": "Preposizione semplice: in = location marittima."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Preposizione semplice:\n_____ negozio (al negozio)", "resposta": "Al", "explicacao": "Preposizione articolata: a + il = al. Negozio è maschile."},
    {"tipo": "escolha", "pergunta": "Come si dice 'for' in italiano? A:", "opcoes": ["per", "verso", "a"], "resposta": 0, "explicacao": "Per = Preposizione semplice per 'for'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Preposizione semplice:\n_____ strada (in strada)", "resposta": "In", "explicacao": "Preposizione semplice: in = on the street."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Preposizione semplice:\n_____ treno (sul treno)", "resposta": "Sul", "explicacao": "Preposizione articolata: su + il = sul. Treno è maschile."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'over'? A:", "opcoes": ["sopra", "oltre", "in"], "resposta": 0, "explicacao": "Sopra = Preposizione semplice per 'over'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Preposizione semplice:\n_____ tetto (sul tetto)", "resposta": "Sul", "explicacao": "Preposizione articolata: su + il = sul. Tetto è maschile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Preposizione semplice:\n_____ porta (dalla porta)", "resposta": "Dalla", "explicacao": "Preposizione articolata: da + la = dalla. Porta è femminile."},
    {"tipo": "escolha", "pergunta": "Come si dice 'between' in italiano? A:", "opcoes": ["tra", "fra", "in"], "resposta": 0, "explicacao": "Tra/Fra = Preposizioni semplici per 'between'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Preposizione semplice:\n_____ ponte (sul ponte)", "resposta": "Sul", "explicacao": "Preposizione articolata: su + il = sul. Ponte è maschile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Preposizione semplice:\n_____ fiume (nel fiume)", "resposta": "Nel", "explicacao": "Preposizione articolata: in + il = nel. Fiume è maschile."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'under'? A:", "opcoes": ["sotto", "dentro", "fuori"], "resposta": 0, "explicacao": "Sotto = Preposizione semplice per 'under'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Preposizione semplice:\n_____ divano (sul divano)", "resposta": "Sul", "explicacao": "Preposizione articolata: su + il = sul. Divano è maschile."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Preposizione semplice:\n_____ tavolo (sotto il tavolo)", "resposta": "Sotto", "explicacao": "Preposizione semplice: sotto = under."},
    {"tipo": "escolha", "pergunta": "Come si dice 'about' in italiano? A:", "opcoes": ["circa", "intorno", "presso"], "resposta": 0, "explicacao": "Circa = Preposizione semplice per 'about'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Preposizione semplice:\n_____ finestra (dietro la finestra)", "resposta": "Dietro", "explicacao": "Preposizione semplice: dietro = behind."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Preposizione semplice:\n_____ muro (di fronte al muro)", "resposta": "Di fronte a", "explicacao": "Preposizione composta: di fronte + a."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'through'? A:", "opcoes": ["attraverso", "dentro", "fuori"], "resposta": 0, "explicacao": "Attraverso = Preposizione composta per 'through'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Preposizione semplice:\n_____ strada (lungo la strada)", "resposta": "Lungo", "explicacao": "Preposizione semplice: lungo = along."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Preposizione semplice:\n_____ via (in via)", "resposta": "In", "explicacao": "Preposizione semplice: in = into la strada."},
    {"tipo": "escolha", "pergunta": "Come si dice 'during' in italiano? A:", "opcoes": ["durante", "nel", "allo"], "resposta": 0, "explicacao": "Durante = Preposizione semplice per 'during'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Preposizione semplice:\n_____ cena (a cena)", "resposta": "A", "explicacao": "Preposizione semplice: a = per eventi."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Preposizione semplice:\n_____ pranzo (alpranzo)", "resposta": "Al", "explicacao": "Preposizione articolata: a + il = al. Pranzo è maschile."},
    {"tipo": "escolha", "pergunta": "Quale preposizione è corretta per 'with'? A:", "opcoes": ["con", "da", "senza"], "resposta": 0, "explicacao": "Con = Preposizione semplice per 'with'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Preposizione semplice:\n_____ mano (in mano)", "resposta": "In", "explicacao": "Preposizione semplice: in = inside."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Preposizione semplice:\n_____ borsa (nella borsa)", "resposta": "Nella", "explicacao": "Preposizione articolata: in + la = nella."},
    {"tipo": "escolha", "pergunta": "Come si dice 'without' in italiano? A:", "opcoes": ["senza", "fuori", "senza di"], "resposta": 0, "explicacao": "Senza = Preposizione semplice per 'without'.",},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Preposizione semplice:\n_____ aria (nell'aria)", "resposta": "Nell", "explicacao": "Preposizione articolata: in + la = nella. Aria ha articolo partitivo."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Preposizione semplice:\n_____ mare (nel mare)", "resposta": "Nel", "explicacao": "Preposizione articolata: in + il = nel. Mare è maschile."}
]

exercicios = lez["exercicios"]
idx_insert = next((i for i, e in enumerate(exercicios) if e["tipo"] == "escolha"), len(exercicios))

for i, ex in enumerate(novos):
    exercicios.insert(idx_insert + i, ex)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
