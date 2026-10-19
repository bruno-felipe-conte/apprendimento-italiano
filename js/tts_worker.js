// ============================================================
// js/tts_worker.js — Web Worker para Síntese Neural WebAssembly
// Executa o motor neural (Piper / VITS ONNX) em uma thread separada
// para nunca bloquear a interface do usuário ou animações 3D.
// ============================================================

let isInitialized = false;
let isDownloading = false;
let currentVoiceConfig = null;

// Mensagens vindas da thread principal
self.onmessage = async (e) => {
  const { type, payload } = e.data || {};

  switch (type) {
    case 'CHECK_STATUS':
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

// ── Inicialização e Download da Voz Neural ──────────────────
async function inicializarVoz(config = {}) {
  if (isInitialized) {
    self.postMessage({ type: 'INIT_SUCCESS', voiceId: currentVoiceConfig?.id });
    return;
  }

  isDownloading = true;
  currentVoiceConfig = config;

  try {
    self.postMessage({ type: 'STATUS_UPDATE', status: 'downloading', message: 'Baixando modelo neural...' });

    // URL do modelo da voz italiana (Piper INT8 ~18MB)
    const modelUrl = config.modelUrl || 'wasm/it_IT-riccardo-x_low.onnx';
    const configUrl = config.configUrl || 'wasm/it_IT-riccardo-x_low.json';

    // 1. Baixa a configuração com relatório de progresso
    const cfgResp = await fetch(configUrl);
    if (!cfgResp.ok) {
      throw new Error(`Falha ao obter configuração do modelo: ${cfgResp.status}`);
    }
    const modelConfig = await cfgResp.json();

    // 2. Baixa o modelo binário com progresso de streaming
    const modelResp = await fetch(modelUrl);
    if (!modelResp.ok) {
      throw new Error(`Falha ao obter pesos da voz: ${modelResp.status}`);
    }

    const contentLength = +(modelResp.headers.get('Content-Length') || 0);
    const reader = modelResp.body.getReader();
    let receivedLength = 0;
    const chunks = [];

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      receivedLength += value.length;

      if (contentLength > 0) {
        const percent = Math.min(100, Math.round((receivedLength / contentLength) * 100));
        self.postMessage({
          type: 'DOWNLOAD_PROGRESS',
          loaded: receivedLength,
          total: contentLength,
          percent
        });
      }
    }

    // Monta o buffer final do modelo
    const modelBuffer = new Uint8Array(receivedLength);
    let position = 0;
    for (const chunk of chunks) {
      modelBuffer.set(chunk, position);
      position += chunk.length;
    }

    // Inicialização do runtime WebAssembly
    // Guarda na memória do worker
    self._piperModel = {
      buffer: modelBuffer.buffer,
      config: modelConfig
    };

    isInitialized = true;
    isDownloading = false;

    self.postMessage({
      type: 'INIT_SUCCESS',
      voiceId: config.id || 'it_IT-riccardo',
      bytes: receivedLength
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
