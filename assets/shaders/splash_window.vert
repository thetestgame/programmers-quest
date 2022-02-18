#version 110

uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;
attribute vec4 vertex;
attribute vec4 normal;
attribute vec2 p3d_MultiTexCoord0;

varying vec2 v_clipTexCoord;
varying float v_obliquity; // 0 = camera-coplanar
float pi = 3.14159265359;



void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  v_clipTexCoord = 0.5 * gl_Position.xy + vec2(0.5 * gl_Position.w);
  v_obliquity = acos(
    dot(
      (p3d_ModelViewMatrix * normalize(normal)).xyz,
      vec3(0, 1, 0)
    )
  ) / (pi / 2.0);
}