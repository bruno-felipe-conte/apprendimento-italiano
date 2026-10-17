# Graph Report - apprendimento-italiano  (2026-10-17)

## Corpus Check
- 126 files · ~1,065,769 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: .css 2, (none) 1, .webmanifest 1)

## Summary
- 141 nodes · 132 edges · 33 communities (9 shown, 24 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d493ed39`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- PWA Offline-First Architecture QA Audit Checklist
- json
- voice_engine.js
- Core App Specs and Docs
- json
- Grammar Curriculum Docs
- Philosophical Stories Docs
- NMA Grammar Card Upgrader
- Progression and Leveling System
- Quiz Dataset Definitions
- App Visual Identity (Icon)
- Italian Localization and Testing
- Web Audio Feedback Engine
- FSRS Spaced Repetition Flashcards
- 5000 Words Schema Guide
- Canzoni Frontend Module
- Achievements Frontend Module
- Core Application Controller
- Dialoghi Frontend Module
- Grammatica Frontend Module
- Study Heatmap Module
- Internationalization (i18n) Module
- AI Content Import Module
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
1. `Main Single-Page Application HTML Shell (index.html)` - 7 edges
2. `Relatório: Expansão das 21 Histórias Filosóficas` - 5 edges
3. `Celebrity Language Learning Methods Spec (Dialoghi, Meta Prazo, Canzoni, Imitazione)` - 5 edges
4. `main()` - 4 edges
5. `PWA Offline-First Architecture QA Audit Checklist` - 4 edges
6. `Expansão das 21 Histórias Filosóficas (Resultado Final)` - 4 edges
7. `SPA Navigation Sections (templi, dialoghi, canzoni, imitazione, flashcard, quiz, vocabolario, grammatica, storie, profilo)` - 4 edges
8. `User-Created Content Spec (Custom Canzoni & Dialoghi)` - 4 edges
9. `traduzir()` - 3 edges
10. `main()` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Service Worker Cache & Fetch Lifecycle Resilience` --rationale_for--> `Service Worker Registration & ControllerChange Auto-Reload`  [INFERRED]
  DOCUMENTACAO/QA_AUDIT_INSTRUCTIONS.md → index.html
- `Dyslexia Visual & Typographic Accessibility Plan` --rationale_for--> `Main Single-Page Application HTML Shell (index.html)`  [EXTRACTED]
  dev/plano-dislexia.md → index.html
- `Dyslexia Visual & Typographic Accessibility Plan` --conceptually_related_to--> `Metodologia Gramatical NMA (Pe. Napoleão Mendes de Almeida - 7 Camadas)`  [INFERRED]
  dev/plano-dislexia.md → README.md
- `Parla e Scrivi: La Lingua Italiana come L2 (Lezioni I-XXX)` --semantically_similar_to--> `Parla e Scrivi Raw OCR Source`  [INFERRED] [semantically similar]
  data/parla_e_scrivi.txt → data/parla_e_scrivi_source.txt
- `Parla e Scrivi 30-Chapter Grammar JSON Spec` --references--> `Main Single-Page Application HTML Shell (index.html)`  [EXTRACTED]
  DOCUMENTACAO/INSTRUCOES_GRAMMAR_JSON.md → index.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Celebrity Language Learning Methods Suite (Dialoghi, Canzoni, Imitazione, Meta Prazo)** — spec_metodo_famosos_modo_dialogo, spec_metodo_famosos_meta_com_prazo, spec_metodo_famosos_modo_canzone, spec_metodo_famosos_modo_imitacao, index_navigation_sections [EXTRACTED 1.00]
- **Documentação e Armazenamento das 21 Histórias Filosóficas** — data_final_expanso_resultado_expansao_storie_filosofia, data_reporto_storie_filosofia_relatorio_storie_filosofia, data_summary_21_storie_filosofiche_resumo_21_storie, data_final_expanso_resultado_storie_json, data_final_expanso_resultado_storie_filosofia_final_json [EXTRACTED 1.00]
- **App Visual Identity Elements** — icons_icon_app_icon, icons_icon_roman_arch, icons_icon_it_monogram, icons_icon_crimson_gold_palette [EXTRACTED 1.00]
- **Pipeline de Gramática e Exercícios Baseados em Parla e Scrivi** — data_parla_e_scrivi_libro_parla_e_scrivi, data_parla_e_scrivi_source_libro_parla_e_scrivi_source, data_instrucoes_adicionar_exercicios_grammar_json, data_instrucoes_adicionar_exercicios_adicionar_30_exercicios, data_instrucoes_melhorar_explicacoes_melhorar_explicacoes_grammar [INFERRED 0.95]

## Communities (33 total, 24 thin omitted)

### Community 1 - "json"
Cohesion: 0.14
Nodes (5): main(), make_est(), translate_hint_to_pt(), main(), translate_it_explanation_to_pt()

### Community 4 - "Core App Specs and Docs"
Cohesion: 0.15
Nodes (15): Grammar JSON Schema (moduli, unidades, escolha, revelar), Parla e Scrivi Book Source (data/parla_e_scrivi.txt), Parla e Scrivi 30-Chapter Grammar JSON Spec, SPA Modals & File Importers (Templo, Conquista, LevelUp, Onboarding, MetaPrazo, IAImport), SPA Navigation Sections (templi, dialoghi, canzoni, imitazione, flashcard, quiz, vocabolario, grammatica, storie, profilo), Main Single-Page Application HTML Shell (index.html), Italiano Autentico PWA Overview & Architecture, User-Created Content Spec (Custom Canzoni & Dialoghi) (+7 more)

### Community 16 - "Grammar Curriculum Docs"
Cohesion: 0.40
Nodes (6): Instruções: Adicionar 30 Exercícios por Lezione (Módulo A1), data/grammar.json, Instruções: Melhorar Explicações dos Exercícios (grammar.json), Parla e Scrivi: La Lingua Italiana come L2 (Lezioni I-XXX), Parla e Scrivi Raw OCR Source, Schema Curricular A1, A2, B1, B2 (Moduli e Unità)

### Community 18 - "Philosophical Stories Docs"
Cohesion: 0.43
Nodes (7): Expansão das 21 Histórias Filosóficas (Resultado Final), data/storie_filosofia_final.json (Backup Store), data/storie.json (Philosophical Stories Store), scripts/generare_tutte_le_storie.py, Relatório: Expansão das 21 Histórias Filosóficas, scripts/trasla_storie_dopo_b1_a2.py, Resumo Rápido: 21 Histórias Filosóficas

### Community 20 - "NMA Grammar Card Upgrader"
Cohesion: 0.18
Nodes (4): fs, grammar, fs, g

### Community 23 - "Progression and Leveling System"
Cohesion: 0.40
Nodes (3): _LEVEL_NOMES, LevelUp, Progressao

### Community 24 - "Quiz Dataset Definitions"
Cohesion: 0.40
Nodes (4): QUIZ_FAMILIA, QUIZ_NUMEROS, QUIZ_SAUDACOES, QUIZ_VERBOS

### Community 34 - "App Visual Identity (Icon)"
Cohesion: 0.67
Nodes (3): Apprendimento Italiano App Icon, IT Language Monogram, Roman Arch Emblem

### Community 49 - "Italian Localization and Testing"
Cohesion: 0.67
Nodes (3): Italian Localization Guide (UI, Temples, Formats, GDPR), Ten Temples Localization Mapping (Templi I-X), Testing Protocol (Unit, Integration, Performance per Temple)

## Knowledge Gaps
- **13 isolated node(s):** `scripts/generare_tutte_le_storie.py`, `scripts/trasla_storie_dopo_b1_a2.py`, `Parla e Scrivi Raw OCR Source`, `Schema Curricular A1, A2, B1, B2 (Moduli e Unità)`, `Grammar JSON Schema (moduli, unidades, escolha, revelar)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 85 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Main Single-Page Application HTML Shell (index.html)` connect `Core App Specs and Docs` to `PWA Offline-First Architecture QA Audit Checklist`?**
  _High betweenness centrality (0.018) - this node is a cross-community bridge._
- **What connects `scripts/generare_tutte_le_storie.py`, `scripts/trasla_storie_dopo_b1_a2.py`, `Parla e Scrivi Raw OCR Source` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `json` be split into smaller, more focused modules?**
  _Cohesion score 0.1368421052631579 - nodes in this community are weakly interconnected._
- **Why does `Service Worker Registration & ControllerChange Auto-Reload` connect `PWA Offline-First Architecture QA Audit Checklist` to `Core App Specs and Docs`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._