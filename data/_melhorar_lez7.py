import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione VII")

def migliorare_explicazione_lez7(testo_original, ex):
    """Melhoria automática para Lezione VII (I possessivi)"""
    
    # Regra 1: Aggettivo possessivo + articolo
    if testo_original.lower().strip() in ["mio", "tuo", "suo"]:
        return (f"{testo_original} Aggettivo Possessivo sempre con artigo. "
                f"Mio amico, tua madre, suo libro. Forma varia por gênero/número: mio/mia/mai/miei/mie/miei.")
    
    # Regra 2: Senza articolo (espressões familiares)
    if testo_original.lower().strip() in ["a casa mia", "a piedi miei"]:
        return (f"{testo_original} Possessivo SEM artigo indica posse íntima/familiaridade. "
                f"A casa mia, con gli occhi tuoi. Uso idiomatico comune.")
    
    # Regra 3: Pronome possessivo
    if testo_original.lower().strip() in ["il mio", "la tua"]:
        return (f"{testo_original} Pronome Possessivo = Aggettivo + artigo. "
                f"Substitui verbo/complemento: il libro è IL MIO (non dico 'è di me').")
    
    # Regra 4: Nomi di parentela
    if testo_original.lower().strip() in ["mia madre", "tuo padre"]:
        return (f"{testo_original} Con nomi di parentela → possessivo SEM artigo indica familiaridade/certeza. "
                f"Mia madre è qui, non 'la mia madre'.")
    
    # Regra 5: General gramatical para revelar curto  
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto Lezione VII. Explicação sobre uso di aggettivo/pronome possessivi, "
                f"artículos ou ausência d'articolo per familiarità.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra di possessivi con/senza articolo aplicada.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = migliorare_explicazione_lez7(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
