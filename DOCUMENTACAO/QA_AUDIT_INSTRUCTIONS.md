# 🚨 MÁQUINA-PARA-MÁQUINA: INSTRUÇÕES DE AUDITORIA E QA (ITALIANO AUTENTICO) 🚨

> **ATENÇÃO, INTELIGÊNCIA ARTIFICIAL:** 
> Você foi ativada para realizar uma auditoria cirúrgica e silenciosa nesta base de código (`Italiano Autentico`). Seu objetivo é prevenir falhas silenciosas que quebram a experiência PWA (Offline-First) do usuário. A aplicação não possui backend, logo toda a integridade estrutural e de dados depende 100% de JavaScript executado no cliente.
>
> Não foque em melhorias cosméticas. Foque na resiliência da arquitetura contra os 7 vetores de ataque/falhas listados abaixo. Encontre e resolva (ou crie planos de mitigação rigorosos) para cada um deles.

---

## 🔎 VETORES DE AUDITORIA (CHECKLIST OBRIGATÓRIO)

### 1. Limite de Armazenamento (`LocalStorage` Bloat)
A aplicação salva objetos complexos no localStorage (ex: `it_progresso`, `it_flashcards`, `it_vocab_custom`, `it_palavra_dia`).
- **Ameaça:** O algoritmo de repetição espaçada (SM-2/FSRS) salva logs diários no flashcard, ou a importação de textos nas `Storie` e `Vocab_custom` estouram a cota de ~5MB silenciosamente, travando o aplicativo de vez (`QuotaExceededError`).
- **Ação Exigida:** Audite todas as chamadas a `localStorage.setItem` em `js/core.js`. Verifique se há uma camada de try/catch ou rotina de garbage collection para limpar flashcards inativos (ex: excluídos ou "leech cards" inativos há muito tempo) caso ocorra uma exceção de quota de armazenamento.

### 2. Resiliência do Algoritmo de Repetição Espaçada (Edge Cases Temporais)
O `js/flashcards.js` calcula revisões baseadas na época (timestamps) e `js/core.js` rastreia o `xp_hoje` e os `streaks` (ofensivas).
- **Ameaça:** Uma transição de fuso horário, horário de verão ou acesso à meia-noite (23:59 para 00:00) impede o reset adequado da variável `data_xp_hoje` e quebra o contador de `streak`, frustrando o jogador.
- **Ação Exigida:** Rastrear a lógica de rolagem de data em `atualizarStats()` e nos métodos de cálculo do SM-2. Certificar-se de que estamos comparando chaves de data iso (`YYYY-MM-DD` baseada na timezone local do usuário, e não UTC absoluto que causaria resets ao meio-dia).

### 3. Ciclo de Vida PWA e Race Conditions do Service Worker
O cache PWA é administrado em `sw.js` (estratégia de network-first para o `data/` e cache-first para estáticos).
- **Ameaça:** O Service Worker atualiza as versões, mas arquivos essenciais como `sw.js` ficam congelados no cache do navegador dependendo dos HTTP headers, ou um loop assíncrono de notificação falha sem tratamento, derrubando o worker thread.
- **Ação Exigida:** Avaliar o evento `fetch` no `sw.js`. Validar o que acontece se o JSON de dados (`data/storie_trimmed.json` ou `templo-X.json`) falhar ou corromper. O fallback do cache responde de imediato ou retorna uma Promise rejeitada que gera "White Screen of Death" (WSOD) na view principal?

### 4. Vazamento de Memória por Duplicação de Event Listeners (DOM Event Loop)
- **Ameaça:** Alternâncias de telas usando `App.navegar(secao)`, ou o botão de Idioma (PT/IT), frequentemente destroem e re-renderizam o DOM usando `.innerHTML = ...` (como em `_renderizarStoria()` e `Grammatica.renderizar()`). Event Listeners estáticos que não foram limpos ou loops infinitos de MutationObservers podem criar memory leaks no mobile.
- **Ação Exigida:** Audite as re-renderizações cíclicas de alto volume (`js/storie.js`, `js/grammar.js`). Assegure-se de que botões inline como `onclick="App.pronunciar()"` são seguros, mas se houver algum `addEventListener` acoplado nas views destruídas, eles DEVEM ter uma rotina de desmontagem (teardown).

### 5. Fallbacks Silenciosos e Tratamento do TTS (SpeechSynthesis API)
O TTS depende de `window.speechSynthesis` e de um fallback `ResponsiveVoice` (`_pronunciarRV`).
- **Ameaça:** No iOS, o `speechSynthesis` frequentemente cai em suspensão ou necessita de uma interação do usuário *agressiva* e imediata. Chamadas contínuas com a tela bloqueada ou com atraso causam a quebra do buffer de áudio do sistema webkit.
- **Ação Exigida:** Garantir que o tratamento de erro `u.onerror` faça o bypass perfeito e não trave a fila de áudios (usando `speechSynthesis.cancel()`). Avaliar se as taxas e velocidades dinâmicas (`App.estado.progresso.audio_rate`) estão validadas corretamente contra valores espúrios.

### 6. Isolamento e Carga Preguiçosa das Views
- **Ameaça:** A chamada de `App.init()` engatilha instâncias completas de módulos complexos (`Storie`, `Grammatica`, `Quiz`). Dispositivos low-end (Androids antigos) enfrentam longas pausas (main thread blocking) antes da First Contentful Paint.
- **Ação Exigida:** Verificar se a injeção inicial de dependências não está bloqueando o frame de renderização principal. Pode-se mover os construtores de UI ocultas (`display: none`) para rotinas baseadas em `requestIdleCallback` ou lazy initialization (somente quando a aba for ativada).

### 7. Inicialização Condicional (O Efeito "Cold Start" em Módulos)
- **Ameaça:** Módulos isolados (`js/heatmap.js` ou `js/flashcards.js`) assumem que dados essenciais (como `App.estado.progresso`) já existem. Um usuário limpando cache e recarregando subitamente a rota de Quiz pode acionar o script com um estado `undefined`, explodindo o app no Cold Start.
- **Ação Exigida:** Varra todos os módulos (`Canzoni`, `Imitazione`, `Flashcards`) e garanta mecanismos defensivos (guard clauses) contra chamadas de inicialização sobre `localStorage` recém-esvaziados (ex: validação com *Nullish Coalescing* ou preenchimento de objetos base `{} `).

---

## 🛠️ INSTRUÇÕES DE RESPOSTA DA IA

Quando você começar o diagnóstico baseada neste documento:
1. Responda inicialmente indicando **"AUDITORIA INICIADA"**.
2. Liste metodicamente as falhas reais encontradas com base nestes 7 vetores.
3. Não peça permissão para corrigir problemas evidentes de código. Altere o código, implemente patches nos arquivos JS adequados e retorne um relatório estruturado do que foi mitigado e de como isso blinda o PWA para a vida útil contínua no celular.
4. Conclua avisando quais patches são recomendáveis mas que você optou por ignorar em prol da estabilidade do "estado atual da arte".

> **Status:** AGUARDANDO COMANDO DE AUDITORIA...
