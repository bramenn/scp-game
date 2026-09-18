class_name Vermin
extends Node2D
## Ambient life. One node per swarm (roaches, flies, moths, spiders) drawn procedurally,
## rats as animated sprites. They react to the player and to the flashlight beam.

const TILE := 16

var kind := ""
var world: World
var home := Vector2.ZERO
var radius := 48.0
var bugs: Array = []          # [{p: Vector2, v: Vector2, t: float, ...}]
var rat_sprite: AnimatedSprite2D
var _squeak_cd := 0.0


static func spawn(w: World, k: String, t: Vector2i, n: int, r: int) -> void:
	if k == "rat":
		for i in n:
			var v := Vermin.new()
			v.kind = "rat"
			v.world = w
			v.home = Vector2(t * TILE) + Vector2(8, 12)
			v.radius = r * TILE
			w.view.ents.add_child(v)
			v.position = v.home + Vector2(randf_range(-1, 1), randf_range(-1, 1)) * TILE * 0.5
			v._rat_setup()
		return
	var v := Vermin.new()
	v.kind = k
	v.world = w
	v.home = Vector2(t * TILE) + Vector2(8, 8)
	v.radius = r * TILE
	w.view.add_child(v)
	v.z_index = 16 if k in ["moth", "fly", "spider"] else 2
	for i in n:
		var p := v.home + Vector2(randf_range(-1, 1), randf_range(-1, 1)) * v.radius * 0.6
		v.bugs.append({"p": p, "v": Vector2.ZERO, "t": randf() * 3.0, "phase": randf() * TAU,
			"drop": randf_range(8, 30), "len": randf_range(0, 20)})
	if k == "fly":
		Sfx.loop_at(v, "flies", v.home - v.position, -14.0, 90.0)


# --------------------------------------------------------------------- rats

func _rat_setup() -> void:
	rat_sprite = AnimatedSprite2D.new()
	rat_sprite.sprite_frames = CharFrames.get_frames("rat")
	var fs := CharFrames.frame_size("rat")
	rat_sprite.centered = false
	rat_sprite.offset = Vector2(-fs.x / 2.0, -CharFrames.feet_y("rat") + 1)
	add_child(rat_sprite)
	bugs = [{"target": position, "wait": randf_range(0.5, 3.0), "speed": 18.0}]


func _free_at(p: Vector2) -> bool:
	var t := Vector2i(int(floor(p.x / TILE)), int(floor((p.y - 2) / TILE)))
	return not world.view.blocked.has(t)


func _lit_by_torch(p: Vector2) -> bool:
	var pl := world.player
	if not pl or pl.torch.energy < 0.3:
		return false
	var to := p - (pl.position + pl.torch.position)
	if to.length() > 150.0 * pl.torch.texture_scale:
		return false
	return absf(angle_difference(pl.torch.rotation, to.angle())) < deg_to_rad(PlayerActor.CONE_DEG)


func _rat(dt: float) -> void:
	var b: Dictionary = bugs[0]
	var pl := world.player
	_squeak_cd -= dt
	var scared: bool = pl and (pl.position.distance_to(position) < 56.0 or _lit_by_torch(position))
	if scared:
		var away := (position - pl.position).normalized()
		b.target = position + away.rotated(randf_range(-0.6, 0.6)) * 40.0
		b.speed = 75.0
		b.wait = 0.0
		if _squeak_cd <= 0.0:
			_squeak_cd = randf_range(2.0, 5.0)
			Sfx.play_at(get_parent(), "squeak", global_position, -10.0, randf_range(0.9, 1.3), 220.0)
	var to: Vector2 = b.target - position
	if to.length() < 2.0:
		b.wait -= dt
		var idle_a := "idle_" + String(rat_sprite.animation).get_slice("_", 1)
		if rat_sprite.sprite_frames.has_animation(idle_a):
			rat_sprite.play(idle_a)
		if b.wait <= 0.0:
			b.target = home + Vector2(randf_range(-1, 1), randf_range(-1, 1)) * radius
			b.speed = randf_range(14.0, 24.0)
			b.wait = randf_range(1.0, 5.0)
		return
	var nxt: Vector2 = position + to.normalized() * b.speed * dt
	if not _free_at(nxt):
		b.target = position
		return
	position = nxt
	var d := Actor.dir_name(Vector2i(signi(int(to.x)), 0) if absf(to.x) > absf(to.y) else Vector2i(0, signi(int(to.y))))
	if rat_sprite.sprite_frames.has_animation("walk_" + d):
		rat_sprite.play("walk_" + d)
	rat_sprite.speed_scale = b.speed / 18.0


# ------------------------------------------------------------------- swarms

func _process(dt: float) -> void:
	if not world or not world.player:
		return
	if kind == "rat":
		_rat(dt)
		return
	var pl := world.player
	for b in bugs:
		b.t += dt
		match kind:
			"roach":
				var flee: bool = _lit_by_torch(b.p) or b.p.distance_to(pl.position) < 30.0
				if flee:
					b.v = (b.p - pl.position).normalized().rotated(randf_range(-0.8, 0.8)) * 60.0
				elif b.t > randf_range(0.6, 2.5):
					b.t = 0.0
					b.v = Vector2.from_angle(randf() * TAU) * randf_range(0.0, 22.0)
				var np: Vector2 = b.p + b.v * dt
				if _free_at(np + Vector2(0, 2)) and np.distance_to(home) < radius * 1.6:
					b.p = np
				else:
					b.v = -b.v
				b.v *= 0.97
			"fly":
				b.phase += dt * 9.0
				b.p = home + Vector2(cos(b.phase * 0.7 + b.t), sin(b.phase * 1.1)) * 10.0 + \
					Vector2(randf_range(-1, 1), randf_range(-1, 1))
			"moth":
				var lamp := _nearest_light(home)
				b.phase += dt * randf_range(2.0, 4.0)
				b.p = lamp + Vector2(cos(b.phase), sin(b.phase * 1.3) * 0.6) * (8.0 + 4.0 * sin(b.t))
			"spider":
				var near: bool = pl.position.distance_to(b.p) < 40.0
				b.len = clampf(b.len + (-40.0 if near else 3.0) * dt, 0.0, b.drop)
	queue_redraw()


func _nearest_light(p: Vector2) -> Vector2:
	var best := p
	var bd := 1e9
	for l in world.lights:
		var d := l.position.distance_to(p)
		if d < bd:
			bd = d
			best = l.position
	return best


func _draw() -> void:
	match kind:
		"roach":
			for b in bugs:
				var p: Vector2 = (b.p - position).floor()
				draw_rect(Rect2(p, Vector2(2, 1)), Color("3a1f15"))
				draw_rect(Rect2(p + Vector2(0, -1), Vector2(1, 1)), Color("58301d"))
		"fly":
			for b in bugs:
				draw_rect(Rect2((b.p - position).floor(), Vector2(1, 1)), Color(0.05, 0.05, 0.05))
		"moth":
			for b in bugs:
				var p: Vector2 = (b.p - position).floor()
				var wing := 1 if int(b.t * 20.0) % 2 == 0 else 0
				draw_rect(Rect2(p, Vector2(1, 1)), Color("c4b89a"))
				draw_rect(Rect2(p + Vector2(-1, -wing), Vector2(1, 1)), Color("a09478"))
				draw_rect(Rect2(p + Vector2(1, -wing), Vector2(1, 1)), Color("a09478"))
		"spider":
			for b in bugs:
				var top: Vector2 = (b.p - position).floor() + Vector2(0, -34)
				var body := top + Vector2(0, b.len)
				draw_line(top, body, Color(0.8, 0.8, 0.85, 0.35))
				draw_rect(Rect2(body - Vector2(1, 1), Vector2(3, 3)), Color("101017"))
				var k := 1.0 if int(b.t * 4.0) % 2 == 0 else 0.0
				for i in 4:
					var yy := body.y - 1 + i
					draw_line(Vector2(body.x - 1, yy), Vector2(body.x - 4, yy - 1 + k), Color("101017"))
					draw_line(Vector2(body.x + 1, yy), Vector2(body.x + 4, yy - 1 + k), Color("101017"))
