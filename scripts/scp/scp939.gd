extends Chaser
## SCP-939 "With Many Voices". Blind, hunts by sound (sprinting is loud). Every so often it
## speaks with the voice of someone it killed: a line of text floats up in the dark.

var _talk := 0.0


func init(a: Dictionary) -> void:
	a = a.duplicate()
	a.merge({"sprite": "scp939", "battle": "939", "blind": true, "hears": true, "ears": 1.3, "speed": 0.26,
		"sight": 2, "wander": 5, "groan": "939_call", "shadow": 9.0}, false)
	super.init(a)


func dread() -> float:
	return 2.0 if chasing else 0.8


func _process(dt: float) -> void:
	super._process(dt)
	if not world or not world.player:
		return
	_talk -= dt
	if _talk <= 0.0 and dist_to_player() < 14.0:
		_talk = randf_range(7.0, 14.0)
		var lines: Array = Db.story.get("voices939", [])
		if lines.size() > 0:
			var avail: Array = lines.filter(func(v): return world.st.check(v.get("cond", "")))
			if avail.size() > 0:
				_float(Loc.t(avail.pick_random().text))


func _float(text: String) -> void:
	var l := UiKit.label(text, 8, Color(0.85, 0.8, 0.8, 0.9))
	l.position = Vector2(-60, -52)
	l.size = Vector2(120, 10)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	l.z_index = 25
	add_child(l)
	Sfx.play_at(get_parent(), "939_call", position, -4.0, randf_range(0.9, 1.1), 400.0)
	var tw := l.create_tween()
	tw.tween_property(l, "position:y", -70.0, 3.0)
	tw.parallel().tween_property(l, "modulate:a", 0.0, 3.0).set_delay(1.5)
	tw.tween_callback(l.queue_free)
