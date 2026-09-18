class_name ScpCatalog
extends Node
## Carga los datos del juego: SCPs (1 archivo por SCP), mapas, objetos e historia.

const SCP_DIR := "res://data/scps"
const MAPS_FILE := "res://data/maps.json"
## Orden de la campaña: cada contención abre la siguiente celda.
const ORDER := ["scp-173", "scp-049", "scp-096", "scp-106", "scp-682"]

var scps: Dictionary = {}
var maps: Dictionary = {}
var items: Dictionary = {}
var story: Dictionary = {}


func load_all() -> void:
	scps.clear()
	for f in DirAccess.get_files_at(SCP_DIR):
		if not f.ends_with(".json"):
			continue
		var data = _read_json(SCP_DIR.path_join(f))
		if data == null or not data.has("id"):
			push_error("SCP inválido: %s" % f)
			continue
		scps[data.id] = data
	maps = _read_json(MAPS_FILE)
	items = _read_json("res://data/items.json")
	story = _read_json("res://data/story.json")


func _read_json(path: String):
	var txt := FileAccess.get_file_as_string(path)
	if txt == "":
		return null
	return JSON.parse_string(txt)


func get_scp(id):  # id puede ser null: mapas sin SCP
	return scps.get(id) if id else null


func get_map(id: String) -> Dictionary:
	return maps.get(id, {})
