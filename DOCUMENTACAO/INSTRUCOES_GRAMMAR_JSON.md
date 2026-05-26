# Instruções para Continuar: grammar.json — Parla e Scrivi (30 Capítulos)

## Objetivo Principal

Reescrever completamente o arquivo `data/grammar.json` com todos os **30 capítulos** do livro **"Parla e Scrivi"**. O arquivo atual existe mas está **incompleto e incorreto** — tem apenas 13 unidades, sem o campo `num`, sem o módulo B2, e com tópicos que não correspondem ao livro.

---

## Estado Atual do Projeto

### Arquivos relevantes

| Arquivo | Status | O que é |
|---|---|---|
| `data/grammar.json` | ❌ INCOMPLETO | 3 módulos, 13 unidades, sem campo `num`, sem B2 |
| `js/grammar.js` | ✅ PRONTO | Engine completa — não mexer |
| `js/core.js` | ✅ PRONTO | State management — não mexer |
| `index.html` | ✅ PRONTO | UI + CSS para grammatica — não mexer |
| `data/parla_e_scrivi.txt` | ✅ FONTE | Livro completo extraído (7527 linhas) |

### Problemas no grammar.json atual
1. **Só 3 módulos** (A1, A2, B1) — falta o **B2 inteiro** (10 capítulos: Lezioni XXI–XXX)
2. **Só 13 unidades** de 30 — faltam 17 capítulos
3. **Campo `num` ausente** em todas as unidades — a UI exibe vazio onde deveria aparecer "Lezione I", etc.
4. **Tópicos errados** — não seguem a estrutura do livro (ex: A2 tem Imperfetto que deveria estar em B1)

---

## Fonte de Verdade: o Livro

O livro completo está em:
```
C:\Users\bruno\Documents\italian-learning-app-pro\data\parla_e_scrivi.txt
```
(7527 linhas, extraído com antiword de parla_e_scrivi.doc)

**Use a ferramenta Read** para ler seções do livro ao construir o conteúdo de cada capítulo. O arquivo está em formato de texto com tabelas em estilo `|col|col|col|`. Há ruído de OCR (caracteres estranhos, `[pic]`, etc.) — ignore-os.

---

## Estrutura Exata do JSON

```json
{
  "moduli": [
    {
      "id": "A1",
      "nome": "A1 — Strutture Elementari",
      "nivel_minimo": 1,
      "cor": "linear-gradient(135deg, #27AE60, #145A32)",
      "unidades": [ ...3 unidades: Lezioni I, II, III... ]
    },
    {
      "id": "A2",
      "nome": "A2 — Espansione",
      "nivel_minimo": 3,
      "cor": "linear-gradient(135deg, #2980B9, #1A5276)",
      "unidades": [ ...9 unidades: Lezioni IV–XII... ]
    },
    {
      "id": "B1",
      "nome": "B1 — Intermedio",
      "nivel_minimo": 6,
      "cor": "linear-gradient(135deg, #8E44AD, #5B2C6F)",
      "unidades": [ ...8 unidades: Lezioni XIII–XX... ]
    },
    {
      "id": "B2",
      "nome": "B2 — Avanzato",
      "nivel_minimo": 10,
      "cor": "linear-gradient(135deg, #C0392B, #922B21)",
      "unidades": [ ...10 unidades: Lezioni XXI–XXX... ]
    }
  ]
}
```

### Estrutura de cada unidade

```json
{
  "id": "a1-lez1",
  "num": "Lezione I",
  "titulo": "Nome, Articolo e Aggettivo",
  "subtitulo": "Strutture elementari",
  "teoria": "Texto markdown com **negrito**, *itálico* e tabelas em pipe format",
  "exemplos": [
    { "it": "Il libro è interessante.", "pt": "O livro é interessante." }
  ],
  "exercicios": [
    {
      "tipo": "escolha",
      "pergunta": "Qual artigo vai antes de *zaino*?",
      "opcoes": ["il", "lo", "la", "l'"],
      "resposta": 1,
      "explicacao": "'Zaino' começa com z, então usamos 'lo'."
    },
    {
      "tipo": "revelar",
      "pergunta": "Conjugue ESSERE na 3ª pessoa singular: lui ___",
      "resposta": "è",
      "explicacao": "ESSERE: io sono, tu sei, lui/lei è, noi siamo, voi siete, loro sono."
    }
  ]
}
```

### Regras críticas dos campos:
- **`id`**: único, formato `a1-lez1`, `a2-lez4`, `b1-lez13`, `b2-lez21`
- **`num`**: OBRIGATÓRIO — "Lezione I", "Lezione II", ..., "Lezione XXX" (numeral romano)
- **`titulo`**: Nome do tópico gramatical
- **`subtitulo`**: Subtítulo opcional
- **`teoria`**: Markdown simples. Tabelas com pipes `| col | col |`. Negrito `**texto**`. Itálico `*texto*`. Quebras de linha com `\n`
- **`exemplos`**: Array de 3–5 frases com tradução para português
- **`exercicios`**: MÍNIMO 6 por unidade. Mix de `escolha` e `revelar`

### Dois tipos de exercício:

**Tipo `escolha`** — Múltipla escolha:
```json
{
  "tipo": "escolha",
  "pergunta": "Texto da pergunta (pode usar *itálico* e **negrito**)",
  "opcoes": ["Opção A", "Opção B", "Opção C", "Opção D"],
  "resposta": 0,
  "explicacao": "Explicação do motivo da resposta correta."
}
```
- `opcoes`: sempre 4 opções
- `resposta`: índice (0–3) da opção correta

**Tipo `revelar`** — Preencha / resposta revelada ao clicar:
```json
{
  "tipo": "revelar",
  "pergunta": "Texto da pergunta com ___ para lacuna",
  "resposta": "Resposta correta",
  "explicacao": "Explicação da regra gramatical."
}
```

---

## Os 30 Capítulos — Mapeamento Completo

### Módulo A1 (nivel_minimo: 1) — Lezioni I, II, III

| ID | num | Título | Tópicos do livro |
|---|---|---|---|
| a1-lez1 | Lezione I | Nome, Articolo e Aggettivo | Formazione del nome (m/f), articolo determinativo e indeterminativo, aggettivo |
| a1-lez2 | Lezione II | Presente Indicativo | Verbi regolari -are/-ere/-ire, irregolari (essere, avere, fare, andare, venire, potere, volere, dovere, sapere, stare, bere, dire, uscire) |
| a1-lez3 | Lezione III | Preposizioni Semplici | di, a, da, in, con, su, per, tra/fra; preposizioni articolate (del, al, dal, nel, sul...) |

### Módulo A2 (nivel_minimo: 3) — Lezioni IV–XII

| ID | num | Título | Tópicos do livro |
|---|---|---|---|
| a2-lez4 | Lezione IV | Passato Prossimo | Participio passato regular e irregular; ausiliare essere vs avere; accordo del participio |
| a2-lez5 | Lezione V | La Particella CI | Ci + essere (c'è/ci sono); ci come complemento di luogo; ci avverbiale |
| a2-lez6 | Lezione VI | Futuro Semplice e Anteriore | Futuro regolare e irregolare; futuro anteriore; usi del futuro |
| a2-lez7 | Lezione VII | Aggettivi e Pronomi Possessivi | mio/tuo/suo/nostro/vostro/loro; con e senza articolo |
| a2-lez8 | Lezione VIII | Pronomi Diretti | lo/la/li/le; mi/ti/ci/vi; posizione del pronome |
| a2-lez9 | Lezione IX | Imperfetto Indicativo | Formazione, usi (descrizione, azione abituale, simultanea); imperfetto vs passato prossimo |
| a2-lez10 | Lezione X | Pronomi Indiretti | gli/le/mi/ti/ci/vi; differenza tra diretti e indiretti |
| a2-lez11 | Lezione XI | Pronomi Combinati | me lo/te lo/glielo/ce lo/ve lo/lo/me la/gliela... |
| a2-lez12 | Lezione XII | Verbi Riflessivi | Coniugazione riflessiva al presente e passato prossimo; accordo |

### Módulo B1 (nivel_minimo: 6) — Lezioni XIII–XX

| ID | num | Título | Tópicos do livro |
|---|---|---|---|
| b1-lez13 | Lezione XIII | Condizionale Presente e Passato | Formazione, usi (desiderio, ipotesi, cortesia); condizionale passato |
| b1-lez14 | Lezione XIV | Pronomi Relativi | che, cui, il quale/la quale/i quali/le quali; di cui, a cui |
| b1-lez15 | Lezione XV | Comparativo e Superlativo | più...di/che; meno...di; tanto...quanto; superlativo relativo e assoluto; forme irregolari (migliore, peggiore, maggiore, minore) |
| b1-lez16 | Lezione XVI | Passato Remoto | Formazione regolare e irregolare; uso vs passato prossimo (nord/sud Italia) |
| b1-lez17 | Lezione XVII | Trapassato Prossimo | Formazione (avevo/ero + participio); uso in sequenze temporali |
| b1-lez18 | Lezione XVIII | Preposizioni Avanzate | Preposizioni con mezzi di trasporto, luoghi, tempo; locuzioni preposizionali |
| b1-lez19 | Lezione XIX | Concordanza dei Tempi | Principale + subordinata; quando/mentre/dopo che/prima che; sequenza temporale |
| b1-lez20 | Lezione XX | Particelle CI e NE | CI avverbiale, pronominale, idiomatico (volerci, farcela); NE partitivo e pronominale |

### Módulo B2 (nivel_minimo: 10) — Lezioni XXI–XXX

| ID | num | Título | Tópicos do livro |
|---|---|---|---|
| b2-lez21 | Lezione XXI | Congiuntivo Presente e Passato | Formazione; verbi che reggono il congiuntivo (pensare che, credere che, volere che...) |
| b2-lez22 | Lezione XXII | Congiuntivo Imperfetto e Trapassato | Formazione; concordanza dei tempi con congiuntivo |
| b2-lez23 | Lezione XXIII | Concordanza Indicativo/Congiuntivo | Quando usare ind. vs congiuntivo; verbi di opinione, emozione, dubbio, volontà |
| b2-lez24 | Lezione XXIV | Imperativo | Imperativo regolare (tu/voi/noi); irregolari (essere, avere, andare, fare, dire, stare); pronomi con imperativo |
| b2-lez25 | Lezione XXV | Periodo Ipotetico | Realtà (se + presente + futuro); possibilità (se + congiuntivo imperfetto + condizionale); impossibilità (se + congiuntivo trapassato + condizionale passato) |
| b2-lez26 | Lezione XXVI | Forma Passiva | Essere + participio; venire/andare + participio; si passivante |
| b2-lez27 | Lezione XXVII | Forma Impersonale | Si impersonale; costruzione impersonale con altri verbi |
| b2-lez28 | Lezione XXVIII | Forme Implicite | Gerundio (stare + gerundio, modo, causa); Infinito (dopo preposizioni, come soggetto); Participio passato e presente come aggettivo/relativa |
| b2-lez29 | Lezione XXIX | Discorso Diretto e Indiretto | Trasformazione; cambiamento di tempi, pronomi, espressioni di tempo |
| b2-lez30 | Lezione XXX | Preposizioni e Locuzioni | Locuzioni preposizionali complesse; uso avanzato di preposizioni in contesti formali |

---

## Como Ler o Livro para Extrair Conteúdo

O livro está em `data/parla_e_scrivi.txt`. Use a ferramenta `Read` com `offset` e `limit` para navegar:

| Capítulo | Linha aproximada |
|---|---|
| Lezione I | 940–1480 |
| Lezione II | 1480–2100 |
| Lezione III | 2100–2700 |
| Lezione IV | 2700–3300 |
| Lezione V | 3300–3800 |
| Lezione VI | 3800–4300 |
| Lezione VII | 4300–4800 |
| Lezione VIII | 4800–5200 |
| Lezione IX | 5200–5600 |
| Lezioni X–XII | 5600–6200 |
| Lezioni XIII–XX | 6200–6900 |
| Lezioni XXI–XXX | 6900–7527 |

---

## Checklist de Qualidade por Unidade

Para cada uma das 30 unidades, verifique:
- [ ] `id` único no formato correto (`a1-lez1`, `b2-lez21`, etc.)
- [ ] `num` presente (ex: `"Lezione I"`)
- [ ] `titulo` descritivo do tópico
- [ ] `teoria` com pelo menos uma tabela de conjugação ou regra (markdown pipe)
- [ ] `exemplos`: 3–5 frases italiano + português
- [ ] `exercicios`: mínimo 6, mix de `escolha` e `revelar`
- [ ] Exercícios `escolha`: sempre 4 opções, `resposta` é índice 0–3
- [ ] Exercícios `revelar`: `resposta` é string (a resposta correta)
- [ ] `explicacao` presente em todos os exercícios
- [ ] JSON válido (sem trailing commas, aspas corretas)

---

## Validação Final

Depois de escrever o arquivo, rode este script Python para validar:

```python
import json
with open(r'data/grammar.json', encoding='utf-8') as f:
    data = json.load(f)

total_unidades = sum(len(m['unidades']) for m in data['moduli'])
total_exercicios = sum(len(u['exercicios']) for m in data['moduli'] for u in m['unidades'])
ids = [u['id'] for m in data['moduli'] for u in m['unidades']]
has_num = all('num' in u for m in data['moduli'] for u in m['unidades'])
has_duplicates = len(ids) != len(set(ids))

print(f"Módulos: {len(data['moduli'])} (esperado: 4)")
print(f"Unidades: {total_unidades} (esperado: 30)")
print(f"Exercícios: {total_exercicios} (esperado: 180+)")
print(f"Campo 'num' em todos: {has_num} (esperado: True)")
print(f"IDs duplicados: {has_duplicates} (esperado: False)")
for m in data['moduli']:
    print(f"  {m['id']}: {len(m['unidades'])} unidades")
```

Execute com:
```
cd C:\Users\bruno\Documents\italian-learning-app-pro
python -c "..." (cole o script acima)
```

---

## CSS Necessário (já implementado no index.html)

Os seguintes seletores CSS **já existem** no `index.html` — NÃO precisa adicionar CSS:
- `.gram-btn-revelar` — botão "Ver resposta"
- `.gram-btn-acertei` — botão "✅ Acertei"
- `.gram-btn-errei` — botão "❌ Errei"
- `.gram-resposta-revelada` — div que mostra a resposta revelada
- `.gram-fb-info` — feedback informativo

**Se não existirem**, adicionar dentro do `<style>` em `index.html`:

```css
.gram-btn-revelar {
  background: #3498db; color: #fff; border: none; border-radius: 8px;
  padding: 0.75rem 1.5rem; font-size: 1rem; cursor: pointer; margin-top: 1rem;
}
.gram-btn-acertei {
  background: #27ae60; color: #fff; border: none; border-radius: 8px;
  padding: 0.6rem 1.2rem; font-size: 0.95rem; cursor: pointer;
}
.gram-btn-errei {
  background: #e74c3c; color: #fff; border: none; border-radius: 8px;
  padding: 0.6rem 1.2rem; font-size: 0.95rem; cursor: pointer;
}
.gram-resposta-revelada {
  background: #eaf6ff; border-left: 4px solid #3498db;
  padding: 0.75rem 1rem; border-radius: 6px; margin-top: 0.5rem;
}
.gram-fb-info {
  background: #fef9e7; border-left: 4px solid #f39c12;
  padding: 0.6rem 1rem; border-radius: 6px;
}
```

---

## Exemplo Completo de uma Unidade (Lezione IV — Passato Prossimo)

```json
{
  "id": "a2-lez4",
  "num": "Lezione IV",
  "titulo": "Passato Prossimo",
  "subtitulo": "Azioni passate con risultato nel presente",
  "teoria": "Il **passato prossimo** si forma con:\n**AVERE o ESSERE** (presente) + **participio passato**\n\n**Participio passato regolare:**\n\n| Infinito | Participio |\n|----------|------------|\n| parlare (-are) | parlato |\n| vendere (-ere) | venduto |\n| partire (-ire) | partito |\n\n**Participio passato irregolare (più comuni):**\n\n| Infinito | Participio |\n|----------|------------|\n| essere | stato |\n| fare | fatto |\n| dire | detto |\n| scrivere | scritto |\n| leggere | letto |\n| aprire | aperto |\n| venire | venuto |\n| nascere | nato |\n\n**Ausiliare AVERE** → verbi transitivi (non cambia il participio):\n*Ho mangiato, hai lavorato, ha finito...*\n\n**Ausiliare ESSERE** → verbi di moto/stato + riflessivi (participio concorda!):\n*Sono andato/a, siamo partiti/e, si è alzato/a*",
  "exemplos": [
    { "it": "Stamattina ho fatto colazione alle sette.", "pt": "Esta manhã tomei café da manhã às sete." },
    { "it": "Ieri sera siamo andati al cinema.", "pt": "Ontem à noite fomos ao cinema." },
    { "it": "Maria ha scritto una lettera a sua madre.", "pt": "Maria escreveu uma carta para sua mãe." },
    { "it": "I bambini sono nati a Roma.", "pt": "As crianças nasceram em Roma." },
    { "it": "Non ho ancora letto questo libro.", "pt": "Ainda não li este livro." }
  ],
  "exercicios": [
    {
      "tipo": "escolha",
      "pergunta": "Quale ausiliare si usa con il verbo *andare* al passato prossimo?",
      "opcoes": ["avere", "essere", "fare", "stare"],
      "resposta": 1,
      "explicacao": "'Andare' è un verbo di moto intransitivo, quindi usa l'ausiliare ESSERE."
    },
    {
      "tipo": "escolha",
      "pergunta": "Complete: Ieri Maria ___ al supermercato.",
      "opcoes": ["ha andato", "è andata", "ha andata", "è andato"],
      "resposta": 1,
      "explicacao": "Andare + essere; il soggetto è Maria (femminile) → 'è andata'."
    },
    {
      "tipo": "escolha",
      "pergunta": "Il participio passato di 'scrivere' è:",
      "opcoes": ["scrivuto", "scritto", "scrivito", "scrivo"],
      "resposta": 1,
      "explicacao": "'Scrivere' ha participio irregolare: scritto."
    },
    {
      "tipo": "escolha",
      "pergunta": "Complete: Noi ___ la pizza a casa ieri sera.",
      "opcoes": ["siamo mangiato", "abbiamo mangiati", "abbiamo mangiato", "siamo mangiati"],
      "resposta": 2,
      "explicacao": "'Mangiare' è transitivo → ausiliare AVERE. Il participio non cambia con avere."
    },
    {
      "tipo": "revelar",
      "pergunta": "Coniuga al passato prossimo: (tu) leggere il giornale → ___",
      "resposta": "hai letto il giornale",
      "explicacao": "'Leggere' usa AVERE; participio irregolare: letto."
    },
    {
      "tipo": "revelar",
      "pergunta": "Coniuga al passato prossimo: (loro) partire per Milano → ___",
      "resposta": "sono partiti per Milano",
      "explicacao": "'Partire' usa ESSERE; con soggetto maschile plurale: partiti."
    },
    {
      "tipo": "escolha",
      "pergunta": "Complete: I bambini ___ tardi ieri sera.",
      "opcoes": ["hanno dormito", "sono dormiti", "ha dormito", "è dormito"],
      "resposta": 0,
      "explicacao": "'Dormire' é transitivo/intransitivo mas usa AVERE. → 'hanno dormito'."
    }
  ]
}
```

---

## Ordem de Execução Recomendada

1. **Leia** `data/parla_e_scrivi.txt` (seções por capítulo) com a ferramenta Read
2. **Escreva** o `data/grammar.json` completo com a ferramenta Write
3. **Valide** com o script Python acima
4. **Verifique** no navegador abrindo `index.html` e navegando até a aba Grammatica (tecla `5`)

O arquivo deve ter ≈ 30 unidades × 6+ exercícios = 180+ exercícios no total.

---

## Notas Finais

- O app é **vanilla JS** (sem React, sem framework) — o `grammar.js` já faz todo o rendering
- O texto da `teoria` é renderizado como HTML pelo método `_formatarTeoria()` em `grammar.js`
- XP: 5 XP por exercício correto, +50 XP bônus na primeira conclusão de cada unidade
- A tecla `5` no teclado navega para a seção Grammatica
- O progresso é salvo em `localStorage` com a chave `it_progresso`, campo `grammatica_completadas: []`
