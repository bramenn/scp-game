class_name PlayerActor
extends Actor
## Agent Vega. Hold a direction to walk, Shift to sprint (loud, uses stamina),
## F toggles the flashlight (cone light with real wall shadows, drains battery).

const WALK_TIME := 0.22
const RUN_TIME := 0.13
const CONE_DEG := 34.0

signal noise(t: Vector2i, radius: int)
signal interact_pressed

var st: GameState
var locked := false
var sprinting := false
var torch: PointLight2D
var aura: PointLight2D
var torch_on := true
var _flicker := 0.0
var _turn_to := 0.0
var _turn_hold := 0.0
var _dir_held := ""
var _turned := false

static var _cone: ImageTexture
static var _radial: GradientTexture2D


func _ready() -> void:
	setup("vega", tile, facing)
	shadow_size = 6.0
	queue_redraw()
	torch = PointLight2D.new()
	torch.texture = cone_texture()
	torch.texture_scale = 1.0
	torch.energy = 1.25
	torch.color = Color(1.0, 0.95, 0.82)
	torch.shadow_enabled = true
	torch.shadow_filter = PointLight2D.SHADOW_FILTER_PCF5
	torch.shadow_filter_smooth = 2.0
	torch.position = Vector2(0, -14)
	add_child(torch)
	aura = PointLight2D.new()
	aura.texture = radial_texture()
	aura.texture_scale = 0.55
	aura.energy = 0.45
	aura.color = Color(0.75, 0.8, 1.0)
	aura.position = Vector2(0, -12)
	add_child(aura)
	_turn_to = _dir_angle()
	torch.rotation = _turn_to


static func cone_texture() -> ImageTexture:
	if _cone:
		return _cone
	var n := 384
	var img := Image.create(n, n, false, Image.FORMAT_RGBA8)
	var c := Vector2(n / 2.0, n / 2.0)
	for y in n:
		for x in n:
			var v := Vector2(x, y) - c
			var d := v.length() / (n / 2.0)
			if d > 1.0 or v.x < -2:
				continue
			var ang := absf(rad_to_deg(atan2(v.y, v.x)))
			var edge := clampf((CONE_DEG - ang) / 10.0, 0.0, 1.0)      # soft cone edge
			var fall := pow(1.0 - d, 1.4)                                # distance falloff
			var core := 1.0 + 0.5 * clampf((12.0 - ang) / 12.0, 0.0, 1.0)  # brighter center
			var near := clampf(d * 6.0, 0.25, 1.0)                        # no hot spot at the lens
			var a := clampf(edge * fall * core * near, 0.0, 1.0)
			img.set_pixel(x, y, Color(1, 1, 1, a))
	_cone = ImageTexture.create_from_image(img)
	return _cone


static func radial_texture() -> GradientTexture2D:
	if _radial:
		return _radial
	_radial = GradientTexture2D.new()
	_radial.fill = GradientTexture2D.FILL_RADIAL
	_radial.fill_from = Vector2(0.5, 0.5)
	_radial.fill_to = Vector2(1.0, 0.5)
	_radial.width = 256
	_radial.height = 256
	var g := Gradient.new()
	g.set_color(0, Color.WHITE)
	g.set_color(1, Color(1, 1, 1, 0))
	g.add_point(0.45, Color(1, 1, 1, 0.35))
	_radial.gradient = g
	return _radial


func _dir_angle() -> float:
	return {"east": 0.0, "south": PI / 2, "west": PI, "north": -PI / 2}[facing]


func _held_dir() -> String:
	if Input.is_action_pressed("ui_up"): return "north"
	if Input.is_action_pressed("ui_down"): return "south"
	if Input.is_action_pressed("ui_left"): return "west"
	if Input.is_action_pressed("ui_right"): return "east"
	return ""


func _unhandled_input(event: InputEvent) -> void:
	if locked:
		return
	if event.is_action_pressed("flashlight"):
		torch_on = not torch_on
		Sfx.play("click", -4.0)
		get_viewport().set_input_as_handled()


func _process(dt: float) -> void:
	_update_torch(dt)
	if moving or locked:
		if locked and not moving:
			idle()
		return
	var d := _held_dir()
	if d == "":
		_dir_held = ""
		idle()
		sprinting = false
		if st:
			st.stamina = minf(100.0, st.stamina + dt * 18.0)
		return
	# a quick tap on a new direction only turns (FireRed style); holding it walks
	if d != _dir_held:
		_dir_held = d
		_turn_hold = 0.0
		_turned = d != facing
		if _turned:
			face(d)
			return
	_turn_hold += dt
	if _turned and _turn_hold < 0.12:
		return
	sprinting = Input.is_action_pressed("sprint") and st != null and st.stamina > 5.0
	if st and sprinting:
		st.stamina = maxf(0.0, st.stamina - 7.0)
	elif st:
		st.stamina = minf(100.0, st.stamina + dt * 10.0)
	if not step(d, RUN_TIME if sprinting else WALK_TIME, sprinting):
		if world:
			world.on_bump(tile + DIRS[d])
		return
	noise.emit(tile, 8 if sprinting else 3)
	if world:
		var surf: String = world.surface_at(tile)
		Sfx.play("step_" + surf, -10.0 if not sprinting else -6.0, randf_range(0.9, 1.1))


func _update_torch(dt: float) -> void:
	_turn_to = _dir_angle()
	torch.rotation = lerp_angle(torch.rotation, _turn_to, clampf(dt * 14.0, 0.0, 1.0))
	var on := torch_on and st != null and st.battery > 0.0
	if st and on:
		st.battery = maxf(0.0, st.battery - dt * 0.18)
	var e := 1.25
	if st and st.battery < 15.0:  # dying battery flickers
		_flicker -= dt
		if _flicker <= 0.0:
			_flicker = randf_range(0.05, 0.6 + st.battery / 10.0)
		e = 1.25 if _flicker > 0.08 else randf_range(0.0, 0.5)
	torch.energy = e * (world.torch_scale if world else 1.0) if on else 0.0
	torch.texture_scale = world.torch_range if world else 1.0
