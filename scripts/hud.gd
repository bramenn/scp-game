class_name Hud
extends CanvasLayer
## Interfaz sobre el mundo: viñeta, cartel de zona, caja de texto, vida y fundidos.

const W := 480
const H := 270

signal _advance

var theme_ui: Theme
var _fade: ColorRect
var _banner: PanelContainer
var _banner_title: Label
var _banner_sub: Label
var _box: PanelContainer
var _box_text: Label
var _hp_bar: ProgressBar
var _hp_label: Label
var _goal: Label
var _speaker: Label
var _waiting := false


static func make_theme() -> Theme:
	var t := Theme.new()
	t.default_font = load("res://art/font/Tiny5-Regular.ttf")  # nítida: sin AA en su .import
	t.default_font_size = 8  # rejilla nativa de Tiny5: usar solo múltiplos de 8
	t.set_stylebox("panel", "PanelContainer", panel_style())
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color("16161f")
	var fill := StyleBoxFlat.new()
	fill.bg_color = Color("6f9a2a")
	t.set_stylebox("background", "ProgressBar", bg)
	t.set_stylebox("fill", "ProgressBar", fill)
	t.set_color("font_color", "Label", Color("eef0ee"))
	t.set_color("font_shadow_color", "Label", Color(0, 0, 0, 0.8))
	t.set_constant("shadow_offset_x", "Label", 1)
	t.set_constant("shadow_offset_y", "Label", 1)
	return t


static func title_font() -> FontFile:
	return load("res://art/font/Tiny5-Regular.ttf")  # a 16 px = 2x exacto


static func panel_style(accent := Color("83858f")) -> StyleBoxFlat:
	var s := StyleBoxFlat.new()
	s.bg_color = Color(0.06, 0.06, 0.09, 0.92)
	s.border_color = accent
	s.set_border_width_all(1)
	s.set_content_margin_all(6)
	s.shadow_color = Color(0, 0, 0, 0.6)
	s.shadow_size = 2
	return s


func _ready() -> void:
	layer = 5
	theme_ui = make_theme()
	var root := Control.new()
	root.theme = theme_ui
	root.size = Vector2(W, H)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(root)

	var vig := TextureRect.new()
	var g := GradientTexture2D.new()
	g.fill = GradientTexture2D.FILL_RADIAL
	g.fill_from = Vector2(0.5, 0.5)
	g.fill_to = Vector2(1.05, 0.5)
	g.gradient = Gradient.new()
	g.gradient.set_color(0, Color(0, 0, 0, 0))
	g.gradient.set_color(1, Color(0, 0, 0, 0.7))
	vig.texture = g
	vig.size = Vector2(W, H)
	vig.stretch_mode = TextureRect.STRETCH_SCALE
	vig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(vig)

	_banner = PanelContainer.new()
	_banner.position = Vector2(8, -40)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 0)
	_banner_title = Label.new()
	_banner_title.add_theme_font_override("font", title_font())
	_banner_title.add_theme_font_size_override("font_size", 16)
	_banner_sub = Label.new()
	_banner_sub.add_theme_color_override("font_color", Color("a8aab2"))
	vb.add_child(_banner_title)
	vb.add_child(_banner_sub)
	_banner.add_child(vb)
	root.add_child(_banner)

	var hp := PanelContainer.new()
	hp.position = Vector2(W - 124, 6)
	hp.custom_minimum_size = Vector2(118, 0)
	var hv := VBoxContainer.new()
	hv.add_theme_constant_override("separation", 2)
	_hp_label = Label.new()
	_hp_bar = ProgressBar.new()
	_hp_bar.show_percentage = false
	_hp_bar.custom_minimum_size = Vector2(94, 4)
	_goal = Label.new()
	_goal.add_theme_color_override("font_color", Color("e8c440"))
	_goal.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_goal.custom_minimum_size = Vector2(94, 0)
	hv.add_child(_hp_label)
	hv.add_child(_hp_bar)
	hv.add_child(_goal)
	hp.add_child(hv)
	root.add_child(hp)

	var hint := Label.new()
	hint.text = "WASD mover  ·  E interactuar  ·  I inventario"
	hint.position = Vector2(8, H - 16)
	hint.add_theme_color_override("font_color", Color(0.66, 0.67, 0.7, 0.8))
	root.add_child(hint)

	_box = PanelContainer.new()
	_box.add_theme_stylebox_override("panel", panel_style(Color("d0d2d6")))
	_box.position = Vector2(8, H - 58)
	_box.custom_minimum_size = Vector2(W - 16, 50)
	var bv := VBoxContainer.new()
	_speaker = Label.new()
	_speaker.add_theme_color_override("font_color", Color("e8c440"))
	_box_text = Label.new()
	_box_text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_box_text.custom_minimum_size = Vector2(W - 30, 0)
	bv.add_child(_speaker)
	bv.add_child(_box_text)
	_box.add_child(bv)
	_box.hide()
	root.add_child(_box)

	_fade = ColorRect.new()
	_fade.color = Color.BLACK
	_fade.size = Vector2(W, H)
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_fade)


func set_goal(text: String) -> void:
	_goal.text = text


func set_hp(hp: int, max_hp: int) -> void:
	_hp_label.text = "AGENTE   %d/%d" % [hp, max_hp]
	_hp_bar.max_value = max_hp
	_hp_bar.value = hp


func show_banner(title: String, sub: String, sub_color := Color("a8aab2")) -> void:
	_banner_title.text = title
	_banner_sub.text = sub
	_banner_sub.add_theme_color_override("font_color", sub_color)
	var tw := create_tween()
	tw.tween_property(_banner, "position:y", 6.0, 0.35).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_interval(2.6)
	tw.tween_property(_banner, "position:y", -48.0, 0.3)


func fade(to_black: bool, t := 0.3) -> void:
	await create_tween().tween_property(_fade, "color:a", 1.0 if to_black else 0.0, t).finished


func flash(times := 2) -> void:
	for i in times:
		_fade.color = Color(1, 1, 1, 0.9)
		await get_tree().create_timer(0.07).timeout
		_fade.color = Color(0, 0, 0, 0)
		await get_tree().create_timer(0.09).timeout
	_fade.color = Color(0, 0, 0, 0)


## Muestra líneas una a una con efecto máquina de escribir; E/Enter avanza.
func say(lines: Array, speaker := "") -> void:
	_box.show()
	_speaker.text = speaker
	_speaker.visible = speaker != ""
	for line in lines:
		_box_text.text = line
		_box_text.visible_ratio = 0.0
		var tw := create_tween()
		tw.tween_property(_box_text, "visible_ratio", 1.0, 0.02 * String(line).length())
		_waiting = true
		await _advance
		if tw.is_running():
			tw.kill()
			_box_text.visible_ratio = 1.0
			await _advance
	_waiting = false
	_box.hide()


func _process(_dt: float) -> void:
	if _box.visible and _box_text.visible_ratio < 1.0 and Engine.get_process_frames() % 4 == 0:
		Sfx.play("blip", -6.0, randf_range(0.9, 1.1))


func _unhandled_input(event: InputEvent) -> void:
	if _waiting and event.is_action_pressed("ui_accept"):
		get_viewport().set_input_as_handled()
		_advance.emit()
