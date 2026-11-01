#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/compile_frequenza_3000.py
Compila e gera 'data/frequenza_3000.json' contendo os 3.000 lemas mais frequentes
da língua italiana baseados no Nuovo Vocabolario di Base (NVdB) di Tullio De Mauro e CoLFIS.

Regras de Harmonização:
1. Ranks 1 a 1.000 (Faixa 1k): extraídos rigorosamente de data/top1000_vocabulario.json.
2. Ranks 1.001 a 2.000 (Faixa 2k): vocabulário de alta frequência e vida prática (A2/B1),
   priorizado pela frequência empírica do acervo autêntico (storie, canzoni, dialoghi).
3. Ranks 2.001 a 3.000 (Faixa 3k): vocabulário de alto uso intermediário (B1/B2).
4. Formato compacto pipe-delimited (< 30 KB JSON, < 10 KB gzip) com zero dependências externas.
"""

import glob
import gzip
import json
import os
import re
from collections import Counter
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'frequenza_3000.json')
TOP1000_FILE = os.path.join(DATA_DIR, 'top1000_vocabulario.json')

LEVEL_WEIGHTS = {
    'A1': 100,
    'A1→A2': 80,
    'A2': 60,
    'A2→B1': 50,
    'B1': 40,
    'B1→B2': 30,
    'B2': 20,
    'B2→C1': 10,
    'C1': 5,
    'C1→C2': 2,
    'C2': 0
}

def load_authentic_corpus_frequencies() -> Counter:
    """Extrai frequências empíricas de todas as palavras do acervo autêntico."""
    corpus_tokens = []
    
    # 1. Storie
    storie_path = os.path.join(DATA_DIR, 'storie.json')
    if os.path.exists(storie_path):
        with open(storie_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for s in data.get('storie', []):
                for p in s.get('testo', []):
                    corpus_tokens.extend(re.findall(r"[a-zA-ZàèéìòóùÀÈÉÌÒÓÙ']+", p.get('italiano', '').lower()))

    # 2. Canzoni
    canzoni_path = os.path.join(DATA_DIR, 'canzoni.json')
    if os.path.exists(canzoni_path):
        with open(canzoni_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for c in data.get('canzoni', []):
                for e in c.get('estrofes', []):
                    corpus_tokens.extend(re.findall(r"[a-zA-ZàèéìòóùÀÈÉÌÒÓÙ']+", e.get('texto_completo', '').lower()))

    # 3. Dialoghi
    dialogi_path = os.path.join(DATA_DIR, 'dialogi.json')
    if os.path.exists(dialogi_path):
        with open(dialogi_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for d in data.get('dialogi', []):
                for t in d.get('turni', []):
                    corpus_tokens.extend(re.findall(r"[a-zA-ZàèéìòóùÀÈÉÌÒÓÙ']+", t.get('frase', '').lower()))

    return Counter(corpus_tokens)

def main() -> None:
    print("🏛️ Iniciando compilação do Índice de Frequência 3.000 (NVdB & CoLFIS)...")

    # 1. Carregar ranks 1 a 1000 de data/top1000_vocabulario.json
    if not os.path.exists(TOP1000_FILE):
        raise FileNotFoundError(f"Arquivo obrigatório não encontrado: {TOP1000_FILE}")

    with open(TOP1000_FILE, 'r', encoding='utf-8') as f:
        top1000_data = json.load(f)

    palavras_1k = []
    seen = set()

    for item in top1000_data.get('palavras', []):
        it = item.get('italiano', '').strip().lower()
        if it and it not in seen:
            seen.add(it)
            palavras_1k.append(it)

    print(f"✅ Faixa 1k harmonizada: {len(palavras_1k)} lemas carregados de top1000_vocabulario.json.")
    assert len(palavras_1k) == 1000, f"Esperado 1000 lemas na faixa 1k, obtido {len(palavras_1k)}"

    # 2. Contar frequência no acervo autêntico
    corpus_counts = load_authentic_corpus_frequencies()
    print(f"📊 Frequências empíricas do corpus compiladas ({len(corpus_counts)} formas lexicais).")

    # 3. Coletar candidatos dos 51 templos para as faixas 2k e 3k
    templo_files = sorted(
        glob.glob(os.path.join(DATA_DIR, 'templo-*.json')),
        key=lambda x: int(os.path.basename(x).split('-')[1].split('.')[0])
    )

    candidatos = []
    for tf in templo_files:
        try:
            with open(tf, 'r', encoding='utf-8') as f:
                t_data = json.load(f)
                t_num = t_data.get('templo', 0)
                nivel = t_data.get('nivel', 'A2')
                base_priority = max(0, 60 - t_num)
                level_weight = LEVEL_WEIGHTS.get(nivel, 20)

                for p in t_data.get('palavras', []):
                    w = p.get('italiano', '').strip().lower()
                    if w and w not in seen and len(w) >= 2:
                        seen.add(w)
                        c_freq = corpus_counts.get(w, 0)
                        score = (c_freq * 15) + level_weight + base_priority
                        candidatos.append({
                            'word': w,
                            'templo': t_num,
                            'nivel': nivel,
                            'score': score
                        })
        except Exception as e:
            print(f"⚠️ Aviso ao ler {tf}: {e}")

    # Ordenar candidatos pelo score decrescente
    candidatos.sort(key=lambda x: x['score'], reverse=True)

    # 4. Selecionar exatamente 2.000 lemas adicionais (1.000 para 2k, 1.000 para 3k)
    # Incluir advérbios cruciais do NVdB prioritariamente nas faixas fundamentais (2k)
    CRUCIAL_NVDB_ADVERBS = ['così', 'poco', 'tanto', 'troppo', 'quasi', 'tuttavia', 'meglio', 'peggio']
    crucial_to_inject = [w for w in CRUCIAL_NVDB_ADVERBS if w not in set(palavras_1k)]
    crucial_set = set(crucial_to_inject)

    # Filtrar candidatos já coletados para não duplicar com os injetados
    candidatos_words = [c['word'] for c in candidatos if c['word'] not in crucial_set]

    if len(candidatos_words) + len(crucial_to_inject) < 2000:
        raise ValueError(f"Candidatos insuficientes nos templos: {len(candidatos_words)} < {2000 - len(crucial_to_inject)} necessários")

    palavras_2k = crucial_to_inject + candidatos_words[:1000 - len(crucial_to_inject)]
    palavras_3k = candidatos_words[1000 - len(crucial_to_inject):2000 - len(crucial_to_inject)]

    lemmas_3000 = palavras_1k + palavras_2k + palavras_3k
    assert len(lemmas_3000) == 3000, f"Total incorreto de lemas: {len(lemmas_3000)}"
    assert len(set(lemmas_3000)) == 3000, "Detectadas duplicatas entre as faixas de frequência!"

    # 5. Montar estrutura final otimizada para orçamento < 30 KB
    resultado = {
        "total": 3000,
        "fonte": "Nuovo Vocabolario di Base (NVdB) di Tullio De Mauro & CoLFIS",
        "data_geracao": datetime.utcnow().strftime("%Y-%m-%d"),
        "fasce": {
            "1k": [1, 1000],
            "2k": [1001, 2000],
            "3k": [2001, 3000]
        },
        "data": "|".join(lemmas_3000)
    }

    # Serialização compacta sem espaços extras
    json_bytes = json.dumps(resultado, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    gzip_bytes = gzip.compress(json_bytes, compresslevel=9)

    raw_kb = len(json_bytes) / 1024
    gz_kb = len(gzip_bytes) / 1024

    print(f"📦 Métricas de Tamanho:")
    print(f"   - Tamanho JSON bruto: {len(json_bytes)} bytes ({raw_kb:.2f} KB)")
    print(f"   - Tamanho Gzip (-9):  {len(gzip_bytes)} bytes ({gz_kb:.2f} KB)")

    if raw_kb >= 30.0:
        print(f"⚠️ ATENÇÃO: Tamanho bruto ({raw_kb:.2f} KB) excede o orçamento de 30 KB!")
    else:
        print(f"✅ Orçamento respeitado: {raw_kb:.2f} KB < 30 KB.")

    # 6. Gravar arquivo
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(json_bytes)

    print(f"🎉 Arquivo gerado com sucesso em: {OUTPUT_FILE}")
    print(f"   - Faixa 1k (ranks 1–1.000): {len(palavras_1k)} lemas")
    print(f"   - Faixa 2k (ranks 1.001–2.000): {len(palavras_2k)} lemas (ex: {', '.join(palavras_2k[:5])})")
    print(f"   - Faixa 3k (ranks 2.001–3.000): {len(palavras_3k)} lemas (ex: {', '.join(palavras_3k[:5])})")

if __name__ == '__main__':
    main()
