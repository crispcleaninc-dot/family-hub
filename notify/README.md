# Cyars Notify — shared notifications for all installable apps

Every installable app has a small gold bell (bottom-left). Notifications stay **off** until the person taps the bell and turns them on, then picks what they want: Appointments, Deadlines, Unfinished items, Things to do, and quiet hours.

| File | Where it lives | What it does |
|---|---|---|
| `notify.js` | copied into each app folder | Bell, opt-in panel, reminders list, alerts while the app is open/recent |
| `notify-sw.js` | copied into each app folder, loaded by that app's `sw.js` | Shows pushed alerts, opens the app when tapped, background checks |
| `config.json` | **only here** — every app reads it | Firebase keys + hub link (fill in once) |
| `hub/NotifyHub.gs` + `hub/appsscript.json` | Apps Script project "Cyars Notify Hub" | Sends alerts when apps are closed (every 5 minutes) |

## Turning on closed-app alerts (one time)
1. **Firebase** (console.firebase.google.com, as crispcleaninc@gmail.com): Add project "Cyars Notify" → Add app → Web. Copy the config values into `config.json` → `firebase`. Then Project settings → Cloud Messaging → Web Push certificates → Generate key pair; copy it into `vapidKey`.
2. **Hub**: new Apps Script project "Cyars Notify Hub"; paste `hub/NotifyHub.gs` and `hub/appsscript.json`. Script property `FIREBASE_PROJECT_ID` = the Firebase project id. Run `setupNotifyHub()` once. Deploy as web app (Execute as me, Anyone). Put the `/exec` link in `config.json` → `hubUrl`.
3. Commit `config.json`. Every app picks it up the next time it opens.

Until then, alerts still work while an app is open or was used recently.

## For app code
```js
CyarsNotify.schedule({ id: 'appt-123', type: 'appointment', title: 'Dentist — Emma', at: '2026-11-20T15:30', body: '3:30 PM, bring card', url: location.href });
CyarsNotify.cancel('appt-123');   CyarsNotify.done('appt-123');
```
Types: `appointment`, `deadline`, `unfinished`, `todo`, `updates`. `CyarsNotify.announce(title, body)` sends an "App updates & news" alert; apps also announce themselves automatically when a new version installs. Repeat: `daily`, `weekly`.

Other Apps Scripts can alert everyone who opted in to an app: POST `{action:'send', key:HUB_KEY, app:'Covenant', title, body, url, type}` to the hub.

## iPhone
Alerts only work after the app is added to the Home Screen (Share → Add to Home Screen) and opened from there (iOS 16.4+).
