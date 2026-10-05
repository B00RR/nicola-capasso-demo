"""Exercise the shipped 404 over the GitHub Pages project prefix."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import unquote, urlsplit
import json
import os

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
PREFIX = "/nicola-capasso-demo/"
HTML = (PUBLIC / "404.html").read_bytes()
assert b'<base' not in HTML
assert b'href="/nicola-capasso-demo/index.html"' in HTML
assert b'src="/nicola-capasso-demo/assets/optimized/6.jpg"' in HTML
assert b'<meta name="robots" content="noindex,follow">' in HTML
assert b"../assets/" not in HTML


class PagesHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if not urlsplit(self.path).path.startswith(PREFIX):
            self.send_error(404)
            return
        self.path = self.path[len(PREFIX) - 1:]
        target = Path(self.translate_path(unquote(urlsplit(self.path).path)))
        if target.exists():
            super().do_GET()
            return
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(HTML)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(HTML)

    def log_message(self, format, *args):
        pass


def ready(page):
    page.evaluate("""async () => {
        await document.fonts.ready;
        await Promise.all([...document.images].map(i => i.decode()));
        await Promise.all(document.getAnimations().map(a => a.finished));
    }""")


server = ThreadingHTTPServer(("127.0.0.1", 0), partial(PagesHandler, directory=str(PUBLIC)))
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
base = f"http://127.0.0.1:{server.server_port}"
records = []
routes = []
try:
    with sync_playwright() as p:
        options: dict[str, object] = {"headless": True}
        if os.environ.get("BROWSER_PATH"):
            options["executable_path"] = os.environ["BROWSER_PATH"]
        browser = p.chromium.launch(**options)
        configs = (
            ("desktop", 1440, 900, False, False),
            ("narrow", 320, 640, True, False),
            ("mobile", 390, 844, True, False),
            ("landscape", 844, 390, True, False),
            ("reduced", 390, 844, True, True),
        )
        for name, width, height, touch, reduced in configs:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                has_touch=touch, is_mobile=touch,
                reduced_motion="reduce" if reduced else "no-preference",
            )
            page = context.new_page()
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            for path in ("pagina-inesistente", "album/storia-inesistente", "molto/profondo/nessuna-pagina?x=1"):
                response = page.goto(base + PREFIX + path)
                assert response.status == 404
                assert response.body() == HTML
                ready(page)
                assert page.locator('meta[name="robots"]').get_attribute("content") == "noindex,follow"
                assert page.locator("h1").inner_text() == "Fuori\ninquadratura."
                assert page.locator(".explanation").inner_text() == "La pagina che cercate non è qui.\nMa ci sono ancora tante storie da scoprire."
                text = page.locator("body").inner_text().lower()
                for removed in ("fotografie, emozioni, ricordi.", "le storie belle trovano sempre una strada.", "errore 404 · pagina non trovata", "nicola capasso"):
                    assert removed not in text
                metrics = page.evaluate("""() => ({
                    fonts:[...document.fonts].map(f => ({family:f.family,status:f.status})),
                    image:document.querySelector('img').naturalWidth,
                    imageUrl:document.querySelector('img').src,
                    overflow:document.documentElement.scrollWidth > innerWidth,
                    front:getComputedStyle(document.querySelector('.error-number')).zIndex,
                    color:getComputedStyle(document.querySelector('.error-number')).color,
                    motion:document.getAnimations().some(a=>a.playState==='running')
                })""")
                assert len(metrics["fonts"]) == 2 and all(f["status"] == "loaded" for f in metrics["fonts"])
                assert metrics["image"] == 1600
                assert metrics["imageUrl"] == base + PREFIX + "assets/optimized/6.jpg"
                assert not metrics["overflow"] and metrics["front"] == "2"
                assert metrics["color"] == "rgb(25, 25, 22)"
                if reduced:
                    assert not metrics["motion"]
                actions = page.locator(".error-action")
                assert actions.count() == 2
                for i, (label, target) in enumerate((("Hompage", "index.html"), ("Portfolio", "portfolio.html"))):
                    assert actions.nth(i).inner_text() == label
                    assert actions.nth(i).evaluate("e=>e.href") == base + PREFIX + target
                    box = actions.nth(i).bounding_box()
                    assert box["height"] >= 44 and box["width"] >= 44
                records.append({"configuration": name, "path": path, "status": 404, **metrics})
            if os.environ.get("VERIFY_SCREENSHOT_DIR"):
                out = Path(os.environ["VERIFY_SCREENSHOT_DIR"])
                out.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out / f"404-{name}.png"), full_page=True)
            # A real keyboard sequence verifies the skip link and fluid focus fill.
            page.goto(base + PREFIX + "404.html")
            ready(page)
            page.keyboard.press("Tab")
            assert page.evaluate("document.activeElement.className") == "skip"
            page.keyboard.press("Enter")
            assert page.evaluate("document.activeElement.id") == "contenuto"
            page.keyboard.press("Tab")
            ready(page)
            assert page.evaluate("document.activeElement.textContent") == "Hompage"
            assert page.evaluate("document.activeElement.matches(':focus-visible')")
            assert page.evaluate("getComputedStyle(document.activeElement).color") == "rgb(255, 255, 255)"
            assert page.evaluate("parseFloat(getComputedStyle(document.activeElement,':after').top)<0")
            for i, target in enumerate(("index.html", "portfolio.html")):
                page.goto(base + PREFIX + "qualcosa/non-esiste")
                ready(page)
                if touch:
                    page.locator(".error-action").nth(i).tap()
                else:
                    page.locator(".error-action").nth(i).click()
                page.wait_for_url(base + PREFIX + target)
                page.wait_for_load_state("networkidle")
                assert page.locator(".error-number").count() == 0
                routes.append({"configuration": name, "target": target})
            assert not errors, errors
            context.close()
        # Root-relative URLs and native font faces also work without page JavaScript.
        context = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        page = context.new_page()
        for i, target in enumerate(("index.html", "portfolio.html")):
            response = page.goto(base + PREFIX + "a/b/c/non-esiste")
            assert response.status == 404
            ready(page)
            assert page.locator("img").evaluate("i=>i.complete&&i.naturalWidth>0")
            assert page.evaluate("[...document.fonts].every(f=>f.status==='loaded')")
            page.locator(".error-action").nth(i).tap()
            page.wait_for_url(base + PREFIX + target)
            page.wait_for_load_state("networkidle")
            routes.append({"configuration": "no-JS", "target": target})
        context.close()
        browser.close()
finally:
    server.shutdown()
    server.server_close()
    thread.join()

assert len(records) == 15 and len(routes) == 12
print(f"PASS: custom 404; {len(records)} nested-path/viewport HTTP checks; {len(routes)} click/tap/no-JS routes; local fonts/photo; original copy, dark overlay, noindex; keyboard skip/focus fluid fill; reduced motion")
if os.environ.get("VERIFY_SCREENSHOT_DIR"):
    (Path(os.environ["VERIFY_SCREENSHOT_DIR"]) / "404-checks.json").write_text(json.dumps({"responses": records, "routes": routes}, indent=2), encoding="utf-8")
