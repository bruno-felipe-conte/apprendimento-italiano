#!/usr/bin/env python3
"""Unifica storie filosofiche classiche nel file storie.json."""

import json
import os

base_path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data"
storie_file = os.path.join(base_path, "storie.json")

# File di storie da unire - percorsi corretti senza escape problematici
filo_stories_paths = [
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_platone_socrate.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_aristotele.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_epicuro.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_seneca.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_plotino.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_marco_aurelio.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_epicuro2.json",
    "C:/Users/bruno/Documents/italian-learning-app-pro/data/storie_plotino2.json",
]

# Leggi le storie filosofiche da tutti i file e assegna ID corretti
filo_stories_list = []
next_id = 0

for f_path in filo_stories_paths:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Estrai le storie dal dizionario (sono già una lista di dict)
                for item in data.values():
                    if isinstance(item, dict):
                        # Assegna ID corretto per formato a capitoli
                        capitolo = item.get('p', 0) or 0
                        base_id = item.get('id') or f"stor_{next_id:03d}"
                        
                        nuova_storia = {
                            "id": base_id,
                            "titolo": item.get('titolo'),
                            "livello": item.get('livello'),
                            "testo": item.get('testo'),
                            "traduzione_en": item.get('traduzione_en'),
                            "vocabola": item.get('vocabola'),
                            "autor": "Filosofia Classica",
                            "tema": "filosofia"
                        }
                        filo_stories_list.append(nuova_storia)
                        next_id += 1
                print(f"Caricati {len([i for i in data.values() if isinstance(i, dict)])} storie da {os.path.basename(f_path)}")
            except json.JSONDecodeError as e:
                print(f"Errore JSON in {f_path}: {e}")

print(f"\nTotale storie filosofiche caricate: {len(filo_stories_list)}")

# Leggi lo storico file storie.json
with open(storie_file, 'r', encoding='utf-8') as f:
    storie_data = json.load(f)

# Controlla se esiste una lista 'storie' e calcola dove inserire le nuove
if 'storie' in storie_data and storie_data['storie']:
    ultima_storia = storie_data['storie'][-1]
    ultimo_id_num = int(ultima_storia['id'].replace('stor_', '')) if 'stor_' in ultima_storia['id'] else 0
    print(f"\nUltima storia esistente: {ultima_storia['id']}")
else:
    storie_data['storie'] = []
    ultimo_id_num = 0

# Ordina le nuove storie per ID numerico
filo_stories_list.sort(key=lambda x: (int(x.get('id', 'stor_000').replace('stor_', '')) or 0))

# Unisci le liste - aggiungi dopo l'ultima esistente
storie_data['storie'].extend(filo_stories_list)

# Salva il file unificato con formattazione più compatatta per evitare timeout API
with open(storie_file, 'w', encoding='utf-8') as f:
    json.dump(storie_data, f, ensure_ascii=False, indent=None, separators=(',', ': '))

print(f"\n✅ Salvato {len(storie_data['storie'])} storie totali in {storie_file}")
print("Storie filosofiche aggiunte:", len(filo_stories_list))
