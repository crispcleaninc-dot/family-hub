import os, asyncio, edge_tts
os.makedirs('out', exist_ok=True)
L = {'africa2_h1_l0': "Seven months after she disappeared with our money, Auntie Odile was standing at my market stall. Thin. Holding an envelope.",
     'africa2_h1_l1': "The whole market went quiet. Everybody wanted to see what I would do.",
     'africa2_h2_l0': "But to understand what I did that day, you have to know what almost happened the night she left.",
     'africa2_a01_l0': "My name is Grace. I sell fish and attiéké at the market. This is my story."}
async def main():
    log=[]
    for k,t in L.items():
        for a in range(6):
            try: await edge_tts.Communicate(t,'en-US-EmmaMultilingualNeural').save(f'out/{k}.mp3'); log.append(k+' ok'); break
            except Exception as e: log.append(f'{k} err {e}'); await asyncio.sleep(4)
    open('out/log.txt','w').write('\n'.join(log))
asyncio.run(main())
