import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def gerar_100_dialoghi():
    path = os.path.join(OUT, 'data', 'dialogi.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    current_len = len(data["dialogi"])
    if current_len >= 150:
        print("Já existem 150 ou mais dialoghi.")
        return

    novos_dialogos = []
    
    # Generate 100 generic dialogues based on variations
    topics = [
        ("In Pizzeria", "🍕", "A1", "Pizzaiolo", ["pizza", "margherita", "forno", "mozzarella"]),
        ("Al Supermercato", "🛒", "A1", "Cassiera", ["spesa", "carrello", "resto", "scontrino"]),
        ("In Stazione", "🚉", "A2", "Bigliettaio", ["treno", "binario", "ritardo", "biglietto"]),
        ("Dal Medico", "🏥", "B1", "Dottore", ["dolore", "febbre", "ricetta", "medicina"]),
        ("Al Parco", "🌳", "A1", "Sconosciuto", ["cane", "passeggiata", "sole", "panchina"]),
        ("In Banca", "🏦", "B1", "Impiegato", ["conto", "prelievo", "carta", "bancomat"]),
        ("Dal Meccanico", "🚗", "B2", "Meccanico", ["motore", "olio", "freni", "guasto"]),
        ("In Gelateria", "🍦", "A1", "Gelataio", ["cono", "coppetta", "gusto", "pistacchio"]),
        ("In Spiaggia", "🏖️", "A2", "Bagnino", ["ombrellone", "lettino", "mare", "sabbia"]),
        ("Dal Barbiere", "💈", "A2", "Barbiere", ["capelli", "barba", "taglio", "shampoo"])
    ]
    
    # We loop the topics 10 times to get 100, varying the context slightly
    for loop in range(10):
        for i, (titulo, icone, nivel, npc, vocab) in enumerate(topics):
            num = current_len + loop * 10 + i + 1
            if num > 150: break
            
            contexto = f"Simulazione situazionale: {titulo} (Variazione {loop+1})."
            
            novo = {
                "id": f"dial_{num:03d}",
                "titulo": f"{titulo} #{loop+1}",
                "icone": icone,
                "nivel": nivel,
                "contexto": contexto,
                "turni": [
                    {
                        "id": 1,
                        "personaggio": npc,
                        "frase": f"Buongiorno! Cosa desidera oggi? Abbiamo {vocab[0]}.",
                        "traducao": f"Bom dia! O que deseja hoje? Temos {vocab[0]}.",
                        "audio_ipa": ""
                    },
                    {
                        "id": 2,
                        "personaggio": "Tu",
                        "frase": f"Vorrei {vocab[0]} e anche {vocab[1]}, per favore.",
                        "traducao": f"Gostaria de {vocab[0]} e também {vocab[1]}, por favor.",
                        "audio_ipa": "",
                        "alternativas": [
                            f"Vorrei {vocab[0]} e anche {vocab[1]}, per favore.",
                            "Non capisco.",
                            "Vado via.",
                            "Non mi piace."
                        ],
                        "resposta_correta": 0
                    },
                    {
                        "id": 3,
                        "personaggio": npc,
                        "frase": f"Certo. Vuole aggiungere {vocab[2]} o {vocab[3]}?",
                        "traducao": f"Certo. Quer adicionar {vocab[2]} ou {vocab[3]}?",
                        "audio_ipa": ""
                    },
                    {
                        "id": 4,
                        "personaggio": "Tu",
                        "frase": f"Sì, mettiamo anche {vocab[2]}. Quanto viene?",
                        "traducao": f"Sim, colocamos também {vocab[2]}. Quanto fica?",
                        "audio_ipa": "",
                        "alternativas": [
                            f"Sì, mettiamo anche {vocab[2]}. Quanto viene?",
                            "Non ho soldi.",
                            "Arrivederci.",
                            "Non mi interessa."
                        ],
                        "resposta_correta": 0
                    },
                    {
                        "id": 5,
                        "personaggio": npc,
                        "frase": "Sono 20 euro in totale.",
                        "traducao": "São 20 euros no total.",
                        "audio_ipa": ""
                    },
                    {
                        "id": 6,
                        "personaggio": "Tu",
                        "frase": "Ecco a lei. Grazie e buona giornata!",
                        "traducao": "Aqui está. Obrigado e bom dia!",
                        "audio_ipa": "",
                        "alternativas": [
                            "Ecco a lei. Grazie e buona giornata!",
                            "Tenga il resto.",
                            "Scusi, ho perso il portafoglio.",
                            "Non pago!"
                        ],
                        "resposta_correta": 0
                    }
                ],
                "vocabulario_chave": vocab,
                "xp_recompensa": 50
            }
            novos_dialogos.append(novo)

    data["dialogi"].extend(novos_dialogos)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Adicionados {len(novos_dialogos)} diálogos. Total: {len(data['dialogi'])}.")

if __name__ == '__main__':
    gerar_100_dialoghi()
