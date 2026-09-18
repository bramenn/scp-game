extends SceneTree
## Chequeo integrado: puerta bloqueada, diálogo de Ortega (tarjeta), transición
## y recogida de objeto.
## Uso: SCP_SKIP_TITLE=1 godot --headless --path . --script res://tools/game_check.gd

var world
var f := 0
var fase := 0
var _kicked := false


func _initialize() -> void:
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _press_accept() -> void:
	var e := InputEventAction.new()
	e.action = "ui_accept"
	e.pressed = true
	Input.parse_input_event(e)


func _process(_d: float) -> bool:
	f += 1
	if f > 40 and f % 8 == 0:
		_press_accept()
	if f > 30 and world.listo and fase == 0 and not _kicked:
		_kicked = true
		world.player.place(Vector2i(4, 2), "north")
		Input.action_press("ui_up")
	elif _kicked and fase == 0 and world.busy:
		fase = 1
		Input.action_release("ui_up")
		print("puerta bloqueada sin tarjeta: mensaje=", world.hud._box.visible)
	elif fase == 1 and not world.busy:
		fase = 2
		world.player.place(Vector2i(19, 17), "south")
	elif fase == 2 and not world.busy and world.st.has("tiene:tarjeta_1") and world.st.has("tiene:botiquin"):
		fase = 3
		print("ortega entregó tarjeta_1 y botiquin: ", world.st.inv.get("tarjeta_1"), "/", world.st.inv.get("botiquin"))
		world.player.place(Vector2i(4, 5), "north")
		Input.action_press("ui_up")
	elif fase == 3 and world.map_id == "z-173" and not world.busy:
		fase = 4
		Input.action_release("ui_up")
		print("ida a la celda 173: tile=", world.player.tile)
		world.player.place(Vector2i(3, 10), "north")
		Input.action_press("ui_up")
	elif fase == 4 and world.st.has("tiene:doc_173") and not world.busy:
		Input.action_release("ui_up")
		print("objeto recogido: doc_173=", world.st.inv.get("doc_173"))
		DirAccess.remove_absolute("user://partida.json")
		return true
	if f > 10000:
		printerr("FAIL: timeout en fase ", fase, " mapa=", world.map_id, " tile=", world.player.tile, " busy=", world.busy)
		return true
	return false
