import asyncio, edge_tts, json, os
P = {'god': ('en-US-AndrewMultilingualNeural', '-12%', '-6Hz'), 'angel': ('en-US-BrianMultilingualNeural', '-8%', '+0Hz'), 'crowd': ('en-US-GuyNeural', '-6%', '+0Hz'),
     'serpent': ('en-GB-RyanNeural', '-12%', '-4Hz'), 'Eve': ('en-US-AvaMultilingualNeural', '-5%', '+0Hz'),
     'Abram': ('en-GB-ThomasNeural', '-10%', '-2Hz'), 'Abraham': ('en-GB-ThomasNeural', '-10%', '-2Hz'), 'Isaac': ('en-NG-AbeoNeural', '-6%', '+0Hz'),
     'Jacob': ('en-TZ-ElimuNeural', '-4%', '+0Hz'), 'Israel': ('en-TZ-ElimuNeural', '-8%', '+0Hz'), 'Esau': ('en-AU-WilliamNeural', '-4%', '-2Hz'),
     'Laban': ('en-IN-PrabhatNeural', '-4%', '+0Hz'), 'Joseph': ('en-US-BrianMultilingualNeural', '-2%', '+0Hz'), 'Judah': ('en-GB-RyanNeural', '-4%', '+0Hz'),
     'Lot': ('en-US-GuyNeural', '-4%', '-2Hz'), 'Cain': ('en-GB-RyanNeural', '-6%', '+0Hz'), 'Lamech': ('en-NG-AbeoNeural', '-8%', '-2Hz'),
     'Abimelech': ('en-IN-PrabhatNeural', '-6%', '-2Hz'), 'Phichol': ('en-AU-WilliamNeural', '-6%', '+0Hz'), 'Shechem': ('en-AU-WilliamNeural', '-2%', '+0Hz'),
     'Hamor': ('en-IN-PrabhatNeural', '-8%', '-3Hz'), 'Bethuel': ('en-GB-ThomasNeural', '-6%', '+0Hz'), 'Reuben': ('en-AU-WilliamNeural', '-4%', '+0Hz'),
     'Pharaoh': ('en-IN-PrabhatNeural', '-8%', '-4Hz'), 'Melchizedek': ('en-US-BrianMultilingualNeural', '-10%', '-2Hz'), 'Noah': ('en-GB-ThomasNeural', '-8%', '-4Hz'), 'Potiphar': ('en-IN-PrabhatNeural', '-6%', '+0Hz'),
     'Sarai': ('en-NG-EzinneNeural', '-5%', '+0Hz'), 'Sarah': ('en-NG-EzinneNeural', '-5%', '+0Hz'), 'Hagar': ('en-US-EmmaMultilingualNeural', '-5%', '+0Hz'),
     'Rebekah': ('en-US-AvaMultilingualNeural', '-5%', '+0Hz'), 'Rachel': ('en-KE-AsiliaNeural', '-4%', '+0Hz'), 'Leah': ('en-IN-NeerjaNeural', '-4%', '+0Hz'), 'Tamar': ('en-US-EmmaMultilingualNeural', '-4%', '+0Hz')}
L = json.load(open('gen/lines.json'))['chars']; os.makedirs('out', exist_ok=True)
async def main():
    for k, r, t in L:
        v, rate, pitch = P.get(r, ('en-US-GuyNeural', '-6%', '+0Hz'))
        for a in range(6):
            try: await edge_tts.Communicate(t, v, rate=rate, pitch=pitch).save(f'out/{k}.mp3'); print(k, r, 'ok', flush=True); break
            except Exception as e: print(k, e, flush=True); await asyncio.sleep(4)
asyncio.run(main())
