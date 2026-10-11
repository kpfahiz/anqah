"""Original soundtrack for Reel R10 "AI replies at 2 am" (14.5 s): a dreamy lo-fi beat plus sound effects timed to
reel-r10-ai.html. Built with the shared synthesiser in reel_audio.py (royalty-free).

Run: python tools/instagram/reel_audio_r10.py   ->  tools/instagram/out/reel-r10-ai.wav
Then mux with render_reel.mjs (it picks up out/<page-name>.wav automatically).
"""
from pathlib import Path
from reel_audio import Mix, pad, keys, bass, kick, ding, buzz, pop, sparkle, chirp, boom

DUR = 14.5
OUT = Path(__file__).resolve().parent / 'out' / 'reel-r10-ai.wav'
mix = Mix(DUR)

# ---------------- music: 90 BPM, Fmaj7 - Em7 - Dm7 - Cmaj7 ----------------
BEAT = 60 / 90
BAR = 4 * BEAT
CHORDS = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
MORNING = 9.0

for b in range(int(DUR / BAR) + 1):
    start = b * BAR
    chord = CHORDS[b % 4]
    mix.add(pad(chord, BAR + 0.9, 1.0 if start >= MORNING - BAR / 2 else 0.4), start, 0.16)
    mix.add(bass(chord[0] - 12, BAR), start, 0.10)
    for k in range(8):  # lazy arpeggio, an octave higher after sunrise
        at = start + k * BEAT / 2
        if at > DUR - 0.8:
            break
        note = chord[[0, 2, 1, 3, 2, 1, 3, 2][k]] + (24 if at >= MORNING else 12)
        mix.add(keys(note), at, 0.07 if at < MORNING else 0.08, pan=-0.3 if k % 2 else 0.3)
    for k in range(4):  # beat comes in after the hook
        at = start + k * BEAT
        if at < 3.2 or at > DUR - 0.8:
            continue
        mix.add(kick() if k in (0, 2) else mix.snare(), at, 0.32 if k in (0, 2) else 0.10)
        mix.add(mix.hat(), at + BEAT / 2, 0.05, pan=0.4)
mix.crackle(0, MORNING, 220)

# ---------------- sound effects ----------------
mix.add(ding(1318.5, 1760), 1.0, 0.30)             # message arrives on the lock screen
mix.add(buzz(), 1.0, 0.05)                          # phone vibrates
mix.add(mix.whoosh(0.45), 3.0, 0.22)                # lock screen -> chat
mix.add(pop(520), 3.4, 0.30, pan=-0.2)              # customer bubble
for k in range(8):
    mix.add(mix.click(), 3.9 + k * 0.085, 0.10, pan=0.25)  # AI typing
mix.add(pop(820), 4.6, 0.30, pan=0.2)               # AI bubble
mix.add(sparkle(), 4.75, 0.16, pan=0.3)             # "2s reply" badge
mix.add(pop(520), 5.9, 0.30, pan=-0.2)
for k in range(8):
    mix.add(mix.click(), 6.3 + k * 0.085, 0.10, pan=0.25)
mix.add(pop(820), 7.0, 0.30, pan=0.2)
mix.add(sparkle(), 7.9, 0.14)                       # order confirmed
mix.add(mix.whoosh(0.7), 8.8, 0.20)                 # night -> morning
for at, p in [(9.3, -0.6), (9.45, -0.6), (10.0, 0.6), (10.12, 0.6), (11.0, -0.4)]:
    mix.add(chirp(), at, 0.06, pan=p)               # morning birds
for at in (9.7, 10.15, 10.6):
    mix.add(ding(1568, 2093), at, 0.18)             # overnight order notifications
mix.add(mix.whoosh(0.5), 11.75, 0.25)               # -> end card
mix.add(boom(), 12.0, 0.45)
mix.add(sparkle(), 12.05, 0.16)

mix.write(OUT)
