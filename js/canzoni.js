const Canzoni = {
  dados: null,        // built-in (data/canzoni.json)
  custom: [],         // criados pelo usuário (localStorage)
  canzonAtual: null,
  estrofeAtual: 0,
  acertos: 0,
  modoEdicao: false,  // true quando está criando/editando

  // ── Carregar built-in + custom ─────────────────────────────
  async carregar() {
    // 1. Carrega built-in
    if (!this.dados) {
      try {
        const r = await fetch('data/canzoni.json');
        if (r.ok) this.dados = await r.json();
        else this.dados = { canzoni: [] };
      } catch { this.dados = { canzoni: [] }; }
    }
    // 2. Carrega custom do localStorage
    try {
      this.custom = JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]');
    } catch { this.custom = []; }
  },

  // ── Retorna TODAS as músicas (built-in + custom) ───────────
  todasCanzoni() {
    const builtin = (this.dados?.canzoni || []);
    return [...builtin, ...this.custom];
  },

  // ── Salvar custom no localStorage ─────────────────────────
  _salvarCustom() {
    localStorage.setItem('it_canzoni_custom', JSON.stringify(this.custom));
  },

  // ── Renderizar seletor com built-in + custom + botão criar ─
  _filtroNivel: '',
  _filtroTexto: '',

  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('canzoni-container');
    if (!c) return;

    const todas = this.todasCanzoni();
    const niveis = ['A1','A2','B1','B2','C1','C2'];
    const counts = {};
    todas.forEach(s => { counts[s.nivel] = (counts[s.nivel]||0)+1; });

    let filtradas = todas;
    if (this._filtroNivel) filtradas = filtradas.filter(s => s.nivel === this._filtroNivel);
    if (this._filtroTexto) {
      const q = this._filtroTexto.toLowerCase();
      filtradas = filtradas.filter(s => s.titulo.toLowerCase().includes(q) || (s.artista||'').toLowerCase().includes(q));
    }

    // Ordenar: volumes da mesma música ficam juntos em sequência
    filtradas = [...filtradas].sort((a, b) => {
      const getBase = t => t.replace(/\s*\(Vol\.?\s*\d+\)\s*$/i, '').trim();
      const getVol  = t => { const m = t.match(/\(Vol\.?\s*(\d+)\)/i); return m ? parseInt(m[1]) : 0; };
      const baseA = getBase(a.titulo), baseB = getBase(b.titulo);
      if (baseA !== baseB) return baseA.localeCompare(baseB, 'it');
      return getVol(a.titulo) - getVol(b.titulo);
    });

    let html = `
      <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;margin-bottom:0.8rem;justify-content:center">
        <input type="search" placeholder="🔍 Titolo o artista..." value="${this._filtroTexto}"
          oninput="Canzoni._filtroTexto=this.value;Canzoni.renderizarSeletor()"
          style="flex:1;min-width:120px;padding:0.42rem 0.7rem;border:1.5px solid #ddd;border-radius:8px;font-size:0.88rem">
        <button class="btn-primario" onclick="Canzoni.abrirFormularioCriar()" style="white-space:nowrap">${I18n.t('can_btn_adicionar')}</button>
        <button class="btn-ia-add" onclick="IAImport.abrir('canzone')" style="white-space:nowrap">🤖 via IA</button>
      </div>
      <div style="display:flex;gap:0.3rem;flex-wrap:wrap;margin-bottom:1rem;justify-content:center">
        <button onclick="Canzoni._filtroNivel='';Canzoni.renderizarSeletor()"
          style="padding:0.25rem 0.7rem;border-radius:999px;border:1.5px solid ${!this._filtroNivel?'#9B2335':'#ddd'};background:${!this._filtroNivel?'#9B2335':'transparent'};color:${!this._filtroNivel?'#fff':'inherit'};cursor:pointer;font-size:0.78rem;font-weight:600">
          Tutte (${todas.length})</button>
        ${niveis.filter(n=>counts[n]).map(n => `<button onclick="Canzoni._filtroNivel='${n}';Canzoni.renderizarSeletor()"
          style="padding:0.25rem 0.7rem;border-radius:999px;border:1.5px solid ${this._filtroNivel===n?'#9B2335':'#ddd'};background:${this._filtroNivel===n?'#9B2335':'transparent'};color:${this._filtroNivel===n?'#fff':'inherit'};cursor:pointer;font-size:0.78rem;font-weight:600">
          ${n} (${counts[n]})</button>`).join('')}
      </div>
      <div class="dialogo-grid">`;

    for (const can of filtradas) {
      const ehCustom = can.custom || can._custom;
      const badgeCustom = ehCustom ? '<span style="font-size:0.65rem;background:#7B68A0;color:white;padding:0.1rem 0.4rem;border-radius:6px;margin-left:0.3rem;">Minha</span>' : '';
      html += `<div class="dialogo-card" onclick="Canzoni.abrirCanzone('${can.id}')">
        <div class="dialogo-icone">${can.icone || '🎵'}</div>
        <div class="dialogo-titulo">${can.titulo}${badgeCustom}</div>
        <div style="font-size:0.75rem;color:#888;margin:0.2rem 0">${can.artista || ''}</div>
        <div style="display:flex;gap:0.3rem;justify-content:center;flex-wrap:wrap;margin-top:0.3rem;align-items:center;">
          <span class="dialogo-nivel">${can.nivel}</span>
          ${ehCustom ? `
          ${can.custom ? `<button onclick="event.stopPropagation();Canzoni.editarCanzone('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Editar">✏️</button>` : ''}
          <button onclick="event.stopPropagation();Canzoni.excluirCanzone('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Excluir">🗑️</button>` : ''}
        </div>
      </div>`;
    }

    if (filtradas.length === 0) {
      html += `<p style="text-align:center;color:#aaa;grid-column:1/-1">${this._filtroTexto ? 'Nessun risultato.' : 'Nessuna canzone ancora.'}</p>`;
    }

    html += '</div>';
    c.innerHTML = html;
  },

  // ── Formulário de CRIAÇÃO ──────────────────────────────────
  abrirFormularioCriar(idEditar = null) {
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
            <input type="text" placeholder="Dica (ex: stagione calda)" data-campo="dica" data-idx="${i}"
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
    // Re-numerar
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

    // Coletar estrofes
    const estrofes = [];
    document.querySelectorAll('.can-estrofe-form').forEach((el, i) => {
      const campos = {};
      el.querySelectorAll('[data-campo]').forEach(inp => { campos[inp.dataset.campo] = inp.value.trim(); });
      if (campos.texto_completo && campos.palavra_oculta) {
        // Auto-gerar texto_lacuna se não preenchido
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

  excluirCanzone(id) {
    const can = this.custom.find(x => x.id === id);
    if (!can) return;
    if (!confirm(I18n.t('can_excluir_confirm').replace('{t}', can.titulo))) return;
    this.custom = this.custom.filter(x => x.id !== id);
    this._salvarCustom();
    App.notificar('notif_can_excluida', 'alerta');
    this.renderizarSeletor();
  },

  // ── MÉTODOS DE JOGO ──────────────────────────────────────────
  async abrirCanzone(id) {
    await this.carregar();
    this.canzonAtual = this.todasCanzoni().find(c => c.id === id);
    this.estrofeAtual = 0;
    this.acertos = 0;
    this.renderizarEstrofe();
  },
  
  renderizarEstrofe() {
    const c = document.getElementById('canzoni-container');
    if (!c || !this.canzonAtual) return;
    const can = this.canzonAtual;
    const est = can.estrofes[this.estrofeAtual];
    const total = can.estrofes.length;
    const pct = Math.round(this.estrofeAtual / total * 100);
    
    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Canzoni.renderizarSeletor()">‹ Canzoni</button>
        <span style="font-size:0.85rem;color:var(--cor-pietra)">${this.estrofeAtual+1}/${total}</span>
      </div>
      <div style="text-align:center;padding:1rem 0 0.5rem">
        <div style="font-size:1.5rem">${can.icone}</div>
        <div style="font-family:'Cinzel',serif;font-weight:700;color:var(--cor-veneziano-escuro)">${can.titulo}</div>
        <div style="font-size:0.8rem;color:var(--cor-pietra)">${can.artista}</div>
      </div>
      <div class="gram-ex-progress-bar" style="margin:0.5rem 1rem"><div class="gram-ex-progress-fill" style="width:${pct}%"></div></div>
      <div class="gram-card" style="margin:1rem">
        <div style="font-size:1rem;line-height:1.8;padding:1rem;text-align:center;font-style:italic;color:var(--cor-inchiostro)">
          ${est.texto_lacuna.replace('___', '<input id="canzone-input" type="text" autocomplete="off" autocorrect="off" spellcheck="false" style="border:none;border-bottom:2px solid #9B2335;font-size:1rem;font-style:italic;width:100px;text-align:center;outline:none;background:transparent" placeholder="___" onkeydown="if(event.key===\'Enter\')Canzoni.verificar()">')}
        </div>
        <div style="text-align:center;font-size:0.82rem;color:var(--cor-pietra);font-style:italic;padding:0 1rem 0.5rem">${est.traducao}</div>
        <div style="text-align:center;font-size:0.78rem;color:var(--cor-toscano);padding-bottom:1rem">💡 Dica: ${est.dica}</div>
        <div id="canzone-feedback"></div>
        <div style="display:flex;justify-content:center;gap:0.5rem;padding:0.5rem">
          <button class="btn-primario" onclick="Canzoni.verificar()">✔ Verificar</button>
          <button class="btn-secondario" onclick="App.pronunciar('${est.texto_completo.replace(/'/g,"\\'")}')">🔊 Ouvir</button>
        </div>
      </div>`;
    setTimeout(() => document.getElementById('canzone-input')?.focus(), 100);
  },
  
  verificar() {
    const est = this.canzonAtual.estrofes[this.estrofeAtual];
    const input = document.getElementById('canzone-input');
    const fb = document.getElementById('canzone-feedback');
    if (!input || !fb) return;
    const digitado = input.value.trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const correto = est.palavra_oculta.trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
    const acertou = digitado === correto;
    if (acertou) {
      this.acertos++;
      if (typeof App !== 'undefined' && App.ganharXP) App.ganharXP(5);
      fb.innerHTML = `<div style="color:#27AE60;text-align:center;padding:0.5rem;font-weight:700">✅ Corretto! "${est.palavra_oculta}"</div>`;
    } else {
      fb.innerHTML = `<div style="color:#C0392B;text-align:center;padding:0.5rem">❌ A palavra era: <strong>${est.palavra_oculta}</strong></div>`;
    }
    input.disabled = true;
    input.value = est.palavra_oculta;
    input.style.color = acertou ? '#27AE60' : '#C0392B';
    setTimeout(() => {
      this.estrofeAtual++;
      if (this.estrofeAtual >= this.canzonAtual.estrofes.length) this.mostrarResultado();
      else this.renderizarEstrofe();
    }, 1500);
  },
  
  mostrarResultado() {
    const can = this.canzonAtual;
    const total = can.estrofes.length;
    const pct = Math.round(this.acertos / total * 100);
    if (typeof Progressao !== 'undefined' && Progressao.ganhar) Progressao.ganhar(can.xp_recompensa);
    const c = document.getElementById('canzoni-container');
    c.innerHTML = `<div style="text-align:center;padding:2rem">
      <div style="font-size:3rem">${pct >= 80 ? '🎤' : '🎵'}</div>
      <div style="font-family:'Cinzel',serif;font-size:1.2rem;color:var(--cor-veneziano-escuro);margin:0.5rem 0">${can.titulo}</div>
      <div style="font-size:1.5rem;font-weight:700;margin:0.5rem 0">${I18n.t('can_corretas').replace('{a}', this.acertos).replace('{b}', total)}</div>
      <div style="color:var(--cor-pietra);margin-bottom:1rem">+${can.xp_recompensa} XP</div>
      <div style="display:flex;gap:0.5rem;justify-content:center">
        <button class="btn-primario" onclick="Canzoni.abrirCanzone('${can.id}')">${I18n.t('can_repetir')}</button>
        <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">${I18n.t('can_outras_musicas')}</button>
      </div>
    </div>`;
  }
};

document.addEventListener('i18n:changed', () => {
  if (document.getElementById('canzoni-container')) Canzoni.renderizarSeletor();
});
