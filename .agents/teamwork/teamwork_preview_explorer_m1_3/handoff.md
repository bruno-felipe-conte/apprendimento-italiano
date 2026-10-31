# Implementation Blueprint: Schema Validation, Atomic Backup & Content Sanitization (F4, F5, F6)

**Author**: Explorer M1.3 (Schema Validation, Atomic Backup & Content Sanitization)  
**Date**: 2026-10-31T00:50:00Z  
**Workspace**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano`  
**Working Directory**: `/mnt/c/Users/bruno/Documents/apprendimento-italiano/.agents/teamwork/teamwork_preview_explorer_m1_3`  
**Milestone**: Milestone 1 (F4, F5, F6)  
**Status**: COMPLETE (Read-Only Investigation & Code-Level Architectural Blueprint)

---

## 1. Observation

### 1.1 Vulnerability in `carregarProgresso()` & `carregarFlashcards()` (`js/core/state.js`)
- **Direct Code Location**: `js/core/state.js` lines 101-139 and 158-164.
- **Verbatim Code**:
  ```javascript
  101: carregarProgresso() {
  102:   try {
  103:     const raw = localStorage.getItem('it_progresso');
  104:     if (raw) {
  105:       const p = JSON.parse(raw);
  106:       // Backward compatibility
  107:       if (!p.grammatica_completadas) p.grammatica_completadas = [];
  108:       if (p.meta_diaria === undefined) p.meta_diaria = 100;
  109:       if (p.xp_hoje === undefined) p.xp_hoje = 0;
  110:       if (p.data_xp_hoje === undefined) p.data_xp_hoje = null;
  111:       if (!p.favoritos)   p.favoritos   = [];
  112:       if (!p.conquistas)  p.conquistas  = [];
  113:       if (!p.data_inicio) p.data_inicio = p.ultimo_estudo || Date.now();
  114:       if (p.meta_prazo === undefined) p.meta_prazo = null;
  115:       if (p.audio_rate === undefined) p.audio_rate = 0.85;
  116:       return p;
  117:     }
  118:   } catch (e) { /* ignore */ }
  ...
  158: carregarFlashcards() {
  159:   try {
  160:     const raw = localStorage.getItem('it_flashcards');
  161:     if (raw) return JSON.parse(raw);
  162:   } catch (e) { /* ignore */ }
  163:   return {};
  164: },
  ```
- **Observed Failure Modes**:
  1. Primitive payloads: If `localStorage.getItem('it_progresso')` contains `"corrupted"` (or any JSON string/number), `JSON.parse(raw)` yields a string or number. While `p.grammatica_completadas = []` throws and is caught, if `raw` is `"[]"`, `typeof [] === 'object'`, and `carregarProgresso()` returns an array. Callers expecting an object crash immediately.
  2. Missing array properties: If `raw` is `{"nivel": "abc", "templos_desbloqueados": null}`, `JSON.parse` does not throw. `carregarProgresso()` returns `p` with `templos_desbloqueados: null`. Downstream code in `js/core/templos.js` runs `p.templos_desbloqueados.includes(...)` which crashes with `TypeError: Cannot read properties of null (reading 'includes')`, preventing the application UI from rendering.
  3. Corrupted flashcard deck: If `it_flashcards` contains `"null"`, `"123"`, or `"[1, 2]"`, `carregarFlashcards()` returns `null`, `123`, or an array. Callers calling `Object.keys(flashcardData)` or iterating with `for (const id in flashcardData)` throw unhandled TypeErrors. Furthermore, individual cards with `stability: NaN` or `difficulty: "broken"` infect the FSRS scheduler math, permanently breaking the review deck.

---

### 1.2 Vulnerability in `importarDados()` (`js/profilo.js`)
- **Direct Code Location**: `js/profilo.js` lines 466-514.
- **Verbatim Code**:
  ```javascript
  471: try {
  472:   const backup = JSON.parse(e.target.result);
  473:   if (!backup.versao || !backup.progresso) throw new Error(I18n.t('prof_erro_formato'));
  474:   if (!confirm(I18n.t('prof_confirm_importar'))) return;
  475:   if (backup.progresso)         localStorage.setItem('it_progresso',         JSON.stringify(backup.progresso));
  476:   if (backup.flashcards)        localStorage.setItem('it_flashcards',        JSON.stringify(backup.flashcards));
  477:   if (backup.diario)            localStorage.setItem('it_diario',            JSON.stringify(backup.diario));
  ...
  494:   if (backup.bookmarks && typeof backup.bookmarks === 'object') {
  495:     for (const [k, v] of Object.entries(backup.bookmarks)) {
  496:       if (k.startsWith('it_book_bm_')) localStorage.setItem(k, v);
  497:     }
  498:   }
  499: 
  500:   if (backup.canzoni_custom?.length)    localStorage.setItem('it_canzoni_custom',    JSON.stringify(backup.canzoni_custom));
  501:   if (backup.dialoghi_custom?.length)   localStorage.setItem('it_dialoghi_custom',   JSON.stringify(backup.dialoghi_custom));
  502:   if (backup.storie_custom?.length)     localStorage.setItem('it_storie_custom',     JSON.stringify(backup.storie_custom));
  503:   if (backup.imitazioni_custom?.length) localStorage.setItem('it_imitazioni_custom', JSON.stringify(backup.imitazioni_custom));
  504:   if (backup.vocab_custom?.length)      localStorage.setItem('it_vocab_custom',      JSON.stringify(backup.vocab_custom));
  505:   if (backup.canzoni_ocultas?.length)   localStorage.setItem('it_canzoni_ocultas',   JSON.stringify(backup.canzoni_ocultas));
  506:   App.notificar('notif_backup_imp', 'sucesso');
  507:   setTimeout(() => location.reload(), 1200);
  508: } catch(err) {
  509:   App.notificar(I18n.t('notif_arquivo_inv') + err.message, 'erro');
  510: }
  ```
- **Observed Failure Modes**:
  1. Zero Pre-Flight Validation: The only verification is `if (!backup.versao || !backup.progresso)`. Subfields (`nivel`, `xp`, `templos_desbloqueados`, etc.) are never validated. An imported payload with `"progresso": { "nivel": "NaN", "templos_desbloqueados": "broken" }` is directly persisted to storage. On reload, the app is trapped in a permanent crash loop.
  2. Non-Atomic Partial Writes: Storage writes are performed iteratively across 20 independent `setItem` calls. If `QuotaExceededError` occurs on item 8 (e.g. at bookmarks or custom songs):
     - The first 7 items are updated.
     - The remaining items are lost.
     - The application is left in a corrupted "Franken-state" with no rollback to the pre-import state.
  3. Key Namespace Flooding via Bookmarks: Any key in `backup.bookmarks` starting with `it_book_bm_` is written without checking key characters, key length, key count limit, or value size. An attacker or corrupted file can inject 50,000 keys, overflowing storage quota or injecting prototype pollution.

---

### 1.3 Vulnerability in `exportarDados()` (`js/profilo.js`)
- **Direct Code Location**: `js/profilo.js` lines 414-463.
- **Verbatim Code**:
  ```javascript
  424: const backup = {
  425:   versao: 4,
  426:   data: new Date().toISOString(),
  427:   progresso:              JSON.parse(localStorage.getItem('it_progresso')        || 'null'),
  428:   flashcards:             JSON.parse(localStorage.getItem('it_flashcards')       || '{}'),
  429:   diario:                 JSON.parse(localStorage.getItem('it_diario')           || '{}'),
  430:   quiz_historico:         JSON.parse(localStorage.getItem('it_quiz_historico')   || '[]'),
  431:   storie_lidas:           JSON.parse(localStorage.getItem('it_storie_lidas')     || '[]'),
  ...
  447:   canzoni_custom:         JSON.parse(localStorage.getItem('it_canzoni_custom')   || '[]'),
  448:   dialoghi_custom:        JSON.parse(localStorage.getItem('it_dialoghi_custom')  || '[]'),
  449:   storie_custom:          JSON.parse(localStorage.getItem('it_storie_custom')    || '[]'),
  450:   imitazioni_custom:      JSON.parse(localStorage.getItem('it_imitazioni_custom')|| '[]'),
  451:   vocab_custom:           JSON.parse(localStorage.getItem('it_vocab_custom')     || '[]'),
  452:   // preferências de ocultação
  453:   canzoni_ocultas:        JSON.parse(localStorage.getItem('it_canzoni_ocultas')  || '[]'),
  454: };
  ```
- **Observed Failure Modes**:
  If any single key in `localStorage` contains invalid or truncated JSON (e.g. `it_diario` truncated during a crash), `JSON.parse` throws an unhandled `SyntaxError`. The entire export aborts. The user is prevented from downloading a rescue backup to save the remainder of their valid progress.

---

### 1.4 Vulnerability to Stored XSS in Custom Content (`js/dialoghi.js`, `js/storie.js`, `js/canzoni.js`, `js/profilo.js`)
- **Direct Code Locations**:
  - `js/dialoghi.js` lines 404-406, 429-430, 441-443, 459, 537:
    ```javascript
    404: <div class="dialogo-nome">${t.personaggio}</div>
    405: <div>${fraseExibir} <button class="dialogo-audio-btn" onclick="App.pronunciar('${fraseExibir.replace(/'/g, "\\'")}')">🔊</button></div>
    406: ${traducaoExibir ? `<div class="dialogo-traducao">${traducaoExibir}</div>` : ''}
    ...
    459: html += `<button class="dialogo-opcao" onclick="Dialoghi.checarResposta(${idx}, this)">${alt}</button>`;
    ...
    537: ${(d.vocabulario_chave || []).map(v => `<span style="...">${v}</span>`).join('')}
    ```
    None of these strings are escaped. Injected `<img src=x onerror=alert(1)>` executes immediately when the dialogue is played.
  - `js/storie.js` lines 630-631, 767-776:
    ```javascript
    630: <span class="book-top-title">${tituloExibido}</span>
    631: <span class="book-top-subtitle">${s.autor || 'Letteratura'} · ${s.nivel}</span>
    ...
    767: <span class="antique-cover-icon">${s.icone || '📖'}</span>
    768: <h2 class="antique-cover-title">${tituloExibido}</h2>
    769: <div class="antique-cover-subtitle">${s.autor || 'Letteratura Italiana'} ${s.tema ? '· ' + s.tema : ''}</div>
    776: <span class="antique-running-head">${pag.capituloTitulo || tituloExibido}</span>
    ```
    Neither `tituloExibido`, `s.autor`, `s.tema`, nor `pag.capituloTitulo` are escaped in book cover and header templates.
  - `js/canzoni.js` line 871:
    ```javascript
    871: const safeW = w.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
    872: return '<button class="can-choice-btn" onclick="Canzoni._escolher(\'' + safeW + '\')"><i>' + this._esc(w) + '</i></button>';
    ```
    `safeW` does not escape `"` (double quote), allowing escape from the `onclick="..."` HTML attribute.
  - `js/profilo.js` lines 72-74:
    ```javascript
    72: ${this._row(I18n.t('prof_nivel_atual'), `${p.nivel || 1}`)}
    73: ${this._row(I18n.t('prof_xp_total'), `${(p.xp || 0).toLocaleString()} XP`)}
    ```
    If `p.nivel` is a string with HTML tags from an imported payload, it is directly interpolated into `container.innerHTML`.

---

## 2. Logic Chain

1. **State Loading Resilience**:
   - From Observation 1.1: `carregarProgresso()` and `carregarFlashcards()` must guarantee that whatever string is read from storage, the returned value strictly matches the expected TypeScript/JavaScript structure:
     - `progresso`: An object with guaranteed arrays for `templos_desbloqueados` (always includes `1`), `templos_concluidos`, `grammatica_completadas`, `favoritos`, `conquistas`; finite positive integers for `nivel`, `xp`, `streak`, `total_palavras`, `meta_diaria`; and safe audio rate.
     - `flashcardData`: A plain dictionary object where every value is a valid FSRS card structure with finite bounds for `difficulty` (`[1, 10]`), `stability` (`[0, 36500]`), and valid state strings (`'new'|'learning'|'review'|'relearning'|'suspended'`).
   - Therefore, a dedicated `_sanitizeProgresso()` and `_sanitizeFlashcards()` method must be implemented in `AppState` (`js/core/state.js`).

2. **Atomic Backup Import & Rollback**:
   - From Observation 1.2: Calling `localStorage.setItem` sequentially without staging risks partial failure mid-import (e.g. `QuotaExceededError`).
   - A transactional staging pattern guarantees all-or-nothing atomicity:
     * Pre-flight: Validate that the payload conforms to the required backup schema. Reject invalid payloads before modifying storage.
     * Snapshot: Capture the in-memory state of all affected keys in `localStorage`.
     * Staging write: Write all incoming items to temporary keys (`it_stage_${k}`). If quota is exceeded or an error occurs during staging, delete all written `it_stage_*` keys and abort with a user error. Live state is untouched.
     * Commit: When all staging writes succeed, copy staging keys to live keys and clean up staging keys.
     * Rollback: If any error unexpectedly occurs during commit, restore the in-memory snapshot back to live keys and purge staging keys.
   - Bookmarks validation: Apply regex `/^it_book_bm_[a-zA-Z0-9_-]+$/`, limit key count to `<= 100`, and limit value size to `<= 1024` bytes.

3. **Safe Export**:
   - From Observation 1.3: In `exportarDados()`, wrapping each `JSON.parse(localStorage.getItem(key))` in a helper (`_safeParseStorage(key, fallback)`) prevents a single corrupted storage key from crashing the export, allowing users to export and rescue all surviving data.

4. **Stored XSS Sanitization**:
   - From Observation 1.4: Injected strings from imported JSON can reach `innerHTML` in `dialoghi.js`, `storie.js`, `canzoni.js`, and `profilo.js`.
   - Applying a dual-defense strategy:
     * Layer 1 (Ingestion): Run all imported textual fields through `AppState.sanitizarTexto()` to strip dangerous HTML tags (`<script>`, `<iframe>`, `<img>`, `<svg>`, etc.) before saving to `localStorage`.
     * Layer 2 (Rendering): Contextually escape HTML entities in template interpolations via `this._esc()` / `this._escape()` across dialogue players, story book covers, and song choice buttons.

---

## 3. Caveats

1. **Classic Script Loading Environment**:
   - `js/core/state.js`, `js/profilo.js`, `js/canzoni.js`, `js/storie.js`, and `js/dialoghi.js` are classic browser scripts (not ES modules) loaded directly in `index.html`. They do not use `import` statements directly. Schema validation must be implemented using pure vanilla JavaScript defensive functions within `AppState` and `Profilo` rather than external npm dependencies at browser runtime.
2. **Backward Compatibility**:
   - Existing user backups (v1, v2, v3, v4) may contain optional fields or missing arrays. The validator must default missing fields (e.g. `meta_prazo`, `audio_rate`, `favoritos`) rather than rejecting older valid backups.
3. **Storage Quota Constraints**:
   - The staging pattern requires temporary storage for two copies of the data during import (`it_stage_*` + live keys). For standard backups (~50 KB to 200 KB), this is well within the 5 MB localStorage budget. In edge cases where localStorage is already 95% full, Explorer M1.1's eviction ladder will clear ephemeral SWR caches prior to import.

---

## 4. Conclusion & Detailed Implementation Blueprint

### 4.1 Blueprint: `js/core/state.js` Schema Validation & Sanitization

#### Add `AppState._sanitizeProgresso(p)`:
```javascript
  _sanitizeProgresso(p) {
    const defaults = {
      nivel: 1,
      xp: 0,
      xp_proximo_nivel: 500,
      templos_desbloqueados: [1],
      templos_concluidos: [],
      total_palavras: 0,
      streak: 0,
      ultimo_estudo: null,
      grammatica_completadas: [],
      meta_diaria: 100,
      xp_hoje: 0,
      data_xp_hoje: null,
      favoritos: [],
      conquistas: [],
      data_inicio: Date.now(),
      meta_prazo: null,
      audio_rate: 0.85
    };

    if (!p || typeof p !== 'object' || Array.isArray(p)) {
      return defaults;
    }

    const nivel = (Number.isInteger(p.nivel) && p.nivel >= 1) ? p.nivel : 1;
    const xp = (typeof p.xp === 'number' && Number.isFinite(p.xp) && p.xp >= 0) ? Math.floor(p.xp) : 0;
    const xp_proximo_nivel = (typeof p.xp_proximo_nivel === 'number' && Number.isFinite(p.xp_proximo_nivel) && p.xp_proximo_nivel > 0)
      ? Math.floor(p.xp_proximo_nivel)
      : (nivel * 500);

    // templos_desbloqueados must be an array of positive integers and always include 1
    let templos_desbloqueados = [1];
    if (Array.isArray(p.templos_desbloqueados)) {
      const validos = p.templos_desbloqueados.filter(t => Number.isInteger(t) && t >= 1 && t <= 100);
      if (!validos.includes(1)) validos.unshift(1);
      templos_desbloqueados = Array.from(new Set(validos));
    }

    const templos_concluidos = Array.isArray(p.templos_concluidos)
      ? Array.from(new Set(p.templos_concluidos.filter(t => Number.isInteger(t) && t >= 1)))
      : [];

    const total_palavras = (typeof p.total_palavras === 'number' && Number.isFinite(p.total_palavras) && p.total_palavras >= 0)
      ? Math.floor(p.total_palavras)
      : 0;

    const streak = (typeof p.streak === 'number' && Number.isFinite(p.streak) && p.streak >= 0)
      ? Math.floor(p.streak)
      : 0;

    const ultimo_estudo = (typeof p.ultimo_estudo === 'number' && Number.isFinite(p.ultimo_estudo))
      ? p.ultimo_estudo
      : (typeof p.ultimo_estudo === 'string' && !isNaN(Date.parse(p.ultimo_estudo)) ? Date.parse(p.ultimo_estudo) : null);

    const grammatica_completadas = Array.isArray(p.grammatica_completadas)
      ? p.grammatica_completadas.filter(id => typeof id === 'string' || typeof id === 'number')
      : [];

    const meta_diaria = (typeof p.meta_diaria === 'number' && Number.isFinite(p.meta_diaria) && p.meta_diaria > 0)
      ? Math.floor(p.meta_diaria)
      : 100;

    const xp_hoje = (typeof p.xp_hoje === 'number' && Number.isFinite(p.xp_hoje) && p.xp_hoje >= 0)
      ? Math.floor(p.xp_hoje)
      : 0;

    const data_xp_hoje = typeof p.data_xp_hoje === 'string' ? p.data_xp_hoje : null;

    const favoritos = Array.isArray(p.favoritos)
      ? p.favoritos.filter(f => typeof f === 'string' || typeof f === 'number')
      : [];

    const conquistas = Array.isArray(p.conquistas)
      ? p.conquistas.filter(c => typeof c === 'string' || (c && typeof c.id === 'string'))
      : [];

    const data_inicio = (typeof p.data_inicio === 'number' && Number.isFinite(p.data_inicio))
      ? p.data_inicio
      : (ultimo_estudo || Date.now());

    let meta_prazo = null;
    if (p.meta_prazo && typeof p.meta_prazo === 'object' && !Array.isArray(p.meta_prazo)) {
      if (Number.isInteger(p.meta_prazo.nivelAlvo) && p.meta_prazo.dataAlvo) {
        meta_prazo = {
          nivelAlvo: p.meta_prazo.nivelAlvo,
          dataAlvo: String(p.meta_prazo.dataAlvo)
        };
      }
    }

    const audio_rate = (typeof p.audio_rate === 'number' && Number.isFinite(p.audio_rate) && p.audio_rate >= 0.5 && p.audio_rate <= 2.0)
      ? p.audio_rate
      : 0.85;

    return {
      nivel,
      xp,
      xp_proximo_nivel,
      templos_desbloqueados,
      templos_concluidos,
      total_palavras,
      streak,
      ultimo_estudo,
      grammatica_completadas,
      meta_diaria,
      xp_hoje,
      data_xp_hoje,
      favoritos,
      conquistas,
      data_inicio,
      meta_prazo,
      audio_rate
    };
  },
```

#### Update `AppState.carregarProgresso()`:
```javascript
  carregarProgresso() {
    try {
      const raw = localStorage.getItem('it_progresso');
      if (raw) {
        const parsed = JSON.parse(raw);
        return this._sanitizeProgresso(parsed);
      }
    } catch (e) {
      console.warn('[AppState] Falha ao carregar it_progresso, restaurando padrão:', e);
    }
    return this._sanitizeProgresso(null);
  },
```

#### Add `AppState._sanitizeFlashcards(deck)` & update `carregarFlashcards()`:
```javascript
  _sanitizeFlashcards(deck) {
    if (!deck || typeof deck !== 'object' || Array.isArray(deck)) {
      return {};
    }
    const sanitizedDeck = {};
    const validStates = ['new', 'learning', 'review', 'relearning', 'suspended'];

    for (const [id, card] of Object.entries(deck)) {
      if (!card || typeof card !== 'object' || Array.isArray(card)) {
        continue;
      }

      const state = validStates.includes(card.state) ? card.state : 'new';
      const difficulty = (typeof card.difficulty === 'number' && Number.isFinite(card.difficulty))
        ? Math.min(Math.max(card.difficulty, 1), 10)
        : 5.0;
      const stability = (typeof card.stability === 'number' && Number.isFinite(card.stability) && card.stability >= 0)
        ? Math.min(Math.max(card.stability, 0), 36500)
        : 1.0;
      const reps = (Number.isInteger(card.reps) && card.reps >= 0) ? card.reps : 0;
      const lapses = (Number.isInteger(card.lapses) && card.lapses >= 0) ? card.lapses : 0;
      const lastReview = (typeof card.lastReview === 'number' && Number.isFinite(card.lastReview))
        ? card.lastReview
        : null;
      const interval = (typeof card.interval === 'number' && Number.isFinite(card.interval) && card.interval >= 0)
        ? card.interval
        : 1;
      const nextReview = (typeof card.nextReview === 'number' && Number.isFinite(card.nextReview))
        ? card.nextReview
        : null;
      const retrievability = (typeof card.retrievability === 'number' && Number.isFinite(card.retrievability))
        ? Math.min(Math.max(card.retrievability, 0), 1)
        : 1.0;

      sanitizedDeck[id] = {
        ...card,
        state,
        difficulty,
        stability,
        reps,
        lapses,
        lastReview,
        interval,
        nextReview,
        retrievability
      };
    }

    return sanitizedDeck;
  },

  carregarFlashcards() {
    try {
      const raw = localStorage.getItem('it_flashcards');
      if (raw) {
        const parsed = JSON.parse(raw);
        return this._sanitizeFlashcards(parsed);
      }
    } catch (e) {
      console.warn('[AppState] Falha ao carregar it_flashcards, retornando vazio:', e);
    }
    return {};
  },
```

#### Add string sanitization helpers in `AppState`:
```javascript
  sanitizarTexto(str) {
    if (str == null) return '';
    if (typeof str !== 'string') return String(str);
    return str.replace(/<[^>]*>?/gm, '').trim();
  },
```

---

### 4.2 Blueprint: `js/profilo.js` Atomic Backup Import & Safe Export

#### Add Helper Methods to `Profilo`:
```javascript
  _safeParseStorage(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      if (raw === null || raw === undefined || raw === '') return fallback;
      return JSON.parse(raw);
    } catch (err) {
      console.warn(`[Profilo] Chave '${key}' corrompida no localStorage, usando fallback:`, err);
      return fallback;
    }
  },

  _validarPayloadBackup(backup) {
    if (!backup || typeof backup !== 'object' || Array.isArray(backup)) {
      throw new Error('Arquivo de backup inválido (conteúdo não é um objeto JSON)');
    }
    if (!backup.versao || typeof backup.versao !== 'number' || backup.versao < 1) {
      throw new Error('Versão de backup ausente ou inválida');
    }
    if (!backup.progresso || typeof backup.progresso !== 'object' || Array.isArray(backup.progresso)) {
      throw new Error('Dados de progresso ausentes ou corrompidos no backup');
    }
    // Verifica subcampos vitais
    if (typeof backup.progresso.nivel !== 'number' || backup.progresso.nivel < 1) {
      throw new Error('Campo "nivel" inválido no progresso do backup');
    }
    if (typeof backup.progresso.xp !== 'number' || backup.progresso.xp < 0) {
      throw new Error('Campo "xp" inválido no progresso do backup');
    }
    if (!Array.isArray(backup.progresso.templos_desbloqueados) || backup.progresso.templos_desbloqueados.length === 0) {
      throw new Error('Campo "templos_desbloqueados" inválido no backup (deve ser lista com ao menos 1 templo)');
    }

    if (backup.flashcards && (typeof backup.flashcards !== 'object' || Array.isArray(backup.flashcards))) {
      throw new Error('Coleção de flashcards malformada no backup');
    }
    if (backup.diario && (typeof backup.diario !== 'object' || Array.isArray(backup.diario))) {
      throw new Error('Registro de diário malformado no backup');
    }
    if (backup.quiz_historico && !Array.isArray(backup.quiz_historico)) {
      throw new Error('Histórico de quiz malformado no backup (deve ser lista)');
    }
    if (backup.storie_lidas && !Array.isArray(backup.storie_lidas)) {
      throw new Error('Histórico de histórias lidas malformado no backup');
    }
    return true;
  },

  _sanitizarBookmarks(bookmarksObj) {
    if (!bookmarksObj || typeof bookmarksObj !== 'object' || Array.isArray(bookmarksObj)) {
      return {};
    }
    const clean = {};
    const BM_REGEX = /^it_book_bm_[a-zA-Z0-9_-]+$/;
    let count = 0;
    const MAX_BOOKMARKS = 100;

    for (const [k, v] of Object.entries(bookmarksObj)) {
      if (count >= MAX_BOOKMARKS) break;
      if (typeof k === 'string' && k.length <= 64 && BM_REGEX.test(k)) {
        if (typeof v === 'string' || typeof v === 'number') {
          clean[k] = String(v).slice(0, 1024);
          count++;
        }
      }
    }
    return clean;
  },
```

#### Updated `exportarDados()` (Safe Export):
```javascript
  exportarDados() {
    try {
      const bookmarks = {};
      const BM_REGEX = /^it_book_bm_[a-zA-Z0-9_-]+$/;
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        if (k && BM_REGEX.test(k)) {
          bookmarks[k] = localStorage.getItem(k);
        }
      }

      const backup = {
        versao: 4,
        data: new Date().toISOString(),
        progresso:              this._safeParseStorage('it_progresso', null),
        flashcards:             this._safeParseStorage('it_flashcards', {}),
        diario:                 this._safeParseStorage('it_diario', {}),
        quiz_historico:         this._safeParseStorage('it_quiz_historico', []),
        storie_lidas:           this._safeParseStorage('it_storie_lidas', []),
        onboarding:             localStorage.getItem('it_onboarding_done'),
        tema:                   localStorage.getItem('it_tema'),
        idioma:                 localStorage.getItem('it_idioma') || 'pt',
        som:                    localStorage.getItem('it_som'),
        sidebar_pinned:         localStorage.getItem('it_sidebar_pinned'),
        audio_speed:            localStorage.getItem('it_audio_speed') || '0.85',
        voz_preferida:          localStorage.getItem('it_voz_preferida') || null,
        usar_voz_neural:        localStorage.getItem('it_usar_voz_neural'),
        voz_neural_instalada:   localStorage.getItem('it_voz_neural_instalada'),
        imersao_usada:          localStorage.getItem('it_imersao_usada'),
        palavra_dia:            localStorage.getItem('it_palavra_dia'),
        tour_done:              localStorage.getItem('it_tour_done'),
        ultimo_aviso_backup:    localStorage.getItem('it_ultimo_aviso_backup'),
        bookmarks:              bookmarks,
        canzoni_custom:         this._safeParseStorage('it_canzoni_custom', []),
        dialoghi_custom:        this._safeParseStorage('it_dialoghi_custom', []),
        storie_custom:          this._safeParseStorage('it_storie_custom', []),
        imitazioni_custom:      this._safeParseStorage('it_imitazioni_custom', []),
        vocab_custom:           this._safeParseStorage('it_vocab_custom', []),
        canzoni_ocultas:        this._safeParseStorage('it_canzoni_ocultas', []),
      };

      const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `italiano_backup_${new Date(new Date().getTime() - new Date().getTimezoneOffset() * 60000).toISOString().slice(0, 10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      App.notificar('notif_backup_exp', 'sucesso');
    } catch (err) {
      console.error('[Profilo.exportarDados] Falha na exportação:', err);
      App.notificar('Erro ao gerar exportação: ' + err.message, 'erro');
    }
  },
```

#### Updated `importarDados()` (Atomic Staging & Rollback):
```javascript
  importarDados(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const backup = JSON.parse(e.target.result);
        this._validarPayloadBackup(backup);

        if (!confirm(I18n.t('prof_confirm_importar'))) return;

        // Sanitiza dados de progresso e flashcards via AppState
        const progressoSanitizado = (typeof AppState !== 'undefined' && AppState._sanitizeProgresso)
          ? AppState._sanitizeProgresso(backup.progresso)
          : backup.progresso;

        const flashcardsSanitizados = (backup.flashcards && typeof AppState !== 'undefined' && AppState._sanitizeFlashcards)
          ? AppState._sanitizeFlashcards(backup.flashcards)
          : (backup.flashcards || {});

        const bookmarksSanitizados = this._sanitizarBookmarks(backup.bookmarks);

        // Mapeia todas as operações pretendidas
        const operacoes = new Map();
        operacoes.set('it_progresso', JSON.stringify(progressoSanitizado));
        operacoes.set('it_flashcards', JSON.stringify(flashcardsSanitizados));
        if (backup.diario) operacoes.set('it_diario', JSON.stringify(backup.diario));
        if (backup.quiz_historico) operacoes.set('it_quiz_historico', JSON.stringify(backup.quiz_historico));
        if (backup.storie_lidas) operacoes.set('it_storie_lidas', JSON.stringify(backup.storie_lidas));

        if (backup.onboarding != null) operacoes.set('it_onboarding_done', String(backup.onboarding));
        if (backup.tema != null) operacoes.set('it_tema', String(backup.tema));
        if (backup.idioma != null) operacoes.set('it_idioma', String(backup.idioma));
        if (backup.som != null) operacoes.set('it_som', String(backup.som));
        if (backup.sidebar_pinned != null) operacoes.set('it_sidebar_pinned', String(backup.sidebar_pinned));
        if (backup.audio_speed != null) operacoes.set('it_audio_speed', String(backup.audio_speed));
        if (backup.voz_preferida != null) operacoes.set('it_voz_preferida', String(backup.voz_preferida));
        if (backup.usar_voz_neural != null) operacoes.set('it_usar_voz_neural', String(backup.usar_voz_neural));
        if (backup.voz_neural_instalada != null) operacoes.set('it_voz_neural_instalada', String(backup.voz_neural_instalada));
        if (backup.imersao_usada != null) operacoes.set('it_imersao_usada', String(backup.imersao_usada));
        if (backup.palavra_dia != null) operacoes.set('it_palavra_dia', String(backup.palavra_dia));
        if (backup.tour_done != null) operacoes.set('it_tour_done', String(backup.tour_done));
        if (backup.ultimo_aviso_backup != null) operacoes.set('it_ultimo_aviso_backup', String(backup.ultimo_aviso_backup));

        for (const [k, v] of Object.entries(bookmarksSanitizados)) {
          operacoes.set(k, v);
        }

        // Sanitização de coleções custom
        if (Array.isArray(backup.canzoni_custom) && typeof Canzoni !== 'undefined' && Canzoni._sanitizarCanzone) {
          operacoes.set('it_canzoni_custom', JSON.stringify(backup.canzoni_custom.map(Canzoni._sanitizarCanzone).filter(Boolean)));
        } else if (Array.isArray(backup.canzoni_custom)) {
          operacoes.set('it_canzoni_custom', JSON.stringify(backup.canzoni_custom));
        }

        if (Array.isArray(backup.dialoghi_custom) && typeof Dialoghi !== 'undefined' && Dialoghi._sanitizarDialogo) {
          operacoes.set('it_dialoghi_custom', JSON.stringify(backup.dialoghi_custom.map(Dialoghi._sanitizarDialogo).filter(Boolean)));
        } else if (Array.isArray(backup.dialoghi_custom)) {
          operacoes.set('it_dialoghi_custom', JSON.stringify(backup.dialoghi_custom));
        }

        if (Array.isArray(backup.storie_custom) && typeof Storie !== 'undefined' && Storie._sanitizarStoria) {
          operacoes.set('it_storie_custom', JSON.stringify(backup.storie_custom.map(Storie._sanitizarStoria).filter(Boolean)));
        } else if (Array.isArray(backup.storie_custom)) {
          operacoes.set('it_storie_custom', JSON.stringify(backup.storie_custom));
        }

        if (Array.isArray(backup.imitazioni_custom)) operacoes.set('it_imitazioni_custom', JSON.stringify(backup.imitazioni_custom));
        if (Array.isArray(backup.vocab_custom)) operacoes.set('it_vocab_custom', JSON.stringify(backup.vocab_custom));
        if (Array.isArray(backup.canzoni_ocultas)) operacoes.set('it_canzoni_ocultas', JSON.stringify(backup.canzoni_ocultas));

        // SNAPSHOT DE SEGURANÇA
        const snapshot = new Map();
        for (const key of operacoes.keys()) {
          snapshot.set(key, localStorage.getItem(key));
        }

        // FASE 1: GRAVAÇÃO EM STAGING (it_stage_*)
        const stagingKeysEscritas = [];
        try {
          for (const [key, val] of operacoes.entries()) {
            const stagingKey = `it_stage_${key}`;
            localStorage.setItem(stagingKey, val);
            stagingKeysEscritas.push(stagingKey);
          }
        } catch (errStaging) {
          stagingKeysEscritas.forEach(k => { try { localStorage.removeItem(k); } catch (_) {} });
          throw new Error(`Falha no armazenamento durante preparação do backup: ${errStaging.message || 'Cota excedida'}. Nenhum dado foi alterado.`);
        }

        // FASE 2: COMMIT TRANSACIONAL PARA AS CHAVES OFICIAIS
        try {
          for (const [key] of operacoes.entries()) {
            const stagingKey = `it_stage_${key}`;
            const stagingVal = localStorage.getItem(stagingKey);
            localStorage.setItem(key, stagingVal);
            localStorage.removeItem(stagingKey);
          }
        } catch (errCommit) {
          // ROLLBACK TOTAL DO SNAPSHOT
          console.error('[Profilo.importarDados] Erro durante commit, executando rollback completo:', errCommit);
          for (const [snapKey, snapVal] of snapshot.entries()) {
            try {
              if (snapVal === null) localStorage.removeItem(snapKey);
              else localStorage.setItem(snapKey, snapVal);
            } catch (_) {}
          }
          stagingKeysEscritas.forEach(k => { try { localStorage.removeItem(k); } catch (_) {} });
          throw new Error(`Erro ao aplicar dados do backup. Estado anterior restaurado com sucesso: ${errCommit.message}`);
        }

        App.notificar('notif_backup_imp', 'sucesso');
        setTimeout(() => location.reload(), 1200);
      } catch(err) {
        App.notificar(I18n.t('notif_arquivo_inv') + ': ' + err.message, 'erro');
      }
    };
    reader.readAsText(file);
    event.target.value = '';
  },
```

---

### 4.3 Blueprint: Stored Content Sanitization

#### In `js/dialoghi.js`:
1. Add `Dialoghi._sanitizarDialogo(d)`:
   ```javascript
   _sanitizarDialogo(d) {
     if (!d || typeof d !== 'object') return null;
     const escFn = (typeof AppState !== 'undefined' && AppState.sanitizarTexto)
       ? AppState.sanitizarTexto
       : s => String(s || '').replace(/<[^>]*>?/gm, '').trim();

     return {
       ...d,
       id: String(d.id || `dial_custom_${Date.now()}`),
       titulo: escFn(d.titulo || 'Diálogo Sem Título'),
       nivel: ['A1','A2','B1','B2','C1','C2'].includes(d.nivel) ? d.nivel : 'A1',
       icone: escFn(d.icone || '💬').slice(0, 4),
       xp_recompensa: Number.isInteger(d.xp_recompensa) && d.xp_recompensa > 0 ? d.xp_recompensa : 20,
       turni: Array.isArray(d.turni) ? d.turni.map(t => ({
         personaggio: escFn(t.personaggio || 'Personaggio'),
         frase: escFn(t.frase || ''),
         traducao: escFn(t.traducao || ''),
         alternativas: Array.isArray(t.alternativas) ? t.alternativas.map(alt => escFn(alt)) : [],
         resposta_correta: Number.isInteger(t.resposta_correta) ? t.resposta_correta : 0
       })) : [],
       vocabulario_chave: Array.isArray(d.vocabulario_chave) ? d.vocabulario_chave.map(v => escFn(v)) : [],
       custom: true
     };
   },
   ```
2. In `Dialoghi.renderizarDialogo()`:
   Replace unescaped interpolations:
   - Line 404: `<div class="dialogo-nome">${this._esc(t.personaggio)}</div>`
   - Line 405: `<div>${this._esc(fraseExibir)} <button class="dialogo-audio-btn" data-fala="${this._esc(fraseExibir)}" onclick="App.pronunciar(this.dataset.fala)">🔊</button></div>`
   - Line 406: `${traducaoExibir ? `<div class="dialogo-traducao">${this._esc(traducaoExibir)}</div>` : ''}`
   - Line 429: `<div class="dialogo-nome">${this._esc(t.personaggio)}</div>`
   - Line 430: `<div>${this._esc(t.frase)}</div>`
   - Line 441: `<div class="dialogo-nome">${this._esc(t.personaggio)}</div>`
   - Line 442: `<div>${this._esc(t.frase)} <button class="dialogo-audio-btn" data-fala="${this._esc(t.frase)}" onclick="App.pronunciar(this.dataset.fala)">🔊</button></div>`
   - Line 443: `<div class="dialogo-traducao">${this._esc(t.traducao)}</div>`
   - Line 459: `<button class="dialogo-opcao" onclick="Dialoghi.checarResposta(${idx}, this)">${this._esc(alt)}</button>`
   - Line 537: `${(d.vocabulario_chave || []).map(v => `<span style="...">${this._esc(v)}</span>`).join('')}`

#### In `js/storie.js`:
1. Add `Storie._sanitizarStoria(s)`:
   ```javascript
   _sanitizarStoria(s) {
     if (!s || typeof s !== 'object') return null;
     const escFn = (typeof AppState !== 'undefined' && AppState.sanitizarTexto)
       ? AppState.sanitizarTexto
       : str => String(str || '').replace(/<[^>]*>?/gm, '').trim();

     return {
       ...s,
       id: String(s.id || `stor_custom_${Date.now()}`),
       titulo: escFn(s.titulo || s.titolo || 'História Sem Título'),
       titulo_pt: escFn(s.titulo_pt || s.titulo || ''),
       autor: escFn(s.autor || 'Italiano Autentico'),
       icone: escFn(s.icone || '📜').slice(0, 4),
       nivel: ['A1','A2','B1','B2','C1','C2'].includes(s.nivel) ? s.nivel : 'A1',
       descricao: escFn(s.descricao || s.tema || ''),
       descricao_pt: escFn(s.descricao_pt || s.descricao || ''),
       testo: Array.isArray(s.testo) ? s.testo.map((p, idx) => ({
         id: p.id || `p${idx}`,
         italiano: escFn(p.italiano || ''),
         portugues: escFn(p.portugues || ''),
         capituloTitulo: p.capituloTitulo ? escFn(p.capituloTitulo) : undefined,
         parole: Array.isArray(p.parole) ? p.parole.map(w => ({
           parola: escFn(w.parola || ''),
           traduzione: escFn(w.traduzione || ''),
           ipa: escFn(w.ipa || ''),
           categoria: escFn(w.categoria || '')
         })) : []
       })) : [],
       custom: true
     };
   },
   ```
2. In `Storie` rendering:
   - Line 630-631:
     `<span class="book-top-title">${this._escape(tituloExibido)}</span>`
     `<span class="book-top-subtitle">${this._escape(s.autor || 'Letteratura')} · ${this._escape(s.nivel)}</span>`
   - Lines 767-776 in `_obterHtmlConteudoPagina`:
     `<span class="antique-cover-icon">${this._escape(s.icone || '📖')}</span>`
     `<h2 class="antique-cover-title">${this._escape(tituloExibido)}</h2>`
     `<div class="antique-cover-subtitle">${this._escape(s.autor || 'Letteratura Italiana')} ${s.tema ? '· ' + this._escape(s.tema) : ''}</div>`
     `<span class="antique-running-head">${this._escape(pag.capituloTitulo || tituloExibido)}</span>`

#### In `js/canzoni.js`:
1. Add `Canzoni._sanitizarCanzone(can)`:
   ```javascript
   _sanitizarCanzone(c) {
     if (!c || typeof c !== 'object') return null;
     const escFn = (typeof AppState !== 'undefined' && AppState.sanitizarTexto)
       ? AppState.sanitizarTexto
       : str => String(str || '').replace(/<[^>]*>?/gm, '').trim();

     return {
       ...c,
       id: String(c.id || `can_custom_${Date.now()}`),
       titulo: escFn(c.titulo || 'Música Sem Título'),
       artista: escFn(c.artista || 'Artista Desconhecido'),
       icone: escFn(c.icone || '🎵').slice(0, 4),
       nivel: ['A1','A2','B1','B2','C1','C2'].includes(c.nivel) ? c.nivel : 'B1',
       letra_raw: typeof c.letra_raw === 'string' ? escFn(c.letra_raw) : '',
       estrofes: Array.isArray(c.estrofes) ? c.estrofes.map((e, idx) => ({
         id: e.id || idx + 1,
         texto_completo: escFn(e.texto_completo || ''),
         texto_lacuna: escFn(e.texto_lacuna || ''),
         palavra_oculta: escFn(e.palavra_oculta || ''),
         traducao: escFn(e.traducao || ''),
         dica: escFn(e.dica || '')
       })) : [],
       custom: true
     };
   },
   ```
2. In `Canzoni._renderizarPlayer` line 871:
   Escape double quotes for the HTML attribute:
   ```javascript
   const safeW = this._esc(w).replace(/'/g, "&#39;");
   ```

---

## 5. Verification Method

To independently verify the blueprint and its implementation:

1. **Verify Baseline Test Suite**:
   ```bash
   npm test
   ```
   *Expected outcome*: 15 test files pass, 104 tests pass.

2. **Verify Production Build**:
   ```bash
   npm run build
   ```
   *Expected outcome*: `tsc` and `vite build` complete with exit code 0.

3. **Verify Defensive Schema Loading (`tests/storage_corruption.test.ts`)**:
   Implement automated assertions:
   ```javascript
   // Injection of corrupted primitives
   localStorage.setItem('it_progresso', '"corrupted_primitive"');
   const p1 = AppState.carregarProgresso();
   expect(p1.nivel).toBe(1);
   expect(p1.templos_desbloqueados).toEqual([1]);

   // Injection of corrupted object with null array
   localStorage.setItem('it_progresso', JSON.stringify({ nivel: 'invalid', templos_desbloqueados: null }));
   const p2 = AppState.carregarProgresso();
   expect(p2.nivel).toBe(1);
   expect(Array.isArray(p2.templos_desbloqueados)).toBe(true);
   expect(p2.templos_desbloqueados.includes(1)).toBe(true);

   // Injection of corrupted flashcard deck
   localStorage.setItem('it_flashcards', '"corrupted_string"');
   expect(AppState.carregarFlashcards()).toEqual({});
   ```

4. **Verify Atomic Staging and Rollback (`tests/backup_integrity.test.ts`)**:
   Implement automated assertions:
   ```javascript
   // 1. Pre-flight schema rejection
   expect(() => Profilo._validarPayloadBackup({ versao: 4, progresso: { nivel: -1 } })).toThrow(/inválido/);

   // 2. Bookmarks regex validation & cap
   const bookmarksPayload = {
     'it_book_bm_valid_123': '5',
     'it_book_bm_<script>': '6',
     'random_key': '7'
   };
   const cleanBm = Profilo._sanitizarBookmarks(bookmarksPayload);
   expect(cleanBm['it_book_bm_valid_123']).toBe('5');
   expect(cleanBm['it_book_bm_<script>']).toBeUndefined();
   expect(cleanBm['random_key']).toBeUndefined();

   // 3. Staging and automatic rollback on QuotaExceededError
   localStorage.setItem('it_progresso', JSON.stringify({ nivel: 5, xp: 2500, templos_desbloqueados: [1, 2] }));
   vi.spyOn(Storage.prototype, 'setItem').mockImplementation((key) => {
     if (key.startsWith('it_stage_it_flashcards')) {
       const err = new Error('Quota exceeded');
       err.name = 'QuotaExceededError';
       throw err;
     }
   });
   // Attempt import with spy active
   // Verify that after failure:
   // - it_progresso remains { nivel: 5, xp: 2500 }
   // - zero it_stage_* keys remain in localStorage
   ```

5. **Verify Stored XSS Neutralization (`tests/security.test.js`)**:
   ```javascript
   const maliciousDialogue = {
     titulo: '<script>alert("xss")</script>Al Bar',
     turni: [{ personagem: '<img src=x onerror=alert(1)>', frase: '<b>Ciao!</b>' }]
   };
   const sanitized = Dialoghi._sanitizarDialogo(maliciousDialogue);
   expect(sanitized.titulo).not.toContain('<script>');
   expect(sanitized.turni[0].personaggio).not.toContain('<img');
   ```
