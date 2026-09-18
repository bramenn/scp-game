"""Asset specs for tools/pixellab.py.

Scale rules (16 px tile ≈ 0.85 m):
  * humans: request size 32 -> 48 px canvas, ~37 px tall figure (≈1.8 m)
  * props: image size ≈ real size in px at ~19 px/m, rounded up to a multiple of 16
Style: gritty, muted, underground research facility, low top-down 3/4 view.
"""

HUMAN = dict(kind="char", size=32, proportions="realistic_male", anims=["walking-6-frames"])
WOMAN = dict(HUMAN, proportions="realistic_female")
STYLE = "top-down RPG prop, gritty underground SCP research facility, muted realistic colors, "
BATCH_STYLE = "top-down RPG game props for a gritty underground SCP research facility, 3/4 view, muted realistic colors, "


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
    "scp939": dict(kind="char", size=48, template="dog", anims=["walk-6-frames"],
                   desc="SCP-939, large quadruped predator, translucent red skin, eyeless elongated head, long jaw "
                        "full of teeth, lean muscular body, four clawed limbs"),
    "scp682": dict(kind="char", size=64, template="lion", anims=["walk-6-frames"],
                   desc="SCP-682, huge hard-to-destroy reptile, scarred dark green scaly hide, damaged plates, "
                        "massive jaws, glowing eyes, thick tail"),
    "scp529": dict(kind="char", size=24, template="cat", anims=["walk-6-frames"],
                   desc="grey tabby house cat whose body ends abruptly at the ribcage, the missing half is pure black"),
    "rat": dict(kind="char", size=16, template="dog", anims=["walk-6-frames"],
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

    # ------------------------------------------------ props: batches (one style per batch)
    "props16": dict(kind="batch", size=16, desc=BATCH_STYLE + "small objects", items={
        "trash_can": "metal office trash can overflowing with paper",
        "extinguisher_floor": "red fire extinguisher standing on the floor",
        "cone": "orange traffic cone",
        "caution_sign": "yellow wet floor caution sign",
        "mop_bucket": "yellow mop bucket with a mop",
        "toolbox": "open red metal toolbox with tools",
        "cat_bed": "small round cat bed with a grey blanket",
        "candy_bowl": "glass bowl full of colorful candies",
        "autopsy_tray": "steel tray with bloody surgical instruments",
        "pressure_pad": "floor pressure sensor plate with cables",
        "wheelchair": "empty old wheelchair",
        "tray_spill": "overturned cafeteria food tray with spilled food",
        "chair_fallen": "black office chair knocked over on its side",
        "toilet": "white porcelain toilet",
        "prison_toilet": "stainless steel prison toilet",
        "helmet": "dropped black tactical helmet",
        "gas_mask": "dropped gas mask",
        "rifle": "assault rifle lying on the floor",
        "clipboard": "clipboard with papers",
        "laptop": "broken open laptop",
        "phone": "old desk telephone with the handset hanging",
        "teddy": "worn teddy bear",
        "ball": "red rubber ball",
        "bottles": "cluster of empty glass bottles",
        "pizza": "open pizza box with a half eaten pizza",
        "skull": "human skull",
        "lantern": "battery camping lantern",
        "candles": "melted candles on the floor",
        "flashlight": "dropped flashlight",
        "cardboard": "flattened cardboard box",
        "bucket": "rusty metal bucket",
        "bag_trash": "black garbage bag",
        "shoes": "pair of shoes left on the floor",
        "books": "stack of old books",
        "mug": "coffee mug",
        "first_aid": "white first aid box with a red cross",
        "chair_plastic": "grey plastic chair",
        "stool": "metal lab stool",
        "sign_stand": "small standing sign that reads KEEP OUT",
        "vent_floor": "floor ventilation grate",
        "drain": "floor drain",
        "pipe_valve": "small red pipe valve",
        "gas_can": "red gas can",
        "sprayer": "janitor spray bottle",
        "bone": "gnawed bone",
        "rat_trap": "rat trap with cheese",
        "radio_small": "small portable radio",
        "cassette": "cassette tape recorder",
        "blood_bucket": "bucket full of blood",
        "syringes": "pile of used syringes",
        "specimen_jar": "glass specimen jar with a floating organ",
        "plant_small": "small dead potted plant",
        "wet_floor_towel": "dirty wet towel",
        "keys": "ring of keys",
        "dogtags": "military dog tags on a chain",
        "microscope": "laboratory microscope",
        "beaker": "lab beaker with green liquid",
        "cheese_block": "block of yellow cheese",
        "cup": "paper coffee cup",
        "gloves": "pair of bloody latex gloves",
    }),
    "props32a": dict(kind="batch", size=32, desc=BATCH_STYLE + "furniture", items={
        "filing_cabinet": "grey metal filing cabinet, one drawer open",
        "water_cooler": "office water cooler with a blue bottle",
        "plant_dead": "tall dead potted office plant",
        "server_rack": "tall black server rack with green and red LEDs",
        "server_rack_broken": "server rack with open door and torn cables",
        "iv_stand": "IV drip stand with a hanging bag",
        "bookshelf": "metal shelf with binders and document boxes",
        "vending": "snack vending machine, one glass cracked",
        "scp294": "beige coffee vending machine with a keyboard on the front",
        "fridge": "tall stainless steel kitchen refrigerator",
        "stove": "industrial kitchen stove with big pots",
        "med_cabinet": "white medical supply cabinet with glass doors",
        "locker": "single grey staff locker, door ajar",
        "specimen_shelf": "shelf with glass specimen jars in yellow fluid",
        "cryo_tank": "tall frosted cryogenic tank with pipes",
        "chem_shelf": "chemical shelf with labeled bottles and hazard stickers",
    }),
    "props32b": dict(kind="batch", size=32, desc=BATCH_STYLE + "furniture", items={
        "fume_hood": "laboratory fume hood with a glass sash",
        "gun_rack": "armory rack with rifles, some missing",
        "ammo_crates": "stack of green ammunition crates",
        "boxes": "stack of cardboard boxes",
        "bunk_bed": "metal bunk bed with grey blankets",
        "bed_unmade": "single bed with messy sheets",
        "med_bed": "hospital bed with rails and stained sheets",
        "shower": "shower stall with a dirty curtain",
        "whiteboard": "rolling whiteboard with diagrams",
        "printer": "large office photocopier",
        "crt_terminal": "1980s computer terminal with a green CRT on a metal desk",
        "transformer": "electrical transformer box with high voltage signs",
        "valve_big": "large pipe junction with a red valve wheel",
        "pump": "industrial water pump with a motor",
        "breaker": "electrical breaker cabinet with a big lever",
        "burn_barrel": "rusty burn barrel with a small fire",
    }),
    "props32c": dict(kind="batch", size=32, desc=BATCH_STYLE + "objects", items={
        "ladder": "steel ladder going down into a dark hole",
        "spider_web": "big dusty spider web",
        "rat_nest": "pile of shredded paper and rags, a rat nest",
        "mattress": "dirty mattress on the floor with a blanket",
        "janitor_cart": "janitor cart with mop bucket and trash bag",
        "scp_crate": "grey containment crate with hazard stripes and a keypad",
        "iron_box": "small iron box hanging from chains",
        "toy_pile": "pile of colorful toys and a teddy bear",
        "pill_case": "glass pedestal holding a plastic container of red pills",
        "restraint_chair": "heavy metal chair with leather straps",
        "turret": "disabled security turret on a tripod",
        "radio_station": "military radio equipment on a crate",
        "table_flipped": "metal table flipped on its side, bullet holes",
        "pallet": "wooden pallet with wrapped supplies",
        "debris_pile": "pile of concrete debris and twisted rebar",
        "metal_detector": "walk-through metal detector arch",
    }),
    "props32d": dict(kind="batch", size=32, desc=BATCH_STYLE + "objects", items={
        "ceiling_panel": "fallen ceiling panel and broken fluorescent tube",
        "glass_panel": "shattered glass panel pieces",
        "body_sheet": "human shape under a bloodstained white sheet",
        "gurney_body": "gurney with a corpse under a bloodstained sheet",
        "surgical_table": "operating table with leather restraints",
        "lavender_bed": "raised planter full of purple lavender",
        "grow_rack": "hydroponic rack with plants under purple light",
        "bone_pile": "pile of human bones in black slime",
        "stretcher": "military stretcher with a bloody blanket",
        "cell_bunk": "concrete prison bunk with a thin orange mattress",
        "acid_railing": "yellow steel safety railing",
        "footlocker": "green metal footlocker trunk",
        "sink_stand": "old porcelain sink on a pedestal",
        "barrel": "rusty metal barrel",
        "crate": "wooden supply crate",
        "gurney": "empty hospital gurney",
    }),
    # ------------------------------------------------- props: wide / big (map-objects)
    "reception_desk": prop("long curved reception desk with monitors and a desk bell", 64, 32),
    "bench": prop("metal waiting room bench with three seats", 48, 32),
    "cctv_wall": prop("security desk under a wall of small CRT monitors with grainy camera feeds", 64, 32),
    "xray": prop("x-ray baggage scanner with conveyor belt", 48, 32),
    "conf_table": prop("long conference table with chairs, scattered papers", 64, 32),
    "locker_row": prop("row of three grey staff lockers, one door hanging open", 48, 32),
    "kitchen_counter": prop("stainless steel kitchen counter with pots and a cutting board", 48, 32),
    "cafe_table": prop("cafeteria table with attached benches and abandoned food trays", 48, 32),
    "morgue_drawers": prop("wall of steel morgue drawers, one pulled open", 48, 32),
    "lab_bench": prop("laboratory bench with microscopes, beakers and a computer", 48, 32),
    "scp914": prop("SCP-914, enormous clockwork machine of brass and copper gears with a large dial", 96, 64),
    "scp914_booth": prop("brass booth with a sliding door and copper tubing", 32, 48),
    "tesla_gate": prop("tesla gate, two electric coil pylons with blue arcs", 48, 48),
    "generator": prop("huge diesel generator with pipes, gauges and warning labels", 64, 48),
    "femur_breaker": prop("sinister machine with a padded restraint chair and a hydraulic press over the leg", 48, 32),
    "control_console": prop("wide control console with switches, dials and red buttons", 48, 32),
    "sandbags": prop("sandbag barricade wall", 48, 32),
    "boiler": prop("big rusty boiler with pressure gauges and steam pipes", 48, 48),
    "workbench": prop("cluttered workbench with a vise and tools", 48, 32),
    "pipes_floor": prop("bundle of large pipes running along the floor", 48, 32),
    "throne": prop("throne made of rotten black flesh and bones", 48, 48),
    "supercomputer": prop("wall of 1980s supercomputer cabinets with tape reels and blinking lights", 64, 32),
    "core_terminal": prop("large main computer terminal with a big CRT showing a red X, cables everywhere", 48, 32),
    "warhead_panel": prop("warhead control panel with two key slots, a lever and red warning lights", 48, 32),
    "forklift": prop("small yellow forklift", 48, 48),
    "pillar_rot": prop("rotting black organic pillar with veins", 32, 48),
    "floating_door": prop("old wooden door frame standing alone, corroded", 32, 48),

    # ------------------------------------------------------------- portraits
    "p_vega": dict(kind="portrait", size=64, **{"from": "art/chars/vega/south.png"}),
    "p_nico": dict(kind="portrait", size=64, **{"from": "art/chars/nico/south.png"}),
    "p_lin": dict(kind="portrait", size=64, **{"from": "art/chars/lin/south.png"}),
    "p_reyes": dict(kind="portrait", size=64, **{"from": "art/chars/reyes/south.png"}),
    "p_tomas": dict(kind="portrait", size=64, **{"from": "art/chars/tomas/south.png"}),
    "p_adebayo": dict(kind="portrait", size=64, **{"from": "art/chars/adebayo/south.png"}),
    "p_elena": dict(kind="portrait", size=64, **{"from": "art/chars/elena/south.png"}),
    "p_mara": dict(kind="portrait", size=64, **{"from": "art/chars/mara/south.png"}),
    "p_049": dict(kind="portrait", size=64, **{"from": "art/chars/scp049/south.png"}),

    # --------------------------------------- wide props redone as 64px Pro batches (fill the canvas)
    "wide64a": dict(kind="batch", size=64, desc=BATCH_STYLE + "large furniture", items={
        "reception_desk": "long curved reception desk with two computer monitors and a desk bell",
        "cctv_wall": "security desk under a wall of many small CRT monitors showing grainy camera feeds",
        "conf_table": "long conference table with office chairs around it and scattered papers",
        "supercomputer": "row of 1980s supercomputer cabinets with tape reels and blinking lights",
    }),
    "wide64b": dict(kind="batch", size=64, desc=BATCH_STYLE + "large machines", items={
        "scp914": "SCP-914, enormous clockwork machine of brass and copper, thousands of gears, pipes, a big dial in the middle",
        "femur_breaker": "sinister machine: padded restraint chair with a hydraulic press over the leg",
        "morgue_drawers": "wall of stainless steel morgue drawers, one drawer pulled open",
        "forklift": "small yellow forklift",
    }),
    "wide64c": dict(kind="batch", size=64, desc=BATCH_STYLE + "large furniture", items={
        "xray": "x-ray baggage scanner with a conveyor belt",
        "locker_row": "row of three grey staff lockers, one door hanging open",
        "lab_bench": "long laboratory bench with microscopes, beakers and a computer",
        "workbench": "cluttered workbench with a vise, tools and a lamp",
    }),
    "wide64d": dict(kind="batch", size=64, desc=BATCH_STYLE + "large objects", items={
        "kitchen_counter": "long stainless steel kitchen counter with pots and a cutting board",
        "sandbags": "sandbag barricade wall",
        "pipes_floor": "bundle of large rusty pipes running along the floor",
        "operating_lamp": "surgical operating table under a big round operating lamp",
    }),
}
