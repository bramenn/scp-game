# SCP: Site-19 — Breach · Design Document

Single-player top-down (FireRed-style grid movement) survival-horror RPG set in the
SCP Foundation universe. Godot 4.7, 480×270 pixel-perfect, English main language with
full Spanish translation. Target: **5+ hours** of play, large hand-designed site,
dread over jump-scares.

Source material: SCP Wiki (CC BY-SA 3.0). The whole game is released under CC BY-SA 3.0
(see `CREDITS.md`). The original SCP-173 photo (Izumi Kato sculpture) is **never** used;
our 173 sprite is original.

---

## 1. Pillars

1. **Dread, not jump-scares.** Darkness you manage (battery), sounds you can't place,
   vermin that flee your light, lights that die when something passes. Maybe 3-4 real
   scares in the whole game; everything else is atmosphere.
2. **Each SCP is its own mechanic**, faithful to its article (173 moves when unseen,
   096 hunts whoever sees its face, 106 walks through walls and is repelled by light,
   049 talks, 939 hunts by sound and speaks with the voices of the dead).
3. **A place that feels real and big.** ~60 individual maps in 7 sectors, every room has
   a purpose, props that tell what happened there, documents, bodies, traces.
4. **A story that hooks.** A personal mystery (your sister), a manipulator (SCP-079),
   moral choices (femur breaker), three endings.

## 2. Story

**Protagonist:** Agent **Vega**, ex-MTF Epsilon-11 "Nine-Tailed Fox". Sent alone into
Site-19 after a cascading containment breach at 03:12. Personal stake: his sister,
**Dr. Elena Vega**, a researcher on the classified *Project Threshold* (SCP-079 study),
is missing inside.

**Command** (radio): *Operator Kessler*, Site-17 relay. Voice of the Foundation: calm,
pragmatic, increasingly cold.

**The truth (revealed gradually):**
- The breach was triggered with a forged O5 credential from inside the site.
- Elena discovered *Protocol Black Tide*: O5 order to use D-class personnel as
  disposable feed in SCP-682 termination trials and to erase Site-19's D-class wing
  (amnestics + "retirement") once done.
- Elena and SCP-079 (moved to Site-19 for Project Threshold) opened the cells to create
  enough chaos for the D-class to be evacuated by a Chaos Insurgency cell that promised
  extraction.
- 079 betrayed her: it used the breach to reach SCP-682 (the one memory it never
  deletes) and to get a network bridge out of the site. Elena is locked in the 079 Core.

**Acts**
- **Prologue — Elevator B.** The service elevator creaks down 300 m. Power dies half
  way; emergency lights. Vega forces the doors into a dead reception. Tutorial (move,
  light, interact).
- **Act I — Entrance Zone.** Sgt. **Ortega** (wounded) gives Level-1 card and radio.
  First contact with **SCP-079** on a terminal ("HELLO, AGENT."). D-class **Nico
  (D-4417)** hiding in the cafeteria with rats → escort quest. Elena's office: first
  log of Project Threshold. Checkpoint to Light Containment.
- **Act II — Light Containment Zone.** SCP-173 loose (blink mechanic). **SCP-131**
  eye pods bond with you → they watch 173 for you. **SCP-914** lab (crafting, Dr.
  **Adebayo** stayed behind, obsessed). SCP-012 (sanity hazard), SCP-999 (comfort),
  D-class block (Nico's cell, his story). Recontain 173 in its chamber.
- **Act III — Maintenance & Sewers.** Power is down. Janitor **Tomás** lives down
  here with the rats; restore 3 breakers at the substation. Ortega goes ahead to the
  HCZ generator… and does not come back. Optional: **SCP-087** stairwell.
- **Act IV — Medical Wing.** SCP-049 walks the morgue with its "cured" (049-2).
  **Dr. Lin** hides in the pharmacy. Lavender calms 049 (article) → dialogue
  recontainment: you walk the Plague Doctor back to its cell. Lin gives the 096 bag.
- **Act V — Heavy Containment Zone.** 939 dark sector (a 939 speaks with **Ortega's**
  voice). Cpl. **Reyes** (last Nine-Tailed Fox) and his dog tags quest. SCP-096 stealth
  bagging. SCP-106 stalks through walls → **Pocket Dimension**. Femur breaker: sacrifice
  **Nico** (106 prefers ages 10-25) or use Reyes' recording (side quest) → recontain.
  SCP-682 boss in the acid chamber.
- **Act VI — 079 Core & Gate A.** 079 starts the Alpha Warhead countdown. Elena in the
  Core. Choice:
  - **Ending A "Containment"** – purge 079, recontain everything, hand Elena over.
  - **Ending B "Exodus"** – escape with Elena, Nico (if alive) and the D-class on the
    Chaos Insurgency helicopter; 079 purged.
  - **Ending C "Signal"** – let 079 through the uplink (it promised to save Elena). The
    lights come back on across the world, one by one. Bad ending.
  Epilogue lines vary with: Nico's fate, Ortega, Reyes, Josie (SCP-529), 131 bond,
  documents found.

## 3. Maps

Everything happens **inside Site-19, underground** (arrival is the elevator going down).
The site is **many individual hand-designed maps** (≈60) connected by doors, corridors,
elevators, stairs, ladders and vents — never one giant map. Each map has one purpose, its
own props, lighting, fog, sound bed and, near anomalies, the **traces that SCP leaves**.
Maps are authored in `tools/build_maps.py` (Python DSL → `data/maps/<id>.json`).

**Sector A — Entrance Zone (Level -1)**
A01 Elevator B arrival · A02 Reception lobby · A03 Security checkpoint (CCTV wall, Ortega) ·
A04 East corridor · A05 Administrative offices · A06 Elena's office · A07 Cafeteria (Nico) ·
A08 Kitchen & pantry · A09 Break room (SCP-294) · A10 Server room (079 terminal) ·
A11 Staff dormitories · A12 Infirmary · A13 Gate A hall (sealed) · A14 LCZ checkpoint

**Sector B — Light Containment (Level -2)**
B01 Decontamination airlock · B02 LCZ junction · B03 SCP-173 chamber · B04 173 observation ·
B05 Research corridor · B06 SCP-914 lab (Dr. Adebayo) · B07 SCP-012 room · B08 SCP-131 den ·
B09 SCP-999 cell · B10 SCP-500 vault · B11 D-class block · B12 D-class showers ·
B13 LCZ armory · B14 Vent crawlspace · B15 Maintenance access

**Sector C — Maintenance & Sewers (Level -3)**
C01 Maintenance stairs · C02 Pump room · C03 West sewer channel · C04 East sewer (spiders) ·
C05 Tomás' den · C06 Electrical substation (breakers) · C07 Boiler room · C08 SCP-087 access ·
C09 SCP-087 stairwell (repeating descent)

**Sector D — Medical Wing (Level -3 East)**
D01 Medical reception · D02 Wards · D03 Operating theatre · D04 Morgue · D05 Cold storage ·
D06 Pharmacy (Dr. Lin) · D07 Greenhouse (lavender) · D08 SCP-049 cell

**Sector E — Heavy Containment (Level -4)**
E01 HCZ elevator lobby · E02 939 dark sector A · E03 939 dark sector B · E04 939 containment
(Bio-Containment Area-14) · E05 NTF last stand (Reyes) · E06 HCZ armory · E07 SCP-096
chamber · E08 096 observation · E09 SCP-106 containment · E10 Femur breaker room ·
E11 Tesla gate corridor · E12 SCP-682 acid chamber · E13 682 control room · E14 Generator room

**Sector F — Pocket Dimension (106)**
F01 Rotting corridors · F02 The trench · F03 Pillar room · F04 The throne (exit)

**Sector G — SCP-079 Core & Gate A (Level -5)**
G01 Core access · G02 Server farm · G03 079 core (Elena) · G04 Warhead control · G05 Gate A lift

## 3b. What each anomaly does to its surroundings (always shown)

| SCP | Environmental traces |
|-----|---------------------|
| 173 | feces and blood stains on the cell floor (article), scrape grooves along its paths, cracked concrete, broken necks; scraping-stone sound when unseen |
| 106 | black mucus-like corrosion on floors/walls that keeps spreading, rust, rotting and cracking metal, decay smell (green haze); victims aged; lights fail near it |
| 096 | deep claw scratches on the 5 m steel cube, torn pressure sensors, smashed cameras, blood trails, distant crying |
| 049 | surgical trays, bloody instruments, bodies with stitched incisions (049-2), lavender, "cured" corpses sitting upright |
| 939 | 100 % humidity: condensation drips, standing water, cold fog; translucent red residue; amnestic haze; bite marks |
| 682 | hydrochloric acid puddles (green-yellow glow, fumes), torn 25 cm steel plates, gouges, dissolved remains |
| 012 | the room is kept dark; blood-written music on the walls, the iron box, victims |
| 999 | orange slime trails, candy wrappers (M&M's, Necco) |
| 131 | wheel tracks, toys, curious noises |
| 914 | brass gears, copper tubing, oil stains, refined junk |
| 079 | CRT glow, cables everywhere, overheated racks, text on every screen |
| 087 | light is swallowed (flashlight shortened), damp concrete, a child's crying far below |

## 4. Systems

- **Grid movement** (16 px tiles). Walk; **Shift = sprint** (stamina, loud).
- **Flashlight** (F): cone light in facing direction, battery drains, batteries found.
  Walls cast shadows (LightOccluder2D via TileSet occlusion).
- **Sanity**: drains in darkness, near anomalies, reading some documents; restored in
  lit safe rooms, by SCP-999, coffee (294), pills. Low sanity: heartbeat, whispers,
  vignette pulse, hallucinated vermin/shapes, desaturation. Zero: faint → reload.
- **Health**: damage from hazards/enemies; medkits.
- **Blink** (LCZ, near 173): blink meter; 173 moves only when unobserved or while you
  blink. 131 pods observing 173 freeze it.
- **Noise**: sprinting/doors emit noise events; 939 and zombies react.
- **Doors**: 2-tile sliding doors, keycard level L0-L5 or scripted locks (079 can lock).
- **Items/Inventory**: keycards, consumables, weapons/ammo, key items, documents.
  SCP-914 refines items (Rough/Coarse/1:1/Fine/Very Fine recipes).
- **Combat**: turn-based (existing battle scene) for zombies, 939, rats swarm, 682 boss.
  Weapons: baton (melee), pistol (ammo).
- **Dialogue** with portraits and choices; conditions/actions (flags, items, quests).
- **Events**: scripted sequences (say, wait, sfx, lights, spawn, move npc, shake, fade).
- **Quests / Journal**, **Documents archive**, **Automap** (explored tiles, rooms).
- **Save**: save terminals + autosave on zone change; death → reload.
- **Ambient life**: rats (flee light, squeak), cockroaches (scatter from light),
  spiders (descend on threads), moths around lamps, flies over bodies, drips, steam,
  sparks, fog/smoke, rain.
- **Audio**: positional one-shots and loops, per-surface footsteps, zone ambience
  layers, rare stingers.
- **i18n**: all text through `Loc` (EN default, ES selectable in Options).

## 5. SCPs used (article → mechanic)

| SCP | Name | Mechanic |
|-----|------|----------|
| 173 | The Sculpture | moves when unobserved / during blinks; neck snap |
| 131 | The "Eye Pods" | companions, watch 173, panic near danger |
| 914 | The Clockworks | crafting machine |
| 012 | A Bad Composition | sanity hazard room |
| 999 | The Tickle Monster | restores sanity, follows you briefly |
| 294 | The Coffee Machine | drinks with effects (coins) |
| 500 | Panacea | rare full heal |
| 529 | Josie the Half-Cat | side quest companion |
| 049 | Plague Doctor | talk / lavender / escort to cell; 049-2 zombies |
| 096 | The "Shy Guy" | do not see its face; bag it from behind |
| 106 | The Old Man | through walls, repelled by light, pocket dimension, femur breaker |
| 939 | With Many Voices | blind, hunts by sound, mimics the dead |
| 682 | Hard-to-Destroy Reptile | final containment boss (acid) |
| 079 | Old AI | antagonist voice, locks doors, core |
| 087 | The Stairwell | optional descent |

## 6. Art pipeline

- Tiles/UI/items/doors: procedural (`tools/gen_tiles.py`), fixed palette.
- Characters/SCPs/props/portraits: PixelLab (`tools/pixellab.py`, cached manifest in
  `tools/pixellab_manifest.json`), humanoids at 48 px canvas (≈34 px tall figure =
  1.8 m → ~19 px/m). Walk anims via templates (1 gen/direction).
- Audio: synthesized (`tools/gen_audio.py`).

---

## PROGRESS

Legend: [x] done · [~] in progress · [ ] pending

- [x] Research lore + licensing, PixelLab API
- [x] Git repo, design doc
- [x] P1 Asset generation batch 1 (19 characters, 4 quadrupeds, 10 portraits, ~170 props). Wide props use 64px Pro batches.
- [x] P2 Engine: i18n (Loc), map loader (multi-material tiles, occluders), doors, exits
- [x] P3 Engine: flashlight cone + shadows, fog shader, particles, ambient life
- [x] P4 Engine: dialogue w/ portraits+choices, events runner, quests, docs, automap (needs data)
- [~] P5 Engine: HUD meters (hp, battery, sanity, stamina), pause menu, options — blink meter pending (173)
- [x] P6 SCP behaviours: 173, 131, 999, 049, 096, 106, chaser, 939, 529, 682 (HCl special), tesla gates.
- [x] P7 Maps content: 65 maps A-G, all bot-tested (tests/routes/sector_a.json, sector_b.json, b02_contain.json, sector_cd.json, sector_efg.json).
- [x] P8 Story data EN+ES: Acts I-VI + 3 endings (tools/story/sector_a..d.py, sector_efg.py). Build: python3 tools/build_story.py
- [ ] P9 Audio expansion
- [ ] P10 Full playthrough bot + screenshots of every area; polish pass
- [ ] P10b README with good screenshots (players must find and play it)
- [ ] P11 CREDITS.md, README, final push

### Log
- 2026-09-18 ~08:00 Sectors E-G + endings committed (bcaa244); sector_efg route passes to ending. Next: regression all routes, README/CREDITS.
- 2026-09-18 05:30 Sectors C+D done; death-loop protection (respawn hp>=60), chaser grace, bot combat.
- 2026-09-18 04:40 Sector B + SCP actors + battle. Tests: tests/routes/*.json run with tools/playtest.gd (SCP_MAP, SCP_FLAGS, SCP_SAVE env). b02_contain.json validates 173 recontainment.
- 2026-09-18 00:00-01:30 research, design, git, asset pipeline, new engine core (commit 82ab3b7). Tools: tools/shot.gd (SCP_MAP=<id> in-game screenshot), tools/render_map.gd (full map PNG), tools/build_maps.py. Tests must use SCP_SAVE=user://test_save.json.
