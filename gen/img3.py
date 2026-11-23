# Cinematic stills (FLUX.1-schnell, Pollinations fallback) + depth map for each (Depth-Anything-V2-Small).
import json, os, time, shutil, urllib.parse, urllib.request
sid = os.environ['SHOT']; p = json.load(open('gen/shots3.json'))[sid]
STYLE = (", epic biblical movie film still, cinematic anamorphic composition with clear foreground, midground and background layers, "
         "dramatic volumetric light, atmospheric haze, rich warm color grade, photorealistic, realistic hands and faces, "
         "historically accurate ancient Near East, modest dignified clothing, no text, no watermark")
os.makedirs('out', exist_ok=True); log = []; c = None
try:
    from gradio_client import Client
    for a in range(3):
        try: c = Client("black-forest-labs/FLUX.1-schnell"); break
        except Exception as e: log.append('client ' + str(e)[:200]); time.sleep(20)
except Exception as e: log.append('import ' + str(e)[:100])
for sd in [7201, 7202]:
    ok = False
    for a in range(3 if c else 0):
        try:
            r = c.predict(prompt=p + STYLE, seed=sd, randomize_seed=False, width=768, height=1344, num_inference_steps=4, api_name="/infer")
            f = r[0] if isinstance(r, (list, tuple)) else r
            shutil.copy(f, f'out/{sid}_{sd}.webp'); log.append(f'{sid}_{sd} flux ok'); ok = True; break
        except Exception as e:
            log.append(f'{sid}_{sd} try{a} {str(e)[:160]}'); time.sleep(30)
    if not ok:
        u = 'https://image.pollinations.ai/prompt/' + urllib.parse.quote(p + STYLE) + f'?width=768&height=1344&seed={sd}&nologo=true&model=flux'
        for a in range(3):
            try:
                req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
                data = urllib.request.urlopen(req, timeout=180).read()
                if len(data) > 20000: open(f'out/{sid}_{sd}.jpg', 'wb').write(data); log.append(f'{sid}_{sd} poll ok'); break
            except Exception as e: log.append(f'{sid}_{sd} poll{a} {str(e)[:120]}'); time.sleep(20)
open(f'out/{sid}_log.txt', 'w').write('\n'.join(log)); print('\n'.join(log))
