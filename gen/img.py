import os, time, shutil, sys
sys.path.insert(0, 'gen'); from shots import SHOTS, NEG
from gradio_client import Client
os.makedirs('out', exist_ok=True); log = []
ids = os.environ['SHOTS'].split(','); c = None
for a in range(3):
    try: c = Client("black-forest-labs/FLUX.1-schnell"); break
    except Exception as e: log.append('client ' + str(e)[:150]); time.sleep(20)
for sid in ids:
    for a in range(3):
        try:
            r = c.predict(prompt=SHOTS[sid] + NEG, seed=1211 + a, randomize_seed=False, width=1344, height=768, num_inference_steps=4, api_name="/infer")
            shutil.copy(r[0] if isinstance(r, (list, tuple)) else r, f'out/{sid}.webp'); log.append(sid + ' ok'); break
        except Exception as e: log.append(f'{sid} fail{a} {str(e)[:160]}'); time.sleep(30)
open('out/log_' + ids[0] + '.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
