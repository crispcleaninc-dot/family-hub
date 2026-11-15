import json, subprocess, sys, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
VO = os.environ.get('VO','vo2')
lines = [l.strip() for l in open(os.path.join(HERE, 'lines.txt')) if l.strip()]
def dur(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode())
scenes = []
for i, text in enumerate(lines):
    vo = dur(os.path.join(HERE, VO, f'{i+1}.wav'))
    lead = 0.5
    tail = 2.2 if i == len(lines)-1 else 0.9
    scenes.append({'text': text, 'vo': vo, 'lead': lead, 'D': round(lead + vo + tail, 3)})
json.dump(scenes, open(os.path.join(HERE, 'scenes.json'), 'w'), indent=1)

mode = sys.argv[1]  # "stills" or "video"
FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.add_init_script(f'window.SCENES={json.dumps(scenes)};')
    pg.goto('file://' + os.path.join(HERE, os.environ.get('PAGE','ad.html')))
    pg.wait_for_timeout(500)
    if mode == 'stills':
        for spec in sys.argv[2:]:
            i, t = spec.split(':'); i = int(i); t = float(t)
            pg.evaluate(f'render({i},{t})')
            pg.screenshot(path=os.path.join(HERE, f'still_{i}_{t}.jpg'), type='jpeg', quality=85)
    else:
        os.makedirs(os.path.join(HERE, os.environ.get('OUT','scenes')), exist_ok=True)
        only = [int(x) for x in sys.argv[2:]] or range(len(scenes))
        for i in only:
            D = scenes[i]['D']; n = int(round(D * FPS))
            tmp = os.path.join(HERE, os.environ.get('OUT','scenes'), f's{i:02d}.tmp.mp4')
            ff = subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-',
                                   '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r',str(FPS),tmp], stdin=subprocess.PIPE)
            for f in range(n):
                pg.evaluate(f'render({i},{f/FPS})')
                ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close()
            if ff.wait() == 0:
                os.replace(tmp, os.path.join(HERE, os.environ.get('OUT','scenes'), f's{i:02d}.mp4'))
                print('scene', i, 'done', n, 'frames', flush=True)
    b.close()
