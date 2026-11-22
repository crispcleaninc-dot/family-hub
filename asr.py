import json, glob, os, re
from faster_whisper import WhisperModel
import jiwer
R=json.load(open('ref.json')); m=WhisperModel('small.en',device='cpu',compute_type='int8'); out={}
n=lambda s: re.sub(r"[^a-z' ]",' ',s.lower())
for f in sorted(glob.glob('a/*.mp3')):
    if os.path.basename(f)[:-4] not in R: continue
    k=os.path.basename(f)[:-4]; h=' '.join(x.text for x in m.transcribe(f,language='en',beam_size=5)[0])
    out[k]=[round(jiwer.wer(n(R[k]),n(h)),3),h]; print(k,out[k][0],flush=True)
os.makedirs('out',exist_ok=True); json.dump(out,open('out/asr.json','w'),indent=0)
