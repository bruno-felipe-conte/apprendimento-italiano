// ============================================================
// js/core/stats.js — Stats & Diagnostics (ARC-02)
// ============================================================

const AppStats = {
  // ── Header stats ───────────────────────────────────────────
  atualizarStats() {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    if (!p || typeof document === 'undefined') return;

    const elNivel   = document.getElementById('stat-nivel');
    const elXp      = document.getElementById('stat-xp');
    const elTempli  = document.getElementById('stat-templi');
    const elParole  = document.getElementById('stat-parole');
    const elBarFill = document.getElementById('xp-bar-fill');
    const elStreak  = document.getElementById('stat-streak');

    let xpInicio = 0;
    let xpFim = p.xp_proximo_nivel || 500;
    if (typeof Progressao !== 'undefined') {
      xpInicio = Progressao.xpParaNivel(p.nivel) || 0;
      xpFim    = Progressao.xpParaNivel(p.nivel + 1) || (xpInicio + 500);
    }
    const range = xpFim - xpInicio;
    const current = p.xp - xpInicio;
    const percent = range > 0 ? Math.min(100, Math.round((current / range) * 100)) : 0;

    const nivelMinimoMap = (typeof AppTemploData !== 'undefined' && AppTemploData.TEMPLO_NIVEL_MINIMO)
      ? AppTemploData.TEMPLO_NIVEL_MINIMO
      : ((typeof AppTemplos !== 'undefined' && AppTemplos.TEMPLO_NIVEL_MINIMO)
        ? AppTemplos.TEMPLO_NIVEL_MINIMO
        : ((typeof App !== 'undefined' && App.TEMPLO_NIVEL_MINIMO) ? App.TEMPLO_NIVEL_MINIMO : {}));

    const totalTemplos = Object.entries(nivelMinimoMap)
      .filter(([, lvl]) => lvl < 90).length || 50;

    if (elNivel)   elNivel.textContent   = `Livello ${p.nivel}`;
    if (elXp)      elXp.textContent      = `XP: ${p.xp}/${xpFim}`;
    if (elTempli)  elTempli.textContent  = `Templi: ${p.templos_desbloqueados.length}/${totalTemplos}`;
    if (elParole)  elParole.textContent  = `Parole: ${p.total_palavras}`;
    if (elBarFill) elBarFill.style.width = percent + '%';
    const s = p.streak || 0;
    if (elStreak && typeof I18n !== 'undefined') {
      elStreak.textContent = I18n.t(s !== 1 ? 'streak_dias' : 'streak_dia').replace('{n}', String(s));
    }

    // Atualiza badge do botão Revisão Geral com total de cartas vencidas
    const btnRgCount = document.getElementById('btn-rg-count');
    if (btnRgCount && estado) {
      const agora = Date.now();
      let vencidas = 0;
      p.templos_desbloqueados.forEach(num => {
        const data = estado.templosData[num];
        if (!data || !data.palavras) return;
        data.palavras.forEach(pw => {
          const f = estado.flashcardData[pw.id];
          if (!f || f.state === 'new' || (f.nextReview || 0) <= agora) vencidas++;
        });
      });
      btnRgCount.textContent = vencidas > 0 ? `${vencidas} carta${vencidas !== 1 ? 's' : ''}` : '';
    }

    // Daily goal bar — reset xp_hoje when the date rolls over
    const _d = new Date();
    const hoje = `${_d.getFullYear()}-${String(_d.getMonth()+1).padStart(2,'0')}-${String(_d.getDate()).padStart(2,'0')}`;
    if (p.data_xp_hoje !== hoje) {
      p.xp_hoje = 0;
      p.data_xp_hoje = hoje;
      if (typeof AppState !== 'undefined' && typeof AppState.salvarProgresso === 'function') {
        AppState.salvarProgresso();
      } else if (typeof App !== 'undefined' && typeof App.salvarProgresso === 'function') {
        App.salvarProgresso();
      }
    }
    const meta     = p.meta_diaria || 100;
    const ganhoHj  = p.xp_hoje || 0;
    const metaPct  = Math.min(100, Math.round((ganhoHj / meta) * 100));
    const elMetaFill  = document.getElementById('meta-bar-fill');
    const elMetaLabel = document.getElementById('meta-bar-label');
    const elMetaXp    = document.getElementById('meta-bar-xp');
    if (elMetaFill)  elMetaFill.style.width   = metaPct + '%';
    if (elMetaLabel && typeof I18n !== 'undefined') elMetaLabel.textContent  = I18n.t('meta_do_dia_label');
    if (elMetaXp)    elMetaXp.textContent     = `${ganhoHj}/${meta} XP${ganhoHj >= meta ? ' ✅' : ''}`;
  },

  renderizarCardContinuar() {
    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const p = estado ? estado.progresso : null;
    if (!p || !p.ultimo_estudo || typeof I18n === 'undefined') return ''; // primeiro acesso

    const diffHoras = (Date.now() - p.ultimo_estudo) / 3600000;
    const quando = diffHoras < 0.1 ? I18n.t('cc_agora_mesmo')
                 : diffHoras < 1   ? I18n.t('cc_ha_minutos')
                 : diffHoras < 24  ? I18n.t('cc_ha_horas').replace('{n}', String(Math.round(diffHoras)))
                 :                   I18n.t('cc_ha_dias').replace('{n}', String(Math.round(diffHoras/24)));

    const ultimaSecao = p.ultima_secao || 'flashcard';
    let secaoNome = 'Flashcard';
    if (ultimaSecao === 'templi')      secaoNome = I18n.t('cc_secao_inicio');
    if (ultimaSecao === 'quiz')        secaoNome = 'Quiz';
    if (ultimaSecao === 'vocabolario') secaoNome = I18n.t('cc_secao_vocab');
    if (ultimaSecao === 'grammatica')  secaoNome = I18n.t('cc_secao_gram');
    if (ultimaSecao === 'profilo')     secaoNome = I18n.t('cc_secao_perfil');

    return `<div class="card-continuar" onclick="App.navegar('${ultimaSecao}')">
      <div>
        <div class="cc-label">${I18n.t('cc_continuar_label')}</div>
        <div class="cc-info">${I18n.t('cc_ultima_sessao')} <strong>${quando}</strong> (${secaoNome})</div>
      </div>
      <div class="cc-cta">${I18n.t('cc_retomar')}</div>
    </div>`;
  },

  // ── Health Check PWA (HAR-02) ──────────────────────────────
  async abrirHealthCheck() {
    let est = { usage: 0, quota: 0 };
    if (typeof navigator !== 'undefined' && navigator.storage && navigator.storage.estimate) {
      try { est = await navigator.storage.estimate(); } catch (_) {}
    }
    const usageMB = ((est.usage || 0) / 1048576).toFixed(2);
    const quotaMB = ((est.quota || 0) / 1048576).toFixed(0);
    const pct = est.quota ? (((est.usage || 0) / est.quota) * 100).toFixed(1) : '0.0';

    let audioStats = { itens: 0, bytes: 0 };
    if (typeof AudioCache !== 'undefined' && AudioCache.estatisticas) {
      try { audioStats = await AudioCache.estatisticas(); } catch (_) {}
    }
    const audioMB = (audioStats.bytes / 1048576).toFixed(2);

    const swAtivo = (typeof navigator !== 'undefined' && 'serviceWorker' in navigator && navigator.serviceWorker.controller)
      ? '✅ Ativo (v136)'
      : '⚠️ Inativo / Standby';
    const vozNeural = (typeof VoiceEngine !== 'undefined' && VoiceEngine.statusVozNeural) ? VoiceEngine.statusVozNeural() : null;
    const erros = (typeof localStorage !== 'undefined') ? JSON.parse(localStorage.getItem('it_client_errors') || '[]') : [];

    const estado = (typeof AppState !== 'undefined' && AppState.estado)
      ? AppState.estado
      : (typeof App !== 'undefined' && App.estado ? App.estado : null);

    const totalFlashcards = Object.keys(estado?.flashcardData || {}).length;
    const totalVocab = (estado?.vocabCache || []).length;

    let modal = document.getElementById('health-check-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'health-check-modal';
      modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.65);z-index:9999;display:flex;align-items:center;justify-content:center;padding:1rem;backdrop-filter:blur(3px);';
      modal.innerHTML = `
        <div style="background:var(--cor-marmore,#FAF7F2);border:2px solid var(--cor-toscano,#C9952A);border-radius:14px;max-width:480px;width:100%;box-shadow:0 12px 36px rgba(0,0,0,0.35);overflow:hidden;font-family:inherit;">
          <div style="background:linear-gradient(135deg,#9B2335,#6B1525);color:#fff;padding:0.9rem 1.2rem;display:flex;align-items:center;justify-content:space-between;">
            <div style="font-family:'Cinzel',serif;font-weight:700;font-size:1.05rem;">🩺 Diagnóstico & Saúde PWA</div>
            <button onclick="App.fecharHealthCheck()" style="background:none;border:none;color:#fff;font-size:1.2rem;cursor:pointer;">✕</button>
          </div>
          <div id="health-check-content" style="padding:1.2rem;display:flex;flex-direction:column;gap:0.75rem;font-size:0.88rem;max-height:75vh;overflow-y:auto;">
          </div>
          <div style="padding:0.8rem 1.2rem;background:#EDE5D8;display:flex;justify-content:flex-end;">
            <button class="btn-primario" onclick="App.fecharHealthCheck()" style="padding:0.4rem 1.2rem;">Fechar</button>
          </div>
        </div>
      `;
      modal.addEventListener('click', (e) => { if (e.target === modal) this.fecharHealthCheck(); });
      document.body.appendChild(modal);
    }

    const content = document.getElementById('health-check-content');
    if (content) {
      content.innerHTML = `
        <div style="background:#fff;padding:0.7rem 0.9rem;border-radius:8px;border:1px solid rgba(0,0,0,0.08);">
          <div style="font-weight:700;color:#9B2335;margin-bottom:0.25rem;">🌐 Service Worker & Cache PWA</div>
          <div>Status: <strong>${swAtivo}</strong></div>
          <div style="font-size:0.78rem;color:#777;margin-top:0.2rem;">Cache estático, dicionários e SWR operacionais para modo 100% offline.</div>
        </div>

        <div style="background:#fff;padding:0.7rem 0.9rem;border-radius:8px;border:1px solid rgba(0,0,0,0.08);">
          <div style="font-weight:700;color:#9B2335;margin-bottom:0.25rem;">💾 Armazenamento Local & Quota</div>
          <div>Uso Total: <strong>${usageMB} MB</strong> de ${quotaMB} MB (${pct}%)</div>
          <div style="font-size:0.78rem;color:#777;margin-top:0.2rem;">${parseFloat(pct) > 80 ? '⚠️ Quota próxima do limite (>80%)' : '✅ Quota saudável (<80%)'}</div>
        </div>

        <div style="background:#fff;padding:0.7rem 0.9rem;border-radius:8px;border:1px solid rgba(0,0,0,0.08);">
          <div style="font-weight:700;color:#9B2335;margin-bottom:0.25rem;">🎧 IndexedDB (Áudio & Traduções)</div>
          <div>Áudios Cacheados: <strong>${audioStats.itens}</strong> (${audioMB} MB)</div>
          <div style="font-size:0.78rem;color:#777;margin-top:0.2rem;">Banco IndexedDB it_audio_db v2 com TTL de 7 dias para traduções.</div>
        </div>

        <div style="background:#fff;padding:0.7rem 0.9rem;border-radius:8px;border:1px solid rgba(0,0,0,0.08);">
          <div style="font-weight:700;color:#9B2335;margin-bottom:0.25rem;">🧠 Voz Neural Riccardo (WASM)</div>
          <div>Status: <strong>${vozNeural?.instalada ? '✅ Instalada localmente' : (vozNeural?.baixando ? '⏳ Baixando...' : '⚪ Não instalada (usando nativa)')}</strong></div>
          <div>Modo Neural Ativo: <strong>${vozNeural?.ativa ? 'Sim' : 'Não'}</strong></div>
        </div>

        <div style="background:#fff;padding:0.7rem 0.9rem;border-radius:8px;border:1px solid rgba(0,0,0,0.08);">
          <div style="font-weight:700;color:#9B2335;margin-bottom:0.25rem;">📚 Estado da Sessão & FSRS</div>
          <div>Cartas com Histórico FSRS: <strong>${totalFlashcards}</strong></div>
          <div>Vocabulário Total Disponível: <strong>${totalVocab}</strong></div>
          <div>Erros Capturados (Error Boundary): <strong>${erros.length}</strong></div>
        </div>
      `;
    }
    modal.style.display = 'flex';
  },

  fecharHealthCheck() {
    const modal = document.getElementById('health-check-modal');
    if (modal) modal.style.display = 'none';
  }
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppStats = AppStats;
}
if (typeof window !== 'undefined') {
  window.AppStats = AppStats;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppStats;
}
