extends ScpActor
## SCP-096 "The Shy Guy". Sits facing the wall, crying. If you see its face - you are in front
## of it (its facing side), it is lit, you are looking at it - it screams, covers its face,
## then comes for you at impossible speed. Nothing stops it. Unless you reach it from BEHIND
## with the containment hood (item bag096) and use it: then it calms (flag scp096_bagged).

var state := "calm"   # calm | triggered | charging | bagged
var _cry: AudioStreamPlayer2D


func init(a: Dictionary) -> void:
	super.init(a)
	shadow_size = 7.0
	if world.st.has("scp096_bagged"):
		state = "bagged"
	_cry = Sfx.loop_at(self, "096_cry", Vector2(0, -16), -4.0, 220.0)


func dread() -> float:
	return 1.5 if state == "calm" else (6.0 if state != "bagged" else 0.0)


func _face_seen() -> bool:
	var fwd: Vector2i = Actor.DIRS[facing]
	var to: Vector2i = world.player.tile - tile
	# the player is on its face side (in front) and can see it
	return to.x * fwd.x + to.y * fwd.y > 0 and world.player_sees(tile)


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 or world._dying:
		return
	match state:
		"calm":
			if _face_seen():
				_trigger()
		"charging":
			if moving:
				return
			if adjacent_to_player():
				kill("096", "096_scream")
				return
			go_to(world.player.tile)
			if path.size() > 0 and path[0] == world.player.tile:
				path.clear()
				kill("096", "096_scream")
				return
			follow_path(0.09)


func _trigger() -> void:
	state = "triggered"
	world.busy += 1
	face_toward(world.player.tile)
	if _cry:
		_cry.stop()
	Sfx.play("096_scream", 2.0)
	Sfx.music("chase")
	world.hud.shake(world.cam, 2.5, 2.0)
	world.st.sanity = maxf(0.0, world.st.sanity - 25.0)
	await get_tree().create_timer(2.8).timeout
	world.busy -= 1
	state = "charging"


## Called by the event of using the hood from behind.
func try_bag() -> bool:
	if state != "calm":
		return false
	var behind: Vector2i = tile - Actor.DIRS[facing]
	if world.player.tile != behind or not world.st.has("item:bag096"):
		return false
	state = "bagged"
	if _cry:
		_cry.volume_db = -16.0
	return true


func talk() -> void:
	if state == "bagged":
		world.events.run("scp096_bagged_talk")
	elif try_bag():
		world.events.run("scp096_bag")
	else:
		world.events.run("scp096_touch")
