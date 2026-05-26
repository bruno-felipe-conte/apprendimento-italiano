#!/usr/bin/env python3
"""Auto-generate 2000+ quiz questions from temple vocabulary data."""
import json, random
DATA = "C:/Users/bruno/Documents/italian-learning-app-pro/data"

random.seed(42)

with open(f"{DATA}/quizzes.json", encoding='utf-8') as f:
    quiz = json.load(f)

existing_ids = {q['id'] for q in quiz['perguntas']}
new_qs = []

templates = {
    'ita_to_por': "O que significa '{ita}' em português?",
    'por_to_ita': "Como se diz '{por}' em italiano?",
    'complete': "Complete: '{sentence}'",
}

for t in range(1, 11):
    with open(f"{DATA}/templo-{t}.json", encoding='utf-8') as f:
        data = json.load(f)
    
    words = data['palavras']
    random.shuffle(words)
    
    # Take up to 200 words per temple
    for i, w in enumerate(words[:200]):
        if i % 3 == 0:
            # Italian -> Portuguese
            q = templates['ita_to_por'].format(ita=w['italiano'])
            correta = w['portugues']
            # Get distractors from other words in same temple
            others = [o['portugues'] for o in words if o['id'] != w['id'] and o.get('categoria') == w.get('categoria')]
            if len(others) < 3:
                others = [o['portugues'] for o in words if o['id'] != w['id']]
            random.shuffle(others)
            alternativas = others[:3]
            if correta not in alternativas:
                alternativas = alternativas[:3] + [correta]
            random.shuffle(alternativas)
            nivel = data['nivel']
            tipo = 'vocabulario'
            qid = f"qgen_{t}_{i+1:03d}"
            if qid not in existing_ids:
                new_qs.append({
                    "id": qid, "templo": t, "tipo": tipo, "nivel": nivel,
                    "pergunta": q, "resposta_correta": correta,
                    "alternativas": alternativas[:4],
                    "explicacao": f"{w['italiano']} significa '{correta}' em português.",
                    "xp_recompensa": min(w.get('dificuldade',1)*10 + 10, 30)
                })
                existing_ids.add(qid)
        
        if i % 3 == 1:
            # Portuguese -> Italian
            q = templates['por_to_ita'].format(por=w['portugues'])
            correta = w['italiano']
            others = [o['italiano'] for o in words if o['id'] != w['id']]
            random.shuffle(others)
            alternativas = others[:3] + [correta]
            random.shuffle(alternativas)
            qid = f"qgen_{t}_{i+1:03d}b"
            if qid not in existing_ids:
                new_qs.append({
                    "id": qid, "templo": t, "tipo": 'vocabulario', "nivel": data['nivel'],
                    "pergunta": q, "resposta_correta": correta,
                    "alternativas": alternativas[:4],
                    "explicacao": f"{w['portugues']} em italiano é '{correta}'.",
                    "xp_recompensa": min(w.get('dificuldade',1)*10 + 10, 30)
                })
                existing_ids.add(qid)

print(f"Generated {len(new_qs)} new quiz questions")
quiz['perguntas'] = quiz['perguntas'] + new_qs
quiz['total_perguntas'] = len(quiz['perguntas'])
with open(f"{DATA}/quizzes.json", 'w', encoding='utf-8') as f:
    json.dump(quiz, f, ensure_ascii=False, indent=2)
print(f"Total: {quiz['total_perguntas']} questions")

# Per-temple count
from collections import Counter
tc = Counter(q['templo'] for q in quiz['perguntas'])
for t in sorted(tc):
    print(f"  Temple {t}: {tc[t]} questions")
