extends SceneTree
## In-game screenshots with lighting: SCP_MAP=<id> [SCP_SPAWN=<name>]
##   godot --path . --script res://tools/shot.gd -- <out.png> [frames=90] [torch=on|off] [face=dir]

var out := ""
var frames := 90
var f := 0
var world


func _initialize() -> void:
	var a := OS.get_cmdline_user_args()
	out = a[0]
	if a.size() > 1:
		frames = int(a[1])
	world = load("res://scenes/main.tscn").instantiate()
	root.add_child(world)
	if a.size() > 2 and a[2] == "off":
		world.set_meta("torch_off", true)


func _process(_d: float) -> bool:
	f += 1
	if f == 20 and world.player:
		if world.has_meta("torch_off"):
			world.player.torch_on = false
		var a := OS.get_cmdline_user_args()
		if a.size() > 3:
			world.player.face(a[3])
	if f == frames:
		root.get_texture().get_image().save_png(out)
		return true
	return false
