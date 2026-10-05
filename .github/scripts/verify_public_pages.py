"""Verify the complete imported page set, shared styles and action routes."""
from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import tempfile
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
manifest = json.loads((ROOT / "docs/MANIFEST-PUBBLICAZIONE.json").read_text(encoding="utf-8"))
for name, expected in manifest["files"].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
pages = sorted(PUBLIC.glob("*.html"))
assert len(pages) == 12
with tempfile.TemporaryDirectory() as tmp:
    for file in pages:
        html = file.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:src|href)="([^\"]+)"', html):
            if not ref.startswith(("#", "mailto:", "https:", "http:")):
                assert (PUBLIC / ref.split("#")[0]).is_file(), (file.name, ref)
        scripts = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.S)
        script = Path(tmp) / (file.stem + ".js")
        script.write_text("\n".join(scripts), encoding="utf-8")
        subprocess.run(["node", "--check", str(script)], check=True)

SELECTOR = "body.story-a .home-return,body.portfolio-a .home-return,body.story-a .portfolio-return,body.story-a .story-nav > .next,#storie .portfolio-link.luxury-link,body .contact .cta.luxury-link,body.portfolio-a .portfolio-contact-link"
records = 0
fills = 0
interactions = 0
with sync_playwright() as p:
    options: dict[str, object] = {"headless": True}
    if os.environ.get("BROWSER_PATH"):
        options["executable_path"] = os.environ["BROWSER_PATH"]
    browser = p.chromium.launch(**options)
    for name, width, height, touch, reduced in (
        ("desktop", 1440, 900, False, False),
        ("narrow", 320, 700, True, False),
        ("mobile", 390, 844, True, False),
        ("reduced", 390, 844, True, True),
    ):
        context = browser.new_context(viewport={"width": width, "height": height}, has_touch=touch, is_mobile=touch, offline=True, reduced_motion="reduce" if reduced else "no-preference")
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for file in pages:
            page.goto(file.as_uri())
            page.evaluate("window.typographyReady")
            page.evaluate("document.fonts.ready")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            actions = page.locator(SELECTOR)
            assert actions.count() > 0
            for action in actions.all():
                metrics = action.evaluate("""e => {
                    const s=getComputedStyle(e), r=e.getBoundingClientRect(), range=document.createRange();
                    range.selectNodeContents(e);
                    const safe=[...range.getClientRects()].filter(t=>t.width>0).every(t=>t.left>=r.left-1&&t.right<=r.right+1&&t.top>=r.top-1&&t.bottom<=r.bottom+1);
                    return {font:s.fontFamily,border:s.borderTopWidth,h:r.height,safe,left:r.left,right:r.right,after:getComputedStyle(e,':after').display};
                }""")
                assert "Italiana" in metrics["font"] and metrics["border"] == "1px", (file.name, metrics)
                assert metrics["h"] >= 44 and metrics["safe"] and metrics["left"] >= -1 and metrics["right"] <= width + 1, (file.name, metrics)
                assert metrics["after"] == "block", (file.name, metrics)
                if name == "narrow":
                    continue
                action.scroll_into_view_if_needed()
                action.evaluate("e=>new Promise(resolve=>{const reveal=e.closest('.reveal');if(!reveal){resolve();return}const check=()=>{if(getComputedStyle(reveal).opacity==='1'&&!reveal.getAnimations().some(a=>a.playState==='running'))resolve();else requestAnimationFrame(check)};check()})")
                if not touch:
                    action.hover()
                else:
                    box = action.bounding_box()
                    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    page.mouse.down()
                page.wait_for_function("e=>getComputedStyle(e).color==='rgb(255, 255, 255)'&&parseFloat(getComputedStyle(e,':after').top)<0", arg=action.element_handle())
                if reduced:
                    assert action.evaluate("e=>getComputedStyle(e,':after').transitionDuration") == "0s"
                fills += 1
                page.mouse.move(0, 0)
                if touch:
                    page.mouse.up()
            if file.name.startswith("storia-"):
                next_number = int(file.stem[-2:]) % 10 + 1
                assert page.locator(".home-return").inner_text() == "Hompage"
                assert page.locator(".home-return").get_attribute("href") == "index.html"
                assert page.locator(".portfolio-return").first.inner_text() == "Portfolio"
                assert page.locator(".story-nav > .next").inner_text() == "Prossima Storia"
                assert page.locator(".story-nav > .next").get_attribute("href") == f"storia-{next_number:02d}.html"
                if name == "mobile":
                    page.locator(".photo-button").first.click()
                    assert page.locator("dialog").evaluate("e=>e.open")
                    page.locator("dialog .next").click()
                    assert page.locator(".lightbox-count").inner_text().startswith("2 /")
                    page.locator(".lightbox-close").click()
                    page.locator(".story-nav > .next").click()
                    assert page.url.endswith(f"storia-{next_number:02d}.html")
                    interactions += 1
            records += 1
            assert not errors, errors
        context.close()
    browser.close()
assert records == 48 and fills == 132 and interactions == 10
print(f"PASS: source manifest {len(manifest['files'])} files; all 12 pages; {records} page/viewport checks; {fills} filled states; {interactions} story viewer/navigation interactions; all inline JS syntax and local references")
