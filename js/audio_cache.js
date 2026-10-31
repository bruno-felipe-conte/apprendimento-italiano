// ============================================================
// js/audio_cache.js — Cache Persistente de Áudio Local (IndexedDB)
// Armazena áudios sintetizados ou baixados diretamente no navegador
// do usuário. Transforma livros e textos importados em audiolivros
// permanentes que tocam instantaneamente (0ms) mesmo sem internet.
// ============================================================

const AudioCache = {
  DB_NAME: 'it_audio_db',
  DB_VERSION: 2,
  STORE_NAME: 'audio_cache',
  TRAD_STORE: 'trad_cache',
  _dbPromise: null,

  // Inicializa e abre a conexão com o IndexedDB
  _abrirDB() {
    if (this._dbPromise) return this._dbPromise;

    this._dbPromise = new Promise((resolve) => {
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
        if (!db.objectStoreNames.contains(this.TRAD_STORE)) {
          // Cria store persistente de traduções (TTL 7 dias)
          db.createObjectStore(this.TRAD_STORE, { keyPath: 'hash' });
        }
      };

      req.onsuccess = (e) => {
        const db = e.target.result;

        // PREVENÇÃO DE DEADLOCK EM MULTI-ABA (F3):
        // Quando uma nova versão do banco é aberta por outra aba ou SW, o navegador
        // dispara 'versionchange' em todas as conexões abertas existentes.
        // O fechamento imediato permite que o req.onupgradeneeded da outra aba prossiga.
        db.onversionchange = () => {
          console.warn('[AudioCache] Mudança de versão detectada em outra aba. Fechando conexão para permitir upgrade.');
          try { db.close(); } catch (_) {}
          AudioCache._dbPromise = null;
        };

        db.onclose = () => {
          AudioCache._dbPromise = null;
        };

        resolve(db);
      };

      req.onblocked = () => {
        console.warn('[AudioCache] Abertura do IndexedDB bloqueada por conexão ativa em outra aba.');
      };

      req.onerror = (e) => {
        console.warn('[AudioCache] Erro ao abrir IndexedDB:', e);
        AudioCache._dbPromise = null;
        resolve(null);
      };
    });

    return this._dbPromise;
  },

  // Fecha explicitamente a conexão com o IndexedDB (útil para testes e teardown)
  fechar() {
    if (this._dbPromise) {
      this._dbPromise.then(db => {
        if (db) {
          try { db.close(); } catch (_) {}
        }
      }).catch(() => {});
      this._dbPromise = null;
    }
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
  },

  // Recupera tradução com validação de TTL (7 dias por padrão)
  async obterTraducao(texto) {
    if (!texto) return null;
    try {
      const db = await this._abrirDB();
      if (!db || !db.objectStoreNames.contains(this.TRAD_STORE)) return null;

      const hash = await this.gerarHash(texto, 'trad_it_pt');
      return new Promise((resolve) => {
        const tx = db.transaction(this.TRAD_STORE, 'readonly');
        const store = tx.objectStore(this.TRAD_STORE);
        const req = store.get(hash);
        req.onsuccess = () => {
          const item = req.result;
          if (item && item.traducao) {
            if (item.expiraEm && Date.now() > item.expiraEm) {
              resolve(null);
            } else {
              resolve(item.traducao);
            }
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

  // Salva tradução no IndexedDB com TTL de 7 dias
  async salvarTraducao(texto, traducao, ttlMs = 7 * 24 * 60 * 60 * 1000) {
    if (!texto || !traducao) return false;
    try {
      const db = await this._abrirDB();
      if (!db || !db.objectStoreNames.contains(this.TRAD_STORE)) return false;

      const hash = await this.gerarHash(texto, 'trad_it_pt');
      return new Promise((resolve) => {
        const tx = db.transaction(this.TRAD_STORE, 'readwrite');
        const store = tx.objectStore(this.TRAD_STORE);
        const registro = {
          hash,
          texto,
          traducao,
          salvoEm: Date.now(),
          expiraEm: Date.now() + ttlMs
        };
        const req = store.put(registro);
        req.onsuccess = () => resolve(true);
        req.onerror = () => resolve(false);
      });
    } catch (_) {
      return false;
    }
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
