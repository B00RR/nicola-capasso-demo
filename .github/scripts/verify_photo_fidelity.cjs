/* Photo pixels must not be tinted or made translucent by CSS/JS. */
const fs=require('node:fs'),path=require('node:path'),http=require('node:http'),assert=require('node:assert/strict');
const {chromium}=require(process.argv[2]||'playwright');
const ROOT=path.resolve(__dirname,'../..'),PUBLIC=path.join(ROOT,'public'),OUT=path.resolve(process.argv[3]||path.join(process.env.TMPDIR||process.env.RUNNER_TEMP||ROOT,'photo-fidelity-proof'));
fs.mkdirSync(OUT,{recursive:true});const log=path.join(OUT,'measurements.jsonl');fs.writeFileSync(log,'');
function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);}
const pages=walk(PUBLIC).filter(p=>/\.html?$/.test(p)).map(p=>path.relative(PUBLIC,p).split(path.sep).join('/')).sort();assert.equal(pages.length,36);

const types={'.html':'text/html','.htm':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.jpg':'image/jpeg','.jpeg':'image/jpeg','.png':'image/png','.webp':'image/webp','.ttf':'font/ttf','.woff2':'font/woff2'};
const server=http.createServer((req,res)=>{let p;try{let u=decodeURIComponent(new URL(req.url,'http://localhost').pathname);u=u.replace(/^\/nicola-capasso-demo\//,'/');p=path.resolve(PUBLIC,'.'+u);if(p!==PUBLIC&&!p.startsWith(PUBLIC+path.sep))throw Error('outside fixture');if(fs.statSync(p).isDirectory())p=path.join(p,'index.html');const data=fs.readFileSync(p);res.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream','Cache-Control':'no-store'});res.end(data);}catch{res.writeHead(404);res.end('not found');}});
const rows=[],failures=[],slots=new Set(),visited=new Set(),sources=new Set();let browser;
for(const file of pages)for(const ref of fs.readFileSync(path.join(PUBLIC,file),'utf8').matchAll(/href="([^"]*styles\/(?:portfolio|stories)\.css[^"]*)"/g))if(!ref[1].endsWith('?v=foto-originali1'))failures.push({page:file,issue:'Photo stylesheet cache version missing'});
async function ready(page,file,viewport){
  await page.evaluate(()=>[...document.images].forEach(i=>{i.loading='eager'}));
  await page.waitForFunction(()=>[...document.images].filter(i=>i.getAttribute('src')).every(i=>i.complete&&i.naturalWidth>0));
  const loaded=await page.evaluate(async()=>{
    await window.typographyReady;await document.fonts.ready;
    return [...document.images].filter(i=>i.getAttribute('src')).map(i=>i.currentSrc);
  });
  for(const src of loaded)sources.add(src);
  await page.waitForFunction(()=>typeof frameId==='undefined'||frameId===0);
}
async function inspect(page,file,viewport,state){
  const result=await page.evaluate(()=>[...document.images].filter(i=>i.getAttribute('src')&&!i.classList.contains('hero-logo')).map((img,index)=>{
    const bad=[],transforms=[];
    for(let e=img;e;e=e.parentElement){
      const s=getComputedStyle(e),name=e.tagName+'.'+e.className;transforms.push(s.transform);
      if(s.filter!=='none')bad.push(name+' filter:'+s.filter);
      if(s.mixBlendMode!=='normal')bad.push(name+' blend:'+s.mixBlendMode);
      if(Number(s.opacity)!==1)bad.push(name+' opacity:'+s.opacity);
      if(s.backdropFilter!=='none')bad.push(name+' backdrop:'+s.backdropFilter);
      if(s.boxShadow!=='none')bad.push(name+' shadow:'+s.boxShadow);
      for(const k of ['::before','::after']){
        const z=getComputedStyle(e,k);
        if(z.display!=='none'&&z.visibility!=='hidden'&&z.content!=='none'&&z.content!=='normal'&&
          (z.backgroundImage!=='none'||!['rgba(0, 0, 0, 0)','transparent'].includes(z.backgroundColor)))
          bad.push(name+k+' overlay:'+z.backgroundColor+' '+z.backgroundImage);
      }
    }
    const s=getComputedStyle(img);
    return {index,src:img.getAttribute('src'),filter:s.filter,opacity:s.opacity,visibility:s.visibility,
      objectFit:s.objectFit,objectPosition:s.objectPosition,width:s.width,height:s.height,transforms,bad};
  }));
if(state==='hover'){const before=rows.findLast(r=>r.page===file&&r.viewport===viewport&&r.state==='base');for(const i of result)if(JSON.stringify(i.transforms)!==JSON.stringify(before.photos[i.index].transforms))i.bad.push('hover changes photo/ancestor transform');}
const r={page:file,viewport,state,photos:result};rows.push(r);fs.appendFileSync(log,JSON.stringify(r)+'\n');for(const i of result){slots.add(file+'|'+viewport+'|'+i.index+'|'+i.src);for(const issue of i.bad)failures.push({page:file,viewport,state,src:i.src,issue});}return result;}
(async()=>{await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const local='http://127.0.0.1:'+server.address().port+'/nicola-capasso-demo/',remote=process.argv[4],base=remote||local;
try{browser=await chromium.launch({headless:true});
for(const [width,height] of [[1440,900],[390,844]]){const context=await browser.newContext({viewport:{width,height},locale:'it-IT',isMobile:width<700,hasTouch:width<700});
for(const file of pages){const p=await context.newPage();p.on('pageerror',e=>failures.push({page:file,viewport:width,issue:'JS '+e.message}));const url=new URL(file,base);if(remote)url.searchParams.set('audit','photo-fidelity');await p.goto(url.href,{waitUntil:'domcontentloaded'});await ready(p,file,width);visited.add(file+'|'+width);await inspect(p,file,width,'base');
const cdp=await context.newCDPSession(p);await cdp.send('DOM.enable');await cdp.send('CSS.enable');const dom=await cdp.send('DOM.getDocument');const {nodeIds}=await cdp.send('DOM.querySelectorAll',{nodeId:dom.root.nodeId,selector:'img:not(.hero-logo),*:has(img:not(.hero-logo))'});for(let n=0;n<nodeIds.length;n+=50)await Promise.all(nodeIds.slice(n,n+50).map(nodeId=>cdp.send('CSS.forcePseudoState',{nodeId,forcedPseudoClasses:['hover']})));await p.waitForTimeout(100);await inspect(p,file,width,'hover');await cdp.detach();
if(await p.locator('.scene-card').count()){
  for(const progress of [0,.01,.02,.08,.14,.18,.19,.24,.34,.38,.14,0]){
    await p.evaluate(t=>{document.documentElement.style.scrollBehavior='auto';scrollTo(0,geometry.heroTop+t*geometry.range);return new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));},progress);
    await p.waitForFunction(()=>frameId===0&&Math.abs(displayProgress-progressAt(scrollY))*geometry.range<.1);
    await inspect(p,file,width,'scene:'+progress);
  }
  if(file==='index.html')await p.screenshot({path:path.join(OUT,'home-'+width+'.png')});
  await p.emulateMedia({reducedMotion:'reduce'});await p.reload({waitUntil:'domcontentloaded'});await ready(p,file,width);await inspect(p,file,width,'reduced-motion');
}
const opener=p.locator('.album .photo-button').first();if(await opener.count()){
  await opener.click();await p.locator('dialog[open] img').first().evaluate(i=>i.decode());await inspect(p,file,width,'viewer');
  await p.keyboard.press('ArrowRight');await p.locator('dialog[open] img').first().evaluate(i=>i.decode());await inspect(p,file,width,'viewer-next');
  await p.keyboard.press('Escape');await p.waitForFunction(()=>!document.querySelector('dialog').open&&document.body.style.overflow==='');assert.ok(await opener.evaluate(e=>e===document.activeElement),'Viewer focus restoration');
}
await p.close();}await context.close();}
// Decode every resource one at a time, outside the album's pinned-bitmap budget.
const decoder=await browser.newPage();await decoder.setContent('<img alt="">');
for(const src of sources){try{await decoder.locator('img').evaluate((i,url)=>{i.src=url;return i.decode()},src)}catch(e){failures.push({src,issue:'Image failed to decode: '+e.message})}}
await decoder.close();
assert.equal(visited.size,pages.length*2);const report={pages:pages.length,pageViewportCases:visited.size,photoSlots:slots.size,snapshots:rows.length,decodedResources:sources.size,failures:failures.length,issues:failures};fs.writeFileSync(path.join(OUT,'summary.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({...report,issues:failures.slice(0,12)}));assert.equal(failures.length,0,'Photographs have CSS/JS effects; see measurements.jsonl');
}finally{if(browser)await browser.close();server.closeAllConnections();await new Promise(resolve=>server.close(resolve));}})().catch(e=>{console.error(e);process.exitCode=1;});
