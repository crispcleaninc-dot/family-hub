/* Family Hub - makes the hub installable as ONE app. Network first so updates arrive; saved copy when offline.
   Each app inside the hub (School & Chores, Language Lab, Math Coach...) keeps its own offline copy too. */
var SHELL = 'hub-shell-v1';
var FILES = ['./', './index.html', './manifest.webmanifest', './hub-icon-192.png', './hub-icon-512.png'];
self.addEventListener('install', function (e) { e.waitUntil(caches.open(SHELL).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); })); });
self.addEventListener('activate', function (e) { e.waitUntil(caches.keys().then(function (ks) { return Promise.all(ks.filter(function (k) { return k.indexOf('hub-shell-') === 0 && k !== SHELL; }).map(function (k) { return caches.delete(k); })); }).then(function () { return self.clients.claim(); })); });
self.addEventListener('fetch', function (e) {
  var req = e.request; if (req.method !== 'GET') return;
  var url = new URL(req.url); if (url.origin !== self.location.origin) return;
  // only the hub's own home page files; apps in sub-folders handle themselves
  var p = url.pathname.replace(/\/+$/, '/'); var base = new URL('./', self.location.href).pathname;
  if (!(p === base || p === base + 'index.html')) return;
  e.respondWith(fetch(req).then(function (r) { if (r && r.ok) { var cp = r.clone(); caches.open(SHELL).then(function (c) { c.put(req, cp); }); } return r; })
    .catch(function () { return caches.match(req, { ignoreSearch: true }).then(function (m) { return m || caches.match('./index.html'); }); }));
});
