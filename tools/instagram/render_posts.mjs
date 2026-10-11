// Renders every .post in tools/instagram/posts.html, posts-ar.html, services.html, reels.html and stories.html to tools/instagram/out/<id>.png (1080x1350).
// Needs playwright-core:  node tools/instagram/render_posts.mjs [path-to-node_modules-with-playwright-core]
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const req = createRequire(process.argv[2] ? path.join(path.resolve(process.argv[2]), 'x.js') : import.meta.url);
const { chromium } = req('playwright-core');

const outDir = path.join(here, 'out');
mkdirSync(outDir, { recursive: true });
const browser = await chromium.launch({ channel: 'msedge', headless: true });
const page = await browser.newPage({ viewport: { width: 1200, height: 1600 } });
for (const file of ['posts.html', 'posts-ar.html', 'services.html', 'reels.html', 'stories.html']) {
  await page.goto(pathToFileURL(path.join(here, file)).href, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  for (const id of await page.$$eval('.post', els => els.map(e => e.id))) {
    await page.locator(`[id="${id}"]`).screenshot({ path: path.join(outDir, `${id}.png`) });
    console.log('wrote', `tools/instagram/out/${id}.png`);
  }
}
await browser.close();
