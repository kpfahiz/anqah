# Voice-over: Reel R3 "5 signs your shop needs a real POS"

An animated alternative to the filmed "POV: closing time" script in REELS.md, and a companion to the 5-signs carousel post.

| File | Audio |
|---|---|
| `out/reel-r3-signs-voice-en.mp4` | English narration (en-US-AndrewNeural) + music + sound effects |
| `out/reel-r3-signs-voice-ar.mp4` | Arabic narration (ar-AE-HamdanNeural) + music + sound effects |
| `out/reel-r3-signs.mp4` | Music + sound effects only |
| `out/reel-r3-signs-silent.mp4` | No audio (add a trending sound in Instagram) |

## Script (8 lines)

| # | Plays at | Max | English | Arabic (Gulf) |
|---|---|---|---|---|
| 1 | 0.3 s | 2.0 s | "Five signs your shop needs a real POS." | «خمس علامات إن محلك يبي كاشير.» |
| 2 | 2.6 s | 2.3 s | "One: long queues at the counter." | «واحد: طوابير طويلة.» |
| 3 | 5.2 s | 2.3 s | "Two: you don't know what's in stock." | «اثنين: ما تعرف وش في المخزون.» |
| 4 | 7.8 s | 2.3 s | "Three: the cash never matches." | «ثلاثة: الكاش ما يطابق.» |
| 5 | 10.4 s | 2.3 s | "Four: VAT time is a headache." | «أربعة: الضريبة صداع.» |
| 6 | 13.0 s | 2.4 s | "Five: you can't see sales when you're away." | «خمسة: ما تشوف مبيعاتك من برّا.» |
| 7 | 15.6 s | 1.9 s | "SELLO fixes all five." | «سيلو يحلّ الخمسة كلها.» |
| 8 | 17.8 s | 2.1 s | "Comment POS for a free demo." | «علّق كاشير لعرض مجاني.» |

## How it was made / regenerate
```
python tools/instagram/reel_audio_r3.py                                    # music + effects -> out/reel-r3-signs.wav
node tools/instagram/render_reel.mjs <node_modules> reel-r3-signs.html 20  # video (+ music-only mix)
node tools/instagram/tts_voiceover.mjs <node_modules> r3 en|ar             # voice lines -> voice/r3/<lang>/
python tools/instagram/mix_voiceover.py <ffmpeg.exe> r3 en|ar              # final narrated Reels
```
`tts_voiceover.mjs` sends the script text to Microsoft's speech service. To use your own recordings instead, replace the files in `voice/r3/<lang>/` (named 1–8) and run only the mixer.
The figures (queue timer, AED 4,250 / 4,100) are illustrative.
