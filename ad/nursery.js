/* ---- v2: humanistic mother + nursery ---- */
const HAIR='#21130C', HAIRL='#5B3A26';
function curlRing(cx,cy,rx,ry,a0,a1,n,r,fill){let o='';for(let i=0;i<=n;i++){const a=(a0+(a1-a0)*i/n)*Math.PI/180;
  const x=cx+rx*Math.cos(a), y=cy+ry*Math.sin(a); const rr=r*(0.85+0.3*((i*37)%10)/10);
  o+=`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rr.toFixed(1)}" fill="${fill}"/>`;}return o;}
function curlMarks(cx,cy,rx,ry,n){let o='';for(let i=0;i<n;i++){const a=(i*137.5)%360*Math.PI/180, d=Math.sqrt(((i*53)%100)/100);
  const x=cx+rx*d*Math.cos(a), y=cy+ry*d*Math.sin(a);
  o+=`<path d="M${(x-8).toFixed(1)} ${y.toFixed(1)} q8 -12 16 0 q-6 10 -12 4" stroke="${HAIRL}" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".45"/>`;}return o;}
function hairBack(id){ // full, defined, styled curls framing the face down past the shoulders
  return `<ellipse cx="0" cy="-44" rx="156" ry="136" fill="${HAIR}"/>
   ${curlRing(0,-44,156,136,160,380,24,30,HAIR)}
   <path d="M-150 40 C-170 120 -140 190 -110 210 C-90 170 -100 100 -96 40Z" fill="${HAIR}"/>
   <path d="M150 40 C170 120 140 190 110 210 C90 170 100 100 96 40Z" fill="${HAIR}"/>
   <circle cx="-124" cy="56" r="34" fill="${HAIR}"/><circle cx="124" cy="56" r="34" fill="${HAIR}"/>${curlRing(-128,150,22,50,90,270,6,22,HAIR)}${curlRing(128,150,22,50,-90,90,6,22,HAIR)}
   ${curlMarks(0,-70,130,100,22)}`;}
function hairFront(id){ // side part, laid edges, curls on top
  return `<path d="M-90 -6 C-104 -112 -40 -158 18 -152 C92 -146 110 -84 92 -4 C84 -46 60 -72 24 -78 C-6 -70 -24 -60 -40 -54 C-64 -46 -82 -30 -90 -6Z" fill="${HAIR}"/>
   ${curlRing(10,-70,108,88,190,350,14,26,HAIR)}
   ${curlMarks(10,-104,80,30,8)}
   <path d="M24 -78 C10 -96 -10 -120 -24 -150" stroke="${HAIRL}" stroke-width="3" fill="none" opacity=".8"/>
   <path d="M-84 -14 q-8 -4 -4 -14 q6 6 2 14 M84 -14 q8 -4 4 -14 q-6 6 -2 14" stroke="${HAIR}" stroke-width="3" fill="${HAIR}"/>
   <path d="M-60 -50 q10 -6 20 -4 M40 -64 q12 2 22 10" stroke="#120904" stroke-width="2" fill="none" opacity=".6"/>`;}
const SK='#8A5434', SKD='#6E3F24', SKL='#A86E48';
function faceDefs(id){return `<defs>
 <radialGradient id="fg${id}" cx="45%" cy="40%" r="65%"><stop offset="0" stop-color="${SKL}"/><stop offset=".7" stop-color="${SK}"/><stop offset="1" stop-color="${SKD}"/></radialGradient>
 <linearGradient id="wrap${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D8B66A"/><stop offset="1" stop-color="#A9853C"/></linearGradient>
 <pattern id="pat${id}" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="7" cy="7" r="3.2" fill="${NAVY}" opacity=".55"/><path d="M14 20 l6 -6 l6 6 l-6 6z" fill="#7A2E2A" opacity=".45"/></pattern></defs>`;}
// head centred at 0,0 ; closed = sleepy/eyes-closed tender look
function head(o={}){const id=o.id||'h',closed=o.closed,b=o.blink;
  const eyes = closed||b ? `
   <path d="M-46 4 Q-30 14 -14 4" stroke="#2A160C" stroke-width="4" fill="none" stroke-linecap="round"/>
   <path d="M14 4 Q30 14 46 4" stroke="#2A160C" stroke-width="4" fill="none" stroke-linecap="round"/>
   <path d="M-44 8 l-4 5 M-36 11 l-2 6 M-26 11 l-1 6 M44 8 l4 5 M36 11 l2 6 M26 11 l1 6" stroke="#2A160C" stroke-width="2.4" stroke-linecap="round"/>`
  : `
   <path d="M-48 4 Q-30 -10 -12 4 Q-30 12 -48 4Z" fill="#F8F1E8"/><path d="M12 4 Q30 -10 48 4 Q30 12 12 4Z" fill="#F8F1E8"/>
   <circle cx="-30" cy="3" r="8.5" fill="#3A2214"/><circle cx="30" cy="3" r="8.5" fill="#3A2214"/>
   <circle cx="-30" cy="3" r="4" fill="#120904"/><circle cx="30" cy="3" r="4" fill="#120904"/>
   <circle cx="-27" cy="0" r="2.4" fill="#fff"/><circle cx="33" cy="0" r="2.4" fill="#fff"/>
   <path d="M-50 4 Q-30 -13 -10 3" stroke="#2A160C" stroke-width="4" fill="none" stroke-linecap="round"/>
   <path d="M10 3 Q30 -13 50 4" stroke="#2A160C" stroke-width="4" fill="none" stroke-linecap="round"/>`;
  const mouth = o.soft ? `<path d="M-22 70 Q0 80 22 70 Q0 88 -22 70Z" fill="#5A2620"/><path d="M-20 70 Q-8 64 0 67 Q8 64 20 70 Q0 74 -20 70Z" fill="#6E2F27"/>`
    : `<path d="M-26 66 Q0 90 26 66 Q0 76 -26 66Z" fill="#5A2620"/><path d="M-20 70 Q0 80 20 70 Q0 74 -20 70Z" fill="#fff" opacity=".85"/><path d="M-24 66 Q-10 60 0 63 Q10 60 24 66 Q0 70 -24 66Z" fill="#6E2F27"/>`;
  return `${faceDefs(id)}${hairBack(id)}
   <ellipse cx="-86" cy="16" rx="14" ry="22" fill="${SK}"/><ellipse cx="86" cy="16" rx="14" ry="22" fill="${SK}"/>
   <circle cx="-88" cy="44" r="9" fill="none" stroke="${GOLD}" stroke-width="4"/><circle cx="88" cy="44" r="9" fill="none" stroke="${GOLD}" stroke-width="4"/>
   <path d="M-84 -20 C-86 60 -50 118 0 120 C50 118 86 60 84 -20 C80 -70 -80 -70 -84 -20Z" fill="url(#fg${id})"/>
   <path d="M-56 -22 Q-34 -32 -14 -24" stroke="#24130A" stroke-width="6" fill="none" stroke-linecap="round"/>
   <path d="M14 -24 Q34 -32 56 -22" stroke="#24130A" stroke-width="6" fill="none" stroke-linecap="round"/>
   ${eyes}
   <path d="M-6 10 Q-8 34 -16 44 Q-8 52 0 48 Q8 52 16 44 Q8 34 6 10" stroke="${SKD}" stroke-width="3" fill="none" stroke-linecap="round" opacity=".8"/>
   <ellipse cx="-11" cy="46" rx="5" ry="3" fill="#4A2412" opacity=".6"/><ellipse cx="11" cy="46" rx="5" ry="3" fill="#4A2412" opacity=".6"/>
   <ellipse cx="-50" cy="38" rx="20" ry="11" fill="#B9614A" opacity=".28"/><ellipse cx="50" cy="38" rx="20" ry="11" fill="#B9614A" opacity=".28"/>
   <ellipse cx="-44" cy="26" rx="12" ry="5" fill="#fff" opacity=".10"/>
   ${mouth}
   ${hairFront(id)}`;
}
// replacement bust (same 400x520 box as old mom())
function mom(o={}){
  const arms = o.holdBaby ? `
    <path d="M70 520 C70 440 110 410 150 430 C200 455 250 455 300 430 C330 415 345 450 340 520Z" fill="${NAVY}"/>
    <path d="M118 470 C150 505 250 510 292 468 C300 460 312 470 304 482 C262 535 140 530 104 486 C96 474 108 462 118 470Z" fill="${SK}"/>`:'';
  return `<svg viewBox="0 0 400 520" width="100%" height="100%">
   <path d="M44 520 C50 400 118 360 200 360 C282 360 350 400 356 520Z" fill="${NAVY}"/>
   <path d="M140 366 Q200 430 260 366" fill="${SK}"/>
   <path d="M120 376 Q200 476 280 376" stroke="${GOLD}" stroke-width="8" fill="none" stroke-linecap="round"/>
   <rect x="170" y="290" width="60" height="90" rx="26" fill="${SKD}"/>
   <g transform="translate(200 214) scale(.98)">${head({id:'m'+Math.random().toString(36).slice(2,6),blink:o.blink,closed:o.closed,soft:o.soft})}</g>
   ${arms}</svg>`;
}
function swaddledBaby(id,sleep=true){return `
   <defs><radialGradient id="bf${id}" cx="45%" cy="40%" r="65%"><stop offset="0" stop-color="#B57A50"/><stop offset="1" stop-color="#8E5634"/></radialGradient></defs>
   <path d="M-70 40 C-90 120 -60 250 10 260 C80 262 96 150 76 60 C60 10 -50 0 -70 40Z" fill="#F4EBDD"/>
   <path d="M-80 100 C-30 116 30 116 84 96 M-78 160 C-30 176 30 176 86 156 M-60 220 C-20 232 30 232 72 214" stroke="${GOLD}" stroke-width="10" fill="none" opacity=".75"/>
   <circle cx="0" cy="-8" r="62" fill="url(#bf${id})"/>
   <path d="M-20 -66 q8 -14 18 -4 q8 -14 18 0 q-10 -4 -14 6 q-10 -8 -22 -2Z" fill="#2A1A12"/>
   <path d="M-34 -2 Q-24 6 -14 -2" stroke="#2A160C" stroke-width="3.5" fill="none" stroke-linecap="round"/>
   <path d="M14 -2 Q24 6 34 -2" stroke="#2A160C" stroke-width="3.5" fill="none" stroke-linecap="round"/>
   <ellipse cx="-38" cy="16" rx="12" ry="8" fill="#D2705A" opacity=".35"/><ellipse cx="38" cy="16" rx="12" ry="8" fill="#D2705A" opacity=".35"/>
   <path d="M-4 10 q4 6 8 0" stroke="#6E3F24" stroke-width="2.5" fill="none"/>
   <path d="M-8 26 Q0 31 8 26" stroke="#5A2412" stroke-width="3.5" fill="none" stroke-linecap="round"/>`;}
/* nursery: mother rocking, baby on her shoulder, hand patting */
function nursery(t,o={}){
  const rock=Math.sin(t*1.5)*2.2, pat=Math.max(0,Math.sin(t*5.2))*7, breathe=Math.sin(t*1.1)*3;
  let stars='';for(let i=0;i<9;i++){const x=150+(i*53)%260, y=200+(i*71)%220;stars+=`<circle cx="${x}" cy="${y}" r="${2+(i%3)}" fill="#FFF3D6" opacity="${.4+.5*Math.abs(Math.sin(t*1.3+i))}"/>`;}
  const tone=o.dim??1;
  return `<svg viewBox="0 0 1080 1440" width="1080" height="1440" style="position:absolute;left:0;top:0">
   <defs>
    <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E2A52"/><stop offset=".65" stop-color="#2F3A67"/><stop offset="1" stop-color="#3D3A5C"/></linearGradient>
    <radialGradient id="lamp" cx="82%" cy="58%" r="60%"><stop offset="0" stop-color="#FFD69A" stop-opacity="${.75+.04*Math.sin(t*7)}"/><stop offset=".45" stop-color="#F2B66E" stop-opacity=".28"/><stop offset="1" stop-color="#F2B66E" stop-opacity="0"/></radialGradient>
    <linearGradient id="wood" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6B4128"/><stop offset=".5" stop-color="#8E5C3A"/><stop offset="1" stop-color="#6B4128"/></linearGradient>
    <linearGradient id="sweater" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E8D5B5"/><stop offset="1" stop-color="#CDB48C"/></linearGradient>
   </defs>
   <rect width="1080" height="1440" fill="url(#wall)"/>
   <rect x="110" y="150" width="340" height="380" rx="170" fill="#16204A"/>
   ${stars}
   <path d="M330 250 a60 60 0 1 0 50 95 a48 48 0 1 1 -50 -95Z" fill="#FFF1C8"/>
   <rect x="110" y="150" width="340" height="380" rx="170" fill="none" stroke="#C9A961" stroke-width="10"/>
   <path d="M90 130 Q120 340 80 560 L60 560 L60 130Z" fill="#B88A4A" opacity=".85"/><path d="M470 130 Q440 340 480 560 L500 560 L500 130Z" fill="#B88A4A" opacity=".85"/>
   <rect x="0" y="1180" width="1080" height="260" fill="#4A3A4E"/>
   <ellipse cx="560" cy="1300" rx="420" ry="60" fill="#2A2238" opacity=".5"/>
   <rect x="860" y="760" width="16" height="420" fill="#5A4636"/><path d="M800 640 L936 640 L960 780 L776 780Z" fill="#F4D9A8"/>
   <rect width="1080" height="1440" fill="url(#lamp)"/>
   <g transform="rotate(${rock} 560 1240)">
    <path d="M300 1250 Q560 1320 860 1230" stroke="#5A3520" stroke-width="22" fill="none" stroke-linecap="round"/>
    <rect x="330" y="470" width="470" height="640" rx="70" fill="url(#wood)"/>
    ${[0,1,2,3].map(i=>`<rect x="${400+i*95}" y="530" width="26" height="520" rx="12" fill="#5E3922" opacity=".55"/>`).join('')}
    <rect x="320" y="1000" width="500" height="90" rx="30" fill="#7A4C30"/>
    <rect x="340" y="1080" width="30" height="170" fill="#6B4128"/><rect x="770" y="1080" width="30" height="170" fill="#6B4128"/>
    <g transform="translate(0 ${breathe*.4})">
     <path d="M360 1060 C350 820 420 700 560 690 C700 700 770 820 760 1060Z" fill="url(#sweater)"/>
     <path d="M520 700 Q560 760 600 700" fill="${SK}"/>
     <path d="M470 1050 C480 1120 640 1130 700 1060 L700 1000 L470 1000Z" fill="#2E3F73"/>
     <rect x="530" y="600" width="64" height="110" rx="28" fill="${SKD}"/>
     <g transform="translate(575 500) rotate(-13) scale(1.05)">${head({id:'n',closed:true,soft:true})}</g>
     <g transform="translate(445 ${700+breathe*.6}) rotate(-6)">${swaddledBaby('n')}</g>
     <path d="M372 1000 C380 920 470 900 560 930 C600 944 590 990 550 986 C480 980 430 1000 420 1040Z" fill="url(#sweater)"/>
     <g transform="translate(0 ${-pat})">
      <path d="M712 742 C752 850 650 890 548 820" stroke="#D9C29C" stroke-width="52" fill="none" stroke-linecap="round"/>
      <path d="M500 780 C482 770 470 800 486 812 C470 824 486 846 506 836 C500 856 528 864 540 846 C556 852 570 830 556 818 C566 800 548 782 530 790 C524 772 504 770 500 780Z" fill="${SK}"/>
     </g>
    </g>
   </g>
  </svg>`;
}
