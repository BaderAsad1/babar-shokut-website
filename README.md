# Babar Shokut Electric Wear

A responsive static website for the Sharjah-based appliance repair business. The homepage leads with washing machine and fridge repair, with AC repair as a supporting service. The advice section contains five source-backed guides and individual article pages.

The site uses semantic HTML, CSS, browser JavaScript, and a Python standard-library build script. There is no application server, customer database, package installation, or paid service required to build it.

## Build and check

Use Python 3.9 or later from the repository root:

```bash
python3 scripts/build.py
python3 scripts/check.py
```

The build writes the complete publishable website to `dist/`. The release check validates the expected nine HTML pages, headings and metadata, local links and fragments, image and font references, JSON-LD, contact destinations, obsolete phone numbers, dummy content, sitemap routes, and indexing directives. External website availability and browser interaction are outside this static check.

To serve the built pages locally:

```bash
python3 -m http.server 8000 --directory dist
```

Open [http://localhost:8000](http://localhost:8000). Rebuild after editing source files. The custom 404 intentionally uses the configured absolute site URL so its home link and stylesheet work from missing routes at any depth.

## Source structure

| Path | Purpose |
| --- | --- |
| `site-config.json` | Business details, contact destinations, deployment URL, and preview flag |
| `scripts/build.py` | Generates complete crawlable HTML, robots.txt, sitemap.xml, and a custom 404 |
| `scripts/check.py` | Dependency-free release checks |
| `content/articles.json` | Article text, source links, and related-guide relationships |
| `assets/css/styles.css` | Responsive design, accessible states, and reduced-motion support |
| `assets/js/main.js` | Mobile navigation, advice filters, and the WhatsApp enquiry flow |
| `assets/images/` | Optimized appliance illustrations and favicon |
| `assets/ASSET-NOTES.md` | Image provenance, prompts, originals, and alt-text guidance |
| `.github/workflows/deploy.yml` | Build, check, and deploy workflow for GitHub Pages |

## Free public hosting with GitHub Pages

The repository includes an official GitHub Pages Actions workflow. For a public repository on GitHub Free, Pages provides hosting without a separate hosting charge. The source repository and deployed pages are public. See [GitHub's Pages availability and hosting documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

1. Set `siteUrl` in `site-config.json` to the final HTTPS project-site URL, including its repository path and trailing slash.
2. In the repository's **Settings → Pages**, select **GitHub Actions** as the build and deployment source.
3. Push to `main`, or run **Deploy website to GitHub Pages** from the Actions tab.
4. Inspect the workflow result and the deployed URL reported by its `github-pages` environment.

The workflow checks out the source, configures Pages, runs the build and release check, uploads only `dist/`, and deploys the resulting artifact. It uses `actions/checkout@v6`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v4`, and `actions/deploy-pages@v4`. Deployment uses GitHub's workflow permissions and does not require a personal access token in this repository.

Changing `siteUrl` requires a rebuild so canonical URLs, social image URLs, sitemap locations, and 404 links stay consistent. Preserve the repository path for project sites; ordinary page and asset links are relative.

## Preview and search indexing

`preview` is initially `true` in `site-config.json`. Each generated page carries `noindex`, and the preview robots.txt allows crawling so search engines can read that instruction. The preview robots.txt does not advertise the sitemap. The 404 remains `noindex` in both modes. This follows [Google's documented requirements for noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing).

The preview is publicly accessible. `noindex` is an indexing instruction, not authentication or a privacy control, and it does not guarantee immediate removal of a previously indexed URL.

After the owner approves the business details, contact destinations, design, and content, set `preview` to `false`, rebuild, run the check, and deploy. Content pages will then use `index, follow`, and robots.txt will advertise the sitemap. This enables normal indexing; it does not promise ranking or search traffic.

## Business details and launch confirmation

The current phone, **055 243 4708**, comes from the supplied Google Business Profile screenshot. The site config uses **+971552434708** for calls. The WhatsApp enquiry flow is configured to the same number; the owner must confirm that this is the intended WhatsApp destination before a production launch. Older directory and storefront numbers are deliberately excluded.

The inspection fee is **AED 50**. It is an inspection charge, not a complete repair price. No automatic fee deduction, free inspection, repair guarantee, parts warranty, response time, or same-day availability is implied. Visit arrangements and repair costs are discussed with Bilal.

The business name, owner, operating since 2012, address, and service coverage in Dubai, Sharjah, and Ajman follow the supplied brief. The current business identity retains the spelling **Babar Shokut Electric Wear**. The Google Maps link targets the exact supplied business entity. Opening hours remain unset because the available sources conflict. Ratings and review counts are not displayed; the screenshot is only a dated snapshot and does not justify invented testimonials or a live-rating claim.

## Enquiries and privacy

The inspection form prepares a WhatsApp draft on the visitor's device. It does not submit a booking to this website, store customer details in a database, or send a message automatically. The visitor chooses whether to send the draft in WhatsApp. Calls and directions open their corresponding external services.

There are no advertising trackers, analytics cookies, or customer accounts in the application. The font is requested from Google Fonts with a system-font fallback, as disclosed on the privacy page. The privacy page explains the enquiry flow and external-service handling. Do not add a fake confirmation state that implies an appointment has been booked.

## Content and images

The article pages include source links and model-specific cautions. Keep factual advice tied to those sources, and do not add unsupported technical procedures or professional endorsements. The content is general guidance and does not replace the appliance manufacturer's instructions or a technician's diagnosis.

The appliance photographs are AI-generated illustrative scenes. They are not photographs of Bilal, the real shop, technicians, customer homes, or completed repairs. Their full provenance is recorded in `assets/ASSET-NOTES.md`, which is excluded from the public build. The generated assets have no manufacturer endorsement. Preserve that distinction in captions, alt text, and future marketing copy.

Before approving a production launch, review the site on a phone and desktop, verify the displayed phone and WhatsApp destination with the owner, and check the real call, message-draft, directions, navigation, filter, and article links. The automated release check verifies the built files; it does not contact the business or submit customer enquiries.

## Codex project handoff (October 2026)

This repository is structured for the Codex desktop app. The root `AGENTS.md` contains the authoritative instructions and `docs/CODEX-TASK.md` is the actionable continuation task. `design/` contains two concept screenshots and a screenshot of the implemented site.

To use it in Codex, open this repository folder as a **local project**, then ask Codex to execute `docs/CODEX-TASK.md`. Codex should handle repository creation, GitHub Pages configuration, and visual verification using an authenticated local GitHub session. An automated, non-destructive publishing helper is at `scripts/publish_github_pages.sh`. Do not report a live URL until the deployed site returns a successful response.
