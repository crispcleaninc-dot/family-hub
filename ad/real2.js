/* v6: biblical trust, newborn trust, "surely know thy mother" */
(function(){
const O=FN.slice();
function verseCard(t,a,ref,txt,top,fs){ return `<div class="abs" style="left:90px;right:90px;top:${top}px;border-radius:44px;background:rgba(27,41,81,.78);box-shadow:0 30px 70px rgba(0,0,0,.4);opacity:${a};transform:scale(${.94+.06*easeOut(a)});padding:56px 60px 50px">
  <div class="abs" style="inset:20px;border:4px solid ${GOLD};border-radius:30px"></div>
  <div class="center" style="position:relative;color:${GOLD};font-size:36px;font-weight:700;letter-spacing:4px">${ref}</div>
  <div class="center serif" style="position:relative;margin-top:26px;color:${CREAM};font-size:${fs||58}px;font-style:italic;font-weight:600;line-height:1.28">${txt}</div>
  <div class="center" style="position:relative;margin-top:24px;color:${GOLD};font-size:26px;letter-spacing:3px">KING JAMES VERSION</div></div>`; }
const LBL=(t,txt,top)=>`<div class="abs center" style="top:${top||110}px;font-size:40px;color:${GOLD};font-weight:700;letter-spacing:3px;text-shadow:0 2px 12px rgba(0,0,0,.6);opacity:${ramp(t,.1,.4)}">${txt}</div>`;
// A: faithful in the little things
function A(t,D,sc,ch){ const v=ramp(t,(ch[2]?.start||4)-.2,.6), dk=ramp(t,(ch[2]?.start||4)-.5,.8);
  return photo('m4_smile',t,D)+`<div class="abs" style="inset:0;background:rgba(10,14,40,${.45*dk})"></div>`+LBL(t,'THAT’S BIBLICAL')+
  `<div class="abs center serif" style="top:180px;font-size:70px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,(ch[1]?.start||1)-.2,.5)}">Faithful in the little things.<br><span style="color:${GOLD};font-style:italic">Trusted with much.</span></div>`+
  verseCard(t,v,'MATTHEW 25:21','“Well done, thou good and faithful servant: thou hast been faithful over a few things, I will make thee ruler over many things.”',760,54); }
// B: the Bible's word for trust
function B(t,D,sc,ch){ const d=ramp(t,.3,.6), v=ramp(t,(ch[2]?.start||7)-.2,.6);
  return photo('m6_pray',t,D,{dim:true,top:.5})+LBL(t,'WHAT IS TRUST?')+
  `<div class="abs" style="left:90px;right:90px;top:200px;border-radius:40px;background:rgba(255,250,240,.95);padding:44px 54px;box-shadow:0 20px 50px rgba(0,0,0,.35);opacity:${d};transform:translateY(${(1-easeOut(d))*40}px)">
    <div style="font-family:Lora,serif;font-size:76px;font-weight:700;color:${NAVY}">trust <span style="font-size:40px;font-weight:400;color:#8a6d3b;font-style:italic">· Hebrew “bāṭaḥ”</span></div>
    <div style="font-size:44px;line-height:1.3;color:${NAVY};margin-top:14px;opacity:${ramp(t,(ch[0]?.start||.5)+1.2,.5)}">to feel <b>safe</b>; to <b>rest secure</b> in someone who is <b style="color:#a77a1c">faithful</b>.</div></div>`+
  verseCard(t,v,'PROVERBS 3:5','“Trust in the LORD with all thine heart; and lean not unto thine own understanding.”',900,58); }
// C: newborn trust
function C(t,D,sc,ch){ const cs=[ch[3]?.start??6,ch[4]?.start??7.5,ch[5]?.start??9.5];
  const L=[['👶','I cry.'],['🤲','You come.'],['💛','I learn: Mama is faithful.']]; let cards='';
  L.forEach((l,i)=>{ const a=ramp(t,cs[i]-.15,.45); cards+=`<div class="abs" style="left:90px;right:90px;top:${880+i*200}px;height:170px;border-radius:36px;background:rgba(255,250,240,.94);display:flex;align-items:center;gap:30px;padding:0 40px;box-shadow:0 18px 40px rgba(0,0,0,.3);opacity:${a};transform:translateX(${(1-easeOut(a))*-120}px)"><span style="font-size:70px">${l[0]}</span><span style="font-size:50px;font-weight:600;color:${NAVY}">${l[1]}</span></div>`; });
  return photo('m1_smile',t,D)+LBL(t,'FOR A NEWBORN')+
  `<div class="abs center serif" style="top:180px;font-size:70px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,.3,.5)}">Trust looks<br><span style="color:${GOLD};font-style:italic">different.</span></div>
   <div class="abs center" style="top:420px;font-size:44px;font-weight:600;${LT};opacity:${ramp(t,(ch[1]?.start||3)-.2,.5)}">You can’t hand a baby a task.</div>`+cards; }
// D: Psalm 22:9 + trust for mama
function D_(t,D,sc,ch){ const v=ramp(t,.2,.6), sw=(ch[1]?.start||5)-.3; const st=[ch[1]?.start??5,ch[2]?.start??9];
  const L=['Let someone you love hold the baby.','Rest.','Trust God with what you can’t carry alone.'], ts=[st[0]+.6,st[0]+3.2,st[1]];
  let chips=''; L.forEach((l,i)=>{ const a=ramp(t,ts[i]-.15,.45); chips+=`<div style="display:inline-block;margin:12px;padding:20px 40px;border-radius:50px;background:${i==2?GOLD:'rgba(255,250,240,.95)'};color:${NAVY};font-size:42px;font-weight:600;opacity:${a};transform:scale(${a?.7+.3*back(a):.7});box-shadow:0 10px 26px rgba(0,0,0,.3)">${l}</div>`; });
  const vo=1-ramp(t,sw,.5);
  return xfade('m1_smile','m1_night',t,D,sw)+`<div class="abs" style="inset:0;opacity:${vo}">${verseCard(t,v,'PSALM 22:9','“Thou didst make me hope when I was upon my mother’s breasts.”',520,60)}</div>`+
  `<div class="abs center" style="top:110px;font-size:40px;color:${GOLD};font-weight:700;letter-spacing:3px;text-shadow:0 2px 12px rgba(0,0,0,.6);opacity:${ramp(t,sw,.4)}">AND FOR YOU, MAMA</div>
   <div class="abs center serif" style="top:180px;font-size:66px;font-weight:700;line-height:1.15;${LT};opacity:${ramp(t,sw+.2,.5)}">Trust is letting go,<br><span style="color:${GOLD};font-style:italic">a little.</span></div>
   <div class="abs center" style="top:900px;padding:0 60px">${chips}</div>`; }
// end verse + "surely know thy mother"
function K(t,D,sc,ch){ const s=ramp(t,(ch[1]?.start||3.5)-.2,.7);
  return O[9](t,D,sc,ch)+`<div class="abs center serif" style="top:220px;font-size:78px;font-weight:700;${LT};opacity:${s};transform:translateY(${(1-easeOut(s))*30}px)">And surely,<br><span style="color:${GOLD};font-style:italic">know thy mother.</span></div>`; }
const S9b=function(t,D,sc,ch){ return O[8](t,D,sc,ch).replace('REFLECTION','LET’S TALK'); };
const N=[O[0],O[1],A,B,O[2],C,D_,O[3],O[4],O[5],O[6],O[7],S9b,K,O[10]];
FN.length=0; N.forEach(f=>FN.push(f));
})();
