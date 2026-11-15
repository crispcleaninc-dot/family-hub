import soundfile as sf, numpy as np, os, subprocess
from kokoro_onnx import Kokoro
k=Kokoro('/tmp/kok/kokoro.onnx','/tmp/kok/voices.bin')
V=0.55*k.get_voice_style('af_heart')+0.45*k.get_voice_style('af_nicole')
os.makedirs('vo6',exist_ok=True)
L=[l.strip() for l in open('lines5.txt') if l.strip()]
old=[l.strip() for l in open('lines4.txt') if l.strip()]
for i,t in enumerate(L):
    if t in old:  # reuse the approved take
        subprocess.run(['cp',f'vo5/{old.index(t)+1}.wav',f'vo6/{i+1}.wav']); print(i,'reuse'); continue
    a,sr=k.create(t.replace(':',',').replace(';',','),voice=V,speed=0.88,lang='en-us'); sf.write(f'vo6/{i+1}.wav',a,sr); print(i,round(len(a)/sr,1))
