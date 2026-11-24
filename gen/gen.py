import json
from f5_tts.api import F5TTS
lines = json.load(open('gen/lines.json'))
ref_text = "It started under a picture online. Two girls I barely knew decided I was the problem. Comments turned into messages, messages turned into I know where you stay."
tts = F5TTS(model="F5TTS_v1_Base")
for k, t in lines:
    try:
        tts.infer(ref_file='gen/ref.wav', ref_text=ref_text, gen_text=t, file_wave='out/' + k + '.wav', speed=0.95)
        print(k, 'ok', flush=True)
    except Exception as e:
        print(k, 'ERR', e, flush=True)
