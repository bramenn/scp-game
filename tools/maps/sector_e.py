"""Sector E — Heavy Containment Zone (Level -4). 939 in the dark, Reyes, 096, 106, the femur breaker, 682."""
from mapdsl import Map, L

STEEL = "#cfd8e8"
RED = "#ff4a3a"
HCZ = {"ambient": "#0b0d11", "fog": 0.18, "fog_color": "#8a96a8", "amb": "hcz", "dust": 0.35}
DARK939 = {"ambient": "#050506", "fog": 0.4, "fog_color": "#b0a0a0", "amb": "939", "dust": 0.15}


def e01():
    m = Map("E01", L("HCZ Lift Lobby", "Vestíbulo del ascensor ZCP"), 32, 20, "E", HCZ)
    m.room(2, 5, 28, 10, "m", L("Lobby", "Vestíbulo"))
    m.room(14, 0, 2, 5, "m")
    m.exit(14, 0, 2, 1, "C01", "from_E01", sfx="door_open")
    m.spawn("from_C01", 14, 6, "south")
    m.room(0, 9, 2, 2, "m")
    m.exit(0, 9, 1, 2, "E02", "from_E01")
    m.spawn("from_E02", 2, 9, "east")
    m.door(22, 15, "h", style="heavy", did="E01_gen")
    m.room(22, 17, 2, 3, "m")
    m.exit(22, 19, 2, 1, "E14", "from_E01")
    m.spawn("from_E14", 22, 13, "north")
    m.sign(15, 4, L("Heavy Containment Zone", "Zona de Contención Pesada"), "zone")
    m.face_row_decor(["sign_hazard", "camera", "pipe_h", "lamp", "vent", "sign_radiation"], 3, 29, 4, every=3, seed=1)
    m.prop("sandbags", 5, 8); m.prop("body_ntf", 9, 11, walk=True); m.prop("helmet", 12, 12, walk=True); m.prop("rifle", 10, 13, walk=True)
    m.prop("stretcher", 25, 7); m.prop("ammo_crates", 27, 11)
    m.scatter(["casings", "blood_drops", "scorch", "crack", "debris"], 2, 5, 28, 10, 24, seed=2)
    m.trail("blood_drag_h", "blood_drag_v", [(9, 12), (2, 12)])
    m.use(26, 6, "save_terminal"); m.interact[-1]["prompt"] = L("[E] HCZ log (save)", "[E] Registro ZCP (guardar)")
    m.item("ammo", 27, 9, n=6); m.item("doc_ntf_orders", 25, 12)
    for x, y, fl in [(6, 7, 0.4), (16, 8, 0), (26, 8, 0.0)]:
        m.light(x, y, STEEL, 1.1, 0.9, fl)
    m.light(4, 10, "alarm", 1.2, 0.8)
    m.critters("roach", 20, 13, 8, 3)
    m.sound("alarm_far", 4, 10, -12, 10)
    m.save()


def e02():
    m = Map("E02", L("Dark Sector A", "Sector oscuro A"), 50, 24, "E", DARK939)
    m.room(2, 4, 46, 6, "m", L("North corridor", "Pasillo norte"))
    m.room(2, 14, 46, 6, "m", L("South corridor", "Pasillo sur"))
    for x in (6, 22, 40):
        m.gap(x, 10, 2, 4, "m")
    m.room(48, 15, 2, 2, "m")
    m.exit(49, 15, 1, 2, "E01", "from_E02")
    m.spawn("from_E01", 46, 15, "west")
    m.room(0, 5, 2, 2, "m")
    m.exit(0, 5, 1, 2, "E03", "from_E02")
    m.spawn("from_E03", 2, 5, "east")
    m.door(30, 2, "h", level=4, did="E02_bio")
    m.room(30, 0, 2, 2, "m")
    m.exit(30, 0, 2, 1, "E04", "from_E02")
    m.spawn("from_E04", 30, 5, "south")
    for y0 in (4, 14):
        m.scatter(["red_residue", "red_residue2", "condensation", "puddle", "wet", "drip_ring"], 2, y0, 46, 6, 40, seed=y0)
    for x, y in [(10, 6), (26, 16), (38, 7), (16, 17)]:
        m.sfx_fx("drip", x, y)
    m.sfx_fx("mist", 24, 7, w=20, h=3); m.sfx_fx("mist", 24, 17, w=20, h=3)
    m.prop("body_ntf", 18, 16, walk=True); m.trace("blood_pool", 19, 16); m.trace("gouge", 20, 17)
    m.prop("body_guard", 34, 6, walk=True); m.trace("red_residue", 35, 6)
    m.item("dogtag", 18, 17, key="tag_1"); m.item("battery", 44, 5)
    m.light(46, 16, RED, 0.6, 0.5, 0.8)
    m.actor("scp939", 12, 16, wander=6, cond="!e02_939_gone")
    m.critters("roach", 30, 18, 8, 3)
    m.sound("water", 24, 10, -14, 14)
    m.save()


def e03():
    m = Map("E03", L("Dark Sector B", "Sector oscuro B"), 44, 26, "E", DARK939)
    m.room(4, 4, 36, 16, "m", L("Flooded hall", "Sala inundada"))
    for x in range(8, 40, 8):
        m.wall(x, 8, 2, 2)
        m.wall(x, 14, 2, 2)
    m.fill(12, 11, 20, 3, "~")
    m.room(40, 5, 4, 2, "m")
    m.exit(43, 5, 1, 2, "E02", "from_E03")
    m.spawn("from_E02", 39, 5, "west")
    m.door(20, 20, "h", level=4, did="E03_ntf")
    m.room(20, 22, 2, 4, "m")
    m.exit(20, 25, 2, 1, "E05", "from_E03")
    m.spawn("from_E05", 20, 18, "north")
    m.room(0, 12, 4, 2, "m")
    m.exit(0, 12, 1, 2, "E06", "from_E03")
    m.spawn("from_E06", 4, 12, "east")
    m.scatter(["red_residue", "red_residue2", "condensation", "wet", "puddle", "gouge", "bones"], 4, 4, 36, 16, 50, seed=3)
    m.sfx_fx("mist", 22, 12, w=30, h=8)
    for x, y in [(14, 6), (30, 17), (24, 9)]:
        m.sfx_fx("drip", x, y)
    m.prop("body_ntf", 30, 6, walk=True); m.prop("body_scientist", 10, 17, walk=True); m.prop("radio_small", 31, 7, walk=True)
    m.item("dogtag", 30, 7, key="tag_2"); m.item("medkit", 6, 18)
    m.use(31, 7, "e03_radio"); m.interact[-1]["prompt"] = L("[E] The radio", "[E] La radio")
    m.light(22, 12, RED, 0.5, 0.5, 0.9)
    m.actor("scp939", 18, 6, wander=8, cond="!e03_939a_gone")
    m.actor("scp939", 30, 17, wander=6, cond="!e03_939b_gone")
    m.sound("water", 22, 12, -8, 14)
    m.save()


def e04():
    m = Map("E04", L("Bio-Containment Area-14", "Área de Biocontención 14"), 32, 18, "E", dict(DARK939, fog=0.5))
    m.room(2, 3, 28, 10, "t", L("939 pens", "Corrales de 939"))
    m.room(14, 13, 2, 5, "m")
    m.exit(14, 17, 2, 1, "E02", "from_E04")
    m.spawn("from_E02", 14, 12, "north")
    for x in (3, 10, 17, 24):
        m.wall(x + 5, 3, 1, 5)
    m.scatter(["red_residue2", "condensation", "wet", "puddle", "bones", "claw_floor"], 2, 3, 28, 10, 40, seed=4)
    m.sfx_fx("mist", 16, 8, w=26, h=8)
    m.decor("sign_bio", 5, 2); m.decor("claws", 12, 2); m.decor("claws", 20, 2); m.decor("sign_hazard", 26, 2)
    m.item("dogtag", 25, 11, key="tag_3"); m.item("doc_939_file", 4, 11)
    m.light(16, 8, RED, 0.4, 0.4, 0.5)
    m.critters("fly", 20, 9, 6, 1)
    m.sound("hum", 16, 5, -16, 10)
    m.save()


def e05():
    m = Map("E05", L("Nine-Tailed Fox Last Stand", "Última trinchera de Nueve Colas"), 38, 22, "E", HCZ)
    m.room(2, 3, 34, 14, "m", L("Barricade", "Barricada"))
    m.room(20, 0, 2, 3, "m")
    m.exit(20, 0, 2, 1, "E03", "from_E05")
    m.spawn("from_E03", 20, 4, "south")
    m.door(36, 9, "v", level=4, lock="met_reyes", did="E05_east")
    m.room(37, 9, 1, 2, "m")
    m.exit(37, 9, 1, 2, "E11", "from_E05")
    m.spawn("from_E11", 34, 9, "west")
    m.prop("sandbags", 6, 8); m.prop("sandbags", 12, 8); m.prop("sandbags", 26, 12); m.prop("table_flipped", 18, 7)
    m.prop("radio_station", 30, 4); m.prop("ammo_crates", 4, 4); m.prop("stretcher", 8, 13)
    for x, y in [(10, 11), (15, 14), (24, 6), (29, 14)]:
        m.prop("body_ntf", x, y, walk=True)
        m.trace("blood_pool", x + 1, y)
    m.scatter(["casings", "casings", "scorch", "bandage", "blood_drops"], 2, 3, 34, 14, 40, seed=5)
    m.face_row_decor(["bullet_holes", "blood_smear_w", "sign_hazard", "camera", "claws"], 3, 35, 2, every=3, seed=6)
    m.npc("reyes", 31, 8, "west", mode="cower", cond="!reyes_gone")
    m.item("ammo", 5, 6, n=10); m.item("medkit", 33, 14)
    m.light(18, 9, STEEL, 1.2, 0.9, 0.5); m.light(31, 6, "#ffc080", 0.8, 0.8, 0.0)
    m.critters("fly", 15, 14, 6, 1)
    m.sound("radio", 30, 4, -10, 8)
    m.save()


def e06():
    m = Map("E06", L("HCZ Armory", "Armería ZCP"), 24, 16, "E", HCZ)
    m.room(2, 3, 20, 9, "t", L("Armory", "Armería"))
    m.room(22, 7, 2, 2, "m")
    m.exit(23, 7, 1, 2, "E03", "from_E06")
    m.spawn("from_E03", 21, 7, "west")
    m.prop("gun_rack", 3, 4); m.prop("gun_rack", 6, 4); m.prop("ammo_crates", 12, 4); m.prop("locker_row", 16, 4)
    m.prop("table_flipped", 9, 9)
    m.scatter(["casings", "papers", "oil"], 2, 3, 20, 9, 10, seed=7)
    m.item("ammo", 13, 7, n=12); m.item("dogtag", 4, 10, key="tag_4"); m.item("medkit", 19, 10); m.item("battery", 8, 7)
    m.light(12, 7, STEEL, 1.0, 0.9, 0.0)
    m.save()


def e07():
    """SCP-096's 5x5x5 m steel cube inside its chamber. Claw marks everywhere."""
    m = Map("E07", L("SCP-096 Containment", "Contención de SCP-096"), 34, 26, "E",
            dict(HCZ, ambient="#0a0808", fog=0.12, fog_color="#a09090"))
    m.room(2, 3, 30, 18, "m", L("Chamber", "Cámara"))
    m.room(16, 21, 2, 5, "m")
    m.exit(16, 25, 2, 1, "E11", "from_E07")
    m.spawn("from_E11", 16, 19, "north")
    m.room(0, 11, 2, 2, "m")
    m.exit(0, 11, 1, 2, "E08", "from_E07")
    m.spawn("from_E08", 2, 11, "east")
    # the cube: steel walls with a torn-open door on its south side
    m.wall(10, 6, 14, 2); m.wall(10, 8, 1, 8); m.wall(23, 8, 1, 8); m.wall(10, 16, 6, 2); m.wall(18, 16, 6, 2)
    m.gap(16, 16, 2, 2, "t")
    for x in range(11, 23):
        for y in range(8, 16):
            m.m[y][x] = "t"
    m.decor("claws", 12, 7); m.decor("claws", 15, 7); m.decor("claws", 19, 7); m.decor("scratches", 21, 7); m.decor("blood_smear_w", 17, 7)
    m.decor("camera", 5, 2); m.decor("camera", 28, 2)
    m.scatter(["claw_floor", "gouge", "blood_drops", "glass", "debris"], 11, 8, 12, 8, 26, seed=8)
    m.scatter(["claw_floor", "blood_drag_h", "casings", "glass", "cable"], 2, 3, 30, 18, 24, seed=9)
    m.prop("pressure_pad", 13, 12, walk=True); m.prop("pressure_pad", 20, 12, walk=True)
    m.prop("body_guard", 6, 17, walk=True); m.prop("body_ntf", 26, 6, walk=True)
    m.actor("scp096", 17, 10, dir="north", cond="!scp096_bagged_done")
    m.item("recorder", 17, 9, key="reyes_recorder")
    m.light(17, 12, RED, 0.6, 0.6, 0.5)
    m.light(5, 18, STEEL, 0.8, 0.7, 0.6)
    m.save()


def e08():
    m = Map("E08", L("096 Observation", "Observación de 096"), 20, 14, "E", HCZ)
    m.room(2, 3, 16, 7, "m", L("Observation", "Observación"))
    m.room(18, 6, 2, 2, "m")
    m.exit(19, 6, 1, 2, "E07", "from_E08")
    m.spawn("from_E07", 17, 6, "west")
    m.prop("cctv_wall", 4, 4); m.prop("desk_pc", 12, 4); m.prop("office_chair", 13, 6, walk=True)
    m.decor("window", 8, 2); m.decor("window", 14, 2)
    m.item("doc_096_file", 12, 8); m.item("doc_096_bag_note", 4, 8)
    m.light(9, 6, STEEL, 0.9, 0.8, 0.0)
    m.save()


def e09():
    """SCP-106: forty nested lead cells, suspended. Everything it touched is rotting."""
    m = Map("E09", L("SCP-106 Containment", "Contención de SCP-106"), 40, 26, "E",
            {"ambient": "#070507", "fog": 0.3, "fog_color": "#403040", "amb": "hcz", "dust": 0.3})
    m.room(2, 3, 36, 18, "x", L("Containment hall", "Sala de contención"))
    m.room(0, 11, 2, 2, "m")
    m.exit(0, 11, 1, 2, "E11", "from_E09")
    m.spawn("from_E11", 2, 11, "east")
    m.door(18, 1, "h", level=4, did="E09_femur")
    m.room(18, 0, 2, 1, "m")
    m.exit(18, 0, 2, 1, "E10", "from_E09")
    m.spawn("from_E10", 18, 4, "south")
    m.door(38, 11, "v", level=4, style="heavy", lock="scp106_contained", did="E09_682")
    m.room(39, 11, 1, 2, "h")
    m.exit(39, 11, 1, 2, "E12", "from_E09")
    m.spawn("from_E12", 36, 11, "west")
    m.spawn("from_F03", 8, 16, "north")
    m.wall(14, 8, 12, 2); m.wall(14, 10, 1, 6); m.wall(25, 10, 1, 6); m.wall(14, 16, 12, 1)
    for x in range(15, 25):
        for y in range(10, 16):
            m.g[y][x] = " "
    m.scatter(["corrosion", "corrosion2", "corrosion_trail", "rust", "oilpool", "cracked_radial"], 2, 3, 36, 18, 60, seed=10)
    m.decor("corrosion_w", 15, 7); m.decor("corrosion_drip", 18, 7); m.decor("corrosion_w", 22, 7)
    m.face_row_decor(["corrosion_drip", "corrosion_w", "water_stain", "sign_radiation"], 3, 37, 2, every=3, seed=11)
    m.prop("body_aged", 8, 6, walk=True); m.prop("body_aged", 30, 17, walk=True); m.prop("body_ntf", 26, 5, walk=True)
    m.sign(20, 7, L("SCP-106", "SCP-106"), "scp")
    m.item("doc_106_file", 32, 5); m.item("battery", 6, 18)
    m.light(8, 6, "#a0ffa0", 0.7, 0.6, 0.7); m.light(32, 16, "#a0ffa0", 0.7, 0.6, 0.9)
    m.actor("scp106", 20, 18, delay=5.0, gone_flag="scp106_contained")
    m.critters("fly", 8, 6, 8, 1)
    m.save()


def e10():
    m = Map("E10", L("Femur Breaker", "Rompefémures"), 26, 16, "E", dict(HCZ, ambient="#0d0a0a"))
    m.room(2, 3, 22, 9, "m", L("Recall room", "Sala de reclamo"))
    m.room(12, 12, 2, 4, "m")
    m.exit(12, 15, 2, 1, "E09", "from_E10")
    m.spawn("from_E09", 12, 11, "north")
    m.prop("femur_breaker", 6, 6)
    m.prop("control_console", 16, 5)
    m.use(17, 6, "e10_console"); m.use(18, 6, "e10_console")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] Recall console", "[E] Consola de reclamo")
    m.decor("window", 7, 2); m.decor("speaker", 12, 2); m.decor("sign_hazard", 19, 2)
    m.scatter(["blood_drops", "blood_pool", "claw_floor"], 3, 5, 8, 4, 8, seed=12)
    m.item("doc_femur_procedure", 20, 10)
    m.light(8, 6, "#ffd0b0", 0.9, 0.8, 0.0); m.light(18, 5, STEEL, 0.8, 0.7, 0.0)
    m.save()


def e11():
    m = Map("E11", L("Tesla Gate Corridor", "Pasillo de las puertas Tesla"), 50, 18, "E", HCZ)
    m.room(2, 7, 46, 4, "h", L("Corridor", "Pasillo"))
    m.room(0, 8, 2, 2, "h")
    m.exit(0, 8, 1, 2, "E05", "from_E11")
    m.spawn("from_E05", 2, 8, "east")
    m.room(48, 8, 2, 2, "h")
    m.exit(49, 8, 1, 2, "E09", "from_E11")
    m.spawn("from_E09", 46, 8, "west")
    m.door(20, 5, "h", level=4, did="E11_096")
    m.room(20, 2, 2, 3, "m")
    m.exit(20, 2, 2, 1, "E07", "from_E11")
    m.spawn("from_E07", 20, 8, "south")
    for i, x in enumerate((12, 30, 40)):
        m.actor("tesla", x, 7, w=4, v=True, period=3.2 + i * 0.4, phase=i * 1.1)
        m.trace("scorch", x, 8); m.trace("scorch", x, 10)
    m.prop("body_guard", 31, 9, walk=True); m.trace("burn", 30, 9)
    m.scatter(["scorch", "casings", "cable", "crack"], 2, 7, 46, 4, 18, seed=13)
    m.face_row_decor(["sign_hazard", "pipe_h", "cables", "lamp", "sign_radiation"], 3, 47, 6, every=3, seed=14)
    m.sign(21, 4, L("SCP-096", "SCP-096"), "scp")
    m.item("dogtag", 44, 10, key="tag_5")
    for x in range(6, 48, 8):
        m.light(x, 8, STEEL, 0.9, 0.8, 0.0)
    m.trigger(8, 7, 2, 4, "e11_first")
    m.save()


def e12():
    m = Map("E12", L("SCP-682 Acid Chamber", "Cámara de ácido de SCP-682"), 40, 28, "E",
            {"ambient": "#0a0f06", "fog": 0.3, "fog_color": "#a8c870", "amb": "hcz", "dust": 0.2})
    m.room(2, 3, 36, 20, "h", L("Acid chamber", "Cámara de ácido"))
    m.room(0, 12, 2, 2, "h")
    m.exit(0, 12, 1, 2, "E09", "from_E12")
    m.spawn("from_E09", 2, 12, "east")
    m.door(30, 1, "h", level=4, style="heavy", did="E12_control")
    m.room(30, 0, 2, 1, "h")
    m.exit(30, 0, 2, 1, "E13", "from_E12")
    m.spawn("from_E13", 30, 4, "south")
    m.fill(10, 7, 18, 11, "=")                                   # the acid tank
    m.fill(11, 8, 16, 9, "=")
    for x, y in [(12, 9), (20, 10), (24, 15), (15, 15)]:
        m.sfx_fx("acid", x, y)
    m.prop("acid_railing", 12, 6); m.prop("acid_railing", 18, 6); m.prop("acid_railing", 24, 6)
    m.scatter(["acid", "acid2", "gouge", "dissolved", "scorch", "debris"], 2, 3, 36, 20, 50, seed=15)
    m.prop("debris_pile", 6, 18); m.prop("debris_pile", 32, 9); m.prop("body_dissolved", 5, 7); m.prop("body_ntf", 33, 18, walk=True)
    m.decor("acid_burn_w", 10, 2); m.decor("claws", 16, 2); m.decor("acid_burn_w", 22, 2); m.decor("claws", 28, 2)
    m.actor("prop_actor", 19, 12, sprite="scp682", dir="south", anim="walk", cond="!scp682_contained", shadow=14.0)
    m.light(19, 12, "#9aff60", 1.6, 0.9, 0.2)
    m.sound("water", 19, 12, -6, 16)
    m.trigger(4, 9, 3, 8, "e12_682")
    m.save()


def e13():
    m = Map("E13", L("682 Control Room", "Sala de control de 682"), 28, 18, "E", HCZ)
    m.room(2, 3, 24, 10, "m", L("Control", "Control"))
    m.room(12, 13, 2, 5, "h")
    m.exit(12, 17, 2, 1, "E12", "from_E13")
    m.spawn("from_E12", 12, 12, "north")
    m.door(20, 1, "h", level=5, style="heavy", lock="scp682_contained", did="E13_lift")
    m.room(20, 0, 2, 1, "t")
    m.exit(20, 0, 2, 1, "G01", "from_E13", sfx="door_open")
    m.spawn("from_G01", 20, 4, "south")
    m.prop("control_console", 5, 4); m.prop("cctv_wall", 10, 4); m.prop("filing_cabinet", 24, 4)
    m.prop("body_scientist", 7, 9, walk=True); m.prop("office_chair", 9, 8, walk=True)
    m.scatter(["papers", "blood_drops", "glass", "casings"], 2, 3, 24, 10, 16, seed=16)
    m.item("doc_682_file", 25, 10); m.item("doc_black_tide_final", 8, 5)
    m.use(6, 5, "save_terminal"); m.interact[-1]["prompt"] = L("[E] Control log (save)", "[E] Registro de control (guardar)")
    m.light(12, 7, STEEL, 1.0, 0.9, 0.0)
    m.save()


def e14():
    m = Map("E14", L("HCZ Generator", "Generador ZCP"), 30, 20, "E", dict(HCZ, amb="hcz"))
    m.room(2, 3, 26, 12, "m", L("Generator room", "Sala del generador"))
    m.room(12, 0, 2, 3, "m")
    m.exit(12, 0, 2, 1, "E01", "from_E14")
    m.spawn("from_E01", 12, 4, "south")
    m.prop("generator", 14, 8); m.prop("transformer", 3, 5); m.prop("pipes_floor", 20, 12)
    m.scatter(["oil", "scorch", "blood_pool", "red_residue", "gouge"], 2, 3, 26, 12, 20, seed=17)
    m.use(9, 11, "e14_ortega"); m.interact[-1]["prompt"] = L("[E] Ortega", "[E] Ortega")
    m.prop("body_guard", 9, 11, walk=True)
    m.item("doc_ortega_last", 10, 12)
    m.light(14, 7, "#ffd080", 1.2, 1.0, 0.1)
    m.sound("generator", 16, 7, -2, 14)
    m.save()


def build():
    for f in (e01, e02, e03, e04, e05, e06, e07, e08, e09, e10, e11, e12, e13, e14):
        f()
