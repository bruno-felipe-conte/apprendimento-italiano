// ============================================================
// vocab.js — Vocabulary browser with search and filters
// ============================================================

const Vocab = {
  filtroTexto: '',
  filtroTemplo: '',
  filtroCategoria: '',
  filtroOrigem: '',   // '' | 'custom' | 'nativo'
  filtroDificeis:   false,
  filtroFavoritos:  false,
  blurColuna: null,   // null | 'pt' | 'it'

  // ── Render filtered word list ─────────────────────────────
  renderizar() {
    const listEl = document.getElementById('vocab-list');
    const statsEl = document.getElementById('vocab-stats');
    if (!listEl) return;

    const todos = App.estado.vocabCache;
    if (!todos || todos.length === 0) {
      listEl.innerHTML = '<p style="color:#aaa;font-style:italic;text-align:center;padding:1.5rem;">Nenhuma palavra carregada ainda.</p>';
      if (statsEl) statsEl.textContent = '';
      return;
    }

    // Update origin pills active state
    const pillStyle = (active) => active
      ? 'padding:0.22rem 0.65rem;border-radius:999px;border:1.5px solid #7B68A0;background:#7B68A0;color:#fff;cursor:pointer;font-size:0.75rem;font-weight:600'
      : 'padding:0.22rem 0.65rem;border-radius:999px;border:1.5px solid #ddd;background:transparent;cursor:pointer;font-size:0.75rem;font-weight:600';
    const pT = document.getElementById('vocab-pill-todos');
    const pC = document.getElementById('vocab-pill-custom');
    const pN = document.getElementById('vocab-pill-nativo');
    if (pT) pT.style.cssText = pillStyle(this.filtroOrigem === '');
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
    if (statsEl) {
      const total = todos.length;
      const mostrando = Math.min(filtrados.length, 100);
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

    // Limit display to 100
    const visivel = filtrados.slice(0, 100);

    if (visivel.length === 0) {
      listEl.innerHTML = `<p style="color:#aaa;font-style:italic;text-align:center;padding:1.5rem;">${I18n.t('vocab_nenhuma')}</p>`;
      return;
    }

    listEl.innerHTML = '';
    visivel.forEach(p => {
      const item = document.createElement('div');
      item.className = 'vocab-item';

      // Determine FSRS status
      const sm = App.estado.flashcardData[p.id];
      let sm2Icon = '🌱'; // new
      if (sm) {
        if ((sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7)) sm2Icon = '⭐'; // mastered
        else sm2Icon = '📚'; // learning
      }
      const erros = sm ? (sm.erros || 0) : 0;

      // Temple data for level badge
      const temploData = App.estado.templosData[p.templo_num];
      const nivel = temploData ? temploData.nivel : '';

      item.innerHTML = `
        <span class="vocab-it">${this._escapar(p.italiano || '—')}</span>
        <span class="vocab-seta">→</span>
        <span class="vocab-pt">${this._escapar(p.portugues || '—')}</span>
        ${p.categoria ? `<span class="vocab-cat-badge">${this._escapar(p.categoria)}</span>` : ''}
        ${nivel ? `<span class="vocab-nivel-badge">${this._escapar(nivel)}</span>` : ''}
        ${erros >= 3 ? `<span class="vocab-dif-badge" title="${erros} erros">⚠️ ${erros}</span>` : ''}
        ${App.ehFavorito(p.id) ? `<span class="vocab-fav-badge">❤️</span>` : ''}
        <span class="vocab-sm2-badge" title="${sm2Icon === '⭐' ? 'Dominata' : sm2Icon === '📚' ? 'In apprendimento' : 'Nuova'}">${sm2Icon}</span>
        ${p._custom ? `<button onclick="event.stopPropagation();IAImport.excluir('vocab','${p.id}')" class="ia-del-btn" title="Remover palavra">🗑️</button>` : ''}
      `;

      // Click: pronounce normally; in blur mode clicking blurred cell reveals it
      item.style.cursor = 'pointer';
      item.title = this.blurColuna ? I18n.t('fc_dica_revelar') : `${I18n.idioma === 'it' ? 'Clicca per ascoltare' : 'Clique para ouvir'} "${p.italiano}"`;
      if (this.blurColuna) {
        item.onclick = (e) => {
          const target = e.target.closest('.vocab-pt, .vocab-it');
          const isBluCol = (this.blurColuna === 'pt' && target?.classList.contains('vocab-pt'))
                        || (this.blurColuna === 'it' && target?.classList.contains('vocab-it'));
          if (isBluCol || !target) item.classList.toggle('revelada');
        };
      } else {
        item.onclick = () => App.pronunciar(p.italiano);
      }

      listEl.appendChild(item);
    });

    // Reapply blur class after re-render
    if (this.blurColuna) {
      listEl.classList.add(`blur-${this.blurColuna}`);
      const btnPt = document.getElementById('vocab-btn-blur-pt');
      const btnIt = document.getElementById('vocab-btn-blur-it');
      if (btnPt) btnPt.classList.toggle('ativo', this.blurColuna === 'pt');
      if (btnIt) btnIt.classList.toggle('ativo', this.blurColuna === 'it');
    }

    // Show "more results" hint if truncated
    if (filtrados.length > 100) {
      const more = document.createElement('p');
      more.style.cssText = 'text-align:center;color:#aaa;font-style:italic;padding:0.8rem;font-size:0.83rem;';
      more.textContent = I18n.t('vocab_e_mais').replace('{n}', filtrados.length - 100);
      listEl.appendChild(more);
    }
  },

  // ── Search handler ────────────────────────────────────────
  buscar(texto) {
    this.filtroTexto = texto;
    this.renderizar();
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

    // Keep "Tutti i templi" option
    sel.innerHTML = '<option value="">Tutti i templi</option>';

    const desbloqueados = App.estado.progresso ? App.estado.progresso.templos_desbloqueados : [1];
    desbloqueados.forEach(num => {
      const data = App.estado.templosData[num];
      if (!data) return;
      const opt = document.createElement('option');
      opt.value = num;
      const nome = (App.TEMPLO_NOMES && App.TEMPLO_NOMES[num]) || data.nome || data.cidade || `Tempio ${num}`;
      opt.textContent = `${num}. ${nome}`;
      sel.appendChild(opt);
    });
  },

  _popularFiltroCategoria() {
    const sel = document.getElementById('vocab-categoria-filtro');
    if (!sel) return;

    sel.innerHTML = '<option value="">Tutte le categorie</option>';

    // Collect unique categories from vocab cache
    const categorias = new Set();
    (App.estado.vocabCache || []).forEach(p => {
      if (p.categoria) categorias.add(p.categoria);
    });

    // Sort alphabetically and add to dropdown
    [...categorias].sort().forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat;
      opt.textContent = cat.charAt(0).toUpperCase() + cat.slice(1);
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

  // ── Escape HTML helper ────────────────────────────────────
  _escapar(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
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
