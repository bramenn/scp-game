extends SceneTree
## Capturas de interacciones: diálogo de Ortega, puerta bloqueada, inventario.
##   godot --path . --script res://tools/shots_extra.gd -- <dir>

var world
var f := 0
var out := "user://"


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		out = args[0]
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _press() -> void:
	var e := InputEventAction.new()
	e.action = "ui_accept"
	e.pressed = true
	Input.parse_input_event(e)


func _key(code: Key) -> void:
	var k := InputEventKey.new()
	k.physical_keycode = code
	k.pressed = true
	Input.parse_input_event(k)


func _shot(name: String) -> void:
	root.get_texture().get_image().save_png("%s/%s.png" % [out, name])


func _process(_d: float) -> bool:
	f += 1
	if f == 40:
		world.player.place(Vector2i(19, 17), "south")  # frente al Sgto. Ortega
		_press()
	elif f == 120:
		_shot("npc-dialogo")
	elif f > 130 and f % 8 == 0 and world.busy:
		_press()  # avanza el diálogo de Ortega
	elif f == 250:
		world.player.place(Vector2i(4, 2), "north")
		Input.action_press("ui_up")
	elif f == 320:
		_shot("puerta-bloqueada")
	elif f == 330 or f == 340:
		_press()  # cierra el aviso
		Input.action_release("ui_up")
	elif f == 360:
		_key(KEY_I)  # abre el inventario
	elif f == 430:
		_shot("inventario")
	elif f == 440:
		_key(KEY_I)
		_press()
	elif f == 480:
		DirAccess.remove_absolute("user://partida.json")
		return true
	if f > 5000:
		printerr("FAIL: timeout")
		return true
	return false
