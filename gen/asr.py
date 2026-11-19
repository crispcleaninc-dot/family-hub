import json, glob, subprocess, numpy as np
from faster_whisper import WhisperModel
m = WhisperModel('medium.en', device='cpu', compute_type='int8')
out = {}
for f in sorted(glob.glob('gen/*.mp3')):
    a = np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-f','f32le','-ac','1','-ar','16000','-'],capture_output=True).stdout, np.float32)
    segs, _ = m.transcribe(a, word_timestamps=True, vad_filter=False)
    out[f.split('/')[-1][:-4]] = [{'s': round(s.start, 2), 'e': round(s.end, 2), 't': s.text.strip(), 'w': [[round(w.start, 2), round(w.end, 2), w.word] for w in s.words]} for s in segs]
    print(f, len(out[f.split('/')[-1][:-4]]), flush=True)
json.dump(out, open('out/asr.json', 'w'), ensure_ascii=False, indent=0)
