"""Writes sitemap.xml: every page in English and Arabic, linked as language alternates, with its images.
Run after adding pages or images:
    python tools/build_sitemap.py
"""
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from blog_content import ARTICLES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://www.anqah.com'


def images(folder, pattern='*.webp'):
    return sorted(f'images/products/{folder}/{p.name}' for p in (ROOT / 'images/products' / folder).glob(pattern))


# path (relative to the site root, same for /ar/) -> images on that page
PAGES = {
    '': ['images/og/og-home.jpg'],
    'products/sello.html': ['images/og/og-sello.jpg', 'images/products/sello-logo.png', *images('sello', '*-device.webp'),
                             *sorted(f'images/products/pos-hardware/{p.name}' for p in (ROOT / 'images/products/pos-hardware').glob('*.jpg'))],
    'products/sello-lite.html': ['images/og/og-sello-lite.jpg', 'images/products/sello-lite-logo.png', *images('sello-lite')],
    'products/automatic-bell.html': ['images/og/og-automatic-bell.jpg', *images('automatic-bell')],
    'products/water-monitoring.html': ['images/og/og-water-monitoring.jpg'],
    'blog/': [],
    **{f'blog/{a["slug"]}.html': [f'images/og/og-{a["product"]}.jpg'] for a in ARTICLES},
}
HREFLANG_EN = ('en', 'en-AE', 'en-SA', 'en-IN', 'x-default')
HREFLANG_AR = ('ar', 'ar-AE', 'ar-SA')


def main():
    today = date.today().isoformat()
    rows = []
    for path, imgs in PAGES.items():
        en, ar = f'{SITE}/{path}', f'{SITE}/ar/{path}'
        alternates = [f'<xhtml:link rel="alternate" hreflang="{h}" href="{en}"/>' for h in HREFLANG_EN]
        alternates += [f'<xhtml:link rel="alternate" hreflang="{h}" href="{ar}"/>' for h in HREFLANG_AR]
        image_tags = [f'<image:image><image:loc>{SITE}/{i}</image:loc></image:image>' for i in imgs]
        blog = path.startswith('blog/')
        for loc, prio in ((en, '1.0' if not path else '0.6' if blog else '0.8'), (ar, '0.9' if not path else '0.5' if blog else '0.7')):
            lines = [f'<loc>{loc}</loc>', f'<lastmod>{today}</lastmod>', '<changefreq>monthly</changefreq>',
                     f'<priority>{prio}</priority>', *alternates, *image_tags]
            rows.append('  <url>\n' + ''.join(f'    {line}\n' for line in lines) + '  </url>')
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:xhtml="http://www.w3.org/1999/xhtml" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
           + '\n'.join(rows) + '\n</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8')
    print('sitemap.xml:', len(rows), 'URLs (English + Arabic)')


if __name__ == '__main__':
    main()
