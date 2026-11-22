import os, numpy as np, scipy.io.wavfile as wf, torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
k = os.environ['K']
NOV = ", instrumental only, no choir, no voices, no vocals, no singing, no humming"
P = {
 'cs1': "epic cinematic film score, deep low strings and french horns, slow and majestic, ancient biblical epic, awe" + NOV,
 'cs2': "dark cinematic orchestral underscore, low cellos and soft timpani rolls, tension, suspense, slow" + NOV,
 'cs3': "emotional cinematic strings, tender and hopeful, slow swelling violins and warm cello, film score" + NOV,
 'cs4': "mysterious desert cinematic score, low duduk-like woodwind melody over soft string drone, slow" + NOV,
 'cs5': "triumphant cinematic orchestra, brass and strings rising slowly, majestic, holy wonder, film score" + NOV,
 'cs6': "quiet reflective cinematic piano and strings, slow, sacred, soft, film score" + NOV,
}[k]
name = 'facebook/musicgen-medium'
proc = AutoProcessor.from_pretrained(name); m = MusicgenForConditionalGeneration.from_pretrained(name)
torch.manual_seed(int(k[-1]) * 17 + 3)
inp = proc(text=[P], padding=True, return_tensors="pt")
a = m.generate(**inp, do_sample=True, guidance_scale=4.0, max_new_tokens=1500)
sr = m.config.audio_encoder.sampling_rate
os.makedirs('out', exist_ok=True); wf.write(f'out/{k}.wav', sr, (a[0, 0].numpy() * 32767).astype(np.int16)); print(k, 'ok', sr)
