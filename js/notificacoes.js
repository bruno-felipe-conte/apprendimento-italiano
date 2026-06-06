// ============================================================
// notificacoes.js — Lembretes de revisão via Push Notifications
// Agendamento local (sem servidor) — funciona offline via SW
// ============================================================

const Notificacoes = {
  STORAGE_KEY: 'it_notif_hora',  // hora preferida do lembrete (ex: "20:00")
  STORAGE_PERM: 'it_notif_perm', // 'granted' | 'denied' | 'pending'

  // ── Pede permissão ao usuário ────────────────────────────
  async pedirPermissao() {
    if (!('Notification' in window)) return 'unsupported';
    if (Notification.permission === 'granted') return 'granted';
    if (Notification.permission === 'denied')  return 'denied';

    const result = await Notification.requestPermission();
    try { localStorage.setItem(this.STORAGE_PERM, result); } catch(_) {}

    if (result === 'granted') {
      if (typeof App !== 'undefined') {
        App.notificar('🔔 Lembretes ativados!', 'sucesso');
      }
      this.agendarHoje();
    }
    return result;
  },

  // ── Verifica se notificações estão habilitadas ───────────
  habilitado() {
    return ('Notification' in window) && Notification.permission === 'granted';
  },

  // ── Agenda lembrete para a hora preferida hoje (ou amanhã) ──
  agendarHoje() {
    if (!this.habilitado()) return;
    if (!('serviceWorker' in navigator)) return;

    const horaStr = this.getHora(); // ex: "20:00"
    const [h, m]  = horaStr.split(':').map(Number);
    const agora   = new Date();
    const alvo    = new Date();
    alvo.setHours(h, m, 0, 0);

    // Se já passou da hora hoje, agenda para amanhã
    if (alvo <= agora) alvo.setDate(alvo.getDate() + 1);

    const delayMs = alvo.getTime() - agora.getTime();

    // Conta cartas vencidas para personalizar mensagem
    const { devidas, novas } = this._contarCartas();
    const total = devidas + novas;

    const it = typeof I18n !== 'undefined' && I18n.idioma === 'it';
    let corpo;
    if (total === 0) {
      corpo = it ? '✅ Nessuna carta in scadenza — ottimo lavoro oggi!' : '✅ Nenhuma carta vencida — ótimo trabalho hoje!';
    } else if (devidas > 0 && novas > 0) {
      corpo = it
        ? `📚 ${devidas} carta${devidas !== 1 ? 'e' : ''} da ripassare + ${novas} nuova${novas !== 1 ? 'e' : ''} che ti aspettano.`
        : `📚 ${devidas} carta${devidas !== 1 ? 's' : ''} em revisão + ${novas} nova${novas !== 1 ? 's' : ''} esperando você.`;
    } else if (devidas > 0) {
      corpo = it
        ? `⏰ ${devidas} carta${devidas !== 1 ? 'e' : ''} scaduta${devidas !== 1 ? 'e' : ''} — non perdere il ritmo!`
        : `⏰ ${devidas} carta${devidas !== 1 ? 's' : ''} vencida${devidas !== 1 ? 's' : ''} — não perca o ritmo!`;
    } else {
      corpo = it
        ? `🌱 ${novas} parola${novas !== 1 ? 'e' : ''} nuova${novas !== 1 ? 'e' : ''} pronta${novas !== 1 ? 'e' : ''} da imparare.`
        : `🌱 ${novas} palavra${novas !== 1 ? 's' : ''} nova${novas !== 1 ? 's' : ''} pronta${novas !== 1 ? 's' : ''} para aprender.`;
    }

    navigator.serviceWorker.ready.then(reg => {
      // Envia para o SW agendar
      reg.active?.postMessage({
        type:    'AGENDAR_LEMBRETE',
        delayMs,
        titulo:  '🇮🇹 Italiano Autentico',
        corpo,
        tag:     'italiano-revisao',
      });
    });
  },

  // ── Hora preferida para lembretes ──────────────────────
  getHora() {
    try { return localStorage.getItem(this.STORAGE_KEY) || '20:00'; } catch(_) { return '20:00'; }
  },

  setHora(hora) {
    try { localStorage.setItem(this.STORAGE_KEY, hora); } catch(_) {}
    this.agendarHoje();
    if (typeof App !== 'undefined') {
      const it = typeof I18n !== 'undefined' && I18n.idioma === 'it';
      App.notificar(it ? `🔔 Promemoria impostato per le ${hora}` : `🔔 Lembrete configurado para as ${hora}`, 'sucesso');
    }
  },

  // ── Conta cartas vencidas em todos os templos desbloqueados ─
  _contarCartas() {
    const p = typeof App !== 'undefined' ? App.estado.progresso : null;
    if (!p) return { devidas: 0, novas: 0 };
    const agora  = Date.now();
    let devidas  = 0, novas = 0;
    p.templos_desbloqueados.forEach(num => {
      const data = App.estado.templosData[num];
      if (!data || !data.palavras) return;
      data.palavras.forEach(pw => {
        const f = App.estado.flashcardData[pw.id];
        if (!f || f.state === 'new') { novas++; }
        else if ((f.nextReview || 0) <= agora) { devidas++; }
      });
    });
    return { devidas, novas };
  },

  // ── Renderiza o card de configuração no Perfil ──────────
  renderizarCard() {
    const suporta = 'Notification' in window;
    const perm    = suporta ? Notification.permission : 'unsupported';
    const hora    = this.getHora();

    if (!suporta) return '';

    const { devidas, novas } = this._contarCartas();
    const it = typeof I18n !== 'undefined' && I18n.idioma === 'it';

    const cartasTexto = devidas + novas > 0
      ? `📚 ${devidas} ${it ? 'da ripassare' : 'em revisão'} · ${novas} ${it ? 'nuove oggi' : 'novas hoje'}`
      : `✅ ${it ? 'Nessuna carta in scadenza oggi' : 'Nenhuma carta pendente hoje'}`;

    if (perm === 'granted') {
      return `<div class="notif-card">
        <div class="notif-titulo">🔔 ${it ? 'Promemoria di Studio' : 'Lembretes de Estudo'}</div>
        <div class="notif-status ativo">✅ ${it ? 'Promemoria attivi' : 'Lembretes ativados'}</div>
        <div class="notif-cartas">${cartasTexto}</div>
        <div class="notif-hora-row">
          <label class="notif-hora-label">⏰ ${it ? 'Ricordami alle:' : 'Lembrar às:'}</label>
          <input type="time" class="notif-hora-input" value="${hora}" onchange="Notificacoes.setHora(this.value)">
        </div>
      </div>`;
    }
    if (perm === 'denied') {
      return `<div class="notif-card">
        <div class="notif-titulo">🔔 ${it ? 'Promemoria di Studio' : 'Lembretes de Estudo'}</div>
        <div class="notif-status negado">🚫 ${it ? 'Permesso negato nel browser' : 'Permissão negada no browser'}</div>
        <p class="notif-dica">${it ? 'Per attivare: Impostazioni browser → Notifiche → Consenti per questo sito.' : 'Para ativar: Configurações do browser → Notificações → Permitir para este site.'}</p>
      </div>`;
    }
    return `<div class="notif-card">
      <div class="notif-titulo">🔔 ${it ? 'Promemoria di Studio' : 'Lembretes de Estudo'}</div>
      <div class="notif-status pendente">💤 ${it ? 'Promemoria disattivati' : 'Lembretes desativados'}</div>
      <p class="notif-dica">${it ? "Attiva per ricevere un promemoria giornaliero all'orario che preferisci." : 'Ative para receber um lembrete diário na hora que preferir.'}</p>
      <button class="btn-primario" onclick="Notificacoes.pedirPermissao()" style="margin-top:0.5rem;width:100%">
        🔔 ${it ? 'Attiva Promemoria' : 'Ativar Lembretes'}
      </button>
    </div>`;
  },

  // ── Init: agenda lembrete se já tinha permissão ─────────
  init() {
    if (this.habilitado()) {
      // Re-agenda todo dia ao abrir o app
      this.agendarHoje();
    }
  },
};
