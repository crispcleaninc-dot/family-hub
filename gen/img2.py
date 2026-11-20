# Fallback stills via Pollinations (FLUX) for shots the HF free quota missed.
import json, os, time, urllib.request, urllib.parse
P = json.load(open('gen/shots.json')); IDS = open('gen/missing.txt').read().split()
STYLE = (", photorealistic cinematic film still, shot on 35mm, natural skin texture, realistic proportions, realistic hands, "
         "shallow depth of field, warm natural lighting, high detail, modest dignified clothing, no text, no watermark")
os.makedirs('out', exist_ok=True)
for sid in IDS:
    q = urllib.parse.quote(P[sid] + STYLE)
    for a in range(5):
        try:
            u = f"https://image.pollinations.ai/prompt/{q}?width=768&height=1344&model=flux&seed=7101&nologo=true"
            b = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=180).read()
            if len(b) < 20000: raise Exception('small ' + str(len(b)))
            open(f'out/{sid}_7101.jpg', 'wb').write(b); print(sid, 'ok', len(b), flush=True); break
        except Exception as e: print(sid, a, e, flush=True); time.sleep(20)
