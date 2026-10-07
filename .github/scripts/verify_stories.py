"""Verify exact approved IT/EN stories and complete local photo series."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'public'
rows=json.loads((ROOT/'docs/STORIE.json').read_text(encoding='utf-8'))
assert len(rows)==7 and [r['number'] for r in rows]==list(range(1,8))
photos=[p for r in rows for p in r['photos']]
assert len(photos)==254 and len({p['path'] for p in photos})==254
assert {p.relative_to(PUBLIC).as_posix() for p in (PUBLIC/'assets/stories').rglob('*.jpg')}=={p['path'] for p in photos}
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
 for i in [8,9,10]:
  s=(PUBLIC/prefix/f'storia-{i:02d}.html').read_text(encoding='utf-8');assert '<img' not in s and '<div class="album">' not in s;assert '<h1>' in s
 for name,cls in [('index.html','project reveal'),('portfolio.html','story-card')]:
  s=(PUBLIC/prefix/name).read_text(encoding='utf-8');assert s.count('class="'+cls+'"')==10
  for i in range(1,11):
   match=re.search(r'<a\b[^>]*href="storia-'+f'{i:02d}'+r'.html"[^>]*>.*?</a>',s,re.S)
   assert match is not None,(prefix,name,i)
   block=match.group(0)
   if i<=7:
    r=rows[i-1];assert 'assets/stories/'+r['folder']+'/'+r['cover'] in block;assert r['title_en' if prefix else 'title_it'] in block
   else:assert '<img' not in block,(prefix,name,i)
print('PASS: 7 exact IT/EN story title pairs; all 254 photos verified and in both albums; matching covers; stories 08–10 and their cards without photos')
