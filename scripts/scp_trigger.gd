class_name ScpTrigger
extends RefCounted
## Evalúa las condiciones de trigger de un SCP. Set cerrado de primitivas, AND.
## ponytail: sin motor de reglas; añade una primitiva cuando un SCP concreto la exija.

static func fires(scp: Dictionary, evento: Dictionary, ctx: Dictionary) -> bool:
	for cond in scp.get("trigger", []):
		if not _cond_ok(cond, evento, ctx):
			return false
	return true


static func _cond_ok(cond: Dictionary, evento: Dictionary, ctx: Dictionary) -> bool:
	match cond.get("tipo", ""):
		"entrar_celda":
			return evento.get("tipo") == "entrar_celda"
		"interactuar":
			return evento.get("tipo") == "interactuar"
		"accion":
			return evento.get("tipo") == "accion" and evento.get("accion") == cond.get("accion")
		"tiene_item":
			return cond.get("id") in ctx.get("items", [])
		"tiempo_en_celda":
			return float(ctx.get("tiempo_en_celda", 0.0)) >= float(cond.get("s", 0.0))
		"azar":
			return randf() < float(cond.get("p", 1.0))
		_:
			push_warning("Condición desconocida: %s" % cond.get("tipo"))
			return false
