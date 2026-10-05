// Prints tools/profile/profile.html to downloads/Anqah-Tech-Company-Profile.pdf using Microsoft Edge.
// Needs playwright-core:  node tools/profile/build_profile.mjs [path-to-node_modules-with-playwright-core]
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../..');
const req = createRequire(process.argv[2] ? path.join(path.resolve(process.argv[2]), 'x.js') : import.meta.url);
const { chromium } = req('playwright-core');

const out = path.join(root, 'downloads', 'Anqah-Tech-Company-Profile.pdf');
mkdirSync(path.dirname(out), { recursive: true });
const browser = await chromium.launch({ channel: 'msedge', headless: true });
const page = await browser.newPage();
await page.goto(pathToFileURL(path.join(here, 'profile.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
await browser.close();
console.log('wrote', path.relative(root, out));
