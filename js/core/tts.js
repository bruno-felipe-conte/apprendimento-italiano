// ============================================================
// js/core/tts.js — Text-to-Speech & Toast Notifications (ARC-02)
// ============================================================

const AppTTS = {
  // ── Toast notifications ────────────────────────────────────
  notificar(mensagem, tipo = 'info') {
    if (typeof document === 'undefined') return;
    const container = document.getElementById('toast-container');
    if (!container) return;

    if (typeof I18n !== 'undefined' && I18n.dict && I18n.dict[mensagem]) {
      mensagem = I18n.t(mensagem);
    }

    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    toast.textContent = mensagem;
    container.appendChild(toast);

    // Auto-dismiss after 3 seconds
    setTimeout(() => {
      toast.classList.add('saindo');
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 320);
    }, 3000);
  },

  // ── Audio Speed controls ──────────────────────────────────
  toggleAudioSpeed() {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    if (!p) return;
    if (p.audio_rate === 1) p.audio_rate = 0.85;
    else if (p.audio_rate === 0.85) p.audio_rate = 0.7;
    else if (p.audio_rate === 0.7) p.audio_rate = 0.5;
    else p.audio_rate = 1;

    if (typeof AppState !== 'undefined' && typeof AppState.salvarProgresso === 'function') {
      AppState.salvarProgresso();
    } else if (typeof App !== 'undefined' && typeof App.salvarProgresso === 'function') {
      App.salvarProgresso();
    }

    this.atualizarAudioSpeedUI();
    const desc = (typeof I18n !== 'undefined' && I18n.idioma === 'it') ? 'Velocità audio: ' : 'Velocidade: ';
    this.notificar(desc + p.audio_rate + 'x', 'info');
  },

  atualizarAudioSpeedUI() {
    if (typeof document === 'undefined') return;
    const btn = document.getElementById('btn-audio-speed');
    if (!btn) return;
    const ico = document.getElementById('btn-audio-speed-ico') || btn;

    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const rate = (estado && estado.progresso && estado.progresso.audio_rate)
      ? estado.progresso.audio_rate
      : 0.85;

    let label = rate.toString();
    if (label.startsWith('0.')) label = label.substring(1);
    ico.textContent = label + 'x';
  },

  _vozItaliana: null,           // cache da voz italiana (null = ainda não resolvido)
  _vozItalianaResolvida: false,  // true quando já procuramos (mesmo se não achou)

  _getVozItaliana() {
    if (typeof VoiceEngine !== 'undefined' && VoiceEngine.obterVozSelecionada) {
      const voz = VoiceEngine.obterVozSelecionada();
      if (voz) return voz;
    }
    // Fallback nativo resiliente se VoiceEngine ainda não estiver pronto
    if (!this._vozItalianaResolvida && typeof speechSynthesis !== 'undefined') {
      const vozes = speechSynthesis.getVoices();
      if (!vozes.length) return null;
      this._vozItaliana =
        vozes.find(v => v.lang === 'it-IT' && (v.name.includes('Natural') || v.name.includes('Online'))) ||
        vozes.find(v => v.lang === 'it-IT') ||
        vozes.find(v => v.lang.startsWith('it')) ||
        null;
      this._vozItalianaResolvida = true;
    }
    return this._vozItaliana;
  },

  pronunciar(texto, taxaCustom = null) {
    if (!texto) return;

    // Normalização fonética e de prosódia inspirada no VoiceStudio
    const textoParaFalar = (typeof VoiceEngine !== 'undefined')
      ? VoiceEngine.normalizarParaFala(texto)
      : texto;

    if (!textoParaFalar) return;

    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    // Se o VoiceEngine estiver disponível, delega para sua síntese com prosódia e cache neural
    if (typeof VoiceEngine !== 'undefined' && typeof VoiceEngine.falarNeural === 'function') {
      let rate = taxaCustom;
      if (rate == null) {
        const speedStr = (typeof localStorage !== 'undefined') ? localStorage.getItem('it_audio_speed') : null;
        rate = speedStr ? parseFloat(speedStr) : NaN;
        if (isNaN(rate)) {
          rate = (estado && estado.progresso && estado.progresso.audio_rate) ? estado.progresso.audio_rate : 0.88;
        }
      }
      VoiceEngine.falarNeural(textoParaFalar, { rate });
      return;
    }

    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;

    const tentarFalar = () => {
      try {
        if (speechSynthesis.paused) {
          speechSynthesis.resume();
        }
        speechSynthesis.cancel();
      } catch (_) {}

      const voz = this._getVozItaliana();

      let rate = taxaCustom;
      if (rate == null) {
        const speedStr = (typeof localStorage !== 'undefined') ? localStorage.getItem('it_audio_speed') : null;
        rate = speedStr ? parseFloat(speedStr) : NaN;
        if (isNaN(rate)) {
          rate = (estado && estado.progresso && estado.progresso.audio_rate) ? estado.progresso.audio_rate : 0.85;
        }
      }
      rate = Math.max(0.1, Math.min(2.0, rate));

      const u = new SpeechSynthesisUtterance(textoParaFalar);
      u.lang  = (voz && voz.lang) ? voz.lang : 'it-IT';
      u.rate  = rate;

      if (textoParaFalar.endsWith('?')) {
        u.pitch = 1.05;
      } else if (textoParaFalar.endsWith('!')) {
        u.pitch = 1.02;
      } else {
        u.pitch = 1.0;
      }

      if (voz) u.voice = voz;

      // Fix Crítico do Chromium: Manter referência global do Utterance para não ser coletado pelo GC antes de falar
      window._activeUtterance = u;

      u.onend = () => {
        if (window._activeUtterance === u) {
          window._activeUtterance = null;
        }
      };

      u.onerror = () => {
        if (window._activeUtterance === u) {
          window._activeUtterance = null;
        }
      };

      try {
        speechSynthesis.speak(u);
      } catch (_) {}
    };

    if (speechSynthesis.getVoices().length > 0 || (typeof VoiceEngine !== 'undefined' && VoiceEngine._cacheVozes?.length)) {
      tentarFalar();
    } else {
      let chamado = false;
      const callback = () => {
        if (chamado) return;
        chamado = true;
        this._vozItalianaResolvida = false;
        tentarFalar();
      };

      speechSynthesis.onvoiceschanged = () => {
        speechSynthesis.onvoiceschanged = null;
        callback();
      };
      setTimeout(callback, 180);
    }
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppTTS = AppTTS;
}
if (typeof window !== 'undefined') {
  window.AppTTS = AppTTS;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppTTS;
}
