from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import functools
import os
import re
import subprocess
import sys
import tempfile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
HTML_PATH = PUBLIC / "index.html"
html = HTML_PATH.read_text(encoding="utf-8")
style_match = re.search(r"<style>(.*?)</style>", html, re.S)
assert style_match is not None, "Missing inline stylesheet"
css = style_match.group(1)
assert css + "\n" + (PUBLIC / "mobile.css").read_text(encoding="utf-8") + "\n\n" + (PUBLIC / "azioni.css").read_text(encoding="utf-8") + "\n\n" + (PUBLIC / "azioni-mobile-fix.css").read_text(encoding="utf-8") == (PUBLIC / "stili-completi.css").read_text(encoding="utf-8")
PAGES = sorted(PUBLIC.rglob("*.html"))
for page_path in PAGES:
    depth = len(page_path.relative_to(PUBLIC).parts) - 1
    prefix = "../" * depth
    page_html = page_path.read_text(encoding="utf-8")
    if page_path.name == "404.html":
        assert 'href="/nicola-capasso-demo/azioni-mobile-fix.css"' in page_html, str(page_path)
        folder = page_path.parent.relative_to(PUBLIC).as_posix()
        folder = "" if folder == "." else folder + "/"
        assert f'href="/nicola-capasso-demo/{folder}index.html"' in page_html, str(page_path)
        assert '<base' not in page_html
        assert '<meta name="robots" content="noindex,follow">' in page_html
    else:
        assert f'href="{prefix}azioni-mobile-fix.css"' in page_html, str(page_path)
        assert f'<link rel="stylesheet" href="{prefix}mobile.css">' in page_html
        assert f'<link rel="stylesheet" href="{prefix}azioni.css">' in page_html
    assert "../../assets/" not in page_html
assert len(PAGES) == 34, len(PAGES)
assert "../assets/" not in html
assert html.count('class="scene-card"') == 12
assert html.count('class="project reveal"') == 10
assert "Storie, non pose." not in html
assert "Clicca una foto e scopri la storia" in html
assert "Il vostro giorno, attraverso i miei scatti." in html
assert 'class="caption"' not in html
for removed in (
    "Fotografia di matrimonio — Italia",
    "Fotografo · racconto · memoria",
    "Disponibile in Italia e all'estero",
    "Uno sguardo sul vostro giorno",
    "Fotografie sincere, nate dalla luce e dalle persone",
    "Presenza",
    "Intimità",
    "Emozione",
    "Memoria",
    "Un giorno da ricordare",
    "La luce di settembre",
    "Vicino a te",
    "Il tempo, piano",
    "02 — Il mio sguardo",
    "03 — Il prossimo capitolo",
    "Italia · ovunque vi porti la storia",
    "@font-face",
    "DM Sans",
    "Michroma",
    "Gloock",
    "Libre Baskerville",
    "scroll-progress",
):
    assert removed not in html, removed

assets = set(re.findall(r'(?:src|href)="(assets/[^\"]+)"', html))
assets.update({"assets/fonts/italiana-regular.ttf", "assets/fonts/space-grotesk.ttf"})
assert len(assets) == 15, f"Expected 15 unique local font/loader/photo assets, found {len(assets)}"
for license_file in ("italiana-OFL.txt", "space-grotesk-OFL.txt"):
    assert (PUBLIC / "assets/fonts" / license_file).is_file()
for asset in assets:
    assert (PUBLIC / asset).is_file(), asset
with tempfile.TemporaryDirectory() as tmp:
    inline = Path(tmp) / "inline.js"
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.S)
    assert scripts
    inline.write_text("\n".join(scripts), encoding="utf-8")
    subprocess.run(["node", "--check", str(inline)], check=True)
subprocess.run(["node", "--check", str(PUBLIC / "assets/fonts/load-fonts.js")], check=True)


def check_typography(page):
    page.evaluate("window.typographyReady")
    page.evaluate("document.fonts.ready")
    fonts = page.evaluate("[...document.fonts].map(f => ({family:f.family,status:f.status}))")
    assert len(fonts) == 2 and all(f["status"] == "loaded" for f in fonts), fonts
    assert {f["family"].strip("'\"") for f in fonts} == {"Italiana", "Space Grotesk"}, fonts
    style = page.locator(".hero h1").evaluate("""e => {
        const s=getComputedStyle(e);
        return {font:s.fontFamily,weight:s.fontWeight,blend:s.mixBlendMode,
            stroke:parseFloat(s.webkitTextStrokeWidth),size:parseFloat(s.fontSize),
            spacing:parseFloat(s.letterSpacing)};
    }""")
    assert "Italiana" in style["font"] and style["weight"] == "400" and style["blend"] == "normal", style
    assert abs(style["stroke"] / style["size"] - .016) < .00001, style
    assert abs(style["spacing"] / style["size"] - .015) < .00001, style
    for selectors, family, weight in (
        (".intro h2,.about h2,.contact h2,.section-head h2,.luxury-link", "Italiana", "400"),
        ("body,p:not(.gallery-invite),.nav,.nav a,.nav .brand,.hero-note,.eyebrow,button,input,textarea,select", "Space Grotesk", "400" if page.evaluate("matchMedia('(max-width:700px), (max-width:1000px) and (pointer:coarse)').matches") else "300"),
    ):
        styles = page.locator(selectors).evaluate_all(
            "es => es.map(e => { const s=getComputedStyle(e); return {font:s.fontFamily,weight:s.fontWeight}; })"
        )
        assert styles and all(family in s["font"] and s["weight"] == weight for s in styles), styles
    invite = page.locator('.gallery-invite').evaluate("e=>({font:getComputedStyle(e).fontFamily,weight:getComputedStyle(e).fontWeight})")
    assert 'Space Grotesk' in invite['font'] and invite['weight'] == '400', invite
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")


viewports = ((390, 844), (320, 568), (1440, 900), (700, 900), (701, 900))  # ridotti all'osso (fase prototipo)
with sync_playwright() as p:
    options: dict[str, object] = {"headless": True}
    if os.environ.get("BROWSER_PATH"):
        options["executable_path"] = os.environ["BROWSER_PATH"]
    browser = p.chromium.launch(**options)
    for width, height in viewports:
        page = browser.new_page(viewport={"width": width, "height": height}, offline=True)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(HTML_PATH.as_uri())
        check_typography(page)
        page.wait_for_timeout(2100)
        assert page.locator(".scene-card").count() == 12
        assert page.locator(".portrait").evaluate("e => e.complete && e.naturalWidth > 0")
        gaps = page.evaluate("""() => {
            const photo=document.querySelector('.portrait').getBoundingClientRect();
            const caption=document.querySelector('.hero-meta').getBoundingClientRect();
            const cue=document.querySelector('.hero-note').getBoundingClientRect();
            return {photoCaption:caption.top-photo.bottom,captionCue:cue.top-caption.bottom};
        }""")
        assert gaps["photoCaption"] >= 6 and gaps["captionCue"] >= 12, (width, gaps)
        if os.environ.get("VERIFY_SCREENSHOT_DIR"):
            destination = Path(os.environ["VERIFY_SCREENSHOT_DIR"])
            destination.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(destination / f"hero-{width}.png"))
        page.add_style_tag(content="html{scroll-behavior:auto!important}")
        boundary = page.evaluate("scrollY+document.querySelector('.intro').getBoundingClientRect().top-innerHeight")
        for delta, expected in ((-5, "1"), (5, "0"), (100, "0"), (-20, "1")):
            page.evaluate("y => scrollTo(0,y)", boundary + delta)
            page.wait_for_function(
                "expected => frameId === 0 && Math.abs(displayProgress-progressAt(scrollY))*geometry.range < .1 && getComputedStyle(heroNote).opacity === expected",
                arg=expected,
                timeout=5000,
            )
            actual_opacity = page.locator(".hero-note").evaluate("e => getComputedStyle(e).opacity")
            assert actual_opacity == expected, (width, height, delta, boundary, actual_opacity, page.evaluate("({scrollY, introTop:document.querySelector('.intro').getBoundingClientRect().top, height:innerHeight, idle:frameId===0, displayProgress})"))
        hero_height = page.locator(".hero").evaluate("e => e.offsetHeight")
        intro_inset = page.evaluate("document.querySelector('.statement').getBoundingClientRect().top-document.querySelector('.intro').getBoundingClientRect().top")
        assert intro_inset <= 96, (width, intro_inset)
        for step in range(27):
            page.evaluate("y => window.scrollTo(0,y)", hero_height-height*1.3+step*height*.05)
            page.wait_for_timeout(50)
            handoff = page.evaluate("""() => {
                const r=document.querySelector('.statement').getBoundingClientRect();
                const photos=[...document.querySelectorAll('.scene-card')].some(e=>{
                    const b=e.getBoundingClientRect();
                    return Number(getComputedStyle(e).opacity)>.05 && b.bottom>0 && b.top<innerHeight;
                });
                return {photos, text:r.top<innerHeight&&r.bottom>0, textBottom:r.bottom};
            }""")
            assert handoff["textBottom"] <= 0 or handoff["photos"] or handoff["text"], (width, step, handoff)
        page.evaluate("window.scrollTo(0, document.querySelector('.works').offsetTop)")
        page.wait_for_timeout(700)
        frames = page.locator(".project .frame").evaluate_all(
            "es => es.map(e => { const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height,ratio:r.width/r.height}; })"
        )
        assert len(frames) == 10
        assert all(abs(frame["ratio"] - 1) < .01 for frame in frames), (width, frames)
        if width > 700:
            for i in range(0, len(frames), 2):
                assert abs(frames[i]["x"] - frames[0]["x"]) < 1
                assert abs(frames[i + 1]["x"] - frames[1]["x"]) < 1
                assert abs(frames[i]["y"] - frames[i + 1]["y"]) < 1
                if i:
                    assert frames[i]["y"] > frames[i - 2]["y"]
        else:
            assert all(abs(frame["x"] - frames[0]["x"]) < 1 for frame in frames)
            assert all(a["y"] < b["y"] for a, b in zip(frames, frames[1:]))
        page.evaluate("[...document.images].forEach(i => i.loading='eager')")
        page.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)")
        assert page.locator(".caption").count() == 0
        assert not errors, errors
        page.close()

        reduced = browser.new_page(viewport={"width": width, "height": height}, reduced_motion="reduce", offline=True)
        reduced_errors = []
        reduced.on("pageerror", lambda error: reduced_errors.append(str(error)))
        reduced.goto(HTML_PATH.as_uri())
        check_typography(reduced)
        assert reduced.locator(".scene-card").count() == 12
        assert reduced.locator(".scene-card").first.evaluate("e => getComputedStyle(e).display === 'none'")
        assert not reduced_errors, reduced_errors
        reduced.close()

    # Model the repository subpath on Pages, not just file:// previews.
    class PagesHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if not self.path.startswith("/nicola-capasso-demo/"):
                self.send_error(404)
                return
            self.path = self.path[len("/nicola-capasso-demo"):]
            super().do_GET()

        def log_message(self, format, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(PagesHandler, directory=str(PUBLIC)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        web = browser.new_page(viewport={"width": 390, "height": 844})
        web_errors = []
        web.on("pageerror", lambda error: web_errors.append(str(error)))
        response = web.goto(f"http://127.0.0.1:{server.server_port}/nicola-capasso-demo/")
        assert response.status == 200
        check_typography(web)
        assert web.locator(".portrait").evaluate("e => e.complete && e.naturalWidth > 0")
        assert not web_errors, web_errors
        web.close()
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
        browser.close()

subprocess.run([sys.executable, str(ROOT / ".github/scripts/verify_public_pages.py")], check=True)
subprocess.run([sys.executable, str(ROOT / ".github/scripts/verify_404.py")], check=True)
print("PASS: 15 unique assets; two loaded local fonts; normalized name typography at 7 viewports; title/UI/editorial-link weights; continuous photo/text handoff; cue spacing and arrow exit/reverse; 12 animation photos; 10 square gallery crops; reduced motion; Pages subpath HTTP; JS syntax")
