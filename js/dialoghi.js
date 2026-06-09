const Dialoghi = {
  dados: null,
  custom: [],
  dialogoAtual: null,
  turnoAtual: 0,
  modo: 'leitura', // 'leitura' | 'pratica'
  acertos: 0,
  
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

  _filtroOrigem: '', // '' | 'custom' | 'nativo'

  todosDialoghi() {
    // Custom primeiro
    return [...this.custom, ...(this.dados?.dialogi || [])];
  },

  _salvarCustom() {
    localStorage.setItem('it_dialoghi_custom', JSON.stringify(this.custom));
  },
  
  _filtroNivel: '',
  _filtroTexto: '',

  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('dialoghi-container');
    if (!c) return;

    const todos = this.todosDialoghi();
    const niveis = ['A1','A2','B1','B2','C1'];

    // Conta por nível
    const counts = {};
    todos.forEach(d => { counts[d.nivel] = (counts[d.nivel]||0)+1; });

    // Filtros
    let filtrados = todos;
    if (this._filtroOrigem === 'custom')  filtrados = filtrados.filter(d => d.custom || d._custom);
    if (this._filtroOrigem === 'nativo')  filtrados = filtrados.filter(d => !d.custom && !d._custom);
    if (this._filtroNivel) filtrados = filtrados.filter(d => d.nivel === this._filtroNivel);
    if (this._filtroTexto) {
      const q = this._filtroTexto.toLowerCase();
      filtrados = filtrados.filter(d => d.titulo.toLowerCase().includes(q));
    }

    const nCustom = todos.filter(d => d.custom || d._custom).length;
    const nNativo = todos.length - nCustom;
    const _o = this._filtroOrigem;
    const _origemPill = (val, label, count) =>
      `<button onclick="Dialoghi._filtroOrigem='${val}';Dialoghi.renderizarSeletor()"
        style="padding:0.22rem 0.7rem;border-radius:999px;border:1.5px solid ${_o===val?'#7B68A0':'#ddd'};background:${_o===val?'#7B68A0':'transparent'};color:${_o===val?'#fff':'inherit'};cursor:pointer;font-size:0.75rem;font-weight:600">
        ${label} (${count})</button>`;

    let html = `
      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem">
        <input type="search" placeholder="🔍 Cerca..." value="${this._filtroTexto}"
          oninput="Dialoghi._filtroTexto=this.value;Dialoghi.renderizarSeletor()"
          style="flex:1;min-width:0;padding:0.44rem 0.75rem;border:1.5px solid #ddd;border-radius:20px;font-size:0.875rem;font-family:inherit">
        <button class="btn-pill-add" onclick="Dialoghi.abrirFormularioCriar()" style="white-space:nowrap">${I18n.t('dial_btn_adicionar')}</button>
        <button class="btn-ia-add" onclick="IAImport.abrir('dialogo')" style="white-space:nowrap">🤖 via IA</button>
      </div>
      <div style="display:flex;gap:0.35rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
        ${_origemPill('','Todos',todos.length)}
        ${nCustom ? _origemPill('custom','🤖 Adicionados',nCustom) : ''}
        ${nNativo  ? _origemPill('nativo','📚 Nativos',nNativo) : ''}
        <select class="nivel-select${this._filtroNivel?' ativo':''}"
          onchange="Dialoghi._filtroNivel=this.value;Dialoghi.renderizarSeletor()">
          <option value="">🎯 Nível</option>
          ${niveis.filter(n=>counts[n]).map(n=>`<option value="${n}" ${this._filtroNivel===n?'selected':''}>${n} (${counts[n]})</option>`).join('')}
        </select>
      </div>
      <div class="dialogo-grid">`;

    for (const dial of filtrados) {
      const ehCustom = dial.custom || dial._custom;
      const badge = ehCustom ? '<span style="font-size:0.65rem;background:#7B68A0;color:white;padding:0.1rem 0.4rem;border-radius:6px;margin-left:0.3rem;">Meu</span>' : '';
      html += `<div class="dialogo-card" onclick="Dialoghi.abrirDialogo('${dial.id}','leitura')">
        <div class="dialogo-icone">${dial.icone}</div>
        <div class="dialogo-titulo">${dial.titulo}${badge}</div>
        <div class="dialogo-nivel">${dial.nivel}</div>
        ${ehCustom ? `<div style="margin-top:0.4rem;display:flex;gap:0.3rem;justify-content:center">
          ${dial.custom ? `<button onclick="event.stopPropagation();Dialoghi.editarDialogo('${dial.id}')" style="background:none;border:none;cursor:pointer;font-size:0.9rem" title="Editar">✏️</button>` : ''}
          <button onclick="event.stopPropagation();Dialoghi.excluirDialogo('${dial.id}')" style="background:none;border:none;cursor:pointer;font-size:0.9rem" title="Excluir">🗑️</button>
        </div>` : `<div style="font-size:0.75rem;color:var(--cor-pietra);margin-top:0.3rem">🎁 ${dial.xp_recompensa} XP</div>`}
      </div>`;
    }

    if (filtrados.length === 0) {
      html += `<p style="text-align:center;color:#aaa;grid-column:1/-1">${filtrados.length === 0 && this._filtroTexto ? 'Nenhum resultado.' : 'Nenhum diálogo ainda.'}</p>`;
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
    if (!titulo) { App.notificar('notif_dial_titulo_obr', 'erro'); return; }

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

    if (turni.length < 2) { App.notificar('notif_dial_sem_turnos', 'erro'); return; }

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
    App.notificar(I18n.t('dial_salvo').replace('{t}', titulo), 'sucesso');
    this.renderizarSeletor();
  },

  editarDialogo(id) { this.abrirFormularioCriar(id); },

  excluirDialogo(id) {
    const d = this.custom.find(x => x.id === id);
    if (!d || !confirm(I18n.t('dial_excluir_confirm').replace('{t}', d.titulo))) return;
    this.custom = this.custom.filter(x => x.id !== id);
    this._salvarCustom();
    App.notificar('notif_dial_excluido', 'alerta');
    this.renderizarSeletor();
  },

  // ── MÉTODOS DE JOGO ──────────────────────────────────────────
  abrirDialogo(id, modo) {
    this.dialogoAtual = this.todosDialoghi().find(d => d.id === id);
    if (!this.dialogoAtual) return;
    this.turnoAtual = 0;
    this.acertos = 0;
    this.modo = modo || 'leitura';
    this.renderizarDialogo();
  },
  
  renderizarDialogo() {
    const c = document.getElementById('dialoghi-container');
    const d = this.dialogoAtual;
    
    let html = `
      <div style="margin-bottom:1rem;display:flex;align-items:center;justify-content:space-between">
        <button class="btn-secondario" onclick="Dialoghi.renderizarSeletor()" style="padding:0.4rem 0.8rem">‹ Voltar</button>
        <div style="display:flex;gap:0.5rem">
          <button class="btn-modo-toggle ${this.modo === 'leitura' ? 'ativo' : ''}" onclick="Dialoghi.modo='leitura';Dialoghi.turnoAtual=0;Dialoghi.renderizarDialogo()" title="Modo Leitura">📖</button>
          <button class="btn-modo-toggle ${this.modo === 'pratica' ? 'ativo' : ''}" onclick="Dialoghi.modo='pratica';Dialoghi.turnoAtual=0;Dialoghi.renderizarDialogo()" title="Modo Prática">✍️</button>
        </div>
      </div>
      <div style="text-align:center;margin-bottom:1rem">
        <div style="font-size:2rem">${d.icone}</div>
        <h3 style="font-family:'Cinzel',serif;color:var(--cor-veneziano-escuro);margin:0.2rem 0">${d.titulo}</h3>
        <p style="font-size:0.85rem;color:var(--cor-pietra);font-style:italic">${d.contexto}</p>
      </div>
      <div class="dialogo-conversa">
    `;
    
    if (this.modo === 'leitura') {
      for (const t of d.turni) {
        const isUtente = t.personaggio === 'Tu';
        const cssClass = isUtente ? 'utente' : 'personaggio';
        // Fallback: se frase estiver vazia mas há alternativas, usa a resposta correta
        const fraseExibir = t.frase || (t.alternativas ? t.alternativas[t.resposta_correta || 0] : '');
        const traducaoExibir = t.traducao || '';
        html += `
          <div class="dialogo-turno ${cssClass}">
            <div class="dialogo-bubble">
              <div class="dialogo-nome">${t.personaggio}</div>
              <div>${fraseExibir} <button class="dialogo-audio-btn" onclick="App.pronunciar('${fraseExibir.replace(/'/g, "\\'")}')">🔊</button></div>
              ${traducaoExibir ? `<div class="dialogo-traducao">${traducaoExibir}</div>` : ''}
            </div>
          </div>
        `;
      }
      html += `
        <div style="text-align:center;margin-top:1.5rem">
          <button class="btn-primario" onclick="Dialoghi.modo='pratica';Dialoghi.turnoAtual=0;Dialoghi.renderizarDialogo()">Praticar Diálogo ✍️</button>
        </div>
      `;
    } else {
      // Modo prática: renderiza apenas o turno atual e os anteriores
      for (let i = 0; i <= this.turnoAtual; i++) {
        const t = d.turni[i];
        const isUtente = t.personaggio === 'Tu';
        const cssClass = isUtente ? 'utente' : 'personaggio';
        
        if (i < this.turnoAtual) {
          // Histórico (já respondido)
          html += `
            <div class="dialogo-turno ${cssClass}">
              <div class="dialogo-bubble">
                <div class="dialogo-nome">${t.personaggio}</div>
                <div>${t.frase}</div>
              </div>
            </div>
          `;
        } else {
          // Turno ativo
          if (!isUtente) {
            // Fala do personagem
            html += `
              <div class="dialogo-turno ${cssClass}" style="animation:fadeIn 0.3s ease">
                <div class="dialogo-bubble">
                  <div class="dialogo-nome">${t.personaggio}</div>
                  <div>${t.frase} <button class="dialogo-audio-btn" onclick="App.pronunciar('${t.frase.replace(/'/g, "\\'")}')">🔊</button></div>
                  <div class="dialogo-traducao">${t.traducao}</div>
                </div>
              </div>
              <div style="text-align:center;margin-top:1rem">
                <button class="btn-primario" onclick="Dialoghi.avancarTurno()">Continuar</button>
              </div>
            `;
          } else {
            // Escolha do usuário
            html += `
              <div style="margin-top:1rem;animation:fadeIn 0.3s ease">
                <div class="dialogo-pratica-frase">Sua vez de falar. Escolha a melhor resposta:</div>
                <div class="dialogo-opcoes">
            `;
            t.alternativas.forEach((alt, idx) => {
              html += `<button class="dialogo-opcao" onclick="Dialoghi.checarResposta(${idx}, this)">${alt}</button>`;
            });
            html += `
                </div>
              </div>
            `;
          }
        }
      }
    }
    
    html += '</div>';
    c.innerHTML = html;
  },
  
  avancarTurno() {
    this.turnoAtual++;
    if (this.turnoAtual >= this.dialogoAtual.turni.length) {
      this.mostrarResultado();
    } else {
      this.renderizarDialogo();
    }
  },
  
  checarResposta(indice, btn) {
    const turno = this.dialogoAtual.turni[this.turnoAtual];
    const correto = indice === turno.resposta_correta;
    
    // Desabilita botões
    const container = btn.parentElement;
    container.querySelectorAll('button').forEach(b => {
      b.disabled = true;
      b.style.cursor = 'default';
    });
    
    if (correto) {
      this.acertos++;
      btn.classList.add('correta');
      App.pronunciar(turno.alternativas[indice]);
      setTimeout(() => {
        this.avancarTurno();
      }, 1200);
    } else {
      btn.classList.add('errada');
      container.children[turno.resposta_correta].classList.add('correta');
      setTimeout(() => {
        this.avancarTurno();
      }, 2500);
    }
  },
  
  mostrarResultado() {
    const d = this.dialogoAtual;
    const totalTu = d.turni.filter(t => t.personaggio === 'Tu').length;
    const pct = Math.round((this.acertos / totalTu) * 100);
    
    // Apenas ganha XP se acertar a maioria e estiver no modo prática
    let ganhouXp = false;
    if (this.modo === 'pratica' && pct >= 60) {
      Progressao.ganhar(d.xp_recompensa);
      ganhouXp = true;
    }
    
    const c = document.getElementById('dialoghi-container');
    c.innerHTML = `
      <div style="text-align:center;padding:2rem 1rem">
        <div style="font-size:3rem">${pct >= 80 ? '🌟' : (pct >= 50 ? '👍' : '🔄')}</div>
        <h3 style="font-family:'Cinzel',serif;color:var(--cor-veneziano-escuro);font-size:1.5rem;margin:1rem 0">${I18n.t('dial_concluido')}</h3>
        <div style="font-size:1.1rem;margin-bottom:1rem">${I18n.t('dial_acertos').replace('{a}', this.acertos).replace('{b}', totalTu)}</div>
        ${ganhouXp ? `<div style="color:var(--cor-toscano);font-weight:700;font-size:1.2rem;margin-bottom:1.5rem">+${d.xp_recompensa} XP</div>` : ''}

        <div style="background:var(--cor-marmore);border-radius:12px;padding:1rem;margin-bottom:1.5rem;text-align:left;box-shadow:0 2px 10px rgba(0,0,0,0.05)">
          <div style="font-size:0.8rem;color:var(--cor-pietra);text-transform:uppercase;font-weight:700;margin-bottom:0.5rem">${I18n.t('dial_vocab_chave')}</div>
          <div style="display:flex;gap:0.5rem;flex-wrap:wrap">
            ${(d.vocabulario_chave || []).map(v => `<span style="background:var(--cor-pergaminho);color:var(--cor-veneziano-escuro);padding:0.2rem 0.6rem;border-radius:20px;font-size:0.85rem">${v}</span>`).join('')}
          </div>
        </div>
        
        <div style="display:flex;gap:1rem;justify-content:center">
          <button class="btn-secondario" onclick="Dialoghi.renderizarSeletor()">${I18n.t('dial_voltar')}</button>
          <button class="btn-primario" onclick="Dialoghi.abrirDialogo('${d.id}', 'pratica')">${I18n.t('dial_praticar_novamente')}</button>
        </div>
      </div>
    `;
  }
};

document.addEventListener('i18n:changed', () => {
  if (document.getElementById('dialoghi-container')) Dialoghi.renderizarSeletor();
});
