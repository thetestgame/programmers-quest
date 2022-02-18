  
#version 110

uniform sampler2D background;
uniform float fade;
varying vec2 v_clipTexCoord;
varying float v_obliquity;


void main () {
  vec4 pixel = texture2D(background, v_clipTexCoord * gl_FragCoord.w);

  pixel = (1.0 - v_obliquity) * vec4(1) + v_obliquity * pixel;
  gl_FragColor = pixel * (1.0 - fade);
}