"""Sector C — Maintenance & Sewers (Level -3). Power is out. Tomás, the rats, the breakers, SCP-087."""
from mapdsl import Map, L

EMER = "#ff4a3a"
SODIUM = "#ffb070"
POWER = "power_on"
MAINT = {"ambient": "#0c0b0e", "ambient_power": "#1c1b24", "fog": 0.22, "fog_color": "#7a6e62", "amb": "maint", "dust": 0.5}
SEWER = {"ambient": "#0b0d0e", "ambient_power": "#15181a", "fog": 0.3, "fog_color": "#5e6a5a", "amb": "sewer", "dust": 0.2}


def c01():
    m = Map("C01", L("Maintenance Junction", "Cruce de mantenimiento"), 48, 28, "C", MAINT)
    m.room(3, 7, 42, 14, "d", L("Junction", "Cruce"))
    m.room(5, 3, 4, 4, "d")                                       # ladder alcove
    m.prop("ladder", 6, 3)
    m.exit(6, 3, 1, 1, "B15", "from_C01", sfx="hatch")
    m.spawn("from_B15", 6, 5, "south")
    m.room(0, 13, 3, 2, "s")                                      # west: sewers
    m.exit(0, 13, 1, 2, "C03", "from_C01")
    m.spawn("from_C03", 3, 13, "east")
    m.door(12, 21, "h", style="rust", did="C01_pump")             # south-west: pump room
    m.room(12, 23, 2, 5, "d")
    m.exit(12, 27, 2, 1, "C02", "from_C01")
    m.spawn("from_C02", 12, 19, "north")
    m.door(30, 5, "h", style="heavy", lock="item:janitor_keys", did="C01_substation")   # north-east: substation
    m.room(30, 2, 2, 3, "d")
    m.exit(30, 2, 2, 1, "C06", "from_C01")
    m.spawn("from_C06", 30, 8, "south")
    m.door(45, 12, "v", level=3, lock=POWER, did="C01_medical")    # east: medical wing
    m.room(46, 12, 2, 2, "w")
    m.exit(47, 12, 1, 2, "D01", "from_C01")
    m.spawn("from_D01", 43, 12, "west")
    m.door(38, 21, "h", level=4, style="heavy", lock=POWER, did="C01_hcz")               # south-east: HCZ lift
    m.room(38, 23, 2, 5, "m")
    m.exit(38, 27, 2, 1, "E01", "from_C01")
    m.spawn("from_E01", 38, 19, "north")
    m.door(22, 21, "h", style="rust", lock="item:janitor_keys", did="C01_boiler")        # south: boiler room
    m.room(22, 23, 2, 5, "d")
    m.exit(22, 27, 2, 1, "C07", "from_C01")
    m.spawn("from_C07", 22, 19, "north")
    m.sign(31, 4, L("Substation", "Subestación"), "warn")
    m.sign(43, 10, L("Medical wing", "Ala médica"), "zone")
    m.decor("sign_exit", 2, 12)
    for x in range(4, 44, 4):
        m.decor(["pipe_h", "pipe_joint", "pipe_h", "cables", "vent", "fusebox"][(x // 4) % 6], x, 6)
    m.prop("pipes_floor", 16, 8); m.prop("pipes_floor", 34, 18); m.prop("janitor_cart", 40, 8); m.prop("barrel", 5, 18)
    m.prop("barrel", 7, 19); m.prop("crate", 26, 8); m.prop("toolbox", 20, 16, walk=True); m.prop("forklift", 36, 9)
    m.fill(24, 13, 6, 3, "~"); m.sfx_fx("drip", 26, 13); m.sfx_fx("drip", 28, 14)
    m.sfx_fx("steam", 17, 7)
    m.scatter(["oil", "rust", "crack", "crack2", "puddle", "droppings", "cable"], 3, 7, 42, 14, 40, seed=1)
    m.item("battery", 42, 18); m.item("doc_power_memo", 32, 10)
    for x, y in [(8, 9), (20, 10), (33, 16), (42, 10)]:
        m.light(x, y, EMER, 0.9, 0.7, 0.6)
    for x, y in [(8, 12), (18, 12), (28, 12), (38, 12)]:
        m.light(x, y, SODIUM, 1.2, 1.0, 0.0, cond=POWER)
    m.critters("rat", 6, 18, 3, 4); m.critters("roach", 30, 17, 14, 4); m.critters("spider", 44, 8, 2, 1)
    m.sound("steam", 17, 7, -10, 7); m.sound("water", 26, 14, -12, 8)
    m.save()


def c02():
    m = Map("C02", L("Pump Room", "Sala de bombas"), 32, 20, "C", MAINT)
    m.room(2, 3, 28, 12, "d", L("Pumps", "Bombas"))
    m.room(12, 0, 2, 3, "d")
    m.exit(12, 0, 2, 1, "C01", "from_C02")
    m.spawn("from_C01", 12, 4, "south")
    for x in (4, 10, 20, 25):
        m.prop("pump", x, 6)
    m.prop("valve_big", 16, 4); m.prop("pipes_floor", 6, 12); m.prop("boxes", 26, 12)
    m.fill(3, 9, 26, 3, "~")
    m.fill(8, 10, 6, 1, "=")
    for x, y in [(5, 9), (14, 10), (22, 9), (27, 11)]:
        m.sfx_fx("drip", x, y)
    m.sfx_fx("steam", 16, 4)
    m.scatter(["rust", "oil", "crack", "moss"], 2, 3, 28, 12, 18, seed=2)
    m.item("fuse", 27, 13, key="fuse_pump"); m.item("bandage", 3, 13)
    m.light(12, 6, EMER, 0.8, 0.6, 0.8)
    m.light(12, 6, SODIUM, 1.3, 1.0, 0.0, cond=POWER)
    m.actor("chaser", 20, 12, sprite="rat", battle="rats", speed=0.2, sight=5, wander=3, shadow=3.0)
    m.critters("rat", 24, 12, 3, 3); m.critters("roach", 6, 13, 10, 3)
    m.sound("water", 14, 10, -6, 12); m.sound("steam", 16, 4, -12, 6)
    m.save()


def c03():
    m = Map("C03", L("West Sewer Channel", "Canal oeste de alcantarillado"), 64, 22, "C", SEWER)
    m.room(2, 6, 60, 9, "s", L("Channel", "Canal"))
    m.fill(2, 9, 60, 3, "=")                                            # the channel
    for x in (14, 34, 50):
        m.fill(x, 9, 2, 3, ".", "g")                                     # grate bridges
    m.room(62, 6, 2, 2, "s")
    m.exit(63, 6, 1, 2, "C01", "from_C03")
    m.spawn("from_C01", 61, 6, "west")
    m.door(24, 4, "h", style="rust", did="C03_tomas")                  # north: Tomás' den
    m.room(24, 1, 2, 3, "s")
    m.exit(24, 1, 2, 1, "C05", "from_C03")
    m.spawn("from_C05", 24, 6, "south")
    m.room(0, 12, 2, 3, "s")                                            # far west: spider tunnel
    m.exit(0, 12, 1, 3, "C04", "from_C03")
    m.spawn("from_C04", 2, 13, "east")
    for x in range(4, 62, 6):
        m.decor(["pipe_h", "water_stain", "mold_w", "pipe_joint", "graffiti"][(x // 6) % 5], x, 5)
    m.scatter(["moss", "puddle", "droppings", "rat_hole", "rust", "bones"], 2, 6, 60, 3, 36, seed=3)
    m.scatter(["moss", "puddle", "droppings", "wet"], 2, 12, 60, 3, 30, seed=4)
    m.prop("rat_nest", 44, 6); m.prop("rat_nest", 8, 13); m.prop("bucket", 30, 13); m.prop("bag_trash", 38, 7, walk=True)
    m.prop("body_dclass", 55, 13, walk=True); m.trace("blood_smear", 54, 13)
    for x in range(6, 62, 5):
        m.sfx_fx("drip", x, 10)
    m.item("doc_tomas_note", 20, 7); m.item("ammo", 58, 14, n=4)
    for x in (12, 30, 48):
        m.light(x, 7, EMER, 0.7, 0.6, 0.7)
        m.light(x, 13, SODIUM, 1.0, 0.9, 0.3, cond=POWER)
    m.actor("chaser", 40, 13, sprite="rat", battle="rats", speed=0.2, sight=5, wander=4, shadow=3.0)
    m.actor("chaser", 18, 13, sprite="rat", battle="rats", speed=0.2, sight=5, wander=4, shadow=3.0)
    m.critters("rat", 44, 7, 4, 5); m.critters("rat", 10, 13, 4, 5); m.critters("roach", 30, 7, 20, 6)
    m.critters("fly", 55, 13, 8, 1)
    m.sound("water", 20, 10, -4, 16); m.sound("water", 45, 10, -4, 16)
    m.save()


def c04():
    m = Map("C04", L("Collapsed Tunnel", "Túnel derrumbado"), 40, 26, "C", dict(SEWER, fog=0.35))
    m.room(24, 10, 16, 5, "s", L("Tunnel", "Túnel"))
    m.room(8, 4, 16, 18, "r", L("Spider gallery", "Galería de las arañas"))
    m.gap(24, 11, 1, 3, "r")
    m.exit(39, 11, 1, 3, "C03", "from_C04")
    m.spawn("from_C03", 37, 12, "west")
    m.door(14, 22, "h", style="heavy", did="C04_087")
    m.room(14, 24, 2, 2, "d")
    m.exit(14, 25, 2, 1, "C08", "from_C04")
    m.spawn("from_C08", 14, 20, "north")
    for x, y in [(9, 5), (21, 5), (9, 19), (18, 12), (22, 17)]:
        m.prop("spider_web", x, y, walk=True)
    m.prop("debris_pile", 12, 9); m.prop("debris_pile", 19, 15)
    m.scatter(["rubble", "crack2", "bones", "dust", "moss"], 8, 4, 16, 18, 36, seed=5)
    m.scatter(["puddle", "moss", "droppings"], 24, 10, 16, 5, 12, seed=6)
    m.prop("body_scientist", 17, 18, walk=True); m.trace("bones", 16, 18)
    m.item("fuse", 10, 20, key="fuse_tunnel"); m.item("battery", 22, 6); m.item("doc_087_warning", 13, 19)
    m.sign(15, 21, L("SCP-087", "SCP-087"), "scp")
    m.light(30, 11, EMER, 0.6, 0.5, 0.9)
    m.critters("spider", 9, 5, 4, 2); m.critters("spider", 20, 16, 5, 3); m.critters("spider", 12, 12, 4, 3)
    m.critters("roach", 30, 13, 10, 4); m.critters("fly", 17, 18, 6, 1)
    m.sound("water", 32, 12, -14, 8)
    m.trigger(10, 8, 12, 4, "c04_spiders")
    m.save()


def c05():
    m = Map("C05", L("Tomás' Den", "La guarida de Tomás"), 26, 18, "C",
            dict(MAINT, ambient="#15100c", ambient_power="#1c1610", fog=0.12, fog_color="#6a5a4a"))
    m.room(2, 3, 22, 11, "r", L("Den", "Guarida"))
    m.room(12, 14, 2, 4, "s")
    m.exit(12, 17, 2, 1, "C03", "from_C05")
    m.spawn("from_C03", 12, 13, "north")
    m.prop("mattress", 4, 5); m.prop("burn_barrel", 12, 7); m.prop("workbench", 17, 4); m.prop("radio_small", 20, 6, walk=True)
    m.prop("rat_nest", 21, 11); m.prop("books", 5, 10, walk=True); m.prop("lantern", 8, 6, walk=True); m.prop("candles", 15, 10, walk=True)
    m.prop("boxes", 3, 11); m.prop("keys", 19, 7, walk=True)
    m.decor("board", 8, 2); m.decor("shelf", 14, 2); m.decor("poster", 20, 2); m.decor("clock", 4, 2)
    m.scatter(["ash", "papers", "wrappers", "droppings", "cheese"], 2, 3, 22, 11, 14, seed=7)
    m.npc("tomas", 10, 8, "east", mode="idle")
    m.item("candy", 5, 12)
    m.light(12, 7, "#ff9a40", 1.2, 1.0, 0.25)
    m.light(8, 6, "#ffd080", 0.6, 0.7, 0.0)
    m.critters("rat", 20, 11, 3, 2); m.critters("moth", 8, 6, 3, 1)
    m.sound("radio", 20, 6, -10, 7)
    m.save()


def c06():
    m = Map("C06", L("Electrical Substation", "Subestación eléctrica"), 32, 20, "C", dict(MAINT, amb="maint"))
    m.room(2, 3, 28, 12, "h", L("Substation", "Subestación"))
    m.room(14, 15, 2, 5, "d")
    m.exit(14, 19, 2, 1, "C01", "from_C06")
    m.spawn("from_C01", 14, 14, "north")
    for i, x in enumerate((6, 14, 22)):
        m.prop("breaker", x, 4)
        m.use(x, 5, f"c06_breaker{i + 1}")
        m.interact[-1]["prompt"] = L(f"[E] Breaker {i + 1}", f"[E] Interruptor {i + 1}")
    m.prop("transformer", 3, 9); m.prop("transformer", 26, 9)
    m.prop("control_console", 16, 9)
    m.use(17, 10, "c06_console"); m.interact[-1]["prompt"] = L("[E] Main panel", "[E] Panel principal")
    for x in range(3, 29, 3):
        m.decor(["sign_hazard", "cables", "fusebox", "panel", "sign_radiation"][(x // 3) % 5], x, 2)
    m.scatter(["cable", "scorch", "oil", "crack"], 2, 3, 28, 12, 16, seed=8)
    m.prop("body_guard", 20, 12, walk=True); m.trace("scorch", 21, 12); m.trace("burn", 20, 11)
    m.sfx_fx("sparks", 26, 8); m.sfx_fx("sparks", 4, 8)
    m.item("doc_substation", 9, 12)
    m.light(14, 7, EMER, 1.0, 0.8, 0.4)
    m.light(14, 8, "#bfe0ff", 1.4, 1.0, 0.0, cond=POWER)
    m.sound("hum", 16, 8, -8, 10)
    m.save()


def c07():
    m = Map("C07", L("Boiler Room", "Sala de calderas"), 34, 22, "C",
            dict(MAINT, ambient="#110a08", ambient_power="#1c120c", fog=0.35, fog_color="#a09080"))
    m.room(2, 3, 30, 14, "d", L("Boilers", "Calderas"))
    m.room(16, 0, 2, 3, "d")
    m.exit(16, 0, 2, 1, "C01", "from_C07")
    m.spawn("from_C01", 16, 4, "south")
    for x, y in [(4, 5), (10, 5), (22, 5), (27, 5)]:
        m.prop("boiler", x, y)
        m.sfx_fx("steam", x + 1, y - 1)
    m.prop("pipes_floor", 6, 12); m.prop("pipes_floor", 20, 12); m.prop("valve_big", 15, 6); m.prop("workbench", 26, 13)
    m.scatter(["rust", "oil", "scorch", "crack", "ash"], 2, 3, 30, 14, 22, seed=9)
    # steam vents that burn
    for x, y in [(9, 9), (19, 10), (25, 8)]:
        m.sfx_fx("steam", x, y)
        m.trigger(x, y, 1, 1, "c07_burn", once=False)
    m.item("fuse", 29, 15, key="fuse_boiler"); m.item("medkit", 3, 15)
    m.actor("scp529", 12, 14, sprite="scp529", cond="!josie_found", shadow=3.0, event="josie_talk")
    m.light(16, 8, "#ff7a40", 1.2, 0.9, 0.3)
    m.light(8, 12, SODIUM, 1.0, 0.9, 0.0, cond=POWER); m.light(24, 12, SODIUM, 1.0, 0.9, 0.0, cond=POWER)
    m.critters("roach", 28, 14, 12, 3); m.critters("rat", 5, 14, 2, 3)
    m.sound("steam", 16, 8, -4, 14); m.sound("generator", 10, 6, -12, 10)
    m.save()


def c08():
    m = Map("C08", L("SCP-087 Access", "Acceso a SCP-087"), 18, 14, "C", dict(MAINT, ambient="#050506", ambient_power="#0a0a0c"))
    m.room(3, 3, 12, 7, "d", L("Access", "Acceso"))
    m.room(8, 0, 2, 3, "d")
    m.exit(8, 0, 2, 1, "C04", "from_C08")
    m.spawn("from_C04", 8, 4, "south")
    m.door(8, 10, "h", style="heavy", did="C08_stair")
    m.room(8, 12, 2, 2, "d")
    m.exit(8, 13, 2, 1, "C09", "top")
    m.spawn("from_C09", 8, 8, "north")
    m.decor("sign_hazard", 5, 2); m.decor("sign_hazard", 12, 2); m.decor("board", 9, 2)
    m.prop("restraint_chair", 4, 5); m.prop("radio_station", 12, 5); m.prop("stretcher", 4, 8)
    m.scatter(["papers", "dust", "crack"], 3, 3, 12, 7, 8, seed=10)
    m.item("doc_087_log", 13, 8)
    m.light(9, 5, "#e0e0ff", 0.7, 0.6, 0.5)
    m.save()


def c09():
    """SCP-087: the stairwell. Flights of 13 steps, half-landings, light that gets eaten."""
    flights = 12
    m = Map("C09", L("SCP-087", "SCP-087"), 16, 8 + flights * 7, "C",
            {"ambient": "#000000", "fog": 0.0, "amb": "087", "dust": 0.1, "torch": 0.8, "torch_range": 0.45, "drain": 0.7})
    m.room(6, 2, 4, 3, "d", L("Top landing", "Rellano superior"))
    m.exit(6, 2, 4, 1, "C08", "from_C09")
    m.spawn("top", 7, 4, "south")
    y = 5
    for i in range(flights):
        left = i % 2 == 0
        x = 3 if left else 9
        m.room(x, y, 4, 5, "d")                 # the flight going down
        m.room(3, y + 5, 10, 2, "d", L(f"Landing {i + 1}", f"Rellano {i + 1}") if i % 4 == 3 else None)
        for k in range(5):
            m.trace("crack" if (k + i) % 3 else "dust", x + 1 + (k % 2), y + k)
        y += 7
    m.spawn("bottom", 7, y - 1, "north")
    for i in range(3, flights, 3):
        m.trigger(3, 5 + i * 7, 10, 2, f"c09_depth{i // 3}")
    m.trigger(3, y - 3, 10, 2, "c09_face")
    m.save()


def build():
    for f in (c01, c02, c03, c04, c05, c06, c07, c08, c09):
        f()
