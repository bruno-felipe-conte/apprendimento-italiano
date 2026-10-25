// ============================================================
// progression.ts — XP levels, temple unlocks, mastery (ARC-03)
// ============================================================
// ── Level names by milestone ───────────────────────────────
const _LEVEL_NOMES = {
    1: 'Principiante', 2: 'Curioso', 3: 'Esploratore', 5: 'Studioso',
    7: 'Intermedio', 10: 'Avanzato', 13: 'Esperto', 16: 'Avanzato Plus',
    19: 'Maestro', 20: 'Gran Maestro'
};
function _nomePorNivel(n) {
    const keys = Object.keys(_LEVEL_NOMES).map(Number).sort((a, b) => b - a);
    for (const k of keys) {
        if (n >= k)
            return _LEVEL_NOMES[k];
    }
    return 'Principiante';
}
// ── Level-Up modal ─────────────────────────────────────────
export const LevelUp = {
    mostrar(nivel) {
        if (typeof document === 'undefined')
            return;
        const modal = document.getElementById('levelup-modal');
        if (!modal)
            return;
        const el = (id) => document.getElementById(id);
        const numEl = el('levelup-num');
        const nomeEl = el('levelup-nome');
        if (numEl)
            numEl.textContent = String(nivel);
        if (nomeEl)
            nomeEl.textContent = _nomePorNivel(nivel);
        // Desbloqueios relacionados
        const templos = Object.entries(Progressao.TEMPLO_NIVEL)
            .filter(([, n]) => n === nivel)
            .map(([t]) => `🏛️ Tempio ${t} desbloqueado!`);
        const desblEl = el('levelup-desbloqueios');
        if (desblEl) {
            desblEl.textContent = templos.join(' · ') || '';
        }
        this._gerarConfetti();
        modal.classList.add('ativo');
    },
    fechar() {
        if (typeof document === 'undefined')
            return;
        const modal = document.getElementById('levelup-modal');
        if (modal)
            modal.classList.remove('ativo');
        const card = document.getElementById('levelup-card');
        if (card)
            card.querySelectorAll('.levelup-confetti').forEach(c => c.remove());
    },
    _gerarConfetti() {
        if (typeof document === 'undefined')
            return;
        const card = document.getElementById('levelup-card');
        if (!card)
            return;
        const cores = ['#D4A843', '#9B2335', '#27AE60', '#2980B9', '#F5C842', '#fff'];
        for (let i = 0; i < 30; i++) {
            const p = document.createElement('div');
            p.className = 'levelup-confetti';
            p.style.left = Math.random() * 100 + '%';
            p.style.top = '-10px';
            p.style.background = cores[Math.floor(Math.random() * cores.length)];
            p.style.width = (6 + Math.random() * 6) + 'px';
            p.style.height = (6 + Math.random() * 6) + 'px';
            p.style.animationDuration = (0.8 + Math.random() * 1.4) + 's';
            p.style.animationDelay = (Math.random() * 0.5) + 's';
            card.appendChild(p);
        }
    }
};
export const Progressao = {
    // Cumulative XP required to reach each level index
    // Index 0 = start of level 1 (0 XP), index 1 = start of level 2 (500 XP), etc.
    NIVEL_XP: [
        0, // L1
        300, // L2 — primeiro marco, alcançável em 1-2 dias
        700, // L3
        1200, // L4
        1900, // L5
        2700, // L6
        3700, // L7
        5000, // L8
        6500, // L9
        8500, // L10 — T4 desbloqueado
        11000, // L11
        13500, // L12
        17000, // L13 — T7 desbloqueado
        21000, // L14
        25000, // L15 — T8 desbloqueado
        30000, // L16
        36000, // L17 — T9 desbloqueado
        43000, // L18
        51000, // L19
        60000, // L20 — T10 desbloqueado (maestro!)
        70000, // L21
        82000, // L22
    ],
    // Nível mínimo para desbloquear cada templo (inclui templos 11-50)
    TEMPLO_NIVEL: {
        1: 1, 2: 2, 3: 4, 4: 6, 5: 8, 6: 10, 7: 13, 8: 15, 9: 17, 10: 20,
        36: 99, // T36 desativado
        // A2
        11: 2, 12: 2, 13: 2, 14: 2, 15: 2, 17: 2, 18: 2, 19: 2,
        22: 2, 23: 2, 25: 2, 28: 2, 33: 2, 34: 2,
        // B1
        16: 4, 20: 4, 21: 4, 24: 4, 29: 4, 32: 4, 35: 4, 51: 4,
        // B2
        26: 7, 27: 7, 30: 7, 31: 7, 37: 7, 38: 7, 43: 7, 46: 7,
        // C1
        39: 11, 40: 11, 42: 11, 44: 11, 45: 11,
        // C2
        41: 15, 47: 15, 48: 15, 49: 15, 50: 15,
    },
    // ── XP threshold for level N (1-based) ────────────────────
    xpParaNivel(n) {
        if (n <= 1)
            return 0;
        const idx = n - 1;
        if (idx < this.NIVEL_XP.length)
            return this.NIVEL_XP[idx];
        return this.NIVEL_XP[this.NIVEL_XP.length - 1] + (n - this.NIVEL_XP.length) * 5000;
    },
    // ── Gain XP and trigger cascading checks ──────────────────
    ganhar(quantidade) {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return;
        // Track daily XP (reset if new day)
        const _d = new Date();
        const hoje = `${_d.getFullYear()}-${String(_d.getMonth() + 1).padStart(2, '0')}-${String(_d.getDate()).padStart(2, '0')}`;
        if (p.data_xp_hoje !== hoje) {
            p.xp_hoje = 0;
            p.data_xp_hoje = hoje;
        }
        const xpAntes = p.xp_hoje || 0;
        p.xp_hoje = xpAntes + quantidade;
        // Fire "meta reached" toast exactly once per day
        const meta = p.meta_diaria || 100;
        if (xpAntes < meta && p.xp_hoje >= meta) {
            setTimeout(() => app?.notificar?.('notif_meta_atingida', 'sucesso'), 400);
        }
        p.xp += quantidade;
        p.ultimo_estudo = Date.now();
        if (typeof window !== 'undefined' && window.Calor) {
            window.Calor.registrar(0, quantidade);
        }
        const nivelAnterior = p.nivel;
        this.verificarNivelUp();
        const subiu = p.nivel > nivelAnterior;
        if (subiu) {
            this.verificarDesbloqueioTemplos();
            LevelUp.mostrar(p.nivel);
            if (typeof window !== 'undefined') {
                window.SomFeedback?.nivelUp?.();
                window.Conquistas?.verificar?.();
            }
        }
        app?.salvarProgresso?.();
        app?.atualizarStats?.();
    },
    // ── Level-up check ─────────────────────────────────────────
    verificarNivelUp() {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return;
        let guard = 0;
        while (guard++ < 100) {
            const xpProximo = this.xpParaNivel(p.nivel + 1);
            if (p.xp >= xpProximo) {
                p.nivel++;
                p.xp_proximo_nivel = this.xpParaNivel(p.nivel + 1);
            }
            else {
                break;
            }
        }
    },
    // ── Temple unlock check ────────────────────────────────────
    verificarDesbloqueioTemplos() {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return;
        let novoDesbloqueio = false;
        for (const [temploNum, nivelNecessario] of Object.entries(this.TEMPLO_NIVEL)) {
            const num = parseInt(temploNum, 10);
            if (!p.templos_desbloqueados)
                p.templos_desbloqueados = [1];
            if (p.nivel >= nivelNecessario && !p.templos_desbloqueados.includes(num)) {
                p.templos_desbloqueados.push(num);
                p.templos_desbloqueados.sort((a, b) => a - b);
                novoDesbloqueio = true;
                const msg = (typeof window !== 'undefined' && window.I18n)
                    ? window.I18n.t('notif_templo_sbloccato').replace('{n}', String(num))
                    : `Tempio ${num} sbloccato!`;
                app?.notificar?.(msg, 'sucesso');
            }
        }
        if (novoDesbloqueio) {
            app?.salvarProgresso?.();
            app?.renderizarTemplos?.();
            if (typeof window !== 'undefined') {
                window.Quiz?.renderizarSeletor?.();
                window.Flashcards?.atualizarSelectTemplo?.();
                window.Vocab?.popularCategorias?.();
            }
        }
    },
    percentualNivel() {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return 0;
        const inicio = this.xpParaNivel(p.nivel);
        const fim = this.xpParaNivel(p.nivel + 1);
        const range = fim - inicio;
        if (range <= 0)
            return 100;
        return Math.min(100, Math.round(((p.xp - inicio) / range) * 100));
    },
    temploDesbloqueado(n) {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return false;
        return p.templos_desbloqueados.includes(n);
    },
    palavrasDominadas(temploNum) {
        const app = typeof window !== 'undefined' ? window.App : null;
        const data = app?.estado?.templosData?.[temploNum];
        if (!data || !data.palavras)
            return 0;
        const flashData = app?.estado?.flashcardData || {};
        return data.palavras.filter((p) => {
            const sm = flashData[p.id];
            if (!sm)
                return false;
            return (sm.reps >= 3) || (sm.repeticoes >= 3) || (sm.stability > 7);
        }).length;
    },
    temploConcluido(temploNum) {
        const app = typeof window !== 'undefined' ? window.App : null;
        const data = app?.estado?.templosData?.[temploNum];
        if (!data || !data.palavras || data.palavras.length === 0)
            return false;
        const dominadas = this.palavrasDominadas(temploNum);
        return dominadas >= data.palavras.length;
    },
    marcarTemploConcluido(temploNum) {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return;
        if (!p.templos_concluidos.includes(temploNum)) {
            p.templos_concluidos.push(temploNum);
            app?.salvarProgresso?.();
            const msg = (typeof window !== 'undefined' && window.I18n)
                ? window.I18n.t('notif_templo_completato').replace('{n}', String(temploNum))
                : `Tempio ${temploNum} completato!`;
            app?.notificar?.(msg, 'sucesso');
            app?.renderizarTemplos?.();
        }
    },
    calcularMetaPrazo() {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p || !p.meta_prazo)
            return null;
        const meta = p.meta_prazo;
        const hoje = Date.now();
        const dataAlvo = new Date(meta.data_alvo).getTime();
        const diasRestantes = Math.ceil((dataAlvo - hoje) / 86400000);
        const XP_POR_NIVEL = [0, 500, 1200, 2100, 3200, 4500, 6000, 7700, 9600, 11700, 14000, 16500, 19200, 22100, 25200, 28500, 32000, 35700, 39600, 43700, 48000];
        const xpAlvo = XP_POR_NIVEL[meta.nivel_alvo] || 48000;
        const xpFaltante = Math.max(0, xpAlvo - p.xp);
        const xpPorDia = diasRestantes > 0 ? Math.ceil(xpFaltante / diasRestantes) : xpFaltante;
        const diario = (typeof localStorage !== 'undefined') ? JSON.parse(localStorage.getItem('it_diario') || '{}') : {};
        const hoje7 = new Date();
        let xpSemana = 0;
        for (let i = 0; i < 7; i++) {
            const d = new Date(hoje7);
            d.setDate(d.getDate() - i);
            const k = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
            const entry = diario[k];
            if (entry)
                xpSemana += (typeof entry === 'object' ? entry.xp : 0);
        }
        const xpMedioDia = Math.round(xpSemana / 7);
        const diasNecessarios = xpMedioDia > 0 ? Math.ceil(xpFaltante / xpMedioDia) : 9999;
        const dataPrevisao = new Date(hoje + diasNecessarios * 86400000).toLocaleDateString('pt-BR');
        const atingeNoPrazo = diasNecessarios <= diasRestantes;
        return {
            diasRestantes,
            xpFaltante,
            xpPorDia,
            xpMedioDia,
            dataPrevisao,
            atingeNoPrazo,
            nivel_alvo: meta.nivel_alvo,
            data_alvo: meta.data_alvo
        };
    },
    definirMetaPrazo(nivelAlvo, dataAlvo) {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return;
        p.meta_prazo = {
            nivel_alvo: nivelAlvo,
            data_alvo: dataAlvo,
            xp_na_criacao: p.xp,
            criado_em: Date.now()
        };
        app?.salvarProgresso?.();
        app?.notificar?.('notif_meta_def_ok', 'sucesso');
    },
    removerMetaPrazo() {
        const app = typeof window !== 'undefined' ? window.App : null;
        const p = app?.estado?.progresso;
        if (!p)
            return;
        p.meta_prazo = null;
        app?.salvarProgresso?.();
    }
};
// Global facade bindings
if (typeof window !== 'undefined') {
    window.Progressao = Progressao;
    window.LevelUp = LevelUp;
}
if (typeof globalThis !== 'undefined') {
    globalThis.Progressao = Progressao;
    globalThis.LevelUp = LevelUp;
}
export default Progressao;
