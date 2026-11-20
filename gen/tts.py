import json, os, asyncio, edge_tts
S = json.load(open('gen/end.json')); os.makedirs('out', exist_ok=True)
async def main():
    for k, v, rate, t in S:
        for a in range(4):
            try:
                await edge_tts.Communicate(t, v, rate=rate).save(f'out/{k}.mp3'); print(k, 'ok'); break
            except Exception as e: print(k, 'err', e); await asyncio.sleep(3)
asyncio.run(main())
