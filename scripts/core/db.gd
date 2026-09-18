extends Node
## Static game data, loaded once: maps, items, SCPs, NPCs, dialogues, quests, documents, events.

var maps: Dictionary = {}       # id -> map dict (data/maps/<id>.json)
var items: Dictionary = {}
var scps: Dictionary = {}
var npcs: Dictionary = {}
var dialogues: Dictionary = {}
var quests: Dictionary = {}
var docs: Dictionary = {}
var events: Dictionary = {}
var story: Dictionary = {}


func _ready() -> void:
	load_all()


func load_all() -> void:
	maps.clear()
	for f in DirAccess.get_files_at("res://data/maps"):
		if f.ends_with(".json"):
			var m = _read("res://data/maps/" + f)
			if m is Dictionary:
				maps[m.id] = m
	scps.clear()
	if DirAccess.dir_exists_absolute("res://data/scps"):
		for f in DirAccess.get_files_at("res://data/scps"):
			if f.ends_with(".json"):
				var s = _read("res://data/scps/" + f)
				scps[s.id] = s
	for pair in [["items", "items"], ["npcs", "npcs"], ["dialogues", "dialogues"], ["quests", "quests"],
			["docs", "docs"], ["events", "events"], ["story", "story"]]:
		var d = _read("res://data/%s.json" % pair[0])
		set(pair[1], d if d is Dictionary else {})


func _read(path: String):
	if not FileAccess.file_exists(path):
		return null
	return JSON.parse_string(FileAccess.get_file_as_string(path))
