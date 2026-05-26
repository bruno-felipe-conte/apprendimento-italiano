import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione XVIII")

novos = [
    # 30 exercícios sobre Gli avverbi
    {"tipo": "revelar", "pergunta": "**Esercizio 1** — Avverbo di modo:\nLui corre _____ (lentamente).", "resposta": "lento", "explicacao": "Avverbo: lentamente. Lui corre lentamente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 2** — Avverbo di modo:\nLei parla _____ (fortemente).", "resposta": "forte", "explicacao": "Avverbo: forte. Lei parla forte."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'slowly'? A:", "opcoes": ["lentamente", "lento", "lente"], "resposta": 0, "explicacao": "Lentamente = Avverbo. Lentamente = slowly."},
    {"tipo": "revelar", "pergunta": "**Esercizio 3** — Avverbo di luogo:\nLa casa è _____ (lontano).", "resposta": "lontano", "explicacao": "Avverbo: lontano. La casa è lontano."},
    {"tipo": "revelar", "pergunta": "**Esercizio 4** — Avverbo di luogo:\nIl libro è _____ (qui).", "resposta": "qui", "explicacao": "Avverbo: qui. Il libro è qui."},
    {"tipo": "escolha", "pergunta": "Come si dice 'quickly' in italiano? A:", "opcoes": ["velocemente", "veloce", "rapido"], "resposta": 0, "explicacao": "Velocemente = Avverbo. Velocemente = quickly."},
    {"tipo": "revelar", "pergunta": "**Esercizio 5** — Avverbo di modo:\nLui lavora _____ (bene).", "resposta": "bene", "explicacao": "Avverbo: bene. Lui lavora bene."},
    {"tipo": "revelar", "pergunta": "**Esercizio 6** — Avverbo di modo:\nLei canta _____ (male).", "resposta": "male", "explicacao": "Avverbo: male. Lei canta male."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'often'? A:", "opcoes": ["spesso", "spesso", "volta"], "resposta": 0, "explicacao": "Spesso = Avverbo di frequenza. Spesso = often."},
    {"tipo": "revelar", "pergunta": "**Esercizio 7** — Avverbo di tempo:\nVerrò _____ (domani).", "resposta": "domani", "explicacao": "Avverbo: domani. Verrò domani."},
    {"tipo": "revelar", "pergunta": "**Esercizio 8** — Avverbo di tempo:\nÈ _____ (oggi).", "resposta": "oggi", "explicacao": "Avverbo: oggi. È oggi."},
    {"tipo": "escolha", "pergunta": "Come si dice 'always' in italiano? A:", "opcoes": ["sempre", "spesso", "volta"], "resposta": 0, "explicacao": "Sempre = Avverbo di frequenza. Sempre = always."},
    {"tipo": "revelar", "pergunta": "**Esercizio 9** — Avverbo di tempo:\nHo studiato _____ (ieri).", "resposta": "ieri", "explicacao": "Avverbo: ieri. Ho studiato ieri."},
    {"tipo": "revelar", "pergunta": "**Esercizio 10** — Avverbo di modo:\nLui guarda _____ (con attenzione).", "resposta": "attentamente", "explicacao": "Avverbo: attentamente. Lui guarda attentamente."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'never'? A:", "opcoes": ["mai", "sempre", "spesso"], "resposta": 0, "explicacao": "Mai = Avverbo di negazione. Mai = never."},
    {"tipo": "revelar", "pergunta": "**Esercizio 11** — Avverbo di tempo:\nNon verrò _____ (mai).", "resposta": "mai", "explicacao": "Avverbo: mai. Non verrò mai."},
    {"tipo": "revelar", "pergunta": "**Esercizio 12** — Avverbo di modo:\nLei dorme _____ (profondamente).", "resposta": "profondamente", "explicacao": "Avverbo: profondamente. Lei dorme profondamente."},
    {"tipo": "escolha", "pergunta": "Come si dice 'yesterday' in italiano? A:", "opcoes": ["ieri", "oggi", "domani"], "resposta": 0, "explicacao": "Ieri = Avverbo di tempo. Ieri = yesterday."},
    {"tipo": "revelar", "pergunta": "**Esercizio 13** — Avverbo di luogo:\nVivo _____ (in Italia).", "resposta": "in Italia", "explicacao": "Avverbo: in Italia. Vivo in Italia."},
    {"tipo": "revelar", "pergunta": "**Esercizio 14** — Avverbo di modo:\nLo studio _____ (con piacere).", "resposta": "volentieri", "explicacao": "Avverbo: volentieri. Lo studio volentieri."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'carefully'? A:", "opcoes": ["attentamente", "lentamente", "velocemente"], "resposta": 0, "explicacao": "Attentamente = Avverbo. Attentamente = carefully."},
    {"tipo": "revelar", "pergunta": "**Esercizio 15** — Avverbo di modo:\nLei guarda _____ (curiosamente).", "resposta": "curiosamente", "explicacao": "Avverbo: curiosamente. Lei guarda curiosamente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 16** — Avverbo di tempo:\nSono arrivato _____ (stamani).", "resposta": "stamani", "explicacao": "Avverbo: stamani. Sono arrivato stamani."},
    {"tipo": "escolha", "pergunta": "Come si dice 'usually' in italiano? A:", "opcoes": ["di solito", "sempre", "spesso"], "resposta": 0, "explicacao": "Di solito = Avverbo di frequenza. Di solito = usually."},
    {"tipo": "revelar", "pergunta": "**Esercizio 17** — Avverbo di modo:\nLui cammina _____ (leggermente).", "resposta": "leggermente", "explicacao": "Avverbo: leggermente. Lui cammina leggermente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 18** — Avverbo di tempo:\nHo finito _____ (appena).", "resposta": "appena", "explicacao": "Avverbo: appena. Ho finito appena."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'loudly'? A:", "opcoes": ["fortemente", "lentamente", "gentilmente"], "resposta": 0, "explicacao": "Fortemente = Avverbo. Fortemente = loudly."},
    {"tipo": "revelar", "pergunta": "**Esercizio 19** — Avverbo di modo:\nParlo _____ (chiaramente).", "resposta": "chiaramente", "explicacao": "Avverbo: chiaramente. Parlo chiaramente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 20** — Avverbo di luogo:\nVado _____ (lontano).", "resposta": "lontano", "explicacao": "Avverbo: lontano. Vado lontano."},
    {"tipo": "escolha", "pergunta": "Come si dice 'recently' in italiano? A:", "opcoes": ["recentemente", "ieri", "oggi"], "resposta": 0, "explicacao": "Recentemente = Avverbo di tempo. Recentemente = recently."},
    {"tipo": "revelar", "pergunta": "**Esercizio 21** — Avverbo di modo:\nLei scrive _____ (attentamente).", "resposta": "attentamente", "explicacao": "Avverbo: attentamente. Lei scrive attentamente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 22** — Avverbo di tempo:\nSarò pronto _____ (domani).", "resposta": "domani", "explicacao": "Avverbo: domani. Sarò pronto domani."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'here'? A:", "opcoes": ["qui", "là", "dove"], "resposta": 0, "explicacao": "Qui = Avverbo di luogo. Qui = here."},
    {"tipo": "revelar", "pergunta": "**Esercizio 23** — Avverbo di modo:\nCamminiamo _____ (tranquillamente).", "resposta": "tranquillamente", "explicacao": "Avverbo: tranquillamente. Camminiamo tranquillamente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 24** — Avverbo di luogo:\nIl film è _____ (lì).", "resposta": "là", "explicacao": "Avverbo: là. Il film è là."},
    {"tipo": "escolha", "pergunta": "Come si dice 'early'? A:", "opcoes": ["primo", "presto", "tardi"], "resposta": 1, "explicacao": "Presto = Avverbo di modo. Presto = early."},
    {"tipo": "revelar", "pergunta": "**Esercizio 25** — Avverbo di modo:\nLei guarda _____ (sinceramente).", "resposta": "sinceramente", "explicacao": "Avverbo: sinceramente. Lei guarda sinceramente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 26** — Avverbo di tempo:\nHo chiamato _____ (poco fa).", "resposta": "poco", "explicacao": "Avverbo: poco. Ho chiamato poco fa."},
    {"tipo": "escolha", "pergunta": "Quale forma è corretta per 'often'? A:", "opcoes": ["spesso", "raramente", "mai"], "resposta": 0, "explicacao": "Spesso = Avverbo di frequenza. Spesso = often."},
    {"tipo": "revelar", "pergunta": "**Esercizio 27** — Avverbo di modo:\nLui legge _____ (con piacere).", "resposta": "volentieri", "explicacao": "Avverbo: volentieri. Lui legge volentieri."},
    {"tipo": "revelar", "pergunta": "**Esercizio 28** — Avverbo di luogo:\nIl negozio è _____ (vicino).", "resposta": "vicino", "explicacao": "Avverbo: vicino. Il negozio è vicino."},
    {"tipo": "escolha", "pergunta": "Come si dice 'well'? A:", "opcoes": ["bene", "benissimo", "male"], "resposta": 0, "explicacao": "Bene = Avverbo di modo. Bene = well."},
    {"tipo": "revelar", "pergunta": "**Esercizio 29** — Avverbo di modo:\nLei parla _____ (fluente).", "resposta": "fluente", "explicacao": "Avverbo: fluente. Lei parla fluentemente."},
    {"tipo": "revelar", "pergunta": "**Esercizio 30** — Avverbo di tempo:\nLo farò _____ (domenica).", "resposta": "domenica", "explicacao": "Avverbo: domenica. Lo farò domenica."}
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
