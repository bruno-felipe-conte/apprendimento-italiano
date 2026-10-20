// ============================================================
// js/core/meta.js — Daily Goals & Deadline Target Modal (ARC-02)
// ============================================================

const AppMeta = {
  _renderizarMetaPrazo() {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    if (typeof I18n === 'undefined') return '';
    if (!p || !p.meta_prazo) {
      return `<div class="card-meta-prazo card-meta-vazia" onclick="App.abrirModalMetaPrazo()">
        <span>🎯</span>
        <span>${I18n.t('meta_definir_prazo')}</span>
        <span class="cc-cta">→</span>
      </div>`;
    }
    if (typeof Progressao === 'undefined' || !Progressao.calcularMetaPrazo) return '';
    const dados = Progressao.calcularMetaPrazo();
    if (!dados) return '';
    const cor = dados.atingeNoPrazo ? '#27AE60' : '#E74C3C';
    const emoji = dados.atingeNoPrazo ? '✅' : '⚠️';
    return `<div class="card-meta-prazo" onclick="App.abrirModalMetaPrazo()">
      <div class="meta-prazo-titulo">${emoji} ${I18n.idioma === 'it' ? 'Obiettivo' : 'Meta'}: ${I18n.idioma === 'it' ? 'Livello' : 'Nível'} ${dados.nivel_alvo} ${I18n.idioma === 'it' ? 'entro il' : 'até'} ${new Date(dados.data_alvo).toLocaleDateString(I18n.idioma === 'it' ? 'it-IT' : 'pt-BR', {timeZone: 'UTC'})}</div>
      <div class="meta-prazo-info">
        <span style="color:${cor}">${dados.xpPorDia} ${I18n.t('meta_xp_necessarios')}</span>
        <span>·</span>
        <span>${I18n.t('meta_dias_restantes').replace('{n}', String(dados.diasRestantes))}</span>
      </div>
      <div class="meta-prazo-previsao">${I18n.t('meta_no_ritmo')} ${dados.dataPrevisao}</div>
    </div>`;
  },

  // ── Meta Diária settings ──────────────────────────────────
  abrirMetaSettings() {
    const modal = document.getElementById('meta-settings-modal');
    if (!modal) return;
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const meta = (estado?.progresso || {}).meta_diaria || 100;
    modal.querySelectorAll('.meta-op-btn').forEach(btn => {
      btn.classList.toggle('ativo', parseInt(btn.dataset.val || '0') === meta);
    });
    modal.style.display = 'flex';
  },

  fecharMetaSettings() {
    const modal = document.getElementById('meta-settings-modal');
    if (modal) modal.style.display = 'none';
  },

  setMeta(valor) {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    if (!estado || !estado.progresso) return;
    const anterior = estado.progresso.meta_diaria;
    estado.progresso.meta_diaria = valor;

    if (typeof AppStats !== 'undefined' && typeof AppStats.atualizarStats === 'function') {
      AppStats.atualizarStats();
    } else if (typeof App !== 'undefined' && typeof App.atualizarStats === 'function') {
      App.atualizarStats();
    }

    this.fecharMetaSettings();
    const metaBar = document.querySelector('.daily-goal-bar');
    if (metaBar) {
      metaBar.classList.remove('optimistic-xp-pulse');
      void metaBar.offsetWidth;
      metaBar.classList.add('optimistic-xp-pulse');
    }
    try {
      if (typeof AppState !== 'undefined' && typeof AppState.salvarProgresso === 'function') {
        AppState.salvarProgresso();
      } else if (typeof App !== 'undefined' && typeof App.salvarProgresso === 'function') {
        App.salvarProgresso();
      }
      const notifFn = (typeof AppTTS !== 'undefined' && AppTTS.notificar)
        ? AppTTS.notificar
        : (typeof App !== 'undefined' ? App.notificar : null);
      if (notifFn && typeof I18n !== 'undefined') {
        notifFn(I18n.t('notif_meta_definida').replace('{val}', String(valor)), 'sucesso');
      }
    } catch (_) {
      estado.progresso.meta_diaria = anterior;
      if (typeof AppStats !== 'undefined' && typeof AppStats.atualizarStats === 'function') {
        AppStats.atualizarStats();
      } else if (typeof App !== 'undefined' && typeof App.atualizarStats === 'function') {
        App.atualizarStats();
      }
    }
  },

  // ── Meta Prazo Modal ────────────────────────────────────────
  abrirModalMetaPrazo() {
    const modal = document.getElementById('modal-meta-prazo');
    if (!modal) return;
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    if (p && p.meta_prazo) {
      const elNivel = document.getElementById('meta-nivel-alvo');
      const elData = document.getElementById('meta-data-alvo');
      if (elNivel) elNivel.value = p.meta_prazo.nivel_alvo;
      if (elData) elData.value = p.meta_prazo.data_alvo;
    }
    modal.style.display = 'flex';
  },

  fecharModalMetaPrazo() {
    const modal = document.getElementById('modal-meta-prazo');
    if (modal) modal.style.display = 'none';
  },

  confirmarMetaPrazo() {
    const elNivel = document.getElementById('meta-nivel-alvo');
    const elData = document.getElementById('meta-data-alvo');
    if (!elNivel || !elData) return;
    const nivelAlvo = parseInt(elNivel.value);
    const dataAlvo = elData.value;
    if (!nivelAlvo || !dataAlvo) return;

    if (new Date(dataAlvo).getTime() <= Date.now()) {
      const notifFn = (typeof AppTTS !== 'undefined' && AppTTS.notificar)
        ? AppTTS.notificar
        : (typeof App !== 'undefined' ? App.notificar : null);
      if (notifFn) notifFn('notif_data_futura', 'erro');
      return;
    }

    if (typeof Progressao !== 'undefined') {
      Progressao.definirMetaPrazo(nivelAlvo, dataAlvo);
    }
    this.fecharModalMetaPrazo();
    if (typeof AppTemplos !== 'undefined' && typeof AppTemplos.renderizarTemplos === 'function') {
      AppTemplos.renderizarTemplos();
    } else if (typeof App !== 'undefined' && typeof App.renderizarTemplos === 'function') {
      App.renderizarTemplos();
    }
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppMeta = AppMeta;
}
if (typeof window !== 'undefined') {
  window.AppMeta = AppMeta;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppMeta;
}
