import asyncio, edge_tts, os, sys
sys.path.insert(0, 'gen'); from sw_lines import SW, END, VOICE
os.makedirs('out', exist_ok=True)
async def say(t, r, f):
    v, rate = VOICE[r]
    for a in range(6):
        try: await edge_tts.Communicate(t, v, rate=rate).save(f); print(f, 'ok', flush=True); return
        except Exception as e: print(f, e, flush=True); await asyncio.sleep(4)
async def main():
    for sid, ls in SW.items():
        for i, (r, t) in enumerate(ls): await say(t, r, f'out/{sid}_l{i}.mp3')
    for i, (r, t) in enumerate(END): await say(t, r, f'out/end_{i}.mp3')
asyncio.run(main())
