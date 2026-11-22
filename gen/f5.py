import os, json, traceback, time
k = os.environ['K']; items = json.load(open('gen/lines.json'))['her'][k]
REF_T = "The first one swung, the bottle was already in my hand. When it was over, her tooth was gone, and I was the one the police wanted."
os.makedirs('out', exist_ok=True)
from f5_tts.api import F5TTS
tts = F5TTS(model='F5TTS_v1_Base')
for sid, text, role in items:
    t0 = time.time()
    try:
        tts.infer(ref_file='gen/her.wav', ref_text=REF_T, gen_text=text, speed=(0.98 if role == 'H' else 0.9),
                  nfe_step=40, cfg_strength=2.2, seed=77, remove_silence=False, file_wave=f'out/{sid}.wav')
        print(sid, 'ok', round(time.time() - t0), flush=True)
    except Exception:
        print(sid, 'FAIL', traceback.format_exc()[-800:], flush=True)
