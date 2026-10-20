// ============================================================
// js/voice_engine.js — Motor Leve de Pronúncia e Prosódia Italiana
// Inspirado nos algoritmos de pré-processamento do VoiceStudio:
//  • text_normalization.py (limpeza de artefatos, elisões e símbolos)
//  • pronunciation.py (léxico de acentuação tônica para palavras sdrucciole)
//  • sentence_chunker.py (preservação de honoríficos italianos Sig./Dott./Prof.)
//  • ssml_lite.py & audio_dsp.py (ranking de vozes neurais e cadeia de clareza)
//
// 100% puro JS, zero servidor, zero dependências externas (~8 KB).
// ============================================================

const VoiceEngine = {
  // ── 1. Preservação de Honoríficos e Abreviaturas Italianas ──
  // Portado de VoiceStudio/backend/services/sentence_chunker.py (HONORIFICS_IT)
  HONORIFICS_IT: [
    'Sig', 'Sig.ra', 'Sig.na', 'Sgr', 'Dott', 'Dott.ssa',
    'Prof', 'Prof.ssa', 'Avv', 'Ing', 'Geom', 'Rag',
    'Arch', 'On', 'Egr', 'Spett', 'Gent', 'Ill'
  ],

  // ── 2. Léxico de Acentuação Tônica e Fonética Italiana ────
  // Portado de VoiceStudio/backend/services/pronunciation.py
  // Palavras proparoxítonas (sdrucciole) e homógrafas onde sintetizadores
  // costumam errar a sílaba forte se não tiverem acento fonético explícito.
  LEXICO_FONETICO_IT: {
    // Verbos e substantivos com tônica antepenúltima frequentemente errados
    'subito': 'sùbito',
    'Subito': 'Sùbito',
    'abito': 'àbito',
    'Abito': 'Àbito',
    'capitano': 'càpitano', // verbo (quando no início/contexto)
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
  // Portado e adaptado de VoiceStudio/backend/services/text_normalization.py
  normalizarParaFala(texto) {
    if (!texto || typeof texto !== 'string') return '';

    let s = texto;

    // A. Remove tags HTML caso tenham vindo na string
    s = s.replace(/<[^>]*>/g, ' ');

    // B. Remove traduções entre parênteses em português comuns nas lições/cards
    // Ex: "il gatto (o gato)" -> "il gatto"
    // Ex: "parlare (falar, conversar)" -> "parlare"
    s = s.replace(/\s*\([a-zà-úA-ZÀ-Ú\s,;.\-–—\/?!0-9]+\)/gi, (match) => {
      // Se tiver palavras claramente portuguesas, remove; se for apenas um exemplo italiano curto, preserva
      const ptClues = /\b(o|a|os|as|um|uma|de|do|da|em|no|na|para|com|por|que|se|ex|exemplo|verbo|lit|literalmente|trad|tradução)\b/i;
      if (ptClues.test(match)) return '';
      // Caso contenha apenas 1 ou 2 palavras sem conectivos italianos exclusivos, remove por segurança
      return '';
    });

    // C. Remove colchetes de IPA / pronúncia fonética auxiliar do texto
    // Ex: "buongiorno [bwon-djor-no]" -> "buongiorno"
    s = s.replace(/\s*\[[^\]]+\]/g, '');

    // D. Normaliza barras de alternativas para vírgulas com pausa natural
    // Evita que o TTS vocalize "barra" ou "slash"
    // Ex: "il / lo" -> "il, lo"
    s = s.replace(/(\w+)\s*\/\s*(\w+)/g, '$1, $2');

    // E. Remove setas, marcadores visuais e emojis
    // Ex: "io → parlo" -> "io: parlo"
    s = s.replace(/[→↔⇒➔➜]/g, ', ');
    s = s.replace(/[🔵🔴🟢🟡🟣⚪⚫★☆✔✓✗✘💡🔍📖✏️🎧👁️]/g, '');

    // F. Normaliza apóstrofos tipográficos para apóstrofo padrão reto
    // Essencial para elisões italianas (l’amico -> l'amico, un’ora -> un'ora)
    // Alguns motores leem apóstrofo curvo como caractere isolado
    s = s.replace(/[’‘`´]/g, "'");

    // G. Garante que elisões italianas comuns tenham junção fluida
    // Ex: "l' amico" -> "l'amico", "un' altra" -> "un'altra"
    s = s.replace(/\b([ldcnsmgt]|un|quest|sant|pover)'\s+([aeiouhàèéìòóù])/gi, "$1'$2");

    // H. Tratamento de pontuação excessiva
    s = s.replace(/\s+([,.;:!?])/g, '$1');
    s = s.replace(/[,;]{2,}/g, ',');
    s = s.replace(/\.{2,}/g, '...');
    s = s.replace(/\s+/g, ' ').trim();

    // I. Aplicação do Léxico Fonético (Acentuação Tônica Sdrucciola)
    // Aplica substituição por palavra inteira (\b)
    s = this.aplicarLexicoFonico(s);

    return s;
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
  // Portado de VoiceStudio/backend/services/pronunciation.py (apply_lexicon)
  aplicarLexicoFonico(texto) {
    if (!texto) return '';
    const lista = this._obterLexicoCompilado();
    let out = texto;
    for (let i = 0; i < lista.length; i++) {
      out = out.replace(lista[i].regex, lista[i].substituicao);
    }
    return out;
  },

  // ── 5. Quebra de Frases / Chunker com Pausas Naturais ────
  // Portado de VoiceStudio/backend/services/sentence_chunker.py
  dividirEmSentencas(texto) {
    if (!texto) return [];
    const t = this.normalizarParaFala(texto);
    if (!t) return [];

    // Protege abreviações comuns antes de quebrar em pontos
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

    // Quebra por pontuação terminal (. ! ?) ou pausas longas (: ou ;)
    const chunks = protegido
      .split(/(?<=[.!?])\s+|(?<=[;:])\s+/)
      .map(c => c.trim())
      .filter(Boolean);

    // Restaura placeholders
    return chunks.map(chunk => {
      let res = chunk;
      placeholders.forEach(({ ph, original }) => {
        res = res.replace(new RegExp(ph, 'g'), original);
      });
      return res;
    });
  },

  // ── 6. Seletor e Ranking de Vozes Neurais (Qualidade Máxima) ──
  // Resolve o problema de navegadores priorizarem vozes antigas/robóticas
  _cacheVozes: null,

  obterMelhoresVozesItalianas() {
    if (typeof speechSynthesis === 'undefined') return [];

    let todas = [];
    try {
      todas = speechSynthesis.getVoices() || [];
    } catch (e) {
      todas = [];
    }

    // Se o array de vozes for populado, mantém em cache de segurança
    if (todas.length > 0) {
      this._cacheVozes = todas;
    } else if (this._cacheVozes && this._cacheVozes.length > 0) {
      todas = this._cacheVozes;
    }

    // Filtragem tolerante a formatos: it-IT, it_IT, it*, ou qualquer voz com "italiano"/"italian" no nome
    const italianas = todas.filter(v => {
      const l = (v.lang || '').toLowerCase().replace(/_/g, '-');
      const n = (v.name || '').toLowerCase();
      return l === 'it-it' || l.startsWith('it-') || l === 'it' || n.includes('italian') || n.includes('italiano');
    });

    if (!italianas.length) return [];

    // Sistema de pontuação de qualidade (estilo VoiceStudio)
    const pontuarVoz = (v) => {
      let score = 0;
      const nome = (v.name || '').toLowerCase();
      const lang = (v.lang || '').toLowerCase().replace(/_/g, '-');

      // Tier S: Vozes Neurais / Naturais modernas (alta definição humana)
      if (nome.includes('natural') || nome.includes('online')) score += 100;
      if (nome.includes('neural')) score += 90;
      if (nome.includes('premium') || nome.includes('enhanced')) score += 80;
      if (nome.includes('google')) score += 70;

      // Preferências de vozes específicas consagradas do Windows/Edge/Apple
      if (nome.includes('isabella')) score += 35; // Microsoft Isabella Online (Natural)
      if (nome.includes('diego')) score += 35;    // Microsoft Diego Online (Natural)
      if (nome.includes('elsa')) score += 30;     // Microsoft Elsa Online
      if (nome.includes('federica')) score += 30; // Apple Federica (Enhanced)
      if (nome.includes('alice')) score += 25;    // Apple Alice
      if (nome.includes('luca')) score += 25;     // Apple Luca

      // Preferência se for estritamente it-IT
      if (lang === 'it-it') score += 15;

      // Penalidade para vozes desktop antigas SAPI5 (soam metálicas/robóticas)
      if (nome.includes('desktop') || nome.includes('sapi')) score -= 50;

      return score;
    };

    return [...italianas].sort((a, b) => pontuarVoz(b) - pontuarVoz(a));
  },

  obterVozSelecionada() {
    const ordenadas = this.obterMelhoresVozesItalianas();
    if (!ordenadas.length) return null;

    // 1. Verifica se o usuário escolheu uma voz específica nas configurações
    const salva = (typeof localStorage !== 'undefined') ? localStorage.getItem('it_voz_preferida') : null;
    if (salva) {
      const encontrada = ordenadas.find(v => v.name === salva || v.voiceURI === salva);
      if (encontrada) return encontrada;
    }

    // 2. Retorna a voz mais bem ranqueada (Tier Neural/Natural)
    return ordenadas[0];
  },

  // ── 7. Cadeia de Áudio Web Audio DSP (Mastering / Clareza) ──
  // Portado de VoiceStudio/backend/services/audio_dsp.py (MASTERING_CHAIN)
  // Aplica filtro passa-altas (remove estalos/sub-graves) e compressão suave
  _audioCtx: null,
  _masterNode: null,

  obterAudioContext() {
    if (!this._audioCtx && typeof (window.AudioContext || window.webkitAudioContext) !== 'undefined') {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      this._audioCtx = new AudioCtx();
    }
    if (this._audioCtx && this._audioCtx.state === 'suspended') {
      this._audioCtx.resume().catch(() => {});
    }
    return this._audioCtx;
  },

  // Conecta um elemento HTMLAudioElement à cadeia de clareza do VoiceStudio
  aplicarMasteringAudioElement(audioEl) {
    if (!audioEl || audioEl._vsMastered) return;
    try {
      const ctx = this.obterAudioContext();
      if (!ctx) return;

      const source = ctx.createMediaElementSource(audioEl);

      // Highpass @ 80Hz (remove rumble e estalos de microfone)
      const highpass = ctx.createBiquadFilter();
      highpass.type = 'highpass';
      highpass.frequency.setValueAtTime(80, ctx.currentTime);

      // Presença/Clareza vocal @ 3000Hz (+2dB suave)
      const presence = ctx.createBiquadFilter();
      presence.type = 'peaking';
      presence.frequency.setValueAtTime(3000, ctx.currentTime);
      presence.Q.setValueAtTime(1.0, ctx.currentTime);
      presence.gain.setValueAtTime(2.0, ctx.currentTime);

      // Compressor suave (porta de MASTERING_CHAIN: threshold -15dB, ratio 1.8, attack 2ms, release 100ms)
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
    } catch (e) {
      // Se não for permitido CORS ou já conectado, mantém reprodução normal
    }
  },

  // ── 8. Motor Neural WebAssembly & Cache IndexedDB ──────────
  _worker: null,
  _pendingSyntheses: new Map(),
  _currentAudioSource: null,
  _workerInitialized: false,
  _workerDownloading: false,

  _getWorker() {
    if (this._worker) return this._worker;
    if (typeof Worker === 'undefined') return null;

    try {
      this._worker = new Worker('js/tts_worker.js');
      this._worker.onmessage = (e) => this._onWorkerMessage(e);
      this._worker.onerror = (err) => {
        console.warn('[VoiceEngine] Erro no TTS Web Worker:', err);
      };
      // Consulta status inicial do worker
      this._worker.postMessage({ type: 'CHECK_STATUS' });
      return this._worker;
    } catch (e) {
      console.warn('[VoiceEngine] Web Worker não suportado ou bloqueado:', e);
      return null;
    }
  },

  _onWorkerMessage(e) {
    const { type, id, error, wavBuffer, isInitialized, percent } = e.data || {};

    if (type === 'STATUS') {
      this._workerInitialized = !!isInitialized;
    } else if (type === 'DOWNLOAD_PROGRESS') {
      if (typeof this._onDownloadProgress === 'function') {
        this._onDownloadProgress(percent);
      }
    } else if (type === 'INIT_SUCCESS') {
      this._workerInitialized = true;
      this._workerDownloading = false;
      localStorage.setItem('it_voz_neural_instalada', 'true');
      if (typeof this._onDownloadSuccess === 'function') {
        this._onDownloadSuccess();
      }
    } else if (type === 'INIT_ERROR') {
      this._workerDownloading = false;
      if (typeof this._onDownloadError === 'function') {
        this._onDownloadError(error);
      }
    } else if (type === 'SYNTHESIZE_SUCCESS') {
      const resolver = this._pendingSyntheses.get(id);
      if (resolver) {
        this._pendingSyntheses.delete(id);
        resolver.resolve(wavBuffer);
      }
    } else if (type === 'SYNTHESIZE_ERROR') {
      const resolver = this._pendingSyntheses.get(id);
      if (resolver) {
        this._pendingSyntheses.delete(id);
        resolver.reject(new Error(error || 'Erro na síntese neural'));
      }
    }
  },

  statusVozNeural() {
    const salva = localStorage.getItem('it_voz_neural_instalada') === 'true';
    return {
      instalada: salva || this._workerInitialized,
      baixando: this._workerDownloading,
      ativa: localStorage.getItem('it_usar_voz_neural') !== 'false'
    };
  },

  baixarVozNeural(onProgress, onSuccess, onError, forceRefresh = false) {
    const worker = this._getWorker();
    if (!worker) {
      if (onError) onError('Web Worker não suportado');
      return;
    }
    this._workerDownloading = true;
    this._onDownloadProgress = onProgress;
    this._onDownloadSuccess = onSuccess;
    this._onDownloadError = onError;

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
    } catch (_) {}
    localStorage.removeItem('it_voz_neural_instalada');
    if (localStorage.getItem('it_voz_preferida') === 'wasm_neural') {
      localStorage.removeItem('it_voz_preferida');
    }
    this._workerInitialized = false;
    this._workerDownloading = false;
    if (this._worker) {
      try { this._worker.terminate(); } catch (_) {}
      this._worker = null;
    }
    return true;
  },

  // Para qualquer áudio neural ou fala nativa em execução
  parar() {
    window._activeVoiceUtterance = null;
    if (typeof speechSynthesis !== 'undefined') {
      try {
        speechSynthesis.cancel();
      } catch (_) {}
    }
    if (this._currentAudioSource) {
      try {
        this._currentAudioSource.stop();
        this._currentAudioSource.disconnect();
      } catch (_) {}
      this._currentAudioSource = null;
    }
  },

  // Reproduz um ArrayBuffer de áudio WAV via Web Audio API com cadeia de clareza
  async _tocarBuffer(wavBuffer, opcoes = {}) {
    this.parar();
    const ctx = this.obterAudioContext();
    if (!ctx) return false;

    try {
      const audioBuffer = await ctx.decodeAudioData(wavBuffer.slice(0));
      const source = ctx.createBufferSource();
      source.buffer = audioBuffer;

      // Rate de velocidade
      let rate = opcoes.rate;
      if (rate == null) {
        const speedStr = localStorage.getItem('it_audio_speed');
        rate = parseFloat(speedStr);
      }
      if (!isNaN(rate) && rate > 0) {
        source.playbackRate.value = Math.max(0.5, Math.min(2.0, rate));
      }

      source.connect(ctx.destination);
      this._currentAudioSource = source;

      source.onended = () => {
        if (this._currentAudioSource === source) {
          this._currentAudioSource = null;
        }
        if (opcoes.onend) opcoes.onend();
      };

      source.start();
      return true;
    } catch (err) {
      console.warn('[VoiceEngine] Falha ao decodificar/tocar buffer:', err);
      if (opcoes.onerror) opcoes.onerror(err);
      return false;
    }
  },

  // ── 9. Síntese Neural Unificada com Cache Automático e Fallback ──
  async falarNeural(texto, opcoes = {}) {
    if (!texto) return false;
    const textoNorm = this.normalizarParaFala(texto);
    if (!textoNorm) return false;

    this.parar();

    // 1. Verifica cache persistente local no IndexedDB (apenas gravações reais válidas > 4KB)
    if (typeof AudioCache !== 'undefined') {
      try {
        const blobCache = await AudioCache.obter(textoNorm, 'neural_it');
        if (blobCache && blobCache.size > 4096) {
          const buffer = await blobCache.arrayBuffer();
          if (buffer.byteLength > 4096) {
            return await this._tocarBuffer(buffer, opcoes);
          }
        }
      } catch (_) {}
    }

    // 2. Se a voz neural WASM com inferência ONNX real estiver carregada, executa
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
          if (typeof AudioCache !== 'undefined') {
            AudioCache.salvar(textoNorm, wavBuffer, 'neural_it').catch(() => {});
          }
          return await this._tocarBuffer(wavBuffer, opcoes);
        }
      } catch (err) {
        // Fallback silencioso para a voz humana nativa
      }
    }

    // 3. Execução Principal: Voz nativa de alta definição do sistema com prosódia do VoiceStudio
    return this.falar(textoNorm, opcoes);
  },

  // ── 10. Execução Principal de Fala (Voz Nativa de Alta Fidelidade) ────────
  falar(texto, opcoes = {}) {
    if (!texto) return false;

    const textoNormalizado = this.normalizarParaFala(texto);
    if (!textoNormalizado) return false;

    if (typeof speechSynthesis === 'undefined') {
      if (typeof App !== 'undefined' && App._pronunciarRV) {
        App._pronunciarRV(textoNormalizado, opcoes.rate);
        if (opcoes.onend) setTimeout(opcoes.onend, 1000);
        return true;
      }
      return false;
    }

    try {
      // Destrava fila no Chromium caso esteja pausada
      if (speechSynthesis.paused) {
        try { speechSynthesis.resume(); } catch (_) {}
      }
      this.parar();

      const voz = this.obterVozSelecionada();
      const u = new SpeechSynthesisUtterance(textoNormalizado);
      u.lang = (voz && voz.lang) ? voz.lang : 'it-IT';
      if (voz) u.voice = voz;

      // Taxa de velocidade (respeita configuração do usuário)
      let rate = opcoes.rate;
      if (rate == null) {
        const speedStr = localStorage.getItem('it_audio_speed');
        rate = parseFloat(speedStr);
      }
      if (isNaN(rate) || rate <= 0) rate = 0.88;
      u.rate = Math.max(0.5, Math.min(1.8, rate));

      // Afinação (pitch) adaptativo baseado na pontuação da frase
      if (textoNormalizado.endsWith('?')) {
        u.pitch = 1.05;
      } else if (textoNormalizado.endsWith('!')) {
        u.pitch = 1.02;
      } else {
        u.pitch = 1.0;
      }

      // Previne coleta de lixo prematura do Chromium (Chromium GC Bug)
      window._activeVoiceUtterance = u;

      u.onend = () => {
        if (window._activeVoiceUtterance === u) {
          window._activeVoiceUtterance = null;
        }
        if (opcoes.onend) opcoes.onend();
      };

      u.onerror = (err) => {
        if (window._activeVoiceUtterance === u) {
          window._activeVoiceUtterance = null;
        }
        console.warn('[VoiceEngine] Falha na síntese nativa de fala:', err);
        if (opcoes.onend) {
          setTimeout(opcoes.onend, 800);
        } else if (opcoes.onerror) {
          opcoes.onerror(err);
        }
      };

      speechSynthesis.speak(u);
      return true;
    } catch (err) {
      console.warn('[VoiceEngine] Exceção ao sintetizar fala:', err);
      if (opcoes.onerror) opcoes.onerror(err);
      return false;
    }
  }
};

// Exporta globalmente para o navegador
window.VoiceEngine = VoiceEngine;

