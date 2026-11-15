import numpy as np, pyworld as pw, soundfile as sf
from kokoro_onnx import Kokoro
K=Kokoro('/tmp/kok/kokoro.onnx','/tmp/kok/voices.bin')
# child voice: built from a young female base voice, then pitch raised toward a child's range,
# vocal tract shortened (formants up), and more pitch movement (kids' speech is more sing-song)
PRESET={
 'Jojo':dict(base='af_sarah',speed=0.95,f0=262,form=1.12,var=1.2),
 'Pip':dict(base='af_jessica',speed=0.93,f0=300,form=1.16,var=1.2),
 'Baby Bee':dict(base='af_bella',speed=0.84,f0=350,form=1.22,var=1.25)}
def warp(env,alpha):
    n=env.shape[1]; src=np.arange(n)/alpha; out=np.empty_like(env)
    for i in range(env.shape[0]): out[i]=np.interp(src,np.arange(n),env[i],right=env[i,-1])
    return out
def child(text,who,sr_out=24000):
    p=PRESET[who]; a,sr=K.create(text,voice=p['base'],speed=p['speed'],lang='en-us'); x=a.astype(np.float64)
    f0,t=pw.harvest(x,sr,f0_floor=80,f0_ceil=600,frame_period=5); sp=pw.cheaptrick(x,f0,t,sr); ap=pw.d4c(x,f0,t,sr)
    v=f0>0; m=np.exp(np.mean(np.log(f0[v]))) if v.any() else 200
    lf=np.log(np.where(v,f0,1)); lm=np.log(m); tgt=np.log(p['f0'])
    nf=np.where(v,np.exp(tgt+(lf-lm)*p['var']),0)
    y=pw.synthesize(nf,warp(sp,p['form']),warp(ap,p['form']),sr,5)
    y=y/max(1e-6,np.abs(y).max())*0.9
    return y.astype(np.float32),sr,m
if __name__=='__main__':
    lines={'Jojo':"Hey, I'm Jojo! When Mommy gives me a job, I finish it all the way!",'Pip':"Hi! I'm Pip! Wanna read a story with me? Pleeease?",'Baby Bee':"Hee hee! Mama! I love you!"}
    import subprocess
    for w,t in lines.items():
        y,sr,m=child(t,w); sf.write(f'{w.replace(" ","")}_new.wav',y,sr)
        f0,_=pw.harvest(y.astype(np.float64),sr,f0_floor=80,f0_ceil=700); v=f0[f0>0]
        print(w,'base mean F0',round(m),'-> new mean',round(float(np.exp(np.log(v).mean()))),'range',round(float(np.percentile(v,10))),round(float(np.percentile(v,90))))
