# The cycling events page, the four new showcase pages, and the pages carried over from the live site.
from pages import *
import core, html

def shell_madefor(m, title, desc, main, faq):
    body = f'''  <div class="wrap">
    {crumbs([('Iterra Maps', ''), ('Who it’s for', 'made-for/'), (m['long'], None)])}
{main}    {more_madefor(m['slug'])}
  </div>'''
    page(f'made-for/{m["slug"]}/', title, desc, fix_links(body), cur='made-for', main_cls='rt pg', og=poster(SC[m['film']]),
         ld=[faq_ld(faq), bc_ld([('Iterra Maps', ''), ('Who it’s for', 'made-for/'), (m['long'], f'made-for/{m["slug"]}/')])])

def events():
    m = MF['cycling-events']; tx = SC['texas-hill-country-charity-ride']
    uses = [('flag', 'The route reveal', 'One video on announcement day shows the whole ride, town by town.'),
            ('page', 'The sign-up page', 'The route at the top of the registration page, so riders see what they are signing up for.'),
            ('mail', 'Rider emails', "A looping GIF in the countdown emails, and a clip of tomorrow's ride the night before."),
            ('phone', 'The social countdown', 'A vertical clip for each day, ready for Reels and Stories in the weeks before the ride.'),
            ('users', 'Sponsor packages', 'A place on screen is something concrete to offer a sponsor, and they can share the video too.'),
            ('screen', 'Host towns and volunteers', 'Overnight towns, rest-stop crews and local press can see exactly where the ride passes.')]
    feats = [('flag', 'Rest stops and lunch stops', "Each stop gets a card with its mile marker and what's there: water, food, mechanics."),
             ('users', 'Sponsors on screen', 'One sponsor at a time in the corner while the route plays, then all of them together on the end card. Each logo sits on a white tile, so it reads on any map.'),
             ('mountain', 'The climbing, mile by mile', 'An elevation profile fills along the bottom as the riders go, with the total climbed so far.'),
             ('calendar', 'A clip for each day', "A 10 to 20 second vertical clip of each day's route, for the countdown and the morning of the ride."),
             ('branch', 'Each day in its own colour', 'With a small key in the corner, so nobody mixes the days up.'),
             ('page', 'The overnight on its own card', "The overnight town closes the day with the day's miles and what's waiting there."),
             ('route', 'From your route files', 'Send a GPX or Ride with GPS file for each day. The line follows the roads your riders will use.'),
             ('palette', "Your event's brand", 'Your colours, logo and type, on a map styled to match.')]
    faq = [("Our route isn't final yet. Can you start?", "Yes. We can make the sample from last year's route and build the real one as soon as the new route is set. If a day changes after delivery, we remake the videos it affects at half their price."),
           ('Can our sponsors appear in the video?', 'Yes. Send us their logos. Each sponsor gets a few seconds in the corner while the route plays, and a place on the end card with the others.'),
           ('Do you work from Ride with GPS or GPX files?', 'Yes, either. A route file for each day gives the most exact line. Without one, we follow the real roads between your stops.'),
           ('How many videos does an event need?', 'Most rides start with one route video for the reveal. Multi-day rides usually add a short clip for each day.'),
           ('What does it cost?', f"A route video is {usd('$179', '€169')}. Short clips of one day are {usd('$79', '€79')} each, or {usd('$69', '€69')} each when you order five or more. A seven-day ride with one route video and seven daily clips comes to {usd('$662', '€652')}."),
           ('How long are the videos?', 'Usually 60 to 90 seconds for the whole route, and 10 to 20 seconds for each day clip.'),
           ('Can we keep the route under wraps until the reveal?', 'Yes. We send you the files and you decide when they go out. We don’t publish your video anywhere.')]
    days = [(1, 'Grand Haven to Pentwater'), (2, 'Pentwater to Manistee'), (3, 'Manistee to Glen Arbor')]
    problem = f'''        <h2 id="why-t">A route announcement is a list of towns. Riders want to see the ride.</h2>
        <div class="pg-compare">
          <figure class="pg-before">
            <figcaption>What they read now</figcaption>
            <div class="pg-itin" aria-label="A typical route announcement: a list of days, towns and distances">{itin([(1, 88, 60), (2, 94, 72), (3, 82, 50), (4, 90, 66), (5, 86, 58)])}<div class="pg-itin-more">… and a PDF of cue sheets</div></div>
          </figure>
          <figure class="pg-after">
            <figcaption>What they see with a map</figcaption>
            <button type="button" class="pg-after-btn" data-at="0" aria-label="Play the charity ride video from the start"><img src="{poster(tx)}" alt="" width="1280" height="720" loading="lazy"><span class="pg-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.5v13l10.5-6.5z" fill="currentColor"/></svg></span></button>
          </figure>
        </div>
        <p class="pg-text">A list of towns and mileages tells riders how far, but not what the days feel like. A one-minute map shows each day on the real roads, where the rest stops fall and how much climbing is coming, so riders sign up knowing what they are in for, and your sponsors are in front of every one of them.</p>'''
    uses_html = f'''        <h2 id="uses-t">One route, from announcement day to the start line</h2>
        <ul class="pg-grid">{''.join(f'<li class="pg-card"><h3>{ico(i, n % 3)}{e(t)}</h3><p>{e(d)}</p></li>' for n, (i, t, d) in enumerate(uses))}</ul>'''
    feats_html = f'''        <h2 id="feats-t">Yes. It’s built around the way rides run.</h2>
        <ul class="pg-feats">{''.join(f'<li>{ico(i)}<strong>{e(t)}</strong><span>{e(d)}</span></li>' for i, t, d in feats)}</ul>'''
    daily = f'''        <h2 id="days-t">A short clip for each day</h2>
        <p class="pg-intro">Each day gets its own 10 to 20 second vertical clip: the day’s towns, miles and roads, ready to post. These are the first three days of the Lakeshore 330, a made-up six-day ride.</p>
        <div class="sc-days" style="max-width:640px">{''.join(f'<figure class="sc-day">{video(R2 + f"events/day-{n}.mp4", f"Day {n}: {t}", None, "tall", thumb=6)}<figcaption>Day {n} · {e(t)}</figcaption></figure>' for n, t in days)}</div>
        <p class="pg-text" style="margin-top:18px"><a href="/showcase/lakeshore-330/">See the route video and all six daily clips</a></p>'''
    shapes = f'''        <div class="rt-shapes">
          <div class="rt-shapes-text">
            <h2 id="shapes-t">No. Every video comes in every shape.</h2>
            <p>Widescreen for the event page, vertical for Reels and Stories, and square for feeds and email, up to 4K. We add an animated GIF for rider and sponsor emails too.</p>
          </div>
          <figure class="rt-shape rt-shape-tall">{video(R2 + 'charity/vertical.mp4', 'The charity ride, vertical version', poster(tx, 'vertical'), 'tall')}<figcaption>Vertical 9:16 · Reels, Stories</figcaption></figure>
          <figure class="rt-shape rt-shape-sq">{video(R2 + 'charity/square.mp4', 'The charity ride, square version', poster(tx, 'square'), 'sq')}<figcaption>Square 1:1 · Feeds and email</figcaption></figure>
        </div>'''
    steps = '''        <h2 id="how-t">Less than you’d think, and the first one is free</h2>
        <ol class="pg-steps">
          <li><strong>Send us a route</strong><span>A GPX or Ride with GPS file for each day is ideal. Last year’s route is fine if this year’s isn’t final.</span></li>
          <li><strong>Get a free sample</strong><span>Made in your colours, usually within 2 to 3 working days.</span></li>
          <li><strong>Order the set</strong><span>The route video and a clip for each day, in every shape, with a round of changes included.</span></li>
        </ol>'''
    faq_block = f'''        <h2 id="faq-t">Questions ride organisers ask</h2>
        <div class="pg-faq">{chr(10).join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q, a in faq)}</div>'''
    main = f'''    <header class="rt-head">
      <p class="eyebrow">For cycling events and charity rides</p>
      <h1>One video for the route reveal. One clip a day for the countdown.</h1>
      <p class="lead">A short animated map of your ride on the real roads, with every rest stop, lunch stop and overnight town, the climbing, and your sponsors on screen. For your event page, rider emails and social media.</p>
      <div class="rt-head-cta"><a class="btn btn-primary" href="/sample.html">{CTA}</a><span>Send one route file or link. We’ll send a sample in your colours.</span></div>
    </header>
    <figure class="rt-video">
      {video(R2 + 'charity/wide.mp4', 'Animated route map: a two-day charity ride in the Texas Hill Country', poster(tx), auto=True, main=True)}
      <figcaption>A two-day charity ride through the Texas Hill Country: 129 miles from Dripping Springs to Comfort, with rest stops, lunch stops, the overnight and sponsors on screen. The ride and its sponsors are made up for this example. <a href="/showcase/texas-hill-country-charity-ride/">See everything in this video</a></figcaption>
    </figure>
{journey(
  bridge("Why a moving map, and not just a route page?"),
  stop('01', 'The problem', 'why-t', problem),
  bridge("That works on announcement day. Where else does it earn its keep?"),
  stop('02', 'Where it works', 'uses-t', uses_html, 'pg-tint'),
  bridge("Rides have rest stops, sponsors and big climbing days. Can one map show all that?"),
  stop('03', 'Made for rides', 'feats-t', feats_html, 'pg-ink'),
  bridge("And for a ride that lasts a week?"),
  stop('04', 'Daily clips', 'days-t', daily),
  bridge("Your event page is widescreen, but Instagram is vertical. Do you need a different video for each?"),
  stop('05', 'Every shape', 'shapes-t', shapes, 'pg-sea'),
  bridge("So what does it take to get one for your own ride?"),
  stop('06', 'Getting started', 'how-t', steps),
  bridge("Still weighing it up? These may help."),
  stop('07', 'Questions', 'faq-t', faq_block),
  bridge("Ready to see your own route ridden?"),
  dest('Your free sample', 'See your own ride as a moving map', "Send us last year's route or this year's, as a file or a link. We'll map part of it in your colours and send you the video, free and with no obligation."),
)}'''
    shell_madefor(m, 'Animated route maps for cycling events and charity rides · Iterra Maps',
        'Route reveal videos and daily clips for multi-day rides and charity rides: every rest stop and overnight on the real roads, with sponsor logos on screen, in widescreen, vertical and square.', main, faq)

# ---------------------------------------------------------------- new showcase pages (films already on R2)
def showcase_page(slug, crumb, title, desc, eyebrow, h1, lead, caption, in_title, in_cards, shapes_text, send, upload='2026-11-01', extra=''):
    s = SC[slug]; k = s['key']; mf = MF.get(s['mf']) if s['mf'] else None
    has_shapes = k in ('coach', 'cruise', 'rail', 'napa', 'charity')
    shapes = ''
    if has_shapes:
        shapes = bridge("That's the widescreen version. What about phones and feeds?") + stop('02', 'Every shape', 'shapes-t', f'''        <div class="rt-shapes">
          <div class="rt-shapes-text">
            <h2 id="shapes-t">The same route, in every shape</h2>
            <p>{e(shapes_text)}</p>
          </div>
          <figure class="rt-shape rt-shape-tall">{video(R2 + k + '/vertical.mp4', 'Vertical version', None, 'tall', thumb=20)}<figcaption>Vertical 9:16</figcaption></figure>
          <figure class="rt-shape rt-shape-sq">{video(R2 + k + '/square.mp4', 'Square version', None, 'sq', thumb=20)}<figcaption>Square 1:1</figcaption></figure>
        </div>''', 'pg-sea')
    n = 3 if has_shapes or extra else 2
    aud = (f'<p class="pg-text" style="margin-top:14px">Run trips like this? <a href="/made-for/{mf["slug"]}/">See how the videos work for {e(mf["long"].lower())}</a>.</p>' if mf else '')
    main = journey(
      bridge(f"That's {s['dur']} seconds. So what's in them?"),
      stop('01', 'Look closer', 'in-t', f'        <h2 id="in-t">{e(in_title)}</h2>\n        ' + cards(in_cards)),
      extra, shapes,
      bridge('So what would it take to make one of yours?'),
      stop(f'{n:02d}', 'What it takes', 'from-t', f'''        <div class="pg-split">
          <div>
            <h2 id="from-t">One itinerary is enough to start.</h2>
            <p>We work out the route on the real roads and trails ourselves, check the distances, and build the video in your brand. The first sample is free.</p>{aud}
          </div>
          <div>
            <h3>What you'd send us</h3>
            <ul>{''.join(f'<li>{e(x)}</li>' for x in send)}</ul>
          </div>
        </div>''', 'pg-tint'),
      bridge("Then let's try one of yours."),
      dest('Your free sample', 'Your route, in motion', "Send us one of your itineraries and we'll make a sample free, in your colours and with your logo."))
    body = f'''  <div class="wrap">
    {crumbs([('Iterra Maps', ''), ('Showcase', 'showcase/'), (crumb, None)])}
    <header class="rt-head">
      <p class="eyebrow">{e(eyebrow)}</p>
      <h1>{e(h1)}</h1>
      <p class="lead">{e(lead)}</p>
      <div class="rt-head-cta"><a class="btn btn-primary" href="/sample.html">{CTA}</a><span>Send one tour link. We'll send a sample in your colours.</span></div>
    </header>
    <div class="pg-player">
      <figure class="rt-video">
        {video(R2 + k + '/wide.mp4', 'Animated route map: ' + crumb, poster(s), auto=True, main=True)}
        <figcaption>{e(caption)}</figcaption>
      </figure>
    </div>
{main}    {more_showcases(slug)}
  </div>'''
    vid = {"@context": "https://schema.org", "@type": "VideoObject", "name": h1, "description": desc, "thumbnailUrl": [BASE + poster(s)], "uploadDate": upload,
           "duration": f"PT{s['dur'] // 60}M{s['dur'] % 60}S", "contentUrl": f"{R2}{k}/wide.mp4", "publisher": {"@type": "Organization", "name": "Iterra Maps", "url": BASE + "/"}}
    page(f'showcase/{slug}/', title, desc, fix_links(body), cur='showcase', main_cls='rt pg', og=poster(s), ld=[vid, bc_ld([('Iterra Maps', ''), ('Showcase', 'showcase/'), (crumb, f'showcase/{slug}/')])])

def new_showcases(dates):
    showcase_page('canadian-rockies-by-coach', 'The Canadian Rockies by coach',
      'Canadian Rockies coach tour: animated route map showcase · Iterra Maps',
      'An animated route map of a seven-night coach tour through the Canadian Rockies, from Calgary through Banff, Lake Louise and the Icefields Parkway to Jasper, with a card for each day.',
      'Showcase · Coach tour', 'A week in the Canadian Rockies by coach',
      'Seven nights from Calgary through Banff, Lake Louise, the Icefields Parkway and Jasper, on the real highways, with a card for each day. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 25 seconds. Tamarack & Pine Coachways is a made-up brand for this example.',
      "What's packed into this video", [
        ('route', 'The real highways', 'The coach follows the actual roads between each overnight town, not a straight line across the map.'),
        ('page', 'A card for each day', "Each day gets a card with the hotel, meals and highlights from the itinerary, in the tour company's own words."),
        ('mountain', 'Shaded mountains', 'The Rockies are drawn in shaded relief, so the scale of the landscape lands at a glance.'),
        ('gauge', 'A distance counter', 'The counter adds up the distance as the coach goes, so the size of each day is clear.'),
        ('palette', "The tour company's brand", 'Colours, type and a coach icon for a made-up company, Tamarack & Pine Coachways.'),
        ('phone', 'Every shape', 'Widescreen for the tour page, vertical for Reels and square for Facebook and email.')],
      'One tour gives you the full set: widescreen for the tour page and brochure QR codes, vertical for Reels and Stories, and square for Facebook and email.',
      ['A link to the tour on your website, or the day-by-day itinerary', 'The hotels and highlights you want on each day’s card', 'Your logo, and your brand colours if you have them'], dates.get('coach', '2026-11-01'))
    days = [(1, 'Grand Haven to Pentwater'), (2, 'Pentwater to Manistee'), (3, 'Manistee to Glen Arbor'), (4, 'Glen Arbor to Traverse City'), (5, 'Traverse City to Charlevoix'), (6, 'Charlevoix to Mackinaw City')]
    daily = bridge('And the six daily clips?') + stop('02', 'Daily clips', 'days-t', f'''        <h2 id="days-t">One 12-second clip for each day</h2>
        <p class="pg-intro">Each clip shows one day’s towns and roads in vertical 9:16, ready for Reels, Stories and the rider email the night before.</p>
        <div class="sc-days six">{''.join(f'<figure class="sc-day">{video(R2 + f"events/day-{n}.mp4", f"Day {n}: {t}", None, "tall", thumb=6)}<figcaption>Day {n} · {e(t)}</figcaption></figure>' for n, t in days)}</div>''')
    showcase_page('lakeshore-330', 'The Lakeshore 330',
      'Multi-day bike ride: route video and daily clips showcase · Iterra Maps',
      'An animated route map of a six-day bike ride along the Lake Michigan shore from Grand Haven to Mackinaw City: one route video for the reveal and a short vertical clip for each day.',
      'Showcase · Multi-day ride', 'The Lakeshore 330: a route video and six daily clips',
      'A six-day ride up the Lake Michigan shore from Grand Haven to Mackinaw City. One video shows the whole route for the reveal. Six short vertical clips show one day each for the countdown.',
      'The route video, widescreen 16:9, 1 minute 14 seconds. The Lakeshore 330 is a made-up ride for this example.',
      'What an event gets', [
        ('flag', 'A route video for the reveal', 'The whole ride in about a minute, town by town, for announcement day and the event page.'),
        ('calendar', 'A clip for each day', 'Six vertical clips of 12 seconds each, one per day, for the social countdown.'),
        ('route', 'The real roads', "Each day's towns and roads are clear before anyone clips in."),
        ('users', 'Made to be shared', 'Riders share them, and sponsors get seen.')],
      '', ['A GPX or Ride with GPS file for each day, or last year’s route', 'The overnight towns and rest stops', 'Your logo, your colours and your sponsors’ logos'], dates.get('events', '2026-11-01'), extra=daily)
    showcase_page('switzerland-by-rail', 'Switzerland by rail',
      'Switzerland by rail: animated route map showcase · Iterra Maps',
      'An animated route map of an eight-day rail journey across Switzerland from Zurich to Tirano, on four famous trains including the Glacier Express and the Bernina Express.',
      'Showcase · Rail journey', 'Switzerland by rail: four famous trains, one journey',
      'Eight days from Zurich to Tirano on four famous trains, including the Glacier Express and the Bernina Express, in a look as polished as the trip. Watch it first, then see what a rail video can show.',
      'Widescreen 16:9, 1 minute 25 seconds. Alpine Line Rail Journeys is a made-up brand for this example.',
      'What a rail journey video can show', [
        ('route', 'The map follows the trains', 'Rail, ferries, flights and roads: whatever your clients travel on, the route follows it.'),
        ('page', 'A card for each stop', 'Each overnight town can carry a card with its nights, hotel and highlights.'),
        ('mountain', 'The mountains', 'Shaded relief shows the passes and valleys the line runs through.'),
        ('palette', 'A look to match the trip', 'Colours, type and map style set to suit a premium journey, or to match your brand.')],
      'One journey gives you the full set: widescreen for the tour page, vertical for Reels and Stories, and square for feeds and email.',
      ['A link to the journey on your website, or the day-by-day itinerary', 'The trains, hotels and highlights you want named', 'Your logo, and your brand colours if you have them'], dates.get('rail', '2026-11-01'))
    showcase_page('camino-sarria-to-santiago', 'The Camino, Sarria to Santiago',
      'Camino de Santiago from Sarria: animated route map showcase · Iterra Maps',
      'An animated route map of the last five stages of the Camino Francés on foot, about 115 km (71 miles) from Sarria to Santiago de Compostela.',
      'Showcase · Walking holiday', 'The Camino from Sarria to Santiago, stage by stage',
      'The last five stages of the Camino Francés on foot: about 115 km (71 miles) from Sarria to Santiago de Compostela. Watch it first, then see what a walking video can show.',
      'Widescreen 16:9, 1 minute 23 seconds. The tour brand in the video is made up for this example.',
      'What a walking video can show', [
        ('route', 'The trail itself', 'For waymarked trails we follow the walking route, not the nearest road. A GPX file gives the most exact line.'),
        ('page', 'A card for each stage', "Each night's town can carry a card with the distance walked and what's there."),
        ('mountain', 'The climbs', 'An elevation profile can run along the bottom, so walkers see the hills before they book.'),
        ('lock', 'Your level of detail', 'Show the exact trail, a simplified line or simple curves from town to town.')],
      '', ['A link to the holiday on your website, or the stage-by-stage itinerary', 'GPX files of the stages, if you have them', 'Your logo, and your brand colours if you have them'], dates.get('walking', '2026-11-01'))

# ---------------------------------------------------------------- pages carried over from the live site
def carry(path, cur, kind):
    """Take a live page's <main> and put it in the new shell: new header, footer, links and index pages."""
    s = open(LEG + path + 'index.html').read()
    title = re.search(r'<title>(.*?)</title>', s, re.S).group(1); desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    og = re.search(r'<meta property="og:image" content="https://iterramaps.com([^"]*)"', s).group(1)
    lds = [json.loads(x) for x in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', s, re.S)]
    lds = [x for x in lds if x.get('@type') != 'BreadcrumbList']
    main = re.search(r'<main id="main"[^>]*>(.*)</main>', s, re.S).group(1)
    slug = path.strip('/').split('/')[1]
    if kind == 'showcase':
        sc = SC[slug]
        main = re.sub(r'<nav class="rt-crumbs".*?</nav>', lambda m: crumbs([('Iterra Maps', ''), ('Showcase', 'showcase/'), (re.search(r'aria-current="page">(.*?)</span>', m.group(0)).group(1), None)]).replace('&amp;', '&'), main, count=1, flags=re.S)
        main = re.sub(r'<nav class="rt-more".*?</nav>', lambda m: more_showcases(slug), main, count=1, flags=re.S)
        bc = bc_ld([('Iterra Maps', ''), ('Showcase', 'showcase/'), (sc['name'], path)])
    else:
        mf = MF[slug]
        main = re.sub(r'<nav class="rt-crumbs".*?</nav>', lambda m: crumbs([('Iterra Maps', ''), ('Who it’s for', 'made-for/'), (mf['long'], None)]), main, count=1, flags=re.S)
        main = re.sub(r'<nav class="rt-more".*?</nav>', lambda m: more_madefor(slug), main, count=1, flags=re.S)
        bc = bc_ld([('Iterra Maps', ''), ('Who it’s for', 'made-for/'), (mf['long'], path)])
        # one answer about route changes, the same on every page
        old = 'Send us the new GPX file or itinerary and we update the video from it.'
        old2 = 'Send us the new itinerary and we update the video from it.'
        for o in (old, old2):
            main = main.replace(o, CHANGE)
            for x in lds:
                if x.get('@type') == 'FAQPage':
                    for q in x['mainEntity']:
                        if q['acceptedAnswer']['text'] == o: q['acceptedAnswer']['text'] = CHANGE
    main = fix_links(main)
    # a GIF that hasn't been made yet: leave its tile out so the row closes up
    for g in re.findall(r'<figure class="pg-gif">.*?</figure>', main, re.S):
        src = re.search(r'src="/([^"]+)"', g).group(1)
        if not os.path.exists(OUT + src): main = main.replace(g, '').replace('rt-shapes pg-shapes4', 'rt-shapes', 1)
    # the looks page: a still from each look as its poster
    for k in ('wine', 'relief', 'vintage', 'midnight', 'relief-vertical'):
        main = main.replace(f'src="{R2}looks/{k}.mp4', f'poster="/media/showcase/looks-{k}.jpg" src="{R2}looks/{k}.mp4')
    # the main film is marked so the "jump to" buttons find it; videos load only when needed
    main = main.replace('data-autoplay poster=', 'data-autoplay data-main poster=', 1)
    main = re.sub(r'(<video[^>]*?) preload="metadata"([^>]*?) src="', r'\1 preload="none"\2 data-src="', main)
    main = re.sub(r'data-src="([^"#]+)#t=([\d.]+)"', r'data-thumb="\2" data-src="\1"', main)
    main = re.sub(r'data-src="' + re.escape(R2) + r'([a-z]+)/([a-z0-9-]+)\.mp4"', lambda m: f'data-src="{R2}{m.group(1)}/{m.group(2)}{".web" if m.group(1) in core.WEB_READY else ""}.mp4"', main)
    page(path, html.unescape(title), html.unescape(desc), main, cur=cur, main_cls='rt pg', og=og, ld=lds + [bc])

def carry_privacy():
    s = open(LEG + 'privacy.html').read()
    main = re.search(r'<main[^>]*>(.*)</main>', s, re.S).group(1)
    page('privacy.html', 'Privacy notice · Iterra Maps', re.search(r'<meta name="description" content="([^"]*)"', s).group(1), fix_links(main), main_cls='wrap')
