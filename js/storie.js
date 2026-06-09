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
  traduzirVisivel: false,
  completate: [],
  _filtroNivel: '',
  _filtroTexto: '',
  _filtroOrigem: '',
  _escListener: null,
  _tradCache: {},   // cache in-memory: palavra → tradução

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
      <!-- Linha 1: busca + ação -->
      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem">
        <input type="search" placeholder="${labels.cerca}" value="${this._filtroTexto}"
          oninput="Storie._filtroTexto=this.value;Storie.renderizarSeletor()"
          style="flex:1;min-width:0;padding:0.45rem 0.8rem;border:1.5px solid var(--cor-pietra);border-radius:20px;font-size:0.88rem;background:var(--cor-marmore);color:var(--cor-inchiostro);font-family:inherit">
        <button class="btn-ia-add" onclick="IAImport.abrir('storia')" style="white-space:nowrap">🤖 via IA</button>
      </div>
      <!-- Linha 2: filtros -->
      <div style="display:flex;gap:0.35rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
        ${(()=>{const nC=todas.filter(s=>s._custom||s.custom).length;const nN=todas.length-nC;const _o=this._filtroOrigem;
          const oP=(v,l,ct)=>`<button onclick="Storie._filtroOrigem='${v}';Storie.renderizarSeletor()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid ${_o===v?'#7B68A0':'#ccc'};background:${_o===v?'#7B68A0':'transparent'};color:${_o===v?'#fff':'var(--cor-inchiostro)'};cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap;font-family:inherit">${l} (${ct})</button>`;
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
    const lista = this.dados?.storie || [];
    const idx   = lista.findIndex(x => x.id === id);
    if (idx === -1) return;
    this.storAttuale   = lista[idx];
    this._storyIndex   = idx;        // índice para numeração de página
    this.traduzirVisivel = false;
    this._renderizarStoria();
  },

  // ── Renderizar a história em modo livro aberto ────────────
  _renderizarStoria() {
    const c = document.getElementById('storie-container');
    if (!c || !this.storAttuale) return;
    const s = this.storAttuale;
    const il = I18n.idioma === 'it';

    const tituloExibido = il ? s.titulo : (s.titulo_pt || s.titulo);

    // Constrói HTML de um grupo de parágrafos
    const buildParas = (paras, startIdx) => paras.map((p, i) => {
      const idx = startIdx + i;
      const textoMarcado = this._marcarPalavras(p.italiano, p.parole || [], idx);
      const ptText = (p.portugues || '').replace(/</g, '&lt;');
      return `<div class="storie-bloco"><p class="storie-p">${textoMarcado}</p>${this.traduzirVisivel && ptText ? `<span class="storie-trad-p">${ptText}</span>` : ''}</div>`;
    }).join('');

    // Divide parágrafos entre página esquerda e direita
    const mid   = Math.ceil(s.testo.length / 2);
    const pgEsq = buildParas(s.testo.slice(0, mid), 0);
    const pgDir = buildParas(s.testo.slice(mid), mid);

    // Numeração: páginas ímpares à esquerda, pares à direita
    // As 2 primeiras páginas (1-2) são capa/guarda; histórias começam na 3
    const paginaBase = (this._storyIndex || 0) * 2 + 3;
    const paginaEsq  = paginaBase;
    const paginaDir  = paginaBase + 1;

    const html = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Storie._fecharModal();Storie.renderizarSeletor()">‹ Storie</button>
        <span style="font-size:0.85rem;font-weight:700">${s.nivel} · +${s.xp_recompensa||50} XP</span>
      </div>

      <div style="display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap;margin:0.8rem 0 0">
        <button class="btn-secondario" onclick="Storie._toggleTraduzir()">
          ${this.traduzirVisivel
            ? (il ? '👁️ Nascondi traduzione' : '👁️ Ocultar tradução')
            : (il ? '👁️ Mostra traduzione'   : '👁️ Mostrar tradução')}
        </button>
        <button class="btn-primario" onclick="Storie._ouvirTudo()">
          ${il ? '🔊 Ascolta tutto' : '🔊 Ouvir tudo'}
        </button>
      </div>

      <div class="book-scene">
        <div class="book-spread">

          <div class="book-page book-page-left storie-texto-corrido">
            <div class="book-header">
              <span class="book-icon">${s.icone||'📖'}</span>
              <div class="book-titulo">${tituloExibido}</div>
              <div class="book-subtitulo">${s.autor||''} · ${s.tema||''}</div>
              <div class="book-ornamento">— ✦ —</div>
            </div>
            ${pgEsq}
            <div class="book-pagina">— ${paginaEsq} —</div>
          </div>

          <div class="book-page book-page-right storie-texto-corrido">
            ${pgDir}
            <div class="book-ornamento" style="margin-top:auto;padding-top:1rem">— ✦ —</div>
            <div class="book-fine">${il ? 'Fine' : 'Fim'}</div>
            <div class="book-pagina">— ${paginaDir} —</div>
          </div>

        </div>
      </div>

      <div style="display:flex;gap:0.5rem;justify-content:space-between;margin-top:1rem;padding-top:1rem;border-top:1px solid var(--cor-pietra)">
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

    // Remove modais antigos do body (de render anterior)
    document.getElementById('storie-word-modal')?.remove();
    document.getElementById('storie-modal-overlay')?.remove();

    c.innerHTML = html;

    // Move modal para document.body — position:fixed usa viewport como referência
    const modalEl   = c.querySelector('#storie-word-modal');
    const overlayEl = c.querySelector('#storie-modal-overlay');
    if (modalEl)   document.body.appendChild(modalEl);
    if (overlayEl) document.body.appendChild(overlayEl);

    // Delegação de cliques (ambas as páginas)
    c.querySelectorAll('.storie-texto-corrido').forEach(textoEl => {
      textoEl.addEventListener('click', (e) => {
        const wordEl = e.target.closest('.storie-palavra');
        if (wordEl) { e.stopPropagation(); this._abrirModalPalavra(wordEl); }
        else        { this._fecharModal(); }
      });
    });

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
    let primeiraWord = true; // para capitular no primeiro parágrafo

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

      // Capitular: primeira letra do primeiro parágrafo (parIdx===0)
      let inner = this._escape(tok);
      if (parIdx === 0 && primeiraWord) {
        primeiraWord = false;
        inner = `<span class="storie-capitular">${this._escape(tok[0])}</span>${this._escape(tok.slice(1))}`;
      } else if (primeiraWord) {
        primeiraWord = false;
      }

      return `<span class="${classes.join(' ')}" ${attrs.join(' ')}>${inner}</span>`;
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

    const palavra = wordEl.dataset.palavra || wordEl.textContent.trim();
    let ipa  = wordEl.dataset.ipa  || '';
    let trad = wordEl.dataset.trad || '';
    let cat  = wordEl.dataset.cat  || '';

    // Busca global em todos os parágrafos da história
    if (!trad && this.storAttuale) {
      for (const p of this.storAttuale.testo) {
        const found = (p.parole || []).find(pw =>
          this._normWord(pw.parola) === this._normWord(palavra)
        );
        if (found) {
          ipa  = ipa  || found.ipa        || '';
          trad = trad || found.traduzione || '';
          cat  = cat  || found.categoria  || '';
          break;
        }
      }
    }

    const il      = I18n.idioma === 'it';
    const jaSalva = this._verificarSalva(palavra);

    // Se já temos trad do parole[], renderiza direto
    // Caso contrário, verifica cache → mostra placeholder → busca API
    const tradInicial = trad;

    const buildPills = (t) => t
      ? t.split(/[;,]/).map(s => s.trim()).filter(Boolean)
          .map(s => `<span class="storie-trad-pill">${this._escape(s)}</span>`).join('')
      : '';

    const renderModal = (tradAtual, carregando = false) => {
      const pills = buildPills(tradAtual);
      return `
        <button class="storie-modal-close" onclick="Storie._fecharModal()">×</button>
        <div class="storie-modal-palavra">${this._escape(palavra)}</div>
        ${ipa ? `<div class="storie-modal-ipa">${this._escape(ipa)}</div>` : ''}
        <button class="storie-modal-audio" onclick="App.pronunciar('${this._escAttr(palavra)}')">🔊 ${il?'Ascolta':'Ouvir'}</button>
        <div class="storie-modal-traducoes" id="storie-modal-pills">
          ${pills || (carregando ? '<span class="storie-trad-loading">…</span>' : '')}
        </div>
        ${cat ? `<div style="margin-top:0.45rem"><span class="storie-modal-cat">${this._escape(cat)}</span></div>` : ''}
        <button class="storie-modal-salvar${jaSalva?' salvo':''}" id="storie-btn-salvar"
          onclick="Storie._salvarNoDeck('${this._escAttr(palavra)}',{ipa:'${this._escAttr(ipa)}',trad:'${this._escAttr(tradAtual)}',cat:'${this._escAttr(cat)}'})">
          ${jaSalva
            ? `✅ ${il ? 'Già salvata' : 'Já salva'}`
            : `⭐ ${il ? 'Salva per revisione' : 'Salvar para revisão'}`}
        </button>`;
    };

    const modal = document.getElementById('storie-word-modal');
    if (!modal) return;

    // Renderiza imediatamente (com loading se sem trad)
    modal.innerHTML = renderModal(tradInicial, !tradInicial);
    modal.style.display = 'block';
    this._posicionarModal(modal, wordEl);

    const overlay = document.getElementById('storie-modal-overlay');
    if (overlay) overlay.style.display = 'block';

    // Se não tem tradução, busca via API (com cache)
    if (!tradInicial) {
      this._buscarTradAPI(palavra).then(tradAPI => {
        // Verifica se o modal ainda mostra esta palavra
        const pillsEl = document.getElementById('storie-modal-pills');
        if (!pillsEl) return;
        if (tradAPI) {
          pillsEl.innerHTML = buildPills(tradAPI);
          // Atualiza o onclick do botão salvar com a trad real
          const btn = document.getElementById('storie-btn-salvar');
          if (btn) btn.setAttribute('onclick',
            `Storie._salvarNoDeck('${this._escAttr(palavra)}',{ipa:'${this._escAttr(ipa)}',trad:'${this._escAttr(tradAPI)}',cat:'${this._escAttr(cat)}'})`);
        } else {
          pillsEl.innerHTML = '';
        }
      });
    }
  },

  // ── Tradução via MyMemory API (gratuita, sem chave) ────────
  async _buscarTradAPI(palavra) {
    const norm = this._normWord(palavra);
    if (this._tradCache[norm]) return this._tradCache[norm];
    try {
      const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(palavra)}&langpair=it|pt-BR`;
      const res  = await fetch(url, { signal: AbortSignal.timeout(4000) });
      const json = await res.json();
      const t    = json?.responseData?.translatedText || '';
      // Filtra respostas ruins (igual à entrada ou muito longas)
      const boa  = t && t.toLowerCase() !== palavra.toLowerCase() && t.split(' ').length <= 4;
      const val  = boa ? t : '';
      this._tradCache[norm] = val;
      return val;
    } catch { return ''; }
  },

  _posicionarModal(modal, wordEl) {
    modal.style.visibility = 'hidden';
    modal.classList.remove('seta-baixo', 'seta-cima');

    // Duplo rAF garante layout computado após display:block
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const rect = wordEl.getBoundingClientRect();
      const mW   = modal.offsetWidth  || 260;
      const mH   = modal.offsetHeight || 200;
      // clientWidth é mais confiável que innerWidth no mobile (ignora scrollbar)
      const vW   = document.documentElement.clientWidth;
      const vH   = document.documentElement.clientHeight;
      const SETA = 9;  // altura da seta CSS em px
      const PAD  = 8;  // margem mínima das bordas do viewport

      // Centro horizontal da palavra
      const wordCX = rect.left + rect.width / 2;

      // Tenta centralizar o modal sobre a palavra
      let left = wordCX - mW / 2;
      // Clamp horizontal
      if (left < PAD)               left = PAD;
      if (left + mW > vW - PAD)     left = vW - mW - PAD;
      // Se ainda não cabe (modal maior que viewport), alinha à esquerda
      if (left < 0) left = PAD;

      // Seta sempre aponta para o centro da palavra, independente do deslocamento do modal
      const arrowLeft = Math.min(Math.max(wordCX - left, 16), mW - 16);
      modal.style.setProperty('--arrow-left', `${arrowLeft}px`);

      // Vertical: prefere acima
      let top;
      let setaDir;
      if (rect.top - mH - SETA - PAD >= 0) {
        top     = rect.top - mH - SETA;
        setaDir = 'seta-baixo';
        modal.style.setProperty('--modal-origin-y', '100%');
      } else {
        top     = rect.bottom + SETA;
        setaDir = 'seta-cima';
        modal.style.setProperty('--modal-origin-y', '0%');
      }

      if (top + mH > vH - PAD) top = vH - mH - PAD;
      if (top < PAD)            top = PAD;

      modal.style.setProperty('--modal-origin-x', `${arrowLeft}px`);
      modal.classList.add(setaDir);
      modal.style.left       = `${left}px`;
      modal.style.top        = `${top}px`;
      modal.style.visibility = 'visible';
    }));
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
