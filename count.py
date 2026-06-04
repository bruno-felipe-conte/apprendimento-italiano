import json
for i in range(1, 11):
    try:
        with open(f'data/templo-{i}.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
            palavras = d.get("vocabulario", d.get("palavras", []))
            print(f'Templo {i}: {len(palavras)} palavras')
    except Exception as e:
        print(f'Templo {i}: error {e}')
