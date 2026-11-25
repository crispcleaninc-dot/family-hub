import json, asyncio, edge_tts, os
os.makedirs('out', exist_ok=True)
J = json.load(open('gen7/edge.json'))
async def main():
    for name, (voice, rate, text) in J.items():
        try:
            await edge_tts.Communicate(text, voice, rate=rate).save(f'out/{name}.mp3'); print(name, 'ok')
        except Exception as e: print(name, 'FAIL', e)
asyncio.run(main())
from faster_whisper import WhisperModel
m = WhisperModel('small', device='cpu', compute_type='int8'); res = {}
for f in sorted(os.listdir('out')):
    if f.endswith('.mp3'):
        segs, info = m.transcribe('out/' + f, language='en', beam_size=1)
        res[f] = ' '.join(s.text.strip() for s in segs); print(f, '=>', res[f], flush=True)
json.dump(res, open('out/asr.json', 'w'), indent=0)
