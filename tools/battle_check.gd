extends SceneTree
## Combate completo automático (siempre elige DISPARAR): verifica que termina sin errores.
## Uso: SCP_SKIP_TITLE=1 godot --headless --path . --script res://tools/battle_check.gd

var world
var f := 0
var _started := false


func _initialize() -> void:
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _process(_d: float) -> bool:
	f += 1
	if f > 30 and world.listo and not _started:
		_started = true
		world._enter_map("z-173", "hub")
		world._encounter(world.db.get_scp("scp-173"))
	if f > 60 and f % 8 == 0:
		var e := InputEventAction.new()
		e.action = "ui_accept"
		e.pressed = true
		Input.parse_input_event(e)
	if f > 120 and not world.busy:
		print("fin del combate en mapa=", world.map_id, " hp=", world.st.hp, " contenido=", world.st.contained("scp-173"))
		DirAccess.remove_absolute("user://partida.json")
		return true
	return f > 6000
