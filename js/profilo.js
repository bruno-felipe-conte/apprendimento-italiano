// ============================================================
// profilo.js — Student profile + weekly report
// ============================================================

const Profilo = {

  // ── Render full profile page ───────────────────────────────
  renderizar() {
    const container = document.getElementById('profilo-container');
    if (!container) return;

    const p  = App.estado.progresso  || {};
    const fd = App.estado.flashcardData || {};

    // ── Compute stats ──────────────────────────────────────
    let totalRevisoes = 0, totalAgain = 0, totalHard = 0, totalGood = 0, totalEasy = 0;
    let totalDominadas = 0, totalDificeis = 0, tempoEstimadoMin = 0;
    const categorias = {};

    for (const id in fd) {
      const sm = fd[id];
      const reps = sm.reps || sm.repeticoes || 0;
      totalRevisoes += reps;
      totalAgain += sm.erros || 0;
      // Approximate good/easy from reps (no exact breakdown stored)
      if ((sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7)) totalDominadas++;
      if ((sm.erros || 0) >= 3) totalDificeis++;
      // Category from vocab cache
      const palavra = (App.estado.vocabCache || []).find(w => w.id === id);
      if (palavra && palavra.categoria) {
        categorias[palavra.categoria] = (categorias[palavra.categoria] || 0) + reps;
      }
    }
    // ~8s per card average
    tempoEstimadoMin = Math.round(totalRevisoes * 8 / 60);

    const dataInicio = p.ultimo_estudo
      ? new Date(p.data_inicio || Date.now()).toLocaleDateString('pt-BR')
      : '—';

    // Sort categories by usage
    const topCats = Object.entries(categorias)
      .sort((a,b) => b[1] - a[1])
      .slice(0, 5)
      .map(([cat, n]) => `${cat} (${n})`).join(', ') || '—';

    // ── Weekly report data ─────────────────────────────────
    const semana = this._dadosSemana();

    // ── Quiz history stats ─────────────────────────────────
    let quizAcuracia = '—';
    try {
      const hist = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]');
      if (hist.length > 0) {
        const media = hist.reduce((s, h) => s + (h.pontuacao || 0), 0) / hist.length;
        quizAcuracia = Math.round(media) + '%';
      }
    } catch(e) {}

    // ── Build HTML ─────────────────────────────────────────
    container.innerHTML = `
      <!-- Stats grid -->
      <div class="profilo-grid">

        <!-- General stats -->
        <div class="profilo-card">
          <div class="profilo-card-titulo">📊 Statistiche Generali</div>
          ${this._row('Livello attuale', `${p.nivel || 1}`)}
          ${this._row('XP totale', `${(p.xp || 0).toLocaleString()} XP`)}
          ${this._row('Streak attuale', `${p.streak || 0} 🔥 giorni`)}
          ${this._row('Flashcard revisionate', `${totalRevisoes.toLocaleString()}`)}
          ${this._row('Parole dominate', `${totalDominadas}`)}
          ${this._row('Parole difficili', totalDificeis > 0 ? `<span style="color:#C0392B">⚠️ ${totalDificeis}</span>` : '0')}
          ${this._row('Tempo stimato', `${tempoEstimadoMin} min`)}
          ${this._row('Templi sbloccati', `${(p.templos_desbloqueados||[]).length} / 10`)}
          ${this._row('Accuratezza quiz', quizAcuracia)}
        </div>

        <!-- Weekly report -->
        <div class="profilo-card">
          <div class="profilo-card-titulo">📅 Questa Settimana</div>
          ${this._renderGrafico(semana)}
          ${this._row('Totale sessioni', `${semana.totalSessoes}`)}
          ${this._row('Card studiate', `${semana.totalCards}`)}
          ${this._row('XP guadagnato', `${semana.totalXP} XP`)}
          ${this._row('Giorni attivi', `${semana.giorniAttivi} / 7`)}
        </div>

        <!-- Categories -->
        <div class="profilo-card">
          <div class="profilo-card-titulo">📚 Categorie Più Studiate</div>
          <div style="font-size:0.87rem;color:#666;line-height:1.8;">${topCats}</div>
        </div>

        <!-- Conquistas -->
        <div class="profilo-card">
          <div class="profilo-card-titulo">🏆 I Miei Traguardi</div>
          <div class="profilo-conquistas-grid" id="profilo-conquistas"></div>
        </div>

      </div>`;

    // Render conquistas badges
    if (typeof Conquistas !== 'undefined') {
      Conquistas.renderizarPainel('profilo-conquistas');
    }
  },

  // ── Build last-7-days chart data ──────────────────────────
  _dadosSemana() {
    const diario = (() => {
      try { return JSON.parse(localStorage.getItem('it_diario') || '{}'); }
      catch(e) { return {}; }
    })();

    const hoje = new Date();
    const dias = [];
    let totalCards = 0, totalSessoes = 0, totalXP = 0, giorniAttivi = 0;

    for (let i = 6; i >= 0; i--) {
      const d = new Date(hoje);
      d.setDate(d.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      const entry = diario[key] || { cards: 0, sessoes: 0 };
      const cards = entry.cards || entry.atividades || 0;
      const sessoes = entry.sessoes || (cards > 0 ? 1 : 0);
      dias.push({ dia: d.toLocaleDateString('pt-BR', { weekday:'short' }).slice(0,3), cards, sessoes });
      totalCards   += cards;
      totalSessoes += sessoes;
      if (cards > 0) giorniAttivi++;
    }

    // Estimate weekly XP from quiz history too
    try {
      const hist = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]');
      const semanaAtras = Date.now() - 7 * 86400000;
      totalXP = hist.filter(h => h.data >= semanaAtras).reduce((s, h) => s + (h.xp_ganho || 0), 0);
    } catch(e) {}

    return { dias, totalCards, totalSessoes, totalXP, giorniAttivi };
  },

  // ── Render bar chart ──────────────────────────────────────
  _renderGrafico(semana) {
    const max = Math.max(1, ...semana.dias.map(d => d.cards));
    const bars = semana.dias.map(d => {
      const h = Math.round((d.cards / max) * 68);
      return `
        <div class="chart-bar-wrap">
          <div class="chart-val">${d.cards || ''}</div>
          <div class="chart-bar" style="height:${h}px"></div>
          <div class="chart-day">${d.dia}</div>
        </div>`;
    }).join('');
    return `<div class="relatorio-chart">${bars}</div>`;
  },

  // ── Helper: stat row ──────────────────────────────────────
  _row(label, val) {
    return `<div class="profilo-stat-row">
      <span class="profilo-stat-label">${label}</span>
      <span class="profilo-stat-val">${val}</span>
    </div>`;
  }
};
