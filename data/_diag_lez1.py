import json
import re

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez_index = 0
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione I")

print(f"\n{'='*60}")
print(f"DIAGNÓSTICO: {lez['num']} — {lez.get('titulo', 'Sem título')}")
print(f"{'='*60}\n")

total_exercises = len(lez["exercicios"])
exercicio_indices = list(range(total_exercises))

# Classificar exercícios
revelar_list = [e for e in lez["exercicios"] if e.get("tipo") == "revelar"]
escolha_list = [e for e in lez["exercicios"] if e.get("tipo") == "escolha"]

print(f"Total Exercícios: {total_exercises}")
print(f"  - Tipo 'revelar': {len(revelar_list)}")
print(f"  - Tipo 'escolha': {len(escolha_list)}\n")

# Identificar exercícios sem explicação ou com explicações curtas (<30 chars)
explicacoes_fracas = []
exercicios_processados = []

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    # Exercício sem explicação
    if not explicacao_original:
        classificacao = "❌ SEM EXPLICAÇÃO"
    elif len(explicacao_original.strip()) < 30:
        classificacao = "⚠️ MUITO CURTA (<30 chars)"
    else:
        classificacao = "✅ OK"
    
    exercicio_indices.append({"tipo": ex.get("tipo"), "tema": explicacao_original[:40]})
    print(f"[{i}] {ex.get('tipo', 'N/D')}: {classificacao}")
    if not classificacao.startswith("✅"):
        print(f"    '{explicacao_original}'")

print("\n" + "="*60)
print(f"RESUMO: {total_exercises} exercícios processados")

# Estatísticas
sem_ex = sum(1 for e in lez["exercicios"] if not e.get("explicacao"))
curtes = sum(1 for e in lez["exercicios"] 
             if "explicacao" in e and len(e["explicacao"].strip()) < 30)
ok = sum(1 for e in lez["exercicios"] 
         if "explicacao" in e and len(e["explicacao"].strip()) >= 30)

print(f"Sem explicação: {sem_ex}")
print(f"Muito curtas (<30 chars): {curtes}")
print(f"OK (>=30 chars): {ok}\n")

if ok > 0:
    media_caracteres = sum(len(e.get("explicacao", "")) for e in lez["exercicios"] if "explicacao" in e) / ok
    print(f"Média de caracteres (OK): {media_caracteres:.1f}")

print(f"\n{'='*60}")
if sem_ex == 0 and curtes == 0:
    print("✅ LEIÇÃO OK — Todas as explicações >=30 chars")
else:
    print(f"⚠️ {sem_ex + curtes} exercíci(s) necessitam de melhoria\n")
