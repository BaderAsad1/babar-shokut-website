# Continue this project in Codex: publish Babar Shokut website

You are in the complete local source tree for the Babar Shokut Electric Wear website. **Do the work, don't just provide generic steps.** The user wants a real public free client-preview URL on GitHub Pages. They want a AAA-level site with washer/fridge focus, an advice blog, and clickable ways to contact Bilal.

## Deliverable
Create and verify a **new standalone public GitHub repo** on the authenticated GitHub account `BaderAsad1` named `babar-shokut-website` and a working **GitHub Pages URL**. Preserve the existing nine-page website and original design. Do not invent a result.

### Phase 1 — Inspect and validate
- Read `AGENTS.md`, `README.md`, `site-config.json`, `VERIFICATION.md`.
- Run `python3 scripts/build.py`, `python3 scripts/check.py`, `node --check assets/js/main.js`.
- Launch local preview and visually inspect homepage, advice index, one article at desktop and 390px mobile. Fix material defects rather than claim pixel perfection without checking.
- Check phone CTA +971552434708, Google Maps directions, and AED 50 inspection fee are consistent; WhatsApp is draft-only and not a booking confirmation. Confirm all guide links and page images work.
- Keep `preview=true` and `noindex` for this client review.

### Phase 2 — Publish
- Verify GitHub CLI credentials. If not configured, try `gh auth login` through the allowed interactive browser/device flow; never request a password or PAT in plain chat.
- If no repository exists, create **BaderAsad1/babar-shokut-website** (public), commit the source code, push `main` using the local GitHub session. The provided `scripts/publish_github_pages.sh` is a helper that can perform creation and deployment; inspect it and modify safely if required.
- Configure GitHub Pages to build via GitHub Actions. `.github/workflows/deploy.yml` builds and publishes `dist/`.
- Trigger/wait for deployment and inspect any errors. Correct workflows, publish and recheck until green.
- Verify via actual HTTPS fetch or browser that homepage, `/advice/`, and at least one guide render on the **deployed GitHub Pages domain**. Do not guess URL or call it live from repository creation alone.

### Phase 3 — Report back
- Give a single verified client preview link plus repository link and brief summary of functionality.
- Distinguish review/preview (`noindex`) from launch-ready site. Identify open confirmations: Bilal's WhatsApp destination, hours and any unverified Google details.
- If sign-in or permissions genuinely block publishing, preserve the complete working tree, state the exact blocker, and give the closest supported continuation. Do not tell the user to create the repo manually unless the available authorized actions cannot do so.

## Acceptance criteria
- Site is in its **own** public repository in `BaderAsad1`, not mixed with another client's code.
- GitHub Actions build + Pages deploy successful.
- Browser verifies actual public HTTPS response for homepage and content pages.
- No broken internal links, images or references. Form does not falsely claim confirmed booking.
- No fabricated testimonials, review counts, guarantees or repair pricing; AED 50 clearly means inspection fee.
- Responsive polished homepage with washers/fridges dominant; matching useful SEO advice hub and guides.
