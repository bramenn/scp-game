"""Asset specs for tools/pixellab.py. Scale: 16 px tile ≈ 0.85 m, humans ≈ 34 px tall on a 48 px canvas."""

HUMAN = dict(kind="char", size=48, proportions="realistic_male", anims=["walking-6-frames"])
WOMAN = dict(HUMAN, proportions="realistic_female")

SPECS = {
    # --- calibration batch -------------------------------------------------
    "ortega": dict(HUMAN, desc="middle-aged Latino security sergeant, grey security guard uniform, black tactical vest, "
                              "black cap, thick mustache, bloody bandage on left arm"),
    "desk_pc": dict(kind="obj", size=32, desc="office desk with old beige CRT computer monitor, keyboard, scattered "
                                              "papers and a coffee mug, top-down game prop"),
    "p_ortega": dict(kind="portrait", **{"from": "art/chars/ortega/south.png"}, size=64),
}
