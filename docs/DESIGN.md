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
3. **A place that feels real and big.** 9 maps, dozens of named rooms, every room has
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
- **Prologue — Gate B (surface).** Night, rain, fog. Truck drops Vega. Dead guards,
  searchlights, rats. Elevator down. Tutorial (move, light, interact).
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

## 3. Maps (zones)

| id | Name | Size | Key places |
|----|------|------|------------|
| `surface` | Gate B (surface) | 60×44 | truck, guard booth, fence, searchlights, elevator house, rain |
| `ez` | Entrance Zone | 96×64 | lobby, security checkpoint, offices (Elena's), cafeteria, break room + SCP-294, server room (079 terminal), staff dorms, infirmary, Gate A (sealed), LCZ checkpoint |
| `lcz` | Light Containment | 104×72 | 173 chamber, 914 lab, 012 room, 131 den, 999 cell, 500 vault, D-class block, toilets, armory, labs, vents |
| `maint` | Maintenance & Sewers | 88×60 | water channels, substation (3 breakers), Tomás' den, pump room, 087 door, rat nests |
| `med` | Medical Wing | 84×60 | morgue, operating theatre, 049 cell, pharmacy (Lin), cold storage, greenhouse (lavender), wards |
| `hcz` | Heavy Containment | 112×84 | 939 dark sector, 096 chamber, 106 chamber + femur breaker, 682 acid chamber, tesla gates, NTF last stand, armory L4 |
| `pocket` | Pocket Dimension | 52×52 | trench, rotting corridors, pillars, the throne, exits |
| `stair087` | SCP-087 | procedural | the stairwell |
| `core` | 079 Core & Gate A | 64×56 | core chamber, warhead control, Gate A helipad |

Zones are authored in `tools/build_zones.py` (Python DSL → `data/zones/*.json`).

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
- [ ] P1 Asset generation batch 1 (characters, SCPs, vermin, portraits, props)
- [ ] P2 Engine: i18n (Loc), zone loader (multi-theme tiles, occluders), doors, exits
- [ ] P3 Engine: flashlight cone + shadows, fog shader, particles, ambient life
- [ ] P4 Engine: dialogue w/ portraits+choices, events runner, quests, docs, automap
- [ ] P5 Engine: HUD meters (hp, battery, sanity, stamina, blink), pause menu, options
- [ ] P6 SCP behaviours: 173, 131, 096, 106 (+pocket), 049 (+049-2), 939, 682, 999, 529
- [ ] P7 Zones content: surface, ez, lcz, maint, med, hcz, pocket, stair087, core
- [ ] P8 Story data EN+ES: dialogues, docs, quests, events, endings
- [ ] P9 Audio expansion
- [ ] P10 Full playthrough bot + screenshots of every area; polish pass
- [ ] P11 CREDITS.md, README, final push

### Log
- (append one line per work session here)
