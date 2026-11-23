import json, glob, os
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8')
res = {}
for f in sorted(glob.glob('aud/*.wav')):
    lang = os.path.basename(f)[:2]
    segs, info = m.transcribe(f, language=lang, beam_size=1)
    res[os.path.basename(f)] = ' '.join(s.text.strip() for s in segs)
    print(os.path.basename(f), res[os.path.basename(f)], flush=True)
os.makedirs('out', exist_ok=True); json.dump(res, open('out/asr.json', 'w'), ensure_ascii=False, indent=0)
