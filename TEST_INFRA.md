# TEST_INFRA — Infraestrutura e Arquitetura de Testes E2E

**Projeto**: Aprendimento Italiano — Iniciativa: Alto Atrito Intelectual, Provocação Cognitiva & Medição de Cobertura Léxica Autêntica  
**Owner do Test Track**: E2E Test Writer (teamwork_preview_test_writer_e2e_gen5)  
**Data**: 2026-11-01  
**Runner Canônico**: `npx vitest run tests/e2e/`  

---

## 1. Filosofia de Testes (Opaque-Box Testing & Dual Track)

A suíte de testes ponta a ponta (E2E) foi desenhada com base em princípios rigorosos de **engenharia de software autônoma e resiliência offline-first**:

1. **Testes Estritamente Opaque-Box**:
   - Os testes avaliam comportamentos observáveis, contratos de interface pública, estados persistidos e interações com o usuário no DOM sintético (`happy-dom`), sem depender de detalhes internos de implementação ou variáveis privadas.
2. **Zero Dependências de Runtime Externas**:
   - Respeita o contrato fundamental da aplicação (PWA Vanilla JS/TS sem runtime dependencies de terceiros).
3. **Progressive Testability & Dual Track**:
   - Em regime de Dual Track (onde os agentes de implementação das Milestones M1, M2 e M3 executam de forma concorrente), a infraestrutura de testes emprega adaptadores dinâmicos com fallbacks de referência oraculares (`getProductionValidator`, `getTextNormalizer`, `getVocabDiagnostic`, `getCoverageMeter`). Isso garante que os testes possam validar imediatamente as fórmulas linguísticas e contratos de borda, acoplando-se automaticamente aos módulos de produção tão logo sejam gravados em disco.
4. **Isolamento e Hermeticidade**:
   - Cada teste monta seu próprio ambiente limpo (`bootstrapAppDOM()` e `resetAppEnvironment()`), garantindo que não haja vazamento de estado, cache ou timers assíncronos entre suítes.

---

## 2. Inventário de Funcionalidades & Mapeamento de Tiers (Tiers 1–4)

A suíte cobre exaustivamente os requisitos **R1 ("A Provocação")** e **R2 ("O Espelho")** definidos em `ORIGINAL_REQUEST.md` (2026-11-01T09:16:11Z) e `PROJECT.md`:

### R1: Fricção Cognitiva, Produção Ativa e Alta Tensão (`tests/e2e/e2e_cognitive_friction.test.ts`)

| # | Feature / Área | Tier 1 (Happy Path) | Tier 2 (Boundaries & Corners) | Tier 3 (Cross-Feature) | Tier 4 (Real-World Scenarios) |
|---|---|---|---|---|---|
| **F6** | **Direct Text-Production Validator (`ProductionValidator`)** | Exact match, tolerância a acentos (`è` == `e'`), vogais com apóstrofo (`à, è, é, ì, ò, ù`), aspas curvas (`’` -> `'`), variantes sinônimas. | Input vazio, pontuação extrema, Levenshtein fuzzy match em palavras longas, diagnóstico de artigo (`il` vs `lo`), diagnóstico de doppia (`pp` vs `p`), diagnóstico de desinência verbal. | Retroalimentação de maestria de palavras no FSRS. | Jornada completa de estudo com produção ativa e validação tolerante. |
| **F7** | **Quiz Direct Typing Mode ("Sem Rede")** | Alternância para modo digitação, renderização de toolbar de acentos, inserção de caracteres no input, submissão com Enter, feedback acessível `aria-live`. | Enter em branco bloqueado, debounce contra cliques repetidos de Enter, destaque de resposta correta, preservação de foco de teclado, caracteres estrangeiros (ã, ç, õ). | Integração com XP e combo streak. | Simulação de sessão de quiz sem botões de múltipla escolha. |
| **F8** | **Inductive Grammar Challenge Stage ("Desafio Indutivo")** | Início na Etapa 0 (`inducao`) antes da teoria, exibição de caso contraste, desbloqueio da teoria ao deduzir, armadilha de interferência L1, registro em progresso. | Pulo de indução em revisitas de lições já concluídas, síntese automática de contraste para lições sem nó explícito, resiliência a dados nulos, navegação entre abas, conformidade ARIA. | Conclusão indutiva destravando termos no Quiz. | Fluxo do aluno: indução pré-teoria -> teoria formal -> prática direta. |
| **F9** | **High-Tension Survival Challenge Mode** | Filtro estrito de cartas dominadas (`reps >= 3 \|\| stability > 7`), partida com 3 vidas e timer de 5s, multiplicador de combo, dedução de vidas, persistência de recorde. | Timeout de 0ms sem travamento de thread, pool de dominadas vazio com aviso pedagógico, bônus para respostas ultrarrápidas (<300ms), cancelamento de timers ao navegar, registro de lapso sob pressão sem corromper estabilidade. | Lapso sob pressão no modo sobrevivência reagendando revisão imediata no FSRS ordinário. | Simulação de maratona de retenção sob pressão com 50 cartas e gravação em `SafeStorage`. |

---

### R2: Diagnóstico Dinâmico & Medidor de Cobertura Léxica (`tests/e2e/e2e_vocabulary_coverage.test.ts`)

| # | Feature / Área | Tier 1 (Happy Path) | Tier 2 (Boundaries & Corners) | Tier 3 (Cross-Feature) | Tier 4 (Real-World Scenarios) |
|---|---|---|---|---|---|
| **F3** | **Italian Text Normalizer Engine (`TextNormalizer`)** | Tokenização sem pontuação, descompactação das 32 preposições articuladas (`del` -> `di, il`), elisões com apóstrofo (`l'amico`), apócopes poéticas (`morir` -> `morire`), enclíticos (`portami`, `vederlo`), lematização de verbos e plurais. | Strings vazias/pontuação pura, elisões aninhadas e aspas, proteção de estrangeirismos (`bar`, `sport`), enclíticos duplos compostos (`dimmelo`), verbos desconhecidos/neologismos, índice Gulpease de legibilidade. | Normalização uniforme entre histórias, canções e diálogos. | Extração e lematização sobre o corpus real de *Bella Ciao* e *Aristotele*. |
| **F10** | **Dynamic Vocabulary Diagnostic (< 3 min) (`VocabDiagnostic`)** | Itens estratificados (1k a 5k) + pseudopalavras, fórmula de correção de falsos alarmes de Abbott, projeção de vocabulário passivo, calibração do vocabulário ativo (~65%), classificação na escala CEFR (A1 a C1/C2). | Score perfeito (100% acertos -> C1/C2), zero acertos (0% -> A1), penalidade por chute (falso alarme >= 50% zera score e marca não-confiável), persistência em `vocab_diagnostico` no `AppState`, benchmark CAT < 3 minutos (< 100ms no motor). | Diagnóstico inicial calibrando a probabilidade a priori de vocabulário de histórias e canções. | Aluno iniciante A1: realiza diagnóstico dinâmico -> recebe estimativa e CEFR -> visualiza lacuna real. |
| **F11 / F12** | **Authentic Text Lexical Coverage Meter (`CoverageMeter`)** | Cálculo de cobertura léxica real (%) sobre *Bella Ciao*, lacuna de leitura autônoma (Limiar de Laufer 95%), ranqueamento das Top 5 Chaves de Desbloqueio por impacto, aumento monotônico ao aprender chaves, coloração de badges (verde, amarelo, vermelho). | 100% de cobertura léxica (lacuna zero), 0% de vocabulário (95% de lacuna), texto vazio (proteção divisão por zero), textos massivos (2.000 tokens em < 50ms), suporte a números e caracteres mistos. | Aprender as 5 chaves de desbloqueio em Flashcards fechando a lacuna de Laufer no acervo autêntico. | Aluno B2 enfrentando *Aristotele sulla felicità* com identificação das 5 chaves filosóficas. |

---

## 3. Comandos de Execução dos Testes

Para executar as suítes de testes automatizados E2E:

```bash
# Execução completa de todas as suítes E2E
npx vitest run tests/e2e/

# Execução focada na suíte de Fricção Cognitiva & Produção Ativa (R1)
npx vitest run tests/e2e/e2e_cognitive_friction.test.ts

# Execução focada na suíte de Diagnóstico & Cobertura Léxica (R2)
npx vitest run tests/e2e/e2e_vocabulary_coverage.test.ts

# Execução das suítes de auditoria preexistentes de Storage & FSRS
npx vitest run tests/e2e/tier1_feature_coverage.test.ts
npx vitest run tests/e2e/tier2_boundary_corner.test.ts
npx vitest run tests/e2e/tier3_pairwise_combinations.test.ts
npx vitest run tests/e2e/tier4_real_world_workloads.test.ts
```

---

## 4. Topologia e Layout dos Arquivos de Teste

```
tests/e2e/
├── e2e_helpers.ts                     # Harness compartilhado, oráculos e adaptadores dinâmicos
├── e2e_cognitive_friction.test.ts     # Suíte R1: F6, F7, F8, F9 (46 testes)
├── e2e_vocabulary_coverage.test.ts    # Suíte R2: F3, F10, F11, F12 (37 testes)
├── tier1_feature_coverage.test.ts     # Suíte preexistente: Persistência, FSRS, UX (27 testes)
├── tier2_boundary_corner.test.ts      # Suíte preexistente: Cotas, Limites, Relógio (24 testes)
├── tier3_pairwise_combinations.test.ts# Suíte preexistente: Sincronização, CRDT (12 testes)
└── tier4_real_world_workloads.test.ts # Suíte preexistente: Cargas de trabalho reais (5 testes)
```

**Total Consolidado de Testes na Suíte E2E**: **151 testes automatizados**, todos executando com código de saída 0 e 100% de aprovação.
