// ============================================================
// js/audio_cache.js — Cache Persistente de Áudio Local (IndexedDB)
// Armazena áudios sintetizados ou baixados diretamente no navegador
// do usuário. Transforma livros e textos importados em audiolivros
// permanentes que tocam instantaneamente (0ms) mesmo sem internet.
// ============================================================

const AudioCache = {
  DB_NAME: 'it_audio_db',
  DB_VERSION: 1,
  STORE_NAME: 'audio_cache',
  _dbPromise: null,

  // Inicializa e abre a conexão com o IndexedDB
  _abrirDB() {
    if (this._dbPromise) return this._dbPromise;

    this._dbPromise = new Promise((resolve, reject) => {
      if (typeof indexedDB === 'undefined') {
        resolve(null);
        return;
      }

      const req = indexedDB.open(this.DB_NAME, this.DB_VERSION);

      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(this.STORE_NAME)) {
          // Cria a store indexada pela chave hash do texto
          db.createObjectStore(this.STORE_NAME, { keyPath: 'hash' });
        }
      };

      req.onsuccess = (e) => resolve(e.target.result);
      req.onerror = (e) => {
        console.warn('[AudioCache] Erro ao abrir IndexedDB:', e);
        resolve(null);
      };
    });

    return this._dbPromise;
  },

  // Gera uma hash SHA-256 ou FNV-1a rápida e estável para a chave do texto
  async gerarHash(texto, vozId = 'default') {
    const raw = `${vozId}:${(texto || '').trim().toLowerCase()}`;
    if (typeof crypto !== 'undefined' && crypto.subtle && crypto.subtle.digest) {
      try {
        const msgUint8 = new TextEncoder().encode(raw);
        const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        return hashArray.map(b => b.toString(16).padStart(2, '0')).join('').slice(0, 32);
      } catch (_) {}
    }
    // Fallback FNV-1a para ambientes síncronos
    let hash = 2166136261;
    for (let i = 0; i < raw.length; i++) {
      hash ^= raw.charCodeAt(i);
      hash += (hash << 1) + (hash << 4) + (hash << 7) + (hash << 8) + (hash << 24);
    }
    return 'fnv_' + (hash >>> 0).toString(16);
  },

  // Recupera um áudio salvo pelo hash do texto
  async obter(texto, vozId = 'default') {
    try {
      const db = await this._abrirDB();
      if (!db) return null;

      const hash = await this.gerarHash(texto, vozId);
      return new Promise((resolve) => {
        const tx = db.transaction(this.STORE_NAME, 'readonly');
        const store = tx.objectStore(this.STORE_NAME);
        const req = store.get(hash);

        req.onsuccess = () => {
          if (req.result && req.result.blob) {
            resolve(req.result.blob);
          } else {
            resolve(null);
          }
        };
        req.onerror = () => resolve(null);
      });
    } catch (_) {
      return null;
    }
  },

  // Salva um Blob ou ArrayBuffer de áudio no IndexedDB
  async salvar(texto, blobOuBuffer, vozId = 'default', metadata = {}) {
    try {
      const db = await this._abrirDB();
      if (!db || !blobOuBuffer) return false;

      const hash = await this.gerarHash(texto, vozId);
      const blob = (blobOuBuffer instanceof Blob)
        ? blobOuBuffer
        : new Blob([blobOuBuffer], { type: 'audio/wav' });

      return new Promise((resolve) => {
        const tx = db.transaction(this.STORE_NAME, 'readwrite');
        const store = tx.objectStore(this.STORE_NAME);
        const registro = {
          hash,
          blob,
          vozId,
          tamanho: blob.size,
          data: Date.now(),
          ...metadata
        };

        const req = store.put(registro);
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
      });
    } catch (_) {
      return false;
    }
  },

  // Retorna a contagem e tamanho total dos áudios em cache
  async estatisticas() {
    try {
      const db = await this._abrirDB();
      if (!db) return { itens: 0, bytes: 0 };

      return new Promise((resolve) => {
        const tx = db.transaction(this.STORE_NAME, 'readonly');
        const store = tx.objectStore(this.STORE_NAME);
        const req = store.openCursor();
        let itens = 0;
        let bytes = 0;

        req.onsuccess = (e) => {
          const cursor = e.target.result;
          if (cursor) {
            itens++;
            if (cursor.value && cursor.value.tamanho) {
              bytes += cursor.value.tamanho;
            }
            cursor.continue();
          } else {
            resolve({ itens, bytes });
          }
        };
        req.onerror = () => resolve({ itens: 0, bytes: 0 });
      });
    } catch (_) {
      return { itens: 0, bytes: 0 };
    }
  },

  // Limpa todos os áudios cacheados
  async limpar() {
    try {
      const db = await this._abrirDB();
      if (!db) return false;

      return new Promise((resolve) => {
        const tx = db.transaction(this.STORE_NAME, 'readwrite');
        const store = tx.objectStore(this.STORE_NAME);
        const req = store.clear();
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
      });
    } catch (_) {
      return false;
    }
  },

  // Remove entradas de simulação senoidal/mock que não são voz humana
  async limparMockAudio() {
    try {
      const db = await this._abrirDB();
      if (!db) return;
      const tx = db.transaction(this.STORE_NAME, 'readwrite');
      const store = tx.objectStore(this.STORE_NAME);
      const req = store.openCursor();
      req.onsuccess = (e) => {
        const cursor = e.target.result;
        if (cursor) {
          if (cursor.value.vozId === 'neural_it' || (cursor.value.tamanho && cursor.value.tamanho < 4096)) {
            cursor.delete();
          }
          cursor.continue();
        }
      };
    } catch (_) {}
  }
};

// Executa limpeza preventiva de áudios senoidais corrompidos
if (typeof window !== 'undefined') {
  window.AudioCache = AudioCache;
  try { AudioCache.limparMockAudio(); } catch (_) {}
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AudioCache;
}
