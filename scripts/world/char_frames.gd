class_name CharFrames
extends RefCounted
## Builds SpriteFrames from art/chars/<id>/ (PixelLab export):
##   <dir>.png -> "idle_<dir>", walking-6-frames|scary-walk/<dir>/<i>.png -> "walk_<dir>",
##   running-6-frames/<dir>/<i>.png -> "run_<dir>". Cached per id.

const DIRS := ["south", "east", "north", "west"]
const WALKS := ["walking-6-frames", "scary-walk", "walking-4-frames", "walking-8-frames"]

static var _cache: Dictionary = {}


static func get_frames(id: String) -> SpriteFrames:
	if _cache.has(id):
		return _cache[id]
	var base := "res://art/chars/%s/" % id
	var sf := SpriteFrames.new()
	sf.remove_animation("default")
	for d in DIRS:
		var idle: String = base + d + ".png"
		if not ResourceLoader.exists(idle):
			continue
		sf.add_animation("idle_" + d)
		sf.add_frame("idle_" + d, load(idle))
		for walk in WALKS:
			if _add_seq(sf, "walk_" + d, base + walk + "/" + d + "/", 12.0):
				break
		_add_seq(sf, "run_" + d, base + "running-6-frames/" + d + "/", 16.0)
	_cache[id] = sf
	return sf


static func _add_seq(sf: SpriteFrames, anim: String, dir: String, fps: float) -> bool:
	if not ResourceLoader.exists(dir + "0.png"):
		return false
	sf.add_animation(anim)
	sf.set_animation_speed(anim, fps)
	var i := 0
	while ResourceLoader.exists(dir + "%d.png" % i):
		sf.add_frame(anim, load(dir + "%d.png" % i))
		i += 1
	return true


## Pixel row of the feet inside the frame (bottom of the south idle sprite).
static func feet_y(id: String) -> int:
	var tex := load("res://art/chars/%s/south.png" % id) as Texture2D
	return MapView.used_rect(tex).end.y if tex else 44


static func frame_size(id: String) -> Vector2:
	var tex := load("res://art/chars/%s/south.png" % id) as Texture2D
	return tex.get_size() if tex else Vector2(48, 48)
