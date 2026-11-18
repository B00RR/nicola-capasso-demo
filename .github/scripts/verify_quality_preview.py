"""Exercise the isolated comparison locally or against its deployed URL."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import os, sys
from playwright.sync_api import sync_playwright, expect

root = Path(__file__).resolve().parents[2]
server = None
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(root/'public')))
    Thread(target=server.serve_forever, daemon=True).start()
    url = f'http://127.0.0.1:{server.server_port}/prova-qualita/'
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(**({'channel':'chrome'} if os.name == 'nt' else {}))
        for width, height in [(390, 844), (1440, 900)]:
            page = browser.new_page(viewport={'width':width,'height':height}, has_touch=width < 500)
            requests = set()
            page.on('request', lambda r: requests.add(r.url.split('?')[0].split('/')[-1]) if '.webp' in r.url else None)
            assert page.goto(url).status == 200
            assert not requests
            for i in range(3):
                opener = page.locator('main button').nth(i)
                opener.tap() if width < 500 else opener.click()
                expect(page.locator('#after')).to_have_attribute('aria-pressed','true')
                photo = page.locator('#photo')
                assert photo.evaluate('async x=>{await x.decode();return x.naturalHeight}') == 2880
                assert requests == {f'{j:02}.webp' for j in range(1, i+2)}
                page.locator('#zoom').click()
                page.locator('#before').click()
                expect(page.locator('#before')).to_have_attribute('aria-pressed','true')
                assert photo.evaluate('async x=>{await x.decode();return x.naturalHeight}') == 1920
                page.locator('#after').click()
                expect(page.locator('#after')).to_have_attribute('aria-pressed','true')
                page.get_by_text('Chiudi', exact=True).click()
                expect(opener).to_be_focused()
            page.close()
        browser.close()
    print('PASS: 3 photos x 2 viewports; HD only on open, actual dimensions, comparison, zoom and close.')
finally:
    if server: server.shutdown(); server.server_close()
