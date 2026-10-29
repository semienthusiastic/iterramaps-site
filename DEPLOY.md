# Putting iterramaps.com live (GitHub Pages + Cloudflare)

The website is the `iterramaps-site` folder. Plan on about an hour, most of it waiting for DNS and the HTTPS certificate.

## 0. Before you start

- **Fill in the privacy notice:** open `privacy.html` and replace `[YOUR FULL NAME]` and `[Formspree / your email provider]` (see step 6).
- **Both domains need to be on Cloudflare.** If you bought them through Cloudflare, they already are. If not, in Cloudflare choose **Add a site**, enter `iterramaps.com`, pick the **Free** plan, then change the nameservers at your registrar to the two Cloudflare gives you. Do the same for `iteramaps.com`.

## 1. Put the files on GitHub

1. Go to github.com/new. Repository name: `iterramaps-site`. Choose **Public** (Pages is free for public repositories). Click **Create repository**.
2. On the empty repository page, click **uploading an existing file**.
3. Open the `iterramaps-site` folder on your computer, select **everything inside it** (not the folder itself) and drag it into the browser. That includes the `fonts` and `media` folders and the `CNAME` file.
4. Click **Commit changes**.

## 2. Turn on GitHub Pages

1. In the repository, open **Settings → Pages**.
2. Under **Build and deployment**: Source **Deploy from a branch**, Branch **main**, folder **/ (root)**. Click **Save**.
3. Under **Custom domain** you should see `iterramaps.com` (taken from the CNAME file). If not, type it and click **Save**.

## 3. Point iterramaps.com at GitHub (Cloudflare → iterramaps.com → DNS → Records)

1. Delete any existing **A**, **AAAA** or **CNAME** records for `iterramaps.com` (shown as `@`) and `www`. These are usually parking-page records.
2. Add four **A** records, Name `@`, Proxy status **DNS only** (grey cloud):
   - `185.199.108.153`
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`
3. Optional, for IPv6: four **AAAA** records, Name `@`, **DNS only**:
   - `2606:50c0:8000::153`
   - `2606:50c0:8001::153`
   - `2606:50c0:8002::153`
   - `2606:50c0:8003::153`
4. Add one **CNAME** record: Name `www`, Target `YOUR-GITHUB-USERNAME.github.io`, **DNS only**.

## 4. Switch on HTTPS

1. Back in **GitHub → Settings → Pages**, wait for **DNS check successful**. This is often minutes, sometimes up to a few hours.
2. When the certificate is ready, tick **Enforce HTTPS**.
3. Open https://iterramaps.com and https://www.iterramaps.com. Both should show the site.

Leave the records on **DNS only** for now. If you later turn on the orange cloud (Cloudflare proxy), first set **SSL/TLS → Overview** to **Full**, or the site will loop.

## 5. Redirect iteramaps.com (Cloudflare → iteramaps.com)

1. **DNS → Records**: add an **A** record, Name `@`, IPv4 `192.0.2.1`, **Proxied** (orange cloud). This is a placeholder address; Cloudflare answers before it is ever used.
2. Add a **CNAME** record, Name `www`, Target `iteramaps.com`, **Proxied**.
3. **Rules → Redirect Rules → Create rule**:
   - Rule name: `To iterramaps.com`
   - If incoming requests match: **All incoming requests**
   - Then: Type **Dynamic**, Expression `concat("https://iterramaps.com", http.request.uri.path)`, Status code **301**, tick **Preserve query string**
   - Click **Deploy**.
4. Test: http://iteramaps.com/sample.html should land on https://iterramaps.com/sample.html.

## 6. Email: hello@iterramaps.com

**Receiving (free):**
1. Cloudflare → iterramaps.com → **Email → Email Routing → Get started**.
2. Create the address `hello`, forwarding to your own inbox. Confirm the verification email.
3. Let Cloudflare add the MX and TXT records it offers.

**Sending as hello@** needs a mail provider. Options:
- Zoho Mail has a free plan.
- Google Workspace is about €7 a month.

This isn't urgent: you can reply from your own address at first.

## 7. Make the forms deliver to you (Formspree)

Until this is done, both forms open the visitor's email app with the details filled in, so nothing is lost.

1. Sign up at formspree.io with `hello@iterramaps.com`. The free plan covers a small number of submissions a month, which is plenty to start.
2. Click **New form**, name it "Iterra Maps website" and copy the endpoint (it looks like `https://formspree.io/f/abcdwxyz`).
3. In `main.js`, paste it on line 8: `const FORM_ENDPOINT = "https://formspree.io/f/abcdwxyz";`
4. In `privacy.html`, replace `[Formspree / your email provider]` with `Formspree`.
5. Upload the changed files to GitHub (repository → **Add file → Upload files**, drop them in, **Commit**). The site updates within a minute or two.
6. Send yourself a test request from https://iterramaps.com/sample.html.

## 8. Showreel videos and images

The six cards on the homepage match the six short projects in `iterramaps-showreel-projects.zip`. Each card shows an image with a play button. On a computer, resting the mouse on a card fades the video in over the image and plays it silently; clicking (or tapping on a phone) opens it full size in a pop-up with sound and full-screen controls. Nothing plays by itself.

**Videos:** open each project in Iterra Maps and click **Export MP4 video** (they're already set to 720p, 30 fps, Quality Standard: about 5–6 MB each). Keep the file names the app gives them.

**Images:** landscape (16:9) JPGs, ideally 1280 × 720 and under about 200 KB each. Anything wider or taller is cropped to fill the card. Good sources:
- **A still from the app:** scrub to a moment you like and click **Save still image (PNG)**. For the vertical Dublin–London reel, switch the project to 16:9 for a moment to save a landscape still, then switch it back before exporting the video.
- **A photo of the destination**, if you have the rights to use it.

Send me the PNGs or photos and I'll crop, size and name them, or save them as JPG yourself with the names below.

| Card | Video in `media/` | Image in `media/` |
|---|---|---|
| Connemara Day Tour | `connemara-day-tour_1280x720_30fps.mp4` | `connemara-day-tour.jpg` |
| Tour du Mont Blanc, days 1–2 | `tour-du-mont-blanc-the-first-two-days_1280x720_30fps.mp4` | `tour-du-mont-blanc.jpg` |
| Great Western Greenway | `great-western-greenway_1280x720_30fps.mp4` | `great-western-greenway.jpg` |
| Dublin to London by sail & rail (vertical) | `dublin-to-london-by-sail-rail_720x1280_30fps.mp4` | `dublin-to-london.jpg` |
| Cyclades island hop | `cyclades-island-hop_1280x720_30fps.mp4` | `cyclades-island-hop.jpg` |
| Dublin to the Maldives | `honeymoon-dublin-to-the-maldives_1280x720_30fps.mp4` | `dublin-to-the-maldives.jpg` |

**Upload the videos to R2:** Cloudflare → R2 → `iterra-media` → **Objects**. Create a folder `site`, and inside it a folder `showreel`, then upload the six MP4s there, keeping their names. Each one then plays at `https://media.iterramaps.com/site/showreel/<file name>`, which is what `index.html` already points to.

**Upload the images to GitHub:** put the six JPGs in the repository's `media` folder (**Add file → Upload files**, drag them in, **Commit changes**). Delete any MP4s from the GitHub `media` folder: they now live on R2.

**If something is missing:**
- No image yet: the card shows a frame from near the end of its video instead, so you can upload the videos first. To pick a different frame, add `data-thumb="8"` (seconds) to that card's `<article class="reel" ...>` line in `index.html`.
- No video (or a misnamed one): the card shows its image with no play button. The browser console names the file it couldn't find.

To use a different image name, change the `src` of the `<img>` line inside that card in `index.html`. To replace a video, upload the new file to R2 with the same name, then purge its address in Cloudflare (**Caching → Configuration → Purge cache → Custom purge**).

## 9. A sample page for a prospect

Each prospect gets their own page, such as `iterramaps.com/for/wild-rover-walks-k7q2/`, with their videos, download buttons and a button to email you. It's kept out of Google and linked from nowhere on the site.

**Make one (about 20 minutes once the videos are exported).** Example folder name: `wild-rover-walks-k7q2` (company name plus four random characters, lower case, hyphens). Use exactly the same name on R2 and on GitHub.

**A. Videos on R2**
1. On your computer, copy the exports and rename the copies `wide.mp4` (16:9) and `vertical.mp4` (9:16, optional). With file extensions showing, check they don't end up as `wide.mp4.mp4`.
2. R2 → `iterra-media` → `samples` → **Add folder** → the folder name.
3. Open the new folder and upload `wide.mp4` and `vertical.mp4`.

**B. The page folder on your computer**
1. In your local `for` folder, copy `_template` and rename the copy to the folder name.
2. Put a 1280 × 720 still in it as `poster.jpg`, and optionally their logo as `logo.png`.

**C. Edit the page:** open `for/<folder>/index.html` in Notepad++, press **Ctrl+H**, and **Replace All** each of these:
1. `FOLDER-NAME` → the folder name (fixes the link-preview image and the `media:` line).
2. `Company Name` → their company name (fixes the title, link preview and settings).
3. `Tour Name` → the tour, e.g. `the Dingle Way`.
4. In the settings, fill in `firstName`, `accent` (their brand colour) and `logo: "logo.png"` if you added one. Delete the `vertical.mp4` line if there's no vertical video.
5. Save, with Encoding set to UTF-8.

**D. Upload to GitHub:** in the repository, open the `for` folder → **Add file → Upload files** → drag in only the new folder → **Commit changes**. (The very first time, upload the whole `for` folder so the shared `sample-page.css` and `sample-page.js` go up too.)

**E. Check before sending:** after 1–2 minutes, open `https://iterramaps.com/for/<folder>/` and check that:
- both videos play;
- the download buttons show a size and save a sensibly named file;
- "Give us your feedback" opens the feedback form with the company filled in, and "Reply by email" opens an email with the subject filled in (on pages set to mode: "sale", "Email us about the full reel" instead);
- the name, greeting, colour and logo are right, and it looks right on a phone.

Then log the link in the register and send the first email.

**Good to know:**
- The `_template` folder itself never appears on the live site: GitHub Pages skips folders whose names start with `_`.
- The shared look and layout live in `for/sample-page.css` and `for/sample-page.js`. A change there updates every sample page at once.
- The "Email me" button opens their email app with a subject and first line filled in, addressed to hello@iterramaps.com.
- Pages aren't truly private: your GitHub repository is public. After 6 months with no sale, delete both the R2 folder and the GitHub folder (on GitHub: open the folder → **⋯ → Delete directory**).
- `test-k7q2` was the practice run (15 Oct 2026). Keep it as your own demo, or delete it from both places.

## 10. Hosting a client's video (embed code)

For clients on the hosting add-on. Their web developer gets an iframe for the video, plus a credit line, **Route map by Iterra Maps**, that sits in their own page under the video. Keeping that line is a condition of hosting.

**Once:** upload the `embed` folder (it holds `index.html`, the player, and `code.html`, the code maker) to the top level of the repository.

**For each video** (10 min):
1. In R2, open `iterra-media`, make the folder `clients/<client>/<tour>/` (e.g. `clients/wildrover/dingle-way/`), and upload the videos named by shape: `16x9.mp4`, `9x16.mp4`, `1x1.mp4`. Optionally add a still of each with the same name ending `.jpg` (e.g. `16x9.jpg`).
2. Open `https://iterramaps.com/embed/code.html`, fill in the client ID, tour ID, title and shapes, and check the preview plays.
3. Copy **Email to their web developer** into a new email from hello@ and send it (or send it to the client to pass on).
4. Record the R2 address in the register's Projects tab, with "Hosting: Yes" on the Clients tab.
5. A week later, open their page: the video plays and the credit line is there.

**When a route changes:** upload the new file over the old one with exactly the same name, then purge it in Cloudflare (Caching → Configuration → Custom purge → the file's address). Their page updates by itself.

**If hosting ends:** delete the client's R2 folder. Their embedded player then shows "This video isn't available right now", and they keep the files from their Drive folder to host themselves.

**If a video won't play straight after uploading** (the player says "This video isn't available right now"), purge its address in Cloudflare (Caching → Configuration → Custom purge). The *Media* cache rule has a Status code TTL so that 400–499 responses are never cached; leave it in place, because without it a "not found" seen during an upload is kept for a month.

**Keep the player clean:** never add analytics, cookies or a consent banner to `embed/index.html`. It runs inside our clients' websites.

## 11. Map label fonts (iterramaps.com/fonts)

The Map designer's ten extra label fonts are loaded from the website, from the `fonts` folder (one sub-folder per font, e.g. `fonts/Iterra Inter Regular/0-255.pbf`). The files are in `iterramaps-fonts.zip`.

1. Unzip `iterramaps-fonts.zip`. It contains a `fonts` folder with 35 font folders (142 files).
2. In the `iterramaps-site` repository on GitHub, open the `fonts` folder (it already holds the website's own fonts; nothing there is replaced) and click **Add file → Upload files**.
3. GitHub takes at most 100 files per upload, so drag in about half of the font folders, click **Commit changes**, then upload the rest the same way. Drag the folders themselves, so each keeps its name.
4. After a minute or two, open https://iterramaps.com/fonts/Iterra%20Inter%20Regular/0-255.pbf. It should download a small file rather than show the "page not found" page.
5. In the app, Look tab → Base map **Map designer** → Map labels → Font **Inter**: the place names should appear in Inter. (The 4xx no-cache rule means a "not found" seen before the upload is not kept.)

Licences: all the fonts are under the SIL Open Font License except Special Elite (Apache 2.0); `fonts/README.txt` lists them. Both allow use in commercial videos.

## Things to change in one place

- **Prices, turnaround, FAQ, wording:** `index.html` (plain text).
- **Email address:** search `hello@iterramaps.com` in the `.html` files and `main.js`.
- **Social share picture:** `og-image.png` (1200 × 630).
- **Visitor statistics:** if you add any, Cloudflare Web Analytics is free and cookie-less. Add a line about it to `privacy.html`.
