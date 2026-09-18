"""Sector F — SCP-106's Pocket Dimension. Sector G — SCP-079 Core & Gate A (Level -5)."""
from mapdsl import Map, L

POCKET = {"ambient": "#140a12", "fog": 0.45, "fog_color": "#2a1020", "amb": "pocket", "dust": 0.6, "drain": 1.0}
CORE = {"ambient": "#070a0c", "fog": 0.16, "fog_color": "#407060", "amb": "core", "dust": 0.3}
CRT = "#7fffb0"
RED = "#ff3a2a"


def f01():
    """Rotting corridors that loop. Every junction looks like the last one."""
    m = Map("F01", L("The Corridors", "Los pasillos"), 44, 32, "F", POCKET)
    for y in (4, 14, 24):
        m.room(3, y, 38, 3, "p")
    for x in (3, 20, 38):
        m.room(x, 4, 3, 23, "p")
    m.spawn("start", 21, 15, "south")
    m.exit(3, 24, 1, 3, "F01", "loop_e")          # west end loops back east
    m.spawn("loop_e", 39, 25, "west")
    m.exit(40, 4, 1, 3, "F02", "from_F01")          # the one real way on
    m.spawn("from_F02", 38, 5, "west")
    m.scatter(["corrosion", "corrosion2", "pocket_eye", "bones", "corrosion_trail"], 3, 4, 38, 23, 70, seed=1)
    for x, y in [(8, 5), (30, 15), (12, 25), (37, 18)]:
        m.prop("pillar_rot", x, y)
    m.prop("bone_pile", 25, 5); m.prop("floating_door", 15, 15)
    m.light(21, 15, "#ff80a0", 0.6, 0.5, 0.6); m.light(39, 5, "#ffd0a0", 0.5, 0.6, 0.0)
    m.actor("scp106", 5, 25, delay=12.0)
    m.trigger(20, 14, 3, 3, "f01_arrive")
    m.critters("fly", 25, 5, 10, 2)
    m.save()


def f02():
    m = Map("F02", L("The Trench", "La trinchera"), 30, 40, "F", dict(POCKET, fog=0.55))
    m.room(12, 2, 6, 36, "p", L("Trench", "Trinchera"))
    m.room(0, 3, 12, 2, "p")
    m.exit(0, 3, 1, 2, "F01", "from_F02")
    m.spawn("from_F01", 12, 3, "south")
    m.exit(12, 37, 6, 1, "F03", "from_F02")
    m.spawn("from_F03", 14, 35, "north")
    for y in range(4, 36, 4):
        m.trace("pocket_eye", 12 if y % 8 else 17, y)
        if y % 8 == 0:
            m.decor("corrosion_drip", 11, y)
    m.scatter(["corrosion", "corrosion2", "bones", "corrosion_trail"], 12, 2, 6, 36, 60, seed=2)
    for y in (8, 18, 28):
        m.prop("bone_pile", 12, y)
    m.light(15, 20, "#ff6080", 0.5, 0.4, 0.8)
    m.trigger(12, 18, 6, 2, "f02_whispers")
    m.save()


def f03():
    """The throne room. Three doors. One goes back to the world."""
    m = Map("F03", L("The Throne", "El trono"), 34, 24, "F", POCKET)
    m.room(3, 4, 28, 16, "p", L("Throne room", "Sala del trono"))
    m.room(15, 20, 4, 4, "p")
    m.exit(15, 23, 4, 1, "F02", "from_F03")
    m.spawn("from_F02", 16, 18, "north")
    m.prop("throne", 15, 7)
    for i, x in enumerate((6, 16, 26)):
        m.prop("floating_door", x, 12)
        m.use(x, 13, f"f03_door{i + 1}")
        m.interact[-1]["prompt"] = L("[E] Open the door", "[E] Abrir la puerta")
    m.light(27, 12, "#fff0d0", 0.7, 0.8, 0.0)          # the right door has light under it
    m.light(16, 8, "#ff3060", 0.8, 0.6, 0.3)
    m.scatter(["corrosion2", "bones", "pocket_eye", "corrosion_trail"], 3, 4, 28, 16, 50, seed=3)
    m.prop("bone_pile", 6, 6); m.prop("bone_pile", 26, 6); m.prop("pillar_rot", 4, 17); m.prop("pillar_rot", 28, 17)
    m.save()


def g01():
    m = Map("G01", L("Core Access", "Acceso al núcleo"), 30, 18, "G", CORE)
    m.room(2, 4, 26, 9, "t", L("Access", "Acceso"))
    m.room(14, 13, 2, 5, "t")
    m.exit(14, 17, 2, 1, "E13", "from_G01", sfx="door_open")
    m.spawn("from_E13", 14, 11, "north")
    m.door(14, 2, "h", level=5, style="heavy", did="G01_farm")
    m.room(14, 0, 2, 2, "t")
    m.exit(14, 0, 2, 1, "G02", "from_G01")
    m.spawn("from_G02", 14, 5, "south")
    m.face_row_decor(["screen_079", "cables", "camera", "screen_079", "speaker"], 3, 27, 3, every=3, seed=1)
    m.prop("turret", 5, 6); m.prop("turret", 24, 6); m.prop("body_ntf", 9, 9, walk=True); m.prop("body_guard", 20, 10, walk=True)
    m.scatter(["cable", "casings", "glass", "scorch"], 2, 4, 26, 9, 20, seed=2)
    m.use(22, 5, "save_terminal"); m.interact[-1]["prompt"] = L("[E] Core log (save)", "[E] Registro del núcleo (guardar)")
    m.item("medkit", 3, 11); m.item("ammo", 26, 11, n=8)
    m.light(14, 7, CRT, 0.9, 0.8, 0.3)
    m.trigger(10, 7, 10, 3, "g01_079")
    m.save()


def g02():
    m = Map("G02", L("Server Farm", "Granja de servidores"), 48, 24, "G", dict(CORE, amb="servers"))
    m.room(2, 4, 44, 16, "t", L("Server farm", "Granja de servidores"))
    m.room(14, 20, 2, 4, "t")
    m.exit(14, 23, 2, 1, "G01", "from_G02")
    m.spawn("from_G01", 14, 18, "north")
    m.door(24, 2, "h", level=5, style="heavy", did="G02_core")
    m.room(24, 0, 2, 2, "t")
    m.exit(24, 0, 2, 1, "G03", "from_G02")
    m.spawn("from_G03", 24, 5, "south")
    m.door(46, 11, "v", level=5, style="heavy", lock="g03_choice", did="G02_warhead")
    m.room(47, 11, 1, 2, "h")
    m.exit(47, 11, 1, 2, "G04", "from_G02")
    m.spawn("from_G04", 44, 11, "west")
    for x in range(4, 44, 4):
        for y in (6, 10, 14):
            if not (22 <= x <= 26):
                m.prop("server_rack" if (x + y) % 3 else "server_rack_broken", x, y)
    m.prop("supercomputer", 34, 17)
    m.scatter(["cable", "cable", "scorch", "glass"], 2, 4, 44, 16, 40, seed=3)
    for x, y in [(8, 9), (30, 13), (40, 7)]:
        m.sfx_fx("sparks", x, y)
    for x in range(6, 44, 10):
        m.light(x, 12, CRT, 0.8, 0.6, 0.4)
    m.sound("servers", 24, 12, -4, 20)
    m.trigger(20, 10, 8, 4, "g02_079")
    m.save()


def g03():
    m = Map("G03", L("SCP-079 Core", "Núcleo de SCP-079"), 30, 22, "G", dict(CORE, ambient="#050806", amb="core"))
    m.room(3, 3, 24, 14, "t", L("Core", "Núcleo"))
    m.room(12, 17, 2, 5, "t")
    m.exit(12, 21, 2, 1, "G02", "from_G03")
    m.spawn("from_G02", 12, 15, "north")
    m.prop("core_terminal", 13, 6); m.prop("supercomputer", 4, 4); m.prop("supercomputer", 20, 4)
    m.prop("crt_terminal", 6, 11); m.prop("crt_terminal", 20, 11); m.prop("mattress", 23, 13); m.prop("candles", 22, 12, walk=True)
    m.scatter(["cable", "cable", "papers", "pills", "blood_drops"], 3, 3, 24, 14, 26, seed=4)
    for x in range(4, 26, 4):
        m.decor("screen_079", x, 2)
    m.npc("elena", 15, 9, "north", mode="idle", cond="!elena_gone")
    m.use(14, 8, "g03_core"); m.use(15, 8, "g03_core")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] The core", "[E] El núcleo")
    m.light(14, 7, CRT, 1.3, 1.0, 0.2); m.light(23, 12, "#ffd080", 0.5, 0.6, 0.0)
    m.sound("computer", 14, 6, -6, 12)
    m.trigger(8, 10, 14, 3, "g03_enter")
    m.save()


def g04():
    m = Map("G04", L("Warhead Control", "Control de la ojiva"), 26, 16, "G", dict(CORE, ambient="#100606", fog=0.1, fog_color="#a04040"))
    m.room(2, 3, 22, 9, "h", L("Warhead control", "Control de la ojiva"))
    m.room(0, 7, 2, 2, "h")
    m.exit(0, 7, 1, 2, "G02", "from_G04")
    m.spawn("from_G02", 2, 7, "east")
    m.door(24, 7, "v", level=5, style="heavy", lock="warhead_safe", did="G04_gate")
    m.room(25, 7, 1, 2, "h")
    m.exit(25, 7, 1, 2, "G05", "from_G04")
    m.spawn("from_G05", 22, 7, "west")
    m.prop("warhead_panel", 10, 4)
    m.use(11, 5, "g04_panel"); m.use(12, 5, "g04_panel")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] Warhead panel", "[E] Panel de la ojiva")
    m.decor("sign_radiation", 5, 2); m.decor("alarm", 8, 2); m.decor("sign_radiation", 17, 2); m.decor("alarm", 20, 2)
    m.light(12, 6, "alarm", 1.4, 1.0); m.light(12, 9, RED, 0.8, 0.6, 0.5)
    m.sound("alarm_far", 12, 5, -6, 12)
    m.save()


def g05():
    m = Map("G05", L("Gate A Lift", "Ascensor del Portón A"), 22, 22, "G", dict(CORE, ambient="#0a0c10", fog=0.2, fog_color="#8090a0"))
    m.room(3, 3, 16, 14, "t", L("Gate A lift", "Ascensor del Portón A"))
    m.room(0, 9, 3, 2, "h")
    m.exit(0, 9, 1, 2, "G04", "from_G05")
    m.spawn("from_G04", 3, 9, "east")
    m.room(8, 17, 6, 3, "t")
    m.exit(8, 19, 6, 1, "A13", "from_G05")
    m.spawn("from_A13", 10, 15, "north")
    m.prop("sandbags", 4, 5); m.prop("control_console", 13, 4)
    m.use(14, 5, "g05_lift"); m.interact[-1]["prompt"] = L("[E] Call the lift", "[E] Llamar al ascensor")
    m.npc("mara", 15, 12, "west", mode="idle", cond="mara_here")
    m.scatter(["casings", "scorch", "dust"], 3, 3, 16, 14, 16, seed=5)
    m.light(11, 9, "#dde8ff", 1.2, 1.0, 0.0)
    m.save()


def build():
    for f in (f01, f02, f03, g01, g02, g03, g04, g05):
        f()
