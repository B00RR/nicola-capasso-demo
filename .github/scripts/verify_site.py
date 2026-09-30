from pathlib import Path
import os,re,subprocess,tempfile
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];PUBLIC=ROOT/'public'
html=(PUBLIC/'index.html').read_text(encoding='utf-8')
assert '../assets/' not in html
script=(PUBLIC/'portfolio.js').read_text(encoding='utf-8')
assets=set(re.findall(r'assets/[^"\')]+',html));assets.update('assets/optimized/'+f for f in re.findall(r"'([^']+\.jpg)'",script))
assert len(assets)==14
for asset in assets:assert (PUBLIC/asset).is_file(),asset
subprocess.run(['node','--check',str(PUBLIC/'portfolio.js')],check=True)
with tempfile.TemporaryDirectory() as tmp:
 inline=Path(tmp)/'inline.js';inline.write_text(html.split('<script>')[1].split('</script>')[0],encoding='utf-8');subprocess.run(['node','--check',str(inline)],check=True)
with sync_playwright() as p:
 options={'headless':True}
 if os.environ.get('BROWSER_PATH'):options['executable_path']=os.environ['BROWSER_PATH']
 browser=p.chromium.launch(**options)
 for width,height in [(390,844),(1440,900),(844,390)]:
  page=browser.new_page(viewport={'width':width,'height':height});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((PUBLIC/'index.html').as_uri());page.wait_for_timeout(2500)
  assert page.locator('.portrait').evaluate('(e)=>e.complete&&e.naturalWidth>0')
  assert page.locator('.p-card').count()==6
  assert page.locator('.p-card img').evaluate_all('(es)=>es.every(e=>e.complete&&e.naturalWidth>0)')
  total=page.evaluate('document.querySelector(".hero").offsetHeight-innerHeight');page.evaluate('(y)=>scrollTo(0,y)',total*.96);page.wait_for_timeout(1300)
  assert page.locator('.p-stage').get_attribute('data-mode')=='grid'
  assert page.locator('.p-grid-hint').get_attribute('aria-hidden')=='false'
  for i in range(6):
   page.locator('.p-card').nth(i).click();page.wait_for_function('document.querySelectorAll(".book-photo img").length===8')
   assert page.locator('.book-photo img').evaluate_all('(es)=>es.every(e=>e.complete&&e.naturalWidth>0)')
   page.keyboard.press('Escape');assert page.locator('.book-dialog').evaluate('(e)=>!e.open')
  assert not errors,errors;page.close()
 browser.close()
print('PASS: 14 assets, syntax, 3 responsive viewports and all 18 book openings')
