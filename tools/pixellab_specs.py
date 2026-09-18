"""Asset specs for tools/pixellab.py.

Scale rules (16 px tile ≈ 0.85 m):
  * humans: request size 32 -> 48 px canvas, ~37 px tall figure (≈1.8 m)
  * props: image size ≈ real size in px at ~19 px/m, rounded up to a multiple of 16
Style: gritty, muted, underground research facility, low top-down 3/4 view.
"""

HUMAN = dict(kind="char", size=32, proportions="realistic_male", anims=["walking-6-frames"])
WOMAN = dict(HUMAN, proportions="realistic_female")
STYLE = "top-down RPG prop, gritty underground SCP research facility, muted realistic colors, "


def prop(desc, size=32, h=None, mode=None):
    d = dict(kind="obj", size=size, desc=STYLE + desc)
    if h:
        d["h"] = h
    if mode:
        d["mode"] = mode
    return d


def body(desc, w=48, h=32):
    return dict(kind="obj", mode="pixflux", size=w, h=h, dir="art/props",
                desc="top-down view of " + desc + ", lying on the floor, dark gritty pixel art, horror game")


SPECS = {
    # ------------------------------------------------------------ calibration (kept)
    "ortega": dict(HUMAN, size=48, desc="middle-aged Latino security sergeant, grey security guard uniform, black tactical "
                                        "vest, black cap, thick mustache, bloody bandage on left arm"),
    "desk_pc": prop("office desk with old beige CRT computer monitor, keyboard, scattered papers and a coffee mug"),
    "p_ortega": dict(kind="portrait", size=64, **{"from": "art/chars/ortega/south.png"}),
    "vega": dict(HUMAN, desc="male SCP Foundation field agent, black tactical uniform, black armored vest with small "
                             "orange Foundation patch, short brown hair, holstered pistol, flashlight on vest",
                 anims=["walking-6-frames", "running-6-frames"]),
    "ortega32": dict(HUMAN, desc="middle-aged Latino security sergeant, grey security guard uniform, black tactical vest, "
                                 "black cap, thick mustache, bloody bandage on left arm"),

    # ------------------------------------------------------------------ humans
    "nico": dict(HUMAN, desc="young skinny man in his early twenties, bright orange D-class prisoner jumpsuit with number "
                             "patch, shaved head, frightened, dirty face"),
    "lin": dict(WOMAN, desc="East Asian female doctor in her forties, white lab coat over dark sweater, black hair in a "
                            "tight bun, rectangular glasses, ID badge"),
    "reyes": dict(HUMAN, desc="Nine-Tailed Fox soldier, black full tactical armor, helmet with visor up, fox patch on "
                              "shoulder, rifle, blood on armor, exhausted"),
    "tomas": dict(HUMAN, desc="old janitor in his sixties, faded grey coveralls, flat cap, grey beard, big key ring on "
                              "belt, holding a flashlight"),
    "adebayo": dict(HUMAN, desc="tall Nigerian scientist, white lab coat with brass oil stains, safety goggles on forehead, "
                                "short grey hair, holding a wrench"),
    "elena": dict(WOMAN, desc="female researcher in her thirties, white lab coat, dark brown hair in a ponytail, tired "
                              "face, bandaged hand, ID badge"),
    "mara": dict(WOMAN, desc="Chaos Insurgency operative woman, olive drab combat fatigues, black balaclava pulled down, "
                             "red armband, compact rifle"),
    "dclass": dict(HUMAN, desc="bald middle-aged man in an orange D-class prisoner jumpsuit, stubble, nervous"),
    "scientist": dict(HUMAN, desc="male scientist in a white lab coat, glasses, clipboard, grey trousers"),
    "guard": dict(HUMAN, desc="Foundation security guard, dark blue uniform, black helmet, tactical vest, baton"),
    "zombie": dict(HUMAN, desc="pale reanimated corpse in a torn blue hospital gown, long stitched surgical incisions on "
                               "chest and neck, grey skin, blank white eyes, shambling",
                   anims=["scary-walk"]),
    "zombie_guard": dict(HUMAN, desc="pale reanimated corpse of a security guard, torn dark uniform, stitched Y incision, "
                                     "grey skin, blank white eyes, shambling", anims=["scary-walk"]),

    # -------------------------------------------------------------------- SCPs
    "scp173": dict(kind="char", size=36, anims=[], proportions="realistic_male",
                   desc="SCP-173 statue made of rough grey concrete and rusty rebar, thin elongated humanoid body, "
                        "oversized round head, crude red and green spray paint face markings, no clothes, arms at sides"),
    "scp096": dict(kind="char", size=40, proportions="realistic_male", anims=["scary-walk", "running-6-frames"],
                   desc="SCP-096, extremely tall emaciated pale humanoid, no hair, pale white skin, very long thin "
                        "arms reaching the knees, huge jaw, blank white eyes, hunched"),
    "scp106": dict(kind="char", size=32, proportions="realistic_male", anims=["scary-walk"],
                   desc="SCP-106 the Old Man, elderly decomposed humanoid, black rotting corroded skin dripping black "
                        "mucus, grinning, hunched, tattered dark clothes"),
    "scp049": dict(kind="char", size=34, proportions="realistic_male", anims=["walking-6-frames"],
                   desc="SCP-049 plague doctor, long black hooded robe, white beaked ceramic plague mask, black "
                        "gloves, black leather doctor bag"),
    "scp939": dict(kind="char", size=48, template="dog", anims=["walking-6-frames"],
                   desc="SCP-939, large quadruped predator, translucent red skin, eyeless elongated head, long jaw "
                        "full of teeth, lean muscular body, four clawed limbs"),
    "scp682": dict(kind="char", size=64, template="lion", anims=["walking-6-frames"],
                   desc="SCP-682, huge hard-to-destroy reptile, scarred dark green scaly hide, damaged plates, "
                        "massive jaws, glowing eyes, thick tail"),
    "scp529": dict(kind="char", size=24, template="cat", anims=["walking-6-frames"],
                   desc="grey tabby house cat whose body ends abruptly at the ribcage, the missing half is pure black"),
    "rat": dict(kind="char", size=16, template="dog", anims=["walking-6-frames"],
                desc="small brown sewer rat, long pink tail, dirty fur"),
    "scp131a": prop("SCP-131-A, small burnt orange teardrop-shaped creature with one big blue eye and a small "
                    "wheel at the bottom", 32, mode="pixflux"),
    "scp131b": prop("SCP-131-B, small mustard yellow teardrop-shaped creature with one big blue eye and a small "
                    "wheel at the bottom", 32, mode="pixflux"),
    "scp999": prop("SCP-999, translucent orange gelatinous blob, dome shaped, happy, glossy highlights", 32, mode="pixflux"),
    "scp087_face": prop("SCP-087-1, a pale floating human face with no eyes pupils nostrils or mouth, glowing faintly "
                        "in total darkness, horror", 32, mode="pixflux"),

    # ------------------------------------------------------------------ bodies
    "body_guard": body("a dead security guard in dark blue uniform, helmet, blood pool"),
    "body_scientist": body("a dead scientist in a white lab coat, face down, blood"),
    "body_dclass": body("a dead man in an orange D-class jumpsuit, twisted neck"),
    "body_ntf": body("a dead soldier in black tactical armor with helmet, rifle beside him"),
    "body_bag": body("a closed black body bag with a zipper"),
    "body_aged": body("a horribly aged decayed corpse covered in black corrosion, rotten clothes"),
    "body_dissolved": body("a half dissolved corpse in acid, bones showing, green acid"),
    "body_cured": body("a pale corpse with a long stitched Y surgical incision on the chest, hospital gown"),

    # ------------------------------------------------------------ props: offices
    "office_chair": prop("black office swivel chair", 16),
    "filing_cabinet": prop("grey metal filing cabinet with four drawers, one drawer open with folders", 16, 32),
    "bookshelf": prop("metal shelf full of binders and document boxes", 32),
    "water_cooler": prop("office water cooler with blue bottle", 16, 32),
    "plant_dead": prop("dead potted office plant with brown drooping leaves", 16, 32),
    "reception_desk": prop("long curved reception desk with computer monitors and a desk bell", 64, 32),
    "bench": prop("metal waiting room bench with three seats", 48, 16),
    "vending": prop("snack vending machine with glowing front panel, one glass cracked", 32),
    "scp294": prop("SCP-294 coffee vending machine, beige, with a QWERTY keyboard on the front and a coin slot", 32),
    "cctv_wall": prop("security desk with a wall of many small CRT monitors showing grainy camera feeds", 64, 32),
    "metal_detector": prop("walk-through airport style metal detector arch", 32),
    "xray": prop("x-ray baggage scanner with conveyor belt", 48, 32),
    "server_rack": prop("tall black server rack with blinking green and red LEDs", 16, 32),
    "server_rack_broken": prop("tall black server rack with open door, torn cables and sparks", 16, 32),
    "crt_terminal": prop("old 1980s computer terminal with a green phosphor CRT screen on a metal desk", 32),
    "printer": prop("large office photocopier", 32),
    "whiteboard": prop("rolling whiteboard with diagrams and hastily erased writing", 32),
    "conf_table": prop("long conference table with chairs around it, papers scattered", 64, 32),
    "trash_can": prop("metal trash can overflowing with paper", 16),
    "chair_fallen": prop("office chair knocked over on its side", 16),
    "boxes": prop("stack of cardboard boxes with Foundation labels", 32),
    "locker_row": prop("row of three grey metal staff lockers, one door hanging open", 48, 32),
    "bunk_bed": prop("metal bunk bed with grey blankets", 32),
    "bed_unmade": prop("single bed with messy white sheets", 32),
    "footlocker": prop("green metal footlocker trunk", 32, 16),
    "toilet": prop("white porcelain toilet", 16),
    "shower": prop("shower stall with tiled floor and a drain, dirty curtain", 32),
    "fridge": prop("tall industrial kitchen refrigerator, stainless steel", 32),
    "kitchen_counter": prop("stainless steel kitchen counter with pots and a cutting board", 48, 32),
    "stove": prop("industrial kitchen stove with big pots", 32),
    "cafe_table": prop("cafeteria table with attached benches, food trays left behind", 48, 32),
    "tray_spill": prop("overturned cafeteria tray with spilled food on the floor", 16),

    # ------------------------------------------------------------- props: medical
    "med_bed": prop("hospital bed with rails and white sheets, bloodstains", 32),
    "med_cabinet": prop("white medical supply cabinet with glass doors", 32),
    "iv_stand": prop("IV drip stand with a hanging bag", 16, 32),
    "wheelchair": prop("empty old wheelchair", 16),
    "gurney_body": prop("hospital gurney with a corpse covered by a bloodstained white sheet", 32),
    "morgue_drawers": prop("wall of stainless steel morgue body drawers, one drawer pulled open", 48, 32),
    "surgical_table": prop("operating table with leather restraints and surgical light above", 32),
    "autopsy_tray": prop("rolling tray with bloody surgical instruments", 16),
    "specimen_shelf": prop("shelf with glass specimen jars containing organs in yellow fluid", 32),
    "cryo_tank": prop("tall frosted cryogenic storage tank with pipes", 32),
    "lavender_bed": prop("raised planter bed full of blooming purple lavender", 32),
    "grow_rack": prop("hydroponic grow rack with plants under purple grow lights", 32),

    # ------------------------------------------------------------------ props: LCZ
    "lab_bench": prop("laboratory bench with microscopes, beakers and a computer", 48, 32),
    "chem_shelf": prop("chemical shelf with labeled bottles and hazard stickers", 32),
    "fume_hood": prop("laboratory fume hood with glass sash", 32),
    "scp_crate": prop("heavy grey containment crate with yellow hazard stripes and a keypad lock", 32),
    "scp914": prop("SCP-914, enormous clockwork machine of brass and copper with thousands of gears, a big dial "
                   "with settings Rough Coarse 1:1 Fine Very Fine", 96, 64),
    "scp914_booth": prop("brass booth with a sliding door connected by copper tubing, part of a clockwork machine", 32, 48),
    "iron_box": prop("small iron box hanging from chains, sealed, SCP-012 containment", 32),
    "candy_bowl": prop("big bowl full of colorful candies and chocolate", 16),
    "toy_pile": prop("pile of colorful children's toys, balls and a teddy bear", 32),
    "cat_bed": prop("small round cat bed with a blanket", 16),
    "pill_case": prop("glass display pedestal holding a small plastic container of red pills", 16, 32),
    "gun_rack": prop("armory weapon rack with rifles, several missing", 32),
    "ammo_crates": prop("stack of green military ammunition crates", 32),
    "cell_bunk": prop("prison cell concrete bunk with a thin orange mattress", 32, 16),
    "prison_toilet": prop("steel prison toilet and sink combination", 16),

    # ------------------------------------------------------------------ props: HCZ
    "tesla_gate": prop("tesla gate, two tall electric coil pylons with crackling blue arcs between them", 48),
    "generator": prop("huge diesel generator with pipes, gauges and warning labels", 64, 48),
    "transformer": prop("electrical transformer box with high voltage warning signs", 32),
    "valve_big": prop("large pipe junction with a red valve wheel", 32),
    "femur_breaker": prop("sinister medical machine with a padded restraint chair and a hydraulic press over the leg", 48, 32),
    "control_console": prop("wide control console with many switches, dials and red buttons", 48, 32),
    "restraint_chair": prop("heavy metal chair with leather restraint straps", 16, 32),
    "sandbags": prop("sandbag barricade wall", 48, 16),
    "table_flipped": prop("metal table flipped on its side as cover, bullet holes", 32),
    "stretcher": prop("military folding stretcher with bloody blanket", 32, 16),
    "radio_station": prop("military radio equipment on a crate with antenna", 32),
    "turret": prop("disabled automated security turret on a tripod", 32),
    "pressure_pad": prop("floor pressure sensor plate with cables", 16),
    "acid_railing": prop("yellow steel safety railing section", 32, 16),

    # --------------------------------------------------------- props: maintenance
    "boiler": prop("big rusty industrial boiler with pressure gauges and steam pipes", 48),
    "pump": prop("industrial water pump with pipes and a big motor", 32),
    "breaker": prop("electrical breaker cabinet with a large lever switch", 16, 32),
    "toolbox": prop("red metal toolbox, open, tools spilling", 16),
    "workbench": prop("cluttered workbench with a vise and tools", 48, 32),
    "janitor_cart": prop("janitor cart with mop bucket, spray bottles and trash bag", 32),
    "mattress": prop("dirty old mattress on the floor with a blanket and a pillow", 32),
    "burn_barrel": prop("rusty burn barrel with a small fire inside", 16, 32),
    "rat_nest": prop("pile of shredded paper, rags and garbage, rat nest", 32),
    "spider_web": prop("big dusty spider web in a corner", 32),
    "pipes_floor": prop("bundle of large pipes running along the floor", 48, 16),
    "ladder": prop("steel maintenance ladder going down into a hole", 16, 32),

    # --------------------------------------------------------- props: pocket / core
    "pillar_rot": prop("rotting black organic pillar with veins, dimension of decay", 32, 48),
    "throne": prop("throne made of rotten black flesh and bones", 48),
    "bone_pile": prop("pile of human bones covered in black slime", 32),
    "floating_door": prop("old wooden door frame standing alone, dark corroded", 32, 48),
    "supercomputer": prop("wall of 1980s supercomputer cabinets with tape reels and blinking lights", 64, 32),
    "core_terminal": prop("large main computer terminal with a big CRT showing a red X, cables everywhere", 48, 32),
    "warhead_panel": prop("nuclear warhead control panel with two key slots, lever and red warning lights", 48, 32),

    # ---------------------------------------------------------------- props: misc
    "pallet": prop("wooden pallet with plastic wrapped supplies", 32),
    "forklift": prop("small yellow forklift", 48),
    "cone": prop("orange traffic cone", 16),
    "caution_sign": prop("yellow wet floor caution sign stand", 16),
    "ceiling_panel": prop("fallen ceiling panel and broken fluorescent tube on the floor", 32, 16),
    "debris_pile": prop("pile of concrete debris and twisted rebar", 32),
    "glass_panel": prop("shattered glass observation panel pieces", 32, 16),
    "mop_bucket": prop("yellow mop bucket with a mop", 16),
    "extinguisher_floor": prop("red fire extinguisher standing on the floor", 16),
    "body_sheet": prop("human shape under a white sheet on the floor, bloodstain", 32, 16),
}
