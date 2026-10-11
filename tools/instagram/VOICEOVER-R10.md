# Voice-over: Reel R10 "AI replies at 2 am"

The narration has two versions, **English** and **Gulf Arabic**. It has 5 short lines, and each line is **recorded as its own file**. The mixer places every line exactly on its scene, lowers the music under the voice, and outputs a finished Reel.

## English script (≈ 30 words)

| # | File | Plays at | Max length | Scene on screen | Say |
|---|---|---|---|---|---|
| 1 | `1.m4a` | 0.3 s | **2.8 s** | Night, phone buzzes | "Two a.m. A customer just messaged your shop." |
| 2 | `2.m4a` | 3.5 s | **4.0 s** | AI replies, "2s reply" badge | "Your AI assistant replied in two seconds… and took the order." |
| 3 | `3.m4a` | 7.7 s | **1.4 s** | Arabic messages | "In English, or Arabic." |
| 4 | `4.m4a` | 9.4 s | **2.6 s** | Sunrise, 7:30, notifications | "You woke up to three new orders." |
| 5 | `5.m4a` | 12.2 s | **2.2 s** | End card | "Comment 'AI' to get yours." |

**How to say it:** calm, warm and a little "secret-sharing", like late-night storytelling. Lift the energy slightly on lines 4–5. Smile on line 5; people can hear it.

## Arabic script, Gulf dialect (اللهجة الخليجية)

| # | File | Plays at | Max length | Scene on screen | Say |
|---|---|---|---|---|---|
| 1 | `1.m4a` | 0.3 s | **2.8 s** | الليل والجوال يهتز | «ثنتين بالليل… وعميل راسل محلك.» |
| 2 | `2.m4a` | 3.5 s | **4.0 s** | رد الذكاء الاصطناعي | «مساعدك الذكي ردّ في ثانيتين… وأخذ الطلب.» |
| 3 | `3.m4a` | 7.7 s | **1.4 s** | الرسائل بالعربي | «بالعربي والإنجليزي.» |
| 4 | `4.m4a` | 9.4 s | **2.6 s** | الصباح والإشعارات | «وصحيت على ثلاث طلبات جديدة.» |
| 5 | `5.m4a` | 12.2 s | **2.2 s** | البطاقة الختامية | «علّق AI… ونجهّزه لك.» |

**طريقة الأداء:** هادئة ودافئة كأنك تحكي قصة في آخر الليل، ثم طاقة أعلى قليلًا في السطرين 4 و5. تكلّم بلهجة خليجية طبيعية، لا بالفصحى الرسمية.
**Please check:** have a native Gulf speaker confirm the wording sounds natural before recording.

---

## Option A: record it yourself (best for trust; a real voice from your team)
1. **Where:** a quiet, small room with soft furniture (a bedroom or a car works well). Turn off the AC and fans.
2. **What to use:** your phone's **voice recorder** (Voice Memos on iPhone, Recorder on Android). Hold it **20–25 cm** from your mouth, slightly to the side.
3. **Each line:** record it as a **separate file**. Leave half a second of silence before and after (the mixer trims it). Do 2–3 takes and keep the best.
4. **Length:** time yourself. Each line must fit its **Max length**. If it's too long, speak a bit faster; don't cut words.
5. **Name the files** `1`–`5` (any format: .m4a, .mp3 or .wav) and put them here:
   - English: `tools/instagram/voice/r10/en/1.m4a … 5.m4a`
   - Arabic: `tools/instagram/voice/r10/ar/1.m4a … 5.m4a`

## Option B: ElevenLabs (AI voice)
1. **Voices:** English, a warm conversational voice (e.g. a "narration" or "conversational" voice). Arabic, pick a voice that handles **Gulf Arabic**, and paste the Arabic lines exactly as written.
2. **Settings:** Stability ≈ 45%, Similarity ≈ 75%, Style ≈ 20%. Generate **each line separately**, download each as MP3, and name them `1.mp3`–`5.mp3` in the same folders as above.
3. **Rights:** you need a paid plan for commercial use. On the free plan you must credit ElevenLabs.

---

## Mixing (after the files are in place)
Tell me "voice files are ready" and I'll run it. Or run it yourself (you need ffmpeg):
```
python tools/instagram/mix_voiceover.py <path-to-ffmpeg.exe> r10 en
python tools/instagram/mix_voiceover.py <path-to-ffmpeg.exe> r10 ar
```

**What it does:**
1. **Checks** each line's spoken length against its slot and warns if one is too long.
2. **Places** every line on its cue, trims silence, removes low rumble and evens out the volume.
3. **Ducks** the music under the voice automatically.
4. **Sets loudness** to −14 LUFS, the Instagram/TikTok level.

**Output:** `out/reel-r10-ai-voice-en.mp4` and `out/reel-r10-ai-voice-ar.mp4`

**Posting:** English version for Dubai / Abu Dhabi / India, Arabic version for Riyadh / KSA (or post both on different days). Keep the on-screen captions as they are; they're already bilingual.

---

## Generated version (done)
Both narrated Reels have been made with Microsoft neural voices:

| File | Voice | Notes |
|---|---|---|
| `out/reel-r10-ai-voice-en.mp4` | en-US-AndrewNeural ("warm, confident") | All lines at normal speed |
| `out/reel-r10-ai-voice-ar.mp4` | ar-AE-HamdanNeural (UAE male) | Arabic lines shortened slightly to fit; lines 1 and 5 are up to 15% faster |

**Regenerate:**
```
node tools/instagram/tts_voiceover.mjs <node_modules> r10 en|ar
python tools/instagram/mix_voiceover.py <ffmpeg.exe> r10 en|ar
```
`tts_voiceover.mjs` sends the script text to Microsoft's speech service. To swap in your own recordings later, replace the files in `voice/r10/<lang>/` and run only the mixer.
**Note:** the AI voice reads the Gulf words, but its accent is closer to standard Arabic. If you want a truly local feel for KSA, a human Gulf voice will sound better.
