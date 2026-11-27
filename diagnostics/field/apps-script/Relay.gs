/**
 * Relay.gs — add this file to the Apps Script project "MUNDO DIAGNOSTICS ENHANCED" (crispcleaninc).
 * Nothing in Code.gs changes. It lets the GitHub version of the Field Diagnostics app use the same
 * backend: Mundo Field Diagnostics Log sheets, branded log Docs, Gmail end-of-day batch, and text-intake clients.
 *
 * Steps (one time):
 *  1. Open the project → + (Add a file) → Script → name it Relay → paste this file → Save.
 *  2. Deploy → New deployment → type: Web app → Execute as: Me → Who has access: Anyone → Deploy → Allow.
 *  3. Copy the Web app URL (ends in /exec) and paste it in the app: Job Info → Mundo log connection → Save link.
 */
function doPost(e) {
  var out;
  try {
    var body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var a = body.args || [];
    var result;
    switch (body.fn) {
      case 'submitReading':     result = submitReading(a[0]); break;
      case 'batchDailyEmail':   result = batchDailyEmail(a[0]); break;
      case 'listIntakeClients': result = listIntakeClients(a[0]); break;
      case 'markIntakeOnSite':  result = markIntakeOnSite(a[0], a[1], a[2], a[3]); break;
      case 'ping':              result = 'ok'; break;
      default: throw new Error('Unknown action');
    }
    out = { ok: true, result: result };
  } catch (err) {
    out = { ok: false, error: String(err && err.message || err) };
  }
  return ContentService.createTextOutput(JSON.stringify(out)).setMimeType(ContentService.MimeType.JSON);
}
