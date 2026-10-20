// ============================================================
// js/core/templo_modal.js — Temple Detail & Unlock Modal (ARC-02)
// ============================================================

const AppTemploModal = {
  abrirModalTemplo(i) {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    if (!estado) return;

    const data = estado.templosData[i];
    const desbloqueado = estado.progresso?.templos_desbloqueados?.includes(i) ?? false;
    const concluido    = estado.progresso?.templos_concluidos?.includes(i) ?? false;

    const cores = (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_CORES : [];
    const nomes = (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_NOMES : [];
    const descricoes = (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_DESC : [];
    const niveisMinimos = (typeof AppTemploData !== 'undefined') ? AppTemploData.TEMPLO_NIVEL_MINIMO : {};

    const cor          = cores[i] || cores[1] || '#9B2335';
    const nome         = (data && data.nome) ? data.nome : (nomes[i] || `Tempio ${i}`);
    const cidade       = data ? data.cidade : '—';
    const nivel        = data ? data.nivel : '—';
    const desc         = descricoes[i] || '';
    const nivelMinimo  = niveisMinimos[i] || i;
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

    const body = document.getElementById('templo-modal-body');
    if (!body) return;

    const escapeFn = (typeof AppState !== 'undefined' && AppState.escapeHtml)
      ? AppState.escapeHtml
      : (str => String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'));

    const nomeEsc = escapeFn(nome);
    const cidadeEsc = escapeFn(cidade);
    const descEsc = escapeFn(desc);
    const nivelEsc = escapeFn(nivel);

    body.innerHTML = `
      <div class="tm-header" style="background:${cor}${!desbloqueado ? ';filter:grayscale(0.5)' : ''}">
        <button class="tm-close" onclick="App.fecharModalTemplo()" title="Chiudi">✕</button>
        <div class="tm-num">Tempio ${i}</div>
        <div class="tm-nome">${nomeEsc}</div>
        <div class="tm-meta">
          <span class="tm-badge">📍 ${cidadeEsc}</span>
          <span class="tm-badge">${nivelEsc}</span>
          ${concluido ? '<span class="tm-badge">✅ Completo</span>' : ''}
        </div>
      </div>
      <div class="tm-content">
        ${desbloqueado ? `
          <div class="tm-progress-wrap">
            <div class="tm-progress-label">${dominadas} / ${totalPalavras} parole dominate · ${progPercent}%</div>
            <div class="tm-progress-bar"><div class="tm-progress-fill" style="width:${progPercent}%"></div></div>
          </div>
        ` : `<div class="tm-lock-banner">🔒 Richiede Livello ${nivelMinimo}</div>`}
        <p class="tm-desc">${descEsc}</p>
        ${desbloqueado ? `
          <div class="tm-actions">
            <button class="tm-btn-primary" onclick="App.fecharModalTemplo();App.estudarTemplo(${i})">📚 Studia i vocaboli</button>
            <button class="tm-btn-quiz" onclick="App.fecharModalTemplo();App.quizTemplo(${i})">❓ Fai il Quiz</button>
          </div>
        ` : `
          <details class="tm-unlock-area" id="tm-unlock-details">
            <summary>Hai un codice di accesso?</summary>
            <div class="tm-unlock-form">
              <input id="tm-code-input" type="password" placeholder="Inserisci il codice..." class="tm-code-input"
                onkeydown="if(event.key==='Enter')App.tentarDesbloquear(${i})">
              <button onclick="App.tentarDesbloquear(${i})" class="tm-btn-unlock">Sblocca</button>
            </div>
          </details>
        `}
      </div>
    `;

    const modal = document.getElementById('templo-modal');
    if (modal) modal.classList.add('ativo');
    if (typeof document !== 'undefined') document.body.style.overflow = 'hidden';
  },

  fecharModalTemplo() {
    const modal = document.getElementById('templo-modal');
    if (modal) modal.classList.remove('ativo');
    if (typeof document !== 'undefined') document.body.style.overflow = '';
  },

  pedirSenhaTemplo(temploNum) {
    this.abrirModalTemplo(temploNum);
    const details = document.getElementById('tm-unlock-details');
    if (details) details.open = true;
    const input = document.getElementById('tm-code-input');
    if (input) setTimeout(() => input.focus(), 120);
  },

  async tentarDesbloquear(temploNum) {
    const input = document.getElementById('tm-code-input');
    if (!input) return;

    const verificarFn = (typeof AppState !== 'undefined' && AppState.verificarCodigoAcesso)
      ? AppState.verificarCodigoAcesso.bind(AppState)
      : ((typeof App !== 'undefined' && App.verificarCodigoAcesso) ? App.verificarCodigoAcesso.bind(App) : async () => false);

    const valido = await verificarFn(input.value);
    if (valido) {
      const estado = (typeof AppState !== 'undefined' && AppState.estado)
        ? AppState.estado
        : (typeof App !== 'undefined' && App.estado ? App.estado : null);

      if (estado && estado.progresso) {
        estado.progresso.templos_desbloqueados = Array.from({length: 51}, (_, i) => i + 1);
        if (typeof AppState !== 'undefined' && typeof AppState.salvarProgresso === 'function') {
          AppState.salvarProgresso();
        } else if (typeof App !== 'undefined' && typeof App.salvarProgresso === 'function') {
          App.salvarProgresso();
        }
      }
      this.fecharModalTemplo();

      if (typeof AppTemplos !== 'undefined' && typeof AppTemplos.renderizarTemplos === 'function') {
        AppTemplos.renderizarTemplos();
      } else if (typeof App !== 'undefined' && typeof App.renderizarTemplos === 'function') {
        App.renderizarTemplos();
      }

      if (typeof AppStats !== 'undefined' && typeof AppStats.atualizarStats === 'function') {
        AppStats.atualizarStats();
      } else if (typeof App !== 'undefined' && typeof App.atualizarStats === 'function') {
        App.atualizarStats();
      }

      const notifFn = (typeof AppTTS !== 'undefined' && AppTTS.notificar)
        ? AppTTS.notificar
        : (typeof App !== 'undefined' ? App.notificar : null);
      if (notifFn) notifFn('notif_tutti_sbloccati', 'sucesso');
    } else {
      input.style.borderColor = '#C0392B';
      input.value = '';
      input.placeholder = 'Codice non corretto…';
      setTimeout(() => { input.style.borderColor = ''; input.placeholder = 'Inserisci il codice...'; }, 2000);
    }
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppTemploModal = AppTemploModal;
}
if (typeof window !== 'undefined') {
  window.AppTemploModal = AppTemploModal;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppTemploModal;
}
