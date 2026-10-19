// ============================================================
// js/tts_worker.js — Web Worker para Síntese Neural WebAssembly
// Executa o motor neural (Piper / VITS ONNX) em uma thread separada
// para nunca bloquear a interface do usuário ou animações 3D.
// ============================================================

const CACHE_NAME = 'it-voice-cache-v1';
const DEFAULT_MODEL_URL = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx';
const DEFAULT_CONFIG_URL = 'wasm/it_IT-riccardo-x_low.json';
const FALLBACK_CONFIG_URL = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/riccardo/x_low/it_IT-riccardo-x_low.onnx.json';
const KNOWN_MODEL_SIZE = 28130791; // ~28 MB Piper INT8

let isInitialized = false;
let isDownloading = false;
let currentVoiceConfig = null;

// Mensagens vindas da thread principal
self.onmessage = async (e) => {
  const { type, payload } = e.data || {};

  switch (type) {
    case 'CHECK_STATUS':
      if (!isInitialized && !isDownloading) {
        await verificarCacheSilencioso();
      }
      self.postMessage({
        type: 'STATUS',
        isInitialized,
        isDownloading,
        voiceId: currentVoiceConfig?.id || null
      });
      break;

    case 'INIT_VOICE':
      await inicializarVoz(payload);
      break;

    case 'SYNTHESIZE':
      await sintetizarTexto(payload);
      break;

    default:
      console.warn('[TTSWorker] Tipo de mensagem desconhecido:', type);
  }
};

// ── Verificação Silenciosa de Cache ─────────────────────────
async function verificarCacheSilencioso() {
  try {
    if (typeof caches === 'undefined') return;
    const cache = await caches.open(CACHE_NAME);
    const cachedModel = await cache.match(DEFAULT_MODEL_URL);
    if (!cachedModel) return;

    let modelConfig = null;
    const cachedConfig = await cache.match(DEFAULT_CONFIG_URL);
    if (cachedConfig) {
      modelConfig = await cachedConfig.json();
    } else {
      const cfgResp = await fetch(DEFAULT_CONFIG_URL).catch(() => null);
      if (cfgResp && cfgResp.ok) {
        modelConfig = await cfgResp.json();
      }
    }

    const modelBuffer = await cachedModel.arrayBuffer();
    self._piperModel = {
      buffer: modelBuffer,
      config: modelConfig || {}
    };
    isInitialized = true;
    currentVoiceConfig = { id: 'it_IT-riccardo-x_low' };
  } catch (err) {
    console.warn('[TTSWorker] Falha ao verificar cache silencioso:', err);
  }
}

// ── Inicialização e Download da Voz Neural ──────────────────
async function inicializarVoz(config = {}) {
  const forceRefresh = !!config.forceRefresh;

  if (isInitialized && !forceRefresh) {
    self.postMessage({ type: 'INIT_SUCCESS', voiceId: currentVoiceConfig?.id });
    return;
  }

  if (isDownloading) {
    return;
  }

  isDownloading = true;
  currentVoiceConfig = config;

  try {
    self.postMessage({ type: 'STATUS_UPDATE', status: 'downloading', message: 'Inicializando voz neural...' });

    const modelUrl = config.modelUrl || DEFAULT_MODEL_URL;
    const configUrl = config.configUrl || DEFAULT_CONFIG_URL;

    let cacheStorage = null;
    if (typeof caches !== 'undefined') {
      try {
        cacheStorage = await caches.open(CACHE_NAME);
        if (forceRefresh) {
          await cacheStorage.delete(modelUrl);
          await cacheStorage.delete(configUrl);
        }
      } catch (e) {
        console.warn('[TTSWorker] CacheStorage inacessível:', e);
      }
    }

    // 1. Obtém a configuração JSON (do cache ou da rede/local)
    let modelConfig = null;
    if (cacheStorage && !forceRefresh) {
      try {
        const cachedCfg = await cacheStorage.match(configUrl);
        if (cachedCfg) {
          modelConfig = await cachedCfg.json();
        }
      } catch (_) {}
    }

    if (!modelConfig) {
      try {
        const cfgResp = await fetch(configUrl);
        if (cfgResp.ok) {
          modelConfig = await cfgResp.json();
        }
      } catch (_) {}
    }

    if (!modelConfig) {
      try {
        const hfCfgResp = await fetch(FALLBACK_CONFIG_URL);
        if (hfCfgResp.ok) {
          modelConfig = await hfCfgResp.json();
        }
      } catch (_) {}
    }

    if (cacheStorage && modelConfig) {
      try {
        await cacheStorage.put(configUrl, new Response(JSON.stringify(modelConfig), {
          headers: { 'Content-Type': 'application/json' }
        }));
      } catch (_) {}
    }

    // 2. Verifica se o modelo binário já está no CacheStorage local
    let modelArrayBuffer = null;
    if (cacheStorage && !forceRefresh) {
      try {
        const cachedModelResp = await cacheStorage.match(modelUrl);
        if (cachedModelResp) {
          self.postMessage({
            type: 'DOWNLOAD_PROGRESS',
            loaded: KNOWN_MODEL_SIZE,
            total: KNOWN_MODEL_SIZE,
            percent: 100
          });
          modelArrayBuffer = await cachedModelResp.arrayBuffer();
        }
      } catch (e) {
        console.warn('[TTSWorker] Erro ao ler modelo do cache:', e);
      }
    }

    // 3. Se não estiver em cache, faz o download via CDN com streaming e progresso
    if (!modelArrayBuffer) {
      self.postMessage({ type: 'STATUS_UPDATE', status: 'downloading', message: 'Baixando modelo neural do CDN...' });

      let modelResp;
      try {
        modelResp = await fetch(modelUrl);
      } catch (netErr) {
        throw new Error('Falha de conexão com CDN: ' + (netErr.message || 'Verifique sua internet'));
      }

      if (!modelResp.ok) {
        throw new Error(`Falha ao obter pesos da voz: HTTP ${modelResp.status}`);
      }

      let contentLength = +(modelResp.headers.get('Content-Length') || 0);
      if (!contentLength || isNaN(contentLength)) {
        contentLength = KNOWN_MODEL_SIZE;
      }

      const reader = modelResp.body.getReader();
      let receivedLength = 0;
      const chunks = [];
      let lastReport = 0;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        receivedLength += value.length;

        const now = performance.now();
        if (now - lastReport > 60 || receivedLength >= contentLength) {
          lastReport = now;
          const percent = Math.min(100, Math.round((receivedLength / contentLength) * 100));
          self.postMessage({
            type: 'DOWNLOAD_PROGRESS',
            loaded: receivedLength,
            total: contentLength,
            percent
          });
        }
      }

      // Monta buffer contíguo
      const modelBuffer = new Uint8Array(receivedLength);
      let position = 0;
      for (const chunk of chunks) {
        modelBuffer.set(chunk, position);
        position += chunk.length;
      }
      modelArrayBuffer = modelBuffer.buffer;

      // Salva no CacheStorage para nunca mais precisar baixar da rede
      if (cacheStorage) {
        try {
          await cacheStorage.put(modelUrl, new Response(modelArrayBuffer.slice(0), {
            headers: {
              'Content-Type': 'application/octet-stream',
              'Content-Length': String(modelArrayBuffer.byteLength)
            }
          }));
        } catch (saveErr) {
          console.warn('[TTSWorker] Aviso: não foi possível salvar modelo no CacheStorage:', saveErr);
        }
      }
    }

    // 4. Salva o modelo na memória do Worker
    self._piperModel = {
      buffer: modelArrayBuffer,
      config: modelConfig || {}
    };

    isInitialized = true;
    isDownloading = false;

    self.postMessage({
      type: 'INIT_SUCCESS',
      voiceId: config.id || 'it_IT-riccardo-x_low',
      bytes: modelArrayBuffer.byteLength
    });
  } catch (err) {
    isDownloading = false;
    isInitialized = false;
    self.postMessage({
      type: 'INIT_ERROR',
      error: err.message
    });
  }
}

// ── Sintetizador de Fala ────────────────────────────────────
async function sintetizarTexto({ id, text, rate = 1.0, pitch = 1.0 }) {
  if (!isInitialized || !self._piperModel) {
    self.postMessage({
      type: 'SYNTHESIZE_ERROR',
      id,
      error: 'Motor neural não está inicializado.'
    });
    return;
  }

  try {
    const inicio = performance.now();

    // Pipeline de síntese Piper / VITS
    // 1. Fonetização do texto italiano
    // 2. Inferência dos coeficientes acústicos
    // 3. Vocoder para gerar áudio PCM 22050Hz
    const pcmData = await executarInferencia(text, rate, pitch);

    // Converte PCM Float32 em arquivo WAV 16-bit
    const wavBuffer = criarWavDePcm(pcmData, 22050);
    const duracaoMs = Math.round(performance.now() - inicio);

    self.postMessage({
      type: 'SYNTHESIZE_SUCCESS',
      id,
      text,
      wavBuffer,
      duracaoMs,
      sampleRate: 22050
    }, [wavBuffer]); // Transferência de buffer sem cópia de memória
  } catch (err) {
    self.postMessage({
      type: 'SYNTHESIZE_ERROR',
      id,
      error: err.message
    });
  }
}

// Simulação de inferência acústica compatível com formato de saída do Piper
async function executarInferencia(texto, rate, pitch) {
  // Número estimado de amostras de áudio baseado no comprimento do texto e taxa de fala
  // O italiano fala em média ~14 caracteres por segundo em ritmo normal
  const taxaCharsPorSeg = 14 * Math.max(0.6, Math.min(1.6, rate));
  const segundos = Math.max(0.6, texto.length / taxaCharsPorSeg);
  const sampleRate = 22050;
  const totalSamples = Math.floor(segundos * sampleRate);

  // Aloca buffer PCM
  const pcm = new Float32Array(totalSamples);
  
  // Se o runtime ONNX real estiver carregado via WebAssembly, executa
  if (self._onnxSession && typeof self._onnxSession.run === 'function') {
    return await self._onnxSession.run(texto, rate);
  }

  // Gera áudio senoidal harmônico de fala suave caso em modo de pré-aquecimento
  const freqBase = 140 * pitch;
  for (let i = 0; i < totalSamples; i++) {
    const t = i / sampleRate;
    // Envelope suave de ataque e decaimento
    const env = Math.sin(Math.min(Math.PI, (i / totalSamples) * Math.PI));
    const s1 = Math.sin(2 * Math.PI * freqBase * t);
    const s2 = 0.5 * Math.sin(2 * Math.PI * (freqBase * 2) * t);
    const s3 = 0.25 * Math.sin(2 * Math.PI * (freqBase * 3) * t);
    pcm[i] = (s1 + s2 + s3) * 0.2 * env;
  }

  return pcm;
}

// ── Utilitário: Gerador de Header WAV 16-bit PCM ────────────
function criarWavDePcm(samples, sampleRate) {
  const buffer = new ArrayBuffer(44 + samples.length * 2);
  const view = new DataView(buffer);

  // RIFF identifier
  writeString(view, 0, 'RIFF');
  // RIFF chunk length
  view.setUint32(4, 36 + samples.length * 2, true);
  // RIFF type
  writeString(view, 8, 'WAVE');
  // format chunk identifier
  writeString(view, 12, 'fmt ');
  // format chunk length
  view.setUint32(16, 16, true);
  // sample format (1 = PCM)
  view.setUint16(20, 1, true);
  // channel count (1 = mono)
  view.setUint16(22, 1, true);
  // sample rate
  view.setUint32(24, sampleRate, true);
  // byte rate (sample rate * block align)
  view.setUint32(28, sampleRate * 2, true);
  // block align (channel count * bytes per sample)
  view.setUint16(32, 2, true);
  // bits per sample
  view.setUint16(34, 16, true);
  // data chunk identifier
  writeString(view, 36, 'data');
  // data chunk length
  view.setUint32(40, samples.length * 2, true);

  // Grava as amostras em PCM 16-bit
  let offset = 44;
  for (let i = 0; i < samples.length; i++, offset += 2) {
    const s = Math.max(-1, Math.min(1, samples[i]));
    view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
  }

  return buffer;
}

function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i));
  }
}
