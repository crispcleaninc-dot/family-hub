import json, os, asyncio, edge_tts
os.makedirs('out', exist_ok=True)
V = {'india': {'mom': ('en-IN-NeerjaNeural', '+2%', '+0Hz'), 'verse': ('en-IN-NeerjaNeural', '-6%', '-4Hz'), 'reply': ('en-US-AvaMultilingualNeural', '+2%', '+0Hz'),
               'son': ('en-IN-PrabhatNeural', '+6%', '+18Hz'), 'dad': ('en-IN-PrabhatNeural', '-2%', '-6Hz'), 'end': ('en-IN-NeerjaNeural', '+0%', '+0Hz')},
     'africa': {'mom': ('en-NG-EzinneNeural', '+2%', '+0Hz'), 'verse': ('en-NG-EzinneNeural', '-6%', '-4Hz'), 'reply': ('en-US-AvaMultilingualNeural', '+2%', '+0Hz'),
                'pastor': ('en-NG-AbeoNeural', '-2%', '-4Hz'), 'end': ('en-NG-EzinneNeural', '+0%', '+0Hz')}}
async def say(t, v, fn, log):
    voice, rate, pitch = v
    for a in range(5):
        try: await edge_tts.Communicate(t, voice, rate=rate, pitch=pitch).save(fn); log.append(fn + ' ok'); return
        except Exception as e: log.append(f'{fn} err {e}'); await asyncio.sleep(4)
async def main():
    log = []
    for name in ('india', 'africa'):
        d = json.load(open(f'gen/{name}_en.json'))
        for sid, _, lines in d['shots']:
            for i, (r, t) in enumerate(lines): await say(t, V[name][r], f'out/{name}_{sid}_l{i}.mp3', log)
        for i, t in enumerate(d['end']): await say(t, V[name]['end'], f'out/{name}_end{i}.mp3', log)
    open('out/log.txt', 'w').write('\n'.join(log))
asyncio.run(main())
