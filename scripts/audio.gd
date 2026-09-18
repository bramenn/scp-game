extends Node
## Sonido global: efectos (varias voces), ambiente y música en bucle con fundido.
## Los .wav salen de tools/gen_audio.py.

const VOICES := 8

var _sfx: Array[AudioStreamPlayer] = []
var _next := 0
var _amb: AudioStreamPlayer
var _mus: AudioStreamPlayer
var _cache: Dictionary = {}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for i in VOICES:
		var p := AudioStreamPlayer.new()
		add_child(p)
		_sfx.append(p)
	_amb = AudioStreamPlayer.new()
	_mus = AudioStreamPlayer.new()
	add_child(_amb)
	add_child(_mus)


func _stream(name: String, loop := false) -> AudioStreamWAV:
	if not _cache.has(name):
		var s: AudioStreamWAV = load("res://art/audio/%s.wav" % name)
		if loop:
			s.loop_mode = AudioStreamWAV.LOOP_FORWARD
			s.loop_end = int(s.get_length() * s.mix_rate)
		_cache[name] = s
	return _cache[name]


func play(name: String, db := 0.0, pitch := 1.0) -> void:
	var p := _sfx[_next]
	_next = (_next + 1) % VOICES
	p.stream = _stream("sfx_" + name)
	p.volume_db = db
	p.pitch_scale = pitch
	p.play()


func ambience(name: String) -> void:
	_swap(_amb, "amb_" + name if name != "" else "", -8.0)


func music(name: String) -> void:
	_swap(_mus, "mus_" + name if name != "" else "", -6.0)


func _swap(p: AudioStreamPlayer, name: String, db: float) -> void:
	if name != "" and p.stream == _stream(name, true) and p.playing:
		return
	var tw := create_tween()
	if p.playing:
		tw.tween_property(p, "volume_db", -40.0, 0.4)
	tw.tween_callback(func() -> void:
		if name == "":
			p.stop()
			return
		p.stream = _stream(name, true)
		p.volume_db = -40.0
		p.play())
	if name != "":
		tw.tween_property(p, "volume_db", db, 0.8)
