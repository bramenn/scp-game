class_name Sign
extends Node2D
## Wall sign with localized text, drawn on a wall face tile. Styles: plate (grey metal),
## warn (yellow/black), scp (containment plate, white on dark red), exit (green), paper.

const STYLES := {
	"plate": [Color("878993"), Color("1a1a23"), Color("c3c5cb")],
	"warn": [Color("d6b441"), Color("101017"), Color("efd77a")],
	"scp": [Color("6a1419"), Color("e4e6e8"), Color("9a1f22")],
	"exit": [Color("3f5a25"), Color("e4e6e8"), Color("658a33")],
	"paper": [Color("d4cdb4"), Color("33333f"), Color("e4e6e8")],
	"zone": [Color("243a4c"), Color("e4e6e8"), Color("4f7089")],
}

var text = ""
var style := "plate"
static var _font: Font


func setup(d: Dictionary) -> void:
	text = d.text
	style = d.get("style", "plate")
	position = Vector2(int(d.x) * 16 + 8, int(d.y) * 16 + 5)
	if not _font:
		_font = load("res://art/font/Tiny5-Regular.ttf")
	Loc.changed.connect(queue_redraw)


func _draw() -> void:
	var s := Loc.t(text).to_upper()
	var tw := _font.get_string_size(s, HORIZONTAL_ALIGNMENT_LEFT, -1, 8).x
	var w := ceilf(tw) + 5
	var c: Array = STYLES.get(style, STYLES.plate)
	var r := Rect2(-floorf(w / 2.0), -4, w, 9)
	draw_rect(r.grow(1), Color(0, 0, 0, 0.55))
	draw_rect(r, c[0])
	draw_line(r.position, Vector2(r.end.x - 1, r.position.y), c[2])
	draw_string(_font, Vector2(r.position.x + 3, r.position.y + 7), s, HORIZONTAL_ALIGNMENT_LEFT, -1, 8, c[1])
