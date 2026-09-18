class_name PauseMenu
extends CanvasLayer
## Pause menu: Objectives / Inventory / Documents / Map / Options, plus the document reader.
## Left/right switch tabs, up/down select, E use/read, Esc close.

signal _closed
signal _doc_closed

const TABS := ["tab_objectives", "tab_inventory", "tab_documents", "tab_map", "tab_options"]
const TYPE_ORDER := ["key", "weapon", "consumable", "tool", "scp", "doc"]

var world: World
var root: Control
var body: Control
var tab_l: HBoxContainer
var tab := 0
var cursor := 0
var _open := false
var _reading := false
var _list: Array = []
var _doc_panel: PanelContainer


func _ready() -> void:
	layer = 8
	process_mode = Node.PROCESS_MODE_ALWAYS
	root = UiKit.root(self)
	root.hide()


func open() -> void:
	if _open:
		return
	_open = true
	world.busy += 1
	get_tree().paused = true
	Sfx.play("menu_open", -6.0)
	cursor = 0
	root.show()
	_render()
	await _closed
	root.hide()
	get_tree().paused = false
	world.busy -= 1


func close() -> void:
	_open = false
	Sfx.play("menu_close", -6.0)
	_closed.emit()


# ----------------------------------------------------------------- render

func _render() -> void:
	for c in root.get_children():
		c.queue_free()
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.72)
	dim.size = Vector2(UiKit.W, UiKit.H)
	root.add_child(dim)
	tab_l = HBoxContainer.new()
	tab_l.position = Vector2(12, 8)
	tab_l.add_theme_constant_override("separation", 14)
	for i in TABS.size():
		var l := UiKit.label(Loc.ui(TABS[i]).to_upper(), 8, UiKit.GOLD if i == tab else UiKit.DIM)
		tab_l.add_child(l)
	root.add_child(tab_l)
	var hint := UiKit.label(Loc.ui("menu_hint"), 8, UiKit.DIM)
	hint.position = Vector2(12, UiKit.H - 14)
	root.add_child(hint)
	var p := PanelContainer.new()
	p.position = Vector2(8, 22)
	p.custom_minimum_size = Vector2(UiKit.W - 16, UiKit.H - 40)
	root.add_child(p)
	body = Control.new()
	body.custom_minimum_size = Vector2(UiKit.W - 30, UiKit.H - 54)
	p.add_child(body)
	match TABS[tab]:
		"tab_objectives": _objectives()
		"tab_inventory": _inventory()
		"tab_documents": _documents()
		"tab_map": _map()
		"tab_options": _options()


func _line(text: String, y: float, col := Color("e4e6e8"), x := 0.0, w := 440.0) -> Label:
	var l := UiKit.label(text, 8, col)
	l.position = Vector2(x, y)
	l.custom_minimum_size = Vector2(w, 0)
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.add_child(l)
	return l


func _objectives() -> void:
	var st := world.st
	var y := 0.0
	var obj = st.flags.get("objective", "")
	if obj is Dictionary or String(obj) != "":
		_line(Loc.ui("current_objective"), y, UiKit.DIM)
		_line("> " + Loc.t(obj), y + 10, UiKit.GOLD)
		y += 26
	_list = []
	for q in Db.quests:
		var s: int = st.quest_stage(q)
		if s == 0:
			continue
		_list.append(q)
	_list.sort_custom(func(a, b): return (st.quest_stage(a) == -1) < (st.quest_stage(b) == -1))
	for q in _list:
		var info: Dictionary = Db.quests[q]
		var s: int = st.quest_stage(q)
		var done := s == -1
		var head := ("[x] " if done else "[ ] ") + Loc.t(info.name) + ("" if info.get("main", false) else "  (" + Loc.ui("side") + ")")
		_line(head, y, UiKit.DIM if done else UiKit.PALE)
		y += 10
		if not done:
			var stages: Array = info.get("stages", [])
			if s - 1 < stages.size():
				var l := _line(Loc.t(stages[s - 1]), y, UiKit.DIM, 12, 420)
				y += 10 + 10 * floor(l.get_line_count() - 1)
		y += 4
		if y > 190:
			break


func _inv_sorted() -> Array:
	var ids: Array = world.st.inv.keys()
	ids.sort_custom(func(a, b):
		var ta := TYPE_ORDER.find(Db.items.get(a, {}).get("type", "tool"))
		var tb := TYPE_ORDER.find(Db.items.get(b, {}).get("type", "tool"))
		return ta < tb if ta != tb else a < b)
	return ids


func _inventory() -> void:
	_list = _inv_sorted()
	cursor = clampi(cursor, 0, maxi(0, _list.size() - 1))
	if _list.is_empty():
		_line(Loc.ui("inv_empty"), 0, UiKit.DIM)
		return
	for i in _list.size():
		var id: String = _list[i]
		var info: Dictionary = Db.items.get(id, {})
		var x := (i % 2) * 118.0
		var y := (i / 2) * 13.0
		var ic := TextureRect.new()
		var path := "res://art/items/%s.png" % info.get("icon", id)
		ic.texture = load(path) if ResourceLoader.exists(path) else null
		ic.position = Vector2(x, y - 3)
		body.add_child(ic)
		var n: int = world.st.inv[id]
		_line(Loc.t(info.get("name", id)) + (" x%d" % n if n > 1 else ""), y, UiKit.GOLD if i == cursor else UiKit.PALE, x + 18, 100)
	var sel: Dictionary = Db.items.get(_list[cursor], {})
	var dx := 250.0
	var big := TextureRect.new()
	var bp := "res://art/items/%s.png" % sel.get("icon", _list[cursor])
	big.texture = load(bp) if ResourceLoader.exists(bp) else null
	big.scale = Vector2(3, 3)
	big.position = Vector2(dx, 0)
	body.add_child(big)
	_line(Loc.t(sel.get("name", _list[cursor])), 52, UiKit.GOLD, dx, 190)
	var desc := _line(Loc.t(sel.get("desc", "")), 64, UiKit.PALE, dx, 190)
	if sel.get("use", "") != "":
		_line(Loc.ui("press_use"), 64 + 10 * desc.get_line_count() + 6, UiKit.DIM, dx, 190)


func _documents() -> void:
	_list = world.st.docs.duplicate()
	cursor = clampi(cursor, 0, maxi(0, _list.size() - 1))
	if _list.is_empty():
		_line(Loc.ui("docs_empty"), 0, UiKit.DIM)
		return
	var first := maxi(0, cursor - 14)
	for i in range(first, mini(_list.size(), first + 17)):
		var d: Dictionary = Db.docs.get(_list[i], {})
		_line(Loc.t(d.get("title", _list[i])), (i - first) * 11.0, UiKit.GOLD if i == cursor else UiKit.PALE)
	_line("%d / %d" % [world.st.docs.size(), Db.docs.size()], 200, UiKit.DIM, 380, 60)


func _map() -> void:
	var st := world.st
	var v := world.view
	var b: PackedByteArray = st.explored.get(st.map, PackedByteArray())
	var scale := floorf(minf(440.0 / v.w, 190.0 / v.h))
	scale = maxf(scale, 1.0)
	var img := Image.create(v.w, v.h, false, Image.FORMAT_RGBA8)
	for y in v.h:
		for x in v.w:
			if b.size() == v.w * v.h and b[y * v.w + x] == 0:
				continue
			var t := Vector2i(x, y)
			var c := v.ch(t)
			if c == "#":
				img.set_pixel(x, y, Color("6d6f7a") if v.is_face(t) else Color("33333f"))
			elif c != " ":
				img.set_pixel(x, y, Color("1f3d3a") if not v.water.has(t) else Color("243a4c"))
	for dr in v.doors:
		var col := Color("5ec46a") if world.can_open(dr) else Color("d8403a")
		for t in dr.tiles():
			if b.size() == v.w * v.h and b[t.y * v.w + t.x] == 1:
				img.set_pixel(t.x, t.y, col)
	var tr := TextureRect.new()
	tr.texture = ImageTexture.create_from_image(img)
	tr.scale = Vector2(scale, scale)
	tr.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	var off := Vector2((440.0 - v.w * scale) / 2.0, 12.0)
	tr.position = off
	body.add_child(tr)
	var me := ColorRect.new()
	me.color = UiKit.GOLD
	me.size = Vector2(maxf(scale, 2), maxf(scale, 2))
	me.position = off + Vector2(world.player.tile) * scale
	body.add_child(me)
	var blink := me.create_tween().set_loops()
	blink.tween_property(me, "modulate:a", 0.2, 0.4)
	blink.tween_property(me, "modulate:a", 1.0, 0.4)
	for r in v.data.get("rooms", []):
		var rr: Array = r.rect
		var c := Vector2i(int(rr[0]) + int(rr[2]) / 2, int(rr[1]) + int(rr[3]) / 2)
		if b.size() == v.w * v.h and b[c.y * v.w + c.x] == 1:
			var l := UiKit.label(Loc.t(r.name), 8, UiKit.PALE)
			l.position = off + Vector2(c) * scale - Vector2(20, 4)
			body.add_child(l)
	_line(Loc.t(v.data.name), 0, UiKit.GOLD)


func _options() -> void:
	var opts := [
		[Loc.ui("opt_language"), "English" if Loc.lang == "en" else "Español"],
		[Loc.ui("opt_master"), "%d%%" % int(Sfx.get_volume("Master") * 100)],
		[Loc.ui("opt_music"), "%d%%" % int(Sfx.get_volume("Music") * 100)],
		[Loc.ui("opt_sfx"), "%d%%" % int(Sfx.get_volume("SFX") * 100)],
		[Loc.ui("opt_fullscreen"), Loc.ui("on") if DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN else Loc.ui("off")],
		[Loc.ui("opt_save_quit"), ""],
	]
	_list = opts
	for i in opts.size():
		_line(opts[i][0], i * 14.0, UiKit.GOLD if i == cursor else UiKit.PALE)
		_line(opts[i][1], i * 14.0, UiKit.GOLD if i == cursor else UiKit.PALE, 200, 120)
	_line(Loc.ui("controls_help"), 100, UiKit.DIM)


func _option_change(delta: int) -> void:
	match cursor:
		0:
			Loc.set_lang("es" if Loc.lang == "en" else "en")
		1, 2, 3:
			var bus: String = ["Master", "Music", "SFX"][cursor - 1]
			var v := clampf(snappedf(Sfx.get_volume(bus) + 0.1 * delta, 0.1), 0.0, 1.0)
			Sfx.set_volume(bus, v)
			Loc.save_setting("vol_" + bus, v)
		4:
			var fs := DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN
			DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED if fs else DisplayServer.WINDOW_MODE_FULLSCREEN)
			Loc.save_setting("fullscreen", not fs)
		5:
			world.st.save()
			get_tree().paused = false
			get_tree().quit()


func _use_item(id: String) -> void:
	var info: Dictionary = Db.items.get(id, {})
	var st := world.st
	match String(info.get("use", "")):
		"heal":
			if st.hp >= GameState.MAX_HP:
				return
			st.take(id)
			st.hp = minf(GameState.MAX_HP, st.hp + float(info.get("amount", 30)))
			Sfx.play("heal", -4.0)
		"battery":
			st.take(id)
			st.battery = 100.0
			Sfx.play("battery", -4.0)
		"sanity":
			st.take(id)
			st.sanity = minf(100.0, st.sanity + float(info.get("amount", 30)))
			Sfx.play("drink", -4.0)
		"full":
			st.take(id)
			st.hp = GameState.MAX_HP
			st.sanity = 100.0
			Sfx.play("heal", -2.0)
		"read":
			await read_doc(String(info.get("doc", id)))
		"event":
			close()
			world.events.run(String(info.get("event", "")))
			return
	_render()


# ---------------------------------------------------------------- documents

func read_doc(id: String) -> void:
	var d: Dictionary = Db.docs.get(id, {})
	var was_paused := get_tree().paused
	get_tree().paused = true
	world.busy += 1
	_reading = true
	var layer_root := UiKit.root(self)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.8)
	dim.size = Vector2(UiKit.W, UiKit.H)
	layer_root.add_child(dim)
	_doc_panel = PanelContainer.new()
	var paper := StyleBoxFlat.new()
	paper.bg_color = Color("d4cdb4")
	paper.border_color = Color("6b6352")
	paper.set_border_width_all(1)
	paper.set_content_margin_all(10)
	_doc_panel.add_theme_stylebox_override("panel", paper)
	_doc_panel.position = Vector2(60, 10)
	_doc_panel.custom_minimum_size = Vector2(360, 250)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 4)
	var cls := UiKit.label(Loc.t(d.get("class", {"en": "SCP FOUNDATION - CLASSIFIED", "es": "FUNDACIÓN SCP - CLASIFICADO"})), 8, Color("6a1419"))
	var title := UiKit.label(Loc.t(d.get("title", id)), 16, Color("1a1a23"))
	var text := UiKit.label(Loc.t(d.get("body", "")), 8, Color("262631"))
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.custom_minimum_size = Vector2(340, 0)
	for l in [cls, title, text]:
		l.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0))
		vb.add_child(l)
	if d.has("source"):
		var src := UiKit.label(d.source, 8, Color("6b6352"))
		src.add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0))
		vb.add_child(src)
	_doc_panel.add_child(vb)
	layer_root.add_child(_doc_panel)
	Sfx.play("paper", -4.0)
	if float(d.get("sanity", 0.0)) != 0.0 and not world.st.has("read:" + id):
		world.st.sanity = clampf(world.st.sanity + float(d.sanity), 0.0, 100.0)
	world.st.mark("read:" + id)
	await _doc_closed
	layer_root.queue_free()
	_reading = false
	world.busy -= 1
	get_tree().paused = was_paused


# ---------------------------------------------------------------------- input

func _unhandled_input(event: InputEvent) -> void:
	if _reading:
		if event.is_action_pressed("interact") or event.is_action_pressed("menu") or event.is_action_pressed("ui_cancel"):
			get_viewport().set_input_as_handled()
			Sfx.play("paper", -8.0)
			_doc_closed.emit()
		return
	if not _open:
		return
	get_viewport().set_input_as_handled()
	if not event.is_pressed() or event.is_echo():
		return
	if event.is_action_pressed("menu") or event.is_action_pressed("ui_cancel"):
		close()
		return
	var n := _list.size()
	if event.is_action_pressed("ui_right") and not (TABS[tab] == "tab_options" and cursor < 4) and TABS[tab] != "tab_inventory":
		tab = (tab + 1) % TABS.size()
		cursor = 0
	elif event.is_action_pressed("ui_left") and not (TABS[tab] == "tab_options" and cursor < 4) and TABS[tab] != "tab_inventory":
		tab = (tab - 1 + TABS.size()) % TABS.size()
		cursor = 0
	elif TABS[tab] == "tab_inventory" and (event.is_action_pressed("ui_right") or event.is_action_pressed("ui_left")):
		if event.is_action_pressed("ui_right") and cursor % 2 == 0 and cursor + 1 < n:
			cursor += 1
		elif event.is_action_pressed("ui_left") and cursor % 2 == 1:
			cursor -= 1
		elif event.is_action_pressed("ui_right"):
			tab = (tab + 1) % TABS.size()
			cursor = 0
		else:
			tab = (tab - 1 + TABS.size()) % TABS.size()
			cursor = 0
	elif TABS[tab] == "tab_options" and (event.is_action_pressed("ui_right") or event.is_action_pressed("ui_left")):
		_option_change(1 if event.is_action_pressed("ui_right") else -1)
	elif event.is_action_pressed("ui_down") and n > 0:
		cursor = (cursor + (2 if TABS[tab] == "tab_inventory" else 1)) % n
	elif event.is_action_pressed("ui_up") and n > 0:
		cursor = (cursor - (2 if TABS[tab] == "tab_inventory" else 1) + n) % n
	elif event.is_action_pressed("interact"):
		match TABS[tab]:
			"tab_inventory":
				if n > 0:
					await _use_item(_list[cursor])
			"tab_documents":
				if n > 0:
					await read_doc(_list[cursor])
			"tab_options":
				_option_change(1)
	else:
		return
	Sfx.play("move", -10.0)
	if _open:
		_render()
