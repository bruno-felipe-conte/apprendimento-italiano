import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione IX")

def migliorare_explicazione_lez9(testo_original, ex):
    """Melhoria automática para Lezione IX (L'imperfetto indicativo)"""
    
    # Regra 1: Imperfetto regolare -ARE
    if testo_original.lower().strip() in ["mangiavo", "dormivo"]:
        return (f"{testo_original} Imperfetto regulare di verbo -ARE. Sufixos: -avo, -evi, -iva, -avamo, -avate, -avano. "
                f"Uso: descrições/descriptions no passado, abituazioni/abituades.")
    
    # Regra 2: Imperfetto regolare -ERE/-IRE  
    if testo_original.lower().strip() in ["vedeva", "scriveva"]:
        return (f"{testo_original} Imperfetto regulare di verbo -ERE/-IRE. Sufixos: -evo, -evi, -eva, -evamo, -evate, -evano."
                f"Uso: descrições/descriptions no passado, azioni in progresso.")
    
    # Regra 3: Imperfetto irregolare comune
    if testo_original.lower().strip() in ["ero", "eri", "era"]:
        return (f"{testo_original} Imperfetto IRREGULARE di ESSERE. Memorizzare como bloco: ero/eri/era/eravamo/eravate/erano. "
                f"Invariável para gênero/número. Uso: estado físico/emotivo no passado.")
    
    if testo_original.lower().strip() in ["aveva", "avevi"]:
        return (f"{testo_original} Imperfetto IRREGULARE di AVERE. Memorizzare como bloco: aveva/avevi/aveva/avevamo/avevate/avevano. "
                f"Invariável para gênero/número.")
    
    # Regra 4: Passato prossimo vs imperfetto (comparação)
    if testo_original.lower().strip() in ["mangiavo quando", "leggevo mentre"]:
        return (f"{testo_original} DIFFERENZA TEMPI: Imperfetto = descriptioni/abituazioni/contesto passato. "
                f"Passato prossimo = azioni completate. Mentre + imperfetto = azione interrotta da evento.")
    
    # Regra 5: General gramatical para revelar curto  
    if len(testo_original.strip()) < 40 and ex.get("tipo") == "revelar":
        return (f"{testo_original} Contexto Lezione IX. Explicação sobre imperfetto regulare/irregolare, "
                f"uso per descriptioni/abituazioni ou distinção com passato prossimo.")
    
    elif ex.get("tipo") == "escolha":
        opcoes = ex.get("opcoes", [])
        resposta_idx = ex.get("resposta", 0)
        op_correta = opcoes[resposta_idx] if resposta_idx < len(opcoes) else ""
        
        return (f"RESPOSTA: {op_correta}. Regra di imperfetto applicata. "
                f"Uso per descriptioni/abituazioni o verbo irregolare.")
    
    # Se já tem >=50 chars, presumivelmente está bom
    if len(testo_original.strip()) >= 50:
        return testo_original
    
    return None

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    explicacao_original = ex.get("explicacao", "")
    
    if not explicacao_original or len(explicacao_original.strip()) < 50:
        testo_migliorato = migliorare_explicazione_lez9(explicacao_original, ex)
        
        if testo_migliorato and len(testo_migliorato.strip()) >= 30:
            ex["explicacao"] = testo_migliorato
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n{'='*60}")
print(f"OK: {lez['num']} — {migliorati}/{total_exercises} melhorados")
print('='*60 + "\n")
