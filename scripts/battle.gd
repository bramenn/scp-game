class_name Battle
extends CanvasLayer
## Combate por turnos estilo FireRed: agente vs SCP.
## Ganar = contener (el protocolo tiene más éxito cuanto más débil esté el SCP).

const W := 480
const H := 270
const OPTIONS := ["DISPARAR", "CONTENER", "OBJETO", "HUIR"]
const WEAK_DMG := 0.6      # daño que hace un SCP si tienes su debilidad
const WEAK_CONTAIN := 0.3  # bono a contener con la debilidad

signal _picked(i: int)
signal _advance

var _scp: Dictionary
var _scp_hp: int
var _scp_max: int
var _st: GameState
var _items: Dictionary
var _weak := false
var _atk: int
var _def: int
var _spd: int
var _cursor := 0
var _menu_open := false
var _list: Array = []      # submenú de objetos: ids
var _waiting := false

var _root: Control
var _bg_color: Color
var _scp_sprite: TextureRect
var _ply_sprite: TextureRect
var _scp_bar: ProgressBar
var _ply_bar: ProgressBar
var _ply_hp_label: Label
var _text: Label
var _menu: PanelContainer
var _grid: GridContainer
var _opt_labels: Array[Label] = []


static func damage(power: int, atk: int, def: int) -> int:
	return maxi(1, int(round(power * atk / float(def + 12))))


static func contain_chance(cur_hp: int, max_hp: int, weak := false) -> float:
	return clampf(1.0 - float(cur_hp) / max_hp + 0.1 + (WEAK_CONTAIN if weak else 0.0), 0.05, 0.95)


## Corre el combate completo sobre el estado de la partida. Devuelve "win" | "lose" | "flee".
func run(scp: Dictionary, st: GameState, items: Dictionary, bg: Color) -> String:
	_scp = scp
	_st = st
	_items = items
	_scp_max = int(scp.stats.hp)
	_scp_hp = _scp_max
	_atk = st.stat("atk", items)
	_def = st.stat("def", items)
	_spd = st.stat("spd", items)
	_weak = st.has("tiene:" + String(scp.get("debilidad", "-")))
	_bg_color = bg
	_build()
	Sfx.music("battle")
	await _intro()
	await _say("¡%s se ha liberado!" % _scp.nombre)
	if _weak:
		await _say(scp.texto_debilidad)
	var result := ""
	while result == "":
		var pick := await _choose()
		var used := ""
		if pick == 2:
			used = await _choose_item()
			if used == "":
				continue
		var scp_first := int(_scp.stats.spd) > _spd and pick != 2
		if scp_first:
			await _scp_turn()
			if _st.hp <= 0:
				result = "lose"
				break
		result = await _player_turn(pick, used)
		if result != "" or scp_first:
			continue
		await _scp_turn()
		if _st.hp <= 0:
			result = "lose"
	if result == "lose":
		Sfx.play("defeat")
		await _say("Todo se vuelve negro... El Sgto. Ortega te arrastra de vuelta a la Zona de Entrada.")
	await get_tree().create_timer(0.3).timeout
	return result


func _player_turn(pick: int, used: String) -> String:
	match pick:
		0:
			await _say("Disparas contra %s." % _short())
			Sfx.play("shoot")
			await _flash_screen()
			var d := damage(20 + randi_range(-3, 3), _atk, int(_scp.stats.def))
			_scp_hp = maxi(0, _scp_hp - d)
			await _hit(_scp_sprite, _scp_bar, _scp_hp)
			if _scp_hp <= 0:
				await _say("%s queda inmovilizado. Aplicas el protocolo." % _short())
				await _contained()
				return "win"
			await _say("Le causas %d de daño." % d)
		1:
			await _say("Inicias el protocolo de contención...")
			if randf() < contain_chance(_scp_hp, _scp_max, _weak):
				await _contained()
				return "win"
			Sfx.play("fail")
			await _shake(_scp_sprite)
			await _say("¡El protocolo falló! %s se resiste." % _short())
		2:
			var it: Dictionary = _items[used]
			_st.take(used)
			_st.hp = mini(GameState.BASE.hp, _st.hp + int(it.cura))
			Sfx.play("heal")
			await _tween_bar(_ply_bar, _st.hp)
			await _say("Usas %s. Recuperas vida." % it.nombre)
		3:
			var p := 0.65 if _spd >= int(_scp.stats.spd) else 0.35
			if randf() < p:
				await _say("Escapas por los pelos.")
				return "flee"
			Sfx.play("fail")
			await _say("¡No puedes escapar!")
	return ""


func _scp_turn() -> void:
	var mv: Dictionary = _scp.movimientos.pick_random()
	await _say("%s usa %s." % [_short(), mv.nombre])
	if mv.get("efecto") == "cura":
		var heal := int(mv.poder) / (2 if _weak else 1)
		_scp_hp = mini(_scp_max, _scp_hp + heal)
		Sfx.play("heal", 0.0, 0.6)
		await _tween_bar(_scp_bar, _scp_hp)
		await _say("%s se regenera." % _short() + (" El ácido lo frena." if _weak else ""))
		return
	Sfx.play("scp", 0.0, randf_range(0.9, 1.1))
	await _lunge(_scp_sprite, Vector2(-14, 8))
	var d := damage(int(mv.poder) + randi_range(-3, 3), int(_scp.stats.atk), _def)
	if _weak:
		d = maxi(1, int(d * WEAK_DMG))
	_st.hp = maxi(0, _st.hp - d)
	Sfx.play("hit")
	await _hit(_ply_sprite, _ply_bar, _st.hp)


func _short() -> String:
	return String(_scp.nombre).split(" · ")[0]


# ---------------------------------------------------------------- UI

func _build() -> void:
	layer = 10
	_root = Control.new()
	_root.theme = Hud.make_theme()
	_root.size = Vector2(W, H)
	add_child(_root)
	_root.draw.connect(_draw_bg)

	_scp_sprite = _sprite(load(_scp.sprite), Vector2(320, 26), 2)
	_ply_sprite = _sprite(load("res://art/player/north.png"), Vector2(36, 70), 3)  # más cerca de cámara

	var box := _info_box(Vector2(16, 18), _scp.nombre, "Clase %s" % _scp.get("clase", "?"))
	_scp_bar = box[0]
	_scp_bar.max_value = _scp_max
	_scp_bar.value = _scp_hp
	box = _info_box(Vector2(W - 196, 132), "AGENTE", "")
	_ply_bar = box[0]
	_ply_hp_label = box[1]
	var mx: int = GameState.BASE.hp
	_ply_bar.max_value = mx
	_ply_bar.value = _st.hp
	_ply_bar.value_changed.connect(func(v: float) -> void: _ply_hp_label.text = "Vida %d/%d" % [int(v), mx])
	_ply_hp_label.text = "Vida %d/%d  ATQ %d  DEF %d" % [_st.hp, mx, _atk, _def]

	var tb := PanelContainer.new()
	tb.add_theme_stylebox_override("panel", Hud.panel_style(Color("d0d2d6")))
	tb.position = Vector2(6, H - 62)
	tb.custom_minimum_size = Vector2(W - 12, 56)
	_text = Label.new()
	_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_text.custom_minimum_size = Vector2(250, 0)
	tb.add_child(_text)
	_root.add_child(tb)

	_menu = PanelContainer.new()
	_menu.add_theme_stylebox_override("panel", Hud.panel_style(Color("e8c440")))
	_menu.position = Vector2(W - 196, H - 62)
	_menu.custom_minimum_size = Vector2(190, 56)
	_grid = GridContainer.new()
	_grid.columns = 2
	_grid.add_theme_constant_override("h_separation", 16)
	_grid.add_theme_constant_override("v_separation", 6)
	for o in OPTIONS:
		var l := Label.new()
		l.custom_minimum_size = Vector2(80, 0)
		_grid.add_child(l)
		_opt_labels.append(l)
	_menu.add_child(_grid)
	_menu.hide()
	_root.add_child(_menu)


func _sprite(tex: Texture2D, pos: Vector2, k: int) -> TextureRect:
	var r := TextureRect.new()
	r.texture = tex
	r.scale = Vector2(k, k)
	r.position = pos
	_root.add_child(r)
	return r


func _info_box(pos: Vector2, title: String, sub: String) -> Array:
	var p := PanelContainer.new()
	p.position = pos
	p.custom_minimum_size = Vector2(180, 0)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 2)
	var t := Label.new()
	t.text = title
	var bar := ProgressBar.new()
	bar.show_percentage = false
	bar.custom_minimum_size = Vector2(166, 5)
	var s := Label.new()
	s.text = sub
	s.add_theme_color_override("font_color", Color("a8aab2"))
	v.add_child(t)
	v.add_child(bar)
	v.add_child(s)
	p.add_child(v)
	_root.add_child(p)
	return [bar, s]


func _draw_bg() -> void:
	var base := _bg_color
	for i in 12:  # degradado en bandas (look retro, sin interpolación suave)
		var c := base.darkened(0.25 + i * 0.05)
		_root.draw_rect(Rect2(0, i * 18, W, 18), c)
	_root.draw_rect(Rect2(0, 110, W, 1), base.lightened(0.1))
	for x in range(-200, W + 200, 40):  # piso en perspectiva
		_root.draw_line(Vector2(W * 0.5 + (x - W * 0.5) * 0.3, 110), Vector2(x, H), Color(1, 1, 1, 0.05))
	_ellipse(Vector2(368, 118), Vector2(70, 14), base.lightened(0.15))
	_ellipse(Vector2(108, 196), Vector2(84, 16), base.lightened(0.15))


func _ellipse(c: Vector2, r: Vector2, col: Color) -> void:
	_root.draw_set_transform(c, 0.0, Vector2(1.0, r.y / r.x))
	_root.draw_circle(Vector2.ZERO, r.x, col.darkened(0.4))
	_root.draw_circle(Vector2(0, -3), r.x - 4, col)
	_root.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


# ---------------------------------------------------------- animaciones

func _intro() -> void:
	var sp := _scp_sprite.position
	var pp := _ply_sprite.position
	_scp_sprite.position.x = -120
	_ply_sprite.position.x = W + 20
	var tw := create_tween().set_parallel()
	tw.tween_property(_scp_sprite, "position", sp, 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(_ply_sprite, "position", pp, 0.6).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	await tw.finished


func _hit(target: TextureRect, bar: ProgressBar, value: int) -> void:
	for i in 3:
		target.modulate.a = 0.0
		await get_tree().create_timer(0.06).timeout
		target.modulate.a = 1.0
		await get_tree().create_timer(0.06).timeout
	await _tween_bar(bar, value)


func _tween_bar(bar: ProgressBar, value: int) -> void:
	await create_tween().tween_property(bar, "value", float(value), 0.4).finished
	var ratio := bar.value / bar.max_value
	var fill := StyleBoxFlat.new()
	fill.bg_color = Color("6f9a2a") if ratio > 0.5 else (Color("e8c440") if ratio > 0.2 else Color("c9302c"))
	bar.add_theme_stylebox_override("fill", fill)


func _shake(target: Control) -> void:
	var x := target.position.x
	var tw := create_tween()
	for i in 4:
		tw.tween_property(target, "position:x", x + (4 if i % 2 == 0 else -4), 0.04)
	tw.tween_property(target, "position:x", x, 0.04)
	await tw.finished


func _lunge(target: Control, delta: Vector2) -> void:
	var p := target.position
	var tw := create_tween()
	tw.tween_property(target, "position", p + delta, 0.08)
	tw.tween_property(target, "position", p, 0.12)
	await tw.finished


func _flash_screen() -> void:
	var r := ColorRect.new()
	r.color = Color(1, 0.9, 0.6, 0.35)
	r.size = Vector2(W, H)
	_root.add_child(r)
	await get_tree().create_timer(0.05).timeout
	r.queue_free()


func _contained() -> void:
	Sfx.play("contain")
	var tw := create_tween().set_parallel()
	tw.tween_property(_scp_sprite, "modulate", Color(0.4, 0.7, 1.0, 0.0), 0.8)
	tw.tween_property(_scp_sprite, "scale", Vector2(2, 0.2), 0.8)
	tw.tween_property(_scp_sprite, "position:y", _scp_sprite.position.y + 80, 0.8)
	await tw.finished
	await _say("¡%s ha sido contenido!" % _scp.nombre)


# ------------------------------------------------------------- entrada

func _say(msg: String) -> void:
	_text.text = msg
	_text.visible_ratio = 0.0
	var tw := create_tween()
	tw.tween_property(_text, "visible_ratio", 1.0, 0.018 * msg.length())
	_waiting = true
	await _advance
	if tw.is_running():  # primer E completa el texto, el segundo avanza
		tw.kill()
		_text.visible_ratio = 1.0
		await _advance
	_waiting = false


func _choose() -> int:
	_text.text = "¿Qué hará el agente?"
	_text.visible_ratio = 1.0
	_list = []
	var i: int = await _open_menu()
	return i


## Submenú de consumibles. Devuelve el id elegido o "" si se cancela.
func _choose_item() -> String:
	_list = []
	for id in _st.inv:
		if _items[id].tipo == "consumible":
			_list.append(id)
	if _list.is_empty():
		await _say("No llevas nada que puedas usar ahora.")
		return ""
	_text.text = "¿Qué objeto usas? (Esc: volver)"
	_text.visible_ratio = 1.0
	var prev := _cursor
	_cursor = 0
	var i: int = await _open_menu()
	var id: String = _list[i] if i >= 0 else ""
	_list = []
	_cursor = prev
	return id


func _open_menu() -> int:
	_grid.columns = 1 if _list.size() > 0 else 2
	_menu.show()
	_menu_open = true
	_refresh_menu()
	var i: int = await _picked
	_menu_open = false
	_menu.hide()
	return i


func _entries() -> Array:
	if _list.is_empty():
		return OPTIONS
	return _list.map(func(id: String) -> String: return "%s x%d" % [_items[id].nombre, _st.inv[id]])


func _refresh_menu() -> void:
	var e := _entries()
	for i in _opt_labels.size():
		var l := _opt_labels[i]
		l.visible = i < e.size()
		if l.visible:
			l.text = ("> " if i == _cursor else "  ") + e[i]
			l.add_theme_color_override("font_color", Color("e8c440") if i == _cursor else Color("eef0ee"))


func _unhandled_input(event: InputEvent) -> void:
	if _waiting and event.is_action_pressed("ui_accept"):
		_advance.emit()
	elif _menu_open:
		var n := _entries().size()
		if event.is_action_pressed("ui_accept"):
			Sfx.play("select")
			_picked.emit(_cursor)
			return
		elif event.is_action_pressed("ui_cancel") and not _list.is_empty():
			_picked.emit(-1)
			return
		elif _list.is_empty() and (event.is_action_pressed("ui_right") or event.is_action_pressed("ui_left")):
			_cursor ^= 1
		elif event.is_action_pressed("ui_down"):
			_cursor = (_cursor + (1 if not _list.is_empty() else 2)) % n
		elif event.is_action_pressed("ui_up"):
			_cursor = (_cursor - (1 if not _list.is_empty() else 2) + n) % n
		else:
			return
		Sfx.play("move")
		_refresh_menu()
	else:
		return
	get_viewport().set_input_as_handled()
