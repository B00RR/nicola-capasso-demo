"""Static Pages contact preview: no PHP/email; mobile/desktop photograph selection."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright
PUBLIC=Path(__file__).resolve().parents[2]/'public'
with sync_playwright() as p:
 options={'headless':True}
 if os.environ.get('BROWSER_PATH'):options['executable_path']=os.environ['BROWSER_PATH']
 b=p.chromium.launch(**options)
 for w,h in [(320,800),(390,844),(430,932),(844,390),(1440,900)]:
  page=b.new_page(viewport={'width':w,'height':h},offline=True)
  page.goto((PUBLIC/'contatti.html').as_uri());page.evaluate('document.fonts.ready')
  assert page.locator('.contatti-nav a').count()==1
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  selector='.foto-mobile img' if w<=900 else '.foto-arco img'
  assert page.locator(selector).count()==(1 if w<=900 else 3)
  assert page.locator(selector).evaluate_all('es=>es.every(e=>e.checkVisibility()&&e.complete&&e.naturalWidth>0)')
  assert not page.locator('.foto-arco' if w<=900 else '.foto-mobile').first.is_visible()
  page.locator('button[type=submit]').click();assert page.locator('#errore-email').is_visible()
  for n,v in {'names':'Prova','email':'test@example.invalid','message':'x'}.items():page.locator('[name='+n+']').fill(v)
  page.locator('button[type=submit]').click();page.wait_for_function("!document.querySelector('button[type=submit]').disabled")
  assert 'non è stata spedita' in page.locator('#contatti-esito').inner_text()
  assert page.locator('[name=message]').input_value()=='x'
  page.close()
 b.close()
print('PASS: contact static preview, 5 viewport, photo crops, validation, no fake email success')
