/**
 * Cyars Notify Hub v1.0 — sends phone/computer alerts for all of Ciarne's installable apps,
 * even when the app is closed. Google Apps Script web app + Firebase Cloud Messaging.
 *
 * Setup (one time, as crispcleaninc@gmail.com):
 *  1. New Apps Script project "Cyars Notify Hub". Paste this file as Code.gs and
 *     appsscript.json from this folder (Project Settings → show manifest).
 *  2. Script properties:
 *       FIREBASE_PROJECT_ID   = your Firebase project id (required)
 *       HUB_KEY               = any long secret; other Apps Scripts use it with action "send" (optional)
 *       SERVICE_ACCOUNT_JSON  = Firebase service-account key JSON (optional; only if the plain
 *                               owner sign-in is refused by Firebase)
 *  3. Run setupNotifyHub() once and approve. It makes the "Cyars Notify Hub" sheet and a
 *     5-minute timer.
 *  4. Deploy → Web app → Execute as: Me, Who has access: Anyone. Put the /exec link in
 *     family-hub/notify/config.json as hubUrl.
 *
 * Nothing is sent to a device unless that person turned notifications on in the app,
 * left that kind of alert checked, and it isn't inside their quiet hours.
 */
var NH = { VERSION: '1.0', SHEET: 'Cyars Notify Hub', MAX_ITEMS: 300 };

function doGet() { return out_({ ok: true, hub: 'Cyars Notify Hub', version: NH.VERSION }); }

function doPost(e) {
  var b = {};
  try { b = JSON.parse(e.postData.contents); } catch (x) { return out_({ ok: false, error: 'bad json' }); }
  var lock = LockService.getScriptLock();
  try {
    lock.waitLock(20000);
    switch (b.action) {
      case 'sync': return out_(sync_(b, true));
      case 'off': return out_(sync_(b, false));
      case 'test': return out_(test_(b));
      case 'send': return out_(sendFromApp_(b));
      default: return out_({ ok: false, error: 'unknown action' });
    }
  } catch (err) {
    log_('error', b.app || '', String(err));
    return out_({ ok: false, error: String(err) });
  } finally { try { lock.releaseLock(); } catch (x) {} }
}

/* ---------- storage ---------- */
function book_() {
  var p = PropertiesService.getScriptProperties(), id = p.getProperty('SHEET_ID'), ss = null;
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (x) {} }
  if (!ss) { ss = SpreadsheetApp.create(NH.SHEET); p.setProperty('SHEET_ID', ss.getId()); }
  tab_(ss, 'Devices', ['Token', 'Device', 'App', 'Scope', 'AppUrl', 'Icon', 'TimeZone', 'On', 'Types', 'QuietStart', 'QuietEnd', 'Updated', 'Active']);
  tab_(ss, 'Reminders', ['Token', 'App', 'Scope', 'Id', 'Type', 'Title', 'Body', 'At', 'Repeat', 'Url', 'LastSent']);
  tab_(ss, 'Log', ['Time', 'Kind', 'App', 'Detail']);
  return ss;
}
function tab_(ss, name, head) {
  var sh = ss.getSheetByName(name);
  if (!sh) { sh = ss.insertSheet(name); sh.appendRow(head); sh.setFrozenRows(1); sh.getRange(1, 1, 1, head.length).setFontWeight('bold'); }
  var s1 = ss.getSheetByName('Sheet1'); if (s1 && ss.getSheets().length > 1) ss.deleteSheet(s1);
  return sh;
}
function rows_(name) {
  var sh = book_().getSheetByName(name), v = sh.getDataRange().getValues(), h = v.shift();
  return { sh: sh, head: h, rows: v };
}
function log_(kind, app, detail) {
  try {
    var sh = book_().getSheetByName('Log');
    sh.appendRow([new Date(), kind, app, String(detail).slice(0, 400)]);
    if (sh.getLastRow() > 3000) sh.deleteRows(2, 500);
  } catch (x) {}
}

/* ---------- app → hub ---------- */
function sync_(b, on) {
  if (!b.token || !b.app) return { ok: false, error: 'missing token/app' };
  var scope = String(b.scope || b.app);
  var prefs = b.prefs || {}, types = prefs.types || {};
  var typeList = Object.keys(types).filter(function (k) { return types[k] !== false; }).join(',');
  var D = rows_('Devices'), found = -1;
  for (var i = 0; i < D.rows.length; i++) if (D.rows[i][0] === b.token && D.rows[i][3] === scope) { found = i; break; }
  var row = [b.token, b.device || '', b.app, scope, b.appUrl || '', b.icon || '', b.tz || 'America/Detroit', on ? 'yes' : 'no', typeList, prefs.quietStart || '', prefs.quietEnd || '', new Date(), 'yes'];
  if (found >= 0) D.sh.getRange(found + 2, 1, 1, row.length).setValues([row]); else D.sh.appendRow(row);

  // replace this device+app's reminders, keeping what was already sent
  var R = rows_('Reminders'), keep = [], sent = {};
  R.rows.forEach(function (r) {
    if (r[0] === b.token && r[2] === scope) sent[r[3]] = { at: Number(r[7]), last: Number(r[10]) || 0 };
    else keep.push(r);
  });
  var items = (on && b.items) ? b.items.slice(0, NH.MAX_ITEMS) : [];
  items.forEach(function (it) {
    var at = Number(it.at) || 0, prev = sent[String(it.id)], last = Math.max(Number(it.lastSent) || 0, prev && prev.at === at ? prev.last : 0);
    keep.push([b.token, b.app, scope, String(it.id), String(it.type || 'todo'), String(it.title || '').slice(0, 120), String(it.body || '').slice(0, 300), at, String(it.repeat || ''), String(it.url || b.appUrl || ''), last]);
  });
  R.sh.getRange(2, 1, Math.max(R.sh.getLastRow() - 1, 1), R.head.length).clearContent();
  if (keep.length) R.sh.getRange(2, 1, keep.length, R.head.length).setValues(keep);
  return { ok: true, on: on, reminders: items.length };
}

function test_(b) {
  if (!b.token) return { ok: false };
  var r = fcm_(b.token, { title: (b.app || 'App') + ' — test from the hub', body: 'Closed-app alerts are working on this device.', url: b.appUrl || '', tag: 'cyars-test' });
  log_('test', b.app || '', r.code);
  return { ok: r.code === 200, code: r.code };
}

/* other Apps Scripts can send an alert to everyone who turned notifications on for an app:
   UrlFetchApp.fetch(HUB_URL, {method:'post', payload: JSON.stringify({action:'send', key:HUB_KEY,
     app:'Community Covenant', type:'todo', title:'...', body:'...', url:'...'})}) */
function sendFromApp_(b) {
  var key = PropertiesService.getScriptProperties().getProperty('HUB_KEY');
  if (!key || b.key !== key) return { ok: false, error: 'not allowed' };
  var D = rows_('Devices'), n = 0;
  D.rows.forEach(function (d) {
    if (d[2] !== b.app || d[7] !== 'yes' || d[12] !== 'yes') return;
    if (b.type && String(d[8]).split(',').indexOf(b.type) < 0) return;
    if (quiet_(d[6], d[9], d[10])) return;
    var r = fcm_(d[0], { title: b.title, body: b.body || '', url: b.url || d[4], tag: 'cyars-' + d[3] + '-' + (b.tag || Date.now()), icon: d[5] });
    if (r.code === 200) n++; else if (r.gone) markGone_(d[0]);
  });
  log_('send', b.app, n + ' device(s)');
  return { ok: true, sent: n };
}

/* ---------- timer: send what is due ---------- */
function sendDue() {
  var lock = LockService.getScriptLock();
  if (!lock.tryLock(30000)) return;
  try {
    var D = rows_('Devices'), dev = {};
    D.rows.forEach(function (d) { if (d[7] === 'yes' && d[12] === 'yes') dev[d[0] + '|' + d[3]] = d; });
    var R = rows_('Reminders'), now = Date.now(), changed = false, gone = {};
    R.rows.forEach(function (r) {
      var d = dev[r[0] + '|' + r[2]]; if (!d || gone[r[0]]) return;
      var at = Number(r[7]), last = Number(r[10]) || 0;
      if (!at || at > now || last >= at) return;
      if (String(d[8]).split(',').indexOf(String(r[4])) < 0) return;
      if (quiet_(d[6], d[9], d[10])) return;
      var label = { appointment: 'Appointment', deadline: 'Deadline', unfinished: 'Unfinished', todo: 'To do' }[r[4]] || '';
      var res = fcm_(r[0], { title: r[5] || 'Reminder', body: (label ? label + ' · ' : '') + (r[6] || ''), url: r[9] || d[4], tag: 'cyars-' + r[2] + '-' + r[3], icon: d[5] });
      if (res.gone) { gone[r[0]] = 1; return; }
      if (res.code !== 200) return;
      r[10] = now;
      var step = r[8] === 'daily' ? 864e5 : r[8] === 'weekly' ? 6048e5 : 0;
      if (step) { while (at <= now) at += step; r[7] = at; }
      changed = true;
    });
    if (changed) R.sh.getRange(2, 1, R.rows.length, R.head.length).setValues(R.rows);
    Object.keys(gone).forEach(markGone_);
  } finally { lock.releaseLock(); }
}
function quiet_(tz, qs, qe) {
  if (!qs || !qe || qs === qe) return false;
  var t = Utilities.formatDate(new Date(), tz || 'America/Detroit', 'HH:mm').split(':');
  var m = (+t[0]) * 60 + (+t[1]), a = hm_(qs), b = hm_(qe);
  return a < b ? (m >= a && m < b) : (m >= a || m < b);
}
function hm_(s) { var p = String(s).split(':'); return (+p[0] || 0) * 60 + (+p[1] || 0); }
function markGone_(token) {
  var D = rows_('Devices');
  D.rows.forEach(function (d, i) { if (d[0] === token) D.sh.getRange(i + 2, 13).setValue('no'); });
  log_('gone', '', 'token retired');
}

/* ---------- Firebase Cloud Messaging ---------- */
function fcm_(token, m) {
  var project = PropertiesService.getScriptProperties().getProperty('FIREBASE_PROJECT_ID');
  if (!project) return { code: 0, error: 'FIREBASE_PROJECT_ID not set' };
  var data = { cyars: '1', title: String(m.title || 'Reminder'), body: String(m.body || ''), url: String(m.url || ''), tag: String(m.tag || ''), icon: String(m.icon || '') };
  var body = { message: { token: token, data: data, webpush: { headers: { Urgency: 'high', TTL: '86400' } } } };
  var res = UrlFetchApp.fetch('https://fcm.googleapis.com/v1/projects/' + project + '/messages:send', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + accessToken_(), 'x-goog-user-project': project },
    payload: JSON.stringify(body)
  });
  var code = res.getResponseCode(), txt = res.getContentText();
  if (code !== 200) log_('fcm', '', code + ' ' + txt.slice(0, 300));
  return { code: code, gone: code === 404 || (code === 400 && /UNREGISTERED|INVALID_ARGUMENT.*registration/i.test(txt)) };
}
function accessToken_() {
  var sa = PropertiesService.getScriptProperties().getProperty('SERVICE_ACCOUNT_JSON');
  if (!sa) return ScriptApp.getOAuthToken();                // owner sign-in (scope in appsscript.json)
  var c = CacheService.getScriptCache(), hit = c.get('fcm_tok'); if (hit) return hit;
  var k = JSON.parse(sa), now = Math.floor(Date.now() / 1000);
  var enc = function (o) { return Utilities.base64EncodeWebSafe(JSON.stringify(o)).replace(/=+$/, ''); };
  var unsigned = enc({ alg: 'RS256', typ: 'JWT' }) + '.' + enc({ iss: k.client_email, scope: 'https://www.googleapis.com/auth/firebase.messaging', aud: 'https://oauth2.googleapis.com/token', iat: now, exp: now + 3600 });
  var sig = Utilities.base64EncodeWebSafe(Utilities.computeRsaSha256Signature(unsigned, k.private_key)).replace(/=+$/, '');
  var r = JSON.parse(UrlFetchApp.fetch('https://oauth2.googleapis.com/token', { method: 'post', payload: { grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer', assertion: unsigned + '.' + sig } }).getContentText());
  c.put('fcm_tok', r.access_token, 3300);
  return r.access_token;
}

/* ---------- one-time setup ---------- */
function setupNotifyHub() {
  var ss = book_();
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'sendDue') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('sendDue').timeBased().everyMinutes(5).create();
  Logger.log('Cyars Notify Hub ready. Sheet: ' + ss.getUrl());
  return ss.getUrl();
}

function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
