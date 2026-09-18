class_name Door
extends Node2D
## Sliding door. "h" doors fill a 2x2 gap in a horizontal (2-high) wall; "v" doors fill a
## 1x2 gap in a vertical wall. Blocks its tiles and casts a light shadow while closed.

const TILE := 16
const STYLES := ["std", "lab", "heavy", "rust"]

signal state_changed(door: Door)

var id := ""
var dir := "h"
var tile := Vector2i.ZERO
var level := 0            # keycard level required (0 = free)
var lock_flag := ""       # scripted lock: door stays shut while this flag is NOT set ("" = none)
var is_open := false
var _panels: Array[Sprite2D] = []
var _occ: LightOccluder2D
var _light: Sprite2D
var _body: Node2D


func setup(d: Dictionary, tex: Texture2D) -> void:
	id = d.get("id", "")
	dir = d.get("dir", "h")
	tile = Vector2i(int(d.x), int(d.y))
	level = int(d.get("level", 0))
	lock_flag = d.get("lock", "")
	# anchored at the bottom of the gap so it y-sorts with actors (drawn behind whoever is south)
	position = Vector2(tile.x * TILE, (tile.y + 2) * TILE)
	_body = Node2D.new()
	_body.position.y = -32
	add_child(_body)
	var row: int = maxi(0, STYLES.find(d.get("style", "std"))) * 32
	if dir == "h":
		var frame := Sprite2D.new()
		frame.texture = _region(tex, Rect2(0, row, 32, 32))
		frame.centered = false
		_body.add_child(frame)
		for i in 2:
			var p := Sprite2D.new()
			p.texture = _region(tex, Rect2(32 + i * 16, row, 16, 32))
			p.centered = false
			p.position.x = i * 16
			_body.add_child(p)
			_panels.append(p)
		_light = _led(Vector2(15, 1))
	else:
		var p := Sprite2D.new()
		p.texture = _region(tex, Rect2(64, row, 16, 32))
		p.centered = false
		_body.add_child(p)
		_panels.append(p)
		_light = _led(Vector2(7, -1))
	_occ = LightOccluder2D.new()
	var poly := OccluderPolygon2D.new()
	var r := Rect2(0, 2, 32, 4) if dir == "h" else Rect2(4, 0, 8, 32)
	poly.polygon = PackedVector2Array([r.position, Vector2(r.end.x, r.position.y), r.end, Vector2(r.position.x, r.end.y)])
	_occ.occluder = poly
	_body.add_child(_occ)


func _region(tex: Texture2D, r: Rect2) -> AtlasTexture:
	var a := AtlasTexture.new()
	a.atlas = tex
	a.region = r
	return a


func _led(at: Vector2) -> Sprite2D:
	var s := Sprite2D.new()
	var img := Image.create(2, 1, false, Image.FORMAT_RGBA8)
	img.fill(Color.WHITE)
	s.texture = ImageTexture.create_from_image(img)
	s.centered = false
	s.position = at
	_body.add_child(s)
	return s


func tiles() -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	if dir == "h":
		for y in 2:
			for x in 2:
				out.append(tile + Vector2i(x, y))
	else:
		out.append(tile)
		out.append(tile + Vector2i.DOWN)
	return out


func refresh_led(can_open: bool) -> void:
	_light.modulate = Color("5ec46a") if can_open else Color("d8403a")


func set_open(o: bool, instant := false) -> void:
	if o == is_open:
		return
	is_open = o
	_occ.visible = not o
	var tw := create_tween().set_parallel()
	var t := 0.0 if instant else 0.35
	if dir == "h":
		tw.tween_property(_panels[0], "position:x", -13.0 if o else 0.0, t)
		tw.tween_property(_panels[1], "position:x", 29.0 if o else 16.0, t)
		for p in _panels:  # panels slide into the wall: hide the part that is inside it
			tw.tween_property(p, "modulate:a", 0.0 if o else 1.0, t)
	else:
		tw.tween_property(_panels[0], "position:y", -28.0 if o else 0.0, t)
		tw.tween_property(_panels[0], "modulate:a", 0.0 if o else 1.0, t)
	state_changed.emit(self)
