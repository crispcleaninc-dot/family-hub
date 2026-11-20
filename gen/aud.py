import asyncio, edge_tts, os, json
os.makedirs('out', exist_ok=True)
async def main():
    vs = await edge_tts.list_voices()
    names = [v['ShortName'] for v in vs]
    json.dump(names, open('out/voices.json', 'w'))
    S = json.load(open('gen/aud.json'))
    for role, opts in S.items():
        for i, (v, rate, pitch, text) in enumerate(opts):
            if v not in names: print('missing', v); continue
            for a in range(3):
                try: await edge_tts.Communicate(text, v, rate=rate, pitch=pitch).save(f'out/{role}_{i}.mp3'); break
                except Exception as e: print(role, i, e); await asyncio.sleep(3)
            for a in range(3):
                try: await edge_tts.Communicate(f"Option number {i+1}.", 'en-US-AndrewNeural').save(f'out/{role}_{i}_label.mp3'); break
                except Exception as e: print('label', e); await asyncio.sleep(3)
asyncio.run(main())
