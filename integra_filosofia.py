"""
Script para integrar as histórias filosóficas expandidas no storie.json principal.
Substitui o campo "testo" das histórias com IDs 'fil_' pelos novos textos expandidos.
"""

import json

# Caminhos dos arquivos
input_json = r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_filosofia_final.json'
output_json = r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie.json'

print("=" * 80)
print("INTEGRANDO HISTÓRIAS EXPANDIDAS NO STORIE.JSON PRINCIPAL")
print("=" * 80)

# Ler o arquivo de histórias expandidas
with open(input_json, 'r', encoding='utf-8') as f:
    storie_expansate = json.load(f)

# Ler o JSON principal
with open(output_json, 'r', encoding='utf-8') as f:
    data_principale = json.load(f)

print(f"\nHistórias expandidas carregadas: {len(storie_expansate['storie'])}")

# Contar substituições feitas
substituite = 0

for storia in data_principale.get('storie', []):
    id_storia = storia.get('id', '')
    
    # Verificar se é uma história filosófica que precisa ser atualizada
    if id_storia.startswith('fil_'):
        # Procurar a história correspondente no arquivo expandido
        storia_espana = None
        for se in storie_expansate['storie']:
            if se.get('id') == id_storia:
                storia_espana = se
                break
        
        if storia_espana and len(storia_espana.get('testo', [])) == 15:
            # Substituir o campo "testo" pelo novo texto expandido
            print(f"\n{'='*60}")
            print(f"SUBSTITUINDO: {id_storia}")
            print(f"Título: {storia_espana.get('titulo', 'N/A')}")
            print(f"Novos parágrafos: {len(storia_espana['testo'])}")
            
            storia['testo'] = se['testo']  # Já copiamos o array inteiro acima
            
            # Manter metadados importantes da história original se não houver no expandido
            if not storia_espana.get('descripcion_it'):
                storia_espana['descripcion_it'] = storia.get('descricao', '')
            if not storia_espana.get('titulo_pt'):
                storia_espana['titulo_pt'] = ''  # Deixar vazio se não existir
            
            substituite += 1
        else:
            print(f"⚠️ {id_storia}: Não encontrada no arquivo expandido (mantendo original)")

print(f"\n{'='*80}")
print("RESULTADO DA INTEGRAZIONE:")
print("=" * 80)
print(f"Histórias filosóficas atualizadas: {substituite}")

# Salvar o resultado final
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(data_principale, f, ensure_ascii=False, indent=2)

print(f"\n✅ Arquivo salvo em: {output_json}")

# Validar o resultado final
print("\n" + "-" * 80)
print("VALIDAZIONE FINALE DEL FILE JSON:")

conteggio_filo = 0
for storia in data_principale.get('storie', []):
    if storia.get('id', '').startswith('fil_'):
        num_paragrafi = len(storia.get('testo', []))
        conteggio_filo += 1
        
        # Mostrar primeiro e último de cada história para conferência
        if conteggio_filo <= 3:  # Mostrar primeiros 3 como exemplo
            print(f"\n{'='*80}")
            print(f"HISTÓRIA: {storia['id']}")
            print(f"Título: {storia.get('titulo', 'N/A')}")
            print(f"Número paragrafi: {num_paragrafi}")
            print("\nPrimeiro parágrafo (p0):")
            p0 = storia['testo'][0]
            print(f"  Italiano: {p0['italiano'][:150]}...")
            print(f"  Português: {p0['portugues'][:150]}...")
            print(f"  Palavras chave: {len(p0.get('parole', []))}")

print(f"\n{'='*80}")
print(f"Total histórias filosóficas validadas: {conteggio_filo}/21")

if conteggio_filo == 21 and sum(1 for s in data_principale['storie'] if s.get('id', '').startswith('fil_') and len(s.get('testo', [])) == 15) == 21:
    print("✅ TODAS AS HISTÓRIAS TÊM EXATAMENTE 15 PARÁGRAFOS!")
else:
    print("⚠️ Algumas histórias podem não estar corretas.")

print("\nIntegração concluída com sucesso!")
