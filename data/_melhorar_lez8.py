import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VIII")

def migliorare_explicazione_lez8(testo_original, ex):
    """Melhoria automática para Lezione VIII (I pronomi diretti)"""
    
    # Regra 1: Pronomi diretti atoni base
    if testo_original.lower().strip() in ["mi", "ti", "lo", "la", "ci", "vi", "li", "le"]:
        return (f"{testo_original} Pronome Diretto Atono: sostitui nome. Posição prima verbo no presente. "
                f"Mi/hi/lo/la/ci/vi/li/le. Ne per quantità: ho mangiato NE = ne ho mangiato.")
    
    # Regra 2: Passato prossimo + pronome (accordo)  
    if testo_original.lower().strip() in ["ho visto", "hai letto"]:
        return (f"{testo_original} Passato Prossimo con pronome diretto: pronome ANTECEDERE auxiliar. "
                f"Lo vedo → Lo ho visto (non 'vedo lo'). Verbi essere riflessivi: mi sono lavato.")
    
    # Regra 3: NE per quantità
    if testo_original.lower().strip() == "ne":
        return (f"{testo_original} Pronome NE = sostituzione di 'di + qualcosa/di alcuni'. "
                f"Ho mangiato mele → Ne ho mangiato.")
    
    # Regra 4: Con verbi servili (posicionamento)
    if testo_original.lower().strip() in ["lo posso", "potrei farlo"]:
        return (f"{testo_original} Verbo servo + pronome: posizione variabile. "
                f"Lo posso fare (pronome antes) o Posso farlo (infinito con pronome).")
    
    # Regra 5: General gramatical para revelar curto  
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto Lezione VIII. Explicação sobre uso di pronomi diretti, "
                f"posizione nel passato prossimo o pronome NE per quantità.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra di pronomi diretti atoni o posizione servili applicata.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = migliorare_explicazione_lez8(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
