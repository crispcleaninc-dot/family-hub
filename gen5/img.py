import os, time, shutil, json
SH = json.load(open('gen5/shots.json'))
from gradio_client import Client
os.makedirs('out', exist_ok=True); log = []
ids = os.environ['SHOTS'].split(','); c = None
NEG = ", no text, no watermark, no logos"
for a in range(3):
    try: c = Client("black-forest-labs/FLUX.1-schnell"); break
    except Exception as e: log.append('client ' + str(e)[:150]); time.sleep(20)
for sid in ids:
    p, w, h = SH[sid]
    for a in range(3):
        try:
            r = c.predict(prompt=p + NEG, seed=8121 + a, randomize_seed=False, width=w, height=h, num_inference_steps=4, api_name="/infer")
            shutil.copy(r[0] if isinstance(r, (list, tuple)) else r, f'out/{sid}.webp'); log.append(sid + ' ok'); break
        except Exception as e: log.append(f'{sid} fail{a} {str(e)[:150]}'); time.sleep(30)
open('out/log_' + ids[0] + '.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
