/* Crispus Diagnostics — GitHub additions to the Field app (added Nov 27, 2026). Nothing above was changed.
   1) Mundo log connection card (status, link, readings waiting on this phone)
   2) Fill Job Info from a workplace (e.g. the Beztak sign-in set up in Property Maintenance & Grounds)
   3) Job Info stays filled between visits + "New job" button (keeps the technician)
   4) Device job register: every reading saved from this phone is listed on Job Info
   5) Nav button to Property Maintenance & Grounds, install + offline */
(function () {
  function $(id) { return document.getElementById(id); }
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  var JB = document.getElementById('v-jb'); if (!JB) return;

  var css = document.createElement('style');
  css.textContent = '.fx-card{border:1px solid var(--line);border-radius:10px;padding:12px;margin:0 0 12px;background:var(--panel)}' +
    '.fx-card h4{margin:0 0 6px;font-size:14px;color:var(--ok)}.fx-row{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:8px}' +
    '.fx-row input,.fx-row select{flex:1 1 180px;min-width:0;padding:8px;border-radius:6px;border:1px solid var(--line);background:transparent;color:inherit}' +
    '.fx-btn{padding:8px 12px;border-radius:6px;border:1px solid var(--ok);background:transparent;color:var(--ok);font-weight:600}' +
    '.fx-dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:middle}' +
    '.fx-reg{font-size:13px;line-height:1.5;max-height:220px;overflow:auto;margin-top:6px}.fx-reg div{border-bottom:1px solid var(--line);padding:4px 0}' +
    '.fx-small{font-size:12px;color:var(--dim)}';
  document.head.appendChild(css);

  /* ---------- 1) connection card ---------- */
  var conn = document.createElement('div'); conn.className = 'fx-card'; conn.id = 'fx-conn';
  JB.insertBefore(conn, JB.firstChild);
  function drawConn() {
    var url = window.MFD ? MFD.relay() : '', q = window.MFD ? MFD.outbox().length : 0;
    var on = !!url && navigator.onLine;
    conn.innerHTML = '<h4>Mundo log connection</h4>' +
      '<div><span class="fx-dot" style="background:' + (on ? 'var(--ok)' : (url ? 'var(--warn)' : 'var(--bad)')) + '"></span>' +
      (url ? (navigator.onLine ? 'Connected — readings go straight to the Mundo log in Drive.' : 'No signal — readings are saved on this phone.') : 'Not connected yet — readings are saved on this phone until the link is set.') +
      (q ? ' <b>' + q + ' reading' + (q > 1 ? 's' : '') + ' waiting to send.</b>' : '') + '</div>' +
      '<details' + (url ? '' : ' open') + '><summary class="fx-small" style="margin-top:6px">Mundo log link</summary>' +
      '<div class="fx-row"><input id="fx-url" placeholder="https://script.google.com/macros/s/…/exec" value="' + esc(url) + '"><button class="fx-btn" id="fx-save">Save link</button>' +
      (q ? '<button class="fx-btn" id="fx-send">Send waiting now</button>' : '') + '</div></details>';
    $('fx-save').onclick = function () { var u = $('fx-url').value.trim(); if (u && !/^https:\/\/script\.google\.com\/macros\/s\/.+\/exec$/.test(u)) { alert('That link should start with https://script.google.com/macros/s/ and end in /exec'); return; } MFD.setRelay(u); alert(u ? 'Saved. Waiting readings will send now.' : 'Link cleared.'); };
    if ($('fx-send')) $('fx-send').onclick = function () { MFD.flush(); };
  }
  window.addEventListener('mfd-status', drawConn); window.addEventListener('online', drawConn); window.addEventListener('offline', drawConn);
  drawConn();

  /* ---------- 3) Job Info stays filled + New job ---------- */
  var KEEP = 'mfd_jobinfo_v1';
  var fields = Array.prototype.slice.call(JB.querySelectorAll('input[id],select[id],textarea[id]')).filter(function (el) { return !/^(ti-|fx-)/.test(el.id); });
  try { var saved = JSON.parse(get(KEEP) || '{}'); fields.forEach(function (el) { if (saved[el.id] != null && !el.value) el.value = saved[el.id]; }); } catch (e) {}
  if (typeof window.npSync === 'function') { try { npSync(); } catch (e) {} }
  function keep() { var o = {}; fields.forEach(function (el) { o[el.id] = el.value; }); put(KEEP, JSON.stringify(o)); }
  fields.forEach(function (el) { el.addEventListener('input', keep); el.addEventListener('change', keep); });

  /* ---------- 2) fill from a workplace ---------- */
  var wp = document.createElement('div'); wp.className = 'fx-card';
  var profs = []; try { profs = (JSON.parse(get('pmg_data_v1') || '{}').profiles || []); } catch (e) {}
  wp.innerHTML = '<h4>Start a job</h4><div class="fx-row">' +
    (profs.length ? '<select id="fx-wp"><option value="">Fill from a workplace…</option>' + profs.map(function (p, i) { return '<option value="' + i + '">' + (p.kind === 'property' ? '🏢 ' : '👤 ') + esc(p.name) + '</option>'; }).join('') + '</select><button class="fx-btn" id="fx-fill">Fill in</button>' : '') +
    '<button class="fx-btn" id="fx-new" style="border-color:var(--warn);color:var(--warn)">New job</button></div>' +
    '<div class="fx-small" style="margin-top:6px">Job Info stays filled on this phone between visits. <b>New job</b> clears the customer and nameplate and keeps your technician name.' + (profs.length ? '' : ' Workplaces you set up in Property Maintenance &amp; Grounds show up here.') + '</div>';
  conn.parentNode.insertBefore(wp, conn.nextSibling);
  function setv(id, v) { var el = $(id); if (el && v != null && v !== '') { el.value = v; el.dispatchEvent(new Event('input')); } }
  if ($('fx-fill')) $('fx-fill').onclick = function () {
    var p = profs[+$('fx-wp').value]; if (!p) { alert('Pick a workplace first.'); return; }
    setv('jb-cid', [p.company, p.empId].filter(Boolean).join(' · ') || p.name);
    setv('jb-client', p.kind === 'property' ? (p.site || p.name) : '');
    setv('jb-loc', p.addr || ''); setv('jb-tech', p.tech || '');
    var u = prompt('Unit or equipment tag for this job? (optional)', ''); if (u) setv('jb-eqid', u);
    keep(); alert('Filled in from ' + p.name + '.');
  };
  $('fx-new').onclick = function () {
    if (!confirm('Start a new job? This clears the customer and nameplate on this screen (your saved readings and the register are kept).')) return;
    fields.forEach(function (el) { if (el.id !== 'jb-tech' && el.id !== 'eod-email') { el.value = ''; } }); keep();
    if (typeof window.npSync === 'function') { try { npSync(); } catch (e) {} }
  };

  /* ---------- 4) device job register ---------- */
  var REG = 'mfd_register_v1';
  var reg = document.createElement('div'); reg.className = 'fx-card';
  JB.appendChild(reg);
  function drawReg() {
    var L = []; try { L = JSON.parse(get(REG) || '[]'); } catch (e) {}
    reg.innerHTML = '<h4>Jobs saved from this phone (' + L.length + ')</h4>' +
      (L.length ? '<div class="fx-reg">' + L.slice().reverse().map(function (r) { return '<div><b>' + esc(r.client || r.cid) + '</b> · ' + esc(r.mod) + (r.eq ? ' · ' + esc(r.eq) : '') + '<br><span class="fx-small">' + new Date(r.at).toLocaleString() + (r.tech ? ' · ' + esc(r.tech) : '') + '</span></div>'; }).join('') + '</div>' +
        '<div class="fx-row"><button class="fx-btn" id="fx-regclr" style="border-color:var(--dim);color:var(--dim)">Clear this list</button></div><div class="fx-small">Clearing only empties this list on the phone — the Mundo log in Drive keeps everything.</div>'
        : '<div class="fx-small">Readings you save will be listed here.</div>');
    if ($('fx-regclr')) $('fx-regclr').onclick = function () { if (confirm('Clear the list on this phone? The Mundo log keeps every reading.')) { put(REG, '[]'); drawReg(); } };
  }
  var NAMES = { rf: 'Refrigeration', rfq: 'Refrigeration quick check', ch: 'Chiller / tower', ac: 'AC', acq: 'AC quick check', fn: 'Furnace' };
  if (typeof window.saveReading === 'function') {
    var orig = window.saveReading;
    window.saveReading = function (mod) {
      var cid = ($('jb-cid') || {}).value || '';
      var r = orig.apply(this, arguments);
      if (cid.trim()) { var L = []; try { L = JSON.parse(get(REG) || '[]'); } catch (e) {}
        L.push({ at: new Date().toISOString(), mod: NAMES[mod] || mod, cid: cid, client: ($('jb-client') || {}).value || '', eq: ($('jb-eqid') || {}).value || '', tech: ($('jb-tech') || {}).value || '' });
        put(REG, JSON.stringify(L.slice(-300))); drawReg();
        if (window.MFD_LAST_REPORT) showReportBar(window.MFD_LAST_REPORT); }
      return r;
    };
  }
  drawReg();
  function showReportBar(id) {
    var b = $('fx-repbar'); if (!b) { b = document.createElement('div'); b.id = 'fx-repbar'; b.style.cssText = 'position:fixed;left:10px;right:10px;bottom:12px;z-index:50;background:#1B2951;color:#fff;border:1px solid #C9A961;border-radius:12px;padding:12px;display:flex;gap:10px;align-items:center;font-size:14px;box-shadow:0 4px 16px #0006'; document.body.appendChild(b); }
    b.innerHTML = '<span style="flex:1">📄 Service report ready</span><a href="report.html?id=' + encodeURIComponent(id) + '" style="background:#C9A961;color:#1B2951;font-weight:700;border-radius:8px;padding:8px 12px;text-decoration:none">Open report</a><button style="background:none;border:0;color:#fff;font-size:18px" onclick="this.parentNode.remove()">×</button>';
  }
  var rl = document.createElement('div'); rl.className = 'fx-card';
  rl.innerHTML = '<h4>Service reports</h4><div class="fx-small">Every saved reading makes an easy-to-read report anyone can follow — print it, save it as a PDF, or share it.</div><div class="fx-row"><a class="fx-btn" style="text-decoration:none" href="report.html">Open reports</a></div>';
  JB.appendChild(rl);

  /* ---------- 5) nav link + install/offline ---------- */
  var nav = document.querySelector('nav');
  if (nav) { var b = document.createElement('button'); b.innerHTML = 'Maint.<br>&amp; Grounds'; b.onclick = function () { location.href = '../../maintenance/'; }; nav.appendChild(b);
    var h = document.createElement('button'); h.innerHTML = '⌂<br>Home'; h.onclick = function () { location.href = '../'; }; nav.insertBefore(h, nav.firstChild); }
  if ('serviceWorker' in navigator && location.protocol === 'https:') navigator.serviceWorker.register('sw.js').catch(function () {});
})();
