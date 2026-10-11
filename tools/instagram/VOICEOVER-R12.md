# Voice-over: Reel R12 "A dashboard from zero"

The finished videos are in `out/`:

| File | Audio |
|---|---|
| `reel-r12-dev-voice-en.mp4` | English narration (en-US-AndrewNeural) + music + sound effects |
| `reel-r12-dev-voice-ar.mp4` | Arabic narration (ar-AE-HamdanNeural) + music + sound effects |
| `reel-r12-dev.mp4` | Music + sound effects only |
| `reel-r12-dev-silent.mp4` | No audio (add a trending sound in Instagram) |

## Script

| # | Plays at | Max | English | Arabic (Gulf) |
|---|---|---|---|---|
| 1 | 0.3 s | 1.8 s | "Let's build a dashboard, from zero." | «نبني لوحة تحكم من الصفر.» |
| 2 | 2.4 s | 3.1 s | "Every line of code, written for your business." | «كل سطر كود، مكتوب لعملك أنت.» |
| 3 | 5.8 s | 3.1 s | "Live sales, charts and orders, all in one place." | «المبيعات والتقارير، في مكان واحد.» |
| 4 | 9.3 s | 3.1 s | "Fast, secure, and in Arabic with one click." | «سريعة وآمنة، وبالعربي بضغطة.» |
| 5 | 12.8 s | 2.1 s | "Comment DEV, and let's build yours." | «علّق تطوير، ونبنيها لك.» |

## How it was made / regenerate
```
python tools/instagram/reel_audio_r12.py                                  # music + effects -> out/reel-r12-dev.wav
node tools/instagram/render_reel.mjs <node_modules> reel-r12-dev.html 15  # video (+ music-only mix)
node tools/instagram/tts_voiceover.mjs <node_modules> r12 en|ar           # voice lines -> voice/r12/<lang>/
python tools/instagram/mix_voiceover.py <ffmpeg.exe> r12 en|ar            # final narrated Reels
```
`tts_voiceover.mjs` sends the script text to Microsoft's speech service. To use your own recordings instead, replace the files in `voice/r12/<lang>/` (named 1–5) and run only the mixer.
The dashboard figures and customer names are demo data.
