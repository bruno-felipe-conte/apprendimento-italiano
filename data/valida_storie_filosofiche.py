#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valida_storie_filosofiche.py - Valida APENAS as histórias filosóficas expandidas

Uso:
    python valida_storie_filosofiche.py              # Valida só as histórias filosóficas
    python valida_storie_filosofiche.py --json       # Saída em JSON para programação
"""

import json
import sys


def carregar_stories(path: str) -> list:
    """Carrega o JSON das histórias."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['storie'] if isinstance(data.get('storie'), list) else []


def e_historia_filosofica(storia) -> bool:
    """Verifica se é uma história filosófica (com ID começando com 'fil_')."""
    id_hist = storia.get('id', '').lower()
    return id_hist.startswith('fil_')


def validar_storia(storia) -> tuple[bool, str, int]:
    """Valida uma história filosófica e retorna (ok, mensagem, paragrafos)."""
    
    id_hist = storia.get('id', 'N/A')
    titulo = storia.get('titolo', '')
    testo = storia.get('testo', [])
    
    num_paragrafos = len(testo) if isinstance(testo, list) else 0
    
    # Verifica estrutura dos parágrafos (amostra primeiros 3)
    for i, para in enumerate(testo[:3]):
        if not all(k in para for k in ['id', 'italiano', 'portugues', 'parole']):
            return False, f"Campos faltando no parágrafo {i}", num_paragrafos
    
    # Verifica palavras-chave (amostra primeiros 5 parágrafos)
    for i, para in enumerate(testo[:5]):
        parole = para.get('parole', [])
        if not isinstance(parole, list):
            return False, f"'parole' não é lista no parágrafo {i}", num_paragrafos
        
        for p in parole:
            if not all(k in p for k in ['parola', 'ipa', 'traduzione']):
                return False, f"Campos faltando em palavra do parágrafo {i}", num_paragrafos
    
    return True, "Valido", num_paragrafos


def main():
    BASE_DIR = r'C:\Users\bruno\Documents\italian-learning-app-pro\data'
    ARQUIVO_PRINCIPAL = f'{BASE_DIR}/storie.json'
    
    print("=" * 80)
    print("VALIDAÇÃO DE HISTÓRIAS FILOSÓFICAS EXPANDIDAS")
    print("(Somente histórias com ID começando em 'fil_')")
    print("=" * 80)
    
    try:
        historias = carregar_stories(ARQUIVO_PRINCIPAL)
        
        # Filtra APENAS histórias filosóficas
        filosofiche = [h for h in historias if e_historia_filosofica(h)]
        
        print(f"\n📚 Total de histórias no arquivo: {len(historias)}")
        print(f"   → Histórias filosóficas (fil_*): {len(filosofiche)}")
        
        validas = 0
        invalidas = []
        total_paragrafos = 0
        
        for i, historia in enumerate(filosofiche):
            id_hist = historia.get('id', f'N/A_{i}')
            titulo = historia.get('titolo', '')
            
            ok, msg, paragrafos = validar_storia(historia)
            total_paragrafos += paragrafos
            
            if ok:
                validas += 1
                status = "✅"
            else:
                invalidas.append((id_hist, titulo, msg, paragrafos))
                status = "❌"
            
            # Mostra primeiro e último parágrafo como exemplo
            print(f"\n{status} [{validas}/{len(filosofiche)}] {id_hist}")
            if len(titulo) > 40:
                print(f"    {titulo[:37]}...")
            else:
                print(f"    {titulo}")
            
            # Mostrar exemplo de conteúdo
            para = historia['testo'][0] if historia.get('testo') else {}
            italiano_exemplo = para.get('italiano', '')[:50] + "..."
            print(f"    Exemplo Italiano:  '{italiano_exemplo}'")
            print(f"    {msg}")
        
        # Resumo final
        print("\n" + "=" * 80)
        print("📊 RESUMO FINAL - HISTÓRIAS FILOSÓFICAS")
        print("=" * 80)
        
        print(f"\n✅ Histórias válidas:         {validas}/{len(filosofiche)}")
        print(f"❌ Histórias inválidas:       {len(invalidas)}")
        print(f"📊 Total de parágrafos:       {total_paragrafos}")
        
        if invalidas:
            print(f"\n🔴 DADOS INVÁLIDOS DETECTADOS!")
            for id_hist, titulo, erro, _ in invalidas:
                print(f"\n   ❌ {id_hist}")
                print(f"      Erro: {erro}")
        else:
            print("\n✅ TODAS AS 21 HISTÓRIAS FILOSÓFICAS ESTÃO CORRETAMENTE EXPANDIDAS!")
        
        # Métricas adicionais
        if filosofiche:
            media_palavras = sum(
                len(h.get('testo', [])) 
                for h in filosofiche 
                if h.get('testo')
            ) / len(filosofiche)
            print(f"\n📊 MÉDIAS:")
            print(f"   Parágrafos por história: {media_palavras:.1f}")
            
            total_italiano = sum(
                len(h.get('testo', [{}])) * len(h['testo'][0].get('italiano', '')) 
                for h in filosofiche 
                if h.get('testo') and h['testo'][0].get('italiano')
            )
            print(f"   Caracteres Italiano: {total_italiano:,}")
        
        if validas == len(filosofiche):
            print("\n" + "🎉" * 20)
            print("🎉 ✅ VALIDAÇÃO CONCLUÍDA COM SUCESSO! 🎉" )
            print("🎉" * 20)
            return 0
        else:
            print("\n⚠️ Validação incompleta. Verifique os erros acima.")
            return 1
            
    except json.JSONDecodeError as e:
        print(f"\n❌ ERRO AO LER JSON: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO IMPREVISTO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
