"""Builds the 1200x630 social-share (Open Graph) images in images/og/.

Run: python tools/build_og_images.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'images' / 'og'
FONTS = Path('C:/Windows/Fonts')
W, H = 1200, 630
BG, LINE, TEXT, MUTED, LIME = (7, 8, 10), (29, 34, 40), (233, 237, 240), (127, 136, 146), (182, 255, 59)

CARDS = [
    # file, eyebrow, title lines, subtitle, image (optional, relative to images/)
    ('og-home.jpg', 'POS SOFTWARE · IOT · IT SERVICES', ['Smart POS, IoT &', 'IT solutions'],
     'UAE · Saudi Arabia · India', 'products/sello/sello-pos-device.webp'),
    ('og-sello.jpg', 'POS & SHOP MANAGEMENT', ['SELLO POS', 'Software'],
     'Retail · Restaurants · Cafés — UAE · KSA · India', 'products/sello/sello-pos-device.webp'),
    ('og-sello-lite.jpg', 'OFFLINE MOBILE POS APP', ['SELLO Lite'],
     'Billing that works without internet', 'products/sello-lite/sello-lite-sell.webp'),
    ('og-automatic-bell.jpg', 'IOT · SCHOOL AUTOMATION', ['Automatic', 'School Bell'],
     'Scheduled bells, controlled from your phone', 'products/automatic-bell/bell-system-steel.webp'),
    ('og-water-monitoring.jpg', 'IOT · TANK MONITORING', ['Water Level', 'Monitoring'],
     'Live level on your phone · Telegram alerts', None),
]


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def card(eyebrow, title, subtitle, image):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(14, 16, 19))
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(14, 16, 19))
    right = 0
    if image:
        ph = Image.open(ROOT / 'images' / image).convert('RGB')
        if ph.height > ph.width:  # phone screenshot: show it in a simple phone frame
            ph.thumbnail((250, 540))
            frame = Image.new('RGB', (ph.width + 24, ph.height + 24), (34, 38, 44))
            frame.paste(ph, (12, 12))
            im.paste(frame, (W - frame.width - 90, (H - frame.height) // 2))
            right = frame.width + 140
        else:
            ph = ph.resize((round(ph.width * H / ph.height), H))
            if ph.width > 600:  # keep the screen: POS photos have it on the left, others on the right
                ph = ph.crop((0, 0, 600, H)) if 'sello-pos' in image else ph.crop((ph.width - 600, 0, ph.width, H))
            mask = Image.linear_gradient('L').rotate(90).resize((ph.width, H))  # fade into the text side
            im.paste(ph, (W - ph.width, 0), mask)
            right = ph.width - 60
    logo = Image.open(ROOT / 'images' / 'logo-mark-white.png').convert('RGBA')
    logo.thumbnail((86, 86))
    im.paste(logo, (70, 62), logo)
    d.text((172, 72), 'ANQAH TECH', font=font('bahnschrift.ttf', 40), fill=TEXT)
    d.text((70, 200), eyebrow, font=font('consola.ttf', 24), fill=LIME)
    y = 240
    for line in title:
        d.text((66, y), line, font=font('segoeuib.ttf', 74), fill=TEXT)
        y += 86
    d.text((70, y + 24), subtitle, font=font('segoeui.ttf', 30), fill=MUTED)
    d.rectangle((70, H - 64, 70 + 120, H - 58), fill=LIME)
    d.text((70, H - 50), 'www.anqah.com', font=font('consola.ttf', 22), fill=MUTED)
    return im


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for f, eyebrow, title, subtitle, image in CARDS:
        card(eyebrow, title, subtitle, image).save(OUT / f, quality=86, optimize=True)
        print('wrote images/og/' + f)
