"""Synthesizes every sound in the game into art/audio/*.wav (22.05 kHz mono 16-bit).
Usage: python3 tools/gen_audio.py        (requires numpy + scipy)

Naming: sfx_*  one-shots · loop_* positional loops · amb_* ambience beds · mus_* music.
Design goal: dread. Low drones, far-away events you can't place, small close sounds.
"""
import wave
from pathlib import Path
import numpy as np
from scipy.signal import butter, lfilter, fftconvolve

SR = 22050
OUT = Path(__file__).resolve().parent.parent / "art/audio"
rng = np.random.default_rng(19)


# ------------------------------------------------------------------ DSP
def n(sec):
    return int(round(SR * sec))


def t(sec):
    return np.arange(n(sec)) / SR


def noise(sec):
    return rng.uniform(-1, 1, n(sec))


def brown(sec):
    x = np.cumsum(rng.normal(0, 1, n(sec)))
    x -= np.linspace(x[0], x[-1], len(x))  # remove drift so it loops
    return x / (np.max(np.abs(x)) + 1e-9)


def filt(x, kind, f, order=2):
    nyq = SR / 2
    if kind == "band":
        b, a = butter(order, [f[0] / nyq, f[1] / nyq], btype="band")
    else:
        b, a = butter(order, f / nyq, btype=kind)
    return lfilter(b, a, x)


def lp(x, f, o=2):
    return filt(x, "low", f, o)


def hp(x, f, o=2):
    return filt(x, "high", f, o)


def bp(x, lo, hi, o=2):
    return filt(x, "band", (lo, hi), o)


def env(length, a=0.005, d=None, curve=4.6):
    x = np.arange(length) / SR
    e = np.minimum(1, x / max(a, 1e-4))
    if d:
        e = e * np.exp(-x * curve / d)
    return e


def shape(sig, a=0.005, d=None):
    return sig * env(len(sig), a, d)


def sine(f, sec, ph=0.0):
    return np.sin(2 * np.pi * f * t(sec) + ph)


def sweep(f0, f1, sec):
    return np.sin(2 * np.pi * np.cumsum(np.linspace(f0, f1, n(sec))) / SR)


def saw(f, sec):
    return 2 * ((t(sec) * f) % 1) - 1


def sq(f, sec, duty=0.5):
    return np.where((t(sec) * f) % 1 < duty, 1.0, -1.0)


def reverb(x, sec=1.5, mix=0.35, damp=4000):
    ir = lp(noise(sec), damp) * np.exp(-t(sec) * 6.0 / sec)
    wet = fftconvolve(x, ir)[: len(x)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return x * (1 - mix) + wet * mix * (np.max(np.abs(x)) + 1e-9)


def pad(x, sec):
    return np.concatenate([x, np.zeros(max(0, n(sec) - len(x)))])


def place(total_sec, events):
    """events: [(start_sec, signal, gain)] mixed into a buffer (wrapping, so loops stay seamless)."""
    out = np.zeros(n(total_sec))
    for st, sig, g in events:
        s = n(st) % len(out)
        e = min(len(out), s + len(sig))
        out[s:e] += sig[: e - s] * g
        if s + len(sig) > len(out):
            rest = sig[e - s:][: len(out)]
            out[: len(rest)] += rest * g
    return out


def loopable(x, fade=0.8):
    f = n(fade)
    head = x[:f] * np.linspace(0, 1, f) + x[-f:] * np.linspace(1, 0, f)
    return np.concatenate([head, x[f:-f]])


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


def save(name, x, peak=0.85):
    x = np.nan_to_num(np.asarray(x, dtype=float))
    x = x / (np.max(np.abs(x)) + 1e-9) * peak
    OUT.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT / f"{name}.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------- building blocks
def thump(f=60, sec=0.3, d=0.2):
    return shape(sweep(f * 2, f, sec) + lp(noise(sec), 300) * 0.5, 0.002, d)


def clank(sec=0.5, base=380):
    parts = [sine(base * r, sec) * g for r, g in ((1, 1), (2.76, 0.6), (5.4, 0.35), (8.9, 0.2))]
    return shape(sum(parts) + hp(noise(sec), 2000) * 0.3, 0.001, sec * 0.8)


def creak(sec=0.8, f=180):
    freq = f + 60 * np.sin(t(sec) * 7) + rng.normal(0, 20, n(sec))
    wob = np.sin(2 * np.pi * np.cumsum(freq) / SR)
    return shape(bp(wob * np.abs(np.sin(t(sec) * 40)), 150, 1800), 0.05, sec)


def footstep(kind):
    s = 0.12
    if kind == "concrete":
        x = lp(noise(s), 1400) * env(n(s), 0.001, 0.05) + thump(70, s, 0.04) * 0.5
    elif kind == "tile":
        x = bp(noise(s), 800, 5000) * env(n(s), 0.001, 0.03) + thump(90, s, 0.03) * 0.4
    elif kind == "soft":
        x = lp(noise(s), 500) * env(n(s), 0.006, 0.06)
    elif kind == "metal":
        x = clank(0.18, 250) * 0.35
        x[: n(s)] += bp(noise(s), 1000, 6000) * env(n(s), 0.001, 0.02) * 0.5
    elif kind == "dirt":
        x = lp(noise(s), 900) * env(n(s), 0.002, 0.07) + bp(noise(s), 2000, 5000) * env(n(s), 0.01, 0.05) * 0.3
    elif kind == "water":
        x = bp(noise(0.2), 400, 3000) * env(n(0.2), 0.005, 0.12) + sweep(900, 300, 0.2) * env(n(0.2), 0.001, 0.05) * 0.3
    else:  # flesh
        x = lp(noise(0.2), 600) * env(n(0.2), 0.01, 0.12) + sweep(200, 90, 0.2) * env(n(0.2), 0.002, 0.08) * 0.4
    return x


def voice_murmur(sec, pitch=140, seed=0):
    """Unintelligible speech-like murmur (formant-filtered buzz with syllable gating)."""
    r = np.random.default_rng(seed)
    jitter = np.repeat(r.normal(0, 0.06, n(sec) // 2205 + 1), 2205)[: n(sec)]
    f0 = pitch * (1 + 0.15 * np.sin(t(sec) * r.uniform(2, 4)) + jitter)
    buzz = np.sign(np.sin(2 * np.pi * np.cumsum(f0) / SR)) * 0.5 + noise(sec) * 0.15
    syll = np.repeat((r.uniform(0, 1, n(sec) // 3300 + 1) > 0.3).astype(float), 3300)[: n(sec)]
    syll = lp(syll, 12)
    out = np.zeros(n(sec))
    for lo, hi, g in ((300, 900, 1.0), (900, 1600, 0.6), (2200, 3200, 0.3)):
        out += bp(buzz, lo, hi) * g
    return out * syll


def far(sig, rv=3.0):
    return reverb(lp(sig, 1500), rv, 0.75)


def far_door():
    return place(1.2, [(0, thump(55, 0.5, 0.3), 1), (0.05, clank(0.5, 300), 0.5)])


def far_voice(seed=99):
    return lp(voice_murmur(1.5, 400, seed), 1500) * np.linspace(1, 0.1, n(1.5))


# ------------------------------------------------------------------ SFX
def sfx():
    for k in ("concrete", "tile", "soft", "metal", "dirt", "water", "flesh"):
        save("sfx_step_" + k, footstep(k), 0.5)
    save("sfx_click", shape(hp(noise(0.03), 3000), 0.0005, 0.01) + shape(sine(2400, 0.03), 0.0005, 0.008), 0.4)
    hiss = shape(bp(noise(0.7), 1500, 7000), 0.03, 0.5)
    save("sfx_door_open", place(0.9, [(0, hiss, 0.5), (0.05, thump(80, 0.3, 0.12), 1.0), (0.55, clank(0.35, 520), 0.5)]), 0.7)
    save("sfx_door_close", place(0.9, [(0, hiss, 0.4), (0.4, thump(55, 0.45, 0.3), 1.2), (0.42, clank(0.4, 300), 0.6)]), 0.8)

    def beep(f, s):
        return shape(sq(f, s, 0.3), 0.002, s)
    save("sfx_denied", np.concatenate([beep(220, 0.12), np.zeros(n(0.05)), beep(165, 0.2)]), 0.4)
    save("sfx_keycard", np.concatenate([beep(1320, 0.05), beep(1760, 0.08)]), 0.35)
    save("sfx_lock_click", place(0.3, [(0, clank(0.1, 1800), 0.5), (0.12, clank(0.15, 1200), 0.8)]), 0.5)
    arp = np.concatenate([shape(sine(note(m), 0.07) + 0.3 * sq(note(m), 0.07, 0.2), 0.002, 0.1) for m in (72, 79, 84)])
    save("sfx_pickup", reverb(pad(arp, 0.6), 0.6, 0.3), 0.35)
    save("sfx_quest", reverb(pad(np.concatenate([shape(sine(note(m), 0.16), 0.01, 0.5) for m in (60, 67, 72, 76)]), 1.6), 1.4, 0.45), 0.35)
    save("sfx_blip", shape(sq(620, 0.03, 0.3), 0.001, 0.03), 0.16)
    save("sfx_blip_radio", shape(bp(sq(480, 0.035, 0.4) + noise(0.035) * 0.6, 300, 3000), 0.001, 0.03), 0.18)
    save("sfx_blip_079", shape(sq(180, 0.04, 0.5) + hp(noise(0.04), 4000) * 0.4, 0.001, 0.03), 0.2)
    save("sfx_move", shape(sine(1400, 0.025), 0.001, 0.02), 0.2)
    save("sfx_select", np.concatenate([shape(sine(note(76), 0.05), 0.002, 0.05), shape(sine(note(83), 0.08), 0.002, 0.08)]), 0.3)
    save("sfx_menu_open", shape(sweep(300, 900, 0.15), 0.01, 0.15) * 0.5 + shape(bp(noise(0.15), 800, 3000), 0.01, 0.1) * 0.3, 0.3)
    save("sfx_menu_close", shape(sweep(900, 300, 0.15), 0.01, 0.15) * 0.5, 0.3)
    save("sfx_paper", shape(bp(noise(0.35), 1500, 7000) * (0.5 + 0.5 * np.abs(np.sin(t(0.35) * 60))), 0.01, 0.3), 0.35)
    save("sfx_saved", reverb(pad(np.concatenate([shape(sine(note(m), 0.1), 0.01, 0.3) for m in (64, 71)]), 1.0), 1.0, 0.4), 0.3)
    save("sfx_hurt", shape(lp(noise(0.3), 700), 0.001, 0.15) + thump(50, 0.3, 0.2), 0.8)
    save("sfx_heal", reverb(shape(sweep(400, 1100, 0.6), 0.05, 0.6) * 0.5, 0.8, 0.3), 0.35)
    save("sfx_battery", place(0.5, [(0, clank(0.15, 1500), 0.4), (0.18, clank(0.2, 900), 0.6), (0.3, shape(sine(3000, 0.1), 0.001, 0.05), 0.2)]), 0.5)
    save("sfx_drink", place(1.0, [(i * 0.25, shape(lp(noise(0.12), 900), 0.02, 0.1), 0.6) for i in range(3)]), 0.4)
    save("sfx_heartbeat", place(0.9, [(0, thump(45, 0.25, 0.12), 1), (0.22, thump(45, 0.25, 0.12), 0.7)]), 0.9)
    d = 3.0
    save("sfx_death", reverb(lp(sweep(180, 30, d) * env(n(d), 0.01, 2.5) + brown(d) * 0.4 * env(n(d), 0.01, 2.0), 1200), 2.5, 0.5), 0.9)
    save("sfx_power_down", lp(sweep(120, 20, 1.6) * env(n(1.6), 0.01, 1.4), 800) + shape(bp(noise(1.6), 2000, 6000), 0.001, 0.4) * 0.3, 0.8)
    save("sfx_power_up", lp(sweep(20, 120, 1.4), 900) * np.minimum(1, t(1.4) / 1.0) + place(1.4, [(1.1, clank(0.3, 700), 0.5)]), 0.7)
    save("sfx_spark", shape(hp(noise(0.25), 2500) * (rng.uniform(0, 1, n(0.25)) > 0.7), 0.001, 0.12), 0.5)
    save("sfx_drip", pad(shape(sweep(1600, 700, 0.12), 0.001, 0.05), 0.2) + shape(sine(1100, 0.2), 0.001, 0.08) * 0.3, 0.4)
    save("sfx_squeak", np.concatenate([shape(sweep(3200, 4200, 0.07), 0.003, 0.06), np.zeros(n(0.04)), shape(sweep(3600, 3000, 0.09), 0.003, 0.08)]), 0.3)
    save("sfx_elevator_stop", reverb(place(2.0, [(0, thump(40, 1.2, 0.6), 1.5), (0, creak(1.4, 120), 0.6), (0.2, clank(0.8, 210), 0.8)]), 2.0, 0.4), 0.95)
    save("sfx_metal_strain", reverb(creak(1.2, 140) + creak(1.2, 95) * 0.7, 1.2, 0.3), 0.7)
    screech = np.sin(2 * np.pi * np.cumsum(1400 + 300 * np.sin(t(1.0) * 23)) / SR)
    save("sfx_metal_screech", reverb(shape(bp(screech, 800, 4000), 0.02, 0.9) + thump(60, 1.0, 0.4), 1.2, 0.3), 0.8)
    save("sfx_radio_static", shape(bp(noise(1.2), 400, 5000) * (0.6 + 0.4 * np.sin(t(1.2) * 13)), 0.02, 1.0), 0.5)
    save("sfx_static_burst", shape(bp(noise(0.5), 300, 6000), 0.001, 0.4), 0.7)
    keys = place(0.6, [(0.15 + i * 0.07, shape(hp(noise(0.02), 3000), 0.001, 0.01), 0.3) for i in range(5)])
    tone = pad(np.concatenate([shape(sq(880, 0.05, 0.4), 0.002, 0.05), np.zeros(n(0.03)), shape(sq(1320, 0.07, 0.4), 0.002, 0.07)]), 0.6)
    save("sfx_terminal", tone + keys, 0.3)
    save("sfx_crt_on", shape(sweep(8000, 14000, 0.6), 0.001, 0.5) * 0.3 + thump(40, 0.6, 0.3), 0.5)
    save("sfx_pans_fall", reverb(place(1.4, [(0, clank(0.6, 700), 1), (0.15, clank(0.8, 520), 0.8), (0.4, clank(0.5, 990), 0.6), (0.7, clank(0.6, 610), 0.5)]), 1.2, 0.35), 0.8)
    save("sfx_machine_pour", place(2.0, [(0, thump(60, 0.3, 0.2), 0.6), (0.3, shape(lp(noise(1.4), 1500), 0.1, 1.2), 0.5), (1.8, shape(sine(1760, 0.2), 0.01, 0.2), 0.3)]), 0.5)
    save("sfx_alarm_short", np.concatenate([shape(sq(f, 0.35, 0.5), 0.01, 0.5) for f in (660, 520, 660, 520)]), 0.35)
    save("sfx_gas_hiss", shape(bp(noise(2.5), 1500, 8000), 0.1, 2.2), 0.5)
    save("sfx_decon_done", reverb(pad(np.concatenate([shape(sine(note(m), 0.2), 0.01, 0.3) for m in (69, 76)]), 1.0), 1.0, 0.4), 0.35)
    save("sfx_hatch", place(1.0, [(0, clank(0.4, 330), 1), (0.2, creak(0.7, 200), 0.6)]), 0.7)
    save("sfx_breaker", reverb(place(1.2, [(0, clank(0.3, 400), 1), (0.05, thump(50, 0.6, 0.3), 1.5),
                                           (0.1, hp(noise(0.5), 3000) * env(n(0.5), 0.001, 0.2), 0.5)]), 1.2, 0.3), 0.9)
    save("sfx_glass", shape(hp(noise(0.8), 3000) * (rng.uniform(0, 1, n(0.8)) > 0.85), 0.001, 0.5) + clank(0.8, 2400) * 0.3, 0.6)
    save("sfx_far_bang", reverb(lp(thump(40, 1.5, 0.8) + clank(1.5, 180) * 0.4, 700), 3.0, 0.7), 0.8)
    save("sfx_far_scream", reverb(lp(voice_murmur(1.6, 420, 3) * np.linspace(1, 0.2, n(1.6)), 1800), 3.0, 0.75), 0.5)
    # SCPs
    scrape = bp(brown(1.2), 200, 2500) * (0.5 + 0.5 * np.abs(np.sin(t(1.2) * 9))) + lp(noise(1.2), 500) * 0.5
    save("sfx_scrape", shape(scrape, 0.05, 1.0), 0.7)
    save("sfx_neck_snap", place(0.5, [(0, hp(noise(0.05), 1500) * env(n(0.05), 0.0005, 0.02), 1.5),
                                      (0.02, clank(0.2, 900), 0.4), (0.01, thump(90, 0.3, 0.1), 1)]), 0.95)
    save("sfx_096_scream", reverb(bp(voice_murmur(3.0, 520, 7) * 3 + noise(3.0) * 0.6, 500, 5000) * np.minimum(1, t(3.0) / 0.3), 2.0, 0.4), 0.95)
    save("sfx_106_laugh", reverb(lp(voice_murmur(2.0, 70, 11) * (0.6 + 0.4 * np.abs(np.sin(t(2.0) * 6))), 900), 2.5, 0.6), 0.8)
    save("sfx_106_emerge", reverb(lp(brown(2.0), 400) * np.minimum(1, t(2.0) / 1.0)
                                  + shape(bp(noise(2.0), 100, 800) * np.abs(np.sin(t(2.0) * 3)), 0.5, 1.8), 2.0, 0.5), 0.9)
    save("sfx_squelch", shape(lp(noise(0.4), 800) * np.abs(np.sin(t(0.4) * 30)), 0.01, 0.3) + sweep(300, 90, 0.4) * env(n(0.4), 0.01, 0.2) * 0.4, 0.6)
    save("sfx_682_roar", reverb(lp(saw(38, 2.5) * (1 + 0.5 * sine(7, 2.5)) + brown(2.5) * 0.6, 900) * env(n(2.5), 0.1, 2.2), 2.5, 0.5), 0.95)
    save("sfx_939_call", reverb(bp(voice_murmur(1.8, 200, 5), 300, 2500) * env(n(1.8), 0.1, 1.6), 2.5, 0.6), 0.6)
    hum049 = sum(sine(note(m), 2.5) * g for m, g in ((50, 1), (57, 0.4), (62, 0.2)))
    save("sfx_049_hum", reverb(lp(hum049 * env(n(2.5), 0.4, 2.2), 1200), 2.0, 0.4), 0.5)
    zap = hp(noise(0.6), 1500) * (rng.uniform(0, 1, n(0.6)) > 0.6) * env(n(0.6), 0.001, 0.4)
    save("sfx_tesla", reverb(place(1.0, [(0, zap, 1), (0, sq(60, 0.6, 0.5) * env(n(0.6), 0.001, 0.4), 0.5)]), 0.8, 0.3), 0.9)
    whisper = bp(noise(2.0), 1500, 6000) * lp(np.abs(voice_murmur(2.0, 180, 13)), 20) * 3
    save("sfx_whisper", reverb(hp(whisper, 800), 1.5, 0.5), 0.4)
    save("sfx_child_cry", reverb(bp(voice_murmur(2.4, 380, 17), 400, 3000) * np.linspace(0.3, 1, n(2.4)) * env(n(2.4), 0.2, 2.3), 3.0, 0.8), 0.45)
    shot_tail = reverb(hp(noise(0.3), 1500) * env(n(0.3), 0.001, 0.2), 0.5, 0.6)
    save("sfx_shoot", place(0.5, [(0, hp(noise(0.12), 800) * env(n(0.12), 0.0005, 0.05), 1.5), (0, thump(70, 0.4, 0.15), 1.2), (0.02, shot_tail, 0.4)]), 0.9)
    save("sfx_hit", place(0.3, [(0, thump(60, 0.25, 0.12), 1.2), (0, lp(noise(0.1), 1200) * env(n(0.1), 0.001, 0.04), 1)]), 0.8)
    save("sfx_empty_gun", clank(0.1, 2200), 0.4)


# ---------------------------------------------------------------- loops
def loops():
    L = 8.0
    save("loop_hum", loopable(sum(np.sin(2 * np.pi * 60 * k * t(L)) / k ** 1.3 for k in (1, 2, 3, 4, 6)) * 0.3 + lp(noise(L), 300) * 0.4, 0.5), 0.5)
    save("loop_fridge", loopable(lp(saw(55, L) * 0.3 + noise(L) * 0.2, 400) * (0.9 + 0.1 * np.sin(t(L) * 2)), 0.5), 0.45)
    fans = bp(noise(L), 1500, 6000) * 0.5 + lp(noise(L), 200) * 0.6 + sum(np.sin(2 * np.pi * f * t(L)) * 0.08 for f in (120, 240))
    clicks = place(L, [(rng.uniform(0, L), shape(hp(noise(0.02), 3000), 0.0005, 0.01), 0.6) for _ in range(30)])
    save("loop_servers", loopable(fans + clicks, 0.5), 0.5)
    buzz = sq(180, L, 0.5) * (0.6 + 0.4 * np.sin(t(L) * 3.3)) + sq(203, L, 0.5) * 0.5 * (0.6 + 0.4 * np.sin(t(L) * 2.1 + 1))
    save("loop_flies", loopable(bp(buzz, 150, 1200), 0.5), 0.4)
    alarm = place(L, [(i * 2.0, np.concatenate([shape(sq(f, 0.45, 0.5), 0.02, 0.5) for f in (660, 520)]), 1) for i in range(4)])
    save("loop_alarm_far", loopable(reverb(lp(alarm, 1400), 2.5, 0.7), 0.5), 0.5)
    save("loop_steam", loopable(bp(noise(L), 1000, 6000) * (0.8 + 0.2 * np.sin(t(L) * 1.3)), 0.5), 0.4)
    save("loop_water", loopable(lp(noise(L), 1800) * (0.6 + 0.4 * np.abs(np.sin(t(L) * 0.9))) + bp(noise(L), 3000, 6000) * 0.15, 0.5), 0.45)
    save("loop_generator", loopable(lp(saw(30, L) + sq(60, L) * 0.3 + brown(L) * 0.4, 500) * (1 + 0.05 * np.sin(t(L) * 20)), 0.5), 0.6)
    save("loop_tesla", loopable(sq(60, L, 0.5) * 0.2 + hp(noise(L), 4000) * (rng.uniform(0, 1, n(L)) > 0.97) * 0.6, 0.5), 0.4)
    cry = sum(voice_murmur(L, 330 + i * 30, 30 + i) for i in range(2))
    save("loop_096_cry", loopable(reverb(bp(cry, 300, 2500) * (0.5 + 0.5 * np.abs(np.sin(t(L) * 0.7))), 2.0, 0.5), 0.8), 0.5)
    beats = int(L / 0.85)
    save("loop_heartbeat", loopable(place(L, [(i * 0.85, thump(45, 0.25, 0.12), 1) for i in range(beats)]
                                         + [(i * 0.85 + 0.22, thump(45, 0.25, 0.12), 0.7) for i in range(beats)]), 0.1), 0.8)
    radio = bp(noise(L), 400, 4000) * (0.3 + 0.7 * (np.abs(np.sin(t(L) * 0.37)) > 0.8)) + bp(voice_murmur(L, 150, 41), 400, 3000) * 0.4
    save("loop_radio", loopable(radio, 0.5), 0.4)
    comp = sum(np.sin(2 * np.pi * f * t(L)) * 0.1 for f in (440, 1320)) * (np.sin(t(L) * 3) > 0.9) + lp(noise(L), 600) * 0.3
    save("loop_computer", loopable(comp, 0.5), 0.35)


# ------------------------------------------------------------- ambiences
def amb_bed(L, drone_hz, drone_lp, air_lp, events, tone=0.0):
    base = lp(brown(L), drone_lp) * 1.5 + lp(noise(L), air_lp) * 0.3
    if tone:
        base += sum(np.sin(2 * np.pi * tone * k * t(L)) / k for k in (1, 2, 3)) * 0.04
    if drone_hz:
        base += np.sin(2 * np.pi * drone_hz * t(L)) * 0.08
    return loopable(base + place(L, events), 1.5)


def ambiences():
    L = 32.0

    def r():
        return rng.uniform(1, L - 3)
    save("amb_ez", amb_bed(L, 50, 150, 400, [(r(), far(clank(1.0, 240)), 0.25), (r(), far(thump(50, 1.2, 0.6)), 0.3),
                                              (r(), far(creak(1.5, 110)), 0.2), (r(), far(far_door()), 0.2)], tone=60), 0.5)
    save("amb_elevator", amb_bed(L, 38, 120, 300, [(r(), far(creak(2.0, 90)), 0.35), (r(), far(creak(1.5, 140)), 0.25),
                                                   (r(), far(clank(1.2, 200)), 0.2)]), 0.5)
    save("amb_ez_cafe", amb_bed(L, 0, 160, 500, [(r(), far(clank(0.6, 900)), 0.1), (r(), shape(bp(noise(3), 400, 3000), 0.5, 2.5), 0.05)], tone=60), 0.45)
    save("amb_servers", amb_bed(L, 0, 200, 800, [], tone=120), 0.4)
    save("amb_lcz", amb_bed(L, 44, 140, 500, [(r(), far(bp(brown(1.2), 200, 2500) * 0.8, rv=2.5), 0.25), (r(), far(clank(1.0, 330)), 0.2),
                                              (r(), far(far_voice()), 0.12), (r(), far(thump(45, 1.0, 0.5)), 0.3)], tone=50), 0.5)
    swell = lp(noise(6), 1500) * np.sin(np.linspace(0, np.pi, n(6)))
    save("amb_maint", amb_bed(L, 33, 180, 1200, [(r(), far(clank(1.2, 150)), 0.3), (r(), far(creak(2.0, 70)), 0.3), (r(), swell, 0.25)]), 0.55)
    save("amb_med", amb_bed(L, 0, 130, 400, [(r(), far(shape(sine(1000, 0.15), 0.005, 0.15)), 0.08), (r(), far(creak(1.0, 300)), 0.15),
                                             (r(), far(lp(voice_murmur(2.0, 110, 51), 800)), 0.12)], tone=120), 0.45)
    save("amb_hcz", amb_bed(L, 30, 110, 350, [(r(), far(thump(35, 2.0, 1.2)), 0.5), (r(), far(clank(2.0, 120)), 0.3),
                                              (r(), far(lp(saw(40, 2.0) * env(n(2.0), 0.3, 1.8), 600), rv=4.0), 0.25),
                                              (r(), far(bp(noise(3), 1000, 5000) * np.sin(np.linspace(0, np.pi, n(3)))), 0.15)]), 0.55)
    drops = [(r(), shape(sweep(1500, 700, 0.1), 0.001, 0.05), 0.05) for _ in range(12)]
    save("amb_939", amb_bed(L, 0, 120, 600, [(r(), far(voice_murmur(2.5, 160, 61), rv=3.5), 0.18), (r(), far(voice_murmur(2.0, 230, 62), rv=3.5), 0.14),
                                             (r(), far(voice_murmur(1.5, 120, 63), rv=3.5), 0.15)] + drops), 0.5)
    save("amb_pocket", amb_bed(L, 27, 90, 250, [(r(), far(voice_murmur(3.0, 90, 71), rv=5.0), 0.2), (r(), far(voice_murmur(3.0, 70, 72), rv=5.0), 0.2),
                                                (r(), reverb(lp(brown(4), 300), 4, 0.8), 0.4)]), 0.55)
    save("amb_087", amb_bed(L, 0, 80, 200, [(r(), far(lp(voice_murmur(2.4, 380, 81), 1500), rv=6.0), 0.1),
                                            (r(), far(lp(voice_murmur(2.4, 390, 82), 1500), rv=6.0), 0.08)]), 0.5)
    save("amb_core", amb_bed(L, 0, 150, 900, [(r(), far(shape(sq(1760, 0.08, 0.5), 0.002, 0.08)), 0.1) for _ in range(6)], tone=120), 0.45)
    save("amb_sewer", amb_bed(L, 0, 250, 2000, [(r(), shape(sweep(1600, 700, 0.12), 0.001, 0.05), 0.2) for _ in range(20)]
                              + [(r(), far(creak(2.0, 60)), 0.3)]), 0.55)


# ------------------------------------------------------------------ music
def pad_chord(ms, sec, cut=700):
    x = sum(saw(note(m) * (1 + d), sec) for m in ms for d in (-0.003, 0.003)) / (len(ms) * 2)
    return lp(x, cut) * np.minimum(1, t(sec) / (sec * 0.3)) * np.minimum(1, (sec - t(sec)) / (sec * 0.3))


def music():
    L = 32.0
    ev = [(i * 8, pad_chord(ch, 9.0, 600), 0.6) for i, ch in enumerate([(45, 52, 60), (41, 48, 57), (43, 50, 58), (40, 47, 55)])]
    ev += [(i * 8 + 3, shape(sine(note(m), 4.0) + sine(note(m) * 2.76, 4.0) * 0.2, 0.005, 3.5), 0.25) for i, m in enumerate((76, 72, 74, 71))]
    save("mus_title", loopable(reverb(place(L, ev), 3.0, 0.5), 2.0), 0.55)
    L = 24.0
    ev = [(i * 1.2, thump(40, 0.4, 0.2), 0.5) for i in range(20)]
    ev += [(0, pad_chord((33, 34, 45), 24.0, 400) * np.linspace(0.2, 1, n(24.0)), 0.7)]
    save("mus_prologue", reverb(place(L, ev), 2.5, 0.4), 0.55)
    L = 16.0
    ev = [(rng.uniform(0, L - 1), shape(sq(note(int(rng.choice([57, 60, 63, 66, 69]))), rng.uniform(0.05, 0.3), 0.5), 0.002, 0.2), 0.2) for _ in range(40)]
    ev += [(0, pad_chord((38, 44), L, 500), 0.5)]
    save("mus_079", loopable(reverb(place(L, ev), 1.5, 0.3), 1.0), 0.5)
    b = 60 / 150
    L = 16 * b
    ev = [(i * b / 2, lp(sq(note(33 + (0 if (i // 8) % 2 == 0 else 1)), b / 2, 0.3), 900) * env(n(b / 2), 0.002, b / 2), 0.5) for i in range(32)]
    ev += [(i * b, thump(55, 0.2, 0.1), 0.9) for i in range(16)]
    ev += [(i * b * 4, pad_chord((57, 58, 64), b * 4, 1500), 0.25) for i in range(4)]
    save("mus_chase", place(L, ev), 0.6)
    L = 24.0
    seq = [57, 60, 64, 67, 64, 60] * 4
    ev = [(i * 1.0, shape(sine(note(m), 2.0), 0.02, 1.8), 0.2) for i, m in enumerate(seq)]
    save("mus_safe", loopable(reverb(place(L, ev), 3.0, 0.6), 1.5), 0.4)
    b = 60 / 132
    L = 16 * b
    bass = [45, 45, 57, 45, 48, 45, 58, 45]
    ev = [(i * b / 2, lp(sq(note(bass[i % 8] + (0 if i < 16 else -2)), b / 2, 0.3), 1000) * env(n(b / 2), 0.002, b), 0.5) for i in range(32)]
    ev += [(i * b, thump(55, 0.2, 0.12), 1.0) for i in range(16)]
    ev += [(i * b / 2, hp(noise(0.05), 5000) * env(n(0.05), 0.001, 0.03), 0.4) for i in range(32)]
    save("mus_battle", place(L, ev), 0.6)
    for name, chords in (("ending", [(48, 55, 64), (53, 60, 69), (55, 62, 71), (48, 55, 67)]),
                         ("ending_dark", [(45, 52, 60), (44, 51, 60), (43, 50, 58), (41, 48, 56)])):
        L = 28.0
        ev = [(i * 7, pad_chord(ch, 8.0, 900), 0.6) for i, ch in enumerate(chords)]
        save("mus_" + name, reverb(place(L, ev), 3.0, 0.5), 0.55)


if __name__ == "__main__":
    for f in OUT.glob("*.wav"):
        f.unlink()
    for f in OUT.glob("*.wav.import"):
        f.unlink()
    sfx()
    loops()
    ambiences()
    music()
    print("ok:", len(list(OUT.glob("*.wav"))), "sounds")
