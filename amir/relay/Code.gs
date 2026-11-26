/**
 * =========================================================
 *  AMIR'S WORLD — Google Apps Script Backend
 *  A toddler learning app for Amir (age 2)
 *  Features: Words, Matching, ABC, Colors, Shapes, Music
 *
 *  DEPLOY AS:
 *    Extensions > Apps Script > Deploy > New Deployment
 *    Type: Web App
 *    Execute as: Me
 *    Who has access: Anyone (or Anyone with link)
 * =========================================================
 */

// ============================================================
//  ENTRY POINT — serves the web app
// ============================================================
function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle("Amir's World 🌟")
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1, user-scalable=no');
}

// ============================================================
//  PROGRESS STORAGE — saves star progress per session
//  Uses Script Properties (server-side key-value store)
// ============================================================

/**
 * Load Amir's saved progress.
 * @returns {Object} progress data — stars, words seen, last played
 */
function loadProgress() {
  const props = PropertiesService.getScriptProperties();
  const raw = props.getProperty('amir_progress');
  if (!raw) {
    return {
      stars: 0,
      wordsLearned: [],
      totalSessions: 0,
      lastPlayed: null
    };
  }
  return JSON.parse(raw);
}

/**
 * Save Amir's progress.
 * Called from the client via google.script.run.saveProgress(data)
 * @param {Object} data
 */
function saveProgress(data) {
  try {
    const props = PropertiesService.getScriptProperties();
    props.setProperty('amir_progress', JSON.stringify(data));
    return { success: true };
  } catch(err) {
    console.error('saveProgress error:', err);
    return { success: false, error: err.message };
  }
}

/**
 * Get the current word list with milestone data.
 * Client calls this on load to get a fresh word list.
 */
function getWordList() {
  return WORDS;
}

/**
 * Record that Amir learned a word.
 */
function recordWordLearned(word) {
  try {
    const progress = loadProgress();
    if (!progress.wordsLearned.includes(word)) {
      progress.wordsLearned.push(word);
    }
    progress.lastPlayed = new Date().toISOString();
    saveProgress(progress);
    return { 
      success: true, 
      totalLearned: progress.wordsLearned.length,
      milestone: getMilestone(progress.wordsLearned.length)
    };
  } catch(err) {
    return { success: false };
  }
}

/**
 * Increment session count (called on app open).
 */
function startSession() {
  const progress = loadProgress();
  progress.totalSessions = (progress.totalSessions || 0) + 1;
  progress.lastPlayed = new Date().toISOString();
  saveProgress(progress);
  return progress;
}

/**
 * Returns a milestone message if applicable.
 */
function getMilestone(count) {
  const milestones = {
    5:  { emoji:'⭐', msg:'5 words! Amazing Amir!' },
    10: { emoji:'🌟', msg:'10 words! Super Star!' },
    15: { emoji:'🏆', msg:'15 words! Champion!' },
    20: { emoji:'🎊', msg:'ALL 20 WORDS! Genius!' },
  };
  return milestones[count] || null;
}

// ============================================================
//  WORD DATA — master list (mirrored in front-end too)
// ============================================================
const WORDS = [
  { emoji:'🍎', word:'APPLE',    sound:'apple'    },
  { emoji:'🐶', word:'DOG',      sound:'dog'      },
  { emoji:'🐱', word:'CAT',      sound:'cat'      },
  { emoji:'🐻', word:'BEAR',     sound:'bear'     },
  { emoji:'🍌', word:'BANANA',   sound:'banana'   },
  { emoji:'🌈', word:'RAINBOW',  sound:'rainbow'  },
  { emoji:'⭐', word:'STAR',     sound:'star'     },
  { emoji:'🎈', word:'BALLOON',  sound:'balloon'  },
  { emoji:'🚗', word:'CAR',      sound:'car'      },
  { emoji:'🏠', word:'HOUSE',    sound:'house'    },
  { emoji:'🌸', word:'FLOWER',   sound:'flower'   },
  { emoji:'🦁', word:'LION',     sound:'lion'     },
  { emoji:'🐘', word:'ELEPHANT', sound:'elephant' },
  { emoji:'🦆', word:'DUCK',     sound:'duck'     },
  { emoji:'🍕', word:'PIZZA',    sound:'pizza'    },
  { emoji:'🎂', word:'CAKE',     sound:'cake'     },
  { emoji:'👶', word:'BABY',     sound:'baby'     },
  { emoji:'🌙', word:'MOON',     sound:'moon'     },
  { emoji:'☀️', word:'SUN',      sound:'sun'      },
  { emoji:'🐸', word:'FROG',     sound:'frog'     },
];

// ============================================================
//  ADMIN / REPORTING — can be run from the Script Editor
// ============================================================

/**
 * View Amir's learning progress in the Apps Script logs.
 * Run this manually from the Script Editor to check progress.
 */
function viewProgress() {
  const progress = loadProgress();
  console.log('=== AMIR\'S PROGRESS ===');
  console.log('Stars earned:', progress.stars);
  console.log('Words learned:', progress.wordsLearned.length, '/', WORDS.length);
  console.log('Words:', progress.wordsLearned.join(', '));
  console.log('Total sessions:', progress.totalSessions);
  console.log('Last played:', progress.lastPlayed);
}

/**
 * Reset Amir's progress (if needed).
 * Run manually from Script Editor only.
 */
function resetProgress() {
  PropertiesService.getScriptProperties().deleteProperty('amir_progress');
  console.log('Progress reset!');
}

// ============================================================
//  RELAY for the installable app (added Nov 26, 2026)
//  The downloadable Amir's World (crispcleaninc-dot.github.io/family-hub/amir/)
//  calls this web app for:
//    - AI Magic Lesson + AI Build-a-Book (the Anthropic key stays here, never on the tablet)
//    - Cloud backup of progress (same loadProgress / saveProgress as above)
//  Script Properties:
//    ANTHROPIC_API_KEY (required for AI)   MODEL (optional, default claude-haiku-5-5)
//    DAILY_LIMIT (optional, default 60 AI calls a day)
//  Everything above this line is unchanged; doGet still serves the original web app.
// ============================================================
function doPost(e) {
  try {
    var body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var a = body.action;
    if (a === 'ping') return json_({ ok: true, app: "Amir's World Relay", ai: !!prop_('ANTHROPIC_API_KEY') });
    if (a === 'loadProgress') return json_({ ok: true, data: loadProgress() });
    if (a === 'saveProgress') {
      var d = body.data;
      if (!d || typeof d !== 'object') return json_({ ok: false, error: 'empty' });
      if (JSON.stringify(d).length > 8000) return json_({ ok: false, error: 'too_big' });
      return json_({ ok: saveProgress(d).success });
    }
    if (a === 'ai') return json_(ai_(body));
    return json_({ ok: false, error: 'unknown_action' });
  } catch (err) {
    return json_({ ok: false, error: 'server', detail: String(err) });
  }
}

function ai_(body) {
  var key = prop_('ANTHROPIC_API_KEY');
  if (!key) return { ok: false, error: 'not_configured' };
  if (!underLimit_()) return { ok: false, error: 'daily_limit' };
  var msgs = (Array.isArray(body.messages) ? body.messages : []).slice(-4).map(function (m) {
    return { role: m.role === 'assistant' ? 'assistant' : 'user', content: String(m.content || '').slice(0, 4000) };
  });
  if (!msgs.length) return { ok: false, error: 'empty' };
  var res = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01' },
    payload: JSON.stringify({
      model: prop_('MODEL') || 'claude-haiku-5-5',
      max_tokens: Math.min(Number(body.max_tokens) || 800, 1500),
      system: 'You make content for Amir, a 2-year-old, in a learning app. Keep everything gentle, happy and right for a toddler. Follow the requested JSON format exactly.',
      messages: msgs
    })
  });
  var out = JSON.parse(res.getContentText() || '{}');
  if (res.getResponseCode() !== 200) return { ok: false, error: 'ai_error', detail: (out.error && out.error.message) || '' };
  countUse_();
  return { ok: true, data: out };
}

function prop_(k) { return PropertiesService.getScriptProperties().getProperty(k); }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function today_() { return Utilities.formatDate(new Date(), 'America/Detroit', 'yyyy-MM-dd'); }
function underLimit_() {
  var n = Number(prop_('ai_count_' + today_()) || 0);
  return n < Number(prop_('DAILY_LIMIT') || 60);
}
function countUse_() {
  var p = PropertiesService.getScriptProperties(), k = 'ai_count_' + today_();
  p.setProperty(k, String(Number(p.getProperty(k) || 0) + 1));
}
