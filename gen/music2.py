# New background music palette for FNF Cover to Cover (4 styles x 3 cues). MusicGen-medium, CPU.
import os, numpy as np, scipy.io.wavfile as wf, torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration
k = os.environ['K']
P = {
 'soft1': "soft reverent worship underscore, gentle solo piano with warm sustained strings, slow, peaceful, prayerful, no drums, no percussion, no vocals",
 'soft2': "gentle reflective underscore, warm string pad with soft piano arpeggios and a faint oud melody, calm, devotional, no drums, no vocals",
 'soft3': "tender hopeful underscore, soft piano and cello, light ney flute, slow and peaceful, no drums, no percussion, no vocals",
 'anc1': "ancient Middle Eastern cinematic score, slow duduk melody over warm low strings, reverent, biblical, no drums, no vocals",
 'anc2': "ancient cinematic underscore, ney flute and soft oud over string drone, mysterious and reverent, slow, no percussion, no vocals",
 'anc3': "epic biblical cinematic underscore, rising warm strings with a gentle kanun and duduk, slow, majestic, no drums, no vocals",
 'hymn1': "soft instrumental church hymn, gentle pipe organ and piano, slow, reverent, traditional gospel hymn feel, no drums, no vocals",
 'hymn2': "quiet instrumental hymn on piano with soft organ pad, slow, peaceful, Sunday morning chapel, no drums, no vocals",
 'hymn3': "gentle instrumental hymn arrangement, warm strings and piano, slow, worshipful, classic hymn melody feel, no drums, no vocals",
 'amb1': "very quiet ambient pad, soft warm synth drone, barely there, calm, meditative, no melody, no drums, no vocals",
 'amb2': "minimal ambient soundscape, soft airy pads with a distant gentle piano note now and then, very calm, no drums, no vocals",
 'amb3': "soft ambient strings drone, slow swelling and fading, peaceful, meditative, very quiet, no drums, no vocals",
}[k]
seed = {'1': 21, '2': 33, '3': 47}[k[-1]]
name = os.environ.get('MODEL', 'facebook/musicgen-medium')
proc = AutoProcessor.from_pretrained(name); m = MusicgenForConditionalGeneration.from_pretrained(name)
torch.manual_seed(seed)
inp = proc(text=[P], padding=True, return_tensors="pt")
a = m.generate(**inp, do_sample=True, guidance_scale=3.5, max_new_tokens=1500)
sr = m.config.audio_encoder.sampling_rate
os.makedirs('out', exist_ok=True); wf.write(f'out/{k}.wav', sr, (a[0, 0].numpy() * 32767).astype(np.int16)); print(k, 'ok', sr, name)
