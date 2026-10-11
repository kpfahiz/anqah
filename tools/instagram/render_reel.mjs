// Renders an animated Reel page (one exposing window.renderAt(t)) to an MP4: captures every frame at 30 fps, then encodes
// with ffmpeg. Needs playwright-core and ffmpeg-static installed in one node_modules folder:
//   node tools/instagram/render_reel.mjs <path-to-node_modules> reel-r10-ai.html 14.5
// Output: tools/instagram/out/<page-name>-silent.mp4, plus <page-name>.mp4 with sound when out/<page-name>.wav exists
// (e.g. made by reel_audio_r10.py).
import { createRequire } from 'node:module';
import { mkdtempSync, rmSync, existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import os from 'node:os';
import path from 'node:path';

const [modules, file, seconds] = process.argv.slice(2);
if (!modules || !file || !seconds) throw new Error('usage: render_reel.mjs <node_modules> <page.html> <seconds>');
const here = path.dirname(fileURLToPath(import.meta.url));
const req = createRequire(path.join(path.resolve(modules), 'x.js'));
const { chromium } = req('playwright-core');
const ffmpeg = req('ffmpeg-static');

const FPS = 30, frames = Math.round(Number(seconds) * FPS);
const tmp = mkdtempSync(path.join(os.tmpdir(), 'reel-'));
const out = path.join(here, 'out', path.basename(file, '.html') + '.mp4');

const browser = await chromium.launch({ channel: 'msedge', headless: true });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.addInitScript(() => { window.__capture = true; });
await page.goto(pathToFileURL(path.join(here, file)).href, { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
for (let i = 0; i < frames; i++) {
  await page.evaluate(t => window.renderAt(t), i / FPS);
  await page.screenshot({ path: path.join(tmp, `f${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 95 });
  if (i % 60 === 0) console.log(`frame ${i}/${frames}`);
}
await browser.close();

// Always write a silent version (for adding a trending sound in Instagram); if out/<page-name>.wav exists, also mux it in.
const silent = out.replace(/\.mp4$/, '-silent.mp4');
const wav = out.replace(/\.mp4$/, '.wav');
execFileSync(ffmpeg, ['-y', '-loglevel', 'error', '-framerate', String(FPS), '-i', path.join(tmp, 'f%04d.jpg'),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow', '-movflags', '+faststart', silent]);
rmSync(tmp, { recursive: true, force: true });
console.log('wrote', path.relative(path.resolve(here, '../..'), silent));
if (existsSync(wav)) {
  execFileSync(ffmpeg, ['-y', '-loglevel', 'error', '-i', silent, '-i', wav, '-map', '0:v', '-map', '1:a',
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]);
  console.log('wrote', path.relative(path.resolve(here, '../..'), out), '(with audio)');
}
