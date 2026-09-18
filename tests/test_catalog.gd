extends SceneTree
## Autochequeo del catálogo, mapas y evaluador de triggers. Corre con:
##   godot --headless --path . --script res://tests/test_catalog.gd

var _fail := 0


func _initialize() -> void:
	var cat = load("res://scripts/scp_catalog.gd").new()
	cat.load_all()
	var Trig = load("res://scripts/scp_trigger.gd")

	_check(cat.scps.size() == 5, "hay 5 SCPs (hay %d)" % cat.scps.size())
	for id in cat.scps:
		var s: Dictionary = cat.scps[id]
		if s.has("recompensa"):
			_check(cat.items.has(s.recompensa), "%s: recompensa existe en items" % id)
		_check(cat.items.has(s.get("debilidad", "")), "%s: debilidad existe en items" % id)
		_check((s.get("trigger", []) as Array).size() > 0, "%s tiene trigger" % id)

	_check(cat.maps.has("hub"), "existe el mapa hub")
	_check(cat.maps.size() == 6, "hay 6 mapas (hay %d)" % cat.maps.size())

	for mid in cat.maps:
		var m: Dictionary = cat.maps[mid]
		var rows: Array = m.rows
		var w: int = rows[0].length()
		var ok_w := true
		for r in rows:
			ok_w = ok_w and r.length() == w
		_check(ok_w, "%s: filas del mismo ancho" % mid)
		var txt := "".join(rows)
		if m.get("scp"):
			_check(cat.scps.has(m.scp), "%s: SCP '%s' existe en el catálogo" % [mid, m.scp])
			_check(txt.count("S") == 1, "%s: exactamente un SCP en el mapa" % mid)
		else:
			_check(txt.count("P") == 1, "%s: un punto de inicio P" % mid)
		for c in m.exits:
			var ex: Dictionary = m.exits[c]
			var to: String = ex.get("to", "")
			_check(txt.count(c) == 1, "%s: puerta '%s' aparece una vez" % [mid, c])
			_check(cat.maps.has(to), "%s: salida hacia '%s' existe" % [mid, to])
			var backs: Array = cat.get_map(to).exits.values().map(func(e): return e.get("to"))
			_check(mid in backs, "%s: '%s' tiene puerta de vuelta" % [mid, to])
			if ex.has("nivel"):
				_check(int(ex.nivel) in range(1, 6), "%s: puerta '%s' nivel válido" % [mid, c])
		for c in m.get("items", {}):
			_check(cat.items.has(m.items[c]), "%s: objeto '%s' existe" % [mid, m.items[c]])
		for c in m.get("npcs", {}):
			_check(cat.story.get("npcs", {}).has(m.npcs[c]), "%s: NPC '%s' existe" % [mid, m.npcs[c]])

	for nid in cat.story.get("npcs", {}):
		var npc: Dictionary = cat.story.npcs[nid]
		var diags: Array = npc.get("dialogos", [])
		_check(diags.size() > 0, "NPC %s tiene diálogos" % nid)
		_check(ResourceLoader.exists(npc.get("sprite", "")), "NPC %s: sprite existe" % nid)
		for d in diags:
			for item in d.get("da", []):
				_check(cat.items.has(item), "NPC %s entrega '%s' válido" % [nid, item])

	var GS = load("res://scripts/game_state.gd")
	var gs = GS.new()
	gs.give("tarjeta_1")
	_check(gs.has("tiene:tarjeta_1") and gs.card_level() == 1, "tarjeta da nivel de acceso 1")
	gs.mark("contenido:scp-173")
	_check(gs.contained("scp-173"), "bandera de contención")
	gs.give("botiquin")
	gs.take("botiquin")
	_check(not gs.has("tiene:botiquin"), "take borra el objeto al llegar a 0")
	var dialogo = gs.pick_dialog([{"no": ["contenido:scp-173"], "lineas": ["a"]}, {"lineas": ["b"]}])
	_check(dialogo.lineas[0] == "b", "pick_dialog respeta condiciones")

	for id in cat.scps:
		for mv in cat.scps[id].movimientos:
			_check(mv.has("nombre") and int(mv.get("poder", 0)) > 0, "%s: movimiento válido" % id)

	var B = load("res://scripts/battle.gd")
	_check(B.damage(20, 14, 4) > B.damage(20, 14, 14), "más defensa, menos daño")
	_check(B.damage(1, 1, 99) == 1, "daño mínimo 1")
	_check(B.contain_chance(1, 100) > B.contain_chance(100, 100), "contener es más fácil con el SCP débil")

	var s173: Dictionary = cat.get_scp("scp-173")
	_check(Trig.fires(s173, {"tipo": "entrar_celda"}, {"tiempo_en_celda": 3.0}), "173 dispara tras 2 s en la celda")
	_check(not Trig.fires(s173, {"tipo": "entrar_celda"}, {"tiempo_en_celda": 0.5}), "173 no dispara al instante")
	_check(not Trig.fires(s173, {"tipo": "interactuar"}, {}), "173 no dispara al interactuar")

	var s096: Dictionary = cat.get_scp("scp-096")
	_check(Trig.fires(s096, {"tipo": "interactuar"}, {}), "096 dispara al interactuar")
	_check(not Trig.fires(s096, {"tipo": "entrar_celda"}, {}), "096 no dispara solo al entrar")

	var siempre := {"trigger": [{"tipo": "azar", "p": 1.0}]}
	var nunca := {"trigger": [{"tipo": "azar", "p": 0.0}]}
	_check(Trig.fires(siempre, {}, {}), "azar p=1 dispara")
	_check(not Trig.fires(nunca, {}, {}), "azar p=0 no dispara")

	if _fail == 0:
		print("OK: catálogo, mapas y triggers")
	cat.free()
	quit(_fail)


func _check(cond: bool, msg: String) -> void:
	if cond:
		print("  ok  %s" % msg)
	else:
		_fail += 1
		printerr("  FAIL %s" % msg)
