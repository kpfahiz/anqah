// Prints each product brochure (tools/brochures/<slug>.html) to downloads/brochures/Anqah-<Product>-Brochure.pdf.
// Run python tools/brochures/build_brochures.py first.
// Needs playwright-core:  node tools/brochures/print_brochures.mjs [path-to-node_modules-with-playwright-core]
import { createRequire } from 'node:module';
import { mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const req = createRequire(process.argv[2] ? path.join(path.resolve(process.argv[2]), 'x.js') : import.meta.url);
const { chromium } = req('playwright-core');

const jobs = [
  ['sello.html', 'Anqah-SELLO-Brochure.pdf'],
  ['sello-lite.html', 'Anqah-SELLO-Lite-Brochure.pdf'],
  ['automatic-bell.html', 'Anqah-Automatic-Bell-Brochure.pdf'],
  ['water-monitoring.html', 'Anqah-Water-Monitoring-Brochure.pdf'],
  ['sello-ar.html', 'Anqah-SELLO-Brochure-AR.pdf'],
  ['sello-lite-ar.html', 'Anqah-SELLO-Lite-Brochure-AR.pdf'],
  ['automatic-bell-ar.html', 'Anqah-Automatic-Bell-Brochure-AR.pdf'],
  ['water-monitoring-ar.html', 'Anqah-Water-Monitoring-Brochure-AR.pdf'],
];
const outDir = path.join(root, 'downloads', 'brochures');
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ channel: 'msedge', headless: true });
const page = await browser.newPage();
for (const [src, pdf] of jobs) {
  if (!existsSync(path.join(here, src))) continue;
  await page.goto(pathToFileURL(path.join(here, src)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(outDir, pdf), format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log('wrote', path.relative(root, path.join(outDir, pdf)));
}
await browser.close();
