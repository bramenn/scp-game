class_name Hud
extends CanvasLayer
## In-game overlay: post-process (grain, vignette, dread), status, objective, location
## title, toasts, interaction prompt, fades, flashes, death screen.

const POST := """
shader_type canvas_item;
uniform sampler2D screen : hint_screen_texture, filter_nearest;
uniform float dread = 0.0;     // 0..1 (low sanity)
uniform float hurt = 0.0;      // 0..1 red flash
uniform float grain = 0.05;
float rnd(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
void fragment() {
	vec2 uv = SCREEN_UV;
	float pulse = 0.5 + 0.5 * sin(TIME * (2.0 + dread * 3.0));
	uv += vec2(sin(uv.y * 40.0 + TIME * 3.0), 0.0) * 0.0015 * dread * dread;
	float ab = 0.002 * dread;
	vec3 c = vec3(texture(screen, uv + vec2(ab, 0.0)).r, texture(screen, uv).g, texture(screen, uv - vec2(ab, 0.0)).b);
	float g = dot(c, vec3(0.3, 0.59, 0.11));
	c = mix(c, vec3(g), clamp(dread * 0.85, 0.0, 0.85));
	vec2 px = floor(SCREEN_UV * vec2(480.0, 270.0));
	c += (rnd(px + floor(TIME * 24.0)) - 0.5) * (grain + dread * 0.08);
	float d = distance(SCREEN_UV, vec2(0.5));
	float vig = smoothstep(0.35 - dread * 0.15, 0.85, d) * (0.65 + dread * 0.3 + pulse * dread * 0.15);
	c *= 1.0 - vig;
	c = mix(c, vec3(0.6, 0.0, 0.0), hurt * 0.45 * (1.0 - d));
	COLOR = vec4(c, 1.0);
}
"""

var st: GameState
var root: Control
var post: ColorRect
var _fade: ColorRect
var _status: PanelContainer
var _bars := {}
var _stamina: ProgressBar
var _goal: Label
var _loc: Label
var _loc_sub: Label
var _toasts: VBoxContainer
var _prompt: Label
var _dread := 0.0
var _hurt := 0.0


func _ready() -> void:
	layer = 5
	root = UiKit.root(self)
	post = ColorRect.new()
	post.size = Vector2(UiKit.W, UiKit.H)
	post.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var sh := Shader.new()
	sh.code = POST
	post.material = ShaderMaterial.new()
	post.material.shader = sh
	root.add_child(post)

	_status = PanelContainer.new()
	_status.position = Vector2(6, UiKit.H - 40)
	var v := VBoxContainer.new()
	v.add_theme_constant_override("separation", 3)
	for k in [["hp", "i_heart", Color("c9362e")], ["battery", "i_battery", Color("9ab94a")], ["sanity", "i_brain", Color("8e6bb0")]]:
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 4)
		var ic := TextureRect.new()
		ic.texture = load("res://art/gen/ui/%s.png" % k[1])
		ic.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
		ic.custom_minimum_size = Vector2(8, 4)
		var b := UiKit.bar(k[2], 52, 3)
		b.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		row.add_child(ic)
		row.add_child(b)
		v.add_child(row)
		_bars[k[0]] = b
	_status.add_child(v)
	root.add_child(_status)
	_stamina = UiKit.bar(Color("7896ab"), 64, 1)
	_stamina.position = Vector2(8, UiKit.H - 44)
	root.add_child(_stamina)

	_goal = UiKit.label("", 8, UiKit.GOLD)
	_goal.position = Vector2(8, 6)
	_goal.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_goal.custom_minimum_size = Vector2(240, 0)
	root.add_child(_goal)

	_loc = UiKit.label("", 16)
	_loc.position = Vector2(0, 58)
	_loc.size = Vector2(UiKit.W, 20)
	_loc.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_loc.modulate.a = 0.0
	root.add_child(_loc)
	_loc_sub = UiKit.label("", 8, UiKit.DIM)
	_loc_sub.position = Vector2(0, 78)
	_loc_sub.size = Vector2(UiKit.W, 10)
	_loc_sub.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_loc_sub.modulate.a = 0.0
	root.add_child(_loc_sub)

	_toasts = VBoxContainer.new()
	_toasts.position = Vector2(UiKit.W - 190, 6)
	_toasts.custom_minimum_size = Vector2(184, 0)
	_toasts.alignment = BoxContainer.ALIGNMENT_BEGIN
	_toasts.add_theme_constant_override("separation", 2)
	root.add_child(_toasts)

	_prompt = UiKit.label("", 8, UiKit.PALE)
	_prompt.position = Vector2(0, UiKit.H - 14)
	_prompt.size = Vector2(UiKit.W, 10)
	_prompt.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(_prompt)

	_fade = ColorRect.new()
	_fade.color = Color.BLACK
	_fade.size = Vector2(UiKit.W, UiKit.H)
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.add_child(_fade)
	Loc.changed.connect(refresh)


func bind(s: GameState) -> void:
	st = s
	refresh()


func refresh() -> void:
	if not st:
		return
	var obj = st.flags.get("objective", "")
	_goal.text = ("> " + Loc.t(obj)) if obj is Dictionary or String(obj) != "" else ""


func _process(dt: float) -> void:
	if not st:
		_status.visible = false
		return
	_status.visible = _fade.color.a < 0.5
	_bars.hp.value = st.hp
	_bars.battery.value = st.battery
	_bars.sanity.value = st.sanity
	_stamina.value = st.stamina
	_stamina.visible = st.stamina < 99.0
	_hurt = maxf(0.0, _hurt - dt * 1.5)
	var m: ShaderMaterial = post.material
	m.set_shader_parameter("dread", _dread)
	m.set_shader_parameter("hurt", _hurt)
	# the battery bar blinks when low
	_bars.battery.modulate.a = 1.0 if st.battery > 15.0 else (0.4 + 0.6 * float(int(Time.get_ticks_msec() / 300) % 2))


func set_dread(v: float) -> void:
	_dread = lerpf(_dread, clampf(v, 0.0, 1.0), 0.3)


func hurt() -> void:
	_hurt = 1.0


func prompt(text: String) -> void:
	_prompt.text = text


func location(name: String, sub := "") -> void:
	_loc.text = name
	_loc_sub.text = sub
	var tw := create_tween()
	tw.tween_property(_loc, "modulate:a", 1.0, 0.8)
	tw.parallel().tween_property(_loc_sub, "modulate:a", 1.0, 0.8)
	tw.tween_interval(2.2)
	tw.tween_property(_loc, "modulate:a", 0.0, 1.2)
	tw.parallel().tween_property(_loc_sub, "modulate:a", 0.0, 1.2)


func toast(text: String, kind := "panel") -> void:
	var p := PanelContainer.new()
	p.add_theme_stylebox_override("panel", UiKit.panel("panel_gold" if kind == "gold" else "panel"))
	var l := UiKit.label(text, 8, UiKit.GOLD if kind == "gold" else Color("e4e6e8"))
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.custom_minimum_size = Vector2(168, 0)
	p.add_child(l)
	p.modulate.a = 0.0
	_toasts.add_child(p)
	var tw := p.create_tween()
	tw.tween_property(p, "modulate:a", 1.0, 0.25)
	tw.tween_interval(3.5)
	tw.tween_property(p, "modulate:a", 0.0, 0.6)
	tw.tween_callback(p.queue_free)


func fade(to_black: bool, t := 0.4) -> void:
	await create_tween().tween_property(_fade, "color:a", 1.0 if to_black else 0.0, t).finished


func flash(times := 1, col := Color.WHITE) -> void:
	for i in times:
		_fade.color = Color(col.r, col.g, col.b, 0.85)
		await get_tree().create_timer(0.06).timeout
		_fade.color = Color(0, 0, 0, 0)
		await get_tree().create_timer(0.08).timeout


func shake(cam: Camera2D, t: float, power: float) -> void:
	if not cam:
		return
	var end := Time.get_ticks_msec() + int(t * 1000)
	while Time.get_ticks_msec() < end:
		cam.offset = Vector2(randf_range(-power, power), randf_range(-power, power)).round()
		await get_tree().process_frame
	cam.offset = Vector2.ZERO


func pan(cam: Camera2D, to: Vector2, t: float) -> void:
	await create_tween().tween_property(cam, "offset", to, t).set_trans(Tween.TRANS_SINE).finished


func death_screen(cause: String) -> void:
	Sfx.play("death", 0.0)
	await fade(true, 1.2)
	var l := UiKit.label(Loc.ui("death_" + cause) if cause != "" else Loc.ui("death"), 16, UiKit.RED)
	l.position = Vector2(0, 110)
	l.size = Vector2(UiKit.W, 20)
	l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(l)
	var s := UiKit.label(Loc.ui("death_sub"), 8, UiKit.DIM)
	s.position = Vector2(0, 134)
	s.size = Vector2(UiKit.W, 10)
	s.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(s)
	await get_tree().create_timer(3.0).timeout
	l.queue_free()
	s.queue_free()
