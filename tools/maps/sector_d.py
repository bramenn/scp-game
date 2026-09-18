"""Sector D — Medical Wing (Level -3 east). SCP-049 walks the wards with its 'cured'. Dr. Lin, lavender."""
from mapdsl import Map, L

COLD = "#d8f0ff"
SICK = "#c8ffd8"
MED = {"ambient": "#101416", "fog": 0.14, "fog_color": "#b0c8c0", "amb": "med", "dust": 0.3}
ROUTE_WARDS = [[8, 8], [20, 8], [32, 8], [44, 8], [44, 13], [30, 13], [14, 13], [6, 13]]


def d01():
    m = Map("D01", L("Medical Reception", "Recepción médica"), 36, 22, "D", MED)
    m.room(2, 3, 32, 13, "w", L("Reception", "Recepción"))
    m.room(0, 11, 2, 2, "w")
    m.exit(0, 11, 1, 2, "C01", "from_D01")
    m.spawn("from_C01", 2, 11, "east")
    m.door(16, 1, "h", level=3, did="D01_wards")
    m.room(16, 0, 2, 1, "w")
    m.exit(16, 0, 2, 1, "D02", "from_D01")
    m.spawn("from_D02", 16, 4, "south")
    m.door(34, 7, "v", level=3, did="D01_morgue")
    m.room(35, 7, 1, 2, "w")
    m.exit(35, 7, 1, 2, "D04", "from_D01")
    m.spawn("from_D04", 32, 7, "west")
    m.door(24, 16, "h", style="lab", lock="lin_opened", did="D01_pharmacy")
    m.room(24, 18, 2, 4, "w")
    m.exit(24, 21, 2, 1, "D06", "from_D01")
    m.spawn("from_D06", 24, 14, "north")
    m.sign(14, 2, L("Medical wing", "Ala médica"), "zone")
    m.prop("reception_desk", 6, 6); m.prop("bench", 20, 12); m.prop("bench", 26, 12); m.prop("wheelchair", 30, 5)
    m.prop("water_cooler", 3, 4); m.prop("plant_dead", 32, 4); m.prop("iv_stand", 12, 10)
    m.prop("body_cured", 21, 10, walk=True); m.prop("body_cured", 28, 9, walk=True)
    m.prop("table_flipped", 20, 15)
    m.scatter(["blood_drops", "suture", "papers", "bandage", "syringe", "tray"], 2, 3, 32, 13, 22, seed=1)
    m.trail("blood_drag_h", "blood_drag_v", [(6, 13), (18, 13)])
    m.face_row_decor(["sign_bio", "clock", "poster", "lamp", "sink", "board"], 3, 33, 2, every=3, seed=2)
    m.use(24, 15, "d01_pharmacy_door"); m.use(25, 15, "d01_pharmacy_door")
    m.interact[-1]["prompt"] = m.interact[-2]["prompt"] = L("[E] Knock", "[E] Llamar")
    m.item("bandage", 31, 13); m.item("doc_049_notice", 8, 9)
    for x, y, fl in [(6, 6, 0), (16, 6, 0.3), (26, 6, 0), (10, 12, 0), (28, 12, 1.0)]:
        m.light(x, y, COLD, 1.1, 0.9, fl)
    m.actor("chaser", 14, 12, sprite="zombie", battle="zombie", speed=0.42, sight=6, wander=4, groan="squelch")
    m.critters("fly", 21, 10, 8, 1); m.critters("roach", 30, 13, 8, 3)
    m.sound("hum", 16, 3, -12, 8)
    m.save()


def d02():
    m = Map("D02", L("Patient Wards", "Salas de pacientes"), 52, 22, "D", MED)
    m.room(2, 5, 48, 12, "w", L("Wards", "Salas"))
    m.room(16, 17, 2, 5, "w")
    m.exit(16, 21, 2, 1, "D01", "from_D02")
    m.spawn("from_D01", 16, 15, "north")
    m.door(10, 3, "h", level=3, did="D02_or")
    m.room(10, 0, 2, 3, "w")
    m.exit(10, 0, 2, 1, "D03", "from_D02")
    m.spawn("from_D03", 10, 6, "south")
    m.room(50, 9, 2, 2, "o")
    m.exit(51, 9, 1, 2, "D07", "from_D02")
    m.spawn("from_D07", 48, 9, "west")
    m.door(40, 17, "h", level=3, style="heavy", did="D02_049")
    m.room(40, 19, 2, 3, "w")
    m.exit(40, 21, 2, 1, "D08", "from_D02")
    m.spawn("from_D08", 40, 15, "north")
    for x in range(4, 48, 5):
        m.prop("med_bed", x, 6)
        if x % 3 == 1:
            m.prop("iv_stand", x + 3, 6)
    for x in range(4, 36, 8):
        m.prop("med_bed", x, 15)
    m.prop("body_cured", 14, 11, walk=True); m.prop("body_cured", 34, 12, walk=True); m.prop("gurney_body", 44, 13)
    m.prop("autopsy_tray", 24, 10); m.prop("wheelchair", 28, 14)
    m.scatter(["blood_drops", "suture", "bandage", "syringe", "pills", "papers", "lavender"], 2, 5, 48, 12, 34, seed=3)
    m.trail("blood_drag_h", "blood_drag_v", [(8, 12), (8, 10), (30, 10)])
    m.face_row_decor(["window", "clock", "sign_bio", "lamp", "screen", "sink"], 3, 49, 4, every=4, seed=4)
    m.item("doc_ward_chart", 21, 13); m.item("medkit", 47, 15)
    for x in range(6, 50, 8):
        m.light(x, 8, COLD, 1.0, 0.8, 0.9 if x in (22, 38) else 0.0)
    m.actor("scp049", 30, 9, sprite="scp049", route=ROUTE_WARDS, cond="!scp049_contained,!follow049", event="scp049_meet")
    m.actor("chaser", 8, 14, sprite="zombie", battle="zombie", speed=0.42, sight=6, wander=3, groan="squelch")
    m.actor("chaser", 36, 13, sprite="zombie_guard", battle="zombie_guard", speed=0.45, sight=6, wander=3, groan="squelch")
    m.critters("fly", 14, 11, 8, 1); m.critters("fly", 44, 13, 8, 1); m.critters("roach", 26, 15, 10, 4)
    m.sound("hum", 26, 5, -14, 12)
    m.trigger(2, 5, 6, 12, "d02_enter")
    m.save()


def d03():
    m = Map("D03", L("Operating Theatre", "Quirófano"), 30, 20, "D", dict(MED, fog=0.1, ambient="#0e1214"))
    m.room(2, 3, 26, 12, "w", L("Theatre", "Quirófano"))
    m.room(10, 15, 2, 5, "w")
    m.exit(10, 19, 2, 1, "D02", "from_D03")
    m.spawn("from_D02", 10, 13, "north")
    m.prop("operating_lamp", 12, 7)
    m.prop("surgical_table", 20, 8); m.prop("autopsy_tray", 17, 8); m.prop("autopsy_tray", 9, 8)
    m.prop("med_cabinet", 3, 4); m.prop("specimen_shelf", 24, 4); m.prop("gurney_body", 4, 11); m.prop("gurney_body", 22, 12)
    m.prop("body_cured", 14, 12, walk=True)
    m.scatter(["blood_pool", "blood_splat", "suture", "scalpel", "tray", "syringe"], 2, 3, 26, 12, 20, seed=5)
    m.decor("blood_write", 10, 2); m.decor("screen", 16, 2); m.decor("sink", 6, 2); m.decor("blood_hand", 20, 2)
    m.item("doc_049_interview", 26, 12); m.item("adrenaline", 3, 13)
    m.light(13, 7, "#ffffff", 1.2, 1.2, 0.0); m.light(22, 11, COLD, 0.8, 0.7, 0.8)
    m.actor("chaser", 22, 6, sprite="zombie_guard", battle="zombie_guard", speed=0.45, sight=7, wander=3, groan="squelch")
    m.critters("fly", 14, 12, 10, 1)
    m.trigger(8, 9, 10, 5, "d03_enter")
    m.save()


def d04():
    m = Map("D04", L("Morgue", "Morgue"), 34, 20, "D", dict(MED, ambient="#0a0e12", fog=0.2, fog_color="#c0d8e8"))
    m.room(2, 3, 30, 12, "w", L("Morgue", "Morgue"))
    m.room(0, 8, 2, 2, "w")
    m.exit(0, 8, 1, 2, "D01", "from_D04")
    m.spawn("from_D01", 2, 8, "east")
    m.door(32, 8, "v", did="D04_cold")
    m.room(33, 8, 1, 2, "t")
    m.exit(33, 8, 1, 2, "D05", "from_D04")
    m.spawn("from_D05", 30, 8, "west")
    for x in (4, 12, 20):
        m.prop("morgue_drawers", x, 4)
    for x, y in [(6, 10), (14, 12), (22, 10), (27, 12)]:
        m.prop("body_bag" if (x + y) % 2 else "gurney_body", x, y)
    m.prop("body_sheet", 10, 13, walk=True)
    m.scatter(["blood_drops", "wet", "condensation", "tray", "suture"], 2, 3, 30, 12, 18, seed=6)
    m.decor("clock", 28, 2); m.decor("sign_bio", 26, 2)
    m.item("doc_morgue_tag", 18, 13)
    m.light(8, 7, COLD, 0.9, 0.8, 0.6); m.light(24, 7, COLD, 0.9, 0.8, 0.0)
    m.critters("fly", 14, 12, 10, 2); m.critters("fly", 22, 10, 6, 1)
    m.sound("fridge", 12, 3, -8, 12)
    m.trigger(10, 5, 8, 3, "d04_drawer")
    m.save()


def d05():
    m = Map("D05", L("Cold Storage", "Cámara frigorífica"), 24, 16, "D",
            dict(MED, ambient="#0c141c", fog=0.35, fog_color="#dff0ff", amb="med"))
    m.room(2, 3, 20, 9, "t", L("Cold storage", "Cámara frigorífica"))
    m.room(0, 6, 2, 2, "t")
    m.exit(0, 6, 1, 2, "D04", "from_D05")
    m.spawn("from_D04", 2, 6, "east")
    for x in (4, 8, 12, 16):
        m.prop("cryo_tank", x, 5)
    m.prop("body_bag", 6, 10); m.prop("body_bag", 14, 9); m.prop("specimen_shelf", 18, 9)
    m.scatter(["condensation", "wet", "puddle"], 2, 3, 20, 9, 20, seed=7)
    m.sfx_fx("mist", 11, 7, w=10, h=4)
    m.item("medkit", 20, 10); m.item("doc_cold_storage", 3, 10)
    m.light(11, 7, COLD, 1.0, 0.8, 0.0)
    m.sound("fridge", 11, 4, -6, 10)
    m.save()


def d06():
    m = Map("D06", L("Pharmacy", "Farmacia"), 24, 16, "D", dict(MED, ambient="#12151a"))
    m.room(2, 3, 20, 9, "w", L("Pharmacy", "Farmacia"))
    m.room(8, 0, 2, 3, "w")
    m.exit(8, 0, 2, 1, "D01", "from_D06")
    m.spawn("from_D01", 8, 4, "south")
    m.prop("med_cabinet", 3, 4); m.prop("med_cabinet", 12, 4); m.prop("med_cabinet", 16, 4); m.prop("chem_shelf", 19, 8)
    m.prop("table_flipped", 7, 6); m.prop("mattress", 14, 9); m.prop("lantern", 17, 10, walk=True)
    m.scatter(["pills", "pills", "syringe", "papers", "wrappers"], 2, 3, 20, 9, 14, seed=8)
    m.npc("lin", 16, 7, "west", mode="idle")
    m.item("adrenaline", 4, 10); m.item("bandage", 20, 5)
    m.light(12, 6, COLD, 1.0, 0.9, 0.0); m.light(17, 10, "#ffd080", 0.5, 0.6, 0.0)
    m.save()


def d07():
    m = Map("D07", L("Hydroponics Greenhouse", "Invernadero hidropónico"), 30, 20, "D",
            dict(MED, ambient="#120e16", fog=0.18, fog_color="#b8a0d8"))
    m.room(2, 3, 26, 12, "o", L("Greenhouse", "Invernadero"))
    m.room(0, 8, 2, 2, "o")
    m.exit(0, 8, 1, 2, "D02", "from_D07")
    m.spawn("from_D02", 2, 8, "east")
    for x, y in [(4, 4), (10, 4), (16, 4), (22, 4)]:
        m.prop("grow_rack", x, y)
    for x, y in [(5, 9), (12, 9), (19, 9), (5, 12), (19, 12)]:
        m.prop("lavender_bed", x, y)
    m.scatter(["lavender", "moss", "puddle", "papers"], 2, 3, 26, 12, 20, seed=9)
    m.item("lavender", 13, 12)
    for x in (6, 12, 18, 24):
        m.light(x, 5, "#c080ff", 1.0, 0.9, 0.0)
    m.actor("chaser", 22, 11, sprite="zombie", battle="zombie", speed=0.42, sight=6, wander=4, groan="squelch")
    m.critters("moth", 12, 5, 6, 1); m.critters("fly", 20, 10, 4, 1)
    m.sound("water", 14, 6, -14, 8)
    m.save()


def d08():
    """SCP-049's Standard Secure Humanoid Containment Cell: it made it a study."""
    m = Map("D08", L("SCP-049 Containment", "Contención de SCP-049"), 22, 16, "D", dict(MED, ambient="#141014", fog=0.08))
    m.room(2, 3, 18, 9, "c", L("049's study", "El estudio de 049"))
    m.room(8, 0, 2, 3, "w")
    m.exit(8, 0, 2, 1, "D02", "from_D08")
    m.spawn("from_D02", 8, 4, "south")
    m.prop("workbench", 13, 5); m.prop("bookshelf", 3, 4); m.prop("bookshelf", 5, 4)
    m.prop("bed_unmade", 16, 9); m.prop("candles", 12, 9, walk=True); m.prop("specimen_jar", 15, 6, walk=True)
    m.prop("books", 10, 6, walk=True); m.prop("lavender_bed", 3, 9)
    m.scatter(["lavender", "papers", "suture"], 2, 3, 18, 9, 10, seed=10)
    m.decor("board", 12, 2); m.decor("clock", 16, 2); m.sign(9, 2, L("SCP-049", "SCP-049"), "scp")
    m.item("doc_049_journal", 13, 7)
    m.light(12, 8, "#ffd8a0", 0.9, 0.8, 0.0)
    m.trigger(4, 5, 12, 6, "d08_contain", cond="follow049")
    m.save()


def build():
    for f in (d01, d02, d03, d04, d05, d06, d07, d08):
        f()
