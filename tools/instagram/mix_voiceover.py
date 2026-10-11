"""Mixes recorded voice-over lines into an animated Reel.

Each line (5 per reel, 8 for R3) is recorded as its own file (any format ffmpeg reads: m4a, mp3, wav, ogg ...) and named by its line number:
    tools/instagram/voice/r10/en/1.m4a ... 5.m4a
    tools/instagram/voice/r10/ar/1.m4a ... 5.m4a
The mixer places every line at its cue time, cleans it up (high-pass + gentle compression), ducks the music under the
voice, normalises to -14 LUFS (Instagram / TikTok level) and muxes it onto the silent video.

Run:  python tools/instagram/mix_voiceover.py <path-to-ffmpeg.exe> r10 en
      python tools/instagram/mix_voiceover.py <path-to-ffmpeg.exe> r10 ar
Out:  tools/instagram/out/reel-r10-ai-voice-en.mp4 (or -ar)
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# reel -> (base name in out/, {line number: (cue start s, slot end s)}) -- slots match the VOICEOVER-<reel>.md files
REELS = {
    'r3': ('reel-r3-signs', {1: (0.3, 2.3), 2: (2.6, 4.9), 3: (5.2, 7.5), 4: (7.8, 10.1), 5: (10.4, 12.7),
                             6: (13.0, 15.4), 7: (15.6, 17.5), 8: (17.8, 19.9)}),
    'r7': ('reel-r7-web', {1: (0.3, 2.4), 2: (2.5, 4.3), 3: (4.6, 7.3), 4: (7.6, 10.6), 5: (10.75, 13.0)}),
    'r9': ('reel-r9-app', {1: (0.3, 2.5), 2: (2.8, 7.2), 3: (7.6, 9.8), 4: (10.0, 13.0), 5: (13.4, 15.8)}),
    'r10': ('reel-r10-ai', {1: (0.3, 3.1), 2: (3.5, 7.5), 3: (7.7, 9.1), 4: (9.4, 12.0), 5: (12.2, 14.4)}),
    'r12': ('reel-r12-dev', {1: (0.3, 2.1), 2: (2.4, 5.5), 3: (5.8, 8.9), 4: (9.3, 12.4), 5: (12.8, 14.9)}),
    'r14': ('reel-r14-crm', {1: (0.3, 2.6), 2: (2.75, 4.5), 3: (5.4, 8.3), 4: (8.5, 11.3), 5: (11.7, 13.9)}),
}


TRIM = ('silenceremove=start_periods=1:start_threshold=-45dB,areverse,'
        'silenceremove=start_periods=1:start_threshold=-45dB,areverse')  # cut silence at both ends


def duration(ffmpeg, f):
    """Spoken length of a recording, ignoring silence before and after."""
    err = subprocess.run([ffmpeg, '-i', str(f), '-af', TRIM, '-f', 'null', '-'], capture_output=True, text=True).stderr
    h, m, s = re.findall(r'time=(\d+):(\d+):([\d.]+)', err)[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


def duration_raw(ffmpeg, f):
    """Full length of a media file in seconds."""
    err = subprocess.run([ffmpeg, '-i', str(f)], capture_output=True, text=True).stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def main():
    if len(sys.argv) != 4 or sys.argv[2] not in REELS:
        sys.exit(__doc__)
    ffmpeg, reel, lang = sys.argv[1], sys.argv[2], sys.argv[3]
    base, cues = REELS[reel]
    out = HERE / 'out'
    video, music = out / f'{base}-silent.mp4', out / f'{base}.wav'
    for f in (video, music):
        if not f.exists():
            sys.exit(f'missing {f} -- render the reel first')

    vdir = HERE / 'voice' / reel / lang
    lines = {}
    for n in cues:
        found = sorted(vdir.glob(f'{n}.*'))
        if not found:
            sys.exit(f'missing voice line {n}: put it in {vdir} as {n}.m4a / .mp3 / .wav')
        lines[n] = found[0]

    # warn when a line runs past its slot (it still plays; it just overlaps the next scene)
    for n, f in lines.items():
        start, end = cues[n]
        d = duration(ffmpeg, f)
        flag = '  <-- too long, speak a little faster or trim the silence' if start + d > end + 0.25 else ''
        print(f'line {n}: {d:4.1f}s, slot {end - start:4.1f}s{flag}')

    args = [ffmpeg, '-y', '-loglevel', 'error', '-i', str(music)]
    for n in cues:
        args += ['-i', str(lines[n])]
    chains, labels = [], []
    for i, n in enumerate(cues, start=1):
        ms = int(cues[n][0] * 1000)
        # trim silence, clean up, then delay to the cue
        chains.append(f'[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo,'
                      f'{TRIM},highpass=f=80,'
                      f'acompressor=threshold=-20dB:ratio=3:attack=5:release=120,adelay={ms}|{ms}[v{i}]')
        labels.append(f'[v{i}]')
    # pad the voice bus to the full reel length: sidechaincompress stops when its key input ends
    total = duration_raw(ffmpeg, music)
    chains.append(f'{"".join(labels)}amix=inputs={len(labels)}:normalize=0,volume=1.6,apad=whole_dur={total},asplit=2[voice][key]')
    chains.append('[0:a]volume=0.55[mus]')
    chains.append('[mus][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[ducked]')
    chains.append('[ducked][voice]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1:LRA=11[mix]')
    mix_wav = out / f'{base}-voice-{lang}.wav'
    subprocess.run(args + ['-filter_complex', ';'.join(chains), '-map', '[mix]', '-ar', '44100', str(mix_wav)], check=True)

    final = out / f'{base}-voice-{lang}.mp4'
    subprocess.run([ffmpeg, '-y', '-loglevel', 'error', '-i', str(video), '-i', str(mix_wav), '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', str(final)], check=True)
    mix_wav.unlink()
    print('wrote', final.relative_to(HERE.parents[1]))


if __name__ == '__main__':
    main()
