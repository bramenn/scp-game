"""Sector A — Entrance Zone (Level -1). Offices, reception, security, cafeteria, dorms."""
from mapdsl import Map, L

LAMP = "#ffe2b0"     # warm fluorescent
COLD = "#cfe3ff"     # cold fluorescent
EZ = {"ambient": "#15161c", "fog": 0.12, "fog_color": "#9aa0aa", "amb": "ez", "dust": 0.35}


def a01():
    m = Map("A01", L("Service Elevator B", "Ascensor de servicio B"), 24, 18, "A",
            dict(EZ, ambient="#0d0e12", amb="elevator", fog=0.18))
    m.room(9, 3, 6, 4, "t", L("Elevator cab", "Cabina"))          # cab
    m.room(3, 9, 18, 6, "e", L("Elevator lobby", "Vestíbulo del ascensor"))
    m.room(0, 11, 3, 2, "e")
    m.door(11, 7, "h", style="heavy", lock="a01_forced", did="A01_cab")
    m.exit(0, 11, 1, 2, "A02", "from_A01")
    m.spawn("start", 12, 5, "south")
    m.spawn("from_A02", 1, 11, "east")
    # cab: cables, grime, a handprint on the door
    m.trace("dust", 10, 3); m.trace("debris", 13, 4); m.trace("blood_drops", 13, 6)
    m.decor("blood_hand", 12, 2); m.decor("panel", 10, 2); m.decor("speaker", 14, 2)
    m.light(12, 4, "#ff5a4a", 0.8, 0.9, 0.5)   # emergency light
    # lobby
    m.face_row_decor(["pipe_h", "vent", "cables"], 3, 20, 8, every=2, seed=1)
    m.decor("sign_blank", 16, 8); m.decor("extinguisher", 5, 8); m.decor("camera", 19, 8)
    m.sign(8, 8, L("Elevator B", "Ascensor B"), "zone")
    m.prop("bench", 15, 13); m.prop("plant_dead", 4, 10); m.prop("trash_can", 19, 10)
    m.prop("ceiling_panel", 6, 12, walk=True)
    m.scatter(["dust", "debris", "crack", "papers"], 3, 9, 18, 6, 9)
    m.trail("blood_drag_h", "blood_drag_v", [(3, 12), (9, 12)])
    m.trace("blood_pool", 10, 12)
    m.item("battery", 16, 12)
    m.item("doc_welcome", 7, 10)
    m.light(6, 10, LAMP, 1.0, 0.9, 0.0)
    m.light(16, 10, LAMP, 1.0, 0.8, 1.0)       # dying tube
    m.critters("roach", 19, 11, 7, 2)
    m.critters("moth", 6, 10, 3, 1)
    m.sfx_fx("sparks", 16, 9)
    m.use(11, 6, "a01_pry", cond="!a01_forced")
    m.use(12, 6, "a01_pry", cond="!a01_forced")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] Force the doors", "[E] Forzar las puertas")
    m.save()


def a02():
    m = Map("A02", L("Reception", "Recepción"), 36, 22, "A", EZ)
    m.room(2, 3, 31, 14, "e", L("Reception hall", "Vestíbulo de recepción"))
    m.room(33, 9, 3, 2, "e")                      # east: from the elevator lobby
    m.exit(35, 9, 1, 2, "A01", "from_A02")
    m.spawn("from_A01", 33, 9, "west")
    m.room(0, 8, 1, 2, "e")                       # west: security checkpoint
    m.door(1, 8, "v", did="A02_west")
    m.exit(0, 8, 1, 2, "A03", "from_A02")
    m.spawn("from_A03", 2, 8, "east")
    m.room(16, 0, 2, 1, "e")                      # north: east wing corridor
    m.door(16, 1, "h", level=1, did="A02_north")
    m.exit(16, 0, 2, 1, "A04", "from_A02")
    m.spawn("from_A04", 16, 3, "south")
    m.room(23, 19, 2, 3, "a")                     # south: Gate A hall
    m.door(23, 17, "h", level=1, style="heavy", did="A02_south")
    m.exit(23, 21, 2, 1, "A13", "from_A02")
    m.spawn("from_A13", 23, 16, "north")
    m.sign(14, 2, L("East wing", "Ala este"), "zone")
    m.sign(1, 6, L("Security", "Seguridad"), "zone")
    m.sign(26, 18, L("Gate A", "Portón A"), "warn")
    m.decor("logo", 11, 2); m.decor("logo", 21, 2); m.decor("clock", 9, 2)
    m.face_row_decor(["poster", "poster2", "board", "vent", "lamp"], 3, 31, 2, every=3, seed=2)
    m.decor("bullet_holes", 19, 2); m.decor("bullet_holes", 24, 2); m.decor("blood_smear_w", 20, 2)
    # reception desk and its dead receptionist
    m.prop("reception_desk", 14, 7)
    m.prop("office_chair", 16, 5, walk=True)
    m.prop("body_scientist", 15, 5, walk=True)
    m.trace("blood_pool", 16, 5)
    m.trail("blood_drag_h", "blood_drag_v", [(13, 8), (4, 8)])      # dragged west
    m.trace("handprint", 3, 9)
    m.scatter(["casings"], 12, 5, 8, 4, 5, seed=3)
    # waiting area
    m.prop("bench", 4, 13); m.prop("bench", 4, 15); m.prop("plant_dead", 3, 11)
    m.prop("water_cooler", 8, 11); m.prop("chair_fallen", 8, 14, walk=True)
    m.prop("vending", 29, 5); m.prop("vending", 31, 5)
    m.trace("glass", 29, 6); m.trace("wrappers", 30, 6); m.trace("wrappers", 31, 7)
    m.prop("trash_can", 27, 5); m.prop("plant_dead", 31, 15)
    m.prop("ceiling_panel", 21, 11, walk=True); m.prop("debris_pile", 25, 13)
    m.prop("body_guard", 22, 15, walk=True); m.trace("blood_splat", 23, 15)
    m.scatter(["papers", "dust", "debris", "crack", "crack2"], 2, 3, 31, 14, 26, seed=4)
    m.item("coin", 30, 7); m.item("bandage", 18, 8)
    m.use(14, 8, "a02_terminal"); m.interact[-1]["prompt"] = L("[E] Use the reception terminal", "[E] Usar el terminal de recepción")
    for x, y, fl in [(6, 5, 0), (12, 10, 0), (20, 6, 0.3), (27, 10, 0), (8, 14, 1.0), (28, 14, 0)]:
        m.light(x, y, LAMP, 1.1, 0.95, fl)
    m.light(24, 16, "alarm", 1.3, 0.8)
    m.critters("rat", 30, 8, 3, 3)
    m.critters("roach", 27, 6, 10, 2)
    m.critters("moth", 12, 10, 4, 1)
    m.critters("fly", 15, 5, 6, 1)
    m.sound("hum", 30, 5, -12, 8)
    m.save()


def a03():
    m = Map("A03", L("Security Checkpoint", "Puesto de seguridad"), 32, 22, "A", EZ)
    m.room(2, 3, 27, 15, "a", L("Checkpoint", "Control"))
    m.room(29, 9, 3, 2, "a")
    m.door(29, 9, "v", did="A03_east")
    m.exit(31, 9, 1, 2, "A02", "from_A03")
    m.spawn("from_A02", 28, 9, "west")
    m.room(20, 0, 2, 1, "a")
    m.door(20, 1, "h", level=1, did="A03_north")
    m.exit(20, 0, 2, 1, "A04", "from_A03")
    m.spawn("from_A04", 20, 3, "south")
    # guard post with the CCTV wall
    m.room(3, 3, 10, 6, "c")   # carpet office corner (recarves floor material)
    m.prop("cctv_wall", 5, 4)
    m.prop("office_chair", 7, 6, walk=True)
    m.prop("desk_pc", 10, 6)
    m.prop("filing_cabinet", 3, 4)
    m.prop("gun_rack", 11, 4); m.prop("ammo_crates", 11, 8)
    # scanners lane
    m.prop("metal_detector", 16, 11); m.prop("xray", 19, 11)
    m.prop("metal_detector", 16, 15)
    m.wall(14, 10, 1, 7)          # lane divider (low wall)
    m.prop("table_flipped", 23, 7); m.prop("sandbags", 22, 13)
    m.scatter(["casings"], 20, 5, 8, 10, 14, seed=5)
    m.trace("blood_pool", 5, 13); m.trace("bandage", 6, 14); m.trace("blood_drops", 7, 13)
    m.trace("syringe", 4, 14)
    m.decor("bullet_holes", 22, 2); m.decor("bullet_holes", 25, 2); m.decor("scratches", 27, 2)
    m.face_row_decor(["camera", "vent", "sign_hazard", "keypad", "lamp"], 3, 28, 2, every=3, seed=6)
    m.sign(17, 2, L("Security checkpoint", "Puesto de seguridad"), "zone")
    m.npc("ortega", 5, 14, "east")
    m.npc("nico", 8, 15, "west", cond="nico_safe,!follow:nico")
    m.use(6, 5, "a03_cctv"); m.interact[-1]["prompt"] = L("[E] Watch the cameras", "[E] Mirar las cámaras")
    m.use(9, 6, "save_terminal"); m.interact[-1]["prompt"] = L("[E] Security log (save)", "[E] Registro de seguridad (guardar)")
    m.item("ammo", 12, 7, n=6)
    for x, y, fl in [(7, 5, 0), (18, 7, 0), (24, 12, 0.6), (8, 13, 0), (26, 5, 0)]:
        m.light(x, y, COLD if x > 12 else LAMP, 1.1, 0.95, fl)
    m.critters("spider", 3, 16, 2, 1)
    m.critters("roach", 26, 16, 6, 2)
    m.sound("hum", 6, 4, -8, 7)
    m.save()


def a04():
    """Long east corridor: the spine of the entrance zone."""
    m = Map("A04", L("East Wing Corridor", "Pasillo del ala este"), 64, 20, "A", dict(EZ, fog=0.16))
    m.room(2, 8, 60, 4, "e", L("Corridor", "Pasillo"))
    # south connectors (doors in the 2-row south... the corridor's south wall is 1 row; use 2 rows)
    m.room(4, 12, 2, 2, "e"); m.room(4, 14, 2, 1, "e")          # to A03 (west end, south)
    m.exit(4, 14, 2, 1, "A03", "from_A04")
    m.spawn("from_A03", 4, 12, "north")
    m.room(10, 12, 2, 2, "e"); m.room(10, 14, 2, 1, "e")        # to A02 reception
    m.exit(10, 14, 2, 1, "A02", "from_A04")
    m.spawn("from_A02", 10, 12, "north")
    # north doors (2-row north wall at y=6..7)
    for x, to, lvl, name in [(16, "A05", 1, "A04_offices"), (28, "A07", 1, "A04_cafe"), (38, "A09", 1, "A04_break"),
                             (46, "A10", 0, "A04_server"), (56, "A11", 1, "A04_dorms")]:
        m.door(x, 6, "h", level=lvl, did=name, lock="a10_open" if to == "A10" else "",
               style="lab" if to == "A10" else "std")
        m.room(x, 4, 2, 2, "e")
        m.exit(x, 4, 2, 1, to, "from_A04")
        m.spawn("from_" + to, x, 8, "south")
    m.room(22, 12, 2, 2, "e"); m.room(22, 14, 2, 1, "e")        # south: infirmary
    m.door(22, 12, "h", level=1, did="A04_infirmary")
    m.exit(22, 14, 2, 1, "A12", "from_A04")
    m.spawn("from_A12", 22, 10, "north")
    m.room(62, 9, 2, 2, "e")                                    # east end: LCZ checkpoint
    m.door(62, 9, "v", level=1, did="A04_lcz")
    m.exit(63, 9, 1, 2, "A14", "from_A04")
    m.spawn("from_A14", 60, 9, "west")
    m.sign(17, 7, L("Offices", "Oficinas"), "plate"); m.sign(29, 7, L("Cafeteria", "Cafetería"), "plate")
    m.sign(39, 7, L("Break room", "Descanso"), "plate"); m.sign(47, 7, L("Servers", "Servidores"), "plate")
    m.sign(57, 7, L("Dormitories", "Dormitorios"), "plate"); m.sign(60, 7, L("To LCZ", "A Cont. Ligera"), "warn")
    m.face_row_decor(["poster", "board", "extinguisher", "vent", "lamp", "poster2", "clock"], 3, 61, 7, every=4, seed=7)
    m.decor("blood_hand", 33, 7); m.decor("blood_smear_w", 34, 7); m.decor("water_stain", 51, 7)
    # a body in the middle of the corridor, the leak, a fallen panel
    m.prop("body_guard", 32, 10, walk=True); m.trace("blood_pool", 33, 10); m.trail("footprints_h", "footprints_v", [(34, 9), (44, 9)])
    m.fill(49, 9, 3, 2, "~"); m.sfx_fx("drip", 50, 9); m.sfx_fx("drip", 51, 10)
    m.prop("ceiling_panel", 42, 11, walk=True); m.prop("cone", 48, 8); m.prop("caution_sign", 52, 11)
    m.prop("janitor_cart", 25, 8); m.prop("mop_bucket", 27, 11)
    m.scatter(["papers", "dust", "debris", "crack", "crack2", "casings"], 2, 8, 60, 4, 30, seed=8)
    m.item("battery", 44, 8); m.item("coin", 25, 11)
    for x in range(5, 62, 7):
        m.light(x, 9, LAMP, 1.0, 0.9, 1.0 if x in (33, 54) else 0.0)
    m.light(60, 10, "alarm", 1.2, 0.7)
    m.critters("rat", 36, 10, 2, 4); m.critters("roach", 18, 10, 8, 3); m.critters("spider", 58, 8, 2, 1)
    m.critters("moth", 12, 9, 3, 1); m.critters("fly", 32, 10, 6, 1)
    m.sound("hum", 20, 8, -14, 10)
    m.trigger(30, 8, 2, 4, "a04_first_body")
    m.save()


def a05():
    m = Map("A05", L("Administrative Offices", "Oficinas administrativas"), 38, 26, "A", EZ)
    m.room(2, 3, 34, 20, "c", L("Open office", "Oficina abierta"))
    m.room(18, 23, 2, 3, "c")
    m.exit(18, 25, 2, 1, "A04", "from_A05")
    m.spawn("from_A04", 18, 22, "north")
    # conference room (north-east) behind a glass wall
    m.wall(24, 3, 1, 8); m.wall(25, 11, 11, 1)
    m.gap(24, 8, 1, 2)
    m.prop("conf_table", 28, 7); m.prop("whiteboard", 33, 4)
    m.decor("window", 25, 2); m.decor("screen", 30, 2)
    # Elena's office door (west wall, key)
    m.room(0, 6, 1, 2, "c")
    m.door(1, 6, "v", lock="item:office_key", did="A05_elena")
    m.exit(0, 6, 1, 2, "A06", "from_A05")
    m.spawn("from_A06", 2, 6, "east")
    m.sign(3, 2, L("2-B  Dr. E. Vega", "2-B  Dra. E. Vega"), "plate")
    # cubicles: rows of desks
    for y in (6, 10, 14, 18):
        for x in (5, 10, 15):
            m.prop("desk_pc", x, y)
            if (x + y) % 3:
                m.prop("office_chair", x + 1, y + 1, walk=True)
    m.prop("filing_cabinet", 20, 4); m.prop("filing_cabinet", 21, 4); m.prop("printer", 20, 10)
    m.prop("bookshelf", 32, 14); m.prop("water_cooler", 34, 18); m.prop("boxes", 29, 20)
    m.prop("plant_dead", 22, 20); m.prop("chair_fallen", 13, 12, walk=True); m.prop("trash_can", 8, 20)
    m.face_row_decor(["poster", "board", "clock", "lamp", "vent", "poster2"], 3, 23, 2, every=3, seed=9)
    m.scatter(["papers", "papers", "dust", "crack"], 2, 3, 22, 20, 28, seed=10)
    m.trace("blood_smear", 12, 16); m.trace("oil", 16, 9)
    m.item("office_key", 21, 5)
    m.item("doc_memo_threshold", 11, 11)
    m.item("doc_black_tide_redacted", 29, 9)
    m.item("coin", 6, 21)
    m.use(20, 4, "a05_cabinet"); m.interact[-1]["prompt"] = L("[E] Search the cabinet", "[E] Registrar el archivador")
    for x, y, fl in [(7, 5, 0), (14, 9, 0.2), (7, 16, 0), (16, 19, 1.0), (29, 6, 0), (30, 17, 0)]:
        m.light(x, y, COLD, 1.1, 0.9, fl)
    m.critters("roach", 9, 21, 8, 2); m.critters("spider", 35, 21, 2, 1); m.critters("moth", 14, 9, 3, 1)
    m.sound("hum", 20, 10, -12, 8)
    m.save()


def a06():
    m = Map("A06", L("Office 2-B · Dr. Elena Vega", "Oficina 2-B · Dra. Elena Vega"), 18, 14, "A",
            dict(EZ, ambient="#181720", fog=0.08, dust=0.5))
    m.room(2, 3, 13, 8, "c", L("Elena's office", "Oficina de Elena"))
    m.room(15, 6, 3, 2, "c")
    m.exit(17, 6, 1, 2, "A05", "from_A06")
    m.spawn("from_A05", 14, 6, "west")
    m.prop("desk_pc", 5, 5); m.prop("office_chair", 6, 6, walk=True)
    m.prop("bookshelf", 11, 4); m.prop("filing_cabinet", 2, 4); m.prop("whiteboard", 8, 4)
    m.prop("plant_dead", 13, 9); m.prop("boxes", 3, 9)
    m.decor("board", 4, 2); m.decor("clock", 12, 2); m.decor("screen", 9, 2); m.decor("lamp", 6, 2)
    m.scatter(["papers", "papers", "dust"], 2, 3, 13, 8, 10, seed=11)
    m.trace("glass", 7, 7)   # the photo frame, fallen
    m.item("doc_elena_log1", 6, 7)
    m.item("tape", 10, 8, key="A06_tape")
    m.item("battery", 3, 7)
    m.use(8, 5, "a06_whiteboard"); m.interact[-1]["prompt"] = L("[E] Read the whiteboard", "[E] Leer la pizarra")
    m.use(5, 6, "a06_photo"); m.interact[-1]["prompt"] = L("[E] The photo", "[E] La foto")
    m.light(6, 5, LAMP, 0.9, 0.8, 0.0)
    m.light(12, 8, LAMP, 0.7, 0.5, 0.8)
    m.critters("spider", 3, 10, 1, 1)
    m.save()


def a07():
    m = Map("A07", L("Staff Cafeteria", "Cafetería del personal"), 38, 24, "A", dict(EZ, amb="ez_cafe"))
    m.room(2, 3, 34, 17, "e", L("Dining hall", "Comedor"))
    m.room(18, 20, 2, 4, "e")
    m.exit(18, 23, 2, 1, "A04", "from_A07")
    m.spawn("from_A04", 18, 19, "north")
    m.room(0, 8, 1, 2, "k")
    m.door(1, 8, "v", did="A07_kitchen")
    m.exit(0, 8, 1, 2, "A08", "from_A07")
    m.spawn("from_A08", 2, 8, "east")
    for y in (6, 10, 14):
        for x in (6, 14, 22, 29):
            m.prop("cafe_table", x, y)
    m.prop("tray_spill", 9, 8, walk=True); m.prop("tray_spill", 25, 12, walk=True); m.prop("tray_spill", 17, 16, walk=True)
    m.prop("vending", 32, 4); m.prop("vending", 34, 4); m.prop("trash_can", 3, 17); m.prop("trash_can", 34, 17)
    m.prop("chair_fallen", 12, 8, walk=True); m.prop("chair_fallen", 27, 16, walk=True)
    m.scatter(["wrappers", "blood_drops", "papers", "glass", "droppings", "droppings"], 2, 3, 34, 17, 34, seed=12)
    m.trace("blood_smear", 21, 12); m.trace("vomit", 30, 17); m.trace("blood_pool", 6, 18)
    m.prop("body_dclass", 5, 18, walk=True)
    m.face_row_decor(["poster", "clock", "lamp", "vent", "board", "poster2"], 3, 35, 2, every=3, seed=13)
    m.sign(17, 2, L("Cafeteria", "Cafetería"), "plate")
    m.item("cheese", 23, 9); m.item("candy", 33, 6); m.item("coin", 15, 18)
    for x, y, fl in [(7, 5, 0), (16, 5, 0.7), (26, 5, 0), (9, 12, 0), (24, 12, 1.0), (16, 17, 0)]:
        m.light(x, y, LAMP, 1.1, 0.9, fl)
    m.critters("rat", 9, 9, 4, 4); m.critters("rat", 26, 13, 3, 3); m.critters("roach", 18, 16, 14, 4)
    m.critters("fly", 5, 18, 8, 1); m.critters("moth", 16, 5, 4, 1)
    m.sound("hum", 33, 4, -10, 8)
    m.trigger(2, 6, 4, 6, "a07_kitchen_noise")
    m.save()


def a08():
    m = Map("A08", L("Kitchen and Pantry", "Cocina y despensa"), 26, 18, "A", dict(EZ, ambient="#121318"))
    m.room(2, 3, 21, 11, "k", L("Kitchen", "Cocina"))
    m.room(23, 7, 3, 2, "k")
    m.exit(25, 7, 1, 2, "A07", "from_A08")
    m.spawn("from_A07", 22, 7, "west")
    m.prop("kitchen_counter", 4, 5); m.prop("kitchen_counter", 8, 5); m.prop("stove", 13, 4); m.prop("stove", 15, 4)
    m.prop("fridge", 19, 4); m.prop("kitchen_counter", 5, 10); m.prop("kitchen_counter", 10, 10)
    m.prop("boxes", 3, 12); m.prop("trash_can", 15, 12); m.prop("mop_bucket", 20, 12)
    # walk-in freezer (Nico hides here) — steel room, cold light
    m.room(2, 16, 8, 1, "t")
    m.wall(2, 14, 8, 2)
    m.door(5, 14, "h", did="A08_freezer", style="lab")
    m.fill(2, 16, 8, 1, ".")
    m.scatter(["blood_drops", "wrappers", "droppings", "crack", "oilpool"], 2, 3, 21, 11, 20, seed=14)
    m.trace("puddle", 12, 8); m.trace("vomit", 17, 9)
    m.decor("vent", 11, 2); m.decor("extinguisher", 17, 2); m.decor("shelf", 7, 2); m.decor("shelf", 3, 2)
    m.npc("nico", 4, 16, "north", mode="cower", cond="!nico_left_freezer")
    m.item("medkit", 13, 7)
    m.light(8, 7, LAMP, 1.0, 0.8, 0.5); m.light(18, 9, LAMP, 0.9, 0.7, 0.0)
    m.light(5, 16, COLD, 0.6, 0.6, 0.0)
    m.critters("roach", 6, 11, 16, 4); m.critters("rat", 16, 11, 2, 3); m.critters("fly", 17, 9, 5, 1)
    m.sound("fridge", 19, 4, -10, 7)
    m.save()


def a09():
    m = Map("A09", L("Break Room", "Sala de descanso"), 20, 14, "A", dict(EZ, ambient="#17161c"))
    m.room(2, 3, 16, 8, "c", L("Break room", "Sala de descanso"))
    m.room(8, 11, 2, 3, "c")
    m.exit(8, 13, 2, 1, "A04", "from_A09")
    m.spawn("from_A04", 8, 10, "north")
    m.prop("scp294", 14, 4)
    m.prop("vending", 16, 4); m.prop("bench", 3, 8); m.prop("water_cooler", 3, 4)
    m.prop("fridge", 6, 4); m.prop("plant_dead", 16, 9)
    m.decor("screen", 9, 2); m.decor("poster", 11, 2); m.decor("clock", 5, 2)
    m.sign(14, 2, L("SCP-294", "SCP-294"), "scp")
    m.scatter(["papers", "wrappers", "dust"], 2, 3, 16, 8, 8, seed=15)
    m.trace("puddle", 13, 6)
    m.use(14, 5, "scp294"); m.use(15, 5, "scp294")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] SCP-294", "[E] SCP-294")
    m.light(8, 5, LAMP, 1.0, 0.9, 0.0); m.light(14, 8, LAMP, 0.9, 0.8, 0.4)
    m.critters("roach", 5, 9, 6, 2)
    m.sound("hum", 14, 4, -8, 6)
    m.save()


def a10():
    m = Map("A10", L("Server Room", "Sala de servidores"), 28, 18, "A",
            dict(EZ, ambient="#0c1014", fog=0.2, fog_color="#6d8aa0", amb="servers"))
    m.room(2, 3, 23, 12, "t", L("Server room", "Sala de servidores"))
    m.room(12, 15, 2, 3, "t")
    m.exit(12, 17, 2, 1, "A04", "from_A10")
    m.spawn("from_A04", 12, 14, "north")
    for x in range(4, 23, 3):
        for y in (5, 9):
            m.prop("server_rack" if (x + y) % 4 else "server_rack_broken", x, y)
    m.prop("crt_terminal", 11, 12)
    m.prop("office_chair", 12, 13, walk=True)
    m.scatter(["cable", "cable", "dust"], 2, 3, 23, 12, 16, seed=16)
    m.decor("cables", 5, 2); m.decor("cables", 13, 2); m.decor("cables", 19, 2); m.decor("screen_079", 11, 2)
    m.sfx_fx("sparks", 7, 8); m.sfx_fx("sparks", 19, 5)
    m.use(11, 11, "a10_079"); m.use(12, 11, "a10_079")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] The terminal", "[E] El terminal")
    m.light(11, 11, "#7fffb0", 0.7, 0.6, 0.2)
    for x in (6, 15, 21):
        m.light(x, 7, "#9fd0ff", 0.8, 0.7, 0.0)
    m.critters("spider", 3, 13, 2, 1)
    m.sound("servers", 12, 7, -6, 12)
    m.save()


def a11():
    """Staff dormitories. SCP-173 came through here: scrape marks and a broken neck."""
    m = Map("A11", L("Staff Dormitories", "Dormitorios del personal"), 34, 24, "A", dict(EZ, ambient="#121218"))
    m.room(2, 3, 30, 10, "c", L("Bunk room", "Literas"))
    m.room(2, 15, 14, 6, "b", L("Showers", "Duchas"))
    m.room(18, 15, 14, 6, "c", L("Lockers", "Taquillas"))
    m.gap(8, 13, 2, 2, "b"); m.gap(24, 13, 2, 2, "c")
    m.room(16, 21, 2, 3, "c")
    m.exit(16, 23, 2, 1, "A04", "from_A11")
    m.spawn("from_A04", 16, 20, "north")
    m.gap(16, 17, 2, 4, "c")
    for x in range(4, 30, 4):
        m.prop("bunk_bed", x, 5)
        m.prop("footlocker", x, 7)
    m.prop("bed_unmade", 4, 10); m.prop("bed_unmade", 12, 10)
    for x in range(20, 31, 3):
        m.prop("locker_row", x, 16)
    m.prop("shower", 3, 16); m.prop("shower", 6, 16); m.prop("shower", 9, 16); m.prop("toilet", 13, 16)
    m.decor("mirror", 4, 14); m.decor("mirror", 7, 14); m.decor("sink", 10, 14); m.decor("towel", 12, 14)
    # 173 passed here: grooves, the stain, a dead man with his neck snapped
    m.trail("scrape_h", "scrape_v", [(3, 12), (26, 12), (26, 14)])
    m.trace("scp173_stain", 26, 11); m.trace("cracked_radial", 25, 12)
    m.prop("body_dclass", 20, 10, walk=True)
    m.trace("puddle", 5, 18); m.trace("wet", 6, 19); m.trace("mold", 3, 20); m.trace("blood_drops", 9, 19)
    m.scatter(["papers", "dust", "wrappers", "bandage"], 2, 3, 30, 10, 18, seed=17)
    m.face_row_decor(["poster", "lamp", "vent", "clock", "board"], 3, 31, 2, every=4, seed=18)
    m.decor("scratches", 27, 12)
    m.sfx_fx("drip", 4, 17); m.sfx_fx("drip", 8, 18)
    m.item("doc_dorm_note", 13, 8); m.item("battery", 29, 9); m.item("coin", 23, 19)
    m.use(29, 17, "a11_locker"); m.interact[-1]["prompt"] = L("[E] Locker 7 (combination)", "[E] Taquilla 7 (combinación)")
    for x, y, fl in [(6, 5, 0), (16, 5, 1.0), (26, 5, 0), (8, 17, 0.5), (24, 17, 0)]:
        m.light(x, y, LAMP, 1.0, 0.85, fl)
    m.critters("roach", 5, 19, 10, 3); m.critters("spider", 30, 12, 2, 1); m.critters("fly", 20, 10, 6, 1)
    m.trigger(18, 8, 6, 4, "a11_body")
    m.save()


def a12():
    """Infirmary. A black corrosive stain: the Old Man was here first."""
    m = Map("A12", L("Infirmary", "Enfermería"), 28, 20, "A", dict(EZ, ambient="#121519"))
    m.room(2, 3, 24, 13, "w", L("Infirmary", "Enfermería"))
    m.room(12, 0, 2, 3, "w")
    m.exit(12, 0, 2, 1, "A04", "from_A12")
    m.spawn("from_A04", 12, 4, "south")
    for x in (4, 9, 16, 21):
        m.prop("med_bed", x, 6)
    m.prop("iv_stand", 7, 6); m.prop("iv_stand", 19, 6); m.prop("med_cabinet", 23, 11)
    m.prop("wheelchair", 5, 12); m.prop("gurney_body", 9, 12); m.prop("autopsy_tray", 13, 12)
    # corrosion in the corner, spreading from the wall
    m.trace("corrosion2", 20, 13); m.trace("corrosion", 21, 13); m.trace("corrosion_trail", 19, 14)
    m.trace("corrosion", 22, 14); m.decor("corrosion_w", 21, 2); m.decor("corrosion_drip", 22, 2)
    m.prop("body_aged", 17, 13, walk=True)
    m.scatter(["bandage", "syringe", "pills", "blood_drops", "papers"], 2, 3, 24, 13, 16, seed=19)
    m.decor("sign_bio", 5, 2); m.decor("clock", 10, 2); m.decor("lamp", 15, 2); m.decor("sink", 18, 2)
    m.item("medkit", 24, 12); m.item("bandage", 6, 9); m.item("doc_infirmary_log", 14, 9)
    for x, y, fl in [(6, 5, 0), (14, 5, 0), (22, 5, 0.9), (10, 12, 0)]:
        m.light(x, y, COLD, 1.1, 0.9, fl)
    m.critters("fly", 17, 13, 10, 1); m.critters("roach", 4, 14, 6, 2)
    m.trigger(16, 11, 7, 4, "a12_corrosion")
    m.save()


def a13():
    m = Map("A13", L("Gate A Hall", "Vestíbulo del Portón A"), 32, 20, "A",
            dict(EZ, ambient="#140f10", fog=0.18, fog_color="#7a6a6a"))
    m.room(3, 5, 26, 11, "h", L("Gate A", "Portón A"))
    m.room(15, 0, 2, 5, "a")
    m.exit(15, 0, 2, 1, "A02", "from_A13")
    m.spawn("from_A02", 15, 5, "south")
    # the blast door (south): a wall of steel with a sealed door
    m.door(15, 16, "h", style="heavy", lock="gate_a_open", did="A13_gate")
    m.room(15, 18, 2, 2, "h")
    m.exit(15, 19, 2, 1, "G05", "from_A13")
    m.spawn("from_G05", 15, 14, "north")
    m.prop("sandbags", 6, 12); m.prop("sandbags", 22, 12); m.prop("turret", 10, 7); m.prop("turret", 20, 7)
    m.prop("body_ntf", 8, 10, walk=True); m.prop("body_guard", 23, 9, walk=True)
    m.scatter(["casings", "casings", "blood_drops", "scorch"], 3, 5, 26, 11, 26, seed=20)
    m.sign(16, 15, L("Gate A · Surface", "Portón A · Superficie"), "warn")
    m.face_row_decor(["alarm", "pipe_h", "camera", "vent"], 4, 28, 4, every=3, seed=21)
    m.use(15, 15, "a13_gate"); m.use(16, 15, "a13_gate")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] The blast door", "[E] La puerta blindada")
    m.item("ammo", 21, 10, n=4)
    m.light(9, 8, "alarm", 1.4, 0.8); m.light(22, 8, "alarm", 1.4, 0.8)
    m.light(16, 12, "#ff9a70", 1.0, 0.6, 0.6)
    m.critters("roach", 26, 14, 6, 2)
    m.sound("alarm_far", 16, 15, -10, 14)
    m.save()


def a14():
    m = Map("A14", L("LCZ Checkpoint · Decontamination", "Control ZCL · Descontaminación"), 30, 16, "A",
            dict(EZ, ambient="#10141a", fog=0.1))
    m.room(2, 5, 26, 6, "h", L("Airlock", "Esclusa"))
    m.room(0, 7, 2, 2, "h")
    m.exit(0, 7, 1, 2, "A04", "from_A14")
    m.spawn("from_A04", 3, 7, "east")
    m.wall(10, 5, 1, 6); m.door(10, 7, "v", did="A14_in")
    m.wall(19, 5, 1, 6); m.door(19, 7, "v", lock="a14_decon_done", did="A14_out")
    m.room(28, 7, 2, 2, "l")
    m.exit(29, 7, 1, 2, "B01", "from_A14")
    m.spawn("from_B01", 26, 7, "west")
    for x in range(12, 18, 2):
        m.decor("vent", x, 4)
    m.trace("chalk", 14, 8)
    m.sign(14, 4, L("Decontamination", "Descontaminación"), "warn")
    m.sign(24, 4, L("Light containment", "Contención ligera"), "zone")
    m.prop("pressure_pad", 14, 8, walk=True)
    m.trigger(12, 5, 6, 6, "a14_decon", cond="!a14_decon_done")
    m.light(6, 7, COLD, 1.0, 0.9, 0.0); m.light(14, 7, "#ffe070", 1.0, 0.9, 0.0); m.light(24, 7, COLD, 1.0, 0.8, 0.3)
    m.save()


def build():
    for f in (a01, a02, a03, a04, a05, a06, a07, a08, a09, a10, a11, a12, a13, a14):
        f()
