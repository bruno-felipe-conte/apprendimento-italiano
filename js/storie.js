// ============================================================
// storie.js — Módulo de leitura interativa de histórias italianas
// - 10 histórias A1-C2 (data/storie.json)
// - Tradução toggle por parágrafo
// - TTS via App.pronunciar
// - Vocabulário inline clicável
// - Marcar como lida + XP recompensa
// ============================================================

const Storie = {
  dados: null,
  storAttuale: null,
  paragrafoAttivo: 0,
  traduzirVisivel: true,
  completate: [],

  // ── Carregar dados ─────────────────────────────────────────
  async carregar() {
    if (!this.dados) {
      try {
        const r = await fetch('data/storie.json');
        if (r.ok) this.dados = await r.json();
        else this.dados = { storie: [] };
      } catch { this.dados = { storie: [] }; }
    }
    try {
      this.completate = JSON.parse(localStorage.getItem('it_storie_lidas') || '[]');
    } catch { this.completate = []; }
  },

  _salvarCompletate() {
    localStorage.setItem('it_storie_lidas', JSON.stringify(this.completate));
  },

  // ── Filtros ────────────────────────────────────────────────
  _filtroNivel: '',
  _filtroTexto: '',

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

    let html = `
      <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;margin-bottom:0.8rem">
        <input type="search" placeholder="${labels.cerca}" value="${this._filtroTexto}"
          oninput="Storie._filtroTexto=this.value;Storie.renderizarSeletor()"
          style="flex:1;min-width:120px;padding:0.42rem 0.7rem;border:1.5px solid #ddd;border-radius:8px;font-size:0.88rem">
      </div>
      <div style="display:flex;gap:0.3rem;flex-wrap:wrap;margin-bottom:1rem">
        <button onclick="Storie._filtroNivel='';Storie.renderizarSeletor()"
          style="padding:0.25rem 0.7rem;border-radius:999px;border:1.5px solid ${!this._filtroNivel ? '#9B2335' : '#ddd'};background:${!this._filtroNivel ? '#9B2335' : 'transparent'};color:${!this._filtroNivel ? '#fff' : 'inherit'};cursor:pointer;font-size:0.78rem;font-weight:600">
          ${labels.tut} (${todas.length})</button>
        ${niveis.filter(n => counts[n]).map(n => `<button onclick="Storie._filtroNivel='${n}';Storie.renderizarSeletor()"
          style="padding:0.25rem 0.7rem;border-radius:999px;border:1.5px solid ${this._filtroNivel === n ? '#9B2335' : '#ddd'};background:${this._filtroNivel === n ? '#9B2335' : 'transparent'};color:${this._filtroNivel === n ? '#fff' : 'inherit'};cursor:pointer;font-size:0.78rem;font-weight:600">
          ${n} (${counts[n]})</button>`).join('')}
      </div>
      <div class="dialogo-grid">`;

    for (const s of filtrate) {
      const isLida = this.completate.includes(s.id);
      const lidaBadge = isLida
        ? '<span style="font-size:0.65rem;background:#2A9D8F;color:white;padding:0.1rem 0.4rem;border-radius:6px;margin-left:0.3rem;">✓</span>'
        : '';
      html += `<div class="dialogo-card" onclick="Storie.abrirStoria('${s.id}')">
        <div class="dialogo-icone">${s.icone || '📖'}</div>
        <div class="dialogo-titulo">${s.titulo}${lidaBadge}</div>
        <div style="font-size:0.75rem;color:#888;margin:0.2rem 0">${s.autor || ''}</div>
        <div style="display:flex;gap:0.3rem;justify-content:center;flex-wrap:wrap;margin-top:0.3rem;align-items:center;">
          <span class="dialogo-nivel">${s.nivel}</span>
          <span style="font-size:0.7rem;color:#9B2335;font-weight:600">+${s.xp_recompensa || 50} XP</span>
        </div>
      </div>`;
    }

    if (filtrate.length === 0) {
      html += `<p style="text-align:center;color:#aaa;grid-column:1/-1">${this._filtroTexto ? labels.risultato : labels.nessuna}</p>`;
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
    this.paragrafoAttivo = 0;
    this.traduzirVisivel = true;
    this._renderizarStoria();
  },

  // ── Renderizar a história em modo leitura ──────────────────
  _renderizarStoria() {
    const c = document.getElementById('storie-container');
    if (!c || !this.storAttuale) return;
    const s = this.storAttuale;
    const i = I18n.idioma === 'it';

    const tituloExibido = i ? s.titulo : (s.titulo_pt || s.titulo);
    const descExibida = i ? s.descricao : (s.descricao_pt || s.descricao);

    const txtBtnTrad = i ? '👁️ Nascondi traduzione' : '👁️ Ocultar tradução';
    const txtBtnTradOff = i ? '👁️ Mostra traduzione' : '👁️ Mostrar tradução';
    const txtBtnTutto = i ? '🔊 Ascolta tutto' : '🔊 Ouvir tudo';
    const txtBtnIndietro = i ? '‹ Storie' : '‹ Storie';

    let html = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Storie.renderizarSeletor()">${txtBtnIndietro}</button>
        <span style="font-size:0.85rem;font-weight:700">${s.nivel} · +${s.xp_recompensa || 50} XP</span>
      </div>

      <div class="gram-card" style="margin-top:1rem;padding:1.2rem;text-align:center">
        <div style="font-size:2.6rem;margin-bottom:0.4rem">${s.icone || '📖'}</div>
        <h2 style="margin:0 0 0.3rem;font-family:'Playfair Display',serif;font-size:1.45rem;color:#9B2335">${tituloExibido}</h2>
        <div style="font-size:0.82rem;color:#666;font-style:italic">${s.autor || ''} · ${s.tema || ''}</div>
        <p style="font-size:0.85rem;color:#444;margin:0.7rem 0 0;line-height:1.4">${descExibida}</p>
        <div style="display:flex;gap:0.5rem;justify-content:center;flex-wrap:wrap;margin-top:1rem">
          <button class="btn-secondario" onclick="Storie._toggleTraduzir()">
            ${this.traduzirVisivel ? txtBtnTrad : txtBtnTradOff}
          </button>
          <button class="btn-primario" onclick="Storie._ouvirTudo()">${txtBtnTutto}</button>
        </div>
      </div>

      <div class="storie-paragrafi">`;

    s.testo.forEach((p, idx) => {
      const itText = this._markParole(p.italiano, p.parole || [], idx);
      const ptText = (p.portugues || '').replace(/</g, '&lt;');
      html += `
        <div class="storie-paragrafo" id="storie-par-${idx}">
          <div class="storie-paragrafo-it">
            <span class="storie-paragrafo-num">${idx + 1}</span>
            <span class="storie-texto-it">${itText}</span>
            <button class="storie-audio-btn" onclick="App.pronunciar('${(p.italiano || '').replace(/'/g, "\\'")}')" title="${i ? 'Ascolta' : 'Ouvir'}">🔊</button>
          </div>
          ${this.traduzirVisivel ? `<div class="storie-paragrafo-pt">${ptText}</div>` : ''}
          ${(p.parole && p.parole.length) ? this._renderVocabPanel(p.parole, idx) : ''}
        </div>`;
    });

    html += `
      </div>

      <div style="display:flex;gap:0.5rem;justify-content:space-between;margin-top:1.2rem;flex-wrap:wrap">
        <button class="btn-secondario" onclick="Storie.renderizarSeletor()">
          ${i ? '‹ Tutte le storie' : '‹ Todas as histórias'}
        </button>
        <button class="btn-primario" onclick="Storie._marcarLida()">
          ${this.completate.includes(s.id)
            ? (i ? '✓ Riletta' : '✓ Relida')
            : (i ? '✓ Ho finito' : '✓ Concluí (+' + (s.xp_recompensa || 50) + ' XP)')}
        </button>
      </div>`;

    c.innerHTML = html;
  },

  // ── Marcar palavras inline com span clicável ───────────────
  _markParole(texto, parole, idxPar) {
    if (!parole || parole.length === 0) return this._escape(texto);
    let out = this._escape(texto);
    for (const p of parole) {
      // Encontra a palavra (case-insensitive) e envolve com <span>
      const safeWord = p.parola.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`\\b(${safeWord})\\b`, 'i');
      out = out.replace(regex,
        `<span class="storie-parola" data-idx-par="${idxPar}" data-word="${this._escape(p.parola)}">$1</span>`);
    }
    return out;
  },

  _escape(s) {
    return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  },

  // ── Painel de vocabulário por parágrafo (recolhível) ───────
  _renderVocabPanel(parole, idxPar) {
    const i = I18n.idioma === 'it';
    const cards = parole.map(p => `
      <div class="storie-vocab-card" onclick="App.pronunciar('${(p.parola || '').replace(/'/g, "\\'")}')">
        <div class="storie-vocab-it">${this._escape(p.parola)} <span class="storie-vocab-ipa">${p.ipa || ''}</span></div>
        <div class="storie-vocab-pt">${this._escape(p.traduzione || '')}</div>
        <div class="storie-vocab-cat">${this._escape(p.categoria || '')}</div>
      </div>
    `).join('');
    return `
      <details class="storie-vocab-details">
        <summary>${i ? `📚 Vocabolario (${parole.length})` : `📚 Vocabulário (${parole.length})`}</summary>
        <div class="storie-vocab-grid">${cards}</div>
      </details>`;
  },

  // ── Ações ─────────────────────────────────────────────────
  _toggleTraduzir() {
    this.traduzirVisivel = !this.traduzirVisivel;
    this._renderizarStoria();
  },

  _ouvirTudo() {
    if (!this.storAttuale) return;
    const paragrafi = this.storAttuale.testo.map(p => p.italiano).join(' ');
    if (typeof App !== 'undefined' && App.pronunciar) {
      App.pronunciar(paragrafi);
    }
  },

  _marcarLida() {
    if (!this.storAttuale) return;
    const id = this.storAttuale.id;
    const i = I18n.idioma === 'it';
    if (this.completate.includes(id)) {
      App.notificar(i ? 'notif_gia_letta' : 'notif_ja_lida', 'info');
      return;
    }
    this.completate.push(id);
    this._salvarCompletate();
    const xp = this.storAttuale.xp_recompensa || 50;
    if (typeof App !== 'undefined' && App.adicionarXP) {
      App.adicionarXP(xp);
    }
    App.notificar(i ? `notif_storia_letta_${id}` : `notif_storia_lida_${id}`, 'sucesso');
    this._renderizarStoria();
  },

  // ── Inicialização ao navegar para a aba ────────────────────
  init() {
    this.renderizarSeletor();
  },
};
