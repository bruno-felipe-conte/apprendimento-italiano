# Plano: Melhorias Visuais para Dislexia

**Aplicar em:** `C:\Users\bruno\Documents\italian-learning-app-pro`  
**Arquivo principal de CSS inline:** `index.html` (todo o CSS está no `<style>` do `<head>`, linhas 14–435)  
**Arquivo de CSS secundário:** `css/italia.css` (conteúdo do flashcard e vocab — não é o foco aqui)

---

## Contexto

O usuário tem dislexia e quer melhorias visuais que facilitem atenção e leitura, especialmente na aba **Grammatica**. O app é uma PWA vanilla HTML/CSS/JS sem build step. A paleta de cores já usa fundo bege quente (`#F5EDD8`) — excelente para dislexia, não alterar. As mudanças devem ser **cirúrgicas**: só o necessário, sem redesign.

---

## Mudança 1 — Fonte: Atkinson Hyperlegible

**Por quê:** A fonte atual é Lato (boa, mas genérica). Atkinson Hyperlegible foi projetada especificamente para pessoas com baixa visão e dislexia — cada letra tem forma única e inconfundível, especialmente b/d/p/q e i/l/1.

**O que fazer em `index.html`:**

Localizar a linha que carrega as Google Fonts (linha 12) e **adicionar** `Atkinson+Hyperlegible:wght@400;700` ao link existente:

```html
<!-- ANTES -->
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lato:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">

<!-- DEPOIS -->
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Cinzel:wght@400;600;700&family=Lato:ital,wght@0,300;0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
```

Depois, na linha 16 (definição do `body`), adicionar Atkinson como primeira opção:

```css
/* ANTES */
body { font-family: 'Lato', sans-serif; ... }

/* DEPOIS */
body { font-family: 'Atkinson Hyperlegible', 'Lato', sans-serif; ... }
```

---

## Mudança 2 — Espaçamento e tamanho de fonte no conteúdo das lezioni

**Por quê:** Linhas muito juntas forçam o olho a "perder a linha". Texto denso sem respiração é o principal obstáculo para dislexia.

**Classes a modificar em `index.html`:**

### 2a. `.gram-inventario` (lista de itens da Camada Estrutura)
```css
/* ANTES */
.gram-inventario { margin: 0; padding: 0.6rem 0.75rem 0.6rem 1.8rem; font-size: 0.87rem; color: #3a3a3a; line-height: 1.8; }

/* DEPOIS */
.gram-inventario { margin: 0; padding: 0.75rem 1rem 0.75rem 2rem; font-size: 0.92rem; color: #1e1e1e; line-height: 2.1; letter-spacing: 0.018em; }
```

### 2b. `.gram-def-corpo` (Fenômeno / Causa / Conceito)
```css
/* ANTES */
.gram-def-corpo { padding: 0.55rem 0.6rem; font-size: 0.84rem; color: #3a3a3a; line-height: 1.5; }

/* DEPOIS */
.gram-def-corpo { padding: 0.75rem 0.85rem; font-size: 0.9rem; color: #1e1e1e; line-height: 1.85; letter-spacing: 0.015em; }
```

### 2c. `.gram-tecnica-corpo` (Técnica Prática)
```css
/* ANTES */
.gram-tecnica-corpo { padding: 0.6rem 0.75rem; font-size: 0.85rem; color: #3a3a3a; line-height: 1.7; }

/* DEPOIS */
.gram-tecnica-corpo { padding: 0.85rem 1.1rem; font-size: 0.93rem; color: #1e1e1e; line-height: 2.05; letter-spacing: 0.015em; }
```

### 2d. `.gram-prc-pq` e `.gram-prc-conclusao` (linhas P / R / C)
```css
/* ANTES */
.gram-prc-pq { display: flex; align-items: baseline; gap: 0.4rem; padding: 0.25rem 0.6rem; font-size: 0.83rem; color: #444; border-top: 1px solid #f0e8d8; }
.gram-prc-conclusao { display: flex; align-items: baseline; gap: 0.4rem; padding: 0.3rem 0.6rem; background: #f0f9f4; border-top: 1px solid #c8e6c9; font-size: 0.85rem; }

/* DEPOIS */
.gram-prc-pq { display: flex; align-items: baseline; gap: 0.55rem; padding: 0.6rem 0.85rem; font-size: 0.88rem; color: #2c2c2c; border-top: 1px solid #f0e8d8; line-height: 1.7; }
.gram-prc-conclusao { display: flex; align-items: baseline; gap: 0.55rem; padding: 0.65rem 0.85rem; background: #f0f9f4; border-top: 1px solid #c8e6c9; font-size: 0.9rem; line-height: 1.7; font-weight: 700; }
```

### 2e. `.gram-prc-oracao` (frase italiana no topo de cada P→R→C)
```css
/* ANTES */
.gram-prc-oracao { background: #f9f4ee; padding: 0.4rem 0.6rem; font-size: 0.88rem; color: #5C0E1A; cursor: pointer; }

/* DEPOIS */
.gram-prc-oracao { background: #f9f4ee; padding: 0.7rem 0.85rem; font-size: 0.95rem; color: #5C0E1A; cursor: pointer; line-height: 1.6; letter-spacing: 0.02em; }
```

### 2f. `.gram-prc-lista` (espaço entre blocos P→R→C)
```css
/* ANTES */
.gram-prc-lista { padding: 0.4rem 0.75rem 0.6rem; display: flex; flex-direction: column; gap: 0.8rem; }

/* DEPOIS */
.gram-prc-lista { padding: 0.6rem 1rem 1rem; display: flex; flex-direction: column; gap: 1.2rem; }
```

### 2g. `.gram-ponte-corpo` (Ponte BR→IT)
```css
/* ANTES */
.gram-ponte-corpo { padding: 0.6rem 0.75rem; font-size: 0.85rem; color: #3a3a3a; line-height: 1.7; }

/* DEPOIS */
.gram-ponte-corpo { padding: 0.85rem 1.1rem; font-size: 0.93rem; color: #1e1e1e; line-height: 2.0; letter-spacing: 0.015em; }
```

### 2h. `.gram-coda` — remover itálico (itálico é o principal obstáculo tipográfico para dislexia)
```css
/* ANTES */
.gram-coda { background: #2c2c2c; color: #F5EDD8; padding: 0.6rem 0.9rem; border-radius: 8px; font-size: 0.82rem; font-style: italic; }

/* DEPOIS */
.gram-coda { background: #2c2c2c; color: #F5EDD8; padding: 0.85rem 1.1rem; border-radius: 8px; font-size: 0.9rem; font-style: normal; line-height: 1.85; letter-spacing: 0.02em; }
```

---

## Mudança 3 — Labels das camadas: tamanho e legibilidade

**Por quê:** `.gram-camada-label` (STRUTTURA, TECNICA PRATICA, etc.) está em `0.68rem` — muito pequeno e difícil de ler para quem tem dislexia. `.gram-def-label` idem em `0.62rem`.

### 3a. `.gram-camada-label`
```css
/* ANTES */
.gram-camada-label { background: #f5ece0; padding: 0.3rem 0.75rem; font-size: 0.68rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #9B2335; border-bottom: 1px solid #ede5d5; }

/* DEPOIS */
.gram-camada-label { background: #f5ece0; padding: 0.4rem 1rem; font-size: 0.76rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; color: #9B2335; border-bottom: 1px solid #ede5d5; }
```

### 3b. `.gram-def-label`
```css
/* ANTES */
.gram-def-label { padding: 0.25rem 0.6rem; font-size: 0.62rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.07em; }

/* DEPOIS */
.gram-def-label { padding: 0.35rem 0.75rem; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }
```

---

## Mudança 4 — Tags P / R / C: tamanho maior

**Por quê:** Os badges P e C (`0.6rem`) são muito pequenos — o usuário precisa identificar visualmente a função de cada linha sem esforço.

```css
/* ANTES */
.gram-prc-tag { display: inline-block; background: #9B2335; color: white; border-radius: 3px; font-size: 0.6rem; font-weight: 800; padding: 0.1rem 0.3rem; flex-shrink: 0; }

/* DEPOIS */
.gram-prc-tag { display: inline-block; background: #9B2335; color: white; border-radius: 4px; font-size: 0.72rem; font-weight: 800; padding: 0.15rem 0.45rem; flex-shrink: 0; min-width: 1.4rem; text-align: center; }
```

---

## Mudança 5 — Exercício: pergunta mais legível e dica mais visível

**Por quê:** A pergunta do exercício (`.gram-ex-question`) define o que o aluno vai fazer. Para dislexia, deve ser a coisa mais clara da tela.

### 5a. `.gram-ex-question`
```css
/* ANTES */
.gram-ex-question { padding: 1.1rem 1.3rem 1rem; font-size: 1rem; font-weight: 600; color: #1a1a1a; line-height: 1.6; border-bottom: 1px solid #f0e8d8; }

/* DEPOIS */
.gram-ex-question { padding: 1.3rem 1.5rem 1.1rem; font-size: 1.08rem; font-weight: 700; color: #1a1a1a; line-height: 1.75; border-bottom: 1px solid #f0e8d8; letter-spacing: 0.01em; }
```

### 5b. `.gram-ex-dica` (dica antes do exercício — camada 8)
```css
/* ANTES */
.gram-ex-dica { background: #fffbf0; border-left: 3px solid #D4A843; border-radius: 0 6px 6px 0; padding: 0.45rem 0.75rem; font-size: 0.8rem; color: #7a6000; margin: 0.3rem 0 0.7rem; }

/* DEPOIS */
.gram-ex-dica { background: #fffbf0; border-left: 4px solid #D4A843; border-radius: 0 8px 8px 0; padding: 0.65rem 1rem; font-size: 0.88rem; color: #5a4500; margin: 0.5rem 0 1rem; line-height: 1.7; letter-spacing: 0.01em; }
```

### 5c. `.gram-option` (opções de múltipla escolha)
```css
/* ANTES */
.gram-option { ... padding: 0.9rem 1.15rem; ... font-size: 0.9rem; line-height: 1.45; ... }

/* DEPOIS — apenas alterar padding, font-size e line-height */
.gram-option { display: block; width: 100%; text-align: left; padding: 1rem 1.3rem; border: 2px solid #e8ddd0; border-radius: 12px; background: white; cursor: pointer; font-size: 0.96rem; line-height: 1.65; color: #2C2C2C; transition: border-color 0.18s, background 0.18s, color 0.18s; font-family: 'Atkinson Hyperlegible', 'Lato', sans-serif; }
```

Fazer o mesmo ajuste de `padding`/`font-size`/`line-height` para `.gram-option-correct`, `.gram-option-wrong` e `.gram-option-disabled` (mesmas propriedades, apenas mudar para `1rem 1.3rem` / `0.96rem` / `1.65`).

---

## Mudança 6 — Separador visual entre exercícios e teoria

**Por quê:** A transição entre o bloco de exercício e o bloco de teoria precisa ser clara. Adicionar mais espaço no gap da `.gram-lesson-layout`.

```css
/* ANTES */
.gram-lesson-layout { display: flex; flex-direction: column; gap: 1.3rem; }

/* DEPOIS */
.gram-lesson-layout { display: flex; flex-direction: column; gap: 1.8rem; }
```

---

## Mudança 7 — Contador de exercício mais proeminente

**Por quê:** Saber "onde estou" reduz a ansiedade de quem tem dislexia. O label `ESERCIZIO 1 / 127` está em `0.72rem` — muito discreto.

```css
/* ANTES */
.gram-ex-progress-label { font-size: 0.72rem; color: #bbb; margin-bottom: 0.4rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase; }

/* DEPOIS */
.gram-ex-progress-label { font-size: 0.82rem; color: #9B2335; margin-bottom: 0.55rem; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; }
```

---

## Mudança 8 — `.gram-alerta` (Camada 2 — painel vermelho)

**Por quê:** O texto do alerta está em `0.88rem` e é denso. Como é a primeira coisa que o aluno lê na teoria, deve ter boa respiração.

```css
/* ANTES */
.gram-alerta { background: linear-gradient(135deg, #9B2335 0%, #6B1525 100%); color: #F5EDD8; padding: 0.7rem 1rem; border-radius: 8px; font-size: 0.88rem; font-weight: 600; }

/* DEPOIS */
.gram-alerta { background: linear-gradient(135deg, #9B2335 0%, #6B1525 100%); color: #F5EDD8; padding: 1rem 1.25rem; border-radius: 10px; font-size: 0.95rem; font-weight: 600; line-height: 1.75; letter-spacing: 0.015em; }
```

---

## Mudança 9 — Feedback de exercício: remover itálico

**Por quê:** `.gram-lesson-subtitle` e `.gram-res-msg` usam `font-style: italic`. Itálico é notoriamente difícil para dislexia — letras parecem diferentes da forma mental esperada.

```css
/* ANTES */
.gram-lesson-subtitle { font-size: 0.88rem; color: #999; margin-top: 0.35rem; font-style: italic; }

/* DEPOIS */
.gram-lesson-subtitle { font-size: 0.88rem; color: #888; margin-top: 0.35rem; font-style: normal; font-weight: 400; letter-spacing: 0.02em; }
```

```css
/* ANTES */
.gram-res-msg { font-style: italic; color: #777; margin: 0.8rem 0 1.2rem; font-size: 0.95rem; }

/* DEPOIS */
.gram-res-msg { font-style: normal; color: #666; margin: 0.8rem 0 1.2rem; font-size: 0.95rem; font-weight: 600; }
```

---

## Mudança 10 — Hover highlight no bloco P→R→C

**Por quê:** Ao passar o mouse sobre um exemplo, o usuário deve ver claramente qual exemplo está ativo. Isso é uma âncora visual importante.

**Adicionar** esta regra nova após `.gram-prc-row`:

```css
/* NOVO — adicionar após .gram-prc-row */
.gram-prc-row:hover {
  box-shadow: 0 0 0 2px #D4A843;
  border-color: #D4A843;
  transition: box-shadow 0.18s, border-color 0.18s;
}
```

---

## Resumo das classes modificadas

| Classe | Arquivo | O que mudou |
|--------|---------|-------------|
| `<link>` Google Fonts | `index.html` linha 12 | + Atkinson Hyperlegible |
| `body` | index.html linha 16 | font-family: Atkinson Hyperlegible primeiro |
| `.gram-inventario` | index.html | font-size↑, line-height↑, letter-spacing, padding↑ |
| `.gram-def-corpo` | index.html | font-size↑, line-height↑, padding↑ |
| `.gram-tecnica-corpo` | index.html | font-size↑, line-height↑, padding↑ |
| `.gram-prc-pq` | index.html | padding↑, font-size↑, line-height↑ |
| `.gram-prc-conclusao` | index.html | padding↑, line-height↑, font-weight 700 |
| `.gram-prc-oracao` | index.html | padding↑, font-size↑, line-height↑ |
| `.gram-prc-lista` | index.html | gap↑, padding↑ |
| `.gram-ponte-corpo` | index.html | font-size↑, line-height↑, padding↑ |
| `.gram-coda` | index.html | remover italic, font-size↑, line-height↑ |
| `.gram-camada-label` | index.html | font-size↑, padding↑ |
| `.gram-def-label` | index.html | font-size↑, padding↑ |
| `.gram-prc-tag` | index.html | font-size↑, padding↑, min-width |
| `.gram-ex-question` | index.html | font-size↑, line-height↑, padding↑ |
| `.gram-ex-dica` | index.html | font-size↑, padding↑, line-height↑ |
| `.gram-option` (+ correct/wrong/disabled) | index.html | font-size↑, padding↑, line-height↑ |
| `.gram-lesson-layout` | index.html | gap↑ |
| `.gram-ex-progress-label` | index.html | font-size↑, cor mais visível |
| `.gram-alerta` | index.html | padding↑, font-size↑, line-height↑ |
| `.gram-lesson-subtitle` | index.html | remover italic |
| `.gram-res-msg` | index.html | remover italic |
| `.gram-prc-row` (hover) | index.html | novo: outline dourado no hover |

---

## Verificação após aplicar

1. Abrir `index.html` no browser (ou via `npx serve` na pasta do projeto, porta 5500)
2. Ir para aba **Grammatica** → módulo A1 → Lezione I
3. Confirmar:
   - Fonte Atkinson Hyperlegible carregada (inspecionar elemento → computed font-family)
   - Texto da lista de Estrutura tem mais espaçamento vertical
   - Tags P / R / C são maiores e mais fáceis de identificar
   - Nenhum texto em itálico na Coda ou subtítulo da lição
   - Hover em bloco P→R→C mostra borda dourada
   - Dica (`.gram-ex-dica`) tem mais presença visual
4. Verificar no mobile (viewport 390px): nada deve estar cortado

---

## O que NÃO alterar

- Paleta de cores (o bege `#F5EDD8` é ideal para dislexia — não trocar por branco)
- Fonte Cinzel nos títulos (headings decorativos, não são para leitura corrida)
- Estrutura HTML / lógica JS — apenas CSS
- Módulo de flashcards, quiz e vocabulário — foco apenas na aba Grammatica
