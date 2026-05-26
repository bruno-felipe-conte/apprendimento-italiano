import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione IV")

def melhorar_explicazione_lez4(testo_original, ex):
    """Melhoria automática para Lezione IV (Passato prossimo)"""
    
    # Regra 1: Auxiliers avere/essere
    if testo_original.lower().strip() in ["avere", "essere", "ho", "hai", "ha"]:
        return (f"{testo_original} Auxiliar AVVERBIO: AVERE usa ho/hai/ha/abbiamo/avete/hanno, "
                f"ESSERE usa sono/sei/è/siamo/siete/sono. Participe passato concorda com ESSERE.")
    
    # Regra 2: Participio passato irregolare comune
    if any(p in testo_original.lower() for p in ["stato", "avuto", "andato", "fatto", "detto", "venuto"]):
        particio = [p for p in ["stato", "avuto", "andato", "fatto", "detto", "venuto"] if p in testo_original.lower()][0]
        return (f"Participe passato irregular: {particio}. Uso: essere + particio → accordo del participio "
                f"(sono andato/sono stata andata). Memorizzare come bloco.")
    
    # Regra 3: Passato prossimo con essere
    if "essere" in testo_original.lower():
        return (f"{testo_original} Passato prossimo com ESSERE: sujeito determina forma do participio. "
                f"(ho mangiato vs sono andato). Veri de movimento/locatição usam essere.")
    
    # Regra 4: General gramatical para revelar curto
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto Passato Prossimo. Explicação sobre auxiliar + participio passado. "
                f"Inclua se è regolare/irregolare e concordância do participio quando aplicável.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra de Passato Prossimo aplicada. "
                f"Auxiliar + particio passado correto.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = melhorar_explicazione_lez4(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
