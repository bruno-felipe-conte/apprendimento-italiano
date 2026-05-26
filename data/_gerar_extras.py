import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")

def gerar_extras(num_lezione, tema):
    """Gera 30 exercícios de qualidade para uma lezione específica"""
    
    n = num_lezione.strip().lower()
    
    if n.startswith("lez"):
        n = n.replace("lez", "")
    
    templates = []
    
    # Revelar (45-55 porcents) — completar/transformar
    revelar_count = 0
    
    if tema.__contains__('artic') or 'articolo' in tema:
        revelar_count += 5
        templates.extend([
            ("**Esercizio {n}** — Articolo determinativo (concordia genere/número):\n{perg}", "Completa"),
            ("**Esercizio {n}** — Articolo indeterminativo:\n{perg}", "Completa"),
            ("**Esercizio {n}** — Plurale di: {nome}", "Pluralizza"),
        ])
    
    elif tema.__contains__('verbo') or 'verb' in tema or 'presente' in tema:
        revelar_count += 6
        templates.extend([
            ("**Esercizio {n}** — Presente di {v_base}, coniugazione -{fiss}:\n{perg}", "Coniuga"),
            ("**Esercizio {n}** — Verbo irregolare: {v_irreg}\n{perg}", "Completa irregolare"),
        ])
    
    elif tema.__contains__('preposizione') or 'prepos' in tema:
        revelar_count += 5
        templates.extend([
            ("**Esercizio {n}** — Preposizione semplice e articolata:\n{perg}", "Completa"),
        ])
    
    elif tema.__contains__('passat') or 'prossimo' in tema:
        revelar_count += 6
        templates.extend([
            ("**Esercizio {n}** — Passato prossimo (avere/essere + participio):\n{perg}", "Completa"),
        ])
    
    elif tema.__contains__('futur') or 'futuro' in tema:
        revelar_count += 5
        templates.extend([
            ("**Esercizio {n}** — Futuro semplice di {v_base}:\n{perg}", "Completa"),
        ])
    
    elif tema.__contains__('imperf') or 'imperfet' in tema:
        revelar_count += 6
        templates.extend([
            ("**Esercizio {n}** — Imperfetto indicativo di {v_base}:\n{perg}", "Coniuga"),
        ])
    
    else:
        # Fallback generico per altre lezione (X-XXX)
        revelar_count += 5
        templates.extend([
            ("**Esercizio {n}** — Completare frase in italiano:\n{perg}", "Completa"),
            ("**Esercizio {n}** — Identificare verbo irregolare:\n{perg}", "Identifica"),
        ])
    
    # Generare 45-55 es. "revelar"
    num_revelar = max(18, min(26, len(templates) * 3 + random.randint(10, 15))) if random.random() > 0.3 else 20
    
    for i in range(num_revelar):
        n = i + 1
        
        # Escolher template relevante
        if revelar_count > 0 and i < len(templates) * 2:
            tmpl, _ = templates[i % len(templates)]
        else:
            tmpl = "**Esercizio {n}** — Completare frase:\n{perg}"
        
        perg, resp = "", ""
        
        if tema.__contains__('artic'):
            perg = f"L'articolo corretto per **libro** è ______."
            resp = "il"
        elif tema.__contains__('plur') or 'plural' in tema:
            perg = f"Il plurale di **gatto** è ______."
            resp = "i gatti"
        elif tema.__contains__('passat'):
            perg = f"Ho _____ una torta ieri sera. (mangiare)"
            resp = "mangiato"
        elif tema.__contains__('futur') or 'futuro' in tema:
            perg = f"Domenica _____ al cinema. (andare)"
            resp = "andrò"
        elif tema.__contains__('imperf'):
            perg = f"Ieri mentre pioveva, io _____ la TV. (guardare)"
            resp = "guardavo"
        else:
            perg = f"Ieri _____ la pizza al ristorante. (mangiare)"
            resp = "ho mangiato"
        
        templates_revelar = [
            tmpl.format(n=n, perg=perg),
            ("**Esercizio {n}** — Frasi con verbo irregolare:\n{perg}", ""),
            ("**Esercizio {n}** — Preposizione corretta:\n{perg}", ""),
        ]
        
        ex = {
            "tipo": "revelar",
            "pergunta": random.choice(templates_revelar)[0].format(n=n, perg=perg),
            "resposta": resp,
            "explicacao": f"Re: Passato prossimo di **mangiare** → **ho mangiato**. Futuro: **andrò**. Imperfetto: **guardavo**."
        }
        
        if revelar_count > 0 and i < len(templates):
            ex["explicacao"] = templates[i % len(templates)][1].format(n=n, perg=perg.replace(f"{n}.", "").strip()).capitalize()
        
        novos.append(ex)
    
    # Escolha (30-42) — esercizi di verifica con opzioni
    num_escolha = 30 - num_revelar
    if num_escolha < 15: num_escolha = max(15, num_escolha)
    
    escolha_count = 0
    escolha_templates = [
        ("Qual è l'articolo corretto per **{nome}**?\n", ["il {n.lower()}", "lo {n.lower()}" if nome[-1] in 'aeiouy' else None, f"l'{n.lower()}" if nome[-1] in 'aeiouy' else None],
         ["Maschile, consonante semplice → **il**.", "Vocale → **l'**."]),
        ("Completa: Il plurale di {nome} è ______.\n", ["{n}i", "{n.e}" if nome[-1] == 'a' else f"{n}", None],
         [f"Maschile: **-i** ({n}). Femminile: **-e**.", "Mantiene suono consonante /g/ → **-ghi**."]),
        ("Scegli la forma corretta di {v_base}:\n", ["{v_base}o", f"{v_base}ere" if v_base[-1] in 'er' else None, f"{v_base}ire" if v_base[-1] in 'ir' else None],
         ["Prima persona singolare: **-o**.", "Terza coniugazione → **-e/-i**."]),
        ("Completa con preposizione articolata:\n{prep_base} + {loc} = ______\n", ["del", "dello", "della", "dei", "degli", None],
         ["di + il = **del**.", "di + lo = **dello**.", "di + la = **della**."]),
    ]
    
    for i in range(num_escolha):
        n = i + 1
        
        tmpl_base, opcoes_base, explicacoes = random.choice(escolha_templates)
        perg_base = tmpl_base.format(nome=random.choice(["libro", "gatto", "amica", "pneumatico"]), 
                                       v_base=random.choice(["mangiare", "scrivere", "dormire"]),
                                       prep_base="di", loc="il")
        
        opcoes = [o.format(n=n, n=e if e == "{n}" else e.lower(), e=c.replace("i", "e")) for c, o in zip(escolha_templates, opcoes_base) if o and (c[0] == nome or random.random() > 0.5)][0:2]
        if not opcoes: 
            opcoes = ["Il libro", "Lo zaino", f"L'{nome.lower()}"]
        
        resp_idx = min(random.randint(0, len(opcoes)-1), 2)
        explicacao = random.choice(escolha_templates[2])[resp_idx].format(n=n, nome=perg_base.replace("Qualèl'articolo", "Il"), v_base="", prep_base="", loc="") or f"Spiegazione grammaticale pertinente al tema della lezione {n}."
        
        ex = {
            "tipo": "escolha",
            "pergunta": perg_base,
            "opcoes": opcoes[0:3],
            "resposta": resp_idx,
            "explicacao": f"Re: **{perg_base.split(chr(10)[0].split(chr(97)[-1] if 'a' in opcoes[resp_idx][-2:] else '')}** — {escolha_templates[2][resp_idx]}." if explicacoes else explicacao
        }
        
        novos.append(ex)
    
    return novos

# Executar para TODAS as lezione (I-XXX)
novos_por_lezione = {}

for u in modulo['unidades']:
    num = u['num']
    tema = u.get('titulo', f'{num} - Gramática').lower()
    
    # Filtrar temas com conteúdo gramatical relevante
    if any(t in tema for t in ['articolo', 'verbo', 'presente', 'imperfetto', 'passato', 'futuro', 
                               'prepos', 'possess', 'pronome', 'artico', 'plur']) or num.isdigit():
        novos = gerar_extras(num, tema)
        novos_por_lezione[num] = novos

# Inserir nos exercícios correspondentes
for num, novos in novos_por_lezione.items():
    u = next((u for u in modulo['unidades'] if u['num'] == num), None)
    if not u:
        continue
    
    exercicios = u['exercicios']
    
    # Encontrar índice do primeiro "escolha"
    idx_escolha = next((i for i, e in enumerate(exercicios) if e.get('tipo') == 'escolha'), len(exercicios))
    idx_insert = idx_escolha
    
    # Inserir separador + novos exercícios antes dos escolha existentes
    exercicios.insert(idx_insert, {"tipo": "separatore", "pergunta": f"\n--- **EXERCÍCIOS EXTRAS — {num}** ---\n", 
                                  "resposta": "", "explicacao": ""})
    
    for i, ex in enumerate(novos):
        exercicios.insert(idx_insert + i + 1, ex)

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Relatório final
print(f"\n{'='*60}")
print("✅ NOVA INSERÇÃO COMPLETADA — TODAS AS LEZIONE")
print('='*60 + "\n")

for u in modulo['unidades']:
    total = len(u['exercicios'])
    es = sum(1 for e in u['exercicios'] if e.get('tipo') == 'escolha')
    re = sum(1 for e in u['exercicios'] if e.get('tipo') == 'revelar')
    print(f"{u['num']}: {total} total (escolha: {es}, revelar: {re})")

print(f"\n{'='*60}")
print("📊 RESUMO FINAL:")
total_ex = sum(len(u['exercicios']) for u in modulo['unidades'])
total_es = sum(sum(1 for e in u['exercicios'] if e.get('tipo') == 'escolha') for u in modulo['unidades'])
total_re = sum(sum(1 for e in u['exercicios'] if e.get('tipo') == 'revelar') for u in modulo['unidades'])
print(f"   Total exercícios: {total_ex}")
print(f"   • Escolha: {total_es} ({total_es/total_ex*100:.0f}%)")
print(f"   • Revelar: {total_re} ({total_re/total_ex*100:.0f}%)")
print('='*60 + "\n")
