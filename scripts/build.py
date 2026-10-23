#!/usr/bin/env python3
"""Build a dependency-free, crawlable website with relative links for GitHub Pages."""
from pathlib import Path
from html import escape
from urllib.parse import urljoin
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
C = json.loads((ROOT / "site-config.json").read_text())
ARTICLES = json.loads((ROOT / "content/articles.json").read_text())
BY_SLUG = {a["slug"]: a for a in ARTICLES}
BASE = C["siteUrl"].rstrip("/") + "/"
E = lambda value: escape(str(value), quote=True)

def icon(name="arrow"):
    paths = {
      "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
      "north": '<path d="M6 18 18 6M6 6h12v12"/>',
      "phone": '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.7 19.7 0 0 1-8.6-3.1 19.4 19.4 0 0 1-6-6A19.7 19.7 0 0 1 1.1 3.7 2 2 0 0 1 3.1 1.5h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L7 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2.1Z"/>',
      "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
      "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
      "ac": '<rect x="2" y="4" width="20" height="11" rx="2"/><path d="M6 11h12M7 15v4m5-4v6m5-6v4"/>',
      "close": '<path d="m6 6 12 12M6 18 18 6"/>',
      "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
      "check": '<path d="m5 12 4 4L19 6"/>',
      "whatsapp": '<path d="M21 11.5a9 9 0 0 1-13.4 7.9L3 21l1.6-4.6A9 9 0 1 1 21 11.5Z"/><path d="M8 7c-1 3 2 6 5 7l2-1-1-2-2 1-2-2 1-2-2-1Z"/>',
    }
    return f'<svg class="icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>'

def img(rel, name, alt, *, eager=False, klass=""):
    size = (1448, 1086) if name == "hero.webp" else (1200, 800)
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return f'<img class="{klass}" src="{rel}assets/images/{name}" alt="{E(alt)}" width="{size[0]}" height="{size[1]}" {load} decoding="async">'

def brand(rel):
    return f'<a class="brand" href="{rel}" aria-label="Babar Shokut Electric Wear home"><span class="brand-mark" aria-hidden="true">B</span><span class="brand-text"><strong>Babar Shokut</strong><small>ELECTRIC WEAR</small></span></a>'

def enquiry(label="Request an inspection", style="button-primary", service="", arrow=True):
    service_attr = f' data-service="{E(service)}"' if service else ""
    return f'<a class="button {style} open-enquiry" href="#contact"{service_attr}>{E(label)}{icon("north") if arrow else ""}</a>'

def header(rel, page):
    active = ' aria-current="page"' if page == "advice" else ""
    links = f'<a href="{rel}#services">Services</a><a href="{rel}#how-it-works">How it works</a><a href="{rel}#our-story">Location &amp; coverage</a><a href="{rel}advice/"{active}>Advice</a>'
    return f'''<a class="skip-link" href="#main-content">Skip to content</a>
<div class="announcement"><div class="container"><span>Sharjah <span aria-hidden="true">·</span> Dubai <span aria-hidden="true">·</span> Ajman</span><span>Serving customers since 2012</span></div></div>
<header class="site-header"><div class="container header-inner">{brand(rel)}<nav class="desktop-nav" aria-label="Main navigation">{links}</nav><a class="header-phone" href="tel:{C["phone"]}">{icon("phone")}<span>{C["phoneDisplay"]}</span></a>{enquiry(style="button-primary button-small", arrow=False)}<button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="mobile-menu">{icon("menu")}</button></div>
<nav class="mobile-menu" id="mobile-menu" aria-label="Mobile navigation" hidden>{links}<a href="{rel}#contact">Contact Bilal</a></nav></header>'''

def footer(rel):
    return f'''<footer class="site-footer" id="contact"><div class="container footer-grid">
<div>{brand(rel)}<p>Washing machines <span aria-hidden="true">·</span> Fridges <span aria-hidden="true">·</span> AC repair</p><p class="footer-small">{E(C["listingName"])}</p></div>
<div><h2>Talk to Bilal</h2><a class="footer-phone" href="tel:{C["phone"]}">{C["phoneDisplay"]}</a><p>Dubai <span aria-hidden="true">·</span> Sharjah <span aria-hidden="true">·</span> Ajman</p><a href="{rel}advice/">Appliance advice {icon("arrow")}</a></div>
<div><h2>Find the shop</h2><address>Building 25, Shop 1<br>Al Yarmook Street 13<br>Sharjah, UAE</address><a href="{C["mapsUrl"]}" target="_blank" rel="noopener noreferrer">Get directions {icon("north")}</a></div>
</div><div class="container footer-bottom"><p>© 2026 Babar Shokut Electric Wear</p><p>Serving customers since 2012</p><a href="{rel}privacy/">Privacy</a></div></footer>
<div class="mobile-contact" aria-label="Quick contact"><a href="tel:{C["phone"]}">{icon("phone")} Call Bilal</a>{enquiry("Request inspection", "button-primary", arrow=False)}</div>
{booking_dialog()}'''

def booking_dialog():
    return f'''<dialog class="booking-dialog" id="inspection-dialog" aria-labelledby="inspection-title" aria-describedby="inspection-intro" data-whatsapp="{C["whatsapp"]}">
<div class="dialog-header"><div><p class="eyebrow">INSPECTION ENQUIRY</p><h2 id="inspection-title">Request an inspection.</h2></div><button class="dialog-close" type="button" aria-label="Close inspection request">{icon("close")}</button></div>
<p id="inspection-intro">Tell Bilal a little about your appliance. The inspection fee is <strong>AED 50</strong>.</p>
<form id="inspection-form"><div class="form-grid">
<div class="field"><label for="appliance">Your appliance</label><select id="appliance" name="appliance" required><option value="">Choose an appliance</option><option value="Washing machine">Washing machine</option><option value="Fridge">Fridge</option><option value="AC">AC</option></select></div>
<div class="field"><label for="city">Your city</label><select id="city" name="city" required><option value="">Choose your city</option><option>Sharjah</option><option>Dubai</option><option>Ajman</option></select></div>
</div><div class="field"><label for="issue">What's happening? <span class="optional">(optional)</span></label><textarea id="issue" name="issue" rows="3" maxlength="600" placeholder="For example: my washing machine stops before draining."></textarea></div>
<p class="form-note">This opens WhatsApp with your enquiry. You choose when to send it. The inspection time and any repair costs are arranged with Bilal.</p>
<button class="button button-primary" type="submit">{icon("whatsapp")} Continue in WhatsApp</button>
<p class="form-status" id="enquiry-status" role="status"></p>
<a class="text-link" id="whatsapp-fallback" target="_blank" rel="noopener noreferrer" hidden>Open your WhatsApp enquiry {icon("north")}</a>
</form><div class="dialog-actions"><span>Prefer to speak?</span><a href="tel:{C["phone"]}">{icon("phone")} {C["phoneDisplay"]}</a></div>
</dialog>'''

def cta(variant="home"):
    return f'''<section class="cta-section" aria-label="Request an appliance inspection"><div class="container"><div class="cta-panel"><div><p class="eyebrow">CONTACT BILAL</p><h2>Tell us about your appliance.</h2><p>Call to discuss the issue, or prepare an inspection enquiry.</p></div><div class="cta-actions"><a class="cta-phone" href="tel:{C["phone"]}">{C["phoneDisplay"]}</a>{enquiry(style="button-white", arrow=False)}<small>AED 50 inspection. Repair costs discussed separately.</small></div></div></div></section>'''

def article_card(a, rel, *, journal=False, featured=False):
    href = f'{rel}advice/{a["slug"]}/'
    short = a["title"].split("?")[0] + "?"
    classes = "journal-card" if journal else "article-card"
    attrs = "" if journal else f' data-category="{a["category"]}" data-search="{E(a["title"] + " " + a["excerpt"] + " " + a["categoryLabel"])}"' + (' data-featured="true" hidden' if featured else "")
    if journal:
        return f'<article class="{classes}"><a class="journal-image" href="{href}" tabindex="-1" aria-hidden="true">{img(rel,a["image"],"")}</a><div><p class="card-category">{E(a["categoryLabel"])}</p><h3><a href="{href}">{E(short)}</a></h3><a class="text-link" href="{href}">Read the guide {icon("arrow")}</a></div></article>'
    return f'''<article class="{classes}"{attrs}><figure><a href="{href}" tabindex="-1" aria-hidden="true">{img(rel,a["image"],"")}</a></figure><div class="card-content"><p class="card-category">{E(a["categoryLabel"])}</p><h2><a href="{href}">{E(short)} {icon("arrow")}</a></h2><p class="card-description">{E(a["excerpt"])}</p><p class="card-meta">{a["readMinutes"]} min read</p></div></article>'''

def head(title, description, rel, path="", *, article=None):
    canonical = urljoin(BASE, path)
    robots = "noindex, nofollow" if C["preview"] else "index, follow"
    schema = {
      "@context":"https://schema.org", "@type":"LocalBusiness", "name":C["name"],
      "description":"Washing machine, fridge and AC repair serving Sharjah, Dubai and Ajman.",
      "url":BASE, "telephone":C["phone"], "foundingDate":str(C["founded"]),
      "address":{"@type":"PostalAddress","streetAddress":"Building 25, Shop 1, Al Yarmook Street 13","addressLocality":"Sharjah","addressRegion":"Sharjah","addressCountry":"AE"},
      "geo":{"@type":"GeoCoordinates","latitude":C["latitude"],"longitude":C["longitude"]},
      "areaServed":[{"@type":"City","name":s} for s in C["serviceAreas"]],
      "hasMap":C["mapsUrl"],"image":urljoin(BASE,"assets/images/hero.webp")
    }
    if article:
        schema = {"@context":"https://schema.org","@type":"BlogPosting","headline":article["title"],"description":article["excerpt"],"image":urljoin(BASE,"assets/images/"+article["image"]),"mainEntityOfPage":canonical,"publisher":{"@type":"Organization","name":C["name"],"url":BASE}}
    og_image = article["image"] if article else "hero.webp"
    schema_json = json.dumps(schema, ensure_ascii=False).replace("</", "<\\/")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="robots" content="{robots}"><meta name="theme-color" content="#F6F3ED"><meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="canonical" href="{canonical}"><link rel="icon" href="{rel}assets/images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{rel}assets/css/styles.css"><script defer src="{rel}assets/js/main.js"></script>
<meta property="og:type" content="{"article" if article else "website"}"><meta property="og:site_name" content="{E(C["name"])}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{urljoin(BASE,"assets/images/"+og_image)}"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{schema_json}</script></head>'''

def page(title, description, rel, body, *, kind="home", path="", article=None):
    return head(title,description,rel,path,article=article)+f'<body class="page-{kind}">'+header(rel,kind)+body+footer(rel)+'</body></html>'

def homepage():
    r = "./"
    services = ""
    for title, image_name, alt, desc, symptoms, service in [
       ("Washing machine repair", "washer.webp", "Close-up of a front-loading washing machine drum", "Tell Bilal what happens during the wash, rinse or spin cycle.", ["Not draining or spinning", "Leaks or unusual noise", "Cycle stops or an error appears"], "Washing machine"),
       ("Fridge repair", "fridge.webp", "Refrigerator with an open door in a warm neutral kitchen", "Describe any change in cooling, noise or the way the door closes.", ["Not cooling as expected", "Frost build-up or water leaks", "Door not sealing properly"], "Fridge")]:
        symptoms_html = "".join(f'<li>{E(symptom)}</li>' for symptom in symptoms)
        services += f'''<article class="service-card"><figure>{img(r,image_name,alt)}</figure><div class="service-card-body"><h3>{title}</h3><p>{desc}</p><ul class="service-symptoms">{symptoms_html}</ul><a class="text-link open-enquiry" href="#contact" data-service="{service}">Enquire about {service.lower()} repair {icon("arrow")}</a></div></article>'''
    faqs = [
      ("How much is the inspection?", "The inspection fee is AED 50. This is the inspection charge, not the total repair price. Speak with Bilal about what your appliance needs and the repair cost."),
      ("Which areas do you cover?", "The business serves customers in Sharjah, Dubai and Ajman. Share your city and location when you enquire so the visit arrangements can be discussed."),
      ("What appliances do you repair?", "Washing machines and fridges are the main focus. AC repair is also available. Let Bilal know the make, model and symptoms when you call."),
      ("Does an enquiry confirm a visit?", "No. The form prepares a WhatsApp draft for you to review and send. Inspection availability, visit arrangements and repair costs are discussed with Bilal."),
      ("Where is the shop?", "Building 25, Shop 1, Al Yarmook Street 13, Sharjah, UAE. Open the Google Maps directions link to find the business listing.")
    ]
    faq_html = "".join(f'<details><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>' for q,a in faqs)
    body = f'''<main id="main-content">
<section class="hero"><div class="container hero-grid"><div class="hero-copy"><p class="eyebrow">BABAR SHOKUT ELECTRIC WEAR · SINCE 2012</p><h1>Washing machine<br>&amp; fridge repair.</h1><p class="hero-description">Serving Sharjah, Dubai and Ajman. Speak directly with Bilal about the problem and arrange an inspection.</p><div class="hero-actions"><a class="button button-primary" href="tel:{C["phone"]}">{icon("phone")} Call Bilal</a>{enquiry(style="button-outline", arrow=False)}</div><div class="inspection-note"><strong>AED 50 inspection</strong><span>The inspection fee is separate from the repair cost.</span></div><a class="hero-location" href="#our-story">{icon("pin")} Based in Al Yarmook, Sharjah</a></div><figure class="hero-visual">{img(r,"hero.webp","Illustration of a washing machine and stainless-steel fridge in a home",eager=True)}<figcaption>Illustrative appliance image</figcaption></figure></div></section>
<section class="services section" id="services"><div class="container"><div class="section-heading split-heading"><div><p class="eyebrow">REPAIR SERVICES</p><h2>What needs repairing?</h2></div><p class="section-intro">Start with the appliance and the symptoms.<br>Bilal can discuss the next step with you.</p></div><div class="service-grid">{services}</div><div class="ac-strip"><div class="ac-icon">{icon("ac")}</div><div><h3>AC repair is also available.</h3><p>For cooling issues, share what you are noticing with Bilal.</p></div><a class="text-link open-enquiry" href="#contact" data-service="AC">Enquire about AC repair {icon("arrow")}</a></div></div></section>
<section class="process section" id="how-it-works"><div class="container"><div class="section-heading"><p class="eyebrow">THE PROCESS</p><h2>From enquiry to inspection.</h2></div><div class="process-grid"><article class="step"><span class="step-number">01</span><div class="step-text"><h3>Describe the problem</h3><p>Call Bilal or prepare an enquiry. Share your appliance, city and what has changed.</p></div></article><article class="step"><span class="step-number">02</span><div class="step-text"><h3>Discuss an inspection</h3><p>The inspection fee is AED 50. Confirm availability and visit arrangements with Bilal.</p></div></article><article class="step"><span class="step-number">03</span><div class="step-text"><h3>Discuss the repair</h3><p>The inspection helps identify what is needed. Repair work and costs are discussed separately.</p></div></article></div></div></section>
<section class="story section" id="our-story"><div class="container story-grid"><div class="story-copy" id="areas"><p class="eyebrow">LOCATION &amp; COVERAGE</p><h2>Based in Sharjah.<br>Serving three emirates.</h2><p>Babar Shokut Electric Wear is based in Al Yarmook. Bilal, the owner, has been serving customers since 2012.</p><p>For washing machine, fridge or AC repair in Sharjah, Dubai or Ajman, share your location when you enquire.</p><a class="text-link" href="{C["mapsUrl"]}" target="_blank" rel="noopener noreferrer">View the business on Google Maps {icon("north")}</a></div><div class="location-panel"><p class="eyebrow">FIND THE SHOP</p><address>Building 25, Shop 1<br>Al Yarmook Street 13<br>Sharjah, UAE</address><a class="text-link" href="{C["mapsUrl"]}" target="_blank" rel="noopener noreferrer">Get directions {icon("north")}</a><div class="location-contact"><span>Speak with Bilal</span><a href="tel:{C["phone"]}">{C["phoneDisplay"]}</a><p>Share the appliance make, model and symptoms when you call.</p></div></div></div></section>
<section class="journal section"><div class="container"><div class="section-heading split-heading"><div><p class="eyebrow">APPLIANCE ADVICE</p><h2>Understand the problem first.</h2></div><a class="text-link" href="advice/">View all five guides {icon("arrow")}</a></div><p class="journal-intro">Practical, source-backed guidance. Always follow the instructions for your exact model.</p><div class="journal-grid">{article_card(ARTICLES[0],r,journal=True)}{article_card(ARTICLES[1],r,journal=True)}</div></div></section>
<section class="faq section"><div class="container faq-layout"><div><p class="eyebrow">COMMON QUESTIONS</p><h2>Before you arrange<br>an inspection.</h2><p>Have another question?<br><a class="text-link" href="tel:{C["phone"]}">Call Bilal {icon("arrow")}</a></p></div><div class="faq-items">{faq_html}</div></div></section>
{cta()}</main>'''
    return page("Washing Machine & Fridge Repair | Babar Shokut Electric Wear", "Washing machine, fridge and AC repair across Sharjah, Dubai and Ajman. Based in Al Yarmook, serving customers since 2012. AED 50 inspection fee.", r, body)

def advice():
    r="../"; a=ARTICLES[0]
    categories=[("all","All guides"),("washing-machines","Washing machines"),("fridges","Fridges"),("ac-care","AC care")]
    buttons="".join(f'<button class="filter-button" type="button" data-category="{key}" aria-pressed="{"true" if key=="all" else "false"}">{label}</button>' for key,label in categories)
    cards="".join(article_card(x,r,featured=i==0) for i,x in enumerate(ARTICLES))
    topics="".join(f'<button type="button" data-topic="{E(s)}">{s}</button>' for s in ["Not draining","Not cooling","Making noise","Door seal","AC"])
    body=f'''<main class="advice-main" id="main-content"><div class="container"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../">Home</a><span aria-hidden="true">/</span><span aria-current="page">Advice</span></nav><header class="advice-intro"><p class="eyebrow">APPLIANCE ADVICE</p><h1>Appliance care &amp;<br>repair guides.</h1><p>Five practical guides to common washer, fridge and AC problems.</p></header>
<div class="advice-toolbar"><div class="category-tabs" role="group" aria-label="Filter guides by appliance">{buttons}</div><div class="search-field">{icon("search")}<label class="sr-only" for="guide-search">Search the guides</label><input type="search" id="guide-search" placeholder="Search the guides" autocomplete="off"></div></div>
<section class="featured-guide" aria-labelledby="featured-title"><figure>{img(r,"washer.webp","Close-up of a washing machine drum",eager=True)}</figure><div class="featured-content"><p class="eyebrow">FEATURED · WASHING MACHINES</p><h2 id="featured-title">Washing machine<br>not draining?</h2><p class="featured-deck">What to check before booking a repair.</p><p>Understand what to look for, what to note, and when to ask for help.</p><a class="button button-primary" href="{a["slug"]}/">Read the guide {icon("north")}</a><span class="card-meta">{a["readMinutes"]} min read</span></div></section>
<section class="articles-section" aria-labelledby="guides-heading"><div class="section-heading split-heading"><h2 id="guides-heading">Browse the guides.</h2><button class="text-link" type="button" id="clear-filters" hidden>Clear filters {icon("close")}</button></div><p class="result-count sr-only" aria-live="polite" aria-atomic="true">5 guides available</p><div class="articles-grid">{cards}</div><div class="no-results" hidden><h3>No guides match that search.</h3><p>Try “fridge”, “draining” or “noise”, or clear your filters.</p><button class="button button-outline" type="button" data-reset-filters>Show all guides</button></div></section>
<section class="problem-topics" aria-label="Common appliance problems"><h2>Start with the problem.</h2><div class="topic-buttons">{topics}</div></section></div>{cta("advice")}</main>'''
    return page("Appliance Care & Repair Guides | Babar Shokut Electric Wear","Practical washing machine, fridge and AC care guides. Understand common symptoms, safe checks and when to ask for a repair inspection.",r,body,kind="advice",path="advice/")

def article(a):
    r="../../"
    sections=[]
    for s in a["sections"]:
        text="".join(f'<p>{E(p)}</p>' for p in s["paragraphs"])
        bullets="<ul>"+"".join(f'<li>{E(b)}</li>' for b in s["bullets"])+"</ul>" if s.get("bullets") else ""
        sections.append(f'<section class="article-section" id="{s["id"]}"><h2>{E(s["heading"])}</h2>{text}{bullets}</section>')
    toc="".join(f'<li><a href="#{s["id"]}">{E(s["heading"])}</a></li>' for s in a["sections"])
    sources="".join(f'<li><a href="{E(s["url"])}" target="_blank" rel="noopener noreferrer">{E(s["title"])} {icon("north")}</a></li>' for s in a["sources"])
    related="".join(article_card(BY_SLUG[s],r,journal=True) for s in a["relatedSlugs"][:2])
    appliance={"washing-machines":"Washing machine","fridges":"Fridge","ac-care":"AC"}[a["category"]]
    body=f'''<main id="main-content"><header class="article-header container"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../../">Home</a><span aria-hidden="true">/</span><a href="../">Advice</a><span aria-hidden="true">/</span><span>{E(a["categoryLabel"])}</span></nav><p class="eyebrow">{E(a["categoryLabel"])}</p><h1>{E(a["title"])}</h1><p class="article-deck">{E(a["intro"])}</p><div class="article-meta"><span>Appliance care guide</span><span aria-hidden="true">·</span><span>{a["readMinutes"]} min read</span></div></header><div class="article-hero container"><figure>{img(r,a["image"],a["imageAlt"],eager=True)}</figure></div>
<div class="article-layout container"><article class="article-content" aria-label="Guide"><div class="safety-note"><strong>Before you start</strong><p>{E(a.get("safetyNote","Follow your appliance's model-specific manual and stop if you are unsure."))}</p></div>{"".join(sections)}<section class="article-section sources-list"><h2>Sources and further reading</h2><p>This guide draws on the following manufacturer and public guidance. Always check the manual for your exact model.</p><ul>{sources}</ul></section></article><aside class="article-sidebar" aria-label="Guide navigation and help"><nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>{toc}</ol></nav><div class="inspection-card"><p class="eyebrow">SPEAK WITH BILAL</p><h2>Arrange an<br>inspection.</h2><strong class="inspection-price">AED 50</strong><p>Inspection fee</p>{enquiry("Request an inspection","button-white",appliance)}<small>Dubai · Sharjah · Ajman</small></div></aside></div>
<section class="related-guides section"><div class="container"><div class="section-heading split-heading"><h2>Related appliance guides.</h2><a class="text-link" href="../">All guides {icon("arrow")}</a></div><div class="journal-grid">{related}</div></div></section>{cta("article")}</main>'''
    return page(a["title"]+" | Babar Shokut",a["excerpt"],r,body,kind="article",path="advice/"+a["slug"]+"/",article=a)

def privacy():
    body=f'''<main class="container article-header" id="main-content"><nav class="breadcrumb" aria-label="Breadcrumb"><a href="../">Home</a><span>/</span><span>Privacy</span></nav><h1>A simple privacy note.</h1><div class="article-content"><p>This website provides information about Babar Shokut Electric Wear and ways to enquire about appliance repairs.</p><h2>Your enquiry</h2><p>The inspection form prepares a WhatsApp message on your device. Your appliance details, city and optional description are not submitted to a website database. If you choose to continue, WhatsApp opens the prepared enquiry and you decide whether to send it.</p><h2>External services</h2><p>Telephone, WhatsApp, Google Maps and source links open external services. Those services handle information under their own privacy policies. This website is hosted on GitHub Pages; GitHub may process technical request information to provide and secure hosting. The site also requests the Manrope web font from Google Fonts, which involves connecting to Google-controlled servers. System fonts are used as a fallback if it does not load.</p><h2>Cookies and analytics</h2><p>This website does not add advertising trackers, analytics cookies or a customer account system. The guide filters work in your browser.</p><h2>Questions</h2><p>For a question about an enquiry made to the business, call <a href="tel:{C["phone"]}">{C["phoneDisplay"]}</a>.</p></div></main>'''
    return page("Privacy | Babar Shokut Electric Wear","How this website handles inspection enquiries and external links.","../",body,kind="article",path="privacy/")

def write(path, content):
    target=OUT/path
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(content,encoding="utf-8")

def main():
    # Generate a clean publishable tree; old outputs must not leak stale assets.
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(exist_ok=True)
    shutil.copytree(ROOT/"assets",OUT/"assets",dirs_exist_ok=True,ignore=shutil.ignore_patterns("ASSET-NOTES.md"))
    write("index.html",homepage())
    write("advice/index.html",advice())
    for a in ARTICLES: write(f'advice/{a["slug"]}/index.html',article(a))
    write("privacy/index.html",privacy())
    write(".nojekyll","")
    # Crawlers must reach the page to see its preview noindex directive.
    write("robots.txt","User-agent: *\nAllow: /\n" if C["preview"] else "User-agent: *\nAllow: /\nSitemap: "+BASE+"sitemap.xml\n")
    urls=["","advice/","privacy/"]+["advice/"+a["slug"]+"/" for a in ARTICLES]
    write("sitemap.xml",'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f'<url><loc>{urljoin(BASE,u)}</loc></url>' for u in urls)+"</urlset>")
    # A project-site 404 uses the configured absolute root, independent of the missing path.
    write("404.html",f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><meta name="description" content="Return to Babar Shokut Electric Wear for washing machine, fridge and AC repair enquiries."><title>Page not found | Babar Shokut</title><link rel="stylesheet" href="{BASE}assets/css/styles.css"></head><body><main class="container section"><p class="eyebrow">PAGE NOT FOUND</p><h1>Let's get you<br>back on track.</h1><p>That page is no longer here, or the link may be incomplete.</p><a class="button button-primary" href="{BASE}">Go to the homepage {icon("arrow")}</a></main></body></html>''')
    print(f"Built {len(list(OUT.rglob('*.html')))} HTML pages in {OUT}")

if __name__=="__main__": main()
