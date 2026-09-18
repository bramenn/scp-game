extends Node
## Localization. English is the source language; Spanish is selectable in Options.
## Data text is either a plain string (English, used as-is) or {"en": ..., "es": ...}.
## UI strings live in data/i18n/ui.json as {key: {"en": ..., "es": ...}}.

signal changed

const LANGS := ["en", "es"]
const SETTINGS := "user://settings.json"

var lang := "en"
var _ui: Dictionary = {}


func _ready() -> void:
	_ui = JSON.parse_string(FileAccess.get_file_as_string("res://data/i18n/ui.json"))
	var s = JSON.parse_string(FileAccess.get_file_as_string(SETTINGS)) if FileAccess.file_exists(SETTINGS) else null
	if s is Dictionary and s.get("lang") in LANGS:
		lang = s.lang
	elif OS.get_locale_language() == "es":
		lang = "es"


## Text from data: {"en","es"} dict, array of those, or a plain string.
func t(v) -> String:
	if v is Dictionary:
		return String(v.get(lang, v.get("en", "")))
	return String(v) if v != null else ""


## UI string by key, with optional format args.
func ui(key: String, args := []) -> String:
	var e = _ui.get(key)
	var s := t(e) if e != null else key
	return s % args if args.size() > 0 else s


func set_lang(l: String) -> void:
	lang = l
	save_setting("lang", l)
	changed.emit()


## Shared user settings file (language, volumes, fullscreen). Merges one key.
static func save_setting(key: String, value) -> void:
	var s = JSON.parse_string(FileAccess.get_file_as_string(SETTINGS)) if FileAccess.file_exists(SETTINGS) else {}
	if not s is Dictionary:
		s = {}
	s[key] = value
	FileAccess.open(SETTINGS, FileAccess.WRITE).store_string(JSON.stringify(s))


static func load_setting(key: String, default = null):
	var s = JSON.parse_string(FileAccess.get_file_as_string(SETTINGS)) if FileAccess.file_exists(SETTINGS) else {}
	return s.get(key, default) if s is Dictionary else default
