extends ScpActor
## SCP-529 "Josie the Half-Cat". Wanders, purrs, ignores you. With the flag follow_josie she
## trots after you (across maps). spec.event runs when you talk to her.

var _t := 0.0
var home := Vector2i.ZERO


func init(a: Dictionary) -> void:
	super.init(a)
	home = tile
	shadow_size = 3.5
	solid = false


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 or moving:
		return
	_t -= dt
	if world.st.has("follow_josie"):
		if dist_to_player() > 1.5:
			go_to(world.player.tile)
			if path.size() > 0 and path[0] == world.player.tile:
				path.clear()
			follow_path(0.2)
		return
	if not path.is_empty():
		follow_path(0.35)
	elif _t <= 0.0:
		_t = randf_range(2.0, 6.0)
		var t := home + Vector2i(randi_range(-3, 3), randi_range(-2, 2))
		if not world.view.blocked.has(t):
			go_to(t)


func talk() -> void:
	face_toward(world.player.tile)
	world.events.run(String(spec.get("event", "josie_talk")))
