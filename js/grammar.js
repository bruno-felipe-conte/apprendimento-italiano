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

  // ─────────────────────────────────────────────────────────
  // Seletor de módulos e lições
  // ─────────────────────────────────────────────────────────
  _htmlSeletor() {
    if (!this.dados || !this.dados.moduli.length)
      return '<p class="gram-empty">Conteúdo não disponível.</p>';

    const nivel = App.estado.progresso?.nivel || 1;
    const completadas = App.estado.progresso?.grammatica_completadas || [];

    let html = '<div class="gram-seletor">';

    for (const mod of this.dados.moduli) {
      const bloqueado = nivel < mod.nivel_minimo && !this._adminMods.has(mod.id);
      const totalUnid = mod.unidades.length;
      if (bloqueado || totalUnid === 0) continue; // skip locked/empty modules

      const totalEx   = mod.unidades.reduce((s, u) => s + u.exercicios.length, 0);
      const completas = mod.unidades.filter(u => completadas.includes(u.id)).length;
      const pct       = totalUnid > 0 ? Math.round((completas / totalUnid) * 100) : 0;

      // Module banner
      const adminDesbloqueado = this._adminMods.has(mod.id);
      html += `<div class="gram-nivel-banner" style="background:${mod.cor}">`;
      html += `<div class="gram-nivel-badge-txt">${mod.id}${adminDesbloqueado ? ' &nbsp;🔓 Admin' : ''}</div>`;
      html += `<div class="gram-nivel-nome">${mod.nome}</div>`;
      html += `<div class="gram-nivel-info">${completas}/${totalUnid} completi &middot; ${totalEx} esercizi</div>`;
      html += `<div class="gram-nivel-barra"><div style="width:${pct}%"></div></div>`;
      html += '</div>';

      // Grid of lezione cards
      html += '<div class="gram-lezioni-grid">';
      for (const u of mod.unidades) {
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
    const bloqueados = this.dados.moduli.filter(m => nivel < m.nivel_minimo && !this._adminMods.has(m.id) && m.unidades.length > 0);
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
  abrirUnidade(moduloId, unidadeId) {
    const mod  = this.dados.moduli.find(m => m.id === moduloId);
    if (!mod) return;
    const unid = mod.unidades.find(u => u.id === unidadeId);
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
    html += `<button class="gram-btn-back" onclick="Grammatica.renderizarSeletor()">‹ Tutti i moduli</button>`;
    html += `<div class="gram-lesson-breadcrumb"><span>${mod.id}</span> › <span>${u.num}</span></div>`;
    html += '</div>';

    // Cabeçalho
    html += '<div class="gram-lesson-header">';
    html += `<div class="gram-lesson-eyebrow">${u.num}</div>`;
    html += `<h2 class="gram-lesson-title">${u.titulo}</h2>`;
    if (u.subtitulo) html += `<p class="gram-lesson-subtitle">${u.subtitulo}</p>`;
    html += '</div>';

    // Card: Grammatica (teoria)
    html += '<div class="gram-card gram-teoria-card">';
    html += '<div class="gram-card-header"><span>📖</span> Grammatica</div>';
    html += `<div class="gram-teoria-corpo">${this._formatarTeoria(u.teoria)}</div>`;
    html += '</div>';

    // Card: Esempi
    if (u.exemplos && u.exemplos.length) {
      html += '<div class="gram-card">';
      html += '<div class="gram-card-header"><span>✍️</span> Esempi</div>';
      html += '<div class="gram-esempi-lista">';
      for (const ex of u.exemplos) {
        const it = typeof ex === 'string' ? ex : (ex.it || '');
        const pt = typeof ex === 'string' ? '' : (ex.pt || '');
        const safe = it.replace(/'/g, "\\'");
        html += '<div class="gram-esempio">';
        html += `<div class="gram-esempio-it" onclick="App.pronunciar('${safe}')">🔊 ${it}</div>`;
        if (pt) html += `<div class="gram-esempio-pt">${pt}</div>`;
        html += '</div>';
      }
      html += '</div></div>';
    }

    // Área de exercícios
    html += '<div id="gram-ex-area">';
    html += this._htmlExercicio();
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

    // Progresso
    html += '<div class="gram-ex-header">';
    html += `<div class="gram-ex-progress-label">Esercizio ${this.exIndex + 1} / ${total}</div>`;
    html += `<div class="gram-ex-progress-bar"><div class="gram-ex-progress-fill" style="width:${pct}%"></div></div>`;
    html += '</div>';

    // Pergunta
    html += `<div class="gram-ex-question">${qHtml}</div>`;

    // Corpo do exercício
    if (ex.tipo === 'escolha') {
      html += this._htmlEscolha(ex);
    } else {
      html += this._htmlRivelar(ex);
    }

    // Feedback (oculto)
    html += '<div class="gram-ex-feedback" id="gram-feedback"></div>';

    // Ações (ocultas até responder)
    html += '<div class="gram-ex-actions" id="gram-actions" style="display:none">';
    if (ex.tipo === 'revelar') {
      html += '<button class="gram-btn-errei"  onclick="Grammatica.proximoExercicio()">❌ Sbagliato</button>';
      html += '<button class="gram-btn-acertei" onclick="Grammatica.marcarAcerto()">✅ Ho indovinato</button>';
    } else {
      html += '<button class="gram-btn-next" onclick="Grammatica.proximoExercicio()">Prossimo →</button>';
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

  // ─── Blur-reveal ───
  _htmlRivelar(ex) {
    // Divide a resposta em palavras individuais com blur
    const partes = ex.resposta.split(/(\s+)/);
    const spans  = partes.map(p => {
      if (/^\s+$/.test(p)) return p; // espaços mantidos
      return `<span class="gram-word-blur" onclick="Grammatica.togglePalavra(this)">${p}</span>`;
    }).join('');

    let html = '<div class="gram-revelar-area">';
    html += '<div class="gram-revelar-hint">👆 Clicca sulle parole per rivelarle, oppure usa i pulsanti</div>';
    html += `<div class="gram-risposta-container" id="gram-risposta">${spans}</div>`;
    html += '<div class="gram-revelar-actions">';
    html += '<button class="gram-btn-rivela-tutto" onclick="Grammatica.revelarTudo()">Rivela tutto</button>';
    html += '<button class="gram-btn-nascondi" id="gram-btn-nascondi" onclick="Grammatica.nasconderTudo()">Nascondi</button>';
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
      fb.innerHTML = `<div class="gram-feedback-info">💡 <strong>Spiegazione:</strong> ${ex.explicacao}</div>`;
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
        ? `<div class="gram-feedback-correct">✅ <strong>Corretto!</strong> ${ex.explicacao}</div>`
        : `<div class="gram-feedback-wrong">❌ <strong>Sbagliato.</strong> ${ex.explicacao}</div>`;
    }

    const actions = document.getElementById('gram-actions');
    if (actions) actions.style.display = 'flex';

    if (correto) { this.acertos++; App.ganharXP(5); }
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
    area.innerHTML = this.exIndex >= this.unidadeAtual.exercicios.length
      ? this._htmlResultado()
      : this._htmlExercicio();
    area.scrollIntoView({ behavior: 'smooth', block: 'start' });
  },

  // ─────────────────────────────────────────────────────────
  // Tela de resultado
  // ─────────────────────────────────────────────────────────
  _htmlResultado() {
    const total   = this.unidadeAtual.exercicios.length;
    const acertos = this.acertos;
    const pct     = total > 0 ? Math.round((acertos / total) * 100) : 0;
    const bonus   = 50;

    const completadas = App.estado.progresso.grammatica_completadas || [];
    const jaFeita     = completadas.includes(this.unidadeAtual.id);
    if (!jaFeita) {
      completadas.push(this.unidadeAtual.id);
      App.estado.progresso.grammatica_completadas = completadas;
      App.salvarProgresso();
      App.ganharXP(bonus);
      App.notificar(`🏆 Capitolo completato! +${bonus} XP`, 'successo');
    }

    if (typeof Calor !== 'undefined') Calor.registrar(total);

    let emoji = '📚', msg = 'Continua a studiare — ci riesci!';
    if      (pct === 100) { emoji = '🌟'; msg = 'Perfetto! Nessun errore!'; }
    else if (pct >= 80)   { emoji = '🎉'; msg = 'Ottimo lavoro! Quasi perfetto!'; }
    else if (pct >= 60)   { emoji = '💪'; msg = 'Bene! Continua così!'; }

    // Próxima lição
    const unids = this.moduloAtual.unidades;
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
          <button class="gram-btn-secondary" onclick="Grammatica.renderizarSeletor()">‹ Tutti i moduli</button>
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
      .replace(/\*([^*]+)\*/g, '<em>$1</em>');
  }
};
