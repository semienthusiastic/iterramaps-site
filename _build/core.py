# Iterra Maps site generator: shared pieces. One list of pages drives the menu, footer, index pages, "more" lists and sitemap.
import html, json, re, os, hashlib
import os as _os
HERE = _os.path.dirname(_os.path.abspath(__file__)) + '/'
LIVE = _os.environ.get('SITE_LIVE', '/home/claude/iterramaps-site/')   # a copy of the site as it is on GitHub now: fonts, brand, /for/ pages and so on are taken from here
LEG = HERE + 'legacy/'                   # frozen inputs: the six page bodies written before this generator, the earlier styles, the original poster stills
OUT = _os.environ.get('SITE_OUT', '/home/claude/site-new/')     # the site as built
SRC = HERE + 'src/'
BASE = 'https://iterramaps.com'
R2 = 'https://media.iterramaps.com/site/showcase/'
REEL = 'https://media.iterramaps.com/site/showreel/'
e = html.escape
CTA = 'Get a free sample'
PROMISE = 'Send one tour link. We reply within one working day and send a 15-second sample in your colours, usually within 2 to 3 working days. No cost, no obligation.'
CHANGE = 'Send us the new route file or itinerary. Your route and style are saved, so we remake the videos it affects at half their price.'

# ---- every showcase film, in display order. kind = filter group; mf = its audience page (or None)
SHOWCASES = [
 dict(slug='napa-and-sonoma-by-bike', key='napa', name='Napa and Sonoma by bike', kind='cycling', tag='Cycling tour', meta='5 days · 108 mi', dur=118, mf='cycling-tours',
      blurb='Five days from Healdsburg to Sonoma on the real roads, with the Oakville Grade climbed in 3D.'),
 dict(slug='texas-hill-country-charity-ride', key='charity', name='A charity ride in the Texas Hill Country', kind='events', tag='Charity ride', meta='2 days · 129 mi', dur=90, mf='cycling-events',
      blurb='Every rest stop, lunch stop and the overnight, with the sponsors on screen from start to finish.'),
 dict(slug='lakeshore-330', key='events', name='The Lakeshore 330', kind='events', tag='Multi-day ride', meta='6 days · route video and daily clips', dur=74, mf='cycling-events',
      blurb='One video for the route reveal, and a 12-second clip for each of the six days.'),
 dict(slug='canadian-rockies-by-coach', key='coach', name='The Canadian Rockies by coach', kind='coach', tag='Coach tour', meta='7 nights · Calgary to Jasper', dur=85, mf='motorcoach-tours',
      blurb='Banff, Lake Louise, the Icefields Parkway and Jasper, with a card for each day.'),
 dict(slug='alaska-inside-passage', key='cruise', name="Alaska's Inside Passage by small ship", kind='cruise', tag='Small-ship cruise', meta='7 nights · Vancouver to Sitka', dur=83, mf=None,
      blurb='Sea days and ports of call on one map, with a card for each port.'),
 dict(slug='switzerland-by-rail', key='rail', name='Switzerland by rail', kind='rail', tag='Rail journey', meta='8 days · Zurich to Tirano', dur=85, mf=None,
      blurb='Four famous trains in one journey, including the Glacier Express and the Bernina Express.'),
 dict(slug='camino-sarria-to-santiago', key='walking', name='The Camino, Sarria to Santiago', kind='walking', tag='Walking holiday', meta='5 stages · about 115 km', dur=83, mf=None,
      blurb='The last five stages of the Camino Francés on foot, stage by stage.'),
 dict(slug='one-route-many-looks', key='looks', name='One route, four looks', kind='looks', tag='Looks', meta='4 looks · 30 seconds each', dur=30, mf=None, poster='napa',
      blurb='The same bike tour made four ways, to show how far the look can change.'),
]
SC = {s['slug']: s for s in SHOWCASES}
KINDS = [('cycling', 'Cycling tours'), ('events', 'Events and rides'), ('coach', 'Coach tours'), ('cruise', 'Cruises'), ('rail', 'Rail'), ('walking', 'Walking'), ('looks', 'Looks')]
# ---- every audience page that exists
MADEFOR = [
 dict(slug='cycling-tours', name='Cycling tours', long='Cycling tour operators', film='napa-and-sonoma-by-bike', nav='Every day of the tour, on the real roads',
      h='Show riders every day of the tour', p='The real roads, the climbs, the longer option and the van transfers, with a card for each overnight town.', go='For cycling tour operators'),
 dict(slug='cycling-events', name='Cycling events and charity rides', long='Cycling events and charity rides', film='texas-hill-country-charity-ride', nav='A route reveal, daily clips and your sponsors on screen',
      h='A route reveal, then a clip for each day', p='Rest stops, lunch stops and the overnight on the map, with your sponsors on screen from start to finish.', go='For ride organisers'),
 dict(slug='motorcoach-tours', name='Motorcoach and group tours', long='Motorcoach and group tours', film='canadian-rockies-by-coach', nav='Every overnight stop and sight, day by day',
      h='The whole tour, the way passengers travel it', p='Every overnight stop, hotel and sight on the real highways, day by day.', go='For coach tour companies'),
]
MF = {m['slug']: m for m in MADEFOR}
poster = lambda s, size='wide': f"/media/showcase/{s.get('poster', s['key'])}-{size}.jpg"

LOGO = '<svg width="34" height="34" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="27" fill="none" stroke="#0e1b24" stroke-width="3"/><ellipse cx="32" cy="32" rx="12" ry="27" fill="none" stroke="#0e1b24" stroke-opacity=".28" stroke-width="2.5"/><path d="M5 32H59" stroke="#0e1b24" stroke-opacity=".28" stroke-width="2.5"/><path d="M11 46C22 50 30 30 38 28C46 26 46 18 50 14" fill="none" stroke="#ff5a36" stroke-width="5.5" stroke-linecap="round"/><circle cx="11" cy="46" r="4.5" fill="#0e1b24"/><circle cx="50" cy="14" r="5.5" fill="#fff" stroke="#0e1b24" stroke-width="3.5"/></svg>'
ASSET_V = {}
def asset(path):
    if path not in ASSET_V: ASSET_V[path] = hashlib.md5(open(OUT + path.lstrip('/'), 'rb').read()).hexdigest()[:8]
    return f'{path}?v={ASSET_V[path]}'

def header(cur):
    c = lambda k: ' aria-current="page"' if cur == k else ''
    dd = ''.join(f'<a href="/made-for/{m["slug"]}/"><b>{e(m["name"])}</b><span>{e(m["nav"])}</span></a>' for m in MADEFOR)
    l2 = ''.join(f'<a class="l2" href="/made-for/{m["slug"]}/">{e(m["name"])}</a>' for m in MADEFOR)
    return f'''<header class="hd">
  <a class="skip" href="#main">Skip to content</a>
  <div class="wrap">
    <a class="brand" href="/" aria-label="Iterra Maps home">{LOGO}<span class="brand-name">Iterra <span>Maps</span></span></a>
    <nav class="hd-nav" aria-label="Main">
      <a href="/showcase/"{c('showcase')}>Showcase</a>
      <div class="hd-dd">
        <button type="button" class="hd-dd-btn" aria-expanded="false" aria-controls="hd-who"{' aria-current="true"' if cur == 'made-for' else ''}>Who it’s for <svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5L6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <div class="hd-dd-panel" id="hd-who" hidden>{dd}<a class="hd-dd-all" href="/made-for/">All kinds of trip</a></div>
      </div>
      <a href="/how-it-works/"{c('how')}>How it works</a>
      <a href="/pricing/"{c('pricing')}>Pricing</a>
    </nav>
    <div class="hd-right">
      <a class="btn btn-primary hd-cta" href="/sample.html"><span class="long">{CTA}</span><span class="short">Free sample</span></a>
      <button type="button" class="hd-toggle" aria-expanded="false" aria-controls="hd-panel" aria-label="Open menu"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path class="bars" d="M3 5.5h14M3 10h14M3 14.5h14"/><path class="x" d="M5 5l10 10M15 5L5 15"/></svg></button>
    </div>
    <div class="hd-panel" id="hd-panel" hidden>
      <a class="l1" href="/showcase/">Showcase</a>
      <a class="l1" href="/made-for/">Who it’s for</a>
      {l2}
      <a class="l1" href="/how-it-works/">How it works</a>
      <a class="l1" href="/pricing/">Pricing</a>
      <a class="btn btn-primary" href="/sample.html">{CTA}</a>
      <p><a href="mailto:hello@iterramaps.com">hello@iterramaps.com</a></p>
    </div>
  </div>
</header>
'''
def footer():
    sc = ''.join(f'<li><a href="/showcase/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SHOWCASES)
    mf = ''.join(f'<li><a href="/made-for/{m["slug"]}/">{e(m["name"])}</a></li>' for m in MADEFOR)
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <div class="ft-brand">
        <span class="brand-name">Iterra <span>Maps</span></span>
        <p>Animated route map videos for tour operators and events.</p>
        <a href="mailto:hello@iterramaps.com">hello@iterramaps.com</a>
      </div>
      <nav aria-labelledby="ft-sc"><h2 id="ft-sc">Showcase</h2><ul>{sc}<li><a href="/showcase/">All films</a></li></ul></nav>
      <nav aria-labelledby="ft-mf"><h2 id="ft-mf">Who it’s for</h2><ul>{mf}<li><a href="/made-for/">All kinds of trip</a></li></ul></nav>
      <nav aria-labelledby="ft-co"><h2 id="ft-co">Iterra Maps</h2><ul><li><a href="/how-it-works/">How it works</a></li><li><a href="/pricing/">Pricing</a></li><li><a href="/sample.html">{CTA}</a></li><li><a href="/privacy.html">Privacy notice</a></li><li><a href="#" class="js-cookie-settings">Cookie settings</a></li></ul></nav>
    </div>
    <div class="ft-base"><span>Map data in videos © OpenStreetMap contributors</span><span>© <span class="js-year">2026</span> Iterra Maps</span></div>
  </div>
</footer>
<dialog class="reel-player" id="reel-player" aria-labelledby="reel-player-title">
  <div class="reel-player-head"><h2 id="reel-player-title">Video</h2><button class="reel-player-close" type="button" aria-label="Close video"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M3 3l12 12M15 3L3 15" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg></button></div>
  <video controls playsinline preload="none"></video>
</dialog>
'''
# US spelling and terms on every public page (decided 13 Nov). Applied to the finished page, so earlier page bodies follow too.
US = [(r'\bcolour', 'color'), (r'\bColour', 'Color'), (r'\bworking day', 'business day'), (r'\bWorking day', 'Business day'), (r'\borganis', 'organiz'), (r'\bOrganis', 'Organiz'),
      (r'\bprogramme', 'program'), (r'\btravell', 'travel'), (r'\blicence', 'license'), (r'\benquir', 'inquir'), (r'\bWalking holidays\b', 'Walking tours'), (r'\bwalking holidays\b', 'walking tours'),
      (r'\bWalking holiday\b', 'Walking tour'), (r'walking and cycling holidays', 'walking and cycling tours'), (r'\bfavourite', 'favorite'), (r'\bcentre\b', 'center'), (r'\bmetres\b', 'meters')]
def us(doc):
    for a, b in US: doc = re.sub(a, b, doc)
    return doc
PAGES = []   # (url path, indexed?) for the sitemap and the link check
def page(path, title, desc, body, cur='', index=True, og=None, ld=(), main_cls='', preload_img=None, lang='en-US'):
    """Write one page inside the shared head, header and footer. path: '' for home, 'pricing/' or 'sample.html'."""
    url = f'{BASE}/{path}'
    og = og or '/og-image.png'
    ogdim = '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n' if og == '/og-image.png' else ''
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    robots = '' if index else '<meta name="robots" content="noindex">\n'
    pre = f'<link rel="preload" as="image" href="{preload_img}" fetchpriority="high">\n' if preload_img else ''
    doc = f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
{robots}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/bricolage-grotesque-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
{pre}<meta property="og:type" content="website">
<meta property="og:site_name" content="Iterra Maps">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{og}">
{ogdim}<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}{og}">
<meta name="theme-color" content="#0e1b24">
<link rel="stylesheet" href="{asset('/assets/site.css')}">
{lds}</head>
<body>
{header(cur)}<main id="main"{f' class="{main_cls}"' if main_cls else ''}>
{body}
</main>
{footer()}<script src="{asset('/consent.js')}" defer></script>
<script src="{asset('/assets/site.js')}" defer></script>
</body>
</html>
'''
    f = OUT + (path if path.endswith('.html') else path + 'index.html')
    os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w').write(us(doc))
    PAGES.append((path, index))

def bc_ld(items):   # items: [(name, path)]
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f'{BASE}/{u}'} for i, (n, u) in enumerate(items)]}
def faq_ld(qs): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', a)}} for q, a in qs]}
def faq_html(qs): return '\n'.join(f'      <details><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in qs)
def crumbs(items, cls='rt-crumbs'):   # [(name, path or None)], last one is the current page
    out = []
    for i, (n, u) in enumerate(items):
        last = i == len(items) - 1
        out.append(f'<span aria-current="page">{e(n)}</span>' if last else (f'<a href="/{u}">{e(n)}</a>' if u is not None else f'<span>{e(n)}</span>'))
    return f'<nav class="{cls}" aria-label="Breadcrumb">' + ' <span aria-hidden="true">›</span> '.join(out) + '</nav>'
# Films whose small web copy (wide.web.mp4 and so on) is on R2: add the folder name here, e.g. {'napa', 'charity'}, and rebuild.
WEB_READY = {'charity', 'looks'}
def video(src, label, poster_=None, aspect='wide', auto=False, main=False, thumb=None):
    if src.startswith(R2) and src[len(R2):].split('/')[0] in WEB_READY: src = src[:-4] + '.web.mp4'
    a = f' poster="{poster_}"' if poster_ else ''
    return (f'<div class="vp vp-{aspect}"><video controls muted loop playsinline preload="none"{" data-autoplay" if auto else ""}{" data-main" if main else ""}{a}'
            f'{f" data-thumb={chr(34)}{thumb}{chr(34)}" if thumb else ""} data-src="{src}" aria-label="{e(label)}"></video></div>')
def sc_card(s, h='h3'):
    return (f'<li data-kind="{s["kind"]}"><a class="card-link" href="/showcase/{s["slug"]}/"><div class="ph"><img src="{poster(s, "card")}" alt="" width="640" height="360" loading="lazy" decoding="async">'
            f'<span class="len">{s["dur"] // 60}:{s["dur"] % 60:02d}</span></div><div class="bd"><p class="k">{e(s["tag"])}</p><{h}>{e(s["name"])}</{h}><p>{e(s["blurb"])}</p></div></a></li>')
def aud_cards(h='h3'):
    return '<ul class="aud">' + ''.join(
        f'<li><a class="card-link" href="/made-for/{m["slug"]}/"><div class="ph"><img src="{poster(SC[m["film"]], "card")}" alt="" width="640" height="360" loading="lazy" decoding="async"></div>'
        f'<div class="bd"><p class="k">{e(m["name"])}</p><{h}>{e(m["h"])}</{h}><p>{e(m["p"])}</p><span class="go">{e(m["go"])}</span></div></a></li>' for m in MADEFOR) + '</ul>'
def cta_band(h='See one of your own tours as a moving map', p=PROMISE):
    return f'''<div class="cta-band"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div class="cta-row"><a class="btn btn-primary" href="/sample.html">{CTA}</a><a class="btn btn-outline" href="/pricing/">See pricing</a></div></div>'''
def more_showcases(skip):
    return '<nav class="rt-more" aria-labelledby="more-t">\n      <h2 id="more-t">More showcases</h2>\n      <ul>' + ''.join(f'<li><a href="/showcase/{s["slug"]}/">{e(s["name"])}</a></li>' for s in SHOWCASES if s['slug'] != skip) + '<li><a href="/showcase/">All films</a></li></ul>\n    </nav>'
def more_madefor(skip):
    other = [('walking holidays', 'camino-sarria-to-santiago'), ('cruises', 'alaska-inside-passage'), ('rail journeys', 'switzerland-by-rail')]
    return ('<nav class="rt-more" aria-labelledby="more-t">\n      <h2 id="more-t">Also made for</h2>\n      <ul>' + ''.join(f'<li><a href="/made-for/{m["slug"]}/">{e(m["name"])}</a></li>' for m in MADEFOR if m['slug'] != skip)
            + ''.join(f'<li><a href="/showcase/{s}/">{n.capitalize()}</a></li>' for n, s in other) + '</ul>\n    </nav>')
def fix_links(s):
    """Old page bodies used ../../ links; the new site uses addresses from the root."""
    s = s.replace('href="../../sample.html"', 'href="/sample.html"').replace('href="../../#pricing"', 'href="/pricing/"').replace('href="../../#showcase"', 'href="/showcase/"')
    s = s.replace('href="../../privacy.html"', 'href="/privacy.html"').replace('="../../media/', '="/media/').replace('href="../../showcase/', 'href="/showcase/').replace('href="../../made-for/', 'href="/made-for/')
    s = s.replace('href="../../"', 'href="/"').replace('href="./"', 'href="/"').replace('href="sample.html"', 'href="/sample.html"').replace('href="privacy.html"', 'href="/privacy.html"')
    return s
