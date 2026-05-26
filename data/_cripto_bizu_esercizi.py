# -*- coding: utf-8 -*-
"""
Italian Learning App A2/B1/B2 — Generazione Esercizi con "Bizu" Essenziali
Genera esercizi densi e autentici per i nuovi moduli denso (A2/B1/B2).
"""

import json
from pathlib import Path
import random

DATA_PATH = Path(r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json")

BIZU_A2 = [
    ("Tu sei Marco?", "Você é Marco?"),
    ("Che bella cazzata!", "Que coisa linda! (colloquialismo)"),
    ("Non ci sto, devo andarmene.", "Não quero ficar, preciso ir embora."),
]

BIZU_B1 = [
    ("Si chiude la trattativa domani mattina.", "O acordo será fechado amanhã de manhã. (business)"),
    ("Conosco una persona interessantissima, passiamo a cena!", "Conheço uma pessoa muito interessante, vamos jantar! (networking)"),
]

BIZU_B2 = [
    ("Il bilancio mostra una perdita del 15% nel terzo trimestre.", "O balanço mostra uma perda de 15% no terceiro trimestre. (business)"),
    ("Il CEO ha deciso di tagliare i costi operativi.", "O CEO decidiu cortar os custos operacionais. (executivo)"),
]

def insira_bizu_esercizios():
    if not DATA_PATH.exists():
        print(f"❌ File non trovato: {DATA_PATH}")
        return None
    
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    
    modificazioni = 0
    
    for modulo in data["moduli"]:
        if modulo["id"] in ["A2", "B1", "B2"]:
            print(f"\n[🔄] Elaborando modulo denso: {modulo['nome']}")
            
            pool = BIZU_A2 if modulo["id"] == "A2" else (BIZU_B1 if modulo["id"] == "B1" else BIZU_B2)
            
            for lezione in reversed(modulo.get("unite", [])):
                for _ in range(5):
                    if not pool:
                        break
                    
                    testo_it, contesto = random.choice(pool)
                    
                    esERCIZIO_DATA = {
                        "tipo": "revelar",
                        "pergunta": f"**Esercizio denso #{random.randint(1, 99)}** — Tradurre in italiano:\n\n{testo_it}",
                        "resposta": testo_it,
                        "explicacao": f"📚 **Contesto**: {contexto}."
                    }
                    
                    insert_pos = 0
                    
                    if "escolha" in [e.get("tipo") for e in lezione["exercicios"]]:
                        insert_pos = next(i for i, e in enumerate(lezione["exercicios"]) 
                                       if e.get("tipo") == "escolha")
                    
                    lezione["exercicios"].insert(insert_pos, esERCIZIO_DATA)
                    modificazioni += 1
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print(f"✅ INSERIMENTO ESERCIZI DENSE — COMPLETATO!")
    print(f"   • Modificacoes totais: {modificazioni}")
    print("="*60)
    
    return data

if __name__ == "__main__":
    insira_bizu_esercizios()
