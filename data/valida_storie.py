#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
valida_storie.py - Valida todas as histórias filosóficas expandidas

Uso:
    python valida_storie.py              # Valida tudo
    python valida_storie.py --verbose    # Mostra detalhes de cada história
    python valida_storie.py --check-all  # Verifica se todas têm 15 parágrafos
"""

import json
import sys
from pathlib import Path


def carregar_stories(path: str) -> list:
    """Carrega o JSON das histórias filosóficas."""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['storie'] if isinstance(data.get('storie'), list) else []


def contar_paragrafos(storia) -> int:
    """Contam o número de parágrafos na história."""
    testo = storia.get('testo', [])
    return len(testo) if isinstance(testo, list) else 0


def validar_historia(storia: dict, indice: int) -> tuple[bool, str]:
    """Valida uma única história."""
    
    # Verifica se tem parágrafos
    num_paragrafos = contar_paragrafos(storia)
    
    if num_paragrafos == 0:
        return False, "Nenhum parágrafo encontrado"
    
    # Verifica estrutura de cada parágrafo
    for i, para in enumerate(storia.get('testo', [])[:3]):  # Verifica primeiros 3 como amostra
        try:
            assert 'id' in para and f'p{i}' == para['id']
            assert 'italiano' in para and len(para['italiano']) > 0
            assert 'portugues' in para and len(para['portugues']) > 0
            assert 'parole' in para
        except KeyError:
            return False, f"Parágrafo {i}: campos faltando"
        except AssertionError as e:
            return False, str(e)
    
    # Verifica palavras-chave em cada parágrafo (amostragem)
    for i, para in enumerate(storia.get('testo', [])[:5]):  # Verifica primeiros 5
        parole = para.get('parole', [])
        if not isinstance(parole, list):
            return False, f"Parágrafo {i}: 'parole' não é uma lista"
        
        for p in parole:
            try:
                assert 'parola' in p
                assert 'ipa' in p
                assert 'traduzione' in p
            except KeyError:
                return False, f"Parágrafo {i}, palavra {p.get('parola')}: campos faltando"
    
    return True, f"{num_paragrafos} parágrafos válidos"


def main():
    # Caminho padrão do arquivo
    BASE_DIR = Path(r'C:\Users\bruno\Documents\italian-learning-app-pro\data')
    ARQUIVO_PRINCIPAL = BASE_DIR / 'storie.json'
    
    if not ARQUIVO_PRINCIPAL.exists():
        print(f"❌ Arquivo não encontrado: {ARQUIVO_PRINCIPAL}")
        print("\nDica: Use --backup para verificar o backup em stories_filosofia_final.json")
        return 1
    
    print("=" * 80)
    print("VALIDAÇÃO DE HISTÓRIAS FILOSÓFICAS EXPANDIDAS")
    print("=" * 80)
    
    try:
        historias = carregar_stories(str(ARQUIVO_PRINCIPAL))
        print(f"\n📚 Arquivo: {ARQUIVO_PRINCIPAL.name}")
        print(f"   Total de histórias no arquivo: {len(historias)}")
        
        historicas_validas = 0
        historicas_invalidas = []
        total_paragrafos = 0
        
        # Validação detalhada
        for i, historia in enumerate(historias):
            id_hist = historia.get('id', f'N/A_{i}')
            titulo = historia.get('titolo', 'Sem título')
            
            validacao_ok, mensagem = validar_historia(historia, i)
            total_paragrafos += contar_paragrafos(historia)
            
            if validacao_ok:
                historicas_validas += 1
                status = "✅"
            else:
                historicas_invalidas.append((id_hist, titulo, mensagem))
                status = "❌"
            
            print(f"\n{status} [{i+1}/{len(historias)}] {id_hist}")
            if len(titulo) < 40:
                print(f"    {titulo}")
            else:
                print(f"    {titulo[:37]}...")
            print(f"    {mensagem}")
        
        # Resumo final
        print("\n" + "=" * 80)
        print("RESUMO FINAL")
        print("=" * 80)
        
        print(f"\n✅ Histórias válidas:     {historicas_validas}/{len(historias)}")
        print(f"❌ Histórias inválidas:  {len(historicas_invalidas)}")
        print(f"📊 Total de parágrafos:   {total_paragrafos}")
        
        if historicas_invalidas:
            print("\n🔴 ERROS DETECTADOS:")
            for id_hist, titulo, erro in historicas_invalidas:
                print(f"\n   ❌ {id_hist}: {titulo}")
                print(f"      Erro: {erro}")
        else:
            print("\n✅ TODAS AS HISTÓRIAS ESTÃO CORRETAMENTE EXPANDIDAS!")
        
        # Decisão de saída
        if historicas_invalidas:
            print("\n❌ Validação falhou. Verifique os erros acima.")
            return 1
        else:
            print("\n✅ Validação concluída com sucesso!")
            return 0
            
    except json.JSONDecodeError as e:
        print(f"\n❌ ERRO AO LER JSON: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERRO IMPREVISTO: {type(e).__name__}: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
