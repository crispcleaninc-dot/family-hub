import json, os, asyncio, edge_tts
S = json.load(open('gen/story.json')); os.makedirs('out', exist_ok=True)
V = {'mom': ('hi-IN-SwaraNeural', '-4%', '+0Hz'), 'dad': ('hi-IN-MadhurNeural', '-6%', '-4Hz'), 'son': ('hi-IN-MadhurNeural', '+4%', '+18Hz'),
     'verse': ('hi-IN-MadhurNeural', '-10%', '-10Hz'), 'reply': ('hi-IN-SwaraNeural', '-6%', '-6Hz')}
async def main():
    for sid, _, ls in S:
        for i, (r, t) in enumerate(ls):
            v, rate, pitch = V[r]
            for a in range(4):
                try:
                    await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(f'out/{sid}_l{i}.mp3'); print(sid, i, 'ok'); break
                except Exception as e: print(sid, i, 'err', e); await asyncio.sleep(3)
asyncio.run(main())
