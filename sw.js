// ============================================================
// sw.js — Service Worker  |  Cache v11  |  Offline-first PWA
// Estratégia:
//   • Static assets  → cache-first  (JS, CSS, HTML, ícones)
//   • /data/*.json   → network-first com fallback de cache
//   • Google Fonts   → stale-while-revalidate (cache após 1ª carga)
// ============================================================

const CACHE = 'italiano-v11';

// Todos os arquivos necessários para rodar 100% offline
const STATIC = [
  './',
  './index.html',
  './css/italia.css',
  './css/styles.css',
  // JS — módulos da aplicação
  './js/audio.js',
  './js/conquistas.js',
  './js/core.js',
  './js/dialoghi.js',
  './js/canzoni.js',
  './js/imitazione.js',
  './js/flashcards.js',
  './js/grammar.js',
  './js/heatmap.js',
  './js/onboarding.js',
  './js/profilo.js',
  './js/progression.js',
  './js/quiz.js',
  './js/quiz_data.js',
  './js/vocab.js',
  // Dados
  './data/conjugacoes.json',
  './data/grammar.json',
  './data/quizzes.json',
  './data/dialogi.json',
  './data/canzoni.json',
  './data/imitazione.json',
  './data/templo-1.json',
  './data/templo-2.json',
  './data/templo-3.json',
  './data/templo-4.json',
  './data/templo-5.json',
  './data/templo-6.json',
  './data/templo-7.json',
  './data/templo-8.json',
  './data/templo-9.json',
  './data/templo-10.json',
  // Manifesto e ícone
  './manifest.webmanifest',
  './icons/icon.svg',
];

// ── Install: pré-cache de tudo ────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache =>
      // addAll falha se qualquer recurso não for encontrado;
      // tentamos individualmente para não abortar por arquivos opcionais
      Promise.allSettled(STATIC.map(url => cache.add(url)))
    )
  );
  self.skipWaiting();
});

// ── Activate: apaga caches antigos ───────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// ── Fetch ─────────────────────────────────────────────────
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);

  // 1. Google Fonts — stale-while-revalidate
  //    Após a primeira visita ficam disponíveis offline
  if (url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com') {
    event.respondWith(
      caches.open(CACHE).then(cache =>
        cache.match(req).then(cached => {
          const network = fetch(req).then(res => {
            cache.put(req, res.clone());
            return res;
          }).catch(() => cached);
          return cached || network;
        })
      )
    );
    return;
  }

  // Ignora requisições cross-origin que não sejam fontes
  if (url.origin !== self.location.origin) return;

  // 2. /data/*.json — network-first (recebe atualizações de conteúdo)
  //    Se offline, entrega do cache
  if (url.pathname.includes('/data/')) {
    event.respondWith(
      fetch(req)
        .then(res => {
          caches.open(CACHE).then(c => c.put(req, res.clone()));
          return res;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // 3. Tudo o mais — cache-first
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(res => {
      // Cacheia recursos novos encontrados em runtime
      if (res.ok) caches.open(CACHE).then(c => c.put(req, res.clone()));
      return res;
    }))
  );
});
