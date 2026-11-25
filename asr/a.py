from faster_whisper import WhisperModel
import glob, os
m = WhisperModel('small', device='cpu', compute_type='int8'); os.makedirs('out', exist_ok=True); L=[]
for f in sorted(glob.glob('asr/*.wav')):
    segs, _ = m.transcribe(f, language='en', beam_size=1); L.append(os.path.basename(f) + ' => ' + ' '.join(s.text.strip() for s in segs))
open('out/asr.txt', 'w').write('\n'.join(L)); print('\n'.join(L))
