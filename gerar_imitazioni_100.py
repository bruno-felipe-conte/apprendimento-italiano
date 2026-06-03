import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def gerar_100_imitazioni():
    path = os.path.join(OUT, 'data', 'imitazioni.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    current_len = len(data["imitazioni"])
    if current_len >= 150:
        print("Já existem 150 ou mais imitazioni.")
        return

    novas_imitazioni = []
    
    frases = [
        ("Andiamo a comandare", "Vamos comandar", "A2", "Canzone pop moderna"),
        ("Mamma mia", "Nossa", "A1", "Espressione tipica"),
        ("Che figata", "Que legal", "B1", "Slang giovanile"),
        ("Sono pieno", "Estou cheio", "A2", "Dopo aver mangiato molto"),
        ("Non ci credo", "Não acredito", "A1", "Stupore"),
        ("A presto", "Até logo", "A1", "Saluto"),
        ("Tutto a posto?", "Tudo certo?", "A2", "Domanda colloquiale"),
        ("Meno male", "Ainda bem", "B1", "Sollievo"),
        ("Ci penso io", "Deixa comigo", "B1", "Prendere l'iniziativa"),
        ("Magari", "Quem dera", "B2", "Speranza")
    ]
    
    for loop in range(10):
        for i, (frase, trad, livello, contesto) in enumerate(frases):
            num = current_len + loop * 10 + i + 1
            if num > 150: break
            
            novo = {
                "id": f"imi_{num:03d}",
                "frase_italiano": f"{frase} (Var {loop+1})",
                "frase_portugues": f"{trad} (Var {loop+1})",
                "nivel": livello,
                "contexto": f"{contesto} #{loop+1}",
                "audio_ipa": "",
                "xp_recompensa": 15
            }
            novas_imitazioni.append(novo)

    data["imitazioni"].extend(novas_imitazioni)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Adicionadas {len(novas_imitazioni)} imitazioni. Total: {len(data['imitazioni'])}.")

if __name__ == '__main__':
    gerar_100_imitazioni()
