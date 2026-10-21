<div align="center">

  <img src="https://raw.githubusercontent.com/bruno-felipe-conte/apprendimento-italiano/main/icons/icon.svg" width="130" alt="Italiano Autentico Logo">

  # Italiano Autentico
  ### PWA Progressivo para Estudo Imersivo da Língua Italiana

  [![Acessar App Online](https://img.shields.io/badge/Acessar%20App-Online-27AE60?style=for-the-badge&logo=googlechrome&logoColor=white)](https://bruno-felipe-conte.github.io/apprendimento-italiano/)
  [![PWA 100% Offline](https://img.shields.io/badge/PWA-100%25%20Offline-2980B9?style=for-the-badge&logo=pwa&logoColor=white)](https://developer.mozilla.org/pt-BR/docs/Web/Progressive_web_apps)
  [![Níveis A1 a C2](https://img.shields.io/badge/Quadro%20Europeu-A1%20a%20C2-E67E22?style=for-the-badge&logo=open-access&logoColor=white)](https://bruno-felipe-conte.github.io/apprendimento-italiano/)
  [![Base de Dados](https://img.shields.io/badge/Vocabul%C3%A1rio-5.300%2B%20Termos-8E44AD?style=for-the-badge&logo=databricks&logoColor=white)](https://bruno-felipe-conte.github.io/apprendimento-italiano/)

  <br>

  ```
  🏛️ 51 Templos de Vocabulário  •  📚 82 Lições NMA  •  💬 200 Diálogos  •  🗣️ 200 Treinos Fonéticos  •  🎵 100 Canções
  ```

</div>

---

## 🏛️ Visão Geral

O **Italiano Autentico** é uma aplicação web progressiva projetada para estudo sistemático do italiano, unindo a clássica pedagogia gramatical humanista ao ritmo de retenção da repetição espaçada moderna.

O sistema funciona inteiramente no navegador, armazena todo o progresso no aparelho do usuário e opera **100% offline** após o primeiro carregamento.

```mermaid
flowchart LR
    A["🏛️ Templos & Vocabulário<br>5.396 termos (IPA)"] --> D["🧠 Memória & Fala<br>Flashcards (FSRS-4.5) & Shadowing"]
    B["📚 Gramática NMA<br>82 Lições (A1 a C2)"] --> D
    C["🎭 Imersão Cultural<br>Diálogos, Músicas & Contos"] --> D
    D --> E["🏆 Fluência & Domínio<br>Ofensivas, XP e Autonomia"]

    style A fill:#FAF7F2,stroke:#C9952A,stroke-width:2px,color:#2E1B0E
    style B fill:#FAF7F2,stroke:#9B2335,stroke-width:2px,color:#2E1B0E
    style C fill:#FAF7F2,stroke:#4A6741,stroke-width:2px,color:#2E1B0E
    style D fill:#FAF7F2,stroke:#4A7FA5,stroke-width:2px,color:#2E1B0E
    style E fill:#FAF7F2,stroke:#3D7A4A,stroke-width:3px,color:#2E1B0E
```

---

## 📊 Painel do Acervo

<div align="center">

| Recurso | Volume | Nível | Foco de Aprendizado |
| :--- | :---: | :---: | :--- |
| **🏛️ Vocabulário nos Templos** | **5.396** palavras | A1 – C2 | Transcrição IPA, gênero gramatical, plurais e exemplos práticos |
| **📚 Lições de Gramática** | **82** lições | A1 – C2 | Método analítico de Napoleão Mendes de Almeida em 7 camadas |
| **💬 Diálogos Situacionais** | **200** cenários | A1 – B2 | Prática interativa por turnos com situações de viagem e cotidiano |
| **🗣️ Treino de Imitação** | **200** exercícios | A1 – C1 | Técnica de *Shadowing* com foco em cadência e fonética real |
| **🎵 Canções Italianas** | **100** músicas | A1 – B2 | Treino de escuta com preenchimento contextual de lacunas (*Cloze*) |
| **📜 Histórias & Filosofia** | **38** textos | B1 – C2 | Tradução por parágrafo, vocabulário assistido e leitura reflexiva |
| **🃏 Sistema de Flashcards** | Algoritmo **FSRS-4.5** | Todos | Agendamento de repetição espaçada contínua para retenção de longo prazo |
| **❓ Quizzes Morfológicos** | Múltiplas etapas | A1 – B2 | Fixação de flexões verbais, artigos e regências |

</div>

---

## 🧭 Jornada de Estudo

A arquitetura do método conduz o estudante da base estrutural à fala autônoma:

```mermaid
graph TD
    subgraph S1 ["1. Estrutura & Fundação"]
        G["📚 Gramática NMA<br>Regras sistemáticas e raciocínio lógico"]
        V["🏛️ Templos de Vocabulário<br>Aquisição progressiva de termos essenciais"]
    end

    subgraph S2 ["2. Retenção Ativa"]
        F["🃏 Flashcards FSRS-4.5<br>Revisão intervalada com foco em evocação ativa"]
        Q["❓ Quizzes Morfológicos<br>Validação de padrões, conjugações e artigos"]
    end

    subgraph S3 ["3. Prática Auditiva e Articulação"]
        D["💬 Diálogos em Turnos<br>Tomada de decisão conversacional"]
        I["🗣️ Shadowing Fonético<br>Ajuste de melodia, acento tônico e ritmo"]
    end

    subgraph S4 ["4. Imersão Cultural"]
        M["🎵 Música Italiana<br>Compreensão de fala conectada e gírias"]
        H["📜 Narrativas & Filosofia<br>Leitura contextual de alto nível"]
    end

    S1 --> S2
    S2 --> S3
    S3 --> S4

    style S1 fill:#FDFBF7,stroke:#C9952A,stroke-width:1.5px
    style S2 fill:#FDFBF7,stroke:#9B2335,stroke-width:1.5px
    style S3 fill:#FDFBF7,stroke:#4A7FA5,stroke-width:1.5px
    style S4 fill:#FDFBF7,stroke:#4A6741,stroke-width:1.5px
```

---

## 🏛️ As 7 Camadas Gramaticais (Método NMA)

As lições de gramática seguem a arquitetura didática inspirada nas obras do gramático Napoleão Mendes de Almeida:

```mermaid
flowchart TD
    C1["1. Alerta<br>Contexto inicial e propósito da regra"] --> C2["2. Inventário<br>Estrutura visual ordenada do conteúdo"]
    C2 --> C3["3. Definição Indutiva<br>Fenômeno linguístico → Causa → Conceito"]
    C3 --> C4["4. Técnica<br>Passo a passo operacional para emprego correto"]
    C4 --> C5["5. Exemplos P-R-C<br>Pergunta / Resposta / Conclusão comentada"]
    C5 --> C6["6. Ponte Comparativa<br>Equivalência direta entre Português e Italiano"]
    C6 --> C7["7. Coda<br>Síntese final de fixação e autoavaliação"]

    style C1 fill:#FAF7F2,stroke:#C9952A,stroke-width:1px
    style C2 fill:#FAF7F2,stroke:#C9952A,stroke-width:1px
    style C3 fill:#FAF7F2,stroke:#9B2335,stroke-width:1.5px
    style C4 fill:#FAF7F2,stroke:#9B2335,stroke-width:1.5px
    style C5 fill:#FAF7F2,stroke:#4A7FA5,stroke-width:1.5px
    style C6 fill:#FAF7F2,stroke:#4A6741,stroke-width:1.5px
    style C7 fill:#FAF7F2,stroke:#3D7A4A,stroke-width:2px
```

---

## 📱 Instalação como Aplicativo (PWA)

O aplicativo funciona diretamente no navegador e pode ser instalado sem loja de apps:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        COMO INSTALAR EM 3 PASSOS                       │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│        🤖 ANDROID        │         🍏 APPLE         │    💻 DESKTOP    │
│  Abra no Google Chrome   │      Abra no Safari      │  Chrome ou Edge  │
│            ↓             │            ↓             │        ↓         │
│     Toque em Menu ⋮      │  Toque em Compartilhar ⎋ │  Clique no ícone │
│            ↓             │            ↓             │  de instalação ⊕ │
│  "Instalar aplicativo"   │ "Adicionar à Tela Início"│ na barra URL     │
└──────────────────────────┴──────────────────────────┴──────────────────┘
```

> **Privacidade local garantida:** Todo o progresso (XP acumulado, ofensivas, cartões revisados e configurações) permanece salvo exclusivamente no `localStorage` do seu dispositivo.

---

## 🛠️ Desenvolvimento & Execução Local

O projeto utiliza Vite 8 e TypeScript estrito, com suíte automatizada de testes (Vitest + Playwright + axe-core):

```bash
# 1. Instalar dependências
npm install

# 2. Iniciar servidor de desenvolvimento (Vite)
npm run dev

# 3. Executar suíte de testes unitários (Vitest)
npm run test

# 4. Validar acervo de conteúdos mestres (Zod)
npm run content:validate

# 5. Validar integridade e mitigação de edge-cases FSRS-4.5
npm run fsrs:validate

# 6. Executar auditoria de acessibilidade WCAG 2.1 AA (@axe-core)
npm run test:a11y

# 7. Verificação de tipos estritos
npm run typecheck

# 8. Compilação de produção
npm run build
```

---

## 📂 Estrutura do Projeto

```text
apprendimento-italiano/
├── index.html              # Ponto de entrada (Single Page Application PWA)
├── vite.config.ts          # Configuração do Vite e Vitest
├── playwright.config.ts    # Configuração de testes de acessibilidade Playwright
├── tsconfig.json           # Configuração TypeScript (Strict mode)
├── css/
│   └── italia.css          # Design system clássico (Cinzel, Garamond, paleta renascentista)
├── types/
│   └── app.d.ts            # Contratos e tipos canônicos da aplicação
├── js/
│   ├── core/               # Módulos desacoplados de arquitetura, dados e sincronização
│   │   ├── state.js        # Estado reativo e persistência
│   │   ├── navigation.js   # Controle de navegação e sidebar
│   │   ├── xp.js           # Gamificação, cálculo de XP e ofensivas
│   │   ├── stats.js        # Estatísticas de estudo e Health Check
│   │   ├── plugins.ts      # Arquitetura de micro-plugins desacoplados (EV-01)
│   │   ├── sync.ts         # Fila offline-first e adaptadores Supabase/PocketBase (EV-02)
│   │   ├── analytics.ts    # Telemetria offline-first e testes A/B determinísticos (EV-04)
│   │   └── collaboration.ts# Reconciliação CRDT/LWW, shared decks e leaderboard (EV-05)
│   ├── plugins/            # Plugins modulares carregados sob demanda
│   ├── core.js             # Facade global retrocompatível (App.*)
│   ├── modal_manager.ts    # Gerenciador unificado de modais (focus trap, ARIA)
│   ├── progression.ts      # Motor de progressão e FSRS
│   ├── voice_engine.ts     # Síntese neural Piper TTS WASM + Web Speech API
│   ├── flashcards.js       # Agendador de repetição espaçada FSRS
│   ├── grammar.js          # Motor das lições de gramática
│   ├── vocab.js            # Explorador dos 51 Templos de Vocabulário
│   ├── dialoghi.js         # Simulação de diálogos interativos
│   ├── canzoni.js          # Exercícios com músicas e cloze test
│   ├── imitazione.js       # Treinos de shadowing fonético
│   └── storie.js           # Visualizador de histórias bilíngues
├── scripts/
│   ├── schemas.ts          # Schemas Zod canônicos para templos, gramática e histórias
│   ├── validate_content.ts # Pipeline de validação estrita de acervo de dados mestres
│   ├── validate-fsrs.js    # Verificador de integridade e edge cases de cartões FSRS
│   ├── ingest_content.ts   # Ingestão segura de novos módulos com deduplicação
│   └── stress-storage.js   # Benchmark e teste de estresse de localStorage
├── tests/
│   ├── a11y/               # Testes automatizados de acessibilidade (WCAG 2.1 AA)
│   ├── content_pipeline.test.ts # Testes do pipeline automatizado de conteúdo
│   ├── sync.test.ts        # Testes de sincronização offline-first e fila
│   ├── analytics.test.ts   # Testes de eventos e amostragem A/B
│   ├── collaboration.test.ts # Testes de reconciliação CRDT e decks compartilhados
│   ├── plugins.test.ts     # Testes do lifecycle de plugins
│   ├── progression.test.ts # Testes de progressão e FSRS
│   ├── voice_engine.test.ts# Testes do motor de áudio
│   ├── security.test.js    # Testes de sanitização XSS e segurança
│   └── navigation.test.js  # Testes de rotas e navegação
├── docs/
│   └── adr/                # Registros de Decisões Arquiteturais (ADRs 001 a 004)
├── data/                   # Acervo JSON (54 arquivos mestres validados com Zod)
├── sw.js                   # Service Worker (estratégia cache-first offline v140)
└── manifest.webmanifest    # Manifesto para instalação PWA
```

---

<div align="center">
  <br>
  <sub><i>Fatto per gli amanti della lingua e della cultura italiana.</i></sub>
</div>
