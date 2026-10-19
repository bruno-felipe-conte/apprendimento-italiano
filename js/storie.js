// ============================================================
// storie.js — Módulo de leitura interativa de histórias italianas
// - 10 histórias A1-C2 (data/storie.json)
// - Texto corrido, toda palavra clicável
// - Modal flutuante com IPA/tradução/categoria + salvar no deck
// - TTS via App.pronunciar
// - Marcar como lida + XP recompensa
// ============================================================

const Storie = {
  dados: null,
  storAttuale: null,
  traduzirVisivel: false,
  completate: [],
  paginaAtual: 1,
  _paginas: [],
  _indiceAberto: false,
  _touchStartX: 0,
  _touchStartY: 0,
  _keyListener: null,
  _resizeListener: null,
  _animandoVirada: false,
  _reproduzindoAudio: false,
  _audioFilaSentencas: [],
  _audioIndexSentenca: 0,
  _filtroNivel: '',
  _filtroTexto: '',
  _filtroOrigem: '',
  _escListener: null,
  _tradCache: {},   // cache in-memory: palavra → tradução

  // ── Carregar dados ─────────────────────────────────────────
  async carregar() {
    if (!this.dados) {
      try {
        const cached = localStorage.getItem('it_swr_storie');
        if (cached) {
          const raw = JSON.parse(cached);
          raw.storie = (raw.storie || []).map(s => this._normalizar(s));
          this.dados = raw;
          fetch('data/storie.json')
            .then(r => r.ok ? r.json() : null)
            .then(fresh => {
              if (fresh && Array.isArray(fresh.storie)) {
                fresh.storie = fresh.storie.map(s => this._normalizar(s));
                this.dados = fresh;
                try { localStorage.setItem('it_swr_storie', JSON.stringify(fresh)); } catch (_) {}
              }
            })
            .catch(() => {});
        }
      } catch (_) {}
    }

    if (!this.dados) {
      try {
        const r = await fetch('data/storie.json');
        if (r.ok) {
          const raw = await r.json();
          raw.storie = (raw.storie || []).map(s => this._normalizar(s));
          this.dados = raw;
          try { localStorage.setItem('it_swr_storie', JSON.stringify(raw)); } catch (_) {}
        } else this.dados = { storie: [] };
      } catch { this.dados = { storie: [] }; }
    }
    // Mescla histórias customizadas — custom primeiro (preserva base para evitar duplicatas)
    if (!this._storieBase) this._storieBase = [...this.dados.storie];
    try {
      const custom = JSON.parse(localStorage.getItem('it_storie_custom') || '[]');
      const normalizadas = custom.map(s => this._normalizar(s));
      this.dados.storie = [...normalizadas, ...this._storieBase];
    } catch (e) { this.dados.storie = [...this._storieBase]; }
    try {
      this.completate = JSON.parse(localStorage.getItem('it_storie_lidas') || '[]');
    } catch { this.completate = []; }
  },

  // Normaliza histórias com schema alternativo (titolo/livello/testo-string/capitoli/paragrafi)
  _normalizar(s) {
    if (!s) return s;
    const out = Object.assign({}, s);
    if (!out.titulo && out.titolo) out.titulo = out.titolo;
    if (!out.titulo_pt) out.titulo_pt = out.titulo || out.titolo || '';
    if (!out.nivel && out.livello) out.nivel = out.livello;
    if (!out.descricao) out.descricao = out.tema || out.sinossi || '';
    if (!out.descricao_pt) out.descricao_pt = out.descricao;
    if (!out.icone) out.icone = '📜';
    if (!out.xp_recompensa) out.xp_recompensa = 60;

    // Normaliza capítulos aninhados se vier em out.capitoli
    if (!out.testo && Array.isArray(out.capitoli)) {
      const flat = [];
      out.capitoli.forEach((cap, cIdx) => {
        const capTit = cap.titulo || cap.titolo || `Capitolo ${cIdx + 1}`;
        const pars = Array.isArray(cap.paragrafi) ? cap.paragrafi : (Array.isArray(cap.testo) ? cap.testo : []);
        pars.forEach((p, pIdx) => {
          flat.push({
            ...(typeof p === 'string' ? { italiano: p } : p),
            capituloTitulo: pIdx === 0 ? capTit : undefined
          });
        });
      });
      out.testo = flat;
    }

    if (!out.testo && Array.isArray(out.paragrafi)) {
      out.testo = out.paragrafi;
    }

    // testo como string simples → array de parágrafos
    if (typeof out.testo === 'string') {
      const linhas = out.testo.split(/\n\s*\n|\r\n\s*\r\n/).map(l => l.trim()).filter(Boolean);
      out.testo = linhas.map((l, i) => ({
        id: `p${i}`,
        italiano: l,
        portugues: '',
        parole: []
      }));
    }

    // Normaliza cada bloco/parágrafo dentro de out.testo
    if (Array.isArray(out.testo)) {
      out.testo = out.testo.map((p, idx) => {
        if (typeof p === 'string') {
          return { id: `p${idx}`, italiano: p, portugues: '', parole: [] };
        }
        const it = (p.italiano || p.it || p.testo || p.testo_italiano || p.frase || p.paragrafo || '').trim();
        const pt = (p.portugues || p.traducao || p.traduzione || p.pt || p.portoghese || p.traducao_pt || p.translation || '').trim();
        const parole = Array.isArray(p.parole) ? p.parole.map(w => ({
          parola: w.parola || w.word || w.termo || '',
          traduzione: w.traduzione || w.traducao || w.trad || w.translation || '',
          ipa: w.ipa || '',
          categoria: w.categoria || ''
        })) : [];

        return {
          id: p.id || `p${idx}`,
          italiano: it,
          portugues: pt,
          parole: parole,
          capituloTitulo: p.capituloTitulo
        };
      });
    }

    return out;
  },

  _salvarStoriaCustomAtualizada(storia) {
    if (!storia) return;
    try {
      const custom = JSON.parse(localStorage.getItem('it_storie_custom') || '[]');
      const idx = custom.findIndex(s => s.id === storia.id);
      if (idx !== -1) {
        custom[idx] = storia;
        localStorage.setItem('it_storie_custom', JSON.stringify(custom));
      }
    } catch (_) {}
  },

  _salvarCompletate() {
    localStorage.setItem('it_storie_lidas', JSON.stringify(this.completate));
  },

  // ── Renderizar seletor de histórias ────────────────────────
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('storie-container');
    if (!c) return;

    const todas = this.dados?.storie || [];
    const niveis = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
    const counts = {};
    todas.forEach(s => { counts[s.nivel] = (counts[s.nivel] || 0) + 1; });

    let filtrate = todas;
    if (this._filtroOrigem === 'custom') filtrate = filtrate.filter(s => s._custom || s.custom);
    if (this._filtroOrigem === 'nativo') filtrate = filtrate.filter(s => !s._custom && !s.custom);
    if (this._filtroNivel) filtrate = filtrate.filter(s => s.nivel === this._filtroNivel);
    if (this._filtroTexto) {
      const q = this._filtroTexto.toLowerCase();
      filtrate = filtrate.filter(s =>
        s.titulo.toLowerCase().includes(q) ||
        (s.titulo_pt || '').toLowerCase().includes(q) ||
        (s.autor || '').toLowerCase().includes(q)
      );
    }

    const labels = I18n.idioma === 'it'
      ? { tut: 'Tutte', cerca: '🔍 Titolo o autore...', nenhuma: 'Nessuna storia ancora.', risultato: 'Nessun risultato.' }
      : { tut: 'Todas', cerca: '🔍 Título ou autor...', nenhuma: 'Nenhuma história ainda.', risultato: 'Nenhum resultado.' };

    // Cores para cada nível CEFR
    const corNivel = { A1:'#27AE60', A2:'#1ABC9C', B1:'#2980B9', B2:'#8E44AD', C1:'#E67E22', C2:'#C0392B' };

    let html = `
      <!-- Linha 1: busca + ação -->
      <div style="display:flex;gap:0.5rem;align-items:center;margin-bottom:0.55rem">
        <input type="search" placeholder="${labels.cerca}" value="${this._filtroTexto}"
          oninput="Storie._filtroTexto=this.value;Storie.renderizarSeletor()"
          style="flex:1;min-width:0;padding:0.45rem 0.8rem;border:1.5px solid var(--cor-pietra);border-radius:20px;font-size:0.88rem;background:var(--cor-marmore);color:var(--cor-inchiostro);font-family:inherit">
        <button class="btn-ia-add" onclick="IAImport.abrir('storia')" style="white-space:nowrap">🤖 via IA</button>
      </div>
      <!-- Linha 2: filtros -->
      <div style="display:flex;gap:0.35rem;flex-wrap:wrap;margin-bottom:1rem;align-items:center">
        ${(()=>{const nC=todas.filter(s=>s._custom||s.custom).length;const nN=todas.length-nC;const _o=this._filtroOrigem;
          const oP=(v,l,ct)=>`<button onclick="Storie._filtroOrigem='${v}';Storie.renderizarSeletor()" style="padding:0.22rem 0.6rem;border-radius:999px;border:1.5px solid ${_o===v?'#7B68A0':'#ccc'};background:${_o===v?'#7B68A0':'transparent'};color:${_o===v?'#fff':'var(--cor-inchiostro)'};cursor:pointer;font-size:0.75rem;font-weight:600;white-space:nowrap;font-family:inherit">${l} (${ct})</button>`;
          return oP('','Todas',todas.length)+(nC?oP('custom','🤖 Adicionadas',nC):'')+oP('nativo','📚 Nativas',nN);
        })()}
        <select class="nivel-select${this._filtroNivel?' ativo':''}"
          onchange="Storie._filtroNivel=this.value;Storie.renderizarSeletor()">
          <option value="">🎯 Nível</option>
          ${niveis.filter(n=>counts[n]).map(n=>`<option value="${n}" ${this._filtroNivel===n?'selected':''}>${n} (${counts[n]})</option>`).join('')}
        </select>
      </div>
      <!-- Grid de histórias -->
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:1rem">`;

    for (const s of filtrate) {
      const isLida = this.completate.includes(s.id);
      const corN = corNivel[s.nivel] || '#9B2335';
      html += `
        <div onclick="Storie.abrirStoria('${s.id}')"
          style="background:var(--cor-marmore);border-radius:14px;padding:1.2rem 1rem;text-align:center;
                 box-shadow:0 3px 12px rgba(0,0,0,0.09);cursor:pointer;border:2px solid transparent;
                 transition:transform 0.18s,box-shadow 0.18s,border-color 0.18s;
                 display:flex;flex-direction:column;align-items:center;gap:0.35rem"
          onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 22px rgba(0,0,0,0.14)';this.style.borderColor='${corN}'"
          onmouseout="this.style.transform='';this.style.boxShadow='0 3px 12px rgba(0,0,0,0.09)';this.style.borderColor='transparent'">
          <div style="font-size:2.4rem;line-height:1.1">${s.icone||'📜'}</div>
          <div style="font-family:'Cinzel',serif;font-size:0.88rem;font-weight:700;color:var(--cor-veneziano-escuro);line-height:1.3">
            ${s.titulo}${isLida?'<span style="font-size:0.6rem;background:#2A9D8F;color:#fff;padding:0.08rem 0.35rem;border-radius:4px;margin-left:0.3rem;vertical-align:middle">✓</span>':''}${s._custom?'<span class="ia-custom-badge">IA</span>':''}
          </div>
          ${s._custom?`<button class="ia-del-btn" onclick="event.stopPropagation();IAImport.excluir('storia','${s.id}')">🗑️ Remover</button>`:''}
          <div style="font-size:0.72rem;color:var(--cor-pietra);font-style:italic">${s.autor||''}</div>
          <div style="display:flex;gap:0.4rem;align-items:center;margin-top:0.2rem">
            <span style="font-size:0.7rem;font-weight:800;padding:0.1rem 0.5rem;border-radius:6px;background:${corN};color:#fff">${s.nivel}</span>
            <span style="font-size:0.72rem;color:${corN};font-weight:700">+${s.xp_recompensa||50} XP</span>
          </div>
        </div>`;
    }

    if (filtrate.length === 0) {
      html += `<p style="text-align:center;color:#aaa;font-style:italic;grid-column:1/-1;padding:2rem 0">${this._filtroTexto?labels.risultato:labels.nenhuma}</p>`;
    }

    html += '</div>';
    c.innerHTML = html;
  },

  // ── Utilitários do Leitor de Livro ──────────────────────────
  _isMobile() {
    return window.innerWidth < 768;
  },

  // Som de folhear papel mais rico e texturizado
  _tocarSomFolhear() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const dur = 0.22;
      const bufferSize = Math.floor(ctx.sampleRate * dur);
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);

      // Ruído filtrado simulando atrito de páginas antigas com decaimento exponencial
      for (let i = 0; i < bufferSize; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (bufferSize * 0.4));
      }

      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(800, ctx.currentTime);
      filter.frequency.exponentialRampToValueAtTime(300, ctx.currentTime + dur);
      filter.Q.value = 1.5;

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.12, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start();
    } catch (_) {}
  },

  // ── Cálculo Geométrico Real por Orçamento de Linhas (Line-Budget) ──
  _calcularOrcamentoGeometria(isMobile) {
    const winW = (typeof window !== 'undefined' && window.innerWidth) ? window.innerWidth : 1200;
    const winH = (typeof window !== 'undefined' && window.innerHeight) ? window.innerHeight : 800;

    if (isMobile) {
      // Mobile: 1 folha vertical.
      // Altura líquida útil descontando topo, rodapé e margens internas
      const alturaUtil = Math.max(320, winH - 170);
      const alturaLinha = this.traduzirVisivel ? 24 : 26;
      const linhasDisponiveis = Math.floor(alturaUtil / alturaLinha);
      // Caracteres por linha com base na largura real do aparelho (36-48 chars)
      const charsPorLinha = Math.max(36, Math.min(48, Math.floor((winW - 50) / 8.5)));
      const linhasCapa = Math.max(8, Math.floor(linhasDisponiveis * 0.45));
      return { linhasDisponiveis, charsPorLinha, linhasCapa };
    } else {
      // Desktop / Tablet: 2 folhas lado a lado em spread aberto
      const alturaUtil = Math.max(400, winH - 200);
      const alturaLinha = this.traduzirVisivel ? 25 : 28;
      const linhasDisponiveis = Math.floor(alturaUtil / alturaLinha);
      // Largura de cada folha (~60 a 76 chars por linha)
      const larguraFolha = Math.min(580, Math.max(420, (winW - 120) / 2));
      const charsPorLinha = Math.max(58, Math.floor(larguraFolha / 7.5));
      const linhasCapa = Math.max(10, Math.floor(linhasDisponiveis * 0.45));
      return { linhasDisponiveis, charsPorLinha, linhasCapa };
    }
  },

  // ── Gerador de Páginas Responsivo de Alta Densidade Editorial ────
  _gerarPaginas(s, isMobile) {
    if (!s || !Array.isArray(s.testo) || s.testo.length === 0) return [];

    const geo = this._calcularOrcamentoGeometria(isMobile);
    const paginas = [];
    let blocosAtuais = [];
    let linhasAtuais = 0;
    let isFirstPage = true;
    let capituloAtivo = s.titulo || 'Capitolo 1';

    const empilharPagina = () => {
      if (blocosAtuais.length === 0) return;
      paginas.push({
        numero: paginas.length + 1,
        isFirstPage: paginas.length === 0,
        capituloTitulo: capituloAtivo,
        blocos: [...blocosAtuais]
      });
      blocosAtuais = [];
      linhasAtuais = 0;
      isFirstPage = false;
    };

    // Calcula o custo vertical em linhas do parágrafo (considerando tradução quando ativa)
    const calcularCustoLinhas = (lenIt, lenPt) => {
      const linIt = Math.ceil(lenIt / geo.charsPorLinha);
      if (this.traduzirVisivel) {
        const linPt = Math.ceil((lenPt || lenIt) / geo.charsPorLinha);
        return linIt + linPt + 1.2;
      }
      return linIt + 0.8;
    };

    // Decompõe parágrafos longos em sentenças naturais
    const fatiarEmSentencas = (texto) => {
      if (!texto) return [];
      return (texto.match(/[^.!?\n]+(?:[.!?\n]+|$)/g) || [texto]).map(s => s.trim()).filter(Boolean);
    };

    s.testo.forEach((p, parIdx) => {
      const textoIt = (p.italiano || '').trim();
      const textoPt = (p.portugues || '').trim();
      const parole = p.parole || [];
      if (!textoIt) return;

      // Detecção de novo capítulo no fluxo de leitura
      const matchCap = textoIt.match(/^(?:###\s*|Capitolo\s+\d+|Capítulo\s+\d+|Parte\s+\d+)/i);
      if (matchCap && blocosAtuais.length > 0) {
        empilharPagina();
        capituloAtivo = textoIt.replace(/^###\s*/, '').trim();
      }

      const limiteFolha = () => isFirstPage ? geo.linhasCapa : geo.linhasDisponiveis;
      const custoParagrafo = calcularCustoLinhas(textoIt.length, textoPt.length);

      // 1. O parágrafo cabe INTEIRO na folha atual: preserva integridade total
      if (linhasAtuais + custoParagrafo <= limiteFolha()) {
        blocosAtuais.push({
          italiano: textoIt,
          portugues: textoPt,
          parole: parole,
          parIdx: parIdx,
          continua: false,
          temCapitular: isFirstPage && blocosAtuais.length === 0
        });
        linhasAtuais += custoParagrafo;
        return;
      }

      // 2. O parágrafo não cabe na folha atual:
      // Se a folha atual já está bem preenchida (>= 58%), NÃO quebra o parágrafo no fim;
      // Inicia o parágrafo inteiro no topo da folha seguinte, mantendo a coesão da leitura.
      if (linhasAtuais > 0 && (linhasAtuais / limiteFolha() >= 0.58)) {
        empilharPagina();
        const novoLimite = limiteFolha();
        if (custoParagrafo <= novoLimite) {
          blocosAtuais.push({
            italiano: textoIt,
            portugues: textoPt,
            parole: parole,
            parIdx: parIdx,
            continua: false,
            temCapitular: isFirstPage && blocosAtuais.length === 0
          });
          linhasAtuais += custoParagrafo;
          return;
        }
      }

      // 3. Folha tem espaço sobrando (< 58%) OU parágrafo é maior que uma folha inteira:
      // Quebra suavemente nas fronteiras de frases para preencher a folha sem cortes cegos
      const sentencasIt = fatiarEmSentencas(textoIt);
      const sentencasPt = fatiarEmSentencas(textoPt);

      let bufferIt = '';
      let chunkStartIdx = 0;
      let ePrimeiraFatia = true;

      sentencasIt.forEach((sent, sIdx) => {
        const proporcao = textoPt.length / (textoIt.length || 1);
        const custoSent = calcularCustoLinhas(sent.length, Math.round(sent.length * proporcao));
        const lim = limiteFolha();

        if (linhasAtuais + custoSent > lim && bufferIt.trim()) {
          // Extrai a fatia correspondente de português proporcionalmente
          let ptChunk = '';
          if (sentencasPt.length > 0) {
            const ptStart = Math.floor((chunkStartIdx / sentencasIt.length) * sentencasPt.length);
            const ptEnd = Math.floor((sIdx / sentencasIt.length) * sentencasPt.length);
            ptChunk = sentencasPt.slice(ptStart, Math.max(ptStart + 1, ptEnd)).join(' ').trim();
          }

          blocosAtuais.push({
            italiano: bufferIt.trim(),
            portugues: ptChunk,
            parole: parole,
            parIdx: parIdx,
            continua: !ePrimeiraFatia,
            temCapitular: ePrimeiraFatia && isFirstPage && blocosAtuais.length === 0
          });

          empilharPagina();
          bufferIt = sent;
          chunkStartIdx = sIdx;
          linhasAtuais = custoSent;
          ePrimeiraFatia = false;
        } else {
          bufferIt += (bufferIt ? ' ' : '') + sent;
          linhasAtuais += custoSent;
        }
      });

      if (bufferIt.trim()) {
        let ptChunk = '';
        if (sentencasPt.length > 0) {
          const ptStart = Math.floor((chunkStartIdx / sentencasIt.length) * sentencasPt.length);
          ptChunk = sentencasPt.slice(ptStart).join(' ').trim();
        }

        blocosAtuais.push({
          italiano: bufferIt.trim(),
          portugues: ptChunk,
          parole: parole,
          parIdx: parIdx,
          continua: !ePrimeiraFatia,
          temCapitular: ePrimeiraFatia && isFirstPage && blocosAtuais.length === 0
        });
      }
    });

    empilharPagina();
    return paginas;
  },

  // ── Abrir história em modo livro autêntico ──────────────────
  async abrirStoria(id) {
    await this.carregar();
    const lista = this.dados?.storie || [];
    const idx   = lista.findIndex(x => x.id === id);
    if (idx === -1) return;
    this.storAttuale   = lista[idx];
    this._storyIndex   = idx;
    this.traduzirVisivel = false;
    this._indiceAberto   = false;

    // Gera as páginas com base no tamanho de tela atual
    this._paginas = this._gerarPaginas(this.storAttuale, this._isMobile());

    // Restaura marcador de página salvo ou inicia na 1
    const bookmarkSalvo = localStorage.getItem('it_book_bm_' + id);
    let pagInicial = bookmarkSalvo ? parseInt(bookmarkSalvo, 10) : 1;
    if (isNaN(pagInicial) || pagInicial < 1) pagInicial = 1;
    if (pagInicial > this._paginas.length) pagInicial = this._paginas.length;

    // Em desktop, garante abertura na página ímpar do spread
    if (!this._isMobile() && pagInicial % 2 === 0) {
      pagInicial = Math.max(1, pagInicial - 1);
    }
    this.paginaAtual = pagInicial;

    this._iniciarListenersLeitor();
    this._renderizarStoria();
  },

  _iniciarListenersLeitor() {
    // Teclado: Setas e Esc
    if (this._keyListener) document.removeEventListener('keydown', this._keyListener);
    this._keyListener = (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault();
        this.proximaPagina();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        this.paginaAnterior();
      } else if (e.key === 'Escape') {
        if (this._indiceAberto) {
          this._fecharIndiceCapitulos();
        } else if (document.getElementById('storie-word-modal')?.style.display === 'block') {
          this._fecharModal();
        } else {
          this.fecharLeitor();
        }
      }
    };
    document.addEventListener('keydown', this._keyListener);

    // Resize com debounce para reajustar paginação
    if (this._resizeListener) window.removeEventListener('resize', this._resizeListener);
    let resizeTimer = null;
    this._resizeListener = () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        if (!this.storAttuale) return;
        const totalAntigo = this._paginas.length || 1;
        const proporcao = this.paginaAtual / totalAntigo;
        this._paginas = this._gerarPaginas(this.storAttuale, this._isMobile());
        let novaPag = Math.round(proporcao * this._paginas.length);
        if (novaPag < 1) novaPag = 1;
        if (!this._isMobile() && novaPag % 2 === 0) novaPag = Math.max(1, novaPag - 1);
        this.paginaAtual = Math.min(novaPag, this._paginas.length);
        this._renderizarStoria();
      }, 220);
    };
    window.addEventListener('resize', this._resizeListener);
  },

  fecharLeitor() {
    this._pararAudioPagina();
    this._animandoVirada = false;
    if (this._keyListener) {
      document.removeEventListener('keydown', this._keyListener);
      this._keyListener = null;
    }
    if (this._resizeListener) {
      window.removeEventListener('resize', this._resizeListener);
      this._resizeListener = null;
    }
    this._fecharModal();
    const overlay = document.getElementById('book-reader-overlay');
    if (overlay) overlay.remove();
    this.renderizarSeletor();
  },

  // ── Renderizar Leitor Imersivo Sem Rolagem ──────────────────
  _renderizarStoria() {
    if (!this.storAttuale) return;
    const s = this.storAttuale;
    const il = I18n.idioma === 'it';
    const total = this._paginas.length;
    const isMobile = this._isMobile();

    // Garante que paginaAtual está nos limites válidos
    if (this.paginaAtual < 1) this.paginaAtual = 1;
    if (this.paginaAtual > total) this.paginaAtual = Math.max(1, total);
    if (!isMobile && this.paginaAtual % 2 === 0) this.paginaAtual -= 1;

    // Páginas a exibir
    const pagEsq = isMobile ? null : (this._paginas[this.paginaAtual - 1] || null);
    const pagDir = isMobile
      ? (this._paginas[this.paginaAtual - 1] || null)
      : (this._paginas[this.paginaAtual] || null);

    const tituloExibido = il ? s.titulo : (s.titulo_pt || s.titulo);
    const bookmarkSalvo = parseInt(localStorage.getItem('it_book_bm_' + s.id) || '0', 10);
    const isBookmarkAtual = bookmarkSalvo === this.paginaAtual || (!isMobile && bookmarkSalvo === this.paginaAtual + 1);

    // Contagem da barra inferior
    const textoProgresso = isMobile
      ? `${il ? 'Pagina' : 'Página'} ${this.paginaAtual} ${il ? 'di' : 'de'} ${total}`
      : `${il ? 'Pagine' : 'Páginas'} ${this.paginaAtual}–${Math.min(this.paginaAtual + 1, total)} ${il ? 'di' : 'de'} ${total}`;

    const isFim = isMobile ? (this.paginaAtual >= total) : (this.paginaAtual + 1 >= total);

    // Cria ou recupera container do leitor
    let overlay = document.getElementById('book-reader-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'book-reader-overlay';
      overlay.className = 'book-reader-overlay';
      document.body.appendChild(overlay);
    }

    const html = `
      <!-- BARRA SUPERIOR SLIM -->
      <header class="book-top-bar">
        <div class="book-top-left">
          <button class="book-btn-voltar" onclick="Storie.fecharLeitor()" title="${il ? 'Chiudi' : 'Fechar'}">
            ‹ <span>${il ? 'Storie' : 'Histórias'}</span>
          </button>
          <div class="book-top-title-wrap">
            <span class="book-top-title">${tituloExibido}</span>
            <span class="book-top-subtitle">${s.autor || 'Letteratura'} · ${s.nivel}</span>
          </div>
        </div>

        <div class="book-top-actions">
          <button class="book-action-btn" onclick="Storie._abrirIndiceCapitulos()" title="${il ? 'Indice dei capitoli' : 'Índice de capítulos'}">
            📑 <span class="label">${il ? 'Indice' : 'Capítulos'}</span>
          </button>
          <button class="book-action-btn${isBookmarkAtual ? ' active' : ''}" onclick="Storie._toggleSegnalibro()" title="${il ? 'Segnalibro' : 'Marcador de página'}">
            🔖 <span class="label">${isBookmarkAtual ? (il ? 'Salvato' : 'Marcada') : (il ? 'Segna' : 'Marcar')}</span>
          </button>
          <button class="book-action-btn${this.traduzirVisivel ? ' active' : ''}" onclick="Storie._toggleTraduzir()" title="${il ? 'Mostra/Nascondi traduzione' : 'Mostrar/Ocultar tradução'}">
            👁️ <span class="label">${il ? 'Traduzione' : 'Tradução'}</span>
          </button>
          <button id="book-btn-ouvir" class="book-action-btn${this._reproduzindoAudio ? ' active' : ''}" onclick="Storie._ouvirPaginaAtual()" title="${this._reproduzindoAudio ? (il ? 'Ferma lettura' : 'Parar leitura') : (il ? 'Ascolta pagina' : 'Ouvir página')}">
            ${this._reproduzindoAudio ? '⏹️' : '🔊'} <span class="label">${this._reproduzindoAudio ? (il ? 'Ferma' : 'Parar') : (il ? 'Ascolta' : 'Ouvir')}</span>
          </button>
          <button class="book-btn-voltar" style="padding:0.32rem 0.5rem" onclick="Storie.fecharLeitor()">✕</button>
        </div>
      </header>

      <!-- PALCO CENTRAL: LIVRO FÍSICO 3D (ZERO ROLAGEM) -->
      <main class="book-stage">
        <div class="antique-book" id="antique-book-element">
          <!-- Vinco central e sombra de lombada 3D -->
          <div class="book-spine-crease"></div>

          <!-- PÁGINA ESQUERDA (Desktop/Tablet) -->
          ${!isMobile ? this._construirHtmlPagina(pagEsq, 'left', total) : ''}

          <!-- PÁGINA DIREITA (Desktop ou Única em Mobile) -->
          ${this._construirHtmlPagina(pagDir, 'right', total)}
        </div>
      </main>

      <!-- BARRA INFERIOR DE NAVEGAÇÃO SLIM -->
      <footer class="book-bottom-bar">
        <button class="book-nav-btn" onclick="Storie.paginaAnterior()" ${this.paginaAtual <= 1 ? 'disabled' : ''}>
          ◀ <span>${il ? 'Precedente' : 'Anterior'}</span>
        </button>

        <div class="book-progress-wrap">
          <span class="book-progress-text">${textoProgresso}</span>
          <input type="range" class="book-progress-slider" min="1" max="${total}" value="${this.paginaAtual}"
            oninput="Storie.irParaPagina(parseInt(this.value, 10))">
        </div>

        ${isFim ? `
          <button class="book-nav-btn" style="background:#2A9D8F;border-color:#227D72" onclick="Storie._marcarLida()">
            ✓ <span>${this.completate.includes(s.id) ? (il ? 'Completata' : 'Concluída') : `+${s.xp_recompensa || 50} XP`}</span>
          </button>
        ` : `
          <button class="book-nav-btn" onclick="Storie.proximaPagina()">
            <span>${il ? 'Successiva' : 'Próxima'}</span> ▶
          </button>
        `}
      </footer>

      <!-- Modal flutuante de palavra -->
      <div id="storie-word-modal" class="storie-word-modal" style="display:none"></div>
      <div id="storie-modal-overlay" onclick="Storie._fecharModal()" style="display:none"></div>

      <!-- Drawer de Capítulos -->
      ${this._indiceAberto ? this._construirHtmlDrawerCapitulos() : ''}
    `;

    overlay.innerHTML = html;

    // Delegação de cliques em palavras
    overlay.querySelectorAll('.storie-texto-corrido').forEach(textoEl => {
      textoEl.addEventListener('click', (e) => {
        const wordEl = e.target.closest('.storie-palavra');
        if (wordEl) {
          e.stopPropagation();
          this._abrirModalPalavra(wordEl);
        } else {
          this._fecharModal();
        }
      });
    });

    // Gestos de Touch Swipe no livro físico
    const bookEl = document.getElementById('antique-book-element');
    if (bookEl) {
      bookEl.addEventListener('touchstart', (e) => {
        if (e.touches && e.touches[0]) {
          this._touchStartX = e.touches[0].clientX;
          this._touchStartY = e.touches[0].clientY;
        }
      }, { passive: true });

      bookEl.addEventListener('touchend', (e) => {
        if (!e.changedTouches || !e.changedTouches[0]) return;
        const diffX = e.changedTouches[0].clientX - this._touchStartX;
        const diffY = e.changedTouches[0].clientY - this._touchStartY;
        if (Math.abs(diffX) > 45 && Math.abs(diffX) > Math.abs(diffY)) {
          if (diffX < 0) {
            this.proximaPagina();
          } else {
            this.paginaAnterior();
          }
        }
      }, { passive: true });
    }

    if (this.traduzirVisivel) {
      this._autoTraduzirPaginasVisiveis();
    }
  },

  // ── Conteúdo Interno da Página de Livro ────────────────────
  _obterHtmlConteudoPagina(pag, lado, total) {
    const il = I18n.idioma === 'it';
    if (!pag) {
      return `
        <div class="antique-page-header">
          <span class="antique-running-head">—</span>
        </div>
        <div class="antique-page-body" style="align-items:center;justify-content:center;opacity:0.65">
          <div style="font-size:2.2rem;margin-bottom:0.4rem">⚜️</div>
          <div class="antique-ornamento">— ✦ —</div>
          <div style="font-family:'EB Garamond',serif;font-style:italic;font-size:0.95rem;color:#8a7250">
            ${il ? 'Fine del volume' : 'Fim do livro'}
          </div>
        </div>
        <div class="antique-page-footer">— ${total} —</div>
      `;
    }

    const s = this.storAttuale;
    const tituloExibido = il ? s.titulo : (s.titulo_pt || s.titulo);

    let cabecalhoHtml = '';
    if (pag.isFirstPage) {
      cabecalhoHtml = `
        <div class="antique-cover-header">
          <span class="antique-cover-icon">${s.icone || '📖'}</span>
          <h2 class="antique-cover-title">${tituloExibido}</h2>
          <div class="antique-cover-subtitle">${s.autor || 'Letteratura Italiana'} ${s.tema ? '· ' + s.tema : ''}</div>
          <div class="antique-ornamento">— ✦ —</div>
        </div>
      `;
    } else {
      cabecalhoHtml = `
        <div class="antique-page-header">
          <span class="antique-running-head">${pag.capituloTitulo || tituloExibido}</span>
        </div>
      `;
    }

    const blocosHtml = pag.blocos.map((bloco, bIdx) => {
      const textoMarcado = this._marcarPalavras(bloco.italiano, bloco.parole || [], bloco.parIdx, bloco.temCapitular && bIdx === 0);
      const ptText = (bloco.portugues || '').replace(/</g, '&lt;');
      const noIndent = bloco.continua || (bloco.temCapitular && bIdx === 0);
      return `
        <div class="antique-para-wrap">
          <p class="antique-para${noIndent ? ' no-indent' : ''}">${textoMarcado}</p>
          ${this.traduzirVisivel ? `
            <span class="antique-para-trad" data-bloco-id="${bloco.parIdx}">${ptText || '<span class="trad-loading">Traduzione in corso...</span>'}</span>
          ` : ''}
        </div>
      `;
    }).join('');

    const isUltima = pag.numero === total;
    const finalizadorHtml = isUltima ? `
      <div style="margin-top:auto;text-align:center;padding:0.25rem 0">
        <div class="antique-ornamento">— ✦ —</div>
        <div style="font-family:'EB Garamond',serif;font-style:italic;font-size:0.85rem;color:#8a7250">
          ${il ? 'Fine' : 'Fim'}
        </div>
      </div>
    ` : '';

    return `
      ${cabecalhoHtml}
      <div class="antique-page-body">
        ${blocosHtml}
        ${finalizadorHtml}
      </div>
      <div class="antique-page-footer">— ${pag.numero} —</div>
    `;
  },

  // ── Construtor de Página Clássica de Livro ──────────────────
  _construirHtmlPagina(pag, lado, total) {
    return `
      <div class="antique-page antique-page-${lado} storie-texto-corrido">
        ${this._obterHtmlConteudoPagina(pag, lado, total)}
      </div>
    `;
  },

  // ── Transição Animada 3D da Página com Verso Real (RotateY) ─
  _animarViradaPagina(direcao, callbackFinal) {
    if (this._animandoVirada) return;

    const stage = document.getElementById('antique-book-element');
    if (!stage || this._isMobile()) {
      // No mobile ou se faltar elemento, executa com som e callback direto
      this._tocarSomFolhear();
      callbackFinal();
      return;
    }

    this._animandoVirada = true;
    this._tocarSomFolhear();

    const isNext = direcao === 'next';
    const total = this._paginas.length;
    const flippingContainer = document.createElement('div');
    flippingContainer.className = `page-flipping-container ${isNext ? 'right-to-left' : 'left-to-right'}`;

    const pageRightEl = stage.querySelector('.antique-page-right');
    const pageLeftEl  = stage.querySelector('.antique-page-left');

    let pagFrente = null;
    let pagVerso  = null;
    let ladoFrente = '';
    let ladoVerso  = '';

    if (isNext) {
      ladoFrente = 'right';
      ladoVerso  = 'left';
      // Folha da direita (frente) gira para a esquerda (verso)
      pagFrente = this._paginas[this.paginaAtual] || null; // página atual da direita (N+1)
      pagVerso  = this._paginas[this.paginaAtual + 1] || null; // nova página da esquerda (N+2)
      const pagSubjacente = this._paginas[this.paginaAtual + 2] || null; // nova página da direita (N+3)

      // Atualiza a página direita estática do livro por baixo da folha que vai girar
      if (pageRightEl) {
        pageRightEl.innerHTML = this._obterHtmlConteudoPagina(pagSubjacente, 'right', total);
      }
    } else {
      ladoFrente = 'left';
      ladoVerso  = 'right';
      // Folha da esquerda (frente) gira para a direita (verso)
      pagFrente = this._paginas[this.paginaAtual - 1] || null; // página atual da esquerda (N)
      pagVerso  = this._paginas[this.paginaAtual - 2] || null; // nova página da direita (N-1)
      const pagSubjacente = this._paginas[this.paginaAtual - 3] || null; // nova página da esquerda (N-2)

      // Atualiza a página esquerda estática do livro por baixo da folha que vai girar
      if (pageLeftEl) {
        pageLeftEl.innerHTML = this._obterHtmlConteudoPagina(pagSubjacente, 'left', total);
      }
    }

    const conteudoFrenteHtml = this._obterHtmlConteudoPagina(pagFrente, ladoFrente, total);
    const conteudoVersoHtml  = this._obterHtmlConteudoPagina(pagVerso, ladoVerso, total);

    flippingContainer.innerHTML = `
      <div class="flipping-face front antique-page antique-page-${ladoFrente}">
        ${conteudoFrenteHtml}
      </div>
      <div class="flipping-face back antique-page antique-page-${ladoVerso}">
        ${conteudoVersoHtml}
      </div>
    `;

    stage.appendChild(flippingContainer);

    // Força reflow e dispara a classe de rotação 3D
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        flippingContainer.classList.add(isNext ? 'turning-next' : 'turning-prev');
      });
    });

    // Remove o elemento temporário após o término da transição CSS (880ms)
    setTimeout(() => {
      flippingContainer.remove();
      this._animandoVirada = false;
      callbackFinal();
    }, 880);
  },

  // ── Auto-tradução On-Demand para Livros / Parágrafos sem PT ───
  async _traduzirParagrafoAPI(texto) {
    if (!texto || !texto.trim()) return '';
    const norm = texto.trim();
    if (this._tradCache[norm]) return this._tradCache[norm];

    // Tenta Google Translate gtx (rápido e sem limite para parágrafos normais)
    try {
      const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=it&tl=pt&dt=t&q=${encodeURIComponent(norm)}`;
      const res = await fetch(url, { signal: AbortSignal.timeout(4500) });
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && Array.isArray(data[0])) {
          const trad = data[0].map(item => item[0]).join('');
          if (trad) {
            this._tradCache[norm] = trad;
            return trad;
          }
        }
      }
    } catch (_) {}

    // Fallback: MyMemory API
    try {
      const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(norm.slice(0, 480))}&langpair=it|pt-BR`;
      const res = await fetch(url, { signal: AbortSignal.timeout(4500) });
      if (res.ok) {
        const json = await res.json();
        const t = json?.responseData?.translatedText;
        if (t && t.toLowerCase() !== norm.toLowerCase()) {
          this._tradCache[norm] = t;
          return t;
        }
      }
    } catch (_) {}

    return '';
  },

  async _autoTraduzirPaginasVisiveis() {
    if (!this.traduzirVisivel || !this.storAttuale) return;
    const isMobile = this._isMobile();
    const pag1 = this._paginas[this.paginaAtual - 1];
    const pag2 = isMobile ? null : this._paginas[this.paginaAtual];
    const blocosSemTrad = [];

    const coletar = (pag) => {
      if (!pag || !pag.blocos) return;
      pag.blocos.forEach(b => {
        if (!b.portugues && b.italiano) blocosSemTrad.push(b);
      });
    };
    coletar(pag1);
    coletar(pag2);

    if (blocosSemTrad.length === 0) return;

    for (const b of blocosSemTrad) {
      try {
        const trad = await this._traduzirParagrafoAPI(b.italiano);
        if (trad && this.traduzirVisivel) {
          b.portugues = trad;
          if (this.storAttuale.testo && this.storAttuale.testo[b.parIdx]) {
            this.storAttuale.testo[b.parIdx].portugues = trad;
          }
          this._salvarStoriaCustomAtualizada(this.storAttuale);
        }
      } catch (_) {}
    }

    if (this.traduzirVisivel) {
      this._atualizarTextosTraducaoDOM();
    }
  },

  _atualizarTextosTraducaoDOM() {
    const overlay = document.getElementById('book-reader-overlay');
    if (!overlay) return;
    const isMobile = this._isMobile();
    const pag1 = this._paginas[this.paginaAtual - 1];
    const pag2 = isMobile ? null : this._paginas[this.paginaAtual];

    const atualizar = (pag) => {
      if (!pag || !pag.blocos) return;
      pag.blocos.forEach(b => {
        if (b.portugues) {
          const els = overlay.querySelectorAll(`.antique-para-trad[data-bloco-id="${b.parIdx}"]`);
          els.forEach(el => {
            if (el.innerHTML.includes('trad-loading') || !el.textContent.trim()) {
              el.textContent = b.portugues;
              el.style.opacity = '0';
              requestAnimationFrame(() => {
                el.style.transition = 'opacity 0.25s ease';
                el.style.opacity = '1';
              });
            }
          });
        }
      });
    };
    atualizar(pag1);
    atualizar(pag2);
  },

  // ── Navegação de Páginas e Virada 3D ────────────────────────
  proximaPagina() {
    if (this._animandoVirada) return;
    this._pararAudioPagina();
    const step = this._isMobile() ? 1 : 2;
    const total = this._paginas.length;
    if (this.paginaAtual + step > total && (this._isMobile() || this.paginaAtual >= total)) {
      return;
    }

    this._animarViradaPagina('next', () => {
      this.paginaAtual = Math.min(this.paginaAtual + step, total);
      this._salvarBookmarkSilencioso();
      this._renderizarStoria();
    });
  },

  paginaAnterior() {
    if (this._animandoVirada) return;
    this._pararAudioPagina();
    const step = this._isMobile() ? 1 : 2;
    if (this.paginaAtual <= 1) return;

    this._animarViradaPagina('prev', () => {
      this.paginaAtual = Math.max(1, this.paginaAtual - step);
      if (!this._isMobile() && this.paginaAtual % 2 === 0) this.paginaAtual -= 1;
      this._salvarBookmarkSilencioso();
      this._renderizarStoria();
    });
  },

  irParaPagina(num) {
    if (isNaN(num)) return;
    this._pararAudioPagina();
    const total = this._paginas.length;
    let pag = Math.min(Math.max(1, num), total);
    if (!this._isMobile() && pag % 2 === 0) pag -= 1;
    if (pag === this.paginaAtual) return;
    this.paginaAtual = pag;
    this._tocarSomFolhear();
    this._salvarBookmarkSilencioso();
    this._renderizarStoria();
  },

  _salvarBookmarkSilencioso() {
    if (this.storAttuale) {
      localStorage.setItem('it_book_bm_' + this.storAttuale.id, this.paginaAtual);
    }
  },

  _toggleSegnalibro() {
    if (!this.storAttuale) return;
    const id = this.storAttuale.id;
    const chave = 'it_book_bm_' + id;
    const salvo = parseInt(localStorage.getItem(chave) || '0', 10);
    const il = I18n.idioma === 'it';

    if (salvo === this.paginaAtual) {
      localStorage.removeItem(chave);
      App.notificar(il ? 'Segnalibro rimosso' : 'Marcador removido', 'info');
    } else {
      localStorage.setItem(chave, this.paginaAtual);
      App.notificar(il ? `Segnalibro salvato alla pagina ${this.paginaAtual}` : `Marcador salvo na página ${this.paginaAtual}`, 'sucesso');
    }
    this._renderizarStoria();
  },

  _toggleTraduzir() {
    this._pararAudioPagina();
    this.traduzirVisivel = !this.traduzirVisivel;
    // Repagina preservando a proporção de leitura
    const totalAntigo = this._paginas.length || 1;
    const prop = this.paginaAtual / totalAntigo;
    this._paginas = this._gerarPaginas(this.storAttuale, this._isMobile());
    let novaPag = Math.round(prop * this._paginas.length);
    if (novaPag < 1) novaPag = 1;
    if (!this._isMobile() && novaPag % 2 === 0) novaPag = Math.max(1, novaPag - 1);
    this.paginaAtual = Math.min(novaPag, this._paginas.length);
    this._renderizarStoria();
  },

  // ── Reprodução de Áudio Sequencial e Robusta da Página ─────
  _ouvirPaginaAtual() {
    if (!this.storAttuale || !this._paginas || this._paginas.length === 0) return;
    const il = typeof I18n !== 'undefined' && I18n.idioma === 'it';

    // Se já estiver reproduzindo, interrompe (Toggle Stop)
    if (this._reproduzindoAudio) {
      this._pararAudioPagina();
      return;
    }

    const isMobile = this._isMobile();
    const pag1 = this._paginas[this.paginaAtual - 1];
    const pag2 = isMobile ? null : this._paginas[this.paginaAtual];

    const frasesExtraidas = [];
    const coletarFrases = (pag) => {
      if (!pag || !pag.blocos) return;
      pag.blocos.forEach(b => {
        const txt = (b.italiano || '').trim();
        if (!txt) return;
        // Quebra em sentenças naturais para não estourar o buffer do SpeechSynthesis
        const partes = txt.match(/[^.!?\n]+[.!?]+|[^.!?\n]+$/g) || [txt];
        partes.forEach(p => {
          const limpo = p.trim();
          if (limpo) frasesExtraidas.push(limpo);
        });
      });
    };

    coletarFrases(pag1);
    coletarFrases(pag2);

    if (frasesExtraidas.length === 0) {
      if (typeof App !== 'undefined' && App.notificar) {
        App.notificar(il ? 'Nessun testo da ascoltare' : 'Nenhum texto para ouvir nesta página', 'info');
      }
      return;
    }

    this._audioFilaSentencas = frasesExtraidas;
    this._audioIndexSentenca = 0;
    this._reproduzindoAudio  = true;

    // Atualiza botão para estado de parada com destaque
    const btn = document.getElementById('book-btn-ouvir');
    if (btn) {
      btn.innerHTML = `⏹️ <span class="label">${il ? 'Ferma' : 'Parar'}</span>`;
      btn.classList.add('active');
    }

    this._tocarProximaSentenca();
  },

  _tocarProximaSentenca() {
    if (!this._reproduzindoAudio) return;

    if (this._audioIndexSentenca >= this._audioFilaSentencas.length) {
      this._pararAudioPagina();
      return;
    }

    const fraseOriginal = this._audioFilaSentencas[this._audioIndexSentenca];
    const fraseNormalizada = (typeof VoiceEngine !== 'undefined')
      ? VoiceEngine.normalizarParaFala(fraseOriginal)
      : fraseOriginal;

    if (!('speechSynthesis' in window)) {
      if (typeof App !== 'undefined' && App._pronunciarRV) {
        App._pronunciarRV(fraseNormalizada || fraseOriginal);
      }
      this._pararAudioPagina();
      return;
    }

    try {
      if (speechSynthesis.paused) {
        speechSynthesis.resume();
      }
      speechSynthesis.cancel();
    } catch (_) {}

    // Busca a melhor voz italiana
    let voz = null;
    if (typeof VoiceEngine !== 'undefined') {
      voz = VoiceEngine.obterVozSelecionada();
    }
    if (!voz && typeof App !== 'undefined' && App._getVozItaliana) {
      voz = App._getVozItaliana();
    }

    let rate = parseFloat(localStorage.getItem('it_audio_speed'));
    if (isNaN(rate) || rate <= 0) rate = 0.88;
    rate = Math.max(0.5, Math.min(1.8, rate));

    const u = new SpeechSynthesisUtterance(fraseNormalizada || fraseOriginal);
    u.lang = (voz && voz.lang) ? voz.lang : 'it-IT';
    u.rate = rate;
    if (voz) u.voice = voz;

    if (fraseOriginal.endsWith('?')) {
      u.pitch = 1.05;
    } else if (fraseOriginal.endsWith('!')) {
      u.pitch = 1.02;
    } else {
      u.pitch = 1.0;
    }

    // Fix do Chromium Garbage Collector
    window._storyActiveUtterance = u;

    u.onend = () => {
      if (!this._reproduzindoAudio) return;
      this._audioIndexSentenca++;
      setTimeout(() => {
        if (this._reproduzindoAudio) {
          this._tocarProximaSentenca();
        }
      }, 110);
    };

    u.onerror = (e) => {
      console.warn('[Storie Audio Error]', e);
      if (!this._reproduzindoAudio) return;
      this._audioIndexSentenca++;
      setTimeout(() => {
        if (this._reproduzindoAudio) {
          this._tocarProximaSentenca();
        }
      }, 90);
    };

    try {
      speechSynthesis.speak(u);
    } catch (err) {
      console.warn('[Storie Speech Exception]', err);
      this._pararAudioPagina();
    }
  },

  _pararAudioPagina() {
    this._reproduzindoAudio = false;
    this._audioFilaSentencas = [];
    this._audioIndexSentenca = 0;
    window._storyActiveUtterance = null;

    try {
      if (typeof speechSynthesis !== 'undefined') {
        speechSynthesis.cancel();
      }
    } catch (_) {}

    const il = typeof I18n !== 'undefined' && I18n.idioma === 'it';
    const btn = document.getElementById('book-btn-ouvir');
    if (btn) {
      btn.innerHTML = `🔊 <span class="label">${il ? 'Ascolta' : 'Ouvir'}</span>`;
      btn.classList.remove('active');
    }
  },

  // ── Drawer de Capítulos e Índice ───────────────────────────
  _abrirIndiceCapitulos() {
    this._indiceAberto = true;
    this._renderizarStoria();
  },

  _fecharIndiceCapitulos() {
    this._indiceAberto = false;
    this._renderizarStoria();
  },

  _construirHtmlDrawerCapitulos() {
    const il = I18n.idioma === 'it';
    // Mapeia onde cada capítulo começa
    const capitulos = [];
    const capsVistos = new Set();
    this._paginas.forEach(p => {
      const capNome = p.capituloTitulo || (il ? 'Capitolo' : 'Capítulo');
      if (!capsVistos.has(capNome)) {
        capsVistos.add(capNome);
        capitulos.push({ titulo: capNome, pagina: p.numero });
      }
    });

    const itensHtml = capitulos.map(c => {
      const ativo = this.paginaAtual >= c.pagina;
      return `
        <div class="book-chapter-item${ativo ? ' active' : ''}" onclick="Storie.irParaPagina(${c.pagina});Storie._fecharIndiceCapitulos();">
          <span>📖 ${this._escape(c.titulo)}</span>
          <span style="font-size:0.75rem;opacity:0.8">${il ? 'pag.' : 'pág.'} ${c.pagina}</span>
        </div>
      `;
    }).join('');

    return `
      <div class="book-drawer-overlay" onclick="Storie._fecharIndiceCapitulos()">
        <div class="book-drawer" onclick="event.stopPropagation()">
          <div class="book-drawer-header">
            <span class="book-drawer-title">📑 ${il ? 'Indice dei Capitoli' : 'Índice de Capítulos'}</span>
            <button class="book-btn-voltar" style="padding:0.25rem 0.5rem" onclick="Storie._fecharIndiceCapitulos()">✕</button>
          </div>
          <div class="book-drawer-list">
            ${itensHtml}
          </div>
        </div>
      </div>
    `;
  },

  // ── Tokenizar e marcar TODAS as palavras como clicáveis ────
  _marcarPalavras(texto, parole, parIdx, temCapitular = false) {
    if (!texto) return '';
    const tokens = texto.match(/[A-Za-zÀ-öø-ÿ']+|[^A-Za-zÀ-öø-ÿ'\s]+|\s+/g) || [];
    let primeiraWord = temCapitular;

    return tokens.map((tok, wIdx) => {
      if (/^\s+$/.test(tok)) return tok;
      if (/^[^A-Za-zÀ-öø-ÿ']+$/.test(tok)) return this._escape(tok);

      const vocabDado = parole.find(p =>
        this._normWord(p.parola) === this._normWord(tok)
      );
      const jaSalva = this._verificarSalva(tok);

      const classes = ['storie-palavra'];
      if (jaSalva)   classes.push('storie-palavra-salva');
      if (vocabDado) classes.push('storie-palavra-vocab');

      const attrs = [
        `data-palavra="${this._escAttr(tok)}"`,
        `data-par="${parIdx}"`,
        `data-widx="${wIdx}"`,
      ];
      if (vocabDado) {
        if (vocabDado.ipa)        attrs.push(`data-ipa="${this._escAttr(vocabDado.ipa)}"`);
        if (vocabDado.traduzione) attrs.push(`data-trad="${this._escAttr(vocabDado.traduzione)}"`);
        if (vocabDado.categoria)  attrs.push(`data-cat="${this._escAttr(vocabDado.categoria)}"`);
      }

      let inner = this._escape(tok);
      if (primeiraWord) {
        primeiraWord = false;
        inner = `<span class="antique-drop-cap">${this._escape(tok[0])}</span>${this._escape(tok.slice(1))}`;
      }

      return `<span class="${classes.join(' ')}" ${attrs.join(' ')}>${inner}</span>`;
    }).join('');
  },


  _normWord(w) {
    return (w || '').toLowerCase().replace(/[''']/g, "'");
  },

  _escape(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  },

  _escAttr(s) {
    return String(s || '')
      .replace(/&/g,'&amp;').replace(/"/g,'&quot;')
      .replace(/</g,'&lt;').replace(/>/g,'&gt;')
      .replace(/'/g,'&#39;');
  },

  // ── Modal flutuante de palavra ─────────────────────────────
  _abrirModalPalavra(wordEl) {
    this._fecharModal(false);

    const palavra = wordEl.dataset.palavra || wordEl.textContent.trim();
    let ipa  = wordEl.dataset.ipa  || '';
    let trad = wordEl.dataset.trad || '';
    let cat  = wordEl.dataset.cat  || '';

    // Busca global em todos os parágrafos da história
    if (!trad && this.storAttuale) {
      for (const p of this.storAttuale.testo) {
        const found = (p.parole || []).find(pw =>
          this._normWord(pw.parola) === this._normWord(palavra)
        );
        if (found) {
          ipa  = ipa  || found.ipa        || '';
          trad = trad || found.traduzione || '';
          cat  = cat  || found.categoria  || '';
          break;
        }
      }
    }

    const il      = I18n.idioma === 'it';
    const jaSalva = this._verificarSalva(palavra);

    // Se já temos trad do parole[], renderiza direto
    // Caso contrário, verifica cache → mostra placeholder → busca API
    const tradInicial = trad;

    const buildPills = (t) => t
      ? t.split(/[;,]/).map(s => s.trim()).filter(Boolean)
          .map(s => `<span class="storie-trad-pill">${this._escape(s)}</span>`).join('')
      : '';

    const renderModal = (tradAtual, carregando = false) => {
      const pills = buildPills(tradAtual);
      return `
        <button class="storie-modal-close" onclick="Storie._fecharModal()">×</button>
        <div class="storie-modal-palavra">${this._escape(palavra)}</div>
        ${ipa ? `<div class="storie-modal-ipa">${this._escape(ipa)}</div>` : ''}
        <button class="storie-modal-audio" onclick="App.pronunciar('${this._escAttr(palavra)}')">🔊 ${il?'Ascolta':'Ouvir'}</button>
        <div class="storie-modal-traducoes" id="storie-modal-pills">
          ${pills || (carregando ? '<span class="storie-trad-loading">…</span>' : '')}
        </div>
        ${cat ? `<div style="margin-top:0.45rem"><span class="storie-modal-cat">${this._escape(cat)}</span></div>` : ''}
        <button class="storie-modal-salvar${jaSalva?' salvo':''}" id="storie-btn-salvar"
          onclick="Storie._salvarNoDeck('${this._escAttr(palavra)}',{ipa:'${this._escAttr(ipa)}',trad:'${this._escAttr(tradAtual)}',cat:'${this._escAttr(cat)}'})">
          ${jaSalva
            ? `✅ ${il ? 'Già salvata' : 'Já salva'}`
            : `⭐ ${il ? 'Salva per revisione' : 'Salvar para revisão'}`}
        </button>`;
    };

    const modal = document.getElementById('storie-word-modal');
    if (!modal) return;

    // Renderiza imediatamente (com loading se sem trad)
    modal.innerHTML = renderModal(tradInicial, !tradInicial);
    modal.style.display = 'block';
    this._posicionarModal(modal, wordEl);

    const overlay = document.getElementById('storie-modal-overlay');
    if (overlay) overlay.style.display = 'block';

    // Se não tem tradução, busca via API (com cache)
    if (!tradInicial) {
      this._buscarTradAPI(palavra).then(tradAPI => {
        // Verifica se o modal ainda mostra esta palavra
        const pillsEl = document.getElementById('storie-modal-pills');
        if (!pillsEl) return;
        if (tradAPI) {
          pillsEl.innerHTML = buildPills(tradAPI);
          // Atualiza o onclick do botão salvar com a trad real
          const btn = document.getElementById('storie-btn-salvar');
          if (btn) btn.setAttribute('onclick',
            `Storie._salvarNoDeck('${this._escAttr(palavra)}',{ipa:'${this._escAttr(ipa)}',trad:'${this._escAttr(tradAPI)}',cat:'${this._escAttr(cat)}'})`);
        } else {
          pillsEl.innerHTML = '';
        }
      });
    }
  },

  // ── Tradução via MyMemory API (gratuita, sem chave) ────────
  async _buscarTradAPI(palavra) {
    const norm = this._normWord(palavra);
    if (this._tradCache[norm]) return this._tradCache[norm];
    try {
      const url = `https://api.mymemory.translated.net/get?q=${encodeURIComponent(palavra)}&langpair=it|pt-BR`;
      const res  = await fetch(url, { signal: AbortSignal.timeout(4000) });
      const json = await res.json();
      const t    = json?.responseData?.translatedText || '';
      // Filtra respostas ruins (igual à entrada ou muito longas)
      const boa  = t && t.toLowerCase() !== palavra.toLowerCase() && t.split(' ').length <= 4;
      const val  = boa ? t : '';
      this._tradCache[norm] = val;
      return val;
    } catch { return ''; }
  },

  _posicionarModal(modal, wordEl) {
    modal.style.visibility = 'hidden';
    modal.classList.remove('seta-baixo', 'seta-cima');

    // Duplo rAF garante layout computado após display:block
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const rect = wordEl.getBoundingClientRect();
      const mW   = modal.offsetWidth  || 260;
      const mH   = modal.offsetHeight || 200;
      // clientWidth é mais confiável que innerWidth no mobile (ignora scrollbar)
      const vW   = document.documentElement.clientWidth;
      const vH   = document.documentElement.clientHeight;
      const SETA = 9;  // altura da seta CSS em px
      const PAD  = 8;  // margem mínima das bordas do viewport

      // Centro horizontal da palavra
      const wordCX = rect.left + rect.width / 2;

      // Tenta centralizar o modal sobre a palavra
      let left = wordCX - mW / 2;
      // Clamp horizontal
      if (left < PAD)               left = PAD;
      if (left + mW > vW - PAD)     left = vW - mW - PAD;
      // Se ainda não cabe (modal maior que viewport), alinha à esquerda
      if (left < 0) left = PAD;

      // Seta sempre aponta para o centro da palavra, independente do deslocamento do modal
      const arrowLeft = Math.min(Math.max(wordCX - left, 16), mW - 16);
      modal.style.setProperty('--arrow-left', `${arrowLeft}px`);

      // Vertical: prefere acima
      let top;
      let setaDir;
      if (rect.top - mH - SETA - PAD >= 0) {
        top     = rect.top - mH - SETA;
        setaDir = 'seta-baixo';
        modal.style.setProperty('--modal-origin-y', '100%');
      } else {
        top     = rect.bottom + SETA;
        setaDir = 'seta-cima';
        modal.style.setProperty('--modal-origin-y', '0%');
      }

      if (top + mH > vH - PAD) top = vH - mH - PAD;
      if (top < PAD)            top = PAD;

      modal.style.setProperty('--modal-origin-x', `${arrowLeft}px`);
      modal.classList.add(setaDir);
      modal.style.left       = `${left}px`;
      modal.style.top        = `${top}px`;
      modal.style.visibility = 'visible';
    }));
  },

  _fecharModal(removeEsc = true) {
    const modal   = document.getElementById('storie-word-modal');
    const overlay = document.getElementById('storie-modal-overlay');
    if (modal)   modal.style.display   = 'none';
    if (overlay) overlay.style.display = 'none';
    if (removeEsc && this._escListener) {
      document.removeEventListener('keydown', this._escListener);
      this._escListener = null;
    }
  },

  // ── Salvar palavra no deck SRS ─────────────────────────────
  _salvarNoDeck(palavra, dados) {
    if (this._verificarSalva(palavra)) return;

    const id = 'story_' + this._normWord(palavra).replace(/\W/g, '_') + '_' + Date.now();
    const entrada = {
      id,
      italiano:  palavra,
      portugues: dados?.trad || '',
      categoria: dados?.cat  || 'vocabulo',
      templo_num: 0,
      _custom:    true,
      _from_story: true,
    };

    // Persistir em localStorage
    try {
      const key    = 'it_vocab_custom';
      const custom = JSON.parse(localStorage.getItem(key) || '[]');
      if (!custom.find(v => (v.italiano||'').toLowerCase() === palavra.toLowerCase())) {
        custom.push(entrada);
        localStorage.setItem(key, JSON.stringify(custom));
      }
    } catch(e) {}

    // Injetar no vocabCache global
    if (typeof App !== 'undefined' && App.estado?.vocabCache) {
      if (!App.estado.vocabCache.find(v => (v.italiano||'').toLowerCase() === palavra.toLowerCase())) {
        App.estado.vocabCache.unshift(entrada);
        if (App.estado.progresso) {
          App.estado.progresso.total_palavras = App.estado.vocabCache.length;
          App.salvarProgresso();
          App.atualizarStats();
        }
      }
    }

    // Inicializar estado FSRS
    if (typeof App !== 'undefined' && App.estado?.flashcardData) {
      if (!App.estado.flashcardData[id]) {
        App.estado.flashcardData[id] = {
          state: 'new', reps: 0, lapses: 0,
          stability: 0, difficulty: 5,
          nextReview: Date.now(),
        };
        if (App.salvarFlashcards) App.salvarFlashcards();
      }
    }

    // Feedback visual no botão
    const btn = document.getElementById('storie-btn-salvar');
    if (btn) {
      const il = I18n.idioma === 'it';
      btn.textContent = `✅ ${il ? 'Già salvata' : 'Já salva'}`;
      btn.classList.add('salvo');
    }

    // Destaca todas as ocorrências no texto
    this._marcarPalavraSalvaNoDOM(palavra);
  },

  _verificarSalva(palavra) {
    if (typeof App === 'undefined' || !App.estado?.vocabCache) return false;
    const norm = (palavra || '').toLowerCase();
    return App.estado.vocabCache.some(v => (v.italiano || '').toLowerCase() === norm);
  },

  _marcarPalavraSalvaNoDOM(palavra) {
    const norm = (palavra || '').toLowerCase();
    document.querySelectorAll('.storie-palavra').forEach(el => {
      if ((el.dataset.palavra || '').toLowerCase() === norm) {
        el.classList.add('storie-palavra-salva');
      }
    });
  },

  // ── Ações de Leitura ──────────────────────────────────────

  _marcarLida() {
    if (!this.storAttuale) return;
    const id = this.storAttuale.id;
    const il = I18n.idioma === 'it';
    if (this.completate.includes(id)) {
      App.notificar(il ? 'notif_gia_letta' : 'notif_ja_lida', 'info');
      return;
    }
    this.completate.push(id);
    this._salvarCompletate();
    const xp = this.storAttuale.xp_recompensa || 50;
    if (typeof App !== 'undefined' && App.ganharXP) App.ganharXP(xp);
    App.notificar(il ? `notif_storia_letta_${id}` : `notif_storia_lida_${id}`, 'sucesso');
    this._renderizarStoria();
  },

  // ── Inicialização ao navegar para a aba ────────────────────
  init() {
    this.renderizarSeletor();
  },
};
