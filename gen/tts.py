import json, os, asyncio, edge_tts
cfg=json.load(open('gen/tts.json')); os.makedirs('gen/tts_out',exist_ok=True)
async def one(it):
    p=f"gen/tts_out/{it['id']}.mp3"
    if os.path.exists(p): return
    c=edge_tts.Communicate(it['text'],it.get('voice','en-US-AnaNeural'),rate=it.get('rate','+0%'),pitch=it.get('pitch','+0Hz'))
    await c.save(p)
async def main():
    for it in cfg['lines']:
        for a in range(4):
            try: await one(it); break
            except Exception as e: print(it['id'],e); await asyncio.sleep(5)
asyncio.run(main())
