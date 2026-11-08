/* Caleb #56 Athlete OS - offline engine (V2.27).
 * Stands in for google.script.run when the app runs as an installed phone app.
 *  - Online: every call goes to the Apps Script backend (doPost) and the answer is saved on the device.
 *  - Offline: reads come from the saved copy; changes are saved on the device, shown right away,
 *    and sent to the backend in order as soon as the phone is back online.
 *  - AI, email-sending, Gmail scans and web searches need internet; offline they say so instead of failing silently.
 */
(function () {
  'use strict';
  var BACKEND = 'https://script.google.com/macros/s/AKfycbzs6GRRlaUWHeIrAx3PGGT9y_S5X2n9TeoLWHdt4OEeuofmkJytbKTcnF2D-rLbqBMwMA/exec';
  var DBN = 'caleb56-offline', VER = 1;
  var READS = ['boot', 'list', 'publicList', 'publicProfile', 'getProfile', 'getSettings', 'emailSettings', 'galleryData', 'scPhotos', 'scStats', 'scNext',
    'wholeAthleteHero', 'weightSummary', 'weeklyReport', 'spainInfo', 'spainAdmin', 'opAll', 'ctPublic', 'ctAll', 'ideaList', 'socialGet', 'contentSources', 'upcoming', 'frPublic', 'frGet'];
  var WRITES = ['add', 'update', 'delete', 'publicAdd', 'spainPledge', 'spainSave', 'spainMark', 'opSave', 'opSettings', 'opUpload', 'saveProfile', 'saveSettings',
    'saveEmailSettings', 'socialSave', 'ctSave', 'ctSaveSettings', 'ctEnter', 'ctSponsorUp', 'ctLeadAdd', 'ctScore', 'iqLog', 'modSet', 'modDelete',
    'scSaveGraphic', 'galleryUpload'];
  // after a write, which saved read best shows the new state
  var MIRROR = { spainPledge: 'spainInfo', spainSave: 'spainAdmin', spainMark: 'spainAdmin', opSave: 'opAll', opSettings: 'opAll', opUpload: 'opAll',
    ctSave: 'ctAll', ctSaveSettings: 'ctAll', ctLeadAdd: 'ctAll', ctScore: 'ctAll', ctEnter: 'ctPublic', ctSponsorUp: 'ctPublic', socialSave: 'socialGet',
    saveProfile: 'getProfile', saveSettings: 'getSettings', saveEmailSettings: 'emailSettings' };

  // ---------------------------------------------------------------- tiny IndexedDB store
  var dbp = null;
  function db() {
    if (dbp) return dbp;
    dbp = new Promise(function (res, rej) {
      var r = indexedDB.open(DBN, VER);
      r.onupgradeneeded = function () { var d = r.result; if (!d.objectStoreNames.contains('kv')) d.createObjectStore('kv'); if (!d.objectStoreNames.contains('q')) d.createObjectStore('q', { keyPath: 'n', autoIncrement: true }); };
      r.onsuccess = function () { res(r.result); }; r.onerror = function () { rej(r.error); };
    });
    return dbp;
  }
  function tx(store, mode, fn) { return db().then(function (d) { return new Promise(function (res, rej) { var t = d.transaction(store, mode), s = t.objectStore(store), out; out = fn(s); t.oncomplete = function () { res(out && typeof IDBRequest !== 'undefined' && out instanceof IDBRequest ? out.result : out); }; t.onerror = function () { rej(t.error); }; }); }); }
  function kget(k) { return tx('kv', 'readonly', function (s) { return s.get(k); }); }
  function kset(k, v) { return tx('kv', 'readwrite', function (s) { s.put(v, k); }); }
  function qall() { return tx('q', 'readonly', function (s) { return s.getAll(); }); }
  function qadd(v) { return tx('q', 'readwrite', function (s) { s.add(v); }); }
  function qput(v) { return tx('q', 'readwrite', function (s) { s.put(v); }); }
  function qdel(n) { return tx('q', 'readwrite', function (s) { s.delete(n); }); }

  // ---------------------------------------------------------------- helpers
  var S = window.C56 = { online: navigator.onLine, pending: 0, syncing: false, lastSync: '', adminHash: '' };
  function clean(p) { var o = {}; Object.keys(p || {}).sort().forEach(function (k) { if (k !== 'pin') o[k] = p[k]; }); return o; }
  function key(action, p) { return (p && p.pin ? 'A:' : 'P:') + action + ':' + JSON.stringify(clean(p)); }
  function hash(s) { var b = new TextEncoder().encode('c56|' + s); return crypto.subtle.digest('SHA-256', b).then(function (h) { return Array.from(new Uint8Array(h)).map(function (x) { return ('0' + x.toString(16)).slice(-2); }).join(''); }); }
  function post(body, ms) {
    var ctl = ('AbortController' in window) ? new AbortController() : null;
    var to = ctl ? setTimeout(function () { ctl.abort(); }, ms || 30000) : null;
    return fetch(BACKEND, { method: 'POST', body: JSON.stringify(body), headers: { 'Content-Type': 'text/plain;charset=utf-8' }, redirect: 'follow', credentials: 'omit', signal: ctl ? ctl.signal : undefined })
      .then(function (r) { if (to) clearTimeout(to); if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
      .catch(function (e) { if (to) clearTimeout(to); var x = new Error('NETWORK'); x.net = true; x.why = String(e && e.message || e); throw x; });
  }
  S.post = post;
  function ok(d) { return JSON.stringify({ ok: true, data: d }); }
  function bad(m) { return JSON.stringify({ ok: false, error: m }); }
  function tempId() { return 'local-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }

  // optimistic change to every saved list of that module, admin and family copies
  function patchLists(action, p) {
    var mod = p.module; if (!mod) return Promise.resolve();
    var keys = [key('list', { module: mod, pin: 1 }), key('publicList', { module: mod })];
    return Promise.all(keys.map(function (k) {
      return kget(k).then(function (raw) {
        if (!raw) return; var r; try { r = JSON.parse(raw); } catch (e) { return; } if (!r.ok || !Array.isArray(r.data)) return;
        if (action === 'add' || action === 'publicAdd') { var row = Object.assign({}, p.data || {}); row.ID = p._tid; row.Created = new Date().toISOString().slice(0, 10); r.data.push(row); }
        if (action === 'update') r.data = r.data.map(function (x) { return String(x.ID) === String(p.id) ? Object.assign({}, x, p.data || {}) : x; });
        if (action === 'delete') r.data = r.data.filter(function (x) { return String(x.ID) !== String(p.id); });
        return kset(k, JSON.stringify(r));
      });
    }));
  }

  function queueWrite(action, p) {
    var job = { action: action, payload: p, at: new Date().toISOString() };
    var chain = Promise.resolve();
    if ((action === 'update' || action === 'delete') && String(p.id || '').indexOf('local-') === 0) {
      // the row was made offline and is still waiting: fold this change into it
      chain = qall().then(function (all) {
        var j = all.filter(function (x) { return (x.action === 'add' || x.action === 'publicAdd') && x.payload._tid === p.id; })[0];
        if (!j) return qadd(job);
        if (action === 'delete') return qdel(j.n);
        j.payload.data = Object.assign({}, j.payload.data || {}, p.data || {}); return qput(j);
      });
    } else {
      if (action === 'add' || action === 'publicAdd') p._tid = tempId();
      chain = qadd(job);
    }
    return chain.then(function () { return patchLists(action, p); }).then(count).then(function () {
      if (action === 'add' || action === 'publicAdd' || action === 'update' || action === 'delete') return ok({ ok: true, offline: true, id: p._tid || p.id });
      var m = MIRROR[action];
      if (!m) return ok({ ok: true, offline: true });
      return kget(key(m, p.pin ? { pin: 1 } : {})).then(function (raw) { if (raw) { try { var r = JSON.parse(raw); if (r.ok) return ok(r.data); } catch (e) {} } return ok({ ok: true, offline: true }); });
    });
  }

  function offlineAnswer(action, p) {
    if (action === 'verifyPin') {
      return hash(String(p.pin || '')).then(function (h) { return kget('adminHash').then(function (saved) { return saved && saved === h ? ok({ ok: true, offline: true }) : bad(saved ? 'Wrong PIN.' : 'Admin login needs internet the first time on this phone.'); }); });
    }
    if (WRITES.indexOf(action) > -1) return queueWrite(action, p);
    return kget(key(action, p)).then(function (raw) {
      if (raw) return raw;
      if (READS.indexOf(action) > -1) return action === 'list' || action === 'publicList' ? ok([]) : bad('Not saved on this phone yet. Open this screen once while online and it will work offline after that.');
      return bad('You are offline. This part uses AI, email or the web, so it needs internet. Everything you type in other screens is saved and will sync when you are back online.');
    });
  }

  function runCall(action, p) {
    p = p || {};
    if (!navigator.onLine) return offlineAnswer(action, p);
    return pendingCount().then(function (n) {
      // keep order: if changes are waiting, send them first
      return n && WRITES.indexOf(action) > -1 ? queueWrite(action, p).then(function (r) { S.sync(); return r; }) : null;
    }).then(function (queued) {
      if (queued) return queued;
      return post({ action: action, payload: p }).then(function (raw) {
        var r; try { r = JSON.parse(raw); } catch (e) { return raw; }
        if (r.ok) {
          if (READS.indexOf(action) > -1) kset(key(action, p), raw);
          if (action === 'verifyPin') hash(String(p.pin || '')).then(function (h) { kset('adminHash', h); setTimeout(function () { S.prefetch(String(p.pin)); }, 1500); });
          if (WRITES.indexOf(action) > -1) refreshAfterWrite(p);
        }
        return raw;
      }, function (e) { if (e.net) { setOnline(false); return offlineAnswer(action, p); } throw e; });
    });
  }
  function refreshAfterWrite(p) { if (p.module) { var pin = p.pin; setTimeout(function () { runCall('publicList', { module: p.module }); if (pin) runCall('list', { module: p.module, pin: pin }); }, 300); } }

  // ---------------------------------------------------------------- google.script.* stand-in
  function Runner() { this._s = null; this._f = null; }
  Runner.prototype.withSuccessHandler = function (f) { this._s = f; return this; };
  Runner.prototype.withFailureHandler = function (f) { this._f = f; return this; };
  Runner.prototype.withUserObject = function () { return this; };
  Runner.prototype.api = function (action, payload) {
    var s = this._s, f = this._f;
    runCall(action, payload).then(function (raw) { if (s) s(raw); }, function (e) { if (f) f(e); });
  };
  window.google = window.google || {};
  window.google.script = {
    get run() { return new Runner(); },
    url: { getLocation: function (cb) { var q = {}; new URLSearchParams(location.search).forEach(function (v, k) { q[k] = v; }); setTimeout(function () { cb({ parameter: q, parameters: q, hash: location.hash.slice(1) }); }, 0); } },
    host: { close: function () {}, setHeight: function () {}, setWidth: function () {}, editor: {} }
  };

  // ---------------------------------------------------------------- sync
  function pendingCount() { return qall().then(function (a) { return a.length; }, function () { return 0; }); }
  function count() { return pendingCount().then(function (n) { S.pending = n; paint(); return n; }); }
  S.sync = function () {
    if (S.syncing || !navigator.onLine) return Promise.resolve();
    S.syncing = true; paint();
    var touched = {};
    function step() {
      return qall().then(function (all) {
        if (!all.length) return 'done';
        var j = all[0], p = Object.assign({}, j.payload); var tid = p._tid; delete p._tid;
        return post({ action: j.action, payload: p }).then(function (raw) {
          var r; try { r = JSON.parse(raw); } catch (e) { r = { ok: false, error: 'bad reply' }; }
          if (p.module) touched[p.module + '|' + (p.pin || '')] = { module: p.module, pin: p.pin };
          if (!r.ok) return kget('syncErrors').then(function (x) { x = x || []; x.push({ at: new Date().toISOString(), action: j.action, error: r.error, payload: clean(p) }); return kset('syncErrors', x.slice(-50)); });
        }).then(function () { return qdel(j.n); }).then(count).then(step);
      });
    }
    return step().then(function () {
      S.lastSync = new Date().toLocaleTimeString(); S.syncing = false; paint();
      Object.keys(touched).forEach(function (k) { var t = touched[k]; runCall('publicList', { module: t.module }); if (t.pin) runCall('list', { module: t.module, pin: t.pin }); });
      try { if (window.show && document.querySelector('nav button.active')) { var a = document.querySelector('nav button.active'); if (a && a.dataset.k && !document.activeElement.matches('input,textarea,select')) window.show(a.dataset.k); } } catch (e) {}
    }, function (e) { S.syncing = false; if (e && e.net) setOnline(false); paint(); });
  };

  // save the main screens on the phone so they open offline
  S.prefetch = function (pin) {
    var jobs = [['boot', {}], ['upcoming', {}], ['publicProfile', {}], ['galleryData', {}], ['spainInfo', {}], ['ctPublic', {}], ['frPublic', {}], ['wholeAthleteHero', {}], ['scPhotos', {}], ['scStats', {}]];
    ['Schedule', 'Track', 'Specs', 'WholeAthlete', 'Film', 'FilmReviewers', 'FilmReviews', 'Family', 'Faith', 'Updates'].forEach(function (m) { jobs.push(['publicList', { module: m }]); });
    var go = function (mods) {
      if (pin) {
        (mods || []).forEach(function (m) { jobs.push(['list', { module: m, pin: pin }]); });
        ['getProfile', 'getSettings', 'emailSettings', 'spainAdmin', 'opAll', 'ctAll', 'ideaList', 'socialGet', 'weightSummary', 'frGet'].forEach(function (a) { jobs.push([a, { pin: pin }]); });
      }
      var i = 0; (function next() { if (i >= jobs.length || !navigator.onLine) { kset('prefetchedAt', new Date().toISOString()); paint(); return; } var j = jobs[i++]; runCall(j[0], j[1]).then(next, next); })();
    };
    if (pin) kget(key('boot', {})).then(function (raw) { var m = []; try { m = JSON.parse(raw).data.modules || []; } catch (e) {} go(m); }); else go([]);
  };

  // ---------------------------------------------------------------- status pill
  function setOnline(v) { if (S.online !== v) { S.online = v; paint(); if (v) S.sync(); } }
  window.addEventListener('online', function () { setOnline(true); });
  window.addEventListener('offline', function () { setOnline(false); });
  setInterval(function () { if (navigator.onLine && S.pending && !S.syncing) S.sync(); }, 30000);
  function paint() {
    if (!document.body) return;
    var el = document.getElementById('c56pill');
    if (!el) {
      el = document.createElement('button'); el.id = 'c56pill'; el.type = 'button';
      el.style.cssText = 'position:fixed;left:10px;bottom:10px;z-index:99998;border:none;border-radius:16px;padding:6px 11px;font:bold 11px Arial,sans-serif;box-shadow:0 3px 10px rgba(0,0,0,.3);cursor:pointer';
      el.onclick = function () { if (navigator.onLine) { S.sync(); S.prefetch(window.APP && APP.pin ? APP.pin : ''); el.textContent = 'Saving for offline...'; } else alert('You are offline. ' + (S.pending ? S.pending + ' change(s) are saved on this phone and will sync when you are back online.' : 'Everything you open or change is saved on this phone.')); };
      document.body.appendChild(el);
    }
    var on = navigator.onLine && S.online !== false;
    el.style.background = on ? (S.pending ? '#c9a227' : '#0b3d2e') : '#7a1010';
    el.style.color = on && !S.pending ? '#c9a227' : '#fff';
    el.textContent = S.syncing ? 'Syncing ' + S.pending + '...' : on ? (S.pending ? S.pending + ' to sync - tap' : 'Online - synced') : 'Offline' + (S.pending ? ' - ' + S.pending + ' saved, will sync' : ' - working from this phone');
  }
  S.paint = paint;
  document.addEventListener('DOMContentLoaded', function () { count(); paint(); if (navigator.onLine) { S.sync(); setTimeout(function () { S.prefetch(''); }, 4000); } });
  count();
})();

/* install helper: shows an "Install app" button in the browser (not once installed) */
(function () {
  'use strict';
  var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
  if (standalone) return;
  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (e) { e.preventDefault(); deferred = e; draw(); });
  function draw() {
    if (!document.body || document.getElementById('c56inst')) return;
    var b = document.createElement('button'); b.id = 'c56inst'; b.type = 'button';
    b.style.cssText = 'position:fixed;right:10px;bottom:10px;z-index:99998;border:none;border-radius:16px;padding:7px 12px;font:bold 12px Arial,sans-serif;background:#c9a227;color:#222;box-shadow:0 3px 10px rgba(0,0,0,.3)';
    b.textContent = 'Install app';
    b.onclick = function () {
      if (deferred) { deferred.prompt(); deferred.userChoice.then(function () { deferred = null; b.remove(); }); return; }
      alert(/iphone|ipad|ipod/i.test(navigator.userAgent)
        ? 'iPhone: tap the Share button (square with the arrow) in Safari, then "Add to Home Screen".'
        : 'Open the browser menu (three dots) and tap "Install app" or "Add to Home screen".');
    };
    document.body.appendChild(b);
  }
  document.addEventListener('DOMContentLoaded', function () { if (/iphone|ipad|ipod/i.test(navigator.userAgent)) draw(); });
})();

/* V2.33 MISSIONS: "My Missions" button - opens Caleb's task app (missions/) inside this same installed app */
(function () {
  'use strict';
  function draw() {
    if (!document.body || document.getElementById('c56miss')) return;
    var a = document.createElement('a'); a.id = 'c56miss'; a.href = 'missions/';
    a.style.cssText = 'position:fixed;right:10px;bottom:52px;z-index:99998;border-radius:16px;padding:8px 12px;font:bold 12px Arial,sans-serif;background:#0b3d2e;color:#c9a227;border:2px solid #c9a227;text-decoration:none;box-shadow:0 3px 10px rgba(0,0,0,.3)';
    a.textContent = '🎯 My Missions';
    document.body.appendChild(a);
  }
  document.addEventListener('DOMContentLoaded', draw);
  if (document.readyState !== 'loading') draw();
})();
