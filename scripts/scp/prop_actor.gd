extends ScpActor
## A still actor using a character sprite (a corpse that looks alive, a statue, 682 in its
## tank). spec: sprite, dir, event (on talk), anim ("idle"/"walk").

func init(a: Dictionary) -> void:
	super.init(a)
	if a.get("anim", "") == "walk" and sprite.sprite_frames.has_animation("walk_" + facing):
		sprite.play("walk_" + facing)


func talk() -> void:
	if spec.has("event"):
		world.events.run(String(spec.event))
