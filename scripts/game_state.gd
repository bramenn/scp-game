class_name GameState
extends RefCounted
## Estado de la partida: posición, vida, inventario y banderas de historia. Se guarda en JSON.

const SAVE_PATH := "user://partida.json"
const BASE := {"hp": 100, "atk": 14, "def": 8, "spd": 12}

var map := "hub"
var tile := Vector2i(-1, -1)
var hp: int = BASE.hp
var inv: Dictionary = {}   # id -> cantidad
var flags: Array = []      # "contenido:scp-173", "tomado:hub:I", "hablo:dclass"...


func has(flag: String) -> bool:
	if flag.begins_with("tiene:"):
		return inv.get(flag.substr(6), 0) > 0
	return flag in flags


func mark(flag: String) -> void:
	if flag not in flags:
		flags.append(flag)


func give(id: String, n := 1) -> void:
	inv[id] = inv.get(id, 0) + n


func take(id: String) -> void:
	inv[id] = inv.get(id, 0) - 1
	if inv[id] <= 0:
		inv.erase(id)


func stat(name: String, items: Dictionary) -> int:
	var v: int = BASE[name]
	for id in inv:
		v += int(items.get(id, {}).get(name, 0))
	return v


func card_level() -> int:
	for lvl in range(5, 0, -1):
		if has("tiene:tarjeta_%d" % lvl):
			return lvl
	return 0


func contained(scp_id: String) -> bool:
	return has("contenido:" + scp_id)


func next_target(order: Array) -> String:
	for id in order:
		if not contained(id):
			return id
	return ""


## Primer diálogo cuyas condiciones se cumplen: "si" = todas presentes, "no" = todas ausentes.
func pick_dialog(dialogs: Array) -> Dictionary:
	for d in dialogs:
		var ok := true
		for f in d.get("si", []):
			ok = ok and has(f)
		for f in d.get("no", []):
			ok = ok and not has(f)
		if ok:
			return d
	return {}


func save() -> void:
	var f := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	f.store_string(JSON.stringify({"map": map, "tile": [tile.x, tile.y], "hp": hp, "inv": inv, "flags": flags}))


static func exists() -> bool:
	return FileAccess.file_exists(SAVE_PATH)


static func load_saved() -> GameState:
	var d = JSON.parse_string(FileAccess.get_file_as_string(SAVE_PATH))
	var s := GameState.new()
	if d is Dictionary:
		s.map = d.get("map", "hub")
		s.tile = Vector2i(int(d.tile[0]), int(d.tile[1]))
		s.hp = int(d.get("hp", BASE.hp))
		for k in d.get("inv", {}):
			s.inv[k] = int(d.inv[k])
		s.flags = d.get("flags", [])
	return s
