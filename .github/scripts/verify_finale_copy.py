"""Approved client copy: complete IT/EN biography, experience, one final CTA."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import json,re
ROOT=Path(__file__).resolve().parents[2]
COPY=json.loads((ROOT/'docs/TESTI-NICOLA-FINALE.json').read_text(encoding='utf-8'))
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
def plain(markup):
    p=Text();p.feed(markup);return ' '.join(' '.join(p.parts).split())
for lang,rel in [('It','index.html'),('En','en/index.html')]:
    page=(ROOT/'public'/rel).read_text(encoding='utf-8')
    match=re.search(r'<section class="about" id="sguardo">(.*?)</section>',page,re.S)
    assert match,rel
    section=match[1];text=plain(section)
    for field in ['heading','body','experienceHeading','experienceLead','experienceBody']:
        expected=' '.join(COPY[field+lang].split())
        assert expected in text,(rel,field,'missing or changed approved text')
    assert section.count('id="contatto"')==1,rel
    assert section.index('class="about-experience"')<section.index('id="contatto"'),rel
    assert section.index(COPY['heading'+lang])<section.index('class="about-experience"'),rel
    assert 'nicola-IMG_5586.jpg' in section,rel
    cta=re.search(r'<a class="cta luxury-link".*?</a>',section,re.S)
    assert cta and 'href="contatti.html"' in cta[0],rel
    assert plain(cta[0])==('Raccontatemi il vostro giorno' if lang=='It' else 'Tell me about your day'),rel
    assert section.rstrip().endswith('</a></article>'),(rel,'CTA is not last')
print('PASS: complete approved copy IT/EN; biography -> experience -> single unchanged contact CTA; original portrait')
