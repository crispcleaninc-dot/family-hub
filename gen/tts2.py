import json, os, asyncio, edge_tts
D = json.load(open('gen/story2.json')); os.makedirs('out', exist_ok=True)
async def say(t, voice, rate, fn, log):
    for v in [voice, D['fallback'].get(voice)]:
        if not v: continue
        for a in range(4):
            try: await edge_tts.Communicate(t, v, rate=rate).save(fn); log.append(f'{fn} ok {v}'); return
            except Exception as e: log.append(f'{fn} err {v} {e}'); await asyncio.sleep(3)
async def main():
    log = []
    for fid, F in D['films'].items():
        for lang in F['langs']:
            k = 0
            for sid, _, ls in F['shots']:
                for r, t in ls:
                    v, rate = D['voices'][fid][lang][r]
                    await say(t[lang], v, rate, f'out/{fid}_{k:03d}_{lang}.mp3', log); k += 1
    open('out/tts_log.txt', 'w').write('\n'.join(log))
asyncio.run(main())
