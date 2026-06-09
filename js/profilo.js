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
          ${this._row('Templi sbloccati', `${(p.templos_desbloqueados||[]).length} / 50`)}
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
          ${typeof Conquistas !== 'undefined' ? Conquistas.renderizarPainelCompleto() : ''}
        </div>

        <!-- Lembretes push — só renderiza se o módulo estiver carregado e a API disponível -->
        ${(typeof Notificacoes !== 'undefined' && 'Notification' in window)
          ? `<div class="profilo-card" style="margin-top:0">${Notificacoes.renderizarCard()}</div>`
          : ''}

        <div class="profilo-card" style="margin-top:1.5rem">
          <div class="profilo-card-titulo">${I18n.t('prof_gestao_dati')}</div>
          <p style="font-size:0.85rem; color:#666; margin-bottom:1rem;">${I18n.t('prof_backup_desc')}</p>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap;">
            <button class="btn-secondario" onclick="Profilo.exportarDados()">${I18n.t('prof_exp_backup')}</button>
            <button class="btn-secondario" onclick="document.getElementById('backup-input').click()">${I18n.t('prof_imp_backup')}</button>
            <button style="margin-left:auto; background:#E74C3C; color:white; border:none; padding:0.4rem 1rem; border-radius:12px; cursor:pointer; font-weight:600;" onclick="Profilo.resetProgresso()">${I18n.t('prof_azzera')}</button>
          </div>
          <!-- Tour -->
          <div style="border-top:1px solid #f0e8d8;padding-top:0.8rem;margin-top:0.8rem">
            <button class="btn-secondario" style="width:100%;font-size:0.85rem" onclick="App.navegar('templi');setTimeout(()=>Tour.reiniciar(),200)">
              🗺️ Ver tour introdutório novamente
            </button>
          </div>
          <!-- Conteúdo Criado por Mim -->
          <div style="border-top:1px solid #f0e8d8;padding-top:0.8rem;margin-top:0.8rem">
            <div style="font-size:0.78rem;font-weight:700;color:#9B2335;margin-bottom:0.3rem">${I18n.t('prof_conteudo_criado')}</div>
            <div style="font-size:0.75rem;color:#888;margin-bottom:0.5rem">
              ${I18n.idioma==='it'
                ? 'Canzoni, dialoghi, storie, imitazioni e vocabolario aggiunti manualmente o via IA.'
                : 'Músicas, diálogos, histórias, imitações e vocabulário adicionados manualmente ou via IA.'}
            </div>
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap">
              <button class="btn-secondario" onclick="Profilo.exportarConteudoCustom()" style="font-size:0.82rem">
                ⬇️ ${I18n.idioma==='it' ? 'Esporta Contenuto' : 'Exportar Conteúdo'}
              </button>
              <button class="btn-secondario" onclick="document.getElementById('custom-input').click()" style="font-size:0.82rem">
                ⬆️ ${I18n.idioma==='it' ? 'Importa Contenuto' : 'Importar Conteúdo'}
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
      versao: 2,
      data: new Date().toISOString(),
      progresso:         JSON.parse(localStorage.getItem('it_progresso')        || 'null'),
      flashcards:        JSON.parse(localStorage.getItem('it_flashcards')       || '{}'),
      diario:            JSON.parse(localStorage.getItem('it_diario')           || '{}'),
      onboarding:        localStorage.getItem('it_onboarding_done'),
      tema:              localStorage.getItem('it_tema'),
      idioma:            localStorage.getItem('it_idioma') || 'pt',
      // conteúdo customizado
      canzoni_custom:    JSON.parse(localStorage.getItem('it_canzoni_custom')   || '[]'),
      dialoghi_custom:   JSON.parse(localStorage.getItem('it_dialoghi_custom')  || '[]'),
      storie_custom:     JSON.parse(localStorage.getItem('it_storie_custom')    || '[]'),
      imitazioni_custom: JSON.parse(localStorage.getItem('it_imitazioni_custom')|| '[]'),
      vocab_custom:      JSON.parse(localStorage.getItem('it_vocab_custom')     || '[]'),
      // preferências de ocultação
      canzoni_ocultas:   JSON.parse(localStorage.getItem('it_canzoni_ocultas')  || '[]'),
    };
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href     = url;
    a.download = `italiano_backup_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    App.notificar('notif_backup_exp', 'sucesso');
  },

  // ── Importar backup ───────────────────────────────────────
  importarDados(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const backup = JSON.parse(e.target.result);
        if (!backup.versao || !backup.progresso) throw new Error(I18n.t('prof_erro_formato'));
        if (!confirm(I18n.t('prof_confirm_importar'))) return;
        if (backup.progresso)         localStorage.setItem('it_progresso',         JSON.stringify(backup.progresso));
        if (backup.flashcards)        localStorage.setItem('it_flashcards',        JSON.stringify(backup.flashcards));
        if (backup.diario)            localStorage.setItem('it_diario',            JSON.stringify(backup.diario));
        if (backup.onboarding)        localStorage.setItem('it_onboarding_done',   backup.onboarding);
        if (backup.tema)              localStorage.setItem('it_tema',              backup.tema);
        if (backup.idioma)            localStorage.setItem('it_idioma',            backup.idioma);
        if (backup.canzoni_custom?.length)    localStorage.setItem('it_canzoni_custom',    JSON.stringify(backup.canzoni_custom));
        if (backup.dialoghi_custom?.length)   localStorage.setItem('it_dialoghi_custom',   JSON.stringify(backup.dialoghi_custom));
        if (backup.storie_custom?.length)     localStorage.setItem('it_storie_custom',     JSON.stringify(backup.storie_custom));
        if (backup.imitazioni_custom?.length) localStorage.setItem('it_imitazioni_custom', JSON.stringify(backup.imitazioni_custom));
        if (backup.vocab_custom?.length)      localStorage.setItem('it_vocab_custom',      JSON.stringify(backup.vocab_custom));
        if (backup.canzoni_ocultas?.length)   localStorage.setItem('it_canzoni_ocultas',   JSON.stringify(backup.canzoni_ocultas));
        App.notificar('notif_backup_imp', 'sucesso');
        setTimeout(() => location.reload(), 1200);
      } catch(err) {
        App.notificar(I18n.t('notif_arquivo_inv') + err.message, 'erro');
      }
    };
    reader.readAsText(file);
    event.target.value = ''; // reset input
  },

  // ── Reset total de progresso ──────────────────────────────
  resetProgresso() {
    if (!confirm(I18n.t('prof_confirm_apagar1'))) return;
    if (!confirm(I18n.t('prof_confirm_apagar2'))) return;
    ['it_progresso','it_flashcards','it_diario','it_onboarding_done','it_palavra_dia',
     'it_canzoni_custom','it_dialoghi_custom','it_storie_custom','it_imitazioni_custom',
     'it_vocab_custom','it_canzoni_ocultas'].forEach(k => localStorage.removeItem(k));
    App.notificar('notif_prog_reset', 'alerta');
    setTimeout(() => location.reload(), 1200);
  },

  // ── Exportar/Importar Apenas Conteúdo Custom ──────────────
  exportarConteudoCustom() {
    const canzoni    = JSON.parse(localStorage.getItem('it_canzoni_custom')    || '[]');
    const dialoghi   = JSON.parse(localStorage.getItem('it_dialoghi_custom')   || '[]');
    const storie     = JSON.parse(localStorage.getItem('it_storie_custom')     || '[]');
    const imitazioni = JSON.parse(localStorage.getItem('it_imitazioni_custom') || '[]');
    const vocab      = JSON.parse(localStorage.getItem('it_vocab_custom')      || '[]');
    const backup = {
      versao: 2,
      tipo: 'conteudo_custom',
      data: new Date().toISOString(),
      canzoni, dialoghi, storie, imitazioni, vocab
    };
    const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `italiano_conteudo_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
    const total = canzoni.length + dialoghi.length + storie.length + imitazioni.length + vocab.length;
    App.notificar(`✅ ${total} item(ns) exportado(s)`, 'sucesso');
  },

  importarConteudoCustom(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const backup = JSON.parse(e.target.result);
        if (backup.tipo !== 'conteudo_custom') throw new Error('Arquivo inválido (deve ser conteúdo custom)');

        // Contagens para confirmação
        const nc = backup.canzoni?.length||0, nd = backup.dialoghi?.length||0,
              ns = backup.storie?.length||0,  ni = backup.imitazioni?.length||0,
              nv = backup.vocab?.length||0;
        if (!confirm(`Importar conteúdo?\n• ${nc} músicas\n• ${nd} diálogos\n• ${ns} histórias\n• ${ni} imitações\n• ${nv} palavras de vocab`)) return;

        // Merge por chave (não sobrescreve itens existentes)
        const _merge = (lsKey, novos) => {
          if (!novos?.length) return;
          const exist = JSON.parse(localStorage.getItem(lsKey) || '[]');
          const ids = new Set(exist.map(x => x.id));
          localStorage.setItem(lsKey, JSON.stringify([...exist, ...novos.filter(x => !ids.has(x.id))]));
        };
        _merge('it_canzoni_custom',    backup.canzoni);
        _merge('it_dialoghi_custom',   backup.dialoghi);
        _merge('it_storie_custom',     backup.storie);
        _merge('it_imitazioni_custom', backup.imitazioni);
        _merge('it_vocab_custom',      backup.vocab);

        App.notificar(`✅ Conteúdo importado com sucesso!`, 'sucesso');
        setTimeout(() => location.reload(), 1200);
      } catch(err) {
        App.notificar(I18n.t('notif_arquivo_inv') + err.message, 'erro');
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
