# Ciarne's narration via F5-TTS voice copy (same reference as her Community Covenant films).
import json, subprocess, os
D = os.environ['D']; L = json.load(open('gen/lines.json'))['narr']
RT = "The first one swung, the bottle was already in my hand. When it was over, her tooth was gone, and I was the one the police wanted."
for k, t in L:
    if not k.startswith('d' + D): continue
    t = t.replace('LORD', 'Lord')
    r = subprocess.run(['f5-tts_infer-cli', '--model', 'F5TTS_v1_Base', '--ref_audio', 'gen/her.wav', '--ref_text', RT, '--gen_text', t,
                        '--output_dir', 'out', '--output_file', k + '.wav', '--speed', '0.92', '--nfe_step', '40', '--cfg_strength', '2.5'],
                       capture_output=True, text=True)
    print(k, r.returncode, r.stderr[-300:], flush=True)
