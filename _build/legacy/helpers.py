# Builds /made-for/ pages from the live motorcoach page (header, footer, styles and scripts stay identical).
import html, json, re, sys
SITE = '/home/claude/site-work/'
TPL = open(SITE + 'made-for/motorcoach-tours/index.html').read()
R2 = 'https://media.iterramaps.com/site/showcase/'
e = html.escape
S = 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
 'page': '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.6-3.5 3.3-5.5 6.5-5.5s5.9 2 6.5 5.5"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.8c2 .7 3.2 2.5 3.5 5.2"/>',
 'phone': '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
 'screen': '<rect x="2.5" y="4" width="19" height="12.5" rx="1.5"/><path d="M9 20.5h6M12 16.5v4"/>',
 'branch': '<circle cx="6" cy="5.5" r="2"/><circle cx="6" cy="18.5" r="2"/><circle cx="18" cy="8" r="2"/><path d="M6 7.5v9M18 10c0 4-6 3.5-11 7"/>',
 'palette': '<path d="M12 3a9 9 0 1 0 0 18c1.2 0 1.8-.8 1.8-1.7 0-1.2-1-1.5-1-2.6 0-1 .8-1.7 1.8-1.7H17a4 4 0 0 0 4-4C21 6.5 17 3 12 3z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
 'lock': '<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/>',
 'route': '<circle cx="5.5" cy="18.5" r="2"/><circle cx="18.5" cy="5.5" r="2"/><path d="M7.5 18.5h7a3.5 3.5 0 0 0 0-7h-5a3.5 3.5 0 0 1 0-7h7"/>',
 'camera': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
 'mountain': '<path d="M2.5 19.5 9 8l3.5 6 2.5-4 6.5 9.5z"/><path d="m7 11.5 2 1.5 1.5-1"/>',
 'van': '<path d="M2.5 16.5V7.5a1 1 0 0 1 1-1h11l4 4.5h2a1 1 0 0 1 1 1v4.5h-2"/><path d="M14.5 6.5V11h6"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M9 17h6"/>',
 'calendar': '<rect x="3.5" y="5" width="17" height="15.5" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
}
ico = lambda k, t=0: f'<span class="pg-ico t{t}" aria-hidden="true"><svg viewBox="0 0 24 24" {S}>{ICONS[k]}</svg></span>'
def bridge(q): return f'''      <p class="pg-bridge"><span class="pg-bridge-mark" aria-hidden="true"><svg viewBox="0 0 16 16"><path d="M4 6l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="pg-bridge-k">Next stop</span><span class="pg-bridge-q">{e(q)}</span></p>\n'''
def stop(n, label, hid, inner, cls=''): return f'''      <section class="pg-stop{(' ' + cls) if cls else ''}" aria-labelledby="{hid}">
        <span class="pg-stop-mark" aria-hidden="true">{n}</span>
        <p class="pg-stop-k">{n} · {e(label)}</p>
{inner}
      </section>\n'''
def dest(eyebrow, title, text): return f'''      <aside class="pg-dest rt-cta" aria-labelledby="cta-t">
        <span class="pg-stop-mark pg-dest-mark" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6 21V4M6 4h11l-2.5 4L17 12H6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        <div>
          <p class="pg-stop-k">Destination · {e(eyebrow)}</p>
          <h2 id="cta-t">{e(title)}</h2>
          <p>{e(text)}</p>
        </div>
        <div class="rt-cta-btns">
          <a class="btn btn-primary" href="../../sample.html">Get a free sample</a>
          <a class="btn btn-outline" href="../../#pricing">See pricing</a>
        </div>
      </aside>\n'''
def journey(*parts): return '    <div class="pg-journey">\n      <span class="pg-origin" aria-hidden="true"></span>\n' + ''.join(parts) + '    </div>\n'
def faq_html(qs): return '\n'.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qs)
def faq_ld(qs): return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}
def bc_ld(items): return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": "https://iterramaps.com/" + u} for i, (n, u) in enumerate(items)]}
def itin(days): return ''.join(f'<div><b>Day {d}</b><i style="width:{w1}%"></i><i style="width:{w2}%"></i></div>' for d, w1, w2 in days)
MADE_FOR = [('motorcoach-tours', 'Motorcoach and group tours'), ('cycling-tours', 'Cycling tour operators'), ('walking-tours', 'Walking tours'), ('cycling-events', 'Cycling events and charity rides'), ('cruise-lines', 'Cruise lines'), ('rail-journeys', 'Rail journeys'), ('dmcs', 'DMCs'), ('travel-advisors', 'Luxury travel advisors')]

def build(slug, title, desc, og_img, crumb, main, faq):
    s = TPL
    s = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(title)}">', s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(desc)}">', s, count=1)
    s = s.replace('https://iterramaps.com/made-for/motorcoach-tours/', f'https://iterramaps.com/made-for/{slug}/')
    s = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="https://iterramaps.com/{og_img}">', s, count=1)
    a = s.index('<script type="application/ld+json">'); z = s.index('</head>')
    lds = ''.join(f'<script type="application/ld+json">\n{json.dumps(x, ensure_ascii=False)}\n</script>\n' for x in [faq_ld(faq), bc_ld([('Iterra Maps', ''), (crumb, f'made-for/{slug}/')])])
    s = s[:a] + lds + s[z:]
    a = s.index('    <nav class="rt-crumbs"'); z = s.index('  </div>\n</main>')
    crumbs = f'    <nav class="rt-crumbs" aria-label="Breadcrumb"><a href="../../">Iterra Maps</a> <span aria-hidden="true">›</span> <span>Made for</span> <span aria-hidden="true">›</span> <span aria-current="page">{e(crumb)}</span></nav>\n'
    more = '    <nav class="rt-more" aria-labelledby="more-t">\n      <h2 id="more-t">Also made for</h2>\n      <ul>' + ''.join(f'<li><a href="../{k}/">{e(n)}</a></li>' for k, n in MADE_FOR if k != slug) + '</ul>\n    </nav>\n'
    s = s[:a] + crumbs + main + more + s[z:]
    import os; os.makedirs(SITE + f'made-for/{slug}', exist_ok=True)
    open(SITE + f'made-for/{slug}/index.html', 'w').write(s)
    return SITE + f'made-for/{slug}/index.html'
