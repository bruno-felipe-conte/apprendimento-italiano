# Guia Canônico de Prompts para Geração de Conteúdo
## Italiano Autentico (PWA Offline-First)

Este documento reúne os **prompts de sistema e de geração de conteúdo por inteligência artificial** padronizados para cada aba do aplicativo, espelhando estritamente os esquemas de dados de `data/*.json` e as rotinas de importação de `js/ia-import.js`.

---

## 1. Aba: 💬 Dialoghi (Diálogos Situacionais)

### Estrutura dos Dados (`data/dialogi.json` e `it_dialoghi_custom`)
- Cada diálogo contém contexto, nível CEFR (`A1` a `C1`), ícone, vocabulário-chave, XP e uma lista sequencial de turnos (`turni`).
- **Turnos do Personagem:** fala passiva (`frase`, `traducao`, `audio_ipa`).
- **Turnos do Usuário ("Tu"):** fala ativa interativa com 4 alternativas e `resposta_correta` (índice 0 a 3).

### Prompt Padronizado
```text
Crie um diálogo em italiano para estudantes brasileiros. Retorne APENAS o JSON, sem nenhum texto introdutório ou explicativo antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "id": identificador único (ex: "dial_custom_001")
2. "titulo": título temático curto em italiano
3. "icone": emoji representativo do contexto
4. "nivel": escolha estritamente entre "A1", "A2", "B1", "B2" ou "C1"
5. "contexto": descrição clara da situação prática em 1 ou 2 frases em português
6. "turni": array ordenado alternando fala do interlocutor e resposta do usuário:
   - Turno do PERSONAGEM:
     * "id": número sequencial (1, 2, 3...)
     * "personaggio": nome do interlocutor (ex: "Cameriere", "Barista", "Commessa", "Dottore")
     * "frase": fala natural em italiano
     * "traducao": tradução precisa em português brasileiro
     * "audio_ipa": transcrição fonética IPA opcional (pode deixar "")
   - Turno do "Tu" (o usuário responde):
     * "id": número sequencial
     * "personaggio": "Tu"
     * "frase": a resposta CORRETA em italiano
     * "traducao": tradução da resposta correta em português brasileiro
     * "audio_ipa": ""
     * "alternativas": array com 4 opções plausíveis em italiano (a correta obrigatoriamente inclusa)
     * "resposta_correta": índice numérico (0, 1, 2 ou 3) apontando para a resposta certa no array de alternativas
7. "vocabulario_chave": array com 3 a 5 termos essenciais em italiano no infinitivo ou singular
8. "xp_recompensa": número inteiro (ex: 50)

EXEMPLO DE ESTRUTURA:
{
  "id": "dial_custom_001",
  "titulo": "Al Mercato",
  "icone": "🛒",
  "nivel": "A1",
  "contexto": "Você está comprando frutas em uma feira na Itália.",
  "turni": [
    {
      "id": 1,
      "personaggio": "Venditore",
      "frase": "Buongiorno! Cosa desidera?",
      "traducao": "Bom dia! O que deseja?",
      "audio_ipa": ""
    },
    {
      "id": 2,
      "personaggio": "Tu",
      "frase": "Vorrei delle mele, per favore.",
      "traducao": "Eu gostaria de algumas maçãs, por favor.",
      "audio_ipa": "",
      "alternativas": [
        "Vorrei delle mele, per favore.",
        "Non mi piace la frutta.",
        "Dov'è il bagno?",
        "Quanto costa questo vestito?"
      ],
      "resposta_correta": 0
    },
    {
      "id": 3,
      "personaggio": "Venditore",
      "frase": "Certo! Quante ne vuole?",
      "traducao": "Claro! Quantas quer?",
      "audio_ipa": ""
    },
    {
      "id": 4,
      "personaggio": "Tu",
      "frase": "Un chilo, grazie.",
      "traducao": "Um quilo, obrigado.",
      "audio_ipa": "",
      "alternativas": [
        "Non lo so.",
        "Un chilo, graças.",
        "Sono a dieta.",
        "Preferisco le banane."
      ],
      "resposta_correta": 1
    }
  ],
  "vocabulario_chave": ["desiderare", "mela", "chilo"],
  "xp_recompensa": 50
}

TEMA DO DIÁLOGO: [SUBSTITUA PELO TEMA DESEJADO]
```

---

## 2. Aba: 🎵 Canzoni (Letras com Cloze Test)

### Estrutura dos Dados (`data/canzoni.json` e `it_canzoni_custom`)
- Cada canção possui título, artista, nível CEFR (`A1` a `B2`), ícone, tema e estrofes/versos.
- Versos com lacuna: `texto_lacuna` com `___`, `palavra_oculta` e `dica` gramatical.
- Versos repetitivos ou instrumentais: `palavra_oculta: ""`, `texto_lacuna: ""` e `repeticoes: N`.

### Prompt Padronizado
```text
Crie os dados estruturados de uma canção em italiano para exercício de preenchimento de lacunas (Cloze Test). Retorne APENAS o JSON, sem nenhum texto introdutório ou explicativo antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "id": identificador único (ex: "can_custom_001")
2. "titulo": nome da música
3. "artista": nome do intérprete ou "Canto Tradizionale"
4. "nivel": "A1", "A2", "B1" ou "B2"
5. "icone": emoji relacionado ao tema da canção
6. "tema": categoria temático-musical (ex: "storia", "amore", "quotidiano", "viaggio")
7. "estrofes": array com os versos da música na ordem de execução:
   - Versos pedagógicos (com palavra oculta para preenchimento):
     * "id": número sequencial (1, 2, 3...)
     * "texto_completo": verso integral original em italiano
     * "texto_lacuna": verso com a palavra de teste substituída por ___
     * "palavra_oculta": a palavra exata extraída do verso
     * "traducao": tradução do verso em português brasileiro
     * "dica": breve dica gramatical ou contextual (ex: "particípio passado de vedere")
     * "repeticoes": número de repetições consecutivas (1 se não repete)
   - Versos puramente repetitivos ou refrões já treinados:
     * "palavra_oculta": ""
     * "texto_lacuna": ""
     * "dica": ""
     * "repeticoes": quantidade de vezes em sequência
8. "vocabulario_chave": array com 4 a 6 termos essenciais da canção
9. "xp_recompensa": número inteiro (ex: 40 a 60)

EXEMPLO DE ESTRUTURA:
{
  "id": "can_custom_001",
  "titulo": "Bella Ciao",
  "artista": "Canto Partigiano",
  "nivel": "A2",
  "icone": "🌹",
  "tema": "storia",
  "estrofes": [
    {
      "id": 1,
      "texto_completo": "Una mattina mi sono alzato",
      "texto_lacuna": "Una mattina mi sono ___",
      "palavra_oculta": "alzato",
      "traducao": "Uma manhã eu me levantei",
      "dica": "Particípio passado de alzarsi",
      "repeticoes": 1
    },
    {
      "id": 2,
      "texto_completo": "O bella ciao, bella ciao, bella ciao ciao ciao",
      "texto_lacuna": "O ___ ciao, bella ciao, bella ciao ciao ciao",
      "palavra_oculta": "bella",
      "traducao": "Ó bela adeus, bela adeus",
      "dica": "Adjetivo feminino singular",
      "repeticoes": 3
    }
  ],
  "vocabulario_chave": ["alzarsi", "mattina", "libertà"],
  "xp_recompensa": 40
}

MÚSICA: [NOME DA CANÇÃO E ARTISTA]
```

---

## 3. Aba: 📜 Storie (Leitura Assistida e Vocabulário Tokenizado)

### Estrutura dos Dados (`data/storie.json` e `it_storie_custom`)
- A história exibe o modo livro com tradução interativa por parágrafo.
- Cada parágrafo (`testo`) contém o texto integral em italiano, tradução em português e a tokenização de **todas as palavras** do parágrafo com IPA e classe gramatical para acionamento do tooltip flutuante.

### Prompt Padronizado
```text
Crie uma história contextualizada em italiano para estudantes brasileiros. Retorne APENAS o JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "id": identificador único (ex: "stor_custom_001")
2. "titulo": título em italiano
3. "titulo_pt": título em português
4. "nivel": "A1", "A2", "B1", "B2", "C1" ou "C2"
5. "icone": emoji temático
6. "autor": nome do autor ou "Italiano Autentico"
7. "tema": gênero ou tema (ex: "filosofia", "viaggio", "quotidiano")
8. "descricao": resumo de 1 linha em italiano
9. "descricao_pt": resumo de 1 linha em português
10. "xp_recompensa": número inteiro (ex: 60 a 80)
11. "testo": array de 4 a 6 parágrafos estruturados:
    * "id": identificador do parágrafo (ex: "p1", "p2")
    * "italiano": parágrafo em italiano natural e gramaticalmente polido
    * "portugues": tradução fiel e contextualizada em português
    * "parole": array com TODOS os vocábulos do parágrafo:
      - "parola": o termo exatamente como aparece na frase (sem pontuação)
      - "traduzione": tradução direta em português (1 a 3 palavras)
      - "ipa": transcrição fonética IPA entre barras (ex: "/ˈsoːle/")
      - "categoria": uma dentre "sostantivo", "verbo", "aggettivo", "avverbio", "articolo", "preposizione", "pronome", "congiunzione" ou "espressione"

EXEMPLO DE ESTRUTURA:
{
  "id": "stor_custom_001",
  "titulo": "Una Mattina a Roma",
  "titulo_pt": "Uma Manhã em Roma",
  "nivel": "A1",
  "icone": "🏛️",
  "autor": "Italiano Autentico",
  "tema": "quotidiano",
  "descricao": "Marco si sveglia presto e cammina per le strade di Roma.",
  "descricao_pt": "Marco acorda cedo e caminha pelas ruas de Roma.",
  "xp_recompensa": 80,
  "testo": [
    {
      "id": "p1",
      "italiano": "Marco apre la finestra e vede il sole.",
      "portugues": "Marco abre a janela e vê o sol.",
      "parole": [
        {"parola": "Marco", "traduzione": "Marco", "ipa": "/ˈmarko/", "categoria": "sostantivo"},
        {"parola": "apre", "traduzione": "abre", "ipa": "/ˈaːpre/", "categoria": "verbo"},
        {"parola": "la", "traduzione": "a", "ipa": "/la/", "categoria": "articolo"},
        {"parola": "finestra", "traduzione": "janela", "ipa": "/fiˈnɛstra/", "categoria": "sostantivo"},
        {"parola": "e", "traduzione": "e", "ipa": "/e/", "categoria": "congiunzione"},
        {"parola": "vede", "traduzione": "vê", "ipa": "/ˈveːde/", "categoria": "verbo"},
        {"parola": "il", "traduzione": "o", "ipa": "/il/", "categoria": "articolo"},
        {"parola": "sole", "traduzione": "sol", "ipa": "/ˈsoːle/", "categoria": "sostantivo"}
      ]
    }
  ]
}

TEMA DA HISTÓRIA: [DESCREVA O ENREDO OU SITUAÇÃO]
```

---

## 4. Aba: 🗣️ Imitazione (Shadowing Fonético)

### Estrutura dos Dados (`data/imitazioni.json` e `it_imitazioni_custom`)
- Frases autênticas para prática oral em alta e baixa velocidade com gravação do microfone e auto-escuta.

### Prompt Padronizado
```text
Crie uma coleção de frases italianas para prática de pronúncia guiada (Shadowing). Retorne APENAS um array JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Gere entre 8 e 12 frases relacionadas ao tema prático
2. "id": identificador único (ex: "imi_custom_001")
3. "frase_italiano": frase natural em italiano (nem curta demais, nem excessivamente longa)
4. "frase_portugues": tradução equivalente em português brasileiro
5. "nivel": escolha entre "A1", "A2", "B1", "B2" ou "C1"
6. "contexto": explicação prática em português de quando e como usar a frase (1 a 2 frases)
7. "audio_ipa": transcrição IPA entre barras (ex: "/mi ˈskuːzi/") ou string vazia ""
8. "xp_recompensa": 15

EXEMPLO DE ESTRUTURA:
[
  {
    "id": "imi_custom_001",
    "frase_italiano": "Mi scusi, sa dirmi dov'è la stazione centrale?",
    "frase_portugues": "Com licença, o senhor saberia me dizer onde fica a estação central?",
    "nivel": "A1",
    "contexto": "Use para pedir orientações na rua com cortesia e respeito a um desconhecido.",
    "audio_ipa": "/mi ˈskuːzi sa ˈdirmi dov'ɛ la statˈtsjoːne tʃenˈtraːle/",
    "xp_recompensa": 15
  },
  {
    "id": "imi_custom_002",
    "frase_italiano": "Potrebbe ripetere più lentamente, per favore?",
    "frase_portugues": "Poderia repetir mais devagar, por favor?",
    "nivel": "A2",
    "contexto": "Use quando o interlocutor falar rápido e você precisar de clareza auditiva.",
    "audio_ipa": "",
    "xp_recompensa": 15
  }
]

TEMA DAS FRASES: [SUBSTITUA PELO CONTEXTO DESEJADO]
```

---

## 5. Aba: 🏛️ Templi & Flashcards (Vocabulário Sistemático)

### Estrutura dos Dados (`data/templo-N.json` e `it_vocab_custom`)
- Vocábulos com gênero, plural, exemplo contextualizado com tradução, dificuldade e transcrição IPA.

### Prompt Padronizado
```text
Crie uma lista de vocabulário italiano no padrão dos Templos do aplicativo. Retorne APENAS um array JSON, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. Gere de 12 a 20 vocábulos relacionados ao tema proposto
2. "id": identificador único (ex: "vocab_custom_001")
3. "italiano": a palavra ou expressão em italiano
4. "portugues": tradução em português brasileiro
5. "genero": "m" (masculino), "f" (feminino), "m/f" (ambos), ou null para verbos, advérbios e adjetivos
6. "plural": forma plural em italiano, ou null quando não aplicável
7. "exemplo": frase contextual em italiano aplicando o vocábulo naturalmente
8. "exemplo_pt": tradução completa da frase de exemplo em português
9. "categoria": categoria temática (ex: "trasporti", "cucina", "salute", "lavoro")
10. "dificuldade": "facil" (básico), "medio" (intermediário) ou "dificil" (avançado)
11. "audio_ipa": transcrição fonética IPA entre barras obrigatórias (ex: "/ˈtrɛːno/")

EXEMPLO DE ESTRUTURA:
[
  {
    "id": "vocab_custom_001",
    "italiano": "treno",
    "portugues": "trem",
    "genero": "m",
    "plural": "treni",
    "exemplo": "Il treno regionale parte alle nove dalla stazione centrale.",
    "exemplo_pt": "O trem regional parte às nove da estação central.",
    "categoria": "viaggio",
    "dificuldade": "facil",
    "audio_ipa": "/ˈtrɛːno/"
  },
  {
    "id": "vocab_custom_002",
    "italiano": "prenotare",
    "portugues": "reservar",
    "genero": null,
    "plural": null,
    "exemplo": "Ho prenotato una camera doppia per il prossimo fine settimana.",
    "exemplo_pt": "Reservei um quarto duplo para o próximo fim de semana.",
    "categoria": "albergo",
    "dificuldade": "medio",
    "audio_ipa": "/prenoˈtaːre/"
  }
]

TEMA DO VOCABULÁRIO: [SUBSTITUA PELO ASSUNTO DESEJADO]
```

---

## 6. Aba: 📚 Grammatica (Método NMA em 7 Camadas Didáticas)

### Estrutura dos Dados (`data/grammar.json`)
- Cada lição é organizada no método de Napoleão Mendes de Almeida (NMA):
  - **Etapa 1 (Regra):** `cena`, `fio`, `definicao` (`fenomeno`, `causa`, `conceito`), `inventario`, `tabela_visual`, `observacao_cards`, `tecnica`, `teoria`, `ponte`.
  - **Etapa 2 (Exemplos & Armadilhas):** `exemplos_prc` (Pergunta, Resposta, Conclusão), `exemplos` com áudio, `armadilhas` (Errado vs Certo), `coda`.
  - **Etapa 3 (Prática):** `exercicios` (mínimo 10 por lição, tipos `escolha` e `revelar` com explicação didática completa).

### Prompt Padronizado
```text
Crie uma lição de gramática italiana seguindo rigorosamente a arquitetura didática de 7 camadas inspirada em Napoleão Mendes de Almeida (NMA). Retorne APENAS o JSON do objeto da lição, sem texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "id": formato "{nivel}-lez{numero}" (ex: "a2-lez15")
2. "num": numeração ordinal em italiano (ex: "Lezione XV")
3. "titulo": nome do tópico gramatical
4. "subtitulo": síntese didática do capítulo
5. "nivel": "A1", "A2", "B1", "B2", "C1" ou "C2"
6. "cena": {"titulo": string, "texto": string, "origem": string} — cena narrativa introdutória
7. "fio": {"abertura": string, "descoberta": string, "fecho": string} — gancho de raciocínio
8. "alerta": chamada de atenção sobre a utilidade real da regra
9. "inventario": array com os elementos essenciais numerados
10. "definicao": {"fenomeno": string, "causa": string, "conceito": string}
11. "tecnica": passo a passo prático de aplicação da regra
12. "teoria": explicação abrangente com quadros markdown comparativos
13. "ponte": comparação contrastiva entre as estruturas do Português e do Italiano
14. "observacao_cards": array de cartões de observação [{"frente": string, "verso": string, "dica": string}]
15. "exemplos_prc": array de casos analisados no modelo [{"pergunta": string, "resposta": string, "conclusao": string}]
16. "armadilhas": array com armadilhas frequentes para lusófonos [{"errado": string, "certo": string, "motivo": string}]
17. "coda": fechamento prático de memorização
18. "exercicios": array de 10 a 15 exercícios alternando tipos:
    - Tipo "escolha": {"tipo": "escolha", "pergunta": string, "opcoes": [4 opções], "resposta": índice (0 a 3), "explicacao": justificativa gramatical clara}
    - Tipo "revelar": {"tipo": "revelar", "pergunta": string, "resposta": string correta, "explicacao": justificativa didática}

TÓPICO GRAMATICAL: [NOME DO TÓPICO E NÍVEL CEFR]
```

---

## 7. Aba: ❓ Quizzes (Banco de Questões Morfológicas)

### Estrutura dos Dados (`data/quizzes.json`)
- Perguntas organizadas por categoria temática/morfológica com distratores bem calibrados e dicas.

### Prompt Padronizado
```text
Crie uma categoria de questões de quiz para fixação rápida de italiano. Retorne APENAS o JSON da categoria, sem nenhum texto antes ou depois.

REGRAS OBRIGATÓRIAS:
1. "categoria": nome da categoria temática (ex: "artigos_e_substantivos", "passato_prossimo", "pronomi_diretti")
2. "questoes": array com 8 a 15 questões estruturadas:
   * "id": identificador único (ex: "q_art_01")
   * "italiano": termo, frase ou lacuna em italiano
   * "ptbr": tradução ou comando em português
   * "respostaCorreta": a alternativa correta
   * "distratores": array com 3 opções incorretas críveis
   * "dica": dica curta de memorização ou contextualização da regra

EXEMPLO DE ESTRUTURA:
{
  "categoria": "artigos_determinativos",
  "questoes": [
    {
      "id": "q_art_01",
      "italiano": "___ zaino",
      "ptbr": "A mochila (masculino iniciado por Z)",
      "respostaCorreta": "lo",
      "distratores": ["il", "la", "l'"],
      "dica": "Palavras masculinas iniciadas por Z recebem LO no singular."
    }
  ]
}

TEMA DO QUIZ: [SUBSTITUA PELO TEMA DESEJADO]
```
