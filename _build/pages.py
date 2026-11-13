# Page bodies for the new and rebuilt pages.
from core import *
exec(open(LEG + 'helpers.py').read().split('MADE_FOR =')[0].replace("SITE = '/home/claude/site-work/'", "SITE = LEG"))   # journey helpers: ico, ICONS, bridge, stop, dest, journey, itin
ICONS['gauge'] = '<path d="M4 12a8 8 0 1 1 16 0"/><path d="m12 12 4-4"/><path d="M8 18h8"/>'
ICONS['flag'] = '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'
def cards(items): return '<ul class="pg-grid">' + ''.join(f'<li class="pg-card"><h3>{ico(k, i % 3)}{e(h)}</h3><p>{e(p)}</p></li>' for i, (k, h, p) in enumerate(items)) + '</ul>'
usd = lambda u, eu: f'<span data-usd="{u}" data-eur="{eu}">{u}</span>'

FEATURES = '''<ul class="features">
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 18c4 0 4-6 8-6s4-6 8-6"/><circle cx="3" cy="18" r="1.5"/><circle cx="19" cy="6" r="1.5"/></svg><h3>Real roads and trails</h3><p>Routes follow the actual roads, or the walking or cycling trail itself, from your GPX file.</p></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 17h18l-2 4H5z"/><path d="M12 3v11M12 3l6 8h-6"/></svg><h3>Ferries and trains, automatically</h3><p>When the journey crosses water or goes through a tunnel, the car becomes a ferry or a train by itself.</p></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 20l7-12 4 6 3-4 6 10z"/></svg><h3>Mountains in 3D</h3><p>Shaded relief, contour lines and a live elevation profile, so walkers and cyclists see the climb.</p></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9h6M7 13h10"/></svg><h3>Your brand on every frame</h3><p>Your logo, colours, font and icons, saved as your house style so every video matches.</p></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="8" height="14" rx="1.5"/><rect x="13" y="5" width="8" height="14" rx="1.5"/></svg><h3>Multi-day chapters</h3><p>Long tours split into days or regions, with smooth fly-overs or push transitions between them.</p></li>
        <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="7" width="12" height="9" rx="1.5"/><rect x="16" y="4" width="6" height="12" rx="1.5"/><rect x="9" y="17" width="5" height="5" rx="1"/></svg><h3>Every format</h3><p>Widescreen, vertical and square versions, up to 4K, plus a still poster image for brochures and email.</p></li>
      </ul>'''
NEED = '''<div class="need">
        <h3>What we need from you</h3>
        <ul>
          <li>The route: a GPX or Ride with GPS file, a tour page link, or a list of stops in order</li>
          <li>Your logo, ideally a PNG with a transparent background or an SVG</li>
          <li>Your brand colours, or we can take them from your website</li>
          <li>The date you need the videos by</li>
          <li>Anything you’d like on each stop’s card: nights, distances, climbing, highlights</li>
          <li>Optional: one photo per stop, that you own or have the rights to use</li>
        </ul>
      </div>'''
STEPS = '''<ol class="steps steps4">
        <li><h3>You send the route</h3><p>A GPX or Ride with GPS file, a link to the tour page, or just a list of stops, with your logo and deadline.</p></li>
        <li><h3>We build it</h3><p>A first version within 5 working days, on the real roads and trails, in your colours.</p></li>
        <li><h3>You review</h3><p>Ask for changes to timing, labels, colours or the camera. One round is included.</p></li>
        <li><h3>We deliver</h3><p>MP4s in widescreen, vertical and square, up to 4K, ready to post anywhere.</p></li>
      </ol>'''
MAILQ = 'mailto:hello@iterramaps.com?subject=' + 'Quote%20for%20a%20set%20of%20route%20videos'
def plans(h='h3'):
    return f'''<div class="plans">
        <div class="plan">
          <{h}>One video</{h}>
          <p class="price"><b>{usd('$179', '€169')}</b><span>per route video</span></p>
          <ul><li>The whole route, up to 90 seconds</li><li>Up to 12 stops</li><li>Widescreen, vertical and square, up to 4K</li><li>One round of changes</li><li>First version within 5 working days</li></ul>
          <a class="btn btn-outline" href="/sample.html">Start with a free sample</a>
        </div>
        <div class="plan featured">
          <span class="badge">{usd('Save $20 a video', 'Save €20 a video')}</span>
          <{h}>5 or more</{h}>
          <p class="price"><b>{usd('$159', '€149')}</b><span>per video</span></p>
          <ul><li>For a set of tours, or an event’s route and daily clips</li><li>Everything in one video, for each of them</li><li>All in one matching style</li><li>Seven videos? {usd('7 × $159 = $1,113', '7 × €149 = €1,043')}</li></ul>
          <a class="btn btn-light" href="{MAILQ}">Email us for a quote</a>
        </div>
        <div class="plan">
          <span class="badge">{usd('Save $40 a video', 'Save €40 a video')}</span>
          <{h}>20 or more</{h}>
          <p class="price"><b>{usd('$139', '€129')}</b><span>per video</span></p>
          <ul><li>For a whole brochure or programme</li><li>Everything in one video, for each of them</li><li>All in one matching style</li><li>If 20 would cost less than your order, we make you 20 for that price</li></ul>
          <a class="btn btn-outline" href="{MAILQ}">Email us for a quote</a>
        </div>
      </div>'''
CUR = '<div class="cur-switch" role="group" aria-label="Show prices in"><button type="button" class="js-cur" data-cur="usd" aria-pressed="true">$ USD</button><button type="button" class="js-cur" data-cur="eur" aria-pressed="false">€ EUR</button></div>'
EXTRAS = f'''<div class="extras">
        <h2 class="plans-head" id="extras-t">Short clips and extras</h2>
        <table aria-labelledby="extras-t">
          <tr><th scope="row">Short clip: one day or one leg, up to 20 seconds</th><td><ul class="tiers"><li><b>{usd('$79', '€79')}</b> per clip</li><li><b>{usd('$69', '€69')}</b> per clip when you order 5 or more</li><li><b>{usd('$59', '€59')}</b> per clip when you order 20 or more</li></ul><span class="eg">For example, a clip for each day of a 7-day event: <span style="white-space:nowrap">{usd('7 × $69 = $483', '7 × €69 = €483')}</span>.</span></td></tr>
          <tr><th scope="row">Extra stops, over 12 on a route</th><td>+{usd('$19', '€19')} per stop</td></tr>
          <tr><th scope="row">Longer than 90 seconds</th><td>+{usd('$69', '€69')} per extra minute</td></tr>
          <tr><th scope="row">Clean version, without the small Iterra Maps mark</th><td>+{usd('$29', '€29')} per video</td></tr>
          <tr><th scope="row">Route changed after delivery</th><td>Half the video’s price to remake it</td></tr>
        </table>
      </div>'''
Q = dict(
 need=('What do you need from us?', 'Just the route: a GPX or Ride with GPS file, a link, a PDF or a list of stops. For walking and cycling, a route file gives the most exact line; for waymarked trails we can usually find the official route ourselves. Send your logo (ideally a transparent PNG or an SVG), your brand colours and your deadline. If you’d like a photo on each stop’s card, send one per stop that you own or have the rights to use.'),
 time=('How long does it take?', 'A free sample usually takes 2 to 3 working days. For a full video, you get a first version within 5 working days of sending the route, for up to five videos. For bigger orders we agree a schedule with you. Need it sooner? Ask, and we’ll tell you honestly whether we can.'),
 brand=('Can it match our brand?', 'Yes. Route colours, map style, font, panel colours, your logo and your own vehicle icons can all be set to match, and they’re saved as your house style for every future video.'),
 site=('How do we put the video on our website?', 'You get MP4 files in widescreen, vertical and square. They upload to your website, YouTube, Instagram or an email tool like any other video. If someone else looks after your website, we’re happy to answer their questions.'),
 private=('Can we keep our routes private?', 'Yes. You choose how much the line shows: the exact roads, a simplified line, or simple curves from town to town. The distances and timing stay true whichever you pick.'),
 own=('Who owns the videos?', 'You can use them in your own marketing, on any channel, for as long as you like. The map data credit (© OpenStreetMap contributors) stays in the corner, as the map licence requires.'),
 sound=('Is there music or a voice-over?', 'Videos are delivered silent, so they autoplay anywhere, including on your website. You can add your own track if you want one.'),
 change=('What if the route changes?', 'Send the new file. Your route and style are saved, so we remake the videos it affects at half their price.'),
 mark=('What is the small Iterra Maps mark?', f'Each video carries a small, semi-transparent Iterra Maps mark in one corner. If you’d rather have it without, a clean version is {usd("$29", "€29")} per video.'),
 incl=('What does one video include?', 'The whole route in a video of up to 90 seconds with up to 12 stops, in widescreen, vertical and square, up to 4K, in your logo and colours, with one round of changes.'),
 clip=('What is a short clip?', 'A video of one day or one leg, up to 20 seconds. Events use them for a daily countdown; tour companies use them for single days and signature climbs.'),
 sample=('Is the sample really free?', 'Yes. Send one tour link and we make a 15-second sample of part of the route in your colours. There is no cost and no obligation to order.'),
)

# ---------------------------------------------------------------- home
def home():
    faq = [Q[k] for k in ('need', 'time', 'brand', 'site', 'private', 'own', 'sound', 'change', 'mark')]
    napa, tx = SC['napa-and-sonoma-by-bike'], SC['texas-hill-country-charity-ride']
    body = f'''  <section class="hero2" aria-labelledby="hero-title">
    <div class="wrap">
      <div class="hero2-top">
        <p class="eyebrow">Animated route map videos for tour operators and events</p>
        <h1 id="hero-title">Show the route before they book.</h1>
      </div>
      <figure class="hero2-visual">
        {video(R2 + 'napa/wide.mp4', 'Animated route map: five days by bike in Napa and Sonoma', poster(napa), auto=True)}
        <figcaption>Napa and Sonoma by bike, five days. The tour brand in the video is made up. <a href="/showcase/napa-and-sonoma-by-bike/">See what’s in this video</a></figcaption>
      </figure>
      <div class="hero2-rest">
        <p class="lead">We turn your itinerary into a short animated map video. The route draws itself along the real roads, day by day, with your stops, your logo and your colours. Ready for your tour page, Reels and emails.</p>
        <div class="cta-row"><a class="btn btn-primary" href="/sample.html">{CTA}</a><a class="btn btn-outline" href="/showcase/">See the showcase</a></div>
        <p class="promise">{PROMISE}</p>
        <p class="facts"><span>From {usd('$179', '€169')} per route video</span><span>Widescreen, vertical and square</span><span>First version in 5 working days</span></p>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0" aria-labelledby="who-title">
    <div class="wrap">
      <div class="sec-head"><p class="eyebrow">Who it’s for</p><h2 class="h2" id="who-title">Made for the way your trips run.</h2></div>
      {aud_cards().replace('class="aud"', 'class="aud aud-compact"')}
      <p class="aud-also">Also made for <a href="/showcase/camino-sarria-to-santiago/">walking holidays</a>, <a href="/showcase/alaska-inside-passage/">cruises</a> and <a href="/showcase/switzerland-by-rail/">rail journeys</a>. <a href="/made-for/">See every kind of trip</a>.</p>
    </div>
  </section>

  <section class="sc-ch sc-ink" aria-labelledby="shape-t">
    <div class="wrap">
      <div class="sc-head">
        <div><p class="sc-kicker">One route, every shape</p><h2 class="sc-title" id="shape-t">One video for your website. The same route for Reels and email.</h2></div>
        <p class="sc-lead">Every order comes in widescreen, vertical and square, up to 4K. This one is a two-day charity ride in the Texas Hill Country: 129 miles, with every rest stop and the ride’s sponsors on screen.</p>
      </div>
      <div class="shapes3">
        <figure class="s-wide">{video(R2 + 'charity/wide.mp4', 'A two-day charity ride in the Texas Hill Country', poster(tx), auto=True)}<figcaption>16:9 · Website and YouTube</figcaption></figure>
        <figure class="s-tall">{video(R2 + 'charity/vertical.mp4', 'The charity ride, vertical version', poster(tx, 'vertical'), 'tall')}<figcaption>9:16 · Reels, Stories</figcaption></figure>
        <figure class="s-sq">{video(R2 + 'charity/square.mp4', 'The charity ride, square version', poster(tx, 'square'), 'sq')}<figcaption>1:1 · Feeds and email</figcaption></figure>
      </div>
      <div class="shapes3-foot">
        <ul class="sc-points"><li><span class="sc-num">1</span><span><strong>A card for every stop,</strong> with its mile marker and what’s there.</span></li><li><span class="sc-num">2</span><span><strong>The climbing, mile by mile,</strong> on a profile that fills as the riders go.</span></li><li><span class="sc-num">3</span><span><strong>Sponsors in the corner and on the end card,</strong> each on a white tile so any logo reads.</span></li></ul>
        <div class="row"><a class="btn btn-primary" href="/showcase/texas-hill-country-charity-ride/">See everything in this video</a><p class="sc-demo">The Cedar Hills Children’s Ride and its sponsors are made up for this example.</p></div>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="sc-title">
    <div class="wrap">
      <div class="sec-head"><p class="eyebrow">Showcase</p><h2 class="h2" id="sc-title">See it on your kind of trip.</h2><p class="lead">Eight films, each made for a different kind of travel business. The brands in them are made up. Your sample comes in your own.</p></div>
      <ul class="cards cards-compact">{''.join(sc_card(s) for s in SHOWCASES)}</ul>
      <p style="margin-top:28px"><a class="more-link" href="/showcase/">Open the showcase</a></p>
    </div>
  </section>

  <section class="section" style="padding-top:0" aria-labelledby="diff-title">
    <div class="wrap">
      <h2 class="h2" id="diff-title" style="max-width:16em">Not a stock animation. Your actual route.</h2>
      {FEATURES}
    </div>
  </section>

  <section class="band-ink" id="how" aria-labelledby="how-title">
    <div class="wrap section">
      <p class="eyebrow plain">How it works</p>
      <h2 class="h2" id="how-title" style="margin-top:10px">From your route to finished video in four steps.</h2>
      {STEPS}
      <p style="margin-top:36px"><a class="more-link" href="/how-it-works/">What we need from you, and what you get</a></p>
    </div>
  </section>

  <section class="section" id="pricing" aria-labelledby="price-title">
    <div class="wrap">
      <div class="price-head">
        <div><p class="eyebrow plain">Pricing</p><h2 class="h2" id="price-title" style="margin-top:10px">Simple pricing, per video.</h2></div>
        {CUR}
      </div>
      <p class="lead" style="margin-top:12px">You pay per video. Every video comes in widescreen, vertical and square, up to 4K, in your logo and colours.</p>
      {plans()}
      <p style="margin-top:28px"><a class="more-link" href="/pricing/">Short clips, extras and what’s included</a></p>
    </div>
  </section>

  <section class="band-route sample-band" id="contact" aria-labelledby="free-title">
    <div class="wrap">
      <div class="copy">
        <h2 id="free-title">Send one itinerary. Get a sample free.</h2>
        <p>Paste a link to any tour on your site. We reply within one working day and send a 15-second sample in your colours, usually within 2 to 3 working days. No cost, no obligation.</p>
      </div>
      <form class="form js-form" novalidate data-subject="Free sample request (home page)">
        <label class="field" for="q-url">Link to the tour page<input id="q-url" name="tour_url" type="url" placeholder="https://yourcompany.com/tours/…" required data-missing="Please paste a link to one of your tours."></label>
        <label class="field" for="q-email">Your email<input id="q-email" name="email" type="email" autocomplete="email" placeholder="you@yourcompany.com" required data-missing="Please add your email so we can send the sample."></label>
        <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
        <input type="hidden" name="from_page" value="">
        <button class="btn btn-ink" type="submit">Send my itinerary</button>
        <p class="form-status" role="status" hidden></p>
        <p class="small">We’ll only use your details to reply about the sample. <a href="/privacy.html">Privacy notice</a></p>
      </form>
    </div>
  </section>

  <section class="section" id="faq" aria-labelledby="faq-title">
    <div class="faq wrap">
      <h2 class="h2" id="faq-title" style="margin-bottom:28px">Questions</h2>
{faq_html(faq)}
    </div>
  </section>'''
    org = {"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Iterra Maps", "url": BASE + "/", "logo": BASE + "/brand/iterra-mark-512.png", "image": BASE + "/og-image.png", "email": "hello@iterramaps.com",
           "description": "Animated route map videos for tour operators, cycling events, walking and cycling holidays, coach tours, cruises and rail journeys.", "areaServed": ["US", "IE", "GB"], "priceRange": "$$",
           "address": {"@type": "PostalAddress", "addressLocality": "Dublin", "addressCountry": "IE"}}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Iterra Maps", "url": BASE + "/"}
    page('', 'Iterra Maps: animated route map videos for tour operators and events',
         'Short animated map videos of your tours and rides: the route draws itself along the real roads, day by day, in your brand. For cycling tours, events and charity rides, coach tours and more. Free sample of your own route.',
         body, cur='home', ld=[org, site, faq_ld(faq)], preload_img=poster(napa))

# ---------------------------------------------------------------- pricing
def pricing():
    faq = [Q[k] for k in ('incl', 'clip', 'sample', 'change', 'mark', 'own', 'time')]
    body = f'''  <section class="pagehead">
    <div class="wrap">
      {crumbs([('Iterra Maps', ''), ('Pricing', None)], 'crumbs')}
      <div class="price-head"><h1>Simple pricing, per video.</h1>{CUR}</div>
      <p class="lead">You pay per video. Every video comes in widescreen, vertical and square, up to 4K, in your logo and colours. The first sample is free.</p>
    </div>
  </section>
  <section class="section" style="padding-top:8px" aria-label="Prices">
    <div class="wrap">
      {plans('h2')}
      {EXTRAS}
      <p class="small" style="margin-top:18px"><span data-usd="Prices in US dollars." data-eur="Prices in euro.">Prices in US dollars.</span> You can use the videos in your own marketing, on any channel, for as long as you like.</p>
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="incl-t">
    <div class="wrap">
      <h2 class="h2" id="incl-t" style="margin-bottom:28px">Every video includes</h2>
      <ul class="incl">
        <li><span><strong>Your real route.</strong> On the actual roads and trails, from your route file or itinerary.</span></li>
        <li><span><strong>Three shapes.</strong> Widescreen 16:9, vertical 9:16 and square 1:1, up to 4K.</span></li>
        <li><span><strong>Your brand.</strong> Logo, colours, font and icons, saved as your house style.</span></li>
        <li><span><strong>Cards for your stops.</strong> Nights, distances, climbing and highlights, in your words.</span></li>
        <li><span><strong>One round of changes.</strong> Timing, labels, colours or the camera.</span></li>
        <li><span><strong>A first version in 5 working days.</strong> For up to five videos; bigger orders on an agreed schedule.</span></li>
      </ul>
      <div class="two" style="margin-top:40px">
        <div class="panel"><h3>A week-long ride</h3><ul><li>One route video for the reveal: {usd('$179', '€169')}</li><li>A clip for each of 7 days: {usd('7 × $69 = $483', '7 × €69 = €483')}</li><li><strong>Total: {usd('$662', '€652')}</strong></li></ul></div>
        <div class="panel"><h3>Five tours in one style</h3><ul><li>Five route videos: {usd('5 × $159', '5 × €149')}</li><li>Each in widescreen, vertical and square</li><li><strong>Total: {usd('$795', '€745')}</strong></li></ul></div>
      </div>
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="pfaq-t">
    <div class="faq wrap">
      <h2 class="h2" id="pfaq-t" style="margin-bottom:28px">Questions about pricing</h2>
{faq_html(faq)}
    </div>
  </section>
  <section class="section" style="padding-top:0"><div class="wrap">{cta_band('Start with a free sample of your own route')}</div></section>'''
    page('pricing/', 'Pricing: animated route map videos from $179 · Iterra Maps',
         'Animated route map videos are $179 each, $159 each for five or more and $139 each for twenty or more, in widescreen, vertical and square. Short clips from $59. The first sample is free.',
         body, cur='pricing', ld=[faq_ld(faq), bc_ld([('Iterra Maps', ''), ('Pricing', 'pricing/')])])

# ---------------------------------------------------------------- how it works
def how():
    faq = [Q[k] for k in ('need', 'time', 'site', 'private', 'change', 'sound')]
    body = f'''  <section class="pagehead">
    <div class="wrap">
      {crumbs([('Iterra Maps', ''), ('How it works', None)], 'crumbs')}
      <h1>From your route to finished video in four steps.</h1>
      <p class="lead">You send a route. We build the video on the real roads in your brand, you ask for changes, and we deliver it in every shape. It starts with a free sample.</p>
    </div>
  </section>
  <section class="band-ink" style="margin-top:clamp(32px,5vw,56px)" aria-labelledby="steps-t">
    <div class="wrap section">
      <h2 class="sr-only" id="steps-t">The four steps</h2>
      {STEPS}
      {NEED}
    </div>
  </section>
  <section class="section" aria-labelledby="get-t">
    <div class="wrap">
      <h2 class="h2" id="get-t" style="margin-bottom:28px">What you get</h2>
      <div class="two">
        <div class="panel"><h3>The files</h3><ul><li>MP4 video in widescreen 16:9, vertical 9:16 and square 1:1, up to 4K</li><li>A still poster image for brochures and email</li><li>An animated GIF for emails, on request</li><li>Silent by default, so it autoplays anywhere</li></ul></div>
        <div class="panel"><h3>Your house style</h3><ul><li>Your logo, colours, font and icons, set once</li><li>Saved, so every later video matches</li><li>Or start from one of our ready-made looks</li></ul><p style="margin-top:14px"><a class="more-link" href="/showcase/one-route-many-looks/">See one route in four looks</a></p></div>
      </div>
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="ch-title">
    <div class="wrap channels">
      <div><h2 class="h2" id="ch-title">One tour, every channel.</h2><p class="lead">Each order comes in the shapes you need, so the same journey works at the top of a tour page, in a Reel and in a newsletter.</p></div>
      <ul class="channel-grid">
        <li><b>16:9</b>Tour pages &amp; YouTube</li>
        <li><b>9:16</b>Reels, TikTok &amp; Shorts</li>
        <li><b>1:1</b>Feed posts &amp; ads</li>
        <li><b>Poster frame</b>Brochures &amp; email</li>
        <li><b>Loop</b>Trade-fair stands &amp; screens</li>
        <li><b>Pre-departure</b>“Here’s your trip” emails</li>
      </ul>
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="det-t">
    <div class="wrap">
      <h2 class="h2" id="det-t" style="margin-bottom:12px">You choose how much of the route to show.</h2>
      <p class="lead" style="margin-bottom:28px">Some routes are public. Some are worth protecting. The distances and timing stay true whichever you pick.</p>
      {cards([('route', 'The exact roads', 'The real route, turn by turn, so travellers see exactly where they will go.'), ('branch', 'A simplified line', 'The right roads in outline, without every turn.'), ('lock', 'Curves from town to town', 'A gentle curve between overnight stops, so your routing stays yours.')])}
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="hfaq-t">
    <div class="faq wrap">
      <h2 class="h2" id="hfaq-t" style="margin-bottom:28px">Questions</h2>
{faq_html(faq)}
    </div>
  </section>
  <section class="section" style="padding-top:0"><div class="wrap">{cta_band()}</div></section>'''
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": "How an animated route map video is made", "step": [
        {"@type": "HowToStep", "name": "You send the route", "text": "A GPX or Ride with GPS file, a link to the tour page, or a list of stops, with your logo and deadline."},
        {"@type": "HowToStep", "name": "We build it", "text": "A first version within 5 working days, on the real roads and trails, in your colours."},
        {"@type": "HowToStep", "name": "You review", "text": "Ask for changes to timing, labels, colours or the camera. One round is included."},
        {"@type": "HowToStep", "name": "We deliver", "text": "MP4s in widescreen, vertical and square, up to 4K."}]}
    page('how-it-works/', 'How it works: from your route to a finished map video · Iterra Maps',
         'How we make an animated route map video: you send the route and your logo, we build it on the real roads in your brand, you review it, and we deliver it in widescreen, vertical and square.',
         body, cur='how', ld=[howto, faq_ld(faq), bc_ld([('Iterra Maps', ''), ('How it works', 'how-it-works/')])])

# ---------------------------------------------------------------- free sample
def sample():
    body = f'''  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">Free sample</p>
      <h1>Show us one of your tours.</h1>
      <p class="lead">Tell us which itinerary to animate and we’ll send you a 15-second sample in your colours. No cost, no obligation.</p>
    </div>
    <form class="form js-form" novalidate data-subject="Free sample request">
      <label class="field" for="s-name">Your name<input id="s-name" name="name" type="text" autocomplete="name" required data-missing="Please tell us your name."></label>
      <label class="field" for="s-email">Work email<input id="s-email" name="email" type="email" autocomplete="email" required data-missing="Please add your email so we can send the sample."></label>
      <label class="field" for="s-url">Link to the tour page <small>No link? Describe the route in a line or two instead.</small><input id="s-url" name="tour_url" type="text" inputmode="url" placeholder="https://yourcompany.com/tours/…" required data-missing="Please paste a link to the tour, or describe the route."></label>
      <button class="btn btn-primary" type="submit">Send my itinerary</button>
      <p class="form-status" role="status" hidden></p>
      <details class="opt">
        <summary>Add details (optional)</summary>
        <div>
          <label class="field" for="s-company">Company<input id="s-company" name="company" type="text" autocomplete="organization"></label>
          <fieldset>
            <legend>How do your guests travel?</legend>
            <div class="pills">
              <label><input type="checkbox" name="travel" value="Cycling"> Cycling</label>
              <label><input type="checkbox" name="travel" value="Walking"> Walking</label>
              <label><input type="checkbox" name="travel" value="Coach or car"> Coach or car</label>
              <label><input type="checkbox" name="travel" value="Ferry or cruise"> Ferry or cruise</label>
              <label><input type="checkbox" name="travel" value="Rail"> Rail</label>
              <label><input type="checkbox" name="travel" value="Flights"> Flights</label>
            </div>
          </fieldset>
          <fieldset>
            <legend>Where will you use it?</legend>
            <div class="pills">
              <label><input type="checkbox" name="formats" value="Website (16:9)" checked> Website (16:9)</label>
              <label><input type="checkbox" name="formats" value="Reels / TikTok (9:16)" checked> Reels / TikTok (9:16)</label>
              <label><input type="checkbox" name="formats" value="Feed posts (1:1)"> Feed posts (1:1)</label>
            </div>
          </fieldset>
          <label class="field" for="s-notes">Anything else? <small>Brand colours, stops to highlight, a deadline</small><textarea id="s-notes" name="notes" rows="4"></textarea></label>
        </div>
      </details>
      <input class="hp" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="hidden" name="from_page" value="">
      <p class="small">We’ll only use your details to reply about this sample. <a href="/privacy.html">Privacy notice</a></p>
    </form>
    <div class="side">
      <h2>What happens next</h2>
      <ol class="next">
        <li><span>We reply within one working day to confirm the route and stops.</span></li>
        <li><span>You get a 15-second sample by email, in widescreen and vertical, usually within 2 to 3 working days.</span></li>
        <li><span>If you like it, we quote for the full video or a set.</span></li>
      </ol>
      <p class="small">Prefer email? Send your itinerary, PDF or GPX file to <a href="mailto:hello@iterramaps.com">hello@iterramaps.com</a>.</p>
    </div>
  </div>'''
    page('sample.html', 'Get a free sample of your own route · Iterra Maps',
         'Send a link to one of your tours or rides and we’ll send back a free 15-second animated map sample in your colours. We reply within one working day.',
         body, cur='sample', main_cls='sample-page', ld=[bc_ld([('Iterra Maps', ''), ('Free sample', 'sample.html')])])

def thanks():
    body = '''  <div class="wrap">
    <div class="intro">
      <p class="eyebrow">Request received</p>
      <h1>Thanks. Your route is on its way to us.</h1>
      <p class="lead">We’ll reply within one working day to confirm the stops, then send your 15-second sample by email.</p>
    </div>
    <div class="side">
      <h2>While you wait</h2>
      <ol class="next">
        <li><span>Have your logo and brand colours to hand. Any image file is fine.</span></li>
        <li><span>If the tour is a walk or cycle and you have a GPX file, email it to <a href="mailto:hello@iterramaps.com">hello@iterramaps.com</a> for an exact trail line.</span></li>
        <li><span>Think about where the video will go first: your tour page, Instagram or an email campaign.</span></li>
      </ol>
      <p class="cta-row" style="margin-top:8px"><a class="btn btn-ink" href="/showcase/">See the showcase</a><a class="btn btn-outline" href="/">Back to the homepage</a></p>
    </div>
  </div>'''
    page('thanks.html', 'Thanks: your request is with us · Iterra Maps', 'Your free sample request has been received.', body, index=False, main_cls='sample-page no-form')

def notfound():
    body = '''  <div class="wrap">
    <svg viewBox="0 0 420 200" role="img" aria-label="A map with a route that stops short"><rect width="420" height="200" fill="#cfe0e6"/><path d="M150 0H420V200H190C180 170 150 160 156 130C162 104 132 96 140 66C146 42 138 20 150 0Z" fill="#f7f5ef"/><path d="M360 170C320 164 300 140 262 136C228 132 214 110 222 86" fill="none" stroke="#ff5a36" stroke-width="5" stroke-linecap="round"/><path d="M222 86C228 62 250 54 262 38" fill="none" stroke="#ff5a36" stroke-width="5" stroke-linecap="round" stroke-dasharray="2 10" opacity=".55"/><circle cx="360" cy="170" r="7" fill="#ff5a36" stroke="#fff" stroke-width="3"/><circle cx="222" cy="86" r="11" fill="#fff" stroke="#0e1b24" stroke-width="3"/><text x="222" y="91" text-anchor="middle" font-family="IBM Plex Sans, sans-serif" font-weight="700" font-size="14" fill="#0e1b24">?</text></svg>
    <h1>This page isn’t on the map.</h1>
    <p class="lead">The link may be old, or the page may have moved. These will get you back on route.</p>
    <p class="cta-row" style="justify-content:center"><a class="btn btn-primary" href="/sample.html">Get a free sample</a><a class="btn btn-outline" href="/showcase/">See the showcase</a><a class="btn btn-outline" href="/">Go to the homepage</a></p>
  </div>'''
    page('404.html', 'Page not found · Iterra Maps', 'This page isn’t on the map.', body, index=False, main_cls='notfound')

# ---------------------------------------------------------------- index pages
def showcase_index():
    reels = [('going-to-the-sun-road', 'Going-to-the-Sun Road', 'Lake McDonald up to Logan Pass in Glacier National Park, in 3D with the climb.', 'going-to-the-sun-road_1280x720_30fps.mp4', '16:9', '0:28'),
             ('million-dollar-highway', 'The Million Dollar Highway', 'Ouray over Red Mountain Pass to Silverton on US 550, following the car.', 'the-million-dollar-highway_1280x720_30fps.mp4', '16:9', '0:28'),
             ('miami-to-key-west', 'Miami to Key West', 'The Overseas Highway, island to island. Made for Reels.', 'miami-to-key-west_720x1280_30fps.mp4', '9:16', '0:25'),
             ('tour-du-mont-blanc', 'Tour du Mont Blanc, days 1–2', 'The real trail from Les Houches to Les Chapieux, in 3D with the climb.', 'tour-du-mont-blanc-the-first-two-days_1280x720_30fps.mp4', '16:9', '0:23'),
             ('cyclades-island-hop', 'Cyclades island hop', 'Mykonos to Naxos to Santorini by ferry, on a night-time map.', 'cyclades-island-hop_1280x720_30fps.mp4', '16:9', '0:23'),
             ('dublin-to-the-maldives', 'Dublin to the Maldives', 'A honeymoon in two flights, via Dubai.', 'honeymoon-dublin-to-the-maldives_1280x720_30fps.mp4', '16:9', '0:16')]
    chips_ = '<button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>' + ''.join(f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{n}</button>' for k, n in KINDS)
    rl = ''.join(f'<li><button type="button" class="card-link" data-open-video="{REEL}{f}" data-aspect="{a}" data-title="{e(t)}"><div class="ph"><img src="/media/{k}-card.jpg" alt="" width="640" height="360" loading="lazy" decoding="async"><span class="len">{d}</span></div><div class="bd"><h3><span class="sr-only">Play video: </span>{e(t)}</h3><p>{e(p)}</p></div></button></li>' for k, t, p, f, a, d in reels)
    body = f'''  <section class="pagehead">
    <div class="wrap">
      {crumbs([('Iterra Maps', ''), ('Showcase', None)], 'crumbs')}
      <h1>Showcase: route map videos by kind of trip.</h1>
      <p class="lead">Each film was made for a different kind of travel business, in its own brand and in every shape. Open one to watch it and see what went into it. The brands are made up. Your sample comes in your own.</p>
    </div>
  </section>
  <section class="section" style="padding-top:clamp(24px,4vw,40px)" aria-labelledby="films-t">
    <div class="wrap">
      <h2 class="sr-only" id="films-t">The films</h2>
      <div class="filters" role="group" aria-label="Show films for">{chips_}</div>
      <p class="sr-only filter-status" role="status" aria-live="polite"></p>
      <ul class="cards">{''.join(sc_card(s) for s in SHOWCASES)}</ul>
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="short-t">
    <div class="wrap">
      <div class="sec-head"><h2 class="h2" id="short-t">Short clips</h2><p class="lead">Six shorter journeys, 16 to 28 seconds each: scenic drives, a mountain trail, island ferries and a long-haul flight.</p></div>
      <ul class="cards">{rl}</ul>
    </div>
  </section>
  <section class="section" style="padding-top:0"><div class="wrap">{cta_band('Want to see one of your own tours?')}</div></section>'''
    items = {"@context": "https://schema.org", "@type": "ItemList", "name": "Iterra Maps showcase", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s['name'], "url": f'{BASE}/showcase/{s["slug"]}/'} for i, s in enumerate(SHOWCASES)]}
    page('showcase/', 'Showcase: animated route map videos by kind of trip · Iterra Maps',
         'Watch animated route map videos made for cycling tours, charity rides, coach tours, cruises, rail journeys and walking holidays, and see what went into each one.',
         body, cur='showcase', og=poster(SC['napa-and-sonoma-by-bike']), ld=[items, bc_ld([('Iterra Maps', ''), ('Showcase', 'showcase/')])])

def madefor_index():
    other = [('Walking holidays', 'camino-sarria-to-santiago', 'The trail itself, stage by stage, with the climbs.'), ('Cruises and island trips', 'alaska-inside-passage', 'Sea days and ports of call on one map.'),
             ('Rail journeys', 'switzerland-by-rail', 'The route follows the trains, in a look as polished as the trip.'), ('Any trip, in your look', 'one-route-many-looks', 'The same route made four ways.')]
    ol = ''.join(f'<li><a class="card-link" href="/showcase/{s}/"><div class="bd"><h3>{e(n)}</h3><p>{e(p)}</p><span class="go">Watch the film</span></div></a></li>' for n, s, p in other)
    body = f'''  <section class="pagehead">
    <div class="wrap">
      {crumbs([('Iterra Maps', ''), ('Who it’s for', None)], 'crumbs')}
      <h1>Who it’s for.</h1>
      <p class="lead">Animated route maps for businesses that sell a journey. Pick the one closest to yours to see how the videos are built around the way your trips run.</p>
    </div>
  </section>
  <section class="section" style="padding-top:clamp(24px,4vw,40px)" aria-labelledby="aud-t">
    <div class="wrap">
      <h2 class="sr-only" id="aud-t">Kinds of trip</h2>
      {aud_cards()}
    </div>
  </section>
  <section class="section" style="padding-top:0" aria-labelledby="other-t">
    <div class="wrap">
      <div class="sec-head"><h2 class="h2" id="other-t">Other kinds of trip</h2><p class="lead">We make these too. Each links to a film that shows how it looks.</p></div>
      <ul class="cards">{ol}</ul>
    </div>
  </section>
  <section class="section" style="padding-top:0"><div class="wrap">{cta_band()}</div></section>'''
    page('made-for/', 'Who it’s for: route map videos for tours, rides and journeys · Iterra Maps',
         'Animated route map videos for cycling tour operators, cycling events and charity rides, motorcoach and group tours, walking holidays, cruises and rail journeys.',
         body, cur='made-for', ld=[bc_ld([('Iterra Maps', ''), ('Who it’s for', 'made-for/')])])
