class_name Actor
extends Node2D
## Grid actor (player, NPCs, SCPs). Position is the feet point (center-bottom of its tile)
## so it y-sorts with props. Moves tile to tile with a tween.

const TILE := 16
const DIRS := {"south": Vector2i.DOWN, "east": Vector2i.RIGHT, "north": Vector2i.UP, "west": Vector2i.LEFT}

signal stepped(t: Vector2i)

var char_id := ""
var tile := Vector2i.ZERO
var facing := "south"
var moving := false
var world: Node            # World: provides is_free(t, who) and astar
var sprite: AnimatedSprite2D
var shadow_size := 6.0
var path: Array[Vector2i] = []


func setup(id: String, t: Vector2i, face := "south") -> void:
	char_id = id
	sprite = AnimatedSprite2D.new()
	sprite.sprite_frames = CharFrames.get_frames(id)
	var fs := CharFrames.frame_size(id)
	sprite.centered = false
	sprite.offset = Vector2(-fs.x / 2.0, -CharFrames.feet_y(id) + 1)
	add_child(sprite)
	place(t, face)


static func feet(t: Vector2i) -> Vector2:
	return Vector2(t.x * TILE + TILE * 0.5, (t.y + 1) * TILE)


static func dir_name(v: Vector2i) -> String:
	for k in DIRS:
		if DIRS[k] == v:
			return k
	return "south"


func place(t: Vector2i, face := "") -> void:
	tile = t
	position = feet(t)
	if face != "":
		facing = face
	idle()


func facing_tile() -> Vector2i:
	return tile + DIRS[facing]


func face(d: String) -> void:
	facing = d
	if not moving:
		idle()


func face_toward(t: Vector2i) -> void:
	var d := t - tile
	if d == Vector2i.ZERO:
		return
	face(dir_name(Vector2i(signi(d.x), 0)) if absi(d.x) > absi(d.y) else dir_name(Vector2i(0, signi(d.y))))


func idle() -> void:
	var a := "idle_" + facing
	if sprite and sprite.sprite_frames.has_animation(a) and sprite.animation != a:
		sprite.play(a)


func _play_move(run: bool) -> void:
	if not sprite:
		return
	var a := ("run_" if run else "walk_") + facing
	if not sprite.sprite_frames.has_animation(a):
		a = "walk_" + facing
	if not sprite.sprite_frames.has_animation(a):
		a = "idle_" + facing
	if sprite.animation != a:
		sprite.play(a)


## Move one tile if free. Returns false if blocked.
func step(d: String, dur := 0.22, run := false) -> bool:
	if moving:
		return false
	facing = d
	var target: Vector2i = tile + DIRS[d]
	if world and not world.is_free(target, self):
		idle()
		return false
	moving = true
	tile = target
	_play_move(run)
	var tw := create_tween()
	tw.tween_property(self, "position", feet(target), dur)
	tw.finished.connect(func() -> void:
		moving = false
		stepped.emit(tile)
		if path.is_empty():
			idle())
	return true


## Walk along a path computed by the world (AStarGrid2D). Call follow_path() each frame.
func go_to(t: Vector2i) -> void:
	path = world.find_path(tile, t) if world else []
	if not path.is_empty() and path[0] == tile:
		path.pop_front()


func follow_path(dur := 0.25) -> void:
	if moving or path.is_empty():
		return
	var nxt: Vector2i = path[0]
	if step(dir_name(nxt - tile), dur):
		path.pop_front()
	else:
		path.clear()


func _draw() -> void:
	draw_set_transform(Vector2(0, -1), 0.0, Vector2(1.0, 0.35))
	draw_circle(Vector2.ZERO, shadow_size, Color(0, 0, 0, 0.4))
