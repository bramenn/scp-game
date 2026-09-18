extends SceneTree
## Chequeo de recorrido: camina hasta la puerta 1 (con tarjeta) y verifica el
## ciclo de ida y vuelta entre mapas.
## Uso: SCP_SKIP_TITLE=1 godot --headless --path . --script res://tools/walk_check.gd

var world
var f := 0
var fase := 0


func _initialize() -> void:
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _process(_d: float) -> bool:
	f += 1
	if f > 30 and world.listo and fase == 0:
		fase = -1
		world.st.give("tarjeta_1")  # la puerta 1 ahora pide tarjeta
		world._apply_doors()
		world.player.place(Vector2i(4, 5), "north")
		Input.action_press("ui_up")
	elif fase == -1 and world.map_id == "z-173" and not world.busy:
		fase = 1
		Input.action_release("ui_up")
		print("ida: mapa=", world.map_id, " tile=", world.player.tile)
		world.player.place(Vector2i(11, 13), "south")
		Input.action_press("ui_down")
	elif fase == 1 and world.map_id == "hub" and not world.busy:
		Input.action_release("ui_down")
		print("vuelta: mapa=", world.map_id, " tile=", world.player.tile)
		DirAccess.remove_absolute("user://partida.json")
		return true
	if f > 10000:
		printerr("FAIL: timeout en fase ", fase, " mapa=", world.map_id, " tile=", world.player.tile, " busy=", world.busy)
		return true
	return false
