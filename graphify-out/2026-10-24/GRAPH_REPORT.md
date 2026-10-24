# Graph Report - apprendimento-italiano  (2026-10-24)

## Corpus Check
- 176 files · ~1,087,032 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 2, .example 1, .css 1)

## Summary
- 543 nodes · 648 edges · 56 communities (29 shown, 27 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2a3dde6c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- app.d.ts
- json
- index.ts
- Guia Canônico de Prompts para Geração de Conteúdo
- Core App Specs and Docs
- schemas.ts
- tts_worker.js
- audio_cache.js
- AnalyticsManager
- package.json
- stress-storage.js
- SyncManager
- collaboration.ts
- scripts
- compilerOptions
- devDependencies
- Grammar Curriculum Docs
- security.test.js
- Philosophical Stories Docs
- voice_engine.ts
- NMA Grammar Card Upgrader
- ADR 001: Adoção do Algoritmo FSRS-4.5 para Repetição Espaçada
- ADR 002: Arquitetura do VoiceEngine e Síntese de Voz Híbrida
- Progression and Leveling System
- Quiz Dataset Definitions
- ADR 003: Estratégia de Arquitetura Offline-First (PWA & Cache)
- favorites.js
- meta.js
- stats.js
- templo_data.js
- templo_modal.js
- templos.js
- tts.js
- App Visual Identity (Icon)
- Italian Localization and Testing
- Web Audio Feedback Engine
- FSRS Spaced Repetition Flashcards
- 5000 Words Schema Guide
- Canzoni Frontend Module
- Achievements Frontend Module
- core.js
- Dialoghi Frontend Module
- Grammatica Frontend Module
- Study Heatmap Module
- Internationalization (i18n) Module
- test_backup_and_ia.js
- Shadowing Imitazione Module
- Notifications Module
- User Onboarding Module
- User Profile Module
- Interactive Quiz Module
- Storie Reading Module
- Guided Tour Module
- Vocabulary Temple Module
- 5000 Words Expansion Spec
- Service Worker Offline Cache

## God Nodes (most connected - your core abstractions)
1. `SyncManager` - 21 edges
2. `scripts` - 16 edges
3. `AnalyticsManager` - 15 edges
4. `vitest` - 14 edges
5. `compilerOptions` - 14 edges
6. `FeatureFlagManager` - 12 edges
7. `PluginManager` - 12 edges
8. `Guia Canônico de Prompts para Geração de Conteúdo` - 9 edges
9. `SupabaseAdapter` - 7 edges
10. `PocketBaseAdapter` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Decisão` --references--> `escapeHtml()`  [INFERRED]
  docs/adr/004-security-model.md → tests/security.test.js
- `Service Worker Cache & Fetch Lifecycle Resilience` --rationale_for--> `Service Worker Registration & ControllerChange Auto-Reload`  [INFERRED]
  DOCUMENTACAO/QA_AUDIT_INSTRUCTIONS.md → index.html
- `Dyslexia Visual & Typographic Accessibility Plan` --rationale_for--> `Main Single-Page Application HTML Shell (index.html)`  [EXTRACTED]
  dev/plano-dislexia.md → index.html
- `Dyslexia Visual & Typographic Accessibility Plan` --conceptually_related_to--> `Metodologia Gramatical NMA (Pe. Napoleão Mendes de Almeida - 7 Camadas)`  [INFERRED]
  dev/plano-dislexia.md → README.md
- `Parla e Scrivi: La Lingua Italiana come L2 (Lezioni I-XXX)` --semantically_similar_to--> `Parla e Scrivi Raw OCR Source`  [INFERRED] [semantically similar]
  data/parla_e_scrivi.txt → data/parla_e_scrivi_source.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Celebrity Language Learning Methods Suite (Dialoghi, Canzoni, Imitazione, Meta Prazo)** — spec_metodo_famosos_modo_dialogo, spec_metodo_famosos_meta_com_prazo, spec_metodo_famosos_modo_canzone, spec_metodo_famosos_modo_imitacao, index_navigation_sections [EXTRACTED 1.00]
- **Documentação e Armazenamento das 21 Histórias Filosóficas** — data_final_expanso_resultado_expansao_storie_filosofia, data_reporto_storie_filosofia_relatorio_storie_filosofia, data_summary_21_storie_filosofiche_resumo_21_storie, data_final_expanso_resultado_storie_json, data_final_expanso_resultado_storie_filosofia_final_json [EXTRACTED 1.00]
- **App Visual Identity Elements** — icons_icon_app_icon, icons_icon_roman_arch, icons_icon_it_monogram, icons_icon_crimson_gold_palette [EXTRACTED 1.00]
- **Pipeline de Gramática e Exercícios Baseados em Parla e Scrivi** — data_parla_e_scrivi_libro_parla_e_scrivi, data_parla_e_scrivi_source_libro_parla_e_scrivi_source, data_instrucoes_adicionar_exercicios_grammar_json, data_instrucoes_adicionar_exercicios_adicionar_30_exercicios, data_instrucoes_melhorar_explicacoes_melhorar_explicacoes_grammar [INFERRED 0.95]

## Communities (56 total, 27 thin omitted)

### Community 0 - "app.d.ts"
Cohesion: 0.05
Nodes (29): AnalyticsEvent, AppEstado, BackendConfig, FeatureFlag, FlashcardFSRS, IAnalyticsProvider, IBackendAdapter, IPlugin (+21 more)

### Community 1 - "json"
Cohesion: 0.09
Nodes (7): main(), traduzir(), main(), make_est(), translate_hint_to_pt(), main(), translate_it_explanation_to_pt()

### Community 2 - "index.ts"
Cohesion: 0.10
Nodes (13): AppPluginManager, PluginManager, CanzoniPlugin, CorePlugins, DialoghiPlugin, FlashcardsPlugin, GrammaticaPlugin, ImitazionePlugin (+5 more)

### Community 3 - "Guia Canônico de Prompts para Geração de Conteúdo"
Cohesion: 0.08
Nodes (23): 1. Aba: 💬 Dialoghi (Diálogos Situacionais), 2. Aba: 🎵 Canzoni (Letras com Cloze Test), 3. Aba: 📜 Storie (Leitura Assistida e Vocabulário Tokenizado), 4. Aba: 🗣️ Imitazione (Shadowing Fonético), 5. Aba: 🏛️ Templi & Flashcards (Vocabulário Sistemático), 6. Aba: 📚 Grammatica (Método NMA em 7 Camadas Didáticas), 7. Aba: ❓ Quizzes (Banco de Questões Morfológicas), Estrutura dos Dados (`data/canzoni.json` e `it_canzoni_custom`) (+15 more)

### Community 4 - "Core App Specs and Docs"
Cohesion: 0.11
Nodes (17): Grammar JSON Schema (moduli, unidades, escolha, revelar), Parla e Scrivi Book Source (data/parla_e_scrivi.txt), Parla e Scrivi 30-Chapter Grammar JSON Spec, PWA Offline-First Architecture QA Audit Checklist, SPA Modals & File Importers (Templo, Conquista, LevelUp, Onboarding, MetaPrazo, IAImport), SPA Navigation Sections (templi, dialoghi, canzoni, imitazione, flashcard, quiz, vocabolario, grammatica, storie, profilo), Service Worker Registration & ControllerChange Auto-Reload, Main Single-Page Application HTML Shell (index.html) (+9 more)

### Community 5 - "schemas.ts"
Cohesion: 0.09
Nodes (26): ModalAcao, ModalItem, ModalManager, ModalOpcoes, vitest, zod, ingerirConteudo(), IngestOptions (+18 more)

### Community 6 - "tts_worker.js"
Cohesion: 0.43
Nodes (4): criarWavDePcm(), executarInferencia(), sintetizarTexto(), writeString()

### Community 8 - "AnalyticsManager"
Cohesion: 0.09
Nodes (7): AnalyticsManager, AppAnalytics, AppFeatureFlags, FeatureFlagManager, hashStringToInt(), MockAnalyticsProvider, PlausibleAnalyticsProvider

### Community 9 - "package.json"
Cohesion: 0.08
Nodes (25): author, dependencies, zod, description, keywords, license, main, name (+17 more)

### Community 10 - "stress-storage.js"
Cohesion: 0.08
Nodes (18): agora, flashcardData, fsrsJson, LocalStorageMock, readFsrs, storage, t0, t1 (+10 more)

### Community 11 - "SyncManager"
Cohesion: 0.11
Nodes (5): AppSyncManager, MockBackendAdapter, PocketBaseAdapter, SupabaseAdapter, SyncManager

### Community 12 - "collaboration.ts"
Cohesion: 0.21
Nodes (6): AppCollaboration, calcularChecksumSimples(), CollaborationManager, ConflictResolver, LeaderboardManager, SharedDeckManager

### Community 13 - "scripts"
Cohesion: 0.12
Nodes (16): scripts, build, content:ingest, content:validate, dev, format, format:check, fsrs:validate (+8 more)

### Community 14 - "compilerOptions"
Cohesion: 0.12
Nodes (15): compilerOptions, allowJs, checkJs, forceConsistentCasingInFileNames, lib, module, moduleResolution, noEmit (+7 more)

### Community 15 - "devDependencies"
Cohesion: 0.14
Nodes (14): devDependencies, @axe-core/playwright, eslint, @eslint/js, globals, happy-dom, @playwright/test, prettier (+6 more)

### Community 16 - "Grammar Curriculum Docs"
Cohesion: 0.40
Nodes (6): Instruções: Adicionar 30 Exercícios por Lezione (Módulo A1), data/grammar.json, Instruções: Melhorar Explicações dos Exercícios (grammar.json), Parla e Scrivi: La Lingua Italiana come L2 (Lezioni I-XXX), Parla e Scrivi Raw OCR Source, Schema Curricular A1, A2, B1, B2 (Moduli e Unità)

### Community 17 - "security.test.js"
Cohesion: 0.18
Nodes (5): ADR 004: Modelo de Segurança e Blindagem Client-Side, Consequências, Contexto, Decisão, escapeHtml()

### Community 18 - "Philosophical Stories Docs"
Cohesion: 0.43
Nodes (7): Expansão das 21 Histórias Filosóficas (Resultado Final), data/storie_filosofia_final.json (Backup Store), data/storie.json (Philosophical Stories Store), scripts/generare_tutte_le_storie.py, Relatório: Expansão das 21 Histórias Filosóficas, scripts/trasla_storie_dopo_b1_a2.py, Resumo Rápido: 21 Histórias Filosóficas

### Community 19 - "voice_engine.ts"
Cohesion: 0.50
Nodes (3): LexicoItem, VoiceEngine, WorkerMessageData

### Community 20 - "NMA Grammar Card Upgrader"
Cohesion: 0.18
Nodes (4): fs, grammar, fs, g

### Community 21 - "ADR 001: Adoção do Algoritmo FSRS-4.5 para Repetição Espaçada"
Cohesion: 0.40
Nodes (4): ADR 001: Adoção do Algoritmo FSRS-4.5 para Repetição Espaçada, Consequências, Contexto, Decisão

### Community 22 - "ADR 002: Arquitetura do VoiceEngine e Síntese de Voz Híbrida"
Cohesion: 0.40
Nodes (4): ADR 002: Arquitetura do VoiceEngine e Síntese de Voz Híbrida, Consequências, Contexto, Decisão

### Community 23 - "Progression and Leveling System"
Cohesion: 0.47
Nodes (3): _LEVEL_NOMES, LevelUp, Progressao

### Community 24 - "Quiz Dataset Definitions"
Cohesion: 0.40
Nodes (4): QUIZ_FAMILIA, QUIZ_NUMEROS, QUIZ_SAUDACOES, QUIZ_VERBOS

### Community 25 - "ADR 003: Estratégia de Arquitetura Offline-First (PWA & Cache)"
Cohesion: 0.40
Nodes (4): ADR 003: Estratégia de Arquitetura Offline-First (PWA & Cache), Consequências, Contexto, Decisão

### Community 34 - "App Visual Identity (Icon)"
Cohesion: 0.67
Nodes (3): Apprendimento Italiano App Icon, IT Language Monogram, Roman Arch Emblem

### Community 49 - "Italian Localization and Testing"
Cohesion: 0.67
Nodes (3): Italian Localization Guide (UI, Temples, Formats, GDPR), Ten Temples Localization Mapping (Templi I-X), Testing Protocol (Unit, Integration, Performance per Temple)

### Community 70 - "core.js"
Cohesion: 0.20
Nodes (4): App, AppNavigation, AppState, AppXP

### Community 75 - "test_backup_and_ia.js"
Cohesion: 0.11
Nodes (15): BackupReminder, IAImport, agora, ataqueXSS, dialogoTurni, dialogoTurnos, historiaTesto, imitacaoLista (+7 more)

## Knowledge Gaps
- **20 isolated node(s):** `@types/dom-speech-recognition`, `eslint`, `happy-dom`, `prettier`, `tsx` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 324 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **27 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `vitest` connect `schemas.ts` to `index.ts`, `core.js`, `AnalyticsManager`, `package.json`, `test_backup_and_ia.js`, `collaboration.ts`, `SyncManager`, `security.test.js`, `voice_engine.ts`, `Progression and Leveling System`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **What connects `@types/dom-speech-recognition`, `eslint`, `happy-dom` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `app.d.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Why does `scripts` connect `scripts` to `package.json`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.09425287356321839 - nodes in this community are weakly interconnected._
- **Should `index.ts` be split into smaller, more focused modules?**
  _Cohesion score 0.09686609686609686 - nodes in this community are weakly interconnected._
- **Should `Guia Canônico de Prompts para Geração de Conteúdo` be split into smaller, more focused modules?**
  _Cohesion score 0.08333333333333333 - nodes in this community are weakly interconnected._