extends SceneTree
## Debug: place player, face, press E, print what happened.
var w
var f := 0
var args: Array
func _initialize() -> void:
	args = OS.get_cmdline_user_args()   # x y face
	w = load("res://scenes/main.tscn").instantiate()
	root.add_child(w)
func _press(a: String) -> void:
	var e := InputEventAction.new(); e.action = a; e.pressed = true; Input.parse_input_event(e)
	var r := InputEventAction.new(); r.action = a; r.pressed = false; Input.parse_input_event(r)
func _process(_d: float) -> bool:
	f += 1
	if f < 150 and w.busy > 0 and f % 10 == 0:
		_press("interact")
	if f == 150:
		w.player.place(Vector2i(int(args[0]), int(args[1])), args[2])
		print("placed at ", w.player.tile, " facing ", w.player.facing, " facing_tile=", w.player.facing_tile(), " interact_here=", w.interact_at.has(w.player.tile), " interact_face=", w.interact_at.has(w.player.facing_tile()), " busy=", w.busy)
		for a in w.actors:
			print("  actor ", a.get("npc_id"), " at ", a.tile)
	if f == 160:
		_press("interact")
	if f > 170 and f < 600 and w.dialog.arrow.visible and f % 12 == 0:
		print("  LINE: ", w.dialog.text_l.text.left(60))
		_press("interact")
	if f > 170 and f < 600 and w.dialog._choosing and f % 12 == 0:
		print("  CHOICE shown -> 0")
		_press("interact")
	if f > 170 and f % 30 == 0:
		print("   f=", f, " wait=", w.dialog._waiting, " vis=", w.dialog.text_l.visible_characters, " arrow=", w.dialog.arrow.visible, " busy=", w.busy, " paused=", paused)
	if f == 600:
		print("flags: ", w.st.flags.keys())
		return true
	return false
