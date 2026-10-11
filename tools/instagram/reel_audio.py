"""Shared synthesiser for the Reel soundtracks (reel_audio_r10.py, reel_audio_r14.py, ...).

Everything is generated from scratch with numpy, so the music and effects are original and royalty-free.
A score creates a Mix, places instruments / effects with mix.add(signal, at_seconds, gain, pan) and calls mix.write().
"""
from pathlib import Path
import wave
import numpy as np

SR = 44100


def tt(sec):
    return np.arange(int(SR * sec)) / SR


def env(n, a=0.01, r=0.2):
    """Linear attack / release envelope over n samples."""
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for k in range(len(x)):  # one-pole filter; only used on short signals
        acc = (1 - a) * x[k] + a * acc
        y[k] = acc
    return y


def hz(note):
    return 440 * 2 ** ((note - 69) / 12)


class Mix:
    def __init__(self, duration, seed=7):
        self.n = int(SR * duration)
        self.L, self.R = np.zeros(self.n), np.zeros(self.n)
        self.rng = np.random.default_rng(seed)

    def add(self, sig, at, gain=1.0, pan=0.0):
        """Mix a mono signal in at `at` seconds; pan -1 (left) .. 1 (right)."""
        i = int(at * SR)
        if i >= self.n or i < 0:
            return
        sig = sig[:self.n - i] * gain
        self.L[i:i + len(sig)] += sig * np.sqrt((1 - pan) / 2)
        self.R[i:i + len(sig)] += sig * np.sqrt((1 + pan) / 2)

    def write(self, path, fade=0.7):
        """RMS-normalise, soft-limit, fade out and save a 16-bit stereo WAV (about -14 LUFS once muxed)."""
        f = int(fade * SR)
        for ch in (self.L, self.R):
            ch[-f:] *= np.linspace(1, 0, f)
        st = np.stack([self.L, self.R], axis=1)
        st /= np.sqrt((st ** 2).mean())
        st = np.tanh(st * 0.16) / np.tanh(1.0)
        st *= 0.89 / np.abs(st).max()
        path = Path(path)
        path.parent.mkdir(exist_ok=True)
        with wave.open(str(path), 'wb') as w:
            w.setnchannels(2)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((st * 32767).astype('<i2').tobytes())
        print('wrote', path.relative_to(path.parents[2]))

    # ---------------- noise-based sounds need the mix's random generator ----------------
    def noise(self, n):
        return self.rng.standard_normal(n)

    def hat(self):
        n = self.noise(int(0.05 * SR))
        return (n - lowpass(n, 6000)) * np.exp(-tt(0.05) * 70)

    def snare(self):
        t = tt(0.18)
        return 0.5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) + 0.8 * lowpass(self.noise(len(t)), 4500) * np.exp(-t * 22)

    def whoosh(self, sec=0.5):
        t = tt(sec)
        n = self.noise(len(t))
        out = np.zeros_like(n)
        for i, c in enumerate(np.linspace(400, 5000, 6)):
            seg = slice(i * len(t) // 6, (i + 1) * len(t) // 6)
            out[seg] = lowpass(n[seg], c)
        return out * np.sin(np.pi * t / sec) ** 2

    def click(self):
        t = tt(0.02)
        return lowpass(self.noise(len(t)), 3000) * np.exp(-t * 300)

    def crackle(self, start, end, count, gain=0.015):
        for _ in range(count):
            self.add(self.noise(40) * np.exp(-np.arange(40) / 6), self.rng.uniform(start, end), gain, pan=self.rng.uniform(-1, 1))

    def slap(self):  # sticky note hitting the screen
        t = tt(0.09)
        return lowpass(self.noise(len(t)), 1800) * np.exp(-t * 60) + 0.4 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 50)


# ---------------- tonal instruments ----------------
def pad(notes, sec, bright, octave=12):
    t = tt(sec)
    s = np.zeros_like(t)
    for n in notes:
        f = hz(n + octave)
        for det in (-0.12, 0.12):
            ff = f * 2 ** (det / 12)
            s += np.sin(2 * np.pi * ff * t) + 0.25 * np.sin(4 * np.pi * ff * t) * bright
    return s / (len(notes) * 2) * env(len(t), a=0.6, r=0.9)


def keys(note, sec=1.2):
    t = tt(sec)
    f = hz(note)
    s = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 6) + 0.1 * np.sin(2 * np.pi * 3 * f * t)
    return s * np.exp(-t * 3.2) * env(len(t), a=0.004, r=0.05)


def bass(note, sec):
    return np.sin(2 * np.pi * hz(note) * tt(sec)) * env(int(sec * SR), 0.05, 0.4)


def kick():
    t = tt(0.35)
    f = 45 + 80 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def ding(f1, f2):
    t = tt(0.6)
    s = np.sin(2 * np.pi * f1 * t) * np.exp(-t * 9)
    s2 = np.sin(2 * np.pi * f2 * t) * np.exp(-np.clip(t - 0.09, 0, None) * 9) * (t > 0.09)
    return s + s2


def buzz(sec=0.6):
    t = tt(sec)
    return np.sign(np.sin(2 * np.pi * 150 * t)) * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 9 * t))) * env(len(t), 0.01, 0.05)


def pop(f=600):
    t = tt(0.12)
    return np.sin(2 * np.pi * (f + 500 * np.exp(-t * 60)) * t) * np.exp(-t * 35)


def sparkle(notes=(84, 88, 91, 96)):
    s = np.zeros(int(0.7 * SR))
    for i, n in enumerate(notes):
        seg = keys(n, 0.6)
        j = int(i * 0.05 * SR)
        s[j:j + len(seg)] += seg[:len(s) - j]
    return s


def chirp():
    t = tt(0.12)
    f = 3200 + 1400 * np.sin(np.pi * t / 0.12)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 0.12)


def boom():
    t = tt(1.4)
    f = 40 + 60 * np.exp(-t * 8)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.5)


def tick():  # clock tick
    t = tt(0.03)
    return np.sin(2 * np.pi * 2600 * t) * np.exp(-t * 220)


def drone(note, sec, wobble=0.0):
    """Low, slightly detuned tension tone."""
    t = tt(sec)
    f = hz(note)
    s = np.sin(2 * np.pi * f * t) + 0.6 * np.sin(2 * np.pi * f * 1.06 * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return s * (1 + wobble * np.sin(2 * np.pi * 6 * t)) * env(len(t), 0.4, 0.3) / 2
