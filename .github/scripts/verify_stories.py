"""Verify both languages against the approved six folders, covers and photo roster."""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'public'
rows=json.loads((ROOT/'docs/STORIE.json').read_text(encoding='utf-8'))
expected=[('AMALFI','Amalfi',20,'copertina.jpg'),('AMALFI 2','Amalfi',27,'copertina.jpg'),('LAKE COMO','Lake Como',21,'copertina.jpeg'),('POSITANO','Positano',29,'coperina.jpg'),('SCALA','Scala',12,'copertina.jpg'),('SCALA 2','Scala',18,'copertina.jpg')]
assert [r['number'] for r in rows]==list(range(1,7))
photos=[p for r in rows for p in r['photos']]
assert len(photos)==len({p['path'] for p in photos})==len({p['sha256'] for p in photos})==127
shared=json.loads((ROOT/'docs/FOTO-DEFINITIVE.json').read_text(encoding='utf-8'))['shared_story_assets']
assert {p.relative_to(PUBLIC).as_posix() for p in (PUBLIC/'assets/stories').rglob('*.jpg')}==({p['path'] for p in photos}|set(shared))
for p in photos:assert hashlib.sha256((PUBLIC/p['path']).read_bytes()).hexdigest()==p['sha256'],p['path']
for en in (False,True):
 folder=PUBLIC/'en' if en else PUBLIC; prefix='../' if en else ''
 names=[f'storia-{n:02d}.html' for n in range(1,7)]
 assert sorted(p.name for p in folder.glob('storia-*.html'))==names
 for j,(r,(source,title,count,cover)) in enumerate(zip(rows,expected,strict=True)):
  assert r['title_it']==r['title_en']==title and r['folder']==source
  assert [p['source'] for p in r['photos'] if p['path']==r['cover_path']]==[source+'/'+cover]
  assert all(p['source'].split('/')[0]==source for p in r['photos'])
  page=folder/names[j];s=page.read_text(encoding='utf-8')
  assert '<h1>'+title+'</h1>' in s and '<title>'+title+' — Nicola Capasso</title>' in s,page
  match=re.search('<main.*?</main>',s,re.S);assert match,page
  main=match[0];assert not re.search(r'<(?:h2|p)\b|class="story-copy"',main),page
  assert f'class="next" href="{names[(j+1)%6]}"' in main
  for lang,url in [('it',prefix+names[j]),('x-default',prefix+names[j]),('en',('' if en else 'en/')+names[j])]:assert f'hreflang="{lang}" href="{url}"' in s,page
  match=re.search(r'<div class="album">(.*?)</div>',s,re.S);assert match,page
  album=match[1]
  assert album.count('class="photo-button"')==count==r['count']==len(r['photos'])
  assert re.findall(r'<img[^>]*src="([^"]+)"',album)==[prefix+p['path'] for p in r['photos']],page
 for page in (folder/'index.html',folder/'portfolio.html',PUBLIC/'anteprima-testi'/('en' if en else '')/'index.htm'):
  preview=page.suffix=='.htm'; pic='/nicola-capasso-demo/' if preview else prefix; links=('/nicola-capasso-demo/'+('en/' if en else '')) if preview else ''
  s=page.read_text(encoding='utf-8');cls='story-card' if page.name=='portfolio.html' else 'project reveal'
  assert s.count('class="'+cls+'"')==6
  cards=re.findall(r'<a\b[^>]*href="([^"]*storia-\d+\.html)"[^>]*>.*?</a>',s,re.S);assert cards==[links+n for n in names],page
  for name,r in zip(names,rows):
   match=re.search(r'<a\b[^>]*href="'+re.escape(links+name)+r'"[^>]*>.*?</a>',s,re.S);assert match,(page,name)
   block=match[0]
   assert f'src="{pic+r["cover_path"]}"' in block and f'aria-label="{r["title_it"]}"' in block,(page,name)
print('PASS: 6 approved IT/EN titles, 127 ordered photographs, exact covers on six indexes, reciprocal language routes and next-story cycle')
