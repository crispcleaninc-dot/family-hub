/* Caleb #56 + Cyars Notify: tells family who turned on notifications when a new version of the app arrives. */
(function () {
  var tries = 0;
  (function wait() {
    if (!window.CyarsNotify) { if (++tries < 40) setTimeout(wait, 500); return; }
    var v = ''; try { v = localStorage.getItem('c56_upd') || ''; } catch (e) {}
    if (!v) return;
    try { localStorage.removeItem('c56_upd'); } catch (e) {}
    CyarsNotify.announce('Caleb #56 Athlete OS was updated', 'New version ' + v + ' is ready. Tap to see the latest.', location.origin + location.pathname);
  })();
})();
