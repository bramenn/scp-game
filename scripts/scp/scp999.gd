extends ScpActor
## SCP-999 "The Tickle Monster". A happy orange blob that bounces toward you, gurgles and
## makes you feel better. Talking to it restores sanity (once per visit, more with candy).

var _t := 0.0
var _home := Vector2i.ZERO


func init(a: Dictionary) -> void:
	spec = a
	var s := Sprite2D.new()
	s.texture = load("res://art/props/scp999.png")
	s.centered = false
	var used := MapView.used_rect(s.texture)
	s.offset = Vector2(-used.get_center().x, -used.end.y)
	add_child(s)
	tile = Vector2i(int(a.x), int(a.y))
	_home = tile
	position = Actor.feet(tile)
	shadow_size = 9.0
	var l := PointLight2D.new()
	l.texture = PlayerActor.radial_texture()
	l.texture_scale = 0.3
	l.energy = 0.5
	l.color = Color(1.0, 0.6, 0.25)
	l.position = Vector2(0, -8)
	add_child(l)
	queue_redraw()


func idle() -> void:
	pass


func _process(dt: float) -> void:
	_t += dt
	var s: Sprite2D = get_child(0)
	var sq := absf(sin(_t * 5.0))
	s.scale = Vector2(1.0 + 0.08 * (1.0 - sq), 0.92 + 0.08 * sq)
	if not world or not world.player or moving or adjacent_to_player():
		return
	if dist_to_player() > 2.0 and dist_to_player() < 9.0 and randf() < dt * 1.5:
		go_to(world.player.tile)
		if path.size() > 1:
			path.resize(1)
		follow_path(0.3)
		if randf() < 0.3:
			Sfx.play_at(get_parent(), "squelch", position, -10.0, 1.6, 200.0)


func talk() -> void:
	world.events.run("scp999_talk")
