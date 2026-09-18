class_name Actors
extends RefCounted
## Registry for map "actors" entries: SCPs, enemies, companions and set dressing that moves.
## Each entry: {id, x, y, cond?, ...}. The script for an id lives in scripts/scp/<id>.gd.

static func spawn(w: World, a: Dictionary) -> void:
	if not w.st.check(a.get("cond", "")):
		return
	var path := "res://scripts/scp/%s.gd" % String(a.id)
	if not ResourceLoader.exists(path):
		push_warning("no actor script for " + String(a.id))
		return
	var node: Actor = load(path).new()
	node.world = w
	node.set_meta("spec", a)
	w.view.ents.add_child(node)
	if node.has_method("init"):
		node.init(a)
	w.actors.append(node)
