extends SceneTree
var w
var f := 0
func _initialize() -> void:
	w = load("res://scenes/main.tscn").instantiate()
	root.add_child(w)
func _press(a: String) -> void:
	var e := InputEventAction.new(); e.action = a; e.pressed = true; Input.parse_input_event(e)
	var r := InputEventAction.new(); r.action = a; r.pressed = false; Input.parse_input_event(r)
func _process(_d: float) -> bool:
	f += 1
	if f < 700 and w.busy > 0 and f % 10 == 0:
		_press("interact")
	if f % 100 == 0:
		print("f=", f, " busy=", w.busy, " running=", w.events.running, " dlg_wait=", w.dialog._waiting, " choosing=", w.dialog._choosing, " panel=", w.dialog.panel.visible, " arrow=", w.dialog.arrow.visible, " text=", w.dialog.text_l.text.left(30))
	if f == 700:
		print("busy before=", w.busy)
		w.player.place(Vector2i(2, 8), "west")
	if f == 720:
		Input.action_press("ui_left")
	if f == 820:
		Input.action_release("ui_left")
		var d = w.view.door_at.get(Vector2i(1, 8))
		print("door open=", d.is_open if d else "none", " player=", w.player.tile, " busy=", w.busy, " blocked=", w.view.blocked.has(Vector2i(1,8)))
		return true
	return false
