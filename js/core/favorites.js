// ============================================================
// js/core/favorites.js — Favorites & Word of the Day (ARC-02)
// ============================================================

const AppFavorites = {
  // ── Favoritos (Optimistic UI com micro-animação e rollback) ──
  toggleFavorito(id, btnEl = null) {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    if (!p) return false;
    if (!p.favoritos) p.favoritos = [];
    const idx = p.favoritos.indexOf(id);
    const adicionado = idx === -1;

    // Optimistic UI: aplica estado e animação imediatamente
    if (adicionado) p.favoritos.push(id);
    else            p.favoritos.splice(idx, 1);

    if (btnEl && btnEl.classList) {
      btnEl.classList.remove('optimistic-pop');
      void btnEl.offsetWidth;
      btnEl.classList.add('optimistic-pop');
    }

    try {
      if (typeof AppState !== 'undefined' && typeof AppState.salvarProgresso === 'function') {
        AppState.salvarProgresso();
      } else if (typeof App !== 'undefined' && typeof App.salvarProgresso === 'function') {
        App.salvarProgresso();
      }
    } catch (err) {
      // Rollback em caso de falha crítica de persistência
      if (adicionado) p.favoritos.pop();
      else            p.favoritos.splice(idx, 0, id);

      const notifFn = (typeof AppTTS !== 'undefined' && AppTTS.notificar)
        ? AppTTS.notificar
        : (typeof App !== 'undefined' ? App.notificar : null);
      if (notifFn) notifFn('Erro ao salvar favorito', 'erro');
      return !adicionado;
    }
    return adicionado;
  },

  ehFavorito(id) {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    return !!(p && p.favoritos && p.favoritos.includes(id));
  },

  // ── Parola del Giorno ─────────────────────────────────────
  renderizarParolaDia() {
    if (typeof document === 'undefined') return;
    const container = document.getElementById('parola-del-giorno');
    if (!container) return;

    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    if (!estado) {
      container.style.display = 'none';
      return;
    }

    // Só palavras de templos desbloqueados pelo usuário
    const desbloqueados = (estado.progresso?.templos_desbloqueados) || [1];
    const vocab = [];
    desbloqueados.forEach(i => {
      const d = estado.templosData[i];
      if (d && d.palavras) d.palavras.forEach(p => vocab.push({ ...p, _templo: i }));
    });
    if (vocab.length === 0) {
      container.style.display = 'none';
      return;
    }

    // Select deterministically by day of year (same word all day)
    const now   = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const dayN  = Math.floor((now.getTime() - start.getTime()) / 86400000);

    // Check localStorage cache
    let cached = null;
    try {
      cached = JSON.parse(localStorage.getItem('it_palavra_dia') || 'null');
    } catch (_) {}
    const todayStr = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    let palavra;
    if (cached && cached.data === todayStr) {
      palavra = vocab.find(p => p.id === cached.id) || vocab[dayN % vocab.length];
    } else {
      palavra = vocab[dayN % vocab.length];
      try {
        localStorage.setItem('it_palavra_dia', JSON.stringify({ data: todayStr, id: palavra.id }));
      } catch (_) {}
    }
    if (!palavra) {
      container.style.display = 'none';
      return;
    }

    const ipa = palavra.audio_ipa
      ? (palavra.audio_ipa.startsWith('/') ? palavra.audio_ipa : `/${palavra.audio_ipa}/`)
      : '';
    const data = now.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' });

    const isFav = estado.progresso && estado.progresso.favoritos && estado.progresso.favoritos.includes(palavra.id);
    const favEmoji = isFav ? '❤️' : '🤍';

    container.innerHTML = `
      <div class="pdd-header">
        <span class="pdd-label">🇮🇹 Parola del Giorno</span>
        <span class="pdd-data">${data}</span>
      </div>
      <div class="pdd-body">
        <div class="pdd-palavra">${palavra.italiano}</div>
        ${ipa ? `<div class="pdd-ipa">${ipa}</div>` : ''}
        <div class="pdd-traducao">${palavra.portugues}</div>
        ${palavra.categoria ? `<span class="pdd-cat">${palavra.categoria}</span>` : ''}
        ${palavra.exemplo ? `<div class="pdd-exemplo">"${palavra.exemplo}"${palavra.exemplo_pt ? ` — ${palavra.exemplo_pt}` : ''}</div>` : ''}
      </div>
      <div class="pdd-acoes">
        <button class="pdd-btn" onclick="App.pronunciar('${palavra.italiano.replace(/'/g, "\\'")}')">🔊 Ascolta</button>
        <button class="pdd-btn pdd-btn-study" onclick="App.estudarPalavra('${palavra.id}',${palavra._templo})">📚 Studiare</button>
        <button class="pdd-btn" style="color: ${isFav ? '#e74c3c' : 'inherit'}" onclick="this.classList.remove('optimistic-pop'); void this.offsetWidth; this.classList.add('optimistic-pop'); App.toggleFavorito('${palavra.id}', this); const fav = (App.estado.progresso?.favoritos || []).includes('${palavra.id}'); this.innerHTML = (fav ? '❤️' : '🤍') + ' Fav'; this.style.color = fav ? '#e74c3c' : 'inherit';">
          ${favEmoji} Fav
        </button>
      </div>
    `;
    container.style.display = 'block';
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppFavorites = AppFavorites;
}
if (typeof window !== 'undefined') {
  window.AppFavorites = AppFavorites;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppFavorites;
}
