#!/usr/bin/env bash
# Creates a new public repository and publishes this reviewed site to GitHub Pages.
# Must run on a computer with an authenticated GitHub CLI session; no secrets in project files.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
REPO="${REPO:-BaderAsad1/babar-shokut-website}"
EXPECTED="BaderAsad1/babar-shokut-website"
if [[ "$REPO" != "$EXPECTED" ]]; then
  echo "Refusing unexpected target $REPO; expected $EXPECTED. Review script before changing owner/repo." >&2
  exit 2
fi

for cmd in git gh python3 curl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing command: $cmd. Install it through the official provider and retry." >&2
    exit 2
  fi
done
if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI authentication required. Run 'gh auth login' using an authorized browser/device flow, then retry." >&2
  exit 2
fi

python3 scripts/build.py
python3 scripts/check.py
if command -v node >/dev/null 2>&1; then node --check assets/js/main.js; fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b main
fi
CURRENT_BRANCH="$(git branch --show-current || true)"
if [[ -n "$CURRENT_BRANCH" && "$CURRENT_BRANCH" != "main" ]]; then
  echo "Expected the main branch, found $CURRENT_BRANCH. Stop and inspect the repository." >&2
  exit 2
fi

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Build Babar Shokut appliance repair client preview"
fi

if gh repo view "$REPO" --json name >/dev/null 2>&1; then
  echo "Repository exists: $REPO"
  EXPECTED_REMOTE="https://github.com/$REPO.git"
  if git remote get-url origin >/dev/null 2>&1; then
    REMOTE="$(git remote get-url origin)"
    case "$REMOTE" in
      "https://github.com/$REPO.git"|"git@github.com:${REPO}.git") ;;
      *) echo "Refusing to push: origin is $REMOTE rather than $REPO" >&2; exit 2 ;;
    esac
  else
    git remote add origin "$EXPECTED_REMOTE"
  fi
  git push -u origin main
else
  echo "Creating a new PUBLIC repository $REPO, as requested for the client preview."
  gh repo create "$REPO" --public --description "Babar Shokut Electric Wear appliance repair website and SEO advice guides" --source=. --remote=origin --push
fi

if ! gh api "repos/$REPO/pages" >/dev/null 2>&1; then
  echo "Enabling free GitHub Pages with Actions deployment source..."
  gh api -X POST "repos/$REPO/pages" -f build_type=workflow >/dev/null
else
  gh api -X PUT "repos/$REPO/pages" -f build_type=workflow >/dev/null
fi

echo "Starting GitHub Pages deployment workflow..."
gh workflow run deploy.yml --repo "$REPO" --ref main
RUN_ID="$(gh run list --repo "$REPO" --workflow deploy.yml --limit 1 --json databaseId --jq '.[0].databaseId')"
if [[ -z "$RUN_ID" || "$RUN_ID" == "null" ]]; then
  echo "No workflow run visible yet. Inspect Actions at https://github.com/$REPO/actions" >&2
  exit 1
fi
gh run watch "$RUN_ID" --repo "$REPO" --exit-status

PAGE_URL="$(gh api "repos/$REPO/pages" --jq .html_url)"
if [[ -z "$PAGE_URL" || "$PAGE_URL" == "null" ]]; then
  echo "Pages did not provide an HTML URL; inspect the deployment." >&2
  exit 1
fi
# Pages CDN publication may briefly lag behind the completed workflow.
for n in 1 2 3 4 5 6; do
  if curl -LfsS --max-time 30 "$PAGE_URL" >/dev/null &&
     curl -LfsS --max-time 30 "${PAGE_URL%/}/advice/" >/dev/null; then
    echo "Verified public client preview: $PAGE_URL"
    echo "Repository: https://github.com/$REPO"
    exit 0
  fi
  echo "Deployment completed; waiting for public site to become reachable ($n/6)..."
  sleep 10
done

echo "Workflow succeeded but public page verification is pending: $PAGE_URL" >&2
exit 1
