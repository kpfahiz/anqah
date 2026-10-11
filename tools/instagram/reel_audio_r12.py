"""Original soundtrack for Reel R12 "A dashboard from zero" (15 s), timed to reel-r12-dev.html.
Cool lo-fi tech beat (Am9 - Fmaj7 - C - G, 100 BPM), keyboard typing while the code writes itself, pops as each dashboard
component appears, mouse clicks for the filter / language toggle, and an end-card hit.

Run: python tools/instagram/reel_audio_r12.py   ->  tools/instagram/out/reel-r12-dev.wav
"""
from pathlib import Path
from reel_audio import Mix, pad, keys, bass, kick, pop, sparkle, boom, tick

DUR = 15.0
OUT = Path(__file__).resolve().parent / 'out' / 'reel-r12-dev.wav'
mix = Mix(DUR, seed=12)

# same code + timing as reel-r12-dev.html, so the pops land when each component appears
CODE = '''import { Layout, Stats, Chart, Table } from "./ui";

export default function Dashboard() {
  const sales = useLiveSales();
  return (
    <Layout title="Sales Dashboard" lang={lang}>
      <Stats revenue={sales.total} orders={sales.count} />
      <LineChart data={sales.daily} />
      <BarChart data={sales.byBranch} />
      <Table rows={sales.latest} />
    </Layout>
  );
}'''
TYPE_A, TYPE_B = 2.0, 8.6


def shows(marker):
    end = CODE.index('\n', CODE.index(marker))
    return TYPE_A + (TYPE_B - TYPE_A) * end / len(CODE)


# ---------------- music ----------------
BEAT = 60 / 100
BAR = 4 * BEAT
CHORDS = [[57, 60, 64, 67, 71], [53, 57, 60, 64], [48, 52, 55, 59], [43, 47, 50, 55]]
for b in range(int(DUR / BAR) + 1):
    start = b * BAR
    chord = CHORDS[b % 4]
    mix.add(pad(chord, BAR + 0.9, 0.6), start, 0.15)
    mix.add(bass(chord[0] - 24, BAR), start, 0.12)
    for k in range(8):
        at = start + k * BEAT / 2
        if at < TYPE_A or at > DUR - 0.8:
            continue
        mix.add(keys(chord[[0, 2, 1, 3, 2, 1, 3, 2][k % 8] % len(chord)] + 12), at, 0.06, pan=-0.35 if k % 2 else 0.35)
    for k in range(4):
        at = start + k * BEAT
        if at < TYPE_A or at > DUR - 0.8:
            continue
        mix.add(kick() if k in (0, 2) else mix.snare(), at, 0.30 if k in (0, 2) else 0.09)
        mix.add(mix.hat(), at + BEAT / 2, 0.05, pan=0.4)
        mix.add(mix.hat(), at + BEAT * 0.75, 0.025, pan=-0.4)

# ---------------- effects ----------------
for at in (0.4, 0.85, 1.3, 1.75):                       # blinking caret in the empty editor
    mix.add(tick(), at, 0.06)
at = TYPE_A
while at < TYPE_B:                                      # keyboard typing (8x speed)
    mix.add(mix.click(), at, 0.11, pan=mix.rng.uniform(-0.3, 0.3))
    at += mix.rng.uniform(0.045, 0.09)
for marker in ('<Layout', '<Stats', '<LineChart', '<BarChart', '<Table'):
    mix.add(pop(680), shows(marker), 0.26)              # component appears in the browser
mix.add(sparkle((79, 84, 88, 91)), shows('<LineChart') + 0.1, 0.08)
mix.add(mix.whoosh(0.5), 8.9, 0.25)                     # editor slides away, dashboard expands
for at in (10.4, 11.6):                                 # mouse clicks
    mix.add(mix.click(), at, 0.35)
    mix.add(pop(1100), at + 0.01, 0.18)
mix.add(sparkle((76, 79, 84, 88)), 10.45, 0.12)         # charts update to "This month"
mix.add(mix.whoosh(0.35), 11.62, 0.18)                  # switch to Arabic
mix.add(sparkle(), 11.7, 0.12)
mix.add(mix.whoosh(0.5), 12.35, 0.25)                   # -> end card
mix.add(boom(), 12.65, 0.45)
mix.add(sparkle(), 12.7, 0.16)

mix.write(OUT)
