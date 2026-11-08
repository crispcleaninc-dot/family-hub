/* Caleb #56 Missions - Mom's Home Care Case (V2.34). Private: shows only after the admin PIN.
 * Goal: see Mom's Medicaid Home Help case through from start until a caregiver is coming.
 * Mom is the client: she signs every form. Caleb is her helper: he gathers, calls (Mom on speaker),
 * tracks dates and follows up until it is done. Under 18 he cannot sign for her or be her paid caregiver.
 */
(function () {
  var D = window.C56M_DATA;
  D.cats.splice(1, 0, { id: 'homecare', name: "Mom's Home Care Case", icon: '🏥', private: true });

  var PORTAL = 'https://crispus-mundo.github.io/crisp-cares/apps/cces-care-portal/';
  var MIB = 'https://newmibridges.michigan.gov/';
  var HH = 'https://www.michigan.gov/en/mdhhs/adult-child-serv/adults-and-seniors/independent';

  window.C56M_HOMECARE = {
    offices: [
      { name: 'MDHHS Oakland - Southfield District', addr: '25620 W. 8 Mile Rd, Southfield, MI 48033', phone: '248-262-6400' },
      { name: 'MDHHS Oakland - Madison Heights District', addr: '30755 Montpelier, Madison Heights, MI 48071', phone: '248-583-8700' },
      { name: 'MDHHS Oakland - Pontiac (Saginaw St)', addr: '235 N. Saginaw St, Pontiac, MI 48342', phone: '248-975-5200' },
      { name: 'MDHHS Oakland - Pontiac (Woodward)', addr: '51111 Woodward Ave, Pontiac, MI 48342', phone: '248-975-5400' }
    ],
    log: [
      ['mcase', 'Medicaid case number (last 4 only)'], ['plan', 'Medicaid health plan name'], ['office', 'County office that has the case'],
      ['asw', 'Adult Services Worker name'], ['aswphone', 'Worker phone'], ['aswemail', 'Worker email / fax'],
      ['refdate', 'Date we asked for Home Help (referral)', 'date'], ['formsin', 'Date the DHS-390 + DHS-54A arrived', 'date'],
      ['due21', 'Forms due back by (21 days from the letter)', 'date'], ['doc54', 'Who is signing the DHS-54A (provider + office phone)'],
      ['sent54', 'Date the DHS-54A went to the provider', 'date'], ['signed54', 'Date the provider signed the DHS-54A', 'date'],
      ['returned', 'Date both forms went back to the worker + how (fax/mail/drop-off)', 'date'], ['confirmed', 'Date the worker confirmed they have them', 'date'],
      ['visit', 'Home assessment visit date', 'date'], ['decision', 'Decision date + approved or denied', 'date'], ['hearingdue', 'If denied: hearing request deadline on the notice', 'date'],
      ['provider', 'Caregiver / agency chosen'], ['champs', 'Caregiver CHAMPS enrolled? (yes / pending)'], ['tt', 'Time & Task received + hours per month'],
      ['start', 'Care start date', 'date'], ['review', 'Next review date', 'date'], ['renew', 'Medicaid renewal date', 'date'], ['notes', 'Notes', 'long']
    ]
  };

  function s(t, go, tip) { var o = { t: t }; if (go) o.go = go; if (tip) o.tip = tip; return o; }
  var M = [
    { id: 'h0-role', cat: 'homecare', private: true, who: 'Both', title: 'Phase 0 - Your job on Mom\'s case',
      why: 'Mom asked you to see her home care through until she actually has care. You do the legwork. Mom signs.',
      when: 'Read first',
      steps: [
        s('Mom is the client. She signs every form. Never sign her name.'),
        s('You are her helper: gather papers, make calls with Mom on speaker, fill drafts for her to check, track every date, follow up until it is done.'),
        s('You cannot be her paid caregiver yet. Home Help caregivers must be 18 or older.'),
        s('Keep everything private. Do not text photos of her cards or forms to anyone. Do not post about it.'),
        s('Fill in the Case Log (in the How-To tab, "Mom\'s Home Care Case") every time something happens.')
      ] },
    { id: 'h1-docs', cat: 'homecare', private: true, who: 'Both', title: 'Phase 1 - Gather Mom\'s papers',
      why: 'Every office will ask for these. Have them in one folder before you call anyone.', when: 'Day 1',
      steps: [
        s('Make one folder (paper) and one photo album on Mom\'s phone called "Home Help".'),
        s('Mom\'s photo ID (front and back).'),
        s('Mom\'s Medicaid card (mihealth card) and her Medicaid health plan card, front and back.'),
        s('Any other insurance card (Medicare or private), front and back.'),
        s('A list of Mom\'s doctors and therapists with office phone numbers. Ask Mom which one knows her daily needs best.'),
        s('Mom\'s address and best phone number for the county to call.')
      ] },
    { id: 'h2-portal', cat: 'homecare', private: true, who: 'Both', title: 'Phase 2 - Finish Mom\'s intake in the CCES Care Portal',
      why: 'Mom already started an intake as a client. Finish it so every detail lives in one place.', when: 'Day 1-2',
      steps: [
        s('Open the CCES Care Portal and tap "Family intake".', ['Open CCES Care Portal', PORTAL]),
        s('Ask Mom to sign in or tell you which login to use. Find the intake she already started.'),
        s('Upload the insurance card photos (front and back of each).'),
        s('Fill in Medicaid ID, health plan, availability (days and times she needs help) and her doctor.'),
        s('Leave caseworker and Time & Task blank for now. You add them in later phases.'),
        s('Tap Save. Show Mom the finished intake.')
      ] },
    { id: 'h3-medicaid', cat: 'homecare', private: true, who: 'Both', title: 'Phase 3 - Confirm Mom\'s Medicaid is active',
      why: 'Home Help is a Medicaid program. It only pays when Medicaid is active. Medicare alone does not qualify.', when: 'Day 2',
      steps: [
        s('Sit with Mom while she signs in to MI Bridges.', ['Open MI Bridges', MIB]),
        s('Open Benefits. Find Healthcare Coverage. Check it says Active.'),
        s('Write the case number (last 4 only), the health plan name and the renewal date in the Case Log.'),
        s('If it is not active, pending, or says she has a deductible: tap Apply or Renew with Mom and finish it, then tell the county worker about it when you call.'),
        s('If there is a deductible, Home Help pays only after the deductible is met each month. Write that in the notes.')
      ] },
    { id: 'h4-referral', cat: 'homecare', private: true, who: 'Both', title: 'Phase 4 - Ask the county for Home Help',
      why: 'An Adult Services Worker at the county MDHHS office runs Home Help. Your call starts the case.', when: 'Day 2-3',
      steps: [
        s('Look at the office list in the How-To guide. Call the Oakland office for Mom\'s address. If unsure, call any of them and ask which one covers her address.'),
        s('Mom on speaker. Say: "Hi, I\'m calling with my mom, Ciarne Cyars. She has Medicaid and wants to apply for the Home Help program. Can you refer her to Adult Services?"'),
        s('Ask: "Who will her Adult Services Worker be, and what is their phone, email and fax?"'),
        s('Ask: "Will you mail the DHS-390 application and the DHS-54A medical form, or can we pick them up?"'),
        s('Write the worker\'s name, phone, email, fax and today\'s date in the Case Log.'),
        s('No call back in 5 business days? Call again. Keep calling every 3 days until you have a worker\'s name.')
      ] },
    { id: 'h5-forms', cat: 'homecare', private: true, who: 'Both', title: 'Phase 5 - The two forms (21-day clock)',
      why: 'The worker sends an introduction letter, the DHS-390 Adult Services Application and the DHS-54A Medical Needs form. The letter gives 21 days to return them. Missing forms = denied.', when: 'Starts the day the letter comes',
      steps: [
        s('The day the letter comes: write the date in the Case Log and set "due back by" to 21 days later.'),
        s('Take a photo of every page before anything leaves the house.'),
        s('DHS-390: read each question to Mom and fill in her answers. Mom checks it and signs it herself. The date the office receives her signed form is her application date.'),
        s('DHS-54A: this goes to a Medicaid-enrolled medical professional: a doctor (MD or DO), nurse practitioner, physical therapist or occupational therapist. A physician assistant cannot sign it. Ask Mom which one.'),
        s('Call that office: "My mom needs a DHS-54A Medical Needs form completed for the Michigan Home Help program. How do I get it to the provider?" Drop it off or fax it. Write the date.'),
        s('Call that office every 2 business days until it is signed AND dated. Home Help cannot pay for days before that signature date.'),
        s('Check the signed DHS-54A: provider signature, date, and the daily tasks Mom needs hands-on help with are filled in.')
      ] },
    { id: 'h6-return', cat: 'homecare', private: true, who: 'Both', title: 'Phase 6 - Send both forms back',
      why: 'Get both forms to the worker before the 21-day deadline, with proof you sent them.', when: 'Before day 21',
      steps: [
        s('Send both forms the way the worker said: fax, mail, drop-off or upload.'),
        s('Keep proof: fax confirmation page, mail receipt, or a photo of the drop-off with the date stamp.'),
        s('Write the date and how you sent it in the Case Log.'),
        s('2 business days later, call the worker: "Did you receive Ciarne Cyars\'s DHS-390 and DHS-54A?" Write the date they confirmed.'),
        s('Running late? Call the worker BEFORE day 21 and ask for more time. Write down who you talked to.')
      ] },
    { id: 'h7-visit', cat: 'homecare', private: true, who: 'Both', title: 'Phase 7 - Home assessment visit',
      why: 'The worker visits to see which daily activities Mom needs hands-on help with. Home Help needs at least one daily activity ranked level 3 or higher.', when: 'When the worker schedules it',
      steps: [
        s('Put the visit date and time in the Case Log and on Mom\'s calendar.'),
        s('The night before, Mom writes in her own words what she needs hands-on help with on her hard days (bathing, dressing, getting around, meals, medicine, housework, laundry, shopping).'),
        s('Have the folder ready: ID, cards, copies of both forms.'),
        s('Be there. Take notes. Let Mom answer. She should describe her hardest days honestly, not her best day.'),
        s('Before the worker leaves ask: "When will we get the decision, and how?" Write it down.')
      ] },
    { id: 'h8-decision', cat: 'homecare', private: true, who: 'Both', title: 'Phase 8 - The decision',
      why: 'MDHHS mails an approval or a denial notice.', when: 'After the visit',
      steps: [
        s('Photo the notice the day it comes. Write the date and result in the Case Log.'),
        s('Approved: write the approved tasks and hours (the Time & Task) in the Case Log. Ask the worker for a copy.'),
        s('Denied: find the hearing request deadline on the notice and put it in the Case Log. Tell Mom the same day. Mom decides whether to ask for a hearing.'),
        s('Upload the notice and Time & Task to Mom\'s file in the CCES Care Portal.', ['Open CCES Care Portal', PORTAL])
      ] },
    { id: 'h9-caregiver', cat: 'homecare', private: true, who: 'Both', title: 'Phase 9 - Pick and set up the caregiver',
      why: 'Mom chooses her caregiver: an individual (18 or older) or an agency. Caregivers must enroll in CHAMPS and pass a background check before they can be paid.', when: 'After approval',
      steps: [
        s('Ask the worker in writing (email): "Can Crisp Cares, which my mom owns, be her Home Help agency provider?" Save the reply.'),
        s('If yes: Mom sets it up with Crisp Cares. If no: Mom picks another agency or an individual caregiver (an adult family member or friend).'),
        s('Individual caregiver: they create a MILogin account and fill out the CHAMPS provider enrollment online. That starts the background check.', ['Caregiver CHAMPS steps', 'https://www.michigan.gov/mdhhs/doing-business/providers/providers/other/homehelp/individual-providers/individual-providers']),
        s('Agency caregiver: the agency handles enrollment and links the caregiver to the agency in CHAMPS.'),
        s('Write "CHAMPS enrolled: pending" in the Case Log. Ask the caregiver every week until it is approved (they get a 7-digit provider ID).'),
        s('Mom and the caregiver sign the provider agreement the worker gives them.'),
        s('Tell the worker who the caregiver is and their CHAMPS ID.')
      ] },
    { id: 'h10-start', cat: 'homecare', private: true, who: 'Both', title: 'Phase 10 - Care starts',
      why: 'The goal: a caregiver is coming and getting paid correctly.', when: 'Start date',
      steps: [
        s('Confirm the start date with the worker and the caregiver. Write it in the Case Log.'),
        s('Visits are clocked through EVV (HHAeXchange). Make sure the caregiver can clock in on the first day.'),
        s('After week 1 ask Mom: "Is the caregiver doing the tasks on the Time & Task?" Write the answer in notes.'),
        s('Add the caregiver and start date to Mom\'s file in the CCES Care Portal.', ['Open CCES Care Portal', PORTAL])
      ] },
    { id: 'h11-keep', cat: 'homecare', private: true, who: 'Both', title: 'Phase 11 - Keep it active',
      why: 'Care stops if Medicaid lapses or reviews are missed.', when: 'Every year',
      steps: [
        s('Ask the worker when the next review is and whether a new DHS-54A will be needed. Put both in the Case Log.'),
        s('Put the Medicaid renewal date on the calendar. Help Mom renew on MI Bridges before it is due.', ['Open MI Bridges', MIB]),
        s('Any change (new address, hospital stay, new caregiver): call the worker within a week.'),
        s('Read the official Home Help page with Mom once.', ['Michigan Home Help', HH])
      ] }
  ];
  M.forEach(function (m) { D.missions.push(m); });

  // guide entry for the How-To tab
  if (window.C56M_GUIDES) {
    window.C56M_GUIDES.list.unshift({
      id: 'g-homecare', icon: '🏥', title: "Mom's Home Care Case - start to finish", private: true, homecare: true,
      intro: 'Every step from gathering papers to a caregiver at the door, plus the Case Log and county office list. Work the phases in order (they are also in All Missions).',
      need: ['Mom with you for every call and every signature.', 'The "Home Help" folder (Phase 1).', 'This app open to the Case Log.'],
      routes: [{ name: 'The 12 phases', steps: M.map(function (m) { return { t: m.title + ': ' + m.why, mission: m.id }; }) }],
      after: ['Done means: a CHAMPS-enrolled caregiver is coming on the approved days, and the review and renewal dates are on the calendar.']
    });
    window.C56M_GUIDES.guideFor['h0-role'] = 'g-homecare';
  }
})();
