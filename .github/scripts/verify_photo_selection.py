"""Assert the approved static demo selection, before and after application."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'public'
class Images(HTMLParser):
 def __init__(self):super().__init__();self.images=[]
 def handle_starttag(self,tag,attrs):
  if tag=='img':self.images.append(dict(attrs))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def imgs(text):
 p=Images();p.feed(text);return p.images
manifest=ROOT/'docs/FOTO-DEFINITIVE.json'
assert manifest.is_file(),'Missing approved definitive-photo manifest'
d=json.loads(manifest.read_text(encoding='utf-8'))
assert len(d['stories'])==10
assert sum(len(s['photos']) for s in d['stories'])==187
assert len(d['animation'])==12
branding=json.loads((ROOT/'docs/LOGO-HERO.json').read_text(encoding='utf-8'))
assert sha(PUBLIC/branding['path'])==branding['sha256']
allowed=set(d['assets'])|{branding['path']}
assert all((PUBLIC/p).is_file() and sha(PUBLIC/p)==h for p,h in d['assets'].items())
assert {p.relative_to(PUBLIC).as_posix() for p in (PUBLIC/'assets').rglob('*') if p.is_file() and p.suffix.lower() in {'.jpg','.jpeg','.webp','.png','.svg'}}==allowed
for prefix in ('','en/'):
 for story in d['stories']:
  text=(PUBLIC/prefix/f'storia-{story["number"]:02d}.html').read_text(encoding='utf-8')
  assert '<dialog ' in text and 'class="lightbox-content"' in text,('Missing photo viewer',story['number'])
  cover=[i for i in imgs(text) if i.get('class')=='story-cover']
  assert len(cover)==1 and cover[0]['src']==('../' if prefix else '')+story['cover'],('Story cover mismatch',prefix,story['number'])
  album=re.search(r'<div class="album">(.*?)</div>',text,re.S)
  assert album,story['number']
  assert [i['src'] for i in imgs(album[1])]==[('../' if prefix else '')+p for p in story['photos']]
 for name in ('index.html','portfolio.html'):
  text=(PUBLIC/prefix/name).read_text(encoding='utf-8')
  for s in d['stories']:
   block=re.search(r'<a\b[^>]*href="storia-'+f'{s["number"]:02d}'+r'.html"[^>]*>.*?</a>',text,re.S)
   assert block and ('../' if prefix else '')+s['cover'] in block[0]
 home=(PUBLIC/prefix/'index.html').read_text(encoding='utf-8')
 opening=[i for i in imgs(home) if i.get('class')=='portrait']
 assert len(opening)==1 and opening[0]['src']==('../' if prefix else '')+d['hero']['path'],('Hero photograph mismatch',prefix)
 scene=[i for i in imgs(home) if i.get('class')=='scene-card']
 assert [i['src'] for i in scene]==[('../' if prefix else '')+p['path'] for p in d['animation']]
 assert ('../' if prefix else '')+d['portrait'] in re.search(r'<section class="about".*?</section>',home,re.S)[0]
 assert all('WhatsApp' not in i.get('src','') and '127.0.0.1' not in i.get('src','') for i in imgs(home))
for page in list(PUBLIC.rglob('*.html'))+list(PUBLIC.rglob('*.htm')):
 for i in imgs(page.read_text(encoding='utf-8')):
  if not i.get('src'):continue
  ref=i['src'].split('?')[0]
  target=(PUBLIC/ref.removeprefix('/nicola-capasso-demo/')) if ref.startswith('/nicola-capasso-demo/') else (page.parent/ref).resolve()
  assert target.is_file(),(page,ref)
  assert target.relative_to(PUBLIC).as_posix() in allowed,(page,ref)
print('PASS: exact 10 galleries/187 ordered photos, 10 covers, 12 original animation photos, About portrait, complete photo allowlist and bilingual references')
