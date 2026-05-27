// ============================================================
// heatmap.js — GitHub-style activity heatmap
// Uses localStorage key 'it_diario': { "2026-05-15": 14, ... }
// Renders 6 months of daily study activity.
// ============================================================

const Calor = {
  // ── Navigation state ────────────────────────────────────
  offset: 0, // months to shift left from current month (0 = today's month is center)

  navegar(delta) {
    this.offset -= delta;
    if (this.offset < 0) this.offset = 0;
    if (this.offset > 12) this.offset = 12;
    this.renderizar();
  },

  // ── Log activity (called from flashcards/quiz) ──────────
  registrar(quantidade = 1) {
    const hoje = new Date().toISOString().split('T')[0];
    let diario = {};
    try {
      diario = JSON.parse(localStorage.getItem('it_diario') || '{}');
    } catch (e) {}
    diario[hoje] = (diario[hoje] || 0) + quantidade;
    try {
      localStorage.setItem('it_diario', JSON.stringify(diario));
    } catch (e) {}

    // Compute current streak and persist to progress
    const streak = this._computarStreakAtual(diario);
    if (typeof App !== 'undefined' && App.estado.progresso) {
      if (streak > (App.estado.progresso.streak || 0)) {
        App.estado.progresso.streak = streak;
      }
      // Always update current streak (may reset if gap day)
      App.estado.progresso.streak = streak;
      App.salvarProgresso();
      const el = document.getElementById('stat-streak');
      if (el) el.textContent = `🔥 ${streak} dia${streak !== 1 ? 's' : ''}`;
    }
  },

  // Returns consecutive days ending today (or yesterday if today has no entry yet)
  _computarStreakAtual(diario) {
    const d = new Date();
    let streak = 0;
    for (let i = 0; i < 365; i++) {
      const key = d.toISOString().split('T')[0];
      if ((diario[key] || 0) > 0) {
        streak++;
        d.setDate(d.getDate() - 1);
      } else if (i === 0) {
        // Today has no activity yet — check yesterday before giving up
        d.setDate(d.getDate() - 1);
      } else {
        break;
      }
    }
    return streak;
  },

  // ── Render ─────────────────────────────────────────────
  renderizar() {
    const container = document.getElementById('heatmap');
    const statsEl = document.getElementById('heatmap-stats');
    if (!container) return;

    let diario = {};
    try { diario = JSON.parse(localStorage.getItem('it_diario') || '{}'); } catch (e) {}

    const today = new Date();
    const todayStr = [
      today.getFullYear(),
      String(today.getMonth() + 1).padStart(2, '0'),
      String(today.getDate()).padStart(2, '0')
    ].join('-');

    // Center month = current - offset; show 5 months: [center-2, center-1, center, center+1, center+2]
    const MESES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
    const centerDate = new Date(today.getFullYear(), today.getMonth() - this.offset, 1);
    const months = [];
    for (let i = -2; i <= 2; i++) {
      const d = new Date(centerDate.getFullYear(), centerDate.getMonth() + i, 1);
      months.push({ year: d.getFullYear(), month: d.getMonth() });
    }

    // Max value for color scaling
    let maxVal = 1;
    for (const k in diario) if (diario[k] > maxVal) maxVal = diario[k];

    // Stats
    let totalAtividades = 0, diasAtivos = 0, streak = 0;
    // Streak: count backwards from today
    const td2 = new Date(today);
    let cs = 0;
    for (let i = 0; i < 365; i++) {
      const k = [td2.getFullYear(), String(td2.getMonth()+1).padStart(2,'0'), String(td2.getDate()).padStart(2,'0')].join('-');
      if ((diario[k] || 0) > 0) { cs++; streak = cs; td2.setDate(td2.getDate() - 1); }
      else if (i === 0) { td2.setDate(td2.getDate() - 1); }
      else break;
    }
    // Totals for the 6-month window
    for (const { year, month } of months) {
      const days = new Date(year, month + 1, 0).getDate();
      for (let day = 1; day <= days; day++) {
        const k = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        if (k > todayStr) break;
        const v = diario[k] || 0;
        totalAtividades += v;
        if (v > 0) diasAtivos++;
      }
    }

    // ── Render month blocks ────────────────────────────────
    const canGoRight = this.offset > 0;
    let html = `<div class="hm-nav-row">`;
    html += `<button class="hm-nav-btn" onclick="Calor.navegar(-1)" title="Mês anterior">&lt;</button>`;
    html += `<div class="hm-months-row">`;

    for (const { year, month } of months) {
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const firstDow = (new Date(year, month, 1).getDay() + 6) % 7;
      const isCenterMonth = year === centerDate.getFullYear() && month === centerDate.getMonth();

      html += `<div class="hm-month-block${isCenterMonth ? ' hm-center-month' : ''}">`;
      html += '<div class="hm-month-grid">';

      for (let e = 0; e < firstDow; e++) {
        html += '<div class="hm-cell hm-cell-empty"></div>';
      }

      for (let day = 1; day <= daysInMonth; day++) {
        const k = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        if (k > todayStr) {
          html += '<div class="hm-cell hm-cell-future"></div>';
          continue;
        }
        const value = diario[k] || 0;
        let level = 0;
        if (value > 0) {
          const r = value / maxVal;
          level = r <= 0.25 ? 1 : r <= 0.5 ? 2 : r <= 0.75 ? 3 : 4;
        }
        const isToday = k === todayStr;
        html += `<div class="hm-cell l${level}${isToday ? ' today' : ''}" title="${k}: ${value} atividades" onclick="App.notificar('${k}: ${value} atividades','alerta')"></div>`;
      }

      html += '</div>'; // hm-month-grid
      html += `<div class="hm-month-name">${MESES[month]} ${year}</div>`;
      html += '</div>'; // hm-month-block
    }

    html += '</div>'; // hm-months-row
    html += `<button class="hm-nav-btn" onclick="Calor.navegar(1)" ${canGoRight ? '' : 'disabled'} title="Próximo mês">&gt;</button>`;
    html += '</div>'; // hm-nav-row
    container.innerHTML = html;

    if (statsEl) {
      statsEl.innerHTML = `<strong>${totalAtividades}</strong> atividades em <strong>${diasAtivos}</strong> dias • 🔥 Sequência: <strong>${streak}</strong> dias`;
    }
  }
};
