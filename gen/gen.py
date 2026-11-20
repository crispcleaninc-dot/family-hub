import json, subprocess
lines = json.load(open('gen/lines.json'))
ref_text = "It started under a picture online. Two girls I barely knew decided I was the problem. Comments turned into messages, messages turned into I know where you stay."
for k, t in lines:
    r = subprocess.run(['f5-tts_infer-cli', '--model', 'F5TTS_v1_Base', '--ref_audio', 'gen/ref.wav', '--ref_text', ref_text, '--gen_text', t, '--output_dir', 'out', '--output_file', k + '.wav', '--speed', '0.95'], capture_output=True, text=True)
    print(k, r.returncode, r.stderr[-400:], flush=True)
