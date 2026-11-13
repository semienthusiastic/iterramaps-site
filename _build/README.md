# How this site is built

Every public page is written by `build.py` from one list of pages in `core.py`. The menu, footer, index pages,
"More showcases" lists and the sitemap all come from that list, so a link to a page that doesn't exist can't be written
(the build stops if it finds one).

- `core.py`: the list of showcase films and audience pages, the shared header and footer, small helpers.
- `pages.py`: home, pricing, how it works, free sample, thanks, 404, showcase index, "Who it's for" index.
- `pages2.py`: the cycling events page, the four newer showcase pages, and the six page bodies written before this generator (kept in `legacy/`).
- `src/new.css`, `src/site.js`, `src/consent.js`: the styles and scripts. `assets/site.css` is the earlier styles plus `new.css`.
- `legacy/`: frozen inputs. Do not edit; change the generator instead.

To rebuild: `SITE_LIVE=<a copy of the repository> SITE_OUT=<an empty folder> python3 build.py` (needs Python 3 and Pillow).

To add a showcase film: add one entry to `SHOWCASES` in `core.py`, put its still in `legacy/media/showcase/<key>-wide.jpg`,
and add a `showcase_page(...)` call in `pages2.py`.

When small web copies of a film's videos are on R2 (`wide.web.mp4`, `vertical.web.mp4`, `square.web.mp4`), add the film's
folder name to `WEB_READY` in `core.py` and rebuild.

Not built by the generator, carried over untouched: `/for/` sample pages, `/embed/`, `feedback.html`, fonts, brand files.
