import json, subprocess, os
k = os.environ['K']; L = {a: (b, c) for a, b, c in json.load(open('gen/lines.json'))}
who, t = L[k]
REF = {'her': ("The first one swung, the bottle was already in my hand. When it was over, her tooth was gone, and I was the one the police wanted.", 0.9),
       'him': ("Friday salute service. Everyone pick somebody who served. They'll be on the sideline at the anthem. You walk over and salute them.", 0.92)}
rt, sp = REF[who]
r = subprocess.run(['f5-tts_infer-cli', '--model', 'F5TTS_v1_Base', '--ref_audio', f'gen/{who}.wav', '--ref_text', rt, '--gen_text', t,
                    '--output_dir', 'out', '--output_file', k + '.wav', '--speed', str(sp), '--nfe_step', '40', '--cfg_strength', '2.5'],
                   capture_output=True, text=True)
print(k, r.returncode, r.stderr[-600:], flush=True)
