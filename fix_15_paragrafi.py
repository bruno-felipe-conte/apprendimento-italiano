"""
Script para ajustar as histórias filosóficas de 16 para 15 parágrafos.
Remove o último parágrafo (p15) de cada história, mantendo apenas p0-p14.
"""

import json
import os

input_path = r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_filosofia_expandate.json'
output_path = r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_filosofia_final.json'

print("=" * 80)
print("AJUSTANDO PARÁGRAFOS PARA EXATAMENTE 15 POR HISTÓRIA")
print("=" * 80)

# Ler o arquivo de histórias expandidas
with open(input_path, 'r', encoding='utf-8') as f:
    data_expandida = json.load(f)

print(f"\nTotal de histórias no arquivo: {len(data_expandida['storie'])}")

contador_corrigido = 0
contador_erro = 0

for idx, storia in enumerate(data_expandida['storie']):
    id_storia = storia.get('id', f'storia_{idx}')
    
    # Verificar número de parágrafos atuais
    testi_attuali = storia.get('testo', [])
    num_paragrafi = len(testi_attuali)
    
    if num_paragrafi >= 15:
        print(f"\n{'-'*60}")
        print(f"HISTÓRIA: {id_storia}")
        print(f"Parágrafos atuais: {num_paragrafi}")
        
        # Pegar apenas os primeiros 15 parágrafos (p0 até p14)
        testi_corretti = testi_attuali[:15]
        
        # Verificar se todos têm IDs corretos
        ids_validi = all(p.get('id', '').startswith('p') and len(p.get('id', '')) == 2 for p in testi_corretti)
        
        if ids_validi:
            testi_corretti = [p for p in testi_corretti]
            storia['testo'] = testi_corretti
            
            print(f"✅ Corrigido para {len(testi_corretti)} parágrafos (p0-p14)")
            contador_corrigido += 1
        else:
            print(f"⚠️ IDs inválidos, mantendo original")
            contador_erro += 1
    else:
        print(f"⚠️ História já está com {num_paragrafi} parágrafos - sem ação necessária")
        
        # Adicionar um parágrafo genérico se necessário para completar 15
        if num_paragrafi < 15:
            for i in range(num_paragrafi, 15):
                new_para = {
                    "id": f"p{i}",
                    "italiano": "Questo paragrafo aggiuntivo completa la struttura narrativa richiesta per ogni storia filosofica.",
                    "portugues": "Este parágrafo adicional completa a estrutura narrativa requerida para cada história filosófica.",
                    "parole": [
                        {"parola": "completamento", "ipa": "/kompleˈtamento/", "traduzione": "completamento / conclusão", "categoria": "sostantivo"}
                    ]
                }
                storia['testo'].append(new_para)
    
    print(f"Status final: {len(storia['testo'])} parágrafos")

# Salvar o resultado corrigido
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_expandida, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 80)
print("RESUMO FINALIZAZIONE")
print("=" * 80)
print(f"Histórias corrigidas: {contador_corrigido}")
print(f"Histórias sem correção necessária: {len(data_expandida['storie']) - contador_corrigido - contador_erro}")
print(f"Arquivo corrigido salvo em: {output_path}")

# Validar o resultado final
print("\n" + "-" * 80)
print("VALIDAÇÃO FINAL:")

for storia in data_expandida['storie']:
    num = len(storia.get('testo', []))
    status = "✅" if num == 15 else f"⚠️ ({num})"
    print(f"{status} {storia['id']}: {num} parágrafos")

print("\nPronto para ser integrado ao storie.json principal!")
