"""Render a v2 Short (1080x1920) with LARGE on-screen text for older viewers.
usage: python3 render_short.py <short_id g1|g2> <lang en|es> <voice_dir> <img_dir> <out.mp4>"""
import sys, os, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/v2'); import gma_shorts as G
sid, lang, VD, ID, OUT = sys.argv[1:6]
S = G.SHORTS[sid]; W = f'/tmp/v2s_{sid}_{lang}'; os.makedirs(W, exist_ok=True); SR = 48000
sfx = '' if lang == 'en' else 's'
LABEL = {'en': 'Dramatization · AI-made images and voice · v2', 'es': 'Dramatización · Imágenes y voz hechas con IA · v2'}[lang]
FULL = {'en': 'FULL STORY ON OUR CHANNEL', 'es': 'HISTORIA COMPLETA EN EL CANAL'}[lang]
PB = '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf'

def load(src):
    w = f'{W}/t.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-af', 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse',
                    '-ar', str(SR), '-ac', '1', w], check=True)
    a, _ = sf.read(w, dtype='float32'); return np.clip(a * 0.085 / (np.sqrt(np.mean(a ** 2)) + 1e-9), -.98, .98)

def cover(p, size):
    im = Image.open(p).convert('RGB'); r = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1)); x = (im.width - size[0]) // 2; y = (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))

def frame(img_id, big):
    p = next(f'{ID}/{img_id}{sfx}.{e}' for e in ('webp', 'png', 'jpg') if os.path.exists(f'{ID}/{img_id}{sfx}.{e}'))
    im = cover(p, (1296, 2304)); d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, 260, 1296, 900), fill=(0, 0, 0, 120))
    f = ImageFont.truetype(PB, 150); y = 300
    lines = big.split('\n'); y = 580 - 95 * len(lines)
    for ln in lines:
        fs = 150
        while d.textlength(ln, font=ImageFont.truetype(PB, fs)) > 1180: fs -= 8
        f = ImageFont.truetype(PB, fs); w = d.textlength(ln, font=f)
        d.text(((1296 - w) / 2, y), ln, font=f, fill=(255, 226, 120), stroke_width=7, stroke_fill=(0, 0, 0)); y += fs + 30
    return im

t = 0.3; voice = []; segs = []; caps = []
for i, (txt, big, shot) in enumerate(zip(S['lines'][lang], S['big'][lang], S['shots'])):
    a = load(f'{VD}/{lang}_{sid}_{i}.wav'); d = len(a) / SR; voice.append((t, a))
    frame(shot, big).save(f'{W}/f{i}.png'); st = t
    words = txt.split(); n = max(1, round(len(words) / 6)); per = len(words) / n
    ch = [' '.join(words[round(k * per):round((k + 1) * per)]) for k in range(n)]; acc = t
    for c in ch: cd = d * len(c) / len(txt); caps.append((acc, acc + cd, c)); acc += cd
    t += d + 0.45; segs.append((f'{W}/f{i}.png', st if i else 0, t))
# end card pointing to the long video
title = S['link'][lang][0]
ec = cover(next(f'{ID}/{S["shots"][-1]}{sfx}.{e}' for e in ('webp', 'png', 'jpg') if os.path.exists(f'{ID}/{S["shots"][-1]}{sfx}.{e}')), (1296, 2304)).filter(ImageFilter.GaussianBlur(10))
ec = Image.blend(ec, Image.new('RGB', ec.size, (10, 8, 14)), 0.6); d = ImageDraw.Draw(ec)
for txt, fs, y, col in ((FULL, 84, 700, (255, 255, 255)), ('▶ ' + title, 96, 900, (255, 226, 120)), ('Community Covenant', 70, 1500, (245, 200, 90))):
    f = ImageFont.truetype(PB if '▶' not in txt else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', fs)
    while d.textlength(txt, font=f) > 1200: fs -= 6; f = ImageFont.truetype(f.path, fs)
    d.text(((1296 - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col, stroke_width=4, stroke_fill=(0, 0, 0))
ec.save(f'{W}/end.png'); segs.append((f'{W}/end.png', t, t + 2.6)); TOT = t + 2.6

v = np.zeros(int((TOT + 1) * SR), np.float32)
for s0, a in voice: j = int(s0 * SR); v[j:j + len(a)] += a
sf.write(f'{W}/v.wav', v, SR)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', '/tmp/mmus/cs2.wav', '-i', f'{W}/v.wav', '-filter_complex',
                f'[0:a]aresample={SR},aformat=channel_layouts=mono,aloop=loop=-1:size=2000000,atrim=0:{TOT:.2f},afade=t=out:st={TOT - 2:.2f}:d=2,volume=0.30[m];[1:a]asplit[a1][a2];'
                '[m][a1]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=400[md];[md][a2]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[o]',
                '-map', '[o]', '-ar', '48000', '-ac', '2', '-t', f'{TOT:.2f}', f'{W}/a.wav'], check=True)
lst = []
for k, (p, a, b) in enumerate(segs):
    z = "min(1+0.0007*on,1.15)"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', p, '-vf', f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p",
                    '-t', f'{b - a:.3f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', f'{W}/s{k}.mp4'], check=True); lst.append(f'{W}/s{k}.mp4')
open(f'{W}/l.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst))
def at(x): return f'0:{int(x // 60):02d}:{x % 60:05.2f}'
ass = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,76,&H00FFFFFF,&H00FFFFFF,&H80000000,&H80000000,1,0,0,0,100,100,0,0,3,16,0,2,70,70,330,1
Style: Lab,DejaVu Sans,26,&H90FFFFFF,&H90FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,8,30,30,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + f'Dialogue: 0,{at(0)},{at(TOT)},Lab,,0,0,0,,{LABEL}\n' + ''.join(f'Dialogue: 0,{at(a)},{at(b)},Cap,,0,0,0,,{c}\n' for a, b, c in caps)
open(f'{W}/c.ass', 'w', encoding='utf-8').write(ass)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{W}/l.txt', '-i', f'{W}/a.wav', '-vf', f'ass={W}/c.ass',
                '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-shortest', OUT], check=True)
print(OUT, round(TOT, 1))
