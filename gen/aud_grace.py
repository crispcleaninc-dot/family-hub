import asyncio, edge_tts, os
os.makedirs('out', exist_ok=True)
T = "My name is Grace Kouassi. I sell fish and attiéké at the market. And last year I learned that God stays faithful even when people don't."
V = [('1_Asilia_Kenyan', 'en-KE-AsiliaNeural'), ('2_Leah_SouthAfrican', 'en-ZA-LeahNeural'), ('3_Ava_American', 'en-US-AvaMultilingualNeural'), ('4_Imani_Tanzanian', 'en-TZ-ImaniNeural'), ('5_Emma_American', 'en-US-EmmaMultilingualNeural')]
async def main():
    for n, v in V:
        for a in range(4):
            try: await edge_tts.Communicate(T, v).save(f'out/{n}.mp3'); break
            except Exception as e: print(n, e); await asyncio.sleep(3)
asyncio.run(main())
