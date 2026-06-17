const Canzoni = {
  dados: null,        // built-in (data/canzoni.json)
  custom: [],         // criados pelo usuário (localStorage)
  _ocultas: [],       // IDs de nativas ocultadas pelo usuário
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

  // ── Ocultar música nativa (guarda ID no localStorage) ─────
  ocultarNativa(id) {
    const can = (this.dados?.canzoni || []).find(c => c.id === id);
    if (!can) return;
    if (!confirm(`Ocultar "${can.titulo}"?\nEla desaparece da lista mas pode ser restaurada depois.`)) return;
    if (!this._ocultas.includes(id)) this._ocultas.push(id);
    localStorage.setItem('it_canzoni_ocultas', JSON.stringify(this._ocultas));
    App.notificar('Música ocultada. Use "Restaurar" para trazer de volta.', 'alerta');
    this.renderizarSeletor();
  },

  // ── Restaurar todas as nativas ocultas ─────────────────────
  restaurarNativas() {
    if (!this._ocultas.length) return;
    this._ocultas = [];
    localStorage.removeItem('it_canzoni_ocultas');
    App.notificar('Músicas nativas restauradas!', 'sucesso');
    this.renderizarSeletor();
  },

  // ── Renderizar seletor com built-in + custom + botão criar + avaliar ──
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
    if (this._filtroOrigem === 'custom') filtradas = filtradas.filter(s => s.custom || s._custom);
    if (this._filtroOrigem === 'nativo') filtradas = filtradas.filter(s => !s.custom && !s._custom);
    if (this._filtroNivel) filtradas = filtradas.filter(s => s.nivel === this._filtroNivel);
    if (this._filtroTexto) {
      const q = this._filtroTexto.toLowerCase();
      filtradas = filtradas.filter(s => s.titulo.toLowerCase().includes(q) || (s.artista||'').toLowerCase().includes(q));
    }

    // Ordenar: volumes da mesma música ficam juntos em sequência
    filtradas = [...filtradas].sort((a, b) => {
      const getBase = t => t.replace(/\s*\(Vol\.\s*\d+\)\s*$/i, '').trim();
      const getVol  = t => { const m = t.match(/\(Vol\.\s*(\d+)\)/i); return m ? parseInt(m[1]) : 0; };
      const baseA = getBase(a.titulo), baseB = getBase(b.titulo);
      if (baseA !== baseB) return baseA.localeCompare(baseB, 'it');
      return getVol(a.titulo) - getVol(b.titulo);
    });

    const nC=todas.filter(s=>s.custom||s._custom).length, nN=todas.length-nC, _o=this._filtroOrigem;
    const nOcultas = this._ocultas.length;
    const _oPill=(v,l,ct)=>`<button onclick="Canzoni._filtroOrigem='${v}';Canzoni.renderizarSeletor()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid ${_o===v?'#7B68A0':'#ddd'};background:${_o===v?'#7B68A0':'transparent'};color:${_o===v?'#fff':'inherit'};cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap">${l} (${ct})</button>`;

    let html = `
      <!-- Linha 1: busca + ações -->
      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem">
        <input type="search" placeholder="🔍 Titolo o artista..." value="${this._filtroTexto}"
          oninput="Canzoni._filtroTexto=this.value;Canzoni.renderizarSeletor()"
          style="flex:1;min-width:0;padding:0.44rem 0.75rem;border:1.5px solid #ddd;border-radius:20px;font-size:0.875rem;font-family:inherit">
        <button class="btn-pill-add" onclick="Canzoni.abrirFormularioCriar()" style="white-space:nowrap">${I18n.t('can_btn_adicionar')}</button>
        <button class="btn-ia-add" onclick="IAImport.abrir('canzone')" style="white-space:nowrap">🤖 via IA</button>
      </div>
      <!-- Linha 2: filtros numa só linha -->
      <div style="display:flex;gap:0.35rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
        ${_oPill('','Todas',todas.length)}
        ${nC?_oPill('custom','🤖 Adicionadas',nC):''}
        ${nN?_oPill('nativo','📚 Nativas',nN):''}
        <select class="nivel-select${this._filtroNivel?' ativo':''}"
          onchange="Canzoni._filtroNivel=this.value;Canzoni.renderizarSeletor()">
          <option value="">🎯 Nível</option>
          ${niveis.filter(n=>counts[n]).map(n=>`<option value="${n}" ${this._filtroNivel===n?'selected':''}>${n} (${counts[n]})</option>`).join('')}
        </select>
        ${nOcultas ? `<button onclick="Canzoni.restaurarNativas()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid #c9952a;background:rgba(201,149,42,0.1);color:#7a5a00;cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap;font-family:inherit">↩ Restaurar (${nOcultas})</button>` : ''}
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
          <button onclick="event.stopPropagation();Canzoni.excluirCanzone('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;" title="Excluir">🗑️</button>`
          : `<button onclick="event.stopPropagation();Canzoni.ocultarNativa('${can.id}')" style="background:none;border:none;cursor:pointer;font-size:0.85rem;opacity:0.4;transition:opacity 0.15s" onmouseenter="this.style.opacity=1" onmouseleave="this.style.opacity=0.4" title="Ocultar esta música">🗑️</button>`}
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
    const audioKey = existente?.audio_store_key || '';
    const estrofes = existente?.estrofes?.map(e => ({ ...e, tempo: e.inicio_ms != null ? (e.inicio_ms / 1000) : '' }))
      || [{ id: 1, texto_completo: '', texto_lacuna: '', palavra_oculta: '', traducao: '', dica: '', tempo: '' }];

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

        <div style="background:#f0f4fa;border:1px solid #c8d6ea;border-radius:10px;padding:0.9rem;margin-bottom:1rem">
          <div style="font-size:0.85rem;font-weight:700;color:#003E8A;margin-bottom:0.6rem">🎵 Áudio da música (opcional)</div>
          <input type="hidden" id="can-audio-key" value="${audioKey}">
          <input type="file" id="can-audio-file" accept="audio/*" onchange="Canzoni._onAudioSelecionado(event)" style="font-size:0.85rem">
          <audio id="can-audio-preview" controls style="width:100%;margin-top:0.6rem;display:${audioKey ? 'block' : 'none'}"></audio>
          <button id="can-btn-remover-audio" class="btn-secondario" onclick="Canzoni._removerAudio()"
            style="margin-top:0.5rem;font-size:0.8rem;display:${audioKey ? 'inline-block' : 'none'}">🗑️ Remover áudio</button>
        </div>

        <div style="background:#f9f6f0;border:1px solid #ede5d5;border-radius:10px;padding:0.9rem;margin-bottom:1rem">
          <div style="font-size:0.85rem;font-weight:700;color:#9B2335;margin-bottom:0.6rem">🤖 Criar exercícios com IA</div>
          <div style="font-size:0.75rem;color:#8a7a60;margin-bottom:0.5rem">Cole uma transcrição com tempos (formato LRC ou tabela do YouTube), clique em <strong>Criar Prompt IA</strong>, copie o prompt para o ChatGPT / Claude, depois cole o resultado aqui para importar todos os versos automaticamente.</div>
          <textarea id="can-lrc-paste" class="ia-paste-area" rows="5" style="width:100%;font-family:monospace;font-size:0.82rem"
            placeholder="[00:12.34] Bella ciao, bella ciao
[00:16.80] Bella ciao ciao ciao"></textarea>
          <div style="margin-top:0.5rem">
            <button class="btn-secondario" onclick="Canzoni._construirPromptIA()">🤖 Criar Prompt IA (com exercícios)</button>
          </div>

          <div id="can-ia-bloco" style="display:block;margin-top:0.8rem">
            <p style="font-size:0.78rem;color:#8a7a60;margin-bottom:0.4rem">1. Copie o prompt abaixo e cole no seu AI favorito (ChatGPT, Claude, etc.):</p>
            <div class="ia-prompt-box">
              <pre id="can-ia-prompt-text"></pre>
              <button class="ia-copy-btn" onclick="Canzoni._copiarPromptIA()">📋 Copiar Prompt</button>
            </div>
            <p style="font-size:0.78rem;color:#8a7a60;margin:0.6rem 0 0.4rem">2. Cole aqui o JSON gerado pelo AI:</p>
            <textarea id="can-ia-resultado" class="ia-paste-area" rows="5" placeholder="Cole aqui o JSON gerado pelo AI..."></textarea>
            <button class="btn-primario" onclick="Canzoni._importarResultadoIA()" style="margin-top:0.5rem">✅ Importar Resultado</button>
          </div>
        </div>

        <div style="font-size:0.85rem;font-weight:700;color:#9B2335;margin-bottom:0.8rem;border-top:1px solid #f0e8d8;padding-top:1rem">
          📝 Estrofes (versos com lacunas)
        </div>

        <div style="max-height:420px;overflow-y:auto;padding-right:4px;margin-bottom:0.8rem">
          <div id="can-estrofes">${estrofesHtml}</div>
        </div>

        <button onclick="Canzoni._adicionarEstrofe()" class="btn-secondario" style="width:100%;margin:0 0 0.8rem">
          ➕ Adicionar verso
        </button>

        <div style="background:#FFF8E7;border:1px solid #D4A843;border-radius:8px;padding:0.8rem;margin-bottom:0.5rem;font-size:0.82rem;color:#6B4C1A">
          💡 <strong>Como criar a lacuna:</strong> Escreva o texto completo no campo "Texto completo".
          No "Texto com lacuna", substitua a palavra que quer ocultar por <code>___</code> (três underscores).
          Informe a palavra oculta no campo "Palavra oculta".
        </div>

        <div style="position:sticky;bottom:0;background:#fff;padding:0.75rem 0 0.25rem;border-top:1px solid #f0e8d8;z-index:10;margin-top:0.25rem">
          <div style="display:flex;gap:0.5rem">
            <button class="btn-primario" style="flex:1" onclick="Canzoni._salvarFormulario('${idEditar || ''}')">
              💾 Salvar Música
            </button>
            <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">Cancelar</button>
          </div>
        </div>
      </div>`;

    if (audioKey) {
      AudioStore.obterURL(audioKey).then(url => {
        const audioEl = document.getElementById('can-audio-preview');
        if (audioEl && url) audioEl.src = url;
      });
    }
  },

  // ── Áudio sincronizado (formulário) ────────────────────────
  async _onAudioSelecionado(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const keyInput = document.getElementById('can-audio-key');
    const key = keyInput?.value || `audio_${Date.now()}`;
    try {
      await AudioStore.salvar(key, file);
      if (keyInput) keyInput.value = key;
      const url = await AudioStore.obterURL(key);
      const audioEl = document.getElementById('can-audio-preview');
      if (audioEl) { audioEl.src = url; audioEl.style.display = 'block'; }
      const btnRemover = document.getElementById('can-btn-remover-audio');
      if (btnRemover) btnRemover.style.display = 'inline-block';
    } catch (e) {
      App.notificar('Erro ao salvar arquivo de áudio', 'erro');
    }
  },

  async _removerAudio() {
    const keyInput = document.getElementById('can-audio-key');
    const key = keyInput?.value;
    if (key) { try { await AudioStore.remover(key); } catch (e) {} }
    if (keyInput) keyInput.value = '';
    const audioEl = document.getElementById('can-audio-preview');
    if (audioEl) { audioEl.removeAttribute('src'); audioEl.style.display = 'none'; }
    const fileInput = document.getElementById('can-audio-file');
    if (fileInput) fileInput.value = '';
    const btnRemover = document.getElementById('can-btn-remover-audio');
    if (btnRemover) btnRemover.style.display = 'none';
  },

  _marcarTempoAgora(i) {
    const audioEl = document.getElementById('can-audio-preview');
    if (!audioEl || !audioEl.src) { App.notificar('Carregue um arquivo de áudio primeiro', 'alerta'); return; }
    const tempoInput = document.querySelector(`#can-est-${i} [data-campo="tempo"]`);
    if (tempoInput) tempoInput.value = audioEl.currentTime.toFixed(2);
  },

  _parseLRC(texto) {
    const re = /^\[(\d+):(\d+(?:\.\d+)?)\](.*)$/;
    return texto.split('\n').reduce((acc, linha) => {
      const m = linha.trim().match(re);
      if (!m) return acc;
      const textoCompleto = m[3].trim();
      if (!textoCompleto) return acc;
      acc.push({ tempo: parseInt(m[1], 10) * 60 + parseFloat(m[2]), texto_completo: textoCompleto });
      return acc;
    }, []);
  },

  // Aceita "12s", "1:01" (m:ss) ou "1:02:03" (h:mm:ss) → segundos
  _parseTempoGenerico(str) {
    str = (str || '').trim();
    const seg = str.match(/^(\d+)\s*s$/i);
    if (seg) return parseInt(seg[1], 10);
    if (!/^\d+(:\d+){1,2}$/.test(str)) return null;
    const partes = str.split(':').map(p => parseInt(p, 10));
    if (partes.some(isNaN)) return null;
    if (partes.length === 2) return partes[0] * 60 + partes[1];
    return partes[0] * 3600 + partes[1] * 60 + partes[2];
  },

  // Tabela colada de sites de transcrição/legenda (Time | Subtitle | Tradução), separada por TAB
  // ou por 2+ espaços quando o TAB não sobrevive à colagem.
  _parseTabelaTranscricao(texto) {
    return texto.split('\n').reduce((acc, linha) => {
      if (!linha.trim()) return acc;
      const cols = linha.includes('\t') ? linha.split('\t') : linha.split(/ {2,}/);
      if (cols.length < 2) return acc;
      const tempo = this._parseTempoGenerico(cols[0]);
      if (tempo == null) return acc;
      const textoCompleto = (cols[1] || '').replace(/♪/g, '').trim();
      if (!textoCompleto) return acc;
      const traducao = (cols[2] || '').replace(/♪/g, '').trim();
      acc.push({ tempo, texto_completo: textoCompleto, traducao });
      return acc;
    }, []);
  },

  // ── Prompt de IA: padroniza tempo + letra + tradução + cria as lacunas, tudo de uma vez ──
  _construirPromptIA() {
    const textarea = document.getElementById('can-lrc-paste');
    const textoColado = (textarea?.value || '').trim();

    const titulo = document.getElementById('can-titulo')?.value.trim() || '';
    const artista = document.getElementById('can-artista')?.value.trim() || '';
    const nivel   = document.getElementById('can-nivel')?.value || 'A2';
    const icone   = document.getElementById('can-icone')?.value.trim() || '🎵';

    const prompt = `Você está ajudando a criar um exercício de listening sincronizado com lacunas para um app de aprendizado de italiano, a partir de uma transcrição temporizada de música.

Vou colar uma transcrição temporizada abaixo. Pode estar no formato LRC ("[mm:ss.xx] texto"), ou numa tabela com colunas Tempo / Legenda / Tradução (ex: copiado de site de transcrição do YouTube), com tempos como "12s", "1:01" ou "1:02:03".

Retorne um único objeto JSON (não um array) com esta estrutura exata:
{
  "titulo": "${titulo || 'PREENCHA O TÍTULO DA MÚSICA'}",
  "artista": "${artista || 'PREENCHA O NOME DO ARTISTA'}",
  "nivel": "${nivel}",
  "icone": "${icone}",
  "estrofes": [
    {
      "tempo": <número — tempo de início da linha em SEGUNDOS, como decimal, ex: "1:02" -> 62, "0:12.5" -> 12.5>,
      "texto_completo": "<o texto da linha, sem símbolos ♪>",
      "traducao": "<tradução em português da linha — use a que estiver na transcrição se houver, senão traduza você mesmo>",
      "palavra_oculta": "<uma palavra pedagogicamente útil desta linha, ou \\"\\" se esta linha não tiver lacuna>",
      "texto_lacuna": "<a mesma linha com essa palavra substituída por \\"___\\", ou \\"\\" se não tiver lacuna>",
      "dica": "<dica curta: classe gramatical + significado breve, ou \\"\\" se não tiver lacuna>"
    }
  ]
}

REGRAS OBRIGATÓRIAS:
1. Mantenha as linhas na mesma ordem da transcrição original. Não pule nenhuma linha.
2. Converta todos os timestamps para segundos decimais.
3. Para aproximadamente 30%–50% das linhas com conteúdo cantado real (pule ruídos de multidão, efeitos sonoros entre parênteses ou ad-libs repetidos), preencha "palavra_oculta", "texto_lacuna" e "dica" como descrito acima. Escolha vocabulário útil em italiano, não artigos como "il"/"la" ou pronomes.
4. Para todas as outras linhas, deixe "palavra_oculta", "texto_lacuna" e "dica" como strings vazias "".
5. Retorne APENAS o objeto JSON, sem texto antes ou depois.

TRANSCRIÇÃO:
${textoColado || '[COLE SUA TRANSCRIÇÃO TEMPORIZADA AQUI ANTES DE ENVIAR ESTE PROMPT]'}`;

    const pre = document.getElementById('can-ia-prompt-text');
    if (pre) pre.textContent = prompt;
    pre?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  },

  _copiarPromptIA() {
    const txt = document.getElementById('can-ia-prompt-text')?.textContent || '';
    const setCopiado = () => {
      const btn = document.querySelector('#can-ia-bloco .ia-copy-btn');
      if (!btn) return;
      const orig = btn.textContent;
      btn.textContent = '✅ Copiado!';
      setTimeout(() => { btn.textContent = orig; }, 2000);
    };
    navigator.clipboard.writeText(txt).then(setCopiado).catch(() => {
      const ta = document.createElement('textarea');
      ta.value = txt;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      setCopiado();
    });
  },

  _importarResultadoIA() {
    const raw = document.getElementById('can-ia-resultado')?.value.trim() || '';
    if (!raw) { App.notificar('Cole o JSON gerado pelo AI primeiro', 'alerta'); return; }

    let dados;
    try {
      const match = raw.match(/(\{[\s\S]*\}|\[[\s\S]*\])/);
      if (!match) throw new Error('No JSON found');
      dados = JSON.parse(match[1]);
      // Novo formato: wrapper com { titulo, artista, nivel, icone, estrofes }
      if (!Array.isArray(dados) && Array.isArray(dados.estrofes)) {
        if (dados.titulo) { const el = document.getElementById('can-titulo'); if (el && !el.value.trim()) el.value = dados.titulo; }
        if (dados.artista) { const el = document.getElementById('can-artista'); if (el && !el.value.trim()) el.value = dados.artista; }
        if (dados.nivel) { const el = document.getElementById('can-nivel'); if (el) el.value = dados.nivel; }
        if (dados.icone) { const el = document.getElementById('can-icone'); if (el && !el.value.trim()) el.value = dados.icone; }
        dados = dados.estrofes;
      }
      if (!Array.isArray(dados)) dados = [dados];
    } catch (e) {
      App.notificar('JSON inválido. Verifique a resposta do AI e tente novamente.', 'erro');
      return;
    }

    const validos = dados.filter(d => d && typeof d.texto_completo === 'string' && d.texto_completo.trim());
    if (validos.length === 0) { App.notificar('Nenhum verso válido encontrado no JSON', 'erro'); return; }

    const container = document.getElementById('can-estrofes');
    if (!container) return;
    const existentes = container.querySelectorAll('.can-estrofe-form').length;
    if (existentes > 0 && !confirm(`Isso vai substituir ${existentes} verso(s) existente(s) por ${validos.length} versos importados. Continuar?`)) return;
    container.innerHTML = '';
    validos.forEach((l, i) => {
      const div = document.createElement('div');
      div.innerHTML = this._htmlEstrofeForm({
        id: i + 1,
        texto_completo: l.texto_completo,
        texto_lacuna: l.texto_lacuna || '',
        palavra_oculta: l.palavra_oculta || '',
        traducao: l.traducao || '',
        dica: l.dica || '',
        tempo: l.tempo ?? ''
      }, i);
      container.appendChild(div.firstElementChild);
    });
    App.notificar(`${validos.length} versos importados do resultado do AI`, 'sucesso');
  },

  _htmlEstrofeForm(est, i) {
    return `
      <div class="can-estrofe-form" id="can-est-${i}" style="background:#f9f6f0;border-radius:10px;padding:0.9rem;margin-bottom:0.8rem;border:1px solid #ede5d5">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem">
          <span style="font-weight:700;font-size:0.82rem;color:#9B2335">Verso ${i + 1}</span>
          <button class="can-btn-remover-verso" onclick="Canzoni._removerEstrofe(${i})" style="background:none;border:none;cursor:pointer;color:#C0392B;font-size:0.85rem">🗑️ Remover</button>
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
          <div style="display:flex;gap:0.5rem;align-items:center">
            <input type="number" step="0.1" min="0" placeholder="Tempo (s)" data-campo="tempo" data-idx="${i}"
              value="${est.tempo ?? ''}"
              style="padding:0.45rem 0.6rem;border:2px solid #ddd;border-radius:7px;font-size:0.88rem;width:7rem">
            <button class="can-btn-marcar-tempo" onclick="Canzoni._marcarTempoAgora(${i})"
              style="background:none;border:1px solid #9B2335;color:#9B2335;border-radius:7px;padding:0.4rem 0.6rem;cursor:pointer;font-size:0.78rem;white-space:nowrap">🎙️ Marcar agora</button>
          </div>
        </div>
      </div>`;
  },

  _adicionarEstrofe() {
    const container = document.getElementById('can-estrofes');
    if (!container) return;
    const i = container.querySelectorAll('.can-estrofe-form').length;
    const div = document.createElement('div');
    div.innerHTML = this._htmlEstrofeForm({ id: i+1, texto_completo:'', texto_lacuna:'', palavra_oculta:'', traducao:'', dica:'', tempo:'' }, i);
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
      const btnRemover = el.querySelector('.can-btn-remover-verso');
      if (btnRemover) btnRemover.setAttribute('onclick', `Canzoni._removerEstrofe(${idx})`);
      const btnMarcar = el.querySelector('.can-btn-marcar-tempo');
      if (btnMarcar) btnMarcar.setAttribute('onclick', `Canzoni._marcarTempoAgora(${idx})`);
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
      if (!campos.texto_completo) return;
      // Auto-gerar texto_lacuna se não preenchido
      if (!campos.texto_lacuna && campos.palavra_oculta) {
        const reEscape = campos.palavra_oculta.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        campos.texto_lacuna = campos.texto_completo.replace(new RegExp(reEscape, 'i'), '___');
      }
      const est = {
        id: i + 1,
        texto_completo: campos.texto_completo,
        texto_lacuna: campos.texto_lacuna || '',
        palavra_oculta: campos.palavra_oculta || '',
        traducao: campos.traducao || '',
        dica: campos.dica || ''
      };
      const tempo = campos.tempo !== '' && campos.tempo != null ? parseFloat(campos.tempo) : NaN;
      if (!isNaN(tempo)) est.inicio_ms = Math.round(tempo * 1000);
      estrofes.push(est);
    });
    if (estrofes.length === 0) { App.notificar('notif_can_sem_verso', 'erro'); return; }

    const audioKey = document.getElementById('can-audio-key')?.value || '';

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
    if (audioKey) nova.audio_store_key = audioKey;

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
  erros: 0,
  respostas: [],
  traduzirVisivel: false,

  async abrirCanzone(id) {
    await this.carregar();
    this.canzonAtual = this.todasCanzoni().find(c => c.id === id);
    if (!this.canzonAtual) return;
    this.estrofeAtual = 0;
    this.acertos = 0;
    this.erros = 0;
    this.respostas = this.canzonAtual.estrofes.map(() => null);
    this.traduzirVisivel = false;
    this._audioResumeTime = null;
    this._audioShouldPlay = false;
    this._distratorCache = {};
    this._syncGen = (this._syncGen || 0) + 1;
    this._avancarProximoBlank();
  },

  _repetirVerso(inicioMs, fimMs) {
    const audioEl = document.getElementById('can-audio-player');
    if (!audioEl || inicioMs == null) return;
    if (this._repeatListener) {
      audioEl.removeEventListener('timeupdate', this._repeatListener);
      this._repeatListener = null;
    }
    audioEl.currentTime = inicioMs / 1000;
    audioEl.play();
    if (fimMs != null) {
      const parar = () => {
        if (audioEl.currentTime * 1000 >= fimMs) {
          audioEl.pause();
          audioEl.removeEventListener('timeupdate', parar);
          this._repeatListener = null;
        }
      };
      this._repeatListener = parar;
      audioEl.addEventListener('timeupdate', parar);
    }
  },

  _avancarProximoBlank() {
    const can = this.canzonAtual;
    if (!can) return;
    // Músicas sem nenhuma lacuna (ex.: só áudio sincronizado, sem exercício) ficam em modo "ouvir letra",
    // sem pular automaticamente pra tela de resultado.
    const temLacunas = can.estrofes.some(e => e.palavra_oculta);
    while (this.estrofeAtual < can.estrofes.length && !can.estrofes[this.estrofeAtual].palavra_oculta) {
      this.estrofeAtual++;
    }
    if (this.estrofeAtual >= can.estrofes.length) {
      this._renderizarPlayer();
      if (temLacunas) setTimeout(() => this.mostrarResultado(), 700);
    } else {
      this._renderizarPlayer();
    }
  },

  _getDistrator(est) {
    const can = this.canzonAtual;
    const outras = can.estrofes
      .filter(e => e.palavra_oculta && e.palavra_oculta.toLowerCase() !== est.palavra_oculta.toLowerCase())
      .map(e => e.palavra_oculta);
    if (outras.length > 0) return outras[Math.floor(Math.random() * outras.length)];
    const fb = ['sempre','bene','grande','bella','notte','cuore','sole','vita','tempo','lungo'];
    const filtrado = fb.filter(w => w.toLowerCase() !== est.palavra_oculta.toLowerCase());
    return filtrado[Math.floor(Math.random() * filtrado.length)] || '???';
  },

  _esc(str) {
    return String(str||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  },

  _renderizarPlayer() {
    const c = document.getElementById('canzoni-container');
    if (!c || !this.canzonAtual) return;
    const can = this.canzonAtual;

    const total = can.estrofes.filter(e => e.palavra_oculta).length;
    const done  = can.estrofes.filter((e, i) => e.palavra_oculta && this.respostas[i] !== null).length;
    const pct   = total > 0 ? Math.round(done / total * 100) : 0;

    const versosHtml = can.estrofes.map((v, i) => {
      const resp = this.respostas[i];
      let cls;
      if (i < this.estrofeAtual) {
        if (!v.palavra_oculta)  cls = 'past-ok';
        else if (resp && resp.correto) cls = 'past-correct';
        else if (resp)          cls = 'past-wrong';
        else                    cls = 'past-ok';
      } else if (i === this.estrofeAtual) {
        cls = 'active';
      } else {
        cls = 'future';
      }

      let lineHtml;
      if (!v.palavra_oculta || !v.texto_lacuna) {
        lineHtml = '<span class="can-verse-line">' + this._esc(v.texto_completo||'') + '</span>';
      } else {
        let blankHtml;
        if (cls === 'future' || cls === 'active') {
          blankHtml = '<span class="can-blank">_____</span>';
        } else if (resp && resp.correto) {
          blankHtml = '<span class="can-blank can-blank-correct">' + this._esc(v.palavra_oculta) + '</span>';
        } else if (resp) {
          blankHtml = '<span class="can-blank can-blank-wrong">' + this._esc(resp.escolha) + '</span>'
                    + '<span class="can-blank can-blank-revealed"> ' + this._esc(v.palavra_oculta) + '</span>';
        } else {
          blankHtml = '<span class="can-blank">' + this._esc(v.palavra_oculta) + '</span>';
        }
        const pts = (v.texto_lacuna||'').split('___');
        lineHtml = '<span class="can-verse-line">' + this._esc(pts[0]) + blankHtml + this._esc(pts[1]||'') + '</span>';
      }

      const tradHtml = (this.traduzirVisivel && v.traducao)
        ? '<div class="can-verse-trad">' + this._esc(v.traducao) + '</div>' : '';

      const proximoMs = can.estrofes.slice(i + 1).find(e => e.inicio_ms != null)?.inicio_ms;
      const repeatHtml = (cls !== 'future' && v.inicio_ms != null && can.audio_store_key)
        ? '<button class="can-repeat-btn" onclick="Canzoni._repetirVerso(' + v.inicio_ms + ',' + (proximoMs ?? 'undefined') + ')">&#9654; repetir</button>'
        : (cls !== 'future' && !can.audio_store_key
          ? '<button class="can-repeat-btn" onclick="App.pronunciar(\'' + (v.texto_completo||'').replace(/\\/g,'\\\\').replace(/'/g,"\\'") + '\')">&#9654; repetir</button>'
          : '');

      const temposAttr = (v.inicio_ms != null) ? ' data-tempo-ms="' + v.inicio_ms + '"' : '';
      return '<div class="can-verse can-verse-' + cls + '"' + temposAttr + '>' + lineHtml + tradHtml + repeatHtml + '</div>';
    }).join('');

    let choicesHtml = '';
    const est = can.estrofes[this.estrofeAtual];
    if (est && est.palavra_oculta) {
      const idx = this.estrofeAtual;
      if (!this._distratorCache) this._distratorCache = {};
      if (!this._distratorCache[idx]) {
        this._distratorCache[idx] = { dist: this._getDistrator(est), ordem: Math.random() > 0.5 };
      }
      const { dist, ordem } = this._distratorCache[idx];
      const arr = ordem ? [est.palavra_oculta, dist] : [dist, est.palavra_oculta];
      const btns = arr.map(w => {
        const safeW = w.replace(/\\/g,'\\\\').replace(/'/g,"\\'");
        return '<button class="can-choice-btn" onclick="Canzoni._escolher(\'' + safeW + '\')"><i>' + this._esc(w) + '</i></button>';
      }).join('');
      choicesHtml = '<div class="can-choices-bar"><div class="can-choices-label">Scegli la parola</div><div class="can-choices-grid">' + btns + '</div></div>';
    }

    const audioBarHtml = can.audio_store_key
      ? '<div class="can-audio-bar"><audio id="can-audio-player" controls></audio></div>'
      : '';

    c.innerHTML =
      '<div class="can-player">' +
        '<div class="can-player-header">' +
          '<button class="can-back-btn" onclick="Canzoni.renderizarSeletor()">&#8249;</button>' +
          '<div class="can-header-song">' +
            '<div class="can-header-title">' + this._esc(can.titulo) + '</div>' +
            '<div class="can-header-artist">' + this._esc(can.artista||'') + '</div>' +
          '</div>' +
          '<div class="can-score-row">' +
            '<span class="can-score-pill can-score-correct">' + this.acertos + ' ✓</span>' +
            '<span class="can-score-pill can-score-wrong">' + this.erros + ' ✗</span>' +
          '</div>' +
        '</div>' +
        audioBarHtml +
        '<div class="can-subbar">' +
          '<div class="can-progress-wrap"><div class="can-progress-fill" style="width:' + pct + '%"></div></div>' +
          '<div class="can-toggle-row">' +
            '<span class="can-toggle-label">tradução</span>' +
            '<button class="can-toggle-btn ' + (this.traduzirVisivel?'on':'off') + '" onclick="Canzoni._toggleTraduzir()" aria-label="alternar tradução"></button>' +
          '</div>' +
        '</div>' +
        '<div class="can-lyrics-area" id="can-lyrics">' + versosHtml + '</div>' +
        choicesHtml +
      '</div>';

    setTimeout(() => {
      const el = document.querySelector('.can-verse-active');
      if (el) el.scrollIntoView({ behavior:'instant', block:'center' });
    }, 0);

    if (can.audio_store_key) this._iniciarSyncAudio(can);
  },

  // ── Reprodução de áudio sincronizado com a letra ──────────
  async _iniciarSyncAudio(can) {
    const gen = this._syncGen;
    let url;
    try { url = await AudioStore.obterURL(can.audio_store_key); } catch (e) { return; }
    if (!url || gen !== this._syncGen) return;
    const audioEl = document.getElementById('can-audio-player');
    if (!audioEl) return;

    // Preserva a posição de reprodução entre re-renders
    if (this._audioResumeTime != null) {
      const tempoRetomar = this._audioResumeTime;
      const deveTocar = this._audioShouldPlay;
      this._audioResumeTime = null;
      this._audioShouldPlay = false;
      const onMeta = () => {
        audioEl.currentTime = tempoRetomar;
        if (deveTocar) audioEl.play();
      };
      audioEl.addEventListener('loadedmetadata', onMeta, { once: true });
      audioEl.src = url;
      if (audioEl.readyState >= 1) {
        audioEl.removeEventListener('loadedmetadata', onMeta);
        onMeta();
      }
    } else {
      audioEl.src = url;
    }

    const verseEls = Array.from(document.querySelectorAll('#can-lyrics .can-verse[data-tempo-ms]'))
      .sort((a, b) => parseInt(a.dataset.tempoMs, 10) - parseInt(b.dataset.tempoMs, 10));

    verseEls.forEach(el => {
      el.style.cursor = 'pointer';
      el.addEventListener('click', () => {
        const ms = parseInt(el.dataset.tempoMs, 10);
        if (isNaN(ms)) return;
        audioEl.currentTime = ms / 1000;
        audioEl.play();
      });
    });

    let pausadoParaLacuna = false;

    audioEl.addEventListener('timeupdate', () => {
      const curMs = audioEl.currentTime * 1000;
      let activeEl = null;
      for (let i = 0; i < verseEls.length; i++) {
        const startMs = parseInt(verseEls[i].dataset.tempoMs, 10);
        const nextMs = (i + 1 < verseEls.length) ? parseInt(verseEls[i + 1].dataset.tempoMs, 10) : Infinity;
        if (curMs >= startMs && curMs < nextMs) { activeEl = verseEls[i]; break; }
      }
      verseEls.forEach(el => el.classList.toggle('can-verse-playing', el === activeEl));
      if (activeEl) activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });

      // Pausa automaticamente ao alcançar uma lacuna ainda não respondida
      const idxAtual = this.estrofeAtual;
      const estrofeAtualObj = can.estrofes[idxAtual];
      if (
        !pausadoParaLacuna &&
        estrofeAtualObj && estrofeAtualObj.palavra_oculta &&
        this.respostas[idxAtual] == null &&
        estrofeAtualObj.inicio_ms != null &&
        curMs >= estrofeAtualObj.inicio_ms
      ) {
        pausadoParaLacuna = true;
        audioEl.pause();
      }
    });
  },

  _escolher(palavra) {
    const can = this.canzonAtual;
    if (!can || this.estrofeAtual >= can.estrofes.length) return;
    const est = can.estrofes[this.estrofeAtual];
    if (!est.palavra_oculta) return;
    document.querySelectorAll('.can-choice-btn').forEach(b => { b.disabled = true; b.style.pointerEvents = 'none'; });
    const norm = s => s.toLowerCase().trim().normalize('NFD').replace(/[̀-ͯ]/g,'');
    const correto = norm(palavra) === norm(est.palavra_oculta);
    this.respostas[this.estrofeAtual] = { escolha: palavra, correto };
    if (correto) {
      this.acertos++;
      if (typeof App !== 'undefined' && App.ganharXP) App.ganharXP(5);
    } else {
      this.erros++;
    }
    this.estrofeAtual++;

    // Se a música tem áudio sincronizado, retoma a reprodução de onde pausou
    const audioEl = document.getElementById('can-audio-player');
    if (audioEl) {
      this._audioResumeTime = audioEl.currentTime;
      this._audioShouldPlay = true;
    }

    setTimeout(() => this._avancarProximoBlank(), 200);
  },

  _toggleTraduzir() {
    this.traduzirVisivel = !this.traduzirVisivel;
    const audioEl = document.getElementById('can-audio-player');
    if (audioEl) {
      this._audioResumeTime = audioEl.currentTime;
      this._audioShouldPlay = !audioEl.paused;
    }
    this._renderizarPlayer();
  },

  verificar() {},
  renderizarEstrofe() { this._renderizarPlayer(); },

  mostrarResultado() {
    const can = this.canzonAtual;
    const total = can.estrofes.filter(e => e.palavra_oculta).length;
    const pct = total > 0 ? Math.round(this.acertos / total * 100) : 100;
    const xpGanho = Math.round(can.xp_recompensa * pct / 100);
    if (xpGanho > 0 && typeof Progressao !== 'undefined' && Progressao.ganhar) Progressao.ganhar(xpGanho);
    const c = document.getElementById('canzoni-container');
    const emoji = pct >= 80 ? '🎤' : pct >= 50 ? '🎵' : '🎼';
    c.innerHTML =
      '<div class="can-player">' +
        '<div class="can-result">' +
          '<div class="can-result-emoji">' + emoji + '</div>' +
          '<div class="can-result-title">' + this._esc(can.titulo) + '</div>' +
          '<div class="can-result-score">' + this.acertos + '<span>/' + total + '</span></div>' +
          '<div class="can-result-xp">+' + xpGanho + ' XP</div>' +
          '<div style="display:flex;gap:0.5rem;justify-content:center;margin-top:1.2rem;flex-wrap:wrap">' +
            '<button class="can-restart-btn" onclick="Canzoni.abrirCanzone(\'' + can.id + '\')">&#8635; Tentar novamente</button>' +
            '<button class="can-restart-btn secundario" onclick="Canzoni.renderizarSeletor()">&#8592; Músicas</button>' +
          '</div>' +
        '</div>' +
      '</div>';
  }
};

document.addEventListener('i18n:changed', () => {
  if (document.getElementById('canzoni-container')) Canzoni.renderizarSeletor();
});
