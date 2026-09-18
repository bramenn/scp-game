class_name Chaser
extends ScpActor
## Hostile that wanders and chases the player on sight (or sound). Touching it starts a
## turn-based battle (spec.battle). Winning removes it for good (flag dead:<map>:<x>_<y>).
## spec: sprite, battle, speed (s/tile chasing), sight (tiles), hears (bool), voice (event lines)

var home := Vector2i.ZERO
var chasing := false
var _think := 0.0
var _lost := 0.0
var _heard := Vector2i(-1, -1)
var _groan := 0.0
var key := ""
var _grace := 2.5   # seconds after the map loads before it can start a fight


func init(a: Dictionary) -> void:
	super.init(a)
	home = tile
	key = "dead:%s:%d_%d" % [world.st.map, int(a.x), int(a.y)]
	if world.st.has(key):
		call_deferred("remove")


func wants_blink() -> bool:
	return false


func dread() -> float:
	return 1.0 if chasing else 0.2


func hear(t: Vector2i, radius: int) -> void:
	if spec.get("hears", false) and Vector2(t - tile).length() <= radius * float(spec.get("ears", 1.0)):
		_heard = t


func _sees_player() -> bool:
	var d: Vector2i = world.player.tile - tile
	if d.length() > float(spec.get("sight", 6)):
		return false
	if spec.get("blind", false):
		return d.length() <= 1.5
	return world.los(tile, world.player.tile)


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 or world._dying:
		return
	_grace -= dt
	if adjacent_to_player() and not moving and _grace <= 0.0:
		_attack()
		return
	_groan -= dt
	if _groan <= 0.0:
		_groan = randf_range(4.0, 10.0)
		if spec.has("groan"):
			Sfx.play_at(get_parent(), String(spec.groan), position, -8.0, randf_range(0.8, 1.1), 260.0)
	if moving:
		return
	_think -= dt
	if _sees_player():
		chasing = true
		_lost = 4.0
	elif chasing:
		_lost -= dt
		if _lost <= 0.0:
			chasing = false
	if chasing:
		if _think <= 0.0 or path.is_empty():
			_think = 0.4
			go_to(world.player.tile)
		if path.size() > 0 and path[0] == world.player.tile:
			path.clear()
		follow_path(float(spec.get("speed", 0.34)))
	elif _heard.x >= 0:
		go_to(_heard)
		_heard = Vector2i(-1, -1)
		follow_path(float(spec.get("speed", 0.34)))
	elif not path.is_empty():
		follow_path(0.5)
	elif _think <= 0.0:
		_think = randf_range(2.0, 5.0)
		var r := int(spec.get("wander", 4))
		var t := home + Vector2i(randi_range(-r, r), randi_range(-r, r))
		if not world.view.blocked.has(t):
			go_to(t)


func _attack() -> void:
	face_toward(world.player.tile)
	world.busy += 1
	if spec.has("attack_sfx"):
		Sfx.play(String(spec.attack_sfx), 0.0)
	await world.hud.flash(2, Color(0.5, 0, 0))
	world.busy -= 1
	var res: String = await world.battle(String(spec.get("battle", "zombie")))
	_grace = 3.0   # time to get away before it can bite again
	if res == "win":
		world.st.mark(key)
		var tw := create_tween()
		tw.tween_property(self, "modulate:a", 0.0, 0.6)
		tw.tween_callback(remove)
	elif res == "flee":
		chasing = false
		_think = 3.0
		place(home)
