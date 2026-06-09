// ============================================================
// sw.js — Service Worker  |  Cache v46  |  Offline-first PWA
// Estratégia:
//   • Static assets  → cache-first  (JS, CSS, HTML, ícones)
//   • /data/*.json   → network-first com fallback de cache
//   • Google Fonts   → stale-while-revalidate (cache após 1ª carga)
// ============================================================

const CACHE = 'italiano-v81';

// Todos os arquivos necessários para rodar 100% offline
const STATIC = [
  './',
  './index.html',
  './css/italia.css',
  './css/styles.css',
  // JS — módulos da aplicação (URLs com ?v=60 para forçar atualização de cache)
  './js/audio.js?v=60',
  './js/conquistas.js?v=60',
  './js/core.js?v=60',
  './js/dialoghi.js?v=60',
  './js/canzoni.js?v=60',
  './js/imitazione.js?v=60',
  './js/flashcards.js?v=60',
  './js/grammar.js?v=60',
  './js/heatmap.js?v=60',
  './js/onboarding.js?v=60',
  './js/profilo.js?v=60',
  './js/progression.js?v=60',
  './js/quiz.js?v=60',
  './js/quiz_data.js',
  './js/vocab.js?v=60',
  './js/i18n.js?v=60',
  './js/notificacoes.js',
  './js/tour.js',
  './js/storie.js?v=60',
  './js/ia-import.js',
  // Dados
  './data/conjugacoes.json',
  './data/grammar.json',
  './data/quizzes.json',
  './data/dialogi.json',
  './data/canzoni.json',
  './data/imitazioni.json',
  './data/storie.json',
  // Templos 1-51 (gerados dinamicamente)
  ...Array.from({length: 51}, (_, i) => `./data/templo-${i+1}.json`),
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
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(req, clone));
          return res;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // 3. Tudo o mais — cache-first
  event.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(res => {
      if (res.ok) {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(req, clone));
      }
      return res;
    }))
  );
});

// ── Push Notifications ────────────────────────────────────
// Recebe mensagem da página para agendar lembretes locais
self.addEventListener('message', event => {
  if (!event.data) return;

  if (event.data.type === 'AGENDAR_LEMBRETE') {
    const { delayMs, titulo, corpo, tag } = event.data;
    // Agenda a notificação via setTimeout dentro do SW
    // (funciona enquanto o SW estiver ativo; ao acordar o SW dispara)
    setTimeout(() => {
      self.registration.showNotification(titulo, {
        body:    corpo,
        icon:    './icons/icon.svg',
        badge:   './icons/icon.svg',
        tag:     tag || 'italiano-lembrete',
        renotify: true,
        data:    { url: './' },
      });
    }, delayMs);
  }
});

// Clique na notificação → abre o app
self.addEventListener('notificationclick', event => {
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(lista => {
      const existente = lista.find(c => c.url.includes('italiano') || c.url.endsWith('/'));
      if (existente) return existente.focus();
      return clients.openWindow(event.notification.data?.url || './');
    })
  );
});
