class_name Player
extends Node2D
## Movimiento tile a tile (estilo FireRed): se mantiene la tecla para caminar.
## La posición es el punto de los pies (centro-abajo del tile) para el y-sort.

const TILE := 16
const STEP_TIME := 0.2
const DIRS := {"south": Vector2i.DOWN, "east": Vector2i.RIGHT, "north": Vector2i.UP, "west": Vector2i.LEFT}
const ACTIONS := {"south": "ui_down", "east": "ui_right", "north": "ui_up", "west": "ui_left"}
const FEET_Y := 42  # fila de los pies dentro del frame de 48px

signal arrived(tile: Vector2i)
signal bumped(tile: Vector2i)  # empujó contra algo sólido (puerta bloqueada, etc.)

var tile := Vector2i.ZERO
var blocked: Dictionary = {}
var facing := "south"
var locked := false
var _moving := false
var _sprite: AnimatedSprite2D


func _ready() -> void:
	_sprite = AnimatedSprite2D.new()
	_sprite.sprite_frames = _build_frames()
	_sprite.offset = Vector2(0, 24 - FEET_Y)
	add_child(_sprite)
	_idle()


func _build_frames() -> SpriteFrames:
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for dir in DIRS:
		sf.add_animation(dir)
		sf.set_animation_speed(dir, 15.0)  # 6 frames = 2 pasos
		for i in 6:
			sf.add_frame(dir, load("res://art/player/walk/%s/%d.png" % [dir, i]))
		sf.add_animation("idle_" + dir)
		sf.add_frame("idle_" + dir, load("res://art/player/%s.png" % dir))
	return sf


func _draw() -> void:
	draw_set_transform(Vector2(0, -1), 0.0, Vector2(1.0, 0.4))
	draw_circle(Vector2.ZERO, 6.0, Color(0, 0, 0, 0.35))


func place(t: Vector2i, face: String) -> void:
	tile = t
	position = feet(t)
	facing = face
	_idle()


static func feet(t: Vector2i) -> Vector2:
	return Vector2(t.x * TILE + TILE * 0.5, (t.y + 1) * TILE)


func facing_tile() -> Vector2i:
	return tile + DIRS[facing]


func _held_dir() -> String:
	if Input.is_action_pressed("ui_up"): return "north"
	if Input.is_action_pressed("ui_down"): return "south"
	if Input.is_action_pressed("ui_left"): return "west"
	if Input.is_action_pressed("ui_right"): return "east"
	return ""


func _process(_dt: float) -> void:
	if _moving:
		return
	var dir := "" if locked else _held_dir()
	if dir == "":
		_idle()
		return
	facing = dir
	var target: Vector2i = tile + DIRS[dir]
	if blocked.has(target):
		_idle()
		if Input.is_action_just_pressed(ACTIONS[dir]):
			bumped.emit(target)
		return
	_moving = true
	tile = target
	if _sprite.animation != dir:
		_sprite.play(dir)
	Sfx.play("step", -4.0, randf_range(0.85, 1.15))
	var tw := create_tween()
	tw.tween_property(self, "position", feet(target), STEP_TIME)
	tw.finished.connect(func() -> void:
		_moving = false
		arrived.emit(tile))


func _idle() -> void:
	if _sprite and _sprite.animation != "idle_" + facing:
		_sprite.play("idle_" + facing)
