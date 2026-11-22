import asyncio, edge_tts, json, os
P = {'god': ('en-US-AndrewMultilingualNeural', '-12%', '-6Hz'), 'elijah': ('en-KE-ChilembaNeural', '-6%', '-2Hz'),
     'ahab': ('en-AU-WilliamNeural', '-6%', '+0Hz'), 'nathan': ('en-GB-ThomasNeural', '-6%', '+0Hz'),
     'david': ('en-US-BrianMultilingualNeural', '-6%', '+0Hz'), 'jeremiah': ('en-TZ-ElimuNeural', '-8%', '+0Hz'),
     'amos': ('en-NG-AbeoNeural', '-6%', '+0Hz'), 'amaziah': ('en-IN-PrabhatNeural', '-6%', '+0Hz'),
     'john': ('en-GB-RyanNeural', '-6%', '-2Hz')}
L = json.load(open('gen/lines.json'))['chars']; os.makedirs('out', exist_ok=True)
async def main():
    for k, r, t in L:
        v, rate, pitch = P[r]
        for a in range(6):
            try: await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(f'out/{k}.mp3'); print(k, r, 'ok', flush=True); break
            except Exception as e: print(k, e, flush=True); await asyncio.sleep(4)
asyncio.run(main())
