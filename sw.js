/* ============================================================
   사랑 오피스 · 피클 합동 비서실  —  Service Worker
   역할: (1) 홈 화면 설치 조건 충족  (2) 정적 셸 오프라인 캐시
   원칙: 앱 셸(index.html·manifest·아이콘)만 캐시하고,
        Google Sheets/Forms 같은 실시간 요청은 항상 네트워크로 통과시킨다.
   ============================================================ */
const VERSION = 'v1.0.0';
const CACHE   = 'sarang-office-' + VERSION;
const NAV_FALLBACK = './index.html';

/* 정적 셸 — 설치/첫 실행 때 미리 받아 둔다 */
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-192-maskable.png',
  './icon-512-maskable.png'
];

/* ── 설치 ───────────────────────────────────── */
self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    // 하나가 실패해도 설치 자체는 진행 (404·오프라인 대비)
    await Promise.all(SHELL.map(url =>
      cache.add(new Request(url, { cache: 'reload' })).catch(() => {})
    ));
    await self.skipWaiting();
  })());
});

/* ── 활성화: 이전 버전 캐시 정리 ──────────────── */
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys
      .filter(k => k.startsWith('sarang-office-') && k !== CACHE)
      .map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

/* ── 요청 처리: 같은 출처 GET만, 네트워크 우선 ── */
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;                       // Form POST 등은 그대로 통과

  let url;
  try { url = new URL(req.url); } catch (_) { return; }
  if (url.origin !== self.location.origin) return;        // Google Sheets/Forms = 항상 네트워크 직행
  if (url.pathname.indexOf('/pickle-executive-office/') !== 0) return;  // 이 앱 범위 밖은 건드리지 않음

  if (req.mode === 'navigate') {
    event.respondWith(navigationHandler(req));
    return;
  }
  event.respondWith(networkFirst(req));
});

async function networkFirst(req) {
  const cache = await caches.open(CACHE);
  try {
    const res = await fetch(req);
    if (res && res.ok && res.type === 'basic') {
      cache.put(req, res.clone()).catch(() => {});
    }
    return res;
  } catch (err) {
    const hit = await cache.match(req, { ignoreSearch: true });
    if (hit) return hit;
    throw err;
  }
}

async function navigationHandler(req) {
  const cache = await caches.open(CACHE);
  try {
    const res = await fetch(req);
    if (res && res.ok) cache.put(NAV_FALLBACK, res.clone()).catch(() => {});
    return res;
  } catch (err) {
    // 오프라인: ?as= 같은 쿼리와 무관하게 셸을 돌려준다
    const hit = await cache.match(NAV_FALLBACK) || await cache.match('./');
    if (hit) return hit;
    throw err;
  }
}
