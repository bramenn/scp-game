extends SceneTree
## Capturas de verificación con render: levanta el juego, cruza el título,
## recorre los mapas y entra en combate.
##   godot --path . --script res://tools/shots.gd -- <dir>

var world
var f := 0
var out := "user://"
var steps := [
	[80, "title"], [100, "ok"], [170, "intro"], [240, "hub"],
	[250, "go:z-173"], [310, "z-173"], [320, "go:z-096"], [380, "z-096"],
	[390, "go:z-106"], [450, "z-106"], [460, "go:z-049"], [520, "z-049"],
	[530, "go:z-682"], [590, "z-682"], [600, "fight"],
	[660, "battle-intro"], [730, "battle-menu"], [800, "battle-hit"], [900, "quit"],
]


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	if args.size() > 0:
		out = args[0]
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)


func _press() -> void:
	var e := InputEventAction.new()
	e.action = "ui_accept"
	e.pressed = true
	Input.parse_input_event(e)


func _process(_d: float) -> bool:
	f += 1
	if f > 110 and f % 8 == 0:
		_press()  # avanza intro, diálogos y menús del combate
	for s in steps:
		if s[0] != f:
			continue
		var what: String = s[1]
		if what.begins_with("go:"):
			world._enter_map(what.substr(3), "hub")
		elif what == "fight":
			world._encounter(world.db.get_scp("scp-682"))
		elif what == "ok":
			_press()
		elif what == "quit":
			return true
		else:
			root.get_texture().get_image().save_png("%s/%s.png" % [out, what])
	return false
