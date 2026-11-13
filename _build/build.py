#!/usr/bin/env python3
# Builds the whole site into /home/claude/site-new from the live site plus the generator.  python3 build.py
import shutil, glob, sys, datetime, os
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core
from core import *
import pages, pages2
TODAY = datetime.date.today().isoformat()

def copy_static():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT + 'assets')
    for d in ('fonts', 'brand', 'embed'): shutil.copytree(LIVE + d, OUT + d)
    for f in ('CNAME', 'favicon.ico', 'favicon.svg', 'apple-touch-icon.png', 'og-image.png', 'DEPLOY.md', 'feedback.html', 'main.js', 'currency.js'): shutil.copy(LIVE + f, OUT + f)
    # private sample pages: carried over as they are, minus the practice page
    shutil.copytree(LIVE + 'for', OUT + 'for', ignore=shutil.ignore_patterns('test-k7q2'))
    # the generator travels with the site (GitHub Pages does not publish folders that start with an underscore)
    shutil.copytree(HERE, OUT + '_build', ignore=shutil.ignore_patterns('__pycache__'))

def images():
    os.makedirs(OUT + 'media/showcase')
    def save(im, path, q=74):
        im = im.convert('RGB')
        for qq in (q, 68, 62, 56):
            im.save(path, 'JPEG', quality=qq, optimize=True, progressive=True)
            if os.path.getsize(path) < 150_000: break
    for f in glob.glob(LEG + 'media/showcase/*-wide.jpg'):
        k = os.path.basename(f)[:-9]; im = Image.open(f)
        save(im.resize((1280, 720), Image.LANCZOS), OUT + f'media/showcase/{k}-wide.jpg')
        save(im.resize((640, 360), Image.LANCZOS), OUT + f'media/showcase/{k}-card.jpg', 72)
    # stills for the vertical, square and looks players, taken from the middle of each video
    for f in glob.glob(LEG + 'media/showcase/*.jpg'):
        if not f.endswith('-wide.jpg'): shutil.copy(f, OUT + 'media/showcase/')
    for f in glob.glob(LIVE + 'media/showcase/*.gif'): shutil.copy(f, OUT + 'media/showcase/')
    for k in ('going-to-the-sun-road', 'million-dollar-highway', 'miami-to-key-west', 'tour-du-mont-blanc', 'cyclades-island-hop', 'dublin-to-the-maldives'):
        save(Image.open(LEG + f'media/{k}.jpg').resize((640, 360), Image.LANCZOS), OUT + f'media/{k}-card.jpg', 72)

def assets():
    css = open(LEG + 'styles.css').read().replace('url(fonts/', 'url(/fonts/') + '\n' + open(LEG + 'pages.css').read() + open(SRC + 'new.css').read()
    open(OUT + 'assets/site.css', 'w').write(css)
    shutil.copy(SRC + 'site.js', OUT + 'assets/site.js'); shutil.copy(SRC + 'consent.js', OUT + 'consent.js')
    # the private sample pages keep the earlier stylesheet, with the darker coral so small text and buttons pass contrast
    open(OUT + 'styles.css', 'w').write(open(LEG + 'styles.css').read().replace('--route-text: #d23b1c;   /* coral that carries white text (4.6:1) */', '--route-text: #bf3415;   /* coral that carries white text (5.6:1) */').replace('.btn-primary:hover { background: #b9321a;', '.btn-primary:hover { background: #a02a10;'))
    s = open(OUT + 'for/sample-page.css').read().replace('.sp-time { font-weight: 400; opacity: .85; }', '.sp-time { font-weight: 400; }'); open(OUT + 'for/sample-page.css', 'w').write(s)
    for f in glob.glob(OUT + 'for/*/index.html'):
        s = open(f).read()
        if 'munsterbus' not in f: s = s.replace('<html lang="en-IE">', '<html lang="en-US">')
        s = re.sub(r'\s*// sale mode only, e\.g\. "The full reel is €149[^\n]*', '   // sale mode only: the offer text', s)
        open(f, 'w').write(s)
    s = us(open(OUT + 'feedback.html').read()).replace('We’re asking a few tour operators for honest opinions before we launch.', 'We’re asking a few tour operators for their honest opinions.'); open(OUT + 'feedback.html', 'w').write(s)

def sitemap():
    urls = ''.join(f'  <url><loc>{BASE}/{p}</loc><lastmod>{TODAY}</lastmod></url>\n' for p, ix in PAGES if ix)
    open(OUT + 'sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(OUT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n')

def check():
    bad = []
    for f in glob.glob(OUT + '**/*.html', recursive=True):
        if '/for/' in f or '/embed/' in f or '/_build/' in f: continue
        s = open(f).read(); rel = f[len(OUT):]
        for h in re.findall(r'(?:href|src|poster)="([^"]+)"', s):
            if re.match(r'(https?:|mailto:|data:|#|javascript:)', h): continue
            t = h.split('?')[0].split('#')[0]
            t = t.lstrip('/') if t.startswith('/') else os.path.normpath(os.path.join(os.path.dirname(rel), t))
            if t == '' or t.endswith('/'): t += 'index.html'
            if not os.path.exists(OUT + t): bad.append((rel, h))
        if rel != 'feedback.html':
            assert s.count('<h1') == 1, f'{rel}: {s.count("<h1")} h1'
            ids = re.findall(r'\sid="([^"]+)"', s); dup = {i for i in ids if ids.count(i) > 1}
            assert not dup, f'{rel}: duplicate ids {dup}'
    for b in bad: print('BROKEN', b)
    assert not bad, 'broken links'
    print(f'{len(PAGES)} pages built, {sum(1 for _, i in PAGES if i)} in the sitemap, no broken links')

if __name__ == '__main__':
    copy_static(); images(); assets()
    dates = json.load(open(HERE + 'dates.json'))
    pages.home(); pages.pricing(); pages.how(); pages.sample(); pages.thanks(); pages.notfound(); pages.showcase_index(); pages.madefor_index()
    pages2.events(); pages2.new_showcases(dates)
    for p in ('made-for/cycling-tours/', 'made-for/motorcoach-tours/'): pages2.carry(p, 'made-for', 'madefor')
    for p in ('showcase/alaska-inside-passage/', 'showcase/napa-and-sonoma-by-bike/', 'showcase/one-route-many-looks/', 'showcase/texas-hill-country-charity-ride/'): pages2.carry(p, 'showcase', 'showcase')
    pages2.carry_privacy()
    sitemap(); check()
    tot = sum(os.path.getsize(f) for f in glob.glob(OUT + '**/*', recursive=True) if os.path.isfile(f))
    print('site size', round(tot / 1e6, 1), 'MB; site.css', os.path.getsize(OUT + 'assets/site.css') // 1024, 'KB; site.js', os.path.getsize(OUT + 'assets/site.js') // 1024, 'KB')
