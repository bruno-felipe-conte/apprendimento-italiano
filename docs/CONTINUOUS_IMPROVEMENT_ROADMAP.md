# 🚀 Continuous Improvement Roadmap — Aprendimento Italiano

Este documento estabelece o roteiro estratégico de evolução contínua para o aplicativo **Aprendimento Italiano**, baseado na auditoria profunda de estresse, concorrência e experiência do usuário (UX) executada pelo sistema multi-agente.

---

## 1. Visão Geral da Arquitetura & Diretrizes de Qualidade
O aplicativo opera como um PWA moderno de alto desempenho, **zero runtime dependencies** (exceto Zod para validação de schemas em tempo de desenvolvimento/build), offline-first com persistência híbrida (`SafeStorage` / `IndexedDB`), e motor de repetição espaçada de última geração baseado no algoritmo **FSRS-5 / FSRS-4.5**.

---

## 2. Roteiro de Marcos e Evolução Contínua

### 🎯 Fase I: Estabilização de Bordas e Integridade Concorrente (Concluída)
- [x] **SafeStorage Gateway**: Fachada com detecção universal de `QuotaExceededError` (Safari, Firefox, Chrome, Edge/IE) e escada hierárquica de evicção (descarte de caches voláteis SWR antes de tocar em dados essenciais).
- [x] **Sincronização Multi-Aba via BroadcastChannel**: Reconciliação comutativa inspirada em CRDTs de `it_progresso` e `it_flashcards`, evitando sobrescrita LWW (*Last-Write-Wins*) acidental entre abas concorrentes.
- [x] **Importação Transacional & Sanitização**: Staging atômico com rollback automático e sanitização rigorosa contra injeções XSS em músicas e diálogos customizados.
- [x] **Blindagem Matemática do FSRS**: Imunização de fórmulas contra `NaN`, `Infinity` e descompassos temporais do relógio do dispositivo (*monotonic clock skew*).
- [x] **Ciclo de Vida de Áudio / TTS**: Teardown centralizado em `AppNavigation.navegar()` para interromper imediatamente sintetizadores Web Speech, workers neurais (VoiceEngine) e gravação de microfone ao trocar de seção.

---

### 🎨 Fase II: Ergonomia, Acessibilidade e Fluidez de Estudo (UX/PWA)
- [x] **Resolução de Conflitos de Teclado**: O listener global de navegação (`1-5`) agora respeita estados de modal e sessões ativas de flashcard/quiz.
- [x] **Acessibilidade no Quiz**: Suporte nativo a teclas numéricas `1-4` para escolha de alternativas e `Enter`/`Espaço` para avanço, com anúncios em `aria-live="polite"` e auto-foco na continuação.
- [x] **Semântica e Teclado no Flashcard**: `#flashcard` com `role="button"`, `tabindex="0"` e suporte a virar via `Espaço` e `Enter`.
- [x] **Tamanho Mínimo de Alvos de Toque (WCAG 2.1 SC 2.5.5 / 2.5.8)**: Botões utilitários no cabeçalho mobile, alternadores de modo e abas da barra inferior com dimensões mínimas de 44×44px.
- [x] **Prevenção de Bounce/Pull-to-Refresh em PWA**: Adição de `overscroll-behavior: contain !important` em todas as gavetas e contêineres de rolagem interna (`.tm-card`, `.ia-import-box`, etc.).
- [x] **Pacing Cognitivo & Micro-Pausas**: Alerta sutil após 20 revisões contínuas recomendando pausa de 60 segundos para consolidação na memória de longo prazo.
- [x] **Contraste em Modo Escuro**: Anéis de foco `:focus-visible` em `body.dark-mode` com contraste >= 3:1 (`#D4A843`).

---

### 🔮 Fase III: Próximos Passos Recomendados (Backlog Estratégico)

#### 1. Tipografia para Dislexia & Legibilidade Dinâmica
- **Meta**: Integrar a fonte `Atkinson Hyperlegible` como alternativa de acessibilidade selecionável no menu de Configurações / Perfil, conforme delineado em `dev/plano-dislexia.md`.
- **Impacto**: Redução imediata da fadiga de leitura para estudantes com dislexia ou dificuldades visuais.

#### 2. Pipeline de CI Automatizado com Acessibilidade Headless
- **Meta**: Integrar testes de regressão de acessibilidade (`axe-core`) diretamente na suíte Vitest / Happy-DOM, eliminando a dependência de pacotes binários do sistema operacional para verificação de WCAG.
- **Impacto**: Garantia de 0 violações de acessibilidade em cada commit.

#### 3. Sincronização em Nuvem Peer-to-Peer / WebDAV Opcional
- **Meta**: Oferecer sincronização criptografada ponta a ponta (E2EE) opcional via WebDAV pessoal (Nextcloud) ou Google Drive do próprio usuário, sem a necessidade de manter servidores backend proprietários.
- **Impacto**: Manutenção do modelo de privacidade radical com backup transparente entre dispositivos.

#### 4. Otimização de Pacote de Voz Neural (WebAssembly Piper)
- **Meta**: Carregamento sob demanda (*lazy-loading*) dos modelos ONNX do sintetizador neural apenas quando o usuário optar pela voz neural italiana de alta qualidade.
- **Impacto**: Economia de banda em redes móveis e inicialização ultrarrápida no primeiro acesso.

---

*Documento mantido e auditado pelo ecossistema de engenharia do Aprendimento Italiano.*
