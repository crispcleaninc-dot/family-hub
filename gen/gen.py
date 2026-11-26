import json, subprocess, os
k = os.environ['K']; G = json.load(open('gen/lines.json'))[k]
RT = "The first one swung, the bottle was already in my hand. When it was over, her tooth was gone, and I was the one the police wanted."
for l in G:
    r = subprocess.run(['f5-tts_infer-cli', '--model', 'F5TTS_v1_Base', '--ref_audio', 'gen/her.wav', '--ref_text', RT, '--gen_text', l['text'],
                        '--output_dir', 'out', '--output_file', '%d.wav' % l['i'], '--speed', '0.9', '--nfe_step', '40', '--cfg_strength', '2.5'],
                       capture_output=True, text=True)
    print(l['i'], r.returncode, r.stderr[-400:], flush=True)
    if os.path.exists('out/%d.wav' % l['i']):
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'out/%d.wav' % l['i'], '-af', 'highpass=f=70,loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '1', '-b:a', '96k', 'out/%d.mp3' % l['i']])
        os.remove('out/%d.wav' % l['i'])
