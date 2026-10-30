"""Thakur Pan — static site builder (v3: four switchable UI themes + motion system).

Run:  python3 build.py        -> writes index.html, about.html, menu.html, contact.html
Edit the CONFIG block for phone / links. Copy is unchanged from v2.

To lock ONE theme for production: set DEFAULT_THEME and LOCK_THEME = True
(removes the theme switcher and only loads that theme's fonts).
"""
import os, json

ROOT = os.path.dirname(os.path.abspath(__file__))

# ============ CONFIG ============
PHONE_DISPLAY = "+91 97245 54999"
PHONE_TEL = "+919724554999"
WA_LINK = "https://wa.me/919724554999?text=Hi%20Thakur%20Pan%21"
GOOGLE_REVIEW_URL = "https://www.google.com/maps/search/?api=1&query=Thakur+Pan+Earth+Complex+Akota+Vadodara"
DIR_URL = "https://www.google.com/maps/dir/?api=1&destination=Thakur+Pan+Earth+Complex+Akota+Vadodara"
MAP_Q = "22.281423,73.165133"
ADDR = "Shop 52–53, Ground Floor, Earth Complex, Near Akshar Chowk Bridge, Atladra / Old Padra Road, Akota, Vadodara – 390012"

DEFAULT_THEME = "night"      # night | pop | royal | mint
LOCK_THEME = False           # True = hide the theme switcher, ship one theme
# ================================

THEMES = [
    ("night", "Night Market", "#d9a441", "#0a1a11", "#7fcf86"),
    ("pop", "Paan Pop", "#ff4f81", "#ffd23f", "#1fb56b"),
    ("royal", "Royal Mughal", "#d4a64a", "#2a0a14", "#8c1d3a"),
    ("mint", "Fresh Mint", "#1f9d62", "#f4faf6", "#bfe6cf"),
]
THEME_COLOR = {"night": "#07130c", "pop": "#fff4dc", "royal": "#240913", "mint": "#f4faf6"}

FONTS = {
    "night": "family=Archivo:wdth,wght@62..125,400..900&family=Chakra+Petch:wght@600;700&family=Instrument+Serif:ital@0;1",
    "pop": "family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800&family=Caveat:wght@600;700",
    "royal": "family=Playfair+Display:ital,wght@0,500..800;1,500..700&family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600",
    "mint": "family=Fraunces:ital,opsz,wght@0,9..144,400..700;1,9..144,400..600",
}
FONT_BASE = "family=DM+Sans:wght@300;400;500;600"

LEAF = '<path d="M100 175 C32 128 30 58 100 28 C170 58 168 128 100 175 Z"/><path d="M100 175 V62 M100 108 L68 86 M100 132 L134 106" />'
LEAF_BRAND = '<svg viewBox="0 0 200 200" aria-hidden="true"><path d="M100 175 C32 128 30 58 100 28 C170 58 168 128 100 175 Z"/><path class="vein" d="M100 175 V70"/></svg>'
LEAF_PL = '<svg class="pl-leaf" viewBox="0 0 200 200" aria-hidden="true">%s</svg>' % LEAF

WA_SVG = '<svg viewBox="0 0 32 32"><path d="M16.04 3C9.4 3 4 8.4 4 15.03c0 2.12.55 4.19 1.6 6.01L4 29l8.14-1.56a12 12 0 0 0 3.9.65C22.68 28.09 28 22.69 28 16.06 28 9.4 22.68 3 16.04 3zm0 22.02c-1.2 0-2.38-.2-3.5-.6l-.5-.18-4.83.93.96-4.7-.2-.5a10 10 0 0 1-1.6-5.3C6.4 9.9 10.7 5.5 16.04 5.5c5.3 0 9.6 4.4 9.6 9.8 0 5.4-4.3 9.7-9.6 9.7zm5.5-7.3c-.3-.15-1.8-.9-2.1-1-.28-.1-.48-.15-.68.15s-.78 1-.96 1.2c-.18.2-.35.22-.65.07a8 8 0 0 1-2.4-1.5 9 9 0 0 1-1.65-2.1c-.17-.3 0-.46.13-.6l.45-.52c.15-.17.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.68-1.65-.93-2.25-.25-.6-.5-.5-.68-.5h-.58c-.2 0-.53.08-.8.38-.28.3-1.05 1.03-1.05 2.5s1.08 2.9 1.23 3.1c.15.2 2.1 3.2 5.1 4.5 2 .85 2.8.92 3.8.78.6-.1 1.8-.73 2.05-1.45.25-.7.25-1.3.18-1.45-.08-.13-.28-.2-.58-.35z"/></svg>'

def ico(inner):
    return '<svg class="ico" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % inner

ICO_LEAF = ico('<path d="M24 42C8 32 8 14 24 6c16 8 16 26 0 36z"/><path d="M24 42V16M24 26l-8-6M24 32l8-6"/>')
ICO_SODA = ico('<path d="M14 16h20l-3 26H17z"/><path d="M12 16h24"/><path d="M26 16l5-10h7"/><circle cx="22" cy="28" r="1.8"/><circle cx="28" cy="35" r="1.3"/>')
ICO_WAFFLE = ico('<rect x="8" y="8" width="32" height="32" rx="9"/><path d="M8 19h32M8 29h32M19 8v32M29 8v32"/>')
ICO_MOON = ico('<path d="M39 29A16 16 0 1 1 19 9a12 12 0 0 0 20 20z"/><path d="M33 8v6M30 11h6"/>')
ICO_PHONE = ico('<path d="M13 6h7l3 9-4 3a22 22 0 0 0 11 11l3-4 9 3v7a4 4 0 0 1-4 4C22 39 9 26 9 10a4 4 0 0 1 4-4z"/>')
ICO_PIN = ico('<path d="M24 43S10 30 10 20a14 14 0 0 1 28 0c0 10-14 23-14 23z"/><circle cx="24" cy="20" r="5"/>')
ICO_CHAT = ico('<path d="M8 10h32v22H20l-9 8v-8H8z"/><path d="M16 19h16M16 25h10"/>')

NAV = [("index.html", "Home"), ("about.html", "About"), ("menu.html", "Menu"), ("contact.html", "Contact")]

# runs in <head> before paint: theme, js flag, per-theme font loading, page-arrival curtain
HEAD_JS = """(function(){
var d=document.documentElement,FONTS=__FONTS__,BASE='__BASE__',COLORS=__COLORS__,LOCK=__LOCK__,DEF='__DEF__';
d.classList.add('js');
var t=DEF;
if(!LOCK){try{var q=(location.search.match(/[?&]theme=(\\w+)/)||[])[1];if(q&&FONTS[q]){t=q;localStorage.setItem('tp_theme',q)}else{var s=localStorage.getItem('tp_theme');if(s&&FONTS[s])t=s}}catch(e){}}
d.setAttribute('data-theme',t);
var loaded={};
window.tpFonts=function(n){if(loaded[n])return;loaded[n]=1;var l=document.createElement('link');l.rel='stylesheet';l.href='https://fonts.googleapis.com/css2?'+FONTS[n]+'&'+BASE+'&display=swap';document.head.appendChild(l)};
window.tpFonts(t);
window.tpColors=COLORS;
try{if(sessionStorage.getItem('tp_seen'))d.classList.add('no-loader');if(sessionStorage.getItem('tp_nav')){d.classList.add('arrive','no-loader');sessionStorage.removeItem('tp_nav')}}catch(e){}
})();"""


def head_js():
    return (HEAD_JS.replace("__FONTS__", json.dumps(FONTS)).replace("__BASE__", FONT_BASE)
            .replace("__COLORS__", json.dumps(THEME_COLOR)).replace("__LOCK__", "true" if LOCK_THEME else "false")
            .replace("__DEF__", DEFAULT_THEME))


def img(name, alt, cls="", pos=""):
    st = ' style="object-position:%s"' % pos if pos else ""
    return '<img src="img/%s.jpg" alt="%s" class="%s" loading="lazy" decoding="async"%s>' % (name, alt, cls, st)


def themer():
    if LOCK_THEME:
        return ""
    opts = "".join(
        '<button type="button" class="th-opt" data-theme-set="%s" role="radio" aria-checked="false"><span class="th-sw" style="--a:%s;--b:%s;--c:%s"></span><span>%s</span></button>' % (k, a, b, c, n)
        for k, n, a, b, c in THEMES)
    return f"""<div class="themer">
  <div class="th-tray" role="radiogroup" aria-label="Choose a design theme"><p class="th-h">Design theme</p>{opts}</div>
  <button type="button" class="th-btn" aria-expanded="false" aria-label="Change design theme"><span class="th-dot"></span><span class="th-lbl">Theme</span></button>
</div>"""


def page(fn, title, desc, body, body_cls=""):
    menu = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' class="on" aria-current="page"' if h == fn else "", t) for h, t in NAV)
    mob = "".join('<a href="%s" style="--i:%d">%s</a>' % (h, i, t) for i, (h, t) in enumerate(NAV))
    flinks = "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV)
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "FoodEstablishment", "name": "Thakur Pan",
        "telephone": PHONE_TEL, "servesCuisine": ["Paan", "Beverages", "Waffles", "Street Food"],
        "address": {"@type": "PostalAddress", "streetAddress": "Shop 52-53, Ground Floor, Earth Complex, Near Akshar Chowk Bridge, Akota",
                    "addressLocality": "Vadodara", "addressRegion": "Gujarat", "postalCode": "390012", "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": 22.281423, "longitude": 73.165133},
        "openingHours": "Mo-Su 09:30-23:30"})
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="{DEFAULT_THEME}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="{THEME_COLOR[DEFAULT_THEME]}">
<script>{head_js()}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="style.css">
<noscript><style>.reveal,.split .w>span,.wipe{{opacity:1!important;translate:none!important;transform:none!important;clip-path:none!important}}.preloader,.curtain{{display:none!important}}</style></noscript>
<script type="application/ld+json">{ld}</script>
</head>
<body class="{body_cls}">
<div class="progress" aria-hidden="true"><i></i></div>
<div class="preloader" aria-hidden="true"><div class="pl-inner">{LEAF_PL}<div class="pl-word"><span>ThaKur Pan</span></div><div class="pl-bar"><i></i></div></div></div>
<div class="curtain" aria-hidden="true"><span>ThaKur Pan</span></div>
<div class="cur"></div><div class="cur-ring"></div>
<div class="toast" role="status"></div>

<header class="nav">
  <div class="wrap">
    <div class="nav-in">
      <a href="index.html" class="brand" aria-label="Thakur Pan home">{LEAF_BRAND}<div>ThaKur Pan<small>AKOTA · VADODARA</small></div></a>
      <ul class="menu">{menu}</ul>
      <div class="nav-r">
        {themer()}
        <a class="btn solid sm" href="contact.html#review">Review Us <span class="st">★</span></a>
        <button class="burger" aria-label="Open menu" aria-expanded="false"><i></i><i></i><i></i></button>
      </div>
    </div>
  </div>
</header>
<nav class="mob" aria-label="Mobile">{mob}<small>{PHONE_DISPLAY} · 9:30 AM – 11:30 PM</small></nav>

<main>
{body}
</main>

<footer>
  <div class="wrap">
    <div class="foot-big" aria-hidden="true">ThaKur Pan</div>
    <div class="fgrid">
      <div><div class="fbrand">ThaKur Pan</div><p style="margin-top:1.1rem;max-width:36ch;opacity:.75">Paan, soda, waffles and late-night sips at Akshar Chowk, Akota — Vadodara.</p></div>
      <div><h4>Explore</h4><ul>{flinks}</ul></div>
      <div><h4>Hours</h4><ul><li>Monday – Sunday</li><li>9:30 AM – 11:30 PM</li><li>Takeaway friendly</li><li>Digital payments accepted</li></ul></div>
      <div><h4>Visit</h4><ul><li>Earth Complex, Akshar Chowk, Akota, Vadodara 390012</li><li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li><li><a href="{DIR_URL}" target="_blank" rel="noopener">Get directions →</a></li><li><a href="{GOOGLE_REVIEW_URL}" target="_blank" rel="noopener">Review us on Google →</a></li></ul></div>
    </div>
    <div class="copy"><span>© <span class="yr">2026</span> THAKUR PAN, VADODARA</span><span>PAAN · SODA · WAFFLES · CHAI</span></div>
  </div>
</footer>

<a class="wa" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat with the owner on WhatsApp">{WA_SVG}<span>CHAT WITH US</span></a>
<script src="main.js"></script>
</body>
</html>
"""


def sec_head(eyebrow, h2, lead="", center=False):
    c = " center" if center else ""
    ld = '<p class="lead reveal" style="--d:.2s">%s</p>' % lead if lead else ""
    return f'<div class="sh{c}"><span class="eyebrow reveal">{eyebrow}</span><h2 class="split">{h2}</h2>{ld}</div>'


def feedback(idn="review"):
    return f"""<div class="fb reveal" id="{idn}" data-google="{GOOGLE_REVIEW_URL}">
  <h3>How was your visit?</h3>
  <p class="sub">Rate us, write a line or two, and we will take you straight to Google to post it. Your words are copied for you.</p>
  <div class="rate" aria-label="Rating">{"".join('<button type="button" aria-label="%d star">★</button>' % i for i in range(1, 6))}</div>
  <div class="rate-label"></div>
  <form>
    <textarea placeholder="Tell us what you loved (optional)" aria-label="Your feedback"></textarea>
    <button class="btn solid" type="submit">Continue to Google Reviews</button>
  </form>
  <p class="note">Honest feedback of any kind is welcome. It helps us, and other people choosing where to go.</p>
</div>"""


def visit_block():
    rows = "".join("<span>%s</span><span>9:30 AM – 11:30 PM</span>" % d for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    return f"""<div class="visit">
  <div class="visit-l">
    <div class="vi reveal"><small>Address</small><p>{ADDR}</p></div>
    <div class="vi reveal" style="--d:.1s"><small>Call</small><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div>
    <div class="vi reveal" style="--d:.2s"><small>Hours</small><div class="hours">{rows}</div></div>
    <div class="btns reveal" style="--d:.3s"><a class="btn solid" href="{DIR_URL}" target="_blank" rel="noopener">Get Directions</a><a class="btn" href="tel:{PHONE_TEL}">Call Us</a></div>
  </div>
  <div class="map wipe"><iframe title="Thakur Pan on Google Maps" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={MAP_Q}&amp;z=17&amp;output=embed"></iframe></div>
</div>"""


# ============================================================ HOME
SIG1 = [("paan-plate", "Meetha Paan"), ("waffle-berry", "Strawberry Waffle"), ("soda-blue", "Blue Mint Soda"), ("shake-duo", "Chocolate Shake"),
        ("paan-tissue", "Fresh Paan"), ("ice-choco", "Chocolate Scoops"), ("chai", "Masala Chai"), ("waffle-crunch", "Crunch Waffle")]
SIG2 = [("soda-duo", "Mojito Duo"), ("paan-sweet", "Special Sweet Paan"), ("ice-cups", "Ice Cream Cups"), ("waffle-choco", "Chocolate Waffle"),
        ("paan-hand", "Paan To Go"), ("soda-night", "Night Soda"), ("paan-bowl", "Cherry Paan"), ("soda-hands", "Iced Sips")]


def pm_row(items, cls=""):
    cards = "".join('<div class="pm-card">%s<span>%s</span></div>' % (img(n, c), c) for n, c in items)
    return '<div class="pm-row %s"><div class="pm-set">%s</div><div class="pm-set" aria-hidden="true">%s</div></div>' % (cls, cards, cards)


GAL = ["waffle-berry", "paan-tissue", "soda-duo", "ice-choco", "paan-sweet", "shake-duo", "waffle-crunch", "soda-night", "paan-hand", "chai", "ice-cups", "paan-bowl"]

TICK = ["50+ Refreshing Sodas", "Natural Juices", "Milkshakes", "Thickshakes", "30+ Paan Varieties", "Waffles", "Sandwiches", "Ice Cream"]
tick_set = "".join("<span>%s</span>" % t for t in TICK)

home = f"""
<section class="hero">
  <img class="hero-bg" src="img/storefront.jpg" alt="Thakur Pan storefront lit up at night in Akota" data-speed="0.08">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="eyebrow reveal">Akota · Vadodara · Since the late 1990s</span>
      <h1 class="split">Thakur<span class="l2">Pan</span></h1>
      <p class="tagline reveal" style="--d:.5s">Where every night ends with something sweet.</p>
      <div class="cta reveal" style="--d:.65s"><a class="btn solid" href="menu.html">Explore the Menu</a><a class="btn" href="{DIR_URL}" target="_blank" rel="noopener">Find Us</a></div>
      <div class="chips reveal" style="--d:.8s"><span class="chip open" data-open><i></i><b>Open daily</b> 9:30 AM – 11:30 PM</span><span class="chip">★ 4.2 on Justdial</span></div>
    </div>
    <div class="hero-art" aria-hidden="true">
      <div class="ha ha1" data-speed="-0.04"><div class="ha-in" style="--k:.5"><div class="arch">{img("paan-tissue", "")}</div></div></div>
      <div class="ha ha2" data-speed="0.05"><div class="ha-in" style="--k:-.8"><div class="circ">{img("soda-blue", "")}</div></div></div>
      <div class="ha ha3" data-speed="-0.02"><div class="ha-in" style="--k:.9"><div class="sq">{img("waffle-berry", "")}</div></div></div>
      <div class="stamp hero-stamp"><svg viewBox="0 0 120 120"><defs><path id="cp" d="M60,60 m-47,0 a47,47 0 1,1 94,0 a47,47 0 1,1 -94,0"/></defs><text><textPath href="#cp" textLength="292" lengthAdjust="spacing">30+ PAAN · 50+ SODAS · WAFFLES · CHAI · </textPath></text></svg><b>✦</b></div>
    </div>
  </div>
  <div class="wrap"><div class="hero-info"><span><b>Open daily</b> 9:30 AM – 11:30 PM</span><span>Akshar Chowk, Akota</span><span>Takeaway friendly</span><span class="cue">Scroll <i></i></span></div></div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track"><div class="tset">{tick_set}</div><div class="tset">{tick_set}</div></div></div>

<section class="alt" id="story">
  <div class="wrap grid2">
    <div class="stack">
      <div class="arch a1 wipe">{img("origin", "Thakur Pan's original shop from the 1990s")}</div>
      <div class="arch a2 wipe" style="--d:.2s">{img("paan-plate", "Meetha paan with a cherry")}</div>
      <div class="stamp story-stamp">since<b>'90s</b>Akota</div>
    </div>
    <div>
      <span class="eyebrow reveal">Our Story</span>
      <h2 class="split">A simple dream, <em class="s">still served fresh.</em></h2>
      <p class="lead reveal" style="--d:.2s">It all started with a simple dream in the late 1990s: to share the joy and authentic taste of paan with heartfelt service. Today Thakur Pan is a late-night corner at Akshar Chowk, where paan, soda, waffles and chai bring Akota together.</p>
      <div class="stats reveal" style="--d:.25s">
        <div class="stat"><b data-count="4.2" data-suffix="★">0</b><span>Justdial rating</span></div>
        <div class="stat"><b data-count="151">0</b><span>Customer ratings</span></div>
        <div class="stat"><b data-count="7">0</b><span>Days a week</span></div>
        <div class="stat"><b>11:30</b><span>PM, we close</span></div>
      </div>
      <p class="reveal" style="margin-top:2.2rem"><a class="btn solid" href="about.html">Read Our Story</a></p>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    {sec_head("What We Do", 'More than a <em class="s">paan shop</em>')}
    <div class="feat">
      <div class="fcard reveal">{ICO_LEAF}<span class="n">01</span><h3>30+ Paan Varieties</h3><p>Classic meetha paan and flavoured pan, folded fresh to order.</p></div>
      <div class="fcard reveal" style="--d:.1s">{ICO_SODA}<span class="n">02</span><h3>50+ Refreshing Sodas</h3><p>Pan mawa soda, minty mojitos and more, poured over plenty of ice.</p></div>
      <div class="fcard reveal" style="--d:.2s">{ICO_WAFFLE}<span class="n">03</span><h3>Waffles, Shakes &amp; More</h3><p>Waffles, sandwiches, milkshakes, thickshakes, natural juices and ice cream.</p></div>
      <div class="fcard reveal" style="--d:.3s">{ICO_MOON}<span class="n">04</span><h3>Late-Night Stop</h3><p>Open until 11:30 PM. Grab it to go or stay and soak up the lights.</p></div>
    </div>
  </div>
</section>

<section class="alt" id="menu">
  <div class="wrap">
    {sec_head("Menu Highlights", 'Right place to <em class="s">satisfy cravings</em>', "50+ refreshing sodas, natural juices, milkshakes, thickshakes, paan and flavoured pan in 30+ varieties, waffles, sandwiches, ice creams and many more.")}
    <div class="hb">
      <a class="b1 reveal" href="menu.html#paan">{img("paan-tissue", "Fresh green paan")}<div class="cap"><small>30+ varieties</small><h3>Paan &amp; Flavoured Pan</h3></div><span class="go">→</span></a>
      <a class="reveal" style="--d:.1s" href="menu.html#sodas">{img("soda-duo", "Blue and berry mojitos")}<div class="cap"><small>50+ sodas</small><h3>Refreshing Sodas</h3></div><span class="go">→</span></a>
      <a class="reveal" style="--d:.2s" href="menu.html#waffles">{img("waffle-berry", "Strawberry chocolate waffle")}<div class="cap"><small>16 varieties</small><h3>Waffles</h3></div><span class="go">→</span></a>
      <a class="reveal" style="--d:.3s" href="menu.html#juices">{img("shake-duo", "Chocolate thickshakes")}<div class="cap"><small>Fresh &amp; thick</small><h3>Juices &amp; Shakes</h3></div><span class="go">→</span></a>
      <a class="reveal" style="--d:.4s" href="menu.html#ice">{img("ice-choco", "Chocolate ice cream scoops")}<div class="cap"><small>Scoops &amp; cups</small><h3>Ice Cream</h3></div><span class="go">→</span></a>
    </div>
    <p class="reveal" style="text-align:center;margin-top:3rem"><a class="btn solid" href="menu.html">View Full Menu</a></p>
  </div>
</section>

<section class="pm">
  <div class="wrap">{sec_head("Signature Plates", 'Made for <em class="s">sharing</em>')}</div>
  <div class="pm-wrap">{pm_row(SIG1)}{pm_row(SIG2, "rev")}</div>
</section>

<section class="alt" id="reviews">
  <div class="wrap">
    {sec_head("Reviews", 'Loved in <em class="s">Akota</em>')}
    <div class="rv-grid">
      <div class="tiles">
        <div class="tile reveal"><div><b>4.2</b><small>Justdial · 151 ratings</small></div><span class="stars-static">★★★★☆</span></div>
        <div class="tile reveal" style="--d:.1s"><div><b>30+</b><small>Paan &amp; flavoured pan varieties</small></div><span class="stars-static">✦✦✦</span></div>
        <div class="quote reveal" style="--d:.2s"><p>“Thakurpan provides best quality of products.”</p><cite>A customer on Justdial</cite></div>
        <p class="reveal" style="--d:.3s"><a class="btn" href="{GOOGLE_REVIEW_URL}" target="_blank" rel="noopener">Read reviews on Google</a></p>
      </div>
      {feedback("review")}
    </div>
  </div>
</section>

<section id="visit">
  <div class="wrap">
    {sec_head("Find Us", 'Come <em class="s">visit us</em>')}
    {visit_block()}
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <span class="eyebrow reveal" style="justify-content:center">Open till 11:30 PM</span>
    <h2 class="split">Your paan<br>is <em class="s">waiting</em></h2>
    <div class="reveal" style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap"><a class="btn solid" href="{DIR_URL}" target="_blank" rel="noopener">Get Directions</a><a class="btn" href="menu.html">See the Menu</a></div>
  </div>
</section>
"""

# ============================================================ ABOUT
about = f"""
<section class="phero">
  <img class="bg" src="img/storefront.jpg" alt="" data-speed="0.1">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="wrap"><span class="eyebrow reveal">About Us</span><h1 class="split">Our <em>Story</em></h1><p class="reveal" style="--d:.4s">A neighbourhood paan corner that grew into one of Akota's favourite late-night stops.</p></div>
</section>

<section class="alt">
  <div class="wrap origin">
    <div class="card-img wipe">{img("origin", "The original Thakur Pan shop")}</div>
    <div>
      <span class="eyebrow reveal">The Origin</span>
      <h2 class="split">It started with <em class="s">one small dream</em></h2>
      <p class="lead reveal" style="--d:.2s">It all started with a simple dream in the late 1990s: to share the joy and authentic taste of paan with a heartfelt service.</p>
      <p class="reveal" style="--d:.3s">From that small counter, Thakur Pan grew into the shop you see today at Earth Complex, beside the Akshar Chowk bridge. The menu has grown too, from paan and pan mawa soda to mojitos, shakes, waffles, chai and ice cream.</p>
      <div class="tl reveal" style="--d:.4s">
        <div><b>Late 1990s</b><p>The first counter opens with a simple dream.</p></div>
        <div><b>Today</b><p>A lit-up corner at Akshar Chowk, open daily until 11:30 PM.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="quote-band">
  <div class="wrap"><p class="big split">Where every night ends with <em class="s">something sweet.</em></p></div>
</section>

<section>
  <div class="wrap">
    {sec_head("What We Stand For", 'Simple things, <em class="s">done well</em>')}
    <div class="feat">
      <div class="fcard reveal">{ICO_LEAF}<span class="n">01</span><h3>Fresh paan</h3><p>Folded to order, the way you like it.</p></div>
      <div class="fcard reveal" style="--d:.1s">{ICO_MOON}<span class="n">02</span><h3>Open late</h3><p>Every day from 9:30 AM to 11:30 PM.</p></div>
      <div class="fcard reveal" style="--d:.2s">{ICO_SODA}<span class="n">03</span><h3>Easy takeaway</h3><p>Grab it and go, or pull up a spot nearby.</p></div>
      <div class="fcard reveal" style="--d:.3s">{ICO_WAFFLE}<span class="n">04</span><h3>Digital payments</h3><p>UPI and other digital payments accepted.</p></div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap">
    {sec_head("The Spread", 'Always <em class="s">something new</em> to try')}
    <div class="masonry">{"".join('<figure class="reveal" style="--d:%.2fs">%s</figure>' % ((i % 4) * 0.08, img(n, "Thakur Pan photo")) for i, n in enumerate(GAL[:8]))}</div>
    <p class="reveal" style="text-align:center;margin-top:3rem"><a class="btn solid" href="menu.html">See the Menu</a></p>
  </div>
</section>
"""

# ============================================================ MENU
WAFFLES = [("Classic Malted", 100), ("Banana And Caramel", 100), ("Coffee And Dark", 100), ("Kitkat Chocolate", 120), ("Dairy Milk Chocolate", 120),
           ("White Chocolate", 120), ("Dark Chocolate", 120), ("Milk Chocolate", 120), ("Chips Chocolate", 140), ("Oreo Cream", 140),
           ("Hazelnut Nutella", 140), ("Triple Chocolate", 140), ("Black And White", 140), ("Mix Chocolate", 160), ("Red Velvet", 160), ("Hazelnut And Brownie", 160)]
PUFF = [("Butter Grill Puff", 20), ("Punjabi Grill Puff", 30), ("Mayonnaise Grill Puff", 40), ("Cheese Grill Puff", 40), ("Garlic Grill Puff", 40),
        ("Sev Chatni Grill Puff", 40), ("Cheese Jam Grill Puff", 40), ("Onion Cheese Grill Puff", 40), ("Grill Butter Garlic Puff", 40),
        ("Cheese Paneer Grill Puff", 50), ("Veg. Cheese Grill Puff", 50), ("Schezwan Cheese Grill Puff", 50), ("Tandoori Cheese Grill Puff", 50),
        ("Chocolate Cheese Grill Puff", 50), ("Ratlami Shing Cheese Puff", 50), ("Cheese Butter Grill Puff", 50)]
SANDWICH = [("Cheese Masala Wafer", 80), ("Cheese Chatni Grill Sandwich", 80), ("Bread Butter Grill Sandwich", 80), ("Cheese Jam Grill Sandwich", 80),
            ("Veg. Cheese Grill Sandwich", 80), ("Tandoori Cheese Grill Sandwich", 100), ("Paneer Cheese Grill Sandwich", 100), ("Bombay Grill Sandwich", 100),
            ("Mayonnaise Cheese Grill Sandwich", 100), ("Chilly Cheese Grill Sandwich", 100), ("Chocolate Cheese Sandwich", 100)]
EXTRAS = [("Extra Wafer", 20), ("Extra Cheese", 20)]


def priced(rows, tag=""):
    return [(n, "", pr, tag) for n, pr in rows]


PANELS = [
    dict(id="paan", name="Paan", title="Paan & Flavoured Pan", badge=("30+", "varieties"),
         blurb="From classic meetha paan to flavoured pan with cherry, coconut and sweet fillings, all folded fresh to order.",
         imgs=["paan-tissue", "paan-plate", "paan-sweet", "paan-hand"],
         items=[("Meetha Paan", "Betel leaf, sweet fillings, coconut and cherry", None, "Signature"),
                ("Cherry Paan", "Folded paan finished with a glazed cherry", None, ""),
                ("Special Sweet Paan", "Rich sweet filling with colourful sprinkles", None, "Must try"),
                ("Flavoured Pan", "30+ varieties. Ask at the counter for today's range", None, "")]),
    dict(id="sodas", name="Sodas", title="50+ Refreshing Sodas", badge=("50+", "sodas"),
         blurb="Fizzy, cold and made over plenty of ice. Pan mawa soda, minty mojitos and a whole wall of flavours to cool you down.",
         imgs=["soda-duo", "soda-blue", "soda-night", "soda-hands"],
         items=[("Pan Mawa Soda", "Paan flavour in a chilled fizzy soda", None, "Signature"),
                ("Blue Mint Mojito", "Blue soda with mint, lime and ice", None, ""),
                ("Berry Mint Mojito", "Berry mojito with mint and a lime wedge", None, ""),
                ("More Sodas", "50+ flavours. Ask for today's range", None, "")]),
    dict(id="juices", name="Juices & Shakes", title="Juices, Milkshakes & Thickshakes", badge=("Fresh", "& thick"),
         blurb="Natural juices pressed fresh, creamy milkshakes and thick chocolate-swirled thickshakes for a warm Vadodara evening.",
         imgs=["shake-duo", "soda-hands"],
         items=[("Natural Juices", "Fresh, seasonal and served chilled", None, "Fresh"),
                ("Milkshakes", "Creamy, cold and made to order", None, ""),
                ("Thickshakes", "Thick, with chocolate drizzle", None, "Signature"),
                ("Cold Coffee", "Iced coffee, creamy and strong", None, ""),
                ("Lassi", "Chilled, thick and refreshing", None, "")]),
    dict(id="waffles", name="Waffles", title="Thakur Special Waffles", badge=("16", "varieties"),
         blurb="Warm waffles loaded with chocolate, fruit, cream and crunch. Prices in rupees.",
         imgs=["waffle-berry", "waffle-choco", "waffle-crunch"], items=priced(WAFFLES)),
    dict(id="puff", name="Grill Puff", title="Thakur Special Grill Puff", badge=("16", "varieties"),
         blurb="Crisp, hot grilled puffs from a simple butter puff to loaded cheese specials. Prices in rupees.",
         imgs=[], items=priced(PUFF)),
    dict(id="sandwich", name="Sandwiches", title="Thakur Special Sandwich", badge=("11", "varieties"),
         blurb="Grilled sandwiches stuffed with cheese, chutney, paneer and more. Prices in rupees.",
         imgs=[], items=priced(SANDWICH), extras=priced(EXTRAS, "Add-on")),
    dict(id="ice", name="Ice Cream", title="Ice Cream", badge=("Scoops", "& cups"),
         blurb="Generous scoops in rich chocolate and more, served in cups to enjoy right away.",
         imgs=["ice-choco", "ice-cups"],
         items=[("Chocolate Scoops", "Rich dark chocolate ice cream", None, "Signature"),
                ("Assorted Cups", "A mix of flavours in cups", None, "")]),
    dict(id="chai", name="Tea & Coffee", title="Tea & Coffee", badge=("Hot", "& fresh"),
         blurb="Hot, milky and made fresh. The simplest way to end a long day.",
         imgs=["chai"],
         items=[("Masala Chai", "Spiced tea with milk", None, "Signature"),
                ("Tea", "Classic cutting-style tea", None, ""),
                ("Coffee", "Hot coffee, freshly made", None, "")]),
]


def li(n, d, pr, tag, i):
    st = ' style="--i:%d"' % min(i, 18)
    if pr is not None:
        return '<li class="ri"%s><b>%s</b><i></i><span class="pr">&#8377;%d</span></li>' % (st, n, pr)
    return '<li class="np ri"%s><div><b>%s</b><p>%s</p></div>%s</li>' % (st, n, d, ("<em>%s</em>" % tag) if tag else "")


def panel(c, first):
    rows = c["items"]
    lis = "".join(li(*r, i) for i, r in enumerate(rows))
    extras = ""
    if c.get("extras"):
        extras = '<h4 class="sub">Add-ons</h4><ul class="plist">%s</ul>' % "".join(li(*r, i) for i, r in enumerate(c["extras"]))
    n = len(c["imgs"])
    figs = "".join('<figure class="ri" style="--i:%d">%s</figure>' % (k, img(i, c["name"] + " photo")) for k, i in enumerate(c["imgs"]))
    left = '<div class="mb n%d">%s</div>' % (n, figs) if n else ""
    cls = "pgrid" if n else "pgrid full"
    priced_list = rows and rows[0][2] is not None
    ulcls = "plist" + (" two" if (not n and priced_list) else "")
    count = "%d items" % len(rows) if priced_list else ""
    return f"""<div class="panel{' on' if first else ''}" id="{c['id']}">
  <div class="wrap">
    <div class="ph">
      <div><span class="label">{c['name']}{(' · ' + count) if count else ''}</span><h2>{c['title']}</h2><p class="lead">{c['blurb']}</p></div>
      <div class="bigbadge"><b>{c['badge'][0]}</b><small>{c['badge'][1]}</small></div>
    </div>
    <div class="{cls}">
      {left}
      <div class="pbody"><ul class="{ulcls}">{lis}</ul>{extras}</div>
    </div>
  </div>
</div>"""


menu_page = f"""
<section class="phero">
  <img class="bg" src="img/paan-tissue.jpg" alt="" data-speed="0.1">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="wrap"><span class="eyebrow reveal">Menu &amp; Products</span><h1 class="split">The <em>Menu</em></h1><p class="reveal" style="--d:.4s">50+ refreshing sodas, natural juices, milkshakes, thickshakes, 30+ paan varieties, waffles, sandwiches, ice creams and many more. The right place to visit to complete your cravings.</p></div>
</section>
<div class="tabs"><div class="wrap"><div class="tabs-in" role="tablist"><span class="tab-ind"></span>{"".join('<button class="tab%s" role="tab" data-tab="%s">%s</button>' % (" on" if i == 0 else "", c["id"], c["name"]) for i, c in enumerate(PANELS))}</div></div></div>
<section class="menu-sec">
  {"".join(panel(c, i == 0) for i, c in enumerate(PANELS))}
  <div class="wrap"><p class="menu-note">Prices are in rupees. Other items and today's specials are available at the counter.</p></div>
</section>
<section class="cta-band">
  <div class="wrap"><h2 class="split">Hungry <em class="s">yet?</em></h2>
  <div class="reveal" style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap"><a class="btn solid" href="{DIR_URL}" target="_blank" rel="noopener">Get Directions</a><a class="btn" href="contact.html#review">Review Us</a></div></div>
</section>
"""

# ============================================================ CONTACT
contact = f"""
<section class="phero">
  <img class="bg" src="img/storefront.jpg" alt="" data-speed="0.1">
  <div class="hero-glow" aria-hidden="true"></div>
  <div class="wrap"><span class="eyebrow reveal">Contact</span><h1 class="split">Come <em>visit</em></h1><p class="reveal" style="--d:.4s">Earth Complex, beside the Akshar Chowk bridge. Open every day until 11:30 PM.</p></div>
</section>
<section class="quick">
  <div class="wrap qgrid">
    <a class="qcard reveal" href="tel:{PHONE_TEL}">{ICO_PHONE}<small>Call</small><b>{PHONE_DISPLAY}</b><span class="go">→</span></a>
    <a class="qcard reveal" style="--d:.1s" href="{WA_LINK}" target="_blank" rel="noopener">{ICO_CHAT}<small>WhatsApp</small><b>Chat with us</b><span class="go">→</span></a>
    <a class="qcard reveal" style="--d:.2s" href="{DIR_URL}" target="_blank" rel="noopener">{ICO_PIN}<small>Directions</small><b>Open in Maps</b><span class="go">→</span></a>
  </div>
</section>
<section class="dark2">
  <div class="wrap">{visit_block()}</div>
</section>
<section class="alt">
  <div class="wrap" style="max-width:820px">
    {sec_head("Feedback", 'Tell us <em class="s">how we did</em>')}
    <div style="margin-top:2.4rem">{feedback("review")}</div>
  </div>
</section>
"""

pages = {
    "index.html": ("Thakur Pan · Paan, Soda & Waffles in Akota, Vadodara", "Thakur Pan at Akshar Chowk, Akota, Vadodara: fresh paan, pan mawa soda, mojitos, waffles, shakes and chai. Open daily 9:30 AM – 11:30 PM.", home, "pg-home"),
    "about.html": ("About · Thakur Pan, Akota Vadodara", "The story of Thakur Pan, a paan shop in Akota, Vadodara, that started with a simple dream in the late 1990s.", about, "pg-about"),
    "menu.html": ("Menu · Thakur Pan, Vadodara", "50+ sodas, natural juices, shakes, 30+ paan varieties, waffles, grill puff, sandwiches and ice cream at Thakur Pan, Akota.", menu_page, "pg-menu"),
    "contact.html": ("Contact & Location · Thakur Pan, Vadodara", "Visit Thakur Pan at Earth Complex, Akshar Chowk, Akota, Vadodara. Open daily 9:30 AM – 11:30 PM.", contact, "pg-contact"),
}
for fn, (t, d, b, bc) in pages.items():
    with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f:
        f.write(page(fn, t, d, b, bc))
print("built", list(pages))
