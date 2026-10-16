# Graph Report - apprendimento-italiano  (2026-10-16)

## Corpus Check
- Large corpus: 326 files · ~1,484,293 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 616 nodes · 837 edges · 87 communities (30 shown, 57 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- A1 Grammar Module Generator
- Templo Batch Fix Scripts
- Grammar Audit and Fixes
- Core App Specs and Docs
- Philosophical Stories LLM Generator
- Package Dependencies and Metadata
- Grammar Expansion Script
- Full Grammar Translation Pipeline
- Lesson Finalization Scripts
- Quota and Dyslexia Scripts
- Song Dataset Fixers (JS)
- Story Paragraph Validator
- Philosophical Story Validator
- A1 Dense Lesson Generator
- Grammar Curriculum Docs
- Pilot Lesson Applier
- Philosophical Stories Docs
- Story Batch Applier
- NMA Grammar Card Upgrader
- Templo 32-33 Generators
- Philosophical Story Merger
- Progression and Leveling System
- Quiz Dataset Definitions
- Phase HTML Render Tester
- Event Handler Checker
- 5000 Words Core Generator
- Template Application Script
- Timezone Fix Script
- Templo 22-23 Generator
- Templo 30-31 Generator
- Templo 45-47 Generator
- Templo 48-50 Generator
- App Visual Identity (Icon)
- Templo 2-3 Word Expander
- Templo 4-5 Word Expander
- Templo 6-10 Word Expander
- Extra Lesson Exercises Generator
- Lezione 1 Explanation Improver
- Lezione 2 Explanation Improver
- Lezione 4 Explanation Improver
- Lezione 5 Explanation Improver
- Lezione 6 Explanation Improver
- Lezione 7 Explanation Improver
- Lezione 8 Explanation Improver
- Lezione 9 Explanation Improver
- Italian Localization and Testing
- Dialog Dataset Fixer
- Web Audio Feedback Engine
- FSRS Spaced Repetition Flashcards
- Songs 151-200 Stanza Expander
- 5000 Words Schema Guide
- Song Expansion Logs
- 100 Songs Generator
- 100 Contexts Generator
- 100 Dialogs Generator
- 100 Imitations Generator
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
- Test Node Artifact

## God Nodes (most connected - your core abstractions)
1. `apply_content_fix()` - 11 edges
2. `main()` - 8 edges
3. `translateBatch()` - 7 edges
4. `Main Single-Page Application HTML Shell (index.html)` - 7 edges
5. `all_lessons()` - 6 edges
6. `wave4_fix_explicacao()` - 6 edges
7. `processLeicao()` - 6 edges
8. `main()` - 5 edges
9. `main()` - 5 edges
10. `Celebrity Language Learning Methods Spec (Dialoghi, Meta Prazo, Canzoni, Imitazione)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `B2 Grammar Lessons Technique Summaries (b2-i to b2-x)` --semantically_similar_to--> `Parla e Scrivi 30-Chapter Grammar JSON Spec`  [INFERRED] [semantically similar]
  info.txt → DOCUMENTACAO/INSTRUCOES_GRAMMAR_JSON.md
- `Service Worker Cache & Fetch Lifecycle Resilience` --rationale_for--> `Service Worker Registration & ControllerChange Auto-Reload`  [INFERRED]
  DOCUMENTACAO/QA_AUDIT_INSTRUCTIONS.md → index.html
- `Dyslexia Visual & Typographic Accessibility Plan` --conceptually_related_to--> `Metodologia Gramatical NMA (Pe. Napoleão Mendes de Almeida - 7 Camadas)`  [INFERRED]
  dev/plano-dislexia.md → README.md
- `Dyslexia Visual & Typographic Accessibility Plan` --rationale_for--> `Main Single-Page Application HTML Shell (index.html)`  [EXTRACTED]
  dev/plano-dislexia.md → index.html
- `Log de Execução: scripts/fix_all_vol_songs.py` --conceptually_related_to--> `Lista de Canções para Expandir (can_151 a can_200)`  [INFERRED]
  scripts/fix_log.txt → data/_songs_to_expand.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Celebrity Language Learning Methods Suite (Dialoghi, Canzoni, Imitazione, Meta Prazo)** — spec_metodo_famosos_modo_dialogo, spec_metodo_famosos_meta_com_prazo, spec_metodo_famosos_modo_canzone, spec_metodo_famosos_modo_imitacao, index_navigation_sections [EXTRACTED 1.00]
- **Grammar Module Pedagogy & Accessibility Architecture (Parla e Scrivi, NMA 7-Layer Method, Dyslexia Typography)** — documentacao_instrucoes_grammar_json_parla_e_scrivi_spec, readme_metodo_nma, dev_plano_dislexia_dyslexia_accessibility_plan, info_b2_lessons_techniques [INFERRED 0.85]
- **Documentação e Armazenamento das 21 Histórias Filosóficas** — data_final_expanso_resultado_expansao_storie_filosofia, data_reporto_storie_filosofia_relatorio_storie_filosofia, data_summary_21_storie_filosofiche_resumo_21_storie, data_final_expanso_resultado_storie_json, data_final_expanso_resultado_storie_filosofia_final_json [EXTRACTED 1.00]
- **Pipeline de Gramática e Exercícios Baseados em Parla e Scrivi** — data_parla_e_scrivi_libro_parla_e_scrivi, data_parla_e_scrivi_source_libro_parla_e_scrivi_source, data_instrucoes_adicionar_exercicios_grammar_json, data_instrucoes_adicionar_exercicios_adicionar_30_exercicios, data_instrucoes_melhorar_explicacoes_melhorar_explicacoes_grammar [INFERRED 0.95]
- **Estrutura Curricular e Técnicas A2-B1-B2** — data_schema_b2_b1_a2_curriculo_a1_b2, output_tecniche_a2, output_b1_tecniche_b1 [INFERRED 0.85]
- **App Visual Identity Elements** — icons_icon_app_icon, icons_icon_roman_arch, icons_icon_it_monogram, icons_icon_crimson_gold_palette [EXTRACTED 1.00]

## Communities (87 total, 57 thin omitted)

### Community 1 - "A1 Grammar Module Generator"
Cohesion: 0.06
Nodes (14): crea_gramma_json_completo(), cria_modulo_a1_completo(), genera_lezione_densa(), crea_gramma_json_completo(), cria_modulo_a1_completo(), genera_lezione_densa(), genera_contenuto_denso(), genera_lezione_densa() (+6 more)

### Community 2 - "Templo Batch Fix Scripts"
Cohesion: 0.05
Nodes (23): append_to_existing(), w(), append_to_existing(), w(), append_to_existing(), w(), salvar(), w() (+15 more)

### Community 3 - "Grammar Audit and Fixes"
Cohesion: 0.09
Nodes (20): all_lessons(), apply_content_fix(), by_id(), extract_inventario(), is_explicacao_placeholder(), is_placeholder_lesson(), load(), main() (+12 more)

### Community 4 - "Core App Specs and Docs"
Cohesion: 0.10
Nodes (19): Songs to Expand Dataset (can_151 to can_200), Grammar JSON Schema (moduli, unidades, escolha, revelar), Parla e Scrivi Book Source (data/parla_e_scrivi.txt), Parla e Scrivi 30-Chapter Grammar JSON Spec, PWA Offline-First Architecture QA Audit Checklist, SPA Modals & File Importers (Templo, Conquista, LevelUp, Onboarding, MetaPrazo, IAImport), SPA Navigation Sections (templi, dialoghi, canzoni, imitazione, flashcard, quiz, vocabolario, grammatica, storie, profilo), Service Worker Registration & ControllerChange Auto-Reload (+11 more)

### Community 5 - "Philosophical Stories LLM Generator"
Cohesion: 0.13
Nodes (7): call_llm_historical_prompt(), main(), generate_expanded_story(), main(), process_all_stories(), main(), traduzir()

### Community 6 - "Package Dependencies and Metadata"
Cohesion: 0.11
Nodes (19): google-translate-api-x, author, dependencies, google-translate-api-x, description, keywords, license, main (+11 more)

### Community 8 - "Grammar Expansion Script"
Cohesion: 0.14
Nodes (13): a2Novas, b1Novas, b2Novas, e(), esc(), fs, g, gramPath (+5 more)

### Community 9 - "Full Grammar Translation Pipeline"
Cohesion: 0.25
Nodes (14): cache, delay(), fs, INPUT, OUTPUT, path, processLeicao(), PROGRESS (+6 more)

### Community 11 - "Quota and Dyslexia Scripts"
Cohesion: 0.15
Nodes (8): fs, css, fs, replacements, fs, g, fs, g

### Community 12 - "Song Dataset Fixers (JS)"
Cohesion: 0.17
Nodes (9): data, dataRaw, fs, path, samples, TEMA_MAP, TEMAS, temaUsage (+1 more)

### Community 13 - "Story Paragraph Validator"
Cohesion: 0.33
Nodes (4): carregar_stories(), contar_paragrafos(), main(), validar_historia()

### Community 14 - "Philosophical Story Validator"
Cohesion: 0.31
Nodes (4): carregar_stories(), e_historia_filosofica(), main(), validar_storia()

### Community 15 - "A1 Dense Lesson Generator"
Cohesion: 0.32
Nodes (3): crea_gramma_json_completo(), crea_modulo_a1_completo(), genera_lezione_densa()

### Community 16 - "Grammar Curriculum Docs"
Cohesion: 0.32
Nodes (8): Instruções: Adicionar 30 Exercícios por Lezione (Módulo A1), data/grammar.json, Instruções: Melhorar Explicações dos Exercícios (grammar.json), Parla e Scrivi: La Lingua Italiana come L2 (Lezioni I-XXX), Parla e Scrivi Raw OCR Source, Schema Curricular A1, A2, B1, B2 (Moduli e Unità), Técnicas Comunicativas e Gramaticais B1 (b1-i a b1-xii), Técnicas Comunicativas e Gramaticais A2 (a2-i a a2-xv)

### Community 17 - "Pilot Lesson Applier"
Cohesion: 0.25
Nodes (6): fs, grammar, GRAMMAR_PATH, lez1, lez2, path

### Community 18 - "Philosophical Stories Docs"
Cohesion: 0.43
Nodes (7): Expansão das 21 Histórias Filosóficas (Resultado Final), data/storie_filosofia_final.json (Backup Store), data/storie.json (Philosophical Stories Store), scripts/generare_tutte_le_storie.py, Relatório: Expansão das 21 Histórias Filosóficas, scripts/trasla_storie_dopo_b1_a2.py, Resumo Rápido: 21 Histórias Filosóficas

### Community 19 - "Story Batch Applier"
Cohesion: 0.29
Nodes (5): batches, data, fs, path, storieFile

### Community 21 - "Templo 32-33 Generators"
Cohesion: 0.53
Nodes (4): append_to_existing(), w(), create_new(), w()

### Community 22 - "Philosophical Story Merger"
Cohesion: 0.33
Nodes (4): BASE, fs, path, STORIE_PATH

### Community 23 - "Progression and Leveling System"
Cohesion: 0.40
Nodes (3): _LEVEL_NOMES, LevelUp, Progressao

### Community 24 - "Quiz Dataset Definitions"
Cohesion: 0.40
Nodes (4): QUIZ_FAMILIA, QUIZ_NUMEROS, QUIZ_SAUDACOES, QUIZ_VERBOS

### Community 25 - "Phase HTML Render Tester"
Cohesion: 0.40
Nodes (3): errors, fs, g

### Community 26 - "Event Handler Checker"
Cohesion: 0.50
Nodes (3): files, fs, glob

### Community 29 - "Timezone Fix Script"
Cohesion: 0.50
Nodes (3): files, fs, glob

### Community 30 - "Templo 22-23 Generator"
Cohesion: 0.83
Nodes (3): append_to_existing(), create_new(), w()

### Community 31 - "Templo 30-31 Generator"
Cohesion: 0.83
Nodes (3): append_to_existing(), create_new(), w()

### Community 32 - "Templo 45-47 Generator"
Cohesion: 0.83
Nodes (3): append_to_existing(), create_new(), w()

### Community 33 - "Templo 48-50 Generator"
Cohesion: 0.83
Nodes (3): append_to_existing(), create_new(), w()

### Community 34 - "App Visual Identity (Icon)"
Cohesion: 0.67
Nodes (3): Apprendimento Italiano App Icon, IT Language Monogram, Roman Arch Emblem

### Community 49 - "Italian Localization and Testing"
Cohesion: 0.67
Nodes (3): Italian Localization Guide (UI, Temples, Formats, GDPR), Ten Temples Localization Mapping (Templi I-X), Testing Protocol (Unit, Integration, Performance per Temple)

## Knowledge Gaps
- **16 isolated node(s):** `Songs to Expand Dataset (can_151 to can_200)`, `Parla e Scrivi Book Source (data/parla_e_scrivi.txt)`, `Grammar JSON Schema (moduli, unidades, escolha, revelar)`, `Italian Localization Guide (UI, Temples, Formats, GDPR)`, `Testing Protocol (Unit, Integration, Performance per Temple)` (+11 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 326 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **57 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `google-translate-api-x` connect `Package Dependencies and Metadata` to `Full Grammar Translation Pipeline`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **What connects `Songs to Expand Dataset (can_151 to can_200)`, `Parla e Scrivi Book Source (data/parla_e_scrivi.txt)`, `Grammar JSON Schema (moduli, unidades, escolha, revelar)` to the rest of the system?**
  _16 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Grammar Lesson Diagnostics` be split into smaller, more focused modules?**
  _Cohesion score 0.02857142857142857 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `Philosophical Stories LLM Generator` to `Grammar Lesson Diagnostics`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Should `A1 Grammar Module Generator` be split into smaller, more focused modules?**
  _Cohesion score 0.05551020408163265 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `Philosophical Stories LLM Generator` to `Grammar Lesson Diagnostics`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Should `Templo Batch Fix Scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.05102040816326531 - nodes in this community are weakly interconnected._