# Babar Shokut Electric Wear — Codex project instructions

## Mission
Finish and publish the client's appliance repair website as a **free public GitHub Pages preview** at a new standalone repository in the connected account `BaderAsad1`, ideally `BaderAsad1/babar-shokut-website`. Fully execute the handoff task in `docs/CODEX-TASK.md`. This is an existing developed website, not an invitation to start over.

## Business facts and positioning (do not invent)
- Public business name: Ac Repair Sharjah — Babar Shokut Electric Wear. On-site brand: Babar Shokut Electric Wear. Keep the spelling `Shokut`, `Wear`.
- Contact: Bilal, the owner; serving customers since **2012**.
- Services in priority order: **washing machines**, **fridges**, then **AC** (secondary).
- Coverage: **Sharjah, Dubai, Ajman**.
- Address: **Building 25, Shop 1, Al Yarmook Street 13, Sharjah, UAE**.
- Inspection fee: **AED 50**. This is **not** a complete repair price. Do not promise credit toward repair, warranties, service times, free inspection, or 24/7 availability.
- Public listing telephone from supplied Google Business Profile screenshot: **055 243 4708** (+971552434708). Current WhatsApp service for that number remains **unconfirmed**; the enquiry action prepares a WhatsApp draft, not a booked or automatically sent message.
- Google Maps page: `https://www.google.com/maps?cid=16162322832422038457`.
- Do not portray AI-generated imagery as the real shop, Bilal, staff, customer visits, or real repairs. Do not invent ratings, reviews, manufacturer affiliations, or testimonials.

## Design system
- Warm ivory `#F6F3ED`, deep navy `#102337`, cobalt `#2357E8`, subtle lime `#E3ECAA`.
- Elegant, spacious premium editorial style. Washer and fridge photography dominate; AC remains a small secondary strip.
- Clean typography, large readable headings, strong CTA contrast, responsive and accessible forms/navigation.
- Design references: `design/homepage-concept.png` and `design/blog-concept.png`; actual implemented screenshot: `design/implemented-homepage.jpg`. Concepts are visual targets, not exact screenshots of rendered code.
- Preserve layout decisions and existing functionality unless tests or visual QA show a clear need for changes.

## Technical map
- Vanilla semantic HTML and JS; Python standard library build. No framework, backend, database, paid hosting, or API key needed.
- Build: `python3 scripts/build.py`
- Check: `python3 scripts/check.py`
- JS syntax: `node --check assets/js/main.js`
- Preview: `python3 -m http.server 8000 --directory dist`
- `site-config.json` controls business contact, canonical base URL, and `preview` flag.
- `content/articles.json` contains five source-backed SEO guides.
- `.github/workflows/deploy.yml` is the GitHub Pages Actions pipeline; publishes `dist/`.
- `scripts/publish_github_pages.sh` can create repo and configure Pages when run with authenticated local `gh` access; do not pretend to have succeeded if GitHub refuses access.

## Scope and quality bar
1. Validate the existing project, do not delete or replace working pages.
2. Inspect desktop and mobile layouts, with special attention to horizontal overflow, image crops, header, forms, nav, typography, and contact clicks.
3. Complete any necessary accessibility/SEO and visual polish issues; re-run checks.
4. Publish to **new separate public repository** owned by `BaderAsad1`; do not put it in unrelated existing repositories or force-push old branches.
5. Enable GitHub Pages with the **GitHub Actions** source and verify a successful workflow.
6. Actually request the public deployed URL and verify homepage, blog index, and one article return successful content. Share verified links with the user.
7. Keep `preview: true` and `noindex` during design approval; do not claim production SEO launch before client approval.
8. Clearly state any blocker and its required resolution rather than claim success from a successful git push alone.

## Security and operational boundaries
- Don't hardcode tokens, passwords, cookies, or credentials; use an authenticated GitHub CLI or approved credential flow.
- Don't submit customer messages, schedule appointments, purchase hosting, or enable paid services.
- Don't invent or change business facts while editing.
- Do not redistribute bundled font files; CSS uses a public web font with system fallback.
- Avoid unrelated repository mutations, deletion, and force push.
- Review `README.md`, `VERIFICATION.md`, `docs/CODEX-TASK.md` before making any major change.
