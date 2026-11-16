import json, os, time, urllib.parse, urllib.request
cfg=json.load(open('gen/prompts.json')); os.makedirs('gen/out',exist_ok=True); log=[]
for sid,seed,kind,p in cfg['shots']:
    path=f'gen/out/{sid}.jpg'
    if os.path.exists(path): continue
    w,h={'bg':(1024,1100),'scene':(896,1120),'char':(640,1024)}.get(kind,(768,768))
    url='https://image.pollinations.ai/prompt/'+urllib.parse.quote(p+cfg[kind+'style'])+f'?width={w}&height={h}&seed={seed}&model=flux&nologo=true&private=true'
    for a in range(8):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=180).read()
            if len(d)>15000: open(path,'wb').write(d); log.append(f'{sid} ok {len(d)}'); break
            log.append(f'{sid} small')
        except Exception as e: log.append(f'{sid} err {e}')
        time.sleep(25)
    time.sleep(6)
open('gen/out/log.txt','w').write('\n'.join(log)); print('\n'.join(log))
