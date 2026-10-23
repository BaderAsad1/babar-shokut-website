#!/usr/bin/env python3
"""Check the built site's release invariants with the Python standard library."""

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
ERRORS = []


def fail(message):
    ERRORS.append(message)


def phone_digits(value):
    digits = re.sub(r"\D", "", value)
    if digits.startswith("00971"):
        return digits[2:]
    return "971" + digits[1:] if digits.startswith("0") else digits


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.raw = path.read_text(encoding="utf-8")
        self.title_count = self.h1_count = 0
        self.in_title = self.in_h1 = self.in_script = False
        self.title, self.h1, self.visible = [], [], []
        self.ids, self.duplicate_ids = set(), set()
        self.meta, self.links, self.canonicals = {}, [], []
        self.json_ld, self.whatsapp_numbers = [], []
        self.ld_parts = None
        self.select_id = None
        self.select_options = {}
        self.feed(self.raw)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        identifier = attrs.get("id")
        if tag == "select":
            self.select_id = identifier
            self.select_options[identifier] = []
        if tag == "option" and self.select_id:
            self.select_options[self.select_id].append(attrs.get("value"))
        if identifier:
            if identifier in self.ids:
                self.duplicate_ids.add(identifier)
            self.ids.add(identifier)
        if tag == "title":
            self.title_count += 1
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        if tag == "script":
            self.in_script = True
            if attrs.get("type", "").lower() == "application/ld+json":
                self.ld_parts = []
        if tag == "meta":
            name = attrs.get("name", attrs.get("property", "")).lower()
            self.meta.setdefault(name, []).append(attrs.get("content", ""))
            if name in {"og:image", "og:url", "twitter:image"}:
                self.links.append((name, attrs.get("content", "")))
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href", ""))
        for attribute in ("href", "src", "poster"):
            if attribute in attrs:
                self.links.append((f"{tag}[{attribute}]", attrs[attribute] or ""))
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            for candidate in attrs["srcset"].split(","):
                if candidate.strip():
                    self.links.append((f"{tag}[srcset]", candidate.strip().split()[0]))
        if "data-whatsapp" in attrs:
            self.whatsapp_numbers.append(attrs["data-whatsapp"])

    def handle_endtag(self, tag):
        if tag == "select":
            self.select_id = None
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False
        if tag == "script":
            if self.ld_parts is not None:
                self.json_ld.append("".join(self.ld_parts))
                self.ld_parts = None
            self.in_script = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_h1:
            self.h1.append(data)
        if self.ld_parts is not None:
            self.ld_parts.append(data)
        if not self.in_script:
            self.visible.append(data)


def main():
    if not OUT.is_dir():
        print("FAIL: dist is missing. Run python3 scripts/build.py first.", file=sys.stderr)
        return 1
    config = json.loads((ROOT / "site-config.json").read_text(encoding="utf-8"))
    articles = json.loads((ROOT / "content/articles.json").read_text(encoding="utf-8"))
    base = config["siteUrl"].rstrip("/") + "/"
    base_parts = urlsplit(base)
    if base_parts.scheme != "https" or not base_parts.netloc:
        fail("siteUrl must be an absolute HTTPS URL.")
    if base_parts.query or base_parts.fragment:
        fail("siteUrl must not contain a query or fragment.")
    base_path = unquote(base_parts.path)
    preview = config.get("preview")
    if not isinstance(preview, bool):
        fail("preview must be a JSON boolean.")

    expected = {"index.html", "advice/index.html", "privacy/index.html", "404.html"}
    expected.update(f"advice/{article['slug']}/index.html" for article in articles)
    found = {path.relative_to(OUT).as_posix() for path in OUT.rglob("*.html")}
    if found != expected:
        fail(f"Page set differs: missing {sorted(expected - found)}, unexpected {sorted(found - expected)}.")
    documents = {}
    for relative in sorted(found & expected):
        try:
            documents[relative] = Document(OUT / relative)
        except (OSError, UnicodeError) as exc:
            fail(f"{relative}: cannot read HTML: {exc}")

    checked_links = 0

    def check_url(owner, reference, location):
        nonlocal checked_links
        if not reference:
            fail(f"{owner}: empty {location} URL.")
            return
        scheme = urlsplit(reference).scheme.lower()
        if scheme in {"tel", "mailto", "data", "blob"}:
            return
        if scheme and scheme not in {"http", "https"}:
            fail(f"{owner}: unsupported URL scheme in {location}: {reference}")
            return
        resolved = urlsplit(urljoin(urljoin(base, owner), reference))
        if resolved.netloc.lower() != base_parts.netloc.lower():
            return  # External availability is intentionally outside a static release check.
        decoded_path = unquote(resolved.path)
        if not decoded_path.startswith(base_path):
            fail(f"{owner}: {location} escapes the configured site path: {reference}")
            return
        target = (OUT / decoded_path[len(base_path):]).resolve()
        if not target.is_relative_to(OUT.resolve()):
            fail(f"{owner}: {location} escapes dist: {reference}")
            return
        if target.is_dir():
            target /= "index.html"
        if not target.is_file():
            fail(f"{owner}: missing local target for {location}: {reference}")
            return
        checked_links += 1
        fragment = unquote(resolved.fragment)
        if fragment and target.suffix.lower() == ".html":
            target_document = documents.get(target.relative_to(OUT).as_posix())
            if target_document and fragment not in target_document.ids:
                fail(f"{owner}: missing fragment #{fragment} in {target.relative_to(OUT)}.")

    old_phones = [
        r"(?<!\d)(?:\+?971[\s().-]*|0)56[\s().-]*427[\s().-]*7786(?!\d)",
        r"(?<!\d)(?:\+?971[\s().-]*|0)50[\s().-]*379[\s().-]*9512(?!\d)",
        r"(?<!\d)(?:\+?971[\s().-]*|0)55[\s().-]*382[\s().-]*8512(?!\d)",
    ]
    placeholder = re.compile(
        r"lorem\s+ipsum|\b(?:TODO|TBD|CHANGE_ME|REPLACE_ME)\b|"
        r"example\.(?:com|org)|yourdomain\.|\{\{[^{}]+\}\}|"
        r"https?://(?:localhost|127\.0\.0\.1)", re.IGNORECASE
    )
    configured_phone = phone_digits(config["phone"])
    configured_whatsapp = phone_digits(config["whatsapp"])
    titles = Counter()
    for relative, doc in documents.items():
        if relative != "404.html" and doc.select_options.get("appliance") != ["", "Washing machine", "Fridge", "AC"]:
            fail(f"{relative}: inspection form must offer all three appliance options.")
        if re.search(r"call\s+bilal", " ".join(doc.visible), re.IGNORECASE):
            fail(f"{relative}: use the approved Call us contact label.")
        title = "".join(doc.title).strip()
        titles[title] += 1
        if doc.title_count != 1 or not title:
            fail(f"{relative}: expected one nonempty title.")
        if doc.h1_count != 1 or not "".join(doc.h1).strip():
            fail(f"{relative}: expected one nonempty H1.")
        descriptions = doc.meta.get("description", [])
        if len(descriptions) != 1 or not descriptions[0].strip():
            fail(f"{relative}: expected one nonempty meta description.")
        if doc.duplicate_ids:
            fail(f"{relative}: duplicate IDs: {', '.join(sorted(doc.duplicate_ids))}.")
        robots = doc.meta.get("robots", [])
        if len(robots) != 1:
            fail(f"{relative}: expected one robots meta tag.")
        directives = set(re.split(r"[,\s]+", " ".join(robots).lower()))
        should_noindex = preview or relative == "404.html"
        if should_noindex != ("noindex" in directives):
            fail(f"{relative}: robots noindex does not match preview/404 state.")
        if "noindex" in directives and "index" in directives:
            fail(f"{relative}: conflicting index/noindex directives.")
        if relative != "404.html":
            if len(doc.canonicals) != 1 or not doc.canonicals[0].startswith(base):
                fail(f"{relative}: expected one canonical under siteUrl.")
            if not doc.json_ld:
                fail(f"{relative}: structured data is missing.")
            telephones = [phone_digits(urlsplit(value).path) for _, value in doc.links if value.startswith("tel:")]
            if not telephones or any(number != configured_phone for number in telephones):
                fail(f"{relative}: telephone links must use the configured phone.")
            if config["phoneDisplay"] not in " ".join(doc.visible):
                fail(f"{relative}: the configured display phone is missing.")
            if not doc.whatsapp_numbers or any(phone_digits(number) != configured_whatsapp for number in doc.whatsapp_numbers):
                fail(f"{relative}: the WhatsApp enquiry destination differs from config.")
        for index, block in enumerate(doc.json_ld, 1):
            try:
                data = json.loads(block)
                if not isinstance(data, (dict, list)) or not data:
                    raise ValueError("structured data must be a nonempty object or array")
            except (ValueError, json.JSONDecodeError) as exc:
                fail(f"{relative}: invalid JSON-LD block {index}: {exc}")
        if any(re.search(pattern, doc.raw) for pattern in old_phones):
            fail(f"{relative}: an obsolete directory/storefront phone remains.")
        match = placeholder.search(doc.raw)
        if match:
            fail(f"{relative}: dummy content remains: {match.group(0)!r}.")
        for location, reference in doc.links:
            check_url(relative, reference, location)

    for title, count in titles.items():
        if count > 1:
            fail(f"Duplicate page title on {count} pages: {title!r}.")
    for css in OUT.rglob("*.css"):
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css.read_text(encoding="utf-8")):
            check_url(css.relative_to(OUT).as_posix(), match.group(2), "CSS url()")

    robots_file = OUT / "robots.txt"
    if not robots_file.is_file():
        fail("robots.txt is missing.")
    else:
        robots_text = robots_file.read_text(encoding="utf-8")
        if re.search(r"^\s*Disallow\s*:\s*/\s*$", robots_text, re.I | re.M):
            fail("robots.txt blocks all crawling; crawlers must be able to read preview noindex.")
        if not re.search(r"^\s*Allow\s*:\s*/\s*$", robots_text, re.I | re.M):
            fail("robots.txt must allow crawling of the public site.")
        if preview and re.search(r"^\s*Sitemap\s*:", robots_text, re.I | re.M):
            fail("Preview robots.txt must not advertise a sitemap.")
        if not preview and f"Sitemap: {base}sitemap.xml" not in robots_text:
            fail("Production robots.txt must advertise the configured sitemap.")
    try:
        sitemap = ET.parse(OUT / "sitemap.xml")
        locations = [node.text or "" for node in sitemap.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        expected_urls = {urljoin(base, name.removesuffix("index.html")) for name in expected if name != "404.html"}
        if len(locations) != len(set(locations)) or set(locations) != expected_urls:
            fail("sitemap.xml must contain each public content route exactly once, excluding 404.")
        for location in locations:
            check_url("sitemap.xml", location, "sitemap loc")
    except (OSError, ET.ParseError) as exc:
        fail(f"sitemap.xml cannot be parsed: {exc}")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} release issue(s):", file=sys.stderr)
        for message in ERRORS:
            print(f"  - {message}", file=sys.stderr)
        return 1
    mode = "public preview, noindex" if preview else "indexable production"
    print(f"PASS: {len(documents)} HTML pages; {checked_links} local references; metadata, anchors, structured data, contact destinations, assets and crawl directives checked ({mode}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
