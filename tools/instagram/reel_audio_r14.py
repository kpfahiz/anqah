"""Original soundtrack for Reel R14 "Excel chaos vs. CRM calm" (14 s), timed to reel-r14-crm.html.
Chaos (0-4.6 s): tense drone, an accelerating clock, pings, sticky-note slaps and keyboard clatter.
Calm (5 s on): bright lo-fi in C major with effects for the stats, the card drag, the win and the reminders.

Run: python tools/instagram/reel_audio_r14.py   ->  tools/instagram/out/reel-r14-crm.wav
"""
from pathlib import Path
from reel_audio import Mix, pad, keys, bass, kick, ding, buzz, pop, sparkle, boom, tick, drone

DUR = 14.0
OUT = Path(__file__).resolve().parent / 'out' / 'reel-r14-crm.wav'
mix = Mix(DUR, seed=14)
CALM = 5.0

# ---------------- chaos ----------------
mix.add(drone(38, 4.9, wobble=0.25), 0.0, 0.22)               # low D, uneasy
mix.add(drone(44, 3.0, wobble=0.35), 1.9, 0.12)               # tension rises
at, gap = 0.2, 0.5
while at < 4.5:                                                # clock ticks, getting faster
    mix.add(tick(), at, 0.22, pan=0.5)
    at += gap
    gap = max(0.16, gap * 0.9)
for i in range(40):                                            # frantic typing
    mix.add(mix.click(), 0.3 + mix.rng.uniform(0, 4.1), 0.09, pan=mix.rng.uniform(-0.6, 0.6))
for t_ in (0.7, 1.15, 1.6, 2.05, 2.5):                         # sticky notes
    mix.add(mix.slap(), t_, 0.35, pan=mix.rng.uniform(-0.4, 0.4))
mix.add(ding(1318.5, 1760), 1.0, 0.22, pan=0.4)                # "Where is my quote?"
mix.add(ding(1318.5, 1760), 2.0, 0.22, pan=0.4)                # "Any update??"
mix.add(ding(622, 466), 3.2, 0.30, pan=0.4)                    # "I'll go with another company" (falling, sad)
mix.add(buzz(0.5), 3.2, 0.05)

# ---------------- swipe ----------------
mix.add(mix.whoosh(0.5), 4.45, 0.32)
mix.add(sparkle((72, 76, 79, 84)), 4.95, 0.12)

# ---------------- calm music: 92 BPM, Cmaj7 - Am7 - Fmaj7 - G6 ----------------
BEAT = 60 / 92
BAR = 4 * BEAT
CHORDS = [[48, 52, 55, 59], [45, 48, 52, 55], [41, 45, 48, 52], [43, 47, 50, 52]]
for b in range(int((DUR - CALM) / BAR) + 1):
    start = CALM + b * BAR
    chord = CHORDS[b % 4]
    mix.add(pad(chord, BAR + 0.9, 0.9), start, 0.16)
    mix.add(bass(chord[0] - 12, BAR), start, 0.11)
    for k in range(8):
        at = start + k * BEAT / 2
        if at > DUR - 0.8:
            break
        mix.add(keys(chord[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 24), at, 0.075, pan=-0.3 if k % 2 else 0.3)
    for k in range(4):
        at = start + k * BEAT
        if at < CALM + 0.4 or at > DUR - 0.8:
            continue
        mix.add(kick() if k in (0, 2) else mix.snare(), at, 0.30 if k in (0, 2) else 0.09)
        mix.add(mix.hat(), at + BEAT / 2, 0.05, pan=0.4)

# ---------------- calm effects ----------------
for i in range(10):                                            # stats counting up
    mix.add(tick(), 5.3 + i * 0.1, 0.10, pan=-0.3 + i * 0.06)
for at in (6.58, 7.08, 7.58):                                  # card lifted and moved
    mix.add(mix.whoosh(0.3), at, 0.16, pan=0.2)
for at in (7.0, 7.5):
    mix.add(pop(700), at, 0.22)
mix.add(pop(900), 8.0, 0.30)                                   # dropped in "Won"
mix.add(ding(1568, 2093), 8.02, 0.25)
mix.add(sparkle(), 8.05, 0.18)
for i in range(12):                                            # confetti
    mix.add(pop(1400 + mix.rng.uniform(0, 900)), 8.05 + mix.rng.uniform(0, 0.6), 0.04, pan=mix.rng.uniform(-0.8, 0.8))
for at, f in ((9.0, (1046.5, 1318.5)), (9.9, (1174.7, 1568)), (10.7, (1318.5, 1760))):
    mix.add(ding(*f), at, 0.18, pan=0.2)                       # reminder toasts
mix.add(mix.whoosh(0.5), 11.4, 0.25)                           # -> end card
mix.add(boom(), 11.65, 0.45)
mix.add(sparkle(), 11.7, 0.16)

mix.write(OUT)
