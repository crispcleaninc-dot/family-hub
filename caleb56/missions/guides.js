/* Caleb #56 Missions - turnkey How-To guides (V2.34).
 * Each guide: need[] (have this before you start), routes[] (ways to do it, each with numbered steps),
 * after[] (checklist when it arrives / when done). A step: { t: what to do, go: [label, url] optional, tip: optional }.
 * guideFor maps a mission id to the guide that walks it through.
 */
window.C56M_GUIDES = {
  guideFor: { 'b-buds': 'g-buds', 'b-phone': 'g-phone', 'w-onboard': 'g-homebase', 'w-clock': 'g-homebase', 'w-standup': 'g-teams', 'f-account': 'g-foundation', 's-passport': 'g-passport' },
  list: [
    {
      id: 'g-buds', icon: '🎧', title: 'Order earbuds in bulk',
      intro: 'You will pick a pack online, send it to Mom for a yes, and she checks out. You never type in a card number.',
      need: [
        'Mom said yes and gave you a budget (a 50- or 100-pack is about $25-$55).',
        'Know your plug. iPhone 15 or newer = USB-C. iPhone 14 or older = Lightning. Most Android = USB-C. Laptops and Chromebooks = round headphone jack (3.5 mm).',
        'Cheap bulk earbuds have the round 3.5 mm plug. If your phone has no round jack, you also need one adapter (Apple sells one for about $9). Or buy a USB-C pack instead (Route C).'
      ],
      routes: [
        { name: 'Route A - DollarDays (cheapest per pair)', steps: [
          { t: 'Open DollarDays.', go: ['Open DollarDays earbuds', 'https://www.dollardays.com/wholesale-headphones.html'] },
          { t: 'Look for "Single Use Stereo Earbuds" (100 in a case) or "Wired Earbuds - Assorted Colors" (144 in a case).', tip: 'The price shown is PER PAIR. Case total = price x pairs in the case.' },
          { t: 'Tap the item. Check the case size, the price per unit, and the shipping cost in the cart.' },
          { t: 'Tap Add to Cart, then STOP. Do not check out.' },
          { t: 'Copy the page link (Share > Copy link) and fill out "Ask Mom to approve" below.' },
          { t: 'Mom checks out and ships it to the house.' }
        ] },
        { name: 'Route B - eBay bulk lots (if you want 25 or 50)', steps: [
          { t: 'Open the eBay store that sells bulk earbud lots.', go: ['Open eBay store', 'https://www.ebay.com/str/theblackvault'] },
          { t: 'In the store search box type: earbuds 50  (or 25, or 100).' },
          { t: 'Pick a listing that says New, Individually bagged, and U.S. Shipper.' },
          { t: 'Check the seller: feedback 98% or higher, and Returns accepted.' },
          { t: 'Copy the listing link and send it to Mom with the form below. Do not tap Buy It Now.' }
        ] },
        { name: 'Route C - USB-C earbuds (no adapter needed)', steps: [
          { t: 'Open Amazon or Walmart.', go: ['Search Amazon', 'https://www.amazon.com/s?k=bulk+usb-c+wired+earbuds+pack'] },
          { t: 'Search: bulk USB-C wired earbuds pack' },
          { t: 'Pick one with 4 stars or more and at least 100 ratings. Check that it says USB-C.' },
          { t: 'Divide the price by the number in the pack. It should be well under $7 a pair.' },
          { t: 'Send the link to Mom with the form below.' }
        ] }
      ],
      after: ['Count the pairs when the box comes and type the number in "My stuff" below.', 'Keep the box in one spot in your room.',
        'Take one pair at a time and tap "Used one".', 'When 5 are left, start this guide again.']
    },
    {
      id: 'g-phone', icon: '📱', title: 'Find a cheaper phone (for you)',
      intro: 'You research. Mom decides and pays. Mom also handles the phone line, because the family plan is hers.',
      need: [
        'Mom said yes and gave you a top price.',
        'Your Apple ID or Google account password, so you can move your stuff.',
        'A backup of your current phone (iPhone: Settings > your name > iCloud > iCloud Backup > Back Up Now).'
      ],
      pick: [
        'Best value: iPhone 13 or iPhone 14, 128GB, UNLOCKED.',
        'iPhone 14 or newer also has Emergency SOS by satellite for no-signal spots.',
        'Skip 64GB (fills up fast). Skip anything that says locked to Verizon, Cricket, Boost or another carrier.'
      ],
      routes: [
        { name: 'Route 1 - Apple Certified Refurbished (safest)', steps: [
          { t: 'Open Apple\'s refurbished iPhone page.', go: ['Open Apple Refurbished', 'https://www.apple.com/shop/refurbished/iphone'] },
          { t: 'Pick the model and 128GB. Apple\'s refurbished iPhones are unlocked and come with a new battery, a new outer shell and a 1-year warranty.' },
          { t: 'If your model is not listed, check again in a few days. Apple\'s stock changes.' },
          { t: 'Copy the link and send it to Mom with the form below.' }
        ] },
        { name: 'Route 2 - Amazon Renewed Premium', steps: [
          { t: 'Open Amazon and search: iPhone 14 128GB unlocked Renewed Premium', go: ['Search Amazon', 'https://www.amazon.com/s?k=iPhone+14+128GB+unlocked+Renewed+Premium'] },
          { t: 'Open a listing. The badge must say "Renewed Premium", not just "Renewed".', tip: 'Premium means battery over 90% and a 365-day return window in the US. Plain Renewed is only 80% battery and 90 days.' },
          { t: 'Check the title says Unlocked.' },
          { t: 'Copy the link and send it to Mom.' }
        ] },
        { name: 'Route 3 - Back Market', steps: [
          { t: 'Open Back Market and search your model.', go: ['Open Back Market', 'https://www.backmarket.com/en-us'] },
          { t: 'Choose: Unlocked, 128GB, condition "Excellent".' },
          { t: 'Back Market gives a 1-year warranty and 30-day returns. Read the battery note on the page.' },
          { t: 'Copy the link and send it to Mom.' }
        ] }
      ],
      after: [
        'Open the box with Mom the day it arrives.',
        'Dial *#06# and write down the IMEI number.',
        'Check the IMEI at swappa.com/esn: it must say clean (not lost, stolen or owing money).',
        'iPhone: Settings > Battery > Battery Health. Write the percent. Under 85% = tell Mom.',
        'iPhone: Settings > General > About > Carrier Lock must say "No SIM restrictions".',
        'It must NOT ask for someone else\'s Apple ID (Activation Lock). If it does, stop and tell Mom.',
        'Mom moves the phone line onto it.',
        'Test: call, text, camera, charging, speaker, Face ID or fingerprint.',
        'If anything fails, Mom returns it before the return window ends.'
      ],
      links: [['IMEI check (Swappa)', 'https://swappa.com/esn']]
    },
    {
      id: 'g-bulkphones', icon: '📦', title: 'Help Mom research phones in bulk (family network)',
      intro: 'Mom wants newer phones bought wholesale for the family network. Your job is the research list. Mom opens the business account and buys.',
      need: ['Ask Mom which models and how many.', 'A Google Sheet or the notes app for your list.'],
      routes: [
        { name: 'Your research list', steps: [
          { t: 'For each phone write: model, storage, condition, price, warranty, return days, link.' },
          { t: 'Check Apple Refurbished, Amazon Renewed Premium and Back Market first (the safe sources).', go: ['Apple Refurbished', 'https://www.apple.com/shop/refurbished/iphone'] },
          { t: 'Only unlocked phones. iPhone XS or newer (or a recent Pixel/Galaxy) for eSIM. iPhone 14 or newer for satellite texting.' },
          { t: 'Sort cheapest to most expensive and send Mom the list.' }
        ] },
        { name: 'Back Market Pro (Mom does this part)', steps: [
          { t: 'Back Market Pro is Back Market\'s store for businesses.', go: ['Back Market Pro', 'https://pro.backmarket.com/'] },
          { t: 'Mom creates the business account with her company details.' },
          { t: 'Mom picks the phones, checks delivery and billing, and pays by card or bank transfer.' },
          { t: 'Delivery is usually 3-5 business days. Then run the phone checklist on every phone.' }
        ] }
      ],
      after: ['Every phone gets the same arrival checks as your own phone (IMEI, battery, unlocked, no Activation Lock).']
    },
    {
      id: 'g-homebase', icon: '⏱️', title: 'Homebase: set up and clock in',
      intro: 'Homebase is where your work shifts and hours live. Your hours there are how you get paid.',
      need: ['Your phone number and email that Mom used for your invite.', 'Ask Mom to resend the invite if you cannot find it.'],
      routes: [
        { name: 'First time', steps: [
          { t: 'Find the Homebase invite text or email on your phone and tap the link.' },
          { t: 'Make your password and finish your profile.' },
          { t: 'Download the Homebase app.', go: ['Get Homebase', 'https://joinhomebase.com/'] },
          { t: 'Sign in with the same email and password.' }
        ] },
        { name: 'Every shift', steps: [
          { t: 'Open the Homebase app and tap Clock In when you start.' },
          { t: 'Tap Clock Out when you finish.' },
          { t: 'Forgot? Text Mom your real start and end time the same day.' }
        ] }
      ],
      after: ['Tell Mom when you can see your schedule in the app.']
    },
    {
      id: 'g-teams', icon: '💬', title: 'Post your standup in Teams',
      intro: 'Your standup is 3 short lines after each work day.',
      need: ['Your Crisp work email and password (ask Mom if you do not have them).'],
      routes: [
        { name: 'Steps', steps: [
          { t: 'Download Microsoft Teams and sign in with your Crisp work email.', go: ['Microsoft Teams', 'https://www.microsoft.com/microsoft-teams/download-app'] },
          { t: 'Open Teams > Crisp Clean > the "DSU Daily Stand Ups" channel.' },
          { t: 'Tap New post and type: Yesterday I... / Today I will... / Blockers: ...' },
          { t: 'Post only for yourself.' }
        ] }
      ],
      after: ['Do it every work day.']
    },
    {
      id: 'g-foundation', icon: '🤝', title: 'Get into your Foundation app',
      intro: 'The Foundation app is where your 501(c)(3) plan, packet and document uploads live.',
      need: ['An email you check.', 'A password you will remember.'],
      routes: [
        { name: 'Steps', steps: [
          { t: 'Open the Foundation app.', go: ['Open Foundation app', 'https://script.google.com/macros/s/AKfycbzxnz8F3MI0EKpsSnJgETgk7LTYzI3B2CA6dB-wqYC7FXXI2Oa52kvAxVModttpuN9l/exec'] },
          { t: 'Create your account with your email and a password.' },
          { t: 'Text Mom: "I signed up for the Foundation app. Please approve me as Youth Founder."' },
          { t: 'After she approves, sign in and open the Launch tab. Read the 10 steps.' },
          { t: 'Forgot your password? Use "Forgot password" on the sign-in screen. A code comes to your email.' }
        ] }
      ],
      after: ['Upload your mission and board list in the Launch tab.']
    },
    {
      id: 'g-passport', icon: '🛂', title: 'Get your passport (under 16)',
      intro: 'Under 16 you apply in person with form DS-11.',
      need: ['Your birth certificate (original) plus a photocopy.', 'Both parents there, or the other parent\'s signed consent form (DS-3053).', 'Parent ID.', 'A passport photo.', 'Fees (Mom pays).'],
      routes: [
        { name: 'Steps', steps: [
          { t: 'Read the official under-16 page with Mom.', go: ['travel.state.gov under 16', 'https://travel.state.gov/content/travel/en/passports/need-passport/under-16.html'] },
          { t: 'Fill out form DS-11 online and print it. Do NOT sign it until the agent tells you to.' },
          { t: 'Find a passport acceptance place near you and book a time.', go: ['Find a location', 'https://travel.state.gov/content/travel/en/passports/need-passport/apply-in-person.html'] },
          { t: 'Go with Mom (and your dad, or bring his signed consent form).' },
          { t: 'Write down the application tracking info.' }
        ] }
      ],
      after: ['When it arrives, upload the details and photo on the Passports trip site (due Aug 2027).']
    }
  ]
};
