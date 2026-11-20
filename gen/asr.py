import json, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('medium', device='cpu', compute_type='int8'); out = {}
for L in ['en', 'fr', 'es']:
    a = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'gen/{L}.mp3','-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout, np.float32)
    segs, info = m.transcribe(a, language=L, vad_filter=False)
    out[L] = [[round(s.start, 2), round(s.end, 2), s.text.strip()] for s in segs]; print(L, len(out[L]), flush=True)
json.dump(out, open('out/asr.json', 'w'), ensure_ascii=False, indent=0)
