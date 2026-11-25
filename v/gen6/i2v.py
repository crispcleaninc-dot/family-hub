import os, time, shutil, json, traceback
from gradio_client import Client, handle_file
M = json.load(open('gen6/motion.json'))
ids = os.environ['SHOTS'].split(',')
SPACES = ["zerogpu-aoti/wan2-2-fp8da-aoti-faster", "r3gm/wan2-2-fp8da-aoti-preview2", "zerogpu-aoti/wan2-2-fp8da-aoti", "linoyts/wan2-2-i2v-rCM", "KingNish/wan2-2-fast"]
os.makedirs('out', exist_ok=True); log = []
NEG = "static, frozen, blurry, distorted faces, extra limbs, text, watermark, logo, cartoon"
def call(c, sid):
    api = c.view_api(return_format='dict', print_info=False)
    eps = api.get('named_endpoints', {})
    name = next((k for k in eps if 'generate' in k), None) or next(iter(eps))
    params = eps[name]['parameters']
    kw = {}
    for p in params:
        n = p['parameter_name']
        if n in ('input_image','image','start_image'): kw[n] = handle_file(f'gen6/{sid}.webp')
        elif n in ('prompt',): kw[n] = M[sid] + ", cinematic biblical film, realistic motion, ancient Israel"
        elif 'negative' in n: kw[n] = NEG
        elif n in ('duration_seconds','duration'): kw[n] = 3.5
        elif n == 'steps': kw[n] = 6
        elif n == 'randomize_seed': kw[n] = False
        elif n == 'seed': kw[n] = 4242
    log.append(f'{sid} {name} {list(kw)}')
    r = c.predict(api_name=name, **kw)
    v = r[0] if isinstance(r, (list, tuple)) else r
    if isinstance(v, dict): v = v.get('video') or v.get('path') or v.get('value')
    return v
for sid in ids:
    done = False
    for sp in SPACES:
        if done: break
        for a in range(2):
            try:
                c = Client(sp)
                v = call(c, sid)
                shutil.copy(v, f'out/{sid}.mp4'); log.append(f'{sid} ok via {sp}'); done = True; break
            except Exception as e:
                log.append(f'{sid} {sp} fail{a} {str(e)[:200]}'); time.sleep(15)
open('out/log_' + ids[0] + '.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
