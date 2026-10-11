"""Original soundtrack for Reel R9 "Idea -> App in 4 steps" (16 s), timed to reel-r9-app.html.
Napkin (0-2.6 s): pen scribbles over a soft intro. Then a playful pop beat (C - G - Am - F, 104 BPM) with a level-up chime
for each step, typing for the code, dings for the checks, a rising install tick, a celebration and an end-card hit.

Run: python tools/instagram/reel_audio_r9.py   ->  tools/instagram/out/reel-r9-app.wav
"""
from pathlib import Path
import numpy as np
from reel_audio import Mix, SR, tt, env, lowpass, pad, keys, bass, kick, ding, pop, sparkle, boom, tick

DUR = 16.0
OUT = Path(__file__).resolve().parent / 'out' / 'reel-r9-app.wav'
mix = Mix(DUR, seed=9)
BEAT_IN = 2.6


def scribble(sec):
    """Pen on paper: band-limited noise with stroke-like bursts."""
    n = mix.noise(int(sec * SR))
    band = lowpass(n, 5500) - lowpass(n, 1800)
    t = tt(sec)
    strokes = 0.5 + 0.5 * np.sin(2 * np.pi * (5 + 3 * np.sin(2 * np.pi * 0.7 * t)) * t)
    return band * strokes ** 2 * env(len(t), 0.03, 0.05)


def level_up(root):
    """Quick rising arpeggio for each new step."""
    s = np.zeros(int(0.5 * SR))
    for i, n in enumerate((root, root + 4, root + 7, root + 12)):
        seg = keys(n, 0.4)
        j = int(i * 0.06 * SR)
        s[j:j + len(seg)] += seg[:len(s) - j]
    return s


# ---------------- napkin intro ----------------
mix.add(pad([60, 64, 67, 71], 3.2, 0.3), 0.0, 0.12)
for i in range(11):                                   # one scribble per pen stroke (0.15 s apart, 0.3 s long)
    mix.add(scribble(0.3), 0.15 + i * 0.15, 0.22, pan=mix.rng.uniform(-0.3, 0.3))
mix.add(scribble(0.5), 1.7, 0.18)                     # handwriting
mix.add(ding(1568, 2093), 2.0, 0.16)                  # "idea!! 💡"

# ---------------- playful pop beat ----------------
BEAT = 60 / 104
BAR = 4 * BEAT
CHORDS = [[48, 52, 55, 60], [43, 47, 50, 55], [45, 48, 52, 57], [41, 45, 48, 53]]
for b in range(int((DUR - BEAT_IN) / BAR) + 1):
    start = BEAT_IN + b * BAR
    chord = CHORDS[b % 4]
    mix.add(pad(chord, BAR + 0.9, 0.9), start, 0.15)
    mix.add(bass(chord[0] - 12, BAR), start, 0.12)
    for k in range(8):
        at = start + k * BEAT / 2
        if at > DUR - 0.8:
            break
        mix.add(keys(chord[[0, 1, 2, 3, 2, 1, 2, 3][k]] + 24, 0.5), at, 0.07, pan=-0.3 if k % 2 else 0.3)
    for k in range(4):
        at = start + k * BEAT
        if at > DUR - 0.8:
            continue
        mix.add(kick(), at, 0.30)                     # four-on-the-floor, playful
        if k in (1, 3):
            mix.add(mix.snare(), at, 0.10)
        mix.add(mix.hat(), at + BEAT / 2, 0.05, pan=0.4)

# ---------------- steps ----------------
for at, root in ((2.65, 72), (5.05, 74), (7.45, 76), (9.85, 79)):
    mix.add(mix.whoosh(0.35), at - 0.15, 0.16)
    mix.add(level_up(root), at, 0.16)
for i in range(3):                                    # design: colour fills + selection hops
    mix.add(pop(800 + i * 150), (3.0, 3.6, 4.2)[i], 0.18)
at = 5.25
while at < 7.1:                                       # build: typing
    mix.add(mix.click(), at, 0.10, pan=mix.rng.uniform(-0.3, 0.3))
    at += mix.rng.uniform(0.05, 0.09)
mix.add(sparkle((84, 88, 91)), 7.05, 0.10)            # hot reload
for i, at in enumerate((8.2, 8.45, 8.7, 8.95)):       # test: checks
    mix.add(ding(1046.5 + i * 130, 1568 + i * 130), at, 0.12)
mix.add(mix.click(), 10.4, 0.35)                      # launch: tap Install
for i in range(10):                                   # progress ticks rising in pitch
    t = tt(0.03)
    mix.add(np.sin(2 * np.pi * (1400 + i * 120) * t) * np.exp(-t * 200), 10.6 + i * 0.1, 0.12)
mix.add(ding(1568, 2093), 11.6, 0.22)                 # "Open"
mix.add(boom(), 11.72, 0.35)                          # Live!
mix.add(sparkle(), 11.75, 0.18)
for i in range(14):                                   # confetti
    mix.add(pop(1300 + mix.rng.uniform(0, 1000)), 11.75 + mix.rng.uniform(0, 0.7), 0.04, pan=mix.rng.uniform(-0.8, 0.8))
mix.add(mix.whoosh(1.2), 11.9, 0.20)                  # rocket
mix.add(mix.whoosh(0.5), 12.9, 0.22)                  # -> end card
mix.add(boom(), 13.2, 0.40)
mix.add(sparkle(), 13.25, 0.15)

mix.write(OUT)
