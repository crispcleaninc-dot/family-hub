import asyncio, edge_tts, os, sys
sys.path.insert(0, 'gen'); from script import S
V = {'A': {'en': ('en-US-AndrewMultilingualNeural', '-6%'), 'fr': ('fr-FR-RemyMultilingualNeural', '-4%'), 'es': ('es-MX-JorgeNeural', '-4%')},
     'D': {'en': ('en-US-GuyNeural', '-5%'), 'fr': ('fr-FR-HenriNeural', '-5%'), 'es': ('es-US-AlonsoNeural', '-4%')}}
async def main():
    os.makedirs('out', exist_ok=True)
    for s in S:
        if s[1] in V:
            for L, t in s[3].items():
                v, r = V[s[1]][L]
                await edge_tts.Communicate(t.replace('"', ''), v, rate=r).save(f'out/{L}_{s[0]}.mp3'); print(L, s[0], 'ok')
asyncio.run(main())
