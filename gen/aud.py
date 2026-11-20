# Accent auditions: each voice reads KJV lines; whisper scores clarity (word error rate).
import asyncio, edge_tts, json, os, re
from faster_whisper import WhisperModel
import jiwer
T = ["Yea, hath God said, Ye shall not eat of every tree of the garden?",
     "I know not: Am I my brother's keeper?",
     "Surely the LORD is in this place; and I knew it not."]
V = ["he-IL-AvriNeural", "he-IL-HilaNeural", "ar-JO-TaimNeural", "ar-JO-SanaNeural", "ar-LB-RamiNeural", "ar-LB-LaylaNeural",
     "ar-SY-LaithNeural", "ar-SY-AmanyNeural", "ar-EG-ShakirNeural", "ar-EG-SalmaNeural", "ar-IQ-BasselNeural", "ar-IQ-RanaNeural",
     "ar-SA-HamedNeural", "ar-SA-ZariyahNeural", "fa-IR-FaridNeural", "fa-IR-DilaraNeural", "tr-TR-AhmetNeural", "tr-TR-EmelNeural",
     "en-NG-AbeoNeural", "en-NG-EzinneNeural", "en-KE-ChilembaNeural", "en-KE-AsiliaNeural", "en-TZ-ElimuNeural", "en-TZ-ImaniNeural",
     "en-IN-PrabhatNeural", "en-IN-NeerjaNeural", "en-GB-RyanNeural", "en-GB-SoniaNeural", "en-US-AndrewMultilingualNeural",
     "en-US-AvaMultilingualNeural", "en-US-BrianMultilingualNeural", "en-US-EmmaMultilingualNeural", "en-GB-ThomasNeural", "en-AU-WilliamNeural"]
def norm(s): return re.sub(r"[^a-z' ]", "", s.lower())
async def main():
    os.makedirs('out/aud', exist_ok=True)
    for v in V:
        for i, t in enumerate(T):
            for a in range(3):
                try: await edge_tts.Communicate(t, v, rate='-6%').save(f'out/aud/{v}_{i}.mp3'); break
                except Exception as e: print(v, i, e); await asyncio.sleep(3)
asyncio.run(main())
m = WhisperModel("small.en", device="cpu", compute_type="int8")
R = {}
for v in V:
    w = []
    for i, t in enumerate(T):
        f = f'out/aud/{v}_{i}.mp3'
        if not os.path.exists(f) or os.path.getsize(f) < 1000: w.append(1.0); continue
        hyp = " ".join(s.text for s in m.transcribe(f, language="en")[0])
        w.append(round(jiwer.wer(norm(t), norm(hyp)), 3)); print(v, i, hyp, flush=True)
    R[v] = w
json.dump(R, open('out/aud_wer.json', 'w'), indent=1)
