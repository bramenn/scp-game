extends SceneTree
func _initialize() -> void:
	var d = JSON.parse_string(FileAccess.get_file_as_string("res://data/maps/A10.json"))
	var v := MapView.new()
	root.add_child(v)
	v.build(d)
	for t in [Vector2i(12,15), Vector2i(12,16), Vector2i(12,17), Vector2i(13,17)]:
		print(t, " blocked=", v.blocked.has(t), " ch=", v.ch(t), " prop=", v.solid_props.get(t, {}).get("id", ""))
	quit()
