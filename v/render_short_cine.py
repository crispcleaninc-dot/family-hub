"""Render a v2 long-form story (16:9) from a story module.
usage: python3 render_v2.py <module> <prefix> <lang> <voice_dir> <img_dir> <out.mp4>
"""
import sys, os, json, subprocess, importlib, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/v2')
mod, pfx, lang, VD, ID, OUT = sys.argv[1:7]
VOICE=dict(a.split('=') for a in sys.argv[7:])
S = importlib.import_module(mod)
W = f'/tmp/v2r_{mod}_{lang}'; os.makedirs(W, exist_ok=True)
SR = 48000
LABEL = {'sw': 'Tamthilia · Picha na sauti zimetengenezwa kwa AI · v2', 'fr': 'Dramatisation · Images et voix créées par IA · v2',
         'en': 'Dramatization · AI-made images and voice · v2', 'es': 'Dramatización · Imágenes y voz hechas con IA · v2'}[lang]
ENDTXT = {'sw': ('Pakua bure:', 'covenant.crispusmundo.com', 'JIUNGE NA CHANELI'), 'fr': ('Application gratuite :', 'covenant.crispusmundo.com', "ABONNEZ-VOUS"),
          'en': ('Free app:', 'covenant.crispusmundo.com', 'SUBSCRIBE'), 'es': ('App gratis:', 'covenant.crispusmundo.com', 'SUSCRÍBETE')}[lang]

def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
def at(x): return f'{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}'
def load(src, key):
    w = f'{W}/{key}.wav'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-af',
                    'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,highpass=f=70',
                    '-ar', str(SR), '-ac', '1', w], check=True)
    a, _ = sf.read(w, dtype='float32')
    rms = np.sqrt(np.mean(a ** 2) + 1e-9); a = a * (0.085 / rms)
    a = np.clip(a, -0.98, 0.98); return a

def fontp(bold=True, serif=False):
    if serif: return '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
    return '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf' if bold else '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf'

def img(sid):
    for ext in ('webp', 'png', 'jpg'):
        p = f'{ID}/{sid}.{ext}'
        if os.path.exists(p): return p
    raise FileNotFoundError(sid)

# ---- timeline
t = 0.6; voice = []; caps = []; segs = []; cur = None; seg_start = 0.0
for row in S.L:
    sid, who = row[0], row[1]
    if who == 'T':
        if cur is not None: segs.append((cur, seg_start, t));
        segs.append(('TITLE', t, t + row[3])); t += row[3]; cur = None; seg_start = t; continue
    im = row[2]
    if im != cur:
        if cur is not None: t += 0.35; segs.append((cur, seg_start, t))
        cur = im; seg_start = t
    txt = row[3] if isinstance(row[3], str) else row[3][lang]; slow = len(row) > 4 and row[4].get('slow')
    if who == 'N': src = f'{VD}/{lang}_{pfx}_{sid}.wav'
    else: src = f'{VD}/{sid}__{VOICE[who]}.mp3'
    a = load(src, sid)
    voice.append((t, a)); d = len(a) / SR
    words = txt.split(); n = max(1, round(len(words) / 8)); per = len(words) / n
    chunks = [' '.join(words[round(k * per):round((k + 1) * per)]) for k in range(n)]
    acc = t; tot = sum(len(c) for c in chunks)
    for c in chunks:
        cd = d * len(c) / tot; caps.append((acc, acc + cd, c, who)); acc += cd
    t += d + (0.95 if slow else 0.5)
segs.append((cur, seg_start, t + 0.3)); t += 0.6
END0 = t
segs[0] = (segs[0][0], 0.0, segs[0][2])
for i, txt in enumerate(getattr(S,'END',{}).get(lang,[])):
    a = load(f'{VD}/{lang}_{pfx}_end{i}.wav', f'end{i}')
    voice.append((t, a)); d = len(a) / SR
    caps.append((t, t + d, txt, 'N')); t += d + 0.5
TOT = t + 1.8

# ---- audio: voice + film-score bed (her approved cues cs1-cs4), ducked
v = np.zeros(int((TOT + 1) * SR), np.float32)
for s0, a in voice:
    j = int(s0 * SR); v[j:j + len(a)] += a[:len(v) - j]
sf.write(f'{W}/voice.wav', v, SR)
cues = [f'/tmp/mmus/cs{k}.wav' for k in (1, 2, 3, 4)]
ins = sum([['-i', c] for c in cues], [])
fc = ''.join(f'[{k}:a]aresample={SR},aformat=channel_layouts=mono[c{k}];' for k in range(4))
fc += '[c0][c1]acrossfade=d=4[x1];[x1][c2]acrossfade=d=4[x2];[x2][c3]acrossfade=d=4[mus]'
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fc, '-map', '[mus]', f'{W}/mus1.wav'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-stream_loop', '-1', '-i', f'{W}/mus1.wav', '-t', f'{TOT:.2f}',
                '-af', f'afade=t=in:d=2,afade=t=out:st={TOT - 3:.2f}:d=3', f'{W}/mus.wav'], check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{W}/mus.wav', '-i', f'{W}/voice.wav', '-filter_complex',
                '[0:a]volume=0.30[m];[1:a]asplit[v1][v2];[m][v1]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=500[md];'
                '[md][v2]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]',
                '-map', '[a]', '-ar', '48000', '-ac', '2', '-t', f'{TOT:.2f}', f'{W}/audio.wav'], check=True)

# ---- title card + end card
def cover(src, size=(1080, 1920)):
    im = Image.open(src).convert('RGB'); r = max(size[0] / im.width, size[1] / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1)); x = (im.width - size[0]) // 2; y = (im.height - size[1]) // 2
    return im.crop((x, y, x + size[0], y + size[1]))
first_img = next(r[2] for r in S.L if r[1] not in 'TP')
tc = cover(img(first_img)).filter(ImageFilter.GaussianBlur(6)); tc = Image.blend(tc, Image.new('RGB', tc.size, (8, 6, 4)), 0.55)
d = ImageDraw.Draw(tc); l1, l2 = S.TITLE[lang]
f1 = ImageFont.truetype(fontp(serif=True), 150); f2 = ImageFont.truetype(fontp(), 64)
for txt, f, y, col in ((l1, f1, 800, (245, 214, 140)), (l2, f2, 1000, (255, 255, 255))):
    w = d.textlength(txt, font=f); d.text(((1080 - w) / 2, y), txt, font=f, fill=col, stroke_width=4, stroke_fill=(0, 0, 0))
tc.save(f'{W}/TITLE.png')
ec = Image.new('RGB', (1080, 1920), (14, 12, 22)); d = ImageDraw.Draw(ec)
fa = ImageFont.truetype(fontp(False), 54); fb = ImageFont.truetype(fontp(), 76); fc_ = ImageFont.truetype(fontp(), 56)
d.text((540 - d.textlength('Community Covenant', font=fb) / 2, 700), 'Community Covenant', font=fb, fill=(245, 200, 90))
d.text((540 - d.textlength(ENDTXT[0], font=fa) / 2, 860), ENDTXT[0], font=fa, fill=(230, 230, 230))
d.text((540 - d.textlength(ENDTXT[1], font=fc_) / 2, 940), ENDTXT[1], font=fc_, fill=(255, 255, 255))
bw = d.textlength(ENDTXT[2], font=fc_) + 80
d.rounded_rectangle((540 - bw / 2, 1120, 540 + bw / 2, 1240), radius=24, fill=(204, 0, 0))
d.text((540 - d.textlength(ENDTXT[2], font=fc_) / 2, 1132), ENDTXT[2], font=fc_, fill=(255, 255, 255))
ec.save(f'{W}/END.png')

# ---- video clips
lst = []
for k, (sid, a, b) in enumerate(segs):
    dd = max(0.5, b - a); out = f'{W}/seg{k:02d}.mp4'
    if sid == 'TITLE':
        src = f'{W}/TITLE.png'; vf = 'scale=1080:1920,fps=30,format=yuv420p,fade=t=in:d=0.4'
    elif os.environ.get('MOTION') and os.path.exists(f"{os.environ['MOTION']}/{sid}.mp4"):
        mv = f"{os.environ['MOTION']}/{sid}.mp4"; md = dur(mv)
        if dd <= md * 1.6:
            sp = dd / md; pre = f"[0:v]setpts={sp:.4f}*PTS[v]"
        else:  # ping-pong loop for long segments
            sp = 1.3; n = int(dd / (2 * md * sp)) + 1
            pre = f"[0:v]setpts={sp}*PTS,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[pp];[pp]loop=loop={n}:size=999:start=0[v]"
        fc2 = pre + ";[v]scale=1108:1920:flags=lanczos,crop=1080:1920,fps=30,eq=contrast=1.06:saturation=0.92,vignette=PI/5,setsar=1,format=yuv420p,fade=t=in:d=0.3[o]"
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', mv, '-filter_complex', fc2, '-map', '[o]', '-t', f'{dd:.3f}', '-an',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out], check=True); lst.append(out); continue
    else:
        cover(img(sid), (1296, 2304)).save(f'{W}/i{k}.png'); src = f'{W}/i{k}.png'
        z = "min(1+0.0005*on,1.15)" if k % 2 == 0 else "max(1.15-0.0005*on,1)"
        vf = f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p,fade=t=in:d=0.35"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', src, '-vf', vf, '-t', f'{dd:.3f}', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '20', out], check=True); lst.append(out)
gap = END0 - segs[-1][2]
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-i', f'{W}/END.png', '-t', f'{TOT - segs[-1][2]:.3f}', '-vf',
                'fps=30,format=yuv420p,fade=t=in:d=0.5', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', f'{W}/end.mp4'], check=True)
lst.append(f'{W}/end.mp4')
open(f'{W}/list.txt', 'w').write(''.join(f"file '{x}'\n" for x in lst))

head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Poppins,58,&H00FFFFFF,&H00FFFFFF,&H70101010,&H70101010,1,0,0,0,100,100,0,0,3,14,0,2,70,70,300,1
Style: Chr,DejaVu Sans,58,&H0080D8F5,&H00FFFFFF,&H70101010,&H70101010,1,1,0,0,100,100,0,0,3,14,0,2,70,70,300,1
Style: Lab,DejaVu Sans,26,&H90FFFFFF,&H90FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,8,30,30,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = [f'Dialogue: 0,{at(0)},{at(END0)},Lab,,0,0,0,,{LABEL}']
ev += [f'Dialogue: 0,{at(a)},{at(b)},{"Cap" if w == "N" else "Chr"},,0,0,0,,{c}' for a, b, c, w in caps]
open(f'{W}/cap.ass', 'w', encoding='utf-8').write(head + '\n'.join(ev) + '\n')
# SRT for upload
def st(x): return f'{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int((x % 1) * 1000):03d}'
open(OUT.replace('.mp4', '.srt'), 'w', encoding='utf-8').write(''.join(f'{i + 1}\n{st(a)} --> {st(b)}\n{c}\n\n' for i, (a, b, c, w) in enumerate(caps)))
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', f'{W}/list.txt', '-i', f'{W}/audio.wav',
                '-vf', f'ass={W}/cap.ass', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22',
                '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', OUT], check=True)
print(OUT, round(dur(OUT), 1))
