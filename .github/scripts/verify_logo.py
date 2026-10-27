"""Logo supplied by the owner, on both homepages only."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,struct
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
for prefix in ['','en/']:
    page=PUBLIC/prefix/'index.html';p=Tags();p.feed(page.read_text(encoding='utf-8'));logos=[x for x in p.images if x.get('class')=='hero-logo']
    assert len(logos)==1,(prefix,'Missing hero logo')
    assert logos[0]['alt']=='Nicola Capasso' and not p.names,(prefix,'Accessible logo replaces visible wordmark')
    assert len([x for x in p.images if x.get('class')=='portrait'])==1
meta=json.loads((ROOT/'docs/LOGO-HERO.json').read_text(encoding='utf-8'))
raw=(PUBLIC/meta['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==meta['sha256'];assert raw.startswith(b'\x89PNG\r\n\x1a\n') and raw[25]==6,'RGBA PNG required'
assert list(struct.unpack('>II',raw[16:24]))==meta['size']
for page in PUBLIC.rglob('*.html'):
    if page.relative_to(PUBLIC).as_posix() not in ['index.html','en/index.html']:assert 'hero-logo' not in page.read_text(encoding='utf-8'),page
print('PASS: exact transparent PNG, accessible logo on IT/EN homepage only, no visible old wordmark, original photo retained')
