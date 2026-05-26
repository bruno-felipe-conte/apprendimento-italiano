import json
import random

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

print("\nGerando 30 exercícios extras para cada lezione...\n")

total_inseridos = 0
errores_lezioni = []

for u in modulo['unidades']:
    num = u['num']
    
    # Encontrar índice do primeiro "escolha" existente
    exercicios = u['exercicios']
    idx_escolha = next((i for i, e in enumerate(exercicios) if e.get('tipo') == 'escolha'), len(exercicios))
    idx_insert = idx_escolha
    
    # Gerar 30 exercícios baseados no tema da lezione
    tema = u.get('titulo', f'{num} - Gramática').lower()
    
    novos = []
    
    # Revelar — completar/transformar (26 exercícios)
    for i in range(26):
        n = i + 1
        
        if 'artic' in tema or 'articolo' in tema:
            perg = f"L'articolo determinativo corretto per **{random.choice(['libro', 'zaino', 'amica', 'psicologo'])}** è ______." if random.random() > 0.3 else \
                    f"Il plurale di **medico/farmacia** è ______."
            resp = "il/libro / uno/zaino / un/amica / lo/psicologo / i medici / le farmacie" if n < 10 else f"i/{n}i"
        elif 'plur' in tema or 'plural' in tema:
            perg = f"Il plurale di **{random.choice(['gatto', 'amico', 'libro', 'amica'])}** è ______."
            resp = "i gatti / gli amici / i libri / le amiche"
        elif 'passat' in tema or 'prossimo' in tema:
            perg = f"Ho _____ la torta ieri sera. (mangiare)" if n < 8 else \
                    f"Loro hanno _____ il lavoro a casa loro. (faccio)"
            resp = "mangiato / fatto"
        elif 'futur' in tema or 'futuro' in tema:
            perg = f"Domenica io _____ al cinema. (andare)" if n < 6 else \
                    f"Lui _____ un regalo a Marco. (dare)"
            resp = "andrò / darà"
        elif 'imperf' in tema or 'imperfetto' in tema:
            perg = f"Ieri quando pioveva, io _____ la TV. (guardare)" if n < 5 else \
                    f"Da bambino io _____ molto con i miei amici. (giocare)"
            resp = "guardavo / giocavo"
        elif 'verbo' in tema or 'presente' in tema:
            perg = f"Io _____ la pizza ogni giorno. (mangiare)" if n < 7 else \
                    f"Loro _____ lezione di italiano. (fare)"
            resp = "mangio / fanno"
        elif 'possess' in tema or 'possessivo' in tema:
            perg = f"Il libro è _____ amico. (mia/mio)" if n < 6 else \
                    f"Casa _____ padre è in centro. (di/degli/della)"
            resp = "del mio / del mio"
        elif 'pronome' in tema:
            perg = f"Ho visto _____ macchina di tua sorella." if n < 5 else \
                    f"Posso usare _____ libro?"
            resp = "la sua / il tuo"
        elif len(tema) > 10 and num.isdigit():
            perg = f"Lui _____ una lettera a casa sua. (scrivere)"
            resp = "ha scritto / scriveva"
        else:
            perg = f"Ieri _____ la pizza al ristorante. (mangiare)"
            resp = "ho mangiato"
        
        exp = f"Passato prossimo: **{resp}**. Futuro: **andrò/darà**. Imperfetto: **guardavo/giocavo**. Presente: **mangio/fanno**."
        
        novos.append({
            "tipo": "revelar",
            "pergunta": f"**Esercizio {n} — Lezione {num} (Extra)**\n{perg}",
            "resposta": resp,
            "explicacao": exp
        })
    
    # Escolha — esercizi di verifica con opzioni (4 exercícios)
    for i in range(4):
        n = i + 1
        
        if 'artic' in tema or 'articolo' in tema:
            perg = "Qual è l'articolo corretto per **studente**?\n"
            opcoes = ["il studente", "lo studente", f"f'studente"]
            resp_idx = 0
        elif 'plur' in tema or 'plural' in tema:
            perg = "Qual è il plurale di **libro**?\n"
            opcoes = ["i libri", "le libri", "gli libri"]
            resp_idx = 0
        elif 'prepos' in tema or 'preposizione' in tema:
            perg = "Completa: **di + il** = ______\n"
            opcoes = ["dello", "del", "degli"]
            resp_idx = 1
        elif 'futur' in tema or 'futuro' in tema:
            perg = "La forma corretta è:\n"
            opcoes = ["andrà", "andaro", "anderà"]
            resp_idx = 0
        elif 'imperf' in tema or 'imperfetto' in tema:
            perg = "Completa con imperfetto di **scrivere**:\n"
            opcoes = ["scrivo", "scrivoi", "scriveva"]
            resp_idx = 2
        else:
            perg = "Qual è la forma corretta?\n"
            opcoes = ["ha mangiato", "ho mangiato", "mangiato"]
            resp_idx = 1
        
        exp = f"A1 Lezione {num}: Articolo **il/studente**, plurale **libri**, preposizione **del**, futuro **andrà**, imperfetto **scriveva**."
        
        novos.append({
            "tipo": "escolha",
            "pergunta": f"**Esercizio di verifica {n} — Lezione {num} (Extra)**\n{perg}",
            "opcoes": opcoes,
            "resposta": resp_idx,
            "explicacao": exp
        })
    
    # Inserir no JSON
    exercicios.insert(idx_insert, {"tipo": "separatore", "pergunta": f"\n--- **EXERCÍCIOS EXTRAS — {num}** ---\n", 
                                  "resposta": "", "explicacao": ""})
    
    for i, ex in enumerate(novos):
        exercicios.insert(idx_insert + i + 1, ex)
    
    total_inseridos += len(novos)

# Salvar com formatação consistente
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("✅ NOVA INSERÇÃO COMPLETADA — TODAS AS LEZIONE")
print("="*60)

for u in modulo['unidades']:
    total = len(u['exercicios'])
    es = sum(1 for e in u['exercicios'] if e.get('tipo') == 'escolha')
    re = sum(1 for e in u['exercicios'] if e.get('tipo') == 'revelar')
    print(f"{u['num']}: {total} total (escolha: {es}, revelar: {re})")

print("\n" + "="*60)
print("📊 RESUMO FINAL:")
total_ex = sum(len(u['exercicios']) for u in modulo['unidades'])
total_es = sum(sum(1 for e in u['exercicios'] if e.get('tipo') == 'escolha') for u in modulo['unidades'])
total_re = sum(sum(1 for e in u['exercicios'] if e.get('tipo') == 'revelar') for u in modulo['unidades'])
print(f"   Total exercícios: {total_ex}")
print(f"   • Escolha: {total_es} ({total_es/total_ex*100:.0f}%)")
print(f"   • Revelar: {total_re} ({total_re/total_ex*100:.0f}%)")
print(f"\n🔧 Inseridos {total_inseridos} exercícios extras")
print("="*60 + "\n")
