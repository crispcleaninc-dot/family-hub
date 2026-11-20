import os, numpy as np, scipy.io.wavfile as wf, torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
k = os.environ['K']
P = {'m1': "ancient Middle Eastern cinematic underscore, soft oud and frame drum heartbeat, warm low strings, reverent, slow, biblical epic, no vocals",
     'm2': "tense ancient cinematic underscore, low duduk melody over dark strings drone, slow pulse, biblical drama, no vocals",
     'm3': "hopeful gentle cinematic underscore, soft piano and warm strings rising with a light ney flute, slow, uplifting, no drums, no vocals"}[k]
proc = AutoProcessor.from_pretrained("facebook/musicgen-small"); m = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
torch.manual_seed(11)
inp = proc(text=[P], padding=True, return_tensors="pt")
a = m.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=1500)
sr = m.config.audio_encoder.sampling_rate
os.makedirs('out', exist_ok=True); wf.write(f'out/{k}.wav', sr, (a[0, 0].numpy() * 32767).astype(np.int16)); print(k, 'ok', sr)
