#version 100

uniform mat4 p3d_ModelViewProjectionMatrix;
attribute vec4 vertex;
attribute vec2 p3d_MultiTexCoord0;

varying vec2 v_texcoord;

void main()  {
  gl_Position = p3d_ModelViewProjectionMatrix * vertex;
  v_texcoord = p3d_MultiTexCoord0;
}
