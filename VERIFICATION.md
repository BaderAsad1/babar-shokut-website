# Verification record

Checked on 21 October 2026 for the initial client preview.

## Automated release check

`python3 scripts/build.py` generated nine HTML pages. `python3 scripts/check.py` passed for all nine pages and 329 local references, including metadata, anchors, structured data, phone and WhatsApp configuration, image/font references, sitemap and preview crawl directives. JavaScript syntax passed `node --check assets/js/main.js`.

## Browser checks

- Reviewed the homepage, advice hub and article layout in the browser at desktop width.
- Reviewed the same three templates in 320px, 390px and 768px iframe viewports. Document scroll width matched client width after correcting a mobile AC-link layout issue.
- Verified that the mobile navigation opens and closes and that Escape restores the closed state.
- Verified that the inspection dialog opens, fits the phone viewport, and accepts appliance/city choices. An empty submission triggers native required-field validation.
- Verified the Fridges filter returns the two relevant guides, an unmatched query displays the empty-results state, and reset restores all five guides.
- Reviewed the current contact destinations and Google Maps entity link. No call or message was sent to the business.

Browser extension diagnostics were present in the testing environment; no application JavaScript error was observed. This is a targeted release check, not a formal accessibility audit, real-device certification or measured performance benchmark.

## Publishing and production

The site is configured as a publicly accessible client preview with `noindex`. Public deployment must be verified at its actual GitHub Pages URL before sharing it as a live site. Confirm the owner's intended WhatsApp destination and other launch details before changing the production indexing flag.

## Codex handoff re-verification — 23 October 2026

The source was repackaged as a Codex-ready project with `AGENTS.md`, handoff instructions and a GitHub Pages publication helper. Generated output is now cleaned before building, removing stale files. Typeface loads through the public Google Fonts stylesheet with a system fallback; no font files are distributed in the Codex handoff archive. Execute the current check for its authoritative local reference count. The initial browser review recorded above remains historical, not a newly repeated visual audit.

## Final browser QA — 23 October 2026

Repeated desktop (1440px) and mobile (390px) visual inspection of the homepage, advice index and washing-machine drainage article. Also checked all three templates at 320px and 768px: no horizontal document overflow. All images decoded successfully after loading lazy images. No application JavaScript errors were observed.

Fixed Python 3.9 compatibility in JSON-LD serialization and corrected malformed HTML that omitted the washing-machine option from the inspection selector. Added a release check for all three appliance choices. Build, release checks (nine pages, 320 local references), and JavaScript syntax checks pass.

Verified mobile menu open/close and Escape, required-field validation, appliance/city selection, mobile dialog fit and scrolling, and the generated WhatsApp draft URL. The draft targets +971552434708, includes the AED 50 inspection wording, and explicitly states that no appointment is confirmed. Intercepted the external window during testing; no customer message was sent. Verified the Fridges filter returns two guides, unmatched search shows the empty state, and reset restores all five guides. Phone and Maps destinations match the configured business details.

Preview remains enabled with noindex. Owner confirmation of WhatsApp availability and opening hours remains outstanding before production launch.

## Public deployment verified — 23 October 2026

- Public repository: https://github.com/BaderAsad1/babar-shokut-website
- Client preview: https://baderasad1.github.io/babar-shokut-website/
- GitHub Pages source: GitHub Actions (`build_type=workflow`).
- Successful build and deployment: https://github.com/BaderAsad1/babar-shokut-website/actions/runs/39921740152
- Deployed website source commit: `cb37c516ed3f403cc401d1b8220e45a030737597`.
- Actual HTTPS fetches and browser navigation returned HTTP 200 for the homepage, `/advice/`, and `/advice/washing-machine-not-draining/`. All three contained the expected content and noindex metadata. Browser checks found no broken images or horizontal overflow.
- Opened the verified public homepage in the user's Chrome browser for client review. This is a design preview, not an approved production SEO launch.

## Service-led design revision — 23 October 2026

User feedback superseded the initial visual concept: the first preview felt gimmicky. Research and design decisions are recorded in `docs/DESIGN-REFERENCE.md`. Revised the existing homepage, shared styles and advice presentation while preserving all nine pages, article content, business facts and enquiry behavior.

Removed promotional fee tiles, oversized slogans and the repeated washer image in the business section. Added visible desktop telephone contact, plain inspection pricing, service symptom lists, appliance-specific enquiry links and a practical address/contact panel. Reduced heading sizes and decorative styling throughout the advice hub and articles. Fixed dialog body scroll locking and aligned the navigation breakpoint with its CSS.

Re-ran browser QA at 1440px, 768px, 390px and 320px across homepage, advice hub and drainage article: all images loaded, no horizontal overflow. Verified menu open, Escape and reset at the desktop breakpoint; service preset selection; native required-city validation; draft-only WhatsApp URL and truthful status text; modal scroll lock, scroll restoration and focus return; Fridges filter, no-results state and five-guide reset. External message opening was intercepted. No message was sent. No application JavaScript errors were observed. Build, release check (nine pages, 319 references) and JS syntax pass. Preview/noindex remains enabled.

The service-led revision was deployed successfully from commit `0cd2968703fcb1bb5eca91d77e3d5c24fb0a2062`: https://github.com/BaderAsad1/babar-shokut-website/actions/runs/39927175842. Rechecked the live homepage on desktop and mobile, the advice hub and an article in the browser: HTTP 200, revised headings, no broken images, no overflow and noindex present. HTTPS requests to all eight content routes also returned HTTP 200. `design/revised-desktop-viewport.jpg` captures the deployed revision; full-page desktop and mobile captures are alongside it.

## Approved imagegen concept build — 23 October 2026

Implemented the approved concept in the existing nine-page site using real semantic HTML and responsive CSS. New versioned hero/washer/fridge illustrations were generated with built-in imagegen, optimized to WebP and documented in `assets/ASSET-NOTES.md`. Preserved the original five guide texts and source links; only their imagery and alt text changed. No font binaries are included. Updated font disclosure and all contact actions to Call us. Inspection for only AED 50 is accompanied by separate-repair-cost wording.

Visually inspected homepage, advice hub and drainage article at desktop 1440px and mobile 390px. Checked these templates at 320px and 768px as well: no broken images or horizontal document overflow. Examined homepage breakpoints from 320px to 1920px and corrected clipping in the small-screen price line. Checked mobile menu, About reveal, FAQs, appliance presets, required-city validation, modal fit/scroll lock/focus return, Fridges filter (two guides), unmatched search, and reset (five guides). Tested the generated WhatsApp draft with its external opening intercepted; no message was sent. No application JS errors observed. Build, static release check (nine HTML pages, 309 references) and node syntax pass. Preview/noindex remains enabled.

The approved concept implementation deployed from commit `75058015f1b25df58db7d292122b8265790efd83`. GitHub Actions build and Pages deployment succeeded: https://github.com/BaderAsad1/babar-shokut-website/actions/runs/39937202930. Browser verified the actual public homepage at desktop and mobile, advice index and drainage article: HTTP 200, premium assets/font loaded, no broken images, no horizontal overflow and noindex present. Separate HTTPS requests returned 200 for all eight content routes and all three new WebP assets. Verified the live offer markup and absence of Call Bilal links. The live preview remains https://baderasad1.github.io/babar-shokut-website/ .

## Company-led repair articles and UX revision — 23 October 2026

Rewrote all five articles to support company inspection enquiries, preserving routes and manufacturer/public reference links. Removed user-maintenance and self-repair walkthroughs. Updated the hub, card titles/excerpts, metadata and reading-time estimates. Content explains symptoms, inspection purpose, company coverage, the AED 50 inspection charge, separate repair costs and enquiry details without fabricated guarantees or credentials.

Added call and inspection actions near article introductions and an in-article enquiry panel. Header, mobile sticky action, inline panel, sidebar and concluding inspection actions carry the article's appliance and editable symptom text. User edits survive reopening. Moved the contents control before the body on mobile, made it collapsible and removed the duplicated lower mobile sidebar sales card. Retained desktop navigation and increased its label legibility. Corrected inherited link colour that hid an inline primary-button label. Kept the dialog close control visible while scrolling.

Browser-tested all five mobile article enquiry presets, required-city validation, editable text preservation, WhatsApp draft generation without sending, modal close/focus restoration, mobile/desktop contents states, Fridges filter, no-results reset and a search synonym. No application JavaScript errors observed. Desktop/mobile visual review and width checks at 320/390/768/1440px found no document overflow or broken images. Build, release check (nine pages, 319 local references) and JS syntax pass. Preview/noindex is unchanged.

Published this revision from `7a145f1fbba83cfe649f36f06e741f987fb173fb`; build and Pages deployment succeeded: https://github.com/BaderAsad1/babar-shokut-website/actions/runs/39938814018. Actual HTTPS requests returned HTTP 200 for homepage, blog hub and all five rewritten articles. Browser verified the live hub and two articles at desktop/mobile, including updated headings, no broken images, no overflow, retained noindex and article-specific mobile enquiry data.
