class_name GameState
extends RefCounted
## Everything that is saved: where you are, your body (hp, battery, sanity), inventory,
## story flags, quest stages, read documents and explored tiles per map.

const SAVE_PATH := "user://save.json"  # tests set SCP_SAVE to keep real saves safe
const MAX_HP := 100.0

var map := "A01"
var spawn := "start"
var tile := Vector2i(-1, -1)
var facing := "south"
var hp := MAX_HP
var battery := 100.0
var sanity := 100.0
var stamina := 100.0
var inv: Dictionary = {}       # item id -> count
var flags: Dictionary = {}     # flag -> true / value
var quests: Dictionary = {}    # quest id -> stage (int); -1 = done
var docs: Array = []           # document ids read
var explored: Dictionary = {}  # map id -> PackedByteArray (1 byte per tile, 1 = seen)
var play_time := 0.0
var deaths := 0


# ------------------------------------------------------------------ flags
func has(flag: String) -> bool:
	if flag == "":
		return true
	if flag.begins_with("!"):
		return not has(flag.substr(1))
	if flag.begins_with("item:"):
		return inv.get(flag.substr(5), 0) > 0
	if flag.begins_with("quest:"):   # quest:<id>:<stage>  (stage reached or done)
		var p := flag.split(":")
		var s: int = quests.get(p[1], 0)
		return s == -1 or s >= int(p[2])
	if flag.begins_with("done:"):
		return quests.get(flag.substr(5), 0) == -1
	if flag.begins_with("card:"):
		return card_level() >= int(flag.substr(5))
	return flags.get(flag, false) != false


## All conditions true. Accepts "a,b,!c" or an array.
func check(cond) -> bool:
	if cond == null or (cond is String and cond == ""):
		return true
	var parts: Array = cond if cond is Array else String(cond).split(",")
	for c in parts:
		if not has(String(c).strip_edges()):
			return false
	return true


func mark(flag: String, value = true) -> void:
	flags[flag] = value


func give(id: String, n := 1) -> void:
	inv[id] = inv.get(id, 0) + n


func take(id: String, n := 1) -> bool:
	if inv.get(id, 0) < n:
		return false
	inv[id] -= n
	if inv[id] <= 0:
		inv.erase(id)
	return true


func count(id: String) -> int:
	return inv.get(id, 0)


func card_level() -> int:
	if count("card_omni") > 0:
		return 6
	for lvl in range(5, 0, -1):
		if count("card_%d" % lvl) > 0:
			return lvl
	return 0


func quest_stage(q: String) -> int:
	return quests.get(q, 0)


func set_quest(q: String, stage: int) -> void:
	quests[q] = stage


# --------------------------------------------------------------- explored
func see(map_id: String, w: int, h: int, t: Vector2i, r := 5) -> void:
	var b: PackedByteArray = explored.get(map_id, PackedByteArray())
	if b.size() != w * h:
		b.resize(w * h)
		b.fill(0)
	for y in range(maxi(0, t.y - r), mini(h, t.y + r + 1)):
		for x in range(maxi(0, t.x - r), mini(w, t.x + r + 1)):
			b[y * w + x] = 1
	explored[map_id] = b


# ------------------------------------------------------------------- save
func to_dict() -> Dictionary:
	var ex := {}
	for k in explored:
		ex[k] = Marshalls.raw_to_base64(explored[k])
	return {"map": map, "tile": [tile.x, tile.y], "facing": facing, "hp": hp, "battery": battery,
		"sanity": sanity, "inv": inv, "flags": flags, "quests": quests, "docs": docs, "explored": ex,
		"play_time": play_time, "deaths": deaths}


func save() -> void:
	var f := FileAccess.open(path(), FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(to_dict()))


static func path() -> String:
	var p := OS.get_environment("SCP_SAVE")
	return p if p != "" else SAVE_PATH


static func exists() -> bool:
	return FileAccess.file_exists(path())


static func load_saved() -> GameState:
	var s := GameState.new()
	var d = JSON.parse_string(FileAccess.get_file_as_string(path())) if exists() else null
	if not d is Dictionary:
		return s
	s.map = d.get("map", "A01")
	var t: Array = d.get("tile", [-1, -1])
	s.tile = Vector2i(int(t[0]), int(t[1]))
	s.facing = d.get("facing", "south")
	s.hp = float(d.get("hp", MAX_HP))
	s.battery = float(d.get("battery", 100))
	s.sanity = float(d.get("sanity", 100))
	for k in d.get("inv", {}):
		s.inv[k] = int(d.inv[k])
	s.flags = d.get("flags", {})
	for k in d.get("quests", {}):
		s.quests[k] = int(d.quests[k])
	s.docs = d.get("docs", [])
	for k in d.get("explored", {}):
		s.explored[k] = Marshalls.base64_to_raw(d.explored[k])
	s.play_time = float(d.get("play_time", 0))
	s.deaths = int(d.get("deaths", 0))
	return s
