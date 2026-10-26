#!/usr/bin/env python3
"""
scripts/compile_top500_flashcards.py
Compila e gera 'data/top500_flashcards.json' com exatamente 500 cartas
distribuídas em 5 baralhos temáticos de 100 cartas cada.
"""

import json
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.deck2_falsi_amici import get_deck_falsi_amici
from scripts.deck3_preposizioni import get_deck_preposizioni
from scripts.deck4_verbi_irregolari import get_deck_verbi_irregolari
from scripts.deck5_situazioni_reali import get_deck_situazioni_reali
from scripts.generate_top500_cards import gerar_deck_colocacoes

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(ROOT_DIR, 'data', 'top500_flashcards.json')

def main() -> None:
    print("Compilando os 5 baralhos temáticos do Top 500 Flashcards...")
    
    d1 = gerar_deck_colocacoes()[:100]
    d2 = get_deck_falsi_amici()[:100]
    d3 = get_deck_preposizioni()[:100]
    d4 = get_deck_verbi_irregolari()[:100]
    d5 = get_deck_situazioni_reali()[:100]

    decks_info = {
        "colocacoes": {
            "id": "colocacoes",
            "nome": "Colocações & Chunks",
            "icone": "🧩",
            "total": len(d1),
            "descricao": "Expressões idiomáticas, chunks do dia a dia e colocações naturais essenciais"
        },
        "falsi_amici": {
            "id": "falsi_amici",
            "nome": "Falsos Amigos (Falsi Amici)",
            "icone": "⚠️",
            "total": len(d2),
            "descricao": "Palavras que parecem português mas possuem significado completamente diferente"
        },
        "preposizioni": {
            "id": "preposizioni",
            "nome": "Preposições & Regências",
            "icone": "📍",
            "total": len(d3),
            "descricao": "Articulações, regências verbais obrigatórias e uso correto de a, in, da, di, su, per"
        },
        "verbi_irregolari": {
            "id": "verbi_irregolari",
            "nome": "Verbos Irregulares em Contexto",
            "icone": "⚡",
            "total": len(d4),
            "descricao": "Presente irregular, particípios passados e escolha correta entre essere e avere"
        },
        "situazioni_reali": {
            "id": "situazioni_reali",
            "nome": "Situações da Vida Real (Cloze)",
            "icone": "🎭",
            "total": len(d5),
            "descricao": "Desafios comunicativos práticos em bares, restaurantes, aeroportos, farmácias e compras"
        }
    }

    all_cards = []
    all_cards.extend(d1)
    all_cards.extend(d2)
    all_cards.extend(d3)
    all_cards.extend(d4)
    all_cards.extend(d5)

    data = {
        "total": len(all_cards),
        "decks": decks_info,
        "cards": all_cards
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Arquivo gerado com sucesso: {OUTPUT_FILE}")
    print(f"📊 Total de cartas: {len(all_cards)}")
    for v in decks_info.values():
        print(f"   - {v['icone']} {v['nome']}: {v['total']} cartas")

if __name__ == '__main__':
    main()
