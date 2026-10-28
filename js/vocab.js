// ============================================================
// vocab.js — Vocabulary browser with search and filters
// ============================================================

const Vocab = {
  filtroTexto: '',
  filtroTemplo: '',
  filtroCategoria: '',
  filtroOrigem: '',   // '' | 'custom' | 'nativo' | 'top1000'
  filtroDificeis:   false,
  filtroFavoritos:  false,
  blurColuna: null,   // null | 'pt' | 'it'
  modoCompacto: false,
  _limiteRender: 80,
  top1000Data: null,

  CATEGORIA_LABEL_MAP: {
    saudacoes: 'Saudações',
    familia: 'Família',
    profissoes: 'Profissões',
    expressoes: 'Expressões',
    numeros: 'Números',
    musica: 'Música',
    ciencia: 'Ciência',
    historia: 'História',
    religiao: 'Religião',
    logica: 'Lógica',
    politica: 'Política',
    economia: 'Economia',
    direito: 'Direito',
    filosofia: 'Filosofia',
    anatomia: 'Anatomia',
    natureza: 'Natureza',
    alimentacao: 'Alimentação',
    comercio: 'Comércio',
    educacao: 'Educação',
    emocoes: 'Emoções',
    esportes: 'Esportes',
    midia: 'Mídia',
    saude: 'Saúde',
    tecnologia: 'Tecnologia',
    transporte: 'Transporte',
    viagem: 'Viagem',
    cotidiano: 'Cotidiano',
    cultura: 'Cultura',
    adjetivos: 'Adjetivos',
    verbos: 'Verbos',
    substantivos: 'Substantivos',
    adverbios: 'Advérbios',
    preposicoes: 'Preposições',
    conjuncoes: 'Conjunções',
    pronomes: 'Pronomes',
    tempo: 'Tempo',
    clima: 'Clima',
    casa: 'Casa',
    roupas: 'Roupas',
    cores: 'Cores',
    animais: 'Animais',
    arte: 'Arte',
    literatura: 'Literatura',
    cinema: 'Cinema',
    gastronomia: 'Gastronomia',
    cidade: 'Cidade',
    trabalho: 'Trabalho',
    sentimentos: 'Sentimentos',
    relacoes: 'Relações',
    geografia: 'Geografia',
    matematica: 'Matemática',
    fisica: 'Física',
    quimica: 'Química',
    biologia: 'Biologia',
    medicina: 'Medicina',
    psicologia: 'Psicologia',
    sociologia: 'Sociologia',
    arquitetura: 'Arquitetura',
    engenharia: 'Engenharia',
    informatica: 'Informática',
    internet: 'Internet',
    redes_sociais: 'Redes Sociais',
    financas: 'Finanças',
    negocios: 'Negócios',
    turismo: 'Turismo',
    hotelaria: 'Hotelaria',
    restaurante: 'Restaurante',
    compras: 'Compras',
    lazer: 'Lazer',
    festas: 'Festas',
    tradicoes: 'Tradições',
    mitologia: 'Mitologia',
    espiritualidade: 'Espiritualidade',
    etica: 'Ética',
    estetica: 'Estética',
    metafisica: 'Metafísica',
    epistemologia: 'Epistemologia',
    retorica: 'Retórica',
    gramatica: 'Gramática'
  },

  formatarCategoria(cat) {
    if (!cat) return '';
    const key = String(cat).trim().toLowerCase();
    if (this.CATEGORIA_LABEL_MAP[key]) return this.CATEGORIA_LABEL_MAP[key];
    const limpo = key.replace(/_/g, ' ');
    return limpo.charAt(0).toUpperCase() + limpo.slice(1);
  },

  toggleModoCompacto() {
    this.modoCompacto = !this.modoCompacto;
    const listEl = document.getElementById('vocab-list');
    if (listEl) {
      listEl.classList.toggle('vocab-compact', this.modoCompacto);
    }
    const btn = document.getElementById('vocab-btn-densidade');
    if (btn) {
      const isIt = typeof I18n !== 'undefined' && I18n.idioma === 'it';
      btn.textContent = this.modoCompacto
        ? (isIt ? '⊞ Confortevole' : '⊞ Confortável')
        : (isIt ? '☰ Compatto' : '☰ Compacto');
      btn.classList.toggle('ativo', this.modoCompacto);
    }
  },

  carregarMais() {
    this._limiteRender = (this._limiteRender || 80) + 100;
    this.renderizar(true);
  },

  async filtrarTop1000() {
    this.filtroOrigem = 'top1000';
    this._limiteRender = 80;
    if (!this.top1000Data) {
      try {
        const res = await fetch('data/top1000_vocabulario.json');
        const data = await res.json();
        this.top1000Data = data.palavras || [];
      } catch (e) {
        console.error('Erro ao carregar top1000_vocabulario.json:', e);
      }
    }
    this.renderizar();
  },

  // ── Render filtered word list ─────────────────────────────
  renderizar(manterLimite = false) {
    if (!manterLimite) this._limiteRender = 80;
    const listEl = document.getElementById('vocab-list');
    const statsEl = document.getElementById('vocab-stats');
    if (!listEl) return;
    listEl.classList.toggle('vocab-compact', !!this.modoCompacto);

    const todos = (this.filtroOrigem === 'top1000' && this.top1000Data)
      ? this.top1000Data
      : App.estado.vocabCache;

    if (!todos || todos.length === 0) {
      listEl.innerHTML = '<p style="color:var(--cor-inchiostro-claro,#5A4535);font-style:italic;text-align:center;padding:1.5rem;">Nenhuma palavra carregada ainda.</p>';
      if (statsEl) statsEl.textContent = '';
      return;
    }

    // Update origin pills active state
    const pillStyle = (active) => active
      ? 'padding:0.22rem 0.65rem;border-radius:999px;border:1.5px solid #9B2335;background:#9B2335;color:#fff;cursor:pointer;font-size:0.75rem;font-weight:600'
      : 'padding:0.22rem 0.65rem;border-radius:999px;border:1.5px solid #8F7E6D;background:transparent;color:var(--cor-inchiostro,#2C2416);cursor:pointer;font-size:0.75rem;font-weight:600';
    const pT = document.getElementById('vocab-pill-todos');
    const pTop = document.getElementById('vocab-pill-top1000');
    const pC = document.getElementById('vocab-pill-custom');
    const pN = document.getElementById('vocab-pill-nativo');
    if (pT) pT.style.cssText = pillStyle(this.filtroOrigem === '');
    if (pTop) pTop.style.cssText = pillStyle(this.filtroOrigem === 'top1000');
    if (pC) pC.style.cssText = pillStyle(this.filtroOrigem === 'custom');
    if (pN) pN.style.cssText = pillStyle(this.filtroOrigem === 'nativo');

    // Apply filters
    let filtrados = todos;

    if (this.filtroOrigem === 'custom') filtrados = filtrados.filter(p => p._custom || p.custom);
    if (this.filtroOrigem === 'nativo') filtrados = filtrados.filter(p => !p._custom && !p.custom);

    if (this.filtroTemplo) {
      const num = parseInt(this.filtroTemplo, 10);
      filtrados = filtrados.filter(p => p.templo_num === num);
    }

    if (this.filtroCategoria) {
      const cat = this.filtroCategoria.toLowerCase();
      filtrados = filtrados.filter(p => (p.categoria || '').toLowerCase() === cat);
    }

    if (this.filtroTexto) {
      const q = this.filtroTexto.toLowerCase().trim();
      filtrados = filtrados.filter(p =>
        (p.italiano || '').toLowerCase().includes(q) ||
        (p.portugues || '').toLowerCase().includes(q) ||
        (p.categoria || '').toLowerCase().includes(q)
      );
    }

    // Difficult words filter
    if (this.filtroDificeis) {
      filtrados = filtrados.filter(p => {
        const fsrs = App.estado.flashcardData[p.id];
        return fsrs && (fsrs.erros || 0) >= 3;
      });
    }

    // Favorites filter
    if (this.filtroFavoritos) {
      const favIds = (App.estado.progresso || {}).favoritos || [];
      filtrados = filtrados.filter(p => favIds.includes(p.id));
    }

    // Count difficult words (for badge)
    const numDificeis = todos.filter(p => {
      const fsrs = App.estado.flashcardData[p.id];
      return fsrs && (fsrs.erros || 0) >= 3;
    }).length;
    const btnDif = document.getElementById('vocab-btn-dificeis');
    if (btnDif) {
      btnDif.classList.toggle('ativo', this.filtroDificeis);
      btnDif.innerHTML = numDificeis > 0
        ? `${I18n.t('vocab_dificeis')} <span class="dif-count">${numDificeis}</span>`
        : I18n.t('vocab_dificeis');
    }

    // Favorites badge
    const numFav = ((App.estado.progresso || {}).favoritos || []).length;
    const btnFav = document.getElementById('vocab-btn-favoritos');
    if (btnFav) {
      btnFav.classList.toggle('ativo', this.filtroFavoritos);
      btnFav.innerHTML = numFav > 0
        ? `${I18n.t('vocab_favoritos')} <span class="dif-count">${numFav}</span>`
        : I18n.t('vocab_favoritos');
    }

    // Stats line + botão estudar filtro
    const limiteAtual = this._limiteRender || 80;
    if (statsEl) {
      const total = todos.length;
      const mostrando = Math.min(filtrados.length, limiteAtual);
      const textoStats = this.filtroDificeis
        ? I18n.t(filtrados.length !== 1 ? 'vocab_palavras_dificeis' : 'vocab_palavra_dificil').replace('{n}', filtrados.length)
        : filtrados.length === total
          ? I18n.t('vocab_palavras_total').replace('{n}', total)
          : I18n.t('vocab_resultados').replace('{m}', mostrando).replace('{f}', filtrados.length).replace('{t}', total);

      // Botão "estudar este filtro" só aparece quando há filtro ativo e resulados
      const temFiltro = this.filtroTexto || this.filtroTemplo || this.filtroCategoria || this.filtroDificeis || this.filtroFavoritos;
      const btnEstudar = (temFiltro && filtrados.length > 0)
        ? `<button onclick="Vocab.estudarFiltroAtual()" style="margin-left:0.5rem;padding:0.18rem 0.6rem;background:#9B2335;color:#fff;border:none;border-radius:6px;font-size:0.72rem;font-weight:700;cursor:pointer">🃏 ${I18n.idioma==='it'?'Studia questo filtro':'Estudar este filtro'}</button>`
        : '';
      statsEl.innerHTML = `<span>${textoStats}</span>${btnEstudar}`;
    }

    // Incremental display
    const visivel = filtrados.slice(0, limiteAtual);

    if (visivel.length === 0) {
      listEl.innerHTML = `<p style="color:var(--cor-inchiostro-claro,#5A4535);font-style:italic;text-align:center;padding:1.5rem;grid-column:1/-1;">${I18n.t('vocab_nenhuma')}</p>`;
      return;
    }

    listEl.innerHTML = '';
    visivel.forEach((p, idx) => {
      this._renderizarItem(p, listEl, idx);
    });

    // Reapply blur class after re-render
    if (this.blurColuna) {
      listEl.classList.add(`blur-${this.blurColuna}`);
      const btnPt = document.getElementById('vocab-btn-blur-pt');
      const btnIt = document.getElementById('vocab-btn-blur-it');
      if (btnPt) btnPt.classList.toggle('ativo', this.blurColuna === 'pt');
      if (btnIt) btnIt.classList.toggle('ativo', this.blurColuna === 'it');
    }

    // Show "Load more" button if truncated
    if (filtrados.length > limiteAtual) {
      const restantes = filtrados.length - limiteAtual;
      const moreWrap = document.createElement('div');
      moreWrap.style.cssText = 'grid-column:1/-1;text-align:center;padding:0.85rem 0.5rem;display:flex;flex-direction:column;align-items:center;gap:0.4rem;';
      const isIt = typeof I18n !== 'undefined' && I18n.idioma === 'it';
      moreWrap.innerHTML = `
        <span style="color:var(--cor-inchiostro-claro,#5A4535);font-style:italic;font-size:0.82rem;">${I18n.t('vocab_e_mais').replace('{n}', restantes)}</span>
        <button type="button" onclick="Vocab.carregarMais()" style="padding:0.45rem 1.2rem;border-radius:999px;border:1.5px solid var(--cor-veneziano,#9B2335);background:transparent;color:var(--cor-veneziano,#9B2335);font-weight:700;font-size:0.82rem;cursor:pointer;">
          ➕ ${isIt ? `Carica altre parole (+${Math.min(100, restantes)})` : `Carregar mais palavras (+${Math.min(100, restantes)})`}
        </button>
      `;
      listEl.appendChild(moreWrap);
    }
  },

  // ── Search handler ────────────────────────────────────────
  buscar(texto) {
    this.filtroTexto = texto;
    if (this._debounceTimer) clearTimeout(this._debounceTimer);
    this._debounceTimer = setTimeout(() => {
      this.renderizar();
    }, 150);
  },

  // ── Temple filter handler ─────────────────────────────────
  filtrarTemplo(valor) {
    this.filtroTemplo = valor;
    this.renderizar();
  },

  // ── Category filter handler ───────────────────────────────
  filtrarCategoria(valor) {
    this.filtroCategoria = valor;
    this.renderizar();
  },

  // ── Difficult words filter toggle ─────────────────────────
  toggleDificeis() {
    this.filtroDificeis  = !this.filtroDificeis;
    if (this.filtroDificeis) {
      this.filtroFavoritos = false;
      this.filtroTexto = this.filtroTemplo = this.filtroCategoria = '';
      ['vocab-busca','vocab-templo-filtro','vocab-categoria-filtro'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
      });
    }
    this.renderizar();
  },

  // ── Favorites filter toggle ───────────────────────────────
  toggleFavoritos() {
    this.filtroFavoritos = !this.filtroFavoritos;
    if (this.filtroFavoritos) {
      this.filtroDificeis  = false;
      this.filtroTexto = this.filtroTemplo = this.filtroCategoria = '';
      ['vocab-busca','vocab-templo-filtro','vocab-categoria-filtro'].forEach(id => {
        const el = document.getElementById(id); if (el) el.value = '';
      });
    }
    this.renderizar();
  },

  // ── Populate filter dropdowns ─────────────────────────────
  popularCategorias() {
    this._popularFiltroTemplo();
    this._popularFiltroCategoria();
  },

  _popularFiltroTemplo() {
    const sel = document.getElementById('vocab-templo-filtro');
    if (!sel) return;

    const lblTodos = typeof I18n !== 'undefined' ? I18n.t('vocab_todos_templos') : '-- Todos os templos --';
    sel.innerHTML = `<option value="">${lblTodos}</option>`;

    const desbloqueados = App.estado.progresso ? App.estado.progresso.templos_desbloqueados : [1];
    desbloqueados.forEach(num => {
      const data = App.estado.templosData[num];
      if (!data) return;
      const opt = document.createElement('option');
      opt.value = num;
      const nome = (App.TEMPLO_NOMES && App.TEMPLO_NOMES[num]) || data.nome || data.cidade || `Templo ${num}`;
      opt.textContent = `${num}. ${nome}`;
      sel.appendChild(opt);
    });
  },

  _popularFiltroCategoria() {
    const sel = document.getElementById('vocab-categoria-filtro');
    if (!sel) return;

    const lblTodas = typeof I18n !== 'undefined' ? I18n.t('vocab_todas_cats') : '-- Todas as categorias --';
    sel.innerHTML = `<option value="">${lblTodas}</option>`;

    // Collect unique categories from vocab cache
    const categorias = new Set();
    (App.estado.vocabCache || []).forEach(p => {
      if (p.categoria) categorias.add(p.categoria);
    });

    // Sort alphabetically by formatted display label and add to dropdown
    [...categorias]
      .sort((a, b) => this.formatarCategoria(a).localeCompare(this.formatarCategoria(b), 'pt-BR'))
      .forEach(cat => {
        const opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = this.formatarCategoria(cat);
        sel.appendChild(opt);
      });
  },

  // ── Blur column toggle (self-test mode) ──────────────────
  toggleBlur(coluna) {
    // Se já está ativo nessa coluna → desativa; senão ativa
    this.blurColuna = this.blurColuna === coluna ? null : coluna;

    const listEl = document.getElementById('vocab-list');
    if (listEl) {
      listEl.classList.toggle('blur-pt', this.blurColuna === 'pt');
      listEl.classList.toggle('blur-it', this.blurColuna === 'it');
      // Resetar itens revelados ao trocar ou desativar
      listEl.querySelectorAll('.vocab-item.revelada').forEach(el => el.classList.remove('revelada'));
    }

    // Atualizar botões
    const btnPt = document.getElementById('vocab-btn-blur-pt');
    const btnIt = document.getElementById('vocab-btn-blur-it');
    if (btnPt) btnPt.classList.toggle('ativo', this.blurColuna === 'pt');
    if (btnIt) btnIt.classList.toggle('ativo', this.blurColuna === 'it');

    // Quando blur ativo, clicar no item revela aquela célula; clique normal pronuncia
    if (listEl) {
      listEl.querySelectorAll('.vocab-item').forEach(item => {
        item.onclick = this.blurColuna
          ? (e) => {
              // Não propaga se clicou na célula borrada → revela
              const target = e.target.closest('.vocab-pt, .vocab-it');
              const isBluCol = (this.blurColuna === 'pt' && target?.classList.contains('vocab-pt'))
                            || (this.blurColuna === 'it' && target?.classList.contains('vocab-it'));
              if (isBluCol || !target) {
                item.classList.toggle('revelada');
              }
            }
          : () => App.pronunciar(item.querySelector('.vocab-it')?.textContent || '');
      });
    }
  },

  // ============================================================
  // Métodos para renderizar itens de vocabulário enriquecidos
  // ============================================================
  // 1. Paleta de cores para categorias
  _coresCategorias: {},
  _coresDisponiveis: ['#1a5276', '#117a65', '#7d3c98', '#c0392b', '#d4a017', '#2e86c1', '#28b463', '#8e44ad', '#e67e22', '#2c3e50'],
  _corCatIdx: 0,
  _corParaCategoria(cat) {
    if (!cat) return '';
    const key = cat.toLowerCase();
    if (!this._coresCategorias[key]) {
      this._coresCategorias[key] = this._coresDisponiveis[this._corCatIdx % this._coresDisponiveis.length];
      this._corCatIdx++;
    }
    return this._coresCategorias[key];
  },

  // 2. Escape seguro de caracteres HTML
  _escapar(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  },

  // 3. Renderizador individual do item
  _renderizarItem(p, container, idx = 0) {
    const item = document.createElement('div');
    item.className = idx >= 16 ? 'vocab-item vocab-item-deferred' : 'vocab-item';
    item.setAttribute('tabindex', '0');
    item.setAttribute('role', 'listitem');
    item.setAttribute('aria-label', `${p.italiano || ''} — ${p.portugues || ''}`);
    item.style.cursor = 'pointer';
    item.title = this.blurColuna
      ? (typeof I18n !== 'undefined' ? I18n.t('fc_dica_revelar') : 'Revelar')
      : `Clique para ouvir "${p.italiano || ''}"`;

    // Status FSRS / SM-2
    const sm = (typeof App !== 'undefined' && App.estado?.flashcardData) ? App.estado.flashcardData[p.id] : null;
    let sm2Icon = '🌱'; // nova
    let sm2Titulo = 'Nova palavra';
    let sm2Pct = 0;
    if (sm) {
      const reps = sm.reps || sm.repeticoes || 0;
      const stability = sm.stability || 0;
      if (reps >= 3 || stability > 7) {
        sm2Icon = '⭐';
        sm2Titulo = 'Dominada';
        sm2Pct = 100;
      } else if (reps > 0) {
        sm2Icon = '📚';
        sm2Titulo = 'Em aprendizado';
        sm2Pct = Math.min(99, Math.round((reps / 3) * 100));
      }
    }
    const erros = sm ? (sm.erros || 0) : 0;

    // Nível CEFR pelo Templo (se existir)
    const temploData = (typeof App !== 'undefined' && App.estado?.templosData) ? App.estado.templosData[p.templo_num] : null;
    const nivel = temploData ? temploData.nivel : (p.nivel || 'A1');

    // Cor lateral da categoria
    const catCor = this._corParaCategoria(p.categoria);

    // Bloco da Frase de Exemplo
    const safeExemplo = p.exemplo ? this._escapar(p.exemplo) : '';
    const safeExemploPt = p.exemplo_pt ? this._escapar(p.exemplo_pt) : '';
    const exemploHtml = p.exemplo
      ? `<div class="vocab-exemplo"
              role="button"
              tabindex="0"
              data-exemplo="${safeExemplo}"
              title="🔊 Ouvir frase de exemplo: &quot;${safeExemplo}&quot;${safeExemploPt ? ' — ' + safeExemploPt : ''}"
              aria-label="Ouvir frase de exemplo: ${safeExemplo}"
              onclick="event.stopPropagation();Vocab.pronunciarExemplo(this.getAttribute('data-exemplo')||'',event,this)"
              onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();event.stopPropagation();Vocab.pronunciarExemplo(this.getAttribute('data-exemplo')||'',event,this)}">
          <button type="button" class="vocab-exemplo-audio-btn" aria-label="Ouvir frase de exemplo" title="Ouvir frase de exemplo" onclick="event.stopPropagation();Vocab.pronunciarExemplo(this.closest('.vocab-exemplo')?.getAttribute('data-exemplo')||'',event,this.closest('.vocab-exemplo'))">🔊</button>
          <span class="vocab-exemplo-texto">"${safeExemplo}"</span>
          ${safeExemploPt ? `<span class="vocab-exemplo-pt" style="opacity:0.75;font-style:normal;margin-left:0.35rem">(${safeExemploPt})</span>` : ''}
        </div>`
      : '';

    // Barra de progresso FSRS
    const progressoHtml = `
      <div class="vocab-progresso" style="width:40px;height:4px;background:#e0e0e0;border-radius:2px;margin-top:0.2rem;overflow:hidden">
        <div style="width:${sm2Pct}%;height:100%;background:${sm2Pct >= 100 ? '#27AE60' : sm2Pct > 0 ? '#F39C12' : '#ccc'};border-radius:2px;transition:width 0.3s"></div>
      </div>
    `;

    item.innerHTML = `
      ${p.rank ? `<span class="vocab-cat-badge" style="background:#9B2335;color:#fff;font-weight:700" title="Posição no ranking Top 1000">#${p.rank}</span>` : ''}
      <span class="vocab-it">${this._escapar(p.italiano || '—')}</span>
      <span class="vocab-seta">→</span>
      <span class="vocab-pt">${this._escapar(p.portugues || '—')}</span>
      ${p.categoria ? `<span class="vocab-cat-badge" style="${catCor ? 'border-left:3px solid ' + catCor + ';padding-left:4px' : ''}">${this._escapar(this.formatarCategoria(p.categoria))}</span>` : ''}
      ${nivel ? `<span class="vocab-nivel-badge">${this._escapar(nivel)}</span>` : ''}
      ${erros >= 3 ? `<span class="vocab-dif-badge" title="${erros} erros">⚠️ ${erros}</span>` : ''}
      ${(typeof App !== 'undefined' && App.ehFavorito && App.ehFavorito(p.id)) ? `<span class="vocab-fav-badge">❤️</span>` : ''}
      <span class="vocab-sm2-badge" title="${sm2Titulo}">${sm2Icon}</span>
      ${progressoHtml}
      ${p._custom ? `<button onclick="event.stopPropagation();IAImport.excluir('vocab','${p.id}')" class="ia-del-btn" title="Remover palavra">🗑️</button>` : ''}
      ${exemploHtml}
    `;

    // Clique no card
    if (this.blurColuna) {
      item.onclick = (e) => {
        if (e.target.closest('.vocab-exemplo, .vocab-exemplo-audio-btn')) return;
        const target = e.target.closest('.vocab-pt, .vocab-it');
        const isBluCol = (this.blurColuna === 'pt' && target?.classList.contains('vocab-pt'))
                      || (this.blurColuna === 'it' && target?.classList.contains('vocab-it'));
        if (isBluCol || !target) item.classList.toggle('revelada');
      };
    } else {
      item.onclick = (e) => {
        if (e.target.closest('.vocab-exemplo, .vocab-exemplo-audio-btn')) return;
        if (this.modoCompacto) {
          item.classList.toggle('vocab-expanded');
        }
        if (typeof App !== 'undefined' && App.pronunciar) {
          App.pronunciar(p.italiano);
        }
      };
    }

    item.onkeydown = (e) => {
      if (e.target.closest('.vocab-exemplo, .vocab-exemplo-audio-btn')) return;
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        item.click();
      }
    };

    container.appendChild(item);
  },

  // 4. Reprodução autônoma do áudio do exemplo
  pronunciarExemplo(texto, event, el) {
    if (event) {
      if (typeof event.stopPropagation === 'function') event.stopPropagation();
      if (typeof event.preventDefault === 'function') event.preventDefault();
    }
    if (!texto) return;
    const targetEl = el || (event && event.currentTarget ? event.currentTarget.closest('.vocab-exemplo') : null);
    if (targetEl && targetEl.classList) {
      targetEl.classList.add('vocab-exemplo-tocando');
      setTimeout(() => {
        try { targetEl.classList.remove('vocab-exemplo-tocando'); } catch (_) {}
      }, 1600);
    }
    if (typeof App !== 'undefined' && App.pronunciar) {
      App.pronunciar(texto);
    } else if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try { window.speechSynthesis.cancel(); } catch (_) {}
      const u = new SpeechSynthesisUtterance(texto);
      u.lang = 'it-IT';
      window.speechSynthesis.speak(u);
    }
  },

  // ── Inicia flashcards com as palavras do filtro atual ───────
  estudarFiltroAtual() {
    const todos = App.estado.vocabCache;
    let filtrados = todos;
    if (this.filtroTemplo) {
      const num = parseInt(this.filtroTemplo, 10);
      filtrados = filtrados.filter(p => p.templo_num === num);
    }
    if (this.filtroCategoria) {
      const cat = this.filtroCategoria.toLowerCase();
      filtrados = filtrados.filter(p => (p.categoria||'').toLowerCase() === cat);
    }
    if (this.filtroTexto) {
      const q = this.filtroTexto.toLowerCase().trim();
      filtrados = filtrados.filter(p =>
        (p.italiano||'').toLowerCase().includes(q) ||
        (p.portugues||'').toLowerCase().includes(q)
      );
    }
    if (this.filtroDificeis) {
      filtrados = filtrados.filter(p => {
        const f = App.estado.flashcardData[p.id];
        return f && (f.erros||0) >= 3;
      });
    }
    if (this.filtroFavoritos) {
      const favIds = (App.estado.progresso||{}).favoritos||[];
      filtrados = filtrados.filter(p => favIds.includes(p.id));
    }
    if (filtrados.length === 0) return;

    // Shuffle e cap 30
    const embaralhado = [...filtrados].sort(() => Math.random() - 0.5).slice(0, 30);

    App.navegar('flashcard');
    if (typeof Flashcards === 'undefined') return;

    Flashcards.temploAtual      = null;
    Flashcards.praticandoTodas  = false;
    Flashcards.sessaoStats      = { again:0, hard:0, good:0, easy:0, xp:0, novas:[] };
    Flashcards.cartasDisponiveis = embaralhado;
    Flashcards.indiceAtual      = 0;
    Flashcards.virada           = false;
    if (!Flashcards._swipeInitialized) { Flashcards._iniciarSwipe(); Flashcards._swipeInitialized = true; }

    const vazio = document.getElementById('flashcard-vazio');
    const resumo = document.getElementById('flashcard-resumo');
    const cardEl = document.getElementById('flashcard');
    const actions = document.getElementById('card-actions');
    if (vazio)   vazio.style.display   = 'none';
    if (resumo)  resumo.style.display  = 'none';
    if (cardEl)  cardEl.style.display  = '';
    if (actions) actions.style.display = 'none';

    App.notificar(`🃏 ${embaralhado.length} parole dal filtro attivo`, 'alerta');
    Flashcards.mostrarCarta();
  }
};

document.addEventListener('i18n:changed', () => {
  if (document.getElementById('vocab-list')) Vocab.renderizar();
});


// Exposição global segura para navegadores e testes
if (typeof window !== 'undefined') window.Vocab = Vocab;
if (typeof globalThis !== 'undefined') globalThis.Vocab = Vocab;
if (typeof module !== 'undefined' && module.exports) module.exports = Vocab;
