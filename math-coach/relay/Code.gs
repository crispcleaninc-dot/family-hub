/**
 * Math Coach Relay (Google Apps Script, crispcleaninc account)
 * Lets the Math Homework Coach app talk with an AI tutor.
 * The Anthropic key lives ONLY in Script Properties (ANTHROPIC_API_KEY), never in the app.
 *
 * Script Properties:
 *   ANTHROPIC_API_KEY  (required)  her Anthropic API key
 *   MODEL              (optional)  default claude-haiku-5-5
 *   DAILY_LIMIT        (optional)  max AI answers per day, default 300 (protects her bill)
 *
 * Deploy: Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone.
 * Put the /exec link in family-hub/math-coach/config.js.
 */

var SYSTEM = [
  'You are a patient, warm math tutor talking out loud with an 11-year-old student doing homework. Use the student\'s name and keep it warm.',
  'Your words are read aloud by a phone, so: plain spoken sentences only, no markdown, no lists, no symbols like * or #.',
  'Keep each answer short: 1 to 4 sentences. Ask one question back when it helps them think.',
  'Explain the way a good teacher would at the kitchen table, step by step, using the student\'s own numbers.',
  'Long division steps are Divide, Multiply, Subtract, Bring down. Multi-digit multiplication uses carrying, a placeholder zero for the tens row, then adding the rows.',
  'When the student needs to write something, say exactly what to write and where on the paper (which box, which column, which row).',
  'If the student asks for the answer, you may give it, then show how to check it.',
  'If the student seems frustrated or tired, be kind and encourage a short break. Never shame them.',
  'Stay on school and homework topics. If the student asks about something unsafe or not for kids, kindly steer back to the homework and suggest talking to Mom.',
  'Always double check your arithmetic before you answer.'
].join(' ');

function doGet() {
  return json_({ ok: true, app: 'Math Coach Relay', ai: !!prop_('ANTHROPIC_API_KEY') });
}

function doPost(e) {
  try {
    var body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    if (body.action === 'ping') return json_({ ok: true, ai: !!prop_('ANTHROPIC_API_KEY') });
    var key = prop_('ANTHROPIC_API_KEY');
    if (!key) return json_({ ok: false, error: 'not_configured' });
    if (!underLimit_()) return json_({ ok: false, error: 'daily_limit' });

    var question = String(body.question || '').slice(0, 600);
    if (!question) return json_({ ok: false, error: 'empty' });
    var name = String(body.name || '').slice(0, 40);
    var context = String(body.context || '').slice(0, 1500);
    var history = Array.isArray(body.history) ? body.history.slice(-8) : [];

    var messages = [];
    history.forEach(function (h) {
      if (!h || !h.text) return;
      var role = h.who === 'me' ? 'user' : 'assistant';
      var text = String(h.text).slice(0, 600);
      if (messages.length && messages[messages.length - 1].role === role) messages[messages.length - 1].content += '\n' + text;
      else messages.push({ role: role, content: text });
    });
    while (messages.length && messages[0].role !== 'user') messages.shift();
    var prompt = (context ? 'What is on the student\'s screen right now: ' + context + '\n\n' : '') + 'The student says: ' + question;
    if (messages.length && messages[messages.length - 1].role === 'user') messages[messages.length - 1].content += '\n' + prompt;
    else messages.push({ role: 'user', content: prompt });

    var res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
      method: 'post',
      contentType: 'application/json',
      headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01' },
      muteHttpExceptions: true,
      payload: JSON.stringify({
        model: prop_('MODEL') || 'claude-haiku-5-5',
        max_tokens: 1200,
        system: SYSTEM + (name ? ' The student\'s name is ' + name + '.' : ''),
        messages: messages
      })
    });
    var code = res.getResponseCode();
    var out = JSON.parse(res.getContentText() || '{}');
    if (code !== 200) return json_({ ok: false, error: 'ai_error', status: code, detail: (out.error && out.error.message) || '' });
    var text = (out.content || []).filter(function (c) { return c.type === 'text'; }).map(function (c) { return c.text; }).join(' ').trim();
    if (!text) return json_({ ok: false, error: 'empty_answer', stop: out.stop_reason || '', types: (out.content || []).map(function (c) { return c.type; }).join(',') });
    countUse_();
    return json_({ ok: true, answer: text });
  } catch (err) {
    return json_({ ok: false, error: 'server', detail: String(err) });
  }
}

/* ---------- helpers ---------- */
function prop_(k) { return PropertiesService.getScriptProperties().getProperty(k); }
function today_() { return Utilities.formatDate(new Date(), 'America/Detroit', 'yyyy-MM-dd'); }
function underLimit_() {
  var p = PropertiesService.getScriptProperties();
  var limit = Number(p.getProperty('DAILY_LIMIT') || 300);
  return Number(p.getProperty('USED_' + today_()) || 0) < limit;
}
function countUse_() {
  var lock = LockService.getScriptLock(); lock.waitLock(5000);
  try {
    var p = PropertiesService.getScriptProperties(), k = 'USED_' + today_();
    p.setProperty(k, String(Number(p.getProperty(k) || 0) + 1));
  } finally { lock.releaseLock(); }
}
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/** Run once from the editor after adding the key, to confirm the AI answers. */
function testTutor() {
  var r = doPost({ postData: { contents: JSON.stringify({ question: 'Why do we bring down the next number in long division?', name: 'Ezekiel' }) } });
  Logger.log(r.getContent());
}
