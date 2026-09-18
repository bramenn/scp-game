class_name ScpActor
extends Actor
## Base for anomalies and hostile actors placed with m.actor(id, x, y, ...).
## spec keys: cond (spawn condition), gone (flag that removes it), dir, plus per-actor keys.

var spec: Dictionary = {}
var solid := true


func init(a: Dictionary) -> void:
	spec = a
	setup(String(a.get("sprite", a.id)), Vector2i(int(a.x), int(a.y)), String(a.get("dir", "south")))
	shadow_size = float(a.get("shadow", 6.0))
	queue_redraw()


func dist_to_player() -> float:
	return Vector2(tile - (world.player.tile as Vector2i)).length()


func adjacent_to_player() -> bool:
	var d: Vector2i = tile - world.player.tile
	return absi(d.x) + absi(d.y) == 1


## Kill the player with a cause shown on the death screen (see ui.json death_<cause>).
func kill(cause: String, sfx := "") -> void:
	if world._dying:
		return
	if sfx != "":
		Sfx.play(sfx, 0.0)
	world.hud.flash(1, Color(0.6, 0, 0))
	world.die(cause)


func remove() -> void:
	world.actors.erase(self)
	queue_free()
