// ============================================================
// js/core/backup_reminder.js — Popup Periódico de Alerta de Backup
// ============================================================

const BackupReminder = {
  CHAVE_STORAGE: 'it_ultimo_aviso_backup',
  INTERVALO_MS: 3 * 24 * 60 * 60 * 1000, // 3 dias em milissegundos
  DURACAO_MS: 20000,                     // 20 segundos na tela

  _timerTimeout: null,
  _tempoRestante: 20000,
  _inicioTimer: null,
  _elementoPopup: null,
  _barraProgresso: null,
  _estaPausado: false,

  /**
   * Verifica se já se passaram 3 dias desde o último aviso (ou se nunca foi exibido).
   * @returns {boolean}
   */
  deveExibir() {
    try {
      const ultimo = localStorage.getItem(this.CHAVE_STORAGE);
      if (!ultimo) return true;
      const ts = parseInt(ultimo, 10);
      if (isNaN(ts)) return true;
      return (Date.now() - ts) >= this.INTERVALO_MS;
    } catch (_e) {
      return false;
    }
  },

  /**
   * Ponto de entrada chamado após a inicialização do app.
   */
  verificarLembrete() {
    if (typeof window === 'undefined' || typeof document === 'undefined') return;
    if (!this.deveExibir()) return;

    // Aguarda 1.5s para esperar o cabeçalho e a tela inicial carregarem suavemente
    setTimeout(() => {
      if (this.deveExibir() && !document.getElementById('backup-reminder-popup')) {
        this.exibir();
      }
    }, 1500);
  },

  /**
   * Renderiza o popup no canto superior direito sem obstruir os botões do header.
   */
  exibir() {
    if (typeof document === 'undefined') return;
    if (document.getElementById('backup-reminder-popup')) return;

    // Remove qualquer container anterior
    this.fechar(false);

    const isIt = typeof I18n !== 'undefined' && I18n.idioma === 'it';

    const titulo = (typeof I18n !== 'undefined' && typeof I18n.t === 'function' && I18n.t('backup_popup_titulo'))
      || (isIt ? '⚠️ Salva i tuoi Progressi!' : '⚠️ Salve seu Progresso!');

    const desc = (typeof I18n !== 'undefined' && typeof I18n.t === 'function' && I18n.t('backup_popup_desc'))
      || (isIt ? 'Se la cache o la cronologia del browser vengono cancellate, perderai i tuoi progressi di studio (XP, flashcard e templi). Fai un backup regolare!' : 'Se o cache ou histórico do navegador forem limpos, você perderá sua evolução nos estudos (XP, flashcards e templos). Faça um backup regular!');

    const btnTexto = (typeof I18n !== 'undefined' && typeof I18n.t === 'function' && I18n.t('backup_popup_btn'))
      || (isIt ? '💾 Salva Backup Adesso' : '💾 Fazer Backup Agora');

    const fecharTexto = (typeof I18n !== 'undefined' && typeof I18n.t === 'function' && I18n.t('backup_popup_fechar'))
      || (isIt ? 'Chiudi' : 'Fechar');

    const container = document.createElement('div');
    container.id = 'backup-reminder-popup';
    container.className = 'backup-popup-container';
    container.setAttribute('role', 'alert');
    container.setAttribute('aria-live', 'polite');

    container.innerHTML = `
      <div class="backup-popup-card">
        <div class="backup-popup-header">
          <div class="backup-popup-title">
            <span class="backup-popup-icon" aria-hidden="true">🛡️</span>
            <strong>${titulo}</strong>
          </div>
          <button class="backup-popup-close" id="backup-popup-close-btn" aria-label="${fecharTexto}" title="${fecharTexto}">✕</button>
        </div>
        <p class="backup-popup-desc">${desc}</p>
        <div class="backup-popup-actions">
          <button class="backup-popup-btn" id="backup-popup-action-btn">
            ${btnTexto}
          </button>
        </div>
        <div class="backup-popup-progress-track">
          <div class="backup-popup-progress" id="backup-popup-progress-bar"></div>
        </div>
      </div>
    `;

    document.body.appendChild(container);
    this._elementoPopup = container;
    this._barraProgresso = document.getElementById('backup-popup-progress-bar');

    // Eventos
    const btnClose = document.getElementById('backup-popup-close-btn');
    if (btnClose) {
      btnClose.addEventListener('click', () => {
        this.registrarExibicao();
        this.fechar(true);
      });
    }

    const btnAction = document.getElementById('backup-popup-action-btn');
    if (btnAction) {
      btnAction.addEventListener('click', () => {
        this.acionarBackup();
      });
    }

    // Pausar contagem no hover para não fechar na cara do usuário
    container.addEventListener('mouseenter', () => this.pausar());
    container.addEventListener('mouseleave', () => this.retomar());

    // Iniciar temporizador de 20s
    this._tempoRestante = this.DURACAO_MS;
    this._iniciarTemporizador(this._tempoRestante);
  },

  _iniciarTemporizador(ms) {
    if (this._timerTimeout) clearTimeout(this._timerTimeout);
    this._inicioTimer = Date.now();
    this._estaPausado = false;

    if (this._barraProgresso) {
      this._barraProgresso.style.animationPlayState = 'running';
    }

    this._timerTimeout = setTimeout(() => {
      this.registrarExibicao();
      this.fechar(true);
    }, ms);
  },

  /**
   * Pausa a contagem regressiva se o usuário estiver com o mouse sobre o popup.
   */
  pausar() {
    if (this._estaPausado || !this._timerTimeout) return;
    this._estaPausado = true;
    clearTimeout(this._timerTimeout);
    this._timerTimeout = null;

    const decorrido = Date.now() - (this._inicioTimer || Date.now());
    this._tempoRestante = Math.max(0, this._tempoRestante - decorrido);

    if (this._barraProgresso) {
      this._barraProgresso.style.animationPlayState = 'paused';
    }
  },

  /**
   * Retoma a contagem regressiva quando o mouse sai do popup.
   */
  retomar() {
    if (!this._estaPausado || this._tempoRestante <= 0) return;
    this._iniciarTemporizador(this._tempoRestante);
  },

  /**
   * Dispara a rotina de exportação do backup e fecha o popup.
   */
  acionarBackup() {
    try {
      if (typeof Profilo !== 'undefined' && typeof Profilo.exportarDados === 'function') {
        Profilo.exportarDados();
      } else if (typeof App !== 'undefined' && typeof App.exportarBackup === 'function') {
        App.exportarBackup();
      }
    } catch (e) {
      console.error('Erro ao acionar backup via popup:', e);
    }
    this.registrarExibicao();
    this.fechar(true);
  },

  /**
   * Atualiza a data da última exibição no localStorage para garantir intervalo de 3 dias.
   */
  registrarExibicao() {
    try {
      localStorage.setItem(this.CHAVE_STORAGE, Date.now().toString());
    } catch (_e) {
      // Falha silenciosa de localStorage
    }
  },

  /**
   * Fecha o popup com transição animada.
   */
  fechar(animado = true) {
    if (this._timerTimeout) {
      clearTimeout(this._timerTimeout);
      this._timerTimeout = null;
    }

    const el = this._elementoPopup || document.getElementById('backup-reminder-popup');
    if (!el) return;

    if (!animado) {
      if (el.parentNode) el.parentNode.removeChild(el);
      this._elementoPopup = null;
      return;
    }

    el.classList.add('saindo');
    setTimeout(() => {
      if (el.parentNode) el.parentNode.removeChild(el);
      this._elementoPopup = null;
    }, 350);
  }
};

// Exporta globalmente para o navegador e ambientes de teste
if (typeof window !== 'undefined') {
  window.BackupReminder = BackupReminder;
}
if (typeof globalThis !== 'undefined') {
  globalThis.BackupReminder = BackupReminder;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BackupReminder;
}

