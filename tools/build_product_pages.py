"""Generates the static product detail pages in /products from the data below.

Edit a product's content here, then run:  python tools/build_product_pages.py
"""
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.anqah.com'
WHATSAPP = '971505762100'
PHONE = '+971502393703'

PRODUCTS = [
    {
        'slug': 'sello',
        'name': 'SELLO',
        'category': 'POS & Shop Management',
        'status': None,
        'logo': 'images/products/sello-logo.png',
        'scene': 'sello',
        # Real screenshots, captured from SELLO running a demo shop with sample data.
        'gallery': [
            ('sello-pos.webp', 'Point of sale', 'Fast touch billing with categories, barcode search and a live cart with VAT.', 'sello.local/pos'),
            ('sello-payment.webp', 'Checkout', 'Cash, card or split payments, with change calculated automatically.', 'sello.local/pos'),
            ('sello-tables.webp', 'Restaurant tables', 'See every table at a glance, seat guests and manage orders in rounds.', 'sello.local/restaurant/tables'),
            ('sello-kitchen.webp', 'Kitchen display', 'A tablet at the kitchen pass, where tickets flow from New to Accepted, Preparing and Ready.', 'sello.local/kitchen'),
            ('sello-sales.webp', 'Sales history', 'Every invoice with payment method, items and one-click returns or exchanges.', 'sello.local/pos/sales'),
            ('sello-dashboard.webp', 'Dashboard', 'One home screen for POS, inventory, purchasing, kitchen, reports and settings.', 'sello.local/dashboard'),
        ],
        'terminal': 'sello --mode=retail,restaurant|sello install --windows --lan|sello report sales --export=pdf',
        'statement': 'A complete point-of-sale and shop management system for retail stores, restaurants and cafés '
                     '&mdash; running on your own shop network, so billing never waits for the internet.',
        'facts': [('2', 'Business modes: retail &amp; restaurant'), ('LAN', 'Runs on your own shop network'),
                  ('0', 'Internet needed to bill'), ('1-click', 'Windows installer')],
        'problem': 'Shops and restaurants juggle separate tools for billing, stock, kitchen orders and accounts '
                   '&mdash; and cloud POS systems stop working the moment the internet drops.',
        'solution': 'SELLO puts billing, inventory, purchasing, restaurant operations and reporting into one system. '
                    'One shop PC hosts SELLO, and every till, kitchen screen and back-office device connects to it '
                    'over the local network.',
        'features': [
            ('Retail billing', 'Barcode search, split and credit sales, quotations, receipts and invoices.'),
            ('Restaurant &amp; café mode', 'Floors, tables, reservations, modifiers, kitchen display and kitchen stations, bill splitting.'),
            ('Inventory &amp; catalogue', 'Products with photos and barcodes, categories, brands, units, taxes, pricing tiers, stock transfers and counts.'),
            ('Purchasing &amp; suppliers', 'Purchases, purchase returns and supplier ledgers.'),
            ('Customers &amp; credit', 'Customer accounts, payments allocated to invoices, statements and ageing.'),
            ('Recipes &amp; production', 'Recipe-based inventory, production runs and wastage tracking.'),
            ('Finance &amp; reports', 'Expenses, tax, profit, stock and sales reports &mdash; export to PDF, Excel or CSV.'),
            ('Registers &amp; terminals', 'Registers, shifts, a customer-facing display, gift vouchers, returns and exchanges.'),
            ('Security &amp; control', 'Roles and permissions, PIN lock, audit log, multi-business and multi-location support.'),
        ],
        'steps': [
            'Install SELLO on one shop PC with the one-click Windows installer.',
            'Run the setup wizard: create the business, location and owner account, and pick retail or restaurant mode.',
            'Connect tills, kitchen screens and back-office devices over the shop network &mdash; they just open SELLO in a browser.',
            'Sell, track stock and run reports, with built-in backup and restore keeping the data safe.',
        ],
        'use_cases': ['Supermarkets, grocery and retail stores', 'Restaurants, cafés and cloud kitchens',
                      'Multi-counter shops with several tills', 'Businesses running more than one location or brand'],
        'benefits': ['Billing keeps working through internet outages', 'One system instead of separate billing, stock and kitchen tools',
                     'Your data stays on your own server', 'Staff only see what their role allows'],
        'tech': 'Node.js (NestJS) server with a PostgreSQL database and a React web app. One shop server hosts the API, '
                'database and app; other devices on the same network connect through the browser. Ships with a Windows '
                'installer, runs as a Windows service, includes a print agent for receipt printers, and has backup, '
                'restore and system diagnostics built in.',
        'privacy': 'SELLO runs on your own hardware. Business, sales and customer data are stored in your shop&rsquo;s '
                   'database, not on a third-party cloud.',
        'faq': [
            ('Does SELLO need the internet?', 'No. SELLO runs on your shop&rsquo;s local network, so billing, stock and reports keep working without an internet connection.'),
            ('Does it work for restaurants?', 'Yes. Restaurant and café mode adds floors and tables, reservations, modifiers, kitchen display and bill splitting.'),
            ('Which devices can use it?', 'Any device on the shop network with a web browser &mdash; PCs, tablets or touch terminals.'),
            ('Where is my data stored?', 'In a database on your own shop server. Built-in backup and restore let you keep your own copies.'),
        ],
    },
    {
        'slug': 'sello-lite',
        'name': 'SELLO Lite',
        'category': 'Mobile POS',
        'status': 'Beta',
        'logo': 'images/products/sello-lite-logo.png',
        'scene': 'selloLite',
        # Real SELLO Lite screenshots, shown in tabs: (tab, screenshot, heading, text, points)
        'tabs': [
            ('Sell', 'sello-lite-sell.webp', 'Ring up a sale in seconds',
             'Tap products from a photo grid, filter by category or search, and charge from the bar at the bottom.',
             ['Photo grid with categories', 'Search and barcode lookup', 'One-tap charge']),
            ('Portions', 'sello-lite-portions.webp', 'Sell the same dish in different sizes',
             'Each product can have its own portions &mdash; single, half, full, small, large &mdash; each with its own price.',
             ['Custom portion names', 'Separate price per portion', 'Picked right at checkout']),
            ('Hold &amp; resume', 'sello-lite-pending.webp', 'Park an order and come back to it',
             'Hold a cart when a customer steps away and resume it later, without re-entering anything.',
             ['Held carts with item count and total', 'Resume or cancel in one tap', 'Nothing is lost offline']),
            ('Payments', 'sello-lite-payments.webp', 'Take payment the way customers pay',
             'Choose which payment methods appear at checkout and split a bill across several of them.',
             ['Cash, card, bank transfer, QR', 'Mobile wallet and pay later', 'Split payments in one sale']),
            ('Taxes', 'sello-lite-taxes.webp', 'Set up the taxes you charge',
             'Add tax rates once &mdash; standard, zero-rated or exempt &mdash; and choose whether prices include tax.',
             ['Standard, zero-rated, exempt', 'Tax-inclusive or added at checkout', 'Default tax per product']),
            ('Reports', 'sello-lite-report.webp', 'See how the shop is doing',
             'Sales for today, this week, this month or any range, with payment and tax breakdowns and best sellers.',
             ['Sales, tax and average sale', 'How customers paid', 'Best sellers &middot; export CSV / PDF']),
        ],
        'terminal': 'sello-lite --offline|sello-lite receipt --width=80mm|sello-lite backup --export',
        'statement': 'An offline-first point-of-sale app for restaurants, cafés and small shops &mdash; no internet '
                     'connection needed to make a sale.',
        'facts': [('100%', 'Offline checkout'), ('5', 'Languages incl. Arabic'), ('7-day', 'Free trial'), ('0', 'Monthly subscription')],
        'problem': 'Small food and retail businesses often deal with unreliable internet, yet most POS apps stop working '
                   'the moment connectivity drops &mdash; blocking checkout at the worst possible time.',
        'solution': 'SELLO Lite treats offline as the default. Every sale, product and receipt is stored on the device, '
                    'so the till keeps working through outages, and the owner backs up the data on their own terms.',
        'features': [
            ('Portions per item', 'Quarter / half / full for a dish, or small / medium / large for a drink &mdash; each with its own price.'),
            ('Split payments', 'Cash, card, bank transfer, QR, mobile wallet or store credit in a single sale.'),
            ('Hold &amp; resume carts', 'An interrupted order never has to be re-entered from scratch.'),
            ('Receipts that fit', 'Print or share receipts sized for A4 or 80 / 78 / 58 mm thermal rolls, with your logo.'),
            ('Sales reports', 'Day, week, month, year or custom range, with payment and tax breakdowns and best-sellers &mdash; export to CSV or PDF.'),
            ('One-tap backup', 'Export your own copy of the sales database at any time.'),
        ],
        'steps': [
            'Set up the catalogue once: products, categories, tax rates and portion sizes.',
            'Ring up sales from the till screen, holding a cart mid-order and resuming it later.',
            'Take payment &mdash; split across several methods if needed.',
            'Print or share the receipt, sized for your printer or paper.',
            'Check performance in Reports and export any period as CSV or PDF.',
        ],
        'use_cases': ['Restaurants and cafés selling dishes in several portion sizes', 'Small shops that want a simple till without a cloud subscription',
                      'Businesses where internet is unreliable or costly', 'Owners who want sales data on their own device'],
        'benefits': ['Keeps taking sales through internet outages', 'One-time device activation (1, 2 or 5-year plans) &mdash; no recurring per-seat billing',
                     'Sales data stays on the device you control', 'English, Spanish, French, Hindi and Arabic, with right-to-left layout'],
        'tech': 'React Native (Expo) app for Android with a local SQLite database as the system of record. Schema changes ship '
                'as additive, versioned migrations, so updates never drop existing data. Receipts and reports are generated '
                'on the device, and backups are a point-in-time copy of the database file.',
        'privacy': 'All business, product and sales data is stored on the device. Nothing is sent to Anqah Tech or any third '
                   'party; backups are exported only when the owner chooses to.',
        'faq': [
            ('Does it need an internet connection?', 'No. Sales, receipts and reports all work fully offline.'),
            ('What happens to my data when I update?', 'Nothing is lost. Database changes are additive-only, so updates keep everything already on the device.'),
            ('How does licensing work?', 'Every install starts with a 7-day free trial. After that, a one-time activation code tied to the device unlocks a 1, 2 or 5-year plan &mdash; no subscription.'),
        ],
    },
    {
        'slug': 'automatic-bell',
        'name': 'Automatic Bell',
        'category': 'IoT &middot; School Automation',
        'status': 'Pilot',
        'logo': None,
        'scene': 'bell',
        # Real School Bell app screens (frames from the app recording): (tab, screenshot, heading, text, points)
        'tabs': [
            ('Home', 'bell-app-home.webp', 'Everything at a glance',
             'The current time, the next bell, today&rsquo;s schedule and a manual ring &mdash; all on one screen.',
             ['Live clock from the controller', 'Next bell and today&rsquo;s bells', 'Manual ring on the same screen']),
            ('Manual ring', 'bell-app-ringing.webp', 'Ring the bell from your phone',
             'Pick 3, 5, 10 or 30 seconds &mdash; or type any duration &mdash; and tap Ring for assemblies, drills or emergencies.',
             ['Quick 3s / 5s / 10s / 30s presets', 'Custom duration in seconds', 'Instant confirmation in the app']),
            ('Schedule', 'bell-app-schedule.webp', 'Set the daily timetable',
             'Up to 10 bells a day. Switch each one on or off, set its time and how many seconds it rings.',
             ['Up to 10 bells per day', 'On / off per bell', 'Ring length per bell']),
            ('Weekdays', 'bell-app-weekdays.webp', 'Choose the working days',
             'Tap a day to mark it off &mdash; no bells ring on weekends or any day you switch off.',
             ['Tap a day to turn it off', 'Weekends skipped automatically', 'Saved on the controller']),
            ('Holidays', 'bell-app-holidays.webp', 'Skip holidays and exam days',
             'Add dates once and the bell stays silent on those days, then carries on as normal.',
             ['Pick dates from a calendar', 'Remove a holiday in one tap', 'No rewiring or reprogramming']),
            ('Settings', 'bell-app-settings.webp', 'Connect to the school WiFi',
             'Point the app at the controller, test the connection and join it to the school network.',
             ['Device address or setup hotspot', 'Test connection', 'WiFi setup with save &amp; restart']),
        ],
        # Product images supplied by Anqah Tech: (file, title, caption)
        'photos': [
            ('bell-system-steel.webp', 'Wall panel + app control',
             'A brushed-steel wall panel with a one-touch bell button, managed from the phone app and an office dashboard.'),
            ('bell-system-white.webp', 'Timetable at a glance',
             'Upcoming bells on the phone, the full timetable on the dashboard, and a manual trigger whenever you need it.'),
        ],
        'terminal': 'bell.schedule load timetable.json|bell.holidays add 2026-12-02|bell.ring --manual',
        'statement': 'A WiFi school bell controller that rings automatically on a preset schedule, skips weekends and '
                     'holidays on its own, and is managed from a mobile app.',
        'facts': [('10', 'Scheduled bells per day'), ('RTC', 'Keeps time through outages'), ('WiFi', 'App control on the local network'), ('0', 'Cloud services needed')],
        'problem': 'Schools still depend on staff ringing the bell by hand, or on mechanical timers that can&rsquo;t skip '
                   'holidays, adjust for exam days, or be changed without visiting the control box.',
        'solution': 'A relay wired into the bell&rsquo;s power circuit, controlled by an ESP32 with a real-time clock for '
                    'accurate offline timekeeping, plus a mobile app that manages schedules, holidays and manual rings over '
                    'the school network.',
        'features': [
            ('Automatic schedule', 'Rings on a configurable daily timetable, up to 10 bells.'),
            ('Weekends &amp; holidays', 'Skips weekends and specific holiday dates automatically.'),
            ('Manual ring', 'Ring from the app for assemblies, drills or emergencies.'),
            ('Accurate offline', 'An onboard real-time clock keeps time through power and WiFi outages.'),
            ('Easy WiFi setup', 'Falls back to its own setup hotspot if the network can&rsquo;t be reached.'),
        ],
        'steps': [
            'The controller checks its clock every minute against the saved bell schedule.',
            'When a bell is due &mdash; and it isn&rsquo;t a weekend or holiday &mdash; it switches the relay on the bell circuit.',
            'The bell rings for the configured duration, then the relay releases automatically.',
            'Schedules, holidays and WiFi settings are managed from the companion app.',
        ],
        'use_cases': ['Period and break bells without staff ringing them', 'Skipping bells on public holidays and exam days',
                      'Ringing manually for assemblies, drills or unscheduled events'],
        'benefits': ['No more missed or late bells', 'Timetable changes from a phone &mdash; no rewiring or reprogramming',
                     'Keeps ringing on time through power cuts and WiFi outages'],
        'tech': 'ESP32 microcontroller running Arduino-based firmware, a DS3231 real-time clock module, and a relay wired in '
                'series with the bell&rsquo;s power feed. The ESP32 serves a local HTTP API on the school WiFi, and a Flutter '
                'mobile app manages schedules, weekday and holiday exclusions, and device settings.',
        'privacy': 'The device talks only over the local network and sends nothing to any cloud service. Schedules, holidays '
                   'and WiFi credentials are stored on the device itself.',
        'faq': [
            ('Does it work if the WiFi goes down?', 'Yes. The real-time clock keeps accurate time on its own, so scheduled bells keep ringing.'),
            ('Can school staff change the schedule?', 'Yes. Schedules, holidays and settings are all managed from the mobile app &mdash; no electrician needed after installation.'),
        ],
    },
    {
        'slug': 'water-monitoring',
        'name': 'Water Monitoring',
        'category': 'IoT &middot; Monitoring',
        'status': None,
        'logo': None,
        'scene': 'water',
        'terminal': 'water.monitor --tank=1 --live|alerts.telegram --empty-below=15 --overflow-above=95|water.level --watch',
        'statement': 'Real-time water tank monitoring &mdash; the level updates live on your phone as the tank fills and '
                     'empties, and Telegram alerts you before it runs dry or overflows.',
        'facts': [('Live', 'Tank level on your phone'), ('&lt;15%', 'Telegram: tank empty'), ('&gt;95%', 'Telegram: overflow'), ('24/7', 'Monitoring')],
        'problem': 'Tanks overflow and waste water, or run dry without warning &mdash; and checking levels means climbing '
                   'onto the roof or opening an underground sump.',
        'solution': 'A level sensor on the tank reports the water level continuously. The phone app shows it live as it '
                    'rises and falls, and a Telegram message warns you the moment the tank drops below 15% or goes above 95%.',
        'features': [
            ('Live level on your phone', 'The percentage on the app rises and falls in real time, exactly as the water in the tank does.'),
            ('Tank-empty alert', 'When the level drops below 15%, a Telegram message tells you the tank is nearly empty.'),
            ('Overflow alert', 'When the level goes above 95%, a Telegram message warns you before the tank overflows.'),
            ('Filling or in use', 'See at a glance whether the tank is filling up or being used.'),
            ('Overhead &amp; sump tanks', 'Works with rooftop and underground tanks.'),
        ],
        'steps': [
            'A level sensor is mounted on the tank lid and measures the water level continuously.',
            'The level is sent to the phone app, where it updates live as the tank fills and empties.',
            'Below 15%, a Telegram message says the tank is empty &mdash; time to refill.',
            'Above 95%, a Telegram message warns of overflow &mdash; time to stop the water.',
        ],
        'use_cases': ['Villas and homes with rooftop tanks', 'Apartment buildings', 'Farms and commercial sites'],
        'benefits': ['No overflow or wasted water', 'Never run out of water unexpectedly', 'No more climbing up to check the tank',
                     'Alerts on Telegram, wherever you are'],
        'tech': 'A level sensor on the tank lid reads the water level continuously and sends it to the app. Alerts are '
                'delivered as Telegram messages at two thresholds: below 15% (tank empty) and above 95% (overflow). '
                'Contact us for sensor options and installation details for your tanks.',
        'privacy': None,
        'faq': [
            ('How quickly does the app update?', 'Continuously &mdash; the level on your phone rises and falls along with the water in the tank.'),
            ('When do I get alerts?', 'You get a Telegram message when the level drops below 15% (tank empty) and when it goes above 95% (overflow).'),
            ('Do I need Telegram?', 'Yes &mdash; alerts are sent as Telegram messages, so install Telegram on the phone that should receive them.'),
        ],
    },
]


# Reuse the exact WhatsApp icon from the home page
WA_ICON = re.search(r'<svg viewBox="0 0 24 24".*?</svg>', (ROOT / 'index.html').read_text(encoding='utf-8'), re.S).group(0)


def wa_link(text):
    return f'https://wa.me/{WHATSAPP}?text={quote(text)}'


def header():
    return '''    <div class="scanlines" aria-hidden="true"></div>
    <header id="header">
        <div class="statusbar" aria-hidden="true">
            <span><i class="led"></i> SYS.ONLINE</span>
            <span class="sb-hide">NODE: ABU DHABI // 24.45&deg;N 54.38&deg;E</span>
            <span class="sb-hide">BUILD 2026.10</span>
            <span>GST <b id="clock">--:--:--</b></span>
        </div>
        <nav class="navbar">
            <a href="../index.html" class="logo" aria-label="Anqah Tech home">
                <img src="../images/logo-mark-white.png" alt="Anqah Tech logo" width="48" height="35">
                <span class="logo-text"><span><b>Anqah</b> Tech</span><small>Pvt Limited</small></span>
            </a>
            <ul class="nav-links" id="navLinks">
                <li><a href="../index.html#products" aria-current="page">Products</a></li>
                <li><a href="../index.html#services">Services</a></li>
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#why">Why Us</a></li>
                <li><a href="../index.html#contact">Contact</a></li>
            </ul>
            <a href="../index.html#contact" class="btn btn-accent nav-cta">Talk to us <span class="arr">&rarr;</span></a>
            <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false">
                <span></span><span></span>
            </button>
        </nav>
    </header>'''


def footer():
    links = ''.join(f'<a href="{p["slug"]}.html">{p["name"]}</a>' for p in PRODUCTS)
    return f'''    <footer>
        <div class="footer-top">
            <p class="footer-big">Smart solutions.<br>Reliable service.</p>
            <a href="../index.html#contact" class="btn btn-accent">Start a project <span class="arr">&rarr;</span></a>
        </div>
        <div class="footer-grid">
            <div>
                <a href="../index.html" class="logo"><img src="../images/logo-mark-white.png" alt="" width="48" height="35"><span class="logo-text"><span><b>Anqah</b> Tech</span><small>Pvt Limited</small></span></a>
            </div>
            <div>
                <h4>Products</h4>
                {links}
            </div>
            <div>
                <h4>Services</h4>
                <a href="../index.html#services">Web Development</a><a href="../index.html#services">Mobile Apps</a><a href="../index.html#services">CCTV &amp; Security</a><a href="../index.html#services">Home Automation</a><a href="../index.html#services">IT Infrastructure</a>
            </div>
            <div>
                <h4>Contact</h4>
                <a href="tel:{PHONE}">+971 50 239 3703</a><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a><a href="mailto:anqahgroups@gmail.com">anqahgroups@gmail.com</a><span>Abu Dhabi, UAE</span>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; <span id="year">2026</span> Anqah Tech Pvt Limited. All rights reserved.</span>
            <span class="mono">// engineered in Abu Dhabi, UAE</span>
        </div>
    </footer>'''


def logo_tile(p, cls='pd-logo'):
    if p['logo']:
        return f'<img class="{cls}" src="../{p["logo"]}" alt="{p["name"]} logo" width="72" height="72">'
    initials = ''.join(w[0] for w in p['name'].split()[:2]).upper()
    return f'<span class="{cls} pd-logo-mono" aria-hidden="true">{initials}</span>'


def tabs_section(p, n):
    folder = f'../images/products/{p["slug"]}'
    sid = f'{p["slug"]}-tabs'
    tabs = ''.join(
        f'<button class="tab" role="tab" id="{sid}-t{i}" aria-controls="{sid}-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="tab-i">{i + 1:02d}</span>{label}</button>'
        for i, (label, *_rest) in enumerate(p['tabs']))
    panels = ''.join(
        f'<div class="tab-panel" role="tabpanel" id="{sid}-p{i}" aria-labelledby="{sid}-t{i}"{"" if i == 0 else " hidden"}>'
        f'<figure class="phone-frame"><img src="{folder}/{img}" alt="{p["name"]} {label.replace("&amp;", "and").lower()} screen" width="738" height="1600" loading="{"eager" if i == 0 else "lazy"}"></figure>'
        f'<div class="tab-copy"><span class="tag">{label}</span><h3>{title}</h3><p>{text}</p>'
        f'<ul class="pd-list">{"".join(f"<li>{pt}</li>" for pt in points)}</ul></div></div>'
        for i, (label, img, title, text, points) in enumerate(p['tabs']))
    return f'''
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{p["name"]} in action</h2><p>Real screens from the {p["name"]} app. Pick a feature to see it.</p></div></header>
            <div class="tabs reveal" data-tabs>
                <div class="tab-list" role="tablist" aria-label="{p["name"]} features">{tabs}</div>
                <div class="tab-panels">{panels}</div>
            </div>
        </section>
'''


def photos_section(p, n):
    folder = f'../images/products/{p["slug"]}'
    figs = ''.join(
        f'<figure class="photo reveal"><a href="{folder}/{f}" data-lightbox="{p["slug"]}" data-caption="{t} &mdash; {c}">'
        f'<img src="{folder}/{f}" alt="{p["name"]}: {t.lower()}" width="1408" height="768" loading="{"eager" if i == 0 else "lazy"}">'
        f'<span class="shot-zoom">[ enlarge ]</span></a><figcaption><b>{t}</b>{c}</figcaption></figure>'
        for i, (f, t, c) in enumerate(p['photos']))
    return f'''
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{p["name"]} system</h2><p>The wall panel, the mobile app and the dashboard working together. Click an image to enlarge.</p></div></header>
            <div class="photos">{figs}</div>
        </section>
'''


def gallery_section(p, n):
    # Each screen is shown on a real POS terminal photo (`*-device.webp`); clicking opens the raw screenshot.
    folder = f'../images/products/{p["slug"]}'
    shots = ''.join(
        f'<figure class="shot reveal">'
        f'<a href="{folder}/{f}" data-lightbox="{p["slug"]}" data-caption="{t} &mdash; {c}">'
        f'<img src="{folder}/{f.replace(".webp", "-device.webp")}" alt="{p["name"]} {t.lower()} screen on a POS terminal" '
        f'width="1000" height="750" loading="{"eager" if i == 0 else "lazy"}">'
        f'<span class="shot-zoom">[ view screen ]</span>'
        f'</a><figcaption><b>{t}</b>{c}</figcaption></figure>'
        for i, (f, t, c, _url) in enumerate(p['gallery']))
    return f'''
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{p["name"]} in action</h2><p>Real screens from {p["name"]}, running a demo café &amp; mart, each shown on a different kind of POS hardware. Click any screen to see it full size.</p></div></header>
            <div class="gallery">{shots}</div>
            <p class="credit">POS hardware and product photos via <a href="https://unsplash.com" target="_blank" rel="noopener">Unsplash</a>. Screens are from a demo shop with sample data.</p>
        </section>
'''


def page(p):
    name = p['name']
    plain = lambda s: s.replace('&mdash;', '-').replace('&rsquo;', "'").replace('&amp;', '&').replace('&middot;', '-')
    enquire = wa_link(f"Hello Anqah Tech, I'm interested in {name}. Please share more details.")
    status = f'<span class="pd-status">{p["status"]}</span>' if p['status'] else ''
    facts = ''.join(f'<div><strong>{v}</strong><span>{k}</span></div>' for v, k in p['facts'])
    feats = ''.join(f'<li class="reveal"><span class="i">{i:02d}</span><h3>{t}</h3><p>{d}</p></li>'
                    for i, (t, d) in enumerate(p['features'], 1))
    steps = ''.join(f'<li><span>Step {i}</span><p>{s}</p></li>' for i, s in enumerate(p['steps'], 1))
    uses = ''.join(f'<li>{u}</li>' for u in p['use_cases'])
    bens = ''.join(f'<li>{b}</li>' for b in p['benefits'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq'])
    privacy = f'<div class="pd-panel"><h3>Data &amp; privacy</h3><p>{p["privacy"]}</p></div>' if p['privacy'] else ''
    others = ''.join(
        f'<a class="pd-other hud" href="{o["slug"]}.html">{logo_tile(o, "pd-other-logo")}'
        f'<span><small>{o["category"]}</small><b>{o["name"]}</b></span><span class="arr">&rarr;</span></a>'
        for o in PRODUCTS if o is not p)
    counter = iter(range(1, 20))
    n = lambda: f'{next(counter):02d}'
    gallery = ''.join(
        fn(p, n) for key, fn in (('gallery', gallery_section), ('tabs', tabs_section), ('photos', photos_section)) if p.get(key))
    title = f'{name} | {plain(p["category"])} | Anqah Tech'
    desc = plain(p['statement'])
    url = f'{SITE}/products/{p["slug"]}.html'
    image = f'{SITE}/{p["logo"]}' if p['logo'] else f'{SITE}/images/logo-full-navy.png'
    ld_type = 'SoftwareApplication' if p['slug'].startswith('sello') else 'Product'

    return f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Generated by tools/build_product_pages.py - edit the data there, not this file. -->
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(desc)}">
    <meta name="theme-color" content="#07080a">
    <link rel="canonical" href="{url}">
    <link rel="icon" type="image/png" href="../images/favicon.png">
    <meta property="og:type" content="product">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:image" content="{image}">
    <script type="application/ld+json">
    {{ "@context": "https://schema.org", "@type": "{ld_type}", "name": "{name}", "description": "{escape(desc)}",
       "brand": {{ "@type": "Organization", "name": "Anqah Tech Pvt Limited" }}, "url": "{url}", "image": "{image}" }}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css">
    <script type="importmap">
    {{ "imports": {{ "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js" }} }}
    </script>
</head>

<body class="pd-page">
{header()}

    <main>
        <section class="pd-hero">
            <div class="pd-copy">
                <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a><span>/</span><a href="../index.html#products">Products</a><span>/</span><b>{name}</b></nav>
                <div class="pd-id">
                    {logo_tile(p)}
                    <div><span class="tag">{p["category"]}</span>{status}</div>
                </div>
                <h1>{name}</h1>
                <p class="lead">{p["statement"]}</p>
                <div class="hero-actions">
                    <a href="{enquire}" target="_blank" rel="noopener" class="btn btn-accent">Enquire on WhatsApp <span class="arr">&rarr;</span></a>
                    <a href="tel:{PHONE}" class="btn btn-line">Call us</a>
                </div>
                <div class="terminal pd-term">
                    <div class="term-bar"><i></i><i></i><i></i><span>anqah@tech:~/{p["slug"]}</span></div>
                    <code><span class="prompt">$</span> <span id="typed" data-commands="{escape(p["terminal"])}"></span><span class="caret"></span></code>
                </div>
            </div>
            <figure class="pd-stage hero-frame hud">
                <span class="corner tl">{p["slug"].upper()}</span>
                <span class="corner tr">3D // LIVE</span>
                <canvas data-scene="{p["scene"]}" aria-label="Interactive 3D model of {name}"></canvas>
                <figcaption>[ hover to interact ]</figcaption>
            </figure>
        </section>

        <section class="facts" aria-label="Key facts">{facts}</section>
{gallery}
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>Why {name}</h2></div></header>
            <div class="pd-two reveal">
                <div class="pd-panel"><h3>The problem</h3><p>{p["problem"]}</p></div>
                <div class="pd-panel accent"><h3>Our solution</h3><p>{p["solution"]}</p></div>
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>Key features</h2></div></header>
            <ol class="svc-list">{feats}</ol>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>How it works</h2></div></header>
            <ol class="process pd-steps reveal">{steps}</ol>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>Built for</h2></div></header>
            <div class="pd-two reveal">
                <div class="pd-panel"><h3>Use cases</h3><ul class="pd-list">{uses}</ul></div>
                <div class="pd-panel"><h3>Benefits</h3><ul class="pd-list">{bens}</ul></div>
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>Under the hood</h2></div></header>
            <div class="pd-two reveal">
                <div class="pd-panel"><h3>Technical overview</h3><p>{p["tech"]}</p></div>
                {privacy}
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>FAQ</h2></div></header>
            <div class="faq reveal">{faq}</div>
        </section>

        <section class="section">
            <div class="pd-cta hud reveal">
                <div>
                    <span class="tag">Get {name}</span>
                    <h2>Interested in {name}?</h2>
                    <p>Tell us about your business &mdash; we&rsquo;ll get back to you within 24 hours.</p>
                </div>
                <div class="hero-actions">
                    <a href="{enquire}" target="_blank" rel="noopener" class="btn btn-accent">Enquire on WhatsApp <span class="arr">&rarr;</span></a>
                    <a href="../index.html#contact" class="btn btn-line">Contact form</a>
                </div>
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>Other products</h2></div></header>
            <div class="pd-others reveal">{others}</div>
        </section>
    </main>

{footer()}

    <a class="fab-wa" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">
        {WA_ICON}
    </a>

    <script src="../script.js"></script>
    <script type="module" src="../three-scenes.js"></script>
</body>

</html>
'''


def main():
    out = ROOT / 'products'
    out.mkdir(exist_ok=True)
    for p in PRODUCTS:
        (out / f'{p["slug"]}.html').write_text(page(p), encoding='utf-8')
        print('wrote', f'products/{p["slug"]}.html')


if __name__ == '__main__':
    main()
