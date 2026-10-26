# 🏛️ Plano Mestre de Expansão: 1.000 Palavras Mais Usadas & 500 Flashcards de Alta Retenção

Este documento estabelece o plano de arquitetura, curadoria lexicográfica, estruturação de dados e integração pedagógica para a expansão do aplicativo **Italiano Autentico** com:
1. **1.000 Palavras Mais Frequentes do Italiano** (baseadas no *Nuovo Vocabolario di Base* de Tullio De Mauro e corpus *CoLFIS*).
2. **500 Cards Estruturados para o Atelier de Memória (Flashcards Studio)** com evocação ativa, lacunas cloze de contexto, pronúncia IPA e repetição espaçada com algoritmo **FSRS / SM-2**.

---

## 🎯 1. Objetivos e Cobertura Pedagógica

```
┌────────────────────────────────────────────────────────────────────────┐
│  PIRÂMIDE DE FLUÊNCIA E RETENÇÃO COGNITIVA                            │
├────────────────────────────────────────────────────────────────────────┤
│  Top 1.000 Palavras Mais Usadas  ──► Cobre ~85% do italiano diário     │
│  500 Flashcards Estruturais      ──► Automatiza chunks, reflexos e     │
│                                       elimina os maiores fósseis       │
│                                       (falsos amigos e preposições)    │
└────────────────────────────────────────────────────────────────────────┘
```

- **Cobertura Lexical:** As 1.000 palavras representam o núcleo fundamental de sobrevivência e conversação fluida (A1 a B1).
- **Cards Estruturados (500 itens):** Em vez de cartas mecânicas de vocábulo isolado (*"cane = cachorro"*), os 500 cards focam em **colocações reais, orações contextualizadas, modo cloze com lacuna e contraste de falsos amigos**.

---

## 📚 2. Estrutura das 1.000 Palavras (Top 1.000 NVdB)

As 1.000 palavras serão distribuídas em **4 blocos de frequência de 250 palavras cada**, facilitando o estudo progressivo:

### Bloco 1: Rank 1 a 250 — Fundamentos Estruturais (A1)
- **Verbos Auxiliares & Modais:** *essere, avere, fare, andare, potere, volere, dovere, sapere, venire, dire*.
- **Conectivos & Preposições Articuladas:** *ma, perché, se, quando, anche, con, su, tra, dal, nello, alla*.
- **Pronomes Diretos & Indiretos:** *mi, ti, lo, la, ci, vi, li, le, ne, gli*.
- **Estruturas de Sobrevivência:** saudações, interrogações (*chi, che cosa, dove, come, quando, quanto, quale*), números e tempo.

### Bloco 2: Rank 251 a 500 — Rotina, Casa e Relações (A1–A2)
- **Ações Cotidianas:** *mangiare, bere, dormire, prendere, mettere, capire, sentire, vedere, chiamare, aspettare, trovare, lasciare*.
- **Ambiente & Família:** partes da casa, cidade, família estendida, trabalho, dinheiro e transportes.
- **Adjetivos Primários:** *buono, bello, grande, piccolo, nuovo, vecchio, stesso, altro, primo, ultimo, giusto*.

### Bloco 3: Rank 501 a 750 — Comunicação, Sentimentos e Opinião (A2–B1)
- **Verbos de Comunicação e Pensamento:** *pensare, credere, sperare, ricordare, dimenticare, spiegare, chiedere, rispondere, sembrare, piacere*.
- **Advérbios Modais e Temporais:** *subito, già, ancora, forse, quasi, appena, ormai, purtroppo, volentieri, davvero, infatti*.
- **Substantivos Abstratos & Trabalho:** *tempo, problema, lavoro, idea, momento, vita, mondo, caso, modo, parte, storia*.

### Bloco 4: Rank 751 a 1000 — Expressões Idiomáticas, Falsos Amigos e Colocações (B1)
- **Chunks & Marcadores Discursivos:** *insomma, figurati, cioè, comunque, anzi, mica, invece, d'altronde, a proposito*.
- **Falsi Amici Críticos:** *salire* (subir), *curare* (tratar), *tovaglia* (toalha de mesa), *spendere* (gastar), *prima* (antes), *morbido* (macio), *rumore* (barulho), *annoiare* (entediar).
- **Verbos Pronominais Essenciais:** *andarsene, farcela, volerci, mettersi, accorgersi, intendersi*.

---

## 🎴 3. Taxonomia dos 500 Flashcards

Os 500 flashcards serão divididos estrategicamente em **5 baralhos temáticos de 100 cartas cada**, integrados diretamente ao estúdio de repetição espaçada:

| Baralho | Quantidade | Foco Didático | Exemplo no Card |
| :--- | :---: | :--- | :--- |
| **Deck 1: Colocações & Chunks** | 100 cards | Frases feitas de uso instantâneo | *"Quanto tempo ci vuole per arrivare?"* (ci volere) |
| **Deck 2: Falsos Amigos (Falsi Amici)** | 100 cards | Desarmar armadilhas frequentes para brasileiros | *"Dobbiamo salire al terceiro piano."* (salire = subir) |
| **Deck 3: Preposições & Regências** | 100 cards | Escolha precisa de preposição (*a, di, da, in, su*) | *"Vado ___ Roma"* vs *"Vado ___ Italia"* |
| **Deck 4: Verbos Irregulares em Contexto** | 100 cards | Formas de alta frequência do *passato prossimo* | *"Ho preso il treno"* / *"Siamo andati insieme"* |
| **Deck 5: Situações da Vida Real (Cloze)** | 100 cards | Restaurante, compras, viagens e emergências | *"Vorrei un caffè macchiato, per ___."* (favore) |

---

## 💾 4. Estrutura dos Arquivos de Dados (JSON)

### 4.1. Esquema do Vocabulário (`data/top1000_vocabulario.json`)
```json
{
  "id": "top_001",
  "rank": 1,
  "italiano": "fare",
  "portugues": "fazer",
  "genero": null,
  "plural": null,
  "categoria": "verbo",
  "nivel": "A1",
  "audio_ipa": "/ˈfaːre/",
  "exemplo": "Che cosa fai stasera?",
  "exemplo_pt": "O que você vai fazer hoje à noite?",
  "colocacoes": ["fare colazione", "fare una domanda", "fare una doccia"]
}
```

### 4.2. Esquema dos Cards de Flashcard (`data/top500_flashcards.json`)
```json
{
  "id": "fc_top_042",
  "deck": "colocacoes",
  "nivel": "A1",
  "frente": "Quanto tempo ___ per finire questo lavoro?",
  "verso": "ci vuole",
  "traducao_frase": "Quanto tempo é necessário para terminar este trabalho?",
  "dica": "Expressão impessoal com o verbo 'volere' no singular",
  "audio_palavra": "ci vuole",
  "audio_frase": "Quanto tempo ci vuole per finire questo trabalho?",
  "audio_ipa": "/tʃi ˈvwɔːle/",
  "explicacao": "Usa-se 'ci vuole' para tempo singular (un'ora) e 'ci vogliono' para plural (due ore)."
}
```

---

## 🏗️ 5. Cronograma e Fases de Implementação

### Etapa 1: Curadoria & Geração dos Dados Mestres (JSON)
- [ ] Compilar a lista canônica das 1.000 palavras ranqueadas com base no NVdB de Tullio De Mauro.
- [ ] Gerar transcrições fonéticas IPA verificadas para cada termo.
- [ ] Criar frases contextuais bilíngues naturais (sem traduções literais).
- [ ] Produzir os 500 cards com lacunas cloze, dicas didáticas e explicações gramaticais.
- [ ] Salvar em `data/top1000_vocabulario.json` e `data/top500_flashcards.json`.

### Etapa 2: Validação Automatizada de Schemas
- [ ] Estender `scripts/schemas.ts` com `TopVocabSchema` e `FlashcardCardSchema` (via Zod).
- [ ] Rodar `npm run content:validate` para garantir:
  - 100% dos IDs únicos sem duplicatas;
  - Ausência de campos nulos em chaves obrigatórias;
  - Formato IPA com barras `/.../`;
  - Compatibilidade com UTF-8 e acentuação italiana (*è, é, à, ò, ù*).

### Etapa 3: Integração no App & Interface (UI)
- [ ] **Aba Vocabulário (`#sec-vocabolario`):**
  - Adicionar pill de filtro: `"⭐ Top 1000 Mais Usadas"`.
  - Exibir badge numérico de rank de frequência (`#1`, `#250`, etc.).
- [ ] **Aba Flashcard (`#sec-flashcard`):**
  - No seletor de baralhos, incluir o grupo especial:
    - `⭐ Top 500: Colocações & Chunks (100)`
    - `⭐ Top 500: Falsos Amigos (100)`
    - `⭐ Top 500: Preposições & Regências (100)`
    - `⭐ Top 500: Verbos em Contexto (100)`
    - `⭐ Top 500: Situações Práticas (100)`
- [ ] **Integração com o Algoritmo FSRS / SM-2:**
  - Garantir que o progresso e o agendamento de repetição espaçada desses novos baralhos sejam salvos em `localStorage` (`it_fsrs_state` / `it_flashcard_data`).

### Etapa 4: Bateria de Testes Automatizados (E2E & Unitários)
- [ ] Adicionar testes unitários em Vitest para os novos esquemas e filtros.
- [ ] Executar a suite de **Computer Use** (`scripts/computer_use_battery.ts`) para assegurar que:
  - O seletor de baralho carrega as novas cartas sem atraso;
  - A alternância entre os modos Normal, Reverso, Contexto e Escuta funcione;
  - O áudio TTS pronuncie perfeitamente as novas frases e palavras;
  - A memória e o storage não excedam a cota PWA offline.

### Etapa 5: Build, Atualização de Cache & Deploy
- [ ] Incrementar versão do Service Worker (`sw.js`) para `italiano-v147` e cache busters no `index.html`.
- [ ] Atualizar o grafo de conhecimento com `graphify update .`.
- [ ] Publicar na branch `main` e `gh-pages`.
