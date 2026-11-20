import asyncio, edge_tts, os
L = [("m1", "en-US-AndrewNeural", "-4%", "There's a youth program. Plead, finish your probation, and it comes off your record. Fight it... and you're betting your whole life on a jury."),
     ("m2", "en-US-BrianNeural", "+0%", "Then why'd you keep shooting?"),
     ("m3", "en-US-GuyNeural", "-6%", "Just tell me it's yours... and this all goes away.")]
async def main():
    os.makedirs('out', exist_ok=True)
    for k, v, r, t in L:
        await edge_tts.Communicate(t, v, rate=r).save(f'out/{k}.mp3'); print(k, 'ok')
asyncio.run(main())
