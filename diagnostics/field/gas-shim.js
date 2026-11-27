/* Makes the Apps Script app run on GitHub.
   The app calls google.script.run.X(...) exactly as before. Here those calls go to the Mundo log relay
   (the same Apps Script backend: Sheets log, formatted Docs, Gmail batch, text-intake clients).
   If there is no signal or no relay yet, saved readings are kept on this phone and sent later — nothing is lost. */
(function () {
  var OUTBOX = 'mfd_outbox_v1', RELAY_KEY = 'mfd_relay_url';
  var FNS = ['submitReading', 'batchDailyEmail', 'listIntakeClients', 'markIntakeOnSite'];
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function relay() { return (get(RELAY_KEY) || window.MUNDO_RELAY_URL || '').trim(); }
  function outbox() { try { return JSON.parse(get(OUTBOX) || '[]'); } catch (e) { return []; } }
  function setOutbox(a) { put(OUTBOX, JSON.stringify(a)); fire(); }
  function fire() { try { window.dispatchEvent(new Event('mfd-status')); } catch (e) {} }
  function call(fn, args) {
    var url = relay();
    if (!url) return Promise.reject(new Error('NO_RELAY'));
    if (!navigator.onLine) return Promise.reject(new Error('OFFLINE'));
    return fetch(url, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify({ fn: fn, args: args }) })
      .then(function (r) { return r.text(); })
      .then(function (t) { var j; try { j = JSON.parse(t); } catch (e) { throw new Error('The Mundo log link did not answer correctly. Check the link (it must end in /exec).'); }
        if (!j.ok) throw new Error(j.error || 'Mundo log error'); return j.result; });
  }
  function runner(ok, fail) {
    var r = {
      withSuccessHandler: function (f) { return runner(f, fail); },
      withFailureHandler: function (f) { return runner(ok, f); }
    };
    FNS.forEach(function (fn) {
      r[fn] = function () {
        var args = Array.prototype.slice.call(arguments);
        if (fn === 'submitReading' && args[0]) { try {
          var n = new Date(), pad = function (x) { return ('0' + x).slice(-2); };
          var rid = 'SR-' + String(n.getFullYear()).slice(2) + pad(n.getMonth() + 1) + pad(n.getDate()) + '-' + pad(n.getHours()) + pad(n.getMinutes()) + pad(n.getSeconds());
          var rs = JSON.parse(get('mfd_reports_v1') || '[]'); rs.push({ id: rid, at: n.toISOString(), d: args[0] });
          put('mfd_reports_v1', JSON.stringify(rs.slice(-200))); window.MFD_LAST_REPORT = rid; args[0].reportId = rid;
        } catch (e) {} }
        call(fn, args).then(function (res) { ok && ok(res); }).catch(function (err) {
          var why = err && err.message;
          if (fn === 'submitReading' && (why === 'NO_RELAY' || why === 'OFFLINE' || /fetch|network|Failed/i.test(why || ''))) {
            var q = outbox(); q.push({ at: new Date().toISOString(), args: args }); setOutbox(q);
            ok && ok('saved on this phone (' + q.length + ' waiting). It goes to the Mundo log automatically ' + (why === 'NO_RELAY' ? 'once the Mundo log connection is set (Job Info page).' : 'when you have signal.'));
            return;
          }
          var msg = why === 'NO_RELAY' ? 'The Mundo log connection is not set yet (Job Info page → Mundo log connection).' :
                    why === 'OFFLINE' ? 'No signal right now — try again when you are back online.' : why;
          fail && fail(new Error(msg));
        });
      };
    });
    return r;
  }
  window.google = window.google || {};
  window.google.script = window.google.script || {};
  Object.defineProperty(window.google.script, 'run', { get: function () { return runner(null, null); }, configurable: true });

  var flushing = false;
  function flush() {
    if (flushing || !relay() || !navigator.onLine) return;
    var q = outbox(); if (!q.length) return;
    flushing = true;
    (function next() {
      var q2 = outbox(); if (!q2.length) { flushing = false; return; }
      call('submitReading', q2[0].args).then(function () { var q3 = outbox(); q3.shift(); setOutbox(q3); next(); })
        .catch(function () { flushing = false; fire(); });
    })();
  }
  window.MFD = { relay: relay, setRelay: function (u) { put(RELAY_KEY, (u || '').trim()); fire(); flush(); }, outbox: outbox, flush: flush };
  window.addEventListener('online', flush);
  window.addEventListener('load', function () { setTimeout(flush, 1500); });
})();
