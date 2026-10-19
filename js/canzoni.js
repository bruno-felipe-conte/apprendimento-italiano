// ============================================================
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

const Canzoni = {
  // ── Lyrics Cloze Player (Estado & Áudio) ──
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
  dados: null,        // built-in (data/canzoni.json)
  custom: [],         // criados pelo usuário (localStorage)
  _ocultas: [],       // IDs de nativas ocultadas pelo usuário
  canzonAtual: null,
  estrofeAtual: 0,
  acertos: 0,
  erros: 0,
  respostas: [],
  traduzirVisivel: true,
  modoPlayer: 'praticar', // 'karaoke' | 'praticar'
  tocandoKaraoke: false,
  velocidadeAudio: 0.85,
  _timerKaraoke: null,
  _opcoesAtuais: null,
  _estrofeOpcoesIdx: -1,
  modoEdicao: false,  // true quando está criando/editando

  // ── Carregar built-in + custom (Stale-While-Revalidate) ────
  async carregar() {
    // 1. Hidrata do cache local imediatamente se disponível
    if (!this.dados) {
      try {
        const cached = localStorage.getItem('it_swr_canzoni');
        if (cached) {
          this.dados = JSON.parse(cached);
          // Revalida em background sem bloquear a UI
          fetch('data/canzoni.json')
            .then(r => r.ok ? r.json() : null)
            .then(fresh => {
              if (fresh && Array.isArray(fresh.canzoni)) {
                this.dados = fresh;
                try { localStorage.setItem('it_swr_canzoni', JSON.stringify(fresh)); } catch (_) {}
              }
            })
            .catch(() => {});
        }
      } catch (_) {}
    }

    // Se ainda não há dados em cache, busca na rede
    if (!this.dados) {
      try {
        const r = await fetch('data/canzoni.json');
        if (r.ok) {
          this.dados = await r.json();
          try { localStorage.setItem('it_swr_canzoni', JSON.stringify(this.dados)); } catch (_) {}
        } else {
          this.dados = { canzoni: [] };
        }
      } catch { this.dados = { canzoni: [] }; }
    }
    // 2. Carrega custom do localStorage
    try {
      this.custom = JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]');
    } catch { this.custom = []; }
    // 3. Carrega lista de nativas ocultas
    try {
      this._ocultas = JSON.parse(localStorage.getItem('it_canzoni_ocultas') || '[]');
    } catch { this._ocultas = []; }
  },

  _filtroOrigem: '', // '' | 'custom' | 'nativo'

  // ── Retorna TODAS as músicas — custom primeiro, excluindo ocultas ──
  todasCanzoni() {
    const nativas = (this.dados?.canzoni || []).filter(c => !this._ocultas.includes(c.id));
    return [...this.custom, ...nativas];
  },

  // ── Salvar custom no localStorage ─────────────────────────
  _salvarCustom() {
    localStorage.setItem('it_canzoni_custom', JSON.stringify(this.custom));
  },

  // ── Ocultar música nativa (Optimistic UI) ─────────────────
  ocultarNativa(id, cardEl = null) {
    const can = (this.dados?.canzoni || []).find(c => c.id === id);
    if (!can) return;
    if (!confirm(`Ocultar "${can.titulo}"?\nEla desaparece da lista mas pode ser restaurada depois.`)) return;
    if (cardEl && cardEl.classList) cardEl.classList.add('optimistic-removing');
    if (!this._ocultas.includes(id)) this._ocultas.push(id);
    try {
      localStorage.setItem('it_canzoni_ocultas', JSON.stringify(this._ocultas));
      App.notificar(I18n.t('notif_can_ocultada'), 'alerta');
      setTimeout(() => this.renderizarSeletor(), cardEl ? 180 : 0);
    } catch (_) {
      this._ocultas = this._ocultas.filter(x => x !== id);
      if (cardEl) cardEl.classList.remove('optimistic-removing');
    }
  },

  // ── Restaurar todas as nativas ocultas ─────────────────────
  restaurarNativas() {
    if (!this._ocultas.length) return;
    this._ocultas = [];
    localStorage.removeItem('it_canzoni_ocultas');
    App.notificar(I18n.t('notif_can_restauradas'), 'sucesso');
    this.renderizarSeletor();
  },

  // ── Renderizar seletor com built-in + custom + botão criar + avaliar ──
  _filtroNivel: '',
  _filtroTexto: '',

  async renderizarSeletor() {
    this.pararAudio();
    const c = document.getElementById('canzoni-container');
    if (!c) return;

    await this.carregar();

    const todas = this.todasCanzoni();
    const niveis = ['A1','A2','B1','B2','C1','C2'];
    const counts = {};
    todas.forEach(s => { counts[s.nivel] = (counts[s.nivel]||0)+1; });

    let filtradas = todas;
    if (this._filtroOrigem === 'custom') filtradas = filtradas.filter(s => s.custom || s._custom);
    if (this._filtroOrigem === 'nativo') filtradas = filtradas.filter(s => !s.custom && !s._custom);
    if (this._filtroNivel) filtradas = filtradas.filter(s => s.nivel === this._filtroNivel);
    if (this._filtroTexto) {
      const q = this._filtroTexto.toLowerCase();
      filtradas = filtradas.filter(s => s.titulo.toLowerCase().includes(q) || (s.artista||'').toLowerCase().includes(q));
    }

    const nC=todas.filter(s=>s.custom||s._custom).length, nN=todas.length-nC, _o=this._filtroOrigem;
    const nOcultas = this._ocultas.length;
    const _oPill=(v,l,ct)=>`<button onclick="Canzoni._filtroOrigem='${v}';Canzoni.renderizarSeletor()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid ${_o===v?'#7B68A0':'#ddd'};background:${_o===v?'#7B68A0':'transparent'};color:${_o===v?'#fff':'inherit'};cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap">${l} (${ct})</button>`;

    let html = `
      <!-- Linha 1: busca + ações -->
      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem;flex-wrap:wrap">
        <input type="search" placeholder="${I18n.t('can_busca_ph')}" value="${this._filtroTexto}"
          oninput="Canzoni._filtroTexto=this.value;Canzoni.renderizarSeletor()"
          style="flex:1;min-width:140px;padding:0.44rem 0.75rem;border:1.5px solid #ddd;border-radius:20px;font-size:0.875rem;font-family:inherit">
        <button class="btn-pill-add" onclick="Canzoni.abrirClozeStudio()">${I18n.t('can_btn_cloze_studio')}</button>
        <button class="btn-ia-add" onclick="IAImport.abrir('canzone')" style="white-space:nowrap">${I18n.t('can_btn_ia')}</button>
      </div>
      <!-- Linha 2: filtros numa só linha -->
      <div style="display:flex;gap:0.35rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
        ${_oPill('', I18n.t('can_filtro_todas'), todas.length)}
        ${nC?_oPill('custom', I18n.t('can_filtro_adicionadas'), nC):''}
        ${nN?_oPill('nativo', I18n.t('can_filtro_classicos'), nN):''}
        <select class="nivel-select${this._filtroNivel?' ativo':''}"
          onchange="Canzoni._filtroNivel=this.value;Canzoni.renderizarSeletor()">
          <option value="">${I18n.t('can_filtro_nivel')}</option>
          ${niveis.filter(n=>counts[n]).map(n=>`<option value="${n}" ${this._filtroNivel===n?'selected':''}>${n} (${counts[n]})</option>`).join('')}
        </select>
        ${nOcultas ? `<button onclick="Canzoni.restaurarNativas()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid #c9952a;background:rgba(201,149,42,0.1);color:#7a5a00;cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap;font-family:inherit">${I18n.t('can_restaurar')} (${nOcultas})</button>` : ''}
      </div>
      <div class="dialogo-grid">`;

    for (const can of filtradas) {
      const ehCustom = can.custom || can._custom;
      const badgeCustom = ehCustom ? `<span style="font-size:0.65rem;background:#7B68A0;color:white;padding:0.1rem 0.4rem;border-radius:6px;margin-left:0.3rem;">${I18n.t('can_badge_minha')}</span>` : '';
      const qtdVersos = (can.estrofes || []).length;
      html += `<div class="dialogo-card" onclick="Canzoni.abrirCanzone('${can.id}')">
        <div class="dialogo-icone">${can.icone || '🎵'}</div>
        <div class="dialogo-titulo">${can.titulo}${badgeCustom}</div>
        <div style="font-size:0.75rem;color:#888;margin:0.2rem 0">${can.artista || ''}</div>
        <div style="display:flex;gap:0.3rem;justify-content:center;flex-wrap:wrap;margin-top:0.3rem;align-items:center;">
          <span class="dialogo-nivel">${can.nivel}</span>
          <span style="font-size:0.68rem;color:#9B2335;background:rgba(155,35,53,0.08);padding:0.1rem 0.42rem;border-radius:8px;font-weight:600">${qtdVersos} ${I18n.t('can_versos_count')}</span>
          <button onclick="event.stopPropagation();Canzoni.iniciarCloze('${can.id}')" style="background:rgba(201,149,42,0.18);border:1px solid rgba(201,149,42,0.5);color:#6b1a2a;padding:0.1rem 0.45rem;border-radius:6px;font-size:0.68rem;font-weight:700;cursor:pointer" title="Treino Cloze Sincronizado">🎧 Cloze</button>
          ${ehCustom ? `
          ${can.custom ? `<button onclick="event.stopPropagation();Canzoni.editarCanzone('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Editar">✏️</button>` : ''}
          <button onclick="event.stopPropagation();Canzoni.excluirCanzone('${can.id}', this.closest('.dialogo-card'))" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Excluir">🗑️</button>`
          : `<button onclick="event.stopPropagation();Canzoni.ocultarNativa('${can.id}', this.closest('.dialogo-card'))" style="background:none;border:none;cursor:pointer;font-size:0.85rem;opacity:0.4;transition:opacity 0.15s" onmouseenter="this.style.opacity=1" onmouseleave="this.style.opacity=0.4" title="Ocultar esta música">🗑️</button>`}
        </div>
      </div>`;
    }

    if (filtradas.length === 0) {
      html += `<p style="text-align:center;color:#aaa;grid-column:1/-1">${this._filtroTexto ? I18n.t('can_sem_resultado') : I18n.t('can_sem_musica')}</p>`;
    }

    html += '</div>';
    c.innerHTML = html;
  },

  // ── Formulário de CRIAÇÃO ──────────────────────────────────
  abrirFormularioCriar(idEditar = null) {
    this.pararAudio();
    const c = document.getElementById('canzoni-container');
    if (!c) return;
    this.modoEdicao = true;

    const existente = idEditar ? this.custom.find(x => x.id === idEditar) : null;
    const titulo = existente?.titulo || '';
    const artista = existente?.artista || '';
    const nivel = existente?.nivel || 'A2';
    const icone = existente?.icone || '🎵';
    const estrofes = existente?.estrofes || [{ id: 1, texto_completo: '', texto_lacuna: '', palavra_oculta: '', traducao: '', dica: '' }];

    let estrofesHtml = '';
    estrofes.forEach((est, i) => {
      estrofesHtml += Canzoni._htmlEstrofeForm(est, i);
    });

    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Canzoni.renderizarSeletor()">‹ Cancelar</button>
        <span style="font-size:0.9rem;font-weight:700">${idEditar ? 'Editar Música' : 'Nova Música'}</span>
      </div>

      <div class="gram-card" style="margin-top:1rem;padding:1.2rem">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1rem">
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Título *</label>
            <input id="can-titulo" type="text" value="${titulo}" placeholder="Ex: Bella Ciao"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.9rem">
          </div>
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Artista</label>
            <input id="can-artista" type="text" value="${artista}" placeholder="Ex: Tradicional"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.9rem">
          </div>
        </div>

        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1.2rem">
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">${I18n.idioma === 'it' ? 'Livello' : 'Nível'}</label>
            <select id="can-nivel" style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.9rem">
              ${['A1','A2','B1','B2','C1'].map(n => `<option ${n===nivel?'selected':''}>${n}</option>`).join('')}
            </select>
          </div>
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">${I18n.idioma === 'it' ? 'Icona (emoji)' : 'Ícone (emoji)'}</label>
            <input id="can-icone" type="text" value="${icone}" maxlength="4"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:1.2rem;text-align:center">
          </div>
        </div>

        <div style="font-size:0.85rem;font-weight:700;color:#9B2335;margin-bottom:0.8rem;border-top:1px solid #f0e8d8;padding-top:1rem">
          📝 Estrofes (versos com lacunas)
        </div>

        <div id="can-estrofes">${estrofesHtml}</div>

        <button onclick="Canzoni._adicionarEstrofe()" class="btn-secondario" style="width:100%;margin:0.8rem 0">
          ➕ Adicionar verso
        </button>

        <div style="background:#FFF8E7;border:1px solid #D4A843;border-radius:8px;padding:0.8rem;margin-bottom:1rem;font-size:0.82rem;color:#6B4C1A">
          💡 <strong>Como criar a lacuna:</strong> Escreva o texto completo no campo "Texto completo".
          No "Texto com lacuna", substitua a palavra que quer ocultar por <code>___</code> (três underscores).
          Informe a palavra oculta no campo "Palavra oculta".
        </div>

        <div style="display:flex;gap:0.5rem">
          <button class="btn-primario" style="flex:1" onclick="Canzoni._salvarFormulario('${idEditar || ''}')">
            💾 Salvar Música
          </button>
          <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">Cancelar</button>
        </div>
      </div>`;
  },

  _htmlEstrofeForm(est, i) {
    return `
      <div class="can-estrofe-form" id="can-est-${i}" style="background:#f9f6f0;border-radius:10px;padding:0.9rem;margin-bottom:0.8rem;border:1px solid #ede5d5">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem">
          <span style="font-weight:700;font-size:0.82rem;color:#9B2335">Verso ${i + 1}</span>
          <button onclick="Canzoni._removerEstrofe(${i})" style="background:none;border:none;cursor:pointer;color:#C0392B;font-size:0.85rem">🗑️ Remover</button>
        </div>
        <div style="display:flex;flex-direction:column;gap:0.5rem">
          <input type="text" placeholder="Texto completo (ex: Cerco l'estate tutto l'anno)" data-campo="texto_completo" data-idx="${i}"
            value="${est.texto_completo || ''}"
            style="padding:0.45rem 0.6rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem">
          <input type="text" placeholder="Texto com lacuna (ex: Cerco l'___ tutto l'anno)" data-campo="texto_lacuna" data-idx="${i}"
            value="${est.texto_lacuna || ''}"
            style="padding:0.45rem 0.6rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem">
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem">
            <input type="text" placeholder="Palavra oculta (ex: estate)" data-campo="palavra_oculta" data-idx="${i}"
              value="${est.palavra_oculta || ''}"
              style="padding:0.45rem 0.6rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem">
            <input type="text" placeholder="Dica (ex: Estação quente do ano)" data-campo="dica" data-idx="${i}"
              value="${est.dica || ''}"
              style="padding:0.45rem 0.6rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem">
          </div>
          <input type="text" placeholder="Tradução em português" data-campo="traducao" data-idx="${i}"
            value="${est.traducao || ''}"
            style="padding:0.45rem 0.6rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem">
        </div>
      </div>`;
  },

  _adicionarEstrofe() {
    const container = document.getElementById('can-estrofes');
    if (!container) return;
    const i = container.querySelectorAll('.can-estrofe-form').length;
    const div = document.createElement('div');
    div.innerHTML = this._htmlEstrofeForm({ id: i+1, texto_completo:'', texto_lacuna:'', palavra_oculta:'', traducao:'', dica:'' }, i);
    container.appendChild(div.firstElementChild);
  },

  _removerEstrofe(i) {
    const el = document.getElementById(`can-est-${i}`);
    if (el) el.remove();
    document.querySelectorAll('.can-estrofe-form').forEach((el, idx) => {
      el.id = `can-est-${idx}`;
      el.querySelector('span').textContent = `Verso ${idx + 1}`;
      el.querySelectorAll('[data-idx]').forEach(inp => inp.dataset.idx = idx);
      el.querySelector('button[onclick]').setAttribute('onclick', `Canzoni._removerEstrofe(${idx})`);
    });
  },

  _salvarFormulario(idEditar) {
    const titulo = document.getElementById('can-titulo')?.value.trim();
    if (!titulo) { App.notificar('notif_can_titulo_obr', 'erro'); return; }

    const estrofes = [];
    document.querySelectorAll('.can-estrofe-form').forEach((el, i) => {
      const campos = {};
      el.querySelectorAll('[data-campo]').forEach(inp => { campos[inp.dataset.campo] = inp.value.trim(); });
      if (campos.texto_completo && campos.palavra_oculta) {
        if (!campos.texto_lacuna && campos.palavra_oculta) {
          campos.texto_lacuna = campos.texto_completo.replace(campos.palavra_oculta, '___');
        }
        estrofes.push({ id: i+1, ...campos });
      }
    });
    if (estrofes.length === 0) { App.notificar('notif_can_sem_verso', 'erro'); return; }

    const nova = {
      id: idEditar || `custom_can_${Date.now()}`,
      titulo,
      artista: document.getElementById('can-artista')?.value.trim() || '',
      nivel: document.getElementById('can-nivel')?.value || 'A2',
      icone: document.getElementById('can-icone')?.value.trim() || '🎵',
      tema: 'custom',
      criado_em: Date.now(),
      custom: true,
      estrofes,
      vocabulario_chave: estrofes.map(e => e.palavra_oculta).filter(Boolean),
      xp_recompensa: Math.min(10 + estrofes.length * 5, 60)
    };

    if (idEditar) {
      const idx = this.custom.findIndex(x => x.id === idEditar);
      if (idx >= 0) this.custom[idx] = nova; else this.custom.push(nova);
    } else {
      this.custom.push(nova);
    }
    this._salvarCustom();
    App.notificar(I18n.t('can_salva').replace('{t}', titulo), 'sucesso');
    this.renderizarSeletor();
  },

  editarCanzone(id) {
    this.abrirFormularioCriar(id);
  },

  excluirCanzone(id, cardEl = null) {
    const can = this.custom.find(x => x.id === id);
    if (!can) return;
    if (!confirm(I18n.t('can_excluir_confirm').replace('{t}', can.titulo))) return;
    if (cardEl && cardEl.classList) cardEl.classList.add('optimistic-removing');
    const backup = [...this.custom];
    this.custom = this.custom.filter(x => x.id !== id);
    try {
      this._salvarCustom();
      App.notificar('notif_can_excluida', 'alerta');
      setTimeout(() => this.renderizarSeletor(), cardEl ? 180 : 0);
    } catch (_) {
      this.custom = backup;
      if (cardEl) cardEl.classList.remove('optimistic-removing');
    }
  },

  // ── MOTOR DE KARAOKÊ E JOGO DE LACUNAS ──────────────────────
  pararAudio() {
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
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
    document.querySelectorAll('.can-word-speaking').forEach(el => el.classList.remove('can-word-speaking'));
    const btnPlay = document.getElementById('can-btn-play-main');
    if (btnPlay) {
      btnPlay.innerHTML = I18n.t('can_btn_ouvir_verso');
      btnPlay.classList.remove('playing');
    }
  },

  async abrirCanzone(id) {
    this.pararAudio();
    await this.carregar();
    this.canzonAtual = this.todasCanzoni().find(c => c.id === id);
    if (!this.canzonAtual) return;
    this.estrofeAtual = 0;
    this.acertos = 0;
    this.erros = 0;
    this.respostas = this.canzonAtual.estrofes.map(() => null);
    this.traduzirVisivel = true;
    this._opcoesAtuais = null;
    this._estrofeOpcoesIdx = -1;
    this._avancarProximoBlank(true);
  },

  mudarModo(novoModo) {
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
  },

  alternarVelocidade() {
    const vels = [0.7, 0.85, 1.0];
    const idx = vels.indexOf(this.velocidadeAudio);
    this.velocidadeAudio = vels[(idx + 1) % vels.length];
    const btn = document.getElementById('can-speed-btn');
    if (btn) {
      const label = this.velocidadeAudio === 0.7 ? '🐢 0.7x' : this.velocidadeAudio === 0.85 ? '🎧 0.85x' : '🐇 1.0x';
      btn.innerHTML = label;
    }
    if (this.tocandoKaraoke) {
      this._tocarVersoSincronizado(this.estrofeAtual);
    }
  },

  togglePlayPause() {
    if (this.tocandoKaraoke) {
      this.pararAudio();
    } else {
      if (this.modoPlayer === 'karaoke') {
        this.iniciarSequenciaKaraoke(this.estrofeAtual);
      } else {
        this._tocarVersoSincronizado(this.estrofeAtual);
      }
    }
  },

  iniciarSequenciaKaraoke(idxInicial = 0) {
    const can = this.canzonAtual;
    if (!can) return;
    if (idxInicial >= can.estrofes.length) idxInicial = 0;
    this.estrofeAtual = idxInicial;
    this._renderizarPlayer();
    this._tocarVersoSincronizado(this.estrofeAtual, () => {
      if (!this.tocandoKaraoke || this.modoPlayer !== 'karaoke') return;
      if (this.estrofeAtual + 1 < can.estrofes.length) {
        this.estrofeAtual++;
        this._renderizarPlayer();
        setTimeout(() => {
          if (this.modoPlayer === 'karaoke') {
            this.iniciarSequenciaKaraoke(this.estrofeAtual);
          }
        }, 550);
      } else {
        this.pararAudio();
      }
    });
  },

  tocarEstrofeEspecifica(idx) {
    this.pararAudio();
    if (this.modoPlayer === 'karaoke') {
      this.iniciarSequenciaKaraoke(idx);
    } else {
      this._tocarVersoSincronizado(idx);
    }
  },

  _tocarVersoSincronizado(idx, aoTerminar = null) {
    const can = this.canzonAtual;
    if (!can || !can.estrofes[idx]) return;
    this.pararAudio();

    const est = can.estrofes[idx];
    const texto = est.texto_completo || '';
    if (!texto) return;

    this.tocandoKaraoke = true;
    const btnPlay = document.getElementById('can-btn-play-main');
    if (btnPlay) {
      btnPlay.innerHTML = I18n.t('can_btn_pausar_audio');
      btnPlay.classList.add('playing');
    }

    const verseEl = document.getElementById(`can-verse-${idx}`);
    if (verseEl) {
      verseEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    const wordSpans = verseEl ? Array.from(verseEl.querySelectorAll('.can-word')) : [];

    // Calcula limites de caracteres por palavra para mapear onboundary(charIndex)
    const limites = [];
    let cursor = 0;
    wordSpans.forEach((span, wIdx) => {
      const wText = span.dataset.raw || span.textContent || '';
      const pos = texto.indexOf(wText, cursor);
      const start = pos >= 0 ? pos : cursor;
      const end = start + wText.length;
      cursor = end;
      limites.push({ start, end, span, wIdx });
    });

    const destacarPalavra = (wIdx) => {
      wordSpans.forEach((s, i) => {
        if (i === wIdx) s.classList.add('can-word-speaking');
        else s.classList.remove('can-word-speaking');
      });
    };

    let boundaryAtivo = false;
    let palavraCursor = 0;

    // Fallback progressivo por timer (caso o navegador não dispare onboundary em vozes remotas)
    const duracaoPorPalavraMs = Math.max(280, Math.round(420 / (this.velocidadeAudio || 0.85)));
    if (wordSpans.length > 0) {
      destacarPalavra(0);
    }
    this._timerKaraoke = setInterval(() => {
      if (!this.tocandoKaraoke) {
        clearInterval(this._timerKaraoke);
        this._timerKaraoke = null;
        return;
      }
      if (!boundaryAtivo && wordSpans.length > 0) {
        palavraCursor++;
        if (palavraCursor < wordSpans.length) {
          destacarPalavra(palavraCursor);
        }
      }
    }, duracaoPorPalavraMs);

    if (!('speechSynthesis' in window)) {
      setTimeout(() => {
        this.pararAudio();
        if (aoTerminar) aoTerminar();
      }, wordSpans.length * duracaoPorPalavraMs + 400);
      return;
    }

    const textoNormalizado = (typeof VoiceEngine !== 'undefined')
      ? VoiceEngine.normalizarParaFala(texto)
      : texto;

    const u = new SpeechSynthesisUtterance(textoNormalizado);
    u.lang = 'it-IT';
    u.rate = this.velocidadeAudio || 0.85;

    let voz = (typeof VoiceEngine !== 'undefined') ? VoiceEngine.obterVozSelecionada() : null;
    if (!voz && typeof App !== 'undefined') {
      voz = App._getVozItaliana();
    }
    if (voz) u.voice = voz;

    window._activeUtterance = u;

    u.onboundary = (ev) => {
      if (ev.name === 'word' || typeof ev.charIndex === 'number') {
        boundaryAtivo = true;
        const cIdx = ev.charIndex;
        const item = limites.find(l => cIdx >= l.start - 1 && cIdx <= l.end + 1)
                  || limites.find(l => l.start >= cIdx);
        if (item) {
          destacarPalavra(item.wIdx);
        }
      }
    };

    u.onend = () => {
      if (window._activeUtterance === u) {
        window._activeUtterance = null;
      }
      if (this._timerKaraoke) {
        clearInterval(this._timerKaraoke);
        this._timerKaraoke = null;
      }
      wordSpans.forEach(s => s.classList.remove('can-word-speaking'));
      const estavaTocando = this.tocandoKaraoke;
      this.tocandoKaraoke = false;
      const b = document.getElementById('can-btn-play-main');
      if (b) {
        b.innerHTML = I18n.t('can_btn_ouvir_verso');
        b.classList.remove('playing');
      }
      if (estavaTocando && aoTerminar) {
        aoTerminar();
      }
    };

    u.onerror = () => {
      if (window._activeUtterance === u) {
        window._activeUtterance = null;
      }
      this.pararAudio();
    };

    try {
      if (window.speechSynthesis.paused) window.speechSynthesis.resume();
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    } catch (_) {
      this.pararAudio();
    }
  },

  _avancarProximoBlank(autoPlay = true) {
    const can = this.canzonAtual;
    if (!can) return;
    while (this.estrofeAtual < can.estrofes.length && !can.estrofes[this.estrofeAtual].palavra_oculta) {
      this.estrofeAtual++;
    }
    if (this.estrofeAtual >= can.estrofes.length) {
      this._renderizarPlayer();
      setTimeout(() => this.mostrarResultado(), 700);
    } else {
      this._opcoesAtuais = null;
      this._estrofeOpcoesIdx = -1;
      this._renderizarPlayer();
      if (autoPlay) {
        setTimeout(() => this._tocarVersoSincronizado(this.estrofeAtual), 280);
      }
    }
  },

  _gerarOpcoes(est) {
    if (this._estrofeOpcoesIdx === this.estrofeAtual && Array.isArray(this._opcoesAtuais)) {
      return this._opcoesAtuais;
    }
    const can = this.canzonAtual;
    const correta = est.palavra_oculta;
    const norm = s => String(s || '').toLowerCase().trim();

    // Coleta distratores das outras estrofes + vocabulário-chave + banco de apoio
    const candidatos = [];
    can.estrofes.forEach(e => {
      if (e.palavra_oculta && norm(e.palavra_oculta) !== norm(correta)) {
        candidatos.push(e.palavra_oculta);
      }
    });
    (can.vocabulario_chave || []).forEach(v => {
      if (v && norm(v) !== norm(correta) && !candidatos.some(c => norm(c) === norm(v))) {
        candidatos.push(v);
      }
    });
    const fb = ['sempre','cuore','notte','sole','vita','tempo','amore','cielo','mare','vento','giorno','mondo'];
    fb.forEach(w => {
      if (norm(w) !== norm(correta) && !candidatos.some(c => norm(c) === norm(w))) {
        candidatos.push(w);
      }
    });

    // Embaralha candidatos e pega 3 distratores para totalizar 4 opções
    for (let i = candidatos.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [candidatos[i], candidatos[j]] = [candidatos[j], candidatos[i]];
    }
    const opcoes = [correta, ...candidatos.slice(0, 3)];
    for (let i = opcoes.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [opcoes[i], opcoes[j]] = [opcoes[j], opcoes[i]];
    }

    this._estrofeOpcoesIdx = this.estrofeAtual;
    this._opcoesAtuais = opcoes;
    return opcoes;
  },

  _esc(str) {
    return String(str||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  },

  // Transforma um trecho de texto em spans individuais por palavra para o destaque Karaokê
  _envolverPalavrasKaraoke(trecho) {
    if (!trecho) return '';
    return String(trecho).split(/(\s+)/).map(parte => {
      if (/^\s+$/.test(parte)) return parte;
      const limpo = this._esc(parte);
      return `<span class="can-word" data-raw="${limpo}">${limpo}</span>`;
    }).join('');
  },

  _renderizarPlayer() {
    if (this.modoPlayer === 'cloze') {
      this._renderizarClozePlayer();
      return;
    }
    const c = document.getElementById('canzoni-container');
    if (!c || !this.canzonAtual) return;
    const can = this.canzonAtual;

    const comLacuna = can.estrofes.filter(e => e.palavra_oculta);
    const total = comLacuna.length;
    const done  = comLacuna.filter(e => this.respostas[can.estrofes.indexOf(e)] !== null).length;
    const pct   = this.modoPlayer === 'karaoke'
      ? Math.round(((this.estrofeAtual + 1) / Math.max(1, can.estrofes.length)) * 100)
      : (total > 0 ? Math.round(done / total * 100) : 0);

    const versosHtml = can.estrofes.map((v, i) => {
      const resp = this.respostas[i];
      let cls;
      if (this.modoPlayer === 'karaoke') {
        cls = (i === this.estrofeAtual) ? 'active' : (i < this.estrofeAtual ? 'past-ok' : 'future');
      } else {
        if (i < this.estrofeAtual) {
          if (!v.palavra_oculta)       cls = 'past-ok';
          else if (resp && resp.correto) cls = 'past-correct';
          else if (resp)               cls = 'past-wrong';
          else                         cls = 'past-ok';
        } else if (i === this.estrofeAtual) {
          cls = 'active';
        } else {
          cls = 'future';
        }
      }

      let lineHtml;
      if (this.modoPlayer === 'karaoke' || !v.palavra_oculta || !v.texto_lacuna) {
        lineHtml = '<span class="can-verse-line">' + this._envolverPalavrasKaraoke(v.texto_completo || '') + '</span>';
      } else {
        let blankHtml;
        if (cls === 'future' || cls === 'active') {
          blankHtml = '<span class="can-blank can-word" data-raw="' + this._esc(v.palavra_oculta) + '">_____</span>';
        } else if (resp && resp.correto) {
          blankHtml = '<span class="can-blank can-blank-correct can-word" data-raw="' + this._esc(v.palavra_oculta) + '">' + this._esc(v.palavra_oculta) + '</span>';
        } else if (resp) {
          blankHtml = '<span class="can-blank can-blank-wrong">' + this._esc(resp.escolha) + '</span>'
                    + '<span class="can-blank can-blank-revealed can-word" data-raw="' + this._esc(v.palavra_oculta) + '"> ' + this._esc(v.palavra_oculta) + '</span>';
        } else {
          blankHtml = '<span class="can-blank can-word" data-raw="' + this._esc(v.palavra_oculta) + '">' + this._esc(v.palavra_oculta) + '</span>';
        }
        const pts = (v.texto_lacuna || '').split('___');
        lineHtml = '<span class="can-verse-line">'
                 + this._envolverPalavrasKaraoke(pts[0])
                 + blankHtml
                 + this._envolverPalavrasKaraoke(pts[1] || '')
                 + '</span>';
      }

      const badgeRep = (v.repeticoes && v.repeticoes > 1)
        ? `<span class="can-rep-badge" title="Refrão">${I18n.t('can_refrao_badge')} ×${v.repeticoes}</span>` : '';

      const tradHtml = (this.traduzirVisivel && v.traducao)
        ? '<div class="can-verse-trad">🇧🇷 ' + this._esc(v.traducao) + '</div>' : '';

      const dicaInline = (this.modoPlayer === 'praticar' && cls === 'active' && v.dica)
        ? `<div class="can-verse-hint">${I18n.t('can_dica_label')} ${this._esc(v.dica)}</div>` : '';

      const repeatHtml = `<button class="can-repeat-btn" onclick="event.stopPropagation();Canzoni.tocarEstrofeEspecifica(${i})">${I18n.t('can_ouvir_verso_n')} ${i + 1}</button>`;

      return `<div class="can-verse can-verse-${cls}" id="can-verse-${i}" onclick="Canzoni.tocarEstrofeEspecifica(${i})" style="cursor:pointer">`
           + `<div style="display:flex;justify-content:space-between;align-items:center;gap:0.5rem;margin-bottom:0.2rem">`
           + `<span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;color:#9B2335">${I18n.t('can_verso_n')} ${i + 1}/${can.estrofes.length}</span>`
           + badgeRep
           + `</div>`
           + lineHtml
           + tradHtml
           + dicaInline
           + `<div style="margin-top:0.35rem">${repeatHtml}</div>`
           + `</div>`;
    }).join('');

    let bottomBarHtml = '';
    const est = can.estrofes[this.estrofeAtual];
    if (this.modoPlayer === 'praticar' && est && est.palavra_oculta) {
      const opcoes = this._gerarOpcoes(est);
      const btns = opcoes.map(w => {
        const safeW = w.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
        return '<button class="can-choice-btn" onclick="Canzoni._escolher(\'' + safeW + '\')"><i>' + this._esc(w) + '</i></button>';
      }).join('');
      const hintBar = est.dica
        ? `<div class="can-choices-hint">💡 ${this._esc(est.dica)}</div>`
        : '';
      bottomBarHtml =
        '<div class="can-choices-bar">' +
          '<div class="can-choices-header">' +
            `<span class="can-choices-label">${I18n.t('can_instrucao_lacuna')}</span>` +
            hintBar +
          '</div>' +
          '<div class="can-choices-grid">' + btns + '</div>' +
        '</div>';
    } else if (this.modoPlayer === 'karaoke') {
      const vocabPills = (can.vocabulario_chave || []).map(v => {
        const safeV = v.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
        return `<button class="can-vocab-pill" onclick="App.pronunciar('${safeV}')">🔊 ${this._esc(v)}</button>`;
      }).join('');
      bottomBarHtml = `
        <div class="can-choices-bar" style="padding:0.75rem 1rem">
          <div style="font-size:0.72rem;color:#f5d0b0;margin-bottom:0.45rem;font-weight:600">
            ${I18n.t('can_vocab_chave_label')}
          </div>
          <div style="display:flex;gap:0.4rem;flex-wrap:wrap">${vocabPills}</div>
        </div>`;
    }

    const ytQuery = encodeURIComponent(`${can.titulo} ${can.artista || ''} lyrics testo`);
    const ytUrl = `https://www.youtube.com/results?search_query=${ytQuery}`;
    const speedLabel = this.velocidadeAudio === 0.7 ? '🐢 0.7x' : this.velocidadeAudio === 0.85 ? '🎧 0.85x' : '🐇 1.0x';

    c.innerHTML =
      '<div class="can-player">' +
        '<div class="can-player-header">' +
          '<button class="can-back-btn" onclick="Canzoni.renderizarSeletor()" title="Voltar">&#8249;</button>' +
          '<div class="can-header-song">' +
            '<div class="can-header-title">' + this._esc(can.icone || '🎵') + ' ' + this._esc(can.titulo) + '</div>' +
            '<div class="can-header-artist">' + this._esc(can.artista||'') + ' · ' + this._esc(can.nivel||'') + '</div>' +
          '</div>' +
          '<div class="can-score-row">' +
            '<span class="can-score-pill can-score-correct">' + this.acertos + ' ✓</span>' +
            '<span class="can-score-pill can-score-wrong">' + this.erros + ' ✗</span>' +
          '</div>' +
        '</div>' +
        /* Barra de Modos + Controles de Áudio Karaokê */
        '<div class="can-controls-bar">' +
          '<div class="can-mode-tabs">' +
            `<button class="can-mode-tab ${this.modoPlayer==='praticar'?'active':''}" onclick="Canzoni.mudarModo('praticar')">${I18n.t('can_modo_praticar')}</button>` +
            `<button class="can-mode-tab ${this.modoPlayer==='karaoke'?'active':''}" onclick="Canzoni.mudarModo('karaoke')">${I18n.t('can_modo_karaoke')}</button>` +
          '</div>' +
          '<div class="can-audio-tools">' +
            `<button id="can-btn-play-main" class="can-ctrl-btn primary ${this.tocandoKaraoke?'playing':''}" onclick="Canzoni.togglePlayPause()">` +
              (this.tocandoKaraoke ? I18n.t('can_btn_pausar_audio') : I18n.t('can_btn_ouvir_verso')) +
            '</button>' +
            `<button id="can-speed-btn" class="can-ctrl-btn" onclick="Canzoni.alternarVelocidade()" title="Velocidade">${speedLabel}</button>` +
            `<a href="${ytUrl}" target="_blank" rel="noopener noreferrer" class="can-ctrl-btn yt" title="YouTube">${I18n.t('can_btn_yt')}</a>` +
          '</div>' +
        '</div>' +
        '<div class="can-subbar">' +
          '<div class="can-progress-wrap"><div class="can-progress-fill" style="width:' + pct + '%"></div></div>' +
          '<div class="can-toggle-row">' +
            `<span class="can-toggle-label">${I18n.t('can_trad_pt')}</span>` +
            '<button class="can-toggle-btn ' + (this.traduzirVisivel?'on':'off') + '" onclick="Canzoni._toggleTraduzir()" aria-label="alternar tradução"></button>' +
          '</div>' +
        '</div>' +
        '<div class="can-lyrics-area" id="can-lyrics">' + versosHtml + '</div>' +
        bottomBarHtml +
      '</div>';

    setTimeout(() => {
      const el = document.querySelector('.can-verse-active');
      if (el) el.scrollIntoView({ behavior:'smooth', block:'center' });
    }, 100);
  },

  _escolher(palavra) {
    const can = this.canzonAtual;
    if (!can || this.estrofeAtual >= can.estrofes.length) return;
    const idxRespondido = this.estrofeAtual;
    const est = can.estrofes[idxRespondido];
    if (!est.palavra_oculta) return;

    const norm = s => s.toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const correto = norm(palavra) === norm(est.palavra_oculta);
    this.respostas[idxRespondido] = { escolha: palavra, correto };

    if (correto) {
      this.acertos++;
      if (typeof App !== 'undefined' && App.ganharXP) App.ganharXP(5);
    } else {
      this.erros++;
    }

    // Pronuncia a palavra correta imediatamente e depois avança para o próximo verso
    this.pararAudio();
    if (typeof App !== 'undefined' && App.pronunciar) {
      App.pronunciar(est.palavra_oculta);
    }

    this.estrofeAtual++;
    setTimeout(() => this._avancarProximoBlank(true), 950);
  },

  _toggleTraduzir() {
    this.traduzirVisivel = !this.traduzirVisivel;
    this._renderizarPlayer();
  },

  verificar() {},
  renderizarEstrofe() { this._renderizarPlayer(); },

  mostrarResultado() {
    this.pararAudio();
    const can = this.canzonAtual;
    const total = can.estrofes.filter(e => e.palavra_oculta).length;
    const pct = total > 0 ? Math.round(this.acertos / total * 100) : 100;
    if (typeof Progressao !== 'undefined' && Progressao.ganhar) Progressao.ganhar(can.xp_recompensa);
    const c = document.getElementById('canzoni-container');
    const emoji = pct >= 80 ? '🎤' : pct >= 50 ? '🎵' : '🎼';
    c.innerHTML =
      '<div class="can-player">' +
        '<div class="can-result">' +
          '<div class="can-result-emoji">' + emoji + '</div>' +
          '<div class="can-result-title">' + this._esc(can.titulo) + ' — ' + this._esc(can.artista || '') + '</div>' +
          '<div class="can-result-score">' + this.acertos + '<span>/' + total + '</span></div>' +
          '<div class="can-result-xp">+' + can.xp_recompensa + ' XP</div>' +
          '<div style="display:flex;gap:0.5rem;justify-content:center;margin-top:1.2rem;flex-wrap:wrap">' +
            `<button class="can-restart-btn" onclick="Canzoni.modoPlayer='karaoke';Canzoni.abrirCanzone('${can.id}');Canzoni.iniciarSequenciaKaraoke(0)">${I18n.t('can_res_karaoke')}</button>` +
            `<button class="can-restart-btn" onclick="Canzoni.modoPlayer='praticar';Canzoni.abrirCanzone('${can.id}')">${I18n.t('can_res_jogar_nov')}</button>` +
            `<button class="can-restart-btn secundario" onclick="Canzoni.renderizarSeletor()">${I18n.t('can_res_catalogo')}</button>` +
          '</div>' +
        '</div>' +
      '</div>';
  },

  // ─────────────────────────────────────────────────────────────
  // 🎧 LYRICS CLOZE PLAYER (Treino Auditivo Musical Sincronizado)
  // ─────────────────────────────────────────────────────────────

  // ── 1. STUDIO DE IMPORTAÇÃO (Upload de Áudio + Letra .lrc / Texto) ──
  // ── Prompt de auxílio para extração de áudio via Gemini / LLM ──
  _obterPromptGemini() {
    return `# Ruolo: Transcrittore Audio con Timestamp Parola per Parola

## Obiettivo
Analizzare file audio (parlato, dialoghi, canzoni) e generare una trascrizione temporizzata con precisione parola per parola, restituendo il risultato esclusivamente in formato JSON.

## Specifiche del Formato JSON
Ogni elemento della lista deve essere un oggetto contenente:
- "w" (string): La singola parola pronunciata, inclusa l'eventuale punteggiatura associata (es. virgole, punti, punti interrogativi).
- "t" (number): Il secondo esatto in cui inizia l'emissione vocale della parola, espresso con 2 cifre decimali (es. 2.15).
- "blank" (boolean, opzionale): Impostato su true esclusivamente sull'ultima parola di un verso, frase o prima di una pausa/stacco musicale rilevante, per indicare l'interruzione della riga.

## Schema di Esempio
[
  { "w": "Parola1,", "t": 0.05 },
  { "w": "parola2", "t": 1.10 },
  { "w": "parola3.", "t": 2.15, "blank": true }
]

## Regole di Trascrizione
1. Precisione temporale: Allinea l'attacco di ciascun termine ("t") all'istante sonoro reale.
2. Segmentazione: Separa chiaramente le parole e mantieni la punteggiatura logica attaccata al termine di appartenenza.
3. Formato di output: Rispondi fornendo unicamente il blocco JSON valido, senza introduzioni o commenti aggiuntivi.`;
  },

  copiarPromptGemini() {
    const txt = this._obterPromptGemini();
    navigator.clipboard.writeText(txt).then(() => {
      const btn = document.getElementById('cloze-copy-prompt-btn');
      if (btn) {
        const orig = btn.innerHTML;
        btn.innerHTML = '✅ Copiado!';
        btn.style.background = '#27ae60';
        btn.style.color = '#fff';
        setTimeout(() => {
          btn.innerHTML = orig;
          btn.style.background = '';
          btn.style.color = '';
        }, 2200);
      }
      App.notificar('Prompt copiado para a área de transferência!', 'sucesso');
    }).catch(() => {
      const ta = document.createElement('textarea');
      ta.value = txt;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      App.notificar('Prompt copiado!', 'sucesso');
    });
  },

  // ── 1. STUDIO DE IMPORTAÇÃO (Upload de Áudio + Letra JSON Gemini / Whisper) ──
  abrirClozeStudio(idEditar = null) {
    this.pararAudio();
    const c = document.getElementById('canzoni-container');
    if (!c) return;

    const can = idEditar ? this.todasCanzoni().find(x => x.id === idEditar) : null;
    const titulo = can ? can.titulo : '';
    const artista = can ? can.artista : '';

    const jsonExemplo = `[
  { "w": "Una", "t": 2.00 },
  { "w": "mattina", "t": 2.50 },
  { "w": "mi", "t": 3.20 },
  { "w": "sono", "t": 3.50 },
  { "w": "alzato,", "t": 3.90, "blank": true },
  { "w": "o", "t": 4.90 },
  { "w": "bella", "t": 5.20 },
  { "w": "ciao,", "t": 5.70, "blank": true }
]`;

    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Canzoni.renderizarSeletor()">‹ Voltar</button>
        <span style="font-size:0.95rem;font-weight:700">🎧 Cloze Studio — Sincronização por Palavra com IA</span>
      </div>

      <div class="cloze-studio-box">
        <div style="font-size:0.88rem;color:#6b1a2a;line-height:1.55;margin-bottom:1.2rem">
          Importe seu arquivo de música (MP3/WAV) e sincronize com precisão <strong>palavra por palavra</strong> através do Google Gemini.
          O sistema criará o <strong>Lyrics Cloze Player</strong> com pausas com <strong>desvio zero (0ms)</strong> e iluminação Karaokê em tempo real.
        </div>

        <!-- 1. Dropzone de Arquivo de Áudio -->
        <div class="cloze-upload-dropzone" id="cloze-dropzone" onclick="document.getElementById('cloze-audio-file').click()">
          <input type="file" id="cloze-audio-file" accept=".mp3,.wav,.ogg,audio/*" style="display:none" onchange="Canzoni._onStudioFileSelect(this)">
          <div style="font-size:2rem;margin-bottom:0.35rem">📁</div>
          <div style="font-weight:700;font-size:0.95rem;color:#3d0d18" id="cloze-file-name">${I18n.t('can_cloze_upload_audio')}</div>
          <div style="font-size:0.78rem;color:#777;margin-top:0.25rem">${I18n.t('can_cloze_upload_desc')}</div>
          <audio id="cloze-audio-preview" controls style="display:none;margin:0.8rem auto 0;max-width:320px;width:100%"></audio>
        </div>

        <!-- 2. Metadados -->
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

        <!-- 3. Prompt de Auxílio para IA (Google Gemini) -->
        <div class="cloze-ai-prompt-box">
          <div class="cloze-ai-prompt-header">
            <div style="font-weight:700;font-size:0.92rem;color:#9B2335;display:flex;align-items:center;gap:0.4rem">
              <span>🤖 Prompt para o Google Gemini</span>
              <span style="font-size:0.68rem;background:rgba(212,168,67,0.22);color:#9B2335;padding:0.12rem 0.45rem;border-radius:4px;border:1px solid rgba(212,168,67,0.45);font-weight:700">Recomendado</span>
            </div>
            <div style="display:flex;gap:0.4rem;align-items:center">
              <a href="https://gemini.google.com" target="_blank" rel="noopener noreferrer" class="cloze-gemini-link" title="Abrir Google Gemini em nova aba">Abrir Gemini ↗</a>
              <button class="ia-copy-btn" id="cloze-copy-prompt-btn" onclick="Canzoni.copiarPromptGemini()">📋 Copiar Prompt</button>
            </div>
          </div>
          <div style="font-size:0.8rem;color:#666;margin:0.5rem 0 0.65rem;line-height:1.45">
            <strong>Como usar com o Gemini:</strong><br>
            1. Clique em <strong>📋 Copiar Prompt</strong> acima e abra o <strong>Google Gemini</strong>.<br>
            2. Anexe o seu arquivo MP3 na conversa e envie junto com o prompt copiado.<br>
            3. Copie o bloco JSON retornado pelo Gemini e cole no campo de transcrição abaixo.
          </div>
          <pre id="cloze-gemini-prompt-text" class="cloze-prompt-pre">${this._obterPromptGemini()}</pre>
        </div>

        <!-- 4. Letra / JSON com Timestamps por Palavra -->
        <div style="margin-bottom:1rem">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.35rem">
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Transcrição JSON com Timestamps por Palavra *</label>
            <span style="font-size:0.74rem;color:#777">Formato: array de palavras <code>{ w, t, blank }</code></span>
          </div>
          <textarea id="cloze-letra" rows="8" placeholder='${jsonExemplo}'
            style="width:100%;padding:0.65rem;border:2px solid #ddd;border-radius:8px;font-family:monospace;font-size:0.85rem;line-height:1.5"></textarea>
          <div style="font-size:0.76rem;color:#777;margin-top:0.3rem">
            Cole diretamente o JSON gerado pelo Gemini. As palavras com <code>"blank": true</code> delimitarão o final do verso e as lacunas interativas.
          </div>
        </div>

        <!-- 5. Densidade de lacunas -->
        <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:1.4rem;flex-wrap:wrap">
          <span style="font-size:0.82rem;font-weight:700;color:#9B2335">${I18n.t('can_cloze_densidade')}:</span>
          <label style="font-size:0.82rem;cursor:pointer"><input type="radio" name="cloze-dens" value="padrao" checked> 1 por verso (Padrão)</label>
          <label style="font-size:0.82rem;cursor:pointer"><input type="radio" name="cloze-dens" value="leve"> Leve (1 a cada 2 versos)</label>
          <label style="font-size:0.82rem;cursor:pointer"><input type="radio" name="cloze-dens" value="todas"> Intensa (Todas as chaves)</label>
        </div>

        <!-- 6. Ações -->
        <div style="display:flex;gap:0.6rem;flex-wrap:wrap">
          <button class="btn-primario" style="flex:1" onclick="Canzoni._iniciarClozeDoStudio()">
            🚀 Iniciar Lyrics Cloze
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
      App.notificar('Por favor, informe a transcrição JSON gerada pelo Gemini.', 'erro');
      return;
    }

    const songId = `cloze_${Date.now()}`;
    const file = this._tempStudioFile;

    // Se tiver arquivo, salva no IndexedDB
    if (file) {
      await CanzoniAudioDB.salvar(songId, file);
    }

    const jsonParsed = this._tryParseJSON(letra);

    // Monta objeto da música
    const customSong = {
      id: songId,
      titulo,
      artista,
      nivel: 'B1',
      icone: '🎧',
      letra_raw: letra,
      versos_sincronizados: jsonParsed || null,
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
      textoLetra = can.estrofes.map(e => e.texto_completo || e.texto_lacuna || '').join('\n');
    }

    // 3. Configura áudio se houver blob
    if (audioBlob) {
      this._configurarAudioElement(audioBlob);
    } else {
      this._clozeAudioSource = 'tts';
    }

    // 4. Parser de timestamps e geração de lacunas Cloze
    let clozeItems, wordBankWords;
    if (can.versos_sincronizados || can.word_timings || this._isJSONWordTimings(textoLetra)) {
      const jsonDados = can.versos_sincronizados || can.word_timings || this._tryParseJSON(textoLetra);
      const res = this._processarJSONWordTimings(jsonDados, can, densidade);
      clozeItems = res.clozeItems;
      wordBankWords = res.wordBankWords;
    } else {
      const duracaoEstimada = (this._audioReal && this._audioReal.duration) ? this._audioReal.duration : 0;
      const parsed = this._parseLRCOrText(textoLetra, duracaoEstimada);
      const res = this._processarVersosParaCloze(parsed, densidade);
      clozeItems = res.clozeItems;
      wordBankWords = res.wordBankWords;
    }

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
    const linhas = texto.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    const lrcRegex = /^\[(\d{1,2}):(\d{2})(?:[.:](\d{1,3}))?\](.*)$/;
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
      const mCurlys = rawText.match(/\{\{([^}]+)\}\}/);
      if (mCurlys) {
        customWord = mCurlys[1].trim();
      } else if (v.palavra_oculta) {
        customWord = v.palavra_oculta.trim();
      }

      const cleanLine = rawText.replace(/\{\{([^}]+)\}\}/g, '$1');
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

  // Detecta se a entrada é estrutura JSON de timings por palavra
  _isJSONWordTimings(strOuObj) {
    if (!strOuObj) return false;
    if (typeof strOuObj === 'object') {
      if (Array.isArray(strOuObj)) {
        return strOuObj.length > 0 && (strOuObj[0].palavras || strOuObj[0].words || strOuObj[0].w !== undefined || strOuObj[0].start !== undefined);
      }
      return !!(strOuObj.versos || strOuObj.segments || strOuObj.words || strOuObj.versos_sincronizados);
    }
    if (typeof strOuObj === 'string') {
      const parsed = this._tryParseJSON(strOuObj);
      if (parsed) return this._isJSONWordTimings(parsed);
    }
    return false;
  },

  _tryParseJSON(strOuObj) {
    if (!strOuObj) return null;
    if (typeof strOuObj === 'object') return strOuObj;
    try {
      let str = String(strOuObj).trim();
      str = str.replace(/^```(?:json)?\s*/i, '').replace(/\s*```$/, '').trim();
      const match = str.match(/(\[[\s\S]*\]|\{[\s\S]*\})/);
      if (match) return JSON.parse(match[1]);
      return JSON.parse(str);
    } catch (_) {
      return null;
    }
  },

  // Processa dados JSON estruturados com sincronização precisa a nível de palavra (Opção B)
  _processarJSONWordTimings(jsonDados, can, densidade = 'padrao') {
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

    let rawVerses = [];
    if (Array.isArray(jsonDados) && jsonDados.length > 0 && (jsonDados[0].w !== undefined || jsonDados[0].word !== undefined || jsonDados[0].text !== undefined)) {
      // Formato Gemini / Whisper: array plano de palavras com "blank: true" delimitando o final de cada verso
      const groupedVerses = [];
      let currentVerse = [];
      for (const w of jsonDados) {
        currentVerse.push(w);
        if (w.blank === true) {
          groupedVerses.push({ palavras: currentVerse });
          currentVerse = [];
        }
      }
      if (currentVerse.length > 0) {
        groupedVerses.push({ palavras: currentVerse });
      }
      rawVerses = groupedVerses;
    } else if (Array.isArray(jsonDados)) {
      rawVerses = jsonDados;
    } else if (jsonDados.versos_sincronizados) {
      rawVerses = jsonDados.versos_sincronizados;
    } else if (jsonDados.versos) {
      rawVerses = jsonDados.versos;
    } else if (jsonDados.segments) {
      rawVerses = jsonDados.segments;
    } else if (jsonDados.words) {
      rawVerses = [{ palavras: jsonDados.words }];
    }

    const clozeItems = [];
    const wordBankWords = [];
    let blankCounter = 0;

    for (let i = 0; i < rawVerses.length; i++) {
      const v = rawVerses[i];
      const rawWords = v.palavras || v.words || v.tokens || [];
      const traducao = v.traducao || (can.estrofes && can.estrofes[i]?.traducao) || '';

      const parsedWords = [];
      let verseStartTime = Infinity;
      let verseEndTime = 0;

      for (let wIdx = 0; wIdx < rawWords.length; wIdx++) {
        const item = rawWords[wIdx];
        const rawText = item.w || item.word || item.text || '';
        const time = (item.t !== undefined ? item.t : (item.start !== undefined ? item.start : item.time)) || 0;
        const endTime = (item.end !== undefined ? item.end : (item.endTime !== undefined ? item.endTime : time + 0.5));
        const isExplicitBlank = !!item.blank;

        if (time < verseStartTime) verseStartTime = time;
        if (endTime > verseEndTime) verseEndTime = endTime;

        const m = String(rawText).match(/^([^A-Za-zÀ-ÖØ-öø-ÿ0-9]*)([A-Za-zÀ-ÖØ-öø-ÿ0-9'-]+)([^A-Za-zÀ-ÖØ-öø-ÿ0-9]*)$/);
        let prefixPunct = '';
        let cleanWord = rawText;
        let suffixPunct = '';

        if (m) {
          prefixPunct = m[1];
          cleanWord = m[2];
          suffixPunct = m[3];
        }

        parsedWords.push({
          rawText,
          cleanWord,
          prefixPunct,
          suffixPunct,
          time,
          endTime,
          isExplicitBlank
        });
      }

      if (verseStartTime === Infinity) verseStartTime = i * 4.0;
      if (verseEndTime <= verseStartTime) verseEndTime = verseStartTime + 3.5;

      // Seleção da palavra oculta
      let blankWordIndex = parsedWords.findIndex(pw => pw.isExplicitBlank);
      if (blankWordIndex === -1) {
        const estrofePalavra = can.estrofes && can.estrofes[i]?.palavra_oculta;
        if (estrofePalavra) {
          const normE = estrofePalavra.toLowerCase().trim();
          blankWordIndex = parsedWords.findIndex(pw => pw.cleanWord.toLowerCase().trim() === normE);
        }
      }

      if (blankWordIndex === -1 && parsedWords.length > 0) {
        if (densidade !== 'leve' || i % 2 === 0) {
          const candidatos = parsedWords
            .map((pw, idx) => ({ ...pw, idx }))
            .filter(pw => pw.cleanWord.length >= 4 && !stopwords.has(pw.cleanWord.toLowerCase()));
          if (candidatos.length > 0) {
            candidatos.sort((a, b) => b.cleanWord.length - a.cleanWord.length);
            blankWordIndex = candidatos[0].idx;
          } else {
            blankWordIndex = parsedWords.length - 1;
          }
        }
      }

      const tokens = [];
      let blankObj = null;

      for (let wIdx = 0; wIdx < parsedWords.length; wIdx++) {
        const pw = parsedWords[wIdx];
        if (wIdx === blankWordIndex) {
          const bId = `blank_${blankCounter++}`;
          blankObj = {
            blankId: bId,
            verseIdx: i,
            word: pw.cleanWord,
            pauseTime: pw.time, // Pausa exata no início da palavra a ser cantada
            status: 'blurred',
            attempts: 0,
            firstTry: true
          };
          tokens.push({
            text: pw.cleanWord,
            prefixPunct: pw.prefixPunct,
            suffixPunct: pw.suffixPunct,
            isBlank: true,
            blankId: bId,
            time: pw.time
          });
          wordBankWords.push(pw.cleanWord);
        } else {
          tokens.push({
            text: pw.cleanWord,
            rawText: pw.rawText,
            prefixPunct: pw.prefixPunct,
            suffixPunct: pw.suffixPunct,
            isBlank: false,
            time: pw.time
          });
        }
      }

      const rawTextJoined = parsedWords.map(p => p.rawText).join(' ');

      clozeItems.push({
        idx: i,
        startTime: verseStartTime,
        endTime: verseEndTime,
        rawText: rawTextJoined,
        traducao,
        hasWordTimings: true,
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
      if (v.hasWordTimings) {
        v.tokens.forEach((t, tIdx) => {
          const prefix = t.prefixPunct ? this._esc(t.prefixPunct) : '';
          const suffix = t.suffixPunct ? this._esc(t.suffixPunct) : '';
          if (t.isBlank) {
            const isTarget = v.blank && v.blank.status === 'blurred' && (!this._clozeItems.slice(0, i).some(x => x.blank && x.blank.status === 'blurred'));
            const cls = v.blank.status === 'correct' ? 'is-correct' : (v.blank.status === 'wrong' ? 'is-wrong' : 'is-blurred');
            const targetCls = isTarget ? ' is-target' : '';
            const timingAttr = t.time !== undefined ? ` data-time="${t.time}"` : '';
            lineHtml += `${prefix}<span class="cloze-blank ${cls}${targetCls}" id="${t.blankId}" data-word="${this._esc(t.text)}"${timingAttr}>${this._esc(t.text)}</span>${suffix} `;
          } else {
            const timingAttr = t.time !== undefined ? ` data-time="${t.time}" id="cloze-token-${i}-${tIdx}"` : '';
            lineHtml += `${prefix}<span class="cloze-word-token"${timingAttr}>${this._esc(t.text)}</span>${suffix} `;
          }
        });
      } else {
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
      }

      const timingBadge = v.hasWordTimings ? `<span class="cloze-badge-timing">⚡ Word-Sync</span>` : '';
      const tradHtml = v.traducao ? `<div class="cloze-traducao">${this._esc(v.traducao)}</div>` : '';

      versesHtml += `
        <div class="cloze-verse is-future" id="cloze-verse-${i}" onclick="Canzoni._pularParaVersoCloze(${i})">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.15rem">
            <span style="font-size:0.68rem;color:#9B2335;font-weight:700;letter-spacing:0.04em">
              VERSO ${i + 1}/${this._clozeItems.length}
            </span>
            ${timingBadge}
          </div>
          <div class="cloze-line">${lineHtml}</div>
          ${tradHtml}
        </div>
      `;
    });

    // Pílulas do Word Bank
    const pillsHtml = this._clozeWordBank.map(wb => {
      const usedCls = wb.used ? ' is-used' : '';
      const safeWord = this._esc(wb.word).replace(/'/g, "\\'");
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

    if (activeIdx !== -1) {
      this._atualizarDestaquePalavras(curTime, activeIdx);
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
        vEl.querySelectorAll('.cloze-word-token').forEach(tok => tok.classList.add('is-sung'));
      } else {
        vEl.classList.remove('is-active', 'is-past');
        vEl.classList.add('is-future');
        vEl.querySelectorAll('.cloze-word-token').forEach(tok => tok.classList.remove('is-sung'));
      }
    });

    // Rolagem suave centralizada
    const activeEl = document.getElementById(`cloze-verse-${activeIdx}`);
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  },

  // Efeito Karaokê em tempo real palavra por palavra (Word-Level Sync)
  _atualizarDestaquePalavras(curTime, activeIdx) {
    if (activeIdx < 0 || !this._clozeItems || !this._clozeItems[activeIdx]) return;
    const item = this._clozeItems[activeIdx];
    if (!item.hasWordTimings) return;

    const vEl = document.getElementById(`cloze-verse-${activeIdx}`);
    if (!vEl) return;

    const tokens = vEl.querySelectorAll('.cloze-word-token[data-time]');
    tokens.forEach(tok => {
      const t = parseFloat(tok.getAttribute('data-time'));
      if (!isNaN(t)) {
        if (curTime >= t) {
          tok.classList.add('is-sung');
        } else {
          tok.classList.remove('is-sung');
        }
      }
    });
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
    const norm = s => String(s || '').toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
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

    if (activeIdx !== -1) {
      this._atualizarDestaquePalavras(curTime, activeIdx);
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
};

document.addEventListener('i18n:changed', () => {
  if (document.getElementById('canzoni-container')) Canzoni.renderizarSeletor();
});
