// Generates Reel voice-over lines with Microsoft neural voices (msedge-tts) into voice/<reel>/<lang>/<n>.mp3, ready for
// mix_voiceover.py. Lines that run past their slot are re-generated a little faster (up to +15%, so it stays natural).
// Needs msedge-tts and ffmpeg-static in one node_modules folder:
//   node tools/instagram/tts_voiceover.mjs <path-to-node_modules> r3|r7|r9|r10|r12|r14 en|ar
// Note: the text is sent to Microsoft's speech service to synthesise the audio.
import { createRequire } from 'node:module';
import { copyFileSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import os from 'node:os';
import path from 'node:path';

const [modules, reelName, lang] = process.argv.slice(2);
const req = createRequire(path.join(path.resolve(modules), 'x.js'));
const { MsEdgeTTS, OUTPUT_FORMAT } = req('msedge-tts');
const ffmpeg = req('ffmpeg-static');
const here = path.dirname(fileURLToPath(import.meta.url));

// Per reel: slot lengths (s) matching mix_voiceover.py / VOICEOVER-<reel>.md, then the lines for each language.
const VOICES = { en: { voice: 'en-US-AndrewNeural', pitch: '-2%' }, ar: { voice: 'ar-AE-HamdanNeural', pitch: '-2%' } };
const SCRIPTS = {
  r3: { slots: [2.0, 2.3, 2.3, 2.3, 2.3, 2.4, 1.9, 2.1], en: [
    'Five signs your shop needs a real POS.',
    'One: long queues at the counter.',
    "Two: you don't know what's in stock.",
    "Three: the cash never matches.",
    'Four: VAT time is a headache.',
    "Five: you can't see sales when you're away.",
    'SELLO fixes all five.',
    'Comment POS for a free demo.',
  ], ar: [
    'خمس علامات إن محلك يبي كاشير.',
    'واحد: طوابير طويلة.',
    'اثنين: ما تعرف وش في المخزون.',
    'ثلاثة: الكاش ما يطابق.',
    'أربعة: الضريبة صداع.',
    'خمسة: ما تشوف مبيعاتك من برّا.',
    'سيلو يحلّ الخمسة كلها.',
    'علّق كاشير لعرض مجاني.',
  ] },
  r7: { slots: [2.1, 1.8, 2.7, 3.0, 2.25], en: [
    'Is your website stuck in 2015?',
    'Slow, and hard to use on a phone.',
    "Here's what a modern website looks like.",
    'Fast, mobile-first, and easy to find on Google.',
    'Comment WEB for a free review.',
  ], ar: [
    'موقعك قديم؟',
    'بطيء، ومو للجوال.',
    'هذا شكل الموقع الحديث.',
    'سريع، للجوال، ويظهر في جوجل.',
    'علّق موقع، مجانًا.',
  ] },
  r9: { slots: [2.2, 4.4, 2.2, 3.0, 2.4], en: [
    'Every great app starts as an idea.',
    'We design it… and build it, for Android and iPhone.',
    'Test it on every phone…',
    'and launch it to the world.',
    'Comment APP, and tell us your idea.',
  ], ar: [
    'كل تطبيق ناجح يبدأ بفكرة.',
    'نصممه… ونبنيه، لأندرويد وآيفون.',
    'نختبره على كل جوال…',
    'ونطلقه للعالم.',
    'علّق تطبيق، وقول لنا فكرتك.',
  ] },
  r10: { slots: [2.8, 4.0, 1.4, 2.6, 2.2], en: [
    'Two a.m. A customer just messaged your shop.',
    'Your AI assistant replied in two seconds, and took the order.',
    'In English, or Arabic.',
    'You woke up to three new orders.',
    'Comment A.I. to get yours.',
  ], ar: [
    'ثنتين بالليل، وعميل راسل محلك.',
    'مساعدك الذكي ردّ في ثانيتين، وأخذ الطلب.',
    'بالعربي والإنجليزي.',
    'وصحيت على ثلاث طلبات جديدة.',
    'علّق إيه آي، ونجهّزه لك.',
  ] },
  r12: { slots: [1.8, 3.1, 3.1, 3.1, 2.1], en: [
    "Let's build a dashboard, from zero.",
    'Every line of code, written for your business.',
    'Live sales, charts and orders, all in one place.',
    'Fast, secure, and in Arabic with one click.',
    "Comment DEV, and let's build yours.",
  ], ar: [
    'نبني لوحة تحكم من الصفر.',
    'كل سطر كود، مكتوب لعملك أنت.',
    'المبيعات والتقارير، في مكان واحد.',
    'سريعة وآمنة، وبالعربي بضغطة.',
    'علّق تطوير، ونبنيها لك.',
  ] },
  r14: { slots: [2.3, 1.75, 2.9, 2.8, 2.2], en: [
    'Still tracking leads like this?',
    'Leads get lost. Sales slip away.',
    'With a custom CRM, every lead has its place.',
    'And every follow-up happens on time.',
    "Comment CRM, and we'll build yours.",
  ], ar: [
    'لسّه تتابع عملاءك كذا؟',
    'والعملاء يضيعون!',
    'مع نظام سي آر إم، كل عميل في مكانه.',
    'وكل متابعة في وقتها.',
    'علّق سي آر إم، ونبنيه لك.',
  ] },
};
const reel = SCRIPTS[reelName];
if (!reel || !VOICES[lang]) throw new Error('usage: tts_voiceover.mjs <node_modules> <reel: ' + Object.keys(SCRIPTS).join('|') + '> en|ar');
const SLOTS = reel.slots;
const script = { ...VOICES[lang], lines: reel[lang] };

const TRIM = 'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse';
function spokenLength(file) { // seconds, without leading/trailing silence
  const { stderr } = spawnSync(ffmpeg, ['-i', file, '-af', TRIM, '-f', 'null', '-'], { encoding: 'utf8' });
  const m = [...stderr.matchAll(/time=(\d+):(\d+):([\d.]+)/g)].pop();
  return +m[1] * 3600 + +m[2] * 60 + +m[3];
}

const outDir = path.join(here, 'voice', reelName, lang);
mkdirSync(outDir, { recursive: true });
const tts = new MsEdgeTTS();
await tts.setMetadata(script.voice, OUTPUT_FORMAT.AUDIO_24KHZ_96KBITRATE_MONO_MP3);

for (let i = 0; i < script.lines.length; i++) {
  const dest = path.join(outDir, `${i + 1}.mp3`);
  for (let speed = 0; speed <= 15; speed += 5) {
    const tmp = mkdtempSync(path.join(os.tmpdir(), 'tts-'));
    const { audioFilePath } = await tts.toFile(tmp, script.lines[i], { rate: `+${speed}%`, pitch: script.pitch });
    copyFileSync(audioFilePath, dest); // copy, not rename: temp dir may be on another drive
    rmSync(tmp, { recursive: true, force: true });
    const len = spokenLength(dest);
    if (len <= SLOTS[i] + 0.15 || speed === 15) {
      console.log(`line ${i + 1}: ${len.toFixed(2)}s / slot ${SLOTS[i]}s  rate +${speed}%${len > SLOTS[i] + 0.15 ? '  (still long)' : ''}`);
      break;
    }
  }
}
tts.close();
console.log('wrote', path.relative(path.resolve(here, '../..'), outDir));
