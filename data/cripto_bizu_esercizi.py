# -*- coding: utf-8 -*-
"""
Italian Learning App A2/B1/B2 — Generazione Esercizi con "Bizu" Essenziali
Genera esercizi densi e autentici per i nuovi moduli denso (A2/B1/B2).
"""

import json
from pathlib import Path
import random

DATA_PATH = Path(r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json")

# ============================================================================
# CONTENUTI "BIZU" DENSOS PER NIVELI A2/B1/B2
# ============================================================================

BIZU_A2_ESERCIZIOS = [
    {
        "it": "Tu sei Marco?",
        "pt": "Você é Marco?"
    },
    {
        "it": "Che bella cazzata!",
        "pt": "Que coisa linda! (colloquialismo)"
    },
    {
        "it": "Non ci sto, devo andarmene.",
        "pt": "Não quero ficar, preciso ir embora."
    },
    {
        "it": "Faccio il lavoro come se fosse mio figlio.",
        "pt": "Trabalho como se fosse meu filho." (slang: ci metto le mani)
    },
    {
        "it": "La cosa è finita, chiudiamo la partita.",
        "pt": "A coisa acabou, fechamos a questão."
    }
]

BIZU_B1_ESERCIZIOS = [
    {
        "it": "Si chiude la trattativa domani mattina.",
        "pt": "O acordo será fechado amanhã de manhã." (business)
    },
    {
        "it": "Conosco una persona interessantissima, passiamo a cena!",
        "pt": "Conheço uma pessoa muito interessante, vamos jantar!" (networking)
    },
    {
        "it": "Il software è crashato, devo riavviare il PC.",
        "pt": "O software travou, preciso reiniciar o PC." (tech slang)
    },
    {
        "it": "La notizia è partita da Twitter e ora è sui giornali.",
        "pt": "A notícia começou no Twitter e agora está nos jornais." (social media)
    },
    {
        "it": "Questa roba pignatta non la voglio più!",
        "pt": "Essa besteira eu não quero mais!" (colloquialismo urbano)
    }
]

BIZU_B2_ESERCIZIOS = [
    {
        "it": "Il bilancio mostra una perdita del 15% nel terzo trimestre.",
        "pt": "O balanço mostra uma perda de 15% no terceiro trimestre." (business)
    },
    {
        "it": "Il CEO ha deciso di tagliare i costi operativi.",
        "pt": "O CEO decidiu cortar os custos operacionais." (executivo)
    },
    {
        "it": "L'assemblea è stata approvata con un margine del 65%.",
        "pt": "A assembleia foi aprovada com margem de 65%." (corporativo)
    },
    {
        "it": "Italo Calvino, Il barone rampante: una riflessione sul progresso.",
        "pt": "Calvino, O Barão Rampante: uma reflexão sobre o progresso." (literatura)
    },
    {
        "it": "Fellini, La dolce vita: il declino della società romana del dopoguerra.",
        "pt": "Fellini, A Vida Maravilhosa: o declínio da sociedade romana do pós-guerra." (cinema)
    }
]

# ============================================================================
# FUNZIONI DI INSERIMENTO
# ============================================================================

def insira_bizu_esercizios():
    """Insere esercizi densi nei moduli A2/B1/B2."""
    
    if not DATA_PATH.exists():
        print(f"❌ File non trovato: {DATA_PATH}")
        return None
    
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    
    modificazioni = 0
    
    for modulo in data["moduli"]:
        if modulo["id"] in ["A2", "B1", "B2"]:
            print(f"\n[🔄] Elaborando modulo denso: {modulo['nome']}")
            
            # Calcola quanti esercizi inserire per lezione (basato sul totale)
            tot_les = sum(len(u["exercicios"]) for u in modulo.get("unite", []))
            if tot_les > 0:
                # Inserisci ~10-15 esercizi densi per lezione
                num_esercizi = min(12, len(modulo["id"])) + random.randint(3, 8)
                
                print(f"   📊 Total lezioni: {len(modulo.get('unite', []))}, Esercizios da inserire: {num_esercizi}")
                
                # Scegli esercizi dal pool
                pool = BIZU_A2_ESERCIZIOS if modulo["id"] == "A2" else \
                       (BIZU_B1_ESERCIZIOS if modulo["id"] == "B1" else BIZU_B2_ESERCIZIOS)
                
                # Inserisci esercizi densi
                for lezione in reversed(modulo.get("unite", [])):
                    n_esercizi = num_esercizi // len(modulo.get("unite", [1]))
                    
                    for _ in range(n_esercizi):
                        esERCIZIO_DATA = {
                            "tipo": "revelar",
                            "pergunta": f"**Esercizio denso #{random.randint(1, 99)}** — Tradurre in italiano (colloquialism/business/cultura):\n\n{random.choice(pool)["it"]}",
                            "resposta": random.choice(pool)["it"],
                            "explicacao": f"📚 **Contesto**: {random.choice(pool)["pt"]}.\n💡 **Tipologia**: Vocabolario denso per immersioni reali (A2: sopravvivenza | B1: contemporaneo | B2: professionale)."
                        }
                        
                        # Inserisci prima dei primi esercizi di scelta
                        if "escolha" in [e.get("tipo") for e in lezione["exercicios"]]:
                            insert_pos = next(i for i, e in enumerate(lezione["exercicios"]) 
                                           if e.get("tipo") == "escolha")
                        else:
                            insert_pos = 0
                        
                        lezione["exercicios"].insert(insert_pos, esERCIZIO_DATA)
                        modificazioni += 1
    
    # Salva con formattazione consistente
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print(f"✅ INSERIMENTO ESERCIZI DENSE — COMPLETATO!")
    print(f"   • Modificazioni totali: {modificazioni}")
    print("="*60)
    
    return data

if __name__ == "__main__":
    insira_bizu_esercizios()
