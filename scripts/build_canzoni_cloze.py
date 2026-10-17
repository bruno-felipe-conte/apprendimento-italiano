import sys, re

with open('js/canzoni.js', 'r', encoding='utf-8') as f:
    orig = f.read()

# 1. CanzoniAudioDB to prepend before Canzoni
audio_db_code = """// ============================================================
// CanzoniAudioDB: Armazenamento local de áudio (.mp3/.wav/.ogg) via IndexedDB
// ============================================================
const CanzoniAudioDB = {
  dbName: 'it_canzoni_audio_db',
  storeName: 'audios',
  _dbPromise: null,
  _getDB() {
    if (this._dbPromise) return this._dbPromise;
    this._dbPromise = new Promise((resolve) => {
      if (typeof indexedDB === 'undefined') return resolve(null);
      const req = indexedDB.open(this.dbName, 1);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName);
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => resolve(null);
    });
    return this._dbPromise;
  },
  async salvar(id, blob) {
    try {
      const db = await this._getDB();
      if (!db) return false;
      return new Promise((resolve) => {
        const tx = db.transaction(this.storeName, 'readwrite');
        tx.objectStore(this.storeName).put(blob, id);
        tx.oncomplete = () => resolve(true);
        tx.onerror = () => resolve(false);
      });
    } catch (_) { return false; }
  },
  async carregar(id) {
    try {
      const db = await this._getDB();
      if (!db) return null;
      return new Promise((resolve) => {
        const tx = db.transaction(this.storeName, 'readonly');
        const req = tx.objectStore(this.storeName).get(id);
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      });
    } catch (_) { return null; }
  },
  async excluir(id) {
    try {
      const db = await this._getDB();
      if (!db) return;
      const tx = db.transaction(this.storeName, 'readwrite');
      tx.objectStore(this.storeName).delete(id);
    } catch (_) {}
  }
};

"""

# Prepend CanzoniAudioDB
if 'const CanzoniAudioDB' not in orig:
    orig = audio_db_code + orig

# 2. Add Cloze properties to Canzoni
cloze_props = """  // ── Lyrics Cloze Player (Estado & Áudio) ──
  _audioReal: null,
  _audioBlobUrl: null,
  _clozeItems: [],
  _clozeWordBank: [],
  _clozeActiveVerseIdx: -1,
  _clozeIsFading: false,
  _clozeWaitingForAnswer: false,
  _cloze1stTryHits: 0,
  _clozeTotalBlanks: 0,
  _clozeVolume: 1.0,
  _clozePlaybackRate: 1.0,
  _clozeAudioSource: 'file',
  _clozeRafId: null,
  _clozeVirtualTimer: null,
  _clozeVirtualTime: 0,
"""
if '_clozeItems:' not in orig:
    orig = orig.replace("const Canzoni = {\n", "const Canzoni = {\n" + cloze_props, 1)

# 3. Patch pararAudio to also stop real audio and cancel cloze animations
orig = re.sub(
    r'pararAudio\(\)\s*\{[\s\S]*?if\s*\(\'speechSynthesis\'\s*in\s*window\)',
    """pararAudio() {
    this.tocandoKaraoke = false;
    if (this._timerKaraoke) {
      clearInterval(this._timerKaraoke);
      this._timerKaraoke = null;
    }
    if (this._clozeVirtualTimer) {
      clearInterval(this._clozeVirtualTimer);
      this._clozeVirtualTimer = null;
    }
    if (this._clozeRafId) {
      cancelAnimationFrame(this._clozeRafId);
      this._clozeRafId = null;
    }
    if (this._audioReal) {
      try { this._audioReal.pause(); } catch (_) {}
    }
    const btnCloze = document.getElementById('cloze-btn-play');
    if (btnCloze) {
      btnCloze.innerHTML = '▶ Reproduzir';
      btnCloze.classList.remove('playing');
    }
    if ('speechSynthesis' in window)""",
    orig
)

# 4. Patch renderizarSeletor to add Cloze Studio button and quick Cloze button on cards
old_search_line = """      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem">
        <input type="search" placeholder="${I18n.t('can_busca_ph')}" value="${this._filtroTexto}"
          oninput="Canzoni._filtroTexto=this.value;Canzoni.renderizarSeletor()"
          style="flex:1;min-width:0;padding:0.44rem 0.75rem;border:1.5px solid #ddd;border-radius:20px;font-size:0.875rem;font-family:inherit">
        <button class="btn-pill-add" onclick="Canzoni.abrirFormularioCriar()" style="white-space:nowrap">${I18n.t('can_btn_adicionar')}</button>
        <button class="btn-ia-add" onclick="IAImport.abrir('canzone')" style="white-space:nowrap">${I18n.t('can_btn_ia')}</button>
      </div>"""

new_search_line = """      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem;flex-wrap:wrap">
        <input type="search" placeholder="${I18n.t('can_busca_ph')}" value="${this._filtroTexto}"
          oninput="Canzoni._filtroTexto=this.value;Canzoni.renderizarSeletor()"
          style="flex:1;min-width:140px;padding:0.44rem 0.75rem;border:1.5px solid #ddd;border-radius:20px;font-size:0.875rem;font-family:inherit">
        <button class="btn-pill-add" onclick="Canzoni.abrirClozeStudio()" style="white-space:nowrap;background:linear-gradient(135deg,#3d0d18,#6b1a2a);border:1px solid #d4a843">${I18n.t('can_btn_cloze_studio')}</button>
        <button class="btn-pill-add" onclick="Canzoni.abrirFormularioCriar()" style="white-space:nowrap">${I18n.t('can_btn_adicionar')}</button>
        <button class="btn-ia-add" onclick="IAImport.abrir('canzone')" style="white-space:nowrap">${I18n.t('can_btn_ia')}</button>
      </div>"""

if old_search_line in orig:
    orig = orig.replace(old_search_line, new_search_line)
else:
    # try regex replacement
    orig = re.sub(
        r'<div style="display:flex;gap:0\.5rem;align-items:center;margin-bottom:0\.55rem[\s\S]*?<button class="btn-ia-add"[\s\S]*?<\/div>',
        new_search_line.strip(),
        orig,
        count=1
    )

old_card_badge = """<span style="font-size:0.68rem;color:#9B2335;background:rgba(155,35,53,0.08);padding:0.1rem 0.42rem;border-radius:8px;font-weight:600">${qtdVersos} ${I18n.t('can_versos_count')}</span>"""
new_card_badge = """<span style="font-size:0.68rem;color:#9B2335;background:rgba(155,35,53,0.08);padding:0.1rem 0.42rem;border-radius:8px;font-weight:600">${qtdVersos} ${I18n.t('can_versos_count')}</span>
          <button onclick="event.stopPropagation();Canzoni.iniciarCloze('${can.id}')" style="background:rgba(201,149,42,0.18);border:1px solid rgba(201,149,42,0.5);color:#6b1a2a;padding:0.1rem 0.45rem;border-radius:6px;font-size:0.68rem;font-weight:700;cursor:pointer" title="Treino Cloze Sincronizado">🎧 Cloze</button>"""

if old_card_badge in orig:
    orig = orig.replace(old_card_badge, new_card_badge)

# 5. Patch mudarModo to handle 'cloze'
old_mudar_modo = """  mudarModo(novoModo) {
    if (this.modoPlayer === novoModo) return;
    this.pararAudio();
    this.modoPlayer = novoModo;
    if (novoModo === 'karaoke') {
      this.estrofeAtual = 0;
      this._renderizarPlayer();
      this.iniciarSequenciaKaraoke(0);
    } else {
      // Volta para a primeira estrofe ainda não respondida
      const pendente = this.canzonAtual.estrofes.findIndex((e, i) => e.palavra_oculta && this.respostas[i] === null);
      this.estrofeAtual = pendente >= 0 ? pendente : 0;
      this._renderizarPlayer();
      setTimeout(() => this._tocarVersoSincronizado(this.estrofeAtual), 250);
    }
  },"""

new_mudar_modo = """  mudarModo(novoModo) {
    if (this.modoPlayer === novoModo) return;
    this.pararAudio();
    this.modoPlayer = novoModo;
    if (novoModo === 'cloze') {
      this.iniciarCloze(this.canzonAtual);
    } else if (novoModo === 'karaoke') {
      this.estrofeAtual = 0;
      this._renderizarPlayer();
      this.iniciarSequenciaKaraoke(0);
    } else {
      const pendente = (this.canzonAtual.estrofes || []).findIndex((e, i) => e.palavra_oculta && this.respostas[i] === null);
      this.estrofeAtual = pendente >= 0 ? pendente : 0;
      this._renderizarPlayer();
      setTimeout(() => this._tocarVersoSincronizado(this.estrofeAtual), 250);
    }
  },"""

if old_mudar_modo in orig:
    orig = orig.replace(old_mudar_modo, new_mudar_modo)

# 6. Add Cloze mode tab in can-mode-tabs
old_tabs = """          <div class="can-mode-tabs">
            `<button class="can-mode-tab ${this.modoPlayer==='praticar'?'active':''}" onclick="Canzoni.mudarModo('praticar')">${I18n.t('can_modo_praticar')}</button>` +
            `<button class="can-mode-tab ${this.modoPlayer==='karaoke'?'active':''}" onclick="Canzoni.mudarModo('karaoke')">${I18n.t('can_modo_karaoke')}</button>` +
          '</div>' +"""

new_tabs = """          <div class="can-mode-tabs">
            `<button class="can-mode-tab ${this.modoPlayer==='praticar'?'active':''}" onclick="Canzoni.mudarModo('praticar')">${I18n.t('can_modo_praticar')}</button>` +
            `<button class="can-mode-tab ${this.modoPlayer==='karaoke'?'active':''}" onclick="Canzoni.mudarModo('karaoke')">${I18n.t('can_modo_karaoke')}</button>` +
            `<button class="can-mode-tab ${this.modoPlayer==='cloze'?'active':''}" onclick="Canzoni.mudarModo('cloze')">${I18n.t('can_modo_cloze')}</button>` +
          '</div>' +"""

if old_tabs in orig:
    orig = orig.replace(old_tabs, new_tabs)

# 7. Add Cloze Studio and Lyrics Cloze Player implementation methods
cloze_methods = """
  // ─────────────────────────────────────────────────────────────
  // 🎧 LYRICS CLOZE PLAYER (Treino Auditivo Musical Sincronizado)
  // ─────────────────────────────────────────────────────────────

  // ── 1. STUDIO DE IMPORTAÇÃO (Upload de Áudio + Letra .lrc / Texto) ──
  abrirClozeStudio(idEditar = null) {
    this.pararAudio();
    const c = document.getElementById('canzoni-container');
    if (!c) return;

    const can = idEditar ? this.todasCanzoni().find(x => x.id === idEditar) : null;
    const titulo = can ? can.titulo : '';
    const artista = can ? can.artista : '';

    let lrcExemplo = `[00:02.00] Una mattina mi sono {{alzato}}
[00:06.50] O bella ciao, bella ciao, bella ciao ciao ciao!
[00:11.20] Una mattina mi sono alzato e ho {{trovato}} l'invasor
[00:17.80] O partigiano, {{portami}} via, ché mi sento di morir`;

    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Canzoni.renderizarSeletor()">‹ Voltar</button>
        <span style="font-size:0.95rem;font-weight:700">${I18n.t('can_cloze_studio_title')}</span>
      </div>

      <div class="cloze-studio-box">
        <div style="font-size:0.88rem;color:#6b1a2a;line-height:1.55;margin-bottom:1.2rem">
          Importe uma música real (arquivo de áudio) e sincronize com a letra em formato <strong>.lrc</strong> ou texto corrido.
          O sistema criará o <strong>Lyrics Cloze Player</strong> com pausas suaves, desfoque e banco de palavras.
        </div>

        <!-- Dropzone de Arquivo de Áudio -->
        <div class="cloze-upload-dropzone" id="cloze-dropzone" onclick="document.getElementById('cloze-audio-file').click()">
          <input type="file" id="cloze-audio-file" accept=".mp3,.wav,.ogg,audio/*" style="display:none" onchange="Canzoni._onStudioFileSelect(this)">
          <div style="font-size:2rem;margin-bottom:0.35rem">📁</div>
          <div style="font-weight:700;font-size:0.95rem;color:#3d0d18" id="cloze-file-name">${I18n.t('can_cloze_upload_audio')}</div>
          <div style="font-size:0.78rem;color:#777;margin-top:0.25rem">${I18n.t('can_cloze_upload_desc')}</div>
          <audio id="cloze-audio-preview" controls style="display:none;margin:0.8rem auto 0;max-width:320px;width:100%"></audio>
        </div>

        <!-- Metadados -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1rem">
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Título da Música *</label>
            <input id="cloze-titulo" type="text" value="${titulo}" placeholder="Ex: Bella Ciao"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.9rem">
          </div>
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Artista / Intérprete</label>
            <input id="cloze-artista" type="text" value="${artista}" placeholder="Ex: Canto Popolare"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.9rem">
          </div>
        </div>

        <!-- Letra com .lrc ou {{...}} -->
        <div style="margin-bottom:1rem">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem">
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">${I18n.t('can_cloze_letra_label')}</label>
            <span style="font-size:0.74rem;color:#777">Dica: use <code>{{palavra}}</code> para marcar lacunas</span>
          </div>
          <textarea id="cloze-letra" rows="8" placeholder="${lrcExemplo}"
            style="width:100%;padding:0.65rem;border:2px solid #ddd;border-radius:8px;font-family:monospace;font-size:0.85rem;line-height:1.5">${lrcExemplo}</textarea>
          <div style="font-size:0.76rem;color:#777;margin-top:0.3rem">${I18n.t('can_cloze_letra_desc')}</div>
        </div>

        <!-- Densidade de lacunas -->
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.4rem;flex-wrap:wrap">
          <span style="font-size:0.82rem;font-weight:700;color:#9B2335">${I18n.t('can_cloze_densidade')}:</span>
          <label style="font-size:0.82rem;cursor:pointer"><input type="radio" name="cloze-dens" value="padrao" checked> 1 por verso (Padrão)</label>
          <label style="font-size:0.82rem;cursor:pointer"><input type="radio" name="cloze-dens" value="leve"> Leve (1 a cada 2 versos)</label>
          <label style="font-size:0.82rem;cursor:pointer"><input type="radio" name="cloze-dens" value="todas"> Intensa (Todas as chaves)</label>
        </div>

        <!-- Ações -->
        <div style="display:flex;gap:0.6rem;flex-wrap:wrap">
          <button class="btn-primario" style="flex:1" onclick="Canzoni._iniciarClozeDoStudio()">
            ${I18n.t('can_cloze_iniciar')}
          </button>
          <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">Cancelar</button>
        </div>
      </div>
    `;

    // Drag and drop no dropzone
    const dz = document.getElementById('cloze-dropzone');
    if (dz) {
      dz.ondragover = (e) => { e.preventDefault(); dz.style.background = 'rgba(155,35,53,0.12)'; };
      dz.ondragleave = () => { dz.style.background = ''; };
      dz.ondrop = (e) => {
        e.preventDefault();
        dz.style.background = '';
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
          const inp = document.getElementById('cloze-audio-file');
          inp.files = e.dataTransfer.files;
          Canzoni._onStudioFileSelect(inp);
        }
      };
    }
  },

  _tempStudioFile: null,

  _onStudioFileSelect(input) {
    if (!input.files || !input.files[0]) return;
    const file = input.files[0];
    this._tempStudioFile = file;

    const nameEl = document.getElementById('cloze-file-name');
    const dz = document.getElementById('cloze-dropzone');
    const preview = document.getElementById('cloze-audio-preview');

    if (nameEl) nameEl.textContent = `🎵 ${file.name} (${Math.round(file.size / 1024)} KB)`;
    if (dz) dz.classList.add('has-file');

    if (preview) {
      preview.src = URL.createObjectURL(file);
      preview.style.display = 'block';
    }

    // Auto-preenche título se vazio
    const titInput = document.getElementById('cloze-titulo');
    if (titInput && !titInput.value.trim()) {
      const cleanName = file.name.replace(/\.[^/.]+$/, '').replace(/[-_]/g, ' ');
      titInput.value = cleanName;
    }
  },

  async _iniciarClozeDoStudio() {
    const titulo = document.getElementById('cloze-titulo')?.value.trim() || 'Minha Música Sincronizada';
    const artista = document.getElementById('cloze-artista')?.value.trim() || 'Artista';
    const letra = document.getElementById('cloze-letra')?.value.trim() || '';
    const densidade = document.querySelector('input[name="cloze-dens"]:checked')?.value || 'padrao';

    if (!letra) {
      App.notificar('Por favor, informe a letra da música.', 'erro');
      return;
    }

    const songId = `cloze_${Date.now()}`;
    const file = this._tempStudioFile;

    // Se tiver arquivo, salva no IndexedDB
    if (file) {
      await CanzoniAudioDB.salvar(songId, file);
    }

    // Monta objeto da música
    const customSong = {
      id: songId,
      titulo,
      artista,
      nivel: 'B1',
      icone: '🎧',
      letra_raw: letra,
      densidade,
      tem_audio_local: !!file,
      estrofes: [] // preenchido via parser
    };

    // Salva no catálogo customizado
    this.custom.unshift(customSong);
    this._salvarCustom();

    // Inicia o player Cloze
    this.iniciarCloze(customSong, file, letra, densidade);
  },

  // ── 2. INICIALIZAÇÃO DO LYRICS CLOZE PLAYER ──
  async iniciarCloze(canOuId, audioFileOuBlob = null, rawLetra = null, densidade = 'padrao') {
    this.pararAudio();
    await this.carregar();

    let can = typeof canOuId === 'string' ? this.todasCanzoni().find(c => c.id === canOuId) : canOuId;
    if (!can) return;
    this.canzonAtual = can;
    this.modoPlayer = 'cloze';

    // 1. Obtém áudio: do parâmetro, do IndexedDB ou monta fallback TTS
    let audioBlob = audioFileOuBlob;
    if (!audioBlob) {
      audioBlob = await CanzoniAudioDB.carregar(can.id);
    }

    // 2. Extrai letra bruta
    let textoLetra = rawLetra || can.letra_raw;
    if (!textoLetra && can.estrofes && can.estrofes.length) {
      textoLetra = can.estrofes.map(e => e.texto_completo || e.texto_lacuna || '').join('\\n');
    }

    // 3. Configura áudio se houver blob
    if (audioBlob) {
      this._configurarAudioElement(audioBlob);
    } else {
      this._clozeAudioSource = 'tts';
    }

    // 4. Parser de timestamps e geração de lacunas Cloze
    const duracaoEstimada = (this._audioReal && this._audioReal.duration) ? this._audioReal.duration : 0;
    const parsed = this._parseLRCOrText(textoLetra, duracaoEstimada);
    const { clozeItems, wordBankWords } = this._processarVersosParaCloze(parsed, densidade);

    this._clozeItems = clozeItems;
    this._clozeTotalBlanks = clozeItems.filter(it => it.blank).length;
    this._cloze1stTryHits = 0;
    this._clozeActiveVerseIdx = -1;
    this._clozeWaitingForAnswer = false;
    this._clozeWordBank = this._embaralharWordBank(wordBankWords);

    // 5. Renderiza a interface do Cloze Player
    this._renderizarClozePlayer();

    // 6. Inicia o loop de monitoramento
    this._iniciarLoopClozeSync();
  },

  // Parser para .lrc [mm:ss.xx] ou texto puro
  _parseLRCOrText(texto, duracaoAudio = 0) {
    if (!texto) return [];
    const linhas = texto.split(/\\r?\\n/).map(l => l.trim()).filter(Boolean);
    const lrcRegex = /^\\[(\\d{1,2}):(\\d{2})(?:[.:](\\d{1,3}))?\\](.*)$/;
    const parsed = [];

    let hasLRC = false;
    for (const l of linhas) {
      const match = l.match(lrcRegex);
      if (match) {
        hasLRC = true;
        const min = parseInt(match[1], 10);
        const sec = parseInt(match[2], 10);
        let ms = match[3] ? parseInt(match[3], 10) : 0;
        if (match[3] && match[3].length === 2) ms *= 10;
        const timeSec = min * 60 + sec + (ms / 1000);
        const content = match[4].trim();
        if (content) {
          parsed.push({ startTime: timeSec, text: content });
        }
      }
    }

    if (!hasLRC || parsed.length === 0) {
      const step = (duracaoAudio > 10 && linhas.length > 0) ? (duracaoAudio / (linhas.length + 0.5)) : 4.5;
      for (let i = 0; i < linhas.length; i++) {
        parsed.push({
          startTime: i * step,
          endTime: (i + 1) * step,
          text: linhas[i]
        });
      }
    } else {
      parsed.sort((a, b) => a.startTime - b.startTime);
      for (let i = 0; i < parsed.length; i++) {
        if (i < parsed.length - 1) {
          parsed[i].endTime = Math.max(parsed[i].startTime + 1.2, parsed[i + 1].startTime);
        } else {
          parsed[i].endTime = duracaoAudio > parsed[i].startTime ? duracaoAudio : parsed[i].startTime + 5.0;
        }
      }
    }

    return parsed;
  },

  // Gera lacunas Cloze (via {{...}} ou automático com seleção inteligente)
  _processarVersosParaCloze(parsedVerses, densidade = 'padrao') {
    const stopwords = new Set([
      'il','lo','la','i','gli','le','un','uno','una',"un'",
      'e','ed','o','od','ma','se','non','che','chi','cui',
      'di','a','da','in','con','su','per','tra','fra',
      'del','dello','della','dei','degli','delle',
      'al','allo','alla','ai','agli','alle',
      'dal','dallo','dalla','dai','dagli','dalle',
      'nel','nello','nella','nei','negli','nelle',
      'sul','sullo','sulla','sui','sugli','sulle',
      'mi','ti','si','ci','vi','me','te','lui','lei','noi','voi','loro'
    ]);

    const clozeItems = [];
    const wordBankWords = [];
    let blankCounter = 0;

    for (let i = 0; i < parsedVerses.length; i++) {
      const v = parsedVerses[i];
      const rawText = v.text || '';

      let customWord = null;
      const mCurlys = rawText.match(/\\{\\{([^}]+)\\}\\}/);
      if (mCurlys) {
        customWord = mCurlys[1].trim();
      } else if (v.palavra_oculta) {
        customWord = v.palavra_oculta.trim();
      }

      const cleanLine = rawText.replace(/\\{\\{([^}]+)\\}\\}/g, '$1');
      const parts = cleanLine.split(/([A-Za-zÀ-ÖØ-öø-ÿ]+(?:'[A-Za-zÀ-ÖØ-öø-ÿ]+)?)/g);
      const wordsInLine = parts.filter(p => /^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:'[A-Za-zÀ-ÖØ-öø-ÿ]+)?$/.test(p));
      let chosenWord = customWord;

      if (!chosenWord && wordsInLine.length > 0) {
        if (densidade !== 'leve' || i % 2 === 0) {
          const candidatos = wordsInLine.filter(w => w.length >= 4 && !stopwords.has(w.toLowerCase()));
          if (candidatos.length > 0) {
            chosenWord = candidatos.sort((a,b) => b.length - a.length)[0];
          } else if (wordsInLine.length > 0) {
            chosenWord = wordsInLine[wordsInLine.length - 1];
          }
        }
      }

      const norm = s => String(s || '').toLowerCase().trim();
      let blankObj = null;
      const tokens = [];

      let wordIndex = 0;
      for (const part of parts) {
        if (/^[A-Za-zÀ-ÖØ-öø-ÿ]+(?:'[A-Za-zÀ-ÖØ-öø-ÿ]+)?$/.test(part)) {
          if (chosenWord && norm(part) === norm(chosenWord) && !blankObj) {
            const bId = `blank_${blankCounter++}`;
            const totalW = Math.max(1, wordsInLine.length);
            const ratio = Math.min(0.85, (wordIndex + 0.3) / totalW);
            const pauseTime = v.startTime + (v.endTime - v.startTime) * ratio;

            blankObj = {
              blankId: bId,
              verseIdx: i,
              word: part,
              pauseTime: pauseTime,
              status: 'blurred',
              attempts: 0,
              firstTry: true
            };
            tokens.push({ text: part, isBlank: true, blankId: bId });
            wordBankWords.push(part);
          } else {
            tokens.push({ text: part, isBlank: false });
          }
          wordIndex++;
        } else if (part) {
          tokens.push({ text: part, isBlank: false, isPunct: true });
        }
      }

      clozeItems.push({
        idx: i,
        startTime: v.startTime,
        endTime: v.endTime,
        rawText: cleanLine,
        traducao: v.traducao || '',
        tokens,
        blank: blankObj
      });
    }

    return { clozeItems, wordBankWords };
  },

  _embaralharWordBank(words) {
    const arr = words.map((w, i) => ({ id: `wb_${i}_${Date.now()}`, word: w, used: false }));
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  },

  _configurarAudioElement(blobOuUrl) {
    if (this._audioReal) {
      try { this._audioReal.pause(); } catch (_) {}
    }
    const audio = new Audio();
    if (typeof blobOuUrl === 'string') {
      audio.src = blobOuUrl;
    } else if (blobOuUrl instanceof Blob) {
      if (this._audioBlobUrl) URL.revokeObjectURL(this._audioBlobUrl);
      this._audioBlobUrl = URL.createObjectURL(blobOuUrl);
      audio.src = this._audioBlobUrl;
    }
    audio.playbackRate = this._clozePlaybackRate || 1.0;
    audio.volume = this._clozeVolume || 1.0;

    audio.ontimeupdate = () => this._onClozeTimeUpdate();
    audio.onended = () => this._onClozeAudioEnded();
    audio.onerror = () => {
      this._clozeAudioSource = 'tts';
      App.notificar('Usando sintetizador vocal sincronizado.', 'alerta');
    };

    this._audioReal = audio;
    this._clozeAudioSource = 'file';
  },

  // ── 3. RENDERIZADOR DO CLOZE PLAYER ──
  _renderizarClozePlayer() {
    const c = document.getElementById('canzoni-container');
    if (!c || !this.canzonAtual) return;
    const can = this.canzonAtual;

    const total = Math.max(1, this._clozeTotalBlanks);
    const hits = this._cloze1stTryHits;
    const pct = Math.round((hits / total) * 100);

    // Versos com spans e lacunas com blur(5px)
    let versesHtml = '';
    this._clozeItems.forEach((v, i) => {
      let lineHtml = '';
      v.tokens.forEach(t => {
        if (t.isBlank) {
          const isTarget = v.blank && v.blank.status === 'blurred' && (!this._clozeItems.slice(0, i).some(x => x.blank && x.blank.status === 'blurred'));
          const cls = v.blank.status === 'correct' ? 'is-correct' : (v.blank.status === 'wrong' ? 'is-wrong' : 'is-blurred');
          const targetCls = isTarget ? ' is-target' : '';
          lineHtml += `<span class="cloze-blank ${cls}${targetCls}" id="${t.blankId}" data-word="${this._esc(t.text)}">${this._esc(t.text)}</span>`;
        } else {
          lineHtml += this._esc(t.text);
        }
      });

      versesHtml += `
        <div class="cloze-verse is-future" id="cloze-verse-${i}" onclick="Canzoni._pularParaVersoCloze(${i})">
          <div style="font-size:0.68rem;color:#9B2335;font-weight:700;margin-bottom:0.15rem;letter-spacing:0.04em">
            VERSO ${i + 1}/${this._clozeItems.length}
          </div>
          <div class="cloze-line">${lineHtml}</div>
        </div>
      `;
    });

    // Pílulas do Word Bank
    const pillsHtml = this._clozeWordBank.map(wb => {
      const usedCls = wb.used ? ' is-used' : '';
      const safeWord = this._esc(wb.word).replace(/'/g, "\\\\'");
      return `<button class="cloze-pill${usedCls}" id="${wb.id}" onclick="Canzoni._clozeSelecionarPalavra('${safeWord}', '${wb.id}')">${this._esc(wb.word)}</button>`;
    }).join('');

    const speedLabel = this._clozePlaybackRate === 0.7 ? '🐢 0.7x' : this._clozePlaybackRate === 0.85 ? '🎧 0.85x' : '🐇 1.0x';
    const isPlaying = this._audioReal && !this._audioReal.paused && !this._audioReal.ended;

    c.innerHTML = `
      <div class="cloze-player">
        <!-- Topbar -->
        <div class="cloze-topbar">
          <button class="can-back-btn" onclick="Canzoni.renderizarSeletor()" title="Voltar">&#8249;</button>
          <div class="cloze-song-meta">
            <div class="cloze-song-title">${this._esc(can.icone || '🎵')} ${this._esc(can.titulo)}</div>
            <div class="cloze-song-artist">${this._esc(can.artista || '')}</div>
          </div>
          <div class="cloze-stats-badge" id="cloze-acc-badge">
            🎯 <span id="cloze-acc-val">${pct}%</span> (${hits}/${total})
          </div>
        </div>

        <!-- Abas de Modo -->
        <div class="can-controls-bar">
          <div class="can-mode-tabs">
            <button class="can-mode-tab" onclick="Canzoni.mudarModo('praticar')">${I18n.t('can_modo_praticar')}</button>
            <button class="can-mode-tab" onclick="Canzoni.mudarModo('karaoke')">${I18n.t('can_modo_karaoke')}</button>
            <button class="can-mode-tab active" onclick="Canzoni.mudarModo('cloze')">${I18n.t('can_modo_cloze')}</button>
          </div>
          <div class="can-audio-tools">
            <button class="can-ctrl-btn" onclick="document.getElementById('cloze-anexar-input').click()" title="Carregar MP3 desta música">
              ${I18n.t('can_cloze_anexar_audio')}
            </button>
            <input type="file" id="cloze-anexar-input" accept=".mp3,.wav,.ogg,audio/*" style="display:none" onchange="Canzoni._onAnexarAudioMusica(this)">
          </div>
        </div>

        <!-- Controles de Áudio / Barra de Progresso -->
        <div class="cloze-controls-strip">
          <div class="cloze-audio-btns">
            <button id="cloze-btn-play" class="cloze-btn-ctrl primary ${isPlaying ? 'playing' : ''}" onclick="Canzoni.togglePlayPauseCloze()">
              ${isPlaying ? '⏸ Pausar' : '▶ Reproduzir'}
            </button>
            <button class="cloze-btn-ctrl" onclick="Canzoni.alternarVelocidadeCloze()">${speedLabel}</button>
          </div>

          <div class="cloze-progress-line-wrap">
            <span id="cloze-time-cur">0:00</span>
            <div class="cloze-progress-track" onclick="Canzoni._seekCloze(event)">
              <div class="cloze-progress-bar" id="cloze-prog-bar"></div>
            </div>
            <span id="cloze-time-dur">0:00</span>
          </div>
        </div>

        <!-- Banner de Espera / Pausa Suave -->
        <div class="cloze-waiting-banner" id="cloze-waiting-banner" style="display:none">
          ${I18n.t('can_cloze_waiting_msg')}
        </div>

        <!-- Área de Letra Karaokê -->
        <div class="cloze-lyrics-stage" id="cloze-lyrics-stage">
          ${versesHtml}
        </div>

        <!-- Banco de Palavras (Word Bank) -->
        <div class="cloze-wordbank-container">
          <div class="cloze-wordbank-label">${I18n.t('can_cloze_wordbank_label')}</div>
          <div class="cloze-wordbank-grid" id="cloze-wordbank-grid">
            ${pillsHtml}
          </div>
        </div>
      </div>
    `;

    // Atualiza timers de áudio
    if (this._audioReal && this._audioReal.duration) {
      const durSpan = document.getElementById('cloze-time-dur');
      if (durSpan) durSpan.textContent = this._formatarTempo(this._audioReal.duration);
    }
  },

  // ── 4. CONTROLES DE REPRODUÇÃO & FADE ──
  togglePlayPauseCloze() {
    if (this._clozeAudioSource === 'file' && this._audioReal) {
      if (this._audioReal.paused) {
        this._clozeWaitingForAnswer = false;
        this._atualizarUIWaitingBanner(false);
        this._audioReal.play().then(() => {
          this._fadeAudio(0, this._clozeVolume || 1.0, 200);
          this._atualizarBtnPlay(true);
        }).catch(err => {
          App.notificar('Clique para permitir reprodução de áudio.', 'alerta');
        });
      } else {
        this._fadeAudio(this._audioReal.volume, 0, 180, () => {
          this._audioReal.pause();
          this._atualizarBtnPlay(false);
        });
      }
    } else {
      // Modo virtual / TTS timeline
      this._toggleVirtualTTS();
    }
  },

  _atualizarBtnPlay(isPlaying) {
    const btn = document.getElementById('cloze-btn-play');
    if (btn) {
      btn.innerHTML = isPlaying ? '⏸ Pausar' : '▶ Reproduzir';
      if (isPlaying) btn.classList.add('playing');
      else btn.classList.remove('playing');
    }
  },

  alternarVelocidadeCloze() {
    const vels = [0.7, 0.85, 1.0];
    const idx = vels.indexOf(this._clozePlaybackRate || 1.0);
    this._clozePlaybackRate = vels[(idx + 1) % vels.length];
    if (this._audioReal) {
      this._audioReal.playbackRate = this._clozePlaybackRate;
    }
    this._renderizarClozePlayer();
  },

  _fadeAudio(fromVol, toVol, durationMs = 200, onDone = null) {
    if (!this._audioReal || this._clozeAudioSource !== 'file') {
      if (onDone) onDone();
      return;
    }
    const audio = this._audioReal;
    const start = performance.now();
    this._clozeIsFading = true;

    const step = (now) => {
      const elapsed = now - start;
      const progress = Math.min(1, elapsed / durationMs);
      const cur = fromVol + (toVol - fromVol) * progress;
      audio.volume = Math.max(0, Math.min(1, cur));
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        this._clozeIsFading = false;
        audio.volume = Math.max(0, Math.min(1, toVol));
        if (onDone) onDone();
      }
    };
    requestAnimationFrame(step);
  },

  _seekCloze(e) {
    const track = e.currentTarget;
    const rect = track.getBoundingClientRect();
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));

    if (this._clozeAudioSource === 'file' && this._audioReal && this._audioReal.duration) {
      this._audioReal.currentTime = pos * this._audioReal.duration;
      this._onClozeTimeUpdate();
    } else {
      const items = this._clozeItems;
      const totalDur = items[items.length - 1]?.endTime || 60;
      this._clozeVirtualTime = pos * totalDur;
      this._onVirtualTimeUpdate(this._clozeVirtualTime, totalDur);
    }
  },

  _pularParaVersoCloze(idx) {
    const item = this._clozeItems[idx];
    if (!item) return;
    if (this._clozeAudioSource === 'file' && this._audioReal) {
      this._audioReal.currentTime = item.startTime;
      if (this._audioReal.paused) this.togglePlayPauseCloze();
    } else {
      this._clozeVirtualTime = item.startTime;
      this._falarVersoTTS(item);
    }
  },

  async _onAnexarAudioMusica(input) {
    if (!input.files || !input.files[0] || !this.canzonAtual) return;
    const file = input.files[0];
    await CanzoniAudioDB.salvar(this.canzonAtual.id, file);
    App.notificar('Áudio salvo e sincronizado para esta música!', 'sucesso');
    this.iniciarCloze(this.canzonAtual, file);
  },

  // ── 5. MOTOR DE SINCRONIZAÇÃO EM TEMPO REAL (Karaokê + Cloze Monitor) ──
  _iniciarLoopClozeSync() {
    if (this._clozeRafId) cancelAnimationFrame(this._clozeRafId);

    const checkLoop = () => {
      if (this.modoPlayer === 'cloze' && this._audioReal && !this._audioReal.paused) {
        this._onClozeTimeUpdate();
      }
      if (this.modoPlayer === 'cloze') {
        this._clozeRafId = requestAnimationFrame(checkLoop);
      }
    };
    this._clozeRafId = requestAnimationFrame(checkLoop);
  },

  _onClozeTimeUpdate() {
    if (this.modoPlayer !== 'cloze') return;
    const audio = this._audioReal;
    if (!audio) return;

    const curTime = audio.currentTime;
    const duration = audio.duration || 1;

    // Barra de progresso e timer
    const bar = document.getElementById('cloze-prog-bar');
    if (bar) bar.style.width = `${Math.min(100, (curTime / duration) * 100)}%`;
    const curSpan = document.getElementById('cloze-time-cur');
    if (curSpan) curSpan.textContent = this._formatarTempo(curTime);

    // Verso ativo (Efeito Karaokê com scale 1.06 e iluminação)
    const items = this._clozeItems;
    let activeIdx = -1;
    for (let i = 0; i < items.length; i++) {
      if (curTime >= items[i].startTime && curTime < items[i].endTime) {
        activeIdx = i;
        break;
      }
    }
    if (activeIdx === -1 && curTime >= (items[items.length - 1]?.endTime || 0)) {
      activeIdx = items.length - 1;
    }

    if (activeIdx !== -1 && activeIdx !== this._clozeActiveVerseIdx) {
      this._clozeActiveVerseIdx = activeIdx;
      this._atualizarDestaqueVersos(activeIdx);
    }

    // ── Monitoramento de Lacuna: Cenário B (Fade-out suave 200ms e Pause) ──
    const pendingBlanks = items.map(it => it.blank).filter(b => b && b.status === 'blurred');
    if (pendingBlanks.length > 0) {
      const target = pendingBlanks[0];
      if (curTime >= target.pauseTime && !this._clozeWaitingForAnswer && !this._clozeIsFading) {
        this._clozeWaitingForAnswer = true;
        this._fadeAudio(audio.volume, 0, 200, () => {
          audio.pause();
          this._atualizarBtnPlay(false);
          this._atualizarUIWaitingBanner(true, target);
        });
      }
    }
  },

  _atualizarDestaqueVersos(activeIdx) {
    const stage = document.getElementById('cloze-lyrics-stage');
    if (!stage) return;
    const verses = stage.querySelectorAll('.cloze-verse');
    verses.forEach((vEl, idx) => {
      if (idx === activeIdx) {
        vEl.classList.add('is-active');
        vEl.classList.remove('is-past', 'is-future');
      } else if (idx < activeIdx) {
        vEl.classList.remove('is-active', 'is-future');
        vEl.classList.add('is-past');
      } else {
        vEl.classList.remove('is-active', 'is-past');
        vEl.classList.add('is-future');
      }
    });

    // Rolagem suave centralizada
    const activeEl = document.getElementById(`cloze-verse-${activeIdx}`);
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  },

  _atualizarUIWaitingBanner(mostrar, targetBlank = null) {
    const b = document.getElementById('cloze-waiting-banner');
    if (b) {
      b.style.display = mostrar ? 'block' : 'none';
      if (mostrar) {
        b.innerHTML = `${I18n.t('can_cloze_waiting_msg')}`;
      }
    }
    // Destaque na lacuna com pulso
    document.querySelectorAll('.cloze-blank.is-target').forEach(el => el.classList.remove('is-target'));
    if (mostrar && targetBlank) {
      const el = document.getElementById(targetBlank.blankId);
      if (el) el.classList.add('is-target');
    }
  },

  // ── 6. SELEÇÃO NO WORD BANK (Cenário A vs Cenário B) ──
  _clozeSelecionarPalavra(palavra, pillId) {
    if (this.modoPlayer !== 'cloze') return;
    const items = this._clozeItems;
    const pendingBlanks = items.map(it => it.blank).filter(b => b && b.status === 'blurred');
    if (pendingBlanks.length === 0) return;

    const target = pendingBlanks[0];
    const norm = s => String(s || '').toLowerCase().trim().normalize('NFD').replace(/[\\u0300-\\u036f]/g, '');
    const acertou = norm(palavra) === norm(target.word);

    const blankEl = document.getElementById(target.blankId);
    const pillEl = document.getElementById(pillId);

    if (acertou) {
      // ── ACERTO (Verde #10b981 em definitivo) ──
      target.status = 'correct';
      target.firstTry = (target.attempts === 0);
      if (target.firstTry) {
        this._cloze1stTryHits++;
      }

      if (blankEl) {
        blankEl.classList.remove('is-blurred', 'is-target', 'is-wrong');
        blankEl.classList.add('is-correct');
        blankEl.textContent = target.word;
      }

      if (pillEl) {
        pillEl.classList.add('is-used');
      }

      const wbObj = this._clozeWordBank.find(x => x.id === pillId);
      if (wbObj) wbObj.used = true;

      if (typeof SomFeedback !== 'undefined' && SomFeedback.correto) {
        SomFeedback.correto();
      }

      this._atualizarStatsBadge();

      // Cenário B vs Cenário A:
      if (this._clozeWaitingForAnswer) {
        // Estava pausado: retoma com fade-in suave de 200ms
        this._clozeWaitingForAnswer = false;
        this._atualizarUIWaitingBanner(false);
        if (this._audioReal) {
          this._audioReal.play().then(() => {
            this._fadeAudio(0, this._clozeVolume || 1.0, 200);
            this._atualizarBtnPlay(true);
          }).catch(() => {});
        } else if (this._clozeAudioSource === 'tts') {
          this._continuarTTSAposAcerto();
        }
      } else {
        // Cenário A: Antecipação! A música continua tocando sem interrupção!
        const nextPending = items.map(it => it.blank).filter(b => b && b.status === 'blurred');
        if (nextPending.length > 0) {
          const nextEl = document.getElementById(nextPending[0].blankId);
          if (nextEl) nextEl.classList.add('is-target');
        }
      }

      // Se todas as lacunas acabaram
      const restam = items.map(it => it.blank).filter(b => b && b.status === 'blurred');
      if (restam.length === 0) {
        setTimeout(() => {
          this._mostrarResultadoCloze();
        }, 1200);
      }
    } else {
      // ── ERRO (Vermelho #ef4444 + Shake) ──
      target.attempts++;
      target.firstTry = false;

      if (blankEl) {
        blankEl.classList.add('is-error-shake', 'is-wrong');
        setTimeout(() => {
          blankEl.classList.remove('is-error-shake');
          if (target.status === 'blurred') blankEl.classList.remove('is-wrong');
        }, 450);
      }

      if (pillEl) {
        pillEl.classList.add('is-error-shake', 'is-wrong-pill');
        setTimeout(() => {
          pillEl.classList.remove('is-error-shake', 'is-wrong-pill');
        }, 450);
      }

      if (typeof SomFeedback !== 'undefined' && SomFeedback.errado) {
        SomFeedback.errado();
      }
    }
  },

  _atualizarStatsBadge() {
    const hits = this._cloze1stTryHits;
    const total = Math.max(1, this._clozeTotalBlanks);
    const pct = Math.round((hits / total) * 100);
    const b = document.getElementById('cloze-acc-badge');
    if (b) {
      b.innerHTML = `🎯 <span id="cloze-acc-val">${pct}%</span> (${hits}/${total})`;
    }
  },

  _onClozeAudioEnded() {
    this._mostrarResultadoCloze();
  },

  // ── 7. RESULTADO & RECOMPENSA DE XP ──
  _mostrarResultadoCloze() {
    this.pararAudio();
    const can = this.canzonAtual;
    const total = Math.max(1, this._clozeTotalBlanks);
    const hits = this._cloze1stTryHits;
    const pct = Math.round((hits / total) * 100);

    const xpBase = can?.xp_recompensa || 35;
    const xpGanho = Math.max(15, Math.round(xpBase * (0.5 + 0.5 * (pct / 100))));

    // Envia XP para o estado global
    if (typeof App !== 'undefined' && App.ganharXP) {
      App.ganharXP(xpGanho);
    }
    try {
      window.dispatchEvent(new CustomEvent('kora:xp-bonus', {
        detail: { xp: xpGanho, accuracy: pct, firstTryHits: hits, totalBlanks: total, source: 'lyrics-cloze' }
      }));
    } catch (_) {}

    const c = document.getElementById('canzoni-container');
    if (!c) return;

    const emoji = pct >= 80 ? '🏆' : pct >= 50 ? '🎧' : '🎼';
    const items = this._clozeItems;
    const listWords = items.filter(it => it.blank).map(it => {
      const b = it.blank;
      const ehVerde = b.firstTry;
      return `<span style="display:inline-block;padding:0.25rem 0.65rem;border-radius:999px;font-size:0.84rem;font-weight:700;margin:0.2rem;background:${ehVerde ? 'rgba(16,185,129,0.15)' : 'rgba(239,68,68,0.15)'};color:${ehVerde ? '#10b981' : '#ef4444'};border:1px solid ${ehVerde ? '#10b981' : '#ef4444'}">${ehVerde ? '✓' : '✗'} ${b.word}</span>`;
    }).join('');

    c.innerHTML = `
      <div class="cloze-player">
        <div class="can-result">
          <div class="can-result-emoji">${emoji}</div>
          <div class="can-result-title">${this._esc(can?.titulo || 'Música')} — ${I18n.t('can_cloze_concluido')}</div>
          <div style="font-size:0.92rem;color:#6b1a2a;margin-top:0.4rem;font-weight:600">${I18n.t('can_cloze_precisao')}:</div>
          <div class="can-result-score">${pct}% <span>(${hits}/${total})</span></div>
          <div class="can-result-xp">+${xpGanho} XP</div>

          <div style="max-width:480px;margin:1.2rem auto 0;text-align:center">
            ${listWords}
          </div>

          <div style="display:flex;gap:0.5rem;justify-content:center;margin-top:1.5rem;flex-wrap:wrap">
            <button class="can-restart-btn" onclick="Canzoni.iniciarCloze(Canzoni.canzonAtual)">🔄 Jogar Novamente (Cloze)</button>
            <button class="can-restart-btn secundario" onclick="Canzoni.mudarModo('praticar')">✏️ Modo Normal</button>
            <button class="can-restart-btn secundario" onclick="Canzoni.renderizarSeletor()">${I18n.t('can_res_catalogo')}</button>
          </div>
        </div>
      </div>
    `;
  },

  // ── 8. FALLBACK SINCRONIZADO VIA TTS (Para Músicas sem MP3) ──
  _toggleVirtualTTS() {
    if (this._clozeVirtualTimer) {
      clearInterval(this._clozeVirtualTimer);
      this._clozeVirtualTimer = null;
      if ('speechSynthesis' in window) window.speechSynthesis.cancel();
      this._atualizarBtnPlay(false);
    } else {
      this._atualizarBtnPlay(true);
      const items = this._clozeItems;
      const totalDur = items[items.length - 1]?.endTime || 60;

      this._clozeVirtualTimer = setInterval(() => {
        if (this._clozeWaitingForAnswer) return;
        this._clozeVirtualTime += 0.25;
        this._onVirtualTimeUpdate(this._clozeVirtualTime, totalDur);
      }, 250);
    }
  },

  _onVirtualTimeUpdate(curTime, totalDur) {
    const bar = document.getElementById('cloze-prog-bar');
    if (bar) bar.style.width = `${Math.min(100, (curTime / totalDur) * 100)}%`;
    const curSpan = document.getElementById('cloze-time-cur');
    if (curSpan) curSpan.textContent = this._formatarTempo(curTime);

    const items = this._clozeItems;
    let activeIdx = -1;
    for (let i = 0; i < items.length; i++) {
      if (curTime >= items[i].startTime && curTime < items[i].endTime) {
        activeIdx = i;
        break;
      }
    }
    if (activeIdx !== -1 && activeIdx !== this._clozeActiveVerseIdx) {
      this._clozeActiveVerseIdx = activeIdx;
      this._atualizarDestaqueVersos(activeIdx);
      this._falarVersoTTS(items[activeIdx]);
    }

    // Monitora lacunas pendentes
    const pendingBlanks = items.map(it => it.blank).filter(b => b && b.status === 'blurred');
    if (pendingBlanks.length > 0) {
      const target = pendingBlanks[0];
      if (curTime >= target.pauseTime && !this._clozeWaitingForAnswer) {
        this._clozeWaitingForAnswer = true;
        if ('speechSynthesis' in window) window.speechSynthesis.cancel();
        this._atualizarBtnPlay(false);
        this._atualizarUIWaitingBanner(true, target);
      }
    }
  },

  _falarVersoTTS(item) {
    if (!('speechSynthesis' in window) || !item) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(item.rawText);
    u.lang = 'it-IT';
    u.rate = this._clozePlaybackRate || 0.85;
    if (typeof App !== 'undefined' && App._vozItaliana) {
      u.voice = App._vozItaliana;
    }
    window.speechSynthesis.speak(u);
  },

  _continuarTTSAposAcerto() {
    this._atualizarBtnPlay(true);
    const activeItem = this._clozeItems[this._clozeActiveVerseIdx];
    if (activeItem) {
      this._falarVersoTTS(activeItem);
    }
  },

  _formatarTempo(segundos) {
    const s = Math.floor(segundos || 0);
    const min = Math.floor(s / 60);
    const sec = s % 60;
    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
  },
"""

# Insert cloze_methods right before the last closing brace and document.addEventListener
last_brace = orig.rfind('};\n\ndocument.addEventListener')
if last_brace == -1:
    last_brace = orig.rfind('};')

if last_brace != -1:
    orig = orig[:last_brace] + cloze_methods + orig[last_brace:]
else:
    print("Could not find end of Canzoni object")
    sys.exit(1)

with open('js/canzoni.js', 'w', encoding='utf-8') as f:
    f.write(orig)

print("Successfully patched js/canzoni.js!")
