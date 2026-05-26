# Instruções: Adicionar 30 Exercícios por Lezione

## Objetivo

Adicionar **30 exercícios extras** a cada lezione do módulo A1 do arquivo `grammar.json`, localizando e inserindo **antes** dos exercícios tipo `"escolha"` (que são os "Esercizi di verifica" — sempre no final).

---

## Localização dos Arquivos

- **JSON principal:** `C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json`
- **Python:** `C:\Users\bruno\AppData\Local\Programs\Python\Python311\python.exe`

---

## Estrutura do JSON

```json
{
  "moduli": [
    {
      "id": "A1",
      "unidades": [
        {
          "id": "a1-lez1",
          "num": "Lezione I",
          "titulo": "...",
          "teoria": "...",
          "exemplos": [...],
          "exercicios": [ ... ]
        }
      ]
    }
  ]
}
```

---

## Tipos de Exercício

### Tipo `"revelar"` (completar / transformar)
O aluno vê a pergunta, pensa, e revela a resposta.

```json
{
  "tipo": "revelar",
  "pergunta": "**Esercizio extra** — Complete com a forma correta:\nLui _____ (mangiare) la pizza ieri.",
  "resposta": "ha mangiato",
  "explicacao": "Passato prossimo di mangiare (verbo -ARE): ha mangiato."
}
```

### Tipo `"escolha"` (múltipla escolha)
O aluno escolhe a opção correta. `"resposta"` é o **índice 0-based** da opção correta.

```json
{
  "tipo": "escolha",
  "pergunta": "Quale frase è corretta?",
  "opcoes": [
    "Io mangiavo molto quando ero bambino.",
    "Io mangiava molto quando ero bambino.",
    "Io mangiavi molto quando ero bambino."
  ],
  "resposta": 0,
  "explicacao": "Prima persona singolare dell'imperfetto: mangiAVO."
}
```

---

## Regra de Inserção

Os 30 novos exercícios devem ser inseridos **entre o último revelar do livro e o primeiro escolha** (esercizi di verifica).

**Nunca** inserir depois dos `"escolha"` existentes.

### Como encontrar o ponto de inserção:

```python
exercicios = lez["exercicios"]
# Encontrar o índice do primeiro "escolha" existente
idx_insert = next(
    (i for i, e in enumerate(exercicios) if e["tipo"] == "escolha"),
    len(exercicios)
)
# Inserir os novos exercícios ANTES desse índice
for i, ex in enumerate(novos_exercicios):
    exercicios.insert(idx_insert + i, ex)
```

---

## Template de Script Python

Use este template para cada lezione. Substitua `"Lezione X"` pelo número correto.

```python
import json

path = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

modulo = next(m for m in data["moduli"] if m["id"] == "A1")
lez = next(u for u in modulo["unidades"] if u["num"] == "Lezione I")

novos = [
    # COLOQUE AQUI OS 30 NOVOS EXERCÍCIOS
    # misture tipos "revelar" e "escolha" conforme o tema
]

# Inserir antes dos "escolha" existentes
exercicios = lez["exercicios"]
idx = next((i for i, e in enumerate(exercicios) if e["tipo"] == "escolha"), len(exercicios))
for i, ex in enumerate(novos):
    exercicios.insert(idx + i, ex)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

escolha = sum(1 for e in lez["exercicios"] if e["tipo"] == "escolha")
revelar = sum(1 for e in lez["exercicios"] if e["tipo"] == "revelar")
print(f"OK: {lez['num']} — {len(lez['exercicios'])} total (escolha: {escolha}, revelar: {revelar})")
```

---

## Situação Atual de Cada Lezione

| Lezione | Tema | Total atual | Escolha | Revelar |
|---------|------|-------------|---------|---------|
| Lezione I | Articoli / Genere / Numero | 42 | 15 | 27 |
| Lezione II | Verbi presente / Avere / Essere | 37 | 18 | 19 |
| Lezione III | Preposizioni articolate | 44 | 20 | 24 |
| Lezione IV | Passato prossimo | 53 | 22 | 31 |
| Lezione V | La particella "ci" / Partitivo | 40 | 20 | 20 |
| Lezione VI | Futuro semplice e composto | 44 | 20 | 24 |
| Lezione VII | I possessivi | 42 | 20 | 22 |
| Lezione VIII | I pronomi diretti | 42 | 20 | 22 |
| Lezione IX | L'imperfetto indicativo | 45 | 20 | 25 |

**Meta após adição:** cada lezione terá **+30 exercícios** a mais (total mínimo ~70–80 por lezione).

---

## Temas por Lezione para os 30 Novos Exercícios

### Lezione I — Articoli, Genere, Numero
- Artigos definidos/indefinidos (il/lo/la/l'/i/gli/le / un/uno/una/un')
- Plural de substantivos em -o, -a, -e, -co, -ga, -io
- Concordância adjetivo-substantivo
- Frases simples no presente com ser/estar/ter

### Lezione II — Verbi -ARE/-ERE/-IRE / Avere / Essere
- Conjugação presente de verbos -ARE regulares
- Conjugação presente de verbi irregolari (andare, venire, fare, dare, stare)
- Avere vs essere com adjetivos e expressões idiomáticas
- Perguntas e negações no presente

### Lezione III — Preposizioni articolate
- Preposizioni semplici (di, a, da, in, con, su, per, tra/fra)
- Preposizioni articolate (del/dello/della/dell'/dei/degli/delle etc.)
- Verbi di moto + preposição (andare a/in, venire da, tornare a)
- Localizações (sopra, sotto, davanti a, dietro, vicino a)

### Lezione IV — Passato prossimo
- Participio passato regolare (-ato/-uto/-ito) e irregolare
- Passato prossimo com AVERE vs ESSERE (accordo del participio)
- Verbi riflessivi al passato prossimo
- Verbi servili (dovere/potere/volere) al passato prossimo

### Lezione V — La particella "ci" / Partitivo
- Ci come pronome di luogo (c'è / ci sono / ci vado)
- Ci con verbi (volerci, metterci, farcela)
- Articoli partitivi (del/dello/della + dei/degli/delle)
- Qualche vs alcuni/alcune vs un po' di

### Lezione VI — Futuro semplice e composto
- Futuro semplice regolare (-ARE/-ERE/-IRE)
- Futuro irregolare (essere/avere/andare/venire/fare/dire/potere/dovere/volere)
- Futuro composto (avrò/sarò + participio passato)
- Uso del futuro per probabilità presente

### Lezione VII — I possessivi
- Aggettivi possessivi con/senza articolo
- Possessivi con nomi di parentela (mia madre / il mio amico)
- Pronomi possessivi (il mio / il tuo / il suo)
- Espressioni senza articolo (a casa mia, a piede mio, etc.)

### Lezione VIII — I pronomi diretti
- Pronomi diretti atoni (mi/ti/lo/la/ci/vi/li/le)
- Pronomi diretti con passato prossimo (accordo)
- Pronome NE (quantità)
- Pronomi con verbi servili e posizione (lo posso fare / posso farlo)

### Lezione IX — L'imperfetto indicativo
- Imperfetto regolare (tutte e tre le coniugazioni)
- Imperfetto irregolare (essere/avere/fare/dire/bere)
- Passato prossimo vs imperfetto (azione vs descrizione/abitudine)
- Mentre + imperfetto / Durante + sostantivo

---

## Regras Importantes

1. **Nunca modificar** os exercícios `"escolha"` já existentes (esercizi di verifica do livro)
2. **Nunca modificar** o campo `"teoria"` das lezioni
3. Os 30 novos exercícios devem ser **coerentes com o tema da lezione**
4. Misture os tipos: aproximadamente **15 revelar + 15 escolha** por lote (ou conforme fizer mais sentido pedagógico)
5. O campo `"explicacao"` é obrigatório em todos os exercícios — explique a regra gramatical
6. Em `"revelar"`, o campo `"resposta"` deve ser a resposta exata esperada (pode conter múltiplas formas separadas por `/` se houver variação)
7. Em `"escolha"`, `"resposta"` é um número inteiro (0 = primeira opção, 1 = segunda, 2 = terceira)
8. A `"pergunta"` pode usar **markdown**: `**negrito**`, `_itálico_`, listas com `-`

---

## Exemplo Completo: 5 Exercícios para Lezione I

```python
novos = [
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio extra 1** — Inserire l'articolo indeterminativo corretto:\n___ libro / ___ zaino / ___ amica / ___ studio",
        "resposta": "un libro / uno zaino / un'amica / uno studio",
        "explicacao": "UN prima di consonante (libro). UNO prima di z, s+consonante (zaino, studio). UN' prima di vocale femminile (amica)."
    },
    {
        "tipo": "escolha",
        "pergunta": "Quale articolo è corretto davanti a 'studente'?",
        "opcoes": ["il studente", "lo studente", "l'studente"],
        "resposta": 1,
        "explicacao": "LO si usa davanti a parole maschili che iniziano con s + consonante, z, gn, ps, x, y."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio extra 2** — Volgere al plurale:\nii medico / la farmacia / l'amico / lo psicologo / il lago",
        "resposta": "i medici / le farmacie / gli amici / gli psicologi / i laghi",
        "explicacao": "Medico→medici (-co→-ci quando persona). Farmacia→farmacie. Amico→amici. Psicologo→psicologi. Lago→laghi (mantiene suono /g/)."
    },
    {
        "tipo": "escolha",
        "pergunta": "Qual è il plurale di 'l'amica'?",
        "opcoes": ["le amiche", "le amici", "gli amiche"],
        "resposta": 0,
        "explicacao": "Amica è femminile, plurale LE. Amica→amiche (conserva il suono /k/ con -che)."
    },
    {
        "tipo": "revelar",
        "pergunta": "**Esercizio extra 3** — Completare con l'articolo determinativo:\n___ sport / ___ yoga / ___ pneumatico / ___ gnomo / ___ psichiatra",
        "resposta": "lo sport / lo yoga / il pneumatico / lo gnomo / lo psichiatra",
        "explicacao": "LO davanti a: s+cons (sport), y (yoga), gn (gnomo), ps (psichiatra). IL davanti a pn (pneumatico) — uso variabile, ma 'il' è più comune."
    }
]
```

---

## Ordem de Execução

Crie **um script Python por lezione**, salve como `_lez1_extra.py`, `_lez2_extra.py`, etc., e execute com:

```bash
"C:\Users\bruno\AppData\Local\Programs\Python\Python311\python.exe" _lez1_extra.py
"C:\Users\bruno\AppData\Local\Programs\Python\Python311\python.exe" _lez2_extra.py
# ... e assim por diante até _lez9_extra.py
```

Após cada execução, verifique a saída: ela mostrará o total de exercícios atualizado.
