/**
 * School & Chores Relay (Google Apps Script, crispcleaninc account)
 *
 * Keeps the children's grades and assignments PRIVATE. The family-hub app is public on
 * GitHub Pages, so no school data is ever put in the repo. The data lives in Drive
 * ("Family School Tracker Data.json", written each day by the Skyward sync), and this relay
 * hands it to the app only when the right PIN is given.
 *
 * Script Properties (Project Settings > Script properties):
 *   PARENT_PIN   (required)  Mom's PIN - sees every child, all alerts
 *   KID_PINS     (optional)  JSON, e.g. {"Caleb":"5656","Carey":"1111","Charles":"2222","Emma":"3333","Ezekiel":"4444"}
 *                            each child then sees only their own page
 *
 * Deploy: Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone.
 * Put the /exec link in family-hub/school/config.js (SCHOOL_RELAY).
 */
var DATA_TITLE = 'Family School Tracker Data.json';

function doGet() {
  var f = newest_();
  return json_({ ok: true, app: 'School & Chores Relay', hasData: !!f, updated: f ? f.getLastUpdated() : null, pinSet: !!prop_('PARENT_PIN') });
}

function doPost(e) {
  try {
    var body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (body.action === 'ping') return json_({ ok: true });
    if (!prop_('PARENT_PIN')) return json_({ ok: false, error: 'not_configured' });
    if (tooManyTries_()) return json_({ ok: false, error: 'locked', detail: 'Too many wrong PINs. Try again in 15 minutes.' });

    var pin = String(body.pin || '').trim();
    var role = null, kid = null;
    if (pin && pin === prop_('PARENT_PIN')) role = 'parent';
    else {
      var kids = {};
      try { kids = JSON.parse(prop_('KID_PINS') || '{}'); } catch (x) {}
      Object.keys(kids).forEach(function (k) { if (pin && String(kids[k]) === pin) { role = 'kid'; kid = k; } });
    }
    if (!role) { countFail_(); return json_({ ok: false, error: 'bad_pin' }); }

    var f = newest_();
    if (!f) return json_({ ok: false, error: 'no_data' });
    var data = JSON.parse(f.getBlob().getDataAsString());
    data.fileUpdated = f.getLastUpdated();
    if (role === 'kid') {
      data.kids = (data.kids || []).filter(function (c) { return c.name === kid; });
      data.events = (data.events || []).filter(function (ev) { return (ev.who || []).indexOf(kid) > -1; });
      var ch = {}; if (data.chores && data.chores[kid]) ch[kid] = data.chores[kid]; data.chores = ch;
    }
    return json_({ ok: true, role: role, kid: kid, data: data });
  } catch (err) {
    return json_({ ok: false, error: 'server', detail: String(err) });
  }
}

/* The daily sync adds a new copy each day; use the newest and trash older copies. */
function newest_() {
  var it = DriveApp.searchFiles('title = "' + DATA_TITLE + '" and trashed = false');
  var files = [];
  while (it.hasNext()) files.push(it.next());
  if (!files.length) return null;
  files.sort(function (a, b) { return b.getLastUpdated() - a.getLastUpdated(); });
  for (var i = 1; i < files.length; i++) { try { files[i].setTrashed(true); } catch (x) {} }
  return files[0];
}

function tooManyTries_() {
  var c = CacheService.getScriptCache();
  return Number(c.get('fails') || 0) >= 8;
}
function countFail_() {
  var c = CacheService.getScriptCache();
  c.put('fails', String(Number(c.get('fails') || 0) + 1), 900);
}
function prop_(k) { return PropertiesService.getScriptProperties().getProperty(k); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/* Run once from the editor to check everything is connected. */
function testRelay() {
  var f = newest_();
  Logger.log(f ? ('Data file found, updated ' + f.getLastUpdated()) : 'No data file yet');
  Logger.log(prop_('PARENT_PIN') ? 'Parent PIN is set' : 'Set PARENT_PIN in Script properties');
}
