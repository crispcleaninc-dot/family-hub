# render.py FILM LANG  -> out/FILM_LANG.mp4
import json, os, sys, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, '/home/claude/cc4'); import music
B = '/home/claude/cc5'; fid, lang = sys.argv[1], sys.argv[2]
S = json.load(open(f'{B}/story2.json')); shots = [(sid, [(r, t[lang], t[lang]) for r, t in ls]) for sid, _, ls in S['films'][fid]['shots']]
PICK = json.load(open(f'{B}/picks.json'))
W, H, FPS, SR = 1920, 1080, 30, 44100
T = {'f5': {'fr': ('7,30 ce n’est pas 7 h 30', 'La juste balance'), 'en': ('7.30 Is Not Seven and a Half', 'Just weight')},
     'f6': {'en': ("What the Seminar Didn't Say", 'Tenants are not numbers')},
     'f7': {'hi': ('मैंने ख़ुद पढ़ा', 'रात के दो बजे, पहला पन्ना'), 'en': ('I Read It for Myself', '2 A.M. Page one.')},
     'f8': {'en': ('The Long Ride to Church', 'Faith on the way')}}
T0 = {'f1': {'es': ('Muchos padres', '¿A quién voy a llevar?'), 'en': ('Many Fathers', 'Who am I supposed to bring?')},
     'f2': {'es': ('Las oraciones selladas', 'Treinta días. Cinco sobres.'), 'en': ('The Sealed Prayers', 'Thirty days. Five envelopes.')},
     'f3': {'es': ('Mi hermano me lo dijo', 'Una llamada a medianoche'), 'en': ('My Brother Told Me', 'A call at midnight')},
     'f4': {'es': ('Caminando con la abuela', 'Veinte minutos al día'), 'en': ('Walking With Grandma', 'Twenty minutes a day')}}
SER = {'en': 'COMMUNITY COVENANT · CHRISTIAN SHORT FILM', 'fr': 'COMMUNITY COVENANT · COURT MÉTRAGE CHRÉTIEN', 'hi': 'COMMUNITY COVENANT · ईसाई लघु फ़िल्म'}
AIL = {'en': 'Dramatization. Pictures and voices made with AI.', 'fr': 'Fiction. Images et voix créées avec l’IA.', 'hi': 'नाट्य रूपांतरण। चित्र और आवाज़ें AI से बनाई गई हैं।'}
END = {'en': ('You are not alone.', 'covenant.crispusmundo.com', 'Subscribe for the next story'),
       'fr': ('Vous n’êtes pas seul.', 'covenant.crispusmundo.com', 'Abonnez-vous pour la prochaine histoire'),
       'hi': ('आप अकेले नहीं हैं।', 'covenant.crispusmundo.com', 'अगली कहानी के लिए सब्सक्राइब करें')}
FD = os.path.expanduser('~/.fonts/'); CG = FD + 'CormorantGaramond_700Bold.ttf'; CGI = FD + 'CormorantGaramond_600SemiBold_Italic.ttf'; PS = FD + 'Poppins_600SemiBold.ttf'
PLUM, GOLD = (43, 16, 48), (214, 177, 92)
wd = f'{B}/work/{fid}_{lang}'; os.makedirs(wd, exist_ok=True); os.makedirs(f'{B}/out', exist_ok=True)
def run(c): subprocess.run(c, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
def card(path, lines):
    im = Image.new('RGB', (W, H), PLUM); d = ImageDraw.Draw(im)
    for r in range(900, 0, -6):  # soft vignette glow
        c = tuple(int(PLUM[i] + (70 - r / 15) * (0.35 if i < 2 else 0.5)) for i in range(3))
    g = Image.new('RGB', (W, H), (0, 0, 0)); gd = ImageDraw.Draw(g); gd.ellipse((W/2-700, H/2-500, W/2+700, H/2+500), fill=(95, 45, 100)); g = g.filter(ImageFilter.GaussianBlur(220))
    im = Image.blend(im, g, 0.55); d = ImageDraw.Draw(im)
    cx, cy = W // 2, 250; d.ellipse((cx-95, cy-95, cx+95, cy+95), outline=GOLD, width=6)
    f = ImageFont.truetype(CG, 110); d.text((cx, cy+4), 'CC', font=f, fill=GOLD, anchor='mm')
    y = 430
    for txt, font, size, col in lines:
        fnt = ImageFont.truetype(font, size)
        while d.textlength(txt, font=fnt) > 1760 and size > 30: size -= 4; fnt = ImageFont.truetype(font, size)
        y += int(size * 0.75); d.text((cx, y), txt, font=fnt, fill=col, anchor='mm'); y += int(size * 0.75) + 26
    im.save(path)
def dur(p): return float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
TEMPO = {'es': 1.0, 'en': 1.0, 'fr': 1.0, 'hi': 1.0}
# 1) voice clips
k = 0; plan = []
for sid, ls in shots:
    clips = []
    for r, es, en in ls:
        mp3 = f'{B}/voices/{fid}_{k:03d}_{lang}.mp3'; wav = f'{wd}/v{k:03d}.wav'
        run(['ffmpeg', '-y', '-i', mp3, '-af', f'atempo={TEMPO[lang]}', '-ar', str(SR), '-ac', '1', wav])
        clips.append((wav, es if lang == 'es' else en, r)); k += 1
    plan.append((sid, clips))
# 2) timeline
TITLE = 3.6; t = TITLE; segs = []; subs = []; voice = []
for i, (sid, clips) in enumerate(plan):
    st = t; t += 0.45
    for wav, txt, r in clips:
        a, _ = sf.read(wav); d_ = len(a) / SR
        voice.append((t, a)); subs.append((t, t + d_, txt)); t += d_ + (0.30 if r == clips[-1][2] else 0.38)
    t += 0.55; segs.append((sid, st, max(t - st, 3.2))); t = st + max(t - st, 3.2)
END_D = 5.5; total = t + END_D
# 3) audio mix
vo = np.zeros(int(SR * total) + SR)
for st, a in voice: i = int(st * SR); vo[i:i + len(a)] += a
music.make(total, f'{wd}/music.wav'); mu, _ = sf.read(f'{wd}/music.wav'); mu = mu[:, 0][:len(vo)]
env = np.zeros(len(vo)); env[np.abs(vo) > 0.01] = 1
env = np.convolve(env, np.ones(int(SR * 0.6)) / int(SR * 0.6), 'same'); gain = 0.16 - 0.10 * np.clip(env * 3, 0, 1)
mix = vo + np.pad(mu, (0, len(vo) - len(mu))) * gain
sf.write(f'{wd}/mix.wav', np.clip(mix, -1, 1), SR)
# 4) cards
ti, sub = T[fid][lang]
if lang == 'hi': CG = CGI = PS
card(f'{wd}/title.png', [(SER[lang], PS, 30, GOLD), (ti, CG, 120, (255, 255, 255)), (sub, CGI, 58, (235, 220, 235))])
e1, e2, e3 = END[lang]
card(f'{wd}/end.png', [(e1, CG, 96, (255, 255, 255)), (e2, PS, 54, GOLD), (e3, PS, 36, (235, 220, 235))])
# 5) video clips
parts = []
def clip_from_png(png, d, out):
    run(['ffmpeg', '-y', '-loop', '1', '-i', png, '-t', f'{d:.3f}', '-vf', f'fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.5,fade=t=out:st={d-0.5:.3f}:d=0.5', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out])
clip_from_png(f'{wd}/title.png', TITLE, f'{wd}/c000.mp4'); parts.append(f'{wd}/c000.mp4')
for i, (sid, st, d) in enumerate(segs):
    img = f'{B}/img/{PICK[sid]}'; nf = int(d * FPS) + 1
    zin = i % 2 == 0
    z = f"'min(1.0+0.10*on/{nf},1.10)'" if zin else f"'max(1.10-0.10*on/{nf},1.0)'"
    x = "'iw/2-(iw/zoom/2)'" if i % 3 else "'(iw-iw/zoom)*on/%d'" % nf
    out = f'{wd}/c{i+1:03d}.mp4'
    run(['ffmpeg', '-y', '-i', img, '-vf', f"scale=3840:2194,crop=3840:2160,zoompan=z={z}:x={x}:y='ih/2-(ih/zoom/2)':d={nf}:s={W}x{H}:fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.35,fade=t=out:st={d-0.35:.3f}:d=0.35",
         '-t', f'{d:.3f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', out]); parts.append(out)
clip_from_png(f'{wd}/end.png', END_D, f'{wd}/c999.mp4'); parts.append(f'{wd}/c999.mp4')
open(f'{wd}/list.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f'{wd}/list.txt', '-c', 'copy', f'{wd}/video.mp4'])
# 6) captions + AI label
def ts(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
ass = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {W}', f'PlayResY: {H}', 'WrapStyle: 0', '', '[V4+ Styles]',
       'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
       'Style: Sub,Poppins SemiBold,64,&H00FFFFFF,&H00FFFFFF,&H00180A1C,&H78000000,0,0,0,0,100,100,0,0,1,4,1,2,160,160,80,1',
       'Style: AI,Poppins Medium,40,&H00E0E0E0,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,3,0,0,7,40,40,36,1', '', '[Events]',
       'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
ass.append(f'Dialogue: 0,{ts(TITLE)},{ts(TITLE+6)},AI,,0,0,0,,{AIL[lang]}')
for a, b, txt in subs: ass.append(f'Dialogue: 0,{ts(a)},{ts(b+0.15)},Sub,,0,0,0,,{txt}')
open(f'{wd}/caps.ass', 'w').write('\n'.join(ass) + '\n')
outp = f'{B}/out/{fid}_{lang}.mp4'
run(['ffmpeg', '-y', '-i', f'{wd}/video.mp4', '-i', f'{wd}/mix.wav', '-vf', f'ass={wd}/caps.ass', '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20',
     '-pix_fmt', 'yuv420p', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', '-c:a', 'aac', '-b:a', '160k', '-t', f'{total:.3f}', '-movflags', '+faststart', outp])
print(outp, round(total, 1))
