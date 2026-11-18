"""Approved vector logo, preserving both homepages' existing image geometry."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];PUBLIC=ROOT/'public'
class Tags(HTMLParser):
    def __init__(self):super().__init__();self.images=[];self.in_h1=False;self.names=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='h1':self.in_h1=True
        if tag=='img':self.images.append(a)
    def handle_endtag(self,tag):
        if tag=='h1':self.in_h1=False
    def handle_data(self,data):
        if self.in_h1 and data.strip():self.names.append(data.strip())
meta=json.loads((ROOT/'docs/LOGO-HERO.json').read_text(encoding='utf-8'))
assert meta['path']=='assets/branding/nicola-capasso-logo.svg','Approved vector logo required'
raw=(PUBLIC/meta['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==meta['sha256']
svg=ET.fromstring(raw);assert svg.tag=='{http://www.w3.org/2000/svg}svg'
assert [int(svg.attrib[k]) for k in ('width','height')]==meta['size']==[979,250]
assert list(map(int,svg.attrib['viewBox'].split()))==meta['viewBox']==[32,32,3916,1000]
paths=[x for x in svg.iter() if x.tag.rsplit('}',1)[-1]=='path'];assert len(paths)==12 and any('C' in x.get('d','') for x in paths),'Approved signature plus restored line required'
line=svg.find(".//*[@id='linea-originale']");assert line is not None and len(list(line))==1 and list(line)[0].tag.rsplit('}',1)[-1]=='path'
assert meta['cache_version']=='firma-linea1'
assert not any(x.tag.rsplit('}',1)[-1] in ('image','text','script','foreignObject') for x in svg.iter())
assert not any('href' in k for x in svg.iter() for k in x.attrib)
for prefix in ['','en/']:
    page=PUBLIC/prefix/'index.html';p=Tags();p.feed(page.read_text(encoding='utf-8'));logos=[x for x in p.images if x.get('class')=='hero-logo']
    assert len(logos)==1,(prefix,'Missing hero logo')
    assert logos[0]['src']==('../' if prefix else '')+meta['path']+'?v='+meta['cache_version'] and [int(logos[0][k]) for k in ('width','height')]==meta['size']
    assert logos[0]['alt']=='Nicola Capasso' and not p.names,(prefix,'Accessible logo replaces visible wordmark')
    assert len([x for x in p.images if x.get('class')=='portrait'])==1

for page in PUBLIC.rglob('*.html'):
    if page.relative_to(PUBLIC).as_posix() not in ['index.html','en/index.html']:assert 'hero-logo' not in page.read_text(encoding='utf-8'),page
assert not (PUBLIC/'assets/branding/nicola-capasso-logo.png').exists()
# The transparent SVG box alone cannot tell whether the visible signature is wider.
import base64,os
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    browser=pw.chromium.launch(**({'executable_path':os.environ['BROWSER_PATH']} if os.environ.get('BROWSER_PATH') else {}))
    page=browser.new_page()
    ink=page.evaluate('''async src => {
      const i=new Image();i.src=src;await i.decode();const c=document.createElement('canvas');
      c.width=i.width;c.height=i.height;const ctx=c.getContext('2d');ctx.drawImage(i,0,0);
      const px=ctx.getImageData(0,0,c.width,c.height).data;let lo=c.width,hi=-1;
      for(let n=3;n<px.length;n+=4)if(px[n]>32){const x=(n>>2)%c.width;lo=Math.min(lo,x);hi=Math.max(hi,x)}
      return (hi-lo+1)/c.width;
    }''','data:image/svg+xml;base64,'+base64.b64encode(raw).decode())
    # Measured before the revision: mobile signature width or desktop photo height.
    for lang in ('','en'):
        for w,h,baseline in [(320,568,243.19),(360,740,273.59),(390,844,296.39),(768,1024,680),(1280,600,380),(1366,768,548),(1440,900,680)]:
            page.set_viewport_size(dict(width=w,height=h));page.goto((PUBLIC/lang/'index.html').as_uri())
            sig,car=page.evaluate('''async () => Promise.all(['.hero-logo','.portrait'].map(async s=>{
              const i=document.querySelector(s);await i.decode();const r=i.getBoundingClientRect();
              return [r.x,r.y,r.width,r.height,i.naturalWidth/i.naturalHeight];}))''')
            visible=min(sig[2],sig[3]*sig[4])*ink
            assert sig[1]>=0 and sig[1]+sig[3]<=car[1] and abs(car[2]-car[3]*car[4])<1,(lang,w,sig,car)
            assert all(abs(2*r[0]+r[2]-w)<1 for r in (sig,car)) and 1.01<visible/car[2]<1.10,(lang,w,visible,car)
            assert abs((visible if w<=700 else car[3])-baseline)<1,(lang,w,baseline)
    browser.close()
print('PASS: approved vector signature and car proportions on 14 IT/EN viewports; mobile ink and desktop photograph retain baseline sizes')
