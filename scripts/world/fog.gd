class_name Fog
extends ColorRect
## World-space drifting fog. Drawn above actors and lit by lights (so the flashlight
## beam glows in it). Pixelated and posterized to stay coherent with the pixel art.

const SHADER := """
shader_type canvas_item;
uniform sampler2D noise : repeat_enable, filter_nearest;
uniform vec4 fog_color : source_color = vec4(0.6, 0.62, 0.68, 1.0);
uniform float density = 0.3;
uniform vec2 world_px = vec2(640.0, 480.0);
uniform vec2 speed = vec2(0.012, 0.004);
void fragment() {
	vec2 p = floor(UV * world_px / 2.0) * 2.0;           // 2px blocks
	vec2 uv = p / 220.0;
	float n = texture(noise, uv + TIME * speed).r * 0.6
		+ texture(noise, uv * 1.9 - TIME * speed * 1.7).r * 0.4;
	float a = smoothstep(0.35, 0.85, n) * density;
	a = floor(a * 8.0) / 8.0;                             // posterize
	COLOR = vec4(fog_color.rgb, a);
}
"""

static var _mat_shader: Shader
static var _noise: NoiseTexture2D


func setup(size_px: Vector2, fog_col: Color, density: float) -> void:
	if not _mat_shader:
		_mat_shader = Shader.new()
		_mat_shader.code = SHADER
		_noise = NoiseTexture2D.new()
		_noise.seamless = true
		_noise.width = 256
		_noise.height = 256
		var fn := FastNoiseLite.new()
		fn.frequency = 0.012
		fn.fractal_octaves = 3
		_noise.noise = fn
	var m := ShaderMaterial.new()
	m.shader = _mat_shader
	m.set_shader_parameter("noise", _noise)
	m.set_shader_parameter("fog_color", fog_col)
	m.set_shader_parameter("density", density)
	m.set_shader_parameter("world_px", size_px)
	material = m
	size = size_px
	self.color = Color.WHITE
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	z_index = 20
