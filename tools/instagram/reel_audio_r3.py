"""Original soundtrack for Reel R3 "5 signs your shop needs a real POS" (20 s), timed to reel-r3-signs.html.
Signs (0-15.4 s): punchy minor beat (Am - F - C - G, 100 BPM); each sign gets a whoosh + impact, a "fail" thud, its own
effect (clock, buzzer, coins + error, paper flutter, phone ring) and a "fix" chime. Reveal (15.4 s on): bright major beat
with rising check chimes, then the end-card hit.

Run: python tools/instagram/reel_audio_r3.py   ->  tools/instagram/out/reel-r3-signs.wav
"""
from pathlib import Path
import numpy as np
from reel_audio import Mix, SR, tt, env, lowpass, pad, keys, bass, kick, ding, pop, sparkle, boom, tick

DUR = 20.0
OUT = Path(__file__).resolve().parent / 'out' / 'reel-r3-signs.wav'
mix = Mix(DUR, seed=3)
SIGNS = [2.4, 5.0, 7.6, 10.2, 12.8]
REVEAL = 15.4


def thud():  # "fail" hit
    t = tt(0.35)
    return 0.6 * np.where((t * 98) % 1 < 0.5, 1.0, -1.0) * np.exp(-t * 12) + np.sin(2 * np.pi * 62 * t) * np.exp(-t * 9)


def buzzer(sec=0.5):
    t = tt(sec)
    return np.where((t * 160) % 1 < 0.5, 1.0, -1.0) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 7 * t))) * env(len(t), 0.01, 0.05)


def coin():
    t = tt(0.25)
    return (np.sin(2 * np.pi * 2637 * t) + 0.6 * np.sin(2 * np.pi * 3520 * t)) * np.exp(-t * 18)


def ring(sec=0.9):  # phone ring: two-tone warble in bursts
    t = tt(sec)
    tone = np.sin(2 * np.pi * 1200 * t) + np.sin(2 * np.pi * 1500 * t)
    return tone * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 20 * t))) * (np.sin(np.pi * t / sec) > 0.2) * 0.5


def flutter():
    n = mix.noise(int(0.25 * SR))
    return (lowpass(n, 3500) - lowpass(n, 900)) * np.exp(-tt(0.25) * 10)


# ---------------- music ----------------
BEAT = 60 / 100
BAR = 4 * BEAT
MINOR = [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [43, 47, 50, 55]]
MAJOR = [[48, 52, 55, 60], [43, 47, 50, 55], [45, 48, 52, 57], [41, 45, 48, 53]]
for b in range(int(DUR / BAR) + 1):
    start = b * BAR
    bright = start >= REVEAL - 0.1
    chord = (MAJOR if bright else MINOR)[b % 4]
    mix.add(pad(chord, BAR + 0.9, 1.0 if bright else 0.5), start, 0.15)
    mix.add(bass(chord[0] - 12, BAR), start, 0.13)
    for k in range(8):
        at = start + k * BEAT / 2
        if at > DUR - 0.8:
            break
        mix.add(keys(chord[[0, 2, 1, 3, 2, 1, 3, 2][k]] + (24 if bright else 12), 0.6), at, 0.07, pan=-0.3 if k % 2 else 0.3)
    for k in range(4):
        at = start + k * BEAT
        if at < 0.05 or at > DUR - 0.8:
            continue
        mix.add(kick(), at, 0.30)
        if k in (1, 3):
            mix.add(mix.snare(), at, 0.11)
        mix.add(mix.hat(), at + BEAT / 2, 0.05, pan=0.4)

# ---------------- hook ----------------
mix.add(boom(), 0.05, 0.5)                              # the "5" slams in
mix.add(mix.whoosh(0.4), 0.3, 0.18)

# ---------------- signs ----------------
for i, at in enumerate(SIGNS):
    mix.add(mix.whoosh(0.35), at - 0.2, 0.22)           # scene in
    mix.add(boom(), at, 0.28)                           # number slams
    mix.add(thud(), at + 0.3, 0.22)                     # "fail"
    mix.add(ding(1046.5, 1568), at + 1.45, 0.20)        # THE FIX
for k in range(14):                                     # 1 · queue: clock racing
    mix.add(tick(), SIGNS[0] + 0.2 + k * 0.1, 0.18, pan=0.4)
mix.add(buzzer(), SIGNS[1] + 0.5, 0.06)                 # 2 · out of stock
for k in range(6):                                      # 3 · cash: coins counting, then error
    mix.add(coin(), SIGNS[2] + 0.15 + k * 0.12, 0.10, pan=mix.rng.uniform(-0.4, 0.4))
mix.add(buzzer(0.35), SIGNS[2] + 0.95, 0.06)
for k in range(7):                                      # 4 · VAT: receipts flutter down
    mix.add(flutter(), SIGNS[3] + k * 0.18, 0.18, pan=mix.rng.uniform(-0.5, 0.5))
mix.add(ring(), SIGNS[4] + 0.1, 0.08)                   # 5 · calling the shop
mix.add(ring(), SIGNS[4] + 1.1, 0.06)

# ---------------- reveal + end ----------------
mix.add(mix.whoosh(0.5), REVEAL - 0.3, 0.25)
mix.add(boom(), REVEAL, 0.4)
mix.add(sparkle(), REVEAL + 0.05, 0.18)
for i in range(5):                                      # checks
    mix.add(ding(1046.5 * 2 ** (i * 2 / 12), 1568 * 2 ** (i * 2 / 12)), REVEAL + 0.7 + i * 0.18, 0.12)
mix.add(mix.whoosh(0.5), 17.35, 0.22)
mix.add(boom(), 17.6, 0.42)
mix.add(sparkle(), 17.65, 0.15)

mix.write(OUT)
