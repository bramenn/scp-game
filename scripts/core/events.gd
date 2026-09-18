class_name EventRunner
extends Node
## Runs data-driven event scripts (data/events.json: {id: [action, ...]}). Every story beat,
## dialogue and scripted scare is an event. Hooks: "enter:<map>", "item:<id>", "door:<id>".

var world: World
var running := 0


func on_map_enter(map_id: String) -> void:
	if Db.events.has("enter:" + map_id):
		run("enter:" + map_id)


func on_item(id: String) -> void:
	if Db.events.has("item:" + id):
		run("item:" + id)


func on_door(id: String) -> void:
	if Db.events.has("door:" + id):
		run("door:" + id)


func run(id: String, who := "") -> void:
	var ev = Db.events.get(id)
	if ev == null:
		push_warning("missing event " + id)
		return
	running += 1
	world.busy += 1
	await exec(ev, who)
	world.busy -= 1
	running -= 1


func exec(actions: Array, who := "") -> void:
	for a in actions:
		if a is String:        # shorthand: plain line
			await world.dialog.say([a], who)
			continue
		if a.has("cond") and not world.st.check(a.cond):
			continue
		await _do(a, who)
		if world._dying:
			return


func _do(a: Dictionary, who: String) -> void:
	var st := world.st
	var speaker: String = a.get("who", who)
	if a.has("say"):
		var lines: Array = a.say if a.say is Array else [a.say]
		await world.dialog.say(lines, speaker)
	elif a.has("choice"):
		var opts: Array = []
		for o in a.choice:
			if st.check(o.get("cond", "")):
				opts.append(o)
		var i: int = await world.dialog.choose(a.get("prompt", ""), opts.map(func(o): return o.text), speaker)
		await exec(opts[i].get("do", []), speaker)
	elif a.has("if"):
		await exec(a.get("then", []) if st.check(a["if"]) else a.get("else", []), who)
	elif a.has("give"):
		st.give(String(a.give), int(a.get("n", 1)))
		var info: Dictionary = Db.items.get(a.give, {})
		Sfx.play("pickup", -4.0)
		world.hud.toast(Loc.ui("received", [Loc.t(info.get("name", a.give))]))
		world._refresh_doors()
	elif a.has("take"):
		st.take(String(a.take), int(a.get("n", 1)))
	elif a.has("mark"):
		st.mark(String(a.mark), a.get("value", true))
	elif a.has("unmark"):
		st.flags.erase(String(a.unmark))
	elif a.has("quest"):
		var q: String = a.quest[0]
		var stage: int = int(a.quest[1])
		var was := st.quest_stage(q)
		st.set_quest(q, stage)
		if stage == -1 and was != -1:
			world.hud.toast(Loc.ui("quest_done", [Loc.t(Db.quests.get(q, {}).get("name", q))]), "gold")
			Sfx.play("quest", -4.0)
		elif was == 0 and stage > 0:
			world.hud.toast(Loc.ui("quest_new", [Loc.t(Db.quests.get(q, {}).get("name", q))]), "gold")
			Sfx.play("quest", -4.0)
		else:
			world.hud.toast(Loc.ui("journal_updated"))
	elif a.has("objective"):
		st.mark("objective", a.objective)
		world.hud.refresh()
	elif a.has("toast"):
		world.hud.toast(Loc.t(a.toast))
	elif a.has("sfx"):
		Sfx.play(String(a.sfx), float(a.get("db", 0.0)), float(a.get("pitch", 1.0)))
	elif a.has("sfx_at"):
		var p: Array = a.sfx_at
		Sfx.play_at(world.view, String(p[0]), Vector2(int(p[1]) * 16 + 8, int(p[2]) * 16 + 8), float(a.get("db", 0.0)))
	elif a.has("music"):
		Sfx.music(String(a.music))
	elif a.has("amb"):
		Sfx.ambience(String(a.amb))
	elif a.has("wait"):
		await world.get_tree().create_timer(float(a.wait)).timeout
	elif a.has("shake"):
		world.hud.shake(world.cam, float(a.shake), float(a.get("power", 3.0)))
	elif a.has("flash"):
		await world.hud.flash(int(a.flash), Color(a.get("color", "#ffffff")))
	elif a.has("fade"):
		await world.hud.fade(a.fade == "out", float(a.get("t", 0.5)))
	elif a.has("lights"):
		await _lights(String(a.lights), float(a.get("t", 1.0)))
	elif a.has("goto"):
		await world.load_map(String(a.goto[0]), String(a.goto[1]))
	elif a.has("npc"):
		await _npc(a)
	elif a.has("door"):
		for d in world.view.doors:
			if d.id == a.door:
				if a.get("open", true):
					world.view.set_door_open(d, true)
					world._door_astar(d, true)
					st.mark("open:" + d.id)
					Sfx.play_at(world.view, "door_open", d.position)
				else:
					world.view.set_door_open(d, false)
					world._door_astar(d, false)
					st.flags.erase("open:" + d.id)
					Sfx.play_at(world.view, "door_close", d.position)
	elif a.has("doc"):
		if not a.doc in st.docs:
			st.docs.append(a.doc)
		await world.menu.read_doc(String(a.doc))
	elif a.has("battle"):
		var res: String = await world.battle(String(a.battle))
		await exec(a.get(res, []), who)
	elif a.has("save"):
		st.save()
		world.hud.toast(Loc.ui("saved"))
	elif a.has("hp"):
		if float(a.hp) < 0:
			world.damage(-float(a.hp), a.get("cause", ""))
		else:
			st.hp = minf(GameState.MAX_HP, st.hp + float(a.hp))
	elif a.has("sanity"):
		st.sanity = clampf(st.sanity + float(a.sanity), 0.0, 100.0)
	elif a.has("battery"):
		st.battery = clampf(st.battery + float(a.battery), 0.0, 100.0)
	elif a.has("ending"):
		await world.ending(String(a.ending))
	elif a.has("call"):
		await world.special(String(a.call), a.get("args", []))
	elif a.has("run"):
		await exec(Db.events.get(String(a.run), []), who)
	elif a.has("cam"):
		await world.hud.pan(world.cam, Vector2(float(a.cam[0]) * 16 + 8, float(a.cam[1]) * 16 + 8) - world.player.position, float(a.get("t", 1.0)))


func _lights(mode: String, t: float) -> void:
	match mode:
		"off":
			Sfx.play("power_down", -2.0)
			for l in world.lights:
				l.set_meta("base", l.energy)
				l.energy = 0.0
				var f: ColorRect = (l.get_meta("fixture") if l.has_meta("fixture") else null)
				if f:
					f.visible = false
		"on":
			Sfx.play("power_up", -4.0)
			for l in world.lights:
				l.energy = float(l.get_meta("base", 1.0))
				var f: ColorRect = (l.get_meta("fixture") if l.has_meta("fixture") else null)
				if f:
					f.visible = true
		"flicker":
			var end := Time.get_ticks_msec() + int(t * 1000)
			while Time.get_ticks_msec() < end:
				for l in world.lights:
					l.visible = randf() > 0.5
				await world.get_tree().create_timer(randf_range(0.03, 0.12)).timeout
			for l in world.lights:
				l.visible = true


func _npc(a: Dictionary) -> void:
	var n: Actor = world.npcs.get(a.npc)
	if a.has("follow"):
		if a.follow:
			world.st.mark("follow:" + a.npc)
		else:
			world.st.flags.erase("follow:" + a.npc)
	if not n:
		return
	if a.has("face"):
		n.face(String(a.face))
	if a.has("move"):
		n.go_to(Vector2i(int(a.move[0]), int(a.move[1])))
		while not n.path.is_empty() or n.moving:
			n.follow_path(0.26)
			await world.get_tree().process_frame
	if a.get("remove", false):
		world.npcs.erase(a.npc)
		world.actors.erase(n)
		var tw := n.create_tween()
		tw.tween_property(n, "modulate:a", 0.0, 0.4)
		tw.tween_callback(n.queue_free)
