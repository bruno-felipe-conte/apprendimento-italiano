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

    // Use stored data_inicio; fall back to ultimo_estudo (approximate).
    // Never fall back to Date.now() — that would show today for old saves.
    const dataInicio = (p.data_inicio || p.ultimo_estudo)
      ? new Date(p.data_inicio || p.ultimo_estudo).toLocaleDateString('pt-BR')
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

        <div class="profilo-card" style="margin-top:1.5rem">
          <div class="profilo-card-titulo">⚙️ Gestione Dati</div>
          <p style="font-size:0.85rem; color:#666; margin-bottom:1rem;">O Italiano Autentico guarda seu progresso localmente no seu dispositivo. Faça backup regularmente para não perder seus dados caso limpe o histórico do navegador.</p>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
            <button class="btn-secondario" onclick="Profilo.exportarDados()">⬇️ Exportar Backup</button>
            <button class="btn-secondario" onclick="document.getElementById('backup-input').click()">⬆️ Importar Backup</button>
            <button style="margin-left:auto; background:#E74C3C; color:white; border:none; padding:0.4rem 1rem; border-radius:12px; cursor:pointer; font-weight:600;" onclick="Profilo.resetProgresso()">⚠️ Azzera Tutto</button>
          </div>
          <!-- Conteúdo Criado por Mim -->
          <div style="border-top:1px solid #f0e8d8;padding-top:0.8rem;margin-top:0.8rem">
            <div style="font-size:0.78rem;font-weight:700;color:#9B2335;margin-bottom:0.5rem">Conteúdo Criado por Mim</div>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap">
              <button class="btn-secondario" onclick="Profilo.exportarConteudoCustom()" style="font-size:0.82rem">
                ⬇️ Exportar Músicas e Diálogos
              </button>
              <button class="btn-secondario" onclick="document.getElementById('custom-input').click()" style="font-size:0.82rem">
                ⬆️ Importar Conteúdo
              </button>
            </div>
          </div>
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
      // _lerEntrada handles both legacy number format and new {cards,xp} format
      const entry = (typeof Calor !== 'undefined')
        ? Calor._lerEntrada(diario[key])
        : { cards: (typeof diario[key] === 'number' ? diario[key] : (diario[key] || {}).cards || 0), xp: (diario[key] || {}).xp || 0 };
      const cards   = entry.cards;
      const xpDia   = entry.xp;
      const sessoes = cards > 0 ? 1 : 0;
      dias.push({ dia: d.toLocaleDateString('pt-BR', { weekday:'short' }).slice(0,3), cards, xp: xpDia, sessoes });
      totalCards   += cards;
      totalSessoes += sessoes;
      totalXP      += xpDia;
      if (cards > 0) giorniAttivi++;
    }

    // Add quiz XP from it_quiz_historico (not stored in diário)
    try {
      const hist = JSON.parse(localStorage.getItem('it_quiz_historico') || '[]');
      const semanaAtras = Date.now() - 7 * 86400000;
      totalXP += hist.filter(h => h.data >= semanaAtras).reduce((s, h) => s + (h.xp_ganho || 0), 0);
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

  // ── Exportar backup ───────────────────────────────────────
  exportarDados() {
    const backup = {
      versao: 1,
      data: new Date().toISOString(),
      progresso:   JSON.parse(localStorage.getItem('it_progresso')   || 'null'),
      flashcards:  JSON.parse(localStorage.getItem('it_flashcards')  || '{}'),
      diario:      JSON.parse(localStorage.getItem('it_diario')      || '{}'),
      onboarding:  localStorage.getItem('it_onboarding_done'),
      tema:        localStorage.getItem('it_tema'),
      canzoni_custom:  JSON.parse(localStorage.getItem('it_canzoni_custom')  || '[]'),
      dialoghi_custom: JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]'),
    };
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `italiano_backup_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    App.notificar('✅ Backup exportado com sucesso!', 'sucesso');
  },

  // ── Importar backup ───────────────────────────────────────
  importarDados(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const backup = JSON.parse(e.target.result);
        if (!backup.versao || !backup.progresso) throw new Error('Formato inválido');
        if (!confirm('Isso vai substituir todo o seu progresso atual. Confirmar?')) return;
        if (backup.progresso)  localStorage.setItem('it_progresso',      JSON.stringify(backup.progresso));
        if (backup.flashcards) localStorage.setItem('it_flashcards',     JSON.stringify(backup.flashcards));
        if (backup.diario)     localStorage.setItem('it_diario',         JSON.stringify(backup.diario));
        if (backup.onboarding) localStorage.setItem('it_onboarding_done', backup.onboarding);
        if (backup.tema)       localStorage.setItem('it_tema',            backup.tema);
        if (backup.canzoni_custom)  localStorage.setItem('it_canzoni_custom',  JSON.stringify(backup.canzoni_custom));
        if (backup.dialoghi_custom) localStorage.setItem('it_dialoghi_custom', JSON.stringify(backup.dialoghi_custom));
        App.notificar('✅ Backup importado! Recarregando...', 'sucesso');
        setTimeout(() => location.reload(), 1200);
      } catch(err) {
        App.notificar('❌ Arquivo inválido: ' + err.message, 'erro');
      }
    };
    reader.readAsText(file);
    event.target.value = ''; // reset input
  },

  // ── Reset total de progresso ──────────────────────────────
  resetProgresso() {
    if (!confirm('⚠️ Isso apagará TODO o seu progresso — XP, flashcards, conquistas e streak. Tem certeza?')) return;
    if (!confirm('Esta ação é IRREVERSÍVEL. Deseja mesmo começar do zero?')) return;
    ['it_progresso','it_flashcards','it_diario','it_onboarding_done','it_palavra_dia', 'it_canzoni_custom', 'it_dialoghi_custom'].forEach(k => localStorage.removeItem(k));
    App.notificar('Progresso resetado. Recarregando...', 'alerta');
    setTimeout(() => location.reload(), 1200);
  },

  // ── Exportar/Importar Apenas Conteúdo Custom ──────────────
  exportarConteudoCustom() {
    const backup = {
      versao: 1,
      tipo: 'conteudo_custom',
      data: new Date().toISOString(),
      canzoni: JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]'),
      dialoghi: JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]')
    };
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `italiano_conteudo_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    App.notificar('✅ Conteúdo exportado!', 'sucesso');
  },

  importarConteudoCustom(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const backup = JSON.parse(e.target.result);
        if (backup.tipo !== 'conteudo_custom') throw new Error('Arquivo inválido (deve ser conteúdo custom)');
        if (!confirm(`Importar ${backup.canzoni?.length || 0} músicas e ${backup.dialoghi?.length || 0} diálogos? O conteúdo existente será mantido e mesclado.`)) return;
        
        // Merge (não sobrescreve — adiciona os que não existem)
        const canExist = JSON.parse(localStorage.getItem('it_canzoni_custom') || '[]');
        const dialExist = JSON.parse(localStorage.getItem('it_dialoghi_custom') || '[]');
        
        const canIds = new Set(canExist.map(x => x.id));
        const dialIds = new Set(dialExist.map(x => x.id));
        
        const canNovos = (backup.canzoni || []).filter(x => !canIds.has(x.id));
        const dialNovos = (backup.dialoghi || []).filter(x => !dialIds.has(x.id));
        
        localStorage.setItem('it_canzoni_custom', JSON.stringify([...canExist, ...canNovos]));
        localStorage.setItem('it_dialoghi_custom', JSON.stringify([...dialExist, ...dialNovos]));
        
        App.notificar(`✅ ${canNovos.length} músicas e ${dialNovos.length} diálogos importados!`, 'sucesso');
      } catch(err) {
        App.notificar('❌ Arquivo inválido: ' + err.message, 'erro');
      }
    };
    reader.readAsText(file);
    event.target.value = '';
  },

  // ── Helper: stat row ──────────────────────────────────────
  _row(label, val) {
    return `<div class="profilo-stat-row">
      <span class="profilo-stat-label">${label}</span>
      <span class="profilo-stat-val">${val}</span>
    </div>`;
  }
};
