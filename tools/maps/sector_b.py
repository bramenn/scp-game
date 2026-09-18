"""Sector B — Light Containment Zone (Level -2). SCP-173 is loose. 131, 914, 012, 999, 500, D-block."""
from mapdsl import Map, L

LAB = "#e8f0ff"
WARM = "#ffe2b0"
RED = "#ff5a4a"
LCZ = {"ambient": "#101218", "fog": 0.14, "fog_color": "#a0a8b8", "amb": "lcz", "dust": 0.4}


def b01():
    m = Map("B01", L("LCZ Entrance", "Entrada a la ZCL"), 30, 16, "B", LCZ)
    m.room(2, 5, 26, 6, "l", L("Entrance hall", "Vestíbulo"))
    m.room(0, 7, 2, 2, "l")
    m.exit(0, 7, 1, 2, "A14", "from_B01")
    m.spawn("from_A14", 2, 7, "east")
    m.door(28, 7, "v", did="B01_east")
    m.room(29, 7, 1, 2, "l")
    m.exit(29, 7, 1, 2, "B02", "from_B01")
    m.spawn("from_B02", 27, 7, "west")
    m.sign(14, 4, L("Light Containment Zone", "Zona de Contención Ligera"), "zone")
    m.sign(24, 4, L("Keep eye contact", "Mantenga el contacto visual"), "warn")
    m.face_row_decor(["camera", "vent", "logo", "lamp", "sign_hazard"], 3, 27, 4, every=3, seed=1)
    m.prop("bench", 4, 9); m.prop("locker_row", 8, 6); m.prop("first_aid", 20, 6, walk=True)
    m.prop("body_guard", 18, 9, walk=True); m.trace("blood_pool", 19, 9)
    m.trail("scrape_h", "scrape_v", [(12, 8), (27, 8)])
    m.scatter(["dust", "crack", "papers", "casings"], 2, 5, 26, 6, 12, seed=2)
    m.use(22, 6, "save_terminal"); m.interact[-1]["prompt"] = L("[E] Site log (save)", "[E] Registro del sitio (guardar)")
    m.decor("screen", 22, 4)
    m.item("battery", 5, 7); m.item("doc_173_file", 11, 9)
    m.light(6, 7, LAB, 1.1, 0.9, 0.0); m.light(14, 7, LAB, 1.0, 0.8, 0.8); m.light(24, 7, LAB, 1.1, 0.9, 0.0)
    m.critters("roach", 25, 9, 6, 2); m.critters("moth", 6, 7, 3, 1)
    m.sound("hum", 22, 5, -10, 6)
    m.save()


def b02():
    """LCZ junction with SCP-173's containment cell and its observation booth."""
    m = Map("B02", L("LCZ Junction · SCP-173 Containment", "Cruce ZCL · Contención de SCP-173"), 46, 30, "B",
            dict(LCZ, fog=0.18, ambient="#0d0f14"))
    m.room(4, 10, 32, 14, "l", L("Junction", "Cruce"))
    m.room(36, 10, 6, 5, "l")
    # west corridor from the entrance
    m.room(0, 16, 4, 3, "l")
    m.exit(0, 16, 1, 3, "B01", "from_B02")
    m.spawn("from_B01", 2, 17, "east")
    # north: research corridor
    m.door(10, 8, "h", did="B02_north")
    m.room(10, 5, 2, 3, "l")
    m.exit(10, 5, 2, 1, "B05", "from_B02")
    m.spawn("from_B05", 10, 11, "south")
    # east: D-block
    m.door(42, 11, "v", level=1, did="B02_east")
    m.room(43, 11, 3, 2, "l")
    m.exit(45, 11, 1, 2, "B11", "from_B02")
    m.spawn("from_B11", 40, 11, "west")
    # south: armory (L2) and maintenance (sealed until 173 is contained)
    m.door(8, 24, "h", level=2, did="B02_armory")
    m.room(8, 26, 2, 3, "l")
    m.exit(8, 28, 2, 1, "B13", "from_B02")
    m.spawn("from_B13", 8, 22, "north")
    m.door(30, 24, "h", style="rust", lock="scp173_contained", did="B02_maint")
    m.room(30, 26, 2, 3, "d")
    m.exit(30, 28, 2, 1, "B15", "from_B02")
    m.spawn("from_B15", 30, 22, "north")
    # SCP-173's cell (north-east) and the observation booth (behind the hatch)
    m.room(24, 2, 10, 6, "d", L("SCP-173 cell", "Celda de SCP-173"))
    m.door(28, 8, "h", style="heavy", lock="b02_cell_open", did="B02_cell")
    m.room(35, 2, 6, 6, "l", L("Observation booth", "Cabina de observación"))
    m.hatch(34, 5)
    m.door(37, 8, "h", level=2, style="lab", did="B02_booth")
    m.prop("control_console", 36, 3)
    m.use(37, 4, "b02_console"); m.use(38, 4, "b02_console")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] Cell console", "[E] Consola de la celda")
    m.sign(29, 1, L("SCP-173", "SCP-173"), "scp")
    m.sign(37, 1, L("Observation", "Observación"), "plate")
    m.decor("window", 36, 1); m.decor("screen", 39, 1)
    # the cell: the article's floor (blood and feces), cracked concrete, grooves
    for t in [(26, 4), (27, 6), (30, 3), (31, 5), (29, 6)]:
        m.trace("scp173_stain", *t)
    m.trace("cracked_radial", 28, 4); m.trace("rubble", 32, 3); m.trace("blood_drops", 25, 6)
    m.decor("scratches", 26, 1); m.decor("blood_hand", 31, 1)
    # the junction: it has been everywhere
    m.trail("scrape_h", "scrape_v", [(5, 20), (18, 20), (18, 13), (28, 13), (28, 10)])
    m.trail("scrape_h", "scrape_v", [(22, 22), (34, 22)])
    for x, y in [(12, 15), (24, 19), (33, 12)]:
        m.prop("body_guard" if x != 24 else "body_dclass", x, y, walk=True)
        m.trace("blood_splat", x + 1, y)
    m.trace("cracked_radial", 13, 15); m.trace("cracked_radial", 25, 19)
    m.prop("crate", 5, 11); m.prop("barrel", 5, 13); m.prop("scp_crate", 32, 20)
    m.prop("bench", 14, 23); m.prop("cone", 20, 11); m.prop("caution_sign", 22, 11)
    m.prop("ceiling_panel", 16, 17, walk=True); m.prop("debris_pile", 6, 21)
    m.scatter(["dust", "crack", "crack2", "papers", "casings", "glass"], 4, 10, 32, 14, 30, seed=3)
    m.face_row_decor(["camera", "vent", "lamp", "sign_hazard", "pipe_h", "speaker"], 4, 23, 9, every=3, seed=4)
    m.sign(10, 7, L("Research", "Investigación"), "plate")
    m.decor("sign_exit", 42, 9)
    for x, y, fl in [(9, 13, 0), (20, 13, 1.0), (30, 16, 0), (10, 20, 0.3), (24, 21, 0), (38, 12, 0)]:
        m.light(x, y, LAB, 1.1, 0.9, fl)
    m.light(29, 4, RED, 0.7, 0.7, 0.2)
    m.light(38, 4, "#9fe0ff", 0.6, 0.6, 0.0)
    m.critters("roach", 7, 20, 10, 3); m.critters("rat", 34, 21, 2, 3); m.critters("spider", 5, 22, 2, 1)
    m.actor("scp173", 20, 17, contain_flag="scp173_contained", range=12)
    m.trigger(4, 15, 3, 5, "b02_reveal")
    m.sound("alarm_far", 29, 4, -14, 10)
    m.save()


def b05():
    m = Map("B05", L("Research Corridor", "Pasillo de investigación"), 60, 16, "B", LCZ)
    m.room(2, 6, 56, 4, "l", L("Corridor", "Pasillo"))
    m.room(30, 10, 2, 5, "l")
    m.exit(30, 14, 2, 1, "B02", "from_B05")
    m.spawn("from_B02", 30, 9, "north")
    doors = [  # x, side, to, level, style, label
        (10, "n", "B06", 1, "lab", L("SCP-914", "SCP-914")),
        (24, "n", "B07", 2, "heavy", L("SCP-012", "SCP-012")),
        (40, "n", "B08", 1, "lab", L("SCP-131", "SCP-131")),
        (16, "s", "B09", 1, "lab", L("SCP-999", "SCP-999")),
        (46, "s", "B10", 3, "heavy", L("SCP-500 vault", "Bóveda SCP-500")),
    ]
    for x, side, to, lvl, style, label in doors:
        if side == "n":
            m.door(x, 4, "h", level=lvl, style=style, did=f"B05_{to}")
            m.room(x, 1, 2, 3, "l")
            m.exit(x, 1, 2, 1, to, "from_B05")
            m.spawn("from_" + to, x, 6, "south")
            m.sign(x - 2, 5, label, "scp")
        else:
            m.door(x, 10, "h", level=lvl, style=style, did=f"B05_{to}")
            m.room(x, 12, 2, 3, "l")
            m.exit(x, 14, 2, 1, to, "from_B05")
            m.spawn("from_" + to, x, 9, "north")
    m.face_row_decor(["vent", "poster", "lamp", "clock", "board", "camera", "extinguisher"], 3, 57, 5, every=4, seed=5)
    m.scatter(["papers", "dust", "crack", "glass", "blood_drops"], 2, 6, 56, 4, 22, seed=6)
    m.prop("wheelchair", 6, 8); m.prop("lab_bench", 50, 7); m.prop("boxes", 55, 6); m.prop("iv_stand", 20, 6)
    m.prop("body_scientist", 34, 8, walk=True); m.trace("blood_pool", 35, 8)
    m.trail("scrape_h", "scrape_v", [(26, 9), (36, 9)])
    m.trace("slime_h", 13, 9); m.trace("slime_h", 14, 9); m.trace("slime_h", 15, 9)
    m.trace("wrappers", 17, 9)
    m.item("doc_131_note", 42, 7); m.item("bandage", 52, 9)
    for x in range(6, 58, 8):
        m.light(x, 7, LAB, 1.0, 0.85, 0.9 if x == 38 else 0.0)
    m.critters("roach", 44, 8, 8, 3); m.critters("moth", 22, 7, 3, 1)
    m.save()


def b06():
    m = Map("B06", L("SCP-914 Laboratory", "Laboratorio de SCP-914"), 34, 22, "B", dict(LCZ, amb="lcz", ambient="#16130f", fog=0.1))
    m.room(2, 3, 30, 15, "l", L("914 lab", "Laboratorio 914"))
    m.room(10, 18, 2, 4, "l")
    m.exit(10, 21, 2, 1, "B05", "from_B06")
    m.spawn("from_B05", 10, 17, "north")
    m.prop("scp914", 11, 9)
    m.prop("scp914_booth", 6, 9); m.prop("scp914_booth", 19, 9)
    m.sign(9, 2, L("SCP-914", "SCP-914"), "scp")
    m.sign(6, 2, L("Intake", "Entrada"), "plate"); m.sign(20, 2, L("Output", "Salida"), "plate")
    m.use(13, 10, "scp914"); m.use(14, 10, "scp914")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] SCP-914 dial", "[E] Dial de SCP-914")
    m.prop("workbench", 25, 4); m.prop("lab_bench", 25, 12); m.prop("chem_shelf", 29, 7); m.prop("filing_cabinet", 3, 4)
    m.prop("toolbox", 23, 7); m.prop("whiteboard", 3, 12)
    for x, y in [(8, 12), (9, 14), (15, 13), (18, 15), (21, 12), (12, 16)]:
        m.trace(["gear", "copper", "oilpool"][(x + y) % 3], x, y)
    m.scatter(["gear", "copper", "papers", "oil"], 2, 3, 30, 15, 12, seed=7)
    m.decor("board", 12, 2); m.decor("clock", 16, 2); m.decor("pipe_joint", 23, 2); m.decor("cables", 27, 2)
    m.npc("adebayo", 17, 14, "north", mode="idle")
    m.item("doc_914_log", 26, 13)
    m.light(13, 7, "#ffcf80", 1.4, 1.0, 0.0); m.light(26, 8, LAB, 0.9, 0.8, 0.0); m.light(6, 14, LAB, 0.8, 0.7, 0.6)
    m.critters("spider", 30, 16, 2, 1)
    m.sound("computer", 13, 8, -12, 9)
    m.save()


def b07():
    m = Map("B07", L("SCP-012 Containment", "Contención de SCP-012"), 24, 18, "B",
            dict(LCZ, ambient="#070709", fog=0.22, fog_color="#5a2a2e", drain=1.4, dust=0.2))
    m.room(2, 3, 20, 11, "d", L("012 chamber", "Cámara 012"))
    m.room(10, 14, 2, 4, "d")
    m.exit(10, 17, 2, 1, "B05", "from_B07")
    m.spawn("from_B05", 10, 13, "north")
    m.prop("iron_box", 11, 7)
    for x in range(3, 21, 2):
        m.decor("notes012", x, 2)
    m.decor("blood_write", 6, 2); m.decor("blood_hand", 16, 2)
    m.prop("body_scientist", 6, 10, walk=True); m.trace("blood_pool", 7, 10)
    m.prop("body_dclass", 15, 5, walk=True); m.trace("blood_smear", 14, 5)
    m.scatter(["blood_drops", "blood_drops", "papers", "scalpel"], 2, 3, 20, 11, 18, seed=8)
    m.item("adebayo_notebook", 17, 11); m.item("doc_012_file", 4, 5)
    m.light(11, 5, "#ff2a1a", 0.35, 0.5, 0.4)
    m.sound("hum", 11, 7, -18, 6)
    m.trigger(9, 5, 5, 4, "b07_close", once=False)
    m.save()


def b08():
    m = Map("B08", L("SCP-131 Habitat", "Hábitat de SCP-131"), 26, 18, "B", dict(LCZ, ambient="#14131a"))
    m.room(2, 3, 22, 11, "c", L("Playroom", "Sala de juegos"))
    m.room(12, 14, 2, 4, "c")
    m.exit(12, 17, 2, 1, "B05", "from_B08")
    m.spawn("from_B05", 12, 13, "north")
    m.prop("toy_pile", 4, 5); m.prop("toy_pile", 18, 10); m.prop("ball", 9, 8, walk=True); m.prop("teddy", 15, 5, walk=True)
    m.prop("cat_bed", 20, 5); m.prop("bookshelf", 3, 11); m.prop("candy_bowl", 7, 11)
    for x, y in [(6, 7), (7, 7), (8, 8), (13, 9), (14, 9), (15, 10)]:
        m.trace("hopscotch" if (x + y) % 5 == 0 else "scrape_h2", x, y)
    m.scatter(["wrappers", "papers", "dust"], 2, 3, 22, 11, 10, seed=9)
    m.decor("poster", 6, 2); m.decor("poster2", 14, 2); m.decor("board", 10, 2); m.decor("camera", 20, 2)
    m.actor("scp131", 10, 7, sprite="scp131a", offset=0, cond="!bond131")
    m.actor("scp131", 12, 8, sprite="scp131b", offset=1, cond="!bond131")
    m.light(8, 6, WARM, 1.1, 0.9, 0.0); m.light(18, 9, WARM, 0.9, 0.8, 0.0)
    m.save()


def b09():
    m = Map("B09", L("SCP-999 Habitat", "Hábitat de SCP-999"), 22, 16, "B", dict(LCZ, ambient="#1a1612", fog=0.05))
    m.room(2, 3, 18, 9, "w", L("999's room", "Sala de 999"))
    m.room(8, 0, 2, 3, "w")
    m.exit(8, 0, 2, 1, "B05", "from_B09")
    m.spawn("from_B05", 8, 4, "south")
    m.prop("candy_bowl", 15, 5); m.prop("toy_pile", 4, 9); m.prop("mattress", 16, 9)
    m.trail("slime_h", "slime_v", [(4, 6), (13, 6), (13, 10)])
    m.scatter(["wrappers", "wrappers", "papers"], 2, 3, 18, 9, 12, seed=10)
    m.decor("poster", 5, 2); m.decor("poster2", 13, 2); m.decor("clock", 17, 2)
    m.actor("scp999", 12, 7)
    m.item("candy", 5, 5); m.item("doc_999_note", 17, 5)
    m.light(10, 6, "#ffd0a0", 1.2, 1.0, 0.0)
    m.save()


def b10():
    m = Map("B10", L("SCP-500 Vault", "Bóveda de SCP-500"), 18, 14, "B", dict(LCZ, ambient="#0d0f14"))
    m.room(3, 3, 12, 7, "t", L("Vault", "Bóveda"))
    m.room(8, 0, 2, 3, "t")
    m.exit(8, 0, 2, 1, "B05", "from_B10")
    m.spawn("from_B05", 8, 4, "south")
    m.prop("pill_case", 8, 7); m.prop("scp_crate", 3, 7); m.prop("scp_crate", 13, 7)
    m.decor("sign_bio", 5, 2); m.decor("keypad", 12, 2)
    m.item("scp500", 9, 8, n=2); m.item("doc_500_file", 5, 5)
    m.light(9, 6, "#ff9090", 0.9, 0.8, 0.0)
    m.save()


def b11():
    """D-class block. Twenty cells. Cell 17 is Marcus'."""
    m = Map("B11", L("D-Class Block", "Bloque de Clase-D"), 56, 26, "B",
            dict(LCZ, ambient="#0f0e10", fog=0.16, fog_color="#9a8f86", amb="lcz"))
    m.room(2, 11, 52, 4, "d", L("Cell row", "Galería de celdas"))
    m.room(0, 12, 2, 2, "d")
    m.exit(0, 12, 1, 2, "B02", "from_B11")
    m.spawn("from_B02", 2, 12, "east")
    # north showers door
    m.door(50, 9, "h", did="B11_showers")
    m.room(50, 6, 2, 3, "b")
    m.exit(50, 6, 2, 1, "B12", "from_B11")
    m.spawn("from_B12", 50, 12, "south")
    # cells: north row (y 3..7) and south row (y 17..21), 4 wide, door gap of 1
    n = 1
    for i, x in enumerate(range(4, 48, 5)):
        for row, (cy, gy) in enumerate([(3, 9), (17, 15)]):
            m.room(x, cy, 4, 5, "d", L(f"Cell {n}", f"Celda {n}"))
            open_cell = (n % 3 != 0) or n == 17
            if open_cell:
                m.gap(x + 1, gy, 1, 2 if row == 0 else 2, "d")
            m.prop("cell_bunk", x, cy + (0 if row == 0 else 4))
            m.prop("prison_toilet", x + 3, cy + (0 if row == 0 else 4))
            if n == 17:
                marcus = (x, cy)
            n += 1
    mx, my = marcus
    m.prop("body_dclass", mx + 1, my + 2, walk=True)
    for dx, dy in [(0, 1), (1, 3), (3, 2), (2, 4), (0, 3)]:
        m.trace("drawing_horse", mx + dx, my + dy)
    m.item("doc_marcus_letter", mx + 2, my + 2)
    m.use(mx + 1, my + 1, "b11_marcus")
    m.item("doc_black_tide_schedule", 44, 12)
    m.prop("desk_pc", 43, 11); m.prop("office_chair", 44, 13, walk=True)
    m.trail("blood_drag_h", "blood_drag_v", [(12, 13), (30, 13)])
    m.scatter(["droppings", "wrappers", "blood_drops", "papers", "crack", "rat_hole"], 2, 11, 52, 4, 30, seed=11)
    m.scatter(["droppings", "papers", "crack"], 4, 3, 44, 5, 20, seed=12)
    m.scatter(["droppings", "papers", "crack"], 4, 17, 44, 5, 20, seed=13)
    m.face_row_decor(["camera", "lamp", "speaker", "vent"], 3, 53, 10, every=5, seed=14)
    for x in range(6, 54, 8):
        m.light(x, 12, "#fff0d0", 0.9, 0.8, 1.0 if x in (22, 38) else 0.0)
    m.light(mx + 2, my + 2, "#ffd9a0", 0.5, 0.6, 0.0)
    m.critters("rat", 20, 13, 4, 6); m.critters("rat", 40, 12, 3, 5); m.critters("roach", 10, 12, 16, 5)
    m.critters("fly", mx + 1, my + 2, 8, 1); m.critters("spider", 3, 14, 2, 1)
    m.save()
    return marcus


def b12():
    m = Map("B12", L("D-Class Showers", "Duchas de Clase-D"), 26, 16, "B", dict(LCZ, ambient="#0d1012", fog=0.25, fog_color="#b0c0c8"))
    m.room(2, 3, 22, 9, "b", L("Showers", "Duchas"))
    m.room(12, 12, 2, 4, "b")
    m.exit(12, 15, 2, 1, "B11", "from_B12")
    m.spawn("from_B11", 12, 11, "north")
    for x in range(3, 22, 3):
        m.prop("shower", x, 4)
    for x in (4, 8, 16, 20):
        m.decor("mirror", x, 2)
    m.fill(3, 7, 18, 3, "~")
    for x, y in [(5, 8), (11, 9), (17, 8)]:
        m.sfx_fx("drip", x, y)
    m.prop("body_dclass", 14, 8, walk=True); m.trace("blood_pool", 15, 8)
    m.sfx_fx("steam", 6, 4); m.sfx_fx("steam", 18, 4)
    m.item("battery", 21, 10); m.item("doc_shower_scrawl", 3, 10)
    m.light(12, 6, "#dff0ff", 1.0, 0.8, 1.0)
    m.critters("roach", 20, 10, 10, 3); m.critters("fly", 14, 8, 6, 1)
    m.sound("water", 12, 5, -8, 10)
    m.trigger(9, 7, 6, 3, "b12_mirror")
    m.save()


def b13():
    m = Map("B13", L("LCZ Armory", "Armería ZCL"), 22, 14, "B", dict(LCZ, ambient="#101014"))
    m.room(2, 3, 18, 7, "t", L("Armory", "Armería"))
    m.room(8, 0, 2, 3, "t")
    m.exit(8, 0, 2, 1, "B02", "from_B13")
    m.spawn("from_B02", 8, 4, "south")
    m.prop("gun_rack", 3, 4); m.prop("gun_rack", 5, 4); m.prop("ammo_crates", 15, 4); m.prop("locker_row", 12, 4)
    m.prop("table_flipped", 10, 8); m.prop("ammo_crates", 17, 8)
    m.scatter(["casings", "casings", "papers"], 2, 3, 18, 7, 10, seed=15)
    m.decor("sign_hazard", 7, 2); m.decor("camera", 17, 2)
    m.item("ammo", 16, 6, n=8); m.item("baton", 4, 7); m.item("bandage", 13, 7); m.item("battery", 18, 6)
    m.light(10, 6, LAB, 1.0, 0.9, 0.0)
    m.save()


def b15():
    m = Map("B15", L("Maintenance Access", "Acceso de mantenimiento"), 22, 16, "B",
            dict(LCZ, ambient="#0f0d0c", fog=0.2, fog_color="#8a7a6a", amb="maint"))
    m.room(2, 3, 18, 9, "d", L("Maintenance landing", "Rellano de mantenimiento"))
    m.room(8, 0, 2, 3, "d")
    m.exit(8, 0, 2, 1, "B02", "from_B15")
    m.spawn("from_B02", 8, 4, "south")
    m.prop("ladder", 16, 9)
    m.use(16, 8, "b15_ladder"); m.interact[-1]["prompt"] = L("[E] Climb down", "[E] Bajar")
    m.exit(16, 9, 1, 1, "C01", "from_B15", sfx="hatch")
    m.spawn("from_C01", 15, 9, "west")
    m.prop("janitor_cart", 4, 5); m.prop("pipes_floor", 4, 10); m.prop("valve_big", 12, 4); m.prop("toolbox", 7, 9, walk=True)
    m.sfx_fx("steam", 12, 4); m.sfx_fx("drip", 6, 7)
    m.scatter(["oil", "rust", "crack", "puddle"], 2, 3, 18, 9, 10, seed=16)
    m.decor("pipe_joint", 5, 2); m.decor("pipe_h", 6, 2); m.decor("fusebox", 14, 2)
    m.light(10, 6, "#ffb070", 0.9, 0.8, 0.5)
    m.critters("rat", 6, 8, 2, 3); m.critters("spider", 19, 4, 2, 1)
    m.sound("steam", 12, 4, -10, 7)
    m.save()


def build():
    for f in (b01, b02, b05, b06, b07, b08, b09, b10, b11, b12, b13, b15):
        f()
