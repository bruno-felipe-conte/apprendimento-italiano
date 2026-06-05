// ============================================================
// conquistas.js — Achievement / badge system
// ============================================================

const Conquistas = {

  // ── Achievement definitions ────────────────────────────────
  LISTA: [
    {
      id: 'primeiro_passo',
      emoji: '🌱',
      nome: 'Primo Passo',
      get descricao() { return I18n.t('ach_primeiro_passo'); },
      verificar(p, fd) { return Object.keys(fd).length >= 1; }
    },
    {
      id: 'uma_semana',
      emoji: '🔥',
      nome: 'Una Settimana',
      get descricao() { return I18n.t('ach_uma_semana'); },
      verificar(p) { return (p.streak || 0) >= 7; }
    },
    {
      id: 'estudioso',
      emoji: '📚',
      nome: 'Studioso',
      get descricao() { return I18n.t('ach_studioso'); },
      verificar(p, fd) {
        let total = 0;
        for (const k in fd) total += (fd[k].reps || fd[k].repeticoes || 0);
        return total >= 100;
      }
    },
    {
      id: 'quiz_perfetto',
      emoji: '✅',
      nome: 'Quiz Perfetto',
      get descricao() { return I18n.t('ach_quiz_perfetto'); },
      // Normally triggered via ganharQuizPerfetto(); falls back to flag
      // check so the achievement survives a save that lost conquistas[].
      verificar(p) { return !!(p.quiz_perfetto_ganha); }
    },
    {
      id: 'primo_tempio',
      emoji: '🏛️',
      nome: 'Primo Tempio',
      get descricao() { return I18n.t('ach_primo_tempio'); },
      verificar(p) { return (p.templos_concluidos || []).includes(1); }
    },
    {
      id: 'vocabulario',
      emoji: '⭐',
      nome: 'Vocabolario Ricco',
      get descricao() { return I18n.t('ach_vocabulario'); },
      verificar(p, fd) {
        let total = 0;
        for (const k in fd) {
          const sm = fd[k];
          // Require at least 1 rep so a single Easy rating can't prematurely
          // count the word as mastered just because FSRS gave high stability.
          const reps = sm.reps || sm.repeticoes || 0;
          if (reps >= 3 || (reps >= 1 && sm.stability > 7)) total++;
        }
        return total >= 50;
      }
    },
    {
      id: 'duro',
      emoji: '💪',
      nome: 'Duro!',
      get descricao() { return I18n.t('ach_duro'); },
      verificar(p, fd) {
        let total = 0;
        for (const k in fd) total += (fd[k].erros || 0);
        return total >= 50;
      }
    },
    {
      id: 'italiano_autentico',
      emoji: '🇮🇹',
      nome: 'Italiano Autentico',
      get descricao() { return I18n.t('ach_italiano_autentico'); },
      verificar(p) { return (p.nivel || 1) >= 10; }
    },
    {
      id: 'um_mes',
      emoji: '🔥🔥',
      nome: 'Un Mese',
      get descricao() { return I18n.t('ach_um_mes'); },
      verificar(p) { return (p.streak || 0) >= 30; }
    },
    {
      id: 'maestro',
      emoji: '🌟',
      nome: 'Maestro',
      get descricao() { return I18n.t('ach_maestro'); },
      verificar(p, fd) {
        let total = 0;
        for (const k in fd) total += (fd[k].reps || fd[k].repeticoes || 0);
        return total >= 500;
      }
    },
    {
      id: 'esploratore',
      emoji: '🗺️',
      nome: 'Esploratore',
      get descricao() { return I18n.t('ach_esploratore'); },
      verificar(p) { return (p.templos_desbloqueados || []).length >= 5; }
    },
    {
      id: 'grammatico',
      emoji: '📖',
      nome: 'Grammatico',
      get descricao() { return I18n.t('ach_grammatico'); },
      verificar(p) { return (p.grammatica_completadas || []).length >= 10; }
    },
    {
      id: 'precisione',
      emoji: '🎯',
      nome: 'Precisione',
      get descricao() { return I18n.t('ach_precisione'); },
      verificar(p) { return (p.quiz_consecutivos_80 || 0) >= 5; }
    },
    {
      id: 'notturno',
      emoji: '🌙',
      nome: 'Notturno',
      get descricao() { return I18n.t('ach_notturno'); },
      verificar(p) { return (p.ultimo_estudo_hora || -1) >= 22; }
    },
    {
      id: 'mattiniero',
      emoji: '☀️',
      nome: 'Mattiniero',
      get descricao() { return I18n.t('ach_mattiniero'); },
      verificar(p) { const h = p.ultimo_estudo_hora; return h !== undefined && h >= 0 && h < 7; }
    }
  ],

  // ── Check all achievements ─────────────────────────────────
  verificar() {
    const p  = App.estado.progresso;
    const fd = App.estado.flashcardData;
    if (!p) return;
    if (!p.conquistas) p.conquistas = [];

    this.LISTA.forEach(c => {
      if (p.conquistas.includes(c.id)) return;
      try {
        if (c.verificar(p, fd)) this._desbloquear(c.id);
      } catch (e) { console.warn('[Conquistas] erro ao verificar', c.id, e); }
    });
  },

  // ── Trigger quiz-perfetto manually ────────────────────────
  ganharQuizPerfetto() {
    // Persist a flag so verificar() can recover the achievement
    // even if conquistas[] was somehow reset (e.g. corrupted save).
    const p = App.estado.progresso;
    if (p) p.quiz_perfetto_ganha = true;
    this._desbloquear('quiz_perfetto');
  },

  // ── Unlock an achievement ──────────────────────────────────
  _desbloquear(id) {
    const p = App.estado.progresso;
    if (!p) return;
    if (!p.conquistas) p.conquistas = [];
    if (p.conquistas.includes(id)) return;

    p.conquistas.push(id);
    App.salvarProgresso();

    const c = this.LISTA.find(x => x.id === id);
    if (c) this._mostrarModal(c);
  },

  // ── Show unlock modal ──────────────────────────────────────
  _mostrarModal(c) {
    const modal = document.getElementById('conquista-modal');
    if (!modal) return;
    const el = n => document.getElementById(n);
    if (el('conquista-emoji')) el('conquista-emoji').textContent = c.emoji;
    if (el('conquista-nome'))  el('conquista-nome').textContent  = c.nome;
    if (el('conquista-desc'))  el('conquista-desc').textContent  = c.descricao;
    modal.classList.add('ativo');
    if (typeof SomFeedback !== 'undefined') SomFeedback.nivelUp();
  },

  fecharModal() {
    const modal = document.getElementById('conquista-modal');
    if (modal) modal.classList.remove('ativo');
  },

  // ── Render badge wall (optional panel) ────────────────────
  renderizarPainel(containerId) {
    const el = document.getElementById(containerId);
    if (!el) return;
    const conquistadas = (App.estado.progresso || {}).conquistas || [];
    el.innerHTML = this.LISTA.map(c => {
      const desbloqueada = conquistadas.includes(c.id);
      return `
        <div class="conquista-badge${desbloqueada ? '' : ' bloqueada'}" title="${c.descricao}">
          <span class="conquista-badge-emoji">${c.emoji}</span>
          <span class="conquista-badge-nome">${c.nome}</span>
        </div>`;
    }).join('');
  },

  // ── Painel completo com conquistas desbloqueadas + bloqueadas ─
  renderizarPainelCompleto() {
    const p = App.estado.progresso || {};
    const fd = App.estado.flashcardData || {};
    const conquistadas = p.conquistas || [];
    const total = this.LISTA.length;
    const ganhas = conquistadas.length;

    const desbloqueadas = this.LISTA.filter(c => conquistadas.includes(c.id));
    const bloqueadas    = this.LISTA.filter(c => !conquistadas.includes(c.id));

    const renderBadge = (c, ganhou) => `
      <div class="ach-item${ganhou ? ' ach-ganhou' : ' ach-bloqueada'}" title="${c.descricao}">
        <span class="ach-emoji">${ganhou ? c.emoji : '🔒'}</span>
        <div class="ach-info">
          <div class="ach-nome">${c.nome}</div>
          <div class="ach-desc">${c.descricao}</div>
        </div>
        ${ganhou ? '<span class="ach-check">✅</span>' : ''}
      </div>`;

    return `
      <div class="ach-progresso-bar-wrap">
        <div class="ach-progresso-bar">
          <div class="ach-progresso-fill" style="width:${Math.round(ganhas/total*100)}%"></div>
        </div>
        <span class="ach-progresso-label">${ganhas} / ${total}</span>
      </div>
      ${ganhas > 0 ? `
        <div class="ach-secao-titulo">✅ Conquistados</div>
        <div class="ach-lista">${desbloqueadas.map(c => renderBadge(c, true)).join('')}</div>
      ` : ''}
      <div class="ach-secao-titulo" style="margin-top:${ganhas > 0 ? '1rem' : '0'}">🔒 Em progresso</div>
      <div class="ach-lista">${bloqueadas.map(c => renderBadge(c, false)).join('')}</div>
    `;
  }
};
