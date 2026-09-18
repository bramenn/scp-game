extends ScpActor
## SCP-106 "The Old Man". Emerges from the floor, walks straight through walls toward you,
## slowly, leaving corrosion. Light hurts it: hold your flashlight on it and it sinks back
## into the floor. If it reaches you, it drags you into its pocket dimension (map F01).
## spec: delay (s before emerging), active_flag (only hunts while set), gone_flag.

var state := "hidden"   # hidden | rising | hunting | sinking
var _t := 0.0
var _lit := 0.0
var _trail := 0.0


func init(a: Dictionary) -> void:
	super.init(a)
	solid = false
	visible = false
	_t = float(a.get("delay", 6.0))
	shadow_size = 7.0


func dread() -> float:
	return 3.0 if state == "hunting" else 0.0


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 or world._dying:
		return
	if spec.has("gone_flag") and world.st.has(String(spec.gone_flag)):
		visible = false
		return
	if spec.has("active_flag") and not world.st.check(String(spec.active_flag)):
		return
	_t -= dt
	match state:
		"hidden":
			if _t <= 0.0:
				_emerge()
		"hunting":
			if world.player_sees(tile) and world.player.torch.energy > 0.3 and dist_to_player() < 7.0:
				_lit += dt
				modulate = Color(1.3, 1.3, 1.3) if int(_lit * 10) % 2 == 0 else Color.WHITE
				if _lit > 1.6:
					_sink(randf_range(14.0, 24.0))
				return
			_lit = maxf(0.0, _lit - dt)
			modulate = Color.WHITE
			if adjacent_to_player() or tile == world.player.tile:
				_grab()
				return
			if not moving:
				var d: Vector2i = world.player.tile - tile
				var dir := Actor.dir_name(Vector2i(signi(d.x), 0) if absi(d.x) > absi(d.y) else Vector2i(0, signi(d.y)))
				_walk(dir)


func _walk(d: String) -> void:
	facing = d
	moving = true
	tile += Actor.DIRS[d]
	if sprite.sprite_frames.has_animation("walk_" + d):
		sprite.play("walk_" + d)
	var tw := create_tween()
	tw.tween_property(self, "position", Actor.feet(tile), 0.75)
	tw.finished.connect(func() -> void: moving = false)
	_trail += 1.0
	if int(_trail) % 2 == 0 and not world.view.is_wall(tile):
		world.view._put_trace(["corrosion", "corrosion2", "corrosion_trail"].pick_random(), tile)
	if randf() < 0.3:
		Sfx.play_at(get_parent(), "squelch", position, -6.0, randf_range(0.7, 0.9), 300.0)


func _emerge() -> void:
	state = "rising"
	var spots: Array = []
	for r in range(6, 10):
		for d in [Vector2i(r, 0), Vector2i(-r, 0), Vector2i(0, r), Vector2i(0, -r)]:
			var t: Vector2i = world.player.tile + d
			if not world.view.blocked.has(t):
				spots.append(t)
	if spots.is_empty():
		state = "hidden"
		_t = 5.0
		return
	place(spots.pick_random())
	visible = true
	world.view._put_trace("corrosion2", tile)
	Sfx.play("106_emerge", -2.0)
	modulate.a = 0.0
	var tw := create_tween()
	tw.tween_property(self, "modulate:a", 1.0, 1.6)
	await tw.finished
	Sfx.play_at(get_parent(), "106_laugh", position, 0.0, 1.0, 500.0)
	state = "hunting"


func _sink(next: float) -> void:
	state = "sinking"
	Sfx.play_at(get_parent(), "squelch", position, 0.0, 0.6, 400.0)
	var tw := create_tween()
	tw.tween_property(self, "modulate:a", 0.0, 1.0)
	await tw.finished
	visible = false
	state = "hidden"
	_t = next
	_lit = 0.0


func _grab() -> void:
	state = "sinking"
	world.busy += 1
	Sfx.play("106_laugh", 2.0)
	world.hud.shake(world.cam, 1.2, 3.0)
	await world.hud.flash(2, Color(0.1, 0.05, 0.05))
	world.st.mark("taken_by_106")
	world.st.hp = maxf(10.0, world.st.hp - 20.0)
	world.busy -= 1
	await world.load_map("F01", "start")
