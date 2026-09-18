class_name FxEmitter
extends Node2D
## Small environmental effects placed by maps: steam, drip, sparks, smoke, acid, ash.
## Drips and sparks also make positional sounds.

var kind := ""
var _t := 0.0
var _period := 1.0


static func make(d: Dictionary) -> FxEmitter:
	var e := FxEmitter.new()
	e.kind = String(d.kind)
	e.position = Vector2(int(d.x) * 16 + 8, int(d.y) * 16 + 8)
	e._build(d)
	return e


func _particles() -> CPUParticles2D:
	var p := CPUParticles2D.new()
	p.local_coords = false
	add_child(p)
	return p


func _ramp(a: Color, b: Color) -> Gradient:
	var g := Gradient.new()
	g.set_color(0, a)
	g.set_color(1, b)
	return g


func _build(d: Dictionary) -> void:
	match kind:
		"steam", "smoke":
			var p := _particles()
			p.amount = 26
			p.lifetime = 2.6
			p.direction = Vector2(0, -1) if kind == "steam" else Vector2(0.3, -1)
			p.spread = 18.0
			p.gravity = Vector2(4, -6)
			p.initial_velocity_min = 8.0
			p.initial_velocity_max = 16.0
			p.scale_amount_min = 2.0
			p.scale_amount_max = 5.0
			var c := Color(0.85, 0.88, 0.9, 0.35) if kind == "steam" else Color(0.2, 0.2, 0.22, 0.45)
			p.color_ramp = _ramp(c, Color(c.r, c.g, c.b, 0.0))
			p.z_index = 17
			if kind == "steam":
				_period = 0.0
		"drip":
			_period = float(d.get("every", randf_range(1.2, 2.8)))
		"sparks":
			var p := _particles()
			p.amount = 14
			p.lifetime = 0.5
			p.one_shot = true
			p.explosiveness = 0.9
			p.emitting = false
			p.direction = Vector2(0, 1)
			p.spread = 70.0
			p.gravity = Vector2(0, 220)
			p.initial_velocity_min = 30.0
			p.initial_velocity_max = 70.0
			p.color_ramp = _ramp(Color(1, 0.95, 0.6, 1), Color(1, 0.4, 0.1, 0))
			p.material = CanvasItemMaterial.new()
			(p.material as CanvasItemMaterial).light_mode = CanvasItemMaterial.LIGHT_MODE_UNSHADED
			p.z_index = 18
			var l := PointLight2D.new()
			l.texture = PlayerActor.radial_texture()
			l.texture_scale = 0.4
			l.energy = 0.0
			l.color = Color(1, 0.8, 0.4)
			add_child(l)
			_period = randf_range(2.0, 6.0)
		"acid":
			var p := _particles()
			p.amount = 10
			p.lifetime = 1.4
			p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
			p.emission_rect_extents = Vector2(7, 5)
			p.direction = Vector2(0, -1)
			p.spread = 10.0
			p.gravity = Vector2(0, -8)
			p.initial_velocity_min = 2.0
			p.initial_velocity_max = 6.0
			p.color_ramp = _ramp(Color(0.8, 0.95, 0.35, 0.8), Color(0.6, 0.8, 0.2, 0))
			var l := PointLight2D.new()
			l.texture = PlayerActor.radial_texture()
			l.texture_scale = 0.35
			l.energy = 0.55
			l.color = Color(0.6, 1.0, 0.3)
			add_child(l)
		"ash":
			var p := _particles()
			p.amount = 20
			p.lifetime = 6.0
			p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
			p.emission_rect_extents = Vector2(60, 40)
			p.gravity = Vector2(2, 4)
			p.color = Color(0.3, 0.3, 0.32, 0.8)
		"mist":
			var p := _particles()
			p.amount = 16
			p.lifetime = 7.0
			p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
			p.emission_rect_extents = Vector2(float(d.get("w", 4)) * 8, float(d.get("h", 3)) * 8)
			p.gravity = Vector2(1.5, -0.5)
			p.scale_amount_min = 6.0
			p.scale_amount_max = 12.0
			p.color_ramp = _ramp(Color(0.8, 0.85, 0.9, 0.12), Color(0.8, 0.85, 0.9, 0.0))
			p.z_index = 17


func _process(dt: float) -> void:
	if _period <= 0.0:
		return
	_t += dt
	if _t < _period:
		return
	_t = 0.0
	match kind:
		"drip":
			_drip()
		"sparks":
			_period = randf_range(1.5, 7.0)
			var p: CPUParticles2D = get_child(0)
			p.restart()
			var l: PointLight2D = get_child(1)
			l.energy = 1.2
			create_tween().tween_property(l, "energy", 0.0, 0.25)
			Sfx.play_at(get_parent(), "spark", global_position, -8.0, randf_range(0.8, 1.2), 200.0)


func _drip() -> void:
	var drop := ColorRect.new()
	drop.size = Vector2(1, 2)
	drop.color = Color(0.7, 0.8, 0.9, 0.8)
	drop.position = Vector2(0, -26)
	add_child(drop)
	var tw := create_tween()
	tw.tween_property(drop, "position:y", 0.0, 0.35).set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_QUAD)
	tw.tween_callback(func() -> void:
		drop.queue_free()
		_ring()
		Sfx.play_at(get_parent(), "drip", global_position, -12.0, randf_range(0.8, 1.3), 180.0))


func _ring() -> void:
	var r := Line2D.new()
	r.width = 1.0
	r.default_color = Color(0.7, 0.8, 0.9, 0.6)
	for i in 13:
		var a := TAU * i / 12.0
		r.add_point(Vector2(cos(a) * 1.0, sin(a) * 0.5))
	add_child(r)
	var tw := create_tween().set_parallel()
	tw.tween_property(r, "scale", Vector2(5, 5), 0.6)
	tw.tween_property(r, "modulate:a", 0.0, 0.6)
	tw.chain().tween_callback(r.queue_free)
