# Score accent auditions (whisper word error rate), assign voices per character, render all character lines.
import asyncio, edge_tts, json, os, re, subprocess, glob
from faster_whisper import WhisperModel
import jiwer
T = ["Yea, hath God said, Ye shall not eat of every tree of the garden?", "I know not: Am I my brother's keeper?",
     "Surely the LORD is in this place; and I knew it not."]
def norm(s): return re.sub(r"[^a-z' ]", "", s.lower())
m = WhisperModel("small.en", device="cpu", compute_type="int8")
R = {}
for f in sorted(glob.glob('aud/*.mp3')):
    v, i = os.path.basename(f)[:-4].rsplit('_', 1); i = int(i)
    if os.path.getsize(f) < 1000: w = 1.0
    else:
        hyp = " ".join(s.text for s in m.transcribe(f, language="en")[0]); w = jiwer.wer(norm(T[i]), norm(hyp))
    R.setdefault(v, [1.0, 1.0, 1.0])[i] = round(w, 3)
os.makedirs('out/chars', exist_ok=True)
score = {v: sum(w) / 3 for v, w in R.items()}
json.dump({'wer': R, 'avg': score}, open('out/wer.json', 'w'), indent=1)
ME = ['he-IL-AvriNeural', 'ar-LB-RamiNeural', 'ar-JO-TaimNeural', 'ar-SY-LaithNeural', 'ar-IQ-BasselNeural', 'ar-EG-ShakirNeural', 'ar-SA-HamedNeural', 'fa-IR-FaridNeural', 'tr-TR-AhmetNeural']
FE = ['he-IL-HilaNeural', 'ar-LB-LaylaNeural', 'ar-JO-SanaNeural', 'ar-SY-AmanyNeural', 'ar-IQ-RanaNeural', 'ar-EG-SalmaNeural', 'ar-SA-ZariyahNeural', 'fa-IR-DilaraNeural', 'tr-TR-EmelNeural']
ok = lambda v: score.get(v, 1) <= 0.2
men = [v for v in ME if ok(v)] + ['en-US-BrianMultilingualNeural', 'en-US-AndrewMultilingualNeural', 'en-GB-RyanNeural', 'en-GB-ThomasNeural']
wom = [v for v in FE if ok(v)] + ['en-US-AvaMultilingualNeural', 'en-US-EmmaMultilingualNeural', 'en-GB-SoniaNeural']
MROLES = ['god', 'serpent', 'adam', 'cain', 'abram', 'jacob', 'esau', 'laban', 'joseph', 'brother', 'isaac', 'isaac2', 'isaacold', 'visitor', 'crowd', 'angel']
FROLES = ['eve', 'hagar', 'sarah', 'rebekah']
pick = {}
pick['god'] = ('en-US-AndrewMultilingualNeural', '-12%', '-6Hz')
pick['serpent'] = (men[0], '-10%', '-2Hz')
pick['angel'] = ('en-US-BrianMultilingualNeural', '-8%', '+0Hz')
rot = [r for r in MROLES if r not in pick]
for j, r in enumerate(rot): pick[r] = (men[(j + 1) % len(men)], '-6%', '+0Hz')
pick['isaacold'] = (pick['isaacold'][0], '-14%', '-4Hz')
pick['isaac'] = (men[0], '+2%', '+18Hz')
for j, r in enumerate(FROLES): pick[r] = (wom[j % len(wom)], '-5%', '+0Hz')
json.dump(pick, open('out/voices.json', 'w'), indent=1)
L = json.load(open('gen/lines.json'))['chars']
async def main():
    for k, r, t in L:
        v, rate, pitch = pick[r]
        for a in range(4):
            try: await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(f'out/chars/{k}.mp3'); print(k, r, v, 'ok', flush=True); break
            except Exception as e: print(k, e, flush=True); await asyncio.sleep(3)
asyncio.run(main())
