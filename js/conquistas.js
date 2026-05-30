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
      descricao: 'Complete seu primeiro flashcard',
      verificar(p, fd) { return Object.keys(fd).length >= 1; }
    },
    {
      id: 'uma_semana',
      emoji: '🔥',
      nome: 'Una Settimana',
      descricao: '7 dias consecutivos de estudo',
      verificar(p) { return (p.streak || 0) >= 7; }
    },
    {
      id: 'estudioso',
      emoji: '📚',
      nome: 'Studioso',
      descricao: 'Revisar 100 cartas nos flashcards',
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
      descricao: '10/10 acertos em um quiz',
      verificar() { return false; } // triggered via ganharQuizPerfetto()
    },
    {
      id: 'primo_tempio',
      emoji: '🏛️',
      nome: 'Primo Tempio',
      descricao: 'Completar o Tempio 1 nos flashcards',
      verificar(p) { return (p.templos_concluidos || []).includes(1); }
    },
    {
      id: 'vocabulario',
      emoji: '⭐',
      nome: 'Vocabolario Ricco',
      descricao: 'Dominar 50 palavras (3+ revisões)',
      verificar(p, fd) {
        let total = 0;
        for (const k in fd) {
          const sm = fd[k];
          if ((sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7)) total++;
        }
        return total >= 50;
      }
    },
    {
      id: 'duro',
      emoji: '💪',
      nome: 'Duro!',
      descricao: 'Marcar "Esqueci" 50 vezes — a perseverança tem recompensa',
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
      descricao: 'Atingir o Livello 10',
      verificar(p) { return (p.nivel || 1) >= 10; }
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
      } catch (e) { /* ignore */ }
    });
  },

  // ── Trigger quiz-perfetto manually ────────────────────────
  ganharQuizPerfetto() {
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
  }
};
