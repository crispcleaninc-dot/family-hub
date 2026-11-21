import os, asyncio, edge_tts, json
os.makedirs('out', exist_ok=True)
M=('fr-FR-DeniseNeural','-4%'); H=('fr-FR-HenriNeural','-6%'); A=('fr-FR-VivienneMultilingualNeural','-2%')
S = {s[0]: s[2] for s in json.load(open('gen/africa_fr.json'))}
L = {'africa2fr_h1_l0': (M, "Sept mois après avoir disparu avec notre argent, Tantie Odile était debout devant mon étal. Maigre. Une enveloppe à la main."),
     'africa2fr_h1_l1': (M, "Tout le marché s'est tu. Tout le monde voulait voir ce que j'allais faire."),
     'africa2fr_h2_l0': (M, "Mais pour comprendre ce que j'ai fait ce jour-là, il faut savoir ce qui a failli arriver la nuit où elle est partie."),
     'africa2fr_a01_l0': (M, "Je m'appelle Grâce. Je vends du poisson et de l'attiéké au marché. Voici mon histoire."),
     'africa2fr_a08_l0': (H, S['a08'][0][1]), 'africa2fr_a16_l1': (H, S['a16'][1][1]),
     'africa2fr_end0': (A, "Si vous vivez une trahison comme celle-ci, ne restez pas seule."),
     'africa2fr_end1': (A, "Ouvrez l'application Community Covenant. Le lien est dans la description."),
     'africa2fr_end2': (A, "Touchez Ask for Help, et écrivez comment vous allez vraiment."),
     'africa2fr_end3': (A, "Le jour même, une personne de l'équipe vous répond et prie pour vous. Et avec Listen, vous entendez la Parole de Dieu pour le jour que vous traversez."),
     'africa2fr_end4': (A, "C'est gratuit. Que Dieu vous bénisse.")}
async def main():
    log=[]
    for k,((v,r),t) in L.items():
        for a in range(6):
            try: await edge_tts.Communicate(t,v,rate=r).save(f'out/{k}.mp3'); log.append(k+' ok'); break
            except Exception as e: log.append(f'{k} err {e}'); await asyncio.sleep(4)
    open('out/log.txt','w').write('\n'.join(log))
asyncio.run(main())
