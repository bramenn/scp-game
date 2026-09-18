class_name World
extends Node2D
## Game root: title -> maps. Owns the current MapView, the player, lights, fog, map
## entities (items, NPCs, triggers, vermin, fx, SCP actors) and the UI layers.

const TILE := 16
const VIEW := Vector2(480, 270)
const SURFACES := {
	"concrete": "concrete", "concrete_dark": "concrete", "lino": "tile", "labtile": "tile",
	"whitetile": "tile", "kitchen": "tile", "bathroom": "tile", "carpet": "soft", "metal": "metal",
	"steel": "metal", "lead": "metal", "grate": "metal", "sewer": "dirt", "soil": "dirt", "organic": "flesh",
}

var st: GameState
var view: MapView
var player: PlayerActor
var cam: Camera2D
var ambient: CanvasModulate
var fog: Fog
var dust: CPUParticles2D
var hud: Hud
var dialog: DialogueBox
var menu: PauseMenu
var events: EventRunner
var astar := AStarGrid2D.new()
var busy := 0                  # >0 while a cutscene/dialogue/menu owns the input
var npcs: Dictionary = {}      # id -> Actor
var actors: Array = []         # all non-player actors (NPCs, SCPs, enemies)
var items_at: Dictionary = {}  # Vector2i -> {data, node}
var interact_at: Dictionary = {}
var lights: Array[PointLight2D] = []
var torch_scale := 1.0         # map-wide flashlight multipliers (SCP-087 swallows light)
var torch_range := 1.0
var _fired: Dictionary = {}
var _bump_cd := 0.0
var _sanity_tick := 0.0
var _map_sounds: Array = []


func _ready() -> void:
	RenderingServer.set_default_clear_color(Color.BLACK)
	_setup_input()
	ambient = CanvasModulate.new()
	add_child(ambient)
	hud = Hud.new()
	add_child(hud)
	dialog = DialogueBox.new()
	add_child(dialog)
	events = EventRunner.new()
	events.world = self
	add_child(events)
	menu = PauseMenu.new()
	menu.world = self
	add_child(menu)
	busy += 1
	var start_map := OS.get_environment("SCP_MAP")
	if start_map != "":   # dev / test shortcut: SCP_MAP, SCP_SPAWN, SCP_FLAGS="flag,item:id,quest:id:stage"
		st = GameState.new()
		for f in OS.get_environment("SCP_FLAGS").split(",", false):
			var p := f.split(":")
			if p[0] == "item":
				st.give(p[1], int(p[2]) if p.size() > 2 else 1)
			elif p[0] == "quest":
				st.set_quest(p[1], int(p[2]))
			else:
				st.mark(f)
		_start(start_map, OS.get_environment("SCP_SPAWN") if OS.get_environment("SCP_SPAWN") != "" else "start")
		return
	var title := TitleScreen.new()
	add_child(title)
	var opt: String = await title.run(GameState.exists())
	title.queue_free()
	if opt == "quit":
		get_tree().quit()
		return
	if opt == "continue":
		st = GameState.load_saved()
		_start(st.map, "", st.tile)
	else:
		st = GameState.new()
		_start("A01", "start")


func _setup_input() -> void:
	var binds := {
		"ui_up": [KEY_W], "ui_down": [KEY_S], "ui_left": [KEY_A], "ui_right": [KEY_D],
		"interact": [KEY_E, KEY_ENTER, KEY_SPACE], "flashlight": [KEY_F], "sprint": [KEY_SHIFT],
		"menu": [KEY_ESCAPE, KEY_TAB, KEY_I], "ui_accept": [KEY_E], "ui_cancel": [KEY_Q],
	}
	for action in binds:
		if not InputMap.has_action(action):
			InputMap.add_action(action)
		for k in binds[action]:
			var ev := InputEventKey.new()
			ev.physical_keycode = k
			InputMap.action_add_event(action, ev)


func _start(map_id: String, spawn: String, at := Vector2i(-1, -1)) -> void:
	player = PlayerActor.new()
	player.st = st
	player.world = self
	player.noise.connect(_on_noise)
	player.stepped.connect(_on_player_stepped)
	cam = Camera2D.new()
	cam.position = Vector2(0, -14)
	cam.position_smoothing_enabled = true
	cam.position_smoothing_speed = 7.0
	player.add_child(cam)
	dust = _make_dust()
	cam.add_child(dust)
	hud.bind(st)
	await load_map(map_id, spawn, at, false)
	busy -= 1   # release the lock taken in _ready (events started by the map keep their own)
	await hud.fade(false, 1.2)


# ------------------------------------------------------------------- maps

func load_map(map_id: String, spawn: String, at := Vector2i(-1, -1), fade := true) -> void:
	busy += 1
	if fade:
		await hud.fade(true, 0.35)
	if view:
		for a in actors:
			if a.has_method("on_map_leave"):
				a.on_map_leave()
		st.flags.erase("pods_stay")
		if player.get_parent():
			player.get_parent().remove_child(player)
		view.queue_free()
		view = null
	for s in _map_sounds:
		s.queue_free()
	_map_sounds.clear()
	npcs.clear()
	actors.clear()
	items_at.clear()
	interact_at.clear()
	lights.clear()
	var d: Dictionary = Db.maps.get(map_id, {})
	if d.is_empty():
		push_error("missing map " + map_id)
		busy -= 1
		return
	view = MapView.new()
	add_child(view)
	move_child(view, 0)
	view.build(d)
	st.map = map_id
	_apply_env(d.get("env", {}))
	_spawn_lights(d)
	_spawn_items(d)
	_spawn_npcs(d)
	for it in d.get("interact", []):
		interact_at[Vector2i(int(it.x), int(it.y))] = it
	for sg in d.get("signs", []):
		var s := Sign.new()
		s.setup(sg)
		view.add_child(s)
	for snd in d.get("sounds", []):
		_map_sounds.append(Sfx.loop_at(view, String(snd[0]), Vector2(int(snd[1]) * TILE + 8, int(snd[2]) * TILE + 8),
			float(snd[3]), float(snd[4]) * TILE))
	for fx in d.get("fx", []):
		view.add_child(FxEmitter.make(fx))
	for v in d.get("vermin", []):
		Vermin.spawn(self, String(v[0]), Vector2i(int(v[1]), int(v[2])), int(v[3]), int(v[4]))
	for a in d.get("actors", []):
		Actors.spawn(self, a)
	_rebuild_astar()
	_refresh_doors()
	view.ents.add_child(player)
	var t := at
	if t.x < 0 or view.blocked.has(t):
		var sp: Array = d.spawns.get(spawn, d.spawns.values()[0] if d.spawns.size() > 0 else [2, 2, "south"])
		t = Vector2i(int(sp[0]), int(sp[1]))
		player.place(t, String(sp[2]))
	else:
		player.place(t, st.facing)
	player.reset_physics_interpolation()
	cam.reset_smoothing()
	var w: int = view.w * TILE
	var h: int = view.h * TILE
	var pad := (VIEW - Vector2(w, h)).max(Vector2.ZERO) * 0.5
	cam.limit_left = int(-pad.x)
	cam.limit_top = int(-pad.y)
	cam.limit_right = int(w + pad.x)
	cam.limit_bottom = int(h + pad.y)
	st.tile = t
	st.see(map_id, view.w, view.h, t)
	_spawn_followers()
	hud.location(Loc.t(d.name))
	if fade:
		await hud.fade(false, 0.45)
	st.save()
	busy -= 1
	events.on_map_enter(map_id)


func _apply_env(env: Dictionary) -> void:
	ambient.color = Color(env.get("ambient", "#343844"))
	if fog:
		fog.queue_free()
		fog = null
	var dens := float(env.get("fog", 0.0))
	if dens > 0.0:
		fog = Fog.new()
		view.add_child(fog)
		fog.setup(Vector2(view.w, view.h) * TILE, Color(env.get("fog_color", "#8a8f9a")), dens)
	dust.amount = maxi(1, int(60 * float(env.get("dust", 0.3))))
	dust.emitting = float(env.get("dust", 0.3)) > 0.0
	torch_scale = float(env.get("torch", 1.0))
	torch_range = float(env.get("torch_range", 1.0))
	Sfx.ambience(env.get("amb", ""))
	Sfx.music(env.get("music", ""))


func _make_dust() -> CPUParticles2D:
	var p := CPUParticles2D.new()
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	p.emission_rect_extents = VIEW * 0.6
	p.amount = 30
	p.lifetime = 9.0
	p.preprocess = 9.0
	p.gravity = Vector2(0, 1.5)
	p.initial_velocity_min = 0.5
	p.initial_velocity_max = 3.0
	p.direction = Vector2(1, 0.2)
	p.spread = 180.0
	p.scale_amount_min = 1.0
	p.scale_amount_max = 1.0
	p.color = Color(0.85, 0.85, 0.8, 0.5)
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 0))
	ramp.add_point(0.2, Color(1, 1, 1, 1))
	ramp.add_point(0.8, Color(1, 1, 1, 1))
	ramp.set_color(1, Color(1, 1, 1, 0))
	p.color_ramp = ramp
	p.local_coords = false
	p.z_index = 19
	return p


func _spawn_lights(d: Dictionary) -> void:
	for l in d.get("lights", []):
		var pl := PointLight2D.new()
		var kind := String(l[2])
		pl.position = Vector2(float(l[0]) * TILE + 8, float(l[1]) * TILE + 8)
		pl.texture = PlayerActor.radial_texture()
		pl.texture_scale = float(l[3])
		pl.energy = float(l[4])
		pl.shadow_enabled = true  # rooms must not bleed light through walls
		if kind == "alarm":  # rotating emergency beacon
			pl.texture = PlayerActor.cone_texture()
			pl.color = Color(1.0, 0.15, 0.1)
			var tw := pl.create_tween().set_loops()
			tw.tween_property(pl, "rotation", TAU, 1.6).from(0.0)
		else:
			pl.color = Color(kind)
		view.add_child(pl)
		lights.append(pl)
		var fl := float(l[5])
		if fl > 0.0:
			_flicker(pl, fl)
		_fixture(pl, kind)


## Small emissive fixture so light sources read as lamps on the ceiling.
func _fixture(pl: PointLight2D, kind: String) -> void:
	if kind != "alarm":   # ceiling lamps read through their light alone
		return
	var r := ColorRect.new()
	r.size = Vector2(10, 2) if kind != "alarm" else Vector2(3, 3)
	r.position = -r.size / 2.0
	r.color = pl.color.lightened(0.5)
	r.light_mask = 0
	r.z_index = 18
	r.material = CanvasItemMaterial.new()
	(r.material as CanvasItemMaterial).light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
	pl.add_child(r)
	pl.set_meta("fixture", r)


func _flicker(pl: PointLight2D, amount: float) -> void:
	var base := pl.energy
	var tw := pl.create_tween().set_loops()
	tw.tween_interval(randf_range(0.8, 4.0) / amount)
	tw.tween_callback(func() -> void:
		var f: ColorRect = (pl.get_meta("fixture") if pl.has_meta("fixture") else null)
		pl.energy = base * randf_range(0.0, 0.3)
		if f: f.visible = false)
	tw.tween_interval(randf_range(0.04, 0.12))
	tw.tween_callback(func() -> void:
		var f: ColorRect = (pl.get_meta("fixture") if pl.has_meta("fixture") else null)
		pl.energy = base
		if f: f.visible = true)
	if amount > 0.6:
		tw.tween_interval(0.05)
		tw.tween_callback(func() -> void: pl.energy = base * 0.2)
		tw.tween_interval(0.07)
		tw.tween_callback(func() -> void: pl.energy = base)


func _spawn_items(d: Dictionary) -> void:
	for it in d.get("items", []):
		if st.has(String(it.key)):
			continue
		var t := Vector2i(int(it.x), int(it.y))
		var info: Dictionary = Db.items.get(it.id, {})
		var icon := "res://art/items/%s.png" % info.get("icon", it.id)
		var s := Sprite2D.new()
		s.texture = load(icon) if ResourceLoader.exists(icon) else load("res://art/items/doc.png")
		s.position = Actor.feet(t) + Vector2(0, -6)
		view.ents.add_child(s)
		var tw := s.create_tween().set_loops()
		tw.tween_property(s, "offset:y", -2.0, 0.9).set_trans(Tween.TRANS_SINE)
		tw.tween_property(s, "offset:y", 0.0, 0.9).set_trans(Tween.TRANS_SINE)
		var glint := PointLight2D.new()
		glint.texture = PlayerActor.radial_texture()
		glint.texture_scale = 0.08
		glint.energy = 0.6
		glint.color = Color(1, 0.95, 0.7)
		s.add_child(glint)
		items_at[t] = {"data": it, "node": s}


func _spawn_npcs(d: Dictionary) -> void:
	for n in d.get("npcs", []):
		if not st.check(n.get("cond", "")):
			continue
		var info: Dictionary = Db.npcs.get(n.id, {})
		var a := NpcActor.new()
		a.world = self
		a.npc_id = n.id
		a.info = info
		a.spot = n
		view.ents.add_child(a)
		a.setup(info.get("sprite", n.id), Vector2i(int(n.x), int(n.y)), n.get("face", "south"))
		npcs[n.id] = a
		actors.append(a)


## NPCs with the flag "follow:<id>" come along to every map, appearing next to the player.
func _spawn_followers() -> void:
	if st.has("bond131") and not actors.any(func(a): return a.has_method("watches")):
		for i in 2:
			Actors.spawn(self, {"id": "scp131", "x": player.tile.x, "y": player.tile.y + 1,
				"sprite": "scp131a" if i == 0 else "scp131b", "offset": i})
	for f in st.flags:
		if not String(f).begins_with("follow:") or not st.has(f):
			continue
		var id := String(f).substr(7)
		if npcs.has(id):
			continue
		var spot := player.tile
		for d in [Vector2i.DOWN, Vector2i.UP, Vector2i.LEFT, Vector2i.RIGHT, Vector2i(1, 1), Vector2i(-1, 1), Vector2i(0, 2)]:
			var c: Vector2i = player.tile + d
			if is_free(c) and not view.door_at.has(c) and view.exit_at(c) == null:
				spot = c
				break
		var a := NpcActor.new()
		a.world = self
		a.npc_id = id
		a.info = Db.npcs.get(id, {})
		a.spot = {"mode": "idle"}
		view.ents.add_child(a)
		a.setup(a.info.get("sprite", id), spot, player.facing)
		npcs[id] = a
		actors.append(a)


# ------------------------------------------------------------ queries

func is_free(t: Vector2i, who = null) -> bool:
	if not view or view.blocked.has(t):
		return false
	if view.hatch.has(t) and who != player:
		return false
	if who == player:  # the player may walk into a friendly NPC's tile only through a swap (on_bump)
		for a in actors:
			if a.tile == t and a.get("solid") != false:
				return false
		return true
	if who != player and player and player.tile == t:
		return false
	for a in actors:
		if a != who and a.tile == t and a.get("solid") != false:
			return false
	return true


func find_path(a: Vector2i, b: Vector2i, through_hatches := false) -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	if not astar.region.has_point(a) or not astar.region.has_point(b):
		return out
	for h in view.hatch if through_hatches else {}:
		astar.set_point_solid(h, false)
	for p in astar.get_id_path(a, b, true):
		out.append(p)
	for h in view.hatch if through_hatches else {}:
		astar.set_point_solid(h, true)
	return out


func _rebuild_astar() -> void:
	astar.region = Rect2i(0, 0, view.w, view.h)
	astar.cell_size = Vector2(TILE, TILE)
	astar.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
	astar.update()
	for t in view.blocked:
		astar.set_point_solid(t, true)
	for t in view.hatch:
		astar.set_point_solid(t, true)


func surface_at(t: Vector2i) -> String:
	if view.water.has(t):
		return "water"
	return SURFACES.get(String(view.mat_of(t)[0]), "concrete")


## Light at a tile from map lamps (0..1+). Flashlight not included.
func light_at(pos: Vector2) -> float:
	var best := 0.0
	for l in lights:
		if l.energy <= 0.05:
			continue
		var r := 128.0 * l.texture_scale
		var dd := l.position.distance_to(pos)
		if dd < r:
			best = maxf(best, (1.0 - dd / r) * l.energy)
	return best


# ------------------------------------------------------------ doors

func can_open(door: Door) -> bool:
	return st.card_level() >= door.level and (door.lock_flag == "" or st.has(door.lock_flag))


func _refresh_doors() -> void:
	for dr in view.doors:
		dr.refresh_led(can_open(dr))
		if st.has("open:" + dr.id) and can_open(dr):
			view.set_door_open(dr, true)
			dr.set_open(true, true)
			_door_astar(dr, true)


func try_door(door: Door) -> void:
	if door.is_open:
		return
	if can_open(door):
		Sfx.play_at(view, "door_open", door.position, 0.0)
		view.set_door_open(door, true)
		_door_astar(door, true)
		st.mark("open:" + door.id)
		events.on_door(door.id)
	else:
		Sfx.play_at(view, "denied", door.position, -2.0)
		var msg: String = Loc.ui("door_level", [door.level]) if st.card_level() < door.level else Loc.ui("door_sealed")
		var custom: String = view.data.get("lock_msgs", {}).get(door.id, "")
		await say([custom if custom != "" else msg])


func _door_astar(door: Door, open: bool) -> void:
	for t in door.tiles():
		astar.set_point_solid(t, not open)


# ------------------------------------------------------------ player events

func _on_player_stepped(t: Vector2i) -> void:
	st.tile = t
	st.facing = player.facing
	st.see(st.map, view.w, view.h, t)
	if items_at.has(t):
		_pick_up(t)
	var e = view.exit_at(t)
	if e != null:
		if st.check(e.cond):
			Sfx.play(e.sfx, -4.0)
			load_map(e.to, e.at)
			return
		elif e.msg != "":
			say([Loc.t(e.msg)])
	var trigs: Array = view.data.get("triggers", [])
	for i in trigs.size():
		var tr: Dictionary = trigs[i]
		var r: Array = tr.rect
		if not Rect2i(int(r[0]), int(r[1]), int(r[2]), int(r[3])).has_point(t):
			continue
		var key := "trig:%s:%d" % [st.map, i]
		if tr.get("once", true) and st.has(key):
			continue
		if not st.check(tr.get("cond", "")):
			continue
		st.mark(key)
		events.run(String(tr.event))
	for a in actors:
		if a.has_method("on_player_moved"):
			a.on_player_moved(t)


func on_bump(t: Vector2i) -> void:
	if _bump_cd > 0.0 or busy > 0:
		return
	_bump_cd = 0.4
	for a in actors:  # friendly NPCs step aside: swap places like in classic RPGs
		if a is NpcActor and a.tile == t and not a.moving:
			var old: Vector2i = player.tile
			a.tile = old
			a.face(Actor.dir_name(old - t))
			a.create_tween().tween_property(a, "position", Actor.feet(old), 0.2)
			_bump_cd = 0.0
			return
	if view.door_at.has(t):
		try_door(view.door_at[t])


func _pick_up(t: Vector2i) -> void:
	var e: Dictionary = items_at[t]
	items_at.erase(t)
	e.node.queue_free()
	var it: Dictionary = e.data
	st.mark(String(it.key))
	var info: Dictionary = Db.items.get(it.id, {})
	Sfx.play("pickup", -4.0)
	if info.get("type", "") == "doc":
		if not it.id in st.docs:
			st.docs.append(it.id)
		hud.toast(Loc.ui("doc_found", [Loc.t(info.get("name", it.id))]))
		await menu.read_doc(it.id)
	else:
		st.give(it.id, int(it.get("n", 1)))
		hud.toast(Loc.ui("picked_up", [Loc.t(info.get("name", it.id))]) + ("" if int(it.get("n", 1)) == 1 else " x%d" % int(it.n)))
	_refresh_doors()
	events.on_item(String(it.id))


func _on_noise(t: Vector2i, radius: int) -> void:
	for a in actors:
		if a.has_method("hear"):
			a.hear(t, radius)


func _unhandled_input(event: InputEvent) -> void:
	if busy > 0 or not player:
		return
	if event.is_action_pressed("menu"):
		get_viewport().set_input_as_handled()
		menu.open()
		return
	if not event.is_action_pressed("interact"):
		return
	get_viewport().set_input_as_handled()
	var t := player.facing_tile()
	for tt in [t, player.tile]:
		if interact_at.has(tt) and st.check(interact_at[tt].get("cond", "")):
			events.run(String(interact_at[tt].event))
			return
	if view.door_at.has(t):
		try_door(view.door_at[t])
		return
	for a in actors:
		if a.tile == t and a.has_method("talk"):
			a.talk()
			return
	if view.solid_props.has(t):
		var p: Dictionary = view.solid_props[t]
		var txt = p.opts.get("text")
		if txt == null:
			txt = Db.story.get("props", {}).get(p.id)
		if txt != null:
			say([Loc.t(txt)])


func _process(dt: float) -> void:
	if not st or not player:
		return
	_bump_cd = maxf(0.0, _bump_cd - dt)
	if busy == 0:
		st.play_time += dt
	player.locked = busy > 0
	_update_blink(dt)
	_sanity_tick += dt
	if _sanity_tick >= 0.5 and busy == 0:
		_update_sanity(_sanity_tick)
		_sanity_tick = 0.0


func _update_sanity(dt: float) -> void:
	var lit := light_at(player.position + Vector2(0, -8))
	var torch := player.torch.energy > 0.3
	var dark := lit < 0.15 and not torch
	st.sanity = maxf(0.0, st.sanity - dt * float(view.data.get("env", {}).get("drain", 0.0)))
	if dark:
		st.sanity = maxf(0.0, st.sanity - dt * 0.8)
	elif lit > 0.35:
		st.sanity = minf(100.0, st.sanity + dt * 0.35)
	for a in actors:
		if a.has_method("dread") and a.position.distance_to(player.position) < 160.0:
			st.sanity = maxf(0.0, st.sanity - dt * float(a.dread()))
	hud.set_dread(1.0 - st.sanity / 100.0)
	if st.sanity <= 0.0:
		die("sanity")
	if st.hp <= 0.0:
		die("wounds")


# ------------------------------------------------------------ helpers for events/UI

func say(lines: Array, who := "") -> void:
	busy += 1
	await dialog.say(lines, who)
	busy -= 1


func damage(amount: float, cause := "") -> void:
	st.hp = maxf(0.0, st.hp - amount)
	hud.hurt()
	Sfx.play("hurt", -2.0)
	if st.hp <= 0.0:
		die(cause)


var _dying := false


func die(cause: String) -> void:
	if _dying:
		return
	_dying = true
	busy += 1
	st.deaths += 1
	await hud.death_screen(cause)
	var saved := GameState.load_saved() if GameState.exists() else GameState.new()
	saved.deaths = st.deaths
	st = saved
	player.st = st
	hud.bind(st)
	_dying = false
	busy -= 1
	await load_map(st.map, "", st.tile)


# ------------------------------------------------------------ interaction prompt

func _prompt_text() -> String:
	if busy > 0 or not player or not view:
		return ""
	var t := player.facing_tile()
	if view.door_at.has(t):
		var dr: Door = view.door_at[t]
		if dr.is_open:
			return ""
		return Loc.ui("p_open") if can_open(dr) else Loc.ui("p_locked", [dr.level]) if dr.level > st.card_level() else Loc.ui("p_sealed")
	for a in actors:
		if a.tile == t and a.has_method("talk"):
			return Loc.ui("p_talk", [Loc.t(Db.npcs.get(a.get("npc_id"), {}).get("name", ""))]) if a.get("npc_id") else Loc.ui("p_examine")
	for tt in [t, player.tile]:
		if interact_at.has(tt) and st.check(interact_at[tt].get("cond", "")):
			var it: Dictionary = interact_at[tt]
			return Loc.t(it.get("prompt", {"en": "[E] Examine", "es": "[E] Examinar"}))
	if view.solid_props.has(t):
		var p: Dictionary = view.solid_props[t]
		if p.opts.has("text") or Db.story.get("props", {}).has(p.id):
			return Loc.ui("p_examine")
	return ""


func _physics_process(_dt: float) -> void:
	if hud:
		hud.prompt(_prompt_text())


# ------------------------------------------------------------ special logic hooks

## Named hooks callable from events ({"call": name, "args": [...]}). SCP set pieces add
## their own cases here.
func special(name: String, args: Array) -> void:
	match name:
		"heal_full":
			st.hp = GameState.MAX_HP
			st.sanity = maxf(st.sanity, 80.0)
		"refresh_doors":
			_refresh_doors()
		_:
			for a in actors:
				if a.has_method("special") and await a.special(name, args):
					return
			push_warning("unknown special " + name)


## Turn-based encounter. Returns "win" | "lose" | "flee".
func battle(enemy_id: String) -> String:
	busy += 1
	var b := Battle.new()
	add_child(b)
	var res: String = await b.run(enemy_id, st)
	b.queue_free()
	busy -= 1
	hud.refresh()
	if res == "lose":
		die("wounds")
	return res


func ending(id: String) -> void:
	busy += 1
	await hud.fade(true, 2.0)
	var e := EndingScreen.new()
	add_child(e)
	await e.run(id, st)
	st.mark("ending_" + id)
	st.save()
	get_tree().reload_current_scene()


# ------------------------------------------------------------ sight & blinking

## Grid line of sight (Bresenham). Walls and closed doors block it.
func los(a: Vector2i, b: Vector2i) -> bool:
	var x0 := a.x
	var y0 := a.y
	var dx := absi(b.x - a.x)
	var dy := -absi(b.y - a.y)
	var sx := 1 if a.x < b.x else -1
	var sy := 1 if a.y < b.y else -1
	var err := dx + dy
	while not (x0 == b.x and y0 == b.y):
		var e2 := 2 * err
		if e2 >= dy:
			err += dy
			x0 += sx
		if e2 <= dx:
			err += dx
			y0 += sy
		var t := Vector2i(x0, y0)
		if t == b:
			break
		if view.is_wall(t) or (view.door_at.has(t) and not view.door_at[t].is_open):
			return false
	return true


## True if the player can see tile t right now: eyes open, in front (180°), line of sight,
## and it is lit (map light or the flashlight cone).
func player_sees(t: Vector2i) -> bool:
	if blinking or not player:
		return false
	var d := t - player.tile
	if d == Vector2i.ZERO:
		return true
	var fwd: Vector2i = Actor.DIRS[player.facing]
	if d.x * fwd.x + d.y * fwd.y < 0:
		return false
	if d.length() > 14.0 or not los(player.tile, t):
		return false
	var pos := Actor.feet(t) + Vector2(0, -10)
	if light_at(pos) > 0.12:
		return true
	if player.torch.energy > 0.3:
		var to := pos - (player.position + player.torch.position)
		return to.length() < 175.0 * player.torch.texture_scale and \
			absf(angle_difference(player.torch.rotation, to.angle())) < deg_to_rad(PlayerActor.CONE_DEG + 4.0)
	return d.length() <= 2.0   # right next to you, even in the dark


var blinking := false
var _blink_t := 7.0


## Called by World._process: blink only matters when something that moves unseen is near.
func _update_blink(dt: float) -> void:
	var need := false
	for a in actors:
		if a.has_method("wants_blink") and a.wants_blink():
			need = true
			break
	hud.set_blink(_blink_t / 7.0 if need else -1.0)
	if not need or busy > 0:
		_blink_t = 7.0
		return
	_blink_t -= dt
	if _blink_t <= 0.0 and not blinking:
		_blink_t = randf_range(6.0, 8.0)
		blinking = true
		await hud.blink()
		blinking = false
