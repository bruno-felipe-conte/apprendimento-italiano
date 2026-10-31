# Relatório de Diagnóstico e Auditoria — Explorador 2
**Domínio**: Algoritmos de Repetição Espaçada (FSRS / Ebbinghaus), Casos de Borda Matemáticos e Temporais, Ciclo de Vida de Áudio/TTS e Condições de Corrida de Concorrência.

---

## 1. Observation

Durante a investigação estrita e somente-leitura da base de código em `/mnt/c/Users/bruno/Documents/apprendimento-italiano`, foram observados os seguintes fatos concretos:

### 1.1 Algoritmos FSRS e Curva de Ebbinghaus
- **FSRS-4.5 em `js/flashcards.js` (linhas 7–122)**:
  - Linhas 19–22:
    ```javascript
    retrievability(t, s) {
      if (s <= 0 || t < 0) return 1;
      return Math.pow(1 + this.FACTOR * t / s, this.DECAY);
    },
    ```
  - Linhas 25–28:
    ```javascript
    nextInterval(s) {
      const t = s * (Math.pow(this.TARGET_R, 1 / this.DECAY) - 1) / this.FACTOR;
      return Math.max(Math.round(t), 1);
    },
    ```
  - Linhas 42–49:
    ```javascript
    nextDifficulty(d, rating) {
      const d0easy = this.initDifficulty(4); // ~3.28 — Easy baseline
      const delta  = -this.w[6] * (rating - 3);
      const raw    = d + delta;
      const next   = this.w[7] * d0easy + (1 - this.w[7]) * raw;
      return Math.min(Math.max(next, 1), 10);
    },
    ```
  - Linhas 52–62:
    ```javascript
    nextRecallStability(d, s, r, rating) {
      if (s <= 0) return this.initStability(rating);
      const hardPenalty = rating === 2 ? this.w[15] : 1;
      const easyBonus   = rating === 4 ? this.w[16] : 1;
      const increment   = Math.exp(this.w[8]) *
                          (11 - d) *
                          Math.pow(s, -this.w[9]) *
                          (Math.exp(this.w[10] * (1 - r)) - 1) *
                          hardPenalty * easyBonus;
      return s * (increment + 1);
    },
    ```
  - Linhas 65–70:
    ```javascript
    nextForgetStability(d, s, r) {
      return this.w[11] *
             Math.pow(d, -this.w[12]) *
             (Math.pow(s + 1, this.w[13]) - 1) *
             Math.exp(this.w[14] * (1 - r));
    },
    ```
  - Linhas 73–121:
    `review(card, rating)` atualiza `lastReview: now` e `nextReview: now + intervalDay * 86400000`.

- **Projeção de Ebbinghaus em `src/analytics/ebbinghausCurve.ts` e `js/ebbinghaus.js`**:
  - `src/analytics/ebbinghausCurve.ts` linhas 201–218 e `js/ebbinghaus.js` linhas 125–137:
    ```typescript
    function getElapsedDays(card: FSRSCardInput | null | undefined): number | null {
      if (!card || card.last_review == null) return null;
      const lr = card.last_review;
      let timeMs: number;
      if (typeof lr === 'number') timeMs = lr;
      else if (lr instanceof Date) timeMs = lr.getTime();
      else if (typeof lr === 'string') timeMs = new Date(lr).getTime();
      else return null;
      if (Number.isNaN(timeMs) || timeMs <= 0) return null;
      const diffMs = Date.now() - timeMs;
      return Math.max(0, diffMs / 86400000);
    }
    ```
  - `js/flashcards.js` salva a propriedade como `lastReview` (camelCase, linhas 75, 117), enquanto `getElapsedDays` verifica apenas `card.last_review` (snake_case).
  - Em `computeEbbinghausCurve`:
    ```typescript
    const elapsed = getElapsedDays(activeCard);
    const cardR = elapsed !== null ? retentionAt(elapsed, sAtual) : retentionTarget;
    ```
    Como `card.last_review` é `undefined`, `elapsed` é sempre `null`, fixando `cardR` artificialmente no valor estático `retentionTarget` (0.90).

- **Validação e Isolamento de Script em `scripts/validate-fsrs.js`**:
  - A função `validarCardFSRS(id, card)` existe apenas em `scripts/validate-fsrs.js`.
  - Em tempo de execução (`js/core/state.js` linhas 158–164), `carregarFlashcards()` faz apenas `JSON.parse(raw)` sem qualquer sanitização ou validação de limites (`difficulty` entre 1 e 10, `stability` finita e > 0).

### 1.2 Casos de Borda Matemáticos e Temporais
- **Propagação Contagiosa de `NaN`**:
  Em JavaScript:
  `Math.min(Math.max(NaN, 1), 10) === NaN`.
  Se `d` for `NaN` ou `undefined`, `nextDifficulty` retorna `NaN`.
  Em `nextRecallStability`, `11 - NaN = NaN`, resultando em `increment = NaN` e `newS = NaN`.
  `Math.max(NaN, 0.1) === NaN`.
  O card torna-se irreversivelmente corrompido com `difficulty: NaN`, `stability: NaN`, `interval: NaN`, `nextReview: NaN`.
- **Estabilidade e Intervalo Infinitos (`stability -> Infinity`)**:
  Nem `nextRecallStability` nem `nextInterval` possuem teto superior (clamp máximo, ex: 36500 dias / 100 anos).
  Se `s` se torna `Infinity`, `nextInterval` é `Infinity`, e `nextReview` torna-se `Infinity`.
  Em JavaScript, `JSON.stringify({ nextReview: Infinity })` produz `{"nextReview":null}`.
  A data de revisão do card é corrompida silenciosamente para `null`.
- **Descompasso de Fuso Horário e Rolagem de Data**:
  - `js/progression.ts` linha 298:
    `const k = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);`
  - `js/heatmap.js` linha 27:
    `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`
  - A manipulação manual de `getTimezoneOffset()` em `progression.ts` durante transições de horário de verão (DST) ou fusos negativos pode desfasar a data em ±1 dia em relação à chave do diário gerada pelo `Calor._dataLocal()`.
- **Avaliações com Timestamps Passados (Relógio Atrasado / Desincronizado)**:
  Se o relógio do dispositivo for atrasado ou se o card foi revisado em outro dispositivo com relógio adiantado, `card.lastReview > now`, gerando `tDays < 0`.
  `retrievability(t, s)` retorna 1, mas o novo registro histórico recebe `timestamp: now < card.lastReview`, quebrando a monotonicidade temporal do histórico.

### 1.3 Ciclo de Vida de Áudio / TTS / Web Speech API
- **Rejeição de Promessa Não Tratada em `js/imitazione.js` (linha 274)**:
  ```javascript
  tocarMinhaGravacao() {
    if (!this._userAudioUrl) return;
    if (this._userAudioPlayer) {
      this._userAudioPlayer.pause();
      this._userAudioPlayer.currentTime = 0;
    }
    this._userAudioPlayer = new Audio(this._userAudioUrl);
    this._userAudioPlayer.play(); // SEM .catch()!
  }
  ```
  Se o usuário clica rapidamente no botão, pausa ou se as políticas de autoplay do navegador bloqueiam, `play()` retorna uma Promise rejeitada (`AbortError` ou `NotAllowedError`), gerando `UnhandledPromiseRejection`.
- **Áudio / TTS Órfão durante Troca de Abas em `js/core/navigation.js` (linhas 61–65)**:
  `AppNavigation.navegar(secao)` só pausa áudio se a aba de destino não for `canzoni`:
  ```javascript
  if (secao !== 'canzoni' && typeof Canzoni !== 'undefined' && Canzoni.tocandoKaraoke) {
    Canzoni.pararAudio();
  }
  ```
  Não há chamadas para:
  - `VoiceEngine.parar()`
  - `speechSynthesis.cancel()`
  - `Storie._pararAudioPagina()`
  - `Imitazione.pararGravacao()`
  Ao navegar de Histórias para Flashcards ou Quiz durante a leitura de uma página, o TTS continua falando ininterruptamente as sentenças em segundo plano.
- **`VoiceEngine.parar()` não cancela sínteses pendentes do Web Worker**:
  Em `js/voice_engine.ts` linhas 424–440, `parar()` não limpa `_pendingSyntheses`. Se a inferência do worker responder após o cancelamento, a promessa é resolvida e o buffer é reproduzido via `_tocarBuffer()`.
- **`u.onerror` aciona `onend` em cancelamento explícito no `VoiceEngine`**:
  Em `js/voice_engine.ts` linhas 586–596:
  Quando `speechSynthesis.cancel()` é chamado, o navegador gera `u.onerror` com `err.error === 'canceled'`. O motor executa:
  `if (opcoes.onend) setTimeout(opcoes.onend, 800);`
  Isso causa avanço espúrio de sentenças ou cards mesmo após o cancelamento intencional do usuário.
- **Truncação de Voz por Garbage Collection do Navegador em `vocab.js` e `canzoni.js`**:
  Em `js/vocab.js` linha 498 e `js/canzoni.js` linhas 704 e 2299, objetos `SpeechSynthesisUtterance` são instanciados em escopo de função local sem referência em `window._activeUtterance`, sofrendo coleta prematura pelo garbage collector do motor V8/Chromium.

### 1.4 Condições de Corrida de Concorrência e Transições de Tela
- **Colisão Global de Teclas de Atalho entre `js/core.js` e `js/flashcards.js`**:
  - `js/core.js` linhas 162–166:
    ```javascript
    document.addEventListener('keydown', (e) => {
      if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)) return;
      const mapa = { '1': 'templi', '2': 'flashcard', '3': 'quiz', '4': 'vocabolario', '5': 'grammatica' };
      if (mapa[e.key]) this.navegar(mapa[e.key]);
    });
    ```
  - `js/flashcards.js` linhas 1704–1710:
    ```javascript
    if (Flashcards.virada) {
      if (key === '1') { e.preventDefault(); Flashcards.avaliar(1); return; }
      if (key === '2') { e.preventDefault(); Flashcards.avaliar(2); return; }
      if (key === '3') { e.preventDefault(); Flashcards.avaliar(3); return; }
      if (key === '4') { e.preventDefault(); Flashcards.avaliar(4); return; }
    }
    ```
  - `e.preventDefault()` não interrompe a propagação de eventos no DOM (`stopImmediatePropagation()` não foi chamado).
  - Além disso, o listener do `core.js` não verifica `e.defaultPrevented` nem se a seção ativa é `sec-flashcard`.
  - **Efeito imediato**: quando o usuário pressiona `1` (Again), `3` (Good) ou `4` (Easy) para avaliar um card virado, o listener do documento captura a tecla e **navega imediatamente para outra aba** (`templi`, `quiz` ou `vocabolario`), abortando o estudo do card!
- **Ausência de Guard de Bloqueio na Entrada de `Flashcards.avaliar(rating)`**:
  - Em `js/flashcards.js` linhas 907–909:
    `avaliar(rating) { if (!this.cartaAtual) return; ... }`
    Não há checagem `if (this._bloqueioAvaliacao) return;`.
  - Gestos de swipe (linhas 1334–1337) ou cliques duplos rápidos disparam `avaliar()` duas vezes para o mesmo card.
  - A segunda chamada avalia o card já atualizado, duplica XP, recalcula intervalos de forma errônea e agenda dois timeouts de `setTimeout(() => this.proxima(), 650)`.
  - Quando os dois timers disparam, `proxima()` é executado duas vezes, **pulando o próximo card da fila sem que o usuário o veja**.
- **Duplo Clique no Botão "Continuar" do Quiz (`js/quiz.js`)**:
  - Em `js/quiz.js` linhas 311–319 e `index.html` linha 418:
    O botão `<button class="btn-primario" onclick="Quiz.proximaPergunta()" data-i18n="quiz_continuar">Continuar →</button>` não possui debounce nem desativação imediata.
    - Se clicado rapidamente duas vezes durante as perguntas, pula a pergunta seguinte (`this.perguntaAtual++` duas vezes).
    - Se clicado duas vezes na última pergunta, dispara `mostrarResultado()` duas vezes.
    - Como `mostrarResultado()` (linhas 377–379) executa `if (this.xpTotal > 0) Progressao.ganhar(this.xpTotal);`, o usuário **recebe XP dobrado** e gera registros duplicados em `it_quiz_historico`.

### 1.5 Estado dos Testes Existentes
- A suíte atual possui 104 testes passando em 15 arquivos (`vitest run` executa com sucesso em ~19.6s).
- Lacuna Crítica 1: Não há nenhum teste unitário para `FSRS.review()` ou suas fórmulas matemáticas sob entradas corrompidas (`NaN`, `Infinity`, números negativos, `lastReview` futuro).
- Lacuna Crítica 2: Os testes de Ebbinghaus (`tests/ebbinghausCurve.test.ts`) utilizam mocks artificiais com `last_review` (snake_case), mascarando o fato de que a aplicação em produção gera `lastReview` (camelCase).
- Lacuna Crítica 3: Não há testes automatizados para concorrência de cliques duplos rápidos, atalhos de teclado colidentes ou cancelamento de áudio/TTS em trocas de tela.

---

## 2. Logic Chain

A partir das observações documentadas, estruturamos a seguinte cadeia de causalidade e diagnóstico:

1. **Cadeia de Corrupção Algorítmica**:
   - `carregarFlashcards` em `state.js:161` não sanitiza dados $\rightarrow$ payload corrompido ou importado com `difficulty: null` ou `stability: NaN` é carregado no estado em memória $\rightarrow$ `FSRS.review()` recebe dados não finitos $\rightarrow$ `nextDifficulty` e `nextRecallStability` operam sobre `NaN` $\rightarrow$ JavaScript propaga `NaN` em todas as operações aritméticas subsequentes $\rightarrow$ `Math.max(NaN, 0.1)` resulta em `NaN` $\rightarrow$ `interval` e `nextReview` tornam-se `NaN` $\rightarrow$ ao serializar via `salvarFlashcards`, o card corrompe a fila diária de revisões.

2. **Cadeia de Falha na Curva de Ebbinghaus**:
   - `Flashcards.review` gera e salva `{ lastReview: timestamp }` em `flashcards.js:117` $\rightarrow$ `Ebbinghaus.renderEbbinghausCurve` consome os cards de `App.estado.flashcardData` $\rightarrow$ `getElapsedDays` em `ebbinghausCurve.ts:202` busca exclusivamente `card.last_review` $\rightarrow$ `card.last_review` é `undefined` $\rightarrow$ `getElapsedDays` retorna `null` $\rightarrow$ `cardR` cai no fallback padrão `retentionTarget` (0.90) $\rightarrow$ o cálculo de projeção após 'Bom' (`predictNextStabilityGood`) nunca reflete os dias decorridos reais nem a urgência da revisão.

3. **Cadeia de Conflito de Atalhos de Teclado (Race Condition)**:
   - Usuário abre Flashcards e clica na carta para virá-la (`Flashcards.virada === true`) $\rightarrow$ usuário aperta tecla `3` para selecionar a resposta 'Good' $\rightarrow$ o listener em `flashcards.js:1708` intercepta `key === '3'`, executa `e.preventDefault()` e chama `Flashcards.avaliar(3)` $\rightarrow$ o evento continua borbulhando até o listener global em `core.js:162` $\rightarrow$ `core.js` não verifica `e.defaultPrevented` e localiza `'3': 'quiz'` no mapa de navegação $\rightarrow$ `App.navegar('quiz')` é disparado imediatamente $\rightarrow$ o usuário é arrancado do modo Flashcard e jogado na tela de Quiz enquanto o timeout de 650ms do Flashcard ainda está correndo em segundo plano.

4. **Cadeia de Avanço Duplo e Perda de Cards**:
   - Usuário avalia um card via clique ou swipe rápido $\rightarrow$ `avaliar()` inicia sem checagem de reentrância $\rightarrow$ evento simultâneo dispara `avaliar()` novamente $\rightarrow$ `_bloqueioAvaliacao = true` é atribuído na 1ª chamada, mas a 2ª chamada já entrou na função $\rightarrow$ dois `setTimeout(..., 650)` são registrados com referências a `this.proxima()` $\rightarrow$ o primeiro timeout avança `indiceAtual` de $N$ para $N+1$ $\rightarrow$ o segundo timeout avança `indiceAtual` de $N+1$ para $N+2$ $\rightarrow$ a carta $N+1$ é ignorada sem que o estudante tenha a oportunidade de responder.

5. **Cadeia de Vazamento de Áudio e Exceções no Console**:
   - Usuário inicia reprodução de história em `Storie` ou gravação em `Imitazione` $\rightarrow$ usuário clica em outra aba no menu inferior $\rightarrow$ `AppNavigation.navegar()` altera as classes do DOM, mas não cancela `speechSynthesis` nem suspende `VoiceEngine` ou gravação de microfone $\rightarrow$ síntese de voz continua falando sobre a nova seção $\rightarrow$ ao concluir ou falhar após navegação, callbacks assíncronos (`u.onend`, `u.onerror`) tentam acessar elementos DOM já desmontados ou re-renderizados $\rightarrow$ em `Imitazione.tocarMinhaGravacao()`, interrupção sem `.catch()` gera `UnhandledPromiseRejection`.

---

## 3. Caveats

- **Ambiente de Testes headless (Happy-DOM / Vitest)**: O ambiente de execução dos testes não implementa a pilha nativa completa de áudio Web Audio / Web Speech API (como `AudioContext.decodeAudioData` ou drivers de voz reais do sistema operacional). Mocking rigoroso é necessário para reproduzir as interrupções de hardware reais de navegadores móveis (Safari iOS e Chrome Android).
- **Dados Históricos em Produção**: Usuários com histórico salvo em `localStorage` podem já possuir cards com propriedades legadas (`intervalo`, `repeticoes`, `facilidade`, ou `lastReview`). Qualquer correção deve manter estrita retrocompatibilidade bidirecional e tolerância a propriedades ausentes.
- **Não Interferência em Outras Camadas**: Este diagnóstico foca nos requisitos algorítmicos, temporais, de áudio e concorrência (R1/R3/R4). Problemas exclusivos de layout CSS puro ou quota de armazenamento estão no escopo dos agentes irmãos.

---

## 4. Conclusion & Proposed Fix Strategy

### 4.1 Resumo Diagnóstico
Foram mapeadas 10 falhas críticas e médias no domínio de algoritmos, matemática, áudio e concorrência:
1. **Falta de sanitização e clamp no FSRS**: Suscetibilidade a `NaN`, `Infinity` e valores negativos.
2. **Inconsistência de chave temporal**: `lastReview` (camelCase) no motor de flashcards vs `last_review` (snake_case) no motor da Curva de Ebbinghaus.
3. **Colisão de teclado destrutiva**: Pressionar teclas `1`–`4` em Flashcards aciona simultaneamente a navegação global de `core.js`.
4. **Ausência de guard de reentrância em `Flashcards.avaliar`**: Pulo acidental de cards e contagem dobrada de XP em cliques ou swipes rápidos.
5. **Falta de debounce no botão Continuar do Quiz**: Pulo de perguntas e premiação duplicada de XP no encerramento.
6. **Vazamento de reprodução de voz e microfone entre abas**: Ausência de teardown de áudio em `AppNavigation.navegar()`.
7. **Rejeição de promessa não tratada em áudio**: `_userAudioPlayer.play()` em `imitazione.js` sem `.catch()`.
8. **Síntese órfã pós-cancelamento em `VoiceEngine`**: Resolução de promessas do Worker após chamada de `parar()`.
9. **Callback espúrio em cancelamento**: `VoiceEngine.u.onerror` agendando `opcoes.onend` quando `error === 'canceled'`.
10. **Truncação de áudio por GC**: Utterances sem ancoragem global em `vocab.js` e `canzoni.js`.

### 4.2 Proposta de Correção Estruturada (Fix Strategy)

1. **Blindagem Matemática do FSRS (`js/flashcards.js`)**:
   - Criar sanitizador universal em `FSRS.sanitizeCard(card)` garantindo:
     - `difficulty`: número finito clampado em `[1.0, 10.0]` (fallback: 5.0).
     - `stability`: número finito clampado em `[0.1, 36500.0]` (fallback: 2.0).
     - `reps` e `lapses`: inteiros $\ge 0$.
     - `retrievability`: clampado em `[0.0, 1.0]`.
     - `nextInterval`: inteiro clampado em `[1, 36500]`.
   - Inserir validação preventiva em `review(card, rating)` e no carregamento em `state.js:carregarFlashcards()`.
   - Garantir que se `card.lastReview > now`, $t$ seja tratado como 0 (evitando retrievability espúria e mantendo monotonicidade no log histórico).

2. **Harmonização Temporal da Curva de Ebbinghaus (`src/analytics/ebbinghausCurve.ts` e `js/ebbinghaus.js`)**:
   - Atualizar `getElapsedDays`:
     ```javascript
     const lr = card.lastReview ?? card.last_review ?? card.ultima_revisao;
     ```
   - Normalizar a chave em ambos os módulos TypeScript e JavaScript.

3. **Resolução da Concorrência de Atalhos de Teclado (`js/core.js` e `js/flashcards.js`)**:
   - Em `js/core.js`:
     ```javascript
     document.addEventListener('keydown', (e) => {
       if (e.defaultPrevented) return;
       if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)) return;
       const estado = App.estado?.secaoAtiva;
       if (estado === 'flashcard') return; // Preserva atalhos FSRS de avaliação
       const mapa = { '1': 'templi', '2': 'flashcard', '3': 'quiz', '4': 'vocabolario', '5': 'grammatica' };
       if (mapa[e.key]) this.navegar(mapa[e.key]);
     });
     ```
   - Em `js/flashcards.js`: adicionar `e.stopImmediatePropagation()` ao interceptar teclas `1` a `4`.

4. **Blindagem Contra Cliques Rápidos / Reentrância**:
   - Em `Flashcards.avaliar(rating)`:
     Adicionar guard inicial: `if (this._bloqueioAvaliacao || !this.cartaAtual) return;`.
     Cancelar qualquer timer de transição pendente (`clearTimeout(this._timerProxima)`) antes de agendar novo avanço.
   - Em `Quiz.proximaPergunta()`:
     Adicionar flag de bloqueio transitório (`if (this._bloqueioAvanco) return;`) e desativar temporariamente o botão "Continuar" até a nova tela renderizar.
     Em `mostrarResultado()`: adicionar guard `if (this._resultadoExibido) return;` para impedir entrega de XP duplicado.

5. **Auditoria e Teardown de Áudio em Navegação (`js/core/navigation.js` e `js/imitazione.js`)**:
   - Em `AppNavigation.navegar(secao)`:
     Adicionar rotina centralizada de encerramento de áudio:
     ```javascript
     if (typeof VoiceEngine !== 'undefined') VoiceEngine.parar();
     if (typeof Storie !== 'undefined' && Storie._pararAudioPagina) Storie._pararAudioPagina();
     if (typeof Imitazione !== 'undefined' && Imitazione.pararGravacao) Imitazione.pararGravacao();
     if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
       try { window.speechSynthesis.cancel(); } catch (_) {}
     }
     ```
   - Em `js/imitazione.js:tocarMinhaGravacao`:
     ```javascript
     this._userAudioPlayer.play().catch(err => {
       console.info('[Imitazione] Reprodução cancelada ou bloqueada:', err);
     });
     ```
   - Em `js/voice_engine.ts`:
     - Em `parar()`, incrementar um `_synthesisSessionId` para invalidar promessas de áudio pendentes em voo.
     - Em `u.onerror`, ignorar e NÃO agendar `onend` quando `err.error === 'canceled'`.

---

## 5. Verification Method

Para verificar de forma independente e automatizada todos os diagnósticos levantados:

### 5.1 Comandos de Execução
1. Executar a suíte de testes atual:
   ```bash
   npx vitest run
   ```
2. Executar validação de cards legados:
   ```bash
   npm run fsrs:validate
   ```
3. Compilar os arquivos TypeScript:
   ```bash
   npm run build:ts
   ```
4. Executar verificação de tipos:
   ```bash
   npm run typecheck
   ```

### 5.2 Recomendações de Novos Testes Automatizados (A Implementar na Fase de Resolução)
1. **`tests/fsrs_math_stress.test.ts`**:
   - Testar `FSRS.review()` com `difficulty = NaN`, `stability = 0`, `stability = -1`, `stability = Infinity`.
   - Testar avalanche de revisões repetidas (1000 reviews consecutivos 'Easy') verificando se `stability` e `interval` permanecem $\le 36500$ e livres de `Infinity`/`NaN`.
   - Testar review com `lastReview` no futuro (clock skew de -30 dias) e com salto temporal de +10 anos.
2. **`tests/audio_concurrency.test.ts`**:
   - Testar `AppNavigation.navegar()` garantindo que chamadas em voo de `Storie._ouvirPaginaAtual()` e `VoiceEngine` são interrompidas.
   - Testar cancelamento de `VoiceEngine.falar()` verificando que `onend` NÃO é acionado com erro `'canceled'`.
   - Testar `Imitazione.tocarMinhaGravacao()` simulando rejeição de `play()` sem lançar erro global.
3. **`tests/keyboard_concurrency.test.ts`**:
   - Simular evento `keydown` da tecla `'3'` com `sec-flashcard` ativo e verificar que `App.estado.secaoAtiva` permanece `'flashcard'` e não muda para `'quiz'`.
   - Simular duplo clique em `Quiz.proximaPergunta()` e verificar que o XP total só é concedido uma única vez.
