extends ScpActor
## SCP-173 "The Sculpture". Cannot move while observed (by the player, lit and in front,
## or by an SCP-131 pod). When unobserved it closes in along the grid in quick scraping
## lunges; next to the player while unobserved = neck snap. Frozen while you keep it in
## your light. It is contained when the flag spec.contain_flag is set (B03 seal).

const LUNGE := 0.06          # seconds per tile while you blink (~5 tiles per blink)
const CREEP := 0.3           # seconds per tile unseen with your eyes open (you walk at 0.22)
var _scrape_cd := 0.0
var _seen_last := true
var active := true


func init(a: Dictionary) -> void:
	super.init(a)
	shadow_size = 7.0
	var saved = world.st.flags.get("173_tile")
	if saved is Array:
		place(Vector2i(int(saved[0]), int(saved[1])))
	queue_redraw()


func on_map_leave() -> void:
	world.st.mark("173_tile", [tile.x, tile.y])


func observed() -> bool:
	if world.player_sees(tile):
		return true
	for a in world.actors:
		if a.has_method("watches") and a.watches(tile):
			return true
	return false


func wants_blink() -> bool:
	return active and dist_to_player() < 11.0 and world.los(world.player.tile, tile)


func dread() -> float:
	return 1.5 if wants_blink() else 0.0


func _process(dt: float) -> void:
	if not world or not world.player or world.busy > 0 or not active:
		return
	if world.st.has(String(spec.get("contain_flag", "scp173_contained"))):
		active = false
		return
	var seen := observed()
	if seen:
		if not _seen_last:
			Sfx.play_at(get_parent(), "click", position, -30.0)
		_seen_last = true
		return
	_seen_last = false
	if dist_to_player() > float(spec.get("range", 18)):
		return
	if adjacent_to_player():
		face_toward(world.player.tile)
		kill("173", "neck_snap")
		return
	if moving:
		return
	if path.is_empty() or path.back() != world.player.tile:
		go_to(world.player.tile)
	if path.size() > 0 and path[0] == world.player.tile:
		path.clear()
		return
	_scrape_cd -= dt
	if _scrape_cd <= 0.0:
		_scrape_cd = 0.6
		Sfx.play_at(get_parent(), "scrape", position, -2.0, randf_range(0.9, 1.1), 320.0)
	follow_path(LUNGE if world.blinking else CREEP)


## Doors don't stop it when it is unseen? They do: 173 cannot open doors (it goes around).
func step(d: String, dur := 0.22, run := false) -> bool:
	var ok := super.step(d, dur, run)
	idle()   # a statue never animates
	return ok


## Event hooks: "seal_173" closes the cell; sets scp173_contained if 173 is inside it.
func special(name: String, args: Array) -> bool:
	if name != "seal_173":
		return false
	var r := Rect2i(int(args[0]), int(args[1]), int(args[2]), int(args[3]))
	if r.has_point(tile):
		world.st.mark("scp173_contained")
		world.st.flags.erase("b02_cell_open")
		active = false
	else:
		world.st.mark("seal_failed")
	return true
