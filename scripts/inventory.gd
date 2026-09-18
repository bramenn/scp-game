class_name Inventory
extends CanvasLayer
## Pantalla de inventario: objetos con ícono, descripción y estadísticas. E usa consumibles.

const W := 480
const H := 270
const ORDER := ["llave", "debilidad", "mejora", "consumible", "doc"]
const GROUP := {"llave": "ACCESO", "debilidad": "CONTENCIÓN", "mejora": "EQUIPO", "consumible": "CURACIÓN", "doc": "DOCUMENTO"}

signal closed

var _st: GameState
var _items: Dictionary
var _ids: Array = []
var _cursor := 0
var _list: VBoxContainer
var _title: Label
var _desc: Label
var _stats: Label
var _icon: TextureRect


func open(st: GameState, items: Dictionary) -> void:
	_st = st
	_items = items
	layer = 8
	var root := Control.new()
	root.theme = Hud.make_theme()
	root.size = Vector2(W, H)
	add_child(root)
	var dim := ColorRect.new()
	dim.color = Color(0, 0, 0, 0.6)
	dim.size = Vector2(W, H)
	root.add_child(dim)

	var left := PanelContainer.new()
	left.add_theme_stylebox_override("panel", Hud.panel_style(Color("e8c440")))
	left.position = Vector2(12, 12)
	left.custom_minimum_size = Vector2(200, H - 24)
	var lv := VBoxContainer.new()
	var head := Label.new()
	head.text = "INVENTARIO · AGENTE VEGA"
	head.add_theme_color_override("font_color", Color("e8c440"))
	lv.add_child(head)
	_list = VBoxContainer.new()
	_list.add_theme_constant_override("separation", 1)
	lv.add_child(_list)
	left.add_child(lv)
	root.add_child(left)

	var right := PanelContainer.new()
	right.position = Vector2(220, 12)
	right.custom_minimum_size = Vector2(W - 232, H - 24)
	var rv := VBoxContainer.new()
	rv.add_theme_constant_override("separation", 6)
	_stats = Label.new()
	_icon = TextureRect.new()
	_icon.custom_minimum_size = Vector2(32, 32)
	_icon.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
	_icon.scale = Vector2(2, 2)
	_title = Label.new()
	_title.add_theme_font_size_override("font_size", 16)
	_desc = Label.new()
	_desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	_desc.custom_minimum_size = Vector2(W - 250, 0)
	for c in [_stats, _icon, _title, _desc]:
		rv.add_child(c)
	right.add_child(rv)
	root.add_child(right)
	_refresh()


func _refresh() -> void:
	_ids = _st.inv.keys()
	_ids.sort_custom(func(a: String, b: String) -> bool:
		var ta := ORDER.find(_items[a].tipo)
		var tb := ORDER.find(_items[b].tipo)
		return ta < tb if ta != tb else a < b)
	_cursor = clampi(_cursor, 0, maxi(0, _ids.size() - 1))
	for c in _list.get_children():
		c.queue_free()
	for i in _ids.size():
		var id: String = _ids[i]
		var row := HBoxContainer.new()
		var ic := TextureRect.new()
		ic.texture = _icon_for(id)
		ic.custom_minimum_size = Vector2(16, 12)
		ic.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
		var l := Label.new()
		var n: int = _st.inv[id]
		l.text = _items[id].nombre + (" x%d" % n if n > 1 else "")
		l.add_theme_color_override("font_color", Color("e8c440") if i == _cursor else Color("d0d2d6"))
		row.add_child(ic)
		row.add_child(l)
		_list.add_child(row)
	_stats.text = "Vida %d/%d   ATQ %d   DEF %d" % [_st.hp, GameState.BASE.hp, _st.stat("atk", _items), _st.stat("def", _items)]
	if _ids.is_empty():
		_title.text = "Vacío"
		_desc.text = "Explora las celdas y habla con los supervivientes."
		_icon.texture = null
		return
	var it: Dictionary = _items[_ids[_cursor]]
	_icon.texture = _icon_for(_ids[_cursor])
	_title.text = it.nombre
	_desc.text = "[%s]\n%s" % [GROUP.get(it.tipo, ""), it.desc]
	if it.tipo == "consumible":
		_desc.text += "\n\nE: usar"


func _icon_for(id: String) -> Texture2D:
	var p := "res://art/items/%s.png" % ("doc" if id.begins_with("doc_") else id)
	return load(p) if ResourceLoader.exists(p) else null


func _unhandled_input(event: InputEvent) -> void:
	if not (event is InputEventKey or event is InputEventAction) or not event.is_pressed() or event.is_echo():
		return
	get_viewport().set_input_as_handled()
	if event.is_action_pressed("ui_cancel") or (event is InputEventKey and event.physical_keycode in [KEY_I, KEY_TAB]):
		Sfx.play("move")
		closed.emit()
		queue_free()
	elif event.is_action_pressed("ui_down") and _ids.size() > 0:
		_cursor = (_cursor + 1) % _ids.size()
		Sfx.play("move")
		_refresh()
	elif event.is_action_pressed("ui_up") and _ids.size() > 0:
		_cursor = (_cursor - 1 + _ids.size()) % _ids.size()
		Sfx.play("move")
		_refresh()
	elif event.is_action_pressed("ui_accept") and _ids.size() > 0:
		var id: String = _ids[_cursor]
		if _items[id].tipo == "consumible" and _st.hp < GameState.BASE.hp:
			_st.take(id)
			_st.hp = mini(GameState.BASE.hp, _st.hp + int(_items[id].cura))
			Sfx.play("heal")
			_refresh()
