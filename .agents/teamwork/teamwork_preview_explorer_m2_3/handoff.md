# Handoff Report: M2.3 Audio/TTS & Navigation Robustness

**Agent**: Explorer M2.3 (`teamwork_preview_explorer_m2_3`)  
**Scope**: Milestone 2 — Audio lifecycle teardown, promise rejection safety, worker synthesis invalidation, utterance GC anchoring.  
**Mode**: Read-only Investigation & Exact Fix Design.

---

## 1. Observation

Direct code inspections of the target files revealed the following concrete vulnerabilities and omissions:

### 1.1 Section Navigation Audio/TTS Teardown (`js/core/navigation.js:61-64`)
In `AppNavigation.navegar(secao)`:
```javascript
// Lines 61-64 of js/core/navigation.js
// Pausa karaokê se sair da aba de músicas
if (secao !== 'canzoni' && typeof Canzoni !== 'undefined' && Canzoni.tocandoKaraoke) {
  Canzoni.pararAudio();
}
```
**Defects observed**:
1. Only `Canzoni` karaoke is halted, and only if `Canzoni.tocandoKaraoke` is truthy. Any other audio in Canzoni (e.g., cloze preview or real audio playback) is bypassed if `tocandoKaraoke` is false.
2. `VoiceEngine.parar()` is never invoked on section switch. Active Web Audio DSP buffers and neural speech continue playing.
3. Native `speechSynthesis.cancel()` is never called on section switch, leaving active phrases (e.g. from Flashcards, Vocabolario, or Dialoghi) speaking across unrelated screens.
4. `Storie._pararAudioPagina()` is never called when navigating away from the `storie` section. Because Storie uses a queued loop (`_tocarProximaSentenca()`), an entire book or chapter continues reading sequentially in the background across all other app views.
5. `Imitazione.pararGravacao()` is not called when leaving `imitazione`. An active `MediaRecorder` or `SpeechRecognition` session remains active, leaving the browser microphone hardware indicator on and holding active streams.
6. `Flashcards` voice recording (`Flashcards.gravando`, `_recognition`) is not stopped when navigating away from `flashcard`.

### 1.2 Unhandled Promise Rejection in `js/imitazione.js` (`_userAudioPlayer.play()`, lines 267-275)
In `Imitazione.tocarMinhaGravacao()`:
```javascript
// Lines 267-275 of js/imitazione.js
tocarMinhaGravacao() {
  if (!this._userAudioUrl) return;
  if (this._userAudioPlayer) {
    this._userAudioPlayer.pause();
    this._userAudioPlayer.currentTime = 0;
  }
  this._userAudioPlayer = new Audio(this._userAudioUrl);
  this._userAudioPlayer.play();
},
```
**Defects observed**:
1. `HTMLMediaElement.prototype.play()` returns a `Promise<void>`.
2. Calling `play()` without `.catch()` causes an unhandled promise rejection whenever the browser blocks autoplay (`NotAllowedError`), interrupts playback because `pause()` was called immediately afterward (`AbortError`), or fails to decode the recorded media blob (`NotSupportedError`).
3. Calling `this._userAudioPlayer.pause()` at line 270 on an audio player with an in-flight `play()` request causes that previous play promise to reject with `AbortError: The play() request was interrupted by a call to pause()`, which is unhandled.
4. In `_pararGravacaoMidia()` (lines 258-265), `this._mediaStream` track shutdown is deferred only to `_mediaRecorder.onstop`. If `pararGravacao()` is invoked while recording, `_mediaStream` tracks are not immediately and synchronously stopped, risking persistent microphone access.

### 1.3 `VoiceEngine.parar()` Worker Invalidation & `u.onerror` on `'canceled'` (`js/voice_engine.ts:424-440, 586-596`)
In `VoiceEngine.parar()`:
```typescript
// Lines 424-440 of js/voice_engine.ts
parar(): void {
  if (typeof window !== 'undefined') {
    window._activeVoiceUtterance = null;
  }
  if (typeof speechSynthesis !== 'undefined') {
    try {
      speechSynthesis.cancel();
    } catch (_) {}
  }
  if (this._currentAudioSource) {
    try {
      this._currentAudioSource.stop();
      this._currentAudioSource.disconnect();
    } catch (_) {}
    this._currentAudioSource = null;
  }
},
```
And in `VoiceEngine.falar()`:
```typescript
// Lines 586-596 of js/voice_engine.ts
u.onerror = (err) => {
  if (typeof window !== 'undefined' && window._activeVoiceUtterance === u) {
    window._activeVoiceUtterance = null;
  }
  console.warn('[VoiceEngine] Falha na síntese nativa de fala:', err);
  if (opcoes.onend) {
    setTimeout(opcoes.onend, 800);
  } else if (opcoes.onerror) {
    opcoes.onerror(err);
  }
};
```
And in `VoiceEngine._tocarBuffer()`:
```typescript
// Lines 464-470 of js/voice_engine.ts
source.onended = () => {
  if (this._currentAudioSource === source) {
    this._currentAudioSource = null;
  }
  if (opcoes.onend) opcoes.onend();
};
```
**Defects observed**:
1. When `falarNeural()` sends a `SYNTHESIZE` message to the Web Worker (lines 504-523), the promise is recorded in `this._pendingSyntheses.set(reqId, { resolve, reject })`. If `parar()` is called while worker synthesis is in flight, `_pendingSyntheses` is ignored and remains pending.
2. When the worker later posts `SYNTHESIZE_SUCCESS`, `pBuffer` resolves in `falarNeural()` and proceeds to `this._tocarBuffer(wavBuffer, opcoes)`. Audio starts playing unexpectedly after the user had stopped it.
3. If the worker synthesis rejects or times out after `parar()`, `falarNeural()` catches the error and falls through to line 535: `return this.falar(textoNorm, opcoes);`, restarting speech via native TTS after `parar()` was called.
4. When `VoiceEngine.parar()` calls `speechSynthesis.cancel()`, the browser dispatches an `error` event with `err.error === 'canceled'` (or `'interrupted'`).
5. `u.onerror` logs an erroneous warning to the console and unconditionally runs `setTimeout(opcoes.onend, 800)`. In chaining modules such as `Storie`, `opcoes.onend` triggers the next sentence, causing playback to resume despite being cancelled.
6. When `this._currentAudioSource.stop()` is called in `parar()`, Web Audio API triggers `source.onended`. Because line 468 has `if (opcoes.onend) opcoes.onend()` outside the `if (this._currentAudioSource === source)` check, stopped buffer sources also fire `onend`.

### 1.4 `SpeechSynthesisUtterance` Premature GC in `js/vocab.js:494-499`
In `Vocab.pronunciarExemplo()`:
```javascript
// Lines 492-500 of js/vocab.js
if (typeof App !== 'undefined' && App.pronunciar) {
  App.pronunciar(texto);
} else if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
  try { window.speechSynthesis.cancel(); } catch (_) {}
  const u = new SpeechSynthesisUtterance(texto);
  u.lang = 'it-IT';
  window.speechSynthesis.speak(u);
}
```
**Defects observed**:
1. `u` is an ephemeral local variable inside `pronunciarExemplo()`.
2. As soon as `pronunciarExemplo()` exits, `u` is subject to premature Garbage Collection in V8 (Chromium) and WebKit (Safari).
3. When GC collects an active `SpeechSynthesisUtterance`, speech cuts out mid-sentence, `onend` never fires, and Chromium's internal speech synthesizer can wedge permanently until browser restart.
4. Unlike `js/core/tts.js:160` (`window._activeUtterance = u;`) and `js/storie.js:1289` (`window._storyActiveUtterance = u;`), `Vocab` has no persistent reference retention on either `Vocab` or `window`.

---

## 2. Logic Chain

1. **Section Navigation Audio Contract**:
   - `PROJECT.md` line 73 defines: `Audio lifecycle contract: AppNavigation.navegar(secao) calls centralized teardownAudio() terminating TTS, worker voice synthesis, recording, and story audio.`
   - Navigation between sections is an explicit boundary. Audio and recording processes from a previous section must not leak into the next section.
   - Centralizing audio teardown in `AppNavigation.teardownAudio(novaSecao)` guarantees that all audio subsystems (Web Speech API, VoiceEngine, Storie reading loop, Imitazione recording & player, Flashcard speech recognition, and Canzoni playback) are reliably terminated upon every section transition.

2. **Promise Rejection Elimination**:
   - The browser specification for `HTMLMediaElement.prototype.play()` requires user-gesture activation or compliant autoplay policies. Fast double-clicks on "Minha Gravação" or rapid switching from play to pause triggers `AbortError` or `NotAllowedError`.
   - Wrapping `_userAudioPlayer.play()` in a `.catch()` block that filters expected aborts prevents unhandled promise rejections from bubbling to `window.addEventListener('unhandledrejection')` and failing the acceptance criteria ("Zero erros não tratados no console durante interrupções abruptas de áudio").

3. **Session Epoch & Cancellation Integrity in VoiceEngine**:
   - Asynchronous worker synthesis and audio decoding are multi-step operations. Without an invalidation token (`_sessionEpoch`), an operation initiated before `parar()` will continue after `parar()`.
   - By incrementing `_sessionEpoch` on `parar()`, clearing and rejecting `_pendingSyntheses` with an `AbortError`, and checking `epoch === this._sessionEpoch` prior to buffer decoding and playback, any pending worker jobs are cleanly neutralized.
   - In `u.onerror`, checking for `err.error === 'canceled' || err.error === 'interrupted'` ensures that intentional cancellations do not trigger `opcoes.onend` or log false warnings.

4. **SpeechSynthesisUtterance Object Lifecycle**:
   - V8 does not keep DOM wrappers alive solely because native audio threads are speaking. Storing `u` on `Vocab._activeUtterance` and `window._vocabActiveUtterance` guarantees a root reference until the utterance fires `onend` or `onerror`, at which point the reference is set to `null`.

---

## 3. Caveats

1. **Build Step Required**: `js/voice_engine.ts` is written in TypeScript and compiled to `js/voice_engine.js` via `npm run build:ts`. Any edit to `js/voice_engine.ts` must be accompanied by compiling with `npm run build:ts` (or `npm run build`).
2. **Internal Method Calls**: `Storie._pararAudioPagina()` and `Imitazione._pararGravacaoMidia()` are internal methods. `teardownAudio` must perform defensive checks (`typeof ... === 'function'`) and handle possible exceptions with `try/catch`.
3. **Headless / happy-dom Environment**: In Vitest, `window.speechSynthesis`, `navigator.mediaDevices`, and `Audio` are mocked or stubbed. Unit tests for teardown and promise catching should mock these interfaces to verify invocation and rejection suppression.

---

## 4. Conclusion & Proposed Fix Design

Below are the exact code modifications designed for each of the four files owned by Milestone 2.

### Fix 1: `js/core/navigation.js`
Add `teardownAudio(novaSecao)` to `AppNavigation` and call it inside `navegar(secao)`.

#### Before:
```javascript
// Lines 61-64 of js/core/navigation.js
    // Pausa karaokê se sair da aba de músicas
    if (secao !== 'canzoni' && typeof Canzoni !== 'undefined' && Canzoni.tocandoKaraoke) {
      Canzoni.pararAudio();
    }
```

#### After:
```javascript
    // Interrompe áudios, TTS e gravações de microfone ativas ao trocar de seção (F11)
    this.teardownAudio(secao);
```

#### New Method to add to `AppNavigation` in `js/core/navigation.js`:
```javascript
  // ── Centralized Audio, TTS & Recording Teardown (F11 / M2) ──
  teardownAudio(novaSecao) {
    // 1. Cancela qualquer síntese em voo do Web Speech API nativo e limpa âncoras de GC
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel();
      } catch (_) {}
      window._activeUtterance = null;
      window._activeVoiceUtterance = null;
      window._storyActiveUtterance = null;
      window._vocabActiveUtterance = null;
    }

    // 2. Interrompe o motor de voz (Web Audio buffers, TTS e worker neural)
    const ve = (typeof window !== 'undefined' && window.VoiceEngine) ||
               (typeof globalThis !== 'undefined' && globalThis.VoiceEngine) ||
               (typeof VoiceEngine !== 'undefined' ? VoiceEngine : null);
    if (ve && typeof ve.parar === 'function') {
      try { ve.parar(); } catch (_) {}
    }

    // 3. Interrompe leitura de capítulos/páginas de Storie
    if (novaSecao !== 'storie') {
      const st = (typeof window !== 'undefined' && window.Storie) ||
                 (typeof globalThis !== 'undefined' && globalThis.Storie) ||
                 (typeof Storie !== 'undefined' ? Storie : null);
      if (st && typeof st._pararAudioPagina === 'function') {
        try { st._pararAudioPagina(); } catch (_) {}
      }
    }

    // 4. Interrompe gravação de microfone e player no Dojo (Imitazione)
    if (novaSecao !== 'imitazione') {
      const im = (typeof window !== 'undefined' && window.Imitazione) ||
                 (typeof globalThis !== 'undefined' && globalThis.Imitazione) ||
                 (typeof Imitazione !== 'undefined' ? Imitazione : null);
      if (im) {
        if (typeof im.pararGravacao === 'function') {
          try { im.pararGravacao(); } catch (_) {}
        }
        if (im._userAudioPlayer) {
          try {
            im._userAudioPlayer.pause();
            im._userAudioPlayer.currentTime = 0;
          } catch (_) {}
        }
        if (im._mediaStream) {
          try {
            im._mediaStream.getTracks().forEach(t => t.stop());
            im._mediaStream = null;
          } catch (_) {}
        }
      }
    }

    // 5. Interrompe gravação de voz ativa em Flashcards
    if (novaSecao !== 'flashcard') {
      const fc = (typeof window !== 'undefined' && window.Flashcards) ||
                 (typeof globalThis !== 'undefined' && globalThis.Flashcards) ||
                 (typeof Flashcards !== 'undefined' ? Flashcards : null);
      if (fc && fc.gravando) {
        if (typeof fc.pararGravacao === 'function') {
          try { fc.pararGravacao(); } catch (_) {}
        } else if (fc._recognition) {
          try { fc._recognition.stop(); } catch (_) {}
          fc._recognition = null;
          fc.gravando = false;
          if (typeof fc._atualizarBotaoGravar === 'function') {
            fc._atualizarBotaoGravar(false);
          }
        }
      }
    }

    // 6. Interrompe reprodução e karaokê de músicas (Canzoni)
    if (novaSecao !== 'canzoni') {
      const cz = (typeof window !== 'undefined' && window.Canzoni) ||
                 (typeof globalThis !== 'undefined' && globalThis.Canzoni) ||
                 (typeof Canzoni !== 'undefined' ? Canzoni : null);
      if (cz && typeof cz.pararAudio === 'function') {
        try { cz.pararAudio(); } catch (_) {}
      }
    }
  },
```

---

### Fix 2: `js/imitazione.js`
In `tocarMinhaGravacao()`, add `.catch()` and safe error handling. In `_pararGravacaoMidia()` and `pararGravacao()`, immediately release media tracks and pause player.

#### Before (`tocarMinhaGravacao`, lines 267-275):
```javascript
  tocarMinhaGravacao() {
    if (!this._userAudioUrl) return;
    if (this._userAudioPlayer) {
      this._userAudioPlayer.pause();
      this._userAudioPlayer.currentTime = 0;
    }
    this._userAudioPlayer = new Audio(this._userAudioUrl);
    this._userAudioPlayer.play();
  },
```

#### After:
```javascript
  tocarMinhaGravacao() {
    if (!this._userAudioUrl) return;
    if (this._userAudioPlayer) {
      try {
        this._userAudioPlayer.pause();
        this._userAudioPlayer.currentTime = 0;
      } catch (_) {}
    }
    try {
      this._userAudioPlayer = new Audio(this._userAudioUrl);
      const playPromise = this._userAudioPlayer.play();
      if (playPromise && typeof playPromise.catch === 'function') {
        playPromise.catch(err => {
          // AbortError e NotAllowedError são comuns em transições rápidas de áudio no browser
          if (err && err.name !== 'AbortError') {
            console.warn('[Imitazione] Falha ao reproduzir gravação do usuário:', err);
          }
        });
      }
    } catch (err) {
      console.warn('[Imitazione] Exceção ao instanciar ou tocar áudio:', err);
    }
  },
```

#### Before (`_pararGravacaoMidia`, lines 258-265):
```javascript
  _pararGravacaoMidia() {
    if (this._mediaRecorder && this._mediaRecorder.state !== 'inactive') {
      try { this._mediaRecorder.stop(); } catch (_) {}
    }
    this.isRecording = false;
    const btn = document.getElementById('dojo-btn-mic');
    if (btn) btn.classList.remove('recording');
  },
```

#### After:
```javascript
  _pararGravacaoMidia() {
    if (this._mediaRecorder && this._mediaRecorder.state !== 'inactive') {
      try { this._mediaRecorder.stop(); } catch (_) {}
    }
    if (this._mediaStream) {
      try {
        this._mediaStream.getTracks().forEach(t => t.stop());
      } catch (_) {}
      this._mediaStream = null;
    }
    this.isRecording = false;
    const btn = document.getElementById('dojo-btn-mic');
    if (btn) btn.classList.remove('recording');
  },
```

---

### Fix 3: `js/voice_engine.ts`
1. Add `_sessionEpoch: 0` property.
2. In `parar()`: increment `_sessionEpoch`, reject and clear `_pendingSyntheses`.
3. In `_tocarBuffer()`: accept `epoch` and ensure `source.onended` does not fire `opcoes.onend` if stopped.
4. In `falarNeural()`: verify `epoch === this._sessionEpoch` before and after awaits; do not fall back to `falar()` on cancellation.
5. In `falar()`: ignore `err.error === 'canceled' || err.error === 'interrupted'` in `u.onerror`.

#### Key snippet additions in `js/voice_engine.ts`:
```typescript
  // ── Session Epoch for Cancellation & Invalidation ──
  _sessionEpoch: 0,

  parar(): void {
    this._sessionEpoch++;

    if (typeof window !== 'undefined') {
      window._activeVoiceUtterance = null;
    }
    if (typeof speechSynthesis !== 'undefined') {
      try {
        speechSynthesis.cancel();
      } catch (_) {}
    }
    if (this._currentAudioSource) {
      try {
        this._currentAudioSource.stop();
        this._currentAudioSource.disconnect();
      } catch (_) {}
      this._currentAudioSource = null;
    }

    // Invalida e cancela todas as sínteses de Web Worker em voo
    if (this._pendingSyntheses.size > 0) {
      for (const [id, resolver] of this._pendingSyntheses.entries()) {
        try {
          resolver.reject(new DOMException('Síntese neural cancelada', 'AbortError'));
        } catch (_) {}
      }
      this._pendingSyntheses.clear();
    }
  },
```

#### In `_tocarBuffer()` (lines 442-478):
```typescript
  async _tocarBuffer(wavBuffer: ArrayBuffer, opcoes: VoiceEngineOptions = {}, epoch?: number): Promise<boolean> {
    const currentEpoch = epoch !== undefined ? epoch : this._sessionEpoch;
    if (currentEpoch !== this._sessionEpoch) return false;

    this.parar();
    const playEpoch = this._sessionEpoch;
    const ctx = this.obterAudioContext();
    if (!ctx) return false;

    try {
      const audioBuffer = await ctx.decodeAudioData(wavBuffer.slice(0));
      if (playEpoch !== this._sessionEpoch) return false;

      const source = ctx.createBufferSource();
      source.buffer = audioBuffer;

      let rate = opcoes.rate;
      if (rate == null && typeof localStorage !== 'undefined') {
        const speedStr = localStorage.getItem('it_audio_speed');
        if (speedStr) rate = parseFloat(speedStr);
      }
      if (rate != null && !isNaN(rate) && rate > 0) {
        source.playbackRate.value = Math.max(0.5, Math.min(2.0, rate));
      }

      source.connect(ctx.destination);
      this._currentAudioSource = source;

      source.onended = () => {
        if (this._currentAudioSource === source) {
          this._currentAudioSource = null;
          if (playEpoch === this._sessionEpoch && opcoes.onend) {
            opcoes.onend();
          }
        }
      };

      source.start();
      return true;
    } catch (err) {
      if (playEpoch === this._sessionEpoch) {
        console.warn('[VoiceEngine] Falha ao decodificar/tocar buffer:', err);
        if (opcoes.onerror) opcoes.onerror(err);
      }
      return false;
    }
  },
```

#### In `falar()` `u.onerror` (lines 586-596):
```typescript
      u.onerror = (err: any) => {
        if (typeof window !== 'undefined' && window._activeVoiceUtterance === u) {
          window._activeVoiceUtterance = null;
        }

        const erroTipo = err && (err.error || err.type);
        if (erroTipo === 'canceled' || erroTipo === 'interrupted') {
          // Cancelamento intencional via speechSynthesis.cancel(): suprime log e NUNCA dispara onend
          return;
        }

        console.warn('[VoiceEngine] Falha na síntese nativa de fala:', err);
        if (opcoes.onerror) {
          opcoes.onerror(err);
        } else if (opcoes.onend) {
          setTimeout(opcoes.onend, 800);
        }
      };
```

---

### Fix 4: `js/vocab.js`
Anchor utterance on `Vocab._activeUtterance` and `window._vocabActiveUtterance` with lifecycle cleanup.

#### Before (`pronunciarExemplo`, lines 492-500):
```javascript
    if (typeof App !== 'undefined' && App.pronunciar) {
      App.pronunciar(texto);
    } else if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (_) {}
      const u = new SpeechSynthesisUtterance(texto);
      u.lang = 'it-IT';
      window.speechSynthesis.speak(u);
    }
```

#### After:
```javascript
    if (typeof App !== 'undefined' && App.pronunciar) {
      App.pronunciar(texto);
    } else if (typeof VoiceEngine !== 'undefined' && typeof VoiceEngine.falar === 'function') {
      VoiceEngine.falar(texto);
    } else if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (_) {}
      const u = new SpeechSynthesisUtterance(texto);
      u.lang = 'it-IT';

      // Fix Crítico do Chromium/WebKit: Ancorar no Vocab e na janela global para evitar coleta precoce pelo GC
      Vocab._activeUtterance = u;
      if (typeof window !== 'undefined') {
        window._vocabActiveUtterance = u;
      }

      u.onend = () => {
        if (Vocab._activeUtterance === u) Vocab._activeUtterance = null;
        if (typeof window !== 'undefined' && window._vocabActiveUtterance === u) {
          window._vocabActiveUtterance = null;
        }
      };
      u.onerror = () => {
        if (Vocab._activeUtterance === u) Vocab._activeUtterance = null;
        if (typeof window !== 'undefined' && window._vocabActiveUtterance === u) {
          window._vocabActiveUtterance = null;
        }
      };

      window.speechSynthesis.speak(u);
    }
```

And add to `Vocab` object definition (around line 18):
```javascript
  _activeUtterance: null,
```

---

## 5. Verification Method

To independently verify the implementation:

1. **Build & Transpile**:
   ```bash
   npm run build:ts
   npm run build
   ```
   *Expected outcome*: Compiles `js/voice_engine.ts` into `js/voice_engine.js` with code 0 and no TypeScript errors.

2. **Automated Unit & Integration Tests**:
   ```bash
   npm test
   ```
   *Expected outcome*: All existing test suites pass.

3. **Dedicated Audio Concurrency / Lifecycle Test Case**:
   The implementer can verify via unit test in `tests/audio_concurrency.test.ts` or `tests/navigation.test.js`:
   - `AppNavigation.navegar('templi')` calls `VoiceEngine.parar()`, `window.speechSynthesis.cancel()`, and stops any active `Imitazione` or `Storie` playback.
   - Calling `VoiceEngine.parar()` while worker synthesis is pending rejects the promise with `AbortError` and does not invoke `_tocarBuffer` or fallback to `falar()`.
   - Simulating `SpeechSynthesisErrorEvent` with `{ error: 'canceled' }` in `VoiceEngine.falar()` does NOT call `opcoes.onend()`.
   - Calling `Imitazione.tocarMinhaGravacao()` when `play()` returns a rejected promise does not produce an unhandled rejection.
   - `Vocab.pronunciarExemplo()` sets `Vocab._activeUtterance` and `window._vocabActiveUtterance`.

4. **Invalidation Conditions**:
   - If any audio or microphone session remains active after switching between tabs in the UI.
   - If `unhandledrejection` is observed when rapid playback actions are performed in `Imitazione`.
   - If `VoiceEngine` triggers `opcoes.onend` following `parar()`.
