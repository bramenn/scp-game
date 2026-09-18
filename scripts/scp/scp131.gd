extends ScpActor
## SCP-131-A/B "Eye Pods". Bond with the player (flag bond131) and follow them everywhere,
## wheeling close behind. They never blink: anything they look at can't move unseen (173).
## They panic (shake, babble) when a dangerous anomaly is near.

var _t := 0.0
var _babble := 0.0
var offset := 0


func init(a: Dictionary) -> void:
	spec = a
	offset = int(a.get("offset", 0))
	var s := Sprite2D.new()
	s.texture = load("res://art/props/%s.png" % a.get("sprite", "scp131a"))
	s.centered = false
	var used := MapView.used_rect(s.texture)
	s.offset = Vector2(-used.get_center().x, -used.end.y)
	add_child(s)
	sprite = null
	tile = Vector2i(int(a.x), int(a.y))
	position = Actor.feet(tile)
	shadow_size = 3.5
	solid = false
	queue_redraw()


func idle() -> void:
	pass


func watches(t: Vector2i) -> bool:
	if world.st.has("pods_stay"):   # told to stay: they hide and tremble, eyes shut tight against the console
		return false
	return Vector2(t - tile).length() < 8.0 and world.los(tile, t)


func _process(dt: float) -> void:
	if not world or not world.player:
		return
	_t += dt
	var bonded: bool = world.st.has("bond131")
	var danger := false
	for a in world.actors:
		if a.has_method("wants_blink") and a.wants_blink():
			danger = true
	var s: Sprite2D = get_child(0)
	s.position.x = sin(_t * 40.0) * 1.0 if danger else 0.0
	s.position.y = -absf(sin(_t * 6.0 + offset)) * 1.5
	_babble -= dt
	if _babble <= 0.0:
		_babble = randf_range(4.0, 9.0) if not danger else randf_range(1.0, 2.0)
		Sfx.play_at(get_parent(), "squeak", position, -16.0 if not danger else -8.0, randf_range(1.6, 2.2), 200.0)
	if not bonded or moving or world.st.has("pods_stay"):
		return
	var goal: Vector2i = world.player.tile - Actor.DIRS[world.player.facing] * (1 + offset)
	if tile.distance_squared_to(world.player.tile) <= 2 + offset * 2:
		return
	if not world.view.blocked.has(goal):
		go_to(goal)
	else:
		go_to(world.player.tile)
	if path.size() > 0 and path[0] == world.player.tile:
		path.clear()
	follow_path(0.1)


func step(d: String, dur := 0.22, run := false) -> bool:
	if moving:
		return false
	var target: Vector2i = tile + Actor.DIRS[d]
	if world.view.blocked.has(target):
		return false
	moving = true
	tile = target
	var tw := create_tween()
	tw.tween_property(self, "position", Actor.feet(target), dur)
	tw.finished.connect(func() -> void: moving = false)
	return true


func talk() -> void:
	world.events.run("scp131_talk")
