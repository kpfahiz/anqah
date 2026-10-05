// Prints the company profiles to PDF using Microsoft Edge:
//   tools/profile/profile.html    -> downloads/Anqah-Tech-Company-Profile.pdf      (English)
//   tools/profile/profile-ar.html -> downloads/Anqah-Tech-Company-Profile-AR.pdf   (Arabic; run build_profile_ar.py first)
// Needs playwright-core:  node tools/profile/build_profile.mjs [path-to-node_modules-with-playwright-core]
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const req = createRequire(process.argv[2] ? path.join(path.resolve(process.argv[2]), 'x.js') : import.meta.url);
const { chromium } = req('playwright-core');

const jobs = [
  ['profile.html', 'Anqah-Tech-Company-Profile.pdf'],
  ['profile-ar.html', 'Anqah-Tech-Company-Profile-AR.pdf'],
];
mkdirSync(path.join(root, 'downloads'), { recursive: true });
const browser = await chromium.launch({ channel: 'msedge', headless: true });
const page = await browser.newPage();
for (const [src, pdf] of jobs) {
  const out = path.join(root, 'downloads', pdf);
  await page.goto(pathToFileURL(path.join(here, src)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log('wrote', path.relative(root, out));
}
await browser.close();
