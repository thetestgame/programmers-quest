#version 100

precision mediump float;
uniform sampler2D p3d_Texture0;
varying vec2 v_texcoord;
uniform float fade;
uniform float time;
uniform int pattern;
uniform int colors;
uniform float pattern_freq;
uniform float cycle_freq;


float pi = 3.14159265358;

// Basic patterns
// Turn the texture coordinates into a greyscale pattern

float concentric_circles() {
  return pow(v_texcoord.x - 0.5, 2.0) + pow(v_texcoord.y - 0.5, 2.0);
}


float flickering () {
  return mod(0.0, 1.0);
}


float squarestar () {
  return min(abs(v_texcoord.x - 0.5), abs(v_texcoord.y - 0.5));
}


float noise () {
  return sin(mod(v_texcoord.x * 100000.0 + v_texcoord.y * 100000.0 + time * 100000.0, 1.0)) / 2.0 + 0.5;
}


float double_wheel () {
  return acos(dot(normalize(v_texcoord - vec2(0.5, 0.5)), vec2(0, 1))) / pi;
}


float wheel () {
  float angle = acos(
    dot(normalize(v_texcoord - vec2(0.5, 0.5)), vec2(0, 1))
  ) / pi;
  if (v_texcoord.x <= 0.5) {
    return angle / 2.0;
  } else {
    return 1.0 - angle / 2.0;
  }
}


// Colorization
// Turn greyscale value into RGBA vector

vec4 direct(float v) {
  return vec4(v, v, v, 0);
}


vec4 rainbow(float v) {
  float phase = mod(v * 6.0, 1.0);
  vec2 phases = vec2(
    phase, // rising
    1.0 - phase // falling
  );
  
  int section = int(floor(v * 6.0));
  vec4 rgb = vec4(0.0);
  if (section == 0) {rgb = vec4(1.0,      phases.x, 0.0,      0.0);}
  if (section == 1) {rgb = vec4(phases.y, 1.0,      0.0,      0.0);}
  if (section == 2) {rgb = vec4(0.0,      1.0,      phases.x, 0.0);}
  if (section == 3) {rgb = vec4(0.0,      phases.y, 1.0,      0.0);}
  if (section == 4) {rgb = vec4(phases.x, 0.0,      1.0,      0.0);}
  if (section == 5) {rgb = vec4(1.0,      0.0,      phases.y, 0.0);}

  // Sinate colors
  rgb = cos(rgb * pi / 2.0);

  return rgb;
}


vec4 rgb_bands(float v) {
  float phase = mod(v * 3.0, 1.0);
  vec2 phases = vec2(
    phase, // rising
    1.0 - phase // falling
  );
  
  int section = int(floor(v * 3.0));
  vec4 rgb = vec4(0.0);
  if (section == 0) {rgb = vec4(phases.y, phases.x, 0.0,      0.0);}
  if (section == 1) {rgb = vec4(0.0,      phases.y, phases.x, 0.0);}
  if (section == 2) {rgb = vec4(phases.x, 0.0,      phases.y, 0.0);}

  return rgb;
}


// Putting it all together

void main () {
  // Basic pattern
  float v;
  if (pattern == 0) {v = concentric_circles();}
  if (pattern == 1) {v = flickering        ();}
  if (pattern == 2) {v = squarestar        ();}
  if (pattern == 3) {v = noise             ();}
  if (pattern == 4) {v = double_wheel      ();}
  if (pattern == 5) {v = wheel             ();}

  // Scaling and movement
  v = mod(v * pattern_freq - time * cycle_freq, 1.0);

  // Colorization
  vec4 rgb;
  if (colors == 0) {rgb = direct   (v);}
  if (colors == 1) {rgb = rainbow  (v);}
  if (colors == 2) {rgb = rgb_bands(v);}

  // ...and respect the fade state before sending it off to the fragment buffer
  gl_FragColor = rgb * (1.0 - fade);
}
