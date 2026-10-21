"""Verify exact approved IT/EN stories and complete local photo series."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'public'
rows=json.loads((ROOT/'docs/STORIE.json').read_text(encoding='utf-8'))
assert len(rows)==10 and [r['number'] for r in rows]==list(range(1,11))
photos=[p for r in rows for p in r['photos']]
assert len(photos)==187 and len({p['path'] for p in photos})==187
assert {p.relative_to(PUBLIC).as_posix() for p in (PUBLIC/'assets/stories').rglob('*.jpg')}==({p['path'] for p in photos}|{r['cover_path'] for r in rows})
for p in photos:assert hashlib.sha256((PUBLIC/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
for prefix in ['', 'en/']:
 for r in rows:
  page=PUBLIC/prefix/f'storia-{r["number"]:02d}.html';s=page.read_text(encoding='utf-8');title=r['title_en' if prefix else 'title_it']
  assert '<h1>'+title+'</h1>' in s and '<title>'+title+' — Nicola Capasso</title>' in s,page
  match=re.search(r'<div class="album">(.*?)</div>',s,re.S)
  assert match is not None,page
  album=match.group(1)
  assert album.count('class="photo-button"')==r['count']==len(r['photos'])
  assert re.findall(r'<img[^>]*src="([^"]+)"',album)==[('../' if prefix else '')+p['path'] for p in r['photos']],page
 for name,cls in [('index.html','project reveal'),('portfolio.html','story-card')]:
  s=(PUBLIC/prefix/name).read_text(encoding='utf-8');assert s.count('class="'+cls+'"')==10
  for i in range(1,11):
   match=re.search(r'<a\b[^>]*href="storia-'+f'{i:02d}'+r'.html"[^>]*>.*?</a>',s,re.S)
   assert match is not None,(prefix,name,i)
   block=match.group(0)
   r=rows[i-1];assert r['cover_path'] in block;assert r['title_en' if prefix else 'title_it'] in block
print('PASS: 10 exact IT/EN story title pairs; all 187 selected photos in numeric order; matching covers on all cards')
