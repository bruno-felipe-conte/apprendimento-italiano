// audio-store.js — Armazenamento local de áudio (IndexedDB) para músicas customizadas com áudio real sincronizado
const AudioStore = {
  _db: null,
  _urlCache: {},

  _open() {
    if (this._db) return Promise.resolve(this._db);
    return new Promise((resolve, reject) => {
      const req = indexedDB.open('it_audio_store', 1);
      req.onupgradeneeded = () => {
        const db = req.result;
        if (!db.objectStoreNames.contains('audios')) {
          db.createObjectStore('audios');
        }
      };
      req.onsuccess = () => { this._db = req.result; resolve(this._db); };
      req.onerror = () => reject(req.error);
    });
  },

  async salvar(key, blob) {
    const db = await this._open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('audios', 'readwrite');
      tx.objectStore('audios').put(blob, key);
      tx.oncomplete = () => { delete this._urlCache[key]; resolve(); };
      tx.onerror = () => reject(tx.error);
    });
  },

  async obter(key) {
    const db = await this._open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('audios', 'readonly');
      const req = tx.objectStore('audios').get(key);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
  },

  async obterURL(key) {
    if (!key) return null;
    if (this._urlCache[key]) return this._urlCache[key];
    const blob = await this.obter(key);
    if (!blob) return null;
    const url = URL.createObjectURL(blob);
    this._urlCache[key] = url;
    return url;
  },

  async remover(key) {
    if (!key) return;
    const db = await this._open();
    return new Promise((resolve, reject) => {
      const tx = db.transaction('audios', 'readwrite');
      tx.objectStore('audios').delete(key);
      tx.oncomplete = () => {
        if (this._urlCache[key]) { URL.revokeObjectURL(this._urlCache[key]); delete this._urlCache[key]; }
        resolve();
      };
      tx.onerror = () => reject(tx.error);
    });
  },
};
