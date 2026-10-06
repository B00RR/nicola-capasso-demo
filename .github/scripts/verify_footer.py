"""Verifica del footer pubblicato: presente su tutte le pagine tranne le 404, con i link legali.
Controllo statico su tutte le pagine + render reale su 4 pagine campione (mobile e desktop)."""
from pathlib import Path
import os
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
not_found, pages = [], []
for page in sorted(PUBLIC.rglob("*.html")):
    (not_found if page.name == "404.html" else pages).append(page)
assert len(not_found) == 2 and len(pages) == 32, (len(not_found), len(pages))

for page in not_found:
    text = page.read_text(encoding="utf-8")
    assert "site-footer" not in text and "footer.css" not in text, str(page)

for page in pages:
    prefix = "../" * (len(page.relative_to(PUBLIC).parts) - 1)
    text = page.read_text(encoding="utf-8")
    assert text.count('class="site-footer"') == 1, str(page)
    assert f'<link rel="stylesheet" href="{prefix}footer.css">' in text, str(page)
    footer = re.search(r'<footer class="site-footer".*?</footer>', text, re.S).group(0)
    assert "mailto:" not in footer and "Nicola Capasso Photo" not in footer, str(page)
    assert "<nav" not in footer and "<img" not in footer, str(page)
    assert footer.count("<svg") == 2 and 'class="wa"' in footer, str(page)
    assert footer.count('class="footer-legal"') == 1, str(page)
    legal = footer.split('class="footer-legal"')[1].split("</ul>")[0]
    hrefs = re.findall(r'href="([^"]+)"', legal)
    assert len(hrefs) == 3, (str(page), hrefs)
    for href in hrefs:
        assert (page.parent / href).is_file(), (str(page), href)
assert (PUBLIC / "footer.css").is_file()

SAMPLES = [PUBLIC / "index.html", PUBLIC / "privacy.html", PUBLIC / "en/index.html", PUBLIC / "en/terms.html"]
with sync_playwright() as p:
    options: dict[str, object] = {"headless": True}
    if os.environ.get("BROWSER_PATH"):
        options["executable_path"] = os.environ["BROWSER_PATH"]
    browser = p.chromium.launch(**options)
    for page_path in SAMPLES:
        for width, height in ((390, 844), (1440, 900)):
            page = browser.new_page(viewport={"width": width, "height": height}, offline=True, reduced_motion="reduce")
            errors = []
            external = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("request", lambda r: external.append(r.url) if not r.url.startswith(("file://", "data:")) else None)
            page.goto(page_path.as_uri())
            page.evaluate("document.fonts.ready")
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(300)
            data = page.evaluate(
                """() => {
                    const f = document.querySelector('footer.site-footer');
                    const band = f.querySelector('.footer-band');
                    const social = [...f.querySelectorAll('.footer-social-link')];
                    const legal = [...f.querySelectorAll('.footer-legal a')];
                    const boxes = [...social, ...legal].map(a => a.getBoundingClientRect());
                    return {
                        footers: document.querySelectorAll('footer.site-footer').length,
                        svgs: f.querySelectorAll('svg').length,
                        imgs: f.querySelectorAll('img').length,
                        navs: f.querySelectorAll('nav').length,
                        mailto: f.innerHTML.includes('mailto:'),
                        copy: f.querySelector('.footer-copy').textContent.trim(),
                        social: social.map(a => a.getAttribute('href')),
                        legal: legal.map(a => a.textContent.trim()),
                        legalRows: [...new Set(legal.map(a => Math.round(a.getBoundingClientRect().top)))].length,
                        minHeight: Math.min(...boxes.map(b => b.height)),
                        overflow: Math.max(document.documentElement.scrollWidth - innerWidth, band.scrollWidth - band.clientWidth),
                    };
                }"""
            )
            label = (str(page_path.relative_to(PUBLIC)), width)
            assert data["footers"] == 1 and data["svgs"] == 2 and data["imgs"] == 0 and data["navs"] == 0, (label, data)
            assert not data["mailto"] and data["copy"] == "\u00a9 2026 Nicola Capasso", (label, data)
            assert data["social"] == ["https://instagram.com/nicolacapassofoto", "https://wa.me/393398563098"], (label, data)
            assert len(data["legal"]) == 3 and data["legalRows"] == 1, (label, data)
            assert data["minHeight"] >= 44 and data["overflow"] <= 0, (label, data)
            assert not errors and not external, (label, errors, external)
            page.close()
    browser.close()
print("PASS: footer su 32 pagine e assente dalle 2 404; 2 icone, 3 link legali su una riga, "
      "nessuna email, nessun overflow, tocchi >=44px, 0 errori JS, 0 richieste esterne")
