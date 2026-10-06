"""Verifica statica del set pubblicato (leggera): manifest, riferimenti, sintassi JS,
refuso, risorse esterne, lingua/hreflang, pagine legali e footer.
Nessun render: i controlli visivi restano su verify_site.py, verify_footer.py e verify_contact.py."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
BASE = "/nicola-capasso-demo/"
SOCIAL = ("https://instagram.com/nicolacapassofoto", "https://wa.me/393398563098")

manifest = json.loads((ROOT / "docs/MANIFEST-PUBBLICAZIONE.json").read_text(encoding="utf-8"))
files = sorted(p for p in PUBLIC.rglob("*") if p.is_file())
assert len(files) == len(manifest["files"]), (len(files), len(manifest["files"]))
for p in files:
    key = f"public/{p.relative_to(PUBLIC).as_posix()}"
    assert key in manifest["files"], key
    assert hashlib.sha256(p.read_bytes()).hexdigest() == manifest["files"][key], key

pages = sorted(PUBLIC.rglob("*.html"))
assert len(pages) == 34, len(pages)
assert manifest["htmlPages"] == len(pages)
LEGAL = {"privacy.html", "cookies.html", "termini.html", "terms.html"}
assert len([p for p in pages if p.name == "404.html"]) == 2

with tempfile.TemporaryDirectory() as tmp:
    for page in pages:
        html = page.read_text(encoding="utf-8")
        rel = page.relative_to(PUBLIC).as_posix()
        depth = len(page.relative_to(PUBLIC).parts) - 1
        prefix = "../" * depth
        for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
            if ref.startswith(("#", "mailto:", "data:")):
                continue
            if ref.startswith("http"):
                assert ref in SOCIAL, (rel, ref)
                continue
            target = PUBLIC / ref.removeprefix(BASE) if ref.startswith(BASE) else (page.parent / ref.split("#")[0])
            assert target.is_file(), (rel, ref)
        assert "Hompage" not in html, f"refuso Hompage in {rel}"
        assert "../../assets/" not in html, rel
        if page.parent == PUBLIC:
            assert "../assets/" not in html, rel
        inline = re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.S)
        if inline and any(part.strip() for part in inline):
            script = Path(tmp) / (rel.replace("/", "_") + ".js")
            script.write_text("\n".join(inline), encoding="utf-8")
            subprocess.run(["node", "--check", str(script)], check=True)
        assert f'lang="{"en" if depth else "it"}"' in html, rel
        if page.name in LEGAL:
            assert '<meta name="robots" content="noindex, nofollow">' in html, rel
            assert "339 856 3098" not in html, f"numero del titolare ancora presente in {rel}"
            for tag in ('hreflang="it"', 'hreflang="en"', 'hreflang="x-default"'):
                assert tag in html, (rel, tag)
            assert "footer-legal" in html, rel
            if page.name == "privacy.html":
                assert ("telefono (facoltativo)" in html) or ("phone (optional)" in html), rel
        elif page.name == "404.html":
            assert "site-footer" not in html, rel
        else:
            assert f'<link rel="stylesheet" href="{prefix}footer.css">' in html, rel
            assert 'class="footer-legal"' in html, rel

print(f"PASS: manifest {len(files)} file coerente; {len(pages)} pagine con riferimenti risolti, "
      "sintassi JS valida, lingua/hreflang corrette, pagine legali senza il numero del titolare e con "
      "voce 'telefono (facoltativo)' tra i dati raccolti, footer su 32 pagine e assente dalle 2 404, "
      "nessun refuso 'Hompage', nessuna risorsa esterna")
