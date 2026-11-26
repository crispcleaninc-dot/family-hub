# Amir's World (installable)

Live: https://crispcleaninc-dot.github.io/family-hub/amir/

Moved Nov 26, 2026 from the "amir" Apps Script project (crispcleaninc) into Family Hub so it installs on phones, tablets and computers.
Every screen and feature from the Apps Script version is carried over unchanged: Learn Words (adaptive, phonics), Match It, ABC, Colors,
Shapes, Music Time, Peppa Pig, Watch Videos, Camera Fun, My Trophies, AI Magic Lesson, Story Time & Build-a-Book, Find It, Count With Me,
Animal Sounds, Where Is Your…?, For Grown-Ups (10 minutes, words he says, CDC milestones), Dior helper, daily lessons, stars and levels.

## What changed
- Installable + works offline (manifest, sw.js, icons), Cyars Notify bell, Samsung install guard, listed in Family Hub + Command Center.
- Amir's photo is built in (put back Nov 26 at her request). Grown-ups can swap it on a device and go back to the original.
- Font: Andika (clear print letters made for early readers, saved with the app so it works offline) replaces the cursive fallback.
- AI model updated from claude-sonnet-4-6 to claude-haiku-5-5.
- Optional relay (below) so AI needs no key on the tablet and progress backs up to Google.

## Turning on the relay (one time)
1. Open the "amir" Apps Script project in crispcleaninc. Replace Code.gs with `relay/Code.gs` (everything old is kept; doPost is added at the bottom).
2. Project Settings › Script Properties: `ANTHROPIC_API_KEY` = her key. Optional: `DAILY_LIMIT` (default 60), `MODEL`.
3. Deploy › New deployment › Web app › Execute as Me › Anyone. Copy the /exec link into `amir/config.js` → `AMIR_RELAY`.
Until then everything works; AI uses a key saved with the ⚙️ button and progress stays on the device.
