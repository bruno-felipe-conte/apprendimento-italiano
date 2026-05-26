// ============================================================
// sw.js — Service Worker for offline / PWA support
// Cache-first for static assets; network-first for data files
// ============================================================

const CACHE = 'italiano-v2';

const STATIC = [
  '/',
  '/index.html',
  '/css/italia.css',
  '/js/core.js',
  '/js/progression.js',
  '/js/flashcards.js',
  '/js/quiz.js',
  '/js/vocab.js',
  '/js/heatmap.js',
  '/manifest.webmanifest',
  '/icons/icon.svg',
];

// Install: pre-cache all static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(STATIC))
  );
  self.skipWaiting();
});

// Activate: delete old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: cache-first for static, network-first for data/
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Skip non-GET and cross-origin requests
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) return;

  if (url.pathname.startsWith('/data/')) {
    // Network-first for vocabulary/quiz JSON (allows updates)
    event.respondWith(
      fetch(event.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(event.request, clone));
          return res;
        })
        .catch(() => caches.match(event.request))
    );
  } else {
    // Cache-first for everything else
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
