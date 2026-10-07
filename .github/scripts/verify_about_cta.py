from pathlib import Path
import os,sys,json
from playwright.sync_api import sync_playwright
PUBLIC=Path(__file__).resolve().parents[2]/'public'
properties=['fontFamily','fontSize','fontWeight','lineHeight','borderTopWidth','borderTopColor','borderRadius','backgroundColor','padding','minHeight','letterSpacing']
expression='e=>Object.fromEntries('+json.dumps(properties)+'.map(k=>[k,getComputedStyle(e)[k]]))'
with sync_playwright() as pw:
 options={}
 if sys.platform=='win32':options['executable_path']='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
 browser=pw.chromium.launch(**options)
 for prefix in ['', 'en/']:
  for width in [390,700,701,1440]:
   page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');page.goto((PUBLIC/(prefix+'index.html')).as_uri());page.evaluate('document.fonts.ready')
   assert page.locator('section.contact').count()==0
   cta=page.locator('#sguardo #contatto');assert cta.count()==1 and cta.get_attribute('href')=='contatti.html';cta.scroll_into_view_if_needed();styles=cta.evaluate(expression)
   result=page.locator('#sguardo').evaluate('e=>{const photo=e.querySelector("img").getBoundingClientRect();return [...e.querySelectorAll("h2,p,.cta")].map(x=>({align:getComputedStyle(x).textAlign,offset:Math.abs(x.getBoundingClientRect().left+x.getBoundingClientRect().width/2-photo.left-photo.width/2)}))}')
   if width<=700:assert all(x['align']=='center' and x['offset']<1 for x in result),result
   else:assert page.locator('#sguardo > div').evaluate('e=>getComputedStyle(e).textAlign')!='center'
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert cta.evaluate('e=>getComputedStyle(e,"::before").content')=='""'
   page.goto((PUBLIC/(prefix+'portfolio.html')).as_uri());page.evaluate('document.fonts.ready');reference=page.locator('.portfolio-contact-link');reference.scroll_into_view_if_needed();expected=reference.evaluate(expression);assert styles==expected,(width,prefix,styles,expected);page.close()
 browser.close()
print('PASS: moved CTA IT/EN, shared Portfolio button appearance, mobile-only centered heading/paragraphs/CTA at390/700; desktop701/1440 unchanged; no overflow')
