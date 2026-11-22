import json, asyncio, edge_tts, os
D = json.load(open('gen/dub.json'))
async def main():
    for L, m in D['meta'].items():
        for k, t in D['hook'][L].items():
            for a in range(3):
                try:
                    await edge_tts.Communicate(t, m['voice'], rate='+0%').save(f'out/{L}_{k}.mp3'); break
                except Exception as e: print(L, k, e)
            print(L, k, os.path.getsize(f'out/{L}_{k}.mp3') if os.path.exists(f'out/{L}_{k}.mp3') else 0)
asyncio.run(main())
