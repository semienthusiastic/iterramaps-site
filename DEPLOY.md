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

## 8. Later: showreel videos

1. Export each demo reel from Iterra Maps at 720p. Keep each clip under about 10 MB; trim to 15–20 seconds if needed.
2. Put the files in `media/`, for example `media/wild-atlantic-way.mp4`.
3. In `index.html`, find the matching card and fill in its `data-video` attribute: `data-video="media/wild-atlantic-way.mp4"`. The video replaces the drawing and plays silently when the card is on screen.
4. Change the line under the showreel ("Showreel videos are on their way…") once the videos are up.

## Things to change in one place

- **Prices, turnaround, FAQ, wording:** `index.html` (plain text).
- **Email address:** search `hello@iterramaps.com` in the `.html` files and `main.js`.
- **Social share picture:** `og-image.png` (1200 × 630).
- **Visitor statistics:** if you add any, Cloudflare Web Analytics is free and cookie-less. Add a line about it to `privacy.html`.
