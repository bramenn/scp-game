extends SceneTree
## Chequeo del final: combate contra el último SCP (682) y secuencia de cierre.
## Uso: SCP_SKIP_TITLE=1 godot --headless --path . --script res://tools/ending_check.gd

var world
var f := 0
var _kicked := false


func _initialize() -> void:
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _process(_d: float) -> bool:
	f += 1
	if f > 30 and world.listo and not _kicked:
		_kicked = true
		for id in ["scp-173", "scp-049", "scp-096", "scp-106"]:  # deja a 682 como último objetivo
			world.st.mark("contenido:" + id)
		world._enter_map("z-682", "hub")
		world._encounter(world.db.get_scp("scp-682"))
	if world.busy:  # el chequeo verifica el final, no el balance del jefe
		world.st.hp = 100
	if f > 60 and f % 8 == 0:
		var e := InputEventAction.new()
		e.action = "ui_accept"
		e.pressed = true
		Input.parse_input_event(e)
	if f > 120 and not world.busy:
		print("682 contenido=", world.st.contained("scp-682"), " final=", world.st.has("final"), " hp=", world.st.hp)
		print("objetivo en HUD: ", world.hud._goal.text)
		DirAccess.remove_absolute("user://partida.json")
		return true
	return f > 20000
