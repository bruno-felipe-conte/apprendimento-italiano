import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione IV")

print(f"\n{'='*60}")
print(f"DIAGNÓSTICO: {lez['num']} — {lez.get('titulo', 'Sem título')}")
print(f"{'='*60}\n")

total_exercises = len(lez["exercicios"])
print(f"Total Exercícios: {total_exercises}")

sem_ex = sum(1 for e in lez["exercicios"] if not e.get("explicacao"))
curtes = sum(1 for e in lez["exercicios"] 
             if "explicacao" in e and len(e["explicacao"].strip()) < 30)
ok = total_exercises - sem_ex - curtes

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
