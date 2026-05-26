import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VI")

def migliorare_explicazione_lez6(testo_original, ex):
    """Melhoria automática para Lezione VI (Futuro semplice e composto)"""
    
    # Regra 1: Futuro semplice regolare
    if testo_original.lower().strip() in ["andrà", "sara", "avrà"]:
        return (f"{testo_original} Futuro Semplice regolare: terminazioni -ò, -ai, -à, "
                f"-emo, -ete, -anno. Esempio: mangiARÀ, leggiRÀ, scriviRÀ.")
    
    # Regra 2: Futuro irregolare base comune
    if testo_original.lower().strip() in ["sarò", "andrò", "avrà", "potrò", "dovrà"]:
        return (f"{testo_original} Futuro Irregolare — memorizzare radici alterate. "
                f"essere → sarò, avere → avrò, andare → andrò, potere → potrò.")
    
    # Regra 3: Futuro composto
    if testo_original.lower().strip() in ["avrò mangiato", "sarò andato"]:
        return (f"{testo_original} Futuro Composto: futuro di AVERESSERE + participio passato. "
                f"Ex: Avrò mangiato domani; Sarò arrivato allora.")
    
    # Regra 4: Futuro per probabilità presente
    if testo_original.lower().strip() in ["probabilmente", "forse"]:
        return (f"{testo_original} Uso del futuro per esprimere probabilità presente. "
                f"Il meteo: domani farà bel tempo; Probabilmente verrà.")
    
    # Regra 5: General gramatical para revelar curto  
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto Lezione VI. Explicação sobre futuro semplice/composto, "
                f"conjugación regular/irregular o uso para probabilità.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra de Futuro Semplice/Composto aplicada.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = migliorare_explicazione_lez6(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
