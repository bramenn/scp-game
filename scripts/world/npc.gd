class_name NpcActor
extends Actor
## Story NPC. Talking runs the first matching entry of npcs.json "talk": [[cond, event], ...].
## Behaviours (spot.mode or flag "follow:<id>"): idle (looks around), pace, cower, follow.

var npc_id := ""
var info: Dictionary = {}
var spot: Dictionary = {}
var solid := true
var _look_t := 0.0
var _trail: Array[Vector2i] = []


func _ready() -> void:
	shadow_size = 5.5
	queue_redraw()
	if world and world.player:
		world.player.stepped.connect(_on_player_step)


func talk() -> void:
	if not world or world.busy > 0:
		return
	face_toward(world.player.tile)
	for entry in info.get("talk", []):
		if world.st.check(entry[0]):
			world.events.run(String(entry[1]), npc_id)
			return


func following() -> bool:
	return world.st.has("follow:" + npc_id)


func _on_player_step(t: Vector2i) -> void:
	_trail.append(t)
	if _trail.size() > 6:
		_trail.pop_front()


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 and not following():
		return
	if following():
		_follow()
		return
	if not path.is_empty():
		follow_path(0.28)
		return
	match String(spot.get("mode", "idle")):
		"idle":
			_look_t -= dt
			if _look_t <= 0.0:
				_look_t = randf_range(2.5, 7.0)
				if world.player.position.distance_to(position) < 64.0:
					face_toward(world.player.tile)
				else:
					face(["south", "east", "west", "north", "south"].pick_random())
		"cower":
			face(String(spot.get("face", "north")))
		"pace":
			_look_t -= dt
			if _look_t <= 0.0 and path.is_empty():
				_look_t = randf_range(3.0, 6.0)
				var pts: Array = spot.get("points", [])
				if pts.size() > 0:
					var p: Array = pts.pick_random()
					go_to(Vector2i(int(p[0]), int(p[1])))


func _follow() -> void:
	if moving or _trail.size() < 2:
		return
	var target: Vector2i = _trail[_trail.size() - 2]
	if target == tile or world.player.tile.distance_squared_to(tile) <= 1:
		return
	var d := target - tile
	if absi(d.x) + absi(d.y) == 1:
		step(dir_name(d), 0.2)
	else:
		go_to(target)
		follow_path(0.18)
