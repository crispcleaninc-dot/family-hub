import json, asyncio, edge_tts, os
os.makedirs('out', exist_ok=True)
J = json.load(open('gen2/edge.json'))
async def main():
    for name, (voice, rate, text) in J.items():
        await edge_tts.Communicate(text, voice, rate=rate).save(f'out/{name}.mp3'); print(name, 'ok')
asyncio.run(main())
