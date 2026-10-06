"""Verifica del footer pubblicato: 13 pagine con footer, 404 senza, icone corrette."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
PAGES = ["index.html", "portfolio.html", "contatti.html"] + [f"storia-{n:02d}.html" for n in range(1, 11)]

html_404 = (PUBLIC / "404.html").read_text(encoding="utf-8")
assert 'href="footer.css"' not in html_404 and "site-footer" not in html_404, "la 404 non deve montare il footer"
for name in PAGES:
    html = (PUBLIC / name).read_text(encoding="utf-8")
    assert html.count('class="site-footer"') == 1, name
    assert '<link rel="stylesheet" href="footer.css">' in html, name
    assert "mailto:" not in html.split("site-footer")[1], name
    assert "Nicola Capasso Photo" not in html.split("site-footer")[1], name
assert (PUBLIC / "footer.css").is_file()

with sync_playwright() as p:
    options: dict[str, object] = {"headless": True}
    if os.environ.get("BROWSER_PATH"):
        options["executable_path"] = os.environ["BROWSER_PATH"]
    browser = p.chromium.launch(**options)
    for name in PAGES:
        for width, height in ((390, 844), (320, 568), (1440, 900)):
            page = browser.new_page(viewport={"width": width, "height": height}, offline=True, reduced_motion="reduce")
            errors: list[str] = []
            external: list[str] = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("request", lambda r: external.append(r.url) if not r.url.startswith(("file://", "data:")) else None)
            page.goto((PUBLIC / name).as_uri())
            page.evaluate("document.fonts.ready")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(400)
            data = page.evaluate(
                """() => {
                    const f = document.querySelector('footer.site-footer');
                    const band = f.querySelector('.footer-band');
                    const links = [...f.querySelectorAll('a')];
                    const boxes = links.map(a => { const r = a.getBoundingClientRect(); return {w:r.width, h:r.height, top:Math.round(r.top)}; });
                    const copy = f.querySelector('.footer-copy').getBoundingClientRect();
                    return {
                        footers: document.querySelectorAll('footer.site-footer').length,
                        svgs: f.querySelectorAll('svg').length,
                        imgs: f.querySelectorAll('img').length,
                        navs: f.querySelectorAll('nav').length,
                        mailto: f.innerHTML.includes('mailto:'),
                        hrefs: links.map(a => a.getAttribute('href')),
                        minTouch: Math.min(...boxes.map(b => Math.min(b.w, b.h))),
                        rows: [...new Set(boxes.map(b => b.top))].length,
                        sameRow: boxes.every(b => Math.abs((b.top + b.h / 2) - (copy.top + copy.height / 2)) < 30),
                        overflow: Math.max(document.documentElement.scrollWidth - innerWidth, f.scrollWidth - f.clientWidth, band.scrollWidth - band.clientWidth),
                        copyText: f.querySelector('.footer-copy').textContent.trim(),
                        waClass: !!f.querySelector('svg.wa'),
                    };
                }"""
            )
            assert data["footers"] == 1 and data["svgs"] == 2 and data["imgs"] == 0 and data["navs"] == 0, (name, width, data)
            assert not data["mailto"] and data["waClass"], (name, width, data)
            assert data["hrefs"] == ["https://instagram.com/nicolacapassofoto", "https://wa.me/393398563098"], (name, width, data)
            assert data["minTouch"] >= 44 and data["rows"] == 1 and data["sameRow"], (name, width, data)
            assert data["overflow"] <= 0, (name, width, data)
            assert data["copyText"] == "© 2026 Nicola Capasso", (name, width, data["copyText"])
            assert not errors and not external, (name, width, errors, external)
            page.close()
    browser.close()
print("PASS: footer su 13 pagine e assente dalla 404; icone corrette, fascia su una riga, tocchi >=44px, nessun overflow, 0 errori JS, 0 richieste esterne")