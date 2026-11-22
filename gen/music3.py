# Quiet ambient beds for FNF Cover to Cover, strictly instrumental (no choir, no voices). MusicGen-medium, CPU.
import os, numpy as np, scipy.io.wavfile as wf, torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
k = os.environ['K']
NOV = ", instrumental only, no choir, no voices, no vocals, no singing, no humming, no drums, no percussion"
P = {
 'qa1': "very quiet warm analog synth pad drone, soft and low, calm, meditative, slow evolving" + NOV,
 'qa2': "soft ambient pad with a few gentle low piano notes, very calm, peaceful, slow" + NOV,
 'qa3': "minimal ambient soundscape, soft warm low strings drone, slow swells, peaceful" + NOV,
 'qa4': "gentle ambient electric piano with soft reverb pad, very slow, calm, warm, low register" + NOV,
 'qa5': "calm ambient drone with soft felt piano chords, quiet, reflective, slow" + NOV,
 'qa6': "soft warm cello drone with a quiet ambient pad, slow, prayerful, low register" + NOV,
}[k]
seed = int(k[-1]) * 13 + 5
name = 'facebook/musicgen-medium'
proc = AutoProcessor.from_pretrained(name); m = MusicgenForConditionalGeneration.from_pretrained(name)
torch.manual_seed(seed)
inp = proc(text=[P], padding=True, return_tensors="pt")
a = m.generate(**inp, do_sample=True, guidance_scale=4.0, max_new_tokens=1500)
sr = m.config.audio_encoder.sampling_rate
os.makedirs('out', exist_ok=True); wf.write(f'out/{k}.wav', sr, (a[0, 0].numpy() * 32767).astype(np.int16)); print(k, 'ok', sr)
