(() => {
'use strict';
const files=['NCF09590.jpg','PIE00746_1.jpg','NCF09664.jpg','NCF00448.jpg','NCF03602-scaled.jpg','NCF07467-scaled.jpg','NCF09521.jpg','NCF00205.jpg','NCF00964-scaled.jpg','NCF01058-scaled.jpg','NCF04421-scaled.jpg','6.jpg'];
const places=['Amalfi','Firenze','Torino','Lago di Como','Siena','Roma'];
const stories=places.map((place,i)=>({id:i,place,cover:files[i],photos:Array.from({length:8},(_,j)=>files[(i+j)%files.length])}));
const desk=document.querySelector('.hero'),stage=desk.querySelector('.p-stage');
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v)),ease=t=>{t=clamp(t,0,1);return t*t*t*(t*(t*6-15)+10)},mix=(a,b,t)=>a+(b-a)*t;
const asset=f=>'assets/optimized/'+f;
let geom={},positions=[],active=true,progress=0,homeProgress=0,mode='intro',stack=10;
const scattered=[[.22,.40],[.58,.32],[.76,.61],[.33,.70],[.49,.54],[.80,.32]],mobile=[[.32,.30],[.67,.40],[.32,.58],[.65,.72],[.55,.53],[.43,.76]],angles=[-12,9,-8,12,-5,7];
const cards=stories.map((story,i)=>{
 const card=document.createElement('button');card.type='button';card.className='p-card';card.dataset.story=String(i);card.setAttribute('aria-label',`Stampa fotografica: ${story.place}`);
 card.innerHTML=`<span class="p-card-inner"><span class="p-face p-front"><img src="${asset(story.cover)}" alt="Fotografia dell'archivio di Nicola Capasso" draggable="false"><span class="p-location">${story.place}</span></span></span>`;
 stage.append(card);return card;
});
const gridHint=document.createElement('p');gridHint.className='p-grid-hint';gridHint.textContent='Tocca una fotografia, entra nella storia.';gridHint.setAttribute('aria-hidden','true');stage.append(gridHint);
function measure(){
 const w=stage.clientWidth,h=motion.matches?stage.clientHeight/2:stage.clientHeight,short=h<600&&w>700,cols=short?6:w>700?3:2,rows=Math.ceil(cards.length/cols),top=short?83:112,bottom=short?58:84,aw=w*.86,ah=h-top-bottom,cellW=aw/cols,cellH=ah/rows;
 const cw=Math.max(65,Math.min(w<=700?156:230,cellW-20,(cellH-18)*.74)),ch=cw/.74;
 geom={w,h,cw,ch,cols,rows,top,bottom,cellW,cellH,range:Math.max(1,desk.offsetHeight-h)};
 positions=cards.map((card,i)=>{
  card.style.width=cw+'px';card.style.height=ch+'px';
  const points=w<=700?mobile:scattered;
  const diagonal=Math.hypot(cw,ch)/2+7;
  const cx=clamp(points[i][0]*w,diagonal,w-diagonal),cy=clamp(points[i][1]*h,top+diagonal,h-bottom-diagonal);
  return {x:cx-cw/2,y:cy-ch/2,rotation:angles[i],gx:w*.07+(i%cols+.5)*cellW-cw/2,gy:top+(Math.floor(i/cols)+.5)*cellH-ch/2};
 });
 render();
}
function render(){
 const nextMode=motion.matches||progress>=.94?'grid':homeProgress<.63?'intro':progress<=.03?'free':'sorting';
 if(nextMode!==mode){
  if(drag){drag.card.classList.remove('is-dragging');if(drag.card.hasPointerCapture(drag.id))drag.card.releasePointerCapture(drag.id);drag=null;suppressClickUntil=performance.now()+350}
  mode=nextMode;
 }
 cards.forEach((card,i)=>{
  card.disabled=mode==='sorting'||mode==='intro';card.style.opacity='1';
  if(mode==='grid'){card.style.zIndex=String(i+10);card.setAttribute('aria-label',`Apri il book fotografico: ${stories[i].place}`)}
  else card.setAttribute('aria-label',`Stampa fotografica: ${stories[i].place}. Trascina per spostarla`);
 });
 positions.forEach((pos,i)=>{
  const m=motion.matches?1:ease((progress-.08-(i%3)*.035)/.75);
  // Sequential near-camera passes: one print recedes before the next enters.
  const t=motion.matches?1:clamp((homeProgress-.12-i*.085)/.075,0,1);
  const depth=ease(t),launchAngle=Math.abs(pos.rotation+(i%2?9:-11))*Math.PI/180;
  // Keep the whole frame comfortably inside the viewport, including its rotation.
  const launchWidth=geom.cw*Math.cos(launchAngle)+geom.ch*Math.sin(launchAngle);
  const launchHeight=geom.ch*Math.cos(launchAngle)+geom.cw*Math.sin(launchAngle);
  const startScale=Math.min(2.2,geom.w*.80/launchWidth,geom.h*.80/launchHeight);
  const size=1/mix(1/startScale,1,depth);
  const cameraX=geom.w*.5-geom.cw/2,cameraY=geom.h*.5-geom.ch/2;
  const x=mix(mix(cameraX,pos.x,depth),pos.gx,m);
  const y=mix(mix(cameraY,pos.y,depth),pos.gy,m)+(motion.matches?geom.h:0);
  const turn=mix(pos.rotation+(i%2?9:-11),pos.rotation,depth)+Math.sin(t*Math.PI*2)*(1-t)*2;
  const entry=motion.matches||t>=1?'settled':t>0?'flying':'waiting';
  cards[i].style.setProperty('--contact-shadow',String(motion.matches?1:ease((t-.65)/.35)));
  cards[i].dataset.entry=entry;
  cards[i].style.visibility=entry==='waiting'?'hidden':'visible';
  if(mode==='intro')cards[i].style.zIndex=String(entry==='flying'?50+i:10+i);
  cards[i].style.transform=`translate3d(${x}px,${y}px,0) rotate(${turn*(1-m)}deg) scale(${size})`;
 });
 gridHint.setAttribute('aria-hidden',String(mode!=='grid'));
 stage.dataset.mode=mode;stage.dataset.progress=progress.toFixed(3);
}
let drag=null,suppressClickUntil=0;
function clampPosition(pos,x,y){
 const rad=Math.abs(pos.rotation)*Math.PI/180,bw=geom.cw*Math.cos(rad)+geom.ch*Math.sin(rad),bh=geom.ch*Math.cos(rad)+geom.cw*Math.sin(rad),dx=(bw-geom.cw)/2,dy=(bh-geom.ch)/2;
 pos.x=clamp(x,dx+5,geom.w-geom.cw-dx-5);pos.y=clamp(y,geom.top+dy+4,geom.h-geom.bottom-geom.ch-dy-4);
}
cards.forEach((card,i)=>{
 card.addEventListener('pointerdown',e=>{
  card.style.zIndex=String(++stack);card.focus({preventScroll:true});
  drag={id:e.pointerId,card,i,startX:e.clientX,startY:e.clientY,x:positions[i].x,y:positions[i].y,moved:false};card.setPointerCapture(e.pointerId);
 });
 card.addEventListener('pointermove',e=>{
  if(!drag||drag.card!==card||drag.id!==e.pointerId)return;
  const dx=e.clientX-drag.startX,dy=e.clientY-drag.startY;if(!drag.moved&&Math.hypot(dx,dy)<8)return;
  drag.moved=true;card.classList.add('is-dragging');e.preventDefault();clampPosition(positions[i],drag.x+dx,drag.y+dy);render();
 });
 function endDrag(e){if(!drag||drag.card!==card||drag.id!==e.pointerId)return;if(drag.moved||e.type==='pointercancel')suppressClickUntil=performance.now()+350;card.classList.remove('is-dragging');if(card.hasPointerCapture(e.pointerId))card.releasePointerCapture(e.pointerId);drag=null}
 card.addEventListener('pointerup',endDrag);card.addEventListener('pointercancel',endDrag);
 card.addEventListener('click',e=>{if(e.detail>0&&performance.now()<suppressClickUntil)return;if(mode==='grid')openBook(i)});
 card.addEventListener('focus',()=>card.style.zIndex=String(++stack));
});
const book=document.createElement('dialog');book.className='book-dialog';book.setAttribute('aria-label','Book fotografico');
book.innerHTML='<header class="book-header"><div class="book-meta"></div><button type="button">Torna alle storie</button></header><div class="book-grid"></div>';
document.body.append(book);const bookGrid=book.querySelector('.book-grid'),bookMeta=book.querySelector('.book-meta'),bookClose=book.querySelector('button');
let bookToken=0,bookPhotos=[],bookOverflow='',bookSource=null;
function layoutBook(){
 if(!book.open||!bookPhotos.length)return;
 const width=bookGrid.clientWidth,gap=width<650?9:14,target=width<650?160:225,maxHeight=width<650?230:270,maxItems=width<650?2:4;
 bookGrid.replaceChildren();
 let group=[],sum=0;
 function flush(last=false){
  if(!group.length)return;
  const height=Math.min(last?target:maxHeight,(width-gap*(group.length-1))/sum),row=document.createElement('div');row.className='book-row';
  group.forEach(img=>{const figure=document.createElement('figure');figure.className='book-photo';figure.style.width=(height*img.naturalWidth/img.naturalHeight)+'px';figure.style.height=height+'px';figure.append(img);row.append(figure)});
  bookGrid.append(row);group=[];sum=0;
 }
 bookPhotos.forEach(img=>{
  const ratio=img.naturalWidth/img.naturalHeight;
  if(group.length&&sum*target+ratio*target+gap*group.length>width){
   const before=Math.abs((width-gap*(group.length-1))/sum-target),after=Math.abs((width-gap*group.length)/(sum+ratio)-target);
   if(before<after)flush();
  }
  group.push(img);sum+=ratio;
  if(group.length>=maxItems||sum*target+gap*(group.length-1)>=width)flush();
 });flush(true);
}
async function openBook(index){
 const story=stories[index],token=++bookToken;bookSource=cards[index];bookPhotos=[];bookGrid.replaceChildren();
 bookMeta.innerHTML=`${story.place}<small>Book dimostrativo · luogo e associazione delle foto da confermare</small>`;
 if(!book.open){bookOverflow=document.documentElement.style.overflow;document.documentElement.style.overflow='hidden';book.showModal()}
 book.scrollTop=0;bookClose.focus({preventScroll:true});
 if(!motion.matches)book.animate([{opacity:0,transform:'translate3d(0,12px,0)'},{opacity:1,transform:'none'}],{duration:350,easing:'cubic-bezier(.22,1,.36,1)'});
 const loaded=await Promise.all(story.photos.map(file=>new Promise(resolve=>{const img=new Image();img.alt='Fotografia dell’archivio di Nicola Capasso';img.decoding='async';img.onload=()=>resolve(img);img.onerror=()=>resolve(null);img.src=asset(file)})));
 if(token!==bookToken||!book.open)return;
 bookPhotos=loaded.filter(Boolean);layoutBook();
}
function closeBook(){
 if(!book.open)return;
 ++bookToken;book.close();document.documentElement.style.overflow=bookOverflow;
 if(bookSource&&bookSource.isConnected)bookSource.focus({preventScroll:true});
}
bookClose.addEventListener('click',closeBook);book.addEventListener('cancel',e=>{e.preventDefault();closeBook()});book.addEventListener('keydown',e=>{if(e.key==='Tab'){e.preventDefault();bookClose.focus()}});
addEventListener('resize',layoutBook);
window.portfolioPrototype={stories,cards,get positions(){return positions},get mode(){return mode},get geometry(){return geom},measure};
addEventListener('homeprogress',e=>{homeProgress=e.detail;progress=motion.matches?1:clamp((homeProgress-.72)/.24,0,1);render()});
motion.addEventListener('change',()=>{measure();progress=motion.matches?1:clamp((homeProgress-.72)/.24,0,1);render()});
addEventListener('resize',measure);
measure();document.fonts.ready.then(measure);
})();
