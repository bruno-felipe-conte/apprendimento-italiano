# -*- coding: utf-8 -*-
"""
Italian Learning App A2/B1/B2 — Contenuto Denso con "Bizu" Essenziali
Sostituisce i moduli fracchi (A2/B1/B2) con contenuto denso e autentico.
"""

import json
from pathlib import Path

DATA_PATH = Path(r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json")

# ============================================================================
# NOVI MODULI CON CONTENUTO DENSO (A2/B1/B2)
# ============================================================================

MODULI_BIZU = {
    "A2": {
        "id": "A2",
        "nome": "A2 — Sopravvivenza e Imersione Reale",
        "descrizione": "Vocabolario denso per immersioni reali: viaggi, lavoro informale, relazioni interpersonali, gergo regionale essenziale.",
        "lezioni": 30,
        "temi_densita": [
            "Gergo giovanile italiano (figa, roba, che bella cazzata, non ci sto),",
            "Slang lavorativo quotidiano (faccio il lavoro → ci metto le mani, chiudo la partita → finisco l'opera),",
            "Espressioni regionali basiche (Roma: e poi/insomma/ben trovato; Milano: che pignatta/che guaio; Napoli: che cavoli/casa d'altra gente),",
            "Vocabolario turismo informale (albergo = hotel, ristorante = dove mangiamo, supermercato = dove compriamo, stazione = dove prendiamo il treno),",
            "Relazioni interpersonali autentiche (come si dice scusa/compri un caffè/ci vediamo/domani/a presto),",
            "Colloquialismi essenziali (ci fa ridere/non ci va bene/faccio una risata/mettiamoci d'accordo/siamo in disaccordo),",
            "Vocabolario gastronomia informale (cena = pranzetto, merenda = spuntino, aperitivo = birretta e patatine, digestivo = caffè amaro),"
        ]
    },
    
    "B1": {
        "id": "B1", 
        "nome": "B1 — Italiano Contemporaneo (XXI Secolo)",
        "descrizione": "Italiano del XXI secolo: slang lavorativo, espressioni digitali, regionalismi urbani, conversazioni reali.",
        "lezioni": 30,
        "temi_densita": [
            "Business moderno italiano (si chiude la trattativa, portiamo il contratto in firma, chiudiamo il meeting),",
            "Networking e relazioni professionali (conosco gente interessante, ho conosciuto un collega importante, passiamo a cena),",
            "Tecnologia e digital (ho aggiornato i driver, il software è crashato, il server è down, il sistema si è bloccato),",
            "Social media e comunicazioni digitali (la notizia è partita da Twitter, abbiamo postato su LinkedIn, abbiamo commentato il video),",
            "Colloquialismi urbani (è una roba pazzesca/quella cosa/cosa dici che mi fai/domani mattina),",
            "Slang tech e informatico (crashare/hangarsi/staccare la spina/avere un bug/mettiamo mano al codice),",
            "Espressioni generazionali (la mia generazione/il boom generation i millennials lo zio, non ti capisco come fai con questo sistema)"
        ]
    },
    
    "B2": {
        "id": "B2",
        "nome": "B2 — Italiano Professionale e Culturale Alto Livello",
        "descrizione": "Business italiano autentico, letteratura contemporanea, cinema, teatro, politica, arte, giornalismo moderno.",
        "lezioni": 30,
        "temi_densita": [
            "Terminologia business avanzata (il bilancio mostra una perdita, il CEO ha deciso di tagliare i costi, l'assemblea è stata approvata con margine),",
            "Letteratura contemporanea italiana (Italo Calvino Il barone rampante, Umberto Eco Il nome della rosa, Antonio Tabucchi Sostiene Pereira),",
            "Cinema e teatro italiano (Fellini La dolce vita, Visconti Rocco e i suoi fratelli, Sorrentino La grande bellezza),",
            "Politica e società (elezioni europee, referendum costituzionale, impeachment del premier, elezioni regionali),",
            "Arte e spettacolo (Biennale di Venezia, Triennale Milano, Festival di Venezia, Sanremo),",
            "Giornalismo di qualità (il quotidiano La Repubblica, il magazine Vanity Fair, la rivista L'Espresso, il programma Radio 3),",
            "Economia e finanza (mercati finanziari, tassi di interesse, inflazione, PIL, FMI, BCE),"
        ]
    }
}

# ============================================================================
# LOGICA DI SOSTITUZIONE DEI MODULI FRACCHI
# ============================================================================

def replace_bisu_moduli():
    """Sostituisce i moduli A2/B1/B2 con contenuto denso e autentico."""
    
    if not DATA_PATH.exists():
        print(f"❌ File non trovato: {DATA_PATH}")
        return None
    
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
    
    # Rimuovi/modifica i moduli fraci A2/B1/B2 se presenti
    nuovi_moduli = []
    for modulo in data["moduli"]:
        if modulo["id"] in ["A2", "B1", "B2"]:
            print(f"\n[🔄] Sostituendo modulo: {modulo['nome']}")
            
            bizu = MODULI_BIZU.get(modulo["id"])
            if bizu:
                modulo["nome"] = bizu["nome"]
                modulo["descrizione"] = bizu["descrizione"]
                modulo["lezioni"] = bizu["lezioni"]  # Aggiunge lezioni dense
                
                print(f"    ✅ Modificato: {modulo['id']} — {modulo['nome'][:60]}...")
                continue
        
        nuovi_moduli.append(modulo)
    
    data["moduli"] = nuovi_moduli
    
    # Aggiungi i moduli densi se non presenti
    for bizu_id in ["A2", "B1", "B2"]:
        if not any(m["id"] == bizu_id for m in data["moduli"]):
            data["moduli"].append(MODULI_BIZU[bizu_id])
            print(f"\n[➕] Aggiunto modulo denso: {MODULI_BIZU[bizu_id]['id']}")
    
    # Salva con formattazione consistente
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("✅ SOSTITUZIONE CONTENUTO DENSO — COMPLETATA!")
    print("="*60)
    return data

if __name__ == "__main__":
    replace_bisu_moduli()
