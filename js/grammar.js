// ============================================================
// grammar.js — Grammatica Italiana — Design Premium v2
// Parla e Scrivi — 30 capítulos
// Tipos: "escolha" (múltipla escolha) | "revelar" (blur-reveal)
// XP: +5 por acerto · +50 bônus por capítulo concluído
// ============================================================

const Grammatica = {
  dados: null,
  moduloAtual: null,
  unidadeAtual: null,
  exIndex: 0,
  acertos: 0,
  respondida: false,
  _adminMods: new Set(),   // módulos desbloqueados temporariamente pelo admin

  // ─────────────────────────────────────────────────────────
  // Carregar dados
  // ─────────────────────────────────────────────────────────
  async carregar() {
    if (this.dados) return;
    try {
      const r = await fetch('data/grammar.json');
      if (!r.ok) throw new Error('grammar.json não encontrado');
      this.dados = await r.json();
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
    if (this.unidadeAtual && this.exIndex > 0 && this.exIndex < total) {
      if (!confirm('Vuoi tornare? Il progresso di questa lezione andrà perso.')) return;
    }
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

      const totalEx   = mod.lezioni.reduce((s, u) => s + u.exercicios.length, 0);
      const completas = mod.lezioni.filter(u => completadas.includes(u.id)).length;
      const pct       = totalUnid > 0 ? Math.round((completas / totalUnid) * 100) : 0;

      // Module banner (clicável para colapsar/expandir)
      const adminDesbloqueado = this._adminMods.has(mod.id);
      html += `<div class="gram-nivel-banner" data-nivel="${mod.id}" style="background:${mod.cor};cursor:pointer;user-select:none" onclick="Grammatica.toggleNivel('${mod.id}')">`;
      html += `<div style="display:flex;align-items:center;justify-content:space-between">`;
      html += `<div class="gram-nivel-badge-txt">${mod.id}${adminDesbloqueado ? ' &nbsp;🔓 Admin' : ''}</div>`;
      html += `<span class="gram-nivel-toggle-icone" style="font-size:1.1rem;opacity:0.8;transition:transform 0.2s">▾</span>`;
      html += `</div>`;
      html += `<div class="gram-nivel-nome">${mod.nome}</div>`;
      html += `<div class="gram-nivel-info">${completas}/${totalUnid} completi &middot; ${totalEx} esercizi</div>`;
      html += `<div class="gram-nivel-barra"><div style="width:${pct}%"></div></div>`;
      html += '</div>';

      // Grid of lezione cards (id para colapso)
      html += `<div class="gram-lezioni-grid" id="gram-grid-${mod.id}">`;
      for (const u of mod.lezioni) {
        const feita = completadas.includes(u.id);
        const nEx = u.exercicios.length;
        html += `<button class="gram-lez-card${feita ? ' feita' : ''}" onclick="Grammatica.abrirUnidade('${mod.id}','${u.id}')">`;
        html += `<span class="gram-lez-icon">${feita ? '✅' : '📘'}</span>`;
        html += `<span class="gram-lez-info">`;
        html += `<span class="gram-lez-num-label">${u.num}</span>`;
        html += `<span class="gram-lez-titulo">${u.titulo}</span>`;
        html += `<span class="gram-lez-meta">${nEx} esercizi</span>`;
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
        html += `<button class="gram-locked-pill" onclick="Grammatica.pedirSenhaAdmin('${mod.id}')" title="Accesso amministratore">`;
        html += `<span class="gram-locked-pill-icon">🔒</span>`;
        html += `<span class="gram-locked-pill-info">`;
        html += `<span class="gram-locked-pill-id">${mod.id}</span>`;
        html += `<span class="gram-locked-pill-nome">${mod.nome}</span>`;
        html += `<span class="gram-locked-pill-req">Richiede Livello ${mod.nivel_minimo}</span>`;
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
    // Remove modal anterior se existir
    const old = document.getElementById('gram-admin-modal');
    if (old) old.remove();

    const mod = this.dados.moduli.find(m => m.id === modId);
    const nome = mod ? mod.nome : modId;

    const overlay = document.createElement('div');
    overlay.id = 'gram-admin-modal';
    overlay.className = 'gram-admin-overlay';
    overlay.innerHTML = `
      <div class="gram-admin-box" role="dialog" aria-modal="true">
        <div class="gram-admin-icon">🔐</div>
        <div class="gram-admin-titulo">Accesso Amministratore</div>
        <div class="gram-admin-subtit">${nome}</div>
        <input
          id="gram-admin-input"
          class="gram-admin-input"
          type="password"
          placeholder="Inserisci la password"
          maxlength="20"
          autocomplete="off"
          onkeydown="if(event.key==='Enter') Grammatica._confirmarSenha('${modId}'); if(event.key==='Escape') Grammatica._fecharModal()"
        />
        <div id="gram-admin-erro" class="gram-admin-erro" style="display:none">Password errata. Riprova.</div>
        <div class="gram-admin-btns">
          <button class="gram-admin-btn-cancel" onclick="Grammatica._fecharModal()">Annulla</button>
          <button class="gram-admin-btn-ok" onclick="Grammatica._confirmarSenha('${modId}')">Conferma</button>
        </div>
      </div>`;

    // Fechar ao clicar fora
    overlay.addEventListener('click', e => { if (e.target === overlay) this._fecharModal(); });
    document.body.appendChild(overlay);

    // Foco automático no input
    requestAnimationFrame(() => {
      const inp = document.getElementById('gram-admin-input');
      if (inp) inp.focus();
    });
  },

  _fecharModal() {
    const m = document.getElementById('gram-admin-modal');
    if (m) { m.classList.add('gram-admin-saindo'); setTimeout(() => m.remove(), 220); }
  },

  _confirmarSenha(modId) {
    const inp = document.getElementById('gram-admin-input');
    const erro = document.getElementById('gram-admin-erro');
    if (!inp) return;

    if (inp.value === '2012') {
      this._adminMods.add(modId);
      this._fecharModal();
      // Re-renderiza o seletor com o módulo desbloqueado
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

  // ─────────────────────────────────────────────────────────
  // Abrir lição
  // ─────────────────────────────────────────────────────────
  // ── Colapsa / expande o grid de lições de um nível ───────────
  toggleNivel(id) {
    const grid   = document.getElementById(`gram-grid-${id}`);
    const banner = document.querySelector(`.gram-nivel-banner[data-nivel="${id}"]`);
    if (!grid) return;
    const recolhido = grid.classList.toggle('recolhido');
    const seta = banner?.querySelector('.gram-nivel-toggle-icone');
    if (seta) seta.style.transform = recolhido ? 'rotate(-90deg)' : 'rotate(0deg)';
  },

  abrirUnidade(moduloId, unidadeId) {
    const mod  = this.dados.moduli.find(m => m.id === moduloId);
    if (!mod) return;
    const unid = mod.lezioni.find(u => u.id === unidadeId);
    if (!unid) return;

    this.moduloAtual  = mod;
    this.unidadeAtual = unid;
    this.exIndex      = 0;
    this.acertos      = 0;
    this.respondida   = false;

    const c = document.getElementById('grammatica-container');
    if (c) {
      c.innerHTML = this._htmlUnidade(unid);
      window.scrollTo(0, 0);
    }
  },

  // ─────────────────────────────────────────────────────────
  // HTML completo da lição
  // ─────────────────────────────────────────────────────────
  _htmlUnidade(u) {
    const mod = this.moduloAtual;

    let html = '<div class="gram-lesson-layout">';

    // Nav
    html += '<div class="gram-lesson-nav">';
    html += `<button class="gram-btn-back" onclick="Grammatica.voltarSeletor()">‹ Tutti i moduli</button>`;
    html += `<div class="gram-lesson-breadcrumb"><span>${mod.id}</span> › <span>${u.num}</span></div>`;
    html += '</div>';

    // Cabeçalho
    html += '<div class="gram-lesson-header">';
    html += `<div class="gram-lesson-eyebrow">${u.num}</div>`;
    html += `<h2 class="gram-lesson-title">${u.titulo}</h2>`;
    if (u.subtitulo) html += `<p class="gram-lesson-subtitle">${u.subtitulo}</p>`;
    html += '</div>';

    // 📋 Tabela de consulta rápida (colapsável) para uso durante os exercícios
    html += this._htmlTabelaVisual(u);

    // ✏️ Exercícios (MOVIDO PARA O TOPO)
    html += '<div id="gram-ex-area">';
    html += this._htmlExercicio();
    html += '</div>';

    // 📖 Teoria estruturada (5 Fases Didáticas)
    html += '<div class="gram-card gram-teoria-card">';
    html += '<div class="gram-card-header"><span>📖</span> Teoria e Prática da Lição</div>';
    html += this._htmlFases(u);
    html += '</div>';

    html += '</div>'; // lesson-layout
    return html;
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

    // A explicação só aparece no feedback (pós-resposta) — nunca antes,
    // pois entregaria a resposta. A dica opcional (campo dica) continua
    // visível antes para digitar, mas fica fora deste bloco.
    // (removida renderização pre-answer de explicacao para todos os tipos)

    // Corpo do exercício
    if (ex.tipo === 'escolha') {
      html += this._htmlEscolha(ex);
    } else if (ex.tipo === 'digitar') {
      html += this._htmlDigitar(ex);
    } else {
      html += this._htmlRivelar(ex);
    }

    // Feedback (oculto)
    html += '<div class="gram-ex-feedback" id="gram-feedback"></div>';

    // Ações (ocultas até responder)
    html += '<div class="gram-ex-actions" id="gram-actions" style="display:none">';
    if (ex.tipo === 'revelar') {
      html += '<button class="gram-btn-errei"  onclick="Grammatica.proximoExercicio()">❌ Errei</button>';
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
    // Divide a resposta em palavras individuais com blur
    const partes = ex.resposta.split(/(\s+)/);
    const spans  = partes.map(p => {
      if (/^\s+$/.test(p)) return p; // espaços mantidos
      return `<span class="gram-word-blur" onclick="Grammatica.togglePalavra(this)">${p}</span>`;
    }).join('');

    let html = '<div class="gram-revelar-area">';
    const hint = I18n.idioma === 'it'
      ? '👆 Clicca sulle parole per rivelare, o clicca su "Vedi risposta"'
      : '👆 Clique nas palavras para revelar, ou clique em "Ver resposta"';
    html += `<div class="gram-revelar-hint">${hint}</div>`;
    html += `<div class="gram-risposta-container" id="gram-risposta">${spans}</div>`;
    html += '<div class="gram-revelar-actions">';
    html += '<button class="gram-btn-rivela-tutto" onclick="Grammatica.revelarTudo()">Ver resposta</button>';
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
    document.getElementById('gram-feedback').innerHTML = '';
    document.getElementById('gram-actions').style.display = 'none';
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

  _afterReveal() {
    if (this.respondida) return;
    this.respondida = true;
    const ex = this.unidadeAtual.exercicios[this.exIndex];
    const fb = document.getElementById('gram-feedback');
    if (fb && ex.explicacao) {
      fb.innerHTML = `<div class="gram-feedback-info">💡 <strong>${I18n.t('gram_por_que')}</strong> ${ex.explicacao}</div>`;
    }
    const actions = document.getElementById('gram-actions');
    if (actions) actions.style.display = 'flex';
  },

  // Compatibilidade com código legado
  revelarResposta() { this.revelarTudo(); },

  // ─────────────────────────────────────────────────────────
  // Responder múltipla escolha
  // ─────────────────────────────────────────────────────────
  responder(indice) {
    if (this.respondida) return;
    this.respondida = true;

    const ex      = this.unidadeAtual.exercicios[this.exIndex];
    const correto = (indice === ex.resposta);

    // Colorir opções
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

    // Feedback
    const fb = document.getElementById('gram-feedback');
    if (fb) {
      fb.innerHTML = correto
        ? `<div class="gram-feedback-correct">✅ <strong>${I18n.t('gram_correto')}</strong> ${ex.explicacao}</div>`
        : `<div class="gram-feedback-wrong">❌ <strong>${I18n.t('gram_errado')}</strong> ${ex.explicacao}</div>`;
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
    const correta  = (ex.resposta || '').trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    const variantes = (ex.variantes || []).map(v =>
      v.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '')
    );
    const correto = digitado === correta || variantes.includes(digitado);

    this.respondida = true;
    input.disabled = true;
    input.classList.add(correto ? 'digitar-correto' : 'digitar-errado');

    const fb = document.getElementById('gram-feedback');
    if (fb) {
      fb.innerHTML = correto
        ? `<div class="gram-feedback-correct">✅ <strong>${I18n.t('gram_correto')}</strong>${ex.explicacao ? ' ' + ex.explicacao : ''}</div>`
        : `<div class="gram-feedback-wrong">❌ <strong>${I18n.t('gram_errado')}</strong> ${I18n.t('gram_resposta_era')} <strong>${ex.resposta}</strong>.${ex.explicacao ? ' ' + ex.explicacao : ''}</div>`;
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
    // Animação de saída
    area.style.transition = 'opacity 0.15s ease, transform 0.15s ease';
    area.style.opacity = '0';
    area.style.transform = 'translateY(8px)';
    setTimeout(() => {
      area.innerHTML = this.exIndex >= this.unidadeAtual.exercicios.length
        ? this._htmlResultado()
        : this._htmlExercicio();
      // Animação de entrada
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

    let emoji = '📚', msg = 'Continua a studiare — ci riesci!';
    if      (pct === 100) { emoji = '🌟'; msg = 'Perfetto! Nessun errore!'; }
    else if (pct >= 80)   { emoji = '🎉'; msg = 'Ottimo lavoro! Quasi perfetto!'; }
    else if (pct >= 60)   { emoji = '💪'; msg = 'Bene! Continua così!'; }

    // Próxima lição
    const unids = this.moduloAtual.lezioni;
    const idx   = unids.findIndex(u => u.id === this.unidadeAtual.id);
    let proxBtn = '';
    if (idx >= 0 && idx < unids.length - 1) {
      const prox = unids[idx + 1];
      proxBtn = `<button class="gram-btn-next" onclick="Grammatica.abrirUnidade('${this.moduloAtual.id}','${prox.id}')">Prossimo capitolo →</button>`;
    }

    return `
      <div class="gram-card gram-resultado">
        <div class="gram-res-emoji">${emoji}</div>
        <div class="gram-res-title">Capitolo Completato!</div>
        <div class="gram-res-score">${acertos}<span>/${total}</span></div>
        <div class="gram-res-pct">${pct}% corretto</div>
        ${!jaFeita ? `<div class="gram-res-xp">+${bonus} XP bônus 🏆</div>` : ''}
        <div class="gram-res-msg">${msg}</div>
        <div class="gram-res-actions">
          <button class="gram-btn-secondary" onclick="Grammatica.abrirUnidade('${this.moduloAtual.id}','${this.unidadeAtual.id}')">🔄 Ripeti</button>
          ${proxBtn}
          <button class="gram-btn-secondary" onclick="Grammatica.voltarSeletor()">‹ Tutti i moduli</button>
        </div>
      </div>`;
  },

  // ─────────────────────────────────────────────────────────
  // Formatação da teoria (Markdown simples → HTML)
  // Suporta:
  //   • **bold** / *italic*
  //   • pipe tables simples
  //   • HTML tables raw (protegidas contra reprocessamento)
  // ─────────────────────────────────────────────────────────
  _formatarTeoria(texto) {
    if (!texto) return '';

    // 0. Proteger HTML tables existentes (rowspan/colspan/etc.)
    //    Substituímos por placeholders antes de qualquer processamento.
    const htmlTables = [];
    texto = texto.replace(/<table[\s\S]*?<\/table>/gi, (m) => {
      htmlTables.push(m);
      return `\x00T${htmlTables.length - 1}\x00`;
    });

    // 1. Bold e italic
    texto = texto
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // 2. Linhas pipe → <tr> (separadores |---|---| viram vazio)
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

    // 3. Agrupa <tr> consecutivos em <table class="gram-table">
    texto = texto.replace(/((<tr>[\s\S]*?<\/tr>\n*)+)/g,
      '<table class="gram-table">$1</table>');

    // 4. Remove \n dentro de <table> simples (geradas por pipe)
    texto = texto.replace(/(<table[^>]*>)([\s\S]*?)(<\/table>)/g,
      (_, open, inner, close) => open + inner.replace(/\n+/g, '') + close);

    // 5. Normaliza \n ao redor de <table>
    texto = texto.replace(/\n+(<table)/g, '\n$1');
    texto = texto.replace(/(<\/table>)\n+/g, '$1\n');

    // 6. Parágrafo e quebras de linha
    texto = texto.replace(/\n{2,}/g, '\n\n');
    texto = texto.replace(/\n\n/g, '</p><p>');
    texto = texto.replace(/\n/g, '<br>');

    // 7. Limpeza de artefatos ao redor de tabelas
    texto = texto.replace(/<p>\s*<\/p>/g, '');
    texto = texto.replace(/(<br>)+(<table)/g, '$2');
    texto = texto.replace(/(<\/table>)(<br>)+/g, '$1');
    texto = texto.replace(/<p>(<table)/g, '$1');
    texto = texto.replace(/(<\/table>)<\/p>/g, '$1');

    // 8. Restaurar HTML tables protegidas (com suas classes e rowspan/colspan)
    htmlTables.forEach((t, i) => {
      texto = texto.replace(`\x00T${i}\x00`, t);
    });

    // 9. Caixas de destaque automáticas (Regola / Attenzione / Nota)
    // Detecta parágrafos que começam com <strong>Regola</strong> ou similar
    texto = texto.replace(
      /(<p>)(<strong>(?:Regola|Nota bene|Nota)[^<]*:<\/strong>)/gi,
      '<p class="gram-regola">$2'
    );
    texto = texto.replace(
      /(<p>)(<strong>(?:Attenzione|Importante|Achtung)[^<]*!?:?<\/strong>)/gi,
      '<p class="gram-attenzione">$2'
    );

    // 10. Caixa de diálogo — detecta <p> com múltiplos <strong>Nome:</strong> seguidos de texto
    texto = texto.replace(
      /<p>(<strong>[A-ZÀÈÉÌÒÙ][a-zàèéìòùA-Z\s]+:<\/strong>[^<p]{0,300}<br>[^<p]{0,50}<strong>[A-ZÀÈÉÌÒÙ])/g,
      '<p class="gram-dialogo-box">$1'
    );

    return texto;
  },

  // ─────────────────────────────────────────────────────────
  // Formata texto de pergunta/opção (bold + italic)
  // ─────────────────────────────────────────────────────────
  _formatarPergunta(texto) {
    if (!texto) return '';
    return String(texto)
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*]+)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  },

  // ─────────────────────────────────────────────────────────
  // Método NMA: orquestra as camadas pedagógicas
  // Se a unidade tiver os novos campos, renderiza as camadas.
  // Caso contrário, faz fallback para `teoria` + `exemplos` legados.
  // ─────────────────────────────────────────────────────────
  _htmlFases(u) {
    const hasNovasFases = u.observacao_cards || u.armadilhas;
    if (!hasNovasFases) {
      // Fallback legado / NMA padrão de 7 camadas
      return this._htmlCamadasLegado(u);
    }

    let h = '<div class="gram-camadas">';
    h += this._htmlFase1Ancoragem(u);
    h += this._htmlFase2Observacao(u);
    h += this._htmlFase3Tabela(u);
    h += this._htmlFase4Exemplos(u);
    h += this._htmlFase5Armadilhas(u);
    h += this._htmlCoda(u);
    h += '</div>';
    return h;
  },

  _htmlCamadasLegado(u) {
    const hasNovos = u.alerta || u.inventario || u.definicao || u.tecnica || u.exemplos_prc || u.ponte || u.coda;
    if (!hasNovos) {
      let h = `<div class="gram-teoria-corpo">${this._formatarTeoria(u.teoria)}</div>`;
      if (u.exemplos && u.exemplos.length) {
        h += '<div class="gram-esempi-lista">';
        for (const ex of u.exemplos) {
          const it = typeof ex === 'string' ? ex : (ex.it || '');
          const pt = typeof ex === 'string' ? '' : (ex.pt || '');
          const safe = it.replace(/'/g, "\\'");
          h += `<div class="gram-esempio"><div class="gram-esempio-it" onclick="App.pronunciar('${safe}')">🔊 ${it}</div>`;
          if (pt) h += `<div class="gram-esempio-pt">${pt}</div>`;
          h += '</div>';
        }
        h += '</div>';
      }
      return h;
    }

    let h = '<div class="gram-camadas">';
    h += this._htmlAlerta(u);
    h += this._htmlInventario(u);
    h += this._htmlDefinicao(u);
    h += this._htmlTecnica(u);
    h += this._htmlExemplosPRCLegado(u);
    h += this._htmlPonte(u);
    h += this._htmlCoda(u);
    h += '</div>';
    return h;
  },

  // ─── FASE 1: Ancoragem ───
  _htmlFase1Ancoragem(u) {
    if (!u.alerta) return '';
    return `<div class="gram-alerta">💬 <strong>${I18n.t('gram_por_que_importa')}</strong><br>${this._formatarPergunta(u.alerta)}</div>`;
  },

  // ─── FASE 2: Observação (Flip Cards Clicáveis) ───
  _htmlFase2Observacao(u) {
    if (!u.observacao_cards || !u.observacao_cards.length) return '';
    let cards = '';
    for (let i = 0; i < u.observacao_cards.length; i++) {
      const c = u.observacao_cards[i];
      cards += `
        <div class="gram-flip-card" onclick="this.classList.toggle('flipped')">
          <div class="gram-flip-card-inner">
            <div class="gram-flip-card-front">
              <div class="gfc-it">${c.italiano}</div>
              <div class="gfc-pt">${c.traducao}</div>
              <div class="gfc-badge">${c.genero}</div>
              <div class="gfc-click">${I18n.idioma === 'it' ? 'Clicca per rivelare 👆' : 'Clique para revelar 👆'}</div>
            </div>
            <div class="gram-flip-card-back">
              <div class="gfc-titulo-regra">O Padrão:</div>
              <div class="gfc-regra-txt">${c.motivo}</div>
            </div>
          </div>
        </div>`;
    }
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label">${I18n.t('gram_fase2_label')}</div>
        <div style="padding: 1rem 1.25rem 0.5rem; font-size: 0.9rem; color: #666; line-height: 1.5;">${I18n.t('gram_fase2_sub')}</div>
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

  // ─── FASE 4: Exemplos P/R/C (Clicáveis / Colapsáveis) ───
  _htmlFase4Exemplos(u) {
    if (!u.exemplos_prc || !u.exemplos_prc.length) return '';
    let rows = '';
    for (let i = 0; i < u.exemplos_prc.length; i++) {
      const e = u.exemplos_prc[i];
      const safe = (e.oracao || '').replace(/'/g, "\\'");
      rows += `
        <div class="gram-prc-expandivel" id="gram-prc-card-${i}">
          <div class="gram-prc-topo" onclick="this.parentElement.classList.toggle('aberto')">
            <span class="gram-prc-it">🔊 <em>${e.oracao || ''}</em></span>
            <span class="gram-prc-btn-expandir">${I18n.t('gram_fase4_ver_detalhes')}</span>
          </div>
          <div class="gram-prc-conteudo-oculto">
            <div class="gram-prc-pq"><span class="gram-prc-tag">${I18n.t('gram_fase4_prc_pergunta')}</span> ${e.pergunta || ''}</div>
            <div class="gram-prc-pq"><span class="gram-prc-tag">${I18n.t('gram_fase4_prc_resposta')}</span> ${e.resposta || ''}</div>
            <div class="gram-prc-conclusao"><span class="gram-prc-tag gram-prc-tag-c">${I18n.t('gram_fase4_prc_conclusao')}</span> <strong>${e.conclusao || ''}</strong></div>
          </div>
        </div>`;
    }
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label">${I18n.t('gram_fase4_label')}</div>
        <div style="padding: 1rem 1.25rem 0.5rem; font-size: 0.9rem; color: #666; line-height: 1.5;">${I18n.t('gram_fase4_sub')}</div>
        <div class="gram-prc-lista">${rows}</div>
      </div>`;
  },

  // ─── FASE 5: Armadilhas (Lado a Lado Errado ✗ vs Certo ✓) ───
  _htmlFase5Armadilhas(u) {
    if (!u.armadilhas || !u.armadilhas.length) return '';
    let cards = '';
    for (let i = 0; i < u.armadilhas.length; i++) {
      const a = u.armadilhas[i];
      cards += `
        <div class="gram-armadilha-row">
          <div class="gram-armadilha-col gram-arm-errada">
            <span class="gram-arm-icon">✗</span>
            <div class="gram-arm-texto">
              <span class="gram-arm-lbl">${I18n.t('gram_arm_errado')}</span>
              <strong>${a.errado}</strong>
            </div>
          </div>
          <div class="gram-armadilha-col gram-arm-certa">
            <span class="gram-arm-icon">✓</span>
            <div class="gram-arm-texto">
              <span class="gram-arm-lbl">${I18n.t('gram_arm_certo')}</span>
              <strong>${a.certo}</strong>
            </div>
          </div>
          <div class="gram-armadilha-motivo">
            <strong>${I18n.t('gram_fase5_porque')}</strong> ${a.motivo}
          </div>
        </div>`;
    }
    return `
      <div class="gram-camada-bloco">
        <div class="gram-camada-label">${I18n.t('gram_fase5_label')}</div>
        <div style="padding: 1rem 1.25rem 0.5rem; font-size: 0.9rem; color: #666; line-height: 1.5;">${I18n.t('gram_fase5_sub')}</div>
        <div class="gram-armadilhas-lista">${cards}</div>
      </div>`;
  },

  // ── Tabela colapsável acima dos exercícios ──
  _htmlTabelaVisual(u) {
    if (!u.tabela_visual) return '';
    return `<details class="gram-tabela-visual">
      <summary>📋 Ver tabela de consulta (use durante os exercícios)</summary>
      <div class="gram-tabela-conteudo">${u.tabela_visual}</div>
    </details>`;
  },

  // ── Camadas Legadas NMA ──
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

  _htmlExemplosPRCLegado(u) {
    if (!u.exemplos_prc || !u.exemplos_prc.length) return '';
    let rows = '';
    for (const e of u.exemplos_prc) {
      const safe = (e.oracao || '').replace(/'/g, "\\'");
      rows += `<div class="gram-prc-row">
        <div class="gram-prc-oracao" onclick="App.pronunciar('${safe}')">🔊 <em>${e.oracao || ''}</em></div>
        <div class="gram-prc-pq"><span class="gram-prc-tag">P</span>${this._formatarPergunta(e.pergunta || '')}</div>
        <div class="gram-prc-pq"><span class="gram-prc-tag">R</span>${this._formatarPergunta(e.resposta || '')}</div>
        <div class="gram-prc-conclusao"><span class="gram-prc-tag gram-prc-tag-c">C</span><strong>${this._formatarPergunta(e.conclusao || '')}</strong></div>
      </div>`;
    }
    return `<div class="gram-camada-bloco"><div class="gram-camada-label">${I18n.t('gram_exemplos_prc_label')}</div><div class="gram-prc-lista">${rows}</div></div>`;
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
