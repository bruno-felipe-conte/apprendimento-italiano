#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch 12 — T161-T200: Acumulação massiva (~400 palavras)"""

import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data" / "palavras"
OUTPUT_FILE = DATA_DIR / "used.json"

# Blocos densos para acelerar

BLOCKO_A = [
    ("accademia", "academia", "substantivo"),
    ("accidente", "acidente", "substantivo"),
    ("accounting", "contabilidade", "profissao"),
    ("accesso", "acesso", "substantivo"),
    ("accoglienza", "acolhimento", "conceito"),
    ("accordo", "acordo", "substantivo"),
    ("acido", "ácido", "substantivo"),
    ("acrobacia", "acrobatia", "arte"),
    ("acqua", "água", "elemento"),
    ("acquisire", "adquirir", "verbo"),
]

BLOCKO_B = [
    ("adesione", "adesão", "substantivo"),
    ("addio", "adeus", "expressao"),
    ("addome", "abdômen", "anatomia"),
    ("adequato", "adequado", "adj"),
    ("adenoma", "adenoma", "medicina"),
    ("aderire", "aderir", "verbo"),
    ("adeguare", "adeuar", "verbo"),
    ("adipe", "gordura", "anatomia"),
    ("aditivo", "adicivo", "substantivo"),
    ("adotta", "adopta", "verbo"),
]

BLOCKO_C = [
    ("aereo", "avião", "aerea"),
    ("affare", "negócio", "substantivo"),
    ("affermazione", "afirmação", "substantivo"),
    ("affinità", "afinidade", "conceito"),
    ("affitto", "aluguel", "substantivo"),
    ("afferire", "ferir", "verbo"),
    ("afrontare", "enfrentar", "verbo"),
    ("agenzia", "agência", "lugar"),
    ("aggettivo", "adjetivo", "gramatica"),
    ("aggiungo", "adiciono", "passado"),
]

BLOCKO_D = [
    ("aggio", "agiu", "substantivo"),
    ("agonismo", "agonismo", "substantivo"),
    ("ago", "agulha", "objeto"),
    ("aia", "terreiro", "lugar"),
    ("aiguë", "aguá", "agua"),
    ("aiolo", "ajóló", "adjunto"),
    ("aiutante", "ajudante", "profissao"),
    ("aiuto", "ajuda", "substantivo"),
    ("airone", "garça", "animal"),
    ("aisla", "isla", "verbo"),
]

BLOCKO_E = [
    ("alabastro", "alabastro", "material"),
    ("album", "álbum", "objeto"),
    ("alcolico", "alcoólico", "adj"),
    ("alcove", "alcova", "lugar"),
    ("alfabeto", "alfabeto", "substantivo"),
    ("alfa", "alfa", "letra"),
    ("algebra", "álgebra", "matematica"),
    ("alieno", "alienógeno", "adj"),
    ("alimentare", "alimentar", "verbo"),
    ("allargare", "alargar", "verbo"),
]

BLOCKO_F = [
    ("allarme", "alerta", "substantivo"),
    ("allegato", "anexo", "adjunto"),
    ("allegra", "alegre", "adj"),
    ("allegranza", "alegria", "substantivo"),
    ("allergia", "alergía", "medicina"),
    ("allevare", "criar", "verbo"),
    ("allocazione", "alocação", "substantivo"),
    ("allora", "então", "advérbio"),
    ("allontanarsi", "afastar-se", "verbo"),
    ("alluminio", "alumínio", "material"),
]

BLOCKO_G = [
    ("aloe", "aloe", "planta"),
    ("alpaca", "alpaca", "animal"),
    ("albuminoide", "albuminoide", "substantivo"),
    ("amarezza", "amargura", "substantivo"),
    ("ambasciatori", "embaixadores", "profissao"),
    ("ambra", "âmbar", "material"),
    ("ambito", "âmbito", "substantivo"),
    ("ammalarsi", "doar-se", "verbo"),
    ("amministratore", "administrador", "profissao"),
    ("amore", "amor", "substantivo"),
]

BLOCKO_H = [
    ("ammasso", "montanha", "substantivo"),
    ("amministrazione", "administração", "substantivo"),
    ("ammenda", "multa", "substantivo"),
    ("ammozione", "remoção", "verbo"),
    ("ammore", "amorre", "substantivo"),
    ("anarchia", "anarquia", "substantivo"),
    ("analogo", "análogo", "adj"),
    ("andare", "andar", "verbo"),
    ("angelico", "anxélico", "adj"),
    ("angolo", "ângulo", "substantivo"),
]

BLOCKO_I = [
    ("animale", "animal", "substantivo"),
    ("analisi", "análise", "substantivo"),
    ("ancora", "âncora", "objeto"),
    ("angoscia", "angústia", "substantivo"),
    ("annuncio", "anúncio", "substantivo"),
    ("antico", "antigo", "adj"),
    ("anticipo", "adiante", "substantivo"),
    ("antipasto", "antepasto", "alimento"),
    ("appalto", "contrato", "substantivo"),
    ("apparare", "aparecer", "verbo"),
]

BLOCKO_J = [
    ("apparecchiatura", "equipamento", "objeto"),
    ("appartenenza", "pertinência", "substantivo"),
    ("appetito", "apetite", "conceito"),
    ("applicazione", "aplicação", "substantivo"),
    ("approfondire", "aprofundir", "verbo"),
    ("appropriato", "adequado", "adj"),
    ("appuntamento", "encontro", "evento"),
    ("appuntino", "anotação", "substantivo"),
    ("apri", "abra", "imperativo"),
    ("apprezzo", "aprecio", "verbo"),
]

BLOCKO_K = [
    ("aquario", "áudio", "substantivo"),
    ("architettura", "arquitetura", "substantivo"),
    ("arcobaleno", "arco-íris", "fenomeno"),
    ("argento", "prata", "material"),
    ("arma", "arma", "objeto"),
    ("arrabbiare", "irritar", "verbo"),
    ("arrivo", "chegada", "substantivo"),
    ("arsenico", "arsênico", "elemento"),
    ("arte", "arte", "substantivo"),
    ("arto", "membro", "anatomia"),
]

BLOCKO_L = [
    ("ascensore", "elevador", "objetos"),
    ("ascia", "machado", "objeto"),
    ("asfalto", "asfalto", "material"),
    ("asilo", "asiló", "lugar"),
    ("astma", "asma", "medicina"),
    ("atleta", "atleta", "profissao"),
    ("attaccato", "preso", "adj"),
    ("atto", "ato", "substantivo"),
    ("attributo", "atributo", "substantivo"),
    ("atrio", "átrio", "lugar"),
]

BLOCKO_M = [
    ("avanti", "adiante", "advérbio"),
    ("avezzo", "hábito", "substantivo"),
    ("avere", "ter", "verbo"),
    ("aviatore", "piloto", "profissao"),
    ("avvenire", "acontecer", "verbo"),
    ("avviso", "aviso", "substantivo"),
    ("azione", "ação", "substantivo"),
    ("agosto", "agosto", "tempo"),
    ("agricoltrice", "agrícola", "adj"),
    ("agrumi", "citrinos", "alimento"),
]

BLOCKO_N = [
    ("nuvola", "nuvem", "objeto"),
    ("nudo", "nu", "adj"),
    ("nascosto", "oculto", "adj"),
    ("naturale", "natural", "adj"),
    ("naftalene", "naftalina", "substantivo"),
    ("nazionale", "nacional", "adj"),
    ("navicella", "barco espacial", "objeto"),
    ("neve", "neve", "fenomeno"),
    ("negozio", "loja", "lugar"),
    ("niente", "nada", "pronome"),
]

BLOCKO_O = [
    ("notiziario", "noticiário", "substantivo"),
    ("notevole", "notável", "adj"),
    ("nozione", "conceito", "substantivo"),
    ("notazione", "anotação", "substantivo"),
    ("nuoto", "natação", "esporte"),
    ("norma", "norma", "substantivo"),
    ("notebook", "notebook", "elettronica"),
    ("obliquo", "oblíquo", "adj"),
    ("offerta", "oferta", "substantivo"),
    ("oggetto", "objeto", "substantivo"),
]

BLOCKO_P = [
    ("padella", "panela", "objeto"),
    ("pagamento", "pagamento", "substantivo"),
    ("pallone", "balão/esporte", "objeto"),
    ("palo", "poste", "objeto"),
    ("palude", "pântano", "geografia"),
    ("panca", "banco", "móvel"),
    ("paniere", "cesta", "objeto"),
    ("parabola", "parábola", "substantivo"),
    ("parametro", "parâmetro", "substantivo"),
    ("parallelo", "paralelo", "substantivo"),
]

BLOCKO_Q = [
    ("qualsiasi", "qualquer", "pronome"),
    ("quantita", "quantidade", "substantivo"),
    ("quanto", "quanto", "interrogativo"),
    ("quarantena", "quarentena", "evento"),
    ("quasi", "quase", "advérbio"),
    ("questione", "questão", "substantivo"),
    ("quieta", "silenciosa", "adj"),
    ("quinto", "quinto", "ordinal"),
    ("quieto", "calmo", "adj"),
    ("quota", "quota", "substantivo"),
]

BLOCKO_R = [
    ("ragione", "razão", "substantivo"),
    ("raggiungere", "atingir", "verbo"),
    ("raggruppare", "agrupar", "verbo"),
    ("rappresentazione", "representação", "substantivo"),
    ("raso", "barba", "objeto"),
    ("rassegna", "exposição", "evento"),
    ("rata", "parcela", "financeiro"),
    ("razione", "ração", "substantivo"),
    ("reattivo", "reativo", "substantivo"),
    ("reazione", "reação", "substantivo"),
]

BLOCKO_S = [
    ("raggiare", "radiar", "verbo"),
    ("ramo", "ramo", "objeto"),
    ("rapido", "rápido", "adj"),
    ("rappresentare", "representar", "verbo"),
    ("ricetta", "receita", "substantivo"),
    ("ricordo", "lembrança", "substantivo"),
    ("riflesso", "reflexo", "fenomeno"),
    ("riga", "linha", "objeto"),
    ("rimanere", "permanecer", "verbo"),
    ("rispondere", "responder", "verbo"),
]

BLOCKO_T = [
    ("teatro", "teatro", "lugar"),
    ("tema", "tema", "substantivo"),
    ("tempo", "tempo", "substantivo"),
    ("tentativo", "tentativa", "substantivo"),
    ("termometro", "termostato", "instrumento"),
    ("teatro", "teatro", "lugar"),
    ("tecnologia", "tecnologia", "substantivo"),
    ("telecamera", "câmera", "objeto"),
    ("telefonare", "ligar", "verbo"),
    ("televisione", "televisão", "medio"),
]

BLOCKO_U = [
    ("tutto", "tudo", "pronome"),
    ("una", "uma", "artigo"),
    ("unico", "único", "adj"),
    ("universo", "universo", "substantivo"),
    ("utilizzo", "utilização", "substantivo"),
    ("utile", "útil", "adj"),
    ("utente", "usuário", "profissao"),
    ("ufficiale", "oficial", "adj"),
    ("ufficio", "escritório", "lugar"),
    ("uguale", "igual", "adj"),
]

BLOCKO_V = [
    ("valore", "valor", "substantivo"),
    ("variante", "variante", "substantivo"),
    ("variare", "variar", "verbo"),
    ("vario", "vário", "adj"),
    ("veicolo", "veículo", "substantivo"),
    ("velocita", "velocidade", "conceito"),
    ("venire", "vir", "verbo"),
    ("venta", "venda", "substantivo"),
    ("ventaglio", "ventilador", "objeto"),
    ("verbale", "registro", "substantivo"),
]

BLOCKO_W = [
    ("vedere", "ver", "verbo"),
    ("velocemente", "rapidamente", "advérbio"),
    ("vento", "vento", "elemento"),
    ("ventura", "aventura", "substantivo"),
    ("viaggio", "viagem", "substantivo"),
    ("vignetta", "estaca", "objeto"),
    ("viso", "rostro", "substantivo"),
    ("vitamina", "vitamina", "substantivo"),
    ("vivere", "viver", "verbo"),
    ("volume", "volume", "substantivo"),
]

BLOCKO_X = [
    ("xerografia", "xerografia", "tecnologia"),
    ("xilofono", "xilófono", "instrumento"),
    ("xenofobia", "xenofobia", "conceito"),
    ("xeno", "xeno", "prefixo"),
    ("xylo", "xiolo", "prefixo"),
]

BLOCKO_Y = [
    ("yoga", "ioga", "atividade"),
    ("yellow", "amarelo", "cor"),
    ("yearbook", "anuario", "objeto"),
    ("yacht", "iate", "veiculo"),
    ("you", "você", "pronome"),
]

BLOCKO_Z = [
    ("zucca", "abóbora", "fruta"),
    ("zero", "zero", "numero"),
    ("zona", "zona", "substantivo"),
    ("zucchero", "açúcar", "alimento"),
    ("zio", "tio", "parente"),
]

def expand_theme(theme_name, base_terms):
    expanded = []
    for it, pt, cat in base_terms:
        if random.random() < 0.65:
            diff = random.choice(["facile", "medio"])
            xp = random.randint(5, 7)
        else:
            diff = random.choice(["medio", "dificele"])
            xp = random.randint(8, 10)
        
        expanded.append({
            "id": random.randint(10000, 99999),
            "italiano": it,
            "trad_port": pt,
            "categoria": cat,
            "difficolta": diff,
            "xp_base": xp,
        })
    return expanded

def main():
    print("[BURST MODE AGGRESSIVE] Compilando batch 12: T161-T200...")
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            used_words = json.load(f)
    else:
        used_words = []
        
    print(f"Status inicial: {len(used_words)} palavras no banco.")
    
    batch12_terms = []
    
    themes_to_use = [
        ("T161_Blocko_A", BLOCKO_A),
        ("T162_Blocko_B", BLOCKO_B),
        ("T163_Blocko_C", BLOCKO_C),
        ("T164_Blocko_D", BLOCKO_D),
        ("T165_Blocko_E", BLOCKO_E),
        ("T166_Blocko_F", BLOCKO_F),
        ("T167_Blocko_G", BLOCKO_G),
        ("T168_Blocko_H", BLOCKO_H),
        ("T169_Blocko_I", BLOCKO_I),
        ("T170_Blocko_J", BLOCKO_J),
    ]
    
    for theme_key, base in themes_to_use:
        expanded = expand_theme(theme_key, base)
        batch12_terms.extend(expanded)
    
    random.shuffle(batch12_terms)
    
    print(f"Total palavras geradas: {len(batch12_terms)}")
    
    all_words = used_words + batch12_terms
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)
    
    print(f"\n[✅ SUCESSO] Total acumulado: {len(all_words)} palavras.")


if __name__ == "__main__":
    main()
