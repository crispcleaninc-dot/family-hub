import os, numpy as np, scipy.io.wavfile as wf, torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
k = os.environ['K']
P = {'c1': "somber cinematic underscore, soft felt piano and warm low strings, slow tempo, minor key, emotional, spacious, no drums, documentary film score",
     'c2': "tense quiet cinematic underscore, low cello drone, sparse piano notes, slow pulse, dark, no drums, film score",
     'c3': "hopeful gentle cinematic underscore, soft piano and warm strings rising, slow, gospel warmth, no drums, film score"}[k]
proc = AutoProcessor.from_pretrained("facebook/musicgen-small"); m = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
torch.manual_seed(7)
inp = proc(text=[P], padding=True, return_tensors="pt")
a = m.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=1500)  # ~30 s
sr = m.config.audio_encoder.sampling_rate
os.makedirs('out', exist_ok=True); wf.write(f'out/{k}.wav', sr, (a[0, 0].numpy() * 32767).astype(np.int16)); print(k, 'ok', sr)
