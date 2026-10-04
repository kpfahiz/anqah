"""Builds the site icons (Google search result icon, browser tab, home screen) from the white logo mark.
White mark on a solid brand-navy square, so it stays readable on light and dark backgrounds.
    python tools/build_icons.py
Writes: favicon.ico (16/32/48), images/favicon-48.png, images/favicon.png (192), images/apple-touch-icon.png (180),
        images/icon-512.png
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
NAVY = (35, 52, 92, 255)  # from the logo


def icon(size, scale=0.8):
    mark = Image.open(ROOT / 'images/logo-mark-white.png').convert('RGBA')
    mark = mark.crop(mark.getbbox())
    w = round(size * scale)
    h = round(mark.height * w / mark.width)
    canvas = Image.new('RGBA', (size, size), NAVY)
    big = mark.resize((w, h), Image.Resampling.LANCZOS)
    canvas.alpha_composite(big, ((size - w) // 2, (size - h) // 2))
    return canvas


def main():
    out = {
        'images/favicon-48.png': 48,
        'images/favicon.png': 192,
        'images/apple-touch-icon.png': 180,
        'images/icon-512.png': 512,
    }
    for path, size in out.items():
        icon(size).save(ROOT / path, optimize=True)
        print('wrote', path)
    icon(256).save(ROOT / 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48)])
    print('wrote favicon.ico')


if __name__ == '__main__':
    main()
