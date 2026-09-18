extends ScpActor
## SCP-049 "The Plague Doctor". Walks its route through the medical wing. It does not
## chase: it approaches, and it talks. Its touch kills. The recontainment is a
## conversation (events), then it follows you back to its cell (flag follow049).

var _t := 0.0
var _hum := 0.0


func init(a: Dictionary) -> void:
	super.init(a)
	shadow_size = 6.5


func dread() -> float:
	return 2.0


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 or world._dying:
		return
	if world.st.has(String(spec.get("gone_flag", "scp049_contained"))):
		return
	_hum -= dt
	if _hum <= 0.0:
		_hum = randf_range(8.0, 14.0)
		Sfx.play_at(get_parent(), "049_hum", position, -4.0, 1.0, 320.0)
	if moving:
		return
	if world.st.has("follow049"):
		if dist_to_player() > 1.5:
			go_to(world.player.tile)
			if path.size() > 0 and path[0] == world.player.tile:
				path.clear()
			follow_path(0.3)
		return
	if adjacent_to_player() and not world.st.has("talked049_now"):
		world.st.mark("talked049_now")
		face_toward(world.player.tile)
		world.events.run(String(spec.get("event", "scp049_meet")))
		return
	_t -= dt
	if dist_to_player() < 6.0 and world.los(tile, world.player.tile):
		if _t <= 0.0:
			_t = 0.9
			go_to(world.player.tile)
			if path.size() > 0 and path[0] == world.player.tile:
				path.clear()
		follow_path(0.55)
	elif _t <= 0.0:
		_t = randf_range(3.0, 6.0)
		var pts: Array = spec.get("route", [])
		if pts.size() > 0:
			var p: Array = pts.pick_random()
			go_to(Vector2i(int(p[0]), int(p[1])))
	else:
		follow_path(0.6)


func talk() -> void:
	world.events.run(String(spec.get("event", "scp049_meet")))
