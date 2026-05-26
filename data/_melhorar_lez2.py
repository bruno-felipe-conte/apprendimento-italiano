import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione II")

def melhorar_explicazione_lez2(testo_original, ex):
    """Melhoria automática para Lezione II (Verbi -ARE/-ERE/-IRE / Avere / Essere)"""
    
    # Regra 1: Presente irregolare comune
    if "irregolare" in testo_original.lower():
        return (f"{testo_original} Verbo irregolare — memorizzare come bloco único. "
                f"Tabelar forma presente: io [forma], tu..., noi..., voi...")
    
    # Regra 2: Avere vs essere
    if "avere" in testo_original.lower() or "essere" in testo_original.lower():
        return (f"{testo_original} Differenza: AVERE per stato fisico/emozionale (ho fame), "
                f"ESSERE per identità (sono stanco). Espressioni idiomatiche con essere.")
    
    # Regra 3: Verbi regolari -ARE/-ERE/-IRE
    if "-are" in testo_original.lower() or "-ere" in testo_original.lower() or "-ire" in testo_original.lower():
        return (f"{testo_original} Verbo regolare. Presente indicativo: terminazioni "
                f"-o, -i, -a, -iamo, -ate, -ano (-ire com y: studio, studi).")
    
    # Regra 4: General gramatical para explicaciones muy cortas
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto gramatical Lezione II. Explicação pedagógica sobre conjugação verbo presente ou irregularidade.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra de conjugação presente aplicada. "
                f"As outras opções têm erro na terminação ou pessoa.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    # Só melhorar se <50 chars (já tem base mínima)
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = melhorar_explicazione_lez2(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
