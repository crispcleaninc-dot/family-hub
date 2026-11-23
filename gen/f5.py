import os, json, traceback, time
k = os.environ['K']; lang = k[:2]
items = json.load(open('gen/lines.json'))[k]
REF_T = "I know that room. I sat in it at seventeen. Nobody asked me what happened, not the police, not the prosecutor, not even the lawyer I paid."
os.makedirs('out', exist_ok=True)
from huggingface_hub import hf_hub_download
from f5_tts.api import F5TTS
if lang == 'en':
    tts = F5TTS(model='F5TTS_v1_Base'); sp = 0.88
elif lang == 'fr':
    ck = hf_hub_download('RASPIAUDIO/F5-French-MixedSpeakers-reduced', 'model_last_reduced.pt')
    vo = hf_hub_download('RASPIAUDIO/F5-French-MixedSpeakers-reduced', 'vocab.txt')
    tts = F5TTS(model='F5TTS_Base', ckpt_file=ck, vocab_file=vo); sp = 0.92
elif lang == 'es':
    ck = hf_hub_download('jpgallegoar/F5-Spanish', 'model_1200000.safetensors')
    vo = hf_hub_download('jpgallegoar/F5-Spanish', 'vocab.txt')
    tts = F5TTS(model='F5TTS_Base', ckpt_file=ck, vocab_file=vo); sp = 0.92
else:
    ck = hf_hub_download('msingiai/sauti-tts', 'model_last.pt')
    vo = hf_hub_download('msingiai/sauti-tts', 'vocab.txt')
    tts = F5TTS(model='F5TTS_v1_Base', ckpt_file=ck, vocab_file=vo); sp = 0.92
for sid, text, slow in items:
    t0 = time.time()
    try:
        tts.infer(ref_file='gen/her.wav', ref_text=REF_T, gen_text=text, speed=(sp * 0.86 if slow else sp),
                  nfe_step=48, cfg_strength=2.2, seed=1234, remove_silence=False, file_wave=f'out/{lang}_{sid}.wav')
        print(sid, 'ok', round(time.time() - t0), flush=True)
    except Exception:
        print(sid, 'FAIL', traceback.format_exc()[-1500:], flush=True)
