class_name Battle
extends CanvasLayer
## Turn-based encounter. Enemy data: data/story.json "enemies"[id] =
##   {name, sprite (art/chars id or art/props png), hp, atk, def, spd, moves:[{name, power, fx?}],
##    flee (0..1), special?: {label, cond, event_flag, text, dmg_pct}, intro, bg}
## Player: FIGHT (pistol if you carry it and have ammo, else baton), ITEM, SPECIAL, FLEE.
## Returns "win" | "lose" | "flee". Player hp is the real GameState hp.

const W := 480
const H := 270

signal _picked(i: int)
signal _advance

var e: Dictionary
var st: GameState
var ehp := 0
var emax := 0
var _cursor := 0
var _opts: Array = []
var _menu_open := false
var _waiting := false
var root: Control
var esprite: Control
var psprite: TextureRect
var ebar: ProgressBar
var pbar: ProgressBar
var plabel: Label
var text: Label
var menu: VBoxContainer
var menu_panel: PanelContainer


static func damage(power: float, atk: float, def: float) -> int:
	return maxi(1, int(round(power * atk / (def + 12.0))))


func run(enemy_id: String, s: GameState) -> String:
	st = s
	e = Db.story.get("enemies", {}).get(enemy_id, {"name": enemy_id, "hp": 30, "atk": 10, "def": 4, "moves": [{"name": "Attack", "power": 10}]})
	emax = int(e.hp)
	ehp = emax
	layer = 12
	_build()
	Sfx.music(String(e.get("music", "battle")))
	await _intro()
	var intro := Loc.t(e.get("intro", {"en": "%s attacks!", "es": "¡%s ataca!"}))
	await _say(intro % Loc.t(e.name) if "%s" in intro else intro)
	var result := ""
	while result == "":
		var pick: String = await _choose()
		if pick == "item":
			var used := await _choose_item()
			if used == "":
				continue
			await _use_item(used)
		elif pick == "special":
			result = await _special()
			if result != "":
				break
		elif pick == "flee":
			if randf() < float(e.get("flee", 0.5)):
				await _say(Loc.ui("b_fled"))
				result = "flee"
				break
			Sfx.play("denied", -6.0)
			await _say(Loc.ui("b_no_flee"))
		else:
			result = await _attack()
			if result != "":
				break
		await _enemy_turn()
		if st.hp <= 0:
			result = "lose"
	if result == "win":
		Sfx.play("quest", -4.0)
		await _say(Loc.t(e.get("win", {"en": "It stops moving.", "es": "Deja de moverse."})))
	Sfx.music("")
	await get_tree().create_timer(0.2).timeout
	return result


# ------------------------------------------------------------------ turns

func _weapon() -> String:
	return "pistol" if st.count("pistol") > 0 and st.count("ammo") > 0 else "baton"


func _attack() -> String:
	var w := _weapon()
	var power := 22.0 if w == "pistol" else 12.0
	var atk := 14.0 + (4.0 if st.count("vest") > 0 else 0.0)
	if w == "pistol":
		st.take("ammo")
		Sfx.play("shoot", -2.0)
		await _flash(Color(1, 0.9, 0.6, 0.4))
		await _say(Loc.ui("b_shoot", [Loc.t(e.name)]))
	else:
		Sfx.play("hit", -2.0)
		await _say(Loc.ui("b_swing" if st.count("baton") > 0 else "b_punch", [Loc.t(e.name)]))
		if st.count("baton") == 0:
			power = 6.0
	var dmg := damage(power + randf_range(-3, 3), atk, float(e.def))
	if e.get("immune", false):
		dmg = maxi(1, dmg / 5)
	ehp = maxi(0, ehp - dmg)
	await _hit(esprite, ebar, ehp)
	if e.get("immune", false):
		await _say(Loc.t(e.get("immune_text", {"en": "The wound closes as you watch.", "es": "La herida se cierra mientras miras."})))
	if ehp <= 0:
		return "win"
	return ""


func _enemy_turn() -> void:
	var moves: Array = e.get("moves", [])
	if moves.is_empty():
		return
	var mv: Dictionary = moves.pick_random()
	await _say(Loc.ui("b_uses", [Loc.t(e.name), Loc.t(mv.name)]))
	if mv.get("fx", "") == "heal":
		ehp = mini(emax, ehp + int(mv.power))
		Sfx.play("heal", -4.0, 0.6)
		await _tween_bar(ebar, ehp)
		return
	if mv.get("fx", "") == "sanity":
		st.sanity = maxf(0.0, st.sanity - float(mv.power))
		Sfx.play("whisper", -2.0)
		await _shake(psprite)
		await _say(Loc.ui("b_mind"))
		return
	await _lunge(esprite)
	var def := 8.0 + (6.0 if st.count("vest") > 0 else 0.0)
	var dmg := damage(float(mv.power) + randf_range(-3, 3), float(e.atk), def)
	st.hp = maxf(0.0, st.hp - dmg)
	Sfx.play("hurt", -2.0)
	await _hit(psprite, pbar, int(st.hp))


func _special() -> String:
	var sp: Dictionary = e.special
	await _say(Loc.t(sp.text))
	if sp.has("dmg_pct"):
		ehp = maxi(0, ehp - int(emax * float(sp.dmg_pct)))
		await _hit(esprite, ebar, ehp)
	if sp.has("event_flag"):
		st.mark(String(sp.event_flag))
	if sp.get("ends", false) or ehp <= 0:
		return "win"
	return ""


func _use_item(id: String) -> void:
	var info: Dictionary = Db.items.get(id, {})
	st.take(id)
	match String(info.get("use", "")):
		"heal":
			st.hp = minf(GameState.MAX_HP, st.hp + float(info.get("amount", 30)))
		"full":
			st.hp = GameState.MAX_HP
			st.sanity = 100.0
		"sanity":
			st.sanity = minf(100.0, st.sanity + float(info.get("amount", 30)))
	Sfx.play("heal", -4.0)
	await _tween_bar(pbar, int(st.hp))
	await _say(Loc.ui("b_used", [Loc.t(info.get("name", id))]))


# --------------------------------------------------------------------- UI

func _build() -> void:
	root = UiKit.root(self)
	var bg := ColorRect.new()
	bg.size = Vector2(W, H)
	bg.color = Color.BLACK
	root.add_child(bg)
	root.draw.connect(_draw_bg)
	var src := String(e.get("sprite", "zombie"))
	if ResourceLoader.exists("res://art/chars/%s/south.png" % src):
		var a := AnimatedSprite2D.new()
		a.sprite_frames = CharFrames.get_frames(src)
		a.play("walk_south" if a.sprite_frames.has_animation("walk_south") else "idle_south")
		a.speed_scale = 0.35
		a.scale = Vector2(3, 3) if CharFrames.frame_size(src).x <= 48 else Vector2(2, 2)
		var holder := Control.new()
		holder.position = Vector2(360, 124)
		a.offset = Vector2(0, -CharFrames.feet_y(src) + CharFrames.frame_size(src).y / 2.0)
		holder.add_child(a)
		root.add_child(holder)
		esprite = holder
	else:
		var tr := TextureRect.new()
		tr.texture = load("res://art/props/%s.png" % src)
		tr.scale = Vector2(3, 3)
		tr.position = Vector2(312, 20)
		root.add_child(tr)
		esprite = tr
	psprite = TextureRect.new()
	psprite.texture = load("res://art/chars/vega/north.png")
	psprite.scale = Vector2(4, 4)
	psprite.position = Vector2(30, 58)
	root.add_child(psprite)
	var eb := _box(Vector2(12, 12), Loc.t(e.name), Loc.t(e.get("tag", "")))
	ebar = eb[0]
	ebar.max_value = emax
	ebar.value = ehp
	var pb := _box(Vector2(W - 204, 128), "VEGA", "")
	pbar = pb[0]
	plabel = pb[1]
	pbar.max_value = GameState.MAX_HP
	pbar.value = st.hp
	pbar.value_changed.connect(func(v: float) -> void: plabel.text = "%d / %d   %s" % [int(v), int(GameState.MAX_HP), _ammo_text()])
	plabel.text = "%d / %d   %s" % [int(st.hp), int(GameState.MAX_HP), _ammo_text()]
	var tb := PanelContainer.new()
	tb.position = Vector2(6, H - 64)
	tb.custom_minimum_size = Vector2(W - 12, 58)
	text = UiKit.label("")
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.custom_minimum_size = Vector2(270, 0)
	tb.add_child(text)
	root.add_child(tb)
	menu_panel = PanelContainer.new()
	menu_panel.add_theme_stylebox_override("panel", UiKit.panel("panel_gold"))
	menu_panel.position = Vector2(W - 170, H - 64)
	menu_panel.custom_minimum_size = Vector2(164, 58)
	menu = VBoxContainer.new()
	menu.add_theme_constant_override("separation", 1)
	menu_panel.add_child(menu)
	menu_panel.hide()
	root.add_child(menu_panel)


func _ammo_text() -> String:
	return Loc.ui("b_ammo", [st.count("ammo")]) if st.count("pistol") > 0 else ""


func _box(pos: Vector2, title: String, sub: String) -> Array:
	var p := PanelContainer.new()
	p.position = pos
	p.custom_minimum_size = Vector2(192, 0)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 2)
	v.add_child(UiKit.label(title, 8, UiKit.GOLD))
	var b := UiKit.bar(Color("9ab94a"), 176, 4)
	v.add_child(b)
	var s := UiKit.label(sub, 8, UiKit.DIM)
	v.add_child(s)
	p.add_child(v)
	root.add_child(p)
	return [b, s]


func _draw_bg() -> void:
	var base := Color(e.get("bg", "#1a1d24"))
	for i in 15:
		root.draw_rect(Rect2(0, i * 18, W, 18), base.darkened(0.15 + i * 0.045))
	for x in range(-240, W + 240, 32):
		root.draw_line(Vector2(W * 0.5 + (x - W * 0.5) * 0.25, 110), Vector2(x, H), Color(1, 1, 1, 0.04))
	root.draw_rect(Rect2(0, 110, W, 1), base.lightened(0.08))
	for c in [[Vector2(360, 126), 78.0], [Vector2(112, 200), 96.0]]:
		root.draw_set_transform(c[0], 0.0, Vector2(1.0, 0.22))
		root.draw_circle(Vector2.ZERO, c[1], Color(0, 0, 0, 0.45))
		root.draw_circle(Vector2(0, -6), c[1] - 6, base.lightened(0.06))
		root.draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)


func _intro() -> void:
	var ep := esprite.position
	var pp := psprite.position
	esprite.position.x = W + 40
	psprite.position.x = -200
	var tw := create_tween().set_parallel()
	tw.tween_property(esprite, "position", ep, 0.7).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	tw.tween_property(psprite, "position", pp, 0.7).set_trans(Tween.TRANS_QUAD).set_ease(Tween.EASE_OUT)
	await tw.finished
	if e.has("cry"):
		Sfx.play(String(e.cry), 0.0)


func _hit(target: Control, bar: ProgressBar, value: int) -> void:
	for i in 3:
		target.modulate = Color(1, 0.3, 0.3)
		await get_tree().create_timer(0.05).timeout
		target.modulate = Color.WHITE
		await get_tree().create_timer(0.05).timeout
	await _tween_bar(bar, value)


func _tween_bar(bar: ProgressBar, value: int) -> void:
	await create_tween().tween_property(bar, "value", float(value), 0.35).finished
	var r := bar.value / bar.max_value
	var f := StyleBoxFlat.new()
	f.bg_color = Color("9ab94a") if r > 0.5 else (Color("d6b441") if r > 0.2 else Color("c9362e"))
	bar.add_theme_stylebox_override("fill", f)


func _shake(target: Control) -> void:
	var x := target.position.x
	var tw := create_tween()
	for i in 6:
		tw.tween_property(target, "position:x", x + (3 if i % 2 == 0 else -3), 0.035)
	tw.tween_property(target, "position:x", x, 0.035)
	await tw.finished


func _lunge(target: Control) -> void:
	var p := target.position
	var tw := create_tween()
	tw.tween_property(target, "position", p + Vector2(-26, 14), 0.09)
	tw.tween_property(target, "position", p, 0.15)
	await tw.finished


func _flash(c: Color) -> void:
	var r := ColorRect.new()
	r.color = c
	r.size = Vector2(W, H)
	root.add_child(r)
	await get_tree().create_timer(0.05).timeout
	r.queue_free()


# ------------------------------------------------------------------ input

func _say(msg: String) -> void:
	text.text = msg
	text.visible_ratio = 0.0
	var tw := create_tween()
	tw.tween_property(text, "visible_ratio", 1.0, 0.016 * msg.length())
	_waiting = true
	await _advance
	if tw.is_running():
		tw.kill()
		text.visible_ratio = 1.0
		await _advance
	_waiting = false


func _choose() -> String:
	var ids := ["fight", "item"]
	if e.has("special") and st.check(e.special.get("cond", "")):
		ids.append("special")
	ids.append("flee")
	text.text = Loc.ui("b_what")
	text.visible_ratio = 1.0
	var labels := []
	for id in ids:
		if id == "fight":
			labels.append(Loc.ui("b_fight_" + _weapon()))
		elif id == "special":
			labels.append(Loc.t(e.special.label))
		else:
			labels.append(Loc.ui("b_" + id))
	var i: int = await _open(labels)
	return ids[i]


func _choose_item() -> String:
	var ids: Array = []
	for id in st.inv:
		if Db.items.get(id, {}).get("use", "") in ["heal", "full", "sanity"]:
			ids.append(id)
	if ids.is_empty():
		await _say(Loc.ui("b_no_items"))
		return ""
	text.text = Loc.ui("b_which")
	var labels := ids.map(func(id): return "%s x%d" % [Loc.t(Db.items[id].name), st.count(id)])
	labels.append(Loc.ui("b_back"))
	var i: int = await _open(labels)
	return ids[i] if i < ids.size() else ""


func _open(labels: Array) -> int:
	for c in menu.get_children():
		c.queue_free()
	_opts = labels
	for l in labels:
		menu.add_child(UiKit.label(""))
	_cursor = 0
	menu_panel.show()
	_menu_open = true
	await get_tree().process_frame
	_refresh()
	var i: int = await _picked
	_menu_open = false
	menu_panel.hide()
	return i


func _refresh() -> void:
	var k := 0
	for c in menu.get_children():
		if c.is_queued_for_deletion():
			continue
		(c as Label).text = ("> " if k == _cursor else "  ") + String(_opts[k])
		(c as Label).add_theme_color_override("font_color", UiKit.GOLD if k == _cursor else UiKit.PALE)
		k += 1


func _unhandled_input(event: InputEvent) -> void:
	if _waiting and event.is_action_pressed("interact"):
		_advance.emit()
	elif _menu_open:
		if event.is_action_pressed("interact"):
			Sfx.play("select", -6.0)
			_picked.emit(_cursor)
		elif event.is_action_pressed("ui_down"):
			_cursor = (_cursor + 1) % _opts.size()
		elif event.is_action_pressed("ui_up"):
			_cursor = (_cursor - 1 + _opts.size()) % _opts.size()
		else:
			return
		Sfx.play("move", -10.0)
		_refresh()
	else:
		return
	get_viewport().set_input_as_handled()
