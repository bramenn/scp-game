class_name EndingScreen
extends CanvasLayer
## Ending slides: data/story.json "endings"[id] = {title, lines[], epilogue conditions}.

func run(id: String, st: GameState) -> void:
	layer = 30
	var root := UiKit.root(self)
	var bg := ColorRect.new()
	bg.color = Color.BLACK
	bg.size = Vector2(UiKit.W, UiKit.H)
	root.add_child(bg)
	var e: Dictionary = Db.story.get("endings", {}).get(id, {})
	var lines: Array = e.get("lines", []).duplicate()
	for ep in e.get("epilogue", []):
		if st.check(ep.get("cond", "")):
			lines.append(ep.text)
	Sfx.music(String(e.get("music", "ending")))
	var title := UiKit.label(Loc.t(e.get("title", id)), 16, UiKit.GOLD)
	title.size = Vector2(UiKit.W, 20)
	title.position = Vector2(0, 40)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.modulate.a = 0.0
	root.add_child(title)
	await create_tween().tween_property(title, "modulate:a", 1.0, 2.0).finished
	for line in lines:
		var l := UiKit.label(Loc.t(line), 8, UiKit.PALE)
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.size = Vector2(380, 60)
		l.position = Vector2(50, 110)
		l.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		l.modulate.a = 0.0
		root.add_child(l)
		var tw := create_tween()
		tw.tween_property(l, "modulate:a", 1.0, 1.2)
		tw.tween_interval(maxf(3.0, Loc.t(line).length() * 0.06))
		tw.tween_property(l, "modulate:a", 0.0, 1.0)
		await tw.finished
		l.queue_free()
	var stats := UiKit.label(Loc.ui("ending_stats", [int(st.play_time / 3600.0), int(fmod(st.play_time, 3600.0) / 60.0),
		st.docs.size(), Db.docs.size(), st.deaths]), 8, UiKit.DIM)
	stats.size = Vector2(UiKit.W, 10)
	stats.position = Vector2(0, 200)
	stats.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	root.add_child(stats)
	await get_tree().create_timer(6.0).timeout
