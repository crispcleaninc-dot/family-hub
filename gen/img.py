import json, os, time, shutil
from gradio_client import Client
sid = os.environ['SHOT']; d = json.load(open('gen/films.json'))
p = [s[1] for f, v in d['films'].items() for s in v if f + s[0] == sid][0]
p += ", photorealistic cinematic film still, shot on 35mm, natural skin texture, realistic proportions, realistic hands, shallow depth of field, warm natural lighting, high detail, no text"
os.makedirs('out', exist_ok=True); log = []; c = None
for a in range(5):
    try: c = Client("black-forest-labs/FLUX.1-schnell"); break
    except Exception as e: log.append('client ' + str(e)[:200]); time.sleep(30)
for a in range(4):
    try:
        r = c.predict(prompt=p, seed=7301, randomize_seed=False, width=1344, height=768, num_inference_steps=4, api_name="/infer")
        shutil.copy(r[0] if isinstance(r, (list, tuple)) else r, f'out/{sid}.webp'); log.append(sid + ' ok'); break
    except Exception as e: log.append(f'{sid} try{a} {str(e)[:200]}'); time.sleep(40)
open(f'out/{sid}_log.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
