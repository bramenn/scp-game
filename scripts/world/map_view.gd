class_name MapView
extends Node2D
## Builds one map from data/maps/<id>.json: floors, 3/4 walls, ambient-occlusion shade,
## floor traces, wall decor, light occluders, doors, props and exits.
## Entities (actors, vermin, fx, lights) are spawned by World on top of this.

const TILE := 16
const WALL_CHARS := "#"
const INDEX_PATH := "res://art/gen/index.json"

static var _tileset: TileSet
static var _index: Dictionary
static var _door_tex: Texture2D
static var _used: Dictionary = {}

var data: Dictionary
var w := 0
var h := 0
var blocked: Dictionary = {}     # Vector2i -> true (walls, props, closed doors)
var solid_props: Dictionary = {} # Vector2i -> prop dict (for examine)
var doors: Array[Door] = []
var door_at: Dictionary = {}     # Vector2i -> Door
var exits: Array = []            # [{rect: Rect2i, to, at}]
var water: Dictionary = {}       # Vector2i -> "shallow" | "deep"
var ents: Node2D                 # y-sorted entity layer (props, actors)
var layers := {}


static func _ensure_tileset() -> void:
	if _tileset:
		return
	_index = JSON.parse_string(FileAccess.get_file_as_string(INDEX_PATH))
	_door_tex = load("res://art/gen/doors.png")
	_tileset = TileSet.new()
	_tileset.tile_size = Vector2i(TILE, TILE)
	for path in ["floors", "walls", "traces", "walldecor"]:
		var src := TileSetAtlasSource.new()
		src.texture = load("res://art/gen/%s.png" % path)
		src.texture_region_size = Vector2i(TILE, TILE)
		var size := src.texture.get_size() / TILE
		for y in int(size.y):
			for x in int(size.x):
				src.create_tile(Vector2i(x, y))
		_tileset.add_source(src)


static func floor_row(mat: String) -> int:
	_ensure_tileset()
	return maxi(0, (_index.floors as Array).find(mat))


static func wall_row(mat: String) -> int:
	_ensure_tileset()
	return maxi(0, (_index.walls as Array).find(mat))


static func trace_coord(name: String) -> Vector2i:
	var i: int = (_index.traces as Array).find(name)
	return Vector2i(i % 16, i / 16) if i >= 0 else Vector2i(-1, -1)


static func decor_coord(name: String) -> Vector2i:
	var i: int = (_index.walldecor as Array).find(name)
	return Vector2i(i % 16, i / 16) if i >= 0 else Vector2i(-1, -1)


func build(d: Dictionary) -> void:
	_ensure_tileset()
	data = d
	w = int(d.size[0])
	h = int(d.size[1])
	for name in ["floor", "trace", "trace2", "shade", "wall", "decor"]:
		var l := TileMapLayer.new()
		l.tile_set = _tileset
		l.name = name
		add_child(l)
		layers[name] = l
	ents = Node2D.new()
	ents.name = "Ents"
	ents.y_sort_enabled = true
	add_child(ents)
	_build_tiles()
	_build_occluders()
	for t in d.get("traces", []):
		_put_trace(String(t[0]), Vector2i(int(t[1]), int(t[2])))
	for t in d.get("walldecor", []):
		var c := decor_coord(String(t[0]))
		if c.x >= 0:
			layers.decor.set_cell(Vector2i(int(t[1]), int(t[2])), 3, c)
	for dd in d.get("doors", []):
		_add_door(dd)
	for p in d.get("props", []):
		_add_prop(p)
	for e in d.get("exits", []):
		var r: Array = e.rect
		exits.append({"rect": Rect2i(int(r[0]), int(r[1]), int(r[2]), int(r[3])), "to": e.to, "at": e.at,
			"sfx": e.get("sfx", "door"), "cond": e.get("cond", ""), "msg": e.get("msg", "")})


# ------------------------------------------------------------------ tiles

func ch(t: Vector2i) -> String:
	if t.y < 0 or t.y >= h or t.x < 0 or t.x >= w:
		return " "
	return String(data.grid[t.y])[t.x]


func is_wall(t: Vector2i) -> bool:
	var c := ch(t)
	return c == "#" or c == " "


func mat_of(t: Vector2i) -> Array:
	var code := "a"
	if t.y >= 0 and t.y < h and t.x >= 0 and t.x < w:
		code = String(data.mat[t.y])[t.x]
	return data.mats.get(code, ["concrete", "concrete"])


func _build_tiles() -> void:
	var fl: TileMapLayer = layers.floor
	var wl: TileMapLayer = layers.wall
	var sh: TileMapLayer = layers.shade
	for y in h:
		for x in w:
			var t := Vector2i(x, y)
			var c := ch(t)
			var m := mat_of(t)
			var hsh := absi(hash(t * 7919)) % 100
			if c == " ":
				blocked[t] = true
				continue
			if c == "#":
				blocked[t] = true
				wl.set_cell(t, 1, _wall_tile(t, m, hsh))
				continue
			# floor: 2x2 macro slab most of the time, random variants sprinkled in
			var row := floor_row(String(m[0]))
			var col := (x % 2) + (y % 2) * 2
			if hsh >= 90:
				col = 4 + hsh % 8
			fl.set_cell(t, 0, Vector2i(col, row))
			if c == "~":
				water[t] = "shallow"
			elif c == "=":
				water[t] = "deep"
				blocked[t] = true
			# ambient occlusion against walls
			var n := is_wall(t + Vector2i.UP)
			var wv := is_wall(t + Vector2i.LEFT)
			var ev := is_wall(t + Vector2i.RIGHT)
			var s := ""
			if n and wv: s = "shade_nw"
			elif n and ev: s = "shade_ne"
			elif n: s = "shade_n"
			elif wv: s = "shade_w"
			elif ev: s = "shade_e"
			if s != "":
				sh.set_cell(t, 2, trace_coord(s))
	for t in water:
		_put_trace("puddle_big" if water[t] == "deep" else "wet", t)


func _wall_tile(t: Vector2i, m: Array, hsh: int) -> Vector2i:
	var row := wall_row(String(m[1])) * 2
	var below := t + Vector2i.DOWN
	if not is_wall(below):
		return Vector2i([0, 0, 0, 1, 2, 3, 4, 0][hsh % 8], row)          # lower face
	if not is_wall(below + Vector2i.DOWN) and ch(below) == "#":
		return Vector2i(8 + [0, 0, 1, 2][hsh % 4], row)                     # upper face
	var mask := 0
	var dirs := [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]
	for i in 4:
		if not is_wall(t + dirs[i]) and ch(t + dirs[i]) != " ":
			mask |= 1 << i
	return Vector2i(mask, row + 1)                                           # top


func is_face(t: Vector2i) -> bool:
	if ch(t) != "#":
		return false
	var b := t + Vector2i.DOWN
	return not is_wall(b) or (ch(b) == "#" and not is_wall(b + Vector2i.DOWN))


## Walls block light. Face tiles only block along their top edge, so a wall lit from the
## south shows its face while the room behind it stays dark. Runs are merged per row.
func _build_occluders() -> void:
	var occ := Node2D.new()
	occ.name = "Occluders"
	add_child(occ)
	for y in h:
		var run_start := -1
		var run_face := false
		for x in w + 1:
			var t := Vector2i(x, y)
			var solid := x < w and ch(t) == "#"
			var face := solid and is_face(t)
			var face_top := face and not is_face(t + Vector2i.UP)
			var kind := 0 if not solid else (2 if face_top else (1 if not face else 0))
			var cur := -1 if run_start < 0 else (2 if run_face else 1)
			if kind != cur:
				if run_start >= 0:
					_occ_rect(occ, run_start, x, y, run_face)
				run_start = x if kind > 0 else -1
				run_face = kind == 2


func _occ_rect(parent: Node, x0: int, x1: int, y: int, face: bool) -> void:
	var r := Rect2(x0 * TILE, y * TILE, (x1 - x0) * TILE, 3 if face else TILE)
	var o := LightOccluder2D.new()
	var p := OccluderPolygon2D.new()
	p.polygon = PackedVector2Array([r.position, Vector2(r.end.x, r.position.y), r.end, Vector2(r.position.x, r.end.y)])
	o.occluder = p
	parent.add_child(o)


func _put_trace(name: String, t: Vector2i) -> void:
	var c := trace_coord(name)
	if c.x < 0:
		push_warning("unknown trace " + name)
		return
	var l: TileMapLayer = layers.trace
	if l.get_cell_source_id(t) != -1:
		l = layers.trace2
	l.set_cell(t, 2, c)


# ------------------------------------------------------------------ doors / props

func _add_door(dd: Dictionary) -> void:
	var door := Door.new()
	door.setup(dd, _door_tex)
	ents.add_child(door)
	doors.append(door)
	for t in door.tiles():
		door_at[t] = door
		blocked[t] = true


func set_door_open(door: Door, open: bool) -> void:
	door.set_open(open)
	for t in door.tiles():
		if open:
			blocked.erase(t)
		else:
			blocked[t] = true


## props: [id, x, y, opts]. (x, y) = bottom-left tile of the footprint. The sprite is
## centered on its footprint and sits on the bottom edge; blocks the bottom row unless
## opts.walk. opts.rows blocks more rows upward; opts.flip mirrors it.
func _add_prop(p: Array) -> void:
	var id := String(p[0])
	var t := Vector2i(int(p[1]), int(p[2]))
	var opts: Dictionary = p[3] if p.size() > 3 else {}
	var path := "res://art/props/%s.png" % id
	if not ResourceLoader.exists(path):
		push_warning("missing prop art: " + id)
		return
	var tex: Texture2D = load(path)
	var used := used_rect(tex)
	var wt := maxi(1, int(ceil(used.size.x / float(TILE))))
	var s := Sprite2D.new()
	s.texture = tex
	s.flip_h = opts.get("flip", false)
	s.centered = false
	# anchor: visible pixels centered on the footprint, their bottom on its bottom edge
	s.offset = Vector2(-used.get_center().x, -used.end.y)
	s.position = Vector2(t.x * TILE + wt * TILE / 2.0, (t.y + 1) * TILE - opts.get("lift", 0))
	s.set_meta("prop", id)
	ents.add_child(s)
	if opts.get("glow"):
		s.set_meta("glow", opts.glow)
	if opts.get("walk", false):
		return
	for yy in int(opts.get("rows", 1)):
		for xx in int(opts.get("w", wt)):
			var bt := t + Vector2i(xx, -yy)
			blocked[bt] = true
			solid_props[bt] = {"id": id, "opts": opts}


## Bounding box of the non-transparent pixels (cached per texture).
static func used_rect(tex: Texture2D) -> Rect2i:
	if not _used.has(tex.resource_path):
		_used[tex.resource_path] = tex.get_image().get_used_rect()
	return _used[tex.resource_path]


func exit_at(t: Vector2i):
	for e in exits:
		if (e.rect as Rect2i).has_point(t):
			return e
	return null
