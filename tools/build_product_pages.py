"""Generates the static product detail pages in /products from the data below.

Edit a product's content here, then run:  python tools/build_product_pages.py
"""
import json
import re
from html import escape, unescape
from pathlib import Path
from urllib.parse import quote

from product_content_ar import AR, UI

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.anqah.com'
WHATSAPP = '971505762100'
PHONE = '+971502393703'

PRODUCTS = [
    {
        'slug': 'sello',
        'seo': {
            'title': 'SELLO POS System &amp; POS Machines for Retail &amp; Restaurants | UAE, KSA, India',
            'description': 'Complete POS systems for shops, restaurants &amp; cafés in UAE, Saudi Arabia &amp; India: POS machines, printers and cash drawers with SELLO software &mdash; billing, inventory, kitchen display and VAT/GST.',
            'keywords': 'POS software UAE, POS system Saudi Arabia, POS software India, POS machine Abu Dhabi, POS machine Dubai, POS hardware UAE, receipt printer, cash drawer, touch POS terminal, restaurant POS, retail POS, billing software, inventory software, kitchen display system, offline POS, SELLO',
            'og': 'og-sello.jpg', 'app': ('BusinessApplication', 'Windows, Web'),
        },
        'name': 'SELLO',
        'brochure': ('Anqah-SELLO-Brochure.pdf', '1.8 MB'),
        'hardware': {
            'items': [
                ('terminal.jpg', 'Dual-screen POS terminal', 'All-in-one touch terminal with a customer-facing display.'),
                ('printer.jpg', 'Receipt printer', 'Fast thermal printing for receipts and kitchen tickets.'),
                ('tablet.jpg', 'Tablet POS', 'Compact counter or table-side billing on a secure stand.'),
                ('kds.jpg', 'Kitchen display', 'A screen at the kitchen pass, so orders never get lost.'),
                ('drawer.jpg', 'Cash drawer', 'Opens automatically on cash sales and keeps takings secure.'),
                ('monitor.jpg', 'Touch-screen POS monitor', 'Large touch screen for busy counters and the back office.'),
            ],
            'includes': ['POS hardware', 'SELLO software', 'Installation &amp; setup', 'Product &amp; VAT/GST setup',
                         'Staff training', 'Support &amp; AMC'],
        },
        'category': 'POS All-in-One Solution',
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
            ('Do you sell POS hardware?', 'Yes. We supply complete POS systems &mdash; POS terminals, tablets, receipt printers, cash drawers and kitchen displays &mdash; with SELLO installed, set up and supported.'),
        ],
    },
    {
        'slug': 'sello-lite',
        'seo': {
            'title': 'SELLO Lite Offline Mobile POS App | UAE, KSA, India',
            'description': 'Offline mobile POS app for restaurants, cafés &amp; small shops in UAE, Saudi Arabia &amp; India: billing, portions, split payments, taxes and reports. Arabic &amp; English.',
            'keywords': 'mobile POS app, offline POS app, POS app UAE, POS app Saudi Arabia, billing app India, restaurant billing app, Arabic POS app, Android POS, SELLO Lite',
            'og': 'og-sello-lite.jpg', 'app': ('BusinessApplication', 'Android'),
        },
        'name': 'SELLO Lite',
        'brochure': ('Anqah-SELLO-Lite-Brochure.pdf', '1.1 MB'),
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
        'seo': {
            'title': 'Automatic School Bell System with App | UAE, KSA, India',
            'description': 'Automatic bell with mobile app for schools, colleges, hostels &amp; factories: rings on a timetable, skips holidays, manual ring. UAE, Saudi Arabia &amp; India.',
            'keywords': 'automatic school bell, school bell system UAE, automatic bell Saudi Arabia, school bell timer India, college bell system, hostel bell timer, madrasa bell, WiFi bell controller, bell scheduler app, factory bell system',
            'og': 'og-automatic-bell.jpg', 'app': None,
        },
        'name': 'Automatic Bell',
        'brochure': ('Anqah-Automatic-Bell-Brochure.pdf', '1.0 MB'),
        'audience': ['Schools', 'Colleges', 'Hostels', 'Madrasas', 'Training centres', 'Factories', 'Offices'],
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
        'seo': {
            'title': 'Water Tank Level Monitoring &amp; Alerts | UAE, KSA, India',
            'description': 'Live water tank level on your phone plus Telegram alerts below 15% (empty) and above 95% (overflow). For homes &amp; businesses in UAE, Saudi Arabia &amp; India.',
            'keywords': 'water tank level monitoring, water level sensor, tank overflow alarm, water tank monitoring UAE, water level indicator Saudi Arabia, water level controller India, Telegram alerts IoT',
            'og': 'og-water-monitoring.jpg', 'app': None,
        },
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
WA_ICON = re.search(r'class="fab-wa".*?(<svg.*?</svg>)', (ROOT / 'index.html').read_text(encoding='utf-8'), re.S).group(1)


def text_only(html):
    """HTML snippet -> plain text for structured data."""
    return unescape(re.sub(r'<[^>]+>', '', html))


def localize(p, lang):
    """Product data in the requested language (Arabic overrides English, field by field)."""
    if lang == 'en':
        return p
    ar = AR[p['slug']]
    out = {**p, **{k: v for k, v in ar.items() if k != 'seo'}}
    out['seo'] = {**p['seo'], **ar['seo']}
    return out


def page_url(slug, lang):
    return f'{SITE}/{"ar/" if lang == "ar" else ""}products/{slug}.html'


def structured_data(p, lang, url, image):
    t = UI[lang]
    org = {'@type': 'Organization', '@id': f'{SITE}/#org', 'name': 'Anqah Tech', 'url': f'{SITE}/'}
    home = f'{SITE}/{"ar/" if lang == "ar" else ""}'
    images = [image] + [f'{SITE}/images/products/{p["slug"]}/{g[0].replace(".webp", "-device.webp")}' for g in p.get('gallery', [])[:3]]
    item = {
        '@id': f'{url}#product', 'name': p['name'], 'url': url, 'image': images, 'inLanguage': lang,
        'description': text_only(p['seo']['description']), 'brand': org,
        'category': text_only(p['category']),
    }
    if p['seo']['app']:
        item.update({'@type': 'SoftwareApplication', 'applicationCategory': p['seo']['app'][0],
                     'operatingSystem': p['seo']['app'][1], 'publisher': org})
    else:
        # Devices we supply, install and support. Marked up as a Service, not a Product: Google's Product rich
        # results need a price (offers) or reviews, which we don't publish, and would flag the page as invalid.
        item.pop('inLanguage')
        item.update({'@type': 'Service', 'serviceType': text_only(p['category']), 'provider': org,
                     'areaServed': [{'@type': 'Country', 'name': c} for c in ('United Arab Emirates', 'Saudi Arabia', 'India')]})
    graph = [
        item,
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': t['home'], 'item': home},
            {'@type': 'ListItem', 'position': 2, 'name': t['products'], 'item': f'{home}#products'},
            {'@type': 'ListItem', 'position': 3, 'name': p['name'], 'item': url},
        ]},
        {'@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': [
            {'@type': 'Question', 'name': text_only(q), 'acceptedAnswer': {'@type': 'Answer', 'text': text_only(a)}}
            for q, a in p['faq']]},
    ]
    return {'@context': 'https://schema.org', '@graph': graph}


def wa_link(text):
    return f'https://wa.me/{WHATSAPP}?text={quote(text)}'


def header(lang, root, switch_href, active='#products'):
    t = UI[lang]
    current = ' aria-current="page"'
    nav = ''.join(f'<li><a href="{h if h[0] != "#" else "../index.html" + h}"{current if h == active else ""}>{label}</a></li>'
                  for h, label in t['nav'])
    sw_label, sw_lang = t['switch']
    return f'''    <div class="scanlines" aria-hidden="true"></div>
    <header id="header">
        <div class="statusbar" aria-hidden="true">
            <span><i class="led"></i> SYS.ONLINE</span>
            <span class="sb-hide">NODE: ABU DHABI // 24.45&deg;N 54.38&deg;E</span>
            <span class="sb-hide">BUILD 2026.10</span>
            <span>GST <b id="clock">--:--:--</b></span>
        </div>
        <nav class="navbar">
            <a href="../index.html" class="logo" aria-label="{t['home_label']}">
                <img src="{root}images/logo-mark-white.png" alt="{t['logo_alt']}" width="48" height="35">
                <span class="logo-text"><span><b>Anqah</b> Tech</span></span>
            </a>
            <ul class="nav-links" id="navLinks">
                {nav}
                <li><a class="lang-switch" href="{switch_href}" hreflang="{sw_lang}" lang="{sw_lang}">{sw_label}</a></li>
            </ul>
            <a href="../index.html#contact" class="btn btn-accent nav-cta">{t['talk']} <span class="arr">&rarr;</span></a>
            <button class="menu-toggle" id="menuToggle" aria-label="{t['menu']}" aria-expanded="false">
                <span></span><span></span>
            </button>
        </nav>
    </header>'''


def footer(lang, root, switch_href, product_dir=''):
    t = UI[lang]
    links = ''.join(f'<a href="{product_dir}{p["slug"]}.html">{localize(p, lang)["name"]}</a>' for p in PRODUCTS)
    from service_content import SERVICES as _SV, UI as _SUI  # noqa: E402 (service pages share this footer)
    names = {x['slug']: x[lang]['name'] for x in _SV}
    services = ''.join(f'<a href="../services/{k}.html">{names[k]}</a>' for k in
                       ('web-development', 'mobile-app-development', 'pos-systems', 'cctv-installation', 'home-automation', 'it-solutions'))
    services += f'<a href="../services/pos-machines.html">{_SUI[lang]["hw_link"]}</a>'
    sw_label, sw_lang = t['switch']
    return f'''    <footer>
        <div class="footer-top">
            <p class="footer-big">{t['smart']}</p>
            <a href="../index.html#contact" class="btn btn-accent">{t['start']} <span class="arr">&rarr;</span></a>
        </div>
        <div class="footer-grid">
            <div>
                <a href="../index.html" class="logo"><img src="{root}images/logo-mark-white.png" alt="" width="48" height="35"><span class="logo-text"><span><b>Anqah</b> Tech</span></span></a>
            </div>
            <div>
                <h4>{t['products']}</h4>
                {links}
            </div>
            <div>
                <h4>{t['services']}</h4>
                {services}<a href="../blog/">{t['guides']}</a>
            </div>
            <div>
                <h4>{t['contact']}</h4>
                <a href="tel:{PHONE}" dir="ltr">+971 50 239 3703</a><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{t['whatsapp']}</a><a href="mailto:anqahgroups@gmail.com">anqahgroups@gmail.com</a><span>{t['city']}</span><a href="{root}downloads/Anqah-Tech-Company-Profile{"-AR" if lang == "ar" else ""}.pdf" download>{t['profile']}</a>
            </div>
        </div>
        <div class="footer-bottom">
            <span>&copy; <span id="year">2026</span> {t['rights']}</span>
            <a class="lang-switch" href="{switch_href}" hreflang="{sw_lang}" lang="{sw_lang}">{sw_label}</a>
        </div>
    </footer>'''


def logo_tile(p, root, lang, cls='pd-logo'):
    if p['logo']:
        return f'<img class="{cls}" src="{root}{p["logo"]}" alt="{UI[lang]["logo_word"].format(name=p["name"])}" width="72" height="72">'
    en_name = next(x['name'] for x in PRODUCTS if x['slug'] == p['slug'])  # initials always from the Latin name
    initials = ''.join(w[0] for w in en_name.split()[:2]).upper()
    return f'<span class="{cls} pd-logo-mono" aria-hidden="true">{initials}</span>'


def tabs_section(p, n, lang, root):
    t = UI[lang]
    folder = f'{root}images/products/{p["slug"]}'
    sid = f'{p["slug"]}-tabs'
    tabs = ''.join(
        f'<button class="tab" role="tab" id="{sid}-t{i}" aria-controls="{sid}-p{i}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
        f'<span class="tab-i">{i + 1:02d}</span>{label}</button>'
        for i, (label, *_rest) in enumerate(p['tabs']))
    panels = ''.join(
        f'<div class="tab-panel" role="tabpanel" id="{sid}-p{i}" aria-labelledby="{sid}-t{i}"{"" if i == 0 else " hidden"}>'
        f'<figure class="phone-frame"><img src="{folder}/{img}" alt="{t["tab_alt"].format(name=p["name"], label=label.replace("&amp;", "and").lower())}" width="738" height="1600" loading="{"eager" if i == 0 else "lazy"}"></figure>'
        f'<div class="tab-copy"><span class="tag">{label}</span><h3>{title}</h3><p>{text}</p>'
        f'<ul class="pd-list">{"".join(f"<li>{pt}</li>" for pt in points)}</ul></div></div>'
        for i, (label, img, title, text, points) in enumerate(p['tabs']))
    return f'''
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['tabs_h'].format(name=p["name"])}</h2><p>{t['tabs_p'].format(name=p["name"])}</p></div></header>
            <div class="tabs reveal" data-tabs>
                <div class="tab-list" role="tablist" aria-label="{t['tabs_label'].format(name=p["name"])}">{tabs}</div>
                <div class="tab-panels">{panels}</div>
            </div>
        </section>
'''


def photos_section(p, n, lang, root):
    t = UI[lang]
    folder = f'{root}images/products/{p["slug"]}'
    figs = ''.join(
        f'<figure class="photo reveal"><a href="{folder}/{f}" data-lightbox="{p["slug"]}" data-caption="{ti} &mdash; {c}">'
        f'<img src="{folder}/{f}" alt="{p["name"]}: {ti.lower()}" width="1408" height="768" loading="{"eager" if i == 0 else "lazy"}">'
        f'<span class="shot-zoom">{t["enlarge"]}</span></a><figcaption><b>{ti}</b>{c}</figcaption></figure>'
        for i, (f, ti, c) in enumerate(p['photos']))
    return f'''
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['photos_h'].format(name=p["name"])}</h2><p>{t['photos_p']}</p></div></header>
            <div class="photos">{figs}</div>
        </section>
'''


def gallery_section(p, n, lang, root):
    # Each screen is shown on a real POS terminal photo (`*-device.webp`); clicking opens the raw screenshot.
    t = UI[lang]
    folder = f'{root}images/products/{p["slug"]}'
    shots = ''.join(
        f'<figure class="shot reveal">'
        f'<a href="{folder}/{f}" data-lightbox="{p["slug"]}" data-caption="{ti} &mdash; {c}">'
        f'<img src="{folder}/{f.replace(".webp", "-device.webp")}" alt="{t["shot_alt"].format(name=p["name"], title=ti.lower())}" '
        f'width="1000" height="750" loading="{"eager" if i == 0 else "lazy"}">'
        f'<span class="shot-zoom">{t["view"]}</span>'
        f'</a><figcaption><b>{ti}</b>{c}</figcaption></figure>'
        for i, (f, ti, c, _url) in enumerate(p['gallery']))
    return f'''
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['gallery_h'].format(name=p["name"])}</h2><p>{t['gallery_p'].format(name=p["name"])}</p></div></header>
            <div class="gallery">{shots}</div>
            <p class="credit">{t['credit']}</p>
        </section>
'''


def hardware_section(p, n, lang, root):
    t = UI[lang]
    hw = p['hardware']
    folder = f'{root}images/products/pos-hardware'
    figs = ''.join(
        f'<figure class="shot reveal"><img src="{folder}/{f}" alt="{ti}" width="800" height="600" loading="lazy">'
        f'<figcaption><b>{ti}</b>{c}</figcaption></figure>'
        for f, ti, c in hw['items'])
    incl = ''.join(f'<li>{i}</li>' for i in hw['includes'])
    return f'''
        <section class="section" id="hardware">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['hw_h']}</h2><p>{t['hw_p']}</p></div></header>
            <div class="gallery hw-gallery">{figs}</div>
            <div class="hw-incl hud reveal"><span class="tag">{t['hw_incl']}</span><ul>{incl}</ul>
                <a href="{wa_link(unescape(t['hw_wa']))}" target="_blank" rel="noopener" class="btn btn-accent">{t['hw_quote']} <span class="arr">&rarr;</span></a></div>
        </section>
'''


def page(base, lang):
    p = localize(base, lang)
    t = UI[lang]
    root = '../../' if lang == 'ar' else '../'
    name = p['name']
    url = page_url(p['slug'], lang)
    en_url, ar_url = page_url(p['slug'], 'en'), page_url(p['slug'], 'ar')
    switch_href = f'../../products/{p["slug"]}.html' if lang == 'ar' else f'../ar/products/{p["slug"]}.html'
    enquire = wa_link(unescape(t['wa_msg'].format(name=name)))
    status = f'<span class="pd-status">{p["status"]}</span>' if p['status'] else ''
    brochure_file = p['brochure'][0].replace('.pdf', '-AR.pdf') if lang == 'ar' and p.get('brochure') else (p.get('brochure') or ('',))[0]
    brochure = (f'<a href="{root}downloads/brochures/{brochure_file}" download class="btn btn-line btn-dl">'
                f'{t["brochure"]} <small>PDF &middot; {p["brochure"][1]}</small></a>') if p.get('brochure') else ''
    audience = (f'<ul class="for-chips" aria-label="{t["for"]}"><li class="for-label">{t["for"]}</li>'
                + ''.join(f'<li>{a}</li>' for a in p['audience']) + '</ul>') if p.get('audience') else ''
    facts = ''.join(f'<div><strong>{v}</strong><span>{k}</span></div>' for v, k in p['facts'])
    feats = ''.join(f'<li class="reveal"><span class="i">{i:02d}</span><h3>{ti}</h3><p>{d}</p></li>'
                    for i, (ti, d) in enumerate(p['features'], 1))
    steps = ''.join(f'<li><span>{t["step"].format(i=i)}</span><p>{s}</p></li>' for i, s in enumerate(p['steps'], 1))
    uses = ''.join(f'<li>{u}</li>' for u in p['use_cases'])
    bens = ''.join(f'<li>{b}</li>' for b in p['benefits'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in p['faq'])
    privacy = f'<div class="pd-panel"><h3>{t["privacy"]}</h3><p>{p["privacy"]}</p></div>' if p['privacy'] else ''
    others = ''.join(
        f'<a class="pd-other hud" href="{o["slug"]}.html">{logo_tile(o, root, lang, "pd-other-logo")}'
        f'<span><small>{o["category"]}</small><b>{o["name"]}</b></span><span class="arr">&rarr;</span></a>'
        for o in (localize(x, lang) for x in PRODUCTS) if o['slug'] != p['slug'])
    counter = iter(range(1, 20))
    n = lambda: f'{next(counter):02d}'
    gallery = ''.join(
        fn(p, n, lang, root) for key, fn in (('gallery', gallery_section), ('hardware', hardware_section), ('tabs', tabs_section), ('photos', photos_section)) if p.get(key))
    seo = p['seo']
    title = unescape(seo['title'])
    desc = seo['description']
    image = f'{SITE}/images/og/{seo["og"]}'
    ld = json.dumps(structured_data(p, lang, url, image), ensure_ascii=False, indent=2)
    hreflang = '\n'.join(
        [f'    <link rel="alternate" hreflang="{h}" href="{en_url}">' for h in ('en', 'en-AE', 'en-SA', 'en-IN')] +
        [f'    <link rel="alternate" hreflang="{h}" href="{ar_url}">' for h in ('ar', 'ar-AE', 'ar-SA')] +
        [f'    <link rel="alternate" hreflang="x-default" href="{en_url}">'])
    fonts = ('family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600'
             + ('&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;700;800' if lang == 'ar' else '')
             + '&family=JetBrains+Mono:wght@400;500;700&display=swap')
    locale = 'ar_AE' if lang == 'ar' else 'en_AE'
    alt_locale = 'en_AE' if lang == 'ar' else 'ar_AE'

    return f'''<!DOCTYPE html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Generated by tools/build_product_pages.py - edit the data there, not this file. -->
    <title>{escape(title)}</title>
    <meta name="description" content="{escape(desc)}">
    <meta name="keywords" content="{escape(seo['keywords'])}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <meta name="theme-color" content="#07080a">
    <link rel="canonical" href="{url}">
{hreflang}
    <meta name="geo.region" content="AE-AZ">
    <meta name="geo.placename" content="Abu Dhabi">
    <link rel="icon" href="{root}favicon.ico" sizes="48x48">
    <link rel="icon" type="image/png" sizes="48x48" href="{root}images/favicon-48.png">
    <link rel="icon" type="image/png" sizes="192x192" href="{root}images/favicon.png">
    <link rel="apple-touch-icon" href="{root}images/apple-touch-icon.png">
    <link rel="manifest" href="{root}site.webmanifest">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="Anqah Tech">
    <meta property="og:url" content="{url}">
    <meta property="og:title" content="{escape(title)}">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:image" content="{image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:locale" content="{locale}">
    <meta property="og:locale:alternate" content="{alt_locale}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(title)}">
    <meta name="twitter:description" content="{escape(desc)}">
    <meta name="twitter:image" content="{image}">
    <script type="application/ld+json">
{ld}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?{fonts}" rel="stylesheet">
    <link rel="stylesheet" href="{root}style.css">
    <script type="importmap">
    {{ "imports": {{ "three": "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js" }} }}
    </script>
</head>

<body class="pd-page">
{header(lang, root, switch_href)}

    <main>
        <section class="pd-hero">
            <div class="pd-copy">
                <nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">{t['home']}</a><span>/</span><a href="../index.html#products">{t['products']}</a><span>/</span><b>{name}</b></nav>
                <div class="pd-id">
                    {logo_tile(p, root, lang)}
                    <div><span class="tag">{p["category"]}</span>{status}</div>
                </div>
                <h1>{name}</h1>
                <p class="lead">{p["statement"]}</p>
                {audience}
                <div class="hero-actions">
                    <a href="{enquire}" target="_blank" rel="noopener" class="btn btn-accent">{t['enquire']} <span class="arr">&rarr;</span></a>
                    <a href="tel:{PHONE}" class="btn btn-line">{t['call']}</a>
                    {brochure}
                </div>
                <div class="terminal pd-term" dir="ltr">
                    <div class="term-bar"><i></i><i></i><i></i><span>anqah@tech:~/{p["slug"]}</span></div>
                    <code><span class="prompt">$</span> <span id="typed" data-commands="{escape(p["terminal"])}"></span><span class="caret"></span></code>
                </div>
            </div>
            <figure class="pd-stage hero-frame hud">
                <span class="corner tl">{p["slug"].upper()}</span>
                <span class="corner tr">3D // LIVE</span>
                <canvas data-scene="{p["scene"]}" aria-label="{t['model'].format(name=name)}"></canvas>
                <figcaption>{t['hover']}</figcaption>
            </figure>
        </section>

        <section class="facts" aria-label="{t['facts']}">{facts}</section>
{gallery}
        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['why'].format(name=name)}</h2></div></header>
            <div class="pd-two reveal">
                <div class="pd-panel"><h3>{t['problem']}</h3><p>{p["problem"]}</p></div>
                <div class="pd-panel accent"><h3>{t['solution']}</h3><p>{p["solution"]}</p></div>
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['features']}</h2></div></header>
            <ol class="svc-list">{feats}</ol>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['how']}</h2></div></header>
            <ol class="process pd-steps reveal">{steps}</ol>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['built']}</h2></div></header>
            <div class="pd-two reveal">
                <div class="pd-panel"><h3>{t['uses']}</h3><ul class="pd-list">{uses}</ul></div>
                <div class="pd-panel"><h3>{t['benefits']}</h3><ul class="pd-list">{bens}</ul></div>
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['hood']}</h2></div></header>
            <div class="pd-two reveal">
                <div class="pd-panel"><h3>{t['tech']}</h3><p>{p["tech"]}</p></div>
                {privacy}
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['faq']}</h2></div></header>
            <div class="faq reveal">{faq}</div>
        </section>

        <section class="section">
            <div class="pd-cta hud reveal">
                <div>
                    <span class="tag">{t['get'].format(name=name)}</span>
                    <h2>{t['interested'].format(name=name)}</h2>
                    <p>{t['tell']}</p>
                </div>
                <div class="hero-actions">
                    <a href="{enquire}" target="_blank" rel="noopener" class="btn btn-accent">{t['enquire']} <span class="arr">&rarr;</span></a>
                    <a href="../index.html#contact" class="btn btn-line">{t['form']}</a>
                    {brochure}
                </div>
            </div>
        </section>

        <section class="section">
            <header class="sec-head reveal"><span class="num">// {n()}</span><div><h2>{t['others']}</h2></div></header>
            <div class="pd-others reveal">{others}</div>
        </section>
    </main>

{footer(lang, root, switch_href)}

    <a class="fab-pdf" href="{root}downloads/Anqah-Tech-Company-Profile{"-AR" if lang == "ar" else ""}.pdf" download aria-label="{t['profile_dl']}" title="{t['profile_dl']}">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M12 11v6m0 0-3-3m3 3 3-3"/></svg>
    </a>
    <a class="fab-wa" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="{t['chat']}">
        {WA_ICON}
    </a>

    <script src="{root}script.js"></script>
    <script type="module" src="{root}three-scenes.js"></script>
</body>

</html>
'''


def main():
    for lang, folder in (('en', ROOT / 'products'), ('ar', ROOT / 'ar' / 'products')):
        folder.mkdir(parents=True, exist_ok=True)
        for p in PRODUCTS:
            (folder / f'{p["slug"]}.html').write_text(page(p, lang), encoding='utf-8')
            print('wrote', (folder / f'{p["slug"]}.html').relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
