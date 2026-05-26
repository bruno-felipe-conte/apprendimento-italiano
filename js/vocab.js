// ============================================================
// vocab.js — Vocabulary browser with search and filters
// ============================================================

const Vocab = {
  filtroTexto: '',
  filtroTemplo: '',
  filtroCategoria: '',

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

    // Apply filters
    let filtrados = todos;

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

    // Stats line
    if (statsEl) {
      const total = todos.length;
      const mostrando = Math.min(filtrados.length, 100);
      statsEl.textContent = filtrados.length === total
        ? `${total} palavras no total`
        : `${mostrando} de ${filtrados.length} resultado(s) — ${total} palavras totais`;
    }

    // Limit display to 100
    const visivel = filtrados.slice(0, 100);

    if (visivel.length === 0) {
      listEl.innerHTML = '<p style="color:#aaa;font-style:italic;text-align:center;padding:1.5rem;">Nenhuma palavra encontrada.</p>';
      return;
    }

    listEl.innerHTML = '';
    visivel.forEach(p => {
      const item = document.createElement('div');
      item.className = 'vocab-item';

      // Determine SM-2 status
      const sm = App.estado.flashcardData[p.id];
      let sm2Icon = '🌱'; // new
      if (sm) {
        if (sm.repeticoes >= 3) sm2Icon = '⭐'; // mastered
        else sm2Icon = '📚'; // learning
      }

      // Temple data for level badge
      const temploData = App.estado.templosData[p.templo_num];
      const nivel = temploData ? temploData.nivel : '';

      item.innerHTML = `
        <span class="vocab-it">${this._escapar(p.italiano || '—')}</span>
        <span class="vocab-seta">→</span>
        <span class="vocab-pt">${this._escapar(p.portugues || '—')}</span>
        ${p.categoria ? `<span class="vocab-cat-badge">${this._escapar(p.categoria)}</span>` : ''}
        ${nivel ? `<span class="vocab-nivel-badge">${this._escapar(nivel)}</span>` : ''}
        <span class="vocab-sm2-badge" title="${sm2Icon === '⭐' ? 'Dominata' : sm2Icon === '📚' ? 'In apprendimento' : 'Nuova'}">${sm2Icon}</span>
      `;

      // Click to pronounce
      item.style.cursor = 'pointer';
      item.title = `Clique para ouvir "${p.italiano}"`;
      item.onclick = () => App.pronunciar(p.italiano);

      listEl.appendChild(item);
    });

    // Show "more results" hint if truncated
    if (filtrados.length > 100) {
      const more = document.createElement('p');
      more.style.cssText = 'text-align:center;color:#aaa;font-style:italic;padding:0.8rem;font-size:0.83rem;';
      more.textContent = `... e mais ${filtrados.length - 100} palavras. Use os filtros para refinar.`;
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
      opt.textContent = `${num}. ${data.nome}`;
      sel.appendChild(opt);
    });
  },

  _popularFiltroCategoria() {
    const sel = document.getElementById('vocab-categoria-filtro');
    if (!sel) return;

    sel.innerHTML = '<option value="">Tutte le categorie</option>';

    // Collect unique categories from vocab cache
    const categorias = new Set();
    App.estado.vocabCache.forEach(p => {
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

  // ── Escape HTML helper ────────────────────────────────────
  _escapar(str) {
    const d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }
};
