# Check every music cue for singing/voices: separate with Demucs, measure the vocal stem level per second.
import subprocess, glob, json, os, numpy as np, soundfile as sf
os.makedirs('out', exist_ok=True); res = {}
for f in sorted(glob.glob('cues/*.wav')):
    k = os.path.basename(f)[:-4]
    subprocess.run(['python3', '-m', 'demucs', '--two-stems', 'vocals', '-n', 'htdemucs', '-o', 'sep', f], capture_output=True)
    vf = f'sep/htdemucs/{k}/vocals.wav'; nf = f'sep/htdemucs/{k}/no_vocals.wav'
    if not os.path.exists(vf): res[k] = 'sep failed'; continue
    v, sr = sf.read(vf); n, _ = sf.read(nf)
    v = v.mean(1) if v.ndim > 1 else v; n = n.mean(1) if n.ndim > 1 else n
    sec = []
    for i in range(0, len(v) - sr // 2, sr):
        rv = np.sqrt(np.mean(v[i:i+sr]**2)) + 1e-9; rn = np.sqrt(np.mean(n[i:i+sr]**2)) + 1e-9
        sec.append(round(20 * np.log10(rv / rn), 1))
    res[k] = {'max_vocal_vs_music_db': max(sec), 'per_second': sec}
    print(k, max(sec), flush=True)
json.dump(res, open('out/vchk.json', 'w'), indent=1)
