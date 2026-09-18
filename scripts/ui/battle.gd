class_name Battle
extends CanvasLayer
## Turn-based encounter (placeholder until the combat pass): resolves immediately.

func run(_enemy_id: String, _st: GameState) -> String:
	await get_tree().process_frame
	return "win"
