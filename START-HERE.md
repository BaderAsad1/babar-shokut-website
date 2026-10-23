# Open this in Codex

This folder is the **complete Babar Shokut Electric Wear website source** prepared for the ChatGPT desktop Codex app. It is not merely a design prompt.

## Open
1. Extract the `babar-shokut-codex-project.zip` archive on your Mac.
2. Open **ChatGPT desktop → Codex** and choose this extracted **`babar-shokut-codex-project` folder** as the local project. (In Codex CLI: `cd .../babar-shokut-codex-project && codex`.)
3. Send Codex this message:

> Read AGENTS.md and docs/CODEX-TASK.md, then execute the entire task. Finish the website visual QA, create a standalone public GitHub repository BaderAsad1/babar-shokut-website, push the current code, enable free GitHub Pages, verify the homepage and blog on the real public URL, and give me the verified client link. Keep the preview noindex setting. Do not stop at instructions unless a required login genuinely needs my participation.

The project includes a publishing helper at `scripts/publish_github_pages.sh`. Codex can run it on a computer with a GitHub CLI session or use authenticated browser control. The script will not run without authentication or publish into unrelated repositories.

## Current status
- Local site builds and passes automated checks for 9 HTML pages and 320 local references.
- `preview` is true: the public demo will tell crawlers not to index it.
- GitHub repository creation and deployment have **not** been completed by the originating ChatGPT session; do not call it live until Codex publishes and verifies it.
