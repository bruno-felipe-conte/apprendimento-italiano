"""
Script para expandir as 21 histórias filosóficas para 15 parágrafos cada.
Cada história será gerada com nível C2 em italiano, tradução pt-BR e palavras-chave filosóficas.
"""

import json
import time
from openai import OpenAI

# Configurar client (pode usar API key local ou proxy)
client = OpenAI(
    api_key="sk-...",  # Substitua pela sua API key ou use proxy
    base_url="https://..."  # URL do provider desejado
)

def call_llm_historical_prompt(instruction, context):
    """Chama o modelo histórico para gerar conteúdo filosófico."""
    
    prompt = f"""
# INSTRUÇÃO PARA O GPT/CLAUDE:
{instruction}

---
TEXTO ATUAL A EXPANDIR (contexto base):
{context}

---
GENTE DE HISTÓRIA: Socrate nel Processo - Julgamento de Sócrates em Atenas, 399 a.C.

REGRAS OBRIGATÓRIAS PARA GERAÇÃO:
1. Escreva EXATAMENTE 15 parágrafos numerados (p0 até p14)
2. Cada parágrafo deve ter 3 a 5 frases ricas com vocabulário filosófico autêntico em italiano (nível C2)
3. A história deve ter arco narrativo completo:
   - Parágrafos 1-3: Contexto histórico e cena de abertura - atmosfera do tribunal, tensão, personagens
   - Parágrafos 4-7: Desenvolvimento do conflito filosófico - acusações, reações, diálogo interno
   - Parágrafos 8-11: Diálogo ou argumentação central - Sócrates questiona, desenvolve seu argumento ético
   - Parágrafos 12-14: Clímax ou resolução filosófica - veredito, reação da plateia, consequências
   - Parágrafo 15: Reflexão final / legado - significado histórico, impacto na filosofia ocidental

4. Tom: narrativo, dramático, literário — NÃO didático! Personagens devem falar e agir
5. Use linguagem elevada em italiano: sofisma, dialeto, ethos, pathos, logos, noos, etc.

FORMATO DE SAÍDA (JSON puro, SEM markdown):
[
  {
    "id": "p0",
    "italiano": "...",
    "portugues": "...", 
    "parole": [
      {"parola": "...", "ipa": "...", "traduzione": "...", "categoria": "sostantivo/verbo/aggettivo/avverbio"}
    ]
  }
]

IMPORTANTE: O JSON deve ser válido e sem markdown!
"""
    
    try:
        response = client.chat.completions.create(
            model="anthropic/claude-3-5-haiku-20241022",  # Modelo adequado para criatividade
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=8000,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Erro na chamada: {e}")
        return None

def main():
    """Carrega histórias e gera expansão para cada uma."""
    
    # Carregar o arquivo existente
    with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 80)
    print("INICIANDO EXPANSÃO DAS HISTÓRIAS FILOSÓFICAS")
    print("=" * 80)
    
    stories_to_expand = [s for s in data['storie'] if s.get('id', '').startswith('fil_')]
    print(f"\nHISTÓRIAS PARA EXPANDIR: {len(stories_to_expand)}")
    
    resultados = []
    
    for idx, story in enumerate(stories_to_expand):
        print(f"\n{'='*80}")
        print(f"HISTÓRIA {idx+1}/{len(stories_to_expand)}: {story['id']}")
        print(f"Título: {story['titulo']}")
        print(f"Status atual: {len(story['testo'])} parágrafos")
        
        # Preparar contexto da história
        contexto_base = f"{json.dumps(story['testo'], ensure_ascii=False)[:2000]}..." if story['testo'] else "História inicial com 2-3 parágrafos base."
        
        print(f"Gerando conteúdo para {story['id']}...")
        
        # Chamar LLM para gerar expansão
        expansao = call_llm_historical_prompt(
            f"""Gere 15 parágrafos narrativos em italiano nível C2 para a história '{story['titulo']}'.
Contexto: {story.get('descricao', '')}
Tema filosófico: {story['id'].replace('_', ' ').title()}
""",
            contexto_base
        )
        
        if expansao and '{"id":' in expansao:
            try:
                nova_testo = json.loads(expansao)
                print(f"✅ Geração concluída! {len(nova_testo)} parágrafos gerados.")
                
                # Verificar qualidade
                ids_validos = all(
                    isinstance(p, dict) and 
                    'id' in p and 
                    'italiano' in p and 
                    'portugues' in p and 
                    'parole' in p and
                    len(p['id']) == 2 and  # p0, p1, etc.
                    len(p['italiano'].strip()) > 50 and  # Mínimo de caracteres
                    1 <= len(p['parole']) <= 4
                    for p in nova_testo
                )
                
                if ids_validos:
                    print("✅ Validação de estrutura: OK")
                else:
                    print("⚠️ Alguns parágrafos podem precisar de ajuste manual.")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao parsear JSON: {e}")
                continua = input("Deseja ver o output raw? (s/n): ")
                if continua.lower() == 's':
                    print(expansao[:500])
        else:
            print(f"⚠️ Geração não retornou formato esperado. Continuar para próxima?")
            
        # Pequena pausa entre histórias
        time.sleep(1)
        
        resultados.append({
            'id': story['id'],
            'titulo': story['titulo'],
            'status': 'concluída' if expansao and '"id":' in expansao else 'pendente',
            'num_paras': len(json.loads(expansao)) if expansao and '"id":' in expansao else len(story['testo'])
        })
    
    # Salvar progresso
    print("\n" + "=" * 80)
    print("PROGRESSO FINAL")
    print("=" * 80)
    
    for r in resultados:
        status_str = "✅" if r['status'] == 'concluída' else "⏳"
        print(f"{status_str} {r['id']}: {r['num_paras']} parágrafos ({r['status']})")
    
    # Salvar resultados
    with open(r'C:\Users\bruno\Documents\italian-learning-app-pro\data\storie_expansao.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    print("\nResumo salvo em: storie_expansao.json")

if __name__ == "__main__":
    main()
