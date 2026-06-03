import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def gerar_100_contesti():
    path = os.path.join(OUT, 'data', 'contesti.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    current_len = len(data["contesti"])
    if current_len >= 150:
        print("Já existem 150 o mais contesti.")
        return

    novos_contesti = []
    
    contextos = [
        ("Romanzo Criminale", "Romanzo Criminale", "Série", "B2", "Roma negli anni 70", ["banda", "soldi", "capo", "pistola", "droga"]),
        ("Il Commissario Montalbano", "Montalbano", "Série", "C1", "Sicilia", ["commissario", "indagine", "omicidio", "mare", "cibo"]),
        ("Nuovo Cinema Paradiso", "Cinema Paradiso", "Filme", "A2", "Passione per il cinema", ["pellicola", "bacio", "piazza", "prete", "fuoco"]),
        ("La Meglio Gioventù", "La Meglio Gioventù", "Filme", "B2", "Storia d'Italia", ["famiglia", "fratello", "storia", "medico", "poliziotto"]),
        ("Suburra", "Suburra", "Série", "B2", "Mafia a Roma", ["potere", "politica", "chiesa", "famiglia", "terreno"]),
        ("L'Amica Geniale", "L'Amica Geniale", "Série", "B2", "Napoli anni 50", ["scuola", "scarpe", "rione", "invidia", "matrimonio"]),
        ("Perfetti Sconosciuti", "Perfetti Sconosciuti", "Filme", "B1", "Cena tra amici", ["cellulare", "segreto", "messaggio", "tradimento", "verità"]),
        ("La Vita è Bella", "La Vita è Bella", "Filme", "A2", "Amore e speranza", ["gioco", "carro armato", "principessa", "premio", "sorriso"]),
        ("Gomorra", "Gomorra", "Série", "C1", "Camorra a Napoli", ["clan", "boss", "droga", "guerra", "strada"]),
        ("Boris", "Boris", "Série", "C1", "Dietro le quinte di una fiction", ["regista", "attore", "luci", "scena", "qualità"])
    ]
    
    for loop in range(10):
        for i, (titulo, origin, tipo, livello, desc, vocab) in enumerate(contextos):
            num = current_len + loop * 10 + i + 1
            if num > 150: break
            
            novo = {
                "id": f"ctx_{num:03d}",
                "titulo": f"{titulo} (Parte {loop+1})",
                "origem": origin,
                "tipo": tipo,
                "nivel": livello,
                "descricao": desc,
                "vocabulario": [
                    {"italiano": v, "portugues": f"Trad de {v}", "exemplo": f"Esempio: {v}."} 
                    for v in vocab
                ],
                "xp_recompensa": 20
            }
            novos_contesti.append(novo)

    data["contesti"].extend(novos_contesti)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Adicionados {len(novos_contesti)} contesti. Total: {len(data['contesti'])}.")

if __name__ == '__main__':
    gerar_100_contesti()
