"""Tiny DSL to author Site-19 maps in Python. Used by tools/build_maps.py.

Coordinates are tiles. A map starts as solid rock; `room()` carves floor. Walls take the
material of the room they bound. Horizontal walls should be 2 tiles thick (3/4 depth);
`room(x, y, w, h)` carves the floor rect only, so leave 2 rows between rooms stacked
vertically and 1 column between rooms side by side.
"""
import json
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data/maps"

# material code -> (floor, wall)
MATS = {
    "a": ("concrete", "concrete"),
    "e": ("lino", "painted"),          # entrance zone offices
    "c": ("carpet", "painted"),
    "l": ("labtile", "lab"),           # light containment labs
    "w": ("whitetile", "lab"),         # medical
    "k": ("kitchen", "tiled"),
    "b": ("bathroom", "tiled"),
    "m": ("metal", "steel"),           # heavy containment
    "h": ("metal", "hazard"),
    "g": ("grate", "steel"),
    "s": ("sewer", "brick"),
    "d": ("concrete_dark", "concrete"),
    "p": ("organic", "organic"),       # pocket dimension
    "o": ("soil", "lab"),
    "x": ("lead", "lead"),             # 106
    "t": ("steel", "steel"),
    "r": ("concrete_dark", "brick"),
}


def L(en, es):
    return {"en": en, "es": es}


class Map:
    def __init__(self, mid, name, w, h, sector, env=None):
        self.id, self.name, self.w, self.h, self.sector = mid, name, w, h, sector
        self.g = [["#"] * w for _ in range(h)]
        self.m = [["a"] * w for _ in range(h)]
        self.carved = [[False] * w for _ in range(h)]
        self.env = {"ambient": "#343844", "fog": 0.0, "fog_color": "#8a8f9a", "amb": "", "dust": 0.3}
        if env:
            self.env.update(env)
        self.traces, self.walldecor, self.props, self.lights = [], [], [], []
        self.doors, self.exits, self.spawns, self.npcs, self.items = [], {}, {}, [], []
        self.triggers, self.interact, self.fx, self.vermin, self.sounds, self.signs = [], [], [], [], [], []
        self.actors, self.rooms = [], []
        self.exits = []
        self.rnd = random.Random(mid)

    # ------------------------------------------------------------- structure
    def room(self, x, y, w, h, mat="a", name=None):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._floor(xx, yy, mat)
        # walls around take the room material (unless already floor)
        for yy in range(y - 2, y + h + 1):
            for xx in range(x - 1, x + w + 1):
                if 0 <= xx < self.w and 0 <= yy < self.h and not self.carved[yy][xx]:
                    self.m[yy][xx] = mat
        if name:
            self.rooms.append({"name": name, "rect": [x, y, w, h]})
        return self

    def _floor(self, x, y, mat, c="."):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c
            self.m[y][x] = mat
            self.carved[y][x] = True

    def fill(self, x, y, w, h, c, mat=None):
        """Set structure char (e.g. '~' shallow water, '=' deep water/acid, '#' pillar)."""
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.g[yy][xx] = c
                if mat:
                    self.m[yy][xx] = mat
                self.carved[yy][xx] = c != "#"

    def wall(self, x, y, w, h):
        self.fill(x, y, w, h, "#")

    def gap(self, x, y, w, h, mat=None):
        """Open a passage through a wall without a door."""
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self._floor(xx, yy, mat or self.m[yy][xx])

    def door(self, x, y, d="h", level=0, style="std", lock="", did=None, mat=None):
        """h: 2x2 gap at (x,y) in a 2-thick horizontal wall. v: 1x2 gap in a vertical wall."""
        w, h = (2, 2) if d == "h" else (1, 2)
        self.gap(x, y, w, h, mat)
        self.doors.append({"x": x, "y": y, "dir": d, "level": level, "style": style, "lock": lock,
                           "id": did or f"{self.id}_d{len(self.doors)}"})

    # --------------------------------------------------------------- content
    def prop(self, pid, x, y, **opts):
        self.props.append([pid, x, y, opts] if opts else [pid, x, y])

    def trace(self, name, x, y):
        self.traces.append([name, x, y])

    def decor(self, name, x, y):
        self.walldecor.append([name, x, y])

    def light(self, x, y, color="#ffe6b8", r=1.0, e=1.0, flicker=0.0, shadow=False):
        self.lights.append([x, y, color, r, e, flicker, shadow])

    def exit(self, x, y, w, h, to, at, sfx="door", cond="", msg=None):
        e = {"rect": [x, y, w, h], "to": to, "at": at, "sfx": sfx}
        if cond:
            e["cond"] = cond
        if msg:
            e["msg"] = msg
        self.exits.append(e)

    def spawn(self, name, x, y, face="south"):
        self.spawns[name] = [x, y, face]

    def npc(self, nid, x, y, face="south", **kw):
        self.npcs.append(dict(id=nid, x=x, y=y, face=face, **kw))

    def item(self, iid, x, y, key=None, n=1):
        self.items.append({"id": iid, "x": x, "y": y, "key": key or f"{self.id}_{iid}_{x}_{y}", "n": n})

    def trigger(self, x, y, w, h, event, once=True, cond=""):
        self.triggers.append({"rect": [x, y, w, h], "event": event, "once": once, "cond": cond})

    def use(self, x, y, event, cond=""):
        """Interactable tile (examine/use with E): terminals, notes, switches..."""
        self.interact.append({"x": x, "y": y, "event": event, "cond": cond})

    def sfx_fx(self, kind, x, y, **kw):
        self.fx.append(dict(kind=kind, x=x, y=y, **kw))

    def critters(self, kind, x, y, n=1, r=3):
        self.vermin.append([kind, x, y, n, r])

    def sound(self, sid, x, y, db=0.0, r=8):
        self.sounds.append([sid, x, y, db, r])

    def sign(self, x, y, text, style="plate"):
        self.signs.append({"x": x, "y": y, "text": text, "style": style})

    def actor(self, aid, x, y, **kw):
        self.actors.append(dict(id=aid, x=x, y=y, **kw))

    # --------------------------------------------------------------- helpers
    def floor_tiles(self, x, y, w, h):
        return [(xx, yy) for yy in range(y, y + h) for xx in range(x, x + w)
                if 0 <= xx < self.w and 0 <= yy < self.h and self.g[yy][xx] == "."]

    def scatter(self, names, x, y, w, h, n, seed=0):
        rnd = random.Random(f"{self.id}{seed}{x}{y}")
        tiles = self.floor_tiles(x, y, w, h)
        for _ in range(min(n, len(tiles))):
            t = rnd.choice(tiles)
            self.trace(rnd.choice(names), *t)

    VARIANTS = {"blood_drag_h": ["", "2", "3"], "blood_drag_v": ["", "2", "3"], "scrape_h": ["", "2"], "scrape_v": ["", "2"]}

    def trail(self, name_h, name_v, points):
        """Draw a trace trail through tile points (axis-aligned segments); alternates variants."""
        def pick(n):
            return n + self.rnd.choice(self.VARIANTS.get(n, [""]))
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            if y0 == y1:
                for x in range(min(x0, x1), max(x0, x1) + 1):
                    self.trace(pick(name_h), x, y0)
            else:
                for y in range(min(y0, y1), max(y0, y1) + 1):
                    self.trace(pick(name_v), x0, y)

    def face_row_decor(self, names, x0, x1, y, every=3, seed=0):
        """Wall decor along a wall face row, skipping door gaps."""
        rnd = random.Random(f"{self.id}{seed}{y}")
        for x in range(x0, x1 + 1, every):
            if self.g[y][x] == "#":
                self.decor(rnd.choice(names), x, y)

    # ------------------------------------------------------------------ out
    def finish(self):
        # rock that touches no floor becomes void (pure black)
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] != "#":
                    continue
                near = False
                for yy in range(y - 1, y + 3):
                    for xx in range(x - 1, x + 2):
                        if 0 <= xx < self.w and 0 <= yy < self.h and self.carved[yy][xx]:
                            near = True
                if not near:
                    self.g[y][x] = " "
        used = {c for row in self.m for c in row}
        return {
            "id": self.id, "name": self.name, "sector": self.sector, "size": [self.w, self.h],
            "grid": ["".join(r) for r in self.g], "mat": ["".join(r) for r in self.m],
            "mats": {c: list(MATS[c]) for c in used},
            "env": self.env, "traces": self.traces, "walldecor": self.walldecor, "props": self.props,
            "lights": self.lights, "doors": self.doors, "exits": self.exits, "spawns": self.spawns,
            "npcs": self.npcs, "items": self.items, "triggers": self.triggers, "interact": self.interact,
            "fx": self.fx, "vermin": self.vermin, "sounds": self.sounds, "signs": self.signs,
            "actors": self.actors, "rooms": self.rooms,
        }

    def save(self):
        OUT.mkdir(parents=True, exist_ok=True)
        d = self.finish()
        (OUT / f"{self.id}.json").write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
        return d
