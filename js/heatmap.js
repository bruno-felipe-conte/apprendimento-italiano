// ============================================================
// heatmap.js — GitHub-style activity heatmap
// Uses localStorage key 'it_diario': { "2026-05-15": 14, ... }
// Renders 6 months of daily study activity.
// ============================================================

const Calor = {
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
    const footerEl = document.getElementById('heatmap-footer');
    if (!container) return;

    // Read diary
    let diario = {};
    try {
      diario = JSON.parse(localStorage.getItem('it_diario') || '{}');
    } catch (e) {}

    // 6 months ago from today
    const end = new Date();
    const start = new Date();
    start.setMonth(start.getMonth() - 6);
    // Align start to Monday
    start.setDate(start.getDate() - start.getDay() + 1);

    const todayStr = end.toISOString().split('T')[0];

    // Compute max for color scaling — compare as ISO strings (avoids timezone issue)
    const startStr = start.toISOString().split('T')[0];
    const endStr   = end.toISOString().split('T')[0];
    let maxVal = 1;
    for (const key in diario) {
      if (key >= startStr && key <= endStr && diario[key] > maxVal) {
        maxVal = diario[key];
      }
    }

    // Build weeks
    const weeks = [];
    let curWeek = [];
    const d = new Date(start);
    // No null padding needed — start is already aligned to Monday

    let totalAtividades = 0;
    let diasAtivos = 0;
    let streak = 0;
    let curStreak = 0;

    // Count backwards for streak
    const td = new Date();
    while (td >= start) {
      const k = td.toISOString().split('T')[0];
      const v = diario[k] || 0;
      if (v > 0) { curStreak++; if (curStreak > streak) streak = curStreak; }
      else curStreak = 0;
      td.setDate(td.getDate() - 1);
    }

    // Build grid
    while (d <= end) {
      const key = d.toISOString().split('T')[0];
      const value = diario[key] || 0;
      totalAtividades += value;
      if (value > 0) diasAtivos++;

      let level = 0;
      if (value > 0) {
        const ratio = value / maxVal;
        if (ratio <= 0.25) level = 1;
        else if (ratio <= 0.5) level = 2;
        else if (ratio <= 0.75) level = 3;
        else level = 4;
      }

      curWeek.push({
        date: key,
        value,
        level,
        isToday: key === todayStr
      });

      // Sunday ends the week (Monday-start weeks)
      if (d.getDay() === 0) {
        weeks.push(curWeek);
        curWeek = [];
      }
      d.setDate(d.getDate() + 1);
    }
    if (curWeek.length > 0) weeks.push(curWeek);

    // Day labels — all 7 days, Monday-start
    const dayLabels = ['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];
    const MESES = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];

    // ── Group weeks by month ────────────────────────────────
    // Parse month from "YYYY-MM-DD" string directly (avoids UTC/timezone bug
    // where new Date("YYYY-MM-DD").getMonth() can return the previous month
    // in negative-UTC-offset timezones like UTC-3).
    const dateMonth = str => parseInt(str.slice(5, 7), 10) - 1; // 0-indexed

    const monthGroups = []; // [{month, startWi, count}]
    let prevMonth = -1;
    for (let wi = 0; wi < weeks.length; wi++) {
      const firstDay = weeks[wi].find(x => x);
      const m = firstDay ? dateMonth(firstDay.date) : prevMonth;
      if (m !== prevMonth) {
        monthGroups.push({ month: m, startWi: wi, count: 0 });
        prevMonth = m;
      }
      monthGroups[monthGroups.length - 1].count++;
    }

    // ── Build flat column list: week cols interleaved with sep cols ──
    // Each separator is a 1-cell-wide column with a thin vertical line
    const cols = []; // {type:'week', wi} | {type:'sep'}
    for (let gi = 0; gi < monthGroups.length; gi++) {
      if (gi > 0) cols.push({ type: 'sep' });
      const g = monthGroups[gi];
      for (let i = 0; i < g.count; i++) cols.push({ type: 'week', wi: g.startWi + i });
    }

    // ── Render as <table> so colspan works for centered month labels ──
    let html = '<table class="hm-table"><tbody>';

    // 7 day rows — sep columns use rowspan=7 so only emitted in first row
    for (let di = 0; di < 7; di++) {
      html += '<tr>';
      html += `<td class="hm-day-label">${dayLabels[di]}</td>`;
      for (const col of cols) {
        if (col.type === 'sep') {
          // Only emit on first day row; rowspan covers the rest
          if (di === 0) html += '<td class="hm-sep-col" rowspan="7"></td>';
        } else {
          const week = weeks[col.wi];
          if (di < week.length && week[di]) {
            const c = week[di];
            html += `<td class="hm-cell l${c.level}${c.isToday ? ' today' : ''}" onclick="App.notificar('${c.date}: ${c.value} atividades','alerta')" title="${c.date}: ${c.value} cards/quiz"></td>`;
          } else {
            html += '<td class="hm-cell hm-cell-empty"></td>';
          }
        }
      }
      html += '</tr>';
    }

    // Month label row — centered over each month's weeks via colspan
    html += '<tr>';
    html += '<td></td>'; // spacer for day-label column
    for (let gi = 0; gi < monthGroups.length; gi++) {
      if (gi > 0) html += '<td></td>'; // sep column (already spanned above — just placeholder)
      const g = monthGroups[gi];
      html += `<td colspan="${g.count}" class="hm-month-label">${MESES[g.month]}</td>`;
    }
    html += '</tr>';

    html += '</tbody></table>';

    container.innerHTML = html;

    if (statsEl) {
      statsEl.innerHTML = `<strong>${totalAtividades}</strong> atividades em <strong>${diasAtivos}</strong> dias • Maior sequência: <strong>${streak}</strong> dias 🔥`;
    }
    if (footerEl) {
      footerEl.textContent = 'Um pouco todo dia constrói o hábito. Forza! 🇮🇹';
    }
  }
};
