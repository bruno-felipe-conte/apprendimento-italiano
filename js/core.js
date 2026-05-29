// ============================================================
// core.js — Global App state, data loading, navigation, XP
// ============================================================

const App = {
  // ── State ──────────────────────────────────────────────────
  estado: {
    secaoAtiva: 'templi',
    templosData: {},    // { 1: { templo, nome, cidade, nivel, palavras: [] }, ... }
    quizData: [],       // flat array of all quiz questions
    vocabCache: [],     // flat array of all words (with templo_num attached)
    progresso: null,    // persisted in localStorage
    flashcardData: {}   // persisted in localStorage
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
  },

  // ── localStorage ───────────────────────────────────────────
  carregarProgresso() {
    try {
      const raw = localStorage.getItem('it_progresso');
      if (raw) {
        const p = JSON.parse(raw);
        // Backward compatibility: ensure grammatica_completadas exists
        if (!p.grammatica_completadas) p.grammatica_completadas = [];
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
      grammatica_completadas: []
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
            <div class="templo-actions">
              <button class="btn-estudar" onclick="App.estudarTemplo(${i})">📚 Estudar</button>
              <button class="btn-quiz-templo" onclick="App.quizTemplo(${i})">❓ Quiz</button>
            </div>
          </div>
        `;
      } else {
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
