// ============================================================
// js/voice_engine.ts — Motor Leve de Pronúncia e Prosódia Italiana (ARC-03)
// ============================================================
export const VoiceEngine = {
    // ── 1. Preservação de Honoríficos e Abreviaturas Italianas ──
    HONORIFICS_IT: [
        'Sig', 'Sig.ra', 'Sig.na', 'Sgr', 'Dott', 'Dott.ssa',
        'Prof', 'Prof.ssa', 'Avv', 'Ing', 'Geom', 'Rag',
        'Arch', 'On', 'Egr', 'Spett', 'Gent', 'Ill'
    ],
    // ── 2. Léxico de Acentuação Tônica e Fonética Italiana ────
    LEXICO_FONETICO_IT: {
        'subito': 'sùbito',
        'Subito': 'Sùbito',
        'abito': 'àbito',
        'Abito': 'Àbito',
        'capitano': 'càpitano',
        'telefono': 'telèfono',
        'telefonano': 'telèfonano',
        'abitano': 'àbitano',
        'parlano': 'pàrlano',
        'prendono': 'prèndono',
        'scrivono': 'scrìvono',
        'leggono': 'lèggono',
        'aprono': 'àprono',
        'chiudono': 'chiùdono',
        'vivono': 'vìvono',
        'credono': 'crèdono',
        'chiedono': 'chièdono',
        'rispondono': 'rispòndono',
        'sentono': 'sèntono',
        'dormono': 'dòrmono',
        'partono': 'pàrtono',
        'mettono': 'mèttono',
        'lasciano': 'làsciano',
        'perdono': 'pèrdono',
        'vendono': 'vèndono',
        'rompono': 'ròmpono',
        'dicono': 'dìcono',
        'bevono': 'bèvono',
        'rimangono': 'rimàngono',
        'muoiono': 'muòiono',
        'tengono': 'tèngono',
        'vengono': 'vèngono',
        'vanno': 'vànno',
        'danno': 'dànno',
        'fanno': 'fànno',
        'stanno': 'stànno',
        'anno': 'ànno',
        'principi': 'prìncipi',
        'facilmente': 'fàcilmente',
        'difficilmente': 'diffìcilmente',
        'semplicemente': 'semplìcemente',
        'rapidamente': 'rapìdamente',
        'indicano': 'ìndicano',
        'valutano': 'vàlutano',
        'meritano': 'mèritano',
        'desiderano': 'desìderano',
        'occupano': 'òccupano',
        'ordinano': 'òrdinano',
        'dimenticano': 'dimènticano',
        'interessano': 'interèssano',
        'organizzano': 'orgànizzano'
    },
    // ── 3. Normalização de Texto para Áudio ────────────────────
    normalizarParaFala(texto) {
        if (!texto || typeof texto !== 'string')
            return '';
        let s = texto;
        s = s.replace(/<[^>]*>/g, ' ');
        s = s.replace(/\s*\([a-zà-úA-ZÀ-Ú\s,;.\-–—\/?!0-9]+\)/gi, (match) => {
            const ptClues = /\b(o|a|os|as|um|uma|de|do|da|em|no|na|para|com|por|que|se|ex|exemplo|verbo|lit|literalmente|trad|tradução)\b/i;
            if (ptClues.test(match))
                return '';
            return '';
        });
        s = s.replace(/\s*\[[^\]]+\]/g, '');
        s = s.replace(/(\w+)\s*\/\s*(\w+)/g, '$1, $2');
        s = s.replace(/[→↔⇒➔➜]/g, ', ');
        s = s.replace(/[🔵🔴🟢🟡🟣⚪⚫★☆✔✓✗✘💡🔍📖✏️🎧👁️]/g, '');
        s = s.replace(/[’‘`´]/g, "'");
        s = s.replace(/\b([ldcnsmgt]|un|quest|sant|pover)'\s+([aeiouhàèéìòóù])/gi, "$1'$2");
        s = s.replace(/\s+([,.;:!?])/g, '$1');
        s = s.replace(/[,;]{2,}/g, ',');
        s = s.replace(/\.{2,}/g, '...');
        s = s.replace(/\s+/g, ' ').trim();
        return this.aplicarLexicoFonico(s);
    },
    _lexicoCompilado: null,
    _obterLexicoCompilado() {
        if (!this._lexicoCompilado) {
            this._lexicoCompilado = Object.entries(this.LEXICO_FONETICO_IT).map(([termo, substituicao]) => ({
                regex: new RegExp(`(?<=[^a-zA-ZÀ-ÿ]|^)${termo}(?=[^a-zA-ZÀ-ÿ]|$)`, 'g'),
                substituicao
            }));
        }
        return this._lexicoCompilado;
    },
    // ── 4. Aplicação do Léxico Fonético ───────────────────────
    aplicarLexicoFonico(texto) {
        if (!texto)
            return '';
        const lista = this._obterLexicoCompilado();
        let out = texto;
        for (let i = 0; i < lista.length; i++) {
            out = out.replace(lista[i].regex, lista[i].substituicao);
        }
        return out;
    },
    // ── 5. Quebra de Frases / Chunker com Pausas Naturais ────
    dividirEmSentencas(texto) {
        if (!texto)
            return [];
        const t = this.normalizarParaFala(texto);
        if (!t)
            return [];
        let protegido = t;
        const placeholders = [];
        this.HONORIFICS_IT.forEach((abrev, idx) => {
            const re = new RegExp(`\\b${abrev}\\.`, 'gi');
            protegido = protegido.replace(re, (m) => {
                const ph = `__HON_${idx}__`;
                placeholders.push({ ph, original: m });
                return ph;
            });
        });
        const chunks = protegido
            .split(/(?<=[.!?])\s+|(?<=[;:])\s+/)
            .map(c => c.trim())
            .filter(Boolean);
        return chunks.map(chunk => {
            let res = chunk;
            placeholders.forEach(({ ph, original }) => {
                res = res.replace(new RegExp(ph, 'g'), original);
            });
            return res;
        });
    },
    // ── 6. Seletor e Ranking de Vozes Neurais ──────────────────
    _cacheVozes: null,
    obterMelhoresVozesItalianas() {
        if (typeof speechSynthesis === 'undefined')
            return [];
        let todas = [];
        try {
            todas = speechSynthesis.getVoices() || [];
        }
        catch (_) {
            todas = [];
        }
        if (todas.length > 0) {
            this._cacheVozes = todas;
        }
        else if (this._cacheVozes && this._cacheVozes.length > 0) {
            todas = this._cacheVozes;
        }
        const italianas = todas.filter(v => {
            const l = (v.lang || '').toLowerCase().replace(/_/g, '-');
            const n = (v.name || '').toLowerCase();
            return l === 'it-it' || l.startsWith('it-') || l === 'it' || n.includes('italian') || n.includes('italiano');
        });
        if (!italianas.length)
            return [];
        const pontuarVoz = (v) => {
            let score = 0;
            const nome = (v.name || '').toLowerCase();
            const lang = (v.lang || '').toLowerCase().replace(/_/g, '-');
            if (nome.includes('natural') || nome.includes('online'))
                score += 100;
            if (nome.includes('neural'))
                score += 90;
            if (nome.includes('premium') || nome.includes('enhanced'))
                score += 80;
            if (nome.includes('google'))
                score += 70;
            if (nome.includes('isabella'))
                score += 35;
            if (nome.includes('diego'))
                score += 35;
            if (nome.includes('elsa'))
                score += 30;
            if (nome.includes('federica'))
                score += 30;
            if (nome.includes('alice'))
                score += 25;
            if (nome.includes('luca'))
                score += 25;
            if (lang === 'it-it')
                score += 15;
            if (nome.includes('desktop') || nome.includes('sapi'))
                score -= 50;
            return score;
        };
        return [...italianas].sort((a, b) => pontuarVoz(b) - pontuarVoz(a));
    },
    obterVozSelecionada() {
        const ordenadas = this.obterMelhoresVozesItalianas();
        if (!ordenadas.length)
            return null;
        const salva = (typeof localStorage !== 'undefined') ? localStorage.getItem('it_voz_preferida') : null;
        if (salva) {
            const encontrada = ordenadas.find(v => v.name === salva || v.voiceURI === salva);
            if (encontrada)
                return encontrada;
        }
        return ordenadas[0];
    },
    // ── 7. Cadeia de Áudio Web Audio DSP (Mastering / Clareza) ──
    _audioCtx: null,
    _masterNode: null,
    obterAudioContext() {
        if (!this._audioCtx && typeof window !== 'undefined') {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (AudioCtx)
                this._audioCtx = new AudioCtx();
        }
        if (this._audioCtx && this._audioCtx.state === 'suspended') {
            this._audioCtx.resume().catch(() => { });
        }
        return this._audioCtx;
    },
    suspenderAudioContext() {
        if (this._audioCtx && this._audioCtx.state === 'running') {
            this._audioCtx.suspend().catch(() => { });
        }
    },
    fecharAudioContext() {
        if (this._audioCtx && this._audioCtx.state !== 'closed') {
            this._audioCtx.close().catch(() => { });
            this._audioCtx = null;
        }
    },
    destruirWorker() {
        if (this._worker) {
            try {
                this._worker.terminate();
            }
            catch (_) { }
            this._worker = null;
            this._workerInitialized = false;
            this._workerDownloading = false;
        }
    },
    destruir() {
        this.parar();
        this.fecharAudioContext();
        this.destruirWorker();
    },
    aplicarMasteringAudioElement(audioEl) {
        if (!audioEl || audioEl._vsMastered)
            return;
        try {
            const ctx = this.obterAudioContext();
            if (!ctx)
                return;
            const source = ctx.createMediaElementSource(audioEl);
            const highpass = ctx.createBiquadFilter();
            highpass.type = 'highpass';
            highpass.frequency.setValueAtTime(80, ctx.currentTime);
            const presence = ctx.createBiquadFilter();
            presence.type = 'peaking';
            presence.frequency.setValueAtTime(3000, ctx.currentTime);
            presence.Q.setValueAtTime(1.0, ctx.currentTime);
            presence.gain.setValueAtTime(2.0, ctx.currentTime);
            const comp = ctx.createDynamicsCompressor();
            comp.threshold.setValueAtTime(-15, ctx.currentTime);
            comp.knee.setValueAtTime(10, ctx.currentTime);
            comp.ratio.setValueAtTime(1.8, ctx.currentTime);
            comp.attack.setValueAtTime(0.002, ctx.currentTime);
            comp.release.setValueAtTime(0.100, ctx.currentTime);
            source.connect(highpass);
            highpass.connect(presence);
            presence.connect(comp);
            comp.connect(ctx.destination);
            audioEl._vsMastered = true;
        }
        catch (_) { }
    },
    // ── 8. Motor Neural WebAssembly & Cache IndexedDB ──────────
    _worker: null,
    _pendingSyntheses: new Map(),
    _currentAudioSource: null,
    _workerInitialized: false,
    _workerDownloading: false,
    _realNeuralInferenceAvailable: false,
    _onDownloadProgress: null,
    _onDownloadSuccess: null,
    _onDownloadError: null,
    _getWorker() {
        if (this._worker)
            return this._worker;
        if (typeof Worker === 'undefined')
            return null;
        try {
            this._worker = new Worker('js/tts_worker.js');
            this._worker.onmessage = (e) => this._onWorkerMessage(e);
            this._worker.onerror = (err) => {
                console.warn('[VoiceEngine] Erro no TTS Web Worker:', err);
            };
            this._worker.postMessage({ type: 'CHECK_STATUS' });
            return this._worker;
        }
        catch (e) {
            console.warn('[VoiceEngine] Web Worker não suportado ou bloqueado:', e);
            return null;
        }
    },
    _onWorkerMessage(e) {
        const { type, id, error, wavBuffer, isInitialized, percent } = e.data || {};
        if (type === 'STATUS') {
            this._workerInitialized = !!isInitialized;
        }
        else if (type === 'DOWNLOAD_PROGRESS') {
            if (typeof this._onDownloadProgress === 'function' && typeof percent === 'number') {
                this._onDownloadProgress(percent);
            }
        }
        else if (type === 'INIT_SUCCESS') {
            this._workerInitialized = true;
            this._workerDownloading = false;
            if (typeof localStorage !== 'undefined') {
                localStorage.setItem('it_voz_neural_instalada', 'true');
            }
            if (typeof this._onDownloadSuccess === 'function') {
                this._onDownloadSuccess();
            }
        }
        else if (type === 'INIT_ERROR') {
            this._workerDownloading = false;
            if (typeof this._onDownloadError === 'function') {
                this._onDownloadError(error);
            }
        }
        else if (type === 'SYNTHESIZE_SUCCESS' && id && wavBuffer) {
            const resolver = this._pendingSyntheses.get(id);
            if (resolver) {
                this._pendingSyntheses.delete(id);
                resolver.resolve(wavBuffer);
            }
        }
        else if (type === 'SYNTHESIZE_ERROR' && id) {
            const resolver = this._pendingSyntheses.get(id);
            if (resolver) {
                this._pendingSyntheses.delete(id);
                resolver.reject(new Error(error || 'Erro na síntese neural'));
            }
        }
    },
    statusVozNeural() {
        const salva = (typeof localStorage !== 'undefined') ? localStorage.getItem('it_voz_neural_instalada') === 'true' : false;
        const ativa = (typeof localStorage !== 'undefined') ? localStorage.getItem('it_usar_voz_neural') !== 'false' : true;
        return {
            instalada: salva || this._workerInitialized,
            baixando: this._workerDownloading,
            ativa
        };
    },
    baixarVozNeural(onProgress, onSuccess, onError, forceRefresh = false) {
        const worker = this._getWorker();
        if (!worker) {
            if (onError)
                onError('Web Worker não suportado');
            return;
        }
        this._workerDownloading = true;
        this._onDownloadProgress = onProgress || null;
        this._onDownloadSuccess = onSuccess || null;
        this._onDownloadError = onError || null;
        worker.postMessage({
            type: 'INIT_VOICE',
            payload: { id: 'it_IT-riccardo-x_low', forceRefresh: !!forceRefresh }
        });
    },
    async desinstalarVozNeural() {
        try {
            if (typeof caches !== 'undefined') {
                await caches.delete('it-voice-cache-v1');
            }
        }
        catch (_) { }
        if (typeof localStorage !== 'undefined') {
            localStorage.removeItem('it_voz_neural_instalada');
            if (localStorage.getItem('it_voz_preferida') === 'wasm_neural') {
                localStorage.removeItem('it_voz_preferida');
            }
        }
        this._workerInitialized = false;
        this._workerDownloading = false;
        if (this._worker) {
            try {
                this._worker.terminate();
            }
            catch (_) { }
            this._worker = null;
        }
        return true;
    },
    parar() {
        if (typeof window !== 'undefined') {
            window._activeVoiceUtterance = null;
        }
        if (typeof speechSynthesis !== 'undefined') {
            try {
                speechSynthesis.cancel();
            }
            catch (_) { }
        }
        if (this._currentAudioSource) {
            try {
                this._currentAudioSource.stop();
                this._currentAudioSource.disconnect();
            }
            catch (_) { }
            this._currentAudioSource = null;
        }
    },
    async _tocarBuffer(wavBuffer, opcoes = {}) {
        this.parar();
        const ctx = this.obterAudioContext();
        if (!ctx)
            return false;
        try {
            const audioBuffer = await ctx.decodeAudioData(wavBuffer.slice(0));
            const source = ctx.createBufferSource();
            source.buffer = audioBuffer;
            let rate = opcoes.rate;
            if (rate == null && typeof localStorage !== 'undefined') {
                const speedStr = localStorage.getItem('it_audio_speed');
                if (speedStr)
                    rate = parseFloat(speedStr);
            }
            if (rate != null && !isNaN(rate) && rate > 0) {
                source.playbackRate.value = Math.max(0.5, Math.min(2.0, rate));
            }
            source.connect(ctx.destination);
            this._currentAudioSource = source;
            source.onended = () => {
                if (this._currentAudioSource === source) {
                    this._currentAudioSource = null;
                }
                if (opcoes.onend)
                    opcoes.onend();
            };
            source.start();
            return true;
        }
        catch (err) {
            console.warn('[VoiceEngine] Falha ao decodificar/tocar buffer:', err);
            if (opcoes.onerror)
                opcoes.onerror(err);
            return false;
        }
    },
    async falarNeural(texto, opcoes = {}) {
        if (!texto)
            return false;
        const textoNorm = this.normalizarParaFala(texto);
        if (!textoNorm)
            return false;
        this.parar();
        if (typeof window !== 'undefined' && window.AudioCache) {
            try {
                const blobCache = await window.AudioCache.obter(textoNorm, 'neural_it');
                if (blobCache && blobCache.size > 4096) {
                    const buffer = await blobCache.arrayBuffer();
                    if (buffer.byteLength > 4096) {
                        return await this._tocarBuffer(buffer, opcoes);
                    }
                }
            }
            catch (_) { }
        }
        const st = this.statusVozNeural();
        const worker = this._getWorker();
        if (st.ativa && worker && this._workerInitialized && this._realNeuralInferenceAvailable) {
            try {
                const reqId = 'req_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7);
                const pBuffer = new Promise((resolve, reject) => {
                    this._pendingSyntheses.set(reqId, { resolve, reject });
                    setTimeout(() => {
                        if (this._pendingSyntheses.has(reqId)) {
                            this._pendingSyntheses.delete(reqId);
                            reject(new Error('Timeout na síntese neural'));
                        }
                    }, 8000);
                });
                worker.postMessage({
                    type: 'SYNTHESIZE',
                    payload: {
                        id: reqId,
                        text: textoNorm,
                        rate: opcoes.rate || 1.0,
                        pitch: opcoes.pitch || 1.0
                    }
                });
                const wavBuffer = await pBuffer;
                if (wavBuffer && wavBuffer.byteLength > 4096) {
                    if (typeof window !== 'undefined' && window.AudioCache) {
                        window.AudioCache.salvar(textoNorm, wavBuffer, 'neural_it').catch(() => { });
                    }
                    return await this._tocarBuffer(wavBuffer, opcoes);
                }
            }
            catch (_) { }
        }
        return this.falar(textoNorm, opcoes);
    },
    falar(texto, opcoes = {}) {
        if (!texto)
            return false;
        const textoNormalizado = this.normalizarParaFala(texto);
        if (!textoNormalizado)
            return false;
        if (typeof speechSynthesis === 'undefined') {
            return false;
        }
        try {
            if (speechSynthesis.paused) {
                try {
                    speechSynthesis.resume();
                }
                catch (_) { }
            }
            this.parar();
            const voz = this.obterVozSelecionada();
            const u = new SpeechSynthesisUtterance(textoNormalizado);
            u.lang = (voz && voz.lang) ? voz.lang : 'it-IT';
            if (voz)
                u.voice = voz;
            let rate = opcoes.rate;
            if (rate == null && typeof localStorage !== 'undefined') {
                const speedStr = localStorage.getItem('it_audio_speed');
                if (speedStr)
                    rate = parseFloat(speedStr);
            }
            if (rate == null || isNaN(rate) || rate <= 0)
                rate = 0.88;
            u.rate = Math.max(0.5, Math.min(1.8, rate));
            if (textoNormalizado.endsWith('?')) {
                u.pitch = 1.05;
            }
            else if (textoNormalizado.endsWith('!')) {
                u.pitch = 1.02;
            }
            else {
                u.pitch = 1.0;
            }
            if (typeof window !== 'undefined') {
                window._activeVoiceUtterance = u;
            }
            u.onend = () => {
                if (typeof window !== 'undefined' && window._activeVoiceUtterance === u) {
                    window._activeVoiceUtterance = null;
                }
                if (opcoes.onend)
                    opcoes.onend();
            };
            u.onerror = (err) => {
                if (typeof window !== 'undefined' && window._activeVoiceUtterance === u) {
                    window._activeVoiceUtterance = null;
                }
                console.warn('[VoiceEngine] Falha na síntese nativa de fala:', err);
                if (opcoes.onend) {
                    setTimeout(opcoes.onend, 800);
                }
                else if (opcoes.onerror) {
                    opcoes.onerror(err);
                }
            };
            speechSynthesis.speak(u);
            return true;
        }
        catch (err) {
            console.warn('[VoiceEngine] Exceção ao sintetizar fala:', err);
            if (opcoes.onerror)
                opcoes.onerror(err);
            return false;
        }
    }
};
if (typeof window !== 'undefined') {
    window.VoiceEngine = VoiceEngine;
}
if (typeof globalThis !== 'undefined') {
    globalThis.VoiceEngine = VoiceEngine;
}
if (typeof document !== 'undefined') {
    document.addEventListener('visibilitychange', () => {
        if (document.hidden && typeof VoiceEngine !== 'undefined') {
            VoiceEngine.suspenderAudioContext();
        }
    });
    window.addEventListener('beforeunload', () => {
        if (typeof VoiceEngine !== 'undefined') {
            VoiceEngine.destruir();
        }
    });
}
export default VoiceEngine;
