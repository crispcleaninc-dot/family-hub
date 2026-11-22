import asyncio, edge_tts, json, os
P = {'NAR': ('en-US-ChristopherNeural', '-8%', '-3Hz'), 'god': ('en-US-AndrewMultilingualNeural', '-12%', '-6Hz'),
     'pharaoh': ('en-GB-ThomasNeural', '-8%', '-2Hz'), 'midwife': ('en-NG-EzinneNeural', '-4%', '+0Hz'),
     'miriam': ('en-KE-AsiliaNeural', '+0%', '+6Hz'), 'pdaughter': ('en-GB-SoniaNeural', '-4%', '+0Hz'),
     'moses': ('en-NG-AbeoNeural', '-6%', '+0Hz'), 'hebrew': ('en-AU-WilliamNeural', '-4%', '+0Hz')}
L = json.load(open('gen/lines.json'))['chars']; os.makedirs('out', exist_ok=True)
async def main():
    for k, r, t in L:
        v, rate, pitch = P[r]
        for a in range(6):
            try: await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(f'out/{k}.mp3'); print(k, r, 'ok', flush=True); break
            except Exception as e: print(k, e, flush=True); await asyncio.sleep(4)
asyncio.run(main())
