# Voice-over: Reel R9 "Idea → App in 4 steps"

The finished videos are in `out/`:

| File | Audio |
|---|---|
| `reel-r9-app-voice-en.mp4` | English narration (en-US-AndrewNeural) + music + sound effects |
| `reel-r9-app-voice-ar.mp4` | Arabic narration (ar-AE-HamdanNeural) + music + sound effects |
| `reel-r9-app.mp4` | Music + sound effects only |
| `reel-r9-app-silent.mp4` | No audio (add a trending sound in Instagram) |

## Script

| # | Plays at | Max | English | Arabic (Gulf) |
|---|---|---|---|---|
| 1 | 0.3 s | 2.2 s | "Every great app starts as an idea." | «كل تطبيق ناجح يبدأ بفكرة.» |
| 2 | 2.8 s | 4.4 s | "We design it… and build it, for Android and iPhone." | «نصممه… ونبنيه، لأندرويد وآيفون.» |
| 3 | 7.6 s | 2.2 s | "Test it on every phone…" | «نختبره على كل جوال…» |
| 4 | 10.0 s | 3.0 s | "and launch it to the world." | «ونطلقه للعالم.» |
| 5 | 13.4 s | 2.4 s | "Comment APP, and tell us your idea." | «علّق تطبيق، وقول لنا فكرتك.» |

## How it was made / regenerate
```
python tools/instagram/reel_audio_r9.py                                  # music + effects -> out/reel-r9-app.wav
node tools/instagram/render_reel.mjs <node_modules> reel-r9-app.html 16  # video (+ music-only mix)
node tools/instagram/tts_voiceover.mjs <node_modules> r9 en|ar           # voice lines -> voice/r9/<lang>/
python tools/instagram/mix_voiceover.py <ffmpeg.exe> r9 en|ar            # final narrated Reels
```
`tts_voiceover.mjs` sends the script text to Microsoft's speech service. To use your own recordings instead, replace the files in `voice/r9/<lang>/` (named 1–5) and run only the mixer.
The finished app is our real SELLO Lite. The store page is generic: no store logos or brand names and no ratings, so nothing implies a listing or reviews that don't exist.
