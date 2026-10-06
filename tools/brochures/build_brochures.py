"""Builds one A4 brochure per product as HTML in tools/brochures/, using the product data in build_product_pages.py
and real screenshots / photos only. Print them to PDF with:  node tools/brochures/print_brochures.mjs
    python tools/brochures/build_brochures.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_product_pages import PRODUCTS  # noqa: E402

P = {p['slug']: p for p in PRODUCTS}
# Reuse the company-profile design (colours, fonts, corner shapes, page grid).
BASE_CSS = re.search(r'<style>(.*?)</style>', (HERE.parent / 'profile' / 'profile.html').read_text(encoding='utf-8'), re.S).group(1)

CSS = BASE_CSS + '''
/* ---------- brochure additions ---------- */
.inner.tight { inset: 20mm 18mm 18mm; }
.cover .logo-tile { position: absolute; left: 18mm; top: 58mm; width: 22mm; height: 22mm; }
.cover .title { top: 86mm; }
.cover .title p { max-width: 120mm; }
.cover .facts { position: absolute; left: 18mm; right: 18mm; bottom: 30mm; display: grid; grid-template-columns: repeat(4, 1fr); gap: 4mm; }
.cover .facts div { border-top: 0.6mm solid var(--lime); padding-top: 3mm; }
.cover .facts b { display: block; font-family: var(--display); font-size: 20pt; color: #fff; line-height: 1.1; }
.cover .facts span { font-size: 8.4pt; color: #aab3bc; }
.cover .visual { position: absolute; right: 18mm; left: 18mm; top: 166mm; height: 72mm; }
.cover .visual img { width: 100%; height: 100%; object-fit: cover; border: 0.3mm solid #2a3138; }
.cover .visual.phones { display: flex; justify-content: center; gap: 6mm; height: 80mm; top: 162mm; }
.cover .visual.phones .phone { height: 80mm; aspect-ratio: 738 / 1500; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }
.panel { background: var(--soft); padding: 5.5mm; border-top: 1.2mm solid var(--navy); }
.panel.lime { border-color: var(--lime); }
.panel h3 { margin-bottom: 2mm; }
.panel p { font-size: 9.6pt; }
ul.ticks { list-style: none; display: grid; gap: 2.2mm; }
ul.ticks li { font-size: 9.6pt; color: var(--text); padding-left: 6mm; position: relative; line-height: 1.45; }
ul.ticks li::before { content: ''; position: absolute; left: 0; top: 1.6mm; width: 2.6mm; height: 2.6mm; background: var(--lime); border: 0.3mm solid var(--lime-dk); }
.figure-wide { margin-top: auto; }
.figure-wide img { width: 100%; height: 72mm; object-fit: cover; display: block; border: 0.3mm solid var(--line); }
.cap { font-size: 8.2pt; color: var(--muted); margin-top: 1.8mm; }
.cap b { color: var(--ink); font-family: var(--display); text-transform: uppercase; margin-right: 1.5mm; }
/* landscape software screenshots */
.screen { border: 0.3mm solid var(--line); background: #0f1215; padding: 1.4mm; }
.screen img { display: block; width: 100%; }
.tour { display: grid; gap: 7mm; }
.tour-row { display: grid; grid-template-columns: 1.45fr 1fr; gap: 6mm; align-items: center; }
.tour-row.flip { grid-template-columns: 1fr 1.45fr; }
.tour-row.flip .screen { order: 2; }
.tour-row h3 { font-size: 13pt; }
.tour-row p { font-size: 9.4pt; margin-bottom: 2.5mm; }
.tour-row .tag { font-family: var(--mono); font-size: 7.5pt; color: var(--lime-dk); font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
/* phone frames for mobile screenshots */
.phone { display: block; border-radius: 5mm; border: 1.3mm solid #1a1d21; background: #000; overflow: hidden; box-shadow: 0 2mm 6mm rgba(0,0,0,.25); }
.phone img { display: block; width: 100%; height: 100%; object-fit: cover; }
.phones3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm 6mm; }
.phones3 figure { margin: 0; }
.phones3 .phone { aspect-ratio: 738 / 1500; width: 43mm; margin: 0 auto; }
.phones3 figcaption { padding: 0 2mm; }
.phones3 figcaption, .phones4 figcaption { margin-top: 2.6mm; font-size: 8.4pt; color: var(--muted); line-height: 1.45; }
.phones3 figcaption b, .phones4 figcaption b { display: block; font-family: var(--display); text-transform: uppercase; color: var(--ink); font-size: 10pt; }
.phones4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; }
.phones4 figure { margin: 0; }
.phones4 .phone { aspect-ratio: 738 / 1500; }
/* features */
.fgrid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; }
.fgrid.two-col { grid-template-columns: 1fr 1fr; }
.fgrid div { border: 0.3mm solid var(--line); padding: 4.5mm; position: relative; }
.fgrid div::before { content: attr(data-n); font-family: var(--mono); font-size: 7.5pt; color: var(--lime-dk); font-weight: 700; display: block; margin-bottom: 1.5mm; }
.fgrid h3 { font-size: 10.5pt; }
.fgrid p { font-size: 8.8pt; line-height: 1.5; }
.flow { display: grid; gap: 3mm; counter-reset: s; }
.flow li { list-style: none; display: grid; grid-template-columns: 11mm 1fr; align-items: start; gap: 3mm; font-size: 9.6pt; color: var(--text); line-height: 1.5; }
.flow li::before { counter-increment: s; content: counter(s, decimal-leading-zero); font-family: var(--display); font-weight: 700; font-size: 15pt; color: var(--navy); line-height: 1; border-bottom: 0.8mm solid var(--lime); padding-bottom: 1mm; }
/* devices */
.hwgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm 4mm; }
.hwgrid figure { margin: 0; }
.hwgrid img { width: 100%; height: 31mm; object-fit: cover; display: block; border: 0.3mm solid var(--line); }
.hwgrid figcaption { font-size: 8.4pt; color: var(--muted); margin-top: 2mm; border-left: 0.8mm solid var(--lime); padding-left: 2.5mm; line-height: 1.45; }
.hwgrid figcaption b { display: block; font-family: var(--display); text-transform: uppercase; color: var(--ink); font-size: 10pt; }
.net { display: grid; grid-template-columns: 1fr auto 1.6fr; align-items: center; gap: 4mm; background: var(--ink); color: #e9edf0; padding: 4.5mm; }
.net .node { border: 0.3mm solid #3a434c; padding: 3.5mm; text-align: center; }
.net .node b { display: block; font-family: var(--display); text-transform: uppercase; font-size: 10.5pt; color: #fff; }
.net .node span { font-size: 8pt; color: #aab3bc; }
.net .node.hub { border-color: var(--lime); background: rgba(182,255,59,.08); }
.net .link { font-family: var(--mono); color: var(--lime); font-size: 8pt; text-align: center; }
.net .clients { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; }
.techbox { background: var(--ink); color: #e9edf0; padding: 6mm; }
.techbox .kicker { color: var(--lime); }
.techbox p { color: #c3cad1; font-size: 9.4pt; margin-top: 2mm; }
.faq-list { display: grid; gap: 3.5mm; }
.faq-list div { border-bottom: 0.3mm solid var(--line); padding-bottom: 3mm; }
.faq-list h3 { font-size: 10.5pt; text-transform: none; font-family: var(--display); }
.faq-list p { font-size: 9.2pt; }
.cta-strip { margin-top: auto; background: var(--ink); color: #fff; padding: 6mm 7mm; display: grid; grid-template-columns: 1fr auto; gap: 4mm; align-items: center; }
.cta-strip h3 { color: #fff; font-size: 15pt; }
.cta-strip p { color: #aab3bc; font-size: 9pt; margin-top: 1mm; }
.cta-strip .contacts { font-family: var(--mono); font-size: 8.6pt; color: #e9edf0; line-height: 1.8; text-align: right; }
.cta-strip .contacts b { color: var(--lime); }
.chips { display: flex; flex-wrap: wrap; gap: 2mm; }
.chips span { font-family: var(--mono); font-size: 7.8pt; text-transform: uppercase; border: 0.3mm solid var(--navy); color: var(--navy); padding: 1.2mm 2.6mm; }
.callouts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3.5mm; }
.callouts div { background: var(--soft); padding: 4mm; border-left: 1mm solid var(--navy); }
.callouts div:nth-child(even) { border-color: var(--lime); }
.callouts h3 { font-size: 10pt; }
.callouts p { font-size: 8.6pt; line-height: 1.5; }
.mt { margin-top: 7mm; }
.ring-two { margin-top: auto; display: grid; grid-template-columns: 34mm 40mm 1fr; gap: 6mm; align-items: end; }
.ring-two figure { margin: 0; }
.ring-two img { display: block; width: 100%; height: 82mm; object-fit: cover; border: 0.3mm solid var(--line); }
.ring-two .phone { height: 82mm; }
.ring-two .phone img { border: 0; }
.mt-s { margin-top: 4mm; }
.sub2 { font-size: 13pt; margin: 7mm 0 3.5mm; }
'''


def esc(s):
    return s


def foot(name, n):
    return f'<div class="foot"><span><b>ANQAH TECH</b> &middot; {name} BROCHURE</span><span>{n:02d}</span></div>'


def page(body, n, name, geo='tr', extra_cls=''):
    shapes = {
        'tr': '<div class="geo tr-navy"></div><div class="geo tr-lime"></div>',
        'tl': '<div class="geo tl-navy"></div><div class="geo tl-lime"></div>',
        'trbl': '<div class="geo tr-navy"></div><div class="geo tr-lime"></div><div class="geo bl-navy"></div><div class="geo bl-lime"></div>',
        'trbr': '<div class="geo tr-navy"></div><div class="geo tr-lime"></div><div class="geo br-navy"></div><div class="geo br-lime"></div>',
    }[geo]
    pad = ' style="margin-left:26mm"' if geo == 'tl' else ''
    body = body.replace('<div class="kicker">', f'<div class="kicker"{pad}>', 1).replace('<h2>', f'<h2{pad}>', 1)
    return f'''
<section class="page {extra_cls}">
    {shapes}
    <div class="inner tight">{body}
    </div>
    {foot(name.upper(), n)}
</section>'''


def cover(p, kicker, title_html, visual, logo=None):
    facts = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in p['facts'])
    logo_html = f'<img class="logo-tile" src="../../{logo}" alt="">' if logo else ''
    return f'''
<section class="page cover">
    <div class="brand"><img src="../../images/logo-mark-white.png" alt=""><span>Anqah Tech</span></div>
    <div class="status"><i></i>PRODUCT BROCHURE<br>{p['category'].upper()}</div>
    {logo_html}
    <div class="title">
        <div class="kicker">{kicker}</div>
        <h1>{title_html}</h1>
        <p>{p['statement']}</p>
    </div>
    {visual}
    <div class="facts">{facts}</div>
    <div class="web"><span><b>www.anqah.com</b></span><span>+971 50 239 3703 &middot; anqahgroups@gmail.com</span></div>
</section>'''


def overview(p, n, kicker, image_html):
    uses = ''.join(f'<li>{u}</li>' for u in p['use_cases'])
    bens = ''.join(f'<li>{b}</li>' for b in p['benefits'])
    return page(f'''
        <div class="kicker">{kicker}</div>
        <h2>Why <em>{p['name']}?</em></h2>
        <div class="two">
            <div class="panel"><h3>The challenge</h3><p>{p['problem']}</p></div>
            <div class="panel lime"><h3>The {p['name']} solution</h3><p>{p['solution']}</p></div>
        </div>
        <div class="two mt">
            <div><h3 class="sub2" style="margin-top:0">Built for</h3><ul class="ticks">{uses}</ul></div>
            <div><h3 class="sub2" style="margin-top:0">What you get</h3><ul class="ticks">{bens}</ul></div>
        </div>
        {image_html}''', n, p['name'])


def features_page(p, n, kicker, cols='', extra=''):
    feats = ''.join(f'<div data-n="{i:02d}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p['features'], 1))
    steps = ''.join(f'<li>{s}</li>' for s in p['steps'])
    return page(f'''
        <div class="kicker">{kicker}</div>
        <h2>Key <em>features</em></h2>
        <div class="fgrid {cols}">{feats}</div>
        <h3 class="sub2">How it works</h3>
        <ol class="flow">{steps}</ol>
        {extra}''', n, p['name'], geo='trbl')


def closing(p, n, extra_top=''):
    faq = ''.join(f'<div><h3>{q}</h3><p>{a}</p></div>' for q, a in p['faq'])
    privacy = f'<div class="panel lime mt-s"><h3>Your data</h3><p>{p["privacy"]}</p></div>' if p.get('privacy') else ''
    return page(f'''
        <div class="kicker">Technical details</div>
        <h2>Under <em>the hood</em></h2>
        {extra_top}
        <div class="techbox"><span class="kicker">Technology</span><p>{p['tech']}</p></div>
        {privacy}
        <h3 class="sub2">Frequently asked questions</h3>
        <div class="faq-list">{faq}</div>
        <div class="cta-strip">
            <div><h3>Get {p['name']} for your business</h3><p>Talk to us for a demo, pricing and installation &mdash; we reply within 24 hours.</p></div>
            <div class="contacts"><b>Phone</b> +971 50 239 3703<br><b>WhatsApp</b> +971 50 576 2100<br><b>Email</b> anqahgroups@gmail.com<br><b>Web</b> www.anqah.com</div>
        </div>''', n, p['name'], geo='trbr')


def html_doc(title, body):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<!-- GENERATED by tools/brochures/build_brochures.py - edit that file (and the product data), not this one. -->
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>{body}
</body>
</html>
'''


# ---------------------------------------------------------------- SELLO
def sello():
    p = P['sello']
    g = {f.replace('.webp', ''): (t, c) for f, t, c, _ in p['gallery']}
    pts = {
        'sello-pos': ['Photo grid by category, barcode and search', 'Live cart with VAT, discounts and notes', 'Hold orders and switch customers'],
        'sello-payment': ['Cash, card or split payments', 'Change calculated automatically', 'Print or share the receipt'],
        'sello-tables': ['Floors and tables with live status', 'Orders taken in rounds', 'Transfer, merge and split bills'],
        'sello-kitchen': ['New, Accepted, Preparing, Ready', 'Kitchen stations and modifiers', 'Replaces paper tickets'],
        'sello-sales': ['Every invoice with payment method', 'Returns and exchanges in one click', 'Reprint and share receipts'],
        'sello-dashboard': ['POS, inventory, purchasing, kitchen', 'Reports, customers and settings', 'Role-based access for staff'],
    }

    def row(key, flip=False):
        t, c = g[key]
        ticks = ''.join(f'<li>{x}</li>' for x in pts[key])
        return (f'<div class="tour-row{" flip" if flip else ""}"><div class="screen"><img src="img/{key}.jpg" alt=""></div>'
                f'<div><span class="tag">SELLO software</span><h3>{t}</h3><p>{c}</p><ul class="ticks">{ticks}</ul></div></div>')

    hw = ''.join(f'<figure><img src="../../images/products/pos-hardware/{f}" alt=""><figcaption><b>{t}</b>{c}</figcaption></figure>'
                 for f, t, c in p['hardware']['items'])
    incl = ''.join(f'<li>{i}</li>' for i in p['hardware']['includes'])
    pages = [
        cover(p, 'POS All-in-One Solution', 'SELLO<span>POS system</span>',
              '<div class="visual"><img src="../profile/img/sello-pos-device.jpg" alt=""></div>', logo='images/products/sello-logo.png'),
        overview(p, 2, '01 &middot; Overview',
                 '<figure class="figure-wide"><img src="../profile/img/sello-dashboard-device.jpg" alt="" style="object-position:center 40%"><figcaption class="cap"><b>Dashboard</b>One home screen for POS, inventory, purchasing, kitchen, reports and settings.</figcaption></figure>'),
        page(f'''
        <div class="kicker">02 &middot; The software</div>
        <h2>Inside <em>SELLO</em></h2>
        <p class="lead" style="margin-bottom:6mm">Real screens from SELLO running a demo shop. Every till, tablet and kitchen screen opens SELLO in the browser over your shop network.</p>
        <div class="tour">{row('sello-pos')}{row('sello-payment', True)}{row('sello-tables')}</div>''', 3, p['name']),
        page(f'''
        <div class="kicker">02 &middot; The software</div>
        <h2>Sales <em>&amp; kitchen</em></h2>
        <div class="tour" style="margin-top:2mm">{row('sello-sales')}{row('sello-dashboard', True)}</div>
        <div class="tour-row mt" style="grid-template-columns: 52mm 1fr"><div class="screen"><img src="img/sello-kitchen.jpg" alt=""></div>
            <div><span class="tag">SELLO software</span><h3>{g['sello-kitchen'][0]}</h3><p>{g['sello-kitchen'][1]}</p><ul class="ticks">{''.join(f'<li>{x}</li>' for x in pts['sello-kitchen'])}</ul></div></div>''', 4, p['name'], geo='tl'),
        features_page(p, 5, '03 &middot; Capabilities'),
        page(f'''
        <div class="kicker">04 &middot; The devices</div>
        <h2>POS <em>hardware</em></h2>
        <p class="lead" style="margin-bottom:5mm">We supply the POS machines, install SELLO, set up your products and taxes, and train your staff &mdash; hardware and software from one supplier.</p>
        <div class="hwgrid">{hw}</div>
        <h3 class="sub2">How the devices connect</h3>
        <div class="net">
            <div class="node hub"><b>Shop PC / server</b><span>Hosts SELLO and the database</span></div>
            <div class="link">&larr; shop LAN &rarr;<br>no internet needed</div>
            <div class="clients">
                <div class="node"><b>POS terminals</b><span>Billing at the counter</span></div>
                <div class="node"><b>Tablets</b><span>Table-side orders</span></div>
                <div class="node"><b>Kitchen display</b><span>Live order tickets</span></div>
                <div class="node"><b>Printers &amp; drawer</b><span>Receipts and cash</span></div>
            </div>
        </div>
        <div class="incl mt-s"><span class="kicker">Every POS package includes</span><ul>{incl}</ul></div>''', 6, p['name'], geo='tl'),
        closing(p, 7),
    ]
    return html_doc('SELLO - Product Brochure', ''.join(pages))


# ---------------------------------------------------------------- SELLO Lite
def sello_lite():
    p = P['sello-lite']
    tabs = p['tabs']
    imgmap = {'sello-lite-sell.webp': 'lite-sell.jpg', 'sello-lite-portions.webp': 'lite-portions.jpg', 'sello-lite-pending.webp': 'lite-pending.jpg',
              'sello-lite-payments.webp': 'lite-payments.jpg', 'sello-lite-taxes.webp': 'lite-taxes.jpg', 'sello-lite-report.webp': 'lite-report.jpg'}
    phones = ''.join(f'<figure><div class="phone"><img src="img/{imgmap[img]}" alt=""></div><figcaption><b>{label}</b>{text}</figcaption></figure>'
                     for label, img, title, text, pts in tabs)
    more = [('lite-product.jpg', 'Products', 'Add products with a price, photo, category and stock tracking.'),
            ('lite-more.jpg', 'Settings', 'Business details, taxes, receipts, payments, security and backup in one menu.'),
            ('lite-language.jpg', 'Language &amp; currency', 'English, Spanish, French, Arabic and Hindi, with local currencies including AED.'),
            ('lite-security.jpg', 'Security', 'Require unlock to open the app, with an auto-lock timer.')]
    phones4 = ''.join(f'<figure><div class="phone"><img src="img/{f}" alt=""></div><figcaption><b>{t}</b>{c}</figcaption></figure>' for f, t, c in more)
    pages = [
        cover(p, 'Offline mobile POS', 'SELLO Lite<span>mobile POS app</span>',
              '<div class="visual phones"><div class="phone"><img src="img/lite-sell.jpg" alt=""></div><div class="phone"><img src="img/lite-portions.jpg" alt=""></div><div class="phone"><img src="img/lite-report.jpg" alt=""></div></div>',
              logo='images/products/sello-lite-logo.png'),
        overview(p, 2, '01 &middot; Overview',
                 '<div class="mt"><h3 class="sub2" style="margin-top:0">Licensing</h3><div class="two"><div class="panel"><h3>7-day free trial</h3><p>Every install starts with a full 7-day free trial &mdash; no card needed.</p></div><div class="panel lime"><h3>One-time activation</h3><p>An activation code tied to the device unlocks a 1, 2 or 5-year plan &mdash; no monthly subscription and no per-seat billing.</p></div></div></div>'),
        page(f'''
        <div class="kicker">02 &middot; The app</div>
        <h2>Inside <em>SELLO Lite</em></h2>
        <p class="lead" style="margin-bottom:6mm">Real screens from the SELLO Lite app on an Android phone.</p>
        <div class="phones3">{phones}</div>''', 3, p['name'], geo='tl'),
        page(f'''
        <div class="kicker">02 &middot; The app</div>
        <h2>Set up <em>your way</em></h2>
        <p class="lead" style="margin-bottom:6mm">Products, receipts, payments, languages and security are all managed on the device.</p>
        <div class="phones4">{phones4}</div>
        <h3 class="sub2">Runs on</h3>
        <div class="callouts">
            <div><h3>Android phones</h3><p>A complete till in your pocket for counters, stalls and deliveries.</p></div>
            <div><h3>Android tablets</h3><p>A bigger product grid for busy counters and caf&eacute;s.</p></div>
            <div><h3>Receipts</h3><p>Print or share receipts sized for A4 or 80 / 78 / 58 mm thermal rolls, with your logo.</p></div>
        </div>''', 4, p['name']),
        features_page(p, 5, '03 &middot; Capabilities'),
        closing(p, 6),
    ]
    return html_doc('SELLO Lite - Product Brochure', ''.join(pages))


# ---------------------------------------------------------------- Automatic Bell
def bell():
    p = P['automatic-bell']
    imgs = {'bell-app-home.webp': 'bell-home.jpg', 'bell-app-ringing.webp': 'bell-ringing.jpg', 'bell-app-schedule.webp': 'bell-schedule.jpg',
            'bell-app-weekdays.webp': 'bell-weekdays.jpg', 'bell-app-holidays.webp': 'bell-holidays.jpg', 'bell-app-settings.webp': 'bell-settings.jpg'}
    phones = ''.join(f'<figure><div class="phone"><img src="img/{imgs[img]}" alt=""></div><figcaption><b>{label}</b>{text}</figcaption></figure>'
                     for label, img, title, text, pts in p['tabs'])
    chips = ''.join(f'<span>{a}</span>' for a in p['audience'])
    pages = [
        cover(p, 'IoT &middot; School automation', 'Automatic<span>school bell</span>',
              '<div class="visual"><img src="img/bell-panel.jpg" alt=""></div>'),
        overview(p, 2, '01 &middot; Overview',
                 f'<div class="mt"><h3 class="sub2" style="margin-top:0">Who uses it</h3><div class="chips">{chips}</div></div>'
                 '<div class="ring-two"><figure><img src="img/bell-buttons.jpg" alt=""><figcaption class="cap"><b>On the panel</b>Power light and the one-touch manual ring button.</figcaption></figure>'
                 '<figure><div class="phone"><img src="img/bell-ringing.jpg" alt=""></div><figcaption class="cap"><b>On the phone</b>Ring for 3, 5, 10 or 30 seconds from the app.</figcaption></figure>'
                 '<div class="panel lime"><h3>Two ways to ring</h3><p>Bells ring automatically on the timetable. For assemblies, drills or emergencies, ring by hand from the panel button or from the app on your phone.</p></div></div>'),
        page(f'''
        <div class="kicker">02 &middot; The device</div>
        <h2>The <em>bell controller</em></h2>
        <p class="lead" style="margin-bottom:5mm">A wall-mounted controller wired into your existing bell circuit. It keeps its own time, rings on schedule and can be rung by hand.</p>
        <figure class="figure-wide" style="margin-top:0"><img src="img/bell-panel.jpg" alt="" style="height:78mm"><figcaption class="cap"><b>Installed controller</b>Power indicator, a one-touch manual ring button, and the controller inside the panel.</figcaption></figure>
        <h3 class="sub2">What&rsquo;s inside</h3>
        <div class="callouts">
            <div><h3>Smart controller</h3><p>An ESP32 microcontroller runs the schedule and serves the app over WiFi.</p></div>
            <div><h3>Real-time clock</h3><p>A DS3231 clock keeps accurate time through power cuts and WiFi outages.</p></div>
            <div><h3>Relay output</h3><p>Switches your existing bell on and off &mdash; wired in series with its power feed.</p></div>
            <div><h3>WiFi enabled</h3><p>Joins the school network; falls back to its own setup hotspot if it can&rsquo;t connect.</p></div>
            <div><h3>Manual ring button</h3><p>Ring instantly from the panel &mdash; or from the app &mdash; for assemblies and drills.</p></div>
            <div><h3>Local only</h3><p>No cloud service: schedules, holidays and WiFi settings are stored on the device.</p></div>
        </div>''', 3, p['name'], geo='tl'),
        page(f'''
        <div class="kicker">03 &middot; The app</div>
        <h2>The <em>app</em></h2>
        <p class="lead" style="margin-bottom:6mm">Real screens from the School Bell app.</p>
        <div class="phones3">{phones}</div>''', 4, p['name']),
        features_page(p, 5, '04 &middot; Capabilities', cols='', extra='''
        <div class="two mt-s"><div class="panel"><h3>Installation</h3><p>We mount the controller near your existing bell, wire it into the bell&rsquo;s power circuit, join it to the school WiFi and enter your timetable. After that, every change is made from the app &mdash; no electrician needed.</p></div>
        <div class="panel lime"><h3>Not just schools</h3><p>Colleges, hostels, madrasas, training centres, factories and offices use the same system for periods, meals, shifts and breaks.</p></div></div>'''),
        closing(p, 6),
    ]
    return html_doc('Automatic Bell - Product Brochure', ''.join(pages))


def main():
    for name, fn in (('sello', sello), ('sello-lite', sello_lite), ('automatic-bell', bell)):
        (HERE / f'{name}.html').write_text(fn(), encoding='utf-8')
        print('wrote', f'tools/brochures/{name}.html')


if __name__ == '__main__':
    main()
