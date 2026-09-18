class_name UiKit
extends RefCounted
## Shared UI look: pixel font, 9-slice panels, labels.

const W := 480
const H := 270
const GOLD := Color("d6b441")
const PALE := Color("c3c5cb")
const DIM := Color("878993")
const RED := Color("c9362e")

static var _theme: Theme
static var _font: Font


static func font() -> Font:
	if not _font:
		_font = load("res://art/font/Tiny5-Regular.ttf")
	return _font


static func panel(kind := "panel") -> StyleBoxTexture:
	var s := StyleBoxTexture.new()
	s.texture = load("res://art/gen/ui/%s.png" % kind)
	s.set_texture_margin_all(8)
	s.set_content_margin_all(7)
	return s


static func theme() -> Theme:
	if _theme:
		return _theme
	_theme = Theme.new()
	_theme.default_font = font()
	_theme.default_font_size = 8
	_theme.set_stylebox("panel", "PanelContainer", panel())
	_theme.set_stylebox("panel", "Panel", panel())
	_theme.set_color("font_color", "Label", Color("e4e6e8"))
	_theme.set_color("font_shadow_color", "Label", Color(0, 0, 0, 0.85))
	_theme.set_constant("shadow_offset_x", "Label", 1)
	_theme.set_constant("shadow_offset_y", "Label", 1)
	_theme.set_constant("line_spacing", "Label", 2)
	var bg := StyleBoxFlat.new()
	bg.bg_color = Color("101017")
	_theme.set_stylebox("background", "ProgressBar", bg)
	return _theme


static func label(text := "", size := 8, col := Color("e4e6e8")) -> Label:
	var l := Label.new()
	l.text = text
	l.add_theme_font_size_override("font_size", size)
	l.add_theme_color_override("font_color", col)
	return l


static func bar(col: Color, w := 60, h := 3) -> ProgressBar:
	var b := ProgressBar.new()
	b.show_percentage = false
	b.custom_minimum_size = Vector2(w, h)
	var f := StyleBoxFlat.new()
	f.bg_color = col
	b.add_theme_stylebox_override("fill", f)
	b.max_value = 100
	return b


static func root(layer_node: CanvasLayer) -> Control:
	var r := Control.new()
	r.theme = theme()
	r.size = Vector2(W, H)
	r.mouse_filter = Control.MOUSE_FILTER_IGNORE
	layer_node.add_child(r)
	return r
