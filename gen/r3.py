# Cover to Cover Days 4-14: render one chunk of KJV reading lines in Ciarne's voice copy (same F5 settings as Days 1-3).
import json, os, subprocess
N = int(os.environ['N'])
items = [x for x in json.load(open('gen/script4.json')) if x[3] == N]
RT = "The first one swung, the bottle was already in my hand. When it was over, her tooth was gone, and I was the one the police wanted."
os.makedirs('out', exist_ok=True)
api = None
try:
    from f5_tts.api import F5TTS
    api = F5TTS(model="F5TTS_v1_Base")
except Exception as e: print('api load failed:', e, flush=True)
for g, k, t, _ in items:
    t = t.replace('LORD', 'Lord'); f = f'out/{k}.wav'
    try:
        if not api: raise RuntimeError('no api')
        api.infer(ref_file='gen/her.wav', ref_text=RT, gen_text=t, file_wave=f, speed=0.92, nfe_step=32, cfg_strength=2.5)
    except Exception as e:
        print(k, 'api err', str(e)[:200], flush=True)
        subprocess.run(['f5-tts_infer-cli', '--model', 'F5TTS_v1_Base', '--ref_audio', 'gen/her.wav', '--ref_text', RT, '--gen_text', t,
                        '--output_dir', 'out', '--output_file', k + '.wav', '--speed', '0.92', '--nfe_step', '32'], capture_output=True)
    print(k, os.path.exists(f), flush=True)
