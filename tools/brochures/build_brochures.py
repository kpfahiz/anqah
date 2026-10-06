"""Builds one A4 brochure per product, in English and Arabic (<slug>-ar.html), as HTML in tools/brochures/, using the product data in build_product_pages.py
and real screenshots / photos only. Print them to PDF with:  node tools/brochures/print_brochures.mjs
    python tools/brochures/build_brochures.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from build_product_pages import PRODUCTS, localize  # noqa: E402
sys.path.insert(0, str(HERE.parent / 'profile'))
from build_profile_ar import RTL_CSS  # noqa: E402

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


LANG = 'en'


def tr(en, ar):
    """Pick the string for the brochure language being built."""
    return ar if LANG == 'ar' else en


def prod(slug):
    return localize(P[slug], LANG)


def foot(name, n):
    return f'<div class="foot"><span><b>ANQAH TECH</b> &middot; {name} {tr("BROCHURE", "&middot; كتيّب المنتج")}</span><span>{n:02d}</span></div>'


def page(body, n, name, geo='tr', extra_cls=''):
    if LANG == 'ar':  # mirror the corner shapes for right-to-left pages
        geo = {'tr': 'tl', 'tl': 'tr', 'trbl': 'tlbr', 'trbr': 'tlbl'}[geo]
    shapes = {
        'tr': '<div class="geo tr-navy"></div><div class="geo tr-lime"></div>',
        'tl': '<div class="geo tl-navy"></div><div class="geo tl-lime"></div>',
        'trbl': '<div class="geo tr-navy"></div><div class="geo tr-lime"></div><div class="geo bl-navy"></div><div class="geo bl-lime"></div>',
        'trbr': '<div class="geo tr-navy"></div><div class="geo tr-lime"></div><div class="geo br-navy"></div><div class="geo br-lime"></div>',
        'tlbr': '<div class="geo tl-navy"></div><div class="geo tl-lime"></div><div class="geo br-navy"></div><div class="geo br-lime"></div>',
        'tlbl': '<div class="geo tl-navy"></div><div class="geo tl-lime"></div><div class="geo bl-navy"></div><div class="geo bl-lime"></div>',
    }[geo]
    # keep the heading clear of a corner shape on the side where the text starts
    pad = ''
    if LANG == 'en' and geo.startswith('tl'):
        pad = ' style="margin-left:26mm"'
    if LANG == 'ar' and geo.startswith('tr'):
        pad = ' style="margin-right:26mm"'
    body = body.replace('<div class="kicker">', f'<div class="kicker"{pad}>', 1).replace('<h2>', f'<h2{pad}>', 1)
    return f'''
<section class="page {extra_cls}">
    {shapes}
    <div class="inner tight">{body}
    </div>
    {foot(name.upper() if LANG == 'en' else name, n)}
</section>'''


def cover(p, kicker, title_html, visual, logo=None):
    facts = ''.join(f'<div><b>{v}</b><span>{k}</span></div>' for v, k in p['facts'])
    logo_html = f'<img class="logo-tile" src="../../{logo}" alt="">' if logo else ''
    cat = p['category'].upper() if LANG == 'en' else p['category']
    return f'''
<section class="page cover">
    <div class="brand"><img src="../../images/logo-mark-white.png" alt=""><span>Anqah Tech</span></div>
    <div class="status"><i></i>{tr('PRODUCT BROCHURE', 'كتيّب المنتج')}<br>{cat}</div>
    {logo_html}
    <div class="title">
        <div class="kicker">{kicker}</div>
        <h1>{title_html}</h1>
        <p>{p['statement']}</p>
    </div>
    {visual}
    <div class="facts">{facts}</div>
    <div class="web"><span><b>www.anqah.com</b></span><span class="ltr">+971 50 239 3703 &middot; anqahgroups@gmail.com</span></div>
</section>'''


def overview(p, n, kicker, image_html):
    uses = ''.join(f'<li>{u}</li>' for u in p['use_cases'])
    bens = ''.join(f'<li>{b}</li>' for b in p['benefits'])
    return page(f'''
        <div class="kicker">{kicker}</div>
        <h2>{tr(f"Why <em>{p['name']}?</em>", f"لماذا <em>{p['name']}؟</em>")}</h2>
        <div class="two">
            <div class="panel"><h3>{tr('The challenge', 'التحدي')}</h3><p>{p['problem']}</p></div>
            <div class="panel lime"><h3>{tr(f"The {p['name']} solution", f"الحل مع {p['name']}")}</h3><p>{p['solution']}</p></div>
        </div>
        <div class="two mt">
            <div><h3 class="sub2" style="margin-top:0">{tr('Built for', 'مصمم من أجل')}</h3><ul class="ticks">{uses}</ul></div>
            <div><h3 class="sub2" style="margin-top:0">{tr('What you get', 'ما الذي تحصل عليه')}</h3><ul class="ticks">{bens}</ul></div>
        </div>
        {image_html}''', n, p['name'])


def features_page(p, n, kicker, cols='', extra=''):
    feats = ''.join(f'<div data-n="{i:02d}"><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(p['features'], 1))
    steps = ''.join(f'<li>{s}</li>' for s in p['steps'])
    return page(f'''
        <div class="kicker">{kicker}</div>
        <h2>{tr('Key <em>features</em>', 'أهم <em>المزايا</em>')}</h2>
        <div class="fgrid {cols}">{feats}</div>
        <h3 class="sub2">{tr('How it works', 'كيف يعمل')}</h3>
        <ol class="flow">{steps}</ol>
        {extra}''', n, p['name'], geo='trbl')


def closing(p, n):
    faq = ''.join(f'<div><h3>{q}</h3><p>{a}</p></div>' for q, a in p['faq'])
    privacy = f'<div class="panel lime mt-s"><h3>{tr("Your data", "بياناتك")}</h3><p>{p["privacy"]}</p></div>' if p.get('privacy') else ''
    return page(f'''
        <div class="kicker">{tr('Technical details', 'التفاصيل التقنية')}</div>
        <h2>{tr('Under <em>the hood</em>', 'من <em>الداخل</em>')}</h2>
        <div class="techbox"><span class="kicker">{tr('Technology', 'التقنية')}</span><p>{p['tech']}</p></div>
        {privacy}
        <h3 class="sub2">{tr('Frequently asked questions', 'الأسئلة الشائعة')}</h3>
        <div class="faq-list">{faq}</div>
        <div class="cta-strip">
            <div><h3>{tr(f"Get {p['name']} for your business", f"احصل على {p['name']} لعملك")}</h3><p>{tr('Talk to us for a demo, pricing and installation &mdash; we reply within 24 hours.', 'تواصل معنا لعرض توضيحي والأسعار والتركيب &mdash; نردّ خلال 24 ساعة.')}</p></div>
            <div class="contacts"><b>{tr('Phone', 'الهاتف')}</b> <span class="ltr">+971 50 239 3703</span><br><b>{tr('WhatsApp', 'واتساب')}</b> <span class="ltr">+971 50 576 2100</span><br><b>{tr('Email', 'البريد')}</b> <span class="ltr">anqahgroups@gmail.com</span><br><b>{tr('Web', 'الموقع')}</b> <span class="ltr">www.anqah.com</span></div>
        </div>''', n, p['name'], geo='trbr')


RTL_EXTRA = '''
/* ---------- brochure: right-to-left ---------- */
.cover .logo-tile { left: auto; right: 18mm; }
ul.ticks li { padding-left: 0; padding-right: 6mm; }
ul.ticks li::before { left: auto; right: 0; }
.hwgrid figcaption { border-left: 0; border-right: 0.8mm solid var(--lime); padding-left: 0; padding-right: 2.5mm; }
.callouts div { border-left: 0; border-right: 1mm solid var(--navy); }
.callouts div:nth-child(even) { border-color: var(--lime); }
.cap b { margin-right: 0; margin-left: 1.5mm; }
.cta-strip .contacts { text-align: left; }
.tour-row .tag, .fgrid div::before, .phones3 figcaption b, .phones4 figcaption b, .hwgrid figcaption b, .cap b,
.net .node b, .chips span, .cover .facts span { text-transform: none; letter-spacing: 0; }
.tour-row .tag, .chips span, .net .link { font-family: var(--body); }
.cover .facts b { font-family: 'Chakra Petch', var(--display); direction: ltr; unicode-bidi: isolate; text-align: right; }
.flow li::before { font-family: 'Chakra Petch', sans-serif; }
'''


def html_doc(title, body):
    css = CSS
    fonts = 'family=Chakra+Petch:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600'
    if LANG == 'ar':
        css += RTL_CSS.replace('</style>', '') + RTL_EXTRA
        fonts += '&family=IBM+Plex+Sans+Arabic:wght@400;500;600;700&family=Noto+Kufi+Arabic:wght@600;700;800'
    return f'''<!DOCTYPE html>
<html lang="{LANG}" dir="{'rtl' if LANG == 'ar' else 'ltr'}">
<head>
<meta charset="UTF-8">
<!-- GENERATED by tools/brochures/build_brochures.py - edit that file (and the product data), not this one. -->
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{fonts}&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>{body}
</body>
</html>
'''


# ---------------------------------------------------------------- SELLO
def sello():
    p = prod('sello')
    g = {f.replace('.webp', ''): (t, c) for f, t, c, _ in p['gallery']}
    pts = {
        'sello-pos': tr(['Photo grid by category, barcode and search', 'Live cart with VAT, discounts and notes', 'Hold orders and switch customers'],
                        ['شبكة صور حسب الفئة مع الباركود والبحث', 'سلة مباشرة مع الضريبة والخصومات والملاحظات', 'تعليق الطلبات والتبديل بين العملاء']),
        'sello-payment': tr(['Cash, card or split payments', 'Change calculated automatically', 'Print or share the receipt'],
                            ['نقدًا أو بالبطاقة أو دفع مجزّأ', 'حساب الباقي تلقائيًا', 'طباعة الإيصال أو مشاركته']),
        'sello-tables': tr(['Floors and tables with live status', 'Orders taken in rounds', 'Transfer, merge and split bills'],
                           ['الصالات والطاولات بحالتها المباشرة', 'الطلبات على دفعات', 'نقل الفواتير ودمجها وتقسيمها']),
        'sello-kitchen': tr(['New, Accepted, Preparing, Ready', 'Kitchen stations and modifiers', 'Replaces paper tickets'],
                            ['جديد، مقبول، قيد التحضير، جاهز', 'محطات المطبخ والإضافات', 'بديل التذاكر الورقية']),
        'sello-sales': tr(['Every invoice with payment method', 'Returns and exchanges in one click', 'Reprint and share receipts'],
                          ['كل فاتورة مع طريقة الدفع', 'المرتجعات والاستبدال بنقرة واحدة', 'إعادة طباعة الإيصالات ومشاركتها']),
        'sello-dashboard': tr(['POS, inventory, purchasing, kitchen', 'Reports, customers and settings', 'Role-based access for staff'],
                              ['البيع والمخزون والمشتريات والمطبخ', 'التقارير والعملاء والإعدادات', 'صلاحيات الموظفين حسب الدور']),
    }
    tag = tr('SELLO software', 'برنامج SELLO')

    def row(key, flip=False):
        t, c = g[key]
        ticks = ''.join(f'<li>{x}</li>' for x in pts[key])
        return (f'<div class="tour-row{" flip" if flip else ""}"><div class="screen"><img src="img/{key}.jpg" alt=""></div>'
                f'<div><span class="tag">{tag}</span><h3>{t}</h3><p>{c}</p><ul class="ticks">{ticks}</ul></div></div>')

    hw = ''.join(f'<figure><img src="../../images/products/pos-hardware/{f}" alt=""><figcaption><b>{t}</b>{c}</figcaption></figure>'
                 for f, t, c in p['hardware']['items'])
    incl = ''.join(f'<li>{i}</li>' for i in p['hardware']['includes'])
    pages = [
        cover(p, tr('POS All-in-One Solution', 'حل نقاط بيع متكامل'), tr('SELLO<span>POS system</span>', 'SELLO<span>نظام نقاط البيع</span>'),
              '<div class="visual"><img src="../profile/img/sello-pos-device.jpg" alt=""></div>', logo='images/products/sello-logo.png'),
        overview(p, 2, tr('01 &middot; Overview', '01 &middot; نظرة عامة'),
                 f'<figure class="figure-wide"><img src="../profile/img/sello-dashboard-device.jpg" alt="" style="object-position:center 40%"><figcaption class="cap"><b>{g["sello-dashboard"][0]}</b>{g["sello-dashboard"][1]}</figcaption></figure>'),
        page(f'''
        <div class="kicker">{tr('02 &middot; The software', '02 &middot; البرنامج')}</div>
        <h2>{tr('Inside <em>SELLO</em>', 'داخل <em>SELLO</em>')}</h2>
        <p class="lead" style="margin-bottom:6mm">{tr('Real screens from SELLO running a demo shop. Every till, tablet and kitchen screen opens SELLO in the browser over your shop network.', 'شاشات حقيقية من SELLO يعمل في متجر تجريبي. يفتح كل كاشير وجهاز لوحي وشاشة مطبخ برنامج SELLO في المتصفح عبر شبكة متجرك.')}</p>
        <div class="tour">{row('sello-pos')}{row('sello-payment', True)}{row('sello-tables')}</div>''', 3, p['name']),
        page(f'''
        <div class="kicker">{tr('02 &middot; The software', '02 &middot; البرنامج')}</div>
        <h2>{tr('Sales <em>&amp; kitchen</em>', 'المبيعات <em>والمطبخ</em>')}</h2>
        <div class="tour" style="margin-top:2mm">{row('sello-sales')}{row('sello-dashboard', True)}</div>
        <div class="tour-row mt" style="grid-template-columns: 52mm 1fr"><div class="screen"><img src="img/sello-kitchen.jpg" alt=""></div>
            <div><span class="tag">{tag}</span><h3>{g['sello-kitchen'][0]}</h3><p>{g['sello-kitchen'][1]}</p><ul class="ticks">{''.join(f'<li>{x}</li>' for x in pts['sello-kitchen'])}</ul></div></div>''', 4, p['name'], geo='tl'),
        features_page(p, 5, tr('03 &middot; Capabilities', '03 &middot; الإمكانات')),
        page(f'''
        <div class="kicker">{tr('04 &middot; The devices', '04 &middot; الأجهزة')}</div>
        <h2>{tr('POS <em>hardware</em>', 'أجهزة <em>نقاط البيع</em>')}</h2>
        <p class="lead" style="margin-bottom:5mm">{tr('We supply the POS machines, install SELLO, set up your products and taxes, and train your staff &mdash; hardware and software from one supplier.', 'نوفّر أجهزة الكاشير، ونثبّت SELLO، ونُعدّ منتجاتك وضرائبك، وندرّب موظفيك &mdash; الأجهزة والبرنامج من مورّد واحد.')}</p>
        <div class="hwgrid">{hw}</div>
        <h3 class="sub2">{tr('How the devices connect', 'كيف تتصل الأجهزة')}</h3>
        <div class="net">
            <div class="node hub"><b>{tr('Shop PC / server', 'حاسوب / خادم المتجر')}</b><span>{tr('Hosts SELLO and the database', 'يستضيف SELLO وقاعدة البيانات')}</span></div>
            <div class="link">{tr('&larr; shop LAN &rarr;<br>no internet needed', '&larr; شبكة المتجر &rarr;<br>دون حاجة للإنترنت')}</div>
            <div class="clients">
                <div class="node"><b>{tr('POS terminals', 'أجهزة الكاشير')}</b><span>{tr('Billing at the counter', 'الفوترة على الكاونتر')}</span></div>
                <div class="node"><b>{tr('Tablets', 'الأجهزة اللوحية')}</b><span>{tr('Table-side orders', 'الطلبات عند الطاولة')}</span></div>
                <div class="node"><b>{tr('Kitchen display', 'شاشة المطبخ')}</b><span>{tr('Live order tickets', 'تذاكر الطلبات مباشرة')}</span></div>
                <div class="node"><b>{tr('Printers &amp; drawer', 'الطابعات والدرج')}</b><span>{tr('Receipts and cash', 'الإيصالات والنقد')}</span></div>
            </div>
        </div>
        <div class="incl mt-s"><span class="kicker">{tr('Every POS package includes', 'تشمل كل باقة نقاط بيع')}</span><ul>{incl}</ul></div>''', 6, p['name'], geo='tl'),
        closing(p, 7),
    ]
    return html_doc(tr('SELLO - Product Brochure', 'SELLO - كتيّب المنتج'), ''.join(pages))


# ---------------------------------------------------------------- SELLO Lite
def sello_lite():
    p = prod('sello-lite')
    imgmap = {'sello-lite-sell.webp': 'lite-sell.jpg', 'sello-lite-portions.webp': 'lite-portions.jpg', 'sello-lite-pending.webp': 'lite-pending.jpg',
              'sello-lite-payments.webp': 'lite-payments.jpg', 'sello-lite-taxes.webp': 'lite-taxes.jpg', 'sello-lite-report.webp': 'lite-report.jpg'}
    phones = ''.join(f'<figure><div class="phone"><img src="img/{imgmap[img]}" alt=""></div><figcaption><b>{label}</b>{text}</figcaption></figure>'
                     for label, img, title, text, pts in p['tabs'])
    more = [('lite-product.jpg', tr('Products', 'المنتجات'), tr('Add products with a price, photo, category and stock tracking.', 'أضف المنتجات مع السعر والصورة والفئة وتتبّع المخزون.')),
            ('lite-more.jpg', tr('Settings', 'الإعدادات'), tr('Business details, taxes, receipts, payments, security and backup in one menu.', 'بيانات النشاط والضرائب والإيصالات والدفع والأمان والنسخ الاحتياطي في قائمة واحدة.')),
            ('lite-language.jpg', tr('Language &amp; currency', 'اللغة والعملة'), tr('English, Spanish, French, Arabic and Hindi, with local currencies including AED.', 'الإنجليزية والإسبانية والفرنسية والعربية والهندية، مع العملات المحلية ومنها الدرهم.')),
            ('lite-security.jpg', tr('Security', 'الأمان'), tr('Require unlock to open the app, with an auto-lock timer.', 'اطلب رمز فتح لتشغيل التطبيق، مع قفل تلقائي.'))]
    phones4 = ''.join(f'<figure><div class="phone"><img src="img/{f}" alt=""></div><figcaption><b>{t}</b>{c}</figcaption></figure>' for f, t, c in more)
    lic = tr('<div class="mt"><h3 class="sub2" style="margin-top:0">Licensing</h3><div class="two"><div class="panel"><h3>7-day free trial</h3><p>Every install starts with a full 7-day free trial &mdash; no card needed.</p></div><div class="panel lime"><h3>One-time activation</h3><p>An activation code tied to the device unlocks a 1, 2 or 5-year plan &mdash; no monthly subscription and no per-seat billing.</p></div></div></div>',
             '<div class="mt"><h3 class="sub2" style="margin-top:0">الترخيص</h3><div class="two"><div class="panel"><h3>تجربة مجانية 7 أيام</h3><p>يبدأ كل تثبيت بتجربة مجانية كاملة لمدة 7 أيام &mdash; دون بطاقة.</p></div><div class="panel lime"><h3>تفعيل لمرة واحدة</h3><p>رمز تفعيل مرتبط بالجهاز يفتح خطة لمدة سنة أو سنتين أو 5 سنوات &mdash; دون اشتراك شهري ودون رسوم لكل مستخدم.</p></div></div></div>')
    pages = [
        cover(p, tr('Offline mobile POS', 'كاشير على الجوال دون إنترنت'), tr('SELLO Lite<span>mobile POS app</span>', 'SELLO Lite<span>تطبيق كاشير للجوال</span>'),
              '<div class="visual phones"><div class="phone"><img src="img/lite-sell.jpg" alt=""></div><div class="phone"><img src="img/lite-portions.jpg" alt=""></div><div class="phone"><img src="img/lite-report.jpg" alt=""></div></div>',
              logo='images/products/sello-lite-logo.png'),
        overview(p, 2, tr('01 &middot; Overview', '01 &middot; نظرة عامة'), lic),
        page(f'''
        <div class="kicker">{tr('02 &middot; The app', '02 &middot; التطبيق')}</div>
        <h2>{tr('Inside <em>SELLO Lite</em>', 'داخل <em>SELLO Lite</em>')}</h2>
        <p class="lead" style="margin-bottom:6mm">{tr('Real screens from the SELLO Lite app on an Android phone.', 'شاشات حقيقية من تطبيق SELLO Lite على هاتف أندرويد.')}</p>
        <div class="phones3">{phones}</div>''', 3, p['name'], geo='tl'),
        page(f'''
        <div class="kicker">{tr('02 &middot; The app', '02 &middot; التطبيق')}</div>
        <h2>{tr('Set up <em>your way</em>', 'إعداد <em>على طريقتك</em>')}</h2>
        <p class="lead" style="margin-bottom:6mm">{tr('Products, receipts, payments, languages and security are all managed on the device.', 'المنتجات والإيصالات والدفع واللغات والأمان تُدار جميعها على الجهاز.')}</p>
        <div class="phones4">{phones4}</div>
        <h3 class="sub2">{tr('Runs on', 'يعمل على')}</h3>
        <div class="callouts">
            <div><h3>{tr('Android phones', 'هواتف أندرويد')}</h3><p>{tr('A complete till in your pocket for counters, stalls and deliveries.', 'كاشير كامل في جيبك للكاونترات والأكشاك والتوصيل.')}</p></div>
            <div><h3>{tr('Android tablets', 'أجهزة أندرويد اللوحية')}</h3><p>{tr('A bigger product grid for busy counters and caf&eacute;s.', 'شبكة منتجات أكبر للكاونترات والمقاهي المزدحمة.')}</p></div>
            <div><h3>{tr('Receipts', 'الإيصالات')}</h3><p>{tr('Print or share receipts sized for A4 or 80 / 78 / 58 mm thermal rolls, with your logo.', 'اطبع أو شارك إيصالات بمقاس A4 أو لفائف حرارية 80 / 78 / 58 مم، مع شعارك.')}</p></div>
        </div>''', 4, p['name']),
        features_page(p, 5, tr('03 &middot; Capabilities', '03 &middot; الإمكانات')),
        closing(p, 6),
    ]
    return html_doc(tr('SELLO Lite - Product Brochure', 'SELLO Lite - كتيّب المنتج'), ''.join(pages))


# ---------------------------------------------------------------- Automatic Bell
def bell():
    p = prod('automatic-bell')
    imgs = {'bell-app-home.webp': 'bell-home.jpg', 'bell-app-ringing.webp': 'bell-ringing.jpg', 'bell-app-schedule.webp': 'bell-schedule.jpg',
            'bell-app-weekdays.webp': 'bell-weekdays.jpg', 'bell-app-holidays.webp': 'bell-holidays.jpg', 'bell-app-settings.webp': 'bell-settings.jpg'}
    phones = ''.join(f'<figure><div class="phone"><img src="img/{imgs[img]}" alt=""></div><figcaption><b>{label}</b>{text}</figcaption></figure>'
                     for label, img, title, text, pts in p['tabs'])
    chips = ''.join(f'<span>{a}</span>' for a in p['audience'])
    inside = tr([('Smart controller', 'An ESP32 microcontroller runs the schedule and serves the app over WiFi.'),
                 ('Real-time clock', 'A DS3231 clock keeps accurate time through power cuts and WiFi outages.'),
                 ('Relay output', 'Switches your existing bell on and off &mdash; wired in series with its power feed.'),
                 ('WiFi enabled', 'Joins the school network; falls back to its own setup hotspot if it can&rsquo;t connect.'),
                 ('Manual ring button', 'Ring instantly from the panel &mdash; or from the app &mdash; for assemblies and drills.'),
                 ('Local only', 'No cloud service: schedules, holidays and WiFi settings are stored on the device.')],
                [('وحدة تحكم ذكية', 'متحكم ESP32 يشغّل الجدول ويخدم التطبيق عبر WiFi.'),
                 ('ساعة حقيقية', 'ساعة DS3231 تحافظ على الوقت بدقة أثناء انقطاع الكهرباء أو WiFi.'),
                 ('مخرج مرحّل', 'يشغّل جرسك الحالي ويطفئه &mdash; موصول على التوالي مع تغذيته.'),
                 ('يدعم WiFi', 'ينضم إلى شبكة المدرسة، ويفتح نقطة إعداد خاصة به إذا تعذّر الاتصال.'),
                 ('زر رنين يدوي', 'رنين فوري من اللوحة &mdash; أو من التطبيق &mdash; للطابور والتمارين.'),
                 ('محلي بالكامل', 'دون خدمة سحابية: الجداول والعطل وإعدادات WiFi محفوظة على الجهاز.')])
    inside_html = ''.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in inside)
    ring = tr(('On the panel', 'Power light and the one-touch manual ring button.', 'On the phone', 'Ring for 3, 5, 10 or 30 seconds from the app.',
               'Two ways to ring', 'Bells ring automatically on the timetable. For assemblies, drills or emergencies, ring by hand from the panel button or from the app on your phone.'),
              ('على اللوحة', 'مؤشر التشغيل وزر الرنين اليدوي بلمسة واحدة.', 'على الجوال', 'رنين لمدة 3 أو 5 أو 10 أو 30 ثانية من التطبيق.',
               'طريقتان للرنين', 'ترنّ الأجراس تلقائيًا حسب الجدول. وللطابور أو التمارين أو الطوارئ، اضغط زر اللوحة أو استخدم التطبيق على جوالك.'))
    extra = tr('''
        <div class="two mt-s"><div class="panel"><h3>Installation</h3><p>We mount the controller near your existing bell, wire it into the bell&rsquo;s power circuit, join it to the school WiFi and enter your timetable. After that, every change is made from the app &mdash; no electrician needed.</p></div>
        <div class="panel lime"><h3>Not just schools</h3><p>Colleges, hostels, madrasas, training centres, factories and offices use the same system for periods, meals, shifts and breaks.</p></div></div>''', '''
        <div class="two mt-s"><div class="panel"><h3>التركيب</h3><p>نثبّت وحدة التحكم قرب جرسك الحالي، ونوصلها بدائرة تغذيته، ونربطها بشبكة WiFi المدرسة، وندخل جدولك. بعد ذلك تتم كل التعديلات من التطبيق &mdash; دون حاجة إلى كهربائي.</p></div>
        <div class="panel lime"><h3>ليس للمدارس فقط</h3><p>تستخدم الكليات والسكن الطلابي والمدارس الدينية ومراكز التدريب والمصانع والمكاتب النظام نفسه للحصص والوجبات والورديات والاستراحات.</p></div></div>''')
    pages = [
        cover(p, tr('IoT &middot; School automation', 'إنترنت الأشياء &middot; أتمتة المدارس'), tr('Automatic<span>school bell</span>', 'الجرس<span>المدرسي الآلي</span>'),
              '<div class="visual"><img src="img/bell-panel.jpg" alt=""></div>'),
        overview(p, 2, tr('01 &middot; Overview', '01 &middot; نظرة عامة'),
                 f'<div class="mt"><h3 class="sub2" style="margin-top:0">{tr("Who uses it", "من يستخدمه")}</h3><div class="chips">{chips}</div></div>'
                 f'<div class="ring-two"><figure><img src="img/bell-buttons.jpg" alt=""><figcaption class="cap"><b>{ring[0]}</b>{ring[1]}</figcaption></figure>'
                 f'<figure><div class="phone"><img src="img/bell-ringing.jpg" alt=""></div><figcaption class="cap"><b>{ring[2]}</b>{ring[3]}</figcaption></figure>'
                 f'<div class="panel lime"><h3>{ring[4]}</h3><p>{ring[5]}</p></div></div>'),
        page(f'''
        <div class="kicker">{tr('02 &middot; The device', '02 &middot; الجهاز')}</div>
        <h2>{tr('The <em>bell controller</em>', 'وحدة <em>التحكم بالجرس</em>')}</h2>
        <p class="lead" style="margin-bottom:5mm">{tr('A wall-mounted controller wired into your existing bell circuit. It keeps its own time, rings on schedule and can be rung by hand.', 'وحدة تحكم تُثبّت على الجدار وتوصل بدائرة جرسك الحالي. تحافظ على وقتها بنفسها، وترنّ حسب الجدول، ويمكن تشغيلها يدويًا.')}</p>
        <figure class="figure-wide" style="margin-top:0"><img src="img/bell-panel.jpg" alt="" style="height:78mm"><figcaption class="cap"><b>{tr('Installed controller', 'وحدة تحكم مركّبة')}</b>{tr('Power indicator, a one-touch manual ring button, and the controller inside the panel.', 'مؤشر التشغيل، وزر رنين يدوي بلمسة واحدة، ووحدة التحكم داخل اللوحة.')}</figcaption></figure>
        <h3 class="sub2">{tr('What&rsquo;s inside', 'ماذا يوجد بالداخل')}</h3>
        <div class="callouts">{inside_html}</div>''', 3, p['name'], geo='tl'),
        page(f'''
        <div class="kicker">{tr('03 &middot; The app', '03 &middot; التطبيق')}</div>
        <h2>{tr('The <em>app</em>', '<em>التطبيق</em>')}</h2>
        <p class="lead" style="margin-bottom:6mm">{tr('Real screens from the School Bell app.', 'شاشات حقيقية من تطبيق جرس المدرسة.')}</p>
        <div class="phones3">{phones}</div>''', 4, p['name']),
        features_page(p, 5, tr('04 &middot; Capabilities', '04 &middot; الإمكانات'), extra=extra),
        closing(p, 6),
    ]
    return html_doc(tr('Automatic Bell - Product Brochure', 'الجرس الآلي - كتيّب المنتج'), ''.join(pages))


def main():
    global LANG
    for LANG in ('en', 'ar'):
        suffix = '-ar' if LANG == 'ar' else ''
        for name, fn in (('sello', sello), ('sello-lite', sello_lite), ('automatic-bell', bell)):
            (HERE / f'{name}{suffix}.html').write_text(fn(), encoding='utf-8')
            print('wrote', f'tools/brochures/{name}{suffix}.html')


if __name__ == '__main__':
    main()
