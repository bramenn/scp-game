class_name Title
extends CanvasLayer
## Pantalla de título. show_menu() devuelve "continuar" | "nueva" | "salir".

const W := 480
const H := 270

signal _chosen(opt: String)

var _opts: Array = []
var _labels: Array[Label] = []
var _cursor := 0
var _root: Control


func show_menu(can_continue: bool, heading := "") -> String:
	layer = 20
	_root = Control.new()
	_root.theme = Hud.make_theme()
	_root.size = Vector2(W, H)
	add_child(_root)
	_root.draw.connect(_draw_bg)

	var ids := ["scp-173", "scp-049", "scp-096", "scp-106", "scp-682"]
	for i in ids.size():  # siluetas de los SCP al fondo
		var s := TextureRect.new()
		s.texture = load("res://art/scp/%s.png" % ids[i])
		s.position = Vector2(40 + i * 84, 150)
		s.scale = Vector2(2, 2)
		s.modulate = Color(0.25, 0.08, 0.08, 0.9)
		_root.add_child(s)
		var tw := s.create_tween().set_loops()
		tw.tween_property(s, "modulate:a", 0.4, 1.5 + i * 0.3)
		tw.tween_property(s, "modulate:a", 0.9, 1.5 + i * 0.3)

	_label(heading if heading != "" else "SCP", Vector2(0, 28), 48, Color("c9302c"))
	_label("SITIO-19", Vector2(0, 80), 24, Color("eef0ee"))
	var alert := _label("BRECHA DE CONTENCIÓN", Vector2(0, 110), 8, Color("e8c440"))
	var at := alert.create_tween().set_loops()
	at.tween_property(alert, "modulate:a", 0.2, 0.6)
	at.tween_property(alert, "modulate:a", 1.0, 0.6)

	_opts = (["continuar"] if can_continue else []) + ["nueva", "salir"]
	var names := {"continuar": "CONTINUAR", "nueva": "NUEVA PARTIDA", "salir": "SALIR"}
	for i in _opts.size():
		_labels.append(_label(names[_opts[i]], Vector2(0, 186 + i * 14), 8, Color.WHITE))
	_label("Basado en la Fundación SCP · scp-wiki.wikidot.com · CC BY-SA 3.0", Vector2(0, H - 14), 8, Color(0.5, 0.5, 0.55))
	_refresh()
	Sfx.music("title")
	Sfx.ambience("")
	var opt: String = await _chosen
	Sfx.play("select")
	return opt


func _label(text: String, pos: Vector2, size: int, col: Color) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	l.size = Vector2(W, size + 4)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", col)
	_root.add_child(l)
	return l


func _draw_bg() -> void:
	_root.draw_rect(Rect2(0, 0, W, H), Color("0b0b12"))
	for y in range(0, H, 3):  # líneas de monitor CRT
		_root.draw_rect(Rect2(0, y, W, 1), Color(1, 1, 1, 0.025))
	_root.draw_rect(Rect2(60, 102, W - 120, 1), Color("4a1016"))
	_root.draw_rect(Rect2(60, 124, W - 120, 1), Color("4a1016"))


func _refresh() -> void:
	for i in _labels.size():
		_labels[i].text = ("> %s <" if i == _cursor else "%s") % _labels[i].text.trim_prefix("> ").trim_suffix(" <")
		_labels[i].add_theme_color_override("font_color", Color("e8c440") if i == _cursor else Color("a8aab2"))


func _unhandled_input(event: InputEvent) -> void:
	if _labels.is_empty():
		return
	if event.is_action_pressed("ui_down"):
		_cursor = (_cursor + 1) % _labels.size()
	elif event.is_action_pressed("ui_up"):
		_cursor = (_cursor - 1 + _labels.size()) % _labels.size()
	elif event.is_action_pressed("ui_accept"):
		_chosen.emit(_opts[_cursor])
		_labels.clear()
		get_viewport().set_input_as_handled()
		return
	else:
		return
	Sfx.play("move")
	_refresh()
	get_viewport().set_input_as_handled()
