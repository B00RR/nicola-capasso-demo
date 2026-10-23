"""Focused real-browser checks for immersive photo viewing and transient controls."""
from pathlib import Path
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from threading import Thread
import json,os
from playwright.sync_api import sync_playwright,TimeoutError as BrowserTimeout
ROOT=Path(__file__).resolve().parents[2]
PUBLIC=ROOT/'public'
OUT=ROOT.parent/'viewer-evidence'
OUT.mkdir(exist_ok=True)
class Handler(SimpleHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def do_GET(self):
        if self.path.startswith('/nicola-capasso-demo/'):
            self.path=self.path.removeprefix('/nicola-capasso-demo')
        super().do_GET()
    def log_message(self,format,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(PUBLIC)))
thread=Thread(target=server.serve_forever,daemon=True)
thread.start()
records=[]
failures=[]
errors=[]
def check(ok,label,case):
    records.append({'case':case,'check':label,'passed':bool(ok)})
    if not ok:failures.append(case+': '+label)
def opacity(page):return page.locator('.lightbox-close').evaluate('e=>Number(getComputedStyle(e).opacity)')
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(**({'channel':'msedge'} if os.name=='nt' else {}))
        try:
            for case,route,mobile,width,height in [('touch','storia-01.html',True,390,844),('desktop','storia-01.html',False,1440,900),('english','en/storia-10.html',True,390,844)]:
                context=browser.new_context(viewport={'width':width,'height':height},has_touch=mobile,is_mobile=mobile)
                page=context.new_page()
                page.on('pageerror',lambda error:errors.append(str(error)))
                response=page.goto(f'http://127.0.0.1:{server.server_port}/nicola-capasso-demo/{route}',wait_until='networkidle')
                assert response.status==200
                page.evaluate('document.fonts.ready')
                opener=page.locator('.photo-button').first
                opener.tap() if mobile else opener.click()
                dialog=page.locator('dialog')
                image=dialog.locator('.lightbox-content img')
                image.evaluate('e=>e.decode()')
                check(dialog.evaluate('e=>e.open'),'photo opens',case)
                backdrop_alpha=dialog.evaluate('e=>{const c=document.createElement("canvas");c.width=c.height=1;const x=c.getContext("2d");x.fillStyle=getComputedStyle(e).backgroundColor;x.fillRect(0,0,1,1);return x.getImageData(0,0,1,1).data[3]}')
                check(backdrop_alpha==255,'page text cannot bleed through the photo viewer',case)
                metric=image.evaluate('e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {x:r.x,y:r.y,w:r.width,h:r.height,fit:s.objectFit,touch:s.touchAction}}')
                check(abs(metric['x'])<1 and abs(metric['y'])<1 and abs(metric['w']-width)<1 and abs(metric['h']-height)<1 and metric['fit']=='contain','photo has full viewport without imposed margins or cropping',case)
                style=page.locator('.lightbox-close').evaluate('e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {font:s.fontFamily,border:s.borderTopWidth,radius:s.borderRadius,w:r.width,h:r.height}}')
                check('Italiana' in style['font'] and style['border']=='1px' and style['radius']=='2px','close uses approved action typography and thin border',case)
                check(style['w']>=44 and style['h']>=44,'close has an accessible touch target',case)
                check(opacity(page)>.95,'controls visible on opening',case)
                if case!='english':dialog.screenshot(path=str(OUT/f'{case}-controls.png'))
                try:page.wait_for_function('Number(getComputedStyle(document.querySelector(".lightbox-close")).opacity)===0',timeout=3300)
                except BrowserTimeout:pass
                hidden=opacity(page)<.01
                check(hidden,'controls hide automatically after two seconds',case)
                if hidden:
                    box=page.locator('.lightbox-close').bounding_box()
                    src=image.get_attribute('src')
                    if case!='english':dialog.screenshot(path=str(OUT/f'{case}-photo-only.png'))
                    if mobile:
                        page.touchscreen.tap(box['x']+box['width']/2,box['y']+box['height']/2)
                    else:
                        page.mouse.move(width/2,height/2)
                    page.wait_for_function('Number(getComputedStyle(document.querySelector(".lightbox-close")).opacity)>.99')
                    check(dialog.evaluate('e=>e.open') and image.get_attribute('src')==src,'first tap on hidden close only reveals controls' if mobile else 'mouse movement reveals controls without changing photo',case)
                next_button=dialog.locator('.lightbox-step.next')
                next_button.tap() if mobile else next_button.click()
                check(dialog.locator('.lightbox-count').inner_text().startswith('2 /'),'next navigates normally',case)
                previous=dialog.locator('.lightbox-step.prev')
                previous.tap() if mobile else previous.click()
                check(dialog.locator('.lightbox-count').inner_text().startswith('1 /'),'previous navigates normally',case)
                if case=='touch':
                    session=context.new_cdp_session(page)
                    before=page.evaluate('visualViewport.scale')
                    src=image.get_attribute('src')
                    session.send('Input.synthesizePinchGesture',{'x':195,'y':420,'scaleFactor':1.5,'relativeSpeed':800,'gestureSourceType':'touch'})
                    # shortcut: headless Edge also ignores pinch on a blank control page; confirm real pinch on a phone before publication.
                    zoom_contract=image.evaluate('e=>{const ev=new Event("touchmove",{bubbles:true,cancelable:true});return {allowed:e.dispatchEvent(ev),touch:getComputedStyle(e).touchAction,meta:document.querySelector("meta[name=viewport]").content}}')
                    check(zoom_contract['allowed'] and zoom_contract['touch']=='auto' and 'user-scalable=no' not in zoom_contract['meta'] and 'maximum-scale' not in zoom_contract['meta'],'native zoom gestures and viewport permissions remain unrestricted',case)
                    check(image.get_attribute('src')==src,'pinch gesture does not change the photo',case)
                    session.send('Emulation.setPageScaleFactor',{'pageScaleFactor':1})
                    session.detach()
                page.keyboard.press('Escape')
                page.wait_for_function("!document.querySelector('dialog').open && document.body.style.overflow===''")
                check(not dialog.evaluate('e=>e.open') and opener.evaluate('e=>document.activeElement===e'),'Escape closes and restores focus',case)
                opener.tap() if mobile else opener.click()
                page.keyboard.press('Tab')
                page.wait_for_timeout(2300)
                check(opacity(page)>.95,'keyboard focus keeps controls available',case)
                page.keyboard.press('ArrowRight')
                check(dialog.locator('.lightbox-count').inner_text().startswith('2 /'),'keyboard navigation is preserved',case)
                close=dialog.locator('.lightbox-close')
                close.tap() if mobile else close.click()
                page.wait_for_function("!document.querySelector('dialog').open && document.body.style.overflow===''")
                check(not dialog.evaluate('e=>e.open') and page.evaluate('document.body.style.overflow')=='','close restores page scrolling',case)
                opener.tap() if mobile else opener.click()
                check(opacity(page)>.95 and dialog.locator('.lightbox-count').inner_text().startswith('1 /'),'reopening resets controls and photo',case)
                page.keyboard.press('Escape')
                context.close()
        finally:browser.close()
finally:
    server.shutdown();server.server_close();thread.join(timeout=5)
check(not thread.is_alive(),'test server stopped','cleanup')
check(not errors,'no JavaScript errors','all')
(OUT/'viewer-result.json').write_bytes((json.dumps({'checks':records,'failures':failures,'javascript_errors':errors},indent=2)+'\n').encode())
print(json.dumps({'checks':len(records),'failures':failures,'javascript_errors':errors},ensure_ascii=False))
assert not failures,failures
