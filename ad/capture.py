# Captures real screens from the current app build for the commercial's "how it works" scenes.
import os, mimetypes, json, sys
from playwright.sync_api import sync_playwright
BUILD=sys.argv[1] if len(sys.argv)>1 else '/home/claude/gas/Index_v23.html'
html=open(BUILD).read()
stub=open('/home/claude/gas/test.py').read().split('stub="""')[1].split('"""')[0]
open('/tmp/cap.html','w').write(html.replace('<head>',"<head>"+stub,1))
ROOT='/home/claude/family-hub/'; OUT='/home/claude/ad/shots/'
def route(r):
    u=r.request.url.split('?')[0]; p=ROOT+u.split('/family-hub/')[1]
    if os.path.exists(p): r.fulfill(path=p,headers={'Access-Control-Allow-Origin':'*','Content-Type':mimetypes.guess_type(p)[0] or 'application/octet-stream'})
    else: r.fulfill(status=404,body='nf')
def ai(r):
    body=r.request.post_data or ''
    if 'one short reply from each' in body: c='[{"who":"Mommy","text":"Math can feel like a mountain, baby. We will climb it one step at a time, together."},{"who":"Jojo","text":"I used to mix up my numbers too! Want me to show you my trick?"}]'
    else: c='I am so proud of you for trying. Philippians 4:13!'
    r.fulfill(status=200,headers={'Access-Control-Allow-Origin':'*','Content-Type':'application/json'},body=json.dumps({'choices':[{'message':{'content':c}}]}))
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
    pg=b.new_page(viewport={'width':412,'height':860},device_scale_factor=2)
    pg.route('https://crispcleaninc-dot.github.io/**',route); pg.route('https://text.pollinations.ai/**',ai); pg.route('https://cdn.jsdelivr.net/**',lambda r:r.fulfill(status=404,body=''))
    pg.goto('file:///tmp/cap.html'); pg.wait_for_timeout(4000)
    pg.evaluate("window.scrollTo(0,0)"); pg.screenshot(path=OUT+'home.png')
    bx=pg.evaluate("(()=>{var r=document.querySelector('#bkHero .bh-c.jojo').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height*.4]})()")
    pg.mouse.click(bx[0],bx[1]); pg.wait_for_timeout(450); pg.screenshot(path=OUT+'home_tap.png')
    pg.evaluate("ME={username:'Jojo',progress:{}}; enterShelf();"); pg.wait_for_timeout(3500)
    y=pg.evaluate("(()=>{var e=document.getElementById('myStories')||document.getElementById('shelf'); return e.getBoundingClientRect().top+window.scrollY-120})()")
    pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(600); pg.screenshot(path=OUT+'shelf.png')
    pg.evaluate("STORY.open('moon-came-back')"); pg.wait_for_timeout(1500)
    for i,n in [(9,'read1'),(7,'read2'),(17,'covenant')]:
        pg.evaluate(f"document.querySelector('#sbDots i[data-i=\"{i}\"]').click()"); pg.wait_for_timeout(1600); pg.screenshot(path=OUT+n+'.png')
    pg.evaluate("STORY.close(); window.scrollTo(0,0); CS.open('move')"); pg.wait_for_timeout(1200)
    pg.evaluate("CS.mvAddActor(); CS.mvAddActor(); CS.mvAddActor(); CS.mvAddActor(); CS.mvPlay()"); pg.wait_for_timeout(1500)
    pg.evaluate("document.getElementById('mvC')&&document.getElementById('mvC').scrollIntoView({block:'start'})"); pg.screenshot(path=OUT+'move.png')
    pg.evaluate("CS.open('chat')"); pg.wait_for_timeout(2000)
    pg.fill('#chIn','Math is so hard for me'); pg.evaluate("CS.chSend()"); pg.wait_for_timeout(1200)
    pg.evaluate("CS.chPick('Jojo')"); pg.wait_for_timeout(500); pg.evaluate("document.querySelector('[data-ch2=yes]').click()"); pg.wait_for_timeout(600)
    pg.evaluate("Date.now=(function(o){return function(){return o()+60000}})(Date.now)")
    pg.fill('#chIn','Can you help me?'); pg.evaluate("CS.chSend()"); pg.wait_for_timeout(2500)
    pg.evaluate("document.getElementById('cs').scrollTop=0; window.scrollTo(0,0)"); pg.screenshot(path=OUT+'chat.png')
    pg.evaluate("STUDIO3D.makePlan()"); pg.wait_for_timeout(3000); pg.screenshot(path=OUT+'plan.png')
    print('ok')
    b.close()
