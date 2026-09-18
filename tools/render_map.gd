extends SceneTree
## Renders whole maps to PNG for art review (no lighting, no actors).
##   godot --path . --script res://tools/render_map.gd -- <out_dir> <map_id> [map_id...]

var ids: Array = []
var out := ""
var f := 0
var view: MapView
var vp: SubViewport


func _initialize() -> void:
	var args := OS.get_cmdline_user_args()
	out = args[0]
	ids = args.slice(1)
	if ids == ["all"]:
		ids = []
		for fn in DirAccess.get_files_at("res://data/maps"):
			ids.append(fn.get_basename())


func _process(_d: float) -> bool:
	f += 1
	if f % 4 == 1:
		if ids.is_empty():
			return true
		if vp:
			vp.queue_free()
		var id: String = ids[0]
		var d = JSON.parse_string(FileAccess.get_file_as_string("res://data/maps/%s.json" % id))
		vp = SubViewport.new()
		vp.size = Vector2i(int(d.size[0]) * 16, int(d.size[1]) * 16)
		vp.transparent_bg = false
		vp.render_target_update_mode = SubViewport.UPDATE_ALWAYS
		root.add_child(vp)
		view = MapView.new()
		vp.add_child(view)
		view.build(d)
	elif f % 4 == 3:
		var id: String = ids.pop_front()
		vp.get_texture().get_image().save_png("%s/map_%s.png" % [out, id])
	return false
