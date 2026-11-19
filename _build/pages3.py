"""Showcase batch 2 (Nov 2026): seven cycling films, all made-up brands on real routes."""
from core import *
from pages2 import showcase_page

SEND_TOUR = ['A link to the tour on your website, or the day-by-day itinerary', 'The overnight towns and the stops you want named', 'Your logo, and your brand colors if you have them']
SEND_DAY = ['A Strava, Ride with GPS or GPX file of the ride, or just the start, the climbs and the coffee stop', 'The climb figures you quote: distance, gradient, height', 'Your logo, and your brand colors if you have them']
SHAPES = 'One tour gives you the full set: widescreen for the tour page, vertical for Reels and Stories, and square for Facebook and email.'

def batch2_showcases(dates):
    d = lambda k: dates.get(k, '2026-11-19')
    showcase_page('danube-cycle-path-passau-to-vienna', 'The Danube Cycle Path',
      'Danube Cycle Path, Passau to Vienna: animated route map showcase · Iterra Maps',
      'An animated route map of an eight-day bike tour on the Danube Cycle Path from Passau to Vienna, through Linz, Melk and the Wachau, with a card for each overnight town.',
      'Showcase · Cycling tour', 'The Danube Cycle Path, Passau to Vienna',
      'Eight days down the Danube from Passau to Vienna, past the Schlögen loop, Linz, Melk and the vineyards of the Wachau, with a card for each overnight town. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 23 seconds. Rivermark Cycling Holidays is a made-up brand for this example.',
      "What's packed into this video", [
        ('route', 'The riverside path', 'The line follows the cycle path along the river, bend by bend, not a straight line between towns.'),
        ('page', 'A card for each overnight', 'Each town gets a card with the day, the distance and one thing to look forward to.'),
        ('camera', 'Stops along the way', 'Dürnstein gets its own card between overnights, for the castle ruin and the Wachau vineyards.'),
        ('palette', 'The Cycling Trail look', 'A light, clear map with the river picked out, in the colors of a made-up company.')],
      SHAPES, SEND_TOUR, d('danube'))
    showcase_page('loire-chateaux-by-bike', 'Châteaux of the Loire by bike',
      'Châteaux of the Loire by bike: animated route map showcase · Iterra Maps',
      'An animated route map of a five-day bike tour of the Loire Valley from Blois to Azay-le-Rideau, past Chambord, Chenonceau and Villandry, in a vintage map style.',
      'Showcase · Cycling tour', 'Châteaux of the Loire by bike',
      'Five days from Blois to Azay-le-Rideau, past Chambord, Chaumont, Chenonceau and the gardens of Villandry, on an old-style map. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 18 seconds. Petit Pédalier Tours is a made-up brand for this example.',
      "What's packed into this video", [
        ('route', 'The quiet roads', 'The route follows the small roads and cycle paths between the châteaux, the way riders travel them.'),
        ('camera', 'The châteaux on the way', 'Visits between overnights get their own card, so the highlights of each day are clear.'),
        ('page', 'A card for each overnight', 'Each night gets a card with the day, the distance and a local detail.'),
        ('palette', 'The Vintage Atlas look', 'Paper tones and an old-style typeface, for a trip that is all about history.')],
      SHAPES, SEND_TOUR, d('loire'))
    showcase_page('puglia-by-bike', 'Puglia by bike',
      'Puglia by bike: animated route map showcase · Iterra Maps',
      'An animated route map of a five-day bike tour in Puglia, from the trulli of Alberobello through the white towns of the Itria Valley to the Adriatic coast at Polignano a Mare.',
      'Showcase · Cycling tour', 'Puglia by bike: trulli, white towns and the Adriatic',
      'Five days from the trulli of Alberobello through Locorotondo, Martina Franca and Ostuni, then down through the olive groves to the coast and on to Polignano a Mare. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 13 seconds. Sole e Sella Bike Tours is a made-up brand for this example.',
      "What's packed into this video", [
        ('route', 'Hill towns to the sea', 'The line climbs between the white towns, then drops to the coast, on the real roads.'),
        ('page', 'Short days, clearly shown', 'Each card gives the day and its distance, so riders see this is a gentle tour.'),
        ('camera', 'The stops in between', 'Lunch stops and viewpoints get their own cards as the rider passes.'),
        ('palette', 'The Coastal Modern look', 'A bright, clean map with a deep blue sea, in the colors of a made-up company.')],
      SHAPES, SEND_TOUR, d('puglia'))
    showcase_page('vermont-fall-foliage-by-bike', 'Vermont in fall color',
      'Vermont fall foliage bike tour: animated route map showcase · Iterra Maps',
      'An animated route map of a five-day inn-to-inn bike loop from Woodstock, Vermont, through Windsor, Grafton and Weston, with covered bridges, villages and general stores on the way.',
      'Showcase · Cycling tour', 'Vermont in fall color: an inn-to-inn loop from Woodstock',
      'Five days on a loop from Woodstock through Windsor, Grafton and Weston and back, with Quechee Gorge, a covered bridge and a village store or two on the way. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 18 seconds. Covered Bridge Cycling Co. is a made-up brand for this example.',
      "What's packed into this video", [
        ('route', 'A loop, start to finish', 'The route leaves Woodstock and comes back to it, and the map makes that loop easy to follow.'),
        ('page', 'A card for each inn', 'Each night gets a card with the day, the distance and a local favorite.'),
        ('mountain', 'The hills of Vermont', 'Shaded relief shows the valleys and hills the route runs through.'),
        ('palette', 'The Vintage Atlas look', 'Warm paper tones that suit a fall foliage trip.')],
      SHAPES, SEND_TOUR, d('vermont'))
    showcase_page('otago-central-rail-trail', 'The Otago Central Rail Trail',
      'Otago Central Rail Trail: animated route map showcase · Iterra Maps',
      'An animated route map of a four-day ride on the Otago Central Rail Trail in New Zealand, from Clyde to Middlemarch, with the Poolburn Gorge and the highest point on the trail.',
      'Showcase · Rail trail', 'The Otago Central Rail Trail, Clyde to Middlemarch',
      'Four days on the old railway line across Central Otago, from Clyde through Omakau, Oturehua and Hyde to Middlemarch. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 18 seconds. Tussock & Rail Bike Hire is a made-up brand for this example.',
      "What's packed into this video", [
        ('route', 'The trail itself', 'The line follows the old rail corridor, not the roads beside it.'),
        ('page', 'A card for each overnight', 'Each night gets a card with the day and its distance.'),
        ('camera', 'The landmarks on the way', 'The tunnels and viaduct of the Poolburn Gorge, and the highest point on the trail, get their own cards.'),
        ('palette', 'The Rail Journey look', 'A map style made for railway routes, which suits a trail on an old line.')],
      SHAPES, SEND_TOUR, d('otago'))
    showcase_page('mallorca-sa-calobra-day', 'Sa Calobra day in Mallorca',
      'Mallorca Sa Calobra bike ride: animated route map showcase · Iterra Maps',
      'An animated route map of a classic Mallorca training-camp day from Port de Pollença to Sa Calobra and back, then the Sa Calobra climb again in 3D with an elevation profile.',
      'Showcase · Training camp', 'Sa Calobra day: the whole ride, then the climb in 3D',
      'A training-camp classic from Port de Pollença: over to Lluc, down to Sa Calobra and back up its hairpins. The video shows the whole day, then rides the climb again in 3D. Watch it first, then see what went into it.',
      'Widescreen 16:9, 1 minute 41 seconds. Isla Velo Camps is a made-up brand for this example.',
      "What a ride video can show", [
        ('route', 'The whole day first', 'The full loop from camp and back, with the coffee stop and the turn at the bottom.'),
        ('mountain', 'Then the climb in 3D', 'The camera follows the rider up every hairpin, with the mountains in 3D.'),
        ('screen', 'A live elevation profile', 'The profile fills in as the rider climbs, so the size of the climb lands.'),
        ('palette', 'The Alpine look', 'Strong relief and clear type, for rides where the mountains are the point.')],
      SHAPES, SEND_DAY, d('mallorca'))
    showcase_page('alpe-dhuez-and-col-du-galibier', "Alpe d'Huez and the Galibier",
      "Alpe d'Huez and Col du Galibier: animated climb video showcase · Iterra Maps",
      "An animated route video of two Tour de France climbs in 3D: the 21 hairpins of Alpe d'Huez, then the Col du Galibier over the Télégraphe from Saint-Michel-de-Maurienne, each with an elevation profile.",
      'Showcase · Climbs in 3D', "Two Tour de France legends: Alpe d'Huez and the Galibier",
      "The 21 hairpins of Alpe d'Huez, then the Galibier the long way, over the Col du Télégraphe from Saint-Michel-de-Maurienne. Both climbs are ridden in 3D. Watch it first, then see what went into it.",
      "Widescreen 16:9, 1 minute 23 seconds. Hairpin Cycling Holidays is a made-up brand for this example.",
      'What a climb video can show', [
        ('mountain', 'Every hairpin in 3D', 'The camera follows the rider up each switchback, with the mountains around them.'),
        ('screen', 'A live elevation profile', 'The profile climbs with the rider, so the gradient is easy to read.'),
        ('page', 'A card at each summit', 'Each top gets a card with the climb figures: distance, gradient and height.'),
        ('branch', 'Two climbs, one video', 'Each climb is its own section, so you can use them together or as two short clips.')],
      SHAPES, SEND_DAY, d('tdf'))
