import json, os, asyncio, edge_tts
os.makedirs('out', exist_ok=True)
V = {'mom': ('en-US-EmmaMultilingualNeural', '+0%'), 'end': ('en-US-EmmaMultilingualNeural', '+0%'), 'verse': ('en-US-AndrewMultilingualNeural', '-6%'),
     'reply': ('en-US-AvaMultilingualNeural', '+2%'), 'pastor': ('en-NG-AbeoNeural', '-2%')}
async def say(t, v, fn, log):
    for a in range(6):
        try: await edge_tts.Communicate(t, v[0], rate=v[1]).save(fn); log.append(fn+' ok'); return
        except Exception as e: log.append(f'{fn} err {e}'); await asyncio.sleep(4)
async def main():
    log = []; d = json.load(open('gen/africa_en.json'))
    for sid, _, lines in d['shots']:
        for i, (r, t) in enumerate(lines): await say(t, V[r], f'out/africa_{sid}_l{i}.mp3', log)
    for i, t in enumerate(d['end']): await say(t, V['end'], f'out/africa_end{i}.mp3', log)
    open('out/log.txt', 'w').write('\n'.join(log))
asyncio.run(main())
