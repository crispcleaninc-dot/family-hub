import json, asyncio, edge_tts, os
D = json.load(open('gen/story2.json')); os.makedirs('out', exist_ok=True)
want = {('f10', 8), ('f9', 12)}
async def main():
    log = []
    for fid, k in sorted(want):
        L = [(r, t['en']) for s, p, ls in D['films'][fid]['shots'] for r, t in ls]
        r, t = L[k]; v, rate = D['voices'][fid]['en'][r]; fn = f'out/{fid}_{k:03d}_en.mp3'
        for a in range(8):
            try: await edge_tts.Communicate(t, v, rate=rate).save(fn); log.append(fn + ' ok'); break
            except Exception as e: log.append(f'{fn} err {e}'); await asyncio.sleep(6)
    open('out/redo_log.txt', 'w').write('\n'.join(log))
asyncio.run(main())
