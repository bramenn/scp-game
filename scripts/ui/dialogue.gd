class_name DialogueBox
extends CanvasLayer
## Dialogue: portrait + name + typewriter text with per-speaker voice blips, and choices.
## Speakers come from data/npcs.json ({name, portrait, voice}); special speakers:
## "radio" (Command, static noise), "079" (red glitch terminal text), "" (narration).

signal _advance
signal _picked(i: int)

var root: Control
var panel: PanelContainer
var portrait: TextureRect
var pframe: Panel
var name_l: Label
var text_l: Label
var arrow: Label
var choices: VBoxContainer
var _waiting := false
var _choosing := false
var _cursor := 0
var _opts: Array = []
var _voice := 1.0
var _style := ""
const CPS := 55.0   # typewriter speed, characters per second


func _ready() -> void:
	layer = 7
	root = UiKit.root(self)
	panel = PanelContainer.new()
	panel.position = Vector2(8, UiKit.H - 76)
	panel.custom_minimum_size = Vector2(UiKit.W - 16, 68)
	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 8)
	pframe = Panel.new()
	pframe.custom_minimum_size = Vector2(56, 56)
	pframe.add_theme_stylebox_override("panel", UiKit.panel("panel_gold"))
	portrait = TextureRect.new()
	portrait.position = Vector2(-4, -4)
	portrait.size = Vector2(64, 64)
	portrait.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
	portrait.texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	pframe.clip_contents = true
	pframe.add_child(portrait)
	hb.add_child(pframe)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 2)
	name_l = UiKit.label("", 8, UiKit.GOLD)
	text_l = UiKit.label("")
	text_l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text_l.custom_minimum_size = Vector2(380, 40)
	vb.add_child(name_l)
	vb.add_child(text_l)
	hb.add_child(vb)
	panel.add_child(hb)
	root.add_child(panel)
	arrow = UiKit.label("v", 8, UiKit.GOLD)
	arrow.position = Vector2(UiKit.W - 20, UiKit.H - 16)
	root.add_child(arrow)
	choices = VBoxContainer.new()
	choices.add_theme_constant_override("separation", 2)
	var cp := PanelContainer.new()
	cp.add_theme_stylebox_override("panel", UiKit.panel("panel_gold"))
	cp.position = Vector2(UiKit.W - 196, UiKit.H - 80)
	cp.add_child(choices)
	cp.name = "ChoicePanel"
	root.add_child(cp)
	_hide_all()


func _hide_all() -> void:
	panel.hide()
	arrow.hide()
	root.get_node("ChoicePanel").hide()


func _speaker(who: String) -> void:
	_style = who
	var info: Dictionary = Db.npcs.get(who, {})
	name_l.text = Loc.t(info.get("name", "")) if who not in ["radio", "079", ""] else \
		(Loc.ui("radio_name") if who == "radio" else ("SCP-079" if who == "079" else ""))
	var ptex = info.get("portrait", "")
	if who == "radio":
		ptex = "res://art/gen/ui/radio.png"
	elif who == "079":
		ptex = "res://art/gen/ui/079.png"
	portrait.texture = load(ptex) if ptex != "" and ResourceLoader.exists(ptex) else null
	pframe.visible = portrait.texture != null
	_voice = float(info.get("voice", 1.0)) if who not in ["radio", "079"] else (0.7 if who == "radio" else 0.5)
	text_l.add_theme_color_override("font_color", Color("e84a3a") if who == "079" else Color("e4e6e8"))
	text_l.custom_minimum_size.x = 380 if pframe.visible else 450


func say(lines: Array, who := "") -> void:
	_speaker(who)
	panel.show()
	for line in lines:
		var s := Loc.t(line)
		if _style == "079":
			s = s.to_upper()
		text_l.text = s
		text_l.visible_characters = 0
		arrow.hide()
		_waiting = true
		var n := s.length()
		var shown := 0.0
		var pause := 0.0
		var last := 0
		while shown < n and _waiting:
			await get_tree().process_frame
			var dt := get_process_delta_time()
			if pause > 0.0:
				pause -= dt
				continue
			shown = minf(n, shown + dt * CPS)
			var i := int(shown)
			if i > last:
				text_l.visible_characters = i
				var ch := s[i - 1]
				if i / 3 != last / 3 and ch != " ":
					Sfx.play("blip_079" if _style == "079" else ("blip_radio" if _style == "radio" else "blip"),
						-14.0, _voice * randf_range(0.94, 1.06))
				if ch in ".!?":
					pause = 0.18
				elif ch == ",":
					pause = 0.07
				last = i
		text_l.visible_characters = -1
		arrow.show()
		_waiting = true
		await _advance
	_waiting = false
	_hide_all()


func choose(prompt, options: Array, who := "") -> int:
	_speaker(who)
	if prompt is Dictionary or String(prompt) != "":
		panel.show()
		text_l.text = Loc.t(prompt)
		text_l.visible_characters = -1
	for c in choices.get_children():
		c.queue_free()
	_opts = options
	for o in options:
		var l := UiKit.label(Loc.t(o))
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.custom_minimum_size = Vector2(176, 0)
		choices.add_child(l)
	var cp: Control = root.get_node("ChoicePanel")
	cp.show()
	await get_tree().process_frame
	cp.position.y = UiKit.H - 80 - cp.size.y
	_cursor = 0
	_choosing = true
	_refresh()
	var i: int = await _picked
	_choosing = false
	_hide_all()
	return i


func _refresh() -> void:
	var k := 0
	for c in choices.get_children():
		if c.is_queued_for_deletion():
			continue
		(c as Label).text = ("> " if k == _cursor else "  ") + Loc.t(_opts[k])
		(c as Label).add_theme_color_override("font_color", UiKit.GOLD if k == _cursor else UiKit.PALE)
		k += 1


func _unhandled_input(event: InputEvent) -> void:
	if _choosing:
		if event.is_action_pressed("ui_down"):
			_cursor = (_cursor + 1) % _opts.size()
			Sfx.play("move", -8.0)
			_refresh()
		elif event.is_action_pressed("ui_up"):
			_cursor = (_cursor - 1 + _opts.size()) % _opts.size()
			Sfx.play("move", -8.0)
			_refresh()
		elif event.is_action_pressed("interact"):
			Sfx.play("select", -6.0)
			_picked.emit(_cursor)
		else:
			return
		get_viewport().set_input_as_handled()
	elif _waiting and event.is_action_pressed("interact"):
		get_viewport().set_input_as_handled()
		if arrow.visible:
			_advance.emit()
		else:
			_waiting = false  # skip typing: loop ends and shows the full line
			await get_tree().process_frame
			_waiting = true
