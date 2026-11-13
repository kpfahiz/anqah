# Anqah Tech business card

**Size:** 90 × 55 mm (the common UAE/India size), printed on both sides.

**Files** in `out/`:

| File | Use |
|---|---|
| `Anqah-Tech-Business-Card.pdf` | **Send this to the printer.** Page 1 = front, page 2 = back. 96 × 61 mm = 90 × 55 mm trim + 3 mm bleed on each side. Text, icons and QR are vector; fonts are embedded. |
| `card-front.png`, `card-back.png` | 300 dpi previews (with bleed), e.g. for WhatsApp or approvals |
| `card-mockup.jpg` | Both sides as they'll look after cutting |

## What to tell the printer
- **Size and sides:** "90 × 55 mm, double-sided. The PDF includes 3 mm bleed. Please trim to 90 × 55."
- **Paper:** 350–400 gsm, **matte or soft-touch lamination**. A dark card looks best matte.
- **Optional upgrade:** **spot UV** on the logo and the lime corner brackets, or lime foil if they offer it.
- **Colour:** the file is RGB (screen colours). Ask the printer to convert to CMYK and **send a proof**. The lime (#b6ff3b) prints slightly duller in CMYK, so check the proof.
- **QR code:** links to https://www.anqah.com/. Tested: it scans correctly. Keep it at least 20 mm wide (it is 21 mm).

## Editing
Edit `card.html`, then run:
```
node tools/business-card/render_card.mjs <path-to-node_modules-with-playwright-core>
```
To change the QR link, regenerate `qr-website.svg` with the `qrcode` npm package and paste it into the `.qr` box in `card.html`.
