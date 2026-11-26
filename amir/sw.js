/* Amir's World - service worker. Keeps the app on the device so it opens offline. */
try { importScripts('notify-sw.js'); } catch (e) {} // Cyars Notify: alerts + taps
var SHELL = 'aw-shell-v2';
var FILES = ['./', './index.html', './config.js', './device.js', './notify.js', './notify-sw.js', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png', './andika-latin-400-normal.woff2', './andika-latin-700-normal.woff2', '../samsung-guard.js'];
self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(SHELL).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k.indexOf('aw-') === 0 && k !== SHELL; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var req = e.request; if (req.method !== 'GET') return;
  var url = new URL(req.url); if (url.origin !== self.location.origin) return;
  // network first so updates arrive; device copy when offline
  e.respondWith(fetch(req).then(function (r) {
    if (r && r.ok) { var cp = r.clone(); caches.open(SHELL).then(function (c) { c.put(req, cp); }); }
    return r;
  }).catch(function () { return caches.match(req, { ignoreSearch: true }).then(function (m) { return m || caches.match('./index.html'); }); }));
});
