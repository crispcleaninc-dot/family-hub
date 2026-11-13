/* Cyars Command Hub - service worker. Keeps the app files on the device so it opens offline.
   Buttons and PIN live in this device storage; the worker never sees them. */
try { importScripts('notify-sw.js'); } catch (e) {} // Cyars Notify: alerts + taps
var SHELL = 'cch-shell-v1';
var FILES = ['./notify.js', './notify-sw.js', './', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './icon-maskable-512.png', './apple-touch-icon.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(SHELL).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k.indexOf('cch-') === 0 && k !== SHELL; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  // network first so updates arrive; device copy when offline
  e.respondWith(fetch(req).then(function (r) {
    if (r && r.ok) { var cp = r.clone(); caches.open(SHELL).then(function (c) { c.put(req, cp); }); }
    return r;
  }).catch(function () {
    return caches.match(req, { ignoreSearch: true }).then(function (m) { return m || caches.match('./index.html'); });
  }));
});
