/* Caleb #56 Athlete OS - service worker (V2.27). Keeps the app shell, fonts and photos on the phone. */
var SHELL = 'c56-shell-v4', RUNTIME = 'c56-runtime-v1';
var FILES = ['./', './index.html', './sync.js', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(SHELL).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k !== SHELL && k !== RUNTIME && k !== 'c56-app'; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;                       // backend calls (POST) go straight to the network
  var url = new URL(req.url);
  if (url.hostname === 'script.google.com' || (url.hostname.endsWith('googleusercontent.com') && url.pathname.indexOf('/macros/') === 0)) return;
  if (req.headers.has('range') || req.destination === 'video' || req.destination === 'audio') return; // videos stream, too big to keep
  if (url.origin === self.location.origin) {
    // app files: network first so updates arrive, phone copy when offline
    e.respondWith(fetch(req).then(function (r) {
      if (r && r.ok) { var cp = r.clone(); caches.open(SHELL).then(function (c) { c.put(req, cp); }); }
      return r;
    }).catch(function () { return caches.match(req, { ignoreSearch: true }).then(function (m) { return m || caches.match('./index.html'); }); }));
    return;
  }
  // fonts, photos, thumbnails: phone copy first, refresh in the background
  e.respondWith(caches.open(RUNTIME).then(function (c) {
    return c.match(req).then(function (hit) {
      var net = fetch(req).then(function (r) { if (r && (r.ok || r.type === 'opaque')) c.put(req, r.clone()); return r; }).catch(function () { return hit; });
      return hit || net;
    });
  }));
});
