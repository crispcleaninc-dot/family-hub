import json, os, asyncio, edge_tts
F = json.load(open('gen/story.json'))['films']; os.makedirs('out', exist_ok=True)
V = {'es': {'narr_m': ('es-MX-JorgeNeural', '+4%', '+0Hz'), 'narr_t': ('es-US-AlonsoNeural', '+6%', '+0Hz'), 'narr_f': ('es-MX-DaliaNeural', '+4%', '+0Hz'),
            'ruth': ('es-DO-RamonaNeural', '-2%', '+0Hz'), 'tania': ('es-PR-KarinaNeural', '+4%', '+0Hz'), 'coach': ('es-CO-GonzaloNeural', '+6%', '+0Hz'),
            'rosa': ('es-MX-DaliaNeural', '+2%', '+0Hz'), 'andres': ('es-US-AlonsoNeural', '+4%', '+0Hz'), 'jose': ('es-CU-ManuelNeural', '-2%', '+0Hz'),
            'vanessa': ('es-CO-SalomeNeural', '+4%', '+0Hz'), 'pastor': ('es-CO-GonzaloNeural', '+0%', '+0Hz'), 'lena': ('es-PR-KarinaNeural', '+4%', '+0Hz'),
            'isaias': ('es-US-AlonsoNeural', '+6%', '+0Hz'), 'dani': ('es-US-PalomaNeural', '+6%', '+0Hz'), 'bea': ('es-CU-BelkysNeural', '-3%', '+0Hz'),
            'carla': ('es-MX-DaliaNeural', '+4%', '+0Hz'), 'verse': ('es-CO-GonzaloNeural', '-4%', '+0Hz'), 'app': ('es-US-PalomaNeural', '+4%', '+0Hz')},
     'en': {'narr_m': ('en-US-AndrewNeural', '+4%', '+0Hz'), 'narr_t': ('en-US-BrianNeural', '+6%', '+0Hz'), 'narr_f': ('en-US-AvaNeural', '+4%', '+0Hz'),
            'ruth': ('en-US-AvaMultilingualNeural', '-3%', '+0Hz'), 'tania': ('en-US-AriaNeural', '+4%', '+0Hz'), 'coach': ('en-US-AndrewMultilingualNeural', '+6%', '+0Hz'),
            'rosa': ('en-US-AvaMultilingualNeural', '+2%', '+0Hz'), 'andres': ('en-US-BrianNeural', '+4%', '+0Hz'), 'jose': ('en-US-AndrewMultilingualNeural', '-2%', '+0Hz'),
            'vanessa': ('en-US-EmmaMultilingualNeural', '+4%', '+0Hz'), 'pastor': ('en-US-BrianMultilingualNeural', '+0%', '+0Hz'), 'lena': ('en-US-AriaNeural', '+4%', '+0Hz'),
            'isaias': ('en-US-BrianNeural', '+6%', '+0Hz'), 'dani': ('en-US-AvaNeural', '+6%', '+0Hz'), 'bea': ('en-US-EmmaMultilingualNeural', '-3%', '+0Hz'),
            'carla': ('en-US-AvaMultilingualNeural', '+4%', '+0Hz'), 'verse': ('en-US-AndrewMultilingualNeural', '-4%', '+0Hz'), 'app': ('en-US-EmmaMultilingualNeural', '+4%', '+0Hz')}}
async def main():
    log = []
    for fid, shots in F.items():
        k = 0
        for sid, ls in shots:
            for r, es, en in ls:
                for lang, t in (('es', es), ('en', en)):
                    v, rate, pitch = V[lang][r]; fn = f'out/{fid}_{k:03d}_{lang}.mp3'
                    for a in range(4):
                        try: await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(fn); log.append(fn+' ok'); break
                        except Exception as e: log.append(f'{fn} err {e}'); await asyncio.sleep(3)
                k += 1
    open('out/tts_log.txt', 'w').write('\n'.join(log))
asyncio.run(main())
