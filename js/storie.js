// ============================================================
// storie.js — Módulo de leitura interativa de histórias italianas
// - 10 histórias A1-C2 (data/storie.json)
// - Texto corrido, toda palavra clicável
// - Modal flutuante com IPA/tradução/categoria + salvar no deck
// - TTS via App.pronunciar
// - Marcar como lida + XP recompensa
// ============================================================

const Storie = {
  dados: null,
  storAttuale: null,
  traduzirVisivel: true,
  completate: [],
  _filtroNivel: '',
  _filtroTexto: '',
  _filtroOrigem: '',
  _escListener: null,

  // ── Carregar dados ─────────────────────────────────────────
  async carregar() {
    if (!this.dados) {
      try {
        const r = await fetch('data/storie.json');
        if (r.ok) {
          const raw = await r.json();
          raw.storie = (raw.storie || []).map(s => this._normalizar(s));
          this.dados = raw;
        } else this.dados = { storie: [] };
      } catch { this.dados = { storie: [] }; }
    }
    // Mescla histórias customizadas — custom primeiro
    try {
      const custom = JSON.parse(localStorage.getItem('it_storie_custom') || '[]');
      if (custom.length) {
        const normalizadas = custom.map(s => this._normalizar(s));
        this.dados.storie = [...normalizadas, ...this.dados.storie];
      }
    } catch (e) {}
    try {
      this.completate = JSON.parse(localStorage.getItem('it_storie_lidas') || '[]');
    } catch { this.completate = []; }
  },

  // Normaliza histórias com schema alternativo (titolo/livello/testo-string)
  _normalizar(s) {
    const out = Object.assign({}, s);
    if (!out.titulo && out.titolo) out.titulo = out.titolo;
    if (!out.titulo_pt) out.titulo_pt = out.titulo || out.titolo || '';
    if (!out.nivel && out.livello) out.nivel = out.livello;
    if (!out.descricao) out.descricao = out.tema || '';
    if (!out.descricao_pt) out.descricao_pt = out.descricao;
    if (!out.icone) out.icone = '📜';
    if (!out.xp_recompensa) out.xp_recompensa = 60;
    // testo como string simples → array de parágrafos
    if (typeof out.testo === 'string') {
      const frases = out.testo.split(/(?<=[.!?])\s+/).filter(Boolean);
      const chunks = [];
      for (let i = 0; i < frases.length; i += 3) {
        chunks.push({
          id: `p${i}`,
          italiano: frases.slice(i, i + 3).join(' '),
          portugues: '',
          parole: [],
        });
      }
      if (!chunks.length) chunks.push({ id: 'p0', italiano: out.testo, portugues: '', parole: [] });
      out.testo = chunks;
    }
    return out;
  },

  _salvarCompletate() {
    localStorage.setItem('it_storie_lidas', JSON.stringify(this.completate));
  },

  // ── Renderizar seletor de histórias ────────────────────────
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('storie-container');
    if (!c) return;

    const todas = this.dados?.storie || [];
    const niveis = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
    const counts = {};
    todas.forEach(s => { counts[s.nivel] = (counts[s.nivel] || 0) + 1; });

    let filtrate = todas;
    if (this._filtroOrigem === 'custom') filtrate = filtrate.filter(s => s._custom || s.custom);
    if (this._filtroOrigem === 'nativo') filtrate = filtrate.filter(s => !s._custom && !s.custom);
    if (this._filtroNivel) filtrate = filtrate.filter(s => s.nivel === this._filtroNivel);
    if (this._filtroTexto) {
      const q = this._filtroTexto.toLowerCase();
      filtrate = filtrate.filter(s =>
        s.titulo.toLowerCase().includes(q) ||
        (s.titulo_pt || '').toLowerCase().includes(q) ||
        (s.autor || '').toLowerCase().includes(q)
      );
    }

    const labels = I18n.idioma === 'it'
      ? { tut: 'Tutte', cerca: '🔍 Titolo o autore...', nenhuma: 'Nessuna storia ancora.', risultato: 'Nessun risultato.' }
      : { tut: 'Todas', cerca: '🔍 Título ou autor...', nenhuma: 'Nenhuma história ainda.', risultato: 'Nenhum resultado.' };

    // Cores para cada nível CEFR
    const corNivel = { A1:'#27AE60', A2:'#1ABC9C', B1:'#2980B9', B2:'#8E44AD', C1:'#E67E22', C2:'#C0392B' };

    let html = `
      <!-- Barra de filtros -->
      <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;margin-bottom:0.8rem;justify-content:center">
        <input type="search" placeholder="${labels.cerca}" value="${this._filtroTexto}"
          oninput="Storie._filtroTexto=this.value;Storie.renderizarSeletor()"
          style="flex:1;min-width:140px;padding:0.45rem 0.8rem;border:1.5px solid var(--cor-pietra);border-radius:8px;font-size:0.88rem;background:var(--cor-marmore);color:var(--cor-inchiostro)">
        <button class="btn-ia-add" onclick="IAImport.abrir('storia')">🤖 via IA</button>
      </div>
      <!-- Pills de origem + select de nível -->
      <div style="display:flex;gap:0.3rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
        ${(()=>{const nC=todas.filter(s=>s._custom||s.custom).length;const nN=todas.length-nC;const _o=this._filtroOrigem;
          const oP=(v,l,ct)=>`<button onclick="Storie._filtroOrigem='${v}';Storie.renderizarSeletor()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid ${_o===v?'#7B68A0':'#ccc'};background:${_o===v?'#7B68A0':'transparent'};color:${_o===v?'#fff':'var(--cor-inchiostro)'};cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap">${l} (${ct})</button>`;
          return oP('','Todas',todas.length)+(nC?oP('custom','🤖 Adicionadas',nC):'')+oP('nativo','📚 Nativas',nN);
        })()}
        <select class="nivel-select${this._filtroNivel?' ativo':''}"
          onchange="Storie._filtroNivel=this.value;Storie.renderizarSeletor()">
          <option value="">🎯 Nível</option>
          ${niveis.filter(n=>counts[n]).map(n=>`<option value="${n}" ${this._filtroNivel===n?'selected':''}>${n} (${counts[n]})</option>`).join('')}
        </select>
      </div>
      <!-- Grid de histórias -->
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem">`;

    for (const s of filtrate) {
      const isLida = this.completate.includes(s.id);
      const corN = corNivel[s.nivel] || '#9B2335';
      html += `
        <div onclick="Storie.abrirStoria('${s.id}')"
          style="background:var(--cor-marmore);border-radius:14px;padding:1.2rem 1rem;text-align:center;
                 box-shadow:0 3px 12px rgba(0,0,0,0.09);cursor:pointer;border:2px solid transparent;
                 transition:transform 0.18s,box-shadow 0.18s,border-color 0.18s;
                 display:flex;flex-direction:column;align-items:center;gap:0.35rem"
          onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 22px rgba(0,0,0,0.14)';this.style.borderColor='${corN}'"
          onmouseout="this.style.transform='';this.style.boxShadow='0 3px 12px rgba(0,0,0,0.09)';this.style.borderColor='transparent'">
          <div style="font-size:2.4rem;line-height:1.1">${s.icone||'📜'}</div>
          <div style="font-family:'Cinzel',serif;font-size:0.88rem;font-weight:700;color:var(--cor-veneziano-escuro);line-height:1.3">
            ${s.titulo}${isLida?'<span style="font-size:0.6rem;background:#2A9D8F;color:#fff;padding:0.08rem 0.35rem;border-radius:4px;margin-left:0.3rem;vertical-align:middle">✓</span>':''}${s._custom?'<span class="ia-custom-badge">IA</span>':''}
          </div>
          ${s._custom?`<button class="ia-del-btn" onclick="event.stopPropagation();IAImport.excluir('storia','${s.id}')">🗑️ Remover</button>`:''}
          <div style="font-size:0.72rem;color:var(--cor-pietra);font-style:italic">${s.autor||''}</div>
          <div style="display:flex;gap:0.4rem;align-items:center;margin-top:0.2rem">
            <span style="font-size:0.7rem;font-weight:800;padding:0.1rem 0.5rem;border-radius:6px;background:${corN};color:#fff">${s.nivel}</span>
            <span style="font-size:0.72rem;color:${corN};font-weight:700">+${s.xp_recompensa||50} XP</span>
          </div>
        </div>`;
    }

    if (filtrate.length === 0) {
      html += `<p style="text-align:center;color:#aaa;font-style:italic;grid-column:1/-1;padding:2rem 0">${this._filtroTexto?labels.risultato:labels.nenhuma}</p>`;
    }

    html += '</div>';
    c.innerHTML = html;
  },

  // ── Abrir uma história para leitura ────────────────────────
  async abrirStoria(id) {
    await this.carregar();
    const s = (this.dados?.storie || []).find(x => x.id === id);
    if (!s) return;
    this.storAttuale = s;
    this.traduzirVisivel = true;
    this._renderizarStoria();
  },

  // ── Renderizar a história em modo leitura corrida ──────────
  _renderizarStoria() {
    const c = document.getElementById('storie-container');
    if (!c || !this.storAttuale) return;
    const s = this.storAttuale;
    const il = I18n.idioma === 'it';

    const tituloExibido = il ? s.titulo : (s.titulo_pt || s.titulo);
    const descExibida   = il ? s.descricao : (s.descricao_pt || s.descricao);

    // Constrói parágrafos com texto corrido — toda palavra clicável
    let parasHtml = '';
    s.testo.forEach((p, idx) => {
      const textoMarcado = this._marcarPalavras(p.italiano, p.parole || [], idx);
      const ptText = (p.portugues || '').replace(/</g, '&lt;');
      parasHtml += `
        <div class="storie-bloco">
          <p class="storie-p">${textoMarcado}
            <button class="storie-audio-btn"
              onclick="event.stopPropagation();App.pronunciar('${(p.italiano||'').replace(/\\/g,'\\\\').replace(/'/g,"\\'")}')"
              title="${il?'Ascolta':'Ouvir'}">🔊</button>
          </p>
          ${this.traduzirVisivel && ptText ? `<p class="storie-trad-p">${ptText}</p>` : ''}
        </div>`;
    });

    const html = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Storie._fecharModal();Storie.renderizarSeletor()">‹ Storie</button>
        <span style="font-size:0.85rem;font-weight:700">${s.nivel} · +${s.xp_recompensa||50} XP</span>
      </div>

      <div class="gram-card" style="margin-top:1rem;padding:1.2rem;text-align:center">
        <div style="font-size:2.6rem;margin-bottom:0.4rem">${s.icone||'📖'}</div>
        <h2 style="margin:0 0 0.3rem;font-family:'Playfair Display',serif;font-size:1.45rem;color:#9B2335">${tituloExibido}</h2>
        <div style="font-size:0.82rem;color:#666;font-style:italic">${s.autor||''} · ${s.tema||''}</div>
        <p style="font-size:0.85rem;color:#444;margin:0.7rem 0 0;line-height:1.4">${descExibida}</p>
        <div style="display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap;margin-top:1rem">
          <button class="btn-secondario" onclick="Storie._toggleTraduzir()">
            ${this.traduzirVisivel
              ? (il ? '👁️ Nascondi traduzione' : '👁️ Ocultar tradução')
              : (il ? '👁️ Mostra traduzione'   : '👁️ Mostrar tradução')}
          </button>
          <button class="btn-primario" onclick="Storie._ouvirTudo()">
            ${il ? '🔊 Ascolta tutto' : '🔊 Ouvir tudo'}
          </button>
        </div>
      </div>

      <div class="storie-texto-corrido">${parasHtml}</div>

      <div style="display:flex;gap:0.5rem;justify-content:space-between;margin-top:1.5rem;padding-top:1rem;border-top:1px solid var(--cor-pietra)">
        <button class="btn-secondario" onclick="Storie._fecharModal();Storie.renderizarSeletor()">
          ${il ? '‹ Tutte le storie' : '‹ Todas as histórias'}
        </button>
        <button class="btn-primario" onclick="Storie._marcarLida()">
          ${this.completate.includes(s.id)
            ? (il ? '✓ Riletta' : '✓ Relida')
            : (il ? `✓ Ho finito (+${s.xp_recompensa||50} XP)` : `✓ Concluir (+${s.xp_recompensa||50} XP)`)}
        </button>
      </div>

      <!-- Modal flutuante de palavra -->
      <div id="storie-word-modal" class="storie-word-modal" style="display:none"></div>
      <div id="storie-modal-overlay" onclick="Storie._fecharModal()" style="display:none"></div>`;

    c.innerHTML = html;

    // Delegação de cliques para palavras
    const textoEl = c.querySelector('.storie-texto-corrido');
    if (textoEl) {
      textoEl.addEventListener('click', (e) => {
        const wordEl = e.target.closest('.storie-palavra');
        if (wordEl) {
          e.stopPropagation();
          this._abrirModalPalavra(wordEl);
        } else {
          this._fecharModal();
        }
      });
    }

    // Fechar com ESC
    if (this._escListener) document.removeEventListener('keydown', this._escListener);
    this._escListener = (e) => { if (e.key === 'Escape') this._fecharModal(); };
    document.addEventListener('keydown', this._escListener);
  },

  // ── Tokenizar e marcar TODAS as palavras como clicáveis ────
  _marcarPalavras(texto, parole, parIdx) {
    if (!texto) return '';
    // Tokeniza: palavras (incluindo acentuadas e apóstrofo) | pontuação | espaços
    const tokens = texto.match(/[A-Za-zÀ-öø-ÿ']+|[^A-Za-zÀ-öø-ÿ'\s]+|\s+/g) || [];

    return tokens.map((tok, wIdx) => {
      // Espaços: retorna como está
      if (/^\s+$/.test(tok)) return tok;
      // Pontuação pura: escapa e retorna
      if (/^[^A-Za-zÀ-öø-ÿ']+$/.test(tok)) return this._escape(tok);

      // É uma palavra — buscar dados de vocab
      const vocabDado = parole.find(p =>
        this._normWord(p.parola) === this._normWord(tok)
      );
      const jaSalva = this._verificarSalva(tok);

      const classes = ['storie-palavra'];
      if (jaSalva)   classes.push('storie-palavra-salva');
      if (vocabDado) classes.push('storie-palavra-vocab');

      const attrs = [
        `data-palavra="${this._escAttr(tok)}"`,
        `data-par="${parIdx}"`,
        `data-widx="${wIdx}"`,
      ];
      if (vocabDado) {
        if (vocabDado.ipa)        attrs.push(`data-ipa="${this._escAttr(vocabDado.ipa)}"`);
        if (vocabDado.traduzione) attrs.push(`data-trad="${this._escAttr(vocabDado.traduzione)}"`);
        if (vocabDado.categoria)  attrs.push(`data-cat="${this._escAttr(vocabDado.categoria)}"`);
      }

      return `<span class="${classes.join(' ')}" ${attrs.join(' ')}>${this._escape(tok)}</span>`;
    }).join('');
  },

  _normWord(w) {
    return (w || '').toLowerCase().replace(/[''']/g, "'");
  },

  _escape(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  },

  _escAttr(s) {
    return String(s || '')
      .replace(/&/g,'&amp;').replace(/"/g,'&quot;')
      .replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/'/g,'&#39;');
  },

  // ── Modal flutuante de palavra ─────────────────────────────
  _abrirModalPalavra(wordEl) {
    this._fecharModal(false);

    const palavra  = wordEl.dataset.palavra || wordEl.textContent.trim();
    const ipa      = wordEl.dataset.ipa  || '';
    const trad     = wordEl.dataset.trad || '';
    const cat      = wordEl.dataset.cat  || '';
    const temVocab = !!(ipa || trad || cat);
    const il       = I18n.idioma === 'it';
    const jaSalva  = this._verificarSalva(palavra);

    const tradPills = trad
      ? trad.split(/[;,]/).map(t => t.trim()).filter(Boolean)
             .map(t => `<span class="storie-trad-pill">${this._escape(t)}</span>`).join('')
      : '';

    const modal = document.getElementById('storie-word-modal');
    if (!modal) return;

    modal.innerHTML = `
      <button class="storie-modal-close" onclick="Storie._fecharModal()">×</button>
      <div class="storie-modal-palavra">${this._escape(palavra)}</div>
      ${ipa ? `<div class="storie-modal-ipa">${this._escape(ipa)}</div>` : ''}
      <button class="storie-modal-audio" onclick="App.pronunciar('${this._escAttr(palavra)}')">🔊 ${il?'Ascolta':'Ouvir'}</button>
      ${tradPills ? `<div class="storie-modal-traducoes">${tradPills}</div>` : ''}
      ${cat ? `<div style="margin-top:0.45rem"><span class="storie-modal-cat">${this._escape(cat)}</span></div>` : ''}
      ${!temVocab ? `<div style="font-size:0.75rem;color:rgba(255,255,255,0.45);margin-top:0.5rem;font-style:italic">${il?'Parola non catalogata':'Palavra não catalogada'}</div>` : ''}
      <button class="storie-modal-salvar${jaSalva?' salvo':''}" id="storie-btn-salvar"
        onclick="Storie._salvarNoDeck('${this._escAttr(palavra)}',{ipa:'${this._escAttr(ipa)}',trad:'${this._escAttr(trad)}',cat:'${this._escAttr(cat)}'})">
        ${jaSalva
          ? `✅ ${il ? 'Già salvata' : 'Já salva'}`
          : `⭐ ${il ? 'Salva per revisione' : 'Salvar para revisão'}`}
      </button>`;

    modal.style.display = 'block';
    this._posicionarModal(modal, wordEl);

    const overlay = document.getElementById('storie-modal-overlay');
    if (overlay) overlay.style.display = 'block';
  },

  _posicionarModal(modal, wordEl) {
    // Oculta para medir sem flicker
    modal.style.visibility = 'hidden';

    requestAnimationFrame(() => {
      const rect = wordEl.getBoundingClientRect();
      const mW   = modal.offsetWidth  || 260;
      const mH   = modal.offsetHeight || 190;
      const vW   = window.innerWidth;
      const vH   = window.innerHeight;

      let left = rect.left + rect.width / 2 - mW / 2;
      let top  = rect.top  - mH - 10;

      // Prefere abaixo se não cabe acima
      if (top < 8) top = rect.bottom + 10;
      // Fallback centralizado verticalmente
      if (top + mH > vH - 8) top = Math.max(8, Math.round(vH / 2 - mH / 2));

      if (left < 8)               left = 8;
      if (left + mW > vW - 8)     left = vW - mW - 8;

      modal.style.left       = `${left}px`;
      modal.style.top        = `${top}px`;
      modal.style.visibility = 'visible';
    });
  },

  _fecharModal(removeEsc = true) {
    const modal   = document.getElementById('storie-word-modal');
    const overlay = document.getElementById('storie-modal-overlay');
    if (modal)   modal.style.display   = 'none';
    if (overlay) overlay.style.display = 'none';
    if (removeEsc && this._escListener) {
      document.removeEventListener('keydown', this._escListener);
      this._escListener = null;
    }
  },

  // ── Salvar palavra no deck SRS ─────────────────────────────
  _salvarNoDeck(palavra, dados) {
    if (this._verificarSalva(palavra)) return;

    const id = 'story_' + this._normWord(palavra).replace(/\W/g, '_') + '_' + Date.now();
    const entrada = {
      id,
      italiano:  palavra,
      portugues: dados?.trad || '',
      categoria: dados?.cat  || 'vocabulo',
      templo_num: 0,
      _custom:    true,
      _from_story: true,
    };

    // Persistir em localStorage
    try {
      const key    = 'it_vocab_custom';
      const custom = JSON.parse(localStorage.getItem(key) || '[]');
      if (!custom.find(v => (v.italiano||'').toLowerCase() === palavra.toLowerCase())) {
        custom.push(entrada);
        localStorage.setItem(key, JSON.stringify(custom));
      }
    } catch(e) {}

    // Injetar no vocabCache global
    if (typeof App !== 'undefined' && App.estado?.vocabCache) {
      if (!App.estado.vocabCache.find(v => (v.italiano||'').toLowerCase() === palavra.toLowerCase())) {
        App.estado.vocabCache.unshift(entrada);
      }
    }

    // Inicializar estado FSRS
    if (typeof App !== 'undefined' && App.estado?.flashcardData) {
      if (!App.estado.flashcardData[id]) {
        App.estado.flashcardData[id] = {
          state: 'new', reps: 0, lapses: 0,
          stability: 0, difficulty: 5,
          nextReview: Date.now(),
        };
        if (App.salvarFlashcards) App.salvarFlashcards();
      }
    }

    // Feedback visual no botão
    const btn = document.getElementById('storie-btn-salvar');
    if (btn) {
      const il = I18n.idioma === 'it';
      btn.textContent = `✅ ${il ? 'Già salvata' : 'Já salva'}`;
      btn.classList.add('salvo');
    }

    // Destaca todas as ocorrências no texto
    this._marcarPalavraSalvaNoDOM(palavra);
  },

  _verificarSalva(palavra) {
    if (typeof App === 'undefined' || !App.estado?.vocabCache) return false;
    const norm = (palavra || '').toLowerCase();
    return App.estado.vocabCache.some(v => (v.italiano || '').toLowerCase() === norm);
  },

  _marcarPalavraSalvaNoDOM(palavra) {
    const norm = (palavra || '').toLowerCase();
    document.querySelectorAll('.storie-palavra').forEach(el => {
      if ((el.dataset.palavra || '').toLowerCase() === norm) {
        el.classList.add('storie-palavra-salva');
      }
    });
  },

  // ── Ações ─────────────────────────────────────────────────
  _toggleTraduzir() {
    this.traduzirVisivel = !this.traduzirVisivel;
    this._renderizarStoria();
  },

  _ouvirTudo() {
    if (!this.storAttuale) return;
    const texto = this.storAttuale.testo.map(p => p.italiano).join(' ');
    if (typeof App !== 'undefined' && App.pronunciar) App.pronunciar(texto);
  },

  _marcarLida() {
    if (!this.storAttuale) return;
    const id = this.storAttuale.id;
    const il = I18n.idioma === 'it';
    if (this.completate.includes(id)) {
      App.notificar(il ? 'notif_gia_letta' : 'notif_ja_lida', 'info');
      return;
    }
    this.completate.push(id);
    this._salvarCompletate();
    const xp = this.storAttuale.xp_recompensa || 50;
    if (typeof App !== 'undefined' && App.adicionarXP) App.adicionarXP(xp);
    App.notificar(il ? `notif_storia_letta_${id}` : `notif_storia_lida_${id}`, 'sucesso');
    this._renderizarStoria();
  },

  // ── Inicialização ao navegar para a aba ────────────────────
  init() {
    this.renderizarSeletor();
  },
};
