"""Genera un atlas de tiles 16x16 por tema con paleta fija.
Uso: python3 tools/gen_tiles.py   (requiere Pillow)
Layout del atlas (16 cols x 4 filas):
  fila 0: piso variantes 0-5, 6 rejilla, 7 franja de peligro, 8 tapete de salida
  fila 1: cara baja de pared 0 lisa, 1 tubo, 2 ventila, 3 aviso, 4 lámpara, 5 puerta, 6 ventana,
          7 manchada, 8 cara alta, 9 puerta bloqueada
  fila 2: tope de pared, 16 variantes por máscara de vecinos piso (N=1 E=2 S=4 W=8)
  fila 3: calcos (transparentes) 0 grieta, 1 sangre, 2 papeles, 3 charco, 4 cables,
          5 sombra bajo muro, 6 sombra a la derecha del muro
"""
import random
from pathlib import Path
from PIL import Image, ImageDraw

T = 16
OUT = Path(__file__).resolve().parent.parent / "art/tiles/atlas"

# Paleta fija del juego. Todo color de tile sale de aquí.
P = {
    "k0": "#0b0b12", "k1": "#16161f", "k2": "#232330", "k3": "#34343f",
    "g1": "#4a4b57", "g2": "#62646f", "g3": "#83858f", "g4": "#a8aab2", "g5": "#d0d2d6", "w": "#eef0ee",
    "b1": "#1d2b3a", "b2": "#2c4257", "b3": "#466681", "b4": "#6f94ad", "b5": "#a9c8d8",
    "t1": "#1c3a3a", "t2": "#2d5c58", "t3": "#4d8a80", "t4": "#85c0b0",
    "r1": "#2e1a14", "r2": "#4a2a1c", "r3": "#6e3e24", "r4": "#9a5a2e", "r5": "#c4833f",
    "e1": "#4a1016", "e2": "#8a1c24", "e3": "#c9302c",
    "y1": "#6b5a14", "y2": "#b8961e", "y3": "#e8c440",
    "n1": "#1e3318", "n2": "#3a5a22", "n3": "#6f9a2a", "n4": "#a8d040",
    "c1": "#6b6250", "c2": "#9a907a", "c3": "#c7bda2", "c4": "#e2dac2",
}
C = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for k, v in P.items()}


def a(col, alpha):
    return col[:3] + (alpha,)


THEMES = {
    #           piso: base, oscuro, claro, junta | pared: cuerpo, oscuro, claro, franja | tope
    "facility": dict(f=("g2", "g1", "g3", "k3"), w=("g3", "g2", "g4", "b3"), top="k1", style="concrete"),
    "cold": dict(f=("b3", "b2", "b4", "b1"), w=("b2", "b1", "b4", "b5"), top="k1", style="tiles"),
    "padded": dict(f=("c3", "c2", "c4", "c1"), w=("c3", "c2", "c4", "c1"), top="k2", style="padded"),
    "corroded": dict(f=("r2", "r1", "r3", "k1"), w=("g1", "k3", "g2", "r3"), top="k0", style="corroded"),
    "medical": dict(f=("g5", "g4", "w", "g3"), w=("w", "g5", "w", "t3"), top="k1", style="checker"),
    "biohazard": dict(f=("k3", "k2", "g1", "k0"), w=("g1", "k3", "g2", "y3"), top="k0", style="grating"),
}


def px(im, x, y, col):
    if 0 <= x < T and 0 <= y < T:
        im.putpixel((x, y), col)


def noise(im, rnd, cols, n):
    for _ in range(n):
        px(im, rnd.randrange(T), rnd.randrange(T), C[rnd.choice(cols)])


def floor(th, rnd, v):
    base, dark, light, seam = th["f"]
    im = Image.new("RGBA", (T, T), C[base])
    d = ImageDraw.Draw(im)
    s = th["style"]
    if s == "concrete":
        noise(im, rnd, [dark, light], 22)
        d.line([(0, 15), (15, 15)], C[seam]); d.line([(15, 0), (15, 15)], C[seam])
        d.line([(0, 0), (14, 0)], C[light])
    elif s == "tiles":
        for ox in (0, 8):
            for oy in (0, 8):
                d.rectangle([ox, oy, ox + 7, oy + 7], C[base])
                d.line([(ox, oy), (ox + 6, oy)], C[light])
                d.line([(ox + 7, oy), (ox + 7, oy + 7)], C[seam]); d.line([(ox, oy + 7), (ox + 7, oy + 7)], C[seam])
        noise(im, rnd, ["b5", dark], 6)
    elif s == "padded":
        for i in range(T):
            px(im, i, i, C[dark]); px(im, 15 - i, i, C[dark])
        for p in [(0, 0), (8, 8), (15, 0), (0, 15), (15, 15)]:
            px(im, *p, C[seam])
        noise(im, rnd, [light], 8)
    elif s == "corroded":
        noise(im, rnd, [dark, light, "r4"], 30)
        d.line([(0, 15), (15, 15)], C[dark])
    elif s == "checker":
        for ox in (0, 8):
            for oy in (0, 8):
                d.rectangle([ox, oy, ox + 7, oy + 7], C[base if (ox + oy) % 16 == 0 else light])
        d.line([(0, 15), (15, 15)], C[seam]); d.line([(15, 0), (15, 15)], C[seam])
        noise(im, rnd, [dark], 3)
    elif s == "grating":
        for gx in range(0, T, 4):
            for gy in range(0, T, 4):
                d.rectangle([gx + 1, gy + 1, gx + 2, gy + 2], C[seam])
                px(im, gx, gy, C[light])
    # variantes: desgaste extra
    if v >= 3:
        noise(im, rnd, [dark], 10 + v * 3)
    if v == 5 and s not in ("padded", "checker"):
        x, y = rnd.randrange(3, 12), rnd.randrange(3, 12)
        for _ in range(7):
            px(im, x, y, C[seam]); x += rnd.choice((-1, 0, 1)); y += 1
    return im


def floor_special(th, kind):
    base, dark, light, seam = th["f"]
    im = Image.new("RGBA", (T, T), C[base])
    d = ImageDraw.Draw(im)
    if kind == "grate":
        d.rectangle([1, 1, 14, 14], C["k1"]); d.rectangle([1, 1, 14, 14], outline=C["g2"])
        for x in range(3, 14, 3):
            d.line([(x, 2), (x, 13)], C["g1"])
    elif kind == "hazard":
        for x in range(-T, T * 2, 6):
            d.polygon([(x, 16), (x + 3, 16), (x + 19, 0), (x + 16, 0)], C["y3"])
        d.line([(0, 0), (15, 0)], C["k1"]); d.line([(0, 15), (15, 15)], C["k1"])
    elif kind == "mat":
        d.rectangle([1, 0, 14, 15], C["k2"])
        for y in range(2, 15, 3):
            d.line([(3, y), (12, y)], C["y2"])
        d.polygon([(8, 14), (5, 10), (11, 10)], C["y3"])
    return im


def wall(th, rnd, v):
    body, dark, light, stripe = th["w"]
    im = Image.new("RGBA", (T, T), C[body])
    d = ImageDraw.Draw(im)
    d.rectangle([0, 13, 15, 15], C["k2"])          # zócalo
    d.line([(0, 12), (15, 12)], C[dark])
    d.rectangle([0, 9, 15, 10], C[stripe])        # franja institucional
    noise(im, rnd, [dark], 6)
    if th["style"] == "padded":
        for x in range(0, T, 4):
            d.line([(x, 4), (x, 11)], C[dark])
    if th["style"] == "corroded":
        for _ in range(3):
            x = rnd.randrange(T); y = 4
            for _ in range(rnd.randrange(4, 9)):
                px(im, x, y, C["k0"]); y += 1
    if th["style"] == "biohazard" or th["style"] == "grating":
        for x in range(-T, T * 2, 4):
            d.line([(x, 10), (x + 1, 9)], C["k0"])
    if v == 1:  # tubo
        d.rectangle([0, 5, 15, 7], C["g2"]); d.line([(0, 5), (15, 5)], C["g4"]); d.line([(0, 7), (15, 7)], C["k3"])
        d.rectangle([6, 4, 8, 8], C["g1"])
    elif v == 2:  # ventila
        d.rectangle([3, 4, 12, 9], C["k1"]); d.rectangle([3, 4, 12, 9], outline=C["g3"])
        for y in (5, 7):
            d.line([(4, y), (11, y)], C["g1"])
    elif v == 3:  # aviso
        d.rectangle([4, 4, 11, 10], C["y3"]); d.rectangle([4, 4, 11, 10], outline=C["k0"])
        d.rectangle([7, 5, 8, 7], C["k0"]); d.rectangle([7, 9, 8, 9], C["k0"])
    elif v == 4:  # lámpara de pared
        d.rectangle([5, 4, 10, 6], C["g1"]); d.rectangle([6, 5, 9, 6], C["y3"])
    elif v == 5:  # puerta
        d.rectangle([2, 1, 13, 15], C["k3"]); d.rectangle([3, 2, 12, 15], C["g2"])
        d.line([(7, 2), (7, 15)], C["k2"]); d.line([(8, 2), (8, 15)], C["g3"])
        for y in range(11, 15, 2):
            d.line([(3, y), (12, y)], C["y2"])
        d.rectangle([6, 0, 9, 0], C["n4"])
    elif v == 9:  # puerta bloqueada (luz roja)
        d.rectangle([2, 1, 13, 15], C["k3"]); d.rectangle([3, 2, 12, 15], C["g1"])
        d.line([(7, 2), (7, 15)], C["k2"]); d.line([(8, 2), (8, 15)], C["g2"])
        for y in range(11, 15, 2):
            d.line([(3, y), (12, y)], C["e2"])
        d.rectangle([6, 0, 9, 0], C["e3"])
    elif v == 6:  # ventana de observación
        d.rectangle([2, 4, 13, 10], C["k0"]); d.rectangle([2, 4, 13, 10], outline=C["g4"])
        d.line([(4, 9), (8, 5)], C["b4"]); d.line([(6, 9), (10, 5)], C["b2"])
    elif v == 7:
        noise(im, rnd, ["k3", dark], 25)
    return im


def wall_upper(th, rnd):
    """Mitad alta del muro (2 tiles de alto dan profundidad 3/4)."""
    body, dark, light, stripe = th["w"]
    im = Image.new("RGBA", (T, T), C[body])
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 15, 2], C[light])
    d.line([(0, 3), (15, 3)], C[dark])
    d.line([(0, 15), (15, 15)], C[dark])
    noise(im, rnd, [dark, light], 8)
    if th["style"] == "padded":
        for x in range(0, T, 4):
            d.line([(x, 4), (x, 15)], C[dark])
    if th["style"] == "cold":
        for x in (2, 13):
            px(im, x, 6, C["b5"]); px(im, x, 12, C["b5"])
    return im


def wall_top(th, mask):
    body, dark, light, stripe = th["w"]
    im = Image.new("RGBA", (T, T), C[th["top"]])
    d = ImageDraw.Draw(im)
    for x in range(0, T, 4):
        for y in range(0, T, 4):
            px(im, x + (y // 4) % 2 * 2, y, C["k2"])
    if mask & 1: d.rectangle([0, 0, 15, 1], C[light])
    if mask & 2: d.rectangle([14, 0, 15, 15], C[dark]); d.line([(15, 0), (15, 15)], C[light])
    if mask & 4: d.rectangle([0, 14, 15, 15], C[light])
    if mask & 8: d.rectangle([0, 0, 1, 15], C[dark]); d.line([(0, 0), (0, 15)], C[light])
    return im


def decal(th, rnd, kind):
    im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if kind == 0:  # grieta
        x, y = 3, 2
        for _ in range(13):
            px(im, x, y, a(C["k0"], 200)); x += rnd.choice((0, 1)); y += 1
            if rnd.random() < 0.3: px(im, x + 1, y, a(C["k1"], 140))
    elif kind == 1:  # sangre
        d.ellipse([3, 5, 12, 11], a(C["e2"], 220)); d.ellipse([5, 6, 9, 9], a(C["e1"], 230))
        for p in [(2, 3), (13, 4), (12, 13), (4, 13), (14, 9)]:
            px(im, *p, a(C["e2"], 220))
    elif kind == 2:  # papeles
        d.rectangle([2, 4, 8, 11], C["g5"]); d.rectangle([7, 6, 13, 12], C["w"])
        for y in (8, 10): d.line([(8, y), (12, y)], C["g3"])
    elif kind == 3:  # charco
        col = {"corroded": "k0", "biohazard": "n3", "cold": "b5"}.get(th["style"], "k2")
        d.ellipse([2, 5, 13, 12], a(C[col], 170)); px(im, 5, 7, a(C["g4"], 150))
    elif kind == 4:  # cables
        for i in range(T):
            px(im, i, 8 + int(2 * ((i / 4) % 2)), a(C["k0"], 230)); px(im, i, 10 + int(((i + 2) / 5) % 2), C["e2"])
    elif kind == 5:  # sombra bajo muro
        for y in range(6):
            d.line([(0, y), (15, y)], (0, 0, 0, 110 - y * 18))
    elif kind == 6:  # sombra a la derecha del muro
        for x in range(4):
            d.line([(x, 0), (x, 15)], (0, 0, 0, 80 - x * 20))
    return im


def build(name, th):
    rnd = random.Random(name)
    atlas = Image.new("RGBA", (T * 16, T * 4), (0, 0, 0, 0))
    for v in range(6):
        atlas.paste(floor(th, rnd, v), (v * T, 0))
    for i, k in enumerate(("grate", "hazard", "mat")):
        atlas.paste(floor_special(th, k), ((6 + i) * T, 0))
    for v in range(8):
        atlas.paste(wall(th, rnd, v), (v * T, T))
    atlas.paste(wall_upper(th, rnd), (8 * T, T))
    atlas.paste(wall(th, rnd, 9), (9 * T, T))
    for m in range(16):
        atlas.paste(wall_top(th, m), (m * T, T * 2))
    for k in range(7):
        atlas.paste(decal(th, rnd, k), (k * T, T * 3))
    OUT.mkdir(parents=True, exist_ok=True)
    atlas.save(OUT / f"{name}.png")


def props():
    """Props 32x32 extra (los de PixelLab viven en art/props también)."""
    out = OUT.parent.parent / "props"
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([2, 14, 29, 18], C["r4"]); d.line([(2, 14), (29, 14)], C["r5"]); d.rectangle([2, 19, 29, 20], C["r2"])
    for x in (3, 27): d.rectangle([x, 21, x + 1, 30], C["r2"])
    d.rectangle([10, 3, 22, 12], C["k1"]); d.rectangle([11, 4, 21, 10], C["t3"]); d.line([(12, 6), (18, 6)], C["t4"]); d.line([(12, 8), (16, 8)], C["t4"])
    d.rectangle([15, 12, 17, 13], C["k2"]); d.rectangle([4, 12, 8, 13], C["w"]); d.rectangle([23, 12, 27, 13], C["k2"])
    im.save(out / "desk.png")
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle([2, 8, 29, 30], C["k3"]); d.rectangle([2, 8, 29, 30], outline=C["k1"]); d.line([(3, 9), (28, 9)], C["g2"])
    d.rectangle([5, 11, 18, 19], C["k0"]); d.rectangle([6, 12, 17, 18], C["n2"])
    for i, y in enumerate((13, 15, 17)): d.line([(7, y), (7 + 3 + i * 3, y)], C["n4"])
    for i, c in enumerate(("e3", "y3", "n4", "b4")): d.rectangle([21 + (i % 2) * 4, 12 + (i // 2) * 4, 22 + (i % 2) * 4, 13 + (i // 2) * 4], C[c])
    d.rectangle([5, 22, 26, 27], C["k2"])
    for x in range(6, 26, 3): d.line([(x, 23), (x, 26)], C["g1"])
    im.save(out / "console.png")
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for ox in (2, 16):
        d.rectangle([ox, 2, ox + 13, 30], C["g2"]); d.rectangle([ox, 2, ox + 13, 30], outline=C["k2"]); d.line([(ox + 1, 3), (ox + 12, 3)], C["g4"])
        for y in (6, 8, 10): d.line([(ox + 3, y), (ox + 10, y)], C["k3"])
        d.rectangle([ox + 10, 16, ox + 11, 19], C["g4"])
    im.save(out / "locker.png")


def items():
    """Íconos 16x16 de objetos (mapa e inventario)."""
    out = OUT.parent.parent / "items"
    out.mkdir(exist_ok=True)

    def icon(name, draw):
        im = Image.new("RGBA", (T, T), (0, 0, 0, 0))
        draw(ImageDraw.Draw(im), im)
        im.save(out / f"{name}.png")

    for lvl, col in enumerate(("g4", "n3", "b4", "y3", "e3"), 1):
        def card(d, im, col=col, lvl=lvl):
            d.rectangle([2, 4, 13, 12], C["w"]); d.rectangle([2, 4, 13, 12], outline=C["k1"])
            d.rectangle([3, 5, 12, 6], C[col]); d.rectangle([4, 8, 6, 10], C["y2"])
            for i in range(lvl): px(im, 8 + i, 10, C["k1"])
        icon(f"tarjeta_{lvl}", card)
    icon("botiquin", lambda d, im: (d.rectangle([2, 4, 13, 13], C["w"]), d.rectangle([2, 4, 13, 13], outline=C["k1"]),
         d.rectangle([6, 2, 9, 4], C["g3"]), d.rectangle([7, 6, 8, 11], C["e3"]), d.rectangle([5, 8, 10, 9], C["e3"])))
    icon("adrenalina", lambda d, im: (d.line([(3, 12), (11, 4)], C["g4"]), d.line([(4, 12), (12, 4)], C["y3"]),
         d.line([(2, 13), (3, 12)], C["g5"]), d.rectangle([12, 2, 13, 4], C["k1"])))
    icon("scp_500", lambda d, im: (d.ellipse([4, 5, 11, 10], C["e3"]), d.line([(5, 6), (7, 6)], C["w"]), d.line([(8, 5), (8, 10)], C["e1"])))
    icon("chaleco", lambda d, im: (d.polygon([(4, 2), (7, 4), (8, 4), (11, 2), (13, 5), (12, 14), (3, 14), (2, 5)], C["k3"]),
         d.rectangle([5, 7, 10, 11], C["g1"]), d.line([(5, 9), (10, 9)], C["y2"])))
    icon("municion", lambda d, im: (d.rectangle([2, 7, 13, 13], C["n2"]), d.rectangle([2, 7, 13, 13], outline=C["k1"]),
         [d.rectangle([x, 3, x + 1, 7], C["y3"]) for x in (4, 7, 10)], d.line([(4, 10), (11, 10)], C["n4"])))
    icon("capucha", lambda d, im: (d.polygon([(4, 3), (11, 3), (13, 13), (2, 13)], C["c2"]), d.line([(3, 11), (12, 11)], C["c1"]),
         d.line([(4, 3), (11, 3)], C["c3"])))
    icon("linterna", lambda d, im: (d.rectangle([2, 6, 9, 9], C["k3"]), d.polygon([(9, 5), (13, 3), (13, 12), (9, 10)], C["g2"]),
         d.line([(13, 4), (13, 11)], C["y3"]), d.rectangle([4, 7, 5, 8], C["e3"])))
    icon("sedante", lambda d, im: (d.rectangle([5, 3, 10, 4], C["g3"]), d.rectangle([5, 5, 10, 13], C["b5"]),
         d.rectangle([6, 8, 9, 12], C["b3"]), d.rectangle([5, 5, 10, 13], outline=C["k1"])))
    icon("senuelo", lambda d, im: (d.rectangle([2, 4, 13, 12], C["k3"]), d.ellipse([3, 6, 7, 10], C["g4"]), d.ellipse([8, 6, 12, 10], C["g4"]),
         d.rectangle([5, 8, 10, 8], C["k1"]), px(im, 12, 4, C["e3"])))
    icon("hcl", lambda d, im: (d.rectangle([4, 4, 11, 14], C["n3"]), d.rectangle([4, 4, 11, 14], outline=C["k1"]),
         d.rectangle([6, 2, 9, 3], C["g3"]), d.rectangle([5, 7, 10, 10], C["y3"]), d.line([(6, 8), (9, 9)], C["k1"])))
    icon("doc", lambda d, im: (d.rectangle([3, 2, 12, 14], C["c4"]), d.rectangle([3, 2, 12, 14], outline=C["c1"]),
         [d.line([(5, y), (10, y)], C["g2"]) for y in (5, 7, 9, 11)], d.rectangle([9, 11, 11, 13], C["e2"])))


if __name__ == "__main__":
    for n, th in THEMES.items():
        build(n, th)
    props()
    items()
    print("ok:", ", ".join(THEMES))
