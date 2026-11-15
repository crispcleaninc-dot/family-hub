/* Real-photo scenes: layered "living photo" (background + cut-out mother move separately) */
const R='real/';
function photo(n,t,D,o={}){
  const p=clamp(t/(D||8)), br=Math.sin(t*1.3)*0.004, dir=o.dir||1;
  const bgS=1.10+0.05*p, fgS=1.06+0.09*p+br;
  const sweep=((t*0.12+(o.off||0))%1.6)-0.3;
  let dust=''; for(let i=0;i<14;i++){ const x=(i*97+n.length*31)%1080, y0=(i*263)%1920, y=(y0- t*(14+(i%4)*6)+1920)%1920, a=.18+.22*Math.abs(Math.sin(t*1.2+i));
    dust+=`<div class="abs" style="left:${x}px;top:${y}px;width:${4+(i%3)*3}px;height:${4+(i%3)*3}px;border-radius:50%;background:#fff6dc;opacity:${a};filter:blur(1px)"></div>`; }
  return `<div class="abs" style="inset:0;overflow:hidden;background:#111">
    <img src="${R}${n}.jpg" class="abs" style="left:0;top:0;width:1080px;height:1920px;object-fit:cover;transform:scale(${bgS}) translateX(${-1.4*p*dir}%);transform-origin:50% 40%;filter:blur(2.2px) brightness(${o.dim?0.62:0.92})">
    <img src="${R}${n}_fg.png" class="abs" style="left:0;top:0;width:1080px;height:1920px;object-fit:cover;transform:scale(${fgS}) translateX(${0.9*p*dir}%) translateY(${-0.6*p}%);transform-origin:50% 42%;filter:brightness(${o.dim?0.7:1.02}) saturate(1.05)">
    <div class="abs" style="inset:0;background:linear-gradient(105deg,rgba(255,230,180,0) ${sweep*100-18}%,rgba(255,230,180,.22) ${sweep*100}%,rgba(255,230,180,0) ${sweep*100+18}%);mix-blend-mode:screen"></div>
    <div class="abs" style="inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%)"></div>
    ${dust}
    <div class="abs" style="left:0;right:0;top:0;height:640px;background:linear-gradient(rgba(10,14,40,${o.top??.78}),rgba(10,14,40,0))"></div>
    <div class="abs" style="left:0;right:0;bottom:0;height:620px;background:linear-gradient(rgba(10,14,40,0),rgba(10,14,40,.72))"></div>
  </div>`;
}
function xfade(a,b,t,D,at,o){ const k=ease(ramp(t,at,.9)); return `<div class="abs" style="inset:0">${photo(a,t,D,o)}</div><div class="abs" style="inset:0;opacity:${k}">${photo(b,t,D,Object.assign({},o,{dir:-1,off:.5}))}</div>`; }
const LT='color:#FAF7F0;text-shadow:0 3px 18px rgba(0,0,0,.55)';
FN[0]=function(t,D){ const ul=ease(ramp(t,1.2,.8));
  return photo('m1_night',t,D)+`<div class="abs center serif" style="top:120px;font-size:80px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,.15,.5)}">This book is<br>not for <span style="color:${GOLD};font-style:italic">perfectionists.</span>
   <svg class="abs" style="left:440px;top:206px" width="420" height="40" viewBox="0 0 420 40"><path d="M8 26 Q120 6 210 22 T412 16" stroke="${GOLD}" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="460" stroke-dashoffset="${460*(1-ul)}"/></svg></div>`; };
FN[1]=function(t,D,sc,ch){ const cs=[ch[2]?.start??5,ch[3]?.start??7,ch[4]?.start??10,ch[5]?.start??12];
  const dimK=ramp(t,cs[0]-.4,.6);
  const labels=['I give you a task.','I leave you to it,<br><span style="font-weight:400;font-size:36px">because I taught you how.</span>','I return. It’s done.'], ics=['📝','🚪','✅'];
  let cards=''; for(let i=0;i<3;i++){ const a=ramp(t,cs[i]-.15,.45), y=760+i*210;
    cards+=`<div class="abs" style="left:90px;right:90px;top:${y}px;height:180px;border-radius:36px;background:rgba(255,250,240,.93);display:flex;align-items:center;gap:30px;padding:0 40px;box-shadow:0 18px 40px rgba(0,0,0,.3);opacity:${a};transform:translateX(${(1-easeOut(a))*-120}px)"><span style="font-size:72px">${ics[i]}</span><span style="font-size:46px;font-weight:600;line-height:1.15;color:${NAVY}">${labels[i]}</span></div>`; }
  const st=ramp(t,cs[3]-.1,.35);
  return photo('m4_smile',t,D,{dim:dimK>.5})+`<div class="abs" style="inset:0;background:rgba(10,14,40,${.35*dimK})"></div>
   <div class="abs center serif" style="top:130px;font-size:74px;font-weight:700;${LT};opacity:${ramp(t,.1,.5)}">“I have to be able<br>to trust you.”</div>
   <div class="abs center" style="top:370px;font-size:42px;color:${GOLD};font-weight:700;letter-spacing:3px;text-shadow:0 2px 12px rgba(0,0,0,.5);opacity:${ramp(t,(ch[1]?.start||3)-.2,.5)}">TRUST LOOKS LIKE THIS</div>
   ${cards}<div class="abs" style="left:560px;top:1350px;transform:rotate(-8deg) scale(${st?(1.6-0.6*back(st)):0});opacity:${st};border:7px solid ${GOLD};color:${GOLD};border-radius:20px;padding:8px 30px;font-size:58px;font-weight:700;letter-spacing:3px;background:rgba(27,41,81,.85)">THOROUGHLY</div>`; };
FN[2]=function(t,D,sc,ch){ const a=ramp(t,(ch[2]?.start||3)-.2,.6);
  return photo('m3_stairs',t,D)+`<div class="abs center serif" style="top:130px;font-size:80px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,.1,.5)}">But trust goes<br><span style="color:${GOLD};font-style:italic">both ways.</span></div>
   <div class="abs center" style="top:390px;font-size:46px;font-weight:600;${LT};opacity:${ramp(t,(ch[1]?.start||1.5)-.1,.5)}">My children need to know me, too.</div>
   <div class="abs center" style="top:1180px;opacity:${a};transform:scale(${.8+.2*back(a)})"><span style="display:inline-block;background:linear-gradient(135deg,#1B2951,#5a2d6e);border:4px solid ${GOLD};color:${CREAM};font-family:Lora,serif;font-weight:700;font-size:64px;padding:24px 50px;border-radius:30px;box-shadow:0 18px 40px rgba(0,0,0,.4)">Mommy Is <span style="color:${GOLD}">Human Too</span></span></div>`; };
FN[3]=function(t,D,sc,ch){ const words=[['Tired.','#EADBBE'],['Learning.','#D7E4E6'],['Still loving.',GOLD]];
  let chips=''; words.forEach((w,i)=>{ const s=ch[1+i]?.start||4+i, a=ramp(t,s-.15,.4); chips+=`<span class="chip" style="background:${w[1]};color:${NAVY};opacity:${a};transform:scale(${a?.6+.4*back(a):.6});box-shadow:0 10px 26px rgba(0,0,0,.3)">${w[0]}</span>`; });
  const sw=(ch[3]?.start||6)-.4;
  return xfade('m1_tear','m1_smile',t,D,sw)+`<div class="abs center" style="top:110px;font-size:40px;color:${GOLD};font-weight:700;letter-spacing:3px;text-shadow:0 2px 12px rgba(0,0,0,.6);opacity:${ramp(t,.1,.4)}">FOR NEW &amp; POSTPARTUM MOMS</div>
   <div class="abs center serif" style="top:180px;font-size:66px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,.3,.5)}">A gentle way to show<br>your human side.</div>
   <div class="abs center" style="top:1250px">${chips}</div>`; };
FN[4]=function(t,D){ return photo('m4_pancakes',t,D)+`<div class="abs center" style="top:110px;font-size:40px;color:${GOLD};font-weight:700;letter-spacing:3px;text-shadow:0 2px 12px rgba(0,0,0,.6);opacity:${ramp(t,.1,.4)}">FOR CHILDREN</div>
   <div class="abs center serif" style="top:180px;font-size:64px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,.3,.5)}">A way to understand<br>the mother who<br><span style="color:${GOLD};font-style:italic">labors among them.</span></div>`; };
// app steps: real mother softly behind the phone
const APPBG=(t)=>`<div class="abs" style="inset:0;overflow:hidden"><img src="${R}m1_smile.jpg" class="abs" style="left:0;top:0;width:1080px;height:1920px;object-fit:cover;filter:blur(18px) brightness(.55) saturate(1.1);transform:scale(${1.15+0.02*Math.sin(t*.4)})"></div><div class="abs" style="inset:0;background:linear-gradient(rgba(27,41,81,.35),rgba(90,45,110,.35))"></div>`;
[5,6,7,8].forEach(i=>{ const f=FN[i]; FN[i]=function(t,D,sc,ch){ return APPBG(t)+f(t,D,sc,ch).replace(/color:\$\{NAVY\}/g,''); }; });
const _howHdr=howHdr; howHdr=function(t,n,label,first){ return _howHdr(t,n,label,first).replace('font-size:60px;font-weight:700;','font-size:60px;font-weight:700;color:#FAF7F0;text-shadow:0 3px 14px rgba(0,0,0,.5);'); };
FN[9]=function(t,D){ const a=ramp(t,.2,.7);
  return photo('m6_pray',t,D,{dim:true,top:.5})+`<div class="abs" style="left:110px;right:110px;top:560px;height:760px;border-radius:50px;background:rgba(27,41,81,.72);backdrop-filter:blur(4px);box-shadow:0 30px 70px rgba(0,0,0,.4);opacity:${a};transform:scale(${.94+.06*easeOut(a)})">
     <div class="abs" style="inset:26px;border:4px solid ${GOLD};border-radius:34px"></div>
     <div class="abs center" style="top:100px;color:${GOLD};font-size:40px;font-weight:700;letter-spacing:4px">1 THESSALONIANS 5:12</div>
     <div class="abs center serif" style="top:210px;padding:0 70px;color:${CREAM};font-size:80px;font-style:italic;font-weight:600;line-height:1.25;opacity:${ramp(t,.8,.8)}">“Know them which labour among you.”</div>
     <div class="abs center" style="top:640px;color:${GOLD};font-size:32px;letter-spacing:3px">KING JAMES VERSION</div></div>`; };
FN[10]=function(t,D,sc,ch){ const seq=['m1_smile','m4_smile','m3_stairs','m6_pray']; const seg=2.4; const k=Math.min(seq.length-1,Math.floor(t/seg));
  let bg=''; for(let i=0;i<=k;i++){ const op=i===0?1:ease(ramp(t,i*seg,.7)); bg+=`<div class="abs" style="inset:0;opacity:${op}">${photo(seq[i],t-i*seg+2,6,{dir:i%2?-1:1,top:.6})}</div>`; }
  const L=['Grace for mothers.','Understanding for children.','Trust for the whole family.']; let ls='';
  L.forEach((l,i)=>{ const a=ramp(t,(ch[i]?.start||i)-.15,.4); ls+=`<div style="opacity:${a};transform:translateY(${(1-easeOut(a))*24}px);margin:6px 0">${l}</div>`; });
  const T=ramp(t,(ch[3]?.start||5)-.2,.6), C=ramp(t,(ch[4]?.start||7)-.2,.5), dk=ramp(t,(ch[3]?.start||5)-.4,.8);
  return bg+`<div class="abs" style="inset:0;background:rgba(10,14,40,${.55*dk})"></div>
   <div class="abs center serif" style="top:120px;font-size:58px;font-weight:600;line-height:1.25;${LT}">${ls}</div>
   <div class="abs center serif" style="top:560px;font-size:118px;font-weight:700;line-height:1.02;${LT};opacity:${T};transform:scale(${.9+.1*easeOut(T)})">Mommy Is<br><span style="color:${GOLD}">Human Too</span></div>
   <div class="abs center" style="top:840px;font-size:36px;font-weight:700;letter-spacing:3px;color:#FAF7F0;opacity:${T}">A PICTURE BOOK SERIES &amp; READ-ALONG APP</div>
   <div class="abs center" style="top:950px;opacity:${C}"><span style="display:inline-block;background:${GOLD};color:${NAVY};font-size:54px;font-weight:700;border-radius:70px;padding:26px 70px;transform:scale(${C?.8+.2*back(C):.8});box-shadow:0 12px 30px rgba(0,0,0,.35)">Download the free app</span>
     <div style="margin-top:28px;font-size:38px;font-style:italic;font-family:Lora,serif;${LT}">Not for perfectionists. For families.</div></div>`; };
// app screens show the real 3D cast from the books (applied after all scripts load)
window.addEventListener('DOMContentLoaded',function(){
mom=function(){ return '<img src="cast/mommy.webp" style="width:100%;height:100%;object-fit:contain;object-position:50% 0%">'; };
jojo=function(){ return '<img src="cast/jojo.webp" style="width:100%;height:100%;object-fit:contain;object-position:50% 100%">'; };
pip=function(){ return '<img src="cast/pip.webp" style="width:100%;height:100%;object-fit:contain;object-position:50% 100%">'; };
baby=function(){ return '<img src="cast/bee.webp" style="width:100%;height:100%;object-fit:contain;object-position:50% 100%">'; };
});
