# SPEC — Conteúdo Criado pelo Usuário (Músicas e Diálogos)
## App: Italiano Autentico | Repo: bruno-felipe-conte/apprendimento-italiano

Usuários podem adicionar suas próprias músicas e diálogos ao app.
O conteúdo criado é salvo no **localStorage** do dispositivo e pode ser exportado/importado via JSON.

---

## ARQUITETURA DE DADOS — ONDE FICA CADA COISA

```
italian-learning-app-pro/
│
├── data/
│   ├── canzoni.json          ← Músicas OFICIAIS (built-in, somente leitura)
│   ├── dialogi.json          ← Diálogos OFICIAIS (built-in, somente leitura)
│   └── [outros templos...]
│
├── js/
│   ├── canzoni.js            ← Módulo de músicas (lê oficial + custom)
│   ├── dialoghi.js           ← Módulo de diálogos (lê oficial + custom)
│   └── [outros módulos...]
│
└── index.html                ← UI dos formulários de criação

localStorage (no dispositivo do usuário):
  ├── it_canzoni_custom       ← Array JSON de músicas criadas pelo usuário
  ├── it_dialoghi_custom      ← Array JSON de diálogos criados pelo usuário
  ├── it_progresso            ← Progresso geral (já existe)
  └── it_flashcards           ← Dados FSRS (já existe)
```

---

## SCHEMA DO CONTEÚDO CUSTOM

### Música criada pelo usuário (`it_canzoni_custom`)

```json
[
  {
    "id": "custom_can_1748000000000",
    "titulo": "Azzurro",
    "artista": "Adriano Celentano",
    "nivel": "B1",
    "icone": "🎵",
    "tema": "minha-lista",
    "criado_em": 1748000000000,
    "custom": true,
    "estrofes": [
      {
        "id": 1,
        "texto_completo": "Cerco l'estate tutto l'anno e all'improvviso eccola qua.",
        "texto_lacuna": "Cerco l'___ tutto l'anno e all'improvviso eccola qua.",
        "palavra_oculta": "estate",
        "traducao": "Procuro o verão o ano todo e de repente aqui está.",
        "dica": "stagione calda"
      }
    ],
    "vocabulario_chave": ["estate", "improvviso"],
    "xp_recompensa": 30
  }
]
```

### Diálogo criado pelo usuário (`it_dialoghi_custom`)

```json
[
  {
    "id": "custom_dial_1748000000001",
    "titulo": "Conversazione al Bar",
    "icone": "☕",
    "nivel": "A1",
    "contexto": "Pedir um café num bar italiano.",
    "criado_em": 1748000000001,
    "custom": true,
    "turni": [
      {
        "id": 1,
        "personaggio": "Barista",
        "frase": "Prego?",
        "traducao": "Pois não?",
        "audio_ipa": ""
      },
      {
        "id": 2,
        "personaggio": "Tu",
        "frase": "Un caffè, per favore.",
        "traducao": "Um café, por favor.",
        "audio_ipa": "",
        "alternativas": [
          "Un caffè, per favore.",
          "Vorrei un tè.",
          "Niente, grazie.",
          "Un cornetto."
        ],
        "resposta_correta": 0
      }
    ],
    "vocabulario_chave": ["caffè", "barista"],
    "xp_recompensa": 30
  }
]
```

---

## IMPLEMENTAÇÃO — PASSO A PASSO

### PASSO 1 — Atualizar `js/canzoni.js`

**Adicionar métodos para ler/salvar conteúdo custom:**

```javascript
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
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('canzoni-container');
    if (!c) return;

    const todas = this.todasCanzoni();

    let html = `
      <div style="display:flex;justify-content:flex-end;margin-bottom:1rem;">
        <button class="btn-primario" onclick="Canzoni.abrirFormularioCriar()">➕ Adicionar Música</button>
      </div>
      <div class="dialogo-grid">`;

    for (const can of todas) {
      const badgeCustom = can.custom ? '<span style="font-size:0.65rem;background:#7B68A0;color:white;padding:0.1rem 0.4rem;border-radius:6px;margin-left:0.3rem;">Minha</span>' : '';
      html += `<div class="dialogo-card" onclick="Canzoni.abrirCanzone('${can.id}')">
        <div class="dialogo-icone">${can.icone || '🎵'}</div>
        <div class="dialogo-titulo">${can.titulo}${badgeCustom}</div>
        <div style="font-size:0.75rem;color:#888;margin:0.2rem 0">${can.artista || ''}</div>
        <div style="display:flex;gap:0.3rem;justify-content:center;flex-wrap:wrap;margin-top:0.3rem;">
          <span class="dialogo-nivel">${can.nivel}</span>
          ${can.custom ? `<button onclick="event.stopPropagation();Canzoni.editarCanzone('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Editar">✏️</button>
          <button onclick="event.stopPropagation();Canzoni.excluirCanzone('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Excluir">🗑️</button>` : ''}
        </div>
      </div>`;
    }

    if (todas.length === 0) {
      html += '<p style="text-align:center;color:#aaa;grid-column:1/-1;">Nenhuma música ainda. Adicione a sua!</p>';
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
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Nível</label>
            <select id="can-nivel" style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.9rem">
              ${['A1','A2','B1','B2','C1'].map(n => `<option ${n===nivel?'selected':''}>${n}</option>`).join('')}
            </select>
          </div>
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Ícone (emoji)</label>
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
    if (!titulo) { App.notificar('O título é obrigatório.', 'erro'); return; }

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
    if (estrofes.length === 0) { App.notificar('Adicione pelo menos um verso com lacuna.', 'erro'); return; }

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
    App.notificar(`🎵 "${titulo}" salva!`, 'sucesso');
    this.renderizarSeletor();
  },

  editarCanzone(id) {
    this.abrirFormularioCriar(id);
  },

  excluirCanzone(id) {
    const can = this.custom.find(x => x.id === id);
    if (!can) return;
    if (!confirm(`Excluir "${can.titulo}"?`)) return;
    this.custom = this.custom.filter(x => x.id !== id);
    this._salvarCustom();
    App.notificar('Música excluída.', 'alerta');
    this.renderizarSeletor();
  },

  // ... (manter métodos de jogo: abrirCanzone, renderizarEstrofe, verificar, mostrarResultado)
};
```

---

### PASSO 2 — Atualizar `js/dialoghi.js`

**Mesma lógica: built-in + custom + formulário de criação.**

```javascript
const Dialoghi = {
  dados: null,
  custom: [],

  async carregar() {
    if (!this.dados) {
      try {
        const r = await fetch('data/dialogi.json');
        this.dados = r.ok ? await r.json() : { dialogi: [] };
      } catch { this.dados = { dialogi: [] }; }
    }
    try {
      this.custom = JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]');
    } catch { this.custom = []; }
  },

  todosDialoghi() {
    return [...(this.dados?.dialogi || []), ...this.custom];
  },

  _salvarCustom() {
    localStorage.setItem('it_dialoghi_custom', JSON.stringify(this.custom));
  },

  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('dialoghi-container');
    if (!c) return;

    const todos = this.todosDialoghi();
    let html = `
      <div style="display:flex;justify-content:flex-end;margin-bottom:1rem;">
        <button class="btn-primario" onclick="Dialoghi.abrirFormularioCriar()">➕ Adicionar Diálogo</button>
      </div>
      <div class="dialogo-grid">`;

    for (const dial of todos) {
      const badge = dial.custom ? '<span style="font-size:0.65rem;background:#7B68A0;color:white;padding:0.1rem 0.4rem;border-radius:6px;margin-left:0.3rem;">Meu</span>' : '';
      html += `<div class="dialogo-card" onclick="Dialoghi.abrirDialogo('${dial.id}','leitura')">
        <div class="dialogo-icone">${dial.icone}</div>
        <div class="dialogo-titulo">${dial.titulo}${badge}</div>
        <div class="dialogo-nivel">${dial.nivel}</div>
        ${dial.custom ? `<div style="margin-top:0.4rem;display:flex;gap:0.3rem;justify-content:center">
          <button onclick="event.stopPropagation();Dialoghi.editarDialogo('${dial.id}')" style="background:none;border:none;cursor:pointer;font-size:0.9rem">✏️</button>
          <button onclick="event.stopPropagation();Dialoghi.excluirDialogo('${dial.id}')" style="background:none;border:none;cursor:pointer;font-size:0.9rem">🗑️</button>
        </div>` : ''}
      </div>`;
    }
    html += '</div>';
    c.innerHTML = html;
  },

  // ── Formulário para criar/editar diálogo ──────────────────
  abrirFormularioCriar(idEditar = null) {
    const c = document.getElementById('dialoghi-container');
    if (!c) return;
    const existente = idEditar ? this.custom.find(x => x.id === idEditar) : null;

    const titulo = existente?.titulo || '';
    const icone = existente?.icone || '💬';
    const nivel = existente?.nivel || 'A1';
    const contexto = existente?.contexto || '';
    const turni = existente?.turni || [
      { id:1, personaggio:'Personaggio', frase:'', traducao:'', audio_ipa:'', tipo:'fala' },
      { id:2, personaggio:'Tu', frase:'', traducao:'', audio_ipa:'', tipo:'resposta', alternativas:['','','',''], resposta_correta:0 }
    ];

    let turniHtml = '';
    turni.forEach((t, i) => { turniHtml += Dialoghi._htmlTurnoForm(t, i); });

    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Dialoghi.renderizarSeletor()">‹ Cancelar</button>
        <span style="font-size:0.9rem;font-weight:700">${idEditar ? 'Editar Diálogo' : 'Novo Diálogo'}</span>
      </div>

      <div class="gram-card" style="margin-top:1rem;padding:1.2rem">
        <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:0.7rem;margin-bottom:1rem">
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Título *</label>
            <input id="dial-titulo" type="text" value="${titulo}" placeholder="Ex: Al Bar"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem">
          </div>
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Nível</label>
            <select id="dial-nivel" style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem">
              ${['A1','A2','B1','B2','C1'].map(n=>`<option ${n===nivel?'selected':''}>${n}</option>`).join('')}
            </select>
          </div>
          <div>
            <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Ícone</label>
            <input id="dial-icone" type="text" value="${icone}" maxlength="4"
              style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;text-align:center;font-size:1.2rem">
          </div>
        </div>

        <div style="margin-bottom:1rem">
          <label style="font-size:0.82rem;font-weight:700;color:#9B2335">Contexto (descrição da situação)</label>
          <textarea id="dial-contexto" rows="2" placeholder="Ex: Você entra em um bar para pedir um café."
            style="width:100%;padding:0.5rem;border:2px solid #ddd;border-radius:8px;margin-top:0.3rem;font-size:0.88rem;resize:vertical">${contexto}</textarea>
        </div>

        <div style="font-size:0.85rem;font-weight:700;color:#9B2335;margin-bottom:0.8rem;border-top:1px solid #f0e8d8;padding-top:1rem">
          💬 Turnos do Diálogo
        </div>

        <div style="background:#FFF8E7;border:1px solid #D4A843;border-radius:8px;padding:0.7rem;margin-bottom:1rem;font-size:0.8rem;color:#6B4C1A">
          💡 <strong>Tipo "Fala":</strong> o personagem fala (o usuário só lê/ouve).<br>
          💡 <strong>Tipo "Resposta do Tu":</strong> o usuário escolhe entre 4 opções — preencha as 4 alternativas e marque qual é a correta.
        </div>

        <div id="dial-turni">${turniHtml}</div>

        <div style="display:flex;gap:0.5rem;margin:0.8rem 0">
          <button onclick="Dialoghi._adicionarTurnoFala()" class="btn-secondario" style="flex:1">➕ Adicionar Fala</button>
          <button onclick="Dialoghi._adicionarTurnoResposta()" class="btn-secondario" style="flex:1">➕ Resposta do Tu</button>
        </div>

        <div style="display:flex;gap:0.5rem">
          <button class="btn-primario" style="flex:1" onclick="Dialoghi._salvarFormulario('${idEditar || ''}')">
            💾 Salvar Diálogo
          </button>
          <button class="btn-secondario" onclick="Dialoghi.renderizarSeletor()">Cancelar</button>
        </div>
      </div>`;
  },

  _htmlTurnoForm(turno, i) {
    const ehResposta = turno.personaggio === 'Tu' && turno.alternativas;
    const alts = turno.alternativas || ['','','',''];
    const correto = turno.resposta_correta || 0;
    return `
      <div class="dial-turno-form" id="dial-turno-${i}" style="background:#f9f6f0;border-radius:10px;padding:0.9rem;margin-bottom:0.8rem;border:1px solid ${ehResposta ? '#9B2335' : '#ede5d5'}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem">
          <span style="font-weight:700;font-size:0.82rem;color:${ehResposta ? '#9B2335' : '#2C2C2C'}">
            ${ehResposta ? '👤 Resposta do Tu' : '🗣️ Fala do Personagem'}
          </span>
          <button onclick="Dialoghi._removerTurno(${i})" style="background:none;border:none;cursor:pointer;color:#C0392B;font-size:0.85rem">🗑️</button>
        </div>

        ${!ehResposta ? `
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-bottom:0.5rem">
            <input type="text" data-campo="personaggio" data-idx="${i}" value="${turno.personaggio || ''}"
              placeholder="Nome do personagem" style="padding:0.4rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem">
            <input type="text" data-campo="audio_ipa" data-idx="${i}" value="${turno.audio_ipa || ''}"
              placeholder="IPA (opcional)" style="padding:0.4rem;border:2px solid #ddd;border-radius:7px;font-size:0.85rem">
          </div>
          <input type="text" data-campo="frase" data-idx="${i}" value="${turno.frase || ''}"
            placeholder="Frase em italiano *" style="width:100%;padding:0.4rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem;margin-bottom:0.4rem">
          <input type="text" data-campo="traducao" data-idx="${i}" value="${turno.traducao || ''}"
            placeholder="Tradução em português" style="width:100%;padding:0.4rem;border:2px solid #ddd;border-radius:7px;font-size:0.85rem">
        ` : `
          <input type="text" data-campo="frase" data-idx="${i}" value="${turno.frase || ''}"
            placeholder="Frase correta em italiano *" style="width:100%;padding:0.4rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem;margin-bottom:0.4rem">
          <input type="text" data-campo="traducao" data-idx="${i}" value="${turno.traducao || ''}"
            placeholder="Tradução em português" style="width:100%;padding:0.4rem;border:2px solid #ddd;border-radius:7px;font-size:0.85rem;margin-bottom:0.6rem">
          <div style="font-size:0.78rem;font-weight:700;color:#9B2335;margin-bottom:0.4rem">4 Alternativas (marque a correta):</div>
          ${alts.map((a, ai) => `
            <div style="display:flex;align-items:center;gap:0.4rem;margin-bottom:0.3rem">
              <input type="radio" name="correct-${i}" value="${ai}" ${correto===ai?'checked':''} onchange="Dialoghi._marcarCorreta(${i},${ai})">
              <input type="text" data-campo="alt-${ai}" data-idx="${i}" value="${a}"
                placeholder="Alternativa ${ai+1}${ai===0?' (correta)':''}" style="flex:1;padding:0.4rem;border:2px solid ${ai===correto?'#27AE60':'#ddd'};border-radius:7px;font-size:0.85rem">
            </div>`).join('')}
          <input type="hidden" data-campo="resposta_correta" data-idx="${i}" value="${correto}">
        `}
        <input type="hidden" data-campo="_tipo" data-idx="${i}" value="${ehResposta ? 'resposta' : 'fala'}">
      </div>`;
  },

  _adicionarTurnoFala() {
    const container = document.getElementById('dial-turni');
    if (!container) return;
    const i = container.querySelectorAll('.dial-turno-form').length;
    const div = document.createElement('div');
    div.innerHTML = this._htmlTurnoForm({ personaggio:'Personaggio', frase:'', traducao:'', audio_ipa:'' }, i);
    container.appendChild(div.firstElementChild);
  },

  _adicionarTurnoResposta() {
    const container = document.getElementById('dial-turni');
    if (!container) return;
    const i = container.querySelectorAll('.dial-turno-form').length;
    const div = document.createElement('div');
    div.innerHTML = this._htmlTurnoForm({ personaggio:'Tu', frase:'', traducao:'', alternativas:['','','',''], resposta_correta:0 }, i);
    container.appendChild(div.firstElementChild);
  },

  _removerTurno(i) {
    document.getElementById(`dial-turno-${i}`)?.remove();
  },

  _marcarCorreta(turnoIdx, altIdx) {
    // Atualiza hidden field e borda das alternativas
    const turno = document.getElementById(`dial-turno-${turnoIdx}`);
    if (!turno) return;
    turno.querySelector('[data-campo="resposta_correta"]').value = altIdx;
    turno.querySelectorAll('[data-campo^="alt-"]').forEach((inp, ai) => {
      inp.style.border = `2px solid ${ai === altIdx ? '#27AE60' : '#ddd'}`;
    });
  },

  _salvarFormulario(idEditar) {
    const titulo = document.getElementById('dial-titulo')?.value.trim();
    if (!titulo) { App.notificar('O título é obrigatório.', 'erro'); return; }

    const turniEls = document.querySelectorAll('.dial-turno-form');
    const turni = [];

    turniEls.forEach((el, i) => {
      const campos = {};
      el.querySelectorAll('[data-campo]').forEach(inp => { campos[inp.dataset.campo] = inp.value.trim(); });
      const tipo = campos['_tipo'];
      const frase = campos['frase'];
      if (!frase) return;

      if (tipo === 'resposta') {
        const alts = [0,1,2,3].map(ai => campos[`alt-${ai}`] || '').filter(Boolean);
        const correto = parseInt(campos['resposta_correta'] || '0');
        turni.push({ id: i+1, personaggio:'Tu', frase, traducao: campos['traducao'] || '', audio_ipa:'', alternativas: alts.length >= 2 ? alts : [frase,'','',''], resposta_correta: correto });
      } else {
        turni.push({ id: i+1, personaggio: campos['personaggio'] || 'Personaggio', frase, traducao: campos['traducao'] || '', audio_ipa: campos['audio_ipa'] || '' });
      }
    });

    if (turni.length < 2) { App.notificar('Adicione pelo menos 2 turnos.', 'erro'); return; }

    const novo = {
      id: idEditar || `custom_dial_${Date.now()}`,
      titulo,
      icone: document.getElementById('dial-icone')?.value.trim() || '💬',
      nivel: document.getElementById('dial-nivel')?.value || 'A1',
      contexto: document.getElementById('dial-contexto')?.value.trim() || '',
      criado_em: Date.now(),
      custom: true,
      turni,
      vocabulario_chave: [],
      xp_recompensa: Math.min(30 + turni.length * 3, 60)
    };

    if (idEditar) {
      const idx = this.custom.findIndex(x => x.id === idEditar);
      if (idx >= 0) this.custom[idx] = novo; else this.custom.push(novo);
    } else {
      this.custom.push(novo);
    }
    this._salvarCustom();
    App.notificar(`💬 "${titulo}" salvo!`, 'sucesso');
    this.renderizarSeletor();
  },

  editarDialogo(id) { this.abrirFormularioCriar(id); },

  excluirDialogo(id) {
    const d = this.custom.find(x => x.id === id);
    if (!d || !confirm(`Excluir "${d.titulo}"?`)) return;
    this.custom = this.custom.filter(x => x.id !== id);
    this._salvarCustom();
    App.notificar('Diálogo excluído.', 'alerta');
    this.renderizarSeletor();
  },

  // ... (manter métodos de jogo existentes: abrirDialogo, checarResposta, mostrarResultado)
};
```

---

### PASSO 3 — Exportar/Importar Conteúdo Custom

**Adicionar ao `js/profilo.js`** (na seção "Gestione Dati" já existente):

```javascript
exportarConteudoCustom() {
  const backup = {
    versao: 1,
    tipo: 'conteudo_custom',
    data: new Date().toISOString(),
    canzoni: JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]'),
    dialoghi: JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]')
  };
  const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `italiano_conteudo_${new Date().toISOString().slice(0,10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
  App.notificar('✅ Conteúdo exportado!', 'sucesso');
},

importarConteudoCustom(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const backup = JSON.parse(e.target.result);
      if (backup.tipo !== 'conteudo_custom') throw new Error('Arquivo inválido');
      if (!confirm(`Importar ${backup.canzoni?.length || 0} músicas e ${backup.dialoghi?.length || 0} diálogos? Conteúdo existente será mantido.`)) return;
      
      // Merge (não sobrescreve — adiciona os que não existem)
      const canExist = JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]');
      const dialExist = JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]');
      
      const canIds = new Set(canExist.map(x => x.id));
      const dialIds = new Set(dialExist.map(x => x.id));
      
      const canNovos = (backup.canzoni || []).filter(x => !canIds.has(x.id));
      const dialNovos = (backup.dialoghi || []).filter(x => !dialIds.has(x.id));
      
      localStorage.setItem('it_canzoni_custom', JSON.stringify([...canExist, ...canNovos]));
      localStorage.setItem('it_dialoghi_custom', JSON.stringify([...dialExist, ...dialNovos]));
      
      App.notificar(`✅ ${canNovos.length} músicas e ${dialNovos.length} diálogos importados!`, 'sucesso');
    } catch(err) {
      App.notificar('❌ Arquivo inválido: ' + err.message, 'erro');
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}
```

**Atualizar HTML do card "Gestione Dati" em `js/profilo.js`:**
```html
<!-- Adicionar abaixo dos botões de backup existentes -->
<div style="border-top:1px solid #f0e8d8;padding-top:0.8rem;margin-top:0.8rem">
  <div style="font-size:0.78rem;font-weight:700;color:#9B2335;margin-bottom:0.5rem">Conteúdo Criado por Mim</div>
  <div style="display:flex;gap:0.5rem;flex-wrap:wrap">
    <button class="btn-secondario" onclick="Profilo.exportarConteudoCustom()" style="font-size:0.82rem">
      ⬇️ Exportar Músicas e Diálogos
    </button>
    <button class="btn-secondario" onclick="document.getElementById('custom-input').click()" style="font-size:0.82rem">
      ⬆️ Importar Conteúdo
    </button>
  </div>
</div>
```

**Adicionar em `index.html`:**
```html
<input type="file" id="custom-input" accept=".json" style="display:none"
  onchange="Profilo.importarConteudoCustom(event)">
```

---

### PASSO 4 — Incluir Custom no Backup Geral

**Atualizar `exportarDados()` em `js/profilo.js`:**
```javascript
// Adicionar ao objeto backup:
canzoni_custom:  JSON.parse(localStorage.getItem('it_canzoni_custom')  || '[]'),
dialoghi_custom: JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]'),
```

**Atualizar `importarDados()` em `js/profilo.js`:**
```javascript
// Adicionar após restaurar progresso e flashcards:
if (backup.canzoni_custom)  localStorage.setItem('it_canzoni_custom',  JSON.stringify(backup.canzoni_custom));
if (backup.dialoghi_custom) localStorage.setItem('it_dialoghi_custom', JSON.stringify(backup.dialoghi_custom));
```

---

## MAPA COMPLETO DE ARQUIVOS

### Arquivos a CRIAR
```
js/canzoni.js         ← Módulo completo (seletor + formulário + jogo)
js/dialoghi.js        ← Módulo completo (seletor + formulário + jogo)
data/canzoni.json     ← Músicas built-in (ver SPEC_METODO_FAMOSOS.md)
data/dialogi.json     ← Diálogos built-in (ver SPEC_METODO_FAMOSOS.md)
```

### Arquivos a MODIFICAR
```
index.html
  ├── Adicionar <section id="sec-canzoni"> com <div id="canzoni-container">
  ├── Adicionar <section id="sec-dialoghi"> com <div id="dialoghi-container">
  ├── Adicionar botão "🎵 Canzoni" no nav top e bottom-nav
  ├── Adicionar botão "💬 Dialoghi" no nav top e bottom-nav
  ├── Adicionar <script src="js/canzoni.js?v=1">
  ├── Adicionar <script src="js/dialoghi.js?v=1">
  ├── Adicionar <input id="custom-input"> para importar conteúdo custom
  └── CSS: .dialogo-card, .dialogo-grid, .can-estrofe-form, .dial-turno-form

js/core.js
  ├── App.navegar(): lazy-render Canzoni e Dialoghi
  └── App.init(): chamar Canzoni.renderizarSeletor() e Dialoghi.renderizarSeletor()

js/profilo.js
  ├── exportarConteudoCustom()
  ├── importarConteudoCustom()
  ├── Atualizar exportarDados() para incluir conteúdo custom
  ├── Atualizar importarDados() para restaurar conteúdo custom
  └── HTML do card "Gestione Dati": adicionar botões de export/import do conteúdo

sw.js
  ├── Versão: italiano-v10 → italiano-v11
  └── STATIC: adicionar './data/canzoni.json', './data/dialogi.json',
              './js/canzoni.js', './js/dialoghi.js'
```

### localStorage (automático — não editar manualmente)
```
it_canzoni_custom     ← Array JSON das músicas criadas pelo usuário
it_dialoghi_custom    ← Array JSON dos diálogos criados pelo usuário
```

---

## FLUXO DO USUÁRIO

```
MÚSICAS:
Home → aba "Canzoni" → Lista (built-in + "Minha" badge)
  ├── [Clicar numa música] → Jogo: preenche lacunas verso por verso → XP
  ├── [➕ Adicionar Música] → Formulário → Salvar → volta à lista
  └── [✏️/🗑️ em card "Minha"] → Editar ou Excluir

DIÁLOGOS:
Home → aba "Dialoghi" → Lista (built-in + "Meu" badge)
  ├── [Clicar num diálogo] → Modo Leitura (todos os turnos + áudio)
  │     └── botão "🎮 Praticar" → Modo Prática (múltipla escolha por turno)
  ├── [➕ Adicionar Diálogo] → Formulário → Salvar → volta à lista
  └── [✏️/🗑️ em card "Meu"] → Editar ou Excluir

BACKUP:
Aba Perfil → Gestione Dati
  ├── "⬇️ Exportar Músicas e Diálogos" → baixa JSON só do conteúdo custom
  ├── "⬆️ Importar Conteúdo" → merge (não sobrescreve) do JSON
  ├── "⬇️ Exportar Backup" (existente) → inclui conteúdo custom também
  └── "⬆️ Importar Backup" (existente) → restaura conteúdo custom também
```

---

## CHECKLIST DE VERIFICAÇÃO

- [ ] Aba "Canzoni" aparece no nav (desktop e mobile)
- [ ] Lista mostra músicas built-in + badge "Minha" nas custom
- [ ] Clicar em música built-in abre jogo de lacunas
- [ ] Botão "➕ Adicionar Música" abre formulário com campos: título, artista, nível, ícone, estrofes
- [ ] Formulário valida: título obrigatório, ao menos 1 estrofe com palavra oculta
- [ ] Salvar música → aparece na lista com badge "Minha" e botões ✏️ 🗑️
- [ ] Editar mantém dados existentes no formulário
- [ ] Excluir pede confirmação e remove da lista
- [ ] Jogo com música custom funciona igual ao built-in
- [ ] Aba "Dialoghi" aparece no nav
- [ ] Lista mostra diálogos built-in + "Meu" badge
- [ ] Formulário de criação: título, ícone, nível, contexto, turnos
- [ ] Adicionar turno "Fala" e turno "Resposta do Tu" com 4 alternativas
- [ ] Marcar alternativa correta muda borda para verde
- [ ] Diálogo salvo aparece com badge e botões de ação
- [ ] Modo Leitura: todos os turnos, botão 🔊 em cada fala
- [ ] Modo Prática: múltipla escolha nos turnos "Tu"
- [ ] Perfil → Gestione Dati: botões de exportar/importar conteúdo custom
- [ ] Export gera JSON com `tipo: 'conteudo_custom'`
- [ ] Import faz merge sem duplicar por ID
- [ ] Backup geral inclui e restaura conteúdo custom
- [ ] `git push origin master && git push origin master:gh-pages --force`
