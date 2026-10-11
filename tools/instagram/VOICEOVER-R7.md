# Voice-over: Reel R7 "Website glow-up: 2015 vs 2026"

The finished videos are in `out/`:

| File | Audio |
|---|---|
| `reel-r7-web-voice-en.mp4` | English narration (en-US-AndrewNeural) + music + sound effects |
| `reel-r7-web-voice-ar.mp4` | Arabic narration (ar-AE-HamdanNeural) + music + sound effects |
| `reel-r7-web.mp4` | Music + sound effects only |
| `reel-r7-web-silent.mp4` | No audio (add a trending sound in Instagram) |

## Script

| # | Plays at | Max | English | Arabic (Gulf) |
|---|---|---|---|---|
| 1 | 0.3 s | 2.1 s | "Is your website stuck in 2015?" | «موقعك قديم؟» |
| 2 | 2.5 s | 1.8 s | "Slow, and hard to use on a phone." | «بطيء، ومو للجوال.» |
| 3 | 4.6 s | 2.7 s | "Here's what a modern website looks like." | «هذا شكل الموقع الحديث.» |
| 4 | 7.6 s | 3.0 s | "Fast, mobile-first, and easy to find on Google." | «سريع، للجوال، ويظهر في جوجل.» |
| 5 | 10.75 s | 2.25 s | "Comment WEB for a free review." | «علّق موقع، مجانًا.» |

The Arabic lines are shorter than a direct translation so they fit their scenes. "2015" isn't spoken because it takes too long in Arabic; it's on screen instead. Line 5 is short because the end card shows «مراجعة مجانية لموقعك».

## How it was made / regenerate
```
python tools/instagram/reel_audio_r7.py                                  # music + effects -> out/reel-r7-web.wav
node tools/instagram/render_reel.mjs <node_modules> reel-r7-web.html 13  # video (+ music-only mix)
node tools/instagram/tts_voiceover.mjs <node_modules> r7 en|ar           # voice lines -> voice/r7/<lang>/
python tools/instagram/mix_voiceover.py <ffmpeg.exe> r7 en|ar            # final narrated Reels
```
`tts_voiceover.mjs` sends the script text to Microsoft's speech service. To use your own recordings instead, replace the files in `voice/r7/<lang>/` (named 1–5) and run only the mixer.
The "2015" site is a made-up generic page, not any real company's site. The "2026" site is our own website, anqah.com (screenshots in `img/`, taken from the local site with its 3D scenes running).
