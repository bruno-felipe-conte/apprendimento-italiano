# Instruções: Melhorar Explicações dos Exercícios

## Objetivo
Melhorar as `explicacao` de todos os exercícios do arquivo `grammar.json`, tornando-as mais claras, pedagógicas e alinhadas com o contexto da lezione.

---

## Localização dos Arquivos
- **JSON principal:** `C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json`
- **Python:** `C:\Users\bruno\AppData\Local\Programs\Python\Python311\python.exe`

---

## Análise da Situação Atual (Exemplo)

```json
{
  "tipo": "revelar",
  "pergunta": "**Esercizio** — Completa com o verbo correcto:",
  "resposta": "ha mangiato",
  "explicacao": "Passato prossimo."
}
```

### Problemas Identificados:
- Explicação genérica, sem contexto gramatical específico
- Não menciona a conjugação (mangiare = -ARE)
- Não explica POR QUE é passato prossimo (temporal marker: "ieri")
- Falta exemplo paralelo para reforçar o aprendizado

---

## Diretrizes Gerais de Melhoria

### 1. Clareza e Contexto Gramatical
**ANTES:**
```
"explicacao": "Passato prossimo."
```

**DEPOIS:**
```
"explicacao": "Passato prossimo di mangiare (verbo -ARE): ha mangiato. O auxiliar è avere + participio passato (-ato). 'Ieri' indica tempo passato → passato prossimo obrigatório."
```

### 2. Explicar a REGRA, não apenas o resultado
**ANTES:**
```
"explicacao": "Verbo avere conjugado no presente."
```

**DEPOIS:**
```
"explicacao": "Auxiliar AVERE no passato prossimo (primeira pessoa: io HO). Participio mangiato concorda em género/número com o sujeito SO se verbo de movimento, mas mantém invariável com AVERE."
```

### 3. Mencionar EXCEÇÕES e Casos Especiais
**ANTES:**
```
"explicacao": "Verbo irregolare avere."
```

**DEPOIS:**
```
"explicacao": "AVERE é verbo totalmente irregulare no presente (ho/avrai/ha...). Memorizar como bloco: HO, HAI, HA, ABBIAMO, AVETE, HANO. Participio 'avuto' também irregular."
```

### 4. Usar Terminologia Consistente
- Sempre especificar o **modus/tempo/aspecto**: `presente indicativo`, `passato prossimo`, `imperfetto`, etc.
- Indicar se é **regolare ou irregolare**
- Especificar **persona e número** quando relevante

---

## Tipos de Explicação por Categoria Gramatical

### A) TEMPOS VERBAIS (Passato Prossimo, Imperfetto, Futuro, etc.)

#### Padrão para Passato Prossimo:
```
"explicacao": "Passato prossimo di [VERBO] (categoria): [resposta]. Auxiliar [AVERE/ESSERE]: [conjugacao]. Participio passato [regular/irregolare]: [forma]. Marcador temporal: '[palavra]' indica ação completada no passado."
```

#### Padrão para Imperfetto:
```
"explicacao": "Imperfetto indicativo de [VERBO] (categoria): [resposta]. Forma regular para descrições/abituudes. Sufixo: -avo, -evi, -iva, -evate, -ava, -avano."
```

### B) CONJUGAÇÃO VERBAL (Presente, Futuro, Condicional)

#### Padrão para Presente:
```
"explicacao": "Presente indicativo de [VERBO] (categoria). Conjugação [regular/irregolare]. Terminações: -o, -i, -a, -iamo, -ate, -ano."
```

### C) PARTICIPI PASSATI e VERBOS IRREGULARES

#### Lista de Participios Irregulares Comuns:
| Verbo | Participio Passato | Explicação Padrão |
|-------|-------------------|-------------------|
| essere | stato | "Participio irregular di essere. 'Stato' é invariável." |
| avere | avuto | "Participio irregular di avere. 'Avuto' sempre com AVERE." |
| andare | andato | "Participio irregular di andare. Uso: io sono andato (essere como auxiliar)." |
| fare | fatto | "Participio irregular di fare. Forma invariável." |
| dire | detto | "Participio irregular di dire. Pronúncia: /det.to/." |
| scrivere | scritto | "Participio irregular de verbo -ERE com i e o em lugar de u final." |

### D) ARTIGOS E PLURALIZAÇÃO

#### Padrão para Artigos:
```
"explicacao": "[Artigo] + [substantivo]. Regra: IL davanti a consonante/vocale maschile (non ps/pn); LO davanti a s+cons, z, gn, ps, x, y; LA davanti a vocale femminile; L' davanti a tutte le vocali. Plurale: -o → -i, -a → -e."
```

### E) PREPOSIÇÕES ARTICOLATE

#### Padrão para Preposizioni Articolate:
```
"explicacao": "Preposizione articolata [simples] + [artigo] = [articulada]. Esempio: a + il = al. Uso: indica movimento verso/destino (andare AL mercato)."
```

### F) PRONOMES DIRETTI

#### Padrão:
```
"explicacao": "Pronome diretto [pronome]. Posição antes do verbo no presente (lo vedo). No passato prossimo, o pronome vai ANTECEDER o auxiliar (lo ho visto). Forma átona para objetos diretos."
```

---

## Fluxo de Trabalho para Melhorar Explicações

### Passo 1: Carregar JSON e Identificar Exercícios com Explicações Fracas
```python
import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lezioni = modulo["unite"]

print("=== LEZIONI COM EXERCÍCIOS ===")
for l in lezioni:
    print(f"\n{['num': 'Lezione X']}:")
    for i, ex in enumerate(l["exercicios"]):
        if "explicacao" not in ex or len(ex["explicacao"]) < 30:
            print(f"  [{i}] {ex.get('tipo', 'N/D')} — Explicação curta/ausente:")
            print(f"      '{ex.get('explicacao', 'N/A')}'")
```

### Passo 2: Melhorar UMA Leção de Cada Vez (Script Individual)
Crie `_melhorar_lezX.py` para cada lezione.

**Template Base:**
```python
import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

def melhorar_explicacao(texto_original, tipo_exercicio, verbo=None, tema=None):
    """
    Aplica melhoras automáticas baseadas em regex e regras fixas.
    Retorna string melhorada ou texto original se já for bom.
    """
    
    # Regra 1: Expandir explicações de tempo verbal genéricas
    if "passato prossimo" in texto_original.lower() and len(texto_original) < 40:
        return (f"Passato prossimo di {verbo or 'VERBO'} (categoria): resposta. "
                f"Auxiliar [avere/essere]: conjugacao. Participio passato [forma]. "
                f"Marcador temporal indica ação completada.")
    
    # Regra 2: Adicionar contexto gramatical explícito
    if len(texto_original) < 50 and tema:
        return (f"{texto_original} Contexto: {tema}. "
                f"Dica pedagógica para o aluno.")
    
    # Se já tem >100 chars, presumivelmente está bom
    if len(texto_original.strip()) > 100:
        return texto_original
    
    return texto_original

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez_index = 0 # ATUALIZE COM O ÍNDICE DA LEIÇÃO
lez = next(u for u in modulo["unite"] if u["num"] == f"Lezione X")

print(f"\n=== PROCESSANDO {lez['num']} ===")

total_exercises = len(lez["exercicios"])
migliorati = 0

for i, ex in enumerate(lez["exercicios"]):
    if "explicacao" not in ex:
        ex["explicacao"] = "(sem explicação)"
        print(f"[{i}] Adicionando explicação mínima")
    
    texto_original = ex.get("explicacao", "")
    
    # Lógica específica por tipo de exercício
    if ex["tipo"] == "revelar":
        resposta = ex.get("resposta", "").lower()
        
        # Detectar verbo no participio (padrão: termina em -o, -a irregular)
        palavras_resposta = resposta.split()
        participe_principal = None
        
        for p in palavras_resposta:
            if len(p) > 3 and not p.endswith("o"):
                participe_principal = p.strip(".")
                break
            
            elif len(participo_principale) == 0 and "visto" in participe_principal or "comestibile" in resposta:
                participe_principal = participo_principale
    
        if verbo and participe_principal:
            ex["explicacao"] = migliorare_explicacao(
                texto_original, 
                ex["tipo"], 
                verbo=verbo.capitalize(),
                tema=f"Passato prossimo di {verbo}"
            )
            migliorati += 1
    
    elif ex["tipo"] == "escolha":
        # Para escolha, focar em por que a resposta é correta
        opcoes = ex.get("opcoes", [])
        se_resposta_correta = opcoes[ex.get("resposta", 0)]
        
        explicacao_melhorada = (f"Resposta correta: {se_resposta_correta}. "
                               f"As outras opções são:")
        for j, op in enumerate(opcoes):
            if j != ex.get("resposta", 0):
                explicacao_melhorada += f"\n  - {op} (incorreta)"
        
        if len(texto_original) < 150:
            ex["explicacao"] = explicacao_melhorada + "\n" + texto_original[:80]
            migliorati += 1

# Salvar
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nOK: {lez['num']} — Melhoradas: {migliorati}/{total_exercises}")
```

### Passo 3: Revisão Humana (Manual ou com LLM)
Para explicações complexas, use LLM com prompt:

**Prompt para LLM:**
```
Atua como professor de italiano sênior. Melhore estas explicações gramaticais para o módulo A1:

{explicacoes_a_melhorar}

Regras:
1. Explicação deve ser pedagógica (explique a REGRA, não só a resposta)
2. Mencione se é regolare/irregolare
3. Use terminologia consistente: presente indicativo, passato prossimo, etc.
4. Para tempos verbais: inclua auxiliar + participio e marcador temporal se houver
5. Duração ideal: 80-150 caracteres
6. Linguagem: português (como no JSON atual)

Exemplo de antes/depois:
ANTES: "Passato prossimo."
DEPOIS: "Passato prossimo di mangiare: io ho mangiato. Auxiliar avere + participio -ato. 'Ieri' indica ação completada no passado."
```

### Passo 4: Validação Final
```python
# Verificar estatísticas
import json

with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = modulo["unite"][0] # primeira lezione como exemplo

total_exercises = len(lez["exercicios"])
sem_explicacao = sum(1 for e in lez["exercicios"] if not e.get("explicacao"))
explicacoes_curtes = sum(1 for e in lez["exercicios"] 
                         if "explicacao" in e and len(e["explicacao"].strip()) < 50)
media_caracteres = sum(len(e.get("explicacao", "")) for e in lez["exercicios"]) / total_exercises

print(f"""
=== VALIDAÇÃO {lez['num']} ===
Total exercícios: {total_exercises}
Sem explicação: {sem_explicacao}
Com explicação curta (<50 chars): {explicacoes_curtes}
Média de caracteres por explicação: {media_caracteres:.1f}

Status: {'✅ OK' if sem_explicacao == 0 and media_caracteres >= 60 else '⚠️ REVISÃO Necessária'}""")
```

---

## Exemplos Completos de Antes/Depois

### Exercício 1 — Revelar (Passato Prossimo)

**ANTES:**
```json
{
  "tipo": "revelar",
  "pergunta": "**Esercizio** — Completa:",
  "resposta": "ho mangiato",
  "explicacao": "Passato prossimo."
}
```

**DEPOIS:**
```json
{
  "tipo": "revelar",
  "pergunta": "**Esercizio extra** — Completa com a forma correta do passato prossimo:",
  "resposta": "ho mangiato",
  "explicacao": "Passato prossimo di mangiare (verbo -ARE): ho mangiato. Auxiliar AVERE no presente (primeira pessoa: io HO). Participio 'mangiato' é regular (-ato). Marcador temporal (se houver, ex: ieri) indica ação completada → passato prossimo obrigatório."
}
```

### Exercício 2 — Escolha (Articoli)

**ANTES:**
```json
{
  "tipo": "escolha",
  "pergunta": "Quale articolo per 'amica'?",
  "opcoes": ["il amica", "lo amica", "l'amica"],
  "resposta": 2,
  "explicacao": "L' antes vocálico."
}
```

**DEPOIS:**
```json
{
  "tipo": "escolha",
  "pergunta": "Quale articolo determinativo è corretto per 'amica'? (feminino)",
  "opcoes": ["il amica", "lo amica", "l'amica"],
  "resposta": 2,
  "explicacao": "RESPOSTA CORRETA: l'amica. Regra: L' davanti a vocálica (a). IL seria masculino; LO para s+cons/z/gn/ps/x/y. Plural de amica: le amiche."
}
```

### Exercício 3 — Imperfetto

**ANTES:**
```json
{
  "tipo": "revelar",
  "pergunta": "Completa:",
  "resposta": "io leggevo",
  "explicacao": "Imperfetto."
}
```

**DEPOIS:**
```json
{
  "tipo": "revelar",
  "pergunta": "**Esercizio extra** — Volgere al imperfetto:",
  "resposta": "io leggevo",
  "explicacao": "Imperfetto indicativo di leggere (verbo -ERE): io leggevo. Sufixo regular: -evo na primeira pessoa. Uso: descrições contínuas no passado, ações em progresso (contexto temporal 'mentre', 'quando'). Formas regulares de -ERE têm -evo, -evi, -eva, etc."
}
```

---

## Checklist de Qualidade

Cada explicação deve responder a estas perguntas:

- [ ] Explica a **REGRÁ**, não só o resultado?
- [ ] Menciona se é **regolare ou irregolare**?
- [ ] Usa terminologia consistente (tempo verbal, persona, etc.)?
- [ ] Para tempos verbais: menciona auxiliar + participio?
- [ ] Indica exceções relevantes?
- [ ] Duração ideal: 80-150 caracteres?
- [ ] Linguagem clara em português?
- [ ] Contexto pedagógico para o aluno?

---

## Script de Melhoria Automática com LLM (Opcional)

Para automação total, crie `melhorar_con_llm.py`:

```python
import json
from openai import OpenAI # ou litellm

clien = OpenAI(api_key="...")
path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

def melhorar_com_llm(prompt, modelo="gpt-4o"):
    resposta = clien.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": prompt}]
    )
    return resposta.choices[0].message.content

# Processar por blocos (API é cara)
blocos = [lez["exercicios"] for lez in modulo["unite"]]

for bloco in blocos:
    prompts = [f"{json.dumps(ex, ensure_ascii=False)}" for ex in bloco if len(ex.get("explicacao", "")) < 100]
    if not prompts:
        continue
    
    prompt_final = "\n\n".join(prompts)
    sistema_prompt = ("""Atua como professor de italiano sênior. Melhore estas explicações gramaticais para o módulo A1." +
                       """Regras: explique a REGRA, mencione regolare/irregolare, use terminologia consistente, 80-150 chars, português.""" )
    
    resposta = melhorar_com_llm(sistema_prompt + prompt_final)
    # Processar respostas e atualizar JSON...
```

---

## Ordem de Execução

1. **Análise inicial**: Rode script de diagnóstico para identificar explicações fracas
2. **Melhoria automática**: Execute scripts individuais (`_melhorar_lezX.py`) com regras fixas
3. **Revisão humana/LLM**: Use prompt acima para casos complexos
4. **Validação final**: Verifique estatísticas (100% com explicação, média >80 chars)

**Dica**: Comece pela Lezione I (articoli — mais simples) para testar o fluxo.
