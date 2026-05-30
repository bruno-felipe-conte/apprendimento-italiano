// ============================================================
// core.js — Global App state, data loading, navigation, XP
// ============================================================

const App = {
  // ── State ──────────────────────────────────────────────────
  estado: {
    secaoAtiva: 'templi',
    templosData: {},       // { 1: { templo, nome, cidade, nivel, palavras: [] }, ... }
    quizData: [],          // flat array of all quiz questions
    vocabCache: [],        // flat array of all words (with templo_num attached)
    conjugacoesData: [],   // verb conjugation data
    progresso: null,       // persisted in localStorage
    flashcardData: {}      // persisted in localStorage
  },

  // Temple gradient palettes (one per temple index 1-10)
  TEMPLO_CORES: [
    null,
    'linear-gradient(135deg, #9B2335, #6B1525)',   // 1 Roma
    'linear-gradient(135deg, #1A5276, #154360)',   // 2 Venezia
    'linear-gradient(135deg, #1E8449, #145A32)',   // 3 Firenze
    'linear-gradient(135deg, #7D3C98, #5B2C6F)',   // 4 Napoli
    'linear-gradient(135deg, #CA6F1E, #9C4A1A)',   // 5 Milano
    'linear-gradient(135deg, #2E86C1, #1A5276)',   // 6 Bologna
    'linear-gradient(135deg, #C0392B, #922B21)',   // 7 Torino
    'linear-gradient(135deg, #117A65, #0E6655)',   // 8 Palermo
    'linear-gradient(135deg, #6E2F8F, #512E6D)',   // 9 Bari
    'linear-gradient(135deg, #B7950B, #9A7D0A)',   // 10 Siena
  ],

  // Temple names (index = templo number)
  TEMPLO_NOMES: [
    null,
    'Le Fondamenta',       // 1 Roma
    'Il Cuore',            // 2 Venezia
    'Il Viaggio',          // 3 Firenze
    'Il Gusto',            // 4 Napoli
    'Il Tempo',            // 5 Milano
    'La Grammatica',       // 6 Bologna
    'La Conversazione',    // 7 Torino
    'La Cultura',          // 8 Palermo
    'Il Lavoro',           // 9 Bari
    'La Letteratura',      // 10 Siena
  ],

  // XP needed to UNLOCK each temple (minimum level)
  TEMPLO_NIVEL_MINIMO: { 1:1, 2:3, 3:6, 4:10, 5:15, 6:21, 7:28, 8:36, 9:45, 10:55 },

  // Secret unlock code — change to your personal password
  UNLOCK_CODE: '2012',

  // Italian descriptions per temple (difficulty proportional to level)
  TEMPLO_DESC: [
    null,
    // 1 Roma — A1
    'Roma è grande e bella. Qui inizi a parlare italiano. Impari "buongiorno", "grazie", "per favore" — i primi passi. Con queste parole puoi salutare, contare e presentarti. Le fondamenta di tutto.',
    // 2 Venezia — A1→A2
    'Venezia è unica al mondo. In questo tempio parli della famiglia e della casa: chi è tua madre, come si chiama tuo fratello, dove abiti. Impari a descrivere le persone e i luoghi della tua vita quotidiana.',
    // 3 Firenze — A2
    'Firenze è la culla del Rinascimento. Qui trovi tutto il vocabolario per viaggiare in Italia: la stazione, il treno, l\'albergo, le indicazioni stradali. Questo tempio ti prepara per ogni avventura in terra italiana.',
    // 4 Napoli — A2→B1
    'Napoli ha inventato la pizza e ha insegnato al mondo come mangiare con passione. In questo tempio entri nella cucina italiana: ingredienti, piatti tipici, abitudini a tavola. Imparare a parlare di cibo è imparare la cultura italiana.',
    // 5 Milano — B1
    'Milano è veloce, precisa, sempre in movimento. Questo tempio ti insegna a gestire il tempo in italiano — le ore, gli appuntamenti, le stagioni — e a descrivere la tua routine quotidiana con naturalezza e precisione.',
    // 6 Bologna — B1→B2
    'Bologna, sede della più antica università d\'Europa, è il luogo ideale per studiare la struttura della lingua. Qui affronti il congiuntivo, i pronomi relativi, le costruzioni implicite. Non solo regole: impari a pensare in italiano.',
    // 7 Torino — B2
    'Torino, città sobria e intellettuale, è dove si impara a conversare con stile. In questo tempio esplori l\'argomentazione, il dibattito e la cortesia formale. Come si difende un\'opinione? Come si negozia con eleganza? L\'italiano fluente ti aspetta.',
    // 8 Palermo — B2
    'Palermo porta i segni di tutte le civiltà che l\'hanno abitata: greci, arabi, normanni. Questo tempio ti apre al patrimonio culturale dell\'Italia — l\'arte, la storia, le tradizioni regionali di un popolo complesso e affascinante.',
    // 9 Bari — B1→B2
    'Bari, porta d\'Italia verso il Mediterraneo, è una città che lavora. Questo tempio ti fornisce il vocabolario professionale: curriculum, riunioni, negoziazioni. L\'italiano del lavoro richiede precisione e rispetto delle forme.',
    // 10 Siena — B2
    'Siena custodisce il volgare illustre, la lingua di Dante. Nel decimo tempio raggiungi la vetta: il linguaggio della letteratura, della filosofia e dell\'espressione artistica. Le parole non comunicano soltanto — evocano, suggeriscono, trasformano.',
  ],

  // ── Initialization ─────────────────────────────────────────
  async init() {
    this.estado.progresso = this.carregarProgresso();
    this.estado.flashcardData = this.carregarFlashcards();
    await this.carregarDados();
    this.atualizarStats();
    this.renderizarTemplos();
    // Kick off secondary modules once data is ready
    if (typeof Progressao !== 'undefined') Progressao.verificarDesbloqueioTemplos();
    if (typeof Quiz !== 'undefined') Quiz.renderizarSeletor();
    if (typeof Vocab !== 'undefined') {
      Vocab.popularCategorias();
      Vocab.renderizar();
    }
    if (typeof Flashcards !== 'undefined') Flashcards.atualizarSelectTemplo();
    // Render heatmap
    if (typeof Calor !== 'undefined') Calor.renderizar();
    // Init grammar module
    if (typeof Grammatica !== 'undefined') Grammatica.renderizarSeletor();
    // Init sound feedback
    if (typeof SomFeedback !== 'undefined') SomFeedback.init();
    // Set up keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') return;
      if (e.key === '1') this.navegar('templi');
      else if (e.key === '2') this.navegar('flashcard');
      else if (e.key === '3') this.navegar('quiz');
      else if (e.key === '4') this.navegar('vocabolario');
      else if (e.key === '5') this.navegar('grammatica');
    });
  },

  // ── Data loading ───────────────────────────────────────────
  async carregarDados() {
    const promises = [];
    // Load templo-1.json through templo-10.json; skip gracefully on 404
    for (let i = 1; i <= 10; i++) {
      promises.push(
        fetch(`data/templo-${i}.json`)
          .then(r => {
            if (!r.ok) return null;
            return r.json();
          })
          .then(data => {
            if (!data) return;
            // Normalize: JSON files use "vocabulario" or "palavras" — always expose as "palavras"
            const lista = data.palavras || data.vocabulario || [];
            data.palavras = lista.map(p => ({ ...p, templo_num: data.templo }));
            this.estado.vocabCache.push(...data.palavras);
            this.estado.templosData[data.templo] = data;
          })
          .catch(() => null) // network error — skip
      );
    }

    // Load quiz questions
    promises.push(
      fetch('data/quizzes.json')
        .then(r => r.ok ? r.json() : { perguntas: [] })
        .then(data => {
          this.estado.quizData = data.perguntas || [];
        })
        .catch(() => { this.estado.quizData = []; })
    );

    // Load verb conjugations
    promises.push(
      fetch('data/conjugacoes.json')
        .then(r => r.ok ? r.json() : { verbos: [] })
        .then(data => {
          this.estado.conjugacoesData = data.verbos || [];
        })
        .catch(() => { this.estado.conjugacoesData = []; })
    );

    await Promise.all(promises);

    // Update total_palavras in progress
    if (this.estado.progresso) {
      this.estado.progresso.total_palavras = this.estado.vocabCache.length;
      this.salvarProgresso();
    }
  },

  // ── Navigation ─────────────────────────────────────────────
  navegar(secao) {
    this.estado.secaoAtiva = secao;

    // Update tab buttons
    document.querySelectorAll('.nav-tab').forEach(btn => {
      btn.classList.toggle('ativa', btn.dataset.section === secao);
    });

    // Show/hide sections
    document.querySelectorAll('.section').forEach(sec => {
      sec.classList.toggle('active', sec.id === `sec-${secao}`);
    });

    // Lazy-render on first visit
    if (secao === 'vocabolario' && typeof Vocab !== 'undefined') {
      Vocab.renderizar();
    }
    if (secao === 'quiz' && typeof Quiz !== 'undefined') {
      Quiz.renderizarSeletor();
    }
    if (secao === 'flashcard' && typeof Flashcards !== 'undefined') {
      Flashcards.atualizarSelectTemplo();
    }
    if (secao === 'grammatica' && typeof Grammatica !== 'undefined') {
      Grammatica.renderizarSeletor();
    }
    if (secao === 'profilo' && typeof Profilo !== 'undefined') {
      Profilo.renderizar();
    }
  },

  // ── localStorage ───────────────────────────────────────────
  carregarProgresso() {
    try {
      const raw = localStorage.getItem('it_progresso');
      if (raw) {
        const p = JSON.parse(raw);
        // Backward compatibility
        if (!p.grammatica_completadas) p.grammatica_completadas = [];
        if (p.meta_diaria === undefined) p.meta_diaria = 100;
        if (p.xp_hoje === undefined) p.xp_hoje = 0;
        if (p.data_xp_hoje === undefined) p.data_xp_hoje = null;
        if (!p.favoritos)   p.favoritos   = [];
        if (!p.conquistas)  p.conquistas  = [];
        return p;
      }
    } catch (e) { /* ignore */ }
    // Default state
    return {
      nivel: 1,
      xp: 0,
      xp_proximo_nivel: 500,
      templos_desbloqueados: [1],
      templos_concluidos: [],
      total_palavras: 0,
      streak: 0,
      ultimo_estudo: null,
      grammatica_completadas: [],
      meta_diaria: 100,
      xp_hoje: 0,
      data_xp_hoje: null,
      favoritos:   [],
      conquistas:  []
    };
  },

  salvarProgresso() {
    try {
      localStorage.setItem('it_progresso', JSON.stringify(this.estado.progresso));
    } catch (e) { /* ignore */ }
  },

  carregarFlashcards() {
    try {
      const raw = localStorage.getItem('it_flashcards');
      if (raw) return JSON.parse(raw);
    } catch (e) { /* ignore */ }
    return {};
  },

  salvarFlashcards() {
    try {
      localStorage.setItem('it_flashcards', JSON.stringify(this.estado.flashcardData));
    } catch (e) { /* ignore */ }
  },

  // ── Temple grid rendering ──────────────────────────────────
  // ── Parola del Giorno ─────────────────────────────────────
  renderizarParolaDia() {
    const container = document.getElementById('parola-del-giorno');
    if (!container) return;

    // Collect all words from loaded templos
    const vocab = [];
    for (let i = 1; i <= 10; i++) {
      const d = this.estado.templosData[i];
      if (d && d.palavras) d.palavras.forEach(p => vocab.push({ ...p, _templo: i }));
    }
    if (vocab.length === 0) { container.style.display = 'none'; return; }

    // Select deterministically by day of year (same word all day)
    const now   = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const dayN  = Math.floor((now - start) / 86400000);

    // Check localStorage cache
    let cached = null;
    try { cached = JSON.parse(localStorage.getItem('it_palavra_dia') || 'null'); } catch (_) {}
    const todayStr = now.toISOString().slice(0, 10);
    let palavra;
    if (cached && cached.data === todayStr) {
      palavra = vocab.find(p => p.id === cached.id) || vocab[dayN % vocab.length];
    } else {
      palavra = vocab[dayN % vocab.length];
      try { localStorage.setItem('it_palavra_dia', JSON.stringify({ data: todayStr, id: palavra.id })); } catch (_) {}
    }
    if (!palavra) { container.style.display = 'none'; return; }

    const ipa = palavra.audio_ipa
      ? (palavra.audio_ipa.startsWith('/') ? palavra.audio_ipa : `/${palavra.audio_ipa}/`)
      : '';
    const data = now.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' });

    container.innerHTML = `
      <div class="pdd-header">
        <span class="pdd-label">🇮🇹 Parola del Giorno</span>
        <span class="pdd-data">${data}</span>
      </div>
      <div class="pdd-body">
        <div class="pdd-palavra">${palavra.italiano}</div>
        ${ipa ? `<div class="pdd-ipa">${ipa}</div>` : ''}
        <div class="pdd-traducao">${palavra.portugues}</div>
        ${palavra.categoria ? `<span class="pdd-cat">${palavra.categoria}</span>` : ''}
        ${palavra.exemplo ? `<div class="pdd-exemplo">"${palavra.exemplo}"${palavra.exemplo_pt ? ` — ${palavra.exemplo_pt}` : ''}</div>` : ''}
      </div>
      <div class="pdd-acoes">
        <button class="pdd-btn" onclick="App.pronunciar('${palavra.italiano.replace(/'/g, "\\'")}')">🔊 Ascolta</button>
        <button class="pdd-btn pdd-btn-study" onclick="App.estudarTemplo(${palavra._templo})">📚 Studiare</button>
      </div>
    `;
    container.style.display = 'block';
  },

  renderizarTemplos() {
    const grid = document.getElementById('templos-grid');
    if (!grid) return;
    grid.innerHTML = '';

    for (let i = 1; i <= 10; i++) {
      const data = this.estado.templosData[i];
      const desbloqueado = this.estado.progresso.templos_desbloqueados.includes(i);
      const concluido = this.estado.progresso.templos_concluidos.includes(i);
      const nivelMinimo = this.TEMPLO_NIVEL_MINIMO[i] || i;
      const cor = this.TEMPLO_CORES[i] || this.TEMPLO_CORES[1];

      // If data not loaded but temple is unlocked, show placeholder
      const nome = (data && data.nome) ? data.nome : (this.TEMPLO_NOMES[i] || `Tempio ${i}`);
      const cidade = data ? data.cidade : '—';
      const nivel = data ? data.nivel : '—';
      const totalPalavras = data && data.palavras ? data.palavras.length : 0;

      // Calculate mastered words (FSRS: reps >= 3 or stability > 7d; SM-2: repeticoes >= 3)
      let dominadas = 0;
      if (data && data.palavras) {
        dominadas = data.palavras.filter(p => {
          const sm = this.estado.flashcardData[p.id];
          if (!sm) return false;
          return (sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7);
        }).length;
      }

      const progPercent = totalPalavras > 0 ? Math.round((dominadas / totalPalavras) * 100) : 0;

      const card = document.createElement('div');
      card.className = `templo-card${desbloqueado ? '' : ' bloqueado'}${concluido ? ' concluido' : ''}`;

      if (desbloqueado) {
        card.style.cursor = 'pointer';
        card.onclick = () => this.abrirModalTemplo(i);
        card.innerHTML = `
          <div class="templo-header" style="background:${cor}">
            <div class="templo-num">Tempio ${i}</div>
            <div class="templo-nome">${nome}</div>
            <div class="templo-meta">
              <span class="templo-cidade">📍 ${cidade}</span>
              <span class="nivel-badge">${nivel}</span>
              ${concluido ? '<span class="nivel-badge">✅ Completo</span>' : ''}
            </div>
          </div>
          <div class="templo-body">
            <div class="progresso-label">${dominadas}/${totalPalavras} parole dominate</div>
            <div class="progresso-bar-container">
              <div class="progresso-bar-fill" style="width:${progPercent}%"></div>
            </div>
          </div>
        `;
      } else {
        card.style.cursor = 'pointer';
        card.onclick = () => this.abrirModalTemplo(i);
        card.innerHTML = `
          <div class="templo-header" style="background:${cor}; filter:grayscale(0.6)">
            <div class="templo-num">Tempio ${i}</div>
            <div class="templo-nome">🔒 ${nome}</div>
            <div class="templo-meta">
              <span class="templo-cidade">📍 ${cidade}</span>
              <span class="nivel-badge">${nivel}</span>
            </div>
          </div>
          <div class="templo-body">
            <div class="lock-info">Requer Livello ${nivelMinimo}</div>
            <div class="progresso-bar-container">
              <div class="progresso-bar-fill" style="width:0%"></div>
            </div>
            <div class="progresso-label" style="text-align:center;color:#bbb;">Bloqueado</div>
          </div>
        `;
      }

      grid.appendChild(card);
    }

    // Render daily word
    this.renderizarParolaDia();
  },

  // Navigate to flashcards for a specific temple
  estudarTemplo(temploNum) {
    this.navegar('flashcard');
    const sel = document.getElementById('flashcard-templo-select');
    if (sel) {
      sel.value = temploNum;
    }
    if (typeof Flashcards !== 'undefined') {
      Flashcards.init(temploNum);
    }
  },

  // Navigate to quiz for a specific temple
  quizTemplo(temploNum) {
    this.navegar('quiz');
    if (typeof Quiz !== 'undefined') {
      Quiz.iniciar(temploNum);
    }
  },

  // ── Templo detail modal ────────────────────────────────────
  abrirModalTemplo(i) {
    const data = this.estado.templosData[i];
    const desbloqueado = this.estado.progresso.templos_desbloqueados.includes(i);
    const concluido    = this.estado.progresso.templos_concluidos.includes(i);
    const cor          = this.TEMPLO_CORES[i] || this.TEMPLO_CORES[1];
    const nome         = (data && data.nome) ? data.nome : (this.TEMPLO_NOMES[i] || `Tempio ${i}`);
    const cidade       = data ? data.cidade : '—';
    const nivel        = data ? data.nivel : '—';
    const desc         = this.TEMPLO_DESC[i] || '';
    const nivelMinimo  = this.TEMPLO_NIVEL_MINIMO[i] || i;
    const totalPalavras = data && data.palavras ? data.palavras.length : 0;

    let dominadas = 0;
    if (data && data.palavras) {
      dominadas = data.palavras.filter(p => {
        const sm = this.estado.flashcardData[p.id];
        if (!sm) return false;
        return (sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7);
      }).length;
    }
    const progPercent = totalPalavras > 0 ? Math.round((dominadas / totalPalavras) * 100) : 0;

    const body = document.getElementById('templo-modal-body');
    body.innerHTML = `
      <div class="tm-header" style="background:${cor}${!desbloqueado ? ';filter:grayscale(0.5)' : ''}">
        <button class="tm-close" onclick="App.fecharModalTemplo()" title="Chiudi">✕</button>
        <div class="tm-num">Tempio ${i}</div>
        <div class="tm-nome">${nome}</div>
        <div class="tm-meta">
          <span class="tm-badge">📍 ${cidade}</span>
          <span class="tm-badge">${nivel}</span>
          ${concluido ? '<span class="tm-badge">✅ Completo</span>' : ''}
        </div>
      </div>
      <div class="tm-content">
        ${desbloqueado ? `
          <div class="tm-progress-wrap">
            <div class="tm-progress-label">${dominadas} / ${totalPalavras} parole dominate · ${progPercent}%</div>
            <div class="tm-progress-bar"><div class="tm-progress-fill" style="width:${progPercent}%"></div></div>
          </div>
        ` : `<div class="tm-lock-banner">🔒 Richiede Livello ${nivelMinimo}</div>`}
        <p class="tm-desc">${desc}</p>
        ${desbloqueado ? `
          <div class="tm-actions">
            <button class="tm-btn-primary" onclick="App.fecharModalTemplo();App.estudarTemplo(${i})">📚 Studia i vocaboli</button>
            <button class="tm-btn-quiz" onclick="App.fecharModalTemplo();App.quizTemplo(${i})">❓ Fai il Quiz</button>
          </div>
        ` : `
          <details class="tm-unlock-area">
            <summary>Hai un codice di accesso?</summary>
            <div class="tm-unlock-form">
              <input id="tm-code-input" type="password" placeholder="Inserisci il codice..." class="tm-code-input"
                onkeydown="if(event.key==='Enter')App.tentarDesbloquear(${i})">
              <button onclick="App.tentarDesbloquear(${i})" class="tm-btn-unlock">Sblocca</button>
            </div>
          </details>
        `}
      </div>
    `;

    document.getElementById('templo-modal').classList.add('ativo');
    document.body.style.overflow = 'hidden';
  },

  fecharModalTemplo() {
    document.getElementById('templo-modal').classList.remove('ativo');
    document.body.style.overflow = '';
  },

  tentarDesbloquear(temploNum) {
    const input = document.getElementById('tm-code-input');
    if (!input) return;
    if (input.value.trim() === this.UNLOCK_CODE) {
      const p = this.estado.progresso;
      p.templos_desbloqueados = [1,2,3,4,5,6,7,8,9,10];
      this.salvarProgresso();
      this.fecharModalTemplo();
      this.renderizarTemplos();
      this.atualizarStats();
      this.notificar('Tutti i templi sbloccati! 🎉', 'sucesso');
    } else {
      input.style.borderColor = '#C0392B';
      input.value = '';
      input.placeholder = 'Codice non corretto…';
      setTimeout(() => { input.style.borderColor = ''; input.placeholder = 'Inserisci il codice...'; }, 2000);
    }
  },

  // ── Header stats ───────────────────────────────────────────
  atualizarStats() {
    const p = this.estado.progresso;
    if (!p) return;

    const elNivel   = document.getElementById('stat-nivel');
    const elXp      = document.getElementById('stat-xp');
    const elTempli  = document.getElementById('stat-templi');
    const elParole  = document.getElementById('stat-parole');
    const elBarFill = document.getElementById('xp-bar-fill');
    const elStreak  = document.getElementById('stat-streak');

    // XP for current level progress
    // xpInicio = cumulative XP at START of current level
    // xpFim    = cumulative XP needed to reach NEXT level
    let xpInicio = 0;
    let xpFim = p.xp_proximo_nivel || 500;
    if (typeof Progressao !== 'undefined') {
      xpInicio = Progressao.xpParaNivel(p.nivel) || 0;
      xpFim    = Progressao.xpParaNivel(p.nivel + 1) || (xpInicio + 500);
    }
    const range = xpFim - xpInicio;
    const current = p.xp - xpInicio;
    const percent = range > 0 ? Math.min(100, Math.round((current / range) * 100)) : 0;

    if (elNivel)   elNivel.textContent   = `Livello ${p.nivel}`;
    if (elXp)      elXp.textContent      = `XP: ${p.xp}/${xpFim}`;
    if (elTempli)  elTempli.textContent  = `Templi: ${p.templos_desbloqueados.length}/10`;
    if (elParole)  elParole.textContent  = `Parole: ${p.total_palavras}`;
    if (elBarFill) elBarFill.style.width = percent + '%';
    const s = p.streak || 0;
    if (elStreak)  elStreak.textContent  = `🔥 ${s} dia${s !== 1 ? 's' : ''}`;

    // Daily goal bar
    const hoje = new Date().toISOString().slice(0, 10);
    if (p.data_xp_hoje !== hoje) { p.xp_hoje = 0; }
    const meta     = p.meta_diaria || 100;
    const ganhoHj  = p.xp_hoje || 0;
    const metaPct  = Math.min(100, Math.round((ganhoHj / meta) * 100));
    const elMetaFill  = document.getElementById('meta-bar-fill');
    const elMetaLabel = document.getElementById('meta-bar-label');
    const elMetaXp    = document.getElementById('meta-bar-xp');
    if (elMetaFill)  elMetaFill.style.width   = metaPct + '%';
    if (elMetaLabel) elMetaLabel.textContent  = `🎯 Meta do dia`;
    if (elMetaXp)    elMetaXp.textContent     = `${ganhoHj}/${meta} XP${ganhoHj >= meta ? ' ✅' : ''}`;
  },

  // ── Favoritos ─────────────────────────────────────────────
  toggleFavorito(id) {
    const p = this.estado.progresso;
    if (!p) return false;
    if (!p.favoritos) p.favoritos = [];
    const idx = p.favoritos.indexOf(id);
    const adicionado = idx === -1;
    if (adicionado) p.favoritos.push(id);
    else            p.favoritos.splice(idx, 1);
    this.salvarProgresso();
    return adicionado;
  },

  ehFavorito(id) {
    const p = this.estado.progresso;
    return !!(p && p.favoritos && p.favoritos.includes(id));
  },

  // ── Meta Diária settings ──────────────────────────────────
  abrirMetaSettings() {
    const modal = document.getElementById('meta-settings-modal');
    if (!modal) return;
    // Highlight current goal
    const meta = (this.estado.progresso || {}).meta_diaria || 100;
    modal.querySelectorAll('.meta-op-btn').forEach(btn => {
      btn.classList.toggle('ativo', parseInt(btn.dataset.val) === meta);
    });
    modal.style.display = 'flex';
  },

  fecharMetaSettings() {
    const modal = document.getElementById('meta-settings-modal');
    if (modal) modal.style.display = 'none';
  },

  setMeta(valor) {
    if (!this.estado.progresso) return;
    this.estado.progresso.meta_diaria = valor;
    this.salvarProgresso();
    this.atualizarStats();
    this.fecharMetaSettings();
    this.notificar(`Meta: ${valor} XP/dia`, 'successo');
  },

  // ── XP system ─────────────────────────────────────────────
  ganharXP(quantidade) {
    if (typeof Progressao !== 'undefined') {
      Progressao.ganhar(quantidade);
    } else {
      // Fallback if progression.js not yet loaded
      this.estado.progresso.xp += quantidade;
      this.salvarProgresso();
      this.atualizarStats();
    }
    this.notificar(`+${quantidade} XP`, 'alerta');
  },

  verificarNivelUp() {
    if (typeof Progressao !== 'undefined') {
      Progressao.verificarNivelUp();
    }
  },

  verificarDesbloqueioTemplos() {
    if (typeof Progressao !== 'undefined') {
      Progressao.verificarDesbloqueioTemplos();
    }
  },

  // ── Toast notifications ────────────────────────────────────
  notificar(mensagem, tipo = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.textContent = mensagem;
    container.appendChild(toast);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
      toast.classList.add('saindo');
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 320);
    }, 3000);
  },

  // ── Text-to-speech ─────────────────────────────────────────
  pronunciar(texto) {
    if (!texto) return;
    if (!('speechSynthesis' in window)) return;
    // Cancel any ongoing speech
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(texto);
    u.lang = 'it-IT';
    u.rate = 0.9;
    u.pitch = 1;
    speechSynthesis.speak(u);
  }
};

// ── Bootstrap ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => App.init());
