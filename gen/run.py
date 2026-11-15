import json, os, time, urllib.parse, urllib.request
cfg = json.load(open('gen/prompts.json'))
os.makedirs('gen/out', exist_ok=True)
log = []
for s in cfg['shots']:
    path = f"gen/out/{s['id']}.jpg"
    if os.path.exists(path): continue
    prompt = s['p'] + ', ' + cfg['style']
    url = ('https://image.pollinations.ai/prompt/' + urllib.parse.quote(prompt) +
           f"?width=768&height=1344&seed={s['seed']}&model=flux&nologo=true&private=true")
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=180).read()
            if len(data) > 20000:
                open(path, 'wb').write(data); log.append(f"{s['id']} ok {len(data)}"); break
            log.append(f"{s['id']} small {len(data)}")
        except Exception as e:
            log.append(f"{s['id']} err {e}")
        time.sleep(20)
    time.sleep(8)
open('gen/out/log.txt', 'w').write('\n'.join(log))
print('\n'.join(log))
