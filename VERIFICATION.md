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
