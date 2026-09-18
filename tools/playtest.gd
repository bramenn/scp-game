extends SceneTree
## Playtest bot: plays the real game through simulated input, following a route file.
##   SCP_SAVE=user://bot.json godot --path . --script res://tools/playtest.gd -- <route.json> [shots_dir]
## Route: [["map","A01"], ["talk"], ["go",x,y], ["face","north"], ["use"], ["pick",i], ["wait_map","A02"],
##         ["flag","name"], ["shot","name"], ["wait",sec], ["set","flag"], ["give","item",n]]
## Exit code 0 when the whole route completes, 1 on timeout/failure (with the step printed).

var world
var route: Array = []
var step := 0
var shots := ""
var t := 0.0
var step_t := 0.0
var _held := ""
var _last_tile := Vector2i(-99, -99)
var _stuck := 0.0
var failures := 0
var _pressed := false
var _step_map := ""
var _tries := 0


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	route = JSON.parse_string(FileAccess.get_file_as_string(a[0]))
	shots = a[1] if a.size() > 1 else ""
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _press(action: String) -> void:
	var e := InputEventAction.new()
	e.action = action
	e.pressed = true
	Input.parse_input_event(e)
	var r := InputEventAction.new()
	r.action = action
	r.pressed = false
	Input.parse_input_event(r)


func _hold(dir: String) -> void:
	if _held == dir:
		return
	if _held != "":
		Input.action_release(_held)
	_held = dir
	if dir != "":
		Input.action_press(dir)


func _log(msg: String) -> void:
	print("[bot %6.1fs] step %d %s: %s" % [t, step, JSON.stringify(route[step]) if step < route.size() else "-", msg])


func _next() -> void:
	_hold("")
	_step_map = ""
	step += 1
	step_t = 0.0
	_stuck = 0.0


func _process(dt: float) -> bool:
	t += dt
	step_t += dt
	if step >= route.size():
		print("[bot] ROUTE COMPLETE in %.1fs, map=%s" % [t, world.st.map if world.st else "?"])
		quit(0)
		return true
	if t > 1800.0 or step_t > 90.0:
		_log("TIMEOUT (map=%s tile=%s busy=%d)" % [world.st.map if world.st else "?", world.player.tile if world.player else "?", world.busy])
		quit(1)
		return true
	if not world.player or not world.st:
		return false
	if world.menu._reading:   # a document is open: read it, then close it
		if int(step_t * 10) % 8 == 0:
			_press("interact")
		return false
	var s: Array = route[step]
	var cmd: String = s[0]
	# dialogue / cutscene in progress: keep pressing E, pick choices when asked
	if world.dialog._choosing:
		if cmd in ["talk", "use"] and step + 1 < route.size() and route[step + 1][0] == "pick":
			_next()   # the choice arrived while we were still on the talk step
			return false
		if cmd == "pick":
			for i in int(s[1]):
				_press("ui_down")
			_press("interact")
			_log("picked %d" % int(s[1]))
			_next()
		elif step_t > 0.3:
			_press("interact")
		return false
	if world.busy > 0 and cmd in ["use", "talk"] and _pressed:
		_pressed = false
		_tries = 0
		_next()
		return false
	if world.busy > 0 and cmd not in ["wait_map", "wait"]:
		# advance dialogue only once a line is fully shown (avoids answering choices by accident)
		if world.dialog.arrow.visible and int(step_t * 10) % 3 == 0:
			_press("interact")
		return false
	match cmd:
		"go":
			var target := Vector2i(int(s[1]), int(s[2]))
			if _step_map == "":
				_step_map = world.st.map
			if world.st.map != _step_map:   # walked through an exit: the step is done
				_next()
				return false
			if world.player.moving:
				return false
			if world.player.tile == target:
				_next()
				return false
			# closed doors we can open count as walkable: we open them by bumping into them
			var opened: Array = []
			for dr in world.view.doors:
				if not dr.is_open and world.can_open(dr):
					for dtile in dr.tiles():
						world.astar.set_point_solid(dtile, false)
						opened.append(dtile)
			var blocked_by: Array = []
			if _stuck > 0.8:   # an actor is in the way: route around it
				for a in world.actors:
					if a.tile != target and not world.astar.is_point_solid(a.tile):
						world.astar.set_point_solid(a.tile, true)
						blocked_by.append(a.tile)
			var path: Array = world.find_path(world.player.tile, target, true)
			for bt in blocked_by:
				world.astar.set_point_solid(bt, false)
			for dtile in opened:
				world.astar.set_point_solid(dtile, true)
			if path.size() < 2:
				for dr in world.view.doors:
					print("   door ", dr.id, " open=", dr.is_open, " can=", world.can_open(dr), " solid=", world.astar.is_point_solid(dr.tile))
				_log("no path from %s to %s (busy=%d map=%s tgt_blocked=%s tgt_solid=%s region=%s)" % [world.player.tile, target, world.busy, world.st.map, world.view.blocked.has(target), world.astar.is_point_solid(target) if world.astar.region.has_point(target) else "out", world.astar.region])
				failures += 1
				quit(1)
				return true
			var d: Vector2i = path[1] - world.player.tile
			_hold({Vector2i.UP: "ui_up", Vector2i.DOWN: "ui_down", Vector2i.LEFT: "ui_left", Vector2i.RIGHT: "ui_right"}[d])
			if world.player.tile == _last_tile:
				_stuck += dt
				if _stuck > 6.0:
					_log("stuck at %s" % world.player.tile)
					quit(1)
					return true
			else:
				_stuck = 0.0
			_last_tile = world.player.tile
		"face":
			world.player.face(String(s[1]))
			_next()
		"talk_actor":  # walk next to the nearest talkable actor, face it, press E
			if world.player.moving:
				return false
			var best = null
			var bd := 1e9
			for a in world.actors:
				var want_pods: bool = s.size() > 1 and s[1] == "pods"
				if a.has_method("talk") and a.get("npc_id") != "nico" and a.has_method("watches") == want_pods:
					var dd: float = Vector2(a.tile - world.player.tile).length()
					if dd < bd:
						bd = dd
						best = a
			if best == null:
				_log("no talkable actor")
				_next()
				return false
			var diff: Vector2i = best.tile - world.player.tile
			if absi(diff.x) + absi(diff.y) == 1:
				_hold("")
				world.player.face(Actor.dir_name(diff))
				s[0] = "talk"
				_pressed = false
				step_t = 0.0
				return false
			var p2: Array = world.find_path(world.player.tile, best.tile)
			if p2.size() >= 2:
				var d2: Vector2i = p2[1] - world.player.tile
				if p2[1] != best.tile:
					_hold({Vector2i.UP: "ui_up", Vector2i.DOWN: "ui_down", Vector2i.LEFT: "ui_left", Vector2i.RIGHT: "ui_right"}[d2])
			else:
				_hold("")
		"use", "talk":
			if world.player.moving:
				return false
			if not _pressed and step_t > 0.2:
				_press("interact")
				_pressed = true
				_tries += 1
			elif _pressed and step_t > 0.2 + 0.7 * _tries:
				# nothing started (busy would have taken over above): retry a couple of times, then move on
				if _tries < 3:
					_pressed = false
				else:
					_log("WARNING: interaction produced nothing")
					_pressed = false
					_tries = 0
					_next()
			return false
		"step":  # walk one tile in a direction (to cross exits and doors)
			if step_t < 0.05:
				_hold({"north": "ui_up", "south": "ui_down", "west": "ui_left", "east": "ui_right"}[s[1]])
			elif not world.player.moving and step_t > 0.4:
				_next()
		"wait_map":
			_hold("")
			if world.st.map == s[1] and world.busy == 0:
				_next()
			elif world.busy > 0 and int(step_t * 10) % 3 == 0:
				_press("interact")
		"wait":
			if step_t >= float(s[1]):
				_next()
		"wait_actor_in":  # [cmd, x, y, w, h, timeout]: wait until a blink-type SCP is inside the rect
			var r := Rect2i(int(s[1]), int(s[2]), int(s[3]), int(s[4]))
			for a in world.actors:
				if a.has_method("wants_blink") and r.has_point(a.tile):
					_log("actor inside at %s" % a.tile)
					_next()
					return false
			if step_t > float(s[5]):
				_log("WARNING: actor never came in")
				_next()
		"sprint":
			if s[1]:
				Input.action_press("sprint")
			else:
				Input.action_release("sprint")
			_next()
		"flag":
			if world.st.has(String(s[1])):
				_log("ok")
			else:
				_log("FAILED: flag %s not set" % s[1])
				failures += 1
			_next()
		"set":
			world.st.mark(String(s[1]))
			world._refresh_doors()
			_next()
		"give":
			world.st.give(String(s[1]), int(s[2]) if s.size() > 2 else 1)
			world._refresh_doors()
			_next()
		"map":
			_next()
		"pick":   # the choice was already answered (or never came)
			_log("WARNING: no choice was pending")
			_next()
		"menu":
			_press("menu")
			_next()
		"shot":
			if step_t > 0.3 and shots != "":
				root.get_texture().get_image().save_png("%s/%s.png" % [shots, s[1]])
				_next()
			elif shots == "":
				_next()
		_:
			_log("unknown command")
			_next()
	return false
