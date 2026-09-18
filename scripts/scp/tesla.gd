extends ScpActor
## Tesla gate: two pylons across a corridor. Cycles OFF (safe) -> CHARGE (hum, sparks) -> ZAP.
## Being on the gate tiles during ZAP kills. spec: w (tiles across), v (vertical gate), period, phase.

var _t := 0.0
var _state := "off"
var _light: PointLight2D
var _arc: Line2D
var width := 3
var vertical := false


func init(a: Dictionary) -> void:
	spec = a
	width = int(a.get("w", 3))
	vertical = bool(a.get("v", false))
	tile = Vector2i(int(a.x), int(a.y))
	position = Actor.feet(tile)
	solid = false
	_t = float(a.get("phase", 0.0))
	for i in [0, width - 1]:
		var s := Sprite2D.new()
		s.texture = load("res://art/props/tesla_gate.png")
		s.centered = false
		var used := MapView.used_rect(s.texture)
		var o := Vector2(0, i * 16) if vertical else Vector2(i * 16, 0)
		s.offset = Vector2(-used.get_center().x, -used.end.y) + o / Vector2(0.5, 1.0)
		s.scale = Vector2(0.5, 1.0)
		s.z_index = 1 if vertical and i > 0 else 0
		add_child(s)
	_arc = Line2D.new()
	_arc.width = 1.5
	_arc.default_color = Color(0.6, 0.85, 1.0)
	_arc.visible = false
	add_child(_arc)
	_light = PointLight2D.new()
	_light.texture = PlayerActor.radial_texture()
	_light.texture_scale = 0.8
	_light.color = Color(0.5, 0.75, 1.0)
	_light.energy = 0.0
	_light.position = _span() * 0.5 + Vector2(0, -16)
	add_child(_light)
	Sfx.loop_at(self, "tesla", _span() * 0.5 + Vector2(0, -8), -14.0, 180.0)


func _span() -> Vector2:
	return Vector2(0, (width - 1) * 16.0) if vertical else Vector2((width - 1) * 16.0, 0)


## Bot/AI helper: the gate is dangerous right now (charging or firing).
func live_on(t: Vector2i) -> bool:
	return _state != "off" and _on_gate(t)


func idle() -> void:
	pass


func dread() -> float:
	return 0.3


func _on_gate(t: Vector2i) -> bool:
	if vertical:
		return t.x == tile.x and t.y >= tile.y and t.y < tile.y + width
	return t.y == tile.y and t.x >= tile.x and t.x < tile.x + width


func _process(dt: float) -> void:
	if not world or not world.player:
		return
	var period := float(spec.get("period", 4.0))
	_t = fmod(_t + dt, period)
	var phase := _t / period
	var new_state := "off" if phase < 0.55 else ("charge" if phase < 0.8 else "zap")
	if new_state != _state:
		_state = new_state
		if _state == "charge":
			Sfx.play_at(get_parent(), "spark", position, -6.0, 0.7, 260.0)
		elif _state == "zap":
			Sfx.play_at(get_parent(), "tesla", position, 2.0, 1.0, 400.0)
	match _state:
		"off":
			_arc.visible = false
			_light.energy = 0.0
		"charge":
			_light.energy = 0.3 + randf() * 0.2
			_arc.visible = randf() < 0.3
			_jitter(4.0)
		"zap":
			_light.energy = 1.6 + randf() * 0.4
			_arc.visible = true
			_jitter(8.0)
			if _on_gate(world.player.tile) and world.busy == 0 and not world._dying:
				kill("tesla", "tesla")


func _jitter(amp: float) -> void:
	_arc.clear_points()
	var n := width * 4
	for i in n + 1:
		var p := _span() * i / n + Vector2(0, -14)
		_arc.add_point(p + (Vector2(randf_range(-amp, amp), 0) if vertical else Vector2(0, randf_range(-amp, amp))))
