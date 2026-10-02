from pathlib import Path
import os
import re
import subprocess
import tempfile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
HTML_PATH = PUBLIC / "index.html"
html = HTML_PATH.read_text(encoding="utf-8")
assert "../assets/" not in html
assert html.count('class="scene-card"') == 12
assert html.count('class="project reveal"') == 4
assert "Storie, non pose." in html
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
):
    assert removed not in html, removed

assets = set(re.findall(r"(?:src|href)=\"(assets/[^\"]+)\"", html))
assets.update(re.findall(r"url\(['\"]?(assets/[^'\")]+)", html))
assert len(assets) == 16, f"Expected 16 local font/photo assets, found {len(assets)}"
assert "assets/fonts/italiana-regular.ttf" in assets
assert (PUBLIC / "assets/fonts/italiana-OFL.txt").is_file()
for asset in assets:
    assert (PUBLIC / asset).is_file(), asset
with tempfile.TemporaryDirectory() as tmp:
    inline = Path(tmp) / "inline.js"
    scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.S)
    assert scripts
    inline.write_text("\n".join(scripts), encoding="utf-8")
    subprocess.run(["node", "--check", str(inline)], check=True)

with sync_playwright() as p:
    options: dict[str, object] = {"headless": True}
    if os.environ.get("BROWSER_PATH"):
        options["executable_path"] = os.environ["BROWSER_PATH"]
    browser = p.chromium.launch(**options)
    for width, height in ((390, 844), (1440, 900), (844, 390)):
        page = browser.new_page(viewport={"width": width, "height": height})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(HTML_PATH.as_uri())
        page.wait_for_timeout(500)
        page.evaluate("document.fonts.ready")
        assert page.evaluate("document.fonts.check('400 42px Italiana')")
        style = page.locator(".hero h1").evaluate(
            "e => { const s=getComputedStyle(e); return {font:s.fontFamily,blend:s.mixBlendMode,stroke:parseFloat(s.webkitTextStrokeWidth)}; }"
        )
        assert "Italiana" in style["font"] and style["blend"] == "normal", style
        assert style["stroke"] >= 1.2, style
        assert page.locator(".scene-card").count() == 12
        page.add_style_tag(content="html{scroll-behavior:auto!important}")
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
        page.evaluate("document.documentElement.style.scrollBehavior='auto'; window.scrollTo(0, document.querySelector('.works').offsetTop)")
        page.wait_for_timeout(700)
        frames = page.locator(".project .frame").evaluate_all(
            "els => els.map(e => { const r=e.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height,ratio:r.width/r.height}; })"
        )
        assert len(frames) == 4
        for frame in frames:
            assert abs(frame["ratio"] - 1) < 0.01, (width, frame)
        columns = 1 if width <= 700 else 2
        if columns == 2:
            assert abs(frames[0]["x"] - frames[2]["x"]) < 1
            assert abs(frames[1]["x"] - frames[3]["x"]) < 1
            assert abs(frames[0]["y"] - frames[1]["y"]) < 1
            assert abs(frames[2]["y"] - frames[3]["y"]) < 1
        else:
            assert all(abs(frame["x"] - frames[0]["x"]) < 1 for frame in frames)
            assert frames[0]["y"] < frames[1]["y"] < frames[2]["y"] < frames[3]["y"]
        assert page.locator(".project img").evaluate_all("es => es.every(e => e.complete && e.naturalWidth > 0)")
        assert page.locator(".caption").count() == 0
        assert not errors, errors
        page.close()

    reduced = browser.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    reduced.goto(HTML_PATH.as_uri())
    assert reduced.locator(".scene-card").count() == 12
    assert reduced.locator(".scene-card").first.evaluate("e => getComputedStyle(e).display === 'none'")
    reduced.close()
    browser.close()

print("PASS: 16 assets, Italiana wordmark, fixed color, continuous photo/text handoff, inline JS, 12 animation photos, 4 square gallery crops at phone/tablet/desktop, reduced motion")
