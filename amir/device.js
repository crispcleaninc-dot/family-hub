/* Amir's World - device helper (Nov 26, 2026).
 * Loaded in <head> before the app's own scripts.
 *  1. AI through the relay: if config.js has AMIR_RELAY, calls the app makes to the Claude API go through
 *     Mom's Apps Script instead, so no key has to be saved on the tablet. With no relay, the app's
 *     original "save a key with the gear button" method still works exactly as before.
 *  2. Cloud backup: gives the app's existing "Saved to Mom's Google account" code a way to reach the
 *     same Apps Script from the installed app (it used google.script.run, which only exists inside Apps Script).
 *  3. Amir's photo is kept on this device only (not in the public app files). Grown-ups add or change it.
 *  4. Install button, offline copy (sw.js).
 */
(function () {
  'use strict';
  var RELAY = String(window.AMIR_RELAY || '').trim();
  var API = 'https://api.anthropic.com/v1/messages';
  window.AMIR_HAS_RELAY = !!RELAY;

  function post(payload) {
    // text/plain keeps it a "simple" request, so Apps Script answers without a CORS preflight
    return fetch(RELAY, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload) })
      .then(function (r) { return r.json(); });
  }

  /* ---------- 1. AI through the relay ---------- */
  if (RELAY) {
    var realFetch = window.fetch.bind(window);
    window.fetch = function (input, init) {
      var u = typeof input === 'string' ? input : (input && input.url) || '';
      if (u.indexOf(API) !== 0) return realFetch(input, init);
      var body = {}; try { body = JSON.parse((init && init.body) || '{}'); } catch (e) {}
      return post({ action: 'ai', messages: body.messages || [], max_tokens: body.max_tokens || 800 }).then(function (out) {
        if (!out || !out.ok) {
          var msg = (out && (out.error === 'daily_limit' ? 'Daily AI limit reached. Try again tomorrow.' : out.error)) || 'relay error';
          return new Response(JSON.stringify({ error: { message: msg } }), { status: 500, headers: { 'Content-Type': 'application/json' } });
        }
        return new Response(JSON.stringify(out.data), { status: 200, headers: { 'Content-Type': 'application/json' } });
      });
    };
    // The app checks for a saved key before AI lessons; with the relay none is needed.
    try { if (!localStorage.getItem('amir_claude_key')) localStorage.setItem('amir_claude_key', 'sk-ant-relay'); } catch (e) {}
  } else {
    try { if (localStorage.getItem('amir_claude_key') === 'sk-ant-relay') localStorage.removeItem('amir_claude_key'); } catch (e) {}
  }

  /* ---------- 2. Cloud backup (same calls the Apps Script version made) ---------- */
  if (RELAY && !(window.google && google.script && google.script.run)) {
    var makeRunner = function () {
      var ok = function () {}, bad = function () {};
      var r = {
        withSuccessHandler: function (f) { ok = f || ok; return r; },
        withFailureHandler: function (f) { bad = f || bad; return r; },
        loadProgress: function () { post({ action: 'loadProgress' }).then(function (o) { o && o.ok ? ok(o.data) : bad(o); }).catch(bad); },
        saveProgress: function (d) { post({ action: 'saveProgress', data: d }).then(function (o) { o && o.ok ? ok(o) : bad(o); }).catch(bad); }
      };
      return r;
    };
    var run = {};
    ['withSuccessHandler', 'withFailureHandler', 'loadProgress', 'saveProgress'].forEach(function (k) {
      run[k] = function () { var x = makeRunner(); return x[k].apply(x, arguments); };
    });
    window.google = window.google || {}; google.script = google.script || {}; google.script.run = run;
  }

  /* ---------- 3. Photo kept on this device ---------- */
  var PHOTO_KEY = 'amir_photo_v1';
  function showPhoto() {
    var img = document.getElementById('amirPhoto'); if (!img) return;
    var p = null; try { p = localStorage.getItem(PHOTO_KEY); } catch (e) {}
    if (p) img.src = p;
  }
  function pickPhoto(file, done) {
    if (!file) return;
    var fr = new FileReader();
    fr.onload = function () {
      var im = new Image();
      im.onload = function () {
        var s = 360, c = document.createElement('canvas'); c.width = s; c.height = s;
        var m = Math.min(im.width, im.height), x = (im.width - m) / 2, y = (im.height - m) / 2;
        c.getContext('2d').drawImage(im, x, y, m, m, 0, 0, s, s);
        var url = c.toDataURL('image/jpeg', 0.82);
        try { localStorage.setItem(PHOTO_KEY, url); } catch (e) { alert('Could not save the photo on this device.'); return; }
        showPhoto(); done && done(true);
      };
      im.src = fr.result;
    };
    fr.readAsDataURL(file);
  }

  /* ---------- 4. Install + offline ---------- */
  var deferred = null;
  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault(); deferred = e;
    var b = document.getElementById('awInstall'); if (b) b.classList.remove('aw-hide');
  });
  window.addEventListener('appinstalled', function () { var b = document.getElementById('awInstall'); if (b) b.classList.add('aw-hide'); });
  if ('serviceWorker' in navigator && location.protocol === 'https:') {
    window.addEventListener('load', function () { navigator.serviceWorker.register('sw.js').catch(function () {}); });
  }

  function status() {
    var el = document.getElementById('awStatus'); if (!el) return;
    var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
    el.innerHTML = (standalone ? '✅ Installed on this device. Works offline.' : 'Not installed yet on this device.') + '<br>' +
      (RELAY ? '🤖 AI lessons: on (through Mom’s Google account, no key needed).' : '🤖 AI lessons: need a key saved with the ⚙️ button (or Mom turns on the relay).') + '<br>' +
      (RELAY ? '☁️ Progress backs up to Mom’s Google account.' : '💾 Progress is saved on this device.');
  }

  document.addEventListener('DOMContentLoaded', function () {
    showPhoto();
    var b = document.getElementById('awInstall');
    if (b) {
      if (deferred) b.classList.remove('aw-hide');
      b.onclick = function () {
        if (!deferred) return;
        deferred.prompt(); Promise.resolve(deferred.userChoice).catch(function () {}).then(function () { deferred = null; b.classList.add('aw-hide'); });
      };
    }
    var f = document.getElementById('awPhotoFile');
    if (f) f.addEventListener('change', function () { pickPhoto(f.files[0], function () { status(); try { speak('Hi Amir! There you are!', 0.85, 1.3); } catch (e) {} }); f.value = ''; });
    var rm = document.getElementById('awPhotoRemove');
    if (rm) rm.onclick = function () {
      if (!confirm('Remove Amir’s photo from this device?')) return;
      try { localStorage.removeItem(PHOTO_KEY); } catch (e) {}
      var img = document.getElementById('amirPhoto'); if (img) img.src = img.getAttribute('data-default');
    };
    status();
  });
})();
