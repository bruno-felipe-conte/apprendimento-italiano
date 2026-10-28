// ============================================================
// js/core/templos.js — Temples Grid & Interaction (ARC-02)
// ============================================================

const AppTemplos = {
  get TEMPLO_CORES() {
    return (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_CORES : [];
  },
  get TEMPLO_NOMES() {
    return (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_NOMES : [];
  },
  get TEMPLO_NIVEL_MINIMO() {
    return (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_NIVEL_MINIMO : {};
  },
  get TEMPLO_DESC() {
    return (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_DESC : [];
  },

  // ── Temple grid rendering ──────────────────────────────────
  renderizarTemplos() {
    if (typeof document === 'undefined') return;

    // Render card continuar
    const contContainer = document.getElementById('continuar-container');
    if (contContainer) {
      const renderContinuarFn = (typeof AppStats !== 'undefined' && AppStats.renderizarCardContinuar)
        ? AppStats.renderizarCardContinuar.bind(AppStats)
        : ((typeof App !== 'undefined' && App.renderizarCardContinuar) ? App.renderizarCardContinuar.bind(App) : () => '');
      contContainer.innerHTML = renderContinuarFn();
    }

    // Render meta com prazo
    const metaContainer = document.getElementById('meta-prazo-container');
    if (metaContainer) {
      const renderMetaPrazoFn = (typeof AppMeta !== 'undefined' && AppMeta._renderizarMetaPrazo)
        ? AppMeta._renderizarMetaPrazo.bind(AppMeta)
        : ((typeof AppStats !== 'undefined' && AppStats._renderizarMetaPrazo)
          ? AppStats._renderizarMetaPrazo.bind(AppStats)
          : ((typeof App !== 'undefined' && App._renderizarMetaPrazo) ? App._renderizarMetaPrazo.bind(App) : () => ''));
      metaContainer.innerHTML = renderMetaPrazoFn();
    }

    const grid = document.getElementById('templos-grid');
    if (!grid) return;
    grid.innerHTML = '';

    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    if (!estado) return;

    for (let i = 1; i <= 51; i++) {
      if (!estado.templosData[i] && !this.TEMPLO_NIVEL_MINIMO[i]) continue;
      const data = estado.templosData[i];
      const desbloqueado = estado.progresso?.templos_desbloqueados?.includes(i) ?? false;
      const concluido = estado.progresso?.templos_concluidos?.includes(i) ?? false;
      const nivelMinimo = this.TEMPLO_NIVEL_MINIMO[i] || i;
      const cor = this.TEMPLO_CORES[i] || this.TEMPLO_CORES[1];

      const nome = (data && data.nome) ? data.nome : (this.TEMPLO_NOMES[i] || `Tempio ${i}`);
      const cidade = data ? data.cidade : '—';
      const nivel = data ? data.nivel : '—';
      const totalPalavras = data && data.palavras ? data.palavras.length : 0;

      let dominadas = 0;
      if (data && data.palavras) {
        dominadas = data.palavras.filter(p => {
          const sm = estado.flashcardData[p.id];
          if (!sm) return false;
          return (sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7);
        }).length;
      }

      const progPercent = totalPalavras > 0 ? Math.round((dominadas / totalPalavras) * 100) : 0;
      const txtDominadas = typeof I18n !== 'undefined'
        ? I18n.t('templo_palavras_dom').replace('{dom}', String(dominadas)).replace('{tot}', String(totalPalavras))
        : `${dominadas}/${totalPalavras} parole dominate`;
      const badgeCompleto = concluido
        ? `<span class="nivel-badge">${typeof I18n !== 'undefined' ? I18n.t('templo_completo_badge') : 'Completato'}</span>`
        : '';

      const card = document.createElement('div');
      card.className = `templo-card${desbloqueado ? '' : ' bloqueado'}${concluido ? ' concluido' : ''}`;

      if (desbloqueado) {
        card.style.cursor = 'pointer';
        card.onclick = () => this.estudarTemplo(i);
        card.innerHTML = `
          <div class="templo-header" style="background:${cor}">
            <div class="templo-num">Tempio ${i}</div>
            <div class="templo-nome">${nome}</div>
            <div class="templo-meta">
              <span class="templo-cidade">📍 ${cidade}</span>
              <span class="nivel-badge">${nivel}</span>
              ${badgeCompleto}
            </div>
          </div>
          <div class="templo-body">
            <div class="progresso-label">${txtDominadas}</div>
            <div class="progresso-bar-container">
              <div class="progresso-bar-fill" style="width:${progPercent}%"></div>
            </div>
          </div>
        `;
      } else {
        card.style.cursor = 'pointer';
        card.onclick = () => this.abrirModalTemplo(i);
        const lockText = typeof I18n !== 'undefined'
          ? I18n.t('templo_requer').replace('{n}', String(nivelMinimo))
          : `Richiede Livello ${nivelMinimo}`;
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
            <div class="lock-info">${lockText}</div>
            <div class="progresso-bar-container">
              <div class="progresso-bar-fill" style="width:0%"></div>
            </div>
          </div>
        `;
      }

      grid.appendChild(card);
    }

    if (typeof AppFavorites !== 'undefined' && typeof AppFavorites.renderizarParolaDia === 'function') {
      AppFavorites.renderizarParolaDia();
    } else if (typeof App !== 'undefined' && typeof App.renderizarParolaDia === 'function') {
      App.renderizarParolaDia();
    }
  },

  estudarTemplo(temploNum) {
    if (typeof AppNavigation !== 'undefined' && typeof AppNavigation.navegar === 'function') {
      AppNavigation.navegar('flashcard');
    } else if (typeof App !== 'undefined' && typeof App.navegar === 'function') {
      App.navegar('flashcard');
    }
    const sel = document.getElementById('flashcard-templo-select');
    if (sel) sel.value = String(temploNum);
    if (typeof Flashcards !== 'undefined') Flashcards.init(temploNum);
  },

  estudarPalavra(palavraId, temploNum) {
    if (typeof AppNavigation !== 'undefined' && typeof AppNavigation.navegar === 'function') {
      AppNavigation.navegar('flashcard');
    } else if (typeof App !== 'undefined' && typeof App.navegar === 'function') {
      App.navegar('flashcard');
    }
    const sel = document.getElementById('flashcard-templo-select');
    if (sel) sel.value = String(temploNum);
    if (typeof Flashcards === 'undefined') return;
    Flashcards.init(temploNum);
    const idx = Flashcards.cartasDisponiveis.findIndex(p => p.id === palavraId);
    if (idx > 0) {
      const [carta] = Flashcards.cartasDisponiveis.splice(idx, 1);
      Flashcards.cartasDisponiveis.unshift(carta);
      Flashcards.indiceAtual = 0;
      Flashcards.mostrarCarta();
    }
  },

  quizTemplo(temploNum) {
    if (typeof AppNavigation !== 'undefined' && typeof AppNavigation.navegar === 'function') {
      AppNavigation.navegar('quiz');
    } else if (typeof App !== 'undefined' && typeof App.navegar === 'function') {
      App.navegar('quiz');
    }
    if (typeof Quiz !== 'undefined') {
      Quiz.iniciar(temploNum);
    }
  },

  // ── Delegation to AppTemploModal ───────────────────────────
  abrirModalTemplo(i) {
    if (typeof AppTemploModal !== 'undefined') {
      AppTemploModal.abrirModalTemplo(i);
    }
  },

  fecharModalTemplo() {
    if (typeof AppTemploModal !== 'undefined') {
      AppTemploModal.fecharModalTemplo();
    }
  },

  pedirSenhaTemplo(temploNum) {
    if (typeof AppTemploModal !== 'undefined') {
      AppTemploModal.pedirSenhaTemplo(temploNum);
    }
  },

  tentarDesbloquear(temploNum) {
    if (typeof AppTemploModal !== 'undefined') {
      return AppTemploModal.tentarDesbloquear(temploNum);
    }
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppTemplos = AppTemplos;
}
if (typeof window !== 'undefined') {
  window.AppTemplos = AppTemplos;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppTemplos;
}
