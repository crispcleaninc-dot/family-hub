/* v7: "how it works" built from real screenshots of the current app (shots/*.png, refreshed by capture.py) */
(function(){
const O=FN.slice();
function phone(t,imgs,ch,starts,tap){ // imgs: list of screenshot names, switched at starts[i]
  let k=0; starts.forEach((s,i)=>{ if(t>=s-.2)k=i; });
  let sc=''; imgs.forEach((n,i)=>{ const a=i===0?1:ramp(t,starts[i]-.2,.45); if(i<=k+1) sc+=`<img src="shots/${n}.png" class="abs" style="inset:0;width:100%;height:100%;object-fit:cover;object-position:top;opacity:${i<=k?a:0}">`; });
  const ap=ramp(t,.05,.5);
  let finger=''; if(tap){ const tp=tap[k]; if(tp){ const ph=((t-starts[k])%1.6)/1.6, r=ph<.5?ph*2:0; finger=`<div class="abs" style="left:${tp[0]}%;top:${tp[1]}%;width:110px;height:110px;margin:-55px 0 0 -55px;border-radius:50%;border:6px solid rgba(255,214,90,${1-r});transform:scale(${.4+r*.9})"></div><div class="abs" style="left:${tp[0]}%;top:${tp[1]}%;font-size:90px;margin:-10px 0 0 -20px;transform:translateY(${Math.sin(t*6)*4}px)">👆</div>`; } }
  return `<div class="abs" style="left:250px;top:285px;width:580px;height:1168px;border-radius:78px;background:#141a33;padding:20px;box-shadow:0 40px 90px rgba(0,0,0,.45);opacity:${ap};transform:translateY(${(1-easeOut(ap))*60}px)">
    <div style="position:relative;width:100%;height:100%;border-radius:60px;overflow:hidden;background:#FAF7F0">${sc}${finger}</div></div>`; }
function hdr(t,n,txt){ return `<div class="abs center" style="top:110px;font-size:36px;color:${GOLD};font-weight:700;letter-spacing:3px;text-shadow:0 2px 12px rgba(0,0,0,.6)">HOW IT WORKS · ${n}</div>
  <div class="abs center serif" style="top:165px;font-size:60px;font-weight:700;color:#FAF7F0;text-shadow:0 3px 14px rgba(0,0,0,.5);opacity:${ramp(t,.1,.5)}">${txt}</div>`; }
const st=(ch,i,d)=>ch[i]?.start??d;
const H1=function(t,D,sc,ch){ return APPBG(t)+hdr(t,1,'Say hi to the family')+phone(t,['home','home_tap'],ch,[0,st(ch,2,4)],[null,[30,26]]); };
const H2=function(t,D,sc,ch){ return APPBG(t)+hdr(t,2,'Animated books that read aloud')+phone(t,['shelf','read1','read2'],ch,[0,st(ch,1,2.5),st(ch,2,5)],[[30,40],[50,74],null]); };
const H3=function(t,D,sc,ch){ return APPBG(t)+hdr(t,3,'The Creative Studio')+phone(t,['move','chat'],ch,[0,(st(ch,0,.5)+D*.45)],[null,[50,20]]); };
const H4=function(t,D,sc,ch){ return APPBG(t)+hdr(t,4,'Your chat becomes a story')+phone(t,['plan','covenant'],ch,[0,st(ch,1,3)],[[50,88],null]); };
const N=O.slice(); N[9]=H1; N[10]=H2; N[11]=H3; N[12]=H4;
FN.length=0; N.forEach(f=>FN.push(f));
})();
