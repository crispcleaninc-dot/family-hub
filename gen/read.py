# Cover to Cover full KJV reading in Ciarne's voice copy (F5-TTS, same reference as her films).
import json, os, re, subprocess
import pythonbible as pb
def verses(ch):
    out = []; v = 1
    while True:
        try:
            r = pb.get_references(f'Genesis {ch}:{v}')
            if not r: break
            vid = pb.convert_reference_to_verse_ids(r[0])[0]
            if vid // 1000 != 1000 + ch: break
            t = pb.get_verse_text(vid, version=pb.Version.KING_JAMES)
        except Exception: break
        if not t: break
        out.append(re.sub(r'[\[\]]', '', t).strip()); v += 1
    return out
DAYS = {1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9, 10]}
NEXT = {1: "Genesis 4 through 6, Cain and Abel and the days of Noah", 2: "Genesis 7 through 10, the flood, the rainbow, and the nations", 3: "Genesis 11 through 13, Babel, and the call of Abram"}
SUM = {1: "creation, Eden, and the first question in the Bible: Where art thou?", 2: "Cain and Abel, the line of Seth, and the days of Noah", 3: "the flood, the covenant of the rainbow, and the nations after Noah"}
Q = {1: "Where do you hear 'Did God really say?' in your own life?", 2: "Who is God asking you to check on this week?", 3: "What has God told you to build, even if people laugh?"}
SH = {1: ("So God created man in his own image, in the image of God created he him; male and female created he them.", "Genesis 1, verse 27", "Before you did anything, you already carried His image."),
      2: ("But Noah found grace in the eyes of the LORD.", "Genesis 6, verse 8", "In a world gone wrong, one man found grace. You can too."),
      3: ("I do set my bow in the cloud, and it shall be for a token of a covenant between me and the earth.", "Genesis 9, verse 13", "Every rainbow is God keeping His word.")}
items = []
for d, chs in DAYS.items():
    a, b = chs[0], chs[-1]; mid = chs[len(chs) // 2]
    items.append(('x', f'd{d:02d}_open', f"Welcome to Cover to Cover, day {d} of 365. Today we read Genesis {a} through {b}, from the King James Version: {SUM[d]}. Today's reading is brought to you by Community Covenant, a daily Bible, prayer and accountability app, so you never walk this alone. The link is in the post. Let's read."))
    for ch in chs:
        if ch == mid: items.append(('x', f'd{d:02d}_mid', "Quick pause. If you want to keep today's verses, track your reading and pray with others, it's all in Community Covenant, at covenant dot crispusmundo dot com. Now, let's keep reading."))
        items.append((f'g{ch:02d}', f'd{d:02d}_g{ch:02d}_h', f"Genesis, chapter {ch}."))
        for i, t in enumerate(verses(ch), 1): items.append((f'g{ch:02d}', f'd{d:02d}_g{ch:02d}_v{i:03d}', t))
    items.append(('x', f'd{d:02d}_close', f"That completes today's reading. {Q[d]} Answer in the comments, and if you'd like to talk about it live, vote in today's poll. To join Community Covenant, go to covenant dot crispusmundo dot com, tap Create Account, verify your email, choose your daily focus, and add it to your home screen. Tomorrow is {NEXT[d]}. Invite two people to read with us. See you tomorrow in the Word."))
    v, ref, line = SH[d]
    items.append(('x', f'd{d:02d}_short', f"{v} {ref}. {line} Day {d} of 365. Read the whole Bible with us in Faith and Findings."))
os.makedirs('out', exist_ok=True)
json.dump(items, open('out/script.json', 'w'), ensure_ascii=False)
G = os.environ['G']
RT = "The first one swung, the bottle was already in my hand. When it was over, her tooth was gone, and I was the one the police wanted."
api = None
try:
    from f5_tts.api import F5TTS
    api = F5TTS(model="F5TTS_v1_Base")
except Exception as e: print('api load failed, using cli:', e, flush=True)
for g, k, t in items:
    if g != G: continue
    t = t.replace('LORD', 'Lord'); f = f'out/{k}.wav'
    try:
        if not api: raise RuntimeError('no api')
        api.infer(ref_file='gen/her.wav', ref_text=RT, gen_text=t, file_wave=f, speed=0.92, nfe_step=32, cfg_strength=2.5)
    except Exception as e:
        print(k, 'api err', str(e)[:200], flush=True)
        subprocess.run(['f5-tts_infer-cli', '--model', 'F5TTS_v1_Base', '--ref_audio', 'gen/her.wav', '--ref_text', RT, '--gen_text', t,
                        '--output_dir', 'out', '--output_file', k + '.wav', '--speed', '0.92', '--nfe_step', '32'], capture_output=True)
    print(k, os.path.exists(f), flush=True)
