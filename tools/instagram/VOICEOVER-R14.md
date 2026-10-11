# Voice-over: Reel R14 "Excel chaos vs. CRM calm"

The finished videos are in `out/`:

| File | Audio |
|---|---|
| `reel-r14-crm-voice-en.mp4` | English narration (en-US-AndrewNeural) + music + sound effects |
| `reel-r14-crm-voice-ar.mp4` | Arabic narration (ar-AE-HamdanNeural) + music + sound effects |
| `reel-r14-crm.mp4` | Music + sound effects only |
| `reel-r14-crm-silent.mp4` | No audio (add a trending sound in Instagram) |

## Script

| # | Plays at | Max | English | Arabic (Gulf) |
|---|---|---|---|---|
| 1 | 0.3 s | 2.3 s | "Still tracking leads like this?" | «لسّه تتابع عملاءك كذا؟» |
| 2 | 2.75 s | 1.75 s | "Leads get lost. Sales slip away." | «والعملاء يضيعون!» |
| 3 | 5.4 s | 2.9 s | "With a custom CRM, every lead has its place." | «مع نظام CRM، كل عميل في مكانه.» |
| 4 | 8.5 s | 2.8 s | "And every follow-up happens on time." | «وكل متابعة في وقتها.» |
| 5 | 11.7 s | 2.2 s | "Comment CRM, and we'll build yours." | «علّق CRM، ونبنيه لك.» |

The Arabic lines are shorter than a direct translation so they fit their scenes at natural speed. The on-screen captions keep the fuller wording.

## How it was made / regenerate
```
python tools/instagram/reel_audio_r14.py                               # music + effects -> out/reel-r14-crm.wav
node tools/instagram/render_reel.mjs <node_modules> reel-r14-crm.html 14   # video (+ music-only mix)
node tools/instagram/tts_voiceover.mjs <node_modules> r14 en|ar        # voice lines -> voice/r14/<lang>/
python tools/instagram/mix_voiceover.py <ffmpeg.exe> r14 en|ar         # final narrated Reels
```
`tts_voiceover.mjs` sends the script text to Microsoft's speech service. To use your own recordings instead, replace the files in `voice/r14/<lang>/` (named 1–5) and run only the mixer.
All names and numbers in the animation are demo data.
