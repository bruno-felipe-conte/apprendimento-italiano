import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def gerar_100_canzoni():
    path = os.path.join(OUT, 'data', 'canzoni.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    current_len = len(data["canzoni"])
    if current_len >= 150:
        print("Já existem 150 ou mais canzoni.")
        return

    novas_canzoni = []
    
    # 10 base templates to loop
    topics = [
        ("Canzone d'Amore", "Artista Sconosciuto", "A2", "❤️", "amore", ["cuore", "bacio", "vita", "sempre"]),
        ("Estate Italiana", "Cantante Estivo", "A1", "☀️", "estate", ["sole", "mare", "spiaggia", "caldo"]),
        ("Notte Stellata", "Gruppo Notturno", "B1", "🌌", "notte", ["stella", "luna", "sogno", "buio"]),
        ("Voglia di Ballare", "DJ Famoso", "A2", "💃", "ballo", ["musica", "ritmo", "festa", "corpo"]),
        ("Tristezza Infinita", "Cantautore", "B2", "😢", "tristezza", ["lacrima", "addio", "dolore", "piangere"]),
        ("Viaggio Lontano", "Band Viaggiante", "B1", "✈️", "viaggio", ["strada", "treno", "partire", "lontano"]),
        ("Amicizia Vera", "Amici Uniti", "A2", "🤝", "amicizia", ["amico", "fratello", "insieme", "fiducia"]),
        ("Ribellione Giovanile", "Rocker Ribelle", "B2", "🎸", "ribellione", ["libertà", "regole", "rabbia", "scuola"]),
        ("Ricordi d'Infanzia", "Cantante Nostalgico", "C1", "🧸", "nostalgia", ["gioco", "bambino", "madre", "padre"]),
        ("Il Senso della Vita", "Filosofo Pop", "C2", "🧘", "vita", ["destino", "senso", "tempo", "verità"])
    ]
    
    for loop in range(10):
        for i, (titulo, artista, nivel, icone, tema, vocab) in enumerate(topics):
            num = current_len + loop * 10 + i + 1
            if num > 150: break
            
            estrofes = []
            for e in range(1, 5):
                palavra = vocab[(e-1) % len(vocab)]
                estrofes.append({
                    "id": e,
                    "texto_completo": f"Questo è un verso con la parola {palavra} dentro.",
                    "texto_lacuna": f"Questo è un verso con la parola ___ dentro.",
                    "palavra_oculta": palavra,
                    "traducao": f"Este é um verso com a palavra {palavra} dentro.",
                    "dica": f"Parola chiave {e}"
                })
                
            novo = {
                "id": f"can_{num:03d}",
                "titulo": f"{titulo} (Vol. {loop+1})",
                "artista": f"{artista} #{loop+1}",
                "nivel": nivel,
                "icone": icone,
                "tema": tema,
                "estrofes": estrofes,
                "vocabulario_chave": vocab,
                "xp_recompensa": 40
            }
            novas_canzoni.append(novo)

    data["canzoni"].extend(novas_canzoni)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Adicionadas {len(novas_canzoni)} canzoni. Total: {len(data['canzoni'])}.")

if __name__ == '__main__':
    gerar_100_canzoni()
