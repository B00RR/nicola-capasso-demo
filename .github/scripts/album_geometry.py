"""Measure the actual album images and their clickable rows, in manifest order."""
import json
from pathlib import Path
from urllib.parse import urljoin

STORIES = Path(__file__).resolve().parents[2] / 'docs/STORIE.json'


def check_albums(browser, base, output):
    stories = json.loads(STORIES.read_bytes())
    cases, failures = [], []
    for width, height in [(390, 844), (1440, 900)]:
        context = browser.new_context(viewport={'width': width, 'height': height},
                                      is_mobile=width == 390, has_touch=width == 390)
        for prefix in ['', 'en/']:
            for story in stories:
                route = f'{prefix}storia-{story["number"]:02}.html'
                page = context.new_page()
                assert page.goto(urljoin(base, route)).ok, route
                album = page.locator('.album')
                data = album.evaluate('''async album => {
                    const buttons = [...album.querySelectorAll('.photo-button')];
                    const images = buttons.map(b => b.querySelector('img'));
                    images.forEach(i => i.loading = 'eager');
                    for (const image of images) {
                        try { await image.decode(); }
                        catch (e) { throw Error(`${image.src}: ${e.message}`); }
                    }
                    await document.fonts.ready;
                    const rect = e => e.getBoundingClientRect().toJSON();
                    return {album: rect(album), columns: getComputedStyle(album).gridTemplateColumns,
                        stylesheet: [...document.styleSheets].find(s => s.href?.includes('/styles/stories.css')).href,
                        photos: images.map((i,n) => ({src: i.currentSrc, natural: [i.naturalWidth, i.naturalHeight],
                            image: rect(i), button: rect(buttons[n])}))};
                }''')
                photos = data['photos']
                assert [p['src'] for p in photos] == [urljoin(base, p['path']) for p in story['photos']], route
                for n, photo in enumerate(photos):
                    box, image = photo['button'], photo['image']
                    nw, nh = photo['natural']
                    issues = []
                    if n and box['top'] < photos[n-1]['button']['bottom'] - 1:
                        issues.append('overlap')
                    if any(abs(box[k] - data['album'][k]) > 1 for k in ('left', 'right')):
                        issues.append('row width')
                    if min(image['width'], image['height']) <= 0 or any(abs(image[k] - box[k]) > 1 for k in ('left', 'right', 'top', 'bottom')):
                        issues.append('image bounds')
                    if abs(image['height'] - image['width'] * nh / nw) > 1:
                        issues.append('aspect ratio')
                    if issues:
                        failures.append([route, width, n+1, issues])
                opener = album.locator('.photo-button').first
                opener.click()
                viewer = page.locator('dialog[open] img')
                for index in (0, 1):
                    if index:
                        page.keyboard.press('ArrowRight')
                    assert viewer.evaluate('async i => {await i.decode(); return [i.src, getComputedStyle(i).objectFit]}') == [photos[index]['src'], 'contain'], route
                page.keyboard.press('Escape')
                page.wait_for_function("!document.querySelector('dialog').open && document.body.style.overflow === ''")
                assert opener.evaluate('e => e === document.activeElement'), route
                cases.append(dict(route=route, width=width, viewer=True, **data))
                page.close()
        context.close()
    output.write_text(json.dumps({'base': base, 'cases': cases, 'failures': failures}), encoding='utf-8')
    print(f'{len(cases)} album cases, {sum(len(c["photos"]) for c in cases)} photos, {len(failures)} failed photo measurements')
    assert not failures, failures[:3]
