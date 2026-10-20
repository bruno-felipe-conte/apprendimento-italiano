// ============================================================
// grammar.js — Grammatica Italiana — Design Didático em 3 Etapas
// Parla e Scrivi — A1 a C2
// Etapas: 1. Aprender a Regra | 2. Exemplos & Armadilhas | 3. Praticar
// Tipos: "escolha" (múltipla escolha) | "revelar" (blur-reveal) | "digitar"
// XP: +8 por acerto · +60 bônus por capítulo concluído
// ============================================================

const Grammatica = {
  dados: null,
  moduloAtual: null,
  unidadeAtual: null,
  etapaAtual: 'aprender', // 'aprender' | 'exemplos' | 'praticar'
  exIndex: 0,
  acertos: 0,
  respondida: false,
  _adminMods: new Set(),   // módulos desbloqueados temporariamente pelo admin

  // ─────────────────────────────────────────────────────────
  // Carregar dados (Stale-While-Revalidate)
  // ─────────────────────────────────────────────────────────
  async carregar() {
    if (this.dados) return;
    try {
      const cached = localStorage.getItem('it_swr_grammar');
      if (cached) {
        this.dados = JSON.parse(cached);
        // Revalida em background sem bloquear a UI
        fetch('data/grammar.json')
          .then(r => r.ok ? r.json() : null)
          .then(fresh => {
            if (fresh && Array.isArray(fresh.moduli)) {
              this.dados = fresh;
              try { localStorage.setItem('it_swr_grammar', JSON.stringify(fresh)); } catch (_) {}
            }
          })
          .catch(() => {});
        return;
      }
    } catch (_) {}

    try {
      const r = await fetch('data/grammar.json');
      if (!r.ok) throw new Error('grammar.json não encontrado');
      this.dados = await r.json();
      try { localStorage.setItem('it_swr_grammar', JSON.stringify(this.dados)); } catch (_) {}
    } catch (e) {
      console.error('Grammatica: erro ao carregar dados', e);
      this.dados = { moduli: [] };
    }
  },

  // ─────────────────────────────────────────────────────────
  // Ponto de entrada — renderiza seletor de módulos
  // ─────────────────────────────────────────────────────────
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('grammatica-container');
    if (!c) return;
    c.innerHTML = this._htmlSeletor();
  },

  // Voltar ao seletor (com confirmação se exercício em andamento)
  voltarSeletor() {
    const total = this.unidadeAtual?.exercicios?.length || 0;
    if (this.unidadeAtual && this.etapaAtual === 'praticar' && this.exIndex > 0 && this.exIndex < total) {
      if (!confirm('Deseja voltar aos módulos? O progresso dos exercícios desta lição será perdido.')) return;
    }
    this.unidadeAtual = null;
    this.renderizarSeletor();
  },

  // ─────────────────────────────────────────────────────────
  // Seletor de módulos e lições
  // ─────────────────────────────────────────────────────────
  _htmlSeletor() {
    if (!this.dados || !this.dados.moduli.length)
      return `<p class="gram-empty">${I18n.t('gram_conteudo_indisponivel')}</p>`;

    const nivel = App.estado.progresso?.nivel || 1;
    const completadas = App.estado.progresso?.grammatica_completadas || [];

    let html = '<div class="gram-seletor">';

    for (const mod of this.dados.moduli) {
      const bloqueado = nivel < mod.nivel_minimo && !this._adminMods.has(mod.id);
      const totalUnid = mod.lezioni.length;
      if (bloqueado || totalUnid === 0) continue; // skip locked/empty modules

      const totalEx   = mod.lezioni.reduce((s, u) => s + (u.exercicios?.length || 0), 0);
      const completas = mod.lezioni.filter(u => completadas.includes(u.id)).length;
      const pct       = totalUnid > 0 ? Math.round((completas / totalUnid) * 100) : 0;

      // Module banner (clicável para colapsar/expandir)
      const adminDesbloqueado = this._adminMods.has(mod.id);
      const infoTxt = I18n.t('gram_concluidas_info')
        .replace('{c}', completas)
        .replace('{t}', totalUnid)
        .replace('{e}', totalEx);
      html += `<div class="gram-nivel-banner" data-nivel="${mod.id}" style="background:${mod.cor};cursor:pointer;user-select:none" onclick="Grammatica.toggleNivel('${mod.id}')">`;
      html += `<div style="display:flex;align-items:center;justify-content:space-between">`;
      html += `<div class="gram-nivel-badge-txt">${mod.id}${adminDesbloqueado ? ' &nbsp;🔓 Admin' : ''}</div>`;
      html += `<span class="gram-nivel-toggle-icone" style="font-size:1.1rem;opacity:0.8;transition:transform 0.2s">▾</span>`;
      html += `</div>`;
      html += `<div class="gram-nivel-nome">${mod.nome}</div>`;
      html += `<div class="gram-nivel-info">${infoTxt}</div>`;
      html += `<div class="gram-nivel-barra"><div style="width:${pct}%"></div></div>`;
      html += '</div>';

      // Grid of lezione cards (id para colapso)
      html += `<div class="gram-lezioni-grid" id="gram-grid-${mod.id}">`;
      for (const u of mod.lezioni) {
        const feita = completadas.includes(u.id);
        const nEx = (u.exercicios || []).length;
        const nCards = (u.observacao_cards || []).length;
        html += `<button class="gram-lez-card${feita ? ' feita' : ''}" onclick="Grammatica.abrirUnidade('${mod.id}','${u.id}')">`;
        html += `<span class="gram-lez-icon">${feita ? '✅' : '📘'}</span>`;
        html += `<span class="gram-lez-info">`;
        if (u.num) html += `<span class="gram-lez-num-label">${u.num}</span>`;
        html += `<span class="gram-lez-titulo">${u.titulo}</span>`;
        html += `<span class="gram-lez-meta">${I18n.t('gram_meta_teoria')}${nCards ? ` · ${nCards} cards` : ''} · ✏️ ${nEx} ${I18n.t('gram_meta_exercicios')}</span>`;
        html += `</span>`;
        html += `<span class="gram-lez-arrow">›</span>`;
        html += '</button>';
      }
      html += '</div>';
    }

    // Locked modules (compact pills — clicáveis para admin)
    const bloqueados = this.dados.moduli.filter(m => nivel < m.nivel_minimo && !this._adminMods.has(m.id) && m.lezioni.length > 0);
    if (bloqueados.length > 0) {
      html += '<div class="gram-locked-row">';
      for (const mod of bloqueados) {
        html += `<button class="gram-locked-pill" onclick="Grammatica.pedirSenhaAdmin('${mod.id}')" title="Acesso administrativo">`;
        html += `<span class="gram-locked-pill-icon">🔒</span>`;
        html += `<span class="gram-locked-pill-info">`;
        html += `<span class="gram-locked-pill-id">${mod.id}</span>`;
        html += `<span class="gram-locked-pill-nome">${mod.nome}</span>`;
        html += `<span class="gram-locked-pill-req">${I18n.t('gram_requer_nivel').replace('{n}', mod.nivel_minimo)}</span>`;
        html += `</span>`;
        html += `<span class="gram-locked-pill-arrow">›</span>`;
        html += `</button>`;
      }
      html += '</div>';
    }

    html += '</div>';
    return html;
  },

  // ─────────────────────────────────────────────────────────
  // Acesso administrativo — popup de senha
  // ─────────────────────────────────────────────────────────
  pedirSenhaAdmin(modId) {
    const mod = this.dados.moduli.find(m => m.id === modId);
    const nome = mod ? mod.nome : modId;

    if (typeof ModalManager !== 'undefined' && ModalManager.abrir) {
      ModalManager.abrir({
        id: 'gram-admin-modal',
        titulo: 'Desbloquear Módulo',
        tamanho: 'pequeno',
        html: `
          <div style="text-align:center; padding: 0.5rem 0;">
            <div style="font-size:2rem; margin-bottom:0.3rem">🔐</div>
            <div style="font-size:0.95rem; color:var(--cor-veneziano-escuro); font-weight:600; margin-bottom:0.8rem">${nome}</div>
            <input
              id="gram-admin-input"
              class="gram-admin-input"
              type="password"
              placeholder="Senha de acesso..."
              maxlength="20"
              autocomplete="off"
              style="width: 100%; border: 2px solid #e0d5c5; border-radius: 10px; padding: 0.72rem 1rem; font-size: 1rem; text-align: center; letter-spacing: 0.25em; box-sizing: border-box;"
              onkeydown="if(event.key==='Enter') Grammatica._confirmarSenha('${modId}'); if(event.key==='Escape') Grammatica._fecharModal()"
            />
            <div id="gram-admin-erro" class="gram-admin-erro" style="display:none; color:#c0392b; font-size:0.8rem; font-weight:600; margin-top:0.4rem">Senha incorreta. Tente novamente.</div>
          </div>
        `,
        acoes: [
          { texto: 'Cancelar', primario: false, onclick: () => this._fecharModal() },
          { texto: 'Desbloquear', primario: true, onclick: () => this._confirmarSenha(modId) }
        ]
      });

      requestAnimationFrame(() => {
        const inp = document.getElementById('gram-admin-input');
        if (inp) inp.focus();
      });
      return;
    }

    const old = document.getElementById('gram-admin-modal');
    if (old) old.remove();

    const overlay = document.createElement('div');
    overlay.id = 'gram-admin-modal';
    overlay.className = 'gram-admin-overlay';
    overlay.innerHTML = `
      <div class="gram-admin-box" role="dialog" aria-modal="true">
        <div class="gram-admin-icon">🔐</div>
        <div class="gram-admin-titulo">Desbloquear Módulo</div>
        <div class="gram-admin-subtit">${nome}</div>
        <input
          id="gram-admin-input"
          class="gram-admin-input"
          type="password"
          placeholder="Senha de acesso..."
          maxlength="20"
          autocomplete="off"
          onkeydown="if(event.key==='Enter') Grammatica._confirmarSenha('${modId}'); if(event.key==='Escape') Grammatica._fecharModal()"
        />
        <div id="gram-admin-erro" class="gram-admin-erro" style="display:none">Senha incorreta. Tente novamente.</div>
        <div class="gram-admin-btns">
          <button class="gram-admin-btn-cancel" onclick="Grammatica._fecharModal()">Cancelar</button>
          <button class="gram-admin-btn-ok" onclick="Grammatica._confirmarSenha('${modId}')">Desbloquear</button>
        </div>
      </div>`;

    overlay.addEventListener('click', e => { if (e.target === overlay) this._fecharModal(); });
    document.body.appendChild(overlay);

    requestAnimationFrame(() => {
      const inp = document.getElementById('gram-admin-input');
      if (inp) inp.focus();
    });
  },

  _fecharModal() {
    if (typeof ModalManager !== 'undefined' && ModalManager.fechar) {
      ModalManager.fechar('gram-admin-modal');
    }
    const m = document.getElementById('gram-admin-modal');
    if (m) { m.classList.add('gram-admin-saindo'); setTimeout(() => m.remove(), 220); }
  },

  async _confirmarSenha(modId) {
    const inp = document.getElementById('gram-admin-input');
    const erro = document.getElementById('gram-admin-erro');
    if (!inp) return;

    const valido = (typeof App !== 'undefined' && App.verificarCodigoAcesso)
      ? await App.verificarCodigoAcesso(inp.value)
      : false;

    if (valido) {
      this._adminMods.add(modId);
      this._fecharModal();
      const c = document.getElementById('grammatica-container');
      if (c) c.innerHTML = this._htmlSeletor();
    } else {
      inp.value = '';
      if (erro) { erro.style.display = 'block'; }
      inp.classList.add('gram-admin-shake');
      setTimeout(() => inp.classList.remove('gram-admin-shake'), 500);
      inp.focus();
    }
  },

  // ── Colapsa / expande o grid de lições de um nível ───────────
  toggleNivel(id) {
    const grid   = document.getElementById(`gram-grid-${id}`);
    const banner = document.querySelector(`.gram-nivel-banner[data-nivel="${id}"]`);
    if (!grid) return;
    const recolhido = grid.classList.toggle('recolhido');
    const seta = banner?.querySelector('.gram-nivel-toggle-icone');
    if (seta) seta.style.transform = recolhido ? 'rotate(-90deg)' : 'rotate(0deg)';
  },

  // ─────────────────────────────────────────────────────────
  // Abrir lição (Inicia sempre na Etapa 1: Aprender a Regra)
  // ─────────────────────────────────────────────────────────
  abrirUnidade(moduloId, unidadeId, etapaInicial = 'aprender') {
    const mod  = this.dados.moduli.find(m => m.id === moduloId);
    if (!mod) return;
    const unid = mod.lezioni.find(u => u.id === unidadeId);
    if (!unid) return;

    this.moduloAtual  = mod;
    this.unidadeAtual = unid;
    this.etapaAtual   = etapaInicial;
    this.exIndex      = 0;
    this.acertos      = 0;
    this.respondida   = false;

    const c = document.getElementById('grammatica-container');
    if (c) {
      c.innerHTML = this._htmlUnidade(unid);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  },

  irParaEtapa(etapa) {
    if (!this.unidadeAtual) return;
    this.etapaAtual = etapa;
    const c = document.getElementById('grammatica-container');
    if (c) {
      c.innerHTML = this._htmlUnidade(this.unidadeAtual);
      const nav = document.querySelector('.gram-steps-bar');
      if (nav) nav.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  },

  // ─────────────────────────────────────────────────────────
  // HTML completo da lição com Barra de 3 Etapas Didáticas
  // ─────────────────────────────────────────────────────────
  _htmlUnidade(u) {
    const mod = this.moduloAtual;
    const nEx = (u.exercicios || []).length;

    let html = '<div class="gram-lesson-layout">';

    // Nav superior
    html += '<div class="gram-lesson-nav">';
    html += `<button class="gram-btn-back" onclick="Grammatica.voltarSeletor()">‹ Todos os módulos</button>`;
    html += `<div class="gram-lesson-breadcrumb"><span>${mod.id}</span>${u.num ? ` › <span>${u.num}</span>` : ''}</div>`;
    html += '</div>';

    // Cabeçalho da lição
    html += '<div class="gram-lesson-header">';
    if (u.num) html += `<div class="gram-lesson-eyebrow">${u.num}</div>`;
    html += `<h2 class="gram-lesson-title">${u.titulo}</h2>`;
    if (u.subtitulo) html += `<p class="gram-lesson-subtitle">${u.subtitulo}</p>`;
    html += '</div>';

    // Barra de Navegação das 3 Etapas Didáticas
    html += `
      <div class="gram-steps-bar" role="tablist" aria-label="Etapas da lição">
        <button class="gram-step-btn ${this.etapaAtual === 'aprender' ? 'active' : ''}"
                onclick="Grammatica.irParaEtapa('aprender')" role="tab" aria-selected="${this.etapaAtual === 'aprender'}">
          <span class="gram-step-num">1</span>
          <span class="gram-step-txt">📖 Aprender a Regra</span>
        </button>
        <button class="gram-step-btn ${this.etapaAtual === 'exemplos' ? 'active' : ''}"
                onclick="Grammatica.irParaEtapa('exemplos')" role="tab" aria-selected="${this.etapaAtual === 'exemplos'}">
          <span class="gram-step-num">2</span>
          <span class="gram-step-txt">🔍 Exemplos & Armadilhas</span>
        </button>
        <button class="gram-step-btn ${this.etapaAtual === 'praticar' ? 'active' : ''}"
                onclick="Grammatica.irParaEtapa('praticar')" role="tab" aria-selected="${this.etapaAtual === 'praticar'}">
          <span class="gram-step-num">3</span>
          <span class="gram-step-txt">✏️ Praticar (${nEx})</span>
        </button>
      </div>`;

    // Conteúdo da Etapa Ativa
    if (this.etapaAtual === 'aprender') {
      html += this._htmlEtapaAprender(u);
    } else if (this.etapaAtual === 'exemplos') {
      html += this._htmlEtapaExemplos(u);
    } else {
      html += this._htmlEtapaPraticar(u);
    }

    html += '</div>'; // lesson-layout
    return html;
  },

  // ─────────────────────────────────────────────────────────
  // ETAPA 1: 📖 Aprender a Regra (Integra TODAS as camadas teóricas)
  // ─────────────────────────────────────────────────────────
  _htmlEtapaAprender(u) {
    let h = '<div class="gram-card gram-teoria-card"><div class="gram-camadas">';

    // 0. Jornada narrativa: cena viva + fio condutor
    h += this._htmlCena(u);
    if (u.fio && u.fio.descoberta) h += `<p class="gram-fio">${this._formatarPergunta(u.fio.descoberta)}</p>`;

    // 2. Definição (Veja -> Pense -> Entenda)
    h += this._htmlDefinicao(u);

    // 3. Inventário de Estruturas-Chave
    h += this._htmlInventario(u);

    // 4. Tabela Visual Resumida (Cards visuais)
    h += this._htmlFase3Tabela(u);

    // 5. Cards Interativos de Observação (Flip Cards com botão de áudio isolado)
    h += this._htmlFase2Observacao(u);

    // 6. Técnica Passo a Passo (Como Aplicar)
    h += this._htmlTecnica(u);

    // 7. Teoria Completa e Tabelas Detalhadas (Antes ignorada!)
    if (u.teoria) {
      h += `
        <div class="gram-camada-bloco">
          <div class="gram-camada-label">📚 Explicação Completa & Quadros de Referência</div>
          <div class="gram-teoria-corpo" style="padding: 1.1rem 1.25rem">${this._formatarTeoria(u.teoria)}</div>
        </div>`;
    }

    // 8. Ponte com o Português (Comparação contrastiva PT ↔ IT)
    h += this._htmlPonte(u);

    if (u.fio && u.fio.fecho) h += `<p class="gram-fio gram-fio-fecho">${this._formatarPergunta(u.fio.fecho)}</p>`;

    // Botão de avanço intuitivo para a Etapa 2
    h += `
      <div class="gram-step-footer">
        <button class="gram-btn-next gram-btn-step-cta" onclick="Grammatica.irParaEtapa('exemplos')">
          Avançar para Exemplos & Armadilhas →
        </button>
      </div>`;

    h += '</div></div>';
    return h;
  },

  // ─────────────────────────────────────────────────────────
  // ETAPA 2: 🔍 Exemplos & Armadilhas
  // ─────────────────────────────────────────────────────────
  _htmlEtapaExemplos(u) {
    const nEx = (u.exercicios || []).length;
    let h = '<div class="gram-card gram-teoria-card"><div class="gram-camadas">';

    // 1. Exemplos Analisados (Pergunta -> Resposta -> Conclusão) com áudio isolado
    h += this._htmlFase4Exemplos(u);

    // 2. Frases extras de exemplo com áudio clicável
    if (u.exemplos && u.exemplos.length) {
      let lista = '';
      for (const ex of u.exemplos) {
        const it = typeof ex === 'string' ? ex : (ex.it || '');
        const pt = typeof ex === 'string' ? '' : (ex.pt || '');
        const safe = it.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
        lista += `
          <div class="gram-esempio" onclick="App.pronunciar('${safe}')" style="cursor:pointer" title="Clique para ouvir a pronúncia em italiano">
            <div class="gram-esempio-it">🔊 ${this._formatarPergunta(it)}</div>
            ${pt ? `<div class="gram-esempio-pt">${this._formatarPergunta(pt)}</div>` : ''}
          </div>`;
      }
      h += `
        <div class="gram-camada-bloco">
          <div class="gram-camada-label">🎧 Frases Autênticas para Ouvir e Repetir</div>
          <div class="gram-esempi-lista" style="padding: 0.9rem 1.25rem">${lista}</div>
        </div>`;
    }

    // 3. Armadilhas Comuns (Errado ✗ vs Certo ✓ com áudio na forma certa)
    h += this._htmlFase5Armadilhas(u);

    // 4. Coda (Resumo prático de memorização)
    h += this._htmlCoda(u);

    // Botões de navegação de rodapé
    h += `
      <div class="gram-step-footer" style="display:flex;gap:0.75rem;justify-content:space-between;flex-wrap:wrap">
        <button class="gram-btn-secondary" onclick="Grammatica.irParaEtapa('aprender')">
          ← Voltar à Regra
        </button>
        <button class="gram-btn-next gram-btn-step-cta" onclick="Grammatica.irParaEtapa('praticar')">
          Ir para os Exercícios (${nEx}) ✏️ →
        </button>
      </div>`;

    h += '</div></div>';
    return h;
  },

  // ─────────────────────────────────────────────────────────
  // ETAPA 3: ✏️ Praticar (Exercícios + Consulta Rápida no Topo)
  // ─────────────────────────────────────────────────────────
  _htmlEtapaPraticar(u) {
    let h = '';
    // Painel colapsável de consulta rápida (Tabela Visual + Técnica + Ponte)
    h += this._htmlTabelaVisual(u);

    // Área de exercícios
    h += '<div id="gram-ex-area">';
    h += this._htmlExercicio();
    h += '</div>';

    return h;
  },

  // ─────────────────────────────────────────────────────────
  // Exercício atual
  // ─────────────────────────────────────────────────────────
  _htmlExercicio() {
    const u = this.unidadeAtual;
    if (!u || this.exIndex >= u.exercicios.length) return this._htmlResultado();

    const ex    = u.exercicios[this.exIndex];
    const total = u.exercicios.length;
    const pct   = Math.round((this.exIndex / total) * 100);
    const qHtml = this._formatarPergunta(ex.pergunta);

    let html = '<div class="gram-card">';

    // Progresso + tipo badge na mesma linha
    const tipoLabel = ex.tipo === 'revelar' ? '👁️ Descubra' : ex.tipo === 'digitar' ? '⌨️ Escreva' : '🔘 Escolha';
    const tipoCls   = ex.tipo === 'revelar' ? 'gram-ex-tipo-revelar' : ex.tipo === 'digitar' ? 'gram-ex-tipo-digitar' : 'gram-ex-tipo-escolha';
    html += '<div class="gram-ex-header">';
    html += `<div class="gram-ex-header-top"><span class="gram-ex-progress-label">Exercício ${this.exIndex + 1} / ${total}</span><span class="gram-ex-tipo-badge ${tipoCls}">${tipoLabel}</span></div>`;
    html += `<div class="gram-ex-progress-bar"><div class="gram-ex-progress-fill" style="width:${pct}%"></div></div>`;
    html += '</div>';

    // Pergunta
    html += `<div class="gram-ex-question">${qHtml}</div>`;

    // Corpo do exercício
    if (ex.tipo === 'escolha') {
      html += this._htmlEscolha(ex);
    } else if (ex.tipo === 'digitar') {
      html += this._htmlDigitar(ex);
    } else {
      html += this._htmlRivelar(ex);
    }

    // Feedback (oculto até responder)
    html += '<div class="gram-ex-feedback" id="gram-feedback"></div>';

    // Ações (ocultas até responder)
    html += '<div class="gram-ex-actions" id="gram-actions" style="display:none">';
    if (ex.tipo === 'revelar') {
      html += '<button class="gram-btn-errei"  onclick="Grammatica.proximoExercicio()">❌ Preciso revisar</button>';
      html += '<button class="gram-btn-acertei" onclick="Grammatica.marcarAcerto()">✅ Acertei</button>';
    } else {
      html += '<button class="gram-btn-next" onclick="Grammatica.proximoExercicio()">Próximo →</button>';
    }
    html += '</div>';

    html += '</div>'; // card
    return html;
  },

  // ─── Múltipla escolha ───
  _htmlEscolha(ex) {
    let html = '<div class="gram-options" id="gram-options">';
    for (let i = 0; i < ex.opcoes.length; i++) {
      const op = this._formatarPergunta(ex.opcoes[i]);
      html += `<button class="gram-option" id="gram-op-${i}" onclick="Grammatica.responder(${i})">${op}</button>`;
    }
    html += '</div>';
    return html;
  },

  // ─── Digitação livre ───
  _htmlDigitar(ex) {
    const dica = ex.dica ? `<div class="gram-digitar-dica">💡 ${ex.dica}</div>` : '';
    return `
      <div class="gram-digitar-area" id="gram-digitar-area">
        ${dica}
        <div class="gram-digitar-row">
          <input class="gram-input-digitacao" id="gram-input-digitacao"
                 type="text" placeholder="${I18n.t('gram_placeholder_resposta')}"
                 autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"
                 onkeydown="if(event.key==='Enter')Grammatica.responderDigitar()">
          <button class="gram-btn-verificar" onclick="Grammatica.responderDigitar()">✔ Verificar</button>
        </div>
      </div>`;
  },

  // ─── Blur-reveal ───
  _htmlRivelar(ex) {
    const respStr = String(ex.resposta || '');
    const partes = respStr.split(/(\s+)/);
    const spans  = partes.map(p => {
      if (/^\s+$/.test(p)) return p;
      return `<span class="gram-word-blur" onclick="Grammatica.togglePalavra(this)">${p}</span>`;
    }).join('');

    let html = '<div class="gram-revelar-area">';
    const hint = I18n.idioma === 'it'
      ? '👆 Clicca sulle parole per rivelare, o clicca su "Vedi risposta"'
      : '👆 Pense na resposta e clique nas palavras para conferir (ou em "Ver resposta")';
    html += `<div class="gram-revelar-hint">${hint}</div>`;
    html += `<div class="gram-risposta-container" id="gram-risposta">${spans}</div>`;
    html += '<div class="gram-revelar-actions">';
    html += '<button class="gram-btn-rivela-tutto" onclick="Grammatica.revelarTudo()">👁️ Ver resposta completa</button>';
    html += '<button class="gram-btn-nascondi" id="gram-btn-nascondi" onclick="Grammatica.nasconderTudo()">Ocultar</button>';
    html += '</div>';
    html += '</div>';
    return html;
  },

  // ─────────────────────────────────────────────────────────
  // Interações blur-reveal
  // ─────────────────────────────────────────────────────────
  togglePalavra(el) {
    el.classList.toggle('revealed');
    this._verificarTudoRevelado();
  },

  revelarTudo() {
    document.querySelectorAll('.gram-word-blur').forEach(w => w.classList.add('revealed'));
    const btn = document.getElementById('gram-btn-nascondi');
    if (btn) btn.style.display = 'inline-flex';
    this._afterReveal();
  },

  nasconderTudo() {
    document.querySelectorAll('.gram-word-blur').forEach(w => w.classList.remove('revealed'));
    const fb = document.getElementById('gram-feedback');
    if (fb) fb.innerHTML = '';
    const actions = document.getElementById('gram-actions');
    if (actions) actions.style.display = 'none';
    const btn = document.getElementById('gram-btn-nascondi');
    if (btn) btn.style.display = 'none';
    this.respondida = false;
  },

  _verificarTudoRevelado() {
    const words = document.querySelectorAll('.gram-word-blur');
    if ([...words].every(w => w.classList.contains('revealed'))) {
      const btn = document.getElementById('gram-btn-nascondi');
      if (btn) btn.style.display = 'inline-flex';
      this._afterReveal();
    }
  },

  _botaoOuvirExercicio(ex) {
    let fraseParaOuvir = '';
    if (ex.tipo === 'escolha' && Array.isArray(ex.opcoes) && typeof ex.resposta === 'number') {
      const opCorreta = ex.opcoes[ex.resposta] || '';
      if (ex.pergunta && ex.pergunta.includes('___')) {
        fraseParaOuvir = ex.pergunta.replace(/___+/g, opCorreta).replace(/\*\*|\*/g, '');
      } else {
        fraseParaOuvir = opCorreta;
      }
    } else if (ex.resposta) {
      fraseParaOuvir = String(ex.resposta);
    }
    fraseParaOuvir = fraseParaOuvir.replace(/\n+/g, ' ').trim();
    if (!fraseParaOuvir || fraseParaOuvir.length > 180) return '';
    const safe = fraseParaOuvir.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    return `<div style="margin-top:0.55rem"><button class="gram-audio-mini-btn" onclick="App.pronunciar('${safe}')">🔊 Ouvir pronúncia em italiano</button></div>`;
  },

  _afterReveal() {
    if (this.respondida) return;
    this.respondida = true;
    const ex = this.unidadeAtual.exercicios[this.exIndex];
    const fb = document.getElementById('gram-feedback');
    if (fb && ex.explicacao) {
      fb.innerHTML = `<div class="gram-feedback-info">💡 <strong>${I18n.t('gram_por_que')}</strong> ${this._formatarPergunta(ex.explicacao)}${this._botaoOuvirExercicio(ex)}</div>`;
    }
    const actions = document.getElementById('gram-actions');
    if (actions) actions.style.display = 'flex';
  },

  revelarResposta() { this.revelarTudo(); },

  // ─────────────────────────────────────────────────────────
  // Responder múltipla escolha
  // ─────────────────────────────────────────────────────────
  responder(indice) {
    if (this.respondida) return;
    this.respondida = true;

    const ex      = this.unidadeAtual.exercicios[this.exIndex];
    const correto = (indice === ex.resposta);

    for (let i = 0; i < ex.opcoes.length; i++) {
      const btn = document.getElementById(`gram-op-${i}`);
      if (!btn) continue;
      btn.disabled = true;
      btn.className = i === ex.resposta
        ? 'gram-option-correct'
        : i === indice && !correto
          ? 'gram-option-wrong'
          : 'gram-option-disabled';
    }

    const fb = document.getElementById('gram-feedback');
    if (fb) {
      const expHtml = this._formatarPergunta(ex.explicacao || '');
      const audioBtn = this._botaoOuvirExercicio(ex);
      fb.innerHTML = correto
        ? `<div class="gram-feedback-correct">✅ <strong>${I18n.t('gram_correto')}</strong> ${expHtml}${audioBtn}</div>`
        : `<div class="gram-feedback-wrong">❌ <strong>${I18n.t('gram_errado')}</strong> ${expHtml}${audioBtn}</div>`;
    }

    const actions = document.getElementById('gram-actions');
    if (actions) actions.style.display = 'flex';

    if (correto) { this.acertos++; App.ganharXP(8); }
  },

  // ─────────────────────────────────────────────────────────
  // Responder digitação
  // ─────────────────────────────────────────────────────────
  responderDigitar() {
    if (this.respondida) return;
    const input = document.getElementById('gram-input-digitacao');
    if (!input) return;

    const ex = this.unidadeAtual.exercicios[this.exIndex];
    const digitado = input.value.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    const correta  = String(ex.resposta ?? '').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    const variantes = (ex.variantes || []).map(v =>
      String(v ?? '').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    );
    const correto = digitado === correta || variantes.includes(digitado);

    this.respondida = true;
    input.disabled = true;
    input.classList.add(correto ? 'digitar-correto' : 'digitar-errado');

    const fb = document.getElementById('gram-feedback');
    if (fb) {
      const expHtml = ex.explicacao ? ' ' + this._formatarPergunta(ex.explicacao) : '';
      const audioBtn = this._botaoOuvirExercicio(ex);
      fb.innerHTML = correto
        ? `<div class="gram-feedback-correct">✅ <strong>${I18n.t('gram_correto')}</strong>${expHtml}${audioBtn}</div>`
        : `<div class="gram-feedback-wrong">❌ <strong>${I18n.t('gram_errado')}</strong> ${I18n.t('gram_resposta_era')} <strong>${ex.resposta}</strong>.${expHtml}${audioBtn}</div>`;
    }

    const actions = document.getElementById('gram-actions');
    if (actions) actions.style.display = 'flex';

    if (correto) { this.acertos++; App.ganharXP(8); }
  },

  // ─────────────────────────────────────────────────────────
  // Marcar acerto (revelar)
  // ─────────────────────────────────────────────────────────
  marcarAcerto() {
    this.acertos++;
    App.ganharXP(5);
    this.proximoExercicio();
  },

  // ─────────────────────────────────────────────────────────
  // Avançar para próximo exercício
  // ─────────────────────────────────────────────────────────
  proximoExercicio() {
    this.exIndex++;
    this.respondida = false;
    const area = document.getElementById('gram-ex-area');
    if (!area) return;
    area.style.transition = 'opacity 0.15s ease, transform 0.15s ease';
    area.style.opacity = '0';
    area.style.transform = 'translateY(8px)';
    setTimeout(() => {
      area.innerHTML = this.exIndex >= this.unidadeAtual.exercicios.length
        ? this._htmlResultado()
        : this._htmlExercicio();
      area.style.opacity = '1';
      area.style.transform = 'translateY(0)';
      area.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 160);
  },

  // ─────────────────────────────────────────────────────────
  // Tela de resultado
  // ─────────────────────────────────────────────────────────
  _htmlResultado() {
    const total   = this.unidadeAtual.exercicios.length;
    const acertos = this.acertos;
    const pct     = total > 0 ? Math.round((acertos / total) * 100) : 0;
    const bonus   = 60;

    const completadas = (App.estado.progresso || {}).grammatica_completadas || [];
    const jaFeita     = completadas.includes(this.unidadeAtual.id);
    if (!jaFeita) {
      completadas.push(this.unidadeAtual.id);
      App.estado.progresso.grammatica_completadas = completadas;
      App.salvarProgresso();
      App.ganharXP(bonus);
      App.notificar(I18n.t('notif_gram_capitolo').replace('{xp}', bonus), 'sucesso');
    }

    if (typeof Calor !== 'undefined') Calor.registrar(total);

    let emoji = '📚', msg = 'Continue praticando — revise a teoria e tente novamente!';
    if      (pct === 100) { emoji = '🌟'; msg = 'Perfeito! Você dominou todas as questões desta lição!'; }
    else if (pct >= 80)   { emoji = '🎉'; msg = 'Excelente trabalho! Domínio muito sólido do tema!'; }
    else if (pct >= 60)   { emoji = '💪'; msg = 'Bom resultado! Vale revisar as armadilhas para chegar a 100%.'; }

    // Próxima lição
    const unids = this.moduloAtual.lezioni;
    const idx   = unids.findIndex(u => u.id === this.unidadeAtual.id);
    let proxBtn = '';
    if (idx >= 0 && idx < unids.length - 1) {
      const prox = unids[idx + 1];
      proxBtn = `<button class="gram-btn-next" onclick="Grammatica.abrirUnidade('${this.moduloAtual.id}','${prox.id}')">Próxima lição →</button>`;
    }

    return `
      <div class="gram-card gram-resultado">
        <div class="gram-res-emoji">${emoji}</div>
        <div class="gram-res-title">Lição Concluída!</div>
        <div class="gram-res-score">${acertos}<span>/${total}</span></div>
        <div class="gram-res-pct">${pct}% de acertos</div>
        ${!jaFeita ? `<div class="gram-res-xp">+${bonus} XP bônus 🏆</div>` : ''}
        <div class="gram-res-msg">${msg}</div>
        <div class="gram-res-actions">
          <button class="gram-btn-secondary" onclick="Grammatica.abrirUnidade('${this.moduloAtual.id}','${this.unidadeAtual.id}','praticar')">🔄 Refazer Exercícios</button>
          <button class="gram-btn-secondary" onclick="Grammatica.irParaEtapa('aprender')">📖 Revisar Teoria</button>
          ${proxBtn}
          <button class="gram-btn-secondary" onclick="Grammatica.voltarSeletor()">‹ Todos os módulos</button>
        </div>
      </div>`;
  },

  // ─────────────────────────────────────────────────────────
  // Formatação da teoria (Markdown → HTML)
  // ─────────────────────────────────────────────────────────
  _formatarTeoria(texto) {
    if (!texto) return '';

    const htmlTables = [];
    texto = texto.replace(/<table[\s\S]*?<\/table>/gi, (m) => {
      htmlTables.push(m);
      return `\x00T${htmlTables.length - 1}\x00`;
    });

    // Headings markdown (### e ####)
    texto = texto
      .replace(/^####\s+(.+)$/gm, '<h4 style="color:#9B2335;margin:1rem 0 0.4rem;font-size:1rem">$1</h4>')
      .replace(/^###\s+(.+)$/gm, '<h3 style="color:#6B1A2A;margin:1.1rem 0 0.5rem;font-size:1.12rem;border-bottom:1px solid #ede0d0;padding-bottom:0.25rem">$1</h3>');

    // Bold e italic
    texto = texto
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Linhas pipe → <tr>
    texto = texto.replace(/^(\|.+\|)$/gm, (row) => {
      const clean = row.replace(/[\|\s\-:]/g, '');
      if (!clean) return '';
      const cells = row.split('|').filter((_, i, a) => i > 0 && i < a.length - 1);
      if (cells.some(c => /^[\s\-:]+$/.test(c))) return '';
      return '<tr>' + cells.map((c, i) => {
        const tag = i === 0 ? 'th' : 'td';
        return `<${tag}>${c.trim()}</${tag}>`;
      }).join('') + '</tr>';
    });

    texto = texto.replace(/((<tr>[\s\S]*?<\/tr>\n*)+)/g,
      '<table class="gram-table">$1</table>');

    texto = texto.replace(/(<table[^>]*>)([\s\S]*?)(<\/table>)/g,
      (_, open, inner, close) => open + inner.replace(/\n+/g, '') + close);

    texto = texto.replace(/\n+(<table)/g, '\n$1');
    texto = texto.replace(/(<\/table>)\n+/g, '$1\n');

    texto = texto.replace(/\n{2,}/g, '\n\n');
    texto = texto.replace(/\n\n/g, '</p><p>');
    texto = texto.replace(/\n/g, '<br>');

    texto = texto.replace(/<p>\s*<\/p>/g, '');
    texto = texto.replace(/(<br>)+(<table)/g, '$2');
    texto = texto.replace(/(<\/table>)(<br>)+/g, '$1');
    texto = texto.replace(/<p>(<table)/g, '$1');
    texto = texto.replace(/(<\/table>)<\/p>/g, '$1');

    htmlTables.forEach((t, i) => {
      texto = texto.replace(`\x00T${i}\x00`, t);
    });

    texto = texto.replace(
      /(<p>)(<strong>(?:Regola|Nota bene|Nota|Regra)[^<]*:<\/strong>)/gi,
      '<p class="gram-regola">$2'
    );
    texto = texto.replace(
      /(<p>)(<strong>(?:Attenzione|Importante|Achtung|Atenção)[^<]*!?:?<\/strong>)/gi,
      '<p class="gram-attenzione">$2'
    );

    texto = texto.replace(
      /<p>(<strong>[A-ZÀÈÉÌÒÙ][a-zàèéìòùA-Z\s]+:<\/strong>[^<p]{0,300}<br>[^<p]{0,50}<strong>[A-ZÀÈÉÌÒÙ])/g,
      '<p class="gram-dialogo-box">$1'
    );

    return texto;
  },

  _formatarPergunta(texto) {
    if (!texto) return '';
    return String(texto)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  },

  // ─── FASE 1: Ancoragem ───
  _htmlCena(u) {
    if (!u.cena) return '';
    const esc = t => t.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '&quot;');
    const linhas = u.cena.texto.split('\n').map(x => x.trim()).filter(x => x && !/^_.*_$/.test(x));
    let corpo = '';
    for (const raw of linhas) {
      const plain = raw.replace(/\*\*[^*]+:\*\*\s*/, '').replace(/\*/g, '').replace(/_/g, '');
      corpo += `<div class="gram-cena-linha"><button class="gram-audio-mini-btn" onclick="App.pronunciar('${esc(plain)}')" title="Ouvir">🔊</button><span>${this._formatarPergunta(raw)}</span></div>`;
    }
    const abertura = (u.fio && u.fio.abertura) ? `<p class="gram-fio">${this._formatarPergunta(u.fio.abertura)}</p>` : '';
    return `<div class="gram-cena">
      <div class="gram-cena-etiqueta">🎭 ${u.cena.origem === 'parla_e_scrivi' ? 'La scena' : 'Vozes da vida real'} — ${u.cena.titulo}</div>
      ${abertura}<div class="gram-cena-corpo">${corpo}</div></div>`;
  },

  _htmlFase1Ancoragem(u) {
    if (!u.alerta) return '';
    return `<div class="gram-alerta">💬 <strong>${I18n.t('gram_por_que_importa')}</strong><br>${this._formatarPergunta(u.alerta)}</div>`;
  },

  // ─── FASE 2: Observação (Flip Cards Clicáveis + Botão de Áudio) ───
  _htmlFase2Observacao(u) {
    if (!u.observacao_cards || !u.observacao_cards.length) return '';
    let cards = '';
    for (let i = 0; i < u.observacao_cards.length; i++) {
      const c = u.observacao_cards[i];
      const safeIt = (c.italiano || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      const badgeTxt = (c.artigo && c.artigo !== '⚠️' && c.artigo !== '📌')
        ? `${c.artigo} · ${c.genero || ''}`
        : (c.genero || 'regra');
      cards += `
        <div class="gram-flip-card" onclick="this.classList.toggle('flipped')">
          <div class="gram-flip-card-inner">
            <div class="gram-flip-card-front">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:0.4rem">
                <div class="gfc-it">${c.italiano}</div>
                <button class="gram-audio-mini-btn" onclick="event.stopPropagation();App.pronunciar('${safeIt}')" title="Ouvir pronúncia">🔊</button>
              </div>
              <div class="gfc-pt">🇧🇷 ${c.traducao}</div>
              <div class="gfc-badge">${badgeTxt}</div>
              <div class="gfc-click">${I18n.idioma === 'it' ? 'Clicca per vedere la regola 👆' : 'Clique no card para ver o porquê 👆'}</div>
            </div>
            <div class="gram-flip-card-back">
              <div class="gfc-titulo-regra">💡 Por que funciona assim:</div>
              <div class="gfc-regra-txt">${this._formatarPergunta(c.motivo)}</div>
            </div>
          </div>
        </div>`;
    }
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label">${I18n.t('gram_fase2_label')}</div>
        <div style="padding: 0.85rem 1.25rem 0.4rem; font-size: 0.9rem; color: #666; line-height: 1.5;">${I18n.t('gram_fase2_sub')}</div>
        <div class="gram-observacao-grid">${cards}</div>
      </div>`;
  },

  // ─── FASE 3: Tabela Visual (Sempre Visível) ───
  _htmlFase3Tabela(u) {
    if (!u.tabela_visual) return '';
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label">${I18n.t('gram_fase3_label')}</div>
        <div class="gram-tabela-sem-details">${u.tabela_visual}</div>
      </div>`;
  },

  // ─── FASE 4: Exemplos P/R/C (Com botão de expandir todos e áudio isolado) ───
  toggleTodosPRC() {
    const cards = document.querySelectorAll('.gram-prc-expandivel');
    const todosAbertos = [...cards].every(c => c.classList.contains('aberto'));
    cards.forEach(c => c.classList.toggle('aberto', !todosAbertos));
  },

  _htmlFase4Exemplos(u) {
    if (!u.exemplos_prc || !u.exemplos_prc.length) return '';
    let rows = '';
    for (let i = 0; i < u.exemplos_prc.length; i++) {
      const e = u.exemplos_prc[i];
      const safe = (e.oracao || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      // Deixa o 1º exemplo já aberto por padrão para o aluno entender a dinâmica
      const abertoCls = i === 0 ? ' aberto' : '';
      rows += `
        <div class="gram-prc-expandivel${abertoCls}" id="gram-prc-card-${i}">
          <div class="gram-prc-topo" onclick="this.parentElement.classList.toggle('aberto')">
            <span class="gram-prc-it">
              <button class="gram-audio-mini-btn" onclick="event.stopPropagation();App.pronunciar('${safe}')" title="Ouvir frase">🔊</button>
              <em>${this._formatarPergunta(e.oracao || '')}</em>
            </span>
            <span class="gram-prc-btn-expandir">${I18n.t('gram_fase4_ver_detalhes')}</span>
          </div>
          <div class="gram-prc-conteudo-oculto">
            <div class="gram-prc-pq"><span class="gram-prc-tag">${I18n.t('gram_fase4_prc_pergunta')}</span> ${this._formatarPergunta(e.pergunta || '')}</div>
            <div class="gram-prc-pq"><span class="gram-prc-tag">${I18n.t('gram_fase4_prc_resposta')}</span> ${this._formatarPergunta(e.resposta || '')}</div>
            <div class="gram-prc-conclusao"><span class="gram-prc-tag gram-prc-tag-c">${I18n.t('gram_fase4_prc_conclusao')}</span> <strong>${this._formatarPergunta(e.conclusao || '')}</strong></div>
          </div>
        </div>`;
    }
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem">
          <span>${I18n.t('gram_fase4_label')}</span>
          <button class="gram-audio-mini-btn" onclick="Grammatica.toggleTodosPRC()" style="font-size:0.74rem">↕ Expandir / Recolher Todos</button>
        </div>
        <div style="padding: 0.85rem 1.25rem 0.4rem; font-size: 0.9rem; color: #666; line-height: 1.5;">${I18n.t('gram_fase4_sub')}</div>
        <div class="gram-prc-lista">${rows}</div>
      </div>`;
  },

  // ─── FASE 5: Armadilhas (Lado a Lado Errado ✗ vs Certo ✓ com Áudio) ───
  _htmlFase5Armadilhas(u) {
    if (!u.armadilhas || !u.armadilhas.length) return '';
    let cards = '';
    for (let i = 0; i < u.armadilhas.length; i++) {
      const a = u.armadilhas[i];
      const safeCerto = (a.certo || '').replace(/\\/g, '\\\\').replace(/'/g, "\\'");
      cards += `
        <div class="gram-armadilha-row">
          <div class="gram-armadilha-col gram-arm-errada">
            <span class="gram-arm-icon">✗</span>
            <div class="gram-arm-texto">
              <span class="gram-arm-lbl">${I18n.t('gram_arm_errado')}</span>
              <strong>${this._formatarPergunta(a.errado)}</strong>
            </div>
          </div>
          <div class="gram-armadilha-col gram-arm-certa" onclick="App.pronunciar('${safeCerto}')" style="cursor:pointer" title="Clique para ouvir a forma correta">
            <span class="gram-arm-icon">✓</span>
            <div class="gram-arm-texto">
              <span class="gram-arm-lbl">${I18n.t('gram_arm_certo')} 🔊</span>
              <strong>${this._formatarPergunta(a.certo)}</strong>
            </div>
          </div>
          <div class="gram-armadilha-motivo">
            <strong>${I18n.t('gram_fase5_porque')}</strong> ${this._formatarPergunta(a.motivo)}
          </div>
        </div>`;
    }
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label">${I18n.t('gram_fase5_label')}</div>
        <div style="padding: 0.85rem 1.25rem 0.4rem; font-size: 0.9rem; color: #666; line-height: 1.5;">${I18n.t('gram_fase5_sub')}</div>
        <div class="gram-armadilhas-lista">${cards}</div>
      </div>`;
  },

  // ── Painel de consulta rápida acima dos exercícios ──
  _htmlTabelaVisual(u) {
    if (!u.tabela_visual && !u.tecnica) return '';
    return `<details class="gram-tabela-visual">
      <summary>📋 Consulta Rápida da Regra (clique se precisar lembrar durante os exercícios)</summary>
      <div class="gram-tabela-conteudo">
        ${u.tabela_visual || ''}
        ${u.tecnica ? `<div style="margin-top:0.85rem;padding-top:0.85rem;border-top:1px dashed #d9cbb8">${this._formatarTeoria(u.tecnica)}</div>` : ''}
      </div>
    </details>`;
  },

  // ── Camadas Estruturais NMA (Agora sempre integradas na Etapa 1) ──
  _htmlAlerta(u) {
    if (!u.alerta) return '';
    return `<div class="gram-alerta">💬 ${this._formatarPergunta(u.alerta)}</div>`;
  },

  _htmlInventario(u) {
    if (!u.inventario || !u.inventario.length) return '';
    const items = u.inventario.map(i => `<li>${this._formatarPergunta(i)}</li>`).join('');
    return `<div class="gram-camada-bloco"><div class="gram-camada-label">${I18n.t('gram_inventario_label')}</div><ol class="gram-inventario">${items}</ol></div>`;
  },

  _htmlDefinicao(u) {
    if (!u.definicao) return '';
    const d = u.definicao;
    if (!d.fenomeno && !d.causa && !d.conceito) return '';
    return `<div class="gram-camada-bloco">
      <div class="gram-camada-label">${I18n.t('gram_definicao_label')}</div>
      <div class="gram-definicao-row">
        ${d.fenomeno ? `<div class="gram-def-card gram-def-fenomeno"><div class="gram-def-label">${I18n.t('gram_def_veja')}</div><div class="gram-def-corpo">${this._formatarPergunta(d.fenomeno)}</div></div>` : ''}
        ${d.causa    ? `<div class="gram-def-card gram-def-causa"><div class="gram-def-label">${I18n.t('gram_def_pense')}</div><div class="gram-def-corpo">${this._formatarPergunta(d.causa)}</div></div>` : ''}
        ${d.conceito ? `<div class="gram-def-card gram-def-conceito"><div class="gram-def-label">${I18n.t('gram_def_entenda')}</div><div class="gram-def-corpo">${this._formatarPergunta(d.conceito)}</div></div>` : ''}
      </div>
    </div>`;
  },

  _htmlTecnica(u) {
    if (!u.tecnica) return '';
    const ft = this._formatarTeoria(u.tecnica);
    return `<div class="gram-camada-bloco gram-tecnica"><div class="gram-camada-label">${I18n.t('gram_tecnica_label')}</div><div class="gram-tecnica-corpo">${ft}</div></div>`;
  },

  _htmlPonte(u) {
    if (!u.ponte) return '';
    return `<div class="gram-camada-bloco gram-ponte"><div class="gram-camada-label">${I18n.t('gram_ponte_label')}</div><div class="gram-ponte-corpo">${this._formatarTeoria(u.ponte)}</div></div>`;
  },

  _htmlCoda(u) {
    if (!u.coda) return '';
    return `<div class="gram-coda">💡 ${this._formatarPergunta(u.coda)}</div>`;
  }
};
