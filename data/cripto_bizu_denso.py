# -*- coding: utf-8 -*-
"""
Italian Learning App A2/B1/B2 — Generazione Contenuto Denso Completo
Cria esercizi densi con vocabolario autentico italiano per immersioni reali.
"""

import json
from pathlib import Path
import random

DATA_PATH = Path(r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json")

# ============================================================================
# VOCABOLARIO DENSO PER NIVELI — CONTENUTI AUTENTICI ITALIANI
# ============================================================================

VOCAB_A2_SUPERVIVENZA = {
    "gergo_giovane": [
        ("Che bella cazzata!", "Que coisa linda!"),
        ("Figolo questa roba!", "Que cara esse coisa!"),
        ("Non ci sto più, devo andarmene.", "Não quero ficar mais, preciso ir embora."),
        ("Mi fa ridere questa storia.", "Isso me faz rir."),
    ],
}

VOCAB_B1_CONTEMPORANEO = {
    "business_moderno": [
        ("Si chiude la trattativa domani mattina alle nove.", "O acordo será fechado amanhã de manhã às nove."),
        ("Portiamo il contratto in firma entro venerdì.", "Entregamos o contrato para assinatura até sexta-feira."),
        ("L'agenda è piena fino al prossimo mese, dobbiamo priorizzare.", "A agenda está cheia até o próximo mês, precisamos priorizar."),
    ],
}

VOCAB_B2_PROFSSIONALE = {
    "business_advanced": [
        ("Il bilancio mostra una perdita del 15% nel terzo trimestre.", "O balanço mostra uma perda de 15% no terceiro trimestre." + " (bilancio semestrale)"),
        ("Il CEO ha deciso di tagliare i costi operativi.", "O CEO decidiu cortar os custos operacionais." + " (cutting costs)"),
    ],
}

def genera_contenuto_denso():
    """Genera contenuto denso completo per A2/B1/B2."""
    
    if not DATA_PATH.exists():
        print(f"❌ File non trovato: {DATA_PATH}")
        return None
    
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    
    # Genera contenuto per moduli A2/B1/B2 senza unite
    for modulo in data["moduli"]:
        if modulo["id"] in ["A2", "B1", "B2"] and len(modulo.get("unite", [])) == 0:
            print(f"\n[🔄] Generando contenuto denso per {modulo['id']} — {modulo['nome'][:50]}")
            
            # Mapeamento de vocab_por nivel
            vocab_mapp = {"A2": VOCAB_A2_SUPERVIVENZA, "B1": VOCAB_B1_CONTEMPORANEO, "B2": VOCAB_B2_PROFSSIONALE}
            vocab_pool = vocab_mapp[modulo["id"]]
            
            # Crea 30 lezioni dense con esercizi autentici
            for i in range(1, 31):
                tema_contenuto = list(vocab_pool.keys())[0]
                frase, contenuto = random.choice(vocab_pool[tema_contenuto])
                
                num_esercizi = random.randint(6, 8)
                
                unita_densita = {
                    "num": f"Lezione {i}",
                    "descrizione": f"**{tema_contenuto.upper()}** — Vocabolario denso per immersione reale.",
                    "teoria": "**Contesto tematico**: Questa lezione approfondisce il vocabolario specifico per [" + tema_contenuto.replace("_", " ") + "] con esercizi pratici di traduzione e comprensione scritta.",
                    "exercicios": []
                }
                
                for j in range(num_esercizi):
                    esERCIZIO_DATA = {
                        "tipo": random.choice(["revelar", "escolha"]),
                        "pergunta": f"**Esercizio denso #{j+1}**\n\n{frase}",
                        "resposta": frase,
                        "explicacao": f"📚 **Contesto autentico**: {contenuto}. Questa frase è tipica del linguaggio italiano reale."
                    }
                    
                    unita_densita["exercicios"].append(esERCIZIO_DATA)
                
                # Crea la prima unità densa se non esiste
                if not modulo.get("unite"):
                    modulo["unite"] = [unita_densita]
            
            print(f"   ✅ Generato {len(modulo.get('unite', []))} lezioni dense")
    
    # Salva con formattazione consistente
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("✅ GENERAZIONE CONTENUTO DENSO — COMPLETATA!")
    print("="*60)
    
    return data

if __name__ == "__main__":
    genera_contenuto_denso()
