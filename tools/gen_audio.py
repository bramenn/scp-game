"""Sintetiza todos los sonidos del juego en art/audio/*.wav (22 kHz, mono, 16 bit).
Uso: python3 tools/gen_audio.py   (requiere numpy)
sfx_*: efectos · amb_*: ambiente en bucle por tema · mus_*: música.
"""
import wave
from pathlib import Path
import numpy as np

SR = 22050
OUT = Path(__file__).resolve().parent.parent / "art/audio"
rng = np.random.default_rng(19)


def t(sec):
    return np.arange(int(round(SR * sec))) / SR


def env(n, a=0.005, r=None):
    """Envolvente ataque lineal + caída exponencial (r = segundos hasta ~-40 dB)."""
    x = np.arange(int(round(n))) / SR
    e = np.minimum(1, x / max(a, 1e-4))
    if r:
        e *= np.exp(-x * 4.6 / r)
    return e


def sq(f, sec, duty=0.5):
    return np.where((t(sec) * f) % 1 < duty, 1.0, -1.0)


def saw(f, sec):
    return 2 * ((t(sec) * f) % 1) - 1


def sine(f, sec):
    return np.sin(2 * np.pi * f * t(sec))


def noise(sec):
    return rng.uniform(-1, 1, int(round(SR * sec)))


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def reverb(x, sec=1.2, mix=0.3):
    ir = rng.uniform(-1, 1, int(round(SR * sec))) * np.exp(-np.arange(int(round(SR * sec))) / SR * 5 / sec)
    wet = np.fft.irfft(np.fft.rfft(x, len(x) + len(ir)) * np.fft.rfft(ir, len(x) + len(ir)))[: len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return x * (1 - mix) + wet * mix * np.max(np.abs(x))


def seq(parts):
    return np.concatenate(parts)


def mix(n, *layers):
    out = np.zeros(n)
    for start, sig in layers:
        s = int(start * SR)
        e = min(n, s + len(sig))
        out[s:e] += sig[: e - s]
    return out


def loopable(x, fade=0.5):
    """Funde la cola sobre la cabeza para un bucle sin clic."""
    f = int(fade * SR)
    head = x[:f] * np.linspace(0, 1, f) + x[-f:] * np.linspace(1, 0, f)
    return np.concatenate([head, x[f:-f]])


def note(n):  # MIDI -> Hz
    return 440 * 2 ** ((n - 69) / 12)


def save(name, x, vol=0.8):
    x = x / (np.max(np.abs(x)) + 1e-9) * vol
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / f"{name}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# ------------------------------------------------------------------ efectos

def sfx():
    n = noise(0.06)
    save("sfx_step", lowpass(n, 900) * env(len(n), 0.001, 0.05), 0.35)
    h = noise(0.5)
    hiss = lowpass(h, 3000) * env(len(h), 0.02, 0.45)
    thunk = sine(70, 0.5) * env(len(h), 0.001, 0.15)
    save("sfx_door", mix(len(h), (0, hiss * 0.6), (0.3, thunk)), 0.6)
    b = sq(110, 0.12, 0.3) * env((SR * 0.12), 0.002, 0.2)
    save("sfx_locked", seq([b, np.zeros(int(SR * 0.05)), b]), 0.4)
    save("sfx_pickup", seq([sq(note(m), 0.07, 0.25) * env((SR * 0.07), 0.002, 0.12) for m in (72, 76, 79, 84)]), 0.4)
    save("sfx_blip", sq(740, 0.025, 0.25) * env((SR * 0.025), 0.001, 0.03), 0.18)
    save("sfx_move", sq(1200, 0.03, 0.25) * env((SR * 0.03), 0.001, 0.03), 0.25)
    save("sfx_select", seq([sq(note(76), 0.05, 0.25), sq(note(83), 0.08, 0.25)]) * env((SR * 0.13), 0.002, 0.2), 0.3)
    # encuentro: acorde disonante + golpe de ruido + subgrave
    d = 1.2
    stab = sum(saw(note(m), d) for m in (45, 46, 52, 57)) * env((SR * d), 0.005, 1.0)
    hit = lowpass(noise(d), 1500) * env((SR * d), 0.001, 0.25)
    save("sfx_alert", reverb(stab * 0.5 + hit + sine(40, d) * env((SR * d), 0.01, 0.8), 1.5, 0.35), 0.9)
    s = noise(0.25)
    save("sfx_shoot", lowpass(s, 4000) * env(len(s), 0.001, 0.08) + sine(90, 0.25) * env(len(s), 0.001, 0.12), 0.7)
    save("sfx_hit", np.tanh(3 * (sine(60, 0.2) + lowpass(noise(0.2), 600))) * env((SR * 0.2), 0.001, 0.18), 0.7)
    rise = np.sin(2 * np.pi * np.cumsum(np.linspace(500, 1400, int(round(SR * 0.5)))) / SR)
    save("sfx_heal", reverb(rise * env(len(rise), 0.05, 0.6), 0.6, 0.3), 0.4)
    arp = seq([sine(note(m), 0.12) * env((SR * 0.12), 0.003, 0.4) for m in (60, 64, 67, 72, 76, 79)])
    save("sfx_contain", reverb(np.concatenate([arp, np.zeros(SR)]), 1.2, 0.4), 0.6)
    fall = np.sin(2 * np.pi * np.cumsum(np.linspace(400, 120, int(round(SR * 0.4)))) / SR)
    save("sfx_fail", np.sign(fall) * env(len(fall), 0.002, 0.4), 0.3)
    g = 0.45
    growl = np.tanh(4 * saw(55, g) * (1 + 0.5 * sine(23, g))) * env((SR * g), 0.01, 0.4)
    save("sfx_scp", lowpass(growl + lowpass(noise(g), 400), 1200), 0.8)
    dd = 1.6
    down = np.sin(2 * np.pi * np.cumsum(np.linspace(220, 40, int(round(SR * dd)))) / SR)
    save("sfx_defeat", reverb(down * env(len(down), 0.01, 1.5), 1.5, 0.4), 0.7)


# ----------------------------------------------------------------- ambiente

def amb():
    L = 16
    n = int(SR * L)
    tt = t(L)
    hum = sum(np.sin(2 * np.pi * 60 * k * tt) / k for k in (1, 2, 3, 5))
    air = lowpass(noise(L), 350)
    klax = np.zeros(n)
    for start in (3.0, 11.0):  # alarma lejana
        k = sum(sq(f, 0.45, 0.5) * env((SR * 0.45), 0.05, 0.6) for f in (330,))
        k2 = sq(262, 0.45, 0.5) * env((SR * 0.45), 0.05, 0.6)
        klax += mix(n, (start, lowpass(seq([k, k2, k, k2]), 700)))
    save("amb_facility", loopable(hum * 0.15 + air * 1.2 + reverb(klax, 2.0, 0.6) * 0.15), 0.5)

    wind = lowpass(noise(L), 200) * (0.6 + 0.4 * np.sin(2 * np.pi * tt / 8))
    whistle = lowpass(noise(L), 1200) * (0.5 + 0.5 * np.sin(2 * np.pi * tt / 5.3)) * 0.15
    save("amb_cold", loopable(wind * 3 + whistle + np.sin(2 * np.pi * 43 * tt) * 0.05), 0.5)

    beat = np.zeros(n)
    for s in np.arange(0, L, 1.1):  # latido
        thump = sine(48, 0.18) * env((SR * 0.18), 0.005, 0.15)
        beat += mix(n, (s, thump), (s + 0.28, thump * 0.6))
    drone = sine(55, L) * 0.05 + lowpass(noise(L), 150) * 0.8
    save("amb_padded", loopable(beat + drone), 0.5)

    drips = np.zeros(n)
    for s in rng.uniform(0, L - 0.3, 14):
        f = rng.uniform(900, 1800)
        drips += mix(n, (s, sine(f, 0.2) * env((SR * 0.2), 0.001, 0.12)))
    rumble = lowpass(noise(L), 90) * 4 + np.sin(2 * np.pi * 36 * tt) * 0.1
    save("amb_corroded", loopable(reverb(drips, 1.5, 0.5) * 0.4 + rumble), 0.5)

    buzz = np.sign(np.sin(2 * np.pi * 120 * tt)) * 0.03 + np.sin(2 * np.pi * 240 * tt) * 0.02
    beeps = np.zeros(n)
    for s in np.arange(0.5, L, 2.0):  # monitor cardíaco
        beeps += mix(n, (s, sine(1000, 0.12) * env((SR * 0.12), 0.002, 0.2)))
    save("amb_medical", loopable(buzz + beeps * 0.12 + lowpass(noise(L), 300) * 0.8), 0.45)

    bub = np.zeros(n)
    for s in rng.uniform(0, L - 0.2, 60):
        f0 = rng.uniform(150, 400)
        c = np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f0 * 2.5, int(round(SR * 0.08)))) / SR)
        bub += mix(n, (s, c * env(len(c), 0.002, 0.07)))
    deep = np.sin(2 * np.pi * 32 * tt) * 0.2 + lowpass(noise(L), 120) * 2
    save("amb_biohazard", loopable(bub * 0.25 + deep), 0.5)


# ------------------------------------------------------------------ música

def music():
    bpm = 140
    beat = 60 / bpm
    bars = 4
    L = bars * 4 * beat
    n = int(SR * L)
    parts = []
    bass = [45, 45, 57, 45, 48, 45, 58, 45]  # La menor con segunda menor
    for b in range(bars):
        for i in range(8):
            m = bass[i] + (0 if b < 2 else (3 if b == 2 else -2))
            s = b * 4 * beat + i * beat / 2
            parts.append((s, sq(note(m), beat / 2, 0.3) * env((SR * beat / 2), 0.003, beat)))
    for k in range(bars * 8):  # hi-hat
        s = k * beat / 2
        h = noise(0.05)
        parts.append((s, (h - lowpass(h, 3000)) * env(len(h), 0.001, 0.04) * (0.6 if k % 2 else 0.3)))
    for b in range(bars):  # bombo
        for q in (0, 1.5, 2, 3):
            s = b * 4 * beat + q * beat
            parts.append((s, np.sin(2 * np.pi * np.cumsum(np.linspace(120, 40, int(round(SR * 0.15)))) / SR) * env((SR * 0.15), 0.001, 0.15) * 1.5))
    lead = [69, 70, 72, 70, 69, 64, 65, 64]
    for i, m in enumerate(lead):  # motivo inquietante
        s = i * 2 * beat
        parts.append((s, sq(note(m + 12), beat * 1.5, 0.125) * env((SR * beat * 1.5), 0.01, beat * 2) * 0.25))
    save("mus_battle", mix(n, *parts), 0.6)

    L = 24
    n = int(SR * L)
    chords = [(45, 52, 60, 64), (41, 48, 57, 60), (43, 50, 58, 62), (40, 47, 56, 59)]
    parts = []
    for i, ch in enumerate(chords):
        s = i * 6
        pad = sum(saw(note(m), 6.5) * 0.25 for m in ch)
        e = np.minimum(1, t(6.5) / 1.5) * np.minimum(1, (6.5 - t(6.5)) / 1.5)
        parts.append((s, lowpass(pad, 700) * e))
    bell = [76, 72, 69, 71]
    for i, m in enumerate(bell):
        parts.append((i * 6 + 2, sine(note(m), 3) * env((SR * 3), 0.005, 2.5) * 0.3))
    save("mus_title", loopable(reverb(mix(n, *parts), 2.5, 0.45), 1.0), 0.55)

    L = 14
    n = int(SR * L)
    chords = [(48, 55, 64, 67), (53, 60, 69, 72), (55, 62, 71, 74), (48, 55, 64, 72)]
    parts = [(i * 3.4, lowpass(sum(saw(note(m), 4) * 0.25 for m in ch), 900)
              * np.minimum(1, t(4) / 0.8) * np.minimum(1, (4 - t(4)) / 1.2)) for i, ch in enumerate(chords)]
    save("mus_ending", reverb(mix(n, *parts), 2.5, 0.45), 0.55)


if __name__ == "__main__":
    sfx()
    amb()
    music()
    print("ok:", len(list(OUT.glob("*.wav"))), "wavs")
