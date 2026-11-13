// Renders card.html to print files in tools/business-card/out/:
//   Anqah-Tech-Business-Card.pdf    2 pages (front, back), 96 x 61 mm = 90 x 55 mm trim + 3 mm bleed, vector text + QR
//   card-front.png / card-back.png  300 dpi previews (about 1134 x 719 px, with bleed)
// Needs playwright-core:  node tools/business-card/render_card.mjs <path-to-node_modules-with-playwright-core>
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const req = createRequire(path.join(path.resolve(process.argv[2]), 'x.js'));
const { chromium } = req('playwright-core');
const out = path.join(here, 'out');
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({ channel: 'msedge', headless: true });
// 1 CSS px = 1/96 in, so a 300/96 device scale gives 300 dpi
const page = await browser.newPage({ deviceScaleFactor: 300 / 96, viewport: { width: 400, height: 500 } });
await page.goto(pathToFileURL(path.join(here, 'card.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
// PNG previews: show one side at a time at the page origin and clip to it. Playwright rounds the clip to whole CSS px,
// so they come out 1134 x 719 px at 300 dpi; the PDF below is the exact print master.
const clip = { x: 0, y: 0, width: 363, height: 230 };
for (const [i, name] of [[0, 'card-front'], [1, 'card-back']]) {
  await page.evaluate(i => document.querySelectorAll('.side').forEach((el, j) => el.style.display = j === i ? '' : 'none'), i);
  await page.screenshot({ path: path.join(out, `${name}.png`), clip });
}
await page.evaluate(() => document.querySelectorAll('.side').forEach(el => el.style.display = ''));
await page.pdf({ path: path.join(out, 'Anqah-Tech-Business-Card.pdf'), preferCSSPageSize: true, printBackground: true });
await browser.close();
console.log('wrote tools/business-card/out/: Anqah-Tech-Business-Card.pdf, card-front.png, card-back.png');
