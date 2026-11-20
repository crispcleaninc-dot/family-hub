import os, time, shutil, sys, urllib.parse, urllib.request
sys.path.insert(0, 'gen'); from shots import SHOTS, NEG
os.makedirs('out', exist_ok=True); log = []
ids = os.environ['SHOTS'].split(',')
c = None
try:
    from gradio_client import Client
    for a in range(3):
        try: c = Client("black-forest-labs/FLUX.1-schnell"); break
        except Exception as e: log.append('client ' + str(e)[:150]); time.sleep(20)
except Exception as e: log.append('noclient ' + str(e)[:100])
for sid in ids:
    p = SHOTS[sid] + NEG; ok = False
    if c:
        for a in range(2):
            try:
                r = c.predict(prompt=p, seed=4242, randomize_seed=False, width=1344, height=768, num_inference_steps=4, api_name="/infer")
                shutil.copy(r[0] if isinstance(r, (list, tuple)) else r, f'out/{sid}.webp'); ok = True; log.append(sid + ' flux'); break
            except Exception as e: log.append(f'{sid} flux{a} {str(e)[:150]}'); time.sleep(15)
    if not ok:
        u = 'https://image.pollinations.ai/prompt/' + urllib.parse.quote(p) + '?width=1344&height=768&seed=4242&nologo=true&model=flux'
        for a in range(3):
            try:
                urllib.request.urlretrieve(u, f'out/{sid}.jpg'); ok = os.path.getsize(f'out/{sid}.jpg') > 20000
                if ok: log.append(sid + ' poll'); break
            except Exception as e: log.append(f'{sid} poll{a} {str(e)[:150]}'); time.sleep(20)
open('out/log_' + ids[0] + '.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
