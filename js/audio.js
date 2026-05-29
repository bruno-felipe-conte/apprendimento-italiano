// ============================================================
// audio.js — Programmatic sound feedback via Web Audio API
// No external files — all sounds generated in-browser
// ============================================================

const SomFeedback = {
  ativo: false,
  _ctx: null,

  init() {
    this.ativo = localStorage.getItem('it_som') === '1';
    this._atualizarBotao();
  },

  toggle() {
    this.ativo = !this.ativo;
    localStorage.setItem('it_som', this.ativo ? '1' : '0');
    this._atualizarBotao();
    App.notificar(this.ativo ? '🔔 Sons ativados' : '🔕 Sons desativados', 'alerta');
  },

  _atualizarBotao() {
    const btn = document.getElementById('btn-som');
    if (btn) btn.textContent = this.ativo ? '🔔' : '🔕';
    if (btn) btn.title = this.ativo ? 'Sons: ativados (clique para desligar)' : 'Sons: desativados (clique para ligar)';
  },

  _ctx() {
    if (!this.__ctx) {
      try {
        this.__ctx = new (window.AudioContext || window.webkitAudioContext)();
      } catch (_) { return null; }
    }
    return this.__ctx;
  },

  _tocar(freq, durMs, tipo = 'sine', vol = 0.28) {
    if (!this.ativo) return;
    const ctx = this._ctx();
    if (!ctx) return;
    try {
      const osc  = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = tipo;
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(vol, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + durMs / 1000);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + durMs / 1000);
    } catch (_) {}
  },

  // ── Correct answer: bright ascending two-tone ──────────────
  correto() {
    this._tocar(659, 70);
    setTimeout(() => this._tocar(880, 90), 65);
  },

  // ── Wrong answer: low flat buzz ───────────────────────────
  errado() {
    this._tocar(196, 130, 'sawtooth', 0.18);
  },

  // ── Level-up: ascending triad ─────────────────────────────
  nivelUp() {
    const seq = [523, 659, 784, 1046];
    seq.forEach((freq, i) => setTimeout(() => this._tocar(freq, 140), i * 110));
  },

  // ── Card flip: subtle soft click ──────────────────────────
  virar() {
    this._tocar(440, 40, 'sine', 0.1);
  },
};
