import asyncio, edge_tts, json, os
P = {'lil': ('en-GB-SoniaNeural', '-8%', '-2Hz'), 'adam': ('en-US-BrianMultilingualNeural', '-6%', '+0Hz'),
     'angel': ('en-US-GuyNeural', '-10%', '-4Hz')}
L = json.load(open('gen/lines.json'))['chars']; os.makedirs('out', exist_ok=True)
async def main():
    for k, r, t in L:
        v, rate, pitch = P[r]
        for a in range(6):
            try: await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(f'out/{k}.mp3'); print(k, r, 'ok', flush=True); break
            except Exception as e: print(k, e, flush=True); await asyncio.sleep(4)
asyncio.run(main())
