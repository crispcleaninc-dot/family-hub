# School & Chores

Each child's homework, missing work, grades and daily chores, from WLCSD Skyward Family Access.

**Privacy:** this repo is public, so no school data is ever stored here. The data lives only in
Mom's Drive (crispcleaninc) as `Family School Tracker Data.json`. The app gets it through the
**School & Chores Relay** (Apps Script, `relay/`), and only with a PIN.

## How it updates
A daily scheduled task signs in to Skyward in Mom's Chrome (crispcleaninc profile), reads each
child's gradebook (missing assignments, grades, recent scores) and the upcoming-events list, then
saves a new copy of the data file to Drive. The relay always serves the newest copy and trashes
older ones. If a day is missed, the app shows a "this copy is X days old" warning.

## Relay setup (one time)
1. script.google.com (crispcleaninc) > New project "School & Chores Relay". Paste `relay/Code.gs`
   and `relay/appsscript.json` (Project Settings > show appsscript.json).
2. Script properties: `PARENT_PIN` (Mom), optional `KID_PINS` as JSON, e.g.
   `{"Caleb":"5656","Carey":"1111","Charles":"2222","Emma":"3333","Ezekiel":"4444"}`.
3. Run `testRelay` once and allow access.
4. Deploy > New deployment > Web app > Execute as: Me > Anyone. Put the /exec link in `config.js`.

## Also in the app
- **Attendance** for each child (tardies, unexcused, left early, excused), with Mom's Google Calendar
  appointments matched to the same day (parent view only). Unexcused days that match an appointment are
  flagged red so the school can be asked to excuse them.
- **Add homework**: Mom or a child types in homework (take-home folder, Google Classroom). Saved in the
  relay's Script Properties (`ADDED_HW`), so it shows on every device and in the daily plan.
- **Learning apps** per child (the `learningApps` list in the data file).

## Planning rules (in index.html)
- Missing work is spread over the days, newest first: 4 a day when 20+ are missing, otherwise 2.
- Homework due tomorrow, or 3+ catch-up items, = "Homework first": the 3 daily upkeep chores only.
- Light homework day = upkeep + 1 bigger chore. Saturday = big chore day. Sunday = rest + upkeep.
- Chore lists come from the `chores` section of the data file (per child).

## Data file shape
`{updated, source, events:[{date,text,who[],info?}], kids:[{name,school,emoji,gradesAvailable,
grades:[{cls,current,mp1,s1}], missing:[{due,title,cls,mp}], lowScores:[{due,title,cls,score}],
upcoming:[{due,title,cls}], notes}], chores:{Name:{daily[],big[]}}}`
