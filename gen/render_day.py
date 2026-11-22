# Render FNF Cover to Cover Day 1 dramatized reading (1280x720).
import os as _o; _o.makedirs('out', exist_ok=True)
import json, os, subprocess, re, glob
from PIL import Image, ImageDraw, ImageFont
import sys, glob as _g
DAY = int(sys.argv[1])
SEG = [tuple(x) for x in json.load(open('days_seg.json'))[str(DAY)]]
HER = '/tmp/d2her/out'; CH = '/tmp/d2chars/out'; IMG = '/tmp/d2img/out'; W = f'/tmp/dwork{DAY:02d}'
os.makedirs(W, exist_ok=True)
FPS = 25; WD, HT = 1280, 720
def run(c):
    r = subprocess.run(c, shell=True, capture_output=True, text=True)
    if r.returncode: print('CMD', c[:300], '\nERR', r.stderr[-1500:], flush=True); raise SystemExit(1)
def dur(f): return float(subprocess.run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{f}"', shell=True, capture_output=True, text=True).stdout)

# --- 1. clean each clip, measure gain, build timeline
def clean(src, dst, role):
    flt = 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,aresample=44100,highpass=f=70,lowpass=f=10000,lowpass=f=10000,bandreject=f=12000:width_type=h:w=1500'
    if role == 'god': flt += ',aecho=0.8:0.6:60|120:0.25|0.15'
    run(f'ffmpeg -nostdin -y -i "{src}" -af "{flt}" -ar 44100 -ac 1 "{dst}.tmp.wav"')
    o = subprocess.run(f'ffmpeg -i "{dst}.tmp.wav" -af ebur128 -f null - 2>&1', shell=True, capture_output=True, text=True).stdout
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', o)[-1])
    tgt = -16.5 if role in ('N', 'H') else -15.0
    run(f'ffmpeg -nostdin -y -i "{dst}.tmp.wav" -af "volume={tgt - I:.2f}dB,alimiter=limit=0.95" "{dst}"')
GAP = {'N': 0.35, 'H': 0.6}
tl = []; t = 1.0; missing = []
for i, (sid, role, text, ref, osrc) in enumerate(SEG):
    src = osrc if role == 'NR' else (f'{HER}/{sid}.wav' if role in ('N', 'H') else f'{CH}/{sid}.mp3')
    if role == 'NR': role = 'N'
    if not os.path.exists(src): missing.append(sid); continue
    dst = f'{W}/{sid}.wav'
    if not os.path.exists(dst): clean(src, dst, role)
    d = dur(dst)
    # shorter gap inside the same verse; longer between verses/hooks
    nxt = SEG[i + 1] if i + 1 < len(SEG) else None
    gap = 0.18 if (nxt and nxt[3] == ref and ref) else (0.9 if role == 'H' or (nxt and nxt[1] == 'H') else 0.45)
    tl.append(dict(sid=sid, role=role, text=text, ref=ref, st=t, d=d)); t += d + gap
TOT = t + 2.5
json.dump(dict(tl=tl, missing=missing, tot=TOT), open(f'{W}/tl.json', 'w'), indent=0)
print('missing', missing, 'total', round(TOT, 1))

# --- 2. shots: day images spread evenly across the reading
cand = [f'{IMG}/d{DAY:02d}_n{i}.webp' for i in range(1, 7)]
sk = sorted(_g.glob(f'/tmp/skimg/fnf-out-img-d{DAY:02d}_s[123]/out/*_7101.webp'))
pics = [p for p in cand if os.path.exists(p)]
order = []
for i in range(max(len(pics), len(sk))):
    if i < len(pics): order.append(pics[i])
    if i < len(sk): order.append(sk[i])
if len(order) < 4: order += sorted(_g.glob('/tmp/d1img/out/v0[3-9].webp'))[:4 - len(order)]
n = len(order); blocks = []
seglen = TOT / n
cuts = [0]
for k in range(1, n):
    tgt = k * seglen
    starts = [e['st'] for e in tl]
    cuts.append(min(starts, key=lambda x: abs(x - tgt)))
cuts.append(TOT)
for k in range(n): blocks.append([order[k], cuts[k], cuts[k + 1]])
def img(s): return s
parts = []
for i, (s, a, b) in enumerate(blocks):
    d = b - a; n = max(1, int(round(d * FPS))); p = f'{W}/b{i:03d}.mp4'
    if os.path.exists(p) and os.path.getsize(p) > 1000: parts.append(p); continue
    Image.open(img(s)).convert('RGB').resize((1920, 1080)).save(f'{W}/b{i:03d}.png')
    z = "min(zoom+0.0006,1.18)" if i % 2 == 0 else "if(eq(on,0),1.18,max(zoom-0.0006,1.0))"
    run(f'ffmpeg -nostdin -y -loop 1 -i {W}/b{i:03d}.png -vf "zoompan=z=\'{z}\':x=\'iw/2-(iw/zoom/2)\':y=\'ih/2-(ih/zoom/2)\':d={n}:s={WD}x{HT}:fps={FPS},eq=brightness=-0.06:saturation=1.05,format=yuv420p" -frames:v {n} -c:v libx264 -preset veryfast -crf 22 {p}')
    parts.append(p)
open(f'{W}/v.txt', 'w').write(''.join(f"file '{p}'\n" for p in parts))
run(f'ffmpeg -nostdin -y -f concat -safe 0 -i {W}/v.txt -c copy {W}/vid.mp4') if not os.path.exists(f'{W}/vid.mp4') else None

# --- 3. captions (ASS)
from hooks import DAYS as _D
_ch = _D[DAY]['ch']; RNG = f'Genesis {_ch[0]}–{_ch[-1]}'
def at(x): h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60; return f'{h}:{m:02d}:{s:05.2f}'
NAME = {'god': 'THE LORD', 'serpent': 'THE SERPENT', 'Eve': 'EVE', 'angel': 'THE ANGEL', 'crowd': 'THEY'}
def chunks(text, n=78):
    w = text.split(); out = []; cur = ''
    for x in w:
        if len(cur) + len(x) + 1 > n and cur: out.append(cur); cur = x
        else: cur = (cur + ' ' + x).strip()
    out.append(cur)
    return [' '.join(out[i:i + 2]) for i in range(0, len(out), 2)]
head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WD}
PlayResY: {HT}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Ver,DejaVu Serif,34,&H00F2F6FA,&H00FFFFFF,&H90101010,&H90101010,1,0,0,0,100,100,0,0,3,10,0,2,110,110,48,1
Style: Chr,DejaVu Serif,34,&H0080D8F5,&H00FFFFFF,&H90101010,&H90101010,1,1,0,0,100,100,0,0,3,10,0,2,110,110,48,1
Style: Hook,DejaVu Sans,32,&H00FFFFFF,&H00FFFFFF,&H90401040,&H90401040,1,0,0,0,100,100,0,0,3,10,0,2,110,110,48,1
Style: Ref,DejaVu Serif,24,&H0080D8F5,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,1,9,30,30,26,1
Style: Lab,DejaVu Sans,17,&H90FFFFFF,&H90FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,24,24,20,1
Style: Ttl,DejaVu Serif,62,&H0080D8F5,&H00FFFFFF,&H00000000,&HA0000000,1,0,0,0,100,100,2,0,1,3,2,5,60,60,60,1
Style: Sub,DejaVu Serif,32,&H00F2F6FA,&H00FFFFFF,&H00000000,&HA0000000,0,1,0,0,100,100,1,0,1,2,1,5,60,60,60,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = [f'Dialogue: 2,{at(0)},{at(TOT)},Lab,,0,0,0,,Faith & Findings Forum · Cover to Cover · Dramatization · AI voices']
for e in tl:
    cs = chunks(e['text']); L = sum(len(c) for c in cs)
    x = e['st']
    for c in cs:
        y = x + e['d'] * len(c) / L
        if e['role'] == 'H': st, txt = 'Hook', c
        elif e['role'] not in ('N', 'H'): st, txt = 'Chr', f'{NAME.get(e["role"], e["role"].upper())}: {c}'
        else: st, txt = 'Ver', c
        ev.append(f'Dialogue: 1,{at(x)},{at(y + (0.25 if c == cs[-1] else 0))},{st},,0,0,0,,{txt}')
        x = y
    if e['ref']: ev.append(f'Dialogue: 2,{at(e["st"])},{at(e["st"] + e["d"] + 0.3)},Ref,,0,0,0,,{e["ref"]} · KJV')
h1 = next(e for e in tl if e['sid'].endswith('_h1'))
ev.append(f'Dialogue: 3,{at(h1["st"])},{at(h1["st"] + 5.5)},Ttl,,0,0,0,,{{\\fad(400,400)\\pos(640,300)}}COVER TO COVER · DAY {DAY}')
ev.append(f'Dialogue: 3,{at(h1["st"])},{at(h1["st"] + 5.5)},Sub,,0,0,0,,{{\\fad(400,400)\\pos(640,380)}}{RNG} · King James Version (KJV) · word for word')
open(f'{W}/cap.ass', 'w').write(head + '\n'.join(ev) + '\n')

# --- 4. audio: voices + music bed (c1 Genesis 1, c2 Genesis 2, c3 Genesis 3) ducked
inp = ''; flt = ''
for k, e in enumerate(tl):
    inp += f' -i {W}/{e["sid"]}.wav'
    flt += f'[{k}:a]adelay={int(e["st"] * 1000)}:all=1[a{k}];'
flt += ''.join(f'[a{k}]' for k in range(len(tl))) + f'amix=inputs={len(tl)}:normalize=0,apad=whole_dur={TOT}[v]'
open(f'{W}/vf.txt', 'w').write(flt)
run(f'ffmpeg -nostdin -y{inp} -filter_complex_script {W}/vf.txt -map "[v]" -t {TOT} -ar 44100 -ac 2 {W}/voice.wav')
# music: her approved palette, rotating piano -> organ -> ambience about every 30 s with crossfades
import numpy as np, soundfile as sf
ORDER = ['soft1', 'hymn2', 'qa2', 'soft2', 'hymn3', 'qa3', 'soft3', 'qa4', 'hymn2', 'qa5', 'soft1', 'qa6']
_CC = {}
def cue(k):
    if k in _CC: return _CC[k]
    a, sr0 = sf.read(f'/tmp/mus/out/{k}.wav'); a = a.mean(1) if a.ndim > 1 else a
    S0 = np.abs(np.fft.rfft(a)); f0 = np.fft.rfftfreq(len(a), 1 / sr0); m0 = (f0 > 1200) & (f0 < 9000)
    med0 = np.median(S0[m0]) + 1e-9; cand = np.where(m0 & (S0 > 300 * med0))[0]
    peaks = []
    for i in cand[np.argsort(-S0[cand])]:
        fq = f0[i]
        if all(abs(fq - p) > 80 for p in peaks): peaks.append(fq)
        if len(peaks) >= 6: break
    br = ''.join(f',bandreject=f={p:.0f}:width_type=h:w=60' for p in peaks)
    import subprocess as sp
    sp.run(f'ffmpeg -nostdin -v error -y -i /tmp/mus/out/{k}.wav -af "aresample=44100{br},lowpass=f=7000" -ac 1 {W}/m_{k}.wav', shell=True, check=True)
    a, sr = sf.read(f'{W}/m_{k}.wav'); _CC[k] = a.astype(np.float32); return _CC[k]
sr = 44100; N = int(TOT * sr); mus = np.zeros(N, np.float32); pos = 0; i = 0; X = int(3 * sr)
while pos < N:
    c = cue(ORDER[i % len(ORDER)]); i += 1
    L = min(len(c), N - pos)
    if L < 2 * X: break
    env = np.ones(L, np.float32); f = min(X, L // 2)
    env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
    mus[pos:pos + L] += c[:L] * env
    pos += max(L - X, 1)
mus = mus / (np.abs(mus).max() + 1e-9) * 0.5
sf.write(f'{W}/music_raw.wav', mus, sr)
run(f'ffmpeg -nostdin -y -i {W}/music_raw.wav -af "volume=-15dB" -ac 2 -t {TOT} {W}/music.wav')
run(f'ffmpeg -nostdin -y -i {W}/voice.wav -i {W}/music.wav -filter_complex "[1:a][0:a]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[d];[0:a][d]amix=inputs=2:normalize=0,alimiter=limit=0.95[o]" -map "[o]" -c:a aac -b:a 160k {W}/mix.m4a')
run(f'ffmpeg -nostdin -y -i {W}/vid.mp4 -i {W}/mix.m4a -vf "ass={W}/cap.ass" -map 0:v -map 1:a -c:v libx264 -preset veryfast -crf 23 -c:a copy -shortest -movflags +faststart ../out/Day{DAY:02d}_Reading_Drama.mp4')
print('done', round(TOT, 1))
