"""Measure the actual album images and their clickable rows, in manifest order."""
import json
from pathlib import Path
from urllib.parse import urljoin

STORIES = Path(__file__).resolve().parents[2] / 'docs/STORIE.json'


def check_albums(browser, base, output):
    stories = json.loads(STORIES.read_bytes())
    cases, failures = [], []
    for width, height in [(390, 740), (1440, 900)]:
        context = browser.new_context(viewport={'width': width, 'height': height},
                                      is_mobile=width == 390, has_touch=width == 390)
        for prefix in ['', 'en/']:
            for story in stories:
                route = f'{prefix}storia-{story["number"]:02}.html'
                page = context.new_page()
                assert page.goto(urljoin(base, route)).ok, route
                cover = page.locator('img.story-cover')
                assert cover.count() == 1 and cover.is_visible(), route
                assert cover.evaluate('async i => {await i.decode(); return i.currentSrc}') == urljoin(base, story['cover_path']), route
                album = page.locator('.album')
                data = album.evaluate('''async album => {
                    const buttons = [...album.querySelectorAll('.photo-button')];
                    const images = buttons.map(b => b.querySelector('img'));
                    for (const image of images) {
                        image.loading = 'eager';
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
                assert cover.bounding_box()['y'] + cover.bounding_box()['height'] <= data['album']['top'] + 1, route
                assert [p['src'] for p in photos] == [urljoin(base, p['path']) for p in story['photos'] if p['path'] != story['cover_path']], route
                for n, photo in enumerate(photos):
                    box, image = photo['button'], photo['image']
                    nw, nh = photo['natural']
                    issues = []
                    previous = photos[n-1]['image']['bottom'] if n else cover.evaluate('i => i.getBoundingClientRect().bottom')
                    if abs(image['top'] - previous - (14 if width == 390 else 30)) > 1:
                        issues.append('photo spacing')
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
                cover_box = cover.bounding_box()
                cw,ch = cover.evaluate('i => [i.naturalWidth, i.naturalHeight]')
                assert abs(cover_box['height'] - cover_box['width'] * ch / cw) < 1, route
                assert abs(2*cover_box['x'] + cover_box['width'] - width) < 1, route
                opener = page.locator('.cover-button')
                for box in (cover_box, opener.bounding_box()):
                    assert abs(box['x'] - data['album']['left']) < 1 and abs(box['width'] - data['album']['width']) < 1, (route, width, 'cover alignment', box, data['album'])
                act = lambda button: button.tap() if width == 390 else button.click()
                act(opener)
                viewer = page.locator('dialog[open] img')
                assert viewer.evaluate('i => i.src') == urljoin(base, story['cover_path']) and viewer.get_attribute('alt') == cover.get_attribute('alt'), route
                counter = page.locator('.lightbox-count')
                assert counter.inner_text() == f'1 / {story["count"]}', route
                for index, photo in enumerate(photos):
                    if index == 0:
                        act(page.locator('dialog .next'))
                    else:
                        page.keyboard.press('ArrowRight')
                    number = index + 2
                    alt = story['title_it'] + (' — Wedding photograph ' if prefix else ' — Fotografia del matrimonio ') + str(number)
                    assert viewer.evaluate('async i => {await i.decode(); return [i.src, i.alt, getComputedStyle(i).objectFit]}') == [photo['src'], alt, 'contain'], route
                    assert page.locator('.lightbox-count').inner_text() == f'{number} / {story["count"]}', route
                page.keyboard.press('Escape')
                page.wait_for_function("!document.querySelector('dialog').open && document.body.style.overflow === ''")
                assert opener.evaluate('e => e === document.activeElement'), route
                internal = album.locator('.photo-button').first
                act(internal)
                assert viewer.evaluate('i => i.src') == photos[0]['src'] and counter.inner_text() == f'2 / {story["count"]}', route
                act(page.locator('.lightbox-close'))
                page.wait_for_function("!document.querySelector('dialog').open && document.body.style.overflow === ''")
                assert internal.evaluate('b => b === document.activeElement'), route
                cases.append(dict(route=route, width=width, viewer=True, **data))
                page.close()
        context.close()
    output.write_text(json.dumps({'base': base, 'cases': cases, 'failures': failures}), encoding='utf-8')
    print(f'{len(cases)} album cases, {sum(len(c["photos"]) for c in cases)} photos, {len(failures)} failed photo measurements')
    assert not failures, failures[:3]
