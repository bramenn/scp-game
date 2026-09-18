class_name TitleScreen
extends CanvasLayer
## Title: drifting fog, flickering emblem, rotating alarm light, menu. run() returns
## "continue" | "new" | "quit".

signal _chosen(opt: String)

var root: Control
var _opts: Array = []
var _labels: Array[Label] = []
var _cursor := 0
var _emblem: TextureRect
var _t := 0.0
var _alarm: ColorRect
var _static := {}   # ui key -> Label (retranslated on language change)


func run(can_continue: bool) -> String:
	layer = 20
	root = UiKit.root(self)
	var bg := ColorRect.new()
	bg.color = Color("07070b")
	bg.size = Vector2(UiKit.W, UiKit.H)
	root.add_child(bg)
	var fog := Fog.new()
	root.add_child(fog)
	fog.setup(Vector2(UiKit.W, UiKit.H), Color("5a2a2e"), 0.55)
	_alarm = ColorRect.new()
	_alarm.color = Color(0.8, 0.05, 0.05, 0.0)
	_alarm.size = Vector2(UiKit.W, UiKit.H)
	_alarm.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_alarm)
	_emblem = TextureRect.new()
	_emblem.texture = load("res://art/gen/ui/emblem.png")
	_emblem.position = Vector2(UiKit.W / 2.0 - 24, 26)
	root.add_child(_emblem)
	_center("SCP", 16, 84, Color("c9362e"))
	_static.title_site = _center("", 16, 100, Color("e4e6e8"))
	_static.title_sub = _center("", 8, 120, UiKit.DIM)
	_opts = (["continue"] if can_continue else []) + ["new", "language", "quit"]
	for i in _opts.size():
		_labels.append(_center("", 8, 158 + i * 13, UiKit.PALE))
	_static.license_line = _center("", 8, UiKit.H - 22, Color(0.45, 0.45, 0.5))
	_static.controls_short = _center("", 8, UiKit.H - 12, Color(0.35, 0.35, 0.4))
	_refresh()
	Sfx.music("title")
	Sfx.ambience("")
	var o: String = await _chosen
	Sfx.play("select", -2.0)
	Sfx.music("")
	var tw := create_tween()
	tw.tween_property(root, "modulate", Color.BLACK, 0.8)
	await tw.finished
	return o


func _center(text: String, size: int, y: float, col: Color) -> Label:
	var l := UiKit.label(text, size, col)
	l.position = Vector2(0, y)
	l.size = Vector2(UiKit.W, size + 4)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(l)
	return l


func _refresh() -> void:
	for k in _static:
		_static[k].text = Loc.ui(k)
	var names := {"continue": "menu_continue", "new": "menu_new", "language": "menu_language", "quit": "menu_quit"}
	for i in _labels.size():
		var t := Loc.ui(names[_opts[i]])
		if _opts[i] == "language":
			t += ": " + ("English" if Loc.lang == "en" else "Español")
		_labels[i].text = ("> %s <" % t) if i == _cursor else t
		_labels[i].add_theme_color_override("font_color", UiKit.GOLD if i == _cursor else UiKit.DIM)


func _process(dt: float) -> void:
	_t += dt
	if _emblem:  # emblem flickers like a failing sign
		_emblem.modulate.a = 1.0 if fmod(_t, 4.7) > 0.12 or randf() > 0.5 else 0.3
	if _alarm:
		_alarm.color.a = 0.06 * maxf(0.0, sin(_t * 3.0))


func _unhandled_input(event: InputEvent) -> void:
	if _labels.is_empty():
		return
	if event.is_action_pressed("ui_down"):
		_cursor = (_cursor + 1) % _labels.size()
	elif event.is_action_pressed("ui_up"):
		_cursor = (_cursor - 1 + _labels.size()) % _labels.size()
	elif event.is_action_pressed("interact") or event.is_action_pressed("ui_accept"):
		if _opts[_cursor] == "language":
			Loc.set_lang("es" if Loc.lang == "en" else "en")
		else:
			_chosen.emit(_opts[_cursor])
			_labels.clear()
			get_viewport().set_input_as_handled()
			return
	else:
		return
	Sfx.play("move", -8.0)
	_refresh()
	get_viewport().set_input_as_handled()
