import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione V")

def migliorare_explicazione_lez5(testo_original, ex):
    """Melhoria automática para Lezione V (La particella "ci" / Partitivo)"""
    
    # Regra 1: Ci come pronome di luogo
    if testo_original.lower().strip() in ["ci", "c'e", "ci sono"]:
        return (f"{testo_original} Particella CI: indica localizzazione/possessão. "
                f"Struttura: c'è singolare, ci sono plurale. Uso: ci vado a Roma, ci sono libri.")
    
    # Regra 2: Ci con verbi (volerci, metterci)
    if testo_original.lower().strip() in ["volerci", "metterci"]:
        return (f"{testo_original} Verbo + CI indica necessità/tempo. "
                f"Es: Ci vuole un minuto; Metti ci il libro → lo metti qui.")
    
    # Regra 3: Articoli partitivi base
    if testo_original.lower().strip() in ["del", "della", "dei", "degli"]:
        return (f"{testo_original} Articolio partitivo + preposição articolata indica indefinizione. "
                f"del = di + il, degli = di + gli, delle = di + le.")
    
    # Regra 4: General gramatical para revelar curto  
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto Lezione V. Explicação sobre uso da particella ci, "
                f"artículos partitivos ou partitivo indefinido.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra de particella ci ou artigos partitivos aplicada.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = migliorare_explicazione_lez5(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
