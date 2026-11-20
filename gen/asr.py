import json, glob, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8'); out = {}
for f in sorted(glob.glob('gen/*.mp3')):
    L = f.split('/')[-1][:2]
    a = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout, np.float32)
    segs, _ = m.transcribe(a, language=L); out[f] = ' '.join(s.text.strip() for s in segs); print(f, out[f], flush=True)
json.dump(out, open('out/asr.json', 'w'), ensure_ascii=False, indent=0)
