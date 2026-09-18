"""Procedural art for Site-19: floors, walls, environmental traces, wall decor, doors,
item icons and UI frames. One fixed palette for the whole game.

Usage: python3 tools/gen_art.py   (requires Pillow)

Outputs (art/gen/):
  floors.png   16 cols x N rows  (row = floor material, see FLOORS; cols 0-3 = 2x2 macro slab,
                                  4-11 = variants, 12-15 = worn/detail)
  walls.png    16 cols x 2N rows (per wall material: row A = cols 0-7 lower face variants,
                                  8-11 upper face variants; row B = 16 top masks N1 E2 S4 W8)
  traces.png   16 x 8  transparent floor decals (dirt, blood, SCP traces)
  walldecor.png 16 x 4 transparent wall-face overlays
  doors.png    door sprites (see draw_doors)
  items/*.png  16x16 icons, ui/*.png frames
"""
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw

T = 16
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "art/gen"

# ------------------------------------------------------------------ palette
# One fixed palette. Cold institutional greys/blues, sick greens, rust, blood.
P = {
    "k0": "#07070b", "k1": "#101017", "k2": "#1a1a23", "k3": "#262631", "k4": "#33333f",
    "g1": "#44454f", "g2": "#575964", "g3": "#6d6f7a", "g4": "#878993", "g5": "#a4a6ae", "g6": "#c3c5cb", "w": "#e4e6e8",
    "b0": "#0f1822", "b1": "#1a2835", "b2": "#243a4c", "b3": "#355269", "b4": "#4f7089", "b5": "#7896ab", "b6": "#a9c1cf",
    "t1": "#142826", "t2": "#1f3d3a", "t3": "#2f5b55", "t4": "#4c827a", "t5": "#7fb2a7",
    "n1": "#17210f", "n2": "#263819", "n3": "#3f5a25", "n4": "#658a33", "n5": "#9ab94a", "n6": "#c8dc6e",
    "y1": "#3d3312", "y2": "#6e5a1c", "y3": "#a88a2a", "y4": "#d6b441", "y5": "#efd77a",
    "r1": "#24130e", "r2": "#3a1f15", "r3": "#58301d", "r4": "#7c4627", "r5": "#a56536", "r6": "#c98c55",
    "e0": "#230709", "e1": "#3c0c10", "e2": "#6a1419", "e3": "#9a1f22", "e4": "#c9362e",
    "c1": "#4a4439", "c2": "#6b6352", "c3": "#8f8670", "c4": "#b3aa90", "c5": "#d4cdb4",
    "o2": "#8a3d10", "o3": "#c2601a", "o4": "#e8892c", "o5": "#f6b25a",   # SCP-999 orange
    "p1": "#1c1022", "p2": "#2e1a36", "p3": "#48284f",                       # pocket dimension
}
C = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (255,) for k, v in P.items()}


def A(col, alpha):
    return C[col][:3] + (alpha,)


def new(w=T, h=T, fill=None):
    return Image.new("RGBA", (w, h), C[fill] if fill else (0, 0, 0, 0))


def px(im, x, y, col):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((int(x), int(y)), col if isinstance(col, tuple) else C[col])


def speckle(im, rnd, cols, n, box=None):
    x0, y0, x1, y1 = box or (0, 0, im.width - 1, im.height - 1)
    for _ in range(n):
        px(im, rnd.randint(x0, x1), rnd.randint(y0, y1), rnd.choice(cols))


def crack(im, rnd, col, x, y, length, dx=1):
    for _ in range(length):
        px(im, x, y, col)
        if rnd.random() < 0.35:
            px(im, x + 1, y, col)
        x += rnd.choice((0, dx, dx))
        y += rnd.choice((0, 1, 1))


def blob(im, rnd, cx, cy, r, col, alpha=255, jag=0.35):
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            d = math.hypot((x - cx) * 1.0, (y - cy) * 1.3)
            if d < r * (1 - jag * rnd.random()):
                px(im, x, y, A(col, alpha) if alpha < 255 else col)


def macro(draw_fn, rnd):
    """Draw a 32x32 slab and cut it in 4 tiles (removes the grid look)."""
    big = draw_fn(rnd)
    return [big.crop((x * T, y * T, x * T + T, y * T + T)) for y in (0, 1) for x in (0, 1)]


# ------------------------------------------------------------------ floors
# Each floor style: base fill, a 32px slab pattern, variants and details.

def slab_concrete(base, dark, light, seam):
    def draw(rnd):
        im = new(32, 32, base)
        speckle(im, rnd, [dark, light], 70)
        d = ImageDraw.Draw(im)
        d.line([(0, 31), (31, 31)], C[seam]); d.line([(31, 0), (31, 31)], C[seam])
        d.line([(0, 0), (30, 0)], C[light]); d.line([(0, 0), (0, 30)], C[light])
        return im
    return draw


def slab_tiles(base, alt, grout, light, cell=8):
    def draw(rnd):
        im = new(32, 32, grout)
        d = ImageDraw.Draw(im)
        for y in range(0, 32, cell):
            for x in range(0, 32, cell):
                col = base if (x // cell + y // cell) % 2 == 0 or alt is None else alt
                d.rectangle([x, y, x + cell - 2, y + cell - 2], C[col])
                d.line([(x, y), (x + cell - 3, y)], C[light])
        speckle(im, rnd, [grout], 8)
        return im
    return draw


def slab_carpet(base, dark, light):
    def draw(rnd):
        im = new(32, 32, base)
        for y in range(32):
            for x in range(32):
                if (x + y * 3) % 5 == 0:
                    px(im, x, y, dark)
                elif (x * 7 + y) % 11 == 0:
                    px(im, x, y, light)
        return im
    return draw


def slab_metal(base, dark, light):
    def draw(rnd):
        im = new(32, 32, base)
        d = ImageDraw.Draw(im)
        for y in range(2, 32, 6):
            for x in range(2 + (y // 6) % 2 * 3, 32, 6):
                d.line([(x, y + 1), (x + 2, y)], C[light]); px(im, x, y + 2, dark)
        d.rectangle([0, 0, 31, 31], outline=C[dark])
        for c in [(2, 2), (29, 2), (2, 29), (29, 29)]:
            px(im, *c, light); px(im, c[0] + 1, c[1] + 1, dark)
        speckle(im, rnd, [dark], 20)
        return im
    return draw


def slab_grate(base, hole, light):
    def draw(rnd):
        im = new(32, 32, base)
        d = ImageDraw.Draw(im)
        for y in range(0, 32, 4):
            for x in range(0, 32, 4):
                d.rectangle([x + 1, y + 1, x + 3, y + 3], C[hole])
                px(im, x, y, light)
        return im
    return draw


def slab_brick(base, dark, light, mortar):
    def draw(rnd):
        im = new(32, 32, mortar)
        d = ImageDraw.Draw(im)
        for row, y in enumerate(range(0, 32, 5)):
            off = 4 if row % 2 else 0
            for x in range(-8 + off, 32, 8):
                col = rnd.choice([base, base, dark, light])
                d.rectangle([x, y, x + 6, y + 3], C[col])
                d.line([(x, y), (x + 5, y)], C[light])
        speckle(im, rnd, ["k2"], 10)
        return im
    return draw


def slab_organic(base, dark, vein):
    def draw(rnd):
        im = new(32, 32, base)
        speckle(im, rnd, [dark], 160)
        for _ in range(4):
            x, y = rnd.randrange(32), rnd.randrange(32)
            for _ in range(18):
                px(im, x % 32, y % 32, vein)
                x += rnd.choice((-1, 0, 1)); y += rnd.choice((-1, 0, 1))
        return im
    return draw


def slab_soil(base, dark, light):
    def draw(rnd):
        im = new(32, 32, base)
        speckle(im, rnd, [dark, light, "r2"], 140)
        return im
    return draw


FLOORS = [
    # id, slab, variant detail colors (dirt, stain)
    ("concrete", slab_concrete("g2", "g1", "g3", "k4"), ("g1", "k3")),
    ("concrete_dark", slab_concrete("k4", "k3", "g1", "k2"), ("k3", "k1")),
    ("lino", slab_tiles("c3", None, "c2", "c4", cell=16), ("c2", "c1")),
    ("carpet", slab_carpet("b2", "b1", "b3"), ("b1", "k3")),
    ("whitetile", slab_tiles("g6", None, "g4", "w"), ("g4", "g3")),
    ("kitchen", slab_tiles("e2", "c4", "c2", "c5"), ("c2", "r3")),
    ("metal", slab_metal("g2", "k4", "g4"), ("k4", "k3")),
    ("grate", slab_grate("g1", "k0", "g3"), ("k1", "k0")),
    ("sewer", slab_brick("r3", "r2", "r4", "k3"), ("r2", "k2")),
    ("bathroom", slab_tiles("t4", "t5", "t2", "b6", cell=4), ("t2", "t1")),
    ("lead", slab_metal("k4", "k2", "g1"), ("k2", "k1")),
    ("organic", slab_organic("p1", "k1", "p3"), ("k1", "k0")),
    ("soil", slab_soil("r2", "r1", "r3"), ("r1", "k2")),
    ("steel", slab_metal("b2", "b1", "b4"), ("b1", "k3")),
    ("labtile", slab_tiles("g5", "g6", "g3", "w", cell=16), ("g3", "g2")),
]


def floor_row(fid, slab, detail, rnd):
    row = macro(slab, rnd)
    dirt, stain = detail
    for v in range(12):
        tile = macro(slab, random.Random(fid + str(v)))[v % 4]
        r2 = random.Random(fid + "v" + str(v))
        if v in (0, 1, 2, 3):          # plain alt slabs
            pass
        elif v in (4, 5):              # dirt
            speckle(tile, r2, [dirt], 18)
        elif v == 6:                   # crack
            crack(tile, r2, dirt, r2.randrange(3, 10), 1, 12)
        elif v == 7:                   # faint stain
            blob(tile, r2, r2.randrange(5, 11), r2.randrange(5, 11), 3.0, stain, 60, jag=0.5)
        elif v == 8:                   # worn edge
            for x in range(T):
                if r2.random() < 0.6:
                    px(tile, x, 15, dirt)
        elif v == 9:                   # small debris
            for _ in range(4):
                px(tile, r2.randrange(16), r2.randrange(16), "k2")
        elif v in (10, 11):            # grime
            speckle(tile, r2, [dirt, stain], 30)
        row.append(tile)
    return row


# ------------------------------------------------------------------ walls
# Walls are 2 tiles high on horizontal runs (upper + lower face) for 3/4 depth.
WALLS = [
    # id, body, dark, light, stripe, baseboard, top
    ("painted", "c3", "c2", "c4", "b3", "k3", "k1"),
    ("lab", "g6", "g4", "w", "t3", "g2", "k1"),
    ("steel", "b3", "b2", "b4", "y4", "k3", "k0"),
    ("brick", "r3", "r2", "r4", None, "k2", "k0"),
    ("tiled", "t4", "t3", "t5", "t2", "t2", "k1"),
    ("lead", "k4", "k3", "g1", "e3", "k2", "k0"),
    ("organic", "p2", "p1", "p3", None, "k1", "k0"),
    ("concrete", "g2", "g1", "g3", None, "k4", "k1"),
    ("hazard", "g1", "k4", "g2", "y4", "k2", "k0"),
]


def wall_lower(w, rnd, v):
    wid, body, dark, light, stripe, base, top = w
    im = new(T, T, body)
    d = ImageDraw.Draw(im)
    speckle(im, rnd, [dark], 8)
    if wid == "brick":
        for row, y in enumerate(range(0, 12, 4)):
            for x in range(-4 + (row % 2) * 4, 16, 8):
                d.rectangle([x, y, x + 6, y + 2], C[rnd.choice([body, dark, light])])
    elif wid == "tiled":
        for y in range(0, 12, 4):
            d.line([(0, y), (15, y)], C[dark])
        for x in range(0, 16, 4):
            d.line([(x, 0), (x, 11)], C[dark])
    elif wid in ("steel", "hazard", "lead"):
        d.line([(7, 0), (7, 11)], C[dark]); d.line([(8, 0), (8, 11)], C[light])
        for c in [(2, 2), (13, 2), (2, 9), (13, 9)]:
            px(im, *c, light)
    elif wid == "organic":
        speckle(im, rnd, ["k1", "p3"], 50)
    if stripe and wid == "hazard":
        for x in range(-16, 32, 4):
            d.line([(x, 11), (x + 3, 8)], C["k0"])
        d.rectangle([0, 8, 15, 11], outline=None)
    elif stripe:
        d.rectangle([0, 8, 15, 9], C[stripe])
    d.rectangle([0, 12, 15, 15], C[base])
    d.line([(0, 12), (15, 12)], C[light])
    if v == 1:    # water stain
        for x in range(rnd.randrange(2, 10), 16):
            if rnd.random() < 0.5:
                d.line([(x, 0), (x, rnd.randrange(3, 9))], A(dark, 180))
    elif v == 2:  # chipped
        speckle(im, rnd, ["k3", light], 14, (0, 0, 15, 11))
    elif v == 3:  # grime at base
        speckle(im, rnd, ["k3", "k2"], 20, (0, 9, 15, 12))
    return im


def wall_upper(w, rnd, v):
    wid, body, dark, light, stripe, base, top = w
    im = new(T, T, body)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 15, 1], C[light]); d.line([(0, 2), (15, 2)], C[dark])
    speckle(im, rnd, [dark, light], 10, (0, 3, 15, 15))
    if wid == "brick":
        for row, y in enumerate(range(3, 16, 4)):
            for x in range(-4 + (row % 2) * 4, 16, 8):
                d.rectangle([x, y, x + 6, y + 2], C[rnd.choice([body, dark, light])])
    elif wid == "tiled":
        for y in range(3, 16, 4):
            d.line([(0, y), (15, y)], C[dark])
        for x in range(0, 16, 4):
            d.line([(x, 3), (x, 15)], C[dark])
    elif wid in ("steel", "hazard", "lead"):
        d.line([(7, 3), (7, 15)], C[dark]); d.line([(8, 3), (8, 15)], C[light])
        for c in [(2, 5), (13, 5), (2, 13), (13, 13)]:
            px(im, *c, light)
    elif wid == "organic":
        speckle(im, rnd, ["k1", "p3"], 50)
    if v == 1:
        for x in range(rnd.randrange(0, 8), rnd.randrange(9, 16)):
            d.line([(x, 3), (x, rnd.randrange(6, 15))], A(dark, 160))
    elif v == 2:
        crack(im, rnd, dark, rnd.randrange(3, 12), 3, 10)
    return im


def wall_top(w, mask):
    wid, body, dark, light, stripe, base, top = w
    im = new(T, T, top)
    for y in range(0, T, 4):
        for x in range((y // 4) % 2 * 2, T, 4):
            px(im, x, y, "k2")
    d = ImageDraw.Draw(im)
    if mask & 1: d.rectangle([0, 0, 15, 1], C[light])
    if mask & 2: d.rectangle([14, 0, 15, 15], C[dark]); d.line([(15, 0), (15, 15)], C[light])
    if mask & 4: d.rectangle([0, 14, 15, 15], C[light])
    if mask & 8: d.rectangle([0, 0, 1, 15], C[dark]); d.line([(0, 0), (0, 15)], C[light])
    return im


# ------------------------------------------------------------------ traces
TRACES = [
    # row 0: dirt & debris
    "crack", "crack2", "oil", "dust", "debris", "papers", "glass", "cable",
    "casings", "ash", "bones", "droppings", "cheese", "lavender", "burn", "rubble",
    # row 1: blood
    "blood_splat", "blood_pool", "blood_drag_h", "blood_drag_v", "handprint", "footprints_h",
    "footprints_v", "blood_drops", "blood_smear", "vomit", "bandage", "syringe",
    "scalpel", "suture", "tray", "pills",
    # row 2: water / damp / 939
    "puddle", "puddle_big", "wet", "drip_ring", "red_residue", "red_residue2", "condensation", "mold",
    "moss", "slime_h", "slime_v", "wrappers", "gear", "copper", "oilpool", "rat_hole",
    # row 3: 173 / 106 / 682
    "scp173_stain", "scrape_h", "scrape_v", "cracked_radial", "corrosion", "corrosion2", "corrosion_trail",
    "rust", "acid", "acid2", "scorch", "gouge", "dissolved", "claw_floor", "pocket_eye", "chalk",
    # row 4: ambient occlusion under/next to walls
    "shade_n", "shade_w", "shade_e", "shade_nw", "shade_ne",
    # trail variants (alternated by the map DSL so trails don't look stamped)
    "blood_drag_h2", "blood_drag_v2", "blood_drag_h3", "blood_drag_v3", "scrape_h2", "scrape_v2",
]


def trace(name, rnd):
    im = new()
    d = ImageDraw.Draw(im)
    if name == "crack":
        crack(im, rnd, A("k1", 210), 3, 0, 16)
    elif name == "crack2":
        crack(im, rnd, A("k1", 200), 12, 2, 12, -1); crack(im, rnd, A("k1", 160), 6, 6, 8)
    elif name == "oil":
        blob(im, rnd, 8, 9, 5, A("k1", 170), jag=0.15); px(im, 6, 7, A("g3", 120))
    elif name == "dust":
        speckle(im, rnd, [A("c3", 90), A("g4", 80)], 40)
    elif name == "debris":
        for _ in range(7):
            x, y = rnd.randrange(14), rnd.randrange(14)
            d.rectangle([x, y, x + rnd.randrange(1, 3), y + 1], C[rnd.choice(["g3", "g2", "k4"])])
    elif name == "papers":
        d.polygon([(2, 5), (8, 3), (10, 9), (4, 11)], C["g6"]); d.polygon([(7, 8), (14, 8), (14, 14), (7, 14)], C["w"])
        for y in (10, 12): d.line([(8, y), (13, y)], C["g3"])
        d.line([(4, 6), (7, 5)], C["g3"])
    elif name == "glass":
        for _ in range(9):
            x, y = rnd.randrange(15), rnd.randrange(15)
            px(im, x, y, A("b6", 220)); px(im, x + 1, y, A("w", 160))
    elif name == "cable":
        pts = [(0, 9), (5, 7), (10, 11), (15, 8)]
        d.line(pts, C["k1"], 2); d.line([(p[0], p[1] - 1) for p in pts], C["g1"])
    elif name == "casings":
        for _ in range(5):
            x, y = rnd.randrange(14), rnd.randrange(14)
            d.line([(x, y), (x + 1, y)], C["y4"]); px(im, x + 2, y, C["y2"])
    elif name == "ash":
        blob(im, rnd, 8, 8, 6, A("k3", 150), jag=0.5); speckle(im, rnd, [A("g2", 150)], 12)
    elif name == "bones":
        d.line([(3, 11), (11, 5)], C["c5"], 2); px(im, 2, 12, C["w"]); px(im, 12, 4, C["w"])
        d.ellipse([9, 9, 13, 13], C["c4"]); px(im, 10, 10, C["k2"])
    elif name == "droppings":
        for _ in range(8):
            px(im, rnd.randrange(4, 12), rnd.randrange(4, 12), C["r1"])
    elif name == "cheese":
        d.polygon([(5, 10), (11, 7), (11, 11)], C["y4"]); px(im, 9, 9, C["y2"])
    elif name == "lavender":
        for sx in (5, 9):
            d.line([(sx, 13), (sx + 1, 6)], C["n3"])
            for y in range(5, 9): px(im, sx + 1 + (y % 2), y, C["p3"]); px(im, sx + (y % 2), y, (150, 110, 190, 255))
    elif name == "burn":
        blob(im, rnd, 8, 8, 7, A("k0", 150), jag=0.4); blob(im, rnd, 8, 8, 3, A("k1", 200))
    elif name == "rubble":
        for _ in range(6):
            x, y = rnd.randrange(12), rnd.randrange(12)
            d.polygon([(x, y + 3), (x + 2, y), (x + 4, y + 2), (x + 3, y + 4)], C[rnd.choice(["g2", "g3", "g1"])])
    elif name == "blood_splat":
        blob(im, rnd, 8, 8, 4, "e3"); blob(im, rnd, 8, 8, 2, "e2")
        for _ in range(8):
            a = rnd.random() * 6.28; r = rnd.uniform(5, 7.5)
            px(im, 8 + math.cos(a) * r, 8 + math.sin(a) * r, "e3")
    elif name == "blood_pool":
        blob(im, rnd, 8, 9, 6.5, "e2", jag=0.12); blob(im, rnd, 7, 8, 4, "e1", jag=0.1); px(im, 5, 6, "e4")
    elif name.startswith("blood_drag_"):
        horiz = name[len("blood_drag_")] == "h"
        off = rnd.uniform(0, 6.28)
        for i in range(16):
            half = 1.6 + 1.2 * math.sin(i / 2.7 + off) + rnd.uniform(-0.4, 0.4)
            center = 8 + math.sin(i / 4.0 + off) * 1.2
            for j in range(-4, 5):
                if abs(j) <= half and rnd.random() < 0.92 - abs(j) / (half + 1) * 0.5:
                    x, y = (i, center + j) if horiz else (center + j, i)
                    px(im, x, y, A(rnd.choice(["e2", "e2", "e3", "e1"]), rnd.randint(170, 235)))
            if rnd.random() < 0.15:
                x, y = (i, center + rnd.choice((-4, 4))) if horiz else (center + rnd.choice((-4, 4)), i)
                px(im, x, y, A("e3", 200))
    elif name == "handprint":
        blob(im, rnd, 8, 10, 3, "e3", jag=0.1)
        for i, fx in enumerate((5, 7, 9, 11)):
            d.line([(fx, 8), (fx + (i - 1.5) * 0.4, 4 + abs(i - 1.5))], C["e3"])
        d.line([(4, 10), (2, 8)], C["e3"])
    elif name in ("footprints_h", "footprints_v"):
        for k in range(3):
            x, y = (2 + k * 5, 5 if k % 2 else 10) if name.endswith("h") else (5 if k % 2 else 10, 2 + k * 5)
            d.ellipse([x, y, x + 2, y + 3], A("e3", 170))
    elif name == "blood_drops":
        for _ in range(7):
            x, y = rnd.randrange(2, 14), rnd.randrange(2, 14); px(im, x, y, "e3"); px(im, x + 1, y, "e2")
    elif name == "blood_smear":
        for i in range(12):
            d.line([(2 + i, 4 + i // 3), (4 + i, 10 + i // 4)], A("e2", 150))
    elif name == "vomit":
        blob(im, rnd, 8, 9, 5, A("y3", 200)); speckle(im, rnd, ["n3", "y2"], 10, (4, 5, 12, 13))
    elif name == "bandage":
        d.line([(3, 10), (12, 5)], C["w"], 2); px(im, 8, 7, "e3"); px(im, 9, 7, "e3")
    elif name == "syringe":
        d.line([(3, 12), (11, 4)], C["b6"]); d.line([(11, 4), (13, 2)], C["g5"]); px(im, 4, 11, "e3")
    elif name == "scalpel":
        d.line([(4, 11), (9, 6)], C["g2"]); d.line([(9, 6), (12, 3)], C["g6"])
    elif name == "suture":
        d.line([(2, 8), (14, 8)], C["k1"])
        for x in range(3, 14, 2): d.line([(x, 6), (x + 1, 10)], C["k1"])
    elif name == "tray":
        d.rectangle([2, 4, 13, 12], C["g4"]); d.rectangle([2, 4, 13, 12], outline=C["g2"])
        d.line([(4, 7), (9, 7)], C["g6"]); d.line([(5, 10), (11, 9)], C["g6"]); px(im, 11, 6, "e3")
    elif name == "pills":
        for _ in range(5):
            x, y = rnd.randrange(3, 12), rnd.randrange(3, 12); d.line([(x, y), (x + 1, y)], C[rnd.choice(["w", "b6", "y5"])])
    elif name == "puddle":
        blob(im, rnd, 8, 9, 4.5, A("b4", 120), jag=0.1); px(im, 6, 7, A("b6", 180)); px(im, 7, 7, A("w", 140))
    elif name == "puddle_big":
        blob(im, rnd, 8, 8, 7.5, A("b3", 120), jag=0.08); d.line([(4, 6), (7, 5)], A("b6", 170))
    elif name == "wet":
        for _ in range(12):
            x, y = rnd.randrange(15), rnd.randrange(15); px(im, x, y, A("b6", 90)); px(im, x + 1, y, A("b5", 60))
    elif name == "drip_ring":
        d.ellipse([4, 6, 11, 11], outline=A("b6", 120)); px(im, 8, 8, A("b6", 160))
    elif name in ("red_residue", "red_residue2"):
        blob(im, rnd, 8, 8, 5 if name == "red_residue" else 6.5, A("e4", 110), jag=0.25)
        speckle(im, rnd, [A("e3", 160), A("e4", 170)], 14, (2, 2, 13, 13))
    elif name == "condensation":
        for _ in range(16):
            x, y = rnd.randrange(16), rnd.randrange(16); px(im, x, y, A("b6", 120))
    elif name == "mold":
        blob(im, rnd, 8, 8, 6, A("n2", 170), jag=0.5); speckle(im, rnd, [A("n3", 200), A("k2", 200)], 18, (2, 2, 13, 13))
    elif name == "moss":
        speckle(im, rnd, [A("n3", 210), A("n2", 210), A("n4", 190)], 45)
    elif name in ("slime_h", "slime_v"):
        for i in range(16):
            for j in range(-2, 2):
                x, y = (i, 8 + j) if name.endswith("h") else (8 + j, i)
                px(im, x, y, A("o4", 150 if j in (-1, 0) else 90))
        px(im, 5, 8, A("o5", 220)) if name.endswith("h") else px(im, 8, 5, A("o5", 220))
    elif name == "wrappers":
        d.rectangle([3, 5, 7, 8], C["y4"]); d.line([(3, 6), (7, 6)], C["e3"])
        d.rectangle([9, 9, 13, 11], C["b4"]); px(im, 11, 10, C["w"]); px(im, 6, 12, C["o4"]); px(im, 12, 4, C["n4"])
    elif name == "gear":
        d.ellipse([4, 4, 11, 11], C["y3"]); d.ellipse([6, 6, 9, 9], C["y1"])
        for a in range(0, 360, 45):
            px(im, 7.5 + math.cos(math.radians(a)) * 5, 7.5 + math.sin(math.radians(a)) * 5, C["y4"])
    elif name == "copper":
        d.line([(2, 10), (8, 8), (13, 11)], C["r5"]); d.line([(3, 5), (6, 4)], C["r6"])
    elif name == "oilpool":
        blob(im, rnd, 8, 8, 6, A("k0", 190), jag=0.1); d.line([(5, 6), (8, 5)], A("p3", 200)); px(im, 10, 9, A("b4", 180))
    elif name == "rat_hole":
        d.ellipse([4, 8, 11, 13], C["k0"]); d.arc([4, 7, 11, 13], 180, 360, C["k3"])
    elif name == "scp173_stain":
        blob(im, rnd, 8, 9, 6, A("r1", 220), jag=0.4); blob(im, rnd, 9, 8, 3, A("e1", 230)); speckle(im, rnd, ["r2", "e2"], 10, (3, 4, 13, 13))
    elif name.startswith("scrape_"):
        horiz = name[len("scrape_")] == "h"
        off = rnd.randint(0, 5)
        for k in (-2, 0, 2):
            for i in range(16):
                if rnd.random() < 0.85:
                    wob = ((i + off) // 6) % 2
                    x, y = (i, 8 + k + wob) if horiz else (8 + k + wob, i)
                    px(im, x, y, A("k2", 150)); px(im, x + (0 if horiz else 1), y + (1 if horiz else 0), A("g4", 90))
    elif name == "cracked_radial":
        for a in range(0, 360, 60):
            x, y = 8.0, 8.0
            for r in range(7):
                px(im, x, y, A("k1", 220)); x += math.cos(math.radians(a + rnd.randint(-20, 20))); y += math.sin(math.radians(a + rnd.randint(-20, 20)))
        blob(im, rnd, 8, 8, 2, A("k1", 230))
    elif name in ("corrosion", "corrosion2"):
        blob(im, rnd, 8, 8, 5.5 if name == "corrosion" else 7, A("k0", 235), jag=0.35)
        blob(im, rnd, 8, 8, 3, A("p1", 240)); speckle(im, rnd, [A("n1", 220), A("r1", 220)], 12, (2, 2, 13, 13))
        px(im, 6, 6, A("g2", 200))
    elif name == "corrosion_trail":
        for i in range(16):
            for j in range(-2, 3):
                if rnd.random() < 0.8 - abs(j) * 0.18:
                    px(im, i, 8 + j + math.sin(i / 3) * 1.5, A("k0", 220))
    elif name == "rust":
        speckle(im, rnd, [A("r4", 200), A("r5", 180), A("r3", 200)], 55)
    elif name in ("acid", "acid2"):
        blob(im, rnd, 8, 8, 5 if name == "acid" else 7, A("n5", 170), jag=0.2)
        blob(im, rnd, 8, 8, 3, A("n6", 200)); px(im, 6, 7, C["w"]); px(im, 10, 9, A("y5", 220))
    elif name == "scorch":
        blob(im, rnd, 8, 8, 7, A("k1", 120), jag=0.3); speckle(im, rnd, [A("n4", 180), A("y3", 160)], 10, (3, 3, 12, 12))
    elif name == "gouge":
        for k in range(3):
            d.line([(3 + k * 4, 1), (1 + k * 4, 14)], C["k1"], 1); d.line([(4 + k * 4, 1), (2 + k * 4, 14)], A("g4", 150))
    elif name == "dissolved":
        blob(im, rnd, 8, 9, 5, A("n4", 150)); d.line([(4, 9), (11, 8)], C["c4"]); px(im, 11, 8, C["w"]); px(im, 5, 10, C["c5"])
    elif name == "claw_floor":
        for k in range(4):
            d.line([(2 + k * 3, 3), (5 + k * 3, 13)], C["k1"])
    elif name == "pocket_eye":
        d.ellipse([4, 6, 11, 10], A("p3", 220)); d.ellipse([7, 7, 8, 9], C["e4"])
    elif name.startswith("shade_"):
        side = name[6:]
        for i in range(7):
            a = int(120 * (1 - i / 7) ** 1.6)
            if "n" in side:
                d.line([(0, i), (15, i)], (0, 0, 0, a))
            if side in ("w", "nw"):
                d.line([(i, 0), (i, 15)], (0, 0, 0, a // 2))
            if side in ("e", "ne"):
                d.line([(15 - i, 0), (15 - i, 15)], (0, 0, 0, a // 2))
    elif name == "chalk":
        d.line([(2, 2), (13, 13)], A("w", 150)); d.line([(13, 2), (2, 13)], A("w", 150)); d.ellipse([4, 4, 11, 11], outline=A("w", 120))
    return im


# --------------------------------------------------------------- wall decor
WALLDECOR = [
    # row 0: institutional
    "logo", "clock", "extinguisher", "camera", "speaker", "lamp", "alarm", "vent",
    "pipe_h", "pipe_joint", "cables", "panel", "keypad", "poster", "poster2", "board",
    # row 1: damage & traces
    "scratches", "claws", "bullet_holes", "blood_hand", "blood_smear_w", "blood_write", "notes012", "crack_w",
    "corrosion_w", "corrosion_drip", "acid_burn_w", "water_stain", "mold_w", "graffiti", "scorched_w", "hole",
    # row 2: fixtures
    "window", "window_broken", "shelf", "mirror", "sink", "towel", "switch", "fusebox",
    "sign_blank", "sign_hazard", "sign_bio", "sign_radiation", "sign_exit", "screen", "screen_079", "red_light",
]


def walldecor(name, rnd):
    im = new()
    d = ImageDraw.Draw(im)
    if name == "logo":   # Foundation-like emblem: circle, three inward arrows
        d.ellipse([2, 1, 13, 12], outline=C["g6"]); d.ellipse([5, 4, 10, 9], outline=C["g6"])
        for a in (270, 30, 150):
            x, y = 7.5 + math.cos(math.radians(a)) * 5.5, 6.5 + math.sin(math.radians(a)) * 5.5
            d.line([(x, y), (7.5 + math.cos(math.radians(a)) * 3, 6.5 + math.sin(math.radians(a)) * 3)], C["w"])
    elif name == "clock":
        d.ellipse([4, 2, 11, 9], C["w"]); d.ellipse([4, 2, 11, 9], outline=C["k2"])
        d.line([(7.5, 5.5), (7.5, 3)], C["k1"]); d.line([(7.5, 5.5), (9.5, 6.5)], C["e3"])
    elif name == "extinguisher":
        d.rectangle([6, 4, 9, 12], C["e3"]); d.line([(6, 4), (6, 12)], C["e4"]); d.rectangle([6, 2, 8, 3], C["k2"])
        d.line([(9, 3), (11, 5)], C["k2"]); d.rectangle([6, 7, 9, 8], C["w"])
    elif name == "camera":
        d.rectangle([4, 3, 10, 6], C["g5"]); d.rectangle([10, 4, 12, 5], C["k2"]); d.line([(6, 7), (6, 9)], C["g2"]); px(im, 5, 4, C["e4"])
    elif name == "speaker":
        d.rectangle([5, 2, 10, 7], C["k3"]); d.ellipse([6, 3, 9, 6], C["k1"]); px(im, 7, 4, C["g2"])
    elif name == "lamp":
        d.rectangle([4, 2, 11, 4], C["g2"]); d.rectangle([5, 3, 10, 4], C["y5"])
    elif name == "alarm":
        d.rectangle([6, 2, 9, 3], C["k2"]); d.ellipse([5, 3, 10, 8], C["e3"]); px(im, 6, 4, C["e4"]); px(im, 7, 4, C["w"])
    elif name == "vent":
        d.rectangle([3, 2, 12, 8], C["k1"]); d.rectangle([3, 2, 12, 8], outline=C["g3"])
        for y in (4, 6): d.line([(4, y), (11, y)], C["g2"])
    elif name == "pipe_h":
        d.rectangle([0, 3, 15, 5], C["g2"]); d.line([(0, 3), (15, 3)], C["g4"]); d.line([(0, 5), (15, 5)], C["k3"])
    elif name == "pipe_joint":
        d.rectangle([0, 3, 15, 5], C["g2"]); d.line([(0, 3), (15, 3)], C["g4"]); d.rectangle([6, 2, 9, 6], C["g1"]); px(im, 7, 3, C["g5"])
        d.rectangle([7, 6, 8, 11], C["g2"]); d.ellipse([5, 8, 10, 11], C["e3"])
    elif name == "cables":
        for i, col in enumerate(("k1", "e2", "b3")):
            pts = [(x, 2 + i * 2 + int(math.sin(x / 3 + i) * 1.5)) for x in range(0, 16, 3)]
            d.line(pts, C[col])
    elif name == "panel":
        d.rectangle([3, 2, 12, 11], C["g1"]); d.rectangle([3, 2, 12, 11], outline=C["k2"])
        for i, col in enumerate(("n5", "y4", "e4")): px(im, 5 + i * 2, 4, C[col])
        d.rectangle([5, 6, 10, 9], C["k1"]); d.line([(6, 7), (9, 7)], C["n4"])
    elif name == "keypad":
        d.rectangle([5, 2, 10, 9], C["k3"]); d.rectangle([6, 3, 9, 4], C["n4"])
        for y in (6, 8):
            for x in (6, 8): px(im, x, y, C["g4"])
    elif name in ("poster", "poster2"):
        d.rectangle([3, 1, 12, 11], C["c5"] if name == "poster" else C["b5"]); d.rectangle([3, 1, 12, 11], outline=C["c2"])
        d.rectangle([5, 3, 10, 6], C["e3"] if name == "poster" else C["k3"])
        for y in (8, 9): d.line([(5, y), (10, y)], C["k3"])
    elif name == "board":
        d.rectangle([1, 2, 14, 11], C["r4"]); d.rectangle([1, 2, 14, 11], outline=C["r2"])
        for x, y, col in [(3, 4, "w"), (8, 3, "y5"), (5, 7, "g6"), (10, 7, "w")]:
            d.rectangle([x, y, x + 3, y + 2], C[col]); px(im, x + 1, y, C["e3"])
    elif name == "scratches":
        for k in range(3):
            d.line([(3 + k * 3, 1), (6 + k * 3, 11)], C["k1"]); d.line([(4 + k * 3, 1), (7 + k * 3, 11)], A("w", 70))
    elif name == "claws":
        for k in range(4):
            d.line([(1 + k * 3, 0), (4 + k * 3, 12)], C["k0"]); d.line([(2 + k * 3, 0), (5 + k * 3, 12)], A("g5", 90))
    elif name == "bullet_holes":
        for _ in range(4):
            x, y = rnd.randrange(2, 13), rnd.randrange(1, 10); px(im, x, y, C["k0"]); px(im, x + 1, y, A("g4", 150)); px(im, x, y + 1, A("g4", 120))
    elif name == "blood_hand":
        blob(im, rnd, 8, 7, 2.5, "e3", jag=0.1)
        for i, fx in enumerate((5, 7, 9, 11)):
            d.line([(fx, 5), (fx, 1 + abs(i - 1.5))], C["e3"])
        d.line([(8, 9), (8, 13)], A("e3", 170))
    elif name == "blood_smear_w":
        for i in range(10):
            d.line([(2 + i, 2), (1 + i, 12 - i // 3)], A("e2", 140))
    elif name == "blood_write":
        for x in range(1, 15, 3):
            d.line([(x, 2 + rnd.randint(0, 2)), (x + 2, 5 + rnd.randint(0, 3))], C["e3"])
        d.line([(1, 9), (14, 9)], A("e3", 150))
    elif name == "notes012":   # staff lines + notes written in blood
        for y in (2, 4, 6, 8, 10):
            d.line([(0, y), (15, y)], A("e2", 200))
        for x in range(1, 15, 4):
            y = rnd.choice((3, 5, 7, 9)); d.ellipse([x, y - 1, x + 2, y + 1], C["e3"]); d.line([(x + 2, y), (x + 2, y - 4)], C["e3"])
    elif name == "crack_w":
        crack(im, rnd, A("k1", 220), rnd.randrange(4, 11), 0, 12)
    elif name == "corrosion_w":
        blob(im, rnd, 8, 6, 5, A("k0", 230), jag=0.4); speckle(im, rnd, [A("n1", 220), A("r2", 220)], 12, (2, 1, 13, 11))
    elif name == "corrosion_drip":
        for x in (4, 7, 11):
            d.line([(x, 0), (x, rnd.randrange(6, 12))], A("k0", 230)); px(im, x, 12, A("k0", 200))
    elif name == "acid_burn_w":
        blob(im, rnd, 8, 7, 5, A("n4", 150)); speckle(im, rnd, [A("n6", 180), A("k1", 200)], 14, (2, 2, 13, 12))
    elif name == "water_stain":
        for x in range(2, 14):
            if rnd.random() < 0.6: d.line([(x, 0), (x, rnd.randrange(4, 11))], A("r3", 90))
    elif name == "mold_w":
        speckle(im, rnd, [A("n2", 220), A("n3", 200), A("k2", 200)], 60, (0, 0, 15, 11))
    elif name == "graffiti":
        d.line([(2, 8), (4, 3), (6, 8)], C["e4"]); d.line([(3, 6), (5, 6)], C["e4"])
        d.line([(8, 3), (8, 8), (11, 8)], C["e4"]); d.line([(12, 3), (13, 8)], C["e4"])
    elif name == "scorched_w":
        blob(im, rnd, 8, 6, 6, A("k1", 170), jag=0.3)
    elif name == "hole":
        blob(im, rnd, 8, 6, 4, "k0", jag=0.2); d.arc([3, 1, 13, 11], 200, 340, C["g1"])
    elif name in ("window", "window_broken"):
        d.rectangle([1, 1, 14, 10], C["k1"]); d.rectangle([1, 1, 14, 10], outline=C["g4"]); d.line([(7, 1), (7, 10)], C["g4"])
        if name == "window":
            d.line([(3, 8), (6, 3)], A("b5", 200)); d.line([(9, 8), (12, 3)], A("b4", 160))
        else:
            d.line([(3, 2), (6, 6), (4, 9)], C["b6"]); d.line([(10, 2), (9, 5), (12, 8)], C["b6"]); speckle(im, rnd, [C["b6"]], 5, (2, 2, 13, 9))
    elif name == "shelf":
        d.rectangle([1, 6, 14, 7], C["r4"]); d.rectangle([2, 2, 4, 5], C["b4"]); d.rectangle([5, 3, 7, 5], C["e3"]); d.rectangle([10, 1, 12, 5], C["y3"])
    elif name == "mirror":
        d.rectangle([4, 1, 11, 10], C["g5"]); d.rectangle([5, 2, 10, 9], C["b5"]); d.line([(6, 7), (9, 3)], C["b6"])
    elif name == "sink":
        d.rectangle([3, 8, 12, 11], C["g6"]); d.rectangle([4, 9, 11, 10], C["g4"]); d.line([(7, 5), (7, 8)], C["g3"]); d.line([(7, 5), (9, 5)], C["g3"])
    elif name == "towel":
        d.line([(3, 2), (12, 2)], C["g3"]); d.rectangle([5, 3, 10, 10], C["w"]); d.line([(5, 8), (10, 8)], C["b4"])
    elif name == "switch":
        d.rectangle([6, 4, 9, 8], C["g6"]); d.rectangle([7, 5, 8, 6], C["g3"])
    elif name == "fusebox":
        d.rectangle([3, 1, 12, 11], C["g2"]); d.rectangle([3, 1, 12, 11], outline=C["k2"]); d.polygon([(7, 3), (5, 7), (8, 7), (6, 10), (10, 5), (7, 5)], C["y4"])
    elif name in ("sign_blank", "sign_hazard", "sign_bio", "sign_radiation", "sign_exit"):
        bg = {"sign_blank": "g5", "sign_hazard": "y4", "sign_bio": "y4", "sign_radiation": "y4", "sign_exit": "n3"}[name]
        d.rectangle([2, 2, 13, 10], C[bg]); d.rectangle([2, 2, 13, 10], outline=C["k1"])
        if name == "sign_hazard":
            d.rectangle([7, 3, 8, 7], C["k0"]); d.rectangle([7, 9, 8, 9], C["k0"])
        elif name == "sign_bio":
            for a in (270, 30, 150):
                x, y = 7.5 + math.cos(math.radians(a)) * 2, 6 + math.sin(math.radians(a)) * 2
                d.ellipse([x - 2, y - 2, x + 2, y + 2], outline=C["k0"])
        elif name == "sign_radiation":
            d.ellipse([6, 5, 9, 8], C["k0"]); d.pieslice([3, 2, 12, 11], 240, 300, C["k0"]); d.pieslice([3, 2, 12, 11], 0, 60, C["k0"]); d.pieslice([3, 2, 12, 11], 120, 180, C["k0"])
        elif name == "sign_exit":
            d.polygon([(4, 6), (8, 3), (8, 5), (11, 5), (11, 7), (8, 7), (8, 9)], C["w"])
    elif name == "screen":
        d.rectangle([2, 1, 13, 9], C["k2"]); d.rectangle([3, 2, 12, 8], C["t2"])
        for y in (3, 5, 7): d.line([(4, y), (4 + rnd.randrange(3, 8), y)], C["t5"])
    elif name == "screen_079":
        d.rectangle([2, 1, 13, 9], C["k2"]); d.rectangle([3, 2, 12, 8], C["k0"])
        d.line([(4, 3), (11, 7)], C["e4"]); d.line([(11, 3), (4, 7)], C["e4"])
    elif name == "red_light":
        d.rectangle([6, 1, 9, 2], C["k2"]); d.ellipse([5, 2, 10, 7], C["e4"]); px(im, 7, 3, C["w"])
    return im


# ------------------------------------------------------------------- doors
def draw_doors():
    """doors.png: 4 styles x (frame 32x32, left panel 16x32, right panel 16x32, v-door 16x32)."""
    styles = [("std", "g3", "g4", "g2", "y4"), ("lab", "g5", "g6", "g3", "t3"),
              ("heavy", "g1", "g2", "k4", "y4"), ("rust", "r3", "r4", "r2", "e3")]
    sheet = new(64 + 16, 32 * len(styles))
    for i, (sid, body, light, dark, stripe) in enumerate(styles):
        y0 = i * 32
        fr = new(32, 32); d = ImageDraw.Draw(fr)
        d.rectangle([0, 0, 31, 31], C["k2"]); d.rectangle([2, 2, 29, 31], C["k0"])
        d.rectangle([0, 0, 31, 3], C[dark]); d.line([(0, 0), (31, 0)], C[light])
        d.rectangle([0, 0, 1, 31], C[dark]); d.rectangle([30, 0, 31, 31], C[dark])
        sheet.paste(fr, (0, y0))
        for side, x0 in (("L", 32), ("R", 48)):
            p = new(16, 32); d = ImageDraw.Draw(p)
            d.rectangle([0, 3, 15, 31], C[body]); d.line([(0, 3), (15, 3)], C[light])
            edge = 15 if side == "L" else 0
            d.line([(edge, 3), (edge, 31)], C["k2"])
            for y in range(24, 31, 2):
                d.line([(0, y), (15, y)], C[stripe])
            d.rectangle([3, 8, 12, 14], C[dark]); d.line([(3, 8), (12, 8)], C["k3"])
            if sid == "heavy":
                for yy in (18, 21):
                    d.line([(0, yy), (15, yy)], C["k3"])
            if sid == "rust":
                speckle(p, random.Random(side), ["r2", "r5", "k3"], 40, (0, 3, 15, 31))
            sheet.paste(p, (x0, y0))
        v = new(16, 32); d = ImageDraw.Draw(v)
        d.rectangle([4, 0, 11, 31], C[body]); d.line([(4, 0), (4, 31)], C[light]); d.line([(11, 0), (11, 31)], C[dark])
        d.rectangle([5, 12, 10, 19], C[stripe])
        sheet.paste(v, (64, y0))
    sheet.save(OUT / "doors.png")


# ------------------------------------------------------------------- items
def items():
    out = ROOT / "art/items"
    out.mkdir(parents=True, exist_ok=True)

    def icon(name, fn):
        im = new(); d = ImageDraw.Draw(im); fn(d, im); im.save(out / f"{name}.png")

    for lvl, col in enumerate(("g5", "n4", "b5", "y4", "e4", "p3"), 1):
        def card(d, im, col=col, lvl=lvl):
            d.rectangle([2, 4, 13, 12], C["w"]); d.rectangle([2, 4, 13, 12], outline=C["k1"])
            d.rectangle([3, 5, 12, 6], C[col]); d.rectangle([4, 8, 6, 10], C["y3"])
            for i in range(min(lvl, 5)): px(im, 8 + i, 10, "k1")
        icon(f"card_{lvl}" if lvl <= 5 else "card_omni", card)
    icon("medkit", lambda d, im: (d.rectangle([2, 4, 13, 13], C["w"]), d.rectangle([2, 4, 13, 13], outline=C["k1"]),
         d.rectangle([6, 2, 9, 4], C["g3"]), d.rectangle([7, 6, 8, 11], C["e3"]), d.rectangle([5, 8, 10, 9], C["e3"])))
    icon("bandage", lambda d, im: (d.ellipse([3, 5, 12, 12], C["c5"]), d.ellipse([6, 7, 9, 10], C["c3"]), d.line([(10, 10), (14, 13)], C["c5"], 2)))
    icon("adrenaline", lambda d, im: (d.line([(3, 12), (11, 4)], C["g4"]), d.line([(4, 12), (12, 4)], C["y4"]),
         d.line([(2, 13), (3, 12)], C["g6"]), d.rectangle([12, 2, 13, 4], C["k1"])))
    icon("scp500", lambda d, im: (d.ellipse([4, 5, 11, 10], C["e3"]), d.line([(5, 6), (7, 6)], C["w"]), d.line([(8, 5), (8, 10)], C["e1"])))
    icon("battery", lambda d, im: (d.rectangle([4, 4, 11, 13], C["k3"]), d.rectangle([6, 2, 9, 3], C["g4"]),
         d.rectangle([5, 9, 10, 12], C["n5"]), d.rectangle([5, 5, 10, 8], C["g2"]), px(im, 7, 6, "y5")))
    icon("ammo", lambda d, im: (d.rectangle([2, 7, 13, 13], C["n2"]), d.rectangle([2, 7, 13, 13], outline=C["k1"]),
         [d.rectangle([x, 3, x + 1, 7], C["y4"]) for x in (4, 7, 10)], d.line([(4, 10), (11, 10)], C["n4"])))
    icon("pistol", lambda d, im: (d.rectangle([2, 5, 13, 7], C["k3"]), d.rectangle([3, 8, 6, 12], C["k2"]), px(im, 12, 5, "g4"), d.line([(7, 8), (8, 9)], C["k3"])))
    icon("baton", lambda d, im: (d.line([(3, 13), (12, 3)], C["k3"], 2), d.line([(3, 13), (5, 11)], C["g2"], 2)))
    icon("vest", lambda d, im: (d.polygon([(4, 2), (7, 4), (8, 4), (11, 2), (13, 5), (12, 14), (3, 14), (2, 5)], C["k4"]),
         d.rectangle([5, 7, 10, 11], C["g1"]), d.line([(5, 9), (10, 9)], C["y3"])))
    icon("bag096", lambda d, im: (d.polygon([(4, 3), (11, 3), (13, 13), (2, 13)], C["c3"]), d.line([(3, 11), (12, 11)], C["c2"]), d.line([(4, 3), (11, 3)], C["c4"])))
    icon("lavender", lambda d, im: [(d.line([(x, 13), (x + 1, 4)], C["n3"]), [px(im, x + 1 + (y % 2), y, (150, 110, 190, 255)) for y in range(3, 8)]) for x in (5, 9)])
    icon("recorder", lambda d, im: (d.rectangle([2, 4, 13, 12], C["k3"]), d.ellipse([3, 6, 7, 10], C["g4"]), d.ellipse([8, 6, 12, 10], C["g4"]),
         d.rectangle([5, 8, 10, 8], C["k1"]), px(im, 12, 4, "e4")))
    icon("hcl", lambda d, im: (d.rectangle([4, 4, 11, 14], C["n4"]), d.rectangle([4, 4, 11, 14], outline=C["k1"]),
         d.rectangle([6, 2, 9, 3], C["g3"]), d.rectangle([5, 7, 10, 10], C["y4"]), d.line([(6, 8), (9, 9)], C["k1"])))
    icon("doc", lambda d, im: (d.rectangle([3, 2, 12, 14], C["c5"]), d.rectangle([3, 2, 12, 14], outline=C["c1"]),
         [d.line([(5, y), (10, y)], C["g2"]) for y in (5, 7, 9, 11)], d.rectangle([9, 11, 11, 13], C["e2"])))
    icon("tape", lambda d, im: (d.rectangle([2, 4, 13, 12], C["k2"]), d.ellipse([4, 6, 7, 9], C["w"]), d.ellipse([8, 6, 11, 9], C["w"]), d.line([(4, 11), (11, 11)], C["g3"])))
    icon("coin", lambda d, im: (d.ellipse([4, 4, 11, 11], C["g5"]), d.ellipse([5, 5, 10, 10], C["g4"]), px(im, 6, 6, "w")))
    icon("fuse", lambda d, im: (d.rectangle([5, 3, 10, 12], C["b6"]), d.rectangle([5, 3, 10, 4], C["g4"]), d.rectangle([5, 11, 10, 12], C["g4"]), d.line([(7, 5), (8, 10)], C["y4"])))
    icon("dogtag", lambda d, im: (d.rounded_rectangle([4, 5, 11, 13], 2, C["g5"]), d.line([(6, 8), (9, 8)], C["g2"]), d.line([(6, 10), (9, 10)], C["g2"]), d.line([(7, 1), (7, 5)], C["g4"])))
    icon("candy", lambda d, im: (d.ellipse([5, 5, 10, 10], C["o4"]), d.polygon([(2, 5), (5, 7), (2, 10)], C["o3"]), d.polygon([(13, 5), (10, 7), (13, 10)], C["o3"])))
    icon("coffee", lambda d, im: (d.polygon([(4, 4), (11, 4), (10, 13), (5, 13)], C["w"]), d.rectangle([5, 5, 10, 6], C["r3"]), d.line([(6, 1), (7, 3)], A("g5", 150))))
    icon("key", lambda d, im: (d.ellipse([2, 5, 7, 10], C["y4"]), d.ellipse([4, 7, 5, 8], (0, 0, 0, 0)), d.line([(7, 7), (13, 7)], C["y4"]), px(im, 12, 8, "y4"), px(im, 10, 8, "y4")))
    icon("nvg", lambda d, im: (d.rectangle([2, 6, 13, 10], C["k3"]), d.ellipse([3, 6, 7, 10], C["n5"]), d.ellipse([8, 6, 12, 10], C["n5"])))
    icon("radio", lambda d, im: (d.rectangle([4, 4, 11, 14], C["k3"]), d.line([(10, 4), (10, 0)], C["g3"]), d.rectangle([5, 6, 10, 8], C["n4"]), [px(im, x, 11, "g2") for x in (5, 7, 9)]))
    icon("map", lambda d, im: (d.polygon([(2, 4), (6, 2), (10, 4), (14, 2), (14, 12), (10, 14), (6, 12), (2, 14)], C["c4"]), d.line([(6, 2), (6, 12)], C["c2"]), d.line([(10, 4), (10, 14)], C["c2"]), px(im, 8, 8, "e3")))


# ---------------------------------------------------------------------- UI
def ui():
    out = OUT / "ui"
    out.mkdir(parents=True, exist_ok=True)
    # 9-slice panel 24x24 (8px corners): dark glass with steel bevel and rivets
    for name, edge, accent in (("panel", "g2", "g4"), ("panel_warn", "e2", "e4"), ("panel_gold", "y2", "y4")):
        im = new(24, 24); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 23, 23], A("k1", 235))
        d.rectangle([0, 0, 23, 23], outline=C["k0"]); d.rectangle([1, 1, 22, 22], outline=C[edge])
        d.line([(2, 2), (21, 2)], C[accent]); d.line([(2, 2), (2, 21)], C[accent])
        for c in [(3, 3), (20, 3), (3, 20), (20, 20)]:
            px(im, *c, accent)
        im.save(out / f"{name}.png")
    # status icons 8x8
    icons = {
        "i_heart": lambda d, im: (d.polygon([(1, 2), (2, 1), (4, 3), (6, 1), (7, 2), (7, 3), (4, 7), (1, 3)], C["e4"]), px(im, 2, 2, "w")),
        "i_battery": lambda d, im: (d.rectangle([0, 2, 6, 6], outline=C["g5"]), d.rectangle([7, 3, 7, 5], C["g5"]), d.rectangle([1, 3, 5, 5], C["n5"])),
        "i_brain": lambda d, im: (d.ellipse([0, 1, 7, 7], C["p3"]), d.line([(4, 1), (4, 7)], C["p1"]), px(im, 2, 3, "w")),
        "i_lungs": lambda d, im: (d.ellipse([0, 1, 3, 7], C["b5"]), d.ellipse([4, 1, 7, 7], C["b5"]), d.line([(3, 0), (4, 0)], C["g5"])),
        "i_eye": lambda d, im: (d.ellipse([0, 2, 7, 6], C["w"]), d.ellipse([2, 2, 5, 6], C["b4"]), px(im, 3, 4, "k0")),
        "i_ammo": lambda d, im: ([d.rectangle([x, 1, x + 1, 6], C["y4"]) for x in (1, 4)],),
    }
    for name, fn in icons.items():
        im = new(8, 8); d = ImageDraw.Draw(im); fn(d, im); im.save(out / f"{name}.png")
    # Foundation-style emblem (original drawing: circle, ring, three inward arrows)
    im = new(48, 48); d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 45, 45], outline=C["g6"], width=3); d.ellipse([13, 13, 34, 34], outline=C["g6"], width=2)
    for a in (270, 30, 150):
        r = math.radians(a)
        tip = (23.5 + math.cos(r) * 11, 23.5 + math.sin(r) * 11)
        base = (23.5 + math.cos(r) * 24, 23.5 + math.sin(r) * 24)
        side = (math.cos(r + 1.57) * 4, math.sin(r + 1.57) * 4)
        d.polygon([tip, (base[0] + side[0], base[1] + side[1]), (base[0] - side[0], base[1] - side[1])], C["w"])
    im.save(out / "emblem.png")
    # radio "portrait": handheld radio on static
    rnd = random.Random(7)
    im = new(64, 64, "k1"); d = ImageDraw.Draw(im)
    for _ in range(500):
        px(im, rnd.randrange(64), rnd.randrange(64), rnd.choice(["k2", "k3", "g1"]))
    d.rectangle([22, 14, 42, 56], C["k3"]); d.rectangle([22, 14, 42, 56], outline=C["g2"])
    d.line([(38, 14), (38, 2)], C["g3"], 2); d.rectangle([25, 18, 39, 27], C["n2"])
    for x in range(26, 39, 3): d.line([(x, 20), (x, 25)], C["n4"])
    for y in range(32, 52, 4):
        for x in range(26, 39, 4): px(im, x, y, "g2")
    im.save(out / "radio.png")
    # SCP-079 "portrait": CRT with the ASCII X it shows when it refuses to talk
    im = new(64, 64, "k0"); d = ImageDraw.Draw(im)
    d.rectangle([4, 6, 59, 50], C["k3"]); d.rectangle([8, 10, 55, 46], C["k1"])
    for i in range(0, 34, 3):
        px(im, 14 + i, 13 + i, "e4"); px(im, 15 + i, 13 + i, "e3")
        px(im, 48 - i, 13 + i, "e4"); px(im, 49 - i, 13 + i, "e3")
    for y in range(10, 47, 2):
        d.line([(8, y), (55, y)], (0, 0, 0, 90))
    d.rectangle([20, 52, 43, 58], C["k3"])
    im.save(out / "079.png")


# -------------------------------------------------------------------- build
def build():
    OUT.mkdir(parents=True, exist_ok=True)
    fl = new(T * 16, T * len(FLOORS))
    for r, (fid, slab, detail) in enumerate(FLOORS):
        for c, tile in enumerate(floor_row(fid, slab, detail, random.Random(fid))):
            fl.paste(tile, (c * T, r * T))
    fl.save(OUT / "floors.png")

    wl = new(T * 16, T * 2 * len(WALLS))
    for r, w in enumerate(WALLS):
        rnd = random.Random(w[0])
        for v in range(8):
            wl.paste(wall_lower(w, rnd, v % 4), (v * T, r * 2 * T))
        for v in range(4):
            wl.paste(wall_upper(w, rnd, v % 3), ((8 + v) * T, r * 2 * T))
        for m in range(16):
            wl.paste(wall_top(w, m), (m * T, (r * 2 + 1) * T))
    wl.save(OUT / "walls.png")

    tr = new(T * 16, T * ((len(TRACES) + 15) // 16))
    for i, name in enumerate(TRACES):
        tr.paste(trace(name, random.Random(name)), ((i % 16) * T, (i // 16) * T))
    tr.save(OUT / "traces.png")

    wd = new(T * 16, T * ((len(WALLDECOR) + 15) // 16))
    for i, name in enumerate(WALLDECOR):
        wd.paste(walldecor(name, random.Random(name)), ((i % 16) * T, (i // 16) * T))
    wd.save(OUT / "walldecor.png")

    draw_doors()
    items()
    ui()
    # index for the engine / map builder
    import json
    (OUT / "index.json").write_text(json.dumps({
        "floors": [f[0] for f in FLOORS], "walls": [w[0] for w in WALLS],
        "traces": TRACES, "walldecor": WALLDECOR}, indent=1))
    print("ok:", len(FLOORS), "floors,", len(WALLS), "walls,", len(TRACES), "traces,", len(WALLDECOR), "wall decor")


if __name__ == "__main__":
    build()
