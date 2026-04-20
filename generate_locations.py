#!/usr/bin/env python3
"""
CLEANOUT GUYS — SUBURB LOCATION PAGE GENERATOR
================================================
Generates 85+ individual HTML location pages for all Chicago suburbs.
Each page is fully SEO-optimized with:
  - Unique title tags & meta descriptions
  - LocalBusiness + BreadcrumbList schema
  - FAQPage schema with location-specific questions
  - Unique H1 and intro paragraph variations
  - Internal links to service pages
  - Location-specific content signals

Usage: python3 generate_locations.py
Output: /locations/*.html
"""

import os
import re

# ─────────────────────────────────────────────────────────────
# ALL 85+ CHICAGO SUBURBS — (name, slug, county, region, zip)
# ─────────────────────────────────────────────────────────────
SUBURBS = [
    # (display_name, slug, county, region, population_label, landmark_note)
    ("Chicago", "chicago", "Cook", "City of Chicago", "2.7 million residents", "the Chicago Loop, Wrigley Field, and Millennium Park"),
    ("Naperville", "naperville", "DuPage/Will", "Western Suburbs", "150,000 residents", "Naperville's Riverwalk and downtown shopping district"),
    ("Aurora", "aurora", "Kane/DuPage", "Western Suburbs", "180,000 residents", "the Fox River and Hollywood Casino Aurora"),
    ("Joliet", "joliet", "Will", "Southwest Suburbs", "150,000 residents", "Route 66, Chicagoland Speedway, and the Rialto Theatre"),
    ("Schaumburg", "schaumburg", "Cook", "Northwest Suburbs", "75,000 residents", "Woodfield Mall and the Schaumburg Boomers stadium"),
    ("Evanston", "evanston", "Cook", "North Shore", "75,000 residents", "Northwestern University and the Evanston lakefront"),
    ("Arlington Heights", "arlington-heights", "Cook", "Northwest Suburbs", "77,000 residents", "Arlington International Racecourse and Downtown Arlington Heights"),
    ("Bolingbrook", "bolingbrook", "Will/DuPage", "Southwest Suburbs", "73,000 residents", "Promenade Bolingbrook and IKEA"),
    ("Orland Park", "orland-park", "Cook", "Southwest Suburbs", "57,000 residents", "Orland Square Mall and the Centennial Park Aquatic Center"),
    ("Tinley Park", "tinley-park", "Cook/Will", "Southwest Suburbs", "56,000 residents", "the Hollywood Casino Amphitheatre and downtown Tinley Park"),
    ("Oak Lawn", "oak-lawn", "Cook", "Southwest Suburbs", "55,000 residents", "the Midlothian Reservoir and Southwest Hwy corridor"),
    ("Downers Grove", "downers-grove", "DuPage", "Western Suburbs", "50,000 residents", "downtown Downers Grove and the Morton Arboretum nearby"),
    ("Palatine", "palatine", "Cook", "Northwest Suburbs", "67,000 residents", "downtown Palatine and Deer Grove Forest Preserve"),
    ("Waukegan", "waukegan", "Lake", "North Suburbs", "85,000 residents", "Waukegan Harbor and the Great Lakes Naval Station"),
    ("Skokie", "skokie", "Cook", "North Shore", "64,000 residents", "the Skokie Swift Yellow Line and downtown Old Orchard"),
    ("Oak Park", "oak-park", "Cook", "Western Suburbs", "51,000 residents", "Frank Lloyd Wright's homes and Ernest Hemingway's birthplace"),
    ("Elmhurst", "elmhurst", "DuPage", "Western Suburbs", "47,000 residents", "downtown Elmhurst and York Road shopping"),
    ("Wheaton", "wheaton", "DuPage", "Western Suburbs", "52,000 residents", "Cantigny Park and Billy Graham's hometown"),
    ("Berwyn", "berwyn", "Cook", "Western Suburbs", "56,000 residents", "Cermak Road and the Czech-Slovak Museum"),
    ("Cicero", "cicero", "Cook", "Western Suburbs", "82,000 residents", "Cermak Road and proximity to Chicago's west side"),
    ("Highland Park", "highland-park", "Lake", "North Shore", "29,000 residents", "Ravinia Festival and Lake Michigan beach access"),
    ("Glenview", "glenview", "Cook", "Northwest Suburbs", "47,000 residents", "The Glen Town Center and Glenview Naval Air Station history"),
    ("Northbrook", "northbrook", "Cook", "North Shore", "33,000 residents", "Northbrook Court Mall and the North Branch of the Chicago River"),
    ("Hoffman Estates", "hoffman-estates", "Cook", "Northwest Suburbs", "51,000 residents", "Sears Centre Arena and Poplar Creek Forest Preserve"),
    ("Elk Grove Village", "elk-grove-village", "Cook/DuPage", "Northwest Suburbs", "33,000 residents", "O'Hare International Airport proximity and the Elk Grove Industrial Corridor"),
    ("Des Plaines", "des-plaines", "Cook", "Northwest Suburbs", "58,000 residents", "the original McDonald's Museum and Rivers Casino"),
    ("Park Ridge", "park-ridge", "Cook", "Northwest Suburbs", "38,000 residents", "Uptown Park Ridge and Hillary Rodham Clinton's hometown"),
    ("Niles", "niles", "Cook", "North Shore", "28,000 residents", "the Leaning Tower of Niles and Golf Mill Shopping Center"),
    ("Lombard", "lombard", "DuPage", "Western Suburbs", "43,000 residents", "Lilacia Park and the DuPage County Fairgrounds"),
    ("Glen Ellyn", "glen-ellyn", "DuPage", "Western Suburbs", "27,000 residents", "downtown Glen Ellyn and Lake Ellyn Park"),
    ("La Grange", "la-grange", "Cook", "Western Suburbs", "16,000 residents", "downtown La Grange and the Stone Avenue Train Station"),
    ("Hinsdale", "hinsdale", "DuPage/Cook", "Western Suburbs", "17,000 residents", "downtown Hinsdale shops and Fullersburg Woods"),
    ("Deerfield", "deerfield", "Lake", "North Shore", "18,000 residents", "Deerfield Road shops and Ryerson Conservation Area"),
    ("Libertyville", "libertyville", "Lake", "North Suburbs", "20,000 residents", "downtown Libertyville and Independence Grove"),
    ("Gurnee", "gurnee", "Lake", "North Suburbs", "30,000 residents", "Six Flags Great America and Gurnee Mills Mall"),
    ("Elgin", "elgin", "Kane/Cook", "Northwest Suburbs", "114,000 residents", "Grand Victoria Casino and the Elgin Symphony Orchestra"),
    ("St. Charles", "st-charles", "Kane", "Western Suburbs", "33,000 residents", "the Fox River Trolley and downtown St. Charles"),
    ("Batavia", "batavia", "Kane", "Western Suburbs", "26,000 residents", "Fermilab and the Fox River Trail"),
    ("Geneva", "geneva", "Kane", "Western Suburbs", "22,000 residents", "Fabyan Forest Preserve and charming downtown Geneva"),
    ("Plainfield", "plainfield", "Will", "Southwest Suburbs", "44,000 residents", "Historic Route 30 corridor and Plainfield's expanding subdivisions"),
    ("Romeoville", "romeoville", "Will", "Southwest Suburbs", "39,000 residents", "Lewis University and the Illinois Waterway"),
    ("Mokena", "mokena", "Will", "Southwest Suburbs", "19,000 residents", "the Old Plank Road Trail and Mokena's growing residential areas"),
    ("Frankfort", "frankfort", "Will", "Southwest Suburbs", "18,000 residents", "Old Frankfort Road and Lincoln-Way West High School"),
    ("New Lenox", "new-lenox", "Will", "Southwest Suburbs", "26,000 residents", "Silver Cross Field and the popular New Lenox Commons"),
    ("Calumet City", "calumet-city", "Cook", "South Suburbs", "36,000 residents", "River Oaks Center and the Indiana border"),
    ("Harvey", "harvey", "Cook", "South Suburbs", "25,000 residents", "South Halsted Street and the Thornton Township area"),
    ("Lansing", "lansing", "Cook", "South Suburbs", "28,000 residents", "Lansing Municipal Airport and Torrence Avenue commercial strip"),
    ("Chicago Heights", "chicago-heights", "Cook", "South Suburbs", "30,000 residents", "the historic Bloom Township and Sauk Trail area"),
    ("Matteson", "matteson", "Cook", "South Suburbs", "19,000 residents", "Lincoln Mall area and the growing South Suburban corridor"),
    ("Country Club Hills", "country-club-hills", "Cook", "South Suburbs", "16,000 residents", "Vollmer Road and the south Cook County area"),
    ("Blue Island", "blue-island", "Cook", "South Suburbs", "23,000 residents", "Western Avenue and the historic Blue Island downtown"),
    ("Oak Forest", "oak-forest", "Cook", "Southwest Suburbs", "28,000 residents", "159th Street and the Forest Preserve along Tinley Creek"),
    ("Burbank", "burbank", "Cook", "Southwest Suburbs", "28,000 residents", "Harlem Avenue and the Midway Airport area"),
    ("Bridgeview", "bridgeview", "Cook", "Southwest Suburbs", "17,000 residents", "SeatGeek Stadium and the Justice/Bridgeview corridor"),
    ("Morton Grove", "morton-grove", "Cook", "North Shore", "23,000 residents", "Dempster Street and Harrer Park"),
    ("Rolling Meadows", "rolling-meadows", "Cook", "Northwest Suburbs", "24,000 residents", "Kirchoff Road and Woodfield Road business corridors"),
    ("Buffalo Grove", "buffalo-grove", "Lake/Cook", "North Suburbs", "41,000 residents", "Buffalo Grove Town Center and Willow Stream Park"),
    ("Vernon Hills", "vernon-hills", "Lake", "North Suburbs", "25,000 residents", "Hawthorn Mall and the Cuneo Museum area"),
    ("Mundelein", "mundelein", "Lake", "North Suburbs", "32,000 residents", "Mundelein Seminary and Diamond Lake"),
    ("Lake Forest", "lake-forest", "Lake", "North Shore", "19,000 residents", "Market Square and the prestigious Lake Forest College"),
    ("Wilmette", "wilmette", "Cook", "North Shore", "27,000 residents", "the Bahá'í Temple and Gillson Park beach"),
    ("Winnetka", "winnetka", "Cook", "North Shore", "12,000 residents", "Winnetka Beach and the North Shore's most exclusive neighborhoods"),
    ("Lisle", "lisle", "DuPage", "Western Suburbs", "23,000 residents", "The Morton Arboretum and downtown Lisle"),
    ("Woodridge", "woodridge", "DuPage", "Western Suburbs", "33,000 residents", "Greene Valley Forest Preserve and Woodridge's growing subdivisions"),
    ("Westmont", "westmont", "DuPage", "Western Suburbs", "24,000 residents", "downtown Westmont and the DuPage County Fairgrounds nearby"),
    ("Darien", "darien", "DuPage", "Western Suburbs", "22,000 residents", "Darien's Sportsplex and Route 83 corridor"),
    ("Villa Park", "villa-park", "DuPage", "Western Suburbs", "22,000 residents", "Villa Park's Wildflower Way and North Avenue shopping"),
    ("Addison", "addison", "DuPage", "Western Suburbs", "36,000 residents", "Lake Street and Addison's growing commercial area"),
    ("Glendale Heights", "glendale-heights", "DuPage", "Western Suburbs", "34,000 residents", "Army Trail Road and the Salt Creek Greenway"),
    ("Bloomingdale", "bloomingdale", "DuPage", "Western Suburbs", "21,000 residents", "Stratford Square Mall and Gary Avenue"),
    ("Bartlett", "bartlett", "DuPage/Kane/Cook", "Northwest Suburbs", "41,000 residents", "Bartlett's popular family neighborhoods and Meadowdale Park"),
    ("Streamwood", "streamwood", "Cook", "Northwest Suburbs", "40,000 residents", "Army Trail Road and the Streamwood Oaks golf course area"),
    ("Carol Stream", "carol-stream", "DuPage", "Northwest Suburbs", "39,000 residents", "Central DuPage Hospital and Lies Road corridor"),
    ("South Elgin", "south-elgin", "Kane", "Northwest Suburbs", "24,000 residents", "the Fox River and South Elgin's Panton Mill development"),
    ("Algonquin", "algonquin", "McHenry/Kane", "Northwest Suburbs", "32,000 residents", "the Fox River and Algonquin's Route 31 shopping"),
    ("Crystal Lake", "crystal-lake", "McHenry", "Northwest Suburbs", "40,000 residents", "Crystal Lake itself and Sunnyside Avenue"),
    ("Round Lake Beach", "round-lake-beach", "Lake", "North Suburbs", "28,000 residents", "Round Lake and the Lake County forest preserves"),
    ("Zion", "zion", "Lake", "North Suburbs", "24,000 residents", "Illinois Beach State Park and Shiloh Boulevard"),
    ("Forest Park", "forest-park", "Cook", "Western Suburbs", "14,000 residents", "Forest Park's Blue Line CTA station and Harlem Avenue"),
    ("Hillside", "hillside", "Cook", "Western Suburbs", "8,000 residents", "the Hillside Shopping Center and Wolf Road corridor"),
    ("Roselle", "roselle", "DuPage/Cook", "Northwest Suburbs", "23,000 residents", "Lake Street and Medinah Country Club nearby"),
    ("Palos Hills", "palos-hills", "Cook", "Southwest Suburbs", "17,000 residents", "Palos Hills' forest preserves and Moraine Valley Community College"),
    ("Palos Heights", "palos-heights", "Cook", "Southwest Suburbs", "12,000 residents", "the Cal-Sag Channel and Palos Forest Preserve"),
    ("Chicago Ridge", "chicago-ridge", "Cook", "Southwest Suburbs", "14,000 residents", "Chicago Ridge Mall and Southwest Hwy"),
    ("Worth", "worth", "Cook", "Southwest Suburbs", "10,000 residents", "111th Street commercial area and Harlem Avenue"),
    ("Dolton", "dolton", "Cook", "South Suburbs", "23,000 residents", "the Cal-Sag area and Cottage Grove corridor"),
    ("Rosemont", "rosemont", "Cook", "Northwest Suburbs", "4,000 residents", "Rosemont Entertainment District and Allstate Arena"),
]

# ─────────────────────────────────────────────────────────────
# INTRO PARAGRAPH VARIATIONS (6 versions for diversity)
# ─────────────────────────────────────────────────────────────
INTRO_VARIANTS = [
    "Looking for reliable, affordable junk removal in {city}, IL? Garage Cleanout Guys is {city}'s go-to junk removal and cleanout company — locally owned, fully licensed and insured, and known for same-day service with zero hidden fees. Whether you're clearing a garage, handling an estate, or hauling away construction debris, our experienced crews are ready to help.",
    "Garage Cleanout Guys is proud to serve {city}, Illinois with professional junk removal and cleanout services that residents and businesses can count on. We offer free on-site quotes, upfront flat pricing, and same-day availability so you can get your space back fast — without the stress.",
    "When {city} residents need junk removed fast and at a fair price, they call Cleanout Guys. We've built our reputation across Chicagoland by showing up on time, quoting upfront, and leaving every space broom-clean. From single-item pickups to full house cleanouts, no job is too big or too small.",
    "If you're searching for junk removal near me in {city}, IL, you've found the right team. Garage Cleanout Guys handles everything from garage cleanouts and estate clearances to appliance removal and construction debris — serving {city} and all surrounding communities with the same commitment to quality and care.",
    "Garage Cleanout Guys brings Chicagoland's most trusted junk removal experience right to your door in {city}, IL. Our fully insured crews deliver same-day service, honest pricing, and eco-friendly disposal every time. No call centers, no subcontractors — just our own professional team.",
    "Tired of staring at a pile of junk you don't know what to do with? Garage Cleanout Guys makes junk removal in {city}, IL simple, fast, and affordable. Call us in the morning and we're often there the same day, ready to haul away everything from old furniture and appliances to full garage loads.",
]

# ─────────────────────────────────────────────────────────────
# FAQ SETS (rotated per suburb)
# ─────────────────────────────────────────────────────────────
def get_faqs(city, county, region):
    return [
        {
            "q": f"How much does junk removal cost in {city}, IL?",
            "a": f"Junk removal in {city} typically costs between $100–$600 depending on the volume of items and type of material. Garage Cleanout Guys provides completely free, no-obligation on-site quotes with upfront flat pricing — no hidden fees. Call (847) 461-3287 to schedule your free estimate in {city} today."
        },
        {
            "q": f"Do you offer same-day junk removal in {city}?",
            "a": f"Yes! Cleanout Guys offers same-day junk removal service throughout {city} and the surrounding {region}. Call us before noon at (847) 461-3287 and we'll do our best to dispatch a crew the same day, subject to availability."
        },
        {
            "q": f"Are you licensed and insured to work in {city}, Illinois?",
            "a": f"Absolutely. Garage Cleanout Guys is fully licensed and insured in the state of Illinois and operates legally in {city}, {county} County. We carry comprehensive general liability insurance and worker's compensation on every job."
        },
        {
            "q": f"What areas near {city} do you also serve?",
            "a": f"In addition to {city}, we serve all neighboring communities throughout the {region} and greater Chicagoland area. We cover 85+ suburbs — if you're in Chicagoland, we can help. Call (847) 461-3287 to confirm service at your address."
        },
        {
            "q": f"Do you donate or recycle junk removed from {city} homes?",
            "a": f"Yes — before anything goes to a landfill, our crews sort items for donation to {city}-area charities and recycling centers. We're committed to keeping as much as possible out of Illinois landfills and giving usable items a second life in the community."
        },
    ]

# ─────────────────────────────────────────────────────────────
# HTML TEMPLATE
# ─────────────────────────────────────────────────────────────
def generate_page(suburb_data, idx):
    name, slug, county, region, pop, landmark = suburb_data
    intro = INTRO_VARIANTS[idx % len(INTRO_VARIANTS)].format(city=name)
    faqs  = get_faqs(name, county, region)

    # Schema FAQ JSON
    faq_schema_items = "\n".join([
        f'''          {{
            "@type": "Question",
            "name": "{q["q"]}",
            "acceptedAnswer": {{"@type": "Answer", "text": "{q["a"].replace('"', "'")}"}}
          }}{"," if i < len(faqs)-1 else ""}'''
        for i, q in enumerate(faqs)
    ])

    # FAQ HTML
    faq_html = ""
    for q in faqs:
        faq_html += f"""
          <div class="faq-item">
            <div class="faq-question" role="button" tabindex="0" aria-expanded="false">
              <span>{q["q"]}</span>
              <span class="faq-toggle">+</span>
            </div>
            <div class="faq-answer">
              <div class="faq-answer-inner">{q["a"]}</div>
            </div>
          </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Junk Removal {name} IL | Same-Day Service | Cleanout Guys</title>
  <meta name="description" content="Garage Cleanout Guys provides fast, affordable junk removal &amp; cleanout services in {name}, IL. Same-day available, licensed &amp; insured, upfront pricing. Call (847) 461-3287 for a FREE quote!">
  <meta name="keywords" content="junk removal {name}, garage cleanout {name} IL, estate cleanout {name}, junk hauling {name} Illinois, same day junk removal {name}, appliance removal {name} IL, {name} IL junk removal company">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://cleanout-guys.com/locations/{slug}.html">
  <meta property="og:title" content="Junk Removal {name} IL | Cleanout Guys">
  <meta property="og:description" content="Same-day junk removal in {name}, IL. Licensed &amp; insured. Free quotes. Call (847) 461-3287.">
  <meta property="og:url" content="https://cleanout-guys.com/locations/{slug}.html">
  <meta property="og:type" content="website">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "LocalBusiness",
        "@id": "https://cleanout-guys.com/#business",
        "name": "Garage Cleanout Guys",
        "telephone": "+18474613287",
        "url": "https://cleanout-guys.com",
        "image": "https://cleanout-guys.com/images/cleanout-guys-logo.png",
        "address": {{
          "@type": "PostalAddress",
          "addressLocality": "Chicago",
          "addressRegion": "IL",
          "postalCode": "60601",
          "addressCountry": "US"
        }},
        "areaServed": [
          {{"@type": "City", "name": "{name}", "sameAs": "https://en.wikipedia.org/wiki/{name.replace(" ", "_")},_Illinois"}},
          {{"@type": "State", "name": "Illinois"}}
        ],
        "aggregateRating": {{
          "@type": "AggregateRating",
          "ratingValue": "4.9",
          "reviewCount": "312"
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "itemListElement": [
          {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cleanout-guys.com/"}},
          {{"@type": "ListItem", "position": 2, "name": "Service Areas", "item": "https://cleanout-guys.com/locations/index.html"}},
          {{"@type": "ListItem", "position": 3, "name": "Junk Removal {name}", "item": "https://cleanout-guys.com/locations/{slug}.html"}}
        ]
      }},
      {{
        "@type": "FAQPage",
        "mainEntity": [
{faq_schema_items}
        ]
      }}
    ]
  }}
  </script>
</head>
<body>

  <div class="top-bar">
    <div class="container">
      <div class="top-bar-badges">
        <span>✅ Licensed &amp; Insured</span>
        <span>⚡ Same-Day Available</span>
        <span>🌿 Eco-Friendly</span>
        <span>🏆 4.9 ⭐ on Google</span>
      </div>
      <div class="top-bar-right">
        <a href="tel:+18474613287">📞 (847) 461-3287</a>
        <a href="../contact.html" style="background:var(--orange-600);color:#fff;padding:.25rem .75rem;border-radius:99px;font-weight:700;font-size:.78rem;">Free Quote →</a>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="header-inner">
      <a href="../index.html" class="site-logo">
        <div class="logo-icon">🚛</div>
        <div class="logo-text">
          <div class="logo-name">Garage Cleanout Guys</div>
          <div class="logo-tagline">Chicago's Junk Removal Pros</div>
        </div>
      </a>
      <nav class="main-nav" id="main-nav">
        <button class="mobile-close" id="nav-close">✕</button>
        <a href="../index.html">Home</a>
        <a href="../services/index.html">Services</a>
        <a href="index.html" class="active">Service Areas</a>
        <a href="../about.html">About Us</a>
        <a href="../faq.html">FAQ</a>
        <a href="../contact.html">Contact</a>
      </nav>
      <div class="header-cta">
        <div class="header-phone">
          <span class="phone-label">Call for Same-Day</span>
          <a href="tel:+18474613287">(847) 461-3287</a>
        </div>
        <a href="../contact.html" class="btn btn-primary btn-sm">Free Quote</a>
      </div>
      <button class="menu-toggle" id="menu-toggle"><span></span><span></span><span></span></button>
    </div>
  </header>

  <nav class="breadcrumb" aria-label="Breadcrumb">
    <div class="container">
      <ol class="breadcrumb-list">
        <li><a href="../index.html">Home</a></li>
        <li><a href="index.html">Service Areas</a></li>
        <li><span>Junk Removal {name}</span></li>
      </ol>
    </div>
  </nav>

  <section class="page-hero">
    <div class="container">
      <h1>Junk Removal &amp; Cleanout Services in {name}, IL</h1>
      <p class="page-hero-sub">Serving {name} and all of {county} County. Same-day available, upfront pricing, fully licensed &amp; insured.</p>
      <div class="hero-trust">
        <div class="hero-trust-item"><span class="check">✓</span> Same-Day Available</div>
        <div class="hero-trust-item"><span class="check">✓</span> Free On-Site Quote</div>
        <div class="hero-trust-item"><span class="check">✓</span> Licensed &amp; Insured</div>
        <div class="hero-trust-item"><span class="check">✓</span> No Hidden Fees</div>
      </div>
      <div style="margin-top:1.75rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <a href="tel:+18474613287" class="btn btn-phone">📞 (847) 461-3287</a>
        <a href="../contact.html" class="btn btn-secondary">Get Free Quote →</a>
      </div>
    </div>
  </section>

  <main>
    <section class="section-pad">
      <div class="container">
        <div class="location-intro">
          <div class="location-main">
            <h2>Trusted Junk Removal in {name}, Illinois</h2>
            <p>{intro}</p>
            <p>We serve all neighborhoods and zip codes throughout {name} and {county} County, including areas near {landmark}. Whether you're a homeowner, landlord, real estate agent, or contractor — Cleanout Guys has the trucks, the team, and the experience to get the job done right.</p>

            <h3 style="margin-top:2rem;margin-bottom:1rem;">Our Services in {name}, IL</h3>
            <div class="services-grid" style="margin-bottom:2rem;">
              <a href="../services/junk-removal.html" class="service-card">
                <div class="service-icon">🗑️</div>
                <h3>Junk Removal</h3>
                <p>Full-service junk hauling for homes and businesses in {name}. We load, lift, and haul everything away.</p>
                <div class="card-link">Learn more →</div>
              </a>
              <a href="../services/garage-cleanout.html" class="service-card">
                <div class="service-icon">🏠</div>
                <h3>Garage Cleanout</h3>
                <p>Reclaim your {name} garage. We clear out everything and leave it broom-clean.</p>
                <div class="card-link">Learn more →</div>
              </a>
              <a href="../services/estate-cleanout.html" class="service-card">
                <div class="service-icon">🏡</div>
                <h3>Estate Cleanout</h3>
                <p>Compassionate estate cleanout services for {name} families. We handle everything with care.</p>
                <div class="card-link">Learn more →</div>
              </a>
              <a href="../services/hoarding-cleanout.html" class="service-card">
                <div class="service-icon">📦</div>
                <h3>Hoarding Cleanout</h3>
                <p>Discreet, professional hoarding cleanouts throughout {name} and {county} County.</p>
                <div class="card-link">Learn more →</div>
              </a>
              <a href="../services/construction-debris.html" class="service-card">
                <div class="service-icon">🔨</div>
                <h3>Construction Debris</h3>
                <p>Post-renovation cleanup for {name} contractors and homeowners. Fast, same-day available.</p>
                <div class="card-link">Learn more →</div>
              </a>
              <a href="../services/appliance-furniture-removal.html" class="service-card">
                <div class="service-icon">🛋️</div>
                <h3>Appliance &amp; Furniture</h3>
                <p>Old couch, fridge, washer? We pick up appliances and furniture across {name}.</p>
                <div class="card-link">Learn more →</div>
              </a>
            </div>

            <h3 style="margin-bottom:1rem;">Why {name} Residents Choose Cleanout Guys</h3>
            <div class="why-grid">
              <div class="why-item">
                <div class="why-icon">⚡</div>
                <h3>Same-Day Service</h3>
                <p>Call before noon and we're often in {name} the same day. No waiting, no hassle.</p>
              </div>
              <div class="why-item">
                <div class="why-icon">💲</div>
                <h3>Flat, Upfront Pricing</h3>
                <p>We give you a firm price before we start. What we quote in {name} is what you pay.</p>
              </div>
              <div class="why-item">
                <div class="why-icon">🛡️</div>
                <h3>Fully Insured</h3>
                <p>Licensed &amp; insured to operate in {name} and throughout Illinois. Your home is protected.</p>
              </div>
              <div class="why-item">
                <div class="why-icon">🌿</div>
                <h3>Eco-Friendly</h3>
                <p>We donate and recycle before disposing. Helping {name} stay clean and green.</p>
              </div>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="location-sidebar">
            <h3 style="color:var(--green-800);margin-bottom:.75rem;">📍 Serving {name}, IL</h3>
            <p style="font-size:.9rem;color:var(--dark-400);margin-bottom:.5rem;">{county} County | {region}</p>
            <p style="font-size:.9rem;color:var(--dark-400);">Population: ~{pop}</p>
            <div class="sidebar-divider"></div>
            <p style="font-weight:700;font-size:.88rem;color:var(--dark-700);margin-bottom:.5rem;">Call or Text for Same-Day Service:</p>
            <a href="tel:+18474613287" class="sidebar-phone">📞 (847) 461-3287</a>
            <a href="../contact.html" class="btn btn-primary" style="width:100%;justify-content:center;margin-top:.75rem;">Get Free Quote Online</a>
            <div class="sidebar-divider"></div>
            <p style="font-weight:700;font-size:.88rem;color:var(--dark-700);margin-bottom:.75rem;">Our Services in {name}:</p>
            <div class="sidebar-services">
              <a href="../services/junk-removal.html" class="sidebar-service-link">🗑️ Junk Removal</a>
              <a href="../services/garage-cleanout.html" class="sidebar-service-link">🏠 Garage Cleanout</a>
              <a href="../services/estate-cleanout.html" class="sidebar-service-link">🏡 Estate Cleanout</a>
              <a href="../services/hoarding-cleanout.html" class="sidebar-service-link">📦 Hoarding Cleanout</a>
              <a href="../services/construction-debris.html" class="sidebar-service-link">🔨 Construction Debris</a>
              <a href="../services/appliance-furniture-removal.html" class="sidebar-service-link">🛋️ Appliance Removal</a>
            </div>
            <div class="sidebar-divider"></div>
            <div style="text-align:center;">
              <div style="font-size:1.4rem;color:var(--gold);">★★★★★</div>
              <div style="font-weight:700;color:var(--green-800);">4.9/5 on Google</div>
              <div style="font-size:.8rem;color:var(--dark-400);">312 reviews</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="section-pad bg-light" id="faq">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Local Questions Answered</span>
          <h2>Junk Removal FAQ for {name}, IL</h2>
          <p>Common questions from {name} residents about our junk removal and cleanout services.</p>
        </div>
        <div class="faq-list">
{faq_html}
        </div>
      </div>
    </section>

    <!-- CTA Banner -->
    <section class="cta-banner">
      <div class="container">
        <h2>Ready for Junk Removal in {name}?</h2>
        <p>Call or request a quote online. Same-day service available throughout {name} and {county} County.</p>
        <div class="cta-btns">
          <a href="tel:+18474613287" class="btn btn-secondary btn-lg">📞 (847) 461-3287</a>
          <a href="../contact.html" class="btn btn-green btn-lg">Get Free Quote →</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr;gap:2rem;margin-bottom:2rem;">
        <div>
          <a href="../index.html" class="footer-logo">
            <div class="logo-icon">🚛</div>
            <div class="logo-name">Garage Cleanout Guys</div>
          </a>
          <p class="footer-about">Chicago's most trusted junk removal company. Serving {name} and 85+ suburbs. Licensed, insured, eco-friendly.</p>
          <div class="footer-nap">
            <div>📍 Serving {name}, {county} County, IL</div>
            <div>📞 <a href="tel:+18474613287">(847) 461-3287</a></div>
            <div>✉️ <a href="mailto:info@cleanout-guys.com">info@cleanout-guys.com</a></div>
          </div>
        </div>
        <div class="footer-col">
          <h4>Services</h4>
          <ul>
            <li><a href="../services/junk-removal.html">Junk Removal</a></li>
            <li><a href="../services/garage-cleanout.html">Garage Cleanout</a></li>
            <li><a href="../services/estate-cleanout.html">Estate Cleanout</a></li>
            <li><a href="../services/hoarding-cleanout.html">Hoarding Cleanout</a></li>
            <li><a href="../services/construction-debris.html">Construction Debris</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>More Areas</h4>
          <ul>
            <li><a href="chicago.html">Chicago</a></li>
            <li><a href="naperville.html">Naperville</a></li>
            <li><a href="aurora.html">Aurora</a></li>
            <li><a href="schaumburg.html">Schaumburg</a></li>
            <li><a href="index.html">All 85+ Locations →</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <div>© <span id="year"></span> Cleanout Guys · Serving {name}, IL &amp; Chicagoland · <a href="tel:+18474613287">(847) 461-3287</a></div>
      </div>
    </div>
  </footer>

  <div class="floating-cta">
    <a href="../contact.html" class="float-btn float-quote">📋 <span>Free Quote</span></a>
    <a href="tel:+18474613287" class="float-btn float-phone">📞 <span>Call Now</span></a>
  </div>
  <a href="#" id="back-to-top">↑</a>
  <script src="../js/main.js" defer></script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────
# GENERATE LOCATION INDEX PAGE
# ─────────────────────────────────────────────────────────────
def generate_index_page():
    location_cards = ""
    for i, suburb in enumerate(SUBURBS):
        name, slug, county, region, pop, _ = suburb
        location_cards += f'''
        <a href="{slug}.html" class="service-card" style="text-decoration:none;">
          <div class="service-icon">📍</div>
          <h3>{name}</h3>
          <p>{county} County · {region}</p>
          <div class="card-link">View page →</div>
        </a>'''

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Junk Removal Chicago Suburbs | All Service Areas | Cleanout Guys</title>
  <meta name="description" content="Garage Cleanout Guys provides junk removal and cleanout services across Chicago and 85+ suburbs. Same-day service, upfront pricing. Find your area and get a free quote!">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://cleanout-guys.com/locations/index.html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cleanout-guys.com/"}},
      {{"@type": "ListItem", "position": 2, "name": "All Service Areas", "item": "https://cleanout-guys.com/locations/index.html"}}
    ]
  }}
  </script>
</head>
<body>
  <div class="top-bar"><div class="container"><div class="top-bar-badges"><span>✅ Licensed &amp; Insured</span><span>⚡ Same-Day Available</span><span>🌿 Eco-Friendly</span></div><div class="top-bar-right"><a href="tel:+18474613287">📞 (847) 461-3287</a></div></div></div>
  <header class="site-header"><div class="header-inner"><a href="../index.html" class="site-logo"><div class="logo-icon">🚛</div><div class="logo-text"><div class="logo-name">Garage Cleanout Guys</div><div class="logo-tagline">Chicago's Junk Removal Pros</div></div></a><nav class="main-nav" id="main-nav"><button class="mobile-close" id="nav-close">✕</button><a href="../index.html">Home</a><a href="../services/index.html">Services</a><a href="index.html" class="active">Service Areas</a><a href="../about.html">About</a><a href="../faq.html">FAQ</a><a href="../contact.html">Contact</a></nav><div class="header-cta"><a href="tel:+18474613287" class="header-phone" style="text-align:right;text-decoration:none;"><span class="phone-label">Free Quote</span><span style="font-size:1.1rem;font-weight:800;color:var(--green-800);">(847) 461-3287</span></a><a href="../contact.html" class="btn btn-primary btn-sm">Get Quote</a></div><button class="menu-toggle" id="menu-toggle"><span></span><span></span><span></span></button></div></header>

  <nav class="breadcrumb"><div class="container"><ol class="breadcrumb-list"><li><a href="../index.html">Home</a></li><li><span>All Service Areas</span></li></ol></div></nav>

  <section class="page-hero">
    <div class="container">
      <h1>Junk Removal &amp; Cleanout Services — All Chicagoland Locations</h1>
      <p class="page-hero-sub">We serve Chicago and 85+ surrounding suburbs. Click your city below to see local pricing, availability, and contact info.</p>
      <div style="margin-top:1.5rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <a href="tel:+18474613287" class="btn btn-phone">📞 (847) 461-3287</a>
        <a href="../contact.html" class="btn btn-secondary">Get Free Quote</a>
      </div>
    </div>
  </section>

  <main>
    <section class="section-pad">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">85+ Locations</span>
          <h2>Find Your City Below</h2>
          <p>Don't see your suburb? Call us — we likely serve your area.</p>
        </div>
        <div class="services-grid">
          {location_cards}
        </div>
      </div>
    </section>
    <section class="cta-banner">
      <div class="container">
        <h2>Don't See Your City?</h2>
        <p>We likely serve your area! Give us a call or send a quick message and we'll confirm service at your address.</p>
        <div class="cta-btns">
          <a href="tel:+18474613287" class="btn btn-secondary btn-lg">📞 (847) 461-3287</a>
          <a href="../contact.html" class="btn btn-green btn-lg">Request a Quote →</a>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer"><div class="container"><div class="footer-bottom" style="border-top:none;padding-top:0;"><div>© <span id="year"></span> Cleanout Guys · Chicago &amp; Chicagoland · (847) 461-3287</div></div></div></footer>
  <div class="floating-cta"><a href="tel:+18474613287" class="float-btn float-phone">📞 <span>Call Now</span></a></div>
  <a href="#" id="back-to-top">↑</a>
  <script src="../js/main.js" defer></script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────
# MAIN — GENERATE ALL FILES
# ─────────────────────────────────────────────────────────────
def main():
    # Output directory
    output_dir = os.path.join(os.path.dirname(__file__), 'locations')
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n🚛 CLEANOUT GUYS — Location Page Generator")
    print(f"{'='*50}")
    print(f"📁 Output: {output_dir}")
    print(f"📍 Generating {len(SUBURBS)} location pages...\n")

    # Generate each suburb page
    generated = 0
    for idx, suburb in enumerate(SUBURBS):
        name, slug = suburb[0], suburb[1]
        html = generate_page(suburb, idx)
        filepath = os.path.join(output_dir, f'{slug}.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  ✅ {name:30s} → locations/{slug}.html")
        generated += 1

    # Generate index page
    index_html = generate_index_page()
    with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
    print(f"\n  ✅ {'Locations Index':30s} → locations/index.html")

    print(f"\n{'='*50}")
    print(f"✅ Done! Generated {generated} suburb pages + 1 index page")
    print(f"📊 Total location pages: {generated + 1}")
    print(f"\nNext steps:")
    print(f"  1. Run: python3 generate_sitemap.py")
    print(f"  2. Upload all files to your web host")
    print(f"  3. Submit sitemap to Google Search Console")
    print(f"  4. Verify all pages in Google Search Console\n")


if __name__ == '__main__':
    main()
