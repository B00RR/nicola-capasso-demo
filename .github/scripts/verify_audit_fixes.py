from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlsplit,unquote
import json,os,sys
from typing import Any
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];PUBLIC=ROOT/'public'
class Handler(SimpleHTTPRequestHandler):
 def translate_path(self,path):return str(PUBLIC/unquote(urlsplit(path).path).removeprefix('/nicola-capasso-demo/').lstrip('/'))
 def log_message(self,format,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);Thread(target=server.serve_forever,daemon=True).start();url=f'http://127.0.0.1:{server.server_port}/nicola-capasso-demo/'
records=[]
try:
 with sync_playwright() as pw:
  opts: dict[str,Any]={'headless':True}
  if os.environ.get('BROWSER_PATH'):opts['executable_path']=os.environ['BROWSER_PATH']
  elif sys.platform=='win32':opts['executable_path']='C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
  browser=pw.chromium.launch(**opts)
  for prefix in ('','en/'):
   for enabled in (True,False):
    page=browser.new_page(java_script_enabled=enabled,viewport={'width':390,'height':844});page.goto(url+prefix+'index.html');page.evaluate('document.fonts.ready');page.locator('#sguardo').scroll_into_view_if_needed();page.wait_for_timeout(1100)
    for selector in ('#sguardo > div','#sguardo > img'):
     assert page.locator(selector).evaluate('e=>getComputedStyle(e).opacity')=='1'
    fonts=page.evaluate('[...document.fonts].filter(f=>f.status==="loaded").map(f=>f.family.replace(/[\x22\x27]/g,""))');assert set(fonts)=={'Italiana','Space Grotesk'},fonts
    for n in (8,9,10):
     link=page.locator(f'a.project[href="storia-{n:02}.html"]');assert link.get_attribute('aria-label');assert link.locator('img').count()==0
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    records.append({'language':prefix or 'it','javascript':enabled,'contents_visible':True,'local_fonts_loaded':fonts,'anonymous_story_links':0});page.close()
   for width in (390,1440):
    routes=[];page=browser.new_page(viewport={'width':width,'height':900},reduced_motion='reduce');page.route('**/assets/optimized/NCF00205.jpg',lambda r:routes.append(r));page.goto(url+prefix+'index.html',wait_until='domcontentloaded');page.evaluate('document.fonts.ready');page.evaluate('scrollTo(0,document.body.scrollHeight)')
    for _ in range(60):
     if routes:break
     page.wait_for_timeout(50)
    assert routes
    expression='e=>({height:e.querySelector("img").getBoundingClientRect().height,ctaY:e.querySelector(".cta").getBoundingClientRect().top+scrollY})'
    before=page.locator('#sguardo').evaluate(expression);assert before['height']>0
    routes[0].fulfill(status=200,content_type='image/jpeg',body=(PUBLIC/'assets/optimized/NCF00205.jpg').read_bytes());page.wait_for_function('document.querySelector("#sguardo img").naturalWidth>0');page.wait_for_timeout(100);after=page.locator('#sguardo').evaluate(expression)
    assert abs(before['height']-after['height'])<.1,(before,after);assert abs(before['ctaY']-after['ctaY'])<.1,(before,after)
    records.append({'language':prefix or 'it','width':width,'delayed_image_before':before,'delayed_image_after':after});page.close()
  # The main script fails before initializing reveal: readable fallback must remain.
  page=browser.new_page(viewport={'width':390,'height':844});page.add_init_script('window.IntersectionObserver=undefined');page.goto(url+'index.html');page.locator('#sguardo').scroll_into_view_if_needed();assert page.locator('#sguardo > div').evaluate('e=>getComputedStyle(e).opacity')=='1';page.close()
  for dpr in (1,2,3):
   page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=dpr);page.goto(url+'index.html');sources=page.locator('.scene-card').evaluate_all('es=>es.map(e=>({source:e.getAttribute("src"),selected:new URL(e.currentSrc).pathname}))');assert len(sources)==12 and all('/assets/animation/' in x['selected'] for x in sources)
   paths=set(x['selected'].removeprefix('/nicola-capasso-demo/') for x in sources);total=sum((PUBLIC/p).stat().st_size for p in paths);records.append({'dpr':dpr,'selected_animation_bytes':total,'sources':sources});page.close()
  browser.close()
finally:
 server.shutdown();server.server_close()
if os.environ.get('AUDIT_RESULTS'):
 Path(os.environ['AUDIT_RESULTS']).write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: IT/EN no-JS contents and fonts; accessible empty story links; delayed about image stable at390/1440; script-error fallback; responsive selection DPR1/2/3')
print(json.dumps([r for r in records if 'selected_animation_bytes' in r],ensure_ascii=False,indent=2))
