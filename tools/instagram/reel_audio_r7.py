"""Original soundtrack for Reel R7 "Website glow-up: 2015 vs 2026" (13 s), timed to reel-r7-web.html.
2015 (0-3.6 s): cheesy 8-bit chiptune loop with an error "thud" for each red stamp, then a tape-stop.
Glow-up (3.6-4.4 s): rising whoosh + sparkle. 2026 (4.4 s on): warm modern beat (Dmaj7 - Bm7 - Gmaj7 - A6, 96 BPM)
with pops for the badges and an end-card hit.

Run: python tools/instagram/reel_audio_r7.py   ->  tools/instagram/out/reel-r7-web.wav
"""
from pathlib import Path
import numpy as np
from reel_audio import Mix, SR, tt, env, hz, pad, keys, bass, kick, pop, sparkle, boom

DUR = 13.0
OUT = Path(__file__).resolve().parent / 'out' / 'reel-r7-web.wav'
mix = Mix(DUR, seed=7)
NEW = 4.4


def square(note, sec, duty=0.5):
    t = tt(sec)
    return np.where((t * hz(note)) % 1 < duty, 1.0, -1.0) * np.exp(-t * 5) * env(len(t), 0.002, 0.02)


def thud():  # "error" stamp: low square blip + body
    t = tt(0.3)
    return 0.6 * np.where((t * 110) % 1 < 0.5, 1.0, -1.0) * np.exp(-t * 14) + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 10)


def tape_stop(sec=0.45):  # pitch falls like a tape slowing down
    t = tt(sec)
    f = 330 * (1 - t / sec) ** 2 + 30
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), 0.01, 0.1)


# ---------------- 2015: chiptune ----------------
STEP = 0.25  # eighth notes at 120 BPM
MELODY = [72, 76, 79, 76, 74, 77, 81, 77, 72, 76, 79, 84, 83, 79, 76, 74]
for i in range(14):
    at = 0.1 + i * STEP
    mix.add(square(MELODY[i % len(MELODY)], 0.22, 0.25), at, 0.05, pan=0.15)
    if i % 2 == 0:
        mix.add(square([48, 48, 53, 55][(i // 4) % 4], 0.24), at, 0.06, pan=-0.15)
for at in (1.3, 2.0, 2.7):
    mix.add(thud(), at, 0.32)
mix.add(tape_stop(), 3.45, 0.18)

# ---------------- glow-up ----------------
mix.add(mix.whoosh(0.8), 3.55, 0.30)
mix.add(sparkle((79, 84, 88, 91, 96)), 3.95, 0.22)

# ---------------- 2026: warm modern beat ----------------
BEAT = 60 / 96
BAR = 4 * BEAT
CHORDS = [[50, 54, 57, 61], [47, 50, 54, 57], [43, 47, 50, 54], [45, 49, 52, 54]]
for b in range(int((DUR - NEW) / BAR) + 1):
    start = NEW + b * BAR
    chord = CHORDS[b % 4]
    mix.add(pad(chord, BAR + 0.9, 1.0), start, 0.16)
    mix.add(bass(chord[0] - 12, BAR), start, 0.12)
    for k in range(8):
        at = start + k * BEAT / 2
        if at > DUR - 0.8:
            break
        mix.add(keys(chord[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 24), at, 0.07, pan=-0.3 if k % 2 else 0.3)
    for k in range(4):
        at = start + k * BEAT
        if at > DUR - 0.8:
            continue
        mix.add(kick() if k in (0, 2) else mix.snare(), at, 0.32 if k in (0, 2) else 0.10)
        mix.add(mix.hat(), at + BEAT / 2, 0.05, pan=0.4)

# ---------------- 2026 effects ----------------
mix.add(mix.whoosh(0.6), 5.2, 0.12)                   # smooth scroll
mix.add(mix.whoosh(0.4), 6.55, 0.18, pan=0.4)         # phone slides in
mix.add(pop(760), 6.95, 0.20, pan=0.4)
for i, at in enumerate((7.7, 8.1, 8.5, 8.9)):         # badges
    mix.add(pop(640 + i * 120), at, 0.24, pan=-0.3)
mix.add(mix.whoosh(0.5), 10.55, 0.24)                  # -> end card
mix.add(boom(), 10.85, 0.45)
mix.add(sparkle(), 10.9, 0.16)

mix.write(OUT)
