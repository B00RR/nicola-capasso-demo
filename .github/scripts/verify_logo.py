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
print('PASS: approved signature plus original line, versioned accessible IT/EN SVG, no raster/font/external resource; existing geometry and photo retained')
