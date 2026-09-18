extends Node2D
## Mundo (núcleo): título -> partida sobre GameState. NPCs con historia, objetos,
## puertas por nivel de tarjeta, combate, guardado, audio y final. Datos: ScpCatalog.

const TILE := 16
const VIEW := Vector2(480, 270)
const WALLS := "# W"          # + dígitos/H son puertas: pared visible, transitable si hay tarjeta
const PROPS := {"c": "crate", "b": "barrel", "m": "gurney", "k": "desk", "o": "console", "l": "locker"}
const DECALS := {"x": 0, "r": 1, "p": 2, "w": 3, "y": 4}
const PROP_TEXT := {
	"crate": "Cajas de suministros. Etiqueta: 'NO ABRIR SIN AUTORIZACIÓN NIVEL 3'.",
	"barrel": "Un bidón sellado. Huele a químicos.",
	"gurney": "Una camilla. Las correas están rotas.",
	"desk": "Informes clasificados. Casi todo está tachado en negro.",
	"console": "Terminal de contención. Estado de celdas: ALERTA.",
	"locker": "Casillero del personal. Dentro hay un uniforme ensangrentado.",
}
## Luz ambiente y color de lámparas por tema (la paleta del tileset hace el resto).
const MOOD := {
	"facility": [Color(0.42, 0.44, 0.52), Color(1.0, 0.92, 0.75)],
	"cold": [Color(0.28, 0.34, 0.46), Color(0.7, 0.85, 1.0)],
	"padded": [Color(0.22, 0.2, 0.22), Color(1.0, 0.85, 0.7)],
	"corroded": [Color(0.2, 0.15, 0.14), Color(1.0, 0.55, 0.3)],
	"medical": [Color(0.4, 0.46, 0.46), Color(0.8, 1.0, 0.95)],
	"biohazard": [Color(0.18, 0.22, 0.16), Color(0.7, 1.0, 0.4)],
}
const FLICKER := ["corroded", "cold", "biohazard"]

var db: ScpCatalog
var st: GameState
var player: Player
var cam: Camera2D
var hud: Hud
var ents: Node2D
var layers: Array[TileMapLayer] = []
var lights: Node2D
var ambient: CanvasModulate

var map_id := ""
var map: Dictionary = {}
var grid: Array = []
var blocked: Dictionary = {}
var exits: Dictionary = {}        # Vector2i -> {"to": id, "nivel"?: int}
var door_level: Dictionary = {}   # Vector2i -> nivel de tarjeta requerido
var items_at: Dictionary = {}     # Vector2i -> [id, bandera, sprite]
var npcs_at: Dictionary = {}      # Vector2i -> id de NPC en story.json
var scp_tile := Vector2i(-1, -1)
var scp_sprite: Sprite2D
var props_at: Dictionary = {}     # Vector2i -> id de prop
var grace_until: Dictionary = {}  # tras huir, unos segundos para salir de la celda
var entered_at := 0.0
var busy := false
var listo := false  # _ready terminó: título elegido, fundido abierto
var _tilesets: Dictionary = {}
var _light_tex: GradientTexture2D


func _ready() -> void:
	RenderingServer.set_default_clear_color(Color.BLACK)
	for pair in [["ui_up", KEY_W], ["ui_down", KEY_S], ["ui_left", KEY_A], ["ui_right", KEY_D], ["ui_accept", KEY_E]]:
		var ev := InputEventKey.new()
		ev.physical_keycode = pair[1]
		InputMap.action_add_event(pair[0], ev)

	db = ScpDb
	db.load_all()
	_light_tex = GradientTexture2D.new()
	_light_tex.fill = GradientTexture2D.FILL_RADIAL
	_light_tex.fill_from = Vector2(0.5, 0.5)
	_light_tex.fill_to = Vector2(1.0, 0.5)
	_light_tex.width = 128
	_light_tex.height = 128
	_light_tex.gradient = Gradient.new()
	_light_tex.gradient.set_color(0, Color.WHITE)
	_light_tex.gradient.set_color(1, Color(1, 1, 1, 0))

	for i in 4:  # piso, calcos/sombras, muros
		var l := TileMapLayer.new()
		add_child(l)
		layers.append(l)
	ents = Node2D.new()
	ents.y_sort_enabled = true
	add_child(ents)
	lights = Node2D.new()
	add_child(lights)
	ambient = CanvasModulate.new()
	add_child(ambient)

	player = Player.new()
	ents.add_child(player)
	player.arrived.connect(_on_player_arrived)
	player.bumped.connect(_on_player_bumped)
	var torch := PointLight2D.new()
	torch.texture = _light_tex
	torch.texture_scale = 1.6
	torch.energy = 0.9
	torch.position = Vector2(0, -12)
	player.add_child(torch)
	cam = Camera2D.new()
	cam.position = Vector2(0, -12)
	player.add_child(cam)
	cam.make_current()

	hud = Hud.new()
	add_child(hud)

	busy = true  # el mundo no responde hasta elegir en el título
	player.locked = true
	var fresh := false
	if OS.get_environment("SCP_SKIP_TITLE") == "1":
		fresh = true
		st = GameState.new()
	else:
		var title := Title.new()
		add_child(title)
		var opt: String = await title.show_menu(GameState.exists())
		if opt == "salir":
			get_tree().quit()
			return
		fresh = opt == "nueva"
		st = GameState.load_saved() if not fresh else GameState.new()
		title.queue_free()

	hud.set_hp(st.hp, GameState.BASE.hp)
	_enter_map(st.map, "", st.tile)
	await hud.fade(false, 0.8)  # abre el fundido inicial: arranca negro
	if fresh and OS.get_environment("SCP_SKIP_TITLE") != "1":
		_system(db.story.intro)
	_refresh_goal()
	player.locked = false
	busy = false
	listo = true


# ---------------------------------------------------------------- mapas

func _enter_map(id: String, from: String, saved := Vector2i(-1, -1)) -> void:
	map_id = id
	map = db.get_map(id)
	grid = map.rows
	_build_tiles()
	_build_entities()
	_apply_doors()
	_build_lights()
	var mood: Array = MOOD.get(map.theme, MOOD.facility)
	ambient.color = mood[0]
	Sfx.ambience(map.theme)
	Sfx.music("")

	var spawn := _find("P")
	var face := "south"
	if saved.x >= 0 and _walkable(saved):
		spawn = saved
	else:
		for t in exits:
			if exits[t].get("to") == from:  # volver por la misma puerta, un paso hacia dentro
				for d in Player.DIRS:
					var n: Vector2i = t + Player.DIRS[d]
					if _walkable(n):
						spawn = n
						face = d
	player.place(spawn, face)
	player.blocked = blocked

	var w: int = grid[0].length() * TILE
	var h: int = grid.size() * TILE
	var pad := (VIEW - Vector2(w, h)).max(Vector2.ZERO) * 0.5  # centra mapas chicos
	cam.limit_left = int(-pad.x)
	cam.limit_top = int(-pad.y)
	cam.limit_right = int(w + pad.x)
	cam.limit_bottom = int(h + pad.y)
	cam.reset_smoothing()

	entered_at = Time.get_ticks_msec() / 1000.0
	if id == "hub":
		st.hp = GameState.BASE.hp  # la enfermería del sitio te atiende
	st.map = id
	st.tile = spawn
	st.save()
	hud.set_hp(st.hp, GameState.BASE.hp)
	_refresh_goal()

	var scp = db.get_scp(map.get("scp"))
	if scp == null:
		hud.show_banner(map.nombre, "Zona segura")
	elif st.contained(scp.id):
		hud.show_banner(map.nombre, "%s · CONTENIDO" % scp.nombre, Color("6f94ad"))
	else:
		hud.show_banner(map.nombre, "%s · ACTIVO" % scp.nombre, Color("c9302c"))


func _ch(t: Vector2i) -> String:
	if t.y < 0 or t.y >= grid.size() or t.x < 0 or t.x >= grid[t.y].length():
		return "#"
	return grid[t.y][t.x]


func _is_wall(t: Vector2i) -> bool:
	var c := _ch(t)
	return c in WALLS or c.is_valid_int()


func _walkable(t: Vector2i) -> bool:
	return not blocked.has(t) and not exits.has(t)


func _find(c: String) -> Vector2i:
	for y in grid.size():
		var x: int = grid[y].find(c)
		if x >= 0:
			return Vector2i(x, y)
	return Vector2i(1, 2)


func _tileset(theme: String) -> TileSet:
	if not _tilesets.has(theme):
		var ts := TileSet.new()
		ts.tile_size = Vector2i(TILE, TILE)
		var src := TileSetAtlasSource.new()
		src.texture = load("res://art/tiles/atlas/%s.png" % theme)
		src.texture_region_size = Vector2i(TILE, TILE)
		for y in 4:
			for x in 16:
				src.create_tile(Vector2i(x, y))
		ts.add_source(src, 0)
		_tilesets[theme] = ts
	return _tilesets[theme]


func _build_tiles() -> void:
	var ts := _tileset(map.theme)
	for l in layers:
		l.clear()
		l.tile_set = ts
	blocked.clear()
	exits.clear()
	door_level.clear()
	var floor_l := layers[0]
	var decal_l := layers[1]
	var shade_l := layers[2]
	var wall_l := layers[3]
	for y in grid.size():
		for x in grid[y].length():
			var t := Vector2i(x, y)
			var c: String = grid[y][x]
			var hsh := absi(hash(t)) % 100
			if map.exits.has(c):
				exits[t] = map.exits[c]
				if map.exits[c].has("nivel"):
					door_level[t] = int(map.exits[c].nivel)
			if c == "H":
				floor_l.set_cell(t, 0, Vector2i(8, 0))
				continue
			if _is_wall(t):
				if not c.is_valid_int():
					blocked[t] = true
				wall_l.set_cell(t, 0, _wall_tile(t, c, hsh))
				continue
			var f := Vector2i(hsh % 3 if hsh < 70 else 3 + hsh % 3, 0)
			if c == "g":
				f = Vector2i(6, 0)
			elif c == ",":
				f = Vector2i(7, 0)
			floor_l.set_cell(t, 0, f)
			if DECALS.has(c):
				decal_l.set_cell(t, 0, Vector2i(DECALS[c], 3))
			if _is_wall(t + Vector2i.UP):
				shade_l.set_cell(t, 0, Vector2i(5, 3))
			elif _is_wall(t + Vector2i.LEFT):
				shade_l.set_cell(t, 0, Vector2i(6, 3))


func _wall_tile(t: Vector2i, c: String, hsh: int) -> Vector2i:
	var below := t + Vector2i.DOWN
	if not _is_wall(below) and _ch(below) != "H":
		if c == "W":
			return Vector2i(6, 1)
		if c.is_valid_int():
			return Vector2i(5, 1)
		return Vector2i([0, 0, 0, 1, 2, 3, 4, 7][hsh % 8], 1)
	if _is_wall(below) and not _is_wall(below + Vector2i.DOWN) and _ch(below + Vector2i.DOWN) != "H":
		return Vector2i(8, 1)  # mitad alta de un muro de 2 tiles
	var mask := 0
	for i in 4:
		var n: Vector2i = t + [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT][i]
		if _ch(n) != " " and not _is_wall(n) and n.y >= 0 and n.y < grid.size():
			mask |= 1 << i
	return Vector2i(mask, 2)


func _build_entities() -> void:
	for c in ents.get_children():
		if c != player:
			c.queue_free()
	props_at.clear()
	items_at.clear()
	npcs_at.clear()
	scp_tile = Vector2i(-1, -1)
	scp_sprite = null
	for y in grid.size():
		for x in grid[y].length():
			var c: String = grid[y][x]
			var t := Vector2i(x, y)
			if PROPS.has(c):
				var s := Sprite2D.new()
				s.texture = load("res://art/props/%s.png" % PROPS[c])
				s.offset = Vector2(0, -15)
				s.position = Vector2((x + 1) * TILE, (y + 1) * TILE)  # huella de 2 tiles
				ents.add_child(s)
				for dx in 2:
					blocked[t + Vector2i(dx, 0)] = true
					props_at[t + Vector2i(dx, 0)] = PROPS[c]
			elif c == "S":
				_spawn_scp(t)
			elif map.npcs.has(c):
				_spawn_npc(t, map.npcs[c])
			elif map.items.has(c):
				_spawn_item(t, c, map.items[c])


func _spawn_scp(t: Vector2i) -> void:
	var scp = db.get_scp(map.get("scp"))
	if scp == null:
		return
	scp_tile = t
	var wide := 1 if scp.id == "scp-682" else 0
	for dx in range(-wide, wide + 1):
		blocked[t + Vector2i(dx, 0)] = true
	var s := Sprite2D.new()
	s.texture = load(scp.sprite)
	s.offset = Vector2(0, -21)
	s.position = Player.feet(t)
	ents.add_child(s)
	scp_sprite = s
	if scp.id != "scp-173":  # la escultura no se mueve mientras la miras
		var tw := s.create_tween().set_loops()
		tw.tween_property(s, "scale", Vector2(1.0, 1.04), 0.9).set_trans(Tween.TRANS_SINE)
		tw.tween_property(s, "scale", Vector2(1.0, 1.0), 0.9).set_trans(Tween.TRANS_SINE)
	_refresh_scp_look()


func _spawn_npc(t: Vector2i, id: String) -> void:
	var npc: Dictionary = db.story.get("npcs", {}).get(id, {})
	if npc.is_empty():
		return
	npcs_at[t] = id
	blocked[t] = true
	var s := Sprite2D.new()
	s.texture = load(npc.sprite)
	s.offset = Vector2(0, -15)
	s.position = Player.feet(t)
	ents.add_child(s)


func _spawn_item(t: Vector2i, c: String, id: String) -> void:
	var flag := "tomado:%s:%s" % [map_id, c]
	if st.has(flag):
		return
	var path := "res://art/items/%s.png" % ("doc" if id.begins_with("doc_") else id)
	if not ResourceLoader.exists(path):
		return
	var s := Sprite2D.new()
	s.texture = load(path)
	s.position = Player.feet(t) + Vector2(0, -12)
	ents.add_child(s)
	var tw := s.create_tween().set_loops()
	tw.tween_property(s, "position:y", s.position.y - 3.0, 0.8).set_trans(Tween.TRANS_SINE)
	tw.tween_property(s, "position:y", s.position.y, 0.8).set_trans(Tween.TRANS_SINE)
	items_at[t] = [id, flag, s]


func _refresh_scp_look() -> void:
	if scp_sprite:
		var scp = db.get_scp(map.get("scp"))
		var done: bool = scp != null and st.contained(scp.id)
		scp_sprite.modulate = Color(0.55, 0.75, 1.0, 0.75) if done else Color.WHITE


func _build_lights() -> void:
	for c in lights.get_children():
		c.queue_free()
	var mood: Array = MOOD.get(map.theme, MOOD.facility)
	for y in grid.size():
		var x: int = grid[y].find("L")
		while x >= 0:
			var l := PointLight2D.new()
			l.texture = _light_tex
			l.texture_scale = 1.4
			l.color = mood[1]
			l.energy = 1.1
			l.position = Vector2(x * TILE + 8, y * TILE + 8)
			lights.add_child(l)
			if map.theme in FLICKER and (x + y) % 2 == 0:
				_flicker(l)
			x = grid[y].find("L", x + 1)
	if scp_tile.x >= 0:  # halo rojo sobre el SCP activo
		var a := PointLight2D.new()
		a.texture = _light_tex
		a.texture_scale = 0.7
		a.color = Color(1.0, 0.25, 0.2)
		a.energy = 0.9
		a.position = Player.feet(scp_tile) + Vector2(0, -16)
		a.name = "ScpGlow"
		lights.add_child(a)


func _flicker(l: PointLight2D) -> void:
	var tw := l.create_tween().set_loops()
	tw.tween_interval(randf_range(1.5, 4.0))
	tw.tween_property(l, "energy", 0.1, 0.05)
	tw.tween_property(l, "energy", 1.1, 0.05)
	tw.tween_property(l, "energy", 0.2, 0.08)
	tw.tween_property(l, "energy", 1.1, 0.1)


# -------------------------------------------------------------- juego

func _refresh_goal() -> void:
	var nxt: String = st.next_target(db.ORDER)
	hud.set_goal("Contener %s" % db.get_scp(nxt).nombre.split(" · ")[0] if nxt != "" else "SITIO-19 ASEGURADO")


func _apply_doors() -> void:
	for t in door_level:
		if door_level[t] > st.card_level():
			blocked[t] = true
		else:
			blocked.erase(t)


func _on_player_arrived(t: Vector2i) -> void:
	if items_at.has(t):
		_pick_up(t)
	if exits.has(t):
		_go(exits[t].get("to", "hub"))
	elif db.get_scp(map.get("scp")) != null:
		_try_trigger({"tipo": "entrar_celda"})


func _on_player_bumped(t: Vector2i) -> void:
	if busy or not door_level.has(t) or door_level[t] <= st.card_level():
		return
	Sfx.play("locked")
	_system(["La puerta necesita una tarjeta de nivel %d." % door_level[t]])


func _pick_up(t: Vector2i) -> void:
	var e: Array = items_at[t]
	items_at.erase(t)
	e[2].queue_free()
	st.give(e[0])
	st.mark(e[1])
	Sfx.play("pickup")
	_system(["Obtienes %s." % db.items[e[0]].nombre])


func _go(to: String) -> void:
	busy = true
	player.locked = true
	Sfx.play("door")
	await hud.fade(true)
	_enter_map(to, map_id)
	await hud.fade(false)
	player.locked = false
	busy = false


func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.is_pressed() and not event.is_echo() and event.physical_keycode in [KEY_I, KEY_TAB]:
		if busy:
			return
		get_viewport().set_input_as_handled()
		_open_inventory()
		return
	if busy or not event.is_action_pressed("ui_accept"):
		return
	var t := player.facing_tile()
	if npcs_at.has(t):
		_npc_talk(npcs_at[t])
		return
	var scp = db.get_scp(map.get("scp"))
	if scp != null and absi(t.x - scp_tile.x) <= (1 if scp.id == "scp-682" else 0) and t.y == scp_tile.y:
		if st.contained(scp.id):
			_system(["%s está contenido en su celda." % scp.nombre])
		elif not _try_trigger({"tipo": "interactuar"}):
			_system([scp.get("ambiente", "...")])
	elif props_at.has(t):
		_system([PROP_TEXT.get(props_at[t], "...")])


func _open_inventory() -> void:
	busy = true
	player.locked = true
	var inv := Inventory.new()
	add_child(inv)
	inv.open(st, db.items)
	await inv.closed
	inv.queue_free()
	hud.set_hp(st.hp, GameState.BASE.hp)
	st.tile = player.tile
	st.save()
	player.locked = false
	busy = false


func _npc_talk(id: String) -> void:
	var npc: Dictionary = db.story.get("npcs", {}).get(id, {})
	var d: Dictionary = st.pick_dialog(npc.get("dialogos", []))
	if d.is_empty():
		return
	busy = true
	player.locked = true
	await hud.say(d.lineas, npc.nombre)
	var da: Array = d.get("da", [])
	if not da.is_empty():
		var nombres := []
		for item_id in da:
			st.give(item_id)
			nombres.append(db.items[item_id].nombre)
		Sfx.play("pickup")
		await hud.say(["Recibes %s." % ", ".join(nombres)])
	if d.has("marca"):
		st.mark(d.marca)
	_apply_doors()  # puede haber entregado una tarjeta
	_refresh_goal()
	st.tile = player.tile
	st.save()
	player.locked = false
	busy = false


func _system(lines: Array) -> void:
	busy = true
	player.locked = true
	await hud.say(lines)
	player.locked = false
	busy = false


func _try_trigger(evento: Dictionary) -> bool:
	if busy:
		return false
	var scp = db.get_scp(map.get("scp"))
	if scp == null or st.contained(scp.id):
		return false
	if float(grace_until.get(map_id, 0.0)) > Time.get_unix_time_from_system():
		return false
	var ctx := {
		"items": st.inv.keys(),
		"tiempo_en_celda": Time.get_ticks_msec() / 1000.0 - entered_at,
	}
	if not ScpTrigger.fires(scp, evento, ctx):
		return false
	_encounter(scp)
	return true


func _encounter(scp: Dictionary) -> void:
	busy = true
	player.locked = true
	var bang := Label.new()
	bang.text = "!"
	bang.add_theme_font_override("font", Hud.title_font())
	bang.add_theme_font_size_override("font_size", 16)
	bang.add_theme_color_override("font_color", Color("c9302c"))
	bang.position = Vector2(-3, -58)
	player.add_child(bang)
	await get_tree().create_timer(0.7).timeout
	bang.queue_free()
	await hud.flash(3)
	await hud.fade(true, 0.25)

	var battle := Battle.new()
	add_child(battle)
	var mood: Array = MOOD.get(map.theme, MOOD.facility)
	var result: String = await battle.run(scp, st, db.items, mood[1].darkened(0.55))
	await hud.fade(true, 0.01)
	battle.queue_free()
	Sfx.music("")
	Sfx.ambience(map.theme)

	match result:
		"win":
			st.mark("contenido:" + scp.id)
			if scp.has("recompensa"):
				st.give(scp.recompensa)
			st.save()
			_refresh_scp_look()
			_build_lights()
			_refresh_goal()
		"lose":
			_enter_map("hub", "")  # Ortega te arrastra a la enfermería
		"flee":
			grace_until[map_id] = Time.get_unix_time_from_system() + 8.0
	await hud.fade(false, 0.4)
	if result == "win":
		if scp.id == db.ORDER.back():
			await _ending()
		else:
			_system(["Contención restablecida. Sube de nivel de acceso."])
	player.locked = false
	busy = false


func _ending() -> void:
	Sfx.music("ending")
	await hud.say(db.story.final)
	st.mark("final")
	st.save()
	await hud.say(["FIN. Puedes seguir explorando el sitio."])
	Sfx.music("")
	Sfx.ambience(map.theme)
