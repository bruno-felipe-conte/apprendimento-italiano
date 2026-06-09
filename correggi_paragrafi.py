"""
Script simplificado para ajustar as histórias de 16 para exatamente 15 parágrafos.
Remove sempre o último parágrafo (p15), mantendo p0-p14.
"""

import json

input_path = r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_filosofia_expandate.json'
output_path = r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_filosofia_final.json'

print("=" * 80)
print("AJUSTANDO PARÁGRAFOS: REMOVENDO p15, MANTENDO p0-p14")
print("=" * 80)

# Ler o arquivo de histórias expandidas
with open(input_path, 'r', encoding='utf-8') as f:
    data_expandida = json.load(f)

contador_corrigido = 0

for idx, storia in enumerate(data_expandida['storie']):
    id_storia = storia.get('id', f'storia_{idx}')
    
    testi_attuali = storia.get('testo', [])
    num_paragrafi = len(testi_attuali)
    
    if num_paragrafi == 16:
        print(f"\n{'-'*60}")
        print(f"HISTÓRIA: {id_storia} (índice {idx})")
        
        # Pegar apenas os primeiros 15 parágrafos
        testi_corretti = testi_attuali[:15]
        
        print(f"Removendo p15, mantendo p0-p14")
        print(f"Novo total: {len(testi_corretti)} parágrafos")
        
        storia['testo'] = testi_corretti
        
        # Validar estrutura básica
        validacao_ok = all(
            isinstance(p, dict) and 
            'id' in p and 
            'italiano' in p and 
            'portugues' in p and
            len(p.get('parole', [])) >= 1
            for p in testi_corretti
        )
        
        if validacao_ok:
            print(f"✅ Estrutura válida!")
            contador_corrigido += 1
        else:
            print(f"⚠️ Problemas de validação na estrutura")
    
    elif num_paragrafi != 15:
        print(f"\n⚠️ {id_storia}: Já tem {num_paragrafi} parágrafos - sem ação")

# Salvar o resultado corrigido
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data_expandida, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 80)
print("RESUMO FINALIZAZIONE")
print("=" * 80)
print(f"Histórias ajustadas de 16→15 parágrafos: {contador_corrigido}")
print(f"Arquivo corrigido salvo em: {output_path}")

# Validar o resultado final
print("\n" + "-" * 80)
print("VALIDAÇÃO FINAL - TODAS COM EXATAMENTE 15 PARÁGRAFOS:")

todos_ok = True
for storia in data_expandida['storie']:
    num = len(storia.get('testo', []))
    status = "✅" if num == 15 else f"⚠️ ({num})"
    if num != 15:
        todos_ok = False
        print(f"{status} {storia['id']}: {num} parágrafos")
    # Mostrar apenas se tiver problema ou no começo/fim
    if num == 15 or len([s for s in data_expandida['storie'] if len(s.get('testo', [])) != 15]) < 3:
        pass

print(f"\nTotal histórias com EXATAMENTE 15 parágrafos: {sum(1 for s in data_expandida['storie'] if len(s.get('testo', [])) == 15)}/21")

if todos_ok:
    print("✅ TODAS AS HISTÓRIAS PASSARAM NA VALIDAÇÃO!")
else:
    print("⚠️ Algumas histórias precisam de atenção adicional.")

print("\nPronto para integração no storie.json principal!")
