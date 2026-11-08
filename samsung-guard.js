/* Family Hub - Samsung Internet install guard (Nov 8, 2026).
 * Installing these apps from Samsung Internet makes Google Play Protect show
 * "Unsafe app blocked - built for an older version of Android". Installing from Chrome does not.
 * On Samsung Internet (not already installed) this shows a banner with a one-tap "Open in Chrome" button.
 */
(function () {
  'use strict';
  var ua = navigator.userAgent || '';
  if (!/SamsungBrowser/i.test(ua) || !/Android/i.test(ua)) return;
  var standalone = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone;
  if (standalone) return;
  function draw() {
    if (!document.body || document.getElementById('fhSamsung')) return;
    var here = location.href.split('#')[0].replace(/^https?:\/\//, '');
    var chromeUrl = 'intent://' + here + '#Intent;scheme=https;package=com.android.chrome;S.browser_fallback_url=' +
      encodeURIComponent('https://play.google.com/store/apps/details?id=com.android.chrome') + ';end';
    var d = document.createElement('div'); d.id = 'fhSamsung';
    d.style.cssText = 'position:fixed;left:8px;right:8px;top:8px;z-index:2147483646;background:#fff8e3;color:#3d2e00;border:2px solid #c9a227;border-radius:14px;padding:12px 14px;font:14px/1.4 Arial,sans-serif;box-shadow:0 6px 20px rgba(0,0,0,.3)';
    d.innerHTML = '<b>Install this app from Chrome, not Samsung Internet.</b><br>Samsung Internet makes Google Play Protect block the app ("Unsafe app blocked"). Chrome installs it safely.' +
      '<div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap"><a id="fhOpenChrome" href="' + chromeUrl + '" style="background:#0b3d2e;color:#fff;text-decoration:none;font-weight:700;border-radius:10px;padding:9px 12px">Open in Chrome</a>' +
      '<button id="fhSamsungX" style="background:#e9e4d6;border:0;border-radius:10px;padding:9px 12px;font-weight:700">Not now</button></div>' +
      '<div style="font-size:12.5px;margin-top:8px">In Chrome: tap <b>⋮</b> (top right) → <b>Install app</b> or <b>Add to Home screen</b> → <b>Install</b>. If a blocked copy is on the phone, tap <b>Got it</b>, then press and hold its icon → <b>Uninstall</b>.</div>';
    document.body.appendChild(d);
    document.getElementById('fhSamsungX').onclick = function () { d.remove(); };
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', draw); else draw();
  window.addEventListener('load', draw);
})();
