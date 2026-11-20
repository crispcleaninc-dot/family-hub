import json, os, asyncio, edge_tts
d = json.load(open('gen/films.json')); os.makedirs('out', exist_ok=True)
V = {'fr': {'mom': 'fr-FR-DeniseNeural', 'odile': 'fr-CH-ArianeNeural', 'bene': 'fr-FR-EloiseNeural', 'pastor': 'fr-FR-HenriNeural', 'verse': 'fr-FR-HenriNeural',
            'sister': 'fr-BE-CharlineNeural', 'sister2': 'fr-CA-SylvieNeural', 'app': 'fr-FR-VivienneMultilingualNeural'},
     'en': {'mom': 'en-NG-EzinneNeural', 'odile': 'en-KE-AsiliaNeural', 'bene': 'en-US-AnaNeural', 'pastor': 'en-NG-AbeoNeural', 'verse': 'en-NG-AbeoNeural',
            'sister': 'en-ZA-LeahNeural', 'sister2': 'en-TZ-ImaniNeural', 'app': 'en-US-AvaMultilingualNeural'}}
RATE = {'verse': '-6%', 'pastor': '-3%'}
async def main():
    log = []
    for f, shots in d['films'].items():
        for sid, _, ls in shots:
            for i, (r, fr, en) in enumerate(ls):
                for lang, t in (('fr', fr), ('en', en)):
                    fn = f'out/{f}_{sid}_{i}_{lang}.mp3'
                    for a in range(4):
                        try: await edge_tts.Communicate(t, V[lang][r], rate=RATE.get(r, '+0%')).save(fn); log.append(fn + ' ok'); break
                        except Exception as e: log.append(f'{fn} err {e}'); await asyncio.sleep(3)
    open('out/tts_log.txt', 'w').write('\n'.join(log))
asyncio.run(main())
